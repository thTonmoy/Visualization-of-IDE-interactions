package examples;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Paths;
import java.time.Duration;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Date;
import java.util.Map;
import java.util.Set;

import cc.kave.commons.model.events.visualstudio.BuildEvent;
import com.google.common.collect.Maps;

import cc.kave.commons.model.events.IIDEEvent;
import cc.kave.commons.utils.io.IReadingArchive;
import cc.kave.commons.utils.io.ReadingArchive;

public class CountEventTypeExample {

    private String dir;

    public CountEventTypeExample(String dir) {
        this.dir = dir;
    }

    public void run() {
        Set<String> zips = IoHelper.findAllZips(dir);
        BufferedWriter writer = null;
        int keyCount = 0;
        try {
            writer = new BufferedWriter(new FileWriter("test_events.txt"));
        } catch (IOException e) {
            e.printStackTrace();
        }

        int zipTotal = zips.size();
        int zipCount = 0;
        for (String zip : zips) {
            double perc = 100 * zipCount / (double) zipTotal;
            zipCount++;
            if(zipCount == 2) break;

            System.out.printf("## %s, processing %s... (%d/%d, %.1f%% done)\n", new Date(), zip, zipCount, zipTotal,
                    perc);
            File zipFile = Paths.get(dir, zip).toFile();

            Map<String, Integer> keyMap = Maps.newHashMap();

            int printCounter = 0;
            try (IReadingArchive ra = new ReadingArchive(zipFile)) {
                while (ra.hasNext()) {
                    if (printCounter++ % 1000 == 0) {
                        System.out.printf(".\n");
                    }
                    IIDEEvent e = ra.getNext(IIDEEvent.class);
                    String key = e.getClass().getSimpleName();

                    if (!keyMap.containsKey(key)) {
                        keyMap.put(key,keyCount++);

                    } else {

                        ZonedDateTime trigggerTime = e.getTriggeredAt();
                        ZonedDateTime terminationTime;
                        try {
                            terminationTime = e.getTerminatedAt();
                        }catch (NullPointerException n){
                            //System.err.println(n.getMessage());
                            continue;
                        }
                        long duration = Duration.between(trigggerTime, terminationTime).getSeconds();
                        //if(duration == 0) continue;

                        String info = "," + trigggerTime.toEpochSecond() +"," + terminationTime.toEpochSecond() + "," + duration + "\r\n";
                        writer.append(Integer.toString(keyMap.get(key),10));
                        writer.append(info);

                    }
                }
            } catch (IOException e) {
                e.printStackTrace();
            }

            System.out.printf("\nFound the following events:\n");
            for (String key : keyMap.keySet()) {
                int count = keyMap.get(key);
                System.out.printf("%s: %d\n", key, count);
            }
            System.out.printf("\n");
        }

        System.out.printf("Done (%s)\n", new Date());
    }
}