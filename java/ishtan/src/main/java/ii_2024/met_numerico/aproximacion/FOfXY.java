package ii_2024.met_numerico.aproximacion;


public interface FOfXY {
    double eval(double x_new, double x_old);

    public static FOfXY promedio() {
        return (x_new, x_old) -> {
            return (x_new + x_old) / 2;
        };
    }

    public static FOfXY error_percent() {
        return (x_old, x_new) -> {
            return Math.abs(1 - x_old / x_new) * 100;
        };
    }
}
