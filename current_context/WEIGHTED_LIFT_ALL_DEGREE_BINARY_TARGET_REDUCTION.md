# All-degree binary target reduction and the first exceptional face

Date: 25 July 2026

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift,
and let \(U(A,B,C)\) be the second-subduction polynomial.  For every
\(n\ge1\), consider a nonzero homogeneous binary target
\[
Q_n(A,B)=\sum_{j=0}^n c_jA^jB^{n-j}.
\tag{1}
\]
On every polynomial graph \(z=g(x,y)\), the highest Jacobian equation
for \((U,Q_n)\) has one characteristic formula, valid for all \(n\).
If
\[
d=\max\{j:c_j\ne0\},
\tag{2}
\]
then every possible resonant source sector \(x^It^J\) satisfies
\[
\boxed{
8nJ=(5n+17d)I+15d-5n.
}
\tag{3}
\]

This note classifies what can happen after (3):

- a nonintegral right side leaves a nonzero highest Jacobian;
- descending faces force a forbidden \(x^1\)-term;
- a nonpolynomial characteristic completion produces a negative
  \(t=u/x\) tail, whose exact depth can be compared with the next
  seed sector;
- pure monomial completions have an exact fixed Euler defect;
- genuinely polynomial mixed completions are controlled by a
  source \(x\)-adic residual until that residual meets the first
  lower seed sector.

These mechanisms prove the all-family exclusion for every binary
target degree
\[
n\le5,
\tag{4}
\]
with arbitrary affine perturbations of both target coordinates.  They
also prove every pure monomial face \(A^dB^{n-d}\), in every degree.

The first family not closed by these structural mechanisms is exactly
\[
\boxed{
n=6,\quad d=1,\quad
Q_6=B^5(\lambda A+\mu B),\quad
\lambda\mu\ne0,
}
\tag{5}
\]
on the resonant rays
\[
\begin{aligned}
I&=48k+33,&J&=47k+32,\\
m&=95k+63,&
g_m&=c\,x^{48k+31}y^{47k+32},
\qquad k\ge1.
\end{aligned}
\tag{6}
\]
For these rays the characteristic sector completes to the honest
polynomial
\[
\gamma_{\rm char}
=c\,x^{48k+33}t^{30k+20}(t+\eta)^{17k+12},
\qquad \eta\ne0,
\tag{7}
\]
and every source monomial in (7) is divisible by \(x^2\).  The first
nonzero \(x\)-adic residual appears at exactly the same graph-weight
drop \(m+4\) as the first lower seed sector.  Therefore neither term
can be discarded, and a new exact lower-seed recurrence is required.

This is an exact frontier, not a claimed counterexample or plane
Keller map.

## 1. The all-\(n\) characteristic equation

Put
\[
u=1+xy,\qquad t=\frac ux=y+\frac1x,\qquad
\gamma=1+a\,xy+x^2g(x,y),\qquad
a=-\frac{57}{34}.
\tag{8}
\]
The highest sector of \(U\) is, up to a nonzero scalar,
\[
M=x^{-5}u^{20}\gamma^{17}
=x^{15}t^{20}\gamma^{17}.
\tag{9}
\]
The highest seed sectors of \(A,B\) are
\[
A_{\rm h}=q_6x^4t^6\gamma^4,\qquad
B_{\rm h}=p_5x^4t^5\gamma^4,
\tag{10}
\]
with
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{11}
\]
Thus the whole binary face (1) has the single highest slice
\[
N=x^{4n}t^{5n}\gamma^{4n}P(t),
\tag{12}
\]
where
\[
P(t)=
\sum_{j=0}^n c_jq_6^jp_5^{n-j}t^j,
\qquad \deg P=d.
\tag{13}
\]

Exact logarithmic differentiation gives
\[
x\left(\frac{5n}{t}+17\frac{P'}P\right)\gamma_x
-8n\gamma_t
+\left(-\frac{5n}{t}+15\frac{P'}P\right)\gamma=0
\tag{14}
\]
as the necessary and sufficient equation for \(J(M,N)=0\).
The equation preserves each \(x\)-Laurent sector.  Substituting
\[
\gamma=x^I\phi(t)
\]
gives the unique formal solution
\[
\boxed{
\phi(t)=t^rP(t)^s,\qquad
r=\frac{5(I-1)}8,\qquad
s=\frac{17I+15}{8n}.
}
\tag{15}
\]
At \(t=\infty\), its leading exponent is
\[
J=r+ds
=\frac{(5n+17d)I+15d-5n}{8n},
\tag{16}
\]
which proves (3).

For a graph monomial \(g_m=cx^iy^{m-i}\),
\[
I=i+2,\qquad J=m-i,\qquad m=I+J-2.
\tag{17}
\]
Hence only integral solutions of (3) with \(I\ge2,J\ge0\) can cancel
the highest Jacobian.

## 2. The three elementary closure mechanisms

Normalize the leading coefficient of \(P\).  Formula (15) begins
\[
x^It^J(1+O(t^{-1})).
\tag{18}
\]

### 2.1. Forbidden \(x^1\)-terms

If \(J\ge I+1\), substituting \(t=y+x^{-1}\) forces
\[
c\binom{J}{I-1}x\,y^{J-I+1},
\tag{19}
\]
whose \(y\)-degree is at least two.  It is neither in \(x^2g\) nor in
the fixed part \(1+a xy\) of \(\gamma\).  Lower \(t\)-powers reach
\(x\)-exponent one with smaller \(y\)-degree and cannot cancel it.

If \(J=I-1\), the same calculation forces a nonzero \(x\)-term, also
absent from \(\gamma\).

The filtration drop of (19) is \(2(I-1)\).  Since
\[
m+4=I+J+2,
\tag{20}
\]
the forbidden term always occurs before the first lower seed sector.

The usual sector-uniqueness argument applies.  On any fixed affine
branch \(J(I)\) of (16), the leading weight and source diagonal are
affine functions of \(I\).  A lower resonant sector cannot contribute
the same diagonal through descending \(t\)-powers unless those slopes
degenerate; in the low-degree classification below the explicit
parameterizations certify this directly.

### 2.2. Negative \(t\)-tails

Suppose the formal expression \(t^rP(t)^s\) is not a polynomial in
\(t\).  Its expansion at infinity eventually has nonzero negative
powers.  Every coefficient of every \(x\)-power in
\[
\gamma(x,t)=1-a+axt+x^2g(x,t-x^{-1})
\tag{21}
\]
is polynomial in \(t\), so that negative power is impossible.
Distinct \(x\)-sectors cannot repair it because (14) has coefficients
depending only on \(t\).

If the coefficient of \(t^{-1}\) is nonzero, it occurs after exactly
\(J+1\) descending \(t\)-steps.  By (17),
\[
J+1<m+4,
\tag{22}
\]
so the lower seed cannot enter first.

For a polynomial with sparse or specially cancelling lower
coefficients, the first negative term can occur later; its exact
depth must then be checked rather than inferred from nonpolynomiality
alone.  In the degree-five boundary case below \(P\) is linear, and
the generalized binomial coefficient of \(t^{-1}\) is explicitly
nonzero.

This covers all fractional-power faces except special coefficient
choices, such as a perfect-power \(P\), for which (15) nevertheless
becomes polynomial.  Those polynomial completions must be treated
separately rather than assumed impossible.

### 2.3. Pure monomial Euler defects

If \(P=t^d\), formula (15) reduces exactly to
\[
\phi=t^J.
\tag{23}
\]
When \(I-J\ge2\), the characteristic completion
\[
x^It^J=x^{I-J}u^J
\tag{24}
\]
is graph-divisible and produces no forbidden \(x^1\)-term.

The relevant source Euler operator is
\[
\mathcal L_{n,d}
=(5n+17d)x\partial_x
+(17d-3n)u\partial_u
+(15d-5n).
\tag{25}
\]
On the fixed graph jet it gives
\[
\begin{aligned}
\mathcal L_{n,d}(1+a(u-1))
={}&8a(4d-n)xy\\
&+a(17d-3n)+15d-5n.
\end{aligned}
\tag{26}
\]
The constant coefficient simplifies to
\[
a(17d-3n)+15d-5n
=\frac{n-459d}{34}.
\tag{27}
\]
If (27) vanished, then \(n=459d\), and the characteristic relation
(3) would reduce to
\[
459J=289I-285.
\tag{28}
\]
But
\[
\gcd(289,459)=17,\qquad17\nmid285,
\tag{29}
\]
so (28) has no integral solution.  Therefore every resonant pure
monomial face has a nonzero displayed defect (26).

One must still exclude cancellation by graph terms on the same source
diagonal.  Let their total diagonal contribution be
\[
f(u)=1+a(u-1)+h(u),\qquad
h(u)\in(u-1)^2\mathbb C[u].
\tag{30}
\]
The diagonal equation is
\[
\left((17d-3n)u\partial_u+(15d-5n)\right)f=0.
\tag{31}
\]
If \(17d-3n=0\), then \(15d-5n=-40d/3\ne0\), so (31) would force
\(f=0\), contradicting \(f(1)=1\).  Otherwise every nonzero
polynomial solution of (31) is
\[
f(u)=c u^N,\qquad
N=-\frac{15d-5n}{17d-3n}.
\tag{32}
\]
But the boundary jet fixed by the graph gives
\[
f(1)=1,\qquad f'(1)=a=-\frac{57}{34}.
\tag{33}
\]
Thus \(c=1\) and \(N=a\), impossible because a polynomial monomial
has \(N\in\mathbb Z_{\ge0}\).  This boundary-jet argument, rather than
the displayed defect alone, excludes every same-diagonal
cancellation.  The defect occurs before the lower-seed drop \(m+4\).

This proves every pure \(A^dB^{n-d}\) face in every target degree.

## 3. Mixed polynomial completions and the \(x\)-adic residual

To handle a mixed \(P\), clear its denominator in the source chart.
Put
\[
H(u,x)=x^dP(u/x),
\tag{34}
\]
and define
\[
K=5nH+17uH_u,\qquad
L=-5nH+15uH_u.
\tag{35}
\]
Transforming (14) from \((x,t)\) to \((x,u)\), then back to source
\((x,y)\), gives the polynomial equation
\[
\boxed{
xK(x\gamma_x-y\gamma_y)
+u(K-8nH)\gamma_y
+xL\gamma=0.
}
\tag{36}
\]

Modulo \(x^2\), every contribution from \(x^2g\) vanishes.  If the
leading coefficient of \(P\) is \(p_d\), substituting
\(\gamma=1+a xy\) in (32) leaves
\[
\boxed{
p_d\,\frac{n-459d}{34}\,x
\pmod{x^2}.
}
\tag{37}
\]
Thus the same remarkable integer \(459\) controls every mixed face.
As above, its coefficient cannot vanish on an integral resonant
sector.

There is an important timing caveat.  The leading ordinary degree of
\(H\) is \(2d\).  The residual (33) therefore occurs at filtration
drop
\[
m+2d+2.
\tag{38}
\]
The first lower seed sector enters at drop \(m+4\).  Hence:

- for \(d=0\), one is in the already factored pure \(B^n\) case;
- for \(d=1\), the residual meets the lower seed at exactly the same
  depth;
- for \(d\ge2\), the lower seed enters before the residual.

Consequently (33) certifies the obstruction coefficient but does not
by itself close a mixed polynomial completion.  This is precisely
where the all-degree problem can first escape the elementary
forbidden-term and negative-tail arguments.

## 4. Complete classification through degree five

The resonance relation (3) can now be audited exactly.

For \(n\le4\), every resonant face with \(d>0\) has
\[
J\ge I+1,
\]
and is closed by (19).  The \(d=0\) face is pure \(B^n\) and is
closed by (26).

For \(n=5\), every \(d\ge2\) resonant face still has \(J>I\).
The only boundary face is \(d=1\), where
\[
I=20k+5,\qquad
J=21k+5,\qquad k\ge0.
\tag{39}
\]
For \(k\ge1\), one again has \(J>I\).  At \(k=0\),
\[
I=J=5,\qquad r=s=\frac52.
\tag{40}
\]
If
\[
P(t)=t+\eta,\qquad\eta\ne0,
\]
then
\[
t^{5/2}(t+\eta)^{5/2}
=t^5(1+\eta/t)^{5/2}
\tag{41}
\]
has a nonzero negative tail and is excluded by Section 2.2.  If
\(\eta=0\), the face is pure \(AB^4\) and is excluded by the Euler
defect (26).

Therefore every homogeneous binary target of degrees \(1\) through
\(5\) is excluded, including arbitrary affine perturbations.  A
target-linear addend in the first coordinate lies
\[
\deg U_0-\max(\deg A_0,\deg B_0)=13m+51
\tag{42}
\]
degrees lower and cannot reach any of the displayed obstructions.

## 5. The first exceptional family

Set \(n=6\).  Every \(d\ge2\) resonance has \(J>I\), while \(d=0\)
is the pure \(B^6\) face.  The remaining \(d=1\) relation is
\[
48J=47I-15.
\tag{43}
\]
Its nonnegative integral solutions are
\[
I=48k+33,\qquad
J=47k+32,\qquad k\ge0.
\tag{44}
\]
The characteristic exponents are
\[
r=30k+20,\qquad
s=17k+12,
\tag{45}
\]
both nonnegative integers.

At \(k=0\), \(I-J=1\), so the completion forces the forbidden
\(x^1\)-term from Section 2.1.  Let \(k\ge1\), and normalize
\[
P(t)=t+\eta.
\tag{46}
\]
If \(\eta=0\), the target is the pure monomial \(AB^5\), already
closed by (26).  If \(\eta\ne0\), (15) is the polynomial
\[
\gamma_{\rm char}
=c\,x^{48k+33}
t^{30k+20}(t+\eta)^{17k+12}.
\tag{47}
\]
Its largest \(t\)-degree is
\[
(30k+20)+(17k+12)=47k+32=J.
\]
After \(t=y+x^{-1}\), every source term therefore has \(x\)-exponent
at least
\[
I-J=k+1\ge2.
\tag{48}
\]
So (43) is a genuine polynomial-graph contribution, not a forbidden
Laurent artifact.  It annihilates the entire highest seed equation
(14).

The \(x\)-adic residual coefficient is nonzero:
\[
\frac{6-459}{34}=-\frac{453}{34}.
\tag{49}
\]
But because \(d=1\), its drop from (34) is
\[
m+4,
\tag{50}
\]
exactly the first lower seed gap.  The terms containing
\[
p_4=\frac{35}{92},
\qquad
q_5=\frac7{23}
\tag{51}
\]
can therefore interact with (45).  No degree or sector separation
removes them.

This proves that (5)--(7), with \(k\ge1\), are the first genuinely
exceptional all-degree binary faces.  The next audit should derive
the exact graph-weight-\((m+4)\) recurrence for
\[
Q_6=B^5(\lambda A+\mu B)
\tag{52}
\]
on the polynomial ansatz (43), rather than search arbitrary graph
coefficients.

## 6. Scope

The all-degree structural result is:
\[
\boxed{
\begin{gathered}
\text{all homogeneous binary targets are excluded through }n=5,\\
\text{all pure monomial faces are excluded for every }n,\\
\text{the first unresolved mixed completion is }n=6,d=1,k\ge1.
\end{gathered}
}
\tag{53}
\]

The accompanying exact verifier is
`verify_weighted_lift_all_degree_binary_target_reduction.py`.
