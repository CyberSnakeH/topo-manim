# -*- coding: utf-8 -*-
"""Contre-exemple classique : connexe ne signifie pas connexe par arcs.

La scene suit une narration plus formelle que les autres chapitres :

1. annonce du contre-exemple et decomposition E = G ∪ S ;
2. construction visuelle du graphe de sin(1/x) et de son segment limite ;
3. zooms successifs vers x = 0 pour faire apparaitre l'accumulation ;
4. preuve que E est connexe via le schema G ⊂ E ⊂ cl(G) ;
5. preuve que E n'est pas connexe par arcs via le premier instant de contact
   avec le segment vertical ;
6. bilan final.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Axes,
    BraceBetweenPoints,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Flash,
    Indicate,
    LaggedStart,
    Line,
    MathTex,
    MoveAlongPath,
    NumberLine,
    ParametricFunction,
    Rectangle,
    ReplacementTransform,
    Scene,
    ShowPassingFlash,
    SurroundingRectangle,
    Text,
    TracedPath,
    VGroup,
    Write,
    always_redraw,
    rate_functions,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    UR,
)

from src.objects.presentation import make_glow, make_panel, make_panel_shadow
from src.utils.colors import (
    CLOSED_SET_COLOR,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    PATH_COLOR,
    TEXT_COLOR,
)
from src.utils.layout import title_text


GRAPH_COLOR = OPEN_SET_COLOR
SEGMENT_COLOR = "#4CC9F0"
RUNNER_COLOR = PATH_COLOR
WARN_COLOR = CLOSED_SET_COLOR
THEOREM_COLOR = HIGHLIGHT_COLOR
BACKGROUND_COLOR = "#102033"


class ContreExempleSin1x(Scene):
    """Contre-exemple sin(1/x) pour la reciproque de la connexite par arcs."""

    def setup(self) -> None:
        self.camera.background_color = BACKGROUND_COLOR

    def construct(self) -> None:
        self.section_ouverture()
        self.section_geometrie()
        self.section_zooms()
        self.section_connexite()
        self.section_non_connexite_par_arcs()
        self.section_bilan()

    # ── Helpers ──────────────────────────────────────────────────── #

    def make_axes(
        self,
        x_range: list[float],
        y_range: list[float],
        x_length: float,
        y_length: float,
    ) -> Axes:
        return Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={
                "color": DIM_COLOR,
                "stroke_width": 1.5,
                "include_ticks": False,
            },
            tips=False,
        )

    def make_graph(
        self,
        axes: Axes,
        x_min: float,
        x_max: float,
        step: float,
        stroke_width: float = 2.8,
    ) -> ParametricFunction:
        return axes.plot(
            lambda x: np.sin(1 / x),
            x_range=[x_min, x_max, step],
            color=GRAPH_COLOR,
            stroke_width=stroke_width,
        )

    def make_segment(self, axes: Axes, stroke_width: float = 5) -> Line:
        return Line(
            axes.c2p(0, -1),
            axes.c2p(0, 1),
            color=SEGMENT_COLOR,
            stroke_width=stroke_width,
        )

    def make_formula_panel(self) -> VGroup:
        lines = VGroup(
            MathTex(
                r"A = \left\{\left(x,\sin\!\left(\frac{1}{x}\right)\right) : 0<x\leq \pi\right\}",
                font_size=22,
                color=GRAPH_COLOR,
            ),
            MathTex(
                r"\overline{A} = A \cup \bigl(\{0\}\times[-1,1]\bigr)",
                font_size=22,
                color=SEGMENT_COLOR,
            ),
            MathTex(
                r"\text{contre-exemple canonique du cours}",
                font_size=24,
                color=TEXT_COLOR,
            ),
        ).arrange(DOWN, buff=0.24, aligned_edge=LEFT)
        panel = make_panel("Contre-exemple", lines, THEOREM_COLOR, width=6.8)
        shadow = make_panel_shadow(panel, THEOREM_COLOR)
        return VGroup(shadow, panel)

    def make_section_title(self, text: str, color, font_size: int = 32) -> Text:
        return title_text(text, color=color, font_size=font_size)

    def make_proof_panel(
        self,
        title: str,
        body: VGroup,
        color,
        width: float,
    ) -> VGroup:
        panel = make_panel(title, body, color, width=width)
        shadow = make_panel_shadow(panel, color)
        return VGroup(shadow, panel)

    def make_caption_box(
        self,
        text: str,
        color,
        math: str | None = None,
        width: float = 10.6,
        font_size: int = 26,
        math_size: int = 28,
    ) -> VGroup:
        prose = Text(
            text,
            font_size=font_size,
            color=TEXT_COLOR,
            line_spacing=0.95,
        )
        prose.scale_to_fit_width(width)
        lines = [prose]
        if math is not None:
            formula = MathTex(math, font_size=math_size, color=color)
            if formula.width > width:
                formula.scale_to_fit_width(width)
            lines.append(formula)
        body = VGroup(*lines).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        box = SurroundingRectangle(body, color=color, buff=0.22, stroke_width=1.8)
        box.set_fill("#0B1728", opacity=0.94)
        return VGroup(box, body)

    def make_zoom_view(
        self,
        x_max: float,
        title: str,
        x_step: float,
        graph_min: float,
        graph_step: float,
        width: float = 3.6,
        height: float = 2.7,
    ) -> tuple[VGroup, Axes]:
        axes = self.make_axes(
            [-0.01 * max(1.0, x_max / 0.08), x_max, x_step],
            [-1.2, 1.2, 0.5],
            width,
            height,
        )
        graph = self.make_graph(
            axes,
            graph_min,
            x_max,
            step=graph_step,
            stroke_width=2.2,
        )
        segment = self.make_segment(axes, stroke_width=4)

        upper = DashedLine(
            axes.c2p(0, 1),
            axes.c2p(x_max, 1),
            color=DIM_COLOR,
            stroke_opacity=0.45,
            dash_length=0.08,
        )
        lower = DashedLine(
            axes.c2p(0, -1),
            axes.c2p(x_max, -1),
            color=DIM_COLOR,
            stroke_opacity=0.45,
            dash_length=0.08,
        )
        upper_label = MathTex("1", font_size=18, color=DIM_COLOR).next_to(
            upper, LEFT, buff=0.08,
        )
        lower_label = MathTex("-1", font_size=18, color=DIM_COLOR).next_to(
            lower, LEFT, buff=0.08,
        )
        caption = Text(title, font_size=20, color=TEXT_COLOR).next_to(
            axes, DOWN, buff=0.18,
        )

        return VGroup(
            axes,
            upper,
            lower,
            upper_label,
            lower_label,
            graph,
            segment,
            caption,
        ), axes

    def flash_oscillation_extrema(self, axes: Axes, n_start: int, n_stop: int) -> None:
        animations = []
        for n in range(n_start, n_stop):
            x_top = 1.0 / (np.pi / 2 + 2 * np.pi * n)
            x_bottom = 1.0 / (3 * np.pi / 2 + 2 * np.pi * n)
            animations.extend(
                [
                    Flash(
                        axes.c2p(x_top, 1),
                        color=HIGHLIGHT_COLOR,
                        line_length=0.10,
                        num_lines=10,
                        run_time=0.35,
                    ),
                    Flash(
                        axes.c2p(x_bottom, -1),
                        color=WARN_COLOR,
                        line_length=0.10,
                        num_lines=10,
                        run_time=0.35,
                    ),
                ]
            )
        self.play(LaggedStart(*animations, lag_ratio=0.12), run_time=2.0)

    # ── 1. Ouverture ─────────────────────────────────────────────── #

    def section_ouverture(self) -> None:
        title = title_text(
            "Connexe n'implique pas connexe par arcs",
            color=THEOREM_COLOR,
        )
        subtitle = Text(
            "Le graphe topologique du sinus fournit le contre-exemple canonique.",
            font_size=24,
            color=DIM_COLOR,
        ).next_to(title, DOWN, buff=0.24)

        implication = MathTex(
            r"\text{connexe par arcs} \Longrightarrow \text{connexe}",
            font_size=32,
            color=TEXT_COLOR,
        ).shift(UP * 0.65)
        false_reverse = MathTex(
            r"\text{connexe} \not\!\Longrightarrow \text{connexe par arcs}",
            font_size=32,
            color=WARN_COLOR,
        ).next_to(implication, DOWN, buff=0.35)

        example = self.make_caption_box(
            "Exemple : la courbe de sin(1/x) plus son segment limite.",
            THEOREM_COLOR,
            math=r"\overline{A}=A\cup(\{0\}\times[-1,1])",
            width=8.6,
            font_size=24,
            math_size=28,
        ).shift(DOWN * 2.0)

        self.play(Write(title), FadeIn(subtitle, shift=UP * 0.12))
        self.wait(0.8)
        self.play(Write(implication), run_time=1.4)
        self.wait(0.6)
        self.play(Write(false_reverse), run_time=1.4)
        self.wait(0.7)
        self.play(FadeIn(example, shift=UP * 0.18))
        self.wait(2.3)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ── 2. Geometrie de E = G ∪ S ───────────────────────────────── #

    def section_geometrie(self) -> None:
        title = title_text("1. Géométrie du contre-exemple", color=GRAPH_COLOR)
        self.play(Write(title))

        axes = self.make_axes([-0.25, 3.05, 0.5], [-1.3, 1.3, 0.5], 8.8, 4.8)
        axes.to_edge(LEFT, buff=0.75).shift(DOWN * 0.2)
        graph = self.make_graph(axes, 0.015, 3.0, step=0.0008)
        segment = self.make_segment(axes)

        x_label = MathTex("x", font_size=20, color=DIM_COLOR).next_to(
            axes.x_axis, RIGHT, buff=0.12,
        )
        y_label = MathTex("y", font_size=20, color=DIM_COLOR).next_to(
            axes.y_axis, UR, buff=0.12,
        )
        graph_label = MathTex("A", font_size=26, color=GRAPH_COLOR).move_to(
            axes.c2p(1.35, 1.05),
        )
        segment_label = MathTex(r"\overline{A}\setminus A", font_size=20, color=SEGMENT_COLOR).next_to(
            segment, LEFT, buff=0.18,
        )

        runner = Dot(color=RUNNER_COLOR, radius=0.075).move_to(graph.get_end())
        runner_glow = always_redraw(
            lambda: make_glow(runner, RUNNER_COLOR, radii=(0.14, 0.24, 0.38)),
        )
        runner_trace = TracedPath(
            runner.get_center,
            stroke_color=GRAPH_COLOR,
            stroke_width=3,
            stroke_opacity=0.9,
        )

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(segment), Write(segment_label), run_time=1.0)
        self.add(runner_trace, runner_glow, runner)
        self.play(
            MoveAlongPath(runner, graph.copy().reverse_points()),
            run_time=4.6,
            rate_func=rate_functions.linear,
        )
        runner_glow.clear_updaters()
        self.play(Write(graph_label))

        comment = self.make_caption_box(
            "La courbe A oscille de plus en plus vite et vient se coller au segment vertical.",
            GRAPH_COLOR,
            math=r"A=\left\{\left(x,\sin\left(\frac1x\right)\right):0<x\leq\pi\right\}",
            width=10.8,
            font_size=24,
            math_size=26,
        ).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(comment, shift=UP * 0.12))
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ── 3. Zooms successifs ─────────────────────────────────────── #

    def section_zooms(self) -> None:
        title = title_text("2. Oscillations au voisinage de x = 0", color=THEOREM_COLOR)
        self.play(Write(title))

        global_view, global_axes = self.make_zoom_view(
            x_max=1.4,
            title="Vue 1",
            x_step=0.2,
            graph_min=0.012,
            graph_step=0.00055,
            width=9.2,
            height=4.9,
        )
        zoom_1, zoom_1_axes = self.make_zoom_view(
            x_max=0.22,
            title="Vue 2",
            x_step=0.05,
            graph_min=0.0035,
            graph_step=0.00012,
            width=9.2,
            height=4.9,
        )
        zoom_2, zoom_2_axes = self.make_zoom_view(
            x_max=0.05,
            title="Vue 3",
            x_step=0.01,
            graph_min=0.0009,
            graph_step=0.00003,
            width=9.2,
            height=4.9,
        )

        for view in (global_view, zoom_1, zoom_2):
            view.shift(DOWN * 0.25)

        focus_global = Rectangle(
            width=0.70,
            height=2.0,
            stroke_color=THEOREM_COLOR,
            stroke_width=2,
        ).move_to(global_axes.c2p(0.16, 0))
        focus_zoom_1 = Rectangle(
            width=0.54,
            height=1.95,
            stroke_color=THEOREM_COLOR,
            stroke_width=2,
        ).move_to(zoom_1_axes.c2p(0.038, 0))

        caption_1 = self.make_caption_box(
            "De loin, on voit une courbe ordinaire. La zone importante est tout près de x = 0.",
            THEOREM_COLOR,
            width=10.8,
            font_size=24,
        ).to_edge(DOWN, buff=0.22)
        caption_2 = self.make_caption_box(
            "En zoomant, les oscillations sont toujours là. Elles ne disparaissent jamais.",
            THEOREM_COLOR,
            width=10.8,
            font_size=24,
        ).to_edge(DOWN, buff=0.22)
        caption_3 = self.make_caption_box(
            "Même très près de 0, la courbe remonte vers 1 puis redescend vers -1.",
            THEOREM_COLOR,
            math=r"\forall \delta>0,\ \ A\cap\bigl((0,\delta)\times\mathbb{R}\bigr)\ \text{approche }1\text{ et }-1",
            width=10.8,
            font_size=23,
            math_size=23,
        ).to_edge(DOWN, buff=0.22)

        self.play(FadeIn(global_view, shift=UP * 0.12))
        self.play(FadeIn(caption_1, shift=UP * 0.10), Create(focus_global))
        self.wait(0.8)
        self.play(FadeOut(caption_1), FadeOut(focus_global), FadeOut(global_view))
        self.play(FadeIn(zoom_1, shift=UP * 0.12))
        self.play(FadeIn(caption_2, shift=UP * 0.10), Create(focus_zoom_1))
        self.flash_oscillation_extrema(zoom_1_axes, 3, 6)
        self.wait(0.6)
        self.play(FadeOut(caption_2), FadeOut(focus_zoom_1), FadeOut(zoom_1))
        self.play(FadeIn(zoom_2, shift=UP * 0.12))
        self.play(FadeIn(caption_3, shift=UP * 0.10))
        self.flash_oscillation_extrema(zoom_2_axes, 10, 14)
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ── 4. Pourquoi E est connexe ───────────────────────────────── #

    def section_connexite(self) -> None:
        title = self.make_section_title("3. Pourquoi E est connexe", GRAPH_COLOR, font_size=30)
        self.play(Write(title))

        axes = self.make_axes([-0.05, 3.25, 0.5], [-1.25, 1.25, 0.5], 8.0, 4.5)
        axes.shift(DOWN * 0.35)
        graph = self.make_graph(axes, 0.0014, np.pi, step=0.00008, stroke_width=2.4)
        segment = self.make_segment(axes, stroke_width=4.5)
        graph_label = MathTex("A", font_size=24, color=GRAPH_COLOR).move_to(axes.c2p(2.0, 0.95))
        segment_label = MathTex(r"\overline{A}\setminus A", font_size=20, color=SEGMENT_COLOR).next_to(
            segment, LEFT, buff=0.10,
        )

        self.play(Create(axes), Create(graph), Create(segment), run_time=1.2)
        self.play(Write(graph_label), Write(segment_label))

        caption_1 = self.make_caption_box(
            "Étape 1. La courbe A est d'un seul morceau : elle vient d'un intervalle continu.",
            GRAPH_COLOR,
            math=r"A=f(]0,\pi])",
            width=10.8,
            font_size=24,
            math_size=28,
        ).to_edge(DOWN, buff=0.22)

        domain_line = NumberLine(
            x_range=[0, float(np.pi), 1],
            length=4.0,
            include_ticks=False,
            include_numbers=False,
            color=THEOREM_COLOR,
            stroke_width=2,
        ).move_to(RIGHT * 3.1 + DOWN * 1.95)
        domain_left = MathTex("0", font_size=18, color=THEOREM_COLOR).next_to(domain_line.get_start(), DOWN, buff=0.10)
        domain_right = MathTex(r"\pi", font_size=18, color=THEOREM_COLOR).next_to(domain_line.get_end(), DOWN, buff=0.10)
        domain_label = MathTex(r"]0,\pi]", font_size=24, color=THEOREM_COLOR).next_to(domain_line, UP, buff=0.12)
        arrow_f = Arrow(
            domain_line.get_top() + UP * 0.1,
            axes.c2p(2.3, 0.65),
            color=THEOREM_COLOR,
            buff=0.15,
            stroke_width=2,
        )
        f_label = MathTex(
            r"f(x)=\left(x,\sin\left(\frac1x\right)\right)",
            font_size=22,
            color=THEOREM_COLOR,
        ).next_to(arrow_f, RIGHT, buff=0.08)

        self.play(FadeIn(caption_1, shift=UP * 0.08))
        self.play(Create(domain_line), Write(domain_left), Write(domain_right), Write(domain_label))
        self.play(Create(arrow_f), Write(f_label), run_time=0.8)
        runner = Dot(color=RUNNER_COLOR, radius=0.06).move_to(graph.get_end())
        runner_glow = always_redraw(lambda: make_glow(runner, RUNNER_COLOR, radii=(0.10, 0.18, 0.28)))
        self.add(runner_glow, runner)
        self.play(MoveAlongPath(runner, graph.copy().reverse_points()), run_time=2.0, rate_func=rate_functions.linear)
        runner_glow.clear_updaters()
        self.play(FadeOut(runner_glow), FadeOut(runner))
        self.play(
            FadeOut(domain_line),
            FadeOut(domain_left),
            FadeOut(domain_right),
            FadeOut(domain_label),
            FadeOut(arrow_f),
            FadeOut(f_label),
        )

        caption_2 = self.make_caption_box(
            "Étape 2. Choisissons une hauteur y. On veut montrer que le point (0,y) est collé à la courbe.",
            SEGMENT_COLOR,
            math=r"y\in[-1,1]",
            width=10.8,
            font_size=24,
            math_size=28,
        ).to_edge(DOWN, buff=0.22)

        y_target = 0.55
        theta = float(np.arcsin(y_target))
        a_left = 1.0 / (theta + 2 * np.pi * 3)
        a_right = 1.0 / theta
        left_gate = DashedLine(axes.c2p(a_left, -1.15), axes.c2p(a_left, 1.15), color=THEOREM_COLOR, dash_length=0.06)
        right_gate = DashedLine(axes.c2p(a_right, -1.15), axes.c2p(a_right, 1.15), color=THEOREM_COLOR, dash_length=0.06)
        interval_label = MathTex(
            r"\left[\tfrac{1}{a+2\pi},\tfrac{1}{a}\right]",
            font_size=18,
            color=THEOREM_COLOR,
        ).next_to(right_gate, DOWN, buff=0.14).shift(LEFT * 1.0)
        interval_graph = self.make_graph(axes, a_left, a_right, step=0.00004, stroke_width=5.0).set_color(THEOREM_COLOR)
        approx_dots = VGroup(
            *[
                Dot(axes.c2p(1.0 / (theta + 2 * np.pi * n), y_target), radius=0.05, color=SEGMENT_COLOR)
                for n in [1, 2, 3, 5, 8]
            ]
        )
        target_dot = Dot(axes.c2p(0, y_target), radius=0.065, color=SEGMENT_COLOR)
        target_label = MathTex(r"(0,y)", font_size=20, color=SEGMENT_COLOR).next_to(target_dot, LEFT, buff=0.08)
        horizontal_target = DashedLine(
            axes.c2p(0, y_target),
            axes.c2p(a_right, y_target),
            color=SEGMENT_COLOR,
            dash_length=0.06,
        )

        self.play(ReplacementTransform(caption_1, caption_2))
        self.play(Create(horizontal_target), FadeIn(target_dot), Write(target_label), run_time=0.8)

        caption_3 = self.make_caption_box(
            "Étape 3. Dans une petite fenêtre près de 0, la courbe reprend cette hauteur encore et encore.",
            THEOREM_COLOR,
            math=r"x_n=\frac{1}{\theta+2\pi n}\longrightarrow 0",
            width=10.8,
            font_size=24,
            math_size=28,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_2, caption_3))
        self.play(Create(left_gate), Create(right_gate), Write(interval_label), run_time=0.8)
        self.play(Create(interval_graph), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(dot, scale=1.25) for dot in approx_dots], lag_ratio=0.18), run_time=1.0)
        self.play(
            Indicate(approx_dots, color=SEGMENT_COLOR, scale_factor=1.12),
            Indicate(target_dot, color=SEGMENT_COLOR, scale_factor=1.2),
        )

        def theta_for_height(y_value: float) -> float:
            if abs(y_value) < 1e-8:
                return float(np.pi)
            theta_value = float(np.arcsin(y_value))
            return theta_value if theta_value > 0 else float(np.pi - theta_value)

        other_heights = [0.85, -0.4]
        height_targets = VGroup()
        height_graph_dots = VGroup()
        for index, height in enumerate(other_heights, start=7):
            local_theta = theta_for_height(height)
            local_x = 1.0 / (local_theta + 2 * np.pi * index)
            height_targets.add(Dot(axes.c2p(0, height), radius=0.055, color=SEGMENT_COLOR))
            height_graph_dots.add(Dot(axes.c2p(local_x, height), radius=0.045, color=SEGMENT_COLOR))

        caption_4 = self.make_caption_box(
            "Étape 4. Comme la hauteur y était arbitraire, tout le segment vertical appartient à l'adhérence de A.",
            SEGMENT_COLOR,
            math=r"\overline{A}=A\cup(\{0\}\times[-1,1])",
            width=10.8,
            font_size=24,
            math_size=28,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_3, caption_4))
        self.play(LaggedStart(*[FadeIn(dot, scale=1.15) for dot in height_targets], lag_ratio=0.18))
        self.play(LaggedStart(*[FadeIn(dot, scale=1.15) for dot in height_graph_dots], lag_ratio=0.18))
        self.play(Indicate(segment, color=SEGMENT_COLOR, scale_factor=1.04))

        caption_5 = self.make_caption_box(
            "Étape 5. Or l'adhérence d'un ensemble connexe reste connexe. Donc E = Ā est connexe.",
            THEOREM_COLOR,
            width=10.8,
            font_size=24,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_4, caption_5))
        self.play(Indicate(VGroup(graph, segment), color=THEOREM_COLOR, scale_factor=1.02))
        self.wait(1.8)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ── 5. Pourquoi E n'est pas connexe par arcs ───────────────── #

    def section_non_connexite_par_arcs(self) -> None:
        title = self.make_section_title("4. Pourquoi E n'est pas connexe par arcs", WARN_COLOR, font_size=28)
        self.play(Write(title))

        axes = self.make_axes([-0.05, 3.25, 0.5], [-1.25, 1.25, 0.5], 8.0, 4.5)
        axes.shift(DOWN * 0.30)
        graph = self.make_graph(axes, 0.0014, np.pi, step=0.00008, stroke_width=2.4)
        segment = self.make_segment(axes, stroke_width=4.5)
        self.play(Create(axes), Create(graph), Create(segment), run_time=1.2)

        p_point = Dot(axes.c2p(0, 0), color=THEOREM_COLOR, radius=0.08)
        q_x = np.pi
        q_point = Dot(axes.c2p(q_x, np.sin(1 / q_x)), color=THEOREM_COLOR, radius=0.08)
        p_label = MathTex("P", font_size=24, color=THEOREM_COLOR).next_to(p_point, LEFT, buff=0.10)
        q_label = MathTex("Q", font_size=24, color=THEOREM_COLOR).next_to(q_point, UP, buff=0.10)
        self.play(FadeIn(p_point, scale=1.6), FadeIn(q_point, scale=1.6), Write(p_label), Write(q_label))

        caption_1 = self.make_caption_box(
            "Supposons, pour chercher une contradiction, qu'un chemin continu parte de Q et arrive en P.",
            WARN_COLOR,
            math=r"\gamma:[0,1]\to \overline{A},\qquad \gamma(0)=Q,\ \gamma(1)=P",
            width=10.8,
            font_size=24,
            math_size=24,
        ).to_edge(DOWN, buff=0.22)
        self.play(FadeIn(caption_1, shift=UP * 0.08), run_time=1.0)

        timeline = NumberLine(
            x_range=[0, 1, 0.25],
            length=4.8,
            include_ticks=False,
            include_numbers=False,
            color=DIM_COLOR,
            stroke_width=2,
        ).move_to(RIGHT * 3.0 + DOWN * 2.0)
        t0 = MathTex("0", font_size=18, color=DIM_COLOR).next_to(timeline.n2p(0), DOWN, buff=0.10)
        t1 = MathTex("1", font_size=18, color=DIM_COLOR).next_to(timeline.n2p(1), DOWN, buff=0.10)
        tau_dot = Dot(timeline.n2p(0.78), color=WARN_COLOR, radius=0.055)
        tau_label = MathTex(r"\tau", font_size=22, color=WARN_COLOR).next_to(tau_dot, UP, buff=0.10)
        self.play(Create(timeline), Write(t0), Write(t1), FadeIn(tau_dot), Write(tau_label))
        before_tau = Line(timeline.n2p(0.06), timeline.n2p(0.75), color=GRAPH_COLOR, stroke_width=5)
        before_tau_brace = BraceBetweenPoints(before_tau.get_start(), before_tau.get_end(), direction=UP, color=GRAPH_COLOR)
        before_tau_label = MathTex(r"t<\tau", font_size=20, color=GRAPH_COLOR).next_to(before_tau_brace, UP, buff=0.08)
        self.play(Create(before_tau), Create(before_tau_brace), Write(before_tau_label), run_time=0.8)
        self.play(Indicate(segment, color=WARN_COLOR, scale_factor=1.04))

        caption_2 = self.make_caption_box(
            "Il existe donc un premier instant τ où le chemin touche le segment. Avant τ, il reste sur la courbe A.",
            GRAPH_COLOR,
            math=r"t<\tau\Longrightarrow \gamma(t)\in A",
            width=10.8,
            font_size=24,
            math_size=26,
        ).to_edge(DOWN, buff=0.22)
        self.play(ReplacementTransform(caption_1, caption_2))

        x_value = 0.18
        x_prime = 1.0 / (1.0 / x_value + 2 * np.pi)
        gate_x = DashedLine(axes.c2p(x_value, -1.15), axes.c2p(x_value, 1.15), color=THEOREM_COLOR, dash_length=0.06)
        gate_xprime = DashedLine(axes.c2p(x_prime, -1.15), axes.c2p(x_prime, 1.15), color=THEOREM_COLOR, dash_length=0.06)
        x_label = MathTex("x", font_size=18, color=THEOREM_COLOR).next_to(gate_x, DOWN, buff=0.08)
        xprime_label = MathTex(r"x'", font_size=18, color=THEOREM_COLOR).next_to(gate_xprime, DOWN, buff=0.08)

        caption_3 = self.make_caption_box(
            "Juste avant τ, l'abscisse est toute petite, mais encore positive. Elle parcourt donc l'intervalle [x',x].",
            THEOREM_COLOR,
            math=r"x'<\gamma_x(t)<x",
            width=10.8,
            font_size=24,
            math_size=28,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_2, caption_3))
        self.play(Create(gate_x), Create(gate_xprime), Write(x_label), Write(xprime_label), run_time=0.8)

        oscillation_segment = self.make_graph(axes, x_prime, x_value, step=0.00003, stroke_width=5.0).set_color(THEOREM_COLOR)
        travel_dot = Dot(axes.c2p(x_value, np.sin(1 / x_value)), color=RUNNER_COLOR, radius=0.06)
        travel_glow = always_redraw(lambda: make_glow(travel_dot, RUNNER_COLOR, radii=(0.10, 0.18, 0.28)))

        caption_4 = self.make_caption_box(
            "Or, dans cette petite bande, la courbe refait une oscillation complète : elle monte, redescend, puis remonte.",
            THEOREM_COLOR,
            width=10.8,
            font_size=24,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_3, caption_4))
        self.play(Create(oscillation_segment), run_time=1.0)
        self.add(travel_glow, travel_dot)
        self.play(MoveAlongPath(travel_dot, oscillation_segment.copy().reverse_points()), run_time=1.8, rate_func=rate_functions.linear)
        travel_glow.clear_updaters()
        self.play(FadeOut(travel_glow), FadeOut(travel_dot))
        self.flash_oscillation_extrema(axes, 3, 8)

        alpha_value = 0.45
        alpha_theta = float(np.arcsin(alpha_value))
        alpha_x = 1.0 / (alpha_theta + 8 * 2 * np.pi)
        top_dot = Dot(axes.c2p(1.0 / (np.pi / 2 + 8 * np.pi), 1), radius=0.055, color=HIGHLIGHT_COLOR)
        bottom_dot = Dot(axes.c2p(1.0 / (3 * np.pi / 2 + 8 * np.pi), -1), radius=0.055, color=WARN_COLOR)
        alpha_dot = Dot(axes.c2p(0, alpha_value), radius=0.055, color=SEGMENT_COLOR)
        alpha_graph_dot = Dot(axes.c2p(alpha_x, alpha_value), radius=0.05, color=SEGMENT_COLOR)
        alpha_line = DashedLine(axes.c2p(0, alpha_value), axes.c2p(x_value, alpha_value), color=SEGMENT_COLOR, dash_length=0.06)
        alpha_label = MathTex(r"(0,\alpha)", font_size=18, color=SEGMENT_COLOR).next_to(alpha_dot, LEFT, buff=0.08)
        t_plus = Dot(timeline.n2p(0.67), radius=0.034, color=HIGHLIGHT_COLOR)
        t_minus = Dot(timeline.n2p(0.72), radius=0.034, color=WARN_COLOR)
        t_alpha = Dot(timeline.n2p(0.75), radius=0.034, color=SEGMENT_COLOR)

        caption_5 = self.make_caption_box(
            "On peut donc choisir des instants avant τ où la hauteur vaut 1, puis -1, puis α.",
            WARN_COLOR,
            math=r"\gamma_y(t_n^+)=1,\qquad \gamma_y(t_n^-)=-1,\qquad \gamma_y(s_n)=\alpha",
            width=10.8,
            font_size=24,
            math_size=22,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_4, caption_5))
        self.play(
            Create(alpha_line),
            FadeIn(top_dot, scale=1.2),
            FadeIn(bottom_dot, scale=1.2),
            FadeIn(alpha_dot),
            FadeIn(alpha_graph_dot),
            Write(alpha_label),
            FadeIn(t_plus, scale=1.2),
            FadeIn(t_minus, scale=1.2),
            FadeIn(t_alpha, scale=1.2),
        )
        self.play(
            Indicate(top_dot, color=HIGHLIGHT_COLOR, scale_factor=1.25),
            Indicate(bottom_dot, color=WARN_COLOR, scale_factor=1.25),
            Indicate(alpha_dot, color=SEGMENT_COLOR, scale_factor=1.25),
            Indicate(alpha_graph_dot, color=SEGMENT_COLOR, scale_factor=1.25),
        )

        caption_6 = self.make_caption_box(
            "Mais un chemin continu doit avoir une seule limite quand on arrive au temps τ. Contradiction.",
            WARN_COLOR,
            math=r"\text{Donc }\overline{A}\text{ n'est pas connexe par arcs}",
            width=10.8,
            font_size=24,
            math_size=26,
        ).to_edge(DOWN, buff=0.22)

        self.play(ReplacementTransform(caption_5, caption_6))
        self.play(
            Indicate(t_plus, color=HIGHLIGHT_COLOR),
            Indicate(t_minus, color=WARN_COLOR),
            Indicate(t_alpha, color=SEGMENT_COLOR),
        )
        self.wait(2.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])

    # ── 6. Bilan ────────────────────────────────────────────────── #

    def section_bilan(self) -> None:
        title = title_text("Bilan", color=THEOREM_COLOR)
        self.play(Write(title))

        line_1 = MathTex(
            r"\text{connexe par arcs} \Longrightarrow \text{connexe}",
            font_size=34,
            color=GRAPH_COLOR,
        )
        line_2 = MathTex(
            r"\text{connexe} \not\!\Longrightarrow \text{connexe par arcs}",
            font_size=34,
            color=WARN_COLOR,
        )
        example = MathTex(
            r"E = \left\{\left(x,\sin\!\left(\frac{1}{x}\right)\right):x>0\right\}"
            r"\cup \bigl(\{0\}\times[-1,1]\bigr)",
            font_size=25,
            color=TEXT_COLOR,
        )
        summary = Text(
            "Le segment vertical complète l'adhérence, mais il ne crée aucun chemin continu vers le graphe.",
            font_size=24,
            color=DIM_COLOR,
            line_spacing=0.95,
        )

        block = VGroup(line_1, line_2, example, summary).arrange(
            DOWN,
            buff=0.42,
        ).move_to(ORIGIN + DOWN * 0.2)

        box_1 = SurroundingRectangle(line_1, color=GRAPH_COLOR, buff=0.15)
        box_2 = SurroundingRectangle(line_2, color=WARN_COLOR, buff=0.15)

        self.play(Write(line_1), Create(box_1), run_time=1.4)
        self.wait(0.6)
        self.play(Write(line_2), Create(box_2), run_time=1.4)
        self.wait(0.6)
        self.play(FadeIn(example, shift=UP * 0.12))
        self.play(FadeIn(summary, shift=UP * 0.12))
        self.wait(3.0)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
