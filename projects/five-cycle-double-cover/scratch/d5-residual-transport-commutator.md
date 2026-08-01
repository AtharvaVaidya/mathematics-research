# Residual transport between complementary root triangles

Date: **2026-07-28**

Status: **EXACT SYMBOLIC FORMULA AND COMPLETE ORDER-12 EVIDENCE /
UNPROVED UNIVERSAL LEMMA / NOT A FIVECDC RESOLUTION**.

## 1. Normal form

Work in a saturated disjoint-root state
\[
                         q(r)=ab,\qquad q(s)=xy,
\]
where \(a,b,x,y,h\) are the five coordinates and \(h\) is the unique
coordinate outside the root labels.

At \(r\), use the oriented line triangle
\[
                         ab\to ah\to bh\to ab
\]
with switch sequence
\[
                         R=(bh,\ ab,\ ah).                      \tag{1}
\]
If its dynamically selected circuits are \(K_1,K_2,K_3\), put
\[
                         Z=K_1+K_2,\qquad H=K_1+K_3.            \tag{2}
\]
Assuming all intermediate states are root-bad, all three circuits
contain \(r\) and omit \(s\), so \(Z,H\) are root-avoiding Eulerian
subgraphs.  Direct coordinate tracking gives
\[
        \Delta C_a=Z+H,\qquad \Delta C_b=Z,\qquad \Delta C_h=H. \tag{3}
\]

The hidden transposition of (1) is \(ab\).  For either
\(t\in\{x,y\}\), there are two complementary star triangles at \(s\)
with the same hidden transposition:
\[
\begin{aligned}
S_{t,+}&=(at,\ ab,\ bt),\\
S_{t,-}&=(bt,\ ab,\ at).                                     \tag{4}
\end{aligned}
\]
The other coordinate of \(\{x,y\}\) remains fixed along the star.

If \(U=L_1+L_2,V=L_1+L_3\) are the star's support and residual, then
\[
\begin{array}{c|ccc}
&\Delta C_a&\Delta C_b&\Delta C_t\\ \hline
S_{t,+}&U&U+V&V\\
S_{t,-}&U+V&U&V.
\end{array}                                                   \tag{5}
\]
All other coordinate sets are fixed.

Equations (3)--(5) are exact for dynamically rerouted components.  They
do not replace those components by fixed edge sets.

### A proved fact at the \(H=0\) endpoint

Suppose the line lift (1) remains root-bad and \(H=0\).  Then
\(K_1=K_3=:K\).  Put \(Z=K+K_2\).  The following local classification
is exact.  On an edge of \(K\), write \(0\) if it is outside \(K_2\)
and \(1\) if it is inside \(K_2\).  Up to renaming the two coordinates
\(x,y\), normalize \(a=0,b=1,h=2\).  Its complete list of labels
during the three switches is
\[
\begin{array}{c|ccc}
{\bf 1}_{K_2}&q&q_1&q_2\\ \hline
0&02&01&01\\
0&13&23&23\\
0&14&24&24\\
1&01&02&12\\
1&23&13&03\\
1&24&14&04.
\end{array}                                                   \tag{5a}
\]
This is obtained simply by requiring the edge to be active first in
\(Y_{12}(q)\), then (when it belongs to \(K_2\)) in
\(Y_{01}(q_1)\), and finally in \(Y_{02}(q_2)\).

Consequently
\[
                             H=0\quad\Longrightarrow\quad Z\ne0. \tag{5b}
\]
Indeed, if \(Z=0\), then \(K=K_2\), so every edge of \(K\) has one of
the three initial labels \(01,23,24\) in the bottom half of (5a).
At a cubic vertex the three incident weight-two labels with xor zero
are exactly the three sides of a triangle on three coordinates.  In
particular, two incident labels share one coordinate.  But \(K\)
contains the root edge \(r\), whose label is \(01\); neither \(23\)
nor \(24\) shares a coordinate with \(01\), and the two circuit edges
at an endpoint of \(r\) must be distinct.  This is impossible.

Thus an \(H=0\) line triangle always has nontrivial hidden monodromy:
its endpoint is obtained by switching \(a,b\) on the nonempty,
root-avoiding Eulerian subgraph \(Z\).  This proves the
``no identity line loop'' entry in the finite table below for every
cubic graph, not only through order 12.  It does **not** yet prove the
radius-two rescue statement.

## 2. Both operation orders

Write \(R(q)\) for the endpoint of (1), when its path remains bad.
Starting from \(R(q)\), a complementary star has newly computed supports
\(U_R,V_R\).  For \(S_{t,+}\), the total coordinate change along
\[
                              R\ \text{then}\ S_{t,+}
\]
is
\[
\begin{aligned}
\Delta C_a&=Z+H+U_R,\\
\Delta C_b&=Z+U_R+V_R,\\
\Delta C_h&=H,\\
\Delta C_t&=V_R.                                             \tag{6}
\end{aligned}
\]

In the reverse order, let \(\bar U,\bar V\) be the star supports at
\(q\), and let \(\bar Z,\bar H\) be the line supports recomputed after
that star.  Then
\[
\begin{aligned}
\Delta C_a&=\bar U+\bar Z+\bar H,\\
\Delta C_b&=\bar U+\bar V+\bar Z,\\
\Delta C_t&=\bar V,\\
\Delta C_h&=\bar H.                                          \tag{7}
\end{aligned}
\]
For \(S_{t,-}\), interchange the placements of the residual in the
\(a,b\) rows according to (5).

Thus \(\bar H\) is the exact transported version of the original line
residual \(H\).  If the two operation orders happened to have the same
endpoint, (6)--(7) would force \(H=\bar H\) and
\(V_R=\bar V\).  Actual component switches need not make the rectangle
close; a rescue or a change of residual is precisely the mixed-square
monodromy.

## 3. Candidate descent lemma

Because every Eulerian subgraph of a cubic graph is a disjoint union of
circuits, define
\[
                         \mu(H)=(|E(H)|,\kappa(H))              \tag{8}
\]
lexicographically, where \(\kappa(H)\) is its number of circuit
components.

The exact candidate is:

> **Residual-transport trichotomy.**  If (1) is an all-bad triangle
> lift with \(H\ne0\), then for at least one of the four complementary
> stars (4), one of the following occurs:
>
> 1. the star from \(q\), the star after \(R\), or \(R\) after the star
>    reaches a root-good state;
> 2. every tested path remains bad and its transported line residual
>    satisfies \(\mu(\bar H)<\mu(H)\);
> 3. the circuits realizing a minimal nondecreasing residual have a
>    structural configuration impossible in a connected cubic graph.

The third branch has not been characterized.  A universal proof of the
first two branches would already be substantial.  Finiteness would let
one iterate strict descent until \(H=0\), at which point the line
triangle is exactly a product of component switches in its hidden
inactive factor \(Y_{ab}\).

That endpoint is not yet a contradiction: a final argument must exploit
the simultaneous hidden-factor collapses at both roots or the closure of
the supposed bad covering.

## 4. Complete finite audit

The audit

```text
python3 scratch/audit_d5_residual_transport_commutator_order12.py
```

checks every biconnected simple cubic graph through order 12, every
normalized \(D_5\)-flow, every ordered disjoint root pair, and both
orientations of every line triangle (1).  For each nonzero
all-intermediate-bad residual it tries all four stars (4) and both
operation orders.

Across 107 graphs:

| quantity | count |
|---|---:|
| nonzero all-bad line residuals | 11,718 |
| accepted by a rescue | 11,076 |
| accepted by strict residual descent | 642 |
| descents to \(H=0\) | 622 |
| descents to a smaller nonzero edge support | 20 |
| equal-edge descents using fewer components | 0 |
| failures | **0** |

The maximum initial residual had ten edges and two components.

The same traversal separately audited every all-bad line loop with
\(H=0\).  There were 22,197 such loops, all with \(Z\ne0\).  Starting
from either endpoint of the line loop, arbitrary root-component moves
gave:

| \(H=0\) endpoint quantity | count |
|---|---:|
| rescue radius one | 20,805 |
| rescue radius two | 1,392 |
| radius greater than two | **0** |

The maximum remaining support \(Z\) had twelve edges.

The order-14 girth-five, cyclically five-edge-connected witness in
`scratch/d5-triangle-residual-girth5-cyclic5.md` is also accepted by the
rescue branch.  Its reverse star-first order collapses the displayed
8-cycle residual to zero, while line-first followed by the same star
rescues the roots.

The bounded escape cannot be restricted to complementary stars with the
old hidden pair.  The minimum order-12 cage in
`scratch/d5-hzero-complementary-star-cage.md` has \(H=0\), a four-edge
\(Z\), and four literal-identity complementary stars in both orders.
It is nevertheless rescued by two unrestricted root-component moves.
Thus the finite endpoint statement is a radius-two root-transition
claim, not a fixed-hidden-pair claim.

## 5. Scope

The table is exact finite evidence, not an induction.  It shows that
plain support size is already enough in every strict descent through
order 12; the component tie-break in (8) was never used.  It does not
prove that a larger cubic graph cannot contain a closed nondecreasing
residual cage.

The promising human target is to take a smallest nonzero \(H\), expand
the four mixed line/star rectangles using (6)--(7), and show that
failure of rescue and failure of descent force their first and third
circuits to have identical transition pairings on every component of
\(H\).  Such a pairing identity is the prospective forbidden
configuration in branch 3.  A second required lemma must show that an
\(H=0\) line holonomy forces a rescue within two unrestricted
root-component moves.  Together these would contradict a finite closed
bad covering by strict descent followed by the radius-two endpoint.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the two-order support
formulas, formulated the residual potential, implemented and ran the
complete order-12 audit, and drafted this note.  The formulas, counts,
and checker are exposed for human verification.  This is not peer
review and is not presented as a resolution of FiveCDC.
