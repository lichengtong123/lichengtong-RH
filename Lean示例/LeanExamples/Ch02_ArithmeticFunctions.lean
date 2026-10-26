/-
# 第 2 章：算术函数与 Abel 求和

本文件把书中第 2 章（及附录 A、B）的几条基本恒等式，与 mathlib 中已经形式化的定理对照。
每条 `example` 先用 Lean 写出书中的陈述，再用 mathlib 的定理完成证明；
Lean 接受这个文件，就说明“书中的陈述”与“mathlib 已证明的定理”在形式上一致。
-/
import Mathlib.NumberTheory.VonMangoldt
import Mathlib.NumberTheory.AbelSummation

open ArithmeticFunction Finset MeasureTheory
open scoped ArithmeticFunction

/-! ## 1. von Mangoldt 函数：$\sum_{d \mid n} \Lambda(d) = \log n$

书中第 2 章用这一恒等式联系 $\Lambda$ 与 $\log$，它是 $\psi(x)$ 与 $-\zeta'/\zeta$ 相对应的出发点。
Lean 写法：`n.divisors` 是 $n$ 的全部正因子构成的有限集，`Λ` 是 von Mangoldt 函数。
注意 mathlib 中 $n = 0$ 的情形也成立：`Nat.divisors 0` 是空集，左边为 $0$，而 `Real.log 0 = 0`
（这是 mathlib 的约定，数学上 $\log 0$ 无定义）。 -/
example (n : ℕ) : ∑ i ∈ n.divisors, Λ i = Real.log n :=
  vonMangoldt_sum

/-! ## 2. Möbius 函数：$\sum_{d \mid n} \mu(d) = [n = 1]$

书中写作对每个 $n$ 的求和恒等式。mathlib 用 Dirichlet 卷积的语言写成一个等式：
$\mu * \zeta = 1$，其中 `ζ` 是取值恒为 $1$ 的算术函数（不是 Riemann zeta 函数），
`1` 是卷积的单位元（在 $n = 1$ 处为 $1$，其余为 $0$）。两种写法内容相同。 -/
example : (μ * ζ : ArithmeticFunction ℤ) = 1 :=
  coe_moebius_mul_coe_zeta

/-! ## 3. Möbius 反演公式（附录 A）

若对一切 $n > 0$ 有 $\sum_{d \mid n} f(d) = g(n)$，则 $f(n) = \sum_{d \mid n} \mu(d)\, g(n/d)$，反之亦然。
mathlib 用 `divisorsAntidiagonal`（满足 $ab = n$ 的有序对 $(a, b)$）来写 $\sum_{d \mid n}\mu(d) g(n/d)$。 -/
example (f g : ℕ → ℤ) :
    (∀ n > 0, ∑ i ∈ n.divisors, f i = g n) ↔
      ∀ n > 0, ∑ x ∈ n.divisorsAntidiagonal, μ x.fst • g x.snd = f n :=
  sum_eq_iff_sum_smul_moebius_eq

/-! ## 4. Abel 求和公式（附录 B）

书中附录 B 的 Abel 求和：对 $b \ge 0$，
$$\sum_{0 \le k \le b} f(k)\, c_k = f(b) \sum_{0 \le k \le b} c_k - \int_0^b f'(t) \sum_{0 \le k \le t} c_k \, dt .$$
Lean 的版本把书中“$f$ 连续可微”的条件拆成两条：$f$ 在 $[0, b]$ 上处处可微，
且导数在 $[0, b]$ 上可积。形式化迫使每个条件都写清楚。 -/
example (c : ℕ → ℝ) (f : ℝ → ℝ) {b : ℝ} (hb : 0 ≤ b)
    (hf_diff : ∀ t ∈ Set.Icc 0 b, DifferentiableAt ℝ f t)
    (hf_int : IntegrableOn (deriv f) (Set.Icc 0 b)) :
    ∑ k ∈ Icc 0 ⌊b⌋₊, f k * c k =
      f b * (∑ k ∈ Icc 0 ⌊b⌋₊, c k) - ∫ t in Set.Ioc 0 b, deriv f t * ∑ k ∈ Icc 0 ⌊t⌋₊, c k :=
  sum_mul_eq_sub_integral_mul c hb hf_diff hf_int
