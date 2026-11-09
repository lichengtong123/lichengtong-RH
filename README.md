# 《素数计数与黎曼猜想：ζ 函数、零点与显式公式》配套资源

本仓库是李成桐著《素数计数与黎曼猜想：ζ 函数、零点与显式公式》的配套材料，收录书中动画的视频与 Python（Manim）源程序、插图的 Mathematica 程序、知识谱系关系图，以及供读者自选的学习笔记、习题与解答和形式化证明示例。[命题的形式化验证](命题的形式化验证-Lean4/README.md)从本书中选取若干命题，把它们的陈述与证明写成 Lean 4 代码，由计算机逐步检查，借此介绍形式化证明这种方法，以及怎样检查一个号称“已经形式化”的证明。这些材料都不是理解正文所必需的；书中的论证自足完整。

书中前言所写地址即本仓库：**https://github.com/lichengtong123/lichengtong-RH**

## 预印版同行审阅

[输入密码在线阅读](https://lichengtong123.github.io/lichengtong-RH/docs/同行审阅/)，或[下载预印版同行审阅稿（加密PDF / 加密Word）](docs/同行审阅/README.md)。打开密码由作者通过其他渠道单独提供；审阅版本、下载方式及反馈说明见该页面。

英文审阅版：[输入密码在线阅读 / Read online](https://lichengtong123.github.io/lichengtong-RH/docs/同行审阅/index-en.html)，或[下载加密 PDF / Download](docs/同行审阅/Prime-Counting-and-the-Riemann-Hypothesis-Review-Encrypted.pdf)。使用与中文版相同的打开密码。

## 在线观看书中动画

书中第 20 章只印关键帧，完整动画可通过以下播放页观看，也可下载视频，无需安装 Manim：

| 书中内容 | 地址 |
|----------|------|
| 二维 ζ 同伦（ζ 映射） | [播放](https://lichengtong123.github.io/lichengtong-RH/videos/zeta.html) |
| Hardy 轨迹 | [播放](https://lichengtong123.github.io/lichengtong-RH/videos/hardy.html) |
| π₀ 逼近 | [播放](https://lichengtong123.github.io/lichengtong-RH/videos/pi0.html) |

另提供[三个黑底辅助视频](videos/black/README.md)，供屏幕观看参考；各白底播放页也设有黑底版入口。黑底版与白底版制作批次不同，不替代书稿对应版。

## 目录

各目录的使用方法见其中的 README。

| 目录 | 内容 | 对应章节 |
|------|------|----------|
| [manim/](manim/README.md) | 第 20 章动画的 Python（Manim）源程序、渲染命令与参数说明 | 第 20 章 |
| [videos/](videos/README.md) | 三个白底书稿对应视频及其黑底辅助版，供观看与下载 | 第 20 章 |
| [mathematica/](mathematica/README.md) | 书中曲面图与零迹线图的 Mathematica 程序（`.wl`）及可用免费 Wolfram Player 查看的笔记本（`.nb`） | 第 5、7、9、10、13、17 章 |
| [数值计算/](数值计算/README.md) | 书中数值表格与数据图的源程序、参数与数据：第 19 章可复算的数值实验（含零点区间与核验输出），第 2、13、18 章的数据文件 | 第 2、13、18、19 章 |
| [AIGC检测/](AIGC检测/README.md) | AI 生成痕迹检测结果：知网全文检测与朱雀逐章检测，附核验图与检测说明；同时说明本书使用生成式 AI 的环节与范围 | 全书 |
| [docs/](docs/) | [运行环境与安装说明](docs/运行环境建立与程序安装说明.md)、[ζ 函数数值计算的常用软件](docs/函数数值计算的常用软件.md) | 第 19、20 章 |
| [关系图下载/](关系图下载/) | A3 版黎曼猜想知识谱系关系图（中文版与英文版；PDF 供查阅与打印，SVG 矢量图可插入文档或幻灯片），概括主体理论（第 1–15 章） | 第 16 章 |
| [黎曼原稿扫描/](黎曼原稿扫描/README.md) | Riemann 1859 年论文德文原文扫描本（1876 年文集版，公有领域），供对照书中译稿 | 第 21 章 |
| [学习笔记/](学习笔记/) | 专题证明、推导与说明，提供 PDF（初稿） | 独立专题 |
| [命题的形式化验证-Lean4/](命题的形式化验证-Lean4/README.md) | 从本书选取 8 个命题，按“自己写多少、借用数学库 mathlib 多少”分四个阶段给出 Lean 4 形式化陈述与证明，附 InfoView 截图；最后说明怎样检查一个形式化证明。另附本书其他命题与 mathlib 定理的对照表，以及学习笔记第 11、16 篇的配套例程 | 第 1、2、5、7、9–11 章，附录 A、B、F |
| [习题与解答/](习题与解答/README.md) | 参考习题（题目、提示与完整解答，PDF），按部分发布；第一至五部分均已发布初稿 | 第 1–22 章 |

## 使用注意

1. 动画与图形都是有限范围内的数值示意，不构成定理证明；与书中定义、证明不一致时，以书中正文为准。
2. 改变截断参数（零点个数、自变量范围等）只改变数值选择，不产生新的数学命题。
3. 文件名与目录以本仓库当前版本为准；书中印刷说明与本页不一致时，以本页为准。

## 许可与反馈

源程序（`manim/`、`mathematica/` 中的程序及播放页面，`命题的形式化验证-Lean4/` 中的 Lean 程序）采用 MIT 许可；学习笔记、参考习题、文档、关系图与视频采用 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)；黎曼原稿扫描本属公有领域；同行审阅稿保留所有权利。详见 [LICENSE](LICENSE)。引用书中数学内容请注明书名与作者。问题与勘误请通过本仓库 Issues 反馈，或发邮件至 lichengtong-RH@qq.com。
