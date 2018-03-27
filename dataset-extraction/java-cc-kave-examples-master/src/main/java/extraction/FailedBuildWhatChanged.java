package extraction;


import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.model.events.visualstudio.BuildEvent;
import cc.kave.commons.model.events.visualstudio.BuildTarget;
import cc.kave.commons.model.events.visualstudio.EditEvent;
import cc.kave.commons.model.ssts.declarations.IMethodDeclaration;
import cc.kave.commons.utils.io.ReadingArchive;
import examples.IoHelper;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;

public class FailedBuildWhatChanged {
    private static final String DIR_USERDATA = "Events-170301-2";
    static String outputPath  = "../../data/";
    static int count = 0;

    public FailedBuildWhatChanged() throws IOException {

    }

    public static void readAllEvents() throws IOException {
        // each .zip file corresponds to a user
        Set<String> userZips = IoHelper.findAllZips(DIR_USERDATA);
        SizedStack<String> edits = new SizedStack<>(50);
        for (String user : userZips) {
            String userId = (String) user.subSequence(0, 10);
            System.out.println("Processing " + userId);
            BufferedWriter failedBuildEventsWriter, codeChangeWriter;
            failedBuildEventsWriter = new BufferedWriter(new FileWriter(outputPath + userId + "_FailedBuild.csv"));
            codeChangeWriter = new BufferedWriter(new FileWriter(outputPath + userId + "_changeRF.csv"));
            codeChangeWriter.append("id,time,change,no_of_events\r\n");
            failedBuildEventsWriter.append("id,time,scope,action,project,soln_config\r\n");
            File zipFile = Paths.get(DIR_USERDATA, user).toFile();
            ReadingArchive ra = new ReadingArchive(zipFile);
            while (ra.hasNext()) {
                IIDEEvent e = ra.getNext(IIDEEvent.class);
                try {
                    if (e instanceof BuildEvent) {
                        BuildEvent event = (BuildEvent) e;
                        List<BuildTarget> l = event.Targets;
                        for (BuildTarget x : l) {
                            if (!x.Successful) {
                                String time = Long.toString(x.StartedAt.toEpochSecond(), 10);
                                //System.out.println(x.Project + ", " + x.Platform + ", " + x.ProjectConfiguration +" ," + x.SolutionConfiguration );
                                //System.out.println(event.Action + "," + event.getTriggeredAt() + "," + x.Successful);
                                String info = count
                                        + "," + time
                                        + "," + event.Scope
                                        + "," + event.Action
                                        + "," + x.Project
                                        + "," + x.SolutionConfiguration
                                        + "\r\n";
                                //System.out.print(info);
                                failedBuildEventsWriter.append(info);
                                int noOfEditEvent = edits.size();
                                codeChangeWriter.append(count + "," + time + ",");
                                //System.out.println("Size : " + edits.size());
                                while (!edits.isEmpty()) {
                                    //System.out.println();
                                    codeChangeWriter.append(edits.pop() + " ");
                                }
                                codeChangeWriter.append("," + noOfEditEvent + "\r\n");
                                //System.out.println();
                                count++;
                            }
                        }
                    } else if (e instanceof EditEvent) {
                        EditEvent event = (EditEvent) e;
                        Set<IMethodDeclaration> set = event.Context2.getSST().getMethods();
                        StringBuilder info = new StringBuilder();
                        for (IMethodDeclaration m : set) {
                            String method = m.getName().getFullName();
                            if (method.length() <= 2) continue;
                            info.append(method);
                            info.append(" ");
                        }
                        String methods = info.toString().trim();
                        if (methods.length() > 3) edits.push(info.toString());
                    }
                    //process(e);
                } catch (NullPointerException ne) {
                }
            }
            ra.close();
            codeChangeWriter.flush();
            codeChangeWriter.close();
            failedBuildEventsWriter.flush();
            failedBuildEventsWriter.close();
        }
    }




    public static void main(String[] args) throws IOException {
        readAllEvents();
    }
}
