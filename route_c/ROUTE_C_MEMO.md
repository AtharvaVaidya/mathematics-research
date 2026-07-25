# Route C progress memo

## Outcome

No chart-preserving nonproper étale endomorphism, and hence no plane
Keller counterexample, was obtained.  The calculations below give two exact
obstructions:

1. the entire separated/equivariant polynomial ansatz is forced to be the
   Chebyshev family, and every member of degree greater than one fails the
   chart condition;
2. conjugating the degree-two Chebyshev map by the full
   kernel-polynomial family of non-equivariant locally-nilpotent shears does
   not cure the failure.  An explicit copy of \(\mathbb G_m\) in the
   affine-plane chart is still sent to the deleted line.
3. more generally, no Chebyshev map of degree greater than one preserves
   the complement of *any* affine-line divisor whose complement is
   \(\mathbb A^2\).  Thus changing the plane chart, or conjugating by an
   arbitrary surface automorphism, cannot repair the construction.

There were no pre-existing Route C artifacts in the workspace when this
investigation began.  The only pre-existing workspace artifact was the
unrelated `route_a/route_a_search.py`, which was not changed.

## Surface, charts, and boundary

Put
\[
 S=\operatorname{Spec}\mathbb C[x,y,z]/(x^2y-z^2+1)
\]
and
\[
 D_\epsilon=V(x,z-\epsilon),\qquad \epsilon\in\{+1,-1\}.
\]
The surface is smooth.  The complement \(U_+=S\setminus D_-\) is an affine
plane with coordinates \((x,t)\):
\[
 z=1+x^2t,\qquad y=2t+x^2t^2.
\]
Likewise \(U_-=S\setminus D_+\) has coordinates \((x,s)\):
\[
 z=-1+x^2s,\qquad y=-2s+x^2s^2.
\]
On the overlap,
\[
 s=t+\frac{2}{x^2}.
\]
Thus an endomorphism restricts to a polynomial endomorphism of the desired
plane chart exactly when it maps \(U_+\) to \(U_+\), equivalently
\(\Phi^{-1}(D_-)\subseteq D_-\).

The global nowhere-vanishing two-form
\[
 \omega=\frac{dx\wedge dz}{x^2}
\]
equals \(dx\wedge dt\) on \(U_+\).  Near \(D_\pm\), the surface equation gives
\(\omega=dx\wedge dy/(2z)\), so it really is regular and nonvanishing
globally.  Consequently an étale endomorphism satisfies
\(\Phi^*\omega=c\omega\) for a constant \(c\in\mathbb C^\times\), since
\(\mathcal O(S)^\times=\mathbb C^\times\).

There is also a useful general boundary constraint.  If an étale
endomorphism satisfies \(\Phi^{-1}(D_-)\subseteq D_-\) and this inverse image
is nonempty, then the inverse image is the reduced divisor \(D_-\).
Indeed, étale base change preserves the reduced smooth divisor \(D_-\), and
there is no other possible component in its support.  The restricted map
\[
 \Phi|_{D_-}:\mathbb A^1\longrightarrow\mathbb A^1
\]
is therefore étale, hence affine linear.  In addition
\(\Phi^*[D_-]=[D_-]\) in \(\operatorname{Pic}(S)\).

## Classification of the equivariant ansatz

Consider the full ansatz
\[
 \Phi_{A,B,R}(x,y,z)=\bigl(xA(z),\,yB(z),\,R(z)\bigr)
\]
with \(A,B,R\in\mathbb C[z]\) and \(R\) nonconstant.  It preserves the
surface exactly when
\[
 A(z)^2B(z)=\frac{R(z)^2-1}{z^2-1}. \tag{1}
\]
On the dense set where the displayed fractions can be used directly,
\[
 \Phi^*\omega=\frac{R'(z)}{A(z)}\,\omega.
\]
If \(\Phi\) is étale, the coefficient is a global unit and hence
\[
 R'=cA,\qquad c\in\mathbb C^\times. \tag{2}
\]
Write \(d=\deg R\).  Substituting (2) in (1) and comparing degrees forces
\(B\) to be constant.  Comparing leading coefficients then gives
\[
 (z^2-1)R'(z)^2=d^2\bigl(R(z)^2-1\bigr). \tag{3}
\]
Differentiating (3) and cancelling the nonzero polynomial \(R'\) yields
\[
 (z^2-1)R''+zR'-d^2R=0. \tag{4}
\]
The space of polynomial solutions of (4) of degree at most \(d\) is
one-dimensional: comparison from the leading term downward determines
every coefficient of the same parity, and a solution of smaller degree is
zero.  It is spanned by \(T_d\).  Substitution back into (3) fixes the
scalar, so
\[
 R=\pm T_d,\qquad A=\frac{\pm d}{c}U_{d-1},\qquad
 B=\frac{c^2}{d^2}.
\]
Up to harmless scalings, these are exactly
\[
 \Phi_d(x,y,z)=\bigl(xU_{d-1}(z),\,y,\,T_d(z)\bigr),
\]
and \(\Phi_d^*\omega=d\omega\).

For \(d>1\), these maps never preserve the plane chart.  At each interior
critical point
\[
 r_k=\cos(k\pi/d),\qquad 1\leq k\leq d-1,
\]
one has \(U_{d-1}(r_k)=0\) and \(T_d(r_k)=(-1)^k\).  Therefore the curve
\[
 C_{r_k}=V(z-r_k)
   =\{(x,(r_k^2-1)/x^2,r_k):x\in\mathbb C^\times\}
   \cong\mathbb G_m
\]
is sent into \(D_{(-1)^k}\).  For \(d\geq3\), each target sign has such an
extra curve.  For \(d=2\), \(D_-\) has the extra curve \(C_0\), while the
inverse image of \(D_+\) contains both \(D_+\) and \(D_-\).  Thus neither
choice of deleted component works.  Replacing \(T_d\) by \(-T_d\) merely
interchanges the signs.

## Exact non-equivariant conjugation test

For every \(f\in\mathbb C[x]\), the locally nilpotent shear
\[
 \tau_f(x,y,z)=
 \left(x,\ y+2f(x)z+f(x)^2x^2,\ z+f(x)x^2\right)
\]
is an automorphism of \(S\), with inverse \(\tau_{-f}\).  It is
non-equivariant in \(z\), preserves each \(D_\pm\), and acts on the plane
chart as the triangular automorphism \(t\mapsto t+f(x)\).

Start from the degree-two étale map
\[
 \Phi_2(x,y,z)=(2xz,y,2z^2-1)
\]
and conjugate:
\[
 \Psi_f=\tau_{-f}\circ\Phi_2\circ\tau_f.
\]
Here the \(f\) in the final \(\tau_{-f}\) is evaluated at the new first
coordinate, as required for genuine conjugation.  Write
\[
 u=z+f(x)x^2,\quad X_0=2xu,\quad Z_0=2u^2-1,\quad
 Y_0=y+2f(x)z+f(x)^2x^2.
\]
Then its exact coordinates are
\[
\begin{aligned}
 X'&=X_0,\\
 Z'&=Z_0-f(X_0)X_0^2,\\
 Y'&=Y_0-2f(X_0)Z_0+f(X_0)^2X_0^2.
\end{aligned}
\]
Direct calculation gives the surface relation and the canonical
Jacobian
\[
 X'^2Y'=Z'^2-1,\qquad
 \Psi_f^*\omega=2\omega.
\]
So this really is an étale surface endomorphism for every
\(f\in\mathbb C[x]\).

Nevertheless the curve
\[
 E_f:\quad
 x=s,\quad z=-f(s)s^2,\quad
 y=f(s)^2s^2-s^{-2},\qquad s\in\mathbb C^\times,
\]
lies on \(S\), is contained in \(U_+\), and satisfies
\[
 X'|_{E_f}=0,\qquad Z'|_{E_f}=-1.
\]
Hence \(\Psi_f(E_f)\subset D_-\), proving
\(\Psi_f^{-1}(D_-)\not\subset D_-\).

On the plane chart, set \(u=1+x^2(t+f(x))\).  Where the image remains in
the chart, the induced rational map is
\[
 (x,t)\longmapsto
 \left(
 2xu,\,
 \frac{u^2-1}{2x^2u^2}-f(2xu)
 \right),
\]
whose Jacobian is exactly \(2\).  The second coordinate has a genuine pole
on \(u=0\), precisely the curve \(E_f\).  Thus the constant-Jacobian
identity on a dense open set does not descend to a polynomial plane map.

The same divisor argument applies to arbitrary compositions of these
shears, \(x/y\)-scalings, and \(z\mapsto-z\): these automorphisms only
permute \(D_+\) and \(D_-\), while the extra \(C_{r_k}\) components persist
under inverse image.  It does not by itself classify every automorphism of
\(S\), so no claim beyond this explicit generated family is made.

## No alternative affine-plane boundary for a Chebyshev map

There is an all-degree argument that removes the preceding qualification.
Let
\[
\Phi_d(x,y,z)=\bigl(xU_{d-1}(z),y,T_d(z)\bigr),\qquad d>1,
\]
and suppose that \(E\subset S\) is an irreducible smooth affine line such
that
\[
S\setminus E\simeq\mathbb A^2,\qquad
\Phi_d^{-1}(E)\subseteq E. \tag{5}
\]
The inverse image of a smooth reduced divisor under an étale map is smooth
and reduced.  First note that it is nonempty here.  The Chebyshev identity
shows directly that \(\Phi_d\) is surjective for odd \(d\).  For even \(d\),
the same root-by-root calculation gives
\[
S\setminus\Phi_d(S)=L_-=V(y,z+1):
\]
away from \(T_d(z)=-1\) one chooses a root with
\(U_{d-1}(z)\ne0\), while all roots over \(-1\) are critical and hence
force the target \(x\)-coordinate to vanish.  Thus the only divisor that
can have empty inverse image is \(L_-\).  The Picard calculation below
shows that \(S\setminus L_-\not\simeq\mathbb A^2\), so an \(E\) satisfying
(5) is not omitted.

Its inverse-image support is therefore contained in the irreducible curve
\(E\), so (5) gives
\[
\Phi_d^{-1}(E)=E.
\]
Consequently \(\Phi_d|_E:E\to E\) is étale and nonconstant, hence affine
linear after choosing a coordinate \(s\) on \(E\).

Put \(h(s)=z|_E\).  The semiconjugacy \(z\circ\Phi_d=T_d\circ z\) restricts
to
\[
h(\alpha s+\beta)=T_d(h(s)),\qquad \alpha\ne0. \tag{6}
\]
If \(h\) were nonconstant, the two sides of (6) would have degrees
\(\deg h\) and \(d\deg h\), respectively.  Hence \(h\) is constant.
The curve \(E\) is therefore an irreducible affine-line component of a
fiber \(z=r\).  If \(r^2\ne1\), that fiber is
\[
x^2y=r^2-1\simeq\mathbb G_m,
\]
so it contains no such component.  Thus the only candidates are
\[
D_\pm=V(x,z\mp1),\qquad L_\pm=V(y,z\mp1). \tag{7}
\]

Only \(D_\pm\) can bound an affine-plane chart.  Indeed, on
\(S_x\simeq\mathbb G_m\times\mathbb A^1\), the standard divisor-class
sequence gives
\[
\operatorname {Pic}(S)
=\frac{\mathbb Z[D_+]\oplus\mathbb Z[D_-]}
{\mathbb Z([D_+]+[D_-])}
\simeq\mathbb Z.
\]
Moreover
\[
\operatorname {div}(z-1)=2D_++L_+,\qquad
\operatorname {div}(z+1)=2D_-+L_-.
\]
Thus \([L_\pm]\) is twice a generator of \(\operatorname {Pic}(S)\).
If \(S\setminus E\simeq\mathbb A^2\), the localization sequence forces
\([E]\) to generate \(\operatorname {Pic}(S)\), excluding \(L_\pm\).

Finally \(D_\pm\) are not preserved.  The roots of
\(T_d(z)=\pm1\), together with \(T_d'=dU_{d-1}\), give either an additional
boundary component \(D_\mp\) or an interior critical fiber
\(z=\cos(k\pi/d)\simeq\mathbb G_m\) in the inverse image.  Therefore
\[
\boxed{\text{no }\Phi_d,\ d>1,\text{ preserves any }\mathbb A^2
\text{ complement on }S.} \tag{8}
\]

If an arbitrary surface automorphism \(\tau\) made
\(\tau^{-1}\Phi_d\tau\) preserve the standard chart, then
\(\Phi_d\) would preserve the affine-line boundary \(\tau(D_-)\), whose
complement is again \(\mathbb A^2\), contradicting (8).  Hence the result
also excludes every automorphism conjugate of the Chebyshev family, without
requiring a classification of \(\operatorname {Aut}(S)\).

## A small ansatz that is completely obstructed

Suppose the induced chart map is \((p,q)\) with \(p=h(x)\), and it extends
to a surface endomorphism.  The Keller equation gives
\[
 h'(x)q_t=c\ne0,
\]
so
\[
 h=ax+b,\qquad q=\alpha t+\beta(x),
\quad a,\alpha\ne0.
\]
Use the other chart, \(t=s-2/x^2\).  Regularity of
\[
 Z'=1+p^2q
\]
forces \(b=0\).  Regularity of
\[
 Y'=2q+p^2q^2
\]
then forces \(a^2\alpha=1\).  Thus
\[
 p=ax,\qquad q=\frac{t}{a^2}+\beta(x),
\]
which is triangular and extends to a surface automorphism.  Therefore no
nonproper example occurs in the entire subansatz where the first plane
coordinate depends only on \(x\).

## Reproduction

Run:

```bash
./.venv/bin/python route_c/verify_route_c.py
```

The script verifies over the exact rational function field:

- the formulas for \(\Psi_\lambda\), the constant-\(f\) specialization;
- the surface relation;
- the constant canonical Jacobian \(2\);
- the parametrized exceptional curve and its image in \(D_-\);
- the Chebyshev identities through degree \(8\);
- the rational chart Jacobian \(2\) and its nonremovable pole;
- the surface relation, canonical Jacobian, and exceptional curve for a
  generic quadratic \(f(x)\); the memo's arbitrary-degree statement follows
  formally from the displayed conjugation calculation.

## Comparison with the new three-dimensional quotient mechanism

Shaska's July 2026 analysis
([arXiv:2607.20210](https://arxiv.org/abs/2607.20210)) gives a useful
comparison, but not a Route C construction.  For the announced
three-dimensional graded Keller map, the map on the invariant quotient is
two-dimensional and its Jacobian vanishes to order two on the contracted
locus (Theorem 6.1).  Missing roots of the quotient fiber equation represent
sheets escaping to infinity rather than finite ramification (Proposition
5.1).  This resembles Route C in one precise respect: étaleness upstairs can
coexist with a degenerate or undefined two-dimensional description on a
boundary locus.

The difference is decisive.  Route C requires the chosen affine-plane chart
to be invariant, so no curve inside that chart may be sent to the deleted
divisor.  The curves \(C_{r_k}\) and \(E_f\) above violate exactly that
condition.  In the three-dimensional example the quotient Jacobian is
deliberately nonconstant (of the prescribed square-divisor form), while a
Route C plane restriction would have to be a globally polynomial Keller map.
Moreover, Theorem 3.3 of that paper rules out every genuinely
\(\mathbb G_m\)-equivariant Keller counterexample in dimension two.  Thus the
comparison suggests imposing boundary pullback conditions before lifting a
degenerate quotient map, but it does not bypass the obstruction proved here.

## Next viable directions

The calculations eliminate “equivariant map plus standard shear/scaling
conjugation” as a source of a counterexample.  A genuinely new candidate
must change the pullback geometry of \(D_-\), not merely move the known
critical curves.  Two concrete next targets are:

1. construct an étale endomorphism outside the Chebyshev family, since no
   change of affine-plane boundary can repair a Chebyshev map;
2. search a global-coordinate ansatz in which \(X'\) depends essentially on
   both \(y\) and \(z\), while imposing the exact boundary condition first.

The present work is an obstruction/progress result only, not a resolution
of the Jacobian conjecture.
