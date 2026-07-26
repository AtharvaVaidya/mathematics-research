# Route A: a cubic \(D/H\) seed and its correction complex

Date: 25 July 2026

## Outcome

On the quadratic pseudoplane
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v)
\]
with
\[
\{u,v\}=-2w,\qquad
\{u,w\}=-u^2,\qquad
\{v,w\}=1+2uv,
\]
put
\[
s=uv,\qquad
P_0=w,\qquad
Q_0=-v-2uv^2=-v(1+2s).
\tag{1}
\]

This is a canonical degree-three seed for the unbranched \(D/H\)
collision:
\[
\{P_0,Q_0\}
=1+6s+6s^2
=1+6vw^2.
\tag{2}
\]
Thus it satisfies the Darboux equation modulo \(w^2\), and satisfies it
exactly on both components
\[
D=V(u,w),\qquad H=V(1+uv,w).
\]

The correction audit has three precise conclusions.

1. Keeping \(P=w\) cannot work.  In the rational canonical coordinates
   \(r=u^{-1},w\), every solution of
   \(\{w,Q\}=1\) is
   \[
   Q=-r+F(w),
   \]
   and none belongs to \(B\).  This is an all-degree characteristic
   obstruction, not a support search.
2. Allowing both coordinates to move removes the infinitesimal
   obstruction.  In the natural weight-preserving family, the full
   linearized operator is surjective; an explicit polynomial first
   correction cancels the error in (2).
3. Nevertheless no exact polynomial solution exists in the full
   weight-preserving collision family
   \[
   P=wF(s),\qquad Q=vH(s).
   \]
   A highest-degree calculation rules it out for arbitrary polynomial
   \(F,H\).

There are exact formal Darboux corrections in the completion along
\(D\sqcup H\).  Hence the local and \(w\)-adic routes are exhausted:
the remaining issue is polynomial algebraization.  Any successful
construction—or any stronger obstruction—must mix hyperbolic weights
while controlling the extreme-weight terms.

## 1. Why this is the right degree-three seed

On the Laurent chart,
\[
\operatorname {Frac}B=\mathbf C(s,w),\qquad
v=\frac{s(1+s)}{w^2}.
\]
Set
\[
A(s)=s(1+s)(1+2s).
\]
Then
\[
Q_0=-\frac{A(s)}{w^2}.
\tag{3}
\]
The target field \(\mathbf C(w,Q_0)\) has degree three in
\(\mathbf C(s,w)\), because \(s\) satisfies
\[
A(s)+Q_0w^2=0.
\]

At \(w=0\), the three simple roots are
\[
s=0,\qquad s=-1,\qquad s=-\frac12.
\]
They are respectively the retained divisor \(D\), the retained divisor
\(H\), and a boundary prime omitted from \(S\).  Since
\[
A'(0)=A'(-1)=1,\qquad A'(-1/2)=-1/2,
\]
all three primes are generically unramified.

The bracket in the \((s,w)\)-chart is
\[
\{R,T\}
=w^2(R_sT_w-R_wT_s).
\tag{4}
\]
Equations (2)--(3) follow immediately:
\[
\{w,Q_0\}=A'(s)=1+6s+6s^2.
\]
The relation
\[
s(1+s)=vw^2
\tag{5}
\]
shows that the error is second order along \(D\sqcup H\).

## 2. Exact characteristic obstruction with \(P=w\)

On \(u\ne0\), put \(r=u^{-1}\).  Then
\[
B[u^{-1}]=\mathbf C[r,r^{-1},w],\qquad
\{r,w\}=1.
\]
Consequently
\[
\{w,-\}=-\partial_r.
\tag{6}
\]
Every rational solution of
\[
\{w,Q\}=1
\tag{7}
\]
has the form
\[
Q=-r+F(w),\qquad F(w)\in\mathbf C(w).
\tag{8}
\]

If \(Q\in B\), then \(Q+r\) belongs both to
\(\mathbf C[r,r^{-1},w]\) and to \(\mathbf C(w)\), so
\[
F(w)\in\mathbf C[w].
\]
But \(-r+F(w)\) has a pole along \(D\): \(r=u^{-1}\) has valuation
\(-2\), while a polynomial in \(w\) has nonnegative \(D\)-valuation.
Thus (8) never lies in \(B\).

For the seed (1), the correction \(R\) with \(Q=Q_0+R\) would have to
satisfy
\[
\{w,R\}=-6s(1+s).
\]
Using (4), a rational antiderivative is
\[
R=\frac{3s^2+2s^3}{w^2}+F(w).
\]
It has exactly the pole predicted by (8).  Therefore no correction of
\(Q_0\) alone can terminate in \(B\).

## 3. Exact formal correction and why it does not algebraize

The quotient
\[
B/(w)\simeq
\mathbf C[v]\times\mathbf C[u,u^{-1}]
\]
is disconnected, so the \(w\)-adic completion splits as the product of
the formal neighborhoods of \(D\) and \(H\).  Equation (7) has a regular
formal solution on each factor.

The relation
\[
w^2r^2-r-v=0
\]
gives the two expansions
\[
r_\pm=\frac{1\pm\sqrt{1+4vw^2}}{2w^2}.
\]
On the \(D\)-factor one uses
\[
Q_D=w^{-2}-r_+
=\frac{1-\sqrt{1+4vw^2}}{2w^2}
=-v+v^2w^2-2v^3w^4+\cdots,
\tag{9}
\]
while on the \(H\)-factor one uses
\[
Q_H=-r_-
=\frac{\sqrt{1+4vw^2}-1}{2w^2}
=v-v^2w^2+2v^3w^4-\cdots.
\tag{10}
\]
Both satisfy \(\{w,Q_\bullet\}=1\).

The two different invariant constants in (9)--(10), namely \(w^{-2}\)
and \(0\) in the representation (8), cannot come from one rational
function on the connected surface.  The formal idempotents separating
the two factors are infinite binomial series.  This is the precise
formal-versus-polynomial gap.

The seed \(Q_0\) is the simplest polynomial interpolation of the signs:
\[
Q_0|_D=-v,\qquad Q_0|_H=v.
\]
Its finite error (2) is therefore an algebraization error, not a local
symplectic error.

## 4. The two-coordinate linearized operator

Give \(B\) the hyperbolic grading
\[
\operatorname {wt}(u)=2,\qquad
\operatorname {wt}(v)=-2,\qquad
\operatorname {wt}(w)=1.
\]
The natural weight-preserving collision perturbations are
\[
P_\varepsilon=w(1+\varepsilon f(s)),\qquad
Q_\varepsilon
=-v(1+2s)+\varepsilon v h(s),
\tag{11}
\]
with \(f,h\in\mathbf C[s]\).

Let
\[
B_0(s)=s(1+s),\qquad A(s)=B_0(s)(1+2s).
\]
The coefficient of \(\varepsilon\) in the bracket is
\[
\boxed{
\mathcal L(f,h)
=2A f'+A'f-\bigl(B_0h\bigr)'.
}
\tag{12}
\]
Thus the first correction equation for the seed error
\[
e=A'-1=6s(1+s)
\]
is
\[
\mathcal L(f,h)=-e.
\tag{13}
\]

The operator in (12) has no cokernel.  Indeed, define
\[
\ell(k)=\int_{-1}^{0}k(s)\,ds.
\]
The map
\[
h\longmapsto(B_0h)'
\]
has image exactly \(\ker\ell\): a primitive is divisible by
\(s(1+s)\) precisely when it vanishes at both endpoints.  On the other
hand,
\[
\ell\!\left(2A(s^2)'+A's^2\right)
=-\int_{-1}^{0}A'(s)s^2\,ds
=-\frac1{30}\ne0.
\]
Therefore the \(f\)-term supplies the missing one-dimensional quotient,
and \(\mathcal L\) is surjective.

An explicit solution of (13) is
\[
\begin{aligned}
f(s)&=-\frac{84}{5}+\frac{102}{5}s-30s^2,\\
h(s)&=-\frac{84}{5}-84s^3.
\end{aligned}
\tag{14}
\]
This proves that moving both coordinates removes the first-order
obstruction.  Substituting \(\varepsilon=1\) does not solve the nonlinear
problem: the quadratic bracket of the two corrections is a nonzero
degree-six polynomial.  Thus a Newton scheme begins, but it does not
terminate at its first step.

For comparison, fixing either coordinate exposes a genuine
one-dimensional cokernel.  The second term of (12) alone misses the
functional \(\ell\), while fixing \(P=w\) is ruled out globally by the
characteristic calculation (6)--(8).

## 5. All-degree obstruction in the invariant collision family

Consider the entire polynomial family
\[
P=wF(s),\qquad Q=vH(s)
=\frac{B_0(s)H(s)}{w^2},
\tag{15}
\]
where \(F,H\in\mathbf C[s]\).  It allows both coordinates to vary, keeps
\(D\) and \(H\) over the target collision line whenever
\[
F(0)F(-1)H(0)H(-1)\ne0,
\]
and includes the seed (1).

Put
\[
C(s)=B_0(s)H(s).
\]
Formula (4) gives the exact bracket
\[
\{P,Q\}=-2CF'-C'F.
\tag{16}
\]
Suppose \(\deg F=n\) and \(\deg H=m\), with nonzero leading
coefficients \(f_n,h_m\).  Since \(\deg C=m+2\), the highest term in
(16) has degree \(m+n+1\) and coefficient
\[
-\bigl(2n+m+2\bigr)f_nh_m.
\tag{17}
\]
It is nonzero in characteristic zero.  Hence (16) cannot be the
constant \(1\).  The cases \(F=0\) or \(H=0\) are also impossible.

Therefore:

> **Invariant-family no-go.** No polynomial Darboux pair of the form
> \(P=wF(uv),\ Q=vH(uv)\) exists, at any degrees.

This is a nonlinear all-degree obstruction.  It also explains why the
surjective linearized equation does not imply polynomial termination:
the top degree generated by a correction cannot disappear inside the
same invariant family.

## 6. Full linearization and the remaining route

For arbitrary rational perturbations \(p,q\), the linearization at the
seed is, in the \((s,w)\)-chart,
\[
\boxed{
L(p,q)
=A'(s)\,\partial_wp
+\frac{2A(s)}w\,\partial_sp
-w^2\partial_sq.
}
\tag{18}
\]
Its characteristics are the Hamiltonian trajectories of \(Q_0\)
together with the transverse Hamiltonian field of \(w\).

The weight-preserving part of (18) is surjective, and the \(w\)-adic
completion has exact Darboux solutions.  Consequently neither an
infinitesimal cokernel nor a formal-neighborhood obstruction can finish
Route A.

The remaining promising direction is an **extreme-weight termination
theorem**: prove that every finite mixed-weight correction has a top or
bottom weight pair whose bracket cannot be canceled, while allowing
the lower weights to perform the surjective correction (12).  Such a
theorem would extend (17) beyond the invariant family.  Conversely, a
construction would have to use at least two additional hyperbolic
weights and arrange cancellation of all extreme brackets.

## Scope

This note does not construct a Darboux pair and does not exclude all
mixed-weight perturbations.  It rigorously closes:

1. corrections with \(P=w\);
2. all formal/local obstructions along \(D\sqcup H\);
3. the entire two-coordinate invariant family (15).

The companion verifier checks all displayed identities, the exact
degree-three seed, the explicit linearized correction, and the
highest-degree obstruction.
