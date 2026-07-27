# Exclusion of the constant-\(h\), only-\(j\) \((9,6)\) chart

Date: 26 July 2026

## Outcome

Consider the cube-\(h\) normal form of
`NORMAL_DEGREE_96_CUBE_LAURENT_TIME_REDUCTION.md`, and assume:

1. \(h=r^3\) with \(r\in\mathbf C^\times\) constant; and
2. the six extra upper constants vanish:
   \[
   \kappa _8=\kappa _7=\kappa _5=\kappa _4
   =\kappa _2=\kappa _1=0.
   \tag{1}
   \]

Thus
\[
 f=(g^{3/2})_+ +j(g^{1/2})_+,
 \qquad
 g=w^6+aw^4+bw^3+cw^2+dw+q,
\tag{2}
\]
but, unlike the connected chart, the four conserved levels
\[
 I_{10}=U,\quad I_{11}=V,\quad
 I_{12}=W,\quad I_{13}=Z
\tag{3}
\]
are arbitrary constants.

There is no Keller pair in this chart.

The proof isolates the only potentially difficult level \(U\ne0\).
After exact elimination, every nonconstant polynomial coefficient
curve on that level has one upper Newton edge,
\[
 27C_0^5=32U D_0^2,
\tag{4}
\]
and the Laurent time \(A_5\) has degree \(12e\ge12\).  On the other
hand, the constant-\(r\) terminal equation makes \(A_5\) affine
linear.  This contradiction closes the chart.

This is a genuine enlargement of the connected-chart exclusion:
the levels in (3) are not assumed to have the deck-character values
\(U=V=Z=0\).

## 1. Centered invariant system

Put
\[
 C=c-\frac{a^2}{4},\qquad
 D=d-\frac{ab}{2},\qquad
 Q=q-\frac{b^2}{4}.
\tag{5}
\]
The exact first integrals are
\[
\begin{aligned}
I_{10}&={3\over8}
 \left(3C^2a-12CQ-8Cj-6D^2\right),\\
I_{11}&={3\over8}
 \left(3C^2b+6CDa-12DQ-8Dj\right),\\
I_{12}&={1\over8}\left(
 3C^3-3C^2a^2+18CDb+12CQa+8Caj
 +6D^2a-18Q^2-24Qj\right),
\end{aligned}
\tag{6}
\]
together with
\[
 \boxed{
 I_{13}=\frac98C^2D-\frac b3I_{10}-\frac a6I_{11}.
 }
\tag{7}
\]
Since \(r\) is constant, depression uses a polynomial translation
and
\[
 a,b,C,D,Q\in\mathbf C[x].
\tag{8}
\]
The Laurent reduction supplies \(A_5\in\mathbf C[x]\) with
\[
 6A_5'=\frac{\lambda}{r}\in\mathbf C^\times.
\tag{9}
\]
Consequently
\[
 \boxed{\deg A_5=1.}
\tag{10}
\]

## 2. Elementary branches

If \(C=0\), then \(U=-9D^2/4\).  When \(D\ne0\), equations
\(I_{11}=V\), \(I_{12}=W\), and (7) successively make
\(Q,a,b\) constant.  When \(D=0\), one has \(U=V=Z=0\);
\(Q\) is constant and both normalized coordinates are functions of
the same cubic
\[
 \rho=w^3+\frac a2w+\frac b2.
\]
Their bracket is zero.  Thus \(C=0\) is impossible.

Assume \(C\ne0\).  If \(U=V=0\) and \(Z\ne0\), (7) makes
\(C^2D\) a nonzero constant.  Polynomiality makes \(C,D\) constant,
and \(I_{12}=W\) is a genuine quadratic equation in \(Q\), so every
coefficient is constant.  If \(U=V=Z=0\), this is exactly the
connected-level system already excluded by the two-value/cuspidal
argument.

It remains to consider \(U=0,V\ne0\).  A root of \(C\) would make
\(D=0\) in the \(I_{10}\) equation and then \(V=0\) in the
\(I_{11}\) equation.  Hence the polynomial \(C\) has no root and is
constant.  Eliminating \(a,b,Q\) from (6)--(7) leaves the following
equation in \(D\):
\[
\begin{aligned}
0={}&-6561C^8D^2+11664C^6DZ+384C^5V^2
 -11664C^4D^3V-5184C^4Z^2\\
&+10368C^2D^2VZ-1024C^2V^2W+1024C^2V^2j^2\\
&+2048CDV^3-5184D^4V^2 .
\end{aligned}
\tag{11}
\]
Its leading coefficient as a polynomial in \(D\) is
\(-5184V^2\ne0\).  Thus \(D\), and then every coefficient, is
constant.  This also gives zero bracket.  Therefore any remaining
candidate must have
\[
 \boxed{U\ne0.}
\tag{12}
\]

## 3. Exact elimination when \(U\ne0\)

On \(C\ne0\), solve \(I_{10}=U\) and (7) for \(a,b\):
\[
\begin{aligned}
a&=\frac{\frac83U+12CQ+8Cj+6D^2}{3C^2},\\
b&=\frac{27C^2D}{8U}-\frac{Va}{2U}-\frac{3Z}{U}.
\end{aligned}
\tag{13}
\]
After this substitution, \(I_{11}=V\) and \(I_{12}=W\) have
numerators
\[
\begin{aligned}
E_{11}={}&243C^5D-216C^3Z-144C^2QV-96C^2Vj
 -72CD^2V\\
&+288CDQU+192CDUj-96CUV+288D^3U+128DU^2,
\end{aligned}
\tag{14}
\]
and
\[
\begin{aligned}
E_{12}={}&6561C^5D^2+324C^5U-5832C^3DZ
 -3888C^2DQV\\
&-2592C^2DVj-1944C^2Q^2U-2592C^2QUj
 -864C^2UW\\
&-1944CD^3V-864CDUV-1152CQU^2-768CU^2j\\
&-576D^2U^2-256U^3.
\end{aligned}
\tag{15}
\]
Their resultant in \(Q\) is
\[
 \operatorname {Res}_Q(E_{11},E_{12})
 =648C^2U\,P(C,D).
\tag{16}
\]
The upper Newton edge of \(P\), for
\(\operatorname{wt}(C,D)=(2,5)\), is exactly
\[
 \boxed{
 P_{\rm top}
 =-243D^2(27C^5-32UD^2)^2.
 }
\tag{17}
\]
Every other monomial \(C^iD^k\) in \(P\) satisfies
\[
 2i+5k<30.
\tag{18}
\]
Together with the endpoint monomials \(C^{10}D^2\) and \(D^6\),
this says that the upper Newton polygon has exactly the one edge
displayed in (17).

If \(C\) is constant, (16) is a nonzero constant-coefficient
polynomial equation of degree six for \(D\); hence all coefficients
are constant.  If \(C\) is nonconstant and \(D\) is a nonzero
constant, the term \(C^{10}D^2\) in \(P\) is uniquely dominant, an
impossibility.

The case \(D=0\) is the lower cusp.  Equations (7) and \(I_{11}=V\)
give \(V=Z=b=0\), and the remaining level equation is
\[
\begin{aligned}
0={}&81C^5-486C^2Q^2-648C^2Qj-216C^2W\\
&-288CQU-192CUj-64U^2.
\end{aligned}
\tag{19}
\]
For nonconstant polynomials \(C,Q\), its unique upper edge gives
\[
 \deg C=2e,\qquad \deg Q=3e,\qquad C_0^3=6Q_0^2
\tag{20}
\]
for some \(e\ge1\).  Direct substitution in the residue formula for
\(A_5\) gives
\[
 \deg A_5=7e,\qquad
 [x^{7e}]A_5=-\frac{C_0^2Q_0}{16}\ne0,
\tag{21}
\]
contradicting (10).

It remains that \(C,D\) are both nonconstant.  Equations
(17)--(18) force
\[
 \deg C=2e,\qquad \deg D=5e,\qquad
 27C_0^5=32UD_0^2
\tag{22}
\]
for some \(e\ge1\).

The coefficient of \(Q\) in (14) is
\[
 144C(2UD-CV).
\tag{23}
\]
If \(2UD-CV=0\) identically and \(V\ne0\), substitution in
(14) gives a nonzero degree-five constant-coefficient equation for
the nonconstant polynomial \(C\), impossible.  If \(V=0\), it gives
\(D=0\), already handled.  Hence (14) solves \(Q\) uniquely in
\(\mathbf C(x)\), and (13) then gives \(a,b\).

Using (22), their leading terms have degrees
\[
\deg(Q,a,b)=(8e,6e,9e),
\tag{24}
\]
with leading coefficients
\[
 Q_0^{\rm new}=-\frac{27C_0^4}{16U},\qquad
 a_0=-\frac{81C_0^3}{16U},\qquad
 b_0=\frac{27C_0^2D_0}{8U}.
\]
Exact substitution into the Laurent residue \(A_5\) then gives
\[
 \boxed{
\deg A_5=12e,\qquad
[x^{12e}]A_5=\frac{567C_0^6}{2048U}\ne0.
}
\tag{25}
\]
This again contradicts (10), completing the exclusion.

## Scope

This theorem closes the constant-\(h\) subchart only when the six
extra upper constants in (1) vanish.  Constant-\(h\) charts with at
least one of those constants nonzero, and the nonconstant pure-power
\(r=\gamma(x-a)^{k+1}\) charts, remain open.

The eliminations, Newton edge, exceptional denominator, and both
leading \(A_5\) coefficients are checked exactly by
`verify_normal_degree_96_cube_constant_h_only_j_exclusion.py`.
