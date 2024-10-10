from typing import Callable
from manim import *


class TestPy(Scene):
    def construct(self):
        vertices = [i for i in range(7)]
        edges = [
            (0, 1),
            (1, 2),
            (3, 2),
            (3, 4),
            (5, 2),
        ]

        edge_config = {
            "stroke_width": 2,
            "tip_config": {
                "tip_shape": StealthTip,
                "tip_length": 0.15,
            },
            (3, 4): {
                "color": RED,
                "tip_config": {"tip_length": 0.25, "tip_width": 0.25}
            },
        }

        g = DiGraph(
            vertices,
            edges,
            labels=True,
            layout="circular",
            edge_config=edge_config,
        ).scale(1.4)

        self.play(Create(g))
        self.wait()


def graph_map():
    

TestPy().render(preview=True)
