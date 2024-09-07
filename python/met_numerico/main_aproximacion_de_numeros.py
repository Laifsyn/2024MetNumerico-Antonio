from typing import Callable, Optional, Tuple
from utils.draw_table import DibujarTabla as Tabla


A_6_DECIMALES = lambda f : lambda x: round(f(x), 6)
ERROR= lambda new, old: abs((new - old) / new) * 100

class MetodosNumericos:
    ENCABEZADO_ERROR = "Error(%)"
    FORMATO_ERROR = "{:.4f}%"
    A_FORMATO_ERROR = lambda x: MetodosNumericos.FORMATO_ERROR.format(x)


def regla_falsa(
    f: Callable[[float], float], x0: float, x1: float, percent_threshold: float
) -> Optional[Tuple[Tabla, float]]:
    """
    Args:
        f (Callable[[float], float]): Función a evaluar.
        x0 (float): Lower Bound
        x1 (float): Upper Bound
        percent_threshold (float): Número en formato de porcentaje para la tolerancia.

    Returns:
        Optional[Tuple[Tabla, float]]:
    """
    # Renombrar variables para facilitar la lectura
    a = x0
    b = x1
    # Dibujar los encabezados, y habilitar separación por fila
    tabla = Tabla()
    tabla.insertar_encabezados(["i","a", "b", "f(a)", "f(b)", "c_{i+1}", "f(a)*f(c)", "Error (%)"])

    # Redondear la resultado de f a 5 decimales
    f = A_6_DECIMALES(f)
    a_6_decimales = A_6_DECIMALES(lambda x: x)
    # Inicializamos old_c con un valor arbitrario no-constante
    old_c = a
    i = -1
    # Populamos la tabla con los valores iniciales
    while True:
        i+=1
        f_a = f(a)
        f_b = f(b)
        c = a_6_decimales(  b - f_b * (b - a) / (f_b - f_a))
        error_porcentual = ERROR(c, old_c)
        
        f_c = f(c)
        if f_a * f_c < 0:
            b = c
        elif f_a * f_c > 0:
            a = c
        else:
            # Si f(a) * f(c) == 0, entonces `c` o `a` es la raíz
            if f_a == 0:
                c=a
            error_porcentual = 0.0
        old_c = c    
        tabla.insertar_fila([i,a, b, f_a, f_b, c, a_6_decimales(f_a * f_c), f"{MetodosNumericos.A_FORMATO_ERROR(error_porcentual)}"])
        if error_porcentual < percent_threshold:
            tabla.separar_cada_fila()
            return (tabla, c)


def main():
    func = lambda x: x**3 - 6 * x**2 + 11 * x - 6
    intervalos = [1.2, 2.9]
    regla_false = regla_falsa(func, intervalos[0], intervalos[1], 1)

    if regla_false is not None:
        tabla, raiz = regla_false
        print(f"La raíz es {raiz}")
        print(tabla)

main()