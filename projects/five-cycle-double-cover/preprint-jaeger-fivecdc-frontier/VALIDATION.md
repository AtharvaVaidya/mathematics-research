# Validation record

Date: 2026-07-28

Resolution status: FiveCDC remains unresolved.

The manuscript compiled successfully with
`SOURCE_DATE_EPOCH=1785271878 tectonic main.tex`, reproducing the committed
PDF byte for byte. `pdfinfo` reported 34 US-letter pages, no encryption, no
forms, and no JavaScript.
All pages were rendered with Poppler at 120 dpi and visually inspected.
There were no clipped lines, overflowing tables, broken glyphs, or unreadable
hashes.

The following cited checkers all exited zero in the final validation pass:

- `verify_jaeger_support5_component_criterion.py`: PASS on 30,744 literal
  small flows, with 0 direct-CSP/criterion mismatches.
- `verify_jaeger_k_forest_petersen.py`: PASS on 4,416 ordered packings at
  each Petersen star.
- `check_jaeger_fixed_third_tree_parity_no_go.py`: PASS; 16 fixed-base
  extensions, 0 parity-good.
- `check_jaeger_perfect_forests_first_no_go.py`: PASS; contracted rank sum
  9 is smaller than the 10 required residual copies.
- `verify_jaeger_star_parity_descent_countermodel.py`: PASS; all 108
  fixed-coordinate exchange candidates checked, with 18 legal neighbours
  and the symmetric rescue profile independently reconstructed.
- `verify_jaeger_fano_min_descent_frontier.py`: PASS; canonical coverage of
  419 graphs, 3,567 root orbits, and 529,150,122 producer-enumerated states,
  with zero trapped positive-level components.
- `verify_jaeger_fano_min_descent_order16_closure_no_go.py`: PASS; one
  explicit all-seven-defect-four state and all 147 incident exchanges in
  the targeted order-16 fibre replayed independently.
- `verify_jaeger_reciprocal_exchange_defect_formula.py`: PASS; the
  odd-kernel, bilinear-intersection, quotient-boundary, and Hamming update
  formulas agree on all legal exchanges at the frozen 14- and 16-vertex
  states.
- `verify_jaeger_fano_min_immediate_descent_countermodel.py`: PASS; both
  147-swap neighbourhoods are exhausted. The first has no immediate
  descent; the second has 23 score-two neighbours, zero kernel-inert
  neighbours, and an independently reconstructed active-neutral
  two-step escape.
- `verify_jaeger_sorted_profile_local_no_go_order36.py`: PASS; the literal
  simple 3-edge-connected cubic order-36 state has 867 reciprocal
  candidates and 63 legal neighbours, split exactly as 0 lower, 13 equal,
  and 50 higher for the sorted seven-defect profile. A same-\(d_{\min}\)
  escape to defect zero is independently replayed in two exchanges after
  57 breadth-first states; note/checker SHA-256
  `5d1737becf817615190a875808c5dff12d8cb14c7b8736d3f6967f49c4fb745e` /
  `9b595f2a83371f08792e967d12d49b9050e6ca5766330bb87a7b0be6d4f48178`.
- `verify_jaeger_plateau_escape_radius4_order40.py`: PASS; the literal
  simple 3-edge-connected cubic order-40 state has a complete radius-three
  level-two ball of 958 states in layers \(1,13,108,836\). The checker
  reconstructs 1,037,514 candidate exchanges and 67,392 legal oriented arcs,
  finds no descending boundary before layer three and exactly 32 descending
  arcs from that layer, and replays a shortest four-exchange escape. Thus
  only the radius-three strengthening is refuted; note/checker SHA-256
  `c751e430c4d381a3238f9257c810e58a2ab00ce0d3bab666a04ea08b5256b6fe` /
  `db9382bd873ee741658e5178b671c223103140d9952be568512a96d3e61fa4dc`.
- `verify_jaeger_plateau_profile_laplacian_no_go.py`: PASS; two adjacent
  states with identical ordered profile \((8,2,8,8,6,10,10)\) have legal
  degrees 65 and 63 and total-defect Laplacians \(10\) and \(-14\).
  This refutes profile-only averaging and universal sub/superharmonicity of
  total defect, not the full plateau theorem; note/checker SHA-256
  `8f804b9fd2e6f094be3165729d0c6845c81aa04094a4c994e207e8cc6bc6037b` /
  `24b59ad26f9f35d0589854111db5ced3923f659961199245bdefbb15ee8c9624`.
- `verify_jaeger_triangle_expansion_descent_structure.py`: PASS; the six
  lifted profiles and their common contraction are reconstructed.
- `verify_jaeger_triangle_expanded_fixedtrap_descent.py`: PASS; all thirteen
  inputs, graph premises, census rows, hashes, and the 17,297,280-state
  aggregate are independently audited.
- `search_jaeger_lifted_immediate_traps.py`: PASS on the frozen second
  order-16 state with two simultaneous triangle expansions; all 3,780
  lifts were checked and the minimum equal-neighbour count among states
  with no lower neighbour was seven. This is a finite control for the
  separately proved Cartesian-product theorem, not a universal descent
  check; note/search SHA-256
  `acb8b66d72c350b6f768b791ed9b3167d4282acf2a587d4fcfd52ac062e8b6b7` /
  `94cd82b1dbf84ffd46a6622fff8741fc1bb4187e616e16aee54b5dc5e7717303`.
- `verify_jaeger_kernel_closure_typea_countermodel.py`: PASS; 355,392
  ordered packings in each 12-vertex fibre, zero closure-good and 7,704
  exact-parity-good.
- `verify_jaeger_kernel_closure_frontier.py`: PASS; all 12,695 retained
  positive type-A/B witnesses through order 10 replayed.
- `stars-order16.jsonl`: SHA-256
  `889d0e5857b62e082f3fcad0a929e7c0d92032a8e675f4d2ff9f40272ea43d46`;
  the producer stream records 4,060 graphs, 64,960 roots, 45,248 feasible
  fibres, and one closure failure.
- `verify_jaeger_star_kernel_closure_countermodel_16v.py`: PASS; the
  16-vertex graph/root premises, CNF and LRAT hashes, both LRAT checkers,
  and an independent five-point witness all verified.
- `count_jaeger_star_kernel_closure_countermodel_16v.cpp`: PASS; 16,200
  cographic bases, 158,976 unordered base partitions, 5,723,136 ordered
  star packings, zero closure-good and 40,464 exact-parity-good.
- `verify_jaeger_star_kernel_closure_triangle_expansion.py`: PASS; the
  14-vertex closure-good quotient, all six closure-bad lifts, and the
  Petersen distance-two-cycle description were reconstructed.
- `verify_jaeger_star_exact_parity_triangle_lift.py`: PASS; all 60
  admissible exact-parity traces reduce to seven symmetry orbits and every
  trace has a parity-preserving legal lift (good-lift histogram
  1:18, 2:12, 3:6, 4:24); note/checker SHA-256
  `96259e65072b5a8c03f572e028a650f6e075f787c66e7e59917630c2b22c1008` /
  `e3026b8acdf95555fad33a5a2871174b497a154151f5e0f4fde642d31053bbe7`.
- `verify_jaeger_star_square_any_coordinate_lift_countermodel.py`: PASS;
  all \(3^8=6561\) omitted-owner words were checked, exactly 72 were legal,
  none was good in any coordinate, and a separate good downstairs state
  for the same graph/root/square was independently lifted successfully;
  note/checker SHA-256
  `ea24f997aaae027a25802a9ed291411199789077011c14a605c0956e615fb529` /
  `a26ba8296cdab88685089d43d7be8002d209d90d3d662ef45b86f89aabc053eb`.
- `verify_jaeger_star_square_order6_controls.py`: PASS; every good state of
  both simple 3-edge-connected cubic order-six graphs has an
  any-coordinate good local lift for every eligible smoothing pair;
  SHA-256
  `0f7d64413105ed6c69bd171734297fdf7e45b81af31bd812665efd92111dd73e`.
- `verify_jaeger_star_square_existential_order8.py`: PASS; all four simple
  3-edge-connected cubic order-eight graphs, all roots, and all 21 eligible
  smoothing pairs were exhausted, for 672 whole-fibre instances and zero
  failures; SHA-256
  `f9366e50d6e7b0e53b87114f6daf7ee1ca640ac224f1f8d1363190e87fd7124b`.
- `search_jaeger_star_square_existential_census.py`: PASS at orders 10 and
  12. The exact solver-free runs retained 14 and 57 simple
  3-edge-connected cubic graphs, 140 and 684 labelled roots, and 6,300 and
  53,352 eligible edge-pair instances, with zero failures. Witness-corpus
  digests were
  `1ae75f2864163e8ec6b04c0d92f012f00375ab55f92cc1284ad8233d4c42ab8f`
  and
  `b6b5420643799ddfe9ab3f252b0447c7de7704b27ddd8e75eaed39613b567b4e`;
  note/checker SHA-256
  `0fed1da84326097378145396bf2608aac44ad2c2e6a36c9ad464d215fc019015` /
  `bf3ce5e8c82bce4d84a14c80b538cb5337fd4a4a56016d0043eb70a4d82dbcd8`.
- `verify_jaeger_star_square_existential_order14.py`: PASS on the complete
  explicit witness corpus. It independently regenerated all 509 canonical
  connected cubic records, retained 341 simple 3-edge-connected graphs,
  required all 4,774 root keys and 572,880 eligible edge-pair witnesses,
  and reconstructed every downstairs/lifted tree certificate. The corpus
  contains 24,268 distinct checked downstairs states and has SHA-256
  `26dfe990a6655170f5fdcb6faf1424db279b57e8d094269417b7330fb5affd41`;
  search/checker SHA-256
  `f457fbf60bf5f2b94828bcf6295e0bf289b70205c55b70ab81d35de2fbc9697e` /
  `81545f6d0fc1331783a3d7e1d9f267961172a3398a05c635096c093d6638a791`.
- `verify_jaeger_square_fixed_label_selection_cut_no_go.py`: PASS; all 540
  indexed FiveCDC labellings of the triangular prism were generated, and
  the two selected edges in the three-edge cut always have one-point
  intersecting labels. The exact-good downstairs state and exact-good
  square-local lift both have profile \((2,0,2)\), so only the fixed-label
  selection bridge is refuted; note/checker SHA-256
  `c7fe3f077c695582b4288dcca6cbed726ed885d1976bf3225bfa2f39913c60d5` /
  `fba5be96ab40091e19f9e40a38b1eb5342ada638ef234944562ea304ccad3398`.
- `verify_jaeger_five_point_frontier.py`: PASS; 587 graphs, 944,974
  placements, and all 804,204 feasible fibres successful.
- `verify_jaeger_star_thinning_countermodel_34v.py`: PASS; both
  `lrat-check` and CakeML `cake_lpr` accepted the LRAT.
- `verify_jaeger_34v_star_good_witness.py`: PASS; exact five-point support
  and co-occurrence graph \(K_5\).
- `verify_jaeger_coordinate_five_order44.py`: PASS; 31 graphs and 1,364
  independently reconstructed literal star witnesses.

The positive order-14 and order-38 computations have the trust boundaries
stated in the manuscript. They are not represented as universal proofs or
as witness-by-witness independently checked certificate packages. The
symmetric-descent coverage verifier does not duplicate the C++ state
enumeration. The 16-vertex kernel-closure no-go is a counterexample only to
the explicitly stronger closure lemma; the independent five-point witness
shows that it is not a FiveCDC counterexample. The literature boundary was
also re-audited against Hušek--Šámal, arXiv:2607.24724v1: their Theorem 3.16
independently gives the exact component-parity characterization, their
Conjecture 3.19 is the equivalent flow-selection problem, and their
introduction explicitly retains FiveCDC as open.
