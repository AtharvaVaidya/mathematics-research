#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
root=$(CDPATH= cd -- "$here/../../.." && pwd)
geng=${GENG:-/opt/homebrew/bin/geng}
binary=${TMPDIR:-/tmp}/audit_d5_complement_escape

clang++ -std=c++17 -O3 -DNDEBUG "$here/audit_complement_escape.cpp" -o "$binary"

"$geng" -Cq -d3 -D3 12 2>/dev/null |
  "$binary" --expect-failures 0 2>/dev/null
"$geng" -Cq -d3 -D3 14 2>/dev/null |
  "$binary" --expect-failures 12 2>/dev/null

python3 "$here/audit_full_cycle_space.py"
python3 "$here/check_literal_delimiter.py"

printf '%s\n' PASS
