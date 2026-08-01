#!/bin/sh
set -eu

package_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
cd "$package_dir"

python3 build_formula.py
python3 prove_all.py --jobs 4

c++ -O3 -std=c++17 verify_graph_flow.cpp -o verify_graph_flow
./verify_graph_flow countermodel-order144.txt

python3 verify.py
python3 verify_fivecdc.py fivecdc.witness countermodel-order144.txt

planarg -u countermodel-order144.g6 /dev/null
shasum -a 256 -c SHA256SUMS
