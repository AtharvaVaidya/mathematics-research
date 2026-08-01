# Human-checkable proof and trust boundary

## 1. Scope and exact move

Let \(G\) be a finite graph and let
\(f,g:E(G)\to\mathbb F_2^3\) be nowhere-zero flows.  At every vertex,
the sum over edge incidences is zero.  A loop contributes twice, hence
zero, in characteristic two.  Parallel edges are separate coordinates.

A **fixed-value Eulerian move** chooses a nonzero
\(a\in\mathbb F_2^3\) and an Eulerian edge-set \(C\), and replaces
\[
 f\quad\text{by}\quad f+a\,1_C.
\]
Here Eulerian means that every vertex has even degree in \(C\); \(C\)
need not be connected.  Since \(1_C\) is a binary flow, the result is
again a flow.  A move is **legal** if its resulting flow is
nowhere-zero.

The algebraic statements below allow loops and parallel edges under
these conventions.  Both finite witnesses and every smallness claim in
this package are restricted to connected simple cubic graphs.

## 2. Unrestricted distance equals difference-value rank

Put \(h=f+g\) and
\[
 W=\operatorname{span}\{h(e):e\in E(G)\}.
\]

**Theorem 1.**  If intermediate zero values are allowed, the minimum
number of fixed-value Eulerian moves taking \(f\) to \(g\) is
\(\dim W\).

**Proof.**  Suppose \(k\) moves use constants \(a_1,\ldots,a_k\).
Every final difference value \(h(e)\) is the sum of those \(a_i\) whose
move contains \(e\).  Thus every \(h(e)\) lies in
\(\operatorname{span}\{a_1,\ldots,a_k\}\), and
\(\dim W\leq k\).

Conversely, choose a basis \(a_1,\ldots,a_r\) of \(W\), and write
\[
 h(e)=\sum_{i=1}^r \lambda_i(e)a_i.
\]
For each \(i\), put \(C_i=\{e:\lambda_i(e)=1\}\).  The coordinate
function \(\lambda_i\circ h\) is a binary flow because \(h\) is a
flow.  Hence \(C_i\) is Eulerian.  Adding \(a_i\) on \(C_i\), for all
\(i\), adds exactly \(h\) and reaches \(g\). \(\square\)

This is a fixed-value decomposition, not the usual cycle-rank bound:
the number of moves is at most three for \(\mathbb F_2^3\), independent
of the cycle-space dimension.

## 3. Exact rank-two legality criterion

Assume \(\dim W=2\), and write
\[
 W\setminus\{0\}=\{a,b,a+b\},\qquad
 H_w=\{e:h(e)=w\}.
\]

For the ordered basis \((a,b)\), Theorem 1's two edge-sets are forced:
\[
 X_a=H_a\cup H_{a+b},\qquad
 X_b=H_b\cup H_{a+b}.
\]
Both are Eulerian.

**Theorem 2.**  The ordered two-move factorization
\[
 f\xrightarrow{\,a,X_a\,}f+a1_{X_a}
  \xrightarrow{\,b,X_b\,}g
\]
is legal if and only if
\[
 H_{a+b}\cap f^{-1}(a)=\varnothing. \tag{1}
\]
Some legal two-move factorization exists if and only if (1) holds for
at least one of the six ordered pairs of distinct nonzero vectors in
\(W\).  All six orders are blocked if and only if all six directed
transitions
\[
 (f(e),g(e))=(u,v),\qquad
 u,v\in W\setminus\{0\},\ u\ne v,
\]
occur on edges of \(G\).

**Proof.**  After the first move, only an edge of \(X_a\) can become
zero.  If \(e\in H_a\) and \(f(e)=a\), then
\(g(e)=f(e)+h(e)=0\), impossible.  If
\(e\in H_{a+b}\), the intermediate value is zero exactly when
\(f(e)=a\).  This proves (1); the endpoint is \(g\), which is
nowhere-zero.

For uniqueness, any two-move representation uses constants \(c,d\).
Since the values of \(h\) span a two-dimensional space, \(c,d\) are an
ordered basis of \(W\).  Membership in the two move-sets is then the
unique pair of coordinates of \(h(e)\) in that basis, forcing the two
sets displayed above.  Finally, a blocker for order \((a,b)\) is an
edge with \(h(e)=a+b\) and \(f(e)=a\), equivalently
\((f(e),g(e))=(a,b)\). \(\square\)

Rank at most two is also equivalent to the existence of a nonzero
linear functional \(q\) satisfying
\[
 q(f(e))=q(g(e))\quad\text{for every edge }e.
\]
Thus the two flows share a binary coordinate cycle.  That observation
is the link to coordinate-preserving good-flow selection.

## 4. Smallest connected simple-cubic obstruction

Use graph6 record `EFz_`, namely \(K_{3,3}\), with the following edge
order and values.  Integers \(1,\ldots,7\) encode the corresponding
three-bit vectors.

| edge | endpoints | \(f\) | \(g\) | \(h=f+g\) |
|---:|:---:|---:|---:|---:|
| 0 | 0--3 | 1 | 1 | 0 |
| 1 | 1--3 | 2 | 3 | 1 |
| 2 | 2--3 | 3 | 2 | 1 |
| 3 | 0--4 | 2 | 2 | 0 |
| 4 | 1--4 | 3 | 1 | 2 |
| 5 | 2--4 | 1 | 3 | 2 |
| 6 | 0--5 | 3 | 3 | 0 |
| 7 | 1--5 | 1 | 2 | 3 |
| 8 | 2--5 | 2 | 1 | 3 |

At every vertex the three values of each flow XOR to zero.  The
difference values span \(\{0,1,2,3\}\), and the six changed edges
realize
\[
 (1,2),(1,3),(2,1),(2,3),(3,1),(3,2).
\]
Theorem 2 therefore blocks every two-move order.

There is nevertheless this legal three-move path:

| move | constant | Eulerian edge-set |
|---:|---:|:---|
| 1 | 4 | \(\{1,2,4,5\}\) |
| 2 | 3 | \(\{1,2,7,8\}\) |
| 3 | 6 | \(\{1,2,4,5\}\) |

The two intermediate flows are
```
(1,6,7,2,7,5,3,1,2)
(1,5,4,2,7,5,3,2,1).
```
Every entry is nonzero.  The unrestricted lower bound is two and every
legal two-move factorization is blocked, so the legal distance is
exactly three.

This is smallest among connected simple cubic graphs.  Such a graph
has even order at least four.  At order four the only graph is \(K_4\).
If all six rank-two orders were blocked on its six edges, both flows
would use only the three nonzero values of \(W\) and hence would be
proper 3-edge-colourings.  The three colour classes of \(K_4\) are its
unique three perfect matchings.  Therefore the second colouring is a
permutation of the first.  A permutation with no fixed colour is a
3-cycle and realizes only three directed colour transitions, each
twice—not all six.  This contradiction rules out \(K_4\).
The checker additionally exhausts all 210 nowhere-zero
\(\mathbb F_2^3\)-flows of \(K_4\).

## 5. Bad-to-good shared-coordinate countermodel

Use graph6 record `G?zTb_`, the cube, with this edge order:

| edge | endpoints | \(f\) | \(g\) | \(h=f+g\) |
|---:|:---:|---:|---:|---:|
| 0 | 0--4 | 6 | 4 | 2 |
| 1 | 1--4 | 5 | 5 | 0 |
| 2 | 2--4 | 3 | 1 | 2 |
| 3 | 0--5 | 1 | 3 | 2 |
| 4 | 1--5 | 3 | 2 | 1 |
| 5 | 3--5 | 2 | 1 | 3 |
| 6 | 0--6 | 7 | 7 | 0 |
| 7 | 2--6 | 1 | 2 | 3 |
| 8 | 3--6 | 6 | 5 | 3 |
| 9 | 1--7 | 6 | 7 | 1 |
| 10 | 2--7 | 2 | 3 | 1 |
| 11 | 3--7 | 4 | 4 | 0 |

The difference span is \(\{0,1,2,3\}\).  For each ordered basis, the
checker finds the following blocker:

| order | blocker edge |
|:---:|---:|
| (1,2) | 7 |
| (1,3) | 3 |
| (2,1) | 5 |
| (2,3) | 10 |
| (3,1) | 2 |
| (3,2) | 4 |

The functional \(q(x)=\langle 4,x\rangle\) annihilates the difference,
so both flows have the same nonempty coordinate cycle
\[
 \{0,1,6,8,9,11\},
\]
which is a six-edge circuit in the cube.

For a nowhere-zero flow \(p\), a nonzero functional \(q\), and a value
\(m\) with \(q(m)=1\), put
\[
 F_q=\{e:q(p(e))=1\},\qquad
 Z_m=\{\text{endpoints of edges in }p^{-1}(m)\}.
\]
Call \((q,m)\) good when every component of \(G-F_q\) contains an even
number of vertices of \(Z_m\).  After an invertible change of
coordinates, this is exactly the condition in Hušek--Šámal,
Theorem 3.16.

For \(f\), each of the 28 possible pairs \((q,m)\) has exactly two
component defects, so \(f\) is bad for every coordinate choice.  For
\(g\), the 16 good pairs are
```
(2,2) (2,3) (2,6) (2,7)
(3,1) (3,2) (3,5) (3,6)
(4,4) (4,5) (4,6) (4,7)
(5,1) (5,3) (5,4) (5,6).
```
For example, with \(q=2\), the two components of \(G-F_q\) are
\(\{0,1,2,4\}\) and \(\{3,5,6,7\}\), and all four eligible matching
values have zero component defects.  Thus \(g\) induces a
five-cycle double cover by the cited theorem.

An exact legal three-move path from \(f\) to \(g\) is:

| move | constant | Eulerian edge-set |
|---:|---:|:---|
| 1 | 1 | \(\{0,1,4,5,6,8\}\) |
| 2 | 2 | \(\{0,2,3,5,7,8\}\) |
| 3 | 1 | \(\{0,1,6,7,9,10\}\) |

The intermediate flows are
```
(7,4,3,1,2,3,6,1,7,6,2,4)
(5,4,1,3,2,1,6,3,5,6,2,4).
```
All entries are nonzero.  Theorem 2 and the blocker table make the
legal distance exactly three.

The checker enumerates every nowhere-zero flow on all connected simple
cubic graphs through order six:

| graph6 | graph | total flows | component-parity good |
|:---:|:---|---:|---:|
| `C~` | \(K_4\) | 210 | 210 |
| `EFz_` | \(K_{3,3}\) | 1,092 | 1,092 |
| `EUxo` | triangular prism | 1,050 | 1,050 |

These are the complete elementary graph list at orders four and six
(the complement of a cubic graph on six vertices is 2-regular).
Therefore the cube witness is smallest among connected simple cubic
bad-to-good examples.  On the cube the checker finds 5,712 flows:
1,344 bad and 4,368 good.

For the displayed bad \(f\), the good targets have difference-rank
histogram
```
rank 1:   36
rank 2:  960
rank 3: 3372.
```
Of the 996 good targets of rank at most two, 992 admit a legal path of
length at most two; four, including the displayed \(g\), do not.
So the countermodel defeats arbitrary target selection, not an
existential choice of a clean target.

## 6. These graphs satisfy FiveCDC

The \(K_{3,3}\) flows displayed above use only \(1,2,3\), hence are
Tait colourings.  The cube has the explicit Tait colouring
```
(1,2,3,2,1,3,3,2,1,3,1,2).
```
For any such colouring, the unions of colour pairs
\(\{1,2\},\{1,3\},\{2,3\}\) are Eulerian and cover every edge exactly
twice.  Appending two empty Eulerian subgraphs gives a five-cycle double
cover.  The checker verifies this directly.

Thus neither graph is a FiveCDC counterexample, and no theorem here
resolves the conjecture.

## 7. Relation to the literature

The conventions and claims were compared directly against:

* L. Esperet, K. Hendrey, A. Lagoutte, M. Marseloo, S. Norin, and
  R. Steiner, *Nowhere-zero flow reconfiguration*,
  [arXiv:2512.17342v4](https://arxiv.org/abs/2512.17342).
  Their adjacency requires the support of a difference to be one
  connected 2-regular cycle.  Lemma 2.1 decomposes an arbitrary group
  flow into cycle-supported flows.  Observation 6.11 gives connectivity
  when two flows share a complementary projection that is nowhere-zero
  on every edge.
* D. W. Cranston, J. Li, B. Su, Z. Wang, and N. Xu,
  *Reconfiguration of Nowhere-zero Flows*,
  [arXiv:2606.24685v1](https://arxiv.org/abs/2606.24685).
  Their auxiliary graph \(\mathcal F^*\) allows a difference supported
  on an even subgraph; the values on that support need not be one fixed
  vector.
* R. Hušek and R. Šámal, *Exponentially Many Circuit Double Covers*,
  [arXiv:2607.24724v1](https://arxiv.org/abs/2607.24724).
  Definition 1.2 explicitly allows empty even subgraphs in a labelled
  \(k\)-cycle double cover.  Theorem 3.16 is the
  component-parity/\(Z\)-join criterion used here, and Conjecture 3.19
  states the equivalent good-flow selection problem.

Over \(\mathbb F_2^3\), our move has the same fixed-value pattern as
standard cycle adjacency but allows an arbitrary Eulerian edge-set,
possibly disconnected.  Relative to \(\mathcal F^*\), it is narrower in
value pattern because the added vector is fixed across the support.  A
legal such move decomposes into
legal standard cycle moves by splitting its support into edge-disjoint
circuits: at every intermediate stage each edge still has either its
old or its final nonzero value.  It is also an edge of
\(\mathcal F^*\), but not every \(\mathcal F^*\) edge is a fixed-value
move.

The exact difference-value-rank formula and rank-two blocker normal
form were not located in these papers or by exact-phrase web searches.
That is evidence of novelty, not a priority proof or an exhaustive
literature review.  The unrestricted argument is short enough to be
folklore.  The responsible claim is therefore **candidate novel
auxiliary result**, not “new field,” not a resolution, and not yet a
standalone publishable theorem without expert review.

## 8. Reproducibility and trust boundary

`verify.py` uses only the Python standard library.  It:

1. decodes each graph6 record and checks simplicity, cubicity,
   connectedness, and bridgelessness;
2. independently checks every displayed flow, Eulerian move, blocker,
   shared coordinate, and Tait-derived five-cycle double cover;
3. enumerates flows as triples of binary cycle-space elements;
4. performs the complete small-order census and cube census stated
   above.

The proof of Theorems 1 and 2 is human mathematics and does not depend
on the enumeration.  The minimal bad-to-good claim and numerical
censuses do depend on exhaustive computation, but the checker is short,
deterministic, and independently replayable.  This package contains no
SAT/UNSAT claim and needs no proof-logging certificate.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, derived the normal
form, searched the finite examples, wrote and ran the checker, performed
the literature comparison, and drafted this note.  No independent
human peer review has occurred.
