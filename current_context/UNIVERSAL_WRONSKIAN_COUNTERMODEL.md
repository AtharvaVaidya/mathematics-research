# A scale-five countermodel to Wronskian-only elimination

Date: 25 July 2026

## Result

The universal bound

\[
\deg(2XT'-3X'T)\le r-1
\]

does not, by itself, eliminate the pole-sensitive marked cusp at every
scale.  At \(r=5\) there is a primitive characteristic-zero pair with

\[
\deg X=10,\qquad \deg T=15,\qquad
\deg(T^2-X^3)=10,\qquad
\deg(2XT'-3X'T)=4,
\]

and a marked point at \(h=0\) for which, after the required linear shear,

\[
\operatorname{ord}_0(X-X(0))=3,\qquad
\operatorname{ord}_0(B-B(0))=5.
\]

This is a countermodel to a proposed proof mechanism, not a Keller map.
It shows that the successful scale-four Wronskian obstruction uses a
genuinely exceptional zero-dimensional degeneration.  Any all-scale
argument needs more global five-block, endpoint, or semigroup data.

## Exact normalized system

Put

\[
X=h^{10}+\sum_{i=0}^9a_i h^i,\qquad
T=h^{15}+\sum_{i=0}^{14}b_i h^i
\]

and normalize the marked \((3,5)\) closure by

\[
a_1=a_2=0,\quad a_3=1,\qquad
b_1=b_2=0,\quad b_4=b_3a_4.
\]

Writing \(W=2XT'-3X'T\), the ten rows
\([h^{23}]W,\ldots,[h^{14}]W\) solve triangularly for
\(b_{14},\ldots,b_5\).  The condition \(\deg W\le4\) leaves nine
equations \([h^{13}]W=\cdots=[h^5]W=0\) in

\[
a_0,a_4,a_5,a_6,a_7,a_8,a_9,b_0,b_3.
\]

The actual contact-five lead is

\[
L=b_5-b_3a_5\ne0.
\]

Adjoin an auxiliary variable to invert the numerator of \(L\).

## A simple point modulo \(32003\)

In signed representatives, the saturated system has the point

\[
\begin{array}{c|rrrrrrrrrr}
 &a_0&a_4&a_5&a_6&a_7&a_8&a_9&b_0&b_3&\mathrm{aux}\\ \hline
 &-1727&-6872&8738&-14424&-9482&-10323&-10862&
 -10303&-7755&-3823 .
\end{array}
\]

All ten equations vanish exactly modulo \(32003\), while the determinant
of their \(10\times10\) Jacobian is

\[
13811\ne0\pmod{32003}.
\]

Every denominator introduced by the triangular solve is a unit at this
prime.  Multivariate Hensel therefore gives a unique isolated lift in an
unramified neighborhood over \(\mathbf Z_{32003}\).  Since the point is
isolated, its coordinates are algebraic over \(\mathbf Q\); choosing an
embedding into \(\mathbf C\) gives the asserted characteristic-zero pair.

At the reduced point one directly obtains

\[
\deg X=10,\quad \deg T=15,\quad\deg D=10,\quad\deg W=4,
\]

with \(X,T,D\) squarefree and \(\gcd(X,T)=1\).  Moreover

\[
\gcd(X',T')=h^2,
\qquad
W\doteq h^2(h-8183)(h+4956).
\]

These open conditions persist on the Hensel lift.

Finally, a common polynomial right factor must have degree dividing
\(\gcd(10,15)=5\).  A degree-five right factor would make
\(\gcd(X',T')\) have degree at least four, contradicting the degree-two
gcd above.  The lifted pair is therefore primitive.

## Strategic conclusion

At scale \(r\), the normalized \((3,5)\) Wronskian system has expected
dimension \(r-5\).  Scale four is overdetermined and empty; scale five is
zero-dimensional and populated; larger scales should not be attacked by
repeating the scale-four elimination.

The almost-Belyi map

\[
R(h)=\frac{T(h)^2}{X(h)^3}
\]

explains the surviving freedom.  Its logarithmic derivative is

\[
\frac{R'}R=\frac{W}{XT}.
\]

More precisely, assume \(X,T\) are coprime and put \(d=\deg D\).
The leading term in

\[
TW=XD'-3X'D
\]

has coefficient \((d-6r)\operatorname{lc}(D)\), so for \(D\ne0\)

\[
\boxed{\deg W=d-r-1}.
\]

Thus every primitive coprime pair has \(d\ge r+1\), and the extremal
bound \(d\le2r\) is equivalent to \(\deg W\le r-1\).

The zeros of \(W\) have an exact ramification interpretation.  At a root
of \(X,T,\) or \(D\) of multiplicity \(e\), respectively, \(W\) has
multiplicity \(e-1\).  After removing those repeated-root factors, every
remaining zero of \(W\) is a critical point of \(R\) over a value other
than \(0,\infty,1\).  Riemann--Hurwitz becomes

\[
\begin{aligned}
12r-2
={}&3r+4r+(6r-d-1)+\deg W\\
={}&12r-2.
\end{aligned}
\]

Consequently the Wronskian bound is an exact ramification budget, not a
hidden surplus that could yield a general contradiction.

The marked cusp consumes a double zero of the degree-four critical
polynomial \(W\), while two further simple critical points remain.  Thus
Riemann--Hurwitz is exactly compatible with the marked cusp.

Run:

```bash
.venv/bin/python route_bd_universal_wronskian_countermodel.py
```

The verifier reconstructs the triangular system, checks the modular point
and nonzero Jacobian determinant, and verifies the displayed ramification
and primitivity data.
