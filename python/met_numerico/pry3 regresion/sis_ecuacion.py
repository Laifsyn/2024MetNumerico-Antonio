from typing import List, Self
from ecuacion import Ecuacion  # Assuming you have ecuacion.py file already


class SistemaEcuacion:
    def __init__(self, ecuaciones: List[Ecuacion]):
        cantidad_de_ecuaciones = len(ecuaciones)
        for ecuacion in ecuaciones:
            if ecuacion.variables != cantidad_de_ecuaciones:
                raise ValueError(
                    "Las ecuaciones no tienen la misma cantidad de coeficientes"
                )
        self.ecuaciones = ecuaciones
        self.filas = cantidad_de_ecuaciones

    def a_triangular_inferior(self):
        dim = self.filas
        for col in range(dim - 1, 0, -1):
            for row in range(col - 1, -1, -1):
                fila_a = self.ecuaciones[col]
                fila_b = self.ecuaciones[row]
                escalar_a = fila_a.coeficientes[col]
                escalar_b = fila_b.coeficientes[col]
                if escalar_b == 0 or escalar_a == 0:
                    continue
                f_a = fila_a.producto_escalar(escalar_b / escalar_a)
                f_b = fila_b.clone()
                self.ecuaciones[row] = f_b.resta(f_a)

    def a_triangular_superior(self):
        dim = self.filas
        for col in range(dim - 1):
            for row in range(col + 1, dim):
                fila_a = self.ecuaciones[col]
                fila_b = self.ecuaciones[row]
                escalar_a = fila_a.coeficientes[col]
                escalar_b = fila_b.coeficientes[col]
                if escalar_b == 0 or escalar_a == 0:
                    continue
                f_a = fila_a.producto_escalar(escalar_b / escalar_a)
                f_b = fila_b.clone()
                self.ecuaciones[row] = f_b.resta(f_a)

    def a_diagonal_unitario(self):
        for i in range(self.filas):
            escalar = self.ecuaciones[i].coeficientes[i]
            self.ecuaciones[i] = self.ecuaciones[i].producto_escalar(1 / escalar)

    def clone(self: "SistemaEcuacion") -> "SistemaEcuacion":
        ecuaciones_clonadas = [ecuacion.clone() for ecuacion in self.ecuaciones]
        return SistemaEcuacion(ecuaciones_clonadas)

    def resultado(self, fila: int) -> float:
        return self.ecuaciones[fila].resultado

    def determinante(self) -> float:
        sistema = self.clone()
        sistema.a_triangular_superior()
        det = 1.0
        for i in range(sistema.filas):
            det *= sistema.ecuaciones[i].coeficientes[i]
        return det

    def matriz_inversa(sistema: "SistemaEcuacion") -> list[Ecuacion]:
        if sistema.determinante() == 0:
            raise ValueError("La matriz no tiene inversa")

        # Clonar el sistema para no modificar el original
        sistema = sistema.clone()
        filas = sistema.filas

        # Expandir sistema con una matriz identidad
        for i in range(filas):
            coeficientes = [0.0] * (filas * 2)
            coeficientes[:filas] = sistema.ecuaciones[i].coeficientes
            coeficientes[filas + i] = 1.0
            sistema.ecuaciones[i] = Ecuacion(coeficientes, 0)

        sistema.a_triangular_superior()
        sistema.a_triangular_inferior()
        sistema.a_diagonal_unitario()

        # Extraer la matriz inversa
        inversa = []
        for i in range(filas):
            coeficientes = sistema.ecuaciones[i].coeficientes[filas:]
            inversa.append(Ecuacion(coeficientes, 0))

        return inversa

    def __str__(self) -> str:
        return "\n".join(str(ecuacion) for ecuacion in self.ecuaciones)


def por_matriz_inversa(eq: SistemaEcuacion) -> List[float]:
    inversa = eq.matriz_inversa()
    print("Inversa de la matriz a evaluar:")
    for ecuacion in inversa:
        print(ecuacion)
    print("")

    # Se asume que siempre se tendrá n-filas para n-incógnitas
    respuestas = [0.0] * eq.filas

    for fila in range(eq.filas):
        fila_n = inversa[fila]
        for i in range(eq.filas):
            respuestas[fila] += fila_n.coeficientes[i] * eq.resultado(i)


    # Escribir nombre de las variables
    variables = [f"x_{i+1}" for i in range(eq.filas)]
    for i, respuesta in enumerate(respuestas):
        if respuesta < 0:
            print(f"{variables[i]} = {respuesta}")
        else:
            print(f"{variables[i]} =  {respuesta}")

    return respuestas


def despeje_por_gauss_jordan(eq: SistemaEcuacion) -> List[float]:
    # Operar la matriz
    eq.a_triangular_inferior()
    eq.a_triangular_superior()
    eq.a_diagonal_unitario()

    respuestas = [0.0] * eq.filas
    
    # Escribir nombre de las variables
    variables = [f"x_{i + 1}" for i in range(eq.filas)]
    for i in range(eq.filas):
        respuesta = eq.resultado(i)
        respuestas[i] = respuesta

    return respuestas


def main():
    eqs = [
        Ecuacion.of([3.0, 2.0, 1.0, 4.0], 110),
        Ecuacion.of([2.0, 1.0, 3.0, 2.0], 90),
        Ecuacion.of([1.0, 3.0, 2.0, 1.0], 85),
        Ecuacion.of([1.0, 2.0, 1.0, 2.0], 95),
    ]
    sistema_eq = SistemaEcuacion(eqs)
    print(f"\nPor Matriz Inversa:\n")
    por_inversa = por_matriz_inversa(sistema_eq.clone())
    print(f"Matriz a evaluar:\n{sistema_eq}\nPor GaussJordan")
    por_gauss_jordan = despeje_por_gauss_jordan(sistema_eq.clone())

    print("Respuestas por GaussJordan y matriz inversa respectivamente\n")
    for i in range(len(por_gauss_jordan)):
        print(f"x_{i+1}\n  {por_gauss_jordan[i]} \n  {por_inversa[i]}\n")
    print(sistema_eq)


main()
