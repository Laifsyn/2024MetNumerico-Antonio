from typing import Callable, Optional, Tuple, TypeVar
from utils.draw_table import DibujarTabla as Tabla

# # importing the required modules
# import matplotlib.pyplot as plt
# import numpy as np

# # setting the x - coordinates
# x = np.arange(0, 2*(np.pi), 0.1)
# # setting the corresponding y - coordinates
# y = np.sin(x)

# # plotting the points
# plt.plot(x, y)

# # function to show the plot
# plt.show()


T = TypeVar("A")


def a_6_decimales(x: float) -> float:
    return round(x, 6)


def ERROR(new: T, old: T) -> T:
    return abs(1 - old / new) * 100


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
    tabla.insertar_encabezados(
        ["i", "a", "b", "f(a)", "f(b)", "c_{i+1}", "f(a)*f(c)", "Error (%)"]
    )

    # Redondear el resultado de f a 6 decimales
    tmp = f
    f = lambda x: a_6_decimales(tmp(x))

    # Inicializamos old_c con un valor arbitrario no-constante
    old_c = a
    i = -1
    # Populamos la tabla con los valores iniciales
    while True:
        i += 1
        f_a = f(a)
        f_b = f(b)
        c = a_6_decimales(b - f_b * (b - a) / (f_b - f_a))
        error_porcentual = ERROR(c, old_c)

        f_c = f(c)
        if f_a * f_c < 0:
            b = c
        elif f_a * f_c > 0:
            a = c
        else:
            # Si f(a) * f(c) == 0, entonces `c` o `a` es la raíz
            if f_a == 0:
                c = a
            error_porcentual = 0.0
        old_c = c
        tabla.insertar_fila(
            [
                i,
                a,
                b,
                f_a,
                f_b,
                c,
                a_6_decimales(f_a * f_c),
                f"{MetodosNumericos.A_FORMATO_ERROR(error_porcentual)}",
            ]
        )
        if error_porcentual < percent_threshold:
            tabla.separar_cada_fila()
            return (tabla, c)


def biseccion(
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
    a: float = x0
    b: float = x1
    # Dibujar los encabezados
    tabla = Tabla()
    tabla.insertar_encabezados(["i", "a", "b", "c", "f(a) * f(c)", "Error (%)"])

    # Redondear el resultado de f a 6 decimales
    tmp = f
    f = lambda x: a_6_decimales(tmp(x))

    # Inicializamos old_c con un valor arbitrario no-constante
    old_c = a
    i = -1
    # Populamos la tabla con los valores iniciales
    while True:
        i += 1
        c = a_6_decimales((a + b) / 2)
        f_a = f(a)
        f_c = f(c)
        error_porcentual = ERROR(c, old_c)
        tabla.insertar_fila(
            [
                i,
                a,
                b,
                c,
                a_6_decimales(f_a * f_c),
                f"{MetodosNumericos.A_FORMATO_ERROR(error_porcentual)}",
            ]
        )
        if f_a * f_c < 0:
            b = c
        elif f_a * f_c > 0:
            a = c
        else:
            # Si f(a) * f(c) == 0, entonces `c` o `a` es la raíz
            if f_a == 0:
                c = a
            error_porcentual = 0.0
        old_c = c

        if error_porcentual < percent_threshold:
            tabla.separar_cada_fila()
            return (tabla, c)


def secante(
    f: Callable[[float], float], x0: float, x1: float, percent_threshold: float
) -> Tuple[Tabla, float]:
    """
    Args:
        f (Callable[[float], float]): Función a evaluar.
        x0 (float): Lower Bound
        x1 (float): Upper Bound
        percent_threshold (float): Número en formato de porcentaje para la tolerancia.

    Returns:
        Tuple[Tabla, float]:
    """
    # Renombrar variables para facilitar la lectura
    x0: float = x0
    xi: float = x1
    # Dibujar los encabezados
    tabla = Tabla()
    EMPTY_CELL = "------"
    tabla.insertar_encabezados(
        ["i", "x_{i}", "f(x_{i-1} )", "f(x_{i})", "x_{i+1}", "Error (%)"]
    )
    tabla.insertar_fila(
        ["-1", f"{x0:.6f}", EMPTY_CELL, EMPTY_CELL, EMPTY_CELL, EMPTY_CELL]
    )
    # Redondear el resultado de f a 6 decimales
    tmp = f
    f = lambda x: a_6_decimales(tmp(x))

    # Inicializamos old_c con un valor arbitrario no-constante
    old_x = x0
    i = -1
    # Populamos la tabla con los valores iniciales
    while True:
        i += 1
        f_x_sub_1 = f(old_x)
        f_x = f(xi)
        x_plus_1 = a_6_decimales(xi - f_x * (old_x - xi) / (f_x_sub_1 - f_x))
        error_porcentual = ERROR(x_plus_1, xi)
        tabla.insertar_fila(
            [
                i,
                xi,
                f_x_sub_1,
                f_x,
                x_plus_1,
                f"{MetodosNumericos.A_FORMATO_ERROR(error_porcentual)}",
            ]
        )
        old_x = xi
        xi = x_plus_1

        if error_porcentual < percent_threshold:
            tabla.separar_cada_fila()
            return (tabla, x_plus_1)


def main():
    func = lambda x: x**3 - 6 * x**2 + 11 * x - 6
    intervalos = [1.2, 2.9]
    Regla_falsa = regla_falsa(func, intervalos[0], intervalos[1], 1)
    Biseccion = biseccion(func, intervalos[0], intervalos[1], 1)
    Secante = secante(func, intervalos[0], intervalos[1], 1)

    if Biseccion is not None:
        tabla, raiz = Biseccion
        print(f"# Método de Bisección\nLa raíz es {raiz}")
        print(tabla)
    if Regla_falsa is not None:
        tabla, raiz = Regla_falsa
        print(f"# Método de Regla Falsa\nLa raíz es {raiz}")
        print(tabla)
    if Secante is not None:
        tabla, raiz = Secante
        print(f"# Método de Secante\nLa raíz es {raiz}")
        print(tabla)


main()
