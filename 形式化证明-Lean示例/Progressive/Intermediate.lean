/-
The divisor-sum proof below is adapted from ArithmeticFunction.vonMangoldt_sum
in Mathlib/NumberTheory/VonMangoldt.lean, copyright (c) 2022 Bhavik Mehta.
This file is distributed under Apache-2.0; see Apache-2.0.txt in this directory.
The adaptation expands the proof into an annotated learning example.
-/
import Mathlib.NumberTheory.VonMangoldt
import Mathlib.Tactic

/-!
# 中等示例：von Mangoldt 恒等式与 Möbius 反演

实际证明分为三段：按素数幂与互素乘积归纳证明因子和恒等式；
将它写成卷积；再用 Möbius 函数与常数算术函数的卷积逆关系反演。
不调用 vonMangoldt_sum 或已经算好 Λ 的 Möbius 公式。

基础输入：整数的素因子分解归纳、素数幂的因子枚举、互素数的
素数幂因子分离、对数乘法公式、一般 Dirichlet 卷积及其 Möbius 逆。
这些一般结果不是本例声称重新证明的内容。
-/

open ArithmeticFunction Finset
open scoped ArithmeticFunction

namespace Progressive

-- 第一段：证明所有正整数的因子和恒等式。
theorem mangoldt_divisor_sum (n : ℕ) :
    ∑ d ∈ n.divisors, Λ d = Real.log n := by
  -- 一般素因子分解归纳：处理 0、1，素数幂，以及互素乘积。
  -- 库的 log(0) 和 divisors(0) 约定使 n=0 也成立；数学用途是 n≥1。
  refine Nat.recOnPrimeCoprime ?_ ?_ ?_ n
  -- 基础情形由 Λ(1)=0、空因子集及 log(1)=0 等定义化简得到。
  · simp
  -- 素数幂情形：p^k 的因子为 1,p,...,p^k。
  · intro p k hp
    -- 枚举因子，把 log(p^k) 改写成 k log p，并单独取出 Λ(1)。
    rw [Nat.sum_divisors_prime_pow hp, Nat.cast_pow, Real.log_pow,
      Finset.sum_range_succ', Nat.pow_zero, vonMangoldt_apply_one]
    -- 每个正次幂 p^(j+1) 的 Λ 值都是 log p；有限常数和为 k log p。
    simp [vonMangoldt_apply_pow (Nat.succ_ne_zero _), vonMangoldt_apply_prime hp]
  -- 互素乘积情形：已知 a、b 的结论，证明 ab 的结论。
  · intro a b haPositive hbPositive hab ha hb
    -- 按 Λ 的定义，只保留因子中的素数幂；其他因子贡献为零。
    simp only [vonMangoldt_apply, ← Finset.sum_filter] at ha hb ⊢
    -- a、b 互素，所以 ab 的素数幂因子来自 a 或 b，且两类不交。
    rw [Nat.mul_divisors_filter_prime_pow hab, Finset.filter_union,
      Finset.sum_union (Nat.disjoint_divisors_filter_isPrimePow hab)]
    -- 对两个互不相交的因子集合分别使用归纳假设。
    rw [ha, hb, Nat.cast_mul]
    -- a、b 均为正，故可用 log(ab)=log a+log b；最后取等式的反向。
    exact (Real.log_mul
      (Nat.cast_ne_zero.mpr (pos_of_gt haPositive).ne')
      (Nat.cast_ne_zero.mpr (pos_of_gt hbPositive).ne')).symm

-- 第二段：把已经证明的因子和改写成 Dirichlet 卷积。
-- 这里的 ζ 是恒等于 1（在正整数上）的算术函数，不是复变 ζ 函数。
theorem mangoldt_convolution : Λ * (ζ : ArithmeticFunction ℝ) = ArithmeticFunction.log := by
  -- 两个算术函数相等，只需在每个自然数 n 处取值相等。
  ext n
  -- 与 ζ 卷积就是因子求和；展开后正是第一段的命题。
  rw [ArithmeticFunction.coe_mul_zeta_apply]
  exact mangoldt_divisor_sum n

-- 第三段：在卷积等式右边乘 μ，实际完成反演，而不引用 Λ 的反演结果。
theorem mangoldt_mobius_convolution :
    (μ : ArithmeticFunction ℝ) * ArithmeticFunction.log = Λ := by
  calc
    -- 先交换两个因子的位置，以便随后使用结合律。
    (μ : ArithmeticFunction ℝ) * ArithmeticFunction.log =
        ArithmeticFunction.log * μ := mul_comm _ _
    -- 将第二段得到的 log=Λ*ζ 代入。
    _ = (Λ * ζ) * μ := by rw [mangoldt_convolution]
    -- 卷积结合律允许先计算 ζ*μ。
    _ = Λ * (ζ * μ) := mul_assoc _ _ _
    -- 使用一般 Möbius 逆关系 ζ*μ=1；不是调用本例的目标定理。
    _ = Λ * 1 := by rw [ArithmeticFunction.coe_zeta_mul_coe_moebius]
    -- 卷积单位元消去，得到 Λ。
    _ = Λ := mul_one _

-- 最后把函数等式展开为有限和，便于和通常的数学写法对照。
theorem mangoldt_mobius_sum (n : ℕ) :
    ∑ p ∈ n.divisorsAntidiagonal, (μ p.1 : ℝ) * Real.log p.2 = Λ n := by
  -- 对第三段的算术函数等式，在同一个 n 处取值。
  have h := congrArg (fun f : ArithmeticFunction ℝ => f n) mangoldt_mobius_convolution
  -- 展开卷积定义；有序因子对 (d,e) 满足 de=n，故这就是 Σ μ(d)log(n/d)。
  simpa only [ArithmeticFunction.mul_apply, ArithmeticFunction.intCoe_apply,
    ArithmeticFunction.log_apply] using h

end Progressive
