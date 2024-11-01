package ii_2024.met_numerico.pry3_Regresion;

import java.util.Arrays;

class pry2 {

    public static double[] despeje_por_gauss_jordan(SistemaEcuacion eq) {

        // Escribir nombre de las variables
        String[] variables = new String[eq.filas()];
        for (int i = 0; i < eq.filas(); i++) {
            variables[i] = "x_" + (i + 1);
        }
        System.out.println("Despeje por Gauss Jordan de la siguiente matriz:\n" + eq);

        // Operar la matriz
        eq.a_triangular_inferior();
        eq.a_triangular_superior();
        eq.a_diagonal_unitario();
        double[] respuestas = new double[eq.filas()];
        for (int i = 0; i < eq.filas(); i++) {
            double respuesta = eq.resultado(i);
            respuestas[i] = respuesta;
            if (respuesta < 0) {
                System.out.println(variables[i] + " = " + respuesta);
            } else {
                System.out.println(variables[i] + " =  " + respuesta);
            }
        }
        return respuestas;
    }

    public static double[] por_matriz_inversa(SistemaEcuacion eq) {

        System.out.println("Despeje por inversa de la siguiente matriz:\n" + eq);
        Ecuacion[] inversa = eq.matriz_inversa();
        System.out.println("Inversa de la matriz a evaluar:");
        for (Ecuacion ecuacion : inversa) {
            System.out.println(ecuacion);
        }
        System.out.println("");
        // Se asume que siempre se tendrá n-filas para n-incógnitas
        double[] respuestas = new double[eq.filas()];
        for (int fila = 0; fila < eq.filas(); fila++) {
            Ecuacion fila_n = inversa[fila];
            for (int i = 0; i < eq.filas(); i++) {
                respuestas[fila] += fila_n.coeficientes()[i] * eq.resultado(i);
            }
        }

        // Escribir nombre de las variables
        String[] variables = new String[eq.filas()];
        for (int i = 0; i < eq.filas(); i++) {
            variables[i] = "x_" + (i + 1);
        }

        for (int i = 0; i < respuestas.length; i++) {
            double respuesta = respuestas[i];
            if (respuesta < 0) {
                System.out.println(variables[i] + " = " + respuesta);
            } else {
                System.out.println(variables[i] + " =  " + respuesta);
            }
        }
        return respuestas;
    }

    public static void main(String[] args) {
        Ecuacion[] eqs = {
                Ecuacion.of(new Double[] { 3.0, 2.0, 1.0, 4.0 }, 110),
                Ecuacion.of(new Double[] { 2.0, 1.0, 3.0, 2.0 }, 90),
                Ecuacion.of(new Double[] { 1.0, 3.0, 2.0, 1.0 }, 85),
                Ecuacion.of(new Double[] { 1.0, 2.0, 1.0, 2.0 }, 95)
        };
        SistemaEcuacion sistema_eq = new SistemaEcuacion(eqs);
        double[] por_gauss_jordan = pry2.despeje_por_gauss_jordan(sistema_eq.clone());
        System.out.println("\n");
        double[] por_inversa = pry2.por_matriz_inversa(sistema_eq.clone());

        System.out.println("Comparación de ambos métodos (Gauss Jordan seguido de Inversa):");
        for (int i = 0; i < por_gauss_jordan.length; i++) {
            String var = "x_" + (i + 1);
            System.out
                    .println(var + " = " + por_gauss_jordan[i] + "\n" + " ".repeat(var.length() + 3) + por_inversa[i]);
        }

    }
}

/**
 * Un sistema de ecuaciones lineales, que garantiza que todas las ecuaciones
 * sean del mismo "grado"
 */
public final class SistemaEcuacion {
    private final Ecuacion[] ecuaciones;
    private final int filas;

    /**
     * Crea un sistema de ecuaciones lineales
     * 
     * @param ecuaciones: Se adueña de este arreglo de ecuaciones, y es libre de
     *                    modificarlo
     */
    public SistemaEcuacion(Ecuacion[] ecuaciones) {
        // Debido a que se quiere abusar del método de Matriz Inversa por Gauss Jordan,
        // el valor que normalmente representaría la dimensión de la matriz, en lugar de
        // ser la cantidad de variables en la ecuación, sería entonces la cantidad de
        // ecuaciones en el sistema
        int cantidad_de_ecuaciones = ecuaciones.length;

        for (Ecuacion ecuacion : ecuaciones) {
            if (ecuacion.variables() != cantidad_de_ecuaciones) {
                throw new IllegalArgumentException("Las ecuaciones no tienen la misma cantidad de coeficientes");
            }
        }
        this.ecuaciones = ecuaciones;
        this.filas = cantidad_de_ecuaciones;
    }

    public void producto_escalar(double escalar) {
        for (int i = 1; i < this.ecuaciones.length; i++) {
            this.ecuaciones[i] = this.ecuaciones[i].producto_escalar(escalar);
        }
    }

    /**
     * Edita el sistema de ecuaciones a una matriz triangular inferior (Llenando de
     * ceros los elementos superior a la diagonal principal)
     */
    public void a_triangular_inferior() {
        // Dimensión de la matriz
        int dim = this.filas;
        int ultima_columna = dim - 1; // Indice de la última fila
        // (2) Recorrer por columna (empezando desde la última columna)
        for (int col = ultima_columna; col >= 1; col--) {
            int base_row = col; // Fila base
            // (1) Recorrer por fila (empenzando desde la última fila)
            for (int row = col - 1; row >= 0; row--) {
                Ecuacion fila_a = this.ecuaciones[base_row], fila_b = this.ecuaciones[row];
                double escalar_a = fila_a.coeficientes()[col];
                double escalar_b = fila_b.coeficientes()[col];
                if (escalar_b == 0 || escalar_a == 0) {
                    continue;
                }
                Ecuacion f_a = fila_a.producto_escalar(escalar_b / escalar_a);
                Ecuacion f_b = fila_b.clone();

                // Asignar la resta de la fila
                this.ecuaciones[row] = f_b.resta(f_a);
            }
        }
        return;
    }

    /**
     * Edita el sistema de ecuaciones a una matriz triangular superior
     */
    public void a_triangular_superior() {
        // Dimensión de la matriz
        int dim = this.filas;
        // (2) Recorrer por columna
        for (int col = 0; col < dim - 1; col++) {
            int base_row = col; // Fila base
            // (1) Recorrer por fila
            for (int row = 1 + col; row < dim; row++) {
                Ecuacion fila_a = this.ecuaciones[base_row], fila_b = this.ecuaciones[row];
                double escalar_a = fila_a.coeficientes()[col];
                double escalar_b = fila_b.coeficientes()[col];
                if (escalar_b == 0 || escalar_a == 0) {
                    continue;
                }
                Ecuacion f_a = fila_a.producto_escalar(escalar_b / escalar_a);
                Ecuacion f_b = fila_b.clone();

                // Asignar la resta de la fila
                this.ecuaciones[row] = f_b.resta(f_a);
            }
        }
        return;
    }

    /**
     * Edita el sistema de ecuaciones para que su diagonal sea unitaria
     */
    public void a_diagonal_unitario() {
        for (int i = 0; i < this.filas; i++) {
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

    public static Double[] DESPEJAR(SistemaEcuacion sistema) {
        sistema = sistema.clone();
        sistema.a_triangular_inferior();
        sistema.a_triangular_superior();
        sistema.a_diagonal_unitario();
        Double[] respuestas = new Double[sistema.filas];
        for (int i = 0; i < sistema.filas; i++) {
            respuestas[i] = sistema.resultado(i);
        }
        return respuestas;
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

    public Ecuacion[] matriz_inversa() {
        return SistemaEcuacion.matriz_inversa(this);
    }

    public static Ecuacion[] matriz_inversa(SistemaEcuacion original) {
        if (original.determinante() == 0)
            throw new IllegalArgumentException("La matriz no tiene inversa");

        // Clonar el sistema de ecuaciones para no modificar el original
        SistemaEcuacion sistema = original.clone();
        original = null; // Asegurarse que el original no se modifique por accidente
        final int FILAS = sistema.filas;

        // Expandir sistema de ecuaciones con una matriz identidad para que sea
        // posteriormente procesada para obtener la inversa
        for (int i = 0; i < sistema.filas; i++) {

            Double[] coeficientes = new Double[FILAS * 2];
            final Double[] COEFICIENTES = sistema.ecuaciones[i].coeficientes();

            // Llenar con copia
            for (int j = 0; j < FILAS; j++)
                coeficientes[j] = COEFICIENTES[j];
            // Llenar con ceros
            for (int j = FILAS; j < FILAS * 2; j++)
                coeficientes[j] = 0.0;

            // Reemplazar con 1 en la diagonal que representa la matriz identidad
            coeficientes[FILAS + i] = 1.0;
            sistema.ecuaciones[i] = Ecuacion.of(coeficientes, 0);
        }

        // Operar en la nueva "matriz" para obtener la inversa
        sistema.a_triangular_superior();
        sistema.a_triangular_inferior();
        sistema.a_diagonal_unitario();

        // Extraer la matriz inversa
        Ecuacion[] inversa = new Ecuacion[FILAS];
        for (int fila = 0; fila < FILAS; fila++) {
            Double[] coeficientes = new Double[FILAS];
            for (int j = 0; j < FILAS; j++)
                coeficientes[j] = sistema.ecuaciones[fila].coeficientes()[FILAS + j];
            inversa[fila] = Ecuacion.of(coeficientes, 0);
        }
        return inversa;
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (Ecuacion ecuacion : this.ecuaciones) {
            sb.append(ecuacion.toString()).append("\n");
        }
        return sb.toString();
    }

    public int filas() {
        return this.filas;
    }

    public double resultado(int fila) {
        return this.ecuaciones[fila].resultado();
    }

    public Ecuacion[] ecuaciones() {
        return this.ecuaciones;
    }
}