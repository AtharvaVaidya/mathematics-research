# Coloured surfaces and Kempe surgery for \(D_5\)-flows

This directory contains a restrained working research note about structural
and computational results from the FiveCDC project.

It does **not** claim a proof or disproof of the five-cycle-double-cover
conjecture. It also does not claim a result about the orientable FiveCDC.

The July 31 update proves a stronger human-checkable compression delimiter.
A graph-dependent rule may inspect the full local affine triangle of the
supplied Oum cover, but equal triangle states must reuse the same local
recolouring.  A 12-vertex simple bridgeless cubic witness has connected
state-adjacency graphs for all old pairs and full cycle-space rank, forcing
such a rule to be a coboundary.  Weight-two outputs would require
\(K_6\to R_5\), impossible because \(\omega(R_5)=5\).  Order 12 is sharp
for this mechanism.  The graph is Tait-colourable, and its positive cover
uses different local permutations at two occurrences of the same state;
the theorem is not a FiveCDC counterexample.

The same update contains a stronger positive theorem for the narrowed
edge-elimination route. In any Tait-colourable cubic graph, an explicit
edge-label formula makes any prescribed circuit exactly one \(D_5\)
factor. Hence every edge pair in a 2-connected Tait cubic graph is
root-feasible, and inverse insertion gives a five-cover whenever the
eliminated graph is Tait-colourable. The unresolved branch is non-Tait.
The existence statement is a special case of a stronger known 4-CDC lemma
of Hoffmann-Ostenhof; the note presents the explicit \(D_5\) formula and
rooted insertion adaptation, not a novelty claim for that existence result.

The July 31 certificate update proves a finite rooted frontier: every simple
cyclically 4-edge-connected cubic graph through order 28 is feasible for
every independent root pair, conditional on the documented Snarkhunter
source boundary.  The non-Tait part has 14,009 graphs and 10,689,351 root
pairs; 30,858 explicit D5 flows cover them all, and a separately written checker
validates the flows and exhausts all pairs without importing the SAT
generator.  This is a finite auxiliary theorem, not FiveCDC, and priority
for this precise census has not been established.

The update also gives two exact rooted tools.  A local transition-boundary
construction characterizes factor connectivity with a linear-size native
SAT/XOR encoding and an explicit \(8m\)-variable, \(133m/3\)-clause CNF.
Across a cubic three-edge cut, a six-state internal/external cap signature
supports a human-checkable typed gluing lemma.  A complete all-flow census
of 138,144 rooted interfaces through order 14 finds a double star in every
signature; an independent Python replay covers orders only through 10.
The universal double-star premise remains open, so this finite frontier does
not prove rooted feasibility or FiveCDC.

The relevant minimum-obstruction domain is now sharply separated from that
small unrestricted census.  A human nonbacktracking-walk proof shows that
every cap cut from an eliminated girth-ten parent has order at least 44 and
forces parent order at least 88.  If both shore caps are Tait-colourable,
external-mode states make them glue root-good; the exact remaining branch
has a non-Tait cap of order at least 44.  Six explicit checked flows give
the full typed signature on one 890-vertex Petersen--Foster high-girth
non-Tait control.  None of these statements proves the universal
double-star premise.

Files:

- `main.tex`: manuscript source.
- `references.bib`: cited primary and standard sources.
- `main.pdf`: rendered draft, when generated.
- `orbit-certificate.txt`: finite 12-state contraction-orbit certificate.
- `HUMAN-REVIEW.md`: a claim-by-claim review guide.
- `PUBLICATION-ASSESSMENT.md`: restrained novelty and readiness assessment.
- `SHA256SUMS`: digests of the draft package.

## Build

From `projects/five-cycle-double-cover`:

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
(cd scratch/eight-to-five-triangle-state-rigidity-20260731 && ./run_all.sh)
python3 scratch/check_d5_contraction_circuit_orbit_counterexample.py
python3 scratch/check_d4_cubic_trap_root_universality.py
sh scratch/d5-tait-prescribed-circuit-lift-20260731/run_all.sh
sh scratch/d5-tait-prescribed-circuit-lift-blind-audit-20260731/run_all.sh
(cd scratch/d5-root-transition-sat-20260731 && ./run_all.sh)
(cd scratch/d5-typed-cap-double-star-frontier-20260731 && ./run_all.sh)
(cd scratch/d5-root-pair-census-20260731 && ./run_all.sh)
(cd scratch/d5-relevant-cap-order44-cutoff-20260731 && ./run_all.sh)
(cd scratch/petersen-foster-full-typed-cap-signature-20260731 && ./run_all.sh)
python3 scratch/verify_d5_surface_chi_plateaus_order12.py
python3 scratch/verify_d5_root_euler_potential_reports.py
python3 scratch/verify_d5_root_kempe_order14_report.py
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_root_component_distance_order16_summary.py
python3 scratch/verify_d5_root_feasibility_lift13_girth10.py
```

The complete census producers require Brendan McKay's `geng`. The
independent plateau verifiers regenerate graph identities and arithmetic but
semantically replay selected rows rather than rerunning every expensive
enumeration.  The typed-cap C++ census is independently reimplemented only
through order 10.  These scopes are stated explicitly in the manuscript.

The draft contains a full AI-use disclosure. It should not be submitted or
cited as vetted research until a human graph theorist has checked the proofs,
the finite certificates, and the literature comparison.

Verify the frozen package with:

```sh
(cd preprint-d5-surface-kempe && shasum -a 256 -c SHA256SUMS)
```
