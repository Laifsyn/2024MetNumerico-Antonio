package ii_2024.met_numerico.aproximacion;

import ii_2024.met_numerico.DrawTable;

/**
 * Clase que representa el resultado de una aproximación - Alternativa sería
 * usar un Tuple de dos elementos, pero no encuentro implementación en librería
 * estandar de Java
 */
public record ApproximationResult(DrawTable table, double result) {
    @Override
    public final String toString() {
        return "Resultado Final:" + result + "\n" + table;
    }
}