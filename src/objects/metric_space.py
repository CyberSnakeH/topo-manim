"""Espaces métriques, boules ouvertes et voisinages."""

from __future__ import annotations

from manim import (
    DOWN,
    Axes,
    Circle,
    Dot,
    MathTex,
    VGroup,
)

from src.utils.colors import (
    DIM_COLOR,
    OPEN_SET_COLOR,
)


class OpenBall(VGroup):
    """Boule ouverte B(center, radius) dans le plan."""

    def __init__(
        self,
        center: tuple[float, float] = (0, 0),
        radius: float = 1.0,
        color=OPEN_SET_COLOR,
        fill_opacity: float = 0.25,
        label: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.ball_center = center
        self.ball_radius = radius

        self.circle = Circle(
            radius=radius,
            color=color,
            fill_opacity=fill_opacity,
            stroke_width=2,
        ).move_to([center[0], center[1], 0])

        self.dot = Dot(
            point=[center[0], center[1], 0],
            radius=0.05,
            color=color,
        )

        self.add(self.circle, self.dot)

        if label:
            self.label = MathTex(label, font_size=24)
            self.label.next_to(self.dot, DOWN, buff=0.15)
            self.add(self.label)


class MetricSpace(VGroup):
    """Représentation visuelle d'un espace métrique (portion du plan R²)."""

    def __init__(
        self,
        x_range: tuple[float, float] = (-4, 4),
        y_range: tuple[float, float] = (-3, 3),
        show_axes: bool = True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.x_range = x_range
        self.y_range = y_range

        if show_axes:
            self.axes = Axes(
                x_range=[x_range[0], x_range[1], 1],
                y_range=[y_range[0], y_range[1], 1],
                x_length=x_range[1] - x_range[0],
                y_length=y_range[1] - y_range[0],
                axis_config={"color": DIM_COLOR, "stroke_width": 1},
                tips=False,
            )
            self.add(self.axes)

    def coords_to_point(self, x: float, y: float):
        """Convertit des coordonnées métriques en position sur l'écran."""
        if hasattr(self, "axes"):
            return self.axes.c2p(x, y)
        return [x, y, 0]

    def add_ball(self, center, radius, **kwargs) -> OpenBall:
        """Ajoute une boule ouverte à l'espace."""
        ball = OpenBall(center=center, radius=radius, **kwargs)
        self.add(ball)
        return ball
