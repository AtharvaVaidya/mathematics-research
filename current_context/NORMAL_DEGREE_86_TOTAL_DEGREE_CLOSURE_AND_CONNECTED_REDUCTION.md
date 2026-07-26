# Total-degree closure and the connected \((8,6)\) reduction

Date: 26 July 2026

## Outcome

This note has two purposes.

First, it identifies the first pair of \(y\)-degrees which is not
removed by the one-coordinate partial-degree criterion in
Moskowicz, *A variation on Magnus' theorem and its generalizations*,
Theorem 2.7
([preprint](https://arxiv.org/abs/1810.08202)).
If
\[
 [F,G]_{x,y}\in\mathbf C^\times,\qquad
 (m,n)=(\deg_yF,\deg_yG),\qquad m\geq n,
\]
then every pair with \(m\leq7\) is already covered.  At \(m=8\), the
only gap in that one criterion is
\[
 \boxed{(m,n)=(8,6)}
\]
with \(\deg h\) even.  It is **not** a genuine Keller frontier:
Moskowicz's Theorem 2.6, or directly the classical \(2P\)
total-degree criterion after a high source shear, excludes it.

Second, on the connected quadratic cover \(H^2=h\), it reduces the
degree-\((8,6)\) coefficient system to four algebraic first-integral
levels plus one terminal ordinary differential equation.  Seven upper
equations give an explicit polynomial normal form.  The next four give
four exact weighted first integrals.  Thus the five remaining
coefficient functions lie in an explicitly defined weighted algebraic
level set.  Along their one-dimensional image, the constant-Jacobian
equation is the pullback of one rational differential.

The coefficient calculation is retained as an exact approximate-root
model for higher connected-cover systems.  It is not needed to exclude
\((8,6)\), and it is not presented as a new automorphy theorem.  There
is also a separate square-\(h\) chart in which the parity step used on
the connected cover is unavailable.

## 1. The narrow partial-degree gap and its total-degree closure

Let \(f_m,g_n\) be the leading \(y\)-coefficients.  The coefficient of
\(y^{m+n-1}\) in the Jacobian is
\[
 n f_m'g_n-m f_mg_n'=0.
\tag{1}
\]
Put
\[
 d=\gcd(m,n),\qquad m=ad,\qquad n=bd,\qquad \gcd(a,b)=1.
\tag{2}
\]
Unique factorization applied to (1) gives
\[
 f_m=\alpha h^a,\qquad g_n=\beta h^b
\tag{3}
\]
for \(h\in\mathbf C[x]\setminus\{0\}\) and
\(\alpha,\beta\in\mathbf C^\times\).

Let \(s=\deg h\) and \(t=\gcd(d,s)\).  The two partial-degree
invariants appearing after the high source shear in the repaired
Magnus argument are
\[
\begin{aligned}
 \gcd(m,\deg f_m)&=\gcd(ad,as)=a\,t,\\
 \gcd(n,\deg g_n)&=\gcd(bd,bs)=b\,t.
\end{aligned}
\tag{4}
\]
The prior criterion applies if either number in (4) is
\[
 1,\qquad 4,\qquad\text{or a prime}.
\tag{5}
\]

Equal degrees are removed first by a constant linear target change.
Assume \(m>n\).  For \(m\leq7\), a failure of (5) in both coordinates
is impossible.  Indeed:

- if \(t=1\), the first coprime pair \(a>b\) for which neither entry is
  in (5) occurs only above this range;
- if \(t\geq2\), then \(a\geq2\) gives \(d\leq3\).  For \(d=2,t=2\),
  the only potentially composite value below eight is \(a t=6\), but
  then \(bt\) is \(2\) or \(4\).  For \(d=3,t=3\), \(m\leq7\) forces
  \(a=2,b=1\), and \(bt=3\).

At \(m=8\), if \(d=4\), then \((a,b)=(2,1)\) and
\(bt\in\{1,2,4\}\).  If \(d=2\), then \(a=4\).  The chart \(t=1\) is
covered by the value \(at=4\), while \(t=2\) leaves precisely
\[
 b=3,\qquad (m,n)=(8,6),\qquad (at,bt)=(8,6).
\tag{6}
\]
Here \(t=2\) is exactly the condition that \(s=\deg h\) is even
(including \(s=0\)).

This enumeration only locates the first gap in Theorem 2.7.  The
broader prior results close it.  Choose a prime
\[
 p>M+\frac{s}{2},\qquad L=p-\frac{s}{2},
\tag{6a}
\]
where \(M\) exceeds every coefficient \(x\)-degree.  The source shear
\(y\mapsto y+x^L\) makes the two total degrees
\[
 \deg F_L=8p,\qquad \deg G_L=6p.
\tag{6b}
\]
Their greatest common divisor is \(2p\), so the classical \(2P\)
case quoted in Moskowicz's Theorem 1.1 makes the map an automorphism.
The Jung--van der Kulk degree-divisibility theorem then gives a
contradiction, since neither degree in (6b) divides the other.
This includes \(s=0\).

More generally, first remove equal degrees by a linear target change
and remove \(b=1\) by the power shear \(F\mapsto F-cG^a\).  Thus
\(a>b\ge2\).  For a high source shear,
\[
\deg F_L=atW,\qquad \deg G_L=btW,\qquad
W=\frac{s}{t}+\frac{d}{t}L.
\tag{6c}
\]
Dirichlet permits \(W=p\) prime.  If \(t=1\) or \(2\), the total-degree
greatest common divisor is \(p\) or \(2p\); if either \(at\) or \(bt\)
lies in \(\{1,4\}\cup\mathbb P\), one coordinate degree lies in
\(\mathbb P\), \(4\mathbb P\), or \(\mathbb P^2\).  The corresponding
classical criteria imply automorphy, again contradicting
nondivisibility.

These complete criteria exclude every pair with \(m\le8\).  At
\(m=9\), the first surviving arithmetic chart is
\[
\boxed{(m,n)=(9,6),\qquad d=t=3,\qquad(a,b)=(3,2).}
\tag{6d}
\]
That cubic-cover chart, not \((8,6)\), is the next active
coefficient problem.

## 2. The quadratic cover and the hidden square chart

For \((m,n)=(8,6)\), rescale the target coordinates so that
\[
 f_8=h^4,\qquad g_6=h^3.
\tag{7}
\]
Adjoin \(H\) with
\[
 H^2=h
\tag{8}
\]
and put \(z=Hy\).  Over \(L=\mathbf C(x)(H)\), the two coordinates are
monic of degrees eight and six in \(z\), and
\[
 [F,G]_{x,z}=\frac{\lambda}{H},
\qquad \lambda\in\mathbf C^\times.
\tag{9}
\]

Suppose first that \(h\) is not a square in \(\mathbf C(x)\).  Then
\(L/\mathbf C(x)\) is connected and its deck involution satisfies
\[
 \sigma(H)=-H,\qquad \sigma(z)=-z.
\tag{10}
\]
Translate \(z\) over \(L\) to kill the degree-five coefficient of the
degree-six coordinate.  The translation is anti-invariant, so the new
variable \(w\) still satisfies \(\sigma(w)=-w\).  The next Jacobian
equation says that the degree-seven coefficient of the degree-eight
coordinate is constant.  This \(x\)-dependent translation preserves
the bracket because \(dw\wedge dx=dz\wedge dx\).  The residual
coefficient is also anti-invariant.  Since the
constant field of the connected function field \(L\) is \(\mathbf C\),
that coefficient is zero.  Thus both coordinates are depressed:
\[
\begin{aligned}
 f&=w^8+A w^6+B w^5+Cw^4+Dw^3+Ew^2+L_1w+P,\\
 g&=w^6+a w^4+b w^3+cw^2+dw+q.
\end{aligned}
\tag{11}
\]
Here
\[
 a,c,q,A,C,E,P\in\mathbf C(x),\qquad
 b,d,B,D,L_1\in H\mathbf C(x).
\tag{12}
\]

The connectedness hypothesis is essential.  If \(h=r^2\) in
\(\mathbf C(x)\), one may put \(z=ry\), but there is no nontrivial deck
involution of the resulting base field.  After depressing \(g\), the
degree-seven coefficient of \(f\) is only forced to be an arbitrary
constant \(\kappa\); it is not forced to vanish.  For example,
\[
 F=(xy)^8+(xy)^7,\qquad G=(xy)^6,\qquad h=x^2
\tag{13}
\]
descends polynomially and has residual normalized coefficient
\(\kappa=1\).  This pair is not Keller, but it proves that descent and
the top equation alone do not justify the parity step.

Consequently, the square-\(h\) cases split into \(\kappa=0\), where the
two coordinates can both be depressed but further integration
constants in the odd coefficient slots need not vanish, and
\(\kappa\ne0\), where even the displayed depressed shape changes.
The formulas below therefore describe the connected nonsquare chart
(and only the special square subchart in which all of those extra
constants happen to vanish).  They are not asserted to exhaust either
square chart.

## 3. Seven integrated upper equations on the connected cover

In (11), the first equation gives
\[
 A-\frac43a\in\mathbf C.
\]
The constant target shear \(f\mapsto f-kg\) removes this constant.
The next six equations integrate successively.  There are two even
constants \(j,e\in\mathbf C\), and, after harmless target
translations, the result is
\[
\boxed{
\begin{aligned}
 A={}&\frac43a,\\
 B={}&\frac43b,\\
 C={}&\frac43c+\frac29a^2+j,\\
 D={}&\frac43d+\frac49ab,\\
 E={}&\frac43q-\frac4{81}a^3+\frac49ac
       +\frac23aj+\frac29b^2+e,\\
 L_1={}&-\frac4{27}a^2b+\frac49ad+\frac49bc+\frac23bj,\\
 P={}&\frac1{243}\bigl(
 5a^4-36a^2c-27a^2j-36ab^2+81ae+108aq\\
 &\hspace{35mm}+108bd+54c^2+162cj
 \bigr).
\end{aligned}}
\tag{14}
\]
No division by any of \(a,b,c,d,q\) occurs.  Thus (14) includes their
zero charts.

Assign weights
\[
 \operatorname{wt}(a,b,c,d,q;j,e)=(2,3,4,5,6;4,6).
\tag{15}
\]
Every expression in (14) is homogeneous for the coefficient it
defines.

There is a conceptual form of (14).  Expand fractional powers of \(g\)
as formal Laurent series at \(w=\infty\), with leading terms
\[
 g^{1/3}=w^2+O(1),\qquad g^{2/3}=w^4+O(w^2),\qquad
 g^{4/3}=w^8+O(w^6),
\]
and let \((\cdot)_+\) denote polynomial part.  Direct binomial
expansion gives the exact identity
\[
 \boxed{
 f=(g^{4/3})_+ +j(g^{2/3})_+ +e(g^{1/3})_+.
 }
\tag{15a}
\]
Thus the seven integrations are the finite approximate-root
calculation for the exponent pair \((4,3)\), now occurring inside the
even degree-\((8,6)\) system.  This also explains the weights and gives
a theory-first way to generate (14), rather than solving a large
undirected coefficient system.

## 4. Four exact first integrals

Define
\[
\begin{aligned}
 I_9={}&20a^3b-36a^2d-72abc-54abj-12b^3\\
      &\quad+81be+108bq+108cd+162dj,
\tag{16}\\[1mm]
 I_{10}={}&8a^5-60a^3c-36a^3j-90a^2b^2+81a^2e+108a^2q\\
      &\quad+216abd+108ac^2+162acj+108b^2c+81b^2j\\
      &\quad-243ce-324cq-162d^2-486jq,
\tag{17}\\[1mm]
 I_{11}={}&\frac1{81}\bigl(
 20a^4b-28a^3d-96a^2bc-54a^2bj-36ab^3\\
      &\quad+81abe+108abq+108acd+54adj+72b^2d\\
      &\quad+72bc^2+108bcj-162de-216dq
 \bigr),
\tag{18}\\[1mm]
 I_{12}={}&-\frac1{2187}\bigl(
 40a^6-360a^4c-162a^4j-720a^3b^2+324a^3e+432a^3q\\
      &\quad+1620a^2bd+972a^2c^2+972a^2cj
       +1944ab^2c+972ab^2j\\
      &\quad-1458ace-1944acq-972ad^2+162b^4
       -729b^2e-972b^2q\\
      &\quad-2916bcd-1458bdj-648c^3-1458c^2j
       +4374eq+2916q^2
 \bigr).
\tag{19}
\end{aligned}
\]
The subscripts are their weights.

After substituting (14), let \(R_k\) denote the coefficient of \(w^k\)
in \([f,g]_{x,w}\).  Exact differentiation gives
\[
\boxed{
\begin{aligned}
 R_4&=-\frac2{81}I_9',\\
 R_3&=\frac2{243}I_{10}',\\
 R_2&=I_{11}'-\frac{a}{81}I_9',\\
 R_1&=I_{12}'-\frac{2b}{243}I_9'
                    +\frac{2a}{729}I_{10}'.
\end{aligned}}
\tag{20}
\]
Thus the four nonterminal equations are equivalent to four first
integrals.

On the connected cover, \(I_9\) and \(I_{11}\) are anti-invariant,
while \(I_{10}\) and \(I_{12}\) are invariant.  Hence
\[
\boxed{
 I_9=0,\qquad I_{11}=0,\qquad
 I_{10}=K_{10},\qquad I_{12}=K_{12}
}
\tag{21}
\]
for constants \(K_{10},K_{12}\in\mathbf C\).

The five functions \((a,b,c,d,q)\) therefore take values in the
explicit weighted algebraic level set
\[
 \mathcal C_{j,e,K_{10},K_{12}}
 =
 \{I_9=0,\ I_{11}=0,\ I_{10}=K_{10},\
 I_{12}=K_{12}\}\subset\mathbf A^5.
\tag{22}
\]
The generic dimension is expected to be one, but no height statement
for every special choice of the four constants is proved here.
In particular, no assertion of irreducibility, equidimensionality, or
rationality is made.

## 5. The terminal differential

The constant coefficient is the only equation not yet used:
\[
 \boxed{-L_1q'+P'd=\frac{\lambda}{H}.}
\tag{23}
\]
Equivalently, if
\[
 \Omega=d\,\mathrm dP-L_1\,\mathrm dq
\tag{24}
\]
is restricted to the normalization of the one-dimensional coefficient
image (or of any curve component containing it), then the coefficient
map from the quadratic \(x\)-curve must satisfy
\[
 \phi^*\Omega=\frac{\lambda\,dx}{H}.
\tag{25}
\]

Before the total-degree closure above was applied, this isolated the
remaining equation in the connected chart.  No analysis of (25) is
needed to rule out a Keller pair of exact degree \((8,6)\).

The weights explain why the calculation remains a useful model for
the genuine \((9,6)\) cubic-cover frontier.
At a full weighted pole one has prospective orders proportional to
\[
 (2,3,4,5,6),
\]
while \(L_1,P,\Omega\) have weights \(7,8,13\), respectively.  The
same approximate-root organization, with three deck characters
instead of two, is used in the active cubic-cover calculation.

## 6. Two-channel interpretation

For comparison with the degree-\((4,3)\) normal form, put \(u=w^2\)
and write
\[
 f=P_0(u)+wP_1(u),\qquad
 g=Q_0(u)+wQ_1(u).
\tag{26}
\]
On the connected cover, \(P_0,Q_0\) are invariant and
\(P_1=HR,\ Q_1=HS\) with \(R,S\in\mathbf C(x)[u]\).  If
\(\delta=H'/H=h'/(2h)\) and
\(\mathcal L=1+2u\partial_u\), the vanishing odd channel is
\[
 2(P_{0,x}Q_{0,u}-P_{0,u}Q_{0,x})
 +h\bigl((R_x+\delta R)\mathcal LS
        -\mathcal LR(S_x+\delta S)\bigr)=0,
\tag{27}
\]
and the scalar even channel, after division by \(H\), is
\[
\begin{aligned}
 &P_{0,x}\mathcal LS-\mathcal LR\,Q_{0,x}
 +2u\bigl((R_x+\delta R)Q_{0,u}
          -P_{0,u}(S_x+\delta S)\bigr)\\
 &\hspace{45mm}=\frac{\lambda}{h}.
\end{aligned}
\tag{28}
\]
Equations (27)--(28) display (11) as the solved even
degree-\((4,3)\) core coupled to low-degree odd corrections.  The
first-integral calculation above is the coefficient-level
integration of that coupling.
