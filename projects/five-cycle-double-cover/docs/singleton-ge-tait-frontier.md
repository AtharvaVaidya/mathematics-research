# Singleton Gallai--Edmonds case: the connected cross-graph frontier

Date: **2026-07-27**.

Status: **EXACT STRUCTURAL REDUCTION / DISCONNECTED CASE TAIT /
CONNECTED CASE OPEN**.

## 1. Target and honest outcome

Let \(G\) be finite, simple, cubic, and cyclically
4-edge-connected.  Let \(R=\{r_1,r_2\}\) be independent edges, let
\(U=V(R)\), and put \(H=G-U\).  Assume
\[
 \operatorname{def}(H)=2,\qquad |\delta_G(U)|=8,
\]
and assume that every component of \(D\) in the canonical
Gallai--Edmonds decomposition
\[
                         V(H)=D\mathbin{\dot\cup}A
\]
is a singleton.

The requested implication is
\[
\begin{split}
 &\text{every maximum matching \(P\) of \(H\) gives a dumbbell}\\
 &\hspace{38mm}\Longrightarrow G\text{ is Tait-colourable}. \tag{1.1}
\end{split}
\]

This memo does **not** prove or refute (1.1).  It gives a
human-checkable reduction to one sharply defined remaining case.

Delete the two roots and the unique further edge internal to
\(A\cup U\).  The remaining graph \(J\) is bipartite.  If \(J\) is
disconnected, then \(G\) is in fact bipartite and every rooted maximum
matching is dumbbell.  Hence (1.1) is proved in the disconnected case.
Any counterexample to (1.1), and any proof obligation still capable of
using non-Taitness, must have **connected \(J\)**.

No claim is made about the one-boundary-five Gallai--Edmonds case or
about the Five-Cycle Double Cover Conjecture.

## 2. The exact vertex partition

Write
\[
                         a=|A|.
\]
The canonical Gallai--Edmonds theorem and deficiency two give
\[
                         |D|=a+2.                      \tag{2.1}
\]
Because every component of \(H[D]\) is a singleton, \(D\) is an
independent set in \(G\).  Put
\[
                         W=A\cup U.
\]
Then
\[
                         |W|=a+4.                      \tag{2.2}
\]

The boundary-eight incidence count proved in
`boundary-eight-rotation-closure-frontier.md` says that
\(G[W]\) contains the two roots and exactly one further edge.  Denote
that edge by
\[
                              e.                       \tag{2.3}
\]
Thus every edge outside
\[
                         T=\{r_1,r_2,e\}               \tag{2.4}
\]
joins \(D\) to \(W\).

> **Lemma 2.1 (the location trichotomy).**
>
> Under the present boundary-eight assumptions:
>
> 1. \(e\) may have type \(A\)--\(A\);
> 2. \(e\) may have type \(A\)--\(U\);
> 3. \(e\) cannot have type \(U\)--\(U\).
>
> In the \(A\)--\(A\) case the three edges of \(T\) form a matching.
> In the \(A\)--\(U\) case, \(e\) and one root form a two-edge path,
> while the other root is disjoint from that path.

### Proof

For four root endpoints of total cubic degree 12,
\[
                  |\delta_G(U)|=12-2|E(G[U])|.         \tag{2.5}
\]
Boundary eight forces \(|E(G[U])|=2\).  The two roots already are two
edges of \(G[U]\), so there is no further \(U\)--\(U\) edge.

The sets \(A\) and \(U\) are disjoint.  Hence an \(A\)--\(A\) edge is
disjoint from both independent roots.  An \(A\)--\(U\) edge meets the
unique root incident with its \(U\)-endpoint and is disjoint from the
other root. \(\square\)

Define
\[
                         J=G-T.                         \tag{2.6}
\]
By construction:

> **Corollary 2.2.**  \(J\) is bipartite with bipartition
> \((D,W)\).

The degree deficits in \(J\) distinguish the two possible locations of
\(e\):

* if \(e\) is \(A\)--\(A\), precisely its two endpoints and the four
  root endpoints have degree two in \(J\); every other \(W\)-vertex has
  degree three;
* if \(e\) is \(A\)--\(U\), the common \(U\)-endpoint of \(e\) and its
  root has degree one in \(J\), four other \(W\)-vertices have degree
  two, and every remaining \(W\)-vertex has degree three.

In both cases every vertex of \(D\) has degree three in \(J\), and the
total degree deficit on the \(W\)-side is six.

## 3. The Gallai--Edmonds incidence graph

Let \(B\) be the bipartite graph with parts \(A,D\) whose edges are the
\(A\)--\(D\) edges of \(H\).  The extra edge \(e\), when it has type
\(A\)--\(A\), belongs to \(H\) but belongs to no maximum matching:
every maximum matching matches all of \(A\) to distinct vertices of
\(D\).

> **Lemma 3.1 (only two incidence shapes at component level).**  Every
> connected component \(B_i\) of \(B\), with parts \(A_i,D_i\), has
> \[
>                         |D_i|\ge |A_i|+1.             \tag{3.1}
> \]
> Consequently \(B\) is either
>
> 1. connected, with \(|D|-|A|=2\); or
> 2. the disjoint union of exactly two components, each satisfying
>    \(|D_i|-|A_i|=1\).

### Proof

A maximum matching of \(H\) saturates every vertex of \(A\), so its
restriction to \(B_i\) saturates \(A_i\) into distinct vertices of
\(D_i\).  Hence \(|D_i|\ge|A_i|\).

If equality held, every matching saturating \(A_i\) would also saturate
every vertex of \(D_i\).  No vertex of \(D_i\) could then be exposed by
a maximum matching of \(H\), contradicting the definition of the
canonical set \(D\).  This proves (3.1).

Summing over the components and using (2.1) gives
\[
       \sum_i\bigl(|D_i|-|A_i|\bigr)=2.
\]
Every summand is a positive integer, yielding exactly the two listed
possibilities. \(\square\)

The components of \(J\) are obtained from the one or two components of
\(B\) by adjoining the vertices of \(U\) and their \(D\)--\(U\) edges.
Thus \(J\) can be connected even when \(B\) has two components.

## 4. The disconnected cross graph is exactly a Tait trap

The following theorem completely resolves one side of the target.

> **Theorem 4.1 (disconnected cross graph).**  If \(J=G-T\) is
> disconnected, then:
>
> 1. \(J\) has exactly two connected components;
> 2. each of the three edges \(r_1,r_2,e\) joins those two components;
> 3. \(G\) is bipartite, hence Tait-colourable;
> 4. for every maximum matching \(P\) of \(H\),
>    \(G-(R\cup P)\) has a dumbbell core, with \(e\) on its link.

### Proof

Contract every connected component of \(J\) to one vertex, retaining
the three edges of \(T\), including loops if both endpoints lie in one
component.  Call the resulting multigraph \(\Gamma\).

For any nonempty proper union \(X\) of components of \(J\), every edge
of \(\delta_G(X)\) belongs to \(T\).  Three-edge-connectivity of \(G\)
therefore gives
\[
                         |\delta_\Gamma(X)|\ge3.        \tag{4.1}
\]
The whole multigraph \(\Gamma\) has only three edges.  If it has more
than one vertex, (4.1) forces it to consist of exactly two vertices
joined by all three edges.  There can be no loop.  This proves the
first two assertions.

Give \(J\) its bipartition \((D,W)\), and reverse the two bipartition
classes in one of its two components.  Every edge of \(J\) remains
bichromatic.  Every edge of \(T\) originally had both endpoints in
\(W\), but it joins the two components; after the reversal, its
endpoints have opposite colours.  This is a bipartition of \(G\).
König's line-colouring theorem gives a proper three-edge-colouring of
the cubic bipartite graph \(G\).

It remains to identify the rooted complements.  Since maximum
matchings of \(H\) use only \(A\)--\(D\) edges,
\[
                         G-(R\cup P)=J-P+e.             \tag{4.2}
\]
The edge \(e\) is the only edge of (4.2) between the two components of
\(J\), so it is a bridge.

For completeness, remove \(e\) from (4.2).  In each of the two shores,
the endpoint of \(e\) has odd degree one; all other vertices have even
degree two except for vertices of \(D\) exposed by \(P\), which have
degree three.  The handshaking lemma therefore says that each shore
contains an odd number of exposed vertices.  There are exactly two
exposed vertices in total, so each shore contains exactly one.  Thus
the bridge \(e\) separates the two branch vertices.  The two-core
dichotomy makes it the link of a loop--link--loop core. \(\square\)

The sharp ten-vertex control

```text
I?BeeOwM?
```

with roots \(\{2,5\}\) is precisely of this form: \(J\) has two
components, and the two roots plus the extra \(A\)--\(A\) edge join
them.  The graph is bipartite, not merely Tait-colourable.

Theorem 4.1 explains why local barrier rigidity and rotation closure
alone could not prove the focused result: a disconnected cross graph is
a genuine, completely exchange-closed all-dumbbell family, but it lies
on the Tait side of the desired implication.

## 5. Exact Tait-colouring state on a connected cross graph

Assume from now on that \(J\) is connected.  It is useful to state the
remaining colouring condition without ambiguity.

König's theorem supplies a proper edge colouring
\[
                         \phi:E(J)\longrightarrow\{1,2,3\}. \tag{5.1}
\]
Every vertex of \(D\) sees all three colours.  Since
\(|W|=|D|+2\), each colour is absent at exactly two vertices of \(W\),
counting a degree-one vertex as missing two colours.

### 5.1 Extra edge of type \(A\)--\(A\)

All six endpoints of the three edges in \(T\) have degree two in \(J\).
Each has a unique missing colour.  The colouring \(\phi\) extends to a
Tait colouring of \(G\) if and only if the two endpoints of every edge
of \(T\) have the same missing colour.

If this holds, colour each edge of \(T\) with its common missing colour.
The three colours on \(T\) are automatically distinct: each colour is
missing at exactly two \(W\)-vertices.

### 5.2 Extra edge of type \(A\)--\(U\)

Let \(u\in U\) be the common endpoint of \(e\) and one root.  The vertex
\(u\) has degree one in \(J\), so two colours are missing there.  The
other endpoint of \(e\) and the other endpoint of that root must miss
those two colours in opposite order.  The two endpoints of the
disjoint root must share the third missing colour.

Equivalently, \(\phi\) extends precisely when the missing-colour slots
at the five deficient \(W\)-vertices can be paired along the three
edges of \(T\), with the two edges incident with \(u\) receiving its two
different missing colours.

These conditions are both necessary and sufficient by the degree-three
condition at every vertex.  They turn Tait-colourability into a
three-colour boundary-state problem on one connected bipartite graph.

## 6. The one remaining lemma

Theorem 4.1 proves:
\[
                         J\text{ disconnected}
             \quad\Longrightarrow\quad
                         \text{all \(P\) dumbbell and \(G\) Tait}. \tag{6.1}
\]
Therefore any counterexample to the requested implication must satisfy
all of the following:

```text
J is connected;
B is either one surplus-two component or two surplus-one components
  joined inside J through vertices of U;
every A-saturating matching P makes J-P+e a dumbbell;
no 3-edge-colouring of J has the compatible missing-colour state
  described in Section 5.
```

The exact missing assertion is:

> **Connected cross-graph lemma.**  Under the cyclically
> 4-edge-connected singleton hypotheses, if every
> \(A\)-saturating matching \(P\) makes \(J-P+e\) a dumbbell, then the
> compatible missing-colour state of Section 5 exists.

Proving this lemma would prove (1.1).  Refuting it would give the
requested focused counterexample.  The alternating-exchange arguments
presently available do not prove it: a matching chord across a
dumbbell-link cut can destroy that bridge while creating a different
bridge, and connectedness of \(J\) alone does not control that migration.

It would be unsound to infer the connected cross-graph lemma from the
finite theta censuses.  This memo therefore stops at the exact reduction
rather than claiming the target theorem.

## 7. AI-use disclosure

The reduction and exposition were developed with substantial assistance
from OpenAI Codex under human direction.  Lemmas 2.1 and 3.1 and
Theorem 4.1 are written out in full and require no computational
assumption.  No AI-generated argument or finite experiment is presented
as a proof of the connected cross-graph lemma, the one-boundary-five
case, or the Five-Cycle Double Cover Conjecture.
