# Status and strategic pivot — 26 July 2026

## Executive status

The plane Jacobian conjecture is not resolved here.  No counterexample
has been constructed, and no proof of \(JC(2)\) has been obtained.

Three independently checkable advances were completed after the
25 July checkpoint:

1. The Gallagher weighted-lift polynomial-graph obstruction now covers
   every nonconstant, not necessarily homogeneous target of degree at
   most eleven.
2. The projective critical schemes on the two natural scalar
   fixed-plane perturbation rays are classified exactly; every member
   of both rays has an affine critical point.
3. The remaining Route A degree-four log-canonical and adjunction
   ledgers are shown to be feasible, so that line of scalar
   bookkeeping cannot eliminate the two surviving quartic profiles.

The first result has been integrated into the standalone
computer-assisted preprint
`papers/weighted-lift-newton-obstructions/main.tex`.  Its exact theorem
note and verifier passed three independent adversarial reviews after
two genuine proof omissions and two presentation/exhaustiveness defects
were repaired.  The 14-page PDF was rebuilt and inspected page by page.

These are publishable scoped results, not a resolution of the
two-dimensional conjecture.

## 1. Degree-eleven weighted-lift theorem

Let \(F=(A,B,C)\) be the exact Gallagher weighted lift, let \(U\) be its
second-subduction coordinate, and let \(R_{\le2}\) be an arbitrary target
polynomial of degree at most two.  On every polynomial graph,
\[
J_{x,y}\bigl(U+R_{\le2},Q\bigr)\notin\mathbb C^\times
\]
for every nonconstant \(Q(A,B,C)\) of target degree at most eleven.

The proof is finite-dimensional but not a blind coefficient search.
The primitive cusp collision lattice is
\[
\mathbb Z(5,-6,4).
\]
Through degree eleven there are exactly ten collision pairs
\[
B^6M\sim A^5C^4M,\qquad \deg M\le2.
\]
An exact triangular basis replaces their upper sides by
\[
T,\ AT,\ W,\ U,\ A^2T,\ AW,\ AU,\ BW,\ BU,\ CU.
\]
The scalar \(U\)-coefficient is then removed modulo the actual first
coordinate \(U+R_{\le2}\).

At regular graph boundaries, all augmented labels separate for graph
degree \(L\ge2\).  At \(L=1\), four exact two-dimensional groups remain.
Their Wronskian maps are injective, and a separate audit shows that every
next lower label is two degrees away, so no lower atom can cancel the
surviving coefficient.

At a pole boundary, six two-dimensional groups remain.  Four are
nonresonant.  The two exceptional characteristic families are, up to a
nonzero scalar in the leading pole sector,
\[
\begin{aligned}
BW:\quad&
\rho=5-16k,\quad
f=c\,u^{30k-10}(u^2-1)^{17k-5},\\
AU:\quad&
\rho=11-14k,\quad
f=c\,u^{22k-18}(u^2-1)^{17k-13},
\end{aligned}
\qquad k\ge2.
\]
Congruence checks modulo \(16\) and \(14\) prove that these
parametrizations exhaust the integral resonances.

The first lower total-\(\gamma\) layer couples \(BW\) only to \(AT\),
and \(AU\) only to the two-dimensional \(W/A^2B^3\) group.  A
same-\(E\) and intervening-face audit rules out every other target
interference.  Writing \(z=u-1\), the arbitrary zero sector is
\[
f_0(u)=1-\frac{57}{34}z+z^2h(u).
\]
The decisive local Laurent-jet determinants are
\[
\Delta_{BW/AT}\doteq(17k-5)(105k-32),\qquad
\Delta_{AU/W}\doteq(17k-13)^2.
\]
The first is independent of \(h(1)\); the second is independent of
\(h(1)\) and \(h'(1)\).  Higher jets cannot enter the selected
coefficients.  Both determinants are nonzero for every \(k\ge2\).

The exact artifacts are:

- `current_context/WEIGHTED_LIFT_NONHOMOGENEOUS_DEGREE_ELEVEN_NEWTON_BASIS_CLOSURE.md`
- `current_context/verify_weighted_lift_nonhomogeneous_degree_eleven_newton_basis_closure.py`
- `papers/weighted-lift-newton-obstructions/main.tex`
- `papers/weighted-lift-newton-obstructions/main.pdf`

### Review history

The first hostile review rejected the draft for two logically necessary
filtration checks:

- injectivity at \(L=1\) did not by itself exclude lower-label
  interference;
- the resonant pole face had not been proved unique at fixed
  \(E=\beta+\rho q\).

Both claims were true, were added as exact assertions, and were then
re-reviewed.  A second referee required the arbitrary nonzero leading
scalar and a proof that the integer resonance parametrizations were
exhaustive.  Those corrections were also added.  Three independent
referees then returned `ACCEPT`.

This history matters: the theorem was not promoted merely because a
symbolic script printed the desired conclusion.

## 2. Fixed-plane projective critical scalar rays

For the fixed lift \(U_0\), the affine critical scheme has length \(14\).
The two simplest boundary-preserving perturbation rays can now be
analyzed over the full projective parameter line.

For
\[
U_\lambda=U_0+\lambda E^2,
\]
the affine critical length is \(21\) for nonzero generic \(\lambda\),
and it is \(20\) at
\[
\lambda=\frac{-71\pm17\sqrt{17}}{2592}.
\]
At each exceptional value one point escapes to the distinguished
projective point \(P_c\).

For
\[
U_\lambda=U_0+\lambda tE^2,
\]
the affine length is generically \(21\).  It is \(19\) at
\(\lambda=9/8\), with two points escaping to \(P_t\), and \(20\) at
\(\lambda=-1/972\), with one point escaping to \(P_t\).  At
\(\lambda=-1/24\) the length remains \(21\); the apparent degree drop
is replaced by two explicit finite simple points on \(c=0\).

Consequently neither scalar ray contains a polynomial submersion.  The
calculation also shows that the leading homogeneous form determines the
support at infinity but not its intersection multiplicity; lower
projective jets are essential.

Artifacts:

- `current_context/FIXED_PLANE_PROJECTIVE_CRITICAL_SCALAR_RAYS.md`
- `current_context/verify_fixed_plane_projective_critical_scalar_rays.py`

## 3. Route A degree-four adjunction feasibility

The two numerical degree-four survivor profiles were tested against the
remaining canonical, Cartier, conductor, and log-deletion identities.
Both profiles admit exact curve and local finite-cover certificates.
The corrected calculation keeps the conductor adjunction divisor
separate from the deleted log divisor.

Thus those scalar identities do not exclude either survivor.  The local
models are feasibility witnesses only: they do not assemble a global
Keller cover.  The useful conclusion is negative but sharp—more
adjunction bookkeeping of the same kind is unlikely to close degree
four.

Artifacts:

- `current_context/ROUTE_A_DEGREE_FOUR_LOG_ADJUNCTION_FEASIBILITY.md`
- `current_context/verify_route_a_degree_four_log_adjunction_feasibility.py`

## 4. Novelty and publication assessment

The degree-eleven weighted-lift theorem is the strongest positive result
in this checkpoint.  It appears suitable for a scoped computer-assisted
research note because it has:

- a precise theorem with explicit limitations;
- a finite exact basis theorem rather than an empirical search bound;
- a new resonance mechanism resolved uniformly in the infinite
  parameter \(k\);
- executable rational-arithmetic certificates;
- an explicit adversarial review and repair trail.

No claim of priority is made.  A targeted search performed for the
earlier manuscript found no matching polynomial-graph Newton-vertex
theorem, but a broader MathSciNet/zbMATH review and human line-by-line
refereeing remain necessary before submission.

The fixed-plane scalar-ray classification is also new exact information,
but it is better published as part of a larger critical-incidence paper
unless its projective intersection mechanism is generalized beyond the
two rays.

The Route A feasibility theorem is valuable mainly because it prevents
time being spent on a now-demonstrably insufficient obstruction.

## 5. Strategic pivot

Extending the weighted-lift computation directly to degree twelve would
be useful but is not now the best primary route to the requested
resolution.  Degree eleven already shows the characteristic pattern:
new collision groups can be organized by the rank-one cusp lattice, and
rare resonances are controlled by a finite local-jet map.  The right next
question there is a general induction or finite-state collision theorem,
not another isolated degree run.

The primary resolution-directed route should instead move to the
Guccione--Guccione--Valqui finite standard system, because that system is
equivalent to the existence of a plane Keller counterexample rather than
being a special three-dimensional descent family.

The existing reduction is already sharp:

1. Every counterexample produces a reciprocal polynomial arc based at a
   nonzero point of the common-root cone
   \[
   P_0=R^a,\qquad Q_0=R^b,\qquad n=ga,\quad m=gb.
   \]
2. The equation-Jacobian is exactly, up to sign,
   \[
   \operatorname{Res}_x(P_x,Q_x),
   \]
   and a Keller arc would have maximal possible contact
   \((n-1)(m-1)\).
3. A common approximate-root change removes one \(g\)-sector unit but
   not the relative unit
   \[
   \mathcal I=\frac{Q^{a}}{P^{b}}.
   \]
   Its first nonzero \(g\)-multiple jet is physical quotient data.
   The larger triangular \(\lambda_{gq}\)-cancellation in the standard
   presentation is not, by itself, a coordinate gauge on a fixed pair.
4. The final inhomogeneous forcing lies in residue class
   \(-2\bmod g\).
5. On each normalization branch of \(P=0\), the Keller identity forces
   the exact residue condition
   \[
   [t^{em}]
   \left(\frac{\tau^{m+n-2}}{P_x}\Big|_\gamma\right)=0.
   \]

The first normal-form step must therefore retain the relative
\(g\)-sector invariant rather than quotient it away.  In approximate-root
coordinates
\[
P=R^aA(z),\qquad Q=R^bB(z),\qquad z=\tau^g/R,
\]
an honest change \(R\mapsto R\phi(z)\) has the complete relative
invariant \(B^a/A^b\), up to tangent-to-the-identity composition.  One
may normalize \(A=1\) or \(B=1\), but not both.

The relative logarithm
\[
\ell=\log\left(\frac{Q^a}{P^b}\right)
\]
is especially useful because the homogenized Keller identity becomes a
linear first-order equation in \(\ell\).  The \(g\)-multiple relative
jets then remain visible but their residue classes decouple.  The actual
mixing problem is the non-\(g\)-multiple \(Z=0\) nilpotent cascade in
the common \(P,Q\) direction.

Two audits now change that proposed route materially.

First, the Laurent obstruction and the derivative-resultant filtration
must be separated.  For the explicit first normal deformation
\[
P_\epsilon=R^a+\epsilon T
\]
and its polynomial binomial truncation \(Q_q\), where
\[
q=\left\lfloor\frac ba\right\rfloor,\qquad r=b-aq,
\]
there is an exact division-free identity
\[
(Q_q)_X-H_\epsilon(P_\epsilon)_X
=r\binom{b/a}{q}\epsilon^qR^{r-1}R'T^q.
\]
On a natural Zariski-open set this gives
\[
\operatorname {ord}_\epsilon
\operatorname {Res}_X((P_\epsilon)_X,(Q_q)_X)
=gb-q-1.
\]
The earlier claim \((n-1)(q+1)\), inferred from the first Laurent pole,
was false.  The correction gives the first exact obstruction map of the
nonreduced normal cone and shows that generic nilpotent directions lose
determinant contact much earlier than the Laurent calculation suggested.

Second, the affine endpoint contribution can be nonzero while every
individual normalization-branch coefficient
\([t^{em}](\tau^N/P_X)\) vanishes.  More decisively, the
endpoint-invisible affine pairings span the whole one-dimensional
forcing line.  Quotienting all of them therefore kills the Keller
forcing itself.  Restricting the quotient to lower-order cycles does
not help: no nonzero pure affine tail is such a cycle, because it has a
nonzero earlier cross term with \(R^a,R^b\).  Whether an endpoint term
is removable depends on a full lift through the nilpotent cascade.

This rules out the endpoint-only pole-filtered monodromy lemma as the
next standalone obstruction.  The resolution-directed target is now:

> **Lifted endpoint lemma.**  Classify the order-\(N\) obstruction
> values of all lower \(Z=0\) nilpotent lifts with fixed reduced
> common-root data, and prove either that the Keller scalar is absent
> or construct a compatible lift realizing it.

The next work should be deformation-theoretic, not a larger coefficient
sweep:

1. use the division-free Sylvester identity to describe the first
   obstruction ideal and its root/critical-point factors;
2. organize successive \(Z=0\) lifts by the Rees or normal-cone
   filtration, keeping the relative unit \(Q^a/P^b\);
3. compute how a lift changes the endpoint obstruction, rather than
   quotienting the raw affine determinant;
4. test whether the resulting obstruction map has a conserved
   rootwise valuation or trace class;
5. if it does, prove that the scalar Keller forcing misses its image;
   if it does not, use the first exact compatible formal lift as a
   counterexample-construction lead;
6. bring global monodromy back only after this liftability problem has
   been solved.

Small \((g,a,b)\) computations should be used only to discover and test
the normal form and to search for countermodels.  They should not be
mistaken for a proof by bounded enumeration.

## 6. Bottom line

The project has produced another publishable theorem and several exact
route audits, but not the requested proof or counterexample.  The
pole-filtered endpoint idea has now been narrowed enough to expose its
missing premise: liftability through the nonreduced normal cone.  The
current primary direction is the lifted-endpoint obstruction map in the
finite standard system, with Route A boundary-regular Darboux
classification as an independent counterexample-first track.
