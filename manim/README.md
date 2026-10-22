# Manim 动画程序（第 20 章）

本目录是书中第 20 章动画的 Python（Manim Community）源程序。已发布的三个新版视频及下载链接见 [videos/](../videos/README.md)。

## 程序与视频对照

| 书中内容 | 源程序 | 动画场景类 | 静帧场景类 |
|----------|--------|------------|------------|
| 二维 ζ 同伦 | `二维 ζ 同伦.py` | `ZetaConformalMap` | `ZetaStill` |
| Hardy 轨迹 | `Hardy 轨迹.py` | `zeta_3D_18H` | `HardyStill` |
| π₀ 逼近 | `素数计数公式逼近.py` | `RiemannVisualization1800log2` | `Pi0Still` |
| 3B1B 式全平面变换（书中未印，仅保留源码） | `3B1B.py` | `FullPlaneZeta` | — |

前三个程序共用同目录的 `ch20_render.py`（统一的分辨率、白底配色和渲染模式），下载或移动时须一并保留。

## 运行

先按 [运行环境建立与程序安装说明](../docs/运行环境建立与程序安装说明.md) 安装依赖，并激活已安装 Manim Community 的 Python 环境。在本目录执行：

```bash
RH_RENDER_MODE=video python -m manim "二维 ζ 同伦.py" ZetaConformalMap
RH_RENDER_MODE=video python -m manim "Hardy 轨迹.py" zeta_3D_18H
RH_RENDER_MODE=video python -m manim "素数计数公式逼近.py" RiemannVisualization1800log2
python -m manim "3B1B.py" FullPlaneZeta
```

- 前三条命令输出白底、深色线条、1920×1080、30 fps 的完整视频，写入 `media/videos/` 下以程序名命名的子目录，不会覆盖 `videos/` 中已发布的视频。
- 文件名含空格或中文时须加引号。
- 设置 `RH_PREVIEW=1` 可改为 960×540 的低分辨率快速预览；正式渲染不要设置它，也不要添加 `-ql` 等低清选项。
- 设置 `RH_RENDER_MODE=book` 并渲染静帧场景类，输出 2880×1620 的白底书稿静帧（只保存最后一帧）。视频模式与静帧模式分别输出，修改程序后应同步重新生成。

作者的 macOS 环境示例如下；其他机器应换成各自的环境名与仓库路径：

```bash
conda activate manim-3b1b
export PATH=/Library/TeX/texbin:$PATH
cd "/Users/lichengtong/lichengtong-RH/manim"
```

## 修改参数，生成不同的动画

主要参数集中在各程序开头，改后重新运行即可：

| 程序 | 参数 | 含义 |
|------|------|------|
| `二维 ζ 同伦.py` | `x_range_min/max`、`y_range_min/max` | 绘图坐标范围 |
| | `fine_step` | s 平面细网格的间距 |
| | `points_per_line` | 每条网格线的采样点数（越大越光滑、越慢） |
| `Hardy 轨迹.py` | `T_MAX` | 沿临界线的高度上限 t |
| | `DT` | t 的采样步长（越小越密、预计算越久） |
| | `AMPLIFY_FACTOR` | 横截面振幅的显示放大倍数；零点按 `T_MAX` 自动选取 |
| `素数计数公式逼近.py` | `PARAMS["MAXDISTANCE"]` | x 的范围上限 |
| | `PARAMS["NONTRIVIAL_MIN"]`、`["NONTRIVIAL_MAX"]` | 计入的非平凡零点序号范围（截断数 K） |
| | `PARAMS["TRIVIAL_ZEROS"]` | 计入的平凡零点个数 M |
| | `PARAMS["DATA_POINTS"]`、`["DRAW_INTERVAL"]` | 采样点数与逐帧绘制间隔 |

例如将 `NONTRIVIAL_MAX` 的默认值 500 改为 10、100，可比较不同零点截断数下的逼近。该参数计正虚部零点数，即纳入的共轭对数；素数跳跃点的完整反演值采用 π₀ 的左右平均约定。

动画是有限范围内的数值示意；改变参数只改变数值选择，不产生新的数学命题。与书中定义、证明不一致时，以正文为准。

[返回仓库首页](../README.md)
