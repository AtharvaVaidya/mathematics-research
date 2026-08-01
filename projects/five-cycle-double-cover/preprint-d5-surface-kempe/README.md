# Coloured surfaces and Kempe surgery for \(D_5\)-flows

This directory contains a restrained working research note about structural
and computational results from the FiveCDC project.

It does **not** claim a proof or disproof of the five-cycle-double-cover
conjecture. It also does not claim a result about the orientable FiveCDC.

The July 31 update also proves a human-checkable compression delimiter:
a 12-vertex simple bridgeless cubic Oum cover has local old-coordinate
triangles spanning \(Z_1(K_6;\mathbb F_2)\), so every arbitrary
context-free old-pair lookup is forced to be a coboundary.  Weight-two
outputs would require \(K_6\to R_5\), impossible because
\(\omega(R_5)=5\).  The witness is Tait-colourable; this excludes only
the static lookup mechanism and is not a FiveCDC counterexample.

The same update contains a stronger positive theorem for the narrowed
edge-elimination route. In any Tait-colourable cubic graph, an explicit
edge-label formula makes any prescribed circuit exactly one \(D_5\)
factor. Hence every edge pair in a 2-connected Tait cubic graph is
root-feasible, and inverse insertion gives a five-cover whenever the
eliminated graph is Tait-colourable. The unresolved branch is non-Tait.
The existence statement is a special case of a stronger known 4-CDC lemma
of Hoffmann-Ostenhof; the note presents the explicit \(D_5\) formula and
rooted insertion adaptation, not a novelty claim for that existence result.

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
sh scratch/d5-tait-prescribed-circuit-lift-20260731/run_all.sh
sh scratch/d5-tait-prescribed-circuit-lift-blind-audit-20260731/run_all.sh
python3 scratch/verify_d5_surface_chi_plateaus_order12.py
python3 scratch/verify_d5_root_euler_potential_reports.py
python3 scratch/verify_d5_root_kempe_order14_report.py
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_root_component_distance_order16_summary.py
python3 scratch/verify_d5_root_feasibility_lift13_girth10.py
```

The complete census producers require Brendan McKay's `geng`. The
independent verifiers regenerate graph identities and arithmetic but
semantically replay selected rows rather than rerunning every expensive
enumeration. That scope is stated explicitly in the manuscript.

The draft contains a full AI-use disclosure. It should not be submitted or
cited as vetted research until a human graph theorist has checked the proofs,
the finite certificates, and the literature comparison.

Verify the frozen package with:

```sh
(cd preprint-d5-surface-kempe && shasum -a 256 -c SHA256SUMS)
```
