#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把登记表汇总成一张分章结果表（按字符加权合并各块）。

用法：
    python3 AIGC检测/汇总结果.py

输出：
    结果/分章结果.csv
    结果/分章结果.md
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent
REG = BASE / "输出" / "C-朱雀送检" / "登记表.csv"
OUT_CSV = BASE / "结果" / "分章结果.csv"
OUT_MD = BASE / "结果" / "分章结果.md"


def order(ch: str) -> tuple:
    m = re.match(r"chapter(\d+)$", ch)
    if m:
        return (0, int(m.group(1)))
    return (1, {"前言": 0, "导论": 1, "符号与约定": 2}.get(ch, 9))


def main() -> int:
    all_rows = list(csv.DictReader(REG.open(encoding="utf-8-sig")))
    rows = [r for r in all_rows
            if (r.get("疑似AI%") or "").strip() and "部分" not in (r.get("范围") or "")]
    pending = sorted({r["章节"] for r in all_rows if "部分" in (r.get("范围") or "")})
    by: dict[str, list] = {}
    for r in rows:
        by.setdefault(r["章节"], []).append(r)

    out = []
    for ch, rs in by.items():
        w = sum(int(r["字符数"] or 0) or 1 for r in rs)
        def wavg(key: str) -> float:
            return sum(float(r[key]) * (int(r["字符数"] or 0) or 1) for r in rs) / w
        dates = sorted({(r.get("检测时间") or "")[:10] for r in rs if r.get("检测时间")})
        out.append({
            "章节": ch,
            "块数": len(rs),
            "字符数": sum(int(r["字符数"] or 0) for r in rs),
            "人工特征%": round(wavg("人工特征%"), 2),
            "疑似AI%": round(wavg("疑似AI%"), 2),
            "AI特征%": round(wavg("AI特征%"), 2),
            "日期": dates[-1] if dates else "",
        })
    out.sort(key=lambda r: order(r["章节"]))

    OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=["章节", "块数", "字符数", "人工特征%", "疑似AI%", "AI特征%", "日期"])
        wr.writeheader()
        wr.writerows(out)

    L = ["# 分章检测结果（朱雀口径）", "",
         f"共 {len(out)} 章、{sum(r['块数'] for r in out)} 份报告、"
         f"{sum(r['字符数'] for r in out):,} 字符。数值按各块字符数加权合并。", "",
         "| 章节 | 块数 | 字符数 | 人工特征% | 疑似AI% | AI特征% | 检测日期 |",
         "|---|---:|---:|---:|---:|---:|---|"]
    for r in out:
        L.append(f"| {r['章节']} | {r['块数']} | {r['字符数']:,} | {r['人工特征%']:.2f} | "
                 f"{r['疑似AI%']:.2f} | {r['AI特征%']:.2f} | {r['日期']} |")
    nz = [r for r in out if r["疑似AI%"] > 0]
    if pending:
        L += ["", f"> 覆盖率不足 95% 的章未计入：{('、'.join(pending))}。", ""]
    L += ["", f"疑似占比为 0 的章：**{len(out)-len(nz)}/{len(out)}**；"
              f"最高的章：**{max(out, key=lambda r: r['疑似AI%'])['章节']}**"
              f"（{max(r['疑似AI%'] for r in out):.2f}%）。", ""]
    OUT_MD.write_text("\n".join(L), encoding="utf-8")

    print("\n".join(L))
    print(f"CSV → {OUT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
