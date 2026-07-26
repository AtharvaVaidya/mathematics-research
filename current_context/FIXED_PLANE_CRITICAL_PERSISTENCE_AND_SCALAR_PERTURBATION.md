# The fourteen fixed-plane critical points persist under every formal jet-preserving perturbation

Date: 25 July 2026

## Outcome

Let \(U_0,D,K\) be the exact fixed-plane polynomials constructed in
`FIXED_PLANE_SHEET_LOSS_AND_FIRST_ORDER_CRT.md`, and put
\[
 E=DK.
\]
The natural way to retain both the values and the first normal target
jet on \(C\sqcup H=(E=0)\) is
\[
 U_{\epsilon}=U_0+\epsilon E^2\phi,
 \qquad \phi\in\mathbf C[t,c].
\tag{1}
\]
This note proves that (1) cannot remove the global critical-point
obstruction perturbatively.  Every one of the fourteen critical points
of \(U_0\) has a unique formal critical-point continuation for every
choice of \(\phi\).  Equivalently, the old critical scheme is an
étale, not an obstructed, part of the universal critical incidence
scheme.

Consequently:

1. every sufficiently small complex perturbation (1) still has at
   least fourteen distinct critical points;
2. for each \(d\), in the full affine coefficient space of all
   \(\phi\) of degree at most \(d\), a Zariski-open neighborhood of
   \(0\) still has at least fourteen critical points;
3. any critical-free perturbation, if one exists, is necessarily
   exceptional and nonperturbative; determining whether its critical
   branches escape to infinity requires a separate projective-incidence
   calculation; and
4. random coefficient search is aimed at the wrong locus.

The simplest large deformation does not help.  For
\[
 \boxed{\qquad U_1=U_0+E^2,\qquad}
\tag{2}
\]
the exact critical scheme is reduced of length \(21\), is disjoint
from \(E=0\), and therefore again rules out every polynomial
\(V\) with \(\{U_1,V\}=1\).

This is a rigorous obstruction to the *perturbative* critical-removal
strategy, not a proof that the whole coset \(U_0+(E^2)\) contains no
polynomial submersion.

## 1. The old critical scheme is finite étale

Write
\[
 I_0=((U_0)_t,(U_0)_c)\subset\mathbf Q[t,c].
\]
The exact lexicographic Gröbner basis computed previously has the
triangular shape
\[
 t-R(c),\qquad P(c),
\tag{3}
\]
where \(\deg P=14\) and
\[
 \gcd(P,P')=1.
\tag{4}
\]
Thus
\[
 A=\mathbf Q[t,c]/I_0
\]
is a finite étale \(\mathbf Q\)-algebra of dimension \(14\).  Over
\(\mathbf C\), the critical scheme consists of fourteen distinct
points.

There is a useful equivalent differential statement.  The Jacobian
matrix of the two generators of \(I_0\) is the Hessian
\[
 {\rm Hess}(U_0)=
 \begin{pmatrix}
  (U_0)_{tt}&(U_0)_{tc}\\
  (U_0)_{ct}&(U_0)_{cc}
 \end{pmatrix}.
\tag{5}
\]
Since the zero-dimensional complete intersection (3) is reduced, its
Jacobian determinant
\[
 h=\det {\rm Hess}(U_0)
\tag{6}
\]
is a unit in \(A\).  Hence every old critical point is Morse and the
critical equations have an invertible linearization there.

The old calculation also gives
\[
 ((U_0)_t,(U_0)_c,E)=(1),
\tag{7}
\]
so all fourteen points lie away from the retained boundary.

## 2. Formal persistence theorem

The phenomenon is general.

**Proposition.**  Let \(k\) have characteristic zero, let
\(f,g\in k[x,y]\), and suppose that
\[
 Z=(f_x,f_y)
\]
is finite étale over \(k\).  For
\[
 f_\epsilon=f+\epsilon g
\]
the critical scheme of \(f_\epsilon\), completed along
\(\epsilon=0\) and \(Z\), is canonically finite étale of the same
degree over \(k[[\epsilon]]\).  In particular, every geometric point
of \(Z\) has a unique formal critical-point continuation.

**Proof.**  In the coordinate algebra of \(Z\), the determinant of
\({\rm Hess}(f)\) is a unit by the Jacobian criterion.  The two
equations
\[
 (f_\epsilon)_x=(f_\epsilon)_y=0
\]
therefore have invertible Jacobian with respect to \(x,y\) at
\(\epsilon=0\).  Formal étaleness, equivalently the two-variable
Hensel lemma, gives the unique lift over every
\(k[\epsilon]/(\epsilon^N)\), compatibly in \(N\).  Their inverse limit
is finite étale of the same degree over \(k[[\epsilon]]\). \(\square\)

At a critical point \(p\), the first displacement is already explicit:
\[
 \binom{\dot t}{\dot c}
 =
 -{\rm Hess}(U_0)(p)^{-1}
 \binom{(E^2\phi)_t(p)}{(E^2\phi)_c(p)}.
\tag{8}
\]
Thus changing \(\phi\) changes the velocity of a critical point; it
does not delete the point.

Apply the proposition with \(f=U_0\) and \(g=E^2\phi\).  Equations
(3)--(6) prove that all fourteen critical points lift uniquely.
The complex analytic implicit-function theorem then gives fourteen
distinct nearby critical points for all sufficiently small
\epsilon\).

There is also a coefficient-space version.  Fix \(d\), write
\[
 \phi_{\mathbf a}
 =\sum_{i+j\le d}a_{ij}t^ic^j,
\tag{9}
\]
and consider the universal critical incidence scheme over the affine
space of the \(a_{ij}\).  It is étale at the finite degree-\(14\)
fiber over \(\mathbf a=0\).  By the quasi-finite form of Zariski's
Main Theorem, followed by shrinking the irreducible coefficient space
around \(0\), this part becomes finite étale of degree \(14\).  Hence,
for every \(d\), a nonempty Zariski-open neighborhood of \(0\) in the
full degree-\(\le d\) coefficient space---and therefore a dense open
subset of that full space---has at least fourteen critical points.
This statement is not asserted for an arbitrary subfamily, which need
not meet the open set.  A critical-free choice can only lie outside
this open set and outside the sufficiently small analytic neighborhood
given above.

## 3. The boundary remains innocent

The perturbation does not create a critical point on \(E=0\).  Indeed,
\[
 d(U_0+\epsilon E^2\phi)-dU_0
 =\epsilon(2E\phi\,dE+E^2d\phi),
\tag{10}
\]
so the value and the full first differential agree with those of
\(U_0\) along \(E=0\).  Moreover,
\[
 \{U_0+\epsilon E^2\phi,E\}
 =
 \{U_0,E\}+\epsilon E^2\{\phi,E\}.
\tag{11}
\]
The first term is a unit modulo \(E\), by the transverse Hensel
calculation.  Therefore (11) is a unit modulo \(E\), for every
\(\epsilon,\phi\).

If \(dU_\epsilon\) vanished at a point of \(E=0\), then
\(\{U_\epsilon,E\}\) would vanish there, contradicting (11).
Critical points can only move in the open surface \(E\ne0\), or escape
through its compactification.

## 4. Exact audit of the scalar direction

Take the smallest nontrivial choice \(\phi=1,\epsilon=1\), namely (2).
It has total degree \(16\) and \(31\) terms.  An exact lexicographic
Gröbner basis of
\[
 I_1=((U_1)_t,(U_1)_c)
\]
again has two rows, now with leading monomials
\[
 t,\qquad c^{21}.
\tag{12}
\]
The second row is a degree-\(21\) eliminant and is coprime to its
derivative.  Hence
\[
 \boxed{\qquad
 \operatorname {Crit}(U_1)
 \text{ consists of exactly \(21\) distinct complex points.}
 \qquad}
\tag{13}
\]
The verifier also checks
\[
 ((U_1)_t,(U_1)_c,E)=(1).
\tag{14}
\]
Thus all \(21\) points remain off the retained divisor, exactly as
the structural argument predicts.

At any one of these points \(p\), every polynomial \(V\) satisfies
\[
 \{U_1,V\}(p)=0.
\]
Consequently
\[
 \boxed{\qquad
 \text{there is no \(V\in\mathbf C[t,c]\) with
 \(\{U_0+E^2,V\}=1\).}
 \qquad}
\tag{15}
\]

## 5. Strategic consequence

The all-order normal Hensel lift and the present critical-point Hensel
lift run in opposite directions:

- the Keller equation has no obstruction in the \(E\)-adic
  neighborhood; but
- the fourteen off-boundary critical points have no obstruction to
  persisting in the perturbation parameter near the original lift.

So another order-by-order correction, or a random low-degree choice of
\(\phi\), is not a plausible route to a global pair.  The next
well-posed calculation is the projective critical incidence problem:
compactify
\[
 (U_0+E^2\phi)_t=(U_0+E^2\phi)_c=0
\]
and determine whether there is an exceptional coefficient locus on
which all finite critical branches are absorbed at infinity.  Any
critical-free locus found by that analysis would then have to satisfy
the second, independent condition
\[
 1\in\{U,\mathbf C[t,c]\},
\]
that is, polynomial solvability of the Hamiltonian equation
\(\{U,V\}=1\).

The exact finite calculations supporting this note are in
`verify_fixed_plane_critical_persistence_and_scalar_perturbation.py`.
