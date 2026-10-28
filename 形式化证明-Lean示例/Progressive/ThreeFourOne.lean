import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.Tactic

/-!
# 3–4–1 三角不等式：逐步证明示例

目标是展示实际推导，不调用已经证明整个不等式的定理。
基础输入：余弦倍角公式、实数平方非负、实数的代数运算。
`ring` 只核验多项式恒等变形，不承担三角公式或不等式的证明。

书中使用位置：10-19 版第 9.6.2 节及附录 F.1。
本例仅核验三角恒等式与非负性，不包括其后 ζ 的级数与无零点论证。
入口：https://github.com/lichengtong123/lichengtong-RH/tree/main/形式化证明-Lean示例
同目录 ThreeFourOne-逐步说明.pdf 提供每一步的详细解释。
-/

namespace Progressive

-- 第一步：利用倍角公式，把含有 cos(2θ) 的表达式化为多项式。
theorem three_four_one_identity (θ : ℝ) :
    3 + 4 * Real.cos θ + Real.cos (2 * θ) = 2 * (1 + Real.cos θ) ^ 2 := by
  -- 用 cos(2θ) = 2 cos²θ − 1 替换左端的倍角项。
  rw [Real.cos_two_mul]
  -- 展开两边并核对每个多项式系数，得到所需恒等式。
  ring

-- 第二步：从刚刚证明的恒等式推出非负性。
theorem three_four_one_nonnegative (θ : ℝ) :
    0 ≤ 3 + 4 * Real.cos θ + Real.cos (2 * θ) := by
  -- 将目标左边的三角表达式换成平方的两倍。
  rw [three_four_one_identity]
  -- 先单独记录平方非负，不把整个不等式交给自动搜索。
  have hSquare : 0 ≤ (1 + Real.cos θ) ^ 2 := sq_nonneg _
  -- 正数 2 与非负数的乘积仍非负，证明结束。
  exact mul_nonneg (by norm_num) hSquare

end Progressive
