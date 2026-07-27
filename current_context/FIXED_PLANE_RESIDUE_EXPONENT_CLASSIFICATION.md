# The conductor residue exponent and a sharp nonzero model

Date: 25 July 2026

This note completes the Laurent-exponent calculation begun in
`FIXED_PLANE_NORMAL_MAP_GLUING.md`.  In the smooth conductor-image case,
the exponent \(j\) of the Poincare residue is not an independent target
parameter: it is exactly the normalized odd exponent of the residual
pullback divisor on the fixed-source conductor.

The resulting formula is strong, but it does **not** force \(j=0\).
There is a smooth plane quartic \(\Gamma\simeq\mathbf G_m\) which has the
exact fixed-plane Liouville residue \(2/3\), the same \((2,5)\) and
\((2,3)\) infinity branches as the fixed-source conductor, and
\(j=-1\).  Its target-resolution data glue exactly to the two source
conductor ends.  Thus a proof that \(j=0\) needs a genuinely global
source-boundary theorem; conductor parity, projective degree, endpoint
charges, and the Green equation do not suffice.

## 1. Exact classification of \(j\)

Work over an algebraically closed field of characteristic zero.  Retain
the fixed-source notation
\[
C=\{D=0\},\qquad
c=\frac{v^2}{9},\qquad
t=\frac{3(v+2)}{v^2}.
\tag{1}
\]
Suppose that a hypothetical Darboux pair
\[
e=(U,V):\mathbf A^2_{t,c}\longrightarrow\mathbf A^2
\]
has smooth conductor image \(\Gamma\simeq\mathbf G_m\).  Choose a
normalization coordinate \(s\) so that
\[
s=\alpha c^{\epsilon\delta},
\qquad
\epsilon\in\{1,-1\},\quad \delta\ge1.
\tag{2}
\]
Let \(F(X,Y)=0\) be a reduced equation of \(\Gamma\).  The smoothness and
squarefree-pullback argument gives
\[
F(U,V)=D H,\qquad
h(v):=H|_C=\lambda v^m
\tag{3}
\]
for \(\lambda\ne0\) and an odd integer \(m\).

Write the target Poincare residue as
\[
\omega_\Gamma
=\operatorname {Res}_\Gamma\frac{dX\wedge dY}{F}
=\lambda_0s^j\frac{ds}{s},
\qquad j\in\mathbf Z.
\tag{4}
\]
The tangent and conormal vectors on \(\Gamma\) are unimodular.  Hence
there is a Laurent unit \(k(s)\) such that, for
\(X=\bar u(s),Y=\bar w(s)\),
\[
dF=k(s)(-s\bar w_s,s\bar u_s).
\tag{5}
\]
On the open set where \(\bar u_s\ne0\),
\[
\omega_\Gamma
=\frac{dX}{F_Y}
=\frac{\bar u_s\,ds}{k(s)s\bar u_s}
=k(s)^{-1}\frac{ds}{s}.
\tag{6}
\]
Thus \(k(s)\) has Laurent exponent \(-j\).

The fixed-source determinant identity along \(C\) gives
\[
h(v)=-\frac{k(s)s}{6cv\,s_c}.
\tag{7}
\]
Since \(s_c=\epsilon\delta s/c\), equations (2), (6), and (7) give the
exact exponent identity
\[
\boxed{\qquad
m=-1-2\epsilon\delta j,
\qquad
j=-\epsilon\,\frac{m+1}{2\delta}.
\qquad}
\tag{8}
\]
This sharpens the earlier congruence
\(m\equiv-1\pmod {2\delta}\): the quotient is precisely the negative
Poincare-residue exponent, up to the choice of orientation of \(s\).

If \(r=\deg H\), the two source projective intersections are
\[
I_{v=0}(\overline C,\overline H)=2r+m,\qquad
I_{v=\infty}(\overline C,\overline H)=2r-m.
\tag{9}
\]
They are positive odd integers, so
\[
\boxed{\qquad
|1+2\epsilon\delta j|=|m|<2r.
\qquad}
\tag{10}
\]
This is a finite-support bound on \(j\), but it permits nonzero values.

## 2. Endpoint charges

Let
\[
\kappa_i=a_i+\sigma_i,\qquad
\sigma_i=d b_i-\eta_i,
\tag{11}
\]
where \(d=\deg\overline\Gamma\).  The resolved-target normal-map formula
from `FIXED_PLANE_NORMAL_MAP_GLUING.md` says that a source contact of
local cover degree \(e_w\) satisfies
\[
\kappa_{i(w)}
=e_w\bigl(\operatorname {ord}_w\omega_\Gamma+1\bigr).
\tag{12}
\]
Therefore
\[
w\mid s=0:\quad\kappa=e_wj,
\qquad
w\mid s=\infty:\quad\kappa=-e_wj.
\tag{13}
\]

The fixed-source conductor has local cover degree \(2\delta\) at both
ends.  In the orientation \(s=\alpha c^\delta\), its two endpoint
charges are
\[
\boxed{\qquad
\kappa_{v=0}=2\delta j=-(m+1),\qquad
\kappa_{v=\infty}=-2\delta j=m+1.
\qquad}
\tag{14}
\]
The bare \((2,5)\) and \((2,3)\) cusp resolutions have augmented
canonical labels \(1\) and \(-1\) at the conductor contacts.  Before any
additional contact blowup, (14) therefore gives
\[
\sigma_{v=0}=-m-2,\qquad
\sigma_{v=\infty}=m+2.
\tag{15}
\]
A blowup at a conductor contact changes
\[
(a,b,\eta,\sigma)\mapsto(a+1,b,\eta+1,\sigma-1)
\tag{16}
\]
and leaves \(\kappa\) invariant.  It also lowers \(C^2\) by one, so the
conductor identity
\(\sigma_{v=0}+\sigma_{v=\infty}=C^2\) remains exact.

Equations (13)--(15) show the precise limitation of a sign argument.
If one could prove \(\kappa\ge0\) independently at both target ends,
then \(j=0\) would follow immediately.  Component adjunction proves only
that the two charges sum to zero, and the Green formula permits one
negative endpoint whenever the strict-pullback incidence potential is
large enough.

## 3. A smooth quartic with \(j=-1\)

Consider
\[
\boxed{\qquad
F(X,Y)=(3XY+1)^2-X
\qquad}
\tag{17}
\]
and the Laurent parametrization
\[
X=s^2,\qquad
Y=-\frac{s^{-1}+s^{-2}}3.
\tag{18}
\]
These boundary values genuinely descend from the fixed-source target
ring.  If \(B_0=2+4t-3ct^2\) denotes the old generator \(b\), then on
the conductor \(B_0+1=4/(3c)\), and
\[
U_0=c^2,\qquad
V_0=-\frac{B_0+1}{4}-\frac{3(B_0+1)^2}{16}
\tag{18a}
\]
restrict to (18) with \(s=c\).  This proves algebraizability of the
boundary values in the original ring.  The pair \((U_0,V_0)\) is not
claimed to be Darboux; it is not a Keller counterexample.

Put \(T=-(3XY+1)\) in the coordinate ring of (17).  Then
\[
T^2=X,\qquad T^{-1}=-3TY-1,
\tag{19}
\]
so (17) has coordinate ring
\(\mathbf C[T,T^{-1}]\).  In particular it is a closed smooth embedding
of \(\mathbf G_m\) in \(\mathbf A^2\).

The two relevant differentials are
\[
X\,dY
=\left(\frac13+\frac{2}{3s}\right)ds,
\qquad
\operatorname {Res}_{s=0}(X\,dY)=\frac23,
\tag{20}
\]
and
\[
\omega_\Gamma
=\frac{dX}{F_Y}
=-\frac13s^{-1}\frac{ds}{s}.
\tag{21}
\]
Thus this curve has exactly the fixed-plane conductor residue and
\[
\boxed{j=-1.}
\tag{22}
\]
Moreover (5) holds with
\[
k(s)=-3s.
\tag{23}
\]
For the degree-two conductor cover \(s=c=v^2/9\), equation (7) gives
\[
h(v)=\frac v{18},\qquad m=1,
\tag{24}
\]
as the normal coefficient required by the Keller determinant.  It is a
Laurent unit and satisfies (8) sharply.  This does not assert that the
particular non-Darboux lifts (18a) have this normal coefficient.
The required unit is itself algebraizable on the source:
\[
\frac{Dv}{18}
=\frac{9B_0c-27A_0c^2-8}{18}\in R,
\qquad
A_0=t+t^2-ct^3.
\tag{24a}
\]
What remains absent is the nonlinear identity
\(F(U,V)=D(v/18)\) for one global Darboux pair.

The projective closure is the quartic
\[
(3XY+Z^2)^2-XZ^3=0.
\tag{25}
\]
Its two infinity points are distinct.  At \(s=0\), in the chart \(Y=1\),
\[
x=-\frac{3s^4}{1+s},\qquad
z=-\frac{3s^2}{1+s},\qquad
3x+z^2=-\frac{9s^5}{(1+s)^2},
\tag{26}
\]
so the branch has characteristic pair \((2,5)\).  At \(s=\infty\),
putting \(\tau=s^{-1}\) in the chart \(X=1\) gives
\[
y=-\frac{\tau^3+\tau^4}{3},\qquad z=\tau^2,\qquad
3y+z^2=-\tau^3,
\tag{27}
\]
so the other branch has pair \((2,3)\).

Resolve each target pair consisting of the branch and the target line
at infinity.  At the final exceptional curve meeting the strict branch,
the triples
\[
(M,N,c_{\rm rel})
=\bigl(
\operatorname {ord}(\rho^*L_\infty),
\operatorname {ord}(\rho^*\overline\Gamma),
\operatorname {ord}(K_Y-\rho^*K_{\mathbf P^2})
\bigr)
\]
are
\[
\boxed{\qquad
(M,N,c_{\rm rel})_{s=0}=(2,10,6),\qquad
(M,N,c_{\rm rel})_{s=\infty}=(2,6,4).
\qquad}
\tag{28}
\]
Indeed, the \((2,5)\) resolution has total-transform sequences
\[
M=(1,1,1,2),\quad N=(2,4,5,10),\quad c_{\rm rel}=(1,2,3,6),
\tag{29}
\]
and the \((2,3)\) resolution has
\[
M=(1,1,2),\quad N=(2,3,6),\quad c_{\rm rel}=(1,2,4).
\tag{30}
\]
Since \(d=4\), the resolved-target slopes are
\[
\mu=\frac{c_{\rm rel}+1-N}{M}
=-\frac32,\ -\frac12.
\tag{31}
\]
Consequently
\[
d-3+\mu=-\frac12,\ \frac12.
\tag{32}
\]
Pulling back by the local degree-two conductor cover gives
\(b=2M=4\) at both ends and hence
\[
\kappa=-2,\ 2,
\tag{33}
\]
exactly as predicted by \(j=-1\).

There is also an exact source-lift ledger.  At the \((2,5)\) end, one
additional blowup at the conductor contact is necessary and sufficient:
\[
(a,b,\kappa,\sigma,\eta,\theta,r)
=(2,4,-2,-4,20,0,13).
\tag{34}
\]
At the \((2,3)\) end no contact blowup is needed:
\[
(a,b,\kappa,\sigma,\eta,\theta,r)
=(-1,4,2,3,13,1,10).
\tag{35}
\]
Here
\[
\eta=N\beta+\theta,\quad \beta=2,
\qquad
r=c_{\rm rel}\beta+\beta+\theta-1
=\eta+\mu b-1
=a-1+3b
\tag{36}
\]
holds coefficient-for-coefficient.  Also \(C^2=-1\) after (34), and
\[
\sigma_0+\sigma_\infty=-4+3=-1=C^2,
\qquad
\eta_0+\eta_\infty-1=32=2\cdot1\cdot4^2.
\tag{37}
\]

Thus the nonzero exponent is compatible not only with the affine
residue but with both resolved target ends and the exact conductor
intersection identities.  Each local ledger is realizable at the
valuation level by
\[
y\circ\psi=x^\beta\cdot\text{unit},\qquad
q\circ\psi=x^\theta u\cdot\text{unit};
\]
no global source morphism is asserted.

## 4. Why finality and the Green formula do not yet kill the model

At a final type-\(1\) curve of pullback multiplicity \(b_f\),
\[
a_f=-2b_f,\qquad
\sigma_f=db_f,\qquad
\kappa_f=(d-2)b_f.
\tag{38}
\]
For the quartic (17), this is positive.  Positivity at the final
dicritical vertices does not propagate to every point-mapping endpoint:
the Green equation is
\[
\sigma_S=A_S^{-1}V\sigma_D-A_S^{-1}z_S,
\tag{39}
\]
and the second term has the opposite sign.

A one-row exact independence model makes this explicit.  Take a
point-mapping vertex with self-intersection \(-2\), \(b=4\), and attach
two final type-\(1\) defects with \(b=1,7\).  The point row of the
pullback-line equation is
\[
-2\cdot4+1+7=0.
\tag{40}
\]
At the \(s=0\) endpoint use the resolved-source data
\((a,\sigma,\kappa)=(2,-4,-2)\).  Then
\[
-2(-4)+4+28=40=z\ge0.
\tag{41}
\]
Because the central coefficient is \(\eta=20\) and a type-\(1\) curve
has \(\eta=0\), the effective-pullback row is exact as well:
\(-2\cdot20+40=0\).
At the \(s=\infty\) endpoint use
\((a,\sigma,\kappa)=(-1,3,2)\).  Then
\[
-2(3)+4+28=26=z\ge0.
\tag{42}
\]
Here \(\eta=13\), so \(-2\cdot13+26=0\) as well.
The two attached defects \(4,28\) are exactly \(db_f\), their augmented
canonical labels are \(-2,-14\), and all ramification coefficients are
nonnegative.  Equations (40)--(42) are exact point rows of
\(Qb=0\), \(Q\eta+z=0\), and \(Q\sigma=z\).  They show that the Green
equation together with the final type-\(1\) values does not imply
\(j=0\).

There is likewise no contradiction at the level of augmented-canonical
finality.  Starting from the two fixed-source cusp arms:

1. after the necessary contact blowup of the label-\(1\) \((2,5)\)
   endpoint, a generic child has positive label \(3\) and can be final
   type \(3\);
2. two generic blowups away from the conductor on the label-\(-1\)
   \((2,3)\) endpoint end in a label-\(1\) final type-\(3\) curve; and
3. the standard crossing insertion between labels \(-2,-1\), followed
   by a generic blowup, ends in a label-\(-2\) final type-\(1\) curve
   with \(b=1\).

This is a label- and local-equation-compatible skeleton, not a complete
compactified Keller map.  Similarly, (40)--(42) are independence rows,
not a globally realized blowup tree.  Their role is exact: they rule out
deducing \(j=0\) from the listed target/conductor/Green/finality
constraints alone.

## 5. Hypothesis audit

The countermodel has three different logical levels which must not be
conflated.

1. **Genuine plane-curve data.**  Equations (17)--(27) define a smooth
   closed quartic \(\mathbf G_m\subset\mathbf A^2\), its boundary values
   come from the fixed-source ring by (18a), its Liouville residue is
   exactly \(2/3\), and its two projective ends are exactly \((2,5)\)
   and \((2,3)\).
2. **Genuine local valuation data.**  The target resolutions (28), the
   degree-two conductor cover, and the local monomial lifts underlying
   (34)--(36) satisfy the determinant and divisor formulas exactly.
3. **Necessary-equation independence data.**  The odd normal coefficient
   (24), the Green rows (40)--(42), and the finality skeleton are the
   values forced or permitted by a hypothetical Keller completion.
   They have not been glued into one global \(Qb=y\) solution or one
   polynomial Darboux pair.

Accordingly, this note gives a sharp countermodel to the inference
“fixed-source residue + both target ends + endpoint Green equations +
final type values imply \(j=0\).”  It is not a counterexample to the
Jacobian conjecture and not a realization of the full fixed-plane
construction.

## 6. Consequence

The rigorous conclusion is
\[
\boxed{\text{\(j\) is classified by (8), but the available fixed-plane
constraints do not force \(j=0\).}}
\tag{43}
\]
The next useful theorem would have to couple the two target-end Green
problems through the *same global* pullback-line solution and the same
type-\(1\) dicritical set.  A sign theorem for each end separately would
immediately force \(j=0\) by (13), but no such theorem follows from
component adjunction, target resolution, or finality values alone.

All identities for the quartic, both resolution triples, the source
endpoint ledgers, and the exact Green rows are checked in
`verify_fixed_plane_residue_exponent_classification.py`.
