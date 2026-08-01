#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 verify.py | tee reproduced-output.txt
cmp expected-output.txt reproduced-output.txt
shasum -a 256 -c SHA256SUMS
