# -*- coding: utf-8 -*-
"""Scène d'introduction : connexité, connexité par arcs et caractérisation."""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Circle,
    Circumscribe,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    MoveAlongPath,
    ParametricFunction,
    Scene,
    SurroundingRectangle,
    Text,
    VGroup,
    Write,
    DOWN,
    DR,
    LEFT,
    ORIGIN,
    RIGHT,
    UL,
    UP,
)

from src.config import DEFAULT_WAIT, SHORT_WAIT
from src.utils.colors import (
    CLOSED_SET_COLOR,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    PATH_COLOR,
)


class ConnexeVsArcs(Scene):
    """Compare les deux notions fondamentales de connexité."""

    def construct(self):
        self.section_titre()
        self.section_connexite_par_arcs()
        self.section_connexite()
        self.section_implication()
        self.section_caracterisation()

    def section_titre(self) -> None:
        titre = Text("Connexité et connexité par arcs", font_size=42)
        sous_titre = Text(
            "Deux notions proches, mais distinctes",
            font_size=24,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)

        self.play(Write(titre), run_time=1.3)
        self.play(FadeIn(sous_titre, shift=UP * 0.2))
        self.wait(DEFAULT_WAIT)
        self.play(FadeOut(titre), FadeOut(sous_titre))

    def section_connexite_par_arcs(self) -> None:
        titre = Text("Connexité par arcs", font_size=36, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        definition = MathTex(
            r"\forall x,y \in X,\; \exists \gamma : [0,1] \to X"
            r"\text{ continue, } \gamma(0)=x,\; \gamma(1)=y",
            font_size=26,
        ).next_to(titre, DOWN, buff=0.45)
        self.play(Write(definition), run_time=1.8)

        space = Circle(radius=2.2, color=DIM_COLOR, stroke_width=1.5).shift(DOWN * 0.8)
        x_dot = Dot([-1.2, -0.3, 0], color=HIGHLIGHT_COLOR, radius=0.08)
        y_dot = Dot([1.0, -1.0, 0], color=HIGHLIGHT_COLOR, radius=0.08)
        x_label = MathTex("x", font_size=24, color=HIGHLIGHT_COLOR).next_to(x_dot, UL, buff=0.1)
        y_label = MathTex("y", font_size=24, color=HIGHLIGHT_COLOR).next_to(y_dot, DR, buff=0.1)

        path = ParametricFunction(
            lambda t: np.array([
                -1.2 + 2.2 * t + 0.5 * np.sin(3 * np.pi * t),
                -0.3 - 0.7 * t + 0.4 * np.cos(2 * np.pi * t),
                0,
            ]),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=3,
        )
        gamma_label = MathTex(r"\gamma", font_size=28, color=PATH_COLOR)
        gamma_label.next_to(path.point_from_proportion(0.5), UP, buff=0.2)

        self.play(Create(space))
        self.play(FadeIn(x_dot), FadeIn(y_dot), Write(x_label), Write(y_label))
        self.play(Create(path), Write(gamma_label), run_time=1.8)

        moving_dot = Dot(color="#FFD166", radius=0.06).move_to(path.get_start())
        self.play(FadeIn(moving_dot))
        self.play(MoveAlongPath(moving_dot, path), run_time=2.2)

        exemple = MathTex(
            r"\mathbb{R}^n \text{ est connexe par arcs : }"
            r"\gamma(t) = (1-t)x + ty",
            font_size=26,
            color=OPEN_SET_COLOR,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(exemple))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_connexite(self) -> None:
        titre = Text("Connexité", font_size=36, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        definition = MathTex(
            r"X \text{ connexe} \iff "
            r"\nexists U,V \text{ ouverts disjoints non vides tels que } X = U \sqcup V",
            font_size=24,
        ).next_to(titre, DOWN, buff=0.45)
        self.play(Write(definition), run_time=1.8)

        label_non_connexe = Text("Non connexe", font_size=24, color=CLOSED_SET_COLOR)
        label_non_connexe.move_to(LEFT * 3.5 + DOWN * 0.3)
        left_open = Circle(radius=1.0, color=OPEN_SET_COLOR, fill_opacity=0.2).move_to(LEFT * 4.5 + DOWN * 1.5)
        right_open = Circle(radius=0.8, color="#4361EE", fill_opacity=0.2).move_to(LEFT * 2.5 + DOWN * 1.5)
        left_label = MathTex("U", font_size=24, color=OPEN_SET_COLOR).move_to(left_open)
        right_label = MathTex("V", font_size=24, color="#4361EE").move_to(right_open)

        label_connexe = Text("Connexe", font_size=24, color=OPEN_SET_COLOR)
        label_connexe.move_to(RIGHT * 3.5 + DOWN * 0.3)
        blob = Circle(radius=1.5, color=OPEN_SET_COLOR, fill_opacity=0.15).move_to(RIGHT * 3.5 + DOWN * 1.8)

        self.play(
            Write(label_non_connexe),
            Create(left_open),
            Create(right_open),
            Write(left_label),
            Write(right_label),
        )
        self.play(Write(label_connexe), Create(blob))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_implication(self) -> None:
        titre = Text("Théorème : connexe par arcs implique connexe", font_size=34, color=HIGHLIGHT_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        sous_titre = Text("Preuve par contraposée", font_size=24, color=DIM_COLOR)
        sous_titre.next_to(titre, DOWN, buff=0.35)
        self.play(Write(sous_titre))

        etapes = VGroup(
            MathTex(r"\text{Supposons } X = U \sqcup V \text{ avec } U,V \text{ ouverts disjoints non vides}", font_size=23),
            MathTex(r"\text{Prenons } x \in U \text{ et } y \in V", font_size=23),
            MathTex(r"\text{Si un chemin } \gamma \text{ joignait } x \text{ à } y,", font_size=23),
            MathTex(r"\gamma^{-1}(U) \text{ et } \gamma^{-1}(V) \text{ sépareraient } [0,1]", font_size=23),
            MathTex(r"\text{Mais } [0,1] \text{ est connexe : contradiction.}", font_size=24, color=CLOSED_SET_COLOR),
        ).arrange(DOWN, buff=0.32, aligned_edge=LEFT).move_to(ORIGIN + DOWN * 0.45)

        for line in etapes:
            self.play(Write(line), run_time=1.0)
            self.wait(SHORT_WAIT)

        self.play(Circumscribe(etapes[-1], color=CLOSED_SET_COLOR))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    def section_caracterisation(self) -> None:
        titre = Text("Caractérisation par les applications vers {0,1}", font_size=34, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))

        theoreme = MathTex(
            r"X \text{ connexe} \iff "
            r"\text{toute } f : X \to \{0,1\} \text{ continue est constante}",
            font_size=26,
        ).next_to(titre, DOWN, buff=0.45)
        box = SurroundingRectangle(theoreme, color=HIGHLIGHT_COLOR, buff=0.18)
        self.play(Write(theoreme), Create(box), run_time=1.8)

        source_space = Circle(radius=1.5, color=OPEN_SET_COLOR, fill_opacity=0.1).shift(LEFT * 3 + DOWN * 1.5)
        source_label = MathTex("X", font_size=28).next_to(source_space, UP, buff=0.15)
        target = VGroup(
            Dot([3, -1, 0], color="#FFD166", radius=0.1),
            Dot([3, -2, 0], color="#4361EE", radius=0.1),
        )
        target_labels = VGroup(
            MathTex("0", font_size=22).next_to(target[0], RIGHT, buff=0.15),
            MathTex("1", font_size=22).next_to(target[1], RIGHT, buff=0.15),
        )
        target_brace = MathTex(r"\{0,1\}", font_size=26).next_to(
            VGroup(target, target_labels),
            RIGHT,
            buff=0.25,
        )
        arrow = Arrow(LEFT * 1.3 + DOWN * 1.5, RIGHT * 2.3 + DOWN * 1.5, color=DIM_COLOR)
        f_label = MathTex("f", font_size=28).next_to(arrow, UP, buff=0.1)

        self.play(
            Create(source_space),
            Write(source_label),
            FadeIn(target),
            Write(target_labels),
            Write(target_brace),
        )
        self.play(Create(arrow), Write(f_label))

        conclusion = Text(
            "Sur un espace connexe, une telle application ne peut pas séparer l'espace.",
            font_size=22,
            color=HIGHLIGHT_COLOR,
        ).to_edge(DOWN, buff=0.45)
        self.play(Write(conclusion))
        self.wait(DEFAULT_WAIT)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
