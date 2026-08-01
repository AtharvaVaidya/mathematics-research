#!/bin/sh
set -eu

root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
solver=${CADICAL:-cadical}
work=$(mktemp -d "${TMPDIR:-/tmp}/four-charge-kernel.XXXXXX")
trap 'rm -rf -- "$work"' EXIT HUP INT TERM

{
  python3 "$root/exact_abstract_sat.py" \
    --solver "$solver" --work "$work/sat"
  python3 "$root/independent_boundary_verify.py"
  python3 "$root/realization_verify.py"
} > "$work/verification-output.txt"

cmp "$work/verification-output.txt" "$root/verification-output.txt"
(
  cd "$root"
  shasum -a 256 -c SHA256SUMS
)

echo "PASS: four-charge counterexample, descent, and minimum-clean realization"
