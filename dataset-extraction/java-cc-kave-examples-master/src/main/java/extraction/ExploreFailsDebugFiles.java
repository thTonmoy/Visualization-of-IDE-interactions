package extraction;

import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.model.events.testrunevents.TestCaseResult;
import cc.kave.commons.model.events.testrunevents.TestResult;
import cc.kave.commons.model.events.testrunevents.TestRunEvent;
import cc.kave.commons.model.events.visualstudio.BuildEvent;
import cc.kave.commons.model.events.visualstudio.BuildTarget;
import cc.kave.commons.model.events.visualstudio.DebuggerEvent;
import cc.kave.commons.utils.io.ReadingArchive;
import examples.IoHelper;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.util.List;
import java.util.Set;

public class ExploreFailsDebugFiles {
    private static final String DIR_USERDATA = "Events-170301-2";
    static BufferedWriter writer;

    static {
        try {
            writer = new BufferedWriter(new FileWriter("../../data/cluster_data_lang.csv"));
            writer.append("type,lang,duration,success,fail\r\n");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    ;
    //maping : Debug:0, Test:1, Build 2

    public static void readAllEvents() throws IOException {
        // each .zip file corresponds to a user
        Set<String> userZips = IoHelper.findAllZips(DIR_USERDATA);
        //int count =0;
        for (String user : userZips) {
           // count++;
            //if(count<41) continue;
            String userId = (String) user.subSequence(0, 10);
            System.out.println("Processing " + userId);
            File zipFile = Paths.get(DIR_USERDATA, user).toFile();
            ReadingArchive ra = new ReadingArchive(zipFile);
            while (ra.hasNext()) {
                IIDEEvent e = ra.getNext(IIDEEvent.class);
                try {
                    if (e instanceof TestRunEvent) {
                        TestRunEvent testRunEvent = (TestRunEvent) e;
                        if (testRunEvent.WasAborted) continue;
                        int succesCount = 0;
                        int failedCount = 0;
                        for (TestCaseResult x : testRunEvent.Tests) {
                            if (x.Result.equals(TestResult.Success)) succesCount++;
                            else if (x.Result.equals(TestResult.Failed)) {
                                failedCount++;
                            }
                        }
                        String info = "1" + ","
                                + testRunEvent.ActiveDocument.getLanguage() + ","
                                + testRunEvent.Duration.getSeconds() + ","
                                + succesCount + ","
                                + failedCount + "\r\n";
                        //System.out.print(info);
                        writer.append(info);

                    }
                    if (e instanceof BuildEvent) {
                        BuildEvent event = (BuildEvent) e;
                        List<BuildTarget> l = event.Targets;
                        float total = (float) l.size();
                        int failCount = 0;
                        int successCount = 0;
                        for (BuildTarget x : l) {
                            if (!x.Successful) failCount++;
                            else successCount++;
                        }

                        String info = "2" + ","
                                + event.ActiveDocument.getLanguage() + ","
                                + event.Duration.getSeconds() + ","
                                + successCount + ","
                                + failCount + "\r\n";
                       // System.out.println(info);
                        writer.append(info);
                    } else if (e instanceof DebuggerEvent) {
                        DebuggerEvent event = (DebuggerEvent) e;
                        String info = "0" + ","
                                + event.ActiveDocument.getLanguage() + ","
                                + event.Duration.getSeconds() + ","
                                + "0" + ","
                                + "0" + "\r\n";
                        //System.out.println(info);
                        writer.append(info);
                    }
                } catch (NullPointerException ne) {
                }
            }
            ra.close();
            writer.flush();
        }
        writer.close();
    }

    public static void main(String[] args) throws IOException {
        readAllEvents();
    }
}