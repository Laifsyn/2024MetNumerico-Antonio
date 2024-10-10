package ii_2024.met_numerico.sistema_ecuacion;

import java.util.Arrays;

public class pry2 {

    public static void main(String[] args) {
        Ecuacion[] eqs = {
                Ecuacion.of(new Double[] { 3.0, 2.0, 1.0, 4.0 }, 110),
                Ecuacion.of(new Double[] { 2.0, 1.0, 3.0, 2.0 }, 90),
                Ecuacion.of(new Double[] { 1.0, 3.0, 2.0, 1.0 }, 85),
                Ecuacion.of(new Double[] { 1.0, 2.0, 1.0, 2.0 }, 95)
        };
        SistemaEcuacion sistema_eq = new SistemaEcuacion(eqs);
        sistema_eq.a_triangular_superior();
        System.out.println(sistema_eq);
        sistema_eq.a_diagonal_unitario();
        System.out.println(sistema_eq);
    }
}

/**
 * Un sistema de ecuaciones lineales, que garantiza que todas las ecuaciones
 * sean del mismo grado
 */
final class SistemaEcuacion {
    private final Ecuacion[] ecuaciones;
    private final int variables;

    public SistemaEcuacion(Ecuacion[] ecuaciones) {
        int variables = ecuaciones[0].variables();
        for (Ecuacion ecuacion : ecuaciones) {
            if (ecuacion.variables() != variables) {
                throw new IllegalArgumentException("Las ecuaciones no tienen la misma cantidad de coeficientes");
            }
        }
        this.variables = variables;
        this.ecuaciones = ecuaciones;
    }

    public void producto_escalar(double escalar) {
        for (int i = 1; i < this.ecuaciones.length; i++) {
            this.ecuaciones[i] = this.ecuaciones[i].producto_escalar(escalar);
        }
    }

    /**
     * Edita el sistema de ecuaciones a una matriz triangular superior
     */
    public void a_triangular_superior() {
        // Dimensión de la matriz
        int dim = this.variables;
        // (2) Recorrer por columna
        for (int col = 0; col < dim - 1; col++) {
            int base_row = col; // Fila base
            // (1) Recorrer por fila
            for (int row = 1 + col; row < dim; row++) {
                Ecuacion fila_a = this.ecuaciones[base_row], fila_b = this.ecuaciones[row];
                double escalar_a = fila_a.coeficientes()[col];
                double escalar_b = fila_b.coeficientes()[col];
                if (escalar_b == 0) {
                    continue;
                }
                Ecuacion f_a = fila_a.producto_escalar(escalar_b / escalar_a);
                Ecuacion f_b = fila_b.producto_escalar(1);

                // Restar las filas
                this.ecuaciones[row] = f_b.resta(f_a);
                // System.out.println(
                //         String.format("ROW: %d, [%s][%s]:[%s][%s]", row + 1, base_row + 1, col + 1, row + 1, col + 1));
            }
        }
        // System.out.println("END");
        return;
    }

    /**
     * Edita el sistema de ecuaciones para que su diagonal sea unitaria
     */
    public void a_diagonal_unitario() {
        for (int i = 0; i < this.ecuaciones.length; i++) {
            double escalar = this.ecuaciones[i].coeficientes()[i];
            this.ecuaciones[i] = this.ecuaciones[i].producto_escalar(1 / escalar);
        }
    }

    public SistemaEcuacion clone() {
        // Clonar el sistema de ecuaciones
        Ecuacion[] ecuaciones = new Ecuacion[this.ecuaciones.length];
        for (int i = 0; i < this.ecuaciones.length; i++) {
            var resultado = this.ecuaciones[i].resultado();
            var coeficientes = Arrays.copyOf(this.ecuaciones[i].coeficientes(), this.ecuaciones[i].variables());
            ecuaciones[i] = Ecuacion.of(coeficientes, resultado);
        }
        return new SistemaEcuacion(ecuaciones);

    }

    public double determinante() {
        // Clonar el sistema de ecuaciones
        SistemaEcuacion sistema = this.clone();
        sistema.a_triangular_superior();
        double det = 1;
        for (int i = 0; i < sistema.ecuaciones.length; i++) {
            det *= sistema.ecuaciones[i].coeficientes()[i];
        }

        return det;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Ecuacion ecuacion : this.ecuaciones) {
            sb.append(ecuacion.toString()).append("\n");
        }
        return sb.toString();
    }
}