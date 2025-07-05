// JAVA-001: Avoid using System.out.println
public class FinalBlockTest {

    // JAVA-002: Class should have a JavaDoc comment
    int my_var = 0; // JAVA-003: Variable name should be in camelCase

    public static void main(String[] args) {
        System.out.println("Hello World"); // JAVA-001

        int UNUSED_CONSTANT = 42; // JAVA-004: Unused variable

        // JAVA-005: Use meaningful names
        int a = 10;

        // JAVA-006: Deeply nested code (more than 3 levels)
        if (a > 0) {
            if (a < 20) {
                if (a == 10) {
                    if (a != 15) {
                        System.out.println("Deep nesting");
                    }
                }
            }
        }

        // JAVA-007: Magic number
        int result = a * 3;

        // JAVA-008: Method should have a JavaDoc
        new FinalBlockTest().doStuff();

        // JAVA-009: Use of synchronized method
        new FinalBlockTest().synchronizedMethod();

        // JAVA-010: Empty catch block
        try {
            int x = 1 / 0;
        } catch (Exception e) {
        }

        // JAVA-011: Use equals() for string comparison
        String s = "test";
        if (s == "test") {
            System.out.println("Wrong string comparison");
        }

        // JAVA-012: Avoid mutable static fields
        MutableSingleton.counter++;

        // JAVA-013: Avoid assigning parameter directly
        FinalBlockTest fbt = new FinalBlockTest();
        fbt.assignParam("wrong");

        // JAVA-014: Prefer streams/lambdas for collection iteration
        for (String item : java.util.Arrays.asList("a", "b", "c")) {
            System.out.println(item);
        }
    }

    void doStuff() {
        // no comment = JAVA-008
    }

    public synchronized void synchronizedMethod() {
        // JAVA-009
    }

    public void assignParam(String input) {
        input = "changed"; // JAVA-013
    }

    static class MutableSingleton {
        static int counter = 0; // JAVA-012
    }
}
