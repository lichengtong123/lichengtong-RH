import Mathlib.NumberTheory.LSeries.RiemannZeta
import Mathlib.NumberTheory.LSeries.Nonvanishing
import Mathlib.Analysis.SpecialFunctions.Trigonometric.Complex
import BookExamples.S1b_RHStatement

/-!
# 第 4 阶段 · 例题 8：非平凡零点位于开临界带（本书第 9–11 章）

书中第二部分的结论之一：ζ 的零点除平凡零点 −2, −4, −6, … 外，都在开临界带 0 < Re s < 1 内。
本例把三块已知结果拼接起来证明它：
1. Re s ≥ 1 时 ζ(s) ≠ 0（mathlib 定理，对应书中第 9 章的无零点证明）；
2. Re s ≤ 0 时，用函数方程把 s 翻到 1 − s（Re(1 − s) ≥ 1），在那里 ζ、Γ、指数因子都不为零，
   只剩 cos(π(1−s)/2) = 0，由此解出 s 只能是平凡零点；
3. 合起来，非平凡零点只能落在 0 < Re s < 1。

作为推论，证明例题 2 中的两种黎曼猜想陈述等价：mathlib 的 `RiemannHypothesis`
（用“不是平凡零点”刻画）与书中的 `RHBook`（用“在临界带内”刻画）。

## 本例显式引用的 mathlib 定理

| 定理名 | 数学内容 |
|---|---|
| `riemannZeta_ne_zero_of_one_le_re` | Re s ≥ 1 时 ζ(s) ≠ 0 |
| `riemannZeta_one_sub` | 函数方程 ζ(1−s) = 2(2π)^(−s) Γ(s) cos(πs/2) ζ(s) |
| `riemannZeta_zero` | ζ(0) = −1/2 |
| `Complex.Gamma_ne_zero` | s 不是非正整数时 Γ(s) ≠ 0 |
| `Complex.cpow_ne_zero_iff` | 复数幂何时不为零 |
| `Complex.cos_eq_zero_iff` | cos θ = 0 当且仅当 θ = (2k+1)π/2 |

## 值得注意的一点

mathlib 陈述中的条件 s ≠ 1 在这里没有用到：mathlib 给 ζ(1) 规定的约定值不为零，
`riemannZeta_ne_zero_of_one_le_re` 已经覆盖 s = 1。这是约定影响证明细节的又一例。
-/

open Complex
open scoped Real

namespace BookExamples.CriticalStrip

/-- 第一步：若 ζ(s) = 0 且 Re s ≤ 0，则 s 是平凡零点。 -/
theorem trivial_of_re_nonpos {s : ℂ} (hz : riemannZeta s = 0) (hre : s.re ≤ 0) :
    ∃ n : ℕ, s = -2 * (n + 1) := by
  -- 记 s = 1 − w，则 Re w ≥ 1。
  obtain ⟨w, rfl⟩ : ∃ w, s = 1 - w := ⟨1 - s, by ring⟩
  have hwre : 1 ≤ w.re := by
    rw [sub_re, one_re] at hre
    linarith
  -- w ≠ 1：否则 s = 0，而 ζ(0) = −1/2 ≠ 0。
  have hw1 : w ≠ 1 := by
    rintro rfl
    rw [sub_self, riemannZeta_zero] at hz
    norm_num at hz
  -- w 不是非正整数（它的实部 ≥ 1）。
  have hwn : ∀ n : ℕ, w ≠ -n := by
    intro n h
    rw [h, neg_re, natCast_re] at hwre
    have : (0 : ℝ) ≤ n := Nat.cast_nonneg n
    linarith
  -- 函数方程：0 = ζ(1 − w) = 2 (2π)^(−w) Γ(w) cos(πw/2) ζ(w)。
  have hfe := riemannZeta_one_sub hwn hw1
  rw [hz] at hfe
  have hζw : riemannZeta w ≠ 0 := riemannZeta_ne_zero_of_one_le_re hwre
  have hΓ : Gamma w ≠ 0 := Gamma_ne_zero hwn
  have hπ : (π : ℂ) ≠ 0 := ofReal_ne_zero.mpr Real.pi_ne_zero
  have hpow : (2 * (π : ℂ)) ^ (-w) ≠ 0 :=
    cpow_ne_zero_iff.mpr (Or.inl (mul_ne_zero two_ne_zero hπ))
  -- 其余因子都不为零，所以 cos(πw/2) = 0。
  have hcos : cos (π * w / 2) = 0 := by
    have h0 := hfe.symm
    simp only [mul_eq_zero, hζw, hΓ, hpow, two_ne_zero, or_false, false_or] at h0
    exact h0
  -- cos(πw/2) = 0 推出 w = 2k + 1。
  obtain ⟨k, hk⟩ := cos_eq_zero_iff.mp hcos
  have hwk : w = 2 * k + 1 := by
    have h2 : (π : ℂ) * (w - (2 * k + 1)) = 0 := by linear_combination 2 * hk
    rcases mul_eq_zero.mp h2 with h | h
    · exact absurd h hπ
    · linear_combination h
  subst hwk
  -- 于是 s = −2k；由 Re s ≤ 0 得 k ≥ 0，由 s ≠ 0 得 k ≠ 0。
  have hk0' : 0 ≤ k := by
    have h3 : (1 : ℂ) - (2 * k + 1) = ((-2 * k : ℤ) : ℂ) := by push_cast; ring
    rw [h3, intCast_re] at hre
    have h4 : -2 * k ≤ 0 := by exact_mod_cast hre
    omega
  have hkne : k ≠ 0 := by
    rintro rfl
    simp at hw1
  -- 取 n = k − 1，即 s = −2(n + 1)。
  refine ⟨(k - 1).toNat, ?_⟩
  have hn : (((k - 1).toNat : ℕ) : ℤ) = k - 1 := Int.toNat_of_nonneg (by omega)
  have hnC : (((k - 1).toNat : ℕ) : ℂ) = (k : ℂ) - 1 := by exact_mod_cast hn
  rw [hnC]
  ring

/-- 第二步：非平凡零点都在开临界带 0 < Re s < 1 内。 -/
theorem mem_criticalStrip {s : ℂ} (hz : riemannZeta s = 0)
    (hnt : ¬∃ n : ℕ, s = -2 * (n + 1)) : 0 < s.re ∧ s.re < 1 := by
  constructor
  · by_contra h
    push_neg at h
    exact hnt (trivial_of_re_nonpos hz h)
  · by_contra h
    push_neg at h
    exact riemannZeta_ne_zero_of_one_le_re h hz

/-- 推论：mathlib 的黎曼猜想陈述与书中的陈述等价。 -/
theorem riemannHypothesis_iff_book : RiemannHypothesis ↔ RHBook := by
  constructor
  · -- mathlib 陈述 ⇒ 书中陈述：临界带内的零点不是平凡零点，也不是 s = 1。
    intro h s hz h0 h1
    apply h s hz
    · rintro ⟨n, rfl⟩
      have hn : (0 : ℝ) ≤ n := Nat.cast_nonneg n
      simp at h0
      linarith
    · rintro rfl
      simp at h1
  · -- 书中陈述 ⇒ mathlib 陈述：由第二步，非平凡零点都在临界带内。
    intro h s hz hnt _
    obtain ⟨h0, h1⟩ := mem_criticalStrip hz hnt
    exact h s hz h0 h1

end BookExamples.CriticalStrip
