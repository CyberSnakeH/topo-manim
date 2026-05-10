"""Homéomorphismes et déformations continues."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Circle,
    Create,
    MathTex,
    Scene,
    Square,
    Transform,
    VMobject,
    Write,
)

from src.utils.colors import DIM_COLOR, OPEN_SET_COLOR


class ContinuousDeformation:
    """Anime une déformation continue (homotopie) entre deux formes."""

    def __init__(
        self,
        scene: Scene,
        source: VMobject,
        target: VMobject,
        label_source: str = "X",
        label_target: str = "Y",
    ):
        self.scene = scene
        self.source = source
        self.target = target
        self.label_source = label_source
        self.label_target = label_target

    def play_deformation(self, run_time: float = 3.0):
        """Anime la transformation continue de source vers target."""
        src_label = MathTex(self.label_source, font_size=30)
        src_label.next_to(self.source, DOWN, buff=0.2)

        tgt_label = MathTex(self.label_target, font_size=30)
        tgt_label.next_to(self.target, DOWN, buff=0.2)

        self.scene.play(Create(self.source), Write(src_label))
        self.scene.wait(0.5)
        self.scene.play(
            Transform(self.source, self.target),
            Transform(src_label, tgt_label),
            run_time=run_time,
        )


class HomeomorphismDemo:
    """Montre qu'un homéomorphisme préserve les propriétés topologiques."""

    def __init__(self, scene: Scene):
        self.scene = scene

    def play_circle_to_square(self):
        """Classique : le cercle est homéomorphe au carré."""
        circle = Circle(radius=1.5, color=OPEN_SET_COLOR).shift(LEFT * 3)
        square = Square(side_length=3, color=OPEN_SET_COLOR).shift(RIGHT * 3)

        arrow = Arrow(LEFT * 1, RIGHT * 1, color=DIM_COLOR)
        homeo_label = MathTex(r"\cong", font_size=36).next_to(arrow, UP, buff=0.1)

        circle_label = MathTex("S^1", font_size=28).next_to(circle, DOWN)
        square_label = MathTex(r"\partial [0,1]^2", font_size=28).next_to(square, DOWN)

        self.scene.play(
            Create(circle),
            Create(square),
            Write(circle_label),
            Write(square_label),
        )
        self.scene.play(Create(arrow), Write(homeo_label))

        # Déformation
        circle_copy = circle.copy().shift(RIGHT * 6)
        self.scene.play(
            Transform(circle_copy, square),
            run_time=2.5,
        )
