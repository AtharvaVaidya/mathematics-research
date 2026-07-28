# A Petersen four-pole extension theorem for standard FiveCDC

Date: 2026-07-28

Status: exact local theorem and human-checkable certificate; **not** a
resolution of FiveCDC.

## Statement

Let \(G\) be a finite cubic graph with a standard five-cycle double cover.
Choose two vertex-disjoint edges \(e\) and \(f\).  Delete \(e\) and \(f\).
Take a fresh Petersen graph, delete two adjacent vertices, and join its four
degree-two boundary vertices bijectively to the four exposed endpoints of
\(e,f\).  Then the resulting cubic graph has a standard five-cycle double
cover, for every choice of the four-port bijection.

No assumption that the operation is a graph covering is used.

## Pair-label form of the local condition

Write the five Eulerian coordinates as \(0,1,2,3,4\), and label each edge by
the two coordinates containing it.  At a cubic vertex, the five parity
conditions say exactly that the XOR of its three weight-two labels is zero.
Equivalently, the three labels are the three pairs of some three-element
coordinate set.

Let the old labels of \(e,f\) be \(q,r\).  Keep all labels on the untouched
edges of \(G\), and label the four new joining edges \(q,q,r,r\), according
to which old endpoint they replace.  Parity at every old vertex is then
unchanged.  It remains only to label the ten internal edges of the Petersen
four-pole for an arbitrary placement of \(q,q,r,r\) on its four ports.

## A 13-row complete certificate

Use the graph6 Petersen labeling `ICOf@pSb?` and delete vertices \(0,3\),
which are adjacent.  The ordered ports are
\[
 (6,9,7,8),
\]
and the ordered internal edges are
\[
\begin{split}
 &(1,4),(1,6),(1,8),(2,5),(2,6),\\
 &(2,7),(4,7),(4,9),(5,8),(5,9).
\end{split}
\]

Under coordinate permutations, an ordered pair \((q,r)\) has only three
types: \(q=r\); distinct with \(|q\cap r|=1\); or disjoint.  Representatives
are \((01,01)\), \((01,02)\), and \((01,23)\).  The following table gives,
for every distinct placement of the corresponding \(q,q,r,r\) on the four
ordered ports, labels on the ten ordered internal edges.

| port labels | internal-edge labels |
|---|---|
| `01 01 01 01` | `01 02 12 01 12 02 12 02 02 12` |
| `01 01 02 02` | `01 02 12 02 12 01 12 02 01 12` |
| `01 02 01 02` | `02 03 23 34 13 14 04 24 03 04` |
| `01 02 02 01` | `34 03 04 01 13 03 23 24 14 04` |
| `02 01 01 02` | `34 03 04 02 23 03 13 14 24 04` |
| `02 01 02 01` | `01 03 13 34 23 24 04 14 03 04` |
| `02 02 01 01` | `02 01 12 01 12 02 12 01 02 12` |
| `01 01 23 23` | `01 02 12 01 12 02 03 13 13 03` |
| `01 23 01 23` | `01 02 12 01 12 02 12 02 13 03` |
| `01 23 23 01` | `01 02 12 01 12 02 03 13 02 12` |
| `23 01 01 23` | `01 02 12 01 03 13 03 13 13 03` |
| `23 01 23 01` | `01 02 12 01 03 13 12 02 02 12` |
| `23 23 01 01` | `01 02 12 01 03 13 03 13 02 12` |

Each entry has weight two.  At each of the eight internal vertices, the XOR
of the three incident entries is zero; this can be checked directly from the
displayed port and internal-edge orders.  Therefore every row satisfies all
five parity conditions.  Coordinate permutations preserve weight and XOR.
The three intersection types and all their distinct port placements exhaust
the possibilities, so every boundary tuple \(q,q,r,r\) extends.

Using the extension on the Petersen pole and the unchanged labels on \(G\)
gives weight two on every edge and even degree in every coordinate at every
vertex.  These five coordinate sets are the required five Eulerian
edge-subsets.  This proves the theorem.

## Machine audit and direct corpus

`scratch/verify_petersen_four_pole_extension_theorem_20260728.py` checks the
13 displayed rows and then exhausts all 100 ordered choices of \(q,r\), all
distinct placements of \(q,q,r,r\), and all 120 coordinate permutations.
It checks 550 labeled boundary assignments.

As a redundant whole-graph control, one deterministic Petersen dot product
was formed from each of the 7,654 retained order-40 strong snarks, followed
by two further substitution layers at orders 56 and 64.  All 22,962
non-covering outputs had direct SAT witnesses accepted by an independently
written graph/premise/FiveCDC checker.  The theorem, rather than this finite
census, explains the positive result.

## Search consequence and scope

A smallest cubic FiveCDC counterexample cannot be obtained from a smaller
FiveCDC-positive cubic graph by this Petersen four-pole substitution.
Therefore this commonly searched dot-product direction can be pruned unless
one changes the pole or the boundary operation.

The theorem is specific to the standard Eulerian-subgraph formulation.
Nothing here asserts orientability.  No claim of literature novelty is made
without a dedicated specialist comparison.
