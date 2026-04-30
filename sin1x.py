from manim import *
import numpy as np

class TopologistSineNotArcConnected(Scene):
    def construct(self):
        titre = Text("Courbe sinus du topologue : connexe mais non connexe par arc", font_size=28)
        sous_titre = Text("Topologist's Sine Curve", font_size=20, color=GREY)
        
        definition_math = MathTex(
            r"S = \left\{ \left(x, \sin\left(\frac{1}{x}\right)\right) \;\middle|\; x > 0 \right\} \cup \Big\{ (0, y) \;\Big|\; y \in [-1, 1] \Big\}", 
            font_size=28, color=YELLOW
        )
        
        titres = VGroup(titre, sous_titre, definition_math).arrange(DOWN, buff=0.25).to_edge(UP, buff=0.4)
        
        self.play(Write(titre), Write(sous_titre))
        self.wait(1)
        self.play(Write(definition_math), run_time=2)
        self.wait(2)

        axes = Axes(
            x_range=[0, 1.2, 0.2],
            y_range=[-1.2, 1.2, 0.5],
            x_length=6,
            y_length=4,
            axis_config={"color": BLUE_D},
        ).to_edge(DOWN, buff=0.8)

        label_x = Text("x", font_size=20).next_to(axes.x_axis, RIGHT, buff=0.2)
        label_y = Text("y", font_size=20).next_to(axes.y_axis, UP, buff=0.2)
        self.play(Create(axes), Write(label_x), Write(label_y), run_time=1.5)
        self.wait(1.5)

        def f(x):
            return np.sin(1 / x)

        x_vals = np.linspace(0.0002, 1, 40000)
        y_vals = f(x_vals)
        points = [axes.coords_to_point(x, y) for x, y in zip(x_vals, y_vals)]
        
        courbe = VMobject(color=ORANGE, stroke_width=1.5)
        courbe.set_points_smoothly(points)
        
        self.play(Create(courbe), run_time=6)
        self.wait(1.5)

        segment_limite = Line(
            start=axes.coords_to_point(0, -1),
            end=axes.coords_to_point(0, 1),
            color=PURPLE,
            stroke_width=3,
        )
        label_limite = Text("Segment limite x=0", font_size=20, color=PURPLE).next_to(segment_limite, LEFT, buff=0.3)
        self.play(Create(segment_limite), Write(label_limite), run_time=1.5)
        self.wait(2)

        graph_group = VGroup(axes, courbe, segment_limite)

        titre_connexe = Text("1. Pourquoi l'ensemble est-il Connexe ?", font_size=24, color=GREEN).to_edge(DOWN, buff=0.5)
        self.play(Write(titre_connexe))
        self.wait(2.5)

        exp_base_1 = Text("La sous-courbe (pour x > 0) est l'image continue d'un intervalle,", font_size=22).to_edge(DOWN, buff=0.8)
        exp_base_2 = Text("elle est donc d'un seul tenant (connexe).", font_size=22).next_to(exp_base_1, DOWN, buff=0.1)
        
        self.play(FadeOut(titre_connexe))
        self.play(Write(exp_base_1))
        self.play(Write(exp_base_2))
        self.wait(3.5)
        self.play(FadeOut(exp_base_1), FadeOut(exp_base_2))

        x_P, y_P = 0, 0.4
        pt_P = Dot(axes.coords_to_point(x_P, y_P), color=WHITE, radius=0.005)
        lab_P = Text("P", font_size=16, color=WHITE).next_to(pt_P, LEFT, buff=0.1)
        self.play(Create(pt_P), Write(lab_P))

        lab_P.add_updater(lambda m: m.next_to(pt_P, LEFT, buff=0.1))
        graph_group.add(pt_P)
        graph_group.save_state()

        self.play(FadeOut(label_x), FadeOut(label_y), FadeOut(label_limite))

        self.play(
            graph_group.animate.scale(8, about_point=pt_P.get_center()).shift(-pt_P.get_center()),
            run_time=3
        )
        self.wait(1)

        ouvert = Circle(radius=0.1, color=GREEN_B, fill_opacity=0.3).move_to(ORIGIN)
        lab_ouvert = Text("Voisinage ouvert U", font_size=24, color=GREEN_B).next_to(ouvert, UP, buff=0.1)
        self.play(Create(ouvert), Write(lab_ouvert), run_time=0.3)
        self.wait(1)

        exp_1 = Text("Tout voisinage U d'un point\ndu segment limite", font_size=23).to_edge(LEFT, buff=0.5).shift(UP*1)
        exp_2 = Text("intersecte la courbe à cause\nde la densité des oscillations.", font_size=23).next_to(exp_1, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(exp_1))
        self.wait(1)
        self.play(Write(exp_2))
        self.wait(4.5) 
        self.play(FadeOut(exp_1), FadeOut(exp_2))

        exp_3 = Text("Le segment limite est donc\ntotalement inclus dans\nl'adhérence de la courbe.", font_size=23).to_edge(LEFT, buff=0.5)
        self.play(Write(exp_3))
        self.wait(4)
        self.play(FadeOut(exp_3))

        exp_4 = Text("Théorème : Si un ensemble est\nconnexe, son adhérence l'est aussi.", font_size=23, color=YELLOW).to_edge(LEFT, buff=0.5).shift(UP*0.5)
        exp_5 = Text("Il est impossible de séparer l'union\nen deux ouverts disjoints.", font_size=23, color=YELLOW).next_to(exp_4, DOWN, aligned_edge=LEFT, buff=0.3)
        self.play(Write(exp_4))
        self.wait(2)
        self.play(Write(exp_5))
        self.wait(4)
        self.play(FadeOut(exp_4), FadeOut(exp_5))

        conclusion_connexe = Text("Conclusion :\nL'espace total est donc CONNEXE.", font_size=25, color=GREEN_B).to_edge(LEFT, buff=0.5)
        self.play(Write(conclusion_connexe))
        self.wait(3.5)

        self.play(
            Restore(graph_group),
            FadeIn(label_x), FadeIn(label_y), FadeIn(label_limite),
            FadeOut(conclusion_connexe), FadeOut(ouvert), FadeOut(lab_ouvert), 
            run_time=3
        )
        
        lab_P.clear_updaters()
        self.play(FadeOut(pt_P), FadeOut(lab_P))
        self.wait(1.5)

        titre_non_arc = Text("2. Mais est-il Connexe par arc ?", font_size=24, color=RED).to_edge(DOWN, buff=0.5)
        self.play(Write(titre_non_arc))
        self.wait(2.5) 
        self.play(FadeOut(titre_non_arc))

        x_A = 0.2
        y_A = np.sin(1 / x_A)
        pt_A = Dot(axes.coords_to_point(x_A, y_A), color=RED, radius=0.08)
        lab_A = Text("A", font_size=20, color=RED).next_to(pt_A, UR, buff=0.2)

        x_B, y_B = 0, 0.5
        pt_B = Dot(axes.coords_to_point(x_B, y_B), color=RED_B, radius=0.08)
        lab_B = Text("B", font_size=20, color=RED_B).next_to(pt_B, UL, buff=0.2)

        self.play(Create(pt_A), Write(lab_A))
        self.wait(0.5)
        self.play(Create(pt_B), Write(lab_B))
        self.wait(1.5)

        question = Text(
            "Existe-t-il un chemin continu joignant A et B?",
            font_size=24
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(question))
        self.wait(3.5)
        self.play(FadeOut(question))

        t_vals = np.linspace(0.2, 0.01, 100)
        chemin = [axes.coords_to_point(x, f(x)) for x in t_vals]
        point_mobile = Dot(chemin[0], color=YELLOW, radius=0.1)

        self.play(Create(point_mobile))
        for p in chemin[1:]:
            point_mobile.move_to(p)
            self.wait(0.12)

        explication = Text(
            "La limite d'un tel chemin n'existe pas (oscillations denses).",
            font_size=22, color=YELLOW
        ).to_edge(DOWN, buff=0.5)
        self.play(Write(explication))
        self.wait(4.5) 
        self.play(FadeOut(explication))

        ligne_echec = Line(pt_A.get_center(), pt_B.get_center(), color=ORANGE, stroke_width=2)
        croix = Cross(ligne_echec, color=RED, stroke_width=4)

        self.play(Create(ligne_echec), run_time=1.5)
        self.wait(0.5)
        self.play(Create(croix), run_time=1.5) 
        self.wait(2.5)

        conclusion = VGroup(
            Text("Impossible de relier A et B par un chemin continu", font_size=24, color=RED),
            Text("-> Connexe mais NON connexe par arc", font_size=22, color=RED)
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.5)

        self.play(Write(conclusion), run_time=2)
        self.wait(5) 

        self.play(FadeOut(conclusion))
        
        final = Text(
            "La connexité par arc est une condition plus forte que la connexité",
            font_size=24, color=BLUE
        ).to_edge(DOWN, buff=0.5)
        
        self.play(Write(final), run_time=2)
        self.wait(5)
