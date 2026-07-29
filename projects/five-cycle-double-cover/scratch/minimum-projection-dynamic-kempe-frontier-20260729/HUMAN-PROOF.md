# A dynamic Kempe frontier: one exact no-go class and an orbit-reflecting inflator

## 1. Boundary conventions

Let \(K=\mathbb F_2^2=\{0,1,2,3\}\), written additively as xor.  Let
\(H\) be the support of the first coordinate of a nowhere-zero
\(\mathbb F_2^3\)-flow on a cubic graph.  At a vertex of \(H\), write
\(s_{i-1},s_i\in K\) for the low values on its two incident support
edges and \(d_i\in K-\{0\}\) for the low value on its complement edge.
The flow equation is

\[
                         d_i=s_{i-1}+s_i.                 \tag{1}
\]

For a component \(W\) of \(G-H\), xor of the flow equations at its
internal vertices gives

\[
                         \sum_{i\in\partial W}d_i=0.      \tag{2}
\]

A componentwise element of \(\operatorname {GL}(2,2)\) may be applied
to all low values in \(W\).  If the transformed boundary values satisfy
the circuit sums needed to integrate (1), the support values are then
recovered by prefix xor.

An integrated extension is *clean* when, for every complement component
\(W\) and every \(c\in K\), the number of support edges of low value
\(c\) in the cut \(\delta(W)\) is even.  It has a *deletion* when one
support circuit omits a low value: translating that circuit by the
omitted value and removing it from the first-coordinate support gives a
strictly smaller extendable projection.

## 2. A universal directly clean class

### Theorem 1

Suppose \(H\) is one circuit and every component of \(G-H\) has exactly
two boundary terminals on \(H\).  Then every extension is directly
cleanable by componentwise \(\operatorname {GL}(2,2)\) maps.  In
particular, no dynamic goal-free Kempe component exists in this class.

### Proof

For a complement component \(W\), let its two nonzero boundary values be
\(x_W,y_W\).  Equation (2) says \(x_W+y_W=0\), so
\(x_W=y_W\).  Fix one nonzero \(t\in K\).  The group
\(\operatorname {GL}(2,2)\cong S_3\) is transitive on \(K-\{0\}\);
therefore choose the map on each \(W\) to send its boundary value to
\(t\).

Every boundary derivative on \(H\) is now \(t\).  The number of vertices
of \(H\) is twice the number of complement components, hence is even,
so (1) integrates.  Its support values alternate between two values
\(a\) and \(a+t\).

Fix \(W\), attached at two vertices \(p,q\) of \(H\).  At each of
\(p,q\), the two incident support edges have one value \(a\) and one
value \(a+t\).  In the multiset union of those four incidences, each
value consequently occurs twice.  If \(p,q\) are adjacent, their common
support edge is internal to \(W\): it was counted twice and is removed
twice when passing from the incidence multiset to \(\delta(W)\).
Removing two equal copies does not change parity.  Thus every low value
occurs evenly in \(\delta(W)\).  This holds for every \(W\), so the
extension is clean. \(\square\)

The proof is unbounded.  The checkers merely audit its finite indexing
through support order fourteen; they are not the reason the theorem is
valid.

## 3. The \(K_{3,3}-e\) orbit-reflecting two-pole

Let \(ab\) be an edge of \(K_{3,3}\).  Delete \(ab\), regard \(a,b\) as
degree-two terminals, and attach one external edge at each.  Call the
resulting two-pole \(P\).

In every proper three-edge-colouring of \(P\), the two attachment edges
have the same colour \(t\).  One way to see this is the parity lemma for
a three-edge-coloured multipole with two semiedges.  Equivalently, direct
enumeration gives the same conclusion.  Adding \(ab\) in colour \(t\)
then gives a Tait colouring of \(K_{3,3}\), and deleting \(ab\) is the
inverse operation.

The relevant fact about \(K_{3,3}\) is classical: it has two Tait
colourings up to global colour permutation, and in either one every
colour pair is a Hamilton circuit.  Hence it has two edge-Kempe classes
[Belcastro--Haas, Section 4.2](https://arxiv.org/abs/1209.1730).

This gives more than a rigid count.  If a colour pair contains \(t\),
its Hamilton circuit in \(K_{3,3}\) uses \(ab\); deleting \(ab\) turns
it into the unique terminal-to-terminal path of \(P\).  Switching that
path changes the attachment colour exactly as switching the
corresponding projected edge.  If the pair does not contain \(t\), its
Hamilton circuit avoids \(ab\) and remains an internal circuit of
\(P\); switching it leaves the attachment colour unchanged.  Either
switch is a global transposition in the completed \(K_{3,3}\), so it
does not change which of the two Kempe classes the pole colouring
belongs to.

Direct enumeration records twelve proper colourings of \(P\), split
into two Kempe orbits of six.  Thus contraction of \(P\) to one edge
both preserves and reflects every boundary-changing Kempe move; the
two-valued internal orbit label is invariant.

## 4. Orbit-reflecting metric inflation

Replace a complement edge \(uv\) by a chain of \(r\) copies of \(P\).
Attach \(u\) to the first \(a\), consecutive copies terminal-to-terminal,
and the last \(b\) to \(v\).  All attachment and joining edges have the
projected edge colour \(t\).  The shortest \(a\)-to-\(b\) path in
\(K_{3,3}-ab\) has length three, so the old-endpoint distance of the
chain is

\[
                              L=4r+1.                    \tag{3}
\]

In a proper colouring, each copy has equal terminal colour, so these
colours propagate along the chain.  For a pair containing \(t\), all
the terminal paths and joining edges form one path through the chain.
For the other pair, every pole contributes only an internal circuit.
Consequently every boundary-changing Kempe component in the inflated
graph contracts to a Kempe component in the base graph; every internal
switch contracts to the identity.  Conversely, expanding a base Kempe
component gives an inflated one.  The same is true for simultaneous
path switches subject to support-circuit charge, because contraction
preserves their boundary endpoints.  Componentwise global
\(\operatorname {GL}(2,2)\) relabellings also project.

Fresh pole vertices preserve simplicity and cubicity.  If the base graph
is connected and bridgeless, so is the inflated graph: a base circuit
through the replaced edge expands through a terminal path, and internal
pole edges lie on an internal circuit or on a terminal path that can be
completed by such a base circuit.

There is also a metric consequence.  For a current integrated support
word \(s\), put

\[
                         M_c=\{e\in H:s(e)=c\}.
\]

Assume every circuit component of \(H\) uses all four low values and
choose \(L\geq |H|\).  If a binary cycle \(Z\) avoids \(M_c\), decompose
it into edge-disjoint circuits.  A circuit internal to a replacement
chain contains no support edge.  Any other circuit that uses complement
edges traverses a whole chain and hence has at least \(L\) complement
edges, so

\[
                    |C\cap H|\leq |H|\leq L\leq |C-H|.  \tag{4}
\]

A circuit contained in \(H\) would be a circuit component of \(H\);
it meets \(M_c\) by assumption and therefore cannot occur.  Summing (4)
proves, for all four \(c\),

\[
 Z\cap M_c=\varnothing
       \quad\Longrightarrow\quad |Z\cap H|\leq |Z-H|.    \tag{5}
\]

These are the four full binary-cycle, equivalently shortest-\(T\)-join,
inequalities forced by cardinality minimality.

### Conditional dynamic-trap transfer

Suppose a realizable base boundary model has a support-neutral Kempe
component with no clean or deletion state, where feasible componentwise
maps are included as moves.  Inflate every complement edge by the chains
above with \(L\geq|H|\).  Orbit reflection says every inflated reachable
boundary state projects into the same base component, so no new clean or
deletion boundary state appears.  Absence of deletion means every current
support circuit uses all four colours.  Applying (5) separately at every
reachable state proves that every state satisfies all four recomputed
exchange inequalities.

Thus a base goal-free component would yield exactly the sought
necessary-condition-compatible dynamic trap.  This package does **not**
find such a component.

## 5. Exploratory search, not a theorem

The fixed size-sixteen residual

\[
\begin{aligned}
s&=\texttt{01010123|01012302},\\
\pi&=\texttt{0123444444130244}
\end{aligned}
\]

has four two-terminal complement components and one eight-terminal
component.  `exploratory_search.py` retains literal internal colourings,
filters circuit-integrable states, and includes:

1. every charge-restoring simultaneous subset of bichromatic path or
   internal-circuit switches; and
2. every feasible independent componentwise colour relabelling.

The deterministic searches run during this investigation found no
goal-free component in ten random connected order-ten eight-poles
(288--480 literal colourings and 5,760--9,720 combined states), sixty-one
randomly cut and terminal-labelled \(K_{3,3}\) eight-poles
(192 or 216 colourings and 3,840--4,392 states), or four random
order-twelve eight-poles (240--468 colourings and 4,860--9,510 states).
All but one of the order-ten samples had a connected dynamic graph; the
remaining sample had two components, and both contained a clean/deletion
goal.  Every other sampled graph was connected.

This is only negative exploratory evidence.  The samples are not a
canonical exhaustive graph census, and the counts must not be used as a
universal no-go theorem.

## 6. Exact scope

Theorem 1 excludes dynamic traps only when \(H\) is one circuit and every
complement component has exactly two boundary terminals.  It says nothing
universal about three-terminal or larger components, multiple support
circuits, or the full Five-Cycle Double Cover Conjecture.

The inflation theorem is conditional.  It manufactures the known dynamic
exchange inequalities and preserves a boundary Kempe orbit; it does not
make the support globally minimum and does not prove that a goal-free
base orbit exists.

The \(K_{3,3}\) Kempe-class fact is known from Belcastro--Haas.  The
two-terminal cleaning lemma and the orbit-reflecting use of the
edge-deleted pole were derived in this AI-assisted project.  No claim of
literature priority is made without specialist human review.
