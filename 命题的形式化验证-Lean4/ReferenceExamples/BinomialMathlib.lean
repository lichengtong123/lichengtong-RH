import Mathlib -- 导入 Mathlib 数学库（包含代数学、组合数学及二项式定理等基础理论）

open scoped BigOperators -- 启用大运算符作用域，以便使用连加符号 ∑ 等记号

theorem binomial_theorem -- 声明定理：名称为 binomial_theorem（二项式定理）
    {R : Type*} [CommSemiring R] (a b : R) (n : ℕ) : -- 设 R 为交换半环，a 和 b 为 R 中的元素，n 为自然数
    (a + b)^n = -- 等式左边：(a + b) 的 n 次方
      ∑ k ∈ Finset.range (n + 1), -- 对 k 从 0 到 n 进行求和（Finset.range (n + 1) 表示集合 {0, 1, ..., n}）
        a^k * b^(n - k) * (Nat.choose n k : R) := by -- 求和通项：a^k 乘以 b^(n-k) 再乘以组合数 C(n, k)（转换为 R 类型），并进入策略证明模式
  simpa only [mul_comm, mul_left_comm, mul_assoc] using (add_pow a b n) -- 调用 Mathlib 已有的二项式展开定理 add_pow，并仅使用乘法交换律与结合律化简完成证明

#print axioms binomial_theorem -- 显示证明该定理所依赖的所有底层公理
