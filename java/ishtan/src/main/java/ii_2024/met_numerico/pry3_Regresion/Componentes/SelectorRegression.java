package ii_2024.met_numerico.pry3_Regresion.Componentes;

import java.util.ArrayList;

import javax.swing.BoxLayout;
import javax.swing.ButtonGroup;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JRadioButton;

import java.awt.event.*;

import ii_2024.met_numerico.pry3_Regresion.InputType;

public class SelectorRegression {
    private InputType type = InputType.Lineal;
    private ArrayList<ActionListener> listeners = new ArrayList<ActionListener>();

    public JPanel as_JPanel() {
        JPanel panel = new JPanel();
        panel.setLayout(new javax.swing.BoxLayout(panel, BoxLayout.X_AXIS));

        // Crear botones con nombre
        JRadioButton btn_lineal, btn_poly, btn_ln_mult;
        btn_lineal = new JRadioButton("Lineal");
        btn_poly = new JRadioButton("Polinomial");
        btn_ln_mult = new JRadioButton("Lineal Multiple");

        switch (this.type) {
            case Lineal -> btn_lineal.setSelected(true);
            case Polinomial -> btn_poly.setSelected(true);
            case LinealMultiple -> btn_ln_mult.setSelected(true);
        }

        // Agrupar los botones
        ButtonGroup bg = new ButtonGroup();
        bg.add(btn_lineal);
        bg.add(btn_poly);
        bg.add(btn_ln_mult);

        // Registrar eventos
        btn_lineal.addActionListener(_a -> notify_listeners(InputType.Lineal));
        btn_poly.addActionListener(_ -> notify_listeners(InputType.Polinomial));
        btn_ln_mult.addActionListener(_ -> notify_listeners(InputType.LinealMultiple));

        // Agregar los botones al panel
        panel.add(btn_lineal);
        panel.add(btn_poly);
        panel.add(btn_ln_mult);

        return panel;
    }

    public void addActionListener(ActionListener listener) {
        this.listeners.add(listener);
    }

    public void notify_listeners(InputType new_value) {
        this.type = new_value;
        for (ActionListener listener : this.listeners) {
            listener.actionPerformed(new ActionEvent(this, 0, "Type Update"));
        }
    }

    public InputType get_type() {
        return this.type;
    }

    public static void main(String[] args) {
        var selector = new SelectorRegression();
        JFrame frame = new JFrame();

        selector.addActionListener(e -> {
            System.out.println("Type updated to: " + selector.get_type());
        });

        frame.add(selector.as_JPanel());
        frame.pack();
        frame.setVisible(true);
    }
}
