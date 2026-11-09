import Mathlib.NumberTheory.Primorial
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# 第 3 阶段 · 例题 6：Chebyshev 上界 θ(n) ≤ n log 4（本书第 6 章）

书中第 6 章用 Chebyshev 型上界控制素数计数函数的增长。其初等形式是

  θ(n) = ∑_{p ≤ n} log p ≤ n log 4。

## 本阶段的做法：部分显式引用

关键的组合估计“素数连乘积 n# = ∏_{p≤n} p ≤ 4ⁿ”直接引用 mathlib 的 `primorial_le_4_pow`；
其余分析步骤自己写：
1. 按书中定义写出 θ(n)，证明它等于 log(n#)——把对数之和变成乘积的对数；
2. 由 log 的单调性与 log(4ⁿ) = n log 4 得到上界。

显式引用的 mathlib 定理：
| 定理名 | 数学内容 |
|---|---|
| `primorial_le_4_pow` | n# ≤ 4ⁿ |
| `primorial_pos` | n# > 0 |
| `Nat.cast_prod` | 自然数乘积转为实数乘积 |
| `Real.log_prod` | 非零数乘积的对数等于对数之和 |
| `Real.log_le_log` | log 在正数上单调 |
| `Real.log_pow` | log(xⁿ) = n log x |
-/

open Finset

namespace BookExamples.Chebyshev

/-- 书中的 θ(n)：不超过 n 的素数的对数之和。 -/
noncomputable def theta (n : ℕ) : ℝ :=
  ∑ p ∈ range (n + 1) with p.Prime, Real.log p

/-- 第一步：θ(n) = log(n#)。 -/
theorem theta_eq_log_primorial (n : ℕ) : theta n = Real.log (primorial n) := by
  unfold theta primorial
  -- 乘积的对数等于对数之和；条件是每个因子非零，素数当然非零。
  rw [Nat.cast_prod, Real.log_prod]
  intro p hp
  have hp' : p.Prime := (mem_filter.mp hp).2
  exact_mod_cast hp'.ne_zero

/-- 第二步：θ(n) ≤ n log 4。 -/
theorem theta_le (n : ℕ) : theta n ≤ n * Real.log 4 := by
  -- 把 mathlib 的自然数不等式 n# ≤ 4ⁿ 转成实数不等式。
  have h : ((primorial n : ℕ) : ℝ) ≤ (4 : ℝ) ^ n := by exact_mod_cast primorial_le_4_pow n
  have hpos : (0 : ℝ) < primorial n := by exact_mod_cast primorial_pos n
  rw [theta_eq_log_primorial]
  calc Real.log (primorial n) ≤ Real.log ((4 : ℝ) ^ n) := Real.log_le_log hpos h
    _ = n * Real.log 4 := by rw [Real.log_pow]

end BookExamples.Chebyshev
