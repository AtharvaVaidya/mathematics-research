# Standard-system two-jet derivative-lift countermodel

Date: 26 July 2026

## Outcome

At the level of reciprocal polynomial pairs with freely chosen
polynomial \(Q\)-corrections, the division-free Sylvester remainder
has no second-order obstruction.  It has an explicit polynomial
primitive whose coefficients exactly obey the reciprocal degree
bounds.

The jet \(S\) does not cancel the leading
\(\tau^{dq}R^{r-1}R'T^q\) remainder: it first enters one order later,
at \(\tau^{d(q+1)}\).  Rather, a free relative \(Q\)-correction kills
the leading remainder, and the next free correction kills the
\(S\)-dependent lift.  Both corrections are components of one exact
primitive.

More strongly, after adding this primitive one may add the ambient
\(\tau^{m-1}X\) direction and obtain exact maximal derivative-resultant
contact
\[
\operatorname{ord}_\tau\operatorname{Res}(P_X,Q_X)
=(n-1)(m-1)
\]
for every allowed two-jet \(P\) satisfying the bounds below, including
jets outside the reduced common-root tangent cone.

This is an ambient countermodel, not a reciprocal standard-system
solution and not a Keller pair.  The freely chosen primitive changes
the physical relative unit \(Q^a/P^b\); it need not be realizable by
the much narrower constants
\(\lambda_k\tau^kC^{m-k}\).  Consequently the next useful obstruction
must come from that standard-presentation restriction or from the
final homogenized Keller forcing, not from the derivative resultant
and reciprocal degree bounds alone.

## 1. Two-jet setup

Let
\[
n=ga,\qquad m=gb,\qquad \gcd(a,b)=1,\qquad a<b,
\]
and put
\[
q=\left\lfloor\frac ba\right\rfloor,\qquad
r=b-aq,\qquad 1\le r<a.
\tag{1}
\]
Fix a monic degree-\(g\) polynomial \(R\).  Let \(d\ge1\), with
\(2d\le n\), and take
\[
U=\tau^dT+\tau^{2d}S,\qquad
P=R^a+U,
\tag{2}
\]
where
\[
\deg_XT\le n-d,\qquad
\deg_XS\le n-2d.
\tag{3}
\]
If the vanishing \(X^{n-1}\)-coefficient normalization is imposed,
one simply intersects (3) with
\(\deg T,\deg S\le n-2\); nothing below changes.

Retain every polynomial binomial term before the first Laurent pole:
\[
Q_q
=\sum_{\ell=0}^{q}
\binom{b/a}{\ell}R^{\,b-a\ell}U^\ell .
\tag{4}
\]
Define
\[
H
=\sum_{\ell=1}^{q}
\ell\binom{b/a}{\ell}
R^{\,b-a\ell}U^{\ell-1},
\qquad
C_q=r\binom{b/a}{q}.
\tag{5}
\]
The division-free identity from the Sylvester correction audit works
with the whole polynomial \(U\), not merely a one-jet:
\[
\boxed{
(Q_q)_X-H P_X
=C_qR^{\,r-1}R'U^q.
}
\tag{6}
\]

## 2. The obstruction map is an exact derivative

Put
\[
\mathcal K
=-C_q\int R^{\,r-1}R'U^q\,dX,
\tag{7}
\]
where the integration constant is chosen to be zero.  More generally,
one may add a polynomial in \(\tau\) only when its coefficients obey
the same reciprocal bounds.  Characteristic zero makes
\(\mathcal K\) a polynomial in \(X,\tau\), and (6) gives
\[
\boxed{
(Q_q+\mathcal K)_X=H P_X.
}
\tag{8}
\]

This correction obeys the reciprocal degree bounds coefficient by
coefficient.  A term in \(U^q\) with \(j\) copies of \(S\) and
\(q-j\) copies of \(T\) has \(\tau\)-order
\[
d(q+j).
\tag{9}
\]
Before integration its \(X\)-degree is at most
\[
\begin{aligned}
&g(r-1)+(g-1)
+(q-j)(n-d)+j(n-2d)\\
&\hspace{25mm}=m-d(q+j)-1.
\end{aligned}
\tag{10}
\]
Its primitive therefore has degree at most
\[
m-d(q+j),
\tag{11}
\]
exactly the reciprocal bound for the coefficient of
\(\tau^{d(q+j)}\).  The hypothesis \(2d\le n\) also gives
\[
2qd\le m,
\]
so every term of \(\mathcal K\) lies in the allowed reciprocal range.

The first two coefficients display the failed obstruction map
explicitly:
\[
\begin{aligned}
[\tau^{dq}]\mathcal K
&=-C_q\int R^{\,r-1}R'T^q\,dX,\\
[\tau^{d(q+1)}]\mathcal K
&=-qC_q\int
R^{\,r-1}R'T^{q-1}S\,dX.
\end{aligned}
\tag{12}
\]
Thus the leading division-free remainder and the first \(S\)-dependent
lift both lie in the derivative of the allowed \(Q\)-coefficient
space.  No condition forcing
\[
T\in R^{a-1}k[X]
\tag{13}
\]
arises.  In particular, taking \(T\) coprime to \(R\) gives a
non-reduced-tangent two-jet with the same exact lift.

## 3. Maximal resultant contact

Let \(\delta\ne0\), and set
\[
Q^\sharp
=Q_q+\mathcal K+\delta\tau^{m-1}X.
\tag{14}
\]
The last term also saturates its reciprocal degree bound.  Equation
(8) becomes
\[
(Q^\sharp)_X=H P_X+\delta\tau^{m-1}.
\tag{15}
\]
Since \(P_X\) has degree \(n-1\), leading coefficient \(n\), and its
leading coefficient is independent of \(\tau\), the root-product
formula gives
\[
\boxed{
\operatorname{Res}_X(P_X,(Q^\sharp)_X)
=\pm n^{m-1}\delta^{\,n-1}
\tau^{(m-1)(n-1)}.
}
\tag{16}
\]
The sign depends only on the resultant and coefficient-order
conventions.
Hence the contact is exactly \(D=(m-1)(n-1)\).

This construction explains why the first remainder from the
polynomial binomial truncation cannot, by itself, support the proposed
lifted-endpoint proof.  Once arbitrary polynomial relative corrections
are admitted, the remainder is exact and the determinant can be
saturated independently.

## 4. Scope

The construction proves only the following negative statement:

> Reciprocal coefficient bounds, honest approximate-root
> reparametrization, the physical relative unit, and the derivative
> resultant do not produce a second-order obstruction for a two-jet
> \(P=R^a+\tau^dT+\tau^{2d}S\) when \(Q\) may receive arbitrary
> polynomial corrections within its degree bounds.

It does not show that \(\mathcal K\) is available in the GGV standard
presentation.  Testing whether its coefficients can arise from the
finite collection
\[
\sum_k\lambda_k\tau^kC^{m-k}
\]
is the next, strictly smaller problem.  The final inhomogeneous
equation and the branchwise exact-differential residues are also not
imposed by (14).
