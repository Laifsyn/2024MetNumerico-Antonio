package ii_2024.met_numerico.pry3_Regresion;

// Nota: No he pensado muy a detalle las implicaciones de usar entre `Double[]` o `double[]`
public final record Ecuacion(Double[] coeficientes, double resultado, int variables) {

    // Método estático para instanciación. Contiene la lógica de validación
    public static Ecuacion of(Double[] coeficientes, double resultado) {
        if (coeficientes == null || coeficientes.length == 0) {
            // Tirar un error porque se asume que se utilizó mal la función.
            throw new IllegalArgumentException("No se puede crear una ecuacion sin coeficientes");
        }

        // Calcular grado de la ecuación
        int variables = coeficientes.length;

        return new Ecuacion(coeficientes, resultado, variables);
    }

    /**
     * Crea una copia, siendo el resultado de la suma de esta ecuación con otra.
     * Devuelve `null` si las ecuaciones no son del mismo grado.
     */
    public Ecuacion suma(final Ecuacion rhs) {
        if (this.variables != rhs.variables) {
            // Tirar un error porque se asume que se utilizó mal la función.
            throw new IllegalArgumentException(
                    "Las ecuaciones no tienen la misma cantidad de coeficientes para realizar la suma");
        }
        final double resultado = this.resultado + rhs.resultado;
        final int grado = this.variables;
        final Double[] nuevos_coeficientes = new Double[grado];

        for (int i = 0; i < grado; i++)
            nuevos_coeficientes[i] = this.coeficientes[i] + rhs.coeficientes[i];

        return new Ecuacion(nuevos_coeficientes, resultado, grado);
    }

    public Ecuacion resta(final Ecuacion rhs) {
        if (this.variables != rhs.variables) {
            // Tirar un error porque se asume que se utilizó mal la función.
            throw new IllegalArgumentException(
                    "Las ecuaciones no tienen la misma cantidad de coeficientes para realizar la resta");
        }
        return this.suma(rhs.producto_escalar(-1));
    }

    /**
     * Crea una copia, siendo el resultado de esta ecuación multiplicado por un
     * escalar.
     */
    public Ecuacion producto_escalar(final double escalar) {
        if (escalar == 1) {
            return this.clone();
        }
        final double resultado = this.resultado * escalar;
        final int grado = this.variables;

        final Double[] nuevos_coeficientes = new Double[grado];
        for (int i = 0; i < grado; i++) {
            nuevos_coeficientes[i] = this.coeficientes[i] * escalar;
        }

        return Ecuacion.of(nuevos_coeficientes, resultado);
    }

    public Ecuacion clone() {
        return Ecuacion.of(this.coeficientes.clone(), this.resultado);
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < this.variables; i++) {
            double num = this.coeficientes[i];
            if (num < 0) {
                sb.append(" - ");
            } else {
                sb.append(" + ");
            }
            if (i == 0)
                sb.delete(sb.length() - 3, sb.length());
            sb.append(Math.abs(num));
            sb.append("x_");
            sb.append(i);
        }
        sb.append(" = ");
        sb.append(this.resultado);
        return sb.toString();
    }
}
