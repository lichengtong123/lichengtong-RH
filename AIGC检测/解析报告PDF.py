#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""解析朱雀报告单 PDF，把结果写进登记表，并出圆环/上半部分图。

用法：
    python3 解析报告PDF.py 朱雀/*.pdf                  # 解析 + 填表 + 出图
    python3 解析报告PDF.py 朱雀/*.pdf --no-images      # 只解析
    python3 解析报告PDF.py 朱雀/*.pdf --append         # 登记表里没有的章也追加

做的事：
 1. 从 PDF 文本层读出「文件名 / 检测时间 / 片段表」；
 2. 按 AIGC 值把片段归入 人工特征(<0.5) / 疑似AI(0.5–0.99) / AI特征(≥0.99)，
    按字符数加权得到三个百分比；
 3. 与送检文件比对，算出覆盖率（低于 95% 标为“部分”，对照时跳过）；
 4. 回填 登记表.csv；
 5. 可选：生成上半部分 PNG 与裁剪版 PDF。
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
from pathlib import Path

BASE = Path(__file__).resolve().parent
REGISTRY = BASE / "输出" / "C-朱雀送检" / "登记表.csv"
REPORTS_DIR = BASE / "朱雀回文"
SEND_DIRS = [BASE / "输出" / "C-朱雀送检" / "txt", BASE / "输出" / "C-朱雀送检-切块" / "txt"]
RESULT_CSV = BASE / "输出" / "C-朱雀送检" / "朱雀解析.csv"

ROW_RE = re.compile(r"^\s*(\d+)\s+片段(\d+)\s+([\d.]+)%\s+(\d+)\s+([\d.]+)\s*$", re.M)


def pdf_text(pdf: Path) -> str:
    return subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                          check=True, capture_output=True, text=True).stdout


def parse(pdf: Path) -> dict:
    text = pdf_text(pdf)
    m = re.search(r"文件名：\s*(\S+)", text)
    fname = m.group(1) if m else ""
    m = re.search(r"检测时间：\s*([\d/: ]+)", text)
    when = m.group(1).strip() if m else ""
    segs = [{"片段": int(a), "占比": float(b), "字符": int(c), "AIGC": float(d)}
            for _, a, b, c, d in ROW_RE.findall(text)]
    total = sum(s["字符"] for s in segs)
    buckets = {"人工特征%": 0.0, "疑似AI%": 0.0, "AI特征%": 0.0}
    for s in segs:
        k = "人工特征%" if s["AIGC"] < 0.5 else ("疑似AI%" if s["AIGC"] < 0.99 else "AI特征%")
        buckets[k] += s["字符"] / total if total else 0
    chapter = re.sub(r"-C(?:-\d+)?\.txt$", "", fname) if fname else \
        re.sub(r"-C-\d+$|-C$", "", pdf.stem)
    return {
        "pdf": pdf.name,
        "文件": fname,
        "章节": chapter,
        "检测时间": when,
        "片段数": len(segs),
        "覆盖字符": total,
        "人工特征%": round(buckets["人工特征%"] * 100, 2),
        "疑似AI%": round(buckets["疑似AI%"] * 100, 2),
        "AI特征%": round(buckets["AI特征%"] * 100, 2),
        "segments": segs,
    }


def chapter_total(chapter: str) -> int | None:
    """该章所有送检文件（整章或切块）的字符总数。"""
    total = 0
    found = False
    for d in SEND_DIRS:
        for f in d.glob(f"{chapter}-C*.txt"):
            found = True
            total += len(f.read_text(encoding="utf-8"))
    return total if found else None


def source_chars(fname: str) -> int | None:
    if not fname:
        return None
    for d in SEND_DIRS:
        p = d / fname
        if p.exists():
            return len(p.read_text(encoding="utf-8"))
    return None


def apply_images(pdf: Path, out_dir: Path) -> None:
    subprocess.run(["python3", str(BASE / "截取报告上半.py"), str(pdf), "-o", str(out_dir)],
                   check=False, capture_output=True)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pdfs", nargs="*", help="PDF 文件或目录；留空则读取 AIGC检测/朱雀回文/*.pdf")
    ap.add_argument("--registry", default=str(REGISTRY))
    ap.add_argument("--append", action="store_true", help="登记表里没有的章也追加一行")
    ap.add_argument("--no-images", action="store_true")
    args = ap.parse_args()

    targets: list[Path] = []
    for a in (args.pdfs or [str(REPORTS_DIR)]):
        q = Path(a)
        if q.is_dir():
            targets.extend(sorted(q.glob("*.pdf")))
        elif q.exists():
            targets.append(q)
        else:
            print(f"跳过（找不到）：{a}")
    if not targets:
        print(f"没有找到 PDF：{REPORTS_DIR}")
        return 1

    results = []
    for p in targets:
        pdf = Path(p)
        r = parse(pdf)
        total = source_chars(r["文件"])
        r["文件覆盖"] = round(100 * r["覆盖字符"] / total, 1) if total else None
        ctotal = chapter_total(r["章节"])
        r["覆盖率"] = round(100 * r["覆盖字符"] / ctotal, 1) if ctotal else None
        results.append(r)
        if not args.no_images:
            apply_images(pdf, pdf.parent / "图")

    reg_path = Path(args.registry)
    rows = list(csv.DictReader(reg_path.open(encoding="utf-8-sig"))) if reg_path.exists() else []
    fields = rows[0].keys() if rows else ["章节", "文件", "字符数", "人工特征%", "疑似AI%", "AI特征%", "检测时间", "范围"]

    hit = 0
    for r in results:
        target = None
        for row in rows:
            if row.get("章节") == r["章节"] and (not r["文件"] or not row.get("文件")
                                                 or row["文件"] == r["文件"]):
                target = row
                break
        if target is None and args.append:
            target = {k: "" for k in fields}
            target.update({"章节": r["章节"], "文件": r["文件"]})
            rows.append(target)
        if target is None:
            print(f"跳过（登记表无此章）：{r['文件']}")
            continue
        update = {
            "人工特征%": f"{r['人工特征%']:.2f}",
            "疑似AI%": f"{r['疑似AI%']:.2f}",
            "AI特征%": f"{r['AI特征%']:.2f}",
            "检测时间": r["检测时间"],
            "范围": "整章" if (r["覆盖率"] is None or r["覆盖率"] >= 95) else f"部分({r['覆盖率']}%)",
        }
        if r["文件"]:
            update["文件"] = r["文件"]
        src = source_chars(r["文件"]) or r["覆盖字符"]
        if src:
            update["字符数"] = str(src)
        target.update(update)
        hit += 1

    # 按“整章覆盖率”重标范围：切块章的各块单独看都<95%，要按合计判断
    totals: dict[str, int] = {}
    for row in rows:
        if (row.get("疑似AI%") or "").strip():
            totals[row.get("章节", "")] = totals.get(row.get("章节", ""), 0) + int(row.get("字符数") or 0)
    for row in rows:
        ch = row.get("章节", "")
        if not (row.get("疑似AI%") or "").strip():
            continue
        ctotal = chapter_total(ch)
        if ctotal:
            cov = 100.0 * totals.get(ch, 0) / ctotal
            row["范围"] = "整章" if cov >= 95 else f"部分({cov:.1f}%)"

    with reg_path.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(fields), extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    RESULT_CSV.parent.mkdir(parents=True, exist_ok=True)
    with RESULT_CSV.open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["pdf", "文件", "章节", "检测时间", "片段数",
                                           "覆盖字符", "文件覆盖", "覆盖率", "人工特征%", "疑似AI%", "AI特征%"],
                           extrasaction="ignore")
        w.writeheader()
        w.writerows(results)

    print(f"{'文件':<26}{'章':<12}{'章覆盖':>7}  {'人工':>7}{'疑似':>7}{'AI':>7}")
    for r in results:
        cov = f"{r['覆盖率']}%" if r["覆盖率"] is not None else "?"
        print(f"{r['文件']:<26}{r['章节']:<12}{cov:>6}  {r['人工特征%']:>7.2f}{r['疑似AI%']:>7.2f}{r['AI特征%']:>7.2f}")
    print(f"\n已回填 {hit} 行 → {reg_path}")
    print(f"明细 → {RESULT_CSV}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
