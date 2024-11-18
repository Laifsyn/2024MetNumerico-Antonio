package ii_2024.met_numerico.pry4_integracion_numerica;

import java.text.ParseException;

import javax.swing.JButton;
import javax.swing.JComboBox;
import javax.swing.JFormattedTextField;
import javax.swing.JFrame;
import javax.swing.JTable;
import javax.swing.JTextArea;
import javax.swing.JTextField;

public final class Pry4 {

    public static void main(String[] args) {
        Pry4Gui gui = new Pry4Gui(Pry4.default_JFrame());
        Pry4.inject_behaviour(gui);
        gui.show();

    }

    /**
     * Crea un JFrame con un comportamiento por defecto.
     * Comportamiento incluye cerrar la aplicación al presionar la tecla ESC.
     * 
     * @return
     */
    public static JFrame default_JFrame() {
        final JFrame frame = new JFrame("Integración Numérica");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new javax.swing.BoxLayout(frame.getContentPane(), javax.swing.BoxLayout.X_AXIS));
        frame.addKeyListener(new java.awt.event.KeyListener() {
            @Override
            public void keyTyped(java.awt.event.KeyEvent e) {
            }

            @Override
            public void keyPressed(java.awt.event.KeyEvent e) {
                if (e.getKeyCode() == java.awt.event.KeyEvent.VK_ESCAPE) {
                    System.out.println("Cerrando aplicación");
                    frame.dispose();
                    System.exit(0);
                }
            }

            @Override
            public void keyReleased(java.awt.event.KeyEvent e) {
            }
        });
        return frame;
    }

    public static void inject_behaviour(Pry4Gui gui) {
        // Instantiate objects from Pry4Gui
        final JButton calculate_button = gui.getCalculate_button();
        final JTextField input_function_field = gui.getInput_function_field();
        final JFormattedTextField lower_limit_field = gui.getLower_limit_field();
        final JFormattedTextField upper_limit_field = gui.getUpper_limit_field();
        final JFormattedTextField segments_field = gui.getSegments_field();
        final JComboBox<Pry4Gui.IntegrationMethod> method_selector = gui.getMethod_selector();
        final JTable table = gui.getTable();
        final JTextArea result_area = gui.getResult_area();

        // Agregar evento al botón de calcular
        calculate_button.addActionListener(e -> {
            System.out.println("Button clicked!");
            // Leer valores de los componentes
            final String function = input_function_field.getText();
            final double lower_limit = ((Number) lower_limit_field.getValue()).doubleValue();
            final double upper_limit = ((Number) upper_limit_field.getValue()).doubleValue();
            final int segments = ((Number) segments_field.getValue()).intValue();
            final Pry4Gui.IntegrationMethod method = method_selector.getItemAt(method_selector.getSelectedIndex());

            // Chequear que las entrada de datos no estén vacías
            StringBuilder error_msg = new StringBuilder();
            if (FunctionParser.evaluate(function, lower_limit).isEmpty()) {
                if (function.isEmpty())
                    error_msg.append("Error: La función no puede estar vacía.\n");
                else
                    error_msg.append("Error: La función `" + function + "` no es válida.\n");
            }
            if (lower_limit >= upper_limit) {
                error_msg.append("Error: El límite inferior debe ser menor al límite superior.\n");
            }
            if (segments <= 0) {
                error_msg.append("Error: El número de segmentos debe ser mayor a 0.\n");
            }
            // Rechazar valor de segmentos inválidos
            switch (method) {
                case Trapezoidal -> {
                    // No hay restricciones
                }
                case Simpson13 -> {
                    if (segments % 2 != 0 || segments < 4) {
                        error_msg.append("Error: Segmento debe ser múltiplo de 2 y mayor o igual a 4.\n");
                    }
                }
                case Simpson38 -> {
                    if (segments % 3 != 0) {
                        error_msg.append("Error: Segmento debe ser múltiplo de 3.\n");
                    }
                }
                default -> {
                    throw new RuntimeException("Método no soportado: " + method);
                }
            }
            if (error_msg.length() > 0) {
                // Limpiar último salto de línea
                error_msg.deleteCharAt(error_msg.length() - 1);
                result_area.setText("Hubo errores en los datos ingresados:\n" + error_msg.toString());
                gui.getFrame().pack();
                return;
            }

            // Obtener la tabla de valores
            final Double[][] function_values = segment_function(function, segments, lower_limit, upper_limit);
            // Calcular el integral
            final double result = method.calcular(function_values);

            // Actualizar la tabla de datos.
            final String[] column_names = { "n", "x", "f(x)" };
            final javax.swing.table.DefaultTableModel model = new javax.swing.table.DefaultTableModel(
                    new Object[function_values.length][3],
                    column_names);
            for (int row = 0; row < function_values.length; row++) {
                var formatter = java.text.NumberFormat.getNumberInstance();
                for (int col = 0; col < 2; col++) {
                    final Double val = function_values[row][col];
                    final Number number;
                    try {
                        formatter.setMaximumFractionDigits(16);
                        number = formatter.parse(val.toString());
                    } catch (ParseException e1) {
                        // Error Inesperado.
                        throw new RuntimeException(e1);
                    }

                    int int_digits = String.valueOf(number.intValue()).length();
                    // Limitar 15 decimales porque es el límite de precisión de Double
                    formatter.setMaximumFractionDigits(15 - int_digits);
                    model.setValueAt(formatter.format(val), row, col + 1);
                }
                model.setValueAt(row, row, 0);
            }
            table.setModel(model);

            // Actualizar el resultado final.
            final var formatter = java.text.NumberFormat.getNumberInstance();
            final StringBuilder result_msg = new StringBuilder();
            formatter.setMaximumFractionDigits(15);
            result_msg.append("h= " + formatter.format((upper_limit - lower_limit) / segments) + "\n");
            result_msg.append("Resultado: ");
            // Limitar la cantidad de dígitos a 15 porque es el límite de precisión de
            // Double para cualquier variante
            final int truncated = (int) result;
            final int digits = (int) Math.log10(Math.abs(truncated)) + 1;
            formatter.setMaximumFractionDigits(15 - digits);
            result_msg.append(formatter.format(result)); // Agregar área estimada al mensaje

            result_area.setText(result_msg.toString());
        });
    }

    public static Double[][] segment_function(String func_expression, int segments, double lower_limit,
            double upper_limit) {
        final Double[][] result = new Double[segments + 1][2];
        final double step = (upper_limit - lower_limit) / segments;
        for (int i = 0; i <= segments; i++) {
            final double x = lower_limit + i * step;
            result[i][0] = x;
            // Asumpciones hechas: La expresión de la función es válida.
            result[i][1] = FunctionParser.evaluate(func_expression, x).get();
        }
        return result;
    }

}
