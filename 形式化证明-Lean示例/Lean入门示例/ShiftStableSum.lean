import Mathlib.Tactic

/-!
# 常数序列不能被赋予满足首项分离规则的有限实数和

对应学习笔记《自然数之和与负十二分之一》中的求和规则讨论。
设 V 对每个实数序列赋予一个实数，并对每个序列满足
V(a) = a(0) + V(a(1),a(2),...)。把常数序列 1 代入就会矛盾。

本例说明不能把这套规则同时扩展到全部序列，不否定通常收敛级数的求和。
证明只使用首项分离的假设、常数序列的移位不变性与实数加法。
它不证明任何发散级数具有通常意义下的有限和。
-/

namespace Progressive

theorem no_shift_stable_sum (V : (ℕ → ℝ) → ℝ)
    (hV : ∀ a : ℕ → ℝ, V a = a 0 + V (fun n => a (n + 1))) : False := by
  -- 先给常数序列命名；每个自然数位置的值都是实数 1。
  let ones : ℕ → ℝ := fun _ => 1
  -- 删除首项后仍是同一个常数序列，按定义就可核对函数相等。
  have hShift : (fun n => ones (n + 1)) = ones := by
    rfl
  -- 将所假设的首项分离规则专门用于这个序列。
  have hAtOnes := hV ones
  -- 用刚证明的移位不变性替换等式右端的尾序列。
  rw [hShift] at hAtOnes
  -- 展开首项 ones(0)=1，明确得到有限实数满足 S=1+S 的断言。
  change V ones = 1 + V ones at hAtOnes
  -- 实数等式两边消去同一个 V ones 后得到 0=1，因此原假设矛盾。
  linarith [hAtOnes]

end Progressive
