# The global deck budget does not force a shallow repeated root

Date: 26 July 2026

## Outcome

The local deck-gap theorem says that every repeated-root zero chart
capable of reaching the Keller scalar must satisfy
\[
bG>h,
\tag{1}
\]
and that a root in the intermediate band
\[
aG\le h<bG
\tag{2}
\]
consumes the unique zero of the affine polynomial \(P_{n-1}\).
Neither the multiplicity sum, the global first-layer degree bound, nor
the reciprocal coefficient caps force a root into the excluded band
\(bG\le h\), or force two roots into (2).

In fact there is an infinite family of exact support countermodels in
which every repeated root lies in the deep band
\[
\boxed{aG>h.}
\tag{3}
\]
The family simultaneously satisfies:

* the common-polynomial boundary \(P(X,0)=R^a\),
  \(Q(X,0)=R^b\);
* a strict matched first compact face at every repeated root;
* \(e=kh+f\), \(G=hg-ed>0\), and the residual zero root \(f\ge1\);
* the global first-layer divisibility and degree bound;
* every reciprocal coefficient cap; and
* an affine defect-one endpoint whose coefficient at
  \(\tau^{n+m-2}\) is a nonzero scalar.

It is not a Keller pair: mixed coefficients between the common first
face and the affine endpoint remain uncancelled.  Thus it does not
refute the deck-gap theorem.  It proves instead that a global closure
cannot follow from the listed degree, divisor, multiplicity, and
endpoint budgets alone.  Any successful next theorem must use the
intervening Keller equations.

## 1. A family with every root in the deep band

Let
\[
1<a<b,\qquad \gcd(a,b)=1,
\]
and choose distinct complex numbers
\(\alpha_1,\ldots,\alpha_r\), where \(r\ge2\), with multiplicities
\[
e_i\ge2,\qquad g=\sum_{i=1}^r e_i.
\tag{4}
\]
Set
\[
R(X)=\prod_{i=1}^r(X-\alpha_i)^{e_i},
\qquad
L_0(X)=\prod_{i=1}^r(X-\alpha_i)^{e_i-1}.
\tag{5}
\]
Then
\[
L_0\mid R,\qquad \deg L_0=g-r\le g-2.
\tag{6}
\]
More generally, one may replace \(L_0\) by
\[
L=L_0H,\qquad
\deg H\le r-1,\qquad H(\alpha_i)\ne0.
\tag{7}
\]
This gives \(\deg L\le g-1\); choosing \(\deg H=r-1\) saturates the
global first-layer degree cap.

Put
\[
D=R+\tau L.
\tag{8}
\]
At the root \(\alpha_i\), use the normalized local coordinate
\(R=s^{e_i}\).  Since
\[
\operatorname{ord}_{\alpha_i}L=e_i-1,
\]
the first compact face of \(D\) is, up to a nonzero coefficient,
\[
s^{e_i}+c_i\tau s^{e_i-1}
=s^{e_i}\left(1+c_i\frac{\tau}{s}\right).
\tag{9}
\]
Consequently its local data are
\[
d_i=h_i=k_i=1,\qquad
f_i=e_i-1,\qquad
G_i=h_i g-e_i d_i=g-e_i.
\tag{10}
\]
The face is strict because \(r\ge2\) implies \(e_i<g\), hence
\[
\frac{d_i}{h_i}=1<\frac{g}{e_i}.
\tag{11}
\]
Moreover
\[
G_i=g-e_i=\sum_{j\ne i}e_j\ge2.
\tag{12}
\]
Since \(a\ge2\),
\[
\boxed{aG_i\ge4>1=h_i}
\tag{13}
\]
at every root.  Thus every root is strictly beyond the intermediate
band.  This is a structural family, not a numerical coincidence.

The residual zero multiplicity after the Rees chart is
\[
f_i=e_i-1\ge1.
\]
Thus the family is genuinely in the zero-residual repeated-root
setting to which the deck-gap theorem applies.

## 2. The global first-layer and reciprocal budgets

Let
\[
n=ag,\qquad m=bg.
\]
The common powers
\[
P^{(0)}=D^a,\qquad Q^{(0)}=D^b
\tag{14}
\]
have the required boundary at \(\tau=0\).  The first \(P\)-coefficient
is
\[
T=aR^{a-1}L.
\tag{15}
\]
At \(\alpha_i\),
\[
\operatorname{ord}_{\alpha_i}T
=(a-1)e_i+(e_i-1)=ae_i-1.
\tag{16}
\]
Hence the horizontal losses in the global first-layer theorem are
all equal to one:
\[
\ell_i:=ae_i-\operatorname{ord}_{\alpha_i}T=1,
\qquad
\sum_i\ell_i=r\ge1=E.
\tag{17}
\]
This displays why the first-layer degree sum has no tendency to
produce a shallow deck gap: it supplies only the lower bound
\(\sum_i\ell_i\ge E\).

The divisibility and degree conclusions hold exactly:
\[
R^{a-1}\mid T,\qquad
\deg(T/R^{a-1})=\deg L\le g-1=g-E.
\tag{18}
\]
They hold both for the divisor choice \(L=L_0\) and for the saturated
choice (7).

Every binomial coefficient of (14) satisfies the reciprocal cap.  For
\(0\le j\le a\),
\[
\deg_X\!\left(R^{a-j}L^j\right)
\le(a-j)g+j(g-1)=n-j,
\tag{19}
\]
and the same calculation with \(a,n\) replaced by \(b,m\) proves the
\(Q\)-caps.  Thus even simultaneous saturation of the first-layer
cap does not change (13).

This family need not exploit a Kummer kernel.  For example,
\[
(e_1,e_2)=(2,3),\qquad g=5
\tag{20}
\]
has
\[
\gcd(g,e_1,e_2)=1,
\]
which eliminates every sub-\(g\) fixed-base Kummer mode.

## 3. The affine endpoint also fits

The terminal scalar classification lands at the reciprocal
coefficients \(P_{n-1}\) and \(Q_{m-1}\), both of degree at most one.
Choose any \(\beta\in\mathbb C\) and set
\[
\widetilde P
=D^a+\tau^{n-1}(X-\beta),
\qquad
\widetilde Q
=D^b+\tau^{m-1}.
\tag{21}
\]
The added coefficients obey their reciprocal caps.  For the
homogenized Keller operator
\[
\mathscr K(P,Q)
=\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X,
\tag{22}
\]
the endpoint pair alone contributes
\[
\mathscr K\!\left(
\tau^{n-1}(X-\beta),\tau^{m-1}
\right)
=-\tau^{n+m-2}.
\tag{23}
\]
No common-power term can also reach this \(\tau\)-order:
\(\deg_\tau D^a=a<n-1\) and
\(\deg_\tau D^b=b<m-1\).  Since
\(\mathscr K(D^a,D^b)=0\), the full coefficient of
\(\tau^{n+m-2}\) in
\(\mathscr K(\widetilde P,\widetilde Q)\) is exactly \(-1\).

At the root \(\alpha_i\), the surviving \((1,0)\) terminal orientation
has transformed \(t\)-orders
\[
\left(aG_i-h_i+d_i,\ bG_i-h_i\right)
=\left(aG_i,\ bG_i-1\right),
\tag{24}
\]
which are positive by (12).  The affine polynomial \(X-\beta\) has a
nonzero linear jet at every \(\alpha_i\), and the second endpoint is a
unit.  Thus the local terminal support is present at every repeated
root.

The parameter \(\beta\) is arbitrary.  In particular, the unique zero
of \(P_{n-1}=X-\beta\) can be placed away from every root of \(R\).
The affine Wronskian condition therefore supplies no missing divisor
relation between \(P_{n-1}\) and the common polynomial.

## 4. A concrete saturated example

Take
\[
a=2,\quad b=3,\quad
R=X^2(X-1)^3,\quad g=5,
\tag{25}
\]
and
\[
L=X(X-1)^2(X-2),\qquad \deg L=4=g-1.
\tag{26}
\]
The two local data sets are
\[
\begin{array}{c|ccccc}
\alpha&e&d&h&f&G\\ \hline
0&2&1&1&1&3\\
1&3&1&1&2&2
\end{array}
\tag{27}
\]
so \(aG>h\) at both roots.  Here \(n=10\), \(m=15\).  The pair
\[
\widetilde P=(R+\tau L)^2+\tau^9(X-\beta),
\qquad
\widetilde Q=(R+\tau L)^3+\tau^{14}
\tag{28}
\]
obeys every coefficient cap and has
\[
[\tau^{23}]\,\mathscr K(\widetilde P,\widetilde Q)=-1.
\tag{29}
\]
It has nonzero lower mixed coefficients, so (28) is deliberately not
presented as a Keller map.

## Consequence

There is no theorem of the desired form using only
\[
\sum e_i=g,\quad e_i=k_ih_i+f_i,\quad
G_i=h_ig-e_id_i,
\]
the first-layer degree sum, the reciprocal caps, and the affine
defect-one endpoint: those conditions admit (5)--(24), with every
root in the deep band.

The remaining promising target is narrower.  One must derive an
identity from the **intermediate homogeneous Keller coefficients**
which links the common first-face deformation \(D\) to the affine
endpoint.  A possible useful form would be a resultant or residue
that detects the uncancelled cross terms in (21).  Root counting by
itself cannot do so.

The symbolic identities and the concrete saturated example are
checked by
`verify_standard_system_repeated_root_global_deck_budget_countermodel.py`.
