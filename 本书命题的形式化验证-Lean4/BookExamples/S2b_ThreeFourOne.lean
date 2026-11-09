import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# 第 2 阶段 · 例题 4：3–4–1 不等式（本书第 9 章、附录 F）

书中证明 ζ 在直线 Re s = 1 上没有零点时，关键一步是初等不等式

  3 + 4 cos θ + cos 2θ = 2 (1 + cos θ)² ≥ 0。

本例只核验这一三角不等式，不包括其后关于 ζ 的级数与无零点论证。

## 本阶段的做法

推理由自己写出：先用二倍角公式化为多项式恒等式，再由平方非负得到结论。
引用的只是最基本的规则：二倍角公式 `Real.cos_two_mul`，以及“平方非负”`sq_nonneg`、
“非负数之积非负”`mul_nonneg`。`ring` 只核验多项式恒等变形。
-/

namespace BookExamples.ThreeFourOne

/-- 第一步：用 cos 2θ = 2cos²θ − 1 化为多项式恒等式。 -/
theorem identity (θ : ℝ) :
    3 + 4 * Real.cos θ + Real.cos (2 * θ) = 2 * (1 + Real.cos θ) ^ 2 := by
  rw [Real.cos_two_mul]
  ring

/-- 第二步：由恒等式与平方非负推出不等式。 -/
theorem nonneg (θ : ℝ) :
    0 ≤ 3 + 4 * Real.cos θ + Real.cos (2 * θ) := by
  rw [identity]
  have hSquare : 0 ≤ (1 + Real.cos θ) ^ 2 := sq_nonneg _
  exact mul_nonneg (by norm_num) hSquare

end BookExamples.ThreeFourOne
