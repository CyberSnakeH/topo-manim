# -*- coding: utf-8 -*-
"""Primitives visuelles pour des scènes plus structurées et pédagogiques."""

from __future__ import annotations

from manim import Circle, LEFT, ManimColor, Mobject, RoundedRectangle, Text, VGroup, DOWN


def make_glow(target: Mobject, color: ManimColor | str, radii: tuple[float, ...] = (0.18, 0.32, 0.5)) -> VGroup:
    """Construit un halo doux autour d'un objet ponctuel."""

    opacities = (0.22, 0.12, 0.06)
    glow_layers = VGroup(
        *[
            Circle(
                radius=radius,
                stroke_width=0,
                fill_color=color,
                fill_opacity=opacity,
            ).move_to(target)
            for radius, opacity in zip(radii, opacities)
        ]
    )
    return glow_layers


def make_panel(
    title: str,
    body: Mobject,
    color: ManimColor | str,
    width: float | None = None,
    title_font_size: int = 26,
) -> VGroup:
    """Construit un panneau pédagogique à fond sombre et bord coloré."""

    title_mob = Text(title, font_size=title_font_size, color=color)
    content = VGroup(title_mob, body).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
    panel_width = max(content.width + 0.5, width or 0)
    panel = RoundedRectangle(
        corner_radius=0.18,
        width=panel_width,
        height=content.height + 0.45,
        stroke_color=color,
        stroke_width=2,
        fill_color="#101626",
        fill_opacity=0.92,
    )
    content.move_to(panel)
    content.align_to(panel, DOWN).shift(0.06 * DOWN)
    title_mob.align_to(content, LEFT)
    return VGroup(panel, content)


def make_panel_shadow(panel_group: VGroup, color: ManimColor | str) -> RoundedRectangle:
    """Ajoute une lueur large derrière un panneau."""

    panel = panel_group[0]
    return RoundedRectangle(
        corner_radius=0.22,
        width=panel.width + 0.22,
        height=panel.height + 0.22,
        stroke_width=0,
        fill_color=color,
        fill_opacity=0.08,
    ).move_to(panel)
