# ζ 共形映射-100.py
# 由 ζ 共形映射.py 扩展：前 50 个非平凡零点 + 共轭，共 100 个零点
# 再增加 50 个平凡零点 s = -2, -4, ..., -100，蓝色显示
# 新增：一条黄色 y 轴（虚轴），从屏幕下边沿延伸到上边沿
# 新增：一条黄色 x 轴（实轴），从屏幕左边沿延伸到右边沿，线宽 1.5
# 新增：坐标轴、0 点和数值标注显示在最上层
# 修改：关闭 Axes 自带的短刻度线，只保留手写数值标注
from manim import *
import numpy as np
from mpmath import mp, zeta
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ch20_render import BOOK_MODE, PREVIEW, THEME, configure_render

configure_render()
RED, BLUE, GREEN = THEME["zero"], THEME["blue"], THEME["boundary"]
YELLOW, GRAY, GRAY_B, GRAY_D = (THEME["foreground"], THEME["muted"],
                                THEME["grid"], THEME["muted"])
DISPLAY_LIMIT = 30.0
POLE_EPSILON = 1e-6
mp.dps = 18

class ZetaConformalMap(Scene):
    def construct(self):
        # ------------------ 参数区 ------------------
        x_range_min, x_range_max = -20, 20
        y_range_min, y_range_max = -12, 12

        points_per_line = 80 if PREVIEW else 240

        # ------------------ 粉红 / 蓝色细网格 ------------------
        fine_step = 0.25 if PREVIEW else 0.10
        pink_v_x0, pink_v_x1 = 1.01, 4.0
        pink_h_x0, pink_h_x1 = 1.0, 7.0
        pink_h_y0, pink_h_y1 = -2.0, 2.0
        pink_v_y0, pink_v_y1 = -4.0, 4.0
        blue_v_start = 0.99

        # ------------------ 坐标系 ------------------
        plane = Axes(
            x_range=[x_range_min, x_range_max, 2],
            y_range=[y_range_min, y_range_max, 2],
            axis_config={
                "include_tip": False,
                "include_ticks": False,
                "include_numbers": False,
                "color": GRAY_D,
                "stroke_width": 1.5,
            }
        )

        coord_grid = VGroup()
        grid_kw = dict(color=GRAY_B, stroke_width=0.6, stroke_opacity=0.45)
        half_w = config.frame_width / 2
        half_h = config.frame_height / 2
        origin_sc = plane.coords_to_point(0, 0)
        ux = (plane.coords_to_point(1, 0) - origin_sc)[0]
        uy = (plane.coords_to_point(0, 1) - origin_sc)[1]
        ox, oy = origin_sc[0], origin_sc[1]
        n_x_min = int(np.floor((-half_w - ox) / ux)) - 1
        n_x_max = int(np.ceil((half_w - ox) / ux)) + 1
        n_y_min = int(np.floor((-half_h - oy) / uy)) - 1
        n_y_max = int(np.ceil((half_h - oy) / uy)) + 1
        for n in range(n_x_min, n_x_max + 1):
            x = ox + n * ux
            coord_grid.add(Line(
                np.array([x, -half_h, 0.0]),
                np.array([x, half_h, 0.0]),
                **grid_kw,
            ))
        for n in range(n_y_min, n_y_max + 1):
            y = oy + n * uy
            coord_grid.add(Line(
                np.array([-half_w, y, 0.0]),
                np.array([half_w, y, 0.0]),
                **grid_kw,
            ))

        # 只保留数值标注，不画刻度线
        x_ticks = VGroup()
        for x in range(x_range_min, x_range_max + 1, 2):
            if x == 0:
                continue
            point = plane.coords_to_point(x, 0)
            label = MathTex(str(x), font_size=21, color=GRAY)
            label.next_to(point, DOWN, buff=0.2)
            x_ticks.add(label)

        y_ticks = VGroup()
        for y in range(y_range_min, y_range_max + 1, 2):
            if y == 0:
                continue
            point = plane.coords_to_point(0, y)
            if y == 1:
                label = MathTex(r"i", font_size=23, color=BLUE)
            elif y == -1:
                label = MathTex(r"-i", font_size=23, color=BLUE)
            else:
                label = MathTex(f"{y}i", font_size=21, color=BLUE)
            label.next_to(point, LEFT, buff=0.2)
            y_ticks.add(label)

        origin_point = plane.coords_to_point(0, 0)
        origin_label = MathTex("0", font_size=21, color=GRAY)
        origin_label.next_to(origin_point, DOWN+RIGHT, buff=0.1)

        # 黄色 y 轴（虚轴），从屏幕下边沿延伸到上边沿
        y_axis_yellow = Line(
            np.array([ox, -half_h, 0.0]),
            np.array([ox,  half_h, 0.0]),
            color=YELLOW,
            stroke_width=1.5,
        )

        # 黄色 x 轴（实轴），从屏幕左边沿延伸到右边沿
        x_axis_yellow = Line(
            np.array([-half_w, oy, 0.0]),
            np.array([ half_w, oy, 0.0]),
            color=YELLOW,
            stroke_width=1.5,
        )

        # 坐标轴、0 点和数值标注置于最上层
        coord_grid.set_z_index(100)
        plane.set_z_index(100)
        y_axis_yellow.set_z_index(103)
        x_axis_yellow.set_z_index(103)
        x_ticks.set_z_index(104)
        y_ticks.set_z_index(104)
        origin_label.set_z_index(104)

        self.add(
            coord_grid, plane,
            y_axis_yellow,
            x_axis_yellow,
            x_ticks, y_ticks, origin_label,
        )

        # ------------------ 公式与文字 ------------------
        formula_def = MathTex(
            r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} = \prod_p \frac{1}{1-p^{-s}}\ (\operatorname{Re}s>1)",
            font_size=23,
            color=THEME["foreground"],
        ).to_edge(UL, buff=0.5).shift(0.2*DOWN)

        formula_feq = MathTex(
            r"\zeta(s) = 2^s \pi^{s-1} \sin\!\left(\frac{\pi s}{2}\right) \Gamma(1-s)\,\zeta(1-s)",
            font_size=23,
            color=THEME["foreground"],
        ).next_to(formula_def, DOWN, aligned_edge=LEFT, buff=0.25)

        formula = VGroup(formula_def, formula_feq)

        alpha_tracker = ValueTracker(0)

        progress = always_redraw(lambda:
            Text(f"变换进度：{int(alpha_tracker.get_value()*100)}%",
                 font_size=21, color=THEME["muted"])
            .next_to(formula_feq, DOWN, aligned_edge=LEFT, buff=0.35)
        )

        self.add(formula, progress)

        display_note = Text(
            "绿色填充示意临界带边界的形变，不表示像集的精确范围。\n"
            "零点标签表示原位置；显示截限 |ζ|≤30。",
            font_size=15, color=THEME["muted"],
        ).to_corner(DOWN + LEFT, buff=0.35)
        note_background = BackgroundRectangle(
            display_note, color=WHITE, fill_opacity=1.0,
            stroke_width=0, buff=0.08,
        ).set_z_index(109)
        display_note.set_z_index(110)
        self.add(note_background, display_note)

        # ------------------ zeta 映射函数 ------------------
        def zeta_mapped(x, y, alpha):
            s = complex(x, y)
            if abs(s - 1.0) < POLE_EPSILON:
                # A finite drawing placeholder, not a value assigned to zeta(1).
                z = complex(DISPLAY_LIMIT, 0.0)
            else:
                z = complex(zeta(s))
                if not np.isfinite(z.real) or not np.isfinite(z.imag):
                    raise ValueError(f"Non-finite zeta sample at {s}")
            limit = DISPLAY_LIMIT
            if abs(z) > limit:
                z = z / abs(z) * limit
            mapped = (1 - alpha) * s + alpha * z
            return mapped

        # ------------------ 细网格 ------------------
        def _c2s(carr: np.ndarray) -> np.ndarray:
            out = np.zeros((len(carr), 3))
            for i, c in enumerate(carr):
                out[i] = plane.coords_to_point(float(c.real), float(c.imag))
            return out

        def _precompute_segment(z0: complex, z1: complex):
            ts = np.linspace(0.0, 1.0, points_per_line)
            src = np.array([(1 - t) * z0 + t * z1 for t in ts], dtype=complex)
            dst = np.array(
                [zeta_mapped(float(p.real), float(p.imag), 1.0) for p in src],
                dtype=complex,
            )
            return _c2s(src), _c2s(dst)

        pink_re = np.round(np.arange(pink_v_x0, pink_v_x1 + 0.5 * fine_step, fine_step), 10)
        pink_re = pink_re[(pink_re >= pink_v_x0 - 1e-12) & (pink_re <= pink_v_x1 + 1e-12)]
        pink_re = pink_re[np.abs(pink_re - 1.0) > 1e-9]
        pink_im = np.round(np.arange(pink_h_y0, pink_h_y1 + 0.5 * fine_step, fine_step), 10)
        pink_im = pink_im[(pink_im >= pink_h_y0 - 1e-12) & (pink_im <= pink_h_y1 + 1e-12)]

        blue_re = np.unique(np.round(2.0 - pink_re, 10))
        blue_re = blue_re[np.abs(blue_re - 1.0) > 1e-9]
        blue_re = blue_re[blue_re <= blue_v_start + 1e-12]
        if not np.any(np.abs(blue_re - blue_v_start) < 1e-9):
            blue_re = np.unique(np.concatenate([blue_re, [blue_v_start]]))
        blue_h_x0, blue_h_x1 = -5.0, 1.0

        pink0 = ManimColor("#A14A70")
        pink1 = ManimColor("#B68198")
        blue0 = ManimColor(THEME["blue"])
        blue1 = ManimColor("#7096B9")

        def _build_line_groups(v_xs, h_ys, h_x_lo, h_x_hi, v_y_lo, v_y_hi, col0, col1):
            v_src_sc, v_dst_sc, h_src_sc, h_dst_sc = [], [], [], []
            for x in v_xs:
                s, d = _precompute_segment(complex(x, v_y_hi), complex(x, v_y_lo))
                v_src_sc.append(s)
                v_dst_sc.append(d)
            for y in h_ys:
                s, d = _precompute_segment(complex(h_x_lo, y), complex(h_x_hi, y))
                h_src_sc.append(s)
                h_dst_sc.append(d)
            n_v, n_h = len(v_src_sc), len(h_src_sc)
            v_group, h_group = VGroup(), VGroup()
            for i, sc in enumerate(v_src_sc):
                col = interpolate_color(col1, col0, i / max(n_v - 1, 1))
                line = VMobject(stroke_color=col, stroke_width=1.0, stroke_opacity=0.75)
                line.set_points_smoothly([sc[j] for j in range(len(sc))])
                v_group.add(line)
            for i, sc in enumerate(h_src_sc):
                col = interpolate_color(col0, col1, i / max(n_h - 1, 1))
                line = VMobject(stroke_color=col, stroke_width=1.0, stroke_opacity=0.75)
                line.set_points_smoothly([sc[j] for j in range(len(sc))])
                h_group.add(line)

            def make_upd(src_list, dst_list):
                def upd(mob: VGroup):
                    a = alpha_tracker.get_value()
                    b = 1.0 - a
                    for line, src, dst in zip(mob, src_list, dst_list):
                        mid = b * src + a * dst
                        line.set_points_smoothly([mid[j] for j in range(len(mid))])
                return upd

            return (
                v_group, h_group,
                make_upd(v_src_sc, v_dst_sc),
                make_upd(h_src_sc, h_dst_sc),
            )

        v_lines_pink, h_lines_pink, update_v_pink, update_h_pink = _build_line_groups(
            pink_re, pink_im,
            pink_h_x0, pink_h_x1, pink_v_y0, pink_v_y1,
            pink0, pink1,
        )
        v_lines_blue, h_lines_blue, update_v_blue, update_h_blue = _build_line_groups(
            blue_re, pink_im,
            blue_h_x0, blue_h_x1, pink_v_y0, pink_v_y1,
            blue0, blue1,
        )

        # ------------------ 前五十个非平凡零点及其共轭 ------------------
        zero_label_buff = 0.08
        zero_label_nudge = 0.10

        def label_nudge_vec(t):
            return (DOWN if t >= 0 else UP) * zero_label_nudge

        zero_data = [
            {"t": 14.134725141735,  "label": "\\rho_1 = \\frac{1}{2} + 14.13i", "direction": UR},
            {"t": -14.134725141735, "label": "\\bar{\\rho}_1 = \\frac{1}{2} - 14.13i", "direction": DR},
            {"t": 21.022039638772,  "label": "\\rho_{2} = \\frac{1}{2} + 21.02i", "direction": UR},
            {"t": -21.022039638772, "label": "\\bar{\\rho}_{2} = \\frac{1}{2} - 21.02i", "direction": DR},
            {"t": 25.010857580146,  "label": "\\rho_{3} = \\frac{1}{2} + 25.01i", "direction": UR},
            {"t": -25.010857580146, "label": "\\bar{\\rho}_{3} = \\frac{1}{2} - 25.01i", "direction": DR},
            {"t": 30.424876125860,  "label": "\\rho_{4} = \\frac{1}{2} + 30.42i", "direction": UR},
            {"t": -30.424876125860, "label": "\\bar{\\rho}_{4} = \\frac{1}{2} - 30.42i", "direction": DR},
            {"t": 32.935061587739,  "label": "\\rho_{5} = \\frac{1}{2} + 32.94i", "direction": UR},
            {"t": -32.935061587739, "label": "\\bar{\\rho}_{5} = \\frac{1}{2} - 32.94i", "direction": DR},
            {"t": 37.586178158826,  "label": "\\rho_{6} = \\frac{1}{2} + 37.59i", "direction": UR},
            {"t": -37.586178158826, "label": "\\bar{\\rho}_{6} = \\frac{1}{2} - 37.59i", "direction": DR},
            {"t": 40.918719012147,  "label": "\\rho_{7} = \\frac{1}{2} + 40.92i", "direction": UR},
            {"t": -40.918719012147, "label": "\\bar{\\rho}_{7} = \\frac{1}{2} - 40.92i", "direction": DR},
            {"t": 43.327073280915,  "label": "\\rho_{8} = \\frac{1}{2} + 43.33i", "direction": UR},
            {"t": -43.327073280915, "label": "\\bar{\\rho}_{8} = \\frac{1}{2} - 43.33i", "direction": DR},
            {"t": 48.005150881167,  "label": "\\rho_{9} = \\frac{1}{2} + 48.01i", "direction": UR},
            {"t": -48.005150881167, "label": "\\bar{\\rho}_{9} = \\frac{1}{2} - 48.01i", "direction": DR},
            {"t": 49.773832477672,  "label": "\\rho_{10} = \\frac{1}{2} + 49.77i", "direction": UR},
            {"t": -49.773832477672, "label": "\\bar{\\rho}_{10} = \\frac{1}{2} - 49.77i", "direction": DR},
            {"t": 52.970321477714,  "label": "\\rho_{11} = \\frac{1}{2} + 52.97i", "direction": UR},
            {"t": -52.970321477714, "label": "\\bar{\\rho}_{11} = \\frac{1}{2} - 52.97i", "direction": DR},
            {"t": 56.446247697063,  "label": "\\rho_{12} = \\frac{1}{2} + 56.45i", "direction": UR},
            {"t": -56.446247697063, "label": "\\bar{\\rho}_{12} = \\frac{1}{2} - 56.45i", "direction": DR},
            {"t": 59.347044002602,  "label": "\\rho_{13} = \\frac{1}{2} + 59.35i", "direction": UR},
            {"t": -59.347044002602, "label": "\\bar{\\rho}_{13} = \\frac{1}{2} - 59.35i", "direction": DR},
            {"t": 60.831778524610,  "label": "\\rho_{14} = \\frac{1}{2} + 60.83i", "direction": UR},
            {"t": -60.831778524610, "label": "\\bar{\\rho}_{14} = \\frac{1}{2} - 60.83i", "direction": DR},
            {"t": 65.112544048082,  "label": "\\rho_{15} = \\frac{1}{2} + 65.11i", "direction": UR},
            {"t": -65.112544048082, "label": "\\bar{\\rho}_{15} = \\frac{1}{2} - 65.11i", "direction": DR},
            {"t": 67.079810529494,  "label": "\\rho_{16} = \\frac{1}{2} + 67.08i", "direction": UR},
            {"t": -67.079810529494, "label": "\\bar{\\rho}_{16} = \\frac{1}{2} - 67.08i", "direction": DR},
            {"t": 69.546401711174,  "label": "\\rho_{17} = \\frac{1}{2} + 69.55i", "direction": UR},
            {"t": -69.546401711174, "label": "\\bar{\\rho}_{17} = \\frac{1}{2} - 69.55i", "direction": DR},
            {"t": 72.067157674482,  "label": "\\rho_{18} = \\frac{1}{2} + 72.07i", "direction": UR},
            {"t": -72.067157674482, "label": "\\bar{\\rho}_{18} = \\frac{1}{2} - 72.07i", "direction": DR},
            {"t": 75.704690699084,  "label": "\\rho_{19} = \\frac{1}{2} + 75.70i", "direction": UR},
            {"t": -75.704690699084, "label": "\\bar{\\rho}_{19} = \\frac{1}{2} - 75.70i", "direction": DR},
            {"t": 77.144840068875,  "label": "\\rho_{20} = \\frac{1}{2} + 77.14i", "direction": UR},
            {"t": -77.144840068875, "label": "\\bar{\\rho}_{20} = \\frac{1}{2} - 77.14i", "direction": DR},
            {"t": 79.337375020249,  "label": "\\rho_{21} = \\frac{1}{2} + 79.34i", "direction": UR},
            {"t": -79.337375020249, "label": "\\bar{\\rho}_{21} = \\frac{1}{2} - 79.34i", "direction": DR},
            {"t": 82.910380854086,  "label": "\\rho_{22} = \\frac{1}{2} + 82.91i", "direction": UR},
            {"t": -82.910380854086, "label": "\\bar{\\rho}_{22} = \\frac{1}{2} - 82.91i", "direction": DR},
            {"t": 84.735492980517,  "label": "\\rho_{23} = \\frac{1}{2} + 84.74i", "direction": UR},
            {"t": -84.735492980517, "label": "\\bar{\\rho}_{23} = \\frac{1}{2} - 84.74i", "direction": DR},
            {"t": 87.425274613125,  "label": "\\rho_{24} = \\frac{1}{2} + 87.43i", "direction": UR},
            {"t": -87.425274613125, "label": "\\bar{\\rho}_{24} = \\frac{1}{2} - 87.43i", "direction": DR},
            {"t": 88.809111207634,  "label": "\\rho_{25} = \\frac{1}{2} + 88.81i", "direction": UR},
            {"t": -88.809111207634, "label": "\\bar{\\rho}_{25} = \\frac{1}{2} - 88.81i", "direction": DR},
            {"t": 92.491899270558,  "label": "\\rho_{26} = \\frac{1}{2} + 92.49i", "direction": UR},
            {"t": -92.491899270558, "label": "\\bar{\\rho}_{26} = \\frac{1}{2} - 92.49i", "direction": DR},
            {"t": 94.651344040520,  "label": "\\rho_{27} = \\frac{1}{2} + 94.65i", "direction": UR},
            {"t": -94.651344040520, "label": "\\bar{\\rho}_{27} = \\frac{1}{2} - 94.65i", "direction": DR},
            {"t": 95.870634228245,  "label": "\\rho_{28} = \\frac{1}{2} + 95.87i", "direction": UR},
            {"t": -95.870634228245, "label": "\\bar{\\rho}_{28} = \\frac{1}{2} - 95.87i", "direction": DR},
            {"t": 98.831194218194,  "label": "\\rho_{29} = \\frac{1}{2} + 98.83i", "direction": UR},
            {"t": -98.831194218194, "label": "\\bar{\\rho}_{29} = \\frac{1}{2} - 98.83i", "direction": DR},
            {"t": 101.317851005731, "label": "\\rho_{30} = \\frac{1}{2} + 101.32i", "direction": UR},
            {"t": -101.317851005731, "label": "\\bar{\\rho}_{30} = \\frac{1}{2} - 101.32i", "direction": DR},
            {"t": 103.725538040478, "label": "\\rho_{31} = \\frac{1}{2} + 103.73i", "direction": UR},
            {"t": -103.725538040478, "label": "\\bar{\\rho}_{31} = \\frac{1}{2} - 103.73i", "direction": DR},
            {"t": 105.446623052326, "label": "\\rho_{32} = \\frac{1}{2} + 105.45i", "direction": UR},
            {"t": -105.446623052326, "label": "\\bar{\\rho}_{32} = \\frac{1}{2} - 105.45i", "direction": DR},
            {"t": 107.168611184276, "label": "\\rho_{33} = \\frac{1}{2} + 107.17i", "direction": UR},
            {"t": -107.168611184276, "label": "\\bar{\\rho}_{33} = \\frac{1}{2} - 107.17i", "direction": DR},
            {"t": 111.029535543170, "label": "\\rho_{34} = \\frac{1}{2} + 111.03i", "direction": UR},
            {"t": -111.029535543170, "label": "\\bar{\\rho}_{34} = \\frac{1}{2} - 111.03i", "direction": DR},
            {"t": 111.874659176993, "label": "\\rho_{35} = \\frac{1}{2} + 111.87i", "direction": UR},
            {"t": -111.874659176993, "label": "\\bar{\\rho}_{35} = \\frac{1}{2} - 111.87i", "direction": DR},
            {"t": 114.320220915453, "label": "\\rho_{36} = \\frac{1}{2} + 114.32i", "direction": UR},
            {"t": -114.320220915453, "label": "\\bar{\\rho}_{36} = \\frac{1}{2} - 114.32i", "direction": DR},
            {"t": 116.226680320858, "label": "\\rho_{37} = \\frac{1}{2} + 116.23i", "direction": UR},
            {"t": -116.226680320858, "label": "\\bar{\\rho}_{37} = \\frac{1}{2} - 116.23i", "direction": DR},
            {"t": 118.790782865976, "label": "\\rho_{38} = \\frac{1}{2} + 118.79i", "direction": UR},
            {"t": -118.790782865976, "label": "\\bar{\\rho}_{38} = \\frac{1}{2} - 118.79i", "direction": DR},
            {"t": 121.370125002421, "label": "\\rho_{39} = \\frac{1}{2} + 121.37i", "direction": UR},
            {"t": -121.370125002421, "label": "\\bar{\\rho}_{39} = \\frac{1}{2} - 121.37i", "direction": DR},
            {"t": 122.946829293553, "label": "\\rho_{40} = \\frac{1}{2} + 122.95i", "direction": UR},
            {"t": -122.946829293553, "label": "\\bar{\\rho}_{40} = \\frac{1}{2} - 122.95i", "direction": DR},
            {"t": 124.256818554346, "label": "\\rho_{41} = \\frac{1}{2} + 124.26i", "direction": UR},
            {"t": -124.256818554346, "label": "\\bar{\\rho}_{41} = \\frac{1}{2} - 124.26i", "direction": DR},
            {"t": 127.516683879596, "label": "\\rho_{42} = \\frac{1}{2} + 127.52i", "direction": UR},
            {"t": -127.516683879596, "label": "\\bar{\\rho}_{42} = \\frac{1}{2} - 127.52i", "direction": DR},
            {"t": 129.578704199956, "label": "\\rho_{43} = \\frac{1}{2} + 129.58i", "direction": UR},
            {"t": -129.578704199956, "label": "\\bar{\\rho}_{43} = \\frac{1}{2} - 129.58i", "direction": DR},
            {"t": 131.087688530933, "label": "\\rho_{44} = \\frac{1}{2} + 131.09i", "direction": UR},
            {"t": -131.087688530933, "label": "\\bar{\\rho}_{44} = \\frac{1}{2} - 131.09i", "direction": DR},
            {"t": 133.497737202998, "label": "\\rho_{45} = \\frac{1}{2} + 133.50i", "direction": UR},
            {"t": -133.497737202998, "label": "\\bar{\\rho}_{45} = \\frac{1}{2} - 133.50i", "direction": DR},
            {"t": 134.756509753374, "label": "\\rho_{46} = \\frac{1}{2} + 134.76i", "direction": UR},
            {"t": -134.756509753374, "label": "\\bar{\\rho}_{46} = \\frac{1}{2} - 134.76i", "direction": DR},
            {"t": 138.116042054533, "label": "\\rho_{47} = \\frac{1}{2} + 138.12i", "direction": UR},
            {"t": -138.116042054533, "label": "\\bar{\\rho}_{47} = \\frac{1}{2} - 138.12i", "direction": DR},
            {"t": 139.736208952121, "label": "\\rho_{48} = \\frac{1}{2} + 139.74i", "direction": UR},
            {"t": -139.736208952121, "label": "\\bar{\\rho}_{48} = \\frac{1}{2} - 139.74i", "direction": DR},
            {"t": 141.123707404021, "label": "\\rho_{49} = \\frac{1}{2} + 141.12i", "direction": UR},
            {"t": -141.123707404021, "label": "\\bar{\\rho}_{49} = \\frac{1}{2} - 141.12i", "direction": DR},
            {"t": 143.111845807621, "label": "\\rho_{50} = \\frac{1}{2} + 143.11i", "direction": UR},
            {"t": -143.111845807621, "label": "\\bar{\\rho}_{50} = \\frac{1}{2} - 143.11i", "direction": DR},
        ]

        zero_dots = VGroup()
        zero_labels = VGroup()

        def get_zero_label_opacity(z):
            x, y = z.real, z.imag
            if not (x_range_min <= x <= x_range_max and y_range_min <= y <= y_range_max):
                return 0.0
            d_val = np.sqrt(x**2 + y**2)
            if d_val >= 4.0:
                return 1.0
            elif d_val <= 2.0:
                return 0.0
            else:
                return (d_val - 2.0) / 2.0

        for data in zero_data:
            t_val = data["t"]
            lbl_tex = data["label"]
            dir_vec = data["direction"]
            f_size = 16

            dot = Dot(radius=0.045, fill_color=RED, fill_opacity=1.0,
                      stroke_color=WHITE, stroke_width=1.2)
            dot.move_to(plane.coords_to_point(0.5, t_val))
            show_label = any(abs(abs(t_val) - t) < 1e-8 for t in (14.134725141735, 25.010857580146))
            label = MathTex(lbl_tex if show_label else "", font_size=f_size, color=RED)
            label.show_zero_label = show_label
            label.next_to(dot, dir_vec, buff=zero_label_buff)
            label.shift(label_nudge_vec(t_val))
            if not (y_range_min <= t_val <= y_range_max):
                label.set_opacity(0.0)

            zero_dots.add(dot)
            zero_labels.add(label)

        # ------------------ 50 个平凡零点 s = -2, -4, ..., -100 ------------------
        trivial_zero_dots = VGroup()
        trivial_zero_labels = VGroup()
        trivial_zero_has_label = []

        trivial_zero_ts = [-2 * m for m in range(1, 51)]

        def get_trivial_label_opacity(z):
            x, y = z.real, z.imag
            if not (x_range_min <= x <= x_range_max and y_range_min <= y <= y_range_max):
                return 0.0
            d_val = abs(x)
            if d_val >= 4.0:
                return 1.0
            elif d_val <= 2.0:
                return 0.0
            else:
                return (d_val - 2.0) / 2.0

        for idx, s_val in enumerate(trivial_zero_ts, start=1):
            dot = Dot(radius=0.025, color=BLUE, fill_opacity=1.0)
            dot.move_to(plane.coords_to_point(s_val, 0.0))

            if idx in (1, 3, 5):
                label = MathTex(rf"s = {s_val}", font_size=16, color=BLUE)
                label.next_to(dot, DOWN, buff=0.08)
                trivial_zero_has_label.append(True)
            else:
                label = MathTex("", font_size=11, color=BLUE)
                label.set_opacity(0.0)
                trivial_zero_has_label.append(False)

            trivial_zero_dots.add(dot)
            trivial_zero_labels.add(label)

        # ------------------ 临界线 / 边界 / 临界带 ------------------
        def _zeta_only(x, y):
            return zeta_mapped(x, y, 1.0)

        def _lerp_c(s: complex, z1: complex, a: float) -> complex:
            return (1.0 - a) * s + a * z1

        # 临界线 Re s = 1/2
        zero_heights = np.array([data["t"] for data in zero_data])
        t_arr = np.unique(np.concatenate((np.linspace(-150, 150, 601 if PREVIEW else 3001), zero_heights)))
        crit_src = np.array([complex(0.5, t) for t in t_arr], dtype=complex)
        crit_dst = np.array([_zeta_only(0.5, t) for t in t_arr], dtype=complex)
        crit_src_sc = _c2s(crit_src)
        crit_dst_sc = _c2s(crit_dst)
        critical_line = VMobject(stroke_width=1.5, stroke_opacity=0.95, color=RED)
        critical_line.set_points_smoothly([crit_src_sc[i] for i in range(len(crit_src_sc))])
        critical_line.set_z_index(20)

        def upd_critical(m):
            a = alpha_tracker.get_value()
            mid = (1 - a) * crit_src_sc + a * crit_dst_sc
            m.set_points_smoothly([mid[i] for i in range(len(mid))])
            m.set_stroke(color=RED, opacity=0.95)

        # 临界带边界 Re s = 0 与 Re s = 1
        left_src = np.array([complex(0.0, t) for t in t_arr], dtype=complex)
        left_dst = np.array([_zeta_only(0.0, t) for t in t_arr], dtype=complex)
        left_src_sc = _c2s(left_src)
        left_dst_sc = _c2s(left_dst)
        left_bound = VMobject(stroke_width=1.5, stroke_opacity=0.8, color=GREEN)
        left_bound.set_points_smoothly([left_src_sc[i] for i in range(len(left_src_sc))])
        left_bound.set_z_index(15)

        t_right = np.linspace(0.02, 50, 500)
        right_top_src = np.array([complex(1.0, t) for t in t_right], dtype=complex)
        right_top_dst = np.array([_zeta_only(1.0, t) for t in t_right], dtype=complex)
        right_bot_src = np.array([complex(1.0, -t) for t in t_right], dtype=complex)
        right_bot_dst = np.array([_zeta_only(1.0, -t) for t in t_right], dtype=complex)
        right_top_src_sc = _c2s(right_top_src)
        right_top_dst_sc = _c2s(right_top_dst)
        right_bot_src_sc = _c2s(right_bot_src)
        right_bot_dst_sc = _c2s(right_bot_dst)

        right_bound = VGroup()
        right_bound_top = VMobject(stroke_width=1.5, stroke_opacity=0.8, color=GREEN)
        right_bound_top.set_points_smoothly(
            [right_top_src_sc[i] for i in range(len(right_top_src_sc))]
        )
        right_bound_bottom = VMobject(stroke_width=1.5, stroke_opacity=0.8, color=GREEN)
        right_bound_bottom.set_points_smoothly(
            [right_bot_src_sc[i] for i in range(len(right_bot_src_sc))]
        )
        right_bound.add(right_bound_top, right_bound_bottom)
        right_bound.set_z_index(15)

        def upd_left(m):
            a = alpha_tracker.get_value()
            mid = (1 - a) * left_src_sc + a * left_dst_sc
            m.set_points_smoothly([mid[i] for i in range(len(mid))])
            op = 0.8 * (1.0 - (a - 0.7) / 0.3) if a > 0.7 else 0.8
            m.set_stroke(opacity=max(0.0, op))

        def upd_right(m):
            a = alpha_tracker.get_value()
            t_min = 0.01 + 0.99 * a
            mask = t_right >= t_min
            if not np.any(mask):
                mask = np.ones_like(t_right, dtype=bool)
                mask[0] = False
            mid_top = (1 - a) * right_top_src_sc[mask] + a * right_top_dst_sc[mask]
            mid_bot = (1 - a) * right_bot_src_sc[mask] + a * right_bot_dst_sc[mask]
            m[0].set_points_smoothly([mid_top[i] for i in range(len(mid_top))])
            m[1].set_points_smoothly([mid_bot[i] for i in range(len(mid_bot))])
            op = 0.8 * (1.0 - (a - 0.7) / 0.3) if a > 0.7 else 0.8
            op = max(0.0, op)
            m[0].set_stroke(opacity=op)
            m[1].set_stroke(opacity=op)

        # 临界带填充
        strip_color = GREEN
        strip_opacity = 0.25
        t_strip = np.linspace(0.02, 150, 350)
        slt_src = _c2s(np.array([complex(0.0, t) for t in t_strip], dtype=complex))
        slt_dst = _c2s(np.array([_zeta_only(0.0, t) for t in t_strip], dtype=complex))
        srt_src = _c2s(np.array([complex(1.0, t) for t in t_strip], dtype=complex))
        srt_dst = _c2s(np.array([_zeta_only(1.0, t) for t in t_strip], dtype=complex))
        slb_src = _c2s(np.array([complex(0.0, -t) for t in t_strip], dtype=complex))
        slb_dst = _c2s(np.array([_zeta_only(0.0, -t) for t in t_strip], dtype=complex))
        srb_src = _c2s(np.array([complex(1.0, -t) for t in t_strip], dtype=complex))
        srb_dst = _c2s(np.array([_zeta_only(1.0, -t) for t in t_strip], dtype=complex))

        strip_top = VMobject()
        strip_top.set_fill(strip_color, opacity=strip_opacity)
        strip_top.set_stroke(width=0)
        strip_bottom = VMobject()
        strip_bottom.set_fill(strip_color, opacity=strip_opacity)
        strip_bottom.set_stroke(width=0)
        strip_top.set_z_index(5)
        strip_bottom.set_z_index(5)

        def _strip_opacity(a):
            if a < 0.15:
                return strip_opacity * (1.0 - 0.3 * (a / 0.15))
            if a > 0.7:
                return (strip_opacity * 0.7) * (1.0 - (a - 0.7) / 0.3)
            return strip_opacity * 0.7

        def upd_strip_top(m):
            a = alpha_tracker.get_value()
            m.set_fill(strip_color, opacity=max(0.0, _strip_opacity(a)))
            t_min = 0.01 + 0.99 * a
            mask = t_strip >= t_min
            if not np.any(mask):
                mask = np.ones_like(t_strip, dtype=bool)
            left = (1 - a) * slt_src[mask] + a * slt_dst[mask]
            right = (1 - a) * srt_src[mask] + a * srt_dst[mask]
            poly = np.concatenate([left, right[::-1]])
            m.set_points_as_corners(list(poly) + [poly[0]])

        def upd_strip_bottom(m):
            a = alpha_tracker.get_value()
            m.set_fill(strip_color, opacity=max(0.0, _strip_opacity(a)))
            t_min = 0.01 + 0.99 * a
            mask = t_strip >= t_min
            if not np.any(mask):
                mask = np.ones_like(t_strip, dtype=bool)
            left = (1 - a) * slb_src[mask] + a * slb_dst[mask]
            right = (1 - a) * srb_src[mask] + a * srb_dst[mask]
            poly = np.concatenate([left, right[::-1]])
            m.set_points_as_corners(list(poly) + [poly[0]])

        upd_strip_top(strip_top)
        upd_strip_bottom(strip_bottom)
        critical_strip = VGroup(strip_top, strip_bottom)

        # 非平凡零点：预计算 ζ(ρ) ≈ 0
        zero_src = []
        zero_dst = []
        for data in zero_data:
            t_val = data["t"]
            s0 = complex(0.5, t_val)
            zero_src.append(s0)
            zero_dst.append(_zeta_only(0.5, t_val))

        # 固定参考线 Re s = 1/2
        fixed_half_line = DashedLine(
            plane.coords_to_point(0.5, 16.0),
            plane.coords_to_point(0.5, -16.0),
            color=THEME["muted"],
            stroke_width=1.0,
            stroke_opacity=0.5,
        )

        # 图层
        for g in (v_lines_pink, h_lines_pink, v_lines_blue, h_lines_blue):
            g.set_z_index(2)
        critical_strip.set_z_index(5)
        left_bound.set_z_index(15)
        right_bound.set_z_index(15)
        fixed_half_line.set_z_index(19)
        critical_line.set_z_index(20)
        zero_dots.set_z_index(106)
        zero_labels.set_z_index(107)
        trivial_zero_dots.set_z_index(32)
        trivial_zero_labels.set_z_index(33)

        self.add(
            critical_strip,
            v_lines_pink,
            h_lines_pink,
            v_lines_blue,
            h_lines_blue,
            fixed_half_line,
            critical_line,
            left_bound,
            right_bound,
            zero_dots,
            zero_labels,
            trivial_zero_dots,
            trivial_zero_labels,
            formula,
        )

        strip_top.add_updater(upd_strip_top)
        strip_bottom.add_updater(upd_strip_bottom)
        v_lines_pink.add_updater(update_v_pink)
        h_lines_pink.add_updater(update_h_pink)
        v_lines_blue.add_updater(update_v_blue)
        h_lines_blue.add_updater(update_h_blue)
        critical_line.add_updater(upd_critical)
        left_bound.add_updater(upd_left)
        right_bound.add_updater(upd_right)

        # 非平凡零点 updater
        for i, (dot, label, data) in enumerate(zip(zero_dots, zero_labels, zero_data)):
            dir_vec = data["direction"]
            t_val = data["t"]
            s0, s1 = zero_src[i], zero_dst[i]

            def make_updaters(d, l, s0_c, s1_c, t_val_c, dir_c):
                def upd_d(mob):
                    a = alpha_tracker.get_value()
                    z = _lerp_c(s0_c, s1_c, a)
                    mob.move_to(plane.coords_to_point(z.real, z.imag))
                def upd_l(mob):
                    a = alpha_tracker.get_value()
                    z = _lerp_c(s0_c, s1_c, a)
                    mob.next_to(d, dir_c, buff=zero_label_buff)
                    mob.shift(label_nudge_vec(t_val_c))
                    mob.set_opacity(get_zero_label_opacity(z) if mob.show_zero_label else 0.0)
                return upd_d, upd_l

            upd_dot, upd_lbl = make_updaters(dot, label, s0, s1, t_val, dir_vec)
            dot.add_updater(upd_dot)
            label.add_updater(upd_lbl)

        # 平凡零点 updater
        for idx, (dot, label, s_val, has_label) in enumerate(
            zip(trivial_zero_dots, trivial_zero_labels, trivial_zero_ts, trivial_zero_has_label)
        ):
            s0 = complex(s_val, 0.0)
            s1 = _zeta_only(s_val, 0.0)

            def make_trivial_updaters(d, l, s0_c, s1_c, s_val_c, has_lbl):
                def upd_d(mob):
                    a = alpha_tracker.get_value()
                    z = _lerp_c(s0_c, s1_c, a)
                    mob.move_to(plane.coords_to_point(z.real, z.imag))
                def upd_l(mob):
                    a = alpha_tracker.get_value()
                    z = _lerp_c(s0_c, s1_c, a)
                    if not has_lbl:
                        mob.set_opacity(0.0)
                        return
                    mob.next_to(d, DOWN, buff=0.08)
                    mob.set_opacity(get_trivial_label_opacity(z))
                return upd_d, upd_l

            upd_dot, upd_lbl = make_trivial_updaters(dot, label, s0, s1, s_val, has_label)
            dot.add_updater(upd_dot)
            label.add_updater(upd_lbl)

        if getattr(self, "STILL", False) or BOOK_MODE:
            alpha = float(os.environ.get("ALPHA_STILL", "0.56"))
            if not 0 <= alpha <= 1:
                raise ValueError("ALPHA_STILL must be between 0 and 1")
            alpha_tracker.set_value(alpha)
            self.update_mobjects(0)
        else:
            self.play(alpha_tracker.animate.set_value(1), rate_func=linear, run_time=22)
            self.wait(2)


class ZetaStill(ZetaConformalMap):
    """A reproducible still; ALPHA_STILL defaults to 0.56."""
    STILL = True
