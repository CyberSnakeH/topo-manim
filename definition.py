from manim import *
import numpy as np

class ConnexeParArcsCercle(Scene):
    def construct(self):

       
        titre = Text("Connexité par arcs - Cercle", font_size=30, color=BLUE)
        titre.to_edge(UP, buff=0.5)
        self.play(Write(titre))
        self.wait(1)

        definition = VGroup(
            Text("Chemin continu :", font_size=22),
            Text("γ : [0, 1] → X", font_size=20),
            Text("γ(0) = point départ", font_size=18),
            Text("γ(1) = point arrivée", font_size=18),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        definition.move_to(LEFT * 3.5 + UP * 2.2)
        self.play(Write(definition))
        self.wait(1)

        axes = Axes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            x_length=5,
            y_length=5,
            axis_config={"color": BLUE_D}
        ).move_to(RIGHT * 2.5)

        r = 1.8
        cercle = Circle(radius=r, color=PURPLE, fill_opacity=0.2)
        cercle.move_to(axes.get_origin())
        self.play(Create(axes), Create(cercle))
        self.wait(1)

        angles = [1.2, 2.1, 3.6, 5.0] 
        dots = []       
        coords = []    
        labels = []    
        names = ["M1", "M2", "M3", "M4"]

        for i, theta in enumerate(angles):
            x = r * np.cos(theta)
            y = r * np.sin(theta)
            dot = Dot(axes.coords_to_point(x, y), color=RED, radius=0.1)
            lab = Text(f"{names[i]}({x:.1f}, {y:.1f})", font_size=16, color=RED)
            
            offset_dir = np.array([np.cos(theta), np.sin(theta), 0])
            lab.next_to(dot, offset_dir * 0.3)
            dots.append(dot)
            coords.append((x, y))
            labels.append(lab)

        
        self.play(*[Create(d) for d in dots], *[Write(l) for l in labels])
        self.wait(1.5)

      
        idx1, idx2 = 1, 3
        x0, y0 = coords[idx1]
        x1, y1 = coords[idx2]
        dot0, dot1 = dots[idx1], dots[idx2]

       
        select1 = Text("Premier choix : M2 et M4", font_size=18, color=YELLOW)
        select1.move_to(LEFT * 3.5 + UP * 0.6)
        self.play(Write(select1))
        self.wait(1)

        
        chemin1 = VGroup(
            Text("Équation du chemin :", font_size=20),
            Text(f"x(t) = {x0:.1f} + t·({x1:.1f} - {x0:.1f})", font_size=18),
            Text(f"y(t) = {y0:.1f} + t·({y1:.1f} - {y0:.1f})", font_size=18),
            Text("t ∈ [0, 1]", font_size=18, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        chemin1.move_to(LEFT * 3.5 + DOWN * 0.2)
        self.play(Write(chemin1))
        self.wait(1)

       
        def gamma1(t):
            x = x0 + t*(x1 - x0)
            y = y0 + t*(y1 - y0)
            return axes.coords_to_point(x, y)
        ligne1 = ParametricFunction(gamma1, t_range=[0,1], color=YELLOW, stroke_width=2)
        self.play(Create(ligne1))
        self.wait(1)

        point_mobile1 = Dot(gamma1(0), color=YELLOW, radius=0.12)
        t_affiche1 = Text("t = 0.00", font_size=20, color=YELLOW)
        t_affiche1.move_to(LEFT * 3.5 + DOWN * 1.8)
        self.play(Create(point_mobile1), Write(t_affiche1))

        for t in np.linspace(0, 1, 60):
            point_mobile1.move_to(gamma1(t))
            t_affiche1.become(Text(f"t = {t:.2f}", font_size=20, color=YELLOW).move_to(LEFT * 3.5 + DOWN * 1.8))
            self.wait(0.03)
        self.wait(2)

      
        self.play(FadeOut(select1, chemin1, ligne1, point_mobile1, t_affiche1))
        self.wait(0.5)

        
        idx3, idx4 = 0, 2
        x2, y2 = coords[idx3]
        x3, y3 = coords[idx4]
        dot2, dot3 = dots[idx3], dots[idx4]

       
        select2 = Text("Deuxième choix : M1 et M3", font_size=18, color=YELLOW)
        select2.move_to(LEFT * 3.5 + UP * 0.6)
        self.play(Write(select2))
        self.wait(1)

       
        chemin2 = VGroup(
            Text("Équation du chemin :", font_size=20),
            Text(f"x(t) = {x2:.1f} + t·({x3:.1f} - {x2:.1f})", font_size=18),
            Text(f"y(t) = {y2:.1f} + t·({y3:.1f} - {y2:.1f})", font_size=18),
            Text("t ∈ [0, 1]", font_size=18, color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        chemin2.move_to(LEFT * 3.5 + DOWN * 0.2)
        self.play(Write(chemin2))
        self.wait(1)

       
        def gamma2(t):
            x = x2 + t*(x3 - x2)
            y = y2 + t*(y3 - y2)
            return axes.coords_to_point(x, y)
        ligne2 = ParametricFunction(gamma2, t_range=[0,1], color=YELLOW, stroke_width=2)
        self.play(Create(ligne2))
        self.wait(1)

      
        point_mobile2 = Dot(gamma2(0), color=YELLOW, radius=0.12)
        t_affiche2 = Text("t = 0.00", font_size=20, color=YELLOW)
        t_affiche2.move_to(LEFT * 3.5 + DOWN * 1.8)
        self.play(Create(point_mobile2), Write(t_affiche2))

        for t in np.linspace(0, 1, 60):
            point_mobile2.move_to(gamma2(t))
            t_affiche2.become(Text(f"t = {t:.2f}", font_size=20, color=YELLOW).move_to(LEFT * 3.5 + DOWN * 1.8))
            self.wait(0.03)
        self.wait(2)

       
        self.play(FadeOut(definition, select2, chemin2, ligne2, point_mobile2, t_affiche2))
        conclu = Text("Le cercle est connexe par arcs", font_size=24, color=GREEN)
        conclu.to_edge(DOWN, buff=0.8)
        self.play(Write(conclu))
        self.wait(3)