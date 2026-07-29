# Two exact four-pole reductions for FiveCDC

This directory contains a standalone AI-assisted working preprint about two
positive substitutions for the **standard** five-cycle double cover
conjecture.

Resolution status: FiveCDC remains open. The manuscript proves that:

- the Petersen four-pole extends every repeated-pair boundary placement
  `(q,q,r,r)`;
- the Heawood four-pole extends all 640 xor-zero `D5` boundary words; and
- inserting either pole in place of two independent edges of a
  FiveCDC-positive cubic graph preserves FiveCDC, simplicity, and
  bridgelessness under the stated hypotheses.

It also gives `K3,3` minus adjacent vertices as a sharp counterexample to
the tempting claim that every bridgeless bipartite cubic adjacent-deletion
pole is full-boundary.

Build:

```sh
SOURCE_DATE_EPOCH=1785271878 tectonic main.tex
```

See `REPRODUCIBILITY.md` for the exact replay and `HUMAN-REVIEW.md` for the
publication gate. OpenAI Codex agents materially contributed to the search,
certificates, software, and prose under Atharva Vaidya's direction. The
disclosure in the paper must not be removed.
