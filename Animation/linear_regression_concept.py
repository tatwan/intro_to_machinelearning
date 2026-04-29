from manim import *
import numpy as np

class LinearRegressionConcept(Scene):
    def construct(self):
        title = Text("Linear Regression: Learning Process", font_size=40).to_edge(UP)
        self.play(Write(title))

        # Setup Axes
        axes = Axes(
            x_range=[0, 10, 1],
            y_range=[0, 10, 1],
            x_length=6,
            y_length=5,
            axis_config={"color": WHITE}
        ).shift(DOWN * 0.5 + RIGHT * 1)
        
        labels = axes.get_axis_labels(x_label="X", y_label="Y")
        self.play(Create(axes), FadeIn(labels))

        # Generate scattered data points
        np.random.seed(42)
        x_vals = np.random.uniform(1, 9, 20)
        # True hidden relationship
        true_w = 0.8
        true_b = 1.5
        y_vals = x_vals * true_w + true_b + np.random.normal(0, 1, 20)
        
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW) for x, y in zip(x_vals, y_vals)])
        self.play(FadeIn(dots))

        # Value trackers for weight and bias
        # We start with a bad guess
        w_tracker = ValueTracker(-0.5)
        b_tracker = ValueTracker(8.0)

        # The line dynamically updates based on current w and b
        line = always_redraw(
            lambda: axes.plot(
                lambda x: w_tracker.get_value() * x + b_tracker.get_value(),
                color=RED
            )
        )
        self.play(Create(line))

        # Display the dynamically updating Equation and MSE
        equation_text = always_redraw(
            lambda: MathTex(
                f"Y = {w_tracker.get_value():.2f}X + {b_tracker.get_value():.2f}",
                font_size=36,
                color=RED
            ).to_edge(LEFT).shift(UP * 2)
        )

        mse_text = always_redraw(
            lambda: Text(
                f"Error (MSE): {np.mean((y_vals - (w_tracker.get_value() * x_vals + b_tracker.get_value()))**2):.2f}",
                font_size=24,
                color=ORANGE
            ).next_to(equation_text, DOWN, aligned_edge=LEFT)
        )

        self.play(Write(equation_text), FadeIn(mse_text))
        self.wait(1)

        # ---------------------------------------------------------
        # Animate the Learning Process (gradient descent conceptually)
        # ---------------------------------------------------------
        
        # Attempt 1
        self.play(
            w_tracker.animate.set_value(0.1),
            b_tracker.animate.set_value(6.0),
            run_time=2,
            rate_func=linear
        )
        self.wait(0.5)

        # Attempt 2
        self.play(
            w_tracker.animate.set_value(1.3),
            b_tracker.animate.set_value(0.5),
            run_time=2,
            rate_func=linear
        )
        self.wait(0.5)

        # Attempt 3: Settling on best fit
        best_w, best_b = np.polyfit(x_vals, y_vals, 1)

        self.play(
            w_tracker.animate.set_value(best_w),
            b_tracker.animate.set_value(best_b),
            run_time=3,
            rate_func=smooth
        )
        self.wait(1)

        # Success message
        learned_text = Text("Learned! Best Fit Found", font_size=28, color=GREEN).next_to(mse_text, DOWN, aligned_edge=LEFT)
        self.play(Write(learned_text))
        self.wait(3)

        self.play(FadeOut(Group(*self.mobjects)))
