# Filename: 素数计数公式逼近.py
# 第 20 章视频 3：π(x) 与 Möbius–Ei 截断 π_{K,M}(x)（第 19 章式 (19.7)，含常数项 C_ν）
#
# 动画（K = 1, 6, 11, …, 496, 500）：
#   manim -pqk 素数计数公式逼近.py RiemannVisualization1800log2
# 书中静帧（只渲染一帧，输出 PNG，K 由环境变量给出）：
#   K_STILL=31  manim -s -qk 素数计数公式逼近.py Pi0Still
#   K_STILL=500 manim -s -qk 素数计数公式逼近.py Pi0Still
#
# 公式（与正文 (19.7) 一致）：
#   π_{K,M}(x) = Σ_{n≤ν(x)} μ(n)/n Ei(log x / n)
#              − 2 Σ_{k≤K} Re Σ_{n≤ν(x)} μ(n)/n Ei(ρ_k log x / n)
#              − Σ_{m≤M} Σ_{n≤ν(x)} μ(n)/n Ei(−2m log x / n)
#              − log 2 · Σ_{n≤ν(x)} μ(n)/n ,          ν(x) = ⌊log₂ x⌋
from manim import *
import numpy as np
import mpmath as mp
import math
import os
from scipy.special import expi, exp1
from sympy.functions.combinatorial.numbers import primepi
from sympy import primerange
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ch20_render import BOOK_MODE, THEME, configure_render

# ================== Manim Configuration ==================
configure_render()
config.use_latex_in_rendering = True

# Chinese captions use Pango Text; formulas need only the standard math template.
config.tex_template = TexTemplate()

# ================== Global Parameters ==================
PARAMS = {
    "MAXDISTANCE": 200,
    "TRIVIAL_ZEROS": 10,      # M：平凡零点 −2, −4, …, −20（正文 M=10）
    "NONTRIVIAL_MIN": 1,
    "NONTRIVIAL_MAX": 500,    # K 的终值（正文结束帧 K=500）
    "DRAW_INTERVAL": 5,       # K = 1, 6, 11, …, 31, …, 496，最后补 500
    "DATA_POINTS": 1800,
}

mp.mp.dps = 20

# ================== Color Definitions ==================
ORANGE_COLOR = THEME["orange"]
CYAN_COLOR = THEME["cyan"]
WHITE_COLOR = THEME["foreground"]
GREY_COLOR = THEME["grid"]
DARK_GREY_COLOR = THEME["muted"]

# ================== Core Computation Functions ==================

def mobius(n):
    """Möbius 函数 μ(n)"""
    r, p, m = 1, 2, n
    while p * p <= m:
        if m % p == 0:
            m //= p
            if m % p == 0:
                return 0
            r = -r
        p += 1
    return -r if m > 1 else r


def nu(x):
    """Möbius 截断 ν(x) = ⌊log₂ x⌋（n > ν(x) 时 x^{1/n} < 2，J(x^{1/n}) = 0）"""
    if x <= 0:
        raise ValueError("nu requires x > 0")
    # frexp avoids rounding log2(nextafter(2**n, -inf)) up to n.
    return math.frexp(float(x))[1] - 1


def mobius_terms(x):
    """[(n, μ(n)/n)]，n ≤ ν(x) 且 μ(n) ≠ 0"""
    return [(n, mobius(n) / n) for n in range(1, nu(x) + 1) if mobius(n) != 0]


def base_part(x, numbertrivials):
    """与非平凡零点无关的部分：光滑主项 + 常数项 C_ν(x) − 平凡零点项"""
    if x < 2:
        return 0.0
    log_x = math.log(x)
    terms = mobius_terms(x)
    main = sum(c * expi(log_x / n) for n, c in terms)
    const = -math.log(2) * sum(c for n, c in terms)          # C_ν(x)
    trivial = sum(c * expi(-2 * m * log_x / n)
                  for m in range(1, numbertrivials + 1) for n, c in terms)
    return main + const - trivial


def ei_complex(z):
    """复变量 Ei（主支，Im z ≠ 0）：Ei(z) = −E₁(−z) + iπ·sgn(Im z)。
    在非实参数处采用与本书一致的主支；误差须按计算范围另行复核。"""
    return -exp1(-z) + 1j * np.pi * np.sign(z.imag)


def nontrivial_part(x, gammas):
    """Σ_{γ∈gammas} 2 Re Σ_{n≤ν(x)} μ(n)/n Ei(ρ log x / n)，ρ = 1/2 + iγ（未带负号）"""
    if x < 2 or len(gammas) == 0:
        return 0.0
    log_x = math.log(x)
    rho = 0.5 + 1j * np.asarray(gammas, dtype=np.float64)
    s = 0.0
    for n, c in mobius_terms(x):
        s += c * np.sum(ei_complex(rho * log_x / n).real)
    return 2.0 * float(s)


def pi_KM(x, gammas, numbertrivials):
    """π_{K,M}(x)，K = len(gammas)，M = numbertrivials"""
    if x < 2:
        return 0.0
    return base_part(x, numbertrivials) - nontrivial_part(x, gammas)


def prime_pi_numpy(x_values):
    """Prime counting function"""
    return np.array([primepi(int(x)) for x in x_values], dtype=np.float64)


def exact_pi_points(x_min, x_max):
    """Horizontal segments and vertical prime jumps, without sampling ramps."""
    count = int(primepi(math.floor(x_min)))
    points = [(float(x_min), count)]
    for p in primerange(math.floor(x_min) + 1, math.floor(x_max) + 1):
        points.extend(((float(p), count), (float(p), count + 1)))
        count += 1
    points.append((float(x_max), count))
    return points


def k_schedule(p):
    """动画中 K 的取值：nmin, nmin+interval, …，末项补 nmax"""
    ks = list(range(p["NONTRIVIAL_MIN"], p["NONTRIVIAL_MAX"] + 1, p["DRAW_INTERVAL"]))
    if ks[-1] != p["NONTRIVIAL_MAX"]:
        ks.append(p["NONTRIVIAL_MAX"])
    return ks

# ================== Scene Builder ==================

class _Pi0Base(Scene):
    """坐标系、π(x)、图例、公式区（动画与静帧共用）"""

    def build_background(self, animate_pi=True):
        p = PARAMS
        self.maxdist = maxdist = p["MAXDISTANCE"]
        self.mindist = mindist = 2
        self.trivial = p["TRIVIAL_ZEROS"]
        # Sample both sides of changes in the finite Mobius upper limit.
        powers = [2.0**n for n in range(1, nu(maxdist) + 1)]
        extra = [v for power in powers for v in (np.nextafter(power, -np.inf), power)
                 if mindist <= v <= maxdist]
        self.x_vals = np.unique(np.concatenate((
            np.linspace(mindist, maxdist, p["DATA_POINTS"]), extra,
        )))
        self.axes = axes = Axes(
            x_range=[0, maxdist, 20], y_range=[0, 50, 10],
            x_length=11.8, y_length=4.6,
            axis_config={"color": WHITE_COLOR, "stroke_width": 1.6},
            tips=False,
        ).shift(UP * 0.75)
        grid = VGroup(*[
            Line(axes.c2p(x, 0), axes.c2p(x, 50), color=GREY_COLOR,
                 stroke_width=0.6, stroke_opacity=0.45)
            for x in range(20, maxdist + 1, 20)
        ], *[
            Line(axes.c2p(0, y), axes.c2p(maxdist, y), color=GREY_COLOR,
                 stroke_width=0.6, stroke_opacity=0.45)
            for y in range(10, 51, 10)
        ])
        labels = VGroup(*[
            MathTex(str(x), font_size=20, color=WHITE_COLOR)
                .next_to(axes.c2p(x, 0), DOWN, buff=0.12)
            for x in range(0, maxdist + 1, 20)
        ], *[
            MathTex(str(y), font_size=20, color=WHITE_COLOR)
                .next_to(axes.c2p(0, y), LEFT, buff=0.12)
            for y in range(10, 51, 10)
        ])
        x_label = MathTex("x", font_size=23, color=WHITE_COLOR)
        x_label.next_to(axes.c2p(maxdist, 0), RIGHT, buff=0.12)
        y_label = MathTex("y", font_size=23, color=WHITE_COLOR)
        y_label.next_to(axes.c2p(0, 50), UP, buff=0.12)
        self.add(grid, axes, labels, x_label, y_label)

        pi_points = [axes.c2p(x, y) for x, y in exact_pi_points(mindist, maxdist)]
        pi_curve = VMobject().set_points_as_corners(pi_points)
        pi_curve.set_color(ORANGE_COLOR).set_stroke(width=2.3)
        if animate_pi:
            self.play(Create(pi_curve), run_time=1)
        else:
            self.add(pi_curve)

        legend = VGroup(
            MathTex(r"\pi(x)", font_size=25, color=ORANGE_COLOR),
            MathTex(r"\pi_{K,M}(x)", font_size=25, color=CYAN_COLOR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.17)
        legend.move_to(axes.c2p(18, 43))
        self.add(legend)

        # Only the bridge to the book is shown; detailed definitions stay in the text.
        inversion = MathTex(
            r"\pi_0(x)=\sum_{n=1}^{\nu(x)}\frac{\mu(n)}{n}J_0(x^{1/n}),"
            r"\qquad \nu(x)=\lfloor\log_2x\rfloor",
            font_size=25, color=WHITE_COLOR,
        )
        j_formula = MathTex(
            r"J_0(x)=\operatorname{li}(x)-\sum_{\rho}\operatorname{li}(x^\rho)"
            r"-\log2+\int_x^\infty\frac{\mathrm{d}u}{u(u^2-1)\log u}",
            font_size=22, color=DARK_GREY_COLOR,
        )
        footer = VGroup(inversion, j_formula).arrange(DOWN, buff=0.18)
        if footer.width > 12.6:
            footer.scale_to_fit_width(12.6)
        footer.to_edge(DOWN, buff=0.18)
        self.add(footer)

    def counter(self, k):
        # 显示 K、M 的当前数值，与底部公式中的 K、M 对应
        k_label = Text("非平凡零点共轭对数", font_size=20, color=WHITE_COLOR)
        k_sym = MathTex(r"K =", font_size=23, color=WHITE_COLOR)
        k_value = Integer(k, font_size=23, color=WHITE_COLOR)
        m_label = Text("平凡零点数", font_size=20, color=WHITE_COLOR)
        m_sym = MathTex(r"M =", font_size=23, color=WHITE_COLOR)
        m_value = Integer(self.trivial, font_size=23, color=WHITE_COLOR)
        k_group = VGroup(k_label, k_sym, k_value).arrange(RIGHT, buff=0.12)
        m_group = VGroup(m_label, m_sym, m_value).arrange(RIGHT, buff=0.12)
        return VGroup(k_group, m_group).arrange(RIGHT, buff=0.5).to_edge(UP, buff=0.2)

    def curve(self, y_vals):
        pts = [self.axes.coords_to_point(x, y) for x, y in zip(self.x_vals, y_vals)]
        c = VMobject().set_points_as_corners(pts)
        return c.set_color(CYAN_COLOR).set_stroke(width=2.3)

# ================== Main Scene ==================

class RiemannVisualization1800log2(_Pi0Base):
    """视频 3：K 从 1 增至 500"""

    def construct(self):
        p = PARAMS
        ks = k_schedule(p)
        nmax = ks[-1]

        print("Precomputing nontrivial zeros...")
        all_gammas = [float(mp.zetazero(k).imag) for k in range(1, nmax + 1)]
        print(f"Completed: {nmax} nontrivial zeros computed\n")

        self.build_background(animate_pi=True)

        # 与 K 无关的部分只算一次；非平凡零点项逐帧累加
        base = np.array([base_part(x, self.trivial) for x in self.x_vals])
        acc = np.zeros_like(base)
        k_done = 0

        counter_group = self.counter(ks[0])
        self.add(counter_group)

        if BOOK_MODE:
            raise ValueError("Use Pi0Still for book mode")
        last_curve = None
        for k in ks:
            new_gammas = all_gammas[k_done:k]
            acc += np.array([nontrivial_part(x, new_gammas) for x in self.x_vals])
            k_done = k
            pi_curve_K = self.curve(base - acc)

            new_counter_group = self.counter(k)
            if last_curve is None:
                self.play(Create(pi_curve_K), run_time=0.6)
                counter_group.become(new_counter_group)
            else:
                self.play(
                    ReplacementTransform(last_curve, pi_curve_K),
                    ReplacementTransform(counter_group, new_counter_group),
                    run_time=0.6,
                )
                counter_group = new_counter_group
            last_curve = pi_curve_K
            print(f"K = {k}")

        self.wait(3)
        print("Rendering completed")

# ================== Still Frame (书中插图) ==================

class Pi0Still(_Pi0Base):
    """单帧：K 由环境变量 K_STILL 给出（默认 500）。用 manim -s 输出 PNG。"""

    def construct(self):
        k = int(os.environ.get("K_STILL", "500"))
        if not 1 <= k <= PARAMS["NONTRIVIAL_MAX"]:
            raise ValueError("K_STILL must be between 1 and NONTRIVIAL_MAX")
        gammas = [float(mp.zetazero(j).imag) for j in range(1, k + 1)]
        self.build_background(animate_pi=False)
        y = np.array([pi_KM(x, gammas, self.trivial) for x in self.x_vals])
        self.add(self.curve(y), self.counter(k))


if __name__ == "__main__":
    pass
