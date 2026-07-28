# Validation record

Date: 2026-07-28

Resolution status: FiveCDC remains unresolved.

The manuscript compiled successfully with
`SOURCE_DATE_EPOCH=1785271878 tectonic main.tex`, reproducing the committed
PDF byte for byte. `pdfinfo` reported 25 US-letter pages, no encryption, no
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
shows that it is not a FiveCDC counterexample.
