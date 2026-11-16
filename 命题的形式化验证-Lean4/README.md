# 命题的形式化验证（Lean 4）

本栏目借本书读者已经熟悉的数学内容，介绍一种不同的数学证明方法——**形式化证明**：把定义、命题和每一步推理写成严格的形式语言，由计算机逐步检查。

本栏目不是 Lean 教程，而是从本书中选取若干命题，把它们的陈述与证明写成形式化代码，由 Lean 逐步检查。全部例题按“自己写多少、借用数学库多少”分为四个阶段，最后一节说明怎样检查一个号称“已经形式化”的证明。随着 AI 生成的数学证明越来越多，这种检查能力会越来越常用。

系统学习 Lean，请阅读下文推荐的教材。

## Lean 与 mathlib

[Lean](https://lean-lang.org/) 是一种证明助手，本栏目使用 Lean 4。[mathlib](https://github.com/leanprover-community/mathlib4) 是 Lean 社区共同维护的数学库，其中每条定理都有完整的形式化证明，并经 Lean 检查。引用 mathlib 的定理，相当于写论文时引用已发表的引理：省去重复的工作，检查的标准并不降低。

引用 mathlib 有两种方式：

| | 含义 | 例子 |
|---|---|---|
| **显式引用** | 在证明中点名使用某条库定理 | `rw [completedRiemannZeta_eq]` |
| **隐式引用** | 不写定理名，由自动化策略在幕后调用库中的引理；实数、复数、ζ 等定义本身也来自 mathlib | `ring`、`simp`、`field_simp`、`norm_num` |

两种引用同样可靠，最终都追溯到 Lean 的基本公理；区别只在于读者能否直接看到用了哪些已知结果。用 `simp?` 可以列出 `simp` 实际调用的引理，把隐式引用变成显式。

## 读懂 Lean 代码与 InfoView

初次接触 Lean 的读者，可以先读本节，再读例题。这里只解释本栏目用到的写法；系统学习请读下文推荐的教材。

### 一条定理的写法

```lean
theorem nonneg (θ : ℝ) :
    0 ≤ 3 + 4 * Real.cos θ + Real.cos (2 * θ) := by
  rw [identity]
  have hSquare : 0 ≤ (1 + Real.cos θ) ^ 2 := sq_nonneg _
  exact mul_nonneg (by norm_num) hSquare
```

逐段读：

| 部分 | 含义 |
|---|---|
| `theorem nonneg` | 声明一条定理，名字叫 `nonneg`，以后可以用这个名字引用它 |
| `(θ : ℝ)` | 参数：θ 是一个实数。冒号左边是名字，右边是它所属的类型 |
| `:` 后到 `:=` 前 | 定理的陈述，即要证明的命题 |
| `:= by` | 下面开始证明；`by` 表示用一行行**策略**（tactic）逐步完成证明 |
| `rw [identity]` 等 | 每行一个策略，各自把待证目标往前推进一步，直到没有剩余目标 |

其他常见写法：

- `example : 陈述 := 证明`：不起名字的定理，只用来演示。
- `def 名字 … := …`：定义一个函数或命题；`noncomputable def` 表示这个定义只用于证明，不能直接运行求值（例如用到实数的对数）。
- `:= 定理名 参数`（不写 `by`）：直接给出证明。例如 `:= Complex.Gamma_zero` 表示“这正是 mathlib 中的定理 `Complex.Gamma_zero`”。
- `:= Iff.rfl`：两边按定义展开后完全相同，所以 “↔” 成立。
- `-- …` 是单行注释，`/-- … -/` 是写在定义或定理前面的说明，`/-! … -/` 是一节的说明。注释不参与检查。
- `namespace A … end A`：把其中的名字放在 `A.` 之下，避免与 mathlib 中的名字冲突。
- `open Complex`：之后可以把 `Complex.cos` 简写为 `cos`。

### 常见记号

| 记号 | 读作 | 例子 |
|---|---|---|
| `ℕ` `ℤ` `ℝ` `ℂ` | 自然数（含 0）、整数、实数、复数 | `(n : ℕ)` |
| `(2 : ℕ)` | 把 2 指定为自然数。同一个 2 作为自然数和作为实数，在 Lean 中是不同类型的对象 | `(2 : ℕ) - 3 = 0` |
| `↑n` 或 `(n : ℝ)` | 把自然数 n 看作实数（类型转换）。InfoView 中常显示为 `↑n` | |
| `f x` | 函数 f 在 x 处的值；不加括号 | `riemannZeta s` 即 ζ(s) |
| `s.re` | 复数 s 的实部 | `0 < s.re` |
| `P → Q` | 若 P 则 Q | |
| `P ↔ Q` | P 当且仅当 Q | |
| `∀ x, P x` / `∃ x, P x` | 对一切 x / 存在 x | |
| `¬P`、`P ∧ Q`、`P ∨ Q` | 非 P、P 且 Q、P 或 Q | |
| `a ≠ b` | a 不等于 b，即 `¬(a = b)` | |
| `range n` | 集合 {0, 1, …, n−1} | |
| `∑ k ∈ range n, a k` | Σ_{k=0}^{n−1} a(k) | |
| `fun x => …` | 函数 x ↦ … | |
| `⟨a, b⟩` | 把两部分组成一个整体，例如“存在 x”的证明由 x 和 x 满足的性质组成 | |

`s ≠ 1 → s.re = 1 / 2` 这样连写的箭头，读作“若 s ≠ 1，则 Re s = 1/2”；多个箭头连写，前面的都是条件，最后一个是结论。

### InfoView：每一步的证明状态

在 VS Code 中把光标放在 `by` 之后的某一行，右侧 InfoView 的 **Tactic state** 显示此时的证明状态，例如：

```
θ : ℝ
hSquare : 0 ≤ (1 + Real.cos θ) ^ 2
⊢ 0 ≤ 2 * (1 + Real.cos θ) ^ 2
```

- `⊢` 上面的每一行是**已知条件**：`名字 : 内容`。这里 θ 是一个实数，`hSquare` 是已经证明的不等式。
- `⊢` 后面是**待证目标**。上例是 `0 ≤ 3 + 4 cos θ + cos 2θ` 经恒等式改写后的样子。
- 若有几个目标，会显示 `2 goals`，并依次列出；证明中 `·` 开头的一段专门处理其中一个目标。
- 目标全部完成时显示 `No goals`。
- 名字带 `✝` 的条件（如 `x✝`）是证明中没有起名字的条件，不能直接引用，但仍然成立。
- `↑n` 表示把自然数 n 看作实数或复数。

光标放在一行的末尾，显示的是这一行执行之后的状态；放在行首，是执行之前的状态。读证明时，逐行移动光标，比较每一行执行前后目标怎样变化，就能看懂这一行做了什么。这比只读代码容易得多。

光标停在一个表达式（例如定理名或某个参数）上时，InfoView 还会显示 **Expected type**：这个表达式应当证明的命题。例如光标停在 `exact mul_nonneg (by norm_num) hSquare` 的 `hSquare` 上，Expected type 显示 `⊢ 0 ≤ (1 + Real.cos θ) ^ 2`，即 `mul_nonneg` 的第二个参数所需的命题，而 `hSquare` 正是它。

InfoView 下方的 **Messages** 显示检查结果和 `#print`、`#check` 等命令的输出。一条定理全部检查通过时，显示 `Goals accomplished!`，代码左侧行号旁出现勾号。红色波浪线是错误，黄色是警告（例如证明中有 `sorry`），蓝色是普通信息（例如 `#print axioms` 的输出）。

### 常用策略

| 策略 | 作用 |
|---|---|
| `intro h` | 目标是“若 P 则 Q”或“对一切 x”时，把 P（或 x）移到已知条件中，记作 h |
| `exact e` | e 恰好就是目标的证明，目标完成 |
| `apply t` | 定理 t 的结论与目标相符；剩下要证的是 t 的前提 |
| `have h : P := …` | 先证明一个中间结论 P，记作 h，供后面使用 |
| `rw [t]` | 用等式 t 把目标中的左边换成右边；`rw [← t]` 反向替换；`rw [t] at h` 改写已知条件 h |
| `unfold f` | 把 f 按定义展开 |
| `simp` | 用 mathlib 中标记为化简规则的大量引理反复化简；`simp [h]` 额外使用 h；`simp at h` 化简已知条件 h |
| `norm_num` | 数值计算与化简，例如 2 + 2 = 4、97 是素数 |
| `ring` | 证明多项式（交换环中的）恒等式 |
| `field_simp` | 消去分母；分母不为零的条件需要已知 |
| `linarith` | 由已知的线性不等式推出目标中的线性不等式 |
| `linear_combination e` | 目标等式等于已知等式按 e 给出的线性组合，余下的恒等式由 `ring` 检查 |
| `omega` | 整数、自然数的线性算术 |
| `constructor` | 把“P 且 Q”或“P 当且仅当 Q”拆成两个目标 |
| `obtain ⟨x, hx⟩ := h` | 已知“存在 x 使 …”时，取出这个 x 和它满足的性质 |
| `rintro rfl` | 引入一个等式 x = a，并立即把 x 全部替换为 a |
| `by_contra h` | 反证法：假设目标不成立，记作 h，推出矛盾 |
| `push_neg` | 把“非”推到里面，例如 ¬(a < b) 变成 b ≤ a |
| `induction n with …` | 对自然数 n 归纳，分别处理 `zero`（n = 0）和 `succ`（n → n+1） |
| `calc` | 写一串等式或不等式 a = b ≤ c = d，每一步单独给理由 |
| `exact_mod_cast`、`push_cast` | 处理自然数、整数、实数、复数之间的类型转换 |
| `fun_prop` | 由组成部分推出函数的可微、连续等性质 |
| `decide` | 对可以有限检验的命题，直接计算判定真假 |

### 公理：`#print axioms` 的输出

`#print axioms 定理名` 列出一条定理最终依赖的全部公理。它沿着证明所用的定义和引理一直追到底，所以即使证明本身只是计算，也会列出 mathlib 中那些定义和引理所依赖的公理。

本栏目会遇到以下几条：

| 公理 | 含义 | 说明 |
|---|---|---|
| `propext` | 命题外延性：P ↔ Q 时 P = Q | Lean 的三条标准公理之一 |
| `Quot.sound` | 商的可靠性：等价的元素，其等价类相等 | 标准公理之一；构造商集（如模 n 剩余类）时需要，Lean 由它推出“在每一点取值相同的两个函数相等” |
| `Classical.choice` | 选择公理：已知集合非空，就可以从中取出一个元素 | 标准公理之一；由它可推出排中律，即可以使用反证法 |
| `Lean.ofReduceBool` | 承认编译执行得到的结果 | 只在使用 `native_decide` 时出现：计算由编译后的机器码完成，没有经内核检查，因此要额外信任编译器与运行时 |
| `sorryAx` | 用 `sorry` 跳过的步骤 | 出现它说明证明不完整 |

三条标准公理大致对应普通数学默认使用的公理（含选择公理），几乎所有基于 mathlib 的证明都依赖它们。只依赖这三条，说明证明没有额外的假设；出现其他条目时，就要弄清它代表什么。例题 1 和收尾一节演示了这一检查。

## 在浏览器中运行

不安装 Lean 也可以运行这些例题：点表格中的“运行”，代码会载入 Lean 官方的在线编辑器 [live.lean-lang.org](https://live.lean-lang.org)，右侧就是 InfoView，光标移到哪一行就显示那里的证明状态（读法见上文）。第一次打开要加载 mathlib，需等待片刻。

在线编辑器使用最新版的 Lean 与 mathlib，与本目录固定的版本不同，结果可能有以下差别（表中的上标数字对应下列各条；2026 年 11 月 16 日在 Lean v4.36.0-rc2 下逐一核对）：

1. `native_decide` 证明所依赖的附加公理，新版显示为 `…native_decide.ax_1_1` 一类的名称，而不是 `Lean.ofReduceBool`；含义相同，都表示信任编译执行的结果。
2. 例题 5、例题 6 和附表用到的 mathlib 名称或记号在新版中已经改动（模块改名、引理改名、ζ 与 μ 的记号改变作用域），在线运行会报错，因此不给链接。这几例须在本机按本目录固定的版本运行，自动检查保证它们在该版本下通过。
3. 例题 8 与收尾一节引用了其他例题，在线版把所引用的例题依次并入同一个文件，行号与本目录中的文件不同。例题 8 在新版中另有两条提示：`push_neg` 已改名为 `push Not`，不影响证明。

链接直接读取仓库 main 分支中的文件，文件更新后链接打开的就是新内容（并入其他例题的两个在线版除外）。

## 四个阶段与八道例题

| 阶段 | 例题 | 本书出处 | 要点 | 在线运行 |
|---|---|---|---|---|
| **1 认识形式化陈述** | [π(100) = 25 的三种核验](BookExamples/S1a_PrimeCount.lean) | 第 1、2 章 | 内核计算与编译执行的信任范围不同 | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FBookExamples%2FS1a_PrimeCount.lean)¹ |
| | [黎曼猜想的 Lean 陈述](BookExamples/S1b_RHStatement.lean) | 第 11 章 | 读懂形式化陈述；mathlib 的约定值 | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FBookExamples%2FS1b_RHStatement.lean) |
| **2 推理自己写** | [有限 Abel 分部求和公式](BookExamples/S2a_AbelSummation.lean) | 附录 B | 归纳法；只用最基本的运算规则 | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FBookExamples%2FS2a_AbelSummation.lean) |
| | [3–4–1 不等式](BookExamples/S2b_ThreeFourOne.lean) | 第 9 章、附录 F | 三角恒等式与非负性 | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FBookExamples%2FS2b_ThreeFourOne.lean) |
| **3 部分显式引用** | [von Mangoldt 恒等式与 Möbius 反演](BookExamples/S3a_VonMangoldt.lean) | 第 2 章、附录 A | 引用一般结果，主线自己推 | —² |
| | [Chebyshev 上界 θ(n) ≤ n log 4](BookExamples/S3b_Chebyshev.lean) | 第 2 章 | 引用组合估计，分析步骤自己写 | —² |
| **4 全部显式引用** | [ξ 函数](BookExamples/S4a_Xi.lean)：整函数、对称、ξ(0)=ξ(1)=½、临界带内零点与 ζ 一致 | 第 10 章 | 库的约定迫使改用 Λ₀ 定义 ξ | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FBookExamples%2FS4a_Xi.lean) |
| | [非平凡零点位于开临界带](BookExamples/S4b_CriticalStrip.lean)，并证明两种黎曼猜想陈述等价 | 第 9–11 章 | 由函数方程拼接三块已知结果 | [运行](https://live.lean-lang.org/#codez=JYWwDg9gTgLgBAWQIYwBYBtgCMB0A5AVxCwFMoAVVE6ATxwBkBlM4EgZxwCVWQkA7PgC0SMJAChQkWIhQZs%2BIqQpVaDZlFYc8EPgDd%2BwNqmB8A5hPDR4yNJlwBBPknQ02hnIzAkAxsGcAxAj5vGGAdDnINUx0IEBENbxwAYViwdBIADzExAFocuEAKdUB%2Bv0AJJ0Asf8Aac0Bo%2BUBUfUAKV0AwuUA3RUA1uSrADIzAGH%2FATfjAGcTAKKNAYO1AG7lAELdAUMVATu1AXPlAQmtANz1AU0VAGBVAADlAKjlAcNNAN7lAIAZsvLgAXhOTuEBTuUBoOUAuOThGAEYsAH1OAAlGURgSOL4YHHT%2BMdTkcxAB6HIAQjEAGI4IAabzg9zggDY0wCt1nAAO1wDpwABMZUAc3mAH7NADjOgGeDUZwegkQGACTTAA%2FxgAh%2FiqAMzkEfckYADr0AkP%2FZaqAWDlAIPRgDgzQANpqNAFnagDAXTqAK%2BVAGbagAM5QBwBoB2C0A39GrQCG5oAjfUA8PqANGUGZ15oAS6MAY9FwXi2bBwUaAA8UtYAyvwl%2BxhsJZgFo5UYM7KANuAABRsACUdsAeumAZz1AIeKgDe0wCdDp1AM7KgBY5QAyroAyPTgAAY4AAeOCcEhwNh5xFwcajeOdQB52oALhMAvwmASW9AHFyiNBuLd0Nh1rkWDg3t9Yh7djtcAABtxvvw%2BK8aJA0OxDGO4IAEBMAnhnqwBfioB6MzKgE%2FtVaAcCVALCagAdTYudQCnQWJ7jg4IGQ8ds50xLi7yX%2Bdvo%2FG4IAkIlxAA0f4ACxAb%2BABsQGAGQEjL8oAGtoFIAV4GAGyO558HAgD%2B8sWT7%2FgGfAANT3MG3IvgAzO%2BcCAAZEiIvmIgCYSgWRYlkcbYdtklyAEbpcIbOOmRIOA6TLkMgCZioACEZUjS6GAMdygCAHmU2RwHAgAARNhABccCAECEQEaFOAjCKI2EsTmgBJhHAAYADWAMBEcDoepgCohEBzFwDkuJwAAVGZ6H4YiwahqZJbUUi%2Fk4FARYsUioJ4tkK7rIAZN6AO%2FKe6AOaOZRjipJbqVpy7boAOAQHie55sIAuASANj%2FY46bwekiEgxbZfeQbBiVYhjsZ2U5ZeUFQXRnVFZ09rrOOrVwIAe%2FHCYAb6adIAskocaM9bblq2ydIAAOaAHAqqxrtugDLfoAXdFNWOVk2XA9nQW18FIahh0YT1nQoWhcCAHNy2ZwIAAPqANOanSAAJG5x%2FrieGEaGgBryoAsgk%2FWBoF%2FpBcBQXtHChXVJajHWbqACRygCgAcJgCrNvyyxlF6dQ5QUabpuMRWANxKgDcrpGsYJsOtr45%2B35xmT5P7CM26AGQqjaAO9ynSAADpgCBkYAp%2B6AMoJOVE4AaJqyoAkOaM713SAMbW24IsBKKojiAAccD8yKow7fsBSAMUJgDScpNPTI1qDKytumOAB9ugCL8aMyPrIAvirtPsOSgtkThxGwYBIN4RYAEIQBAADWACiGT8Wk7DZOC%2BS032Pr0oAkMYSoAknKAKo6z0rYAjDrboAUHIceuW4TJM%2BxjnxAkkNl%2FKAO6xgCwKoA6tqSlKZWACmEy7qoAOvI5YAyvqAChygCjcn3RW7CK44AJIAGbTyF0%2FoMuoyAPCGgC4BruYjI4AnfFp1nOeADHagAWijbyyfd97dwKJgDTXp0%2FIC4A33KAKrygAVxlK%2BzUoCgClxoA68rdKsgAyEZ0XOgA7D1NA0Iuox1yAGPI9UgA4OStLIEckp06rEAC%2BBuxnKeyrjHI6BYeDTlnPOKgbgSztzEIpRS6VcFaTgBVac%2BkapORMmZA6tk4AOUMs5VyHk8JwG8kRPy2FApwGCqFJ8EU8RHRBIpGec8oALzjocL0ycyhEwrPGOsTZWz3HbBXAAJiQaey5ACbfhsPcgBDGMbk3Mqbxg5h1wQABSgBAMAy5AAWEYALk9Bjbg2K7RkTiXEkWaqpI4y4VocW3N0F27Qy67Azr49o8x%2BQthFIMQkpIySAGfAwAU3KACpzQA1REigwR7MQBjp4FleHY0OjjnFgCkeQ5SalNLaXwVVAyTCRFPXzLDIsoiiz5iCsWEKYUyyRVxIoiEcAuwIJtEnF02QP7oW9IAX8VTwFEAPPWqw4z1kAKP6gBvDKloAHgVOiAAO1QAJtannlAXHKgAD0wzkVUYgAGdUAJ2mgAseXyYAEciJQbEOfsQAoGnqn1EaekE19ki26IAbLkXS7E4oAbbUBqVyjtXZcgAQFUACj2HjtTFM9mCQ41ZTyABM084MYvm3CzLsMcAYkTqUALiEwZlyAHBjCUfRKRIm3Pi8ewpAAlcsYg0gAA70AGregBTV3HG4cAY5sViGwekXBVLcF0rgJFHMRkpFwCwDQYskhFH5FuoAecUsabkAA3OgB8WNPGUVyv44CkTgKS7MFKAyuXsvSuATLJHbluk1S8YlxwOtwYAEkJQz5FImOTom1AA55vnQALqbnl%2FPcClBjfAGOXIAF7dP6AELowA6d6ABIlV0mCpVIpwepX1TrnJWqfDmEJaqNUJuAAY7VcBADJwIUQAgeZxieoAEE1bXkr6PyYS451UhtTcYzcMzez9lbs1FI1cMg4AAOL8V4E8AAXmQCAIbBhl0AA4GgBfTXzlExsepJXSqLOpKdMcZ3zpALwJ6KrK1nvSBehdSBl2rvrX6FtbanJInbYAfTkpYbBdMcwAMAEDyiYcz8dqxDnNHSOBk3oFpCLLNWQAomkF0AFiagBNeRKsJAugxOgYQZPyaYgA1WObNC7IIpU31Bg7aaU446FtOfXwEgL7nFPAgNPdjzGnjpCeHDeS7UyyABMiRiF4GIPlDNRLMY8hh1FbF%2Bvm%2FNAALxoAbPkENIhE4WGiYhAA3RvFb0%2FaNVitcXAEUUSFq7ETnaboWppTDU4UiH9gBQZR0wUcYL5AAv0aMRWgH%2BTXBjEegtMr1IMaENVMsUn6mKVCwwp43GV1sY41xljvGxEBnVZq8AwZsgkD4HouAVTI7R3SGwA4%2BRgQsSuNcaodxgLPCSBoUI3hnAfA0GAf4kkgSnFxVCWEytVaYmxO0OA6syhU3jIAWXlmzPSJsyNkcAACcgBkAg5HAHk2QvRwkADFytZABgSrrbaRtVhlHfZWOMBLGagxAmBSGUE4Di06PWAoM2MxdNEyWAZ5Z9jVH6IASDlADq6oAJ91BbhsAD9Gn866AFNzVJ8lbzvbgIAUyIyxjXqo%2BKTjIrPSk6HuQAKXqbcW2t0YNz4wim5E1N88ORM5gmnUVZzzADQXv0bCgBv%2F0AAxKZZLVsEZIWOVnPQxI%2FuCRQ2vR7yAEAGBtouGWnhOYABW16x%2BZjC%2BChspACWSnAbwEA2ABkAAPAVLfwhnbKGIynRACMrmcqBI6SyykAL8BX5qZNXInAQAECpQ86ONuMNvAC8IQUN7WmPuIjdN3a4z9tqdBFDiVy3pkaAFnPYk5IGTczKFZykE5WkzjnBABcJCxxiEZPTO38Zmbclgco8ctiQ6hzHHngmaii%2BdlhNUQAfGZ6nqJSTHUpsgAB84DSgbnAbvlypj97EJ3vIORR95E7yP%2BjafYvxdXexzjOgUssbhv3%2BHAu4Ao4k1RJ6U%2Fu%2FlVn9VZLTw2AECwMubvdP6f1XuPro3eIHXa%2BDAAPQDPfxtDV1ea512wQ3qPQx98Z9dIwtRBWM1119AwswH9Y12xh8D971Mg50n04sWMEsIDu8Pxtwwx5Zo0UcG0v9IsgCxxECZ1vBIAAB3VA8Ap4YAWeS%2FOAM8QAIT1H4xoFd4DxxSCcANc2AngSAABHGgugoxdfHguAQADuBy04BB4R4JCnwHVQ5%2Fptc4Cp93Q4BDlAB0%2FUAAubZeUYLZbIKzODUYBDAKMsAoPoQAQpspY6hWck9EFbRjFb9QwvlRhfN%2FMXxD8QC580CF8ktl8eNV8a44BAdAB5v0ADDIwANbcHNdhuhtwXRABHfUAFmVEUQAMb9AAgoNGEAAnlVYKod2HFFxXLOAUgsQAo9CNgDXLwfLQsZwL2fidgP2AOArCvIrauDgBrYAJrFrGANretbiQAU2syhLwACpCB5KdnwGISwC84xJUFxoBvg4BujgBdA%2FB0BF8%2BMWM%2BAdBIASwABvDKTSAAXzMlQCXVwRi3CyYVDADFQDEXUh6TgCp1DFUgaUUmsjYQ4Schcnck8j4R8lVXVQaUOEAAbohzP8OACgzoBiLTCgxHAPQE%2FIMcCALAUQEwOAQAC%2FIKDtIF5ABL8lwWskxNBPyBhMrSgjHDKEAAlFEUHKBCcEzCUEy1CgoqRkAGWk8KMEtgIJRSQ4QAWMUAZNwolwSTQ6h6MF4hIFpAAYlUADu3QAcAsDMSxD5axAB%2Fs0ACNjW4JEBk%2FYRSJElE9CDErE9AXE9SfExycRUtYkliNEpEfINgICDLDQMwbEhpVAJAXQIsVACg244TcE4Zf4mgF45yfIG4osQAfOVbged1TwTQwqcSoU5GIAwapLUsAH8tMEzRMsBRctMkQ2TABOU29QjOhIeMgwoVoRhIAG0z9nhQogJ%2FDQoABdOAFAOAIM%2F0w4E3IoQAcgNkk9QOdRMYSqc4Bn4R0NNezNSKFMAnBGtUB4TaTAoyh2YJjy1OggN6poCcIdFXIpNRznTXSmyKDqUZyyxK0ATizDhABZ5UFDKEAHEFQAPujWSaJ5gpJFhRzosTBuiIBaEFFiyoAyyKzT8SB0Bp4WkvDj90D6zGyTj%2FTNioAQA4siAGz4AIKuSiS4BPwcDo1GQN06xYTBctyXS3SKC2EVJ3igIYTqIchbIWJjyKEzyLz74AZbobJOgby7zfw%2BBGQgTu4mySIoSiwYSWJWLCysxOh4ECzN9ABt90AD%2B3Z8uAV85xQ6Kcr8ss1AICZjUwdYlSlAJIJANgGAdYsChCj0kgf07ck9MyCtOABVETCiuAPAFAbg7S3SzYgQEgUwGyf08cpASc6c6%2FMoZVW%2FMEigh%2FVyJ%2FV%2Fd%2FQKz%2FcKngnXCg%2F%2FQMQK0cw4TwyqUA59fwis5cAWJ2BaMoGE1C3A08Rkd0vgbkUXUixEQqvc7kXCnc1AaeE9Fic4sAtK8%2FXc9Cd0%2B4ac4Hfyhkh%2FLMQqpdEiR86%2FQAM90t5Rzvy4BSyTj9Kmy6qnS8Kmy%2FRiTaEj8DIyqK0GrVqmMfDEsl9uNUt8LQp5qaqm11JL1r11rVVzrtrwDWrjq3TtdZVHrMpJMnpK0ONqjVj59nEcBwAoBGJnAcAwBgBqD0D7qmzKDZVuEzJnrNJfI4AX8zIchwrIsQl%2FTyCIAqDvqIBaDZ5fqwB%2FqAwAB5KAHAEwdAMyEAAgL6na98mACgnG7Gps5%2FbLJCuAJoDDWXeXdwr6b%2FLXbXGK3EXq6qt0sQ9SMQnXb4mEsZXq30lshE2qkgHANgGgK9ISA9bePcQAYBiyhAANOUAHvPctaSkypsja2apWlWq9eW8cKm1YgQ8Askg2%2FzGQvuQABfN1hZd%2FNdhuS6hgdRgcoFcioYpAAk4wJSV2ovyFVz5uiv%2FyMmkuMzgB0BcEmttr4MEPQKAlQCWszobUzsoKAnpsZtpurKgCeGnmcDYBICAnLvQErvYygBmtQCzH9L4hCFNunKioFtjqekHLvNxGqX4QSoRJ4LTqEPoLKDEMkJVRdoQmjTgGqSwinrMn7t%2BKImUI7D5IFNDlHO1KQFRLRNDkztDkNJYhHvtvQNxrnnACbJ4PBvdOqXUj4skQ8gHsPMor9OLJNtQEdRhuoVDB4RhPyF9RftXvhtvXfrgHHJpFLo12IBMBQDCHQmhtQFDmtqdsV12xj0AFGDHUMoR6oyRkeBVAR6yS7kQANCNaTLUFDQGjb%2FSoBmtK6SxU7z7V18amzXIKCOjUAmz18FKKEsRW74AkAsAz8oB8tuHiH%2FSsQoHPKnhYGsB4HQgdAmzpyxwKydKhJaSFSVTbgV7B6Gl1GDLUG2bmxtxOF%2FxQ4SoTcxicwND57YShLrHTDbH7HNy77Q4swAByXBHMETB%2B9%2B4yha1Aa1ItfcjSQNZe741%2BoieQgML4kB9SANP%2B30uAMAAgIwORhygAbhWrMDoaUtIiAlfK0p0r0vgqbKOs%2FqCZVnUnifsf7KPI1UEaeBAAgD0UyZ0oqaMpPIRNiBcqQGXHbSlGjVGA7IzUAHpzMoaxixwSuAOx3x%2Be6Svp0wcQRSL%2B0OZjXBapVGgJr82S98%2BRdAf0hO8Cvc6clk9CFiapS1e4JMcx36LyHyIerWQUakn3PgXqcqQxEwIsNEgMapfIIiHAGACAWymAICAAfieGxJMRHUufsZucZANGuFuk5IDPHCheyhV0uG1lGAPXud4X4WDHGu%2Bc2b%2BYBZ8mBdBZQEhehbvrYQDEZYpaBZBbBdwTsieLgCSaudLWpRYknl%2BCpbBbWKctUrMgy2WaQFZqbKCb4CSFlSZd5eDCFcbJLRevkIfrht5ZSeadafaYYYQr4AaQmqmrldrONZMHMFxXyG2wGPdyexe0zBzHzD91LCRHGBmJUFChACtG%2BDkca2AGa3QFa2ADqT2OoSOOuNOJCy2s4WgP9OuN%2BFwVYXZZNJYjqcJZ8k5edaGTEUAHIiXN%2FpN%2BqtacmU3KHN110Y11gZT5jXPgHSqAAgEIaAZcQAMaNRInYZTRy62G2m2QWoAGksQaKrzbzzIAwK2mJgxOgxw0mMnVLlxkWbHpLWz%2BjOhJjGZhKENUBfhGQsDGZuRJLpL1U5GdBuiao%2BHFJZ3UBUDXLwKW6o427t34AAxFjljnA1jQo4stjNcmzTjUBpWh38hzyR24Ax3q2fI7nhy%2Fddgzlt9CDnwiHTjD3%2FTj262z2VHiyr2b3ymL24BBGVrgKwDsa1j%2FCDqeGILrWBzto7DZk7Q48yQGQS8Bx6RuZPXqBvWCPkrCFM9iFDBL6ngsAK9cFJwuOM8s9DA4AL5y97FGmGke3ui%2B3oBB30XDD6Q4BAAlwjgC9AZFUQzHUTjAZmpk6B%2FQgy%2FWXcDLgDMdU8ZCDxvLJ25JqEWGwiY4ZFGF%2B3WAs39P2Z4ZLBONNqbI6p6bgGFO4d7tdfCnbE6EAA345TFTHh0YQAM%2BUsrFoRhRJrgnZRQZT5Igu937dTC41%2FSkAwA0gNVuHfOl0pH0WhinJcJHmiJIT4d8whL4EJ3ixCqswD2pL%2FSXzfg5K0S%2BB9THTiy1nZXZVzLLLDpK0wX7LSnRWXK3LhvMs6lwLm7FuPKvLizAO4BqvxEGvwuaIRKmI3XCrBdkPFv7S3yPyjnFuTmELAvBslFPQGQNOaM%2BwdOTdbW3dGYns1FzO4ATDd8kQ6h%2BRWdOhhSxwnhlxHOgN65m5GQBXp4IAAA1VgGEz0RvDxW4DIQAXHIqqvPev3yyvf2myk2nh%2FTd796m7M77gT7fWYLvAA2g2Q26k%2FOn373%2FYELsJWecxUAOqpU8smiw4WiY42jGeuieigA%3D%3D%3D)³ |
| **收尾** | [怎样检查一个形式化证明](BookExamples/S5_Checking.lean) | 综合 | 证明是否完整、依赖哪些公理、陈述是否忠实 | [运行](https://live.lean-lang.org/#codez=JYWwDg9gTgLgBAWQIYwBYBtgCMB0A5AVxCwFMoAVVE6ATxwAUpQSBhCAgOxmA4HMAoUJFiIUGbDnJIAxt2n5oIQiAZMQJQeGjxkaTLmWkKVWjgAyAZTLASAZxwAlGyCQcOALRIwkm4TrH6%2BERGlNRQdJbWdgocAG6uwLaoPAL8ALRpcIAU6oD9foASToBY%2F4A05oDR8oCo%2BoAUroBhcoBuioBrciWAGRmAMP%2BAm%2FGAM4mAUUaAwdqAN3KAIW6AoYqAndqAufKAhNaAbnqApoqAMCqAAHKAVHKA4aaAb3KAQAz86ZkAvHt7cICncoDQcoBccnAWAIxIAPqMzGycMDjoJK5w%2B3v8APRpAIT8ADEcEANN5wS5wQBsaYBW6zgAHa4E1wQVAAPAAApLgAGTEASg%2BcAATABWQAQ%2F0VAGZyYMugEAGAlwQAHXoBIf625MAtHKATb9AF%2BKgAJfQAOpoBC6N5gF%2FFXlwdEADzx%2FV5gB4FQAWEc0aqyxRjsXidoSietShVAJBygFnPQCdpoB4fUAldFwMxvDhwQAcFoAYrNa80A0XKAPO1mvxAPgKgBNrQAl0YAx6MARvrGwBoyoAJNMAD%2FH9QCZioBVm2ah0AU8qAHAJ%2BYB070A%2BnKAX4DADryp0Ag9GAODNALgEgDfTQApeoBlfUAh%2FKAb7lAANygAk5TZA4FBsPhrYuPTYODK9EcPFR7NwAAGeBQODAalY7C4KTgHBHzUAWdqASTlToBYOUAobGAcfiF3B%2BnzFrzmoA4OTZ80AL4GbY6AI3T%2BsvAGAuWzgcDQYRIIDgU4es%2B4fBuLFMRuABrMgOBIdA4AALjgcdnh%2FdRHjnPhwWxfFiRgjUsBofhX1fAATEhpGAIi4AAajAqAIPQLZAAQE6FAG%2Fo7MCifQBYFXOEdEJnJ4UkA7FQPAyCR0AbH%2FACTFQB35UAOBVAHozCMVSA9VNRE%2FgR2g7CaBHOBAGk5WTCzadpACvlQBIc3mQAZCMANW9AFNXUciJIsjKKE9AR2bQFgQNe0TS2S4cFs4jSJICiqJokcCkARlcLStA9BhtOjFkAAYs7TgTE4EABiU0JSmTADIVU4%2BUmQVmkAdP10uJTZ8JimTIveVlAAj9QB4HX6eZoUAaC9AHi9ZpAHxYwBiWMAAHNAAm%2FeLAFPzeZAHAlfSZJ6wB15VrfpAAuEwAwJTK18YsALQV%2BkAeet5kAU2s00AX4TAEhjKrrX6QBuBMARPjABHIwBMJSG5o0yKQBquMARh1ABDzQAEI0LTYCV8kcOBQYBYhIG47IC0LAAlFToFkWQASJWXNrADR%2FQBF6LewAuc0ACzVAEAPZosjTFHACg5QAXt0AUuNAAX4syitSpNAHx3IslrgQB8BMAMr1AGv9QrACxNZpADF5Mmd2awBCm2MwB5vx3GLbstd5DJkwB%2FIx9VpFjJwBlv0AHPM6cAA7UvUAAHTAEDIwBcjMANE1ayTJG0dPMmSwFwBMVMAe%2Bjaf4ABmH6OEUG4OCIULAE%2FtQBVZWPLlAHvlMLRbtQ9AHIDQsSRKQAgzTgABOAB2OAZL5Rlmg3QBR%2FTiwVXOBQA4A0AdgtAGh3TlADvdQBqJQKEdAR%2FLg4CQcVgAgEBbBHLY1kAanNAD4dfpR0rphq9r%2BvG7gditMAdCVOVaQBDcyffrRkANVj%2BkAC0VZsAG0VH3WbpAH6bQABd0LCpUofVdABiVMpn3mAnAF%2F41LAFS9ZpAAEjQ5AGdlQB%2FeULSW02adNACx5Me4C7cQsF7IAYoTADZcmuY%2Bj5b5z36KvTYWQ4AADULBwDYGRVknRACSioAcAtAB8plkR05MACSHAABmEB4E2AAO4HkQHYWwSBeB2F7IAPjNABcnoAZPjOQiQAOLABgAACQIAAwAV4GAAqlIa%2FQXqAC%2B9QADdGAFV9Vk6ZjLNkALJK8x9SFn6BwmSL44AAHIABCEAIAgQAKLiiQOAV49h7hIT%2FJOacyF%2Fy8H4sBYKkFdFwCImAEgHACK2DgBAa0%2FcG62FggAbSnBAbx4oYAABpkHoCQLYWwwBpBIHQDgaQqAICpJIPEgAigQCAzxbCzgIgAXS2K0XUE9Kri2OpgwAY4qr2aIAA8VABycrfYygAv9UAHFyv8Ag9n6IWXac8%2BgFC2AAKlHJE6JMARwkkAL4qjQ9aADe9YOjICiABI5RYyzACnQYAJLlAAfboAF1DADUKiSegcBAAphHAfJycnoyShssy5%2BJ7mbGmSOQpxScClM4ARBZgAxVX6L7QABukbIKFkQAC%2BaLEAJLegB3uUAM6KgBvn2OAi%2FoOzADCityZofR%2BgIsAN4%2BRzYVLReoAAgTAWADG08OEdACEVvufogBLJUAJryBLGQli1nvboIl6lwEABvxYVuiAArjTkkLNqAE6HQAa8oyiObMDFiwRTEo%2BaOFgiTkmpPSZk7JuSFmAEgEwAl0ar02YAJ91ACn7ksAlgBo9UAHrpgAvL2aE9X2hxABzcqySVnIljYqWoKp1IrABJxqyQA0fqvMAGhG1q4D0GTumR5gBBRUAB3RT8KiAFnlPMMZmx9EAOSal53ZlkAHZmgAsBN5IAM21AAbeT6RN0DHwkjOQao16xDJz2qRPZogAX6ILIWAW%2Bt%2BiAHEFQAfdHNl%2Bv9QGwN%2FJES0pozkbMPUTwmXhTxJBvG%2BP8YEmudcQnhNmSQGJ8TVVJJSWkjJWScnSDyUdHAEBiEOBIARAgJ7DEQHQAUopJSymVNUvU89l7r23pIPe5yB5ADwhoAXAMZIFCRoAcyMzJy1hm1Yqb4oAEBIA6mW3RAB2Hi6c4MAEMkE2DFAWQ1HTv3vkdOAnRHRbVzKvaRxxACm5uvOR%2FQZJLC7bWZRgAF4wmcbakZtExtVZBUGjgACpXpv0K%2BgAhHRdIABuddqWytpsBWgAu6NlfK%2FStZADAwYAF7UNyzGaBXKu8BgmNy0mR%2BYpcI4uhHlUTkdH%2BCADZTdu8xABBQSSCwRIbgsCoNIECKQXhWkZIAMB0KiOnFW2vOQ0NG%2ByrJpzYaRvhbD%2BuoWwYAZCBXvaY8xljog2J4lwLYvxMiGhjPMAoMU0zrBHCDMdcB3ZOuMoABTTEr9GWcTNMVNu0qRHI5aiwk4CAHBjZcAcbSABjtN6hHUzNHVptLau1hai0GusOAsX%2BDvmgJ%2Bb8Di%2Fx8SAoJbrUFYLwXsb%2BXiqEgIYSJFhOAOE52VcCl1mieWMhwEK4AGLkwOI0g%2BsCMp5CvzCGwvWVzQ36pjCkjKS%2FQ2ojYW0tlbUA1vcUcVtgSf1uCAxgnBCc8PNsnfQhqTC6lLu4VfMjgGQMbsPYKzGXUBRva8hDp9X6ztXYgC0jJWUaZrLum6KcJMccE58iLIAfFc3rzEAL9y%2FtA7DILM0QAMAEbhkhnXkUO4sw7h9OG4vP9sTmyzHeO%2BOrtE8Z0QcnT3KcFEABAqvJZi5ydbDcrAAarSzEkzWqLLpu36Pnja%2BjpcLSD8ecQjl%2Fzkk3v8TxwAOvgjtoyJXy2TCw6%2FE7GANxuLq4hLBd3B2vdp40nOp2UAQAuyN9sOAg184GkLIAEBUhFQJgRgnBWQ7xQvMnjZoRDSHkJIFQruCBaH0MYawjhKlHscP6Gc1cgBByLWIAAH1AAsmv0NtMXMggnMgUEyNSmkwKBPp1dA9%2FGY%2BO847bbjaKPZBM9syBQp1novVem9d6jHoE2D3HgBm12D33yhQ%2FSOh0aFP7qC%2Fp4y%2BZkAOa%2BE8G%2Ba8W%2Bvcr%2Bu%2B62zA6uscWwPiBEcAaWZiFiYAViqgR2uWxenwGoJw5wFgAALLcAABrAC%2BbvB4E%2FD%2FBAighwBEFQiwgIhIixwFCAB9wHACKGSJSGhAyMyPwKUP0EKoAD%2FaS8EUf8%2BgvYxqxkD4j4gAP0ZEzS5vTNBCKACPuoZFGGuKeIAMdyvIgALqYQEthwBsj9CKYsishrhwDsFoi2BKQAC9cAtgthgASESXB4gogAB6AA3i4bYN8ASAAL5wCADJwLYQEXiIAG3AthOIzQkwhYEyPk1hCc%2BhIoKk301hGIfhSkNhdhKkDsmRuI%2BINh7h%2BI9hKkRBvkWQgALHKAAyroAGR6yUcAAAPHAFek4S0eCHAIMM0Jwf0IAG9p4qgADgbnCREHiDFZwDLdgAKsj9A5ruyACGMVMqONIA3BgV4Nek4J%2BK4B4F4EgE4UuNIsOIANnAMR%2BIXhvh%2FhQRoR4RBIURMRzQD8phQ2gA4JrBhwBjFpH8CfKrGZYwCbHOA7GeDeCAABBAcc0EcXAMcSCWcRqKcXYRROCN8P4uREiVkXYY8YABG2gA3co7KACB5uKmDqkbyCpJ8lwhYi4IALiEBx5xPhfhARwRYRVxOIkxpwjYG4xMgA5o5sjLzGhrhbC8qzEihZASq7SpyADeGcZDKOsJIT2FkASR0RqJiNSBCIACCa7IUJcAF0y4VQgAZX7Lgyjuj3x7JWG5EOFOGuGlHwmxFwL%2BJKkqlwCqnFSMZNGAAacvqYafwIAEemcucA9hH8gAB6YxiFjEnBzrBsigpJjOG2BuF4g4manyoElFjFTEkqRwKCltDbRayACcplGG9BUFCWCWuLOq%2BGaWUXALYZaXiNCWcaie4c2E%2BKOHXDcCQAAI5aQJG2lwCAAGRMlA6aqd0OeKyLyVeJMaUEwsaJUF3LKQAk%2BFsAAD5DyPhsRwCLnFojCrn8DzkZBpDbkZDzlbm2TADELEJkA%2BLcBIBYCvA3C%2FHrH%2FEETAlIAglaSLnQkpEiibmLkji3mvD3lbEuBuCPkgk3CBJAy2CCIvmFnolKQ1l2EkgiiGjNSMifkrFrG%2FkAnbGAV7EtntmrlQmwlQUIkuFIn%2BLEWXDfDQUoUjhMCYW7HeAjrEIgWMUQQ3AABeZAEAkF%2FivZKUJYHxBF1pcA3wcA5JIAVJZxB5X5bAmW4oOAolVJLsQM7FUAEATFNwsOyeEATceF7R%2FiAAfE0XxfJUgJSWcTxZufwDUMyltIACVZYUoiwY1kI25cxCnAyeKlYACyvsgAdfobLUjUUpAjj%2BXEI2DoAEQ3ApLgALJ6GGGMjUiqSRWeUkjBiAAB3tHukHFvwFEj4sgmhVuvFhYnYMlieigUYulugZgeQcbqYckSKM0AWW%2BXmVkPoYsIALCagAznq3i7TGRrj9BBgx5OwcC3kEDeBXmBRETEJwB1wVn%2BKwSABAhHiPNVhHOrYXANMqtZkKUdMj%2BRsQRP%2BUCXsWCSieCHiMJQSMbkOWuFeAUNxX2RCCWL0QRY4dGbGfhXYTHirl%2BM2W2TNWjgtRWagClLBLdUUWiKgGnh0b2aUdBHOq%2BNNXaR0etf4ptXiNtXlX%2BYCVhd4B0WdRdvrotpkGDI0i8V0cRSDc0FJLeDifNIALPWpNHRHKFQS0j2Y4JAvyNAYlcA4NxmkNXRuZb0XRvZtgIkI44FWAilbFHFOA4AUAWkEUEIQtcAcGEIZNPZyUS0qASAqO4NHisEGIf1eImQINF2YtEtylEA0tU4FZeAbNtgHNX44NOIc6j2DV%2BIb5ZFyJcAHtlFuZgAd26YKADPyoAJ3xXcxxJIgAVEaAB%2FarMUmLmcokWLHVGFJEWA%2FPgula%2BFAFQmEjtRjbRY%2BThZUq%2BI9oAKo6U%2ByRB8zQ%2FtrIWyQdu0hkZyhZcAp4xkj4xoS0nApCYVU1wAztmQ1NdNtgDpZNtIIk3Qn8WQZqE8qwrIgAfkbpSA1o7G2nhc2XC6300g1LQhWQThWJW91wCMrHCMZsyACeGcaIAEoGsKbdc6vcqQ%2BWcAimyInBMkxJJIzVbVnVeMrVPl0ei2yucea2zZBEx5p5sOc4l5rwaOAAIsA2eWA2NXAHNd3XjYTgTVMf%2FEuQUG%2Bc%2FSKOsBDN0NgoANvxk9qwzQgA2fKjiuUcDuVRJaSJoa1a2BSoBQMwOgMXnwOIM50YUAV0VPkXZAMnmwNsPXmcMPmHVzod0PrIF1x72cERSD2kXgjUiwU4jUiAAceryILK6TGNSIJto4ACZphwhIcAgAI34qF70jiUPUOeVwBhQV4LQ%2BUirJE%2BWb1uWzLG4P0EgcGUUahmnNARRvn9AIXNTEzFQfX%2F1fXAAgUsVi2%2FXzWLVIP61G1KTw3IN72l1rhSTNCABnukHQ3TWSrU4SyeIyQpI93XvQ1WCYE7yIhVBQUwiXCTCQibmUtJnXANnejVwwdaCVE2BYIoXagwfRWXUziPrarWRUpNGV7Sdc0CfefZfS0ykO4wpnAHbF40URqPYWEx%2BBE5LSpWjtNSlBqBCLjXrigyXVPsWTYesxWSlAiGiClOM%2FCFBUUXWadYSM0MvsfecJiMzZkB0BuNrKaoAMoJzzUohprQgAxtYyTZkVNDyrj9CAC%2BmqqUtIlW03XG%2BnfQ%2FasyUQ4Vs6tjs6Bfs8AF0Uc0JUY6c3vbMI%2BI9aURqPrQiLc7U3iK82S3SBsyi0IGi8ABi49gHYAFLKnVbRgU%2BlyUJIt1lwjILeZZGzFpMZpRxlplCJ0RGJTxsxgA%2BcqADTmryXi%2FHt3ThZLdjatXEwDbNU0a0fYLDniGDRDeK4tbDUgwjf4kjYtidWtSJRSSZYjXADRdw4%2BTjeSznkXZkBFLpXAAZSlIVLzZiAUMmqmuVlAXs1AMQv%2Bn2oqU0ZMJ0B0UvIAEbGAtmI7oQbcAvSlUqA%2FigAG8rfOdHtH5ui2csoBc3aU9CpWnDdrNCADb7oAH9u9D2tQNUbqT%2BE3rL%2Bibyb9rqL9bpbe9ob4bcARlHrireIPFJIM5S56dXNDDXNXCaOCrfb%2BOCrZtHFalGlkA%2FiE7hbEUYxcJZL27SagAx5GciakajbsIiRFzqa3a3HFo4iP7VY37EI3btOuDt517EdEUsDutNhI%2BtdO3ATVqUsXm1c2Yj9Ovhb1hURVCB71gwFkjjfW4WZucF5l%2BmyuvXWnNCACxipmx%2B7m%2B62JZ68%2B80D1FJIYS01nThx0QveDfEqgMcf0zfUswwZCnUY0SlK0aG60RCD0dK00RWIAChygAo3IVj8X1Pq2%2F2x7bN6ttm7OqXAOxMINWulu9vCdOE4CWsms2vGeBRid2sDspNKk3KAe%2BvAcI1A2BuoPE2ADbaosEmBuKcP0UWP0FPc0IVrMHjAUIJ4MFG9SOK924w728baB%2FhAmxAN6yOwO2O%2FAPp6%2B%2Bu%2BDYvWrdngTva4l8l7RKl3W%2Bl7YJcJl9ravTl5tWrc504YIvuypZbVACvZV4w5u7BP%2B3Vxdnu3BwexeupUDMew25iHvXh2cQRy9fK3O2ccq28wSMx1y%2Fq%2BxdjSe7YClODf049kmDJ%2FJ0WIAGNGb0OyhogAiCrNAV5YdwgdkFhLSrEcC2BYa3owDQBzoIiPaABLhAUK6YAPeePnMuThkXUzNICrMRtIcAu03n%2FRd8hj83%2BIPz9rQ7SXqAo7Qg%2BxYSgNnHq9nHXC5ScABAKSqEKPr473mQgAC4QFBw%2B2cli%2FdMKABsjj53THAEj1zaj%2BAG06gG%2BkgaVcYmgZlvYFVbgZ8EcGcKUBcG5h5sRN5nwJQdaNQb8ACMCPZgUGFsNIsG2IWFsEmFCk%2BMaoLBr8WK0ASi2nGIAM%2BBgAiDpaxDS6irBOizpJGTKTKFjZRDb6GO8FDGQCxYelJQDhBaSADPsTuLZeVj7374BiBkmORmDBWNmManmK7rDQ3aLdAGH%2F0GsFmPmjuEjIDjJJ%2FFyIAGbRgAUip%2BTSCJJQD%2FQroE%2BMK6Kh80C6JLiw16ZQE74hJaQKKfyciSaji18ACC4oLkRQgAy3KADJev0KIkNJ0EXzH9bDDxuPGt3yn5pF9L5I73PIAFcqwCq87vWHz%2Bfcb%2B%2Fiw8Je%2Bc6w4B2keseynfJc%2FnvtBbr4T0WsgAIPqACgdt0DJI2OsJHMZIAF1ygADxoFhVBJhV4bRPhHADeiABpr1dyCoRUjUEaIpl2ifxAA1REkYiYk0W%2FnAGlzdxt8hmbSp%2FDIwTxV4Y8GzAUUd4RhsogAA%2F0XQvSNVo0Hd68pDIQ0JMGFD7QipFMRYbKBC1QxoCNwQ0PtJmCyizASw4Aj%2BNwMGikC5cgAZ4MtY%2FQQBLskaDrBHQE8QyJmDChf9oYgAWtNmwd4PUIsBKCAAFbUAAo9iwhiyZVsq1oaSusXFAFVEsxVVLGVT57rF7AkvLzIsxoJ%2FA4AbkREMVnUxaY5UOyTXvwCRAQg%2Bwqoa5phAxTqICwimAHJzBryPhtM6wQACvWgAYPi7wWyMyBwhLKwFbEB%2BFxDthogFAIkHlLdHEgSR7oNUh6bVCeifQ%2FI%2Fkvifph%2FicS5DicgMAoZum3SlD1UB6LVMelPQfob836e%2FA%2BmqEvp%2Fkb6ZRDUjqRRR%2Bg4BJZCsnWTUha0j4akMCjBQbJmgOaAtMWjLQVoWk%2FADpF0j6RoMpCkuUZLPD6DlZmhpOUdCQHHSFgr8I4PoV%2Bjvy%2FoH8oUfgGmBByIwwcEON6NSAFiCw5szQOgdLB9DdAzCSsd0OrF1gGwawxsU2GZBLDrAK8%2BAx8P0EABn0YADG%2FG9oACnE8fIEJczXA7gG2J4LL0ZD9BZ8MeSAi%2Fhb6DxUCGWBwVgWyFcBDsTIxoUfichUi9%2BMBOkRVSyzEjmRDQxHMBEuFbBHsuYd2JyQKCsFqEnBEUO7EAAPnsHD3hVAM0gAecSjhPYJ8FzAbSzwSM%2FQdfM0ggKPZfY4%2BAgXKH6CAB%2FVMAC37qeA0SAA%2BtMADIZgGURS4pDIbaQsP1EkRgCsgG%2FbpEUD7TaQ8YT%2BLAfvx57lV%2BeOAcgjgGbKgUIqgiB7G4I8ElBXsSA3lCgOpCAAXZVPCAA5vMAA%2FZoABxncQc6P6ARgtgd4OQi2gKB7IhWHRAyhCGk6KclI%2BbK6DWIRrkVFuaYyaN0GaCvxTIZkTYJzEHJ5jCxzo7ZIsD7QbhfYmYAQeAJJChtAApkRdE%2BKcPHisnH4DOpO2PaXtL6k5A1hAAqvKKZKRj2DRIxBjDlxwavmOWl0RE7Csla6UCEIABMiVsSLUg4%2FsmuqlQbrGOvKw4V6l44vMW0LBVBGxdXdeMvVQB0hYIVPJop23KyXlwKUAAFDY3mDuxjkm45ZCKhrAAZDxxeB%2BqGyOYBFsghYVkIAE4LIoF71SibBPqcAeINICKQE8dO%2F1a1mjghDmtzOenCCfZyg5psiiwNczviGOYBs50cEggAhK5p0g0Qr4nhu%2BLUpfigYP4i8a8CdquD3BwIEoFTjYiAB1bUADzCkE2pAuhAAomkdJ2qgAQ8U5CWwIJo1H1CiEGOxUBUXKBYT8AAAYgRTcKe1valwbIoiR761k4A3kjyRiSVC%2BSE4bTS4LEkAB4RHiDxiNRFgZyQAEPKqon7otH4DlinwhYOAM5P8lKRnJGJTSemEADXykmCCau5eUVuFAQOI6Bdwe%2BCcR3phMd6tU6qr8GSJ0A86CZeQ2bKoIAC8M1qJsCpgQt%2Bgdo8VIABQCQaVVNhS9IZBiU6kI5LgBjTXiwYLuJ8V5DDT5gucGTMZE%2Bj8B84lMA3lUCKkPUtYjECMI9AKBVS3%2BDYZoNNOXpjFjIjYFFM2GXashXeVTRCpVG%2FIdM9qmNHhsBVjFi0lw0o5Ud0EpF313YmEj8lVN6p2SjBKnQasNVGoQMJqv8CAERCghogqpS1QAEmEunBifE0QbqRnaAk5Gl0WEqJNCmXkjoqiSqkky7CxuQqdU2ahFgCgIMgDEFN2hCD1YV0uAM6J1ZrZKGsgeuH9HQA4UCAFfa0KjL%2BpwBMZjE01v9VgggAkZkEIKVTKUhyzkZQU2ai50ezE16aozUmRqFsDRcuaaOfWsa0yBKz8Q6sgnIOz4BpMLmq4AoDk0qiuTKK7klwtBWZa%2BTKKFMrIm7PbolMu6KsyCONyVBdwCmOshElR1sDZMg6FbL2uRWdkkUvJnsj2e9WvpZ1Oee9U8MHUMhFxWp%2FQLqesCInkSgp%2FQfccHEAAUsQs2tn8BuePIiMU4Ol4CAgAA%3D%3D%3D)¹ ³ |

第 2 阶段的“推理自己写”指：不引用 mathlib 中关于所论对象（素数、ζ、Γ 等）的定理，只用最基本的运算规则（如有限和拆出最后一项、二倍角公式）和自动化策略。

每道例题的文件开头列出：书中的结论、mathlib 中的对应对象、显式引用的库定理，以及形式化陈述与书中表述在记号、条件和约定上的差别。不安装 Lean 也可以在 GitHub 上直接阅读。

## 附表：本书其他命题在 mathlib 中的对应

[A_LibraryMap.lean](BookExamples/A_LibraryMap.lean) 把书中另外一些结论与 mathlib 已有的定理逐条对照：先用 Lean 写出书中的陈述，再直接引用库定理完成证明。它不属于四个阶段，供查阅。此文件用到的若干 mathlib 名称与记号在最新版中已有改动，暂不提供在线运行链接²。

| 本书出处 | 结论 | mathlib 定理 |
|---|---|---|
| 第 2 章、附录 A | ∑_{d∣n} μ(d) = [n = 1]；Möbius 反演 | `coe_moebius_mul_coe_zeta`、`sum_eq_iff_sum_smul_moebius_eq` |
| 附录 B | Abel 求和公式（积分形式） | `sum_mul_eq_sub_integral_mul` |
| 第 5 章 | Euler 乘积（Re s > 1） | `riemannZeta_eulerProduct_tprod` |
| 第 7 章 | Γ 的倍元公式、余元公式 | `Complex.Gamma_mul_Gamma_add_half`、`Complex.Gamma_mul_Gamma_one_sub` |
| 第 9 章 | 函数方程；Re s ≥ 1 时 ζ(s) ≠ 0；ζ(1) 的约定值 | `riemannZeta_one_sub`、`riemannZeta_ne_zero_of_one_le_re`、`riemannZeta_one` |
| — | ζ(2) = π²/6；ζ(−1) = −1/12 | `riemannZeta_two`；后者由 `riemannZeta_neg_nat_eq_bernoulli'` 补写 |

## 学习笔记配套例程

以下两例对应配套学习笔记，不是本书正文的命题，放在 [NotesExamples](NotesExamples/) 中，同样经自动检查：

| 文件 | 内容 | 对应 | 在线运行 |
|---|---|---|---|
| [ShiftStableSum.lean](NotesExamples/ShiftStableSum.lean) | 对全部实数序列要求“首项分离”求和规则会产生矛盾 | 学习笔记第 11 篇 | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FNotesExamples%2FShiftStableSum.lean) |
| [Mersenne61.lean](NotesExamples/Mersenne61.lean) | 以 Lucas–Lehmer 计算证书核验 2^61 − 1 的素性 | 学习笔记第 16 篇 | [运行](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FNotesExamples%2FMersenne61.lean) |

## 参考例题：二项式定理的两种证明

这一例不是本书或学习笔记中的命题，供读者对照参考。它用两种方式证明同一条定理

(a + b)ⁿ = ∑_{k=0}^{n} aᵏ bⁿ⁻ᵏ C(n, k)，

放在 [ReferenceExamples](ReferenceExamples/) 中，同样经自动检查：

| 文件 | 做法 | 适用范围 | `#print axioms` 的输出 |
|---|---|---|---|
| [Binomial.lean](ReferenceExamples/Binomial.lean)（125 行） | 不用 mathlib，只用 Lean 核心库：自己递归定义组合数与有限和，证明 6 条辅助引理，再对 n 归纳 | 自然数 | `propext`、`Quot.sound` |
| [BinomialMathlib.lean](ReferenceExamples/BinomialMathlib.lean)（12 行） | 引用 mathlib 的 `add_pow`，一行完成 | 任意交换半环（含 ℕ、ℤ、ℚ、ℝ、ℂ） | 三条标准公理 |

两个文件都可以在浏览器中运行（见上文“在浏览器中运行”）：[Binomial.lean](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FReferenceExamples%2FBinomial.lean)、[BinomialMathlib.lean](https://live.lean-lang.org/#url=https%3A%2F%2Fraw.githubusercontent.com%2Flichengtong123%2Flichengtong-RH%2Fmain%2F%25E5%2591%25BD%25E9%25A2%2598%25E7%259A%2584%25E5%25BD%25A2%25E5%25BC%258F%25E5%258C%2596%25E9%25AA%258C%25E8%25AF%2581-Lean4%2FReferenceExamples%2FBinomialMathlib.lean)。

归纳步的思路与手算相同：(a + b)ⁿ⁺¹ = (a + b)ⁿ·a + (a + b)ⁿ·b，把前一个和的末项、后一个和的首项拆出，中间各项用杨辉三角 C(n, k) + C(n, k + 1) = C(n + 1, k + 1) 两两合并，再把首末两项拼回。两份文件对照，可以看到 mathlib 替使用者完成了哪些工作；前者没有用到选择公理，后者经 mathlib 的有限和与代数结构而依赖它。

前一个文件不依赖 mathlib，也可以在本目录之外单独用 `lean Binomial.lean` 检查。两个文件中都有名为 `binomial_theorem` 的定理，所以它们各自构建，不设汇总入口。

## 在 VS Code 中看到的证明状态

Lean 的 VS Code 插件在编辑器右侧显示 InfoView：光标所在位置的已知条件与待证目标（Tactic state）、定理的检查结果（Messages）。读法见上文“读懂 Lean 代码与 InfoView”。以下截图取自作者本机，Lean 与 mathlib 版本与本目录相同。

**例题 1：两种证明依赖的公理不同。** 光标在 `#print axioms primeCounting_100_native` 上，右侧 Messages 列出这条定理依赖的公理。`decide +kernel` 的证明只依赖三条标准公理 `propext`、`Classical.choice`、`Quot.sound`；`native_decide` 的证明多出 `Lean.ofReduceBool`，表示计算由编译后的程序完成、没有经内核检查，因此要额外信任编译器（见上文“公理”一节）。

![例题 1](截图/S1a_PrimeCount-1.png)

**例题 2：约定值。** 光标在 ζ(1) ≠ 0 的证明末尾。这条证明没有用 `by` 逐步推导，而是直接给出一个表达式 `riemannZeta_ne_zero_of_one_le_re (by simp)`：mathlib 的定理“Re s ≥ 1 时 ζ(s) ≠ 0”，再用 `simp` 验证它的条件 1 ≤ Re 1。Expected type 显示这个表达式证明的命题 `riemannZeta 1 ≠ 0`；Messages 中的 `Goals accomplished!` 表示 Lean 接受了它。它说明 mathlib 给 ζ(1) 规定的约定值不为零。

![例题 2](截图/S1b_RHStatement-1.png)

**例题 3：归纳步中拆出最后一项。** 第一张光标在 `rw [sum_range_succ, sum_range_succ]` 之前。Tactic state 中 `case succ` 表示正在证明归纳步：已知条件列出 a、b、A、hA0、hA、n，以及归纳假设 `ih`（n 时的公式）；⊢ 后的目标是 n + 1 时的公式，两边各有一个 `∑ k ∈ range (n + 1)`。第二张是执行这一行之后：两个和都写成了 `∑ k ∈ range n` 加上 k = n 的一项，左边多出 `a n * b n`，右边多出 `A (n + 1) * (b (n + 1) - b n)`。此时目标与 ih 只差这两项，下一行 `linear_combination ih - b n * hA n` 用 ih 和部分和递推式 hA n 完成证明（手算见文件开头）。

![例题 3 改写前](截图/S2a_AbelSummation-1.png)

![例题 3 改写后](截图/S2a_AbelSummation-2.png)

**例题 4：3–4–1 不等式的最后一步。** 光标在最后一行末尾的 `hSquare` 上。Tactic state 显示 `No goals`：这一行执行后已没有待证目标。Expected type 列出已知条件 θ 与 `hSquare : 0 ≤ (1 + cos θ)²`，以及光标处这一项应证明的命题 `0 ≤ (1 + cos θ)²`。`mul_nonneg` 说“两个非负数之积非负”，要用它证明 0 ≤ 2·(1 + cos θ)²，需要提供 0 ≤ 2（由 `by norm_num` 给出）和 0 ≤ (1 + cos θ)²，后者正是 `hSquare`。

![例题 4](截图/S2b_ThreeFourOne-1.png)

**例题 5：互素乘积的素数幂因子分成两组。** 两张截图都在因子和恒等式的互素乘积情形（`case refine_3`）。第一张是第 77 行 `rw` 执行之前：上一行 `simp only` 已按 Λ 的定义把和改写成只对素数幂因子求和，所以 `ha`、`hb` 和 ⊢ 后的目标都是 `∑ a ∈ … with IsPrimePow a, Real.log ↑a.minFac` 的形式，目标中的因子集是 `(a * b).divisors`。第二张是第 78 行末尾，`rw` 执行之后：由于 a、b 互素，ab 的素数幂因子分成 a 的一组与 b 的一组，且互不相交，目标的左边成了两个和相加，每个和的形式与 `ha`、`hb` 的左边相同。下一行 `rw [ha, hb, …]` 就可以用归纳假设替换它们。这里拆分所依据的两条一般结果（`Nat.mul_divisors_filter_prime_pow` 与 `Nat.disjoint_divisors_filter_isPrimePow`）是从 mathlib 显式引用的。

![例题 5 改写前](截图/S3a_VonMangoldt-1.png)

![例题 5 改写后](截图/S3a_VonMangoldt-2.png)

**例题 6：改写之后留下的附加条件。** 第一张是第 48 行 `rw` 执行之前：目标是 `∑ p ∈ range (n + 1) with Nat.Prime p, Real.log ↑p = Real.log ↑(∏ p ∈ … , p)`，即 θ(n) = log(n#)。第二张是执行之后：`Nat.cast_prod` 与 `Real.log_prod` 把右边的“乘积的对数”改写成“对数之和”，等式两边相同，这个目标自动关闭；但 `Real.log_prod` 要求每个因子非零，这个条件成为新的目标 `case hf`：对集合中每个 x，`↑x ≠ 0`。接下来的几行（`intro p hp` 等）证明的就是这个条件。引用库定理时，它的前提条件也要给出证明。

![例题 6 改写前](截图/S3b_Chebyshev-1.png)

![例题 6 改写后](截图/S3b_Chebyshev-2.png)

**例题 7：用 Λ₀ 改写 Λ。** 第一张是改写之前，目标中是 `completedRiemannZeta s`（即 Λ）；第二张是执行 `rw [completedRiemannZeta_eq]` 之后，Λ 已换成 `completedRiemannZeta₀ s - 1 / s - 1 / (1 - s)`。上方列出的 h0 : s ≠ 0、h1 : s ≠ 1、h1' : 1 − s ≠ 0 是随后 `field_simp` 消去分母所需的条件；第一张中 `1 goal` 表示还剩一个待证目标。

![例题 7 改写前](截图/S4a_Xi-1.png)

![例题 7 改写后](截图/S4a_Xi-2.png)

**例题 8：由书中陈述推出 mathlib 陈述。** 光标在最后一行末尾。Expected type 列出全部已知条件：`h : RHBook`（书中的陈述，作为假设）、`hz` 即 ζ(s) = 0、`hnt` 即 s 不是平凡零点、`x✝` 即 s ≠ 1（引入时用 `_` 没有起名字），以及由临界带结论得到的 `h0 : 0 < s.re`、`h1 : s.re < 1`。`RHBook` 的内容是“对一切 s，若 ζ(s) = 0、0 < Re s、Re s < 1，则 Re s = 1/2”，所以 `exact h s hz h0 h1` 把 s 和三个条件依次交给 `h`，就得到 Re s = 1/2。Tactic state 显示 `No goals`，证明完成。

![例题 8](截图/S4b_CriticalStrip-1.png)

**收尾：互相矛盾的假设。** 右侧同时列出 `h1 : 1 < s.re` 与 `h2 : riemannZeta s = 0`。光标处的表达式由 mathlib 定理证明了 `¬riemannZeta s = 0`（即 ζ(s) ≠ 0），与 `h2` 矛盾；`absurd` 由一对矛盾推出任何结论。所以结论 Re s = 1/2 虽被 Lean 接受，却说明不了任何问题。

![收尾](截图/S5_Checking-1.png)

## 自动检查

仓库配置了自动检查：本目录的文件更新后，GitHub 服务器用固定版本的 Lean 与 mathlib 构建全部例题。构建时任何警告都按错误处理；含 `sorry` 的证明会产生警告，因此通不过检查。检查还确认文件中没有用 `axiom` 声明新的公理。检查通过，表示例题中的形式化证明已被 Lean 接受，其中不含 `sorry`，也未添加新的公理；各例实际依赖哪些公理，可用 `#print axioms` 查看（见例题 1 与收尾一节）。检查记录在仓库的 Actions 页面公开。

Lean 只检查推导，不检查形式化陈述是否忠实于书中原意；这一点须由读者对照判断，见收尾一节。

## 推荐教材

以下为 Lean 社区推荐的正式教材与入门材料（英文，均可免费在线阅读）：

| 教材 | 特点 |
|---|---|
| [Mathematics in Lean](https://leanprover-community.github.io/mathematics_in_lean/) | 面向数学工作者的标准教材，以 mathlib 为基础，附练习 |
| [The Mechanics of Proof](https://hrmacbeth.github.io/math2001/) | 节奏较缓，适合数学证明经验较少的读者 |
| [Theorem Proving in Lean 4](https://lean-lang.org/theorem_proving_in_lean4/) | 讲解 Lean 的类型论基础，适合想了解证明助手原理的读者 |
| [Natural Number Game](https://adam.math.hhu.de/#/g/hhu-adam/NNG4) | 浏览器中的交互入门，无需安装 |
| [mathlib 文档](https://leanprover-community.github.io/mathlib4_docs/) | 按名称查找定理及其陈述 |

更多资源见 Lean 社区的 [学习页面](https://leanprover-community.github.io/learn)。

## 在本机运行（可选）

安装 Lean 后，在本目录执行：

```bash
lake exe cache get   # 下载 mathlib 的预编译文件
lake build           # 构建并检查全部例题
```

本目录固定的版本：Lean `v4.22.0-rc4`，mathlib 提交 `e20d25f`（2025-08-06）。
