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
rooted family. It does not claim a proof or counterexample to FiveCDC.

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
