import java.io.Serializable; // JAVA-004
import java.util.*; // JAVA-006, JAVA-007, JAVA-009

// JAVA-001: Avoid System.out.println
public class AllViolationsTrigger implements Serializable { // JAVA-004

    // JAVA-008: Avoid constructors with logic
    public AllViolationsTrigger() {
        System.out.println("Constructor logic"); // JAVA-001
    }

    public void test() {
        // JAVA-001: Avoid System.out.println
        System.out.println("Hello");

        // JAVA-002: Avoid == null
        String s = null;
        if (s == null) {
            System.out.println("Null check"); // JAVA-001
        }

        // JAVA-003: Avoid != null
        if (s != null) {
            System.out.println("Not null"); // JAVA-001
        }

        // JAVA-005: Avoid catching generic Exception
        try {
            int x = 5 / 0;
        } catch (Exception e) {
            System.out.println("Exception caught"); // JAVA-001
        }

        // JAVA-006: Explicit generic allocation
        List<String> list = new ArrayList<String>();

        // JAVA-007: Avoid Vector
        Vector<Integer> v = new Vector<>();

        // JAVA-009: Avoid HashMap
        HashMap<String, String> map = new HashMap<>();

        // JAVA-010: Avoid @Nullable annotations
        @SuppressWarnings("null") String nullableString = null;

        // JAVA-011: Interface naming convention
        class MyServiceImpl implements EmailService {} // Assume EmailService interface exists

        // JAVA-012: Use .equals() instead of ==
        if (s == "check") {
            System.out.println("String compare"); // JAVA-001
        }

        // JAVA-013: Loop logic
        for (int i = 0; i < 5; i++) {
            System.out.println(i); // JAVA-001
        }

        // JAVA-014: Mutable reference assignment
        this.testField = list;
    }

    private List<String> testField;
}
