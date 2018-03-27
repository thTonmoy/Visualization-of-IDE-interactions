package examples;

import cc.kave.commons.model.events.ActivityEvent;
import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.model.events.NavigationEvent;
import cc.kave.commons.model.events.testrunevents.TestCaseResult;
import cc.kave.commons.model.events.testrunevents.TestResult;
import cc.kave.commons.model.events.testrunevents.TestRunEvent;
import cc.kave.commons.model.events.versioncontrolevents.VersionControlAction;
import cc.kave.commons.model.events.versioncontrolevents.VersionControlEvent;
import cc.kave.commons.model.events.visualstudio.BuildEvent;
import cc.kave.commons.model.events.visualstudio.BuildTarget;
import cc.kave.commons.model.events.visualstudio.DebuggerEvent;
import cc.kave.commons.model.events.visualstudio.EditEvent;
import cc.kave.commons.utils.io.IReadingArchive;
import cc.kave.commons.utils.io.ReadingArchive;
import com.google.common.collect.Maps;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.util.Date;
import java.util.List;
import java.util.Map;
import java.util.Set;

public class CountEventTypeExample {

    private String dir;
    Map<String, Integer> keyMap = Maps.newHashMap();
    ZonedDateTime lastExecTim = ZonedDateTime.now();
    boolean xx= false;

    public CountEventTypeExample(String dir) {
        this.dir = dir;
    }

    public void run() {
        Set<String> zips = IoHelper.findAllZips(dir);
        BufferedWriter writer = null;
        int keyCount = 0;
        try {
            writer = new BufferedWriter(new FileWriter("test_events_h.csv"));
        } catch (IOException e) {
            e.printStackTrace();
        }

        int zipTotal = zips.size();
        int zipCount = 0;
        for (String zip : zips) {
            double perc = 100 * zipCount / (double) zipTotal;
            if (zipCount == 51) break;
            zipCount++;
            if (zipCount < 45) continue;

            System.out.printf("## %s, processing %s... (%d/%d, %.1f%% done)\n", new Date(), zip, zipCount, zipTotal,
                    perc);
            File zipFile = Paths.get(dir, zip).toFile();

            int printCounter = 0;
            try (IReadingArchive ra = new ReadingArchive(zipFile)) {
                while (ra.hasNext()) {
                    if (printCounter++ % 50000 == 0) {
                        System.out.printf(".\n");
                    }
                    IIDEEvent e = ra.getNext(IIDEEvent.class);
//                    ZonedDateTime tm = e.getTriggeredAt();
//                    if(tm.isEqual(lastExecTim)) continue;
//                    lastExecTim = tm;

                    if(xx && (keyCount + 25) < printCounter && keyCount > 0)  xx = false;

                    if (e instanceof BuildEvent) {
                        BuildEvent event = (BuildEvent) e;
                        System.out.println(e);
                        /*List<BuildTarget> l = event.Targets;
                        for(BuildTarget x: l){
                            //if(!x.Successful){
                                keyCount = printCounter;
                                xx = true;
                                System.out.println(x.Project + ", " + x.Platform + ", " + x.ProjectConfiguration +" ," + x.SolutionConfiguration );
                                System.out.println(event.Action + "," + event.getTriggeredAt() + "," + x.Successful);
                           // }
                        }*/
                    }
                    if (xx && e instanceof DebuggerEvent) {
                        DebuggerEvent event = (DebuggerEvent) e;

                                System.out.println(event.Reason + ", " + event.Mode );
                                System.out.println(event.Action + "," + event.getTriggeredAt() + "," + event.IDESessionUUID);
                    }
                    /*eventCount++;
                    String key = e.getClass().getSimpleName();

                    if (!keyMap.containsKey(key)) {
                        keyMap.put(key, keyCount++);
                    }

                    ZonedDateTime trigggerTime, terminationTime;
                    try {
                        trigggerTime = e.getTriggeredAt();
                        terminationTime = e.getTerminatedAt();
                    } catch (NullPointerException n) {
                        //System.err.println(n.getMessage());
                        continue;
                    }
                    long duration = Duration.between(trigggerTime, terminationTime).getSeconds();

                    //format:key for event, trigger time(hour of day), duration
                    String info = Integer.toString(keyMap.get(key)) + "," + trigggerTime.getHour() + "," + duration + "\r\n";
                    // System.out.println(info);
                    writer.append(info);
*/
                }
           // } catch (IOException e) {
           //     e.printStackTrace();
           // }

                    System.out.printf("\nFound the following events:\n");
                    for (String key : keyMap.keySet()) {
                        int value = keyMap.get(key);
                        System.out.printf("%s: %d\n", key, value);
                    }
                    System.out.printf("Total events " + printCounter + "\n");
                }

                System.out.printf("Done (%s)\n", new Date());
            }
        }
    }