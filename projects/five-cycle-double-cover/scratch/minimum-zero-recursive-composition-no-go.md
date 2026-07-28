# The 130-vertex matching gap does not amplify under its natural gluings

## Status

**PROVED COMPOSITION NO-GO / NOT A FIVE-CDC COUNTEREXAMPLE.**

The 130-vertex graph in
`search/minimum-zero-exchange-countermodel-130v-20260727/` has minimum
exact-zero matching size five, while its minimum extending matching has
size six.  That gap is real, but it is not inherited by the natural
self-gluing operations.

For the canonical recursion that marks the five new joining edges, the
first recursive graph has 270 vertices and

\[
  r_M=e_M=12,
\]

where \(r_M\) is the minimum size of an exact-zero matching of an
\(\mathbb F_2^2\)-flow and \(e_M\) is the minimum size of such a
matching that extends to the matching/four-flow certificate.  At every
later level the two quantities remain equal.

The two literal ways to reuse one half of each of the five original
marked core edges also collapse the gap immediately:

\[
  r_M=e_M=6
\]

on both resulting 270-vertex graphs.

Every graph discussed here has a directly checked standard 5-CDC.  No
FiveCDC UNSAT claim is made.

## 1. Why a chain of the original five-poles is not defined

Let \(P_0\) be one 65-vertex half of the reported construction: one
60-vertex core with the five marked edges subdivided.  Its five
degree-two vertices form a single five-terminal interface.

Whole-interface gluing consumes that only interface.  If copies of
\(P_0\) are treated as macro-vertices and every gluing pairs all five
terminals of one copy with all five terminals of another, every
macro-vertex has degree one.  The macrograph is therefore a disjoint
union of pairs.  Its only connected member is the original two-pole
gluing.

A chain or tree requires at least two separately designated interfaces
per atom, or it must send different terminals to different neighbours.
Either change defines a new multipole and a new boundary relation; it
is not recursive composition of this one-port atom.

## 2. Exact boundary composition law

Let \(P\) be any graph pole with five degree-two boundary vertices and
degree three elsewhere.  For a flow on its internal edges, define the
boundary value

\[
 s_i=x_i+y_i\in\mathbb F_2^2
\]

at terminal \(i\), where \(x_i,y_i\) are the two incident internal edge
values.  Let \(C_P(s)\) be the minimum number of internal zero edges
among flows which:

- satisfy xor conservation at every degree-three vertex;
- have boundary state \(s=(s_1,\ldots,s_5)\); and
- have a matching as their internal exact-zero set.

Put \(C_P(s)=+\infty\) if no such flow exists and write

\[
 z(s)=|\{i:s_i=0\}|.
\]

Summing the flow equations over all internal degree-three vertices gives
the necessary conservation law

\[
 s_1+s_2+s_3+s_4+s_5=0.                         \tag{1}
\]

It is the only feasibility restriction in the frozen state table below.

When two identical copies of \(P\) are joined terminal by terminal, the
joining edge at position \(i\) must have the same value \(s_i\) at both
ends.  It is zero exactly when \(s_i=0\).  Hence the exact min-plus law is

\[
 r_M(\operatorname{close}(P))
   =\min_s\{\,2C_P(s)+z(s)\,\}.                  \tag{2}
\]

There is a similarly exact law for making a new pole.  Join two copies
of \(P\), then subdivide each new joining edge; the five subdivision
vertices are the next boundary.  Let the two segment-value vectors be
\(\alpha,\beta\).  The new boundary state is
\(\sigma=\alpha+\beta\), coordinatewise.  The two segments contribute
\(z(\alpha)+z(\beta)\) zero edges.  At a new boundary vertex they may
not both be zero, because the zero set is a matching.  Therefore

\[
\begin{split}
C_{P^+}(\sigma)=
 \min_{\substack{\alpha+\beta=\sigma\\
                  \neg(\alpha_i=\beta_i=0)\ \forall i}}
\{C_P(\alpha)+C_P(\beta)+z(\alpha)+z(\beta)\}.
                                                        \tag{3}
\end{split}
\]

Equations (1)--(3) are identities, not heuristic recurrences.  Their
proof is just restriction and gluing of flows.  The matching condition
at an old boundary is already included in \(C_P\); the displayed
condition is exactly the additional matching condition at each new
subdivision vertex.

## 3. The canonical connector recursion

Let \(G_1\) be the reported 130-vertex graph, and let \(J\) be its five
joining edges.  Split every edge of \(J\) once and call the resulting
135-vertex pole \(P_1\).  Closing two copies of \(P_1\) is the canonical
270-vertex recursion \(G_2\).

There are \(4^4=256\) five-term boundary states satisfying (1).  The
frozen table gives an explicit compatible flow for every one and checks
six internal zero edges in every row.  A single CNF allows the boundary
state to vary freely and asks for at most five internal zeros.  Its
independently checked LRAT proof is UNSAT.  Consequently

\[
                 C_{P_1}(s)=6
\quad\text{for every state satisfying (1).}             \tag{4}
\]

Equation (2), or simply the leaf-pole lower bound, gives

\[
                         r_M(G_2)\ge12.                  \tag{5}
\]

The JSON certificate contains a 5-CDC of \(P_1\) with six internal
edges labelled \(01\).  Its five conceptual boundary-edge labels all
belong to

\[
                         \mathcal T=\{23,24,34\}.         \tag{6}
\]

Closing two identical copies with those boundary labels gives a
standard 5-CDC of \(G_2\) whose \(01\)-support has size twelve.  Direct
parity checking verifies the cover and the matching property.  Thus

\[
                         r_M(G_2)=e_M(G_2)=12.            \tag{7}
\]

### Human-checkable cover induction

The positive certificate propagates without SAT.  Let
\(\tau=(2\,3\,4)\) permute the three coordinates in (6).  Suppose a pole
has a 5-CDC with boundary labels \(\lambda_i\in\mathcal T\).  Use one
copy unchanged and apply \(\tau\) to every coordinate name in a second
copy.  Give the two joining segments at the new terminal the labels
\(\lambda_i\) and \(\tau(\lambda_i)\).  These are two distinct edges of
the triangle on \(\{2,3,4\}\); give the conceptual new boundary edge the
third label

\[
                         \tau^2(\lambda_i).
\]

The three local membership vectors xor to zero.  All new labels remain
in \(\mathcal T\), so none is \(01\), and the number of \(01\)-edges
doubles.  This constructs the next pole certificate.

Every later closed graph is a disjoint union of \(P_1\) leaf interiors
plus joining segments.  Restricting any exact-zero matching flow to a
leaf \(P_1\) invokes (4), so every leaf contributes at least six zeros.
The cover induction attains that lower bound and adds no \(01\)-labelled
joining edge.

Indexing the reported graph as \(G_1\), the canonical recursion therefore
satisfies, for every \(k\ge2\),

\[
\begin{aligned}
 |V(G_k)| &= 140\cdot2^{k-1}-10,\\
 r_M(G_k)&=e_M(G_k)=6\cdot2^{k-1}.              \tag{8}
\end{aligned}
\]

Thus the initial gap

\[
 e_M(G_1)-r_M(G_1)=1
\]

becomes zero at the first recursive step and remains zero forever.  The
required support also remains far below the trivial matching ceiling:

\[
6\cdot2^{k-1}
 <
\frac{140\cdot2^{k-1}-10}{2}.
\]

There is no mechanism here for pushing extending supports “beyond all
allowable values.”

## 4. Reusing the marked core halfedges

In the sorted 130-vertex edge list, the two halfedge choices in the first
60-vertex core are

\[
\begin{aligned}
L&=\{41,54,66,78,90\},\\
R&=\{45,58,70,82,94\}.
\end{aligned}
\]

Self-gluing two copies of \(G_1\) after subdividing \(L\), or after
subdividing \(R\), gives a simple cubic graph on 270 vertices and 405
edges.  For each graph:

- a complete exact-zero matching-flow CNF with support at most five is
  UNSAT, with LRAT accepted by two independent checkers; and
- the JSON contains a directly verified standard 5-CDC whose
  \(01\)-support is a matching of size six.

Hence both literal marked-halfedge recursions satisfy

\[
                         r_M=e_M=6.                       \tag{9}
\]

They do not inherit even an additive copy of the original gap.  More
elaborate asymmetric choices among the many descendant halfedges would
define further marked states and require their own boundary tables;
(9) is not silently generalized to every imaginable substitution.

The base 130-vertex graph itself also has a frozen size-six extending
cover whose support avoids all five joining edges.  The interface
therefore does not force every extending support to pay even one zero
edge at that cut.

## 5. Certificates and independent checking

The checker uses its own graph6 parser and independently reconstructs
all graphs.  The JSON contains:

- all 256 boundary states of \(P_1\), with a complete 200-edge flow for
  each;
- the six-zero boundary-labelled 5-CDC seed used in the induction;
- a size-six extending cover of \(G_1\) avoiding its interface; and
- size-six standard 5-CDCs for both marked-halfedge controls.

For every checked five-cover, the checker also derives the
\(\mathbb F_2^2\)-flow directly.  Assign the five coordinates the
columns

\[
                         0,0,1,2,3\in\mathbb F_2^2
\]

and give an edge labelled \(ij\) the value \(a_i+a_j\).  Eulerian
parity makes this a flow, and its value is zero exactly on label \(01\).
Thus the claimed \(01\)-support sizes are literal exact-zero matching
sizes, not merely cover statistics.

For an edge \(e\), the lower-bound CNFs use variables

\[
 z_e,\quad b^0_e,\quad b^1_e.
\]

They encode \(z_e\leftrightarrow(b^0_e=b^1_e=0)\), native three-edge xor
parity in CNF at each cubic vertex, pairwise matching clauses for zero
edges, and a sequential at-most-five counter.  The pole CNF omits parity
only at its five degree-two boundary vertices.  It leaves their boundary
values unrestricted, so its UNSAT proof establishes the uniform lower
bound in (4), not merely a lower bound for selected table rows.

Run:

```sh
python3 scratch/minimum_zero_recursive_composition_checker.py \
  --check-proofs
```

The checker regenerates all three CNFs byte-for-byte, validates every
positive witness by direct semantics, and runs both `lrat-check` and
CakeML `cake_lpr` on every LRAT.

## 6. Exact scope

This audit proves that the reported matching-gap gadget is a countermodel
to the minimum-support extension route, but not an amplifying obstruction.
It does not prove a universal theorem about every multipole substitution.
Most importantly, it does not claim a graph without a 5-CDC: all closed
graphs used in the no-go have explicit standard five-covers.

## AI disclosure

OpenAI Codex agents, under human direction, discovered the original
130-vertex gap and performed this independent composition audit.  The
composition equations and cover induction are given above for human
checking.  Every finite lower bound is tied to an explicit CNF and LRAT
accepted by two checkers, while every positive cover is checked directly.
