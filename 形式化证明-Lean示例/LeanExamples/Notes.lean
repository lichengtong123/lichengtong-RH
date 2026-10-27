/-
# 附录 F 与学习笔记中的几个小命题

以下证明由本仓库补写，不是 mathlib 中的现成定理。它们都很短，用来展示一个完整的 Lean 证明长什么样。
-/
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic
import Mathlib.NumberTheory.LucasLehmer

/-! ## 1. 附录 F 与学习笔记第 20 篇：$3 + 4\cos\theta + \cos 2\theta \ge 0$

零点自由区证明的出发点。先证恒等式 $3 + 4\cos\theta + \cos 2\theta = 2(1+\cos\theta)^2$：
用倍角公式 $\cos 2\theta = 2\cos^2\theta - 1$ 改写后，`ring` 自动完成代数化简。
非负性随之由“平方的倍数非负”得到，`positivity` 自动完成。 -/
theorem three_four_one (θ : ℝ) :
    3 + 4 * Real.cos θ + Real.cos (2 * θ) = 2 * (1 + Real.cos θ) ^ 2 := by
  rw [Real.cos_two_mul]
  ring

theorem three_four_one_nonneg (θ : ℝ) : 0 ≤ 3 + 4 * Real.cos θ + Real.cos (2 * θ) := by
  rw [three_four_one]
  positivity

/-! ## 2. 学习笔记第 11 篇：平移稳定的求和法不能给 $1 + 1 + 1 + \cdots$ 赋值

设 $V$ 给每个数列 $a$ 赋一个实数，并且“平移稳定”：$V(a) = a_0 + V(a_1, a_2, \dots)$。
对常数列 $1, 1, 1, \dots$ 用这条性质，得 $V = 1 + V$，矛盾。
Lean 中数列写作函数 `ℕ → ℝ`，`fun _ => 1` 是常数列，`fun n => a (n + 1)` 是去掉首项后的数列。
结论 `False` 表示“这样的 $V$ 不存在”。$\zeta$ 正则化给出 $1 + 1 + \cdots = -\tfrac12$，
正说明它不是平移稳定的。 -/
theorem no_shift_stable_sum (V : (ℕ → ℝ) → ℝ)
    (hV : ∀ a : ℕ → ℝ, V a = a 0 + V (fun n => a (n + 1))) : False := by
  have h := hV (fun _ => 1)
  linarith

/-! ## 3. 学习笔记第 16 篇：$2^{61} - 1$ 是素数

第 16 篇用 Lucas 判据和一个素性证书说明“验证比寻找容易”。这里换用 mathlib 中专为
Mersenne 数 $M_p = 2^p - 1$ 设计的 Lucas–Lehmer 判据：$M_p$ 为素数，只要数列
$s_0 = 4,\ s_{i+1} = s_i^2 - 2$ 在模 $M_p$ 下满足 $s_{p-2} \equiv 0$。
`norm_num` 实际算出这 59 步模运算并核验结果；整个证明由 Lean 内核检查。 -/
example : mersenne 61 = 2305843009213693951 := by
  norm_num [mersenne]

example : (mersenne 61).Prime :=
  lucas_lehmer_sufficiency _ (by simp) (by norm_num)
