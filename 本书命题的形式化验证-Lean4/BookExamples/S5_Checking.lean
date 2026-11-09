import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.Nonvanishing
import BookExamples.S1a_PrimeCount
import BookExamples.S4a_Xi

/-!
# 收尾：怎样检查一个形式化证明

“某定理已经形式化证明”这类说法，至少要检查三件事：

1. **证明是否完整**：有没有用 `sorry` 跳过步骤。含 `sorry` 的文件也能通过编译，
   只是会给出警告。
2. **依赖哪些公理**：用 `#print axioms 定理名` 查看。标准公理之外若出现别的条目，
   就要弄清它是什么。例如有人声明了“公理 RH 成立”，由它推出的一切结论都会被 Lean 接受，
   而 `#print axioms` 会把这条公理列出来。
3. **陈述是否忠实于原题**：Lean 只检查“由假设推出结论”是否正确，
   不检查假设能否同时成立，也不检查陈述是不是想要的那个命题。这一条只能由人判断。

下面用三个例子演示。
-/

open Complex

namespace BookExamples.Checking

/-! ## 例一：信任范围不同的两个证明

例题 1 中 π(100) = 25 的两种证明结论相同，但依赖的公理不同。比较下面两行输出：
`native_decide` 的证明多出 `Lean.ofReduceBool`，表示信任了编译执行的结果。 -/

#print axioms BookExamples.PrimeCount.primeCounting_100_kernel
#print axioms BookExamples.PrimeCount.primeCounting_100_native

-- 作为对照：例题 7 的 ξ 函数对称性只依赖 Lean 的标准公理。
#print axioms BookExamples.Xi.xi_one_sub

/-! ## 例二：被 Lean 接受、却与黎曼猜想无关的陈述

下面的定理说：若 Re s > 1 且 ζ(s) = 0，则 Re s = 1/2。Lean 接受它，证明只有一行。
但它与黎曼猜想无关：两个假设不可能同时成立（Re s ≥ 1 时 ζ(s) ≠ 0），
从矛盾的假设可以推出任何结论。 -/

theorem vacuous (s : ℂ) (h1 : 1 < s.re) (h2 : riemannZeta s = 0) : s.re = 1 / 2 :=
  absurd h2 (riemannZeta_ne_zero_of_one_le_re h1.le)

/-! ## 例三：名字像函数方程、实际几乎平凡的定理

函数方程的一种推导最后得到对称表示
F(s) = −1/s − 1/(1−s) + A(s) + A(1−s)，其中 A 是 [1,∞) 上的一个含参量积分。
下面的定理证明 F(1−s) = F(s)，名字也叫“函数方程”，Lean 同样接受。
但这里的 A 是**任意**复函数，证明只是把四个加数换了顺序。
真正的难点——A 等于那个积分、F 等于完备化的 ζ 函数——一样都没有证明。
看到“形式化证明了函数方程”时，要读陈述本身：A 是什么，F 与 ζ 有什么关系。

mathlib 中完整的函数方程是 `completedRiemannZeta₀_one_sub`，例题 7 用到了它。 -/

/-- 对任意函数 A 定义的对称表示。 -/
noncomputable def model (A : ℂ → ℂ) (s : ℂ) : ℂ :=
  -1 / s - 1 / (1 - s) + A s + A (1 - s)

/-- “函数方程”：对任意 A 都成立，因此与 ζ 无关。 -/
theorem functional_equation (A : ℂ → ℂ) (s : ℂ) : model A (1 - s) = model A s := by
  have h : (1 : ℂ) - (1 - s) = s := by ring
  unfold model
  rw [h]
  ring

end BookExamples.Checking
