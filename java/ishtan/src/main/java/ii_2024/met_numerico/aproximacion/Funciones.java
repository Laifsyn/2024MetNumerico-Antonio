package ii_2024.met_numerico.aproximacion;

import java.util.Optional;

import ii_2024.met_numerico.DrawTable;

/**
 * TODO: When the function should error out (return None)
 */

public interface Funciones {

    public static ApproximationResult regla_falsa(FOfX f, double x0, double x1, double percent_threshold) {
        var tabla = new DrawTable();
        var deci_5 = FOfX.rounder(5); // Redondear a 5 decimales
        var error = FOfXY.error_percent();

        // renombrar variables a un nombre más significativo para el contexto
        double a = x0;
        double b = x1;

        tabla.insertar_fila(new String[] { "a", "b", "f(a)", "f(b)", "c_{i+1}", "f(a)*f(c)", "error %" });

        // Inicializar la variable con un valor arbitrario.
        double old_c = a;

        while (true) {
            double c = deci_5.eval(b - f.eval(b) * (b - a) / (f.eval(b) - f.eval(a)));
            double f_a = deci_5.eval(f.eval(a));
            double f_c = deci_5.eval(f.eval(c));
            double error_percent = error.eval(old_c, c);

            tabla.insertar_fila(new String[] { String.valueOf(a), String.valueOf(b), String.valueOf(f_a),
                    String.valueOf(f_c), String.valueOf(c), String.format("%.2f", f_a * f_c),
                    String.format("%.4f%%", error_percent) });

            // Actualizar los valores de a o b dependiendo del signo de f(a) * f(c)
            if (f_a * f_c < 0) {
                b = c;
            } else {
                a = c;
            }

            // Actualizar la variable para la siguiente iteración
            old_c = c;

            if (error_percent < percent_threshold) {
                break;
            }

        }

        return new ApproximationResult(tabla, old_c);
    }

    public static ApproximationResult secante(FOfX f, double x_i_menos_uno, double x_i, double percent_threshold) {
        var tabla = new DrawTable();

        // Renombrar variables a un nombre más significativo para el contexto
        double old_x = x_i_menos_uno;
        double x = x_i;

        /**
         * x_{i+1}=x_i-\frac{f(x_i)(x_{i-1}-x_i)}{f(x_{i-1})-f(x_i)}
         */
        // Insertar encabezados de la tabla.
        tabla.insertar_fila(new String[] { "i", "x_{i}", "f(x_{i-1})", "f(x_i)", "x_{i+1}", "error %" });
        tabla.insertar_fila(
                new String[] { "-1", String.format("%.6f", old_x), "------", "------", "------", "------" });

        var deci_5 = FOfX.rounder(5);
        FOfXY error = FOfXY.error_percent();

        // Iterar hasta que el error sea menor al umbral
        for (int i = 0; true; i++) {
            double f_old_x = deci_5.eval(f.eval(old_x));
            double f_x = deci_5.eval(f.eval(x));
            double x_plus_1 = deci_5.eval(x - f_x * (old_x - x) / (f_old_x - f_x));
            double error_percent = error.eval(x_plus_1, x);

            // Agregar la fila de esta iteración a la tabla
            tabla.insertar_fila(new String[] { String.valueOf(i), String.valueOf(x),
                    String.valueOf(f_old_x), String.valueOf(f_x), String.valueOf(x_plus_1),
                    String.format("%.4f%%", error_percent) });

            // Actualizar las variables para la siguiente iteración
            old_x = x;
            x = x_plus_1;

            if (error_percent < percent_threshold) {
                break;
            }

        }

        tabla.separar_cada_fila();
        return new ApproximationResult(tabla, x);
    }

    /**
     * 
     * @param f                 : función a evaluar
     * @param x0                : rango 2
     * @param x1                : rango 1
     * @param percent_threshold : en porcentaje
     * @return
     */
    public static Optional<ApproximationResult> biseccion(FOfX f, double x0, double x1, double percent_threshold) {
        var tabla = new DrawTable();
        var deci_5 = FOfX.rounder(5); // Redondear a 5 decimales
        var avg = FOfXY.promedio();
        var error = FOfXY.error_percent();

        // renombrar variables a un nombre más significativo para el contexto
        double a = x0;
        double b = x1;

        tabla.insertar_fila(new String[] { "a", "b", "c", "f(a) * f(c)", "error %" });

        if (f.eval(a) * f.eval(b) > 0) {
            // No hay raíz en el intervalo dado.
            return Optional.empty();
        }

        // Inicializar la variable con un valor arbitrario.
        double old_c = a;

        while (true) {
            double c = deci_5.eval(avg.eval(a, b));
            double f_a = deci_5.eval(f.eval(a));
            double f_c = deci_5.eval(f.eval(c));
            double error_percent = error.eval(old_c, c);

            tabla.insertar_fila(new String[] { String.valueOf(a), String.valueOf(b), String.valueOf(c),
                    String.format("%.2f", f_a * f_c),
                    String.format("%.4f%%", error_percent) });

            // Actualizar los valores de a o b dependiendo del signo de f(a) * f(c)
            if (f_a * f_c < 0) {
                b = c;
            } else {
                a = c;
            }
            // Actualizar la variable para la siguiente iteración
            old_c = c;

            if (error_percent < percent_threshold) {
                break;
            }
        }
        return Optional.of(new ApproximationResult(tabla, old_c));
    }
}