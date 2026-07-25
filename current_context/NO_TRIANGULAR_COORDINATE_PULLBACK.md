# No target polynomial pulls back to a triangular \(z\)-coordinate

Date: 24 July 2026

A direct nonlinear descent of the three-dimensional counterexample would be
available if some target coordinate \(H(A,B,C)\) pulled back to an elementary
source coordinate

\[
H(F(x,y,z))=\lambda z+\phi(x,y),\qquad \lambda\ne0.
\]

Then every level of \(H\circ F\) would be an affine plane.  This note proves
that no such target polynomial exists.  In fact the result holds for rational
\(H\), and the case \(\lambda=0\) forces \(H\) to be constant.

## 1. Cubic inverse parameter

For the verified map \(F=(a,b,c)\), set

\[
T=y+\frac1x.
\]

Over the target function field it satisfies

\[
\mathcal P(T)=cT^3-2T^2+bT-2a=0,
\tag{1}
\]

and

\[
r(T)=\mathcal P'(T)=3cT^2-4T+b=\frac2x.
\tag{2}
\]

If \(x,y\) are fixed and \(z\) varies, \(T\) is fixed and

\[
\frac{\partial F}{\partial z}
=\bigl((1+xy)^3,\ 3x(1+xy)^2,\ -x^3\bigr)
=x^3(T^3,3T^2,-1).
\]

Using (2), this is

\[
\frac8{r(T)^3}(T^3,3T^2,-1).
\tag{3}
\]

## 2. The forced target gradient

Assume

\[
\partial_z(H\circ F)=\lambda
\]

for a constant \(\lambda\).  Write \(H_A,H_B,H_C\) for the target partial
derivatives.  Formula (3) gives, at each of the three generic roots of
\(\mathcal P\),

\[
8\bigl(T^3H_A+3T^2H_B-H_C\bigr)
-\lambda r(T)^3=0.
\]

Therefore the cubic \(\mathcal P(T)\) divides the left side in
\(\mathbb C(A,B,C)[T]\).  Reducing modulo \(\mathcal P\) and equating the
coefficients of \(1,T,T^2\) gives a nonsingular linear system for the three
partial derivatives.  Its unique solution is

\[
\begin{aligned}
H_A&=\frac{\lambda(9AC-B)(3BC-4)}{4B},\\
H_B&=-\frac{\lambda(12A-B^2)(3BC-4)}{8B},\\
H_C&=-\frac{\lambda(12A-B^2)^2}{8B}.
\end{aligned}
\tag{4}
\]

These identities are function-field identities; working on the dense open
set \(B\ne0\) loses nothing.

## 3. Mixed partials contradict integrability

The first two expressions in (4) have curl

\[
\partial_BH_A-\partial_AH_B
=\frac{3\lambda(12AC+5B^2C-8B)}{4B^2},
\]

which is not the zero rational function when \(\lambda\ne0\).  Hence (4)
cannot be the gradient of any rational function \(H\), a fortiori of any
polynomial.

If \(\lambda=0\), the same nonsingular system gives
\(H_A=H_B=H_C=0\), so \(H\) is constant.

## Conclusion

There is no nonconstant target rational function whose pullback is
independent of \(z\), and no target rational function satisfying

\[
H\circ F=\lambda z+\phi(x,y)
\]

with \(\lambda\ne0\).  Thus nonlinear target coordinates cannot produce an
affine-plane source fiber by becoming an elementary triangular coordinate
in the source \(z\)-direction.

This does not exclude source coordinates obtained by longer, genuinely
three-variable polynomial automorphisms.
