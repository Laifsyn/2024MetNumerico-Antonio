package ii_2024.met_numerico.aproximacion;


import ii_2024.met_numerico.DrawTable;

public class Main {

    /**
     * # hello
     * hello
     * - wjat
     * - to do
     */
    public static void main(String[] args) {
        System.out.println("Hello World!");

        DrawTable table = new DrawTable();
        table.insertar_fila(new String[] { "x", "f(x)" });
        // FOfX f = x -> {
        //     double result = (1 - 0.6 * x) / x;
        //     table.insertar_fila(new String[] { String.valueOf(x), String.valueOf(result) });
        //     return result;
        // };

        FOfX f = x -> {
            // x^2 - 5x + 2
            return Math.pow(x,2) -5*x+2;
        };
        var resultados2 = Funciones.biseccion(f, 5, 4, 1).get();
        resultados2.table().separar_cada_fila();
        System.out.println(resultados2.toString());
        var resultados = Funciones.regla_falsa(f, 5, 4, 1);
        resultados.table().separar_cada_fila();
        System.out.println(resultados.toString());

        FOfX secante = x -> {
            // e^{-x}-x
            return Math.exp(-x) - x;
        };
        var resultados3 = Funciones.secante(secante, 0.5, 1, 1);
        resultados3.table().separar_cada_fila();
        System.out.println(resultados3.toString());
    }


}


