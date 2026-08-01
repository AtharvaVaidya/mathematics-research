#!/bin/sh
set -eu

cd "$(dirname "$0")"

python3 -B verify_certificate.py | diff -u certificate-output.txt -
python3 -B search_petersen.py | diff -u petersen-output.txt -
python3 -B verify_small_order_census.py | diff -u small-order-census-output.txt -

shasum -a 256 -c SHA256SUMS
shasum -a 256 -c SOURCE-SHA256SUMS

echo "ALL NON-TAIT BLOCKER AUDITS PASSED"
