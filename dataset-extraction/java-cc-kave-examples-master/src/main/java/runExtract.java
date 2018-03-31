import extraction.ExtractEventsDataAsCSV;

public class runExtract {
    public static String eventsDir = "Events-170301-2";

    public static void main(String[] args) {

        new ExtractEventsDataAsCSV(eventsDir, true, true, false, true).run();
    }
}