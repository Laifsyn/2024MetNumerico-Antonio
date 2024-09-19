package ii_2024.met_numerico.aproximacion;

public class Main {

    public static void main(String[] args) {
        System.out.println("Hello World!");
        var f = f();
        double a = 1.5;
        double b = 2.5;

        var regla_false = Funciones.regla_falsa(f, a, b, 1).get();
        var biseccion = Funciones.biseccion(f, a, b, 1).get();
        var secante = Funciones.secante(f, a, b, 1);

        System.out.println("Bisección: \n" + biseccion);
        System.out.println("Regla falsa: \n" + regla_false);
        System.out.println("Secante: \n" + secante);

    }

    public static FOfX f() {
        // x^3-6x2+11x-6
        return x -> Math.pow(x, 3) - 6 * Math.pow(x, 2) + 11 * x - 6;
    }
}
