import Mathlib.NumberTheory.PrimeCounting
import Mathlib.Tactic.NormNum.Prime

/-!
# 第 1 阶段 · 例题 1：π(100) = 25（本书第 1、2 章）

书中给出素数计数函数 π(x) 的数值表，其中 π(100) = 25。本例用三种方式让 Lean 核验这一事实，
借此认识形式化陈述的写法，以及“计算也能作为证明”时应当信任什么。

## 形式化陈述

mathlib 中 π(n) 写作 `Nat.primeCounting n`，定义为不超过 n 的素数个数，与书中一致。
下面的定理

  theorem primeCounting_100_kernel : Nat.primeCounting 100 = 25 := by
    decide +kernel

逐段读作：定理名为 `primeCounting_100_kernel`；冒号后是陈述 π(100) = 25；
`:= by` 之后是证明，这里只有一行策略 `decide +kernel`。

## 三种核验方式

1. `decide +kernel`：由 Lean 的内核逐个检验 0 到 100 是否为素数并计数，得到 25。
   内核是 Lean 中很小的一段程序，负责最终检查一切证明，是最受信任的部分。
   内核做的每一步计算都按 Lean 的逻辑规则检查，计算本身就构成证明。
2. `native_decide`：先把同一个判定程序编译成机器码，在计算机上直接运行，得到“真”。
   速度快得多，但运行过程没有经过内核检查，Lean 只是承认这个运行结果。
   因此需要额外信任“编译器与运行时没有错误”。
3. `norm_num`：对单个数给出可由内核检验的素性证明（例如 97 是素数），不必逐个计数。

## 怎样看出差别：`#print axioms`

文件末尾的 `#print axioms 定理名` 列出这条定理最终依赖的全部公理。它沿着证明用到的定义和引理
一直追到底，所以即使证明只是计算，也会列出 mathlib 中那些定义和引理所依赖的公理。
在 VS Code 中把光标放在这一行，InfoView 的 Messages 中显示输出；GitHub 自动检查的构建记录中也有。

前一种证明的输出是

  'BookExamples.PrimeCount.primeCounting_100_kernel' depends on axioms: [propext, Classical.choice, Quot.sound]

这三条是 Lean 的标准公理，几乎所有基于 mathlib 的证明都依赖它们：

* `propext`（命题外延性）：两个命题若互相蕴含（P ↔ Q），就是同一个命题（P = Q）。
* `Quot.sound`（商的可靠性）：在某个等价关系下等价的两个元素，它们的等价类相等。
  构造商集（例如模 n 的剩余类）时要用到它；Lean 还由它推出：在每一点取值相同的两个函数相等。
* `Classical.choice`（选择公理）：已知一个类型非空，就可以从中取出一个元素。
  由它可以推出排中律（P 或非 P），也就是允许使用反证法。

它们大致对应普通数学默认使用的公理（含选择公理）。只依赖这三条，说明证明没有额外的假设。

`native_decide` 的输出多出一条：

  depends on axioms: [propext, Classical.choice, Lean.ofReduceBool, Quot.sound]

`Lean.ofReduceBool` 的意思是：编译执行这个判定程序得到 true，就承认它确实为 true。
内核没有检查这一计算，所以 Lean 把这一步作为公理记下来。它记录的是一个额外的信任前提：
编译器、运行时以及程序中用来加速的底层实现都没有错误。
结论相同的两个证明，信任范围不同，`#print axioms` 把这一差别如实列了出来。
收尾一节（S5_Checking.lean）将用这一点说明怎样检查证明的可信范围。
-/

namespace BookExamples.PrimeCount

/-- 方法一：内核计算。`decide` 对可以有限检验的命题直接计算真假；
`+kernel` 指定由内核完成这一计算，因此每一步都经过内核检查。 -/
theorem primeCounting_100_kernel : Nat.primeCounting 100 = 25 := by
  decide +kernel

/-- 方法二：编译执行。陈述与方法一完全相同，只是计算由编译后的程序完成。 -/
theorem primeCounting_100_native : Nat.primeCounting 100 = 25 := by
  native_decide

/-- 方法三：单个数的素性证明。`norm_num` 是数值计算策略，
它为“97 是素数”生成一份可由内核检验的证明，而不是逐个计数。 -/
theorem prime_97 : Nat.Prime 97 := by
  norm_num

/-- 方法三：合数同样可以判定。`¬` 读作“非”，`¬ Nat.Prime 91` 即“91 不是素数”（91 = 7 × 13）。 -/
theorem not_prime_91 : ¬ Nat.Prime 91 := by
  norm_num

-- 查看三种证明各自依赖的公理。把光标放在下面某一行上，InfoView 的 Messages 显示输出；
-- 输出的含义见文件开头的说明。
-- 第一行：只有三条标准公理。
#print axioms primeCounting_100_kernel
-- 第二行：多出 Lean.ofReduceBool。
#print axioms primeCounting_100_native
-- 第三行：与第一行相同，只有三条标准公理。
#print axioms prime_97

end BookExamples.PrimeCount
