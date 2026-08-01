#!/bin/sh
set -eu
python3 -B verify_refined_formula.py | diff -u formula-output.txt -
python3 -B analyze_order80_control.py | diff -u order80-output.txt -
shasum -a 256 -c SHA256SUMS
shasum -a 256 -c SOURCE-SHA256SUMS
