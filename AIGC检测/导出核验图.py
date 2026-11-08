#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把朱雀报告单导出为「图片型核验图」：只保留片段解析以上的部分，且去掉文本层。

为什么必须栅格化：裁切框（CropBox）只改显示区域，正文仍留在 PDF 里，
`pdftotext` 一跑就能还原。图片型 PDF 没有文本对象，才谈得上“正文已删除”。

用法：
    python3 导出核验图.py                 # 读 朱雀回文/*.pdf，输出 核验图/
    python3 导出核验图.py --dpi 200 --out 核验图

每份产物都会自检：`pdftotext` 必须取不到文字，否则报错并中止。
"""

from __future__ import annotations

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

BASE = Path(__file__).resolve().parent
REPORTS = BASE / "朱雀回文"


def pdf_text(pdf: Path) -> str:
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          check=True, capture_output=True, text=True).stdout


def meta(pdf: Path) -> dict:
    t = pdf_text(pdf)
    m = re.search(r"朱雀AI生成检测报告单_(\d+)", t)
    f = re.search(r"文件名：\s*(\S+)", t)
    d = re.search(r"检测时间：\s*([\d/: ]+)", t)
    segs = re.findall(r"片段\d+\s+[\d.]+%\s+(\d+)", t)
    return {
        "编号": m.group(1) if m else "?",
        "文件": f.group(1) if f else pdf.stem.replace("-01", "") + ".txt",
        "时间": d.group(1).strip() if d else "",
        "缺文件名": not f,
        "片段字符": sum(int(x) for x in segs),
    }


def upper_half(png: Path, dpi: int) -> Image.Image:
    im = Image.open(png).convert("RGB")
    a = np.asarray(im).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    blue = (b > 110) & (b - r > 25) & (b - g > 10)
    blue[:, int(im.width * 0.16):] = False
    ys = sorted(set(np.nonzero(blue)[0].tolist()))
    if not ys:
        raise SystemExit(f"{png}: 找不到小节标题条，无法定位")
    groups, cur = [], [ys[0]]
    for y in ys[1:]:
        if y - cur[-1] <= 6:
            cur.append(y)
        else:
            groups.append((cur[0], cur[-1]))
            cur = [y]
    groups.append((cur[0], cur[-1]))
    if len(groups) < 4:
        raise SystemExit(f"{png}: 只找到 {len(groups)} 根标题条")
    cut = max(0, groups[3][0] - int(dpi * 0.08))
    return im.crop((0, 0, im.width, cut))


def chapter_key(name: str) -> tuple:
    m = re.match(r"chapter(\d+)", name)
    if m:
        return (0, int(m.group(1)), name)
    return (1, 0, name)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpi", type=int, default=200)
    ap.add_argument("--out", default=str(BASE / "核验图"))
    ap.add_argument("--png", action="store_true", help="同时输出 PNG（体积翻倍）")
    args = ap.parse_args()

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for pdf in sorted(REPORTS.glob("*.pdf"), key=lambda p: chapter_key(p.name)):
        info = meta(pdf)
        with tempfile.TemporaryDirectory() as tmp:
            stem = Path(tmp) / "p"
            subprocess.run(["pdftoppm", "-png", "-r", str(args.dpi), "-f", "1", "-l", "1",
                            str(pdf), str(stem)], check=True, capture_output=True)
            png = Path(f"{stem}-1.png")
            img = upper_half(png, args.dpi)
            dst = out / f"{pdf.stem}.pdf"
            img.save(dst, "PDF", resolution=float(args.dpi))
            if args.png:
                img.save(out / f"{pdf.stem}.png")
            left = pdf_text(dst).strip()
            if len(left) > 20:
                raise SystemExit(f"{dst.name}: 仍有可提取文本（{len(left)} 字节），已中止")
            note = ""
            if info["缺文件名"]:
                note = f"报告单未记录文件名；片段字符合计 {info['片段字符']}，据此对应"
            rows.append([pdf.stem, info["文件"], info["时间"], info["编号"],
                         f"{img.width}×{img.height}", f"{dst.stat().st_size//1024} KB",
                         "无文本层✅", note])

    head = ["# 朱雀报告核验图\n",
            "每份为报告单「片段解析」以上的部分，已栅格化为图片，**不含文本层**，",
            "因此不含书稿正文。自检方式：对任一文件执行 `pdftotext 文件 - | wc -c`，输出应接近 0。\n",
            "## 送检文件命名\n",
            "报告单上的文件名形如 `chapter14-C-02.txt`，四段各有含义：\n",
            "| 段 | 含义 |",
            "|---|---|",
            "| `chapter14` | 章号 |",
            "| `-C` | 送检版本。书稿有 B、C 两版，**C 版**为按 2026-11-06 修订意见定稿、参加编译的版本 |",
            "| `-02` | 切块序号。整章送检文本超过 5,500 字符时按段落边界切块，`-01` 为第 1 块；无此段即整章一次提交 |",
            "| `.txt` | 纯文本。朱雀不收 PDF，文本检测支持 txt / docx，故正文统一转为 UTF-8 的 txt 送检 |",
            "",
            "序言、导论与符号表为整章提交，文件名不带块号：`前言-C.txt`、`导论-C.txt`、`符号与约定-C.txt`。\n",
            "| 序号 | 送检文件 | 检测时间 | 报告编号 | 尺寸 | 体积 | 文本层 | 备注 |",
            "|---:|---|---|---|---:|---:|---|---|"]
    for i, r in enumerate(rows, 1):
        head.append(f"| {i} | `{r[1]}` | {r[2]} | {r[3]} | {r[4]} | {r[5]} | {r[6]} | {r[7]} |")
    head += ["", "> 注：`符号与约定` 那份报告单未印「文件名」行（当时以粘贴方式提交，而非上传文件）。"
                 "其片段字符数 2,370 与 `符号与约定-C.txt` 的字符数完全一致，据此对应；"
                 "若需报告单自带文件名，可重新以 txt 文件上传方式提交一次。", ""]
    (out / "索引.md").write_text("\n".join(head), encoding="utf-8")
    print(f"已导出 {len(rows)} 份 → {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
