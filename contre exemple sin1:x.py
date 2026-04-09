from manim import *
import numpy as np

class TopologistSineNotArcConnected(Scene):
    def construct(self):
        titre = Text("Courbe sinus du topologue : connexe mais non arc-connexe", font_size=30)
        sous_titre = Text("Topologist's Sine Curve", font_size=20, color=GREY)
        VGroup(titre, sous_titre).arrange(DOWN, buff=0.2).to_edge(UP, buff=0.6)
        self.play(Write(titre), Write(sous_titre))
        self.wait(2)

        axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[-1.2, 1.2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"color": BLUE_D},
        ).to_edge(DOWN, buff=1.0)

        label_x = Text("x", font_size=20).next_to(axes.x_axis, RIGHT, buff=0.2)
        label_y = Text("y", font_size=20).next_to(axes.y_axis, UP, buff=0.2)
        self.play(Create(axes), Write(label_x), Write(label_y))
        self.wait(1.5)

        def f(x):
            return np.sin(1 / x)

        x_vals = np.linspace(0.0002, 1, 40000)
        y_vals = f(x_vals)
        points = [axes.coords_to_point(x, y) for x, y in zip(x_vals, y_vals)]
        
        courbe = VMobject(color=ORANGE, stroke_width=1.5)
        courbe.set_points_smoothly(points)
        
        self.play(Create(courbe), run_time=4)
        self.wait(1.5)

        segment_limite = Line(
            start=axes.coords_to_point(0, -1),
            end=axes.coords_to_point(0, 1),
            color=PURPLE,
            stroke_width=3,
        )
        label_limite = Text("Segment limite x=0", font_size=20, color=PURPLE).next_to(segment_limite, LEFT, buff=0.3)
        self.play(Create(segment_limite), Write(label_limite))
        self.wait(2)

        x_A = 0.2
        y_A = np.sin(1 / x_A)
        pt_A = Dot(axes.coords_to_point(x_A, y_A), color=RED, radius=0.08)
        lab_A = Text("A", font_size=20, color=RED).next_to(pt_A, UR, buff=0.2)

        x_B, y_B = 0, 0.5
        pt_B = Dot(axes.coords_to_point(x_B, y_B), color=GREEN, radius=0.08)
        lab_B = Text("B", font_size=20, color=GREEN).next_to(pt_B, UL, buff=0.2)

        self.play(Create(pt_A), Create(pt_B), Write(lab_A), Write(lab_B))
        self.wait(1.5)

        question = Text(
            "Existe-t-il un chemin continu joignant A et B?",
            font_size=24
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(question))
        self.wait(3)
        self.play(FadeOut(question))

        t_vals = np.linspace(0.2, 0.01, 100)
        chemin = [axes.coords_to_point(x, f(x)) for x in t_vals]
        point_mobile = Dot(chemin[0], color=YELLOW, radius=0.1)

        self.play(Create(point_mobile))
        for p in chemin[1:]:
            point_mobile.move_to(p)
            self.wait(0.07)

        explication = Text(
            "Oscillations infinies et tres denses pres de 0",
            font_size=22, color=YELLOW
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(explication))
        self.wait(4)
        self.play(FadeOut(explication))

        ligne_echec = Line(pt_A.get_center(), pt_B.get_center(), color=ORANGE, stroke_width=2)
        croix = Cross(ligne_echec, color=RED, stroke_width=4)

        self.play(Create(ligne_echec))
        self.play(Create(croix)) 
        self.wait(2)

        conclusion = VGroup(
            Text("Impossible de relier A et B par un arc continu", font_size=24, color=RED),
            Text("-> Connexe mais NON arc-connexe", font_size=22, color=RED)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.4)

        self.play(Write(conclusion))
        self.wait(5)

        self.play(FadeOut(conclusion))
        final = Text(
            "L'arc-connexite est une condition plus forte que la connexite",
            font_size=26, color=BLUE
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(final))
        self.wait(5)