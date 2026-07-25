# No plane counterexample from an affine two-plane of binary cubics

Date: 24 July 2026

The three-dimensional counterexample comes from normalized
linear-times-quadratic factorization of binary cubics.  A potentially broader
two-dimensional descent is to intersect the cubic target with an arbitrary
affine two-plane, without first passing through the particular affine
three-space used in the known example.  This note rules out that entire
linear-section construction.

## 1. The normalized factorization cover

Write

\[
L=pz+qw,\qquad Q=rz^2+szw+tw^2.
\]

Their product has coefficients

\[
(A,B,C,D)=(pr,\ ps+qr,\ pt+qs,\ qt).
\tag{1}
\]

Normalize the resultant:

\[
Y=\{p^2t-pqs+q^2r=1\}\subset\mathbb A^5.
\tag{2}
\]

Multiplication gives an étale map

\[
\mu:Y\longrightarrow\mathbb A^4_{A,B,C,D}.
\]

A generic cubic has three choices of its distinguished linear factor, so
\(\mu\) is generically three-to-one.

Let \(V\subset\mathbb A^4\) be any affine two-plane.  Choose two independent
linear forms

\[
U=(u_0,u_1,u_2,u_3),\qquad
V=(v_0,v_1,v_2,v_3)
\]

and constants \(\rho,\sigma\) so that the plane is

\[
U(A,B,C,D)=\rho,\qquad V(A,B,C,D)=\sigma.
\]

The source section \(X=\mu^{-1}(V)\) is smooth.  If a component of \(X\)
were an affine plane and the restriction of \(\mu\) were noninjective, it
would be a plane Keller counterexample.

## 2. Projection to the selected linear factor

For fixed \((p,q)\), equations (2) and the two plane equations are linear
in \((r,s,t)\).  Their coefficient matrix is

\[
M(p,q)=
\begin{pmatrix}
q^2&-pq&p^2\\
u_0p+u_1q&u_1p+u_2q&u_2p+u_3q\\
v_0p+v_1q&v_1p+v_2q&v_2p+v_3q
\end{pmatrix}.
\]

Put \(p_{ij}=u_iv_j-u_jv_i\).  Direct expansion gives the binary quartic

\[
\begin{aligned}
\Delta=\det M={}&p_{01}p^4+2p_{02}p^3q
+(p_{03}+3p_{12})p^2q^2\\
&+2p_{13}pq^3+p_{23}q^4.
\tag{3}
\end{aligned}
\]

The Plücker relation is

\[
p_{01}p_{23}-p_{02}p_{13}+p_{03}p_{12}=0.
\tag{4}
\]

Since \(U,V\) are independent, \(\Delta\) is not the zero polynomial:
if all five coefficients in (3) vanished, (4) would force
\(p_{03}=p_{12}=0\), and then every Plücker coordinate would vanish.

Away from \(V(\Delta)\), projection \(X\to\mathbb A^2_{p,q}\) is an
isomorphism.  The reduced zero set of a nonzero homogeneous binary form is
a union of lines through the origin and has Euler characteristic \(1\).
The origin itself has no preimage because the first equation has right-hand
side \(1\).

On each punctured determinant line, compatibility of the three linear
equations normally occurs at finitely many scale values.  At a rank-two
compatible point the fiber is \(\mathbb A^1\).  If compatibility persists
along a whole punctured line instead, the corresponding surface carries the
line parameter as a nonconstant unit and is not \(\mathbb A^2\).  After
discarding such Laurent components, the nonvertical component has a
constructible decomposition

\[
(\mathbb A^2\setminus V(\Delta))
\ \sqcup\ \coprod_{\text{centers}}\mathbb A^1,
\]

so its Euler characteristic is the number of centers.

If the reduced quartic has at least two distinct line factors, this excludes
\(\mathbb A^2\): zero or at least two centers give the wrong Euler
characteristic, while exactly one center leaves every other determinant-line
factor as a nonconstant unit on the section.  Rank-one fibers, when they
occur, are vertical affine-plane components.  For fixed nonzero \(L\), the
map \(Q\mapsto LQ\) is linear and injective, so its restriction to any such
two-dimensional vertical component is an affine-linear isomorphism onto the
target plane; it cannot carry noninjectivity.

Thus only the case in which \(\Delta\) is a fourth power of one linear form
can possibly remain.

## 3. Classification of the fourth-power case

After an \(SL_2\) change of \((z,w)\), suppose
\(\Delta\) is a nonzero multiple of \(p^4\).  Equations (3) give

\[
p_{01}\ne0,\quad
p_{02}=p_{13}=p_{23}=0,\quad
p_{03}+3p_{12}=0.
\]

The Plücker relation reduces to \(p_{03}p_{12}=0\).  In characteristic zero
this forces

\[
p_{03}=p_{12}=0.
\]

Hence the only nonzero Plücker coordinate is \(p_{01}\).  Up to changing
the basis of the two plane equations, the pencil is exactly

\[
\langle A,B\rangle.
\]

It remains to analyze

\[
pr=\rho,\qquad ps+qr=\sigma,\qquad
p^2t-pqs+q^2r=1.
\tag{5}
\]

### If \(\rho\ne0\)

Then \(p\) is invertible and (5) uniquely reconstructs

\[
r=\rho/p,\qquad
s=(\sigma p-q\rho)/p^2,
\]

and then \(t\).  Thus

\[
X\cong\mathbb G_m\times\mathbb A^1,
\]

not \(\mathbb A^2\).

### If \(\rho=0,\ \sigma\ne0\)

Equation \(pr=0\) splits the smooth section into two disjoint components.
On \(p=0\), equations (5) give

\[
q=1/\sigma,\qquad r=\sigma^2,
\]

while \(s,t\) are free.  This component is \(\mathbb A^2\), but (1) gives

\[
(C,D)=(s/\sigma,t/\sigma),
\]

so its map to the target two-plane is a linear automorphism.

On the other component \(r=0\), one has

\[
s=\sigma/p,\qquad t=(1+q\sigma)/p^2,
\]

and therefore the component is
\(\mathbb G_m\times\mathbb A^1\).

### If \(\rho=\sigma=0\)

The \(p=0\) branch is inconsistent with the resultant equation.  The other
branch has

\[
r=s=0,\qquad t=p^{-2},
\]

and is again \(\mathbb G_m\times\mathbb A^1\).

## Conclusion

For every affine two-plane in the binary-cubic target, no component of its
normalized factorization preimage gives a noninjective étale
\(\mathbb A^2\to\mathbb A^2\).  Every nonvertical component is excluded by
Euler characteristic or by a nonconstant unit.  The unique exceptional
fourth-power pencil can contain a flat affine-plane component, but the map
on that component is an explicit linear automorphism.

Thus the linear-times-quadratic factorization mechanism that disproves the
Jacobian conjecture in dimension three cannot be reduced to dimension two
by *any* affine two-plane section of the original four-dimensional cubic
coefficient space.
