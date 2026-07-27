# The case-c cap faces do not by themselves exhaust the Darboux divisor

Date: 25 July 2026

## Audited conclusion

For the exact GGHV case-c Newton polygons, even the following complete
boundary package does **not** force Galois invariance of
\[
J=\Xi^5T^{17}=\frac{Z^5}{W^2}:
\]

1. the genuine normalized outer Davenport--Zannier pair;
2. every required Newton vertex;
3. the forced vertical common root of multiplicities \((2,3)\);
4. the forced diagonal common root of multiplicities \((8,12)\); and
5. the normalized comparison sheet at the outer end.

There is an exact algebraic countermodel with all this data.  Choose the
coefficients away from the three prescribed faces algebraically
generically.  Its geometric degree is
\[
141-2-8=131,
\]
whereas the genuine endpoint map has degree \(21\).  A rational
comparison branch would factor the degree-\(131\) map through the
degree-\(21\) endpoint map, which is impossible.  Hence the divisor of
\(J\) is not Galois invariant.

The countermodel does not satisfy the Keller bracket equation.  It
cannot: the complete case-c bracket scheme is empty by
`CASE_C_FULL_CERTIFICATE_BRIDGE.md`.  Its precise consequence is instead
a no-go theorem:

> Newton polygons, cap vertices, their forced face factorizations, and
> principal-divisor intersection theory cannot by themselves prove
> support exhaustion for \(\operatorname{div}(\sigma J/J)\).

Any positive support-exhaustion argument must use deeper bracket rows,
equivalently the infinitely-near jets above the two cap basepoints.
Merely locating the basepoints and recording their face multiplicities
is insufficient.

## 1. The exact case-c polygons and outer pair

Work over an algebraically closed characteristic-zero field.  The two
polygons are
\[
\begin{aligned}
\Delta_P&=\operatorname{conv}
\{(0,0),(1,0),(8,14),(8,16),(0,8)\},\\
\Delta_Q&=\operatorname{conv}
\{(0,0),(2,1),(12,21),(12,24),(0,12)\}.
\end{aligned}
\tag{1}
\]
Put
\[
w=xy^2.
\]
Fix a genuine normalized endpoint
\[
P_0=xU(w),\qquad Q_0=x^2yV(w),
\tag{2}
\]
where
\[
\deg U=7,\qquad \deg V=10,\qquad
U(0)=V(0)=1,
\tag{3}
\]
the leading coefficients \(u_7,v_{10}\) are nonzero, and
\[
UV+2wUV'-3wU'V=1.
\tag{4}
\]
Equation (4) implies
\[
\gcd(U,V)=1.
\tag{5}
\]

The mixed volume of (1) is
\[
\operatorname{MV}(\Delta_P,\Delta_Q)=141.
\tag{6}
\]
This is the generic number of solutions in the source torus of two
generic translated equations with these polygons, counted with
multiplicity.

## 2. Prescribing both forced cap factorizations

Choose \(s,\lambda\in k^\times\).  Prescribe the vertical faces by
\[
\begin{aligned}
P_{\rm vert}
 &=u_7x^8y^{14}(1-y/s)^2,\\
Q_{\rm vert}
 &=v_{10}x^{12}y^{21}(1-y/s)^3.
\end{aligned}
\tag{7}
\]
Their only common zero in the open orbit of that boundary divisor is
\[
y=s
\]
with multiplicities \((2,3)\).

The coefficients at the upper vertical vertices are respectively
\[
\frac{u_7}{s^2},\qquad -\frac{v_{10}}{s^3}.
\tag{8}
\]
Writing \(z=xy\), prescribe the adjacent diagonal faces by
\[
\begin{aligned}
P_{\rm diag}
 &=\frac{u_7}{s^2}\,y^8(z-\lambda)^8,\\
Q_{\rm diag}
 &=-\frac{v_{10}}{s^3}\,y^{12}(z-\lambda)^{12}.
\end{aligned}
\tag{9}
\]
They have the unique open-orbit common zero
\[
z=\lambda
\]
with multiplicities \((8,12)\).

The three face prescriptions (2), (7), and (9) agree at their shared
vertices:
\[
(8,14),\ (8,16)
\quad\text{for }P,
\qquad
(12,21),\ (12,24)
\quad\text{for }Q.
\tag{10}
\]
In particular every vertex in (1) has a nonzero coefficient after
choosing nonzero constants at \((0,0)\).

Now assign algebraically independent coefficients to every lattice
position not already fixed by (2), (7), or (9).  Equivalently, work at
the generic point of the affine coefficient space with these face
constraints.  The resulting polynomial pair \(F=(P,Q)\) has exactly
the two Newton polygons (1), the genuine outer endpoint (2), and both
forced cap factorizations.

## 3. Exact toric degree: \(131\)

Compactify the source torus by a smooth refinement of the common normal
fan of (1).  The closures of two generic fibers
\[
P=p,\qquad Q=q
\]
have total intersection number \(141\) by (6).

There are only two open boundary basepoints.

### The vertical basepoint

At \(y=s\), choose a local boundary parameter \(u\) and put \(v=y-s\).
Because the polygons contain lattice points exactly one level inward
from the vertical faces, algebraic genericity of the unprescribed
coefficients gives local equations
\[
\begin{aligned}
\widetilde P&=\alpha v^2+A u+\text{higher terms},\\
\widetilde Q&=\beta v^3+B u+\text{higher terms},
\end{aligned}
\tag{11}
\]
with
\[
\alpha\beta AB\ne0.
\]
Eliminating \(u\) leaves a unit times \(v^2\).  Therefore
\[
I_{(u,v)}(\widetilde P,\widetilde Q)=2.
\tag{12}
\]

### The diagonal basepoint

At \(z=\lambda\), the same argument uses the lattice points one level
inward from the diagonal faces.  In local coordinates it gives
\[
\begin{aligned}
\widetilde P&=\alpha' v^8+A'u+\text{higher terms},\\
\widetilde Q&=\beta' v^{12}+B'u+\text{higher terms},
\end{aligned}
\tag{13}
\]
with all displayed coefficients nonzero.  Hence
\[
I_{(u,v)}(\widetilde P,\widetilde Q)=8.
\tag{14}
\]

There are no other boundary intersections:

- on the outer face, (5) excludes a common root;
- on every unprescribed face, the relevant face resultant is nonzero at
  the algebraically generic coefficient point;
- the apparent \(y=0\) factor on the vertical face is the toric node
  leading to the outer face, where \(U(0)=V(0)=1\);
- generic target values exclude affine-axis solutions.

It follows that the generic affine fiber has exactly
\[
\boxed{\deg F=141-2-8=131.}
\tag{15}
\]

This calculation explains what the two cap faces actually control.
They account for ten intersection units at infinity.  The remaining
\(131\) sheets are not located by those two valuations.

## 4. The endpoint degree is \(21\)

For generic endpoint values \((p,q)\), equations (2) give
\[
z^2=\frac{pw}{U(w)},\qquad
z^3=\frac{qw}{V(w)},
\qquad z=xy.
\]
Eliminating \(z\) gives
\[
p^3wV(w)^2-q^2U(w)^3=0.
\tag{16}
\]
The numerator \(wV^2\) and denominator \(U^3\) are coprime by (3), (5),
and both have degree \(21\).  Every generic root of (16) recovers a
unique \(z\).  Thus
\[
\boxed{\deg F_0=21.}
\tag{17}
\]

The number \(17\) in the Darboux product is the high ramification index
at the reciprocal endpoint; it is not the geometric degree of \(F_0\).
Keeping these two numbers distinct is essential.

## 5. The normalized sheet exists but cannot descend

Use the reciprocal variables
\[
t=w^{-1},\qquad \xi=zw^3.
\tag{18}
\]
Then
\[
P_0=\xi^2A(t),\qquad Q_0=\xi^3B(t),
\tag{19}
\]
with
\[
\deg A=7,\qquad\deg B=10,\qquad
3A'B-2AB'=t^{16}.
\tag{20}
\]

Every nonouter case-c block has transverse \(z\)-degree strictly below
\(2\) in \(P\) or below \(3\) in \(Q\).  Hence, after setting
\(\epsilon=\xi^{-1}\), the comparison equations
\[
\Xi^2A(T)=P,\qquad \Xi^3B(T)=Q
\tag{21}
\]
reduce at \(\epsilon=0\) to the endpoint equations.  At generic
\(t\ne0\), their implicit determinant is
\[
-t^{16}\ne0.
\tag{22}
\]
Thus (21) has a unique formal comparison branch normalized by
\[
\Xi/\xi=1+O(\epsilon),\qquad T=t+O(\epsilon).
\tag{23}
\]

Suppose this branch belonged to \(k(x,y)\).  It would define a dominant
rational map \(H\) with
\[
F=F_0\circ H.
\tag{24}
\]
Degrees of generically finite rational maps multiply, so (15), (17)
would imply
\[
131=21\deg H.
\tag{25}
\]
This is impossible.  Therefore the normalized branch is not rational.

The divisor-invariance section theorem from
`GLOBAL_DARBOUX_DIVISOR_SECTION_AUDIT.md` applies to (21), independently
of the missing Keller bracket.  If
\(\operatorname{div}(\Xi^5T^{17})\) were invariant under the normal
closure group, the whole branch would descend.  Consequently
\[
\boxed{
\operatorname{div}\!\left(\Xi^5T^{17}\right)
\text{ is not Galois invariant}.
}
\tag{26}
\]

## 6. Scope and the narrowed positive target

This result does not challenge the exact case-c emptiness certificate.
The algebraically generic lower coefficients in Section 2 do not solve
\[
[P,Q]=1
\quad\text{or its reduced form}\quad
[P,Q]=x^2.
\]
The complete bracket recurrence is precisely what rules them out.

It does prove that no argument based only on:

- the two Newton polygons;
- their principal-divisor intersection numbers;
- the genuine outer Wronskian;
- the \((2,3)\) and \((8,12)\) cap roots; and
- the normalized outer comparison germ

can establish support exhaustion for
\(\operatorname{div}(\sigma J/J)\).

For a higher-degree minimal-pair configuration where the coefficient
scheme is not already empty, the viable positive target must control
the **successive normal jets** at every infinitely-near point above both
cap roots.  A theorem stopping at the two face valuations necessarily
leaves the \(131\)-sheet interior contribution uncontrolled.

The lattice counts, mixed volume, face compatibility, local intersection
losses, and degree obstruction are checked by
`verify_case_c_cap_support_exhaustion_no_go.py`.
