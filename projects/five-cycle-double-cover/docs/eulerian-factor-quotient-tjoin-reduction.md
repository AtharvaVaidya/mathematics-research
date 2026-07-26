# Eulerian factor quotients and the residual \(T\)-join lifting condition

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE QUOTIENT LEMMA / EXACT LIFTING
REFORMULATION / CONNECTED EIGHT-MARK BRANCH STILL OPEN**.

This note investigates the quotient obtained from the monochromatic-mark
two-factor in the connected exact-zero size-four branch.  The quotient is
indeed connected and Eulerian, and every connected Eulerian multigraph
packs two edge-disjoint \(T\)-joins for every even vertex set \(T\).
Those quotient joins do not automatically lift through the contracted
factor circuits.  Section 5 gives the exact additional local condition.

No finite computation is used.

## 1. Conventions

All graphs in the main statements are finite loopless multigraphs.
Parallel edge objects are retained.  Quotienting may create loops; a loop
has two incidences at its vertex and contributes two to degree.  It never
changes the boundary of an edge set.

For an edge set \(J\), write
\[
       \partial J=\{v:d_J(v)\text{ is odd}\}.
\]
A \(T\)-join is an edge set \(J\) with \(\partial J=T\).  Two joins are
edge-disjoint when they contain no common edge object.  They need not be
connected.

When a spanning two-factor \(F\) is contracted, the quotient is defined
directly from the partition of \(V(G)\) into the circuit components of
\(F\).  Every edge outside \(F\) is retained: it becomes a loop if its
ends lie on the same factor circuit and otherwise becomes an edge between
the corresponding quotient vertices.  This avoids any ambiguity from
performing a sequence of ordinary edge contractions around a circuit.

## 2. The monochromatic \(ac\)-factor

Use the connected branch of the marked-core expansion.  Thus:

- \(H\) is a connected Tait-colourable cubic graph;
- \(S\) is a universally separated matching of eight edges of \(H\);
- every \(s\in S\) is subdivided by a distinct terminal \(t_s\);
- a perfect matching \(M\) on the eight terminals supplies four new
  edges; and
- \(G-M\) is the subdivision of \(H\), so in particular it is connected.

Use mark precolouring to give every edge of \(S\) colour \(c\), and fix
the other two colours \(a,b\).  Lift the full \(ac\)-factor of \(H\)
through all eight subdivisions.  Call the resulting edge set \(F\).

At an old core vertex, the \(a\)- and \(c\)-edges give degree two in
\(F\).  At a terminal, the two halves of its subdivided \(c\)-edge give
degree two.  Hence \(F\) is a spanning two-factor of both \(G-M\) and
\(G\).

Every \(ac\)-circuit of the core has even length.  Universal separation
says that it contains at most one mark.  Therefore:

1. eight distinct components of \(F\) contain one terminal each and
   have odd length; and
2. every remaining component of \(F\) contains no terminal and has even
   length.

The complementary perfect matching of \(F\) in \(G\) consists exactly
of the lifted \(b\)-edges together with the four edges of \(M\).

## 3. The quotient is connected and Eulerian

Let \(Q=G/F\) be the factor quotient, retaining quotient loops and
parallel edges.  For a factor circuit \(C\), denote its quotient vertex
by \(q_C\).

Because \(F\) is a spanning two-factor in a cubic graph, every vertex of
\(C\) has exactly one incident complementary-matching edge.  Counting a
quotient loop twice,
\[
             d_Q(q_C)=|V(C)|.                         \tag{1}
\]
Consequently the odd-degree vertices of \(Q\) are precisely the eight
vertices corresponding to the terminal-containing factor circuits.

Let
\[
             \rho:T=\partial M\longrightarrow V(Q)
\]
send a terminal to the quotient vertex of its factor circuit.  Universal
separation puts different terminals on different factor circuits, so
\(\rho\) is injective.  Write
\[
             \overline T=\rho(T).
\]
Thus \(|\overline T|=8\).  The phrase “the eight quotient terminals”
means these eight distinct marked quotient vertices; the original
vertices of \(T\) have been contracted.

Every edge of \(M\) joins two different members of \(\overline T\), and
the four images of the \(M\)-edges form a matching on
\(\overline T\).  Put
\[
             R=Q-M.
\]

> **Factor-quotient lemma.**  \(R\) is a connected Eulerian
> multigraph.

**Proof.**  Deleting \(M\) removes one incidence at each vertex of
\(\overline T\) and none elsewhere.  Equation (1) says that the vertices
of \(\overline T\) had odd degree in \(Q\), while all other quotient
vertices had even degree.  Every degree in \(R\) is therefore even.

For connectivity, first delete \(M\) in the original graph.  The graph
\(K=G-M\) is connected by the connected-branch hypothesis.  Contracting
the connected factor circuits of \(F\subseteq K\) preserves
connectivity, and the resulting quotient is exactly \(R\). \(\square\)

Notice that connectedness does not follow merely from connectedness of
\(G\): deleting all four \(M\)-edges could in general disconnect it.
The required hypothesis is the connectedness of \(G-M\).

The same parity calculation can be made directly in \(R\).  At a factor
circuit \(C\), every nonterminal vertex has one incident edge represented
in \(R\), while its possible terminal has its complementary edge in
the deleted set \(M\).  Hence
\[
       d_R(q_C)=|V(C)|-|V(C)\cap T|,
\]
which is even for both an unmarked even circuit and a one-terminal odd
circuit.

## 4. Two \(T\)-joins in a connected Eulerian multigraph

> **Eulerian two-join lemma.**  Let \(R\) be a connected Eulerian
> multigraph, with loops and parallel edges allowed, and let
> \(U\subseteq V(R)\) have even cardinality.  Then \(R\) has two
> edge-disjoint \(U\)-joins.  In fact, the two joins can be chosen to
> partition \(E(R)\).

### Constructive proof

Choose a spanning tree \(A\) of \(R\), ignoring loops, and root it at
an arbitrary vertex.  For every nonroot vertex \(v\), put its parent edge
in \(J_1\) exactly when the rooted subtree below \(v\) contains an odd
number of vertices of \(U\).

This is the standard constructive \(U\)-join in a tree.  To check it
directly, let \(p_v\) be the parity of the number of \(U\)-vertices in
the subtree at \(v\).  At a nonroot vertex, the selected incident child
edges have parity \(\sum p_w\), and its parent edge has indicator \(p_v\).
Since
\[
       p_v=1_{\{v\in U\}}+\sum_{w\text{ child of }v}p_w
       \pmod2,
\]
the \(J_1\)-degree of \(v\) has parity \(1_{\{v\in U\}}\).  At the root,
the same conclusion follows from \(|U|\) being even.  Hence
\(\partial J_1=U\).

Now put
\[
             J_2=E(R)\setminus J_1.
\]
The full edge set of an Eulerian multigraph has empty boundary, including
when loops are present.  Boundary is linear under symmetric difference,
so
\[
       \partial J_2
       =\partial E(R)\mathbin\triangle\partial J_1
       =\varnothing\mathbin\triangle U
       =U.
\]
Thus \(J_1,J_2\) are edge-disjoint \(U\)-joins and partition all edges.
The construction is linear-time once a spanning tree is fixed.
\(\square\)

Applying the lemma to \((R,\overline T)\) produces two edge-disjoint
\(\overline T\)-joins in the quotient.  The next section explains why
this alone is not yet a pair of \(T\)-joins in \(G-M\).

## 5. Exact lifting through the factor circuits

Let
\[
             \pi:K=G-M\longrightarrow R
\]
be the contraction map.  Edges outside \(F\) correspond bijectively to
the edge objects of \(R\), including quotient loops.

Fix two edge-disjoint \(\overline T\)-joins
\(J_1,J_2\subseteq E(R)\).  Let \(\widehat J_i\) be the corresponding
sets of uncontracted edges in \(K-F\).

Here a lift of \(J_i\) means an edge set in \(K\) whose intersection with
\(E(K)\setminus E(F)\) is exactly \(\widehat J_i\).

For a factor circuit \(C\), define
\[
 A_i(C)=
 \{v\in V(C):
   \text{the complementary edge at \(v\) belongs to }\widehat J_i\}.
                                                               \tag{2}
\]
The complementary edge at a terminal belongs to \(M\), not to \(R\), so
no terminal enters \(A_i(C)\) by that edge.  If a selected quotient edge
is a loop at \(q_C\), its two original ends give two vertices of
\(A_i(C)\); this agrees with the loop's contribution two to quotient
degree.

To turn \(\widehat J_i\) into a \(T\)-join, choose an edge set
\(P_i(C)\subseteq E(C)\) satisfying
\[
       \partial_C P_i(C)
       =A_i(C)\mathbin\triangle(V(C)\cap T).           \tag{3}
\]
Indeed, the boundary already contributed on \(C\) by
\(\widehat J_i\) is \(A_i(C)\), so (3) makes the total boundary on \(C\)
equal to \(V(C)\cap T\).

The right side of (3) always has even cardinality.  The join equation in
the quotient gives
\[
 |A_i(C)|
 \equiv d_{J_i}(q_C)
 \equiv 1_{\{q_C\in\overline T\}}
 \equiv |V(C)\cap T|
 \pmod2.                                                   \tag{4}
\]
An even vertex set on a circuit has a join, so each \(J_i\) can be lifted
individually.  The issue is choosing the two circuit joins
\(P_1(C),P_2(C)\) edge-disjointly.

> **Exact factor-lifting lemma.**  The fixed quotient joins
> \(J_1,J_2\) lift to two edge-disjoint \(T\)-joins in \(K\) if and only
> if, for every factor circuit \(C\), there are edge-disjoint sets
> \(P_1(C),P_2(C)\subseteq E(C)\) satisfying (3).
>
> When they exist, the lifted joins are
> \[
>   L_i=\widehat J_i\ \mathbin{\dot\cup}\
>       \bigcup_{C\in{\cal C}(F)}P_i(C),\qquad i=1,2.  \tag{5}
> \]

**Proof.**  The preceding boundary calculation proves sufficiency, and
the disjointness of the quotient joins together with the local
disjointness on each factor circuit proves that \(L_1,L_2\) are
edge-disjoint.

Conversely, if the fixed \(J_1,J_2\) have edge-disjoint lifts, intersect
those lifts with each \(C\).  Their factor-edge parts satisfy (3) and
remain disjoint.  More generally, projecting any two edge-disjoint
\(T\)-joins of \(K\) to the edges outside \(F\) gives
edge-disjoint \(\overline T\)-joins in \(R\): summing the boundary
equation over the vertices of each factor circuit gives the required
quotient parity.  Their intersections with each \(C\) satisfy (3).
\(\square\)

Existentially, this gives the exact reduction
\[
\begin{split}
K\text{ packs two edge-disjoint \(T\)-joins}
\quad\Longleftrightarrow\quad&
\text{\(R\) has two edge-disjoint \(\overline T\)-joins}\\
&\text{which satisfy (3) disjointly on every factor circuit.}
\end{split}                                                   \tag{6}
\]

## 6. A literal local test

Condition (3) has a small, exact transition form.  Label every edge of a
factor circuit \(C\) by
\[
       0,\ 1,\ \text{or }2,
\]
meaning unused, in \(P_1(C)\), or in \(P_2(C)\), respectively.  For
\(v\in V(C)\), put
\[
\begin{aligned}
\alpha_i(v)&=1_{\{v\in A_i(C)\}},\\
\tau(v)&=1_{\{v\in T\}},\\
\beta_i(v)&=\alpha_i(v)+\tau(v)\pmod2.
\end{aligned}
\]
The two labels on the circuit edges incident with \(v\) must obey
\[
\begin{array}{c|c}
(\beta_1(v),\beta_2(v))
  &\text{allowed unordered pair of incident labels}\\ \hline
(0,0)&\{0,0\},\{1,1\},\text{ or }\{2,2\}\\
(1,0)&\{0,1\}\\
(0,1)&\{0,2\}\\
(1,1)&\{1,2\}.
\end{array}                                                   \tag{7}
\]
This table is necessary and sufficient: it says exactly that colour
\(i\) occurs an odd number of times at \(v\) precisely when
\(\beta_i(v)=1\), while no factor edge receives both colours.

For the particular spanning-tree/complement construction in Section 4,
\(J_1,J_2\) partition \(E(R)\).  The table then simplifies:

- at a terminal, the two incident factor edges must receive labels
  \(1\) and \(2\); and
- at a nonterminal whose complementary edge has quotient colour \(i\),
  its two incident factor edges must receive labels \(0\) and \(i\).

These local requirements need not be compatible around the cyclic order.
For example, let a quotient have two vertices joined by four parallel
edge objects \(e_1,e_2,e_3,e_4\), and let an unmarked four-edge factor
circuit at one quotient vertex meet them in that cyclic order.  The sets
\[
       J_1=\{e_1,e_3\},\qquad J_2=\{e_2,e_4\}
\]
are disjoint \(\varnothing\)-joins in the quotient.  Around the factor
circuit their complementary-edge colours alternate \(1,2,1,2\).  Every
factor edge lies between unlike types and hence would have to receive
label \(0\).  But a type-\(1\) or type-\(2\) vertex requires one incident
factor edge of its own type.  Thus this fixed quotient pair does not
lift.

The example refutes only automatic lifting of an arbitrary quotient pair.
It does not say that no other quotient pair lifts; for
\(\overline T=\varnothing\), the two empty joins trivially do.  Its role
is to expose the missing cyclic-order condition.

On a single circuit, (7) is a three-state finite recurrence and can be
checked by starting with each possible label on one edge and propagating
around the circuit.  Equivalently, each even right side of (3) has two
complementary joins on \(C\), and one must choose one solution for each
of \(i=1,2\) so that the chosen edge sets are disjoint.

## 7. Consequence and remaining obligation

The quotient route proves, without computation:

1. the contracted graph \(R\) in the connected eight-mark branch is
   connected and Eulerian;
2. its eight marked quotient vertices form an even set
   \(\overline T\);
3. \(R\) has two edge-disjoint \(\overline T\)-joins, constructible from
   a spanning tree; and
4. each quotient join separately lifts through every factor circuit.

What remains unproved is the simultaneous choice: one needs two
edge-disjoint quotient joins for which the local transition system (7)
closes on every factor circuit at once.  By (6), proving that statement
would prove two-\(T\)-join packing for this exact zero matching and close
the connected size-four branch.  The bare fact that \(R\) is Eulerian
does not by itself supply the required cyclic-order compatibility.

This residual condition is another form of the component-routing or
signed-holonomy obstruction recorded in
`docs/eight-mark-bichromatic-code.md`; no equivalence with that document's
specific selector variables is asserted here without a separate
coordinate identification.

The argument does not resolve the five-cycle double cover conjecture.

## AI-use disclosure

This reduction and exposition were developed by an OpenAI Codex agent
under human direction.  All graph operations, parity equations, and the
spanning-tree construction are displayed explicitly so that a human can
check the result without trusting an AI system or a solver.
