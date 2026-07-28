# Publication manifest: marked circuits and rooted interfaces

Date: **2026-07-27**

Status: **AI-assisted research draft; the Five-Cycle Double Cover
Conjecture remains unresolved.**

This manifest records the material included through the
`codex/fivecdc-matching-frontier-20260727` branch, which extends the
earlier `codex/five-cdc-marked-circuits-20260727` publication branch.
OpenAI Codex agents, directed by Atharva Vaidya, generated or revised the
arguments, programs, computations, audits, and prose. Agent cross-checks
are not independent human verification or peer review.

## Prescribed-root matching frontier

`MATCHING_FRONTIER_20260727.md` indexes the added matching branch:

- `docs/prescribed-root-matching-deficiency-frontier.md`
- `docs/focused-theta-choice-census-frontier.md`
- `docs/boundary-eight-rotation-closure-frontier.md`
- `docs/singleton-ge-tait-frontier.md`
- `docs/root-insertion-two-factor-frontier.md`
- `scratch/prescribed-root-matching-deficiency-checker.py`
- `scratch/rotation-closure-countermodel-checker.py`
- `scratch/focused-local-insertion-census.cpp`
- `scratch/verify-root-insertion-census.py`
- `scratch/check-root-insertion-published.py`
- `scratch/focused-local-insertion-result.ndjson`
- `scratch/root-insertion-independent-through22.json`
- `scratch/root-insertion-independent-through26.json`
- `scratch/root-insertion-independent-order28-combined.json`
- `scratch/root-insertion-independent-order28-shard0.json` through
  `scratch/root-insertion-independent-order28-shard3.json`
- `scratch/focused-theta-choice-census.cpp`
- `scratch/verify-focused-theta-choice-census.py`
- `scratch/focused-theta-choice-census-result.json`
- `search/focused-theta-choice-through28-20260727/`

The universal deficiency-two theorem, boundary-eight incidence theorem,
and disconnected singleton-case Tait theorem have complete displayed
proofs.  The new oddness argument closes the whole all-singleton branch
for the standard five-cycle-double-cover conclusion.  The stronger
prescribed-root connected singleton case remains open.  The focused and
root-insertion censuses through order 28 are exact over the retained
corpora but are not promoted to universal statements.

## Preprint

The complete `preprint-rooted-four-cut/` directory is included:

- `main.tex`
- `references.bib`
- `output/pdf/main.pdf` (29 pages)
- `README.md`
- `AUDIT.md`
- `NOVELTY-ASSESSMENT.md`
- `CHECKSUMS.sha256`
- `CHECKSUMS-PUBLISHED.sha256`

The abstract, front-matter disclosure, introduction, README, and novelty
assessment all state that the paper neither proves nor disproves five-CDC.

## Human-checkable proof and reduction notes

- `docs/five-cdc-elliptic-quadratic-flow-model.md`
- `docs/four-mark-core-closure.md`
- `docs/root-edge-reduction-four-cut-gate.md`
- `docs/rooted-cycle-translation-obstruction.md`
- `docs/exceptional-cyclic-three-root-signature-factorization.md`
- `docs/rooted-base-pair-cycle-cut-certificate.md`
- `docs/rooted-four-mark-unmarked-toggle.md`
- `docs/rooted-four-mark-bridgeless-reduction.md`
- `docs/rooted-four-mark-odd-k23-reduction.md`
- `docs/rooted-four-mark-ozeki-linkage-gate.md`
- `docs/rooted-four-mark-p4-row-star-reduction.md`
- `docs/rooted-four-mark-singleton-endpoint-closure.md`
- `docs/order22-universal-four-separation-screen.md`
- `docs/exceptional-four-cut-surviving-split-atoms.md`
- `docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`
- `docs/rooted-three-pole-base-pair-closure-target.md`
- `docs/rooted-three-pole-tait-cap-closure.md`
- `docs/rooted-cap-triangle-induction.md`
- `docs/rooted-cap-end-factor-fork-lift.md`
- `docs/five-cdc-five-point-triangle-list-lift.md`

The current research state and open obligations are recorded in:

- `docs/current-status.md`
- `docs/proof-obligation-ledger.md`
- `docs/experiment-ledger.md`
- `docs/publication-assessment-20260726.md`

## Compact checker and result files

- `scratch/tait_all_coloring_mark_separation.cpp`
- `scratch/verify_order22_separation_via_matchings.cpp`
- `scratch/order22-universal-four-separation-result.json`
- `scratch/rooted_cycle_translation_blockers.py`
- `scratch/verify_rooted_cycle_translation_blockers.mjs`
- `scratch/rooted-cycle-translation-blockers-result.json`
- `scratch/rooted_three_pole_signature_factorization.py`
- `scratch/verify_rooted_three_pole_signature_factorization.mjs`
- `scratch/rooted-three-pole-signature-factorization-result.json`
- `scratch/rooted-four-mark-order20-screen-result.json`
- `scratch/verify_rooted_cap_triangle_table.py`
- `scratch/rooted-cap-triangle-table-v2.json`
- `scratch/verify_rooted_end_factor_fork_lift.py`
- `scratch/rooted-end-factor-fork-lift-replay.json`
- `scratch/verify_five_point_triangle_list_lift.py`
- `scratch/five-point-triangle-list-lift-result.json`
- `scratch/verify_five_point_triangle_list_lift.mjs`
- `scratch/five-point-triangle-list-lift-independent.json`
- `scratch/boundary_two_orbit_witness_cadical.cpp`
- `scratch/verify_boundary_two_orbit_witness.py`
- `scratch/verify_boundary_two_orbit_witness_fast.cpp`

## Reproducibility packages

The branch includes all non-cache files in:

- `search/rooted-three-pole-frontier-20260727/` — 90 files, 354,336
  bytes; complete compact order-17 base-pair records and replay scripts.
- `search/four-pole-order22-cap-20260727/` — 84 files, 23,728,989
  bytes; completed cyclically-four order-22 cap-slice records, compressed
  transcripts, corpus identities, and verifier sources.
- `search/four-pole-order24-cyclic4-cap-20260727/` — 44 files,
  1,067,314 bytes; complete retained cyclically-four order-24
  classification and its corrected scope documentation.
- `search/four-pole-order26-cyclic4-cap-20260727/` — 44 files,
  14,019,526 bytes; complete retained cyclically-four order-26
  classification.  Its 1,297 cap records and 859,911 deletion-pole rows
  remain valid; the package alone implies no global exceptional-pole
  lower bound.
- `search/four-pole-order26-strict-cap-probe-20260727/` — 28 files,
  2,341,537 bytes; a finite retained strict-snark source probe, explicitly
  distinct from the complete cyclically-four order-26 classification.
- `search/mnp-h2-h5-aa-deletion-probe-20260727/` — 12 files, 129,104
  bytes; explicit \(H_2,\ldots,H_5\) prescribed-\(AA\) certificates and a
  solver-independent checker.
- `search/rooted-three-pole-nontait-endpoint-frontier-20260727/` — 44
  files, 9,037,638 bytes; complete retained endpoint-factor classification
  through order 26, two byte-identical solver transcripts, a
  solver-independent replay, the sound pure-relation cap bound 54, and,
  through the separate endpoint-fork lift, the scoped mixed-branch bound.
- `search/four-pole-order28-cyclic4-cap-20260727/` — 36 files, 851,281
  bytes in Git; complete 12,517-graph source, theorem, reproduction notes,
  logs, statuses, hashes, compact reports, and checker.  The full local
  package has two independently replayed positive labellings for each of
  9,725,709 poles and proves the scoped order-30 bound.
- `search/focused-theta-choice-through28-20260727/` — compact complete
  retained source corpus, generator logs, two classifier sources, frozen
  result streams, and aggregate verifier for 14,009 graphs and 10,689,351
  independent root pairs.
- `search/rooted-three-pole-c3-cap-frontier-through24-20260727/` —
  compact publication subset of the complete 10,824,084-root
  triangle-free cap screen: source corpora, expanded cores, logs,
  statuses, hashes, summaries, report, verifier, and regeneration notes.

Excluded deliberately: `__pycache__`, `.DS_Store`, private attachments,
temporary `/private/tmp` output, compiled checker binaries, unrelated dirty
files, broad 294 MB graph streams, multi-gigabyte proof files, and
placeholder material. The two byte-identical 34,355,648-byte C3-cap
transcripts are omitted with compressed and uncompressed hashes and exact
regeneration instructions retained. The order-28 witness stream
(363,463,166 compressed bytes) and generated pole stream (40,210,290
compressed bytes) are also omitted; their compressed and uncompressed
hashes and regeneration commands are retained.

## Validation performed before publication

- Every entry in the full laboratory
  `preprint-rooted-four-cut/CHECKSUMS.sha256` passed; every present Git
  artifact passes `CHECKSUMS-PUBLISHED.sha256`.
- The preprint PDF metadata reports 29 pages.  Extracted first-page text
  contains the no-resolution statement, and page two contains the explicit
  AI-use disclosure.
- A clean Tectonic 0.16.9 rebuild produced the committed 29-page PDF with
  SHA-256
  `8d0da87f5e07abf1dc5cc25e05f16faeb442a7dead8754f7b8bb4b88596f9b95`.
  All 29 pages were rendered and visually inspected.
- JSON syntax checks passed for the order-22 separation result, order-17
  base-pair report, and cyclically-four order-22 report.
- Both independently structured order-22 separation checkers compiled and
  agreed on the complete order-12 control:
  85 rows, 80 Tait-colourable graphs, 307 normalized colourings, zero
  target-four witnesses; the matching replay counted 902 perfect matchings.
- The rooted order-17 transcript verifier reconstructed 654,676 canonical
  cores, 15,645,623 nonbridge roots, and zero base-pair violations.
- `verify_report.py` accepted the frozen rooted-frontier report.
- The compact package checksum ledgers passed.  The corrected order-24 and
  order-26 cyclically-four `verify.py` programs were both replayed and
  reproduced their committed JSON reports byte for byte.  The order-26
  replay reconstructed all 1,297 source graphs and 859,911 deletion poles.
  The \(H_2,\ldots,H_5\) verifier had already reproduced its committed
  report independently.
- The corrected rooted base-pair note and Tait-cap closure proof were
  checked for local references, explicit scope, the mixed-relation
  counterexample, and AI-use disclosure.  The audit withdraws the former
  one-sided proof of the order-26 and order-28 lower-bound conclusions
  while preserving the exact finite cyclically-four cap classifications;
  the later endpoint-fork proof independently restores the stated scoped
  order-28 bound.
- The endpoint package passed `SHA256SUMS`, `SOURCES.sha256`, and a fresh
  independent semantic replay over 1,360,452 roots in 38,244 cores; it
  reproduced `report.json` byte for byte.
- The fork-triple checker reproduced
  `scratch/rooted-cap-triangle-table-v2.json` byte for byte. The complete
  two-implementation triangle-free screen now classifies 10,824,084 roots
  with no empty signature or base-pair violation. The compact Git subset's
  present-artifact checksums and source manifest pass; the full row replay
  requires the two hash-frozen omitted transcripts.
- The endpoint-fork checker reproduced
  `scratch/rooted-end-factor-fork-lift-replay.json` byte for byte,
  enumerating all 60 ordered connector triangles, 30 forks, and 900 ordered
  fork pairs.  The human lift bypasses that screen and restores the
  stated bridge-free simple terminal-distinct fixed-five lower bound 28.
- The full order-28 package passed both semantic replays over 9,725,709
  rows and 19,451,418 displayed labellings.  Its two positive boundary
  orbits exclude all six exceptional masks and raise the same scoped lower
  bound to 30.  The independently written C++ replay was rerun before this
  publication and reproduced its compact JSON byte for byte.
- The Python and JavaScript five-point checkers independently agree on all
  392 five-set/line cases.
- The two small prescribed-root countermodel checkers pass using only the
  Python standard library. The focused-theta package checksum ledger and
  aggregate verifier pass; the retained result classifies 14,009 graphs
  and 10,689,351 root pairs with zero all-dumbbell cases through order 28.

No fresh full order-22 census is claimed by this publication preparation.
The frozen reports state their exact scope and provenance.
