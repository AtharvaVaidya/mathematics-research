# The corrected first arithmetic frontier and the connected \((9,6)\) reduction

Date: 26 July 2026

## Outcome

Let
\[
 [F,G]_{x,y}=\lambda\in\mathbf C^\times,\qquad
 m=\deg_yF\geq n=\deg_yG>0.
\]
Use the leading Jacobian equation, constant target reductions, the
partial-degree criterion, and the total-degree criterion after a high
source shear.  The first candidate for a minimal counterexample not
certified automorphic by those operations is
\[
 \boxed{(m,n)=(9,6)}.
\]
It necessarily has
\[
 m=ad,\quad n=bd,\quad (a,b,d)=(3,2,3),\qquad
 t=\gcd(d,\deg h)=3,
\]
where the leading coefficients are constant multiples of \(h^3,h^2\).
Thus the previously proposed \((8,6)\) frontier is not a frontier: its
\(t=2\) chart is removed because a high shear makes the gcd of the two
total degrees \(2p\), with \(p\) prime.

On the connected cubic cover \(H^3=h\), put \(z=Hy\).  The
\(\mu _3\)-character gives a simultaneous depressed slice.  A
triangular approximate-root lemma then gives the exact upper form
\[
 \boxed{
 f=(g^{3/2})_+ +j(g^{1/2})_+,
 }
\]
after a constant target shear and translation.  The four remaining
nonconstant bracket coefficients are exact derivatives of four
weighted first integrals \(I_{10},I_{11},I_{12},I_{13}\).  Deck
characters force
\[
 I_{10}=I_{11}=I_{13}=0,\qquad I_{12}=K\in\mathbf C,
\]
and the terminal equation is
\[
 dP'-Lq'=\frac{\lambda}{H}.
\]

The connected, noncube-\(h\) chart can in fact be excluded completely.
A centered change of the five remaining coefficient variables splits
the first-integral level set into two exact branches.  One has zero
Jacobian identically.  The other is excluded by a two-value pole
argument, except at one cuspidal level; at that level finite-map
integrality restores enough polynomial descent for a final valuation
contradiction.

This does **not** exclude all of \((9,6)\).  If \(h\) is a cube
(including the constant-\(h\) case), the cover is not connected and
seven additional character constants survive.  That chart is recorded
separately below and remains open.

The arithmetic input is taken directly from V. Moskowicz,
[*A variation on Magnus' theorem and its generalizations*,
Theorems 1.1, 1.2, 2.6, and 2.7](https://arxiv.org/abs/1810.08202v2).
The proof here does not use the false number-theoretic Lemma 2.3 in
that preprint: the special leading-coefficient relation makes the two
reduced pairs equal, and ordinary Dirichlet suffices for the single
common progression used below.

## 1. Complete arithmetic enumeration through the first survivor

Write the leading \(y\)-coefficients as \(f_m,g_n\).  The coefficient
of \(y^{m+n-1}\) in the Jacobian is
\[
 n f_m'g_n-m f_mg_n'=0.
\tag{1}
\]
Put
\[
 d=\gcd(m,n),\qquad m=ad,\qquad n=bd,\qquad \gcd(a,b)=1.
\tag{2}
\]
Unique factorization in \(\mathbf C[x]\), followed by rescaling the
two target coordinates, gives
\[
 f_m=h^a,\qquad g_n=h^b
\tag{3}
\]
for a nonzero \(h\in\mathbf C[x]\).  Let
\[
 s=\deg h,\qquad t=\gcd(d,s),
\tag{4}
\]
with \(\gcd(d,0)=d\).  Then
\[
\begin{aligned}
 A&=\gcd(m,\deg f_m)=\gcd(ad,as)=at,\\
 C&=\gcd(n,\deg g_n)=\gcd(bd,bs)=bt.
\end{aligned}
\tag{5}
\]

Choose \(L\) larger than every \(x\)-degree of every coefficient of
\(F,G\), and make the source change \(y\mapsto y+x^L\).  Its two total
degrees are
\[
\begin{aligned}
 \deg F_L&=as+adL=at\,p,\\
 \deg G_L&=bs+bdL=bt\,p,
\end{aligned}
\qquad
 p=\frac{s}{t}+\frac{d}{t}L.
\tag{6}
\]
When \(s>0\), the two integers \(s/t,d/t\) are coprime, so Dirichlet
allows \(L\) to be arbitrarily large with \(p\) prime.  When \(s=0\),
one has \(t=d\), \(p=L\), and one simply chooses \(L\) prime.
Consequently
\[
 \gcd(\deg F_L,\deg G_L)=tp.
\tag{7}
\]

Two valid consequences of the cited total-degree theorems now suffice:

1. If \(t=1\) or \(t=2\), (7) is \(p\) or \(2p\), so the Keller map is
   an automorphism.
2. If either \(at\) or \(bt\) lies in
   \[
      \{1,4\}\cup\{\text{primes}\},
   \tag{8}
   \]
   the corresponding total degree in (6) is respectively a prime,
   \(4p\), or a product of two primes.  The one-coordinate
   total-degree theorem again makes the map an automorphism.

This directly repairs the partial-degree use in this special chart
without the simultaneous-prime assertion of Moskowicz's Lemma 2.3.
In Moskowicz's notation, when \(s>0\),
\[
 (\widetilde u,\widetilde n)
 =(\widetilde v,\widetilde r)
 =\left(\frac{s}{t},\frac{d}{t}\right),
\tag{9}
\]
so this is precisely the equal-reduced-pair branch of Theorem 2.6.

There are two elementary reductions before enumeration.  If \(m=n\),
a constant linear target change cancels one leading coefficient and
lowers one \(y\)-degree.  Hence take \(m>n\).  If \(b=1\), then
\(g_n=h\), while \(f_m=h^a\); subtracting \(G^a\) from \(F\) cancels
the leading \(y^m\)-term.  Induction on the ordered degree pair removes
this power-shear case.  Therefore a minimal unresolved pair has
\[
 a>b\geq2,\qquad \gcd(a,b)=1,\qquad t\geq3,\qquad t\mid d.
\tag{10}
\]
The smallest possible values are
\[
 (a,b,t,d)=(3,2,3,3),
\]
and hence
\[
 (m,n)=(ad,bd)=(9,6).
\tag{11}
\]
Conversely, at (11) the partial invariants are
\((A,C)=(9,6)\), neither belongs to (8), and the high-shear total gcd
is \(3p\), outside the cited \(p\) and \(2p\) cases.  An exhaustive
integer enumeration through \(m=9\) is included in the verifier; its
unique unresolved tuple is
\[
 (m,n,d,a,b,t,A,C)=(9,6,3,3,2,3,9,6).
\tag{12}
\]
This proves the arithmetic assertion only; it does not assert that a
Keller pair of degree \((9,6)\) exists.

## 2. Connected cubic normalization and the character slice

Normalize the leading coefficients as
\[
 f_9=h^3,\qquad g_6=h^2.
\tag{13}
\]
Assume first that \(h\) is not a cube in \(\mathbf C(x)\).  Then
\[
 L=\mathbf C(x)(H),\qquad H^3=h
\tag{14}
\]
is a connected cyclic cubic extension.  With \(z=Hy\), the normalized
coordinates
\[
 f(x,z)=F(x,z/H),\qquad g(x,z)=G(x,z/H)
\]
are monic in \(z\), of degrees nine and six, and
\[
 [f,g]_{x,z}=\frac{\lambda}{H}.
\tag{15}
\]
For a primitive cube root \(\zeta\), the deck generator satisfies
\[
 \sigma(H)=\zeta H,\qquad \sigma(z)=\zeta z.
\tag{16}
\]

Translate \(z\) over \(L\) to kill the degree-five coefficient of
\(g\).  That coefficient has the same deck character as \(z\), so the
new variable \(w\) still satisfies \(\sigma(w)=\zeta w\).  We then
write
\[
 g=w^6+aw^4+bw^3+cw^2+dw+q.
\tag{17}
\]
The characters, equivalently the weights modulo three, are
\[
\begin{array}{c|ccccc}
 &a&b&c&d&q\\ \hline
 \operatorname{wt}&2&3&4&5&6\\
 \sigma&\zeta^2&1&\zeta&\zeta^2&1 .
\end{array}
\tag{18}
\]

Here is the theory-first integration of all upper equations.  For
\(0\leq k\leq9\), let
\[
 A_k=(g^{k/6})_+
\tag{19}
\]
be the polynomial part at \(w=\infty\).  Each \(A_k\) is monic of
degree \(k\), so there is a unique triangular expansion
\[
 f=A_9+\sum_{k=0}^8 c_k(x)A_k.
\tag{20}
\]
The full Laurent series \(g^{k/6}\) commutes with \(g\), while its
negative part begins in degree \(-1\).  Therefore
\[
 \deg_w[A_k,g]\leq4.
\tag{21}
\]
On the other hand,
\[
 [c_kA_k,g]=c_k'A_k g_w+c_k[A_k,g],
\]
whose first summand has leading term \(6c_k'w^{k+5}\).
Descending triangularly from \(k=8\) to \(k=0\), (15) forces every
\(c_k\) to be constant.

The distinguished sixth root of \(g\) has leading term \(w\), so
\(\sigma(A_k)=\zeta^kA_k\).  Since \(f\) is invariant and
\(c_k\in\mathbf C\), connectedness forces \(c_k=0\) unless
\(3\mid k\).  A target shear removes \(c_6g\), a target translation
removes \(c_0\), and \(c_3=j\in\mathbf C\) remains.  Thus
\[
 \boxed{f=(g^{3/2})_+ +j(g^{1/2})_+.}
\tag{22}
\]
This proves both depression of \(f\) and the upper approximate-root
form without solving a large coefficient system.

## 3. Explicit upper form

Expanding (22) gives
\[
\begin{aligned}
 f={}&w^9+\frac32aw^7+\frac32bw^6
 +\frac{3(a^2+4c)}8w^5+\frac{3(ab+2d)}4w^4\\
 &+\frac{-a^3+12ac+6b^2+16j+24q}{16}w^3
 -\frac{3(a^2b-4ad-4bc)}{16}w^2\\
 &+Lw+P,
\end{aligned}
\tag{23}
\]
where
\[
\begin{aligned}
 L={}&\frac{
 3a^4-24a^2c-24ab^2+64aj+96aq+96bd+48c^2
 }{128},\\
 P={}&\frac{
 3a^3b-6a^2d-12abc-2b^3+16bj+24bq+24cd
 }{32}.
\end{aligned}
\tag{24}
\]

Assign weights
\[
 \operatorname{wt}(a,b,c,d,q;j)=(2,3,4,5,6;6).
\tag{25}
\]
Every coefficient in (23)--(24) has the weight complementary to its
power of \(w\).

## 4. Four lower first integrals

Define the following weighted-homogeneous polynomials:
\[
\begin{aligned}
I_{10}={3\over128}\bigl(&3a^5-24a^3c-36a^2b^2+32a^2j+48a^2q\\
 &+96abd+48ac^2+48b^2c-128cj-192cq-96d^2\bigr),
\tag{26}\\
I_{11}={3\over128}\bigl(&15a^4b-24a^3d-72a^2bc-24ab^3
 +64abj+96abq\\
 &+96acd+48b^2d+48bc^2-128dj-192dq\bigr),
\tag{27}\\
I_{12}=-{1\over512}\bigl(&15a^6-132a^4c-288a^3b^2
 +128a^3j+192a^3q\\
 &+672a^2bd+336a^2c^2+768ab^2c-512acj-768acq\\
 &-384ad^2+72b^4-384b^2j-576b^2q-1152bcd\\
 &-192c^3+1536jq+1152q^2\bigr),
\tag{28}\\
I_{13}=-{1\over128}\bigl(&15a^5b-21a^4d-96a^3bc-48a^2b^3
 +64a^2bj+96a^2bq\\
 &+120a^2cd+120ab^2d+144abc^2-64adj-96adq\\
 &+48b^3c-128bcj-192bcq-96bd^2-144c^2d\bigr).
\tag{29}
\end{aligned}
\]

Let \(R_k=[w^k][f,g]_{x,w}\), after substituting (23).  Exact
differentiation gives the triangular identities
\[
\boxed{
\begin{aligned}
 R_4&=I_{10}',\\
 R_3&=I_{11}',\\
 R_2&=I_{12}'+\frac12aR_4,\\
 R_1&=I_{13}'+\frac13bR_4+\frac13aR_3.
\end{aligned}}
\tag{30}
\]
Thus the four nonterminal equations make the four \(I_r\) constant.
Their weights also give their deck characters:
\[
 \sigma(I_r)=\zeta^rI_r.
\tag{31}
\]
The constant field of the connected function field \(L\) is
\(\mathbf C\).  It follows that
\[
 \boxed{
 I_{10}=0,\qquad I_{11}=0,\qquad I_{12}=K,\qquad I_{13}=0
 }
\tag{32}
\]
for one \(K\in\mathbf C\).

The constant coefficient of the bracket is
\[
 \boxed{R_0=dP'-Lq'=\frac{\lambda}{H}.}
\tag{33}
\]
Equivalently, on the normalization of the one-dimensional coefficient
image, the differential
\[
 \Omega=d\,\mathrm dP-L\,\mathrm dq
\tag{34}
\]
pulls back to \(\lambda\,dx/H\).  Equations (17), (23)--(24),
(26)--(34), together with polynomial descent to the original
\(y\)-coefficients, are the exact connected \((9,6)\) endpoint.

## 5. Exact decomposition of the connected level set

The long invariants become triangular after the centered change
\[
 C=c-\frac{a^2}{4},\qquad
 D=d-\frac{ab}{2},\qquad
 Q=q-\frac{b^2}{4}.
\tag{35}
\]
Direct substitution gives
\[
\begin{aligned}
 I_{10}={3\over8}\bigl(
 3C^2a-12CQ-8Cj-6D^2\bigr),\\
 I_{11}={3\over8}\bigl(
 3C^2b+6CDa-12DQ-8Dj\bigr),\\
 I_{12}={1\over8}\bigl(
 3C^3-3C^2a^2+18CDb+12CQa+8Caj\\
 \hspace{31mm}{}+6D^2a-18Q^2-24Qj\bigr),\\
 I_{13}={1\over16}\bigl(
 18C^2D-9C^2ab-6CDa^2+24CQb+16Cbj\\
 \hspace{31mm}{}+12D^2b+12DQa+8Daj\bigr).
\end{aligned}
\tag{36}
\]
More importantly, there is the exact identity
\[
 \boxed{
 I_{13}=\frac98C^2D-\frac b3I_{10}-\frac a6I_{11}.
 }
\tag{37}
\]
On the connected levels (32), (37) gives \(C^2D=0\).  Since the
coefficient field is a field, there are exactly two cases.

If \(C=0\), then \(I_{10}=0\) gives \(D=0\), and
\[
 I_{12}=-\frac34Q(3Q+4j)=K.
\tag{38}
\]
Thus \(Q\) is constant.  With
\[
 \rho=w^3+\frac a2w+\frac b2
\]
the two normalized coordinates are
\[
 g=\rho^2+Q,\qquad
 f=\rho^3+\left(\frac32Q+j\right)\rho.
\tag{39}
\]
Their Jacobian is zero, contradicting (15).  Hence this branch is
impossible.

Now suppose \(C\ne0\).  Equation (37) gives \(D=0\); then
\(I_{11}=0\) gives \(b=0\), and \(I_{10}=0\) gives
\[
 a=\frac{4(3Q+2j)}{3C}.
\tag{40}
\]
The remaining invariant equation is the single cubic level
\[
 \boxed{
 C^3=R(Q):=6Q^2+8jQ+\frac83K.
 }
\tag{41}
\]
Since \(b=D=0\), one has \(d=0,q=Q,P=0\).  The coefficient \(L\)
in (24), reduced modulo (41), is
\[
 L=\frac{S(Q)}{24C},\qquad
 S(Q):=21R(Q)+32(j^2-K).
\tag{42}
\]
The terminal equation is therefore
\[
 -LQ'=\frac{\lambda}{H}.
\tag{43}
\]

## 6. Exclusion of the connected cubic-cover chart

### 6.1 The generic level \(K\ne j^2\)

The coefficients \(b\) and \(q\) are deck-invariant by (18).  Hence
\[
 Q=q-\frac{b^2}{4}
\]
is fixed by \(\operatorname{Gal}(L/\mathbf C(x))\), so
\(Q\in\mathbf C(x)\).  Thus the following is an identity in the base
rational-function field, not merely on the cubic cover.

Cubing (43) and using \(C^3=R(Q)\) gives the base-field identity
\[
 \boxed{
 h=-24^3\lambda^3
 \frac{R(Q)}{S(Q)^3Q'^3}.
 }
\tag{44}
\]
The quadratic \(S\) has discriminant
\[
 12096(j^2-K),
\]
so it has two distinct roots when \(K\ne j^2\).  Neither is a root of
\(R\), because at a common root (42) would give
\(0=32(j^2-K)\).

The terminal equation makes \(Q\) nonconstant.  Regard it as a
rational map \(\mathbf P^1_x\to\mathbf P^1_Q\).  At least one of the
two distinct finite roots \(\alpha\) of \(S\) has a finite preimage:
the single point \(x=\infty\) cannot be the only preimage of two
different target values.  If
\[
 \operatorname{ord}_{x_0}(Q-\alpha)=e>0,
\]
then \(S(Q)\) has order \(e\), \(Q'\) has order \(e-1\), and
\(R(Q)\) is a unit.  Formula (44) makes \(h\) have pole order
\(6e-3>0\) at \(x_0\), impossible for \(h\in\mathbf C[x]\).
This excludes \(K\ne j^2\).

### 6.2 The cuspidal level \(K=j^2\)

Now (41) becomes
\[
 C^3=6\left(Q+\frac{2j}{3}\right)^2.
\]
On the branch \(C\ne0\), put
\[
 v=\frac{Q+2j/3}{C}.
\]
Then
\[
 C=6v^2,\qquad Q=6v^3-\frac{2j}{3},\qquad
 a=4v,\qquad c=10v^2,\qquad b=d=0,
\tag{45}
\]
and the normalized pair is
\[
\begin{aligned}
 f={}&w^9+6vw^7+21v^2w^5+35v^3w^3+\frac{63}{2}v^4w,\\
 g={}&w^6+4vw^4+10v^2w^2+6v^3-\frac{2j}{3}.
\end{aligned}
\tag{46}
\]
An exact calculation gives
\[
 [f,g]_{v,w}=-567v^6.
\tag{47}
\]

One descent point requires care: the depressed coefficients need not
themselves be polynomials.  Set \(g_0=g+2j/3\).  The pair
\((f,g_0)\) is positive weighted-homogeneous for
\(\operatorname{wt}(v,w)=(2,1)\).  Its common zero is only the origin.
On the \(v=0\) axis this follows from
\((f,g_0)=(w^9,w^6)\), and on the \(w=0\) axis it follows from
\(g_0=6v^3\).  Away from the axes put \(T=w^2/v\).  A common nonzero zero
would make
\[
\begin{aligned}
 T^3+4T^2+10T+6&=0,\\
 T^4+6T^3+21T^2+35T+\frac{63}{2}&=0,
\end{aligned}
\]
but the resultant of these two polynomials is \(567/8\).
Thus \(f,g_0\) form a homogeneous system of parameters in the
positively graded ring \(\mathbf C[v,w]\).  The homogeneous-system-of-
parameters lemma makes \(\mathbf C[v,w]\) module-finite over
\(\mathbf C[f,g_0]\).  Consequently
\[
 \Phi=(f,g_0):\mathbf A^2_{v,w}\longrightarrow\mathbf A^2
\]
is finite, and \(v^3,vw\) are integral over
\(\mathbf C[f,g_0]\).

Under the substitution back to the original variables, \(f,g_0\)
are target transforms of the original polynomial coordinates, so
\(\mathbf C[f,g_0]\subset\mathbf C[x,y]\).  A monic equation over
\(\mathbf C[f,g_0]\) is also a monic equation over
\(\mathbf C[x,y]\), so \(v^3,vw\) are integral over
\(\mathbf C[x,y]\).  They are deck-invariant, and the fixed field of
the cubic Kummer action on \(L(y)\) is \(\mathbf C(x,y)\); hence they
belong to \(\operatorname{Frac}\mathbf C[x,y]\).  Normality of
\(\mathbf C[x,y]\) now gives
\[
 v^3,\ vw\in\mathbf C[x,y].
\tag{48}
\]
Write the depressed translation and the cusp parameter as
\[
 w=H(y+s),\qquad v=\frac{V}{H},
\qquad s,V\in\mathbf C(x).
\tag{49}
\]
Then \(vw=V(y+s)\in\mathbf C[x,y]\), so
\[
 V\in\mathbf C[x],\qquad Vs\in\mathbf C[x].
\]
Also \(v^3=V^3/h\) belongs to
\(\mathbf C[x,y]\cap\mathbf C(x)=\mathbf C[x]\), and hence
\[
 h\mid V^3.
\tag{50}
\]

Combining (15), (47), and \(v=V/H\) gives
\[
 \boxed{
 -189V^6(3hV'-Vh')=\lambda h^3.
 }
\tag{51}
\]
Let \(x_0\) be a root of \(h\), and write
\[
 r=\operatorname{ord}_{x_0}V,\qquad
 s_0=\operatorname{ord}_{x_0}h.
\]
Divisibility (50) gives \(s_0\leq3r\).  If \(s_0\ne3r\), the two sides
of (51) have orders
\[
 7r+s_0-1,\qquad 3s_0.
\]
Equality gives \(7r-1=2s_0\).  Together with
\(s_0\leq3r\), this forces \(r=1,s_0=3\), contrary to
\(s_0\ne3r\).  Thus \(s_0=3r\) at every root of \(h\).

A root of \(V\) outside the zero set of \(h\) would instead give
orders \(7r-1>0\) and \(0\) in (51), also impossible.  Therefore
\(h\) and \(V\) have the same support and
\[
 h=\gamma V^3
\]
for some \(\gamma\in\mathbf C^\times\).  But then
\(3hV'-Vh'=0\), contradicting (51).  The same argument covers
the special zero-character-constant subchart when \(h\) is constant,
but it does not cover the general constant-\(h\) system in Section 7.

We have proved:

> **Connected-chart theorem.**  No Keller pair of exact
> \(y\)-degrees \((9,6)\) occurs in the chart in which the common
> leading factor \(h\) is not a cube in \(\mathbf C(x)\).

## 7. The cube-\(h\) chart, including constant \(h\)

If \(h\) is a cube in \(\mathbf C(x)\), polynomial factorization over
\(\mathbf C\) gives \(h=r^3\) for some \(r\in\mathbf C[x]\), up to a
harmless constant cube.  This includes every nonzero constant \(h\).
Put \(z=ry\) and depress \(g\) over \(\mathbf C(x)\).  There is now no
nontrivial deck character.

The same triangular lemma gives the full upper form
\[
\boxed{
\begin{aligned}
 f={}&(g^{3/2})_+
 +\kappa _8(g^{4/3})_+
 +\kappa _7(g^{7/6})_+
 +\kappa _5(g^{5/6})_+\\
 &+\kappa _4(g^{2/3})_+
 +j(g^{1/2})_+
 +\kappa _2(g^{1/3})_+
 +\kappa _1(g^{1/6})_+ ,
\end{aligned}}
\tag{52}
\]
after removing the constant \(g\)-multiple and target translation.
All seven \(\kappa _8,\kappa _7,\kappa _5,\kappa _4,j,\kappa _2,
\kappa _1\) are arbitrary constants at the upper-equation level.
In particular, the residual \(w^8\)-coefficient \(\kappa _8\) is not
forced to vanish.

For example, with \(h=x^3,r=x\),
\[
 F=(xy)^9+(xy)^8,\qquad G=(xy)^6
\tag{53}
\]
descends polynomially and normalizes to \(f=z^9+z^8,g=z^6\).
With constant \(h=1\), the same example is \(F=y^9+y^8,G=y^6\).
These are not Keller pairs; they are exact counterchecks showing that
descent and the upper equations do not erase \(\kappa _8\).
The lower first integrals (26)--(32) apply only when the extra
character constants in (52) vanish.  The general cube-\(h\) lower
system remains a separate problem.

## 8. What remains

The connected cubic cover is closed.  The corrected frontier leaves
two theory-first tasks:

1. derive and decompose the full lower system in the cube-\(h\) chart
   (52), including constant \(h\);
2. determine whether polynomial descent in that chart forces a
   removable target power, or instead leaves a genuinely new
   coefficient curve.

No exclusion of the full \((9,6)\) pair, counterexample, or proof of
the plane Jacobian conjecture is claimed here.
