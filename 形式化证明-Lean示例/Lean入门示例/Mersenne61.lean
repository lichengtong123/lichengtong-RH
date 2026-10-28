import Mathlib.NumberTheory.LucasLehmer
import Mathlib.Tactic

/-!
# 以 Lucas–Lehmer 计算证书核验 2^61−1 的素性

对应学习笔记《计算机能证明定理吗》；作为自选补充例程。
基础输入是已核验的一般 Lucas–Lehmer 充分性判据，本例不重新证明该判据，
也不直接引用已经证明 2^61−1 为素数的专门定理。

对 p=61，从 s₀=4 开始，按 sₖ₊₁=sₖ²−2 在模 2^61−1 下递推。
库的 norm_num 扩展核验第 p−2=59 步的余数为零，并生成可由 Lean 内核检查的证明。
这不是普通浮点试验，也没有把未经认证的外部计算输出直接当作假设。
-/

namespace Progressive

-- 先核对记号 mersenne 61 对应的十进制整数。
theorem mersenne61_value : mersenne 61 = 2305843009213693951 := by
  -- 展开 mersenne p = 2^p−1，作精确整数运算。
  norm_num [mersenne]

-- 把计算与判据的应用分开，显示素性结论的输入。
theorem mersenne61_prime : (mersenne 61).Prime := by
  -- 核对一般充分性判据对指数的范围要求；这里需要 1<61。
  have hExponent : 1 < (61 : ℕ) := by
    norm_num
  -- 独立核验 Lucas–Lehmer 测试通过，即上述第 59 步的模余数为零。
  have hCertificate : LucasLehmer.LucasLehmerTest 61 := by
    norm_num
  -- 将范围条件和计算证书交给一般判据，推出 Mersenne 数为素数。
  exact lucas_lehmer_sufficiency 61 hExponent hCertificate

-- 最后给出十进制整数形式，说明两个写法确实指同一个数。
theorem mersenne61_decimal_prime : Nat.Prime 2305843009213693951 := by
  -- 用第一段核对过的整数等式，将目标改写为 mersenne 61 的素性。
  rw [← mersenne61_value]
  -- 引用本文件第二段实际完成的素性证明。
  exact mersenne61_prime

end Progressive
