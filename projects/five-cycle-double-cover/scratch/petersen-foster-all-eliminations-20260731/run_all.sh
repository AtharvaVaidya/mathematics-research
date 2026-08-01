#!/bin/sh
set -eu

cd "$(dirname "$0")"
if ! python3 -c 'import sys; sys.exit(0 if __debug__ else 1)'; then
  echo "refusing to run with Python assertions disabled" >&2
  exit 1
fi
sha256sum -c SHA256SUMS
python3 checker.py \
  pf-root-transition-labels-0000-0667.json.gz \
  pf-root-transition-labels-0668-1334.json.gz \
  | tee reproduced-output.txt
diff -u expected-output.txt reproduced-output.txt
