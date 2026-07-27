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
- `output/pdf/main.pdf` (21 pages)
- `README.md`
- `AUDIT.md`
- `NOVELTY-ASSESSMENT.md`
- `CHECKSUMS.sha256`

The abstract, first-page disclosure, introduction, README, and novelty
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

## Reproducibility packages

The branch includes all non-cache files in:

- `search/rooted-three-pole-frontier-20260727/` — 90 files, 354,336
  bytes; complete compact order-17 base-pair records and replay scripts.
- `search/four-pole-order22-cap-20260727/` — 84 files, 23,728,989
  bytes; completed cyclically-four order-22 cap-slice records, compressed
  transcripts, corpus identities, and verifier sources.

Excluded deliberately: `__pycache__`, `.DS_Store`, private attachments,
temporary `/private/tmp` output, compiled checker binaries, unrelated dirty
files, broad 294 MB graph streams, and multi-gigabyte proof files.

## Validation performed before publication

- Every entry in `preprint-rooted-four-cut/CHECKSUMS.sha256` passed.
- The preprint PDF metadata reports 21 pages, and extracted first-page text
  contains both the no-resolution statement and AI-use disclosure.
- A clean Tectonic 0.16.9 rebuild succeeded at 21 pages and produced
  identical extracted text.  The rebuilt PDF is not byte-identical because
  Tectonic records a new creation timestamp; the committed PDF is
  authenticated by the frozen checksum instead.
- JSON syntax checks passed for the order-22 separation result, order-17
  base-pair report, and cyclically-four order-22 report.
- Both independently structured order-22 separation checkers compiled and
  agreed on the complete order-12 control:
  85 rows, 80 Tait-colourable graphs, 307 normalized colourings, zero
  target-four witnesses; the matching replay counted 902 perfect matchings.
- The rooted order-17 transcript verifier reconstructed 654,676 canonical
  cores, 15,645,623 nonbridge roots, and zero base-pair violations.
- `verify_report.py` accepted the frozen rooted-frontier report.

No fresh full order-22 census is claimed by this publication preparation.
The frozen reports state their exact scope and provenance.
