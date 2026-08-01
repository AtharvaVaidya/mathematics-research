#!/bin/sh
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ACTUAL_OUTPUT=$(mktemp "${TMPDIR:-/tmp}/d5-translation-no-go.XXXXXX")
trap 'rm -f "$ACTUAL_OUTPUT"' EXIT HUP INT TERM

cd "$SCRIPT_DIR"
python3 verify_translation_no_go.py > "$ACTUAL_OUTPUT"
diff -u expected-output.txt "$ACTUAL_OUTPUT"
cat "$ACTUAL_OUTPUT"
shasum -a 256 -c SHA256SUMS
echo "PACKAGE PASS"
