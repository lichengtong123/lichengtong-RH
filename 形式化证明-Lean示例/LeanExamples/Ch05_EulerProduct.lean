/-
# 第 5 章：Euler 乘积

书中第 5 章：当 $\operatorname{Re} s > 1$ 时，
$$\zeta(s) = \prod_p \frac{1}{1 - p^{-s}} .$$
-/
import Mathlib.NumberTheory.EulerProduct.DirichletLSeries

/-! Lean 写法说明：
* `riemannZeta` 是 mathlib 中的 Riemann zeta 函数，定义在整个复平面上（见第 9 章示例中关于 $s = 1$ 的说明）；
* `Nat.Primes` 是全体素数构成的类型，`∏'` 是无穷乘积（`tprod`）；
* `(p : ℂ) ^ (-s)` 即 $p^{-s}$，$(\cdot)^{-1}$ 即倒数。
条件 `1 < s.re` 对应书中的 $\operatorname{Re} s > 1$；去掉它，Lean 就不接受证明。 -/
example (s : ℂ) (hs : 1 < s.re) :
    ∏' p : Nat.Primes, (1 - (p : ℂ) ^ (-s))⁻¹ = riemannZeta s :=
  riemannZeta_eulerProduct_tprod hs
