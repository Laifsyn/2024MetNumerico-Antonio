from typing import Callable
from manim import *


class TestPy(Scene):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.upper_bound = 1
        self.lower_bound = 0
        self.half_period = 0.5
        self.smoothing = False
        self.graph_dx = 0.001

    def bounded(
        self, f: Callable[[float], float], upper_bound: float, lower_bound: float
    ):
        return lambda x: f(
            (x - lower_bound) % (upper_bound - lower_bound) + lower_bound
        )

    def construct(self):
        def self_f(x: float) -> Callable[[float], float]:
            print("Received {:.3f}", x)
            if x < 0.25:
                return x
            elif x < 0.75:
                return -x + .5
            else:
                return x - 1

        f = self.bounded(self_f, self.upper_bound, self.lower_bound)
        ax = Axes(
            x_range=[-5.0, 5.0, 0.25],  # Displayed (smallest_x, largest_x, step)
            y_range=[-3.0, 3.0, 0.25],
            x_length=20,  # x_length * step
            y_length=30,
            x_axis_config={
                "numbers_to_include": np.arange(-4, 4.01, 1)
            },  # (Inclusive Lower Bound, Exclusive Upper Bound, Step)
            y_axis_config={"numbers_to_include": np.arange(-0.5, 1, 0.25)},
            tips=True,
        )
        labels = ax.get_axis_labels(
            x_label=Tex("$\Delta Q$"), y_label=Tex("T[$^\circ C$]")
        )

        # x_values = np.array([0, 0.25, 0.5, 0.75, 1])
        # y_values = np.array([0, 0.25, 0, -0.25, 0])
        # graph = ax.plot_line_graph(
        #     x_values=x_values, y_values=y_values, line_color=BLUE
        # )

        # x_values = np.array([0, 0.25, 0.5, 0.75, 1])
        # y_values = np.array([0, 0.25, 0, -0.25, 0])
        # graph = ax.plot_line_graph(
        #     x_values=x_values, y_values=y_values, line_color=BLUE
        # )

        graph = ax.plot(f, color=BLUE, x_range=[-3, 3, 0.01], use_smoothing=False)

        self.add(ax, labels, graph)


TestPy().render()
