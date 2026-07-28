# The local neutral-triangle corner-pairing frontier

Date: **2026-07-28**

Status: **RIGOROUS REDUCTION, COMPLETE ORDER-14 CENSUS, AND SHARP
NO-GO RESULTS; NOT A PROOF OF THE LOCAL LEMMA OR OF FIVECDC**.

## 1. The local candidate and its eventual refutation

Let \(q:E(G)\to\binom{[5]}2\) be a \(D_5\)-flow on a connected cubic
graph.  Put
\[
 C_i=\{e:i\in q(e)\},\qquad
 Y_{ij}=C_i\mathbin\triangle C_j .
\]
Every \(C_i\) and every \(Y_{ij}\) is a disjoint union of circuits.  A
switch on a component \(K\) of \(Y_{ij}\) transposes \(i,j\) on all
edges of \(K\).

At a cubic vertex the incident labels have the form
\[
                         ab,\quad ac,\quad bc.                 \tag{1}
\]
The two edges labelled \(ab,ac\) lie together on exactly three factor
components:
\[
                  K_{bc}\subseteq Y_{bc},\qquad
                  K_{ad}\subseteq Y_{ad},\qquad
                  K_{ae}\subseteq Y_{ae},                     \tag{2}
\]
where \(\{d,e\}=[5]\setminus\{a,b,c\}\).

Write \(\delta_P\) for the surface-Euler change under the switch on the
component in (2).  The exact local target is
\[
                         \max(\delta_{bc},\delta_{ad},\delta_{ae})
                         \ \ge 0.                              \tag{3}
\]
At a local surface-\(\chi\) maximum every switch has nonpositive
change, so (3) gives a neutral component through every adjacent pair
of graph edges.  The stronger assertion that one of the three deltas
is exactly zero holds through the complete order-14 census but is false
on an explicit 28-vertex two-lift in Section 4.  More importantly, (3)
itself is false at a local maximum on a second 28-vertex two-lift.
Thus the local-adjacent-neutral route is closed.

## 2. One fixed four-regular corner graph

For each graph vertex \(v\), make a triangle \(\Delta_v\).  Its three
corners are the three coordinates occurring at \(v\), and its side
corresponding to \(e\in\delta(v)\) has endpoints \(q(e)\).  For a graph
edge \(e=uv\) labelled \(ij\), glue the \(ij\)-side of \(\Delta_u\) to
the \(ij\)-side of \(\Delta_v\), matching \(i\) to \(i\) and \(j\) to
\(j\).  The result is the normalized properly coloured surface
\(S(q)\).  Its coloured vertices are the components of the \(C_i\), so
\[
 \chi(S(q))=\sum_i\kappa(C_i)-|E(G)|+|V(G)|.                  \tag{4}
\]

There is an equivalent circuit-partition model which does not change
when a switch is made.  Define a four-regular multigraph \(L(q)\) as
follows.

* A vertex of \(L(q)\) is an edge of \(G\).
* If the two incident graph edges \(e,f\) at \(v\) both contain
  coordinate \(i\), join the vertices \(e,f\) of \(L(q)\) by the
  \(i\)-corner edge in \(\Delta_v\).

At a vertex \(e=uv\) of \(L(q)\), where \(q(e)=ij\), the current
transition pairs the \(i\)-corner at \(u\) to the \(i\)-corner at \(v\),
and likewise for \(j\).  The circuits of this transition partition are
exactly the coordinate circuits \(C_i\).  Hence their number is the
first term of (4).

This puts all surface-Euler changes into one standard
circuit-partition problem on a fixed four-regular graph.

## 3. Exact boundary-twist law

Fix \(P=\{i,j\}\) and a component \(K\) of \(Y_P\).  Let \(V(K)\) be
the graph vertices incident with \(K\), and define
\[
 B(P,K)=\{e=uv:q(e)=P,\ |\{u,v\}\cap V(K)|=1\}.               \tag{5}
\]

> **Lemma 3.1 (corner-pairing law).**  After canonically identifying
> the triangle corners before and after the switch, the switch on
> \(K\) changes the transition of \(L(q)\) exactly at the vertices
> \(B(P,K)\).  Consequently
> \[
> \delta_P=
>   c(\mathcal P\mathbin\triangle B(P,K))-c(\mathcal P),      \tag{6}
> \]
> where \(\mathcal P\) is the current transition partition and
> \(c\) denotes its number of circuits.

**Proof.**  At every \(v\in V(K)\), the two edges of \(K\) are the two
\(P\)-active sides of \(\Delta_v\).  The third side has a label either
equal to \(P\) or disjoint from \(P\).  Apply the transposition \(P\)
to all three corner names of \(\Delta_v\).

On an edge of \(K\), both endpoint triangles are transposed, so the
corner pairing is unchanged under this identification.  A disjoint
third side is fixed pointwise.  A \(P\)-labelled third side has its two
corners exchanged at an endpoint in \(V(K)\).  If both endpoints lie
in \(V(K)\), the two exchanges cancel.  If exactly one does, the two
cross-side pairings are interchanged.  These are precisely the edges
in (5).  Nothing else changes.  The number of transition circuits is
the number of coloured vertices, while the numbers of edges and
triangles in (4) are fixed, proving (6). \(\square\)

Call \(K\) **\(P\)-closed** when \(B(P,K)=\varnothing\).

> **Corollary 3.2.**  A switch on a \(P\)-closed factor component is
> surface-Euler neutral.

There is a second human-checkable neutral case.  The number
\(|B(P,K)|\) is even.  Indeed, orient \(K\) and mark whether each edge
of \(K\) is \(i\)-only or \(j\)-only.  The mark changes exactly at a
vertex whose third edge is labelled \(P\), so the number of such
vertices is even.  A \(P\)-edge with both endpoints on \(K\) accounts
for two marked vertices, while an edge of \(B(P,K)\) accounts for one.
Reducing modulo two proves the assertion.

> **Lemma 3.3 (two-break neutrality).**  If
> \(|B(P,K)|\in\{0,2\}\), then the switch on \(K\) is
> surface-Euler neutral.

**Proof.**  The case zero is Corollary 3.2.  Suppose
\(B(P,K)=\{e,f\}\).  Cut the two current coordinate-link transitions at
the vertices \(e,f\) of the four-regular corner graph.  The part carried
by the triangles of \(K\), including every \(P\)-edge having both
endpoints on \(K\), is a two-port, two-strand tangle.  Apart from closed
circuits, it induces one perfect matching of the four terminal strands
\[
                         e_i,e_j,f_i,f_j.
\]
Transposing \(i,j\) on \(K\) applies
\[
                         (e_i\,e_j)(f_i\,f_j)
\]
to this matching.  Each of the three perfect matchings on four objects
is fixed setwise by that permutation:
\[
\begin{split}
 &(e_i e_j)(f_i f_j),\\
 &(e_i f_i)(e_j f_j),\\
 &(e_i f_j)(e_j f_i).
\end{split}
\]
The closed internal circuits are merely relabelled.  Hence the
connectivity pairing presented to the unchanged outside tangle is
identical before and after the switch.  The total number of corner
circuits, and therefore (4), is unchanged. \(\square\)

The local target would follow from the following purely
combinatorial boundary-degree statement:
\[
 \min\bigl(
 |B(bc,K_{bc})|,\ |B(ad,K_{ad})|,\ |B(ae,K_{ae})|
 \bigr)\le2.                                                  \tag{7}
\]
This boundary-degree statement is false; Section 4 gives a 28-vertex
2-lift counterexample.  Lemma 3.3 remains valid but is not sufficient.

## 4. The boundary-size route fails under a 2-lift

Every factor circuit in (2) lifts to a circuit of \(L(q)\), and the
three lifted circuits share the same corner edge in \(\Delta_v\)
joining the vertices \(ab\) and \(ac\) of \(L(q)\).  Nevertheless, the
suggested bound (7) is not stable under graph covers.

Start with the order-14 state on
```text
M??CBAPUAc@oJ?h??
```
displayed below.  At vertex \(2\), edge pair \(6,7\), its three
boundary sizes are \((2,2,4)\).  Give base edges \(0,3\) voltage one
and every other edge voltage zero, and take the associated two-sheeted
cover.  Each of the three selected factor circuits has odd total
voltage, so each lifts to one connected circuit.  Every base boundary
edge has two lifts, and therefore the three boundary sizes become
\[
                              (4,4,8).                        \tag{8}
\]
The lift is a connected simple bridgeless cubic graph on 28 vertices.
Its graph6 encoding is
```text
[???????????O?_?B?@G?__H@?PD??a_?aA?COO?@S??Ag?AI??@D??P@??AGG??
```
and the local candidate data \((P,|B|,\delta_P)\) are
\[
                       (04,4,0),\quad(12,4,+2),\quad(34,8,+2).
\]
Thus (7) fails while the desired local zero conclusion survives.
The constructor and literal checker are
```text
python3 scratch/check_d5_local_boundary_degree_two_lift_no_go.py
```
and also verify the flow equations, connectedness, cubicity,
bridgelessness, local components, boundary sizes, and deltas.

A different voltage assignment on the same base graph also refutes
universal exact zero-neutrality.  Put voltage one on cotree edges
\(10,14\).  The resulting lift has graph6 encoding
```text
[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P@??AGG??
```
At vertex \(2\), edge pair \(7,8\), its three local candidates are
\[
                     (04,4,-2),\quad(14,4,-2),\quad(23,4,+2), \tag{9}
\]
where each triple records pair, boundary size, and Euler delta.
Therefore none of the three switches is neutral.  The weaker target
(3) survives because the maximum delta in (9) is \(+2\).
The literal checker is
```text
python3 scratch/check_d5_local_zero_two_lift_no_go.py
```

Finally, put voltage one on cotree edges \(10,14,17\).  The lift has
graph6 encoding
```text
[???????????_?O?D??g?__H@?PB??c_?aA?COO?@S??Ag?AE??@H??P?_?AGO??
```
and at vertex \(2\), edge pair \(7,8\), all three local data are
\[
                     (04,4,-2),\quad(14,4,-2),\quad(23,4,-2). \tag{10}
\]
This refutes (3).  It is not an artefact of a state with an immediate
improving move: among
all 24 nonempty component switches the delta histogram is
\[
                              \{-2:12,\ 0:12\}.
\]
Hence the state is a local \(\chi\)-maximum.  The literal checker
```text
python3 scratch/check_d5_local_max_two_lift_no_go.py
```
verifies the graph and flow equations, all 24 nonempty switches, local
maximality,
the three local components, and the following surviving global fact:
the hypergraph of the 12 neutral components is connected.  The two
displayed adjacent edges have neutral-component-chain distance two,
and the maximum neutral distance is three.

This cover explains the exact gap in a naive four-terminal proof.
Formula (6) performs its splices at the remote vertex sets
\[
 B(bc,K_{bc}),\quad B(ad,K_{ad}),\quad B(ae,K_{ae}),          \tag{11}
\]
not at the shared corner edge.  A cover can concatenate the three
return paths and multiply every splice set while retaining a neutral
or positive circuit-count move.  A valid tropical-Plücker argument
must therefore compare the circuit-count changes themselves, not bound
the number of remote breaks.

A tempting intermediate strengthening was:

> if none of the three components is closed, then all three switches
> are neutral.

It holds through the complete order-12 census but is false at order
14.  One first counterexample is on
`M??CBAPUAc@oJ?h??`; after converting the producer's edge order to the
Python order, the displayed state is
```text
03 09 0a 0c 14 18 14 12 06 11 18 09 0c 18 14 0a 06 0c 11 12 18
```
at vertex \(2\), incident edge pair \(6,7\).  The three deltas are
\[
                         0,\quad0,\quad+1,
\]
and all three boundary-twist sets in (11) are nonempty.  Thus this
counterexample does not hurt (3), but it prevents replacing (3) by
that stronger dichotomy.

The complete order-14 feature census sharpens the surviving target:

* in every local triple the minimum boundary size is \(0\) or \(2\);
* 22,389,110 triples have a zero boundary size;
* the remaining 182,446 triples have boundary-size multiset
  \((2,2,2)\) or \((2,2,4)\); and
* none violates the consequent two-break neutrality.

Thus (7), together with Lemma 3.3, is exactly sufficient inside the
order-14 census but not universally.  The feature report is
```text
scratch/d5-local-closed-or-two-neutral-order14.jsonl
```
and its first frozen version has SHA-256
```text
f9ceb777a4d99a46b035aeda6167ee6fc1e57467feb96f9606154a9962a64899
```
The report explicitly pairs each individual boundary size with its
delta.  All 13,368,874 local candidate switches of boundary size two
are neutral.

## 5. Complete finite evidence

Across all 480 biconnected simple cubic graphs on 14 vertices:

| quantity | count |
|---|---:|
| normalized \(D_5\)-flows | 537,418 |
| adjacent-edge local triples | 22,571,556 |
| triples with no zero delta | **0** |

The frozen report is
```text
scratch/d5-local-neutral-triangle-order14.jsonl
```
with SHA-256
```text
6b866459c9a9c438373f0029a533c8b4abfba07cd7a468a91ff4901d00420f45
```
and is checked by
```text
python3 scratch/verify_d5_local_neutral_triangle_order14_report.py
```
including regeneration of the canonical `geng` graph sequence.

An independent Python implementation gives:

| order | graphs | normalized flows | local triples | failures |
|---:|---:|---:|---:|---:|
| 10 | 18 | 1,525 | 45,750 | 0 |
| 12 | 81 | 25,960 | 934,560 | 0 |

These are exact finite results, not a universal proof.

## 6. The surviving global statement

The local-maximum two-lift above proves that neutral-hypergraph connectivity
cannot be obtained by placing every adjacent graph-edge pair on one
neutral component.  The displayed adjacent pair has no such component,
but is joined by a chain of two neutral components.

The corresponding one-state connectivity statement is also false.  A
second 28-vertex lift, checked by
```text
python3 scratch/check_d5_local_chi_max_neutral_connectivity_no_go.py
```
is a local \(\chi\)-maximum with ten neutral factor components, but their
support hypergraph has one 36-edge block and six isolated edges.  This
does not refute the terminal-plateau theorem: its complete equal-\(\chi\)
component has an improving exit.

Any surviving statement must therefore be global over an entire terminal
equal-\(\chi\) plateau, not a static connectivity assertion at one state.

Connectivity alone does **not** imply an immediate distance-lowering
move.  The smallest no-go already occurs at order 8.  On graph6
```text
GCrb`o
```
with state
```text
03 05 06 06 05 03 03 05 06 06 05 03
```
and roots \(1,7\), the state is a local \(\chi\)-maximum, has
factor-chain distance
two, and has eleven neutral first moves.  Every one keeps distance two.
The explicit neutral rescue has distance sequence
\[
                              2,\ 2,\ 1.
\]
The self-contained literal checker is
```text
python3 scratch/check_d5_local_chi_max_direct_chain_descent_no_go.py
```
and verifies every first switch plus the displayed two-switch rescue.
Therefore a proof of the terminal chain theorem must allow traversal of
a fixed-distance neutral plateau.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the local target,
derived the corner-pairing reduction, implemented the independent
finite audits, found and checked the failed strengthenings, and drafted
this note.  The proved statements above are elementary and written out
for human checking; the universal local inequality and FiveCDC remain
open.
