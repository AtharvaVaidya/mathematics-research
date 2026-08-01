# Fano fixed-line preprint draft

This directory contains a cautious short-paper draft built around:

1. the universal combined-image theorem in
   `../docs/fano-combined-line-span.md`;
2. the exact two-cycle quadratic normal form;
3. a general simple-contraction obstruction; and
4. an unbounded-component cotree-diamond separation;
5. the Petersen fixed-line certificate in
   `../search/fano-two-cycle-petersen-countermodel-20260726/`; and
6. the cyclically 4-edge-connected order-60 all-seven fixed-flow
   obstruction in
   `../scratch/fano-cyclic4-allseven-order60-20260728.md`.

The paper is explicitly **not** a proof or disproof of the five-cycle
double cover conjecture. The displayed Petersen and order-60 graphs have
positive five-cycle double covers, and every member of the
unbounded-component family does as well.

Files:

- `main.tex` — manuscript source;
- `references.bib` — primary-source bibliography;
- `NOVELTY-ASSESSMENT.md` — provisional publication assessment and
  literature boundary;
- `main.pdf` — rendered draft, after a successful build.
- `SHA256SUMS` — frozen hashes for the source, bibliography, assessment,
  README, and rendered PDF.

Build:

```sh
tectonic --keep-intermediates --keep-logs main.tex
```

The manuscript, proofs, programs, literature triage, and prose were
substantively AI-assisted. “Independent checker” refers to a separate
implementation, not to independent human review. A human author must
verify the mathematics and literature, revise the paper, supply their
name, and take responsibility before submission.
