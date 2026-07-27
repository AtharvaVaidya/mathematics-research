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
7. a human-checkable root-end factor lift: endpoint base pairs become fork
   triples through an arbitrary cubic three-sum path, and two forks force
   both an intersecting and a disjoint cross-pair;
8. a two-solver endpoint base-pair theorem through factor order 26, complete
   cyclically 4-edge-connected cap classifications through order 26, and
   the resulting bridge-free simple terminal-distinct fixed-five
   exceptional-pole lower bound of order 28;
9. an explicit-witness classification of all 9,725,709 deletions from the
   retained cyclically 4-edge-connected order-28 caps, raising that scoped
   lower bound to order 30;
10. a complete all-cap order-22 exceptional-signature exclusion; and
11. a corrected computer-assisted order-22 theorem restricted explicitly to
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
../search/rooted-three-pole-nontait-endpoint-frontier-20260727/
../search/four-pole-order22-cap-20260727/
../search/four-pole-order24-cyclic4-cap-20260727/
../search/four-pole-order26-cyclic4-cap-20260727/
../search/four-pole-order28-cyclic4-cap-20260727/
../scratch/verify_boundary_two_orbit_witness_fast.cpp
```

The completed claims include the full order-22 all-cap run and the
cyclically-four order-24 and order-26 full-signature runs. At order 28,
two explicit boundary witnesses per deletion row suffice to exclude every
exceptional mask. Order 30 is not classified.

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
discharges the 3-connectivity premise required by the cited decomposition
theorem: a simple bridgeless cubic cap with no cyclic two-edge cut has no
one- or two-vertex cut.

A later hostile audit replaced the conditional triangle-contraction route
with a direct endpoint-factor lift. Fix one labelling of the rest of the
three-sum path. The three endpoint base-pair labellings are all transported
by the same inverse coordinate normalization and glue to that fixed
remainder, so the whole-shore signature contains a fork
\(\{qr,ps,pt\}\). Two forks always exhibit both unequal intersection and
disjointness. Combined with the completed endpoint theorem through factor
order 26 and cyclically-four cap classifications through order 26, this
soundly restores the scoped simple terminal-distinct lower bound 28.
The subsequent order-28 package supplies explicit orbit-0 and orbit-2
\(D_5\) labellings for all \(9\,725\,709\) deletion poles. Since those two
orbits jointly exclude all six exceptional masks, parity raises the scoped
lower bound to 30. It does not prove Five-CDC, and no stronger bound is
claimed.

Before public submission:

- obtain an independent human proof audit;
- reproduce every claimed finite census on an independently provisioned
  machine;
- archive the full source distribution and logs at a permanent URL/DOI;
- perform a broader specialist literature and priority search, especially
  for the elliptic \(O^-(4,2)\) packaging and rooted translation argument; and
- decide authorship and affiliation metadata under the target venue's policy.
