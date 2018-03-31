package extraction;


import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.model.events.testrunevents.TestCaseResult;
import cc.kave.commons.model.events.testrunevents.TestResult;
import cc.kave.commons.model.events.testrunevents.TestRunEvent;
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
import java.time.format.DateTimeFormatter;
import java.util.List;
import java.util.Set;

public class ExploringTestsAndBuilds {
    private static final String DIR_USERDATA = "Events-170301-2";
    static String outputPath  = "../../data/";
    static BufferedWriter failedBuildEventsWriter, codeChangeWriter, testEventWriter;
    static SizedStack<String> edits = new SizedStack<>(40);
    static int count = 0;

    public ExploringTestsAndBuilds() throws IOException {

    }

    private static void createFileWriters(String userId) throws IOException {
        failedBuildEventsWriter = new BufferedWriter(new FileWriter(outputPath + userId + "_FailedBuild.csv"));
        //codeChangeWriter = new BufferedWriter(new FileWriter(outputPath + userId + "_change.csv"));
        //codeChangeWriter.append("id,time,change,no_of_events\r\n");
        failedBuildEventsWriter.append("id,time,scope,action,project,soln_config\r\n");
        //testEventWriter = new BufferedWriter(new FileWriter(outputPath + userId + "_changeRF.csv"));;
    }

    public static void readAllEvents() throws IOException {
        // each .zip file corresponds to a user
        Set<String> userZips = IoHelper.findAllZips(DIR_USERDATA);
        for (String user : userZips) {
            String userId = (String) user.subSequence(0, 10);
            System.out.println("Processing " + userId);
            createFileWriters(userId);
            File zipFile = Paths.get(DIR_USERDATA, user).toFile();
            ReadingArchive ra = new ReadingArchive(zipFile);
            while (ra.hasNext()) {
                IIDEEvent e = ra.getNext(IIDEEvent.class);
                try {
                    /*if (e instanceof TestRunEvent) {
                        TestRunEvent testRunEvent = (TestRunEvent) e;
                        if (testRunEvent.WasAborted) continue;

                        int succesCount = 0;
                        int failedCount = 0;
                        float total = testRunEvent.Tests.size();
                        String time = Long.toString(testRunEvent.TriggeredAt.toEpochSecond(),10);
                        for (TestCaseResult x : testRunEvent.Tests) {
                            if (x.Result.equals(TestResult.Success))   succesCount++;
                            else if (x.Result.equals(TestResult.Failed)){
                                failedCount++;
                                System.out.print(x.TestMethod.getFullName());
                            }
                        }
                        if(failedCount == 0) continue;
                        String info = count + ","
                                + time + ","
                                + testRunEvent.Duration.getSeconds() + ","
                                + succesCount/total + ","
                                + failedCount/total + "\r\n";
                        //testEventWriter.append(info);
                        //savePreviousEditData(time);
                        System.out.print(info);

                    }*/
                    if (e instanceof BuildEvent) {
                        BuildEvent event = (BuildEvent) e;
                        List<BuildTarget> l = event.Targets;
                        float total = (float) l.size();
                        int failCount = 0;
                        for (BuildTarget x : l) {
                            if (!x.Successful)  failCount++;
                        }

                        String time = event.getTriggeredAt().format(DateTimeFormatter.ISO_LOCAL_DATE);
                        String info = time + ","
                                + failCount/total + "\r\n";
                        failedBuildEventsWriter.append(info);
                        failedBuildEventsWriter.flush();
                        //System.out.println(info);
                        /*BuildEvent event = (BuildEvent) e;
                        List<BuildTarget> l = event.Targets;
                        boolean isFailed = false;
                        for (BuildTarget x : l) {
                            if (!x.Successful) {
                                isFailed = true;
                                break;
                            }
                        }
                        if(isFailed){
                            String time = Long.toString(event.getTriggeredAt().toEpochSecond(), 10);
                            //System.out.println(x.Project + ", " + x.Platform + ", " + x.ProjectConfiguration +" ," + x.SolutionConfiguration );
                            //System.out.println(event.Action + "," + event.getTriggeredAt() + "," + x.Successful);
                            String info = count
                                    + "," + time
                                    + "," + event.Scope
                                    + "," + event.Action
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
                    }*/
                        //process(e);
                    }
                } catch (NullPointerException ne) {
                }
            }
            ra.close();
            //codeChangeWriter.flush();
            //codeChangeWriter.close();
            failedBuildEventsWriter.flush();
            failedBuildEventsWriter.close();
        }
    }


    static void savePreviousEditData(String time) throws IOException {
        int noOfEditEvent = edits.size();
        codeChangeWriter.append(count + "," + time + ",");
        //System.out.println("Size : " + edits.size());
        while (!edits.isEmpty()) {
            //System.out.println(edits.pop() + " ");
            codeChangeWriter.append(edits.pop() + " ");
        }
        codeChangeWriter.append("," + noOfEditEvent + "\r\n");
       // System.out.println(", no: " + noOfEditEvent);
    }


    public static void main(String[] args) throws IOException {
        readAllEvents();
    }
}
