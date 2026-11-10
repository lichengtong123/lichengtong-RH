import Mathlib.Algebra.BigOperators.Intervals
import Mathlib.Tactic

/-!
# 第 2 阶段 · 例题 3：有限 Abel 分部求和公式（本书附录 B）

书中附录 B 用 Abel 分部求和把阶梯函数的和写成积分。它的离散形式是：
设 A(0) = 0，A(k+1) = A(k) + a(k)（即 A(n) 为前 n 项部分和），则

  ∑_{k<n} a(k) b(k) = A(n) b(n) − ∑_{k<n} A(k+1) (b(k+1) − b(k))。

## 形式化陈述

  theorem abel_summation (a b A : ℕ → ℝ) (hA0 : A 0 = 0)
      (hA : ∀ k, A (k + 1) = A k + a k) (n : ℕ) : …

* `(a b A : ℕ → ℝ)`：a、b、A 都是从自然数到实数的函数，即实数列。
* `(hA0 : A 0 = 0)`、`(hA : ∀ k, A (k + 1) = A k + a k)`：两个前提，分别命名为 hA0、hA，
  证明中用这两个名字引用它们。
* `∑ k ∈ range n, a k * b k`：`range n` 是集合 {0, 1, …, n−1}，所以这就是 ∑_{k<n} a(k) b(k)。

## 本阶段的做法

推理由自己写出：对 n 归纳。不引用 mathlib 中关于求和公式的现成结论，
只用一条最基本的运算规则——有限和拆出最后一项（`Finset.sum_range_succ`）：

  ∑_{k<n+1} f(k) = ∑_{k<n} f(k) + f(n)，

以及自动化策略 `simp`、`linear_combination`。

## 归纳步的手算

设 n 时公式成立（归纳假设 ih）：∑_{k<n} a(k)b(k) = A(n)b(n) − ∑_{k<n} A(k+1)(b(k+1) − b(k))。
要证 n+1 时成立。两边的和各拆出最后一项 k = n 后，目标变为

  ∑_{k<n} a(k)b(k) + a(n)b(n)
    = A(n+1)b(n+1) − ( ∑_{k<n} A(k+1)(b(k+1) − b(k)) + A(n+1)(b(n+1) − b(n)) )。

用 ih 替换左边的和，再用 A(n+1) = A(n) + a(n)，两边展开后相同。
`linear_combination ih - b n * hA n` 把这段手算交给计算机检查：
它验证“目标等式”减去“ih − b(n) × (hA n)”后，两边只差一个多项式恒等式，由 `ring` 核验。
-/

open Finset

namespace BookExamples.Abel

theorem abel_summation (a b A : ℕ → ℝ) (hA0 : A 0 = 0)
    (hA : ∀ k, A (k + 1) = A k + a k) (n : ℕ) :
    ∑ k ∈ range n, a k * b k =
      A n * b n - ∑ k ∈ range n, A (k + 1) * (b (k + 1) - b k) := by
  -- 对 n 归纳。下面分两种情形：`zero` 是 n = 0，`succ n ih` 是由 n 推到 n + 1，
  -- 其中 ih 是 n 时的结论（归纳假设）。
  induction n with
  | zero =>
    -- n = 0：两边的和都是空和（等于 0），目标化为 0 = A(0) b(0) − 0。
    -- `simp [hA0]` 化简空和，并用 hA0 把 A 0 换成 0。
    simp [hA0]
  | succ n ih =>
    -- 此时目标是 n + 1 时的等式。`sum_range_succ` 把 ∑_{k<n+1} 写成 ∑_{k<n} 加上 k = n 的一项；
    -- 目标中有两个和，所以改写两次。
    rw [sum_range_succ, sum_range_succ]
    -- 剩下的是归纳假设 ih 与部分和递推式 hA n（即 A(n+1) = A(n) + a(n)）的线性组合，
    -- 手算过程见文件开头。
    linear_combination ih - b n * hA n

end BookExamples.Abel
