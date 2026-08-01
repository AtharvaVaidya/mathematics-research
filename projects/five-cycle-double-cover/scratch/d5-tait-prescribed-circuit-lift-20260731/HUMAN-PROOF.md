# A prescribed factor circuit from a Tait colouring

## Conventions

Let

\[
 D_5=\{X\subseteq\{0,1,2,3,4\}:|X|=2\}.
\]

A `D5` flow on a loopless cubic graph is an edge labelling by `D5` for
which the symmetric difference of the three incident labels is empty at
every vertex.  For a coordinate pair `P`, put

\[
 Y_P=\{e:|q(e)\cap P|=1\}.
\]

Coordinate projection shows that `Y_P` is Eulerian.  Its nonempty
components are circuits because the graph is cubic.

## Prescribed-circuit theorem

**Theorem.**  Let `H` be a cubic graph with a proper three-edge-colouring,
and let `K` be any circuit of `H`.  There is a `D5` flow `q` for which

\[
                         Y_{\{0,1\}}(q)=E(K).
\]

Thus `K` is one factor component, indeed the only nonempty component of
that factor.

**Proof.**  Name the three Tait colours `2,3,4`.  If an edge has colour
`c`, define

\[
 q(e)=
 \begin{cases}
   \{0,c\},&e\in E(K),\\
   \{2,3,4\}\setminus\{c\},&e\notin E(K).
 \end{cases}                                                  \tag{1}
\]

Every displayed label has size two.  Consider a vertex outside `K`.
Its three incident Tait colours are `2,3,4`, so its three labels are

\[
                         23,24,34,
\]

whose symmetric difference is empty.

At a vertex of `K`, the two circuit edges have two distinct Tait colours,
say `a,b`, and the third edge has the remaining colour `c`.  Formula (1)
gives the three incident labels

\[
                         0a,0b,ab,
\]

because `\{2,3,4\}\setminus\{c\}=\{a,b\}`.  Their symmetric difference
is again empty.  Hence `q` is a `D5` flow.

Coordinate `1` occurs nowhere.  An edge label meets `\{0,1\}` oddly
exactly when it contains `0`, and by (1) these are exactly the edges of
`K`.  Therefore `Y_{\{0,1\}}(q)=E(K)`.  \(\square\)

## Root-feasibility corollary

**Corollary.**  Let `H` be a 2-connected Tait-colourable cubic graph.
For every two distinct edges `r,s`, `H` has a `D5` flow in which one
factor component contains both roots.

**Proof.**  In a 2-connected graph every two edges lie on a common
circuit.  One elementary proof is to subdivide both edges: the resulting
graph remains 2-connected, and the vertex form of Menger's theorem gives
a circuit through the two subdivision vertices.  Suppressing them gives
a circuit `K` of `H` containing `r,s`.  Apply the theorem to `K`. \(\square\)

The 2-connectivity hypothesis is automatic in the narrowed FiveCDC
premise, which assumes that `H` is simple and 3-edge-connected cubic.
Indeed a cut vertex in a connected cubic graph puts at most three edges
between its components and the cut vertex; parity forces one component
to attach by a single edge, contradicting 3-edge-connectivity.

## Explicit inverse edge insertion

Subdivide `r,s` by new vertices `u,v` and add `e=uv`, obtaining `G`.
The preceding construction also gives a direct five-cover of `G`.
The circuit `K` becomes a circuit `K*` through `u,v`.  Choose either
`u`-to-`v` arc `A` of `K*`, transpose coordinates `0,1` on all edges of
`A`, and label `e` by `01`.

At an internal vertex of `A`, two incident labels are transposed, so xor
conservation remains true.  At each of `u,v`, exactly one old label
changes by xor with `01`, and the new label `01` cancels that defect.
Every transposed label was `0c` and becomes `1c`, still of weight two.
Thus the resulting labels form a `D5` flow on `G`.

Equivalently:

**Edge-reducibility corollary.**  If a cubic graph `G` has an edge `e`
whose standard two-root elimination `H=G div e` is 2-connected and
Tait-colourable, then `G` has a standard five-even-subgraph double cover.

This includes a useful part of the minimum-counterexample induction:
after eliminating an edge from a putative minimum counterexample, a
Tait-colourable reduced graph can never be the obstruction.  The remaining
rooted premise concerns only non-Tait reduced graphs that already possess
a genuinely four- or five-coordinate `D5` flow.

## Scope

The theorem does not prove that every non-Tait `D5` flow can be made
root-good, and it does not resolve FiveCDC.  It does remove the entire
Tait-colourable branch of the exact narrowed premise, by a construction
that prescribes the desired factor circuit rather than searching a Kempe
orbit.

The existence conclusion is a special case of a stronger known result:
Hoffmann-Ostenhof, *A note on 5-cycle double covers*, Graphs and
Combinatorics 29 (2013), 977--979, Lemma 0.2 (arXiv:1209.0096), states
that every 2-regular subgraph of a cubic graph with a nowhere-zero 4-flow
is contained in a 4-CDC.  The direct formula (1) records the specialization
in the exact edge-label language used by this project.  No novelty claim is
made for the existence theorem.

## AI-use disclosure

OpenAI Codex agents, under human direction, discovered formula (1), checked
the local cases, and drafted this proof.  The argument is provided in full
for human verification.  It has not undergone independent human peer review.
