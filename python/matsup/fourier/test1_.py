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
        tex_template = TexTemplate()
        tex_template.add_to_preamble(r"\usepackage{cancel}\usepackage{color}")
        transformed_eq = MathTex(
            *[
                r"a_{n}= \frac{8}{\cancelto{ 2 }{",
                " T ",
                r"}}\int^{\cancelto{ 1/2 }{ \frac{T}{4} } }",
                r"_{0}{\left( t-\frac{1}{2} \right) \cos\left( n ",
                r"\cancelto{ \frac{2\pi}{2} }{\omega }",
                r" t \right)}dt",
            ],
            tex_template=tex_template,
        ).set_color(LIGHT_BROWN)
        transformed_eq[1][0:32].set_color(DARK_BLUE)
        transformed_eq[2][5:50].set_color(DARK_BLUE)
        transformed_eq[4][5:50].set_color(DARK_BLUE)
        self.add(transformed_eq)


TestPy().render(preview=True)
