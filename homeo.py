from manim import *
import numpy as np

class HomeoCercleCarreFinal(Scene):
    def construct(self):
        axes = Axes(
            x_range=[-1.5, 1.5, 1],
            y_range=[-1.5, 1.5, 1],
            axis_config={
                "color": WHITE,
                "tip_width": 0.15,   
                "tip_height": 0.15
            },
            x_length=6,
            y_length=6
        )
        self.play(Create(axes))

        # --------------------
        cercle = Circle(radius=1, color=BLUE)
        carre = Square(side_length=2, color=RED)

        # --------------------
        p_A = np.array([0, 1, 0])
        p_B = np.array([1, 0, 0])
        p_C = np.array([0, -1, 0])
        p_D = np.array([np.sqrt(2)/2, np.sqrt(2)/2, 0])

        points = [p_A, p_B, p_C, p_D]
        dots = VGroup(*[Dot(p, color=YELLOW, radius=0.09) for p in points])

        lignes = VGroup(*[Line(ORIGIN, p, color=GREEN, stroke_width=1) for p in points])

        # --------------------
        titre = Text(
            "Homéomorphisme : Cercle → Carré",
            font_size=24
        ).to_edge(UP)

        eq_cercle = Text(
            "Cercle : x² + y² = 1",
            font_size=20
        ).to_edge(LEFT).shift(UP * 1.5)

        eq_carre = Text(
            "Carré : max(|x|, |y|) = 1",
            font_size=20
        ).to_edge(LEFT).shift(UP * 1.5)

        formule_homeo = Text(
            "Φ(x,y) = (x,y) / max(|x|, |y|)",
            font_size=20
        ).to_edge(LEFT).shift(UP * 0.5)

        lab_A = Text("A (0,1) → (0,1)", font_size=16).next_to(dots[0], UR, buff=0.2)
        lab_B = Text("B (1,0) → (1,0)", font_size=16).next_to(dots[1], DR, buff=0.2)
        lab_C = Text("C (0,-1) → (0,-1)", font_size=16).next_to(dots[2], DL, buff=0.2)
        lab_D = Text("D (√2/2,√2/2) → (1,1)", font_size=16).next_to(dots[3], UR, buff=0.2)

        conclu = Text(
            "La connexité est préservée par homéomorphisme",
            font_size=20
        ).to_edge(DOWN)

        # --------------------
        self.play(Write(titre))
        self.play(Write(eq_cercle))
        self.play(Write(formule_homeo))
        self.play(Create(cercle))
        self.play(FadeIn(dots), FadeIn(lignes))
        self.play(Write(lab_A), Write(lab_B), Write(lab_C), Write(lab_D))
        self.wait(1.5)

        self.play(
            Transform(cercle, carre),
            Transform(eq_cercle, eq_carre),
            Transform(dots, VGroup(*[
                Dot(p / max(abs(p[0]), abs(p[1])), color=YELLOW, radius=0.09)
                for p in points
            ])),
            Transform(lignes, VGroup(*[
                Line(ORIGIN, p / max(abs(p[0]), abs(p[1])), color=GREEN)
                for p in points
            ])),
            run_time=3.5,
            rate_func=smooth
        )

        self.wait(1)
        self.play(Write(conclu))
        self.wait(2)