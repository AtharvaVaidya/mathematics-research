# Simultaneous triangle lifts and the surviving Jaeger plateau problem

Date: 2026-07-28

Status: **HUMAN EXCHANGE-GRAPH REDUCTION / EXACT FINITE STRICT-TRAP
SEARCHES / EXPLORATORY PLATEAU SEARCHES / NO UNIVERSAL PROOF OR
COUNTERMODEL.**

## 1. Exact product theorem for several triangles

Let \(G^S\) be obtained from a loopless cubic graph \(G\) by expanding
each vertex in a set \(S\), disjoint from the fixed star root \(r\), to
a triangle.  The vertices of \(S\) are vertices of the original graph;
in particular, adjacent vertices may both be expanded.  Write
\(\mathcal X(G,r)\) for the reciprocal two-tree exchange graph of one
fixed vertex-star fibre.

> **Proposition.**
> \[
> \mathcal X(G^S,r)\cong
> \mathcal X(G,r)\mathbin{\square}
> \operatorname{Cay}(S_3,\mathcal T)^{\square |S|},
> \]
> where \(\mathcal T\) is the set of three transpositions.

For each new triangle, all three of its edges have multiplicity two.
The three trees therefore omit three distinct triangle edges, one per
tree.  Contracting all new triangles gives a state of
\(\mathcal X(G,r)\), while the bijection assigning omitted triangle
edges to the three trees gives one \(S_3\) coordinate per triangle.
Conversely these data lift uniquely, proving the vertex-set statement.

It remains to classify a reciprocal swap.

1. Two external omitted edges give exactly the corresponding legal swap
   after contraction.
2. Two omitted edges in the same new triangle give one of the three
   transpositions and are always legal.
3. One triangle edge and one external edge are illegal: one changed
   tree contains all three edges of that triangle and hence a cycle.
4. Edges from two different new triangles are also illegal: each
   changed tree gains the omitted edge at one triangle and contains
   that complete triangle as a cycle.  Losing an edge at a different
   triangle cannot remove this cycle.

These are precisely the Cartesian-product adjacencies.  This extends
the one-triangle product statement in
`jaeger-triangle-expansion-descent-structure.md`.

The defect score is **not** a product potential.  Although contraction
preserves external odd-kernel membership, different \(S_3\) sheets can
have different seven-plane profiles.  The proposition therefore does
not establish descent invariance.

## 2. Exact strict-trap search

The program

```text
scratch/search_jaeger_lifted_immediate_traps.py
```

constructs every simultaneous lift of a literal contracted state and
recomputes the exact seven-plane component defect.  For a lifted state
it checks the complete product neighbourhood: every legal contracted
exchange and all \(3|S|\) triangle transpositions.  Thus a reported
`STRICT_TRAP` would be an exact countermodel to the full same-level
component theorem.  A clean search is only a finite negative result.

For the frozen order-16 immediate-descent countermodel

```text
graph6  O??CA?_ceOGgH_F?AK@P?
root    13
omitted (857601,1059160,180390)
```

the contracted state has profile \((4,4,4,2,4,6,4)\), no lower
neighbour, 18 equal neighbours, and 5 higher neighbours.  Exhaustive
simultaneous-lift searches give:

| expanded vertices | lifted states | minimum equal neighbours among states with no lower neighbour |
|---:|---:|---:|
| 0 | 1 | 18 |
| 1 | \(15\cdot6=90\) | 16 |
| 2 | \(\binom{15}{2}6^2=3,780\) | 14 |

A targeted exact three-triangle search over all 2,808 lifts whose
expanded set contains vertices 0 and 7 has minimum 12.  No strict trap
occurs in these searches.

A second literal order-16 state, found by the broad local sampler, is

```text
graph6  Ot?GO?@?_G?T@IOSAIBO?
root    0
spokes  (2,1,0)
omitted (1720610,271049,105492)
profile (4,4,6,4,2,4,6)
```

It has 21 legal contracted neighbours: 12 equal and 9 higher, with no
lower neighbour.  Exhaustive searches give minimum equal-neighbour
counts 10 over all 90 one-triangle lifts and 7 over all 3,780
two-triangle lifts.  Greedy exact extensions found counts 6 with three
triangles and 5 with four, but those last two values are not exhaustive
optima.  Again no strict trap was found.

For example, reproduce the exhaustive two-triangle search for the
second state with

```sh
python3 scratch/search_jaeger_lifted_immediate_traps.py \
  --triangles 2 \
  --graph6 'Ot?GO?@?_G?T@IOSAIBO?' \
  --root 0 --spokes 2,1,0 \
  --omitted 1720610,271049,105492
```

## 3. Broad full-plateau sampling

The local sampler was strengthened to record the smallest neutral
degree observed as well as replaying the complete same-level component
from each sampled boundary-free state, up to its explicit
100,000-state replay limit.

For all 2,828 simple 3-edge-connected cubic graphs of order 16 at root
zero, 300 walk steps per graph produced:

```text
distinct sampled states       768,639
positive sampled states       649,156
exact plateau replays          16,699
largest replay before escape      293
largest escape distance              3
smallest observed neutral degree     12
full plateau traps                    0
```

This is randomized state sampling over a complete graph list, not an
exhaustive state theorem.

On the 36-vertex strict APX countermodel

```text
chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH
```

all 36 roots with 1,500 steps per root produced 51,029 distinct states
and 1,297 exact plateau replays.  Every replay escaped within distance
three; the largest replay explored 2,876 same-level states, and the
smallest observed neutral degree was 13.  A separate 10,000-step root-0
run also found no trap.

A further root-0 stress set contained 211 canonically distinct graphs
obtained from this host by one, two, or three randomly selected triangle
expansions.  At 1,000 walk steps per graph it sampled 199,322 distinct
states and replayed 3,146 plateaux.  Every replay escaped; the largest
explored 10,943 same-level states and the largest escape distance was
four.  This is again a randomized stress experiment, not a census of
all expansions or all fibre states.

These computations materially stress the surviving theorem but do not
prove it.  In particular, neither graph sampling nor a replay that
finds a lower boundary certifies unvisited states elsewhere in the
fibre.

## 4. Current conclusion

Generic matroid basis-partition connectivity only connects the fibre;
it supplies no discrete convexity of the minimum seven-plane defect.
Immediate descent and fixed-kernel exposure are already false.  The
experiments here show that even deliberately adversarial hosts and
triangle-product amplifications continue to have short plateau escapes,
but no human argument presently forces such an escape.

Therefore the full positive-level component-boundary theorem remains
open.  It must not be cited as a proof of FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the simultaneous
triangle product argument, implemented the exact lift and neighbourhood
enumerator, selected adversarial states and hosts, ran the searches,
and drafted this note.  The theorem proof is written above; every
finite count is reproducible from the disclosed literal inputs and
program.  No claim of a FiveCDC resolution is made.
