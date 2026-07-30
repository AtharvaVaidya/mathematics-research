#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$here"

primary_bin=$(mktemp "${TMPDIR:-/tmp}/fivecdc-unrestricted16.XXXXXX")
primary_out=$(mktemp "${TMPDIR:-/tmp}/fivecdc-unrestricted16-out.XXXXXX")
partition_out=$(mktemp "${TMPDIR:-/tmp}/fivecdc-unrestricted16-part.XXXXXX")
audit_out=$(mktemp "${TMPDIR:-/tmp}/fivecdc-unrestricted16-audit.XXXXXX")
trap 'rm -f "$primary_bin" "$primary_out" "$partition_out" "$audit_out"' \
  EXIT HUP INT TERM

c++ -std=c++17 -O3 classify_fixed_word.cpp -o "$primary_bin"
"$primary_bin" > "$primary_out"
diff -u census-output.txt "$primary_out"

python3 verify_partition_count.py > "$partition_out"
diff -u partition-count-output.txt "$partition_out"

python3 verify_residuals.py > "$audit_out"
diff -u independent-output.txt "$audit_out"

shasum -a 256 -c SHA256SUMS
printf '%s\n' "PASS complete replay"
