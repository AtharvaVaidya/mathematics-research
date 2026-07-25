# No target pullback has a nonzero constant directional derivative

Date: 24 July 2026

This strengthens the elementary-coordinate obstruction.  Let

\[
\delta=\alpha\partial_x+\beta\partial_y+\gamma\partial_z
\]

be any nonzero constant vector field on the source of the verified
three-dimensional Keller map \(F\).  There is no rational target function
\(H(A,B,C)\) satisfying

\[
\delta(H\circ F)=1.
\tag{1}
\]

Consequently no target polynomial can pull back to a source coordinate that
becomes elementary triangular after an arbitrary affine-linear change of
source coordinates.

## 1. Forced one-form from the cubic inverse

Use

\[
\mathcal P(T)=CT^3-2T^2+BT-2A,\qquad
r=\mathcal P'(T),
\]

and reconstruct the source by

\[
x=2/r,\qquad y=T-r/2,\qquad
z=5r^2/4-3Tr/2-Cr^3/8.
\]

Write \(h=(H_A,H_B,H_C)^t\).  The chain rule for (1) is

\[
\bigl(\alpha F_x+\beta F_y+\gamma F_z\bigr)\cdot h=1.
\tag{2}
\]

Substitute the reconstruction formulas, clear denominators, and reduce (2)
modulo \(\mathcal P(T)\).  Equating the coefficients of \(1,T,T^2\) gives

\[
M(A,B,C;\alpha,\beta,\gamma)h
=b(A,B,C;\alpha,\beta,\gamma),
\tag{3}
\]

an exact \(3\times3\) linear system over the target function field.

Where \(\det M\ne0\), equation (3) forces the rational one-form

\[
h=M^{-1}b.
\]

For this one-form to equal \(dH\), its \(A,B\) curl must vanish.  With
\(n=\operatorname{adj}(M)b\) and \(d=\det M\), the numerator of that curl is

\[
\mathcal N=
(\partial_Bn_A)d-n_A(\partial_Bd)
-(\partial_An_B)d+n_B(\partial_Ad).
\tag{4}
\]

This formula is polynomial after clearing the harmless powers of \(C\)
introduced by division by the leading coefficient of \(\mathcal P\).

## 2. Finite exact projective certificate

Specialize (4) at the three target points

\[
(-2,1,-2),\qquad(-2,1,-1),\qquad(-2,1,1).
\]

After removal of nonzero rational contents, this gives three homogeneous
quintics

\[
N_{-2},N_{-1},N_{1}
\in\mathbb Q[\alpha,\beta,\gamma],
\]

each with 21 terms.  Exact Gröbner reduction gives

\[
\begin{aligned}
(N_{-2},N_{-1},N_1,\alpha-1)&=(1),\\
(N_{-2},N_{-1},N_1,\beta-1)&=(1),\\
(N_{-2},N_{-1},N_1,\gamma-1)&=(1).
\end{aligned}
\tag{5}
\]

Equivalently, the three quintics have no common point in
\(\mathbb P^2_{\alpha,\beta,\gamma}\).

If \(\det M\) were identically zero for some nonzero direction, (4) would
vanish identically too, so that direction would also contradict (5).
Otherwise a solution of (1) would force the rational curl numerator (4) to
vanish identically and hence at all three displayed target points, again
contradicting (5).

## Conclusion

For every nonzero constant source vector field \(\delta\),

\[
\delta(H\circ F)\notin\mathbb C^\times
\]

for every rational target function \(H\).  In particular, no target
coordinate pulls back to a polynomial of the form

\[
\ell+\phi(m,n),
\]

where \((\ell,m,n)\) is any affine-linear source coordinate system.

The exact 21-term quintics are generated rather than transcribed; the
verifier constructs them from the map, performs all three rational
Gröbner-basis calculations, and checks that each basis is \([1]\).
