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

The nonhomogeneous target problem is now closed through total target
degree eight.  The globally earliest regular vertex is indexed by
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
\(A^5C^4\sim B^6\).  The known subductions \(T,U\) do not yet give a
complete SAGBI normal form: the next exact saturation
\(BT\sim A^5C^3\) produces a new generator outside
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
See `WEIGHTED_LIFT_SAGBI_AFTER_W_MARKOV_AND_NEXT_GENERATORS.md`.

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

An independent all-degree formulation is recorded in
`STANDARD_SYSTEM_WEIGHTED_ESCAPE.md`.  In the finite standard system
equivalent to a counterexample, the equation-Jacobian has exact weight
\((m-1)(n-1)\) and is a nonzero constant along a Keller section.  The
natural degeneration forces that section to escape to weighted infinity,
so the missing theorem is a classification of boundary arcs rather than
an affine monodromy or larger Groebner calculation.

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
