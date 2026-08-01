#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 -B verify_minimal_profiles.py
python3 -B verify_minimal_profiles_independent.py
shasum -a 256 -c SHA256SUMS
