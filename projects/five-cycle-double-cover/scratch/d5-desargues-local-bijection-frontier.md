# The Desargues local-bijection formulation of cubic \(D_5\)-flows

Date: 2026-07-28

## Status

This is an exact reformulation and a small structural frontier, **not** a
resolution of the Five-Cycle Double Cover Conjecture.

The central configuration-coloring equivalence is known.  In 2009,
Král', Máčajová, Pangrác, Raspaud, Sereni, and Škoviera proved that a cubic
graph has a five-cycle double cover if and only if it is colorable by the
Desargues configuration [Theorem 7.1][KMP].  The complementary
vertex-state/Petersen-neighborhood language below is the canonical dual
version of their theorem.

What is added here is:

1. an explicit subdivision-homomorphism statement with all local ports
   displayed;
2. an exact state-first criterion in terms of a degree-tight list
   edge-coloring on equal-state edges;
3. a parallel-edge audit; and
4. a hand proof that the tempting strict locally-injective strengthening
   already fails on \(K_{3,3}\).

## 1. Conventions

Let

\[
 \Omega=\{0,1,2,3,4\},\qquad
 D_5=\binom{\Omega}{2}\subseteq\mathbb F_2^5 .
\]

Throughout the main statement, \(G\) is a finite loopless cubic multigraph.
Parallel edge objects are distinct.  The three incidences at a vertex
therefore refer to three edge IDs, even when some IDs have the same pair of
endpoints.

A \(D_5\)-flow is a map \(q:E(G)\to D_5\) such that

\[
 \bigoplus_{e\ni v}q(e)=0
 \tag{1}
\]

at every vertex.  In a loopless graph each edge incident with \(v\) occurs
once in (1).

As usual, the five coordinate edge sets

\[
 C_i=\{e:i\in q(e)\}\quad (i\in\Omega)
\]

are even at every vertex, and every edge belongs to exactly two of them.
The converse labels an edge by the two coordinate sets containing it.
Empty \(C_i\)'s are allowed, so this is the “at most five” convention.

## 2. The Desargues configuration

Use the following subset model of the Desargues configuration
\(\mathcal D\):

- its ten points are the pairs \(L\in\binom{\Omega}{2}\);
- its ten lines are indexed by triples
  \(A\in\binom{\Omega}{3}\); and
- the three points on line \(A\) are the three pairs in
  \(\binom A2\).

Its Levi graph is the Desargues graph \(GP(10,3)\).

The local \(D_5\) equation gives the relevant line immediately.

**Local triangle lemma.**  If \(L_1,L_2,L_3\in D_5\) and
\(L_1\mathbin\triangle L_2\mathbin\triangle L_3=\varnothing\), then there is
a unique \(A\in\binom{\Omega}{3}\) such that

\[
 \{L_1,L_2,L_3\}=\binom A2 .
 \tag{2}
\]

**Proof.**  From \(L_3=L_1\mathbin\triangle L_2\) and
\(|L_3|=2\), the two pairs \(L_1,L_2\) meet in exactly one coordinate.
Their union \(A\) has size three, and \(L_3\) is its third pair.  In
particular the three labels are distinct. \(\square\)

Thus a \(D_5\)-flow directly gives a \(\mathcal D\)-coloring: edge \(e\)
has point-color \(q(e)\), while vertex \(v\) has the unique line

\[
 A_v=\bigcup_{e\ni v}q(e).
 \tag{3}
\]

The three edge colors at \(v\) are exactly the three points on \(A_v\).
This is precisely the known configuration coloring in [KMP].

## 3. Complementary point states and local ports

Complementation is a duality of \(\mathcal D\).  Put

\[
 B_v=\Omega\setminus A_v\in\binom{\Omega}{2},\qquad
 T_e=\Omega\setminus q(e)\in\binom{\Omega}{3}.
 \tag{4}
\]

Then

\[
 q(e)\subseteq A_v
 \quad\Longleftrightarrow\quad
 B_v\subseteq T_e .
 \tag{5}
\]

Let \(S(G)\) be the incidence subdivision of \(G\): replace each edge object
\(e=uv\) by a new vertex \(x_e\) adjacent to \(u\) and \(v\).  Parallel
edges give distinct subdivision vertices.

**Proposition 3.1 (typed incidence map).**  The following data are
naturally equivalent:

1. a \(D_5\)-flow on \(G\);
2. a map
   \[
      \Phi:V(S(G))\longrightarrow V(\operatorname{Levi}(\mathcal D))
   \]
   that sends every original vertex \(v\) to a point \(B_v\), sends every
   subdivision vertex \(x_e\) to a line \(T_e\), preserves incidence, and
   maps the three incident edge objects at every original vertex
   bijectively to the three lines through \(B_v\).

**Proof.**  Given \(q\), use (3) and (4).  If
\(A_v=\{a,b,c\}\), then the three labels at \(v\) are
\(a b,a c,b c\), and their complementary lines are

\[
 B_v\cup\{a\},\quad B_v\cup\{b\},\quad B_v\cup\{c\}.
\]

These are exactly the three lines through \(B_v\), with no repetition.

Conversely, suppose \(\Phi\) has the stated properties and put
\(q(e)=\Omega\setminus T_e\).  If
\(\Omega\setminus B_v=\{a,b,c\}\), local bijectivity says that the
three lines at \(v\) are
\(B_v\cup\{a\},B_v\cup\{b\},B_v\cup\{c\}\).  Their complementary pairs
are \(b c,a c,a b\), whose xor is zero.  The constructions are inverse.
\(\square\)

This proof is edge-object based and does not assume simplicity.

## 4. Forgetting the bipartite types: the Petersen graph

Let \(P=KG(5,2)\) be the Petersen graph: its vertices are the pairs in
\(\binom{\Omega}{2}\), with adjacency given by disjointness.

Represent the dual line \(T_e\) by its complementary pair \(q(e)\).  Then

\[
 B_v\subseteq T_e
 \quad\Longleftrightarrow\quad
 B_v\cap q(e)=\varnothing
 \quad\Longleftrightarrow\quad
 B_vq(e)\in E(P).
\tag{6}
\]

Consequently Proposition 3.1 is equivalently a graph homomorphism

\[
 \phi:S(G)\longrightarrow P,\qquad
 \phi(v)=B_v,\quad \phi(x_e)=q(e),
\tag{7}
\]

whose restriction

\[
 N_{S(G)}(v)\longrightarrow N_P(B_v)
\]

is bijective for every original vertex \(v\).  In other words, the three
edge labels at \(v\) are the complete Petersen neighborhood of \(B_v\).

The Desargues Levi graph is the bipartite double cover of \(P\); retaining
the point/line types turns (7) back into Proposition 3.1.

This is not a graph covering projection in the standard sense.  A
subdivision vertex has degree two, while its Petersen image has degree
three, and the two endpoint states \(B_u,B_v\) may coincide.  It is therefore
only the original-vertex side on which local bijectivity is required.

## 5. Exact state-first extension criterion

The complementary states isolate the obstruction that remains after
choosing only \(B:V(G)\to\binom{\Omega}{2}\).

For an edge \(e=uv\):

- if \(B_u\cap B_v=\varnothing\), no Desargues line contains both states;
- if \(B_u\ne B_v\) and \(|B_u\cap B_v|=1\), the common line is forced:
  \[
      T_e=B_u\cup B_v;
  \]
- if \(B_u=B_v=B\), there are three possible common lines
  \(B\cup\{x\}\), one for each \(x\in\Omega\setminus B\).

Call \(x=T_e\setminus B_v\) the port used by \(e\) at \(v\).  On an
unequal-state edge this port is forced:

\[
 x_v(e)=B_u\setminus B_v.
 \tag{8}
\]

Let \(F_B\) be the spanning subgraph consisting of the equal-state edges.
At a vertex \(v\), first require that the forced ports (8) on unequal-state
edges are distinct.  Delete those ports from the three-element palette
\(\Omega\setminus B_v\), and call the remaining set \(L_v\).  Necessarily

\[
 |L_v|=\deg_{F_B}(v).
\]

**Proposition 5.1 (port/list criterion).**  The state assignment \(B\)
extends to a \(D_5\)-flow if and only if:

1. no edge has disjoint endpoint states;
2. the forced unequal-edge ports are distinct at every vertex; and
3. the equal-state edges admit an edge-coloring \(c\) such that
   \[
      c(uv)\in L_u\cap L_v
   \]
   and the colors on the \(F_B\)-edges incident with \(v\) are all distinct.

Because the lists are degree-tight, the incident colors at \(v\) then use
every member of \(L_v\).

**Proof.**  Unequal-state edge lines, and hence their ports, are forced.
An equal-state edge has one common port color which must be used at both
ends.  Local bijectivity is exactly the assertion that the three ports at
each vertex are distinct.  After removing the forced ports, this is exactly
condition 3.  Reversing the construction supplies all the lines \(T_e\),
and Proposition 3.1 supplies the flow. \(\square\)

On every component of \(F_B\), the state \(B\) is constant, so its palette
has three fixed coordinates.  In the special case that \(B\) is constant on
all of \(G\), Proposition 5.1 reduces exactly to a proper
three-edge-coloring of \(G\).  Thus the constant-state approach is only the
Tait-colorable case, not a route through snarks.

## 6. A strict strengthening fails on \(K_{3,3}\)

One might hope to choose a flow with

\[
 B_u\ne B_v\qquad\text{for every edge }uv.
\tag{9}
\]

Under (9), the map (7) is locally injective also at every subdivision
vertex.  It is then a locally injective homomorphism in the standard sense.
This would remove the list-edge-coloring part of Proposition 5.1 and leave
only forced ports.  It is false even for a simple, bipartite, bridgeless,
three-edge-colorable cubic graph.

**Proposition 6.1.**  The graph \(K_{3,3}\) has \(D_5\)-flows, but none
satisfies (9).

**Proof.**  Write the bipartition as
\(\{u_0,u_1,u_2\}\cup\{w_0,w_1,w_2\}\).  Assume (9), and use an
\(S_5\) permutation to set \(B_{u_0}=01\).

At \(u_0\), the three ports must be \(2,3,4\).  After permuting the
\(w_j\)'s, their states have the form

\[
 \epsilon_2 2,\quad\epsilon_3 3,\quad\epsilon_4 4,
 \qquad \epsilon_j\in\{0,1\}.
\tag{10}
\]

Up to swapping \(0,1\) and permuting \(2,3,4\), there are only two cases:

\[
\begin{array}{c|c|c}
 &\{B_{w_0},B_{w_1},B_{w_2}\}&
 \text{possible left states other than }01\\ \hline
 \mathrm{I}&\{02,03,04\}&\varnothing\\
 \mathrm{II}&\{02,13,14\}&\{12\}.
\end{array}
\tag{11}
\]

The last column is a direct check of the ten pairs: a possible left state
must meet each displayed right state in exactly one coordinate, and the
three resulting ports at that left vertex must be distinct.

The three left states must themselves be distinct.  Indeed, at any fixed
right vertex, two equal left states would force the same port on two
incident edges, contradicting local bijectivity.  But Case I supplies no
second left state, and Case II supplies only one.  Neither case can provide
the required three distinct left states.  This proves that (9) is
impossible.

On the other hand, \(K_{3,3}\) is three-edge-colorable.  Give its three
matching colors the \(D_5\) labels \(01,02,12\).  Every vertex sees the
coordinate triangle on \(\{0,1,2\}\), so this is a \(D_5\)-flow, with
\(B_v=34\) at every vertex. \(\square\)

The two-vertex cubic multigraph with three parallel edges gives an even
smaller multigraph warning.  Its flows are precisely the \(10\) coordinate
triangles assigned bijectively to the three distinct edge objects, for
\(10\cdot3!=60\) flows.  Both endpoint states are necessarily equal.
The \(K_{3,3}\) argument shows that the failure is not an artifact of
parallel edges.

## 7. Why this is not Petersen coloring

Petersen coloring is a different, stronger conjectural structure.
In Jaeger's terminology it maps each edge of \(G\) to an edge of the
Petersen graph so that every cubic star maps to a cubic star.  Equivalently,
its subdivision-incidence target is the subdivision graph \(S(P)\), which
has ten vertex-nodes and fifteen edge-nodes.

The \(D_5\) target here is instead the Desargues Levi graph, with ten
point-nodes and ten line-nodes.  The difference is already visible in the
possible local star-center states at the ends of one graph edge:

- for the \(D_5\)/Desargues map they are equal or are distinct collinear
  points, hence their two-subsets intersect in one coordinate;
- for a Petersen coloring they are equal or are the two endpoints of a
  Petersen edge, hence their two-subsets are disjoint.

Thus the possible intersection sizes are respectively

\[
 \{1,2\}\quad\text{and}\quad\{0,2\}.
\tag{12}
\]

Král' et al. make the same conceptual separation in configuration
language: FiveCDC is the Desargues configuration (their Theorem 7.1),
whereas Petersen coloring is the depleted Cremona--Richmond configuration
(their Theorem 7.3).  They also record the known implication from Petersen
coloring to FiveCDC by lifting a five-cycle double cover of the Petersen
graph.  No converse or universal Petersen-coloring theorem may be inserted
into the present argument.

## 8. Literature and novelty assessment

- [Král' et al.][KMP], European Journal of Combinatorics 30 (2009),
  53--69, DOI [10.1016/j.ejc.2007.11.029][KMP-DOI], prove the exact
  Desargues-coloring equivalence in Theorem 7.1 and distinguish it from
  Petersen coloring in Theorem 7.3.
- Abreu, Funk, Labbate, and Napolitano explicitly identify the neighborhood
  geometry of the Petersen graph with the Desargues configuration
  [pp. 109--122][AFLN].  This is the geometric content behind (6).
- Fiala and Kratochvíl survey locally bijective/injective/surjective graph
  homomorphisms [Computer Science Review 2 (2008), 97--111][FK].  Their
  standard locally bijective notion requires the local condition at every
  source vertex, so Proposition 3.1 is not automatically a graph-cover
  theorem.

There is a nearby universal theorem in the same configuration-coloring
literature, but it does not apply.  Every bridgeless cubic graph can be
colored by every nontrivial *Steiner triple system*.  The Desargues object
used here is only a partial Steiner triple system: it has ten points and ten
selected triples, and there is no Steiner triple system of order ten.
Embedding it in a larger triple system would only produce a coloring allowed
to use the additional points and blocks; it would not force a coloring to
stay inside the Desargues subconfiguration.  Similarly, general
nowhere-zero binary flows use the full nonzero point set of a projective
geometry and do not force all edge values into the ten weight-two vectors
\(D_5\).

Therefore the core equivalence is established literature, not publishable
novelty.  The complementary-state criterion and the strict \(K_{3,3}\)
no-go are useful proof-engineering observations, but by themselves do not
approach a proof or disproof of FiveCDC closely enough to justify a
resolution preprint.

## 9. Exact replay

Run

```text
python3 scratch/check_d5_desargues_local_bijection.py
```

The checker uses only the Python standard library.  It:

1. enumerates literal \(D_5\)-flows by direct XOR propagation;
2. independently enumerates typed Desargues incidence maps on \(K_4\) and
   the triple-edge multigraph;
3. checks the flow/map round trip;
4. checks Proposition 5.1 for every point-state assignment on those two
   graphs;
5. replays the two human cases in (11);
6. exhausts all \(840\) literal \(D_5\)-flows on \(K_{3,3}\) and all
   \(6000\) on the Petersen graph, finding no strict flow on either; and
7. checks the endpoint-state distinction (12).

Expected final output:

```text
triple-edge multigraph: literal flows=60, Desargues maps=60, strict=0
K4: literal flows=180, Desargues maps=180, strict=120
K3,3 hand cases after B(u0)=01: other-left candidates=(0, 1); strict map impossible
K3,3: literal flows=840, strict=0; Tait-supported witness has constant B_v=34
endpoint-state intersections: D5/Desargues={1,2}, Petersen-coloring={0,2}
Petersen graph: literal flows=6000, strict=0
PASS
```

## 10. Loops

The main statement deliberately assumes looplessness.  If a loop counts
twice toward cubic degree, a cubic vertex incident with a loop has one
further ordinary edge.  The loop contributes its label twice to the parity
equation and cancels, leaving the nonzero label of the ordinary edge, so no
\(D_5\)-flow is possible.  In the port model the two loop half-edges would
also try to use the same line twice at one vertex, contradicting local
bijectivity.  This explains the cubic loop case, but the note does not claim
an unqualified incidence-map theorem for arbitrary-degree pseudographs.

## AI-use disclosure

OpenAI Codex agents, under human direction, rediscovered the complementary
state formulation, located and checked the prior Desargues-coloring theorem,
derived the port/list criterion and the strict \(K_{3,3}\) obstruction, and
drafted the note and checker.  The literature theorems are cited, not claimed
as new.

[KMP]: https://lbgi.fr/~sereni/Articles/KMP%2B08.pdf
[KMP-DOI]: https://doi.org/10.1016/j.ejc.2007.11.029
[AFLN]: https://cdm.ucalgary.ca/article/download/61983/46679/176959
[FK]: https://doi.org/10.1016/j.cosrev.2008.06.001
