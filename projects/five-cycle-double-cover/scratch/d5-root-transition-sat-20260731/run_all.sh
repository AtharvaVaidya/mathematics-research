#!/bin/sh
set -eu

HERE=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)

python3 "$HERE/search.py" --petersen --roots 0 5 \
  --include-labels --output "$HERE/petersen-root-regression.json"
python3 "$HERE/search.py" --petersen --all-eliminations \
  --output "$HERE/petersen-eliminations.json"
cd "$HERE"
shasum -a 256 -c SHA256SUMS
echo "d5-root-transition-sat: PASS"
