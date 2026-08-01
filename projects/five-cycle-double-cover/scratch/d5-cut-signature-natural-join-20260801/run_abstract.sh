#!/bin/sh
set -eu
cd "$(dirname "$0")"
python3 abstract_relations.py | tee reproduced-abstract-output.txt
cmp expected-abstract-output.txt reproduced-abstract-output.txt
shasum -a 256 -c SHA256SUMS
