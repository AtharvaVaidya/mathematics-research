#!/bin/sh
set -eu

cd "$(dirname "$0")"
CXX="${CXX:-c++}"
GENG="${GENG:-/opt/homebrew/bin/geng}"
"$CXX" -O3 -std=c++20 audit_order14.cpp -o /tmp/d5-typed-cap-orbit-external-order14
"$GENG" -Cq -d3 -D3 14 |
    /tmp/d5-typed-cap-orbit-external-order14 > reproduced-order14-output.txt
diff -u expected-order14-output.txt reproduced-order14-output.txt
