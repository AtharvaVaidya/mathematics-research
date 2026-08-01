#!/bin/sh
set -eu
cd "$(dirname "$0")"
out="$(mktemp)"
trap 'rm -f "$out"' EXIT HUP INT TERM
python3 check_local_lemmas.py > "$out"
python3 check_pf_fixed_flow_counterexample.py >> "$out"
cmp expected-output.txt "$out"
shasum -a 256 -c SHA256SUMS
echo "LOCAL_LEMMAS PASS"
