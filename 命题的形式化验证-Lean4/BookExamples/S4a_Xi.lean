import Mathlib.NumberTheory.LSeries.RiemannZeta

/-!
# 第 4 阶段 · 例题 7：ξ 函数（本书第 10 章）

本例的推导全部由 mathlib 中已有的定理拼接而成，自己只写定义与代数整理。

## 书中的结论

书中定义 ξ(s) = ½ s(s−1) π^{−s/2} Γ(s/2) ζ(s)，并证明：
1. ξ 是整函数；
2. ξ(1−s) = ξ(s)；
3. ξ(0) = ξ(1) = ½；
4. 在临界带 0 < Re s < 1 内，ξ 的零点恰为 ζ 的零点。

## mathlib 中的对应对象

* `completedRiemannZeta s`，记作 Λ(s) = π^{−s/2} Γ(s/2) ζ(s)，即书中的完备化 ζ 函数；
* `completedRiemannZeta₀ s`，记作 Λ₀(s) = Λ(s) + 1/s + 1/(1−s)，即消去两个极点后的整函数；
* `Gammaℝ s` = π^{−s/2} Γ(s/2)。

## 为什么不直接照书中公式定义

Lean 中的函数在每一点都必须有值。mathlib 在极点 s = 0、1 处给 Λ 规定了约定值，
所以若定义 ξ(s) = ½ s(s−1) Λ(s)，在 s = 0、1 处得到的是 0 乘约定值，
既不是 ½，也无法证明整函数性。书中靠“s(s−1) 消去 Λ 的两个极点”得到整函数；
在 Lean 中，这一步要改写成用 Λ₀ 定义：

  ξ(s) = ½ (s(s−1) Λ₀(s) + 1)。

定理 `xi_eq` 证明：在 s ≠ 0、1 处它与书中公式一致。

## 本例显式引用的 mathlib 定理

| 定理名 | 数学内容 |
|---|---|
| `differentiable_completedZeta₀` | Λ₀ 是整函数 |
| `completedRiemannZeta₀_one_sub` | Λ₀(1−s) = Λ₀(s)（函数方程） |
| `completedRiemannZeta_eq` | Λ(s) = Λ₀(s) − 1/s − 1/(1−s) |
| `riemannZeta_def_of_ne_zero` | s ≠ 0 时 ζ(s) = Λ(s) / Gammaℝ(s) |
| `Complex.Gammaℝ_ne_zero_of_re_pos` | Re s > 0 时 Gammaℝ(s) ≠ 0 |

其余步骤由自动化策略完成：`fun_prop`（可微性）、`ring`、`field_simp`（代数整理）、
`simp`（化简）。
-/

open Complex

namespace BookExamples.Xi

/-- 书中的 ξ 函数，用 Λ₀ 写成在整个复平面都有定义的形式。 -/
noncomputable def xi (s : ℂ) : ℂ :=
  (s * (s - 1) * completedRiemannZeta₀ s + 1) / 2

/-- 与书中定义一致：s ≠ 0、1 时，ξ(s) = ½ s(s−1) Λ(s)。 -/
theorem xi_eq (s : ℂ) (h0 : s ≠ 0) (h1 : s ≠ 1) :
    xi s = s * (s - 1) * completedRiemannZeta s / 2 := by
  have h1' : (1 : ℂ) - s ≠ 0 := sub_ne_zero.mpr (Ne.symm h1)
  -- 用 Λ = Λ₀ − 1/s − 1/(1−s) 改写，剩下的是有理式的恒等变形
  rw [completedRiemannZeta_eq]
  unfold xi
  field_simp
  ring

/-- 结论 1：ξ 是整函数（在整个复平面上复可微）。 -/
theorem xi_differentiable : Differentiable ℂ xi := by
  have h : Differentiable ℂ completedRiemannZeta₀ := differentiable_completedZeta₀
  unfold xi
  fun_prop

/-- 结论 2：ξ(1−s) = ξ(s)，由 Λ₀ 的函数方程直接得到。 -/
theorem xi_one_sub (s : ℂ) : xi (1 - s) = xi s := by
  unfold xi
  rw [completedRiemannZeta₀_one_sub]
  ring

/-- 结论 3：ξ(0) = ½。 -/
theorem xi_zero : xi 0 = 1 / 2 := by
  simp [xi]

/-- 结论 3：ξ(1) = ½。 -/
theorem xi_one : xi 1 = 1 / 2 := by
  simp [xi]

/-- 右半平面 Re s > 0（s ≠ 1）上，ξ(s) = ½ s(s−1) Gammaℝ(s) ζ(s)，即书中的原始公式。 -/
theorem xi_eq_zeta (s : ℂ) (hs : 0 < s.re) (h1 : s ≠ 1) :
    xi s = s * (s - 1) * Gammaℝ s * riemannZeta s / 2 := by
  have h0 : s ≠ 0 := by
    rintro rfl
    simp at hs
  have hG : Gammaℝ s ≠ 0 := Gammaℝ_ne_zero_of_re_pos hs
  -- 由 ζ = Λ / Gammaℝ 反解出 Λ = Gammaℝ · ζ
  have hΛ : completedRiemannZeta s = Gammaℝ s * riemannZeta s := by
    rw [riemannZeta_def_of_ne_zero h0]
    field_simp
  rw [xi_eq s h0 h1, hΛ]
  ring

/-- 结论 4：在临界带 0 < Re s < 1 内，ξ(s) = 0 当且仅当 ζ(s) = 0。 -/
theorem xi_eq_zero_iff (s : ℂ) (hs0 : 0 < s.re) (hs1 : s.re < 1) :
    xi s = 0 ↔ riemannZeta s = 0 := by
  have h0 : s ≠ 0 := by
    rintro rfl
    simp at hs0
  have h1 : s ≠ 1 := by
    rintro rfl
    simp at hs1
  have h1' : s - 1 ≠ 0 := sub_ne_zero.mpr h1
  have hG : Gammaℝ s ≠ 0 := Gammaℝ_ne_zero_of_re_pos hs0
  rw [xi_eq_zeta s hs0 h1]
  constructor
  · intro h
    simpa [h0, h1', hG] using h
  · intro h
    simp [h]

end BookExamples.Xi
