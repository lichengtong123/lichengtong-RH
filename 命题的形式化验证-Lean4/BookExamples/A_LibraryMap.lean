import Mathlib.NumberTheory.VonMangoldt
import Mathlib.NumberTheory.AbelSummation
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries
import Mathlib.Analysis.SpecialFunctions.Gamma.Beta
import Mathlib.NumberTheory.LSeries.Nonvanishing
import Mathlib.NumberTheory.LSeries.HurwitzZetaValues
import Mathlib.NumberTheory.Harmonic.ZetaAsymp

/-!
# 附表：本书其他命题在 mathlib 中的对应

本文件不属于四个阶段。它把书中若干结论与 mathlib 中已有的定理逐条对照：
每条先用 Lean 写出书中的陈述，再直接引用 mathlib 的定理完成证明。
Lean 接受本文件，说明这些陈述在 mathlib 中已有完整的形式化证明。

阅读时请留意每条陈述中的条件，以及 mathlib 的约定与书中写法的差别。

每条的写法都是

  example (参数与条件) : 书中的陈述 :=
    mathlib 定理名 (所需的条件)

`:=` 后面不写 `by`，直接给出 mathlib 中的一条定理，表示“这正是该定理”。
Lean 检查这条定理的结论与 `:` 后写出的陈述是否一致；一致才接受。
想看某条 mathlib 定理的原始陈述，可在 VS Code 中按住 Ctrl（macOS 为 Cmd）点击定理名跳转，
或在 mathlib 文档中按名称搜索。
-/

open ArithmeticFunction Finset MeasureTheory
open scoped ArithmeticFunction

namespace BookExamples.LibraryMap

/-! ## 第 2 章、附录 A：Möbius 函数与 Möbius 反演 -/

/-- ∑_{d∣n} μ(d) = [n = 1]。mathlib 用 Dirichlet 卷积写成 μ * ζ = 1，
其中 `ζ` 是恒等于 1 的算术函数（不是 Riemann ζ 函数），`1` 是卷积的单位元。 -/
example : (μ * ζ : ArithmeticFunction ℤ) = 1 :=
  coe_moebius_mul_coe_zeta

/-- Möbius 反演：若对一切 n > 0 有 ∑_{d∣n} f(d) = g(n)，则 f(n) = ∑_{d∣n} μ(d) g(n/d)，反之亦然。
`divisorsAntidiagonal` 是满足 ab = n 的有序对 (a, b)。 -/
example (f g : ℕ → ℤ) :
    (∀ n > 0, ∑ i ∈ n.divisors, f i = g n) ↔
      ∀ n > 0, ∑ x ∈ n.divisorsAntidiagonal, μ x.fst • g x.snd = f n :=
  sum_eq_iff_sum_smul_moebius_eq

/-! ## 附录 B：Abel 求和公式（积分形式）

例题 3 是有限形式；书中附录 B 的积分形式在 mathlib 中也已有。书中“f 连续可微”的条件，
在 Lean 中拆成两条：f 在 [0, b] 上处处可微，且导数在 [0, b] 上可积。 -/

example (c : ℕ → ℝ) (f : ℝ → ℝ) {b : ℝ} (hb : 0 ≤ b)
    (hf_diff : ∀ t ∈ Set.Icc 0 b, DifferentiableAt ℝ f t)
    (hf_int : IntegrableOn (deriv f) (Set.Icc 0 b)) :
    ∑ k ∈ Icc 0 ⌊b⌋₊, f k * c k =
      f b * (∑ k ∈ Icc 0 ⌊b⌋₊, c k) - ∫ t in Set.Ioc 0 b, deriv f t * ∑ k ∈ Icc 0 ⌊t⌋₊, c k :=
  sum_mul_eq_sub_integral_mul c hb hf_diff hf_int

/-! ## 第 5 章：Euler 乘积

Re s > 1 时 ζ(s) = ∏_p (1 − p^{−s})^{−1}。条件 `1 < s.re` 不能去掉。 -/

example (s : ℂ) (hs : 1 < s.re) :
    ∏' p : Nat.Primes, (1 - (p : ℂ) ^ (-s))⁻¹ = riemannZeta s :=
  riemannZeta_eulerProduct_tprod hs

/-! ## 第 7 章：Γ 函数的倍元公式与余元公式

两条公式在 mathlib 中都对一切复数陈述，没有排除极点：mathlib 规定 Γ 在极点处取 0，
除以 0 也规定为 0，于是公式在极点处按约定成立。书中则把极点排除在外。 -/

/-- Legendre 倍元公式：Γ(s) Γ(s + ½) = 2^{1−2s} √π Γ(2s)。 -/
example (s : ℂ) :
    Complex.Gamma s * Complex.Gamma (s + 1 / 2) =
      Complex.Gamma (2 * s) * (2 : ℂ) ^ (1 - 2 * s) * ↑(Real.sqrt Real.pi) :=
  Complex.Gamma_mul_Gamma_add_half s

/-- 余元公式：Γ(z) Γ(1 − z) = π / sin(πz)。 -/
example (z : ℂ) :
    Complex.Gamma z * Complex.Gamma (1 - z) = ↑Real.pi / Complex.sin (↑Real.pi * z) :=
  Complex.Gamma_mul_Gamma_one_sub z

/-! ## 第 9 章：ζ 的函数方程与 Re s ≥ 1 上无零点 -/

/-- 函数方程。书中写作 ζ(s) = 2^s π^{s−1} sin(πs/2) Γ(1−s) ζ(1−s)；
mathlib 写的是等价的另一方向，并要求 s ≠ 1、s 不是非正整数。例题 8 用到了它。 -/
example (s : ℂ) (hs : ∀ n : ℕ, s ≠ -n) (hs' : s ≠ 1) :
    riemannZeta (1 - s) =
      2 * (2 * (Real.pi : ℂ)) ^ (-s) * Complex.Gamma s * Complex.cos (Real.pi * s / 2) *
        riemannZeta s :=
  riemannZeta_one_sub hs hs'

/-- Re s ≥ 1 时 ζ(s) ≠ 0（书中第 9 章、附录 F）。mathlib 的版本连 s = 1 也包括在内，
说的是该点的约定值不为零，见下一条。 -/
example (s : ℂ) (hs : 1 ≤ s.re) : riemannZeta s ≠ 0 :=
  riemannZeta_ne_zero_of_one_le_re hs

/-- mathlib 给 ζ(1) 规定的约定值：(γ − log 4π)/2 ≈ −0.977。
它不是 Laurent 展开的常数项（后者是 γ）。数学上 ζ(1) 没有定义。 -/
example : riemannZeta 1 =
    ((Real.eulerMascheroniConstant : ℂ) - Complex.log (4 * (Real.pi : ℂ))) / 2 :=
  riemannZeta_one

/-! ## 两个特殊值：ζ(2) = π²/6 与 ζ(−1) = −1/12 -/

example : riemannZeta 2 = (Real.pi : ℂ) ^ 2 / 6 :=
  riemannZeta_two

/-- mathlib 用 Bernoulli 数给出负整数处的值 ζ(−k) = −B'_{k+1}/(k+1)；
取 k = 1、B'_2 = 1/6，即得 ζ(−1) = −1/12。这一步计算由本仓库补写。 -/
theorem riemannZeta_neg_one : riemannZeta (-1) = -1 / 12 := by
  have h := riemannZeta_neg_nat_eq_bernoulli' 1
  rw [Nat.cast_one] at h
  rw [h]
  norm_num [bernoulli'_two]

end BookExamples.LibraryMap
