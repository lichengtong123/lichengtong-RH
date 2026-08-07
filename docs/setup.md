# 运行环境建立与程序安装说明

## 1. Manim / Python 动画

### 建议环境

- Python 3.10 或 3.11（64 位）
- [Manim Community](https://www.manim.community/) 最新稳定版
- `mpmath`（高精度特殊函数，用于 \(\zeta\)、\(\mathrm{Ei}\) 等）
- 可选：`numpy`、`scipy`、`matplotlib`（部分脚本绘图用）

### 安装示例（macOS / Linux）

```bash
# 建议使用虚拟环境
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

pip install -U pip
pip install manim mpmath numpy
# 若脚本另有依赖，见各 .py 文件头部 import
```

Manim 系统依赖（如 `ffmpeg`、LaTeX）见官方文档：

https://docs.manim.community/en/stable/installation.html

### 运行示例

当前 `manim/` 中的三个脚本与 `videos/` 中三个视频同名对应：

| 脚本 | 场景类（示例） |
|------|----------------|
| `ζ 共形映射.py` | `ZetaConformalMap` |
| `Hardy 轨迹.py` | `zeta_3D_18H` |
| `素数计数公式π0(x)逼近.py` | `RiemannVisualization1800log2` |

```bash
cd manim
# 文件名含空格或中文时请加引号
manim -pql "ζ 共形映射.py" ZetaConformalMap
manim -pql "Hardy 轨迹.py" zeta_3D_18H
manim -pql "素数计数公式π0(x)逼近.py" RiemannVisualization1800log2
# -pql：预览、低质量（快速）；成片可用 -pqh
```

Windows 用户请在「命令提示符」或 PowerShell 中激活虚拟环境后执行同样命令。

### 常见问题

| 现象 | 处理方向 |
|------|----------|
| 找不到 `manim` 命令 | 确认已激活 venv，且 `pip show manim` 有输出 |
| 渲染缺字体 / 中文乱码 | 安装中文字体，或在脚本中指定系统已有字体 |
| \(\zeta\) / \(\mathrm{Ei}\) 过慢 | 减小零点个数 \(K\)、缩小 \(x\) 或 \(t\) 范围；使用 `mpmath` 精度设置见脚本 |
| 与书中截图不完全一致 | 参数、版本、随机种子或插值方式可能不同；以数学对象为准 |

## 2. Mathematica

1. 安装 [Wolfram Mathematica](https://www.wolfram.com/mathematica/)（需合法许可）。
2. 用 Mathematica 打开 `mathematica/` 下的 `.nb` 文件。
3. 按笔记本中的说明求值单元格；部分笔记本体积大，打开与求值需较多内存。

### 未收录的大文件

GitHub 单文件限制为 **100 MB**。下列笔记本因嵌入图形体积过大，**未作为仓库主内容推送**（本地可见 `docs/large-files-local-only/`；亦可向作者另行索取）：

- `xi(s)函数曲面.nb`
- `泛函方程2.nb`

其余笔记本见 `mathematica/` 目录（如 `Gamma图形.nb`、`xi图形.nb`、`zeta延拓前图形.nb`、`zreta延拓后.nb`、`zeta零迹线.nb`、`函数方程.nb`、`li.nb`、`li函数图形.nb`、`选入图形.nb` 等）。

## 3. 视频

`videos/` 中现有三个示意 `.mp4`（与 `manim/` 脚本同名）：

- `ζ 共形映射.mp4`
- `Hardy 轨迹.mp4`
- `素数计数公式π0(x)逼近.mp4`

可用系统播放器直接打开。重新生成请用 `manim/` 中对应脚本渲染。

## 4. 版本

依赖库版本随时间更新；若与本文不一致，以各工具当前官方文档为准。  
本说明随仓库更新；书中印刷地址以 GitHub 页面最新 `README` 为准。
