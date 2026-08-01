#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CXX=${CXX:-clang++}
GENG=${GENG:-/opt/homebrew/bin/geng}
BIN=$(mktemp -t d5-simultaneous.XXXXXX)
CPP_OUT=$(mktemp -t d5-simultaneous-cpp.XXXXXX)
PY_OUT=$(mktemp -t d5-simultaneous-python.XXXXXX)
trap 'rm -f "$BIN" "$CPP_OUT" "$PY_OUT"' EXIT

"$CXX" -std=c++20 -O3 -DNDEBUG -Wno-return-type \
  "$HERE/check_simultaneous.cpp" -o "$BIN"

for n in 4 6 8 10 12 14; do
  echo "ORDER=$n" >> "$CPP_OUT"
  "$GENG" -Cq -d3 -D3 "$n" 2>/dev/null | "$BIN" >> "$CPP_OUT"
done
cmp "$HERE/expected-cpp-output.txt" "$CPP_OUT"

GENG="$GENG" python3 "$HERE/check_simultaneous.py" > "$PY_OUT"
cmp "$HERE/expected-python-output.txt" "$PY_OUT"

(
  cd "$HERE"
  shasum -a 256 -c SHA256SUMS
)
echo "SIMULTANEOUS_EXTERNAL_FRONTIER PASS"
