# Reproducibility

Run these commands from the repository/workspace root, one directory above
this preprint.

## Human-theorem and finite no-go checkers

```sh
python3 scratch/verify_jaeger_support5_component_criterion.py
python3 scratch/verify_jaeger_k_forest_petersen.py
python3 scratch/check_jaeger_fixed_third_tree_parity_no_go.py
python3 scratch/check_jaeger_perfect_forests_first_no_go.py
python3 scratch/verify_jaeger_star_parity_descent_countermodel.py
python3 scratch/verify_jaeger_kernel_closure_typea_countermodel.py
```

## Symmetric Fano-minimum descent through order 14

```sh
python3 scratch/verify_jaeger_fano_min_descent_frontier.py
python3 scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py
```

This independently regenerates the canonical graph streams,
3-edge-connectivity filters, vertex automorphism orbits, census ordering,
totals, and SHA-256. It does not duplicate the C++ enumeration of all
529,150,122 states. To recompute the whole-state census, use the runner
command printed in Section 8 of the paper. The second command independently
replays one explicit state and all 147 incident exchanges in the targeted
order-16 fibre; the full 953,856-state enumeration remains in the C++ trust
boundary.

## Kernel-closure frontier

```sh
python3 scratch/verify_jaeger_kernel_closure_frontier.py
python3 scratch/verify_jaeger_star_kernel_closure_countermodel_16v.py
python3 scratch/verify_jaeger_star_kernel_closure_triangle_expansion.py
clang++ -O3 -std=c++20 \
  scratch/count_jaeger_star_kernel_closure_countermodel_16v.cpp \
  -o /tmp/count_star_kernel_closure_16v
/tmp/count_star_kernel_closure_16v
shasum -a 256 \
  output/jaeger-kernel-closure-frontier/stars-order16.jsonl
```

The first command replays all 12,695 retained positive type-A/B witnesses
through order 10. The preceding
`verify_jaeger_kernel_closure_typea_countermodel.py` command independently
enumerates all 355,392 ordered packings in each of the two 12-vertex
negative fibres. The second command checks the 16-vertex star graph and
root, both LRAT-checker results, and an independent exact-parity/five-point
witness in the same fibre. The third command checks the explicit six-lift
obstruction and Petersen triple-expansion description supporting the human
triangle-contraction theorem. The final command independently enumerates
all 5,723,136 ordered star packings without a SAT solver. The expected
order-16 full-stream SHA-256 is
`889d0e5857b62e082f3fcad0a929e7c0d92032a8e675f4d2ff9f40272ea43d46`;
that stream remains a producer result rather than an independently repeated
full census.

## Complete fixed-fibre census through order 14

```sh
python3 scratch/verify_jaeger_five_point_frontier.py
python3 scratch/verify_jaeger_six_point_frontier.py
```

These structural verifiers check the frozen reports and producer hashes. To
recompute the positive SAT decisions, run the producer command printed in
the paper; witness models are checked semantically inside the producer but
are not all retained.

## Certified 34-vertex thinning countermodel

```sh
python3 scratch/verify_jaeger_star_thinning_countermodel_34v.py
python3 scratch/verify_jaeger_34v_star_good_witness.py
```

The first command checks graph premises, CNF semantics, and acceptance of the
LRAT by both `lrat-check` and the verified CakeML `cake_lpr` binary. The
second independently checks the positive five-point witness in the same
fibre.

## Order-44 literal witnesses

```sh
python3 scratch/verify_jaeger_coordinate_five_order44.py \
  --input search/known_snarks/source/snarks_44.04.oddness4.cyc4.g6 \
  --witnesses output/jaeger-coordinate-five-order44/witnesses.jsonl
```

Expected status: `PASS`, with 31 graphs and 1,364 vertex-star witnesses.

## Build

```sh
cd preprint-jaeger-fivecdc-frontier
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

The fixed epoch reproduces the committed PDF byte for byte; without it,
`xdvipdfmx` records the current creation time even when the rendered pages
are identical.
