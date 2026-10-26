/-
# 第 11 章：黎曼猜想的形式化陈述
-/
import Mathlib.NumberTheory.LSeries.RiemannZeta

/-! ## mathlib 中的 RH

mathlib 给出了 RH 的一个形式化陈述（定义名 `RiemannHypothesis`，文档注释写道：
“构造这个类型的一个项，值一百万美元”）。逐项读出它的意思：
对一切复数 $s$，若
1. $\zeta(s) = 0$，
2. $s$ 不是平凡零点 $-2, -4, -6, \dots$（即不存在自然数 $n$ 使 $s = -2(n+1)$），
3. $s \ne 1$，

则 $\operatorname{Re} s = 1/2$。

下面这条 `example` 只是把定义展开，证明是 `Iff.rfl`（“两边按定义相同”）。
它说明：mathlib 中的 RH 正是书中第 11 章的陈述。条件 3 在数学上多余（$\zeta(1)$ 本无定义），
在 mathlib 中也多余（约定值 $\zeta(1) \ne 0$，见第 9 章示例），但写上它使陈述不依赖于约定。
**这一陈述目前没有人能在 Lean 中证明，也没有人能否证。** -/
example : RiemannHypothesis ↔
    ∀ s : ℂ, riemannZeta s = 0 → (¬∃ n : ℕ, s = -2 * (n + 1)) → s ≠ 1 → s.re = 1 / 2 :=
  Iff.rfl

/-! ## 平凡零点确实是零点

条件 2 排除的点确实是 $\zeta$ 的零点（书中第 9 章由函数方程得到）。 -/
example (n : ℕ) : riemannZeta (-2 * (n + 1)) = 0 :=
  riemannZeta_neg_two_mul_nat_add_one n
