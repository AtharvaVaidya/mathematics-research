#!/bin/sh
set -eu

for cache_path in \
  tmp/case_c_n3_generic_charts_Q.pkl \
  tmp/case_c_n3_special_charts_Q.pkl \
  tmp/case_c_n3_special_recurrence_Q.pkl
do
  if [ -e "$cache_path" ]; then
    echo "ERROR: publication replay requires absent cache: $cache_path" >&2
    exit 1
  fi
done

echo "== environment =="
.venv/bin/python --version
.venv/bin/python -c \
  'import sys; sys.flags.optimize == 0 or sys.exit("ERROR: Python assertions are disabled"); print("Python optimize", sys.flags.optimize)'
.venv/bin/python -c 'import sympy; print("SymPy", sympy.__version__)'
Singular --version
degree125_singular_prefix=$(
  dirname "$(dirname "$(command -v Singular)")"
)
degree125_modstd_path=$(
  find -L "$degree125_singular_prefix/share" \
    -path '*/singular/LIB/modstd.lib' -print -quit
)
if [ -z "$degree125_modstd_path" ]; then
  echo "ERROR: could not locate modstd.lib below $degree125_singular_prefix/share" >&2
  exit 1
fi
echo "modstd.lib: $degree125_modstd_path"
sed -n '2p' "$degree125_modstd_path"

echo "== full case-c interface, global special fiber, and exact-Q charts =="
.venv/bin/python route_bd_ab_hurwitz_count.py
.venv/bin/python \
  current_context/verify_case_c_full_certificate_bridge.py \
  --run-special-fiber \
  --run-special-q

echo "== modular square branch =="
.venv/bin/python route_bd_case_c_n3_hurwitz_bridge.py

echo "== complete modular generic charts =="
.venv/bin/python route_bd_case_c_n3_generic_charts.py

echo "== all-scale a/b obstruction =="
.venv/bin/python route_bd_universal_radial_kernel_theorem.py
.venv/bin/python route_bd_allscale_marked_cusp_obstruction.py
.venv/bin/python current_context/verify_gghv_allscale_scope.py

echo "RESULT: CLEAN-ROOM DEGREE-125 REPLAY PASSED"
