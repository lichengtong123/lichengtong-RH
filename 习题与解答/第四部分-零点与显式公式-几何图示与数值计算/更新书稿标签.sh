#!/bin/sh
# 用法：sh 更新书稿标签.sh /path/to/main-B.aux
# 从书稿编译生成的 main-B.aux 中提取 \newlabel 行，写入本目录的 书稿标签.aux。
# 书稿改版并重新编译后执行一次，再编译习题，题中引用的书内编号即随之更新。
[ -f "$1" ] || { echo "请给出书稿的 main-B.aux 路径"; exit 1; }
grep '^\\newlabel' "$1" > "$(dirname "$0")/书稿标签.aux"
echo "已更新 书稿标签.aux（$(wc -l < "$(dirname "$0")/书稿标签.aux") 个标签）"
