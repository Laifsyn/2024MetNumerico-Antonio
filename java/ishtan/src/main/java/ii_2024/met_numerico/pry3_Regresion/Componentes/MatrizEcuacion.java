package ii_2024.met_numerico.pry3_Regresion.Componentes;

import java.awt.Dimension;
import java.awt.GridBagConstraints;
import java.awt.GridBagLayout;
import java.awt.Insets;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;
import java.text.NumberFormat;
import java.util.concurrent.Callable;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;

import ii_2024.met_numerico.pry3_Regresion.Ecuacion;
import ii_2024.met_numerico.pry3_Regresion.InputType;
import ii_2024.met_numerico.pry3_Regresion.SistemaEcuacion;

public class MatrizEcuacion {
    public static void main(String[] args) {
        System.out.println("Hellow from MatrizEcuacion!");
        MatrizEcuacion mt = new MatrizEcuacion();
        TableInput table = new TableInput(new SelectorRegression());
        final JFrame frame = new JFrame();
        table.addActionListener(e -> {
            mt.leer_tabla(table);
            MatrizEcuacion.smart_pack(frame);
        });

        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BoxLayout(frame.getContentPane(), BoxLayout.Y_AXIS));
        frame.add(table.as_JPanel());
        frame.add(mt.as_JPanel());
        frame.add(Box.createRigidArea(new Dimension(0, 10)));
        frame.pack();
        frame.setVisible(true);

    }

    static void smart_pack(JFrame frame) {
        final int offset = 60;
        Dimension current_size = frame.getSize();
        Dimension packed_size = frame.getPreferredSize();
        int width = Math.max(current_size.width - offset, packed_size.width - offset);
        int height = Math.max(current_size.height, packed_size.height);
        frame.setSize(width + offset, height);

    }

    private final JPanel matriz_panel = new JPanel();

    MatrizEcuacion() {

    }

    public JPanel as_JPanel() {
        return this.matriz_panel;
    }

    public void leer_tabla(TableInput tabla) {
        InputType tipo = tabla.get_input_type();
        final SistemaEcuacion eq;
        final JLabel formula; // Resultado de la ecuación.
        final JPanel formula_and_input = new JPanel();
        final JLabel prediction_label = new JLabel("y(x) = NaN");
        final int IB_COLUMNS = 10;
        formula_and_input.setLayout(new BoxLayout(formula_and_input, BoxLayout.Y_AXIS));
        switch (tipo) {
            case Lineal -> {
                eq = this.leer_tabla_lineal(tabla);
                Double[] coeficientes = SistemaEcuacion.DESPEJAR(eq);
                formula = new JLabel(
                        String.format("<html>y(x) = %.5f + %.5fx</html>", coeficientes[0], coeficientes[1]));
                JFormattedTextField IB_X = new JFormattedTextField(NumberFormat.getNumberInstance());
                IB_X.setColumns(IB_COLUMNS);
                IB_X.addKeyListener(new KeyListener() {

                    @Override
                    public void keyTyped(KeyEvent e) {
                    }

                    @Override
                    public void keyPressed(KeyEvent e) {
                    }

                    @Override
                    public void keyReleased(KeyEvent e) {
                        final JFormattedTextField self = (JFormattedTextField) e.getSource();
                        String text;
                        try {
                            text = String.format("y(%s) = %.5f", self.getText(),
                                    coeficientes[0] + coeficientes[1] * Double.parseDouble(self.getText()));
                        } catch (Exception e1) {
                            text = String.format("y(%s) = NaN", self.getText());
                        }
                        prediction_label.setText(text);
                    }

                });
                final JPanel panel = new JPanel();
                panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
                panel.add(formula);
                panel.add(prediction_label);
                panel.add(IB_X);
                formula_and_input.add(panel);
            }
            case Polinomial -> {
                eq = this.leer_tabla_polinomial(tabla);
                Double[] coeficientes = SistemaEcuacion.DESPEJAR(eq);
                formula = new JLabel(String.format("<html>y(x) = %.5f + %.5fx + %.5fx<sup>2</sup></html>",
                        coeficientes[0], coeficientes[1], coeficientes[2]));
                JFormattedTextField IB_X = new JFormattedTextField(NumberFormat.getNumberInstance());
                IB_X.setColumns(IB_COLUMNS);
                IB_X.addKeyListener(new KeyListener() {

                    @Override
                    public void keyTyped(KeyEvent e) {
                    }

                    @Override
                    public void keyPressed(KeyEvent e) {
                    }

                    @Override
                    public void keyReleased(KeyEvent e) {
                        final JFormattedTextField self = (JFormattedTextField) e.getSource();
                        String text;
                        try {
                            double x = Double.parseDouble(self.getText());
                            text = String.format("y(%s) = %.5f", self.getText(),
                                    coeficientes[0] + coeficientes[1] * x + coeficientes[2] * Math.pow(x, 2));
                        } catch (Exception e1) {
                            text = String.format("y(%s) = NaN", self.getText());
                        }
                        prediction_label.setText(text);
                    }

                });
                final JPanel panel = new JPanel();
                panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
                panel.add(formula);
                panel.add(prediction_label);
                panel.add(IB_X);
                formula_and_input.add(panel);

            }
            case LinealMultiple -> {
                eq = this.leer_tabla_lineal_multiple(tabla);
                Double[] coeficientes = SistemaEcuacion.DESPEJAR(eq);
                formula = new JLabel(String.format(
                        "<html>y(x<sub>1</sub>,x<sub>2</sub>) = %.5f + %.5fx<sub>1</sub> + %.5fx<sub>2</sub></html>",
                        coeficientes[0], coeficientes[1], coeficientes[2]));
                final JFormattedTextField IB_X1 = new JFormattedTextField(NumberFormat.getNumberInstance());
                IB_X1.setColumns(IB_COLUMNS);
                final JFormattedTextField IB_X2 = new JFormattedTextField(NumberFormat.getNumberInstance());
                IB_X2.setColumns(IB_COLUMNS);
                final Callable<Double> predict = () -> coeficientes[0]
                        + coeficientes[1] * Double.parseDouble(IB_X1.getText())
                        + coeficientes[2] * Double.parseDouble(IB_X2.getText());
                IB_X1.addKeyListener(new KeyListener() {

                    @Override
                    public void keyTyped(KeyEvent e) {
                    }

                    @Override
                    public void keyPressed(KeyEvent e) {
                    }

                    @Override
                    public void keyReleased(KeyEvent e) {
                        final JFormattedTextField self = (JFormattedTextField) e.getSource();
                        final String left = self.getText();
                        final String right = IB_X2.getText();
                        String text;
                        try {
                            text = String.format("y(%s,%s) = %.5f", left, right, predict.call());
                        } catch (Exception e1) {
                            text = String.format("y(%s,%s) = NaN", left, right);
                        }
                        prediction_label.setText(text);
                    }

                });

                IB_X2.addKeyListener(new KeyListener() {

                    @Override
                    public void keyTyped(KeyEvent e) {
                    }

                    @Override
                    public void keyPressed(KeyEvent e) {
                    }

                    @Override
                    public void keyReleased(KeyEvent e) {
                        final JFormattedTextField self = (JFormattedTextField) e.getSource();
                        final String left = IB_X1.getText();
                        final String right = self.getText();
                        String text;
                        try {
                            text = String.format("y(%s,%s) = %.5f", left, right, predict.call());
                        } catch (Exception e1) {
                            text = String.format("y(%s,%s) = NaN", left, right);
                        }
                        prediction_label.setText(text);
                    }

                });
                final JPanel panel = new JPanel();
                panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));
                panel.add(formula);
                panel.add(prediction_label);
                panel.add(IB_X1);
                panel.add(IB_X2);
                formula_and_input.add(panel);

            }
            default ->
                throw new IllegalArgumentException("Tipo de entrada no soportado.");
        }

        this.update_JPanel(eq, formula_and_input);

    }

    /**
     * Retorna el JPanel a actualizar para ser consecuentemente editado en el sitio
     * de llamada de ser necesario
     * 
     * @param eq_system
     * @return
     */
    private JPanel update_JPanel(final SistemaEcuacion eq_system, final JPanel formula_and_input) {
        final JPanel panel = this.matriz_panel;
        panel.removeAll();
        panel.invalidate();
        panel.setLayout(new GridBagLayout());
        final GridBagConstraints gbc = new GridBagConstraints();
        gbc.fill = GridBagConstraints.HORIZONTAL;
        gbc.gridy = -1; // Para que empiece en 0.
        gbc.anchor = GridBagConstraints.CENTER;
        gbc.insets = new Insets(0, 2, 0, 2);
        for (final Ecuacion eq : eq_system.clone().ecuaciones()) {
            gbc.gridx = 0;
            gbc.gridy++;
            for (int i = 0; i < eq.variables(); i++) {
                JButton button = new JButton(eq.coeficientes()[i].toString());
                panel.add(button, gbc);
                gbc.gridx++;

            }
            gbc.fill = GridBagConstraints.NONE;
            panel.add(new JLabel("="), gbc);
            gbc.fill = GridBagConstraints.HORIZONTAL;
            gbc.gridx++;
            JButton button = new JButton(String.format("%s", eq.resultado()));
            panel.add(button, gbc);
        }
        gbc.gridx = 0;
        gbc.gridy++;
        gbc.gridwidth = eq_system.filas();
        panel.add(formula_and_input, gbc);
        panel.revalidate();
        panel.repaint();
        return panel;
    }

    // Se asume que la tabla es lineal
    public SistemaEcuacion leer_tabla_lineal(TableInput tabla) {
        // Usar el método de mínimos cuadrados.
        Double[][] data = tabla.get_nullable_dataset();
        double x = 0, y = 0, square_x = 0, xy = 0;
        int n = data.length; // Recordar restarle 1 por cada fila con errores.
        int Y = TableInput.Variables.Y.getValue();
        int X = TableInput.Variables.X.getValue();
        for (Double[] fila : data) {
            // Revisar por valor nulo.
            if (fila[X] == null || fila[Y] == null) {
                n--;
                continue;
            }
            x += fila[X];
            y += fila[Y];
            square_x += Math.pow(fila[X], 2);
            xy += fila[X] * fila[Y];
        }
        return new SistemaEcuacion(new Ecuacion[] {
                Ecuacion.of(new Double[] { Double.valueOf(n), x }, y),
                Ecuacion.of(new Double[] { x, square_x }, xy)
        });
    }

    // Se asume que la tabla es polinomial
    public SistemaEcuacion leer_tabla_polinomial(TableInput tabla) {
        // Regresión polinomial de segundo grado.
        Double[][] data = tabla.get_nullable_dataset();
        double x = 0, xx = 0, xxx = 0, xxxx = 0, y = 0, xy = 0, xxy = 0;
        int n = data.length; // Recordar restarle 1 por cada fila con errores.
        int Y = TableInput.Variables.Y.getValue();
        int X = TableInput.Variables.X.getValue();
        for (Double[] fila : data) {
            // Revisar por valor nulo.
            if (fila[X] == null || fila[Y] == null) {
                n--;
                continue;
            }
            x += fila[X];
            y += fila[Y];
            xx += Math.pow(fila[X], 2);
            xxx += Math.pow(fila[X], 3);
            xxxx += Math.pow(fila[X], 4);
            xy += fila[X] * fila[Y];
            xxy += Math.pow(fila[X], 2) * fila[Y];
        }

        return new SistemaEcuacion(new Ecuacion[] {
                Ecuacion.of(new Double[] { Double.valueOf(n), x, xx }, y),
                Ecuacion.of(new Double[] { x, xx, xxx }, xy),
                Ecuacion.of(new Double[] { xx, xxx, xxxx }, xxy)
        });
    }

    // Se asume que la tabla es lineal multiple
    private SistemaEcuacion leer_tabla_lineal_multiple(TableInput tabla) {
        // Regresión lineal múltiple.
        Double[][] data = tabla.get_nullable_dataset();
        double x1 = 0, x2 = 0, y = 0, xx1 = 0, x1x2 = 0, xx2 = 0, x1y = 0, x2y = 0;
        int n = data.length; // Recordar restarle 1 por cada fila con errores.
        int Y = TableInput.Variables.Y.getValue();
        int X = TableInput.Variables.X.getValue();
        int X2 = TableInput.Variables.X2.getValue();
        for (Double[] fila : data) {
            // Revisar por valor nulo.
            if (fila[X] == null || fila[X2] == null || fila[Y] == null) {
                n--;
                continue;
            }
            x1 += fila[X];
            x2 += fila[X2];
            y += fila[Y];
            xx1 += Math.pow(fila[X], 2);
            x1x2 += fila[X] * fila[X2];
            xx2 += Math.pow(fila[X2], 2);
            x1y += fila[X] * fila[Y];
            x2y += fila[X2] * fila[Y];
        }
        return new SistemaEcuacion(new Ecuacion[] {
                Ecuacion.of(new Double[] { Double.valueOf(n), x1, x2 }, y),
                Ecuacion.of(new Double[] { x1, xx1, x1x2 }, x1y),
                Ecuacion.of(new Double[] { x2, x1x2, xx2 }, x2y)
        });
    }

    private void cargar_tabla_lineal(double[] data) {
        // Descomponen los datos
        int n = (int) data[0];
        double x = data[1], y = data[2], square_x = data[3], xy = data[4];
        DefaultTableModel model = new DefaultTableModel();
        model.addColumn("x");
        model.addColumn("y");

    }

    public enum MatrizType {
        Lineal,
        Polinomial,
        LinealMultiple;

        public static MatrizType from(InputType tipo) {
            switch (tipo) {
                case Lineal:
                    return MatrizType.Lineal;
                case Polinomial:
                    return MatrizType.Polinomial;
                case LinealMultiple:
                    return MatrizType.LinealMultiple;
                default:
                    throw new IllegalArgumentException("Tipo de entrada no soportado.");
            }
        }
    }
}
