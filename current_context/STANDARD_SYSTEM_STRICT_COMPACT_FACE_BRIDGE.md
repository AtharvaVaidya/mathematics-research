# The strict compact-face bridge for an actual Keller pair

Date: 26 July 2026

## Outcome

For an actual reciprocal polynomial Keller pair, the
``isolated matched \(Q\)-face'' hypothesis in the compact-face theorem
is automatic at a strict first local \(P\)-slope.

The proof does not rely on projecting the individual standard terms
\(\lambda_k\tau^kC^{m-k}\).  Such projection can mix finite-root
Taylor weights.  Instead, the local Keller bracket itself excludes
every \(Q\)-face below \(s^b\), and the weight lattice makes the face
at \(s^b\) uniquely of the form \(s^bB(z)\).

Consequently every strict compact first face is a reduced common-root
shift.  At the earliest global order these local shifts glue for both
members of the pair to
\[
R\longmapsto R+\tau^E\dot R(X),
\]
with the expected reciprocal degree bound on \(\dot R\).  Equality of
the face slope with \(g\) remains the physical \(g\)-sector resonance.
Iterating gives the common-power normal form
\[
P\equiv S^a,\qquad Q\equiv S^b\pmod{\tau^g}.
\]

This bridge uses the full polynomial Keller identity.  The finite GGV
standard equations without that identity do not by themselves justify
the local face conclusion.

## 1. Setup and the general \(Q\)-coset bracket

Let
\[
n=ga,\qquad m=gb,\qquad \gcd(a,b)=1,
\]
and work at a simple root of the squarefree common root \(R\), using
\(s=R(X)\) as local coordinate.  Suppose the entire first compact
\(P\)-face is
\[
P_0=s^aA(z),\qquad
z=\frac{\tau^{d'}}{s^{h'}},
\qquad A(0)=1,
\tag{1}
\]
where
\[
\gcd(d',h')=1,\qquad
\frac{d'}{h'}<g.
\tag{2}
\]

The exact homogenized Keller identity is
\[
\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X=-c\tau^N.
\]
Since \(\partial_X=R'(X)\partial_s\), its left side is
\(R'(X(s))\) times the local \(s\)-derivative bracket below.  Thus the
local right side is
\[
-\frac{c}{R'(X(s))}\tau^N.
\]
Squarefreeness gives \(R'(\alpha)\ne0\), so
\(1/R'(X(s))\) has a nonzero constant term and all its other terms
have positive \(s\)-weight.  Consequently only the initial weight
\(h'N\), and not the constancy in \(s\), is used below.

Give \(s,\tau\) weights \(d',h'\).  A polynomial \(Q\)-face in one
lattice coset has the form
\[
Q_{u,v}=\tau^u s^vB(z),\qquad B(0)\ne0,
\tag{3}
\]
with face weight
\[
w=h'u+d'v.
\tag{4}
\]
Put
\[
\Delta=d'-gh'<0,\qquad
L=u+gv-m.
\tag{5}
\]
Direct differentiation in the homogenized Keller bracket gives
\[
\boxed{
\begin{aligned}
\mathscr K(P_0,Q_{u,v})
=\tau^u s^{a+v-1}\bigl(
&aL\,AB
+a\Delta z\,AB'\\
&+(mh'-w)z\,A'B
\bigr).
\end{aligned}
}
\tag{6}
\]

The constant term in \(z\) is
\[
aL\,A(0)B(0).
\tag{7}
\]
This elementary Euler defect is what excludes a lower \(Q\)-face.

## 2. No polynomial \(Q\)-face lies below \(s^b\)

Assume for contradiction that the actual polynomial \(Q\) has a
lowest face of weight
\[
w<bd'.
\tag{8}
\]
Its contribution to the Keller bracket has weight
\[
(a-1)d'+w<(a+b-1)d'.
\tag{9}
\]
The scalar right side has weight \(h'N\), and
\[
\begin{aligned}
h'N-(a+b-1)d'
&=(a+b-1)(gh'-d')+h'(g-2)\\
&>0.
\end{aligned}
\tag{10}
\]
Thus the face in (9) must vanish by itself.  Equation (7) forces
\[
L=0,\qquad u+gv=gb.
\tag{11}
\]
Since \(u,v\ge0\), one has \(v\le b\), and then
\[
\begin{aligned}
w
&=h'g(b-v)+d'v\\
&=bd'+(b-v)(gh'-d')\\
&\ge bd',
\end{aligned}
\tag{12}
\]
contrary to (8).

Therefore the actual \(Q\) has no face below weight \(bd'\).  At
\(\tau=0\), its common-root term is \(s^b\).  Every integer lattice
point on the weight-\(bd'\) line is
\[
(u,v)=(d'j,b-h'j).
\]
Hence the entire face is automatically
\[
\boxed{
Q_0=s^bB(z),\qquad B(0)=1.
}
\tag{13}
\]
There is no second residue coset at the same weight because
\(\gcd(d',h')=1\).

No separate ``equal-weight multi-face'' hypothesis is needed here.
By definition \(A(z)\) contains every \(P\)-monomial on the first
weight line.  Likewise, (13) contains every \(Q\)-monomial on its
lowest weight line.  If \(P_+\) has weight greater than \(ad'\) and
\(Q_+\) has weight greater than \(bd'\), then every bracket involving
\(P_+\) or \(Q_+\) has weight strictly greater than
\[
(a+b-1)d',
\]
because the local bracket of terms of weights \(p,q\) has weight
\(p+q-d'\).  Hence adjacent Newton edges cannot contaminate the
initial bracket.  Collinear monomials are not a second face; they are
already coefficients of \(A\) or \(B\).

The compact-face theorem now applies without an extra matched-face
assumption.  In the strict case (2), it gives
\[
P_0=(s+\kappa\tau^{d'})^a,\qquad
Q_0=(s+\kappa\tau^{d'})^b.
\tag{14}
\]
Indeed, if \((d,\sigma)\) is the far endpoint of the original
\(P\)-face, the compact-face theorem forces
\[
\sigma=0,\qquad \gcd(a,d)=a,\qquad
h'=1,\qquad d'=\frac da<g.
\tag{15}
\]
Thus \(d\) is the far endpoint order, while \(d'\) is the primitive
shift order.  In particular (14) already contains the nonzero term
\[
a\kappa\tau^{d'}s^{a-1}.
\tag{16}
\]
This distinction is essential in the global argument.
At slope equality \(d'/h'=g\), the face bracket is resonant instead
and imposes no relative-power relation.

## 3. What the standard terms and Laurent tail do

On the face (1),
\[
C=P^{1/n}
=s^{1/g}A(z)^{1/n}
\]
in the local Puiseux field.  Therefore
\[
\lambda_k\tau^kC^{m-k}
\]
has face weight
\[
\boxed{
bd'+k\left(h'-\frac{d'}g\right).
}
\tag{17}
\]
For \(k>0\), this is strictly larger than \(bd'\).  When
\(k\not\equiv0\pmod g\), the factor
\(s^{-k/g}\) lies in a nontrivial Kummer character; all powers of
\(z\) retain the same weight and character.  Terms in distinct
characters do not cancel in the Puiseux associated graded ring.

This calculation is consistent with (13), but it is not by itself a
proof about the polynomial \(Q\).  Passing from a Laurent series at
\(X=\infty\) to its polynomial part can change finite-root Taylor
orders.  For example, with
\[
g=2,\qquad R=X^2+1,
\]
one has
\[
\left[R^{5/2}\right]_+
=X^5+\frac52X^3+\frac{15}{8}X,
\tag{18}
\]
and at \(X=i\), a root of \(R\), its value is
\[
\frac38i\ne0.
\tag{19}
\]
The raw Puiseux term has positive fractional \(R\)-order, while its
polynomial projection has local order zero.

The formal tail \(F\) is not an independent polynomial coordinate near
the root: it is defined at \(X=\infty\) so that
\[
Q=\sum_k\lambda_k\tau^kC^{m-k}+F
\]
is the actual polynomial.  Individual \(F\)-monomials therefore do
not define an additional finite-root Newton face.  Polynomial
projection may mix weights as in (18)--(19), but the resulting actual
polynomial \(Q\) is exactly what Sections 1--2 constrain.

The final tail coefficient produces the scalar right side at weight
\(h'N\), which is strictly above the compact face by (10).  It cannot
contaminate the initial bracket.

Thus:

* the raw \(k>0\) standard sectors are strictly above the face;
* rational residue classes remain separated before projection;
* projection and \(F\) make the raw weight argument insufficient; but
* the polynomial Keller identity makes the matched face automatic.

## 4. Global gluing of the reduced shifts

Let
\[
P=R^a+\sum_{j>0}\tau^jT_j(X)
\tag{20}
\]
and
\[
Q=R^b+\sum_{j>0}\tau^jU_j(X)
\]
be reciprocal, with
\[
\deg T_j\le n-j,\qquad \deg U_j\le m-j,
\]
at the current stage of the reduction.  All already exposed
lower-order reduced shifts have been removed.  Define
\[
E=\min\{j>0:T_j\ne0\}.
\tag{21}
\]
Thus \(E\) is the earliest global coefficient order, not the far
endpoint \(d=aE\) of a completed reduced face.

Suppose some strict compact face survives.  By (14)--(16), that face
contains a nonzero coefficient at its primitive shift order \(d'<g\).
Hence global minimality gives
\[
E\le d'<g.
\tag{22}
\]

We claim that at every root \(\alpha\) of \(R\),
\[
\operatorname{ord}_\alpha T_E\ge a-1.
\tag{23}
\]
At an inactive root the order is at least \(a\); at an active root it
is exactly \(a-1\).

To prove the claim, take a root for which
\(\operatorname{ord}_\alpha T_E<a\), and write
\[
\sigma=\operatorname{ord}_\alpha T_E<a,\qquad h=a-\sigma\ge1.
\]
The point supplied by \(T_E\) has local slope \(E/h\le E<g\).
Consequently the actual first local Newton face has an even smaller
strict slope.  The automatic compact-face theorem makes that first
face a reduced shift with primitive exponent, say, \(E_\alpha\).
Its expansion contains a nonzero coefficient at order \(E_\alpha\),
so the definition (21) gives
\[
E_\alpha\ge E.
\]
On the other hand the first-face slope is \(E_\alpha\), because the
theorem forces \(h'=1\), and therefore
\[
E_\alpha\le\frac Eh\le E.
\]
All inequalities are equalities.  Hence \(E_\alpha=E\), \(h=1\), and
\(\sigma=a-1\), proving (23).  At a root where
\(\operatorname{ord}_\alpha T_E\ge a\), (23) is immediate.

This also makes the induction explicit.  Remove the global reduced
shift at order \(E\), recompute the least nonzero coefficient order,
and repeat the same argument.  A physical resonance cannot interrupt
a strict layer: its first order is \(g(a-\sigma)\ge g\), whereas
(22) gives \(E<g\).

Since \(R\) is squarefree, (23) gives the global divisibility
\[
T_E=aR^{a-1}\dot R
\tag{24}
\]
for a polynomial \(\dot R\).  The reciprocal degree bound gives
\[
\deg\dot R
\le(n-E)-g(a-1)
=g-E.
\tag{25}
\]
This is already at most \(g-1\).  If \(E\ge2\), it is already at most
\(g-2\).  In the sole remaining case \(E=1\), the usual missing
\(X^{n-1}\)-coefficient normalization removes the possible
\(X^{g-1}\)-term of \(\dot R\).  Thus in every case
\[
\deg\dot R\le g-2.
\tag{26}
\]
Thus all local constants \(\kappa_\alpha\), including zeros at
inactive roots, are evaluations of one global polynomial
\(\dot R\).

The same argument identifies the \(Q\)-coefficient, not merely its
leading value at the active roots.  Give \(s,\tau\) weights \(E,1\).
At an active root, (14) says that the order-\(E\) \(Q\)-coefficient
starts with
\[
b\kappa_\alpha s^{b-1}.
\]
At an inactive root the \(P\)-initial form for these weights is just
\(s^a\).  Indeed, a later \(P\)-monomial of weight at most \(aE\)
would produce a first local slope at most \(E<g\).  Its reduced face
would contain a coefficient at primitive order \(E_\alpha\le E\);
global minimality would force \(E_\alpha=E\), contradicting
inactivity.  Formula (6), now with \(A=1\), first excludes a
\(Q\)-face below \(s^b\); at weight \(bE\), its strict-face equation is
\[
(E-g)a zB'(z)=0,
\]
so \(B=1\).  Therefore no order-\(E\) root motion occurs in \(Q\) at
an inactive root.

The same below-face argument also shows that \(U_j=0\) for \(j<E\).
Indeed, a local monomial \(\tau^j s^v\) with \(v<b\) would have
\[
j+Ev\le j+E(b-1)<bE.
\]
Thus \(\operatorname{ord}_\alpha U_j\ge b\) at every root.  It follows
that \(R^b\mid U_j\), while
\(\deg U_j\le m-j<m=\deg R^b\), forcing \(U_j=0\).

Finally put
\[
D_E=U_E-bR^{b-1}\dot R.
\]
At each active root the two displayed reduced faces show
\(\operatorname{ord}_\alpha D_E\ge b\).  At each inactive root,
\(\dot R(\alpha)=0\) and the preceding vertex calculation gives the
same inequality.  Hence \(R^b\mid D_E\).  But
\[
\deg D_E\le m-E<m,
\]
so \(D_E=0\), and therefore
\[
\boxed{U_E=bR^{b-1}\dot R.}
\tag{27}
\]

Replacing
\[
R\longmapsto R+\tau^E\dot R
\tag{28}
\]
is an honest reduced common-root reparametrization and removes the
earliest strict face from both \(P\) and \(Q\).  It preserves the
reciprocal degree bounds by (25): its order-\(\ell E\) binomial
contributions have degrees at most
\[
(a-\ell)g+\ell(g-E)=n-\ell E
\]
for \(P\), and
\[
(b-\ell)g+\ell(g-E)=m-\ell E
\]
for \(Q\).

There is no hidden error from using a \(\tau\)-dependent approximate
root in the next induction step.  If \(s=S(\tau,X)\), then
\[
\begin{aligned}
P_X&=S_XP_s,&
P_\tau|_X&=P_\tau|_s+S_\tau P_s,\\
Q_X&=S_XQ_s,&
Q_\tau|_X&=Q_\tau|_s+S_\tau Q_s.
\end{aligned}
\]
The two \(S_\tau P_sQ_s\) terms cancel in the determinant, so the full
homogenized bracket is exactly \(S_X\) times the same local bracket in
\((s,\tau)\).  Since \(S_X\) remains a local unit, Sections 1--2
apply unchanged after every common shift.

This gluing argument can therefore be iterated through all strict
first faces.  It stops only when the first root-moving face has
slope \(g\) or greater; slope \(g\) is the physical resonance not
classified by the strict theorem.

## 5. Subresonant common-power normal form

The preceding induction has a concise global consequence.  There is a
reciprocal polynomial series
\[
S(\tau,X)
=R(X)+\sum_{1\le j<g}\tau^jS_j(X),
\qquad
\deg S_j\le g-j,
\tag{29}
\]
such that
\[
\boxed{
P\equiv S^a\pmod{\tau^g},
\qquad
Q\equiv S^b\pmod{\tau^g}.
}
\tag{30}
\]
For \(j=1\), the missing \(X^{n-1}\) normalization sharpens the bound
to \(\deg S_1\le g-2\).

To see that no \(Q\)-coefficient is left behind after the last
\(P\)-shift, suppose \(j<g\) is its least remaining order.  At any
root, a later \(P\)-term of weight at most \(aj\) for weights
\(\operatorname{wt}(s)=j,\operatorname{wt}(\tau)=1\) would expose a
strict reduced face with primitive order at most \(j\), contrary to
the completed \(P\)-induction.  Thus the \(P\)-initial form is
\(s^a\).  Sections 1--2, with \(A=1\), exclude every \(Q\)-term below
weight \(bj\), while the weight-\(bj\) equation
\[
(j-g)a zB'(z)=0
\]
excludes a nonconstant matched face.  Hence the order-\(j\)
coefficient vanishes to order at least \(b\) at all roots of \(R\).
Its degree is less than \(gb\), so it is zero.  This proves (30).

Accordingly no nontrivial relative deformation can occur before
order \(g\).  The first possible physical data lie precisely in the
\(g\)-sector, where the strict prefactor vanishes and the relative
unit \(Q^a/P^b\) must be retained.

## 6. Scope

The bridge proves automatic matching for:

* an actual polynomial Keller pair;
* a squarefree common root;
* the entire first compact local \(P\)-face;
* every monomial on that Newton weight line; and
* a strict slope \(d'/h'<g\).

It does not prove the same statement from the finite standard
equations plus determinant contact alone.  Nor does it classify
repeated roots or the slope-\(g\) relative resonant sector.  Adjacent
Newton faces and coincident strict valuations are not additional
exceptions: the former have higher initial weight, while the latter
glue simultaneously by Section 4.
