#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把手工登记的朱雀结果与本地评分做同向性对照。

用法：
    python3 对照.py                      # 默认读 输出/C-朱雀送检/登记表.csv
    python3 对照.py --registry 登记表.csv --local 输出/C-段落评分.csv

登记表里「疑似AI%」「AI特征%」为空的块视为未检测，自动跳过。
只要填了任意一行，就能跑。
"""

from __future__ import annotations

import argparse
import csv
import statistics
from pathlib import Path


def kendall_tau(xs: list[float], ys: list[float]) -> tuple[float, int, int]:
    n = len(xs)
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            s = (xs[i] - xs[j]) * (ys[i] - ys[j])
            if s > 0:
                conc += 1
            elif s < 0:
                disc += 1
    return (conc - disc) / max(1, conc + disc), conc, disc


def read_registry(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    with path.open(encoding="utf-8-sig") as fh:
        for row in csv.DictReader(fh):
            raw = (row.get("疑似AI%") or "").strip()
            if not raw:
                continue
            try:
                sus = float(raw)
                ai = float((row.get("AI特征%") or "0").strip() or 0)
                chars = int(row.get("字符数") or 0) or 1   # 未知时按等权处理
            except ValueError:
                continue
            if "部分" in (row.get("范围") or ""):
                continue          # 覆盖不全的提交不计入对照
            ch = row["章节"].strip()
            d = out.setdefault(ch, {"chars": 0, "sus": 0.0, "ai": 0.0, "blocks": 0})
            d["chars"] += chars
            d["sus"] += sus * chars / 100
            d["ai"] += ai * chars / 100
            d["blocks"] += 1
    for d in out.values():
        d["ratio"] = 100 * (d["sus"] + d["ai"]) / max(1, d["chars"])
    return out


def read_local(path: Path) -> dict[str, float]:
    """读分章本地分。支持两种格式：分章汇总表，或逐段的段落评分表。"""
    with path.open(encoding="utf-8-sig") as fh:
        rows = list(csv.DictReader(fh))
    if rows and "本地加权分" in rows[0]:
        return {r["章节"]: float(r["本地加权分"]) for r in rows}
    by: dict[str, list] = {}
    for row in rows:
        by.setdefault(row["文件"], []).append(row)
    return {f.replace("-C.tex", ""):
            sum(int(r["评分"]) * int(r["字数"]) for r in rs) / sum(int(r["字数"]) for r in rs)
            for f, rs in by.items()}


def main() -> int:
    base = Path(__file__).resolve().parent
    ap = argparse.ArgumentParser()
    ap.add_argument("--registry", default=str(base / "输出" / "C-朱雀送检" / "登记表.csv"))
    ap.add_argument("--local", default=str(base / "输出" / "C-朱雀送检" / "分章本地分.csv"))
    ap.add_argument("--out", default=str(base / "输出" / "C-朱雀送检" / "对照报告.md"))
    args = ap.parse_args()

    reg = read_registry(Path(args.registry))
    if not reg:
        print("登记表里还没有检测结果。先按 操作说明.md 跑几章朱雀，再把百分比填进去。")
        return 1
    local = read_local(Path(args.local))

    chapters = [c for c in reg if c in local]
    if not chapters:
        print("登记的章节名与本地 CSV 对不上，检查「章节」列是否形如 chapter20")
        return 1

    rows = []
    for c in chapters:
        rows.append({
            "章节": c,
            "本地分": local[c],
            "朱雀疑似+AI(%)": reg[c]["ratio"],
            "块数": reg[c]["blocks"],
            "字符": reg[c]["chars"],
        })

    if len(rows) < 3:
        print(f"可用章节只有 {len(rows)} 个，不足以算 τ；先再跑几章。")
        for r in rows:
            print(f"  {r['章节']}: 本地 {r['本地分']:.1f}，朱雀疑似+AI {r['朱雀疑似+AI(%)']:.1f}%")
        return 0

    xs = [r["本地分"] for r in rows]
    ys = [r["朱雀疑似+AI(%)"] for r in rows]
    tau, conc, disc = kendall_tau(xs, ys)

    by_local = sorted(rows, key=lambda r: -r["本地分"])
    by_zq = sorted(rows, key=lambda r: -r["朱雀疑似+AI(%)"])
    for i, r in enumerate(by_local, 1):
        r["本地排名"] = i
    for i, r in enumerate(by_zq, 1):
        r["朱雀排名"] = i

    if tau >= 0.5:
        verdict = "同向：本地排序与朱雀大体一致，可以放心用本地排序挑段落。"
    elif tau >= 0:
        verdict = "弱同向：方向大体一致但排序不稳，本地只宜粗筛。"
    elif tau > -0.5:
        verdict = "不同向：两者测的不是同一件事，对外以朱雀为准，本地仅作切分工具。"
    else:
        verdict = "明显反向：本地高分段落反而被朱雀判为更「人写」，说明本指标在此语料上失效。"

    L = ["# 朱雀 × 本地 对照报告", "",
         f"已比对 {len(rows)} 章，Kendall τ = **{tau:+.2f}**（同序 {conc} 对，逆序 {disc} 对）。", "",
         f"**判断：{verdict}**", "",
         "| 章节 | 本地分 | 本地排名 | 朱雀疑似+AI(%) | 朱雀排名 | 块数 | 字符 |",
         "|---|---:|---:|---:|---:|---:|---:|"]
    for r in sorted(rows, key=lambda r: -r["本地分"]):
        L.append(f"| {r['章节']} | {r['本地分']:.1f} | {r['本地排名']} | "
                 f"{r['朱雀疑似+AI(%)']:.1f} | {r['朱雀排名']} | {r['块数']} | {r['字符']} |")
    L += ["", "## 读数提醒", "",
          "- n≤10 时 τ 的方向意义大于数值大小，不要解读小数点后两位。",
          "- 朱雀的百分比是「被判为疑似的字符占比」，不是「AI 写作的字数」。",
          "- 若各章朱雀值都接近 0，说明这批文本在朱雀口径下没有可探信号；此时 τ 无意义，看「都低」这个结论。",
          ""]
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    print(f"τ = {tau:+.2f}；{verdict}")
    print(f"报告：{out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
