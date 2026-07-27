# Marked circuits and fixed-five rooted interfaces in cubic graphs

This directory contains a narrowly scoped research preprint. It records:

1. an exact elliptic-quadratic reformulation of five-cycle double covers,
   with a human-checkable proof and explicit loop/parallel-edge conventions;
2. a human-checkable four-mark core closure theorem under a common-colour
   Tait-colouring hypothesis and the marked cyclic-cut inequality;
3. a human-checkable forbidden-root reduction to an independent cyclic
   four-edge cut, with a cyclically 5-edge-connected corollary;
4. a human-checkable cycle-translation obstruction and exact rooted
   factorization for one surviving exceptional three-pole interface;
5. a human-checkable base-pair/coordinate-cut certificate;
6. a human-checkable Tait-cap closure theorem: a nonbridge rooted shore
   with a Tait-colourable one-vertex cap contains a base pair, with the
   exact one-sided and two-sided exceptional consequences;
7. a two-solver rooted base-pair theorem through order 17 and a two-solver
   full-signature theorem for the cyclically 4-edge-connected order-22 cap
   slice; and
8. a corrected computer-assisted order-22 theorem restricted explicitly to
   Tait-colourable connected simple cubic graphs.

It does **not** claim a resolution of the Five-Cycle Double Cover Conjecture
or its orientable variant. The two-subset encoding is prior literature; the
quadratic packaging and new deductions have not undergone an exhaustive
priority search. All computed four-pole signatures use one fixed
five-coordinate \(D_5\) universe; they do not classify the published
unbounded-colour relation.

## AI disclosure

OpenAI Codex agents, directed by Atharva Vaidya, generated the initial
arguments, programs, audits, and manuscript. The paper gives full proofs for
human inspection and labels imported theorems and computations separately.
AI-agent review is not independent human verification or peer review.

The paper is potentially suitable as a focused research note only after
specialist priority review and independent human verification. Its claims
are structural reductions and a finite census, not a proof of the target
conjecture. See `NOVELTY-ASSESSMENT.md` for the blunt publication verdict.

## Build

From this directory:

```sh
tectonic main.tex --outdir output/pdf
```

The companion programs and frozen census metadata are in the project root:

```text
../scratch/tait_all_coloring_mark_separation.cpp
../scratch/verify_order22_separation_via_matchings.cpp
../scratch/order22-universal-four-separation-result.json
../search/rooted-three-pole-frontier-20260727/
../search/four-pole-order22-cap-20260727/
```

The completed claims use only the order-17 package and the cyclically-four
order-22 cap slice. The larger all-cap order-22 run is not claimed.

## Audit correction

The earlier project census note omitted "Tait-colourable" from its headline.
The programs intentionally skip graphs with no Tait colouring. Under a
literal universal quantifier, separation is vacuous on such a graph. The
preprint states the exact verified result and explains this correction in
the introduction.

A later hostile audit also corrected an overstrong one-sided inference from
base-pair containment. One Tait shore rules out equality-only and
disjointness-only relations, but the mixed equality/intersection relation can
survive. The paper gives the exact invariant-signature counterexample and
states the three-sum path consequence only with the 3-connectivity premise
required by the cited decomposition theorem. A dependent project-level claim
of a global order-28 lower bound was withdrawn; that claim is not made here.

Before public submission:

- obtain an independent human proof audit;
- reproduce every claimed finite census on an independently provisioned
  machine;
- archive the full source distribution and logs at a permanent URL/DOI;
- perform a broader specialist literature and priority search, especially
  for the elliptic \(O^-(4,2)\) packaging and rooted translation argument; and
- decide authorship and affiliation metadata under the target venue's policy.
