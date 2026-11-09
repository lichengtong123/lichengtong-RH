import Mathlib.NumberTheory.PrimeCounting
import Mathlib.Tactic.NormNum.Prime

/-!
# 第 1 阶段 · 例题 1：π(100) = 25（本书第 1、2 章）

书中给出素数计数函数 π(x) 的数值表，其中 π(100) = 25。本例用三种方式让 Lean 核验这一事实，
借此认识形式化陈述的写法，以及“计算也能作为证明”时应当信任什么。

## 形式化陈述

mathlib 中 π(n) 写作 `Nat.primeCounting n`，定义为不超过 n 的素数个数，与书中一致。

## 三种核验方式

1. `decide +kernel`：由 Lean 的内核逐个检验 0 到 100 是否为素数并计数。
   内核是 Lean 中最小、最受信任的部分。
2. `native_decide`：先把判定程序编译成机器码再运行，速度快得多，
   但需要额外信任“编译器与运行时没有错误”。
3. `norm_num`：对单个数给出可检验的素性证明（例如 97 是素数），不必逐个计数。

## 怎样看出差别

文件末尾的 `#print axioms` 列出每个定理依赖的公理。前一种只依赖 Lean 的标准公理；
`native_decide` 的结果还多出一条 `Lean.ofReduceBool`，表示信任了编译执行的结果。
在构建记录中可以看到这些输出。收尾一节将用这一点说明怎样检查证明的可信范围。
-/

namespace BookExamples.PrimeCount

/-- 方法一：内核计算。 -/
theorem primeCounting_100_kernel : Nat.primeCounting 100 = 25 := by
  decide +kernel

/-- 方法二：编译执行。 -/
theorem primeCounting_100_native : Nat.primeCounting 100 = 25 := by
  native_decide

/-- 方法三：单个数的素性证明。`norm_num` 给出可由内核检验的证明。 -/
theorem prime_97 : Nat.Prime 97 := by
  norm_num

/-- 方法三：合数同样可以判定。 -/
theorem not_prime_91 : ¬ Nat.Prime 91 := by
  norm_num

-- 查看三种证明各自依赖的公理（输出见构建记录）。
#print axioms primeCounting_100_kernel
#print axioms primeCounting_100_native
#print axioms prime_97

end BookExamples.PrimeCount
