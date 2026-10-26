/-
# 第 7 章：$\Gamma$ 函数的倍元公式与余元公式
-/
import Mathlib.Analysis.SpecialFunctions.Gamma.Beta

/-! ## Legendre 倍元公式

书中第 7 章（并见参考习题 7.2、学习笔记第 3 篇）：
$$\Gamma(s)\,\Gamma\!\left(s + \tfrac12\right) = 2^{1 - 2s} \sqrt{\pi}\, \Gamma(2s) .$$
mathlib 对一切复数 $s$ 陈述这一公式，没有附加条件。原因是 mathlib 在 $\Gamma$ 的极点
（$0, -1, -2, \dots$）处也给 `Complex.Gamma` 指定了值（取 $0$），于是公式在极点两边都按约定成立。
书中则把极点排除在外。这是“形式化约定”与“数学惯例”不同的一个典型例子。 -/
example (s : ℂ) :
    Complex.Gamma s * Complex.Gamma (s + 1 / 2) =
      Complex.Gamma (2 * s) * (2 : ℂ) ^ (1 - 2 * s) * ↑(Real.sqrt Real.pi) :=
  Complex.Gamma_mul_Gamma_add_half s

/-! ## 余元公式
$$\Gamma(z)\,\Gamma(1 - z) = \frac{\pi}{\sin \pi z} .$$
同样对一切复数 $z$ 陈述：在整数 $z$ 处右边分母为 $0$，mathlib 约定除以 $0$ 得 $0$，
左边按 $\Gamma$ 在极点处取 $0$ 的约定也为 $0$。 -/
example (z : ℂ) :
    Complex.Gamma z * Complex.Gamma (1 - z) = ↑Real.pi / Complex.sin (↑Real.pi * z) :=
  Complex.Gamma_mul_Gamma_one_sub z
