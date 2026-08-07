# zeta_conformal_manim.py
from manim import *
import numpy as np
from mpmath import mp, zeta

mp.dps = 18

class ZetaConformalMap(Scene):
    def construct(self):
        # ------------------ 参数区 ------------------
        # 坐标轴范围调整
        x_range_min, x_range_max = -16, 16
        y_range_min, y_range_max = -9, 9
        
        points_per_line = 150

        # ------------------ 水平网格线和垂直网格线的数量设置 ------------------
        num_h_lines = 300
        num_v_lines = 300

        re_values_right = np.arange(0, num_v_lines) * 0.01
        im_values = np.arange(-num_h_lines // 2, num_h_lines // 2) * 0.01

        # 原 s 平面显示范围，根据网格线范围自动计算
        re_min = -0.1
        re_max = re_values_right[-1]
        im_limit = max(abs(im_values[0]), abs(im_values[-1]))

        # ------------------ 坐标系（使用 Axes 统一管理）------------------
        # 创建完整的坐标轴（不含背景直角网格线）
        plane = Axes(
            x_range=[x_range_min, x_range_max, 2],
            y_range=[y_range_min, y_range_max, 2],
            axis_config={
                "include_tip": False,           # 取消箭头尖端
                "color": GRAY_D,
                "stroke_width": 1.5,
            }
        )
        
        # 手动添加x轴刻度
        x_ticks = VGroup()
        for x in range(-16, 17, 2):
            if x == 0:
                continue
            point = plane.coords_to_point(x, 0)
            # 刻度线（短竖线）
            tick = Line(
                point + DOWN * 0.15,
                point + UP * 0.15,
                color=GRAY_D,
                stroke_width=1.5
            )
            # 刻度标签
            label = MathTex(str(x), font_size=22, color=GRAY)
            label.next_to(point, DOWN, buff=0.2)
            x_ticks.add(tick, label)
        
        # 手动添加y轴刻度
        y_ticks = VGroup()
        for y in range(-8, 9, 2):
            if y == 0:
                continue
            point = plane.coords_to_point(0, y)
            # 刻度线（短横线）
            tick = Line(
                point + LEFT * 0.15,
                point + RIGHT * 0.15,
                color=GRAY_D,
                stroke_width=1.5
            )
            # 刻度标签（虚数单位 i）
            if y == 1:
                label = MathTex(r"i", font_size=24, color=BLUE_B)
            elif y == -1:
                label = MathTex(r"-i", font_size=24, color=BLUE_B)
            else:
                label = MathTex(f"{y}i", font_size=22, color=BLUE_B)
            label.next_to(point, LEFT, buff=0.2)
            y_ticks.add(tick, label)
        
        # 添加原点标签
        origin_point = plane.coords_to_point(0, 0)
        origin_label = MathTex("0", font_size=22, color=GRAY)
        origin_label.next_to(origin_point, DOWN+RIGHT, buff=0.1)
        
        # 添加所有元素到场景
        self.add(plane, x_ticks, y_ticks, origin_label)

        # ------------------ 公式与文字 ------------------
        # 上方：zeta 函数定义（Dirichlet 级数 + Euler 乘积）
        formula_def = MathTex(
            r"\zeta(s) = \sum_{n=1}^{\infty} \frac{1}{n^s} = \prod_{p\,\text{prime}} \frac{1}{1-p^{-s}}",
            font_size=26,
        ).to_edge(UL, buff=0.5).shift(0.2*DOWN)

        # 下方：函数方程（揭示临界线对称性根源）
        formula_feq = MathTex(
            r"\zeta(s) = 2^s \pi^{s-1} \sin\!\left(\frac{\pi s}{2}\right) \Gamma(1-s)\,\zeta(1-s)",
            font_size=26,
        ).next_to(formula_def, DOWN, aligned_edge=LEFT, buff=0.25)

        formula = VGroup(formula_def, formula_feq)

        alpha_tracker = ValueTracker(0)

        progress = always_redraw(lambda: 
            Text(f"变换进度：{int(alpha_tracker.get_value()*100)}%", 
                 font_size=22, color=GRAY_A)
            .next_to(formula_feq, DOWN, aligned_edge=LEFT, buff=0.35)
        )

        self.add(formula, progress)

        # ------------------ zeta 映射函数 ------------------
        def zeta_mapped(x, y, alpha):
            s = complex(x, y)
            if abs(s - 1.0) < 1e-6:
                z = complex(30.0, 0.0)
            else:
                try:
                    z = complex(zeta(s))
                except Exception as e:
                    import traceback
                    with open("/Users/lichengtong/完成的初稿/成书章节/全书修改/视频/error_log.txt", "a") as f:
                        f.write(f"Error for s={s}: {e}\n{traceback.format_exc()}\n")
                    z = s
            limit = 30.0
            if abs(z) > limit:
                z = z / abs(z) * limit
            mapped = (1 - alpha) * s + alpha * z
            return mapped

        # ------------------ 预计算右半平面网格线，避免在 updater 中重复计算 zeta ------------------
        v_lines_math = []
        v_lines_zeta = []
        for re_val in re_values_right:
            if abs(re_val - 1.0) < 1e-6:
                continue
            pts = np.array([complex(re_val, t) for t in np.linspace(im_values[0], im_values[-1], points_per_line)])
            z = np.array([zeta_mapped(re_val, t, 1.0) for t in np.linspace(im_values[0], im_values[-1], points_per_line)])
            v_lines_math.append(pts)
            v_lines_zeta.append(z)

        h_lines_math = []
        h_lines_zeta = []
        for im_val in im_values:
            pts = np.array([complex(r, im_val) for r in np.linspace(re_values_right[0], re_values_right[-1], points_per_line)])
            z = np.array([zeta_mapped(r, im_val, 1.0) for r in np.linspace(re_values_right[0], re_values_right[-1], points_per_line)])
            h_lines_math.append(pts)
            h_lines_zeta.append(z)

        # ------------------ 创建网格 Mobjects ------------------
        v_lines_right = VGroup()
        for pts in v_lines_math:
            line = VMobject(stroke_color=YELLOW, stroke_width=1.0, stroke_opacity=0.4)
            line.set_points_smoothly([plane.coords_to_point(val.real, val.imag) for val in pts])
            v_lines_right.add(line)

        h_lines_right = VGroup()
        for idx, im_val in enumerate(im_values):
            pts = h_lines_math[idx]
            line = VMobject(stroke_color=YELLOW, stroke_width=1.0, stroke_opacity=0.4)
            line.set_points_smoothly([plane.coords_to_point(val.real, val.imag) for val in pts])
            h_lines_right.add(line)

        def update_v_lines_right(mob: VGroup):
            a = alpha_tracker.get_value()
            for line, pts, z in zip(mob, v_lines_math, v_lines_zeta):
                mapped = (1 - a) * pts + a * z
                line.set_points_smoothly([plane.coords_to_point(val.real, val.imag) for val in mapped])

        def update_h_lines_right(mob: VGroup):
            a = alpha_tracker.get_value()
            for line, pts, z in zip(mob, h_lines_math, h_lines_zeta):
                mapped = (1 - a) * pts + a * z
                line.set_points_smoothly([plane.coords_to_point(val.real, val.imag) for val in mapped])

        # ------------------ 前十个非平凡零点及其共轭（临界线上）------------------
        zero_data = [
            {"t": 14.134725,  "label": r"\rho_1 = \frac{1}{2} + 14.13i", "direction": UR},
            {"t": -14.134725, "label": r"\bar{\rho}_1 = \frac{1}{2} - 14.13i", "direction": DR},
            {"t": 21.022040,  "label": r"\rho_2 = \frac{1}{2} + 21.02i", "direction": UR},
            {"t": -21.022040, "label": r"\bar{\rho}_2 = \frac{1}{2} - 21.02i", "direction": DR},
            {"t": 25.010858,  "label": r"\rho_3 = \frac{1}{2} + 25.01i", "direction": UR},
            {"t": -25.010858, "label": r"\bar{\rho}_3 = \frac{1}{2} - 25.01i", "direction": DR},
            {"t": 30.424876,  "label": r"\rho_4 = \frac{1}{2} + 30.42i", "direction": UR},
            {"t": -30.424876, "label": r"\bar{\rho}_4 = \frac{1}{2} - 30.42i", "direction": DR},
            {"t": 32.935062,  "label": r"\rho_5 = \frac{1}{2} + 32.94i", "direction": UR},
            {"t": -32.935062, "label": r"\bar{\rho}_5 = \frac{1}{2} - 32.94i", "direction": DR},
            {"t": 37.586178,  "label": r"\rho_6 = \frac{1}{2} + 37.59i", "direction": UR},
            {"t": -37.586178, "label": r"\bar{\rho}_6 = \frac{1}{2} - 37.59i", "direction": DR},
            {"t": 40.918719,  "label": r"\rho_7 = \frac{1}{2} + 40.92i", "direction": UR},
            {"t": -40.918719, "label": r"\bar{\rho}_7 = \frac{1}{2} - 40.92i", "direction": DR},
            {"t": 43.327073,  "label": r"\rho_8 = \frac{1}{2} + 43.33i", "direction": UR},
            {"t": -43.327073, "label": r"\bar{\rho}_8 = \frac{1}{2} - 43.33i", "direction": DR},
            {"t": 48.005151,  "label": r"\rho_9 = \frac{1}{2} + 48.01i", "direction": UR},
            {"t": -48.005151, "label": r"\bar{\rho}_9 = \frac{1}{2} - 48.01i", "direction": DR},
            {"t": 49.773832,  "label": r"\rho_{10} = \frac{1}{2} + 49.77i", "direction": UR},
            {"t": -49.773832, "label": r"\bar{\rho}_{10} = \frac{1}{2} - 49.77i", "direction": DR},
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
            f_size = data.get("font_size", 12)

            dot = Dot(radius=0.025, color=RED, fill_opacity=1.0)
            dot.move_to(plane.coords_to_point(0.5, t_val))
            label = MathTex(lbl_tex, font_size=f_size, color=RED)
            label.next_to(dot, dir_vec, buff=0.15)
            # 初始状态下若小球不在可视范围内，将标签透明度设为 0
            if not (y_range_min <= t_val <= y_range_max):
                label.set_opacity(0.0)

            zero_dots.add(dot)
            zero_labels.add(label)

        # ------------------ 临界线（红色）------------------
        # 临界线覆盖前十个非平凡零点及其共轭，扩展到 -52 到 52
        t_arr = np.linspace(-52, 52, 1600)
        critical_line = VMobject(stroke_width=0.5, stroke_opacity=0.95, color=RED)
        critical_line.set_points_smoothly([plane.coords_to_point(0.5, t) for t in t_arr])

        def upd_critical(m):
            a = alpha_tracker.get_value()
            points = []
            for t in t_arr:
                z = zeta_mapped(0.5, t, a)
                points.append(plane.coords_to_point(z.real, z.imag))
            m.set_points_smoothly(points)
            # 末尾阶段（a从0.7到1.0）：临界线逐渐淡出消失
            if a > 0.7:
                fade = 1.0 - (a - 0.7) / 0.3
                m.set_stroke(color=RED, opacity=0.95 * fade)
            else:
                m.set_stroke(color=RED, opacity=0.95)

        # ------------------ 临界带边界线（Re(s)=0, Re(s)=1，黄色，同步变换）------------------
        left_bound = VMobject(stroke_width=1.0, stroke_opacity=0.8, color=GREEN)
        left_bound.set_points_smoothly([plane.coords_to_point(0.0, t) for t in t_arr])
        
        # 针对 Re(s)=1 处的极点，使用动态截断：静态时线段完整，计算（变换）时截断范围逐渐扩大至 1.0
        right_bound = VGroup()
        right_bound_top = VMobject(stroke_width=1.0, stroke_opacity=0.8, color=GREEN)
        right_bound_top.set_points_smoothly([plane.coords_to_point(1.0, t) for t in np.linspace(0.01, 27, 600)])
        right_bound_bottom = VMobject(stroke_width=1.0, stroke_opacity=0.8, color=GREEN)
        right_bound_bottom.set_points_smoothly([plane.coords_to_point(1.0, t) for t in np.linspace(-27, -0.01, 600)])
        right_bound.add(right_bound_top, right_bound_bottom)
 
        def upd_left(m):
            a = alpha_tracker.get_value()
            points = []
            for t in t_arr:
                z = zeta_mapped(0.0, t, a)
                points.append(plane.coords_to_point(z.real, z.imag))
            m.set_points_smoothly(points)
            # 末尾阶段（a从0.7到1.0）：左边界线逐渐淡出消失
            if a > 0.7:
                fade = 1.0 - (a - 0.7) / 0.3
                m.set_stroke(opacity=0.8 * fade)
            else:
                m.set_stroke(opacity=0.8)
 
        def upd_right(m):
            a = alpha_tracker.get_value()
            t_min = 0.01 + 0.99 * a  # 动态截断：a=0时为0.01，a=1时为1.0
            points_top = []
            for t in np.linspace(t_min, 27, 600):
                z = zeta_mapped(1.0, t, a)
                points_top.append(plane.coords_to_point(z.real, z.imag))
            m[0].set_points_smoothly(points_top)
            
            points_bottom = []
            for t in np.linspace(-27, -t_min, 600):
                z = zeta_mapped(1.0, t, a)
                points_bottom.append(plane.coords_to_point(z.real, z.imag))
            m[1].set_points_smoothly(points_bottom)
            # 末尾阶段（a从0.7到1.0）：右边界线逐渐淡出消失
            if a > 0.7:
                fade = 1.0 - (a - 0.7) / 0.3
                m[0].set_stroke(opacity=0.8 * fade)
                m[1].set_stroke(opacity=0.8 * fade)
            else:
                m[0].set_stroke(opacity=0.8)
                m[1].set_stroke(opacity=0.8)

        # ------------------ 临界带填充区域（半透明黄色，调试状态下透明度调高）------------------
        strip_color = GREEN
        strip_opacity = 0.5
        
        strip_top = VMobject()
        strip_top.set_fill(strip_color, opacity=strip_opacity)
        strip_top.set_stroke(width=0)
        
        strip_bottom = VMobject()
        strip_bottom.set_fill(strip_color, opacity=strip_opacity)
        strip_bottom.set_stroke(width=0)
        
        def upd_strip_top(m):
            a = alpha_tracker.get_value()
            # 三阶段动态透明度控制（通过 strip_opacity 缩放）：
            # 1. 初始阶段（a从0到0.15）：初始临界带填充稍稍淡出，透明度由 strip_opacity 降至 strip_opacity * 0.7
            # 2. 中间阶段（a从0.15到0.7）：保持较高透明度，展示曲线组成临界带的动态变换填充
            # 3. 最后阶段（a从0.7到1.0）：由于0点附近集中了大量集合元素，填充逐步淡出至 0.0 消失
            if a < 0.15:
                current_opacity = strip_opacity * (1.0 - 0.3 * (a / 0.15))
            elif a > 0.7:
                current_opacity = (strip_opacity * 0.7) * (1.0 - (a - 0.7) / 0.3)
            else:
                current_opacity = strip_opacity * 0.7
            m.set_fill(strip_color, opacity=current_opacity)
            
            t_min = 0.01 + 0.99 * a
            points = []
            for t in np.linspace(t_min, 52, 300):
                z = zeta_mapped(0.0, t, a)
                points.append(plane.coords_to_point(z.real, z.imag))
            for t in np.linspace(52, t_min, 300):
                z = zeta_mapped(1.0, t, a)
                points.append(plane.coords_to_point(z.real, z.imag))
            m.set_points_as_corners(points)
            
        def upd_strip_bottom(m):
            a = alpha_tracker.get_value()
            # 三阶段动态透明度控制（通过 strip_opacity 缩放）：
            # 1. 初始阶段（a从0到0.15）：初始临界带填充稍稍淡出，透明度由 strip_opacity 降至 strip_opacity * 0.7
            # 2. 中间阶段（a从0.15到0.7）：保持较高透明度，展示曲线组成临界带的动态变换填充
            # 3. 最后阶段（a从0.7到1.0）：由于0点附近集中了大量集合元素，填充逐步淡出至 0.0 消失
            if a < 0.15:
                current_opacity = strip_opacity * (1.0 - 0.3 * (a / 0.15))
            elif a > 0.7:
                current_opacity = (strip_opacity * 0.7) * (1.0 - (a - 0.7) / 0.3)
            else:
                current_opacity = strip_opacity * 0.7
            m.set_fill(strip_color, opacity=current_opacity)
            
            t_min = 0.01 + 0.99 * a
            points = []
            for t in np.linspace(-t_min, -52, 300):
                z = zeta_mapped(0.0, t, a)
                points.append(plane.coords_to_point(z.real, z.imag))
            for t in np.linspace(-52, -t_min, 300):
                z = zeta_mapped(1.0, t, a)
                points.append(plane.coords_to_point(z.real, z.imag))
            m.set_points_as_corners(points)
            
        # 初始填充状态
        upd_strip_top(strip_top)
        upd_strip_bottom(strip_bottom)
        
        critical_strip = VGroup(strip_top, strip_bottom)

        # Directly add all objects to the scene (no FadeIn/Create) to prevent ghosting copies
        self.add(
            critical_strip,
            v_lines_right,
            h_lines_right,
            critical_line,
            left_bound,
            right_bound,
            zero_dots,
            zero_labels,
            formula,
        )

        # ------------------ 动画播放完后添加 updaters ------------------
        strip_top.add_updater(upd_strip_top)
        strip_bottom.add_updater(upd_strip_bottom)
        v_lines_right.add_updater(update_v_lines_right)
        h_lines_right.add_updater(update_h_lines_right)
        critical_line.add_updater(upd_critical)
        left_bound.add_updater(upd_left)
        right_bound.add_updater(upd_right)

        # 为零点和小球绑定 updaters
        for dot, label, data in zip(zero_dots, zero_labels, zero_data):
            t_val = data["t"]
            dir_vec = data["direction"]
            def make_updaters(d, l, t_val_c, dir_c):
                def upd_d(mob):
                    a = alpha_tracker.get_value()
                    z = zeta_mapped(0.5, t_val_c, a)
                    mob.move_to(plane.coords_to_point(z.real, z.imag))
                def upd_l(mob):
                    a = alpha_tracker.get_value()
                    z = zeta_mapped(0.5, t_val_c, a)
                    mob.next_to(d, dir_c, buff=0.15)
                    mob.set_opacity(get_zero_label_opacity(z))
                return upd_d, upd_l
            upd_dot, upd_lbl = make_updaters(dot, label, t_val, dir_vec)
            dot.add_updater(upd_dot)
            label.add_updater(upd_lbl)

        self.play(
            alpha_tracker.animate.set_value(1),
            rate_func=linear,
            run_time=22
        )

        self.wait(2)