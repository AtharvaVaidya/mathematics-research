# Whole-fibre square implication at order 16

Date: 2026-07-28

Status: **COMPLETE CANONICAL POSITIVE CERTIFICATE CENSUS / FINITE
THEOREM ONLY / NO UNIVERSAL PROOF / NOT A RESOLUTION OF FIVE-CDC**.

## Statement checked

Let \(H\) be a simple 3-edge-connected cubic graph, let \(r\) be a
vertex, and let \(e,f\) be independent edges not incident with \(r\).
A star packing at \(r\) is a triple of spanning trees in which every
root edge occurs once and every other edge occurs twice.  It is
**exact-good** when the odd-kernel component-parity criterion holds in
at least one coordinate.

Replace \(e=AC\) and \(f=BD\) by
\[
 Aa,\ Bb,\ Cc,\ Dd,\ ab,\ bc,\ cd,\ da .
\]
A square-local lift keeps every tree membership outside these eight
gadget edges fixed.

The checked assertion is

> **(L16)** For every \(H,r,e,f\) as above with
> \(|V(H)|=16\), some exact-good star packing downstairs has an
> exact-good square-local lift.

This allows the selected downstairs packing to depend on \(e,f\).  It
does not assert that every exact-good packing lifts; that statewise
assertion is already false at order eight.

## Canonical scope

The exact input is

```sh
geng -cq -d3 -D3 16
```

It contains 4,060 pairwise nonisomorphic connected simple cubic graph6
records and has SHA-256

```text
b3610f3eab739083ece9fc9c5d896708de5345b8b22104e13425bfcb88b9df5e
```

Deleting every set of zero, one, or two edges independently retains
exactly 2,828 three-edge-connected graphs.  For each retained graph all
16 labelled roots are checked.  Each root has 21 nonroot edges and
\[
 \binom{21}{2}
 -3\binom{2}{2}
 -12\binom{3}{2}=171
\]
eligible independent nonroot pairs.  The corpus therefore contains
exactly
\[
 2,828\cdot16\cdot171=7,737,408
\]
witness rows.

The graph stream is split into the following disjoint half-open
graph-index ranges:

```text
[0,254)       [254,508)     [508,762)     [762,1016)
[1016,1270)   [1270,1524)   [1524,1778)   [1778,2032)
[2032,2286)   [2286,2540)   [2540,2794)   [2794,3048)
[3048,3302)   [3302,3556)   [3556,3810)   [3810,4060)
```

Their union is the complete canonical input, and they are pairwise
disjoint.

## Discovery and certificates

The discovery program is

```text
scratch/search_jaeger_star_square_existential_order16.cpp
```

For each root it sorts the three root spokes and requires tree \(i\) to
contain spoke \(i\).  This is a sound quotient by coordinate \(S_3\):
every ordered star packing has exactly one coordinate permutation in
that normalization, and exact-goodness and square-local liftability are
coordinate invariant.

The program enumerates every normalized star packing.  It reconstructs
each spanning tree, its odd kernel from odd subtree sizes, and its exact
component-parity profile.  For every still-unresolved edge pair and
exact-good state it enumerates the \(2^8\) local edge masks for each
tree, joins the three local omission masks to enforce multiplicity two,
and emits a row only after finding an exact-good lifted triple.

Summed over the 16 shards, discovery reports:

```text
canonical records          4,060
3-edge-connected records   2,828
labelled roots             45,248
witness rows               7,737,408
star states inspected      12,033,989
exact-good states seen        645,729
local-lift attempts        12,723,608
failed instances                    0
```

The state and attempt counts are early-stopping work totals, not
full-fibre cardinalities.  The uncompressed concatenated witness stream,
in increasing shard-index order, has SHA-256

```text
09b57424dd52b0b08072511136d833894ad6dc8b72f3f13030fe896a00990adb
```

Every `W` row contains the canonical graph index and graph6 record, the
root, the edge pair, three downstairs tree masks, and three lifted tree
masks.  Thus every positive answer has an explicit certificate; no
solver model or uncheckable success flag is used.

## Independent checker

The checker

```text
scratch/verify_jaeger_star_square_existential_order16.py
```

uses only the Python standard library and neither imports nor invokes the
C++ discovery code.  It:

1. regenerates the canonical `geng` stream and checks its frozen digest;
2. decodes graph6 independently;
3. deletes every set of at most two edges to identify the 2,828 retained
   graphs;
4. requires exactly one row for every retained graph, every root, and
   every eligible pair in the selected shard;
5. independently checks all six spanning trees and all edge
   multiplicities;
6. checks equality of downstairs and lifted memberships on every old
   outside edge; and
7. reconstructs every odd kernel and both component-parity profiles from
   first principles.

The checker supports a half-open `--start/--end` range, so the 16
certificate shards can be checked independently and in parallel.  With
no range arguments it checks their concatenation as one corpus.
All 16 independent shard replays passed.  Their disjoint-range sum uses
309,472 distinct downstairs states.

## Finite theorem and logical boundary

> **Finite theorem.** Every simple 3-edge-connected cubic graph on at
> most 16 vertices, every root, and every eligible independent nonroot
> edge pair satisfies the whole-fibre local-selection implication (L).

The order-16 claim is exactly (L16), certified above.  The lower even
orders were independently certified in the preceding order-8,
order-10, order-12, and order-14 censuses.  Relabelling transports a
certificate from the canonical representative to every graph in its
isomorphism class.

Consequently, any countermodel to (L) in the simple
3-edge-connected cubic class has downstairs order at least 18.  This is
not a proof of (L) for arbitrary order.  Failure of (L), if found, would
only refute this square-local proof route; it would not be a
counterexample to FiveCDC.  Conversely, this finite positive census does
not resolve FiveCDC.

## AI-use disclosure

OpenAI Codex, under human direction, adapted the exact search, produced
the witness corpus, wrote the independent checker, and prepared this
note.  The source, complete positive certificates, frozen hashes, and
human-readable scope are supplied for replay.  No claim of independent
peer review or universal resolution is made.
