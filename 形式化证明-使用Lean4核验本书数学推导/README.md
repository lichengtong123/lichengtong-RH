# 形式化证明：使用 Lean 4 核验本书数学推导

本栏目**选取本书涉及的若干经典数学命题作为示例**，结合 Mathlib 中已有的形式化成果与展开推理的示例，介绍形式化证明的基本概念、写法及核验过程，为尚未接触 Lean 的读者提供入门引导。本栏目是供读者自由选读的配套材料，不以系统讲授 Lean 为目标，侧重借助读者已经了解的数学内容，认识一种新的证明工具。

[Lean](https://lean-lang.org/) 是一种证明助手；本栏目使用 Lean 4。使用者将数学定义、命题和推理步骤写成严格的形式语言，由计算机逐步检查推导是否符合逻辑规则。随着 AI 生成的数学证明越来越多，形式化核验也日益受到关注。

## 不安装 Lean 也能阅读的内容

- 每个 `.lean` 文件均配有中文注释，说明相应的数学命题、Lean 代码的含义，以及形式化陈述在记号、适用条件和定义约定上与书中表述的区别。在 GitHub 上直接点开即可阅读。
- 仓库配置了自动检查：相关文件更新后，GitHub 服务器会构建项目的统一入口及其导入的例程。检查通过，表示这些例程中的形式化证明已被 Lean 接受。未纳入构建入口的文件不会自动检查；中文注释仅供阅读，其内容仍需人工核对。检查记录在仓库的 Actions 页面公开。

## Lean 入门与章节对照

**阅读具体例程，请进入以下目录，而不是打开根目录中同名的 `.lean` 文件：**

- [Lean入门示例](Lean入门示例/)：通过由易到难的数学例子，介绍 Lean 的基本使用方法、操作步骤、证明写法及核验结果的理解，并提供自选补充例程。初次接触 Lean 的读者可从这里开始。
- [各章Lean示例](各章Lean示例/)：以 `ChXX_…` 例程对照本书命题与 Mathlib 已有定理，主要展示形式化陈述、适用条件及库定理的调用，另有少量应用推导，不逐章重现书中的完整证明。

建议先阅读 3–4–1 例程，再阅读 von Mangoldt 恒等式与 Möbius 反演，随后按兴趣对照各章的库定理引用。θ–Mellin 例程目前只完成反射对称的代数片段，可用于理解模型对称性与完整函数方程证明之间还需要哪些分析步骤。

根目录中的以下三个文件仅用于汇总导入和自动构建，**不包含新的例题证明，读者无需直接阅读**：

| 入口文件 | 用途 |
|----------|------|
| `LeanExamples.lean` | 导入下面两个分组入口，供整个项目统一构建与核验。 |
| `Lean入门示例.lean` | 导入“Lean入门示例”目录中的例程。 |
| `各章Lean示例.lean` | 导入“各章Lean示例”目录中的例程。 |

例程的用途、运行方法及完成范围见 [Lean入门示例的说明](Lean入门示例/README.md)。选题包括 3–4–1 三角不等式、von Mangoldt 恒等式与 Möbius 反演，以及函数方程推导中的反射对称片段。实际推理逐步配中文注释，不以一句现成目标定理代替证明，也不将本栏目扩展为系统课程。

前两项已提供完整代码，函数方程的分析部分尚未形式化。以下按章列表保留作库定理对照，不与逐步推导例程的完成范围混同。

## 与本书的对照

| 文件 | 书中位置 | 内容 | 来源 |
|------|----------|------|------|
| [Ch02_ArithmeticFunctions.lean](各章Lean示例/Ch02_ArithmeticFunctions.lean) | 第 2 章，附录 A、B | $\sum_{d\mid n}\Lambda(d)=\log n$；$\mu*\zeta=1$；Möbius 反演；Abel 求和 | mathlib |
| [Ch05_EulerProduct.lean](各章Lean示例/Ch05_EulerProduct.lean) | 第 5 章 | Euler 乘积 | mathlib |
| [Ch06_Chebyshev.lean](各章Lean示例/Ch06_Chebyshev.lean) | 第 6 章 | $\prod_{p\le n}p\le4^n$（乘积遍历素数）；由此 $\theta(n)\le n\log4$ | mathlib；后者为本仓库补写 |
| [Ch07_Gamma.lean](各章Lean示例/Ch07_Gamma.lean) | 第 7 章 | 倍元公式、余元公式 | mathlib |
| [Ch09_Zeta.lean](各章Lean示例/Ch09_Zeta.lean) | 第 9 章，附录 F | 函数方程；$\operatorname{Re}s\ge1$ 上无零点；mathlib 对 $\zeta(1)$ 的约定；$\zeta(2)=\pi^2/6$；$\zeta(-1)=-1/12$ | mathlib；最后一条为本仓库补写 |
| [Ch11_RiemannHypothesis.lean](各章Lean示例/Ch11_RiemannHypothesis.lean) | 第 11 章 | RH 的形式化陈述；平凡零点；一个被 Lean 接受却与 RH 无关的陈述 | mathlib（RH 本身未证明） |
| [ShiftStableSum.lean](Lean入门示例/ShiftStableSum.lean) | 学习笔记第 11 篇 | 将首项分离规则用于常数序列，推出有限实数赋值的矛盾 | 本仓库展开推导 |
| [Mersenne61.lean](Lean入门示例/Mersenne61.lean) | 学习笔记第 16 篇 | 核验 $2^{61}-1$ 的 Lucas–Lehmer 计算证书，再用一般判据推出素性 | mathlib 的一般判据与认证计算；本仓库组织分步证明 |

本目录目前收录的示例见上表，今后将根据读者需要及内容建设情况逐步增补。本目录固定的 mathlib 版本见下文；其他形式化项目的收录范围与完成情况，可参阅各项目的说明，例如 [PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd)。

## Mathlib 数学库及其定理来源

[mathlib](https://github.com/leanprover-community/mathlib4) 是 Lean 社区共同维护的数学库。其中每条定理都是有人用 Lean 写出完整证明、经 Lean 检查后收入的；按定理名可以在 mathlib 源代码中找到它的证明，并逐层追溯到 Lean 的基本公理。引用 mathlib 的定理，相当于写论文时引用已发表的引理：省去重复的工作，检查的标准并不降低。

反过来，某个版本的 mathlib 未收入一条命题，不意味着它不能在 Lean 中证明，也不意味着其他项目没有形式化。上表中标明“本仓库补写”的几条，就是在 mathlib 已有结果之上写出的证明。扩展到本书的完整主线需要逐项建立依赖，不能由几个示例代替。黎曼猜想的情形不同：它的陈述已在 mathlib 中，缺的是数学上的证明。

## 读这些文件时值得注意的地方

- **条件必须写全。** 书中的“$f$ 连续可微”在 Abel 求和的 Lean 版本里被拆成“处处可微”和“导数可积”两条；Euler 乘积若去掉 `1 < s.re`，Lean 就不接受证明。
- **约定可能与数学惯例不同。** Lean 中的函数在每一点都必须有值：mathlib 规定 $\Gamma$ 在极点处取 $0$，规定 `riemannZeta 1` $=(\gamma-\log4\pi)/2$（数学上 $\zeta(1)$ 无定义）。因此“$\operatorname{Re}s\ge1$ 时 $\zeta(s)\ne0$”在 $s=1$ 处说的是约定值，不是关于极点的断言。
- **Lean 检查的是推导，不检查陈述是否忠实于原意。** 一条形式化陈述即使被 Lean 接受，它是否就是书中那句话，仍要由人对照判断。这正是阅读“AI 证明了某定理并通过形式化验证”这类消息时需要追问的地方。

## 在本机运行（可选）

需要先安装 Lean 的版本管理器 [elan](https://github.com/leanprover/elan)。本目录固定使用 Lean `v4.22.0-rc4` 与 mathlib 提交 `e20d25fa`（2025-08-06），首次运行会下载 mathlib 的预编译文件（数 GB）：

```bash
cd 形式化证明-使用Lean4核验本书数学推导
lake exe cache get
lake build
```

`lake build` 无报错结束，即表示全部通过。mathlib 更新很快，升级时须同时更换 `lean-toolchain` 与 `lakefile.toml` 中的版本，并重新检查定理名称。

## 许可

除另行注明来源与许可的文件外，本目录的 Lean 程序文件采用 MIT 许可，说明文字采用 CC BY-NC-SA 4.0。`VonMangoldtMobius.lean` 中的因子和证明改编自 mathlib，按 Apache-2.0 发布，见[许可全文](Lean入门示例/Apache-2.0.txt)及仓库根目录的 [LICENSE](../LICENSE)。
