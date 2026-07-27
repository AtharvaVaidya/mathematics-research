# Closure of every binary degree-two Newton face

Date: 25 July 2026

> **Correction.**  References here to the older pure-face
> source-boundary Euler lemma are superseded.  That boundary equation
> omitted exact seed layers after the change \(t=u/x\).  The mixed
> Newton-degree-two recurrence below remains valid; the pure binary
> cases are now proved by the exact first-lower numerator and forbidden
> descent in
> `WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_CLOSURE.md`.

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift,
and let \(U\) be its second-subduction coordinate.  For every
\(n\ge2\), consider
\[
Q_n
=B^{n-2}\left(\lambda A^2+\mu AB+\nu B^2\right),
\qquad \lambda\ne0.
\tag{1}
\]
No polynomial graph \(z=g(x,y)\) makes
\[
\bigl(U\circ F,\ Q_n\circ F\bigr)\big|_{z=g}
\tag{2}
\]
have nonzero constant Jacobian.

In the all-degree binary characteristic classification, (1) is
exactly the family whose Newton polynomial has degree \(d=2\).
A nonpolynomial characteristic has a nonzero negative \(t\)-tail
before the first lower seed.  Every honest mixed polynomial
completion is then excluded on the first lower seed slice: its
inhomogeneous characteristic equation has an unavoidable double pole,
whereas the characteristic operator applied to a polynomial graph
sector has only simple poles.  The pure member is already closed by
the boundary-jet theorem.

The polynomial-completion classification has a sharp first example.
No mixed quadratic characteristic can be graph-compatible for
\(n\le11\).  At \(n=12\), the perfect-square face has
\[
I=81,\qquad J=79,\qquad
\gamma_{\rm char}
=c_0x^2u^{50}(u+\eta x)^{29}.
\tag{3}
\]
Its first-lower forcing has the nonzero double-pole coefficient
\[
-1400\,x^{-1}t^{-2}.
\tag{4}
\]
Thus the first honest completion is excluded without solving for
graph coefficients.

There is an important timing point.  The pole obstruction occurs at
the first lower seed drop \(m+4\).  The fixed cleared source-axis
residual for \(d=2\) occurs later, at \(m+6\), and is not combined
with it.  This separation is essential to the proof.

Arbitrary affine perturbations of either target coordinate enter
after the pole obstruction.  The theorem does not address Newton
degrees \(d\ge3\) or targets involving \(C\).

## 1. Highest characteristic

Put
\[
u=1+xy,\qquad t=\frac ux,\qquad
\gamma=1-\frac{57}{34}xy+x^2g(x,y).
\tag{5}
\]
The highest sectors are
\[
\begin{aligned}
U^{(0)}&=\theta x^{15}t^{20}\gamma^{17},\\
A^{(0)}&=q_6x^4t^6\gamma^4,\\
B^{(0)}&=p_5x^4t^5\gamma^4,
\end{aligned}
\tag{6}
\]
where
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{7}
\]
After absorbing the nonzero coefficient
\(\lambda q_6^2p_5^{n-2}\), the highest sector of (1) is
\[
V^{(0)}
=x^{4n}t^{5n}\gamma^{4n}P(t),
\qquad
P(t)=t^2+bt+c.
\tag{8}
\]
The highest Jacobian equation is
\[
\begin{aligned}
\mathcal L_{n,P}(\gamma)={}&
x\left(
\frac{5n}{t}+17\frac{P'}P
\right)\gamma_x
-8n\gamma_t\\
&+\left(
-\frac{5n}{t}+15\frac{P'}P
\right)\gamma=0.
\end{aligned}
\tag{9}
\]
On a fixed \(x\)-Laurent sector, its unique formal solution is
\[
\gamma_I
=c_0x^It^rP(t)^s,
\qquad
r=\frac{5(I-1)}8,\qquad
s=\frac{17I+15}{8n}.
\tag{10}
\]
Its leading \(t\)-degree and graph degree are
\[
J=r+2s,\qquad m=I+J-2.
\tag{11}
\]
Descending, negative-tail, and pure-boundary cases are already
excluded by the all-degree highest-sector mechanisms.  The required
negative-tail timing is uniform here.  Write
\[
P(t)=t^2(1+bt^{-1}+ct^{-2}),\qquad
(1+bz+cz^2)^s=\sum_{q\ge0}a_qz^q.
\]
The identity
\[
(1+bz+cz^2)F'=s(b+2cz)F
\]
gives
\[
(q+1)a_{q+1}
=b(s-q)a_q+c(2s-q+1)a_{q-1}.
\]
Two consecutive zero coefficients force every later coefficient to
vanish.  Therefore, if \(t^JF(t^{-1})\) is not polynomial, at least
one of \(a_{J+1},a_{J+2}\) is nonzero.  It appears by drop \(J+2\),
strictly before
\[
m+4=I+J+2
\]
because \(I\ge2\).  Thus only an honest polynomial completion remains
for the recurrence below.

## 2. The first possible polynomial completion

Factorization of \(P\) makes the first frontier exact.  If
\(P\ne t^2\) and \(t^rP^s\) is a polynomial, then
\[
r\in\mathbb Z,\qquad 2s\in\mathbb Z.
\tag{12}
\]
Indeed:

- if \(P\) has two distinct nonzero roots, \(s\) and \(r\) are
  integers;
- if it has a double nonzero root, \(2s\) and \(r\) are integers;
- if it has one zero and one nonzero root, \(s\) and \(r+s\) are
  integers, hence so is \(r\).

Write
\[
I=8a+1,\qquad
L=2s=\frac{34a+8}{n}.
\tag{13}
\]
Here \(L\) is a positive integer.  Since
\[
J=5a+L,
\tag{14}
\]
graph divisibility \(I-J\ge2\) is equivalent to
\[
L\le3a-1.
\tag{15}
\]
If \(n\le11\), however,
\[
L=\frac{34a+8}{n}
\ge\frac{34a+8}{11}
>3a-1,
\tag{16}
\]
because the final difference is \((a+19)/11>0\).  Thus no mixed
polynomial completion is graph-compatible below degree twelve.

For \(n=12\), integrality of
\[
L=\frac{17a+4}{6}
\]
forces \(a\equiv4\pmod6\).  The first candidate \(a=4\) has
\(L=12>3a-1=11\), while the next candidate \(a=10\) has
\(L=29=3a-1\).  Hence the latter is sharp.

At \(n=12,a=10\),
\[
I=81,\qquad r=50,\qquad L=29,\qquad J=79.
\tag{17}
\]
Taking
\[
P(t)=(t+\eta)^2,\qquad \eta\ne0,
\tag{18}
\]
gives
\[
x^{81}t^{50}P(t)^{29/2}
=x^{81}t^{50}(t+\eta)^{29}
=x^2u^{50}(u+\eta x)^{29},
\tag{19}
\]
which is the first honest graph-divisible mixed completion.

## 3. Exact first-lower slices

The exact second-subduction numerator gives
\[
U^{(1)}
=-\frac{70}{3}\theta x^{14}t^{19}\gamma^{16}
\tag{20}
\]
as the unique first-lower slice of \(U\).

The seed ratios are
\[
\frac{q_5}{q_6}=-\frac{28}{5},
\qquad
\frac{p_4}{p_5}=-\frac{35}{6}.
\tag{21}
\]
Consequently the first-lower target slice is
\[
V^{(1)}
=x^{4n-1}t^{5n-1}\gamma^{4n-1}P_1(t),
\tag{22}
\]
where
\[
P_1(t)=A_nt^2+bB_nt+cC_n
\tag{23}
\]
and
\[
\begin{aligned}
A_n&=2\frac{q_5}{q_6}
+(n-2)\frac{p_4}{p_5}
=-\frac{35n}{6}+\frac7{15},\\
B_n&=\frac{q_5}{q_6}
+(n-1)\frac{p_4}{p_5}
=-\frac{35n}{6}+\frac7{30},\\
C_n&=n\frac{p_4}{p_5}
=-\frac{35n}{6}.
\end{aligned}
\tag{24}
\]
These are the only terms at graph-weight drop \(m+4\).
A \(q_4\) or \(p_3\) term, or two first-lower replacements, costs
\(2(m+4)\).  The added \(w\gamma\) and \(\gamma\) pieces of \(A,B\)
cost \(4m+18>m+4\).  The exact support of the second-subduction
numerator similarly certifies (20).

For the first completion (18), the lower polynomial is
\[
P_1(t)
=-\frac1{15}
\left(
1043t^2+2093\eta t+1050\eta^2
\right).
\tag{25}
\]

## 4. The first-lower double-pole obstruction

There is only one resonant highest sector at a fixed graph degree.
Indeed, using \(J=m-I+2\), the degree-two resonance relation becomes
\[
8n(m-I+2)=(5n+34)I+30-5n,
\]
and hence
\[
I=\frac{8nm+21n-30}{13n+34}.
\tag{26}
\]
Since \(13n+34>0\), this determines \(I\) uniquely.  Thus two
independent characteristic amplitudes cannot occur on the same
highest graph degree.  Because (9) preserves Laurent-\(x\) sectors,
every other monomial of the same highest homogeneous graph part is
nonresonant and its coefficient is forced to vanish.

For an honest mixed polynomial completion, evaluate
\[
J(U^{(1)},V^{(0)})+J(U^{(0)},V^{(1)})
\tag{27}
\]
on the characteristic (10), divide by the common top-top factor,
and call the result \(\mathcal R_{n,I}\).  Exact logarithmic
differentiation gives
\[
\mathcal R_{n,I}
=-\frac{7\,\mathcal N_{n,I}(t)}
{120n\,x\,t^2P(t)^2},
\tag{28}
\]
for an explicit polynomial \(\mathcal N_{n,I}\).  Two specializations
of its numerator are decisive.

This normalization does not set the characteristic amplitude to one.
Before substitution, all powers of \(\gamma\) cancel against the
same top-top common factor.  The remaining dependence is only through
\[
\frac{\gamma_x}{\gamma}=\frac Ix,\qquad
\frac{\gamma_t}{\gamma}
=\frac rt+s\frac{P'}P,
\tag{29}
\]
so the nonzero amplitude \(c_0\) in (10) cancels identically.
Equation (24) already contains every simultaneous \(q_5\) or \(p_4\)
replacement in the target, while (20) is the unique first-lower
slice of the exact \(U\)-numerator.  All other seed and lower-face
terms occur after \(m+4\).

First suppose \(c\ne0\).  Then \(t=0\) is not a root of \(P\), and
\[
\mathcal N_{n,I}(0)
=25c^2n^2(I-1).
\tag{30}
\]
Since \(I\ge2\), the forcing has the nonzero double-pole coefficient
\[
\lim_{t\to0}t^2x\mathcal R_{n,I}
=-\frac{35}{24}n(I-1)\ne0.
\tag{31}
\]

Now suppose \(c=0,b\ne0\), so
\[
P(t)=t(t+b).
\tag{32}
\]
After the common powers of \(t\) are cancelled, the other root still
has
\[
\lim_{t\to-b}(t+b)^2x\mathcal R_{n,I}
=-\frac{
7(17I+15)(4n-1)
}{120n}\ne0.
\tag{33}
\]

For a correction on the required \(x^{-1}\)-sector, write
\[
\delta\gamma=x^{-1}\psi(t).
\tag{34}
\]
The exponent \(-1\) is not an ansatz: (28) lies entirely in the
\(x^{-1}\)-sector, while (9) has coefficients depending only on
\(t\) apart from \(x\partial_x\), so it preserves Laurent powers of
\(x\).  Corrections on every other sector satisfy separate equations
and cannot affect (28).  Adding a homogeneous solution on the
\(x^{-1}\)-sector also cannot alter the forcing because it lies in
the kernel of \(\mathcal L_{n,P}\).

Here \(\psi\) must be polynomial.  Indeed, the coordinate substitution
\[
y=t-x^{-1}
\]
embeds \(\mathbb C[x,y]\) in the Laurent-polynomial ring
\(\mathbb C[x,x^{-1},t]\).  Consequently every coefficient of a
fixed Laurent power of \(x\) in
\[
\gamma=1-\frac{57}{34}xy+x^2g(x,y)
\]
is a polynomial in \(t\).  Equation (9) preserves Laurent powers of
\(x\), and the forcing (28) lies entirely on the \(x^{-1}\)-sector.
Thus denominators in \(\psi\) cannot be cancelled by contributions
from another \(x\)-sector.

For polynomial \(\psi\),
\(\mathcal L_{n,P}(\delta\gamma)\) has denominator dividing
\[
tP(t).
\tag{35}
\]
More precisely, a root of \(P\) of multiplicity \(e\) contributes
\[
\frac{P'}P=\frac{e}{t-\alpha}+\text{regular},
\]
which is still only a simple pole.  In the \(c\ne0\) case, \(t=0\)
is not a root of \(P\), so (9) has only its displayed simple
\(1/t\)-pole there.  In the \(c=0,b\ne0\) case, \(-b\) is a simple
nonzero root.  Therefore the homogeneous operator cannot cancel the
double pole (31) or (33).  Every honest mixed quadratic \(P\) has either
\(c\ne0\) or \(c=0,b\ne0\), so these two cases exhaust the family.

For the first completion \(n=12,I=81,P=(t+\eta)^2\), equation (31)
is exactly the coefficient (4).

The pole obstruction is on the \(m+4\) slice.  Clearing the highest
equation with
\[
H=x^2P(u/x)
\tag{36}
\]
would place its fixed source-axis jet at \(m+2d+2=m+6\).  That later
coefficient is irrelevant because the recurrence already fails at
\(m+4\); the two levels are never added.

When \(b=c=0\), \(P=t^2\) is the pure monomial face
\(A^2B^{n-2}\), already excluded by the exact boundary-jet theorem.
This proves the nonconstant-graph statement.

## 5. Affine terms and constant graphs

The leading \(A^2B^{n-2}\) target term lies at least \(4m+18\) above
an affine second-coordinate perturbation.  An affine
first-coordinate perturbation lies \(13m+51\) below \(U\).  Neither
can reach the \(m+4\) pole obstruction.

For constant graphs, let \(g=z_0\) and put
\[
h=-\frac{57}{34}y+z_0x.
\tag{37}
\]
The toric Jacobian of the highest form of \(U\) with
\(A^2B^{n-2}\) has coefficient pair
\[
\left((5n+98)z_0x,
8(8-n)\left(-\frac{57}{34}\right)y\right).
\tag{38}
\]
It is nonzero except possibly at
\[
z_0=0,\qquad n=8.
\tag{39}
\]

That exception has an exact next-diagonal certificate.  On \(z=0\),
write \(v=xy\) and
\[
U=x^{-5}H_0(v),\qquad
A^2B^6=x^{-10}K_0(v).
\tag{40}
\]
The exact seed and second-subduction numerator give
\[
\begin{aligned}
\deg H_0&=37,&
\frac{(H_0)_{36}}{(H_0)_{37}}&=\frac{562}{57},\\
\deg K_0&=74,&
\frac{(K_0)_{73}}{(K_0)_{74}}&=\frac{1306}{57}.
\end{aligned}
\tag{41}
\]
Moreover,
\[
(H_0)_{37}=\theta a^{17},\qquad
(K_0)_{74}=q_6^2p_5^6a^{32},
\qquad a=-\frac{57}{34}.
\tag{42}
\]
Direct differentiation gives
\[
J(U,A^2B^6)
=5x^{-15}(2H_0'K_0-H_0K_0').
\tag{43}
\]
Its \(v^{109}\)-coefficient is
\[
\frac{910}{57}\theta q_6^2p_5^6a^{49}\ne0,
\tag{44}
\]
producing the degree-\(203\) monomial \(x^{94}y^{109}\).

If the \(AB^7\) coefficient in \(Q_8\) is nonzero, its nonzero
degree-\(204\) toric top leads instead.  If that coefficient vanishes
but the \(B^8\) coefficient is nonzero, its degree-\(203\) top is
\(x^{95}y^{108}\), distinct from (44).  Cancellation is impossible.

Combining Sections 1--5 proves the all-degree \(d=2\) theorem.

The accompanying exact verifier is
`verify_weighted_lift_all_degree_d2_recurrence_closure.py`.
