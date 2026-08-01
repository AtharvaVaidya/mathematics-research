#!/bin/sh
set -eu
here=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
python3 "$here/verify.py" | tee "$here/reproduced-output.txt"
python3 "$here/check_cages.py" | tee -a "$here/reproduced-output.txt"
python3 "$here/check_sat_smoke.py" | tee -a "$here/reproduced-output.txt"
diff -u "$here/expected-output.txt" "$here/reproduced-output.txt"
