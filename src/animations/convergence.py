"""Animations pour suites convergentes, suites de Cauchy et extraction."""

from __future__ import annotations

from typing import Callable

import numpy as np
from manim import (
    Axes,
    Circle,
    Create,
    Dot,
    FadeIn,
    Line,
    MathTex,
    Scene,
    VGroup,
    Write,
    DOWN,
    UP,
)

from src.config import DEFAULT_ANIM_DURATION
from src.utils.colors import DIM_COLOR, EPSILON_COLOR, HIGHLIGHT_COLOR


class SequenceConvergence:
    """Anime la convergence d'une suite dans un espace metrique."""

    def __init__(
        self,
        scene: Scene,
        terms: Callable[[int], tuple[float, float]],
        limit: tuple[float, float],
        n_terms: int = 20,
        axes: Axes | None = None,
    ):
        self.scene = scene
        self.terms = terms
        self.limit = limit
        self.n_terms = n_terms
        self.axes = axes

    def _to_point(self, point: tuple[float, float]):
        if self.axes is None:
            return [point[0], point[1], 0]
        return self.axes.c2p(point[0], point[1])

    def _screen_radius(self, radius: float) -> float:
        if self.axes is None:
            return radius
        center = self.axes.c2p(self.limit[0], self.limit[1])
        shifted = self.axes.c2p(self.limit[0] + radius, self.limit[1])
        return abs(shifted[0] - center[0])

    def play_convergence(self, eps_values: list[float] | None = None) -> None:
        """Affiche les termes et des boules epsilon autour de la limite."""
        eps_values = eps_values or [1.5, 1.0, 0.5, 0.2]

        limit_dot = Dot(
            self._to_point(self.limit),
            color=HIGHLIGHT_COLOR,
            radius=0.08,
        )
        limit_label = MathTex(r"\ell", font_size=26, color=HIGHLIGHT_COLOR)
        limit_label.next_to(limit_dot, DOWN, buff=0.15)

        self.scene.play(FadeIn(limit_dot), Write(limit_label))

        dots = VGroup()
        for n in range(self.n_terms):
            position = self.terms(n)
            dot = Dot(self._to_point(position), radius=0.04, color=DIM_COLOR)
            dots.add(dot)
            self.scene.play(FadeIn(dot), run_time=0.15)

        for eps in eps_values:
            ball = Circle(
                radius=self._screen_radius(eps),
                color=EPSILON_COLOR,
                fill_opacity=0.1,
                stroke_width=2,
            ).move_to(limit_dot)
            eps_label = MathTex(
                rf"\varepsilon = {eps}",
                font_size=22,
                color=EPSILON_COLOR,
            ).next_to(ball, UP, buff=0.1)

            self.scene.play(Create(ball), Write(eps_label))
            self.scene.wait(0.5)
            inside_ball = [
                dot
                for dot in dots
                if np.linalg.norm(dot.get_center() - limit_dot.get_center())
                <= self._screen_radius(eps)
            ]
            if inside_ball:
                self.scene.play(
                    *[dot.animate.set_color(HIGHLIGHT_COLOR) for dot in inside_ball[-5:]],
                    run_time=0.4,
                )
            self.scene.play(ball.animate.set_stroke(opacity=0.0), eps_label.animate.set_opacity(0.0))


class CauchySequence:
    """Anime une suite de Cauchy en mettant en evidence une queue de suite."""

    def __init__(
        self,
        scene: Scene,
        terms: Callable[[int], tuple[float, float]],
        n_terms: int = 25,
        axes: Axes | None = None,
    ):
        self.scene = scene
        self.terms = terms
        self.n_terms = n_terms
        self.axes = axes

    def _to_point(self, point: tuple[float, float]):
        if self.axes is None:
            return [point[0], point[1], 0]
        return self.axes.c2p(point[0], point[1])

    def play_cauchy(self, tail_start: int | None = None) -> None:
        """Montre qu'a partir d'un certain rang, les termes sont tous proches."""
        tail_start = tail_start or max(3, self.n_terms // 2)
        points = [self.terms(n) for n in range(self.n_terms)]
        dots = VGroup(
            *[
                Dot(self._to_point(point), radius=0.04, color=DIM_COLOR)
                for point in points
            ]
        )

        self.scene.play(
            *[FadeIn(dot, run_time=0.1) for dot in dots],
            run_time=DEFAULT_ANIM_DURATION,
        )

        tail = VGroup(*dots[tail_start:])
        self.scene.play(
            *[dot.animate.set_color(HIGHLIGHT_COLOR) for dot in tail],
            run_time=0.8,
        )

        reference_center = np.mean([dot.get_center() for dot in tail], axis=0)
        radius = max(
            np.linalg.norm(dot.get_center() - reference_center)
            for dot in tail
        ) + 0.2
        enclosing_ball = Circle(
            radius=radius,
            color=EPSILON_COLOR,
            stroke_width=2,
            fill_opacity=0.08,
        ).move_to(reference_center)

        connectors = VGroup(
            *[
                Line(tail[0].get_center(), dot.get_center(), color=EPSILON_COLOR, stroke_width=1.5)
                for dot in tail[1:]
            ]
        )
        condition = MathTex(
            r"\forall \varepsilon > 0,\; \exists N\; \forall n,m \geq N,\; d(x_n,x_m) < \varepsilon",
            font_size=24,
            color=EPSILON_COLOR,
        ).to_edge(DOWN, buff=0.5)

        self.scene.play(Create(enclosing_ball), Create(connectors))
        self.scene.play(Write(condition))
