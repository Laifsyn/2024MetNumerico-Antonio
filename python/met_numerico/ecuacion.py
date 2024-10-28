from typing import List, Self


class Ecuacion:
    def __init__(self, coeficientes: List[float], resultado: float):
        self.coeficientes = coeficientes
        self.resultado = resultado
        self.variables = len(coeficientes)

    @staticmethod
    def of(coeficientes: List[float], resultado: float) -> "Ecuacion":
        if not coeficientes:
            raise ValueError("No se puede crear una ecuación sin coeficientes")
        return Ecuacion(coeficientes, resultado)

    def suma(self, other: "Ecuacion") -> "Ecuacion":
        if self.variables != other.variables:
            raise ValueError(
                "Las ecuaciones no tienen la misma cantidad de coeficientes para realizar la suma"
            )

        nuevos_coeficientes = [
            x + y for x, y in zip(self.coeficientes, other.coeficientes)
        ]
        nuevo_resultado = self.resultado + other.resultado

        return Ecuacion.of(nuevos_coeficientes, nuevo_resultado)

    def resta(self, otra: Self) -> "Ecuacion":
        return self.suma(otra.producto_escalar(-1))

    def producto_escalar(self, escalar: float) -> "Ecuacion":
        if escalar == 1:
            return self.clone()

        nuevos_coeficientes = [c * escalar for c in self.coeficientes]
        nuevo_resultado = self.resultado * escalar

        return Ecuacion.of(nuevos_coeficientes, nuevo_resultado)

    def __str__(self) -> str:
        partes = []
        for i, coef in enumerate(self.coeficientes):
            signo = " - " if coef < 0 else " + "
            if i == 0:
                signo = ""  # Eliminar el signo inicial
            partes.append(f"{signo}{abs(coef)}x_{i}")
        partes.append(f" = {self.resultado}")
        return "".join(partes)

    def clone(self) -> "Ecuacion":
        return Ecuacion(self.coeficientes[:], self.resultado)
