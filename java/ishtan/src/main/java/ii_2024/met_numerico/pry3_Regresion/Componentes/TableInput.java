package ii_2024.met_numerico.pry3_Regresion.Componentes;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.HashMap;
import java.awt.*;

import javax.swing.*;
import javax.swing.table.*;

import ii_2024.met_numerico.pry3_Regresion.InputType;

public class TableInput {
    public static void main(String[] args) {
        var table = new TableInput(new SelectorRegression());

        JFrame frame = new JFrame();
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLayout(new BoxLayout(frame.getContentPane(), BoxLayout.Y_AXIS));
        frame.add(table.as_JPanel());
        frame.pack();
        frame.setVisible(true);
    }

    private JTable table = this.default_table();
    private JLabel total_x = new JLabel("x");
    private JLabel total_y = new JLabel("y");
    private JLabel total_x2 = new JLabel("x_2");
    private JLabel median_y = new JLabel("y median");
    private HashMap<Totals, Double> totals = new HashMap<>();
    private SelectorRegression selector;
    private ArrayList<ActionListener> tableModel_listeners = new ArrayList<>();
    /**
     * Usado para guardar el historial de los datos en la tabla
     */
    private ArrayList<Object[]> table_history_stack = new ArrayList<>();

    private JTable default_table() {
        String[] column_names = { "y", "x", "x_2" };
        Object[][] data = {
                { 4, 2, 0 },
                { 9, 3, 0 },
                { "", "", "" }
        };
        DefaultTableModel model = new DefaultTableModel(data, column_names) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return column < (selector.get_type() == InputType.LinealMultiple ? 3 : 2);
            }
        };
        JTable table = new JTable(model);
        table.setDefaultRenderer(Object.class, this.default_cell_renderer());
        table.setCellSelectionEnabled(true);

        return table;
    }

    private DefaultTableCellRenderer default_cell_renderer() {
        return new DefaultTableCellRenderer() {

            @Override
            /**
             * Cambia el color de las celdas dependiendo de si son valores `Double` válidos
             */
            public Component getTableCellRendererComponent(JTable table, Object value, boolean isSelected,
                    boolean hasFocus, int row, int column) {
                Component cell = super.getTableCellRendererComponent(table, value, isSelected, hasFocus, row, column);
                value = table.getValueAt(row, column);
                if (cell_validator(value)) {
                    cell.setForeground(Color.BLACK);
                    cell.setBackground(Color.WHITE);
                } else {
                    cell.setForeground(Color.WHITE);
                    cell.setBackground(new Color(169, 19, 43)); // Desaturated Carmine color
                }

                // Update format for un-editable cells
                if (!table.isCellEditable(row, column)) {
                    cell.setBackground(Color.LIGHT_GRAY);
                    cell.setForeground(Color.LIGHT_GRAY);
                }
                return cell;
            }
        };
    }

    // Valida si es un valor numérico
    private boolean cell_validator(Object val) {
        try {
            Double.parseDouble((String.valueOf(val)).trim());
            return true;
        } catch (Exception _e) {
            return false;
        }
    }

    public TableInput(SelectorRegression selector) {
        this.selector = selector;
        selector.addActionListener(_ignored -> on_selector_change());
        on_selector_change(); // Correr una vez para inicializar los totales
    }

    public InputType get_input_type() {
        return this.selector.get_type();
    }

    public JPanel as_JPanel() {
        JScrollPane scroll_pane = new JScrollPane(this.table);
        scroll_pane.setMaximumSize(new Dimension(350, 175));
        this.selector.addActionListener(_ignored -> notify_model_listeners());
        this.table.getModel().addTableModelListener((_ingored) -> {
            // Actualizar totales cuando el modelo de la tabla cambie
            tally_totals();
            // Notificar a los listeners que el modelo de la tabla ha cambiado
            this.notify_model_listeners();
        });

        // Definir botones y eventos
        final JButton push_row, pop_row, blankize_table;
        push_row = new JButton("Agregar Fila");
        pop_row = new JButton("Eliminar Fila");
        blankize_table = new JButton("Vaciar Tabla");

        // Definir la acción para agregar fila
        push_row.addActionListener((ActionEvent e) -> {
            DefaultTableModel model = (DefaultTableModel) this.table.getModel();
            Object[] data = (this.table_history_stack.size() > 0) ? this.table_history_stack.removeLast()
                    : new Object[] { 0, 0, 0 };
            model.addRow(data);
        });
        // Definir la acción para eliminar fila
        pop_row.addActionListener((ActionEvent e) -> {
            DefaultTableModel model = (DefaultTableModel) this.table.getModel();
            if (model.getRowCount() == 0)
                return; // Early Return on empty table
            Object[] popped = new Object[model.getColumnCount()];
            this.table_history_stack.add(popped);
            for (int i = 0; i < model.getColumnCount(); i++)
                popped[i] = model.getValueAt(model.getRowCount() - 1, i);
            model.removeRow(model.getRowCount() - 1);
        });
        blankize_table.addActionListener(e -> {
            DefaultTableModel model = (DefaultTableModel) this.table.getModel();
            for (int i = 0; i < model.getRowCount(); i++) {
                for (int j = 0; j < model.getColumnCount(); j++) {
                    model.setValueAt("", i, j);
                }
            }

        });

        // Definir Layouts
        JPanel pane = new JPanel();
        pane.setLayout(new BoxLayout(pane, BoxLayout.Y_AXIS));

        JPanel totales = new JPanel();
        totales.setLayout(new GridBagLayout());

        JPanel buttons = new JPanel();
        buttons.setLayout(new BoxLayout(buttons, BoxLayout.X_AXIS));

        // Añadir elementos al panel de totales
        var border = BorderFactory.createTitledBorder("Estadísticas");
        totales.setBorder(border);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.anchor = GridBagConstraints.CENTER;
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.insets = new Insets(0, 10, 0, 10);
        totales.add(this.total_y, gbc);

        gbc.gridx = 1;
        totales.add(this.total_x, gbc);

        gbc.gridx = 2;
        totales.add(this.total_x2, gbc);

        gbc.gridx = 0;
        gbc.gridwidth = 3;
        gbc.gridy = 1;
        totales.add(this.median_y, gbc);
        totales.setMaximumSize(scroll_pane.getMaximumSize());
        // Fin de la región de totales

        // Añadir elementos al panel de botones
        buttons.add(push_row);
        buttons.add(Box.createRigidArea(new Dimension(20, 0)));
        buttons.add(pop_row);
        buttons.add(Box.createRigidArea(new Dimension(20, 0)));
        buttons.add(blankize_table);

        // Añadir elementos al panel
        pane.add(this.selector.as_JPanel());
        pane.add(scroll_pane);
        pane.add(Box.createRigidArea(new Dimension(20, 10)));
        pane.add(totales);
        pane.add(Box.createRigidArea(new Dimension(20, 10)));
        pane.add(buttons);
        return pane;
    }

    /**
     * Realizar actualización de la tabla debido a cambios al selector
     */
    protected void on_selector_change() {
        boolean is_linealMultiple = this.selector.get_type() == InputType.LinealMultiple;
        this.table.repaint();
        this.total_x2.setVisible(is_linealMultiple);
        tally_totals();
    }

    protected void tally_totals() {
        DefaultTableModel model = (DefaultTableModel) this.table.getModel();
        double total_x = 0, total_y = 0, total_x2 = 0;
        boolean total_x_valid = true, total_y_valid = true, total_x2_valid = true;
        int valid_ys = 0;
        for (int i = 0; i < model.getRowCount(); i++) {
            Object x = model.getValueAt(i, 1);
            Object y = model.getValueAt(i, 0);
            total_x += cell_validator(x) ? Double.parseDouble(String.valueOf(x)) : 0;
            total_y += cell_validator(y) ? Double.parseDouble(String.valueOf(y)) : 0;
            if (cell_validator(y)) // TODO: Inline ifs conditions
                valid_ys++;
            if (!cell_validator(x))
                total_x_valid = false;
            if (!cell_validator(y))
                total_y_valid = false;
            if (this.selector.get_type() == InputType.LinealMultiple) {
                Object x2 = model.getValueAt(i, 2);
                total_x2 += cell_validator(x2) ? Double.parseDouble(String.valueOf(x2)) : 0;
                if (!cell_validator(x2))
                    total_x2_valid = false;
            }
        }

        this.totals.put(Totals.X, total_x);
        this.totals.put(Totals.Y, total_y);
        this.totals.put(Totals.X2, total_x2);
        this.totals.put(Totals.Y_MEDIAN, total_y / valid_ys);

        this.total_x.setText("X: " + total_x);
        this.total_x.setForeground((total_x_valid) ? Color.BLACK : Color.RED);
        this.total_y.setText("Y: " + total_y);
        this.total_y.setForeground((total_y_valid) ? Color.BLACK : Color.RED);
        this.total_x2.setText("X_2: " + total_x2);
        this.total_x2.setForeground((total_x2_valid) ? Color.BLACK : Color.RED);
        this.median_y.setForeground((total_y_valid) ? Color.BLACK : Color.RED);
        this.median_y.setText("Y median: " + total_y / valid_ys);
    }

    public Double get_totals(Totals type) {
        // Condicional por si se realiza la lectura antes de que se hayan calculado los
        // totales.
        if (!this.totals.containsKey(type))
            this.tally_totals();
        return this.totals.get(type);
    }

    /**
     * Retorna las columnas de la tabla sin revisar el tipo de regresión
     * seleccionado.
     * Adicionalmente, campos inválidos son reemplazados por `null`
     * 
     * @return
     */
    public Double[][] get_nullable_dataset() {
        DefaultTableModel model = (DefaultTableModel) this.table.getModel();
        Double[][] dataset = new Double[model.getRowCount()][model.getColumnCount()];
        // Se asume que el orden de las columnas es [y, x, x_2]
        for (int i = 0; i < model.getRowCount(); i++) {
            for (Variables j : new Variables[] { Variables.Y, Variables.X, Variables.X2 }) {
                Object val = model.getValueAt(i, j.getValue());
                dataset[i][j.getValue()] = cell_validator(val) ? Double.parseDouble(String.valueOf(val)) : null;
            }
        }
        return dataset;
    }

    public void addActionListener(ActionListener listener) {
        this.tableModel_listeners.add(listener);
    }

    public void notify_model_listeners() {
        for (ActionListener listener : this.tableModel_listeners) {
            listener.actionPerformed(new ActionEvent(this, 0, "Table Model Update"));
        }
    }

    public enum Totals {
        X, Y, X2, Y_MEDIAN
    }

    public enum Variables {
        Y(0), X(1), X2(2);

        private int value;

        Variables(int value) {
            this.value = value;
        }

        public int getValue() {
            return this.value;
        }
    }

}
