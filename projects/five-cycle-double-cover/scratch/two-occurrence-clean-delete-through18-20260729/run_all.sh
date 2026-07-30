#!/bin/sh
set -eu

here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$here"
primary_bin=$(mktemp "${TMPDIR:-/tmp}/fivecdc-support18-primary.XXXXXX")
audit_bin=$(mktemp "${TMPDIR:-/tmp}/fivecdc-support18-audit.XXXXXX")
trap 'rm -f "$primary_bin" "$audit_bin"' EXIT HUP INT TERM

python3 enumerate_profiles.py
c++ -std=c++17 -O3 verify_support18.cpp -o "$primary_bin"
"$primary_bin"
c++ -std=c++17 -O3 independent_literal_audit.cpp -o "$audit_bin"
"$audit_bin"
shasum -a 256 -c SHA256SUMS
