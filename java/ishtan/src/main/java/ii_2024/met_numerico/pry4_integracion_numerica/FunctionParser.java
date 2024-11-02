package ii_2024.met_numerico.pry4_integracion_numerica;

import java.util.*;
import java.text.DecimalFormat;
import java.util.regex.*;

public class FunctionParser {

    private static final Map<String, Integer> OPERATORS = new HashMap<>();
    private static final Map<String, Double> CONSTANTS = new HashMap<>();

    static {
        // Operator precedence
        OPERATORS.put("+", 1);
        OPERATORS.put("-", 1);
        OPERATORS.put("*", 2);
        OPERATORS.put("/", 2);
        OPERATORS.put("^", 3);

        // Constants
        CONSTANTS.put("pi", Math.PI);
        CONSTANTS.put("e", Math.E);
    }

    public static Optional<Double> evaluate(String expression, double x) {

        // Reemplazar x y constantes
        DecimalFormat df = new java.text.DecimalFormat("#." + "#".repeat(15));
        expression = expression.replace("x", df.format(x)); // Usar formato porque la representación de double en String
        try {
            return Optional.of(__evaluate(expression));

        } catch (Exception e) {
            return Optional.empty();
        }
    }

    private static double __evaluate(String expression) {

        List<String> postfix = infixToPostfix(expression);
        if (postfix == null) {
            throw new IllegalArgumentException("Invalid expression");
        }
        return evaluatePostfix(postfix);
    }

    private static List<String> infixToPostfix(String expression) {
        List<String> output = new ArrayList<>();
        Stack<String> operators = new Stack<>();

        Pattern pattern = Pattern.compile("\\d+(\\.\\d+)?|pi|e|[+\\-*/^()]|exp\\(.*?\\)");
        Matcher matcher = pattern.matcher(expression.replaceAll("\\s+", ""));

        boolean expectUnary = true;

        while (matcher.find()) {
            String token = matcher.group();

            if (isNumber(token) || CONSTANTS.containsKey(token)) {
                output.add(token);
                expectUnary = false;
            } else if (token.equals("-") && expectUnary) {
                // Treat unary minus as a special case of multiplication by -1
                output.add("-1");
                operators.push("*");
            } else if (OPERATORS.containsKey(token)) {
                while (!operators.isEmpty() && OPERATORS.containsKey(operators.peek()) &&
                        ((OPERATORS.get(token) <= OPERATORS.get(operators.peek()) && !token.equals("^")) ||
                                (OPERATORS.get(token) < OPERATORS.get(operators.peek()) && token.equals("^")))) {
                    output.add(operators.pop());
                }
                operators.push(token);
                expectUnary = true;
            } else if (token.equals("(")) {
                operators.push(token);
                expectUnary = true;
            } else if (token.equals(")")) {
                while (!operators.isEmpty() && !operators.peek().equals("(")) {
                    output.add(operators.pop());
                }
                if (!operators.isEmpty())
                    operators.pop();
                expectUnary = false;
            } else if (token.startsWith("exp(")) {
                // For `exp` function
                double arg = __evaluate(token.substring(4, token.length() - 1));
                output.add(String.valueOf(Math.exp(arg)));
                expectUnary = false;
            }
        }

        while (!operators.isEmpty()) {
            output.add(operators.pop());
        }

        return output;
    }

    private static double evaluatePostfix(List<String> postfix) {
        Stack<Double> stack = new Stack<>();

        for (String token : postfix) {
            if (isNumber(token)) {
                stack.push(Double.parseDouble(token));
            } else if (CONSTANTS.containsKey(token)) {
                stack.push(CONSTANTS.get(token));
            } else if (OPERATORS.containsKey(token)) {
                double b = stack.pop();
                double a = stack.pop();
                switch (token) {
                    case "+":
                        stack.push(a + b);
                        break;
                    case "-":
                        stack.push(a - b);
                        break;
                    case "*":
                        stack.push(a * b);
                        break;
                    case "/":
                        stack.push(a / b);
                        break;
                    case "^":
                        stack.push(Math.pow(a, b));
                        break;
                }
            }
        }

        return stack.pop();
    }

    private static boolean isNumber(String token) {
        try {
            Double.parseDouble(token);
            return true;
        } catch (NumberFormatException e) {
            return false;
        }
    }

    public static void main(String[] args) {
        String[] expressions = {
                "(2 + 3) * (4 - 2) ^ (1 + 1)",
                "pi * (2 ^ 3) - e ^ (1 - 2)",
                "3 + 4 * -2 / (1 + e ^ (-2))",
                "2 ^ 3 ^ 2 - 4 / (2 + e)",
                // Same as below
                // "2 ^ (3 ^ 2) - 4 / (2 + e)",
                "(1 + e ^ (-3.21)) * pi / 2 - (2 ^ 3) + 4 * (e - 1)"
        };

        for (String expression : expressions) {
            System.out.println("Expression: " + expression);
            try {
                double result = __evaluate(expression);
                System.out.println("Result: " + result);
            } catch (Exception e) {
                System.out.println("Error evaluating expression: " + e.getMessage());
            }
            System.out.println();
        }
    }
}