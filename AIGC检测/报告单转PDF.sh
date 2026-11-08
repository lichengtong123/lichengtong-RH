#!/bin/bash
# 用本机 Chrome 把报告单 HTML 批量转成 PDF。
# 关键选项：--use-mock-keychain --password-store=basic
# 不加这两项时，Chrome 会弹出「找不到用于储存 Chrome 的钥匙串」系统对话框。
set -euo pipefail
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
DIR="${1:-$(cd "$(dirname "$0")" && pwd)/输出/C-报告单}"
OUT="$DIR/pdf"
mkdir -p "$OUT"
for f in "$DIR"/*.html; do
  n="$(basename "$f" .html)"
  "$CHROME" --headless=new --disable-gpu --disable-crash-reporter --disable-breakpad \
    --use-mock-keychain --password-store=basic \
    --user-data-dir="${TMPDIR:-/tmp}/aigc-chrome-profile" \
    --print-to-pdf="$OUT/$n.pdf" --no-pdf-header-footer "file://$f" >/dev/null 2>&1
done
echo "已生成 $(ls "$OUT"/*.pdf | wc -l) 份 PDF → $OUT"
