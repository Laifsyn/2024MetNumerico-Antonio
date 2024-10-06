package ii_2024.met_numerico.aproximacion;

/**
 * Funciones de un argumento
 */
public interface FOfX {
    double eval(double x);

    /**
     * Funcion para redondear
     */
    public static FOfX rounder(int dec_positions) {
        return x -> {
            return Math.round(x * Math.pow(10, dec_positions)) / Math.pow(10, dec_positions);
        };
    }
}
