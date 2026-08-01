#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 independent_audit.py | tee independent-output.txt
shasum -a 256 -c SHA256SUMS
