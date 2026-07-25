# No affine-plane fiber of any linear target coordinate

Date: 24 July 2026

This strengthens `LINEAR_SECTION_NO_GO.md`.  The earlier note treated the
hyperplanes through the displayed three-point collision.  Here the level is
arbitrary.  The conclusion is that **no** affine hyperplane in the target of
the verified three-dimensional Keller map has an inverse-image component
isomorphic to \(\mathbb A^2\) on which generic noninjectivity could descend.

## 1. An arbitrary linear fiber

Let \(F=(a,b,c)\) be the three-dimensional map and fix

\[
\ell(A,B,C)=\alpha A+\beta B+\gamma C\ne0,\qquad \tau\in\mathbb C.
\]

The fiber

\[
S_{\ell,\tau}=\{\ell(F)=\tau\}
\]

is smooth: \(d(\ell\circ F)\) is nowhere zero because \(JF\) is invertible.
With \(e=1+xy\), its equation is

\[
A(x,y)z+C_\tau(x,y)=0,
\]

where

\[
A=\alpha e^3+3\beta xe^2-\gamma x^3
\tag{1}
\]

and

\[
\begin{aligned}
C_\tau={}&\alpha y^2e(4+3xy)
+\beta\bigl(y+3xy^2(4+3xy)\bigr)\\
&+\gamma(2x-3x^2y)-\tau .
\end{aligned}
\tag{2}
\]

After common factors are separated, every vertical component is a cylinder
over a factor of \(A\).  Smoothness makes distinct components disjoint.  The
unique possible nonvertical component has a primitive equation

\[
A_0z+C_0=0,\qquad (A_0,C_0)=1.
\]

Writing \(Z=V(A_0,C_0)\), projection to the \((x,y)\)-plane gives

\[
S_0=(\mathbb A^2\setminus V(A_0))\sqcup(Z\times\mathbb A^1)
\]

and hence

\[
\chi(S_0)=1-\chi(V(A_0))+\#Z.
\tag{3}
\]

## 2. The case \(\alpha\ne0\)

At \(x=0\), \(A=\alpha\), so all components of \(V(A)\) lie in
\(x\ne0\).  Setting \(r=e/x\) gives

\[
A=x^3(\alpha r^3+3\beta r^2-\gamma).
\]

Every reduced factor is a curve

\[
e=r_i x,\qquad x(y-r_i)=-1,
\]

isomorphic to \(\mathbb G_m\); distinct such curves are disjoint.  Removing
common factors only removes some of these curves.  Smoothness prevents a
removed vertical factor from meeting the residual component, so it cannot
remove the last residual divisor factor without making the fiber singular.

Thus every vertical component is
\(\mathbb G_m\times\mathbb A^1\), not \(\mathbb A^2\), while the
nonvertical component has \(\chi(V(A_0))=0\).  If \(Z\ne\varnothing\),
equation (3) gives \(\chi(S_0)>1\).  If \(Z=\varnothing\), then \(A_0\) is a
nonconstant unit in the section ring.  In neither case is \(S_0\) an affine
plane.  Notice that \(\tau\) never entered this argument.

## 3. The case \(\alpha=0,\ \beta\ne0\)

Now

\[
A=xB,\qquad B=3\beta e^2-\gamma x^2.
\]

The reduced zero divisor is the disjoint union of the line \(x=0\) and one
or two \(\mathbb G_m\)-curves \(e=r_i x\).  On the line,

\[
C_\tau(0,y)=\beta y-\tau,
\]

so \(x\) is never a common factor and there is exactly one center on that
line, namely \((0,\tau/\beta)\).

If an additional center lies on a \(\mathbb G_m\)-factor, (3) gives
\(\chi(S_0)>1\).  If there is no additional center, the product of the
remaining \(\mathbb G_m\)-factors has no zero on \(S_0\), hence is a
nonconstant unit.

It remains only to justify that common factors do not erase every
\(\mathbb G_m\)-factor from the residual coefficient.  A common factor
\(\delta\mid B,C_\tau\) produces a vertical component \(\delta=0\).  If
\(\delta\nmid A_0\), then \(x\ne0\) on \(\delta=0\), and the residual linear
equation \(A_0z+C_0=0\) has a solution there.  The two components would
intersect, contradicting smoothness.  Therefore a common factor must remain
in \(A_0\) with positive multiplicity.  The unit/Euler alternative above
still applies.  Every vertical component is again
\(\mathbb G_m\times\mathbb A^1\).

Hence no fiber in this case has an affine-plane component.

## 4. The case \(\alpha=\beta=0\)

Here \(\gamma\ne0\), and after rescaling the equation is

\[
c=x(2-3xy-x^2z)=t.
\]

For \(t\ne0\), \(x\) is invertible and the fiber is
\(\mathbb G_m\times\mathbb A^1\): \(x,y\) are free with \(x\ne0\), and
\(z=(2-3xy-t/x)/x^2\).

For \(t=0\), the fiber is reducible.  The component \(x=0\) is
\(\mathbb A^2\), but the restricted target map on it is

\[
(y,z)\longmapsto(a,b)=(z+4y^2,y),
\]

a triangular automorphism.  The other component is
\(\mathbb G_m\times\mathbb A^1\).  Thus the sole affine-plane component is
globally injective and supplies no counterexample.

## Conclusion

For every nonconstant linear target coordinate \(\ell\) and every level
\(\tau\), no component of \(\ell(F)=\tau\) yields a noninjective étale map
\(\mathbb A^2\to\mathbb A^2\).  The only affine-plane component occurring
at all is the flat component of \(c=0\), and its restriction is an explicit
automorphism.

Consequently every dimension reduction of the new three-dimensional
counterexample by a linear target hyperplane is impossible.  Any successful
descent must use a genuinely nonlinear target coordinate.
