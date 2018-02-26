import examples.CountEventTypeExample;
import extraction.ExtractEditAndTestData;

public class runExtract {
    public static String eventsDir = "Events-170301-2";

    public static void main(String[] args) {

        new ExtractEditAndTestData(eventsDir).run();
    }
}