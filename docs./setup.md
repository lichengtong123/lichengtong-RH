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

`manim/` 中的脚本与 `videos/` 中视频同名对应。章内主线为三条动画（共形映射、Hardy 轨迹、\(\pi_0\) 逼近）；3B1B 为对共形映射的比较：

| 脚本 | 场景类（示例） |
|------|----------------|
| `ζ 共形映射.py` | `ZetaConformalMap` |
| `3B1B.py` | `FullPlaneZeta` |
| `Hardy 轨迹.py` | `zeta_3D_18H` |
| `素数计数公式π0(x)逼近.py` | `RiemannVisualization1800log2` |

```bash
cd manim
# 文件名含空格或中文时请加引号
manim -pql "ζ 共形映射.py" ZetaConformalMap
manim -pql "3B1B.py" FullPlaneZeta
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

安装 [Wolfram Mathematica](https://www.wolfram.com/mathematica/)（需合法许可）。
在本地计算机上使用 Wolfram Mathematica 打开 `mathematica/` 下对应 `.nb` 计算显示3D图形，可以修改参数改变图形生成，用鼠标拖动改变观察视角。

笔记本清单见仓库根目录 [README.md](../README.md)「Mathematica 笔记本」一节。

## 3. 视频

`videos/` 中示意 `.mp4` 与 `manim/` 脚本同名。章内主线为三条动画；3B1B 为对共形映射的比较：

- `ζ 共形映射.mp4`
- `3B1B.mp4`（对共形映射的比较）
- `Hardy 轨迹.mp4`
- `素数计数公式π0(x)逼近.mp4`

可用系统播放器直接打开。重新生成请用 `manim/` 中对应脚本渲染。
浏览器交互页见仓库根目录 [README.md](../README.md)「第 18 章浏览器交互页」。

## 4. 版本

依赖库版本随时间更新；若与本文不一致，以各工具当前官方文档为准。  
本说明随仓库更新；书中印刷地址以 GitHub 页面最新 `README` 为准。
