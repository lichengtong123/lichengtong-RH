# -*- coding: utf-8 -*-
"""Critical-line values, their spatial lift, and component curves.

Video: python -m manim "Hardy 轨迹.py" zeta_3D_18H
Book: RH_RENDER_MODE=book python -m manim -s "Hardy 轨迹.py" HardyStill
The transverse coordinates are enlarged by AMPLIFY_FACTOR; t is unchanged.
"""
import os
import sys
from pathlib import Path

from manim import *
import numpy as np
from mpmath import mp, zeta, zetazero

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ch20_render import BOOK_MODE, THEME, configure_render

configure_render()
T_MAX = 80.0
DT = 0.08
AMPLIFY_FACTOR = 2.25
RUN_TIME = 35.0
mp.dps = 20


def critical_grid(t_max=T_MAX, dt=DT):
    """Include each displayed zero height, not just a nearby uniform sample."""
    zeros = []
    k = 1
    while True:
        gamma = float(zetazero(k).imag)
        if gamma > t_max:
            break
        zeros.append(gamma)
        k += 1
    uniform = np.linspace(0, t_max, int(np.ceil(t_max / dt)) + 1)
    return np.unique(np.concatenate((uniform, zeros))), zeros


def precompute_zeta_on_critical_line(t_grid, dps=20):
    with mp.workdps(dps):
        return np.array(
            [complex(zeta(complex(0.5, float(t)))) for t in t_grid],
            dtype=np.complex128,
        )


class zeta_3D_18H(ThreeDScene):
    def construct(self):
        t_grid, zeros = critical_grid()
        values = precompute_zeta_on_critical_line(t_grid)
        real = values.real * AMPLIFY_FACTOR
        imag = values.imag * AMPLIFY_FACTOR
        foreground = THEME["foreground"]
        main_color = THEME["main"]
        re_color, im_color = THEME["orange"], THEME["blue"]
        projection_color = THEME["boundary"]
        side_y = 19.0

        axes = ThreeDAxes(
            x_range=[0, 88, 10], y_range=[-28, 28, 10], z_range=[-28, 28, 10],
            x_length=12.0, y_length=6.0, z_length=6.0,
            axis_config={"color": THEME["muted"], "stroke_width": 1.3},
        )
        self.set_camera_orientation(phi=65 * DEGREES, theta=-65 * DEGREES, zoom=0.90)

        axis_labels = VGroup(
            MathTex("t", font_size=25, color=foreground).move_to(axes.c2p(89, 0, 0)),
            MathTex(r"2.25\,\operatorname{Im}w", font_size=21, color=im_color)
                .move_to(axes.c2p(0, 29, 0)),
            MathTex(r"2.25\,\operatorname{Re}w", font_size=21, color=re_color)
                .move_to(axes.c2p(0, 0, 30)),
        )
        self.add(axes)
        self.add_fixed_orientation_mobjects(*axis_labels)
        self.add(Line(axes.c2p(0, side_y, 0), axes.c2p(T_MAX, side_y, 0),
                      color=THEME["muted"], stroke_width=1, stroke_opacity=0.6))

        def coords(a, b, c):
            return np.array([axes.c2p(float(x), float(y), float(z))
                             for x, y, z in zip(a, b, c)])

        arrays = [
            coords(t_grid, imag, real),
            coords(np.zeros_like(t_grid), imag, real),
            coords(t_grid, np.full_like(t_grid, side_y), real),
            coords(t_grid, np.full_like(t_grid, side_y), imag),
        ]
        colors = [main_color, projection_color, re_color, im_color]
        curves = VGroup(*[
            VMobject(stroke_color=color, stroke_width=2.5)
                .set_points_as_corners(points[:2])
            for points, color in zip(arrays, colors)
        ])
        tracker = ValueTracker(0.0)

        def prefix(points, t):
            # Linear interpolation advances smoothly on the nonuniform grid.
            j = min(int(np.searchsorted(t_grid, t, side="right")), len(t_grid) - 1)
            if t >= t_grid[-1]:
                return points
            j = max(1, j)
            weight = (t - t_grid[j - 1]) / (t_grid[j] - t_grid[j - 1])
            endpoint = points[j - 1] + weight * (points[j] - points[j - 1])
            return np.vstack((points[:j], endpoint))

        def update_curves(_=None):
            for curve, points in zip(curves, arrays):
                curve.set_points_as_corners(prefix(points, tracker.get_value()))

        curves.add_updater(update_curves)
        moving_dot = Dot3D(arrays[0][0], color=THEME["zero"], radius=0.045)
        moving_dot.add_updater(
            lambda dot: dot.move_to(prefix(arrays[0], tracker.get_value())[-1])
        )
        self.add(curves, moving_dot)

        marks = []
        labeled_indices = {1, 5, 10, 15, len(zeros)}
        for k, gamma in enumerate(zeros, 1):
            j = int(np.searchsorted(t_grid, gamma))
            if abs(values[j]) > 1e-10:
                raise ValueError(f"Unexpected zero residual at gamma_{k}: {values[j]}")
            group = VGroup(
                Dot3D(axes.c2p(gamma, 0, 0), color=main_color, radius=0.035),
                Dot3D(axes.c2p(gamma, side_y, real[j]), color=re_color, radius=0.025),
                Dot3D(axes.c2p(gamma, side_y, imag[j]), color=im_color, radius=0.025),
            ).set_opacity(0)
            self.add(group)
            label = None
            if k in labeled_indices:
                label = MathTex(rf"\gamma_{{{k}}}={gamma:.2f}",
                                font_size=19, color=foreground)
                label.move_to(axes.c2p(gamma, -5.0 if k % 2 else -8.0, -3.5))
                self.add_fixed_orientation_mobjects(label)
                label.set_opacity(0)
            marks.append((gamma, group, label))

        def update_marks(_=None):
            for gamma, group, label in marks:
                visible = float(tracker.get_value() >= gamma)
                group.set_opacity(visible)
                if label is not None:
                    label.set_opacity(visible)

        marker_driver = VMobject()
        marker_driver.add_updater(update_marks)
        self.add(marker_driver)

        # Screen-fixed text remains readable instead of rotating with the scene.
        formula = MathTex(
            r"\zeta(\tfrac12+it)=e^{-i\vartheta(t)}Z(t),\qquad Z(t)\in\mathbb R",
            font_size=27, color=foreground,
        ).to_edge(DOWN, buff=0.23)
        legend = VGroup(*[
            Text(text, font_size=18, color=color)
            for text, color in [
                ("空间轨迹", main_color), ("平面投影", projection_color),
                ("实部分量", re_color), ("虚部分量", im_color),
            ]
        ]).arrange(RIGHT, buff=0.4).to_edge(UP, buff=0.2)
        scale_note = Text("横截面振幅 ×2.25；分量曲线平移至辅助平面",
                          font_size=16, color=THEME["muted"])
        scale_note.next_to(legend, DOWN, buff=0.10)

        count_prefix = MathTex(r"N_0(", font_size=25, color=foreground)
        time_readout = DecimalNumber(0, num_decimal_places=2, font_size=25, color=foreground)
        equals = MathTex(")=", font_size=25, color=foreground)
        count_readout = Integer(0, font_size=25, color=projection_color)
        count = VGroup(count_prefix, time_readout, equals, count_readout).arrange(RIGHT, buff=0.06)
        count.to_corner(DOWN + RIGHT, buff=0.25).shift(UP * 0.65)
        def update_count(group):
            self.camera.remove_fixed_in_frame_mobjects(group)
            time_readout.set_value(tracker.get_value())
            count_readout.set_value(sum(gamma <= tracker.get_value() for gamma in zeros))
            group.arrange(RIGHT, buff=0.06)
            group.to_corner(DOWN + RIGHT, buff=0.25).shift(UP * 0.65)
            # DecimalNumber replaces glyphs; register the new family as screen-fixed.
            self.camera.add_fixed_in_frame_mobjects(group)

        count.add_updater(update_count)
        self.add_fixed_in_frame_mobjects(formula, legend, scale_note, count)

        if getattr(self, "STILL", False) or BOOK_MODE:
            t = float(os.environ.get("T_STILL", str(T_MAX)))
            if not 0 <= t <= T_MAX:
                raise ValueError("T_STILL must be between 0 and T_MAX")
            tracker.set_value(t)
            self.update_mobjects(0)
        else:
            self.play(tracker.animate.set_value(T_MAX), run_time=RUN_TIME, rate_func=linear)
            self.wait(3)


class HardyStill(zeta_3D_18H):
    """A reproducible still; T_STILL defaults to 80."""
    STILL = True
