# Non-equivariant nodal pullback: exact structure and a local-model no-go

Date: 26 July 2026

## Outcome

Let \(K\) be an algebraically closed field of characteristic zero and
suppose, hypothetically, that
\[
 \Phi=(P,Q):\mathbb A^2_{x,y}\longrightarrow\mathbb A^2_{u,v},
 \qquad J(P,Q)=1,
\tag{1}
\]
has boundary
\[
 P(x,0)=x^2,\qquad Q(x,0)=x^3-x.
\tag{2}
\]
No parity or other equivariance is assumed.  Put
\[
 H(u,v)=u(u-1)^2-v^2.
\tag{3}
\]

This note establishes the exact geometry forced by (1)--(3).

1. There is a squarefree polynomial \(R\) such that
   \[
   H(P,Q)=yR,\qquad R(x,0)=1-x^2.
   \tag{4}
   \]
   Thus the residual divisor meets \(y=0\) transversely and only at
   \((1,0)\) and \((-1,0)\).
2. The normalization fiber product
   \[
   E=\{P=t^2,\ Q=t^3-t\}\subset\mathbb A^3_{x,y,t}
   \tag{5}
   \]
   is étale over \(\mathbb A^1_t\).  Its diagonal section
   \((x,y,t)=(t,0,t)\) is open and closed.  An explicit polynomial
   idempotent separates it from the residual normalization.
3. The residual normalization contains the two cross-lifts
   \[
   (1,0,-1),\qquad (-1,0,1).
   \tag{6}
   \]
   Nonproper residual components are not ruled out by simple
   connectedness: their finite completions may ramify at deleted
   points over finite \(t\).
4. More strongly, all of the divisor, normalization, transverse
   intersection, and finite étale monodromy data above occur in an
   explicit polynomial map which is étale on a Zariski neighborhood
   of the whole nodal pullback and has the required boundary.  Its
   Jacobian fails to be constant only away from that divisor.

Consequently, the nodal divisor and its normalization do **not** by
themselves give an all-degree contradiction.  Any successful use of
this boundary must bring in genuinely global information: constancy
of the Jacobian away from the pullback divisor, control of the
nonproper value set, or a global restriction on the residual
correspondence.

## 1. The residual divisor on the boundary

The curve \(C=V(H)\) is the nodal cubic parametrized by
\[
 \gamma(t)=(t^2,t^3-t).
\tag{7}
\]
Equation (2) implies that \(H(P,Q)\) vanishes on \(y=0\), so
\[
 H(P,Q)=yR
\tag{8}
\]
for a polynomial \(R\).

### Proposition 1

The boundary value of the residual factor is
\[
 \boxed{R(x,0)=1-x^2.}
\tag{9}
\]

#### Proof

Since
\[
 H_u=(u-1)(3u-1),\qquad H_v=-2v,
\]
differentiating (8) in the normal direction and using (2) gives
\[
\begin{aligned}
 R(x,0)
 &=H_u(\gamma(x))P_y(x,0)+H_v(\gamma(x))Q_y(x,0)\\
 &=(x^2-1)\bigl((3x^2-1)P_y(x,0)-2xQ_y(x,0)\bigr).
\end{aligned}
\]
But the boundary value of (1) is
\[
 2xQ_y(x,0)-(3x^2-1)P_y(x,0)=1.
\]
Substitution proves (9).  \(\square\)

Because \(\Phi\) is étale, the pullback of the reduced divisor \(C\)
is reduced.  Hence \(yR\), and therefore \(R\), is squarefree.
Furthermore \(R_x(\pm1,0)=\mp2\).  The line \(V(y)\) and the residual
divisor \(V(R)\) therefore meet transversely at exactly the two
displayed affine points.  The singular locus of the whole pullback is
also exact:
\[
 \operatorname{Sing}V(H(P,Q))=V(P-1,Q).
\tag{10}
\]
Indeed the singular locus of \(C\) is its node \((1,0)\), and
étaleness preserves this local description.

## 2. The normalization fiber product and its idempotent

Write
\[
 A=\frac{P-x^2}{y},\qquad
 B=\frac{Q-(x^3-x)}{y}.
\tag{11}
\]
These are polynomials by (2).  Set
\[
 \delta=t-x,\qquad T=t^2+tx+x^2-1.
\tag{12}
\]
The two equations defining \(E\) become
\[
 yA-\delta(t+x)=0,\qquad yB-\delta T=0.
\tag{13}
\]
Define
\[
 \kappa=B(t+x)-AT.
\tag{14}
\]

### Proposition 2

In the coordinate ring
\[
 \mathcal O(E)=K[x,y,t]/(P-t^2,Q-t^3+t)
\]
one has
\[
 \kappa y=0,\qquad \kappa\delta=0,\qquad
 \kappa^2=\kappa.
\tag{15}
\]
Moreover
\[
 E=E_{\mathrm{diag}}\sqcup E_{\mathrm{res}},
\quad
 E_{\mathrm{diag}}=V(\kappa-1)=V(y,t-x),
\quad
 E_{\mathrm{res}}=V(\kappa).
\tag{16}
\]

#### Proof

Equations (13) are the matrix equation
\[
 \begin{pmatrix}A&-(t+x)\\ B&-T\end{pmatrix}
 \binom y\delta=0.
\]
The determinant is \(\kappa\), so the adjugate identity gives the
first two relations in (15).  On \(y=0,t=x\),
\[
 \kappa
 =2xB(x,0)-(3x^2-1)A(x,0)
 =J(P,Q)(x,0)=1.
\tag{17}
\]
Thus \(\kappa-1\in(y,\delta)\) in \(K[x,y,t]\).  Multiplying this
membership by \(\kappa\) and using the first two relations proves
\(\kappa(\kappa-1)=0\).  On the locus \(\kappa=1\), (15) forces
\(y=\delta=0\); the converse follows from (17).  This proves (16).
\(\square\)

Projection \(E\to\mathbb A^1_t\) is étale, because the relative
Jacobian of its two defining equations with respect to \(x,y\) is
\(J(P,Q)=1\).  It follows in particular that \(E\) is reduced and
normal.  More explicitly, base-changing the finite normalization
\(\mathbb A^1_t\to C\) gives a finite map
\(E\to V(H(P,Q))\).  It is an isomorphism over the dense inverse
image of the smooth locus of \(C\), while its source is normal.
Consequently (5) is the normalization of \(V(H(P,Q))\).

The points
\[
 (x,y,t)=(1,0,-1),\quad(-1,0,1)
\]
satisfy (5).  At either point \(t+x=0\) and \(T=0\), hence
\(\kappa=0\).  They lie on \(E_{\mathrm{res}}\), not on the diagonal
section.  This is the precise algebraic form of branch switching at
the node.

## 3. What nonproper residual components can do

Every irreducible component \(\Gamma\) of \(E_{\mathrm{res}}\) is a
smooth affine curve and
\[
 \pi=\left.t\right|_\Gamma:\Gamma\longrightarrow\mathbb A^1
\tag{18}
\]
is étale and quasi-finite.  Zariski's main theorem places \(\Gamma\)
as an open subcurve of a curve finite over \(\mathbb A^1\).

If \(\pi\) is proper, it is finite étale.  Since
\(\mathbb A^1_K\) has no nontrivial connected finite étale covers,
\(\Gamma\simeq\mathbb A^1\) and \(\pi\) is an isomorphism.  This
only produces another polynomial lift of \(\gamma\); it is not a
contradiction.

If \(\pi\) is not proper, the omitted points in its finite completion
may lie over finite values of \(t\).  Ramification of the completion
is permitted precisely at such deleted points, even though (18) is
étale.  Geometrically these are branches for which \((x,y)\) escapes
to infinity while
\[
 (P(x,y),Q(x,y))\longrightarrow\gamma(t_0)
\]
for a finite \(t_0\).  Thus the ordinary simply-connectedness
argument applies only after a properness statement which is
essentially the missing global issue.

## 4. An exact local-algebraic model

The preceding configuration is not intrinsically contradictory.
Put
\[
 a=x^2-1,\qquad S=y(y+4a),
\tag{19}
\]
and define
\[
\boxed{\begin{aligned}
 P_0&=x^2+\frac{3x^2-2}{8}S,\\
 Q_0&=x(x^2-1)+\frac{x}{2}y
       +\frac{9x}{32}\bigl(2(x^2-1)+y\bigr)S.
\end{aligned}}
\tag{20}
\]

### Proposition 3

The map \(\Phi_0=(P_0,Q_0)\) has the following properties.

1. \(P_0(x,0)=x^2\) and \(Q_0(x,0)=x^3-x\).
2. On the two components of \(D_0=V(S)\),
   \[
   \left.\Phi_0\right|_{y=0}=\gamma(x),\qquad
   \left.\Phi_0\right|_{y=-4(x^2-1)}=\gamma(-x).
   \tag{21}
   \]
3. There are polynomials \(W,V\in K[x,y]\) such that
   \[
   J(P_0,Q_0)=1+SW,
   \tag{22}
   \]
   \[
   H(P_0,Q_0)
   =S\left(-\frac14+SV\right).
   \tag{23}
   \]

Consequently \(\Phi_0\) is étale at every point of \(D_0\), and on a
Zariski neighborhood of \(D_0\) the scheme-theoretic inverse image
of \(C\) is exactly \(D_0\).  The induced map
\[
 D_0\longrightarrow C
\tag{24}
\]
is a connected finite étale cover of degree two.  Its normalization
is two copies of \(\mathbb A^1\), and the two branches are glued
crosswise over the node.

#### Proof

The first two assertions follow immediately from \(S=0\) on both
components and from
\[
 x(x^2-1)+\frac{x}{2}\bigl(-4(x^2-1)\bigr)
 =-x(x^2-1).
\]
Direct differentiation and polynomial division by \(S\) give
(22).  Direct substitution into \(H\), followed by division by
\(S\), gives (23).  Exact formulas for \(W,V\) are recorded and
checked by the companion verifier.

Equations (22)--(23) show that the Jacobian is \(1\) on \(D_0\) and
that the residual multiplier in (23) is \(-1/4\) there.  Hence both
remain units on a Zariski neighborhood of \(D_0\).  The two
restrictions (21) show that the generic fiber of (24) has the two
points \(x=t\) and \(x=-t\).  At \(x=\pm1\) the two source
components meet transversely and their target branches are exchanged.
The map is finite: in \(\mathcal O(D_0)\), the element \(x\) satisfies
\(x^2-P_0=0\), while
\[
 y^2+4(P_0-1)y=0.
\]
Thus its generators \(x,y\) are integral over \(\mathcal O(C)\), so
\(\mathcal O(D_0)\) is finite over \(\mathcal O(C)\).  The ambient
étaleness and (23) show pointwise that (24) is étale.  This gives the
asserted finite étale double cover.  \(\square\)

For reference, the Jacobian defect in this example is
\[
 W=-\frac1{64}\left(
 54x^6-108x^4y-108x^4-27x^2y^2+72x^2y
 -18x^2-9y^2+36y-52\right).
\tag{25}
\]
It is nonzero.  The example is therefore **not** a Keller map and
does not threaten the plane Jacobian conjecture.  Its purpose is
sharper: it realizes the full nodal pullback geometry inside an
ambient map which is already étale along the entire pullback.

## 5. Consequence for the search

The factorization \(H(P,Q)=yR\), the two transverse crossings, the
normalization splitting, the explicit idempotent, and the cyclic
degree-two monodromy are all compatible with étaleness on a
neighborhood of the divisor.  Nonproper residual components provide
still more flexibility, not less.

Therefore an all-degree proof cannot follow from those data alone.
The next viable nodal step must control at least one of:

* the global equation \(J(P,Q)=1\), rather than its restriction to
  the nodal pullback;
* the points deleted in the finite completions of residual
  normalization components, equivalently the intersection with the
  nonproper value set;
* the global algebraic correspondence
  \(\mathbb A^2\times_{\Phi}\mathbb A^2\), beyond its restriction to
  the single boundary line.

This is a route closure, not a solution of the two-dimensional
Jacobian conjecture.
