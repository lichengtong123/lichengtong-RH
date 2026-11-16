-- 纯 Lean 4 核心库实现并证明二项式定理（完全不依赖 Mathlib）

-- 1. 利用杨辉三角（帕斯卡恒等式）递归定义组合数 C(n, k)
def choose : Nat → Nat → Nat
  | _, 0 => 1                                    -- C(n, 0) = 1
  | 0, _ + 1 => 0                                -- 当 k > 0 时，C(0, k) = 0
  | n + 1, k + 1 => choose n k + choose n (k + 1) -- 递推关系：C(n+1, k+1) = C(n, k) + C(n, k+1)

-- 2. 递归定义前 n 项求和函数：sumRange f n = f(0) + f(1) + ... + f(n-1)
def sumRange (f : Nat → Nat) : Nat → Nat
  | 0 => 0                                       -- 空和为 0
  | n + 1 => sumRange f n + f n                  -- 前 n+1 项和 = 前 n 项和 + 第 n 项

-- 辅助引理 1a：当 k > n 时，组合数 C(n, k) = 0
theorem choose_eq_zero_of_lt : ∀ (n k : Nat), n < k → choose n k = 0
  | 0, k + 1, _ => rfl
  | n + 1, k + 1, h => by
    rw [choose, choose_eq_zero_of_lt n k (by omega), choose_eq_zero_of_lt n (k + 1) (by omega)]

-- 辅助引理 1b：组合数对角线性质 C(n, n) = 1
theorem choose_self (n : Nat) : choose n n = 1 := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [choose, ih, choose_eq_zero_of_lt n (n + 1) (by omega)]

-- 辅助引理 2：将求和拆出首项 f(0)：sumRange f (n + 1) = f 0 + sumRange (fun k => f (k + 1)) n
theorem sumRange_succ_left (f : Nat → Nat) (n : Nat) :
    sumRange f (n + 1) = f 0 + sumRange (fun k => f (k + 1)) n := by
  induction n with
  | zero => simp [sumRange]
  | succ n ih =>
    rw [sumRange, ih, sumRange, Nat.add_assoc]

-- 辅助引理 3：乘法对求和的右分配律：(∑ f(k)) * c = ∑ (f(k) * c)
theorem sumRange_mul (f : Nat → Nat) (c n : Nat) :
    sumRange f n * c = sumRange (fun k => f k * c) n := by
  induction n with
  | zero => simp [sumRange]
  | succ n ih =>
    rw [sumRange, sumRange, Nat.right_distrib, ih]

-- 辅助引理 4：两个相同范围的求和相加：∑ f(k) + ∑ g(k) = ∑ (f(k) + g(k))
theorem sumRange_add (f g : Nat → Nat) (n : Nat) :
    sumRange f n + sumRange g n = sumRange (fun k => f k + g k) n := by
  induction n with
  | zero => simp [sumRange]
  | succ n ih =>
    simp only [sumRange]
    omega

-- 辅助引理 5：若在 k < n 范围内两函数逐项相等，则它们的求和相等
theorem sumRange_congr {f g : Nat → Nat} {n : Nat} (h : ∀ k, k < n → f k = g k) :
    sumRange f n = sumRange g n := by
  induction n with
  | zero => rfl
  | succ n ih =>
    rw [sumRange, sumRange, ih (fun k hk => h k (by omega)), h n (by omega)]

-- 辅助引理 6：合并相邻项的核心代数恒等式（帕斯卡法则合并同类项）
theorem term_combine (a b n k : Nat) (hk : k < n) :
    a ^ k * b ^ (n - k) * choose n k * a +
      a ^ (k + 1) * b ^ (n - (k + 1)) * choose n (k + 1) * b =
    a ^ (k + 1) * b ^ (n - k) * (choose n k + choose n (k + 1)) := by
  have hsub : n - k = (n - (k + 1)) + 1 := by omega
  have hb : b ^ (n - k) = b ^ (n - (k + 1)) * b := by rw [hsub, Nat.pow_succ]
  calc
    a ^ k * b ^ (n - k) * choose n k * a +
        a ^ (k + 1) * b ^ (n - (k + 1)) * choose n (k + 1) * b
      = (a ^ k * a) * b ^ (n - k) * choose n k +
        a ^ (k + 1) * (b ^ (n - (k + 1)) * b) * choose n (k + 1) := by
          simp only [Nat.mul_assoc, Nat.mul_comm, Nat.mul_left_comm]
    _ = a ^ (k + 1) * b ^ (n - k) * choose n k +
        a ^ (k + 1) * b ^ (n - k) * choose n (k + 1) := by
          rw [← Nat.pow_succ, ← hb]
    _ = a ^ (k + 1) * b ^ (n - k) * (choose n k + choose n (k + 1)) := by
          rw [← Nat.left_distrib]

-- 主定理：二项式定理（纯 Lean 4 证明，不依赖 Mathlib）
theorem binomial_theorem (a b n : Nat) :
    (a + b) ^ n =
      sumRange (fun k => a ^ k * b ^ (n - k) * choose n k) (n + 1) := by
  induction n with
  | zero =>
    simp [sumRange, choose]
  | succ n ih =>
    let T (m k : Nat) := a ^ k * b ^ (m - k) * choose m k
    change (a + b) ^ (n + 1) = sumRange (T (n + 1)) (n + 2)
    rw [Nat.pow_succ, ih, Nat.left_distrib, sumRange_mul, sumRange_mul]
    -- 拆分第一部分（乘以 a 的求和）：拆出最后一项 k = n
    rw [sumRange]
    -- 拆分第二部分（乘以 b 的求和）：拆出第一项 k = 0
    rw [sumRange_succ_left (fun k => T n k * b) n]
    -- 将首尾两项整理并把中间两个长度为 n 的求和合并
    have h_first : T n 0 * b = T (n + 1) 0 := by
      simp [T, choose, Nat.pow_succ, Nat.mul_comm, Nat.mul_left_comm]
    have h_last : T n n * a = T (n + 1) (n + 1) := by
      simp [T, choose_self, Nat.pow_succ, Nat.mul_comm]
    have h_mid :
        sumRange (fun k => T n k * a) n + sumRange (fun k => T n (k + 1) * b) n =
        sumRange (fun k => T (n + 1) (k + 1)) n := by
      rw [sumRange_add]
      apply sumRange_congr
      intro k hk
      dsimp [T, choose]
      rw [Nat.add_sub_add_right]
      exact term_combine a b n k hk
    -- 利用加法交换律和结合律拼回完整的 n + 2 项求和
    calc
      (sumRange (fun k => T n k * a) n + T n n * a) +
          (T n 0 * b + sumRange (fun k => T n (k + 1) * b) n)
        = T n 0 * b +
          (sumRange (fun k => T n k * a) n + sumRange (fun k => T n (k + 1) * b) n) +
          T n n * a := by omega
      _ = T (n + 1) 0 + sumRange (fun k => T (n + 1) (k + 1)) n + T (n + 1) (n + 1) := by
          rw [h_first, h_mid, h_last]
      _ = sumRange (T (n + 1)) (n + 1) + T (n + 1) (n + 1) := by
          rw [← sumRange_succ_left (T (n + 1)) n]
      _ = sumRange (T (n + 1)) (n + 2) := rfl

-- 查看该证明依赖的底层公理：只有 propext 与 Quot.sound，没有用到选择公理 Classical.choice
#print axioms binomial_theorem
-- 实际计算验证：(2 + 3)^4 = 625
#eval (2 + 3) ^ 4
#eval sumRange (fun k => 2 ^ k * 3 ^ (4 - k) * choose 4 k) 5
