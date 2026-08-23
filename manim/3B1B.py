"""
3Blue1Brown — Analytic Continuation 可视化（Manim Community Edition）

对应课文：
  https://www.3blue1brown.com/lessons/zeta/#analytic-continuation
原版场景参考：
  videos-master/_2016/zeta.py 中
  ShowZetaOnHalfPlane / SquiggleOnExtensions /
  IntroduceAnglePreservation / InfiniteContinuousJigsawPuzzle 等

教学主线：
  1. 右半平面 Re(s)>1 上的 ζ 级数共形变换
  2. 高亮 Im = ±i 弧线，引出「想把弧线继续画下去」
  3. 条件定义：Re(s)≤1 时级数失效，需「别的东西」
  4. 任意延伸似乎很多种；但要求处处可微则唯一
  5. 用 f(s)=s² 展示「解析 ⇔ 保角」（几何直觉）
  6. ζ 在右半平面解析；解析延拓 = 无限连续拼图
  7. 完整解析延拓后的 ζ 共形图（含左半平面）

依赖：manim>=0.18, mpmath, numpy
环境示例：
  conda activate manim-3b1b
  cd 素数分布与黎曼猜想8-11/manim
  manim -ql AnalyticContinuation_3b1b.py ZetaOnRightHalf
  manim -ql AnalyticContinuation_3b1b.py AnalyticContinuationStory
"""

from __future__ import annotations

import colorsys
from typing import Callable, Iterable, Optional, Sequence

import numpy as np
from manim import *
from mpmath import mp, zeta as mp_zeta

# 精度：动画网格用中等精度即可；过高会极慢
mp.dps = 10

# macOS 中文：Manim Text 用系统字体；MathTex 默认 latex 不能写中文
CN_FONT = "Songti SC"


def CNText(s: str, font_size: int = 28, color=WHITE, **kwargs) -> Text:
    """中文标题/旁白（Text + CJK 字体）。"""
    return Text(s, font=CN_FONT, font_size=font_size, color=color, **kwargs)


# ============================================================
# 数值与几何工具
# ============================================================

def safe_zeta(z: complex, clip: float = 40.0) -> complex:
    """mpmath.zeta，极点与溢出时做裁剪。"""
    if abs(z - 1.0) < 1e-8:
        return complex(clip, 0.0)
    try:
        w = complex(mp_zeta(z))
    except Exception:
        return complex(clip, 0.0)
    if not np.isfinite(w.real) or not np.isfinite(w.imag):
        return complex(clip, 0.0)
    if abs(w) > clip:
        w = w / abs(w) * clip
    return w


def safe_s_squared(z: complex, clip: float = 40.0) -> complex:
    w = z * z
    if abs(w) > clip:
        w = w / abs(w) * clip
    return w


def complex_lerp(z0: complex, z1: complex, t: float) -> complex:
    return (1.0 - t) * z0 + t * z1


def sample_segment(
    z_start: complex,
    z_end: complex,
    n: int,
) -> np.ndarray:
    ts = np.linspace(0.0, 1.0, n)
    return np.array([(1 - t) * z_start + t * z_end for t in ts], dtype=complex)


def map_samples(
    samples: np.ndarray,
    func: Callable[[complex], complex],
) -> np.ndarray:
    return np.array([func(complex(z)) for z in samples], dtype=complex)


def color_by_parameter(t: float, start_rgb, end_rgb) -> ManimColor:
    """t in [0,1] 线性插值 RGB。"""
    r = start_rgb[0] * (1 - t) + end_rgb[0] * t
    g = start_rgb[1] * (1 - t) + end_rgb[1] * t
    b = start_rgb[2] * (1 - t) + end_rgb[2] * t
    return ManimColor.from_rgb((r, g, b))


# ============================================================
# 复平面网格（可在变换前后插值）
# ============================================================

class ComplexGrid(VGroup):
    """
    由水平/垂直线段组成的复平面网格。
    每条线保存 math 采样点与 func 后的目标采样点，
    用 alpha ∈ [0,1] 做线性同伦（与 3B1B apply_complex_function 同类观感）。
    """

    def __init__(
        self,
        plane: Axes,
        h_samples: Sequence[np.ndarray],
        v_samples: Sequence[np.ndarray],
        h_colors: Optional[Sequence] = None,
        v_colors: Optional[Sequence] = None,
        stroke_width: float = 1.4,
        stroke_opacity: float = 0.85,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.plane = plane
        self.h_math = list(h_samples)
        self.v_math = list(v_samples)
        self.h_img: list[np.ndarray] = [s.copy() for s in self.h_math]
        self.v_img: list[np.ndarray] = [s.copy() for s in self.v_math]
        self.alpha = 0.0

        n_h = len(self.h_math)
        n_v = len(self.v_math)
        if h_colors is None:
            h_colors = [interpolate_color(BLUE_E, TEAL_A, i / max(n_h - 1, 1)) for i in range(n_h)]
        if v_colors is None:
            v_colors = [interpolate_color(YELLOW_E, RED_A, i / max(n_v - 1, 1)) for i in range(n_v)]

        self.h_lines = VGroup()
        for samples, col in zip(self.h_math, h_colors):
            line = VMobject(stroke_color=col, stroke_width=stroke_width, stroke_opacity=stroke_opacity)
            line.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in samples])
            self.h_lines.add(line)

        self.v_lines = VGroup()
        for samples, col in zip(self.v_math, v_colors):
            line = VMobject(stroke_color=col, stroke_width=stroke_width, stroke_opacity=stroke_opacity)
            line.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in samples])
            self.v_lines.add(line)

        self.add(self.h_lines, self.v_lines)

    def set_image_function(self, func: Callable[[complex], complex]):
        self.h_img = [map_samples(s, func) for s in self.h_math]
        self.v_img = [map_samples(s, func) for s in self.v_math]
        return self

    def set_alpha(self, alpha: float):
        self.alpha = float(np.clip(alpha, 0.0, 1.0))
        a = self.alpha
        plane = self.plane
        for line, src, dst in zip(self.h_lines, self.h_math, self.h_img):
            mid = (1 - a) * src + a * dst
            line.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in mid])
        for line, src, dst in zip(self.v_lines, self.v_math, self.v_img):
            mid = (1 - a) * src + a * dst
            line.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in mid])
        return self


def _densify_in_interval(
    base_vals: np.ndarray,
    *,
    span_lo: float,
    span_hi: float,
    dense_lo: float,
    dense_hi: float,
    dense_step: float,
) -> np.ndarray:
    """
    保留 base_vals 在加密区间外的采样；
    在 [dense_lo, dense_hi] ∩ [span_lo, span_hi] 内用 dense_step 加密。
    其余参数（区间外疏密由 base_vals 决定）不变。
    """
    base_vals = np.asarray(base_vals, dtype=float)
    outside = base_vals[(base_vals < dense_lo - 1e-12) | (base_vals > dense_hi + 1e-12)]
    d0 = max(span_lo, dense_lo)
    d1 = min(span_hi, dense_hi)
    if d0 > d1 + 1e-12:
        return np.unique(np.round(base_vals, 10))
    dense = np.arange(d0, d1 + 0.5 * dense_step, dense_step)
    dense = dense[(dense >= d0 - 1e-12) & (dense <= d1 + 1e-12)]
    return np.unique(np.round(np.concatenate([outside, dense]), 10))


def build_right_half_grid(
    plane: Axes,
    *,
    # —— 粉红色细网格规格 ——
    # 水平线：端点 (1.0, y) — (7.0, y)，y ∈ [-2, 2]，间距 0.0625
    h_x0: float = 1.0,
    h_x1: float = 7.0,
    h_y0: float = -2.0,
    h_y1: float = 2.0,
    h_step: float = 0.0625,
    # 垂直线：粉红起点 x=1.125，间距 0.0625，到 x=4
    v_x0: float = 1.125,
    v_x1: float = 4.0,
    v_y0: float = -4.0,
    v_y1: float = 4.0,
    v_step: float = 0.0625,
    pts: int = 100,
    # 兼容旧调用的占位参数（忽略）
    re_min: float = 1.0,
    re_max: float = 7.0,
    im_min: float = -4.0,
    im_max: float = 4.0,
    n_re: int = 18,
    n_im: int = 17,
    dense_near_one: bool = True,
) -> ComplexGrid:
    """
    粉红色 ζ 变换网格（右半平面细网格）：

    - 水平线：从 (1.0, y) 到 (7.0, y)，y ∈ [-2, 2]（间距 0.0625）
    - 垂直线：从 (x, 4) 到 (x, -4)，x 从 1.125 到 4（间距 0.0625）
    """
    # 水平线 y 采样（含端点 ±2）
    im_vals = np.round(np.arange(h_y0, h_y1 + 0.5 * h_step, h_step), 10)
    im_vals = im_vals[(im_vals >= h_y0 - 1e-12) & (im_vals <= h_y1 + 1e-12)]

    # 垂直线 x 采样（从 1+0.06 起，间距 0.06，到 4）
    re_vals = np.round(np.arange(v_x0, v_x1 + 0.5 * v_step, v_step), 10)
    re_vals = re_vals[(re_vals >= v_x0 - 1e-12) & (re_vals <= v_x1 + 1e-12)]

    h_samples = [
        sample_segment(complex(h_x0, y), complex(h_x1, y), pts)
        for y in im_vals
    ]
    v_samples = [
        sample_segment(complex(x, v_y1), complex(x, v_y0), pts)
        for x in re_vals
        if abs(x - 1.0) > 1e-9  # 不画 x=1
    ]

    n_h, n_v = len(h_samples), len(v_samples)
    # 粉红色系
    pink0 = ManimColor("#FF69B4")  # hot pink
    pink1 = ManimColor("#FFB6C1")  # light pink
    h_colors = [interpolate_color(pink0, pink1, i / max(n_h - 1, 1)) for i in range(n_h)]
    v_colors = [interpolate_color(pink1, pink0, i / max(n_v - 1, 1)) for i in range(n_v)]

    return ComplexGrid(
        plane, h_samples, v_samples,
        h_colors=h_colors,
        v_colors=v_colors,
        stroke_width=1.0,
        stroke_opacity=0.75,
    )


def build_mirror_grid_about_one(
    plane: Axes,
    *,
    # 与粉网格相同的几何参数，再关于 x=1 反射
    h_x0: float = 1.0,
    h_x1: float = 7.0,
    h_y0: float = -2.0,
    h_y1: float = 2.0,
    h_step: float = 0.0625,
    v_x0: float = 1.125,      # 与粉红一致，反射后左端起点为 0.875
    v_x1: float = 4.0,
    v_y0: float = -4.0,
    v_y1: float = 4.0,
    v_step: float = 0.0625,
    pts: int = 100,
    mirror_at: float = 1.0,
    blue_v_start: float = 0.875,  # 蓝色垂直网格起点
) -> ComplexGrid:
    """
    关于 Re s = 1 与粉红色网格对称的蓝色网格。

    右粉：垂直 x 从 1.125 起；左蓝：垂直 x 从 0.875 起（= 2−1.125），间距 0.0625
    """
    def refl(x: float) -> float:
        return 2.0 * mirror_at - x

    im_vals = np.round(np.arange(h_y0, h_y1 + 0.5 * h_step, h_step), 10)
    im_vals = im_vals[(im_vals >= h_y0 - 1e-12) & (im_vals <= h_y1 + 1e-12)]

    re_right = np.round(np.arange(v_x0, v_x1 + 0.5 * v_step, v_step), 10)
    re_right = re_right[(re_right >= v_x0 - 1e-12) & (re_right <= v_x1 + 1e-12)]
    # 由粉红反射，并保证最靠 1 的蓝竖线为 blue_v_start（0.875）
    re_left = np.unique(np.round(np.array([refl(x) for x in re_right]), 10))
    re_left = re_left[np.abs(re_left - mirror_at) > 1e-9]
    # 对齐到起点 0.875：保留 ≤ blue_v_start 的线，并确保含 0.875
    re_left = re_left[re_left <= blue_v_start + 1e-12]
    if not np.any(np.abs(re_left - blue_v_start) < 1e-9):
        re_left = np.unique(np.concatenate([re_left, [blue_v_start]]))

    # 水平线：从 mirror 反射后的右端到左端
    hx0_m, hx1_m = refl(h_x1), refl(h_x0)  # -5 与 1
    x_left, x_right = min(hx0_m, hx1_m), max(hx0_m, hx1_m)

    h_samples = [
        sample_segment(complex(x_left, y), complex(x_right, y), pts)
        for y in im_vals
    ]
    v_samples = [
        sample_segment(complex(x, v_y1), complex(x, v_y0), pts)
        for x in re_left
    ]

    n_h, n_v = len(h_samples), len(v_samples)
    blue0 = ManimColor("#1E90FF")  # dodger blue
    blue1 = ManimColor("#87CEEB")  # sky blue
    h_colors = [interpolate_color(blue0, blue1, i / max(n_h - 1, 1)) for i in range(n_h)]
    v_colors = [interpolate_color(blue1, blue0, i / max(n_v - 1, 1)) for i in range(n_v)]

    return ComplexGrid(
        plane, h_samples, v_samples,
        h_colors=h_colors,
        v_colors=v_colors,
        stroke_width=1.0,
        stroke_opacity=0.75,
    )


def build_full_plane_grid(
    plane: Axes,
    *,
    re_min: float = -4.0,
    re_max: float = 5.0,
    im_min: float = -4.0,
    im_max: float = 4.0,
    n_re: int = 22,
    n_im: int = 17,
    pts: int = 90,
    skip_re_one: bool = True,
) -> ComplexGrid:
    re_vals = np.linspace(re_min, re_max, n_re)
    im_vals = np.linspace(im_min, im_max, n_im)

    # 与右半平面一致：垂直细网格 x∈[1.1,4]，水平 y∈[-2,2]
    re_vals = _densify_in_interval(
        re_vals,
        span_lo=re_min,
        span_hi=re_max,
        dense_lo=1.1,
        dense_hi=4.0,
        dense_step=0.05,
    )
    im_vals = _densify_in_interval(
        im_vals,
        span_lo=im_min,
        span_hi=im_max,
        dense_lo=-2.0,
        dense_hi=2.0,
        dense_step=0.05,
    )

    h_samples = [
        sample_segment(complex(re_min, y), complex(re_max, y), pts)
        for y in im_vals
    ]
    v_samples = []
    for x in re_vals:
        if skip_re_one and abs(x - 1.0) < 0.08:
            continue
        v_samples.append(sample_segment(complex(x, im_min), complex(x, im_max), pts))
    n_lines = len(h_samples) + len(v_samples)
    sw = 0.6 if n_lines > 200 else 1.2
    so = 0.45 if n_lines > 200 else 0.85
    return ComplexGrid(plane, h_samples, v_samples, stroke_width=sw, stroke_opacity=so)


def build_s_squared_grid(
    plane: Axes,
    *,
    re_min: float = -3.5,
    re_max: float = 3.5,
    im_min: float = -2.8,
    im_max: float = 2.8,
    step: float = 0.5,
    pts: int = 70,
) -> ComplexGrid:
    re_vals = np.arange(re_min, re_max + 1e-9, step)
    im_vals = np.arange(im_min, im_max + 1e-9, step)
    h_samples = [
        sample_segment(complex(re_min, y), complex(re_max, y), pts)
        for y in im_vals
        if abs(y) > 1e-9 or True
    ]
    v_samples = [
        sample_segment(complex(x, im_min), complex(x, im_max), pts)
        for x in re_vals
    ]
    return ComplexGrid(plane, h_samples, v_samples)


def make_complex_axes(
    x_range=(-7, 7, 1),
    y_range=(-4, 4, 1),
    *,
    max_x_length: float = 13.5,
    max_y_length: float = 7.5,
) -> Axes:
    """
    复平面坐标轴：原点在画面中心；x、y 单位长度相等（正方形格子）。
    默认 x∈[-7,7]、y∈[-4,4]。
    """
    x_span = float(x_range[1] - x_range[0])
    y_span = float(y_range[1] - y_range[0])
    if x_span <= 0 or y_span <= 0:
        raise ValueError("x_range / y_range 跨度必须为正")
    # 同一 unit：1 个复长度 → 相同屏幕长度
    unit = min(max_x_length / x_span, max_y_length / y_span)
    axes = Axes(
        x_range=list(x_range),
        y_range=list(y_range),
        x_length=unit * x_span,
        y_length=unit * y_span,
        axis_config={
            "include_tip": False,
            "color": GREY_B,
            "stroke_width": 1.8,
        },
        tips=False,
    )
    # 原点置于画面中心
    axes.move_to(ORIGIN)
    return axes


def make_unit_coord_grid(
    axes: Axes,
    *,
    color=BLUE_D,
    stroke_width: float = 0.8,
    stroke_opacity: float = 0.55,
    step: float = 1.0,
) -> VGroup:
    """
    蓝色坐标网格：间距 step（默认 1），铺满 axes 的 x/y 范围。
    不画坐标轴本身（轴由 Axes 负责）。
    """
    x0, x1 = float(axes.x_range[0]), float(axes.x_range[1])
    y0, y1 = float(axes.y_range[0]), float(axes.y_range[1])
    grid = VGroup()
    # 竖线 x = k
    xs = np.arange(x0, x1 + 0.5 * step, step)
    for x in xs:
        if abs(x) < 1e-12:
            continue  # 与 y 轴重合，跳过
        grid.add(Line(
            axes.coords_to_point(x, y0),
            axes.coords_to_point(x, y1),
            color=color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
        ))
    # 水平线 y = k
    ys = np.arange(y0, y1 + 0.5 * step, step)
    for y in ys:
        if abs(y) < 1e-12:
            continue  # 与 x 轴重合，跳过
        grid.add(Line(
            axes.coords_to_point(x0, y),
            axes.coords_to_point(x1, y),
            color=color,
            stroke_width=stroke_width,
            stroke_opacity=stroke_opacity,
        ))
    return grid


def build_white_unit_transform_grid(
    plane: Axes,
    *,
    step: float = 1.0,
    pts: int = 120,
    stroke_width: float = 1.6,
    stroke_opacity: float = 0.95,
    skip_re_one: bool = True,
    skip_border: bool = True,
) -> ComplexGrid:
    """
    覆盖在「间距 step 蓝色坐标网格」上的白色线，参与 ζ 变换。
    几何与 make_unit_coord_grid 一致（跳过 x=0、y=0 轴）；
    默认跳过 x=1 竖线（ζ 极点）；
    默认跳过边框四条线（x=x0, x=x1, y=y0, y=y1），边框不参加变换。
    """
    x0, x1 = float(plane.x_range[0]), float(plane.x_range[1])
    y0, y1 = float(plane.y_range[0]), float(plane.y_range[1])

    xs = np.round(np.arange(x0, x1 + 0.5 * step, step), 10)
    ys = np.round(np.arange(y0, y1 + 0.5 * step, step), 10)

    h_samples = []
    for y in ys:
        if abs(y) < 1e-12:
            continue  # 与 x 轴重合
        if skip_border and (abs(y - y0) < 1e-9 or abs(y - y1) < 1e-9):
            continue  # 上下边框不参加变换
        h_samples.append(sample_segment(complex(x0, y), complex(x1, y), pts))

    v_samples = []
    for x in xs:
        if abs(x) < 1e-12:
            continue  # 与 y 轴重合
        if skip_re_one and abs(x - 1.0) < 1e-9:
            continue
        if skip_border and (abs(x - x0) < 1e-9 or abs(x - x1) < 1e-9):
            continue  # 左右边框不参加变换
        v_samples.append(sample_segment(complex(x, y0), complex(x, y1), pts))

    n_h, n_v = len(h_samples), len(v_samples)
    white = WHITE
    h_colors = [white] * n_h
    v_colors = [white] * n_v
    return ComplexGrid(
        plane, h_samples, v_samples,
        h_colors=h_colors,
        v_colors=v_colors,
        stroke_width=stroke_width,
        stroke_opacity=stroke_opacity,
    )


def add_axis_labels(axes: Axes, font_size: int = 22) -> VGroup:
    labels = VGroup()
    x0, x1 = int(round(axes.x_range[0])), int(round(axes.x_range[1]))
    y0, y1 = int(round(axes.y_range[0])), int(round(axes.y_range[1]))
    # 实轴刻度（全整数标注）
    for x in range(x0, x1 + 1):
        if x == 0:
            continue
        p = axes.coords_to_point(x, 0)
        tick = Line(p + 0.08 * DOWN, p + 0.08 * UP, color=GREY_B, stroke_width=1.2)
        lab = MathTex(str(x), font_size=font_size, color=GREY_A)
        lab.next_to(p, DOWN, buff=0.12)
        labels.add(tick, lab)
    for y in range(y0, y1 + 1):
        if y == 0:
            continue
        p = axes.coords_to_point(0, y)
        tick = Line(p + 0.08 * LEFT, p + 0.08 * RIGHT, color=GREY_B, stroke_width=1.2)
        if y == 1:
            tex = r"i"
        elif y == -1:
            tex = r"-i"
        else:
            tex = rf"{y}i"
        lab = MathTex(tex, font_size=font_size, color=BLUE_B)
        lab.next_to(p, LEFT, buff=0.12)
        labels.add(tick, lab)
    origin = MathTex("0", font_size=font_size, color=GREY_A)
    origin.next_to(axes.coords_to_point(0, 0), DL, buff=0.08)
    labels.add(origin)
    return labels


def bg_tex(mob: Mobject, opacity: float = 0.75) -> VGroup:
    rect = BackgroundRectangle(mob, color=BLACK, fill_opacity=opacity, buff=0.08)
    return VGroup(rect, mob)


# ============================================================
# 场景 1：右半平面上的 ζ 变换（仅粉红右半细网格）
# ============================================================

class ZetaOnRightHalf(Scene):
    """
    右半平面 Re(s)>1 上的 ζ 级数共形变换。
    仅粉红右半细网格（无左侧关于 x=1 的蓝色细网格）。
    """

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        # 蓝色单位坐标网格：固定不动（底层，非细网格）
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane)
        self.add(coord_grid, plane, labels)

        title = MathTex(
            r"\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^{s}}",
            font_size=36,
        )
        title.to_corner(UL, buff=0.35)
        domain = MathTex(r"\operatorname{Re}(s)>1", font_size=30, color=YELLOW)
        domain.next_to(title, DOWN, aligned_edge=LEFT, buff=0.15)
        self.play(Write(bg_tex(title)), FadeIn(bg_tex(domain)))
        self.wait(0.5)

        # 仅粉红右半细网格；白：单位线参与变换并淡出
        grid = build_right_half_grid(plane)
        grid_white = build_white_unit_transform_grid(plane, step=1.0)
        grid.set_image_function(safe_zeta)
        grid_white.set_image_function(safe_zeta)
        self.play(Create(grid), Create(grid_white), run_time=2.5)
        self.wait(0.6)

        alpha = ValueTracker(0.0)
        white_op0 = 0.95

        grid.add_updater(lambda m, tr=alpha: m.set_alpha(tr.get_value()))

        def upd_white(m: ComplexGrid):
            a = alpha.get_value()
            m.set_alpha(a)
            fade = max(0.0, 1.0 - a)
            m.set_stroke(opacity=white_op0 * fade)

        grid_white.add_updater(upd_white)
        self.play(alpha.animate.set_value(1.0), run_time=6, rate_func=smooth)
        grid.clear_updaters()
        grid_white.clear_updaters()
        grid.set_alpha(1.0)
        grid_white.set_alpha(1.0)
        grid_white.set_stroke(opacity=0.0)
        grid_white.set_opacity(0.0)
        self.wait(1.5)


# ============================================================
# 场景 2：高亮 Im=±i，想「继续那些弧」
# ============================================================

class ContinueTheArcs(Scene):
    """
    课文：highlight lines Im = ±i → lovely arcs that abruptly stop
    → don't you want to continue those arcs?
    """

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane)
        self.add(coord_grid, plane, labels)

        title = CNText("继续那些弧线？", font_size=32, color=YELLOW)
        title.to_corner(UL, buff=0.35)
        self.play(FadeIn(bg_tex(title)))

        grid = build_right_half_grid(plane, n_re=14, n_im=13, pts=70)
        grid.set_image_function(safe_zeta)
        # 先显示未变换网格
        self.add(grid)

        # Im = ±1 的水平线（右半）
        def make_im_line(im: float, color) -> VMobject:
            samples = sample_segment(complex(1.02, im), complex(5.5, im), 100)
            line = VMobject(stroke_color=color, stroke_width=4, stroke_opacity=1)
            line.set_points_smoothly(
                [plane.coords_to_point(z.real, z.imag) for z in samples]
            )
            line.math = samples
            line.img = map_samples(samples, safe_zeta)
            return line

        line_up = make_im_line(1.0, YELLOW)
        line_dn = make_im_line(-1.0, YELLOW)
        im_lab = MathTex(r"\operatorname{Im}s=\pm 1", font_size=28, color=YELLOW)
        im_lab.to_corner(UR, buff=0.4)

        self.play(Create(line_up), Create(line_dn), FadeIn(bg_tex(im_lab)))
        self.wait(0.6)

        alpha = ValueTracker(0.0)

        def morph_line(line: VMobject):
            a = alpha.get_value()
            mid = (1 - a) * line.math + a * line.img
            line.set_points_smoothly(
                [plane.coords_to_point(z.real, z.imag) for z in mid]
            )

        def upd_all(_=None):
            grid.set_alpha(alpha.get_value())
            morph_line(line_up)
            morph_line(line_dn)

        grid.add_updater(lambda m: m.set_alpha(alpha.get_value()))
        line_up.add_updater(lambda m: morph_line(m))
        line_dn.add_updater(lambda m: morph_line(m))

        self.play(alpha.animate.set_value(1.0), run_time=5.5, rate_func=smooth)
        for m in (grid, line_up, line_dn):
            m.clear_updaters()
        self.wait(0.8)

        stop = CNText("弧线在边界处戛然而止…", font_size=28, color=RED_B)
        stop.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(bg_tex(stop)))
        self.wait(1.0)

        # 左半 Im=±1 经 ζ 的像（解析延拓）
        left_samples_up = sample_segment(complex(-3.5, 1.0), complex(0.98, 1.0), 120)
        left_samples_dn = sample_segment(complex(-3.5, -1.0), complex(0.98, -1.0), 120)
        cont_up = VMobject(stroke_color=BLUE, stroke_width=3.5, stroke_opacity=0.9)
        cont_dn = VMobject(stroke_color=BLUE, stroke_width=3.5, stroke_opacity=0.9)
        cont_up.set_points_smoothly(
            [plane.coords_to_point(z.real, z.imag) for z in map_samples(left_samples_up, safe_zeta)]
        )
        cont_dn.set_points_smoothly(
            [plane.coords_to_point(z.real, z.imag) for z in map_samples(left_samples_dn, safe_zeta)]
        )

        wish = CNText("难道不想把这些弧继续画完吗？", font_size=28, color=BLUE)
        wish.to_edge(DOWN, buff=0.35)
        self.play(FadeOut(stop), FadeIn(bg_tex(wish)))
        self.play(Create(cont_up), Create(cont_dn), run_time=3.5)
        self.wait(1.5)
        self.play(FadeOut(wish))
        self.wait(0.5)


# ============================================================
# 场景 3：条件定义
# ============================================================

class ConditionalDefinition(Scene):
    """
    课文 How to extend?：
      ζ(s) = sum  if Re(s)>1
           = ???  if Re(s)≤1
    """

    def construct(self):
        zeta = MathTex(r"\zeta(s)=", font_size=48)
        zeta[0][2].set_color(YELLOW)

        sigma = MathTex(
            r"\displaystyle\sum_{n=1}^{\infty}\frac{1}{n^{s}}",
            font_size=40,
        )
        sigma[0][-1].set_color(YELLOW)
        other = CNText("Something else…", font_size=34, color=GREEN_B)
        # 旁白中文另放，避免 Brace.get_text 走 latex
        other_cn = CNText("别的东西…", font_size=26, color=GREEN_B)

        defs = VGroup(sigma, other).arrange(DOWN, buff=0.7, aligned_edge=LEFT)
        brace = Brace(defs, LEFT, buff=0.15)
        zeta.next_to(brace, LEFT, buff=0.15)

        conds = VGroup(
            MathTex(r"\text{if }\operatorname{Re}(s)>1", font_size=32),
            MathTex(r"\text{if }\operatorname{Re}(s)\le 1", font_size=32),
        ).arrange(DOWN, buff=0.85)
        conds.next_to(defs, RIGHT, buff=0.9)

        # 先只显示级数定义
        sigma_inline = sigma.copy().next_to(zeta, RIGHT, buff=0.15)
        group0 = VGroup(zeta, sigma_inline).move_to(ORIGIN)
        self.play(Write(group0))
        self.wait(0.8)

        # 展开成分段
        self.play(
            zeta.animate.next_to(brace, LEFT, buff=0.15),
            ReplacementTransform(sigma_inline, sigma),
            GrowFromCenter(brace),
            FadeIn(other),
            FadeIn(conds),
            run_time=1.8,
        )
        self.wait(0.8)

        under = Brace(other, DOWN)
        q = CNText("What to put here?  这里该填什么？", font_size=26, color=GREEN_B)
        q.next_to(under, DOWN, buff=0.15)
        self.play(GrowFromCenter(under), FadeIn(q), other.animate.set_color(GREEN_B))
        self.wait(1.2)

        warn = VGroup(
            MathTex(r"1+2+3+4+\cdots", font_size=30, color=RED_B),
            CNText("级数在 Re(s)≤1 时发散", font_size=26, color=RED_B),
        ).arrange(RIGHT, buff=0.35)
        warn.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(bg_tex(warn)))
        self.wait(2.0)


# ============================================================
# 场景 4：看似任意的延伸 vs 唯一解析延拓
# ============================================================

class ManyExtensions(Scene):
    """
    课文：you can squiggle any extension…
    but requiring a derivative everywhere locks one unique extension.
    以 s=-1 ↦ -1/12 为锚点。
    """

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane, font_size=20)
        self.add(coord_grid, plane, labels)

        title = CNText("延伸有很多种？", font_size=30, color=YELLOW)
        title.to_corner(UL, buff=0.3)
        self.play(FadeIn(bg_tex(title)))

        # 右半网格 → ζ
        right = build_right_half_grid(
            plane, re_min=1.05, re_max=4.8, im_min=-2.8, im_max=2.8,
            n_re=12, n_im=11, pts=60,
        )
        right.set_image_function(safe_zeta)
        right.set_alpha(1.0)
        self.add(right)

        # 左半「假延伸」：若干扭曲
        left_math_h = [
            sample_segment(complex(-3.5, y), complex(0.95, y), 50)
            for y in np.linspace(-2.5, 2.5, 9)
        ]
        left_math_v = [
            sample_segment(complex(x, -2.5), complex(x, 2.5), 50)
            for x in np.linspace(-3.5, 0.8, 8)
        ]

        def warped(func_point):
            h_img = [np.array([func_point(complex(z)) for z in s], dtype=complex) for s in left_math_h]
            v_img = [np.array([func_point(complex(z)) for z in s], dtype=complex) for s in left_math_v]
            g = ComplexGrid(
                plane, left_math_h, left_math_v,
                h_colors=[GREY_B] * len(left_math_h),
                v_colors=[GREY_A] * len(left_math_v),
                stroke_width=1.2,
                stroke_opacity=0.75,
            )
            g.h_img, g.v_img = h_img, v_img
            g.set_alpha(1.0)
            return g

        # 真正的解析延拓
        true_left = warped(safe_zeta)

        # 几种「乱画」的延伸（对左半平面点做额外剪切/扭曲后再看位置）
        def shear(z: complex) -> complex:
            # 在真正 ζ 附近扭动（演示用，非数学定义）
            w = safe_zeta(z)
            x, y = w.real, w.imag
            return complex(x, y + 0.35 * (1 - z.real) ** 2 * 0.15)

        def wiggle(z: complex) -> complex:
            w = safe_zeta(z)
            return complex(
                w.real - 0.25 * np.sin(z.real) * np.sin(z.imag),
                w.imag - 0.25 * np.sin(z.real) * np.cos(z.imag),
            )

        def stretch(z: complex) -> complex:
            w = safe_zeta(z)
            s = 1.0 + 0.12 * (0.5 - z.real)
            return complex(s * w.real, (s ** 1.3) * w.imag)

        variants = [true_left, warped(shear), warped(wiggle), warped(stretch), true_left]
        # 标题用 Text，避免 MathTex 中文
        captions = [
            ("math", r"\zeta(-1)=-\frac{1}{12}"),
            ("cn", "乱画延伸 A"),
            ("cn", "乱画延伸 B"),
            ("cn", "乱画延伸 C"),
            ("cn", "只有处处可微的那一种延伸"),
        ]

        # 标记 -1 与 -1/12
        dot_in = Dot(plane.coords_to_point(-1, 0), color=YELLOW, radius=0.07)
        lab_in = MathTex("-1", font_size=26, color=YELLOW)
        lab_in.next_to(dot_in, UL, buff=0.1)
        self.play(FadeIn(dot_in), FadeIn(bg_tex(lab_in)))
        self.wait(0.3)

        # 点从 -1 移到 -1/12
        target = plane.coords_to_point(-1 / 12, 0)
        lab_out = MathTex(r"-1/12", font_size=26, color=YELLOW)
        lab_out.next_to(target, UP, buff=0.12)
        self.play(
            dot_in.animate.move_to(target),
            FadeOut(lab_in),
            FadeIn(bg_tex(lab_out)),
            run_time=2.0,
        )
        self.wait(0.4)

        def make_caption(kind: str, content: str) -> Mobject:
            if kind == "math":
                m = MathTex(content, font_size=32, color=YELLOW)
            else:
                m = CNText(content, font_size=28, color=YELLOW)
            m.to_edge(DOWN, buff=0.35)
            return bg_tex(m)

        left_mob = true_left
        self.play(FadeIn(left_mob), run_time=1.2)
        cap_bg = make_caption(*captions[0])
        self.play(FadeIn(cap_bg))
        self.wait(1.0)

        for g_new, cap_spec in zip(variants[1:], captions[1:]):
            new_bg = make_caption(*cap_spec)
            self.play(
                Transform(left_mob, g_new),
                FadeOut(cap_bg),
                FadeIn(new_bg),
                run_time=2.2,
            )
            cap_bg = new_bg
            self.wait(0.9)

        lock = CNText(
            "要求处处有导数（解析）⇒ 至多一种延拓",
            font_size=26,
            color=GREEN_B,
        )
        lock.to_edge(DOWN, buff=0.35)
        self.play(FadeOut(cap_bg), FadeIn(bg_tex(lock)))
        self.play(Transform(left_mob, true_left.copy()), run_time=1.8)
        self.wait(2.0)


# ============================================================
# 场景 5：f(s)=s² 的保角性
# ============================================================

class AnglePreservation(Scene):
    """
    课文：s² 变换下任意两线交角不变（解析的几何直觉）。
    """

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane, font_size=20)
        self.add(coord_grid, plane, labels)

        title = MathTex(r"f(s)=s^{2}", font_size=42)
        title.to_corner(UL, buff=0.35)
        self.play(Write(bg_tex(title)))

        # 具体点：2→4, -1→1, i→-1
        examples = [
            (2 + 0j, 4 + 0j, r"2\mapsto 4"),
            (-1 + 0j, 1 + 0j, r"-1\mapsto 1"),
            (1j, -1 + 0j, r"i\mapsto -1"),
        ]
        dots_in = VGroup()
        dots_out = VGroup()
        for z, w, _ in examples:
            d0 = Dot(plane.coords_to_point(z.real, z.imag), color=YELLOW, radius=0.07)
            d1 = Dot(plane.coords_to_point(w.real, w.imag), color=BLUE, radius=0.07)
            dots_in.add(d0)
            dots_out.add(d1)

        for d0, d1, (_, _, tex) in zip(dots_in, dots_out, examples):
            lab = MathTex(tex, font_size=24)
            lab.next_to(d0, UP, buff=0.1)
            self.play(FadeIn(d0), FadeIn(bg_tex(lab)))
            self.play(TransformFromCopy(d0, d1), run_time=0.8)
            self.play(FadeOut(lab))
        self.wait(0.4)

        grid = build_s_squared_grid(plane, step=0.5, pts=60)
        grid.set_image_function(safe_s_squared)
        self.play(Create(grid), run_time=1.5)
        self.play(FadeOut(dots_in), FadeOut(dots_out))

        alpha = ValueTracker(0.0)
        grid.add_updater(lambda m: m.set_alpha(alpha.get_value()))
        self.play(alpha.animate.set_value(1.0), run_time=5.0, rate_func=smooth)
        grid.clear_updaters()
        self.wait(0.6)

        # 两条相交线 + 角度
        # 选交点 p=1+0.5i，两条方向
        p = complex(1.2, 0.6)
        dir1 = complex(1, 0.3)
        dir2 = complex(0.2, 1)
        dir1 /= abs(dir1)
        dir2 /= abs(dir2)

        def line_through(center: complex, direction: complex, half_len=1.6, n=40):
            return sample_segment(
                center - half_len * direction,
                center + half_len * direction,
                n,
            )

        s1 = line_through(p, dir1)
        s2 = line_through(p, dir2)
        L1 = VMobject(color=YELLOW, stroke_width=3.5)
        L2 = VMobject(color=YELLOW, stroke_width=3.5)
        L1.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in s1])
        L2.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in s2])

        ang = np.angle(dir2 / dir1)
        deg = abs(int(round(np.degrees(ang))))
        arc = Arc(
            start_angle=np.angle(dir1),
            angle=ang,
            radius=0.35,
            color=YELLOW,
        ).move_arc_center_to(plane.coords_to_point(p.real, p.imag))
        ang_lab = MathTex(rf"{deg}^\circ", font_size=28, color=YELLOW)
        ang_lab.next_to(arc, UR, buff=0.1)

        # 重置网格再演示保角
        self.play(FadeOut(grid))
        grid2 = build_s_squared_grid(plane, step=0.5, pts=60)
        grid2.set_image_function(safe_s_squared)
        grid2.set_stroke(opacity=0.35)
        self.play(FadeIn(grid2), Create(L1), Create(L2), Create(arc), FadeIn(bg_tex(ang_lab)))
        self.wait(0.8)

        # 变换线与角
        s1i = map_samples(s1, safe_s_squared)
        s2i = map_samples(s2, safe_s_squared)
        L1t = VMobject(color=YELLOW, stroke_width=3.5)
        L2t = VMobject(color=YELLOW, stroke_width=3.5)
        L1t.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in s1i])
        L2t.set_points_smoothly([plane.coords_to_point(z.real, z.imag) for z in s2i])

        # 像点导数旋转：f'(p)=2p
        fp = 2 * p
        rot = np.angle(fp)
        # 变换后两切向
        t1 = fp * dir1
        t2 = fp * dir2
        ang2 = np.angle(t2 / t1)
        pt = safe_s_squared(p)
        arc2 = Arc(
            start_angle=np.angle(t1),
            angle=ang2,
            radius=0.35,
            color=YELLOW,
        ).move_arc_center_to(plane.coords_to_point(pt.real, pt.imag))

        alpha2 = ValueTracker(0.0)
        grid2.add_updater(lambda m: m.set_alpha(alpha2.get_value()))

        self.play(
            alpha2.animate.set_value(1.0),
            Transform(L1, L1t),
            Transform(L2, L2t),
            Transform(arc, arc2),
            ang_lab.animate.next_to(arc2, UR, buff=0.1),
            run_time=4.5,
            rate_func=smooth,
        )
        grid2.clear_updaters()
        self.wait(0.8)

        msg = CNText("交角保持不变（曲线可变弯）", font_size=28, color=YELLOW)
        msg.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(bg_tex(msg)))
        self.wait(1.2)

        equiv = MathTex(
            r"\text{``analytic''}\ \Longleftrightarrow\ \text{angle-preserving}",
            font_size=34,
            color=YELLOW,
        )
        kind = CNText("…某种程度上", font_size=24, color=RED_B)
        equiv.to_edge(UP, buff=0.9)
        kind.next_to(equiv, RIGHT, buff=0.2)
        self.play(FadeOut(title), Write(bg_tex(equiv)))
        self.wait(0.8)
        self.play(FadeIn(bg_tex(kind)))
        self.wait(1.5)

        caveat = CNText(
            "注：f'(s)=0 的点上角度会被整数倍放大，那是少数例外",
            font_size=22,
            color=GREY_A,
        )
        caveat.to_edge(DOWN, buff=0.3)
        self.play(FadeOut(msg), FadeIn(bg_tex(caveat)))
        self.wait(2.0)


# ============================================================
# 场景 6：ζ 在右半平面解析 + 无限拼图
# ============================================================

class AnalyticContinuationUnique(Scene):
    """
    课文：ζ on right half is analytic (right angles remain);
    extending while staying analytic is an infinite continuous jigsaw puzzle.
    """

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane, font_size=20)
        self.add(coord_grid, plane, labels)

        title = MathTex(
            r"\zeta(s)=\sum_{n=1}^{\infty}\frac{1}{n^{s}}",
            font_size=34,
        )
        title.to_corner(UL, buff=0.3)
        self.play(Write(bg_tex(title)))

        right = build_right_half_grid(
            plane, re_min=1.05, re_max=5.0, im_min=-2.8, im_max=2.8,
            n_re=14, n_im=12, pts=65,
        )
        right.set_image_function(safe_zeta)
        self.play(Create(right), run_time=1.5)

        alpha = ValueTracker(0.0)
        right.add_updater(lambda m: m.set_alpha(alpha.get_value()))
        self.play(alpha.animate.set_value(1.0), run_time=5.0, rate_func=smooth)
        right.clear_updaters()
        self.wait(0.5)

        note = CNText("网格线的像仍然近似正交 → ζ 在右半平面解析", font_size=24, color=YELLOW)
        note.to_edge(DOWN, buff=0.35)
        self.play(FadeIn(bg_tex(note)))
        self.wait(1.5)
        self.play(FadeOut(note))

        # 拼图标题
        jigsaw = Text("Infinite continuous jigsaw puzzle", font_size=30, color=WHITE)
        jigsaw_cn = CNText("无限连续拼图：保角条件锁死唯一延拓", font_size=24, color=YELLOW)
        jigsaw.to_edge(UP, buff=0.35)
        jigsaw_cn.next_to(jigsaw, DOWN, buff=0.12)
        self.play(FadeOut(title), FadeIn(bg_tex(jigsaw)), FadeIn(bg_tex(jigsaw_cn)))

        # 左半平面按条带逐片淡入（解析延拓后的像）
        strips = VGroup()
        im_breaks = np.linspace(-2.8, 2.8, 8)
        for y0, y1 in zip(im_breaks[:-1], im_breaks[1:]):
            h = [
                sample_segment(complex(-4.0, y), complex(0.95, y), 55)
                for y in np.linspace(y0, y1, 3)
            ]
            v = [
                sample_segment(complex(x, y0), complex(x, y1), 40)
                for x in np.linspace(-4.0, 0.9, 5)
            ]
            piece = ComplexGrid(
                plane, h, v,
                h_colors=[PURPLE_A] * len(h),
                v_colors=[PURPLE_B] * len(v),
                stroke_width=1.3,
                stroke_opacity=0.85,
            )
            piece.set_image_function(safe_zeta)
            piece.set_alpha(1.0)
            strips.add(piece)

        order = list(range(len(strips)))
        rng = np.random.default_rng(3)
        rng.shuffle(order)
        for i in order:
            self.play(FadeIn(strips[i]), run_time=0.45)
        self.wait(0.8)

        name = Text("Analytic Continuation", font_size=36, color=YELLOW)
        name_cn = CNText("解析延拓", font_size=28, color=YELLOW)
        name.next_to(jigsaw_cn, DOWN, buff=0.35)
        name_cn.next_to(name, DOWN, buff=0.1)
        self.play(Write(bg_tex(name)), FadeIn(bg_tex(name_cn)))
        self.wait(2.0)


# ============================================================
# 场景 7：全平面解析延拓一览（真正全平面网格，非半平面）
# ============================================================

class FullPlaneZeta(Scene):
    """
    全平面 ζ 共形映射（解析延拓后）。
    使用 build_full_plane_grid（Re 跨越左右半平面），与场景 1 的右半级数网格不同。
    """

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane, font_size=20)
        self.add(coord_grid, plane, labels)

        title = MathTex(
            r"\zeta:\ \mathbb{C}\setminus\{1\}\to\mathbb{C}",
            font_size=36,
        )
        title.to_corner(UL, buff=0.3)
        sub = CNText("唯一解析延拓后的共形图（全平面）", font_size=24, color=GREY_A)
        sub.next_to(title, DOWN, aligned_edge=LEFT)
        self.play(Write(bg_tex(title)), FadeIn(bg_tex(sub)))

        grid = build_full_plane_grid(
            plane,
            re_min=-4.0,
            re_max=5.0,
            im_min=-3.0,
            im_max=3.0,
            n_re=20,
            n_im=15,
            pts=70,
        )
        grid.set_image_function(safe_zeta)
        self.play(Create(grid), run_time=2.0)

        # 临界线
        crit_samples = sample_segment(complex(0.5, -3.0), complex(0.5, 3.0), 120)
        crit = VMobject(color=RED, stroke_width=2.5, stroke_opacity=0.9)
        crit.set_points_smoothly(
            [plane.coords_to_point(z.real, z.imag) for z in crit_samples]
        )
        crit.math = crit_samples
        crit.img = map_samples(crit_samples, safe_zeta)
        self.play(Create(crit))
        crit_lab = MathTex(r"\operatorname{Re}s=\tfrac12", font_size=24, color=RED)
        crit_lab.next_to(plane.coords_to_point(0.5, 2.6), RIGHT, buff=0.1)
        self.play(FadeIn(bg_tex(crit_lab)))

        alpha = ValueTracker(0.0)

        def morph_crit(m):
            a = alpha.get_value()
            mid = (1 - a) * m.math + a * m.img
            m.set_points_smoothly(
                [plane.coords_to_point(z.real, z.imag) for z in mid]
            )

        grid.add_updater(lambda m: m.set_alpha(alpha.get_value()))
        crit.add_updater(morph_crit)
        self.play(alpha.animate.set_value(1.0), run_time=7.0, rate_func=smooth)
        grid.clear_updaters()
        crit.clear_updaters()
        self.wait(2.0)


# ============================================================
# 串联故事（可一次渲染完整叙事）
# ============================================================

class AnalyticContinuationStory(Scene):
    """
    按 3B1B 课文顺序压缩串联（适合导出一条完整短片）。
    细节更完整的版本请分别渲染上面各 Scene。
    """

    def construct(self):
        # ---- 标题 ----
        head = Text("Analytic Continuation", font_size=44, color=YELLOW)
        sub = Text("3Blue1Brown · Riemann zeta", font_size=28, color=GREY_A)
        sub.next_to(head, DOWN)
        self.play(Write(head), FadeIn(sub))
        self.wait(1.2)
        self.play(FadeOut(head), FadeOut(sub))

        # ---- 右半平面变换 ----
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid = make_unit_coord_grid(plane, color=BLUE_D, step=1.0)
        labels = add_axis_labels(plane, font_size=20)
        formula = MathTex(
            r"\zeta(s)=\sum_{n=1}^{\infty} n^{-s},\quad \operatorname{Re}s>1",
            font_size=32,
        )
        formula.to_corner(UL, buff=0.3)
        self.play(
            FadeIn(coord_grid), Create(plane), FadeIn(labels), Write(bg_tex(formula))
        )

        grid = build_right_half_grid(
            plane, re_min=1.05, re_max=5.0, im_min=-2.8, im_max=2.8,
            n_re=14, n_im=12, pts=60,
        )
        grid.set_image_function(safe_zeta)
        self.play(Create(grid), run_time=1.2)
        alpha = ValueTracker(0.0)
        grid.add_updater(lambda m: m.set_alpha(alpha.get_value()))
        self.play(alpha.animate.set_value(1.0), run_time=5.0)
        grid.clear_updaters()
        self.wait(0.6)

        # ---- 条件定义闪现 ----
        self.play(*[FadeOut(m) for m in self.mobjects])
        sigma = MathTex(
            r"\zeta(s)=\begin{cases}"
            r"\sum n^{-s}, & \operatorname{Re}s>1\\"
            r"\text{analytic continuation}, & \text{elsewhere}"
            r"\end{cases}",
            font_size=36,
        )
        self.play(Write(sigma))
        self.wait(1.5)
        self.play(FadeOut(sigma))

        # ---- 保角一句话 ----
        eq = MathTex(
            r"\text{analytic}\ \Longleftrightarrow\ \text{angle-preserving}",
            font_size=40,
            color=YELLOW,
        )
        self.play(Write(eq))
        self.wait(1.2)
        self.play(FadeOut(eq))

        # ---- 全平面 ----
        plane2 = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        coord_grid2 = make_unit_coord_grid(plane2, color=BLUE_D, step=1.0)
        labels2 = add_axis_labels(plane2, font_size=20)
        self.play(FadeIn(coord_grid2), Create(plane2), FadeIn(labels2))
        full = build_full_plane_grid(
            plane2, re_min=-3.8, re_max=4.8, im_min=-2.8, im_max=2.8,
            n_re=18, n_im=13, pts=55,
        )
        full.set_image_function(safe_zeta)
        self.play(Create(full), run_time=1.0)
        a2 = ValueTracker(0.0)
        full.add_updater(lambda m: m.set_alpha(a2.get_value()))
        self.play(a2.animate.set_value(1.0), run_time=6.0)
        full.clear_updaters()

        end = CNText("解析延拓：唯一的、保角的无限拼图", font_size=30, color=YELLOW)
        end.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(bg_tex(end)))
        self.wait(2.5)


# ============================================================
# 低配预览（无 mpmath 重计算时可换）
# ============================================================

class GridMorphSmokeTest(Scene):
    """快速冒烟：只测 s² 网格变换，不依赖 zeta 精度。"""

    def construct(self):
        plane = make_complex_axes(x_range=(-7, 7, 1), y_range=(-4, 4, 1))
        self.add(
            make_unit_coord_grid(plane, color=BLUE_D, step=1.0),
            plane,
            add_axis_labels(plane),
        )
        grid = build_s_squared_grid(plane, step=0.75, pts=40)
        grid.set_image_function(safe_s_squared)
        self.add(grid)
        alpha = ValueTracker(0)
        grid.add_updater(lambda m: m.set_alpha(alpha.get_value()))
        self.play(alpha.animate.set_value(1), run_time=3)
        grid.clear_updaters()
        self.wait(0.5)
