# Audit of the leading osculating-cubic ODE

Date: 24 July 2026

## Verdict

The leading bracket equation for the universal osculating cubic is exact,
but it does **not** contradict the full a/b support when \(r=4\).  The
apparent contradiction misses the resonant top \(y\)-degree.

Let
\[
P_{2r}=\alpha x^{2r}\rho(y)^2,\qquad
Q_{3r}=\beta x^{3r}\rho(y)^3,\qquad
\rho=y^{2r-1}(uy+v),
\]
with \(\alpha\beta uv\ne0\), and put
\[
K=\mathcal H(P,Q).
\]
The universal theorem gives \(\deg_xK\le r+3\), while
\[
[P,K]=(2Q+c_5P+c_3)x^2.
\]
Therefore \(\deg_xK=r+3\).  If
\[
K_{r+3}=x^{r+3}k(y),
\]
comparison of the top \(x\)-degree gives
\[
\boxed{
r\rho k'-(r+3)\rho'k=\frac{\beta}{\alpha}\rho^2.
}
\tag{1}
\]

For \(r=2\) and every \(r\ge4\), equation (1) has a unique polynomial
solution in the allowed support.  It has the form
\[
\boxed{
k(y)=y^{2r}(uy+v)^2
H_r\!\left(\frac{uy}{v}\right),
}
\tag{2}
\]
where \(H_r(t)=\sum_{n=0}^4a_nt^n\) is a genuine quartic.  Its
coefficients are determined by
\[
\begin{aligned}
(3-5r)v\,a_0&=\frac{\beta}{\alpha},\\
\bigl(r(n-5)+3\bigr)a_n+r(n-5)a_{n-1}&=0,
\qquad1\le n\le4.
\end{aligned}
\tag{3}
\]
Equivalently,
\[
a_n=a_0\prod_{m=5-n}^{4}\frac{rm}{3-rm}.
\tag{4}
\]
In particular
\[
\boxed{\deg_yk=2r+6,}
\]
not \(2r+1\).  The coefficient of the apparent top degree cancels in
the left side of (1); this is the infinity resonance
\[
r(2r+6)-(r+3)(2r)=0.
\]

There is no support violation.  Under
\[
z=xy,\qquad w=xy^2,
\]
the five terms in (2) become
\[
x^{r+3}y^{2r+2+n}=z^{4-n}w^{r-1+n},
\qquad0\le n\le4.
\]
Thus the solution occupies the exact total-degree-\((r+3)\) window
\[
w^{r-1}\langle z^4,z^3w,z^2w^2,zw^3,w^4\rangle,
\]
including the allowed pure-\(w\) endpoint \(w^{r+3}\).
This window is compatible with both full a/b and full case-c composite
supports: it uses radial \(z\)-degrees \(0,1,2,3,4\), all within the
\(0,\ldots,6\) window of \(Q^2-LP^3\).  The additional negative radial
blocks in case c do not remove these monomials.

For the actual a/b value \(r=4\), every coefficient in (3) is nonzero.
The leading ODE therefore supplies a rigid five-term initial form, not an
obstruction.

There is a genuine exceptional obstruction at \(r=3\).  At the simple
root \(uy+v=0\), a regular polynomial solution would have order two, but
the indicial coefficient
\[
rs-(r+3)=3\cdot2-6
\]
vanishes, so the left side has order greater than two while the right
side has exact order two.  Equivalently, the \(n=4\) recurrence in (3)
has zero coefficient on \(a_4\) and forces the already nonzero \(a_3\)
to vanish.  This exceptional small-\(r\) observation does not apply to
the \(r=4\) GGHV branch.

## Derivation

For \(r=2\) or \(r\ge4\), valuation at \(y=0\) in (1) forces
\(\operatorname{ord}_0k=2r\), and valuation at \(uy+v=0\) forces order
two.  Hence write
\[
k=y^{2r}(uy+v)^2h(y).
\]
After canceling \(y^{4r-2}(uy+v)^2\), equation (1) becomes
\[
r\,y(uy+v)h'
+\bigl(-4ruy+(3-5r)v\bigr)h
=\frac{\beta}{\alpha}.
\tag{4}
\]
Putting \(t=uy/v\) gives recurrence (3).  For \(r=2\) and every
\(r\ge4\), none of its four denominators vanishes.  Starting from the
nonzero \(a_0\), it produces nonzero \(a_1,\ldots,a_4\); the coefficient
of degree five is then forced to zero.  This proves (2), (4), and the
exact degree.

## Strategic use

Equation (1) remains useful: it canonically determines the entire top
five-term slice of \(K\).  A promising next step is to compare this
forced slice with the independently determined boundary polynomial
\(\mathcal H(p(w),q(w))\), or with the four later five-block equations.
What is not sound is to discard the \(y^{2r+6}\) resonance and infer a
degree-\((2r+1)\) contradiction.
