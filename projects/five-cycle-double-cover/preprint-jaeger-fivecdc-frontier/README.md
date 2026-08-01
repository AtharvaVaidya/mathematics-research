# Jaeger fixed-fibre FiveCDC frontier

This directory contains a standalone working preprint about an exact
fixed-multiplicity spanning-tree route to the standard five-cycle double
cover conjecture.

**Resolution status:** the conjecture remains open. The paper proves several
structural lemmas, gives human-sized counterexamples to tempting stronger
lemmas, records a dual-checked SAT certificate for another false
strengthening, gives a parity-element/cographic-base reformulation, and
reports bounded positive computations including an exact symmetric-descent
census through order 14. A separate dual-checked 16-vertex certificate
refutes a stronger kernel-closure lemma while an explicit five-point witness
in the same fibre preserves the actual target; a human triangle-contraction
theorem extends only that discarded closure obstruction to an infinite
rooted family. The exact component-parity target, unlike closure, is proved
invariant under nonroot triangle contraction and lifting by a seven-row local
argument. It does not claim a proof or counterexample to FiveCDC.
The revised exchange section proves the exact all-seven update law and
records two independently replayed order-16 no-gos: immediate descent and
fixed-kernel exposure are both false, while the broader full same-level
descent statement remains open. Simultaneous nonroot triangle expansions
give an exact Cartesian-product theorem with one \(S_3\) Cayley factor per
triangle, but the defect is not a product potential. A 36-vertex exact
countermodel shows that even the sorted seven-defect profile need not
decrease in one exchange; it nevertheless has a checked two-exchange
same-level escape. A 40-vertex exact state goes further: its complete
958-state radius-three same-level ball has no earlier descending boundary,
and its shortest escape has length four. This refutes every radius-three
plateau shortcut, but the state escapes and the unbounded component theorem
remains open. Two adjacent states with that same ordered profile have
total-defect Laplacians \(+10\) and \(-14\), so profile-only averaging and
universal sub/superharmonicity of total defect also fail. A further
solver-free order-eight example
shows that one fixed good state need not have a good square-local lift in
any coordinate; an alternate good state for the same graph and square does
lift. The paper proves an exact fixed-cover square-extension criterion:
the deleted edge labels must be equal or disjoint. Complete whole-fibre
censuses through downstairs order 16 find compatible state-and-lift choices
in all 8,370,612 graph/root/smoothing instances tested. All three order-18
snarks add 12,474 independently replayed positive instances, so the whole-fibre
square reduction remains open rather than refuted. A human three-edge-cut
argument on the triangular prism proves that no choice of a downstairs
five-cover can always make the two deleted labels equal or disjoint, even
though that literal tree state has a good square-local lift. Thus the fixed-
cover label criterion cannot supply the missing tree-state selection lemma.

**Priority correction:** Hušek and Šámal, *Exponentially Many Circuit
Double Covers*, arXiv:2607.24724v1 (submitted July 27, 2026), independently
give the equivalent five-support component-parity characterization in their
Theorem 3.16 and state the remaining equivalent flow-selection problem as
Conjecture 3.19. This draft therefore makes no novelty or priority claim for
its component criterion.

Build from this directory with:

```sh
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

The source artifacts and checkers referenced by the paper live one directory
above, in `scratch/`, `output/`, and `search/`. See `REPRODUCIBILITY.md` for
the short replay suite and `HUMAN-REVIEW.md` for the publication gate.

The prose and much of the research workflow were produced by OpenAI Codex
agents under Atharva Vaidya's direction. The detailed disclosure in the paper
is part of the manuscript and must not be removed.
