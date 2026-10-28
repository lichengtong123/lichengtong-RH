# 形式化证明-Lean示例

本目录以本书的若干定理为例，介绍**形式化证明及其核验**。[Lean](https://lean-lang.org/) 是一种证明助手：使用者将数学定义、命题和推理步骤写成严格的形式语言，由计算机逐步检查推导是否符合逻辑规则。随着 AI 生成的数学证明越来越多，“经过形式化验证”正在成为判断一个证明是否可靠的重要依据；了解它检查什么、不检查什么，对阅读数学新闻和文献都有帮助。

**这些文件是了解形式化验证的示例，不是对本书的整体形式化验证。** 本目录尚未重现显式公式、零点计数、von Koch 等价等主线证明；书中的论证以数学证明和所引文献为依据，不依赖本目录。这一范围说明不代表对其他形式化项目进展的判断。

## 不装 Lean 也能看什么

- 每个 `.lean` 文件都配有中文注释：对应书中哪一章、用通常的数学语言怎样陈述、Lean 写法逐项是什么意思、与书中写法有何不同。在 GitHub 上直接点开即可阅读。
- 仓库配置了自动检查：相关文件更新后，GitHub 的服务器会构建默认目标 `LeanExamples` 及其导入的模块。检查通过，表示这些模块中的形式化证明被 Lean 接受，不包括未被导入的练习文件，也不检查中文注释是否准确。检查记录在仓库的 Actions 页面公开。

## 按难度递进的逐步推导

目录分为两组：[各章Lean示例](各章Lean示例/)保存与正文章节对应的 `ChXX_…` 例程；[Progressive](Progressive/)保存逐步推导例程及配套说明。两者均位于本项目根目录下。`LeanExamples.lean` 是统一构建入口，`LeanExamples/Notes.lean` 暂保留原位，作为补充命题示例。

例程的用途、运行方法及完成范围见 [Progressive 的说明](Progressive/README.md)。选题包括 3–4–1 三角不等式、von Mangoldt 恒等式与 Möbius 反演，以及函数方程推导中的反射对称片段。实际推理逐步配中文注释，不以一句现成目标定理代替证明。

前两项已提供完整代码，函数方程的分析部分尚未形式化。以下按章列表保留作库定理对照，不与逐步推导例程的完成范围混同。

## 与本书的对照

| 文件 | 书中位置 | 内容 | 来源 |
|------|----------|------|------|
| [Ch02_ArithmeticFunctions.lean](各章Lean示例/Ch02_ArithmeticFunctions.lean) | 第 2 章，附录 A、B | $\sum_{d\mid n}\Lambda(d)=\log n$；$\mu*\zeta=1$；Möbius 反演；Abel 求和 | mathlib |
| [Ch05_EulerProduct.lean](各章Lean示例/Ch05_EulerProduct.lean) | 第 5 章 | Euler 乘积 | mathlib |
| [Ch06_Chebyshev.lean](各章Lean示例/Ch06_Chebyshev.lean) | 第 6 章 | $n\#\le4^n$；由此 $\theta(n)\le n\log4$ | mathlib；后者为本仓库补写 |
| [Ch07_Gamma.lean](各章Lean示例/Ch07_Gamma.lean) | 第 7 章 | 倍元公式、余元公式 | mathlib |
| [Ch09_Zeta.lean](各章Lean示例/Ch09_Zeta.lean) | 第 9 章，附录 F | 函数方程；$\operatorname{Re}s\ge1$ 上无零点；mathlib 对 $\zeta(1)$ 的约定；$\zeta(2)=\pi^2/6$；$\zeta(-1)=-1/12$ | mathlib；最后一条为本仓库补写 |
| [Ch11_RiemannHypothesis.lean](各章Lean示例/Ch11_RiemannHypothesis.lean) | 第 11 章 | RH 的形式化陈述；平凡零点；一个被 Lean 接受却与 RH 无关的陈述 | mathlib（RH 本身未证明） |
| [Notes.lean](LeanExamples/Notes.lean) | 附录 F；学习笔记第 11、16、20 篇 | $3+4\cos\theta+\cos2\theta\ge0$；平移稳定的求和法不能给 $1+1+\cdots$ 赋值；$2^{61}-1$ 是素数 | 本仓库补写 |

截至本目录 2026 年 10 月 27 日的检查，默认构建未覆盖：$\xi$ 的 Hadamard 乘积（第 10 章）、零点计数公式（第 11 章）、素数定理（第 12 章）、显式公式（第 14 章）、RH 的算术等价（第 15 章）。本目录固定的 mathlib 版本见下文。独立项目的范围和完成状态应按其具体版本核对，例如 [PrimeNumberTheoremAnd](https://github.com/AlexKontorovich/PrimeNumberTheoremAnd)；不能从本目录未涉及某个结果，推断整个领域尚无相应形式化。

## mathlib 中的定理从哪里来

[mathlib](https://github.com/leanprover-community/mathlib4) 是 Lean 社区共同维护的数学库。其中每条定理都是有人用 Lean 写出完整证明、经 Lean 检查后收入的；按定理名可以在 mathlib 源代码中找到它的证明，并逐层追溯到 Lean 的基本公理。引用 mathlib 的定理，相当于写论文时引用已发表的引理：省去重复的工作，检查的标准并不降低。

反过来，某个版本的 mathlib 未收入一条命题，不意味着它不能在 Lean 中证明，也不意味着其他项目没有形式化。上表中标明“本仓库补写”的几条，就是在 mathlib 已有结果之上写出的证明。扩展到本书的完整主线需要逐项建立依赖，不能由几个示例代替。黎曼猜想的情形不同：它的陈述已在 mathlib 中，缺的是数学上的证明。

## 读这些文件时值得注意的地方

- **条件必须写全。** 书中的“$f$ 连续可微”在 Abel 求和的 Lean 版本里被拆成“处处可微”和“导数可积”两条；Euler 乘积若去掉 `1 < s.re`，Lean 就不接受证明。
- **约定可能与数学惯例不同。** Lean 中的函数在每一点都必须有值：mathlib 规定 $\Gamma$ 在极点处取 $0$，规定 `riemannZeta 1` $=(\gamma-\log4\pi)/2$（数学上 $\zeta(1)$ 无定义）。因此“$\operatorname{Re}s\ge1$ 时 $\zeta(s)\ne0$”在 $s=1$ 处说的是约定值，不是关于极点的断言。
- **Lean 检查的是推导，不检查陈述是否忠实于原意。** 一条形式化陈述即使被 Lean 接受，它是否就是书中那句话，仍要由人对照判断。这正是阅读“AI 证明了某定理并通过形式化验证”这类消息时需要追问的地方。

## 在本机运行（可选）

需要先安装 Lean 的版本管理器 [elan](https://github.com/leanprover/elan)。本目录固定使用 Lean `v4.22.0-rc4` 与 mathlib 提交 `e20d25fa`（2025-08-06），首次运行会下载 mathlib 的预编译文件（数 GB）：

```bash
cd 形式化证明-Lean示例
lake exe cache get
lake build
```

`lake build` 无报错结束，即表示全部通过。mathlib 更新很快，升级时须同时更换 `lean-toolchain` 与 `lakefile.toml` 中的版本，并重新检查定理名称。

## 许可

除另行注明来源与许可的文件外，本目录的 Lean 程序文件采用 MIT 许可，说明文字采用 CC BY-NC-SA 4.0。`Intermediate.lean` 中的因子和证明改编自 mathlib，按 Apache-2.0 发布，见[许可全文](Progressive/Apache-2.0.txt)及仓库根目录的 [LICENSE](../LICENSE)。
