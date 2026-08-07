# -*- coding: utf-8 -*-
"""
临界线螺旋：s = 1/2 + it  →  w = ζ(s)
画面主公式：Hardy 极坐标形式
  ζ(1/2+it) = Z(t) e^{-iϑ(t)},  Z(t) ∈ ℝ
  半径 |Z(t)|，相位 -ϑ(t)，过原点 ⇔ Z(t)=0

性能要点（修复"开始正常、很快跳到结束"）：
  - 公式/计数器禁止 always_redraw(MathTex)（每帧重跑 LaTeX 会卡死）
  - ζ 值预先算好；动画只截取缓存点，不再每帧 ParametricFunction+zeta
"""
from manim import *
import numpy as np
from mpmath import mp, zeta, zetazero

mp.dps = 15  # 动画精度足够；过高会拖慢预计算

T_MAX = 80.0
DT = 0.08  # 采样步长；更小更密、预计算更久
N_SAMPLES = int(T_MAX / DT) + 1
T_GRID = np.linspace(0.0, T_MAX, N_SAMPLES)

RAW_ZEROS = [float(zetazero(n).imag) for n in range(1, 40)]
ZERO_LIST = sorted(tz for tz in RAW_ZEROS if tz <= T_MAX)


def precompute_zeta_on_critical_line(t_grid, dps=15):
    """预计算 ζ(1/2+it)，返回 shape (N,) 的 complex128 数组。"""
    mp.dps = dps
    vals = np.empty(len(t_grid), dtype=np.complex128)
    for i, t in enumerate(t_grid):
        if i % 100 == 0:
            print(f"  precompute zeta: {i}/{len(t_grid)}  t={t:.2f}")
        vals[i] = complex(zeta(complex(0.5, float(t))))
    return vals


class zeta_3D_18H(ThreeDScene):
    def construct(self):
        AMPLIFY_FACTOR = 2.25
        RUN_TIME = 35.0

        print("Precomputing ζ(1/2+it) on grid ...")
        zeta_vals = precompute_zeta_on_critical_line(T_GRID, dps=15)
        re_arr = np.real(zeta_vals) * AMPLIFY_FACTOR
        im_arr = np.imag(zeta_vals) * AMPLIFY_FACTOR
        print("Precompute done.")

        axes = ThreeDAxes(
            x_range=[0, T_MAX + 10, 10],
            y_range=[-30, 30, 10],
            z_range=[-30, 30, 10],
            x_length=20,
            y_length=10,
            z_length=10,
            axis_config={"color": GREY, "stroke_width": 1},
        ).scale(0.6).shift(LEFT * 0.8)
        axes.shift(OUT * (-1))

        # 轴约定（恢复观感更好的布置）：
        #   X = t（螺旋推进）
        #   Y = Im ζ（水平）
        #   Z = Re ζ（竖直向上）
        t_label = MathTex(r"t").scale(0.7).set_color(YELLOW)
        t_label.next_to(axes.c2p(T_MAX + 4, 4, 1))
        t_label.rotate(90 * DEGREES, axis=RIGHT)

        im_label = MathTex(r"\operatorname{Im}\zeta").scale(0.55).set_color(YELLOW)
        im_label.next_to(axes.c2p(-3, 28, 0), LEFT)
        im_label.rotate(90 * DEGREES, axis=RIGHT)

        re_label = MathTex(r"\operatorname{Re}\zeta").scale(0.55).set_color(YELLOW)
        re_label.next_to(axes.c2p(0, 0, 30.5))
        re_label.rotate(90 * DEGREES, axis=RIGHT)

        # 侧面示意平面 y=SIDE_Y：用 Z 方向画 Re/Im 对 t 的波形（图幅，非主轴几何）
        re_centerline = Line(
            axes.c2p(0, 20, 0),
            axes.c2p(T_MAX, 20, 0),
            color=YELLOW,
            stroke_opacity=0.5,
            stroke_width=1.5,
        )

        # ---------- 预计算三维点 ----------
        # 主螺旋：c2p(t, Im, Re)
        pts_helix = np.array(
            [axes.c2p(float(T_GRID[i]), float(im_arr[i]), float(re_arr[i])) for i in range(N_SAMPLES)]
        )
        # YZ 投影（x=0）：(Im, Re) = (Y, Z)
        pts_yz = np.array(
            [axes.c2p(0.0, float(im_arr[i]), float(re_arr[i])) for i in range(N_SAMPLES)]
        )
        # 侧面曲线：y=20 平面，Z 承载幅值
        pts_re = np.array(
            [axes.c2p(float(T_GRID[i]), 20.0, float(re_arr[i])) for i in range(N_SAMPLES)]
        )
        pts_im = np.array(
            [axes.c2p(float(T_GRID[i]), 20.0, float(im_arr[i])) for i in range(N_SAMPLES)]
        )

        def polyline_from_pts(pts, color, width=2, opacity=1.0):
            mob = VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
            if len(pts) >= 2:
                mob.set_points_as_corners(pts)
            return mob

        # 初始极短线段，避免空点报错
        main_helix = polyline_from_pts(pts_helix[:2], WHITE, 2, 1.0)
        proj_yz = polyline_from_pts(pts_yz[:2], "#00FF00", 2, 0.8)
        proj_re = polyline_from_pts(pts_re[:2], "#8B4513", 2, 0.9)
        proj_im = polyline_from_pts(pts_im[:2], BLUE, 2, 0.9)

        time_tracker = ValueTracker(0.0)

        def n_from_t(t):
            """当前 t 对应到采样下标（至少 2 个点）。"""
            n = int(np.clip(t / DT, 1, N_SAMPLES - 1)) + 1
            return max(2, min(n, N_SAMPLES))

        def update_curves(_=None):
            n = n_from_t(time_tracker.get_value())
            main_helix.set_points_as_corners(pts_helix[:n])
            proj_yz.set_points_as_corners(pts_yz[:n])
            proj_re.set_points_as_corners(pts_re[:n])
            proj_im.set_points_as_corners(pts_im[:n])

        main_helix.add_updater(update_curves)

        # 动点：插值最近采样
        moving_dot = Dot3D(point=pts_helix[0], color=RED, radius=0.03)

        def update_dot(mob):
            t = time_tracker.get_value()
            n = n_from_t(t) - 1
            mob.move_to(pts_helix[n])

        moving_dot.add_updater(update_dot)

        # ---------- Hardy Z 公式（静态，略下移）----------
        formula = MathTex(
            r"\zeta\!\left(\dfrac{1}{2}+it\right)"
            r"=Z(t)\,e^{-i\vartheta(t)},\quad "
            r"Z(t)=e^{i\vartheta(t)}\zeta\!\left(\dfrac{1}{2}+it\right)\in\mathbb{R}",
            color=WHITE,
        ).scale(0.58)
        formula.move_to(axes.c2p(40, -10, -20.0))
        formula.rotate(90 * DEGREES, axis=RIGHT)

        # ---------- 曲线旁标注（同平面、靠近不压线）----------
        # 侧面 Re/Im 曲线与标签均在 y=SIDE_Y。
        # 绿投影：(Y,Z)=(Im,Re)；向 Im 正、Re 负略移，再沿 Re 上移 LABEL_LIFT。
        SIDE_Y = 20.0
        LABEL_PAD = 3.8
        LABEL_LIFT = 2.5

        def _local_peak_index(arr, t_lo, t_hi):
            i0 = int(np.clip(t_lo / DT, 0, N_SAMPLES - 1))
            i1 = int(np.clip(t_hi / DT, 0, N_SAMPLES - 1))
            if i1 <= i0:
                i1 = min(i0 + 1, N_SAMPLES - 1)
            return i0 + int(np.argmax(arr[i0 : i1 + 1]))

        i_re = _local_peak_index(re_arr, 0.22 * T_MAX, 0.42 * T_MAX)
        t_re = float(T_GRID[i_re])
        z_re = float(re_arr[i_re]) + LABEL_PAD + LABEL_LIFT

        i_im = _local_peak_index(im_arr, 0.48 * T_MAX, 0.72 * T_MAX)
        t_im = float(T_GRID[i_im])
        z_im = float(im_arr[i_im]) + LABEL_PAD + LABEL_LIFT

        re_max = float(np.max(re_arr))
        im_max = float(np.max(im_arr))
        yz_shift_re = 2.5  # Re 正方向
        yz_shift_im = 2.5  # Im 正方向
        # c2p(t, Im, Re) → Y=Im 正，Z=Re 正，再 +LIFT
        yz_y = float(np.clip(im_max + yz_shift_im, -28.0, 28.0))
        yz_z = float(np.clip(re_max + yz_shift_re + LABEL_LIFT, -28.0, 28.0))

        yz_proj_label = MathTex(
            r"(0,\ \operatorname{Im}\zeta,\ \operatorname{Re}\zeta)",
            font_size=22,
            color="#00FF00",
        )
        yz_proj_label.move_to(axes.c2p(0.0, yz_y, yz_z))
        yz_proj_label.rotate(90 * DEGREES, axis=RIGHT)
        yz_proj_label.rotate(90 * DEGREES, axis=OUT)

        re_curve_label = MathTex(
            r"\operatorname{Re}\zeta\!\left(\tfrac12+it\right)",
            font_size=24,
            color="#8B4513",
        )
        re_curve_label.move_to(axes.c2p(t_re, SIDE_Y, z_re))
        re_curve_label.rotate(90 * DEGREES, axis=RIGHT)

        im_curve_label = MathTex(
            r"\operatorname{Im}\zeta\!\left(\tfrac12+it\right)",
            font_size=24,
            color=BLUE,
        )
        im_curve_label.move_to(axes.c2p(t_im, SIDE_Y, z_im))
        im_curve_label.rotate(90 * DEGREES, axis=RIGHT)

        print(
            f"  label anchors: Re@t={t_re:.1f} y={SIDE_Y} z={z_re:.1f}; "
            f"Im@t={t_im:.1f} y={SIDE_Y} z={z_im:.1f}; "
            f"YZ@(Im={yz_y:.1f}, Re={yz_z:.1f}) lift={LABEL_LIFT}"
        )

        # ---------- 零点标记：预创建，按 t 淡入（避免动画中途 MathTex） ----------
        recorded_marks = VGroup()
        zero_labels = VGroup()
        zero_mark_groups = []  # (tz, VGroup of marks, label)

        for idx, tz in enumerate(ZERO_LIST, start=1):
            # 最近采样点
            j = int(np.clip(round(tz / DT), 0, N_SAMPLES - 1))
            val_re = float(re_arr[j])
            val_im = float(im_arr[j])

            # 零点：t 轴上的标记；侧面曲线上 Re/Im 的采样点
            t_mark = Dot3D(axes.c2p(tz, 0, 0), color=WHITE, radius=0.02)
            re_mark = Dot3D(axes.c2p(tz, 20, val_re), color="#8B4513", radius=0.02)
            im_mark = Dot3D(axes.c2p(tz, 20, val_im), color=BLUE, radius=0.02)
            marks = VGroup(t_mark, re_mark, im_mark)
            marks.set_opacity(0)

            # 全部用 MathTex，避免 DecimalNumber/Text 在 3D 旋转后 font_size 异常
            idx_label = MathTex(f"N_{{{idx}}}", color=GREEN).scale(0.30)
            coords_label = MathTex(
                rf"\tfrac{{1}}{{2}}+{tz:.4f}\,i",
                color=WHITE,
            ).scale(0.30)
            label = VGroup(idx_label, coords_label).arrange(DOWN, buff=0.1)
            label.move_to(t_mark.get_center() + DOWN * 1.2)
            label.rotate(90 * DEGREES, axis=RIGHT)
            label.rotate(90 * DEGREES, axis=OUT)
            label.set_opacity(0)

            recorded_marks.add(marks)
            zero_labels.add(label)
            zero_mark_groups.append((tz, marks, label))

        def update_zero_visibility(_=None):
            t_now = time_tracker.get_value()
            for tz, marks, label in zero_mark_groups:
                op = 1.0 if t_now >= tz else 0.0
                marks.set_opacity(op)
                label.set_opacity(op)

        recorded_marks.add_updater(update_zero_visibility)

        # ---------- 计数公式 + 动态 (当前 t)=当前零点数 ----------
        # 形式：N(T)∼(T/2π)ln(T/(2π))−T/(2π) (t_now)=count
        # 与 Hardy Z 公式相同：绕 RIGHT 转 90°，使读数方向平行于 t 轴（X）
        # 禁止 always_redraw(MathTex)；Integer/Decimal 在旋转前设好 font_size，勿再 scale
        FS_N = 26
        nt_asymp = MathTex(
            r"N(T)\sim\dfrac{T}{2\pi}\log\dfrac{T}{2\pi}-\dfrac{T}{2\pi}",
            font_size=FS_N,
            color=WHITE,
        )
        nt_lpar = MathTex(r"\bigl(", font_size=FS_N, color=WHITE)
        t_disp = DecimalNumber(
            0,
            num_decimal_places=2,
            font_size=FS_N,
            color=YELLOW,
        )
        nt_eq = MathTex(r"\bigr)=", font_size=FS_N, color=WHITE)
        n_count = Integer(0, font_size=FS_N + 4, color=GREEN)
        nt_group = VGroup(nt_asymp, nt_lpar, t_disp, nt_eq, n_count).arrange(
            RIGHT, buff=0.06, aligned_edge=ORIGIN
        )
        # 介于 Hardy 公式与 t 轴上 N_k / 1/2+it 之间；Z=Reζ 为竖直向上
        nt_group.move_to(axes.c2p(0.42 * T_MAX, -9.0, -10.0))
        nt_group.rotate(90 * DEGREES, axis=RIGHT)

        def _count_zeros_upto(t_now):
            return sum(1 for tz in ZERO_LIST if tz <= t_now + 1e-9)

        # 绕 RIGHT 旋转后 height≈0，set_value 会触发 font_size<=0；
        # 用 become 重建未旋转数字再转回，避免 ValueError
        def update_t_disp(mob):
            center = mob.get_center()
            new = DecimalNumber(
                time_tracker.get_value(),
                num_decimal_places=2,
                font_size=FS_N,
                color=YELLOW,
            )
            new.rotate(90 * DEGREES, axis=RIGHT)
            new.move_to(center)
            mob.become(new)

        def update_n_count(mob):
            center = mob.get_center()
            new = Integer(
                _count_zeros_upto(time_tracker.get_value()),
                font_size=FS_N + 4,
                color=GREEN,
            )
            new.rotate(90 * DEGREES, axis=RIGHT)
            new.move_to(center)
            mob.become(new)

        t_disp.add_updater(update_t_disp)
        n_count.add_updater(update_n_count)

        self.add(
            axes,
            re_centerline,
            main_helix,
            proj_yz,
            proj_im,
            proj_re,
            moving_dot,
            formula,
            nt_group,
            recorded_marks,
            t_label,
            im_label,
            re_label,
            re_curve_label,
            im_curve_label,
            yz_proj_label,
            zero_labels,
        )

        self.set_camera_orientation(phi=70 * DEGREES, theta=-0.8)
        # 部分版本无 set_focal_distance；有则设置
        if hasattr(self.camera, "set_focal_distance"):
            self.camera.set_focal_distance(28)
        elif hasattr(self.camera, "focal_distance"):
            self.camera.focal_distance = 28

        self.begin_ambient_camera_rotation(rate=-0.325 / RUN_TIME)
        self.play(
            time_tracker.animate.set_value(T_MAX),
            run_time=RUN_TIME,
            rate_func=linear,
        )
        self.stop_ambient_camera_rotation()

        # 收尾：去掉 updater，固定终态
        main_helix.clear_updaters()
        moving_dot.clear_updaters()
        recorded_marks.clear_updaters()
        t_disp.clear_updaters()
        n_count.clear_updaters()
        update_curves()
        update_zero_visibility()
        # 终态同样用 become，避免对已旋转数字 set_value
        _c = t_disp.get_center()
        _t_end = DecimalNumber(
            T_MAX, num_decimal_places=2, font_size=FS_N, color=YELLOW
        )
        _t_end.rotate(90 * DEGREES, axis=RIGHT)
        _t_end.move_to(_c)
        t_disp.become(_t_end)
        _c = n_count.get_center()
        _n_end = Integer(
            _count_zeros_upto(T_MAX), font_size=FS_N + 4, color=GREEN
        )
        _n_end.rotate(90 * DEGREES, axis=RIGHT)
        _n_end.move_to(_c)
        n_count.become(_n_end)

        self.wait(3)
