# Universal depressed-Wronskian bound

Date: 25 July 2026

## Theorem

Let \(r\ge2\), and let \(A(h),B(h)\) be polynomials of degrees \(2r,3r\)
whose leading terms lie on a cubic relation.  Suppose a generalized
Weierstrass polynomial

\[
\mathcal H(X,Y)
=Y^2-LX^3+c_5XY+c_4X^2+c_3Y+c_2X+c_0
\]

satisfies

\[
\deg_h\mathcal H(A,B)\le r+3.
\]

After completing the square, translating the \(X\)-coordinate, and
rescaling both coordinates, there are monic polynomials

\[
\deg X=2r,\qquad\deg T=3r
\]

such that

\[
D=T^2-X^3,\qquad
\deg D\le\max(2r,r+3).
\]

For

\[
W=2XT'-3X'T
\]

one has

\[
\boxed{\deg W\le\max(2,r-1)}.
\]

In particular, for every \(r\ge3\),

\[
\boxed{\deg W\le r-1}.
\]

This applies to every polynomial boundary restriction to which the
universal osculating-cubic theorem applies.  It is an all-scale
consequence, not a scale-four computation.

## Proof

Completing the square with

\[
T_0=B+\frac{c_5A+c_3}{2}
\]

gives

\[
\mathcal H(A,B)
=T_0^2-LA^3+\alpha A^2+\beta A+\gamma.
\]

Choose \(\ell^3=L\), put \(x=\ell A\), and translate
\(x=X+\alpha/(3\ell^2)\).  The quadratic term in the cubic disappears:

\[
\mathcal H(A,B)=T_0^2-X^3+pX+q.
\]

The leading coefficients \(x_0,t_0\) satisfy \(t_0^2=x_0^3\).
With \(c=t_0/x_0\), one has \(c^2=x_0,c^3=t_0\), so dividing \(X,T_0\)
by \(c^2,c^3\) makes both monic without changing any degree bound.
Consequently

\[
D=T^2-X^3
\]

is a scalar multiple of
\(\mathcal H(A,B)-pX-q\), whence

\[
\deg D\le d:=\max(2r,r+3).
\]

The exact identity

\[
T(2XT'-3X'T)=XD'-3X'D
\]

now gives

\[
\deg(TW)\le2r+d-1.
\]

Since \(T\) is monic of degree \(3r\),

\[
\deg W\le d-r-1=\max(2,r-1).
\]

No integral-domain assumption on a parameter quotient is needed for the
last leading-coefficient descent; monicity is enough.

## Ramification meaning

The same Wronskian is the numerator of

\[
\frac{d}{dh}\log\frac{T^2}{X^3}
=\frac{W}{XT}.
\]

Thus, away from zeros of \(X\) and \(T\), every finite critical point of
the cubic ratio is a zero of a polynomial of degree at most \(r-1\).
This packages the finite ramification budget into an explicit low-degree
object and is more rigid than the bare genus or Riemann--Hurwitz count.

There is an exact almost-Belyi ledger in the squarefree, pairwise-coprime
case.  Put \(d=\deg D\).  The map
\[
f=\frac{T^2}{X^3}:\mathbf P^1\longrightarrow\mathbf P^1
\]
has degree \(6r\).  Its simple roots of \(T\) contribute \(3r\) to
ramification over \(0\), its simple roots of \(X\) contribute \(4r\)
over \(\infty\), and the source point at infinity lies over \(1\) with
index \(6r-d\), contributing \(6r-d-1\).  Riemann--Hurwitz leaves
exactly
\[
(12r-2)-3r-4r-(6r-d-1)=d-r-1
\]
ramification units.  This is exactly the maximal degree allowed for
\(W\).  Because
\[
f'/f=W/(XT),
\]
the zeros of \(W\) are precisely those residual branch points, counted
with multiplicity.  When \(d=2r\), all residual ramification is encoded
by a degree-\((r-1)\) polynomial.

The bound also controls a marked nonimmersive point immediately.  If
\[
\operatorname{ord}_{h_0}(X-X_0)\ge m,\qquad
\operatorname{ord}_{h_0}(T-T_0)\ge m,
\]
then
\[
\operatorname{ord}_{h_0}W\ge m-1.
\]
The affine coordinate changes used to complete and depress the cubic
preserve this lower bound for the marked boundary pair.  Moreover \(W\)
cannot vanish identically when the parametrization is primitive:
\[
W=0\Longrightarrow (T^2/X^3)'=0
\Longrightarrow T^2=X^3
\Longrightarrow X=H^2,\ T=H^3,
\]
after monic normalization, so both original coordinates factor through
the degree-\(r\) polynomial \(H\).  Therefore every primitive marked
pair with \(r\ge3\) satisfies
\[
\boxed{m\le r}.
\]

At \(r=4\), this already excludes the \((5,8)\) and \((7,11)\) cells
without Gröbner elimination.  The critical order-three cell is not
excluded by the degree count alone; its exact vanishing uses the
scale-four triangular Wronskian system.

At \(r=4\), it gives \(\deg W\le3\).  Combining this with the marked
\((3,5)\) conditions produces the exact triangular system used in
`AB_DELTA1_35_WRONSKIAN_OBSTRUCTION.md`.

## Strategic limitation

The degree bound alone is not yet an all-\(r\) contradiction.  It must be
combined with the marked pole-sensitive local type and the node/collision
data that bare Riemann--Hurwitz does not see.  Its value is that the
remaining all-scale problem is now a classification of low-degree
Wronskians, rather than an elimination of all coefficients of \(A,B\).

Run:

```bash
.venv/bin/python route_bd_universal_depressed_wronskian.py
```
