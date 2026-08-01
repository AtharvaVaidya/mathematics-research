#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 verify.py | tee verification-output.txt
python3 independent_check.py | tee independent-output.txt
shasum -a 256 -c SHA256SUMS
