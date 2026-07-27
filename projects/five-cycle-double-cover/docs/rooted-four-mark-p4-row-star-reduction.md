# The forbidden-vertex path obstruction has a row-star separator

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE SEPARATOR REDUCTION / ROOTED FOUR-MARK
BRANCH / THREE-VERTEX ROW-STAR AND \(1+3\) SINGLETON ENDPOINT
OBSTRUCTIONS ELIMINATED UNDER THE SIMULTANEOUS IRREDUCIBLE/PRIVATE-
CIRCUIT PREMISES**.

This note advances the remaining path hypothesis in
`rooted-four-mark-ozeki-linkage-gate.md`.  It first proves that every
failure has one of two explicit low-separator forms.  The companion note
`rooted-four-mark-singleton-endpoint-closure.md` now eliminates the last
\(1+3\) form when the original irreducibility, private circuits, triple
cyclability, and \(Z\)-acyclicity are simultaneously present.  In the
case in which deletion of the forbidden vertex remains 2-connected, the
separator is especially rigid: three stable vertices are joined to
exactly four terminal-bearing components with boundary profile
\[
                         (2,2,2,2)\quad\hbox{or}\quad(2,2,2,3).
\]
Triple cyclability eliminates the first profile and forces the second
profile's incidence multigraph to be \(K_{4,3}\) minus a three-edge
matching.  Ozeki's one-terminal irreducibility condition then eliminates
the second profile as well: every boundary-two terminal component is a
singleton, whereas separator capacity forces at least three of the four
private circuits to be intact.

The later marked-cut analysis is retained as a supplementary audit for
the weakened state in which one-terminal irreducibility, or preservation
of the private circuits through the reduction to it, has been dropped.
It reaches a triangular-prism quotient, whose two distinguished internal
edges are also forced to have the same colour in any Tait colouring.

No flow switch or zero-edge restoration is used.  In particular, the
argument never assigns the common nonzero terminal value to a deleted
zero edge; that operation would violate conservation at both endpoints.

## 1. Setup

Let \(L\) be the simple cubic rooted graph from the standard four-mark
problem.  Its four marked edges
\[
                     S=\{s_1,s_2,s_3,s_4\}
\]
have one common colour \(c\) in a fixed Tait colouring, and the root edge
\(f\notin S\) has another colour.  Put \(J=L-f\), subdivide each
\(s_i\) by a new degree-two vertex \(z_i\), and write
\[
                   \widehat J,\qquad
                   Z=\{z_1,z_2,z_3,z_4\}.              \tag{1}
\]
The rooted bridge reduction makes \(J\), and hence \(\widehat J\),
2-connected.  The \(bc\)-factor supplies four pairwise vertex-disjoint
private circuits
\[
                   R_i\subseteq\widehat J,\qquad
                   z_i\in V(R_i).                      \tag{2}
\]

Assume that \((\widehat J,Z)\) is irreducible in the first two senses
used by Ozeki:

1. no proper side of a 2-separation is nonempty and terminal-free; and
2. a proper side containing exactly one terminal consists of that
   terminal alone.

These conditions may be reached by the certificate-safe reductions in
`rooted-four-mark-ozeki-linkage-gate.md`.  Preservation of (2) under a
nontrivial one-terminal reduction is a separate issue; every invocation
of (2) below is therefore explicitly included as a premise.

For \(w\in V(\widehat J)\setminus Z\), call \(w\) **path-obstructing** if
\(\widehat J-w\) has no path containing all four terminals.

## 2. If deletion is not 2-connected

> **Two-cut branch.**  Suppose that \(w\) is path-obstructing and
> \(\widehat J-w\) is not 2-connected.  Then there is a vertex
> \(u\ne w\) such that the terminal distribution among the components
> of
> \[
>                         \widehat J-\{w,u\}             \tag{3}
> \]
> is either \(2+2\) or \(1+3\).  In the \(1+3\) case the one-terminal
> component is the singleton \(\{z_i\}\), and the other component
> contains the other three private circuits intact.

### Proof

Since \(\widehat J\) is 2-connected, \(\widehat J-w\) is connected.
Choose an articulation \(u\) of \(\widehat J-w\).  Every component of
(3) contains a terminal: a terminal-free component together with
\(\{w,u\}\) would be a forbidden terminal-free side of a
2-separation.  If a component contains exactly one terminal, the second
irreducibility condition says that it is the singleton consisting of
that terminal.

There cannot be two singleton terminal components.  If
\(\{z_i\}\) is such a component, the two neighbours of the degree-two
vertex \(z_i\) are \(w\) and \(u\).  Every circuit through \(z_i\), in
particular \(R_i\), uses both incident edges and therefore contains both
\(w\) and \(u\).  Two singleton components would make two of the
pairwise vertex-disjoint circuits in (2) contain \(w\) and \(u\), a
contradiction.

The positive component terminal counts sum to four and at most one of
them is one.  Hence the only distributions are \(2+2\) and \(1+3\).
In the \(1+3\) case, the three private circuits belonging to the
three-terminal component avoid \(w,u\), because the private circuit of
the singleton terminal contains both vertices and the four circuits are
pairwise disjoint.  Each of those three circuits is consequently
contained in the three-terminal component. \(\square\)

This branch is a literal two-vertex interface.  The statement does not
claim that either the \(2+2\) or the \(1+3\) interface is reducible.

The \(2+2\) interface is in fact excluded as soon as triple cyclability
is available.

> **Two-plus-two splicing lemma.**  If every three terminals lie on a
> circuit, the \(2+2\) case in the two-cut branch cannot occur in a
> \(Z\)-acyclic graph.

### Proof

Let the two components of
\(\widehat J-\{w,u\}\) be \(A\) and \(B\), with two terminals in each.
Choose a terminal of \(B\).  A circuit through it and both terminals
of \(A\) meets \(A\) in a \(w\)-to-\(u\) path \(P_A\) through the two
\(A\)-terminals.  To check the endpoints explicitly, the circuit must
leave \(A\) because it also contains a terminal in \(B\).  If both of
its \(A\)-boundary edges met the same separator vertex, the two circuit
edges at that vertex would already be used and the circuit could not
also enter \(B\).  Thus its two boundary vertices are \(w,u\).

Symmetrically, a circuit through both terminals of \(B\) and one
terminal of \(A\) supplies a \(w\)-to-\(u\) path \(P_B\) through the
two \(B\)-terminals.  The paths \(P_A\) and \(P_B\) are internally
vertex-disjoint because their interiors lie in distinct components of
\(\widehat J-\{w,u\}\).  Their union is therefore a circuit through
all four terminals, contrary to \(Z\)-acyclicity. \(\square\)

Consequently, under (T3), the only branch left by deletion that is not
2-connected is the \(1+3\) singleton interface.

## 3. If deletion remains 2-connected

The only external graph-theoretic input is Corollary 4.10.1 of Kenta
Ozeki's dissertation,
[*Structural Characterizations of Rooted Subdivisions on Four
Vertices*](https://repository.dl.itc.u-tokyo.ac.jp/record/2009547/files/A39572.pdf).
It states that if a 2-connected graph has no path containing four
prescribed vertices, then two non-prescribed vertices can be deleted so
that no component contains two of the prescribed vertices.

> **Three-vertex row-star lemma.**  Suppose that \(w\) is
> path-obstructing and \(\widehat J-w\) is 2-connected.  Then there are
> vertices \(u,v\notin Z\cup\{w\}\) such that, with
> \[
>                         U=\{w,u,v\},                  \tag{4}
> \]
> the following all hold.
>
> 1. \(U\) is stable.
> 2. \(\widehat J-U\) has exactly four components
>    \(C_1,C_2,C_3,C_4\), where \(z_i\in C_i\).
> 3. If
>    \[
>                         d_i=|\delta_{\widehat J}(C_i)|,
>    \]
>    then, after reordering,
>    \[
>                         (d_1,d_2,d_3,d_4)
>       \in\{(2,2,2,2),(2,2,2,3)\}.                    \tag{5}
>    \]
> 4. At least one private circuit \(R_i\) avoids \(U\) and is wholly
>    contained in its terminal component \(C_i\).

### Proof

Apply Ozeki's corollary to the 2-connected graph
\(\widehat J-w\).  It gives \(u,v\notin Z\) such that no component of
\(\widehat J-\{w,u,v\}\) contains two terminals.  Hence there are at
least four terminal components.

Every component \(C\) of \(\widehat J-U\) has at least two distinct
neighbours in \(U\).  Otherwise its unique neighbour in \(U\) would be
a cut vertex of the 2-connected graph \(\widehat J\).  In particular,
\[
                         |\delta_{\widehat J}(C)|\ge2. \tag{6}
\]
As \(\widehat J\) is subcubic,
\[
\begin{aligned}
\sum_{C\in\pi_0(\widehat J-U)}
       |\delta_{\widehat J}(C)|
  &= \sum_{x\in U}\deg_{\widehat J}(x)
       -2|E(\widehat J[U])|\\
  &\le 9-2|E(\widehat J[U])|.                          \tag{7}
\end{aligned}
\]
The four terminal components already contribute at least eight to the
left side.  An additional terminal-free component would raise that
lower bound to ten, contradicting (7).  Thus the four terminal
components are all the components.

The same comparison shows that \(E(\widehat J[U])=\varnothing\), proving
item 1.  The four integers in (6) have sum at most nine, so their only
possible profiles are those in (5).

Finally, the circuits \(R_1,\ldots,R_4\) are pairwise vertex-disjoint,
while \(U\) has only three vertices.  At least one \(R_i\) avoids
\(U\).  A connected subgraph avoiding \(U\) lies in one component of
\(\widehat J-U\); because it contains \(z_i\), that component is
\(C_i\). \(\square\)

The proof uses all three degree incidences at the separator vertices.
There is no hidden assumption that \(\widehat J\) is cubic: the
subcubic inequality in (7) is the reason the two profiles in (5) are
the only ones.

## 4. Triple cyclability forces one incidence graph

Form the bipartite incidence multigraph \(Q\) whose parts are
\[
                 \{C_1,C_2,C_3,C_4\}\quad\hbox{and}\quad U,
\]
with one edge for every edge of \(\widehat J\) between a component
\(C_i\) and a vertex of \(U\).  Items 1 and 2 of the row-star lemma say
that this records every edge leaving the four components.  Its degrees
on the component side are the \(d_i\).

> **Triple-cyclability collapse.**  Suppose, in addition, that every
> three terminals in \(Z\) lie on a circuit of \(\widehat J\).  Then
> the profile \(2222\) is impossible.  In the \(2223\) profile, \(Q\)
> is the simple graph obtained from \(K_{4,3}\) by deleting a matching
> which saturates the three degree-two component vertices and the three
> vertices of \(U\).

### Proof

A circuit of \(\widehat J\) through terminals in three distinct
components projects to a circuit of \(Q\) through the corresponding
three component vertices.  Here is the full projection check.  The
original circuit meets the cut of each visited component positively and
evenly.  Since \(d_i\le3\), it uses exactly two cut edges there.  It
also has degree zero or two at every vertex of \(U\).  Thus the selected
incidence edges have degree zero or two at every quotient vertex.
They are connected: inside a component, at most two selected boundary
edges leave only one circuit segment to contract.  Hence they form one
quotient circuit.

A bipartite circuit through three component vertices uses three distinct
vertices of \(U\).  It is therefore a six-circuit.  In particular, every
degree-two component vertex has two distinct neighbours in \(U\).

Suppose first that the profile is \(2222\).  Each of the four component
vertices then misses exactly one of the three vertices of \(U\).  Two
component vertices miss the same \(U\)-vertex by the pigeonhole
principle.  Choose a third component vertex.  In the subgraph induced by
these three component vertices and \(U\), the repeated-miss vertex of
\(U\) has degree at most one.  It cannot lie on the required
six-circuit, a contradiction.

Now suppose the profile is \(2223\).  Apply the required six-circuit to
the triple of degree-two component vertices.  Their three missing
\(U\)-neighbours must be distinct; otherwise the repeated-miss
\(U\)-vertex again has degree at most one in that triple.

Let \(C_0\) be the degree-three component vertex.  If it missed some
\(x\in U\), one of its three incidences would be parallel to another,
and the degree-two component which also misses \(x\) exists by the
preceding paragraph.  A triple containing those two component vertices
would have at most one neighbour at \(x\), contrary to its required
six-circuit.  Thus \(C_0\) has one edge to each member of \(U\).  The
three degree-two rows miss distinct columns, which is exactly
\(K_{4,3}\) minus the stated matching. \(\square\)

As a transcription audit, `scratch/audit_p4_row_star_profiles.js`
enumerates every \(4\)-by-\(3\) nonnegative incidence matrix with the
two possible row profiles, separator degrees between two and three, and
a six-circuit on every row triple.  It finds no \(2222\) matrix and six
labelled \(3222\) matrices, all row permutations of the single matrix
described above.  The displayed proof is independent of this finite
check.

The earlier Ozeki reduction proves the triple-cyclability premise for
the original irreducible terminal graph from the four private circuits.
It is not silently asserted after a nontrivial one-terminal reduction
which may destroy those circuits.

## 5. One-terminal irreducibility eliminates the row star

> **Boundary-two singleton lemma.**  Under the irreducibility premises
> of Section 1, every component \(C_i\) with \(d_i=2\) in the row-star
> lemma is the singleton \(\{z_i\}\).

### Proof

Let the two boundary edges of \(C_i\) meet vertices \(p,q\in U\).
They meet two distinct vertices.  Indeed, if both met \(p\), then
deleting \(p\) would separate \(C_i\) from the rest of the
2-connected graph \(\widehat J\).

Delete \(p\) and \(q\).  The set \(C_i\) is then a component of the
remaining graph: all of its edges to \(U\) have been deleted, and it
has no edge to a different component of \(\widehat J-U\).  This is a
proper side of a 2-separation containing exactly the one terminal
\(z_i\).  Ozeki's second irreducibility condition therefore gives
\[
                             C_i=\{z_i\}.
\]
\(\square\)

> **Row-star elimination theorem.**  If \((\widehat J,Z)\) is
> irreducible, every terminal triple is cyclable, and the four
> pairwise vertex-disjoint private circuits (2) exist, then no
> path-obstructing vertex \(w\) for which \(\widehat J-w\) is
> 2-connected exists.

### Proof

Sections 3 and 4 leave only the \(2223\) profile and identify its
incidence graph as \(K_{4,3}\) minus a matching.  By the boundary-two
singleton lemma, each of its three boundary-two components is
\(\{z_i\}\).  The private circuit \(R_i\) through such a degree-two
terminal uses both incident edges, so it contains both separator
neighbours of that row.

Any two degree-two rows of \(K_{4,3}\) minus the stated matching share
one separator neighbour.  Their two private circuits therefore share
that vertex, contrary to the pairwise vertex-disjointness in (2).
This contradiction eliminates the \(2223\) profile. \(\square\)

This argument does not use the marked cyclic-cut inequality, the
location of the root, or the colours of the distinguished edges.  It
does use *both* pieces of state whose simultaneous preservation through
one-terminal reductions is delicate: one-terminal irreducibility and
the four private circuits.

## 6. Supplementary marked-cut audit if irreducibility is weakened

Return to the rooted marked graph \(L\).  Suppose it satisfies
\[
 |\delta_L(X)|+|S\cap E(L[X])|\ge4                    \tag{8}
\]
whenever \(L[X]\) contains a circuit.  The same argument applies to the
opposite cyclic-six-cut cap whenever its inherited version of (8) is
available on the shore being considered.

Call \(C_i\) **intact** when \(R_i\cap U=\varnothing\).

> **Root-incidence lemma.**  In the row-star branch, if \(C_i\) is
> intact and \(d_i=2\), then the deleted root edge \(f\) has exactly one
> endpoint in the corresponding suppressed shore.  Equivalently, \(f\)
> crosses that shore.

### Proof

Suppress \(z_i\) inside \(C_i\), and let \(X_i\subseteq V(J)\) be the
resulting vertex shore.  Since \(R_i\) is intact, it suppresses to a
circuit of \(J[X_i]\) containing \(s_i\).  No other marked edge is
internal to \(X_i\): its subdividing terminal belongs to a different
component of \(\widehat J-U\), and an endpoint lying in \(U\) also
cannot make that marked edge internal.  Thus
\[
 |S\cap E(L[X_i])|=1,\qquad
 |\delta_J(X_i)|=d_i.                                  \tag{9}
\]

Restoring \(f\) either leaves the cut size unchanged or increases it by
one.  In the latter case it has exactly one endpoint in \(X_i\).  With
\(d_i=2\), inequality (8) and (9) require
\[
                         |\delta_L(X_i)|\ge3,
\]
so the increase must occur. \(\square\)

A single edge crosses at most two members of a vertex partition.
Therefore:

> **Exact row-star frontier.**  Assume triple cyclability and (8).
> Then:
>
> 1. exactly one private circuit meets \(U\);
> 2. its component has boundary two;
> 3. the other three private circuits are intact; and
> 4. the two endpoints of \(f\) lie in the other two boundary-two
>    components, one in each.

### Proof

The triple-cyclability collapse makes \(Q\) simple with profile \(2223\).
If a private circuit \(R_i\) meets \(U\), project it to \(Q\) exactly as
in the preceding proof.  The result is a quotient circuit.  Because
\(Q\) is simple and bipartite, it uses at least two vertices of \(U\).
Two different non-intact private circuits would use disjoint vertices
of \(U\), by the vertex-disjointness of the \(R_i\), and would therefore
require at least four vertices in the three-element set \(U\).  Thus at
most one private circuit meets \(U\).

At least one does meet \(U\).  Otherwise all three boundary-two
components would be intact, and the root-incidence lemma would force the
single edge \(f\) to cross three distinct parts, which is impossible.
This proves item 1.

If the unique non-intact circuit belonged to the boundary-three
component, all three boundary-two components would again be intact.
Therefore it belongs to a boundary-two component, proving item 2.
Item 3 follows.

The remaining two boundary-two components are intact, so \(f\) crosses
both of their shores.  One edge crosses two distinct members of this
partition only when it has one endpoint in each.  This proves item 4.
\(\square\)

This is a necessary configuration, not a closed rooted certificate.

### The non-intact row is a singleton

Retain the exact frontier and label the unique non-intact component
\(C_1\), with terminal \(z_1\).  Thus \(d_1=2\), while the endpoints of
\(f\) lie in two other components.

> **Singleton-row lemma.**  The component \(C_1\) is the singleton
> \(\{z_1\}\).  After suppressing \(z_1\), the mark \(s_1\) is an edge
> between the two separator vertices adjacent to \(C_1\).

### Proof

First, \(C_1\) is acyclic.  Suppose otherwise.  If both neighbours of
\(z_1\) lie in \(C_1\), suppressing \(z_1\) turns every circuit through
it into a circuit of the corresponding shore of \(J\).  If exactly one
neighbour lies in \(C_1\), no circuit of \(C_1\) uses \(z_1\), and such
a circuit again survives in that shore.  If neither neighbour lies in
\(C_1\), connectedness already gives \(C_1=\{z_1\}\).

In either non-singleton case, let \(X_1\) be the shore after suppressing
\(z_1\).  It contains a circuit and
\[
                         |\delta_J(X_1)|=2.            \tag{10}
\]
The root \(f\) has no endpoint in \(X_1\), by item 4 of the exact
frontier, so the same cut has size two in \(L\).  No mark other than
\(s_1\) can be internal, and \(s_1\) is internal only when both of its
ends lie in \(X_1\).  Consequently
\[
 |\delta_L(X_1)|+|S\cap E(L[X_1])|\le2+1=3,
                                                               \tag{11}
\]
contrary to (8).  Hence \(C_1\) is a tree.

Let \(n=|V(C_1)|\).  It has \(n-1\) internal edges and two boundary
edges, so
\[
 \sum_{x\in V(C_1)}\deg_{\widehat J}(x)
       =2(n-1)+2=2n.                                   \tag{12}
\]
The 2-connected graph \(\widehat J\) has minimum degree two.  Equality
in (12) therefore makes every vertex of \(C_1\) a degree-two vertex of
\(\widehat J\).

The only degree-two vertices of \(\widehat J\) are the four subdividing
terminals and the two endpoints of the deleted root \(f\).  The other
three terminals lie in the other three components, and the exact
frontier puts the two root endpoints in two of those components.
Therefore \(z_1\) is the only possible vertex of \(C_1\), proving
\(C_1=\{z_1\}\).  The two incidences of its degree-two row go to two
distinct vertices of \(U\), because \(Q\) is simple.  Suppressing
\(z_1\) makes \(s_1\) the edge between them. \(\square\)

Thus, in this weakened audit, the counterfactual
2-connected-deletion branch has the following exact central picture.
With \(U=\{u_1,u_2,u_3\}\) and labels chosen suitably:

* the subdivided mark \(z_1\) is adjacent to \(u_2,u_3\);
* the degree-three component meets all three \(u_i\);
* the other two degree-two components meet
  \(\{u_1,u_3\}\) and \(\{u_1,u_2\}\), respectively;
* their private circuits are intact; and
* the deleted root has one endpoint in each of those last two
  components.

Every incidence in this list is forced.  Internal routing within the
three nontrivial components is the remaining freedom.

There is a compact equivalent description.  Suppress \(z_1\), restore
the two distinguished edges \(s_1\) and \(f\), and contract each of the
three nontrivial components to one vertex.  The resulting six-vertex
cubic skeleton is the triangular prism:
\[
\begin{aligned}
 &\{u_2,u_3,C_0\}\quad\text{is one triangle, with edge }s_1=u_2u_3,\\
 &\{u_1,C_2,C_3\}\quad\text{is the other, with edge }f=C_2C_3,\\
 &u_1C_0,\quad u_2C_3,\quad u_3C_2
     \quad\text{are the three matching edges.}
\end{aligned}                                           \tag{13}
\]
Thus this counterfactual P4 state is a
**triangular-prism substitution atom**:
three vertices of the prism are replaced by one-mark rooted pieces,
while the other three are the separator vertices.  This is only a
skeleton identity; contraction does not retain the internal admissible
state sets of the three pieces.

The skeleton also explains the path obstruction directly.  Delete any
one vertex of \(U\).  The other two vertices of \(U\) are the only
vertices through which a path can move between the four terminal
components.  A simple path can use each of those two vertices at most
once, and therefore can visit at most three components.  It cannot
contain all four terminals.  Thus this is not an artefact of applying
Ozeki's corollary: the prism atom is itself a literal P4
obstruction for every separator vertex in \(U\).

### A second independent contradiction on the prism quotient

Even if one ignores the boundary-two singleton lemma and continues to
the triangular-prism quotient, the fixed Tait colouring excludes the
quotient.  Let \(D\) be the triangle containing the marked edge
\(s_1\), and let \(R\) be the opposite triangle containing the root
edge \(f\).  Every edge other than \(s_1\) and \(f\) crosses between
\(D\) and \(R\).

For a colour \(p\), count the \(p\)-coloured cross edges at the three
vertices of \(D\).  Proper 3-edge-colouring gives
\[
       3-2[\,\operatorname{col}(s_1)=p\,].
\]
Counting the same cross edges from \(R\) gives
\[
       3-2[\,\operatorname{col}(f)=p\,].
\]
The two counts are equal for every \(p\), so
\(\operatorname{col}(s_1)=\operatorname{col}(f)\).  In the rooted
setup every mark has colour \(c\) and \(f\) has a different colour.
This is a contradiction independent of the singleton argument.

## 7. The former exact remaining obstruction

For the original irreducible terminal graph, the earlier Ozeki note
already proves triple cyclability from the four private circuits.
Consequently the separator analysis confines a failure of Ozeki's
forbidden-vertex path hypothesis to a \(1+3\) two-cut whose
one-terminal side is a singleton and whose other side contains three
intact private circuits.

The three-vertex row-star and its triangular-prism residual are no
longer missing cases, and the \(2+2\) two-cut is eliminated by direct
path splicing.  The companion singleton-endpoint note supplies the
previously missing step directly in the simultaneous
irreducibility/private-circuit state.

### Exact marked-edge-endpoint formulation

The singleton interface has a particularly concrete form.  Relabel so
that the singleton is \(z_1\), whose neighbours in \(\widehat J\) are
\(w,u\).  Suppressing \(z_1\) restores the marked edge
\[
                              s_1=wu.
\]
Put
\[
                    K=\widehat J-\{w,z_1\}.
\]
The graph \(\widehat J-w\) is connected and \(z_1\) is its leaf at
\(u\).  Consequently:

> **Endpoint-path equivalence.**  The graph \(\widehat J-w\) has a
> path through all four terminals if and only if \(K\) has a path
> starting at \(u\) and passing through \(z_2,z_3,z_4\).

Indeed, a path containing the leaf \(z_1\) must have \(z_1\) as an
endpoint; deleting or adjoining the edge \(z_1u\) gives the two
directions of the equivalence.  Thus the last P4 problem is exactly a
three-terminal path with one prescribed endpoint after deleting the
opposite endpoint of a marked edge.  It is not an unspecified
four-terminal linkage problem.

Triple cyclability gives one further restriction.

> **Deleted-root-endpoint exclusion.**  If \(w\) is an endpoint of the
> deleted root edge \(f\), then the endpoint path above exists.
> Therefore a singleton-interface P4 failure can occur only at a
> vertex \(w\) of degree three in \(\widehat J\), and \(f\) is not
> incident with \(w\).

### Proof

Take a circuit \(C\) through \(z_2,z_3,z_4\), supplied by (T3).  It
cannot contain \(z_1\), because that would be a four-terminal circuit.
If \(w\) is an endpoint of \(f\), then \(w\) has degree two in
\(\widehat J\).  One of its incident edges is \(wz_1\).  A circuit
through \(w\) would have to use both incident edges and hence contain
\(z_1\).  Thus \(C\) avoids \(w\) and is a circuit of \(K\).

The connected graph \(K\) has a path from \(u\) to \(C\) whose internal
vertices avoid \(C\).  At its first vertex on \(C\), continue around
the circuit and stop just before returning to that vertex.  This gives
a simple \(u\)-starting path containing every vertex of \(C\), in
particular \(z_2,z_3,z_4\).  The endpoint-path equivalence completes
the proof. \(\square\)

If \(w\) has degree three and P4 fails, every circuit through
\(z_2,z_3,z_4\) must use \(w\).  Such a circuit uses the two edges from
\(w\) into the three-terminal side; deleting \(w\) leaves a path
through all three terminals between their two neighbours.  Meanwhile
the private circuit \(R_1\), after deleting \(w,z_1\), gives a path
from \(u\) to one of those two neighbours and contains none of
\(z_2,z_3,z_4\).  Hence the exact unresolved obstruction is an
intersection-order obstruction between these two paths, not the
absence of a path through the three large-side terminals.

### Closure by the degree-two endpoint lemma

The hypothetical intersection-order obstruction cannot occur.  The
proof is in
`docs/rooted-four-mark-singleton-endpoint-closure.md`; its two key
steps are short:

1. \(K\) is 2-connected.  A cut vertex \(x\) would make
   \(H-\{w,x\}\) a \(2+2\) terminal split: terminal-free sides are
   forbidden, a singleton one-terminal side would force its private
   circuit to meet \(R_1\) at \(w\), and triple cyclability splices the
   remaining \(2+2\) split into a four-terminal circuit.
2. Every 2-connected subcubic graph with four specified degree-two
   vertices \(r,a,b,c\) has a path starting at \(r\) through the other
   three.  Add a leaf at \(r\), perform endpoint-safe one-terminal
   reductions, and apply Ozeki's Section 4.9 path-obstruction
   description.  Its two possible irreducible obstructions require
   either seven incidences at two subcubic separator vertices or one
   vertex adjacent to four terminals.

Here \(u,z_2,z_3,z_4\) are all degree two in \(K\), so the second step
gives the required \(u\)-starting path.

### Superseded Watkins--Mesner diagnostic

Before the endpoint lemma above was available, the endpoint formulation
eliminated the low-order alternative in the Watkins--Mesner
characterization.  The argument is retained as a diagnostic, but it is
no longer a remaining proof obligation.  Let \(p,q\) be the two
neighbours of \(w\) in \(K\).  Triple cyclability supplies a circuit
through \(z_2,z_3,z_4\) in \(\widehat J\).  Under P4 failure it uses
\(w\), and deleting \(w\) gives a \(p\)-to-\(q\) path in \(K\)
through all three terminals.  On the other hand, \(K\) has no circuit
through those terminals: any such circuit, joined to \(u\) as in the
deleted-root-endpoint proof, would give the required \(u\)-starting
path.

> **No order-one Watkins--Mesner obstruction.**  In the singleton
> interface, \(K\) has no separation of order at most one which puts
> \(z_2,z_3,z_4\) in distinct components.  Hence a Watkins--Mesner
> obstruction in \(K\) must be of \(K_{3,2}\)-decomposition type.

### Proof

The graph \(K\) is connected, so an order-zero separation is
impossible.  Suppose a vertex \(r\) separates the three terminals into
distinct components of \(K-r\).  A simple path uses \(r\) at most
once, and hence can meet vertices in at most two components of
\(K-r\).  This contradicts the \(p\)-to-\(q\) path through all three
terminals obtained by deleting \(w\) from their triple circuit.
\(\square\)

In that formerly remaining \(K_{3,2}\)-decomposition, each of the three
terminal parts has a two-vertex boundary.  Since only \(p,q\) can supply edges
from \(w\) into their interiors, at least one terminal part is not
incident with \(w\).  Its interior is a one-terminal side of the same
two-separation in \(\widehat J\), so irreducibility collapses that
interior to its terminal.  Thus the exact final WM state is:

* a \(K_{3,2}\)-decomposition of \(K\);
* at least one singleton terminal row;
* a \(p\)-to-\(q\) path through all three terminal rows;
* adjoining the degree-three vertex \(w\) along \(wp,wq\) closes that
  path to a three-terminal circuit; and
* the singleton row's private circuit uses both of its boundary
  vertices and closes through the other four WM parts.

The endpoint lemma eliminates this augmented \(K_{3,2}\) state without
having to classify the attachment positions of \(p,q,u\) and the three
private circuits.  In particular, it does not assume that \(p,q\) lie
in distinct terminal interiors.

### Structured finite screen

The candidate finder
`scratch/search_full_hypothesis_p4_residual.py` tested this exact
marked-edge-endpoint condition on all 240 marked-cut-compliant,
universally separated rows in the existing labelled three-sum family.
Every one of the 53 unmarked roots per row was both bridgeless after
deletion and compatible with an all-one-colour mark precolouring; every
one of the eight marked endpoints had a path.  Thus all
\[
                         240\cdot53\cdot8=101\,760
\]
endpoint instances were positive.  The frozen result is
`scratch/rooted-p4-structured-endpoint-screen-result.json`.

The same ordered-simple-path encoding is UNSAT on the weaker
20-vertex boundary example in
`scratch/verify_rooted_p4_fixed_colouring_boundary.py` (552 variables
and 12,724 clauses after subdivision and deletion), while nearby
positive deletions are SAT.  This is a diagnostic screen, not a proof:
the 240 rows are one construction family, and the searcher trusts the
existing producer for universal separation and the marked-cut filter.

A second generator,
`scratch/generate_root_joined_one_mark_leaves.py`, targets the coarse
geometry expected if the marked-cut inequality forces the root across
two disjoint one-mark shores.  It builds two cyclic one-mark leaf
factors and one two-mark central factor so that the two leaf
three-edge cuts share a leaf-to-leaf edge.  Among 30,000 deterministic
order-56 rows, nineteen passed universal separation and the full marked
cut filter.  All 1,520 eligible roots and all eight marked endpoints per
root passed the endpoint-path test, for 12,160 further positive
instances.  The exact counts and hashes are frozen in
`scratch/root-joined-one-mark-leaves-screen-result.json`.  In
particular, the root-joined-leaf geometry is compatible with the full
marked hypotheses, so it could not simply be declared impossible from
coarse cut geometry alone.  Its internal path state is now covered by
the endpoint lemma under the simultaneous premises of Section 1.

## AI-use disclosure

This separator reduction and exposition were developed by an OpenAI
Codex agent under human direction.  Ozeki's path theorem is prior work
and is cited above.  Every new counting, suppression, and root-incidence
step is displayed for line-by-line checking.  No finite computation is
used as proof, and no resolution of the five-cycle double cover
conjecture is claimed.
