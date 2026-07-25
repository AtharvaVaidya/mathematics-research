# First structural obstructions on the cubic pseudo-plane

Date: 24 July 2026

Let
\[
B_3=\mathbf C[u,v,w]/(w^3-u-u^2v)
\]
with
\[
\{u,w\}=-u^2,\qquad
\{u,v\}=-3w^2,\qquad
\{v,w\}=1+2uv.
\]
The cubic pseudo-plane bridge reduces a plane counterexample to finding
\(\{P,Q\}=1\) in \(B_3\).  Three tempting first attempts are now excluded
without a bounded search.

## 1. The Hamiltonian \(v\) has no rational slice

Put
\[
s=1+2uv.
\]
Then
\[
s^2=1+4vw^3.
\]
For the Hamiltonian derivation \(\delta=\{v,-\}\),
\[
\delta w=s,\qquad \delta s=6vw^2.
\]
Over \(K=\mathbf C(v)\), this is the vector field on the smooth elliptic
curve
\[
E/K:\quad s^2=1+4vw^3.
\]
If \(\delta Q=1\) for a rational \(Q\), then
\[
dQ=\frac{dw}{s}.
\]
The right side is a nonzero holomorphic differential on the smooth
projective model of \(E\).  It cannot be the differential of a rational
function: a pole of a rational function produces a pole in its differential,
whereas a pole-free rational function is constant.  Hence
\[
\boxed{\{v,Q\}\ne1\quad\text{for every }Q\in\operatorname{Frac}(B_3).}
\]

## 2. The Hamiltonian \(w\) has a rational slice but no regular one

Put \(r=uv\).  For \(\partial=\{w,-\}\),
\[
\partial r=-u(1+r)=-w^3.
\]
Over \(\mathbf C(w)\), the function field is \(\mathbf C(w)(r)\), so every
rational solution of \(\partial Q=1\) is
\[
Q=-\frac r{w^3}+C(w),\qquad C(w)\in\mathbf C(w).
\tag{1}
\]

The fiber \(w=0\) has two components:
\[
D_0:(u,w)=(0,0),\qquad
D_1:w=0,\ 1+uv=0.
\]
The first term in (1) is regular along \(D_0\) and has principal part
\(w^{-3}\) along \(D_1\).  Canceling that pole forces
\[
C(w)=-w^{-3}+O(1),
\]
after which
\[
-\frac{uv}{w^3}-\frac1{w^3}
=-\frac1u
\]
has a pole along \(D_0\).  Lower negative powers of \(w\) would introduce
poles on both components.  Therefore
\[
\boxed{\{w,Q\}\ne1\quad\text{for every }Q\in B_3.}
\]

## 3. The characteristic-two seed does not lift even once

Modulo \(2\),
\[
\{v,w\}=1.
\]
This suggests the seed
\[
P=v+2A,\qquad Q=w+2B.
\]
For a lift modulo \(4\), one would need
\[
\{A,w\}+\{v,B\}=uv
\quad\text{in }B_3\otimes\mathbf F_2.
\tag{2}
\]

Use the unique reduced monomial basis
\[
u^iv^jw^k,\qquad k=0,1,2.
\]
In characteristic two,
\[
D_w:=\{- ,w\}=u^2\partial_u+\partial_v,
\qquad
D_v:=\{v,-\}=w^2\partial_u+\partial_w.
\]
The coefficient of \(uv\) in \(D_w(u^iv^jw^k)\) is always zero:
the two possible sources have coefficients \(i=0\) and \(j=2=0\).
For \(D_v\), only \(k=1\) can reduce to \(w\)-degree zero, and
\[
D_v(u^iv^jw)
=(i+1)u^iv^j+i\,u^{i+1}v^{j+1}.
\]
Its \(uv\)-coefficient also vanishes.  The cases \(k=0,2\) retain positive
\(w\)-degree.  Thus the linear functional \([uv]\) annihilates the entire
left side of (2) but takes value one on its right side.

Consequently
\[
\boxed{
(v,w)\text{ is a Darboux pair mod }2
\text{ with no lift mod }4.
}
\]
This is an all-degree first-Hensel obstruction, not a finite support search.

## Strategic consequence

The cubic pseudo-plane route remains a direct counterexample architecture,
but its three most natural seeds are closed:

- the exact Kummer pair does not descend;
- neither generator \(v\) nor \(w\) can be one coordinate of a regular
  Darboux pair;
- the simplest Frobenius seed dies at the first \(2\)-adic lift.

The next search should therefore classify boundary-normalized Hamiltonians
\[
P=v+\text{(terms of transverse order at least one)}
\]
whose generic fibers cease to carry the elliptic differential above.
That is a deformation-of-fibration problem, not a sparse coefficient sweep.

## 4. Two infinite transverse deformation families are also closed

The elliptic obstruction survives substantially more than the undeformed
Hamiltonian \(v\).

### 4.1 Graph deformations \(P=v+f(w)\)

Let \(f\in\mathbf C[w]\) and
\[
P=v+f(w).
\]
On the generic fiber \(P=T\), put again \(s=1+2uv\).  Since
\(\{P,w\}=s\), the function field of the fiber is
\[
s^2=1+4\bigl(T-f(w)\bigr)w^3.
\tag{3}
\]
The polynomial on the right is squarefree over \(\mathbf C(T)\).  Indeed,
a common zero with its \(w\)-derivative would imply
\[
T=f(w)-\frac1{4w^3},
\qquad
3+4w^4f'(w)=0.
\]
The second equation makes \(w\) algebraic over \(\mathbf C\), after which
the first would make the transcendental \(T\) constant.

If \(f\) is constant, the right side of (3) has degree three.  If
\(\deg f=d\ge1\), it has degree \(d+3\ge4\).  Thus its smooth projective
hyperelliptic model has positive genus, and
\[
\eta=\frac{dw}{s}
\]
is a nonzero holomorphic differential.  At a finite branch point this is
the usual regular differential; at infinity its order is \(n-3\) in the
odd-degree case and \(n/2-2\) in the even-degree case, where
\(n=\deg_w(1+4(T-f)w^3)\).

If \(\{P,Q\}=1\), restriction to the generic fiber would give
\(dQ=\eta\), which is impossible for a rational function.  Hence
\[
\boxed{
\{v+f(w),Q\}\ne1
\quad\text{for all }f\in\mathbf C[w],\
Q\in\operatorname{Frac}(B_3).
}
\tag{4}
\]
The same conclusion holds for \(av+f(w)\), \(a\ne0\), after scaling.

### 4.2 First transverse shears \(P=v+wA(v)\)

There is a complementary deformation that is not a graph over \(w\):
\[
P=v+wA(v),\qquad A\in\mathbf C[v].
\]
The case \(A=0\) is Section 1.  Suppose \(A\ne0\), put \(P=T\), and use
\(v\) as the base parameter.  Then
\[
w=\frac{T-v}{A(v)}
\]
and the quadratic discriminant coordinate \(s=1+2uv\) obeys
\[
s^2=1+\frac{4v(T-v)^3}{A(v)^3}.
\]
After setting \(Y=A(v)^2s\), the smooth normalization is the double cover
\[
Y^2=H_T(v):=
A(v)\left(A(v)^3+4v(T-v)^3\right).
\tag{5}
\]
Moreover
\[
\{P,v\}=-A(v)s,
\]
so a rational slice would force
\[
dQ=-\frac{dv}{A(v)s}
=-\frac{A(v)\,dv}{Y}.
\tag{6}
\]

The second factor
\[
N_T(v)=A(v)^3+4v(T-v)^3
\]
is squarefree in \(\mathbf C(T)[v]\).  If an irreducible
\(v\)-dependent factor occurred twice, it would divide
\[
\partial_TN_T=12v(T-v)^2.
\]
The factor \(v\) has multiplicity exactly one when it occurs, and
\(T-v\) does not divide \(N_T\), since \(N_T(v,v)=A(v)^3\ne0\).

Formula (6) is holomorphic on the normalization of (5), including when
\(A\) has repeated roots:

- at a nonzero root of \(A\) of multiplicity \(m\), the vanishing order
  of \(H_T\) is \(m\);
- if \(A\) has order \(m\) at zero, the order of \(H_T\) is \(m+1\);
- every root of \(N_T\) away from \(A=0\) is simple.

The standard ramified/unramified local parameter calculation gives
nonnegative order for \(A\,dv/Y\) in every case.  At infinity, if
\(d=\deg A\), then
\[
\deg H_T=
\begin{cases}
4,&d=0,\\
5,&d=1,\\
4d,&d\ge2,
\end{cases}
\]
and the order of \(A\,dv/Y\) is respectively \(0,0,d-2\).
It is therefore a nonzero global holomorphic differential.  It cannot be
exact rationally, and
\[
\boxed{
\{v+wA(v),Q\}\ne1
\quad\text{for all }A\in\mathbf C[v],\
Q\in\operatorname{Frac}(B_3).
}
\tag{7}
\]

These two theorems close both natural one-variable transverse directions
out of \(v\).  Any viable boundary-normalized Hamiltonian must mix \(v\)
and \(w\) in a genuinely two-variable way beyond
\(v+f(w)\) and \(v+wA(v)\).
