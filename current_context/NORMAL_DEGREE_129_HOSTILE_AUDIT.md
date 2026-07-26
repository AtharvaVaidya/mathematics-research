# Hostile audit of the local \((12,9)\) pole calculation

Date: 26 July 2026

> **Integer-graded scope only.**  The repaired recurrence below closes
> the integer orders \(17,18,19\), but it does not prove the local
> \(7/2\) theorem after ramification.  The honest \(\rho=2\)
> half-order resonance and its later obstruction are audited
> separately in
> `NORMAL_DEGREE_129_HALF_ORDER_HOSTILE_AUDIT.md`.

## Verdict

The order-\(19\) conclusion in
`NORMAL_DEGREE_129_LOCAL_POLE_THRESHOLD.md` survives, but the
calculation presently written there is incomplete.  If an
order-\(9\) split is followed by an order-\(10\) split, their
quadratic cross-term also occurs at order \(19\).  After including
that term, the complete coefficient has a simple first-order form
and still cannot be a nonzero constant.

The sentence in Section 3 invoking the zero-Jacobian
common-component theorem "jet by jet" is not, by itself, a valid
argument.  The exact theorem gives a constant-coefficient common
right component when the Jacobian vanishes identically.  Finite
order vanishing need not give even a first-order common-component
lift.

There is, however, a direct repair which does not require a lifting
theorem.  Keeping every jet \(S_7,\ldots,S_{13}\) gives one exact
coefficient recurrence.  That recurrence excludes a realizable
nonzero scalar at each of the only dangerous orders \(17,18,19\).
Consequently the two gaps targeted by this audit can be closed by
replacing Sections 3--4 with the all-jet calculation in Sections
5--7 below.

## 1. What the exact common-component theorem does give

Let \(K\) be a characteristic-zero differential field with
algebraically closed constant field \(C\), and let \(x\) be
differentially independent over \(K\).  For
\[
 F,G\in K[x],\qquad
 J(F,G)=F_tG_x-F_xG_t,
\]
suppose \(J(F,G)=0\) identically.  Then \(F\) and \(G\) satisfy an
algebraic relation with coefficients in \(C\).

One direct proof begins with the irreducible relation
\(R(F,G)=0\) over \(K\).  Differentiation in \(x\) and \(t\), together
with \(J(F,G)=0\), shows that the coefficientwise derivative
\(R^\delta(F,G)\) vanishes.  Minimality gives
\(R^\delta=aR\).  After normalizing one coefficient of \(R\) to one,
\(R^\delta=0\), so \(R\in C[Y,Z]\).

The polynomial common-component theorem now writes
\[
 F=u(H),\qquad G=v(H).
\]
If
\[
 \deg_x F=4d,\qquad \deg_xG=3d
\]
and the common component has maximal degree \(d\), then
\(\deg u=4,\deg v=3\).  Since \(3\) and \(4\) are coprime, the
parametrization \(T\mapsto(u(T),v(T))\) is proper.  Two proper
polynomial parametrizations of the same constant curve differ by
an affine change of \(T\).  Consequently, after making \(H\) monic
and depressed, \(u,v\in C[T]\).  In the normalization relevant here
this gives
\[
 G=H^3+cH,\qquad
 F=H^4+\left(\frac43c+j\right)H^2+kH
\]
up to constant target shear and translation.

This is an **exact formal lemma**.  It justifies (25) if the entire
background is already known to have zero Jacobian as a formal
series, or if every finite jet has first been proved to lift to such
an exact formal composite pair.

## 2. Why the theorem cannot simply be applied jet by jet

Put
\[
 F=U^4+4tU,\qquad G=U^3+3t.
\]
Then
\[
 J(F,G)=-12t.
\]
Thus the first-order perturbation has zero linearized Jacobian: the
constant term of \(J\) vanishes.  Nevertheless it is not the
first-order variation of a common polynomial right component.
Indeed, a variation \(H=U+tq(U)\) would have to satisfy
\[
 4U^3q(U)=4U,\qquad 3U^2q(U)=3,
\]
which would require the nonpolynomial \(q(U)=U^{-2}\).

This is the standard singular-tangent phenomenon when
\(\gcd((U^4)',(U^3)')\ne1\).  The obstruction appears one order
later.  Therefore finite bracket vanishing alone does not imply the
jetwise reduction asserted in Section 3.

The normal-form argument may still establish the needed lifting,
because its residual equations are stronger than linearized
Jacobian vanishing.  But that implication must be stated and proved:
one should inductively separate genuine right-component variations
from singular tangent directions and show that every latter
direction is one of the split normals treated in Sections 2 and 4.

## 3. Exact classification of the \(\eta=9\) equation

Assume \(C=2c+3j=0\), and let the first split at order \(9\) be
\[
 G_9=S,\qquad \deg S<6.
\]
Put
\[
 H=\left(\frac{S^2}{P^2}\right)_+,\qquad
 R_2=S^2-HP^2=\operatorname{rem}_{P^2}(S^2).
\]
Including the quadratic approximate-root term
\[
 F_{18}=\frac29H
\]
and the \(k\)-term \(F_9=kP\), the complete order-\(18\)
coefficient is
\[
 \boxed{\mathcal B_{18}
   =-P\,\frac{d}{dX}\left(2R_2+3kS\right).}
\tag{1}
\]
This proves the factor \(P\) claimed in (33), and it gives the full
kernel:
\[
 \boxed{
 \mathcal B_{18}=0
 \iff
 S^2+\frac32kS-\lambda\equiv0\pmod{P^2}
 \quad\text{for some }\lambda\in C.}
\tag{2}
\]

For squarefree \(P\), (2) has many nonconstant solutions.  In the
Chinese-remainder algebra
\[
 C[X]/(P^2)\cong\prod_{P(a)=0} C[X]/((X-a)^2),
\]
the class of \(S\) may independently take either root of the
quadratic \(Y^2+\frac32kY-\lambda\) at each doubled root of \(P\),
with zero first derivative.  For example,
\[
 P=X^3-X,\qquad
 S=X^4-2X^2+1,\qquad
 k=-\frac23
\]
satisfy
\[
 S^2-S\equiv0\pmod{P^2}
\]
and hence \(\mathcal B_{18}=0\).  Thus the exceptional
\(\eta=9\) kernel is substantially larger than a target
translation.

## 4. The missing order-\(19\) cross-term

Allow a following order-\(10\) split
\[
 G_{10}=T,\qquad \deg T<6.
\]
The polynomial part of \(G^{4/3}\) contains the cross-term
\[
 F_{19}=\frac49K,\qquad
 K=\left(\frac{ST}{P^2}\right)_+.
\]
Let
\[
 R_{ST}=ST-KP^2=\operatorname{rem}_{P^2}(ST),
\qquad
 W=4R_{ST}+3kT.
\]
There are four contributions at order \(19\):
\[
\begin{array}{c|c}
\text{\(F\)-order}&\text{\(G\)-order}\\ \hline
19&0\\
9&10\\
10&9\\
9\text{ (the \(kP\) term)}&10.
\end{array}
\]
Their exact sum is
\[
 \boxed{
 \mathcal B_{19}
 =-\frac13\left(3P W'+P'W\right).}
\tag{3}
\]
The possible order-\(13\) linear split makes no contribution here:
its order-\(19\) \(c,j\)-operator is proportional to
\(C=2c+3j\).

If \(W\ne0\) has degree \(m<6\), then, because \(P\) is monic cubic,
\[
 \deg(3PW'+P'W)=m+2
\]
and its leading coefficient is \(3(m+1)\operatorname{lc}(W)\).
It therefore cannot be constant.  If \(W=0\), (3) is zero.  Hence
\[
 \boxed{\mathcal B_{19}\text{ is constant only when it is zero}.}
\tag{4}
\]

This repairs the dangerous-order conclusion, including all
quadratic \(9+10\) interactions.  It does **not** imply that there is
no order-\(10\) correction: nonzero \(T\) can in principle solve
\(W=0\).  What it proves, and what the pole estimate needs at this
order, is that no nonzero constant bracket can first occur at
order \(19\).

## 5. The all-jet recurrence

The common-component reduction is unnecessary through the
dangerous range.  Retain all corrections
\[
 G=P^3+cz^6P+\Delta,\qquad
 \Delta=\sum_{r\geq7}z^rS_r,\qquad \deg S_r<6,
\tag{5}
\]
and divide
\[
 S_r=PQ_r+B_r,\qquad \deg Q_r,\deg B_r\leq2.
\tag{6}
\]
Put
\[
 C=2c+3j.
\]
For \(14\leq N\leq19\), define the ordered convolution
\[
 A_N=\sum_{\substack{i+j=N\\i,j\geq7}}S_iS_j,
\qquad
 H_N=\left(\frac{A_N}{P^2}\right)_+,
\qquad
 R_N=A_N-H_NP^2.
\tag{7}
\]
Thus \(\deg R_N<6\).  Set \(R_{13}=0\), and set
\[
 W_N=2R_N+3kS_{N-9},
\tag{8}
\]
where an unavailable \(S_r\) is zero.

Through order \(19\), the polynomial part of \(F\) is
\[
\begin{aligned}
F={}&P^4+\left(\frac43c+j\right)z^6P^2+kz^9P\\
&+\frac43P\sum_{r\geq7}z^rS_r\\
&+\left(\frac49c+\frac23j\right)
   \sum_{r\geq7}z^{r+6}Q_r\\
&+\frac29\sum_{N=14}^{19}z^NH_N+O(z^{20}),
\end{aligned}
\tag{9}
\]
apart from irrelevant constant target terms.

Direct substitution in the scaled bracket gives, for
\(13\leq N\leq19\),
\[
\boxed{
\begin{aligned}
\mathcal B_N={}&
-\frac23CP\left((N-15)B_{N-6}P'+3PB_{N-6}'\right)\\
&-PW_N'+\frac{18-N}{3}P'W_N\\
&+\mathbf1_{N=19}\frac{2cC}{9}
  \left(Q_7P'+3PQ_7'\right).
\end{aligned}}
\tag{10}
\]
This formula includes simultaneously:

* the \(c,j\) operator on the new remainder \(B_{N-6}\);
* every quadratic cross-term \(S_iS_j\);
* the \(k\)-operator on \(S_{N-9}\).
* at \(N=19\), the delayed pairing of the order-\(13\)
  \(Q_7\)-correction in \(F\) with \(cz^6P\) in \(G\).

It therefore avoids any assumption that a silent finite jet lifts
to an exact common component.

## 6. Orders \(17\) and \(18\)

First suppose \(C=0\).  If a scalar first occurs at order \(17\),
the preceding equations at orders \(14\) and \(16\) vanish.  From
(10),
\[
\mathcal B_{14}=0
\quad\Longrightarrow\quad
W_{14}^3=\gamma P^4,
\qquad
\mathcal B_{16}=0
\quad\Longrightarrow\quad
W_{16}^3=\delta P^2.
\tag{11}
\]
Unless \(P=L^3\), the regular-scale restart, unique factorization
forces \(W_{14}=W_{16}=0\).  Hence
\[
P^2\mid S_7^2,\qquad P\mid S_7.
\tag{12}
\]

The complete order-\(17\) operator is
\[
\mathcal B_{17}=\frac13(P'W_{17}-3PW_{17}').
\tag{13}
\]
For
\[
P=X^3+AX+B,\qquad \deg W_{17}<6,
\]
coefficient comparison shows that a nonzero constant is possible
in (13) only in the apparent exceptional case
\[
A=0,\qquad W_{17}=\alpha X,\qquad
\mathcal B_{17}=-\alpha B.
\tag{14}
\]
Here \(B\ne0\), so \(P=X^3+B\) is squarefree.  Reducing the
\(W_{16}=0\) equation modulo \(P\), and using \(P\mid S_7\), gives
\[
P\mid S_8.
\tag{15}
\]
But
\[
R_{17}=\operatorname{rem}_{P^2}
       (2S_7S_{10}+2S_8S_9),
\]
so (12), (15), and (8) imply \(P\mid W_{17}\).  A cubic
\(X^3+B\) cannot divide \(\alpha X\).  Thus \(\alpha=0\), and the
exception (14) is not realizable.

Now suppose \(C\ne0\).  The equations at orders \(13\) and \(14\)
give
\[
3PB_7'-2P'B_7=0,\qquad
3PB_8'-P'B_8=0
\tag{16}
\]
after the preceding remainder is inserted.  A nonzero solution of
the first equation would give \(B_7^3=\gamma P^2\), and a nonzero
solution of the second would give \(B_8^3=\delta P\).  Either makes
\(P\) a cube.  Off the regular restart,
\[
B_7=B_8=0,\qquad P\mid S_7,\quad P\mid S_8.
\tag{17}
\]
It follows again that \(P\mid W_{17}\).  Both terms in (10) are then
divisible by \(P\), so \(\mathcal B_{17}\) cannot be a nonzero
constant.

At order \(18\), formula (10) is
\[
\mathcal B_{18}
=-\frac23CP\left(3B_{12}P'+3PB_{12}'\right)-PW_{18}'.
\tag{18}
\]
It is divisible by \(P\) for both \(C=0\) and \(C\ne0\), and hence
cannot be a nonzero constant.

## 7. Order \(19\)

For \(C=0\), formula (10) is exactly
\[
\mathcal B_{19}
=-\frac13(3PW_{19}'+P'W_{19}).
\tag{19}
\]
As proved in Section 4, this is constant only when both
\(W_{19}\) and the constant vanish.

It remains to handle \(C\ne0\) without a composite-jet assumption.
Equations (16)--(17) and the order-\(15\) equation give
\[
S_7=PQ_7,\qquad S_8=PQ_8,\qquad
S_9=PQ_9+b
\tag{20}
\]
for a constant \(b\).  Put
\[
d=4b+3k.
\]
At order \(16\), formula (10) factors as
\[
\mathcal B_{16}
=-\frac P3\left(3PY'+P'Y\right),
\qquad
Y=2CB_{10}+dQ_7.
\tag{21}
\]
Since \(\deg Y\leq2\), its vanishing forces
\[
B_{10}=-\frac d{2C}Q_7.
\tag{22}
\]

The ordered convolution at order \(19\) is
\[
A_{19}=2S_7S_{12}+2S_8S_{11}+2S_9S_{10}.
\]
Using (20), its remainder has the form
\[
R_{19}=PE+2bB_{10}
\]
with \(\deg E<3\).  Consequently
\[
W_{19}=PV+D_0,\qquad
D_0=dB_{10},\qquad \deg V,\deg D_0\leq2.
\tag{23}
\]
The delayed term in the last line of (10) combines with the
\(D_0\)-part of the preceding line:
\[
-PD_0'-\frac13P'D_0
+\frac{2cC}{9}(Q_7P'+3PQ_7')
=-PD'-\frac13P'D,
\]
where
\[
D=D_0-\frac{2cC}{3}Q_7.
\tag{23a}
\]

Suppose \(\mathcal B_{19}=\lambda\) is constant.  Reduction modulo
\(P\) gives
\[
P'D+3\lambda=PM
\tag{24}
\]
for a polynomial \(M\) of degree at most one.  Put
\[
Z=2CB_{13}+V.
\]
Substitution of (23)--(24) into (10) gives the exact identity
\[
\mathcal B_{19}-\lambda
=-\frac P3\left(
3PZ'+4P'Z+3D'+M
\right).
\tag{25}
\]
The right side of
\[
3PZ'+4P'Z=-(3D'+M)
\tag{26}
\]
has degree at most one.  If \(Z\ne0\) has degree \(m\leq2\), the
left side has degree \(m+2\) and leading coefficient
\(3(m+4)\operatorname{lc}(Z)\).  Hence \(Z=0\) and
\(3D'+M=0\).  Combining this with (24) yields
\[
3PD'+P'D=-3\lambda.
\tag{27}
\]
For nonzero \(D\) of degree at most two, the left side has degree at
least two.  Thus \(D=0\) and \(\lambda=0\).

No realizable nonzero scalar occurs at order \(19\).

## 8. Required revision

The local note should:

1. replace its current \(\eta=9\) and \(\eta=10\) discussion by
   (1)--(4), rather than treating the two orders separately;
2. weaken "the next new order is at least twenty-one" to the proved
   assertion that the complete order-\(19\) coefficient is not a
   nonzero constant;
3. remove the jetwise common-component claim and use the all-jet
   recurrence (10), with the order-by-order exclusions in Sections
   6--7.

With these replacements, the common-component and dangerous-order
gaps targeted by this audit are closed through order \(19\).
