# Human proof of the 40-vertex one-switch countermodel

## Scope

This theorem refutes an intermediate proof strategy. It does **not**
refute the five-cycle double cover conjecture. In fact, the graph below
has an explicit three-cycle double cover, with two empty coordinates
appended to make a standard five-cycle double cover.

For a nowhere-zero \(\mathbb F_2^3\)-flow \(f\) on a cubic graph, write

\[
M_k(f)=\{e:f(e)=k\}\qquad (k=1,\ldots,7).
\]

Call \(k\) successful when
\((G-M_k(f),\partial M_k(f))\) has two edge-disjoint \(T\)-joins, and call
\(f\) good when some \(k\) is successful. An allowed one-circuit switch
adds a nonzero \(a\in\mathbb F_2^3\) to the values on one connected
circuit \(C\), with \(a\notin f(C)\). The latter condition keeps every
edge value nonzero.

The false statement is:

> Every nowhere-zero \(\mathbb F_2^3\)-flow on every connected
> bridgeless cubic graph is good or can be made good by one allowed
> connected-circuit switch.

## A ten-vertex base with three noncyclable monochromatic edges

Let \(H\) have the following edge table. Colors \(0,1,2\) receive flow
values \(1,2,3\), respectively; \(1\mathbin{\mathsf{xor}}2=3\).

| edge | endpoints | color | value |
|---:|:---:|---:|---:|
| 0 | 01 | 0 | 1 |
| 1 | 02 | 1 | 2 |
| 2 | 03 | 2 | 3 |
| 3 | 23 | 0 | 1 |
| 4 | 45 | 2 | 3 |
| 5 | 46 | 0 | 1 |
| 6 | 56 | 1 | 2 |
| 7 | 17 | 1 | 2 |
| 8 | 67 | 2 | 3 |
| 9 | 18 | 2 | 3 |
| 10 | 48 | 1 | 2 |
| 11 | 58 | 0 | 1 |
| 12 | 29 | 2 | 3 |
| 13 | 39 | 1 | 2 |
| 14 | 79 | 0 | 1 |

The graph6 record is `It?GYDKKO`. The table gives every vertex one edge
of each color. Hence \(H\) is cubic, the three values xor to zero at
every vertex, and the displayed values are a nowhere-zero flow. The
union of any two color classes is a disjoint union of circuits. Every
edge therefore lies on a circuit, so the connected graph \(H\) is
bridgeless.

Put

\[
P=\{1,6,7\}=\{02,56,17\}.
\]

All three edges have value \(2\), but no connected circuit contains all
three. Here is a direct proof.

Suppose a circuit \(C\) contains \(P\). Consider the triangle
\(\{0,2,3\}\). Since \(C\) also has edges outside this triangle, it
crosses its boundary in two edges. If it used both \(29\) and \(39\)
but not \(01\), the forced degrees at \(0,2,3,9\) would make the
four-cycle \(0\,2\,9\,3\,0\) the whole of \(C\), a contradiction.
Thus \(01\in C\).

Apply the same argument to the triangle \(\{4,5,6\}\). If \(C\) used
both \(48\) and \(58\) but not \(67\), its forced edges would make
\(8\,4\,6\,5\,8\) the whole circuit. Thus \(67\in C\), and exactly one
of \(48,58\) lies in \(C\).

At vertex \(7\), the already forced edges \(17\) and \(67\) exclude
\(79\). At vertex \(1\), the forced edges \(17\) and \(01\) exclude
\(18\). But vertex \(8\) is now incident with exactly one circuit edge:
exactly one of \(48,58\), while \(18\) is absent. This contradicts the
even degree of a circuit. Therefore \(P\) is noncyclable.

## The ten-vertex bad block

Let \(B\) be the graph and flow in
`../fano-value-class-flow-countermodel-20260726/instance.json`. It has
the following property:

> For every \(k=1,\ldots,7\), the graft
> \((B-M_k,\partial M_k)\) has no two edge-disjoint \(T\)-joins.

The edge-by-edge proof is in that package's `HUMAN-PROOF.md`. Its
independent checker literally enumerates the \(T\)-joins. There are 16
for each of \(k=1,2,3,4,5,7\), and 8 for \(k=6\); every pair intersects.

## Aligned two-sums

Delete edges \(xy\) and \(uv\) of the same flow value \(b\) from two
cubic flow graphs and add \(xu,yv\), both with value \(b\). This is an
aligned two-sum.

Each affected vertex loses and gains the same flow value, so cubicity
and flow conservation persist. The two connectors also show that the
sum of connected bridgeless summands is connected and bridgeless. Every
circuit uses zero or both connectors. If it uses both, replacing its
path through a summand by the deleted edge projects it to a circuit in
the graph before the two-sum.

The same operation preserves a five-cycle double cover. Label each edge
by the two cover coordinates containing it. Permute the five coordinates
of one summand so that the deleted edges have the same two-label, and
give both connectors that label. Exact-two coverage and every
vertex-coordinate parity equation are unchanged.

## One unchanged bad block obstructs all seven values

Attach \(B\) at a deleted edge \(xy\) of value \(b\). Suppose a later
flow change leaves the copy of \(B\) and its two connectors unchanged.
Then no global value \(k\) is successful.

Indeed, suppose \(J_1,J_2\) were edge-disjoint global
\(\partial M_k\)-joins.

If \(k=b\), the two connectors are deleted with \(M_k\). Restricting
each \(J_i\) to the isolated block gives two edge-disjoint local
\(\partial M_k(B)\)-joins, contradicting the bad-block property.

If \(k\ne b\), both connectors remain. Parity over all vertices on the
block shore shows that each \(J_i\) uses zero or two connectors. In the
two-connector case, delete the connectors from \(J_i\) and restore the
deleted port edge \(xy\); in the zero-connector case, just restrict
\(J_i\) to the block. Either operation produces a local
\(\partial M_k(B)\)-join. At most one of the two edge-disjoint global
joins can use both connectors, so at most one projected join uses
\(xy\). The two local joins remain edge-disjoint, again a contradiction.

## The 40-vertex construction

In \(H\), replace each of the three edges in \(P\) by an aligned
two-sum with a fresh copy of \(B\), using the value-2 edge 10 of \(B\)
as the port. Call the resulting graph and flow \(G,f\). The complete
record is `construction.json`.

The construction has

```text
vertices       40
edges          60
bad blocks      3
```

It is simple, connected, cubic, bridgeless, and \(f\) is nowhere zero.
The nauty-canonical graph6 record is frozen in `canonical.g6`. Standard
planarity checks report that the graph is planar; this is metadata about
the route countermodel, not a five-CDC obstruction.

Let \(C\) be any connected circuit of \(G\). If \(C\) lies wholly inside
one bad block, the other two bad blocks are untouched. Otherwise,
project every traversed block back to its replaced edge. The result is a
circuit of \(H\). Since no circuit of \(H\) contains all of \(P\), at
least one replaced edge is absent, and its whole bad block and both
connectors are disjoint from \(C\).

An allowed switch on \(C\) therefore leaves one bad block and both its
connectors unchanged. The preceding lemma says that all seven global
values remain unsuccessful. The original flow is bad for the same
reason. Consequently:

> **Theorem.** The explicit 40-vertex connected bridgeless cubic graph
> \(G\) has a nowhere-zero \(\mathbb F_2^3\)-flow \(f\) that is bad and
> remains bad after every allowed switch on one connected circuit.

## Explicit positive five-cycle double cover

On \(H\), label colors \(0,1,2\) by \(01,02,12\). On each copy of \(B\),
use its retained three-edge-coloring and permute coordinates to align
the deleted-edge label. Give the connectors the aligned label.

The resulting coordinate sizes are

```text
40 40 40 0 0
```

Thus the construction actually has a three-cycle double cover, with two
empty Eulerian subgraphs appended. It is not a counterexample to the
standard five-cycle double cover conjecture.

## Independent finite check

`independent_checker.py` does not import the producer. It:

1. decodes the graph6 base and reconstructs all three two-sums;
2. verifies simplicity, cubicity, connectedness, every one-edge
   deletion, and every flow equation;
3. enumerates all 30 circuits of \(H\) and confirms none contains \(P\);
4. enumerates all bad-block \(T\)-joins for all seven values;
5. enumerates all 6,780 circuits of \(G\) and confirms that every one
   misses an entire bad block; and
6. checks every exact-two label and every cover parity equation.

When nauty `labelg` is installed, it also checks `canonical.g6`.

The frozen result is `independent-check.json`.

## AI-use disclosure

OpenAI Codex agents proposed and refuted the intermediate domination
claim, found both finite ingredients, discovered the smaller composition,
wrote the producer and independent checker, and drafted this proof under
the user's direction. A separate Codex agent was instructed to attack
the earlier, larger proof as a hostile referee. This is substantive AI
assistance and is not independent human peer review. A human author must
check the incidence table, the triangle argument, the two-sum lemmas,
the bad-block enumeration, the code, and all attribution before
publication.
