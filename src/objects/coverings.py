"""Recouvrements et sous-recouvrements pour Borel-Lebesgue."""

from __future__ import annotations
from manim import VGroup, Circle, MathTex, FadeIn, FadeOut, DOWN
from src.utils.colors import COVER_COLORS


class Covering(VGroup):
    """Recouvrement d'un ensemble par une famille d'ouverts."""

    def __init__(
        self,
        centers: list[tuple[float, float]],
        radii: list[float],
        colors: list | None = None,
        fill_opacity: float = 0.15,
        label: str | None = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.open_sets: list[Circle] = []
        colors = colors or COVER_COLORS

        for i, (center, radius) in enumerate(zip(centers, radii)):
            c = Circle(
                radius=radius,
                color=colors[i % len(colors)],
                fill_opacity=fill_opacity,
                stroke_width=2,
            ).move_to([center[0], center[1], 0])
            self.open_sets.append(c)
            self.add(c)

        if label:
            self.label = MathTex(label, font_size=24)
            self.label.next_to(self, DOWN, buff=0.2)
            self.add(self.label)

    def extract_subcover(self, indices: list[int]) -> "Covering":
        """Extrait un sous-recouvrement à partir d'indices."""
        centers = []
        radii = []
        for i in indices:
            c = self.open_sets[i]
            centers.append((c.get_center()[0], c.get_center()[1]))
            radii.append(c.radius)
        return Covering(centers=centers, radii=radii, fill_opacity=0.3)

    def highlight_subcover(self, indices: list[int], opacity: float = 0.4):
        """Met en valeur certains ouverts du recouvrement."""
        for i, c in enumerate(self.open_sets):
            if i in indices:
                c.set_fill(opacity=opacity)
                c.set_stroke(width=3)
            else:
                c.set_fill(opacity=0.05)
                c.set_stroke(width=1, opacity=0.3)
