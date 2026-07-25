# Exact interface from the case-c support to the seven-mode charts

Date: 25 July 2026

## Purpose

The direct characteristic-zero chart calculations use seven weighted
parameters rather than the original case-c coefficient array.  This note
records why that change of presentation neither loses a component nor
retains the affine cone origin as a genuine case-c point.

The argument has four independent pieces:

1. the Laurent monomial change is an exact rewriting of the published
   support;
2. the outer quintic exhausts the normalized Hurwitz covers;
3. the descending linear recurrence parametrizes every lower solution
   through the first contradictory row; and
4. the two required opposite vertices exclude the zero parameter vector.

This is an interface statement.  The unit-ideal and scalar chart
certificates themselves are documented separately.

## 1. Exact support dictionary

Put

\[
z=xy,\qquad h=xy^2.
\]

Then

\[
x=\frac{z^2}{h},\qquad y=\frac hz,\qquad
[z,h]_{x,y}=h.
\]

A radial Laurent monomial has the exact source expression

\[
z^i h^j=x^{i+j}y^{i+2j}.
\]

The support inventory in `route_bd_case_c_radial_obstruction.py` checks
that both exponents on the right are nonnegative for every listed term.
It contains:

- the complete outer blocks \(A_2=U/h\) and \(B_3=V/h\);
- all 165 nonouter, nonconstant coefficients of the case-c support; and
- no duplicate monomial.

Thus the radial equations are the coefficient equations of the original
polynomial bracket, not equations for a subfamily.

## 2. The outer normalization is exhaustive

The outer pair obeys

\[
UV+2hUV'-3hU'V=1,\qquad
\deg U=7,\quad\deg V=10,\quad U(0)=V(0)=1.
\]

Here the second degree is forced by the first one, rather than imported
from the modular calculation.  If \(u_7\ne0\) and
\(\deg V=m\leq10\), the coefficient of \(h^{m+7}\) in the outer equation
is

\[
(1+2m-21)u_7v_m=(2m-20)u_7v_m.
\]

It can vanish in characteristic zero only for \(m=10\).  Thus every
point on the required \(u_7\ne0\) locus has the passport below.

Its rational function

\[
R=h\frac{V^2}{U^3}
\]

has passport

\[
(2^{10},1),\qquad(3^7),\qquad(17,1^4).
\]

The exact Hurwitz count is five.  The reconstructed irreducible quintic
outer algebra

\[
K=\mathbf Q[s]/(f(s))
\]

contains five distinct normalized solutions, all satisfying the outer
equation and all required outer nonvanishing conditions.  Hence it
exhausts the five geometric Hurwitz classes, for the following precise
reason.  An isomorphism between two such covers must fix the unique simple
point over the first branch value and the unique ramification-seventeen
point over the third one.  In the chosen source coordinate it is therefore
\(h\mapsto\lambda h\).  The outer scaling acts by

\[
u_i\longmapsto\lambda^iu_i,\qquad
v_j\longmapsto\lambda^jv_j.
\]

Consequently an orbit with \(u_1\ne0\) meets \(u_1=1\) exactly once.
The five distinct roots of the squarefree quintic therefore represent
five distinct Hurwitz orbits, not five representatives with repetitions.
Since the characteristic-zero Hurwitz number is five and the covers have
trivial automorphism groups, no further orbit with \(u_1=0\) can exist.
This is the characteristic-zero exclusion of the \(u_1=0\) locus; the
modular saturated unit ideal for that locus is only an independent
good-reduction check.

The case-c slice is usually normalized by \(u_7=1\), whereas the exact
quintic uses \(u_1=1\).  The scaling

\[
(P,Q)(z,h)\longmapsto
\bigl(\lambda P(z,\lambda h),\lambda Q(z,\lambda h)\bigr)
\]

preserves the bracket and acts invertibly on every lower weighted
coefficient.  On a \(u_1=1\) representative, putting \(u_7=1\) is the
equation

\[
\lambda^7=u_7^{-1}=s.
\]

The exact outer certificate proves \(u_7\ne0\), so this equation has seven
distinct roots over the algebraic closure.  The action is free there
because \(u_1\ne0\): a stabilizing scalar satisfies
\(\lambda u_1=u_1\), hence \(\lambda=1\).  Each of the five Hurwitz
orbits therefore contributes exactly seven distinct \(u_7=1\)
representatives.  Conversely, the preceding \(u_1=0\) exclusion shows
that every \(u_7=1\) point belongs to one of these orbits.  Thus the
case-c slice has exactly \(5\cdot7=35\) geometric points, all checked by
the exact \(K\)-calculation after invertible scaling.

The characteristic-zero ingredients in this paragraph are separated in
the verifiers.  `route_bd_ab_hurwitz_count.py` computes the exact
character sum and records transitivity and trivial automorphisms.
`route_bd_ab_outer_lift.py` reconstructs the squarefree irreducible
quintic, proves \(s u_7=1\), and verifies every coefficient of the outer
ODE in \(K[h]\).  The exact special-chart script independently rechecks
the two outer vertex units before starting its lower recurrence.  No
emptiness or orbit-exhaustion assertion here is deduced from the modular
\(u_1=0\) calculation.

## 3. The seven modes parametrize every lower solution

Assign radial-deficit weights

\[
\operatorname{wt}(A_i)=2-i,\qquad
\operatorname{wt}(B_j)=3-j.
\]

The bracket row of radial degree \(k\) is weighted homogeneous of weight
\(4-k\).  Descending from the outer row, each new block is an affine
linear system whose source consists only of already determined lower
blocks.

Over the exact outer field \(K\), the bounded kernels in deficits one
and higher have multiplicities

\[
(2,2,2,1,0,0,\ldots).
\]

Equivalently, every solution is represented by seven parameters of
weights

\[
(1,1,2,2,3,3,4).
\]

The identity and endpoint count proving
\((2,2,2,1,0,\ldots)\) in characteristic zero are checked in
`route_bd_universal_radial_kernel_theorem.py`.  The exact \(K\)-recurrences
in `scratch_case_c_n3_generic_charts_Q.py` and
`scratch_case_c_n3_special_charts_Q.py` use those seven canonical modes
and solve the subsequent affine linear systems directly over \(K\).

The direct exact recurrences reproduce these kernels and retain every
cokernel row through:

- deficit seven on the two generic charts; and
- deficit eight on the two special charts.

No later coefficient can repair a failed earlier cokernel row.  Hence a
zero of the original 165-coordinate system would determine a zero of
one of the four exact seven-mode chart systems.  The chart cover

\[
L\ne0,\quad
L=0,\ A\ne0,\quad
L=A=0,\ B\ne0,\quad
L=A=B=0
\]

is set-theoretically exhaustive.

The exact-to-modular coefficient comparisons in the chart verifiers
lock the primitive element, mode order, endpoint change, imposed-row
order, and row scalars.  They both identify the good integral model used
by the complete-projective-fiber specialization proof and audit that the
exact recurrence is the same recurrence as the independently generated
full-support calculation.  The direct homogeneous characteristic-zero
chart certificates provide a separate route.

## 4. The cone origin is not a case-c point

The original case-c support requires the opposite vertical vertices

\[
[z^{-8}h^8]P\ne0,\qquad [z^{-12}h^{12}]Q\ne0.
\]

Indeed, under
\[
x^ay^b=z^{2a-b}h^{b-a},
\]
the GGHV vertices \((0,8)\) and \((0,12)\) become \((-8,8)\) and
\((-12,12)\).  They occur in radial deficits ten and fifteen,
respectively—not in the early deficit-two and deficit-three blocks.

This correction does not create an origin loophole.  The exact linear
kernel dimensions at deficits one through fifteen are

\[
(2,2,2,1,0,0,\ldots,0).
\]

Thus after the seven parameters of weights

\[
(1,1,2,2,3,3,4),
\]

are set to zero, the first four lower blocks are zero.  Every later
inhomogeneous source is built from already determined lower blocks and is
therefore zero, while the corresponding linear operator has zero kernel.
Induction forces every later nonconstant lower coefficient to be zero.
In particular,

\[
[z^{-8}h^8]P=[z^{-12}h^{12}]Q=0.
\]

endpoint-coordinate changes used by the chart verifiers fix the origin,
as does the square substitution, so their deepest-chart origin is the
same origin in the canonical seven parameters.  The two omitted additive
constants are bracket-invisible and cannot contribute to either displayed
vertex.

The support locations, all fifteen kernel ranks, and the omission of only
the two additive constants are independently checked in
`current_context/verify_case_c_full_certificate_bridge.py`.  The full
165-coordinate recurrence in `route_bd_case_c_radial_obstruction.py`
provides a second check and uses no characteristic-zero inference for the
support dictionary.

Therefore every genuine case-c solution supplies a nonzero point of

\[
\mathbf P(1,1,2,2,3,3,4).
\]

The affine cone origin left by the deepest exact chart is excluded by the
required original vertices: zero-kernel propagation through the later
radial blocks forces those two vertex coefficients to vanish.

## Conclusion

Together, the exact Hurwitz count and outer lift, the characteristic-zero
kernel theorem, and the exact chart certificates show that the four
seven-mode charts exhaust the original case-c support over characteristic
zero and that their common affine origin is forbidden.
There is no remaining 165-coordinate/projective-origin loophole.

Relevant verifiers:

```text
route_bd_case_c_radial_obstruction.py
route_bd_ab_hurwitz_count.py
route_bd_ab_outer_lift.py
route_bd_universal_radial_kernel_theorem.py
scratch_case_c_n3_generic_charts_Q.py
scratch_case_c_n3_special_charts_Q.py
```
