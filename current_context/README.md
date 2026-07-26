# July 2026 three-dimensional counterexample: relevance to the plane

This note records current context that postdates much of the plane-Jacobian
literature. It is not a solution of the two-dimensional problem.

## Exact three-dimensional construction

For

\[
\begin{aligned}
a&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
b&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
c&=2x-3x^2y-x^3z,
\end{aligned}
\]

direct symbolic calculation gives

\[
\det \frac{\partial(a,b,c)}{\partial(x,y,z)}=-2.
\]

The three distinct rational points

\[
(0,0,-1/4),\qquad (1,-3/2,13/2),\qquad
(-1,3/2,13/2)
\]

all map to \((-1/4,0,0)\). Thus the general Jacobian conjecture is false
in dimension three, while this says nothing by itself about dimension two.

## Hyperbolic quotient

For the grading with source invariants

\[
u=xy,\qquad v=x^2z,
\]

put

\[
L=2-3u-v,\qquad
M=v(1+u)^2+u^2(4+3u).
\]

The target invariants \(P=bc,\ Q=ac^2\) are

\[
P=L(u+3M),\qquad Q=L^2(1+u)M,
\]

and their exact quotient Jacobian is

\[
\frac{\partial(P,Q)}{\partial(u,v)}=2L^2.
\]

The map contracts the line \(L=0\) to \((0,0)\). The square factor is the
mechanism that permits the three-dimensional determinant to remain constant;
the quotient itself is not a plane Keller map.

## Why the direct target slice does not descend

The inverse image of the target plane \(c=0\) is reducible:

\[
c=xL=0.
\]

On \(x=0\), the restriction is the triangular automorphism

\[
(y,z)\longmapsto(z+4y^2,y).
\]

The two other collision points lie on the component \(L=0\), which is
\(\mathbb G_m\times\mathbb A^1\), not an affine plane. In coordinates
\((x,u)\), with \(x\ne0\),

\[
a=\frac{(u+1)(u+2)}{x^2},\qquad
b=\frac{4u+6}{x},\qquad
\frac{\partial(a,b)}{\partial(x,u)}=\frac{2}{x^4}.
\]

Thus the most direct two-dimensional slice is Laurent and has variable
ordinary Jacobian. It does not supply a polynomial map
\(\mathbb A^2\to\mathbb A^2\).

The most symmetric nonlinear target section fails as well.  For
\[
\Delta(A,B,C)=\operatorname{disc}_T(CT^3-2T^2+BT-2A),
\]
the pullback \(\Delta\circ F\) is a polynomial submersion and all three
collision points lie on its level \(16\).  That level is smooth and
irreducible, but an exact two-sheeted projection calculation gives Euler
characteristic \(3\), so it is not \(\mathbb A^2\).  See
`DISCRIMINANT_FIBER_NO_GO.md`.

A substantially broader common-coordinate descent is impossible.  If a
target coordinate \(R\) has \(R\circ F\) as a source coordinate, source
and target automorphisms rectify the threefold map to \((t,p,q)\).
Generic \(t=c\) slices are then plane polynomial maps with constant
Jacobian and geometric degree three, contradicting Orevkov's theorem on
three-sheeted polynomial maps of \(\mathbb C^2\).  This includes wild
nonlinear coordinates.  See
`THREE_DIMENSIONAL_COORDINATE_SLICE_OREVKOV_NO_GO.md`.

For the generic-degree-six weighted lift, every polynomial graph source
followed by every rank-two linear target projection is excluded as well.
The three possible target-minor Jacobians have distinct nonzero leading
degrees, including on a graph containing all six displayed collision
points.  Thus any surviving descent from the weighted-lift family must
use a nonlinear target projection or a non-graph affine-plane embedding.
See `WEIGHTED_LIFT_DEGREE_SIX_GRAPH_PROJECTION_NO_GO.md`.

The primitive nonlinear cancellation \(p_5^6A^5C^4-q_6^5B^6\) has now
been subducted through two exact SAGBI stages.  All graph-leading forms
are excluded except two sparse Newton rays for the \(A\)- and
\(B\)-pivots; the \(C\)-pivot is excluded uniformly.  See
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.
Both rays are subsequently excluded for every parameter: one has an
unavoidable weighted-Euler defect and the other requires a forbidden
\(x^1\) graph term.  See
`WEIGHTED_LIFT_SECOND_SUBDUCTION_RAY_CLOSURE.md`.
The general mixed linear pivot is now excluded too.  The coupled
\(A/B\) characteristic solution has a highest-\(y\), \(x^1\) coefficient
independent of the mixing ratio; in a \(B/C\) mixture, \(C\) enters only
after the already nonzero \(B\)-defect.  Constant graphs have separated
nonzero top forms.  Hence every
\((U+L,\alpha A+\beta B+\delta C)\) fails on every polynomial graph, and
the next honest target must have a genuinely nonlinear second
coordinate.  See `WEIGHTED_LIFT_MIXED_LINEAR_PIVOT_CLOSURE.md`.
The next homogeneous layer was classified through target degree two.  One
characteristic equation classifies the \(A^2\), \(AB\), and \(B^2\)
Newton faces; the new \(AB\) ray forces a forbidden \(x^1\) graph term.
Mixed \(AC/BC\) forces a negative infinity-chart power, \(BC\) has no
resonance, and \(C^2\) reduces to the linear theorem.  The former
pure-\(AC\) boundary proof was not exact, and a lower \(B\) term can
enter the same first-lower sector.  The arbitrary-lower-tier quadratic
claim is therefore open on \(AC+B\).  See
`WEIGHTED_LIFT_ALL_QUADRATIC_PIVOT_CLOSURE.md`.
The cubic classification retains the \(A^2B\) forbidden-\(x^1\) ray,
the mixed negative-tail cases, and the nonresonant \(C\)-faces.  Its
former pure-\(ABC\) boundary proof was not exact, and a lower \(B^2\)
term can enter the same first-lower sector.  The arbitrary-lower-tier
cubic claim is therefore open on \(ABC+B^2\) and also inherits the
lower quadratic \(AC+B\) chain.  See
`WEIGHTED_LIFT_ALL_CUBIC_PIVOT_CLOSURE.md` and
`WEIGHTED_LIFT_C_DIVISIBLE_CUBIC_FACE_CLOSURE.md`.  The exact
cancellation ratios and polynomial first-lower solutions are recorded
in `WEIGHTED_LIFT_QUADRATIC_CUBIC_LOWER_TIER_CORRECTION_AUDIT.md`.
The quartic layer has nine exact rays, two finite coefficient
recurrences, and an exact next-diagonal certificate for the sole
constant-graph \(AB^3\) degeneracy.  A correction audit found that the
claimed arbitrary-lower-tier theorem remains open on two pure rays:
\(AB^2C+B^3\) and \(A^2C^2+ABC\).  In each, the cubic coefficient can
cancel the first-lower double pole and the remaining Laurent-sector
equation is polynomially solvable.  See
`WEIGHTED_LIFT_ALL_QUARTIC_PURE_FACE_CORRECTION_AUDIT.md`.
The all-degree binary
characteristic also closes every pure binary monomial face, all binary
targets through degree five, and—after its exact first lower-seed
recurrence—the first sextic completion
\(B^5(\lambda A+\mu B)\).  The latter residue is
\(-(221578k+153403)/510\).  Quintic \(C\)-divisible faces and
non-graph source surfaces are the first unresolved full layers.  See
`WEIGHTED_LIFT_ALL_QUARTIC_PIVOT_CLOSURE.md`,
`WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_REDUCTION.md`, and
`WEIGHTED_LIFT_DEGREE_SIX_EXCEPTIONAL_RECURRENCE_CLOSURE.md`.
The sextic computation is the first instance of a uniform result:
every binary Newton-degree-one face
\[
B^{n-1}(\lambda A+\mu B),\qquad n\ge1,\quad\lambda\ne0,
\]
has a nonzero first-lower source-axis residue.  Its numerator is
\[
2975In^2+952In-2023I-3035n^2+22780n-1785>0
\]
for all graph sectors \(I\ge2\).  Graph corrections start in \(x^2\)
and cannot change it.  Thus the next unresolved binary characteristic
has Newton degree at least two.  See
`WEIGHTED_LIFT_ALL_DEGREE_D1_RECURRENCE_CLOSURE.md`.
The exact maximal-\(x\) filtration closes those remaining binary
characteristics as well.  Every one of the 77 lower \(U\)-support
terms, and every lower \(A/B\) seed, lies below the maximal Laurent
sector \(x^I\psi_I(t)\); only the top support reaches \(x^I\), and
only the first-lower support reaches \(x^{-1}\).  Hence a
nonpolynomial characteristic is impossible in every degree, while a
mixed polynomial completion meets the nonzero double-pole obstruction.
Pure faces and constant graphs are separately exact.  Therefore every
homogeneous binary target \(Q_n(A,B)\), \(n\ge1\), is excluded on every
polynomial graph.  See
`WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md`,
`WEIGHTED_LIFT_GENERAL_BINARY_FIRST_LOWER_POLE_OBSTRUCTION.md`, and
`WEIGHTED_LIFT_ALL_DEGREE_D2_RECURRENCE_CLOSURE.md`.
Every nonzero homogeneous ternary target is now closed in every
degree.  The corrected proof chooses the globally earliest
source-boundary face of the whole target.  For a regular graph
boundary, exact full-seed gaps isolate its Wronskian; for a graph with
a boundary pole, cancellation at \(u=1\) forces a sign condition that
contradicts the leading coefficient at \(u=\infty\).  Therefore
\[
\left(U+R_{\le1}(A,B,C),\,Q_n(A,B,C)+c\right)
\]
cannot have nonzero constant restricted Jacobian on a polynomial
graph when \(Q_n\ne0\) is homogeneous, \(R_{\le1}\) is affine, and
\(c\) is constant.  See
`WEIGHTED_LIFT_GLOBAL_MINIMAL_BOUNDARY_FACE_CLOSURE.md`.

The earlier facewise Euler proof was genuinely invalid: at
\(t=u/x\), exact seed layers coalesce and higher-\(C\) monomials can
share or precede the chosen boundary order.  Its correction history is
kept in `WEIGHTED_LIFT_TERNARY_PURE_BOUNDARY_SEPARATION_AUDIT.md`;
the degree-six full-seed calculation remains a useful special case.

The primitive nonhomogeneous target problem is closed first through
total target degree eight.  The globally earliest regular vertex is indexed by
\((\beta,h)\), while the polar face is indexed by \((E,q)\); both maps
have primitive collision kernel
\[
\mathbb Z(5,-6,4).
\]
No two support monomials of degree at most eight can differ in this
direction, so for every nonconstant \(Q\) in that range and every
\(R_{\le2}\),
\[
J(U+R_{\le2},Q)\notin\mathbb C^\times.
\]
The same proof closes the four formerly open remove-one-\(C\) chains.
An explicit \(A^3/A^2B\) bifiltration then restores the bounded quartic
scope when combined with the cases surviving its correction audit.
See `WEIGHTED_LIFT_NONHOMOGENEOUS_NEWTON_VERTEX_CLOSURE.md`.

The first possible support collision is degree nine,
\(A^5C^4\sim B^6\).  Exact replacement by the first cusp subduction
\(T\) closes arbitrary targets through degree nine.  Through degree ten,
the four collision pairs are the primitive pair and its multiples by
\(A,B,C\).  Replacing them triangularly by \(T,AT,W,U\), then removing
the \(U\)-coefficient modulo the actual first coordinate
\(U+R_{\le2}\), leaves isolated augmented Newton atoms.  The sole polar
collision \(W\sim A^2B^3\) has an exact two-term Wronskian that never
vanishes.  Consequently, for every nonconstant target \(Q\) of degree at
most ten and every \(R_{\le2}\),
\[
J(U+R_{\le2},Q)\notin\mathbb C^\times
\]
on every polynomial graph.  See
`WEIGHTED_LIFT_NONHOMOGENEOUS_DEGREE_NINE_CUSP_CLOSURE.md` and
`WEIGHTED_LIFT_NONHOMOGENEOUS_DEGREE_TEN_NEWTON_BASIS_CLOSURE.md`.
Through degree eleven there are ten cusp collisions, triangularly
replaced by products of \(T,W,U\).  Nine augmented atoms remain after
the same first-coordinate reduction.  All regular boundaries are
separated, including four exact \(L=1\) two-dimensional groups.  At a
pole, four of the six repeated groups are nonresonant.  The two
remaining characteristic rays are closed at their first lower
total-\(\gamma\) layer by local Laurent-jet determinants
\[
\Delta_{BW/AT}\doteq(17k-5)(105k-32),\qquad
\Delta_{AU/W}\doteq(17k-13)^2.
\]
These depend only on the graph's forced 1-jet and are independent of
every higher zero-sector coefficient.  Consequently the same
nonconstant-target obstruction holds through target degree eleven.
See
`WEIGHTED_LIFT_NONHOMOGENEOUS_DEGREE_ELEVEN_NEWTON_BASIS_CLOSURE.md`.

These finite-dimensional theorems do not give a complete SAGBI normal
form.  The next exact saturation \(BT\sim A^5C^3\) produces a new
generator outside
\(\langle A,B,C,T,U\rangle\), with distinct \(L=1\) and \(L\ge2\)
leading behavior.  See
`WEIGHTED_LIFT_SAGBI_SATURATION_NEXT_GENERATOR_AUDIT.md`.

After adjoining that first new element \(W\), the formal
three-component toric ideal has an exact eight-binomial minimal Markov
basis.  The graph-degree projection is subtler: the next element \(V\)
is projected-new for \(L=2\) and \(L\ge4\), but has exactly two reducers
at \(L=3\).  A subsequent element \(X\) is projected-new relative to
the displayed seven generators for every \(L\ge2\).  This proves
additional incompleteness without claiming termination or infinitude.
The apparent cubic exception is now closed exactly: after the two
degree-\(139\) reducers, the fixed graph jets force the remainder into
an unreducible gap at degree \(138\), \(136\), or \(133\), according to
three explicit coefficient strata.  Thus \(V\) exposes a new projected
value for every cubic graph as well.  See
`WEIGHTED_LIFT_SAGBI_AFTER_W_MARKOV_AND_NEXT_GENERATORS.md` and
`WEIGHTED_LIFT_CUBIC_GRAPH_V_SUBDUCTION_CLOSURE.md`.

On the independent Route A cubic normalization, the residual factor
\(\tau^2=g(v)\) has also been audited at infinity.  After removing
squares it is \(\mathbb C(v)(\sqrt{s})\), ramified at infinity exactly
when \(\deg g\) is odd.  The two canonical quadratic-pseudoplane
valuations instead split the distinguished cubic sheet, so their deck
pairing imposes no parity on the residual two sheets.  An explicit
Miranda family realizes every squarefree degree and parity with a
connected finite-flat cubic cover, an everywhere-étale distinguished
section, and a smooth normal total surface.  Any contradiction therefore
needs a genuinely global theorem coupling residual monodromy to the
non-distinguished dicritical defect.  See
`ROUTE_A_RESIDUAL_QUADRATIC_INFINITY_AUDIT.md`.
The canonical finite degree-six compactification shows that even this
point-to-defect bridge is unavailable.  Finite odd residual places are
points on already-existing cubic boundary components; the distinguished
lift stays on the single divisor \(D_-\) with local degree one, and the
four missing residual sheets are reused at each intersection.  The deck
involution exchanges omitted \(D_-\) with retained \(D_+\), while its
behavior over cubic boundary primes is controlled by divisorial
valuation data rather than root parity.  An exact model places
arbitrarily many odd roots on one ramification component.  The viable
next input is a projective intersection bound for the fixed boundary
curves.  See
`ROUTE_A_GLOBAL_MONODROMY_DICRITICAL_BRIDGE_NO_GO.md`.
The corresponding projective intersection ledger is exact but still
nonrestrictive:
\(\deg g+I_\infty=M\delta\).  Localization from the plane open makes
the affine class group free on all boundary primes, while repeated
blowups at the unique infinity end vary the raw adjunction labels
without changing any affine datum.  Smooth branch curves and connected
cubic families realize the resulting freedom.  See
`ROUTE_A_PROJECTIVE_INTERSECTION_BOUND_NO_GO.md`.
The canonical local arm has now been extracted exactly: four ordinary
point blowups produce \(D_-\), with
\(\operatorname {ord}(a,s,s+a^2)=(1,2,4)\) and residue parameter
\((s+a^2)/a^4\).  But this does not determine the cubic-boundary arms.
The one-place family with infinity pair \((k,2k+1)\) has multiplicity
sequence \((k,k,1,\ldots,1)\) and requires exactly \(k+2\) blowups.
That singular injective cusp supplies no Keller map or monodromy data,
and the componentwise form of the cited Chau results does not exclude it.
It proves that the chart, Bézout ledger, and canonical minimality alone
cannot bound the target tree.  A viable Route A theorem must now cross
the distinguished and cubic-boundary arms through a Keller-specific
determinant or finality relation.  See
`ROUTE_A_CANONICAL_INFINITY_TREE_FLEXIBILITY.md`.
The global log topology now sharply reduces those unknown arms.  Since
the pseudoplane is a rational \(\mathbf Q\)-homology plane, every SNC
completion boundary is a rational tree and every boundary singularity
has a rational-homology-sphere link.  Hence
\(H_c^1(R;\mathbf Q)=0\).  The cubic fiber-length obstruction transfers
unibranchness to the branch curve, and
\(r+c+N_{\mathrm{tr}}=2\) forces \(r=c=1\) and
\(N_{\mathrm{tr}}=0\).  The hypothetical cubic cover therefore has one
rational unibranch boundary component, one irreducible branch curve
with bijective \(\mathbf A^1\)-normalization, and no affine transitive or
non-Gorenstein fiber.  A singular cusp is not excluded by the cited
Chau results, so the remaining target is its single-place monodromy at
infinity.  See `ROUTE_A_LOG_TOPOLOGY_CUBIC_COLLAPSE.md`.
The two simplest ways to upgrade this collapse are now ruled out.
The local \(A_{2m}\) double-plane model has a rational-chain
resolution, \(C_2\) inertia, and a singular bijectively normalized
cusp, so rational-tree topology does not force \(\Delta\) smooth.
Also \(A_H=\Gamma_D\cup\Delta\), while the distinguished curve already
has free rank \(\rho_\Gamma\ge1\) from its forced normalization
self-identification.  If the curves meet in \(k\ge1\) affine points,
\(\pi_1(A_H)=F_{\rho_\Gamma+k-1}\); if not, the union is disconnected.
Hence Chau's full-set simply-connected prohibition does not apply.
See `ROUTE_A_SINGLE_INFINITY_GRAPH_NO_GO.md`.
The cubic cover is nonetheless impossible.  The retained prime cannot
meet the sole ramified boundary prime, since that would merge the
degree-two and degree-one specializations into a forbidden one-support
fiber.  It is therefore a closed, unpunctured curve \(C\subset S\), and étale
base change makes \(C\to\Delta\) a finite étale map of rank one, hence
an isomorphism.  Zaidenberg's singular-homology-line theorem forces
\(C\) and \(\Delta\) to be smooth affine lines because
\(S\not\simeq\mathbf A^2\).  After Abhyankar--Moh--Suzuki
rectification, the complement has cyclic fundamental group; its branch
meridian is a transposition and cannot generate connected cubic
monodromy.  Thus \(S(2,2,1)\) has no étale map to \(\mathbf A^2\) of
geometric degree three.  See
`ROUTE_A_CONTRACTIBLE_RETAINED_SHEET_CUBIC_EXCLUSION.md`.

The degree-four successor now has exact Euler bookkeeping.  If
\(c,r,t,\delta\) denote branch components, boundary components,
triple-inertia components, and unibranch support-orbit deficit, then
\[
r=3-c-t-\delta,\qquad r\ge c.
\]
This forces one branch component and three numerical cases.  Triple
inertia is impossible.  The two simple-inertia survivors are localized
to a \(3+1\) collision plus a \(2+2\) self-intersection, or to an extra
unramified boundary curve puncturing both split residual sections.  This
is not yet a degree-four exclusion; it identifies the exact new
obstruction.  See
`ROUTE_A_DEGREE_FOUR_RETAINED_SHEET_AUDIT.md`.
The survivors now have exact normalization profiles.  In the
\(3+1\)/self-intersection case, residual ramification is governed by
intersection parity; with \(n\) two-branch values and \(e\) odd
contacts, the retained Euler characteristic is \(1-4n\), and a
connected completion has genus \(e-1\).  In the extra-boundary case,
the split residual affine lines lose \(k_1,k_2\ge1\) points and have
equal classes in \(\operatorname {Cl}(S)=\mathbf Z/2\).  Every
\(r=2,\delta=0\) survivor is Gorenstein with
\(\omega_Y\simeq\mathcal O_Y(E)\) and Cartier \(E\); the only
non-Gorenstein \(3+1\) escape forces branch multiplicity at least four.
See `ROUTE_A_DEGREE_FOUR_SURVIVOR_NORMALIZATION_PROFILE.md`.
The remaining canonical and log-adjunction identities have now been
tested against both profiles.  Exact local curve and finite-cover models
realize every required degree, conductor, ramification, and deleted-divisor
ledger; in particular the adjunction divisor is distinct from the
log-puncture divisor.  These identities therefore do not eliminate either
survivor.  This is a scoped feasibility result, not a global Keller model.
See `ROUTE_A_DEGREE_FOUR_LOG_ADJUNCTION_FEASIBILITY.md`.

A new generic-fiber theorem gives a structural restriction in every
degree.  A Darboux coordinate on the quadratic pseudoplane cannot have
split generic fiber \(\mathbb A^1\) or \(\mathbb G_m\): the Hamiltonian
slice makes the first case birational and the second a cyclic Galois
extension, while units, purity, and the nontrivial class group exclude
both.  The Galois pseudo-covering ingredient is prior work of Miyanishi;
the new synthesis is its coupling to the slice equation and the quartic
inertia profiles.  In either quartic survivor, a geometrically rational
generic fiber has at least four punctures.  In the one-boundary survivor,
if both coordinate fibers are rational, at least one has at least six
punctures and the projective branch curve has degree \(4\), \(5\), or
\(6\).  See
`ROUTE_A_LOW_LOG_COMPLEXITY_FIBER_OBSTRUCTION.md`.

Those three remaining branch degrees cannot be eliminated by finite
curve geometry alone.  Explicit polynomial normalizations in degrees
\(4,5,6\) realize the required cusp, node, one-place-at-infinity,
delta, puncture, and local \(S_4\)-permutation ledgers.  They do not
construct a finite surface cover: the unresolved invariant is the
global braid-monodromy representation of the curve complement.  See
`ROUTE_A_QUARTIC_BRANCH_DEGREES_FOUR_TO_SIX_FEASIBILITY.md`.

For case c, the corrected degree-four outer cover has now been tested
against every linear jet adjoint through derivative order three.  Both
capped new-block maps are surjective modulo \(E^j\) for
\(j=1,2,3,4\); at \(E^5\), Hermite coordinates merely recover the old
bounded row cokernels.  Their unique common linear adjoint is the
outer-independent support coefficient \([h^{19}]\).  Consequently no
scalar transvectant with the outer quartic can couple the caps; the next
finite-support invariant must be nonlinear in existing cokernel values.
See `CASE_C_OUTER_QUARTIC_ADJOINT_NO_GO.md`.
The first such nonlinear tests are nondegenerate: the two canonical
residual adjoint lines have nonzero norms, trace-Gram determinant, and
Wronskian norm at all five outer points, while the weight-nine
determinant of their source cokernel vectors is a nonzero polynomial
rather than an identity.  The next case-c target must therefore use a
later bounded row or a multistage relation, not only the first two
cokernel planes.  See
`CASE_C_COKERNEL_NONLINEAR_PAIRING_NO_GO.md`.
A complete later-jet rank staircase now finds the first such positive
invariant.  The deficit-\(4,5,6\) residual adjoints span the trace-zero
quartic algebra, so the smallest three-stage Gram determinant is again
nonzero.  But the unique deficit-eight adjoint modulo \(E^3\) evaluates
to \(C_8X_6^2\) on the deepest weight-four branch, with \(C_8\ne0\);
it canonically forces \(X_6=0\).  This compresses the five old
special-chart rows into one terminal scalar without replacing the
generic-chart certificates.  See `CASE_C_MULTISTAGE_JET_STAIRCASE.md`.

The fixed source plane now has a sharper global obstruction candidate.
Its conductor completion admits an exact formal Darboux pair, so local
parity and completion arguments alone cannot work.  Rational descended
charts instead retain a logarithmic class in the one-dimensional kernel
\[
\ker\bigl(H^1_{\rm dR}(X^\circ)\to H^1_{\rm dR}(C^\circ)\bigr)
=\mathbf Q\,d\log(x/c).
\]
Both natural monomial orientations land in a nonzero odd residue coset,
but the corresponding rational parity conjecture is false.  Exact
endpoint-neutral canonical scalings preserve conductor and Darboux data
while moving the odd class to interior level divisors.  They introduce
affine poles, so the remaining polynomial question is global
pole-freeness/termination rather than residue parity.  See
`FIXED_PLANE_RESIDUE_PARITY_SCALING_NO_GO.md`.

The first-order Hermite--CRT Keller jet in fact lifts through every
finite normal order along \(E=DK\): \(\{U,E\}\) is a unit modulo \(E\),
so an explicit Hensel recurrence constructs compatible polynomial
solutions modulo \(E^N\) for every \(N\).  Thus no finite thickening can
supply the hoped-for obstruction.  For the fixed lift \(U_0\), a
squarefree degree-\(14\) eliminant instead exhibits fourteen critical
points, all off \(E=0\), which forbids any global polynomial
\(V\) with \(\{U_0,V\}=1\).  The surviving question is whether
\(U_0+E^2\phi\) can remove this global critical scheme while preserving
the established boundary jets.  See
`FIXED_PLANE_ALL_ORDER_HERMITE_CRT_LIFT.md`.
All fourteen points are Morse and persist uniquely under every formal
\(U_0+\epsilon E^2\phi\).  For each degree bound, a dense open subset
of the full coefficient space still contains a finite-étale
degree-\(14\) critical subscheme, so any successful perturbation must
be exceptional and nonperturbative.  The scalar test \(U_0+E^2\) has
exactly \(21\) distinct off-boundary critical points.  The next
well-posed task is the projective critical-incidence locus, not a random
coefficient search.  See
`FIXED_PLANE_CRITICAL_PERSISTENCE_AND_SCALAR_PERTURBATION.md`.
That projective analysis is now exact on the two natural scalar rays.
For \(U_0+\lambda E^2\), the affine critical length is generically \(21\)
and drops to \(20\) at
\(\lambda=(-71\pm17\sqrt{17})/2592\), with one point escaping to
infinity.  For \(U_0+\lambda tE^2\), the exceptional lengths are
\(19\) at \(9/8\) and \(20\) at \(-1/972\); at \(-1/24\) the length
remains \(21\), including two explicit simple points on \(c=0\).
Neither ray contains a polynomial submersion.  The calculation also
shows why leading homogeneous support alone cannot control projective
intersection multiplicity.  See
`FIXED_PLANE_PROJECTIVE_CRITICAL_SCALAR_RAYS.md`.

An independent all-degree formulation is recorded in
`STANDARD_SYSTEM_WEIGHTED_ESCAPE.md`.  In the finite standard system
equivalent to a counterexample, the equation-Jacobian has exact weight
\((m-1)(n-1)\) and is a nonzero constant along a Keller section.  The
natural degeneration forces that section to escape to weighted infinity,
so the missing theorem is a classification of boundary arcs rather than
an affine monodromy or larger Groebner calculation.
The first normal-form step has now been corrected.  For
\(P=R^aA(z)\), \(Q=R^bB(z)\), an honest approximate-root change can
normalize one of \(A,B\), but the relative unit
\[
\mathcal I=B^a/A^b=Q^a/P^b
\]
survives up to tangent-to-the-identity composition.  Its first nonzero
jet is quotient-invariant, and exact degree-bound-compatible examples
show it need not vanish.  The relative logarithm satisfies an exact
linear transport equation; lower \(g\)-multiple relative jets decouple
from the final \((-2\bmod g)\) forcing.  The actual unresolved mixing is
the non-\(g\)-multiple \(Z=0\) nilpotent cascade, together with the
affine endpoint pairing.  See
`STANDARD_SYSTEM_G_MULTIPLE_REPARAMETRIZATION_QUOTIENT.md`.
The endpoint pairing itself is now known to be invisible to ordinary
normalization-branch residues.  Exact reciprocal affine tails contribute
\((sv-ut)\tau^{m+n-2}\ne0\) to the homogenized bracket, yet over every
simple common-root cluster the unique ramified branch has
\[
\operatorname {ord}_t(\tau^{m+n-2}/P_X)
=am+a(g-1)-1>am.
\]
Thus every branch coefficient tested by the exact differential vanishes.
This is not a Keller countermodel—the earlier leading/tail cross terms
remain—but it proves that the endpoint class must be quotiented before a
global pole-filtered monodromy obstruction can begin.  See
`STANDARD_SYSTEM_ENDPOINT_PAIRING_BRANCH_INVISIBILITY.md`.
That quotient cannot be taken naively.  The endpoint-invisible affine
pairings span the entire scalar forcing line, so quotienting all of them
also kills the Keller forcing.  On the other hand, no nonzero pure affine
tail solves its earlier cross equation.  Its endpoint contribution is
therefore meaningful only after the lower nilpotent jets have been
lifted.  See `STANDARD_SYSTEM_ENDPOINT_QUOTIENT_NO_GO.md`.

A separate audit corrected the first-normal-direction determinant
contact.  If \(q=\lfloor b/a\rfloor\), \(r=b-aq\), and \(Q_q\) retains
the polynomial binomial terms of
\((R^a+\epsilon T)^{b/a}\), then the exact derivative identity
\[
(Q_q)_X-H_\epsilon(R^a+\epsilon T)_X
=r\binom{b/a}{q}\epsilon^qR^{r-1}R'T^q
\]
gives, on a natural Zariski-open set,
\[
\operatorname {ord}_\epsilon
\operatorname {Res}_X\bigl((R^a+\epsilon T)_X,(Q_q)_X\bigr)
=gb-q-1.
\]
Thus the first Laurent pole and the derivative-resultant remainder
belong to different filtrations.  See
`STANDARD_SYSTEM_SYLVESTER_REMAINDER_CORRECTION_AUDIT.md`.

That corrected remainder is not itself a lifted obstruction.  For every
allowed two-jet \(P=R^a+\tau^dT+\tau^{2d}S\), its entire
division-free remainder has a polynomial primitive satisfying the
reciprocal \(Q\)-degree bounds.  Adding the ambient
\(\tau^{m-1}X\) direction then gives exact maximal derivative-resultant
contact.  The construction is not a standard-system or Keller solution:
the primitive is a free physical relative correction, not necessarily
one of the scalar \(\lambda_k\tau^kC^{m-k}\) combinations.  It proves
that the next obstruction must use that narrower presentation or the
Keller bracket itself.  See
`STANDARD_SYSTEM_TWO_JET_DERIVATIVE_LIFT_COUNTERMODEL.md`.

The Keller bracket does give a positive face theorem.  A single
root-vanishing binomial face has an uncancellable terminal unless it is
the already known \(g\)-sector monomial
\[
T=cR^\sigma,\qquad d=g(a-\sigma).
\]
For an entire isolated compact matched face, including all interior
monomials, every strict-slope kernel is instead a reduced common-root
shift; equality of slopes is precisely the physical \(g\)-sector
resonance.  This is a rigorous face classification, but it does not yet
control post-resonant cascades or repeated common roots.  See
`STANDARD_SYSTEM_SINGLE_BINOMIAL_FACE_NO_SCALAR.md`.

For an actual polynomial Keller pair with squarefree common root, the
matched-\(Q\)-face hypothesis is automatic at every strict first local
\(P\)-slope.  The Euler defect excludes all lower \(Q\)-faces, and the
weight lattice leaves a unique matched residue coset.  The resulting
local reduced shifts glue simultaneously in \(P\) and \(Q\) to a
degree-compatible global change
\[
R\longmapsto R+\tau^E\dot R(X).
\]
This closes the pre-resonant matching and gluing gap.  See
`STANDARD_SYSTEM_STRICT_COMPACT_FACE_BRIDGE.md`.

The squarefree case is now closed completely.  After the subresonant
bridge, any least residual below a slope-\(g\) sector would expose a
strict face and hence an already-vanished primitive shift.  The
reciprocal degree average then forces every surviving layer to be a
scalar \(g\)-sector.  Thus
\[
P=S^aA(\tau^g/S),\qquad Q=S^bB(\tau^g/S)
\]
for a reciprocal polynomial approximate root \(S\).  The homogenized
Keller bracket of every such pair vanishes identically, contradicting
its nonzero scalar forcing.  Therefore an actual reciprocal Keller pair
cannot have squarefree common-root boundary.  This is a boundary
exclusion theorem, not a proof of the plane Jacobian conjecture; see
`STANDARD_SYSTEM_SQUAREFREE_COMMON_ROOT_EXCLUSION.md`.

For repeated roots, the strict local compact-face calculation still
forces a common deformation, and the globally first \(P\)-coefficient
has the exact form
\[
T=aR^{a-1}L,\qquad \deg L\le g-E.
\]
The matching \(Q\)-coefficient differs only by a polynomial Kummer mode
\(cR^{b-E/g}\), which exists exactly when \(g\mid e_iE\) at every root
multiplicity \(e_i\).  These results are deliberately fixed-base and
first-layer only: after the deformation, repeated factors may split and
the argument cannot yet be iterated.  See
`STANDARD_SYSTEM_REPEATED_ROOT_COMPACT_FACE.md` and
`STANDARD_SYSTEM_REPEATED_ROOT_GLOBAL_FIRST_LAYER.md`.

The polynomial Kummer modes themselves have now been followed through
all mutual nonlinear interactions.  If
\[
d=\gcd(g,e_1,\ldots,e_r),\qquad \kappa=g/d,\qquad R=H^d,
\]
then the pure fixed-base modes span the exact zero-bracket cone
\[
P=\sum A_j\tau^{\kappa j}H^{da-j},\qquad
Q=\sum B_j\tau^{\kappa j}H^{db-j}.
\]
For \(\kappa>1\), both dehomogenized top derivatives in this cone share
\(x^{\kappa-1}\), so they cannot satisfy the first scalar Bezout
equation.  Any Keller candidate must therefore introduce a top form
outside \(\mathbb C[x^\kappa]\).  This is a necessary escape theorem,
not an exclusion of repeated roots; see
`STANDARD_SYSTEM_REPEATED_ROOT_KUMMER_NONLINEAR_AUDIT.md`.

The first secondary Rees chart is now exact at the residual zero root.
At every strict secondary slope the lowest \(Q\)-face is automatically
matched, and its scalar term is impossible.  A matched resonant face has
zero bracket, an isolated matched super-slope face violates the reciprocal
degree bound, and a direct super-face/Kummer scalar is impossible as well.
For arbitrary anchored faces, every nonzero terminal scalar pulls back to
the original affine defect-one coefficient pair.  This is not yet a
repeated-root exclusion: an unmatched chain may cancel successive
non-scalar terms before reaching that terminal.  The occupied-support
convention and exact arbitrary-anchor operator are recorded in
`STANDARD_SYSTEM_REPEATED_ROOT_ZERO_RESIDUAL_SECONDARY_FACE_NO_GO.md`.

The proper-divisor descent in Makar-Limanov--Trakhtenberg does not close
that chain.  Even assuming the Rees cancellations embed into their Newton
resolution, it only makes the nonprincipal power stages finite before a
principal edge.  The principal category is genuinely populated by an
explicit Laurent face with Jacobian one, and its reciprocal terminal is
the ordinary defect-one Bezout equation
\[
p_0'q_1-p_1q_0'=c.
\]
Thus power-index descent is a route to the lifted endpoint, not an
obstruction to it.  See
`STANDARD_SYSTEM_POWER_INDEX_PRINCIPAL_FACE_BRIDGE_AUDIT.md`.

On Route A, each of the three explicit degree-\(4,5,6\) branch curves
has a full-degree \((3,2)\) cusp for the trigonal projection.  A small
generic vertical fiber lies entirely in the cusp Milnor ball, so its
local cusp group surjects onto the global affine complement group.
Two transposition meridians satisfying the cusp braid relation generate
at most an \(S_3\) fixing one of four letters.  Hence none of these
three curves supports the required transitive \(S_4\) monodromy.  No
claim about the full complement fundamental group is made; see
`ROUTE_A_TRIGONAL_CUSP_GLOBAL_MONODROMY_OBSTRUCTION.md`.

The same monodromy idea closes the complete four-puncture equality case,
not just those three examples.  In the one-boundary quartic survivor,
four punctures would make the branch normalization map to either
coordinate line with degree three.  The cubic has either one totally
ramified critical point, whose local nontransitive image generates
globally, or a second critical point that reduces the global image to at
most two transpositions or a local \(2+2\) image.  Thus every rational
generic \(P\)- or \(Q\)-fiber in this profile has at least six punctures.
Six-or-more punctures, positive genus, and the two-boundary survivor
remain open; see
`ROUTE_A_QUARTIC_MINIMAL_PUNCTURE_MONODROMY_OBSTRUCTION.md`.

On the independent Danielewski-surface route, changing the affine-plane
chart cannot rescue a Chebyshev étale endomorphism.  A preserved boundary
line would make its \(z\)-coordinate satisfy a polynomial semiconjugacy
with an affine-linear self-map, forcing that coordinate to be constant.
The four resulting lines are then separated by their Picard classes and
explicit inverse images.  Thus no degree-\(d>1\) Chebyshev map, nor any
surface-automorphism conjugate of one, preserves an \(\mathbb A^2\) chart;
see `route_c/ROUTE_C_MEMO.md`.

Run `python current_context/verify_3d_descent.py` with SymPy available to
check every displayed identity exactly.

## Primary current reference

T. Shaska, *Graded Keller maps and the Jacobian Conjecture*,
[arXiv:2607.20210](https://arxiv.org/abs/2607.20210), submitted
22 July 2026. The paper also proves that every
\(\mathbb G_m\)-equivariant plane Keller map is an automorphism, so a plane
counterexample cannot be obtained by copying the grading of the
three-dimensional construction unchanged.
