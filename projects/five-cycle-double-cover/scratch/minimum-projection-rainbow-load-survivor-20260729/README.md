# A goal-free survivor of the rainbow/load/static-exchange filters

Date: 2026-07-29

Status: **EXACT METHOD OBSTRUCTION / NOT GLOBALLY MINIMUM / NOT A
FIVECDC RESOLUTION**.

This package strengthens the smaller local rainbow/load counterstate.
At total support fourteen it gives a boundary state with:

- a rainbow-odd dual witness;
- all six witness switches integrable;
- zero clean and zero circuit-deletion outcomes across those six
  switches—and, by the prior full component-map census, across every
  integrable component-map tuple;
- all nine colour-load inequalities; and
- a 278-vertex simple bridgeless cubic realization satisfying all four
  complete static shortest-\(T_c\)-join inequalities.

The realized 14-edge projection is uncleanable, but exact contraction
and base cycle-space enumeration prove that the graph's global minimum
projection size is seven.  It is therefore a proof-method obstruction,
not a FiveCDC counterexample.

The human proof is in `HUMAN-PROOF.md`.  Replay the two exact
implementations from the repository root:

```sh
python3 projects/five-cycle-double-cover/scratch/minimum-projection-rainbow-load-survivor-20260729/verify.py
python3 projects/five-cycle-double-cover/scratch/minimum-projection-rainbow-load-survivor-20260729/independent_audit.py
shasum -a 256 -c projects/five-cycle-double-cover/scratch/minimum-projection-rainbow-load-survivor-20260729/SHA256SUMS
```

The independent audit uses the separately written and frozen size-14
cycle-space model, reconstructs the graph in its different edge
labeling, and recomputes the six-map table, 384,064 semantic low-flow
states, weighted minimum, inflation, and four shortest joins.

The earlier exhaustive theorem through support thirteen establishes
minimality only for the stronger notion of a boundary state with no
clean or deletion component map at all.  No claim is made that support
fourteen is minimal under weaker, single-witness-only conditions.

OpenAI Codex agents under Atharva Vaidya's direction developed the
result, code, proof, and audits.  Agent cross-checks are not independent
human verification or peer review.
