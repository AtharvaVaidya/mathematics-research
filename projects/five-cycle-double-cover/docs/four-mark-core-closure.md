# A four-mark core closure from cyclic decomposition

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE PROOF / INDEPENDENT CODEX-AGENT AUDIT
PASSED**.

This note proves the marked-core statement left open in
`marked-core-cyclic-lift-condition.md`, subject only to the standard
3-sum decomposition of a 3-connected cubic graph into cyclically
4-edge-connected factors.  The exact cubic statement and its short proof
are Theorem 6.1 of R. Nedela, M. Seifrtová, and M. Škoviera,
*Decycling cubic graphs*, <https://arxiv.org/abs/2309.11606>.  A more
general component-tree theorem is A. V. Pastor, *On the Decomposition of
a 3-Connected Graph into Cyclically 4-Edge-Connected Components*, J.
Math. Sci. 232 (2018), 61--83,
<https://doi.org/10.1007/s10958-018-3859-0>.

The two other imported circuit results are:

1. R. E. L. Aldred, M. N. Ellingham, R. L. Hemminger, and D. A.
   Holton, *Cycles in quasi 4-connected graphs*, Australas. J. Combin.
   15 (1997), 37--46,
   <https://ajc.maths.uq.edu.au/pdf/15/ocr-ajc-v15-p37.pdf>.  Their
   Theorem 3.3 includes the consequence that four independent edges in
   a quasi 4-connected graph lie on one cycle, and they explicitly note
   that cyclically 4-edge-connected cubic graphs are quasi
   4-connected.
2. P. Knappe and M. Pitz, *Circuits through prescribed edges*, J.
   Graph Theory 93 (2020), 470--482,
   <https://doi.org/10.1002/jgt.22497>.  Their Fact 5.4 gives
   \(g(3)=3\): in a 3-edge-connected graph, a set of three edges is
   contained in one circuit if and only if it contains no odd cut.
   The open preprint is
   <https://arxiv.org/abs/1810.09323>.

No claim of novelty is made until the combination below has been
checked against the earlier four-edge and decomposition literature.

## 1. Statement

Let \(H\) be a connected simple cubic graph, and let \(S\) be a
four-edge matching.  A proper three-edge-colouring of \(H\) is called a
Tait colouring.  Say that \(S\) is **universally separated** if no
bichromatic circuit in any Tait colouring contains two edges of \(S\).

Assume:

1. \(H\) is Tait-colourable;
2. \(S\) is universally separated; and
3. for every \(X\subseteq V(H)\) for which \(H[X]\) contains a circuit,
   \[
      |\delta_H(X)|+|S\cap E(H[X])|\ge4.                 \tag{1}
   \]

> **Four-mark core theorem.**  Under these hypotheses there is a binary
> cycle \(Q\subseteq E(H)\) containing \(S\) such that every circuit
> component of \(Q\) contains an even number of edges of \(S\).

More precisely, the proof constructs either two disjoint two-mark
circuits (at an unmarked \(2+2\) cyclic three-cut) or one circuit
containing all four marks.  It does **not** prove an unconditional
one-circuit strengthening.

The already proved even-marked circuit criterion then says that the
four corresponding terminals pack two edge-disjoint \(T\)-joins.

## 2. Preliminary facts

### 2.1 Mark precolouring

Every map \(S\to\{a,b,c\}\) extends to a Tait colouring of \(H\).

Indeed, begin with any Tait colouring.  If a marked edge \(e\) has
colour \(p\) and is requested to have colour \(q\), switch \(p\) and
\(q\) on the unique \(pq\)-bichromatic circuit through \(e\).
Universal separation says that this switch changes no other mark.
Processing the marks one at a time proves the assertion.

In particular, there is a Tait colouring in which all four marks have
one common colour \(c\).

### 2.2 No cyclic two-edge cut

The two-mark shore lemma in
`marked-three-edge-cut-signatures.md` proves that \(H\) has no cyclic
two-edge cut if the conclusion of the four-mark core theorem fails.
For such a cut, (1) puts exactly two marks on each shore, and one
circuit through each pair gives the required binary cycle.

### 2.3 Three-connectivity

If the conclusion fails, \(H\) is 3-connected.

A Tait-colourable cubic graph has no bridge by the Parity Lemma.  A
cutvertex in a bridgeless cubic graph is also impossible: among the
components behind the cutvertex, one receives only one of its three
incident edges, making that edge a bridge.

Suppose \(\{u,v\}\) is a two-vertex cut.  Every component \(D\) of
\(H-\{u,v\}\) has at least three boundary edges.  Otherwise
\(\delta_H(D)\) has size at most two; both of its shores are cyclic by
the cubic degree sum, and this is the cyclic two-edge cut excluded
above.

There are at least two such components, while \(u\) and \(v\) supply
at most six boundary incidences.  Hence \(uv\notin E(H)\), there are
exactly two components \(D_1,D_2\), and each has three boundary edges.
Neither component can send all three edges to the same one of \(u,v\),
because the other vertex would be a cutvertex.  Relabel so that
\(D_1\) sends two edges to \(u\) and one to \(v\).  Then
\[
  \delta_H(D_1\cup\{u\})
\]
has exactly two edges: the one edge from \(u\) to \(D_2\) and the one
edge from \(D_1\) to \(v\).  Both shores contain a circuit, again
contradicting Section 2.2.  Thus no two-vertex cut exists.

## 3. Every marked cyclic three-cut is reducible

Let \(B=\delta_H(A)\) be a cyclic three-edge cut, and put
\[
 r=|B\cap S|,\qquad
 a=|S\cap E(H[A])|,\qquad
 d=|S\cap E(H[V(H)\setminus A])|.
\]
Applying (1) to both shores gives \(a,d\ge1\), and
\[
 a+d+r=4.                                             \tag{2}
\]
Consequently \(r\le2\).

### 3.1 Two marked cut edges

If \(r=2\), then (2) gives \(a=d=1\).  The one-mark shore lemma supplies,
on each shore, a path through its unique internal mark between the ends
of the two marked cut edges.  The two paths and those two cut edges form
one circuit containing all four marks.

### 3.2 One marked cut edge

Suppose \(r=1\).  Up to exchanging the shores, \(a=1,d=2\).
Cap the two-mark shore by adjoining a new cubic vertex \(z\), and let
\(\widehat D\) be the resulting cubic graph.  The cap is Tait-colourable.
It is 3-edge-connected: a two-edge cut in a cubic graph has two cyclic
shores, and the shore avoiding \(z\) would give a cyclic two-edge cut
of \(H\).

In \(\widehat D\), select the cap edge corresponding to the marked
member of \(B\), together with the two internal marks.  These three
edges are independent because \(S\) is a matching.  They contain no
odd cut.  Indeed, 3-edge-connectivity leaves only a three-edge cut to
consider.  A trivial three-cut is a vertex star and cannot equal an
independent set.  For a nontrivial three-cut, take the cyclic shore
avoiding \(z\).  Both internal marks would lie on its boundary and no
mark would lie internally, contradicting \(3+0\ge4\) in (1).

Knappe--Pitz \(g(3)=3\) therefore gives a circuit through the three
selected edges.  Since \(\widehat D\) is cubic, the edge set of this
connected even subgraph is a cycle.  At \(z\) it uses the marked cap
edge and one other cap edge.  Delete \(z\); what remains is a path
through both internal marks between those two boundary positions.

On the one-mark shore, the one-mark shore lemma gives a path through its
mark for the same boundary pair.  Gluing the two paths with the two cut
edges gives one circuit with
\[
  2\text{ internal marks}+1\text{ internal mark}
    +1\text{ marked cut edge}=4
\]
marks.

Thus a nonpacking graph has no marked cyclic three-edge cut.

## 4. The unmarked cuts and their weighted tree

For an unmarked cyclic three-cut, (2) leaves either the split \(2+2\) or
\(1+3\).  The balanced cyclic three-cut corollary in
`marked-three-edge-cut-signatures.md` packs the \(2+2\) case using one
two-mark circuit on each shore.  Hence every cyclic three-cut of a
surviving nonpacking graph is unmarked and splits the four marks
\(1+3\).

Apply the standard 3-sum decomposition theorem to the 3-connected cubic
graph \(H\).  Recall its elementary construction.  Split a nontrivial
cyclic three-edge cut and cap each shore by a new cubic root vertex.
Both capped graphs are 3-connected.  Repeat until no factor has a
nontrivial cyclic three-cut.  Termination is by decreasing order, and
the final factors are cyclically 4-edge-connected.  Reversing the
splits reconstructs \(H\) by repeated vertex 3-sums.  This is precisely
the existence part of Nedela--Seifrtová--Škoviera Theorem 6.1.

Make a tree \(\mathcal T\) whose vertices are the final factors and
whose edges record the reverse 3-sums.  Every reverse sum joins two
previously disjoint composites, so the incidence graph is a tree.
Each tree edge corresponds to its principal cyclic three-edge cut in
\(H\).

The root vertices used by different tree edges incident with one factor
are distinct because one vertex cannot be deleted twice.  They need not
be nonadjacent.  If two roots are adjacent, their common edge may be the
same-colour edge selected for both branches below.  The proof therefore
takes the **set** of selected edges and treats the case in which its size
drops below four separately.

Because all those cuts are unmarked, every marked edge belongs to one
decomposition node.  Give each node weight equal to its number of
marks.  The preceding paragraph says that deleting any tree edge
splits the total weight four as \(1+3\).

There is a node \(K\) such that every component of
\(\mathcal T-K\) has weight one.  To see this, start at any node.  If
some component after its deletion has weight three, move into that
component.  The component just left has weight one, so this walk never
backtracks and must stop.  At the stopping node, no component has weight
three; no component can have weight two by the \(1+3\) rule, and no
component can have weight zero because every tree edge has positive
weight on both sides.  Thus every component has weight one.

Let \(K\) itself contain \(r\) marked edges, and let
\[
 q=4-r
\]
be the number of incident one-mark branches.  In the capped cubic graph
corresponding to \(K\), denote the cap vertices of those branches by
\(z_1,\ldots,z_q\).

## 5. One Aldred cycle closes the tree

Choose, by Section 2.1, a Tait colouring of \(H\) in which all four marks
have colour \(c\).  Restrict it to the capped central component \(K\).
The \(r\) internal marks of \(K\) have colour \(c\).  At each cap vertex
\(z_j\), select the unique incident edge \(f_j\) of colour \(c\).

Let \(F\) be the set of distinct edges among
\[
   (S\cap E(K))\cup\{f_1,\ldots,f_q\}                 \tag{3}
\]
and note that \(F\) is a matching because it lies in one colour class.
Every internal mark belongs to \(F\), and every cap vertex \(z_j\) is
incident with an edge of \(F\).  Also \(1\le |F|\le4\).

If \(|F|=4\), the
Aldred--Ellingham--Hemminger--Holton theorem gives a cycle through \(F\)
because the cyclically 4-edge-connected cubic graph \(K\) is quasi
4-connected.  If \(|F|\le3\), then \(F\) contains no odd cut.  A
one-edge cut is excluded by 3-edge-connectivity.  A three-edge cut
contained in the matching \(F\) cannot be a vertex star, while every
nontrivial three-edge cut is excluded by cyclic 4-edge-connectivity.
Knappe--Pitz \(g(3)=3\) therefore gives a circuit through \(F\), whose
edge set is a cycle because \(K\) is cubic.  In either case denote the
cycle by \(Z\).

For every \(j\), the cycle \(Z\) passes through \(z_j\), using \(f_j\)
and exactly one other incident edge.  The branch of \(\mathcal T-K\)
represented by \(z_j\) contains exactly one mark.  Apply the one-mark
shore lemma to that entire shore and to the corresponding boundary
pair.  It supplies a path through its unique mark between those two
boundary positions.

Lift \(Z\) through the remembered 3-sums one at a time, replacing each
two-edge passage through a cap root by the supplied one-mark path and
the corresponding boundary edges.  This sequential formulation also
covers adjacent cap roots.  In particular, if \(f_i=f_j=z_i z_j\),
then the common cap edge expands to the single boundary edge between
the two expanded shores; the two shore paths meet it at its opposite
ends, so no edge is duplicated and every resulting vertex still has
degree two.  Each lift preserves one circuit.  The final circuit in
\(H\) contains the \(r\) central marks and one mark from each of the
\(q=4-r\) branches: all four marks.  Its marked count is even, so it is
the binary cycle required by the theorem.  This contradicts the assumed
nonpacking.

## 6. Scope and remaining five-CDC work

The theorem closes the **four-mark, two-component marked-core branch**
of the minimum exact-zero matching reduction.  It does not resolve the
five-cycle double cover conjecture.  In particular, the connected
eight-mark core branch and the global existence/exchange step for a
suitable minimum exact-zero matching remain.

The proof is predominantly elementary.  A human audit should focus on
the transfer of marks and Tait colours through the repeated 3-sum
decomposition and on the assertion that the factor-incidence structure
may be read as the reconstruction tree used in Section 4.

An independently prompted Codex referee agent checked the reductions,
the two prescribed-edge theorems, and the cubic decomposition argument
on 2026-07-26 and reported that the stated binary-cycle theorem is
sound.  This is a second AI-agent audit, not independent human
verification or peer review.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the combination of the
marked shore lemmas, the Knappe--Pitz three-edge circuit theorem, the
cyclic component tree, and the Aldred--Ellingham--Hemminger--Holton
four-edge cycle theorem; wrote the proof; and ran the finite diagnostics
that motivated it.  The argument is displayed for line-by-line human
checking.  The finite searches are not used as proof.
