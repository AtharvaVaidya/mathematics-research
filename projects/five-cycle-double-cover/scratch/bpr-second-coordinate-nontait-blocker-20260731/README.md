# Order-18 non-Tait blocker for the refined BPR gate

This package gives an exact, vertex-minimal obstruction to the proposed
partner-free/all-in/fixed-residual second-coordinate descent gate.

The witness is an 18-vertex Blanuša snark.  A standard-library verifier
checks that it is simple, cubic, bridgeless, cyclically four-edge-connected,
and non-3-edge-colourable.  It checks the nowhere-zero
\(\mathbb F_2^3\)-flow, all 64 joins for the target value class, the optimal
potential \((0,8)\), and six short dual cut-space certificates showing
that every partner-free direction at both old odd components—the minimal
profiles \((3,3)\) and \((5,1)\)—is blocked by the reduced even-four-cut
gate.

The obstruction is representative-dependent: the same target class has
two other optimal joins, and each admits a certified descent to \((0,0)\).
This limitation is included explicitly in the proof and verifier.

The host has girth five.  It therefore settles the requested non-Tait,
cyclically-four structural question, but remains outside the girth-ten
domain of the full BPR conjecture.

The independent small-order audit generates every connected simple cubic
graph through order 16 with nauty `geng`.  The Petersen graph is the only
cyclically-four non-Tait host below order 18; a separate exhaustive checker
enumerates its 28,560 nowhere-zero flows and proves that it has no relevant
optimal state.  Thus order 18 is smallest in this precise host/state domain.

Run the complete frozen audit:

```sh
./run_all.sh
```

Or run the components:

```sh
python3 -B verify_certificate.py
python3 -B search_petersen.py
python3 -B verify_small_order_census.py  # requires nauty geng
```

`search_snarks18.py` records the Z3-assisted discovery search.  The
certificate verifier does not import it, does not use Z3, and does not trust
its model.

This is a negative result about one proof mechanism.  It is **not** a
counterexample to BPR and **not** a proof or disproof of FiveCDC.

All research text, code, and certificate files in this package were
produced by OpenAI Codex under human direction and have not yet received
independent human peer review.
