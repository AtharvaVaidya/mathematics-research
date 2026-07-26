# Mathematics research archive

This repository is a reproducible research workspace for current and future
mathematics papers.  Its first project studies the plane Jacobian
conjecture, with exact symbolic verifiers, computational certificates, proof
notes, countermodels, and route audits.

## Status

The plane Jacobian conjecture is **not resolved here**.  This repository
does not contain a proof or a counterexample in two variables.

The strongest adversarially audited structural result currently in the
workspace excludes every genuine consecutive \((2,3)\) five-block
completion, at every radial scale.  The proof combines the universal
deficit-one mode, a completed-square root-consumption lemma, and the
exhaustive fixed-pole Puiseux charts; it also closes ramified
multisections of the boundary normalization.  The precise hypotheses and
proof are in
[`current_context/ALLSCALE_MARKED_CUSP_OBSTRUCTION.md`](current_context/ALLSCALE_MARKED_CUSP_OBSTRUCTION.md),
with a symbolic verifier in
[`route_bd_allscale_marked_cusp_obstruction.py`](route_bd_allscale_marked_cusp_obstruction.py).
This eliminates the full consecutive five-block class, not arbitrary
Newton configurations or case c.

An exact scope audit identifies its consequence for the public GGHV preprint
reduction: both alternatives a and b at the remaining \((72,108)\)
frontier are covered, while case c and the other higher-degree admissible
corner chains are not.  See
[`current_context/ALLSCALE_GGHV_SCOPE_AUDIT.md`](current_context/ALLSCALE_GGHV_SCOPE_AUDIT.md).

The remaining case-c coefficient system has now been eliminated by an
exact computer-assisted certificate.  A unimodular support audit checks
all 61 and 125 lattice positions, the outer Hurwitz count exhausts the
five normalized covers, and the full 165-coordinate recurrence reduces to
seven weighted modes.  Its complete weighted-projective special fiber is
empty over every factor above \(32003\); proper specialization then proves
characteristic-zero emptiness.  The required late Newton vertices have
also been checked explicitly, closing an earlier interface loophole.
Together with the GGHV preprint reduction and the a/b theorem, this gives,
over an algebraically closed field of characteristic zero, the bounded result
\[
\boxed{\max(\deg P,\deg Q)\ge125}
\]
for any hypothetical plane Keller counterexample.  The audited dependency
chain and reproduction protocol are in
[`current_context/CASE_C_FULL_CERTIFICATE_BRIDGE.md`](current_context/CASE_C_FULL_CERTIFICATE_BRIDGE.md).
An independent announcement of the same bound exists, so no priority or
uniqueness claim is made here.

This mechanism is genuinely special to transverse degree two.  The tempting
extension to general consecutive transverse degrees is refuted by an exact
local analytic \((3,4)\) countermodel, archived in
[`current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md`](current_context/TRANSVERSE_34_ROOT_CONSUMPTION_COUNTERMODEL.md)
and checked by
[`route_bd_transverse_34_local_countermodel.py`](route_bd_transverse_34_local_countermodel.py).
Keeping such countermodels is part of the proof audit: they prevent a valid
special theorem from being promoted into a false general one.

The proposed global degree-lowering bridge has also been audited.  Full
membership in the affine-modification subring \(k[x,x^r y]\) really does
turn a pair with Jacobian \(cx^r\) into a constant-Jacobian polynomial pair
with the same field degree.  However, an exact arbitrary-degree family
shows that boundary contraction, the leading normal jets, high field
degree, and even a finite-flat Rees comparison do not force that subring
membership or keep the diagonal sheet separate from the cusp.  See
[`current_context/LAURENT_DEGREE_DESCENT_AUDIT.md`](current_context/LAURENT_DEGREE_DESCENT_AUDIT.md).
The larger one-boundary toroidal class is now classified as well: every
triangular chart absorbing a monomial Jacobian is
\(u=x^a,\ v=x^{r+1-a}y+f(x)\), and iterations produce nothing new.
Required GGHV vertices exclude every such chart, while normalization leaves
a residual Jacobian power.  Thus any global degree-lowering proof must use
multiple boundary valuations or genuinely nontriangular geometry; see
[`current_context/TOROIDAL_DEGREE_DESCENT_NO_GO.md`](current_context/TOROIDAL_DEGREE_DESCENT_NO_GO.md).

The complementary Standard/Kummer route now has an exact one-coordinate
field-descent criterion.  For a normalized comparison branch, full descent
of \(Z,W\) is equivalent to descent of the single weighted invariant
\(\Xi=ZW^k\); an exact torus countermodel shows why valuations and local
symplecticity alone cannot force it.  See
[`current_context/RADIAL_INVARIANT_FIELD_DESCENT.md`](current_context/RADIAL_INVARIANT_FIELD_DESCENT.md).
The reciprocal Wronskian further gives canonical Darboux powers
\(S=\Xi^5\) and \(Y=T^{5k+2}\).  An exact trace-and-support argument proves
that descent of either power—or of their product
\(SY=Z^5/W^2\)—is equivalent to descent of the entire comparison branch.
A genuine-endpoint completed-local cusp model shows that none is forced by
the Liouville identity or the sole allowed ramification signature,
isolating the normalized global infinity sheet and polynomial Newton
support as essential.  See
[`current_context/RECIPROCAL_DARBOUX_LIOUVILLE_AUDIT.md`](current_context/RECIPROCAL_DARBOUX_LIOUVILLE_AUDIT.md).
At the global level, invariance of the complete principal divisor of
either Darboux power—or of their product \(Z^5/W^2\)—does force full
descent.  Divisor divisibility alone is tautological, and an exact target-
translation model shows that the normalized infinity sheet and outer
support do not force invariance.  The remaining target is therefore a
boundary-orbit theorem using the forced inner vertices; see
[`current_context/GLOBAL_DARBOUX_DIVISOR_SECTION_AUDIT.md`](current_context/GLOBAL_DARBOUX_DIVISOR_SECTION_AUDIT.md).
Two adjacent boundary orders, even to arbitrarily high precision, still
do not suffice: an exact symplectic countermodel hides the moving divisor
support away from both rays.  The sharp positive criterion is now support
exhaustion for every divisor quotient \(\sigma J/J\); the exact GGHV cap
vertices remain the possible mechanism.  See
[`current_context/TWO_BOUNDARY_DIVISOR_ORBIT_AUDIT.md`](current_context/TWO_BOUNDARY_DIVISOR_ORBIT_AUDIT.md).
Even the exact case-c cap faces do not suffice by themselves.  A
constrained generic pair with the full case-c polygons, genuine outer
Wronskian, and both forced cap factorizations has degree \(131\), not
divisible by the endpoint degree \(21\), so its comparison branch still
has hidden monodromy.  It is not a bracket solution; its role is to prove
that deeper bracket-controlled infinitely-near jets are indispensable.
See
[`current_context/CASE_C_CAP_SUPPORT_EXHAUSTION_NO_GO.md`](current_context/CASE_C_CAP_SUPPORT_EXHAUSTION_NO_GO.md).
The full local bracket still does not close this gap.  At both the
vertical and diagonal caps there is a unique minimum-height resonant
contact star; each star avoids every no-log threshold, preserves the
resultant constant, and lifts recursively to an exact formal local bracket
solution.  Consequently no purely local infinitely-near refinement can
exclude case c.  What remains is finite global support termination or a
cross-cap relation through the common outer cover; see
[`current_context/CASE_C_CAP_RESONANT_STAR_NO_GO.md`](current_context/CASE_C_CAP_RESONANT_STAR_NO_GO.md).
The required deeper input now has a general branchwise form: the bracket
restricts on every cap Puiseux leaf to an Euler equation whose only free
term is one resonant constant per irreducible factor.  Its finite
no-log residues forbid the exact same-color contact sums \(5,9\) at the
vertical cap and \(10,14\) at the diagonal cap.  The accompanying trace
identity is valid but retains a homogeneous constant, so no global
contradiction is claimed; see
[`current_context/CAP_PUISEUX_EULER_JET_INVARIANT.md`](current_context/CAP_PUISEUX_EULER_JET_INVARIANT.md).

The first proposed cross-cap conormal shortcut has now been audited and
withdrawn.  The actual diagonal chart has eleven \(P\)-layers and sixteen
\(Q\)-layers and satisfies an Euler bracket.  At deficit four, the three
Laurent-tail pairings omitted by the \(2/3\) ordinary-Jacobian truncation
are nonzero and cancel the retained middle contribution exactly.  Hence
its local quotient and completed-square discriminant are not invariants
of the full case-c system; see
[`current_context/CASE_C_CONORMAL_TRUNCATION_NO_GO.md`](current_context/CASE_C_CONORMAL_TRUNCATION_NO_GO.md).
The associated outer quartic is instead the four-point unramified
residual part of the degree-\(21\) fiber with monodromy
\((17)(1^4)\).  The natural cap incidence does not produce the
previously contemplated \(8\)- or \(12\)-sheet subset: the common
normalization of the \((8,12)\) face has degree
\(\gcd(8,12)=4\), exactly matching the four residual outer sheets.
Moreover, its Kummer four-point divisor has binary-quartic invariant
\(J=0\), whereas all five certified outer quartics have \(J\ne0\)
modulo \(32003\).  Thus neither projective identification nor an
arbitrary labeling supplies a canonical correspondence.  Exact formal
caps over the quartic incidence algebra show that valuations and
completed local jets alone remain compatible; see
[`current_context/CASE_C_OUTER_QUARTIC_INCIDENCE_NO_GO.md`](current_context/CASE_C_OUTER_QUARTIC_INCIDENCE_NO_GO.md).
The corrected common-cover audit is in
[`current_context/CASE_C_DEGREE_FOUR_INCIDENCE_AUDIT.md`](current_context/CASE_C_DEGREE_FOUR_INCIDENCE_AUDIT.md).
At the full deficit-\(4\) and deficit-\(5\) linear quotients, the
new-block operators are surjective modulo the quartic and its square on
all three outer Hurwitz factors.  Thus even raw \(E\)- or \(E^2\)-remainder
is not a cokernel invariant.  The full linear-adjoint audit extends this
surjectivity through \(E^4\), exhausting all distributions on the four
roots through derivative order three.  At order four the quartic jets
merely re-coordinate the original bounded rows; the unique adjoint common
to both new-block images is the ordinary support ceiling
\([h^{19}]\), independent of \(E\).  Thus no scalar linear adjoint or
fixed-\(E\) transvectant couples the caps; a surviving construction must
be nonlinear in existing cokernel values.  See
[`current_context/CASE_C_OUTER_QUARTIC_COKERNEL_NO_GO.md`](current_context/CASE_C_OUTER_QUARTIC_COKERNEL_NO_GO.md)
and
[`current_context/CASE_C_OUTER_QUARTIC_ADJOINT_NO_GO.md`](current_context/CASE_C_OUTER_QUARTIC_ADJOINT_NO_GO.md).
The smallest nonlinear continuation is nondegenerate as well.  Canonical
Frobenius representatives for the two residual cokernel lines have
nonzero norms, nonzero trace-Gram determinant, and nonzero Wronskian
norm at all five outer points.  Their weight-nine source determinant is
an explicit nonzero 76-term polynomial, not a universal compatibility
identity.  Resultant, norm, bilinear, and first tangency constructions
from only these two cokernel planes therefore add no obstruction; a
successful case-c invariant must import a later finite-support row or a
multistage identity.  See
[`current_context/CASE_C_COKERNEL_NONLINEAR_PAIRING_NO_GO.md`](current_context/CASE_C_COKERNEL_NONLINEAR_PAIRING_NO_GO.md).
The later-row complex now supplies the first positive terminal
invariant.  For deficits \(4\) through \(15\), reduction modulo \(E^j\)
has rank \(\min(4j,r_d)\).  The first three residual adjoints span the
trace-zero quartic algebra, so their three-stage Gram determinant gives
no identity.  At deficit eight, however, the unique adjoint modulo
\(E^3\) restricts on the deepest weight-four branch to
\(C_8X_6^2\), with nonzero total norm modulo \(32003\); it therefore
forces \(X_6=0\).  This replaces five special-chart rows by one
canonical scalar, although the generic charts still need their existing
certificates.  See
[`current_context/CASE_C_MULTISTAGE_JET_STAIRCASE.md`](current_context/CASE_C_MULTISTAGE_JET_STAIRCASE.md).

The pseudo-plane construction route has a new degree-independent
function-field restriction.  For any étale map from a normal affine
complex surface with only constant units to \(\mathbf A^2\), a finite
nontrivial Galois function-field extension is impossible: normalization,
purity, and Galois inertia would otherwise make a branch equation pull
back to a nonconstant unit.  Applied to the quadratic pseudo-plane, this
excludes generic degree \(2\).  A surviving cubic must have \(S_3\)
closure and, over each branch component, retain a principal unramified
sheet while omitting a ramified double sheet.  The two nonprincipal
boundary curves cannot be retained sheets, but an exact cubic model shows
that the \(2+1\) branch geometry itself is consistent.

The cubic normalization has now been audited through its topology,
triple-cover algebra, collision curve, and extreme weights.  It is finite
flat of rank three.  Non-Gorenstein fibers, when present, are holes in
the étale image, and the entire distinguished curve \(\Gamma_D\) avoids
them.  At any self-identification of its normalization \(D\simeq\mathbb
A^1\), the cubic fiber is completely étale and has at most three retained
points.  After base change to \(D\), the algebra splits globally as
\[
\mathbb C[v]\times
\mathbb C[v,\tau]/(\tau^2-g(v)),
\]
and the restricted cubic discriminant is a nonzero constant times
\(g(v)\).  Exact nodal and normal \(S_3\) countermodels show why these
facts do not yet contradict cubicity.  The surviving algebraic target is
therefore a boundary or intersection theorem for this residual quadratic
cover, together with the triangularly irreducible extreme-weight cusp.
See
[`current_context/ROUTE_A_QUADRATIC_DEGREE_EXCLUSION.md`](current_context/ROUTE_A_QUADRATIC_DEGREE_EXCLUSION.md)
and
[`current_context/ROUTE_A_CUBIC_BRANCH_SECTION_AUDIT.md`](current_context/ROUTE_A_CUBIC_BRANCH_SECTION_AUDIT.md),
[`current_context/ROUTE_A_NON_GORENSTEIN_GAMMA_D_INCIDENCE.md`](current_context/ROUTE_A_NON_GORENSTEIN_GAMMA_D_INCIDENCE.md),
and
[`current_context/ROUTE_A_CUBIC_EXTREME_WEIGHT_VALUATION_AUDIT.md`](current_context/ROUTE_A_CUBIC_EXTREME_WEIGHT_VALUATION_AUDIT.md).
For the associated degree-six plane lift, the distinguished line image
is indeed a component of the nonproper-value curve, but its exact
Newton--Puiseux index is \(1\), not \(2\).  Chau's ratio theorem and the
invariant filtration give \(d_1/d_2=m_1/m_2\) and \(d_i\ge4m_i\);
these are total coordinate degrees and do not contradict geometric
degree six.  Orevkov's exact defect formula assigns this class
contribution \(1\) and leaves residual defect \(4\), sharply compatible
with \(6-1=(2-1)+2(3-1)\).  An explicit polynomial dicritical chart is
étale even at the forced node, closing that shortcut; see
[`current_context/ROUTE_A_SINGULAR_DICRITICAL_INDEX_AUDIT.md`](current_context/ROUTE_A_SINGULAR_DICRITICAL_INDEX_AUDIT.md).
The associated invariant degree filtration is sharp:
\(\deg\phi(F)\ge4\deg_b\phi(F)(0,b)\), with equality block exactly a
multiple of \(v^m\).  The top homogeneous Keller relation, boundary
Bézout identity, geometric degree six, and standard nonproperness/degree
bounds all remain compatible.  A nodal first-neighborhood model realizes
the equality architecture while failing the global Jacobian equation;
see
[`current_context/ROUTE_A_INVARIANT_DEGREE_FILTRATION_SHARPNESS.md`](current_context/ROUTE_A_INVARIANT_DEGREE_FILTRATION_SHARPNESS.md).
The residual quadratic cover itself has now been normalized explicitly:
if \(g=c h^2s\) with \(s\) squarefree, it has function field
\(\mathbb C(v)(\sqrt{s})\), finite ramification at the odd-order roots
of \(g\), and ramification at infinity exactly when \(\deg g\) is odd.
The two canonical boundary valuations instead split the distinguished
cubic sheet and do not control this longitudinal residual monodromy.
More strongly, an exact connected finite-flat cubic family realizes
every squarefree \(g\), of arbitrary degree and parity, with an
everywhere-étale distinguished section and a smooth normal total
surface.  Thus finite flatness, normality, the section, and the deck
involution do not provide the missing parity or degree bound.  See
[`current_context/ROUTE_A_RESIDUAL_QUADRATIC_INFINITY_AUDIT.md`](current_context/ROUTE_A_RESIDUAL_QUADRATIC_INFINITY_AUDIT.md).
The actual finite degree-six compactification closes the next proposed
bridge as well.  A finite odd place of \(g\) is a point where the
residual curve meets the already-existing cubic boundary; its
distinguished lift lies on the one fixed divisor \(D_-\), where the
local degree remains one.  It creates no new dicritical component and
no additional Orevkov summand.  The deck involution exchanges omitted
\(D_-\) with retained \(D_+\), while its action over cubic boundary
primes depends on a divisorial valuation and residue square class, not
on root parity.  An exact transverse model places arbitrarily many odd
residual roots on one ramification component.  The surviving Route A
target is therefore an intersection bound for the fixed projective
boundary curves, not a root-to-component count; see
[`current_context/ROUTE_A_GLOBAL_MONODROMY_DICRITICAL_BRIDGE_NO_GO.md`](current_context/ROUTE_A_GLOBAL_MONODROMY_DICRITICAL_BRIDGE_NO_GO.md).
Projective intersection theory supplies the exact identity
\[
\deg g+I_\infty=M\delta,
\]
where \(M=\deg\overline\Gamma\), \(\delta\) is the cubic discriminant
degree, and the nonnegative remainder is carried at the unique end of
\(\Gamma\).  It does not bound either term separately.  In the affine
degree-six normalization, localization from the plane open shows that
the class group is freely generated by all boundary primes, so
\(D_-\) and the primes above the omitted cubic boundary have no affine
class relation.  Adjunction varies under harmless infinity blowups, and
exact smooth branch and connected cubic families realize arbitrary
finite/infinite allocations.  The surviving input would have to be a
Keller-specific relation crossing between the distinguished and cubic
boundary arms; see
[`current_context/ROUTE_A_PROJECTIVE_INTERSECTION_BOUND_NO_GO.md`](current_context/ROUTE_A_PROJECTIVE_INTERSECTION_BOUND_NO_GO.md).
The canonical local calculation is now exact.  Four ordinary point
blowups extract the distinguished divisor \(D_-\), with key valuation
\[
\operatorname {ord}(a,s,s+a^2)=(1,2,4)
\]
and nonconstant residue parameter \(q_3=(s+a^2)/a^4\).  This fixed
arm still does not constrain the cubic-boundary arms.  Indeed, an
explicit one-place curve family has primitive infinity pair
\((k,2k+1)\), multiplicity sequence
\((k,k,1,\ldots,1)\), and exactly \(k+2\) blowups.  The family is not
a Keller counterexample and supplies no cover monodromy.  Its singular
injective parametrization is not excluded by the componentwise form of
the cited Chau results; it proves precisely that chart data, Bézout,
and canonical minimality alone leave the target tree unbounded.  Route A
therefore needs a functorial determinant or finality relation that
crosses the two arms, not a minimal-tree bound; see
[`current_context/ROUTE_A_CANONICAL_INFINITY_TREE_FLEXIBILITY.md`](current_context/ROUTE_A_CANONICAL_INFINITY_TREE_FLEXIBILITY.md).
Log topology nevertheless gives a new Keller-specific collapse.  The
pseudoplane is a rational \(\mathbf Q\)-homology plane, so every SNC
completion boundary is a rational tree and every singularity of the
finite cubic partial compactification has a rational-homology-sphere
link.  Alexander--Lefschetz duality then gives
\(H_c^1(R;\mathbf Q)=0\).  Flat cubic fiber length transfers the same
unibranch property to the branch curve, and the Euler equation
\[
r+c+N_{\mathrm{tr}}=2,\qquad r\ge c\ge1,
\]
forces \(r=c=1\) and \(N_{\mathrm{tr}}=0\).  Thus there is one rational
unibranch boundary, one irreducible bijectively parametrized branch
curve, no affine transitive inertia, and no non-Gorenstein triple fiber.
A singular cusp remains possible, so the cited Chau theorems do not yet
give a contradiction; the live Route A problem is now monodromy at the
single place at infinity.  See
[`current_context/ROUTE_A_LOG_TOPOLOGY_CUBIC_COLLAPSE.md`](current_context/ROUTE_A_LOG_TOPOLOGY_CUBIC_COLLAPSE.md).
Both immediate topological shortcuts at that point are closed.  The
local \(2+1\) model
\(z^2=y^2-x^{2m+1}\) is an \(A_{2m}\) rational double point with
\(C_2\) inertia and a singular bijectively normalized cusp, so a
rational boundary tree does not force smoothness.  Moreover
\(A_H=\Gamma_D\cup\Delta\), and the forced self-identification on
\(\Gamma_D\) already gives a free loop.  If the two components meet in
\(k\) affine points, then
\[
\pi_1(A_H)\simeq F_{\rho_\Gamma+k-1},\qquad \rho_\Gamma\ge1.
\]
Thus Chau's simply-connected-set corollary cannot apply; a contradiction
must use the actual \(S_3\) monodromy or determinant labels at infinity.
See
[`current_context/ROUTE_A_SINGLE_INFINITY_GRAPH_NO_GO.md`](current_context/ROUTE_A_SINGLE_INFINITY_GRAPH_NO_GO.md).

The counterexample-first fixed-source-plane route has a second independently
audited global theorem.  If a Darboux pair existed in its explicit pinch
ring and \(F(U,V)=D H\) were the pullback of the conductor-image equation,
then
\[
H|_C(-v)=-H|_C(v).
\]
Thus an additional affine preimage component over the conductor image is
compulsory.  If that image is smooth, one irreducible residual component
meets both marked cusp arms with positive odd multiplicity, and its Laurent
exponent satisfies \(m\equiv-1\pmod{2\delta}\).  Independently, the
Chau--Jelonek theorem forces a different nonproper-value component.  The
complete statement and its sharp countermodels are in
[`current_context/FIXED_SOURCE_PLANE_ROUTE.md`](current_context/FIXED_SOURCE_PLANE_ROUTE.md).
The associated counterexample-first test family is also closed exactly:
among all \(f(c)+g(c)D(3ct-2)\), the sole nonconstant submersions are
affine rescalings of \(cD(3ct-2)\), and that Hamiltonian has no polynomial
Darboux mate even in the normalization.  See
[`current_context/RESIDUAL_FACTOR_HAMILTONIAN.md`](current_context/RESIDUAL_FACTOR_HAMILTONIAN.md).
This still constrains only the fixed-source construction and is not a proof
of \(JC(2)\).

The corresponding projective intersection system has now been pushed
through the full effective pullback of the conductor image.  An exact dual
certificate rules out the first scalar boundary skeleton, but a second
19-component integral ledger satisfies every current effectivity,
adjunction, ramification, and residual-cover equation.  It fails the
minimal-resolution final-curve condition, so the next obstruction must
couple effectivity to finality rather than add more scalar inequalities.
The ledger is explicitly numerical—not a morphism or counterexample—and is
recorded in
[`current_context/GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`](current_context/GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md).
For that ledger, the defect vector \(db-\eta\) now rules out every
branched or crossing exceptional cap over its decisive positive-label
final curve while the old coefficients are retained.  This is an exact
arbitrary-cluster theorem, although a different enlarged global ledger
remains possible; see
[`current_context/FIXED_PLANE_FINALITY_CAP_OBSTRUCTION.md`](current_context/FIXED_PLANE_FINALITY_CAP_OBSTRUCTION.md).
Globally, every point-mapping subtree has a positive Green kernel and the
conductor endpoints obey the exact defect budget
\(\sigma_\alpha+\sigma_\beta=-q\).  Residual components also obey the new
endpoint-charge law
\(\sum(a_i+\sigma_i)=2g+s-2\).  This law rules out the first
four-curve local stress test as non-geometric, but an exact degree-two
component ledger still satisfies projection, adjunction,
Riemann--Hurwitz, Hodge, and ramification while retaining negative
defect under those summed tests.  The missing pointwise normal-map law is
now derived: every residual endpoint charge is fixed by the single
Laurent exponent of the target Poincaré residue.  It rules out the
degree-two repair and the earlier degree-nine witness for its particular
displayed target curve, while leaving other target embeddings open; see
[`current_context/FIXED_PLANE_DEFECT_GREEN_FUNCTION.md`](current_context/FIXED_PLANE_DEFECT_GREEN_FUNCTION.md)
and
[`current_context/FIXED_PLANE_COMPONENT_ENDPOINT_PAIRING.md`](current_context/FIXED_PLANE_COMPONENT_ENDPOINT_PAIRING.md),
with the gluing theorem in
[`current_context/FIXED_PLANE_NORMAL_MAP_GLUING.md`](current_context/FIXED_PLANE_NORMAL_MAP_GLUING.md).
The remaining Laurent exponent is now classified exactly: if
\(H|_C=\lambda v^m\) and the conductor cover is
\(s=\alpha c^{\epsilon\delta}\), then
\(m=-1-2\epsilon\delta j\).  This does not force \(j=0\): a smooth
quartic \(\mathbf G_m\) has the exact conductor residue \(2/3\), the
same \((2,5)\) and \((2,3)\) ends, and \(j=-1\), while satisfying both
local endpoint ledgers and the necessary Green/finality rows.  This is
a sharp scoped countermodel, not a Keller map; see
[`current_context/FIXED_PLANE_RESIDUE_EXPONENT_CLASSIFICATION.md`](current_context/FIXED_PLANE_RESIDUE_EXPONENT_CLASSIFICATION.md).
Even global pairing of both target ends does not repair the divisor-level
route.  A smooth degree-nine \(\mathbf G_m\) with residue \(2/3\) realizes
all four conductor/residual normal contacts of the 19-vertex pullback
ledger at once.  Its only recorded failure is exactly the six forbidden
final point-mapping curves; no global sections or morphism are claimed.
See
[`current_context/FIXED_PLANE_GLOBAL_ENDPOINT_NORMAL_COUNTERMODEL.md`](current_context/FIXED_PLANE_GLOBAL_ENDPOINT_NORMAL_COUNTERMODEL.md).
Likewise, the finite endpoint-charge sum is exactly the missing-sheet
Euler/Riemann--Hurwitz identity, not an additional inequality.  An exact
first-order Hermite-CRT model realizes the conductor, a residual sheet,
the odd normal factor, and the Keller determinant modulo their union,
while deliberately stopping short of a global Keller pair.  See
[`current_context/FIXED_PLANE_SHEET_LOSS_AND_FIRST_ORDER_CRT.md`](current_context/FIXED_PLANE_SHEET_LOSS_AND_FIRST_ORDER_CRT.md).
The broader residue-parity conjecture is also false for rational
descended pairs: endpoint-neutral canonical scalings preserve the
Darboux equation, conductor data, and endpoint residue while moving the
odd class onto arbitrary interior level divisors.  These scalings
introduce affine poles and therefore do not produce polynomial pairs.
Consequently any valid replacement must use global pole-freeness or
finite polynomial termination; see
[`current_context/FIXED_PLANE_RESIDUE_PARITY_SCALING_NO_GO.md`](current_context/FIXED_PLANE_RESIDUE_PARITY_SCALING_NO_GO.md).

Finally, the new three-dimensional counterexample does not descend to a
plane counterexample through a common source/target coordinate.  Such a
coordinate would give generic plane slices of geometric degree three,
contradicting Orevkov's theorem that a two- or three-sheeted polynomial
map of \(\mathbb C^2\) cannot have nonzero constant Jacobian.  This
closes arbitrary, including wild, common-coordinate descent, but not
nonlinear source surfaces or nonlinear target projections; see
[`current_context/THREE_DIMENSIONAL_COORDINATE_SLICE_OREVKOV_NO_GO.md`](current_context/THREE_DIMENSIONAL_COORDINATE_SLICE_OREVKOV_NO_GO.md).
For the independent generic-degree-six weighted lift, a second theorem
closes every polynomial graph source \(z=g(x,y)\) followed by a rank-two
linear target projection.  The three target-minor Jacobians have
nonzero, strictly separated leading degrees, so no nonzero linear
combination is constant.  The result includes a graph interpolating all
six known colliding points and extends to every nonconstant graph in the
full weighted-lift family.  See
[`current_context/WEIGHTED_LIFT_DEGREE_SIX_GRAPH_PROJECTION_NO_GO.md`](current_context/WEIGHTED_LIFT_DEGREE_SIX_GRAPH_PROJECTION_NO_GO.md).
The first nonlinear cusp cancellation has also been subducted exactly.
Its primitive relation is \(p_5^6A^5C^4-q_6^5B^6\), not
\(A^5-\lambda B^6\).  Two SAGBI-style subductions leave only two sparse
Newton rays on which a top Jacobian with \(A\) or \(B\) can vanish:
\[
\begin{aligned}
g_m&=c x^{8k+7}y^{5k+5},&m&=13k+12,\\
g_m&=c x^{4k-1}y^{11k+4},&m&=15k+3,\quad k\ge1.
\end{aligned}
\]
Every graph is excluded for the \(C\)-pivot, and every graph outside
these rays is excluded for the other original pivots.  The first ray is
governed by an explicit weighted-Euler equation, giving a focused
lower-order recursion rather than an unrestricted search; see
[`current_context/WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`](current_context/WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md).
That recursion is now closed on both rays.  On the \(B\)-ray, the fixed
coefficient \(a=-57/34\) leaves an unavoidable
\((228/17)xy+1/34\) weighted-Euler defect before any lower seed sector
can enter.  On the \(A\)-ray, binomial completion requires a monomial
with only one factor of \(x\), impossible because graph terms enter
through \(x^2g\).  Hence, for every linear target correction \(L\),
none of \((U+L,A)\), \((U+L,B)\), or \((U+L,C)\) descends on a
nonconstant polynomial graph.  The mixed linear pivot is now closed too:
for every nonzero \(\alpha A+\beta B+\delta C\), the coupled \(A/B\)
characteristic equation forces the same forbidden \(x^1\)-term,
independently of the mixing ratio; in the \(B/C\) case the \(B\)-defect
appears before \(C\) can enter.  Constant graphs are excluded by exact
separated top forms.  Genuinely nonlinear second coordinates remain
open; see
[`current_context/WEIGHTED_LIFT_SECOND_SUBDUCTION_RAY_CLOSURE.md`](current_context/WEIGHTED_LIFT_SECOND_SUBDUCTION_RAY_CLOSURE.md)
and
[`current_context/WEIGHTED_LIFT_MIXED_LINEAR_PIVOT_CLOSURE.md`](current_context/WEIGHTED_LIFT_MIXED_LINEAR_PIVOT_CLOSURE.md).
The exclusion now extends to every affine quadratic second coordinate.
For the binary \(A/B\) face, one characteristic equation classifies the
\(A^2\), \(AB\), and \(B^2\) rays; the new \(AB\) ray forces
\(\binom{27k+2}{16k}x y^{11k+2}\), which cannot arise from \(x^2g\).
On the \(C\)-faces, mixed \(AC/BC\) forces a negative infinity-chart
power, pure \(AC\) has a fixed Euler defect, \(BC\) has no resonance,
and \(C^2\) reduces to the closed linear cases.  Affine perturbations
enter after these defects.  Thus every
\((U+L,Q(A,B,C))\) with nonzero quadratic part fails on every
polynomial graph.  See
[`current_context/WEIGHTED_LIFT_ALL_QUADRATIC_PIVOT_CLOSURE.md`](current_context/WEIGHTED_LIFT_ALL_QUADRATIC_PIVOT_CLOSURE.md).
The target-Newton argument now closes degree three as well.  Every
\[
V=Q_3(A,B,C)+Q_{\le2}(A,B,C),\qquad Q_3\ne0,
\]
fails on every polynomial graph even after adding an arbitrary
degree-at-most-two target polynomial to \(U\).  A master
characteristic formula classifies all binary and \(C\)-divisible cubic
faces; the new \(A^2B\) ray forces a forbidden \(x^1\)-term, the mixed
\(ABC/B^2C\) ray forces a negative infinity-chart power or a fixed
Euler defect, and all remaining \(C\)-faces are nonresonant.  An exact
Newton staircase prevents lower target tiers from repairing any defect.
See
[`current_context/WEIGHTED_LIFT_ALL_CUBIC_PIVOT_CLOSURE.md`](current_context/WEIGHTED_LIFT_ALL_CUBIC_PIVOT_CLOSURE.md)
and
[`current_context/WEIGHTED_LIFT_C_DIVISIBLE_CUBIC_FACE_CLOSURE.md`](current_context/WEIGHTED_LIFT_C_DIVISIBLE_CUBIC_FACE_CLOSURE.md).
The quartic layer is now closed in the same uniform form:
\[
V=Q_4+Q_{\le3},\qquad U\longmapsto U+R_{\le3}.
\]
All binary and \(C\)-divisible faces reduce to nine exact rays.
Finite coefficient recurrences close the mixed \(C^2Q_2\) face and
the interleaved \(A/B/C^4\) face; the sole constant-graph toric
degeneracy, \(AB^3\) at \(z=0\), has an exact nonzero next diagonal.
See
[`current_context/WEIGHTED_LIFT_ALL_QUARTIC_PIVOT_CLOSURE.md`](current_context/WEIGHTED_LIFT_ALL_QUARTIC_PIVOT_CLOSURE.md).
More generally, every pure binary monomial face is closed in every
target degree, and every binary target through degree five follows
from one all-degree characteristic formula.  The first polynomial
completion, the sextic \(B^5(\lambda A+\mu B)\) family, is also closed:
its first lower-seed recurrence has residue
\[
-\frac{221578k+153403}{510}\ne0.
\]
See
[`current_context/WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_REDUCTION.md`](current_context/WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_REDUCTION.md)
and
[`current_context/WEIGHTED_LIFT_DEGREE_SIX_EXCEPTIONAL_RECURRENCE_CLOSURE.md`](current_context/WEIGHTED_LIFT_DEGREE_SIX_EXCEPTIONAL_RECURRENCE_CLOSURE.md).
The sextic recurrence has now been promoted to a uniform theorem.
For every \(n\ge1\), the entire Newton-degree-one family
\[
B^{n-1}(\lambda A+\mu B),\qquad \lambda\ne0,
\]
has source-axis residue
\[
-\frac{
2975In^2+952In-2023I-3035n^2+22780n-1785
}{2040n}.
\]
Its numerator is positive for all admissible \(I\ge2,n\ge1\), while
every polynomial graph correction remains divisible by \(x^2\).
Hence no member of this family descends on a polynomial graph in any
target degree.  See
[`current_context/WEIGHTED_LIFT_ALL_DEGREE_D1_RECURRENCE_CLOSURE.md`](current_context/WEIGHTED_LIFT_ALL_DEGREE_D1_RECURRENCE_CLOSURE.md).
Quintic \(C\)-divisible faces and non-graph source surfaces are now the
first unresolved full layers; among binary faces, the next unresolved
characteristic class has Newton degree at least two.

## Reproduction

The quick exact verifier suite is:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python verify_all.py
```

Several certificates also require
[Singular](https://www.singular.uni-kl.de/) 4.4 or newer.  Slow
characteristic-zero reconstruction and Gröbner calculations are kept
separate from the default suite; their notes give the exact invocation and
cache behavior.

Every script labeled a verifier uses exact arithmetic.  Files prefixed
`scratch_` are exploratory artifacts and should not be cited as proofs
without a corresponding audited note.

## Guide

- `current_context/` — focused theorem statements, derivations, and route
  audits.
- `route_bd_*.py` — exact verifiers for the bounded Newton-support and
  radial/Hurwitz program.
- `route_a/` — the pseudoplane/Darboux counterexample-first program.
- `route_3d_*.py` — audits connecting the known three-dimensional
  counterexample to two-dimensional descent problems.
- `RESEARCH_REPORT.md` — long-form research history and consolidated
  derivations.
- `papers/degree-125-bound/` — preprint source and publication replay
  instructions for the bounded theorem.
- `STATUS_AND_PIVOT_2026-07-25.md` — the latest high-level result and
  strategy audit.
- `verify_all.py` — bundled deterministic regression suite.

## Standards used in this archive

- A finite-field calculation is not presented as a characteristic-zero
  theorem without a valid lifting or specialization argument.
- Probabilistic Gröbner output is labeled as evidence until accompanied by
  a deterministic membership, homogeneous, or independently reproduced
  certificate.
- Countermodels are retained when they falsify an attractive but invalid
  extrapolation.
- Publication claims are separated from the unresolved \(JC(2)\) goal.

## References

- J. A. Guccione, J. J. Guccione, R. Horruitiner, and C. Valqui,
  “Increasing the degree of a possible counterexample to the Jacobian
  Conjecture from 100 to 108,”
  [arXiv:2204.14178](https://arxiv.org/abs/2204.14178).
- A. Dubouloz and K. Palka, “The Jacobian Conjecture fails for
  pseudo-planes,”
  [arXiv:1701.01425](https://arxiv.org/abs/1701.01425).
- S. Yu. Orevkov, “On three-sheeted polynomial mappings of
  \(\mathbb C^2\),” Math. USSR-Izv. **29** (1987), 587--596,
  [DOI 10.1070/IM1987v029n03ABEH000984](https://doi.org/10.1070/IM1987v029n03ABEH000984).
- T. Shaska, “Graded Keller maps and the Jacobian Conjecture,”
  [arXiv:2607.20210](https://arxiv.org/abs/2607.20210).
- A. Gallagher, “The Jacobian counterexample, explained,” including the
  weighted-lift family and exact supporting code,
  [jacobianfun.org](https://jacobianfun.org/jacobian-explained).
- N. V. Chau, “Non-zero constant Jacobian polynomial maps of
  \(\mathbb C^2\),” Ann. Polon. Math. **71** (1999), 287--310,
  [journal PDF](https://matwbn.icm.edu.pl/ksiazki/apm/apm71/apm7135.pdf).

## Attribution

The repository is maintained by Atharva Vaidya.  Computational and drafting
assistance from AI systems should be disclosed in any paper derived from
this archive, alongside independent human verification of the mathematical
claims.
