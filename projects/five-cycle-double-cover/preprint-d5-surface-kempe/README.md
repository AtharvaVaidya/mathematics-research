# Coloured surfaces and Kempe surgery for \(D_5\)-flows

This directory contains a restrained working research note about structural
and computational results from the FiveCDC project.

It does **not** claim a proof or disproof of the five-cycle-double-cover
conjecture. It also does not claim a result about the orientable FiveCDC.

Files:

- `main.tex`: manuscript source.
- `references.bib`: cited primary and standard sources.
- `main.pdf`: rendered draft, when generated.
- `orbit-certificate.txt`: finite 12-state contraction-orbit certificate.
- `HUMAN-REVIEW.md`: a claim-by-claim review guide.
- `PUBLICATION-ASSESSMENT.md`: restrained novelty and readiness assessment.
- `SHA256SUMS`: digests of the draft package.

## Build

From the repository root:

```sh
mkdir -p tmp/pdfs/d5-surface-kempe
tectonic -X compile preprint-d5-surface-kempe/main.tex \
  --outdir tmp/pdfs/d5-surface-kempe
cp tmp/pdfs/d5-surface-kempe/main.pdf \
  preprint-d5-surface-kempe/main.pdf
```

## Core verification

```sh
python3 scratch/audit_d5_surface_euler_switch.py
python3 scratch/check_d5_contraction_circuit_orbit_counterexample.py
python3 scratch/check_d4_cubic_trap_root_universality.py
python3 scratch/verify_d5_surface_chi_plateaus_order12.py
python3 scratch/verify_d5_root_euler_potential_reports.py
python3 scratch/verify_d5_root_kempe_order14_report.py
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_terminal_foreign_block_order14.py
python3 scratch/verify_d5_cyclic_block_lex_reports.py
python3 scratch/check_d5_cyclic_block_one_step_no_go_order14.py
python3 scratch/check_d5_no_fresh_coordinate_blocker_order12.py
```

The complete census producers require Brendan McKay's `geng`. The
independent verifiers check graph identities, arithmetic, frozen report
hashes, and focused semantics.  The directed-root blocker implementation
is separately structured.  Their exact scopes are stated in the
manuscript.

The draft contains a full AI-use disclosure. It should not be submitted or
cited as vetted research until a human graph theorist has checked the proofs,
the finite certificates, and the literature comparison.

Verify the frozen package with:

```sh
(cd preprint-d5-surface-kempe && shasum -a 256 -c SHA256SUMS)
```
