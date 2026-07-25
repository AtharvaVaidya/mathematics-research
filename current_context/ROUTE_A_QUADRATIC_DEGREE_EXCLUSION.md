# Route A: exclusion of Galois generic degree

Date: 25 July 2026

## Audited statement

The following general observation is the main result of this memo.

> **Galois-degree exclusion.**
> Let \(S=\operatorname {Spec}B\) be a normal integral affine complex
> surface with
> \[
> B^\times=\mathbf C^\times.
> \]
> If
> \[
> F=(P,Q):S\longrightarrow\mathbf A^2
> \]
> is étale, then a finite function-field extension
> \[
> \operatorname {Frac}B/\mathbf C(P,Q)
> \]
> cannot be nontrivial and Galois.

For the Route A surface, let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad S=\operatorname {Spec}B,
\]
and equip \(B\) with the hypersurface Jacobian bracket
\[
\{u,v\}=-2w,\qquad
\{v,w\}=1+2uv,\qquad
\{u,w\}=-u^2.
\tag{1}
\]
If \(P,Q\in B\) satisfy
\[
\{P,Q\}=1,
\tag{2}
\]
then
\[
\bigl[\operatorname {Frac}B:\mathbf C(P,Q)\bigr]\ne2.
\tag{3}
\]

Indeed, (2) makes \((P,Q)\) étale, and every separable extension of
degree two is Galois.  Thus (3) is an immediate corollary of the general
exclusion.

## 1. Preliminary facts

Write
\[
h=w^2-u-u^2v.
\]
The three partial derivatives
\[
h_u=-1-2uv,\qquad h_v=-u^2,\qquad h_w=2w
\tag{4}
\]
have no common zero on \(S\): if \(u=w=0\), then \(h_u=-1\).
Thus \(S\) is smooth.  The polynomial \(h\), viewed as a primitive
linear polynomial in \(v\) over \(\mathbf C[u,w]\), is irreducible, so
\(B\) is a domain.

The bracket (1) is the negative residue/Jacobian Poisson bracket
associated with \(h\), in the convention used by Route A.  Equation
(4) also shows that its Poisson bivector is nowhere zero.  On the smooth
surface \(S\), it is therefore symplectic.
Consequently (2) implies
\[
dP\wedge dQ\ne0
\]
at every point.  Hence
\[
F=(P,Q):S\longrightarrow\mathbf A^2
\tag{5}
\]
is étale.  In particular \(P,Q\) are algebraically independent whenever
\(\operatorname {Frac}B/\mathbf C(P,Q)\) is finite.

The units of \(B\) are exactly the constants.  Indeed, after inverting
\(u\), the defining equation eliminates \(v\) and gives
\[
B_u\simeq\mathbf C[u,u^{-1},w],
\tag{6}
\]
whose units are \(cu^n\), with \(c\in\mathbf C^\times\) and
\(n\in\mathbf Z\).  If \(b\in B^\times\), its image in (6) is \(cu^n\).
For \(n>0\), the equality \(b=cu^n\) in \(B_u\), hence in the common
fraction field, is an equality in \(B\); it would make \(u^n\), and
therefore \(u\), a unit.  For \(n<0\), apply the same argument to
\(b^{-1}\).  But \(u\) is not a unit, since
\[
B/(u,w)\simeq\mathbf C[v]\ne0.
\]
Thus \(n=0\) and
\[
B^\times=\mathbf C^\times.
\tag{7}
\]

## 2. The actual normalization contains \(S\) as an open set

We prove the general Galois-degree exclusion.  Put
\[
K=\operatorname {Frac}B,\qquad
L=\mathbf C(P,Q).
\tag{8}
\]
Assume that \(K/L\) is finite, nontrivial, and Galois.  Since \(F\) is
étale, it is dominant and \(P,Q\) are algebraically independent.  Put
\(A=\mathbf C[P,Q]\simeq\mathbf C[x,y]\), and let \(A'\) be the
integral closure of \(A\) in \(K\).  Since \(A\) is excellent, \(A'\) is
finite over \(A\).  Set
\[
Y=\operatorname {Spec}A',\qquad
\pi:Y\longrightarrow\operatorname {Spec}A=\mathbf A^2.
\tag{9}
\]
This is the finite normalization of \(\mathbf A^2\) in the actual
function-field extension \(K/L\).

There is a canonical inclusion
\[
A'\subset B.
\tag{10}
\]
To see this, every element of \(A'\) is integral over \(A\), hence also
integral over \(B\), because \(A\subset B\).  Normality makes \(B\)
integrally closed, and both rings lie in \(K\), so the element belongs
to \(B\).
The inclusion (10) induces
\[
j:S\longrightarrow Y,\qquad F=\pi\circ j.
\tag{11}
\]

The morphism \(j\) is of finite type, separated, birational, and
quasi-finite.  For quasi-finiteness, each fiber of \(j\) lies in a
fiber of the étale morphism \(F\), and those fibers are finite.
Since \(Y\) is normal, the birational form of Zariski's Main Theorem
therefore makes \(j\) an open immersion.  We henceforth identify \(S\)
with the open subset \(j(S)\subset Y\).

This step is important: the proof does not choose an arbitrary finite
compactification of \(S\).  It uses the unique normalization determined
by the function-field extension (8).

## 3. A branch divisor must exist

The extension \(K/L\) is separable.  If the finite map \(\pi\) had no
codimension-one branch locus, Zariski--Nagata purity of the branch
locus, applied over the regular scheme \(\mathbf A^2\), would make
\(\pi\) finite étale.

But \(Y\) is connected because \(A'\) is a domain, and
\(\mathbf A^2_{\mathbf C}\) has trivial étale fundamental group.
It has no nontrivial connected finite étale cover.  Therefore the branch
locus of \(\pi\) contains a divisor.

Choose an irreducible branch component
\[
D=V(f)\subset\mathbf A^2,
\tag{12}
\]
where \(f\in A\simeq\mathbf C[x,y]\) is irreducible and nonconstant.

## 4. Galois symmetry removes the whole inverse image of \(D\)

At the generic point of \(D\), the ring \(A_{(f)}\) is a discrete
valuation ring.  Since \(K/L\) is Galois, its Galois group acts
transitively on the height-one primes
\[
E_1,\ldots,E_r
\tag{13}
\]
of \(A'\) above \((f)\), and their inertia groups are conjugate.  Because
\(D\) is a branch component, one inertia group is nontrivial.  Hence
every \(E_i\) is ramified.

There can be no additional vertical component or isolated topological
piece in \(\pi^{-1}(D)\).  Every irreducible component of
\[
V(fA')\subset Y
\]
has codimension one by the principal ideal theorem, and a
one-dimensional component maps finitely onto a one-dimensional closed
subset of \(D\), hence dominates \(D\).  Consequently
\[
\lvert\pi^{-1}(D)\rvert=\bigcup_{i=1}^r\lvert E_i\rvert.
\tag{14}
\]

The ramification locus of \(\pi\) is closed and contains the generic
point of every \(E_i\), so it contains their union.  On the other hand,
\(\pi|_S=F\) is étale.  Hence
\[
S\cap\bigcup_iE_i=\varnothing.
\tag{15}
\]
Combining (14) and (15),
\[
F^{-1}(D)=\varnothing.
\tag{16}
\]

It follows that \(f(P,Q)\) has no zero on \(S\), or equivalently
\[
f(P,Q)\in B^\times.
\tag{17}
\]
By (7), \(f(P,Q)\) is a nonzero scalar.

Finally, \(P,Q\) are algebraically independent, so evaluation gives an
injective map
\[
\mathbf C[x,y]\hookrightarrow B,\qquad x\mapsto P,\quad y\mapsto Q.
\]
The nonconstant polynomial \(f\) cannot map to a scalar.  This
contradicts (17) and proves the Galois-degree exclusion.  Since every
separable quadratic extension is Galois, the Route A conclusion (3)
follows.

## 5. Scope and remaining gaps

The general theorem excludes every nontrivial Galois generic extension,
and in particular generic degree \(2\), for the Route A surface.  It
does not exclude a non-Galois extension of degree \(3\) or higher.  Over
a branch divisor of a non-Galois normalization there may be both a
ramified component, which the open set removes, and an unramified
component that remains.  The unit argument then no longer forces the
pullback of the branch equation to be invertible.  In particular, a
degree-three candidate would have to be non-Galois; its Galois closure
would have group \(S_3\), rather than \(C_3\).  At each branch divisor
it must retain an unramified component, so its inertia type is
transpositional rather than total cubic ramification.

The result also does not by itself prove the two-variable Jacobian
conjecture.  Its value for Route A is as a rigorous low-degree
obstruction and as a precise indication of where the quadratic argument
stops generalizing.  No claim of novelty is made here; the Galois-cover
argument is likely classical and should be checked against the
literature before publication.

The proof depends on four standard inputs:

1. finiteness of normalization for a finite-type algebra over
   \(\mathbf C\);
2. the birational, quasi-finite form of Zariski's Main Theorem;
3. Zariski--Nagata purity of the branch locus;
4. \(\pi_1^{\mathrm{et}}(\mathbf A^2_{\mathbf C})=1\).

These theorem-level inputs are not replaced by symbolic computation.
