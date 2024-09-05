package ii_2024.met_numerico.aproximacion;

public interface FOfX {
    double eval(double x);

    public static FOfX rounder(int dec_positions) {
        return x -> {
            return Math.round(x * Math.pow(10, dec_positions)) / Math.pow(10, dec_positions);
        };
    }
}
