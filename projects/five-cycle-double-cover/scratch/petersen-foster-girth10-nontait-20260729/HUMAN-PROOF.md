# Human-checkable proof

Let \(F\) be the Foster graph on 90 vertices, represented by the LCF string
\([17,-9,37,-37,9,-17]^{15}\).  Let \(P=F-0\), retaining the three dangling
incidences at the former neighbours \(1,17,89\) as the ports of a three-pole.
Take ten copies of \(P\), one for each vertex of the Petersen graph, and join
their ports according to the Petersen edges.  Call the resulting graph \(G\).

## Basic graph properties

Every internal vertex of a copy of \(P\) retains degree three, except its three
port vertices, which have internal degree two and receive one new external
edge.  Hence \(G\) is cubic.  It has \(10(90-1)=890\) vertices and therefore
\(3\cdot890/2=1335\) edges.  The explicit construction has neither loops nor
parallel edges.

The independent verifier performs Tarjan bridge searches on \(G\), and again
after deleting each of its 1,335 edges.  Thus it proves that there is no
one-edge or two-edge cut.  The three external edges incident with any one pole
form an edge cut.  Both shores contain cycles, so the ordinary and cyclic edge
connectivities are both exactly three.

The Foster graph has girth 10.  In \(F-0\), any path between two distinct ports
has length at least 8: adding the two edges from its endpoints to vertex 0
would otherwise make a cycle of length less than 10 in \(F\).  A cycle of
\(G\) that uses external edges projects to a closed trail in the Petersen
graph.  Such a trail contains a Petersen cycle and hence uses at least five
external edges.  Between consecutive external edges it uses a path between
distinct ports, so its length is at least \(5(8+1)=45\).  An internal cycle
has length at least 10.  Finally,

```text
0,81,80,79,78,77,4,3,2,1,0
```

is a 10-cycle in the first pole.  Therefore \(G\) has girth exactly 10.

## Why \(G\) has no Tait colouring

We use the parity lemma for cubic multipoles.  Fix one colour in a proper
three-edge-colouring of an odd-order three-pole.  Counting incidences of that
colour at its internal vertices gives

\[
  |V(P)| = 2\,(\text{internal edges of the colour})
           +(\text{boundary edges of the colour}).
\]

Here \(|V(P)|=89\), so the number of boundary edges of each colour is odd.
There are only three boundary edges total.  Consequently the three boundary
edges have the three distinct colours.

Apply this to every copy of \(P\).  Contracting each pole to one vertex would
turn any Tait colouring of \(G\) into a Tait colouring of the Petersen graph.
But the Petersen graph has no such colouring.  One elementary verification is
as follows.  A colour class in a Tait colouring is a perfect matching, and the
other two colours form alternating even cycles.  The Petersen graph has six
perfect matchings; for each one, its complement is two disjoint 5-cycles.
The verifier enumerates all six matchings and checks this last statement
directly.  Hence \(G\) is not Tait-colourable.

## Why the attached labels are a FiveCDC

Order the edges as in graph6: for \(v=1,\ldots,889\), list pairs
\((u,v)\) for \(u=0,\ldots,v-1\).  The corresponding integer in
`fivecdc-labels.txt` is a five-bit mask.

The verifier checks:

1. every mask has exactly two set bits, so every edge belongs to exactly two
   of the five edge-subsets; and
2. at each vertex the XOR of the three incident masks is zero, so every one of
   the five edge-subsets has even degree at every vertex.

An edge-subset of a finite graph is Eulerian in the cycle-space sense exactly
when every vertex has even degree in it.  Thus the five bit coordinates are
five Eulerian edge-subsets and cover every edge exactly twice.

This is a positive certificate.  It proves that \(G\) is not a FiveCDC
counterexample.
