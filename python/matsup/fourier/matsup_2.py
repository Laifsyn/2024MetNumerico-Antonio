from manim import *
import numpy as np
from typing import Callable, Sequence


class MatSup_2(MovingCameraScene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upper_bound = 1.0
        self.lower_bound = 0.0
        self.half_period = 0.5
        self.smoothing = False
        self.graph_dx = 0.001

    def f(self) -> Callable[[float], float]:
        def _f(x):
            if x < 0.25:
                return x
            elif x < 0.75:
                return -x + 0.5
            else:
                return x - 1

        return self.bounded(_f, self.upper_bound, self.lower_bound)

    @property
    def plane(self) -> NumberPlane:
        [lower_x, upper_x, *_] = self.graph_bounds

        return NumberPlane(
            x_range=[
                0.0 + lower_x,
                0.0 + upper_x,
                0.25,
            ],  # Displayed (smallest_x, largest_x, step)
            y_range=[-1.0, 1.0, 0.25],
            x_length=10,  # x_length * step
            y_length=10,
            x_axis_config={
                "numbers_to_include": np.arange(
                    lower_x + self.half_period,
                    upper_x - self.half_period + 0.1,
                    0.5,
                )
            },  # (Inclusive Lower Bound, Exclusive Upper Bound, Step)
            y_axis_config={"numbers_to_include": np.arange(-0.5, 1, 0.25)},
            tips=True,
            background_line_style={
                "stroke_color": GRAY_BROWN,  # Change grid line color here
                "stroke_width": 1,  # Width of the grid lines
                "stroke_opacity": 0.5,  # Opacity of the grid lines
            },
        )

    @property
    def graph_bounds(self) -> Sequence[float]:
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

        ax = self.plane

        f = lambda x: self.f()(x)

        graph = ax.plot(
            f,
            color=BLUE,
            x_range=self.graph_bounds,
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

        equation = (
            MathTex(
                r"f(x) = \begin{cases} x & \text{if } 0 \leq x < 0.25 \\ -x + 0.5 & \text{if } 0.25 \leq x < 0.75 \\ x - 1 & \text{if } 0.75 \leq x < 1 \end{cases}"
            )
            .move_to([-2, -2, 0])
            .scale(0.5)
            .set_color(TEAL)
        )
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
                self.play(AnimationGroup(Write(dot_1), Write(dot_2)))
                continue
            if i is gimT:
                # Pan in between F(x - T) and F(x + T), while drawing the Half-T Dot
                self.play(
                    AnimationGroup(
                        Write(dot_m),
                        # self.camera.frame.animate.scale(1).move_to(gip.get_center()),
                    )
                )
                # Write f(x - T) and f(x + T)
                self.play(AnimationGroup(Write(gimT), Write(gipT)), run_time=2)
                # Espejo de gipT con el origen de coordenadas
                self.play(gipT.animate.rotate(PI, Y_AXIS, about_point=ax.get_origin()))
                # self.wait()
                continue
            self.play(Write(i))
        self.wait()
        # Voltear gipT de maneral horizontal
        # self.play(gipT.animate.rotate_about_origin(PI, Y_AXIS))
        # Pan in to the graph
        # self.play(self.camera.frame.animate.scale(0.5).move_to(moving_dot))
        self.camera.frame.add_updater(update_curve)
        self.play(
            MoveAlongPath(moving_dot, graph_in_period, rate_func=linear),
            run_time=1,
        )
        self.camera.frame.remove_updater(update_curve)

        # Pan Out to center
        self.play(self.camera.frame.animate.scale(0.8).move_to(gip.get_center()))
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
        self.add(graph.copy())
        self.bring_to_front(gip)
        self.play(
            AnimationGroup(
                ReplacementTransform(graph.copy(), shifted_graph),
                ReplacementTransform(gip, shifted_gip),
            ),
            run_time=2,
        )
        self.bring_to_front(shifted_gip)
        self.wait()
        # Vertically Flip (with x-axis as the axis of reflection)
        self.play(shifted_graph.animate.rotate(PI, X_AXIS, about_point=ax.get_origin()).set_color(BS381.SIGNAL_RED))
        self.wait()

    def show_axis(self):
        x_start = np.array([-6, 0, 0])
        x_end = np.array([6, 0, 0])

        y_start = np.array([-4, -2, 0])
        y_end = np.array([-4, 2, 0])

        x_axis = Line(x_start, x_end)
        y_axis = Line(y_start, y_end)

        self.add(x_axis, y_axis)
        self.add_x_labels()

        self.origin_point = np.array([-4, 0, 0])
        self.curve_start = np.array([-3, 0, 0])


def render():
    MatSup_2().render(preview=True)


render()
print("Done!\n")
