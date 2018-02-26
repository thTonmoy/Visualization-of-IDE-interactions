package extraction;

import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.model.events.testrunevents.TestCaseResult;
import cc.kave.commons.model.events.testrunevents.TestResult;
import cc.kave.commons.model.events.testrunevents.TestRunEvent;
import cc.kave.commons.model.events.visualstudio.EditEvent;
import cc.kave.commons.utils.io.IReadingArchive;
import cc.kave.commons.utils.io.ReadingArchive;
import com.google.common.collect.Maps;
import examples.IoHelper;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Date;
import java.util.Map;
import java.util.Set;

public class ExtractEditAndTestData {
    private String dir;

    public ExtractEditAndTestData(String dir) {
        this.dir = dir;
    }

    public void run() {
        Set<String> zips = IoHelper.findAllZips(dir);
        BufferedWriter writer = null;
        String filenamePrefix = "transformed_data_";
        int zipTotal = zips.size();
        int zipCount = 0;
        for (String zip : zips) {
            String fileName = filenamePrefix +  zip.toString().subSequence(0,10);
            BufferedWriter testEventWriter= null, editEventWriter = null;
            try {
                testEventWriter = new BufferedWriter(new FileWriter(fileName + "_test.csv", true));
                editEventWriter = new BufferedWriter(new FileWriter(fileName + "_edit.csv", true));
            } catch (IOException e) {
                e.printStackTrace();
            }
            double perc = 100 * zipCount / (double) zipTotal;
            zipCount++;
            if(zipCount == 5) break;

            System.out.printf("## %s, processing %s... (%d/%d, %.1f%% done)\n", new Date(), zip, zipCount, zipTotal,
                    perc);
            File zipFile = Paths.get(dir, zip).toFile();

            //Map<String, Integer> keyMap = Maps.newHashMap();

            int printCounter = 0;
            try (IReadingArchive ra = new ReadingArchive(zipFile)) {
                while (ra.hasNext()) {
                    if (printCounter++ % 10000 == 0) {
                        System.out.printf(".\n");
                    }
                    IIDEEvent e = ra.getNext(IIDEEvent.class);
                    if(e instanceof TestRunEvent){
                        TestRunEvent testRunEvent = (TestRunEvent) e;
                        if(testRunEvent.WasAborted) continue;

                        int succesCount = 0;
                        int failedCount = 0;
                        for(TestCaseResult x: testRunEvent.Tests){
                            if(x.Result.equals(TestResult.Success)) succesCount++;
                            else if(x.Result.equals(TestResult.Failed)) failedCount++;
                        }
                        String info = testRunEvent.IDESessionUUID + ","
                                + testRunEvent.TriggeredAt.toEpochSecond() + ","
                                + testRunEvent.Duration.getSeconds() + ","
                                + succesCount+ ","
                                + failedCount+  "\r\n";
                        testEventWriter.append(info);

                    }
                    else if(e instanceof EditEvent){
                        EditEvent editEvent = (EditEvent) e;
                        String info = editEvent.IDESessionUUID + ","
                                + editEvent.TriggeredAt.toEpochSecond() + ","
                                + editEvent.Duration.getSeconds() + ","
                                + editEvent.NumberOfChanges + ","
                                + editEvent.SizeOfChanges + "\r\n";
                        editEventWriter.append(info);
                    }

                }
            } catch (IOException e) {
               e.printStackTrace();
            }

        }

        System.out.printf("Done (%s)\n", new Date());
    }
}