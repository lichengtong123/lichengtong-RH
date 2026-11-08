#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""从朱雀报告单 PDF 中截取「检测片段详情」以上的内容，保存为 PNG。

用法：
    python3 截取报告上半.py 朱雀/*.pdf              # 输出到 朱雀/图/
    python3 截取报告上半.py a.pdf -o 输出目录

原理：报告单每个小节标题左侧都有一根蓝色竖条。找到第 4 根竖条
（「检测片段详情」）的位置，从页顶裁到它上方 20px 处。
"""

from __future__ import annotations

import argparse
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

DPI = 300
MARGIN = 20


def render_first_page(pdf: Path, outstem: Path) -> Path:
    subprocess.run(
        ["pdftoppm", "-png", "-r", str(DPI), "-f", "1", "-l", "1", str(pdf), str(outstem)],
        check=True, capture_output=True,
    )
    return Path(f"{outstem}-1.png")


def find_section_bars(img: Image.Image) -> list[tuple[int, int]]:
    a = np.asarray(img.convert("RGB")).astype(int)
    r, g, b = a[:, :, 0], a[:, :, 1], a[:, :, 2]
    blue = (b > 110) & (b - r > 25) & (b - g > 10)
    blue[:, int(img.width * 0.16):] = False          # 只保留左侧标题条区域
    ys = sorted(set(np.nonzero(blue)[0].tolist()))
    if not ys:
        return []
    groups, cur = [], [ys[0]]
    for y in ys[1:]:
        if y - cur[-1] <= 8:
            cur.append(y)
        else:
            groups.append((cur[0], cur[-1]))
            cur = [y]
    groups.append((cur[0], cur[-1]))
    return groups


def crop_upper(pdf: Path, out_png: Path) -> tuple[int, int]:
    with tempfile.TemporaryDirectory() as tmp:
        rendered = render_first_page(pdf, Path(tmp) / "page")
        img = Image.open(rendered).convert("RGB")
        bars = find_section_bars(img)
        if len(bars) < 4:
            raise SystemExit(f"{pdf.name}: 只找到 {len(bars)} 根标题条，无法定位")
        cut = max(0, bars[3][0] - MARGIN)
        upper = img.crop((0, 0, img.width, cut))
        out_png.parent.mkdir(parents=True, exist_ok=True)
        upper.save(out_png)
        return upper.size


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="+")
    ap.add_argument("-o", "--out", default=None, help="输出目录（默认 PDF 同级的 图/）")
    args = ap.parse_args()
    for p in args.pdfs:
        pdf = Path(p)
        out_dir = Path(args.out) if args.out else pdf.parent / "图"
        dst = out_dir / f"{pdf.stem}_上半.png"
        size = crop_upper(pdf, dst)
        print(f"{dst.name}  {size[0]}×{size[1]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
