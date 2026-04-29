from manim import *
import numpy as np

class RegressionVsClassification(ThreeDScene):
    def construct(self):
        title = Text("Regression vs Classification", font_size=48)
        self.play(Write(title))
        self.wait(1)
        self.play(title.animate.to_edge(UP))

        # ---------------------------------------------------------
        # Part 1: Regression in 2D
        # ---------------------------------------------------------
        reg_title = Text("Regression: Fit through the points", font_size=36, color=BLUE).to_edge(UP)
        self.play(Transform(title, reg_title))

        axes2d = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": WHITE}
        )
        self.play(Create(axes2d))

        np.random.seed(42)
        x_vals = np.random.uniform(1, 9, 20)
        y_vals = x_vals * 0.8 + 1.5 + np.random.normal(0, 1, 20)
        reg_dots = VGroup(*[Dot(axes2d.c2p(x, y), color=YELLOW) for x, y in zip(x_vals, y_vals)])
        self.play(FadeIn(reg_dots))

        # Animate regression line finding fit
        w_reg = ValueTracker(0.0)
        b_reg = ValueTracker(5.0)
        reg_line = always_redraw(lambda: axes2d.plot(lambda x: w_reg.get_value() * x + b_reg.get_value(), color=RED))
        
        self.play(Create(reg_line))
        self.wait(0.5)
        # Moving to find the best fit line
        self.play(w_reg.animate.set_value(0.8), b_reg.animate.set_value(1.5), run_time=2, rate_func=smooth)
        self.wait(1)
        
        self.play(FadeOut(reg_dots), FadeOut(reg_line))

        # ---------------------------------------------------------
        # Part 2: Classification in 2D
        # ---------------------------------------------------------
        class_title = Text("Classification: Separate the classes", font_size=36, color=GREEN).to_edge(UP)
        self.play(Transform(title, class_title))

        # Two linearly separable classes
        # Class 1: Top Left
        class1_x = np.random.uniform(1, 4.5, 15)
        class1_y = np.random.uniform(5.5, 9, 15)
        # Class 2: Bottom Right
        class2_x = np.random.uniform(5.5, 9, 15)
        class2_y = np.random.uniform(1, 4.5, 15)

        class1_dots = VGroup(*[Dot(axes2d.c2p(x, y), color=BLUE) for x, y in zip(class1_x, class1_y)])
        class2_dots = VGroup(*[Dot(axes2d.c2p(x, y), color=ORANGE) for x, y in zip(class2_x, class2_y)])

        self.play(FadeIn(class1_dots), FadeIn(class2_dots))

        # Animate separation line finding the boundary
        # Starts with a bad guess that crosses through both classes
        w_cls = ValueTracker(-1.0)
        b_cls = ValueTracker(10.0)
        sep_line = always_redraw(lambda: axes2d.plot(lambda x: w_cls.get_value() * x + b_cls.get_value(), color=RED))
        
        self.play(Create(sep_line))
        self.wait(0.5)
        
        # Moves to isolate/separate the classes (y = x)
        self.play(w_cls.animate.set_value(1.0), b_cls.animate.set_value(0.0), run_time=2.5, rate_func=smooth)
        self.wait(1.5)
        
        self.play(FadeOut(axes2d), FadeOut(class1_dots), FadeOut(class2_dots), FadeOut(sep_line), FadeOut(title))

        # ---------------------------------------------------------
        # Part 3: Classification in 3D (Hyperplane)
        # ---------------------------------------------------------
        hyper_title = Text("Classification in 3D: Hyperplane", font_size=36, color=PURPLE)
        self.play(Write(hyper_title))
        self.wait(1)
        self.play(FadeOut(hyper_title))

        axes3d = ThreeDAxes(
            x_range=[-5, 5, 1],
            y_range=[-5, 5, 1],
            z_range=[-5, 5, 1],
            x_length=6,
            y_length=6,
            z_length=6
        )
        self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)
        self.play(Create(axes3d))

        c1_3d = VGroup(*[Dot3D(axes3d.c2p(
            np.random.uniform(-4, -1),
            np.random.uniform(-4, -1),
            np.random.uniform(1, 4)
        ), color=BLUE) for _ in range(20)])
        
        c2_3d = VGroup(*[Dot3D(axes3d.c2p(
            np.random.uniform(1, 4),
            np.random.uniform(1, 4),
            np.random.uniform(-4, -1)
        ), color=ORANGE) for _ in range(20)])

        self.play(FadeIn(c1_3d), FadeIn(c2_3d))
        self.wait(1)

        # Hyperplane
        hyperplane = Surface(
            lambda u, v: axes3d.c2p(u, v, -u - v),
            u_range=[-4, 4],
            v_range=[-4, 4],
            resolution=(10, 10)
        )
        hyperplane.set_style(fill_opacity=0.5, fill_color=RED, stroke_color=RED)
        
        self.play(Create(hyperplane))
        
        # Rotate camera to show the 3D perspective
        self.begin_ambient_camera_rotation(rate=0.2)
        self.wait(5)
        self.stop_ambient_camera_rotation()

        self.play(FadeOut(Group(*self.mobjects)))
