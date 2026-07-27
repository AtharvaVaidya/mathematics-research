# Exact differentials in the inverse character of a Kummer cover

Date: 26 July 2026

## Outcome

Let \(d\geq2\), let \(h\in\mathbf C[x]\setminus\{0\}\), and put
\[
 K=\mathbf C(x,H),\qquad H^d=h.
\]
Fix \(c\in\mathbf C^\times\).  On a connected cover, an element in
the inverse deck character has the form
\[
 A=\frac{S}{H},\qquad S\in\mathbf C(x).
\]
This note classifies exactly when
\[
 \frac{dA}{dx}=\frac{c}{H}.
\tag{1}
\]

Every rational solution \(S\) is in fact a nonconstant squarefree
polynomial.  If
\[
 S=L\prod_{i=1}^r(x-a_i),\qquad L\ne0,
\tag{2}
\]
then, up to a nonzero constant factor, necessarily
\[
 h=\prod_{i=1}^r(x-a_i)^{m_i},
\qquad
 m_i=d-\frac{dc}{S'(a_i)}\in\mathbf Z_{\geq0}.
\tag{3}
\]
Conversely, (2)--(3) are sufficient.  Exponents \(m_i=0\) are
allowed: such an \(a_i\) is a zero of \(S\), but not of \(h\).

There are two useful equivalent forms of the classification.  Put
\[
 n_i=d-m_i\in\mathbf Z\setminus\{0\},\qquad
 P=\prod_{i=1}^r(x-a_i).
\tag{4}
\]
Then
\[
 \sum_i n_i\frac{P(x)}{x-a_i}=C_0\in\mathbf C^\times,
\qquad
 S=\frac{dc}{C_0}P.
\tag{5}
\]
For \(r\geq2\), this says exactly
\[
 \sum_i n_i a_i^k=0\quad(0\leq k\leq r-2),
\qquad
 C_0=\sum_i n_i a_i^{r-1}\ne0.
\tag{6}
\]
For \(r=1\), it says \(C_0=n_1\ne0\).

The exact differential does **not** force the normalization of the
Kummer cover to have genus zero.  For example, with \(d=3\),
\[
\begin{aligned}
 S&=\frac{3c}{2}x(x^2-1),\\
 h&=(x+1)^2(x-1)^2x^5
\end{aligned}
\tag{7}
\]
satisfy (1).  The cover \(H^3=h\) is connected and has genus one.
For the connected fourth-root case, the analogous example
\[
\begin{aligned}
 S&=2c\,x(x^2-1),\\
 h&=(x+1)^3(x-1)^3x^6
\end{aligned}
\tag{8}
\]
again has genus one.

Thus a terminal inverse-character exact differential is a strong
Belyi-type restriction on \(h\), but it is not a rationality theorem
for the cover.  It also gives a sharp pole dichotomy: the only
solutions for which \(A\) has no finite pole are the one-root cases
(14) with \(m<d\).

## 1. Reduction to a polynomial numerator

Equation (1) is equivalent to
\[
 dS'-\frac{h'}hS=dc.
\tag{9}
\]
Suppose \(S\) had a pole of order \(p>0\) at \(x=a\).  If \(h\) has
multiplicity \(m\geq0\) there, the leading coefficient on the
left-hand side of (9) is proportional to
\[
 -dp-m,
\]
and has order \(-p-1\).  It cannot equal the nonzero constant on the
right.  Hence \(S\) has no finite pole and is a polynomial.  A
constant \(S\) is also impossible, so \(\deg S\geq1\).

Divide (9) by \(S\):
\[
 \frac{h'}h=d\frac{S'}S-\frac{dc}{S}.
\tag{10}
\]
If \(S\) had a zero of order \(e\geq2\), the last term in (10) would
have a pole of order \(e\), whereas a logarithmic derivative has only
simple poles.  Thus \(S\) is squarefree.

Every zero of \(h\) must now be a zero of \(S\), since otherwise the
left side of (10) has a pole and the right side does not.  At a simple
zero \(a_i\) of \(S\), the residue of the right side is
\[
 d-\frac{dc}{S'(a_i)}.
\]
It must be the nonnegative integral multiplicity \(m_i\) of \(h\).
This proves necessity of (2)--(3).

Conversely, the rational function on the right side of (10) is
proper and has precisely the residues \(m_i\) at the \(a_i\).
Therefore it equals
\[
 \sum_i\frac{m_i}{x-a_i}
 =\frac{d}{dx}\log\prod_i(x-a_i)^{m_i}.
\]
This proves sufficiency, with an arbitrary nonzero constant factor in
\(h\).

## 2. Moment form and the resonances

Writing \(S=LP\), equation (9) becomes
\[
\begin{aligned}
 dS'-\frac{h'}hS
 &=LP\sum_i\frac{d-m_i}{x-a_i}\\
 &=L\sum_i n_i\frac{P}{x-a_i}.
\end{aligned}
\tag{11}
\]
It is the nonzero constant \(dc\) exactly when (5) holds.  Expansion
at infinity gives (6).  Conversely, (6) makes the polynomial in (5)
constant, and the Vandermonde matrix shows that its constant value
cannot vanish unless every \(n_i\) vanishes.

This identifies both apparent resonances:

1. A finite multiplicity \(m_i=d\) is impossible.  It would give
   \(n_i=0\), contradicting \(dc/S'(a_i)\ne0\).
2. If \(r\geq2\), the \(k=0\) moment in (6) gives
   \[
   \sum_i m_i=dr.
   \tag{12}
   \]
   Thus the leading terms in (9) cancel at infinity.  This infinity
   resonance is mandatory, not pathological.

For \(r\geq2\), the nonzero integers \(n_i\) sum to zero.  Hence some
\(n_i\) are positive and some are negative.  Equivalently, every such
solution has at least one multiplicity below \(d\) and at least one
multiplicity strictly above \(d\).  Multiplicities larger than \(d\)
are therefore not exceptional cases which can be discarded; they are
forced.  A multiplicity zero corresponds to the extreme allowed value
\(n_i=d\).

The pole caused by a multiplicity above \(d\) is exact on the
normalization.  Put \(g_i=\gcd(d,m_i)\).  At a point over \(a_i\), a
local parameter \(t\) may be chosen so that
\[
 x-a_i=t^{d/g_i}\cdot(\text{unit}),\qquad
 H=t^{m_i/g_i}\cdot(\text{unit}).
\]
Because \(S\) has a simple zero in \(x\),
\[
 \operatorname{ord}_t(A)
 =\frac{d-m_i}{g_i}=\frac{n_i}{g_i}.
\tag{13}
\]
Thus every solution with \(r\geq2\) has a genuine finite pole of
\(A\), of order \((m_i-d)/g_i\), over each \(a_i\) with \(m_i>d\).

When \(r=1\), one instead has
\[
 h=C(x-a)^m,\qquad m\geq0,\quad m\ne d,
\qquad
 S=\frac{dc}{d-m}(x-a).
\tag{14}
\]
This is the only nonresonant-at-infinity family.

## 3. Connectedness and genus

The Kummer cover is connected precisely when
\[
 \gcd(d,m_1,\ldots,m_r)=1,
\tag{15}
\]
where zero exponents may be omitted.  Since \(m_i=d-n_i\), this is
equivalently \(\gcd(d,n_1,\ldots,n_r)=1\).

For a connected cover, Riemann--Hurwitz gives
\[
 2g-2=-2d+
 \sum_i\bigl(d-\gcd(d,m_i)\bigr)
+\bigl(d-\gcd(d,\deg h)\bigr).
\tag{16}
\]
In the one-root family (14), connectedness means
\(\gcd(d,m)=1\), and (16) gives \(g=0\).

For \(r\geq2\), equation (12) makes infinity unramified and completely
split.  Formula (16) becomes
\[
 \boxed{
 g=1+\frac{d(r-2)-\sum_i\gcd(d,m_i)}2.
 }
\tag{17}
\]
Thus genus zero among the realized moment configurations is
equivalent to
\[
 \sum_i\gcd(d,m_i)=d(r-2)+2.
\tag{18}
\]
There is no general reason for (18) to hold.  In (7), the finite
multiplicities are \((2,2,5)\), so (17) gives \(g=1\).  In (8), they
are \((3,3,6)\), and (17) again gives \(g=1\).

## 4. The associated three-value rational map

Raising \(A=S/H\) to the \(d\)-th power gives
\[
 A^d=\kappa\prod_i(x-a_i)^{n_i}
 =:\kappa R(x).
\tag{19}
\]
Equation (5) is equivalently
\[
 \frac{R'}R=\frac{C_0}{P}.
\tag{20}
\]
Thus \(R\) has no finite critical point away from its zeros and poles.
When \(r\geq2\), (6) shows that \(R\) has local degree exactly \(r-1\)
at infinity, so infinity is critical exactly when \(r\geq3\).  After
scaling the target,
all branch values of \(R:\mathbf P^1_x\to\mathbf P^1\) lie in
\(\{0,1,\infty\}\).

The classification can therefore also be read as follows: the
allowable \(h\) are encoded by the three-value rational maps
\[
 R=\prod_i(x-a_i)^{d-m_i}
\]
whose only critical point outside the zero and pole fibres is
infinity.  This is the precise global restriction supplied by the
exact differential.

## 5. Consequences for connected normal-degree covers

Suppose a connected normal-degree reduction uses \(H^d=h\), and its
terminal equation produces an inverse-character first integral
\[
 A'=\frac{c}{H},\qquad c\ne0.
\]
Then:

1. \(h\) must have the form (3), or equivalently the moment/Belyi form
   (4)--(6).  A generic polynomial \(h\) is excluded immediately.
2. If the arithmetic frontier has \(d\mid\deg h\), the one-root
   family (14) is incompatible with connectedness.  Hence
   \(r\geq2\), \(\deg h=dr\), infinity is unramified and completely
   split, and multiplicities occur on both sides of \(d\).  In
   particular, (13) gives a finite pole of \(A\).
3. The cover need not be rational.  In particular, replacing it by a
   rational parameter solely because the terminal differential is
   exact is invalid; (7) and (8) are exact connected genus-one
   counterexamples to that inference.
4. What remains valid is the three-value restriction (19)--(20).
   It turns the possible terminal covers into a discrete
   dessin/passport problem once the multiplicities are fixed.

This result concerns the terminal Kummer differential only.  The
other conserved coefficient levels in a normal-degree system may
exclude some or all of these Kummer configurations, but that requires
additional equations.
