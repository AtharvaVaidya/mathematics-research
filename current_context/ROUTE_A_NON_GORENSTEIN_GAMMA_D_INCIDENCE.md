# Route A: non-Gorenstein fibers versus the distinguished collision curve

Date: 25 July 2026

## Outcome

Let
\[
\pi:Y\longrightarrow\mathbf A^2
\]
be the finite flat rank-three normalization of a hypothetical cubic
Darboux map
\[
F:S\longrightarrow\mathbf A^2
\]
from the quadratic pseudoplane, and let
\[
D\simeq\mathbf A^1,\qquad
\nu_D=F|_D:D\longrightarrow\Gamma_D=\overline{F(D)}.
\]
The earlier collision audit proves that \(\nu_D\) is the normalization
of \(\Gamma_D\).

The exact incidence conclusions are:

> **Distinguished-curve avoidance theorem.**
> Let \(Z_{\rm ng}\subset\mathbf A^2\) be the base locus where the
> Miranda triple-cover fiber is the non-Gorenstein algebra
> \[
> \mathbf C[z,w]/(z,w)^2.
> \]
> Then
> \[
> \boxed{\Gamma_D\cap Z_{\rm ng}=\varnothing.}
> \tag{1}
> \]
> More generally, if
> \[
> b_q=\#\nu_D^{-1}(q)
> \]
> for \(q\in\Gamma_D\), then
> \[
> b_q\le3.
> \tag{2}
> \]
> If \(b_q\ge2\), the cubic cover is completely étale over \(q\);
> in particular
> \[
> q\notin\Delta.
> \tag{3}
> \]

Thus every nodal or triple self-identification of the polynomially
parametrized curve \(\Gamma_D\) is disjoint from both the branch curve
and the non-Gorenstein base locus.

This is a genuine new incidence restriction, but not yet a
contradiction.  An exact connected cubic countermodel realizes a nodal
\(\Gamma_D\) with two retained normalization points and a completely
étale three-point fiber.  Boundary localization classes do not see
that fiber because it contains no boundary point.

## 1. Why \(D\to\Gamma_D\) is finite and surjective

The map is given by two polynomials in the coordinate \(v\) of
\(D=\mathbf A^1\).  The induced inclusion is
\[
\mathbf C[\Gamma_D]\hookrightarrow\mathbf C[v].
\tag{4}
\]
It is birational by the mandatory collision theorem.  Choose a
nonconstant element \(h(v)\in\mathbf C[\Gamma_D]\).  The polynomial
ring \(\mathbf C[v]\) is finite over \(\mathbf C[h(v)]\).  Since
\[
\mathbf C[h(v)]\subset
\mathbf C[\Gamma_D]\subset
\mathbf C[v],
\]
the same finite generating set makes \(\mathbf C[v]\) finite over
\(\mathbf C[\Gamma_D]\).  Therefore (4) is finite.

Since \(D\) is normal and the map is finite birational, it is the
normalization.  A finite dominant morphism is closed and surjective, so
\[
\boxed{F(D)=\Gamma_D\quad\text{set-theoretically}.}
\tag{5}
\]
In particular,
\[
\Gamma_D\subset F(S).
\tag{6}
\]

This surjectivity is stronger than mere density of the image and is the
key point in (1).

## 2. Non-Gorenstein values are missing values of \(F\)

At a non-Gorenstein Miranda point \(q\), the flat length-three fiber is
\[
\pi^{-1}(q)=
\operatorname{Spec}\mathbf C[z,w]/(z,w)^2.
\tag{7}
\]
It has one underlying point \(p\), and \(p\) is singular.  Since the
open surface \(S\) is smooth and \(F=\pi|_S\) is étale,
\[
p\notin S.
\]
There is no other point in the fiber, so
\[
q\notin F(S).
\tag{8}
\]
Combining (6) and (8) proves (1).

Equivalently:

> Every non-Gorenstein cubic value is a hole in the image of the étale
> map \(F:S\to\mathbf A^2\), whereas the entire distinguished curve
> \(\Gamma_D\) is filled by retained points of \(D\).

No class-group input is needed for this avoidance.

## 3. Fiber-length bound at a self-identification

Let \(q\in\Gamma_D\), and write
\[
\nu_D^{-1}(q)=\{d_1,\ldots,d_{b_q}\}.
\]
The points \(d_i\) are distinct points of \(S\) in the cubic fiber.
Since \(F\) is étale at every \(d_i\), the local fiber algebra at
\(d_i\) is the reduced length-one algebra \(\mathbf C\).  The full
fiber has length three by flatness.  Hence
\[
b_q\le3,
\]
proving (2).

Suppose \(b_q\ge2\).  If \(q\) were a branch value, the fiber would
have a non-étale local Artin factor.  Over \(\mathbf C\), such a factor
has length at least two and is supported away from the étale points
\(d_i\).  Therefore
\[
\operatorname{length}\pi^{-1}(q)
\ge b_q+2\ge4,
\]
contrary to rank three.  This proves (3).

The two possible singular cases are therefore:

\[
\begin{array}{c|c}
b_q&\pi^{-1}(q)\\ \hline
2&d_1+d_2+e,\quad\text{three distinct étale points},\\
3&d_1+d_2+d_3,\quad\text{three distinct étale points}.
\end{array}
\tag{9}
\]

If \(\Gamma_D\) has an ordinary \(r\)-fold point, then
\(b_q=r\).  Thus it can have nodes or ordinary triple points, but no
ordinary point with four or more branches.

## 4. Local pullback incidence at a singular point

Let
\[
Z=F^{-1}(\Gamma_D)\subset S.
\]
At a point \(d_i\) over \(q\), étaleness identifies the completed
surface germ with the completed target-plane germ:
\[
\widehat{\mathcal O}_{S,d_i}
\simeq
\widehat{\mathcal O}_{\mathbf A^2,q}.
\tag{10}
\]
Consequently the completed curve germ \(Z_{d_i}\) is an exact copy of
the full plane-curve germ \((\Gamma_D,q)\).

If \(q\) has \(b_q\) branches, then \(Z\) has \(b_q\) local branches at
each \(d_i\).  Exactly one is the local branch of \(D\); the remaining
\(b_q-1\) branches are supplied by the other collision components.
This explains how a single global normalization curve \(D\) can have
several points over \(q\) without exceeding cubic degree: collision
components pass through the same retained étale points.

The conductor on \(D=\mathbf A^1\) records these identifications but is
still principal.  The new information is the fiber-length bound (2),
not a new divisor class.

## 5. Exact nodal countermodel

Consider the standard connected cubic cover
\[
\pi_0:\mathbf A^2_{s,t}\longrightarrow\mathbf A^2_{x,y},
\qquad
x=s,\qquad y=t^3-3st.
\tag{11}
\]
It is finite flat of rank three, since \(t\) satisfies
\[
t^3-3xt-y=0.
\]
Its Jacobian and branch curve are
\[
J_{\pi_0}=3(t^2-s),\qquad
\Delta_0=V(4x^3-y^2).
\tag{12}
\]

Inside the source, take the smooth affine line
\[
D_0=V\!\left(s-t^2+\frac23\right).
\tag{13}
\]
Along \(D_0\),
\[
J_{\pi_0}=2,
\]
so \(D_0\) lies entirely in the étale locus.  Parameterizing by \(t\)
gives
\[
x=t^2-\frac23,\qquad
y=2t(1-t^2).
\tag{14}
\]
Elimination yields the irreducible rational curve
\[
\Gamma_0:
\quad
y^2=
4\left(x+\frac23\right)
\left(\frac13-x\right)^2.
\tag{15}
\]

The two parameters \(t=1\) and \(t=-1\) map to
\[
q=\left(\frac13,0\right).
\]
Their tangent directions are distinct, so \(q\) is an ordinary node
and \(D_0\to\Gamma_0\) is its normalization.

The cubic fiber over \(q\) is
\[
t^3-t=t(t-1)(t+1),
\]
with three distinct points
\[
t=-1,\quad0,\quad1.
\tag{16}
\]
Moreover
\[
4x(q)^3-y(q)^2=\frac4{27}\ne0,
\]
so the cover is completely étale over the node, exactly as (9)
requires.

## 6. Global splitting after normalization base change

There is a stronger global formulation of the distinguished sheet.
Base-change the cubic cover along the normalization parameter:
\[
Y_D=Y\times_{\mathbf A^2}D
   \longrightarrow D=\operatorname{Spec}\mathbf C[v].
\tag{23}
\]
The inclusion \(D\hookrightarrow Y\) supplies a section
\[
\sigma:D\longrightarrow Y_D.
\tag{18}
\]
Because the original map is étale along \(D\), this section lies in
the étale locus of (17).  A section of an unramified morphism is an
open immersion (Stacks Project, Tag 024T).  It is also closed because
(17) is finite, hence separated.  Thus \(\sigma(D)\) is open and
closed in \(Y_D\).

On coordinate rings, the pulled-back cubic algebra therefore splits
globally:
\[
\boxed{\mathcal A_D\simeq \mathbf C[v]\times\mathcal B_2,}
\tag{19}
\]
where \(\mathcal B_2\) is finite flat of rank two over
\(\mathbf C[v]\).  In particular, every fiber over a point of the
normalization contains the distinguished reduced length-one factor.
This gives a second, scheme-theoretic proof that no point of
\(\Gamma_D\) can be a non-Gorenstein value: the local algebra
\(\mathbf C[z,w]/(z,w)^2\) has no nontrivial idempotent and cannot
admit the decomposition (19).

Since \(2\) is invertible and every line bundle on \(\mathbf A^1\) is
trivial, the trace-zero summand of \(\mathcal B_2\) is free of rank
one.  After choosing its generator \(\tau\),
\[
\boxed{\mathcal B_2\simeq
 \mathbf C[v,\tau]/\bigl(\tau^2-g(v)\bigr)}
\tag{20}
\]
for a polynomial \(g(v)\).  Thus the full cubic cover along the
normalization of \(\Gamma_D\) has been reduced to a single explicit
quadratic cover.

## 7. Restricted discriminant identity

The trace pairing for the product (19) is block diagonal.  Its
rank-one factor has discriminant \(1\), while the rank-two factor
(20) has discriminant \(4g(v)\).  The product basis and the pullback
of any global cubic basis differ by an element of
\(\operatorname{GL}_3(\mathbf C[v])\), whose determinant is a
nonzero constant.  Consequently, if \(\operatorname{Disc}_\pi(x,y)\)
denotes a branch-discriminant polynomial for the cubic cover, then
\[
\boxed{
\operatorname{Disc}_\pi\bigl(\nu_D(v)\bigr)
=c\,g(v),\qquad c\in\mathbf C^\times .
}
\tag{21}
\]
In particular, the intersections of the normalized distinguished
curve with the branch curve are exactly the branch points of the
residual quadratic algebra, including multiplicities.

For the exact nodal countermodel, restriction of the branch
polynomial to (14) gives
\[
4x(t)^3-y(t)^2
=\frac4{27}\bigl(9t^2-8\bigr).
\tag{22}
\]
The two residual branch points \(t=\pm2\sqrt2/3\) are distinct from
the two normalization parameters \(t=\pm1\) lying over the node.
This cleanly separates the two phenomena:

* self-identification of \(\Gamma_D\) occurs in a completely split
  cubic fiber;
* ramification along \(\Gamma_D\) occurs only in the residual
  quadratic factor.

The splitting theorem is more informative than the raw fiber-length
argument, but by itself it still does not force a contradiction.
The remaining question is whether the special compactification of a
quadratic pseudoplane imposes a parity, divisor-class, or
monodromy-at-infinity condition on the polynomial \(g(v)\) that a
general cubic cover does not satisfy.

The full pullback of the nodal curve factors as
\[
\begin{aligned}
\pi_0^*(\Gamma_0)
=-\frac1{27}
&\left(3s-3t^2+2\right)\\
&\cdot
\left(
36s^2-45st^2-24s+9t^4+6t^2+4
\right).
\end{aligned}
\tag{17}
\]
The first factor is \(D_0\); the second is the residual degree-two
collision component.  It passes through all three points (16) and
supplies the additional local branch at both retained \(D_0\)-points.

Thus a nodal normalization self-identification and the required
collision geometry coexist exactly in a connected cubic cover.

This model is not the quadratic pseudoplane: the étale open
\[
\mathbf A^2_{s,t}\setminus V(t^2-s)
\]
has nonconstant units and different class data.  Its role is to show
that the local incidence established above does not, by itself, yield
a contradiction.

## 8. Boundary localization at the nodal fiber

At a self-identification \(q\) with \(b_q\ge2\), equation (3) says
that the entire cubic fiber is étale.  In particular it contains no
ramification boundary point and no non-Gorenstein boundary point.
The local principal pullback of the equation of \(\Gamma_D\) is split
among retained collision branches as in (23).

Therefore the global injection
\[
\bigoplus_i\mathbf Z[R_i]\hookrightarrow\operatorname{Cl}(Y)
\]
does not add a local relation at such a fiber: no \(R_i\) passes
through it for ramification reasons, and any optional unramified
boundary component would have to replace the third étale point in the
\(b_q=2\) case.  For \(b_q=3\), all three points are already retained
and no boundary point is possible.

The exact consequences for \(\Gamma_D\) are:

1. it avoids every non-Gorenstein value;
2. its singular locus avoids the branch curve;
3. every singularity has at most three analytic branches;
4. a triple point has no omitted sheet over it;
5. a node has at most one omitted unramified sheet over it.

These restrictions are compatible with both the class sequence and
the nodal countermodel.

## 9. Remaining route

A global contradiction would follow from an independent theorem that
forces one of:

1. \(\Delta\) to pass through a singular point of \(\Gamma_D\);
2. a non-Gorenstein value to lie on \(\Gamma_D\);
3. an ordinary four-fold self-identification of the normalization
   \(D=\mathbf A^1\);
4. two omitted sheets over a node or one omitted sheet over a triple
   point.

None of these has yet been forced by the Darboux or class-group
identities.  The next useful target is therefore an intersection
formula for \(\Delta\cdot\Gamma_D\) or a resultant identity involving
the Miranda building coefficients restricted to the polynomial
normalization \(D\).
