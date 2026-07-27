# The odd \(q=6\) local problem: a uniform subextremal theorem and the first \((15,6)\) nodal Hensel obstruction

Date: 25 July 2026

## Outcome

Let
\[
 p=3A,\qquad q=6,\qquad A\ge3\ \text{odd},
\tag{1}
\]
and use the full constant upper approximate-root polynomial described
in `Q6_ODD_FRONTIERS_UNIFORM_REDUCTION_AND_A_DEPENDENCE.md`.
At a coefficient pole of weighted scale \(\rho>0\), suppose that
\(A_5\) has positive pole order and
\[
 A_1,\ldots,A_4\in\mathbf C.
\tag{2}
\]

This note proves two uniform reductions.

1. If
   \[
   \operatorname {pole}(A_5)<2\rho,
   \tag{3}
   \]
   then the weighted leading pair is necessarily
   \[
   \boxed{F_0=R^A,\qquad G_0=R^2}
   \tag{4}
   \]
   for a monic cubic \(R\).  This follows from a
   polynomial-\(abc\) argument and requires no coprimality
   hypothesis.

2. Write the first transverse normal as
   \[
   G=R^2+\varepsilon E+\cdots,\qquad \deg E\le2,
   \tag{5}
   \]
   and put \(h=(A+1)/2\).  The first normal contribution of the top
   flow is the negative Laurent tail of
   \[
   \binom{A/2}{h}\frac{E^h}{R}.
   \tag{6}
   \]
   It vanishes exactly when
   \[
   \boxed{R\mid E^h\quad\Longleftrightarrow\quad
   \operatorname {rad}(R)\mid E.}
   \tag{7}
   \]
   Hence a nonzero silent normal is impossible when \(R\) is
   squarefree.  Every possible low-pole arc is forced into a nodal
   or triple-root cubic chart.

For \((p,q)=(15,6)\), the natural nodal scaling has apparent ratio
one.  It is not itself an invariant arc: three conserved Laurent
coefficients have nonconstant tails.  The first possible Hensel
repair has an exact cube-root congruence with three solutions, but
each solution creates a strictly earlier nonzero mixed bracket term.

The top-flow rational-support filtration below closes every direct
repair: a genuine support strictly between the leading normal and
the Hensel jet is obstructed, and supports at and after \(9/2\)
cannot cancel the order-twelve nodal tail.  Delayed
\(P\)-multiples are removed by exact moving-cubic square completion.

The physical grading leaves one all-character chain.  On the
nineteen-fold character cover, its successive equations say that a
quadratic \(Q(x)\) and then \(Q'(x)\) vanish.  The Hensel jet has
nonzero value at the double root, so the next coefficient is the
unavoidable nonzero term \(Q''V(1)^2\).  This closes the full nodal
chart, including the two core upper modes and every delayed
resonant character.

The nominal triple-root chart is not an infinity face in depressed
coordinates: it forces \(R=X^3\), so no lower coefficient attains
the positive pole scale.  The scale must restart.  Consequently the
corrected nodal filtration closes the positive-terminal-pole
\((15,6)\) sub-threshold local problem without enumerating smooth
stationary branches:
\[
 \boxed{\operatorname {pole}(A_5)\ge2\rho.}
\tag{7a}
\]

No exact one-pole formal countermodel is produced here.

## 1. Scaled bracket and the dangerous interval

After a finite local extension, let \(t\) be an honest uniformizer
and let the integral pole scale be \(m\).  Put
\[
 X=t^mw,\qquad
 \bar G=t^{6m}G(t,t^{-m}X),\qquad
 \bar F=t^{3Am}F(t,t^{-m}X).
\tag{8}
\]
The scaled bracket is
\[
\begin{aligned}
\mathcal B(\bar F,\bar G)
={}&t(\bar F_t\bar G_X-\bar F_X\bar G_t)\\
&-3Am\,\bar F\bar G_X+6m\,\bar F_X\bar G.
\end{aligned}
\tag{9}
\]
If \(A_5\) has pole order \(n\), the first scalar term in
\(\mathcal B\) has honest order
\[
 N=(3A+5)m-n.
\tag{10}
\]
Thus a violation \(n<2m\) lies in the narrow interval
\[
 (3A+3)m<N<(3A+5)m.
\tag{11}
\]

The upper constants have strictly smaller natural weights than the
top term.  At the weighted leading boundary only the top pair
matters.

## 2. Uniform polynomial-\(abc\) subextremality

Let \(s=G_0^{1/6}\) at infinity.  Under (3), the conserved levels and
the terminal level have no top-weight contribution.  Hence
\[
 F_0=s^{3A}+O(s^{-6}).
\tag{12}
\]
It follows that
\[
 \deg_X(F_0^2-G_0^A)\le3A-6.
\tag{13}
\]

Suppose the difference in (13) is nonzero.  Divide the three-term
equation
\[
 F_0^2-G_0^A=H
\tag{14}
\]
by \(D=\gcd(F_0^2,G_0^A)\), of degree \(d\).  Mason's theorem gives
\[
\begin{aligned}
6A-d
&\le \deg F_0+\deg G_0+\deg H-d-1\\
&\le 3A+6+(3A-6)-d-1\\
&=6A-d-1,
\end{aligned}
\tag{15}
\]
a contradiction.  Therefore
\[
 F_0^2=G_0^A.
\tag{16}
\]
Since \(\gcd(A,2)=1\) and both polynomials are monic, unique
factorization gives (4).

This argument is uniform in \(A\), survives arbitrary ramification,
and does not classify any stationary top branch.  In particular,
the three new \((15,6)\) branches found in the companion note are
automatically on the safe, non-subextremal side.

## 3. The first transverse normal

Put
\[
 A=2h-1,\qquad h=\frac{A+1}{2}.
\tag{17}
\]
After absorbing tangent changes of the canonical cubic \(R\), write
\[
 \bar G=R^2+\varepsilon t^\delta E+\cdots,
\qquad \deg E\le2.
\tag{18}
\]
The top approximate root has binomial expansion
\[
 \bar G^{A/2}
 =\sum_{j\ge0}\binom{A/2}{j}
 R^{A-2j}(\varepsilon t^\delta E)^j.
\tag{19}
\]
For \(0\le j<h\), the exponent \(A-2j\) is a positive odd
integer.  These terms are polynomials and belong to the exact
polynomial part.  The first possibly nonpolynomial term is (6).

The negative Laurent tail of \(E^h/R\) vanishes if and only if its
Euclidean remainder modulo \(R\) vanishes.  This proves
\[
 R\mid E^h.
\tag{20}
\]
In the UFD \(\mathbf C[X]\), (20) is equivalent to every distinct
factor of \(R\) dividing \(E\), which is (7).

Since \(\deg E\le2\), there are only three possibilities:

1. \(R\) squarefree: then \(E=0\), so the pole scale must be
   restarted at a later normal;
2. \(R=H^2K\), with \(H,K\) distinct linear factors:
   \[
   E=cHK;
   \tag{21}
   \]
3. \(R=H^3\):
   \[
   E=H(\alpha H+\beta).
   \tag{22}
   \]

Thus all sub-threshold work is confined to the nodal and triple
charts.

The triple entry in this formal list cannot actually occur at a
positive pole scale.  Since \(G_0=R^2\) is depressed, its
\(X^5\)-coefficient is zero.  If
\[
 R=(X-\xi)^3,
\tag{22a}
\]
then
\[
 [X^5]R^2=2[X^2]R=-6\xi,
\tag{22b}
\]
so \(\xi=0\) and
\[
 R=X^3,\qquad G_0=X^6.
\tag{22c}
\]
But the pole scale is defined as the maximum normalized pole of the
lower sextic coefficients.  At least one lower coefficient of the
scaled leading sextic must therefore be nonzero.  Equation (25)
contradicts that normalization.  The scale must be restarted, and
the preceding leading-pair argument applies again.

Thus the only genuine singular infinity face is nodal.  This
observation is uniform in odd \(A\).

## 4. The apparent ratio-one nodal germ at \((15,6)\)

Take a parameter \(T\to\infty\), a nonzero constant \(e\), and put
\[
\begin{aligned}
R_T&=(w-T^4)^2(w+2T^4)
=w^3-3T^8w+2T^{12},\\
E_T&=eT^{-3}(w-T^4)(w+2T^4)\\
&=e(T^{-3}w^2+Tw-2T^5),\\
g_T&=R_T^2+E_T,\qquad
f_T=(g_T^{5/2})_+.
\end{aligned}
\tag{23}
\]
The depressed sextic coefficients have weighted pole scale
\[
 \rho=4.
\tag{24}
\]
An exact Laurent calculation gives
\[
\begin{aligned}
A_1&=\frac{5e^4}{128T^{12}},&
A_2&=\frac{5e^4}{32T^8},&
A_3&=\frac{15e^4}{64T^4},\\
A_4&=\frac{5e^4}{48},&
A_5&=-\frac{e^4(25T^{19}+2e)}{384T^{15}}.
\end{aligned}
\tag{25}
\]
Thus
\[
 \operatorname {pole}(A_5)=4,\qquad
 \frac{\operatorname {pole}(A_5)}\rho=1.
\tag{26}
\]
But (23) is not an invariant curve: \(A_1,A_2,A_3\) vary with
\(T\).  Formula (25) is an exact approximate germ, not a local
countermodel.

In the honest parameter \(t=T^{-1}\), the scaling (8) has \(m=4\)
and
\[
\bar G=P^2+et^{19}S,
\quad
P=(X-1)^2(X+2),
\quad
S=(X-1)(X+2).
\tag{27}
\]
The apparent scalar would occur at order
\[
(15+5)4-4=76=4\cdot19.
\tag{28}
\]

## 5. First Hensel repair

To cancel the fourth-order nodal residual in (27) by a generic
normal, its cubic self-interaction must occur at the same order.
Let \(y=t^m\) be the pole-scale parameter.  The leading normal has
\(y\)-support \(19/4\).  Put \(z=y^{19/12}\), so the leading and
Hensel supports become three and four:
\[
 \bar G=P^2+z^3S+z^4V+\cdots.
\tag{29}
\]
At order twelve, the two relevant binomial terms are
\[
 \binom{5/2}{3}\frac{V^3}{P}
 +\binom{5/2}{4}\frac{S^4}{P^3}
 =\frac5{128P^3}(8P^2V^3-S^4).
\tag{30}
\]
Put
\[
 H=X-1,\qquad K=X+2,\qquad
 P=H^2K,\qquad S=HK.
\tag{31}
\]
Polynomiality of (30) is equivalent to the exact Hensel congruence
\[
 \boxed{8V^3\equiv K^2\pmod P.}
\tag{32}
\]
It has three solutions in \(\mathbf C[X]/(P)\).  One representative
is
\[
 V=c(X-10)(X+2),\qquad
 c^3=-\frac1{17496};
\tag{33}
\]
the other two multiply \(c\) by the nontrivial cube roots of unity.

The repair fails earlier than order twelve if no further rational
jets are admitted.  Let
\[
 \bar F=(\bar G^{5/2})_+
\tag{34}
\]
and use the correctly regraded scaled bracket
\[
\mathcal B
=\frac{19}{12}z(\bar F_z\bar G_X-\bar F_X\bar G_z)
-15\bar F\bar G_X+6\bar F_X\bar G.
\tag{35}
\]
For every solution (33), the order-eleven coefficient is
\[
 \boxed{
 [z^{11}]\mathcal B
 =-\frac{10935}{32}c^2
 (X-1)^2(X+2)(17X+5)\ne0.
 }
\tag{36}
\]
It comes from the mixed \(SV^2/P\) term, before the intended
order-twelve self-cancellation.  Equation (36) is nonconstant in
\(X\), so it cannot be the terminal scalar.

The next three subsections prove that (36) survives every top-flow
rational support character and every delayed tangent character.
Subsection 5.5 identifies the remaining core upper-character gap.

### 5.1 Rational supports below four

Pass to a finite cover whenever necessary, so displayed support
orders are integral there.  Let \(U\), of degree at most two, be the
least genuine extra normal at rational order \(r\), with
\[
 3<r<4.
\tag{37}
\]
The first possible nonpolynomial convolution is the mixed cubic
\(SU^2/P\), at order \(3+2r\).  Exact application of (35) gives
\[
\boxed{
 [z^{3+2r}]\mathcal B
 =-\frac{15}{32}H^2K\,U(1)^2
 \bigl((38r-135)X+(38r-147)\bigr).
}
\tag{38}
\]
The two coefficients of the final linear factor cannot vanish
simultaneously.  Thus (38) forces \(H\mid U\).

Write \(U=HL\).  The first remaining nonpolynomial self-convolution,
\(U^3/P\), occurs at order \(3r\), and its exact bracket is
\[
\boxed{
 [z^{3r}]\mathcal B
 =\frac{45}{32}H^3L(-2)^3
 \bigl((19r-64)X+(19r-56)\bigr).
}
\tag{39}
\]
Again the linear factor is never zero.  Hence \(K\mid L\), so
\[
 U\in\mathbf C\,HK=\mathbf C\,S.
\tag{40}
\]
Such a jet is only a later coefficient of the already present
silent normal \(S\).  All its cubic convolutions remain polynomial,
and its first quartic convolution with the leading \(S\) occurs
strictly after order twelve.  It cannot affect either (36) or the
order-twelve tail.

Taking the least nonresonant support and repeating (38)--(40)
classifies an arbitrary finite Puiseux denominator.  Therefore no
genuine support in \((3,4)\) can start an indirect chain.

### 5.2 The order-four Hensel jet

At \(r=4\), polynomiality at order twelve is precisely the Hensel
congruence (32).  Its three solutions are (33).  For each one, (36)
is the order-eleven forcing.

If one tries to kill (36) by requiring \(H\mid V\), then (32)
becomes impossible already modulo \(H\), because
\[
 8V^3\equiv0\not\equiv K^2\pmod H.
\tag{41}
\]
Thus no top-flow normal at order four can remove both the mixed and
the self obstruction.

### 5.3 Supports above four

If \(4<r<9/2\), the first mixed term \(SU^2/P\) occurs at
\(3+2r<12\).  Formula (38), which depends only on the relevant
associated-graded character, again forces \(H\mid U\).  Such a
character cannot change the already fixed order-twelve base tail.

At the only possible collision \(r=9/2\), the mixed cubic and the
base quartic both have order twelve.  After multiplication by
\(P^3\), their combined rational numerator is
\[
 \frac5{128}H^4K^3\bigl(24HU^2-K\bigr).
\tag{42}
\]
Polynomiality would require
\[
 H^2\mid 24HU^2-K,
\tag{43}
\]
which is impossible modulo \(H\).  A support \(r>9/2\) arrives
after the nonzero base order-twelve coefficient
\[
 \boxed{
 [z^{12}]\mathcal B=\frac{15}{64}HK^2(3X-1).
 }
\tag{44}
\]
Consequently no rational support above four repairs the nodal arc.

### 5.4 Delayed \(P\)-multiples

At every order, split an arbitrary sextic jet uniquely as
\[
 W=B+PQ,\qquad \deg B,\deg Q<3.
\tag{45}
\]
The tangent part is removed exactly, not discarded: replacing the
moving canonical cubic by
\[
 P(z)\longmapsto P(z)+\frac12z^rQ
\tag{46}
\]
absorbs \(z^rPQ\) into \(P(z)^2\), while the quadratic descendant
\(\frac14z^{2r}Q^2\) is retained in the new normal \(B\).  Iterating
this square completion gives a unique moving-cubic gauge in which
every normal has degree below three.  Thus (38)--(44) already
include all effects of delayed \(P\)-multiples; none is silently
dropped.

Equivalently, the tangent character is zero in the associated
graded normal quotient.  Its forced descendants merely change the
representatives \(U,V,\ldots\), and the exact bracket (35) is
unchanged.

### 5.5 Correct physical grading of the upper constants

For an upper mode \(k\), put
\[
 H_k=(P^{k/3})_+.
\tag{47}
\]
Its first \(z\)-order and leading bracket character are
\[
\begin{aligned}
 d_k&=\frac{12(15-k)}{19},\\
 \mathscr U_k
 &=2P\bigl(3P H_k'-kP'H_k\bigr).
\end{aligned}
\tag{48}
\]
For nodal \(P\), this vanishes only for the core modes
\(k=9,3\), now at orders \(72/19\) and \(144/19\).  The noncore
modes occur at
\[
\begin{array}{c|cccccccccc}
k&14&13&11&10&8&7&5&4&2&1\\
\hline
\frac{19}{12}d_k&1&2&4&5&7&8&10&11&13&14 .
\end{array}
\tag{49}
\]
On the \(\tau=z^{1/19}\) cover, the ten noncore first characters
occur at orders
\[
 12,24,48,60,84,96,120,132,156,168,
\]
all strictly before the first top-flow Laurent character in the
core/Hensel chain, which occurs at order \(201\).  Hence (48)
successively forces every noncore upper constant to vanish in this
ratio-one chain.

The two core modes cannot be discarded.  Write
\[
 a=\kappa_9,\qquad b=\kappa_3,\qquad
 r=\frac{72}{19},
\tag{50}
\]
and allow a normal jet \(z^rU\).  At the common order
\[
 3+2r=\frac{201}{19},
\tag{51}
\]
three Laurent tails collide:
\[
 \frac{15}{16}\frac{SU^2}{P},\qquad
 \frac{3a}{4}\frac{SU}{P},\qquad
 \frac b2\frac S P.
\tag{52}
\]
Their common \(H^{-1}\) coefficient vanishes exactly when
\[
 \boxed{15U(1)^2+12aU(1)+8b=0.}
\tag{53}
\]
Thus the first \(k=3\) tail need not force \(b=0\); it can be
canceled by an order-\(72/19\) normal and the \(k=9\) descendant.
Equation (53) is the first live indirect-chain equation.  It also
closes after two further associated-graded coefficients.

Put \(\tau=z^{1/19}\).  The relevant integer character exponents are
\[
\begin{array}{c|ccccc}
\text{character}&S&\kappa_9,\ U&V&\kappa_3&
\text{mixed obstruction}\\
\hline
\tau\text{-order}&57&72&76&144&209.
\end{array}
\tag{54}
\]
Use the moving-cubic gauge of Subsection 5.4, and let \(B_n\), of
degree below three, be the normal at \(\tau^n\).

If \(57<n<72\) and \(B_n(1)\ne0\), the top mixed tail
\(SB_n^2/P\) occurs at \(57+2n\), strictly before any core
descendant.  Hence \(H\mid B_n\).  Its cubic self-tail then occurs
at \(3n\), again before a core descendant, and forces
\(K\mid B_n/H\).  Thus
\[
 B_n\in\mathbf C S\qquad(57<n<72).
\tag{55}
\]
These are precisely the delayed resonant coefficients of the
leading \(S\)-amplitude.

Let
\[
 x=U(1),\qquad
 Q(T)=\frac{15}{16}T^2+\frac{3a}{4}T+\frac b2.
\tag{56}
\]
Then (53) is \(Q(x)=0\), at order \(201\).  If
\(72<n<76\), the first \(H\)-tail of a jet with
\(B_n(1)\ne0\) is \(Q'(x)B_n(1)\), at order \(129+n\).
If \(Q'(x)=0\), its next coefficient is
\((15/16)B_n(1)^2\), at order \(57+2n<209\).  Therefore every such
jet is divisible by \(H\) and cannot alter the double-root
calculation.

At order \(205=57+72+76\), the Hensel jet gives
\[
 Q'(x)V(1)=0.
\tag{57}
\]
Congruence (32) reduced modulo \(H\) gives
\[
 8V(1)^3=K(1)^2=9,
\tag{58}
\]
so \(V(1)\ne0\), and (57) forces \(Q'(x)=0\).

Finally, at order \(209=57+2\cdot76\), the \(H^{-1}\) tail is
\[
 \frac{15}{16}\frac{V(1)^2}{H}.
\tag{59}
\]
No later normal enters linearly because \(Q'(x)=0\).  Every earlier
resonant \(S\)-multiple multiplies a coefficient of \(Q\) already
zero, and (55) rules out an independent \(K\)-pole collision.
Applying the bracket operator at order \(209/19\) gives
\[
\boxed{
 [\tau^{209}]\mathcal B
 =-\frac{15}{32}V(1)^2P(17X+5)\ne0.
}
\tag{60}
\]
For the representative (33), \(V(1)=-27c\), and (60) is exactly
(36).  Thus (36) is invariant in the full physical associated
graded, not merely in the top-flow regrading.

### 5.6 Every sub-threshold terminal order

The preceding ratio-one character chain is the generic collision,
but the local estimate requires every terminal order.  Normalize
\(\rho=1\), and suppose for contradiction that
\[
 n=\operatorname {pole}(A_5)<2,\qquad
 N=20-n\in(18,20)
\tag{61}
\]
is the first scalar bracket order.  Let \(s>0\) be the first normal
support in the nodal chart, so the leading normal is \(y^sS\).
The noncore upper modes occur at their fixed physical orders
\(15-k<15\).  Their leading characters have the stronger exact
factorization
\[
 \mathscr U_k=C_kH^3K,\qquad C_k\ne0
 \quad
 (k=14,13,11,10,8,7,5,4,2,1).
\tag{61a}
\]
If such a character occurs before every Laurent tail, it forces its
upper constant to vanish.  If it collides with a Laurent character,
the following root filtration separates the two contributions.

At physical order \(M\), the bracket images of leading principal
parts \(C/H\) and \(D/K\) are respectively
\[
\begin{aligned}
 \mathcal B_M(C/H)
 &=6C\,H^2K\bigl((M-16)X+(M-17)\bigr),\\
 \mathcal B_M(D/K)
 &=6D\,H^3\bigl((M-16)X+(M-14)\bigr).
\end{aligned}
\tag{61b}
\]
The first image has exact \(H\)-order two for \(M<33/2\), and the
second has nonzero value after division by \(H^3\) at \(K=0\) for
\(M<18\).  In either range it cannot be canceled by (61a).
Thus a collision does not invalidate the successive elimination of
the noncore upper constants.

If \(s<9/2\), the base quartic tail occurs at \(4s<18<N\).
Its first possible repair is a normal at \(4s/3<6\).  The top-flow
rational filtration of Subsections 5.1--5.4 applies before either
core mode can contribute and produces an \(H^{-1}\) mixed tail at
\[
 \frac{11s}{3}<4s<N.
\tag{62}
\]
Here \(11s/3<33/2\), so (61b) shows that this term survives every
possible collision with a noncore upper character.  It forces the
repair to be \(H\)-divisible.  Its ensuing \(K^{-1}\) self-tail has
order \(4s<18\); the second line of (61b) forces \(K\)-divisibility.
The repair is therefore only an \(S\)-multiple and cannot repair the
base quartic.  This contradicts the definition of \(N\).  The same
two-root argument, applied to the least intervening support, removes
every support strictly between \(s\) and \(4s/3\).

At the boundary \(s=9/2\), the \(k=9\) mode and the Hensel normal
both have support six.  Write
\[
 V=v_0+v_1X+v_2X^2,\qquad
 a=\kappa_9,\qquad b=\kappa_3.
\tag{63}
\]
Use \(z=y^{3/2}\), so the relevant orders are eleven and twelve.
The order-eleven bracket is
\[
 -\frac3{16}H^3K
 \bigl(12aV(1)+8b+15V(1)^2\bigr).
\tag{64}
\]
After imposing its vanishing, the order-twelve bracket has the form
\[
 -\frac3{32}H^2K(\mathcal AX+\mathcal C),
\tag{65}
\]
where
\[
\begin{aligned}
\mathcal A
 &=(v_1-v_2)^2(48a+120v_0+240v_2)-5,\\
\mathcal C&=-\mathcal A-15.
\end{aligned}
\tag{66}
\]
Thus \(\mathcal A=\mathcal C=0\) is impossible.  This excludes the
only collision where the top Hensel jet and a core upper mode arrive
simultaneously.  Any support strictly between \(9/2\) and \(6\) is
first forced to be an \(H\)-multiple by the first line of (61b), and
then an \(S\)-multiple by the second line; hence no omitted
intermediate character changes (64)--(66).

Finally suppose \(s>9/2\).  A nonresonant normal with support below
six first produces its top \(H^{-1}\) square before a core
descendant, and is therefore forced to be \(H\)-divisible; its
separate \(K\)-tail then makes it a resonant \(S\)-multiple.  At
support six, let \(x\) be the value at \(H=0\) of the combined
normal, taking \(x=0\) if no such normal occurs.  The first core
coefficient is the same quadratic
\[
 Q(x)=\frac{15}{16}x^2+\frac{3\kappa_9}{4}x
      +\frac{\kappa_3}{2}.
\tag{67}
\]
If its order \(s+12\) is at or before \(N\), it must vanish; if it
is after \(N\), it cannot supply the terminal scalar.

For every later first nonresonant value \(W(1)\), the next
associated-graded \(H\)-coefficient is either
\[
 Q'(x)W(1)
\quad\text{or, after }Q'(x)=0,\quad
 \frac{15}{16}W(1)^2.
\tag{68}
\]
Every earlier resonant \(S\)-multiple only multiplies a coefficient
of \(Q\) already zero.  The bracket image of a nonzero
\(C/H\)-tail at physical order \(M\) is
\[
 \boxed{
 6C\,H^2K\bigl((M-16)X+(M-17)\bigr),
 }
\tag{69}
\]
which is nonconstant for every \(M\).  Hence if one of (68) occurs
at or before \(N\), it contradicts the zero/scalar requirement; if
both occur after \(N\), there is no source for a scalar at \(N\).
The top quartic and every attempted Hensel repair are instances of
this same square alternative.  Separate \(K\)-pole characters are
forced resonant before they can meet (68), exactly as in (55).

The three cases prove (7a) for every rational support and after
arbitrary finite ramification.

## 6. Structural \(p=15\) pivot

The local \((15,6)\) theorem is now proved without enumerating the
algebraic stationary branches:

1. the polynomial-\(abc\) lemma removes every sub-threshold
   non-composite leading form;
2. the radical-divisibility lemma removes every squarefree cubic
   normal;
3. the full nodal chart is excluded by the physical all-character
   filtration (47)--(69);
4. the triple chart is removed by the depressed scale-restart lemma
   (22a)--(22c).

The local estimate is therefore available for:

* the split pure-power chart via the uniform line theorem;
* constant-\(r\) coefficient curves; and
* places on the connected noncube cubic normalization.

The exact calculations, including (38), (39), (44), (53), and
(57)--(60), (64)--(66), and (69),
are checked by
`verify_q6_odd_local_subextremal_and_156_nodal_hensel_audit.py`.
