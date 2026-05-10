"""Invariance topologique de la connexité."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    DR,
    LEFT,
    RIGHT,
    UL,
    UP,
    Arrow,
    Circle,
    Create,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    NumberLine,
    ParametricFunction,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    Write,
)

from src.config import DEFAULT_WAIT, SHORT_WAIT
from src.utils.colors import (
    CLOSED_SET_COLOR,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    PATH_COLOR,
)


class InvarianceTopologique(Scene):
    """Montre que la connexité est une propriété topologique."""

    def construct(self):
        self.section_titre()
        self.section_image_continue()
        self.section_homeomorphisme()
        self.section_application_r_r2()

    def section_titre(self) -> None:
        titre = Text("Invariance topologique", font_size=42)
        sous_titre = Text(
            "La connexité se transporte par les homéomorphismes",
            font_size=24,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)

        self.play(Write(titre), run_time=1.4)
        self.play(FadeIn(sous_titre, shift=UP * 0.2))
        self.wait(DEFAULT_WAIT)
        self.play(FadeOut(titre), FadeOut(sous_titre))

    def section_image_continue(self) -> None:
        titre = Text(
            "Image continue d'un espace connexe par arcs", font_size=32, color=OPEN_SET_COLOR
        )
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        theoreme = MathTex(
            r"f : X \to Y \text{ continue},\quad "
            r"X \text{ connexe par arcs } \Longrightarrow f(X) \text{ connexe par arcs}",
            font_size=24,
        ).next_to(titre, DOWN, buff=0.4)
        self.play(Write(theoreme), run_time=1.8)

        x_space = Circle(radius=1.5, color=OPEN_SET_COLOR, stroke_width=2).shift(
            LEFT * 3.5 + DOWN * 1.3
        )
        x_label = MathTex("X", font_size=28).next_to(x_space, UP, buff=0.15)
        x_dot = Dot([-4.2, -1.0, 0], color=HIGHLIGHT_COLOR, radius=0.07)
        y_dot = Dot([-2.8, -1.8, 0], color=HIGHLIGHT_COLOR, radius=0.07)
        x_text = MathTex("x", font_size=20).next_to(x_dot, UL, buff=0.08)
        y_text = MathTex("y", font_size=20).next_to(y_dot, DR, buff=0.08)
        gamma = ParametricFunction(
            lambda t: np.array(
                [
                    -4.2 + 1.4 * t + 0.3 * np.sin(2 * np.pi * t),
                    -1.0 - 0.8 * t + 0.2 * np.cos(3 * np.pi * t),
                    0,
                ]
            ),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=2.5,
        )
        gamma_label = MathTex(r"\gamma", font_size=22, color=PATH_COLOR).next_to(
            gamma.point_from_proportion(0.5),
            LEFT,
            buff=0.15,
        )

        y_space = Ellipse(width=3.5, height=2.5, color=OPEN_SET_COLOR, stroke_width=2).shift(
            RIGHT * 3.5 + DOWN * 1.3
        )
        y_space_label = MathTex("Y", font_size=28).next_to(y_space, UP, buff=0.15)
        fx_dot = Dot([2.5, -0.8, 0], color=HIGHLIGHT_COLOR, radius=0.07)
        fy_dot = Dot([4.3, -1.6, 0], color=HIGHLIGHT_COLOR, radius=0.07)
        fx_text = MathTex("f(x)", font_size=20).next_to(fx_dot, UL, buff=0.08)
        fy_text = MathTex("f(y)", font_size=20).next_to(fy_dot, DR, buff=0.08)
        image_path = ParametricFunction(
            lambda t: np.array(
                [
                    2.5 + 1.8 * t + 0.4 * np.sin(2.5 * np.pi * t),
                    -0.8 - 0.8 * t + 0.3 * np.cos(2 * np.pi * t),
                    0,
                ]
            ),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=2.5,
        )
        image_label = MathTex(r"f \circ \gamma", font_size=22, color=PATH_COLOR).next_to(
            image_path.point_from_proportion(0.5),
            RIGHT,
            buff=0.15,
        )
        arrow = Arrow(LEFT * 1.5 + DOWN * 1.3, RIGHT * 1.5 + DOWN * 1.3, color=DIM_COLOR)
        arrow_label = MathTex("f", font_size=26).next_to(arrow, UP, buff=0.1)

        self.play(Create(x_space), Write(x_label), Create(y_space), Write(y_space_label))
        self.play(
            FadeIn(x_dot),
            FadeIn(y_dot),
            Write(x_text),
            Write(y_text),
            FadeIn(fx_dot),
            FadeIn(fy_dot),
            Write(fx_text),
            Write(fy_text),
            Create(arrow),
            Write(arrow_label),
        )
        self.play(Create(gamma), Write(gamma_label), run_time=1.5)
        self.play(Create(image_path), Write(image_label), run_time=1.5)

        conclusion = MathTex(
            r"\gamma \text{ relie } x \text{ a } y \Longrightarrow f \circ \gamma \text{ relie } f(x) \text{ a } f(y)",
            font_size=22,
            color=HIGHLIGHT_COLOR,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(conclusion))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_homeomorphisme(self) -> None:
        titre = Text(
            "Corollaire : l'homéomorphisme préserve la connexité",
            font_size=32,
            color=OPEN_SET_COLOR,
        )
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        corollaire = MathTex(
            r"X \cong Y \Longrightarrow"
            r"\bigl(X \text{ connexe} \iff Y \text{ connexe}\bigr)",
            font_size=26,
        ).next_to(titre, DOWN, buff=0.4)
        box = SurroundingRectangle(corollaire, color=HIGHLIGHT_COLOR, buff=0.15)
        self.play(Write(corollaire), Create(box), run_time=1.8)

        circle = Circle(radius=1.3, color=OPEN_SET_COLOR, fill_opacity=0.15).shift(
            LEFT * 3 + DOWN * 1.5
        )
        circle_label = MathTex(r"S^1", font_size=24).next_to(circle, DOWN, buff=0.2)
        square = Square(side_length=2.4, color=OPEN_SET_COLOR, fill_opacity=0.15).shift(
            RIGHT * 3 + DOWN * 1.5
        )
        square_label = MathTex(r"\partial [0,1]^2", font_size=24).next_to(square, DOWN, buff=0.2)
        symbol = MathTex(r"\cong", font_size=36, color=HIGHLIGHT_COLOR).move_to(DOWN * 1.5)

        self.play(Create(circle), Write(circle_label))
        self.play(Write(symbol))
        self.play(Create(square), Write(square_label))

        deformed_circle = circle.copy()
        self.play(Transform(deformed_circle, square), run_time=2.2)
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_application_r_r2(self) -> None:
        titre = Text(
            "Application : R n'est pas homéomorphe à R^2", font_size=34, color=HIGHLIGHT_COLOR
        )
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        idee = Text(
            "On retire un point : les deux espaces réagissent topologiquement différemment.",
            font_size=22,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)
        self.play(Write(idee))

        line = NumberLine(x_range=[-4, 4, 1], length=6, color=DIM_COLOR, stroke_width=2).shift(
            DOWN * 0.8
        )
        removed_point = Dot([0, -0.8, 0], color=CLOSED_SET_COLOR, radius=0.1)
        cross = MathTex(r"\times", font_size=28, color=CLOSED_SET_COLOR).move_to(removed_point)
        left_part = Line([-3, -0.8, 0], [-0.2, -0.8, 0], color=OPEN_SET_COLOR, stroke_width=4)
        right_part = Line([0.2, -0.8, 0], [3, -0.8, 0], color="#4361EE", stroke_width=4)
        line_label = MathTex(r"\mathbb{R} \setminus \{0\}", font_size=26).next_to(
            line, DOWN, buff=0.25
        )
        line_conclusion = Text(
            "Non connexe : deux composantes",
            font_size=20,
            color=CLOSED_SET_COLOR,
        ).next_to(line_label, DOWN, buff=0.15)

        self.play(Create(line), FadeIn(cross))
        self.play(Create(left_part), Create(right_part))
        self.play(Write(line_label), Write(line_conclusion))
        self.wait(SHORT_WAIT)

        punctured_plane = Circle(radius=1.3, color=DIM_COLOR, stroke_width=1.5).shift(DOWN * 3.2)
        removed_origin = Dot([0, -3.2, 0], color=CLOSED_SET_COLOR, radius=0.08)
        cross2 = MathTex(r"\times", font_size=22, color=CLOSED_SET_COLOR).move_to(removed_origin)
        detour_path = ParametricFunction(
            lambda t: np.array(
                [
                    -0.8 * np.cos(np.pi * t),
                    -3.2 + 0.8 * np.sin(np.pi * t),
                    0,
                ]
            ),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=2.5,
        )
        plane_label = MathTex(r"\mathbb{R}^2 \setminus \{0\}", font_size=26).next_to(
            punctured_plane,
            DOWN,
            buff=0.25,
        )
        plane_conclusion = Text(
            "Connexe par arcs : on contourne le point retiré",
            font_size=20,
            color=OPEN_SET_COLOR,
        ).next_to(plane_label, DOWN, buff=0.15)

        self.play(Create(punctured_plane), FadeIn(cross2))
        self.play(Create(detour_path))
        self.play(Write(plane_label), Write(plane_conclusion))
        self.wait(DEFAULT_WAIT)

        conclusion = MathTex(
            r"\mathbb{R} \not\cong \mathbb{R}^2",
            font_size=36,
            color=HIGHLIGHT_COLOR,
        ).to_edge(DOWN, buff=0.25)
        box = SurroundingRectangle(conclusion, color=HIGHLIGHT_COLOR, buff=0.15)
        self.play(Write(conclusion), Create(box))
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
