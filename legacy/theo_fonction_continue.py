from manim import *
import numpy as np

class ConnectednessContinuousFunction(Scene):
    def construct(self):
      
        title_left = Text("Cercle : espace connexe", font_size=22, color=BLUE)
        title_left.to_edge(UP).shift(LEFT * 4.5)
        self.play(Write(title_left))

        circle = Circle(radius=1.2, color=PURPLE, fill_opacity=0.2)
        circle.move_to(LEFT * 4.5)
        self.play(Create(circle))
        self.wait(1)

        theta1 = 1.0
        theta2 = 4.0
        A = circle.point_at_angle(theta1)
        B = circle.point_at_angle(theta2)
        dotA = Dot(A, color=RED, radius=0.1)
        dotB = Dot(B, color=BLUE, radius=0.1)
        labA = Text("A", font_size=18).next_to(A, UR, buff=0.1)
        labB = Text("B", font_size=18).next_to(B, DL, buff=0.1)
        self.play(Create(dotA), Create(dotB), Write(labA), Write(labB))
        self.wait(1)

       
        title_mid = Text("Ensemble discrete {0,1}", font_size=22, color=BLUE)
        title_mid.to_edge(UP)
        self.play(Write(title_mid))

        p0 = Dot(LEFT * 1.0, color=RED, radius=0.12)
        p1 = Dot(RIGHT * 1.0, color=BLUE, radius=0.12)
        lab0 = Text("0", font_size=20).next_to(p0, DOWN)
        lab1 = Text("1", font_size=20).next_to(p1, DOWN)
        self.play(Create(p0), Create(p1), Write(lab0), Write(lab1))
        self.wait(1)

       
        title_right = Text("Caracterisation", font_size=22, color=BLUE)
        title_right.to_edge(UP).shift(RIGHT * 4.5)
        self.play(Write(title_right))

        th1 = VGroup(
            Text("X connexe si et seulement si", font_size=19),
            Text("toute fonction continue f: X->{0,1}", font_size=19),
            Text("est constante", font_size=19)
        ).arrange(DOWN, buff=0.15)
        th1.move_to(RIGHT * 4.5 + UP * 1.2) 
        self.play(Write(th1))
        self.wait(1)

        ivt = VGroup(
            Text("Theoreme des valeurs intermediaires :", font_size=18),
            Text("Si f continue sur [0,1]", font_size=18),
            Text("alors f prend toutes les valeurs", font_size=18),
            Text("entre f(0) et f(1)", font_size=18)
        ).arrange(DOWN, buff=0.15)
        ivt.move_to(RIGHT * 4.5 + UP * 0.0)  
        self.play(Write(ivt))
        self.wait(2)

        
        hypo = Text("Supposons f non constante continue", font_size=19, color=YELLOW)
        hypo.move_to(RIGHT * 4.5 + DOWN * 1.0)  
        self.play(Write(hypo))
        self.wait(1)

        arrA = Arrow(A, p0, color=YELLOW, stroke_width=2)
        arrB = Arrow(B, p1, color=YELLOW, stroke_width=2)
        fA = Text("f(A)=0", font_size=16, color=YELLOW).move_to(LEFT * 3.5 + DOWN * 1.0)
        fB = Text("f(B)=1", font_size=16, color=YELLOW).move_to(LEFT * 5.5 + DOWN * 1.0)
        self.play(Create(arrA), Create(arrB), Write(fA), Write(fB))
        self.wait(1)

        path = ArcBetweenPoints(A, B, radius=1.2, color=YELLOW)
        self.play(Create(path))
        self.wait(1)

        comp = VGroup(
            Text("g = f sur le chemin", font_size=18, color=YELLOW),
            Text("g: [0,1] -> {0,1} continue", font_size=18, color=YELLOW),
            Text("g(0)=0, g(1)=1", font_size=18, color=YELLOW)
        ).arrange(DOWN, buff=0.15)
        comp.move_to(RIGHT * 4.5 + DOWN * 2.0)  
        self.play(Write(comp))
        self.wait(1)

        contra = VGroup(
            Text("Contradiction !", font_size=20, color=RED),
            Text("TVI impose des valeurs entre 0 et 1", font_size=18, color=RED),
            Text("mais {0,1} n'en a pas", font_size=18, color=RED)
        ).arrange(DOWN, buff=0.15)
        contra.move_to(RIGHT * 4.5 + DOWN * 3.2)  
        self.play(Write(contra))
        self.wait(2)

       
        concl = VGroup(
            Text("Donc f ne peut pas etre non constante", font_size=20, color=GREEN),
            Text("f est necessairement constante", font_size=20, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        concl.to_edge(DOWN).shift(UP * 0.8)  
        self.play(Write(concl))
        self.wait(3)