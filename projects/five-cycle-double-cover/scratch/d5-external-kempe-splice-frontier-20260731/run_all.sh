#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 checker.py | tee reproduced-output.txt
diff -u expected-output.txt reproduced-output.txt
shasum -a 256 -c SHA256SUMS
