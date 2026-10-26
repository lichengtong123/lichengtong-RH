# Lean 示例：用形式化验证对照本书的定理

本目录以本书的若干定理为例，介绍**形式化验证**：把数学陈述和证明写成证明助手 [Lean](https://lean-lang.org/) 能够逐步检查的形式。随着 AI 生成的数学证明越来越多，“经过形式化验证”正在成为判断一个证明是否可靠的重要依据；了解它检查什么、不检查什么，对阅读数学新闻和文献都有帮助。

**这些文件是了解形式化验证的示例，不是对本书的验证。** 本书主线上的大部分定理（显式公式、零点计数、von Koch 等价等）目前都还没有形式化；书中的论证以数学证明和所引文献为依据，不依赖本目录。

## 不装 Lean 也能看什么

- 每个 `.lean` 文件都配有中文注释：对应书中哪一章、用通常的数学语言怎样陈述、Lean 写法逐项是什么意思、与书中写法有何不同。在 GitHub 上直接点开即可阅读。
- 仓库配置了自动检查：每次更新后，GitHub 的服务器都会用 Lean 完整编译本目录。检查通过，就说明这里的每一条陈述都已被 Lean 接受。检查记录在仓库的 Actions 页面公开。

## 与本书的对照

| 文件 | 书中位置 | 内容 | 来源 |
|------|----------|------|------|
| [Ch02_ArithmeticFunctions.lean](LeanExamples/Ch02_ArithmeticFunctions.lean) | 第 2 章，附录 A、B | $\sum_{d\mid n}\Lambda(d)=\log n$；$\mu*\zeta=1$；Möbius 反演；Abel 求和 | mathlib |
| [Ch05_EulerProduct.lean](LeanExamples/Ch05_EulerProduct.lean) | 第 5 章 | Euler 乘积 | mathlib |
| [Ch06_Chebyshev.lean](LeanExamples/Ch06_Chebyshev.lean) | 第 6 章 | $n\#\le4^n$；由此 $\theta(n)\le n\log4$ | mathlib；后者为本仓库补写 |
| [Ch07_Gamma.lean](LeanExamples/Ch07_Gamma.lean) | 第 7 章 | 倍元公式、余元公式 | mathlib |
| [Ch09_Zeta.lean](LeanExamples/Ch09_Zeta.lean) | 第 9 章，附录 F | 函数方程；$\operatorname{Re}s\ge1$ 上无零点；mathlib 对 $\zeta(1)$ 的约定；$\zeta(2)=\pi^2/6$；$\zeta(-1)=-1/12$ | mathlib；最后一条为本仓库补写 |
| [Ch11_RiemannHypothesis.lean](LeanExamples/Ch11_RiemannHypothesis.lean) | 第 11 章 | RH 的形式化陈述；平凡零点；一个被 Lean 接受却与 RH 无关的陈述 | mathlib（RH 本身未证明） |
| [Notes.lean](LeanExamples/Notes.lean) | 附录 F；学习笔记第 11、16、20 篇 | $3+4\cos\theta+\cos2\theta\ge0$；平移稳定的求和法不能给 $1+1+\cdots$ 赋值；$2^{61}-1$ 是素数 | 本仓库补写 |

mathlib 中尚未收入、本目录也未涉及的：$\xi$ 的 Hadamard 乘积（第 10 章）、零点计数公式（第 11 章）、素数定理（第 12 章；它不在 mathlib 中，但已在独立项目中形式化：Isabelle 与 HOL Light 中分别于 2007、2009 年完成；Lean 中有 Tao 与 Kontorovich 发起的 [PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd)，带误差项的强形式由 AI 代理 Gauss 于 2025 年完成）、显式公式（第 14 章）、RH 的算术等价（第 15 章）。书中最核心的部分，正是形式化尚未到达的地方。

## mathlib 中的定理从哪里来

[mathlib](https://github.com/leanprover-community/mathlib4) 是 Lean 社区共同维护的数学库。其中每条定理都是有人用 Lean 写出完整证明、经 Lean 检查后收入的；按定理名可以在 mathlib 源代码中找到它的证明，并逐层追溯到 Lean 的基本公理。引用 mathlib 的定理，相当于写论文时引用已发表的引理：省去重复的工作，检查的标准并不降低。

反过来，mathlib 中没有的命题，只是还没有人把它形式化并收入，并不意味着它不能在 Lean 中证明。上表中标明“本仓库补写”的几条，就是在 mathlib 已有结果之上自己写出的证明。书中显式公式、零点计数等内容尚未形式化，原因在于工作量大，而不是原则上做不到。黎曼猜想的情形不同：它的陈述已在 mathlib 中，缺的是数学上的证明。

## 读这些文件时值得注意的地方

- **条件必须写全。** 书中的“$f$ 连续可微”在 Abel 求和的 Lean 版本里被拆成“处处可微”和“导数可积”两条；Euler 乘积若去掉 `1 < s.re`，Lean 就不接受证明。
- **约定可能与数学惯例不同。** Lean 中的函数在每一点都必须有值：mathlib 规定 $\Gamma$ 在极点处取 $0$，规定 `riemannZeta 1` $=(\gamma-\log4\pi)/2$（数学上 $\zeta(1)$ 无定义）。因此“$\operatorname{Re}s\ge1$ 时 $\zeta(s)\ne0$”在 $s=1$ 处说的是约定值，不是关于极点的断言。
- **Lean 检查的是推导，不检查陈述是否忠实于原意。** 一条形式化陈述即使被 Lean 接受，它是否就是书中那句话，仍要由人对照判断。这正是阅读“AI 证明了某定理并通过形式化验证”这类消息时需要追问的地方。

## 在本机运行（可选）

需要先安装 Lean 的版本管理器 [elan](https://github.com/leanprover/elan)。本目录固定使用 Lean `v4.22.0-rc4` 与 mathlib 提交 `e20d25fa`（2025-08-06），首次运行会下载 mathlib 的预编译文件（数 GB）：

```bash
cd Lean示例
lake exe cache get
lake build
```

`lake build` 无报错结束，即表示全部通过。mathlib 更新很快，升级时须同时更换 `lean-toolchain` 与 `lakefile.toml` 中的版本，并重新检查定理名称。

## 许可

本目录的 Lean 程序文件采用 MIT 许可，说明文字采用 CC BY-NC-SA 4.0，见仓库根目录的 [LICENSE](../LICENSE)。
