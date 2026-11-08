#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""按章生成「检测报告单」HTML：环图 + 分布条 + 片段解析表 + 片段详情。

版式参照朱雀的检测报告单，但**不冒充朱雀**：页眉页脚都标出实际检测器。

用法：
    python3 report_sheet.py 段落评分.csv --out 报告单
    python3 report_sheet.py 段落评分.csv --scale zhuque --out 报告单   # 需 CSV 内有 AIGC值 列

两种刻度：
    --scale local   （默认）把每段分数换算成全书内的相对位次 0–1，
                     分类为 低 / 中 / 高，标签为「相对整齐度」。
    --scale zhuque  直接使用朱雀返回的 AIGC 值（0–1），
                     分类为 人工特征 / 疑似AI / AI特征。
"""

from __future__ import annotations

import argparse
import csv
import html
import json
import math
import re
import statistics
import time
from pathlib import Path
from typing import Sequence

# 颜色沿用朱雀报告的绿/橙/红
COLORS = ("#3aa84a", "#d69a2a", "#c1443c")

SCALES = {
    "local": {
        "thresholds": (0.50, 0.85),
        "labels": ("相对整齐（低位次）", "居中", "偏模板（高位次）"),
        "legend": "AIGC 值（相对位次 0–1）",
        "note": "本地启发式刻度：0 = 全书最松散的一段，1 = 全书最整齐的一段。不是概率。",
    },
    "zhuque": {
        "thresholds": (0.50, 0.99),
        "labels": ("人工特征", "疑似 AI", "AI 特征"),
        "legend": "AIGC 值（0–1）",
        "note": "朱雀返回的 AIGC 值。",
    },
}


def load_rows(path: Path, scale: str) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    if not rows:
        raise SystemExit("CSV 为空")
    if scale == "zhuque":
        if "AIGC值" not in rows[0]:
            raise SystemExit("--scale zhuque 需要 CSV 含「AIGC值」列")
        for r in rows:
            r["value"] = float(r["AIGC值"])
        return rows
    scores = [int(r["评分"]) for r in rows]
    order = sorted(range(len(rows)), key=lambda i: scores[i])
    ranks = [0] * len(rows)
    for pos, i in enumerate(order):
        ranks[i] = pos
    n = max(1, len(rows) - 1)
    for r, rk in zip(rows, ranks):
        r["value"] = rk / n
    return rows


def category(value: float, thresholds: Sequence[float]) -> int:
    if value < thresholds[0]:
        return 0
    if value < thresholds[1]:
        return 1
    return 2


def smooth(rows: list[dict]) -> None:
    """1-2-1 邻域平均，避免相邻段落反复翻转导致片段过碎。"""
    vals = [r["value"] for r in rows]
    n = len(vals)
    for i, r in enumerate(rows):
        if n < 3:
            continue
        a = vals[i - 1] if i > 0 else vals[i]
        b = vals[i + 1] if i < n - 1 else vals[i]
        r["value"] = (a + 2 * vals[i] + b) / 4


def segments(rows: list[dict], thresholds) -> list[dict]:
    """把相邻同类的段落并成一个片段。"""
    out: list[dict] = []
    for r in rows:
        cat = category(r["value"], thresholds)
        if out and out[-1]["cat"] == cat:
            out[-1]["rows"].append(r)
        else:
            out.append({"cat": cat, "rows": [r]})
    for seg in out:
        chars = sum(int(r["字数"]) for r in seg["rows"])
        seg["chars"] = chars
        seg["value"] = sum(r["value"] * int(r["字数"]) for r in seg["rows"]) / max(1, chars)
        seg["text"] = " ".join(r["正文"] for r in seg["rows"])
        seg["line"] = seg["rows"][0]["行号"]
    return out


def donut(parts: list[tuple[str, float, str]], size: int = 260) -> str:
    r, w = 78, 30
    c = 2 * math.pi * r
    off = 0.0
    arcs = []
    for color, frac, _ in parts:
        dash = max(0.0, frac * c)
        arcs.append(
            f'<circle cx="130" cy="130" r="{r}" fill="none" stroke="{color}" '
            f'stroke-width="{w}" stroke-dasharray="{dash:.2f} {c - dash:.2f}" '
            f'stroke-dashoffset="{-off:.2f}" transform="rotate(-90 130 130)"/>'
        )
        off += dash
    if off < c - 0.01:  # 补齐余量（理论上不会出现）
        arcs.append(f'<circle cx="130" cy="130" r="{r}" fill="none" stroke="#eee" '
                    f'stroke-width="{w}" stroke-dasharray="{c - off:.2f} {off:.2f}" '
                    f'stroke-dashoffset="{-off:.2f}" transform="rotate(-90 130 130)"/>')
    labels = []
    pos = [(64, 84), (200, 196), (148, 52)]
    acc = 0.0
    for i, (color, frac, name) in enumerate(parts):
        if frac <= 0.001:
            acc += frac
            continue
        x, y = pos[i % len(pos)]
        labels.append(f'<text x="{x}" y="{y}" font-size="15" fill="#333" text-anchor="middle" '
                      f'stroke="#fff" stroke-width="4" paint-order="stroke" '
                      f'style="paint-order:stroke">{frac*100:.2f}%</text>')
        acc += frac
    return (f'<svg viewBox="0 0 260 260" width="{size}" height="{size}" role="img">'
            + "".join(arcs) + "".join(labels) + "</svg>")


def fmt_pct(x: float) -> str:
    return f"{x*100:.2f}%"


def sheet_for(chapter: str, rows: list[dict], scale_cfg: dict, provider: str) -> str:
    total = sum(int(r["字数"]) for r in rows)
    smooth(rows)
    segs = segments(rows, scale_cfg["thresholds"])
    shares = [0.0, 0.0, 0.0]
    for seg in segs:
        shares[seg["cat"]] += seg["chars"] / total

    parts = [(COLORS[i], shares[i], scale_cfg["labels"][i]) for i in range(3)]
    legend_rows = "".join(
        f'<div class="lg"><i style="background:{COLORS[i]}"></i>'
        f'<span>{html.escape(scale_cfg["labels"][i])}'
        f'</span>'
        f'<b>{fmt_pct(shares[i])}</b></div>'
        for i in range(3)
    )
    bar = "".join(
        f'<span style="width:{max(shares[i]*100,0):.2f}%;background:{COLORS[i]}"></span>'
        for i in range(3)
    )
    table = "".join(
        f'<tr><td>{i}</td><td>片段{i}</td><td>{fmt_pct(seg["chars"]/total)}</td>'
        f'<td>{seg["chars"]}</td>'
        f'<td style="color:{COLORS[seg["cat"]]}">{seg["value"]:.4f}</td></tr>'
        for i, seg in enumerate(segs, 1)
    )
    detail = ""
    for i, seg in enumerate(segs, 1):
        txt = re.sub(r"\s+", " ", seg["text"])[:420]
        detail += (
            f'<div class="seg"><div class="sh"><span class="no">NO.{i}</span>'
            f'<b>片段{i}</b><span class="v">AIGC 值 {seg["value"]:.4f}</span>'
            f'<span class="meta">起于第 {seg["line"]} 行 · {seg["chars"]} 字</span></div>'
            f'<p>{html.escape(txt)}…</p></div>'
        )

    stamp = time.strftime("%Y/%m/%d %H:%M")
    esc = html.escape
    return f"""<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<title>{esc(chapter)} · 检测报告单</title>
<style>
@page {{ size: A4; margin: 16mm 14mm; }}
body {{ margin:0; background:#e9e9e9; font-family: "Songti SC","Source Han Serif SC",serif; color:#222; }}
.sheet {{ width:186mm; min-height:262mm; margin:10mm auto; background:#fff; padding:16mm 14mm;
         box-shadow:0 2px 12px rgba(0,0,0,.18); box-sizing:border-box; }}
.top {{ display:flex; justify-content:space-between; font-size:10.5pt; color:#555;
        border-bottom:1px solid #ddd; padding-bottom:6px; }}
h1 {{ text-align:center; font-size:22pt; letter-spacing:2px; margin:20px 0 14px; }}
.meta {{ font-size:11.5pt; line-height:1.9; margin-bottom:10px; }}
.meta b {{ font-weight:600; color:#333; }}
h2 {{ font-size:12.5pt; margin:20px 0 10px; padding-left:9px; border-left:5px solid #2f6fb3; }}
.pie {{ display:flex; align-items:center; gap:24px; }}
.lg {{ font-size:11pt; display:flex; align-items:center; gap:8px; margin:9px 0; }}
.lg i {{ width:16px; height:16px; display:inline-block; border-radius:2px; }}
.lg em {{ font-style:normal; color:#777; font-size:9.5pt; }}
.lg b {{ margin-left:auto; font-weight:600; }}
.bar {{ display:flex; height:26px; border-radius:3px; overflow:hidden; margin:8px 0 10px; }}
.bar span {{ display:block; height:100%; }}
table {{ width:100%; border-collapse:collapse; font-size:11pt; margin-top:6px; }}
th,td {{ border-bottom:1px solid #e6e6e6; padding:7px 6px; text-align:left; }}
th {{ color:#555; font-weight:600; background:#fafafa; }}
.seg {{ border:1px solid #e8e8e8; border-radius:4px; padding:10px 12px; margin:10px 0; }}
.seg .sh {{ display:flex; align-items:center; gap:12px; font-size:11pt; }}
.seg .no {{ background:#2f6fb3; color:#fff; padding:2px 8px; border-radius:3px; font-size:9.5pt; }}
.seg .v {{ color:#c1443c; font-weight:600; }}
.seg .meta {{ margin-left:auto; color:#888; font-size:9.5pt; }}
.seg p {{ font-size:10.5pt; line-height:1.85; color:#333; margin:8px 0 0; }}
.note {{ font-size:9.5pt; color:#777; line-height:1.7; border-top:1px dashed #ddd; padding-top:8px; }}
@media print {{ body{{background:#fff}} .sheet{{margin:0;box-shadow:none;width:auto;min-height:auto}} }}
</style></head><body><div class="sheet">
<div class="top"><span>{stamp}</span><span>AI 痕迹检测报告单 · {esc(chapter)}</span></div>
<h1>AI 痕迹检测报告单</h1>
<div class="meta">
<b>检测器：</b>{esc(provider)}<br>
<b>检测对象：</b>{esc(chapter)}<br>
<b>规模：</b>{len(rows)} 段，{total} 字符
</div>
<h2>检测结果</h2>
<div class="pie">{donut(parts)}<div style="flex:1">{legend_rows}</div></div>
<h2>分布图</h2>
<div class="bar">{bar}</div>
<div style="font-size:9.5pt;color:#666">{html.escape(scale_cfg['note'])}</div>
<h2>片段解析</h2>
<table><thead><tr><th>序号</th><th>片段</th><th>占全文比例</th><th>占字符数</th><th>AIGC 值</th></tr></thead>
<tbody>{table}</tbody></table>
<h2>片段详情</h2>{detail}
<div class="note">本单由 aigc_check.py 生成，用于定位值得复看的段落。分值只在本节内可比较，
不构成对作者身份的判断，也不可作为对外声明或学术不端的依据。</div>
</div></body></html>"""


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="按章生成检测报告单 HTML")
    ap.add_argument("csv", help="段落评分.csv")
    ap.add_argument("--out", default=None, help="输出目录（默认 CSV 同级/报告单）")
    ap.add_argument("--scale", default="local", choices=["local", "zhuque"])
    ap.add_argument("--provider", default=None, help="页面上显示的检测器名称")
    args = ap.parse_args(argv)

    csv_path = Path(args.csv)
    out_dir = Path(args.out) if args.out else csv_path.parent / "报告单"
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = load_rows(csv_path, args.scale)
    scale_cfg = SCALES[args.scale]
    provider = args.provider or ("zhuque（腾讯朱雀）" if args.scale == "zhuque"
                                 else "local（本地启发式，非朱雀）")

    by: dict[str, list[dict]] = {}
    for r in rows:
        by.setdefault(r["文件"], []).append(r)

    index_rows = []
    for name, group in by.items():
        group.sort(key=lambda r: int(r["行号"]))
        total = sum(int(r["字数"]) for r in group)
        smooth(group)
        segs = segments(group, scale_cfg["thresholds"])
        shares = [0.0, 0.0, 0.0]
        for s in segs:
            shares[s["cat"]] += s["chars"] / total
        chapter = name.replace("-C.tex", "").replace(".tex", "")
        (out_dir / f"{chapter}.html").write_text(
            sheet_for(chapter, group, scale_cfg, provider), encoding="utf-8")
        index_rows.append((chapter, len(group), total, shares))

    cards = "".join(
        f'<tr><td><a href="{html.escape(c)}.html">{html.escape(c)}</a></td>'
        f'<td>{n}</td><td>{t}</td>'
        + "".join(f'<td style="color:{COLORS[i]}">{fmt_pct(sh[i])}</td>' for i in range(3))
        + "</tr>" for c, n, t, sh in index_rows)

    (out_dir / "index.html").write_text(f"""<!doctype html><html lang="zh-CN"><head>
<meta charset="utf-8"><title>分章检测报告单</title>
<style>body{{font-family:-apple-system,"Songti SC",serif;margin:40px;color:#222}}
table{{border-collapse:collapse;font-size:13px}}th,td{{border-bottom:1px solid #e5e5e5;padding:8px 14px;text-align:left}}
th{{background:#fafafa}}a{{color:#2f6fb3;text-decoration:none}}
.note{{color:#777;font-size:12px;line-height:1.8;max-width:820px}}</style></head><body>
<h2>分章检测报告单（{len(index_rows)} 份）</h2>
<p class="note">检测器：{html.escape(provider)}。{"相对位次刻度" if args.scale=="local" else "朱雀 AIGC 值"}：
{html.escape(scale_cfg['labels'][0])} / {html.escape(scale_cfg['labels'][1])} / {html.escape(scale_cfg['labels'][2])}。
点章节名查看报告单，浏览器打印即可得到 A4 单页。</p>
<table><thead><tr><th>章节</th><th>段数</th><th>字符</th>
<th>{html.escape(scale_cfg['labels'][0])}</th><th>{html.escape(scale_cfg['labels'][1])}</th>
<th>{html.escape(scale_cfg['labels'][2])}</th></tr></thead><tbody>{cards}</tbody></table>
</body></html>""", encoding="utf-8")

    print(f"已生成 {len(index_rows)} 份报告单 → {out_dir}/index.html")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
