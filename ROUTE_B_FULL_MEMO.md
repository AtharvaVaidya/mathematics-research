# Full reduced \((72,108)\) system

Date: 2026-07-24

> **25 July update.**  The later Wronskian calculation
> `route_bd_ab_delta1_35_wronskian.py` eliminates the final a/b
> \((3,5)\) boundary cell exactly over \(\mathbf Q\), so all five
> primitive cells are now excluded without a large modular lift.  The
> two generic case-c charts are independently empty at deficit seven in
> `route_bd_case_c_n3_generic_charts.py`; together with the two earlier
> charts this gives a small exhaustive proof of modular
> weighted-projective emptiness.  These are cleaner replacements for the
> large lower-fiber certificates, not an all-degree proof.

> **Audit correction (24 July 2026).**  The later claim below that the
> \(h^4\mid D_5\) middle descent is exhaustive in all five \(h\)-adic
> charts is not currently established.  In
> `route_bd_case_c_middle_divisibility_r2.py`, the displayed \(q_{10}\)
> forcing divides by \(r_4\), although the chart assumes only \(r_2\ne0\);
> the \(r_3\) continuation imports or assumes that value without a separate
> \(r_3\)-chart proof.  The corresponding \(r_2,r_3\) constant descents
> inherit the gap.  Read those sections as localized partial results until
> the \(r_4=0\) subcharts are supplied.  This correction does not affect
> the independent full modular/Singular elimination in Sections 1--5, nor
> the global \(c_{11}=0\) consequence used for the non-cusp contact bound.

## Result

Both GGHV branches in the bounded \((72,108)\) reduction have no point over
\(\mathbf C\): the 25+47 a/b coefficient variety and the 61+125 case-c
coefficient variety, in each case with every required Newton vertex.  This
is not a forced-edge or sampled-\(P\) statement.

The proof has three exact parts.  The outer differential equation defines
degree-21 three-point covers with passport
\[
(2^{10},1),\qquad(3^7),\qquad(17,1^4).
\]
An exact Murnaghan--Nakayama calculation gives Hurwitz number five.  At
\(p=32003\), the normalized outer coefficient algebra is reduced of length
five, and the complete lower fiber over each of its two rational and one
cubic factors has only the affine origin.  Finally, prime-to-\(p\) tame
specialization identifies the characteristic-zero and characteristic-\(p\)
outer covers, while properness of the weighted projectivization of the
original lower equations prevents a nonzero lower solution from disappearing
under specialization.  Section 5 gives the bridge carefully.

The case-c diagonal equation is exactly the same Hurwitz equation.  Its
\(u_7=1\) normalization has 35 geometric points.  A complete radial
recursion expresses all 165 nonouter, noncentral coefficients in seven
parameters of weights \((1,1,2,2,3,3,4)\).  Modulo 32003, exact Gröbner
bases over both rational factors and the cubic factor have quotient dimension
328 and contain \(X_0^{32},\ldots,X_6^{32}\).  Hence every case-c special
weighted-projective fiber is empty, and the same tame-specialization and
properness argument eliminates case c in characteristic zero.

This closes the bounded \((72,108)\) reduction only.  It does **not** prove
the two-dimensional Jacobian conjecture: no all-degree reduction to this
bounded case is asserted here.

## 1. Exact five-block form

Put
\[
z=xy,\qquad w=xy^2.
\]
Then \(x=z^2/w\), \(y=w/z\), and
\[
[z,w]_{x,y}=w.
\]
Every a/b-supported pair, after normalizing the coefficients of \(x\) and
\(x^2y\) to one, has the unique form
\[
\begin{aligned}
P&=\frac{z^2}{w}+a_0(w)+z a_1(w)+z^2a_2(w),\\
Q&=\frac{z^3}{w}+b_0(w)+z b_1(w)+z^2b_2(w)+z^3b_3(w),
\end{aligned}
\]
where
\[
\deg a_r\le 8-r,\qquad \deg b_r\le12-r.
\]
The two constants are bracket-invisible and may be chosen nonzero afterward.
The four nontrivial required vertices are
\[
[w^6]a_2,\ [w^8]a_0,\ [w^9]b_3,\ [w^{12}]b_0\ne0.
\]

Writing \(A=a_0+za_1+z^2a_2\) and
\(B=b_0+zb_1+z^2b_2+z^3b_3\), the equation
\([P,Q]_{x,y}=x^2\) is
\[
2zwB_w+z^2B_z-z^3A_z-3z^2wA_w+w^2[A,B]_{z,w}=0.
\]
Its five \(z\)-coefficients are:
\[
\begin{aligned}
0={}&a_1b_0'-a_0'b_1,\\
0={}&w^2(2a_2b_0'+a_1b_1'-a_1'b_1-2a_0'b_2)+2wb_0',\\
0={}&w^2(2a_2b_1'+a_1b_2'-2a_1'b_2-a_2'b_1-3a_0'b_3)
 {}+b_1+2wb_1'-3wa_0',\\
0={}&w^2(2a_2b_2'+a_1b_3'-3a_1'b_3-2a_2'b_2)
 {}+2b_2+2wb_2'-a_1-3wa_1',\\
0={}&w^2(2a_2b_3'-3a_2'b_3)
 {}+3b_3+2wb_3'-2a_2-3wa_2'.
\end{aligned}
\]

The verifier checks the coordinate map term-by-term: 25 \(P\)-monomials,
47 \(Q\)-monomials, 92 output rows, and all 975 nonzero bracket terms.

## 2. The outer variety and its Hurwitz count

Set
\[
U=1+wa_2,\qquad V=1+wb_3.
\]
The last block becomes
\[
UV+2wUV'-3wU'V=1,\qquad \deg U=7,\quad\deg V=10. \tag{1}
\]
Write \(U=\sum_{i=0}^7u_iw^i\) and
\(V=\sum_{j=0}^{10}v_jw^j\), with \(u_0=v_0=1\).
For \(1\le k\le10\), the coefficient equation
\[
\sum_{i+j=k}(1+2j-3i)u_iv_j=0
\]
solves \(v_k\) uniquely because \(1+2k\ne0\) in characteristic zero and
modulo 32003.  Degrees 11 through 16 leave six compatibility equations in
\(u_1,\ldots,u_7\); degree 17 is identically zero.

The required vertex is \(u_7\ne0\).  Modulo 32003, exact saturated Gröbner
calculations give:

* the \(u_1=0,\ u_7\ne0\) ideal is the unit ideal;
* the symmetry \(w\mapsto\lambda w\) therefore puts every special-fiber
  solution in the chart \(u_1=1\);
* the normalized outer algebra has vector-space dimension five;
* its reduced lexicographic basis begins with
  \[
  h(s)=s^5+9413s^4+8734s^3-3563s^2+7508s-3664
  \]
  and linear formulas for \(u_2,\ldots,u_7\);
* it factors as
  \[
  h=(s+5164)(s+15382)
  (s^3-11133s^2-11294s-6180).
  \]

The verifier checks
\(\gcd(h,h')=1\), \(u_7\) is a unit, and \(v_{10}\) is a unit in this
quotient.  Thus the modular outer algebra is reduced and consists of two
prime-field points plus one irreducible cubic point, i.e. exactly five
geometric points with both required outer vertices nonzero.

There is an independent characteristic-zero count.  Put
\[
R(w)=\frac{wV(w)^2}{U(w)^3}.
\]
Equation (1) gives
\[
R'(w)=\frac{V(w)}{U(w)^4}.
\]
The same equation makes \(U,V\) coprime and squarefree.  The ten roots of
\(V\) are double zeros of \(R\), the seven roots of \(U\) are triple poles,
and Riemann--Hurwitz forces the third fiber to have partition
\((17,1^4)\).  The Frobenius character formula, evaluated exactly by the
Murnaghan--Nakayama rule, gives
\[
\sum_{\lambda\vdash21}
\frac{\chi^\lambda(2^{10},1)\chi^\lambda(3^7)
\chi^\lambda(17,1^4)}{\dim\lambda}
=\frac{31104}{19019}
\]
and weighted Hurwitz count
\[
\frac{21!}{z_{(2^{10},1)}z_{(3^7)}z_{(17,1^4)}}
\frac{31104}{19019}=5.
\]
Every triple is transitive: a disconnected component outside the unique
17-cycle would lie among the four fixed sheets and would make a 3-cycle equal
an involution.  Automorphisms are trivial because the distinguished simple
zero and 17-fold point are fixed, and the normalization \(R(w)=w+O(w^2)\)
rules out a nontrivial scaling.  Hence there are exactly five normalized
complex outer maps.

More generally, if
\[
UV+\alpha wUV'-\beta wU'V=1,\qquad
\deg U=p,\quad\deg V=q,\quad \beta p-\alpha q=1,
\]
then
\[
R=\frac{wV^\alpha}{U^\beta},\qquad
R'=\frac{V^{\alpha-1}}{U^{\beta+1}}.
\]
Writing \(d=\beta p=\alpha q+1\), Riemann--Hurwitz gives the passport
\[
(\alpha^q,1),\qquad(\beta^p),\qquad(p+q,1^{\,d-p-q}).
\]
Thus every leading-edge equation of this form is a finite Hurwitz problem.

## 3. All lower coefficients, not a slice

Over each of the three field factors, the fourth block is a linear system in
the 19 coefficients of \((a_1,b_2)\).  It has rank 17, so write its complete
kernel as
\[
(a_1,b_2)=L\,e_1+M\,e_2.
\]
The third block is then linear in the 20 nonconstant coefficients of
\((a_0,b_1)\).  It has rank 18, its quadratic source is always consistent,
and its full solution is parametrized by \(N_0,N_1\).
The second block is a rank-12 system for the 12 nonconstant \(b_0\)
coefficients.  Its five consistency equations, together with the 18
coefficients of the first block, generate an ideal in
\((L,M,N_0,N_1)\).

For both rational factors and the cubic factor, the reduced 12-element
Gröbner basis contains, successively,
\[
N_1^2,\qquad N_0^2,\qquad
M^3+\text{terms in }(N_0,N_1),\qquad
L^3+\text{terms in }(M,N_0,N_1).
\]
Its geometric zero set is therefore only
\[
L=M=N_0=N_1=0.
\]
The verifier makes this projective statement explicit by reducing
\[
L^{12},\quad M^{12},\quad N_0^2,\quad N_1^2
\]
to zero modulo each of the three exact Gröbner bases.  Hence every lower
projective coordinate is nilpotent and the associated weighted Proj is
empty, not merely empty at sampled field values.
At this point every nonconstant coefficient of \(a_0\) and \(b_0\) is zero.
In particular,
\[
[w^8]a_0=[w^{12}]b_0=0,
\]
contradicting the two opposite required vertices.

## 4. Why this covers the algebraic closure

The cubic factor is handled inside
\[
\mathbf F_{32003}[t]/
(t^3-11133t^2-11294t-6180),
\]
not by testing its prime-field values.  Hence the three conjugate points are
checked simultaneously.  Together with the two split points and the saturated
outer Gröbner basis, this covers every point over
\(\overline{\mathbf F}_{32003}\).

## 5. Characteristic-zero bridge

Let \(S=\operatorname{Spec}\mathbf Z_{(32003)}\).  Consider the
automorphism-free Hurwitz functor of degree-21 covers of the constant marked
curve
\[
(\mathbf P^1_S;0,1,\infty)
\]
with the three partitions in Section 2.  The Galois-closure monodromy group
is a subgroup of \(S_{21}\).  Since \(32003>21\), its order is prime to
32003, and the inertia orders \(2,3,17\) are tame.  Grothendieck's
prime-to-\(p\) tame specialization theorem (SGA 1, Exposé XIII, §2.10)
identifies the corresponding finite covers of the geometric generic and
special fibers of the constant marked curve.  Equivalently here, the five
transitive permutation triples persist unchanged.  Rigidity and trivial
automorphisms therefore give a finite étale Hurwitz scheme of degree five
over \(S\).

The exact modular computation in Section 2 already supplies five reduced
points, all with \(u_1,u_7,v_{10}\ne0\), and proves that the saturated
\(u_1=0\) locus is empty.  Thus the \(u_1\ne0\) open is the whole local
Hurwitz scheme.  Its scaling is a unit over \(S\), so the integral chart
\(u_1=1\) used by the coefficient calculation covers all five generic and
special outer maps.

For the lower equations it is best not to globalize the sequential row
solves.  Give the original nonconstant coefficient blocks the weights
\[
\operatorname{wt}(a_1,b_2)=1,\qquad
\operatorname{wt}(a_0,b_1)=2,\qquad
\operatorname{wt}(b_0)=3.
\]
The remaining four bracket rows are homogeneous of weights \(1,2,3,4\).
They define a closed subscheme \(\mathcal X\) of the corresponding weighted
projective bundle over the finite étale outer scheme.  Weighted Proj is
proper over \(S\).

If a characteristic-zero lower solution with the required vertices existed,
the Nullstellensatz would give one over a finite number-field extension.
After choosing a place above 32003 and making a finite valued-field
extension, its outer Hurwitz point and its nonzero weighted-projective lower
point would extend to the valuation ring.  Properness would produce a point
of \(\mathcal X_{\overline{\mathbf F}_{32003}}\).  Section 3 proves that this
special fiber is empty: every lower projective coordinate is nilpotent over
each of the five outer points.  This contradiction eliminates the full a/b
branch over characteristic zero.  No rational outer Gröbner basis and no
global choice of the sequential lower pivot minors is required.

## 6. Reproduction

Exact Hurwitz count:

```sh
.venv/bin/python route_bd_ab_hurwitz_count.py
```

Fast exact special-fiber certificate (about 25 seconds on the reference
machine):

```sh
.venv/bin/python route_bd_fbar_obstruction.py --run-singular
```

It prints:

```text
OUTER U1=0 SATURATED
Gbad[1]=1
OUTER CHART VDIM
5
OUTER U7 UNIT
Gu7[1]=1
OUTER V10 UNIT
Gv10[1]=1
OUTER ELIMINANT GCD
1
...
LOWER r1 ranks 17,18,12
LOWER r2 ranks 17,18,12
LOWER cubic ranks 17,18,12
LOWER ... PROJECTIVE NILPOTENCE
0
0
0
0
RESULT: FULL a/b VARIETY IS EMPTY OVER FBAR_32003
```

An optional independent modular reconstruction of the rational triangular
outer algebra is intentionally separate because it is much slower:

```sh
.venv/bin/python route_bd_ab_outer_lift.py
```

It lifts 61 large-prime lexicographic bases by CRT, checks three unused
primes, and substitutes the reconstructed triangular basis into every outer
coefficient equation.  This is corroboration; the characteristic-zero bridge
above does not depend on it.

Independent prime-field enumeration and fixed-\(P\) certificates:

```sh
.venv/bin/python route_bd_modular_branch_search.py --prime 5
.venv/bin/python route_bd_modular_branch_search.py --prime 7
```

## 7. The case-c branch

The case-c supports contain 61 and 125 monomials.  In the grading
\(z=xy\), they have
\[
P=x+\sum_{d=0}^8y^dp_d(z),\qquad
Q=x^2y+\sum_{e=0}^{12}y^eq_e(z),
\]
and the bracket becomes 21 univariate identities
\[
\sum_{d+e=k}\left(e\,p_d'q_e-d\,p_dq_e'\right)
=\delta_{k,-2}z^2.
\]

The global diagonal exactness locus already has a finite description, and
it is not a new outer moduli problem.  For
\[
C(q)=q^7+c_6q^6+\cdots+c_0,\qquad \deg R\le10,
\]
the diagonal genus-three differential is exact exactly when
\[
2CR'-3C'R=2q^{16}. \tag{2}
\]
Set
\[
w=q^{-1},\qquad C=q^7U(w),\qquad R=-2q^{10}V(w).
\]
Direct differentiation gives
\[
C'=q^6(7U-wU'),\qquad R'=-2q^9(10V-wV'),
\]
so (2) is precisely
\[
UV+2wUV'-3wU'V=1.
\]
Moreover
\[
u_i=c_{7-i},\qquad v_j=-\frac12[q^{10-j}]R.
\]
Thus the diagonal locus has the same five-orbit Hurwitz quotient as the a/b
outer equation.  The normalization \(c_0=u_7=1\) is a weight-seven slice.
Because the scaling action is free, it contains \(5\cdot7=35\) geometric
points.  Algebraically, if \(A\) is the five-dimensional \(u_1=1\) outer
algebra and \(s=u_7^{-1}\), then this slice is
\[
B=A[\lambda]/(\lambda^7-s),\qquad
u_i^{(c)}=\lambda^iu_i,\quad v_j^{(c)}=\lambda^jv_j.
\]
This is the exact finite coefficient base for the transverse elimination.

In the same \(z,w\) coordinates,
write
\[
P=\sum_i z^iA_i(w),\qquad Q=\sum_jz^jB_j(w),
\qquad A_2=U/w,\quad B_3=V/w.
\]
Give the nonouter layers the radial-deficit weights
\[
\operatorname{wt}(A_i)=2-i,\qquad
\operatorname{wt}(B_j)=3-j.
\]
Every term in the \(z^k\) bracket row then has weight \(4-k\).  Exact rank
calculation over each of the two rational and one cubic modular outer
factors leaves, after removing the two additive constants, only seven
meaningful kernel parameters, of weights
\[
(1,1,2,2,3,3,4).
\]
The exact descending recursion covers all 165 nonouter, noncentral
coefficients.  Its 15 linear blocks, for output \(z\)-degrees \(3\) through
\(-11\), have only those seven kernel parameters; every later unknown block
is uniquely determined.  Their cokernels give 79 weighted-homogeneous
consistency equations.

Singular computes, over each rational factor and over the cubic field factor,
\[
\dim_K K[X_0,\ldots,X_6]/I=328,
\]
and reduces
\[
X_0^{32},X_1^{32},\ldots,X_6^{32}
\]
to zero.  Here \(K=\mathbf F_{32003}\) for the two rational points and
\(K=\mathbf F_{32003^3}\) for the irreducible cubic factor.  Consequently
the radical of every consistency ideal is
\((X_0,\ldots,X_6)\), so its weighted Proj is empty.  The cubic calculation
handles all three conjugate Hurwitz points at once.

The complete tail is not needed even scheme-theoretically for the radical
claim.  The first 19 consistency equations, of weights \(4,\ldots,8\), have
quotient dimension 380 over every one of the three field factors and already
reduce all seven \(32\)-nd powers to zero.  Equations of weights \(9\)
through \(15\) only shrink the embedded length from 380 to 328.

The terminal bracket rows of \(z\)-degrees \(-12,\ldots,-21\) introduce no
new coefficients.  They are not needed for the obstruction: the zero set of
the first 79 equations is already the origin, and adding equations can only
shrink it.  As an additional check, the verifier can generate all terminal
rows over the first rational factor and reduce them to zero modulo the same
Gröbner basis.

The computation uses the economical \(u_1=1\) representatives.  Scaling
\[
(P,Q)(z,w)\longmapsto
\bigl(\lambda P(z,\lambda w),\lambda Q(z,\lambda w)\bigr)
\]
preserves \([P,Q]=z^4/w^2=x^2\), sends
\((U,V)(w)\) to \((U,V)(\lambda w)\), and is invertible on the transverse
parameters.  At \(p=32003\), the seventh-power map is bijective in both
\(\mathbf F_p\) and \(\mathbf F_{p^3}\).  Thus each checked representative
scales to the \(u_7=1\) case-c slice; the other six points in each orbit are
its \(\mu_7\)-scalings.

The required vertical vertices are
\[
[w^8]A_0\ne0,\qquad [w^{12}]B_0\ne0,
\]
so a full case-c solution gives a nonzero point of
\(\mathbf P(1,1,2,2,3,3,4)\) after the fiberwise linear recursion.  For the
specialization argument, use the original 165 lower coordinates with weights
\(\operatorname{wt}(A_i)=2-i\) and
\(\operatorname{wt}(B_j)=3-j\).  Their bracket rows define a closed
subscheme of a proper weighted-projective bundle over the finite étale
Hurwitz base; the seven-parameter calculation proves that its complete
special fiber is empty.  If a characteristic-zero case-c point existed,
tame specialization of its outer cover and properness of this original
transverse weighted Proj would extend it, after a finite valued-field
extension, to one of the special fibers just proved empty.  This
contradiction eliminates the full bounded case-c branch over characteristic
zero.

Together with Sections 1--5, this eliminates both branches supplied by the
bounded \((72,108)\) reduction.  The remaining problem is the genuinely
all-degree step; this calculation does not establish such a reduction.

### 7.1 Supplementary local structure

Its forced top edge is
\[
p_8=(z-t)^8,\qquad q_{12}=\kappa(z-t)^{12}
\]
after normalization.

Put \(h=z-t\).  The descending equation of grade \(12+d\), for
\(d=0,\ldots,7\) and \(e=d+4\), has new-unknown operator
\[
12\kappa h^{12}p_d'-12d\kappa h^{11}p_d
8e h^7q_e-8h^8q_e'.
\]
Its image and cokernel are coordinate spaces in the \(h\)-monomial basis.
At grade 19 the complete solution is
\[
q_{11}=\frac{3\kappa}{2}h^4p_7+\lambda_{11}h^{11}.
\]
The grade-18 and grade-17 compatibility coefficients then prove, over every
characteristic-zero algebraic extension,
\[
h^4\mid p_7.
\]
Writing
\[
p_7=h^4(r_0+r_1h+r_2h^2+r_3h^3+r_4h^4),\qquad
p_6=\sum_{i=0}^8d_ih^i
\]
and normalizing the two top-edge scalars, grade 16 further gives
\[
d_0=\frac{r_0^2}{4},\qquad
d_1=\frac{r_0r_1}{2},\qquad
d_8=\frac{r_4^2}{4},\qquad
r_0^3\lambda_{11}=0.
\]
Here the resonant parameter is defined by
\(q_{11}=\frac32h^4p_7+\lambda_{11}h^{11}\).  If instead
\(\widetilde\lambda_{11}\) denotes the total coefficient of \(h^{11}\)
in \(q_{11}\), the last relation is equivalently
\(r_0^3(2\widetilde\lambda_{11}-3r_3)=0\).
For example, the first and last equalities occur as the exact square
compatibility factors
\[
-\frac94(4d_0-r_0^2)^2,\qquad
\frac34(4d_8-r_4^2)^2.
\]

There is also a useful coefficient-at-infinity description.  Let
\[
A(y)=\sum_{d=6}^8 [z^8]p_d\,y^d,\qquad
B(y)=\sum_{e=9}^{12}[z^{12}]q_e\,y^e.
\]
The coefficient of \(z^{19}\) in the high-grade bracket is
\[
4y(2AB'-3A'B)=0.
\]
Consequently \(B^2/A^3\) is constant.  Unique factorization and the four
nonzero endpoint coefficients imply
\[
A=a\,y^6(y-s)^2,\qquad B=b\,y^9(y-s)^3,\qquad abs\ne0.
\]
This explains the high-end square relation \(4d_8=r_4^2\) and packages the
leading coefficients as an exact square/cube approximate root.
Because the \(p_6\) endpoint coefficient is required to be nonzero, the
coefficient \(r_4=[h^8]p_7=[z^8]p_7\) is nonzero.  Combining the low and high
grade-16 square relations gives the invariant statement
\[
h^4\mid\left(p_6-\frac{r^2}{4a}\right),\qquad
\deg_h\left(p_6-\frac{r^2}{4a}\right)\le7,
\quad p_7=h^4r.
\]
The stronger \(h^4\)-divisibility follows from an exhaustive three-chart
calculation in grades 15 and 14, according as
\(r_0\ne0\), \(r_0=0,r_1\ne0\), or \(r_0=r_1=0\).
The grade-15 \(h^{18}\) compatibility coefficient is
\[
-\frac{77}{1024a^3}\lambda_{11}r_4^4.
\]
It follows that the grade-19 resonant parameter vanishes universally:
\(\lambda_{11}=0\).  The grade-17 solution then forces the other required
vertical endpoint
\[
[h^{12}]q_9=\frac{b\,r_4^3}{8a^3}\ne0.
\]

There is an all-parameter approximate-root normal form for all the upper
identities.  Put
\[
P_+=\sum_{d=0}^8p_d(h)y^d,\qquad
Q_+=\sum_{e=0}^{12}q_e(h)y^e,
\]
choose \(\alpha^8=a\), take
\(L=P_+^{1/8}=\alpha h y+O(1)\) at \(y=\infty\), and define
\(A_j=(L^j)_+\).  Then
\[
E_{12}=\cdots=E_{20}=0
\quad\Longleftrightarrow\quad
Q_+=\sum_{j=4}^{12}c_jA_j+S_3,
\]
where \(c_j\) are constants and \(\deg_yS_3\le3\).  Indeed,
\(\deg_yJ(P_+,A_j)\le6\), while a nonconstant coefficient of \(A_j\)
has a nonzero descending triangular term in degree \(j+7\).

The canonical approximate square root \(H=A_4\) satisfies
\[
P_+=H^2+R_3,\qquad \deg_yR_3\le3,
\]
and \(A_{12}-H^3-\frac32HR_3\) has \(y\)-degree at most two.  The
\(h^4\)-divisibility above proves that the \(y^2\)-coefficient of \(H\)
is polynomial in \(h\).  The eliminated resonance \(\lambda_{11}\) is
exactly the fractional-power coefficient \(c_{11}\).  The remaining
fractional resonances and the constant coefficient of \(H\) are the
finite exact obstruction still to be settled; the middle descent below
also proves that the \(y\)-coefficient is polynomial.

The upper grades alone do not make the last two coefficients polynomial.
Two exact full-vertex witnesses with \(h=z-1\) satisfy
\(E_{12}=\cdots=E_{20}=0\):

* For
  \[
  p_8=h^8,\ p_7=h^8,\ p_6=h^8/4,\ p_5=h^2,
  \quad p_4=p_3=p_2=p_1=0,
  \]
  the canonical \(H\) has \([y]H=1/(2h^2)\).
* Replacing \(p_5=h^2\) by \(p_5=0,p_4=h^2\) makes
  \([y]H=0\) but \([1]H=1/(2h^2)\).

The verifier supplies the corresponding \(q_4,\ldots,q_{12}\) explicitly
and checks every upper identity.  For each underlying fixed \(P\), the full
partner matrix has rank \(124\) and its target augmentation rank \(125\), so
neither upper fiber extends merely by changing \(Q\).  Hence any universal
proof of the last two divisibilities must use \(E_{11},\ldots,E_{-1}\); the
upper approximate-root system cannot supply them.

The first witness is already eliminated by adding \(E_{11}\): with
\(q_{12}=B(z-1)^{12}\), the affine system is consistent only on \(B=0\)
(free-\(B\) rank pair \((105,105)\), but the \(B=1\) slice has
\((105,106)\)).  The second extends through \(E_9\), but adding \(E_8\)
similarly forces \(B=0\), with rank pairs \((120,120)\) and
\((120,121)\).  Thus the required nonzero top edge removes both pole
fibers at a precisely identified middle grade.

More generally, the last obstruction can be removed on the maximal
\(h\)-adic chart.  Normalize
\[
r=h^4,\qquad
p_6=\frac14h^8+h^4(s_0+s_1h+s_2h^2+s_3h^3).
\]
The upper rows first force \([h^0]p_5=[h^1]p_5=0\).  The exact ideal
generated by \(E_{13}[h^5]\), \(E_{12}[h^3]\), and \(E_{11}[h^1]\)
has Gröbner consequence \([h^2]p_5^3\), so \([h^2]p_5=0\).
For \(v=[h^3]p_5\), the remaining rows reduce to
\[
\begin{aligned}
4p_{4,0}&=s_0^2,\\
0&=-\frac92\big((2p_{4,1}-s_0s_1)^2-2s_0v^2\big),\\
0&=\frac{21}{2}s_0v(2p_{4,1}-s_0s_1).
\end{aligned}
\]
If \(s_0\ne0\) these imply \(v=0\); if \(s_0=0\), another \(E_{11}\)
row is \(3v^3=0\).  Hence
\[
h^4\mid p_5-\frac{rs}{2a}
\]
on this entire maximal chart, and the \(y\)-coefficient of \(H\) is
polynomial there.  Other \(h\)-adic charts remain open.

The opposite unit chart \(r_0\ne0\) is also eliminated, more directly.
Rows in grades 15 and 14 successively solve the \(q_{10}\) and \(q_9\)
resonances and force the \(h^0,h^1\) coefficients of
\[
D_5=p_5-\frac{rs}{2a}
\]
to vanish.  The remaining two equations are the exact squares
\[
\frac{27}{2}r_0[h^2]D_5^2,\qquad
\frac{21}{2}r_0[h^3]D_5^2
\]
after normalization.  Thus \(h^4\mid D_5\) on \(r_0\ne0\) as well.
The next chart \(r_0=0,r_1\ne0\) also closes.  Two pairs of compatibility
rows eliminate shared resonance expressions and leave nonzero multiples of
\([h^1]D_5^2\) and \([h^2]D_5^2\); the last row is
\(9r_1[h^3]D_5^2\).  Hence \(h^4\mid D_5\) there.  Only the
\(\operatorname{ord}_h(r)=2,3\) charts remain at this stage.

They close as well.  On \(r_0=r_1=0,r_2\ne0\), the first middle ideal
contains \([h^2]D_5^3\).  After the high endpoint rows fix the \(q_{10}\)
resonance, the \(s_0\ne0\) ideal from \(E_{11},E_{10}\) contains
\([h^3]D_5^3\).  On \(s_0=0\), the next endpoint is
\[
E_9[h^0]=\frac{15}{32}r_2^2[h^3]D_5^3.
\]
On \(r_0=r_1=r_2=0,r_3\ne0\), the corresponding first ideal again
contains \([h^2]D_5^3\), and the \(s_0\)-unit ideal contains
\([h^3]D_5^3\).  For the complementary \(s_0=0\) chart, put
\(w=[h^3]D_5\) and \(x=2p_{4,1}\).  The exact rows
\[
E_9[h^0]=\frac{15}{16}wx^2,\qquad
E_{11}[h^4]=-\frac3{16}
 \left(96p_{3,0}x+9r_3x^2-48s_1wx-16w^3\right)
\]
generate an ideal containing \(w^7\).  Thus every possible order
\(0,\ldots,4\) of the nonzero polynomial \(r\) is covered, and
\[
\boxed{\quad h^4\mid p_5-\frac{rs}{2a}\quad}
\]
universally.  Consequently the \(y\)-coefficient of \(H\) is polynomial
in \(h\).  All five chart verifiers carry the fixed base block
\(p_{-1}=z=h+t\) explicitly before descending to \(E_{11}\).  Its
contributions change only the solved \(q_3,q_2,q_1\) coefficients and leave
every compatibility row used in the proof unchanged.  The other fixed base
block \(q_{-1}=z^2\) first enters at \(E_7\), below the identities used for
this divisibility.  The constant coefficient of \(H\) is the next unresolved
divisibility.

The constant-coefficient descent has begun on the maximal chart.  Write
\[
p_5=h^4(S/2+W),\qquad
D_4=p_4-\frac{S^2}{4}-\frac{h^4W}{2}
    =\sum_{i=0}^6e_ih^i.
\]
The four low grade-12 rows are exactly
\[
-24e_0^2,\quad -42e_0e_1,\quad
-18(2e_0e_2+e_1^2),\quad -30(e_0e_3+e_1e_2),
\]
so \(e_0=e_1=0\) universally on this chart.  If \(s_0\ne0\), an endpoint
first fixes \(q_{9,9}=3(s_1+w_1)/2\).  With
\(x=2p_{3,0}-s_0w_0\), the next two rows reduce to
\[
-15e_2x,\qquad -\frac92(x^2-2s_0e_2^2).
\]
Their ideal over \(\mathbf Q(s_0)\) contains \(e_2^3\), proving \(e_2=0\)
on the \(s_0\)-unit subchart.  On \(s_0=0\), four division-free rows in
grades \(11,10,8\) generate an ideal containing \(e_2^4\).

The last coefficient closes similarly.  On \(s_0\ne0\), after the two
endpoint resonances are fixed, put
\(X=2p_{3,1}-s_0w_1-s_1w_0\).  One row is a unit multiple of \(e_3X\),
and the exact combination \(E_{10}[h^5]-2E_8[h^1]/s_0\) is
\[
-\frac{15}{4}(X^2-2s_0e_3^2).
\]
Their ideal contains \(e_3^3\).  On \(s_0=0,s_1\ne0\), the relevant
square and product again generate an ideal containing \(e_3^3\).  Finally,
on \(s_0=s_1=0\), after the two preceding squares are imposed the rows
reduce to
\[
\frac92e_3^2w_0,\qquad
-\frac3{256}\left(
-128e_3^3-768e_3p_{3,2}w_0+384e_3s_2w_0^2
+30q_{9,9}w_0^3-45w_0^3w_1\right).
\]
Their division-free ideal contains \(e_3^5\).  Therefore
\[
\boxed{\quad h^4\mid D_4\quad}
\]
throughout the maximal \(r=h^4\) chart, and the constant coefficient of
\(H\) is polynomial there.  The other orders of \(r\) remain open for
this final coefficient.

The opposite \(r_0\)-unit chart also closes for this last coefficient.
With
\[
p_5=\frac{rs}{2}+h^4W,\qquad
D_4=p_4-\frac{s^2}{4}-\frac{rW}{2}
    =\sum_{i=0}^6e_ih^i,
\]
the exact triangular rows first force \(e_0=e_1=e_2=0\).  A high endpoint
then gives
\[
E_{14}[h^{17}]=12w_3^2,
\]
where \(w_3=[h^3]W\).  Hence \(w_3=0\), and after the \(q_{5,5}\)
resonance is eliminated the remaining low row is
\[
E_{10}[h^1]=-\frac98r_0^2e_3^2.
\]
Thus \(e_3=0\) because \(r_0\ne0\), proving \(h^4\mid D_4\) on this
chart.  The verifier restores the fixed block \(p_{-1}=h+t\) before
\(E_{11}\), so the result uses the full base rather than the truncated
upper recurrence.

There is also a further exact approximate-root consequence on this closed
\(r_0\)-unit chart.  Normalize \(a=b=1\) and write
\[
Q_+=A_{12}+c_{10}A_{10}+c_9A_9+c_8A_8
     +c_7A_7+c_6A_6+c_5A_5+c_4A_4+S_3,
\]
with the already-proved \(c_{11}=0\).  Direct identification of the
triangular slots, followed by the exact compatibility rows, gives
\[
E_{15}[h^5]=-\frac{45}{16}r_0^3c_{10},\qquad
E_{14}[h^4]=-\frac{135}{128}r_0^3c_9
\text{(a term proportional to \(c_{10}\))}.
\]
Consequently \(c_{10}=c_9=0\).  Retain the integral-power parameter
\[
c_8=q_{8,8}-[h^8y^8]A_{12}.
\]
The exact resonance values produced by the constant descent satisfy
\[
\begin{aligned}
q_{7,7}&=[h^7y^7](A_{12}+c_8P),\\
q_{6,6}&=[h^6y^6](A_{12}+c_8P),\\
q_{5,5}&=[h^5y^5](A_{12}+c_8P).
\end{aligned}
\]
Since \(A_7,A_6,A_5\) have triangular diagonal terms
\(h^7y^7,h^6y^6,h^5y^5\), respectively, these three identities prove
\[
\boxed{\quad c_{10}=c_9=c_7=c_6=c_5=0\quad}
\]
on the closed \(r_0\)-unit chart.  The integral terms \(c_8P,c_4H\) and
the degree-three remainder are not eliminated by this argument.

After the fractional terms vanish, the remaining lower system has a much
smaller invariant form.  Write
\[
P_+=H^2+R,\qquad
Q_+=H^3+\frac32HR+c_8P_++c_4H+S,
\qquad \deg_yR,\deg_yS\le3.
\]
For the compressed bracket
\([F,G]=y(F_zG_y-F_yG_z)\), a direct derivation gives
\[
\boxed{\quad
[P_+,Q_+]=[P_+,S]-\left(\frac32R+c_4\right)[H,R].
\quad}
\]
Restoring \(X=zy^{-1}\) and \(B=z^2y^{-1}\), the full residual outside the
already-correct target term is exactly
\[
[X,Q_+]+[P_+,B]+[P_+,S]
-\left(\frac32R+c_4\right)[H,R].
\]
This is the compact system now controlling \(E_{11},\ldots,E_{-1}\).
It does not yet prove \(R=S=0\); in particular, the bottom row remains
\(zq_0'-z^2p_0'=0\).

Its first row is nevertheless completely soluble.  If
\(\sigma_3(h)=[y^3]S\), then degree \(11\) is
\[
(h+t)(h^{12})'+12h^{12}
+3(h^8)'\sigma_3-8h^8\sigma_3'=0.
\]
The operator on \(h^n\) has multiplier \(8(3-n)\), so its only polynomial
kernel is \(h^3\).  Therefore
\[
\boxed{\quad
\sigma_3(h)=\kappa h^3+\frac32t\,h^4+\frac32h^5
\quad}
\]
for one remaining constant resonance \(\kappa\).  The subsequent
\(E_{10}\) row starts a further exact descent.  Put
\[
\rho_3(h)=[y^3]R=u_0+u_1h+u_2h^2+\cdots .
\]
The new unknown \(\sigma_2=[y^2]S\) occurs only through
\(16h^7\sigma_2-8h^8\sigma_2'\), so it does not enter powers below
\(h^7\).  The low rows are
\[
\begin{aligned}
[h^3]E_{10}&=-18u_0^2,\\
[h^5]E_{10}&=-12(2u_0u_2+u_1^2),\\
[h^6]E_{10}&=-9(\kappa r_0+2u_0u_3+2u_1u_2).
\end{aligned}
\]
Consequently, on the \(r_0\)-unit chart,
\[
\boxed{\quad h^2\mid\rho_3,\qquad \kappa=0.\quad}
\]
Thus the free \(E_{11}\) resonance is removed one row later.  Solving the
first two nonresonant coefficients of
\(\sigma_2=[y^2]S\) in the same \(E_{10}\) equation and passing to
\(E_9\) gives the next endpoint
\[
[h^3]E_9=\frac{15}{2}r_0u_2^2.
\]
It follows that
\[
\boxed{\quad h^3\mid\rho_3\quad}
\]
on the \(r_0\)-unit chart.  The next \(E_9\) coefficient fixes, rather than
kills, the remaining \(\sigma_2\) resonance:
\[
\lambda=\frac{6r_1+6r_2t+9u_3^2}{8}.
\]
Substitution into the next compact row gives the decisive square
\[
[h^1]E_8=-\frac{27}{8}r_0^2u_3^2.
\]
The new \(\sigma_1,\sigma_0\) contributions cannot affect this coefficient:
they begin at \(h^3\) and \(h^8\), respectively.  Hence
\[
\boxed{\quad h^4\mid [y^3]R\quad}
\]
on the closed \(r_0\)-unit chart.  This proves polynomial divisibility of
the leading cubic-remainder coefficient, not its vanishing.  The lower
coefficients of \(R,S\) and the rows below \(E_8\) remain open.

The exact boundary of the same calculation is also known.  With
\[
[y^3]R=h^4(u_4+u_5h+u_6h^2),\qquad
a_0=[h^0y^2]R,
\]
the coefficient
\[
[h^5]\sigma_2=\frac34(r_4+u_4u_5)
\]
fixed by \(E_{10}\) cancels the apparent resonant \(E_9[h^8]\) forcing
identically.  Thus there is no equation \(r_4+u_4u_5=0\).  The preceding
nonresonant \(E_9\) row fixes the constant coefficient of
\(\sigma_1=[y]S\) as
\[
\tau_0=\frac3{16}
\left(4a_0u_4-r_0u_4^2+4s_0t\right).
\]
Restoring this already-solved term in \(E_8[h^3]\) changes the apparent
quadric to the exact square
\[
E_8[h^3]=-3(2a_0-r_0u_4)^2.
\]
Thus
\[
\boxed{\quad a_0=\frac{r_0u_4}{2}.\quad}
\]
The next \(E_8\) row fixes the remaining \(\sigma_1\) resonance:
\[
\mu=\frac{
12a_1u_4-3r_1u_4^2+12s_0+12s_1t
}{16}.
\]
After these substitutions \(E_7[h^0]\) vanishes identically.  Therefore
the paired rows relate, rather than independently kill, the constant
coefficient of \([y^2]R\).

The next two coefficient pairs have also been checked against the direct
full compact expression, with every already-solved coefficient of
\(\sigma_2\) and \(\sigma_1\) restored through the target row.  In
particular \(E_{10}\) fixes
\[
[h^6]\sigma_2=\frac38(2u_4u_6+u_5^2),\quad
[h^7]\sigma_2=\frac34u_5u_6,\quad
[h^8]\sigma_2=\frac38u_6^2,
\]
and the nonresonant rows \(E_9[h^9],E_9[h^{10}],E_9[h^{11}]\) fix the
corresponding coefficients of \(\sigma_1\).  After those substitutions,
\[
E_7[h^1]=\frac9{16}r_0
  (-2a_1+r_0u_5+r_1u_4)^2,
\]
so
\[
\boxed{\quad a_1=\frac{r_0u_5+r_1u_4}{2}.\quad}
\]
The intervening coefficient \(E_7[h^2]\) then vanishes identically, while
the next direct coefficient is
\[
E_7[h^3]=\frac98r_0
  (-2a_2+r_0u_6+r_1u_5+r_2u_4)^2.
\]
Consequently
\[
\boxed{\quad a_2=\frac{r_0u_6+r_1u_5+r_2u_4}{2}.\quad}
\]
For the next pair one must first restore two more nonresonant
\(\sigma_1\) coefficients and solve \(E_8[h^8],E_8[h^9]\) for the first
two nonconstant coefficients of \(\sigma_0=[y^0]S\).  The direct result is
\[
E_7[h^4]=0,\qquad
E_7[h^5]=\frac38r_0
  (-2a_3+r_1u_6+r_2u_5+r_3u_4)^2,
\]
and hence
\[
\boxed{\quad a_3=\frac{r_1u_6+r_2u_5+r_3u_4}{2}.\quad}
\]

These four relations are exactly the first four coefficients of
\[
\Delta_2=2h^4[y^2]R-r(h)[y^3]R.
\]
Equivalently, the first four coefficients of \([y^2]R\) agree with those
of \(\frac12r(h)\,[y^3]R/h^4\).

The finite endpoint of the completed \(\sigma_0\) chain is
\[
E_8[h^{15}]=6r_4^2u_6^2.
\]
Since the universal first descent has \(r_4\ne0\), this gives \(u_6=0\).
The direct full \(E_6\) row then gives
\[
E_6[h^{13}]
=-\frac{27}{32}r_4^2(2a_5-r_4u_5)^2,
\]
so \(a_5=r_4u_5/2\).  Hence
\[
\frac{\Delta_2}{h^4}=d_4h^4,\qquad
d_4=2a_4-r_3u_5-r_4u_4.
\]
The remaining \(d_4\) is transferred, rather than killed, by the first
lower pair:
\[
r_0E_7[h^7]-2E_6[h^3]
=\frac34(r_0d_4-4b_0+2s_0u_4)^2.
\]
Thus \(b_0=r_0d_4/4+s_0u_4/2\), where
\(b_0=[h^0y^1]R\).

This transfer is the first coefficient of the next defect
\[
\Delta_1
=4h^4[y^1]R-2s(h)[y^3]R-r(h)\frac{\Delta_2}{h^4}.
\]
After its \(h^4\) coefficient is removed by the preceding square, the
next direct identity is
\[
6r_0E_5[h^1]-6r_1E_5[h^0]-r_0^2E_6[h^5]
=\frac{27}{32}r_0^2\bigl([h^5]\Delta_1\bigr)^2.
\]
Consequently
\[
b_1=\frac{r_1d_4+2s_0u_5+2s_1u_4}{4}.
\]

There is a uniform algebraic meaning to these defects.  Put
\[
\begin{aligned}
A(T)&=h^4+\frac r2T+\frac s2T^2+\frac w2T^3+H_0T^4,\\
B(T)&=\rho_3+\rho_2T+\rho_1T^2+\rho_0T^3,
\end{aligned}
\]
where \(\rho_j=[y^j]R\), and write \(B/A=\sum c_kT^k\) formally.  Then
\[
\boxed{\qquad
\Delta_{3-k}=2^kh^8c_k,\qquad k=1,2,3.
\qquad}
\]
Equivalently, for \(k\ge1\),
\[
\Delta_{3-k}
=2^kh^4\rho_{3-k}-2^kA_{4-k}\rho_3
-\sum_{i=1}^{k-1}\frac{2^iA_{4-i}}{h^4}
 \Delta_{3-k+i}.
\]
Thus the remaining task is to prove \(h^8\mid\Delta_1,\Delta_0\), i.e.
polynomiality of the next formal quotient coefficients.  At present
\([h^4]\Delta_1=[h^5]\Delta_1=0\); degrees \(6,7\) remain open, while
degree \(8\) is the allowed constant quotient coefficient.

The same recurrence continues through the fixed base term.  Indeed
\[
P-H^2=T^{-3}B_{\rm full}(T),\qquad
B_{\rm full}=B+zT^4,
\]
because \(X=z/y=zT\).  The next scaled quotient numerator is therefore
\[
\Delta_{-1}
=16h^4z-16H_0\rho_3
-\frac{r}{h^4}\Delta_0
-\frac{2s}{h^4}\Delta_1
-\frac{4w}{h^4}\Delta_2,
\]
and \(c_4=\Delta_{-1}/(16h^8)\).  Thus the fixed base is the next term
of the same formal-division invariant, not an unrelated perturbation.

There is also a uniform binomial form for every coefficient solved above.
With \(C=B_{\rm full}/A=\sum_{j\ge0}c_jT^j\), direct formal expansion gives
\[
\begin{aligned}
P^{3/2}
 &=T^{-12}A^3+\frac32T^{-7}A^2C
   +\frac38T^{-2}AC^2+O(T^3),\\
P^{1/2}
 &=T^{-4}A+\frac12TC+O(T^6).
\end{aligned}
\]
The omitted terms cannot affect any coefficient through \(y^{-1}=T\).
Consequently the four coefficients
\(\sigma_j=[y^j]S\) are, all at once,
\[
\begin{aligned}
\sigma_3&=\frac32zh^4,\\
\sigma_2&=\frac32z\frac r2+\frac38[T^0](AC^2),\\
\sigma_1&=\frac32z\frac s2+\frac38[T^1](AC^2),\\
\sigma_0&=\frac32z\frac w2+\frac38[T^2](AC^2)+\kappa_0.
\end{aligned}
\]
Here \(\kappa_0\) is exactly the bracket-invisible additive constant.
Symbolic substitution over the complete case-c support recovers every
previously solved coefficient of \(\sigma_3,\ldots,\sigma_0\), including all
Euler resonances.

The next coefficient is therefore forced to match the fixed base:
\[
\boxed{\quad
z^2=\frac32zH_0+\frac38[T^3](AC^2)+c_8z+\frac{c_4}{2}c_0.
\quad}
\]
This is a theorem, rather than an extra ansatz.  Indeed
\[
[T^3](AC^2)
=2\rho_0c_0-\frac w2c_0^2+\frac r2c_1^2+2h^4c_1c_2.
\]
On the present chart \(c_0=u_4+u_5h\), \(c_1=d_4/2\), and
\(h^2c_2\) is polynomial because \(h^6\mid\Delta_1\).  Hence the
difference \(M=z^2-q_{-1,\mathrm{formal}}\) is a polynomial in \(h\).
After adding \(\kappa_0\) so that the constant coefficients agree, the
formal centralizer
\[
F=P^{3/2}+c_8P+c_4P^{1/2}+\kappa_0
\]
and \(Q\) first differ, if at all, in degree \(y^{-1}\).  The complete
grade-seven equation is then simply
\[
-8h^7(M+hM')=0.
\]
Its only Laurent solution is \(M=\lambda/h\), and polynomiality forces
\(M=0\), proving the displayed fixed-base identity.

The same argument has an arbitrary-order normal form.  If a formal
difference first has the term \(n_kh^ky^{-m}\), its highest bracket
coefficient is
\[
-8(m+k)n_kh^{k+7}.
\]
Thus the unique Laurent resonance at order \(m\) is \(h^{-m}y^{-m}\).
It extends uniquely to the formal centralizer \(P^{-m/8}\).  Iterating
through the finite support therefore identifies every homogeneous
first-mismatch freedom with a negative fractional power of \(P\), rather
than with a new row-by-row parameter.

This gives a formal approximate-root normal-form theorem.  In the completed
Laurent field at \(y=\infty\), choose
\(S=P^{1/8}=hy+\text{lower \(y\)-degree}\).  The same first-mismatch
induction proves
\[
\ker [P,-]=\mathbb C(t)((S^{-1})).
\]
After normalizing one particular formal mate \(W_P\) with
\([P,W_P]=z^2y^{-2}\), every hypothetical case-c mate has the unique form
\[
\boxed{\quad
Q=F+W_P+\sum_{m\ge2}\lambda_mP^{-m/8},
\qquad
F=P^{3/2}+c_8P+c_4P^{1/2}+\kappa_0.
\quad}
\]
The \(m=1\) coefficient is absent by the terminal polynomiality argument.
This is the global formal version of the complete approximate-root descent:
all remaining homogeneous freedoms are coefficients of one Laurent series
in \(P^{1/8}\).

At the target grade, \(m=10\), the missing output monomial is \(h^{-3}\).
The prescribed \(z^2=(h+t)^2\) has no such component, so it is
nonresonant.  A particular leading coefficient is
\[
n_{10}
=-\frac1{40}h^{-5}-\frac t{16}h^{-6}
-\frac{t^2}{24}h^{-7}+\lambda_{10}h^{-10},
\]
where only the last term is homogeneous.  In particular, no resonant
coefficient generates the prescribed bracket; the target is produced by
the three displayed nonresonant terms.

The next order supplies the global obstruction on the \(r_0\)-unit chart.
Normalize \(\lambda_{10}=0\).  Since all earlier terms of \(W_P\) vanish,
grade \(-3\) contains only
\[
L_{11}(n_{11})-10p_7'n_{10}-7p_7n_{10}'=0,
\qquad
L_{11}=-8h^7(11+h\partial_h).
\]
The image of \(L_{11}\) omits \(h^{-4}\).  For the complete
\(p_7=h^4(r_0+\cdots+r_4h^4)\), exact extraction gives
\[
\boxed{\quad
[h^{-4}]\bigl(-10p_7'n_{10}-7p_7n_{10}'\bigr)
=-\frac38r_0t^2.
\quad}
\]
Both factors are required nonzero: \(r_0\) defines the chart, while
\(t\ne0\) is the required \((0,8)\) vertex of
\((z-t)^8y^8\).  Hence no formal mate exists on the \(r_0\)-unit chart.
This proof normalizes \(Q\) directly by subtracting formal powers
\(P^{e/8}\); it does not depend on the preceding finite coefficient
descent.

The same obstruction has a coordinate-free weighted-face form.  If
\(r_jh^j\) is the lowest term of \(r\), put
\[
q=\frac{T}{h^{4-j}},\qquad
P_{\rm face}=h^{8j-24}p(q),\qquad
p(q)=q^{-8}a(q)^2.
\]
Use the Rees filtration with
\(\operatorname{wt}(h)=1,\operatorname{wt}(T)=4-j\).  If the full
generic-fiber differential is \(dQ\), then its first nonzero homogeneous
term is \(d(\operatorname{in}Q)\) on the normalization of the face curve.
If \(\operatorname{in}Q\) is a function of \(p\), subtract the
corresponding function of \(P\) and repeat.  Thus the first term not in the
face centralizer must still be an exact rational differential.  This
descent is unchanged by adjoining the eighth root used for the
approximate-root normalization: exactness over the original field implies
exactness after that finite extension.

Consequently a nonzero residue or a nonzero algebraic de Rham class of the
first noncentral face differential is a genuine obstruction to every
possible infinite negative-centralizer cancellation.  For \(j=0\),
the face differential has residue
\[
\operatorname {res}_{q=0}
\frac{t^2}{24}q^{-2}
\left(1+\frac{r_0}{2}q\right)^{3/4}dq
=\frac{r_0t^2}{64},
\]
which is the preceding cokernel after multiplication by \(-24\).

For the lowest-\(r_1\) face the ordinary residue vanishes, but the
differential still has a nonzero algebraic de Rham class.  With
\(c=r_1/2\), it is
\[
\frac{t^2}{16}q^{-5/2}(1+cq)^{7/8}dq.
\]
After \(q=u^2,\ v^8=1+cu^2\), and the harmless constant scaling
\(y=\sqrt c\,u,\ x=v\), the curve is
\[
y^2=x^8-1
\]
and the differential is a nonzero scalar multiple of
\(x^{14}dx/y^5\).  Exact Hermite reduction gives
\[
\frac{x^{14}dx}{y^5}
=d\left(-\frac{x^7}{12y^3}\right)
+\frac7{12}d\left(-\frac{x^7}{4y}\right)
+\frac7{16}\frac{x^6dx}{y}.
\]
The last term is nonexact.  It is regular at every finite point; at the two
points at infinity it has order \(-4\) and zero residue.  If it were
\(df\), hyperelliptic-involution averaging would give an anti-invariant
primitive regular on the affine curve, hence \(f=yB(x)\) with \(B\)
polynomial.  But
\[
d(yx^n)
=\bigl((n+4)x^{n+7}-nx^{n-1}\bigr)\frac{dx}{y},
\]
whose leading degree is at least seven, so no polynomial \(B\) can produce
\(x^6dx/y\).  This excludes the lowest-\(r_1\) face.

For \(j=2\), the full square face is
\[
a(q)=1+\frac{r_2}{2}q+\frac{s_0}{2}q^2.
\]
The logarithmic residue of
\((t^2/8)q^{-4}a(q)^{5/4}dq\) gives the invariant cokernel
\[
\boxed{\quad
\frac{5}{1024}r_2t^2(r_2^2-16s_0).
\quad}
\]
On the two branches left by the preceding square compatibility,
\(s_0=0\) and \(s_0=r_2^2/8\), this is respectively
\(5r_2^3t^2/1024\) and \(-5r_2^3t^2/1024\), hence nonzero.  The
mandatory \(p_6\) square term is included in this face formula; omitting it
would produce a spurious \(r_1\) residue.

On the two remaining charts \(\operatorname{ord}_h(r)=3,4\), the primary
face differential is exact or degenerate, so the normalized tail must be
continued transversely.  Keeping the complete square-root blocks
\[
\begin{aligned}
p_7&=h^4r,\\
p_6&=\frac{r^2}{4}+h^4s,\\
p_5&=\frac{rs}{2}+h^4w,\\
p_4&=\frac{s^2}{4}+\frac{rw}{2}+h^4u,
\end{aligned}
\]
the \(m=11,12,13\) Euler cokernels vanish identically on both charts.
The first transverse cokernel, at \(m=14\), is
\[
\boxed{\quad
-\frac3{16}s_0t(s_0+s_1t).
\quad}
\]
Thus every surviving point on either chart lies on
\[
s_0=0\qquad\text{or}\qquad s_1=-s_0/t.
\]
At \(m=15\) the constant coefficient of \(p_3\), equivalently the first
genuine cubic-remainder face, enters.  The two displayed subbranches remain
open.  The exact transfer has been followed through \(m=19\):

* On \(s_0=s_1=0\), \(m=15\) gives \([h^0]p_3=0\).  Writing
  \(a_1=[h^1]p_3\), \(b_0=[h^0]p_2\), the next two nontrivial cokernels
  are
  \[
  -\frac5{16}a_1t^2w_0
  \]
  and
  \[
  \frac{11}{1024}t^2w_0
  \begin{cases}
  46a_1r_3-48b_0+5w_0^2,&\operatorname{ord}_h(r)=3,\\
  -48b_0+5w_0^2,&\operatorname{ord}_h(r)=4.
  \end{cases}
  \]
  Thus \(w_0\ne0\) fixes \(a_1=0\) and then
  \(b_0=5w_0^2/48\); it does not kill \(w_0\).
* On \(s_1=-s_0/t\) with \(s_0\ne0\), the \(m=17,18,19\) cokernels are
  successively linear in \(a_1,b_0,c_0=[h^0]p_1\), with nonzero
  coefficients proportional to \(s_0t,s_0t,s_0t^2\).  They solve those
  three transverse coefficients and yield no invariant obstruction.

Hence no claim of a complete \(j=3,4\) exclusion is made.

Nor does the terminal identity alone contradict the required vertices.
For example, set \(R=0\), take
\[
H_0=\frac23(z-c_8),\qquad c_8\ne0,
\]
and retain \(t,r_0,r_4\ne0\).  Then the terminal identity holds,
\([z^0]p_0=4c_8^2/9\ne0\), the required high vertices are
\([z^8]p_6=r_4^2/4\) and \([z^{12}]q_9=r_4^3/8\), and an additive
constant supplies the \(Q\)-constant vertex.  All three earlier remainder
defects \(\Delta_2,\Delta_1,\Delta_0\) vanish.  This is not a full
solution: its next fixed-base numerator is
\(\Delta_{-1}=16h^4z\), and the subsequent formal tail fails lower
equations.  More explicitly, with \(c_4=0\) its first nonzero omitted
coefficient is
\[
[y^{-6}]F=\frac38z^2h^{-4},
\]
whose first-mismatch Euler row is
\[
6h^3(2h^2+3th+t^2)\ne0.
\]
It shows precisely why a contradiction still requires control of the
negative formal tail, not merely vertex nonvanishing.

If the descending approximate-root construction can be upgraded globally to
\[
P=x+H^2,\qquad Q=x^2y+H^3,
\]
then the remaining Jacobian equation is
\[
2x^2H_x+(3H-4xy)H_y=0.
\]
Its only polynomial solutions are \(H=\mathrm{constant}\) and
\(H=2xy/3\): a \(y\)-degree comparison first gives
\(\deg_yH\le1\), and substitution of \(H=a(x)y+b(x)\) reduces to two
elementary polynomial ODEs.  Neither solution has the required case-c
vertices.  This is a conditional endgame lemma; the global square/cube
closure has not yet been proved.

The obstruction cannot come from the high grades alone.  With \(h=z-1\), the
explicit full-vertex skeleton
\[
\begin{aligned}
P={}&z/y+1+h^8y^6(y+1)^2,\\
Q={}&z^2/y+1+h^{12}y^9(y+1)^3
       +\frac32(h+1)h^4(y^2+y^3)
\end{aligned}
\]
satisfies every identity \(E_8,\ldots,E_{20}\) exactly and has every required
case-c Newton vertex nonzero.  Its remaining residual is supported only in
grades \(1,2,5,6,7\).  For this fixed \(P\), however, the full
\(302\times125\) exact partner matrix has rank \(124\), while its target
augmentation has rank \(125\).  Thus its lower residual cannot be repaired
by changing \(Q\) alone; one must also deform the approximate root in \(P\).
Any full elimination must use the coupled lower-grade equations
\(E_7,\ldots,E_{-1}\).

The same verifier also gives a four-row covector obstruction on a
29-parameter forced-edge-compatible family with the full required Newton
polygon.  In particular, for
\[
P=1+x+x^8y^{14}+y^8(xy-1)^8
\]
the exact fixed-\(P\) matrix has rank \(124\), while augmentation by the
target \(x^2\) has rank \(125\).

All case-c statements above are checked by

```sh
.venv/bin/python route_bd_case_c_blocks.py
.venv/bin/python route_bd_case_c_diagonal_hurwitz.py
.venv/bin/python route_bd_case_c_radial_obstruction.py
.venv/bin/python route_bd_case_c_graded.py
.venv/bin/python route_bd_case_c_next_descent.py
.venv/bin/python route_bd_case_c_approx_root.py
.venv/bin/python route_bd_case_c_approx_divisibility.py
.venv/bin/python route_bd_case_c_approx_pole_witness.py
.venv/bin/python route_bd_case_c_middle_divisibility_r0.py
.venv/bin/python route_bd_case_c_middle_divisibility_r1.py
.venv/bin/python route_bd_case_c_middle_divisibility_r2.py
.venv/bin/python route_bd_case_c_middle_divisibility_r3.py
.venv/bin/python route_bd_case_c_middle_divisibility.py
.venv/bin/python route_bd_case_c_constant_descent_r0.py
.venv/bin/python route_bd_case_c_constant_descent_r2.py
.venv/bin/python route_bd_case_c_constant_descent_r3.py
.venv/bin/python route_bd_case_c_constant_descent.py
.venv/bin/python route_bd_case_c_fractional_resonances_r0.py
.venv/bin/python route_bd_case_c_lower_remainder_identity.py
.venv/bin/python route_bd_case_c_formal_tail.py
```

The earlier weighted-face analysis excluded
\(\operatorname{ord}_h(r)=0,1,2\) and left the
\(\operatorname{ord}_h(r)=3,4\) charts unresolved.  The global radial
certificate above supersedes that local frontier: it eliminates all charts
simultaneously, without requiring separate square/cube closure on the two
previously open subbranches.

## 8. Universal outer-edge theorem and the all-degree frontier

The Belyi reduction is not special to \((m,n)=(2,3)\).  Let \(1\le m<n\)
be coprime, put
\[
p=mk+1,\qquad q=nk+1,\qquad \delta=n-m,
\]
and suppose \(U,V\) have degrees \(p,q\) and satisfy
\[
E:=\delta UV+mwUV'-nwU'V=\text{a nonzero constant}. \tag{3}
\]
Then
\[
R=\frac{w^\delta V^m}{U^n},\qquad
\frac{R'}R=\frac{E}{wUV}. \tag{4}
\]
Equation (3) makes \(U,V\) coprime and squarefree.  It follows directly
from (4) that \(R\) is a degree
\[
d=n(mk+1)
\]
three-point cover with passport
\[
\left(m^{nk+1},\delta\right),\qquad
\left(n^{mk+1}\right),\qquad
\left((m+n)k+2,1^\kappa\right), \tag{5}
\]
where
\[
\kappa=d-((m+n)k+2)
=\bigl((m-1)(n-1)-1\bigr)k+n-2.
\]
The three defects in (5) add to \(2d-2\).  If \(\kappa<0\), this
Riemann--Hurwitz identity rules out the proposed polynomial edge outright.

There is a normalization point that matters outside the consecutive case.
If (3) is normalized to \(E=1\), evaluation at \(w=0\) forces
\[
U(0)V(0)=\frac1{n-m}.
\]
Thus \(U(0)=V(0)=1\) forces the right side of (3) to be \(n-m\), not one,
unless \(n-m=1\).

For \((m,n)=(2,3)\), the exact Frobenius character formula applied to (5)
gives, for \(k=1,2,3,4\),
\[
1,\quad2,\quad5,\quad14,
\]
the first four nontrivial Catalan numbers.  The bounded calculation above is
the \(k=3\) member.  This pattern is exact computational evidence for a
Catalan classification of the consecutive outer dessins, but no general
Catalan proof is claimed here.

The linear lower deformation at radial deficit \(d\) also has a uniform
form.  With \(F=U/w,\ G=V/w\), new layers
\[
A=A_{m-d},\qquad B=B_{n-d}
\]
map to
\[
\mathcal L_d(A,B)
=w\bigl((m-d)AG'-nA'G+mFB'-(n-d)F'B\bigr). \tag{6}
\]
Writing \(c=m+n-d\), (6) factorizes as
\[
\frac{\mathcal L_d(A,B)}w
=-nG^{c/n}\,d\!\left(AG^{-(m-d)/n}\right)
{}+mF^{c/m}\,d\!\left(BF^{-(n-d)/m}\right). \tag{7}
\]
On the \(mn\)-th-root cover of \(R\),
\[
\frac{F^{c/m}}{G^{c/n}}=R^{-c/(mn)}.
\]
Thus the entire radial rank problem is a two-term twisted de Rham complex on
the same Belyi curve.  Formula (7) is the promising all-degree mechanism:
its kernel and cokernel should be computable uniformly from the divisor
bounds by Kummer eigenspaces and Riemann--Roch, replacing coefficientwise
rank enumeration.

There is an exact formal normal form at the distinguished point over the
third branch value, and it too is valid for general \((m,n)\).  Write
\(t=w^{-1}\), let \(u_p,v_q\) be the leading coefficients, let \(E\) be the
nonzero constant in (3), and put
\[
L=\frac{v_q^m}{u_p^n},\qquad N=(m+n)k+2.
\]
Since \(R=G^m/F^n\) for \(F=U/w,\ G=V/w\), (4) gives
\[
\frac RL
=1-\frac{E}{u_pv_qN}t^N+O(t^{N+1}). \tag{8}
\]
Consequently
\[
\sigma=\left(\frac{u_pv_qN}{E}(1-R/L)\right)^{1/N}
=t+O(t^2)
\]
is the unique normalized formal parameter.  There is a unique unit
\(H(\sigma)=1+O(\sigma)\) such that
\[
F=u_p\sigma^{-mk}H^m.
\]
After the triangular change \(\zeta=zH(\sigma)\), the outer pair is exactly
\[
P_{\rm out}=u_p\zeta^m\sigma^{-mk},\qquad
Q_{\rm out}=v_q\zeta^n\sigma^{-nk}
 (1-\sigma^N)^{1/m}. \tag{9}
\]
Indeed, the \(m\)-th power of the quotient of the second expression by
\(v_q\sigma^{-nk}H^n\) is forced by \(G^m/F^n=R\), and its constant term
selects the unique formal \(m\)-th root.  Moreover
\[
\{\zeta,\sigma\}=-\sigma\mu(\sigma),\qquad
\mu=H\,\frac t\sigma\frac{d\sigma}{dt}=1+O(\sigma).
\]
Multiplication by this unit does not change any lower zero row.  For
\((m,n)=(2,3)\), (9) is the square-root normal form previously displayed.

The finite Laurent-jet lattice change has an exact determinant formula.
Before normalizing, write
\[
\sigma=at+O(t^2),\qquad H=h+O(\sigma),
\]
with \(a,h\) units.  For an integer interval \(I=[r,s]\), project
\[
H^e\sum_{j\in I}c_jt(\sigma)^{-j}
\]
to the window spanned by \(\sigma^{-j}\), \(j\in I\).  In bases ordered by
increasing \(j\), the matrix is upper triangular, because
\[
H^et(\sigma)^{-j}
=a^jh^e\sigma^{-j}+\text{terms of larger \(\sigma\)-valuation}.
\]
Thus
\[
\det T_{I,e}
=a^{\sum_{j\in I}j}h^{e|I|}. \tag{10}
\]
At deficit \(d\), the exponents are \(e=d-m\) for the \(P\)-layer and
\(e=d-n\) for the \(Q\)-layer.  With vertical bound \(m(k+1)\), the
\(P\)-interval is
\[
\begin{cases}
[0,mk+d],&d<m,\\
[1,m(k+1)],&d=m,\\
[d-m,m(k+1)],&d>m,
\end{cases} \tag{11}
\]
as long as the last interval is nonempty; the \(Q\)-formula is obtained by
replacing \(m\) by \(n\).  Equations (10)--(11) recast the local lattice
theorem for every gcd-reduced degree pair, not merely the radial
\((2,3)\) support.

For \((m,n)=(2,3)\), multiplying (10) over the layers \(d=1,\ldots,8\)
gives the source-lattice determinant
\[
a^{52k^2+113k+7}h^{76k-32}. \tag{12}
\]
If the bracket unit is absorbed into the target coordinates, the
corresponding product over the output jet windows is
\[
a^{100k^2+125k+28}h^{-20k-32}. \tag{13}
\]
The canonical choice has \(a=h=1\), so all these changes are unipotent.
In particular, no discriminant or resultant can occur in this local
determinant.

There are no hidden discriminant or resultant divisors on the outer
Hurwitz locus either.  Over a base on which
\[
mn(n-m)E u_pv_q
\]
is invertible, reduce (3) modulo \(U\):
\[
-nwU'V=E.
\]
Thus \(w,U',V\) are units in the finite algebra \(B[w]/(U)\).  Their norms
show that \(\operatorname{Disc}(U)\) and \(\operatorname{Res}(U,V)\) are
units.  Reducing modulo \(V\) similarly makes
\(\operatorname{Disc}(V)\) a unit.  The only possible divisors needed to
construct the normalized formal change are therefore among
\[
mn(n-m)N E u_pv_q=0, \tag{14}
\]
and none occurs over a characteristic-zero passport fiber with nonzero
leading terms.

The qualification “formal differential problem” remains essential.  The
change \((z,w)\mapsto(\zeta,\sigma)\) sends each bounded polynomial
coefficient space to an outer-dependent lattice in
\(\mathbf C((\sigma))\).  Formula (10) identifies every individual
projected lattice with a standard filtered jet module and proves base
change for that lattice.  It does **not** prove strictness of the
two-term differential with respect to the valuation filtration.  Indeed, a
naive replacement of all transformed lattices by their monomial Laurent
windows gives, at \(d=1,\ldots,8\), the kernel profiles
\[
\begin{array}{c|c}
k&\text{naive associated-graded kernel dimensions}\\ \hline
1&(5,5,4,3,2,1,0,0)\\
2&(7,7,6,5,4,3,2,1)\\
3&(9,9,8,7,6,5,4,3),
\end{array}
\]
instead of \((2,2,2,1,0,\ldots)\).  This is a concrete exact countermodel
to assuming strictness from the associated graded alone.

The naive filtration therefore cannot prove the stable kernel dimensions.
The direct polynomial parameterization below bypasses this problem for the
linear complex.  Strict filtered transport remains necessary for the 19
nonlinear compatibility rows.  The determinant calculation removes
divisorial degeneration as the issue there; the possible failure is
extension data between valuation grades.

There is a more intrinsic candidate for the required strict filtration.
Put \(c=m+n-d\), \(X=AG\), and \(Y=BF\).  Formula (7) becomes the exact
identity
\[
\frac{\mathcal L_d(A,B)}w
=-n\left(dX-\frac cnX\,d\log G\right)
{}+m\left(dY-\frac cmY\,d\log F\right). \tag{15}
\]
Thus every linear layer is the sum of two rank-one logarithmic Kummer
connections
\[
\nabla_{G,c}=d-\frac cn\,d\log G,\qquad
\nabla_{F,c}=d-\frac cm\,d\log F. \tag{16}
\]
Their local monodromies are roots of unity.  After compactifying the
punctured \(w\)-line, their canonical Deligne extensions are therefore
finite-monodromy parabolic line bundles, and their logarithmic de Rham
complexes have the standard strict Hodge filtration.

The bounded polynomial spaces are not automatically the canonical
Deligne lattices.  Multiplication by \(G\) in \(X=AG\) and by \(F\) in
\(Y=BF\) forces one zero at each simple root, while the canonical
extension calls for the integral shifts determined by
\(\lceil c/n\rceil\) and \(\lceil c/m\rceil\).  The endpoint intervals
(11) add further modifications at \(0\) and \(\infty\).  Hence the exact
linear all-\(k\) problem is reduced to a finite elementary-modification
complex supported on
\[
\operatorname{div}(F)+\operatorname{div}(G)+\{0,\infty\}. \tag{17}
\]
Its matrices are root-value and, when a shift exceeds one, confluent
root-jet evaluation matrices.  Their determinants are products of
leading coefficients, Vandermonde discriminants, and cross-resultants.
By the norm argument following (14), all of these are units on the tame
outer Hurwitz locus, apart from explicit scalar residue factors such as
\(c-rm\) and \(c-sn\).  Those scalar resonances depend only on
\((m,n,d)\), not on \(k\) or on the individual dessin.

For the consecutive pair, the stable linear pattern can in fact be proved
without completing that modification table.  Put \(p=2k+1,\ q=3k+1\),
let
\[
E=UV+2wUV'-3wU'V
\]
be the nonzero outer constant, and let \(\mathcal K_d(A,B)\) denote the
deficit-\(d\) linear bracket after clearing the two powers of \(w\):
\[
\mathcal K_d(A,B)
=(2-d)A(wV'-V)-3wA'V
{}+2wUB'-(3-d)(wU'-U)B. \tag{18}
\]
For \(c=5-d\ne0\) and a polynomial \(C\), define
\[
\begin{aligned}
A_C&=\frac{cwCU'+(d-3)CU-2wC'U}{c},\\
B_C&=\frac{cwCV'+(d-2)CV-3wC'V}{c}. \tag{19}
\end{aligned}
\]
Direct differentiation gives the three identities
\[
\begin{aligned}
\mathcal K_d(A_C,B_C)&=wC E'=0,\\
2UB_C-3VA_C&=EC,\\
\mathcal K_d(2UT,3VT)&=cET. \tag{20}
\end{aligned}
\]
Consequently every bounded kernel pair is represented by exactly one
polynomial
\[
C=\frac{2UB-3VA}{E}. \tag{21}
\]
Indeed, subtract (19); the second identity in (20), coprimality of \(U,V\),
and the last identity show that the difference vanishes.

The support count in \(C\) is elementary at the two endpoints.  The
low-degree classes are
\[
C=1\quad(d=1),\qquad C=w\quad(d=2,3),
\]
and there is no low-degree class at \(d=4\).  Any additional class has
degree forced by the common indicial root at infinity:
\[
\deg C=ck+1. \tag{22}
\]
For fixed leading coefficient, the descending coefficients are unique,
because the successive indicial coefficients are \(2,4,6,\ldots\).

Existence of this high class is a direct consequence of the Belyi contact.
The two normalized formal horizontal solutions of the operators in (19)
are
\[
\Phi_U=u_p^{-c/2}w^{(d-3)/2}U^{c/2},\qquad
\Phi_V=v_q^{-c/3}w^{(d-2)/3}V^{c/3}. \tag{23}
\]
They both lead with \(w^{ck+1}\), and
\[
\frac{\Phi_U}{\Phi_V}
=\left(\frac LR\right)^{c/6}=1+O(t^N),\qquad N=5k+2. \tag{24}
\]
Since
\[
(ck+1)-N=-(dk+1)<0,
\]
their polynomial parts at infinity coincide.  Call the common part
\(C_d^+\).  For \(d=1\), it already has the required lower support.  For
\(d=2,3,4\), discard respectively its constant, constant, or affine part.
The discarded polynomial contributes only inside the permitted upper
window, while the remainder has the required zero at \(w=0\).
This constructs the unique high class.

At \(d=5\), one instead has
\[
\mathcal K_5(A,B)
=w^2\frac d{dw}\left(\frac{2UB-3VA}{w}\right).
\]
The lower endpoint forces the integration constant to vanish; coprimality
and the upper endpoint then give \(A=B=0\).  For \(d\ge6\), (21) makes
\(C\) divisible by \(w^{d-3}\), while the upper \(P\)-bound permits degree
at most one unless the indicial root \((5-d)k+1\) occurs.  That root is
nonpositive, so again \(C=0\).

This proves, in characteristic zero and for every \(k\ge1\),
\[
\dim\ker\mathcal L_d=
\begin{cases}
2,&d=1,2,3,\\
1,&d=4,\\
0,&d\ge5.
\end{cases} \tag{25}
\]
Thus the seven kernel weights
\[
(1,1,2,2,3,3,4)
\]
are now an all-\(k\) theorem for the stated \((2,3)\) radial support, not
merely a \(k=1,2,3\) observation.  Explicit \(C\)-representatives for the
seven classes are
\[
\begin{array}{c|c}
d& C\text{-classes}\\ \hline
1&1,\quad
\left[u_p^{-2}w^{-1}U^2\right]_+
 -\left[u_p^{-2}w^{-1}U^2\right]_+(0),\\
2&w,\quad V-V(0)-V'(0)w,\\
3&w,\quad U-U(0)-U'(0)w,\\
4&\left[u_p^{-1/2}(wU)^{1/2}\right]_+
 -\text{its affine part}.
\end{array} \tag{26}
\]
Here \([\,\cdot\,]_+\) is the polynomial part at \(w=\infty\); rescaling
any displayed class is harmless.  Formula (19) turns these seven
polynomials into the corresponding kernel pairs \((A,B)\).  The exact
small-field rank calculations below remain independent checks.

The \(C\)-parameter also supplies the missing multiplicative structure.
Normalize \(E=1\) and write
\[
P_0=z^2U/w,\qquad Q_0=z^3V/w.
\]
Their Jacobian two-form is
\[
\Omega=dP_0\wedge dQ_0=\frac{z^4}{w^3}\,dz\wedge dw. \tag{27}
\]
For \(c=5-d\ne0\), set
\[
H_{d,C}=-\frac{z^cC(w)}{cw}. \tag{28}
\]
With the convention \(\iota_{X_H}\Omega=dH\), its Hamiltonian vector field
is
\[
X_{d,C}
=z^{1-d}\frac{w(C-wC')}{c}\,\partial_z
{}+z^{-d}w^2C\,\partial_w. \tag{29}
\]
Direct substitution gives
\[
X_{d,C}(P_0)=z^{2-d}A_C,\qquad
X_{d,C}(Q_0)=z^{3-d}B_C. \tag{30}
\]
Thus the seven linear modes are precisely the bounded Hamiltonian gauge
modes for the fixed volume form (27).  Their formal Hamiltonian flows
preserve \(\Omega\), and hence preserve the full bracket, to every order.
The nonlinear consistency equations are therefore not intrinsic formal
Maurer--Cartan obstructions: they measure escape of these exact formal
flows from the bounded polynomial support.

The scalar potentials carry an explicit graded Lie bracket.  For a second
class \((e,D)\), put \(f=5-e\) and \(g=5-d-e\).  The commutator potential is
\[
H_{d,C}\star H_{e,D}
=z^g\left(
\frac{(wC'-C)D}{c}
+\frac{C(D-wD')}{f}
\right). \tag{31}
\]
When \(g\ne0\), this is \(H_{d+e,C\star D}\), where
\[
C\star D
=-gw\left(
\frac{(wC'-C)D}{c}
+\frac{C(D-wD')}{f}
\right). \tag{32}
\]
Equation (32) is antisymmetric and polynomial in \(C,D\).  At \(g=0\),
(31) remains the correct \(z^0\) Hamiltonian even though the normalization
(28) is singular.

This replaces the abstract \(L_\infty\)-transport proposal by a concrete
target.  The remaining nonlinear theorem should filter the completed
Hamiltonian Lie algebra by the allowed Newton support and prove that any
nonzero combination of the seven potentials has an unavoidable first
escaped coefficient, in weights at most eight.  A triangular endpoint or
residue formula for that first escape would imply the all-\(k\)
origin-only statement without transporting the full 19-row matrix.

There is, however, an exact obstruction to using only the leading
endpoint.  The four high classes have
\[
C_d=w^{(5-d)k+1}+\text{lower powers},\qquad 1\le d\le4,
\]
so their principal Hamiltonians are
\[
H_{d,C_d}=-\frac{(zw^k)^{5-d}}{5-d}+\text{lower \(w\)-order}. \tag{33}
\]
They are all functions of the same monomial \(\xi=zw^k\), hence their
principal Hamiltonian brackets vanish.  This also follows directly from
(31): if \(c=5-d,\ f=5-e\), \(r=ck+1\), and \(s=fk+1\), then the leading
coefficient is
\[
\frac{r-1}{c}+\frac{1-s}{f}=k-k=0. \tag{34}
\]
Writing
\[
C=w^r+a w^{r-1}+\cdots,\qquad
D=w^s+b w^{s-1}+\cdots,
\]
the first coefficient that can survive is instead
\[
\frac{b}{f}-\frac{a}{c}. \tag{35}
\]
For the actual outer edge even (35) vanishes.  Put
\[
T_U=\left(\frac{U}{u_pw^{2k+1}}\right)^{1/2},\qquad
T_V=\left(\frac{V}{v_qw^{3k+1}}\right)^{1/3}.
\]
The contact formula for \(R\) gives
\[
T_V/T_U=1+O(t^{5k+2}),\qquad t=w^{-1}. \tag{36}
\]
Since \(5k+2-(ck+1)=(5-c)k+1>0\), every polynomial term of each high
class is the allowed truncation of
\[
\widehat C_c=w^{ck+1}T_U^c=w\chi^c,\qquad
\chi=w^kT_U,\qquad 1\le c\le4. \tag{37}
\]
For two such complete Laurent series,
\[
\frac{(w\widehat C_c'-\widehat C_c)\widehat C_f}{c}
+\frac{\widehat C_c(\widehat C_f-w\widehat C_f')}{f}=0. \tag{38}
\]
Consequently every high--high bracket is a commutator of the pieces
discarded by the two endpoint truncations.  A successful infinity argument
must therefore retain the boundary tails, not merely any fixed number of
common leading coefficients.

The most obvious refinement still fails.  Give the seven parameters the
\(w\)-degrees of their \(C\)-polynomials,
\[
(0,4k+1,1,3k+1,1,2k+1,k+1). \tag{39}
\]
For the complete \(k=1\) and \(k=2\) coefficient fields, every
weight-at-most-eight consistency equation has a unique highest
(39)-term, a nonzero pure power of \(X_1\).  Their initial ideal is therefore
only
\[
\langle X_1^4\rangle, \tag{40}
\]
which leaves six free coordinate directions.  This is an exact
countermodel to a one-step leading-degree degeneration, not evidence of a
nonzero solution of the original consistency equations.

Nor can the Darboux torus turn bounded support directly into local
nilpotence.  In
\[
r=\frac{z^5}{5w},\qquad s=\frac1w,\qquad
\Omega=ds\wedge dr,
\]
the Hamiltonian \(H=rs\) generates the semisimple derivation
\(r\partial_r-s\partial_s\).  It is not locally nilpotent, while its flow
\((r,s)\mapsto(e^t r,e^{-t}s)\) preserves every finite Laurent support.
Any two-parahoric argument must therefore prove actual extension or
integrality of the symplectomorphism, not infer it from finite support of
two images alone.

The boundary cover itself is rigid enough once such an extension is
available.  For \((m,n)=(2,3)\), the passport of
\[
R(w)=\frac{wV(w)^2}{U(w)^3}
\]
has a unique simple zero and a unique point of ramification \(5k+2\), the
latter at \(w=\infty\).  A deck transformation fixes both.  In coordinates
placing them at \(0,\infty\), it is \(w\mapsto\lambda w\); comparison at the
simple zero forces \(\lambda=1\).  Equivalently, a nontrivial orbit size
would divide both \(3k+1\) and \(2k+1\), whereas
\[
3(2k+1)-2(3k+1)=1. \tag{41}
\]
Thus the outer Belyi map has trivial deck group for every \(k\ge1\).
For \(k=1\), the exact normalized companion to the displayed \(U\) below is
\[
V=1+\frac23w+\frac6{25}w^2+\frac{36}{875}w^3
  +\frac{18}{4375}w^4,
\]
and direct calculation gives \(E=1\), \(L=160/441\), a simple zero at
\(w=0\), and contact order seven with \(L\) at infinity.

There is an exact warning against strengthening deck rigidity to a
statement about Hamiltonians.  Bracket the low \(d=1\) mode \(C=1\)
with the high \(d=4\) mode \(D=C_4^+\).  Formula (31), now with
\(5-d-e=0\), gives the nonzero \(z\)-independent Hamiltonian
\[
h_D(w)=\frac34D(w)-wD'(w).
\]
Since \(D\) has only terms of degrees \(2,\ldots,k+1\), this cannot
vanish.  In the Darboux coordinates above its flow is
\[
(r,s)\longmapsto
\bigl(r-t\,\partial_s h_D(1/s),\,s\bigr).
\]
It is a finite Laurent translation, fixes \(w=1/s\), and therefore fixes
\(R(w)\) exactly.  Thus triviality of the deck group does not force a
cover-fixed meromorphic Hamiltonian to vanish: the flow can be vertical
over the cover.

Nor does a naive trace-zero supplement repair this.  On both rational
points of the certified degree-\(21\) fiber over
\(\mathbf F_{32003}\), exact Newton-sum calculation for
\[
wV(w)^2-TU(w)^3
\]
shows that
\[
\operatorname{Tr}(w^j)\in\mathbf F_{32003}
\qquad(0\le j\le12).
\]
Consequently the twelve polynomials
\[
w^j-\frac1{21}\operatorname{Tr}(w^j),
\qquad1\le j\le12,
\]
are linearly independent, trace-zero, and have a pole only at infinity.
On the full scalar window
\(\langle w^{-1},1,w,\ldots,w^{12}\rangle\), the trace map has rank
only two.  In particular \(\operatorname{Tr}(h_D)\) is constant for the
actual degree-\(21\) \(d=4\) modes.  Subtracting
\(\operatorname{Tr}(h_D)/21\) makes \(h_D\) trace-zero without changing
its vector field.  Hence bounded principal parts, trace zero, finite
Laurent flow, exact preservation of \(R\), and trivial deck group still
do not imply that the Hamiltonian is zero.

The missing word is **integral**.  The vertical translation above sends
\[
z^5\longmapsto z^5+B(w).
\]
If \(B\ne0\), the right side is not a fifth power in \(K(w)(z)\): as a
polynomial in \(z\), it is squarefree and each of its zeros has valuation
one.  Thus the flow is finite in \((r,s)\) but does not give a rational
map in the original \(z\)-coordinate, and its action on \(z^2,z^3\)
has an infinite Kummer expansion.

This yields a useful terminal rigidity lemma.  Suppose a rational
symplectomorphism \(\phi\) of \(K(z,w)\) satisfies
\[
R(\phi(w))=R(w),\qquad \phi^*\Omega=\Omega.
\]
Because \(K(w)\) is relatively algebraically closed in \(K(w)(z)\),
\(\phi(w)\in K(w)\); triviality of the deck group gives
\(\phi(w)=w\).  The volume equation then integrates to
\[
\phi(z)^5=z^5+B(w).
\]
The fifth-power argument forces \(B=0\), so
\(\phi(z)=\zeta z\) with \(\zeta^5=1\).  An identity-jet Hamiltonian flow
has \(\zeta=1\).  Thus cover rigidity becomes effective only after the
formal flow is proved rational in the original Kummer coordinate.

This does **not** yet finish the two-parahoric route.  A bounded completion
\((P,Q)\) has not been shown to extend to an automorphism of the normalized
compactified \(R\)-cover, or even to a birational self-map whose boundary
restriction is a deck transformation.  Triviality of the deck group proves
rigidity only after that reconstruction/integrality step.

The integrality target can be stated sharply.  If one could prove the ring
descent
\[
P,Q\in K[P_0,Q_0], \tag{42}
\]
then the problem would be over.  Give \(P_0,Q_0\) their \(z\)-weights
\(2,3\).  Distinct target monomials of the same weight cannot cancel their
leading coefficient: after factoring one monomial, such a cancellation
would be a nonzero polynomial relation over \(K\) for the nonconstant
function \(R=Q_0^2/P_0^3\).  Hence the \(z\)-bounds imply
\[
P=aP_0+c,\qquad Q=bQ_0+\lambda P_0+d. \tag{43}
\]
The fixed outer edge gives \(a=b=1\).  In the \(z^2\)-block of \(Q\), the
allowed \(w\)-exponents are nonnegative, whereas
\(P_0=z^2U/w\) has the nonzero coefficient \(U(0)\) at \(w^{-1}\);
indeed \(E=U(0)V(0)\ne0\).  Thus \(\lambda=0\), and the standard additive
normalization removes \(c,d\).  Therefore ring descent implies
\((P,Q)=(P_0,Q_0)\).

Field descent alone is weaker: even if \(K(P,Q)=K(P_0,Q_0)\), rational
target expressions could have boundary denominators.  Proving that the two
bounded images are integral over, and actually lie in, the target
coordinate ring is the precise missing bridge.

There is an exact converse bridge in the **source** direction.  Return to
the original case-c plane
\[
z=xy,\qquad w=xy^2,\qquad x=z^2/w,\qquad y=w/z.
\]
Both \(F_0\) and a normalized completion \(F\) have Jacobian \(x^2\).
The outer model \(F_0\) contracts \(D=(x=0)\) to the target origin, whereas
a full case-c completion generally restricts to a nonconstant degree-
\((8,12)\) map on \(D\).  Let \(T=(X,Y)\) be the algebraic branch of
\(F_0^{-1}\circ F\) selected by the outer formal expansion.  If **both**
\(X,Y\) are integral over \(K[x,y]\), then \(T\) is polynomial.

Indeed, let \(\Gamma\) be the normalization of \(\mathbb A^2\) in
\(K(x,y)(X,Y)\).  Integrality makes the graph projection
\(\pi:\Gamma\to\mathbb A^2\) finite, while \(X,Y\) define a regular second
projection \(\tau:\Gamma\to\mathbb A^2\).  The identity
\[
F_0\circ\tau=F\circ\pi
\]
places \((\pi,\tau)\) in the fiber product of \(F\) and \(F_0\).  Over
\(x\ne0\), a prime divisor of \(\Gamma\) cannot have \(X=0\): it would map
by \(F\) to the origin, whereas \(F\) is étale there and therefore has
zero-dimensional fibers.  At every remaining codimension-one point the
graph projection is a component of the base change of the étale locus of
\(F_0\), hence is unramified.  Zariski--Nagata purity, applied to the
finite generically separable map onto the regular surface
\(\mathbb G_m\times\mathbb A^1\), removes a possible codimension-two branch
locus.  Consequently
\[
\Gamma|_{x\ne0}\longrightarrow\mathbb G_m\times\mathbb A^1
\]
is finite étale.

Every connected finite étale cover of
\(\mathbb G_m\times\mathbb A^1\) in characteristic zero is Kummer,
\(u^e=x\).  At the selected radial valuation
\[
t=w^{-1},\qquad x=z^2t,\qquad y=(zt)^{-1},
\]
one has \(v_t(x)=1\), while the normalized branch lies in the unextended
completion \(K(z)((t))\).  A nontrivial Kummer cover is totally ramified of
index \(e\) at this valuation.  The split branch therefore forces \(e=1\).
Thus \(X,Y\in K(x,y)\); normality of \(K[x,y]\) and integrality give
\(X,Y\in K[x,y]\).

The chain rule now gives
\[
X^2\operatorname{Jac}(T)=x^2.
\]
Unique factorization forces
\[
X=cx,\qquad Y=c^{-3}y+h(x).
\]
The identity outer jet sets \(c=1\).  If \(a_rx^r\) is the lowest nonzero
term of \(h\), then
\[
x(y+h)^2
=w+2a_rz^{2r+1}w^{-r}+\text{higher \(z\)-degree},
\]
and \(xU(x(y+h)^2)\) acquires the nonzero first escaped layer
\[
2a_rz^{2r+3}w^{-r-1}U'(w).
\]
This contradicts the case-c cap \(\deg_zP\le2\).  Hence
\[
\boxed{\text{original-plane integrality of the selected branch implies }
T=\mathrm{id}.} \tag{43a}
\]

The word “integral” cannot be replaced by “the two outputs are
polynomial.”  For example
\[
F_0=(x^2,xy),\qquad F=(x^2+(xy)^2,xy)
\]
are polynomial, have the same Jacobian \(2x^2\), and contract the same
critical line.  The normalized inverse branch is
\[
X=x\sqrt{1+y^2},\qquad Y=\frac{y}{\sqrt{1+y^2}}.
\]
The first coordinate is monic integral, but the second has a pole above
\(1+y^2=0\).  Higher-degree versions can be tangent to the identity to
arbitrarily high order.  Thus polynomiality of \(P,Q\) gives polynomial
graph equations, not finiteness of the chosen graph component; the
nonproperness of \(F_0\) is exactly the remaining loophole.  The earlier
nonlinear-shear countermodel fails the new hypothesis for the same reason:
it is regular only after localization and its missing inverse coordinate
has a divisor pole.

Trivial deck group cannot supply even field descent by itself.  The
elementary extension
\[
K(t)/K(t^3+t)
\]
has degree three and trivial deck group: an affine transformation
\(t\mapsto at+b\) preserving \(t^3+t\) has \(a=1,b=0\).  Nevertheless
\(t\notin K(t^3+t)\).  Thus the deck theorem is only a terminal rigidity
input after reconstruction, not a mechanism for reconstruction.

The boundary-tail calculation does reveal two stable square relations.
In the canonical parameter order, define
\[
Y_0=X_0-2X_1,\qquad
Y_2=X_2-\frac23X_3,\qquad
Y_3=X_4-X_5. \tag{44}
\]
These are not fitted coordinates.  The coefficient \(2\) is the constant
term of \(U^2/w\), while \(V'(0)=2/3\) and \(U'(0)=1\) in the normalized
\(u_1=1\) chart.  Thus (44) measures exactly the affine pieces missing
from the high polynomial truncations.

Over the complete \(k=1,2\) coefficient fields and every \(k=3\) Hurwitz
factor, the weight-four equations contain
\[
\left(Y_2-\kappa_kY_0^2\right)^2,\qquad
\kappa_k=\frac{(4k+1)^2}{16k}. \tag{45}
\]
The exact values are \(25/16,81/32,169/48\).  On the reduced boundary
\(Y_0=Y_2=0\), every one of these fibers also contains a nonzero multiple
of
\[
Y_3^2 \tag{46}
\]
at weight six.  Relations (45)--(46) are the first concrete
scale-independent-looking endpoint/BCH chain.  The formula in (45) is
still a conjectural all-\(k\) extrapolation: it has been verified on all
small Hurwitz fibers available here, not derived symbolically for arbitrary
\(k\).

The much longer rational \(k=1\) factor chain is **not** stable.  At
\(k=1\), after imposing (45), particular rows factor successively as
\(Y_0G,Y_0^2G,Y_0^3G\).  At \(k=2\), the second weight-four binary
quadratic has nonzero resultant with (45), so weight four already forces
\(Y_0=Y_2=0\).  At \(k=3\), both weight-four rows are multiples of (45),
but the surviving weight-five row after (45) is not divisible by \(Y_0\).
Consequently only the endpoint coordinates and square relations, not the
common factor \(G\), are credible universal structure.

There is a cleaner first integrality functional at the Kummer resonance
\(d+e=5\).  For such a pair, (31) is a \(z\)-independent Hamiltonian
\[
h_{C,D}(w)=
\frac{(wC'-C)D}{5-d}
+\frac{C(D-wD')}{5-e}. \tag{47}
\]
In Darboux coordinates it translates \(r\), hence
\[
z^5\longmapsto z^5+B_{C,D}(w),\qquad
B_{C,D}=5w^3h_{C,D}' . \tag{48}
\]
If \(B_{C,D}\ne0\), the right side is squarefree as a polynomial in \(z\)
and cannot be a fifth power in \(K(w)(z)\).  Thus, if an exact ordered
rational factorization through weight five isolates this resonant
translation factor, rationality of that factor forces the total
translation polynomial to vanish.  Rationality of the full time-one map,
even after rational lower-weight factors are removed, does not by itself
imply rationality of the flow of its leading logarithmic symbol; the
statement here is conditional on factorization through the resonant
factor.

The low-low \(d=2,d=3\) bracket vanishes.  The other five products,
in the canonical \(X_0,\ldots,X_6\) order, have independent translation
polynomials over the complete \(k=1,2\) coefficient fields and every
\(k=3\) Hurwitz factor.  Consequently the first factorized resonant
obstruction is exactly
\[
X_0X_6=X_1X_6=X_2X_5=X_3X_4=X_3X_5=0. \tag{49}
\]
At \(k=3\), the fixed coefficient minor in degrees \(w^4,\ldots,w^8\)
is nonzero on all five points of the finite étale special fiber, so it is
a unit on the localized Hurwitz algebra.  Hence the rank statement behind
(49) is branch-independent for the actual bounded \((72,108)\) family in
characteristic zero.  Deducing (49) for a rational comparison branch
still requires exact rational factorization through the weight-five
translation, not only rational descent of the lower weights.

For arbitrary scale, order the five nonzero \(B\)'s as
\[
(1-,4+),(1+,4+),(2-,3+),(2+,3-),(2+,3+)
\]
and set
\[
\Delta_k=\det([w^i]B_j)_{4\le i\le8}. \tag{50}
\]
If \(\widetilde B_j=B_j/w^4\), then
\[
\Delta_k=
\frac{\operatorname{Wr}(\widetilde B_1,\ldots,\widetilde B_5)(0)}
{0!\,1!\,2!\,3!\,4!}. \tag{51}
\]
Writing
\(C_{4,+}=s_2w^2+s_3w^3+\cdots\), expansion along the first row gives
\[
\Delta_k=-\frac{25}{2}s_2\det M_{1,1}, \tag{52}
\]
where the explicit universal \(4\times4\) endpoint matrix is recorded in
`current_context/RADIAL_RATIONAL_DESCENT_CRITERION.md`.  The contact
identity says
\[
C_{4,+}=[u_p^{-1/2}(wU)^{1/2}]_{\deg\ge2},
\]
so, with \(t=w^{-1}\),
\[
s_2=[t^{k-1}]
\left(\frac{U}{u_pw^{2k+1}}\right)^{1/2}.
\]
In particular \(s_2=u_4/(2u_5)\) for \(k=2\), while
\(s_2=u_5/(2u_7)-u_6^2/(8u_7^2)\) for \(k=3\).  The contact with the
cube-root coordinate from \(V\) identifies the same coefficient but does
not visibly force \(s_2\ne0\).  Moreover the normalized local ODE
specialization \(u_2=u_3=0\) makes \(\Delta_k=0\).  Therefore all-\(k\)
nonvanishing of (50) is not a formal endpoint consequence; it requires a
global passport/common-root theorem and remains conjectural beyond the
complete \(k\le3\) fibers.

The monomial ideal (49) has six minimal coordinate strata, obtained by
combining \(\{X_6\}\) or \(\{X_0,X_1\}\) with one of
\[
\{X_5,X_4\},\qquad \{X_5,X_3\},\qquad \{X_2,X_3\}. \tag{53}
\]
Conditionally on that factorization, this replaces an undifferentiated
seven-variable problem by six explicit cases for the next nonresonant or
higher-resonant descent step; it does not yet eliminate those cases.

An exact flow audit shows why.  Every one of the six strata still contains
nonzero algebraic Hamiltonian flows.  The low \(d=1\) axis has
\[
Z=z\left(1-\frac{3atw}{4z}\right)^{-1/3},\qquad
W=w\left(1-\frac{3atw}{4z}\right)^{-4/3},
\]
and the commuting low \(d=2,3\) axes have
\[
Z=z,\qquad
W=w\left(1-2tw^2\left(\frac a{z^2}+\frac b{z^3}\right)\right)^{-1/2}.
\]
For a high principal Hamiltonian
\[
H=-\frac a c(zw^k)^c,\qquad 1\le c\le4,
\]
put \(N=5k+2\).  Its exact flow is
\[
\begin{aligned}
Z&=z\left(1-
Nat\,\frac{w^{ck+2}}{z^{5-c}}\right)^{k/N},\\
W&=w\left(1-
Nat\,\frac{w^{ck+2}}{z^{5-c}}\right)^{-1/N}.
\end{aligned} \tag{53a}
\]
These formulas preserve \(z^4w^{-3}dz\wedge dw\) exactly.  Their
binomials have simple divisors, so the nonzero autonomous flows are not
rational in \(K(z,w)\).  This is an exact Kummer obstruction to an
autonomous-flow shortcut, but not yet to a general completion: later
Hamiltonians can alter the time map.

The endpoint coordinates give a more conceptual description of four
reduced strata.  On \(Y_0=0,Y_2=0,Y_3=0\), respectively, the matched
Hamiltonians are
\[
H_1=-\frac{P_0^2-x^2}{4},\qquad
H_2=-\frac{Q_0-x^2y}{3},\qquad
H_3=-\frac{P_0-x}{2}. \tag{53b}
\]
Hence (45)--(46) reduce the strata
\[
\begin{array}{c|c}
(X_6=0,\ X_2=X_3=0)&H_1+H_3\\
(X_0=X_1=0,\ X_4=X_5=0)&H_2+H_4\\
(X_0=X_1=0,\ X_3=X_5=0)&H_4\\
(X_0=X_1=0,\ X_2=X_3=0)&H_3+H_4.
\end{array}
\]
The two remaining strata, containing \(d=1\) and \(d=2\), retain the
larger graph \(Y_2=\kappa_kY_0^2\).  No unconditional rational-descent
identity now available eliminates these six pieces.  Conditional on
original-plane integrality, theorem (43a) eliminates all of them at once.
Thus the high-leverage target is finiteness of the selected graph, not
case-by-case Gröbner elimination on (53).

Two tiny exact calculations sharpen this proposal.  For \(k=1\), the unique
normalized outer point is
\[
U=1+w+\frac6{25}w^2+\frac9{250}w^3.
\]
For \(k=2\), the two normalized points form one quadratic factor over
\(\mathbf F_{32003}\).  Writing
\[
s^2+9432s-2820=0,
\]
one has
\[
\begin{aligned}
u_2&=6033+5035s,&u_3&=-12856+821s,\\
u_4&=12547-1635s,&u_5&=-8440+12404s.
\end{aligned}
\]
Exact ranks over these complete coefficient fields give, for both \(k=1\)
and \(k=2\), the same kernel weights as for \(k=3\):
\[
(1,1,2,2,3,3,4).
\]
There is no kernel at any later deficit.  Thus the tempting extrapolation
“two copies of \(1,\ldots,k\), followed by \(k+1\)” is false; its agreement
at \(k=3\) was accidental.  The stable cutoff \(d=4=m+n-1\) instead matches
the resonance range \(c=m+n-d>0\) in (7).

The nonlinear reconnaissance is stronger still.  The \(k=1\) and \(k=2\)
complete lower consistency ideals are origin-only, of quotient dimensions
243 and 225.  More importantly, the prefix of weights at most eight is
already origin-only:
\[
\begin{array}{c|ccc}
k&1&2&3\\ \hline
\dim(\text{weight}\le8\text{ quotient})&255&247&380.
\end{array}
\]
For \(k=3\), dimension 380 holds over both rational points and the cubic
factor.  In every entry the reductions
\[
X_0^{32}=\cdots=X_6^{32}=0
\]
are exact.  For \(k\ge2\) this prefix consists of the same 19 equations,
with weight multiplicities \(2,2,4,5,6\) in weights \(4,5,6,7,8\).
The smallest observed pure powers in its reduced bases follow the
weight-descending pattern
\[
X_6^3,\qquad X_4^{\le4},X_5^{\le4},\qquad
X_2^{\le6},X_3^{\le6},\qquad X_0^{\le12},X_1^{\le12}.
\]

This identifies a concrete finite-jet theorem to prove: after using the
outer ODE and the approximate square/cube relation at infinity, the 19
weight-\(\le8\) equations should stabilize over the universal \(k\ge2\)
Hurwitz algebra and have irrelevant radical.  The remaining algebraic task
is to express the seven pure-power certificates over that universal outer
jet ring and show that their leading determinants are units, ideally from
the squarefreeness/passport rather than by enumerating covers.

What remains genuinely open is nonlinear.  The index of (7) can control
the number and weights of transverse parameters and consistency equations,
but it does not by itself show that the resulting weighted-homogeneous ideal
has only the origin for every \((m,n,k)\).  A uniform origin-only theorem for
these lower weighted fibers, or a separate all-degree infinity reduction,
is still required before any conclusion about \(JC(2)\).

The exact outer identities, passports, Riemann--Hurwitz checks, and the four
Catalan counts are reproduced by

```sh
.venv/bin/python route_bd_universal_outer_edge.py
.venv/bin/python route_bd_universal_belyi_deck_rigidity.py
.venv/bin/python route_bd_universal_lattice_change.py
.venv/bin/python route_bd_universal_radial_kernel_theorem.py
.venv/bin/python route_bd_universal_hamiltonian_gauge.py
.venv/bin/python route_bd_universal_hamiltonian_filtration_limits.py
.venv/bin/python route_bd_universal_hamiltonian_endpoint_squares.py
.venv/bin/python route_bd_radial_rational_descent_criterion.py
.venv/bin/python route_bd_universal_radial_rank.py
.venv/bin/python route_bd_universal_radial_consistency.py
```
