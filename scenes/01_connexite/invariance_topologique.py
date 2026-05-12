"""Invariance topologique de la connexité."""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    DR,
    LEFT,
    RIGHT,
    UL,
    UP,
    Arrow,
    Circle,
    Create,
    Cross,
    Dot,
    Ellipse,
    FadeIn,
    FadeOut,
    GrowFromPoint,
    Indicate,
    Line,
    MathTex,
    NumberLine,
    NumberPlane,
    ParametricFunction,
    Scene,
    Square,
    SurroundingRectangle,
    Text,
    Transform,
    VGroup,
    Write,
)

from src.config import DEFAULT_WAIT, SHORT_WAIT
from src.utils.colors import (
    CLOSED_SET_COLOR,
    DIM_COLOR,
    HIGHLIGHT_COLOR,
    OPEN_SET_COLOR,
    PATH_COLOR,
)

TITLE_TEXT_SIZE = 32
SUBTITLE_TEXT_SIZE = 24
CONCLUSION_TEXT_SIZE = 28

INTER_TITLE_WAIT = DEFAULT_WAIT * 2
END_TITLE_WAIT = DEFAULT_WAIT * 3
INTER_ANIM_WAIT = DEFAULT_WAIT
END_ANIM_WAIT = DEFAULT_WAIT * 2
KEY_FRAME_WAIT = DEFAULT_WAIT * 8

ANIMATION_TIME = 2.5
SHORT_ANIMATION_TIME = 1.5
WRITE_TIME = 2
SHORT_WRITE_TIME = WRITE_TIME / 2


def position_title(title) -> None:
    title.to_edge(UP, buff=0.5)


def position_subtitle(title, subtitle) -> None:
    subtitle.next_to(title, DOWN, buff=0.4)


def box_subtitle(subtitle) -> SurroundingRectangle:
    return SurroundingRectangle(subtitle, color=HIGHLIGHT_COLOR, buff=0.15)


# Fix for bad kerning in the text
TEXT_SCALE_FACTOR = 0.3


class ScaledText(Text):
    def __init__(self, *args, **kwargs):
        scale_font = False
        # If the font size is lower than 32, scale it up
        if "font_size" in kwargs and kwargs["font_size"] < 32:
            scale_font = True
            kwargs["font_size"] /= TEXT_SCALE_FACTOR
        super().__init__(*args, **kwargs)
        if scale_font:
            self.scale(TEXT_SCALE_FACTOR)


class InvarianceTopologique(Scene):
    """Montre que la connexité est une propriété topologique."""

    def construct(self):
        self.section_titre()
        self.section_image_continue()
        self.section_homeomorphisme()
        self.section_application_r_r2()

    def end_of_section(self) -> None:
        self.wait(DEFAULT_WAIT * 5)
        self.play(*[FadeOut(mob) for mob in self.mobjects])
        self.wait(DEFAULT_WAIT * 2)

    def section_titre(self) -> None:
        titre = ScaledText("Invariance topologique", font_size=42)
        sous_titre = ScaledText(
            "La connexité se transporte par les homéomorphismes",
            font_size=24,
            color=DIM_COLOR,
        ).next_to(titre, DOWN, buff=0.35)

        self.play(Write(titre), run_time=WRITE_TIME)
        self.wait(INTER_TITLE_WAIT)

        self.play(FadeIn(sous_titre, shift=UP * 0.2))

        self.wait(DEFAULT_WAIT * 2)
        self.play(FadeOut(titre), FadeOut(sous_titre))
        self.wait(DEFAULT_WAIT * 1.5)

    def section_image_continue(self) -> None:
        titre = ScaledText(
            "Théorème : Image continue d'un espace connexe par arcs",
            font_size=TITLE_TEXT_SIZE,
            color=OPEN_SET_COLOR,
        )
        position_title(titre)
        self.play(Write(titre), run_time=WRITE_TIME)
        self.wait(INTER_TITLE_WAIT)

        theoreme = MathTex(
            r"f : X \to Y \text{ continue},\quad "
            r"X \text{ connexe par arcs } \Longrightarrow f(X) \text{ connexe par arcs}",
            font_size=SUBTITLE_TEXT_SIZE,
        )
        position_subtitle(titre, theoreme)
        box = box_subtitle(theoreme)
        self.play(Write(theoreme), Create(box), run_time=ANIMATION_TIME)
        self.wait(END_TITLE_WAIT)

        y_level = -0.5
        x_space_pos = np.array([-3.5, y_level, 0])
        x_space = Circle(radius=1.5, color=OPEN_SET_COLOR, stroke_width=2)
        x_space.shift(x_space_pos)
        x_label = MathTex("X", font_size=28).next_to(x_space, UP, buff=0.15)

        x_pos = x_space_pos + np.array([-0.7, 0.3, 0])
        x_dot = Dot(x_pos, color=HIGHLIGHT_COLOR, radius=0.07)
        x_text = MathTex("x", font_size=20).next_to(x_dot, UL, buff=0.08)

        dx = 1.4
        dy = -0.8
        y_pos = x_pos + np.array([dx, dy, 0])
        y_dot = Dot(y_pos, color=HIGHLIGHT_COLOR, radius=0.07)
        y_text = MathTex("y", font_size=20).next_to(y_dot, DR, buff=0.08)

        factx = 0.3
        facty = 0.2
        gamma = ParametricFunction(
            lambda t: np.array(
                [
                    x_pos[0] + dx * t + factx * np.sin(2 * np.pi * t),
                    x_pos[1] + dy * t + facty * np.sin(3 * np.pi * t),
                    0,
                ]
            ),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=2.5,
        )
        gamma_label = MathTex(r"\gamma", font_size=22, color=PATH_COLOR).next_to(
            gamma.point_from_proportion(0.5),
            LEFT,
            buff=0.15,
        )

        y_space_pos = np.array([-x_space_pos[0], y_level, 0])
        y_space = Ellipse(width=3.5, height=2.5, color=OPEN_SET_COLOR, stroke_width=2)
        y_space.shift(y_space_pos)
        y_space_label = MathTex("Y", font_size=28).next_to(y_space, UP, buff=0.15)

        fx_pos = y_space_pos + np.array([-1.35, +0.5, 0])
        fx_dot = Dot(fx_pos, color=HIGHLIGHT_COLOR, radius=0.07)
        fx_text = MathTex("f(x)", font_size=20).next_to(fx_dot, UL, buff=0.08)

        fdx = 2.2
        fdy = -0.8
        fy_pos = fx_pos + np.array([fdx, fdy, 0])
        fy_dot = Dot(fy_pos, color=HIGHLIGHT_COLOR, radius=0.07)
        fy_text = MathTex("f(y)", font_size=20).next_to(fy_dot, DR, buff=0.08)

        ffactx = 0.4
        ffacty = 0.3
        image_path = ParametricFunction(
            lambda t: np.array(
                [
                    fx_pos[0] + (fdx - ffactx) * t + ffactx * np.sin(2.5 * np.pi * t),
                    fx_pos[1] + fdy * t + ffacty * np.sin(2 * np.pi * t),
                    0,
                ]
            ),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=2.5,
        )
        image_label = MathTex(
            r"f \circ \gamma", font_size=22, color=PATH_COLOR
        ).next_to(
            image_path.point_from_proportion(0.5),
            RIGHT,
            buff=0.15,
        )

        arrow_dx = 1.5
        arrow = Arrow([-arrow_dx, y_level, 0], [arrow_dx, y_level, 0], color=DIM_COLOR)
        arrow_label = MathTex("f", font_size=26).next_to(arrow, UP, buff=0.1)

        self.play(
            Create(x_space),
            Write(x_label),
            run_time=SHORT_ANIMATION_TIME,
        )
        self.wait(INTER_ANIM_WAIT)

        self.play(
            Create(arrow),
            Write(arrow_label),
            run_time=SHORT_ANIMATION_TIME,
        )
        self.wait(INTER_ANIM_WAIT)

        self.play(
            Create(y_space),
            Write(y_space_label),
            run_time=SHORT_ANIMATION_TIME,
        )
        self.wait(END_ANIM_WAIT)

        self.play(
            FadeIn(x_dot),
            FadeIn(y_dot),
            Write(x_text),
            Write(y_text),
            run_time=SHORT_ANIMATION_TIME,
        )
        self.wait(INTER_ANIM_WAIT)

        self.play(Create(gamma), Write(gamma_label), run_time=ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        arrow_grp = VGroup(arrow, arrow_label)
        self.play(Indicate(arrow_grp, color=HIGHLIGHT_COLOR, scale_factor=1.1))
        self.wait(INTER_ANIM_WAIT)

        self.play(
            FadeIn(fx_dot),
            FadeIn(fy_dot),
            Write(fx_text),
            Write(fy_text),
            run_time=SHORT_ANIMATION_TIME,
        )
        self.wait(INTER_ANIM_WAIT)

        self.play(Create(image_path), Write(image_label), run_time=ANIMATION_TIME)
        self.wait(KEY_FRAME_WAIT)

        conclusion_dy = -2
        conclusion = MathTex(
            r"\gamma \text{ relie } x \text{ à } y \Longrightarrow f \circ \gamma \text{ relie } f(x) \text{ à } f(y)",
            font_size=CONCLUSION_TEXT_SIZE,
            color=HIGHLIGHT_COLOR,
        ).shift([0, y_level + conclusion_dy, 0])

        self.play(Write(conclusion), run_time=WRITE_TIME)
        self.end_of_section()

    def section_homeomorphisme(self) -> None:
        titre = ScaledText(
            "Corollaire : l'homéomorphisme préserve la connexité",
            font_size=TITLE_TEXT_SIZE,
            color=OPEN_SET_COLOR,
        )
        position_title(titre)
        self.play(Write(titre), run_time=WRITE_TIME)
        self.wait(INTER_TITLE_WAIT)

        corollaire = MathTex(
            r"X \cong Y \Longrightarrow"
            r"\bigl(X \text{ connexe} \iff Y \text{ connexe}\bigr)",
            font_size=SUBTITLE_TEXT_SIZE,
        )
        position_subtitle(titre, corollaire)
        box = box_subtitle(corollaire)
        self.play(Write(corollaire), Create(box), run_time=WRITE_TIME)
        self.wait(END_TITLE_WAIT)

        S1_radius = 1.3
        S1_line_width = 1.5
        S1_pos = LEFT * 3
        S1 = Circle(
            radius=S1_radius,
            color=OPEN_SET_COLOR,
            fill_opacity=0.15,
            stroke_width=S1_line_width,
        )
        S1.move_to(S1_pos)

        plane_max = 1.2
        plane_range = 2 * plane_max
        S1_plane = NumberPlane(
            x_range=(-plane_max, plane_max, 1),
            y_range=(-plane_max, plane_max, 1),
            x_length=plane_range * S1_radius,
            y_length=plane_range * S1_radius,
            background_line_style={
                "stroke_color": DIM_COLOR,
                "stroke_width": S1_line_width / 4,
            },
            axis_config={"stroke_color": DIM_COLOR, "stroke_width": S1_line_width},
        ).move_to(S1_pos)
        S1_label = MathTex(r"\mathbb{S}^1", font_size=24).next_to(
            S1_plane, DOWN, buff=0.2
        )

        square_side_length = 2.6
        square = Square(
            side_length=square_side_length,
            color=OPEN_SET_COLOR,
            fill_opacity=0.15,
            stroke_width=S1_line_width,
        )
        square_pos = RIGHT * 3
        square.shift(square_pos)

        plane_min = -0.1
        plane_max = 1.1
        plane_range = -plane_min + plane_max
        square_plane = NumberPlane(
            x_range=(plane_min, plane_max, 1),
            y_range=(plane_min, plane_max, 1),
            x_length=plane_range * square_side_length,
            y_length=plane_range * square_side_length,
            background_line_style={
                "stroke_color": DIM_COLOR,
                "stroke_width": S1_line_width / 4,
            },
            axis_config={"stroke_color": DIM_COLOR, "stroke_width": S1_line_width},
        ).move_to(square_pos)
        square_label = MathTex(r"[0,1]^2", font_size=24).next_to(
            square_plane, DOWN, buff=0.2
        )

        cong1 = MathTex(r"\cong", font_size=40, color=HIGHLIGHT_COLOR)

        ex1 = VGroup(S1, S1_label, S1_plane, square, square_label, square_plane, cong1)
        ex1_pos = np.array([0, -0.5, 0])
        ex1.shift(ex1_pos)

        # TODO: Find other exemple
        self.play(FadeIn(S1_plane), run_time=SHORT_ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(Create(S1), Write(S1_label), run_time=ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(Write(cong1), run_time=SHORT_WRITE_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(FadeIn(square_plane), run_time=SHORT_ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        deformed_circle = S1.copy()
        self.play(
            Transform(deformed_circle, square),
            Write(square_label),
            run_time=ANIMATION_TIME,
        )
        self.wait(END_ANIM_WAIT)

        ccl_pos = ex1_pos - [0, 2.5, 0]
        conclusion = MathTex(
            r"\mathbb{S}^1 \text{ est connexe (par arcs) et homéomorphe à }[0,1]^2 \Longrightarrow [0,1]^2 \text{ est connexe (par arcs)}",
            font_size=CONCLUSION_TEXT_SIZE,
            color=HIGHLIGHT_COLOR,
        ).move_to(ccl_pos)

        self.play(Write(conclusion), run_time=WRITE_TIME)
        self.wait(SHORT_WAIT)
        self.end_of_section()

    def section_application_r_r2(self) -> None:
        espace = 0.15
        application = ScaledText(
            r"Application : ",
            font_size=TITLE_TEXT_SIZE,
            color=HIGHLIGHT_COLOR,
        )
        R = (
            MathTex(
                r"\mathbb{R}",
                font_size=TITLE_TEXT_SIZE + 10,
                color=HIGHLIGHT_COLOR,
            )
            .next_to(application, buff=espace)
            .shift(0.04 * UP)
        )
        pas_homeo = (
            ScaledText(
                r" n'est pas homéomorphe à ",
                font_size=TITLE_TEXT_SIZE,
                color=HIGHLIGHT_COLOR,
            )
            .next_to(R, buff=espace)
            .shift(0.03 * DOWN)
        )
        R2 = (
            MathTex(
                r"\mathbb{R}^2",
                font_size=TITLE_TEXT_SIZE + 10,
                color=HIGHLIGHT_COLOR,
            )
            .next_to(pas_homeo, buff=espace)
            .shift(0.08 * UP)
        )

        titre = VGroup(application, R, pas_homeo, R2)
        titre.move_to([0, 3.25, 0])
        self.play(Write(titre), run_time=WRITE_TIME)
        self.wait(INTER_TITLE_WAIT)

        idee = ScaledText(
            "Lorsqu'on retire un point, les deux espaces réagissent topologiquement différemment.",
            font_size=SUBTITLE_TEXT_SIZE - 2,
            color=DIM_COLOR,
        )
        position_subtitle(titre, idee)
        self.play(Write(idee), run_time=WRITE_TIME)
        self.wait(END_TITLE_WAIT)

        line_posy = 1.6
        line_width = 2
        line_max = 6.5
        line_range = 2 * line_max
        scale = 0.75
        line = NumberLine(
            x_range=[-line_max, line_max, 1],
            length=scale * line_range,
            color=DIM_COLOR,
            stroke_width=line_width,
        ).shift([0, line_posy, 0])

        removed_point = Cross(
            color=CLOSED_SET_COLOR,
            scale_factor=0.1,
            stroke_width=line_width,
        ).move_to([0, line_posy, 0])

        part_width = 2 * line_width
        left_part = Line(
            [-scale * line_max, line_posy, 0],
            [-0.1, line_posy, 0],
            color=OPEN_SET_COLOR,
            stroke_width=part_width,
        )
        right_part = Line(
            [0.1, line_posy, 0],
            [scale * line_max, line_posy, 0],
            color="#4361EE",
            stroke_width=part_width,
        )

        line_label = MathTex(r"\mathbb{R} \setminus \{0\}", font_size=26).next_to(
            line, DOWN, buff=0.2
        )
        line_conclusion = ScaledText(
            "Non connexe : deux composantes",
            font_size=20,
            color=CLOSED_SET_COLOR,
        ).next_to(line_label, DOWN, buff=0.15)

        self.play(FadeIn(line), run_time=SHORT_ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(Write(line_label), FadeIn(removed_point), run_time=WRITE_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(
            GrowFromPoint(left_part, left_part.get_end()),
            Create(right_part),
            run_time=ANIMATION_TIME,
        )
        self.wait(INTER_ANIM_WAIT)

        self.play(Write(line_conclusion), run_time=WRITE_TIME)
        self.wait(END_ANIM_WAIT)

        plane_posy = line_posy - 2.7
        plane_xmax = 6.5
        plane_xrange = 2 * plane_xmax
        plane_ymax = plane_xmax * 2 / 3
        plane_yrange = 2 * plane_ymax
        scale2 = 0.35
        punctured_plane = NumberPlane(
            x_range=(-plane_xmax, plane_xmax, 1),
            y_range=(-plane_ymax, plane_ymax, 1),
            x_length=scale2 * plane_xrange,
            y_length=scale2 * plane_yrange,
            background_line_style={
                "stroke_color": DIM_COLOR,
                "stroke_width": line_width / 4,
            },
            axis_config={"stroke_color": DIM_COLOR, "stroke_width": line_width},
        )
        punctured_plane.shift([0, plane_posy, 0])
        removed_origin = Cross(
            color=CLOSED_SET_COLOR,
            scale_factor=0.1,
            stroke_width=line_width,
        ).move_to([0, plane_posy, 0])

        start_path = -0.8
        start_detour = -0.2
        dx = start_detour - start_path
        t1 = 1 / 4
        t2 = 1 - t1
        dt = t2 - t1

        def approach(t):
            return (
                np.array([start_path + dx * (t / t1), plane_posy, 0])
                if t < t1
                else np.array([0, 0, 0])
            )

        def detour(t):
            if t1 <= t and t <= t2:
                return np.array(
                    [
                        start_detour * np.cos(np.pi / dt * (t - t1)),
                        plane_posy - start_detour * np.sin(np.pi / dt * (t - t1)),
                        0,
                    ]
                )
            return np.array([0, 0, 0])

        def escape(t):
            return (
                np.array([-start_detour + dx * ((t - t2) / (1 - t2)), plane_posy, 0])
                if t > t2
                else np.array([0, 0, 0])
            )

        detour_path = ParametricFunction(
            lambda t: approach(t) + detour(t) + escape(t),
            t_range=[0, 1],
            color=PATH_COLOR,
            stroke_width=2.5,
        )
        plane_label = MathTex(
            r"\mathbb{R}^2 \setminus \{(0,0)\}", font_size=26
        ).next_to(
            punctured_plane,
            DOWN,
            buff=0.2,
        )
        plane_conclusion = ScaledText(
            "Connexe par arcs (et donc connexe) : on peut contourner le point retiré",
            font_size=20,
            color=OPEN_SET_COLOR,
        ).next_to(plane_label, DOWN, buff=0.15)

        self.play(FadeIn(punctured_plane), run_time=SHORT_ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(Write(plane_label), FadeIn(removed_origin), run_time=WRITE_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(Create(detour_path), run_time=ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        self.play(Write(plane_conclusion), run_time=WRITE_TIME)
        self.wait(KEY_FRAME_WAIT)

        ccl_ylevel = -1
        proof = VGroup(
            line,
            removed_point,
            line_label,
            line_conclusion,
            left_part,
            right_part,
            punctured_plane,
            removed_origin,
            plane_label,
            detour_path,
            plane_conclusion,
        )
        proof2 = proof.copy().scale(0.6).move_to([-3.5, ccl_ylevel, 0])
        self.play(Transform(proof, proof2), run_time=ANIMATION_TIME)
        self.wait(INTER_ANIM_WAIT)

        ccl_font_size = 38
        imply = MathTex(r"\Longrightarrow ", font_size=ccl_font_size)
        imply.move_to([0, ccl_ylevel, 0])
        self.play(FadeIn(imply))
        self.wait(INTER_ANIM_WAIT)

        conclusion = MathTex(
            r"\mathbb{R} \not\cong \mathbb{R}^2",
            font_size=ccl_font_size,
        )
        conclusion.move_to([0, ccl_ylevel, 0]).shift(3 * RIGHT)
        box = SurroundingRectangle(conclusion, color=HIGHLIGHT_COLOR, buff=0.15)

        self.play(Write(conclusion), Create(box), run_time=WRITE_TIME)
        self.wait(KEY_FRAME_WAIT)
        self.end_of_section()
