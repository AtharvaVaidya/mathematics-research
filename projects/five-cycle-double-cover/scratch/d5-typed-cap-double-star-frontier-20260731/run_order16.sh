#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CXX=${CXX:-clang++}
GENG=${GENG:-/opt/homebrew/bin/geng}
BIN=$(mktemp -t d5-typed-cap-order16.XXXXXX)
OUT=$(mktemp -t d5-typed-cap-order16-output.XXXXXX)
trap 'rm -f "$BIN" "$OUT"' EXIT HUP INT TERM

"$CXX" -std=c++20 -O3 -DNDEBUG \
  "$HERE/audit_d5_typed_cap_ports.cpp" -o "$BIN"
"$GENG" -Cq -d3 -D3 16 2>/dev/null \
  | "$BIN" 2>/dev/null > "$OUT"
cmp "$HERE/expected-order16-output.txt" "$OUT"
cat "$OUT"
echo "ORDER16_CPP_FRONTIER PASS"
