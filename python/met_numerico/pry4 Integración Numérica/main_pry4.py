from enum import Enum
from typing import *


class DataArgument(Enum):
    N = 0
    X = 1
    F_x = 2


class Estrategia(Enum):
    Trapecio = 0
    Simpson_13 = 1
    Simpson_38 = 2

    def __str__(self) -> str:
        return self.name.replace("_", " ")

    def is_valid_segments(self, n: int) -> bool:
        assert n == int(n)  # Asegurar que sea un entero
        if self == Estrategia.Trapecio:
            return True
        if self == Estrategia.Simpson_13:
            return n % 2 == 0 and n >= 4
        if self == Estrategia.Simpson_38:
            return n % 3 == 0 and n >= 3
        raise ValueError("Estrategia desconocida")

    def integrate(
        self, integration_instance: "IntegrationStrategy"
    ) -> Tuple[float, List[Tuple[int, float, float]]]:
        segmentos = integration_instance.segmentos
        assert self.is_valid_segments(
            segmentos
        ), f"Cantidad de segmentos inválida para la estrategia {self}"
        (a, b) = integration_instance.limites
        assert a < b, "Los límites de integración deben ser `a < b`"
        f = integration_instance.function

        rows = segmentos + 1
        h = (b - a) / segmentos
        n = [i for i in range(rows)]
        x = [a + i * h for i in n]
        f_x = [f(x_i) for x_i in x]

        N = DataArgument.N.value
        X = DataArgument.X.value
        F_X = DataArgument.F_x.value

        data: List[Tuple[int, float, float]] = [
            (n[i], x[i], f_x[i]) for i in range(rows)
        ]

        assert len(data) == rows, "Error en la creación de la tabla de datos"
        assert data[0][N] == n[0], "Error en la creación de la tabla de datos: N"
        assert data[0][X] == x[0], "Error en la creación de la tabla de datos: X"
        assert data[0][F_X] == f_x[0], "Error en la creación de la tabla de datos: F(x)"

        if self == Estrategia.Trapecio:
            resultado = self.trapecio(data, h)
        elif self == Estrategia.Simpson_13:
            resultado = self.simpson_13(data, h)
        elif self == Estrategia.Simpson_38:
            resultado = self.simpson_38(data, h)
        else:
            raise ValueError("Estrategia desconocida")

        return (resultado, data)

    def trapecio(
        self, data: List[Tuple[int, float, float]], h: Optional[float] = None
    ) -> float:
        X, Y = DataArgument.X.value, DataArgument.F_x.value
        if h is None:
            h = data[1][X] - data[0][X]
        n = len(data)
        assert n > 1, "No hay suficientes datos para integrar"

        suma = 0.0
        for i in range(1, n - 1):
            suma += data[i][Y]
        suma = data[0][Y] + data[n - 1][Y] + 2 * suma
        return h / 2 * suma

    def simpson_13(
        self, data: List[Tuple[int, float, float]], h: Optional[float] = None
    ) -> float:
        X, Y = DataArgument.X.value, DataArgument.F_x.value
        if h is None:
            h = data[1][X] - data[0][X]

        n = len(data)
        assert n > 4, "No hay suficientes datos para integrar"
        assert (n - 1) % 2 == 0, f"La cantidad de segmentos debe ser par (n+1={n})"

        suma_impar = 0.0
        suma_par = 0.0

        for i in range(1, n - 1):
            if i % 2 == 0:
                suma_par += data[i][Y]
            else:
                suma_impar += data[i][Y]

        result = data[0][Y] + 4 * suma_impar + 2 * suma_par + data[-1][Y]
        return (h / 3) * result

    def simpson_38(
        self, data: List[Tuple[int, float, float]], h: Optional[float] = None
    ) -> float:
        X, Y = DataArgument.X.value, DataArgument.F_x.value

        if h is None:
            h = data[1][X] - data[0][X]

        n = len(data)
        assert (
            n > 1 and (n - 1) % 3 == 0
        ), "Simpson's 3/8 requiere una cantidad de intervalos en múltiplo de 3"

        suma_multiples_of_3 = 0.0
        suma_resto = 0.0

        for i in range(1, n - 1):
            if i % 3 == 0:
                suma_multiples_of_3 += data[i][Y]
            else:
                suma_resto += data[i][Y]

        result = data[0][Y] + 2 * suma_multiples_of_3 + 3 * suma_resto + data[-1][Y]
        return (3 * h / 8) * result


class IntegrationBuilder:
    def __init__(
        self,
        function: Callable[[float], float] | None = None,
        limites: Tuple[float, float] | None = None,
        segmentos: int | None = None,
        estrategia: Estrategia | None = None,
    ) -> None:
        if limites is not None:
            (l, r) = limites
            if l > r:  # Intercambiar orden
                (r, l) = (l, r)
            limites = (l, r)
        self.limites: Optional[Tuple[float, float]] = limites
        self.segmentos = segmentos
        self.estrategia = estrategia
        self.function = function


class IntegrationStrategy:
    def __init__(self, builder: IntegrationBuilder):
        # Llenar valores que no están definidos
        if builder.limites is None:
            builder.limites = (0, 1)
        if builder.segmentos is None:
            builder.segmentos = 6
        if builder.estrategia is None:
            builder.estrategia = Estrategia.Trapecio
        if builder.function is None:
            builder.function: Callable[[float], float] = lambda x: x**2  # type: ignore
        # Asignar valores
        if not builder.estrategia.is_valid_segments(builder.segmentos):
            raise ValueError("Cantidad de segmentos inválida")
        self.function = builder.function
        self.limites: Tuple[float, float] = builder.limites
        self.segmentos = builder.segmentos
        self.estrategia = builder.estrategia

    def __str__(self) -> str:

        try:
            f_1_result = str(self.function(1))
        except Exception as e:
            f_1_result = f"Error: `{e}`"

        return f"Integración con {self.estrategia} en {self.segmentos} segmentos, límites {self.limites}. Función: No representable - f(1) = {f_1_result}"

    def update_parameters(self) -> Self:
        """Actualizar los parámetros de la integración"""
        print("Parámetros actuales:", f"\n{self}", "\n")
        lista_opciones = [
            "Parámetros disponibles:\n",
            "-1: Imprimir opciones\n",
            "0: Cancelar\n",
            "1: Función\n",
            "2: Límites\n",
            "3: Segmentos\n",
            "4: Estrategia(i.j. Simpson, Trapecio)\n",
        ]
        print(
            *lista_opciones,
        )

        while True:
            opcion = leer_entero("Elija un parámetro para cambiar: ")
            match opcion:
                case -1:
                    print(*lista_opciones)
                case 0:
                    break
                case 1:
                    self.function = leer_función()
                case 2:
                    self.limites = leer_límites()
                case 3:
                    n = leer_cantidad_de_segmentos()
                    if not self.estrategia.is_valid_segments(n):
                        print(
                            f"Cantidad de segmentos inválida para el método de `{self.estrategia}`. Intente cambiar la método primero"
                        )
                        continue
                    self.segmentos = n
                case 4:
                    strat = leer_estrategia()
                    if not strat.is_valid_segments(self.segmentos):
                        print(
                            f"La estrategia {strat} es incompatible para `{self.segmentos}` segmentos. Intente modificar los segmentos primero"
                        )
                        continue
                    self.estrategia = strat
                case _:
                    print("Opción inválida")
                    continue
            print(f"Parámetro ({opcion}) ha sido actualizado!")
        return self

    def integrate(self) -> Tuple[float, List[Tuple[int, float, float]]]:
        # La lógica de integración debería en realidad estar definido en la estrategia. Por eso se delegará el trabajo a la estrategia
        # TODO: print output
        return self.estrategia.integrate(self)


def leer_función(test_value: int = 2) -> Callable[[float], float]:
    read_result = input("Introduce la función a integrar (ej. `(58**x)/20`): ")

    def f(x: float) -> float:
        # fmt: off
        # Importar funciones matemáticas para la función de evaluar
        from math import (
            e, pi, tau, inf, nan,
            sin, cos, tan, asin, acos, atan,
            sinh, cosh, tanh, asinh, acosh, atanh,
            log, log10, log2, log1p, exp, expm1, sqrt,
            ceil, floor, trunc, copysign,
            pow, degrees, radians, factorial, gcd
        )
        # fmt: on
        return eval(read_result)

    try:
        f(test_value)
    except Exception as e:
        print("Error: ", e)
        print("Se esperaba números, variable `x`, operadores y funciones matemáticos\n")
        return leer_función(test_value)
    return f


def leer_cantidad_de_segmentos() -> int:
    return int(__leer_numero("Elija la cantidad de segmentos en dividir el límite: "))


def leer_entero(msg: str) -> int:
    return int(__leer_numero(msg))


def __leer_numero(msg: str) -> float:
    while True:
        try:
            n = float(input(msg))
            break
        except ValueError:
            print("Entrada inválida. Por favor, introduce un número válido.")
    return n


def leer_límites() -> Tuple[float, float]:
    print(
        "Defina los límites de integración. (Se reordenará de menor a mayor automáticamente)"
    )
    (smaller, bigger) = (
        __leer_numero("Defina el límite Inferior "),
        __leer_numero("Defina el límite Superior "),
    )
    if bigger < smaller:
        (smaller, bigger) = (bigger, smaller)

    return (smaller, bigger)


def leer_estrategia() -> Estrategia:
    # Convertir un entero a una Estrategia
    while True:
        n = leer_entero(
            "Ingrese una estrategia: \n(0) Trapecio, \n(1) Simpson 1/3, \n(2) Simpson 3/8\n"
        )
        for e in Estrategia:
            if e.value == n:
                return e
        print("Estrategia inválida")


def main():
    integration_method = IntegrationStrategy(IntegrationBuilder())
    ESTRATEGIAS = Estrategia
    for e in ESTRATEGIAS:
        print(f"Para la estrategia {e}:")
        for i in range(10):
            print(f"{i}: {e.is_valid_segments(i)}")
    func = leer_función()
    integration_method.function = func
    integration_method.update_parameters()
    print("Parámetros actualizados!:", integration_method)
    lista_opciones = [
        "\nElija una opción:\n-1: Mostrar opciones \n0: Salir\n1: Integrar\n2: Cambiar parámetros\n"
    ]
    while True:
        opcion = leer_entero(*lista_opciones)
        match opcion:
            case -1:
                print(*lista_opciones)
            case 0:
                break
            case 1:
                result, data = integration_method.integrate()
                print("Tabla de datos:")
                print(f"|{"N":^5}|{"X":^19}|{"f(x)":^19}|")
                for row in data:
                    print(f"|{str(row[0]):^5}|{str(row[1]):<19}|{str(row[2]):<19}|")
                print(f"{"FIN DE LA TABLA":^42}")
                print(f"Área Estimada: {integration_method.estrategia} = {result}")
            case 2:
                integration_method.update_parameters()
            case _:
                print("Opción inválida")
                continue
    print("Programa finalizado")


main()
