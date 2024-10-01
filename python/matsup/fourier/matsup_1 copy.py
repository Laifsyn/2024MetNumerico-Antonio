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

        # Update Frame to fit graph
        [x_0, x_1, *_] = self.graph_x_bounds
        print(x_0, x_1)
        config.frame_width = x_1 - x_0
        config.frame_height = config.frame_width / config.aspect_ratio
        self.camera.frame_height = config.frame_height
        self.camera.frame_width = config.frame_width
        config.frame_rate = 24
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
                    run_time=4,
                )
                self.play(AnimationGroup(gipT.animate.flip()))
                continue
            self.play(Write(i))
        self.wait(0.75)
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
        self.play([FadeOut(x) for x in [dot_1, dot_2, dot_m, shifted_gip, moving_dot]])
        del dot_1, dot_2, dot_m, shifted_gip, moving_dot

        # Dibujar area bajo las curvas
        area_1 = ax.get_area(graph, [0, 1], opacity=0.5)
        area_2 = ax.get_area(shifted_graph, [0, 1], opacity=0.5)

        self.play(AnimationGroup(Write(area_1), Write(area_2)))

        # Shift up and down by 1 unit, and update the equation to match the graph
        updated_equation = MathTex("f(x) = |x|").move_to(equation)

        # Reduce Areas to fit shifted graph
        reduced_area_1 = ax.get_area(
            graph.copy().shift(DOWN), [0, 1], opacity=0.5, color=(PURPLE_E, TEAL_A)
        )
        reduced_area_2 = ax.get_area(
            shifted_graph.copy().shift(UP),
            [0, 1],
            opacity=0.5,
            color=(PURPLE_E, TEAL_A),
        )
        # Animate the shift
        self.play(
            AnimationGroup(
                shifted_graph.animate.shift(UP),
                graph.animate.shift(DOWN),
                ReplacementTransform(equation, updated_equation),
                ReplacementTransform(area_1, reduced_area_1),
                ReplacementTransform(area_2, reduced_area_2),
            )
        )

        # Small Cleanup and variable updating
        [equation, area_1, area_2] = [updated_equation, reduced_area_1, reduced_area_2]
        del updated_equation, reduced_area_1, reduced_area_2
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

        transformed_eq = (
            MathTex(
                r"f(t)=\begin{cases}\
t & \text{si } -1\leq t\leq 0 \\\
t& \text{si } 0\leq t\leq 1 \
\end{cases}; t=[-1,1]"
            )
            .move_to(equation.get_center() + UP * 3)
            .set_color_by_gradient(PURPLE_E, TEAL_A)
        )
        context_text = Text("La función es 1/4 de onda (Par)", color=TEAL_E)
        context_text.width = 8
        background: List[VMobject] = [ax, graph, area_1, area_2, labels]
        # Transformar la ecuación base para el rango a evaluar
        CAMERA_SW_CORNER = [-8.5, -4.0, 0.0]
        self.play(
            AnimationGroup(
                Write(context_text),
                ReplacementTransform(equation, transformed_eq),
                FadeOut(shifted_graph),
                self.camera.frame.animate.set_width(ax.c2p(9, 9) - ax.c2p(-9, -9)),
                # reducir la opacidad de los elementos del fondo
                *[x.animate.set_opacity(0.2) for x in background],
            )
        )

        self.play(
            context_text.animate.move_to(
                CAMERA_SW_CORNER - context_text.get_corner(DOWN + LEFT)
            )
        )

        # _Helper function to generate math equations
        custom_mathtex = lambda tex: (
            MathTex(tex, tex_template=tex_template, color=GOLD_E)
        )
        # Write solution

        solution1 = custom_mathtex(
            r"A_{n}=\frac{1}{2\cdot T}\cdot{2}\int_{0}^{T/2}{(1+t)\cos(n\omega t)dt}"
        )
        context = [context_text]

        def with_context(string: str, context: List[Text]) -> TransformMatchingShapes:
            text = Text(string, color=TEAL_E)
            text.move_to(CAMERA_SW_CORNER - text.get_corner(DOWN + LEFT))
            transform = TransformMatchingShapes(context[0], text)
            context[0] = text
            return transform

        last_solution = None
        self.play(
            AnimationGroup(Write(solution1), with_context("Hello World", context))
        )

        solution2 = custom_mathtex(
            r"A_{n}=\frac{1}{2}\int_{0}^{T/2}{\left(\cos(n\omega t)+t\cos(n\omega t)\right)dt}"
        ).next_to(solution1, DOWN)
        self.wait()
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
        self.wait()
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
