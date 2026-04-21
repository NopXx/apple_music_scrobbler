#!/bin/bash
# แปลง PNG ใหญ่ตัวเดียว → icon.icns
# Usage:  ./make_icns.sh path/to/icon.png
set -e

SRC="${1:-icon.png}"
OUT="${2:-icon.icns}"

if [ ! -f "$SRC" ]; then
  echo "✗ ไม่พบไฟล์: $SRC"
  echo "Usage: $0 <source.png> [output.icns]"
  exit 1
fi

TMP="$(mktemp -d)/icon.iconset"
mkdir -p "$TMP"

echo "→ สร้าง iconset จาก $SRC"
sips -z 16 16     "$SRC" --out "$TMP/icon_16x16.png"       > /dev/null
sips -z 32 32     "$SRC" --out "$TMP/icon_16x16@2x.png"    > /dev/null
sips -z 32 32     "$SRC" --out "$TMP/icon_32x32.png"       > /dev/null
sips -z 64 64     "$SRC" --out "$TMP/icon_32x32@2x.png"    > /dev/null
sips -z 128 128   "$SRC" --out "$TMP/icon_128x128.png"     > /dev/null
sips -z 256 256   "$SRC" --out "$TMP/icon_128x128@2x.png"  > /dev/null
sips -z 256 256   "$SRC" --out "$TMP/icon_256x256.png"     > /dev/null
sips -z 512 512   "$SRC" --out "$TMP/icon_256x256@2x.png"  > /dev/null
sips -z 512 512   "$SRC" --out "$TMP/icon_512x512.png"     > /dev/null
sips -z 1024 1024 "$SRC" --out "$TMP/icon_512x512@2x.png"  > /dev/null

echo "→ compile เป็น .icns"
iconutil -c icns "$TMP" -o "$OUT"

echo "✓ เสร็จ → $OUT"
