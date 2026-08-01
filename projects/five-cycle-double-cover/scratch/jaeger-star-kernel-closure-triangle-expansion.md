# Triangle expansion for the Jaeger star kernel-closure property

Date: 2026-07-28

Status: **HUMAN CONTRACTION THEOREM / INFINITE COUNTERMODEL FAMILY FOR
THE CLOSURE STRENGTHENING / EXPLICIT LIFTING NO-GO / NOT A FIVE-CDC
RESULT**.

## 1. Triangle contraction preserves closure-goodness downward

Let \(G^\triangle\) be a simple cubic graph, let
\(\Delta=abc\) be a triangle, and let \(G\) be obtained by contracting
\(\Delta\) to one vertex \(z\).  Fix a star root
\(r\notin V(\Delta)\).

Suppose \(T_0,T_1,T_2\) form a star-fibre packing in \(G^\triangle\).
Every triangle edge has multiplicity two, so the total number of
triangle-edge occurrences in the three trees is six.  A tree contains
at most two edges of a triangle.  Consequently,
\[
                    |T_i\cap E(\Delta)|=2
                    \qquad(i=0,1,2).                          \tag{1}
\]
Contracting the two triangle edges in each \(T_i\) therefore gives a
spanning tree \(\bar T_i\) of \(G\).  Edge multiplicities outside the
triangle do not change, so the \(\bar T_i\) form the same star fibre at
\(r\).

For every tree edge \(e\notin E(\Delta)\), one side of
\(T_i-e\) becomes one side of \(\bar T_i-e\) after two vertices are
removed.  Its order has the same parity.  Hence
\[
 e\in K(T_i)\quad\Longleftrightarrow\quad
 e\in K(\bar T_i) \qquad(e\notin E(\Delta)).                  \tag{2}
\]

Now suppose the packing upstairs is closure-good in coordinate \(k\).
If
\[
 e\in K(\bar T_i)\cap K(\bar T_j),
 \qquad \{i,j,k\}=\{0,1,2\},
\]
then (2) puts the corresponding external edge in
\(K(T_i)\cap K(T_j)\).  Its endpoints are joined by a \(K(T_k)\)-path.
Contracting the triangle maps that path to a
\(K(\bar T_k)\)-walk, and hence to a path.  Thus
\[
 K(\bar T_i)\cap K(\bar T_j)
       \subseteq\operatorname{cl}_G K(\bar T_k).
\]

This proves:

> **Triangle-contraction theorem.**  For a root outside the expanded
> triangle, every closure-good star packing contracts to a
> closure-good star packing.

The contrapositive is the useful direction: triangle expansion at any
nonroot vertex preserves failure of the closure strengthening.

## 2. Simplicity and 3-edge-connectivity

Expanding a vertex of a simple cubic graph into a triangle clearly
preserves simplicity and cubicity.

It also preserves 3-edge-connectivity.  Let a cut of size at most two
split the new triangle.  If one triangle vertex is on one shore, move
the contracted vertex to that shore; the two crossing triangle edges
are replaced in the contracted graph by the two external edges at the
other triangle vertices.  If two triangle vertices are on the shore,
use the complementary version of the same argument.  In either case a
cut of size at most two descends to the contracted graph.  A cut not
splitting the triangle descends without change.  This contradicts
3-edge-connectivity downstairs.

Starting from the certified 16-vertex rooted countermodel

```text
O??CA?_ceOGgH_F?AK@P? , root 13,
```

and repeatedly triangle-expanding any vertex other than the fixed root
therefore gives a recursively defined infinite family of simple cubic
3-edge-connected rooted graphs with no closure-good star packing.
Their orders are \(16+2t\), \(t\ge0\).

This is an infinite counterexample family only for the **kernel-closure
strengthening**.  It says nothing negative about the exact
component-parity lemma or Five-CDC.

## 3. Exact local lifting law

The converse of the contraction theorem is false.  The reason can be
seen without computation.

Let a tree \(\bar T\) of the contracted graph be expanded by omitting
triangle edge \(ac\), so its two new tree edges form the path
\[
                              a-b-c.
\]
For \(x\in\{a,b,c\}\), let \(b_x\) be one if the external edge at \(x\)
belongs to \(K(\bar T)\), and zero otherwise.  At the contracted vertex
\[
                         b_a+b_b+b_c=1\pmod2.                 \tag{3}
\]
Membership of every external edge in the odd forest is unchanged.
Odd incidence at the three new vertices then uniquely gives
\[
\begin{split}
 1_{ab\in K(T)}&=1+b_a,\\
 1_{bc\in K(T)}&=1+b_c
\end{split}
\qquad\pmod2.                                                 \tag{4}
\]
The middle equation follows from (3).

In particular, if all three external edges at \(z\) belong to
\(K(\bar T)\), then neither new path edge belongs to \(K(T)\).
The one \(K(\bar T)\)-component passing through \(z\) splits into three
components upstairs.  An edge closed by a path through \(z\) can
therefore cease to be closed under **every** lift.

## 4. A literal six-lift no-go

Contract the triangle \(\{0,6,9\}\) in the 16-vertex countermodel.  In
canonical graph6 form the quotient is

```text
MC?A@BGPdGB_CoIO?
```

and the old root is vertex 11.  In the quotient edge order, the
following packing is closure-good in coordinate two:

```text
T0 = 1 2 3 5 6 9 10 11 12 15 16 17 20
T1 = 0 2 4 6 7 8 10 11 14 15 17 18 19
T2 = 0 1 3 4 5 7 8 9 13 16 18 19 20
```

At the contracted vertex, the incident edge indices are \(0,3,9\),
and the three odd-forest traces are

```text
K0 trace = 9
K1 trace = 0
K2 trace = 0 3 9
```

Thus coordinate two has the \(111\) local pattern described after
(4).  Its unique common edge \(K_0\cap K_1\) is edge 10.  The
\(K_2\)-path closing that edge passes through the contracted vertex.

There are exactly six legal lifts, one for each bijection between the
three coordinates and the omitted triangle edge.  Direct application
of (4), followed by the component test, gives

```text
closure vector downstairs  (false, false, true)
closure vector of each of the six lifts
                           (false, false, false)
```

This is a precise counterexample to any claim that every
closure-good packing of a triangle contraction has a closure-good
lift.

The standard check is:

```sh
python3 scratch/verify_jaeger_star_kernel_closure_triangle_expansion.py
```

It reconstructs the quotient, verifies the three quotient trees and
their closure vector, constructs all six lifted tree packings, and
checks their odd forests and closure vectors without a SAT solver.

## 5. Why the 16-vertex graph is a Petersen expansion

The countermodel has the three disjoint triangles
\[
 \{0,6,9\},\qquad \{1,7,11\},\qquad \{2,8,15\}.
\]
Contracting all three gives the Petersen graph.  Relative to the image
of root 13, the six vertices at distance two induce a 6-cycle, and the
three expanded vertices form one alternating class of that cycle.

This description is canonical.  In the 2-subset model of Petersen, fix
the root \(\{1,2\}\).  The distance-two vertices are
\[
 (1,3),(1,4),(1,5),(2,3),(2,4),(2,5),
\]
and adjacency makes them a 6-cycle.  Its alternating independent
classes are the three vertices with first entry 1 and the three with
first entry 2.  The stabilizer of the root contains the transposition
\((1\,2)\), so it interchanges the two classes.  Since the automorphism
group is root-transitive, all pairs

```text
(root r, one alternating class in the distance-two C6 from r)
```

form one orbit.  There are exactly \(10\cdot2=20\) such rooted
Petersen triple expansions, and every one is rooted-isomorphic to the
certified countermodel.

This explains the obstruction more concretely than the raw graph6
string: three separated triangle expansions split the odd-forest
connectivity needed by the closure strengthening, while leaving the
weaker quotient boundary even.

## 6. Roots inside the triangle

Ordinary contraction does not transport the relevant star fibre when
the root lies inside the expanded triangle.  If \(r=a\), the triangle
edge multiplicities are
\[
 m(ab)=1,\qquad m(ac)=1,\qquad m(bc)=2,
\]
so the three trees contain only four triangle-edge occurrences in
total.  Contracting a tree to a tree would require two triangle edges
in each coordinate, hence six occurrences.  Therefore at least one
coordinate does not contract to a tree.

The outside-root theorem above is exact; it should not be extended to
inside-root expansions.  Empirical failures when the expanded vertex
itself is used as root require a different argument and are not part
of the infinite-family theorem proved here.

## AI-use disclosure

OpenAI Codex, under human direction, derived and checked the
contraction theorem, local lifting law, explicit six-lift obstruction,
Petersen orbit description, and infinite family.  These results concern
only a discarded sufficient strengthening of the Jaeger route.  No
resolution of Five-CDC is claimed.
