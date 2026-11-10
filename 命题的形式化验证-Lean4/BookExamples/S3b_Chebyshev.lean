import Mathlib.NumberTheory.Primorial
import Mathlib.Analysis.SpecialFunctions.Log.Basic

/-!
# 第 3 阶段 · 例题 6：Chebyshev 上界 θ(n) ≤ n log 4（本书第 2 章）

书中第 2 章“Chebyshev 的初等估计”一节证明了 Chebyshev 型上界 θ(x) < (log 4) x，
第 15 章等处还要引用它。这里对整数 n 证明稍弱的非严格形式

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

/-- 书中的 θ(n)：不超过 n 的素数的对数之和。
`range (n + 1)` 是 {0, 1, …, n}，`with p.Prime` 只保留其中的素数，所以这就是 ∑_{p ≤ n} log p。
`noncomputable` 表示这个定义只用于证明，不能直接运行求值（实数的对数无法精确计算）。
`(p : ℝ)` 的类型转换由 Lean 自动补上：p 是自然数，取对数前先看作实数。 -/
noncomputable def theta (n : ℕ) : ℝ :=
  ∑ p ∈ range (n + 1) with p.Prime, Real.log p

/-- 第一步：θ(n) = log(n#)。 -/
theorem theta_eq_log_primorial (n : ℕ) : theta n = Real.log (primorial n) := by
  -- 展开 θ 与素数连乘积 n# 的定义，目标变为 ∑_{p ≤ n} log p = log(∏_{p ≤ n} p)。
  unfold theta primorial
  -- `Nat.cast_prod`：自然数的乘积先算再看作实数，等于先看作实数再相乘。
  -- `Real.log_prod`：乘积的对数等于对数之和，条件是每个因子非零。
  -- 改写后等式本身已经成立，只剩下 `Real.log_prod` 的条件“每个因子非零”成为新目标。
  rw [Nat.cast_prod, Real.log_prod]
  -- 新目标：对集合中的每个 p，(p : ℝ) ≠ 0。引入 p 与“p 属于该集合”的条件 hp。
  intro p hp
  -- `mem_filter.mp hp` 把“p 属于筛选后的集合”拆成“p ∈ range (n+1)”与“p 是素数”两部分，
  -- `.2` 取第二部分。
  have hp' : p.Prime := (mem_filter.mp hp).2
  -- 素数不为零（`hp'.ne_zero`），这是自然数的结论；`exact_mod_cast` 把它转成实数的结论。
  exact_mod_cast hp'.ne_zero

/-- 第二步：θ(n) ≤ n log 4。 -/
theorem theta_le (n : ℕ) : theta n ≤ n * Real.log 4 := by
  -- 把 mathlib 的自然数不等式 n# ≤ 4ⁿ 转成实数不等式，记作 h。
  have h : ((primorial n : ℕ) : ℝ) ≤ (4 : ℝ) ^ n := by exact_mod_cast primorial_le_4_pow n
  -- 取对数需要 n# > 0，同样由自然数的结论转成实数，记作 hpos。
  have hpos : (0 : ℝ) < primorial n := by exact_mod_cast primorial_pos n
  -- 用第一步把 θ(n) 换成 log(n#)。目标变为 log(n#) ≤ n log 4。
  rw [theta_eq_log_primorial]
  -- `calc` 写出一串不等式，每一步在 `:=` 后给出理由：
  --   log(n#) ≤ log(4ⁿ)：log 在正数上单调（`Real.log_le_log`，需要 hpos 与 h）；
  --   log(4ⁿ) = n log 4：`Real.log_pow`。
  -- 两步连起来就是目标。
  calc Real.log (primorial n) ≤ Real.log ((4 : ℝ) ^ n) := Real.log_le_log hpos h
    _ = n * Real.log 4 := by rw [Real.log_pow]

end BookExamples.Chebyshev
