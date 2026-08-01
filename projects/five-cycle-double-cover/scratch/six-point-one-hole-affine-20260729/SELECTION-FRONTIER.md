# Selection frontier for the six-point one-hole lift

Date: **2026-07-29**

Status: **EXACT FINITE EVIDENCE / FIXED-FLOW SEPARATIONS / UNIVERSAL
SELECTION OPEN**.

The graph-level statement “some Fano flow has a soluble six-point
one-hole system” is equivalent to FiveCDC.  This note records what the
new affine normal form changes at the two meaningful intermediate
quantifier levels: a fixed flow, and a fixed Jaeger three-tree
multiplicity fibre.

## Complete all-flow census on the rigid 12-vertex graph

For graph6

```text
K??FEaKR@oE_
```

the retained all-flow report has 900
\(\mathrm{GL}(3,2)\)-orbits, representing 150,192 labelled nowhere-zero
flows.  Translation of the eight coordinate points reduces the 56
five-sets to seven representatives and the 420 disjoint
\((R,M)\)-choices to 63 representatives.

Two newly written exact implementations independently obtain:

| fixed-flow class | flow orbits | labelled flows |
|---|---:|---:|
| five-point soluble | 566 | 94,080 |
| five-point insoluble, six-hole soluble | 252 | 42,336 |
| six-hole insoluble, but generally five-colourable Oum potential exists | 18 | 3,024 |
| no five-colourable Oum potential | 64 | 10,752 |

Thus the six-hole affine form rescues 252 of 334 flow orbits that fail
all five-point restrictions.  It is a substantial strict extension at
fixed flow, but it is not the most general five-colourable Oum
compression: 18 successful flow orbits require a packing using more
than six coordinate points.  The 64 fully obstructed fixed flows remain
obstructed.

The literal unique-potential spanning-tree flow

```text
1 2 3 4 7 3 5 3 6 5 7 2 5 1 4 6 2 4
```

is among the 64.  Its unique gauged potential uses every edge of a
coordinate \(K_6\), so every global translate still has all 15 pairs on
six points.  It has zero five-point and zero six-hole choices.  This is
a fixed-flow obstruction only.

Reproduction:

```sh
python3 scratch/six-point-one-hole-affine-20260729/audit_all_flows_12v.py
node scratch/six-point-one-hole-affine-20260729/verify_all_flows_12v.mjs
```

## Jaeger fixed-fibre selection

The same rigid flow comes from three spanning-tree fundamental
completions.  Its edge-multiplicity vector has one zero edge (edge 10),
one multiplicity-one edge (edge 15), and multiplicity two everywhere
else: it belongs to a Type-B fibre.

The already frozen complete fixed-fibre census through order 14 proves
that **every** one of the 804,204 feasible Type-A/Type-B fibres has a
five-point representative.  In particular, the rigid Type-B fibre has
a different three-tree choice whose flow passes the stronger
five-point criterion.  Hence tree selection repairs the rigid fixed
flow without leaving its multiplicity fibre.

The exact retained finite frontier is:

| corpus | fixed fibres | five-point witnesses | implication |
|---|---:|---:|---|
| all 587 simple bridgeless cubic graphs through order 14 | 804,204 feasible Type-A/B fibres | 804,204 | all are six-hole soluble |
| 705 retained order-38 strong snarks | 26,790 vertex-star fibres | 26,790 | all are six-hole soluble |
| 31 retained order-44 oddness-four snarks | 1,364 vertex-star fibres | 1,364 independently replayed | all are six-hole soluble |

For the order-44 corpus the independent standard-library verifier
reconstructs every literal tree triple, fundamental completion, flow,
and five-point pair labelling.  The order-38 result has producer-side
semantic checking but no separate full witness replay in the retained
package, so its evidentiary status is weaker and is stated separately.

The 34-vertex strict flow in `HUMAN-PROOF.md` belongs to a canonical
vertex-star fibre and gives a different phenomenon: that **particular**
tree packing has no five-point lift but has eight skew six-hole lifts.
The local compression target is therefore genuinely broader even inside
the Jaeger star domain.

Relevant retained hashes:

```text
482e2ee028aa1663f2b91b71569422ab59c1033d51601ca52fac581b173872f1  output/jaeger-five-point-fibres-through14/census.jsonl
9bfa6ba83f22a6b2013699a817662ce3e6d57734f86d332c23463bfa8b02cfd6  output/jaeger-six-point-fibres-through14/census.jsonl
9322f3dfa82d42966873cbb49f93dd328bfd1d57d61853a84db0ac21e2604d96  scratch/jaeger-coordinate-five-star-order38-result.json
3ff25437d5e32fff7c60ceca695a6476d6c7d2404c1e8551bf14987f228cd4b4  output/jaeger-coordinate-five-order44/witnesses.jsonl
41c50f3413262cfb6a382424674edc2e226325f8b444af0f079ad89f5bc8924a  output/oum-combined-choice-12v/all-flow-orbits.json
```

Independent retained replays run with:

```sh
python3 scratch/verify_jaeger_five_point_frontier.py
python3 scratch/verify_jaeger_six_point_frontier.py
python3 scratch/verify_jaeger_coordinate_five_order44.py \
  --input search/known_snarks/source/snarks_44.04.oddness4.cyc4.g6 \
  --witnesses output/jaeger-coordinate-five-order44/witnesses.jsonl
```

## Remaining falsifiable lemma

The useful new selection target is:

> In a canonical Jaeger vertex-star fibre of every 3-edge-connected
> cubic graph, some three-tree packing, some disjoint omitted pair
> \(R\), and some merge pair \(M\) make the affine system soluble.

This statement would imply FiveCDC, but it is still stronger than the
bare graph-level conjecture because it fixes the Jaeger star fibre.  It
is not proved by the finite data above.

For a proposed countermodel to this selection lemma, each fixed
\((f,R,M)\) failure has an exact left-kernel certificate
\(y^{\mathsf T}A=0,\ y^{\mathsf T}b=1\).  A fibre-level UNSAT
certificate would have to combine the tree/base constraints with all
of those affine choices; no such fibre has been found in the retained
frontier.

## AI-use disclosure

OpenAI Codex agents, under human direction, performed the new all-flow
classification, wrote its two implementations, interpreted the retained
fixed-fibre results, and drafted this note.  The prior fixed-fibre
producers and verifiers were also AI-assisted.  No human peer review or
FiveCDC resolution is claimed.
