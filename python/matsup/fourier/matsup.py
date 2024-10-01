from manim import *
import numpy as np
import math as math
from typing import Callable, Sequence


class MatSup_1(MovingCameraScene):
    def construct(self):
        npl = NumberPlane(
            # default numberplane has scene coordinates
        ).add_coordinates()
        self.add(npl)
        ax1 = Axes(
            x_range=[-10,10,2],
            y_range=[-10,10,2],
            x_length=5,
            y_length=5,
        ).add_coordinates().to_corner(UP+LEFT).set_color(YELLOW)     
        ax2 = Axes(
            x_range=[-100,100,20],
            y_range=[-100,100,20],
            x_length=5,
            y_length=5,
        ).add_coordinates().rotate(-30*DEGREES).to_corner(DOWN+RIGHT).set_color(RED) 

        self.add(ax1,ax2)

        dot1 = Dot(color=YELLOW).move_to(ax1.c2p(5,5))     
        text1a = MathTex(r"(+5,+5)", color=YELLOW, font_size=20)
        text1b = MathTex(r"({:.1f},{:.1f},{:.1f})".format(*ax1.c2p(5,5)), color=WHITE, font_size=20)
        text1c = MathTex(r"({:.1f},{:.1f})".format(*ax2.p2c(ax1.c2p(5,5))), color=RED, font_size=20)
        self.add(
            dot1,
            text1c.next_to(dot1,UP,buff=0),
            text1b.next_to(text1c,UP,buff=0),
            text1a.next_to(text1b,UP,buff=0),
        )
              
        dot2 = Dot(color=RED).move_to(ax2.c2p(-60,+40))     
        text2a = MathTex(r"(-60,+40)", color=RED, font_size=20)
        text2b = MathTex(r"({:.1f},{:.1f},{:.1f})".format(*ax2.c2p(-60,+40)), color=WHITE, font_size=20)
        text2c = MathTex(r"({:.1f},{:.1f})".format(*ax1.p2c(ax2.c2p(-60,+40))), color=YELLOW, font_size=20)
        self.add(
            dot2,
            text2c.next_to(dot2,UP,buff=0),
            text2b.next_to(text2c,UP,buff=0),
            text2a.next_to(text2b,UP,buff=0),
        )

        dot3 = Dot(color=WHITE).move_to([-2,-3,0])     
        text3a = MathTex(r"(-3,-2, 0)", color=WHITE, font_size=20)
        text3b = MathTex(r"({:.1f},{:.1f})".format(*ax2.p2c([-2,-3,0])), color=RED, font_size=20)
        text3c = MathTex(r"({:.1f},{:.1f})".format(*ax1.p2c([-2,-3,0])), color=YELLOW, font_size=20)
        self.add(
            dot3,
            text3c.next_to(dot3,UP,buff=0),
            text3b.next_to(text3c,UP,buff=0),
            text3a.next_to(text3b,UP,buff=0),
        )

        dot4 = Dot(color=WHITE).move_to(1*RIGHT+2*UP)     
        text4a = Tex(r"(1*RIGHT+2*UP)", color=WHITE, font_size=20)
        text4b = MathTex(r"({:.1f},{:.1f})".format(*ax2.p2c(1*RIGHT+2*UP)), color=RED, font_size=20)
        text4c = MathTex(r"({:.1f},{:.1f})".format(*ax1.p2c(1*RIGHT+2*UP)), color=YELLOW, font_size=20)
        self.add(
            dot4,
            text4c.next_to(dot4,UP,buff=0),
            text4b.next_to(text4c,UP,buff=0),
            text4a.next_to(text4b,UP,buff=0),
        )


def render():
    MatSup_1().render(preview=True)


render()
print("Done!\n")
