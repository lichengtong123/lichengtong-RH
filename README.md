# 素数分布与黎曼猜想 — 配套资源

本仓库为中文著作《素数分布与黎曼猜想》的**配套材料**（不包含全书 PDF 正文）。

书中「书后附注」与前言、后记所写地址即本仓库：

**https://github.com/lichengtong123/lichengtong-RH**

## 目录结构

| 路径 | 内容 |
|------|------|
| `videos/` | 与正文（第 18 章等）对应的示意视频（`.mp4`） |
| `manim/` | 生成上述视频的 Manim / Python 源程序（`.py`） |
| `mathematica/` | Mathematica 笔记本（`.nb`）及部分导出图（`.pdf`） |
| `docs/` | 运行环境与安装说明 |
| `images/` | 静态图件；含 `黎曼猜想知识谱系关系图.pdf`（全文着色总图） |

## 视频与 Manim 脚本（一一对应）

文件名中英文、空格与书中称谓一致。视频在 `videos/`，脚本在 `manim/`。

| 示意内容（书中） | 视频 | Manim 脚本 | 场景类名（脚本内） |
|------------------|------|------------|-------------------|
| \(\zeta\) 共形映射 | `videos/ζ 共形映射.mp4` | `manim/ζ 共形映射.py` | `ZetaConformalMap` |
| Hardy 轨迹 | `videos/Hardy 轨迹.mp4` | `manim/Hardy 轨迹.py` | `zeta_3D_18H` |
| 素数计数 \(\pi_0(x)\) 逼近 | `videos/素数计数公式π0(x)逼近.mp4` | `manim/素数计数公式π0(x)逼近.py` | `RiemannVisualization1800log2` |

渲染参数见各脚本注释与 [docs/setup.md](docs/setup.md)。

### 快速渲染示例

```bash
cd manim
# 低质量预览（-pql）；成片可用 -pqh
manim -pql "ζ 共形映射.py" ZetaConformalMap
manim -pql "Hardy 轨迹.py" zeta_3D_18H
manim -pql "素数计数公式π0(x)逼近.py" RiemannVisualization1800log2
```

（路径含空格或中文时请加引号；Windows 建议在已激活的 venv 中同样执行。）

## Mathematica 笔记本（`mathematica/`）

| 文件 | 大致用途（由文件名） |
|------|----------------------|
| `Gamma图形.nb` | \(\Gamma\) 函数相关图形 |
| `xi图形.nb` | \(\xi\) 函数相关图形 |
| `zeta延拓前图形.nb` | \(\zeta\) 解析延拓前（\(\operatorname{Re}s>1\) 等）图形 |
| `zreta延拓后.nb` | \(\zeta\) 解析延拓后图形（文件名即仓库中实际拼写） |
| `zeta零迹线.nb` | \(\zeta\) 零迹线相关图形 |
| `函数方程.nb` | 函数方程相关图形 |
| `li.nb` / `li函数图形.nb` | 对数积分 \(\mathrm{li}\) 相关 |
| `li模曲面.pdf` | \(\mathrm{li}\) 模曲面导出图 |
| `选入图形.nb` | 书中选用/汇总的图形笔记本 |

用本机 [Wolfram Mathematica](https://www.wolfram.com/mathematica/) 打开对应 `.nb` 求值即可。部分笔记本体积较大，打开与求值需较多内存。

### 未推送到 GitHub 的大文件

GitHub 单文件限制约 **100 MB**。下列笔记本体积过大，放在本地 `docs/large-files-local-only/`（**不**作为仓库主内容推送；若克隆后没有该目录，可向作者另行索取）：

- `xi(s)函数曲面.nb`
- `泛函方程2.nb`

## 环境与安装

请先阅读：

- [docs/setup.md](docs/setup.md) — Python / Manim / mpmath 等
- Mathematica 需本机安装 Wolfram Mathematica（商业软件）

## 使用注意

1. **数值动画与数值图为示意，不构成定理证明**；与书中定义、证明冲突时，以书中正文为准。
2. 改变截断参数（零点个数、自变量范围等）会改变画面，对应的是数值选择，不是新的数学命题。
3. 仓库中的文件名、目录以当前版本为准；书中印刷说明若与本页不一致，以 GitHub 页面最新 `README` 为准。

## 许可

源程序与视频的使用许可由作者另行声明。引用书中数学内容时请注明书名与作者。

## 联系

问题与勘误可通过本仓库 Issues 反馈（若已开启），或以书中作者联系方式为准。
