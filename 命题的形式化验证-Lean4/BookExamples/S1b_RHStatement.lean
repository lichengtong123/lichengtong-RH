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

下面第一个 `example` 把它写成 Lean 代码：

  ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * (n + 1)) → s ≠ 1 → s.re = 1 / 2

逐个符号对照：`∀ s : ℂ,` 是“对一切复数 s”；`riemannZeta s` 是 ζ(s)；
`→` 是“若……则……”，几个 `→` 连写时，前面的都是条件，最后一项是结论；
`¬∃ n : ℕ, …` 是“不存在自然数 n 使……”，自然数 n 从 0 开始，所以 −2(n+1) 取遍 −2, −4, −6, …；
`s.re` 是 s 的实部。

两者写法不同：书中用“在临界带内”刻画非平凡零点，mathlib 用“不是平凡零点”刻画。
它们是否等价，需要知道“临界带外只有平凡零点”，这正是第 4 阶段例题 8 要证明的结论。
在那之前，这两条陈述只是写法相近的两个命题。
-/

namespace BookExamples

/-- mathlib 的陈述按定义展开后就是上面逐项读出的内容。
`example` 是不起名字的定理；`↔` 读作“当且仅当”。证明 `Iff.rfl` 的意思是：
两边按定义展开后完全相同，所以 ↔ 成立，不需要任何推理。
Lean 接受这一行，就确认了上面的逐项解读与 mathlib 的定义一致。 -/
example : RiemannHypothesis ↔
    ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * (n + 1)) → s ≠ 1 → s.re = 1 / 2 :=
  Iff.rfl

/-- 书中的陈述：临界带内的零点实部都等于 1/2。
`def` 给一个对象起名字；`RHBook : Prop` 表示它是一个命题（Prop），
`:=` 后面是这个命题的内容。定义一个命题并不等于证明它：黎曼猜想至今未被证明。 -/
def RHBook : Prop :=
  ∀ s : ℂ, riemannZeta s = 0 → 0 < s.re → s.re < 1 → s.re = 1 / 2

/-! ## mathlib 的约定

Lean 中的函数在每一点都必须有值，因此数学上“无定义”的地方会被规定一个值。
阅读形式化陈述时，必须知道这些约定。下面四个 `example` 各演示一条。 -/

/-- 实数除以零规定为 0。`(1 : ℝ)` 指定这里的 1 是实数。证明交给化简策略 `simp`。 -/
example : (1 : ℝ) / 0 = 0 := by simp

/-- 自然数减法不出现负数：2 − 3 规定为 0。`(2 : ℕ)` 指定 2 是自然数；
若写成 `(2 : ℤ) - 3`，结果就是整数 −1。`decide` 直接计算判定。 -/
example : (2 : ℕ) - 3 = 0 := by decide

/-- Γ 在极点 0 处规定为 0。这里不写 `by`，直接给出 mathlib 中的定理
`Complex.Gamma_zero`，它的内容恰好就是这个等式。 -/
example : Complex.Gamma 0 = 0 := Complex.Gamma_zero

/-- ζ 在极点 s = 1 处也有一个约定值，而且这个值不是 0。
因此 mathlib 陈述中的条件 s ≠ 1 实际上多余；写上它，使陈述不依赖于约定。

证明直接引用 mathlib 定理 `riemannZeta_ne_zero_of_one_le_re`：
“若 1 ≤ Re s，则 ζ(s) ≠ 0”。把它用于 s = 1，需要提供条件 1 ≤ Re 1，
括号中的 `by simp` 证明这个条件。mathlib 的这条定理连 s = 1 也包括在内，
说的正是约定值不为零。 -/
example : riemannZeta 1 ≠ 0 :=
  riemannZeta_ne_zero_of_one_le_re (by simp)

end BookExamples
