# Residual endpoint pairing and the limit of the Green inequality

Date: 25 July 2026

**Subsequent resolution.**  The component-level repair below passes the
summed tests recorded in this note, but it does not pass the pointwise
normal-map gluing law.  `FIXED_PLANE_NORMAL_MAP_GLUING.md` proves that a
residual contact over a simple end of a smooth conic must satisfy
\(r_i=b_i+\eta_i-1\), equivalently \(a_i+\sigma_i=0\), at each endpoint.
The two endpoints in Section 4 violate that law in opposite directions.
Thus the repair remains a valid independence example for the summed
equations, but it is not realizable by a resolved morphism.

This note tests whether Riemann--Hurwitz, adjunction, projection formula,
and separated local intersections supply the missing upper bound on the
affine-incidence term in the fixed-plane Green formula
\[
\sigma_S=A_S^{-1}V\sigma_D-A_S^{-1}z_S.
\tag{1}
\]

They give a useful new endpoint-charge law, and they rule out the
four-vertex local counterledger of
`FIXED_PLANE_DEFECT_GREEN_FUNCTION.md` as an actual fixed-plane
component ledger.  However, the smallest degree-corrected version still
satisfies every component-level equation while retaining a negative
point defect.  Thus these tools alone do not prove
\[
A_S^{-1}z_S\le A_S^{-1}V\sigma_D.
\tag{2}
\]
The remaining inequality must use the full boundary morphism, finality,
or a local normal-map constraint stronger than the degrees of its zero
divisor.

Throughout, retain the smooth-\(\Gamma\), reduced-pullback, disjoint
affine-component, and separated-contact hypotheses of
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`.  Write
\[
P=\sum b_iE_i,\qquad
G=C+\sum_jH_j+\sum\eta_iE_i,\qquad
\sigma_i=db_i-\eta_i,
\tag{3}
\]
and
\[
r_i=a_i-1+3b_i.
\tag{4}
\]

## 1. The residual endpoint-charge law

The affine curve \(\Gamma\) is smooth with
\(\Gamma\simeq\mathbf G_m\).  Since the polynomial map is étale in the
affine plane, every connected component
\[
H_j^\circ\longrightarrow\Gamma
\]
is an étale quasi-finite cover.  It need not be finite: nonproperness
can remove finitely many points lying over finite points of \(\Gamma\).
Zariski's Main Theorem embeds it in its finite normalization over
\(\Gamma\), but that finite cover can ramify at the omitted points.
Let \(H_j\) be the smooth projective completion, of genus \(g_j\), and
let \(s_j\) be its number of separated transverse boundary contacts.
There is at least one contact over each of the two infinity ends of
\(\Gamma\), so \(s_j\ge2\); further contacts can lie over finite
nonproper values.

Let the two points of
\(\overline\Gamma^\nu\setminus\Gamma\) meet the target line at
multiplicities \(\ell_+,\ell_->0\).  Then
\[
\ell_++\ell_-=d.
\tag{6}
\]
For a contact \(w\) over the \(+\) or \(-\) infinity end, let
\(e_w\) be its local mapping degree.  Projection formula gives
\[
\boxed{\qquad
b_w=e_w\ell_\pm,\qquad
\sum_{w\mid +}e_w=\sum_{w\mid -}e_w=e_j.
\qquad}
\tag{7}
\]
Every additional contact \(E_w\) has \(b_w=0\).  In particular the sum
of the \(b\)-coefficients over all contacts is \(e_jd\).  In the
unramified connected-cover subcase there is exactly one contact over
each infinity end and both local degrees equal \(e_j\).

The component defect identity and adjunction give
\[
H_j^2=\sum_{w\in\partial H_j}\sigma_w
\tag{8}
\]
and
\[
\sum_{w\in\partial H_j}r_w
=2g_j-2-H_j^2+3e_jd.
\tag{9}
\]
Substituting (3)--(4), (7), and (8) into (9) cancels all degree terms:
\[
\boxed{\qquad
\sum_{w\in\partial H_j}(a_w+\sigma_w)
=2g_j+s_j-2\ge0.
\qquad}
\tag{10}
\]
Thus the natural endpoint charge
\[
\kappa_i=a_i+\sigma_i
\tag{11}
\]
has nonnegative total on every residual component.  In the
unramified \(\mathbf G_m\)-cover subcase \(g_j=0,s_j=2\), the two
charges are paired with exact opposite values.  The conductor has the
same equality-zero identity,
because
\[
a_\alpha+a_\beta=q,\qquad
\sigma_\alpha+\sigma_\beta=-q.
\tag{12}
\]

Summing (7) and (10) over the residual components gives the global
necessary identities
\[
\sum_i b_i z_i^{\mathrm{res}}=d(n-2\delta),
\qquad
\sum_i\kappa_i z_i^{\mathrm{res}}
=\sum_j(2g_j+s_j-2)\ge0,
\tag{13}
\]
where separated incidence counts every endpoint once.  The first is
the cover-degree projection formula; the second is the new charge
inequality.

These equations constrain *where* the negative Green mass can end: an
endpoint with negative \(\kappa\) requires enough positive charge on
the other contacts.  They do not bound how many disjoint residual
components can use the same boundary curve at distinct points.

## 2. Hodge and normal-ramification inequalities

For each residual component, the Hodge index theorem gives
\[
\boxed{\qquad
H_j^2\le\frac{(e_jd)^2}{n}.
\qquad}
\tag{14}
\]
Equation (9) and effectivity of ramification also give
\[
H_j^2\le2g_j-2+3e_jd.
\tag{15}
\]

There is a useful local interpretation of (9).  The compactified cover
\(H_j\to\overline\Gamma^\nu\simeq\mathbf P^1\) has total tangential
ramification
\[
2g_j-2+2e_j
\]
by Riemann--Hurwitz; all of it is supported at boundary contacts
because the affine restriction is étale.  The remaining part of
\(\sum_{w\in\partial H_j}r_w\) is the zero degree of the induced
normal-bundle map.  Its degree is
\[
\left(\sum_{w\in\partial H_j}r_w\right)
-(2g_j-2+2e_j)
=-H_j^2+e_j(3d-2)\ge0.
\tag{16}
\]
This strengthens (15), but gives no upper bound on the number of
different components meeting the same boundary divisor at different
points.  Explicitly, (16) is the genus-independent inequality
\[
H_j^2\le e_j(3d-2).
\tag{16a}
\]
Thus Riemann--Hurwitz does not by itself imply (2).

## 3. Why the original four-vertex ledger is not geometric

Use the four-vertex cluster of
`FIXED_PLANE_DEFECT_GREEN_FUNCTION.md`, ordered
\((E_0,E_1,E_2,E_3)\):
\[
b=(2,1,2,1),\qquad
\sigma=(2,-1,1,1),
\tag{17}
\]
with augmented-canonical labels
\[
a=(-2,-1,-3,-2).
\tag{18}
\]
The final curve \(E_3\) is type \(1\).  Since a type-\(1\) divisor is
not a component of \(G\), \(\eta_3=0\), and hence
\[
\sigma_3=db_3=d.
\tag{19}
\]
But (17) gives \(\sigma_3=b_3=1\), so \(d=1\).

On the other hand, a degree-one plane curve is a line and its smooth
affine part has at most one puncture.  It cannot be isomorphic to
\(\mathbf G_m\), whose smooth completion has two punctures.  Therefore
\[
\boxed{\text{the original four-vertex counterledger cannot occur in
the fixed-plane setting.}}
\tag{20}
\]
This is a genuine correction to the local stress test, not a global
contradiction.

## 4. The smallest component-level repair

The obstruction (20) does not extend to a universal Green bound.
The smallest repair has
\[
d=2,\qquad n=6,\qquad\delta=1.
\tag{21}
\]
Take \(\Gamma\) to have two simple infinity ends, so
\[
\ell_+=\ell_-=1.
\tag{22}
\]

Keep the same blowup graph, labels, and pullback-line vector as in
(17)--(18), but replace the defect and vertical multiplicity by
\[
\sigma=(3,-1,2,2),\qquad
\eta=2b-\sigma=(1,3,2,0).
\tag{23}
\]
On the three new exceptional rows,
\[
Qb=(0,0,1),\qquad
Q\sigma=(4,0,0).
\tag{24}
\]
Thus the sole final curve \(E_3\) is still type \(1\), while
\[
\boxed{\sigma_1=-1}
\tag{25}
\]
and four residual endpoints meet \(E_1\).
The number four is minimal in this cluster: type \(1\) forces
\(\sigma_3=d=2\), the final row forces \(\sigma_2=2\), and an integral
negative \(\sigma_1\) makes
\[
z_1=-2\sigma_1+\sigma_2\ge4.
\tag{26}
\]

Introduce a remote point-mapping endpoint \(F\) with
\[
(a_F,b_F,\sigma_F,\eta_F,r_F)=(1,1,1,1,3).
\tag{27}
\]
At the local endpoint \(E_1\),
\[
(a_1,b_1,\sigma_1,\eta_1,r_1)=(-1,1,-1,3,1).
\tag{28}
\]
Take the unramified \(\mathbf G_m\)-cover subcase
\((g_j,s_j)=(0,2)\), with no extra punctures, and four pairwise
disjoint degree-one residual components
\[
H_1,\ldots,H_4,
\]
each meeting \(E_1\) and \(F\) transversely at distinct points.  For
every \(H_j\), equations (7)--(10), (14)--(16) hold exactly:
\[
\begin{aligned}
P\cdot H_j&=1+1=2=e_jd,\\
H_j^2&=-1+1=0,\\
G\cdot H_j&=e_jd^2=4,\\
R\cdot H_j&=1+3=4
            =-2-H_j^2+3e_jd,\\
\kappa_1+\kappa_F&=(-2)+2=0.
\end{aligned}
\tag{29}
\]
The normal-map zero degree in (16) is \(4\), split as \(1+3\) at the
two ends.

The cover degree is also exact:
\[
2\delta+\sum_{j=1}^4e_j=2+4=6=n.
\tag{30}
\]
For completeness, a numerical conductor with \(q=0\) can have two
endpoints
\[
(a,b,\sigma,\eta,r)=(0,2,0,4,5).
\tag{31}
\]
They give
\[
P\cdot C=4,\quad C^2=0,\quad
G\cdot C=8,\quad R\cdot C=10,
\tag{32}
\]
exactly as required for \((d,\delta,q)=(2,1,0)\).

The four \(H_j\) with square zero are compatible with the Hodge index
theorem: disjoint fibers of a ruling are numerically equivalent, and
\((P\cdot H_j)^2=4\) does not contradict \(P^2=6\) when
\(H_j^2=0\).  Thus neither adjunction nor Hodge index removes this
component ledger.

## 5. Exact conclusion

The endpoint laws (7) and (10) are new global necessary conditions.
They exclude the original \(d=1\) local counterledger and should be
imposed in every future compactification search.  Equation (10) is an
inequality rather than an equality when a residual component has
positive genus or extra punctures over finite nonproper values.

The repaired ledger is deliberately only a **component-level
counterledger**.  It does not provide the unspecified old attachment
rows, a complete blowup tree, two global sections defining a morphism,
or an actual Keller map.  It proves the narrower negative statement:

> Riemann--Hurwitz, component adjunction, projection formula, effective
> ramification, cover degree, and Hodge index still do not imply the
> desired Green-potential inequality (2).

The next promising target is therefore local-to-global compatibility of
the **normal maps** at all boundary crossings, together with Keller
finality.  Degree (16) records only the total number of their zeros; it
does not enforce that the local normal maps glue to the two global
sections of \(dP\).

The exact endpoint, component, conductor, and minimality calculations
are checked in `verify_fixed_plane_component_endpoint_pairing.py`.
