import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# 第 2 阶段 · 例题 4：3–4–1 不等式（本书第 9 章、附录 F）

书中证明 ζ 在直线 Re s = 1 上没有零点时，关键一步是初等不等式

  3 + 4 cos θ + cos 2θ = 2 (1 + cos θ)² ≥ 0。

本例只核验这一三角不等式，不包括其后关于 ζ 的级数与无零点论证。

## 本阶段的做法

推理由自己写出，分两步，与手算相同：
1. 用二倍角公式 cos 2θ = 2cos²θ − 1 代入，左边化为 2 + 4cos θ + 2cos²θ = 2(1 + cos θ)²；
2. 平方非负，乘以正数 2 仍非负。

引用的只是最基本的规则：二倍角公式 `Real.cos_two_mul`，以及“平方非负”`sq_nonneg`、
“非负数之积非负”`mul_nonneg`。`ring` 只核验多项式恒等变形。

在 Lean 中，`Real.cos θ` 是实数 θ 的余弦，`x ^ 2` 是 x 的平方，`*` 是乘号，不能省略。
-/

namespace BookExamples.ThreeFourOne

/-- 第一步：用 cos 2θ = 2cos²θ − 1 化为多项式恒等式。 -/
theorem identity (θ : ℝ) :
    3 + 4 * Real.cos θ + Real.cos (2 * θ) = 2 * (1 + Real.cos θ) ^ 2 := by
  -- `Real.cos_two_mul` 是等式 cos(2x) = 2cos²x − 1。`rw` 用它把目标中的 cos(2θ) 换成右边。
  -- 此后目标变为 3 + 4cos θ + (2cos²θ − 1) = 2(1 + cos θ)²。
  rw [Real.cos_two_mul]
  -- 把 cos θ 看作一个未知数，这是多项式恒等式，`ring` 展开两边比较。
  ring

/-- 第二步：由恒等式与平方非负推出不等式。 -/
theorem nonneg (θ : ℝ) :
    0 ≤ 3 + 4 * Real.cos θ + Real.cos (2 * θ) := by
  -- 用第一步证明的等式 `identity` 改写，目标变为 0 ≤ 2 * (1 + cos θ)²。
  rw [identity]
  -- `have` 先证明一个中间结论，命名为 hSquare：(1 + cos θ)² ≥ 0。
  -- `sq_nonneg x` 是 mathlib 中的“x² ≥ 0”；下划线 `_` 让 Lean 自己找出 x = 1 + cos θ。
  have hSquare : 0 ≤ (1 + Real.cos θ) ^ 2 := sq_nonneg _
  -- `mul_nonneg` 说：若 0 ≤ a 且 0 ≤ b，则 0 ≤ a * b。这里 a = 2，b = (1 + cos θ)²。
  -- 第一个条件 0 ≤ 2 由 `by norm_num` 计算得到，第二个条件就是 hSquare。
  -- `exact` 表示这一项正好证明了目标，证明结束。
  exact mul_nonneg (by norm_num) hSquare

end BookExamples.ThreeFourOne
