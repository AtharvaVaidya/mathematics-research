#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CXX=${CXX:-clang++}
GENG=${GENG:-/opt/homebrew/bin/geng}
BIN=$(mktemp -t d5-typed-cap.XXXXXX)
OUT=$(mktemp -t d5-typed-cap-output.XXXXXX)
trap 'rm -f "$BIN" "$OUT"' EXIT

"$CXX" -std=c++20 -O3 -DNDEBUG "$HERE/audit_d5_typed_cap_ports.cpp" -o "$BIN"

for n in 4 6 8 10 12 14; do
  echo "ORDER=$n" >> "$OUT"
  "$GENG" -Cq -d3 -D3 "$n" 2>/dev/null | "$BIN" 2>/dev/null >> "$OUT"
done

cmp "$HERE/expected-output.txt" "$OUT"
python3 "$HERE/verify_small_and_algebra.py"
(
  cd "$HERE"
  shasum -a 256 -c SHA256SUMS
)
echo "FULL_CPP_FRONTIER PASS"
