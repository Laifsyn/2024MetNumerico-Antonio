from manim import *
import random
from manim import BS381


def EmptyAnim() -> Wait:
    return Wait(run_time=0)


class NodeState:
    def __init__(self):
        pass


class InsercionDirecta(MovingCameraScene):
    def __init__(self):
        super().__init__()
        self.to_sort_vec = [2, 17, 0, 12, 20, 10, 6]
        random.shuffle(self.to_sort_vec)
        print(self.to_sort_vec)
        config.frame_rate = 60

    def construct(self):
        __question = self.draw_question__()
        self.draw_vec()

        # Cargar objetos necesarios para la animación
        g_highlight = self.highligther_cell
        g_focused = self.highligther_focused
        g_value = self.tex_values
        g_indexes = self.indexes
        steps_list: List[Tex] = []

        data = [x for x in self.to_sort_vec]
        data_len = len(data)
        instrucciones = VGroup(
            *[
                Tex(i)
                for i in [
                    "Si b $<$ a : Intercambiar a y b, y asignar `i` a `puntero`",
                    "Donde:",
                    "\ta = data[i]",
                    "\tb = data[puntero]",
                ]
            ]
        )
        instrucciones.arrange(DOWN)
        instrucciones.scale(0.7)
        instrucciones.align_to(self.camera.frame.get_corner(DOWN + LEFT), DOWN + LEFT)
        [
            instruccion.align_to(instrucciones.get_corner(LEFT), LEFT)
            for instruccion in instrucciones
        ]
        self.play(Write(instrucciones))
        arrow: Arrow = Arrow(UP, DOWN)
        arrow_label: Tex = Tex("Puntero").next_to(arrow, UP)
        arrow_and_label = VGroup(arrow, arrow_label)
        for cola_de_particion in range(1, data_len):
            puntero = cola_de_particion
            step = Tex(str(cola_de_particion))
            step.align_to(self.camera.frame.get_corner(UP + LEFT), UP + LEFT)
            vgroup_steps: VGroup | None = None
            self.add(step)
            # Resaltar/Colorear el elemento de comparación.
            focus_mobject = g_value[puntero]
            focus_mobject.set_color(PINK)
            triggered_flag: List[Animation] | None = (
                None  # A flag that represents that a set of data suffers no changes (to color objects which value are below the value[pointer])
            )
            ## Dibujar Flecha de Puntero
            steps_list.append(Tex(f"Pasada \\#{cola_de_particion}").scale(0.7))
            self.add(g_focused[0])
            self.remove(arrow_and_label)
            self.play(
                LaggedStart(
                    Create(arrow_and_label.next_to(g_indexes[puntero], UP)),
                    Write(g_focused[cola_de_particion]),
                    lag_ratio=0.4,
                )
            )
            for i in reversed(range(0, cola_de_particion)):
                step.become(
                    Tex(
                        f"Pasada \\#{cola_de_particion}, Comparaciones$_i$: {i}/{cola_de_particion-1}"
                    ).align_to(step, LEFT + UP)
                )

                a = Tex(f"{data[i]}").set_color(g_value[i].get_color())
                b = Tex(f"{data[puntero]}", " $<$ ")
                b[0].set_color(PINK)
                comparison = VGroup(b, a).arrange(RIGHT).next_to(g_highlight, DOWN)
                comparison[1] = g_value[i].copy()
                self.add(comparison[0])
                self.play(
                    comparison[1].animate.become(a),
                    run_time=0.5,
                )

                if triggered_flag is None and i != 0 and data[puntero] >= data[i]:
                    triggered_flag = [
                        AnimationGroup(
                            val.animate.set_color(val.get_color()),
                            focus.animate.set_color(focus.get_color()),
                        )
                        for (val, focus) in zip(
                            g_value[0 : i + 1], g_focused[0 : i + 1]
                        )
                    ]
                    self.play(
                        LaggedStart(
                            [
                                AnimationGroup(
                                    val.animate.set_color(BS381.CRIMSON),
                                    focus.animate.set_color(BS381.CRIMSON),
                                )
                                for (val, focus) in zip(
                                    reversed(g_value[0 : i + 1]),
                                    reversed(g_focused[0 : i + 1]),
                                )
                            ],
                            lag_ratio=0.6,
                        ),
                        run_time=0.5,
                    )
                    [val.set_color(BS381.CRIMSON) for val in g_value[0 : i + 1]]

                # region: Mostrar lista de pasos
                if data[puntero] < data[i]:
                    steps_list.append(Tex(f"D[{puntero}] $<$ D[{i}]\\; Sí").scale(0.7))
                else:
                    steps_list.append(
                        Tex(f"D[{puntero}] $\\ge$ D[{i}]\\; No").scale(0.5)
                    )
                if isinstance(vgroup_steps, VGroup):
                    self.remove(vgroup_steps)
                if len(steps_list) > 13:
                    steps_list.pop(0)
                vgroup_steps = VGroup(*steps_list)
                vgroup_steps.arrange(DOWN)
                vgroup_steps.align_to(
                    self.camera.frame.get_corner(UP + RIGHT), RIGHT + UP
                )
                [
                    inst.align_to(self.camera.frame.get_corner(UP + RIGHT), RIGHT)
                    for inst in vgroup_steps
                ]
                self.add(vgroup_steps)
                # endregion: Mostrar lista de pasos

                # **************************************************************************************************
                # TODO:Región que realiza la comparación lógica
                # **************************************************************************************************
                if data[puntero] < data[i]:
                    (data[puntero], data[i]) = (data[i], data[puntero])
                    
                    a = g_value[i]
                    b = g_value[puntero]
                    swapped_a = a.copy().move_to(b.get_center())
                    swapped_b = b.copy().move_to(a.get_center())
                    self.play(
                        AnimationGroup(
                            ClockwiseTransform(a, swapped_a, path_arc=PI / 2),
                            ClockwiseTransform(b, swapped_b, path_arc=PI),
                            arrow_and_label.animate.next_to(g_indexes[i], UP),
                        )
                    )
                    
                    g_value[i] = b
                    g_value[puntero] = a
                    puntero = i  # update pointer
                self.wait(0.10)
                self.remove(comparison[0], comparison[1])
            if triggered_flag is not None:
                self.play(
                    LaggedStart(*triggered_flag, lag_ratio=0.1),
                    run_time=1.2,
                )
            triggered_flag = None

            [val.set_color(WHITE) for val in g_value]
            self.wait(0.5)
            self.remove(step)
            if (cola_de_particion - 1) % 3 == 0 or len(steps_list) > 8:
                steps_list.clear()
                self.remove(vgroup_steps)
            vgroup_steps = None
        # print(data)
        self.wait(1)

    def draw_question__(self) -> Mobject | None:
        title = Tex("Ordenación por Inserción Directa")
        question = Tex("Pregunta Indagatoria:")
        q = Tex("¿Cuál es la complexidad espacial?")
        group = VGroup(title, question, q).arrange(DOWN).move_to(ORIGIN)

        self.play(Write(group), run_time=1)
        self.wait(1)
        self.play(
            AnimationGroup(
                q.animate.align_to(
                    self.camera.frame.get_corner(DOWN + RIGHT), DOWN + RIGHT
                ),
                FadeOut(title),
                FadeOut(question),
            )
        )
        return None

    def draw_vec(self):
        cell_value = self.to_sort_vec
        cell_value = [Text(str(i)) for i in cell_value]
        max_side = max([max(val.height, val.width) for val in cell_value])
        indexes = [Tex(str(i)) for i in range(len(cell_value))]

        def normal_rect() -> Rectangle:
            side = max_side * 1.2
            rect = Rectangle(WHITE, side, side)
            rect.set_color_by_gradient(BLUE_E, RED_E)
            return rect

        cell_highligther = [normal_rect().scale(1.2) for _ in range(len(cell_value))]
        cell_is_focused = [
            normal_rect().set_color(BLUE_D) for _ in range(len(cell_value))
        ]

        cell_value = VGroup(*cell_value)
        cell_highligther = VGroup(*cell_highligther)
        cell_is_focused = VGroup(*cell_is_focused)
        indexes = VGroup(*indexes)
        cell_highligther.arrange(RIGHT)
        cell_highligther.move_to(ORIGIN + LEFT * 2)
        # self.play(Write(cell_highligther))
        # return
        [
            (cell.move_to(ch.get_center()), val.move_to(ch.get_center()))
            for (ch, cell, val) in zip(cell_highligther, cell_is_focused, cell_value)
        ]
        [
            index.next_to(highlight, UP)
            for (index, highlight) in zip(indexes, cell_highligther)
        ]
        self.play(
            LaggedStart(
                [
                    AnimationGroup(Write(a), EmptyAnim(), Write(c))
                    for (a, _, c) in zip(cell_highligther, indexes, cell_value)
                ],
                Write(indexes),
                lag_ratio=0.4,
                run_time=3.0,
            ),
            # run_time=3,
        )
        self.indexes = indexes
        self.highligther_cell = cell_highligther
        self.highligther_focused = cell_is_focused
        self.tex_values = cell_value


InsercionDirecta().render(True)
