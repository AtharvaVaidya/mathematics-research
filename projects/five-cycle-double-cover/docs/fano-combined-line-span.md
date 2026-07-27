# The three line-preserving Fano images always span the rainbow defect

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE UNIVERSAL LINEAR LEMMA / UNIVERSAL
PRESCRIBED-LINE QUADRATIC CLEANING REFUTED**.

This note strengthens the fixed-value split-cut duality in
`docs/fano-canonical-join-cut-certificates.md`.  For one fixed Fano line,
the sum of the three initially valid switch images always contains the
rainbow-defect vector.  Consequently a common odd split-cut dual for all
three line values is algebraically impossible.

This does **not** yet give a valid switch sequence or a good Fano line.
There are two nonlinear effects: a line-valued edge can be turned into
zero, and overlapping switches on affine edges contribute a quadratic
correction which is invisible in the sum of the three initial linear
maps.  Section 5 gives an exact coordinate-free replacement for the
misleading idea that only the first effect matters.

## 1. Fixed line and the combined image

Let
\[
 f:E(G)\longrightarrow {\mathbb F}_2^3-\{0\}
\]
be a flow on a finite loopless cubic graph.  Fix a nonzero functional
\(\mu\), let
\[
 L=\ker\mu-\{0\},\qquad A=\{a:\mu(a)=1\},
\]
and let \({\cal K}\) be the components of
\[
 F_L=\{e:f(e)\in L\}.
\]
The subgraph \(F_L\) has degree one or three at every vertex.  Let
\[
 r\in{\mathbb F}_2^{\cal K}
\]
indicate the components on whose boundary all four colors in \(A\)
occur oddly.

For \(t\in L\), translation by \(t\) splits \(A\) into two pairs.  Pick
one pair \(P_t\).  Put
\[
 Z_t=Z_1(G-M_t;{\mathbb F}_2),\qquad M_t=f^{-1}(t),
\]
and, for \(C\in Z_t\), define
\[
 \tau_t(C)_K
   =|C\cap\delta(K)\cap f^{-1}(P_t)|\pmod2.             \tag{1}
\]
The complementary pair gives the same bit because a binary cycle
crosses every cut evenly.  Define the combined initial image
\[
 {\cal W}_L=\sum_{t\in L}\operatorname{im}\tau_t.       \tag{2}
\]

> **Combined-line span theorem.**
> \[
>                         r\in{\cal W}_L.               \tag{3}
> \]

The theorem uses all three values of \(L\).  It is false in general that
one prescribed \(\operatorname{im}\tau_t\) contains \(r\).

## 2. Common-dual formulation

Suppose (3) fails.  Linear duality gives a vector
\(y\in{\mathbb F}_2^{\cal K}\) such that
\[
 y\mathbin\cdot r=1,\qquad
 y\mathbin\cdot\tau_t(C)=0
 \quad(t\in L,\ C\in Z_t).                              \tag{4}
\]
Let \({\cal Y}\) be the support of \(y\) and put
\[
 U=\bigcup_{K\in{\cal Y}}V(K).
\]
The same calculation as in the fixed-value split-cut theorem says that
\[
 R_t=\delta(U)\cap f^{-1}(P_t)                          \tag{5}
\]
is a cut of \(G-M_t\), now for all three \(t\) and for the **same**
shore union \(U\).

An invertible linear change of flow coordinates lets us normalize
\[
 L=\{1,2,3\},\qquad A=\{4,5,6,7\},
\]
where addition is bitwise XOR.  Choose
\[
 P_t=\{4,4+t\}\quad(t=1,2,3).                           \tag{6}
\]
Let \(u:V(G)\to{\mathbb F}_2\) indicate \(U\).  For each \(t\), choose
\(x_t:V(G)\to{\mathbb F}_2\) whose cut in \(G-M_t\) is \(R_t\).

Write the state at a vertex as
\[
                    q=(u,x_1,x_2,x_3).                 \tag{7}
\]
Across an edge, the possible nonzero state differences are forced:

| flow color | possible active state difference |
|---:|:---|
| \(1\) | \((0;100)\) |
| \(2\) | \((0;010)\) |
| \(3\) | \((0;001)\) |
| \(4\) | \((1;111)\) |
| \(5=4+1\) | \((1;100)\) |
| \(6=4+2\) | \((1;010)\) |
| \(7=4+3\) | \((1;001)\) |

The zero state difference is also allowed in every row.  For a line
color \(t\), the cut \(x_t\) may cross its deleted \(M_t\)-edge while
the other two cuts cannot.  For an affine color, (5)--(6) give exactly
the last four rows.

## 3. Telescoping proof

For \(q=(u,x_1,x_2,x_3)\), define
\[
 {\cal A}(q)=
 \bigl(
 u(x_2+x_3),\
 u(x_1+x_3),\
 x_1x_2+x_1x_3+x_2x_3
 \bigr)\in{\mathbb F}_2^3.                              \tag{8}
\]

The seven rows above give the pointwise identity
\[
 \bigl({\cal A}(q_v)+{\cal A}(q_w)\bigr)\mathbin\cdot f(vw)
 =
 \begin{cases}
 1,&f(vw)=4\text{ and }u(v)\ne u(w),\\
 0,&\text{otherwise}.
 \end{cases}                                            \tag{9}
\]
Here the dot is the ordinary binary dot product.

For completeness, the active cases are immediate from (8):

* toggling \(x_1,x_2,x_3\) on colors \(1,2,3\), respectively,
  leaves the corresponding dot product unchanged;
* on color \(4\), toggling \(u,x_1,x_2,x_3\) changes
  \(x_1x_2+x_1x_3+x_2x_3\) by \(1\);
* on colors \(5,6,7\), the change in the relevant \(u\)-term is
  cancelled by the change in the quadratic term.

Sum (9) over the edges.  Regrouping the left side at vertices gives
\[
 \begin{aligned}
 \sum_{vw\in E(G)}
   \bigl({\cal A}(q_v)+{\cal A}(q_w)\bigr)\cdot f(vw)
 &=
 \sum_{v\in V(G)}
   {\cal A}(q_v)\cdot
   \left(\bigoplus_{e\ni v}f(e)\right)\\
 &=0,                                                   \tag{10}
 \end{aligned}
\]
by flow conservation.  The right side of (9) sums to
\[
                   |\delta(U)\cap M_4|\pmod2.           \tag{11}
\]
When the boundaries of the selected \(F_L\)-components are added,
edges between two selected components cancel twice.  Therefore (11)
is exactly \(y\cdot r\), which is \(1\) by (4).  This contradicts
(10), proving (3). \(\square\)

This is an explicit row-space proof.  It does not use girth, cyclic
edge-connectivity, or a finite census.

## 4. At most two factor components are always cleanable

Every vector in every \(\operatorname{im}\tau_t\) has even Hamming
weight.  Indeed, sum (1) over all \(F_L\)-components.  Each counted
affine edge has its two ends in two factor components and is counted
twice.  Thus every image lies in
\[
 E_{\cal K}:=\left\{z\in{\mathbb F}_2^{\cal K}:
                     \sum_{K\in{\cal K}}z_K=0\right\}.
\]

If \(F_L\) is connected, \(E_{\cal K}=0\), so (3) already gives
\(r=0\).  If \(F_L\) has two components, \(E_{\cal K}\) has dimension
one.  When \(r\ne0\), (3) implies that at least one of the three image
spaces is nonzero, and that image space must contain the unique
nonzero vector \(r\) of \(E_{\cal K}\).  Hence some single initially
valid \(t\)-cycle changes \(r\) to zero.

There is no mixed-switch correction for a single cycle.  Because the
cycle avoids \(M_t\), translation by \(t\) also creates no zero edge.
We have proved:

> **Two-component corollary.**  If \(F_L\) has at most two components,
> then the fixed Fano line \(L\) is good already or is made good by one
> valid line-preserving binary-cycle switch.

This strictly extends the familiar connected-factor observation.

## 5. Tait-colorable graphs have every projection cleanable

There is a second universal positive class.  Suppose \(G\) has a
nowhere-zero \({\mathbb F}_2^2\)-flow \(s=(p,q)\), equivalently a Tait
three-edge-coloring.  Let \(h\) be any binary cycle and put
\[
                         F=E(G)-\operatorname{supp}h.
\]
The cycles \(p,q\) cover every edge, hence certainly cover \(F\).

For a component \(W\) of \(F\), its boundary lies in
\(\operatorname{supp}h\).  Therefore \(|\delta(W)|\) is even.  Flow
conservation for \(s\) makes the boundary parities of its three nonzero
colors equal.  They cannot all be odd, since their sum would make
\(|\delta(W)|\) odd.  Thus all three are even, including the
\((p,q)=(1,1)\) color.  Equations (15)--(16) now show that \(p,q\)
clean the projection \(h\).

> **Tait corollary.**  On a Tait-colorable cubic graph, every binary
> functional projection is two-cycle cleanable.

Consequently an all-seven bad projection search may be restricted
soundly to snarks.

## 6. Exact nonlinear normal form

By (3), there are binary cycles
\[
 C_t\in Z_1(G-M_t;{\mathbb F}_2)\quad(t\in L)
\]
such that
\[
                         \sum_{t\in L}\tau_t(C_t)=r.    \tag{12}
\]
It is important that (12) is only the linearization at the initial
flow.  Even when no line edge becomes zero, an affine edge which lies
in two or three of the \(C_t\) is not described by the sum of its three
initial toggle contributions.

Here is an exact description which avoids that ambiguity.  Include
zero and write
\[
                         K=\ker\mu\cong{\mathbb F}_2^2.
\]
Fix \(b\) with \(\mu(b)=1\).  Every flow \(f'\) with the same
\(\mu\)-projection as \(f\) has a unique expression
\[
                 f'_e=b\,\mu(f_e)+s_e,\qquad s=(p,q),  \tag{13}
\]
where \(p\) and \(q\) are binary cycles.  Conversely every pair of
binary cycles in (13) gives such a flow.  This follows simply by
subtracting the fixed flow \(b(\mu\circ f)\); the remainder is a
\(K\)-valued flow.

Let
\[
                         F_\mu=\{e:\mu(f_e)=0\}.
\]
On an affine edge, \(b+s_e\) is automatically nonzero.  On an edge of
\(F_\mu\), the value is \(s_e=(p_e,q_e)\).  Hence
\[
 f'\text{ is nowhere-zero}
 \quad\Longleftrightarrow\quad
 p_e\lor q_e=1\quad(e\in F_\mu).                       \tag{14}
\]

Now contract each component \(W\) of \(F_\mu\).  Its boundary consists
of affine edges.  The boundary size is even, and the cut-sum of each
binary cycle \(p,q\) is zero.  The parity of the affine color \(b\) is
therefore
\[
\begin{aligned}
 \sum_{e\in\delta(W)}(1+p_e)(1+q_e)
 &=\sum_{e\in\delta(W)}
       (1+p_e+q_e+p_eq_e)\\
 &=\sum_{e\in\delta(W)}p_eq_e.                         \tag{15}
\end{aligned}
\]
Flow conservation makes the four affine-color parities equal, so \(W\)
is rainbow-odd exactly when the last sum in (15) is one.

We have thus reduced line cleaning to the following exact quadratic
problem:

> **Two-cycle normal form.**  The fixed line \(L\) can be made good
> while preserving \(\mu\circ f\) if and only if there are two binary
> cycles \(p,q\) such that
> \[
> \begin{cases}
> p_e\lor q_e=1,&e\in F_\mu,\\
> \displaystyle\sum_{e\in\delta(W)}p_eq_e=0,
>     &W\text{ a component of }F_\mu.
> \end{cases}                                          \tag{16}
> \]
> Equivalently, \(p,q\) cover \(F_\mu\), and the affine edge set
> \(\{e:p_e=q_e=1\}\) has even degree after the components of
> \(F_\mu\) are contracted.

This is also a human-checkable characterization of the true remaining
step.  The span theorem proves that the first-order equations are never
the obstruction; it does **not** solve the quadratic equations (16).

Universal feasibility of (16) for a prescribed line is false.  The
certified package
`search/fano-two-cycle-petersen-countermodel-20260726/` gives a
nowhere-zero Fano flow on the Petersen graph for which the lines
\(\{1,2,3\}\) and \(\{1,6,7\}\) are not cleanable while preserving their
functional projection.

There is a short proof.  For either failed line, \(F_\mu\) is a perfect
matching and contracting it gives \(K_5\).  In a clean lift, the four
affine colors would partition the ten edges of \(K_5\) into four even
subgraphs.  A nonempty even subgraph of simple \(K_5\) has at least
three edges, so one color must be absent.  Choosing the absent color as
affine base makes the residual \(K\cong{\mathbb F}_2^2\)-flow
nowhere-zero on every Petersen edge, which would be a Tait coloring.
The Petersen graph has no Tait coloring, a contradiction.

The same proof gives a reusable obstruction.  Suppose \(F_\mu\) is a
perfect matching, its contraction \(Q\) is simple, and
\[
                         |E(Q)|<4\,\operatorname{girth}(Q).
\]
If a clean lift existed, its four affine-color classes would be even
subgraphs of \(Q\).  Four nonempty classes would violate the displayed
inequality, so one is absent and rebasing again gives a nowhere-zero
\({\mathbb F}_2^2\)-flow on \(G\).  Consequently, when \(G\) is not
Tait-colorable, such a line is necessarily uncleanable.  Petersen has
\(Q=K_5\), so \(10<4\cdot3\).

This countermodel is deliberately narrow.  The other five lines of the
same displayed flow are cleanable, and the graph has an explicit
five-cycle double cover.  Thus it does not refute a theorem asserting
that **some** line can be made good, nor the five-cycle double cover
conjecture.

In fact the package classifies all 64 possible binary functional
projections on Petersen.  Exactly seven are uncleanable: zero and the
six complements of perfect matchings.  The six nonzero failures have
rank five and only their total XOR relation.  The seven projections of
any nowhere-zero three-bit Petersen flow form the nonzero part of a
three-dimensional subspace: lower rank would itself give a Tait
coloring.  At most three projections can therefore be failures.  Hence
every such flow has at least four cleanable lines.

For comparison with the switch language, let an affine edge initially
have color \(b+s\), and put
\[
 c_t(e)=1_{e\in C_t},\qquad
 z(e)=\sum_{t\in L}c_t(e)t.
\]
Its actual change in the \(b\)-color indicator is
\[
 \chi_s(c)=1_{s=0}+1_{s+z=0},                          \tag{17}
\]
whereas the initial linear sum used in (12) is
\[
 \ell_s(c)=\sum_{t\in L}c_t\,1_{s\in\{0,t\}}.          \tag{18}
\]
The two agree when at most one cycle contains the edge and disagree
for every membership pattern of weight at least two.  Thus the exact
rainbow update is the linear update plus the componentwise boundary
sum of
\(\kappa_s(c)=\chi_s(c)+\ell_s(c)\).

Separately, a line edge of initial value \(t+t'\) is turned into zero
exactly when it lies in both \(C_t\) and \(C_{t'}\).  Therefore
\[
 C_t\cap C_{t'}\cap M_{t+t'}=\varnothing
 \qquad(t\ne t')                                      \tag{19}
\]
is the exact zero-avoidance condition for a fixed triple.  Conditions
(12) and (19) alone do not imply cleaning, because they omit the
quadratic correction (17)--(18).  Pairwise edge-disjoint cycles
satisfying (12) are one sufficient special case, but their universal
existence is not proved here.

## 7. Finite audit

`scratch/audit_fano_combined_line_span.py` independently:

1. checks (9) on every state and every allowed transition;
2. reconstructs the retained ten-vertex resistant flow;
3. computes the three valid cycle spaces for each Fano line;
4. verifies \(r\in{\cal W}_L\) for all seven lines; and
5. checks all sixteen mixed-affine discrepancies in (17)--(18);
6. directly evaluates the final flow, rather than trusting its
   linearization, and finds an actual cleaning triple for each of the
   seven lines on that finite flow; and
7. independently enumerates pairs \(p,q\) and verifies (16).

`scratch/audit_fano_two_cycle_corpus.py` additionally builds ordinary
CNFs for (16) on each line of the retained 40-vertex connected
one-switch countermodel and the retained 46-vertex pure-merge
countermodel.  It checks all fourteen CaDiCaL models directly as binary
cycles and reconstructs the resulting nowhere-zero three-bit flows.
Thus neither known connected local countermodel refutes the exact
quadratic formulation.

The Petersen countermodel package independently enumerates its 64
binary cycles and all 4,096 ordered cycle pairs for every line.  Each
failed line has 960 pairs covering its factor, but their product-boundary
defects run through all fifteen nonzero even five-bit vectors and never
zero.  Two 65-variable, 210-clause ordinary CNFs and independently
checked DRAT proofs provide a second certificate.

The finite checks audit the transcription.  The proof of (3) is the
telescoping calculation above.

## AI-use disclosure

The combined image, its common-dual formulation, the telescoping
potential (8), the nonlinear normal form (16), the audit, and this
exposition were developed by OpenAI Codex agents under human direction.
The result is a partial structural lemma plus a countermodel to one
prescribed-line strengthening, not a resolution of the five-cycle
double cover conjecture.  Independent human review is required before
publication.
