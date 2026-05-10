"""Animations pour la continuite : epsilon-delta et image reciproque d'ouverts."""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Circle,
    Create,
    Dot,
    FadeIn,
    MathTex,
    Scene,
    ValueTracker,
    VGroup,
    Write,
    always_redraw,
)

from src.config import DEFAULT_ANIM_DURATION
from src.utils.colors import DELTA_COLOR, EPSILON_COLOR, OPEN_SET_COLOR


class EpsilonDeltaAnimation:
    """Construit une animation epsilon-delta a partir de deux axes."""

    def __init__(
        self,
        scene: Scene,
        f_graph,
        x0: float = 1.0,
        axes_source: Axes | None = None,
        axes_target: Axes | None = None,
    ):
        self.scene = scene
        self.f_graph = f_graph
        self.x0 = x0
        self.axes_source = axes_source
        self.axes_target = axes_target
        self.source_point: Dot | None = None
        self.target_point: Dot | None = None
        self.source_label: MathTex | None = None
        self.target_label: MathTex | None = None

    def _evaluate_f(self, x_value: float) -> float:
        """Evalue la fonction associee au graphe ou le callable fourni."""
        if callable(self.f_graph):
            return float(self.f_graph(x_value))
        if hasattr(self.f_graph, "underlying_function"):
            return float(self.f_graph.underlying_function(x_value))
        raise TypeError(
            "f_graph doit etre soit un callable, soit un objet Manim "
            "portant l'attribut underlying_function.",
        )

    def _screen_radius(
        self,
        axes: Axes,
        center: tuple[float, float],
        radius: float,
    ) -> float:
        """Convertit un rayon en coordonnées mathématiques vers l'écran."""
        x0, y0 = center
        point = axes.c2p(x0, y0)
        shifted = axes.c2p(x0 + radius, y0)
        return abs(shifted[0] - point[0])

    def setup(self) -> VGroup:
        """Prepare les points x0 et f(x0) sur les deux axes."""
        if self.axes_source is None or self.axes_target is None:
            raise ValueError(
                "axes_source et axes_target doivent etre fournis pour l'animation epsilon-delta.",
            )

        y0 = self._evaluate_f(self.x0)
        source_position = self.axes_source.c2p(self.x0, 0)
        target_position = self.axes_target.c2p(self.x0, y0)

        self.source_point = Dot(source_position, color=DELTA_COLOR, radius=0.06)
        self.target_point = Dot(target_position, color=EPSILON_COLOR, radius=0.06)

        self.source_label = MathTex("x_0", font_size=26, color=DELTA_COLOR)
        self.source_label.next_to(self.source_point, DOWN, buff=0.15)

        self.target_label = MathTex(r"f(x_0)", font_size=26, color=EPSILON_COLOR)
        self.target_label.next_to(self.target_point, RIGHT, buff=0.15)

        objects = VGroup(
            self.source_point,
            self.target_point,
            self.source_label,
            self.target_label,
        )
        self.scene.play(
            FadeIn(self.source_point),
            FadeIn(self.target_point),
            Write(self.source_label),
            Write(self.target_label),
        )
        return objects

    def play_epsilon_shrink(
        self,
        start_eps: float = 1.5,
        end_eps: float = 0.3,
        delta_factor: float = 0.5,
    ) -> None:
        """Anime le retrecissement de epsilon et du delta associe."""
        if self.source_point is None or self.target_point is None:
            self.setup()

        assert self.axes_source is not None
        assert self.axes_target is not None
        assert self.source_point is not None
        assert self.target_point is not None

        eps_tracker = ValueTracker(start_eps)
        delta_tracker = ValueTracker(start_eps * delta_factor)

        y0 = self._evaluate_f(self.x0)
        source_center = (self.x0, 0.0)
        target_center = (self.x0, y0)

        eps_circle = always_redraw(
            lambda: Circle(
                radius=self._screen_radius(
                    self.axes_target,
                    target_center,
                    eps_tracker.get_value(),
                ),
                color=EPSILON_COLOR,
                fill_opacity=0.15,
                stroke_width=2,
            ).move_to(self.target_point)
        )
        delta_circle = always_redraw(
            lambda: Circle(
                radius=self._screen_radius(
                    self.axes_source,
                    source_center,
                    delta_tracker.get_value(),
                ),
                color=DELTA_COLOR,
                fill_opacity=0.15,
                stroke_width=2,
            ).move_to(self.source_point)
        )
        eps_label = always_redraw(
            lambda: MathTex(
                rf"\varepsilon = {eps_tracker.get_value():.2f}",
                font_size=24,
                color=EPSILON_COLOR,
            ).next_to(eps_circle, UP, buff=0.15)
        )
        delta_label = always_redraw(
            lambda: MathTex(
                rf"\delta = {delta_tracker.get_value():.2f}",
                font_size=24,
                color=DELTA_COLOR,
            ).next_to(delta_circle, UP, buff=0.15)
        )

        self.scene.play(
            Create(eps_circle),
            Create(delta_circle),
            Write(eps_label),
            Write(delta_label),
        )
        self.scene.play(
            eps_tracker.animate.set_value(end_eps),
            delta_tracker.animate.set_value(end_eps * delta_factor),
            run_time=DEFAULT_ANIM_DURATION * 1.5,
        )

    def play_epsilon_delta(
        self,
        eps_values: list[float] | None = None,
        delta_factor: float = 0.5,
    ) -> None:
        """Parcourt plusieurs valeurs de epsilon en montrant un delta associe."""
        eps_values = eps_values or [1.2, 0.8, 0.4]
        for index, epsilon in enumerate(eps_values):
            start = eps_values[index - 1] if index > 0 else epsilon * 1.5
            self.play_epsilon_shrink(
                start_eps=start,
                end_eps=epsilon,
                delta_factor=delta_factor,
            )


class PreimageOpenSet:
    """Montre qu'une image reciproque d'ouvert reste ouverte."""

    def __init__(self, scene: Scene):
        self.scene = scene

    def play_preimage(self) -> None:
        """Anime le schema topologique f^-1(V)."""
        source_space = MathTex("X", font_size=30).shift(LEFT * 4 + UP * 2)
        target_space = MathTex("Y", font_size=30).shift(RIGHT * 4 + UP * 2)

        target_open = Circle(
            radius=1.0,
            color=OPEN_SET_COLOR,
            fill_opacity=0.2,
        ).shift(RIGHT * 3)
        target_label = MathTex("V", font_size=28).next_to(target_open, DOWN)

        source_open = Circle(
            radius=1.2,
            color=OPEN_SET_COLOR,
            fill_opacity=0.2,
        ).shift(LEFT * 3)
        source_label = MathTex("f^{-1}(V)", font_size=28).next_to(source_open, DOWN)

        arrow = Arrow(LEFT * 1.5, RIGHT * 1.5, color="#8D99AE")
        f_label = MathTex("f", font_size=30).next_to(arrow, UP, buff=0.1)
        conclusion = MathTex(
            r"V \text{ ouvert dans } Y \Longrightarrow f^{-1}(V) \text{ ouvert dans } X",
            font_size=26,
            color=OPEN_SET_COLOR,
        ).to_edge(DOWN, buff=0.6)

        self.scene.play(Write(source_space), Write(target_space))
        self.scene.play(Create(target_open), Write(target_label))
        self.scene.play(Create(arrow), Write(f_label))
        self.scene.play(Create(source_open), Write(source_label))
        self.scene.play(Write(conclusion))
