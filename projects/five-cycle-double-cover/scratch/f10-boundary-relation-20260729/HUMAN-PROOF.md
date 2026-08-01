# The full F10 six-port relation and its network consequence

## 1. Duad form of the FiveCDC condition

Write
\[
 D_5=\binom{\{0,1,2,3,4\}}2.
\]
A label in \(D_5\) is represented by its five-bit characteristic vector.
For a graph edge \(e\), the label \(\lambda(e)\) records the two members of
the proposed five even edge sets which contain \(e\).

At a vertex \(v\), the five parity conditions are the single vector
equation
\[
 \bigoplus_{e\ni v}\lambda(e)=0.                 \tag{1}
\]
Every label has Hamming weight two, so every edge is in exactly two sets.
The \(i\)-th coordinate of (1) says that the edges whose labels contain
\(i\) have even degree at \(v\).  Thus a \(D_5\)-labeling satisfying (1) is
equivalent to five Eulerian edge subsets which cover every edge twice.
Disconnected and empty Eulerian subsets are allowed.

The F10 pole in this package has 288 vertices, 429 internal edges, and two
ordered three-port connectors
\[
 (0,2,3),\qquad (13,15,16).
\]
The six semiedges are placed after the 429 internal edges in every witness.

## 2. Exact boundary relation

Let \(b_0,\ldots,b_5\in D_5\) be the six port labels.  Summing (1) over all
288 pole vertices cancels every internal label twice.  Therefore every
extension necessarily satisfies
\[
 b_0\oplus b_1\oplus\cdots\oplus b_5=0.          \tag{2}
\]

The converse is the finite certificate in `boundary-witnesses.jsonl`.
There are

- \(10^6\) ordered six-duad words;
- 62,560 words satisfying (2);
- 571 orbits of those words under simultaneous permutation of the five
  coordinates.

`s5-representatives.json` contains one word from every one of the 571
orbits.  The corresponding row of `boundary-witnesses.jsonl` contains 435
duad labels: 429 internal labels followed by the six boundary labels.
For every row, each label has weight two and the XOR of the three labels at
each pole vertex is zero.

Permuting the five coordinates of a witness gives a witness for the entire
coordinate orbit.  The 571 certified orbits cover all 62,560 words
satisfying (2).  Hence the exact relation is
\[
 R_{\mathrm{F10}}
   =\{(b_0,\ldots,b_5)\in D_5^6:
       b_0\oplus\cdots\oplus b_5=0\}.            \tag{3}
\]

No negative SAT result is used.  Every orbit is positive and is certified
by an explicit labeling.  The independent standard-library checker
reconstructs the 62,560-word universe and checks all 571 labelings directly.

Although the underlying pole need not have every port permutation as a
graph automorphism, (3) has full \(S_6\) symmetry on the ports.  This is an
emergent symmetry of the boundary relation.  Quotienting (3) by
\(S_5\times S_6\) leaves 11 orbits; their representatives are frozen in
`relation-summary.json`.

## 3. Universal trivalent-junction theorem

Consider any finite network made from copies of the F10 pole.  Attach every
port to exactly one new trivalent junction, and attach three port half-edges
to every junction.  A junction may receive two or three ports from the same
F10 copy, and it may receive repeated macro-incidences from the same one of
that copy's two connectors.

Form the incidence multigraph \(H\):

- its left vertices are the two connector triples of every F10 copy;
- its right vertices are the trivalent junctions;
- every pole-to-junction edge is an edge of \(H\), retaining multiplicity.

Every left vertex has degree three because a connector contains three
distinct port half-edges and every port is attached once.  Every right
vertex has degree three by the junction definition.  If a junction receives
several ports from the same connector, \(H\) has parallel edges; those
parallel edges are distinct port incidences and still count separately
toward degree three.  There are no incidence loops because the two parts of
\(H\) are disjoint.  Thus \(H\) is a cubic bipartite multigraph.

Every cubic bipartite multigraph is 3-edge-colourable.  For completeness,
if \(S\) is a set of vertices on one side, its \(3|S|\) incident edges end
in \(N(S)\), which can receive at most \(3|N(S)|\) of them.  Hence Hall's
condition holds and \(H\) has a perfect matching.  Removing it leaves a
2-regular bipartite multigraph, whose even cycles split into two perfect
matchings.  This proof permits parallel edges.  Colour the three matchings
with colours \(a,b,c\).

Use the three triangle duads
\[
 q_a=01,\qquad q_b=02,\qquad q_c=12.
\]
They satisfy \(q_a\oplus q_b\oplus q_c=0\).  Give each network edge the
duad corresponding to its edge colour.  At every junction the three colours
occur once, so (1) holds there.  At each connector vertex of \(H\), the
three colours occur once.  Therefore the two connector triples belonging
to one F10 copy together contain each of \(q_a,q_b,q_c\) exactly twice, and
their six labels have XOR zero.  Equation (3) extends this boundary word
through that F10 copy.

Choosing an extension independently for every copy labels every edge of the
expanded graph by a duad and satisfies (1) at every vertex.  By Section 1
this is a FiveCDC.

> **Theorem.** Every finite graph obtained by attaching all ports of any
> number of copies of the retained F10 six-pole to trivalent junctions has
> five Eulerian edge subsets covering every edge exactly twice.

The theorem does not require the expanded graph to be simple, connected,
bridgeless, or high-girth.  Those restrictions matter when constructing a
candidate counterexample, but the positive labeling works without them.

## 4. Logical scope

This eliminates the entire F10/trivalent-junction construction family from
the counterexample search.  It is not a proof of the Five-Cycle Double
Cover Conjecture for arbitrary bridgeless graphs, and it is not an UNSAT or
counterexample claim.  Novelty relative to the literature has not been
established.
