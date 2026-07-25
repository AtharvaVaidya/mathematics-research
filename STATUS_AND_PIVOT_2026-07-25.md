# Status and strategic pivot

Date: 25 July 2026

## Executive verdict

The plane Jacobian conjecture is not resolved in this archive.

There is, however, now a publishable bounded theorem.  Subject to the
public preprint reductions of Guccione--Guccione--Horruitiner--Valqui
(GGHV), a
hypothetical characteristic-zero plane Keller counterexample satisfies

\[
\boxed{\max(\deg P,\deg Q)\ge125.}
\]

The proof has two new parts:

1. an all-scale theorem excluding the complete consecutive \((2,3)\)
   five-block family, which covers GGHV Proposition 4.3(2); and
2. an exact computer-assisted elimination of the full case-c coefficient
   system in Proposition 4.3(1).

An independent announcement of the same numerical bound exists.  No
priority or uniqueness claim is made here.

The broader search has also reached a useful negative conclusion: every
one-boundary triangular toroidal/Rees descent has now been classified and
excluded.  Continuing to vary a single Rees weight is therefore not a
promising path to \(JC(2)\).  The next structural target must use at least
two boundary valuations, or an equivalent global monodromy/divisor
invariance theorem.

## 1. What is proved

### 1.1 All-scale five-block obstruction

`current_context/ALLSCALE_MARKED_CUSP_OBSTRUCTION.md` proves that no
genuine consecutive \((2,3)\) five-block completion with the required
vertices and fixed poles exists, at any radial scale.

The proof is structural rather than a scale-by-scale Gröbner search.  Its
key ingredients are:

- the universal deficit-one kernel;
- a completed-square root-consumption lemma;
- an exact multiplicity budget on the marked boundary normalization;
- the equality-case obstruction; and
- exhaustive horizontal, vertical, and ramified-multisection charts.

The exact \((3,4)\) local countermodel in
`current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md` shows
that this mechanism is genuinely special to transverse degree two.

### 1.2 Exact elimination of GGHV case c

`current_context/CASE_C_FULL_CERTIFICATE_BRIDGE.md` records the complete
dependency chain.

The exact support audit starts with all lattice points of

\[
\begin{aligned}
\Delta_P&=\operatorname{conv}
\{(0,0),(1,0),(8,14),(8,16),(0,8)\},\\
\Delta_Q&=\operatorname{conv}
\{(0,0),(2,1),(12,21),(12,24),(0,12)\}.
\end{aligned}
\]

The unimodular change \(z=xy,\ h=xy^2\) gives 61 \(P\)-positions and
125 \(Q\)-positions, with no loss of a support condition.  The outer
equation

\[
UV+2hUV'-3hU'V=1,\qquad \deg U=7,\quad\deg V=10,
\]

has five normalized Hurwitz covers.  Exact descending row reduction
parametrizes all 165 lower nonconstant coefficients by seven modes of
weights

\[
(1,1,2,2,3,3,4),
\]

and retains every cokernel row.

Over the two rational and one cubic factors above \(32003\), the rows
through deficit eight contain \(X_i^{32}\) for every mode.  Thus the
original-row weighted-projective special fiber is empty.  Independently,
the exact characteristic-zero square identity and every substituted
square-branch row reduce coefficient-for-coefficient to a complete empty
four-chart special fiber.  Properness of that complete
weighted-projective square-branch family—not of one affine chart—then
proves that the characteristic-zero generic fiber is empty.

One important audit correction was made before declaring the result
closed.  The required vertices \((0,8)\) and \((0,12)\) occur at radial
deficits ten and fifteen, not deficits two and three.  The exact kernel
sequence

\[
(2,2,2,1,0,\ldots,0)
\]

shows that the seven-mode origin propagates uniquely to zero through all
later blocks, so both required late vertices vanish there.  The cone
origin is therefore not a genuine case-c point.

### 1.3 Global Darboux divisor criterion

For a reciprocal endpoint pair, put

\[
S=\Xi^5,\qquad Y=T^{5m+2},\qquad J=SY=\frac{Z^5}{W^2}.
\]

`current_context/RECIPROCAL_DARBOUX_LIOUVILLE_AUDIT.md` proves that
descent of any one of \(S,Y,J\) is equivalent to descent of the complete
comparison branch.  The new global theorem in
`current_context/GLOBAL_DARBOUX_DIVISOR_SECTION_AUDIT.md` sharpens this:
invariance under the normal-closure Galois action of the complete
principal divisor of any one of \(S,Y,J\) forces full descent.

Divisor divisibility alone is automatic and carries no such information.
An exact constant target-translation model retains the genuine endpoint,
the symplectic equation, polynomial support containment, and the
normalized infinity sheet while keeping the branch nonrational.  It
omits the forced inner vertices.  This isolates the precise missing
input as a global boundary-orbit statement, rather than another local
Wronskian calculation.

The natural two-boundary strengthening has now also been stress-tested.
Even normalized identity behavior to arbitrarily high order at two
adjacent toric divisors does not force invariance of
\(\operatorname{div}(J)\): an exact affine-symplectic endpoint
deformation retains polynomial support and a full lower transverse block
while hidden cusp-orbit monodromy remains elsewhere.  Two boundary orders
become sufficient only after a separate theorem proves
\[
\operatorname{Supp}\operatorname{div}(\sigma J/J)
\subseteq D_1\cup D_2
\]
for every conjugate.  The exact forced GGHV cap vertices are not present
in the countermodel and remain the plausible mechanism for this support
exhaustion.  See
`current_context/TWO_BOUNDARY_DIVISOR_ORBIT_AUDIT.md`.

A second stress test now imposes the actual case-c polygons, every
vertex, the genuine outer Wronskian pair, and both forced cap-face
factorizations of multiplicities \((2,3)\) and \((8,12)\).  Generic
interior coefficients give toric degree
\[
141-2-8=131,
\]
while the endpoint map has degree \(21\).  Rational comparison would
force \(21\mid131\), so divisor invariance still fails.  This model
cannot satisfy the bracket—the case-c bracket scheme is empty—but it
proves that exact cap faces and principal-divisor intersections alone do
not yield support exhaustion.  The next usable input must be the
bracket-controlled successive jets above the cap roots.  See
`current_context/CASE_C_CAP_SUPPORT_EXHAUSTION_NO_GO.md`.

Those successive jets now have a general, finite invariant.  In any
boundary chart \(P=u^{-p}F,\ Q=u^{-q}G\), restriction of the monomial
bracket equation to a Puiseux branch of \(F=0\) becomes a first-order
Euler equation for \(G/u^q\).  It forces every nonresonant jet, leaves
one constant per irreducible branch factor, and imposes a no-log residue
condition.  For the vertical case-c cap this forbids same-color contact
sums \(5\) and \(9\); for the diagonal cap it forbids \(10\) and \(14\).
The exact trace equation glues conjugate leaves but retains a homogeneous
constant, so this is not yet a global contradiction.  See
`current_context/CAP_PUISEUX_EULER_JET_INVARIANT.md`.

This local program is now closed sharply.  The vertical and diagonal caps
have unique minimum-height resonant stars, at contacts \(4\) and \(1\).
They avoid every forbidden residue order, retain resultant orders \(24\)
and \(96\), and lift recursively to exact formal solutions of the full
local bracket.  These formal series need not terminate inside the finite
case-c polygons.  Thus the missing input is not a deeper local jet: it is
finite global support termination or a relation between the two resonant
constants through the common outer Hurwitz cover.  See
`current_context/CASE_C_CAP_RESONANT_STAR_NO_GO.md`.

The first attempted realization of that cross-cap relation has also been
closed.  The tempting \(2/3\) ordinary-Jacobian conormal truncation is not
the case-c diagonal system: the complete chart has eleven \(P\)-layers,
sixteen \(Q\)-layers, and an Euler bracket.  At deficit four the omitted
tail is nonzero and cancels the retained middle term exactly on a
certified square-branch point.  Its remainder is nonzero modulo the outer
quartic, so the truncated quotient and its discriminant cannot be
identified with the canonical radial obstruction.  See
`current_context/CASE_C_CONORMAL_TRUNCATION_NO_GO.md`.

The outer quartic itself now has an exact geometric interpretation.  Its
four roots are the four simple, unramified residual points in the
degree-\(21\) fiber with local monodromy \((17)(1^4)\), not unused branch
points.  Consequently an equivariant injection of the eight or twelve
cap leaves into the outer sheets would be impossible, but no such
leaf-to-sheet map is currently known.  A simultaneous formal
\((8,12)\) cap over the quartic incidence algebra proves that the four
valuations and all completed local jets are compatible.  See
`current_context/CASE_C_OUTER_QUARTIC_INCIDENCE_NO_GO.md`.

There is a stronger representative-independent no-go.  At deficits four
and five the complete new-block operators have two-dimensional cokernels,
but their reductions are surjective onto \(K[w]/(E)\) and
\(K[w]/(E^2)\), respectively, over both rational and the cubic outer
factors modulo \(32003\).  Raw quartic remainder can therefore be changed
arbitrarily without changing the full solvability problem and is not a
cokernel invariant.  See
`current_context/CASE_C_OUTER_QUARTIC_COKERNEL_NO_GO.md`.

### 1.4 Pseudo-plane function-field degree

For the Route A quadratic pseudo-plane
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),
\]
there is a new global normalization theorem.  More generally, let
\(S=\operatorname {Spec}B\) be a normal integral affine complex surface
with \(B^\times=\mathbf C^\times\).  If an étale map
\(S\to\mathbf A^2\) has finite function-field extension, that extension
cannot be nontrivial and Galois.  Indeed, its finite normalization must
have a branch divisor by purity and
\(\pi_1^{\mathrm{et}}(\mathbf A^2)=1\); Galois symmetry makes every prime
above that divisor ramified and hence absent from \(S\), forcing the
branch equation to pull back to a nonconstant unit.

Every quadratic extension in characteristic zero is Galois, so a Route A
Darboux pair cannot have generic degree \(2\).  This is a rigorous
all-coefficient obstruction, not a bounded search.  See
`current_context/ROUTE_A_QUADRATIC_DEGREE_EXCLUSION.md`.

The first surviving degree, \(3\), is now sharply constrained rather than
excluded.  It must have \(S_3\) closure.  Above every branch component,
\[
\operatorname {div}_Y(f)=2E+C,
\]
where the ramified double sheet \(E\) is omitted and the unramified sheet
\(C\) is retained as a principal divisor on \(S\).  Since
\(\operatorname {Cl}(B)\simeq\mathbf Z/2\), neither distinguished
nonprincipal boundary curve can be \(C\), and the mandatory collision
curve is not a branch component.  The exact model
\[
(s,t)\longmapsto(s,t^3-3st)
\]
realizes the same \(2+1\) branch pattern after deleting its ramification
curve, while \(V(u-1)\subset S\) supplies an internal class-zero prime.
Thus cubic ramification, the class group, and the symplectic form alone
do not contradict one another.  See
`current_context/ROUTE_A_CUBIC_BRANCH_SECTION_AUDIT.md`.

### 1.5 Fixed-plane Green formula

For the fixed-source-plane construction, the global pullback equations
give the defect

\[
\sigma=db-\eta,\qquad Q\sigma=z.
\]

On every connected point-mapping component \(S\),

\[
\sigma_S=A_S^{-1}V\sigma_D-A_S^{-1}z_S,
\qquad A_S=-Q_S,\qquad A_S^{-1}>0.
\]

The conductor endpoints satisfy

\[
\sigma_\alpha+\sigma_\beta=-q.
\]

These are exact global identities.  They rule out every exceptional cap
retaining the current 19-vertex core.  A small finality-compatible local
counterledger shows that the identities alone do not imply nonnegative
point defect.  The residual endpoint-charge law
\[
\sum_{w\in\partial H}(a_w+\sigma_w)=2g(H)+s(H)-2
\]
rules out that first local stress test as non-geometric.  An exact
degree-two component-level repair still satisfies projection formula,
adjunction, Riemann--Hurwitz, Hodge index, ramification, conductor, and
cover degree while retaining a negative point defect under those summed
tests.

That repair is now also ruled out by the missing pointwise constraint.
If
\[
\omega_\Gamma=\operatorname{Res}_\Gamma
\frac{dU\wedge dV}{F}
=\lambda s^j\,\frac{ds}{s},
\]
then every residual contact has normalized endpoint charge
\(\kappa/e_w=j\) over \(s=0\) and \(-j\) over \(s=\infty\).
Simple conic ends have \(j=0\), whereas the repaired ledger assigned
opposite nonzero charges.  A resolved-target valuation formula extends
the law to singular ends and also excludes the old degree-nine numerical
witness for its particular displayed Laurent target.  This is not yet a
global exclusion for every target embedding.  See
`current_context/FIXED_PLANE_NORMAL_MAP_GLUING.md`.

The remaining target exponent has now been classified rather than
searched.  If the conductor cover is
\(s=\alpha c^{\epsilon\delta}\), the residual pullback unit is
\(H|_C=\lambda v^m\), and
\[
\omega_\Gamma=\lambda_0s^j\,\frac{ds}{s},
\]
then
\[
m=-1-2\epsilon\delta j.
\]
This sharpens the earlier congruence but does not force \(j=0\).  The
quartic
\[
(3XY+1)^2-X=0,\qquad
X=s^2,\quad Y=-\frac{s^{-1}+s^{-2}}3
\]
is a smooth \(\mathbf G_m\) with
\(\operatorname {Res}(X\,dY)=2/3\), \(j=-1\), and exactly the
\((2,5)\), \((2,3)\) target ends.  Its target-resolution triples are
\((2,10,6)\) and \((2,6,4)\), and they give the paired conductor charges
\(-2,2\).  Exact local lift and Green rows show that final type-\(1\)
values do not by themselves contradict those charges.  This is a sharp
countermodel to the proposed inference, not a global Darboux pair or
Keller map.  See
`current_context/FIXED_PLANE_RESIDUE_EXPONENT_CLASSIFICATION.md`.

Global endpoint pairing is also insufficient at the divisor/valuation
level.  The smooth degree-nine target
\[
X=s^{-2}+\frac23s^{-1},\qquad Y=s+X^4
\]
has residue \(2/3\), \(j=-1\), resolved endpoint triples
\((8,72,22)\) and \((1,7,1)\), and realizes all four normal-map contacts
of the existing 19-vertex ledger simultaneously.  The same ledger still
fails precisely on six final point-mapping curves and has no realized
global sections or morphism.  See
`current_context/FIXED_PLANE_GLOBAL_ENDPOINT_NORMAL_COUNTERMODEL.md`.

Finally, the proposed nonproper-value degree/genus inequality collapses
to an identity: finite endpoint charge equals missing-sheet
Euler/Riemann--Hurwitz loss, componentwise and globally.  A fixed-source
Hermite-CRT construction realizes the conductor, one residual sheet, the
odd normal coefficient \(v/18\), and \(\operatorname{Jac}(U,V)=1\) to
first order along their union.  It does not extend to a global Keller
pair.  This isolates higher-order Keller integrability, section
realization, and minimal-resolution finality as the remaining sources of
rigidity; see
`current_context/FIXED_PLANE_SHEET_LOSS_AND_FIRST_ORDER_CRT.md`.

## 2. What the audit disproved

Several attractive shortcuts are now known to be false.

- Local Wronskian, Liouville, and valuation data do not force global
  comparison-branch descent.
- Boundary contraction and a finite-flat Rees comparison do not force
  membership in \(k[x,x^r y]\).
- Post-resolution blowups cannot repair a bad final point-mapping curve.
- Scalar pullback, ramification, adjunction, and effectivity equations
  alone do not contradict one another.
- A universal nonnegative-defect principle on point-mapping subtrees is
  false.
- The transverse \((2,3)\) root-consumption argument does not extend to
  \((3,4)\).
- All local Puiseux cap jets can coexist in exact formal bracket germs.
- The \(2/3\) conormal truncation omits essential case-c Laurent tails,
  and raw remainder modulo the outer quartic is not a full-system
  invariant.
- The four outer-quartic points are unramified incidence sheets, not an
  additional Riemann--Hurwitz obstruction.
- Galois normalization excludes Route A degree \(2\), but the required
  non-Galois cubic \(2+1\) branch geometry is locally consistent.
- Global endpoint pairing and sheet-loss counts add no contradiction
  before finality or section realization is imposed.

These countermodels are not failed proof attempts to hide; they delimit
the hypotheses of the valid theorems.

## 3. The one-boundary degree-lowering route is closed

`current_context/TOROIDAL_DEGREE_DESCENT_NO_GO.md` classifies every
dominant triangular polynomial chart whose Jacobian absorbs
\(\kappa x^r\).  After affine normalization it is

\[
u=x^a,\qquad v=x^{r+1-a}y+f(x),\qquad 1\le a\le r+1.
\]

Finite iterations collapse to the same form.  Membership of \(P,Q\) in
this chart algebra gives a genuine constant-Jacobian descent.  For a
minimal-function-field-degree counterexample, every finite case \(a>1\)
is excluded by degree reduction and the classical Galois case of the
Jacobian conjecture.

More decisively, the required GGHV top vertex \((8,16)\) violates the
exact leading-coefficient semigroup condition for all three \(r=2\)
possibilities \(a=1,2,3\).  Normalizing the chart algebra does not help:
it leaves a residual Jacobian \(x^{a-1}\), and an exact family of
unbounded field degree realizes this failure.

This rules out further searches based only on changing a single Rees
weight, adding a cyclic cover, translating its center, or iterating those
operations.

## 4. Strategic pivot

The best remaining direction is now a finite-global-support or
minimality theorem, not another local boundary identity.

One concrete formulation is:

> Compare the two resonant formal cap solutions through the common outer
> Hurwitz cover and prove that they cannot both terminate at the exact
> global Newton-support cutoffs.

By the divisor-invariance theorem, this would give full field descent.
Unlike one-boundary Rees membership or a local contact tree, this can see
both caps and the finite polynomial cutoff simultaneously.  The raw
outer-quartic remainder is now known not to descend through the full
new-block quotient.  The viable small target is instead a genuine
monodromy-equivariant incidence correspondence from cap leaves to outer
sheets, or an adjoint/transvectant of the full cokernel that constructs
such a correspondence.

The fixed-plane analogue is:

> Promote the target-determined endpoint charges and Green potential to
> an actual minimal-resolution section theorem, or derive a second-order
> obstruction to extending the first-order Hermite-CRT Keller jet.

The two formulations share the same geometry: all local and divisor-level
constraints can be satisfied, but finite global realization may fail at
termination, finality, or higher-order integrability.

The research program should therefore prioritize:

1. a global leaf-to-sheet incidence theorem through the common outer
   Hurwitz cover, rather than raw quartic divisibility;
2. the Route A non-Galois cubic, especially the interaction between its
   principal retained branch sections and the distinguished
   \(\mathbf Z/2\) boundary class;
3. minimal-resolution finality coupled to actual polynomial sections;
4. second-order extension of the fixed-source Hermite-CRT Keller jet; and
5. exact countermodels whenever a proposed global inequality is too weak.

It should not return to unrestricted coefficient brute force except for
small, theorem-driven certificate targets.

## 5. Publication state

The bounded degree-\(125\) theorem is mathematically closed under its
stated public preprint inputs and standard exact-CAS trust assumptions.
The publication bundle now includes a cache-free clean-room replay,
archived stdout/software versions, and SHA-256 hashes.  Submission
readiness still requires:

- independent human checking of the GGHV implication chain; and
- editorial compression into a conventional paper.

Those are reproducibility and exposition tasks, not missing mathematical
lemmas for the bounded theorem.  They do not change the central status:
\(JC(2)\) remains open.
