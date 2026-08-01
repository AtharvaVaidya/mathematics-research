# Rectangle projection and the typed-cap orbit frontier

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE ALGEBRA / COMPLETE PYTHON CENSUS THROUGH ORDER
12 / SUPPLEMENTAL C++ CENSUS AT ORDER 14 / EXACT ORBIT COUNTEREXAMPLES /
NOT A PROOF OF FIVECDC**.

## 1. `D5` flows as triangle maps

Write a weight-two vector of \(\mathbb F_2^5\) as the edge joining its two
nonzero coordinate positions in \(K_5\).  At a cubic vertex, three
weight-two labels have xor zero if and only if they are the three distinct
edges of a triangle of \(K_5\).  Indeed, if two labels are \(x,y\), then
the third is \(x\mathbin\triangle y\); it has weight two precisely when
\(|x\cap y|=1\).  Thus a `D5` flow is equivalently an edge map to
\(E(K_5)\) which sends every cubic vertex-star to a triangle.

For a coordinate pair \(P\), the factor \(Y_P\) is the inverse image of
the \(2:3\) cut \(\delta_{K_5}(P)\).  This explains both vertex parity and
the important limitation: the label equations are local, but membership
of two graph edges in one component of \(Y_P\) is global connectivity
data.

## 2. Four coordinates are exactly the Tait boundary

> **Proposition 2.1.** A loopless cubic graph has a Tait colouring if and
> only if it has a `D5` flow whose labels collectively use at most four
> coordinate names.

**Proof.**  A Tait colouring with colours \(A,B,C\) becomes the `D5` flow
\(A\mapsto01\), \(B\mapsto02\), \(C\mapsto12\).

Conversely, inject the at most four used coordinate names into the four
elements of \(\mathbb F_2^2\).  Colour a label \(uv\) by
\(\phi(u)+\phi(v)\).  At a cubic vertex the labels are
\(uv,uw,vw\) for distinct \(u,v,w\).  Their colours are the three pairwise
differences of three distinct points of \(\mathbb F_2^2\), hence are the
three distinct nonzero vectors.  This is a proper 3-edge-colouring.
\(\square\)

Consequently every `D5` flow on a non-Tait graph uses all five coordinate
names.  This support fact alone says nothing about factor-component
connectivity; it must not be promoted to an external-port theorem.

## 3. The exact rectangle projection for one physical port

Normalize the cap labels in physical order to

\[
                         q(a)=01,\qquad q(b)=02,\qquad q(c)=12.
\]

The four external factors through physical port \(a\) are

\[
                         Y_{03},Y_{04},Y_{13},Y_{14}.              \tag{1}
\]

For a label \(x\), record its membership in these four factors:

\[
 \pi(x)=(x_0+x_3,x_0+x_4,x_1+x_3,x_1+x_4).                       \tag{2}
\]

Direct substitution gives

| label | \(\pi\) | label | \(\pi\) |
|:--:|:--:|:--:|:--:|
| `01` | `1111` | `02` | `1100` |
| `03` | `0110` | `04` | `1001` |
| `12` | `0011` | `13` | `1001` |
| `14` | `0110` | `23` | `1010` |
| `24` | `0101` | `34` | `1111` |

The image is exactly the seven nonzero words of the even-weight code
\(E_4\cong\mathbb F_2^3\).  Since (2) is linear, the three projected edge
values at every cubic vertex xor to zero.  Thus every `D5` flow induces a
nowhere-zero \(\mathbb F_2^3\)-flow under this projection.  Its four
coordinate even subgraphs are exactly (1), and the cap triangle projects
to

\[
                              1111,1100,0011.                     \tag{3}
\]

> **Proposition 3.1 (rectangle criterion).**  In the normalized flow,
> physical port \(a\) has an external state with root \(r\) if and only if
> \(a,r\) lie in one component of at least one of the four coordinate
> even subgraphs of the projected flow (2).

**Proof.**  The four coordinate supports are precisely the four factors
in (1).  By (3), all four contain \(a\); the first two leave `12` inactive
and the last two leave `02` inactive.  Those inactive labels are disjoint
from the respective factor pairs, so these and only these components give
external states through \(a\). \(\square\)

This is the exact code/flow formulation of a missing external port.  In a
fixed flow, failure gives four coordinate circuits through `a`, none of
which contains `r`.  If \(S_i\) is the vertex set of such a circuit, every
edge of \(\delta(S_i)\) has zero in coordinate \(i\) of (2).  The four
factor supports also have xor zero.  These four circuit/cut incidences are
a finite obstruction template, but not a contradiction: the independently
checked Petersen--Foster fixed flow in the companion package realizes the
template in a simple 3-edge-connected non-Tait graph of girth ten.

### Exact action of a Kempe switch

All `D5` labels lie in the four-dimensional even subspace

\[
 V=\{x\in\mathbb F_2^5:\textstyle\sum_i x_i=0\}.
\]

The dot product is a nondegenerate alternating form on \(V\), and the
indicator of \(Y_P\) on an edge is \(q(e)\mathbin\cdot P\).  Let \(D\) be
one circuit component of \(Y_T\), and transpose the two coordinates of
\(T\) on \(D\).  Since every label on \(D\) meets \(T\) oddly,

\[
                 q'(e)=q(e)+T\,1_D(e).                            \tag{4}
\]

Taking the dot product with any factor pair \(P\) gives the exact law

\[
Y_P(q')=
 \begin{cases}
  Y_P(q)\mathbin\triangle D,&|P\cap T|=1,\\
  Y_P(q),&|P\cap T|=0\text{ or }2.
 \end{cases}                                                       \tag{5}
\]

Applying the rectangle map to (4) gives

\[
                    \pi(q')=\pi(q)+\pi(T)1_D.                    \tag{6}
\]

Thus a `D5` Kempe move projects to addition of one constant nonzero
\(E_4\)-value along one circuit.  The projected flow alone does not always
determine which circuit may be switched.  If
\(p=\pi(q)=(p_0,p_1,p_2,p_3)\), then

\[
\begin{array}{c|cccccc}
T&03&04&13&14&01&34\\ \hline
Y_T&p_0&p_1&p_2&p_3&p_0+p_2&p_0+p_1.
\end{array}                                                        \tag{7}
\]

Put \(h=q_0+q_2\).  The four remaining supports are

\[
Y_{02}=h,\quad Y_{12}=h+p_0+p_2,\quad
Y_{23}=h+p_0,\quad Y_{24}=h+p_1.                                  \tag{8}
\]

The map \(q\mapsto(p,h)\) is a linear isomorphism
\(V\to\mathbb F_2^4\).  Equations (6)--(8) are therefore a complete
four-bit description of the move, not merely a lossy analogy.  They also
show why a proof using only the visible rectangle can miss switches whose
pair contains coordinate `2`.

### Gluing needs no common orbit

> **Proposition 3.2 (two externally covering shores glue).** If the
> aggregate external states of each of two rooted caps cover all three
> physical ports, the two caps glue root-good.  The witnesses may be in
> unrelated Kempe orbits and may be different flows on each shore.

**Proof.**  An external pair-state set covering three ports contains at
least two of the three edges of the physical port triangle.  Two such
pair sets intersect.  Choose a common physical pair and one external
witness on each shore.  Normalize the two connector triangles
independently; the unused-coordinate transposition aligns the two external
factor names without changing the connector labels.  The typed-port gluing
lemma then applies. \(\square\)

## 4. Three strict orbit strengthenings are false

A component-Kempe switch transposes coordinates \(i,j\) on one component
of \(Y_{ij}\).  The exact typed signature may be restricted to one such
Kempe orbit.

Take the Wagner graph in graph6 form

```text
GCrb`o
```

with lexicographic edge list

```text
(0,3) (0,4) (1,4) (0,5) (1,5) (2,5)
(1,6) (2,6) (3,6) (2,7) (3,7) (4,7).
```

The literal `D5` flow, in that edge order, is

```text
03 05 06 06 03 05 05 03 06 06 05 03.
```

For cap `z=0` and root edge `r=7=(2,6)`, its complete 13-state Kempe orbit
has exact typed mask

```text
46 = {ab-out, ac-in, ac-out, bc-out}.
```

It has no double star.  Hence the proposed strengthening “every nonempty
Kempe orbit supplies a double star” is false, even for a biconnected simple
cubic graph on eight vertices.  Notice that all three physical ports are
nevertheless externally covered: the three external bits are present.

The next strengthening asks for one flow in each orbit whose external
states cover all three ports simultaneously.  It first fails at order 12:

```text
graph6  K?`@EQgLAcAo
cap     z=0
root    r=15=(3,11)
flow    03 0c 05 05 14 11 06 14 12 11 05 14 18 0c 14 09 18 11
```

Its complete 144-state orbit has aggregate typed mask `47`, so all three
external states occur somewhere in the orbit.  Nevertheless the external
physical masks of its individual states have exact distribution

```text
mask 0: 72 states;  mask 1: 24;  mask 2: 24;  mask 4: 24.
```

No state has two external physical pairs.  This is only an orbit
counterexample: among all 498 flows modulo \(S_5\), the literal flow

```text
03 05 05 05 03 06 06 03 05 06 0a 0c 06 12 14 18 09 11
```

has fixed typed mask `10`, consisting of external states on two physical
pairs, and therefore covers all three ports.

Even aggregate external coverage by every orbit fails at order 14:

```text
graph6  M??CBAPqB_B_H_B_?
cap     z=7
root    r=19=(5,13)
flow    03 05 0c 11 18 09 12 03 11 06 14 12 0a 12 18 18 12 0a 03 0a 09
```

Its complete 12-state orbit has exact typed mask

```text
23 = {ab-in, ab-out, ac-in, bc-in}.
```

Ten states have fixed external physical mask `1` and two have mask `0`.
Thus only `ab` is externally realized anywhere in the orbit.  Again this
does not refute the all-flow target: the same graph/interface has the
literal flow

```text
03 03 05 05 03 06 06 05 03 06 03 05 06 0a 0c 06 14 12 09 18 11
```

with fixed typed mask `42` and external physical mask `7`.

The order-12 delimiter has girth three and a cyclic two-edge cut.  The
order-14 delimiter is Tait-colourable, has girth four, edge-connectivity
three, and cyclic edge-connectivity four.  Hence neither lies in the
non-Tait marked-girth cap branch.  What they prove is exact: unrestricted
Kempe-orbit universality cannot be used as an intermediate lemma.

## 5. Exact finite hierarchy through order fourteen

For every graph generated by

```text
geng -Cq -d3 -D3 n
```

at even orders \(4\le n\le12\), `verify.py` independently:

1. decodes and checks the biconnected simple cubic graph;
2. enumerates all `D5` flows modulo global \(S_5\);
3. reconstructs every component-Kempe orbit;
4. computes its exact six-state signature for every cap vertex and every
   proper root edge;
5. distinguishes double-star containment, aggregate external coverage
   inside an orbit, and a simultaneous externally covering flow inside an
   orbit; and
6. checks separately whether some flow across all orbits simultaneously
   covers all three ports.

The exact totals are:

| order | graphs | flows / \(S_5\) | orbits / \(S_5\) | orbit interfaces | no double star | no orbit union | no simultaneous orbit flow | no simultaneous all-flow witness |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 2 | 2 | 24 | 0 | 0 | 0 | 0 |
| 6 | 2 | 13 | 12 | 432 | 0 | 0 | 0 | 0 |
| 8 | 5 | 128 | 35 | 2,520 | 56 | 0 | 0 | 0 |
| 10 | 18 | 1,525 | 323 | 38,760 | 161 | 0 | 0 | 0 |
| 12 | 81 | 25,960 | 2,650 | 477,000 | 7,072 | 0 | 2 | 0 |

The optional C++ order-14 census uses the already frozen orbit engine and
checks all 480 graphs, 537,418 flows modulo \(S_5\), 33,102 orbits, and
8,341,704 orbit interfaces.  It finds four orbit-union failures and 72
orbit-simultaneous failures, but zero all-flow-simultaneous failures.  Its
external-pair mask distribution is

```text
1:4, 3:886022, 5:932438, 6:883918, 7:5639322.
```

Thus the surviving finite statement is exactly:

> Through order 14, every rooted interface of every biconnected simple
> cubic graph has at least one `D5` flow which simultaneously realizes
> external states covering all three physical ports.

The complete through-order-12 result has the independent standard-library
Python implementation in this package.  The order-14 extension uses one
C++ implementation, including the previously audited orbit engine, so it
is not promoted to an independently replayed theorem.

The universal *all-flow existence* statement remains open.  Proposition
3.2 shows that it would be enough for three-cut gluing, and in fact the
weaker aggregate-all-flow external coverage would suffice.  The orbitwise
versions are now disproved.  The finite all-flow census is evidence for
the exact remaining premise, not a proof and not a FiveCDC resolution.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the rectangle and hidden
coordinate projections, derived the exact switch law, found the three
orbit delimiters, ran the finite frontiers, implemented the checkers, and
drafted this note.  The retained algebra and literal witnesses are
human-checkable.  The order-bounded censuses are computer-assisted; the
order-14 extension has not received an independently written full replay.
Human peer review is required before citation.
