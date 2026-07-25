# Global Darboux audit on the quadratic pseudoplane

## Outcome

Let

\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v)
\]

with

\[
\{u,v\}=-2w,\qquad
\{u,w\}=-u^2,\qquad
\{v,w\}=1+2uv.
\]

No global Darboux pair \(\{P,Q\}=1\) was constructed, and this note does
not resolve the plane Jacobian Conjecture.

It does give three all-degree restrictions on any hypothetical pair:

1. its Pfaff potential cannot be homogeneous of weight \(-1\);
2. neither Hamiltonian derivation can be locally finite, hence neither can
   come from an algebraic one-parameter flow;
3. its étale map \(e=(P,Q):S\to\mathbf A^2\) must identify the distinguished
   affine line \(D=(u,w)\) with at least one additional source divisor.

The first theorem closes the natural weight-eigenvector strategy
completely.  An exact Laurent-cylinder countermodel shows why the missing
step—homogenizing the Pfaff potential by target symplectic changes—cannot
be obtained formally from the Pfaff equations alone.

## 1. Generic fibers and the Pfaff system

Put

\[
s=uv,\qquad
\operatorname{Frac}(B)=\mathbf C(s,w),\qquad
\{s,w\}=w^2.
\]

Equivalently, on \(u\ne0\), put \(r=u^{-1}\).  Then

\[
B[u^{-1}]=\mathbf C[r,r^{-1},w],\qquad
v=r^2w^2-r,\qquad
\{r,w\}=1.
\]

The global symplectic form has the homogeneous primitive

\[
\beta=w\,dr+2r\,dw.
\]

For a Darboux pair, \(H^1_{\mathrm{dR}}(B)=0\) gives a polynomial \(h\)
such that

\[
\beta=P\,dQ+dh.
\]

With

\[
\mathcal E=2u\partial_u-2v\partial_v+w\partial_w
          =-2r\partial_r+w\partial_w,
\]

contraction gives

\[
\{P,h\}=-(\mathcal E+1)P,\qquad
\{Q,h\}=-\mathcal E Q. \tag{Pf}
\]

On the generic fiber of \(P\), the equality \(\{P,Q\}=1\) says that the
forced differential \(\eta_P\), characterized by

\[
\eta_P(D_P)=1,
\]

is exactly \(dQ\).  Hence it must have zero residues and zero periods and
its primitive must extend regularly across the affine fiber.  This is the
common geometric source of the earlier residue, holomorphic-differential,
and one-pole obstructions.

It is not by itself a universal contradiction.  A punctured curve can
carry an exact zero-free differential when every zero and pole of its
primitive lies at the deleted boundary.  Likewise, a smooth morphism to
\(\mathbf A^1\) need not be an \(\mathbf A^1\)-bundle: already
\(x+x^2y:\mathbf A^2\to\mathbf A^1\) is critical-point-free but has
generic fiber \(\mathbf G_m\).  Any global proof must control the boundary,
not merely smoothness of \(P\).

## 2. Complete classification when \(h\) has weight \(-1\)

Give \(B\) the hyperbolic grading

\[
\operatorname{wt}(u)=2,\qquad
\operatorname{wt}(v)=-2,\qquad
\operatorname{wt}(w)=1.
\]

Every weight-\(-1\) element is

\[
h=vwH(s)=\frac{A(s)}w,\qquad
A(s)=s(1+s)H(s).
\]

Assume first that \(A\ne0\).  In the function field, every homogeneous
element of weight \(i\) has the form

\[
f=w^iF(s).
\]

Since \(h\) has weight \(-1\), the Pfaff equations preserve each weight.
For the weight-\(i\) pieces \(P_i=w^iF_i(s)\) and
\(Q_i=w^iG_i(s)\), they become

\[
\begin{aligned}
A F_i'+iA'F_i&=(i+1)F_i,\\
A G_i'+iA'G_i&=iG_i. \tag{1}
\end{aligned}
\]

Work in a differential extension containing a nonzero solution

\[
\frac{R'}R=\frac1A
\]

and put

\[
Y=\frac{wR}{A}.
\]

Every solution of (1) is a scalar multiple of

\[
F_i=A^{-i}R^{i+1},\qquad
G_i=A^{-i}R^i.
\]

Consequently, for finite Laurent polynomials \(p,q\),

\[
P=R\,p(Y),\qquad Q=q(Y).
\]

Direct calculation gives

\[
\{R,Y\}=Y^2
\]

and therefore

\[
1=\{P,Q\}=Y^2p(Y)q'(Y). \tag{2}
\]

In the Laurent UFD \(\mathbf C[Y,Y^{-1}]\), equation (2) forces both
\(p\) and \(q'\) to be units.  Thus

\[
p=aY^m,\qquad
q=bY^{-m-1}+c.
\]

The logarithmic exceptional exponent \(m=-1\) cannot occur because a
Laurent polynomial has no logarithmic primitive.  Hence, after deleting
the irrelevant constant \(c\), \(P,Q\) are homogeneous and their weights
sum to \(-1\).

The existing homogeneous theorem for this pseudoplane then gives a
contradiction.  It reduces the only possible weights to \(1,-2\), where
the polynomial equation

\[
\left[s(1+s)a(s)^2b(s)\right]'=-a(s)
\]

has incompatible degrees in characteristic zero.

If \(h=0\), (Pf) instead forces \(P\) to have weight \(-1\) and \(Q\)
weight zero.  Write

\[
P=\frac{s(1+s)C(s)}w,\qquad Q=G(s).
\]

Then \(\{P,Q\}=s(1+s)C(s)G'(s)\), which cannot equal \(1\).

We have proved:

> **Weight-\(-1\) Pfaff obstruction.** No Darboux pair in \(B\) has a
> Pfaff potential homogeneous of weight \(-1\).

This is an all-degree classification of the finite-weight eigenvectors,
not a bounded support calculation.

## 3. Why Pfaff homogenization is not formal

The preceding theorem would solve the pseudoplane route if every Pfaff
potential could be made weight \(-1\) by a polynomial symplectic change
of target coordinates.  The following exact countermodel on the Laurent
chart shows that this reduction does not follow from (Pf).

In

\[
L=\mathbf C[r,r^{-1},w],\qquad \{r,w\}=1,
\]

put

\[
P=r^2,\qquad
Q=\frac{w}{2r}+\frac r2.
\]

Then

\[
\{P,Q\}=1
\]

and

\[
\beta=P\,dQ+dh,\qquad
h=\frac32rw-\frac16r^3.
\]

Thus \(h\) has weights \(-1\) and \(-6\).

This pair defines a quadratic field extension over
\(\mathbf C(P,Q)\), with involution

\[
\sigma(r,w)=(-r,-w-2r^2).
\]

If a polynomial target symplectomorphism made the new potential
homogeneous of weight \(-1\), its difference from \(h\) would lie in
\(\mathbf C(P,Q)\), hence be \(\sigma\)-invariant.

Every homogeneous Laurent polynomial of weight \(-1\) is

\[
H=rwF(rw^2).
\]

The equation

\[
H-\sigma H=h-\sigma h=-\frac{10}{3}r^3
\]

has the unique solution

\[
H=\frac53rw.
\]

For completeness, uniqueness follows from the highest \(w\)-degree.  If
\(\deg F=N\) is odd, the highest terms of \(H\) and \(\sigma H\) have
opposite signs.  If \(N\) is positive and even, their highest terms agree
but the next \(w\)-coefficient is nonzero and cannot be cancelled by
lower terms.  The constant case gives the displayed solution.

The required target Liouville primitive would therefore be

\[
K=h-H=-\frac13PQ.
\]

Let a polynomial symplectomorphism be \((X,Y)\mapsto(F,G)\).  If

\[
F\,dG-X\,dY=d(cXY),
\]

then comparison of coefficients gives

\[
FG_X=cY,\qquad FG_Y=(1+c)X
\]

and hence

\[
(1+c)XG_X-cYG_Y=0.
\]

For \(c=-1/3\), this is

\[
2XG_X+YG_Y=0.
\]

Every nonconstant polynomial monomial has positive \((2,1)\)-weight, so
\(G\) would be constant, contradicting the preceding equations.

Therefore no polynomial target symplectomorphism homogenizes this
potential.  The countermodel does not lie in the filled ring \(B\), so it
does not refute a theorem using boundary regularity.  It does refute any
argument based only on (Pf), extreme weights, and target symplectic
changes.

## 4. Algebraic-flow obstruction

The surface \(S=\operatorname{Spec}B\) is the classical pseudoplane
\(S(2,2,1)\), with

\[
\pi_1(S)=\mathbf Z/2.
\]

Suppose a locally nilpotent derivation \(\delta\) on \(B\) had a slice
\(q\), so \(\delta q=1\).  The slice theorem gives

\[
B=(\ker\delta)[q].
\]

Thus \(S\) would be a cylinder \(C\times\mathbf A^1\) over a smooth affine
curve.  Its topological fundamental group would be the free, hence
torsion-free, group \(\pi_1(C)\), contradicting
\(\pi_1(S)=\mathbf Z/2\).

More generally, let \(\delta\) be locally finite.  In characteristic zero
its commuting Jordan components are

\[
\delta=\delta_s+\delta_n
\]

with \(\delta_s\) semisimple and \(\delta_n\) locally nilpotent.  If
\(\delta q=1\), decompose \(q\) into \(\delta_s\)-weight spaces.
On every nonzero weight, \(\lambda+\delta_n\) is invertible because
\(\delta_n\) is nilpotent on the finite-dimensional orbit.  Hence only
the weight-zero part \(q_0\) remains and

\[
\delta_nq_0=1.
\]

This is the prohibited locally nilpotent slice.

For a Darboux pair,

\[
D_PQ=1,\qquad D_QP=-1.
\]

Consequently:

> **Wild-flow theorem.** Neither \(D_P\) nor \(D_Q\) can be locally
> finite.  In particular neither Hamiltonian belongs to a
> \(\mathbf G_a\)- or \(\mathbf G_m\)-integrable algebraic flow.

This closes every LND, semisimple, and locally finite Hamiltonian route at
once.  It also explains why the unique \(\mathbf A^1\)-fibration does not
produce a pair.  Its standard locally nilpotent derivation is

\[
D_u=-2w\partial_v-u^2\partial_w,
\]

but its quotient has the double fiber \(u=0\), so it has no global slice.

The Laurent cylinder again supplies the necessary warning: for
\(P=r+w,\ Q=w\), both Hamiltonian derivations have slices but are not
locally finite.  Thus “has a slice” cannot be upgraded to LND without
using the pseudoplane topology.

## 5. Class group and a mandatory collision divisor

Let

\[
D=V(u,w)\simeq\mathbf A^1_v.
\]

Localizing at \(u\) gives the UFD

\[
B[u^{-1}]=\mathbf C[u,u^{-1},w].
\]

The only height-one prime above \(u\) is \(D\), and

\[
\operatorname{div}(u)=2D.
\]

Nagata's theorem therefore says that \(\operatorname{Cl}(B)\) is generated
by \([D]\) with \(2[D]=0\).

The class is nonzero.  If \(D=\operatorname{div}(f)\), then, since
\(B^\times=\mathbf C^\times\), one would have \(f^2=cu\).  In the Laurent
UFD this says that a square equals \(cr^{-1}\), impossible by parity of
the \(r\)-valuation.  Hence

\[
\boxed{\operatorname{Cl}(B)\simeq\mathbf Z/2,\quad [D]\ne0.}
\]

Now let

\[
e=(P,Q):S\longrightarrow\mathbf A^2
\]

be any étale morphism; a Darboux pair is a special case.  The restriction
to \(D\) is an immersion, because \(de\) is an isomorphism on tangent
spaces.  Its image has an irreducible curve closure \(\Gamma\), say
\(\Gamma=V(F)\).

At the generic point of \(D\), étaleness gives ramification index one, so

\[
\operatorname{div}(F(P,Q))=D+E
\]

for an effective divisor \(E\) not containing \(D\).  Since the left side
is principal,

\[
[E]=-[D]=[D]\ne0.
\]

Thus \(E\) is nonempty.  Every component of \(E\) maps dominantly to
\(\Gamma\), because an étale morphism has finite fibers.

In fact, \(D\to\Gamma\) is the normalization.  The normalization is an
affine rational curve dominated by \(\mathbf A^1\), hence it is
\(\mathbf A^1\); it cannot be \(\mathbf G_m\), since every morphism
\(\mathbf A^1\to\mathbf G_m\) is constant.  The induced polynomial
\(\mathbf A^1\to\mathbf A^1\) has nowhere-zero derivative because
\(e|_D\) is immersive, so it is affine linear.

We conclude:

> **Mandatory collision theorem.** For every étale
> \(e:S\to\mathbf A^2\), the plane curve \(e(D)\) has at least two
> distinct source-divisor components above it.  The component \(D\)
> maps birationally onto its image, while at least one additional
> component dominates the same curve.

This is an all-degree global restriction on a hypothetical Darboux pair.
It proves noninjectivity on a divisor before using the explicit plane
pseudocover.

The mechanism is sharp.  The known nonproper étale endomorphism

\[
\eta(u,v,w)=
\left(w^2,\ 4v,\ w(1+2uv)\right)
\]

satisfies

\[
\{\eta^*f,\eta^*g\}=4\,\eta^*\{f,g\}.
\]

Moreover, the inverse image of the target component \(D\) is exactly the
two components of \(w=0\):

\[
D=V(u,w),\qquad
H=V(1+uv,w)\simeq\mathbf G_m,
\]

and

\[
\operatorname{div}(w)=D+H,\qquad [H]=[D].
\]

Thus the extra divisor predicted by the class group is not itself a
contradiction; it is realized by the standard pseudoplane étale
architecture.

A construction-first follow-up classifies the case in which this natural
component \(H\) also dominates \(e(D)\).  On the normalization
\(\widetilde\Gamma\simeq\mathbf A^1_t\), the two restrictions necessarily
have the form

\[
t|_D=v,\qquad t|_H=b+a u^n
\quad(a\ne0,\ n\in\mathbf Z\setminus\{0\}).
\]

Their values and first symplectic normal jets always glue by the CRT
splitting

\[
B/(w)\simeq\mathbf C[v]\times\mathbf C[u,u^{-1}],
\]

so there is no first-order obstruction.  However, the exact architecture
\(e^{-1}(e(D))=D\sqcup H\) is impossible: it would make the defining
equation of \(e(D)\) a constant multiple of \(w\), rectify that smooth
embedded affine line to a target coordinate, and produce a polynomial
mate \(R\) with \(\{w,R\}=1\).  Every rational mate has the unavoidable
form

\[
R=-u^{-1}+C(w^2),
\]

and is not regular along \(D\).  See
`current_context/QUADRATIC_PSEUDOPLANE_DH_COLLISION.md`.

## 6. What remains

These theorems rule out several tempting global constructions:

- homogeneous or target-homogenizable Pfaff potentials;
- all algebraic Hamiltonian flows;
- any injective or single-divisor étale map to the plane;
- arguments claiming that generic-fiber smoothness alone forces the
  unique \(\mathbf A^1\)-fibration.

A surviving Darboux pair must instead have:

- a genuinely multiweight Pfaff potential that cannot be homogenized by a
  target polynomial symplectomorphism;
- two non-locally-finite commuting Hamiltonian derivations;
- a nonproper étale map whose pullback of \(\Gamma=e(D)\) contains a
  second nonprincipal divisor of class \([D]\);
- exact forced differentials on every generic fiber despite this boundary
  collision.

The next plausible global obstruction is to classify the residual
class-\([D]\) component \(E\) in the standard boundary completion and
compare its two transverse étale sheets over \(\Gamma\).  The explicit
endomorphism above is the adversarial model: any proposed contradiction
must use that the target is \(\mathbf A^2\), not merely that it is a
smooth symplectic surface with trivial canonical bundle.

## Verification

Run:

```bash
.venv/bin/python route_a/pfaff_global_structure.py
```

The verifier checks the Laurent bracket, the exact Pfaff ODE reduction,
the non-homogenizable countermodel, the locally nilpotent generator,
the boundary factorization, and the multiplier of the known degree-two
étale endomorphism.
