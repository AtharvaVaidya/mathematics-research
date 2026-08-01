# A component-parity criterion for five-point Oum support

Date: 2026-07-28

Status: **HUMAN PROOF / EXHAUSTIVELY CHECKED LOCAL AND SMALL-FLOW
CLASSIFICATION / EXACT SELECTION TARGET / NOT A FIVEDC PROOF**.

## 1. Setup

Let \(W=\mathbb F_2^3\), and let
\(\phi:E(G)\to W-\{0\}\) be a nowhere-zero flow on a loopless cubic
graph.  Thus the three incident values at every vertex are distinct and
xor to zero.

Let \(B\subset W\) have three points.  Its affine span is a four-point
affine plane
\[
 A=b_0+U_0,
\]
where \(U_0\leq W\) is a two-dimensional linear subspace.  Write
\[
 a^*=A-B,\qquad A'=W-A,\qquad S=W-B=A'\cup\{a^*\}.
\]
Choose an arbitrary base point \(z\in A'\).

A compatible pair labelling is a map
\[
 \lambda(e)=\{x_e,y_e\}\subset W,\qquad x_e\ne y_e,
\]
such that
\[
 x_e+y_e=\phi(e)
\]
and, at each graph vertex, every point of \(W\) occurs an even number
of times among the three incident pairs.  We ask when such a labelling
can be supported entirely in the prescribed five-set \(S\).

Let \(h_0\in W^*-\{0\}\) be the unique functional with
\(\ker h_0=U_0\).  At a graph vertex \(v\), let
\[
 U_v=\{0\}\cup\{\phi(e):e\ni v\}
\]
be the incident flow plane and let \(h_v\) be its nonzero normal.
Finally, let
\[
 E_0=\{e:\phi(e)\in U_0\}.
\]

## 2. Local triangle lemma

At a cubic vertex, three compatible two-point labels form a triangle.
Indeed, they form a three-edge loopless multigraph on \(W\) in which
every point has even degree.  The three edge differences are distinct,
so the only possibility is a simple triangle.  Conversely, a triangle
has even point degrees.  Its three pair differences are precisely the
three nonzero vectors of \(U_v\).

The subgraph \((V(G),E_0)\) has degree one or three at every vertex:

* if \(U_v=U_0\), equivalently \(h_v=h_0\), all three incident edges
  belong to \(E_0\);
* otherwise \(U_v\cap U_0\) is a one-dimensional subspace, so exactly
  one incident flow value belongs to \(U_0\).

Call the first kind **special** and the second kind a **leaf vertex** of
\(E_0\).

### Special vertices

If \(U_v=U_0\), a supported local triangle cannot lie in \(A\), because
\(A\cap S=\{a^*\}\).  It must be
\[
 A'-\{t_v\}
\]
for some \(t_v\in A'\).  These are the four possible local triangles.

For each \(p\in U_0-\{0\}\), the affine plane \(A'\) is partitioned into
two \(p\)-pairs.  Give the pair
\[
 \{z,z+p\}
\]
port bit \(1\), and give the other \(p\)-pair port bit \(0\).  If
\(p_1,p_2,p_3\) are the incident values at a special vertex, then the
three selected port bits satisfy
\[
 x_{p_1}+x_{p_2}+x_{p_3}=0.                 \tag{1}
\]
Moreover, all four even bit triples occur.

To see this, write \(t_v=z+u\) with \(u\in U_0\).  The selected
\(p\)-pair is the one not containing \(t_v\).  Its bit is therefore one
exactly when \(u\notin\{0,p\}\).  For
\(\{p_1,p_2,p_3\}=U_0-\{0\}\), the four choices of \(u\) give
```text
000, 011, 101, 110.
```

### Leaf vertices

Suppose \(U_v\ne U_0\).  Write the unique incident value in \(U_0\) as
\(p\), and the other two as \(q,r\), so
\[
 p=q+r,\qquad q,r\notin U_0.
\]
There is exactly one supported local triangle:
\[
 \{a^*,a^*+q,a^*+r\}.                       \tag{2}
\]
The label on the \(p\)-edge is the \(p\)-pair
\[
 \{a^*+q,a^*+r\}\subset A'.
\]
Its port bit is forced; denote it by \(\ell_v\).

For either outside value, say \(q\notin U_0\), the forced label is
\[
 \{a^*,a^*+q\}.                              \tag{3}
\]
Consequently a graph edge outside \(E_0\) receives the same forced pair
from both endpoints.  Compatibility outside \(E_0\) is automatic.

There is also a coordinate-free formula for the forced bit.  Put
\[
 w=z+a^*.
\]
Then \(w\notin U_0\), and
\[
 \ell_v=(h_v+h_0)(w).                        \tag{4}
\]
Indeed, the forced \(p\)-pair equals the base pair
\(\{z,z+p\}\) exactly when \(w\in U_v\), equivalently
\(h_v(w)=0\).  Since \(h_0(w)=1\), this is (4).

## 3. Component criterion

> **Five-point support criterion.**  A compatible pair labelling
> supported in \(S\) exists if and only if, for every connected component
> \(Q\) of \((V(G),E_0)\),
> \[
>                    \bigoplus_{v\in L(Q)}\ell_v=0,            \tag{5}
> \]
> where \(L(Q)\) is the set of its degree-one vertices.

**Proof.** Give every edge \(e\in E_0\) one binary variable \(x_e\),
encoding which of the two \(\phi(e)\)-pairs in \(A'\) labels the edge.
The local classification gives exactly the equations
\[
\begin{aligned}
 x_e&=\ell_v
       &&\text{at a degree-one vertex }v,\\
 \bigoplus_{e\ni v}x_e&=0
       &&\text{at a degree-three vertex }v.
\end{aligned}                                                   \tag{6}
\]
Equality of the two endpoint bits is precisely edge-label
compatibility in \(E_0\), while (3) already handles every other edge.

For a connected component \(Q\), system (6) is its vertex-edge
incidence system over \(\mathbb F_2\), with right-hand side \(\ell_v\)
at leaves and zero elsewhere.  The image of the incidence matrix of a
connected loopless graph is exactly the even-parity subspace.  Hence
(6) is soluble exactly when the xor of its right-hand sides is zero,
which is (5).  A solution determines one of the four allowed local
triangles at every special vertex and therefore reconstructs the full
supported pair labelling. \(\square\)

The criterion applies to every component, cyclic or acyclic.  If \(Q\)
is a tree, the port solution is unique.  If its cycle rank is
\(\beta(Q)\), a soluble component has \(2^{\beta(Q)}\) port solutions.
Thus a cycle creates freedom but does not remove the parity condition.

Formula (4) gives a base-point-free form.  Define
\[
 \sigma_Q=\sum_{v\in L(Q)}(h_v+h_0)\in W^*.
\]
Changing \(z\) adds an edge-direction gauge to all port bits and
preserves every special-vertex equation.  Equivalently,
\(\sigma_Q\) annihilates \(U_0\), so
\(\sigma_Q\in\{0,h_0\}\).  Since \(h_0(w)=1\), condition (5) is simply
\[
                         \sigma_Q=0.          \tag{7}
\]
This shows explicitly that the criterion is independent of the
auxiliary choice of \(z\).

## 4. The forest-coordinate specialization

Suppose now that
\[
 \phi=(1_{F_1},1_{F_2},1_{F_3})
\]
comes from three fundamental completions.  If \(h_0\) is a coordinate
functional, say the third one, then
\[
 E_0=E(G)-F_3.
\]
This is a forest contained in \(T_3\).  The general criterion therefore
becomes a leaf-parity test on every component of a literal zero forest.

With coordinates normalized so
\[
 U_0=\{0,1,2,3\},\qquad w=4,
\]
a leaf bit has a particularly transparent meaning:
\[
 \ell_v=1
 \quad\Longleftrightarrow\quad
 \text{one of the two incident edges outside \(E_0\) has flow value \(4\)}.
                                                               \tag{8}
\]
Consequently (5) is equivalent to saying that, after contracting every
component of \(E-F_3\), the edges of pure value \(4\) have even degree
at every contracted vertex.

For a type-A star fibre, \(E-F_3\) contains the unique star edge assigned
to \(T_3\), so the distinguished central vertex is a leaf of one of
these forest components.  This is the sharp remaining selection
problem:

> Can the three trees in every star fibre be chosen so that, for one
> coordinate \(i\), the pure-\(i\) flow edges have even incidence on
> every component of \(E-F_i\)?

A positive answer is sufficient for FiveCDC.  It is not proved here.

## 5. Exhaustive validation

The independent checker
`verify_jaeger_support5_component_criterion.py`:

1. enumerates all seven incident flow planes and confirms the four
   even port triples in the special case and the unique supported
   triangle in each of the six nonspecial cases;
2. enumerates every nowhere-zero \(\mathbb F_2^3\)-flow on every
   connected simple cubic graph through order eight;
3. independently solves the original supported-local-triangle CSP and
   compares it with (5); and
4. checks the explicit 34-vertex strong-snark support-five witness.

The small-flow census contains 30,744 literal flows on eight graphs.
For the canonical plane \(U_0=\{0,1,2,3\}\), 11,592 admit a supported
labelling.  Direct CSP existence and the component criterion agree in
all 30,744 cases.  The number of supporting planes per flow is:

| supporting planes | flows |
|---:|---:|
| 0 | 2,520 |
| 1 | 10,920 |
| 2 | 1,848 |
| 4 | 13,104 |
| 5 | 672 |
| 6 | 1,008 |
| 7 | 672 |

Thus the criterion is not automatic for an arbitrary nowhere-zero
flow: already at order eight, 2,520 literal flows fail it for every
plane.

For the 34-vertex non-thin witness, precisely one of the seven planes
passes:
```text
U0 = {0,1,2,3}.
```
Its \(E_0\) forest has twelve components: eight isolated edges, three
four-vertex cubic stars, and one six-vertex tree with four leaves.
Every component has leaf-bit xor zero.  Each of the other six planes has
between four and eight parity-failing components.

The support-constrained SAT driver
`audit_jaeger_star_all_directions_sat.cpp` separately finds a
five-point-supported representative for all 5,646 star fibres in all
simple 3-edge-connected cubic graphs through order fourteen.  It also
finds one in all 34 star fibres of the non-thin strong snark.  The
3-edge-connectivity premise matters: the 8-vertex bridgeless,
2-edge-connected graph
```text
GCXmd_
```
has no five-point-supported representative in any of its eight star
fibres.

These are finite results, not a universal selection theorem.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the port
criterion, corrected its component quantifier and parity convention,
proved the local and global equivalences, implemented the exhaustive
checker, and ran the finite audits.  The displayed proof and checker
are intended for human verification.  This is not independent peer
review and is not claimed as a resolution of FiveCDC.
