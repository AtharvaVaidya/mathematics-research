# An all-scale obstruction to the pole-sensitive marked cusps

Date: 25 July 2026

## Theorem

Let a genuine consecutive \((2,3)\) five-block completion have
\[
\deg A=2R,\qquad \deg B=3R,
\]
and outer pair
\[
p_2=\frac Uh,\qquad q_3=\frac Vh,\qquad
UV+2hUV'-3hU'V=1,
\]
where
\[
\deg U=2R-1,\qquad \deg V=3R-2,\qquad
U(0)=V(0)=1.
\]
Assume its marked boundary branch at \(h=0\) has one of the
pole-sensitive nonintegral types
\[
\operatorname{ord}_0(A-A(0))=2t+1,\qquad
\operatorname{ord}_0(B-B(0))=3t+2,\qquad
\operatorname{ord}_0p_1=t.
\]
Then no such completion exists.

Thus the obstruction is not special to the scale-four cells
\[
(3,5,1),\qquad(5,8,2),\qquad(7,11,3).
\]
It excludes the complete infinite family selected by the fixed-pole
valuation equation \(2n=3m+1\).

## 1. The deficit-one mode

The universal bounded kernel at deficit one has two \(C\)-modes,
\[
C=1,\qquad
C_*=\frac{U^2-u_0^2-2u_0u_1h}{h}.
\]
For
\[
\mathcal A_C
=hCU'-\frac12CU-\frac12hC'U
\]
one has
\[
\mathcal A_1=hU'-\frac12U,
\]
and a direct simplification gives
\[
\mathcal A_{C_*}
=-2u_0u_1\left(hU'-\frac12U\right)-u_0^2U'.
\]
Consequently every nonzero deficit-one coefficient is
\[
\boxed{p_1=(ah+b)U'-\frac a2U.} \tag{1}
\]

The outer equation makes every root of \(U\) nonzero and simple, with
\(V\ne0\) there.  Moreover
\[
\boxed{\gcd(U,p_1)=1.} \tag{2}
\]
Indeed, if \(U(\alpha)=p_1(\alpha)=0\), the four lower bracket rows first
give, after evaluating the full bracket at \(h=\alpha\),
\[
-\bigl(A'+p_1'z+p_2'z^2\bigr)
 \bigl(q_1+2q_2z+3q_3z^2\bigr)
=\text{unit}\cdot z^4.
\]
The outer equation makes
\[
p_2'(\alpha)=\frac{U'(\alpha)}{\alpha}\ne0,\qquad
q_3(\alpha)=\frac{V(\alpha)}{\alpha}\ne0.
\]
Both quadratic factors must therefore be scalar multiples of \(z^2\),
which forces
\[
A'(\alpha)=p_1'(\alpha)=q_1(\alpha)=q_2(\alpha)=0.
\]
But (1) says either \(a=0\), when \(p_1=bU'\) is nonzero at \(\alpha\),
or \(a\ne0\), when \(ah+b=0\) at \(\alpha\) and
\[
p_1'(\alpha)=\frac a2U'(\alpha)\ne0.
\]
Both alternatives contradict the bracket rows.

## 2. A local multiplicity lemma

Let \(\beta\ne0\) be a root of \(p_1\), of multiplicity \(m\).  By (2),
\(p_2(\beta)\ne0\).

First,
\[
\boxed{A'(\beta)=0.} \tag{3}
\]
If \(A'(\beta)\ne0\), write the boundary as \(B=g(A)\).  The graph
identities are
\[
\begin{aligned}
q_3&=g''p_1p_2+\frac16g'''p_1^3,\\
0&=\frac12g''p_2^2+\frac12g'''p_1^2p_2
  +\frac1{24}g''''p_1^4.
\end{aligned}
\]
At \(p_1=0\), the first identity gives \(q_3(\beta)=0\).  The outer
equation makes this a simple zero.  The second identity gives
\(g''(\beta)=0\), and differentiating the first then gives
\(q_3'(\beta)=0\), a contradiction.

Complete the square in the source:
\[
\zeta=\sqrt{p_2}\left(z+\frac{p_1}{2p_2}\right),\qquad
P=\zeta^2+H(h).
\]
The boundary \(z=0\) is \(\zeta=s(h)\), with
\(\operatorname{ord}_\beta s=m\).  Since \(p_2\) and \(h\) are units,
the Jacobian equation becomes
\[
\{P,Q\}_{\zeta,h}=u(h)(\zeta-s(h))^4,\qquad u(\beta)\ne0.
\]
Write
\[
Q=q_0+q_1\zeta+q_2\zeta^2+q_3\zeta^3.
\]
The relevant exact rows are
\[
\begin{aligned}
H'q_1&=-us^4,\\
2q_1'-3H'q_3&=6us^2,\\
2q_3'&=u.
\end{aligned}
\tag{4}
\]
By (3), \(H'(\beta)=0\).  Put \(b=\operatorname{ord}_\beta H'\).
The last row says that \(q_3\) is either a unit or has a simple zero.
If \(b\le2m-2\), the first row of (4) gives
\[
\operatorname{ord}_\beta q_1=4m-b\ge2m+2.
\]
Consequently
\[
\operatorname{ord}_\beta q_1'\ge2m+1,\qquad
\operatorname{ord}_\beta(H'q_3)\le b+1\le2m-1.
\]
The second row of (4) would then have a unique term of order below the
right-hand order \(2m\), which is impossible.  Hence
\[
b\ge2m-1.
\]

Since
\[
A'=H'+2ss',
\]
this yields the uniform bound
\[
\boxed{\operatorname{ord}_\beta A'\ge2m-1.} \tag{5}
\]

## 3. The degree count

At the marked point,
\[
\operatorname{ord}_0p_1=t,\qquad
\operatorname{ord}_0A'=2t.
\]

If \(a\ne0\) in (1), then
\[
\deg p_1=2R-1.
\]
The sum of the nonmarked multiplicities of \(p_1\) is \(2R-1-t\).
Using \(2m-1\ge m\) in (5), the forced degree of \(A'\) is at least
\[
2t+(2R-1-t)=2R-1+t>2R-1,
\]
contrary to \(\deg A'=2R-1\).

If \(a=0\), then \(p_1=bU'\) and
\[
\deg p_1=2R-2.
\]
The same count gives
\[
\deg A'\ge2t+(2R-2-t)=2R-2+t.
\]
This is already too large for every \(t\ge2\).

Only \(t=1\) can attain equality.

## 4. The sole equality case

In the remaining case,
\[
p_1=bU',\qquad
A'=\lambda hU'
\]
for nonzero constants \(b,\lambda\).  The first bracket row gives
\[
q_1=\frac{b}{\lambda}\frac{B'}h,
\qquad
\deg q_1=3R-2.
\]

The second equality above follows from the equality case of the preceding
degree count: every nonmarked root of \(U'\) is simple, each consumes
exactly one zero of \(A'\), and \(A'\) has no other root.  At the marked
point \(U'\) has order one while \(A'\) has order two, so the divisors of
\(A'\) and \(hU'\) coincide.

Here \(u_1=0\), and the high deficit-one partner simplifies, up to a
nonzero scalar, to
\[
q_2
=V'+\frac{V}{2h}-\frac{U}{2u_0^2h}.
\]
Its leading coefficient is
\[
\left(3R-2+\frac12\right)\operatorname{lc}(V)\ne0,
\]
so
\[
\deg q_2=3R-3.
\]

Use the original \(z^1\) bracket row
\[
h^2\left(
2a_2B'+p_1q_1'-p_1'q_1-2A'q_2
\right)+2hB'=0,
\qquad
a_2=\frac{U-1}{h}.
\tag{6}
\]
Here \(a_2\) is the polynomial part of the total quadratic coefficient
\(U/h=1/h+a_2\).  Equivalently, one may use \(U/h\) in (6) and absorb
the displayed \(2hB'\) term; the two conventions must not be mixed.
The degrees inside the parentheses are
\[
\begin{array}{c|c}
\text{term}&\text{degree}\\ \hline
a_2B'&5R-3\\
p_1q_1'&5R-5\\
p_1'q_1&5R-5\\
A'q_2&5R-4.
\end{array}
\]
The outside term \(hB'\) has degree \(3R\).  Therefore
\(2h^2a_2B'\) is the unique highest-degree term in (6), with nonzero
coefficient.  This is impossible.

The equality case is eliminated, completing the proof.

## 5. Companion outer-root covariant

For
\[
\begin{aligned}
J&=A'B''-B'A'',\\
K&=A'J'-3A''J,\\
L&=A'K'-5A''K,
\end{aligned}
\]
the fourth Taylor row clears to
\[
h^2p_1^4L
+12hp_1^2(A')^2UK
+12(A')^4U^2J=0.
\tag{7}
\]
Together with (2), this proves
\[
\boxed{U\mid L.}
\]
At a root of \(U\) where \(A'\ne0\), one has
\[
K\ne0,\qquad \operatorname{ord}L=1.
\]
At a critical root with \(\operatorname{ord}A'=e\), the cleared third
and fourth graph rows sharpen this to
\[
\operatorname{ord}K=5e,\qquad
\operatorname{ord}L=7e+1,\qquad
\operatorname{ord}(3K^2-JL)=10e.
\]

If \(W_d\) denotes the Wronskian of the completed and depressed boundary
pair, then \(\deg W_d\le R-1\).  This bound is for the depressed pair,
not automatically for the raw \(2AB'-3A'B\).  The marked cusp consumes
at least two zeros of \(W_d\), so at least \(R+2\) of the \(2R-1\) outer
roots are regular.  If \(H\) is their product, then
\[
H\mid L,\qquad
\gcd(H,K)=\gcd(H,L/H)=1.
\]

Finally, if \(S^2=3K^2-JL\), the rational quadratic root selected by the
five-block pole gives a global sign \(\epsilon=\pm1\) such that, writing
\(L=UM\),
\[
\begin{aligned}
h p_1^2M
  &=2(A')^2(\sqrt3\,\epsilon S-3K),\\
S+\sqrt3\,\epsilon K
  &=-2\sqrt3\,\epsilon\,
    \frac{(A')^2JU}{hp_1^2}.
\end{aligned}
\]
These congruences explain the simple regular roots and the high critical
multiplicities, but the marked-cusp degree argument above is the shorter
all-scale contradiction.

Run:

```bash
.venv/bin/python route_bd_allscale_marked_cusp_obstruction.py
```
