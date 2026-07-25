# No plane counterexample from a linear target section of the 3D map

Date: 24 July 2026

This is a new obstruction for dimension reduction from the verified
three-dimensional counterexample. It goes beyond checking only the coordinate
slice \(c=0\).

## 1. Why an affine-plane section would solve the plane problem

Write the three-dimensional Keller map as \(F=(a,b,c)\), with
\(\det JF=-2\), and let

\[
q=(-1/4,0,0)
\]

be the common image of the three known collision points.

For a nonzero linear form

\[
\ell(A,B,C)=\alpha A+\beta B+\gamma C,
\]

put

\[
S_{\alpha,\beta,\gamma}
=\{\,\ell(F)=\ell(q)=-\alpha/4\,\}\subset\mathbb A^3.
\]

The differential of \(\ell\circ F\) is nowhere zero because \(JF\) is
invertible and \((\alpha,\beta,\gamma)\ne0\). Thus the surface is smooth.
After completing \(\ell\) to a linear coordinate system on the target, the
other two target coordinates restrict to an étale map from
\(S_{\alpha,\beta,\gamma}\) to \(\mathbb A^2\), and the three collision
points remain in one fiber.

Consequently, if any \(S_{\alpha,\beta,\gamma}\) were isomorphic to
\(\mathbb A^2\), this restriction would be a plane Keller counterexample.
The result below rules out every such linear section.

## 2. Affine-modification equation

Set

\[
e=1+xy.
\]

The map is

\[
\begin{aligned}
a&=e^3z+y^2e(4+3xy),\\
b&=y+3xe^2z+3xy^2(4+3xy),\\
c&=2x-3x^2y-x^3z.
\end{aligned}
\]

The section equation is

\[
A(x,y)z+C(x,y)=0,
\]

where

\[
A=\alpha e^3+3\beta xe^2-\gamma x^3
\tag{1}
\]

and

\[
\begin{aligned}
C={}&\alpha y^2e(4+3xy)
+\beta\bigl(y+3xy^2(4+3xy)\bigr)\\
&+\gamma(2x-3x^2y)+\alpha/4.
\end{aligned}
\tag{2}
\]

Let \(D=\gcd(A,C)\). The fiber factors as

\[
D\left((A/D)z+C/D\right)=0.
\]

The components coming from \(D=0\) are vertical cylinders. The possible
factors of \(D\) will be described below; except for the factor \(x\) in the
coordinate section \(c=0\), every one is a curve isomorphic to
\(\mathbb G_m\), so its cylinder is not \(\mathbb A^2\). The exceptional
\(x=0\) cylinder in \(c=0\) contains only the collision point
\((0,0,-1/4)\), while the other two collision points lie on the
\(\mathbb G_m\times\mathbb A^1\) component.

Smoothness prevents this division from removing a distinct divisor factor
completely from the residual coefficient. Indeed, if an irreducible
\(\delta\mid D\) did not divide \(A/D\), then over \(\delta=0\) the equation
\((A/D)z+C/D=0\) would have a solution for \(z\); the vertical and
nonvertical components would intersect there, making the fiber singular.
Thus a common divisor factor can occur only with enough multiplicity that it
still divides the residual \(A\). In particular, the residual coefficient is
nonconstant in the \(\alpha\ne0\) case, and in the
\(\alpha=0,\beta\ne0\) case it retains at least one of the
\(\mathbb G_m\)-factors in addition to \(x\).

It remains to analyze the unique possible nonvertical component. Replacing
\((A,C)\) by \((A/D,C/D)\), we may assume they are coprime. Then
\(Z=V(A,C)\) is finite, and projection to \((x,y)\) gives the constructible
decomposition

\[
S=(\mathbb A^2\setminus V(A))\ \sqcup\ (Z\times\mathbb A^1).
\tag{3}
\]

Thus

\[
\chi(S)=1-\chi(V(A))+\#Z.
\tag{4}
\]

Here \(\chi\) is the complex topological Euler characteristic; it is additive
on constructible sets, \(\chi(\mathbb A^1)=1\), and
\(\chi(\mathbb G_m)=0\).

## 3. Case \(\alpha\ne0\)

At \(x=0\), equation (1) gives \(A=\alpha\), so \(V(A)\) lies in
\(\{x\ne0\}\). Put \(r=e/x\). Then

\[
A=x^3\bigl(\alpha r^3+3\beta r^2-\gamma\bigr).
\]

For every distinct root \(r_i\) of the cubic, the corresponding reduced
component is

\[
D_{r_i}: e=r_ix
\quad\Longleftrightarrow\quad
x(y-r_i)=-1,
\]

which is isomorphic to \(\mathbb G_m\). Different \(D_{r_i}\) are disjoint.
Therefore

\[
\chi(V(A))=0.
\]

The same description applies after common \(\mathbb G_m\)-factors have been
removed: \(V(A)\) is simply the union of the remaining \(D_{r_i}\)'s.

If \(Z\ne\varnothing\), equation (4) gives

\[
\chi(S)=1+\#Z>1=\chi(\mathbb A^2).
\]

If \(Z=\varnothing\), then \((A,C)=(1)\) in \(\mathbb C[x,y]\). In the
section ring, \(C=-Az\), so a Bézout identity makes \(A\) a unit. It is a
nonconstant unit because \(\mathbb C[x,y]\) injects into the section ring.
This is again impossible for \(\mathbb A^2\), whose only units are constants.

Hence no section with \(\alpha\ne0\) is an affine plane.

## 4. Case \(\alpha=0,\ \beta\ne0\)

Now

\[
A=xB,\qquad B=3\beta e^2-\gamma x^2.
\]

Before removing any common \(\mathbb G_m\)-factors, the reduced divisor
\(V(A)\) is the disjoint union of the line
\[
D_0=\{x=0\}\cong\mathbb A^1
\]
and one or two curves \(e=r_ix\), each isomorphic to \(\mathbb G_m\).
Thus

\[
\chi(V(A))=1.
\]

The factor \(x\) cannot be common to \(A,C\), because on \(D_0\), equation
(2) restricts to \(C=\beta y\). Consequently the residual nonvertical
component still has \((0,0)\in Z\), and this is the unique center point on
\(D_0\). Removing common \(\mathbb G_m\)-factors changes neither this fact
nor the Euler characteristic contribution of the remaining
\(\mathbb G_m\)-divisors.

If \(\#Z>1\), equation (4) gives
\[
\chi(S)=\#Z>1.
\]

If \(\#Z=1\), none of the \(\mathbb G_m\)-components of \(V(B)\) meets the
center. Hence \(B\) has no zero on \(S\) and is a nonconstant unit in the
section ring. Either way the section is not \(\mathbb A^2\).

This includes the coordinate section \(b=0\). In that case the unit can be
displayed directly:

\[
(1+xy)
\left(3x^3yz+9x^2y^2+3x^2z+3xy-2\right)+2=xb.
\]

Modulo \(b\), the factor \(1+xy\) is therefore invertible and nonconstant.

## 5. Case \(\alpha=\beta=0\)

Then \(\gamma\ne0\) and the section is

\[
c=x(2-3xy-x^2z)=0,
\]

Its \(x=0\) component is \(\mathbb A^2\) but contains only the collision
point \((0,0,-1/4)\). Its other component is
\(2-3xy-x^2z=0\cong\mathbb G_m\times\mathbb A^1\) and contains the two
remaining collision points. Hence no affine-plane component contains a
collision pair.

## Conclusion

For every nonzero linear target form \(\ell\), neither the full special
source fiber \(\ell(F)=\ell(q)\) nor any component containing at least two
of the exact collision points is isomorphic to \(\mathbb A^2\). Therefore
the verified three-dimensional counterexample cannot yield a plane
counterexample by restricting to a linear target hyperplane through the
collision value, even if one is allowed to select a connected component.

The argument does **not** cover nonlinear target coordinates
\(H(a,b,c)\) that are components of polynomial automorphisms. Such nonlinear
sections remain a possible dimension-reduction route.

Run

```sh
.venv/bin/python current_context/verify_linear_sections.py
```

to verify the displayed polynomial identities and divisor parametrizations.
