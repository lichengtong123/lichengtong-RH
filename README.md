---
noteId: "2c706390bd3711f1a0e6edfe24e778c6"
tags: []

---

# 《素数计数与黎曼猜想：ζ 函数、零点与显式公式》配套资源

本仓库是李成桐著《素数计数与黎曼猜想：ζ 函数、零点与显式公式》的配套材料，收录书中动画的视频与 Python（Manim）源程序、图形的 Mathematica 程序、浏览器交互页与知识谱系关系图。仓库不含全书正文。

书中前言与「书后附注」所写地址即本仓库：**https://github.com/lichengtong123/lichengtong-RH**

## 目录结构

| 路径 | 内容 | 对应章节 |
|------|------|----------|
| `*.html`（根目录） | 浏览器交互页（GitHub Pages） | 第 20 章 |
| `videos/` | 示意动画视频（`.mp4`） | 第 20 章 |
| `manim/` | 生成上述视频的 Python（Manim）源程序（`.py`） | 第 20 章 |
| `mathematica/` | Mathematica 笔记本（`.nb`）与程序（`.wl`） | 第 5、7、9、13、17 章等 |
| `docs/` | 运行环境与安装说明、数值计算软件介绍、练习 | 第 19 章等 |
| `images/` | 静态图件，含知识谱系全着色关系图 | 第 16 章 |

## 一、浏览器交互页（第 20 章）

书中第 20 章正文只印关键帧，完整动画可在浏览器中直接打开，无需安装任何软件：

| 书中内容 | 地址 |
|----------|------|
| ζ 映射（共形映射） | https://lichengtong123.github.io/lichengtong-RH/Conformal-100.html |
| Hardy 轨迹 | https://lichengtong123.github.io/lichengtong-RH/Hardy.html |
| π₀ 逼近 | https://lichengtong123.github.io/lichengtong-RH/J2pi.html |
| 3B1B 式全平面变换（与共形映射对照，书中未印） | https://lichengtong123.github.io/lichengtong-RH/3B1B.html |

## 二、Python（Manim）动画程序

### 程序与视频对照

| 书中内容 | 源程序 | 场景类名 | 视频 |
|----------|--------|----------|------|
| ζ 映射 | `manim/ζ 共形映射.py` | `ZetaConformalMap` | `videos/ζ 共形映射.mp4` |
| Hardy 轨迹 | `manim/Hardy 轨迹.py` | `zeta_3D_18H` | `videos/Hardy 轨迹.mp4` |
| π₀ 逼近 | `manim/素数计数公式π0(x)逼近.py` | `RiemannVisualization1800log2` | `videos/素数计数公式π0(x)逼近.mp4` |
| 3B1B 式全平面变换 | `manim/3B1B.py` | `FullPlaneZeta` | `videos/3B1B.mp4` |

### 运行

先按 [docs/setup.md](docs/setup.md) 安装 Python、Manim Community 与 `mpmath`，然后：

```bash
cd manim
manim -pql "ζ 共形映射.py" ZetaConformalMap          # -pql 低质量预览；成片用 -pqh
manim -pql "Hardy 轨迹.py" zeta_3D_18H
manim -pql "素数计数公式π0(x)逼近.py" RiemannVisualization1800log2
manim -pql "3B1B.py" FullPlaneZeta
```

文件名含空格或中文时须加引号。

### 修改参数，生成不同的动画

各程序的主要参数集中在文件开头，改后重新运行即可：

| 程序 | 参数 | 含义 |
|------|------|------|
| `ζ 共形映射.py` | `x_range_min/max`、`y_range_min/max` | 值域平面（w 平面）的显示范围 |
| | `num_h_lines`、`num_v_lines` | s 平面网格线条数，决定被映射区域的大小与疏密 |
| | `points_per_line` | 每条网格线的采样点数（越大越光滑、越慢） |
| `Hardy 轨迹.py` | `T_MAX` | 沿临界线的高度上限 t |
| | `DT` | t 的采样步长（越小越密、预计算越久） |
| | `range(1, 40)` | 标注的非平凡零点个数 |
| `素数计数公式π0(x)逼近.py` | `PARAMS["MAXDISTANCE"]` | x 的范围上限 |
| | `PARAMS["NONTRIVIAL_MIN"]`、`["NONTRIVIAL_MAX"]` | 计入的非平凡零点序号范围（截断数 K） |
| | `PARAMS["TRIVIAL_ZEROS"]` | 计入的平凡零点个数 |
| | `PARAMS["DATA_POINTS"]`、`["DRAW_INTERVAL"]` | 采样点数与逐帧绘制间隔 |

例如把 `NONTRIVIAL_MAX` 由 1000 改为 10、100，可观察计入的零点增多时，逼近曲线如何贴合 π₀(x) 的阶梯。

## 三、Mathematica 程序

在本机用 [Wolfram Mathematica](https://www.wolfram.com/mathematica/) 打开并执行。三维曲面可用鼠标拖动旋转，从任意角度观察；书中所印只是其中一个视角。修改文件中的范围、采样点数等参数，可生成不同的图形。

| 文件 | 内容 | 书中位置 |
|------|------|----------|
| `zeta零迹线-修订.wl` | ζ 零迹线（Re ζ = 0、Im ζ = 0 与平凡零点） | 图 17.4 |
| `xi零迹线-修订-2.wl` | ξ 零迹线 | 图 17.6 |
| `zeta零迹线.nb` | ζ 零迹线（旧版笔记本） | 第 17 章 |
| `xi图形.nb` | ξ 的实部、虚部曲面 | 第 17 章 |
| `Gamma图形.nb` | Γ 函数图形 | 第 7 章 |
| `zeta延拓前图形.nb` | Re(s) > 1 上 ζ 的图形 | 第 5 章 |
| `zeta延拓后.nb` | 解析延拓后 ζ 的图形 | 第 9 章 |
| `函数方程.nb` | 函数方程相关图形 | 第 9 章 |
| `li函数图形.nb` | 对数积分 li 的图形 | 第 13 章 |
| `选入图形.nb` | 书中选用图形的汇总 | — |

`.wl` 程序末行的 `Export` 会把图导出为 PDF，与书中所用文件同名。

## 四、数值计算软件与练习

- [docs/numerics.md](docs/numerics.md)：计算 ζ 值、非平凡零点与 π(x) 的常用软件（mpmath、Mathematica、PARI/GP、SageMath、FLINT、lcalc、primecount）和零点数据（Odlyzko 零点表、LMFDB），附 mpmath 最小示例。
- [docs/exercises.md](docs/exercises.md)：八道数值练习，附参考结果。
- [docs/exercises-mainline.md](docs/exercises-mainline.md)：第 2–15 章（逻辑主线）的推导练习，按章编排，每题附提示。

## 五、环境与安装

见 [docs/setup.md](docs/setup.md)：Python / Manim / mpmath 的安装、渲染命令与常见问题；Mathematica 为商业软件，须本机安装。

## 使用注意

1. 动画与图形都是有限范围内的数值示意，不构成定理证明；与书中定义、证明不一致时，以书中正文为准。
2. 改变截断参数（零点个数、自变量范围等）只改变数值选择，不产生新的数学命题。
3. 文件名与目录以本仓库当前版本为准；书中印刷说明与本页不一致时，以本页为准。

## 许可与反馈

源程序与视频的使用许可由作者另行声明；引用书中数学内容请注明书名与作者。问题与勘误请通过本仓库 Issues 反馈，或发邮件至 lichengtong123@qq.com。
