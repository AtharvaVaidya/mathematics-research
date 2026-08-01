#!/bin/sh
set -eu

cd "$(dirname "$0")/../.."

shasum -a 256 -c scratch/d5-root-pair-census-20260731/SHA256SUMS
python3 -B scratch/d5-root-pair-census-20260731/check_compact_certificate.py \
  scratch/d5-root-pair-census-20260731/compact-witnesses-through24.json
python3 -B scratch/d5-root-pair-census-20260731/check_compact_certificate.py \
  scratch/d5-root-pair-census-20260731/compact-witnesses-order26.json.gz
python3 -B scratch/d5-root-pair-census-20260731/check_compact_certificate.py \
  scratch/d5-root-pair-census-20260731/compact-witnesses-order28.json.gz
python3 -B search/focused-theta-choice-through28-20260727/verify.py
