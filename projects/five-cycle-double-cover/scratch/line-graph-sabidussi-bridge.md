# The exact line-graph bridge to Sabidussi, and where it stops

Date: 2026-07-28

## Scope

This note works with a finite **simple cubic** graph \(G\).  It does not
silently extend the construction to loops.  Parallel edges can be treated by
an incidence line multigraph, but that convention is not needed below and is
not claimed here.

Write

\[
 D_k=\{\mathbf 1_{\{i,j\}}:0\le i<j<k\}\subseteq \mathbb F_2^k .
\]

A \(D_k\)-flow is a map \(q:E(G)\to D_k\) whose three values at every
vertex have xor zero.  For \(k=5\), its five coordinates are exactly five
even edge-subsets in which every edge occurs twice.

Let \(H=L(G)\).  Every \(v\in V(G)\) gives a triangle \(T_v\) of \(H\).
If \(e=uv\in E(G)=V(H)\), the four half-edges of \(H\) at \(e\) are paired
in two prescribed transitions: the two belonging to \(T_u\), and the two
belonging to \(T_v\).

## Exact equivalence

**Proposition.**  The following data are naturally equivalent.

1. A \(D_k\)-flow \(q\) on \(G\).
2. An edge-colouring \(\chi:E(H)\to\{0,\ldots,k-1\}\) such that:
   - every colour class has even degree at every vertex of \(H\); and
   - the two edges in each of the two prescribed triangle transitions at
     every vertex of \(H\) have different colours.

Unused colours are allowed.

**Proof.**  At a cubic vertex \(v\), the three weight-two vectors have xor
zero.  Thus each coordinate occurs an even number of times among their six
coordinate incidences.  The three two-subsets are consequently

\[
 \{a,b\},\quad \{b,c\},\quad \{c,a\}
\]

for three distinct coordinates \(a,b,c\).  Colour an edge \(ef\) of the
triangle \(T_v\) by the unique coordinate in \(q(e)\cap q(f)\).

Now fix \(e=uv\).  The two triangle edges at \(e\) in \(T_u\) receive the
two distinct coordinates of \(q(e)\), and the same is true in \(T_v\).
Hence each of those two prescribed transitions is bichromatic.  Across all
four incident edges of \(H\), each coordinate of \(q(e)\) occurs twice and
every other coordinate occurs zero times.  Every colour class is therefore
even at \(e\).

Conversely, fix a vertex \(e\) of \(H\).  Evenness says that every colour
has even multiplicity among its four incident half-edges.  A prescribed
transition is bichromatic, so all four cannot have one colour.  There are
therefore exactly two colours, each occurring twice.  Define \(q(e)\) to be
that two-subset.  On a triangle \(T_v\), the two triangle edges incident
with each vertex have different colours.  Thus the three edges of \(T_v\)
have three distinct colours \(a,b,c\).  The reconstructed labels at its
vertices are \(\{a,b\},\{b,c\},\{c,a\}\), whose xor is zero.  The two
constructions are inverse. \(\square\)

For \(k=5\), this proposition is not a reduction to an already solved
colouring theorem: it is exactly the Five-Cycle Double Cover problem on
cubic graphs, restated on their line graphs.

## What Ulyanov's theorem supplies

Ulyanov's Theorem 1.1 (arXiv:2607.13225v1) starts with **one Euler tour**
of an Eulerian graph.  It four-colours the edges so that every colour class
is even and every transition induced by that tour is bichromatic.

The prescribed transitions above instead form the circuit partition
\(\{T_v:v\in V(G)\}\) into triangles.  One can change transitions at some
vertices of \(H\) to merge these triangles into one Euler tour and apply
Ulyanov.  The unchanged vertices are then safe.  At a changed vertex there
are three pairings of its four half-edges:

- the original triangle pairing \(P\);
- the selected Euler-tour pairing \(Q\); and
- the third pairing.

Ulyanov avoids \(Q\), not \(P\).  Evenness forces the local colour multiset
to be either \(a,a,a,a\) or \(a,a,b,b\); avoiding \(Q\) excludes the first
case, but the monochromatic pairing in the second case may still be \(P\).
Thus the tour merge loses exactly the transition condition needed by the
line-graph proposition.

This is a genuine obstruction to a four-colour extension.  A \(D_4\)-flow
on a cubic graph is equivalent to a Tait colouring: quotient the six
weight-two labels into the three complementary pairs

\[
 \{01,23\},\qquad \{02,13\},\qquad \{03,12\}.
\]

At a vertex, the three quotient values are the three distinct nonzero
elements of \(\mathbb F_2^2\), so they form a proper three-edge-colouring.
Conversely, the three labels \(01,02,12\) turn any Tait colouring into a
\(D_4\)-flow.

The Petersen graph is not Tait-colourable.  Indeed, deleting any colour
class of a Tait colouring leaves a union of even cycles.  Every perfect
matching complement in the Petersen graph is instead two 5-cycles.  Hence
the triangle transition system of \(L(\mathrm{Petersen})\) has no compatible
even four-colouring, although Ulyanov supplies one for the transitions of
every chosen Euler tour.  Consequently at least one changed vertex must
retain a bad original triangle transition.

For a completely hand-checkable version of the finite Petersen assertion,
number its edges in the order used by the checker:

\[
\begin{array}{c|ccccccccccccccc}
i&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14\\ \hline
e_i&
01&12&23&34&04&05&16&27&38&49&57&79&69&68&58 .
\end{array}
\]

Its six perfect matchings are

\[
\begin{split}
&\{0,2,9,10,13\},\quad \{0,3,7,12,14\},\\
&\{1,4,8,10,12\},\quad \{2,4,6,11,14\},\\
&\{1,3,5,11,13\},\quad \{5,6,7,8,9\}.
\end{split}
\]

Direct deletion leaves two 5-cycles in each case.  The usual forced-edge
enumeration starting at vertex \(0\) shows that this list is exhaustive:
choose its matching edge, then repeatedly choose the only still available
edge whenever a vertex has two already matched neighbours.  This is also
replayed without graph libraries by the checker.

## A fifth colour cannot be added by pure recolouring

There is also a local no-go for the most direct repair.

Suppose the original pairing is

\[
 P=\{\{0,1\},\{2,3\}\}
\]

and the Euler-tour pairing is

\[
 Q=\{\{0,2\},\{1,3\}\}.
\]

At a \(P\)-bad, \(Q\)-good vertex, the colours, after exchanging names, are

\[
 (a,a,b,b),\qquad a\ne b.
\]

Try to recolour a subset of the four incident edges with a new fifth
colour while leaving every other colour unchanged.  To make each pair of
\(P\) bichromatic, exactly one edge from the \(a,a\) pair and exactly one
edge from the \(b,b\) pair must be recoloured.  The old \(a\)-degree and
old \(b\)-degree then both become odd at this vertex.  This contradicts the
required evenness of every colour class.

So no operation of the form “apply Ulyanov, then recolour a union of old
colour-class even subgraphs with colour five” can repair even one bad
switched vertex.  A successful fifth-colour argument would have to
reconfigure at least two old colours locally, not merely extract a fifth
colour.

The cyclic-word proof has the same boundary.  It uses the four elements of
\(\mathbb F_2^2\), the nonzero differences forming a three-state set, and a
quadratic parity identity to enforce the transitions of one cyclic word.
The second triangle pairing is not another constraint on that same cyclic
word: after merging the triangle circuit partition, it is precisely the
discarded pairing at every switched occurrence.  Enforcing it would prove
the proposition with \(k=5\), hence the cubic Five-Cycle Double Cover
conjecture itself.

## Independent finite replay

Run:

```text
python3 scratch/check_line_graph_sabidussi_bridge.py
```

The checker uses no SAT package.  It directly:

1. enumerates all perfect matchings, Hamiltonian cycles, and Tait
   colourings of the Petersen graph;
2. enumerates literal \(D_4\)- and \(D_5\)-flows by propagating the vertex
   xor equations;
3. maps a literal \(D_5\)-flow to the line-graph colouring and back; and
4. exhausts all local four-colour patterns and all \(2^4\) choices of edges
   to recolour with colour five.

Expected terminal lines include:

```text
Tait colourings: 0
literal D4 flows: 0
valid pure fifth-colour repairs: 0
PASS
```

This is a no-go result for a proposed proof bridge, not a counterexample to
FiveCDC.  The same checker exhibits a \(D_5\)-flow on the Petersen graph.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified and checked the
line-graph equivalence, the Petersen four-colour obstruction, and the local
fifth-colour no-go, and drafted this note.  Ulyanov's theorem is cited, not
reproved here.
