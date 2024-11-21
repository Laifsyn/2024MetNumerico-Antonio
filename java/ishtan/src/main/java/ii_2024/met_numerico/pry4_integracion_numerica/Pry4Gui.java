package ii_2024.met_numerico.pry4_integracion_numerica;

import javax.swing.*;

import java.awt.*;
import java.text.NumberFormat;

/**
 * Clase que se usará solamente para el propósito de dibujar la interfaz
 * gráfica.
 * La lógica de la aplicación se encuentra en la clase `Pry4`, donde se
 * inyectará el comportamiento.
 */
public final class Pry4Gui {
    public static void main(String[] args) {
        final JFrame frame = Pry4.default_JFrame();
        final Pry4Gui gui = new Pry4Gui(frame);
        gui.show();
    }

    private final JFrame frame;
    private final JTextField input_function_field;
    private final JFormattedTextField lower_limit_field;
    private final JFormattedTextField upper_limit_field;
    private final JFormattedTextField segments_field;
    private final JComboBox<IntegrationMethod> method_selector;
    private final JButton calculate_button;
    private final JTable table;
    private final JTextArea result_area;

    public Pry4Gui(JFrame InputFrame) {
        frame = InputFrame;
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);
        frame.setLayout(new BorderLayout());

        // Panel for data input
        JPanel input_panel = new JPanel();
        input_panel.setLayout(new GridLayout(5, 2, 5, 5));

        // Function input
        input_panel.add(new JLabel("Function f(x):"));
        input_function_field = new JTextField();
        input_panel.add(input_function_field);

        // Lower limit input
        input_panel.add(new JLabel("Lower Limit (a):"));
        lower_limit_field = new JFormattedTextField(NumberFormat.getNumberInstance());
        lower_limit_field.setValue(0.0);
        on_focus_replace_commas(lower_limit_field);
        input_panel.add(lower_limit_field);

        // Upper limit input
        input_panel.add(new JLabel("Upper Limit (b):"));
        upper_limit_field = new JFormattedTextField(NumberFormat.getNumberInstance());
        upper_limit_field.setValue(1.0);
        on_focus_replace_commas(upper_limit_field);
        input_panel.add(upper_limit_field);

        // Number of segments input
        input_panel.add(new JLabel("Number of Segments (n):"));
        segments_field = new JFormattedTextField(NumberFormat.getIntegerInstance());
        segments_field.setValue(1l);
        on_focus_replace_commas(segments_field);
        input_panel.add(segments_field);

        // Method selector dropdown
        input_panel.add(new JLabel("Method:"));
        method_selector = new JComboBox<>(new IntegrationMethod[] {
                IntegrationMethod.Trapezoidal,
                IntegrationMethod.Simpson13,
                IntegrationMethod.Simpson38
        });
        input_panel.add(method_selector);

        frame.add(input_panel, BorderLayout.NORTH);

        // Button to trigger calculation
        calculate_button = new JButton("Calculate");
        frame.add(calculate_button, BorderLayout.CENTER);

        // Area to display results
        JPanel output_pane = new JPanel();
        output_pane.setLayout(new BoxLayout(output_pane, BoxLayout.Y_AXIS));

        table = new JTable( /* data */ new Double[][] { { 1.0, 2. }, { .2, .3 } },
                /* headers */ new String[] { "x", "f(x)" });
        table.setEnabled(false);
        JScrollPane table_scroll_pane = new JScrollPane(table);
        System.out.println("Prefered: " + table_scroll_pane.getPreferredSize().height);
        table_scroll_pane.setPreferredSize(new Dimension(frame.getPreferredSize().width, 225));
        output_pane.add(table_scroll_pane);

        result_area = new JTextArea();
        result_area.setEditable(false);
        JScrollPane scroll_pane = new JScrollPane(result_area);
        scroll_pane.setPreferredSize(new Dimension(scroll_pane.getSize().width, 35));
        output_pane.add(scroll_pane);

        frame.add(output_pane, BorderLayout.SOUTH);
        frame.pack();
    }

    /**
     * Registra un evento de que al obtener el foco, se reemplacen las comas por un
     * espacio vacío.
     * 
     * @param field
     */
    private JTextField on_focus_replace_commas(final JTextField field) {
        field.addFocusListener(new java.awt.event.FocusListener() {
            @Override
            public void focusGained(java.awt.event.FocusEvent e) {
                field.setText(field.getText().replace(",", ""));
                field.selectAll();
            }

            @Override
            public void focusLost(java.awt.event.FocusEvent e) {
                // Do nothing
            }
        });
        return field;
    }

    public enum IntegrationMethod {
        Trapezoidal,
        Simpson13,
        Simpson38;

        @Override
        public String toString() {
            switch (this) {
                case Trapezoidal:
                    return "Trapecio";
                case Simpson13:
                    return "Simpson 1/3";
                case Simpson38:
                    return "Simpson 3/8";
                default:
                    return "Unknown Integration Method";
            }
        }

        public double calcular(Double[][] valores) {
            // Se asume que los demás indices tienen la misma longitud
            assert valores[0].length == 2;
            switch (this) {
                case Trapezoidal:
                    return trapezoidal(valores);
                case Simpson13:
                    return simpson13(valores);
                case Simpson38:
                    return simpson38(valores);
                default:
                    return 0.0;
            }
        }

        private double trapezoidal(Double[][] valores) {
            double result = 0.0;
            final double h = valores[1][0] - valores[0][0];
            final int fx = 1;
            for (int i = 1; i < valores.length - 1; i++) {
                result += valores[i][fx];
            }
            result = (h / 2) * (valores[0][fx] + 2 * result + valores[valores.length - 1][fx]);
            return result;
        }

        private double simpson13(Double[][] valores) {
            double impares = 0.0;
            double pares = 0.0;
            final double h = valores[1][0] - valores[0][0];
            final int fx = 1;

            for (int i = 1; i < valores.length - 1; i++) {
                if (i % 2 == 0) {
                    pares += valores[i][fx];
                } else {
                    impares += valores[i][fx];
                }
            }
            return (h / 3) * (valores[0][fx] + 4 * impares + 2 * pares + valores[valores.length - 1][fx]);
        }

        private double simpson38(Double[][] valores) {
            double result = 0.0;
            double multiplos_3 = 0.0;
            final double h = valores[1][0] - valores[0][0];
            final int fx = 1;

            for (int i = 1; i < valores.length - 1; i++) {
                if (i % 3 == 0) {
                    multiplos_3 += valores[i][fx];
                } else {
                    result += valores[i][fx];
                }
            }
            return (3 * h / 8) * (valores[0][fx] + 2 * multiplos_3 + 3 * result + valores[valores.length - 1][fx]);
        }
    }

    /**
     * Método para mostrar la interfaz.
     */
    public void show() {
        frame.setVisible(true);
    }

    // Getters para exponer los componentes que serán usados para inyección de comportamiento.
    public JFrame getFrame() {
        return frame;
    }
    public JTextField getInput_function_field() {
        return input_function_field;
    }

    public JFormattedTextField getLower_limit_field() {
        return lower_limit_field;
    }

    public JFormattedTextField getUpper_limit_field() {
        return upper_limit_field;
    }

    public JFormattedTextField getSegments_field() {
        return segments_field;
    }

    public JComboBox<IntegrationMethod> getMethod_selector() {
        return method_selector;
    }

    public JButton getCalculate_button() {
        return calculate_button;
    }

    public JTable getTable() {
        return table;
    }

    public JTextArea getResult_area() {
        return result_area;
    }

}
