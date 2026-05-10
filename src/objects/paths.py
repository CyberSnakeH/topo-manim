"""Chemins, arcs et concaténation pour la connexité par arcs."""

from __future__ import annotations

from collections.abc import Callable

import numpy as np
from manim import (
    DOWN,
    Dot,
    ManimColor,
    MathTex,
    ParametricFunction,
    VGroup,
)

from src.utils.colors import ARC_COLOR, PATH_COLOR


class Path(VGroup):
    """Chemin continu γ : [0,1] → X visualisé dans le plan."""

    def __init__(
        self,
        func: Callable[[float], np.ndarray],
        color: ManimColor = PATH_COLOR,
        t_range: tuple[float, float] = (0, 1),
        label: str | None = None,
        show_endpoints: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.path_func = func

        self.curve = ParametricFunction(
            lambda t: np.array([*func(t), 0]) if len(func(t)) == 2 else func(t),
            t_range=[t_range[0], t_range[1]],
            color=color,
            stroke_width=3,
        )
        self.add(self.curve)

        if show_endpoints:
            start = func(t_range[0])
            end = func(t_range[1])
            self.start_dot = Dot(
                [start[0], start[1], 0],
                color=color,
                radius=0.07,
            )
            self.end_dot = Dot(
                [end[0], end[1], 0],
                color=color,
                radius=0.07,
            )
            self.add(self.start_dot, self.end_dot)

        if label:
            self.label = MathTex(label, font_size=24, color=color)
            self.label.next_to(self.curve, DOWN, buff=0.15)
            self.add(self.label)


class Arc(Path):
    """Arc = chemin continu injectif. Même API que Path."""

    def __init__(self, func, color: ManimColor = ARC_COLOR, **kwargs):
        super().__init__(func=func, color=color, **kwargs)


def concatenate_paths(gamma1: Callable, gamma2: Callable) -> Callable[[float], np.ndarray]:
    """Concaténation γ1 * γ2 : [0,1] → X."""

    def concatenated(t: float) -> np.ndarray:
        if t <= 0.5:
            return gamma1(2 * t)
        return gamma2(2 * t - 1)

    return concatenated
