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
That next layer is now closed through target degree two.  One
characteristic equation classifies the \(A^2\), \(AB\), and \(B^2\)
Newton faces; the new \(AB\) ray forces a forbidden \(x^1\) graph term.
Mixed \(AC/BC\) forces a negative infinity-chart power, pure \(AC\)
has a fixed Euler defect, \(BC\) has no resonance, and \(C^2\) reduces
to the linear theorem.  Hence every affine quadratic second coordinate
fails on every polynomial graph.  Cubic target faces and non-graph
source surfaces remain open.  See
`WEIGHTED_LIFT_ALL_QUADRATIC_PIVOT_CLOSURE.md`.

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
cubic families realize the resulting freedom.  Route A now requires a
canonical-minimal infinity-tree theorem controlling \(I_\infty\) and
\(\delta\) together.  See
`ROUTE_A_PROJECTIVE_INTERSECTION_BOUND_NO_GO.md`.

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
