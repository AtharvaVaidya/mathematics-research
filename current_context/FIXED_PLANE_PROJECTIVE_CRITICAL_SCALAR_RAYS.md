# Projective critical incidence on two fixed-plane scalar rays

Date: 26 July 2026

## Outcome

Let \(U_0,D,K\) be the fixed-plane polynomials, and put
\[
 E=DK.
\]
This note studies two exact one-parameter families
\[
 U_\lambda^{(1)}=U_0+\lambda E^2,\qquad
 U_\lambda^{(t)}=U_0+\lambda tE^2.
\tag{1}
\]
The parameter is denoted by \(\lambda\) to distinguish it from the
source coordinate \(t\).

Neither ray contains a polynomial submersion.  More precisely, counting
scheme length:

\[
\begin{array}{c|c}
 \text{family and parameter}&
 \operatorname {length}\operatorname {Crit}(U_\lambda)\\ \hline
 U_\lambda^{(1)},\ \lambda=0&14\\
 U_\lambda^{(1)},\ \lambda\ne0,\
 104976\lambda^2+5751\lambda+2\ne0&21\\
 U_\lambda^{(1)},\
 104976\lambda^2+5751\lambda+2=0&20\\ \hline
 U_\lambda^{(t)},\ \lambda=0&14\\
 U_\lambda^{(t)},\
 \lambda\ne0,\lambda\notin
 \{-1/24,9/8,-1/972\}&21\\
 U_\lambda^{(t)},\ \lambda=-1/24&21\\
 U_\lambda^{(t)},\ \lambda=9/8&19\\
 U_\lambda^{(t)},\ \lambda=-1/972&20 .
\end{array}
\tag{2}
\]

Thus every member of both rays has an affine critical point.  The
exceptional losses in (2) are genuine collisions with infinity:

- on the \(E^2\)-ray, one point escapes to \([0:1:0]\) at each of
  \[
  \lambda=\frac{-71\pm17\sqrt {17}}{2592};
  \tag{3}
  \]
- on the \(tE^2\)-ray, two points escape to \([1:0:0]\) at
  \(\lambda=9/8\), and one escapes there at \(\lambda=-1/972\);
- at \(\lambda=-1/24\), the two branches with \(c\to0\) instead land
  at two finite, simple critical points on \(c=0\).

This also gives a sharp warning about the proposed leading-form
strategy.  On either punctured ray the leading homogeneous form is
constant up to a nonzero scalar, but the local intersection
multiplicity at infinity still jumps.  The leading form determines
the *support* of the critical scheme at infinity; it does not determine
whether affine critical points escape.  Any general criterion for the
whole coset \(U_0+(E^2)\) must use lower homogeneous jets.

## 1. What the leading form does determine

The exact leading forms are
\[
 E_8=81c^4t^4,\qquad
 (U_0)_{11}=-\frac{81}{2}c^5t^6.
\tag{4}
\]
If \(\phi\) has degree \(d\), with leading binary form \(\Phi_d\), then
for \(\phi\ne0\)
\[
 (U_0+E^2\phi)_{16+d}
 =6561c^8t^8\Phi_d(t,c).
\tag{5}
\]
After homogenizing the two gradient equations to degree \(15+d\),
their restrictions to the line at infinity are the two partial
derivatives of (5).  Euler's identity shows that their common points
are precisely the multiple roots of the binary form
\[
 c^8t^8\Phi_d(t,c).
\tag{6}
\]
In particular, the two coordinate points
\[
 P_t=[1:0:0],\qquad P_c=[0:1:0]
\tag{7}
\]
are always present.  If \(\Phi_d\) is squarefree and coprime to \(tc\),
there are no other points in the support at infinity.

This support statement is rigorous but insufficient.  Local
intersection numbers depend on lower homogeneous pieces of the two
gradient equations.  The jumps below occur while (5) is unchanged
projectively.

## 2. Resultant bookkeeping

Let
\[
 R_\phi(c,\lambda)
 =
 \operatorname {Res}_t
 \left(
  (U_0+\lambda E^2\phi)_t,
  (U_0+\lambda E^2\phi)_c
 \right).
\tag{8}
\]
The large powers of \(c\) in this affine resultant are endpoint
factors caused by degree loss in \(t\) at the fixed projective
basepoint \(P_t\).  Their exponents are not, by themselves, the full
local intersection multiplicity at \(P_t\).  The remaining primitive
factor records the moving affine critical scheme, except when its
endpoint at \(c=0\) is itself projective.  Its highest
\(c\)-coefficient detects escape to \(P_c\).

Here scheme length is recovered from the resultant with
multiplicity, not merely by counting its distinct roots.  Precisely,
after fixing \(\lambda\), localize at a finite value \(c=c_0\) where
the two \(t\)-leading coefficients are units.  The standard local
resultant formula gives
\[
 \operatorname {ord}_{c_0}\operatorname {Res}_t(F,G)
 =
 \operatorname {length}_{\mathbf C}
 \frac{\mathbf C[[c-c_0]][t]}{(F,G)}.
\tag{8a}
\]
One may prove (8a) by making \(F\) monic and identifying the resultant
with the determinant of multiplication by \(G\) on the finite free
\(\mathbf C[[c-c_0]]\)-module
\(\mathbf C[[c-c_0]][t]/(F)\).  Thus the degree of the primitive
factor, after removing any projective endpoint contribution, is the
total affine critical-scheme length.  At the exceptional finite
points with \(c=0\) below, length is instead checked directly by the
Hessian.

At \(\lambda=0\), the primitive moving factor specializes, up to a
nonzero rational scalar, to the squarefree degree-\(14\) eliminant of
\(\operatorname {Crit}(U_0)\).  Turning on \(\lambda\) introduces seven
additional affine branches from infinity.  There is no globally
canonical division of the moving cover into “old” and “new” branches;
the exact invariant is its total affine length.

## 3. The scalar \(E^2\)-ray

Exact elimination gives
\[
 R_1(c,\lambda)
 \doteq
 \lambda^2c^{52}P_1(c,\lambda),
\tag{9}
\]
where \(\doteq\) means equality up to a nonzero rational scalar, and
\[
 \deg_cP_1=21,\qquad \deg_\lambda P_1=9.
\tag{10}
\]
The endpoint coefficients are
\[
 P_1(0,\lambda)\in\mathbf Q^\times
\tag{11}
\]
and
\[
 [c^{21}]P_1
 \doteq
 \lambda^3
 \left(104976\lambda^2+5751\lambda+2\right)^2.
\tag{12}
\]
At a root of the quadratic in (12), the \(c^{20}\)-coefficient is
nonzero.  Hence \(P_1\) has degree \(21\) for every other nonzero
\(\lambda\), and degree \(20\) at the two roots (3).  Because (11)
never vanishes, every one of those roots has \(c\ne0\).

For \(c\lambda\ne0\), the two critical equations have respective
\(t\)-degrees \(7,8\), with leading coefficients
\[
 52488c^8\lambda,\qquad 52488c^7\lambda.
\tag{13}
\]
Thus every zero of \(P_1\) gives a finite common \(t\)-root.  This
proves the first half of (2).

For \(\lambda\ne0\), \(U_\lambda^{(1)}\) has degree \(16\), so the two
projective gradient curves have degree \(15\) and total intersection
number \(225\).  The affine length is generically \(21\), leaving
intersection length \(204\) at infinity.  At either value (3), the
degree drop in (12), together with (11) and (13), shows that exactly
one branch reaches \(c=\infty\), hence \(P_c\); the infinity length is
then \(205\).

## 4. The scalar \(tE^2\)-ray

Here exact elimination gives
\[
 R_t(c,\lambda)
 \doteq
 \lambda^3c^{64}P_t(c,\lambda),
\tag{14}
\]
with
\[
 \deg_cP_t=21,\qquad \deg_\lambda P_t=10,
\tag{15}
\]
and
\[
 [c^{21}]P_t\doteq\lambda^4,
\tag{16}
\]
\[
 P_t(0,\lambda)
 \doteq
 (8\lambda-9)(24\lambda+1)^2(972\lambda+1).
\tag{17}
\]
For \(c\lambda\ne0\), the two equations have \(t\)-degrees \(8,9\)
and leading coefficients
\[
 59049c^8\lambda,\qquad 52488c^7\lambda.
\tag{18}
\]

The \(c\)-adic orders of the specializations of \(P_t\) are
\[
\begin{array}{c|ccc}
\lambda&9/8&-1/24&-1/972\\ \hline
\operatorname {ord}_cP_t(c,\lambda)&2&2&1 .
\end{array}
\tag{19}
\]
Direct restriction of the two critical equations to \(c=0\) gives
\[
 (U_\lambda^{(t)})_t\big|_{c=0}
 =\frac83(24\lambda+1),
\tag{20}
\]
\[
 (U_\lambda^{(t)})_c\big|_{c=0}
 =-6\left(
 160\lambda t^2+144\lambda t+4t^2+9t+3
 \right).
\tag{21}
\]
At \(9/8\) and \(-1/972\), (20) is nonzero.  The orders \(2\) and
\(1\) in (19) therefore represent projective roots with
\(c\to0,t\to\infty\), namely collisions with \(P_t\).

At \(-1/24\), equation (20) vanishes identically and (21) becomes
\[
 2(8t^2-9t-9).
\tag{22}
\]
Its two roots are
\[
 t=\frac{9\pm3\sqrt {41}}{16}.
\tag{23}
\]
On \(c=0\), the Hessian determinant is
\[
 -4(16t-9)^2,
\tag{24}
\]
and hence equals \(-1476\) at either root.  Both points are therefore
simple affine critical points.  This proves all counts in the second
half of (2).

For nonzero \(\lambda\), this family has degree \(17\), and the
projective gradient intersection number is \(16^2=256\).  The
infinity length is \(235\) generically and also at \(-1/24\); it jumps
to \(237\) at \(9/8\) and to \(236\) at \(-1/972\).

## 5. Consequence and limit

These two rays rigorously rule out the simplest scalar deformations,
including the source-linear direction \(tE^2\).  They also disprove
the tempting assertion that a fixed leading homogeneous form prevents
critical branches from escaping: the exceptional values above have
the same projective leading form as all neighboring nonzero values.

The calculation does **not** prove that every
\(\phi\in\mathbf C[t,c]\) leaves an affine critical point.  It instead
identifies the missing ingredient in any such theorem: one must
control the lower homogeneous jets at \(P_t,P_c\), and, when
\(\Phi_d\) is not squarefree, at the additional multiple roots of
(6).  A leading-form-only criterion cannot settle the full coset.

The supporting exact calculation is
`verify_fixed_plane_projective_critical_scalar_rays.py`.
