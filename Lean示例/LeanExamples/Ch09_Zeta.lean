/-
# 第 9 章：$\zeta$ 的延拓、函数方程与 $\operatorname{Re} s \ge 1$ 上无零点

mathlib 中的 `riemannZeta` 已经是延拓到整个复平面的函数；书中第 9 章用两种方法构造这一延拓。
-/
import Mathlib.NumberTheory.LSeries.Nonvanishing
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues
import Mathlib.NumberTheory.Harmonic.ZetaAsymp

/-! ## 1. 函数方程

书中第 9 章写作 $\zeta(s) = 2^s \pi^{s-1} \sin(\pi s/2)\, \Gamma(1-s)\, \zeta(1-s)$。
mathlib 写的是“反方向”的等价形式：当 $s \ne 1$ 且 $s$ 不是非正整数时，
$$\zeta(1 - s) = 2\,(2\pi)^{-s}\, \Gamma(s) \cos(\pi s / 2)\, \zeta(s) .$$
两者可以互相推出；形式化时选择哪一种写法，取决于证明的方便。 -/
example (s : ℂ) (hs : ∀ n : ℕ, s ≠ -n) (hs' : s ≠ 1) :
    riemannZeta (1 - s) =
      2 * (2 * (Real.pi : ℂ)) ^ (-s) * Complex.Gamma s * Complex.cos (Real.pi * s / 2) *
        riemannZeta s :=
  riemannZeta_one_sub hs hs'

/-! ## 2. $\zeta(1 + it) \ne 0$：素数定理的关键输入

书中第 9 章证明 $\zeta$ 在直线 $\operatorname{Re} s = 1$ 上无零点，附录 F 进一步给出零点自由区。
mathlib 的版本是 $\operatorname{Re} s \ge 1$ 时 $\zeta(s) \ne 0$，**连 $s = 1$ 也包括在内**。
这不同于本书在极点处不赋有限值的约定；mathlib 在该点使用补值，见下一节。 -/
example (s : ℂ) (hs : 1 ≤ s.re) : riemannZeta s ≠ 0 :=
  riemannZeta_ne_zero_of_one_le_re hs

/-! ## 3. 一个形式化约定：mathlib 中的“$\zeta(1)$”

$\zeta$ 在 $s = 1$ 有极点，数学上 $\zeta(1)$ 没有定义。但 Lean 中的函数必须在每一点都有值，
固定版本的 mathlib 根据其函数定义，在该点给出补值：
$$\texttt{riemannZeta 1} = \frac{\gamma - \log(4\pi)}{2} \approx -0.977 .$$
这个补值不是 Laurent 展开中的常数项；通常的有限部分
$\lim_{s\to1}(\zeta(s)-1/(s-1))=\gamma$，两者不能混同。
有趣的是，这个数恰好等于 $\lambda_1 - 1$，其中 $\lambda_1 = 1 + \gamma/2 - \tfrac12\log(4\pi)$
是 Li 判据的第一个系数（学习笔记第 10 篇）。
**教训**：读形式化陈述时，必须知道这些约定；上一节的“$\operatorname{Re} s \ge 1$ 时 $\zeta(s) \ne 0$”
在 $s = 1$ 处说的其实是这个约定值不为零，而不是关于极点的任何断言。 -/
example : riemannZeta 1 =
    ((Real.eulerMascheroniConstant : ℂ) - Complex.log (4 * (Real.pi : ℂ))) / 2 :=
  riemannZeta_one

/-! ## 4. 两个特殊值：$\zeta(2) = \pi^2/6$ 与 $\zeta(-1) = -1/12$

前者见学习笔记第 18 篇（用留数证明），后者见学习笔记第 11 篇（延拓后的值）。
mathlib 用 Bernoulli 数给出 $\zeta$ 在负整数处的值：$\zeta(-k) = -B'_{k+1}/(k+1)$，
其中 `bernoulli'` 是 $B_1 = +\tfrac12$ 约定下的 Bernoulli 数。
取 $k = 1$，$B'_2 = \tfrac16$，即得 $\zeta(-1) = -\tfrac1{12}$——这一步计算由本仓库补写，Lean 检查。 -/
example : riemannZeta 2 = (Real.pi : ℂ) ^ 2 / 6 :=
  riemannZeta_two

theorem riemannZeta_neg_one : riemannZeta (-1) = -1 / 12 := by
  have h := riemannZeta_neg_nat_eq_bernoulli' 1
  rw [Nat.cast_one] at h
  rw [h]
  norm_num [bernoulli'_two]
