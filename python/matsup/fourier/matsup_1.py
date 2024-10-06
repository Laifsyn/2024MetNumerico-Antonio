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
        self.replaced_val_color = RED_E

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

        # Update Frame to fit graph
        [x_0, x_1, *_] = self.graph_x_bounds
        config.frame_width = x_1 - x_0
        config.frame_height = config.frame_width / config.aspect_ratio
        self.camera.frame_height = config.frame_height
        self.camera.frame_width = config.frame_width
        config.frame_rate = 60
        self.camera.frame.save_state()
        ax = self.plane

        f = lambda x: self.f()(x)

        graph = ax.plot(
            f,
            color=BLUE,
            x_range=self.graph_x_bounds,
            use_smoothing=self.smoothing,
        )
        graph_in_period = gip = ax.plot(
            f,
            color=RED,
            x_range=[self.lower_bound, self.upper_bound, self.graph_dx],
            use_smoothing=self.smoothing,
        )
        graph_in_plus_1T = gipT = ax.plot(
            f,
            color=GREEN_E,
            x_range=self.period_offset_by_T(1),
            use_smoothing=self.smoothing,
        )
        graph_in_minus_1T = gimT = ax.plot(
            f,
            color=DARK_BROWN,
            x_range=self.period_offset_by_T(-1),
            use_smoothing=self.smoothing,
        )

        # create dots based on the graph
        moving_dot = Dot(ax.i2gp(gip.t_min, gip), color=ORANGE)
        dot_1 = Dot(ax.i2gp(gip.t_min, gip), color=PURPLE_E)
        dot_2 = Dot(ax.i2gp(gip.t_max, gip), color=PURPLE_E)
        dot_m = dot_in_half_step = Dot(
            ax.i2gp((gip.t_max + gip.t_min) / 2, gip), color=BLUE_E
        )

        def update_curve(mob):
            mob.move_to(moving_dot.get_center())

        equation = MathTex("f(x) = 1 + |x|").move_to([-2, -1, 0])
        labels = self.labels(ax)
        # Add the Axes
        self.add(ax)
        # Draw the Equation
        self.play(Write(equation))
        # Draw the graph's components
        for i in [
            labels,
            graph,
            graph_in_period,
            # dot_m,
            dot_1,
            # dot_2,
            gimT,
            # gipT,
        ]:
            if i is dot_1:
                self.play(LaggedStart(Write(dot_1), Write(dot_2)))
                continue
            if i is gimT:
                # Draw the Dot in Half-T
                self.play(Write(dot_m))
                # Write f(x - T) and f(x + T)
                self.play(
                    LaggedStart(
                        Write(gimT, running_start=0.25, rate_func=linear), Write(gipT)
                    ),
                    run_time=3,
                )
                continue
            self.play(Write(i))
        self.wait(0.25)
        # Voltear gipT de maneral horizontal
        # self.play(gipT.animate.rotate_about_origin(PI, Y_AXIS))
        self.play(gipT.animate.rotate(PI, Y_AXIS, about_point=ax.get_origin()))
        # Pan in to the graph
        self.play(self.camera.frame.animate.scale(0.9).move_to(moving_dot))

        self.camera.frame.add_updater(update_curve)
        self.play(
            MoveAlongPath(moving_dot, graph_in_period, rate_func=linear),
            run_time=1,
        )
        self.camera.frame.remove_updater(update_curve)

        # Pan Out to center
        self.play(self.camera.frame.animate.scale(1.2).move_to(gip.get_center()))
        # Remove F(x - T) and F(x + T)
        self.play(FadeOut(gimT), FadeOut(gipT))
        # Recolor the grap in the period
        self.play(gip.animate.set_color(GOLD))

        # Define a shift by half period
        shift = self.half_period
        shifted_f = lambda x: f(x + shift)
        shifted_graph = ax.plot(
            shifted_f,
            color=GREY,
            x_range=[graph.t_min + shift, graph.t_max + shift, self.graph_dx],
            use_smoothing=self.smoothing,
        )
        shifted_gip = ax.plot(
            shifted_f,
            color=GOLD,
            x_range=[gip.t_min + shift, gip.t_max + shift, self.graph_dx],
            use_smoothing=self.smoothing,
        )

        self.bring_to_front(gip)
        self.play(
            AnimationGroup(
                ReplacementTransform(graph.copy(), shifted_graph),
                ReplacementTransform(gip, shifted_gip),
            ),
            run_time=2,
        )
        self.bring_to_front(shifted_gip)
        self.play(Restore(self.camera.frame))

        self.wait(0.5)
        # Vertical Flip
        self.play(shifted_graph.animate.rotate(PI, X_AXIS, about_point=ax.get_origin()))
        self.wait(0.5)  # 0.5 seconds

        # Borrar elementos innecesarios
        self.play([FadeOut(x) for x in [dot_1, dot_2, dot_m, moving_dot]])
        del dot_1, dot_2, dot_m, moving_dot

        # Dibujar area bajo las curvas
        area_1 = ax.get_area(graph, [0, 1], opacity=0.5)
        area_2 = ax.get_area(shifted_graph, [0, 1], opacity=0.5)

        self.play(AnimationGroup(Write(area_1), Write(area_2)))

        def equation_updater(obj: MathTex):
            """Update's the equation's constant based on the graph's center"""
            new_constant = graph.get_center()[1] - 0.5
            new_obj = MathTex(r"f(x) = ", f"{new_constant:.3f}", " + |x|").set_color(
                WHITE
            )
            new_obj[1].set_color_by_gradient(DARK_BLUE, RED_D)
            new_corner = new_obj.get_corner(DOWN + LEFT)
            old_corner = obj.get_corner(DOWN + LEFT)
            new_center = new_obj.get_center()
            new_center[0] += old_corner[0] - new_corner[0]
            new_center[1] += old_corner[1] - new_corner[1]
            new_obj.move_to(new_center)
            # Update the equation's LaTeX with the new constant (formatting to 3 decimal places)
            obj.become(new_obj)

        def a_0_updater(obj: MathTex):
            new_constant = graph.get_center()[1]
            if new_constant <= 0:
                new_constant = 0
            new_obj = MathTex(
                f"a_0 ", "=", f"{new_constant:.3f}"
            ).set_color_by_gradient(RED_A, PURE_RED)
            new_obj[0].set_color(RED_A)
            new_obj[2].set_color(PURE_RED)
            new_corner = new_obj.get_corner(DOWN + LEFT)
            old_corner = obj.get_corner(DOWN + LEFT)
            new_center = new_obj.get_center()
            new_center[0] += old_corner[0] - new_corner[0]
            new_center[1] += old_corner[1] - new_corner[1]
            new_obj.move_to(new_center)
            obj.become(new_obj)

        ##### Mostrar el comportamiento de a_0 a medida que desfasas la gráfica #####

        # Reduce Areas to fit shifted graph
        reduced_area_1 = ax.get_area(
            graph.copy().shift(DOWN * 1.5),
            [0, 1],
            opacity=0.5,
            color=(PURPLE_E, TEAL_A),
        )
        reduced_area_2 = ax.get_area(
            shifted_graph.copy().shift(UP * 1.5),
            [0, 1],
            opacity=0.5,
            color=(PURPLE_E, TEAL_A),
        )
        # Animate the shift
        equation.set_color(WHITE)

        equation.add_updater(equation_updater)

        a_0 = (
            MathTex(r"a_{0} ", "=", "1.5")
            .move_to(equation.get_center())
            .set_color_by_gradient(RED_A, PINK)
        )
        a_0[0].set_color(RED_A)
        a_0[2].set_color(PINK)
        self.play(
            FadeIn(a_0),
            a_0.animate.shift(UP * 2),
        )

        a_0.add_updater(a_0_updater)
        self.play(
            AnimationGroup(
                shifted_graph.animate.shift(UP * 1.5),
                graph.animate.shift(DOWN * 1.5),
                shifted_gip.animate.shift(DOWN * 1.5),
                area_1.animate.become(reduced_area_1),
                area_2.animate.become(reduced_area_2),
            ),
            run_time=2,
        )

        self.wait(0.4)

        ## YEET a_0
        self.play(
            AnimationGroup(
                FadeOut(shifted_gip),
                FadeOut(area_2),
                a_0.animate.shift(RIGHT * 50),
            )
        )
        # Small Cleanup and variable updating

        self.remove(area_2)
        del reduced_area_1, reduced_area_2, shifted_gip, area_2
        self.wait(0.5)

        # Create a copy to shift by balf period, and vertically flip
        copy_of_shifted_graph = shifted_graph.copy()
        ## Shift by half period to left
        self.play(
            copy_of_shifted_graph.animate.shift(
                LEFT * self.half_period
            ).set_color_by_gradient(PURPLE_D, TEAL_A)
        )
        ## Vertical Flip
        self.play(
            copy_of_shifted_graph.animate.rotate(
                PI, X_AXIS, about_point=ax.get_origin()
            )
        )
        ## undraw the object
        self.play(FadeOut(graph))
        ## cleanup
        graph = copy_of_shifted_graph
        del copy_of_shifted_graph

        self.wait(0.5)

        # Display the equation for the shifted graph
        transformed_eq = MathTex(
            r"f(t)=\begin{cases}\
        -t -0.5 & \text{si } -1\leq t\leq 0 \\\
        t  -0.5 & \text{si } 0\leq t\leq 1 \
        \end{cases}; t=[-1,1]",
        ).set_color_by_gradient(PURPLE_E, TEAL_A)
        transformed_eq[0][20:32].set_color_by_gradient(LIGHT_PINK, RED_E)

        context_text = (
            Tex("Tiene simetría $1/4$ de onda (Par)", color=TEAL_E)
            .set_color_by_gradient(PURPLE_E, TEAL_A)
            .next_to(transformed_eq, DOWN)
        )
        context_text.width = 8
        CAMERA_SW_CORNER = [-8.5, -4.0, 0.0]
        background: List[VMobject] = [
            ax,
            area_1,
            labels,
        ]  # Mark for opacity reduction
        # Esquina inferior para colocar el texto de contexto
        # Animar cambio de contexto (Fondo más transparente etc)
        self.play(
            AnimationGroup(
                Write(context_text),
                ReplacementTransform(equation, transformed_eq),
                FadeOut(shifted_graph),
                self.camera.frame.animate.set_width(ax.c2p(9, 9) - ax.c2p(-9, -9)),
                # reducir la opacidad de los elementos del fondo
                graph.animate.set_stroke(BLUE, opacity=0.2),
                *[x.animate.set_opacity(0.2) for x in [*background]],
                run_time=1.5,
            )
        )

        # Mover la descripción a la esquina inferior izquierda
        self.play(
            context_text.animate.move_to(
                CAMERA_SW_CORNER - context_text.get_corner(DOWN + LEFT)
            ),
        )

        # _Helper function to generate math equations
        custom_mathtex = lambda tex: (
            MathTex(*tex, tex_template=tex_template, color=LIGHT_BROWN)
        )

        solution1 = custom_mathtex(
            [r"A_{n}=\frac{1}{2\cdot T}\cdot{2}\int_{0}^{T/2}{(1+t)\cos(n\omega t)dt}"]
        )
        context = [context_text]

        def with_context(string: str, context: List[Tex]) -> TransformMatchingShapes:
            tex = Tex(string).set_color_by_gradient(PURPLE_E, TEAL_A)
            tex.align_to(context[0], DOWN + LEFT)
            transform = TransformMatchingShapes(context[0], tex)
            context[0] = tex
            return transform

        replaced_val_color = self.replaced_val_color
        solution_steps: Tuple[str, List[str] | str, list[ManimColor | None] | None] = [
            (
                "$f(x)=|x| - 0.5$",
                r"f(x)=|x| - 0.5 \text{ tiene simetria par y media onda}",
                None,
            ),
            (
                "Calculando para Simetría Par y Media Onda",
                r"\begin{aligned}\
a_{n}= & \frac{8}{T}\int^{T/4}_{0}{f(t) \cdot \cos(n \omega t)}dt\\\
b_{n}= & 0 \text{ (Por ser simetría par)}\
\end{aligned}",
                None,
            ),
            (
                "Resolviendo para $a_{n}$",
                r"a_{n}= \frac{8}{T}\int^{T/4}_{0}{f(t) \cdot \cos(n \omega t)}dt",
                None,
            ),
            (
                "Reemplazando $f(t)$",
                r"a_{n}= \frac{8}{T}\int^{T/4}_{0}{\cancelto{ t - \frac{1}{2} }{ f(t) } \cdot \cos(n \omega t)}dt",
                None,
            ),
            (
                "Reemplazando $T = 2$",
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
            ),
            (
                "Se simplifica y separa la expresión",
                r"a_{n}= 4\int^{1/2}_{0}{t \cdot \cos\left( n \pi t \right)}dt + 4\int^{1/2}_{0}{-\frac{1}{2} \cdot \cos\left( n \pi t \right)}dt",
                None,
            ),
            (
                "Se hace Integración por parte e identidad",
                [
                    r"a_{n}= 4 \left[ ",
                    r"\frac{t}{n\pi}\sin(n\pi t) + \frac{1}{(n\pi)^{2}}\cos(n\pi t)",
                    r"\ -\ ",
                    r"\frac{1}{2n\pi}\sin(n\pi t) ",
                    r"\right]^{1/2}_{0}",
                ],
                [None, replaced_val_color, None, MAROON_D, None],
            ),
            (
                "Se factoriza el seno",
                [
                    r"a_{n}= 4 \left[ ",
                    r"\frac{t}{n\pi}\sin(n\pi t)\left( t-\frac{1}{2} \right) ",
                    r"+ \frac{1}{(n\pi)^{2}}\cos(n\pi t) \right]^{1/2}_{0}",
                ],
                [None, replaced_val_color, None],
            ),
            (
                "Se valúa el intervalo de la Integral",
                [
                    r"a_{n}= 4 \left[ ",
                    r"\xcancel{\frac{t}{n\pi}\sin(n\pi t)}\cancelto{ 0 }{ \left( t-\frac{1}{2} \right) }",
                    r" + \frac{1}{(n\pi)^{2}}\cos\left( \frac{n\pi}{2} \right) ",
                    r" - \cancelto{ 0 }{ \frac{0}{n\pi}\sin(n\pi t) }",
                    r" -\frac{1}{(n\pi)^{2}}",
                    r"\cancelto{ 1 }{ \cos( n\pi \cdot 0 ) }",
                    r"\right]",
                ],
                [
                    None,
                    replaced_val_color,
                    None,
                    replaced_val_color,
                    None,
                    replaced_val_color,
                    None,
                ],
            ),
            (
                "Se Reducen los términos",
                r"a_{n}= 4 \left[\
            \frac{1}{(n\pi)^{2}}\cos\left( \frac{n\pi}{2} \right) -\
            \frac{1}{(n\pi)^{2}}\
            \right]",
                None,
            ),
            (
                "Factorizar los términos",
                [
                    r"a_{n}=  ",
                    r"\frac{4}{(n\pi)^{2}}\left( ",
                    r"\cos\left( \frac{n\pi}{2} \right) - 1 ",
                    r"\right)",
                ],
                [None, None, replaced_val_color, None],
            ),
            (
                "Traer la serie de Fourier",
                r"\begin{aligned}\
                &f(t)=\frac{1}{2}a_{0}+\
                \sum^{\infty}_{n=1}a_{n}\cos(n\omega t)+\
                \xcancel{\sum^{\infty}_{n=1}b_{n}\sin(n\omega t)} \\ \
                &a_{n}=\frac{4}{(n\pi)^{2}}\left( \cos\left( \frac{n\pi}{2} \right) - 1 \right)\
            \end{aligned}",
                None,
            ),
            (
                "Reemplazamos $a_{n}$",
                [
                    r"f(t)=",
                    r"\frac{1}{2}a_{0}",
                    r"+\sum^{\infty}_{n=1}",
                    r"\frac{4}{(n\pi)^{2}}\left( \cos\left( \frac{n\pi}{2} \right) - 1 \right)",
                    r"\cos(n\pi t)",
                ],
                [None, PINK, None, replaced_val_color, None],
            ),
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
            # Colorear los elementos de la ecuació
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
            copied_last_solution = last_solution.copy().set_opacity(0).shift(UP * 0.5)
            to_shift_again = copied_last_solution
            self.play(
                LaggedStart(
                    desc,
                    AnimationGroup(
                        *animation_list,
                        copied_last_solution.animate.next_to(step, UP).set_opacity(0.7),
                        # TODO: Consider using write the step instead of transform
                        ReplacementTransform(last_solution, step),
                        # FadeOut(last_solution),
                        # Write(step),
                    ),
                    lag_ratio=0.4,
                    run_time=2,
                ),
            )
            self.wait(0.35)
            last_solution = step
        else:
            self.play([FadeOut(x) for x in [to_drop, to_shift_again]])
            del to_drop, to_shift_again, solution_steps

        self.wait(0.2)

        harmonic_equation = (
            custom_mathtex(
                [
                    r"f(t)=",
                    r"0.000",
                    r"+\sum^{\infty}_{n=1}",
                    r"\frac{4}{(n\pi)^{2}}\left( \cos\left( \frac{n\pi}{2} \right) - 1 \right)",
                    r"\cos(n\pi t)",
                ]
            )
            .next_to(context[0], UP)
            .align_to(context_text, LEFT)
        )
        harmonic_equation[1].set_color(PINK)
        harmonic_equation[3].set_color(self.replaced_val_color)
        expanded_area = ax.get_area(
            graph.copy(), [-4, 4], opacity=0.5, color=(PURPLE_E, TEAL_A)
        )
        self.play(
            AnimationGroup(
                [x.animate.set_opacity(1.0) for x in background],
                ReplacementTransform(last_solution, harmonic_equation),
                FadeOut(area_1),
                with_context(
                    "Incrementar $a_0$ por lo que se le había restado", context
                ),
                area_1.animate.become(expanded_area),
                graph.animate.set_stroke(RED, opacity=1.0),
                run_time=2,
            )
        )
        self.remove(area_1)
        area_1 = expanded_area
        del expanded_area

        def harmonic_updater(this: MathTex):
            const = graph.get_center()[1]
            latex_content = [
                r"f(t)=",
                f"{const:.3f}",
                r"+\sum^{\infty}_{n=1}",
                r"\frac{4}{(n\pi)^{2}}\left( \cos\left( \frac{n\pi}{2} \right) - 1 \right)",
                r"\cos(n\pi t)",
            ]
            new_obj = custom_mathtex(latex_content).align_to(this, LEFT + DOWN)
            new_obj[1].set_color(PINK)
            new_obj[3].set_color(self.replaced_val_color)
            this.become(new_obj)

        harmonic_equation.add_updater(harmonic_updater)

        expanded_area = ax.get_area(
            graph.copy().shift(UP * 1.5),
            [-4, 4],
            opacity=0.7,
            color=(PURE_BLUE, TEAL_A),
        )
        self.bring_to_front(graph)
        self.play(
            AnimationGroup(
                graph.animate(rate_func=rate_functions.ease_in_out_quint).shift(
                    UP * 1.5
                ),
                ReplacementTransform(area_1, expanded_area),
                run_time=2,
            )
        )
        harmonic_equation.remove_updater(harmonic_updater)
        self.bring_to_front(graph)
        self.wait(0.5)
        self.play(
            AnimationGroup([FadeOut(x) for x in [expanded_area, graph]]), run_time=1.5
        )

        area_1 = expanded_area
        del expanded_area
        fourier_n = ValueTracker(0)

        # Display the Fourier Transformation formation
        def fourier_function(x: float) -> float:
            a_0 = 1.5  # Ya se determinó anteriormente que a_0 vale 1.5
            result = a_0
            n_size = round(fourier_n.get_value())
            for n in range(1, n_size + 1):
                quotient = 4 / (((2 * n - 1) * np.pi) ** 2)
                result += (
                    quotient
                    * (np.cos((2 * n - 1) * np.pi / 2) - 1)
                    * np.cos((2 * n - 1) * np.pi * x)
                )
            return result

        def harmonic_repr_updater(old: MathTex) -> Tuple[MathTex, MathTex]:
            n_size = round(fourier_n.get_value())
            new = custom_mathtex(
                [
                    r"f(t)=",
                    r"1.500",
                    f"+\\sum^{{{n_size}}}_{{n=1}}",
                    r"\frac{4}{((2n-1)\pi)^{2}}\left( \cos\left( \frac{(2n-1)\pi}{2} \right) - 1 \right)",
                    r"\cos((2n-1)\pi t)",
                ]
            ).align_to(old, LEFT + DOWN)
            new[1].set_color(PINK)
            new[3].set_color(self.replaced_val_color)
            old.become(new)
            return (old, new)

        graphed_fourier = ax.plot(
            fourier_function, self.graph_x_bounds, color=(RED, BLUE)
        )
        fourier_area = ax.get_area(
            graphed_fourier,
            [graphed_fourier.t_min, graphed_fourier.t_max],
            opacity=0.7,
            color=(PURE_BLUE, TEAL_A),
        )

        def fourier_graph_updater(
            old: ParametricFunction,
        ) -> Tuple[ParametricFunction, ParametricFunction]:
            new = ax.plot(fourier_function, self.graph_x_bounds).set_color_by_gradient(
                RED, BLUE
            )
            old.become(new)
            fourier_area.become(
                ax.get_area(
                    new,
                    [self.graph_x_bounds[0], self.graph_x_bounds[1]],
                    opacity=0.7,
                    color=(PURE_BLUE, TEAL_A),
                )
            )
            return

        updated_harmonic_eq = custom_mathtex(
            [
                r"f(t)=",
                r"1.500",
                f"+\\sum^{{0}}_{{n=1}}",
                r"\frac{4}{((2n-1)\pi)^{2}}\left( \cos\left( \frac{(2n-1)\pi}{2} \right) - 1 \right)",
                r"\cos((2n-1)\pi t)",
            ]
        ).align_to(harmonic_equation, LEFT + DOWN)
        updated_harmonic_eq[1].set_color(PINK)
        updated_harmonic_eq[3].set_color(self.replaced_val_color)

        self.play(
            Write(graphed_fourier),
            LaggedStart(
                with_context("Debido a Simetría Media Onda: $n \\to (2n-1)$", context),
                Write(fourier_area),
                harmonic_equation.animate.become(updated_harmonic_eq),
                lag_ratio=0.75,
                run_time=3,
            ),
        )
        graphed_fourier.add_updater(fourier_graph_updater)
        harmonic_equation.add_updater(harmonic_repr_updater)
        del updated_harmonic_eq

        self.camera.frame.save_state()
        self.play(
            LaggedStart(
                with_context("Expandir la serie de Fourier", context),
                AnimationGroup(
                    fourier_n.animate(run_time=2).set_value(3),
                    self.camera.frame.animate(run_time=3)
                    .set_height(6)
                    .set_width(6 * config.aspect_ratio)
                    .set_x(-2.5)
                    .set_y(-0.5),
                ),
                lag_ratio=0.75,
                run_time=4,
            )
        )

        self.play(
            self.camera.frame.animate.set_x(-1.5).set_y(1),
            LaggedStart(
                fourier_n.animate(rate_func=rate_functions.ease_in_out_quad).set_value(
                    999
                ),
                run_time=4,
            ),
        )
        # self.play(fourier_n.animate.set_value(450), run_time=2)
        self.play(
            LaggedStart(
                Restore(self.camera.frame),
                with_context("Apreciar la convergencia a la función original", context),
                lag_ratio=1 / 3,
                run_time=2.5,
            )
        )

        self.wait(1)
        return


def render():
    MatSup_1().render(preview=True)


render()
print("Done!\n")
