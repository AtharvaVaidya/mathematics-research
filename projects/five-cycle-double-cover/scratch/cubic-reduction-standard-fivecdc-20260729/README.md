# Cubic and snark reductions for the standard FiveCDC

Status: **self-contained reduction theorem, not a resolution of FiveCDC**.

Date: 2026-07-29

This note fixes the exact convention and proves that the standard
five-cycle-double-cover conjecture for finite bridgeless multigraphs reduces
to loopless cubic multigraphs.  It then proves, rather than assumes, the
usual minimum-counterexample reductions through a strong snark class.
The orientable variant is treated separately in Section 9.

No theorem below says that a five-cycle double cover exists.  It says only
that a counterexample in the broad standard class would force a
counterexample in the restricted cubic/snark class.

## 1. Convention

A graph in this note is a finite undirected multigraph.  Parallel edges are
distinct edge objects.  A loop has two incidences at its endpoint.  An edge
is a bridge if deleting that edge increases the number of connected
components; in particular, a loop is never a bridge.

An edge set \(C\subseteq E(G)\) is **even** if, at every vertex, the number
of incidences belonging to \(C\) is even.  It may be empty or disconnected
and need not be 2-regular at a vertex of degree greater than three.

A standard indexed five-cycle double cover, abbreviated 5-CyDC here, is a
tuple
\[
                    (C_1,C_2,C_3,C_4,C_5)
\]
of even edge sets such that every edge lies in exactly two coordinates.
Equivalently, label every edge by the two-set
\[
       L(e)=\{i:e\in C_i\}\in D_5:=\binom{[5]}2 .
\]
The condition at a vertex is
\[
                 \bigtriangleup_{e\text{ incident at }v}L(e)=\varnothing ,
                 \tag{1}
\]
where an edge appears once per incidence.  Thus a loop appears twice and
cancels in (1).

This is the modern cycle-space convention.  Hušek--Šámal, Definition 1.2,
define a labeled \(k\)-cycle double cover as a tuple of \(k\) even
subgraphs, explicitly allow the empty subgraph, and state FiveCDC for
bridgeless cubic graphs in Conjecture 1.9:

- R. Hušek and R. Šámal, *Exponentially Many Circuit Double Covers*,
  arXiv:2607.24724v1 (2026),
  <https://arxiv.org/html/2607.24724v1>.

Liu--Hao--Luo--Zhang state the broad conjecture as a family of even
subgraphs of a bridgeless graph:

- S. Liu, R.-X. Hao, R. Luo, and C.-Q. Zhang,
  *5-Cycle Double Covers, 4-Flows, and Catlin Reduction*,
  SIAM J. Discrete Math. 37 (2023), 253--267,
  <https://doi.org/10.1137/22M1472425>.

Huck's primary formulation explicitly says “at most 5 Eulerian
subgraphs” for bridgeless multigraphs:

- A. Huck, *On cycle-double covers of graphs of small oddness*,
  Discrete Math. 229 (2001), 125--165,
  <https://doi.org/10.1016/S0012-365X(00)00205-3>.

Hoffmann-Ostenhof explains the older terminology and, in the cubic setting,
uses 2-regular subgraphs:

- A. Hoffmann-Ostenhof, *A note on 5-cycle double covers*,
  Graphs Combin. 29 (2013), 977--981,
  <https://doi.org/10.1007/s00373-012-1169-8>.

On a cubic graph, an even edge set has degree zero or two at each vertex, so
after isolated vertices are omitted it is a (possibly disconnected)
2-regular subgraph.  The conventions therefore agree for the existential
cubic FiveCDC question.

Because empty coordinates are allowed, “exactly five indexed coordinates”
and “at most five coordinates” are equivalent: a tuple of length at most
five can be padded by empty even edge sets, while a tuple of length five
already has length at most five.  The tuple convention also permits repeated
members; it is the exact convention in Hušek--Šámal.

The restriction to five **even subgraphs** is not a restriction to five
connected circuits.  Decomposing an even subgraph into circuits can increase
the number of members.  The reductions below are for the standard
even-subgraph formulation.

### Provenance boundary

No novelty is claimed for the reduction theorem.  Cubic and snark
minimum-counterexample reductions are standard throughout the cycle-cover
literature; the purpose of this note is to check that every reconstruction
preserves the **fixed bound of five** under the exact indexed/even-subgraph
convention.  Huck's stronger computer-assisted reducible-configuration
theorem is recorded in:

- A. Huck, *Reducible configurations for the cycle double cover
  conjecture*, Discrete Appl. Math. 99 (2000), 71--90,
  <https://doi.org/10.1016/S0166-218X(99)00126-2>.

That literature gives stronger girth restrictions than the elementary
girth-five conclusion proved here.  No imported girth theorem is used in
Theorem 2.1.

## 2. Main reduction theorem

### Theorem 2.1

The following universal assertions are equivalent.

1. Every finite bridgeless multigraph, allowing loops and parallel edges,
   has a standard 5-CyDC.
2. Every finite bridgeless loopless cubic multigraph has a standard
   5-CyDC.
3. Every finite bridgeless simple cubic graph has a standard 5-CyDC.
4. Every snark has a standard 5-CyDC, where here a snark means a connected
   simple cubic graph that is not 3-edge-colourable, has girth at least
   five, and is cyclically 4-edge-connected.

The implications \(1\Rightarrow2\Rightarrow3\Rightarrow4\) are immediate.
Section 3 proves \(2\Rightarrow1\).  Section 4 audits why the reverse map
for an individual fixed cover is unnecessary and can fail.  Sections 5--8
prove \(4\Rightarrow2\).

The theorem concerns universal existence only.  A particular cover of a
noncubic graph need not lift through the particular cubic expansion used
below; Section 4 gives the exact obstruction.

## 3. A bridgeless loopless cubic expansion

Let \(G\) be a finite bridgeless multigraph.  Isolated vertices do not
affect any edge-cover statement and are discarded.  Every remaining vertex
has incidence degree at least two: a nonloop edge at a vertex of incidence
degree one would be a bridge, while a loop already contributes two.

For every vertex \(v\) of incidence degree \(d(v)\), make a cluster
\[
       Z_v=(v,0)(v,1)\cdots(v,d(v)-1)(v,0).
\]
For \(d(v)\ge3\), this is an ordinary cycle.  For \(d(v)=2\), it consists
of two vertices joined by two parallel cluster edges.  Bijections assign
the \(d(v)\) incidences at \(v\) to the \(d(v)\) cluster vertices.

For every original edge \(e\):

- if \(e=uv\) is not a loop, join the cluster vertex assigned its
  \(u\)-incidence to the cluster vertex assigned its \(v\)-incidence;
- if \(e\) is a loop at \(v\), join the two distinct cluster vertices
  assigned its two incidences.

Call the resulting graph \(X(G)\), and call those last edges **old edges**.
There is one old edge in \(X(G)\) for each edge of \(G\).

Every cluster vertex has two cluster-edge incidences and one old-edge
incidence, so \(X(G)\) is cubic.  It is loopless even when \(G\) has loops.
In particular, a component consisting of one vertex and one loop expands
to two vertices joined by three parallel edges: two cluster edges and the
one old edge.  If \(m=|E(G)|\), where each loop is one edge but supplies
two incidences, then
\[
                         |V(X(G))|=2m,\qquad |E(X(G))|=3m.
\]

### Lemma 3.1

If \(G\) is bridgeless, then \(X(G)\) is bridgeless.

### Proof

Every cluster edge belongs to the cluster cycle \(Z_v\), including the
two-edge cycle when \(d(v)=2\), so it is not a bridge.

An old edge coming from a loop has an alternative path between its two
ends along \(Z_v\).  If an old edge comes from a nonloop edge \(e=uv\),
then \(G-e\) contains a \(u\)-to-\(v\) path because \(e\) is not a bridge.
At every vertex visit along that path, including its endpoint visits at
\(u\) and \(v\), join the appropriate attachment vertices by a path in
the cluster \(Z_w\).  This gives a walk in \(X(G)\) between the ends of
the old edge that avoids that old edge.  Deleting repetitions yields an
alternative path.  Hence no old edge is a bridge. \(\square\)

### Lemma 3.2 (pushforward)

If \(X(G)\) has a standard 5-CyDC, then \(G\) has a standard 5-CyDC.

### Proof

Let \(D_i\) be coordinate \(i\) of a 5-CyDC of \(X(G)\), and define
\[
                    C_i=D_i\cap E_{\rm old}.
\]
Fix an original vertex \(v\).  Sum modulo two the even-degree equations
for \(D_i\) over all cluster vertices of \(Z_v\).  Every selected cluster
edge contributes twice and cancels.  What remains is exactly the number of
selected old-edge incidences attached to \(Z_v\).  It is even.

Under the old-edge identification this is the incidence degree of \(C_i\)
at \(v\).  In particular, an original loop contributes through its two
distinct attachment vertices, hence contributes two exactly as it should.
Thus every \(C_i\) is even.  Every old edge was covered exactly twice in
\(X(G)\), so every original edge is covered exactly twice in \(G\).
\(\square\)

For disconnected \(G\), the construction can be made componentwise.
Alternatively, solve each edge-containing component and take coordinatewise
unions of the five tuples.  Therefore Lemmas 3.1 and 3.2 prove
\(2\Rightarrow1\) in Theorem 2.1.

Equivalently in counterexample language, if \(G\) has no 5-CyDC, then the
explicit graph \(X(G)\) has no 5-CyDC; otherwise Lemma 3.2 would push one
back to \(G\).

## 4. The direction that is not needed, and is false for a fixed expansion

The pushforward in Lemma 3.2 is all that a universal reduction needs.
A given 5-CyDC of \(G\) need not extend to a 5-CyDC of the fixed cyclic
expansion \(X(G)\).

Around a degree-\(d\) expanded vertex, let the old-edge labels in cyclic
order be \(A_0,\ldots,A_{d-1}\in D_5\), and let the cluster-edge labels be
\(Y_0,\ldots,Y_{d-1}\in D_5\).  The local equations are
\[
                       Y_{j-1}\triangle Y_j=A_j.       \tag{2}
\]
The necessary xor condition \(\triangle_jA_j=\varnothing\) guarantees a
solution of (2) in the full vector space \(\mathbb F_2^5\), but not one in
which every \(Y_j\) has weight two.

For example, take
\[
             (A_0,A_1,A_2,A_3)=(01,02,01,02).
\]
If (2) had a \(D_5\)-valued solution, some two-set \(T\) and each of
\[
                     T\triangle01,\quad
                     T\triangle02,\quad
                     T\triangle12
\]
would be two-sets.  The first two requirements say that \(T\) contains
exactly one of each of the pairs \(01\) and \(02\); the third says the same
for \(12\).  Thus among \(0,1,2\), every pair would contain exactly one
element of \(T\), which is impossible.

This is realized without any artificial parity word.  Let \(G\) be one
vertex with two loops \(e,f\), label \(e\) by \(01\), label \(f\) by \(02\),
and place their four incidences alternately around the expansion.  These
labels are a 5-CyDC of \(G\): every loop cancels twice at the vertex.
The expansion is \(K_4\), but this particular labelled cover does not
extend to its four cluster edges.  (Of course \(K_4\) has other 5-CyDCs.)

The same example marks the circuit/even-subgraph boundary.  A Hamilton
cycle of this \(K_4\) can use both old chord edges; after the cluster is
contracted and cluster edges are discarded, its old edges are the two
loops, an even subgraph of degree four at the contracted vertex, not a
connected 2-regular circuit.

### Subdivision and suppression are different

Replacing an edge \(e\) by a nonempty path \(P_e\), with distinct
degree-two internal vertices, preserves 5-CyDCs in both directions.
Indeed, in any even coordinate the two path edges at an internal
degree-two vertex have the same membership, so membership is constant
along \(P_e\).  Conversely, replace every selected \(e\) by the whole
path \(P_e\).  This also works when a loop is subdivided into a closed
path: its two end incidences at the original vertex reproduce the two
loop incidences.  Thus ordinary subdivision/suppression is an equivalence;
the failure above is specific to splitting a high-degree vertex while
requiring every new edge to have a weight-two label.

More locally, splitting one vertex into two vertices joined by a new edge
forces the new edge label to be the xor of the old labels placed on either
shore.  The split lifts a supplied labelled cover if and only if that xor
has weight two.  It can instead have weight zero or four.

## 5. Three finite label lemmas

The rest of the reduction is most transparent in the \(D_5\) label
language.

### Lemma 5.1 (cubic vertex)

If \(A,B,C\in D_5\) and \(A\triangle B\triangle C=\varnothing\), then
\((A,B,C)\) are the three distinct edges of a triangle on three elements
of \([5]\).  Consequently any ordered such triple can be mapped to any
other ordered such triple by a permutation of \([5]\).

### Proof

If \(A=B\), then \(C=\varnothing\), impossible because \(C\in D_5\).
Thus \(A\ne B\).  We have \(C=A\triangle B\).  Since \(C\) has weight two,
the two distinct two-sets \(A,B\) meet in exactly one element.  Writing
\(A=\{p,q\}\), \(B=\{p,r\}\) gives \(C=\{q,r\}\).  Any ordered edge
bijection between two triangles is induced by a vertex bijection between
their three underlying elements, which extends arbitrarily to a
permutation of \([5]\). \(\square\)

### Lemma 5.2 (parallel-pair lift)

For every \(A=\{p,q\}\in D_5\), there are \(B,C\in D_5\) with
\(A\triangle B\triangle C=\varnothing\).

### Proof

Choose \(r\notin A\) and take \(B=\{p,r\}\), \(C=\{q,r\}\). \(\square\)

### Lemma 5.3 (four-cycle lift)

For every \(A,B\in D_5\), there is \(T\in D_5\) such that
\[
                       T\triangle A,\ T\triangle B\in D_5.       \tag{3}
\]
Hence the boundary word \(A,A,B,B\) in cyclic order extends through a
four-cycle.

### Proof

It is enough that \(T\) meet each of \(A,B\) in exactly one element.

- If \(A=B\), take one element of \(A\) and one outside \(A\).
- If \(|A\cap B|=1\), take their common element and one element outside
  \(A\cup B\).
- If \(A\cap B=\varnothing\), take one element from each.

Label the four cycle edges in cyclic order by
\[
                 T\triangle A,\quad T,\quad
                 T\triangle B,\quad T.
\]
At the four boundary vertices, respectively, the xors are
\[
\begin{aligned}
A\triangle T\triangle(T\triangle A)&=0,\\
A\triangle(T\triangle A)\triangle T&=0,\\
B\triangle T\triangle(T\triangle B)&=0,\\
B\triangle(T\triangle B)\triangle T&=0.
\end{aligned}
\]
All four internal labels lie in \(D_5\) by (3). \(\square\)

The small program `verify_local_relations.py` exhaustively checks these
finite claims and the degree-four obstruction of Section 4.  It is not
needed for the proofs.  `verification-output.txt` freezes the expected
output, and `SHA256SUMS` identifies the exact three-file package.

## 6. Parallel edges and small cuts

Assume, for contradiction, that assertion 2 of Theorem 2.1 fails, and
choose a connected counterexample \(G\) with as few vertices as possible.
Disconnected counterexamples are impossible because covers of components
can be united coordinatewise.

### 6.1 Parallel edges

Suppose \(u,v\) are joined by two parallel edges.  If all three incident
edges at \(u\) and \(v\) are parallel, their component is 3-edge-colourable
and has a 3-CyDC.

Otherwise write the remaining incident edges as \(ux\) and \(vy\).
Bridgelessness forces \(x\ne y\): if \(x=y\), the third edge at \(x\)
would be a bridge.  Delete \(u,v\) and add a new edge \(xy\), obtaining a
smaller loopless cubic multigraph \(H\).

The graph \(H\) is bridgeless.  The remainder contains an \(x\)-to-\(y\)
path, or else \(ux\) (equivalently \(vy\)) was a bridge in \(G\).  This
path makes the new edge nonbridging.  A cycle of \(G\) through any other
edge translates to a closed walk of \(H\) by replacing a passage through
the two-vertex parallel-edge gadget by \(xy\); hence every other edge of
\(H\) is also nonbridging.

By minimality, \(H\) has a 5-CyDC.  If \(xy\) has label \(A\), give
\(ux,vy\) label \(A\), and give the two parallel \(uv\) edges the labels
\(B,C\) from Lemma 5.2.  The vertex xor at both \(u\) and \(v\) is zero.
This lifts the cover to \(G\), a contradiction.  Thus \(G\) is simple.

### 6.2 Two-edge cuts

Every two-edge cut in a connected bridgeless graph is a bond.  Indeed, if
deleting its two edges produced at least three components, the four ends
of the deleted edges would be distributed positively among at least three
component boundaries.  One component would have a one-edge boundary,
making that edge a bridge already in the original graph.

Let a two-edge bond separate connected shores \(S,T\), with cut edges
\(s_1t_1,s_2t_2\).  The two attachment vertices on either shore are
distinct: if, say, both cut edges met the same \(s\), the unique edge from
\(s\) into the rest of \(S\) would be a bridge.

Cap \(S\) by the edge \(s_1s_2\), and cap \(T\) by \(t_1t_2\).  Each
capped graph is loopless, cubic, bridgeless, and smaller.  To see
bridgelessness, a bridge of a shore separates its two boundary
attachments (otherwise it would already be a bridge of \(G\)), and the
cap edge bypasses it; the cap edge itself has a path through the connected
shore.

Take 5-CyDCs of the two capped graphs.  Their cap labels are two elements
of \(D_5\).  Permute the five coordinates of one cover so the cap labels
agree.  Delete both caps and give both original cut edges that common
label.  Every boundary vertex sees exactly the label that its deleted cap
had, so all vertex equations remain true.  This gives a 5-CyDC of \(G\),
a contradiction.  Hence \(G\) has no two-edge cut.

### 6.3 Nontrivial three-edge cuts

Let a three-edge bond have connected shores \(S,T\), neither a single
vertex.  Cap each shore by a new cubic vertex joined to its three boundary
incidences.  Each capped graph is a smaller loopless cubic bridgeless
multigraph.  Indeed, any bridge inside a shore separates boundary
incidences on both sides and is bypassed through the cap vertex; every
cap edge is bypassed through another cap edge and a path in the connected
shore (parallel cap edges cover repeated attachment vertices).

Take 5-CyDCs of the capped graphs.  At either cap vertex, the three labels
form an ordered triangle by Lemma 5.1.  Permute the coordinates on one
shore so the labels agree on each corresponding cut position.  Delete the
cap vertices and restore the three cut edges with those common labels.
Again all boundary equations are unchanged.  This covers \(G\), a
contradiction.

Every three-edge cut of \(G\) is a bond: if deleting its three edges left
three or more components, the boundary of one component would have size
one or two, contrary to bridgelessness and Section 6.2.  Thus the argument
above applies to every three-edge cut.  Each is trivial, meaning that one
shore is a single vertex.

## 7. Four-cycles

The preceding conclusions already imply that \(G\) has no triangle.
A triangle has a three-edge cut to the rest of the graph.  If that cut is
trivial on the other shore, the graph is \(K_4\), which is
3-edge-colourable; otherwise it is a forbidden nontrivial three-edge cut.

Suppose \(Q=v_0v_1v_2v_3v_0\) is a four-cycle.  Its four third edges all
leave \(Q\).  A diagonal would leave a two-edge cut, unless both diagonals
are present and the component is \(K_4\).

Let the four third edges join \(v_i\) to \(a_i\), and put
\(R=G-V(Q)\).  Consider the two adjacent perfect matchings of the four
terminal incidences
\[
 P_0=\{a_0a_1,a_2a_3\},\qquad
 P_1=\{a_1a_2,a_3a_0\}.                                      \tag{4}
\]
At least one choice \(P\in\{P_0,P_1\}\) makes \(H=R+P\) bridgeless.
Here is a complete proof.

Every component of \(R\) contains at least two terminal incidences;
otherwise its unique edge to \(Q\) is a bridge of \(G\).  Hence \(R\)
has one or two components.  If it has two, each contains exactly two
terminals; choose the matching in (4) whose two edges cross between the
components.  Every internal bridge of either component separates its two
terminals, since a shore containing neither terminal would give a bridge
of \(G\).  The two crossing matching edges, together with paths inside
the other component, therefore bypass every such bridge.

It remains to treat connected \(R\).  Deleting a bridge of \(R\)
partitions the four terminal incidences with at least one on each side.
A matching in (4) fails to bypass it only when both matched pairs lie
within the two shores, so the terminal split is respectively
\[
             01\mid23\quad\hbox{or}\quad12\mid30.              \tag{5}
\]
The two crossing splits in (5) cannot both be induced by bridges of one
connected graph.  For example, root the bridge-block tree at terminal
0; shores not containing the root are nested or disjoint, whereas
\(\{2,3\}\) and \(\{1,2\}\) cross.  Thus one of \(P_0,P_1\) bypasses every
bridge of \(R\).  Each new matching edge lies on a cycle: its endpoints
are joined in \(R\) when \(R\) is connected, and when \(R\) has two
components the other matching edge supplies the return route.  Hence
\(H\) is bridgeless.

The graph \(H\) is a smaller loopless cubic multigraph.  It is loopless
because \(a_i=a_{i+1}\) would make the triangle
\(a_iv_iv_{i+1}a_i\), already excluded.  By minimality, \(H\) has a
5-CyDC.  Let the labels on the selected two matching edges be \(A,B\).
Restore the four terminal edges with cyclic boundary labels \(A,A,B,B\).
Lemma 5.3 fills the four edges of \(Q\).  This gives a 5-CyDC of \(G\),
the final contradiction.  Therefore \(G\) has girth at least five.

## 8. The minimum counterexample is a snark

A 3-edge-colouring with colour classes \(M_1,M_2,M_3\) immediately gives
the three even subgraphs
\[
                 M_1\cup M_2,\quad M_1\cup M_3,\quad M_2\cup M_3.
\]
Every edge occurs twice, and two empty coordinates pad this to a 5-CyDC.
Therefore the minimum counterexample \(G\) is not 3-edge-colourable.

It is connected and simple, has girth at least five, and has no edge cut
of size one or two and no nontrivial edge cut of size three.  Any cut of
size at most three separating two cyclic shores is nontrivial.  Hence
\(G\) is cyclically 4-edge-connected.  It is a snark under the definition
in Theorem 2.1.

Consequently, if all such snarks have 5-CyDCs, there is no loopless cubic
counterexample.  This proves \(4\Rightarrow2\) and completes Theorem 2.1.

The qualifier on “snark” matters.  Some authors omit the girth condition;
some require cyclic connectivity four, five, or six.  The proof gives
girth at least five and cyclic connectivity at least four.  It does **not**
reduce FiveCDC to cyclically 5-edge-connected or cyclically
6-edge-connected snarks.

## 9. Orientable FiveCDC: separate conclusion

For this section only, an orientable 5-CyDC means that every occurrence of
an edge in a coordinate is directed, each coordinate is balanced at every
vertex, and the two occurrences of every edge use opposite directions.
For loops, “opposite” refers to the two opposite choices of loop dart.

The cluster pushforward of Section 3 remains valid.  Sum the integer
inflow-minus-outflow equations over all vertices of \(Z_v\).  Directed
cluster edges cancel internally.  The remaining old-edge occurrences are
balanced at the contracted vertex.  Opposite coverage of every old edge is
unchanged.  Therefore:

> If every finite bridgeless loopless cubic multigraph has an orientable
> 5-CyDC, then every finite bridgeless multigraph has an orientable
> 5-CyDC, under the directed-even-subgraph convention above.

This implication is independent of the standard unoriented proof.

No orientable analogue of the full snark reduction is claimed here.
Pair-label compatibility alone forgets the directed transition data needed
when gluing covers.  In particular, the four-cycle proof uses only even
parity and can change how same-coordinate boundary occurrences are paired.
It must not be cited as an orientable four-cycle reduction without an
additional directed-interface proof.

## 10. Exact scope ledger

| Statement | Status |
|---|---|
| General bridgeless multigraph \(\Leftarrow\) loopless cubic multigraph | Proved, including loops and parallel edges |
| Loopless cubic multigraph \(\Leftarrow\) simple cubic graph | Proved by the parallel-pair reduction |
| Cubic minimum counterexample is a strong snark | Proved through 2-cuts, 3-cuts, triangles, and 4-cycles |
| Reduction to cyclic connectivity at least five or six | **Not proved** |
| Stronger minimum-counterexample girth restriction | Huck's girth-at-least-ten theorem is sourced but not reproved or used here |
| Fixed-cover lift through cyclic vertex expansion | **False**; explicit two-loop obstruction |
| Subdivision/suppression equivalence | Proved |
| “Five” versus “at most five” with empty indexed coordinates | Equivalent and faithful to Hušek--Šámal Definition 1.2 |
| Five even subgraphs versus five connected circuits | **Not equivalent as a cardinality statement** |
| Orientable general-to-cubic implication | Proved separately |
| Orientable full snark reduction | **Not claimed** |
| FiveCDC itself | **Unresolved by this note** |
