import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.Nonvanishing

/-!
# 第 1 阶段 · 例题 2：黎曼猜想的 Lean 陈述（本书第 11 章）

本例不证明新的定理，只学习怎样读一条形式化陈述，并认识 mathlib 的几条约定。

## 书中的陈述

ζ(s) 的非平凡零点，即临界带 0 < Re s < 1 内的零点，实部都等于 1/2。

## mathlib 中的陈述

mathlib 的 `RiemannHypothesis` 逐项读出是：对一切复数 s，若
1. ζ(s) = 0，
2. s 不是平凡零点 −2, −4, −6, …（不存在自然数 n 使 s = −2(n+1)），
3. s ≠ 1，

则 Re s = 1/2。

两者写法不同：书中用“在临界带内”刻画非平凡零点，mathlib 用“不是平凡零点”刻画。
它们是否等价，需要知道“临界带外只有平凡零点”，这正是第 4 阶段例题 8 要证明的结论。
在那之前，这两条陈述只是写法相近的两个命题。
-/

namespace BookExamples

/-- mathlib 的陈述按定义展开后就是上面逐项读出的内容；证明是“按定义相同”。 -/
example : RiemannHypothesis ↔
    ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * (n + 1)) → s ≠ 1 → s.re = 1 / 2 :=
  Iff.rfl

/-- 书中的陈述：临界带内的零点实部都等于 1/2。 -/
def RHBook : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → 0 < s.re → s.re < 1 → s.re = 1 / 2

/-! ## mathlib 的约定

Lean 中的函数在每一点都必须有值，因此数学上“无定义”的地方会被规定一个值。
阅读形式化陈述时，必须知道这些约定。 -/

/-- 实数除以零规定为 0。 -/
example : (1 : ℝ) / 0 = 0 := by simp

/-- 自然数减法不出现负数：2 − 3 规定为 0。 -/
example : (2 : ℕ) - 3 = 0 := by decide

/-- Γ 在极点 0 处规定为 0。 -/
example : Complex.Gamma 0 = 0 := Complex.Gamma_zero

/-- ζ 在极点 s = 1 处也有一个约定值，而且这个值不是 0。
因此 mathlib 陈述中的条件 s ≠ 1 实际上多余；写上它，使陈述不依赖于约定。 -/
example : riemannZeta 1 ≠ 0 :=
  riemannZeta_ne_zero_of_one_le_re (by simp)

end BookExamples
