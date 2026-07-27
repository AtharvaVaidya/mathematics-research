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

Two independent construction-first results have also reached
preprint-level form.  First, there is no degree-three étale morphism
\(S(2,2,1)\to\mathbb A^2\).  Second, in the Gallagher weighted-lift
graph family,
\[
\boxed{
\deg_{A,B,C}Q\le8,\quad Q\notin\mathbb C
\ \Longrightarrow\
J(U+R_{\le2},Q)\notin\mathbb C^\times
}
\]
for every polynomial graph.  The latter is a fully nonhomogeneous
target theorem; its first possible Newton cancellation is the sharp
degree-nine cusp pair \(A^5C^4,B^6\).  Neither statement resolves the
plane conjecture, and both still require independent human review
before journal submission.

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
points.  The natural face correspondence does not inject eight or twelve
cap leaves into them.  Writing the diagonal face as
\[
\overline P=a\eta^8=aH^2,\qquad
\overline Q=b\eta^{12}=bH^3,\qquad H=\eta^4,
\]
shows that its common normalized cover has degree four.  This is exactly
compatible with the four residual sheets.  It is not canonically
projectively identical to them either: the Kummer fiber has
binary-quartic invariant \(J=0\), while all five certified outer
quartics have \(J\ne0\) at the good prime.  A simultaneous formal
\((8,12)\) cap over the quartic incidence algebra proves that the four
valuations and all completed local jets are compatible.  See
`current_context/CASE_C_OUTER_QUARTIC_INCIDENCE_NO_GO.md`.
The correction and its general multiplicity-gcd rule are in
`current_context/CASE_C_DEGREE_FOUR_INCIDENCE_AUDIT.md`.

There is a stronger representative-independent no-go.  At deficits four
and five the complete new-block operators have two-dimensional cokernels,
but their reductions are surjective onto \(K[w]/(E)\) and
\(K[w]/(E^2)\), respectively, over both rational and the cubic outer
factors modulo \(32003\).  Raw quartic remainder can therefore be changed
arbitrarily without changing the full solvability problem and is not a
cokernel invariant.  See
`current_context/CASE_C_OUTER_QUARTIC_COKERNEL_NO_GO.md`.
The stronger terminal-adjoint audit is also negative: each new-block
operator is surjective modulo \(E^j\) for \(j=1,2,3,4\), so no
distribution on the four roots using derivatives through order three
annihilates it.  Modulo \(E^5\), Hermite coordinates simply recover the
old bounded row cokernels.  The unique linear adjoint common to both
images is \([h^{19}]\), the outer-independent support ceiling.  Hence a
scalar transvectant with \(E\) cannot be the missing cap coupling; see
`current_context/CASE_C_OUTER_QUARTIC_ADJOINT_NO_GO.md`.
The first nonlinear continuation has also been exhausted.  The
degree-filtered residual adjoints have nonzero individual norms, nonzero
trace-Gram determinant, and nonzero Wronskian norm at every outer point.
The weight-nine determinant of their complete source cokernel vectors is
a nonzero 76-term polynomial rather than an identity.  Thus the first
resultant, norm, bilinear, tangency, and determinant constructions from
the two cokernel planes do not couple the caps; see
`current_context/CASE_C_COKERNEL_NONLINEAR_PAIRING_NO_GO.md`.
The later finite-support complex does contain a canonical obstruction.
For \(4\le d\le15\),
\[
\operatorname {rank}(L_d\bmod E^j)=\min(4j,r_d),
\]
with
\((r_4,\ldots,r_{15})=(18,17,15,13,11,9,7,5,4,3,2,1)\).
The centered deficit-\(4,5,6\) residual adjoints have nonzero
three-stage trace-Gram determinant and already span the trace-zero
quartic algebra, closing another abstract-degeneracy shortcut.  At
deficit eight, the unique adjoint modulo \(E^3\) instead evaluates on
the pure weight-four branch as
\[
C_8X_6^2,\qquad \operatorname {Nm}(C_8)=-9989\ne0\pmod {32003}.
\]
It therefore forces \(X_6=0\), intrinsically compressing the five old
deficit-eight special-chart rows to one terminal scalar.  This closes
the deepest branch structurally but does not replace the generic-chart
certificates.  See
`current_context/CASE_C_MULTISTAGE_JET_STAIRCASE.md`.

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

The finite cubic normalization is automatically flat of rank three, but
its canonical class need not be trivial even though the open pseudoplane
has a nowhere-vanishing symplectic form.  Hence a non-Gorenstein fiber is
not forced.  Miranda's presentation does show that such a fiber, if it
occurs, is the length-three algebra
\(\mathbb C[z,w]/(z,w)^2\), is an isolated singular point, and forces
branch multiplicity at least four.  The normal twisted-cubic cone is an
exact \(S_3\) countermodel, so these facts do not exclude the Gorenstein
case or cubicity itself.  See
`current_context/ROUTE_A_FINITE_FLAT_TRIPLE_NON_GORENSTEIN_AUDIT.md`.

There is nevertheless a new global incidence theorem.  The distinguished
line \(D\simeq\mathbb A^1\) maps finitely and surjectively onto its
collision image \(\Gamma_D\).  Therefore \(\Gamma_D\) avoids every
non-Gorenstein value.  Every self-identification of \(D\) over
\(\Gamma_D\) is disjoint from the branch curve and contains at most
three retained points.  After base change to \(D\), the cubic algebra
splits as
\[
\mathbb C[v]\times
\mathbb C[v,\tau]/(\tau^2-g(v)),
\]
and the restricted discriminant is \(c\,g(v)\).  The problem has thus
been reduced along this curve to a single residual quadratic cover.
An exact nodal cubic model realizes the splitting and shows that the
incidence theorem alone is not contradictory.  See
`current_context/ROUTE_A_NON_GORENSTEIN_GAMMA_D_INCIDENCE.md`.

The extreme-weight audit gives a complementary algebraic target.  In
\(\mathbb C(s,w)\), \(s=uv\),
\[
\{w^af(s),w^bg(s)\}
=w^{a+b+1}(bf'g-afg').
\]
After reversible target shears are removed, every surviving cubic extreme
must be a triangularly irreducible cusp with coprime exponents at least
two.  In the resonant invariant family, the degree-three field ledger
forces the unique boundary seed \(P=w,\ Q=-v(1+2uv)\), whose bracket is
\(1+6uv+6u^2v^2\), not \(1\).  Formal linear corrections exist, but
polynomial termination must mix hyperbolic weights.  See
`current_context/ROUTE_A_CUBIC_EXTREME_WEIGHT_VALUATION_AUDIT.md` and
`current_context/ROUTE_A_CUBIC_DH_SEED_LINEARIZATION.md`.

The degree-six plane lift supplies an exact nonproper component:
the rational deck involution sends points tending to infinity onto
the distinguished line image \(\Gamma\).  Its Newton--Puiseux class,
however, is
\[
(m_\varphi,n_\varphi,i_\varphi)=(2,5,1),
\]
not index two.  Chau's degree-ratio theorem and the invariant filtration
give \(d_1/d_2=m_1/m_2\) and \(d_i\ge4m_i\), but \(d_i\) are total
coordinate degrees rather than geometric degree six.  The exact
dicritical chart has nonzero constant Jacobian and remains unramified at
the forced node.  In the exact geometric-degree defect formula this
class contributes \(1\), leaving defect \(4\) for the other mandatory
dicritical classes, compatibly with
\(6-1=(2-1)+2(3-1)\).  Thus no index or degree-six contradiction follows;
see `current_context/ROUTE_A_SINGULAR_DICRITICAL_INDEX_AUDIT.md`.

The invariant degree estimate behind this calculation is itself sharp.
If \(m=\deg_bH_i(0,b)\), then \(\deg H_i\ge4m\), and equality forces the
distinguished Laurent block to be exactly a multiple of \(v^m\).
For both coordinates the degree-ratio theorem yields only a common
factor inequality \(K\ge4M\).  The top Keller dependence and the
boundary equation are compatible with equality, and an exact nodal
first-neighborhood model realizes all of these conditions while its
global Jacobian remains nonconstant.  Geometric degree six does not
bound raw coordinate degrees.  See
`current_context/ROUTE_A_INVARIANT_DEGREE_FILTRATION_SHARPNESS.md`.

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
The higher-order possibility is now settled in the constructive
direction: because \(\{U,DK\}\) is a unit modulo \(DK\), an explicit
Hensel recurrence lifts the jet through every finite power
\((DK)^N\).  No finite normal order can obstruct it.  The fixed
polynomial \(U_0\) nevertheless has fourteen distinct critical points,
all away from \(DK=0\), so no global polynomial \(V\) can satisfy
\(\{U_0,V\}=1\).  The sharper remaining question is critical-point
removal under \(U_0+(DK)^2\phi\), followed by algebraization; see
`current_context/FIXED_PLANE_ALL_ORDER_HERMITE_CRT_LIFT.md`.
That perturbative route is now constrained exactly.  The fourteen
critical points are Morse and persist uniquely under every formal
\(U_0+\epsilon(DK)^2\phi\).  For each degree bound, a dense open
subset of the full coefficient space retains a finite-étale
degree-\(14\) critical subscheme.  Any successful perturbation is
therefore exceptional and nonperturbative; the first scalar choice
\(U_0+(DK)^2\) instead has \(21\) distinct off-boundary critical
points.  See
`current_context/FIXED_PLANE_CRITICAL_PERSISTENCE_AND_SCALAR_PERTURBATION.md`.

The proposed rational residue-parity quantization is false as stated.
Canonical scalings \(U=Af(AB), V=B/f(AB)\) can be chosen to be the
identity on the conductor, add zero residue at the distinguished
infinity endpoint, and preserve the Darboux equation, while introducing
either fractional residues or new integral odd classes on interior level
divisors.  They necessarily introduce affine poles and are not polynomial
Keller pairs.  Thus the useful missing hypothesis is global pole-freeness
or finite polynomial termination, not endpoint parity.  See
`current_context/FIXED_PLANE_RESIDUE_PARITY_SCALING_NO_GO.md`.

### 1.6 Three-dimensional descent closures

For the July 2026 cubic Keller map in dimension three, any common
coordinate \(R\) with \(R\circ F\) also a source coordinate would
rectify the map to \((t,p,q)\).  Generic \(t=c\) slices would then be
plane Keller maps of geometric degree three.  Orevkov's theorem forbids
such maps.  This closes every common-coordinate descent, including wild
nonlinear coordinates.  The natural \(A\)- and \(B\)-fibers are not
affine planes either.  See
`current_context/THREE_DIMENSIONAL_COORDINATE_SLICE_OREVKOV_NO_GO.md`.

The generic-degree-six weighted lift supplies a genuinely different
test, and its first broad descent class is now closed without coefficient
search.  For every polynomial graph \(z=g(x,y)\) and every rank-two
linear target projection, the restricted Jacobian is a linear
combination of the three target minors.  On a graph of degree \(m\ge1\),
their nonzero top degrees are
\[
33+8m,\qquad 19+5m,\qquad 18+5m,
\]
so their coefficients vanish successively if the combination is
constant.  Constant graphs have the same separation \(33,19,18\).
An exact interpolation graph contains all six rational collision points,
so the obstruction is nonvacuous.  The leading-form proof extends to
every weighted lift on every nonconstant polynomial graph.  See
`current_context/WEIGHTED_LIFT_DEGREE_SIX_GRAPH_PROJECTION_NO_GO.md`.

The first nonlinear target cancellation is now sharply reduced as well.
The primitive toric relation is
\[
E=p_5^6A^5C^4-q_6^5B^6,
\]
whose next form is a nonzero multiple of \(y^{29}C_0^{23}\).
Completing the first SAGBI slice produces a new generator with top
\(y^{25}C_0^{19}\); a second subduction exposes
\(x^{49}y^{20}g_m^{17}\).  Its Jacobian with \(C\) never vanishes.
With \(B\) or \(A\), even the top Jacobian can vanish only on the two
Newton rays
\[
\begin{aligned}
g_m&=c x^{8k+7}y^{5k+5},&m&=13k+12,\\
g_m&=c x^{4k-1}y^{11k+4},&m&=15k+3,\quad k\ge1.
\end{aligned}
\]
The \(B\)-ray is the solution set of an exact weighted-Euler equation
for the leading \(\gamma\), so its lower recursion is the next small
target.  See
`current_context/WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.

That lower recursion now closes both rays uniformly.  The \(B\)-ray
completes to \(c x^{3k+4}(1+xy)^{5k+5}\), but the fixed low part of
\(\gamma\) leaves the uncancellable defect
\((228/17)xy+1/34\) before a lower seed term can appear.  The \(A\)-ray
requires a nonzero \(x^1\)-term, while every graph contribution is
divisible by \(x^2\).  Therefore, for every linear correction \(L\),
the subduced coordinate \(U+L\) paired with \(A\), \(B\), or \(C\)
cannot give a plane Keller map on a nonconstant polynomial graph.
The full mixed linear pivot is excluded as well.  If the \(A\)
coefficient is nonzero, the coupled \(A/B\) characteristic equation
forces a highest-\(y\), \(x^1\) monomial whose coefficient is independent
of the mixing ratio.  If it vanishes, the \(B\)-defect occurs before a
\(C\)-term can enter; constant graphs have separated nonzero top forms.
Thus every pair \((U+L,\alpha A+\beta B+\delta C)\) fails on every
polynomial graph.  Genuinely nonlinear second coordinates remain outside
the theorem; see
`current_context/WEIGHTED_LIFT_SECOND_SUBDUCTION_RAY_CLOSURE.md` and
`current_context/WEIGHTED_LIFT_MIXED_LINEAR_PIVOT_CLOSURE.md`.
The nonlinear continuation classifies every homogeneous quadratic
face.  A single characteristic equation classifies the three
binary \(A/B\) faces; the new \(AB\) ray forces a forbidden
\(x^1\)-term.  Mixed \(AC/BC\) forces a negative infinity-chart power,
while \(BC\) has no resonance and \(C^2\) reduces to the linear
theorem.  The former pure-\(AC\) boundary proof was not exact: a lower
\(B\) term can occupy its first-lower sector.  Thus the
arbitrary-lower-tier quadratic claim remains open on \(AC+B\).  See
`current_context/WEIGHTED_LIFT_ALL_QUADRATIC_PIVOT_CLOSURE.md`.
The cubic master characteristic classifies all binary and
\(C\)-divisible faces; the descending, negative-tail, nonresonant, and
constant-graph certificates survive.  The former pure-\(ABC\)
boundary proof was not exact, and a lower \(B^2\) term can occupy its
first-lower sector.  Thus the arbitrary-lower-tier cubic claim remains
open on \(ABC+B^2\) and also inherits the lower quadratic
\(AC+B\) chain.  See
`current_context/WEIGHTED_LIFT_ALL_CUBIC_PIVOT_CLOSURE.md` and
`current_context/WEIGHTED_LIFT_QUADRATIC_CUBIC_LOWER_TIER_CORRECTION_AUDIT.md`.
The quartic face classification has nine integral rays.  Exact
coefficient recurrences close \(C^2Q_2\) and the close
\(A/B/C^4\) interleaving; on constant graphs the sole toric
degeneracy \(AB^3\) at \(z=0\) has a certified nonzero degree-\(134\)
next diagonal.  A correction audit found that the arbitrary-lower-tier
theorem remains incomplete on exactly two pure families:
\(AB^2C+B^3\) and \(A^2C^2+ABC\).  Their cubic coefficients can
cancel the first-lower pole, after which that Laurent-sector equation
is polynomially solvable.  See
`current_context/WEIGHTED_LIFT_ALL_QUARTIC_PURE_FACE_CORRECTION_AUDIT.md`.

The binary calculation now has an all-degree form:
\[
8nJ=(5n+17d)I+15d-5n.
\]
It closes every pure monomial face in every degree and every binary
target through degree five.  Its first honest mixed polynomial
completion occurs at \(n=6,d=1\), but the exact first lower-seed
recurrence closes that family with unavoidable residue
\[
-\frac{221578k+153403}{510}.
\]
Thus every homogeneous binary second coordinate through degree six is
closed.  See
`current_context/WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_REDUCTION.md`
and
`current_context/WEIGHTED_LIFT_DEGREE_SIX_EXCEPTIONAL_RECURRENCE_CLOSURE.md`.
The same lower recurrence is now closed uniformly for every
Newton-degree-one binary face
\[
B^{n-1}(\lambda A+\mu B),\qquad n\ge1,\quad\lambda\ne0.
\]
For every admissible source sector \(I\ge2\), the exact residue is
\[
-\frac{
2975In^2+952In-2023I-3035n^2+22780n-1785
}{2040n},
\]
whose numerator is strictly positive.  Since graph corrections enter
through \(x^2h\), none can alter this source-axis coefficient.  The
next unresolved binary class therefore has Newton degree \(d\ge2\).
See
`current_context/WEIGHTED_LIFT_ALL_DEGREE_D1_RECURRENCE_CLOSURE.md`.

The exact maximal-\(x\) filtration closes every remaining binary
characteristic, so every homogeneous \(Q_n(A,B)\) is excluded in all
degrees.  More strongly, a global source-boundary argument now closes
every nonzero homogeneous \(Q_n(A,B,C)\).  It selects the earliest face
of the entire target.  When the graph boundary is regular, exact seed
gaps isolate a nonzero Wronskian coefficient; when it has a pole,
cancellation at \(u=1\) contradicts the leading coefficient at
\(u=\infty\).  Thus
\[
\left(U+R_{\le1}(A,B,C),\,Q_n(A,B,C)+c\right)
\]
cannot have nonzero constant restricted Jacobian on any polynomial
graph.  Here \(R_{\le1}\) is affine and \(c\) is constant.  Arbitrary
lower-degree second-coordinate tiers are not included.  See
`current_context/WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md` and
`current_context/WEIGHTED_LIFT_GLOBAL_MINIMAL_BOUNDARY_FACE_CLOSURE.md`.

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
- The common \((8,12)\) cap normalization has degree four, so the natural
  incidence is compatible with—not contradictory to—the four outer
  residual sheets.
- Outer-quartic jets through order three are fully movable by both
  capped new-block operators; the only common linear terminal adjoint is
  the outer-independent coefficient \([h^{19}]\).
- The canonical residual cokernel lines have nonzero norm, Gram, and
  Wronskian invariants; their first source-vector determinant is not a
  universal identity.
- The first three later residual symbols span the trace-zero quartic
  algebra, but the unique deficit-eight \(E^3\)-adjoint supplies a
  nonzero terminal scalar and kills the deepest weight-four branch.
- Galois normalization excludes Route A degree \(2\), but the required
  non-Galois cubic \(2+1\) branch geometry is locally consistent.
- A finite flat cubic normalization need not be forced non-Gorenstein;
  a normal \(S_3\) twisted-cubic-cone countermodel realizes the proposed
  local singularity.
- The distinguished degree-six dicritical has Puiseux index one; its
  degree-ratio theorem controls total coordinate degree, not geometric
  degree.
- The invariant total-degree lower bound is attained by exact nodal
  first-neighborhood data; the missing condition is the global bracket.
- The residual quadratic factor ramifies at infinity exactly when
  \(\deg g\) is odd, but the two canonical boundary valuations belong to
  the distinguished cubic sheet and impose no parity on \(g\).  Smooth
  normal connected cubic countermodels with an étale distinguished
  section realize squarefree \(g\) of every degree.
- In the finite degree-six compactification, odd residual places are
  intersection points on pre-existing boundary components, not new
  dicritical classes.  The distinguished local degree stays one, and
  the residual four-sheet loss is reused rather than added per root.
- Projective Bézout gives only
  \(\deg g+I_\infty=M\delta\).  The affine boundary class group is free,
  and nonminimal infinity blowups make raw adjunction labels variable,
  so neither supplies a bound on the two terms.
- Global endpoint pairing and sheet-loss counts add no contradiction
  before finality or section realization is imposed.
- Rational canonical scaling destroys residue parity unless global
  pole-freeness is imposed.
- The original facewise ternary boundary proof is invalid: after
  \(t=u/x\), exact seed layers coalesce and a higher-\(C\) term may
  share or precede the chosen boundary order.  The corrected theorem
  must start from the globally earliest face and treat polar graph
  boundaries separately.

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

The best remaining directions are now (i) a finite-global-support or
minimality theorem and (ii) a genuinely nonlinear descent from the new
three-dimensional weighted-lift maps.  Neither is another local boundary
identity.

One concrete formulation is:

> Compare the two resonant formal cap solutions through the common outer
> Hurwitz cover and prove that they cannot both terminate at the exact
> global Newton-support cutoffs.

By the divisor-invariance theorem, this would give full field descent.
Unlike one-boundary Rees membership or a local contact tree, this can see
both caps and the finite polynomial cutoff simultaneously.  The raw
outer-quartic remainder is now known not to descend through the full
new-block quotient, and the natural common face cover is only degree
four.  The linear terminal-row adjoint/transvectant has now also been
exhausted: quartic jets through order three are fully movable, and the
only common linear functional is the bare support ceiling.  The first
nonlinear norm, Gram, Wronskian, and weight-nine determinant tests are
also nonzero.  The viable small target must therefore involve a later
finite-support row or a multistage identity among at least three
cokernel stages, not a leaf-count injection, scalar transvectant, or
pairing of the first two planes.

For Route A, the direct residual-parity shortcut is now closed.  Writing
\(g=c h^2s\), the normalized residual cover is
\(\mathbb C(v)(\sqrt{s})\), and it ramifies at infinity precisely for
odd \(\deg g\).  The canonical quadratic pseudoplane valuations split
the distinguished cubic sheet, whereas \(g\) records monodromy of the
other two sheets.  An explicit Miranda family realizes arbitrary
squarefree \(g\) on a smooth normal connected cubic surface with an
étale distinguished section.

The specific finite degree-six compactification has now been constructed,
and it refutes the hoped-for point-to-component count.  Each finite odd
place is an intersection point of the residual curve with the
pre-existing cubic boundary.  Its distinguished lift lies on the one
fixed divisor \(D_-\), with constant local degree one; the other lifts
reuse the same residual boundary components and four-sheet loss.  The
deck action depends on divisorial valuations of \(u\), not on the parity
of these closed intersection points.  An exact local model carries
arbitrarily many odd places on one ramification component.

Projective intersection then gives the exact ledger
\[
\deg g+I_\infty=M\delta.
\]
The affine degree-six normalization has class group freely generated by
its boundary primes, so the distinguished and omitted cubic boundaries
have no affine divisor-class relation.  Raw adjunction labels change
under arbitrary blowups at the unique infinity end.  Explicit smooth
branch curves and connected Miranda cubics realize the full numerical
freedom.  The exact Bézout, class-group, adjunction, and countermodel
audit is in
`current_context/ROUTE_A_PROJECTIVE_INTERSECTION_BOUND_NO_GO.md`.

The canonical local completion has now been computed rather than
postulated.  Four ordinary point blowups over
\((a,b)=(0,\infty)\) extract \(D_-\), with fixed arm
\[
B_\infty-E_2-E_3-D_-,\qquad E_1\text{ attached to }E_2,
\]
key valuation
\[
\operatorname {ord}_{D_-}(a,s,s+a^2)=(1,2,4),
\]
and residue parameter \(q_3=(s+a^2)/a^4\).  This exact arm still supplies
no label on the unknown cubic-boundary arms.  Moreover, the explicit
one-place family with primitive infinity pair \((k,2k+1)\) has
multiplicity sequence \((k,k,1,\ldots,1)\) and exactly \(k+2\) ordinary
blowups, so its canonical minimal target tree is unbounded.  The family
is a singular injectively parametrized curve, not a Keller
counterexample, and the cited Chau theorems do not exclude it
componentwise.  It is a countermodel only to deductions from the chart,
Bézout data, and canonical minimality.  Thus the focused Route A target
must be a Keller-specific determinant or finality identity crossing from
\(p^{-1}(R)\) to the fixed \(D_-\) arm.  See
`current_context/ROUTE_A_CANONICAL_INFINITY_TREE_FLEXIBILITY.md`.

There is, however, a stronger Keller-specific topological restriction.
The pseudoplane is a rational \(\mathbf Q\)-homology plane, hence every
SNC completion boundary is a tree of rational curves.  Exceptional
divisors over singularities of the finite cubic partial compactification
are subtrees, so all links are rational homology spheres and
\[
H_c^1(R;\mathbf Q)=0.
\]
Every component of \(R\) consequently has normalization
\(\mathbf A^1\), distinct components are disjoint, and all points are
unibranch.  Finite-flat cubic length then forces the same conclusions
for the branch curve \(\Delta\).  The exact Euler balance becomes
\[
r+c+N_{\mathrm{tr}}=2,\qquad r\ge c\ge1,
\]
and therefore
\[
r=c=1,\qquad N_{\mathrm{tr}}=0.
\]
The hypothetical cubic normalization has exactly one ramified boundary
curve, one irreducible branch curve with bijective
\(\mathbf A^1\)-normalization, no affine transitive inertia, and no
non-Gorenstein triple fiber.  The remaining curve may be a singular
cusp; the primary Chau statements audited here exclude a smooth line
component or a simply connected full exceptional set, not an arbitrary
singular component by itself.  Route A has therefore reduced to
monodromy at the single place at infinity.  See
`current_context/ROUTE_A_LOG_TOPOLOGY_CUBIC_COLLAPSE.md`.
Neither rational-tree smoothness nor the simply-connected exceptional-set
criterion finishes this reduction.  The exact local model
\[
z^2=y^2-x^{2m+1}
\]
is an \(A_{2m}\) rational double point with a rational-chain resolution,
\(C_2\) inertia, and a singular bijectively normalized cusp.  For the
degree-six lift, the full nonproper set is
\(A_H=\Gamma_D\cup\Delta\).  The forced normalization
self-identification of \(\Gamma_D\) gives free rank
\(\rho_\Gamma\ge1\), and if the curves meet in \(k\ge1\) affine points,
\[
\pi_1(A_H)\simeq F_{\rho_\Gamma+k-1}.
\]
Thus the full set is never simply connected; the deck involution changes
source-boundary lifts but not this target graph.  See
`current_context/ROUTE_A_SINGLE_INFINITY_GRAPH_NO_GO.md`.
The cubic case is now closed by the retained sheet itself.  The unique
unramified prime \(\overline C\) over \(\Delta\) cannot intersect the
unique ramified boundary \(E\): since both maps are finite birational
over the bijectively normalized branch, an intersection would make the
whole length-three fiber have one support point, contrary to
\(N_{\mathrm{tr}}=0\).  Boundary purity therefore puts
\(\overline C=C\) entirely inside \(S\), and scheme-theoretic étale
base change gives
\[
C\xrightarrow{\sim}\Delta.
\]
The curve \(C\) is a homology line.  Zaidenberg's Theorem 1(c) says
that a singular homology line on a smooth \(\mathbf Q\)-homology plane
forces the ambient surface to be \(\mathbf A^2\); this contradicts
\(\operatorname {Cl}(S)=\mathbf Z/2\).  Hence
\(\Delta\simeq\mathbf A^1\) is smooth and rectifiable.  Its complement
has cyclic fundamental group, but a connected cubic cover requires
transitive monodromy while the generic branch meridian is a
transposition.  Therefore no degree-three étale map
\(S(2,2,1)\to\mathbf A^2\) exists.  See
`current_context/ROUTE_A_CONTRACTIBLE_RETAINED_SHEET_CUBIC_EXCLUSION.md`.

The degree-four successor has now been reduced without a coefficient
search.  Its normalization data satisfy
\[
r=3-c-t-\delta,\qquad r\ge c,
\]
so the branch is irreducible and only three numerical cases remain.
Triple inertia is excluded.  The two simple-inertia survivors precisely
require either a \(3+1\) unibranch collision together with a \(2+2\)
self-intersection, or an extra unramified boundary curve that punctures
both residual sections.  Thus degree four is not yet excluded, but its
failure to retain a homology line is completely localized.  See
`current_context/ROUTE_A_DEGREE_FOUR_RETAINED_SHEET_AUDIT.md`.
The two survivors now have exact normalization profiles.  Residual
ramification in the \(3+1\)/self-intersection survivor is controlled by
intersection parity; its retained Euler characteristic is \(1-4n\),
and the connected completion has genus \(e-1\).  In the extra-boundary
survivor, two punctured affine lines have equal
\(\mathbf Z/2\)-classes.  Every \(r=2,\delta=0\) survivor is
Gorenstein with \(\omega_Y\simeq\mathcal O_Y(E)\) and Cartier \(E\);
the sole non-Gorenstein \(3+1\) escape forces branch multiplicity at
least four.  These sharpen but do not eliminate the survivors.  See
`current_context/ROUTE_A_DEGREE_FOUR_SURVIVOR_NORMALIZATION_PROFILE.md`.

The structurally different construction-first target starts from the
weighted-lift family of genuine three-dimensional Keller maps of every
generic degree at least three.  Common-coordinate descent is impossible
by Orevkov, so any plane descent must use a nonlinear source surface and
a nonlinear target projection.  Polynomial graph source surfaces under
linear projections are now excluded by the separated-leading-degree
theorem.  The honest surviving target is therefore the lower-order
subduction of a genuinely nonlinear second pivot or a non-graph
affine-plane embedding; the two original-pivot rays are now closed.
In fact all their linear mixtures are now closed as well, so the next
pivot must be genuinely nonlinear.  The former lower-tier chains
\(AC+B\), \(ABC+B^2\), \(AB^2C+B^3\), and
\(A^2C^2+ABC\) are now closed by a global Newton-vertex argument.
More strongly, every arbitrary nonhomogeneous target of degree at most
ten is excluded with a first-coordinate perturbation of degree at
most two.  The simultaneous regular and polar collision kernel is
\(\mathbb Z(5,-6,4)\), so the primitive criterion first fails at the
degree-nine cusp relation \(A^5C^4\sim B^6\).  Exact triangular
replacement by \(T,AT,W,U\), including reduction modulo the actual
first coordinate and a two-term polar Wronskian, resolves all collisions
through degree ten.  Binary homogeneous targets
are now closed in every degree: the exact maximal-\(x\) filtration
isolates the top characteristic from all 77 lower \(U\)-support terms
and all lower \(A/B\) seeds, and the unique \(x^{-1}\) recurrence has
an unavoidable double pole for every mixed polynomial completion.
Homogeneous ternary targets are now closed in every degree as well.
The corrected proof chooses the globally earliest source-boundary face
of the complete \(Q_n\).  A regular graph boundary is closed by the
exact full-seed Wronskian and its symbolic support gaps; a polar graph
boundary is closed by incompatible cancellation conditions at
\(u=1\) and \(u=\infty\).  It permits an affine perturbation of \(U\)
and a constant in the second coordinate.  The earlier facewise
boundary argument remains retracted, but its failure is now bypassed
rather than left as a gap.

The next weighted-lift target is no longer those four chains.  Exact
subduction of the first remaining saturation \(BT\sim A^5C^3\)
produces a new two-vector frontier outside
\(\langle A,B,C,T,U\rangle\), so the five known elements are not a
complete SAGBI basis.  The promising task is to understand the
resulting generator sequence structurally—separating the \(L=1\) and
\(L\ge2\) boundary regimes—rather than assume a premature finite
normal form.  The first step is now exact.  After adjoining \(W\), the
formal three-component toric ideal has an eight-binomial minimal Markov
basis.  Under the actual graph projection, its next frontier \(V\) is
new for \(L=2\) and \(L\ge4\), but at \(L=3\) it has precisely the two
reducers \(CA^3T\) and \(B^5A^3\).  The fixed cubic graph jets close
that exception: after subduction, \(V\) always reaches an unreducible
projected gap.  A later element \(X\) is outside the
displayed projected semigroup for every \(L\ge2\).  This proves further
incompleteness, but neither infinitude nor termination.

The fixed-plane analogue is:

> Promote the target-determined endpoint charges and Green potential to
> an actual minimal-resolution section theorem, or perturb
> \(U_0\) by \(E^2\phi\) to remove its global critical scheme while
> preserving the all-order boundary lift.

The two formulations share the same geometry: all local and divisor-level
constraints can be satisfied.  In fact the fixed-plane Keller jet lifts
through every finite normal order because \(\{U,E\}\) is a unit modulo
\(E\).  The chosen \(U_0\) nevertheless has fourteen off-boundary
critical points and cannot belong to a global Keller pair.  Those points
are Morse and persist throughout a dense open set of every full
bounded-degree coefficient space.  A successful deformation must lie
outside these open sets; determining whether one exists requires the
projective critical-incidence analysis.  Finite global realization must
therefore fail at critical-locus removal, termination, or finality
rather than finite-order integrability.

The research program should therefore prioritize:

1. the degree-four-and-higher pseudoplane normalization after the Route
   A cubic exclusion, with special attention to whether the retained
   homology-line mechanism survives more than one unramified sheet;
2. the source values of later case-c adjoints on the remaining generic
   charts, since the first terminal scalar now kills the deepest special
   branch but the abstract residual symbols themselves are maximally
   nondegenerate;
3. a recurrence theorem for the projected SAGBI generator sequence,
   now that the cubic \(V\)-exception is closed, followed by nonlinear
   first-coordinate perturbations or a non-graph source surface;
4. minimal-resolution finality coupled to actual polynomial sections;
5. global critical-point removal for \(U_0+E^2\phi\) and polynomial
   algebraization of the all-order Hermite--CRT lift; and
6. exact countermodels whenever a proposed global inequality is too weak.

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
