package ii_2024.met_numerico.pry3_Regresion;

import java.awt.event.ActionListener;
import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;

import javax.swing.BoxLayout;
import javax.swing.JFrame;

import ii_2024.met_numerico.pry3_Regresion.Componentes.MatrizEcuacion;
import ii_2024.met_numerico.pry3_Regresion.Componentes.SelectorRegression;
import ii_2024.met_numerico.pry3_Regresion.Componentes.TableInput;

// Se siente complicado implementar y mantener lógica de reacción a eventos y mantener buen seguimiento del estado interno de la interfaz en Java.
// Mantener una consistencia entre dependencia de datos y la información mostrada se siente complicado en java.
public class pry3 {
    public static void main(String[] args) {
        final TableInput entrada_datos = new TableInput(new SelectorRegression());
        final MatrizEcuacion resultados = new MatrizEcuacion();
        final JFrame frame = getFrame();
        ActionListener action = e -> {
            resultados.leer_tabla(entrada_datos);
            MatrizEcuacion.smart_pack(frame);
        };
        entrada_datos.addActionListener(action);
        frame.add(resultados.as_JPanel());
        frame.add(entrada_datos.as_JPanel());
        action.actionPerformed(null);
        
        frame.pack();
    }

    public static JFrame getFrame() {
        final JFrame frame = new JFrame("Regresión de Datos");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.addKeyListener(new KeyListener() {

            @Override
            public void keyTyped(KeyEvent e) {
            }

            @Override
            public void keyPressed(KeyEvent e) {
                if (e.getKeyCode() == KeyEvent.VK_ESCAPE) {
                    System.out.println("Cerrando aplicación");
                    frame.dispose();
                    System.exit(0);
                }
            }

            @Override
            public void keyReleased(KeyEvent e) {
            }

        });
        frame.setLayout(new BoxLayout(frame.getContentPane(), BoxLayout.X_AXIS));
        frame.setVisible(true);
        return frame;
    }
}
