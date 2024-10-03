from manim import *
import numpy as np
import math as math
from typing import Callable, Sequence, Tuple


class MatSup_1(MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upper_bound = 1
        self.lower_bound = -1
        self.graph_dx = 0.01

        self.half_period = (self.upper_bound - self.lower_bound) / 2.0
        self.smoothing = True

    def f(self) -> Callable[[float], float]:

        # f = self.bounded(lambda x: x, self.upper_bound, self.lower_bound)
        f = self.bounded(lambda x: 1 + abs(x), self.upper_bound, self.lower_bound)
        # f = self.bounded(lambda x: np.sin(x), self.upper_bound, self.lower_bound)

        # f = self.bounded(lambda x: np.sin(x), self.upper_bound, self.lower_bound)
        return f

    @property
    def plane(self) -> NumberPlane:
        [lower_x, upper_x, *_] = self.graph_x_bounds
        [lower_y, upper_y, *_] = self.y_bounds
        return NumberPlane(
            x_range=[
                lower_x - self.period_size,
                upper_x + self.period_size,
            ],  # Displayed (smallest_x, largest_x, step)
            y_range=[-upper_y, upper_y, 1],
            # x_length=6,  # x_length * step
            # y_length=5,
            x_axis_config={
                "numbers_to_include": np.arange(
                    lower_x + self.half_period,
                    upper_x - self.half_period + 0.1,
                    1,
                )
            },  # (Inclusive Lower Bound, Exclusive Upper Bound, Step)
            y_axis_config={"numbers_to_include": np.arange(lower_y, upper_y, 1)},
            tips=True,
            background_line_style={
                "stroke_color": GRAY_BROWN,  # Change grid line color here
                "stroke_width": 1,  # Width of the grid lines
                "stroke_opacity": 0.5,  # Opacity of the grid lines
            },
        )

    @property
    def y_bounds(self) -> Sequence[float]:
        range = [
            self.f()(x)
            for x in np.arange(self.lower_bound, self.upper_bound, self.graph_dx)
        ]
        # print(range)
        _max = math.ceil(max(range) + 0.01)
        _min = math.floor(min(range) - 0.01)
        return [_min, _max, self.graph_dx]

    @property
    def graph_x_bounds(self) -> Sequence[float]:
        return [
            self.lower_bound - self.period_size - self.half_period,
            self.upper_bound + self.period_size + self.half_period,
            self.graph_dx,
        ]

    @property
    def period_size(self):
        return self.upper_bound - self.lower_bound

    def period_offset_by_T(self, n: int) -> Sequence[float]:
        return [
            self.lower_bound + n * self.period_size,
            self.upper_bound + n * self.period_size,
            self.graph_dx,
        ]

    def bounded(
        self, f: Callable[[float], float], upper_bound: float, lower_bound: float
    ):
        return lambda x: f(
            (x - lower_bound) % (upper_bound - lower_bound) + lower_bound
        )

    def labels(self, ax):
        labels = ax.get_axis_labels(x_label=Tex("$x$"), y_label=Tex("$y$"))
        return labels

    def construct(self):
        self.camera.frame.save_state()

        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{cancel}\usepackage{color}")

        #         # Update Frame to fit graph
        #         [x_0, x_1, *_] = self.graph_x_bounds
        #         print(x_0, x_1)
        #         config.frame_width = x_1 - x_0
        #         config.frame_height = config.frame_width / config.aspect_ratio
        #         self.camera.frame_height = config.frame_height
        #         self.camera.frame_width = config.frame_width
        config.frame_rate = 20
        #         self.camera.frame.save_state()
        ax = self.plane

        #         f = lambda x: self.f()(x)

        #         graph = ax.plot(
        #             f,
        #             color=BLUE,
        #             x_range=self.graph_x_bounds,
        #             use_smoothing=self.smoothing,
        #         )
        #         graph_in_period = gip = ax.plot(
        #             f,
        #             color=RED,
        #             x_range=[self.lower_bound, self.upper_bound, self.graph_dx],
        #             use_smoothing=self.smoothing,
        #         )
        #         graph_in_plus_1T = gipT = ax.plot(
        #             f,
        #             color=GREEN_E,
        #             x_range=self.period_offset_by_T(1),
        #             use_smoothing=self.smoothing,
        #         )
        #         graph_in_minus_1T = gimT = ax.plot(
        #             f,
        #             color=DARK_BROWN,
        #             x_range=self.period_offset_by_T(-1),
        #             use_smoothing=self.smoothing,
        #         )

        #         # create dots based on the graph
        #         moving_dot = Dot(ax.i2gp(gip.t_min, gip), color=ORANGE)
        #         dot_1 = Dot(ax.i2gp(gip.t_min, gip), color=PURPLE_E)
        #         dot_2 = Dot(ax.i2gp(gip.t_max, gip), color=PURPLE_E)
        #         dot_m = dot_in_half_step = Dot(
        #             ax.i2gp((gip.t_max + gip.t_min) / 2, gip), color=BLUE_E
        #         )

        #         def update_curve(mob):
        #             mob.move_to(moving_dot.get_center())

        #         equation = MathTex("f(x) = 1 + |x|").move_to([-2, -1, 0])
        #         labels = self.labels(ax)
        #         # Add the Axes
        #         self.add(ax)
        #         # Draw the Equation
        #         self.play(Write(equation))
        #         # Draw the graph's components
        #         for i in [
        #             labels,
        #             graph,
        #             graph_in_period,
        #             # dot_m,
        #             dot_1,
        #             # dot_2,
        #             gimT,
        #             # gipT,
        #         ]:
        #             if i is dot_1:
        #                 self.play(LaggedStart(Write(dot_1), Write(dot_2)))
        #                 continue
        #             if i is gimT:
        #                 # Draw the Dot in Half-T
        #                 self.play(Write(dot_m))
        #                 # Write f(x - T) and f(x + T)
        #                 self.play(
        #                     LaggedStart(
        #                         Write(gimT, running_start=0.25, rate_func=linear), Write(gipT)
        #                     ),
        #                     run_time=3,
        #                 )
        #                 continue
        #             self.play(Write(i))
        #         self.wait(0.25)
        #         # Voltear gipT de maneral horizontal
        #         # self.play(gipT.animate.rotate_about_origin(PI, Y_AXIS))
        #         self.play(gipT.animate.rotate(PI, Y_AXIS, about_point=ax.get_origin()))
        #         # Pan in to the graph
        #         self.play(self.camera.frame.animate.scale(0.9).move_to(moving_dot))
        #         self.camera.frame.add_updater(update_curve)
        #         self.play(
        #             MoveAlongPath(moving_dot, graph_in_period, rate_func=linear),
        #             run_time=1,
        #         )
        #         self.camera.frame.remove_updater(update_curve)

        #         # Pan Out to center
        #         self.play(self.camera.frame.animate.scale(1.2).move_to(gip.get_center()))
        #         # Remove F(x - T) and F(x + T)
        #         self.play(FadeOut(gimT), FadeOut(gipT))
        #         # Recolor the grap in the period
        #         self.play(gip.animate.set_color(GOLD))

        #         # Define a shift by half period
        #         shift = self.half_period
        #         shifted_f = lambda x: f(x + shift)
        #         shifted_graph = ax.plot(
        #             shifted_f,
        #             color=GREY,
        #             x_range=[graph.t_min + shift, graph.t_max + shift, self.graph_dx],
        #             use_smoothing=self.smoothing,
        #         )
        #         shifted_gip = ax.plot(
        #             shifted_f,
        #             color=GOLD,
        #             x_range=[gip.t_min + shift, gip.t_max + shift, self.graph_dx],
        #             use_smoothing=self.smoothing,
        #         )

        #         self.bring_to_front(gip)
        #         self.play(
        #             AnimationGroup(
        #                 ReplacementTransform(graph.copy(), shifted_graph),
        #                 ReplacementTransform(gip, shifted_gip),
        #             ),
        #             run_time=2,
        #         )
        #         self.bring_to_front(shifted_gip)
        #         self.play(Restore(self.camera.frame))

        #         self.wait(0.5)
        #         # Vertical Flip
        #         self.play(shifted_graph.animate.rotate(PI, X_AXIS, about_point=ax.get_origin()))
        #         self.wait(0.5)  # 0.5 seconds

        #         # Borrar elementos innecesarios
        #         self.play([FadeOut(x) for x in [dot_1, dot_2, dot_m, moving_dot]])
        #         del dot_1, dot_2, dot_m, moving_dot

        #         # Dibujar area bajo las curvas
        #         area_1 = ax.get_area(graph, [0, 1], opacity=0.5)
        #         area_2 = ax.get_area(shifted_graph, [0, 1], opacity=0.5)

        #         self.play(AnimationGroup(Write(area_1), Write(area_2)))

        #         def equation_updater(obj: MathTex):
        #             """Update's the equation's constant based on the graph's center"""
        #             new_constant = graph.get_center()[1] - 0.5
        #             new_obj = MathTex(r"f(x) = ", f"{new_constant:.3f}", " + |x|").set_color(
        #                 WHITE
        #             )
        #             new_obj[1].set_color_by_gradient(DARK_BLUE, RED_D)
        #             new_corner = new_obj.get_corner(DOWN + LEFT)
        #             old_corner = obj.get_corner(DOWN + LEFT)
        #             new_center = new_obj.get_center()
        #             new_center[0] += old_corner[0] - new_corner[0]
        #             new_center[1] += old_corner[1] - new_corner[1]
        #             new_obj.move_to(new_center)
        #             # Update the equation's LaTeX with the new constant (formatting to 3 decimal places)
        #             obj.become(new_obj)

        #         def a_0_updater(obj: MathTex):
        #             new_constant = graph.get_center()[1]
        #             if new_constant <= 0:
        #                 new_constant = 0
        #             new_obj = MathTex(
        #                 f"a_0 ", "=", f"{new_constant:.3f}"
        #             ).set_color_by_gradient(RED_A, PURE_RED)
        #             new_obj[0].set_color(RED_A)
        #             new_obj[2].set_color(PURE_RED)
        #             new_corner = new_obj.get_corner(DOWN + LEFT)
        #             old_corner = obj.get_corner(DOWN + LEFT)
        #             new_center = new_obj.get_center()
        #             new_center[0] += old_corner[0] - new_corner[0]
        #             new_center[1] += old_corner[1] - new_corner[1]
        #             new_obj.move_to(new_center)
        #             obj.become(new_obj)

        #         ##### Mostrar el comportamiento de a_0 a medida que desfasas la gráfica #####

        #         # Reduce Areas to fit shifted graph
        #         reduced_area_1 = ax.get_area(
        #             graph.copy().shift(DOWN * 1.5),
        #             [0, 1],
        #             opacity=0.5,
        #             color=(PURPLE_E, TEAL_A),
        #         )
        #         reduced_area_2 = ax.get_area(
        #             shifted_graph.copy().shift(UP * 1.5),
        #             [0, 1],
        #             opacity=0.5,
        #             color=(PURPLE_E, TEAL_A),
        #         )
        #         # Animate the shift
        #         equation.set_color(WHITE)
        #         # TODO: re-add updater
        #         # equation.add_updater(equation_updater)

        #         a_0 = (
        #             MathTex(r"a_{0} ", "=", "1.5")
        #             .move_to(equation.get_center())
        #             .set_color_by_gradient(RED_A, PURE_RED)
        #         )
        #         a_0[0].set_color(RED_A)
        #         a_0[2].set_color(PURE_RED)
        #         self.play(
        #             FadeIn(a_0),
        #             a_0.animate.shift(UP * 2),
        #         )

        #         # TODO: Re-add updater
        #         # a_0.add_updater(a_0_updater)
        #         self.play(
        #             AnimationGroup(
        #                 shifted_graph.animate.shift(UP * 1.5),
        #                 graph.animate.shift(DOWN * 1.5),
        #                 shifted_gip.animate.shift(DOWN * 1.5),
        #                 area_1.animate.become(reduced_area_1),
        #                 area_2.animate.become(reduced_area_2),
        #             ),
        #             run_time=2,
        #         )

        #         self.wait(1)

        #         ## YEET a_0
        #         self.play(
        #             AnimationGroup(
        #                 FadeOut(shifted_gip),
        #                 a_0.animate.shift(RIGHT * 50),
        #             )
        #         )
        #         # Small Cleanup and variable updating
        #         [area_1, area_2] = [reduced_area_1, reduced_area_2]
        #         del reduced_area_1, reduced_area_2, shifted_gip
        #         self.wait(0.5)

        #         # Create a copy to shift by balf period, and vertically flip
        #         copy_of_shifted_graph = shifted_graph.copy()
        #         ## Shift by half period to left
        #         self.play(
        #             copy_of_shifted_graph.animate.shift(
        #                 LEFT * self.half_period
        #             ).set_color_by_gradient(PURPLE_D, TEAL_A)
        #         )
        #         ## Vertical Flip
        #         self.play(
        #             copy_of_shifted_graph.animate.rotate(
        #                 PI, X_AXIS, about_point=ax.get_origin()
        #             )
        #         )
        #         ## undraw the object
        #         self.play(FadeOut(graph))
        #         ## cleanup
        #         graph = copy_of_shifted_graph
        #         del copy_of_shifted_graph

        #         self.wait(0.5)

        #         # Display the equation for the shifted graph
        transformed_eq = (
            MathTex(
                r"f(t)=\begin{cases}\
        -t -0.5 & \text{si } -1\leq t\leq 0 \\\
        t  -0.5 & \text{si } 0\leq t\leq 1 \
        \end{cases}; t=[-1,1]",
            )
            # .move_to(equation.get_center() + UP * 3) # TODO: remove comment
            .set_color_by_gradient(PURPLE_E, TEAL_A)
        )
        transformed_eq[0][20:32].set_color_by_gradient(LIGHT_PINK, RED_E)
        self.add(transformed_eq)

        # TODO UNCOMMENT THIS BLOCK ABOVE
        context_text = Tex(
            "La función es 1/4 de onda (Par)", color=TEAL_E
        ).set_color_by_gradient(PURPLE_E, TEAL_A)
        context_text.width = 8
        CAMERA_SW_CORNER = [-8.5, -4.0, 0.0]
        # TODO UNCOMMEN THIS BLOCK BELOW
        # background: List[VMobject] = [
        #     ax,
        #     area_1,
        #     area_2,
        #     labels,
        # ]  # Mark for opacity reduction
        # # Esquina inferior para colocar el texto de contexto
        # # Animar cambio de contexto (Fondo más transparente etc)
        # self.play(
        #     AnimationGroup(
        #         Write(context_text),
        #         ReplacementTransform(equation, transformed_eq),
        #         FadeOut(shifted_graph),
        #         self.camera.frame.animate.set_width(ax.c2p(9, 9) - ax.c2p(-9, -9)),
        #         # reducir la opacidad de los elementos del fondo
        #         graph.animate.set_stroke(BLUE, opacity=0.2),
        #         *[x.animate.set_opacity(0.2) for x in background],
        #     )
        # )
        # # Agregar la gráfica principal a la lista de elementos del fondo
        # background.append(graph)

        # Mover la descripción a la esquina inferior izquierda
        self.play(
            # TODO: Remove camera zoom animation
            self.camera.frame.animate.set_width(ax.c2p(9, 9) - ax.c2p(-9, -9)),
            context_text.animate.move_to(
                CAMERA_SW_CORNER - context_text.get_corner(DOWN + LEFT)
            ),
        )

        # _Helper function to generate math equations
        custom_mathtex = lambda tex: (
            MathTex(*tex, tex_template=tex_template, color=LIGHT_BROWN)
        )
        # Write solution

        solution1 = custom_mathtex(
            [r"A_{n}=\frac{1}{2\cdot T}\cdot{2}\int_{0}^{T/2}{(1+t)\cos(n\omega t)dt}"]
        )
        context = [context_text]

        def with_context(string: str, context: List[Tex]) -> TransformMatchingShapes:
            tex = Tex(string).set_color_by_gradient(PURPLE_E, TEAL_A)
            tex.move_to(CAMERA_SW_CORNER - tex.get_corner(DOWN + LEFT))
            transform = TransformMatchingShapes(context[0], tex)
            context[0] = tex
            return transform

        replaced_val_color = DARK_BLUE
        solution_steps: Tuple[str, List[str] | str, list[ManimColor | None] | None] = [
            (
                "$f(x)=|x| - 0.5$",
                r"f(x)=|x| - 0.5 \text{ tiene simetria par y media onda}",
                None,
            ),
            (
                "Calculando para Simetría Par y Media Onda",
                r"\begin{aligned}\
a_{n}= & \frac{8}{T}\int^{T/4}_{0}{f(t) \cdot \sin(n \omega t)}dt\\\
b_{n}= & 0 \text{ (Por ser simetría par)}\
\end{aligned}",
                None,
            ),
            (
                "Resolviendo para $a_{n}$",
                r"a_{n}= \frac{8}{T}\int^{T/4}_{0}{f(t) \cdot \sin(n \omega t)}dt",
                None,
            ),
            (
                "Reemplazando $f(t)$",
                r"a_{n}= \frac{8}{T}\int^{T/4}_{0}{\cancelto{ t - \frac{1}{2} }{ f(t) } \cdot \cos(n \omega t)}dt",
                None,
            ),
            (
                "Reemplazando T",
                [
                    r"a_{n}= \frac{8}{\cancelto{ 2 }{",
                    " T ",
                    r"}}\int^{\cancelto{ 1/2 }{ \frac{T}{4} } }",
                    r"_{0}{\left( t-\frac{1}{2} \right) \cos\left( n ",
                    r"\cancelto{ \frac{2\pi}{2} }{\omega }",
                    r" t \right)}dt",
                ],
                [
                    None,
                    replaced_val_color,
                    replaced_val_color,
                    None,
                    replaced_val_color,
                    None,
                ],
            ), # TODO : CONTINUE HERE
            # ("", r"", None),
            # ("", r"", None),
            # ("", r"", None),
            # ("", r"", None),
            # ("", r"", None),
            # ("", r"", None),
            # ("", r"", None),
            # ("", r"", None),
        ]
        to_drop = None
        to_shift_again = None
        last_solution = transformed_eq

        for idx, (desc, step, colors) in enumerate(solution_steps):
            print("index:", idx)

            print(f"{idx}-)description:", desc)
            print("list type:", type(step))
            if isinstance(step, list):
                print(f"{idx}-)step is List")
                step = custom_mathtex([*step])
            else:
                print(f"{idx}-)step is not List")
                step = custom_mathtex([step])
            print(f"{idx}-)Parse description:", desc)
            desc = with_context(desc, context)
            # Position step just above x axis
            step_sw_corner = step.get_corner(DOWN + LEFT)
            # Get center point because .move_to() moves the center of the object
            step_center = step.get_center()
            step_center[1] = 0 - step_sw_corner[1]

            step.move_to(step_center)
            if colors is not None:
                for i, color in enumerate(colors):
                    if color is not None:
                        step[i].set_color(color)
            animation_list = []
            if to_shift_again is not None:
                center = to_shift_again.get_center()
                center[1] = (
                    last_solution.height
                    + step.height
                    + to_shift_again.height * 0.5
                    + 0.4
                )
                animation_list.append(
                    to_shift_again.animate.move_to(center).set_opacity(0.5)
                )
                if to_drop is not None:
                    animation_list.append(to_drop.animate.shift(UP * 2))
                    animation_list.append(FadeOut(to_drop))
                to_drop = to_shift_again
            to_shift_again = last_solution

            self.play(
                AnimationGroup(
                    last_solution.animate.next_to(step, UP),
                    TransformMatchingShapes(last_solution.copy(), step),
                    desc,
                    *animation_list,
                    run_time=2,
                ),
            )
            self.wait(0.5)
            last_solution = step
        self.wait(1)
        return  # Early return
        self.play(
            AnimationGroup(Write(solution1), with_context("Hello World", context))
        )

        solution2 = custom_mathtex(
            r"A_{n}=\frac{1}{2}\int_{0}^{T/2}{\left(\cos(n\omega t)+t\cos(n\omega t)\right)dt}"
        ).next_to(solution1, DOWN)
        self.play(
            AnimationGroup(
                ReplacementTransform(solution1.copy(), solution2),
                transformed_eq.animate.shift(UP * 2),
                with_context("Hola mundo 2", context),
            )
        )

        solution3 = MathTex(
            r"A_{n}=\frac{1}{2} \left[\frac{\sin(n \pi t)}{n\pi}+\frac{t}{n\pi}\sin(n\pi t)+\frac{1}{(n\pi)^{2}}\cos(n\pi t)\right]_{0}^{1} "
        ).set_color(BLUE_E)
        self.play(
            AnimationGroup(
                solution2.animate.shift(UP * 2),
                ReplacementTransform(solution2.copy(), solution3),
                solution1.animate.shift(UP * 2),
            )
        )

        solution4 = MathTex(
            r"A_{n}=\frac{1}{2}\left[ \cancelto{ 0 }{ {\frac{\sin(n\pi)}{2\pi}}}+ \cancelto{ 0 }{ \frac{1}{n\pi}\sin(n\pi) }+\frac{1}{(n\pi)^{2}}\cancelto{ (-1)^n }{ \cos(n\pi) }-\cancelto{ 0 }{ \frac{\sin(0)}{n\pi}-\frac{0}{n\pi} }-\frac{1}{(k\pi)^{2}}\right] ",
            tex_template=tex_template,
        ).set_color(BLUE_E)
        self.wait()

        self.play(
            AnimationGroup(
                solution3.animate.shift(UP * 2),
                ReplacementTransform(solution3.copy(), solution4),
                solution2.animate.shift(UP * 2),
            )
        )

        self.wait()


def render():
    MatSup_1().render(preview=True)


render()
print("Done!\n")
