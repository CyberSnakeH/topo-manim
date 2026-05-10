"""Compacité et théorème de Borel-Lebesgue."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    UP,
    Circle,
    Create,
    DashedVMobject,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    NumberLine,
    Scene,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
)

from src.config import DEFAULT_WAIT, SHORT_WAIT
from src.utils.colors import (
    COVER_COLORS,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    TEXT_COLOR,
)

WARN_COLOR = "#EF476F"


class BorelLebesgue(Scene):
    """Scène sur la compacité métrique et les recouvrements ouverts."""

    def construct(self):
        self.section_titre()
        self.section_def_compacite()
        self.section_recouvrement()
        self.section_segment_compact()
        self.section_non_compact()
        # self.section_lebesgue()

    def section_titre(self) -> None:
        titre = Text("Compacité et Borel-Lebesgue", font_size=42)
        sous_titre = Text(
            "Du recouvrement infini au sous-recouvrement fini",
            font_size=24,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)

        self.play(Write(titre), run_time=1.4)
        self.play(FadeIn(sous_titre, shift=UP * 0.2))
        self.wait(DEFAULT_WAIT)
        self.play(FadeOut(titre), FadeOut(sous_titre))

    def section_def_compacite(self) -> None:
        titre = Text("Compacité séquentielle", font_size=32, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        definition = MathTex(
            r"(X,d)\text{ compact} \iff \text{ toute suite admet une sous-suite convergente}",
            font_size=24,
        ).next_to(titre, DOWN, buff=0.45)
        box = SurroundingRectangle(definition, color=HIGHLIGHT_COLOR, buff=0.15)
        self.play(Write(definition), Create(box), run_time=1.8)

        line = NumberLine(
            x_range=[0, 1, 0.1],
            length=8,
            numbers_to_include=[0, 0.5, 1],
            color=DIM_COLOR,
            stroke_width=2,
            font_size=20,
        ).shift(DOWN * 1.0)
        self.play(Create(line))

        np.random.seed(42)
        values = []
        for n in range(1, 32):
            value = 0.5 + 0.4 * (-1) ** n / n + 0.05 * np.random.randn()
            values.append(float(np.clip(value, 0.01, 0.99)))

        dots = VGroup(
            *[Dot(line.n2p(value), radius=0.025, color=OPEN_SET_COLOR) for value in values]
        )
        for dot in dots[:8]:
            self.play(FadeIn(dot), run_time=0.18)
        self.play(*[FadeIn(dot) for dot in dots[8:]], run_time=0.5)

        limit_dot = Dot(line.n2p(0.5), radius=0.025, color=HIGHLIGHT_COLOR)
        limit_label = MathTex(r"\ell", font_size=24, color=HIGHLIGHT_COLOR).next_to(
            limit_dot, UP, buff=0.2
        )
        self.play(FadeIn(limit_dot, scale=2), Write(limit_label))

        subsequence_indices = [1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27]
        subsequence = VGroup(*[dots[i] for i in subsequence_indices])
        self.play(*[dot.animate.set_color("#FFD166") for dot in subsequence], run_time=0.8)

        caption = Text(
            "Une sous-suite se rapproche de la valeur d'adhérence.", font_size=20, color="#FFD166"
        )
        caption.to_edge(DOWN, buff=0.3)
        self.play(Write(caption))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_recouvrement(self) -> None:
        titre = Text("Théorème de Borel-Lebesgue", font_size=32, color=HIGHLIGHT_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        theoreme = MathTex(
            r"X \text{ compact} \iff \text{ tout recouvrement ouvert admet un sous-recouvrement fini}",
            font_size=22,
        ).next_to(titre, DOWN, buff=0.4)
        box = SurroundingRectangle(theoreme, color=HIGHLIGHT_COLOR, buff=0.15)
        self.play(Write(theoreme), Create(box), run_time=1.8)

        line = NumberLine(
            x_range=[-0.2, 1.2, 0.2], length=10, color=TEXT_COLOR, stroke_width=2
        ).shift(DOWN * 0.8)
        segment = Line(line.n2p(0), line.n2p(1), color=OPEN_SET_COLOR, stroke_width=5)
        segment_label = MathTex("[0,1]", font_size=22).next_to(segment, DOWN, buff=0.25)
        self.play(Create(line), Create(segment), Write(segment_label))

        centers = np.linspace(0, 1, 12)
        radii = [0.15] * 12
        cover = VGroup()
        for index, (center, radius) in enumerate(zip(centers, radii, strict=False)):
            circle = Circle(
                radius=radius * 5,
                color=COVER_COLORS[index % len(COVER_COLORS)],
                fill_opacity=0.20,
                stroke_width=0,
            )
            bords_pointilles = DashedVMobject(
                Circle(
                    radius=radius * 5,
                    color=COVER_COLORS[index % len(COVER_COLORS)],
                    stroke_width=1.5,
                ),
                num_dashes=20,
            )
            groupe_cercles = VGroup(circle, bords_pointilles).move_to(line.n2p(center))
            cover.add(groupe_cercles)
        label = Text("Beaucoup d'ouverts couvrent déjà [0,1].", font_size=20, color=DIM_COLOR)
        label.next_to(cover, UP, buff=0.25)
        self.play(*[FadeIn(group) for group in cover], Write(label), run_time=2)

        chosen = [0, 2, 3, 5, 7, 9, 11]
        others = [i for i in range(len(cover)) if i not in chosen]
        self.play(
            *[cover[i][0].animate.set_fill(opacity=0.35) for i in chosen],
            *[cover[i][1].animate.set_stroke(width=3) for i in chosen],
            *[cover[i].animate.set_fill(opacity=0.02).set_stroke(opacity=0.2) for i in others],
            run_time=1.2,
        )

        conclusion = Text(
            "Un nombre fini d'ouverts suffit encore.", font_size=22, color=HIGHLIGHT_COLOR
        )
        conclusion.next_to(cover, DOWN, buff=0.75)
        self.play(Write(conclusion))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_segment_compact(self) -> None:
        titre = Text("Dans R^n : Heine-Borel", font_size=32, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        theorem = MathTex(
            r"\text{Dans } \mathbb{R}^n,\; \text{compact} \iff \text{fermé et borné}",
            font_size=26,
        ).next_to(titre, DOWN, buff=0.4)
        box = SurroundingRectangle(theorem, color=HIGHLIGHT_COLOR, buff=0.15)
        self.play(Write(theorem), Create(box), run_time=1.5)

        props = (
            VGroup(
                MathTex(r"[0,1]", font_size=28, color=OPEN_SET_COLOR),
                MathTex(r"\text{fermé : } \checkmark", font_size=24),
                MathTex(r"\text{borné : } \checkmark", font_size=24),
                MathTex(r"\Longrightarrow \text{ compact}", font_size=26, color=OPEN_SET_COLOR),
            )
            .arrange(DOWN, buff=0.3)
            .shift(DOWN * 1.2)
        )

        for line in props:
            self.play(Write(line), run_time=0.7)
            self.wait(SHORT_WAIT)

        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_non_compact(self) -> None:
        titre = Text("Pourquoi ]0,1] n'est pas compact", font_size=32, color=WARN_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        line = NumberLine(
            x_range=[-0.1, 1.2, 0.2], length=10, color=DIM_COLOR, stroke_width=2
        ).shift(DOWN * 0.5)
        self.play(Create(line))

        missing_zero = MathTex(r"\times", font_size=24, color=WARN_COLOR).move_to(line.n2p(0))
        self.play(FadeIn(missing_zero))

        dots = VGroup()
        for n in range(1, 32):
            value = 1.0 / n
            dots.add(Dot(line.n2p(value), radius=0.05, color=OPEN_SET_COLOR))

        for dot in dots[:15]:
            self.play(FadeIn(dot), run_time=0.22)
        self.play(*[FadeIn(dot) for dot in dots[15:]], run_time=0.45)

        sequence_label = MathTex(
            r"x_n = \frac{1}{n} \to 0 \notin ]0,1]",
            font_size=24,
            color=WARN_COLOR,
        ).next_to(line, DOWN, buff=0.45)
        cover_label = MathTex(
            r"\text{La réunion des }U_n = \left]\frac{1}{n},2\right[ \text{ couvre } ]0,1] \text{ sans sous-recouvrement fini}",
            font_size=22,
            color=WARN_COLOR,
        ).to_edge(DOWN, buff=0.3)

        self.play(Write(sequence_label))
        self.play(Write(cover_label))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])


#    def section_lebesgue(self) -> None:
#         titre = Text("Lemme de Lebesgue", font_size=32, color=HIGHLIGHT_COLOR)
#         titre.to_edge(UP, buff=0.5)
#         self.play(Write(titre))

#         lemma = VGroup(
#             MathTex(
#                 r"\text{Si } X \text{ est compact et } \{U_i\} \text{ un recouvrement ouvert,}",
#                 font_size=24,
#             ),
#             MathTex(
#                 r"\exists \alpha > 0 \text{ tel que } \forall x,\; B(x,\alpha) \subset U_i \text{ pour un certain } i.",
#                 font_size=24,
#             ),
#         ).arrange(DOWN, buff=0.18).next_to(titre, DOWN, buff=0.35)
#         self.play(Write(lemma), run_time=1.8)

#         line = NumberLine(x_range=[-0.2, 1.2, 0.2], length=8, color=TEXT_COLOR, stroke_width=2).shift(DOWN * 1.0)
#         self.play(Create(line))

#         left_open = Circle(
#             radius=2.5,
#             color=COVER_COLORS[0],
#             fill_opacity=0.12,
#             stroke_width=1.5,
#         ).move_to(line.n2p(0.25))
#         right_open = Circle(
#             radius=2.5,
#             color=COVER_COLORS[2],
#             fill_opacity=0.12,
#             stroke_width=1.5,
#         ).move_to(line.n2p(0.75))
#         labels = VGroup(
#             MathTex("U_1", font_size=20, color=COVER_COLORS[0]).next_to(left_open, UP, buff=0.0),
#             MathTex("U_2", font_size=20, color=COVER_COLORS[2]).next_to(right_open, UP + RIGHT, buff=0.0),
#         )
#         self.play(Create(left_open), Create(right_open), Write(labels))

#         point = Dot(line.n2p(0.55), color="#FFD166", radius=0.06)
#         alpha_ball = Circle(
#             radius=0.6,
#             color=EPSILON_COLOR,
#             stroke_width=2,
#             fill_opacity=0.1,
#         ).move_to(line.n2p(0.55))
#         alpha_label = MathTex(r"\alpha", font_size=24, color=EPSILON_COLOR).next_to(alpha_ball, DOWN, buff=0.2)
#         result = MathTex(
#             r"B(x,\alpha) \subset U_2",
#             font_size=24,
#             color=EPSILON_COLOR,
#         ).to_edge(DOWN, buff=0.45)

#         self.play(FadeIn(point), Create(alpha_ball), Write(alpha_label))
#         self.play(Write(result))
#         self.wait(DEFAULT_WAIT)
#         self.play(*[FadeOut(mob) for mob in self.mobjects])
