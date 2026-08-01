#!/bin/sh
set -eu

python3 -B verify.py | diff -u certificate.json -
echo "primary certificate: PASS"

python3 -B independent_check.py | diff -u independent-output.json -
echo "independent certificate: PASS"

shasum -a 256 -c SHA256SUMS
echo "hash ledger: PASS"

echo "ALL CHECKS PASSED"
