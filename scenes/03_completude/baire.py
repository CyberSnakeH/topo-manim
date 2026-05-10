"""Complétude et théorème de Baire."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    Circle,
    Create,
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
    CLOSED_SET_COLOR,
    COVER_COLORS,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    TEXT_COLOR,
)


class Baire(Scene):
    """Illustre l'énoncé et l'idée de preuve du théorème de Baire."""

    def construct(self):
        self.section_titre()
        self.section_enonce()
        self.section_ouverts_denses()
        self.section_preuve()
        self.section_application()

    def section_titre(self) -> None:
        titre = Text("Théorème de Baire", font_size=42)
        sous_titre = Text(
            "La complétude empêche un espace d'être trop mince",
            font_size=24,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)
        self.play(Write(titre), run_time=1.4)
        self.play(FadeIn(sous_titre, shift=UP * 0.2))
        self.wait(DEFAULT_WAIT)
        self.play(FadeOut(titre), FadeOut(sous_titre))

    def section_enonce(self) -> None:
        titre = Text("Énoncé", font_size=32, color=HIGHLIGHT_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        statement = (
            VGroup(
                MathTex(
                    r"(X,d)\text{ complet},\quad U_n \text{ ouverts denses}",
                    font_size=24,
                ),
                MathTex(
                    r"\Longrightarrow \bigcap_{n \geq 0} U_n \text{ est dense dans } X",
                    font_size=28,
                    color=OPEN_SET_COLOR,
                ),
            )
            .arrange(DOWN, buff=0.2)
            .next_to(titre, DOWN, buff=0.4)
        )
        box = SurroundingRectangle(statement, color=HIGHLIGHT_COLOR, buff=0.2)

        dual = MathTex(
            r"\text{Version duale : une union dénombrable de fermés d'intérieur vide"
            r"\text{ garde un intérieur vide.}",
            font_size=22,
            color=CLOSED_SET_COLOR,
        ).shift(DOWN * 1.8)

        self.play(Write(statement), Create(box), run_time=1.8)
        self.play(Write(dual), run_time=1.5)
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_ouverts_denses(self) -> None:
        titre = Text("Exemple d'ouvert dense", font_size=32, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        definition = MathTex(
            r"U \text{ ouvert dense dans } X \iff \overline{U} = X",
            font_size=24,
        ).next_to(titre, DOWN, buff=0.4)
        self.play(Write(definition), run_time=1.4)

        line = NumberLine(
            x_range=[-3, 3, 1],
            length=10,
            color=TEXT_COLOR,
            stroke_width=2,
            font_size=18,
        ).shift(DOWN * 0.5)
        self.play(Create(line))

        left_part = Line(line.n2p(-3), line.n2p(-0.05), color=OPEN_SET_COLOR, stroke_width=4)
        right_part = Line(line.n2p(0.05), line.n2p(3), color=OPEN_SET_COLOR, stroke_width=4)
        removed_zero = MathTex(r"\times", font_size=22, color=CLOSED_SET_COLOR).move_to(line.n2p(0))
        label = MathTex(
            r"\mathbb{R} \setminus \{0\}",
            font_size=24,
            color=OPEN_SET_COLOR,
        ).next_to(line, DOWN, buff=0.35)
        explanation = Text(
            "On retire un point, mais l'adhérence reste tout R.",
            font_size=20,
            color=DIM_COLOR,
        ).next_to(label, DOWN, buff=0.2)
        example2 = MathTex(
            r"\mathbb{R} \setminus \mathbb{Z} \text{ est aussi ouvert dense dans } \mathbb{R}.",
            font_size=22,
            color=COVER_COLORS[0],
        ).to_edge(DOWN, buff=0.3)

        self.play(Create(left_part), Create(right_part), FadeIn(removed_zero))
        self.play(Write(label), Write(explanation))
        self.play(Write(example2))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_preuve(self) -> None:
        titre = Text("Idée de preuve", font_size=32, color=HIGHLIGHT_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        intro = Text(
            "On construit des boules fermées emboîtées de rayons tendant vers 0.",
            font_size=22,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)
        self.play(Write(intro))

        balls = VGroup()
        radii = [2.5, 1.8, 1.2, 0.7, 0.35]
        for index, radius in enumerate(radii):
            ball = Circle(
                radius=radius,
                color=COVER_COLORS[index % len(COVER_COLORS)],
                fill_opacity=0.1,
                stroke_width=2,
            ).shift(DOWN * 1.0)
            balls.add(ball)

        labels = VGroup(
            *[
                MathTex(
                    rf"B_{index}",
                    font_size=20,
                    color=COVER_COLORS[index % len(COVER_COLORS)],
                )
                .next_to(balls[index], RIGHT, buff=0.12)
                .shift(UP * 0.08 * index)
                for index in range(len(balls))
            ]
        )

        for ball, label in zip(balls, labels, strict=False):
            self.play(Create(ball), Write(label), run_time=0.7)
            self.wait(SHORT_WAIT)

        steps = (
            VGroup(
                MathTex(
                    r"1.\ \text{Comme } U_n \text{ est dense, } B_n \cap U_n \neq \varnothing.",
                    font_size=20,
                ),
                MathTex(
                    r"2.\ \text{On choisit } B_{n+1} \subset B_n \cap U_n \text{ plus petite.}",
                    font_size=20,
                ),
                MathTex(
                    r"3.\ \text{Les centres forment une suite de Cauchy.}",
                    font_size=20,
                ),
                MathTex(
                    r"4.\ \text{La complétude donne une limite } x \in \bigcap_n B_n \subset \bigcap_n U_n.",
                    font_size=20,
                    color=OPEN_SET_COLOR,
                ),
            )
            .arrange(DOWN, buff=0.18, aligned_edge=LEFT)
            .to_edge(DOWN, buff=0.2)
        )

        for line in steps:
            self.play(Write(line), run_time=1.0)
            self.wait(SHORT_WAIT)

        limit = Dot(DOWN * 1.0, color=HIGHLIGHT_COLOR, radius=0.1)
        limit_label = MathTex(
            r"x \in \bigcap_{n \geq 0} U_n",
            font_size=22,
            color=HIGHLIGHT_COLOR,
        ).next_to(limit, DOWN, buff=0.15)
        self.play(FadeIn(limit, scale=1.8), Write(limit_label))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_application(self) -> None:
        titre = Text("Application : R est non dénombrable", font_size=32, color=HIGHLIGHT_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        proof = (
            VGroup(
                MathTex(
                    r"\text{Supposons } \mathbb{R} = \{x_n : n \in \mathbb{N}\}.", font_size=24
                ),
                MathTex(r"F_n = \{x_n\} \text{ est fermé d'intérieur vide.}", font_size=24),
                MathTex(r"\mathbb{R} = \bigcup_{n \geq 0} F_n.", font_size=24),
                MathTex(
                    r"\text{Par Baire, cette union ne peut pas avoir d'intérieur non vide.}",
                    font_size=24,
                ),
                MathTex(r"\text{Contradiction.}", font_size=24, color=CLOSED_SET_COLOR),
            )
            .arrange(DOWN, buff=0.32, aligned_edge=LEFT)
            .move_to(ORIGIN + DOWN * 0.45)
        )

        for line in proof:
            self.play(Write(line), run_time=1.1)
            self.wait(SHORT_WAIT)

        conclusion = MathTex(
            r"\mathbb{R} \text{ n'est pas dénombrable.}",
            font_size=28,
            color=OPEN_SET_COLOR,
        ).to_edge(DOWN, buff=0.45)
        box = SurroundingRectangle(conclusion, color=OPEN_SET_COLOR, buff=0.15)
        self.play(Write(conclusion), Create(box))
        self.wait(2.2)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
