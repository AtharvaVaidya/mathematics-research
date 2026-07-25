# The minimal residual factor: a unique submersion and no Hamiltonian mate

Date: 25 July 2026

Work over an algebraically closed field \(k\) of characteristic zero.  In
the normalization \(k[t,c]\) of the fixed-source ring, put
\[
v=3ct-2,\qquad D=v^2-9c,\qquad U_0=Dv.
\]
The identity
\[
U_0=9bc-27ac^2-8
\]
shows that \(U_0\) belongs to the fixed-source ring
\[
R=k[a,b,c]\subset k[t,c].
\]
Its restriction data are the smallest residual pattern singled out by
the oddness theorem in Section 1.15 of `FIXED_SOURCE_PLANE_ROUTE.md`.

## 1. The smallest residual factor is not a submersion

Direct differentiation gives
\[
\begin{aligned}
(U_0)_t&=9c(v^2-3c),\\
(U_0)_c&=9\bigl(t(v^2-3c)-v\bigr).
\end{aligned}
\tag{1}
\]
If \(c\ne0\), the first equation in the critical-point system forces
\(v^2=3c\), while the second then forces \(v=0\), a contradiction.
If \(c=0\), then \(v=-2\), and the second equation gives
\(t=-1/2\).  Thus
\[
\operatorname {Crit}(U_0)=\{(-1/2,0)\},\qquad U_0(-1/2,0)=-8.
\tag{2}
\]
The Hessian at this point is
\[
\begin{pmatrix}0&36\\36&0\end{pmatrix},
\]
so the critical point is nondegenerate.  In particular \(U_0\) cannot
be one component of a Keller pair.

## 2. Classification of the natural one-variable perturbation family

Consider the full family
\[
U=f(c)+g(c)Dv,\qquad f,g\in k[c],\quad g\ne0.
\tag{3}
\]
This includes multiplication of the residual factor by \(g(c)\) and a
target-ring perturbation by \(f(c)\).  The family retains the paired
conductor behavior: on \(D=0\), \(U=f(c)\), while the transverse
residual term restricts to the required odd factor.

Set
\[
A=f'(c),\qquad B=6cg'(c)+9g(c).
\]
On the locus \(v^2=3c\), where the \(t\)-derivative of \(Dv\) vanishes,
\[
U_c=A-vB.
\tag{4}
\]
Consequently a submersion must have
\[
E(c):=A(c)^2-3cB(c)^2
\tag{5}
\]
with no nonzero root.

This necessary condition is already rigid enough to classify the
submersions.  Since \(k\) is algebraically closed, a polynomial with no
root in \(k^\times\) is a monomial.  Here \(E\) cannot vanish
identically: after adjoining \(s\) with \(c=s^2\), either factor below
would otherwise vanish, and its even and odd parts would give
\(A=B=0\), contrary to \(g\ne0\).  Thus \(E=\kappa c^N\) with
\(\kappa\ne0\).  Substitute
\(c=s^2\) and factor:
\[
E(s^2)=
\bigl(A(s^2)+\sqrt3\,sB(s^2)\bigr)
\bigl(A(s^2)-\sqrt3\,sB(s^2)\bigr)
=\kappa s^{2N}.
\tag{6}
\]
Both factors are nonzero.  Since \(k[s]\) is a UFD and their product has
no irreducible factor other than \(s\), each factor must be a monomial.
The two factors are exchanged by \(s\mapsto-s\); taking their even and
odd parts shows that an even monomial forces \(B=0\), while an odd
monomial forces \(A=0\).  The first alternative would give
\(6cg'+9g=0\), which has no nonzero polynomial solution.  Thus \(f\) is
constant.  Moreover \(B\), and hence \(g\), is a monomial, because the
operator
\[
g\longmapsto6cg'+9g
\]
acts diagonally with nonzero eigenvalues on the monomial basis of
\(k[c]\).

Writing \(g=\lambda c^q\), the line \(c=0\) finishes the classification:

* \(q=0\) leaves the critical point in (2);
* \(q\ge2\) makes the whole line \(c=0\) critical;
* \(q=1\) is a submersion.

For the last assertion, put
\[
W=cDv.
\tag{7}
\]
Then
\[
W_t=9c^2(v^2-3c).
\]
Away from \(c=0\), a critical point would have \(v^2=3c\), but there
\[
W_c=-15cv\ne0.
\]
On \(c=0\), one has \(W_c=-8\).  We have proved:

> **Residual-family classification.**  The submersions in (3) are
> exactly
> \[
> U=\mu+\lambda cDv,\qquad \mu\in k,\quad\lambda\in k^\times.
> \tag{8}
> \]

Thus multiplying by \(c\) is not merely the first repair of \(U_0\);
within the entire family (3), it is the unique repair up to affine
rescaling.

## 3. The unique submersion has no polynomial Hamiltonian mate

Although \(W=cDv\) is a polynomial submersion, there is no
\(V\in k[t,c]\) for which
\[
\{W,V\}_{t,c}\in k^\times.
\tag{9}
\]
In fact the following stronger centralizer statement holds:
\[
\ker\{W,-\}=k[W].
\tag{10}
\]

Write
\[
V=\sum_{i=0}^n f_i(c)t^i,\qquad f_n\ne0.
\]
The leading \(t\)-terms are
\[
W=27c^4t^3+\text{lower \(t\)-degree},\quad
W_t=81c^4t^2+\cdots,\quad
W_c=108c^3t^3+\cdots.
\]
If \(\{W,V\}\) is constant (including the zero constant), the
coefficient of \(t^{n+2}\) for \(n>0\) must vanish:
\[
27c^3\bigl(3cf_n'-4nf_n\bigr)=0.
\tag{11}
\]
Coefficient comparison in \(k[c]\) says that \(3\mid n\), say
\(n=3m\), and
\[
f_n=\alpha c^{4m}.
\tag{12}
\]
Since the leading \(t\)-term of \(W^m\) is
\(27^m c^{4m}t^{3m}\), subtracting
\(\alpha 27^{-m}W^m\) from \(V\) preserves its bracket with \(W\) and
strictly lowers its \(t\)-degree.  Descending induction reduces \(V\)
modulo \(k[W]\) to a polynomial \(q(c)\).

Finally
\[
\{W,q(c)\}=W_tq'(c)
=9c^2(v^2-3c)q'(c).
\tag{13}
\]
This vanishes only when \(q\) is constant and can never be a nonzero
constant.  Equations (10) and (9) follow.

The same conclusion holds for every affine rescaling in (8).  Hence the
smallest odd residual divisor yields a sharp near miss:

* \(Dv\) descends but has one Morse critical point;
* its unique one-variable submersion repair is \(cDv\);
* that repair has no polynomial Hamiltonian mate even in the full
  normalization \(k[t,c]\), and therefore none in \(R\).

This is an exact obstruction for the natural residual-factor
construction.  It is not a proof that arbitrary Hamiltonians in \(R\)
have no mate, and it does not produce a plane counterexample.

The identities used above are checked in
`verify_fixed_plane_residual_hamiltonian.py`.
