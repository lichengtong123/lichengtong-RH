/-
# 第 6 章：Chebyshev 型上界 $\theta(n) \le n \log 4$

书中第 6 章用 Chebyshev 上界控制素数计数函数的增长。这里给出它的一个初等形式：
$$\theta(n) = \sum_{p \le n} \log p \le n \log 4 .$$
mathlib 已证明“素数连乘积” $n\# = \prod_{p \le n} p \le 4^n$；下面的证明是本仓库补写的，
只用了几行：对两边取对数即可。
-/
import Mathlib.NumberTheory.Primorial
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-! ## mathlib 的定理：$n\# \le 4^n$

`primorial n` 即 $\prod_{p \le n,\ p \text{ 素}} p$。 -/
example (n : ℕ) : primorial n ≤ 4 ^ n :=
  primorial_le_4_pow n

/-! ## 本仓库补写：$\theta(n) = \log(n\#) \le n \log 4$

由 $\log$ 的单调性与 $\log(4^n) = n \log 4$ 得到。证明中每一步都由 Lean 检查：
先把自然数不等式转成实数不等式（`exact_mod_cast`），再用 $\log$ 单调（需要 $n\# > 0$），
最后用 $\log(x^n) = n\log x$。 -/
theorem theta_le_mul_log_four (n : ℕ) : Real.log (primorial n) ≤ n * Real.log 4 := by
  have h : ((primorial n : ℕ) : ℝ) ≤ (4 : ℝ) ^ n := by exact_mod_cast primorial_le_4_pow n
  have hpos : (0 : ℝ) < primorial n := by exact_mod_cast primorial_pos n
  calc Real.log (primorial n) ≤ Real.log ((4 : ℝ) ^ n) := Real.log_le_log hpos h
    _ = n * Real.log 4 := by rw [Real.log_pow]
