# All-degree dicritical ledger

This note records an exact infinity lemma that survives beyond the bounded
\((72,108)\) calculation.  It is a partial obstruction, not a proof of the
Jacobian conjecture.

## 1. Local Keller identity on a horizontal boundary divisor

Let \(\pi:X\to\mathbf P^2\) resolve the boundary of a polynomial Keller map
\[
F=(P,Q),\qquad dP\wedge dQ=c\,dx\wedge dy,\quad c\ne0.
\]
Let \(E\subset X\setminus\mathbf A^2\) be a boundary divisor.  At its generic
point choose \(E=(t=0)\) and a coordinate \(q\) along \(E\), and write
\[
P=t^{-a}(p(q)+O(t)),\qquad
Q=t^{-b}(s(q)+O(t)),\qquad a,b>0.
\]
Put
\[
g=\gcd(a,b),\qquad a_0=\frac ag,\qquad b_0=\frac bg.
\]
Suppose
\[
\alpha=\frac{s^{a_0}}{p^{b_0}}\in\mathbf C(E)
\]
is nonconstant.  Direct differentiation gives
\[
dP\wedge dQ
=g\,t^{-a-b-1}p\,s\,d\log(\alpha)\wedge dt
+O(t^{-a-b})\,dt\wedge dq.
\]
Consequently
\[
\operatorname{ord}_E\pi^*(dx\wedge dy)=-a-b-1. \tag{1}
\]
If
\[
\pi^*(dx\wedge dy)
=t^{-a-b-1}\bigl(\gamma(q)+O(t)\bigr)\,dt\wedge dq,
\]
then the leading coefficient identity is
\[
d\log\alpha=-\frac c g\,\frac{\gamma(q)\,dq}{p(q)s(q)}. \tag{2}
\]

In discrepancy notation
\[
A(E)=1+\operatorname{ord}_E\pi^*(dx\wedge dy),
\]
equation (1) is the sharp equality
\[
A(E)=-a-b. \tag{3}
\]
This is the unnormalized divisorial version of the affine Jacobian formula
\(\nu(JF)+A(\nu)=d(F,\nu)A(F_\bullet\nu)\).

Coordinate-free, if \(N_E=O_E(E)\), then \(p,s,\gamma\,dq\) are meromorphic
sections of
\[
N_E^a,\qquad N_E^b,\qquad K_E\otimes N_E^{a+b},
\]
respectively.  Hence (2) is intrinsically a meromorphic differential on
\(E\).

## 2. Ramification read from the canonical coefficient

Away from the nodes of the boundary:

- if \(\gamma(q_0)\ne0\), a zero of \(p\) or \(s\) is simple, and the
  corresponding ramification index of \(\alpha\) is \(b_0\) or \(a_0\);
- if \(p(q_0)s(q_0)\ne0\) and
  \(\operatorname{ord}_{q_0}\gamma=g\), then \(\alpha\) has ramification
  index \(g+1\);
- if, for example, \(p(q_0)=0\), \(s(q_0)\ne0\), and
  \(\operatorname{ord}_{q_0}\gamma=g\), then
  \(\operatorname{ord}_{q_0}p=g+1\).

Common zeros of \(p,s\), and poles of \(\gamma\), occur at boundary nodes and
must be computed from the adjacent divisorial labels.  This is exactly where
bare Riemann--Hurwitz stops being an obstruction: the line-bundle degree of
(2) is automatically \(-2\).

For the bounded radial face, (2) becomes the polynomial identity behind the
degree-21 passport
\[
(2^{10},1),\qquad(3^7),\qquad(17,1^4).
\]
In arbitrary degree, the node orders of \(\gamma\), rather than the abstract
Riemann--Hurwitz total, are the additional data to control.

## 3. Exact exclusion of toric horizontal divisors

Assume \(E\) is monomial in affine coordinates:
\[
\operatorname{ord}_E x=-r,\qquad
\operatorname{ord}_E y=-s,\qquad r,s>0.
\]
Then
\[
A(E)=-(r+s).
\]
The pole orders of \(P,Q\) are their weighted degrees
\[
a=\deg_{(r,s)}P,\qquad b=\deg_{(r,s)}Q.
\]
If \(E\) is horizontal for \(Q^a/P^b\), (3) gives
\[
a+b=r+s. \tag{4}
\]

Translate source and target so that \(F(0)=0\).  The linear parts of \(P,Q\)
form an invertible matrix.  Suppose \(r\ge s\).  At least one component has
an \(x\)-term and therefore weighted degree at least \(r\); linear
independence forces the other component to have weighted degree at least
\(s\).  Equality (4) makes both bounds equalities.

If \(r>s\), the component of weighted degree \(s\) has no \(x\)-term and no
nonlinear monomial, so it is a nonzero scalar multiple of \(y\).  The
constant-Jacobian identity then makes the other component affine-linear in
\(x\), and \(F\) is triangular.  If \(r=s\), both components are affine
linear.  Therefore:

> A noninvertible Keller map cannot have a ratio-horizontal boundary
> divisor whose valuation is monomial with two positive affine pole
> weights.

Thus a hypothetical counterexample must use a genuinely non-monomial
divisorial valuation, with a nontrivial key-polynomial sequence at infinity.

## 4. Boundary-label recursion and remaining bottleneck

For every boundary component \(D\), attach
\[
\bigl(A_D,a_D,b_D\bigr)
=\left(
1+\operatorname{ord}_D(dx\wedge dy),
-\operatorname{ord}_D P,
-\operatorname{ord}_D Q
\right).
\]
The original line at infinity starts with \(A=-2\).  Under a boundary
blowup:

- at a corner \(D_1\cap D_2\),
  \(A_{\rm new}=A_{D_1}+A_{D_2}\);
- at a smooth point of \(D\),
  \(A_{\rm new}=A_D+1\);
- at a smooth point where the leading coefficient of \(P\) has order \(m\),
  \(a_{\rm new}=a_D-m\), and similarly for \(Q\);
- at a generic corner, pole orders add.

A ratio-horizontal component is characterized by
\[
A_D+a_D+b_D=0.
\]

There is a precise node formula.  Let \(C_P,C_Q\) be the strict transforms of
generic translates \(P=c_P,Q=c_Q\), chosen to avoid every boundary node.
For a ratio-horizontal \(E\), restriction of the three relevant divisors
gives
\[
\begin{aligned}
\operatorname{div}_E(p)
  &=C_P|_E-\sum_{D\sim E}a_D[q_D],\\
\operatorname{div}_E(s)
  &=C_Q|_E-\sum_{D\sim E}b_D[q_D],\\
\operatorname{div}_E(\gamma\,dq)
  &=\sum_{D\sim E}(A_D-1)[q_D].
\end{aligned}
\]
Consequently (2) has the intrinsic divisor
\[
\boxed{\;
\operatorname{div}_E(d\log\alpha)
=-C_P|_E-C_Q|_E
+ \sum_{D\sim E}(A_D+a_D+b_D-1)[q_D].
\;} \tag{5}
\]
Its degree is \(-2\), as it must be.

Set
\[
\Delta_D=A_D+a_D+b_D.
\]
At a node \(q_D=E\cap D\), the order of \(\alpha\) is
\[
n_{ED}=b_0a_D-a_0b_D. \tag{6}
\]
Equation (5) yields the following adjacency dichotomy:

- if \(n_{ED}\ne0\), then \(d\log\alpha\) has a simple pole, hence
  \(\Delta_D=0\);
- if \(n_{ED}=0\), then \(\alpha(q_D)\in\mathbf C^*\) and
  \(\Delta_D\ge1\); if \(\alpha\) is nonconstant at the node, its
  ramification index there is exactly \(\Delta_D\).

Thus a change of pole slope across an edge adjacent to a horizontal
component forces the neighboring component onto the same sharp canonical
equality \(\Delta_D=0\).  A same-slope edge instead records its ramification
index directly in the neighboring \(\Delta\)-label.  This recovers the large
ramification index on the third branch of the bounded Belyi passport.

Distinct-slope adjacent \(\Delta=0\) components cannot simply be prohibited.
The identity map already supplies the smallest test.  Near the line at
infinity write
\[
x=t^{-1},\qquad y=q\,t^{-1}.
\]
The line has \((A,a,b)=(-2,1,1)\).  Blow up \(q=t u\) at the point \(q=0\).
The new exceptional component has
\[
(A,a,b)=(-1,1,0),\qquad \Delta=0,
\]
and the slope determinant across the new edge is nonzero.  It is the target
corner blowup of an automorphism, not a forbidden configuration.

Therefore the all-degree problem is to classify the complete connected
\(\Delta=0\) subtree emanating from \(E\), including endpoints where one pole
order becomes zero, and to couple its determinant labels to the positive
\(\Delta\)-labels on same-slope branches.  Negative definiteness must be
applied to this whole decorated subtree, not to a single edge.  A degree
count alone cannot finish the argument, because the total degree in (5) is
identically \(\deg K_E=-2\).

## 5. Global intersection-matrix constraint

Let \(B_1,\ldots,B_n\) be all boundary components and
\[
M=(B_i\cdot B_j).
\]
They form a basis of \(\operatorname{Pic}(X)\), and
\[
\det M=(-1)^{n-1}.
\]
For a morphism resolving \(F\), put
\[
H=F^*L_\infty=\sum_i r_iB_i,\qquad
h_i=H\cdot B_i.
\]
Here \(r_i\ge0\), while \(h_i\ge0\) is nonzero exactly when \(B_i\) maps
onto a target curve that meets \(L_\infty\).  The projection formula gives
\[
Mr=h,\qquad r=M^{-1}h. \tag{7}
\]

The diagonal entry of \(M^{-1}\) is precisely the determinant label
\[
(M^{-1})_{ii}
=\det\bigl(-M_{\widehat i,\widehat i}\bigr)=d_i. \tag{8}
\]
Thus if \(B_i\) were the only horizontal boundary component, (7) would give
\[
r_i=d_i h_i.
\]
In particular \(d_i>0\).  The standard ample-ramification sign constraint
for a noninvertible Keller map says that a component mapped onto the target
line at infinity has \(d_i<0\).  Hence a counterexample cannot have only one
horizontal boundary component: off-diagonal cofactors in \(M^{-1}\) and at
least one additional horizontal component are essential.

Equations (5)--(8) isolate the remaining combinatorial target.  One needs an
inequality for a tree with at least two horizontal vertices, negative
determinant labels at the infinity vertices, and the decorated
\(\Delta=0\) paths forced by (6).  The one-horizontal argument is exact but
does not extend by discarding the off-diagonal cofactors.

The exploratory verifier
`scratch_dicritical_tree_labels.py` exhausts all rooted decorated boundary
trees obtainable by at most eight blowups (at most nine vertices).  For
each nonempty proposed horizontal set it solves the exact system
\[
(M^{-1})_{H,H}h_H
=\left(-\frac{A_i}{2}\right)_{A_i<0}
\oplus(0)_{A_i>0}. \tag{9}
\]
The right side imposes \(A_i=-2r_i\) on components mapped to
\(L_\infty\), and \(r_i=0\) on components mapped to affine curves.  It then
checks \(h_H\in\mathbf Z_{>0}^H\) and \(M^{-1}h\ge0\).  No tree through nine
vertices passes.  All singular principal systems in this range are
inconsistent, so none are silently omitted.

This is only a small-tree lower bound, not an all-degree argument.  It does
show that the first superficially feasible two-horizontal tree (seven
vertices if the canonical relation is ignored) is spurious: its proposed
horizontal vertices have \(A=-1\) and pullback multiplicity \(2\), violating
\(A=-2r\).

## 6. Schur complement: exact formulation and limitation

Let \(H\) now denote the set of all horizontal vertices and \(V\) its
complement.  Since the divisor \(F^*L_\infty\) is nef and big and every
vertical component is orthogonal to it, the Hodge index theorem makes
\(M_{V,V}\) negative definite.  Eliminate the vertical coefficients:
\[
S=M_{H,H}-M_{H,V}M_{V,V}^{-1}M_{V,H}
  =\bigl((M^{-1})_{H,H}\bigr)^{-1}. \tag{10}
\]
The matrix \(S\) has signature \((1,|H|-1)\).  Because \(-M_{V,V}\) is a
positive-definite tree \(M\)-matrix, its inverse is entrywise nonnegative;
therefore the off-diagonal entries of \(S\) are nonnegative.

Partition
\[
H=H_\infty\sqcup H_{\rm fin}
\]
according to whether a component maps onto \(L_\infty\) or onto a curve in
\(\mathbf A^2\).  The exact horizontal equations are
\[
\rho_i=
\begin{cases}
-A_i/2,&i\in H_\infty,\\
0,&i\in H_{\rm fin},
\end{cases}
\qquad
h_H=S\rho,\qquad h_H\in\mathbf Z_{>0}^{H},             \tag{11}
\]
and
\[
r_V=-M_{V,V}^{-1}M_{V,H}\rho\in\mathbf Z_{\ge0}^{V}.   \tag{12}
\]
Equivalently,
\[
(M^{-1})_{H,H}h_H=\rho.
\]
The augmented-canonical labels are not free: if
\(\operatorname{val}(B_i)\) is the boundary valency, then
\[
MA=(\operatorname{val}(B_i)-2)_i.                     \tag{13}
\]
The determinant-label assumption is
\[
(M^{-1})_{ii}<0\qquad(i\in H).                        \tag{14}
\]

There is no contradiction from signature, off-diagonal signs, and (14)
alone.  The abstract Lorentzian pair
\[
C=\begin{pmatrix}-1&2\\2&-1\end{pmatrix},
\qquad
S=C^{-1}=\frac13\begin{pmatrix}1&2\\2&1\end{pmatrix}
\]
has negative diagonal entries in \(C\) and satisfies
\[
S(1,1)^t=(1,1)^t.
\]
Thus the desired symbolic obstruction has to use the tree-realizability
condition (13), and probably the \(\Delta=0\) slope decorations, not merely a
Schur-complement inequality.

The assumptions entering (11)--(14) should remain explicit:

1. the source rational map has been resolved to a morphism by boundary
   blowups, so all boundary components form the unimodular tree used above;
2. a component over \(L_\infty\) has \(A_i=-2r_i<0\), by the log-Jacobian
   formula;
3. a component mapping to an affine curve has \(r_i=0\) and
   \(A_i>0\), equal to its transverse ramification index;
4. every horizontal vertex has negative determinant label.  This is the
   ample-ramification sign theorem for a noninvertible Keller map; it is an
   imported geometric input, not proved by the tree enumerator.

There is one more useful label that packages the log ramification:
\[
\Lambda_i=A_i+2r_i.
\]
For the resolved morphism of log pairs
\[
(X,B_X)\longrightarrow(\mathbf P^2,L_\infty),
\]
the log-canonical formula is
\[
K_X+B_X
=F^*(K_{\mathbf P^2}+L_\infty)+R_{\log}
=-2H+R_{\log},
\]
so
\[
R_{\log}=\sum_i\Lambda_iB_i,\qquad \Lambda_i\ge0.       \tag{15}
\]
Thus \(\Lambda_i=0\) on an infinity-horizontal component and
\(\Lambda_i=A_i>0\) on a finite horizontal component.  The tree verifier
also checks (15).

The identity \(M\Lambda=(\operatorname{val}-2)+2h\) has a sharp local
meaning.  If \(E=B_i\) maps onto \(L_\infty\), then
\[
\sum_{D\sim E}\Lambda_D
=\operatorname{val}(E)-2+2h_E,
\]
or equivalently
\[
\sum_{D\sim E}(\Lambda_D-1)=2h_E-2.                   \tag{16}
\]
Here \(h_E\) is the degree of \(E\to L_\infty\).  When
\(-\operatorname{ord}_E P=-\operatorname{ord}_E Q\), the node formula
(5)--(6) identifies \(\Lambda_D\) with the local ramification index of that
map: on a slope-change edge,
\(\Lambda_D=|a_D-b_D|\), while on a same-slope edge
\(\Lambda_D=\Delta_D\).  Hence (16) is exactly Riemann--Hurwitz on the
horizontal rational curve.  This is a valuable consistency theorem, but it
also explains why adjunction by itself gives no new inequality: it
repackages the full ramification equality.
