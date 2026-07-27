# Route A: the Pfaff derivation is necessarily non-algebraic

## Scope and outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v)
\]
with Poisson bracket
\[
\{u,v\}=-2w,\qquad
\{u,w\}=-u^2,\qquad
\{v,w\}=1+2uv
\]
and Euler derivation
\[
\mathcal E=2u\partial_u-2v\partial_v+w\partial_w.
\]
Suppose that \(P,Q\in B\) are a Darboux pair,
\[
\{P,Q\}=1,
\]
and that \(h\in B\) is the Pfaff potential characterized by
\[
\{P,h\}=-(\mathcal E+1)P,\qquad
\{Q,h\}=-\mathcal E Q. \tag{1}
\]
Put
\[
\boxed{\Delta=\{h,-\}-\mathcal E.} \tag{2}
\]

This note proves:

> **Pfaff algebraic-flow obstruction.**
> For every hypothetical Darboux pair \(P,Q\in B\), the derivation
> \(\Delta\) in (2) is not locally finite.  In particular, it is not
> the infinitesimal generator of an algebraic one-parameter torus
> action.

Thus the proposed route
\[
B^\times=\mathbf C^\times
\quad+\quad
[\operatorname{Frac}B:\mathbf C(P,Q)]<\infty
\quad\Longrightarrow\quad
\Delta\ \hbox{locally finite}
\]
cannot be justified from units and finite field degree alone.  A
stronger regularity lemma using the full Pfaff and étale structure
would still prove nonexistence; the countermodels in Section 5 do not
refute such a lemma.  On this surface, local finiteness itself would
contradict the Darboux equation.

The proof uses the uniqueness theorem for semisimple derivations on
normal affine surfaces with nontrivial Makar--Limanov invariant due to
Flenner--Zaidenberg.  It does **not** prove that no Darboux pair exists:
the surviving possibility is precisely that the forced derivation
\(\Delta\) is wild.

## 1. The Pfaff equations give an eigenfunction and an invariant

Antisymmetry in (1) gives
\[
\{h,P\}=(\mathcal E+1)P,\qquad
\{h,Q\}=\mathcal E Q.
\]
Consequently,
\[
\boxed{\Delta(P)=P,\qquad \Delta(Q)=0.} \tag{3}
\]

The Euler derivation is conformally Poisson:
\[
\mathcal E\{f,g\}
=\{\mathcal Ef,g\}+\{f,\mathcal Eg\}+\{f,g\}.
\]
Since a Hamiltonian derivation is Poisson, (2) therefore also gives
\[
\Delta\{f,g\}
=\{\Delta f,g\}+\{f,\Delta g\}-\{f,g\}. \tag{4}
\]
Equation (4) is consistent with (3) and \(\{P,Q\}=1\), but it does not
imply local finiteness.

## 2. Finite field degree kills the nilpotent Jordan part

Assume for contradiction that \(\Delta\) is locally finite.  In
characteristic zero it has commuting Jordan components
\[
\Delta=\Delta_s+\Delta_n,
\]
where \(\Delta_s\) is semisimple and \(\Delta_n\) is locally nilpotent.
This is the Jordan decomposition for locally bounded derivations in
Flenner--Zaidenberg, Lemma 2.2; on a finitely generated algebra their
terminology agrees here with local finiteness.
Because \(P\) is a \(\Delta\)-eigenvector of eigenvalue \(1\), while
\(Q\) is a \(\Delta\)-eigenvector of eigenvalue \(0\), Jordan
decomposition gives
\[
\Delta_sP=P,\quad \Delta_nP=0,\qquad
\Delta_sQ=0,\quad \Delta_nQ=0. \tag{5}
\]

Let
\[
K=\operatorname{Frac}B,\qquad K_0=\mathbf C(P,Q).
\]
The Poisson bivector is nowhere zero: its three displayed
coefficients \(-2w,-u^2,1+2uv\) cannot vanish simultaneously.
Thus it is the inverse of a nowhere-vanishing algebraic two-form, and
\(\{P,Q\}=1\) says that \(dP\wedge dQ\) is nowhere zero.  Hence
\((P,Q)\) is dominant and étale, in particular generically finite, so
\(K/K_0\) is a finite separable extension.  The extension of
\(\Delta_n\) to \(K\) kills \(K_0\).  If \(\alpha\in K\) has
separable minimal polynomial \(F(T)\in K_0[T]\), then
\[
0=\Delta_n(F(\alpha))=F'(\alpha)\Delta_n(\alpha).
\]
Thus \(\Delta_n(\alpha)=0\).  Hence
\[
\boxed{\Delta_n=0,\qquad \Delta=\Delta_s.} \tag{6}
\]

This is the one genuinely useful consequence of finite field degree:
local finiteness would force semisimplicity.  It does not establish
local finiteness in the first place.

## 3. Uniqueness of the torus action

The surface \(\operatorname{Spec}B\) is the
\(\mathrm{ML}_1\) pseudoplane \(S(2,2,1)\); in particular
\[
\operatorname{ML}(B)=\mathbf C[u]\ne\mathbf C.
\]
Here one locally nilpotent derivation is
\[
\partial_0(u)=0,\qquad \partial_0(w)=u^2,\qquad
\partial_0(v)=2w.
\]
It has kernel \(\mathbf C[u]\): after localizing at \(u\), it is
\(u^2\partial_w\) on \(\mathbf C[u,u^{-1},w]\), and its kernel
intersects \(B\) in \(\mathbf C[u]\).  Masuda--Miyanishi's
classification of affine pseudoplanes with torus actions states that
\(S(k,r,a)\), for \(k,r\ge2\), has a unique
\(\mathbf A^1\)-fibration; see also Dubouloz--Palka,
*The Jacobian Conjecture fails for pseudo-planes*, Theorem A and the
discussion preceding it, arXiv:1701.01425.  Consequently every
nonzero locally nilpotent derivation on this \(S(2,2,1)\) has the same
kernel \(\mathbf C[u]\), proving the displayed Makar--Limanov
identity.
It carries the standard hyperbolic \(\mathbf C^*\)-action with
infinitesimal generator \(\mathcal E\).  The grading is effective
because the weights \(2,-2,1\) have greatest common divisor one.

The hypersurface is smooth, hence normal: the partial derivatives of
\(w^2-u-u^2v\) cannot vanish simultaneously.  Moreover
\[
B[u^{-1}]=\mathbf C[u,u^{-1},w]
\]
has unit group \(\mathbf C^\times u^{\mathbf Z}\), and intersecting
with units regular on \(B\) leaves \(B^\times=\mathbf C^\times\).
Thus \(\operatorname{Spec}B\) is neither
\(\mathbf C^*\times\mathbf C^*\) nor
\(\mathbf A^1\times\mathbf C^*\), the two exceptions in the theorem
used next.

Flenner--Zaidenberg's uniqueness theorem
[*On the uniqueness of \(\mathbf C^*\)-actions on affine surfaces*,
Theorem 3.3, Contemp. Math. **369** (2005), 97--111;
arXiv:math/0406239]
says in this situation that every semisimple derivation is of the form
\[
\Delta=c\,\phi^{-1}\mathcal E\phi,\qquad
c\in\mathbf C,\quad \phi\in\operatorname{Aut}(B), \tag{7}
\]
where \(\phi\) may be chosen from a \(\mathbf C^+\)-subgroup.
Equation \(\Delta(P)=P\) then forces \(c\ne0\).

For completeness, automorphisms cannot destroy the Darboux equation.
The Poisson structure is the inverse of a nowhere-vanishing algebraic
two-form \(\omega\).  Since
\[
B^\times=\mathbf C^\times,
\]
every automorphism satisfies \(\phi^*\omega=\lambda\omega\) for some
\(\lambda\in\mathbf C^\times\), and hence scales the bracket by a
nonzero scalar.  (For the \(\mathbf C^+\)-conjugator in (7), the
scaling character is actually trivial.)

Put
\[
p=\phi(P),\qquad q=\phi(Q).
\]
Equations (3) and (7) imply
\[
\mathcal Ep=c^{-1}p,\qquad \mathcal Eq=0, \tag{8}
\]
while
\[
\{p,q\}\in\mathbf C^\times. \tag{9}
\]
As the \(\mathcal E\)-grading of \(B\) is integral, \(m=c^{-1}\) in
(8) is an integer.  The bracket raises standard weight by one, so (9)
forces
\[
m+0+1=0,\qquad m=-1. \tag{10}
\]

## 4. The terminal homogeneous contradiction

Put \(s=uv\).  In the reduced basis
\(u^iv^jw^\epsilon\), \(\epsilon\in\{0,1\}\), the standard weight
spaces needed in (8)--(10) are
\[
B_0=\mathbf C[s],\qquad
B_{-1}=vw\,\mathbf C[s].
\]
Therefore
\[
p=vw\,A(s),\qquad q=F(s)
\]
for polynomials \(A,F\in\mathbf C[s]\).  Direct calculation gives
\[
\boxed{\{p,q\}=s(1+s)A(s)F'(s).} \tag{11}
\]
The right side cannot be a nonzero scalar.  This contradicts (9) and
proves the Pfaff algebraic-flow obstruction.

Notice that uniqueness of the \(\mathbf C^*\)-action does not literally
force \(q\) to be a polynomial in the \(\mathbf A^1\)-fibration
coordinate \(u\).  After conjugation it forces
\(q\in B_0=\mathbf C[uv]\).  Formula (11), rather than the
\(\mathrm{ML}_1\) fibration by itself, is the final contradiction.

## 5. Affine-modification countermodels to the coarse lemma

The implications
\[
A^\times=\mathbf C^\times,\qquad
[\operatorname{Frac}A:\mathbf C(P,Q)]<\infty,\qquad
D(P)=P,\quad D(Q)=0
\]
do not force a derivation \(D\) to be locally finite, even when \(A\)
is a polynomial ring.

For any integer \(d\ge1\), take
\[
A=\mathbf C[a,z],\qquad
P=a^dz,\qquad Q=a^d(1-z)
\]
and
\[
D=\frac{az}{d}\partial_a+z(1-z)\partial_z. \tag{12}
\]
Then
\[
A^\times=\mathbf C^\times,\qquad
D(P)=P,\qquad D(Q)=0,
\]
and
\[
[\mathbf C(a,z):\mathbf C(P,Q)]=d, \tag{13}
\]
because
\[
a^d=P+Q,\qquad z=\frac{P}{P+Q}.
\]
But \(D\) is not locally finite: if a polynomial in \(z\) has degree
\(n>0\), then \(z(1-z)\partial_z\) raises its degree to \(n+1\).
In particular the degrees of \(D^k(z)\) are \(k+1\).

This family is the affine modification
\[
A\simeq
\mathbf C[P,Q,z]\big/\bigl((P+Q)z-P\bigr)
\quad(d=1)
\]
and its cyclic \(d\)-fold analogue.  Its map to the \((P,Q)\)-plane
collapses \(a=0\); indeed
\[
\operatorname{Jac}_{a,z}(P,Q)=-d\,a^{2d-1}. \tag{14}
\]
Thus it is not a Darboux/étale countermodel.  It pinpoints the missing
input: unit rigidity and finite function-field degree do not control
the vector field across a non-quasi-finite boundary modification.

The earlier Laurent Pfaff model gives the complementary warning.  There
the exact Pfaff derivation is locally finite, but the ring has
nonconstant units.  Together, the two examples show that neither the
field extension nor the unit condition can be used in isolation.

## 6. Exact logical status

What is proved:

1. the Pfaff equations canonically produce (3);
2. if the resulting \(\Delta\) were locally finite, finite field degree
   would make it semisimple;
3. uniqueness of semisimple actions on this \(\mathrm{ML}_1\) surface
   would then produce a forbidden standard homogeneous Darboux pair;
4. hence \(\Delta\) is necessarily non-locally-finite;
5. a concrete affine-modification family disproves the broader
   unit-plus-finite-degree local-finiteness principle.

What is not proved:

- no Darboux pair in \(B\) is excluded;
- no new function-field degree is excluded;
- the plane Jacobian conjecture is not resolved;
- boundary regularity does not upgrade \(\Delta\) to an algebraic flow.

The useful pivot is therefore away from algebraic-flow classification.
Any successful use of \(\Delta\) must exploit a genuinely wild
derivation invariant—most plausibly valuations of the finite
normalization or the geometry of its non-quasi-finite boundary—not
local finiteness.

## 7. Verification

Run

```sh
.venv/bin/python \
  current_context/verify_route_a_pfaff_algebraic_derivation_no_go.py
```

The verifier checks the standard-weight terminal formula (11), the
Pfaff eigen/invariant identities on the exact Laurent chart, and the
all-\(d\) affine-modification countermodel through a representative
range.  The Jordan decomposition, separability, Makar--Limanov
invariant, and Flenner--Zaidenberg uniqueness theorem are
theorem-level inputs rather than computer proofs.
