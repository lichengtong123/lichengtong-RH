# Filename: RiemannVisualization_LaTeX.py
# Stable version using xelatex with corrected LaTeX rendering and axis ticks
#manim -pqk RiemannVisualization_LaTeX1800log2.py   RiemannVisualization1800log2
from manim import *
import numpy as np
import mpmath as mp
import math
from sympy import mobius
from scipy.special import expi
from sympy.functions.combinatorial.numbers import primepi

# ================== Manim Configuration ==================
config.pixel_height = 1440
config.pixel_width = 2560
config.frame_rate = 30
config.use_latex_in_rendering = True

# 全局使用 XeLaTeX 并启用中文支持
config.tex_template = TexTemplate(
    tex_compiler="xelatex",
    output_format=".pdf"
)

config.tex_template.add_to_preamble(r"""
\usepackage[UTF8]{ctex}
%\setCJKmainfont{PingFang SC}           % macOS 自带字体（根据需要取消注释）
% 或使用更现代的开源字体（需先安装）：
%\setCJKmainfont{Source Han Sans SC}
""")

# ================== Global Parameters ==================
PARAMS = {
    "MAXDISTANCE": 200,
    "TRIVIAL_ZEROS": 20,
    "NONTRIVIAL_MIN": 1,
    "NONTRIVIAL_MAX": 1000,
    "DRAW_INTERVAL": 5,
    "DATA_POINTS": 1800,
}

# ================== Color Definitions ==================
ORANGE_COLOR = "#FFA500"
CYAN_COLOR   = "#00FFFF"
WHITE_COLOR  = "#FFFFFF"
GREY_COLOR   = "#888888"
DARK_GREY_COLOR = "#444444"
ORANGE_RED   = "#FF4500"
LIGHT_GREY   = "#AAAAAA"

# ================== Core Computation Functions ==================

def Riemann_main(x, numbersums):
    """Riemann main term"""
    if x <= 1:
        return 0.0
    log_x = math.log(x)
    main_sum = 0.0
    for n in range(1, numbersums + 1):
        mu_n = mobius(n)
        if mu_n == 0:
            continue
        arg = log_x / n
        ei_val = expi(arg)
        main_sum += (mu_n / n) * ei_val
    return main_sum

def zeta_nontrivial_correction(x, numbersums, gammas):
    """Nontrivial zeros correction"""
    if x <= 1 or not gammas:
        return 0.0
    log_x = math.log(x)
    corr_sum = 0.0
    mp.dps = 20 
    for n in range(1, numbersums + 1):
        mu_n = mobius(n)
        if mu_n == 0:
            continue
        n_term = 0.0
        for gamma in gammas:
            complex_arg = (0.5 + 1j * gamma) * log_x / n
            ei_complex = mp.ei(complex_arg)
            real_part = float(mp.re(ei_complex))
            n_term += (1 / n) * 2 * real_part
        corr_sum += -mu_n * n_term
    return corr_sum

def trivial_zeros_correction(x, numbersums, numbertrivials):
    """Trivial zeros correction"""
    if x <= 1 or numbertrivials == 0:
        return 0.0
    log_x = math.log(x)
    corr_sum = 0.0
    for n in range(1, numbersums + 1):
        mu_n = mobius(n)
        if mu_n == 0:
            continue
        n_term = 0.0
        for m in range(1, numbertrivials + 1):
            arg = (-2 * m / n) * log_x
            ei_val = expi(arg)
            n_term += (1 / n) * ei_val
        corr_sum += -mu_n * n_term
    return corr_sum

def pi_0(x, numbersums, gammas, numbertrivials):
    """Complete approximation function"""
    if x <= 1:
        return 0.0
    main_term = Riemann_main(x, numbersums)
    non_trivial_corr = zeta_nontrivial_correction(x, numbersums, gammas)
    trivial_corr = trivial_zeros_correction(x, numbersums, numbertrivials)
    return main_term + non_trivial_corr + trivial_corr

def prime_pi_numpy(x_values):
    """Prime counting function"""
    return np.array([primepi(int(x)) for x in x_values], dtype=np.float64)

# ================== Main Scene ==================

class RiemannVisualization1800log2(Scene):
    """Riemann Hypothesis Visualization - Stable xelatex Version"""
    
    def construct(self):
        print("\n" + "="*70)
        print("  Riemann Hypothesis Visualization - Stable Version")
        print("="*70)
        
        p = PARAMS
        maxdist = p["MAXDISTANCE"]
        trivial = p["TRIVIAL_ZEROS"]
        nmin = p["NONTRIVIAL_MIN"]
        nmax = p["NONTRIVIAL_MAX"]
        interval = p["DRAW_INTERVAL"]
        
        mindist = 2
        numbersums = int(math.ceil(math.log2(maxdist)))
        x_vals = np.linspace(mindist, maxdist, p["DATA_POINTS"])
        
        print("Precomputing nontrivial zeros...")
        all_gammas = [float(mp.zetazero(k).imag) for k in range(1, nmax + 1)]
        print(f"Completed: {nmax} nontrivial zeros computed\n")
        
        axes = Axes(
            x_range=[mindist, maxdist, 10],
            y_range=[0, 50, 5],
            x_length=14,
            y_length=8,
            axis_config={"color": WHITE_COLOR, "stroke_width": 2.5},
            tips=False,
        )
        
        # 坐标轴名称
        x_label = MathTex(r"x", font_size=20, color=WHITE_COLOR)
        x_label.to_corner(DOWN + RIGHT, buff=0.4)
        
        y_label = MathTex(r"y", font_size=20, color=WHITE_COLOR)
        y_label.to_corner(UP + LEFT, buff=0.4)
        
        # 网格线
        grid_lines = VGroup(*[
            Line(axes.coords_to_point(x, 0), axes.coords_to_point(x, 50),
                 color=GREY_COLOR, stroke_width=0.8, stroke_opacity=0.4)
            for x in np.arange(mindist, maxdist + 1, 10)
        ] + [
            Line(axes.coords_to_point(mindist, y), axes.coords_to_point(maxdist, y),
                 color=GREY_COLOR, stroke_width=0.8, stroke_opacity=0.4)
            for y in np.arange(0, 51, 5)
        ])
        
        # ── x 轴与 y 轴刻度数值标注 ──
        x_tick_values = np.arange(0, maxdist + 10, 20)
        x_labels = VGroup(*[
            Text(str(int(x)), font_size=12, color=WHITE_COLOR)
                .next_to(axes.coords_to_point(x, 0), UP, buff=0.2)
            for x in x_tick_values
            if x >= mindist - 5
        ])
        
        y_tick_values = np.arange(0, 55, 10)
        y_labels = VGroup(*[
            Text(str(int(y)), font_size=12, color=WHITE_COLOR)
                .next_to(axes.coords_to_point(mindist, y), RIGHT, buff=0.2)
            for y in y_tick_values
        ])
        
        pi_vals = prime_pi_numpy(x_vals)
        pi_points = [axes.coords_to_point(x, y) for x, y in zip(x_vals, pi_vals)]
        pi_curve = VMobject().set_points_as_corners(pi_points)
        pi_curve.set_color(ORANGE_COLOR).set_stroke(width=1)
        
        self.add(grid_lines, axes, x_label, y_label, x_labels, y_labels)
        self.play(Create(pi_curve), run_time=1)
        
        # 图例
        legend_pi = MathTex(r"\pi(x) ", font_size=16, color=ORANGE_COLOR)
        legend_pi.to_corner(UP + LEFT, buff=1)
        
        legend_pi_line = Line(
            legend_pi.get_right() + RIGHT*0.1,
            legend_pi.get_right() + RIGHT*0.5,
            color=ORANGE_COLOR, stroke_width=1
        )
        
        legend_pi0 = MathTex(r"\pi_0(x) ", font_size=16, color=CYAN_COLOR)
        legend_pi0.next_to(legend_pi, DOWN, buff=0.3, aligned_edge=LEFT)
        
        legend_pi0_line = Line(
            legend_pi0.get_right() + RIGHT*0.1,
            legend_pi0.get_right() + RIGHT*0.5,
            color=CYAN_COLOR, stroke_width=1
        )
        
        self.add(legend_pi, legend_pi_line, legend_pi0, legend_pi0_line)
        
        # 计数器
        counter_label = Text("非平凡零点:", font_size=16, color=GREEN_E)
        counter_value = Integer(nmin, font_size=16, color=GREEN_E)
        divider = Text("  平凡零点 ", font_size=16, color=GREEN_E)
        trivial_value = Integer(trivial, font_size=16, color=GREEN_E)
        
        counter_group = VGroup(
            counter_label, counter_value, divider, trivial_value
        ).arrange(RIGHT, buff=0.2).to_corner(UP + LEFT, buff=0.6)
        self.add(counter_group)
        
        # 公式区域
        formula_1 = MathTex(
            r"\pi(x) = \sum_{\substack{p\,\text{ 素数} \\ p \leq x}} 1 = "
            r"\sum_{k=1}^{\infty} \frac{\mu(k)}{k} J(x^{1/k})",
            font_size=15, color=ORANGE_RED
        ).set_stroke(width=0.8).to_corner(UP + RIGHT, buff=1.8).shift(DOWN * 0.8)
        
        formula_2 = MathTex(
            r"J(x) = \text{Li}(x) - \sum_{\rho} \text{Li}(x^{\rho}) - \log 2 + \int_{x}^{\infty} \frac{dt}{t(t^2 - 1)\log t}",
            font_size=15, color=DARK_GREY_COLOR
        ).set_stroke(width=0.8).arrange(RIGHT, buff=0.2).to_corner(UP + RIGHT, buff=3).shift(DOWN * 0.8)
        
        formula_3 = MathTex(
            r"Ei(x) = \displaystyle \text{PV}\int_{-\infty}^{x} {\frac{e^{t}}{t}}\ d t = \gamma + \log\lvert x \rvert + \sum_{k=1}^{\infty} \frac{x^k}{k \cdot k!}",
            font_size=15, color=DARK_GREY_COLOR
        ).set_stroke(width=0.8).next_to(formula_2, DOWN, buff=0.3, aligned_edge=LEFT)     
        
        formula_4 = MathTex(
            r"\mu(n) = \displaystyle \begin{cases} 1 & \text{if} \quad n=1 \\ (-1)^r & if \quad \displaystyle n=\prod_{k=1}^r p_k^{r_k}\quad \forall r_k =1\\ 0 & \text{if} \quad \displaystyle n=\prod_{k=1}^r p_k^{r_k}\quad \exists r_k  \geq 2 \end{cases}",
            font_size=15, color=DARK_GREY_COLOR
        ).set_stroke(width=0.8).next_to(formula_3, DOWN, buff=0.3, aligned_edge=LEFT)
        
        formula_5 = MathTex(
            r"\displaystyle \pi_0(x) \approx \sum_{n=1}^{N} \frac{\mu(n)}{n} Ei\left(\frac{\log x}{n}\right) - 2\sum_{\rho} \operatorname{Re} \left[ \sum_{n=1}^{N} \frac{\mu(n)}{n} Ei\left(\frac{\rho \log x}{n}\right) \right] - \sum_{m=1}^{M} \sum_{n=1}^{N} \frac{\mu(n)}{n} Ei\left(\frac{-2m \log x}{n}\right) ",
            font_size=15, color=CYAN_COLOR,
        ).set_stroke(width=0.8).arrange(RIGHT, buff=0.2).to_corner(DOWN + LEFT, buff=1.5).shift(DOWN * 0.9)
        
        self.add(formula_1, formula_2, formula_3, formula_4, formula_5)
        
        # 动画循环
        last_curve = None
        for n_zeros in range(nmin, nmax + 1, interval):
            current_gammas = all_gammas[:n_zeros]
            
            pi0_vals = np.array([
                pi_0(x, numbersums, current_gammas, trivial)
                for x in x_vals
            ], dtype=np.float64)
            
            pi0_points = [axes.coords_to_point(x, y) for x, y in zip(x_vals, pi0_vals)]
            pi0_curve = VMobject().set_points_as_corners(pi0_points)
            pi0_curve.set_color(CYAN_COLOR).set_stroke(width=1)
            
            if last_curve is None:
                self.play(Create(pi0_curve), run_time=0.6)
            else:
                self.play(ReplacementTransform(last_curve, pi0_curve), run_time=0.4)
            
            new_counter_value = Integer(n_zeros, font_size=18, color=GREEN_E)
            new_counter_group = VGroup(
                counter_label, new_counter_value, divider, trivial_value
            ).arrange(RIGHT, buff=0.2).to_corner(UP + LEFT, buff=0.5)
            
            self.play(ReplacementTransform(counter_group, new_counter_group), run_time=0.2)
            counter_group = new_counter_group
            last_curve = pi0_curve
        
        self.wait(3)
        
        print("="*70)
        print("Rendering completed")
        print("="*70 + "\n")

if __name__ == "__main__":
    pass