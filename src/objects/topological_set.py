"""Ouverts, fermés, intérieur, adhérence, frontière."""

from __future__ import annotations

from manim import (
    DOWN,
    Circle,
    DashedVMobject,
    MathTex,
    VGroup,
    VMobject,
)

from src.utils.colors import (
    BOUNDARY_COLOR,
    CLOSED_SET_COLOR,
    INTERIOR_COLOR,
    OPEN_SET_COLOR,
)


class TopologicalSet(VGroup):
    """Ensemble topologique visualisé comme une courbe fermée dans le plan.

    Utilise un cercle déformable pour représenter un sous-ensemble
    générique d'un espace topologique.
    """

    def __init__(
        self,
        shape: VMobject | None = None,
        is_open: bool = True,
        label: str | None = None,
        center: tuple[float, float] = (0, 0),
        radius: float = 1.5,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.is_open = is_open

        color = OPEN_SET_COLOR if is_open else CLOSED_SET_COLOR

        if shape is not None:
            self.boundary_curve = shape.copy()
        else:
            self.boundary_curve = Circle(radius=radius, color=color)
            self.boundary_curve.move_to([center[0], center[1], 0])

        if is_open:
            # Ouverts : bord en pointillés
            self.boundary_curve = DashedVMobject(self.boundary_curve, num_dashes=30)
        else:
            self.boundary_curve.set_stroke(width=3)

        self.add(self.boundary_curve)

        if label:
            self.label = MathTex(label, font_size=28, color=color)
            self.label.next_to(self.boundary_curve, DOWN, buff=0.2)
            self.add(self.label)

    def get_interior(self, **kwargs) -> TopologicalSet:
        """Retourne une représentation de l'intérieur (légèrement plus petit)."""
        interior = TopologicalSet(
            is_open=True,
            center=(0, 0),
            radius=1.2,
            label=None,
            **kwargs,
        )
        interior.boundary_curve.set_color(INTERIOR_COLOR)
        interior.move_to(self.get_center())
        return interior

    def get_boundary_highlight(self) -> VMobject:
        """Retourne le bord mis en évidence."""
        bnd = self.boundary_curve.copy()
        bnd.set_color(BOUNDARY_COLOR)
        bnd.set_stroke(width=4)
        return bnd
