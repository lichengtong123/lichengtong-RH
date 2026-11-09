import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic

/-!
# 第 2 阶段 · 例题 3：有限 Abel 分部求和公式（本书附录 B）

书中附录 B 用 Abel 分部求和把阶梯函数的和写成积分。它的离散形式是：
设 A(0) = 0，A(k+1) = A(k) + a(k)（即 A(n) 为前 n 项部分和），则

  ∑_{k<n} a(k) b(k) = A(n) b(n) − ∑_{k<n} A(k+1) (b(k+1) − b(k))。

## 本阶段的做法

推理由自己写出：对 n 归纳。不引用 mathlib 中关于求和公式的现成结论，
只用一条最基本的运算规则——有限和拆出最后一项（`Finset.sum_range_succ`）——
以及自动化策略 `simp`、`linear_combination`。

`linear_combination ih - b n * hA n` 的含义是：目标等式减去
“归纳假设 − b(n) × 部分和递推式”后，两边只差一个多项式恒等式，由 `ring` 核验。
这一行把手算时的整理过程交给计算机检查。
-/

open Finset

namespace BookExamples.Abel

theorem abel_summation (a b A : ℕ → ℝ) (hA0 : A 0 = 0)
    (hA : ∀ k, A (k + 1) = A k + a k) (n : ℕ) :
    ∑ k ∈ range n, a k * b k =
      A n * b n - ∑ k ∈ range n, A (k + 1) * (b (k + 1) - b k) := by
  induction n with
  | zero =>
    -- n = 0：两边都是空和，A(0) = 0。
    simp [hA0]
  | succ n ih =>
    -- 把两个求和各拆出最后一项（k = n）。
    rw [sum_range_succ, sum_range_succ]
    -- 剩下的是归纳假设与部分和递推式的线性组合。
    linear_combination ih - b n * hA n

end BookExamples.Abel
