#!/bin/sh
set -eu

cd "$(dirname "$0")"
python3 checker.py | tee reproduced-output.txt
diff -u expected-output.txt reproduced-output.txt
sha256sum -c SHA256SUMS
