# -*- coding: utf-8 -*-
"""Contre-exemple classique : connexe ne signifie pas connexe par arcs.

Style 3Blue1Brown : caméra mobile, narration visuelle progressive,
point lumineux parcourant la courbe, argument du « coureur topologique ».
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
    Scene,
    ParametricFunction,
    Rectangle,
    ShowPassingFlash,
    SurroundingRectangle,
    Text,
    TracedPath,
    TransformFromCopy,
    Transform,
    VGroup,
    VMobject,
    Write,
    always_redraw,
    rate_functions,
    DOWN,
    LEFT,
    ORIGIN,
    RIGHT,
    UP,
    UL,
    DR,
    YELLOW,
)

from src.config import DEFAULT_WAIT, SHORT_WAIT
from src.objects.presentation import make_glow
from src.utils.colors import (
    CLOSED_SET_COLOR,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    TEXT_COLOR,
)

GRAPH_COLOR = OPEN_SET_COLOR
SEGMENT_COLOR = "#4CC9F0"
PATH_COLOR = "#FFD166"
WARN_COLOR = CLOSED_SET_COLOR
RUNNER_COLOR = "#F72585"


class ContreExempleSin1x(Scene):
    """Contre-exemple sin(1/x) — style 3Blue1Brown.

    Sections :
    1. Titre + question
    2. Construction progressive du graphe (point lumineux)
    3. Zoom caméra vers x = 0 (oscillations infinies)
    4. Pourquoi E est connexe (adhérence d'un connexe par arcs)
    5. Le coureur topologique (pourquoi pas connexe par arcs)
    6. Bilan encadré
    """

    def construct(self):
        self.section_titre()
        self.section_construction()
        self.section_zoom_camera()
        self.section_connexe()
        self.section_coureur()
        self.section_bilan()

    # ── helpers ──────────────────────────────────────────────────── #

    def make_axes(self, x_range, y_range, x_length, y_length) -> Axes:
        return Axes(
            x_range=x_range,
            y_range=y_range,
            x_length=x_length,
            y_length=y_length,
            axis_config={"color": DIM_COLOR, "stroke_width": 1.4, "include_ticks": False},
            tips=False,
        )

    def make_graph(self, axes: Axes, x_min: float, x_max: float, step: float = 0.0007):
        return axes.plot(
            lambda x: np.sin(1 / x),
            x_range=[x_min, x_max, step],
            color=GRAPH_COLOR,
            stroke_width=2.5,
        )

    def make_segment(self, axes: Axes) -> Line:
        return Line(
            axes.c2p(0, -1), axes.c2p(0, 1),
            color=SEGMENT_COLOR, stroke_width=5,
        )

    # ── 1. Titre ─────────────────────────────────────────────────── #

    def section_titre(self) -> None:
        question = Text(
            "Un espace connexe est-il toujours connexe par arcs ?",
            font_size=38,
        )
        self.play(Write(question), run_time=2)
        self.wait(1.5)

        non = Text("Pas nécessairement.", font_size=44, color=WARN_COLOR)
        non.next_to(question, DOWN, buff=0.5)
        self.play(FadeIn(non, shift=UP * 0.2))
        self.wait(1)

        formule = MathTex(
            r"E \;=\; \bigl\{\bigl(x,\,\sin\tfrac{1}{x}\bigr) : x > 0\bigr\}"
            r"\;\cup\; \{0\}\times[-1,1]",
            font_size=30, color=TEXT_COLOR,
        ).next_to(non, DOWN, buff=0.6)
        self.play(Write(formule), run_time=2)
        self.wait(2)
        self.play(FadeOut(question), FadeOut(non), FadeOut(formule))

    # ── 2. Construction progressive du graphe ────────────────────── #

    def section_construction(self) -> None:
        # Grands axes centrés
        axes = self.make_axes([-0.3, 3.0, 0.5], [-1.5, 1.5, 0.5], 11, 5.5)
        axes.shift(DOWN * 0.2)

        # Labels axes
        x_lab = MathTex("x", font_size=22, color=DIM_COLOR).next_to(axes.x_axis, DR, buff=0.1)
        y_lab = MathTex("y", font_size=22, color=DIM_COLOR).next_to(axes.y_axis, UL, buff=0.1)

        self.play(Create(axes, run_time=1.2), Write(x_lab), Write(y_lab))

        # Segment vertical en premier (cible mystérieuse)
        segment = self.make_segment(axes)
        seg_label = MathTex(
            r"\{0\}\times[-1,1]", font_size=22, color=SEGMENT_COLOR,
        ).next_to(segment, LEFT, buff=0.25)
        self.play(Create(segment, run_time=1.5), Write(seg_label))
        self.wait(0.5)

        # Graphe : construit progressivement avec un point lumineux
        # On trace depuis la droite (x large) vers la gauche (x petit)
        graph = self.make_graph(axes, 0.015, 2.8, step=0.0008)

        # Point mobile lumineux
        runner = Dot(color=PATH_COLOR, radius=0.07)
        runner.move_to(graph.get_end())  # commence à droite
        glow = always_redraw(lambda: make_glow(runner, PATH_COLOR))
        trace = TracedPath(
            runner.get_center,
            stroke_color=GRAPH_COLOR, stroke_width=2.8, stroke_opacity=0.85,
        )

        graph_label = MathTex(
            r"y = \sin\!\left(\frac{1}{x}\right)",
            font_size=26, color=GRAPH_COLOR,
        ).move_to(axes.c2p(1.8, 1.2))

        self.add(trace, glow, runner)
        # Parcours de droite à gauche (on inverse le graphe)
        reversed_graph = graph.copy().reverse_points()
        self.play(
            MoveAlongPath(runner, reversed_graph),
            run_time=5, rate_func=rate_functions.linear,
        )
        self.play(Write(graph_label))

        note = Text(
            "Plus on s'approche de 0, plus le graphe oscille frénétiquement.",
            font_size=21, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(note, shift=UP * 0.1))
        self.wait(2)

        # Garder en mémoire pour la section suivante
        self.main_axes = axes
        self.main_graph = graph
        self.main_segment = segment
        self.to_clear = [
            axes, x_lab, y_lab, segment, seg_label,
            graph_label, note, trace, glow, runner,
        ]

    # ── 3. Zoom vers x = 0 (nouveaux axes dédiés) ──────────────── #

    def section_zoom_camera(self) -> None:
        # Encadrer la zone de zoom sur la vue globale
        axes = self.main_axes
        focus_box = Rectangle(
            width=axes.c2p(0.25, 0)[0] - axes.c2p(0, 0)[0],
            height=axes.c2p(0, 1.1)[1] - axes.c2p(0, -1.1)[1],
            stroke_color=HIGHLIGHT_COLOR, stroke_width=2, fill_opacity=0,
        ).move_to(axes.c2p(0.12, 0))

        zoom_text = Text("Zoomons ici...", font_size=24, color=HIGHLIGHT_COLOR)
        zoom_text.next_to(focus_box, UP, buff=0.15)

        self.play(Create(focus_box), FadeIn(zoom_text, shift=UP * 0.1))
        self.wait(1)

        # Transition : tout disparaît
        self.play(*[FadeOut(m) for m in self.mobjects])

        # ── Zoom niveau 1 : x ∈ [0, 0.3] ──
        z1_title = Text(
            "x entre 0 et 0.3", font_size=24, color=HIGHLIGHT_COLOR,
        ).to_edge(UP, buff=0.4)

        z1_axes = self.make_axes([-0.01, 0.32, 0.05], [-1.3, 1.3, 0.5], 11, 5)
        z1_axes.shift(DOWN * 0.2)
        z1_graph = self.make_graph(z1_axes, 0.004, 0.32, step=0.0002)
        z1_seg = self.make_segment(z1_axes)

        self.play(Write(z1_title))
        self.play(Create(z1_axes, run_time=0.6), Create(z1_graph, run_time=1.5), Create(z1_seg))
        self.wait(1.5)

        # Accolade montrant l'amplitude = 2
        # Trouver un sommet dans cette fenêtre
        k_z1 = 3
        x_top_z1 = 1.0 / (np.pi / 2 + 2 * np.pi * k_z1)  # ≈ 0.049
        brace1 = BraceBetweenPoints(
            z1_axes.c2p(x_top_z1 + 0.005, -1),
            z1_axes.c2p(x_top_z1 + 0.005, 1),
            direction=RIGHT, color=HIGHLIGHT_COLOR,
        )
        brace1_label = MathTex(
            r"\text{amplitude} = 2", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(brace1, RIGHT, buff=0.15)

        self.play(Create(brace1), Write(brace1_label))
        self.wait(1.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # ── Zoom niveau 2 : x ∈ [0, 0.06] ──
        z2_title = Text(
            "x entre 0 et 0.06", font_size=24, color=HIGHLIGHT_COLOR,
        ).to_edge(UP, buff=0.4)

        z2_axes = self.make_axes([-0.002, 0.065, 0.01], [-1.3, 1.3, 0.5], 11, 5)
        z2_axes.shift(DOWN * 0.2)
        z2_graph = self.make_graph(z2_axes, 0.001, 0.065, step=0.00005)
        z2_seg = self.make_segment(z2_axes)

        self.play(Write(z2_title))
        self.play(Create(z2_axes, run_time=0.6), Create(z2_graph, run_time=1.5), Create(z2_seg))

        comment = Text(
            "On a beau zoomer, on voit toujours le même dessin !",
            font_size=22, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(comment, shift=UP * 0.1))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── 4. Pourquoi E est connexe ────────────────────────────────── #

    def section_connexe(self) -> None:
        titre = Text("Pourquoi E est connexe", font_size=36, color=GRAPH_COLOR)
        titre.to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # Graphe à gauche — propre, sans surcharge
        axes = self.make_axes([-0.01, 0.5, 0.1], [-1.3, 1.3, 0.5], 5.5, 3.8)
        axes.to_edge(LEFT, buff=0.6).shift(DOWN * 0.3)
        graph = self.make_graph(axes, 0.005, 0.5, step=0.0003)
        segment = self.make_segment(axes)

        g_label = MathTex("G", font_size=24, color=GRAPH_COLOR).move_to(axes.c2p(0.35, 1.1))
        s_label = MathTex("S", font_size=24, color=SEGMENT_COLOR).next_to(segment, LEFT, buff=0.15)

        self.play(Create(axes), run_time=0.8)
        self.play(Create(graph, run_time=1.5), Write(g_label))
        self.play(Create(segment, run_time=1), Write(s_label))

        # Animation : flash lumineux le long du graphe qui montre
        # que les oscillations s'accumulent contre le segment
        self.play(
            ShowPassingFlash(
                graph.copy().set_color(HIGHLIGHT_COLOR).set_stroke(width=6),
                time_width=0.4,
            ),
            run_time=2,
        )
        # Puis le segment pulse pour montrer qu'il est dans l'adhérence
        self.play(
            Indicate(segment, color=HIGHLIGHT_COLOR, scale_factor=1.05),
            run_time=1.2,
        )

        # Preuve à droite — concise
        proof = VGroup(
            MathTex(r"G", r"\text{ est connexe par arcs}", font_size=24),
            MathTex(
                r"\text{(image continue de } ]0,+\infty[\text{)}",
                font_size=20, color=DIM_COLOR,
            ),
            MathTex(r"S", r"\;\subset\; \overline{G}", font_size=24),
            MathTex(
                r"\text{(les oscillations s'accumulent sur } S \text{)}",
                font_size=20, color=DIM_COLOR,
            ),
            MathTex(r"G \;\subset\; E \;\subset\; \overline{G}", font_size=24),
            MathTex(
                r"\overline{G} \text{ est connexe}",
                font_size=24, color=TEXT_COLOR,
            ),
            MathTex(
                r"\Longrightarrow\; E \text{ est connexe}",
                font_size=28, color=HIGHLIGHT_COLOR,
            ),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        proof.to_edge(RIGHT, buff=0.5).shift(DOWN * 0.15)

        # Colorer G et S dans la preuve
        proof[0][0].set_color(GRAPH_COLOR)
        proof[2][0].set_color(SEGMENT_COLOR)

        for line in proof:
            self.play(Write(line), run_time=0.9)
            self.wait(0.35)

        box = SurroundingRectangle(proof[-1], color=HIGHLIGHT_COLOR, buff=0.12)
        self.play(Create(box))
        self.wait(2)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── 5. Le coureur topologique ────────────────────────────────── #

    def section_coureur(self) -> None:
        titre = Text(
            "Pourquoi E n'est pas connexe par arcs",
            font_size=36, color=WARN_COLOR,
        )
        titre.to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # Setup : axes + graphe + segment
        axes = self.make_axes([-0.02, 0.8, 0.1], [-1.3, 1.3, 0.5], 10, 5)
        axes.shift(DOWN * 0.2)
        graph = self.make_graph(axes, 0.008, 0.8, step=0.0004)
        segment = self.make_segment(axes)

        self.play(Create(axes), Create(graph), Create(segment), run_time=1.5)

        # Point P sur le segment, point Q sur le graphe
        P = Dot(axes.c2p(0, 0.5), color=HIGHLIGHT_COLOR, radius=0.08)
        Q = Dot(axes.c2p(0.6, np.sin(1 / 0.6)), color=HIGHLIGHT_COLOR, radius=0.08)
        P_lab = MathTex("P", font_size=24, color=HIGHLIGHT_COLOR).next_to(P, LEFT, buff=0.12)
        Q_lab = MathTex("Q", font_size=24, color=HIGHLIGHT_COLOR).next_to(Q, UP, buff=0.12)

        self.play(FadeIn(P, scale=1.5), FadeIn(Q, scale=1.5), Write(P_lab), Write(Q_lab))

        # Question
        question = MathTex(
            r"\exists\, \gamma : [0,1] \to E \text{ continue reliant } Q \text{ à } P \;?",
            font_size=24, color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.6)
        self.play(Write(question))
        self.wait(1)

        # Le coureur : un point qui part de Q et essaie de rejoindre P
        # Il longe le graphe vers la gauche
        runner_path_graph = axes.plot(
            lambda x: np.sin(1 / x),
            x_range=[0.03, 0.6, 0.0004],
            color=RUNNER_COLOR,
            stroke_width=0,  # invisible, juste pour le chemin
        )
        # Inverser pour aller de droite à gauche
        runner_path_reversed = runner_path_graph.copy().reverse_points()

        runner = Dot(color=RUNNER_COLOR, radius=0.07)
        runner.move_to(Q.get_center())
        runner_glow = always_redraw(lambda: make_glow(runner, RUNNER_COLOR, radii=(0.12, 0.22, 0.35)))
        runner_trace = TracedPath(
            runner.get_center,
            stroke_color=RUNNER_COLOR, stroke_width=3, stroke_opacity=0.6,
        )

        runner_label = Text("γ(t)", font_size=18, color=RUNNER_COLOR)
        runner_label.add_updater(lambda m: m.next_to(runner, UP, buff=0.1))

        self.add(runner_trace, runner_glow, runner)
        self.add(runner_label)

        # Parcourt le graphe vers la gauche — de plus en plus vite, oscillations violentes
        self.play(
            MoveAlongPath(runner, runner_path_reversed),
            run_time=5, rate_func=rate_functions.linear,
        )
        self.wait(0.5)

        # Le coureur est bloqué : il oscille sans cesse entre +1 et -1
        # Marquer les oscillations
        osc_text = Text(
            "Le coureur oscille indéfiniment entre +1 et -1...",
            font_size=22, color=WARN_COLOR,
        ).next_to(question, UP, buff=0.2)
        self.play(FadeIn(osc_text, shift=UP * 0.1))

        # Flash sur les extrêmes
        for k in range(3, 7):
            x_top = 1.0 / (np.pi / 2 + 2 * np.pi * k)
            x_bot = 1.0 / (3 * np.pi / 2 + 2 * np.pi * k)
            self.play(
                Flash(axes.c2p(x_top, 1), color=HIGHLIGHT_COLOR, line_length=0.12, run_time=0.3),
                Flash(axes.c2p(x_bot, -1), color=WARN_COLOR, line_length=0.12, run_time=0.3),
            )

        self.wait(1)

        # Argument mathématique
        runner_label.clear_updaters()
        self.play(FadeOut(runner_label), FadeOut(runner_trace), FadeOut(runner_glow), FadeOut(runner))
        self.play(FadeOut(osc_text))

        argument = VGroup(
            MathTex(
                r"\text{Si } \gamma : [0,1] \to E \text{ est un chemin de } Q \text{ à } P,",
                font_size=22,
            ),
            MathTex(
                r"\text{posons } \tau = \inf\{t : \gamma(t) \in S\}.",
                font_size=22,
            ),
            MathTex(
                r"\text{Quand } t \nearrow \tau,\; "
                r"\text{la coordonnée } x(t) \to 0",
                font_size=22,
            ),
            MathTex(
                r"\text{mais } \sin\!\bigl(\tfrac{1}{x(t)}\bigr) "
                r"\text{ oscille entre } {-1} \text{ et } {+1}",
                font_size=22, color=WARN_COLOR,
            ),
            MathTex(
                r"\Longrightarrow\; \gamma \text{ n'admet pas de limite en } \tau",
                font_size=22, color=WARN_COLOR,
            ),
            MathTex(
                r"\text{Contradiction avec la continuité de } \gamma.",
                font_size=24, color=WARN_COLOR,
            ),
        ).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
        argument.next_to(question, UP, buff=0.25)

        for line in argument:
            self.play(Write(line), run_time=1)
            self.wait(0.5)

        box = SurroundingRectangle(argument[-1], color=WARN_COLOR, buff=0.1)
        self.play(Create(box))
        self.wait(2.5)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── 6. Bilan ─────────────────────────────────────────────────── #

    def section_bilan(self) -> None:
        line1 = MathTex(
            r"\text{Connexe par arcs}",
            r"\;\Longrightarrow\;",
            r"\text{Connexe}",
            font_size=34,
        )
        line1[0].set_color(GRAPH_COLOR)
        line1[2].set_color(GRAPH_COLOR)

        line2 = MathTex(
            r"\text{Connexe}",
            r"\;\not\!\Longrightarrow\;",
            r"\text{Connexe par arcs}",
            font_size=34,
        )
        line2[0].set_color(WARN_COLOR)
        line2[2].set_color(WARN_COLOR)

        counter = MathTex(
            r"E = \text{graphe}\bigl(\sin(1/x)\bigr) \cup \{0\}\times[-1,1]",
            font_size=26, color=TEXT_COLOR,
        )

        rescue = MathTex(
            r"\text{Mais : complet + connexe + localement connexe par arcs}"
            r"\;\Longrightarrow\; \text{connexe par arcs}",
            font_size=22, color=DIM_COLOR,
        )

        bilan = VGroup(line1, line2, counter, rescue).arrange(DOWN, buff=0.5)
        bilan.move_to(ORIGIN)

        box1 = SurroundingRectangle(line1, color=GRAPH_COLOR, buff=0.15, stroke_width=1.5)
        box2 = SurroundingRectangle(line2, color=WARN_COLOR, buff=0.15, stroke_width=1.5)

        self.play(Write(line1), Create(box1), run_time=1.5)
        self.wait(0.8)
        self.play(Write(line2), Create(box2), run_time=1.5)
        self.wait(0.8)
        self.play(FadeIn(counter, shift=UP * 0.15))
        self.wait(1)
        self.play(FadeIn(rescue, shift=UP * 0.1))
        self.wait(3)

        self.play(*[FadeOut(m) for m in self.mobjects])
