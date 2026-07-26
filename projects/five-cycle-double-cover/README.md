# Five-cycle double cover research archive

Status as of **2026-07-26**: the standard five-cycle double cover
conjecture remains open.  Nothing in this directory is a proof or a
counterexample to that conjecture.

This is a curated, reproducible publication bundle from an autonomous
conjecture-resolution laboratory.  It contains two research drafts, a
computer-free marked-graph theorem, explicit human-checkable
countermodels to two intermediate proof strategies, exact SAT/XOR
documentation, and compact checker sources.  Temporary search output and
multi-gigabyte certificates are deliberately not committed.

## Main research drafts

- [`output/pdf/four-universally-separated-marks-preprint-20260726.pdf`](output/pdf/four-universally-separated-marks-preprint-20260726.pdf)
  proves a marked cubic-graph theorem.  Under universal Tait separation
  and a precise cyclic-cut inequality, four marked edges lie in one
  four-mark cycle or two disjoint two-mark cycles.  The argument is
  computer-free.  Its source is
  [`preprint-four-mark-core/main.tex`](preprint-four-mark-core/main.tex),
  and a standalone proof is in
  [`docs/four-mark-core-closure.md`](docs/four-mark-core-closure.md).
- [`output/pdf/two-connected-countermodels-five-cdc-preprint.pdf`](output/pdf/two-connected-countermodels-five-cdc-preprint.pdf)
  gives explicit 40- and 46-vertex countermodels to two proposed
  one-circuit repair strategies.  Both graphs positively have standard
  five-cycle double covers, so they are not counterexamples to five-CDC.
  Its source is
  [`preprint-fano-one-switch/main.tex`](preprint-fano-one-switch/main.tex).

Both PDFs prominently disclose substantive AI involvement and explicitly
state their scope.  Their novelty assessments are provisional pending
independent expert literature review.

## Latest structural branch

The connected eight-mark branch remains open.  The newest notes expose
its exact remaining constraints without claiming a five-CDC resolution:

- [`docs/kempe-transversality-and-eight-mark-girth.md`](docs/kempe-transversality-and-eight-mark-girth.md)
  proves human-checkable Kempe and marked-girth lemmas and records the
  limits of a finite counterexample.
- [`docs/eight-mark-bichromatic-code.md`](docs/eight-mark-bichromatic-code.md)
  reduces the fixed-colouring problem to an exact signed-graph component
  test.
- [`docs/connected-eight-mark-paired-cut-condition.md`](docs/connected-eight-mark-paired-cut-condition.md)
  derives the paired cyclic-cut condition that retains the four matching
  pairs lost by the simpler unpaired inequality.
- [`docs/cyclic-four-separated-triple-atom-reduction.md`](docs/cyclic-four-separated-triple-atom-reduction.md)
  explicitly marks the proposed cyclic-four atom lemma as refuted while
  retaining its sound conditional reductions.

The compact package
[`search/cyclic4-universally-separated-triple-n24-20260726/`](search/cyclic4-universally-separated-triple-n24-20260726/)
freezes the refuting order-24 graph, all 144 retained hits, exact search
scope, canonical records, hashes, and independently structured single-
and batch-verifiers.  It establishes that a universally separated triple
can occur in a cyclically four-edge-connected Tait-colourable cubic graph.
All 144 construction hits have marked-subdivision girth five, however,
so none satisfies the surviving connected-branch threshold of ten.

## Human-checkable material

- [`docs/four-mark-core-closure.md`](docs/four-mark-core-closure.md) gives
  the full computer-free four-mark proof.
- [`search/connected-one-switch-countermodel-40v-20260726/HUMAN-PROOF.md`](search/connected-one-switch-countermodel-40v-20260726/HUMAN-PROOF.md)
  proves the planar 40-vertex intermediate countermodel.
- [`search/fano-pure-merge-one-switch-countermodel-46v-20260726/HUMAN-PROOF.md`](search/fano-pure-merge-one-switch-countermodel-46v-20260726/HUMAN-PROOF.md)
  proves the nonplanar 46-vertex pure-merge countermodel.
- [`docs/encoding.md`](docs/encoding.md) proves the equivalence between
  five Eulerian edge-subsets and the exact SAT/XOR edge-label formula,
  including graph-convention cautions.
- [`docs/publication-assessment-20260726.md`](docs/publication-assessment-20260726.md)
  separates apparently new statements from known ingredients.
- [`docs/current-status.md`](docs/current-status.md) and
  [`docs/proof-obligation-ledger.md`](docs/proof-obligation-ledger.md)
  record the broader search status and remaining proof obligations.

## Quick independent checks

The compact countermodel checkers use only the Python standard library:

```sh
python3 search/fano-value-class-flow-countermodel-20260726/independent_checker.py
python3 search/connected-one-switch-countermodel-40v-20260726/independent_checker.py
python3 search/connected-one-switch-countermodel-40v-20260726/verify_package.py
python3 search/fano-pure-merge-one-switch-countermodel-46v-20260726/independent_checker.py
python3 -m tools.test_encode_five_cdc_xor_fast
python3 search/h4-all-minimum-support-packing-20260726/verify_upper_witness.py
python3 -B search/cyclic4-universally-separated-triple-n24-20260726/verify_package.py
```

The 40-vertex checker optionally uses nauty's `labelg` to recheck the
canonical graph6 encoding.  Its semantic checks still run when nauty is
absent.

The complete laboratory replay is documented in
[`REPRODUCING.md`](REPRODUCING.md).  Some commands there refer to the full
local laboratory rather than this curated Git bundle.  See
[`ARTIFACTS.md`](ARTIFACTS.md) for the exact included and omitted scope.

## Standard versus orientable five-CDC

This archive's primary target is the standard conjecture: at most five
Eulerian edge-subsets cover every edge exactly twice.  Empty Eulerian
subgraphs may pad a cover with fewer than five coordinates.  The
orientable version is stronger and is not silently substituted for the
standard formulation.

## AI-use disclosure

OpenAI Codex agents, operating under Atharva Vaidya's direction, made
substantive contributions throughout this project: proposing and
refuting intermediate claims, finding proof architectures and finite
constructions, writing programs and checkers, conducting literature
searches, drafting manuscripts, and performing additional agent audits.
Those agent audits are not independent human verification or peer review.

No mathematical claim should be accepted because an AI system generated
or checked it.  A human graph theorist should independently verify every
proof and attribution, rerun the checkers, conduct a specialist novelty
search, and assume normal scholarly responsibility before any formal
submission.
