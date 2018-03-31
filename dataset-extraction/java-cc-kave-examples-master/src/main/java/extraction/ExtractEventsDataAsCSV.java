package extraction;

import cc.kave.commons.model.events.CommandEvent;
import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.model.events.testrunevents.TestCaseResult;
import cc.kave.commons.model.events.testrunevents.TestResult;
import cc.kave.commons.model.events.testrunevents.TestRunEvent;
import cc.kave.commons.model.events.visualstudio.BuildEvent;
import cc.kave.commons.model.events.visualstudio.BuildTarget;
import cc.kave.commons.model.events.visualstudio.EditEvent;
import cc.kave.commons.model.events.visualstudio.FindEvent;
import cc.kave.commons.utils.io.IReadingArchive;
import cc.kave.commons.utils.io.ReadingArchive;
import examples.IoHelper;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.List;
import java.util.Set;

public class ExtractEventsDataAsCSV {
    private String dir;
    public boolean editEvent, testEvent, commandEvent, buildEvent;

    public ExtractEventsDataAsCSV(String dir, boolean editEvent, boolean testEvent, boolean commandEvent, boolean buildEvent) {
        this.dir = dir;
        this.editEvent = editEvent;
        this.testEvent = testEvent;
        this.commandEvent = commandEvent;
        this.buildEvent = buildEvent;
    }

    public void run() {
        Set<String> zips = IoHelper.findAllZips(dir);
        BufferedWriter writer = null;
        String filenamePrefix = "../../data/csv_data_";
        int zipTotal = zips.size();
        int zipCount = 0;
        for (String zip : zips) {
            zipCount++;
            //if(zipCount<=10) continue;
            if (zipCount == 21) break;
            String fileName = filenamePrefix + zip.toString().subSequence(0, 10);
            System.out.printf("Processing" + fileName+ "\n");
            BufferedWriter testEventWriter = null, editEventWriter = null, commandEventWriter = null, buidEventWriter = null;
            try {
                if (testEvent) testEventWriter = new BufferedWriter(new FileWriter(fileName + "_test.csv", true));
                if (editEvent) editEventWriter = new BufferedWriter(new FileWriter(fileName + "_edit.csv", true));
                if(commandEvent) commandEventWriter  =new BufferedWriter(new FileWriter(fileName + "_command.csv", true));
                if (buildEvent) buidEventWriter = new BufferedWriter(new FileWriter(fileName + "_failed_build.csv", true));
            } catch (IOException e) {
                e.printStackTrace();
            }
            double perc = 100 * zipCount / (double) zipTotal;

            System.out.printf("## %s, processing %s... (%d/%d, %.1f%% done)\n", new Date(), zip, zipCount, zipTotal,
                    perc);
            File zipFile = Paths.get(dir, zip).toFile();

            //Map<String, Integer> keyMap = Maps.newHashMap();

            int printCounter = 0;
            try (IReadingArchive ra = new ReadingArchive(zipFile)) {
                while (ra.hasNext()) {
                    IIDEEvent e = ra.getNext(IIDEEvent.class);
                    if (testEvent && e instanceof TestRunEvent) {
                        TestRunEvent testRunEvent = (TestRunEvent) e;
                        if (testRunEvent.WasAborted) continue;

                        int successCount = 0;
                        int failedCount = 0;
                        float total = (float) testRunEvent.Tests.size();
                        //System.out.println(total);
                        String time = testRunEvent.getTriggeredAt().format(DateTimeFormatter.ISO_LOCAL_DATE);
                        for (TestCaseResult x : testRunEvent.Tests) {
                            if (x.Result.equals(TestResult.Success))   successCount++;
                            else if (x.Result.equals(TestResult.Failed))    failedCount++;
                        }
                        if(failedCount == 0) continue;
                        String info = time + ","
                                + testRunEvent.Duration.getSeconds() + ","
                                + successCount/total + ","
                                + failedCount/total + "\r\n";
                        testEventWriter.append(info);
                        //System.out.println(info);

                    }
                    if (editEvent && e instanceof EditEvent) {
                        EditEvent editEvent = (EditEvent) e;
                        String time = editEvent.getTriggeredAt().format(DateTimeFormatter.ISO_LOCAL_DATE);
                        String info = //editEvent.IDESessionUUID + "," +
                                 time + ","
                                + editEvent.Duration.getSeconds() + ","
                                + editEvent.NumberOfChanges + ","
                                + editEvent.SizeOfChanges + "\r\n";
                        editEventWriter.append(info);
                    }
                    if (commandEvent && e instanceof CommandEvent) {
                        CommandEvent commandEvent = (CommandEvent) e;
                        String info =
                                //commandEvent.IDESessionUUID+ "," +
                          commandEvent.getCommandId() + ","
                          + commandEvent.TriggeredAt.toEpochSecond() + ","
                          + commandEvent.TriggeredBy.name()
                              +  "\r\n";
                        commandEventWriter.append(info);
                    }

                    if (buildEvent && e instanceof BuildEvent) {
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
                        buidEventWriter.append(info);
                        //System.out.println(info);
                    }

                }
            } catch (IOException e) {
                e.printStackTrace();
            }

        }

        System.out.printf("Done (%s)\n", new Date());
    }
}