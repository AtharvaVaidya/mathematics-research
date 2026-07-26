# The refuted cyclic-four separated-triple atom and its transition reduction

Date: **2026-07-26**.

Status: **ATOM LEMMA REFUTED / EXACT CONDITIONAL REDUCTIONS RETAINED**.

This note originally audited the proposed statement

> A cyclically \(4\)-edge-connected, Tait-colourable, simple cubic graph
> has no universally separated three-edge matching.

That statement is false.  The frozen package
`search/cyclic4-universally-separated-triple-n24-20260726/` gives a
24-vertex counterexample and a clean-room exhaustive verifier.  The
purpose of retaining this note is to record what the standard
prescribed-circuit theorems do prove, identify the precise extension
step they do not prove, and preserve the exact transition reduction.
Those reductions remain sound and help explain why the counterexample
exists.

The counterexample has girth four and marked-subdivision girth five.
It therefore does not satisfy the stronger marked circuit-length
condition inherited from a girth-ten ambient minimum counterexample.

## 1. Universal separation and mark precolouring

Let \(H\) be a Tait-colourable cubic graph and let
\(S=\{e_1,e_2,e_3\}\) be a universally separated matching.  Thus no
bichromatic circuit in any Tait colouring contains two members of \(S\).

Every map
\[
   S\longrightarrow\{a,b,c\}
\]
extends to a Tait colouring.  Start with an arbitrary colouring and
process the marks one at a time.  To change the colour of \(e_i\) from
\(p\) to \(q\), interchange \(p,q\) on the unique \(pq\)-circuit through
\(e_i\).  Universal separation says that circuit contains no other
mark, including marks processed earlier.  This proves the assertion.

In particular, the marks may all be given one common colour, or may be
assigned any prescribed pattern using two colours.

## 2. What the prescribed-circuit theorems give

A cyclically \(4\)-edge-connected cubic graph is \(3\)-edge-connected.
Indeed, in a cubic graph every shore of an edge cut of size at most two
contains a circuit, by the degree sum, so such a cut would be cyclic.

Give all three marks the same Tait colour.  By the Parity Lemma, a cut
contained in one colour class has even size.  Hence \(S\) contains no odd
cut.  The Knappe--Pitz circuit theorem therefore gives a circuit
containing all three marks.  In a cubic graph their connected Eulerian
subgraph is an ordinary cycle.

This conclusion also follows from the stronger cycle theorem of
Aldred, Ellingham, Hemminger, and Holton: a cyclically
\(4\)-edge-connected cubic graph is quasi \(4\)-connected, and four
independent edges in such a graph lie on one cycle.  Add any fourth edge
independent of \(S\), when one is available.

These are ordinary graph cycles.  They are not asserted to be
bichromatic circuits in any Tait colouring.  That distinction is the
unresolved step.

The primary sources are:

- P. Knappe and M. Pitz, [*Circuits through prescribed
  edges*](https://arxiv.org/abs/1810.09323), Theorem 1.4;
- R. E. L. Aldred, M. N. Ellingham, R. L. Hemminger, and D. A.
  Holton, [*Cycles in quasi 4-connected
  graphs*](https://ajc.maths.uq.edu.au/pdf/15/ocr-ajc-v15-p37.pdf),
  Theorem 3.3.

## 3. The exact even-factor gap

An **even 2-factor** is a spanning disjoint union of even circuits.

> **Even-factor characterization.**  A matching \(S\) is universally
> separated if and only if every component of every even 2-factor of
> \(H\) contains at most one edge of \(S\).

**Proof.**  The union of any two colour classes of a Tait colouring is
an even 2-factor, and its components are precisely the corresponding
bichromatic circuits.  This proves the forward implication.

Conversely, let \(F\) be an even 2-factor.  Its complement in a cubic
graph is a perfect matching.  Alternately colour every even circuit of
\(F\) with \(a,b\), independently from component to component, and colour
the complementary matching with \(c\).  This is a Tait colouring.
Therefore a component of \(F\) containing two marks is a bichromatic
circuit witnessing failure of universal separation. \(\square\)

Consequently the cycles supplied in Section 2 contradict universal
separation only if one of them can be made a component of an even
2-factor.  Neither prescribed-circuit theorem supplies such an extension.

For one fixed cycle \(C\), the obstruction can be written explicitly.
Let \(D(C)\) be the set of all edges incident with \(V(C)\) but not in
\(C\).  The cycle \(C\) is a component of a 2-factor precisely when
there is a perfect matching containing \(D(C)\); it is a component of
an even 2-factor precisely when that perfect matching can be chosen so
that every other component of its complementary 2-factor is even.
The first requirement may already fail because two edges of \(D(C)\)
can meet at a vertex outside \(C\).

This gives a sound conditional form of the atom lemma:

> **Conditional atom lemma.**  Suppose every three-edge matching in
> \(H\) with no odd cut is contained in a cycle which extends to an even
> 2-factor.  Then \(H\) has no universally separated three-edge
> matching.

The proof is immediate from Knappe--Pitz and the even-factor
characterization.  The extension hypothesis is not currently known to
follow from cyclic \(4\)-edge-connectivity.

## 4. The transition quotient of a hypothetical atom

There is a more structural exact reduction.  Precolour the three marks
using only colours \(a,b\).  Universal separation forces them into three
different components of the \(ab\)-factor.

Contract every \(ab\)-circuit to one vertex.  Each \(c\)-edge becomes an
edge, possibly a loop, of a multigraph \(R\).  Then:

1. \(R\) is connected;
2. \(R\) is Eulerian; and
3. \(R\) is \(4\)-edge-connected.

For the second assertion, the degree of a contracted vertex, with loops
counted twice, is the length of its even \(ab\)-circuit.  For the third,
let \(U\) be a nonempty proper set of vertices of \(R\).  The union of
the corresponding \(ab\)-circuits is a vertex shore \(X\) of \(H\).
Its boundary consists exactly of the \(c\)-edges in
\(\delta_R(U)\).  Both shores contain \(ab\)-circuits, so cyclic
\(4\)-edge-connectivity gives
\[
   |\delta_R(U)|=|\delta_H(X)|\ge4.
\]

Each contracted \(ab\)-circuit gives a cyclic ordering of the incident
\(c\)-half-edges.  Its \(a\)-edges pair alternating consecutive
half-edges, while its \(b\)-edges give the complementary alternating
pairing.  Following the \(a\)-pairing at every vertex decomposes \(R\)
into circuits corresponding exactly to the \(ac\)-circuits of \(H\);
following the \(b\)-pairing gives the \(bc\)-circuits.

The three marks lie at three distinct vertices
\(v_1,v_2,v_3\) of \(R\).  A marked \(a\)- or \(b\)-edge specifies one
of the two local transition pairs at its vertex.

Now interchange \(a,b\) on any chosen set of \(ab\)-circuits.  In \(R\)
this independently swaps the two transition pairings at the
corresponding vertices.  Begin with all three marks coloured \(a\).
For every \(W\subseteq V(R)\), let \(P_W\) use the \(b\)-transition at
vertices in \(W\) and the \(a\)-transition elsewhere; let \(Q_W\) use
the complementary transition at every vertex.  Universal separation
implies the following robust condition:

- the marked transitions at \(v_i\notin W\) lie in distinct circuits
  of \(P_W\); and
- the marked transitions at \(v_i\in W\) lie in distinct circuits of
  \(Q_W\).

Marks on opposite sides of \(W\) have different colours and are already
separated in the unchanged \(ab\)-factor.

Thus every counterexample to the atom lemma produces a
\(4\)-edge-connected Eulerian multigraph with two alternating transition
systems at every vertex and three distinguished transition pairs that
remain separated under every vertex toggle in the sense above.

> **Transition conditional.**  If no transition system with these
> properties exists, then the cyclic-four separated-triple atom lemma
> holds.

This is a one-way necessary reduction.  A converse would require both
that the transition object lift to a simple cubic Tait-coloured graph
and that the three marks remain separated in every other Tait colouring,
not merely in the Kempe subfamily generated by the displayed
\(ab\)-circuit toggles.  The reduction nevertheless isolates concrete
extra structure not seen by ordinary cycle theorems.

## 5. A small countermodel to transition-only sufficiency

The robustness condition from Section 4 is not sufficient by itself.
Let \(R\) have three vertices and two parallel edges between every pair.
It is Eulerian and \(4\)-edge-connected.  At each vertex, pair together
the two half-edges going to either neighbour for the \(a\)-transition.
For the \(b\)-transition, cross-pair the first half-edge to one neighbour
with the first half-edge to the other, and similarly for the second.
Distinguish:

- the \(a\)-pair going from vertex \(0\) to vertex \(1\);
- the \(a\)-pair going from vertex \(1\) to vertex \(2\); and
- the \(a\)-pair going from vertex \(2\) to vertex \(0\).

A direct eight-case trace verifies the Section 4 condition.  With no
vertices or all three vertices toggled, the three distinguished
transitions lie in three different circuits of the applicable
partition.  With one vertex toggled, the other two distinguished
transitions remain in different circuits; with two toggled, the two
toggled distinguished transitions remain in different circuits.

This object even lifts to a simple cyclically \(4\)-edge-connected cubic
graph.  One labelled lift has graph6 record

```text
Kr`GOKA?X@AB
```

and distinguished edges
\[
   (0,1),\quad(6,7),\quad(10,11).
\]
Nevertheless the triple is not universally separated.  The following
is a Tait colouring:

\[
\begin{array}{c|l}
a&(0,1),(2,3),(4,6),(5,7),(8,10),(9,11)\\
b&(0,2),(1,3),(4,5),(6,8),(7,9),(10,11)\\
c&(0,4),(1,5),(2,10),(3,11),(6,7),(8,9).
\end{array}
\]

The \(ac\)-circuit
\[
   0,1,5,7,6,4,0
\]
contains the first two distinguished edges.  Thus a proof must use Tait
colourings outside the single \(ab\)-toggle family, not just the robust
transition condition derived from one starting colouring.

## 6. The actual counterexample and why no low cut follows

The graph6 record

```text
W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E
```

with marked edges
\[
 (0,1),\qquad (2,3),\qquad (20,23)
\]
is simple, connected, cubic, and cyclically \(4\)-edge-connected.  The
independent verifier enumerates all 36 Tait colourings modulo global
colour permutation and checks that no bichromatic circuit contains two
marks.  It also exhausts all cuts of sizes one through three and exhibits
a cyclic four-cut.  Thus this is a genuine counterexample to the proposed
atom lemma, not merely to the transition-only converse in Section 5.

The construction is deliberately kept separate from the surviving
five-CDC branch.  Its girth is four, and subdividing all three marked
edges gives girth five.  In the actual connected minimum-counterexample
branch every core circuit \(C\) must instead satisfy
\[
 |C|+|C\cap S|\ge 10.
\]
All 144 hits in the complete retained \(K_4\)-sum construction have
marked-subdivision girth five, and none passes this stronger condition.

Knappe--Pitz cannot by itself expose a low cut here.  The common-colour
precolouring proves that the marked set contains no odd cut, so its
theorem produces a cycle rather than a cut certificate.  Aldred et al.
produce still more ordinary cycles but likewise do not place any of them
inside an even 2-factor.

Accordingly, possible replacements for the false atom statement are:

1. use the inherited marked circuit-length condition, not cyclic
   \(4\)-edge-connectivity alone;
2. strengthen the transition reduction to incorporate all Tait-colouring
   orbits and the marked-girth constraint; or
3. prove the required four-mark packing statement directly, bypassing a
   stable-triple atom theorem.

The project follows the third route for the four-mark branch.  The
connected eight-mark branch still requires additional structure.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the atom
conjecture, performed the finite screens, and derived this conditional
transition reduction.  A later systematic Codex search refuted the atom
conjecture and produced the frozen witness package.  Any use of the
reduction or counterexample should independently replay the checker and
check the transition correspondence and cited circuit theorems.
