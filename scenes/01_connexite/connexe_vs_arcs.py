# -*- coding: utf-8 -*-
"""Connexité et connexité par arcs.

Cette scène suit fidèlement le chapitre IV (Connexité) du cours
Le Roux / Klopp — *Mémo de topologie*, SU 3M260, 2021.

Notation et terminologie alignées sur le cours :

* un *chemin* dans X joignant x_0 à x_1 est une application continue
  γ : [0,1] → X telle que γ(0) = x_0 et γ(1) = x_1 (§ IV.1.(a)) ;
* X est *connexe par arcs* si pour tout couple (x_0, x_1), un tel
  chemin existe ;
* X est *connexe* si ∅ et X sont les seules parties à la fois
  ouvertes et fermées de X (§ IV.1.(c)) ;
* la partition d'un espace non connexe est notée X = O ⊔ O' ;
* la caractérisation par les fonctions vers {0,1} (§ IV.1.(c),
  exercice 88) précède le corollaire « connexe par arcs ⟹ connexe »
  qui se démontre par contraposition (recette du cours).

Style visuel inspiré de 3Blue1Brown : schémas centraux grands et
persistants, ligne d'étape unique en bas qui transforme à chaque
temps fort, animations ciblées (Indicate, Flash, Circumscribe,
TracedPath, glow halos) synchronisées avec les arguments.
"""

from __future__ import annotations

import numpy as np
from manim import (
    Arrow,
    Circle,
    Circumscribe,
    Create,
    DashedLine,
    DashedVMobject,
    Dot,
    Ellipse,
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
    Scene,
    SurroundingRectangle,
    Text,
    TracedPath,
    Transform,
    VGroup,
    Write,
    always_redraw,
    rate_functions,
    DL,
    DOWN,
    DR,
    LEFT,
    RIGHT,
    UL,
    UP,
    UR,
)

from src.config import DEFAULT_WAIT
from src.objects.presentation import make_glow
from src.utils.colors import (
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    PATH_COLOR,
    TEXT_COLOR,
)


# ── Couleurs sémantiques locales ─────────────────────────────────── #
# Notation du cours : O et O' désignent les deux ouverts d'une
# partition non triviale d'un espace métrique non connexe (§ IV.1.(c)).
O_COLOR = OPEN_SET_COLOR        # ouvert O
O_PRIME_COLOR = "#4361EE"       # ouvert O' (bleu profond)
RUNNER_COLOR = "#FFD166"        # point lumineux qui parcourt γ
WARN_COLOR = "#EF476F"          # alerte / contradiction


class ConnexeVsArcs(Scene):
    """Suit le chapitre IV (Connexité) du cours Le Roux/Klopp 3M260 2021.

    Plan, dans l'ordre exact du cours :

        1. Ouverture — pose la question fondamentale.
        2. Connexité par arcs (§ IV.1.(a)) — chemin γ : [0,1] → X,
           définition, exemple ℝⁿ avec γ(t) = (1-t)x_0 + t x_1,
           Proposition IV.1 (image continue) et concaténation.
        3. Connexité (§ IV.1.(c)) — définition primaire par les
           ouverts-fermés ; proposition équivalente : X non connexe
           ⟺ ∃ partition X = O ⊔ O' en deux ouverts non vides.
        4. Caractérisation par les applications vers {0,1}
           (§ IV.1.(c), via l'exercice 88 sur les applications
           localement constantes) ; corollaire : [0,1] est connexe.
        5. Corollaire : connexe par arcs ⟹ connexe — démonstration
           par contraposition selon la recette du cours.
        6. Et la réciproque ? — contre-exemple sin(1/x), théorème
           de relais (§ IV.2.(a)) : tout métrique complet, connexe,
           localement connexe est connexe par arcs.
    """

    def construct(self) -> None:
        self.section_ouverture()
        self.section_connexite_par_arcs()
        self.section_connexite()
        self.section_caracterisation()
        self.section_implication()
        self.section_reciproque()

    # ── 1. Ouverture ──────────────────────────────────────────────── #

    def section_ouverture(self) -> None:
        """Pose la question intuitive et révèle le titre."""

        question = Text(
            "Que veut dire qu'un espace est « d'un seul tenant » ?",
            font_size=32,
            color=TEXT_COLOR,
        )
        self.play(Write(question), run_time=2)
        self.wait(1.2)

        # Les deux candidats sémantiques
        bullet_path = Text(
            "•  on peut joindre deux points par un chemin continu",
            font_size=22,
            color=PATH_COLOR,
        )
        bullet_open = Text(
            "•  on ne peut pas le découper en deux ouverts disjoints",
            font_size=22,
            color=OPEN_SET_COLOR,
        )
        bullets = VGroup(bullet_path, bullet_open).arrange(
            DOWN, buff=0.32, aligned_edge=LEFT,
        )
        bullets.next_to(question, DOWN, buff=0.55)

        self.play(FadeIn(bullet_path, shift=UP * 0.15))
        self.wait(0.7)
        self.play(FadeIn(bullet_open, shift=UP * 0.15))
        self.wait(1.2)

        # Annonce du titre
        titre = Text(
            "Connexité  vs  connexité par arcs",
            font_size=42,
            color=HIGHLIGHT_COLOR,
        )
        sous_titre = Text(
            "Deux formalisations d'une même intuition — et le théorème qui les relie",
            font_size=22,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.32)

        self.play(
            FadeOut(question, shift=UP * 0.4),
            FadeOut(bullets, shift=UP * 0.4),
            run_time=1.0,
        )
        self.play(Write(titre), run_time=1.5)
        self.play(FadeIn(sous_titre, shift=UP * 0.15))
        self.wait(DEFAULT_WAIT * 1.6)
        self.play(FadeOut(titre), FadeOut(sous_titre))

    # ── 2. Connexité par arcs (§ IV.1.(a)) ────────────────────────── #

    def section_connexite_par_arcs(self) -> None:
        """Définition du cours, runner sur γ, exemples ℝᴺ et intervalles.

        Suit § IV.1.(a) : un chemin dans X joignant x_0 à x_1 est une
        application continue γ : [0,1] → X telle que γ(0) = x_0 et
        γ(1) = x_1. X est connexe par arcs si pour tout couple (x_0, x_1)
        un tel chemin existe.

        Mentionne :
            * la formule γ(t) = (1-t)x_0 + tx_1 dans ℝᴺ ;
            * la Proposition IV.1 (image continue, réunion, produit) ;
            * la concaténation γ ⋆ γ' (mise bout à bout).
        """

        titre = Text("1.  Connexité par arcs", font_size=34, color=PATH_COLOR)
        titre.to_edge(UP, buff=0.45)
        self.play(Write(titre))

        intuition = Text(
            "Tout couple de points de X peut être joint par un chemin continu.",
            font_size=22,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.3)
        self.play(FadeIn(intuition, shift=UP * 0.12))
        self.wait(0.6)

        # Espace X : ellipse souple, fond doux
        space = Ellipse(
            width=6.4, height=3.6,
            color=OPEN_SET_COLOR, stroke_width=2.4,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.10,
        ).shift(DOWN * 0.6)
        x_label_X = MathTex("X", font_size=30, color=OPEN_SET_COLOR).move_to(
            space.get_corner(UR) + DL * 0.35,
        )
        self.play(Create(space, run_time=1.2), Write(x_label_X))

        # Deux points distincts dans X — notation du cours : x_0 et x_1
        x0_pt = space.get_center() + np.array([-2.0, -0.5, 0])
        x1_pt = space.get_center() + np.array([2.1, 0.5, 0])
        x0_dot = Dot(x0_pt, color=HIGHLIGHT_COLOR, radius=0.085)
        x1_dot = Dot(x1_pt, color=HIGHLIGHT_COLOR, radius=0.085)
        x0_lab = MathTex("x_0", font_size=28, color=HIGHLIGHT_COLOR).next_to(
            x0_dot, DL, buff=0.08,
        )
        x1_lab = MathTex("x_1", font_size=28, color=HIGHLIGHT_COLOR).next_to(
            x1_dot, UR, buff=0.08,
        )
        self.play(
            FadeIn(x0_dot, scale=2.0),
            FadeIn(x1_dot, scale=2.0),
            Write(x0_lab),
            Write(x1_lab),
        )
        self.wait(0.4)

        # Le chemin γ : segment dévié par une oscillation douce
        def gamma(t: float) -> np.ndarray:
            base = (1.0 - t) * x0_pt + t * x1_pt
            wobble = np.array([
                0.0,
                0.7 * np.sin(np.pi * t) - 0.25 * np.sin(2 * np.pi * t),
                0.0,
            ])
            return base + wobble

        path = ParametricFunction(
            gamma,
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=4,
        )

        # Runner lumineux qui parcourt γ et laisse une trace
        runner = Dot(color=RUNNER_COLOR, radius=0.075).move_to(x0_pt)
        runner_glow = always_redraw(
            lambda: make_glow(runner, RUNNER_COLOR, radii=(0.14, 0.24, 0.38)),
        )
        runner_trace = TracedPath(
            runner.get_center,
            stroke_color=PATH_COLOR,
            stroke_width=4,
            stroke_opacity=0.95,
        )
        gamma_tag = MathTex(r"\gamma(t)", font_size=24, color=PATH_COLOR)
        gamma_tag.add_updater(lambda m: m.next_to(runner, UP, buff=0.16))

        self.add(runner_trace, runner_glow, runner, gamma_tag)
        self.play(
            MoveAlongPath(runner, path),
            run_time=2.8,
            rate_func=rate_functions.smooth,
        )
        gamma_tag.clear_updaters()
        runner_glow.clear_updaters()
        self.wait(0.4)
        self.play(FadeOut(gamma_tag))

        # Définition formelle du cours (§ IV.1.(a)) — en remplacement de l'intuition
        self.play(FadeOut(intuition))
        definition = VGroup(
            MathTex(
                r"\text{Un \emph{chemin} de } x_0 \text{ à } x_1 \text{ dans } X"
                r" : \text{ application continue } \gamma : [0,1] \to X",
                font_size=22,
            ),
            MathTex(
                r"\text{telle que } \gamma(0) = x_0 \text{ et } \gamma(1) = x_1.",
                font_size=22,
            ),
            MathTex(
                r"X \text{ \emph{connexe par arcs}}",
                r"\;\Longleftrightarrow\;",
                r"\forall\, x_0, x_1 \in X,\; \exists \text{ un tel chemin}.",
                font_size=22,
            ),
        ).arrange(DOWN, buff=0.18, aligned_edge=LEFT).next_to(titre, DOWN, buff=0.28)
        definition[2][0].set_color(PATH_COLOR)
        self.play(Write(definition[0]), run_time=1.4)
        self.play(Write(definition[1]), run_time=1.0)
        self.play(Write(definition[2]), run_time=1.6)
        self.wait(1.0)

        # Exemple : ℝᴺ via la combinaison affine du cours
        exemple = MathTex(
            r"\text{Dans } \mathbb{R}^N : \;\;",
            r"\gamma : t \mapsto (1-t)\,x_0 + t\,x_1",
            r"\;\;\text{convient.}",
            font_size=24,
            color=TEXT_COLOR,
        )
        exemple[1].set_color(PATH_COLOR)
        exemple.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(exemple, shift=UP * 0.15))

        # Petit flash d'emphase sur le runner et le chemin
        self.play(
            Indicate(runner, color=HIGHLIGHT_COLOR, scale_factor=1.4),
            Flash(
                runner.get_center(),
                color=RUNNER_COLOR,
                line_length=0.18,
                num_lines=12,
            ),
        )
        self.wait(2.0)

        self.play(*[FadeOut(m) for m in self.mobjects])

        # ── Compléments visuels : Proposition IV.1 + concaténation ───
        # Cinq sub-frames distincts, chacun avec un schéma central et un
        # énoncé court — un par item du cours.
        self._subframe_image_continue()
        self._subframe_reunion_point_commun()
        self._subframe_produit_fini()
        self._subframe_concatenation()
        self._subframe_invariance_topologique()

    # ── Sub-frames de la Proposition IV.1 et concaténation ─────────── #

    def _subframe_image_continue(self) -> None:
        """Sub-frame : image continue d'un c.p.a. est c.p.a."""
        titre = Text(
            "Proposition IV.1 — image continue",
            font_size=30, color=PATH_COLOR,
        ).to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # X (gauche) — un blob c.p.a.
        x_space = Ellipse(
            width=4.4, height=2.6,
            color=OPEN_SET_COLOR, stroke_width=3,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.16,
        ).move_to(np.array([-3.6, 0.0, 0]))
        x_space_lab = MathTex(
            "X", font_size=32, color=OPEN_SET_COLOR,
        ).next_to(x_space, UP, buff=0.15)

        x0_in_X = x_space.get_center() + np.array([-1.4, -0.4, 0])
        x1_in_X = x_space.get_center() + np.array([1.4, 0.4, 0])
        x0_dot_in = Dot(x0_in_X, color=HIGHLIGHT_COLOR, radius=0.08)
        x1_dot_in = Dot(x1_in_X, color=HIGHLIGHT_COLOR, radius=0.08)
        x0_lab_in = MathTex("x_0", font_size=24, color=HIGHLIGHT_COLOR).next_to(
            x0_dot_in, DL, buff=0.08,
        )
        x1_lab_in = MathTex("x_1", font_size=24, color=HIGHLIGHT_COLOR).next_to(
            x1_dot_in, UR, buff=0.08,
        )

        def gamma_in_X(t: float) -> np.ndarray:
            base = (1 - t) * x0_in_X + t * x1_in_X
            wobble = np.array([0, 0.45 * np.sin(np.pi * t), 0])
            return base + wobble

        gamma_curve = ParametricFunction(
            gamma_in_X, t_range=[0, 1],
            color=PATH_COLOR, stroke_width=3.5,
        )
        gamma_label_in = MathTex(
            r"\gamma", font_size=22, color=PATH_COLOR,
        ).next_to(gamma_curve.point_from_proportion(0.5), UP, buff=0.08)

        # Y (droite) — l'image
        y_space = Ellipse(
            width=4.4, height=2.6,
            color=OPEN_SET_COLOR, stroke_width=3,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.10,
        ).move_to(np.array([3.6, 0.0, 0]))
        y_space_lab = MathTex(
            "Y", font_size=32, color=OPEN_SET_COLOR,
        ).next_to(y_space, UP, buff=0.15)

        fx0_in_Y = y_space.get_center() + np.array([-1.0, 0.6, 0])
        fx1_in_Y = y_space.get_center() + np.array([1.2, -0.5, 0])
        fx0_dot_in = Dot(fx0_in_Y, color=HIGHLIGHT_COLOR, radius=0.08)
        fx1_dot_in = Dot(fx1_in_Y, color=HIGHLIGHT_COLOR, radius=0.08)
        fx0_lab_in = MathTex(
            r"f(x_0)", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(fx0_dot_in, UL, buff=0.08)
        fx1_lab_in = MathTex(
            r"f(x_1)", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(fx1_dot_in, DR, buff=0.08)

        def fgamma_in_Y(t: float) -> np.ndarray:
            base = (1 - t) * fx0_in_Y + t * fx1_in_Y
            wobble = np.array([0.3 * np.sin(2 * np.pi * t), 0.35 * np.sin(np.pi * t), 0])
            return base + wobble

        fgamma_curve = ParametricFunction(
            fgamma_in_Y, t_range=[0, 1],
            color=PATH_COLOR, stroke_width=3.5,
        )
        fgamma_label = MathTex(
            r"f \circ \gamma", font_size=22, color=PATH_COLOR,
        ).next_to(fgamma_curve.point_from_proportion(0.5), UP, buff=0.10)

        f_arrow = Arrow(
            x_space.get_right() + RIGHT * 0.10,
            y_space.get_left() + LEFT * 0.10,
            color=DIM_COLOR, buff=0.05, stroke_width=4,
        )
        f_arrow_lab = MathTex(
            "f", font_size=28, color=TEXT_COLOR,
        ).next_to(f_arrow, UP, buff=0.10)

        # Animation
        self.play(
            Create(x_space), Write(x_space_lab),
            Create(y_space), Write(y_space_lab),
        )
        self.play(
            FadeIn(x0_dot_in, scale=1.5), FadeIn(x1_dot_in, scale=1.5),
            Write(x0_lab_in), Write(x1_lab_in),
        )
        self.play(Create(gamma_curve), Write(gamma_label_in), run_time=1.8)
        self.play(Create(f_arrow), Write(f_arrow_lab))
        self.play(
            FadeIn(fx0_dot_in, scale=1.5), FadeIn(fx1_dot_in, scale=1.5),
            Write(fx0_lab_in), Write(fx1_lab_in),
        )
        self.play(Create(fgamma_curve), Write(fgamma_label), run_time=1.8)

        enonce = MathTex(
            r"f \text{ continue,}\; X \text{ c.p.a.} \;\Longrightarrow\;",
            r"f(X) \text{ est c.p.a. (le chemin } f \circ \gamma \text{ convient)}",
            font_size=24,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.45)
        enonce[1].set_color(HIGHLIGHT_COLOR)
        self.play(Write(enonce), run_time=2.0)
        self.wait(2.4)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _subframe_reunion_point_commun(self) -> None:
        """Sub-frame : réunion de c.p.a. ayant un point commun."""
        titre = Text(
            "Proposition IV.1 — réunion (point commun)",
            font_size=30, color=PATH_COLOR,
        ).to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # Deux blobs A_1, A_2 qui se rencontrent en un point P
        a1 = Circle(
            radius=1.7, color=OPEN_SET_COLOR, stroke_width=3,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.18,
        ).move_to(np.array([-1.4, -0.3, 0]))
        a2 = Circle(
            radius=1.7, color="#06D6A0", stroke_width=3,
            fill_color="#06D6A0", fill_opacity=0.18,
        ).move_to(np.array([1.4, -0.3, 0]))
        a1_lab = MathTex(
            "A_1", font_size=30, color=OPEN_SET_COLOR,
        ).move_to(a1.get_center() + LEFT * 1.1 + UP * 0.6)
        a2_lab = MathTex(
            "A_2", font_size=30, color="#06D6A0",
        ).move_to(a2.get_center() + RIGHT * 1.1 + UP * 0.6)

        # Point commun P à l'intersection
        p_pt = np.array([0, -0.30, 0])
        p_dot = Dot(p_pt, color=HIGHLIGHT_COLOR, radius=0.10)
        p_lab = MathTex(
            "P", font_size=26, color=HIGHLIGHT_COLOR,
        ).next_to(p_dot, UP, buff=0.10)

        # Deux points dans chaque blob
        x1_pt = np.array([-2.4, 0.4, 0])
        x2_pt = np.array([2.4, -0.5, 0])
        x1_dot_loc = Dot(x1_pt, color="#FFD166", radius=0.085)
        x2_dot_loc = Dot(x2_pt, color="#FFD166", radius=0.085)
        x1_label_loc = MathTex(
            "x", font_size=24, color="#FFD166",
        ).next_to(x1_dot_loc, UL, buff=0.08)
        x2_label_loc = MathTex(
            "y", font_size=24, color="#FFD166",
        ).next_to(x2_dot_loc, UR, buff=0.08)

        # Chemin γ_1 dans A_1 de x à P, chemin γ_2 dans A_2 de P à y
        def gamma1(t: float) -> np.ndarray:
            base = (1 - t) * x1_pt + t * p_pt
            return base + np.array([0, 0.35 * np.sin(np.pi * t), 0])
        def gamma2(t: float) -> np.ndarray:
            base = (1 - t) * p_pt + t * x2_pt
            return base + np.array([0, -0.35 * np.sin(np.pi * t), 0])

        path1 = ParametricFunction(
            gamma1, t_range=[0, 1],
            color=PATH_COLOR, stroke_width=3.5,
        )
        path2 = ParametricFunction(
            gamma2, t_range=[0, 1],
            color="#F72585", stroke_width=3.5,
        )

        self.play(
            Create(a1), Write(a1_lab),
            Create(a2), Write(a2_lab),
        )
        self.play(
            FadeIn(p_dot, scale=2),
            Write(p_lab),
        )
        self.play(
            FadeIn(x1_dot_loc, scale=1.5),
            FadeIn(x2_dot_loc, scale=1.5),
            Write(x1_label_loc),
            Write(x2_label_loc),
        )
        self.play(Create(path1), run_time=1.4)
        self.play(Create(path2), run_time=1.4)

        enonce = MathTex(
            r"A_1, A_2 \text{ c.p.a.,}\; P \in A_1 \cap A_2",
            r"\;\Longrightarrow\;",
            r"A_1 \cup A_2 \text{ est c.p.a. (par concaténation)}",
            font_size=24,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.45)
        enonce[2].set_color(HIGHLIGHT_COLOR)
        self.play(Write(enonce), run_time=2.0)
        self.wait(2.4)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _subframe_produit_fini(self) -> None:
        """Sub-frame : produit fini de c.p.a. est c.p.a."""
        titre = Text(
            "Proposition IV.1 — produit fini",
            font_size=30, color=PATH_COLOR,
        ).to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # X_1 × X_2 visualisé comme un rectangle (le produit)
        rect = Rectangle(
            width=6.4, height=3.6,
            color=OPEN_SET_COLOR, stroke_width=3,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.14,
        ).move_to(np.array([0, -0.20, 0]))
        rect_lab = MathTex(
            r"X_1 \times X_2", font_size=30, color=OPEN_SET_COLOR,
        ).next_to(rect, UP, buff=0.15)

        # Deux points (x_1, y_1) et (x_2, y_2)
        p1 = rect.get_center() + np.array([-2.3, -1.2, 0])
        p2 = rect.get_center() + np.array([2.3, 1.2, 0])
        # Point intermédiaire (x_2, y_1) ou (x_1, y_2) — pour l'animation en L
        pmid = np.array([p2[0], p1[1], 0])

        p1_dot = Dot(p1, color=HIGHLIGHT_COLOR, radius=0.085)
        p2_dot = Dot(p2, color=HIGHLIGHT_COLOR, radius=0.085)
        pmid_dot = Dot(pmid, color="#FFD166", radius=0.075)

        p1_lab = MathTex(
            r"(x_1, y_1)", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(p1_dot, DL, buff=0.10)
        p2_lab = MathTex(
            r"(x_2, y_2)", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(p2_dot, UR, buff=0.10)
        pmid_lab = MathTex(
            r"(x_2, y_1)", font_size=20, color="#FFD166",
        ).next_to(pmid_dot, DR, buff=0.10)

        # Chemin horizontal (x_1, y_1) → (x_2, y_1) puis vertical (x_2, y_1) → (x_2, y_2)
        h_seg = Line(p1, pmid, color=PATH_COLOR, stroke_width=4)
        v_seg = Line(pmid, p2, color="#F72585", stroke_width=4)

        h_lab = MathTex(
            r"\text{horizontal dans } X_1",
            font_size=18, color=PATH_COLOR,
        ).next_to(h_seg, DOWN, buff=0.12)
        v_lab = MathTex(
            r"\text{vertical dans } X_2",
            font_size=18, color="#F72585",
        ).next_to(v_seg, RIGHT, buff=0.12)

        self.play(Create(rect), Write(rect_lab))
        self.play(
            FadeIn(p1_dot, scale=1.5),
            FadeIn(p2_dot, scale=1.5),
            Write(p1_lab),
            Write(p2_lab),
        )
        self.play(Create(h_seg), Write(h_lab), run_time=1.4)
        self.play(FadeIn(pmid_dot, scale=2), Write(pmid_lab))
        self.play(Create(v_seg), Write(v_lab), run_time=1.4)

        enonce = MathTex(
            r"X_1, X_2 \text{ c.p.a.}",
            r"\;\Longrightarrow\;",
            r"X_1 \times X_2 \text{ c.p.a.}\;",
            r"(\text{chemin en L : } X_1 \text{ puis } X_2)",
            font_size=23,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.45)
        enonce[2].set_color(HIGHLIGHT_COLOR)
        enonce[3].set_color(DIM_COLOR)
        self.play(Write(enonce), run_time=2.0)
        self.wait(2.4)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _subframe_concatenation(self) -> None:
        """Sub-frame : concaténation γ ⋆ γ' de deux chemins."""
        titre = Text(
            "Concaténation  γ ⋆ γ'",
            font_size=32, color=PATH_COLOR,
        ).to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # Espace ambiant
        space = Ellipse(
            width=9.0, height=4.4,
            color=OPEN_SET_COLOR, stroke_width=2.4,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.10,
        ).move_to(np.array([0, -0.20, 0]))
        space_lab = MathTex(
            "X", font_size=28, color=OPEN_SET_COLOR,
        ).move_to(space.get_corner(UR) + DL * 0.40)

        # Trois points : γ(0), γ(1) = γ'(0) = P, γ'(1)
        a_pt = space.get_center() + np.array([-3.0, -0.6, 0])
        p_pt = space.get_center() + np.array([0.0, 0.7, 0])
        b_pt = space.get_center() + np.array([3.0, -0.5, 0])

        a_dot = Dot(a_pt, color=HIGHLIGHT_COLOR, radius=0.09)
        p_dot = Dot(p_pt, color="#FFD166", radius=0.10)
        b_dot = Dot(b_pt, color=HIGHLIGHT_COLOR, radius=0.09)

        a_lab = MathTex(
            r"\gamma(0)", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(a_dot, DL, buff=0.10)
        p_lab = MathTex(
            r"\gamma(1) = \gamma'(0)", font_size=22, color="#FFD166",
        ).next_to(p_dot, UP, buff=0.12)
        b_lab = MathTex(
            r"\gamma'(1)", font_size=22, color=HIGHLIGHT_COLOR,
        ).next_to(b_dot, DR, buff=0.10)

        # γ : a_pt -> p_pt
        def gamma1(t: float) -> np.ndarray:
            base = (1 - t) * a_pt + t * p_pt
            return base + np.array([0, 0.4 * np.sin(np.pi * t), 0])
        # γ' : p_pt -> b_pt
        def gamma2(t: float) -> np.ndarray:
            base = (1 - t) * p_pt + t * b_pt
            return base + np.array([0, -0.4 * np.sin(np.pi * t), 0])

        path_g = ParametricFunction(
            gamma1, t_range=[0, 1],
            color=PATH_COLOR, stroke_width=4,
        )
        path_gprime = ParametricFunction(
            gamma2, t_range=[0, 1],
            color="#F72585", stroke_width=4,
        )

        gamma_lab_curve = MathTex(
            r"\gamma", font_size=24, color=PATH_COLOR,
        ).next_to(path_g.point_from_proportion(0.5), UP, buff=0.12)
        gprime_lab_curve = MathTex(
            r"\gamma'", font_size=24, color="#F72585",
        ).next_to(path_gprime.point_from_proportion(0.5), DOWN, buff=0.12)

        self.play(Create(space), Write(space_lab))
        self.play(
            FadeIn(a_dot, scale=1.5),
            FadeIn(p_dot, scale=1.8),
            FadeIn(b_dot, scale=1.5),
            Write(a_lab), Write(p_lab), Write(b_lab),
        )
        self.play(Create(path_g), Write(gamma_lab_curve), run_time=1.6)
        self.play(Create(path_gprime), Write(gprime_lab_curve), run_time=1.6)

        # Formule en bas
        enonce = MathTex(
            r"\gamma \star \gamma' \text{ joint } \gamma(0) \text{ à } \gamma'(1)",
            r"\;:\quad",
            r"(\gamma \star \gamma')(t) = \gamma(2t)",
            r"\;\text{si } t \le \tfrac{1}{2},\;\;",
            r"\gamma'(2t-1)",
            r"\;\text{si } t \ge \tfrac{1}{2}.",
            font_size=22,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.45)
        enonce[2].set_color(PATH_COLOR)
        enonce[4].set_color("#F72585")
        self.play(Write(enonce), run_time=2.4)
        self.wait(2.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

    def _subframe_invariance_topologique(self) -> None:
        """Sub-frame : Corollaire IV.2 — invariance topologique."""
        titre = Text(
            "Corollaire IV.2 — invariance topologique",
            font_size=28, color=HIGHLIGHT_COLOR,
        ).to_edge(UP, buff=0.45)
        self.play(Write(titre))

        # X (gauche) ≅ Y (droite)
        x_space = Ellipse(
            width=3.6, height=2.4,
            color=OPEN_SET_COLOR, stroke_width=3,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.16,
        ).move_to(np.array([-3.2, -0.2, 0]))
        x_lab = MathTex(
            "X", font_size=32, color=OPEN_SET_COLOR,
        ).next_to(x_space, UP, buff=0.15)

        y_space = Ellipse(
            width=3.6, height=2.4,
            color=OPEN_SET_COLOR, stroke_width=3,
            fill_color=OPEN_SET_COLOR, fill_opacity=0.16,
        ).move_to(np.array([3.2, -0.2, 0]))
        y_lab = MathTex(
            "Y", font_size=32, color=OPEN_SET_COLOR,
        ).next_to(y_space, UP, buff=0.15)

        homeo_arrow = Arrow(
            x_space.get_right() + RIGHT * 0.10,
            y_space.get_left() + LEFT * 0.10,
            color=DIM_COLOR, buff=0.05, stroke_width=4,
        )
        homeo_lab = MathTex(
            r"\varphi \text{ homéo}", font_size=24, color=TEXT_COLOR,
        ).next_to(homeo_arrow, UP, buff=0.12)
        cong_lab = MathTex(
            r"X \cong Y", font_size=28, color=HIGHLIGHT_COLOR,
        ).next_to(homeo_arrow, DOWN, buff=0.18)

        self.play(
            Create(x_space), Write(x_lab),
            Create(y_space), Write(y_lab),
        )
        self.play(
            Create(homeo_arrow),
            Write(homeo_lab),
            Write(cong_lab),
        )

        enonce = MathTex(
            r"X \cong Y \;\Longrightarrow\;",
            r"\bigl(X \text{ c.p.a.} \;\Longleftrightarrow\; Y \text{ c.p.a.}\bigr)",
            font_size=28,
            color=TEXT_COLOR,
        ).to_edge(DOWN, buff=0.55)
        enonce[1].set_color(HIGHLIGHT_COLOR)
        self.play(Write(enonce), run_time=2.0)
        self.wait(2.4)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── 3. Connexité (topologique) ────────────────────────────────── #

    def section_connexite(self) -> None:
        """Connexité (§ IV.1.(c)) — définition par les ouverts-fermés.

        Suit textuellement le cours :

            « Soit (X, d) un espace métrique. On dit que X est connexe
            si ∅ et X sont les seules parties de X qui soient à la fois
            ouvertes et fermées. »

        Puis on énonce la proposition équivalente du cours :

            « X n'est pas connexe ⟺ il existe une partition X = O ⊔ O'
            en deux parties ouvertes non vides. »

        Visuel : à gauche un espace non connexe (deux disques séparés
        O et O'), à droite un espace connexe (un seul blob).
        """

        titre = Text("2.  Connexité", font_size=34, color=OPEN_SET_COLOR)
        titre.to_edge(UP, buff=0.45)
        self.play(Write(titre))

        question = Text(
            "Comment formuler « d'un seul tenant » sans parler de chemin ?",
            font_size=22,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.3)
        self.play(FadeIn(question, shift=UP * 0.12))
        self.wait(0.9)

        # ── Visuel de gauche : un espace non connexe = O ⊔ O'
        left_center = LEFT * 3.5 + DOWN * 1.0

        o_set = Circle(
            radius=0.95,
            color=O_COLOR,
            stroke_width=2.6,
            fill_color=O_COLOR,
            fill_opacity=0.22,
        ).move_to(left_center + LEFT * 0.95)
        oprime_set = Circle(
            radius=0.85,
            color=O_PRIME_COLOR,
            stroke_width=2.6,
            fill_color=O_PRIME_COLOR,
            fill_opacity=0.22,
        ).move_to(left_center + RIGHT * 0.95)
        o_lab = MathTex("O", font_size=28, color=O_COLOR).move_to(o_set)
        oprime_lab = MathTex("O'", font_size=28, color=O_PRIME_COLOR).move_to(oprime_set)

        non_conn_label = Text(
            "Non connexe",
            font_size=22,
            color=WARN_COLOR,
        ).move_to(left_center + UP * 1.7)

        # ── Visuel de droite : un espace connexe = un seul morceau
        right_center = RIGHT * 3.5 + DOWN * 1.0
        connexe_blob = Ellipse(
            width=3.4,
            height=2.1,
            color=OPEN_SET_COLOR,
            stroke_width=2.6,
            fill_color=OPEN_SET_COLOR,
            fill_opacity=0.18,
        ).move_to(right_center)
        connexe_label = Text(
            "Connexe",
            font_size=22,
            color=OPEN_SET_COLOR,
        ).move_to(right_center + UP * 1.7)

        self.play(
            LaggedStart(
                Create(o_set), Create(oprime_set),
                Write(o_lab), Write(oprime_lab),
                Write(non_conn_label),
                lag_ratio=0.15,
            )
        )
        self.play(
            Create(connexe_blob),
            Write(connexe_label),
        )
        self.wait(0.8)

        # ── Définition primaire du cours (§ IV.1.(c)) : par les clopens ──
        self.play(FadeOut(question))
        definition = MathTex(
            r"X \text{ est \emph{connexe} si } \varnothing \text{ et } X",
            r"\text{ sont les seules parties de } X",
            r"\text{ à la fois ouvertes \emph{et} fermées.}",
            font_size=24,
        ).arrange(RIGHT, buff=0.10).next_to(titre, DOWN, buff=0.30)
        definition[0].set_color(OPEN_SET_COLOR)
        self.play(Write(definition), run_time=2.4)
        self.wait(1.2)

        # ── Proposition équivalente (du cours) : partition en O ⊔ O' ──
        proposition = MathTex(
            r"\textbf{Proposition.}\;",
            r"X \text{ n'est pas connexe}",
            r"\;\Longleftrightarrow\;",
            r"\exists\, X = O \sqcup O' \text{ avec } O, O' \text{ ouverts non vides.}",
            font_size=22,
            color=HIGHLIGHT_COLOR,
        )
        proposition.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(proposition, shift=UP * 0.12), run_time=1.6)

        # Petit pulse sur le blob "connexe" et flash sur la partition
        self.play(
            Indicate(connexe_blob, color=HIGHLIGHT_COLOR, scale_factor=1.04),
            Indicate(VGroup(o_set, oprime_set), color=WARN_COLOR, scale_factor=1.04),
        )
        self.wait(2.4)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── 4. Théorème : c.p.a. ⟹ connexe ────────────────────────────── #

    def section_implication(self) -> None:
        """Corollaire : connexe par arcs ⟹ connexe (§ IV.1.(c)).

        Démonstration suivant la *recette du cours* :

            « On raisonne par contraposition. Soit X un espace métrique
            qui n'est pas connexe : il existe une partition X = O ⊔ O'
            en deux parties ouvertes non vides. Supposons qu'il existe
            un chemin γ : [0,1] → X joignant un point de O à un point
            de O'. Fabriquer alors une partition de [0,1] en deux
            ouverts non vides. Conclure. »

        Visuel persistant en deux niveaux :
            * X = O ⊔ O' avec les points x_0 ∈ O, x_1 ∈ O' (haut) ;
            * une flèche verticale étiquetée γ⁻¹ relie les niveaux ;
            * le segment [0,1] (bas) accueille la partition
              γ⁻¹(O) ⊔ γ⁻¹(O') au fil de la preuve.

        Une seule ligne de texte d'étape en bas, qui transforme à chaque
        temps fort, accompagnée d'une animation ciblée sur le diagramme.
        La conclusion exploite explicitement le corollaire « [0,1] est
        connexe » établi à la section précédente.
        """

        # ── Header ────────────────────────────────────────────────── #
        titre = Text(
            "Corollaire : connexe par arcs ⟹ connexe",
            font_size=34,
            color=HIGHLIGHT_COLOR,
        ).to_edge(UP, buff=0.4)
        sous = Text(
            "Démonstration par contraposition (recette du cours)",
            font_size=22,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.18)
        self.play(Write(titre))
        self.play(FadeIn(sous, shift=UP * 0.1))
        self.wait(1.0)
        self.play(FadeOut(sous))

        # ── Schéma persistant : X = O ⊔ O' (haut) et [0,1] (bas) ─── #

        # Espace X = O ⊔ O', large et centré, deux disques nettement disjoints
        o_center = np.array([-2.50, 1.05, 0])
        oprime_center = np.array([2.50, 1.05, 0])
        o_set = Circle(
            radius=1.10, color=O_COLOR, stroke_width=3.2,
            fill_color=O_COLOR, fill_opacity=0.22,
        ).move_to(o_center)
        oprime_set = Circle(
            radius=1.10, color=O_PRIME_COLOR, stroke_width=3.2,
            fill_color=O_PRIME_COLOR, fill_opacity=0.22,
        ).move_to(oprime_center)
        o_lab = MathTex("O", font_size=34, color=O_COLOR).move_to(
            o_center + UP * 0.62,
        )
        oprime_lab = MathTex("O'", font_size=34, color=O_PRIME_COLOR).move_to(
            oprime_center + UP * 0.62,
        )
        x_eq_label = MathTex(
            r"X = O \sqcup O'",
            font_size=28,
            color=DIM_COLOR,
        ).move_to(np.array([0, 2.55, 0]))

        x0_pt = o_center + np.array([0.45, -0.10, 0])
        x1_pt = oprime_center + np.array([-0.45, 0.10, 0])
        x0_dot = Dot(x0_pt, color=HIGHLIGHT_COLOR, radius=0.10)
        x1_dot = Dot(x1_pt, color=HIGHLIGHT_COLOR, radius=0.10)
        x0_label_dot = MathTex(
            "x_0", font_size=28, color=HIGHLIGHT_COLOR,
        ).next_to(x0_dot, DOWN, buff=0.10)
        x1_label_dot = MathTex(
            "x_1", font_size=28, color=HIGHLIGHT_COLOR,
        ).next_to(x1_dot, DOWN, buff=0.10)

        # Chemin γ : tracé en pointillés à l'étape 2
        def gamma_func(t: float) -> np.ndarray:
            base = (1.0 - t) * x0_pt + t * x1_pt
            wobble = np.array([0.0, 0.55 * np.sin(np.pi * t), 0.0])
            return base + wobble

        path = ParametricFunction(
            gamma_func, t_range=[0, 1],
            color=PATH_COLOR, stroke_width=4,
        )
        dashed_path = DashedVMobject(path, num_dashes=22)

        # Flèche verticale γ⁻¹ entre X et [0,1]
        pre_arrow = Arrow(
            np.array([0, -0.20, 0]),
            np.array([0, -1.20, 0]),
            color=DIM_COLOR, buff=0.05, stroke_width=4,
        )
        pre_label = MathTex(
            r"\gamma^{-1}", font_size=28, color=TEXT_COLOR,
        ).next_to(pre_arrow, RIGHT, buff=0.18)

        # Segment [0,1] avec sa partition.
        # Pas de labels automatiques (sinon ils chevauchent l'étiquette
        # [0,1] et les tags 0/1 colorés que l'on ajoute manuellement).
        number_line = NumberLine(
            x_range=[0, 1, 0.1],
            length=8.0,
            color=DIM_COLOR,
            stroke_width=3,
            include_numbers=False,
            include_ticks=True,
        ).move_to(np.array([0, -1.85, 0]))
        interval_label = MathTex(
            "[0,1]", font_size=28, color=TEXT_COLOR,
        ).next_to(number_line, LEFT, buff=0.40)

        tau = 0.5
        a_segment = Line(
            number_line.n2p(0), number_line.n2p(tau),
            color=O_COLOR, stroke_width=11,
        )
        b_segment = Line(
            number_line.n2p(tau), number_line.n2p(1),
            color=O_PRIME_COLOR, stroke_width=11,
        )
        a_lab_pre = MathTex(
            r"\gamma^{-1}(O)", font_size=24, color=O_COLOR,
        ).next_to(a_segment, UP, buff=0.16)
        b_lab_pre = MathTex(
            r"\gamma^{-1}(O')", font_size=24, color=O_PRIME_COLOR,
        ).next_to(b_segment, UP, buff=0.16)
        zero_dot = Dot(number_line.n2p(0), color=O_COLOR, radius=0.085)
        one_dot = Dot(number_line.n2p(1), color=O_PRIME_COLOR, radius=0.085)
        zero_tag = MathTex("0", font_size=24, color=O_COLOR).next_to(
            zero_dot, DOWN, buff=0.18,
        )
        one_tag = MathTex("1", font_size=24, color=O_PRIME_COLOR).next_to(
            one_dot, DOWN, buff=0.18,
        )
        boundary_marker = Dot(
            number_line.n2p(tau), color=WARN_COLOR, radius=0.10,
        )

        # ── Zone de texte d'étape — UNE seule ligne, en bas ──────── #
        step_pos = np.array([0, -3.30, 0])

        # Étape 1 — Hypothèse de la contraposée (formulation du cours)
        step = MathTex(
            r"\text{Supposons } X \text{ non connexe : } X = O \sqcup O',\;",
            r"x_0 \in O,\; x_1 \in O'.",
            font_size=28,
        ).move_to(step_pos)

        self.play(
            LaggedStart(
                Write(x_eq_label),
                Create(o_set), Create(oprime_set),
                Write(o_lab), Write(oprime_lab),
                lag_ratio=0.12,
            ),
            run_time=2.0,
        )
        self.play(
            FadeIn(x0_dot, scale=1.6), FadeIn(x1_dot, scale=1.6),
            Write(x0_label_dot), Write(x1_label_dot),
            Write(step),
            run_time=1.6,
        )
        self.wait(1.6)

        # Étape 2 — On suppose un chemin γ continu joignant x_0 à x_1
        next_step = MathTex(
            r"\text{Supposons un chemin } \gamma : [0,1] \to X \text{ continu},\;",
            r"\gamma(0)=x_0,\; \gamma(1)=x_1.",
            font_size=27,
        ).move_to(step_pos)

        runner = Dot(color=RUNNER_COLOR, radius=0.10).move_to(x0_pt)
        runner_glow = always_redraw(
            lambda: make_glow(runner, RUNNER_COLOR, radii=(0.16, 0.28, 0.42))
        )
        self.add(runner_glow, runner)
        self.play(
            FadeOut(step), FadeIn(next_step),
            Create(dashed_path),
            MoveAlongPath(runner, path),
            run_time=2.8,
        )
        runner_glow.clear_updaters()
        self.play(FadeOut(runner_glow), FadeOut(runner))
        step = next_step
        self.wait(1.4)

        # Étape 3 — Fabrication des préimages : γ⁻¹(O), γ⁻¹(O') ouverts
        next_step = MathTex(
            r"\gamma \text{ continue } \Rightarrow\;"
            r"\gamma^{-1}(O),\, \gamma^{-1}(O') \text{ ouverts dans } [0,1].",
            font_size=28,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Create(pre_arrow), Write(pre_label),
            run_time=1.6,
        )
        self.play(
            Create(number_line), Write(interval_label),
            run_time=1.0,
        )
        self.play(
            Create(a_segment), Create(b_segment),
            Write(a_lab_pre), Write(b_lab_pre),
            run_time=1.6,
        )
        step = next_step
        self.wait(1.4)

        # Étape 4 — Non vides : 0 ∈ γ⁻¹(O), 1 ∈ γ⁻¹(O')
        next_step = MathTex(
            r"0 \in \gamma^{-1}(O),\quad 1 \in \gamma^{-1}(O')",
            r"\;\Rightarrow\; \text{ils sont non vides.}",
            font_size=28,
        ).move_to(step_pos)
        next_step[1].set_color(DIM_COLOR)

        self.play(
            FadeOut(step), FadeIn(next_step),
            FadeIn(zero_dot, scale=1.6), FadeIn(one_dot, scale=1.6),
            Write(zero_tag), Write(one_tag),
            run_time=1.6,
        )
        self.play(
            Flash(zero_dot, color=O_COLOR, line_length=0.20, num_lines=12),
            Flash(one_dot, color=O_PRIME_COLOR, line_length=0.20, num_lines=12),
        )
        step = next_step
        self.wait(1.2)

        # Étape 5 — Disjoints
        next_step = MathTex(
            r"\gamma^{-1}(O) \cap \gamma^{-1}(O') = \gamma^{-1}(O \cap O') = \varnothing.",
            font_size=28,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            FadeIn(boundary_marker, scale=2),
            run_time=1.6,
        )
        self.play(
            Indicate(boundary_marker, color=WARN_COLOR, scale_factor=2),
        )
        self.play(FadeOut(boundary_marker))
        step = next_step
        self.wait(1.2)

        # Étape 6 — Recouvrement de [0,1]
        next_step = MathTex(
            r"\gamma^{-1}(O) \cup \gamma^{-1}(O') = \gamma^{-1}(X) = [0,1].",
            font_size=28,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Indicate(
                VGroup(a_segment, b_segment),
                color=HIGHLIGHT_COLOR,
                scale_factor=1.06,
            ),
            run_time=1.8,
        )
        step = next_step
        self.wait(1.2)

        # Étape 7 — Bilan : partition non triviale en ouverts (= recette « fabriquer »)
        next_step = MathTex(
            r"\Longrightarrow\; [0,1] = \gamma^{-1}(O) \sqcup \gamma^{-1}(O')",
            r"\text{ partition non triviale en ouverts.}",
            font_size=26,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Indicate(number_line, color=HIGHLIGHT_COLOR, scale_factor=1.04),
            run_time=1.8,
        )
        step = next_step
        self.wait(1.4)

        # Étape 8 — Contradiction avec le corollaire « [0,1] est connexe »
        next_step = MathTex(
            r"\text{Or } [0,1] \text{ est connexe (corollaire vu plus haut) :}",
            r"\text{ contradiction.}",
            font_size=30,
            color=WARN_COLOR,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Indicate(
                VGroup(a_segment, b_segment, number_line),
                color=WARN_COLOR,
            ),
            run_time=1.8,
        )
        step = next_step
        self.play(Circumscribe(step, color=WARN_COLOR, buff=0.18))
        self.wait(2.5)

        # ── Conclusion encadrée ───────────────────────────────────── #
        self.play(*[FadeOut(m) for m in self.mobjects])

        conclusion = MathTex(
            r"\boxed{\;X \text{ connexe par arcs} \;\Longrightarrow\; X \text{ connexe}\;}",
            font_size=44,
            color=HIGHLIGHT_COLOR,
        )
        self.play(Write(conclusion), run_time=2.0)
        self.wait(2.8)
        self.play(FadeOut(conclusion))

    # ── 5. Caractérisation par {0,1} ──────────────────────────────── #

    def section_caracterisation(self) -> None:
        """Théorème : X connexe ⟺ toute f : X → {0,1} continue est constante.

        Schéma central X --f--> {0,1} grand et persistant ; ligne d'étape
        unique en bas qui transforme. Le schéma lui-même se modifie pour
        illustrer chacun des deux sens de l'équivalence :

        * sens (⟸) : on partitionne X en O ⊔ O' (deux disques colorés
          apparaissent dans X) et la flèche unique est remplacée par
          deux flèches partielles O → 0 et O' → 1 ; le rappel passe par
          l'exercice 88 du cours sur les applications localement constantes ;
        * sens (⟹) : on revient à un X uniforme, on teinte ses préimages,
          puis l'une des deux teintes disparaît (X est connexe → l'autre
          est ∅) et la flèche pointe vers une seule cible.

        On termine par le **corollaire « [0,1] est connexe »** qui sera
        utilisé dans la démonstration de la section suivante.
        """

        # ── Header compact ────────────────────────────────────────── #
        titre = Text(
            "Caractérisation par les applications vers {0,1}",
            font_size=30,
            color=OPEN_SET_COLOR,
        ).to_edge(UP, buff=0.4)
        self.play(Write(titre))

        theoreme = MathTex(
            r"X \text{ connexe}",
            r"\;\Longleftrightarrow\;",
            r"\text{toute } f : X \to \{0,1\} \text{ continue est constante}",
            font_size=26,
        ).next_to(titre, DOWN, buff=0.22)
        theoreme[0].set_color(OPEN_SET_COLOR)
        box = SurroundingRectangle(theoreme, color=HIGHLIGHT_COLOR, buff=0.16)
        precision = MathTex(
            r"(\,\{0,1\} \text{ muni de la topologie discrète}\,)",
            font_size=18,
            color=DIM_COLOR,
        ).next_to(theoreme, DOWN, buff=0.14)

        self.play(Write(theoreme), Create(box), run_time=1.8)
        self.play(FadeIn(precision))
        self.wait(0.8)

        # ── Schéma central : X --f--> {0,1} (grand et persistant) ─── #
        space = Ellipse(
            width=4.4,
            height=2.8,
            color=OPEN_SET_COLOR,
            stroke_width=3.2,
            fill_color=OPEN_SET_COLOR,
            fill_opacity=0.18,
        ).move_to(np.array([-3.5, -0.50, 0]))
        space_lab = MathTex(
            "X", font_size=34, color=OPEN_SET_COLOR,
        ).next_to(space, UP, buff=0.18)

        target_zero = Dot(np.array([2.8, 0.40, 0]), color=O_COLOR, radius=0.13)
        target_one = Dot(np.array([2.8, -1.40, 0]), color=O_PRIME_COLOR, radius=0.13)
        zero_lab = MathTex("0", font_size=30, color=O_COLOR).next_to(
            target_zero, RIGHT, buff=0.22,
        )
        one_lab = MathTex("1", font_size=30, color=O_PRIME_COLOR).next_to(
            target_one, RIGHT, buff=0.22,
        )
        target_brace = MathTex(
            r"\{0,1\}",
            font_size=28,
            color=DIM_COLOR,
        ).move_to(np.array([4.0, -0.50, 0]))

        arrow_main = Arrow(
            space.get_right() + RIGHT * 0.10,
            np.array([2.20, -0.50, 0]),
            color=DIM_COLOR,
            buff=0.05,
            stroke_width=4,
        )
        f_lab = MathTex("f", font_size=30, color=TEXT_COLOR).next_to(
            arrow_main, UP, buff=0.10,
        )

        self.play(
            Create(space), Write(space_lab),
            FadeIn(target_zero, scale=1.6), FadeIn(target_one, scale=1.6),
            Write(zero_lab), Write(one_lab), Write(target_brace),
        )
        self.play(Create(arrow_main), Write(f_lab))
        self.wait(0.6)

        # ── Éléments visuels pour la phase (⟸) ───────────────────── #
        o_region = Circle(
            radius=0.85, color=O_COLOR, stroke_width=3,
            fill_color=O_COLOR, fill_opacity=0.45,
        ).move_to(space.get_center() + LEFT * 0.95)
        oprime_region = Circle(
            radius=0.85, color=O_PRIME_COLOR, stroke_width=3,
            fill_color=O_PRIME_COLOR, fill_opacity=0.45,
        ).move_to(space.get_center() + RIGHT * 0.95)
        o_region_lab = MathTex("O", font_size=24, color=O_COLOR).move_to(o_region)
        oprime_region_lab = MathTex("O'", font_size=24, color=O_PRIME_COLOR).move_to(oprime_region)

        arrow_o = Arrow(
            o_region.get_right() + RIGHT * 0.05,
            target_zero.get_left() + LEFT * 0.05,
            color=O_COLOR, buff=0.05, stroke_width=3,
        )
        arrow_oprime = Arrow(
            oprime_region.get_right() + RIGHT * 0.05,
            target_one.get_left() + LEFT * 0.05,
            color=O_PRIME_COLOR, buff=0.05, stroke_width=3,
        )

        # ── Éléments visuels pour la phase (⟹) ───────────────────── #
        f_preimage_uniform = space.copy().set_fill(O_COLOR, opacity=0.40).set_stroke(
            color=O_COLOR, width=3.2,
        )

        # ── Zone de texte d'étape — UNE seule ligne, en bas ──────── #
        step_pos = np.array([0, -3.30, 0])

        # ── Rappel : exercice 88 du cours sur localement constante ─ #
        # Cette ligne préliminaire évoque la notion-clé du cours.
        rappel = MathTex(
            r"\textbf{Exercice 88 :}\;",
            r"f : X \to \{0,1\} \text{ continue}",
            r"\;\Longleftrightarrow\;",
            r"f \text{ localement constante.}",
            font_size=22,
            color=DIM_COLOR,
        ).move_to(np.array([0, -3.30, 0]))
        self.play(Write(rappel), run_time=1.6)
        self.wait(1.2)
        self.play(FadeOut(rappel))

        # ── Phase (⟸) — Étape 1 : hypothèse de la décomposition ──── #
        step = MathTex(
            r"(\Longleftarrow)\;\;\text{Supposons } X = O \sqcup O' \text{ (non connexe).}",
            font_size=28,
        ).move_to(step_pos)

        self.play(Write(step))
        self.wait(0.6)

        # On dessine la partition dans X
        next_step = MathTex(
            r"\text{Posons } f|_O = 0,\;\; f|_{O'} = 1.",
            font_size=30,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Create(o_region), Create(oprime_region),
            Write(o_region_lab), Write(oprime_region_lab),
            FadeOut(arrow_main), FadeOut(f_lab),
            Create(arrow_o), Create(arrow_oprime),
            run_time=2.4,
        )
        step = next_step
        self.wait(1.2)

        # f localement constante → continue, et non constante
        next_step = MathTex(
            r"f \text{ est localement constante (donc continue) et non constante.}",
            font_size=26,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Indicate(arrow_o, color=HIGHLIGHT_COLOR, scale_factor=1.10),
            Indicate(arrow_oprime, color=HIGHLIGHT_COLOR, scale_factor=1.10),
            run_time=1.8,
        )
        step = next_step
        self.wait(1.2)

        # Conclusion contraposée
        next_step = MathTex(
            r"\text{Par contraposée : ``toute telle } f \text{ est constante''} \Rightarrow X \text{ est connexe.}",
            font_size=24,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            run_time=1.4,
        )
        step = next_step
        self.wait(1.6)

        # ── Transition vers (⟹) — on rétablit le X uniforme ──────── #
        self.play(
            FadeOut(o_region), FadeOut(oprime_region),
            FadeOut(o_region_lab), FadeOut(oprime_region_lab),
            FadeOut(arrow_o), FadeOut(arrow_oprime),
            FadeIn(arrow_main), FadeIn(f_lab),
            run_time=1.2,
        )

        # ── Phase (⟹) — Étape 1 : on prend X connexe et f continue ─ #
        next_step = MathTex(
            r"(\Longrightarrow)\;\;\text{Soit } X \text{ connexe et } f : X \to \{0,1\} \text{ continue.}",
            font_size=28,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            Indicate(space, color=OPEN_SET_COLOR, scale_factor=1.05),
            run_time=1.6,
        )
        step = next_step
        self.wait(1.0)

        # Étape 2 — f⁻¹({0}), f⁻¹({1}) comme sous-régions distinctes de X.
        # On les représente par deux disques colorés à l'intérieur de X,
        # accompagnés de leurs étiquettes formelles. À l'étape 3, l'un
        # rétrécira jusqu'à disparaître pour matérialiser « l'un est ∅ ».
        next_step = MathTex(
            r"f^{-1}(\{0\}),\; f^{-1}(\{1\}) \text{ ouverts \textit{et} fermés,",
            r"\text{ disjoints, d'union } X.",
            font_size=26,
        ).move_to(step_pos)

        # Sous-région f^{-1}({0}) : à gauche dans X, vert (couleur du 0)
        pre_zero_region = Ellipse(
            width=1.8, height=1.6,
            color=O_COLOR, stroke_width=2.6,
            fill_color=O_COLOR, fill_opacity=0.45,
        ).move_to(space.get_center() + LEFT * 0.95 + UP * 0.05)
        pre_zero_lab = MathTex(
            r"f^{-1}(\{0\})", font_size=20, color=O_COLOR,
        ).next_to(pre_zero_region, DOWN, buff=0.08)

        # Sous-région f^{-1}({1}) : à droite dans X, bleu (couleur du 1)
        pre_one_region = Ellipse(
            width=1.6, height=1.4,
            color=O_PRIME_COLOR, stroke_width=2.6,
            fill_color=O_PRIME_COLOR, fill_opacity=0.45,
        ).move_to(space.get_center() + RIGHT * 0.95 + DOWN * 0.05)
        pre_one_lab = MathTex(
            r"f^{-1}(\{1\})", font_size=20, color=O_PRIME_COLOR,
        ).next_to(pre_one_region, DOWN, buff=0.08)

        # Petites flèches qui montrent que chaque sous-région est envoyée
        # respectivement sur 0 et 1 par f.
        link_to_zero = DashedLine(
            pre_zero_region.get_top() + UP * 0.05,
            target_zero.get_left() + LEFT * 0.05,
            color=O_COLOR, stroke_width=1.6,
        )
        link_to_one = DashedLine(
            pre_one_region.get_top() + UP * 0.05,
            target_one.get_left() + LEFT * 0.05,
            color=O_PRIME_COLOR, stroke_width=1.6,
        )

        self.play(
            FadeOut(step), FadeIn(next_step),
            Create(pre_zero_region), Write(pre_zero_lab),
            Create(pre_one_region), Write(pre_one_lab),
            run_time=2.2,
        )
        self.play(
            Create(link_to_zero), Create(link_to_one),
            run_time=1.0,
        )
        step = next_step
        self.wait(1.6)

        # Étape 3 — X connexe ⇒ l'un est vide (définition primaire).
        # Visualisation : la région f^{-1}({1}) RÉTRÉCIT à zéro, son
        # étiquette s'efface, son lien disparaît ; symétriquement, la
        # région f^{-1}({0}) S'ÉTEND pour remplir tout X.
        next_step = MathTex(
            r"X \text{ connexe} \Rightarrow \text{ l'un des deux ouverts-fermés est } \varnothing.",
            font_size=27,
        ).move_to(step_pos)

        pre_zero_full = space.copy().set_fill(O_COLOR, opacity=0.45).set_stroke(
            color=O_COLOR, width=3,
        )
        pre_zero_full_lab = MathTex(
            r"f^{-1}(\{0\}) = X", font_size=22, color=O_COLOR,
        ).next_to(space, DOWN, buff=0.18)

        self.play(
            FadeOut(step), FadeIn(next_step),
            # f^{-1}({1}) s'efface littéralement à un point puis disparaît
            pre_one_region.animate.scale(0.001).move_to(space.get_center()),
            FadeOut(pre_one_lab),
            FadeOut(link_to_one),
            # f^{-1}({0}) gonfle pour remplir tout X
            Transform(pre_zero_region, pre_zero_full),
            Transform(pre_zero_lab, pre_zero_full_lab),
            run_time=2.4,
        )
        self.play(FadeOut(pre_one_region))
        step = next_step
        self.wait(1.4)

        # Étape 4 — f est constante (égale à 0 ici)
        next_step = MathTex(
            r"\Longrightarrow\; f \text{ est constante (égale à } 0 \text{ ici).}",
            font_size=34,
            color=HIGHLIGHT_COLOR,
        ).move_to(step_pos)

        self.play(
            FadeOut(step), FadeIn(next_step),
            FadeOut(link_to_zero),
            Indicate(target_zero, color=HIGHLIGHT_COLOR, scale_factor=2.2),
            Flash(target_zero, color=HIGHLIGHT_COLOR, line_length=0.22, num_lines=14),
            run_time=2.0,
        )
        step = next_step
        self.play(Circumscribe(step, color=HIGHLIGHT_COLOR, buff=0.16))
        self.wait(2.6)

        # ── Corollaire utilisé par la section suivante : [0,1] connexe ──
        self.play(*[FadeOut(m) for m in self.mobjects])

        corollaire_titre = Text(
            "Corollaire",
            font_size=30,
            color=HIGHLIGHT_COLOR,
        ).to_edge(UP, buff=1.2)
        corollaire = MathTex(
            r"\boxed{\;[0,1] \text{ est connexe.}\;}",
            font_size=42,
            color=OPEN_SET_COLOR,
        )
        corollaire_just = MathTex(
            r"\text{En effet, toute application continue }",
            r"f : [0,1] \to \{0,1\}",
            r"\text{ est constante (TVI).}",
            font_size=22,
            color=DIM_COLOR,
        ).arrange(RIGHT, buff=0.10).next_to(corollaire, DOWN, buff=0.45)

        self.play(Write(corollaire_titre))
        self.play(Write(corollaire), run_time=1.8)
        self.play(FadeIn(corollaire_just, shift=UP * 0.12))
        self.wait(2.6)

        self.play(*[FadeOut(m) for m in self.mobjects])

    # ── 6. Et la réciproque ? (§ IV.2.(a)) ─────────────────────────── #

    def section_reciproque(self) -> None:
        """Question de la réciproque + théorème de relais du § IV.2.(a).

        Le cours énonce :

            « Tout espace métrique complet, connexe, localement connexe,
            est connexe par arcs. »

        et donne comme contre-exemple à la réciproque ``brute'' (sans
        hypothèse supplémentaire) le graphe de x ↦ sin(1/x) sur un
        intervalle ]0, α], complété par le segment vertical de longueur 2
        centré en l'origine.
        """

        titre = Text(
            "Et la réciproque ?",
            font_size=36,
            color=HIGHLIGHT_COLOR,
        )
        titre.to_edge(UP, buff=0.6)
        self.play(Write(titre))
        self.wait(0.6)

        question = MathTex(
            r"X \text{ connexe} \;\overset{?}{\Longrightarrow}\;"
            r"X \text{ connexe par arcs}",
            font_size=34,
        )
        self.play(Write(question), run_time=1.6)
        self.wait(1.3)

        non = Text(
            "Non, en général.",
            font_size=38,
            color=WARN_COLOR,
        ).next_to(question, DOWN, buff=0.55)
        self.play(FadeIn(non, shift=UP * 0.2))
        self.play(Flash(non.get_center(), color=WARN_COLOR, line_length=0.25))
        self.wait(0.8)

        # Contre-exemple — formulation textuelle du cours (§ IV.2.(a))
        teaser_titre = Text(
            "Contre-exemple (cours, § IV.2.(a)) :",
            font_size=22,
            color=DIM_COLOR,
        )
        teaser_formule = MathTex(
            r"\text{graphe de } x \mapsto \sin(1/x) \text{ sur } ]0, \alpha]",
            r"\;\cup\;",
            r"\text{segment vertical de longueur } 2 \text{ centré en } 0",
            font_size=22,
            color=TEXT_COLOR,
        ).arrange(RIGHT, buff=0.12)
        teaser = VGroup(teaser_titre, teaser_formule).arrange(DOWN, buff=0.2)
        teaser.next_to(non, DOWN, buff=0.5)
        self.play(Write(teaser_titre))
        self.play(Write(teaser_formule), run_time=2.0)
        self.wait(1.4)

        # ── Théorème de relais — énoncé EXACT du cours ──────────────── #
        relais_titre = Text(
            "Théorème (§ IV.2.(a))",
            font_size=22,
            color=HIGHLIGHT_COLOR,
        )
        relais_enonce = MathTex(
            r"\text{Tout espace métrique \emph{complet}, \emph{connexe}, \emph{localement connexe},}",
            r"\text{ est connexe par arcs.}",
            font_size=22,
            color=HIGHLIGHT_COLOR,
        ).arrange(DOWN, buff=0.10)
        relais = VGroup(relais_titre, relais_enonce).arrange(DOWN, buff=0.18)
        relais.to_edge(DOWN, buff=0.4)

        self.play(FadeIn(relais_titre, shift=UP * 0.1))
        self.play(Write(relais_enonce), run_time=2.2)
        self.wait(2.8)

        self.play(*[FadeOut(m) for m in self.mobjects])
