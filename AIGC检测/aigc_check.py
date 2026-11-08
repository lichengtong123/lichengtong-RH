#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把书稿正文切成可送检的段落，逐段给出「模板化/AI 痕迹」评分并汇总。

这个脚本做两件事：

1. 切分：读 .tex / .md / .txt，去掉 LaTeX 命令、公式环境、图表、注释、
   页边注，只留下能送进检测器的自然语言段落，并记下每段的出处（文件:行号）。
2. 打分：默认用离线启发式（--provider local），也可以接腾讯云朱雀
   （--provider zhuque，需要网关与 API Key）。

🔴 必须记住的前提
----------------
任何检测器输出的都是「这段文字像不像机器写的」的概率估计，不是
「这段有多少字是 AI 写的」这一事实。同一段文字换一个站点，0% 与 95%
都出现过。本脚本的 local 评分尤其只是一个可解释的模板化指数，
它的用途是**定位值得复看的段落**，不是给出一个可以写进报告的百分比。

另外，切分阶段会剥掉全部公式与符号，只留自然语言骨架。因此数学密集的
段落看起来会短、会碎，这是清洗的产物，不是文风问题。

用法
----
    python3 aigc_check.py extract 书稿/chapter1-B.tex -o 输出/段落.csv
    python3 aigc_check.py scan 书稿/chapter*-B.tex --provider local
    python3 aigc_check.py scan 书稿/chapter1-B.tex --provider zhuque

不带子命令时等同于 scan，默认输出到脚本同级的 输出/ 目录。
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, Iterator, Sequence

# --------------------------------------------------------------------------
# 常量
# --------------------------------------------------------------------------

CJK = r"\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff"
CJK_RE = re.compile(f"[{CJK}]")
LATIN_DIGIT_RE = re.compile(r"[0-9A-Za-z]")
SENT_RE = re.compile(r"[^。！？!?；;\n]+[。！？!?；;\n]?")
PUNCT_CHARS = set("，。、；：！？「」『』（）【】《》“”‘’—…·,.;:!?\"'()[]{}")

# 整块丢弃的环境：公式、图表、代码、逐字环境
SKIP_ENVS = (
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "eqnarray", "eqnarray*", "multline", "multline*", "flalign", "flalign*",
    "alignat", "alignat*", "split", "aligned", "array", "matrix", "pmatrix",
    "bmatrix", "vmatrix", "Vmatrix", "smallmatrix", "cases", "figure",
    "figure*", "table", "table*", "tabular", "tabular*", "tabularx",
    "longtable", "tikzpicture", "verbatim", "lstlisting", "comment",
    "thebibliography", "wrapfigure", "subfigure", "pspicture",
    # pgfplots 画图环境：里面是坐标数据，不是正文
    "axis", "semilogxaxis", "semilogyaxis", "loglogaxis", "polaraxis",
    "groupplot", "tikz", "pgfonlayer", "scope",
)

# 标题类命令：连同参数一起删除，并把该行当作段落边界
HEADING_CMDS = (
    "chapter", "chapter*", "section", "section*", "subsection", "subsection*",
    "subsubsection", "subsubsection*", "paragraph", "subparagraph",
    "part", "part*", "caption", "title", "author", "date",
)

# 保留参数文字的排版命令
KEEP_CMDS = (
    "emph", "textbf", "textit", "textsl", "textsc", "texttt", "textrm",
    "textsf", "textnormal", "text", "mbox", "hbox", "underline", "uline",
    "MakeUppercase", "MakeLowercase", "textsuperscript", "textsubscript",
    "foreignlanguage",
)

# 连同参数一起丢弃的命令
DROP_CMDS = (
    "cite", "citep", "citet", "citealp", "citeauthor", "citeyear",
    "parencite", "textcite", "ref", "eqref", "autoref", "pageref", "cref",
    "Cref", "label", "index", "glossary", "footnote", "footnotetext",
    "footnotemark", "includegraphics", "input", "include", "bibliography",
    "bibliographystyle", "addcontentsline", "addtocontents", "vspace",
    "hspace", "vskip", "hskip", "setlength", "addtolength", "phantom",
    "hphantom", "vphantom", "bibitem", "noindent", "indent", "centering",
    "raggedright", "raggedleft", "linebreak", "pagebreak", "newpage",
    "clearpage", "tableofcontents", "listoffigures", "listoftables",
    "maketitle", "frontmatter", "mainmatter", "backmatter", "appendix",
    "bibliographyitem", "nolinenumbers", "linenumbers", "protect",
)

MATH_ENVS = (
    "equation", "equation*", "align", "align*", "gather", "gather*",
    "eqnarray", "eqnarray*", "multline", "multline*", "flalign", "flalign*",
    "alignat", "alignat*", "split", "aligned", "array", "matrix", "pmatrix",
    "bmatrix", "vmatrix", "Vmatrix", "smallmatrix", "cases",
)
OTHER_ENVS = tuple(e for e in SKIP_ENVS if e not in MATH_ENVS)

MATH_MARK = "〔式〕"
BLOCK_MATH_RE = re.compile(
    r"\\begin\{(" + "|".join(re.escape(e) for e in MATH_ENVS) + r")\}\s*(?:\[[^\]]*\])?.*?\\end\{\1\}",
    re.S,
)
BLOCK_OTHER_RE = re.compile(
    r"\\begin\{(" + "|".join(re.escape(e) for e in OTHER_ENVS) + r")\}\s*(?:\[[^\]]*\])?.*?\\end\{\1\}",
    re.S,
)
DISPLAY_MATH_RE = re.compile(r"\\\[.*?\\\]|\\\(.*?\\\)|\$\$.*?\$\$", re.S)
BEGIN_END_RE = re.compile(r"\\(?:begin|end)\s*\{[^{}\n]*\}(?:\s*\[[^\]\n]*\])?")
TEXORPDF_RE = re.compile(r"\\texorpdfstring\s*\{([^{}]*)\}\s*\{([^{}]*)\}")
ACCENT_RE = re.compile(r"\\[`'\"^~=.]\s*\{?([A-Za-z])\}?")
SPECIAL_LETTERS = {
    "ss": "ss", "ae": "ae", "AE": "AE", "oe": "oe", "OE": "OE",
    "aa": "a", "AA": "A", "o": "o", "O": "O", "l": "l", "L": "L",
    "i": "i", "j": "j",
}

# 高精度套话标记：只收真正成串出现的说法
STOCK_PHRASES = (
    "综上所述", "总而言之", "总的来说", "值得注意的是", "需要指出的是",
    "不容忽视", "至关重要", "具有重要意义", "起到了重要作用", "发挥重要作用",
    "在当今", "随着科技的", "随着人工智能", "随着社会的", "在信息化时代",
    "从某种意义上说", "可以说", "可以看出", "由此可见", "众所周知",
    "毋庸置疑", "前所未有", "赋能", "助力", "抓手", "闭环", "底层逻辑",
    "多维度", "全链路", "生态化", "范式", "迭代升级", "本文认为",
    "笔者以为", "值得深入探讨", "提供有益借鉴", "奠定坚实基础", "深入研究",
)

CONNECTOR_RE = re.compile(
    r"(首先|其次|再次|最后|一方面|另一方面|综上所述|总之|因而|因此|由此可见)"
)

LABELS = ((66, "高"), (40, "中"))


# --------------------------------------------------------------------------
# LaTeX 清洗
# --------------------------------------------------------------------------

def strip_comment(line: str) -> str:
    """去掉 % 注释，但保留 \\% 之类的转义。"""
    out = []
    i = 0
    n = len(line)
    while i < n:
        ch = line[i]
        if ch == "\\" and i + 1 < n:
            out.append(line[i:i + 2])
            i += 2
            continue
        if ch == "%":
            break
        out.append(ch)
        i += 1
    return "".join(out)


def _find_matching_brace(s: str, open_idx: int) -> int:
    depth = 0
    for j in range(open_idx, len(s)):
        if s[j] == "{":
            depth += 1
        elif s[j] == "}":
            depth -= 1
            if depth == 0:
                return j
    return -1


def unwrap_commands(s: str, names: Sequence[str]) -> str:
    """\\emph{文字} -> 文字，可处理嵌套的花括号。"""
    rx = re.compile(r"\\(?:" + "|".join(re.escape(n) for n in names) + r")\*?\s*(?=\{)")
    for _ in range(300):
        m = rx.search(s)
        if not m:
            return s
        open_idx = m.end()
        close_idx = _find_matching_brace(s, open_idx)
        if close_idx < 0:
            return s[:m.start()] + s[open_idx + 1:]
        s = s[:m.start()] + s[open_idx + 1:close_idx] + s[close_idx + 1:]


def drop_commands(s: str, names: Sequence[str]) -> str:
    """\\label{...} 之类：连同可选的 [..] 与 {...} 一起删除。"""
    rx = re.compile(
        r"\\(?:" + "|".join(re.escape(n) for n in names) + r")\*?\s*(?:\[[^\]]*\])?\s*(?=\{)"
    )
    for _ in range(300):
        m = rx.search(s)
        if not m:
            break
        open_idx = m.end()
        close_idx = _find_matching_brace(s, open_idx)
        if close_idx < 0:
            s = s[:m.start()] + s[open_idx + 1:]
            break
        s = s[:m.start()] + s[close_idx + 1:]
    rx2 = re.compile(r"\\(?:" + "|".join(re.escape(n) for n in names) + r")\*?(?![a-zA-Z])")
    return rx2.sub("", s)


def _blank_preserve_lines(match: re.Match) -> str:
    return "\n" * match.group(0).count("\n")


def _mark_preserve_lines(match: re.Match) -> str:
    """公式块换成占位符，并保留原有行数：段落不因公式而断开。"""
    return "\n".join([MATH_MARK] * (match.group(0).count("\n") + 1))


def clean_inline(s: str) -> str:
    """处理单行内联标记。"""
    s = TEXORPDF_RE.sub(lambda m: m.group(2), s)          # 取文字版本
    for _ in range(6):
        s2 = re.sub(r"\\href\s*\{[^{}]*\}\s*\{([^{}]*)\}", r"\1", s)
        if s2 == s:
            break
        s = s2
    s = drop_commands(s, DROP_CMDS)
    s = unwrap_commands(s, KEEP_CMDS)
    s = ACCENT_RE.sub(lambda m: m.group(1), s)
    s = re.sub(r"\\(ss|ae|AE|oe|OE|aa|AA|o|O|l|L)(?![a-zA-Z])",
               lambda m: SPECIAL_LETTERS.get(m.group(1), m.group(1)), s)
    s = re.sub(r"\$[^$]*\$", " ", s)                      # 行内公式
    s = re.sub(r"\^\{[^{}]*\}|_\{[^{}]*\}|\^[A-Za-z0-9]|_[A-Za-z0-9]", " ", s)
    s = re.sub(r"\\[a-zA-Z]+\*?", " ", s)                 # 剩余命令
    s = re.sub(r"\\[0-9.]+\s*", " ", s)                   # 间距命令
    s = s.replace("~", " ").replace("\\\\", " ")
    s = s.replace("---", "—").replace("--", "–")
    s = re.sub(r"[{}]", "", s)
    s = re.sub(r"[\\|`^_]", " ", s)
    s = re.sub(r"[ \t\u3000]+", " ", s)
    return s.strip()


def clean_tex_lines(text: str) -> list[tuple[int, str]]:
    """逐行清洗，返回 (行号, 清洗后文本)；空串表示段落边界。"""
    # 1. 去注释（逐行，保留换行）
    text = "\n".join(strip_comment(line) for line in text.splitlines())
    # 2. 整块删除公式环境与行间公式，用换行占位以保住行号
    prev = None
    while prev != text:
        prev = text
        text = BLOCK_MATH_RE.sub(_mark_preserve_lines, text)
        text = BLOCK_OTHER_RE.sub(_blank_preserve_lines, text)
    text = DISPLAY_MATH_RE.sub(_mark_preserve_lines, text)
    # 3. 删掉 \begin{...} / \end{...}（含可选参数），避免环境名漏成正文
    text = BEGIN_END_RE.sub("", text)

    out: list[tuple[int, str]] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw
        heading = False
        for cmd in HEADING_CMDS:
            pat = re.compile(r"\\" + re.escape(cmd) + r"\s*\{")
            m = pat.search(line)
            if m:
                open_idx = m.end() - 1
                close_idx = _find_matching_brace(line, open_idx)
                line = line[:m.start()] + (line[close_idx + 1:] if close_idx > 0 else "")
                heading = True
        if re.search(r"\\item\b", raw):
            out.append((max(1, lineno - 1), ""))          # 条目开新段
        line = clean_inline(line)
        if heading or not line:
            out.append((lineno, ""))
        else:
            out.append((lineno, line))
    return out


def clean_plain_lines(text: str) -> list[tuple[int, str]]:
    return [(i, re.sub(r"\s+", " ", line).strip())
            for i, line in enumerate(text.splitlines(), 1)]


# --------------------------------------------------------------------------
# 切段
# --------------------------------------------------------------------------

@dataclass
class Paragraph:
    pid: str
    file: str
    line: int
    chars: int
    cjk: int
    text: str


def split_chunks(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    parts: list[str] = []
    rest = text
    while len(rest) > limit:
        window = rest[:limit]
        cut = max(window.rfind("。"), window.rfind("；"), window.rfind("！"), window.rfind("？"))
        cut = limit if cut < limit // 2 else cut + 1
        parts.append(rest[:cut].strip())
        rest = rest[cut:].strip()
    if rest:
        parts.append(rest)
    return [p for p in parts if p]


def iter_paragraphs(
    path: Path,
    min_chars: int = 60,
    chunk: int = 1000,
    rel_to: Path | None = None,
    merge_short: bool = True,
) -> Iterator[Paragraph]:
    """把一份文件切成段落。短段并入前一段，公式由占位符承担，不会切断段落。"""
    raw = path.read_text(encoding="utf-8", errors="replace")
    lines = clean_tex_lines(raw) if path.suffix.lower() == ".tex" else clean_plain_lines(raw)
    name = str(path.relative_to(rel_to)) if rel_to else path.name

    groups: list[tuple[int, str]] = []
    buf: list[str] = []
    start = 0
    for lineno, cleaned in lines:
        if not cleaned:
            if buf:
                groups.append((start, " ".join(buf)))
                buf = []
            continue
        if not buf:
            start = lineno
        buf.append(cleaned)
    if buf:
        groups.append((start, " ".join(buf)))

    texts: list[list] = []
    for start, pieces in groups:
        t = re.sub(r"\s+", " ", pieces.replace(MATH_MARK, " ")).strip()
        if t:
            texts.append([start, t])

    if merge_short:
        merged: list[list] = []
        for start, t in texts:
            if merged and len(CJK_RE.findall(t)) < min_chars:
                merged[-1][1] = merged[-1][1] + " " + t
            else:
                merged.append([start, t])
        texts = merged

    idx = 0
    seen: set[str] = set()
    for start, text in texts:
        if len(CJK_RE.findall(text)) < min_chars:
            continue
        for part in split_chunks(text, chunk):
            key = hashlib.sha1(part.encode()).hexdigest()
            if key in seen:
                continue
            seen.add(key)
            if len(CJK_RE.findall(part)) < min_chars:
                continue
            idx += 1
            yield Paragraph(
                pid=f"{path.stem}-{idx:03d}",
                file=name,
                line=start,
                chars=len(part),
                cjk=len(CJK_RE.findall(part)),
                text=part,
            )


# --------------------------------------------------------------------------
# 离线启发式评分（模板化指数，不是 AI 比例）
# --------------------------------------------------------------------------

@dataclass
class Score:
    score: int
    label: str
    features: dict


def sentence_lengths(text: str) -> list[int]:
    return [len(s.strip()) for s in SENT_RE.findall(text) if len(s.strip()) > 3]


def label_of(score: int) -> str:
    for threshold, name in LABELS:
        if score >= threshold:
            return name
    return "低"


def local_score(text: str) -> Score:
    cjk = max(1, len(CJK_RE.findall(text)))
    lengths = sentence_lengths(text)
    cv = (statistics.pstdev(lengths) / statistics.mean(lengths)) if len(lengths) > 1 and sum(lengths) else 0.0

    stock = sum(text.count(p) for p in STOCK_PHRASES)
    stock_density = stock * 100.0 / cjk

    connectors = len(CONNECTOR_RE.findall(text))
    punct_kinds = len({ch for ch in text if ch in PUNCT_CHARS})
    tech_density = len(LATIN_DIGIT_RE.findall(text)) * 100.0 / cjk

    score = 50.0
    score += min(30.0, stock_density * 25.0)
    if cv:
        if cv < 0.30:
            score += 12
        elif cv < 0.45:
            score += 8
        elif cv < 0.60:
            score += 4
        if cv > 1.0:
            score -= 6
    if connectors >= 3:
        score += 10
    elif connectors == 2:
        score += 6
    elif connectors == 1:
        score += 3
    if punct_kinds <= 3:
        score += 6
    elif punct_kinds <= 5:
        score += 3
    score -= min(12.0, tech_density * 4.0)

    score = int(round(max(0.0, min(100.0, score))))
    return Score(score, label_of(score), {
        "句数": len(lengths),
        "句长变异系数": round(cv, 3),
        "套话密度(每百字)": round(stock_density, 3),
        "连接词数": connectors,
        "标点种类": punct_kinds,
        "数字字母密度(每百字)": round(tech_density, 3),
    })


# --------------------------------------------------------------------------
# 朱雀（腾讯云 EdgeOne MCP 网关）评分
# --------------------------------------------------------------------------

def _to_percent(value) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        v = float(value)
        return v * 100 if 0 <= v <= 1.0001 else v
    if isinstance(value, str):
        m = re.search(r"([0-9]+(?:\.[0-9]+)?)\s*%", value)
        if m:
            return float(m.group(1))
        try:
            v = float(value)
            return v * 100 if 0 <= v <= 1.0001 else v
        except ValueError:
            return None
    return None


def find_ai_share(obj) -> float | None:
    """在未知 JSON 结构里找「AI 占比」字段。"""
    if isinstance(obj, dict):
        for key, value in obj.items():
            if re.search(r"(ai|aigc|machine|机器)", key, re.I) and re.search(
                r"(rate|ratio|prob|percent|share|score|比例|占比|概率)", key, re.I
            ):
                p = _to_percent(value)
                if p is not None:
                    return p
        for value in obj.values():
            p = find_ai_share(value)
            if p is not None:
                return p
    elif isinstance(obj, list):
        for value in obj:
            p = find_ai_share(value)
            if p is not None:
                return p
    # 兜底：单键结果 {"AI": 87.5} 这类
    if isinstance(obj, dict) and len(obj) == 1:
        key, value = next(iter(obj.items()))
        if re.fullmatch(r"(ai|aigc|机器|生成)", str(key), re.I):
            return _to_percent(value)
    return None


class ZhuqueProvider:
    """腾讯云 EdgeOne AI 网关的朱雀文本检测。

    需要的环境变量：
        ZHUQUE_GATEWAY_URL  创建网关后获得的域名
        ZHUQUE_API_KEY      网关的 API Key

    文档：https://cloud.tencent.cn/document/product/1552/135974
    """

    def __init__(self, dump: bool = False, sleep: float = 1.5, timeout: float = 60.0):
        self.gateway = os.environ.get("ZHUQUE_GATEWAY_URL", "").rstrip("/")
        self.key = os.environ.get("ZHUQUE_API_KEY", "")
        self.dump = dump
        self.sleep = sleep
        self.timeout = timeout
        if not self.gateway or not self.key:
            raise SystemExit(
                "缺少环境变量 ZHUQUE_GATEWAY_URL / ZHUQUE_API_KEY。\n"
                "在腾讯云 EdgeOne 控制台创建 AI 网关后，把网关域名与 API Key 写入环境变量；\n"
                "拿不到就先用 --provider local。"
            )
        self.url = self.gateway + "/v1/providers/zhuque-text/classify"

    def score(self, text: str) -> Score:
        body = json.dumps({"text": text, "is_merge": True}, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            self.url,
            data=body,
            headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
            method="POST",
        )
        last_err: Exception | None = None
        for attempt in range(3):
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                    payload = json.loads(resp.read().decode("utf-8"))
                share = find_ai_share(payload)
                if share is None:
                    if self.dump:
                        print(json.dumps(payload, ensure_ascii=False, indent=2), file=sys.stderr)
                    raise ValueError("响应里找不到 AI 占比字段，用 --dump-response 看原始结构")
                score = int(round(max(0.0, min(100.0, share))))
                return Score(score, label_of(score), {"朱雀响应": payload})
            except (urllib.error.HTTPError, urllib.error.URLError, ValueError) as exc:
                last_err = exc
                time.sleep(self.sleep * (2 ** attempt))
        raise RuntimeError(f"朱雀检测失败：{last_err}")


# --------------------------------------------------------------------------
# 缓存
# --------------------------------------------------------------------------

class Cache:
    def __init__(self, path: Path | None):
        self.path = path
        self.data: dict[str, dict] = {}
        if path and path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                self.data[row["key"]] = row

    @staticmethod
    def key(provider: str, text: str) -> str:
        return hashlib.sha1(f"{provider}\x00{text}".encode("utf-8")).hexdigest()

    def get(self, provider: str, text: str) -> Score | None:
        row = self.data.get(self.key(provider, text))
        if not row:
            return None
        return Score(row["score"], row["label"], row.get("features", {}))

    def put(self, provider: str, text: str, score: Score) -> None:
        row = {"key": self.key(provider, text), "score": score.score,
               "label": score.label, "features": score.features}
        self.data[row["key"]] = row
        if self.path:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.path.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------
# 汇总与输出
# --------------------------------------------------------------------------

def weighted(rows: Iterable[dict]) -> float:
    total = sum(r["字数"] for r in rows)
    if not total:
        return 0.0
    return sum(r["评分"] * r["字数"] for r in rows) / total


def histogram(scores: Sequence[int]) -> str:
    buckets = [0] * 5
    for s in scores:
        buckets[min(4, s // 20)] += 1
    total = max(1, sum(buckets))
    rows = []
    for i, count in enumerate(buckets):
        lo = i * 20
        hi = 100 if i == 4 else i * 20 + 19
        bar = "█" * int(round(count * 40 / total))
        rows.append(f"| {lo:>3}–{hi:<3} | {count:>4} | {bar} |")
    return "\n".join(rows)


CJK_STRIP = re.compile(f"[{CJK}]")


def write_report(path: Path, rows: list[dict], provider: str) -> None:
    by_file: dict[str, list[dict]] = {}
    for row in rows:
        by_file.setdefault(row["文件"], []).append(row)

    lines = [
        "# AIGC 痕迹分段检测报告",
        "",
        f"- 生成时间：{time.strftime('%Y-%m-%d %H:%M:%S')}",
        f"- 检测器：`{provider}`",
        f"- 段落数：{len(rows)}；总字数：{sum(r['字数'] for r in rows)}",
        f"- 字符加权总分：**{weighted(rows):.1f} / 100**",
        "",
        "> 这不是「AI 生成比例」。检测器估的是文本的统计形态，不是作者身份；",
        "> 分值只用于排序，用来决定先复看哪几段。",
        "",
        "## 一、分章概览",
        "",
        "| 文件 | 段落数 | 字数 | 加权分 | 高（≥66） | 中（40–65） | 低（<40） |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    for name in sorted(by_file):
        group = by_file[name]
        high = sum(1 for r in group if r["评分"] >= 66)
        mid = sum(1 for r in group if 40 <= r["评分"] < 66)
        low = len(group) - high - mid
        lines.append(
            f"| {name} | {len(group)} | {sum(r['字数'] for r in group)} | "
            f"{weighted(group):.1f} | {high} | {mid} | {low} |"
        )

    lines += ["", "## 二、分值分布", "", "| 区间 | 段数 | 分布 |", "|---|---:|---|",
              histogram([r["评分"] for r in rows]), "", "## 三、优先复看的段落", ""]
    for row in sorted(rows, key=lambda r: -r["评分"])[:15]:
        excerpt = re.sub(r"\s+", " ", row["正文"])[:70]
        lines.append(f"{row['评分']:>3}  `{row['文件']}:{row['行号']}`  {excerpt}……")
        lines.append("")

    lines += [
        "## 四、怎么读这份报告",
        "",
        "1. 先看**高分段**有没有整段连续被标；零散的高分多半只是文风规整。",
        "2. 连接词密度高、句长过分均匀的段落，通常是该补具体内容的地方，不只是该改措辞。",
        "3. 公式与记号在切分时被剥掉，数学密集的段落因此偏短，低分不代表质量更高。",
        "4. 若出版方要的是「AI 使用说明」，按他们的模板写声明即可，不要提交本报告的百分比。",
        "",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def write_csv(path: Path, rows: list[dict], with_text: bool) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = ["编号", "文件", "行号", "字数", "汉字数", "评分", "标签", "特征"]
    if with_text:
        fields.append("正文")
    with path.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            item = dict(row)
            item["特征"] = json.dumps(row["特征"], ensure_ascii=False)
            writer.writerow(item)


# --------------------------------------------------------------------------
# 命令
# --------------------------------------------------------------------------

def collect_files(patterns: Sequence[str]) -> list[Path]:
    files: list[Path] = []
    for pattern in patterns:
        p = Path(pattern)
        if p.is_dir():
            files.extend(sorted(x for x in p.rglob("*")
                                if x.suffix.lower() in {".tex", ".md", ".txt"}))
        elif p.is_file():
            files.append(p)
        else:
            raise SystemExit(f"找不到：{pattern}")
    return files


def natural_key(path: Path) -> list:
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.name)]


def cmd_extract(args) -> int:
    files = sorted(collect_files(args.paths), key=natural_key)
    if getattr(args, "format", "csv") == "txt":
        out_dir = Path(args.out_dir) if args.out_dir else Path(__file__).resolve().parent / "输出" / "纯文本"
        txt_dir = out_dir / "txt"
        txt_dir.mkdir(parents=True, exist_ok=True)
        manifest = []
        for path in files:
            paras = [p.text for p in iter_paragraphs(path, 1, 100000, merge_short=False)]
            chunks, cur = [], []
            for t in paras:
                if cur and sum(len(x) + 2 for x in cur) + len(t) > args.chars_per_file:
                    chunks.append(cur); cur = []
                cur.append(t)
            if cur:
                chunks.append(cur)
            # 末尾残块并入前一块，避免出现不足 350 字的碎片（朱雀对短文本不出结果）
            min_block = getattr(args, "min_block", 350)
            if len(chunks) > 1 and sum(len(x) + 2 for x in chunks[-1]) < min_block:
                tail = chunks.pop()
                chunks[-1].extend(tail)
            for k, ch in enumerate(chunks, 1):
                body = "\n\n".join(ch)
                name = f"{path.stem}.txt" if len(chunks) == 1 else f"{path.stem}-{k:02d}.txt"
                (txt_dir / name).write_text(body + "\n", encoding="utf-8")
                manifest.append([path.stem, k, name, len(body),
                                 len(CJK_RE.findall(body)), len(ch),
                                 re.sub(r"\s+", " ", ch[0])[:40]])
        with (out_dir / "清单.csv").open("w", encoding="utf-8-sig", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["章节", "块号", "文件", "字符数", "汉字数", "段落数", "首段开头"])
            w.writerows(manifest)
        print(f"已导出 {len(manifest)} 块（{len(files)} 章）→ {txt_dir}")
        print(f"清单：{out_dir / '清单.csv'}")
        return 0
    out = Path(args.out) if args.out else Path(__file__).resolve().parent / "输出" / "段落.csv"
    rows = [asdict(para) for path in files
            for para in iter_paragraphs(path, args.min_chars, args.chunk)]
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8-sig", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["pid", "file", "line", "chars", "cjk", "text"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"已导出 {len(rows)} 段 → {out}")
    return 0


def build_provider(name: str, args):
    if name == "local":
        return "local", local_score
    if name == "zhuque":
        provider = ZhuqueProvider(dump=args.dump_response, sleep=args.sleep)
        return "zhuque", provider.score
    raise SystemExit(f"未知的检测器：{name}")


def cmd_scan(args) -> int:
    files = sorted(collect_files(args.paths), key=natural_key)
    out_dir = Path(args.out_dir) if args.out_dir else Path(__file__).resolve().parent / "输出"
    provider_name, scorer = build_provider(args.provider, args)
    cache = Cache(Path(args.cache) if args.cache else out_dir / "缓存.jsonl")

    rows: list[dict] = []
    for path in files:
        for para in iter_paragraphs(path, args.min_chars, args.chunk):
            cached = cache.get(provider_name, para.text)
            if cached is None:
                if args.sleep and provider_name != "local":
                    time.sleep(args.sleep)
                cached = scorer(para.text)
                cache.put(provider_name, para.text, cached)
            rows.append({
                "编号": para.pid, "文件": para.file, "行号": para.line,
                "字数": para.chars, "汉字数": para.cjk,
                "评分": cached.score, "标签": cached.label,
                "特征": cached.features, "正文": para.text,
            })
            if args.progress and len(rows) % 20 == 0:
                print(f"  已评 {len(rows)} 段……", file=sys.stderr)

    if not rows:
        print("没有可检测的段落。可调低 --min-chars，或检查输入文件是否为正文。", file=sys.stderr)
        return 1

    write_csv(out_dir / "段落评分.csv", rows, with_text=True)
    write_report(out_dir / "报告.md", rows, args.provider)
    print(f"已评 {len(rows)} 段，字符加权总分 {weighted(rows):.1f}")
    print(f"报告：{out_dir / '报告.md'}")
    print(f"明细：{out_dir / '段落评分.csv'}")
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="书稿段落切分与 AIGC 痕迹检测（用于排序与自查，不是 AI 生成比例）"
    )
    sub = parser.add_subparsers(dest="command")

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("paths", nargs="+", help=".tex / .md / .txt 文件或目录")
    common.add_argument("--min-chars", type=int, default=60,
                        help="段落最少汉字数（朱雀建议每段不少于 120，见 README）")
    common.add_argument("--chunk", type=int, default=1000, help="单段送检字数上限")

    p_extract = sub.add_parser("extract", parents=[common], help="只切分，导出段落 CSV 或纯文本")
    p_extract.add_argument("-o", "--out", help="输出 CSV 路径")
    p_extract.add_argument("--format", default="csv", choices=["csv", "txt"],
                           help="csv=段落清单；txt=按块导出纯文本，供粘贴到朱雀网页版")
    p_extract.add_argument("--out-dir", help="--format txt 时的输出目录")
    p_extract.add_argument("--min-block", type=int, default=350,
                           help="末尾残块小于此值时并入前一块（默认 350，朱雀的短文本下限）")
    p_extract.add_argument("--chars-per-file", type=int, default=3000,
                           help="--format txt 时每块字符数上限（朱雀网页版单次不宜过长）")
    p_extract.set_defaults(func=cmd_extract)

    p_scan = sub.add_parser("scan", parents=[common], help="切分 + 打分 + 生成报告")
    p_scan.add_argument("--provider", default="local", choices=["local", "zhuque"])
    p_scan.add_argument("--out-dir", help="输出目录（默认 输出/）")
    p_scan.add_argument("--cache", help="缓存文件路径")
    p_scan.add_argument("--sleep", type=float, default=1.5, help="远程调用间隔秒数")
    p_scan.add_argument("--dump-response", action="store_true", help="打印朱雀原始响应")
    p_scan.add_argument("--progress", action="store_true", help="打印进度")
    p_scan.set_defaults(func=cmd_scan)

    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        args = parser.parse_args(["scan", *(argv if argv is not None else sys.argv[1:])])
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
