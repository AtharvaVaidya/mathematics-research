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
python3 scratch/verify_jaeger_reciprocal_exchange_defect_formula.py
python3 scratch/verify_jaeger_fano_min_immediate_descent_countermodel.py
python3 scratch/verify_jaeger_sorted_profile_local_no_go_order36.py
python3 scratch/verify_jaeger_plateau_escape_radius4_order40.py
python3 scratch/verify_jaeger_plateau_profile_laplacian_no_go.py
python3 scratch/verify_jaeger_kernel_closure_typea_countermodel.py
python3 scratch/verify_jaeger_star_exact_parity_triangle_lift.py
python3 scratch/verify_jaeger_star_square_any_coordinate_lift_countermodel.py
python3 scratch/verify_jaeger_star_square_order6_controls.py
python3 scratch/verify_jaeger_star_square_existential_order8.py
python3 scratch/verify_jaeger_square_fixed_label_selection_cut_no_go.py
python3 scratch/search_jaeger_star_square_existential_census.py --order 10
python3 scratch/search_jaeger_star_square_existential_census.py --order 12
clang++ -O3 -std=c++20 \
  scratch/search_jaeger_star_square_existential_order14.cpp \
  -o /tmp/search_square_order14
geng -cq -d3 -D3 14 |
  /tmp/search_square_order14 |
  gzip -9 >/tmp/square-order14-witnesses.tsv.gz
python3 scratch/verify_jaeger_star_square_existential_order14.py \
  /tmp/square-order14-witnesses.tsv.gz
```

The exact-triangle command checks the separate two-way theorem for the surviving
exact target: 60 admissible local traces, seven symmetry orbits, and no
trace without a parity-preserving legal triangle lift. The expected SHA-256
values are `96259e65072b5a8c03f572e028a650f6e075f787c66e7e59917630c2b22c1008`
for the human note and
`e3026b8acdf95555fad33a5a2871174b497a154151f5e0f4fde642d31053bbe7`
for the checker.

The final five square commands freeze the exact square-local quantifier
boundary.
The first checks the order-eight fixed-state countermodel: 6,561 gadget
words, 72 legal lifts, and no lift good in any coordinate, followed by an
alternate-state positive control. The second proves that no such fixed-state
failure occurs on either simple 3-edge-connected cubic graph of order six.
The third checks the weaker whole-fibre existential statement on all four
simple 3-edge-connected cubic graphs of order eight, all roots, and all
eligible smoothing pairs: 672 instances and zero failures. Expected
SHA-256 values are
`ea24f997aaae027a25802a9ed291411199789077011c14a605c0956e615fb529`
for the human note,
`a26ba8296cdab88685089d43d7be8002d209d90d3d662ef45b86f89aabc053eb`
for the countermodel checker,
`0f7d64413105ed6c69bd171734297fdf7e45b81af31bd812665efd92111dd73e`
for the order-six controls, and
`f9366e50d6e7b0e53b87114f6daf7ee1ca640ac224f1f8d1363190e87fd7124b`
for the order-eight census. The final two commands extend the whole-fibre
frontier to every simple 3-edge-connected cubic graph of orders 10 and 12:
6,300 and 53,352 labelled root/edge-pair instances, respectively, with zero
failures. The human note also proves the fixed-cover extension criterion
\(P=Q\) or \(P\cap Q=\varnothing\). Expected SHA-256 values are
`0fed1da84326097378145396bf2608aac44ad2c2e6a36c9ad464d215fc019015`
for the note and
`bf3ce5e8c82bce4d84a14c80b538cb5337fd4a4a56016d0043eb70a4d82dbcd8`
for the combined order-10/order-12 checker. The final compile/generate/check
sequence produces and independently replays one explicit witness for each
of the 572,880 labelled order-14 instances. It must report 341 retained
graphs, 4,774 roots, 24,268 distinct certified downstairs states, and corpus
SHA-256
`26dfe990a6655170f5fdcb6faf1424db279b57e8d094269417b7330fb5affd41`.
Expected program SHA-256 values are
`f457fbf60bf5f2b94828bcf6295e0bf289b70205c55b70ab81d35de2fbc9697e`
for the C++ search and
`81545f6d0fc1331783a3d7e1d9f267961172a3398a05c635096c093d6638a791`
for the independent checker.

The triangular-prism command independently enumerates all 540 indexed
five-cover pair labellings and verifies that the two selected matching edges
always meet in exactly one coordinate. It also reconstructs the displayed
profile-\((2,0,2)\) star state and its profile-\((2,0,2)\) square-local
lift. The human proof is the three-edge-cut parity identity. Expected
note/checker SHA-256 values are
`c7fe3f077c695582b4288dcca6cbed726ed885d1976bf3225bfa2f39913c60d5` /
`fba5be96ab40091e19f9e40a38b1eb5342ada638ef234944562ea304ccad3398`.

The sorted-profile command reconstructs the literal 36-vertex state,
checks all 867 exchange candidates and the exact \(0/13/50\)
lower/equal/higher split among 63 legal neighbours, then replays a
two-exchange same-\(d_{\min}\) escape. Expected SHA-256 values are
`5d1737becf817615190a875808c5dff12d8cb14c7b8736d3f6967f49c4fb745e`
for the note and
`9b595f2a83371f08792e967d12d49b9050e6ca5766330bb87a7b0be6d4f48178`
for the independent checker.

The radius-four command reconstructs the literal simple 3-edge-connected
cubic order-40 state and its complete level-two ball through radius three.
It must report layer sizes \(1,13,108,836\), 1,037,514 candidate exchanges,
67,392 legal oriented arcs, no descending boundary before layer three, and
32 descending arcs from layer three. It independently replays a shortest
four-exchange escape. Expected SHA-256 values are
`c751e430c4d381a3238f9257c810e58a2ab00ce0d3bab666a04ea08b5256b6fe`
for the note and
`db9382bd873ee741658e5178b671c223103140d9952be568512a96d3e61fa4dc`
for the checker. The hashes of the canonical radius-three ball and all
scored legal arcs are
`51aa4f3ff1efa9bebcffe0f2869919c7bd25d60c2047f8b5383b8be90d435c58`
and
`d2ad5a4bb090e43efffba60e51dec5c66037cf10465b7c43f86a2c5b3407c4ce`.

The profile-Laplacian command checks two adjacent states with the identical
ordered profile \((8,2,8,8,6,10,10)\). It exhausts their 65- and 63-neighbour
exchange neighbourhoods and must report total-defect Laplacians \(10\) and
\(-14\). Expected note/checker SHA-256 values are
`8f804b9fd2e6f094be3165729d0c6845c81aa04094a4c994e207e8cc6bc6037b` /
`24b59ad26f9f35d0589854111db5ced3923f659961199245bdefbb15ee8c9624`.

## Symmetric Fano-minimum descent through order 14

```sh
python3 scratch/verify_jaeger_fano_min_descent_frontier.py
python3 scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py
python3 scratch/verify_jaeger_triangle_expansion_descent_structure.py
python3 scratch/verify_jaeger_triangle_expanded_fixedtrap_descent.py
```

This independently regenerates the canonical graph streams,
3-edge-connectivity filters, vertex automorphism orbits, census ordering,
totals, and SHA-256. It does not duplicate the C++ enumeration of all
529,150,122 states. To recompute the whole-state census, use the runner
command printed in Section 8 of the paper. The second command independently
replays one explicit state and all 147 incident exchanges in the targeted
order-16 fibre; the full 953,856-state enumeration remains in the C++ trust
boundary. The third command checks the exact six-lift score table. The
fourth independently regenerates and audits the thirteen triangle-expanded
inputs and their 17,297,280-state producer census; it does not duplicate
the C++ whole-state enumeration.

## Simultaneous triangle-product controls

```sh
python3 -m py_compile scratch/search_jaeger_lifted_immediate_traps.py
python3 scratch/search_jaeger_lifted_immediate_traps.py \
  --triangles 2 \
  --graph6 'Ot?GO?@?_G?T@IOSAIBO?' \
  --root 0 --spokes 2,1,0 \
  --omitted 1720610,271049,105492
```

Expected final JSON: 3,780 tested lifts, zero lower neighbour at the
minimizing lift, and minimum equal-neighbour count seven. The Cartesian
product theorem is proved separately in
`scratch/jaeger-simultaneous-triangle-lift-plateau-search.md`; the program
checks only finite controls. Expected SHA-256 values are
`acb8b66d72c350b6f768b791ed9b3167d4282acf2a587d4fcfd52ac062e8b6b7`
for the note and
`94cd82b1dbf84ffd46a6622fff8741fc1bb4187e616e16aee54b5dc5e7717303`
for the Python search.

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
