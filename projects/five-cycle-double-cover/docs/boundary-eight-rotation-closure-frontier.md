# Boundary-eight rotation closure: exact barrier structure and its limit

Date: **2026-07-27**.

Status: **BOUNDARY-EIGHT STRUCTURE PROVED / LOCAL ROTATION-CLOSURE
LEMMA FALSE / FOCUSED CYCLIC-FOUR LEMMA OPEN**.

This memo attacks the rotation-closure step isolated in Section 6 of
`focused-theta-choice-census-frontier.md`.

The useful outcome is twofold:

1. the Gallai--Edmonds incidence structure in the boundary-eight case
   can be described exactly; but
2. that local structure does not force an alternating escape.

The sharp ten-vertex Tait example already obeys the complete canonical
singleton-barrier pattern and is closed under every maximum-matching
exchange.  A stronger 18-vertex example is simple, cubic,
3-edge-connected, non-Tait, boundary eight, and still exchange-closed.
It fails the focused hypotheses at exactly cyclic
four-edge-connectivity.  Its canonical barrier exposes the failure as a
nontrivial cyclic component of boundary three.

Consequently no universal or Five-Cycle Double Cover conclusion is
claimed.  The version retaining global cyclic four-edge-connectivity
remains open.

## 1. Exact boundary-eight Gallai--Edmonds structure

Let \(G\) be a finite simple cubic 3-edge-connected graph.  Let
\(R=\{r_1,r_2\}\) be independent roots, let \(U=V(R)\), put
\(H=G-U\), and assume
\[
                  \operatorname{def}(H)=2,
                  \qquad |\delta_G(U)|=8.              \tag{1.1}
\]

Write \(D,A,C\) for the Gallai--Edmonds decomposition of \(H\):

* \(D\) is the set of vertices exposed by at least one maximum matching;
* \(A=N_H(D)\setminus D\);
* \(C=V(H)\setminus(A\cup D)\).

The components of \(H[D]\) are factor-critical, \(H[C]\) has a perfect
matching, and \(A\) is a tight barrier.  If \(s=|A|\), then \(H-A\) has
\(s+2\) odd \(D\)-components.

> **Theorem 1.1 (boundary-eight incidence form).**  Under (1.1):
>
> 1. \(C=\varnothing\);
> 2. if \(Q_1,\ldots,Q_{s+2}\) are the \(D\)-components and
>    \(q_i=|\delta_G(Q_i)|\), then either every \(q_i=3\), or exactly one
>    \(q_i=5\) and all the others equal three;
> 3. in the all-three case, \(G[A\cup U]\) has exactly the two roots and
>    one further edge; in the one-five case, its only edges are the
>    roots;
> 4. if \(G\) is cyclically 4-edge-connected, every boundary-three
>    \(D\)-component is a singleton.

### Proof

There are \(s+2\) odd components.  Cubic parity and
3-edge-connectivity give
\[
                 q_i\ge3,\qquad q_i\equiv1\pmod2.      \tag{1.2}
\]
Every edge leaving a component of \(H-A\) ends in \(A\cup U\).  The
available incidence capacity is at most
\[
                         3s+|\delta_G(U)|=3s+8.        \tag{1.3}
\]
The odd components alone consume at least \(3(s+2)=3s+6\).

If \(C\ne\varnothing\), a connected component of \(H[C]\) is a nonempty
proper vertex set of \(G\), so its boundary has at least three edges.
Together with the odd components this would consume at least
\(3s+9\) incidences in (1.3), a contradiction.  Thus \(C=\varnothing\).

Now
\[
                    \sum_i(q_i-3)\le2.
\]
Each summand is a nonnegative even integer by (1.2), proving the two
boundary profiles.

Because boundary eight means that the roots are the only edges of
\(G[U]\), count the unused capacity in (1.3).  If \(e\) is the number
of non-root edges internal to \(A\cup U\), then
\[
                    3s+8-\sum_iq_i=2e.                \tag{1.4}
\]
Hence \(e=1\) in the all-three case and \(e=0\) in the one-five case.

Finally, the singleton conclusion is exactly the degree-counting and
cyclic-cut argument of Theorem 3.1 in the deficiency memo: a
boundary-three odd component is either a singleton or one shore of a
cyclic 3-edge-cut.  Cyclic four-edge-connectivity excludes the latter.
\(\square\)

Define the incidence multigraph \(B\) with left side \(A\), right side
\(\{Q_1,\ldots,Q_{s+2}\}\), and one edge for every \(H\)-edge joining
the corresponding objects.

> **Lemma 1.2 (matching choices in \(B\)).**  Every maximum matching
> \(P\) of \(H\) matches every vertex of \(A\) into a distinct
> \(D\)-component.  Exactly two \(D\)-components are not assigned a
> vertex of \(A\), and each contains one vertex exposed by \(P\).

### Proof

There are \(s+2\) odd components of \(H-A\).  If only \(k\) of them
receive matching edges from \(A\), at least \(s+2-k\) vertices remain
exposed inside them.  A maximum matching exposes exactly two vertices,
so \(k\ge s\).  A matching has at most one edge at each of the \(s\)
vertices of \(A\), hence \(k=s\).  The \(s\) edges have distinct
component endpoints, and the two unassigned odd components each
contribute one exposed vertex. \(\square\)

Factor-criticality supplies the converse extensions whenever the
chosen incidence edges form a matching saturating \(A\).  Thus the
rooted matching problem is controlled by the \(A\)-to-component
incidence matching together with the internal factor-critical choices.

## 2. Why local barrier rigidity cannot prove rotation escape

The ten-vertex graph

```text
I?BeeOwM?
```

with roots \(\{2,5\}\) was checked in
`prescribed-root-matching-deficiency-frontier.md`.  Its canonical
Gallai--Edmonds decomposition is
\[
 A=\{4,7\},\qquad D=\{0,1,8,9\},\qquad C=\varnothing.
\]
All four \(D\)-components are singletons of boundary three.  The
incidence graph \(B\) is the disjoint union of two copies of
\(K_{1,2}\), and the unique extra edge allowed by (1.4) is
\(8=(4,7)\), joining the two vertices of \(A\).

Every maximum matching selects one leaf edge in each \(K_{1,2}\).
The other leaf on each side is exposed, and edge 8 is never selected.
The roots and edge 8 form a cyclic 3-edge-cut.  After deleting the
roots and the maximum matching, edge 8 is the unique surviving edge
across that cut, hence is the link of a dumbbell.

This example satisfies every *local* conclusion of Theorem 1.1,
including the canonical singleton conclusion.  All four maximum
matchings are dumbbell matchings, so every alternating circuit switch
and every exposed-vertex rotation stays dumbbell.  What fails is the
global cyclic-four hypothesis; the graph is also Tait-colourable.

Therefore “boundary eight plus the rigid barrier profile” is not a
sound replacement for cyclic four-edge-connectivity.

## 3. A non-Tait, 3-edge-connected exchange-closed countermodel

The stronger graph has canonical graph6 encoding

```text
Q???C@?GF?CKSOF?AQ?W_B_AA_?
```

and indexed edges

| \(i\) | edge | \(i\) | edge | \(i\) | edge |
|---:|:---:|---:|:---:|---:|:---:|
| 0 | 0--7 | 9 | 1--12 | 18 | 4--15 |
| 1 | 1--8 | 10 | 3--12 | 19 | 5--15 |
| 2 | 2--9 | 11 | 7--12 | 20 | 9--15 |
| 3 | 0--10 | 12 | 3--13 | 21 | 4--16 |
| 4 | 1--10 | 13 | 4--13 | 22 | 5--16 |
| 5 | 2--10 | 14 | 5--13 | 23 | 6--16 |
| 6 | 2--11 | 15 | 3--14 | 24 | 0--17 |
| 7 | 7--11 | 16 | 6--14 | 25 | 6--17 |
| 8 | 8--11 | 17 | 9--14 | 26 | 8--17 |

Take
\[
                         R=\{12,20\}.
\]
Then \(U=\{3,9,13,15\}\), the roots are the only edges of \(G[U]\),
and \(|\delta_G(U)|=8\).

The graph is simple, cubic, and 3-edge-connected.  It is not cyclically
4-edge-connected: for
\[
                         X=\{4,5,13,15,16\},
\]
which induces \(K_{2,3}\),
\[
                         \delta_G(X)=\{12,20,23\}.      \tag{3.1}
\]
Both shores contain circuits.

### 3.1 The human obstruction

For \(H=G-U\), the canonical Gallai--Edmonds decomposition is
\[
\begin{aligned}
 A&=\{6,16\},\\
 C&=\varnothing,\\
 D_0&=\{0,1,2,7,8,10,11,12,17\},\\
 D_1&=\{4\},\qquad D_2=\{5\},\qquad D_3=\{14\}.
\end{aligned}                                           \tag{3.2}
\]
All four \(D_i\) are factor-critical.  The incidence edges are
\[
\begin{array}{c|c}
6\text{ to }D_0 & 25\\
6\text{ to }D_3 & 16\\
16\text{ to }D_1 & 21\\
16\text{ to }D_2 & 22 .
\end{array}                                               \tag{3.3}
\]
Thus \(B\) is again two disjoint copies of \(K_{1,2}\).  Its unique
extra \(A\)-edge is \(23=(6,16)\).

By Lemma 1.2 every maximum matching of \(H\) selects one of
\(\{16,25\}\) and one of \(\{21,22\}\), and never selects edge 23.
It leaves one exposed vertex in \(D_0\) or \(D_3\), outside \(X\), and
one of the singleton vertices 4 or 5 exposed inside \(X\).

For every maximum \(P\), (3.1) therefore gives
\[
          \delta_{\,G-(R\cup P)}(X)=\{23\}.             \tag{3.4}
\]
Edge 23 is a bridge separating the two degree-three vertices.  The
two-core dichotomy forces a loop--link--loop core.  This proves by hand,
without relying on a heuristic search, that every maximum matching is
dumbbell.

The exact matching count is 40.  If
\[
 \beta(P)=\#\{\text{bridges of }G-(R\cup P)\},
\]
the distribution over these 40 matchings is
\[
\begin{array}{c|ccccc}
\beta&3&4&5&8&10\\ \hline
\#P&8&8&8&8&8.
\end{array}                                               \tag{3.5}
\]
In particular a \(\beta\)-minimal matching has \(\beta=3>0\).

The elementary exchange graph has the 40 maximum matchings as vertices
and joins two when their symmetric difference is one even alternating
path or one even alternating circuit.  It is connected, with 384
edges: 364 rotations and 20 circuit switches.  Since (3.4) holds for
all 40 vertices, the entire maximum-matching space is closed under
every elementary exchange while remaining dumbbell.  Thus
\(\beta\)-minimality plus rotation closure is consistent.

### 3.2 A short non-Tait proof

The shore \(X\) in (3.1) is a \(K_{2,3}\) substituted for a cubic
vertex.  Contract it to one vertex.  In the resulting 14-vertex graph,
\[
                         \{3,6,9,14,x\}
\]
is another \(K_{2,3}\) shore; contract it as well.  The resulting
10-vertex graph is the Petersen graph.

Replacing a cubic vertex by this \(K_{2,3}\) three-pole preserves
3-edge-colourability in both directions.  Indeed, at the three
degree-two port vertices a proper colouring of the pole has three
distinct missing colours, and any three distinct boundary colours
extend across the six internal edges.  Contracting or expanding
therefore preserves Tait-colourability.  Since the Petersen graph is
not Tait-colourable, neither is the displayed 18-vertex graph.

As an independent finite check, the graph has 24 perfect matchings and
the complementary 2-factor has circuit lengths \(5\) and \(13\) for
every one.  No complement is a union of even circuits, which is
equivalent to the absence of a Tait colouring in a cubic graph.

## 4. Exactly which focused hypothesis fails

The 18-vertex countermodel satisfies:

* finite, connected, simple, cubic;
* 3-edge-connectivity;
* non-Taitness;
* independent roots and boundary eight;
* \(\operatorname{def}(G-U)=2\);
* a noncanonical tight barrier \(S=\{16\}\) with exactly the numerical
  pattern allowed by Theorem 3.1: two boundary-three singletons and one
  boundary-five exception;
* closure of the complete maximum-matching space under alternating
  circuits and exposed-vertex rotations.

It fails **cyclic four-edge-connectivity**, explicitly by (3.1).  The
canonical barrier \(A=\{6,16\}\) shows why this matters: \(D_0\) is a
nontrivial boundary-three component.  It contains a circuit and is
itself a shore of the second cyclic 3-edge-cut
\[
             \delta_G(D_0)=\{2,10,25\}.                 \tag{4.1}
\]
This is exactly the alternative excluded in the last step of
Theorem 1.1(4).

There are three tight barriers,
\[
                         \{6\},\quad\{16\},\quad\{6,16\}.
\]
The fact that one noncanonical barrier has the permitted numerical
shape therefore does not rescue the argument: the canonical
Gallai--Edmonds barrier is the one that exposes the cyclic-3
decomposition of the matching space.

The exact focused lemma

```text
cyclically 4-edge-connected + boundary eight + deficiency two
    => some maximum matching has a theta complement
```

is neither proved nor disproved here.  What is disproved is the proposed
derivation from boundary-eight barrier counts, non-Taitness, and
rotation minimality without using global cyclic four-edge-connectivity.
A successful proof must use that global hypothesis to prevent the
incidence matching from splitting along a root-aligned cyclic 3-cut, or
must find an equivalent global condition.

## 5. Finite minimality and replay

Within the retained documented-complete non-Tait connected simple cubic
corpora, order 18 is smallest for a 3-edge-connected graph with an
independent all-dumbbell root pair.  The independent checker verifies
all root pairs in the lower-order hard corpora:

| order | non-Tait rows | 3-edge-connected rows | root pairs | all-dumbbell |
|---:|---:|---:|---:|---:|
| 10 | 1 | 1 | 75 | 0 |
| 12 | 1 | 1 | 117 | 0 |
| 14 | 5 | 4 | 672 | 0 |
| 16 | 26 | 18 | 4,104 | 0 |

This minimality statement inherits only the source-completeness
documentation of
`search/order22-prelaunch-validation-20260725`; the checker hashes the
retained inputs and does not regenerate them.

Run:

```sh
python3 scratch/rotation-closure-countermodel-checker.py
```

The standard-library checker independently verifies:

* graph6, the literal edge table, simplicity, cubicity, and
  3-edge-connectivity;
* both displayed cyclic 3-cuts;
* boundary eight and matching deficiency two;
* all 40 maximum matchings and their bridge counts;
* the complete Gallai--Edmonds decomposition, factor-critical
  components, and tight barriers;
* the connected 384-edge elementary exchange graph;
* non-Taitness from all perfect matchings;
* both \(K_{2,3}\) contractions and the Petersen quotient; and
* the lower-order finite minimality table.

Frozen SHA-256 values:

```text
cc15e7e59c6eeb497822bd1fbd5e1ac533f844cdc281abf0e5c6e8a0cefb943c  scratch/rotation-closure-countermodel-checker.py
eafeb250822be4213a6caca7a729d35d71d62ba6e5edcad67e068f6ab9a5ab8a  checker standard-output JSON
```

## 6. AI-use disclosure

The barrier derivation, countermodel search, checker, and exposition were
developed with substantial assistance from OpenAI Codex under human
direction.  The universal statements proved here are written out in
full.  The countermodel is accompanied by a direct cut-and-matching
proof and a deterministic standard-library checker.  No finite census
or AI-generated argument is represented as a resolution of the
remaining cyclic-four lemma or of the Five-Cycle Double Cover
Conjecture.
