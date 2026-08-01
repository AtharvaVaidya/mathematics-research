#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 search_through10.py | tee reproduced-census-output.txt
cmp expected-census-output.txt reproduced-census-output.txt
shasum -a 256 -c SHA256SUMS
