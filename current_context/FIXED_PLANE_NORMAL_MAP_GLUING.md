# Normal-map gluing at resolved target ends

Date: 25 July 2026

**Subsequent exponent audit.**
`FIXED_PLANE_RESIDUE_EXPONENT_CLASSIFICATION.md` carries out the target
suggested in Section 8.  It proves the exact formula
\(m=-1-2\epsilon\delta j\) relating the conductor residual exponent to
the Poincare-residue exponent.  The formula does not force \(j=0\): a
smooth quartic \(\mathbf G_m\) with the exact fixed-plane residue \(2/3\)
has \(j=-1\) and passes both resolved-end valuation ledgers.  Thus the
remaining obstruction must couple the two endpoint Green problems
globally.

This note supplies the local compatibility condition missing from
`FIXED_PLANE_COMPONENT_ENDPOINT_PAIRING.md`.  In the degree-two case it
is strictly stronger than component adjunction: the tangential and
normal parts of the Jacobian must glue **at every residual boundary
contact**, not merely have the correct total degree.

Under the hypotheses below, this rules out the repaired \(d=2\)
component ledger in that note.  Resolving a singular target end gives a
more general valuation formula.  For the explicit two-ended degree-nine
curve used in `GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`, that formula
also rules out the displayed full-effectivity witness as a realization
of that particular target curve.

## 1. Setup

Retain the smooth-affine-\(\Gamma\), reduced-pullback, and
separated-contact hypotheses of
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`.  Let
\[
\phi:X\longrightarrow\mathbf P^2
\]
be a resolved morphism, let \(E_i\) be a boundary component, and let
\(H\) be a residual component of \(\phi^*\overline\Gamma\).  Write
\[
P=\phi^*L_\infty=\sum_i b_iE_i,\qquad
\phi^*\overline\Gamma=C+\sum_jH_j+\sum_i\eta_iE_i,
\tag{1}
\]
\[
K_X-\phi^*K_{\mathbf P^2}=\sum_i r_iE_i,\qquad
r_i=a_i-1+3b_i,
\tag{2}
\]
and
\[
\sigma_i=db_i-\eta_i,\qquad \kappa_i=a_i+\sigma_i.
\tag{3}
\]

Assume now that \(d=2\), that \(\overline\Gamma\) is an irreducible
conic, and that its two infinity ends are simple.  An irreducible
projective conic is smooth, and each end is a transverse intersection
of \(\overline\Gamma\) with \(L_\infty\).

Let \(w\in H\cap E_i\) be a separated transverse contact mapping to one
of these ends.

## 2. The pointwise tangential-normal identity

Choose regular target parameters \((z,q)\) at \(\phi(w)\), with
\[
L_\infty=(z=0),\qquad \overline\Gamma=(q=0).
\]
Choose regular source parameters \((x,u)\) at \(w\), with
\[
E_i=(x=0),\qquad H=(u=0).
\]
The divisor identities (1), reducedness of \(H\), and separation of the
contact give
\[
z\circ\phi=x^{b_i}A(x,u),\qquad
q\circ\phi=x^{\eta_i}uB(x,u),
\tag{4}
\]
where \(A(0,0)B(0,0)\ne0\).  Wedge differentiation yields
\[
\phi^*(dz\wedge dq)
=x^{b_i+\eta_i-1}
\bigl(b_iA(0,0)B(0,0)+xC(x,u)+uD(x,u)\bigr)\,dx\wedge du.
\tag{5}
\]
Because the ground field has characteristic zero and \(b_i>0\), the
coefficient displayed in (5) is nonzero at \(w\).  Thus the generic
ramification order along \(E_i\) is forced to be
\[
\boxed{\qquad r_i=b_i+\eta_i-1.\qquad}
\tag{6}
\]
Combining (2), (3), and \(d=2\) gives the equivalent vertexwise laws
\[
\boxed{\qquad
\eta_i=a_i+2b_i,\qquad
\sigma_i=-a_i,\qquad
\kappa_i=a_i+\sigma_i=0.
\qquad}
\tag{7}
\]

The same equality holds if several residual components meet \(E_i\) at
distinct points: applying (5) at any one of their simple roots prevents
the leading Jacobian coefficient from vanishing identically along
\(E_i\).  Consequently endpoint charge cannot be transferred from one
boundary vertex to another merely because the component-level charge
sum is zero.

## 3. Global normal-section interpretation

Let \(f=\phi|_H:H\to\overline\Gamma\simeq\mathbf P^1\) have degree
\(e\).  The normal differential is a section
\[
\nu_H\in H^0\!\left(
H,\;N_{H/X}^{\vee}\otimes f^*N_{\overline\Gamma/\mathbf P^2}
\right).
\tag{8}
\]
Since the affine map is étale, \(\nu_H\) has no affine zero.  Formula
(4) says that its zero order at \(w\) is exactly \(\eta_i\).  Since
\[
\deg N_{\overline\Gamma/\mathbf P^2}=4,\qquad
\deg N_{H/X}=H^2,
\]
one obtains
\[
\boxed{\qquad
\operatorname{div}(\nu_H)=\sum_{w\in\partial H}\eta_{i(w)}w,
\qquad
\sum_{w\in\partial H}\eta_{i(w)}=4e-H^2.
\qquad}
\tag{9}
\]
Likewise, at one of the two infinity contacts the tangential
differential contributes \(b_i-1\), because the target end is simple
and the local cover degree is \(b_i\).  Equation (6) is exactly the
local gluing of these two factors in the determinant:
\[
r_i=(b_i-1)+\eta_i.
\tag{10}
\]
At an additional boundary contact over a finite nonproper value, the
same determinant decomposition uses its actual local tangential
ramification order in place of \(b_i-1\).  Summing all these local
decompositions, (9) and Riemann--Hurwitz recover
\[
R\cdot H=2g(H)-2-H^2+6e.
\tag{11}
\]
Thus the global degree formula in the previous note was correct, but it
lost the decisive pointwise allocation (10).

## 4. Exclusion of the repaired \(d=2\) ledger

The repaired ledger of
`FIXED_PLANE_COMPONENT_ENDPOINT_PAIRING.md` places four residual
contacts on
\[
(a,b,\sigma,\eta,r)_{E_1}=(-1,1,-1,3,1)
\tag{12}
\]
and pairs each with a remote contact on
\[
(a,b,\sigma,\eta,r)_F=(1,1,1,1,3).
\tag{13}
\]
At \(E_1\), (6) requires
\[
r_{E_1}=1+3-1=3,
\]
whereas the assigned ramification coefficient is \(1\).  At \(F\), it
requires
\[
r_F=1+1-1=1,
\]
whereas the assigned coefficient is \(3\).  Equivalently,
\(\kappa_{E_1}=-2\) and \(\kappa_F=2\), while (7) requires each charge
to vanish separately.

Therefore
\[
\boxed{\text{the repaired \(d=2\) component ledger has no realization
by a resolved morphism satisfying the stated conic-end hypotheses.}}
\tag{14}
\]
This conclusion is local and does not depend on completing the
unspecified old attachment rows or on searching larger blowup trees.

## 5. The resolved-target valuation formula

There is an exact replacement for (6) at a singular target end.  Let
\[
\rho:Y\longrightarrow\mathbf P^2
\]
be an embedded resolution of the pair
\((\overline\Gamma,L_\infty)\).  After further source blowups, resolve
the rational lift of \(\phi\) to a morphism
\(\psi:X'\to Y\).  At the lifted residual contact, let \(D\) be the
target boundary component meeting the strict transform of
\(\overline\Gamma\).  Choose local target coordinates \((y,q)\) with
\[
D=(y=0),\qquad \widetilde\Gamma=(q=0),
\]
and write
\[
\rho^*L_\infty=y^M\cdot\text{unit},\qquad
\rho^*\overline\Gamma=y^Nq\cdot\text{unit},
\tag{15}
\]
\[
K_Y-\rho^*K_{\mathbf P^2}=cD+\cdots .
\tag{16}
\]
Here \(M>0\), \(N\ge0\), and \(c\ge0\) are determined entirely by the
resolved target branch.

If the lifted source boundary component has
\[
y\circ\psi=x^\beta A,\qquad
q\circ\psi=x^\theta uB,
\tag{17}
\]
then
\[
b=M\beta,\qquad \eta=N\beta+\theta.
\tag{18}
\]
The local Jacobian of \(\psi\) has order
\(\beta+\theta-1\), while the pullback of the relative canonical
divisor (16) adds \(c\beta\).  Therefore
\[
\boxed{\qquad
r=\eta+\mu b-1,\qquad
\mu=\frac{c+1-N}{M}.
\qquad}
\tag{19}
\]
Equivalently,
\[
\boxed{\qquad
\kappa=a+\sigma=(d-3+\mu)b.
\qquad}
\tag{20}
\]

This formula genuinely descends to the pre-lift source tree.  Blowing
up a transverse contact of \(H\) with a single boundary component
changes
\[
(a,b,\eta,\sigma)\longmapsto
(a+1,b,\eta+1,\sigma-1),
\tag{21}
\]
so
\[
\boxed{\qquad b\ \text{and}\ \kappa=a+\sigma
\text{ are invariant along the contact blowup chain}.\qquad}
\tag{22}
\]
Thus the target valuation fixes the endpoint charge already visible in
the unresolved ledger.

## 6. One Laurent exponent glues every residual component

The target invariant in (20) has an intrinsic affine interpretation.
Let \(F(U,V)=0\) be a reduced equation of the smooth affine curve
\(\Gamma\), and let
\[
\omega_\Gamma=
\operatorname {Res}_{\Gamma}\frac{dU\wedge dV}{F}.
\tag{23}
\]
Smoothness makes this a nowhere-vanishing generator of
\(\omega_\Gamma\).  After choosing
\(\mathbf C[\Gamma]=\mathbf C[s,s^{-1}]\), every unit is a Laurent
monomial, so there is one integer \(j\) such that
\[
\boxed{\qquad
\omega_\Gamma=\lambda s^j\,\frac{ds}{s},
\qquad\lambda\ne0.
\qquad}
\tag{24}
\]

To compare (24) with the target-resolution data, use the projective
chart \(V\ne0\), with \(u=U/V,z=Z/V\), and let \(q\) be the
dehomogenized degree-\(d\) equation.  Directly,
\[
\frac{dU\wedge dV}{F(U,V)}
=-z^{d-3}\frac{du\wedge dz}{q(u,z)}.
\tag{25}
\]
On the resolved target, the Poincare residue of the rightmost fraction
has order \(c-N\) along the normalized branch.  Therefore
\[
\operatorname {ord}_t(\omega_\Gamma)
=(d-3)M+c-N,
\tag{26}
\]
where \(t\) is a local parameter at that normalization end.  Combining
(19)--(20) and (26), a contact of local cover degree \(e_w=\beta\)
obeys
\[
\boxed{\qquad
\kappa_{i(w)}
=e_w\bigl(\operatorname {ord}_t\omega_\Gamma+1\bigr).
\qquad}
\tag{27}
\]

At \(s=0\), (24) has order \(j-1\); at \(s=\infty\), it has order
\(-j-1\).  Hence every residual component, and every split contact of
that component, is glued by the same target integer:
\[
\boxed{\begin{aligned}
w\mid s=0&:\quad \kappa_{i(w)}=e_wj,\\
w\mid s=\infty&:\quad \kappa_{i(w)}=-e_wj.
\end{aligned}}
\tag{28}
\]
In particular, two boundary vertices serving the same target end cannot
carry unrelated values of \(\kappa/e_w\).  Summing (28) over a
degree-\(e\) residual component recovers the zero-charge law, but the
pointwise proportionality is strictly stronger.  This is the global
normal-map gluing constraint that the component ledger did not encode.

## 7. The explicit Laurent two-end curve

For \(d\ge3\), consider the degree-\(d\) curve
\[
UVZ^{d-2}-U^d+\lambda Z^d=0,\qquad \lambda\ne0,
\tag{29}
\]
parametrized on its affine part by
\[
U=As,\qquad V=Bs^{-1}+A^{d-1}s^{d-1}.
\tag{30}
\]
Here \(A,B\in\mathbf C^\times\) and \(AB+\lambda=0\).
Both normalization ends map to \([0:1:0]\).  In the chart \(V=1\), put
\(u=U/V,z=Z/V\).  The local equation is
\[
uz^{d-2}-u^d+\lambda z^d=0.
\tag{31}
\]

At the \(s=0\) end, one blowup \(u=zu_1\) separates the smooth branch.
The target data are
\[
(M,N,c)=(1,d-1,1).
\tag{32}
\]
At the \(s=\infty\) end, the branch has primitive parametrization
\[
(u,z)=(t^{d-2}\cdot\text{unit},
       t^{d-1}\cdot\text{unit}).
\]
The final exceptional valuation in its toric resolution has
\[
(M,N,c)=
\bigl(d-1,\ d(d-2),\ 2d-4\bigr).
\tag{33}
\]
In both cases,
\[
\mu=3-d.
\tag{34}
\]
Consequently (20) becomes the pointwise law
\[
\boxed{\qquad\kappa=0\quad\text{at both ends of (29).}\qquad}
\tag{35}
\]
Equivalently, \(F_V=U\) gives
\(\omega_\Gamma=dU/F_V=ds/s\), so \(j=0\) in (24).

For the \(d=9\) full-effectivity witness in
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`, the residual bridge meets
nodes \(3\) and \(6\).  Its displayed vectors give
\[
\kappa_3=a_3+(9b_3-\eta_3)=1+(72-74)=-1,
\]
\[
\kappa_6=a_6+(9b_6-\eta_6)=0+(9-8)=1.
\tag{36}
\]
Their sum passes component adjunction, but each value violates (35).
Hence that numerical witness cannot be realized using the explicit
degree-nine target curve (29) of that memo.  This is independent of its
already-recorded final-curve failure.

## 8. Scope and next target

The argument proves a bounded structural theorem, not the Jacobian
conjecture.  Its trust boundary is:

1. for the degree-two exclusion, \(\overline\Gamma\) is an irreducible
   conic with two simple infinity ends;
2. for the singular-end formula, the target pair and the rational
   source lift are resolved so that the displayed contact is
   transverse;
3. the pullback of \(\Gamma\) is reduced, and the source contacts have
   been separated and made transverse;
4. the resolution actually defines a morphism \(\phi\); and
5. the affine restriction is étale.

For \(d\ge3\), an affine curve isomorphic to \(\mathbf G_m\) cannot have
a smooth projective plane closure of degree \(d\).  Formula (19)
handles this by resolving the target branch, but the value of
\((M,N,c)\) varies with the target embedding.  The promising
continuation was therefore to derive the two endpoint values of
\(\mu\) directly from the conductor Laurent embedding and its residue
constraint.  The subsequent exponent audit cited above does this and
finds a sharp nonzero model.  The new target is a global coupling of the
two endpoint subtrees, rather than a broader search over source blowup
trees.

The local determinant, normal-degree identity, resolved-target formula,
and contradictions to (12)--(13) and (36) are checked in
`verify_fixed_plane_normal_map_gluing.py`.
