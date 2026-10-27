# 数值计算

书中数值表格与数据图的源程序、参数文件和生成数据。书中写作“资源仓库‘数值计算’目录下的 `dat`”“`numerical/ch19`”等，指的就是本目录下的两个子目录。

## 目录

| 路径 | 内容 | 对应章节 |
|------|------|----------|
| `numerical/ch19/` | 第 19 章数值实验（计算版本 v2.0）：源程序 `reproduce.py`、参数 `config.json`、测试 `test_reproduce.py`、依赖 `requirements.txt`，以及 `results/` 中的零点区间、逐点包络、统计与核验输出 | 第 19 章 |
| `numerical/ch2/reproduce_comparison.py` | 重算第 2 章 $\pi(x)$、$\operatorname{Li}(x)$、$x/\log x$ 对照数据 | 第 2 章 |
| `dat/pi_x_comparison.dat` | 第 2 章对照图数据 | 第 2 章 |
| `dat/li_real_a.dat`、`dat/li_real_b.dat` | 第 13 章 $\operatorname{li}$ 实部曲线数据 | 第 13 章 |
| `dat/riemann_data.dat`、`dat/fourier_data.dat` 及 `generate_ch18_*.py` | 第 18 章两幅对照图的数据与生成程序 | 第 18 章 |
| `dat/riemann_data_{20,60,200,500}.dat`、`dat/ch19-*-rows.tex` | 第 19 章数据图与表格行，由 `reproduce.py` 生成 | 第 19 章 |

`dat/` 中另有 `pnt_data*.dat`、`riemann_data_{40,100}.dat`，是早期版本留下的数据，书中现已不用，保留供对照。`numerical/ch19/results/legacy/` 同理。

## 运行

在本目录（`数值计算/`）下执行。所用 Python 为 3.11，依赖版本已固定：

```sh
python3 -m pip install -r numerical/ch19/requirements.txt
python3 numerical/ch19/reproduce.py                    # 重建 dat/ 中第 19 章的数据与表格行
python3 -m unittest discover -s numerical/ch19 -v      # 运行测试
python3 numerical/ch19/reproduce.py --verify-artifacts # 核对输出文件的 SHA-256 摘要
python3 numerical/ch2/reproduce_comparison.py          # 重算第 2 章对照数据
python3 dat/generate_ch18_riemann.py                   # 第 18 章（读取 numerical/ch19/results/zeros.json）
python3 dat/generate_ch18_fourier.py
```

程序按自身位置解析路径，因此 `dat/` 与 `numerical/` 须保持并列。参数、运行环境与耗时记录在 `numerical/ch19/results/manifest.json` 中。

**运行前注意：**请保留仓库原有的 `dat/` 目录。重建命令会覆盖其中相应的数据文件、表格行，以及 `numerical/ch19/results/` 中的核验输出；需要比较旧结果时，应在仓库副本中运行。测试与 `--verify-artifacts` 不重建这些产物。计算版本 v2.0 对应书稿 10-19；运行耗时会随机器变化，产物哈希只用于核对版本一致性，不代替数学认证。

## 核验的范围

`numerical/ch19/README.md`（英文）逐条说明了哪些结果有严格的区间包络、哪些只是取整后的中点值。要点如下：

- 零点由 FLINT 给出，脚本在每个零点两侧验证实 $\Xi$ 变号，并与 FLINT 给出的计数 $N(T)$ 对照，从而确认所用高度以下零点完整且为单零点。这不是 RH 的证明。
- 有限和以 160 位球算术计算，在有理网格点上给出严格包络；`.dat` 绘图文件中是取整后的中点值。
- 网格统计只针对 3001 个采样点，不声称连续区间上的上确界。
