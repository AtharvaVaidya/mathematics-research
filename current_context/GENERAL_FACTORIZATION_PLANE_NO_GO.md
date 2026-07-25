# No affine-plane descent from a marked linear factor, in any degree

Date: 24 July 2026

This note generalizes `FACTORIZATION_PLANE_NO_GO.md`.  It rules out not only
the linear-times-quadratic cover behind the known three-dimensional
counterexample, but every normalized linear-times-degree-\(d\) factorization
cover, for every \(d\geq2\), followed by intersection with an arbitrary
affine two-plane in the coefficient space.

All statements are over an algebraically closed field of characteristic zero.

## 1. The factorization cover

Put \(n=d+1\), and write

\[
L=pz+qw,\qquad
Q=\sum_{i=0}^{d}a_i z^{d-i}w^i .
\]

If

\[
LQ=\sum_{k=0}^{n}A_kz^{n-k}w^k,
\]

then, with \(a_{-1}=a_{d+1}=0\),

\[
A_k=pa_k+qa_{k-1}\qquad(0\leq k\leq n).
\tag{1}
\]

Normalize the resultant by

\[
\operatorname{Res}(L,Q)=Q(-q,p)
=\sum_{i=0}^{d}a_i(-q)^{d-i}p^i=1.
\tag{2}
\]

Let \(Y_d\) be the hypersurface (2), and let

\[
\mu_d:Y_d\longrightarrow \mathbb A^{n+1},\qquad (L,Q)\longmapsto LQ.
\]

The factors are coprime on \(Y_d\).  If an infinitesimal tangent vector is in
the kernel of multiplication, then

\[
\dot L\,Q+L\,\dot Q=0.
\]

Coprimality and degrees force \(\dot L=cL,\ \dot Q=-cQ\).  Under this
infinitesimal rescaling the resultant changes by \((d-1)c\).  Since \(d\geq2\),
the tangent equation to (2) forces \(c=0\).  Thus \(\mu_d\) is étale.  (The
normalization leaves a finite \(\mu_{d-1}\)-ambiguity for each marked root;
that does not affect the argument.)

Let \(\Pi=C+\langle F,G\rangle\) be any affine two-plane in the target, where
\(F,G\) are independent binary forms of degree \(n\).  We study

\[
X=\mu_d^{-1}(\Pi).
\]

Because \(\mu_d\) is étale, \(X\) is smooth.  A plane Keller counterexample
from this construction would have to be an \(\mathbb A^2\)-component of \(X\)
on which \(\mu_d\) is noninjective.

## 2. The projection determinant is a Wronskian

Write

\[
F=\sum_{k=0}^{n}f_kz^{n-k}w^k,\qquad
G=\sum_{k=0}^{n}g_kz^{n-k}w^k.
\]

For fixed \((p,q)\), introduce the two plane coordinates \(s,t\).  Equations

\[
pa_k+qa_{k-1}=C_k+sf_k+tg_k\quad(0\leq k\leq n)
\tag{3}
\]

together with (2) form a square linear system for

\[
(a_0,\ldots,a_d,s,t).
\]

Let \(M_{F,G}(p,q)\) be its coefficient matrix, with the \(s,t\) columns
written as \(-f_k,-g_k\).  Its determinant has a short intrinsic
interpretation.  A vector in the kernel gives a pencil member
\(H=sF+tG=L\dot Q\).  The resultant tangent row says
\(\dot Q(-q,p)=0\), so \(H\) is divisible by \(L^2\).  Such a pencil member
exists exactly when the pencil map \([F:G]\) is ramified at the root
\([-q:p]\), namely when \(W(F,G)(-q,p)=0\).  Both sides below are bilinear
alternating forms in \(F,G\) of the same degree in \(p,q\); evaluating at
\(F=z^{d+1},G=w^{d+1}\) fixes the scalar.  This proves the universal
identity

\[
\det M_{F,G}(p,q)
=\frac{1}{d+1}
\bigl(F_zG_w-F_wG_z\bigr)(-q,p).
\tag{4}
\]

The accompanying verifier additionally expands (4) symbolically for
\(2\leq d\leq6\).

Set

\[
W(F,G)=F_zG_w-F_wG_z.
\]

Since \(F,G\) are independent in characteristic zero, \(W(F,G)\neq0\).
Away from the union of lines

\[
D=V\bigl(W(F,G)(-q,p)\bigr)\subset\mathbb A^2_{p,q},
\]

projection \(X\to\mathbb A^2_{p,q}\) is an isomorphism.

## 3. Why two determinant lines exclude an affine plane

The origin \((p,q)=(0,0)\) has no preimage because of (2).  The reduced
determinant divisor is a union of lines through that missing origin.

At an isolated compatible point of a determinant line, the linear system
(2)--(3) acquires an affine-space fiber.  Rank-two vertical components are
harmless: for a fixed nonzero \(L\), multiplication \(Q\mapsto LQ\) is
linear and injective.  Consequently, if such a component is an affine plane,
its map to \(\Pi\) is an affine-linear isomorphism, not a counterexample.

If compatibility persists along a punctured determinant line, the resulting
two-dimensional component has the line parameter as a nonconstant unit, so
it is not \(\mathbb A^2\).

It remains to consider the unique component dominating
\(\mathbb A^2_{p,q}\).  Its constructible decomposition consists of
\(\mathbb A^2\setminus D\), whose Euler characteristic is zero, plus one
\(\mathbb A^1\)-contribution at every isolated compatible center.  Hence an
\(\mathbb A^2\)-component would need exactly one center.  If \(D\) has at
least two distinct lines, every other determinant line is absent from that
component; its defining linear form therefore pulls back to a nonconstant
unit.  This again excludes \(\mathbb A^2\).

Thus the only remaining possibility is that \(W(F,G)\) is supported at one
point of \(\mathbb P^1\).

## 4. Classification of the one-line Wronskian

Let \(R=\gcd(F,G)\), and write

\[
F=Rf,\qquad G=Rg,
\]

where \(f,g\) are coprime binary forms of the same degree
\(m=n-\deg R\).  Passing to one affine coordinate (where the ordinary
one-variable Wronskian has cancelling cross terms) gives the homogeneous
identity

\[
W(F,G)=\frac{n}{m}R^2W(f,g).
\tag{5}
\]

If \(m\geq2\), the rational map

\[
[f:g]:\mathbb P^1\longrightarrow\mathbb P^1
\]

has degree \(m\).  Its Wronskian is its ramification divisor, of total degree
\(2m-2\).  A single point contributes at most \(m-1\), so the ramification
divisor has at least two distinct points.  Therefore a one-point Wronskian
forces \(m=1\).

The nonzero scalar \(n/m\) does not change the zero divisor.  It follows
from (5) that

\[
\deg R=d,\qquad R=\ell^d
\]

for one linear form \(\ell\), and hence

\[
\langle F,G\rangle=\ell^d\operatorname{Sym}^1.
\tag{6}
\]

After an \(SL_2\)-change of variables, take \(\ell=w\).  The affine plane
then varies only the last two product coefficients \(A_d,A_{d+1}\), while

\[
A_0=c_0,\ldots,A_{d-1}=c_{d-1}
\tag{7}
\]

are fixed.

## 5. The exceptional pencil is still harmless

On \(p\neq0\), (1) and (7) reconstruct recursively

\[
a_0=\frac{c_0}{p},\qquad
a_i=\frac{c_i-qa_{i-1}}p\quad(1\leq i\leq d-1).
\tag{8}
\]

Equation (2), whose coefficient of \(a_d\) is \(p^d\), then reconstructs
\(a_d\) uniquely.  This locus is

\[
\mathbb G_m\times\mathbb A^1,
\]

with coordinates \(p,q\), and is not an affine plane.

On \(p=0\), compatibility with (2) forces \(q\neq0\).  If the fixed
coefficients are compatible, then

\[
a_{k-1}=c_k/q\qquad(1\leq k\leq d-1),
\]

while \(a_{d-1},a_d\) are free.  (The equations
\((-1)^dc_1q^{d-1}=1\) leave only finitely many possible nonzero values of
\(q\).)  Each resulting component is an affine plane, but its two varying
target coordinates are

\[
(A_d,A_{d+1})=(qa_{d-1},qa_d).
\tag{9}
\]

Because \(q\neq0\), (9) is a linear automorphism of that affine plane.

## Conclusion

For every \(d\geq2\), every affine target two-plane \(\Pi\), and every
component of

\[
\mu_d^{-1}(\Pi)\subset
\{\operatorname{Res}(L,Q)=1\},
\]

an affine-plane component maps injectively (indeed linearly in the only
exceptional case).  All other components are excluded from being
\(\mathbb A^2\) by Euler characteristic or by a nonconstant unit.

Therefore no two-dimensional Jacobian counterexample can be obtained by:

1. marking a linear factor of a binary form of arbitrary degree,
2. normalizing its resultant with the complementary factor, and
3. cutting the coefficient target by an arbitrary affine two-plane.
