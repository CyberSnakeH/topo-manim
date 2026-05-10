"""Utilitaires de positionnement, légendes et annotations."""

from manim import (
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    ManimColor,
    MathTex,
    Rectangle,
    Text,
    VGroup,
)


def title_text(text: str, font_size: int = 40, **kwargs) -> Text:
    """Crée un titre positionné en haut de l'écran."""
    t = Text(text, font_size=font_size, **kwargs)
    t.to_edge(UP, buff=0.5)
    return t


def section_label(text: str, position=LEFT, **kwargs) -> Text:
    """Petit label de section sur le côté."""
    label = Text(text, font_size=24, color=ManimColor("#8D99AE"), **kwargs)
    label.to_edge(position, buff=0.3).to_edge(UP, buff=0.3)
    return label


def side_by_side(*mobjects, buff: float = 1.0) -> VGroup:
    """Place des mobjects côte à côte, centrés horizontalement."""
    group = VGroup(*mobjects).arrange(RIGHT, buff=buff)
    group.move_to(ORIGIN)
    return group


def annotate(mobject, label_text: str, direction=DOWN, font_size: int = 22):
    """Ajoute une annotation LaTeX sous un mobject."""
    label = MathTex(label_text, font_size=font_size)
    label.next_to(mobject, direction, buff=0.25)
    return label


def bounding_box(mobject, buff: float = 0.2, **kwargs) -> Rectangle:
    """Rectangle englobant un mobject."""
    rect = Rectangle(
        width=mobject.width + 2 * buff,
        height=mobject.height + 2 * buff,
        **kwargs,
    )
    rect.move_to(mobject)
    return rect
