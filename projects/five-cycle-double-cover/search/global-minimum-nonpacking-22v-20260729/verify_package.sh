#!/bin/sh
set -eu
cd "$(dirname "$0")"
tmp_result="$(mktemp)"
trap 'rm -f "$tmp_result"' EXIT HUP INT TERM
PYTHONDONTWRITEBYTECODE=1 python3 verify.py >"$tmp_result"
cmp expected-report.json "$tmp_result"
shasum -a 256 -c SHA256SUMS
echo "PASS"
