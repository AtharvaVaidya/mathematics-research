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
descent statement remains open.

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
