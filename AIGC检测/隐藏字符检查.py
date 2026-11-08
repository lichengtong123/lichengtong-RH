#!/usr/bin/env python3
"""隐藏字符检查：在文本文件中查找零宽字符、格式控制符、特殊空格和私用区字符。

这类不可见字符常被用作文本水印；正常书稿中不应出现。
用法：
    python3 隐藏字符检查.py                 # 默认检查 ../书稿 下全部 .tex
    python3 隐藏字符检查.py 文件或目录 ...   # 检查指定文件；目录则递归查其中的 .tex/.txt/.md
退出码：0 表示未发现，1 表示发现可疑字符。
"""
import sys, unicodedata
from pathlib import Path

# 不属于 Cf/Co/Cs 类别、但同样不可见或易被用作标记的空白字符
EXTRA = set('  ᠎       '
            '      ㅤ﻿ﾠ')

def suspicious(ch):
    # Cf 格式控制（零宽空格、零宽连接符、方向控制等），Co 私用区，Cs 代理项
    return unicodedata.category(ch) in ('Cf', 'Co', 'Cs') or ch in EXTRA

def collect(args):
    if not args:
        args = [str(Path(__file__).resolve().parent.parent / '书稿')]
    for a in args:
        p = Path(a)
        if p.is_dir():
            for ext in ('*.tex', '*.txt', '*.md'):
                yield from sorted(p.rglob(ext))
        elif p.is_file():
            yield p

def main():
    files = list(collect(sys.argv[1:]))
    found = 0
    for f in files:
        try:
            text = f.read_text(encoding='utf-8')
        except (UnicodeDecodeError, OSError) as e:
            print(f'跳过 {f}：{e}')
            continue
        for n, line in enumerate(text.splitlines(), 1):
            for col, ch in enumerate(line, 1):
                if suspicious(ch):
                    found += 1
                    name = unicodedata.name(ch, '未命名')
                    print(f'{f}:{n}:{col}  U+{ord(ch):04X}  {name}')
    print(f'共检查 {len(files)} 个文件，发现可疑字符 {found} 处。')
    return 1 if found else 0

if __name__ == '__main__':
    sys.exit(main())
