# Publication manifest: marked circuits and rooted interfaces

Date: **2026-07-27**

Status: **AI-assisted research draft; the Five-Cycle Double Cover
Conjecture remains unresolved.**

This manifest records the material added on the
`codex/five-cdc-marked-circuits-20260727` branch.  OpenAI Codex agents,
directed by Atharva Vaidya, generated or revised the arguments, programs,
computations, audits, and prose.  Agent cross-checks are not independent
human verification or peer review.

## Preprint

The complete `preprint-rooted-four-cut/` directory is included:

- `main.tex`
- `references.bib`
- `output/pdf/main.pdf` (24 pages)
- `README.md`
- `AUDIT.md`
- `NOVELTY-ASSESSMENT.md`
- `CHECKSUMS.sha256`

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
  remain valid, but no global exceptional-pole lower bound follows.
- `search/four-pole-order26-strict-cap-probe-20260727/` — 28 files,
  2,341,537 bytes; a finite retained strict-snark source probe, explicitly
  distinct from the complete cyclically-four order-26 classification.
- `search/mnp-h2-h5-aa-deletion-probe-20260727/` — 12 files, 129,104
  bytes; explicit \(H_2,\ldots,H_5\) prescribed-\(AA\) certificates and a
  solver-independent checker.
- `search/rooted-three-pole-nontait-endpoint-frontier-20260727/` — 44
  files, 9,037,638 bytes; complete retained endpoint-factor classification
  through order 26, two byte-identical solver transcripts, a
  solver-independent replay, and the sound pure-relation cap bound 54.

Excluded deliberately: `__pycache__`, `.DS_Store`, private attachments,
temporary `/private/tmp` output, compiled checker binaries, unrelated dirty
files, broad 294 MB graph streams, multi-gigabyte proof files, the running
`search/rooted-three-pole-c3-cap-frontier-through24-20260727/` screen, and
the unfinished `search/four-pole-order28-cyclic4-cap-20260727/`
classification or other placeholder material.

## Validation performed before publication

- Every entry in `preprint-rooted-four-cut/CHECKSUMS.sha256` passed.
- The preprint PDF metadata reports 24 pages.  Extracted first-page text
  contains the no-resolution statement, and page two contains the explicit
  AI-use disclosure.
- A clean Tectonic 0.16.9 rebuild produced the committed 24-page PDF with
  SHA-256
  `cdeeef2049fb4cb267b1b01328f412bcd9293f0e93a403754edccebbf0f2c9c4`.
  All 24 pages were rendered and visually inspected.
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
  global order-26 and order-28 lower-bound conclusions while preserving the
  exact finite cyclically-four cap classifications.
- The endpoint package passed `SHA256SUMS`, `SOURCES.sha256`, and a fresh
  independent semantic replay over 1,360,452 roots in 38,244 cores; it
  reproduced `report.json` byte for byte.
- The fork-triple checker reproduced
  `scratch/rooted-cap-triangle-table-v2.json` byte for byte.  The proof is
  conditional on the explicitly excluded running triangle-free screen and
  does not claim the mixed branch or an order-28 lower bound.

No fresh full order-22 census is claimed by this publication preparation.
The frozen reports state their exact scope and provenance.
