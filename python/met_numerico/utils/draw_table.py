from dataclasses import dataclass


class DibujarTabla:

    _NW_CORNER = "┌"
    _W_CORNER = "├"
    _SW_CORNER = "└"

    _NE_CORNER = "┐"
    _E_CORNER = "┤"
    _SE_CORNER = "┘"

    _N_CORNER = "┬"
    _M_CORNER = "┼"
    _S_CORNER = "┴"

    _VERTICAL_BAR = "│"
    _HORIZONTAL_BAR = "─"

    def __init__(self):
        self._encabezado: list[str] = []
        self._contenido: list[list[str]] = []
        self._columnas: int = 0
        self._separar_cada_fila: bool = False

    def __str__(self) -> str:
        # calcular el padding necesario para cada columna
        rows: list[str] = []
        top_corners: dict[str, str] = {
            "Left": DibujarTabla._NW_CORNER,
            "Mid": DibujarTabla._N_CORNER,
            "Right": DibujarTabla._NE_CORNER,
        }
        mid_corners = {
            "Left": DibujarTabla._W_CORNER,
            "Mid": DibujarTabla._M_CORNER,
            "Right": DibujarTabla._E_CORNER,
        }
        bottom_corners = {
            "Left": DibujarTabla._SW_CORNER,
            "Mid": DibujarTabla._S_CORNER,
            "Right": DibujarTabla._SE_CORNER,
        }
        paddings = self._max_paddings()

        # Imprimir borde superior
        rows.append(DibujarTabla._borde(paddings, top_corners))

        # Agregar encabezados
        if len(self._encabezado) > 0:
            fila = []
            for i in range(self._columnas):
                fila.append(self._encabezado[i].ljust(paddings[i]))
            rows.append(
                DibujarTabla._VERTICAL_BAR
                + DibujarTabla._VERTICAL_BAR.join(fila)
                + DibujarTabla._VERTICAL_BAR
            )
            rows.append(DibujarTabla._borde(paddings, mid_corners))

        # Imprimir contenido
        for fila in self._contenido:
            fila_formateada = [
                element.ljust(paddings[i]) for i, element in enumerate(fila)
            ]
            rows.append(
                DibujarTabla._VERTICAL_BAR
                + DibujarTabla._VERTICAL_BAR.join(fila_formateada)
                + DibujarTabla._VERTICAL_BAR
            )
            if self._separar_cada_fila:
                rows.append(DibujarTabla._borde(paddings, mid_corners))

        if len(self._contenido) > 0 and self._separar_cada_fila:
            rows.pop()

        rows.append(DibujarTabla._borde(paddings, bottom_corners))

        return "\n".join(rows)

    def insertar_fila(self, fila: list):
        if len(self._contenido) == 0:
            self._columnas = len(fila)
        elif len(fila) != self._columnas:
            raise ValueError(
                "La cantidad de elementos en la fila no es igual a la cantidad de columnas: \
                Cantidad de filas: {0}, Cantidad de columnas: {1}".format(
                    len(fila), self._columnas
                )
            )

        self._contenido.append([str(element) for element in fila])

    def separar_cada_fila(self):
        self._separar_cada_fila = True

    def insertar_encabezados(self, encabezados: list):
        if self._columnas != 0:
            if self._columnas != len(encabezados):
                raise ValueError(
                    "La cantidad de elementos en la fila no es igual a la cantidad de columnas: \
                    Cantidad de filas: {0}, Cantidad de columnas: {1}".format(
                        len(encabezados), self._columnas
                    )
                )
        else:
            self._columnas = len(encabezados)

        self._encabezado = [str(encabezado) for encabezado in encabezados]

    def _max_paddings(self) -> list[int]:
        paddings = []
        for i in range(self._columnas):
            # Obtener la longitud del encabezado actual
            header_length = len(self._encabezado[i])

            # Obtener la longitud de la columna actual
            column_lengths = [len(fila[i]) for fila in self._contenido]

            # Obtener la longitud máxima de la columna actual
            max_length = max([header_length] + column_lengths)

            # Agregar el padding a la lista
            paddings.append(max_length)
        return paddings

    def _borde(paddings: list[int], corners: dict[str, str]) -> str:
        borde = [corners["Left"]]
        for padding in paddings:
            borde.append(DibujarTabla._HORIZONTAL_BAR * padding + corners["Mid"])
        borde[-1] = "─" * paddings[-1] + corners["Right"]
        return "".join(borde)
