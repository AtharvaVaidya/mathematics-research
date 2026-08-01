# The order-56 cutoff for relevant typed caps

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE STRUCTURAL THEOREM / NOT A PROOF OF FIVECDC**.

## 1. Setting

Let `G` be a simple cyclically 4-edge-connected cubic graph of girth at
least ten.  For an edge `e=uv`, delete `u,v` and add the two artificial
edges

\[
 r=u_1u_2,\qquad s=v_1v_2,
\]

where `u_1,u_2` and `v_1,v_2` are the other neighbours of `u,v`.
Write `H=G div e`.  The standard elimination lemma makes `H` simple and
3-edge-connected.

Suppose `delta_H(X)` is a nontrivial three-edge cut.  Thus both `X` and
its complement have more than one vertex.  Cap either shore by replacing
the other shore with a new cubic vertex `z`.  The cap containing `r` is
denoted `(A,z,r)`.

## 2. The cut must separate the roots

> **Lemma 2.1.** Neither `r` nor `s` crosses `delta_H(X)`, and the two
> endpoints of `r` lie on the shore opposite the two endpoints of `s`.

For a cubic graph and a three-cut,

\[
 |E(H[X])|=(3|X|-3)/2.
\]

If `|X|>1`, this is strictly larger than `|X|-1`; hence each shore of a
nontrivial three-cut contains a circuit.

Let `t` be the number of artificial roots crossing the cut.  Restore
`u,v,e`.  A crossing artificial root is replaced by two spokes, exactly
one of which crosses regardless of which shore receives its inserted
vertex.  A noncrossing root contributes zero crossing spokes when its
inserted vertex is put with its two endpoints.

- If `t=2`, put `u,v` on the same shore.  The one old cut edge and one
  spoke from each root give a three-cut of `G`.
- If `t=1`, put both inserted vertices on the shore containing the
  noncrossing root.  Two old cut edges and one spoke give a three-cut.
- If `t=0` and both roots lie on the same shore, put both inserted
  vertices there.  The original three old cut edges remain a three-cut.

In every case the shore circuits survive (an internal artificial root is
merely replaced by a two-edge path), so the displayed cut is cyclic.  This
contradicts cyclic 4-edge-connectivity of `G`.  The sole remaining case is
that both roots are noncrossing and lie on opposite shores.  This proves
the lemma.  Notice that restoring `u` and `v` on their respective root
shores then turns this three-cut into a four-cut: its three old edges and
`e`.

## 3. Exact structure of a shore cap

> **Lemma 3.1.** Each capped shore `A` is simple and 3-edge-connected.
> The graph `K=A-z` is connected and bridgeless, has exactly three
> degree-two vertices, and has degree three at every other vertex.

Two cut edges cannot have the same endpoint `x` on a nontrivial shore.
If they did, the complement of `x` inside that shore would have boundary
of size at most two: at most the cut edges not incident with `x`, together
with the at most one internal edge at `x`.  (This also covers the case in
which all three cut edges meet `x`.)  The complement is nonempty, so this
contradicts 3-edge-connectivity of `H`.  Thus the three boundary endpoints
are distinct, and adding `z` creates neither a loop nor parallel edges.

Any edge cut of size at most two in `A` gives the same cut in `H`: use
the shore not containing `z`, or take its complement if necessary.
Therefore `A` is 3-edge-connected.  In particular `A-z` is connected,
because otherwise one of its components would use at most one of the
three edges at `z`.  Its three neighbours of `z` have degree two after
deletion, and every other vertex retains degree three.

If an edge `f` were a bridge of `K`, its two shores would contain, say,
`k` and `3-k` of the three neighbours of `z`.  In `A`, their edge
boundaries would have sizes `1+k` and `1+(3-k)`.  Three-edge-connectivity
would require both `k>=2` and `3-k>=2`, which is impossible.  Thus `K` is
bridgeless.  In particular `K-r` is connected, a restriction that can be
useful when exploiting the stronger marked condition below.

> **Lemma 3.2 (marked girth).** `K=A-z` has girth at least nine, and every
> 9-circuit of `K` contains `r`.  Equivalently, `g(K-r)>=10`.

A circuit of `K` avoiding `r` is a circuit of `H` avoiding both roots and
therefore lifts to a circuit of the same length in `G`.  A circuit using
`r` lifts after replacing `r` by the two-edge path through `u`, increasing
its length by one.  Since `g(G)>=10`, the two claimed bounds follow.

## 4. A self-contained order bound

> **Theorem 4.1.** Let `K` be a connected simple graph of girth at least
> nine with exactly three degree-two vertices and every other vertex of
> degree three.  If `n=|V(K)|`, then `n>=43`.

For `j=1,2,3,4`, let `W_j` be the number of oriented nonbacktracking
walks of length `j`.  A walk of length at most four cannot repeat a
vertex, since such a repetition contains a circuit of length at most
four.  It is therefore a path.  From any fixed initial vertex, two
distinct such paths, even if their lengths differ, cannot have the same
endpoint: delete their common initial segment, and their two remaining
arcs contain a circuit whose length is at most the sum of the original
path lengths, hence at most eight.  Thus all endpoints, including the
initial vertex at length zero, are distinct.  Consequently

\[
                         n^2\;\ge\;n+W_1+W_2+W_3+W_4.       \tag{1}
\]

The degree sum gives

\[
 W_1=3n-3,\qquad
 W_2=\sum_v d(v)(d(v)-1)=6n-12.                            \tag{2}
\]

Put `a(v)=d(v)-1`, and let `t` be the number of edges having both ends
among the three degree-two vertices.  Centering a length-three walk on
its middle edge gives

\[
 W_3=2\sum_{xy\in E(K)}a(x)a(y)=12n-36+2t\;\ge\;12n-36.   \tag{3}
\]

For completeness, the equality follows by edge type.  There are `t`
degree-2--degree-2 edges and `6-2t` degree-2--degree-3 edges; starting
from the all-degree-three value `4|E(K)|` loses respectively three and
two per such edge.

Center a length-four walk at a vertex `c`.  Its contribution is

\[
 F(c)=\sum_{x,y\in N(c),\ x\ne y}a(x)a(y).                 \tag{4}
\]

If `c` has degree three and `k` of its neighbours have degree two, the
four possible values of `F(c)` are

\[
                         24,16,10,6,
\]

so `F(c)>=24-8k`.  The degree-three centers see exactly `6-2t`
incidences from degree-two vertices.  Their total contribution is at
least

\[
                         24(n-3)-8(6-2t).
\]

If a degree-two center has `k` degree-two neighbours, its contribution is
`8-5k+k^2`.  If the three such values are `k_1,k_2,k_3`, then
`k_1+k_2+k_3=2t`.  Hence

\[
\begin{aligned}
 W_4
 &\ge 24(n-3)-8(6-2t)
       +\sum_{i=1}^3(8-5k_i+k_i^2)\\
 &=24n-96+6t+\sum_{i=1}^3k_i^2\\
 &\ge24n-96.                                                \tag{5}
\end{aligned}
\]

Substitution of (2)--(5) into (1) yields

\[
                       n^2\ge46n-147.                       \tag{6}
\]

The roots of `x^2-46x+147` are `23-sqrt(382)` and
`23+sqrt(382)`, lying strictly between 3 and 4 and between 42 and 43,
respectively.  The graph contains a circuit of length at least nine, so
the small interval is impossible.  Thus the integer `n` is at least 43.
This proves the theorem.

Combining the preceding lemmas gives the main conclusion.

> **Corollary 4.2 (elementary cutoff).** Every cap arising from a
> nontrivial three-cut of `H=G div e` has at least 44 vertices.  Both
> shores have at least 43 vertices before capping, so `|V(G)|>=88` whenever
> such a cut occurs.

This is a theorem, not a finite-census observation.  The next section
strengthens its numerical conclusion using a standard irregular Moore
bound.

## 5. Irregular-Moore strengthening

Put `L=K-r`.  By Lemma 3.2 it has `n` vertices and girth at least ten.
Deleting one edge from the degree profile of `K` gives

\[
 |E(L)|=(3n-5)/2,\qquad \bar d(L)=3-5/n.                   \tag{7}
\]

Alon, Hoory, and Linial proved that a graph of average degree `d>=2` and
even girth `2s` has at least

\[
 2\sum_{i=0}^{s-1}(d-1)^i
\]

vertices.  Their proof explicitly deletes all degree-zero and degree-one
vertices first; this preserves every cycle and weakly raises average
degree.  Thus it applies even if an endpoint of `r` had degree two in `K`
and becomes a leaf in `L`.  The primary source is N. Alon, S. Hoory, and
N. Linial, *The Moore Bound for Irregular Graphs*, Graphs and
Combinatorics 18 (2002), 53--57, doi:10.1007/s003730200002.

Using `s=5` and (7) gives

\[
 n\ge R(n):=2\sum_{i=0}^{4}(2-5/n)^i.                     \tag{8}
\]

Here is a direct exact check of the integer threshold, so no numerical
root finder is hidden.  Let `h(n)=n-R(n)` and `x=2-5/n`.  For `n>=43`,

\[
 R'(n)=\frac{10}{n^2}(1+2x+3x^2+4x^3)
       <\frac{490}{n^2}<1.
\]

Hence `h` is strictly increasing on the range left by Theorem 4.1.  Exact
arithmetic gives

\[
 h(53)=-\frac{2300549}{7890481}<0,
 \qquad
 h(54)=\frac{2366681}{4251528}>0.
\]

Inequality (8) therefore forces `n>=54`.  Finally, the degree sum of `K`
is `3n-3`, which is even; hence `n` is odd and in fact `n>=55`.

> **Theorem 5.1 (relevant-cap cutoff).** Every relevant core has at least
> 55 vertices, every relevant cap has at least 56 vertices, and a restored
> parent with such a nontrivial three-cut has at least
> `55+55+2=112` vertices.

The Alon--Hoory--Linial theorem is prior work.  The contribution here is
its application after the marked-root cut analysis, not a novelty claim for
the irregular Moore bound itself.

## 6. A Tait one-sided replacement

The double-star premise is stronger than necessary on Tait-colourable
caps.

> **Proposition 6.1.** If the rooted cap `(A,z,r)` is 2-connected and
> Tait-colourable, then its typed signature has external-mode states whose
> physical pairs cover all three ports.  Consequently two such caps have a
> common external typed state and glue root-good.

Fix a proper three-edge-colouring of `A`, with colours `2,3,4`.  For each
port `a`, 2-connectivity supplies a circuit `C` through `r` and `a`.
At `z`, the circuit uses `a` and exactly one other port, say `b`; write
`c` for the inactive port.  Define

\[
q(f)=
 \begin{cases}
  0\alpha,&f\in E(C)\text{ and has Tait colour }\alpha,\\
  \{2,3,4\}\setminus\{\alpha\},&f\notin E(C)\text{ and has colour }\alpha.
\end{cases}                                                \tag{9}
\]

At a vertex outside `C` the labels are `23,24,34`; at a vertex on `C`
they are `0alpha,0beta,alphabeta`.  Thus (7) is a `D5`-flow and
`Y_01(q)=E(C)`.  In particular the root circuit uses physical pair `ab`.
The inactive port `c` has the third Tait colour `gamma`, so
`q(c)={2,3,4}-{gamma}` is disjoint from `01`.  The state is external.

Repeating this for each of the three ports proves external port coverage.
Any subset of the three physical pairs covering all three ports has at
least two members.  Two subsets of a three-element set of size at least
two intersect, and both states at an intersecting pair are external.
The typed-port gluing lemma now applies.

## 7. Exact open boundary

Theorem 5.1 does **not** prove that an order-56 relevant cap exists, that
every relevant signature contains a double star, or that every relevant
cap has external port coverage.  Proposition 6.1 leaves the case in which
at least one shore cap is non-Tait.  That non-Tait, order-at-least-56 case
is the exact surviving typed-cap branch of this edge-elimination strategy.

The order-14 unrestricted cap census remains correct, but none of its
interfaces satisfies the marked-girth conditions forced here.  It cannot
be cited as direct finite evidence in the relevant minimum-obstruction
domain without this distinction.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the cut classification,
the degree-specific nonbacktracking count, and the Tait external-mode
replacement, and implemented the arithmetic replay.  No priority claim is
made.  Independent human review is required before citation.
