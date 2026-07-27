# The fixed-plane Keller jet lifts through every normal order

Date: 25 July 2026

## Outcome

The first-order Hermite--CRT pair in
`FIXED_PLANE_SHEET_LOSS_AND_FIRST_ORDER_CRT.md` has no second-order
Keller obstruction.  In fact, it has no obstruction on any finite
infinitesimal neighborhood of the disjoint divisor
\[
 E=DK=0.
\]

The reason is structural rather than computational.  The Hamiltonian
derivation
\[
 \partial_U=\{U,-\}
\]
is transverse to \(E=0\): the class of
\[
 \delta=\{U,E\}
\]
is a unit in \(\mathbf Q[t,c]/(E)\).  Once this holds, a one-line
Hensel recurrence corrects the Jacobian one normal order at a time.
Applied to the explicit fixed-plane model, it gives an exact polynomial
second-order lift and compatible polynomial lifts to every finite
order.

Consequently, no contradiction can arise from a finite-order formal
Keller calculation along \(C\sqcup H\).  Any obstruction on this route
must involve polynomial termination/algebraization, the global
nonproper-value geometry, global monodromy, or the boundary finality
tree.

For the particular first coordinate \(U_0\), the algebraization
question has an exact negative answer: \(U_0\) has fourteen critical
points, all away from \(E=0\).  Therefore no polynomial \(V\) can
satisfy \(\{U_0,V\}=1\) globally.  The formal lift succeeds precisely
because the \(E\)-adic neighborhood does not see those points.

This is not a polynomial Keller pair.  The all-order object is an
\(E\)-adic formal function, and no stabilization of the correction
sequence is proved.

## 1. The transverse Hensel lemma

Let \(k\) be a field of characteristic zero, let
\[
 R=k[t,c],\qquad \{A,B\}=A_tB_c-A_cB_t,
\]
and fix \(U,E\in R\).  Suppose that
\[
 \delta=\{U,E\}
\]
is invertible modulo \(E\).  Thus there is an \(a\in R\) such that
\[
 a\delta\equiv1\pmod E.
\tag{1}
\]

Suppose that, for some \(m\ge1\),
\[
 \{U,V_m\}=1+E^m q_m
\tag{2}
\]
with \(V_m,q_m\in R\).  Define
\[
 \boxed{\qquad
 V_{m+1}
 =
 V_m-\frac{E^{m+1}}{m+1}a q_m.
 \qquad}
\tag{3}
\]
The Leibniz rule gives
\[
 \begin{aligned}
 \{U,V_{m+1}\}-1
 &=
 E^m q_m
 -E^m a q_m\delta
 -\frac{E^{m+1}}{m+1}\{U,aq_m\}\\
 &=
 E^m q_m(1-a\delta)
 -\frac{E^{m+1}}{m+1}\{U,aq_m\}.
 \end{aligned}
\tag{4}
\]
By (1), the right side is divisible by \(E^{m+1}\).  Therefore
\[
 \boxed{\qquad
 \{U,V_{m+1}\}\equiv1\pmod {E^{m+1}}.
 \qquad}
\tag{5}
\]

Starting with any solution modulo \(E\), (3) constructs a polynomial
solution modulo \(E^N\) for every finite \(N\).  Moreover,
\[
 V_{m+1}\equiv V_m\pmod {E^{m+1}},
\tag{6}
\]
so the sequence has a compatible limit
\[
 \widehat V\in\widehat R^{(E)}
 =\varprojlim_N R/(E^N)
\]
satisfying
\[
 \{U,\widehat V\}=1
\]
in the \(E\)-adic completion.

No smoothness or squarefreeness hypothesis on \(E\) is needed for the
lemma itself.  In the application below, \(E=DK\) is reduced and its
two components are smooth and disjoint, which makes the unit condition
transparent.

## 2. Exact transversality in the fixed plane

Use the notation of the first-order construction:
\[
 v=3ct-2,\qquad
 D=v^2-9c,\qquad K=v+D,\qquad E=DK,
\]
and take \(U=U_0\).  Along the conductor \(C=(D=0)\) and residual curve
\(H=(K=0)\), the earlier exact calculations give
\[
 K|_C=v,\qquad D|_H=-v,
\]
\[
 \{U,D\}|_C=-\frac4{27}v^5,\qquad
 \{U,K\}|_H=-6v^2(v+1).
\]
It follows that
\[
 \boxed{
 \delta|_C=-\frac4{27}v^6,\qquad
 \delta|_H=6v^3(v+1).
 }
\tag{7}
\]
The functions \(v\) on \(C\), and \(v,v+1\) on \(H\), are units.
Hence \(\delta\) is a unit modulo both \(D\) and \(K\), and therefore
modulo \(E=DK\).

There is a compact polynomial representative of its inverse.  Recall
\[
 \iota_C=\frac{tv-3}{6},\qquad
 \iota_H=\frac{t(v+1)-3}{6},
\]
which represent \(v^{-1}\) on \(C\) and \(H\), respectively, and put
\[
 \eta_H=\frac{tv-3}{3}.
\]
The identity
\[
 (v+1)\eta_H-1=\frac t3K
\]
shows that \(\eta_H\) represents \((v+1)^{-1}\) on \(H\).  With the
CRT idempotents
\[
 e_C=K\iota_C,\qquad e_H=-D\iota_H,\qquad e_C+e_H=1,
\]
set
\[
 \boxed{\qquad
 a=
 -\frac{27}{4}e_C\iota_C^6
 +\frac16e_H\iota_H^3\eta_H.
 \qquad}
\tag{8}
\]
Equations (7)--(8) give
\[
 a\delta\equiv1\pmod D,\qquad
 a\delta\equiv1\pmod K,
\]
and comaximality of \(D,K\) proves (1).

This identifies the deformation-theoretic compatibility group
directly: the normal linearization at every stage is multiplication by
\((m+1)\delta\) on \(R/(E)\), hence is an automorphism.  Its cokernel,
which would contain the next-order obstruction, is zero.

## 3. The exact second-order polynomial

Let
\[
 V_1=V_0+E\beta
\]
be the polynomial constructed by first-order Hermite CRT.  It satisfies
\[
 \{U,V_1\}\equiv1\pmod E.
\]
Define the exact polynomial
\[
 q_1=\frac{\{U,V_1\}-1}{E}\in R.
\tag{9}
\]
The second-order correction furnished by (3) is
\[
 \boxed{\qquad
 V_2=V_1-\frac12E^2a q_1.
 \qquad}
\tag{10}
\]
Substitution in (4) gives the explicit certificate
\[
 \{U,V_2\}-1
 =
 E q_1(1-a\delta)
 -\frac{E^2}{2}\{U,aq_1\},
\tag{11}
\]
which is divisible by \(E^2\).  Thus
\[
 \boxed{\qquad
 \{U,V_2\}\equiv1\pmod {D^2K^2}.
 \qquad}
\tag{12}
\]

The exact verifier constructs these polynomials over \(\mathbf Q\).
For scale, it finds
\[
 \begin{array}{c|c|c}
 \text{polynomial}&\text{total degree}&\text{number of terms}\\ \hline
 q_1&55&266\\
 a&25&53\\
 -aq_1/2&80&521\\
 V_2&96&749
 \end{array}
\]
and verifies direct divisibility of
\(\{U,V_2\}-1\) by \(D^2K^2\).  The displayed formulas, rather than a
search over those coefficients, construct the solution.

Because \(V_2-V_1\in(E^2)\), the second-order correction preserves:

1. the target restrictions on \(C\) and \(H\);
2. the first normal target jet along \(E=0\);
3. the quotient \(F(U,V)/E\) modulo \(E\); and therefore
4. \(L|_C=1/18\), \(L|_H=-1/(v+1)\), and the odd conductor
   coefficient \(v/18\).

## 4. The fixed first coordinate cannot algebraize

The formal recurrence raises the natural question whether it can
terminate at a polynomial \(V\).  For the displayed \(U=U_0\), a much
simpler global obstruction answers no.

An exact lexicographic Groebner basis of
\[
 (U_t,U_c)\subset\mathbf Q[t,c]
\]
has leading monomials \(t\) and \(c^{14}\).  Its \(c\)-eliminant,
cleared of denominators, is
\[
\begin{aligned}
 P(c)={}&129600c^{14}-16086645c^{13}+762804802c^{12}
 -17935387965c^{11}\\
 &+234413004346c^{10}-1767283629696c^9
 +7546547140810c^8\\
 &-17058892809204c^7+19276910317992c^6
 -11149073947836c^5\\
 &+2118379838400c^4-155004753276c^3
 +3161279664c^2\\
 &+95831424c-3359232.
\end{aligned}
\tag{13}
\]
The verifier checks
\[
 \gcd(P,P')=1.
\tag{14}
\]
Thus \(U\) has fourteen distinct critical points over \(\mathbf C\);
the first Groebner-basis row determines one \(t\)-coordinate for each
root of \(P\).  It also checks
\[
 (U_t,U_c,E)=(1),
\tag{15}
\]
so every critical point lies outside \(C\sqcup H\), as already
predicted by the transversality of \(\{U,E\}\) there.

At any critical point \(p\), for every polynomial \(V\),
\[
 \{U,V\}(p)=U_t(p)V_c(p)-U_c(p)V_t(p)=0.
\]
Consequently,
\[
 \boxed{\qquad
 \text{there is no }V\in\mathbf C[t,c]\text{ with }\{U_0,V\}=1.
 \qquad}
\tag{16}
\]

There is no conflict between (16) and the all-order lift.  Since
\(E(p)\ne0\) at every critical point, those points are absent from the
formal completion along \(E=0\).

This closes the algebraization question only for the chosen polynomial
lift \(U_0\).  A perturbation of \(U\) by a multiple of \(E\), or by
\(E^2\) if the first normal target jet is to be retained, is a different
global first coordinate and is not excluded by (13)--(16).

## 5. What this closes and what it does not

The proposed next test was a second-order obstruction to the
first-order Hermite--CRT jet.  Equations (7)--(12) close that test in
the constructive direction, and the Hensel lemma closes every finite
normal order at once.

This does not solve the Jacobian conjecture and does not produce a
counterexample.  The distinction is essential:

- each \(V_N\) is a polynomial, but the recurrence need not preserve
  any fixed degree or support bound;
- the limit \(\widehat V\) is proved only in the \(E\)-adic completion;
- no finite-stage correction is shown to stabilize;
- no global equation \(\{U,V_N\}=1\) is obtained; and
- generic degree, nonproper values, monodromy, and boundary finality
  are not supplied by the formal construction.

The route should therefore stop searching for an obstruction in a
fixed finite thickening of \(C\sqcup H\).  For \(U_0\), the fourteen
critical points already prove nonalgebraization.  The sharper remaining
question is whether a polynomial perturbation
\[
 U'=U_0+E^2\phi
\]
can simultaneously remove every critical point and support a
terminating Keller correction while retaining the established
conductor, residual-sheet, and first-normal target data.  This is a
global critical-locus/algebraization problem, not another normal-jet
compatibility calculation.

The exact instance and the general recurrence identity are checked by
`verify_fixed_plane_all_order_hermite_crt_lift.py`.
