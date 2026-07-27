# Closure of every cubic second target pivot

Date: 25 July 2026

> **Correction.**  The pure-face boundary-Euler subargument used below
> is not the full exact source-boundary equation after \(t=u/x\).
> Moreover, in the arbitrary-lower-tier theorem a lower \(B^2\) term
> can enter the same first-lower sector as the pure \(ABC\) face.  The
> full cubic conclusion stated below is therefore not currently proved
> on the \(ABC+B^2\) chain; it also inherits the unresolved lower
> quadratic \(AC+B\) chain.  The descending, mixed negative-tail,
> nonresonance, and constant-graph certificates remain valid.

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift,
and let \(U(A,B,C)\) be the second-subduction polynomial from
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.  Let
\[
V=Q_3(A,B,C)+Q_{\le2}(A,B,C),
\qquad Q_3\ne0,
\tag{1}
\]
where \(Q_3\) is homogeneous cubic and \(Q_{\le2}\) is arbitrary of
target degree at most two.  Let \(R_{\le2}\) be another arbitrary
target polynomial of degree at most two.  Then no polynomial graph
\[
z=g(x,y)
\tag{2}
\]
makes
\[
\left((U+R_{\le2})\circ F,\ V\circ F\right)\big|_{z=g}
\tag{3}
\]
have nonzero constant Jacobian.

Thus every cubic second target coordinate, with arbitrary quadratic
and affine lower terms, is excluded.  The proof is a target-Newton
classification rather than a coefficient search:

- the binary cubic face in \(A,B\) reduces to four characteristic
  degrees \(d=3,2,1,0\);
- the \(C\)-divisible face \(C Q_2(A,B,C)\) has only two resonant
  subfaces, both of which close;
- terms of lower target degree interleave with the \(C^2(A,B)\) and
  \(C^3\) faces, but an exact graph-degree staircase shows that they
  enter strictly after every surviving defect;
- constant graphs have ten separated, nonzero cubic monomial
  Jacobians.

The new binary ray is the \(A^2B\)-leading family
\[
m=73k+26,\qquad
g_m=c\,x^{24k+7}y^{49k+19},
\qquad k\ge0,
\tag{4}
\]
which forces
\[
c\binom{49k+19}{24k+8}
x\,y^{25k+11}.
\tag{5}
\]
The \(AB^2\)-leading face repeats the ray later encountered by
\(A^2C\):
\[
m=7k+5,\qquad
g_m=c\,x^{3k+1}y^{4k+4},
\qquad k\ge0.
\tag{6}
\]

This is not an arbitrary nonlinear-target theorem.  Quartic and
higher target Newton faces remain outside the result.

## 1. A characteristic formula for every cubic face

Put
\[
u=1+xy,\qquad t=\frac ux=y+\frac1x,\qquad
\gamma=1+a\,xy+x^2g(x,y),\qquad a=-\frac{57}{34}.
\tag{7}
\]
Up to a nonzero scalar, the highest sector of \(U\) is
\[
M=x^{-5}u^{20}\gamma^{17}
=x^{15}t^{20}\gamma^{17}.
\tag{8}
\]
The highest seed sectors of the target coordinates are
\[
A_{\rm h}=q_6x^4t^6\gamma^4,\qquad
B_{\rm h}=p_5x^4t^5\gamma^4,\qquad
C_{\rm h}=x\gamma,
\tag{9}
\]
where
\[
p_5=-\frac3{46},\qquad q_6=-\frac5{92}.
\tag{10}
\]

Consider a homogeneous target face with \(n\) factors from
\(\{A,B\}\), \(c\) factors \(C\), and \(n+c=3\).  Its combined
highest sector has the form
\[
N=x^{4n+c}t^{5n}\gamma^{4n+c}P(t),
\qquad \deg P\le n.
\tag{11}
\]
Exact logarithmic differentiation shows that \(J(M,N)=0\) is
equivalent to
\[
\begin{aligned}
x\left(
\frac{5n-20c}{t}+17\frac{P'}P
\right)\gamma_x
{}-(8n+2c)\gamma_t\\
{}+\left(
-\frac{5n+20c}{t}+15\frac{P'}P
\right)\gamma=0.
\end{aligned}
\tag{12}
\]
A fixed \(x\)-Laurent sector \(\gamma=x^I\phi(t)\) therefore has the
unique formal solution
\[
\phi(t)=
t^rP(t)^s,
\tag{13}
\]
where
\[
r=\frac{(5n-20c)I-(5n+20c)}{8n+2c},
\qquad
s=\frac{17I+15}{8n+2c}.
\tag{14}
\]
If \(d=\deg P\) and the leading term at \(t=\infty\) is \(t^J\), then
\[
J=r+ds.
\tag{15}
\]
Equations (12)--(15) classify every possible cubic resonance.

## 2. The binary cubic face

Write
\[
\begin{aligned}
Q_{3,AB}={}&
\alpha A^3+\beta A^2B+\chi AB^2+\delta B^3,\\
P_3(t)={}&
\alpha q_6^3t^3+\beta q_6^2p_5t^2
+\chi q_6p_5^2t+\delta p_5^3.
\end{aligned}
\tag{16}
\]
Here \((n,c)=(3,0)\).  Formula (12) becomes
\[
x\left(\frac{15}{t}+17\frac{P_3'}{P_3}\right)\gamma_x
-24\gamma_t
+\left(-\frac{15}{t}+15\frac{P_3'}{P_3}\right)\gamma=0,
\tag{17}
\]
and
\[
r=\frac{5I-5}{8},\qquad
s=\frac{17I+15}{24}.
\tag{18}
\]

Let \(d=\deg P_3\); equivalently, \(d\) records the first nonzero
coefficient in \((\alpha,\beta,\chi,\delta)\).  The complete list
from (15) is
\[
\begin{array}{c|c|c|c}
d&J(I)&(I,J)&m\\ \hline
3&(11I+5)/4&(4k+1,\,11k+4)&15k+3,\ k\ge1\\
2&(49I+15)/24&(24k+9,\,49k+19)&73k+26,\ k\ge0\\
1&4I/3&(3k+3,\,4k+4)&7k+5,\ k\ge0\\
0&5(I-1)/8&(8k+9,\,5k+5)&13k+12,\ k\ge0.
\end{array}
\tag{19}
\]
As usual, \(I=i+2\), \(J=m-i\), where
\(g_m=cx^iy^J\).

### 2.1. The three descending faces

For \(d=3,2,1\), one has \(J>I\).  Normalize the leading coefficient
of \(P_3\).  Formula (13) starts as
\[
\gamma_I=cx^It^J(1+O(t^{-1})).
\tag{20}
\]
After \(t=y+x^{-1}\), its highest-\(y\) term with \(x\)-exponent one
is
\[
c\binom{J}{I-1}x\,y^{J-I+1}.
\tag{21}
\]
It is nonzero and cannot lie in
\(\gamma=1+a xy+x^2g\).  Lower powers of \(t\) have smaller
\(y\)-degree when they reach \(x\)-exponent one and cannot cancel it.

There is also no cancellation from another \(x\)-sector.  On the
three rows of (19), the leading weight \(W(I)=I+J(I)\) has slopes
\[
\frac{15}{4},\qquad\frac{73}{24},\qquad\frac73,
\tag{22}
\]
whereas the source diagonal \(D(I)=I-J(I)\) has slopes
\[
-\frac74,\qquad-\frac{25}{24},\qquad-\frac13.
\tag{23}
\]
A lower resonant sector therefore has larger source diagonal, and
its descending \(t\)-terms only increase that diagonal.  A higher
sector would violate top-weight maximality; a nonresonant sector has
no free leading coefficient.  Hence (21) is the complete obstruction.

Explicitly, the three forbidden terms and their filtration drops are
\[
\begin{array}{c|c|c}
d&\text{forbidden monomial}&\text{drop}\\ \hline
3&
c\binom{11k+4}{4k}x\,y^{7k+4}&8k\\
2&
c\binom{49k+19}{24k+8}x\,y^{25k+11}&48k+16\\
1&
c\binom{4k+4}{3k+2}x\,y^{k+2}&6k+4.
\end{array}
\tag{24}
\]
The next seed sector enters after \(m+4\) degrees.  In all three
rows,
\[
8k<m+4,\qquad
48k+16<m+4,\qquad
6k+4<m+4,
\tag{25}
\]
respectively.

### 2.2. The \(B^3\)-face

For \(d=0\), the characteristic ray completes to
\[
\gamma_{\rm ray}
=c\,x^{3k+4}u^{5k+5}.
\tag{26}
\]
This is the old \(B\)-ray because
\[
J(U,B^3)=3B^2J(U,B).
\tag{27}
\]
The fixed part of \(\gamma\) leaves
\[
\left(5x\partial_x-3u\partial_u-5\right)
(1+a(u-1))
=\frac{228}{17}xy+\frac1{34}.
\tag{28}
\]
The defect appears at drop \(m\), before the next seed sector.

Thus every nonzero binary cubic face is closed, uniformly in all
coefficients below its leading \(d\)-face.

## 3. The \(C\)-divisible cubic faces

The detailed face proof also appears in
`WEIGHTED_LIFT_C_DIVISIBLE_CUBIC_FACE_CLOSURE.md`.  The characteristic
calculation is included here so that the all-cubic composition is
self-contained.

### 3.1. The \(C Q_2(A,B)\)-face

Put
\[
P_2(t)=
\alpha q_6^2t^2+\beta p_5q_6t+\chi p_5^2.
\tag{29}
\]
For \(C(\alpha A^2+\beta AB+\chi B^2)\), one has
\((n,c)=(2,1)\), and (12) is
\[
x\left(-\frac{10}{t}+17\frac{P_2'}{P_2}\right)\gamma_x
-18\gamma_t
+\left(-\frac{30}{t}+15\frac{P_2'}{P_2}\right)\gamma=0.
\tag{30}
\]
The sector solution is
\[
\phi(t)=
t^{-(5I+15)/9}P_2(t)^{(17I+15)/18}.
\tag{31}
\]
The three possible degrees of \(P_2\) give
\[
\begin{array}{c|c|c|c}
d&J(I)&(I,J)&m\\ \hline
2&4I/3&(3k+3,\,4k+4)&7k+5\\
1&(7I-15)/18&(18k+15,\,7k+5)&25k+18\\
0&-(5I+15)/9&\text{none}&\text{none}.
\end{array}
\tag{32}
\]

The \(d=2\) row repeats the third binary-cubic row and forces
\[
c\binom{4k+4}{3k+2}x\,y^{k+2}
\tag{33}
\]
at drop \(6k+4\).

For \(d=1\), normalize
\(P_2(t)=p_1(t+\eta)\).  Formula (31) becomes
\[
\phi(t)=
t^{7k+5}(1+\eta/t)^{17k+15}.
\tag{34}
\]
If \(\eta\ne0\), the coefficient of \(t^{-1}\) is
\[
\binom{17k+15}{7k+6}\eta^{7k+6}\ne0.
\tag{35}
\]
Every fixed \(x\)-coefficient of
\[
\gamma(x,t)=1-a+axt+x^2g(x,t-x^{-1})
\tag{36}
\]
is polynomial in \(t\), so (35) is impossible.  The characteristic
equation has coefficients only in \(t\), hence distinct \(x\)-Laurent
sectors cannot cancel it.  With the grading
\(\operatorname{wt}(x^rt^s)=r+s\), the obstruction occurs at drop
\(7k+6\), before the first lower target tier at drop
\[
m+2=25k+20.
\tag{37}
\]

If \(\eta=0\), the ray instead completes to
\[
\gamma_{\rm ray}
=c\,x^{11k+10}u^{7k+5}.
\tag{38}
\]
The normalized \(ABC\) operator is
\[
\mathcal L_{ABC}
=7x\partial_x-11u\partial_u-15,
\tag{39}
\]
and
\[
\mathcal L_{ABC}(1+a(u-1))
=\frac{741}{17}xy+\frac{117}{34}.
\tag{40}
\]
No graph term on the zero diagonal can cancel (40), since the largest
\(x^ny^n\), \(n\ge2\), has coefficient \(-11n-15\).

The \(d=0\), or \(B^2C\), diagonal coefficient is
\[
-10I-18J-30<0,
\tag{41}
\]
so it has no resonant ray.

### 3.2. The \(C^2(A,B)\)- and \(C^3\)-faces

For
\[
C^2(\mu A+\nu B)
\tag{42}
\]
one has \((n,c)=(1,2)\).  If \(\mu\ne0\), (15) gives
\[
J=-\frac{3I+5}{2}<0.
\tag{43}
\]
If \(\mu=0,\nu\ne0\), it gives
\[
J=-\frac{35I+45}{12}<0.
\tag{44}
\]
Neither can be the nonnegative \(t\)-degree of a leading graph
sector.  For \(C^3\), formula (14) gives
\[
J=-10(I+1)<0.
\tag{45}
\]
Thus the remaining cubic faces are nonresonant.

## 4. Exact composition with arbitrary lower target terms

The subtle point is that target degree alone does not order all
restricted forms: for example, a quadratic \(A^2\) can dominate a
cubic \(AC^2\).  The exact graph-degree staircase resolves this.
For a nonconstant graph of degree \(m\), the target monomial degrees
are strictly ordered as follows:
\[
\begin{array}{c|c}
\text{target face}&\text{degrees}\\ \hline
A^3,A^2B,AB^2,B^3&
12m+54,\ 12m+53,\ 12m+52,\ 12m+51\\
A^2C,ABC,B^2C&
9m+39,\ 9m+38,\ 9m+37\\
A^2,AB,B^2&
8m+36,\ 8m+35,\ 8m+34\\
AC^2,BC^2&
6m+24,\ 6m+23\\
AC,BC&
5m+21,\ 5m+20\\
A,B&
4m+18,\ 4m+17\\
C^3,C^2,C&
3m+9,\ 2m+6,\ m+3.
\end{array}
\tag{46}
\]
Every entry in a row exceeds the next entry, and the last entry of
each row exceeds the first entry of the next row for all \(m\ge1\).
The same order holds for their Jacobians with \(U\), because the
common degree \(\deg U_0-2=17m+67\) is added.

If a binary cubic term is present, its face leads.  The first
\(C\)-cubic Jacobian lies below the four binary faces by
\[
3m+15,\quad3m+14,\quad3m+13,\quad3m+12,
\tag{47}
\]
respectively.  These gaps exceed all defects in (24) and (28).

If the binary cubic face vanishes but \(C Q_2(A,B)\ne0\), that face
leads.  The first binary-quadratic lower term enters below its three
faces at gaps
\[
m+3,\qquad m+2,\qquad m+1.
\tag{48}
\]
For \(A^2C\), \(m+3>6k+4\).  For the mixed \(ABC/B^2C\) face,
\(m+2>7k+6\); for pure \(ABC\), \(m+2>m\).  The last face is
nonresonant.

If only \(C^2(A,B)\) or \(C^3\) survives cubically, a lower target
term can lead.  The remaining cases use the already proved
quadratic and linear closures:

- a binary quadratic face lies above \(C^2(A,B)\) by at least
  \(2m+10\), later than each quadratic defect;
- an \(AC/BC\) quadratic face lies above the first possible linear
  face by \(m+3\), later than its mixed \(k+1\) or pure \(m\) defect;
- an \(A/B\) linear face lies above \(C^3\) by \(m+9\) or \(m+8\),
  later than the linear-pivot defects;
- if the leading target is a polynomial in \(C\), its Jacobian is a
  nonzero polynomial multiple of \(J(U,C)\).

This proves that no cubic or lower target tier repairs a defect from
the first nonzero tier.

Finally, adding \(R_{\le2}\) to the first coordinate cannot change
the conclusion.  Its largest possible restricted degree is
\[
8m+36,
\]
whereas
\[
\deg U_0=17m+69.
\tag{49}
\]
Thus every \(J(R_{\le2},V)\) term enters at least \(9m+33\) degrees
below the corresponding \(J(U,V)\) sector, later than every
obstruction above.

## 5. Constant graphs

Let \(g=z_0\), and put
\[
h=ay+z_0x.
\tag{50}
\]
The highest forms are
\[
U_0=\theta x^{32}y^{20}h^{17},\qquad
A_0\sim x^8y^6h^4,\qquad
B_0\sim x^8y^5h^4,\qquad
C_0=x^2h.
\tag{51}
\]
For
\[
R=x^Ay^Bh^C,\qquad S=x^Dy^Eh^F,
\]
direct logarithmic differentiation gives
\[
\frac{J(R,S)}{RS/(xyh)}
=(AE-BD)h+(CE-BF)z_0x+(AF-CD)ay.
\tag{52}
\]
Applying (52) to \(R=U_0\) and the ten cubic target monomials gives,
in descending target degree, the coefficient pairs
\[
\begin{array}{c|c|c}
\text{monomial}&(z_0x,\ ay)\text{ coefficients}&\deg J\\ \hline
A^3&(162,72)&121\\
A^2B&(113,40)&120\\
AB^2&(64,8)&119\\
B^3&(15,-24)&118\\
A^2C&(48,6)&106\\
ABC&(-1,-26)&105\\
B^2C&(-50,-58)&104\\
AC^2&(-66,-60)&91\\
BC^2&(-115,-92)&90\\
C^3&(-180,-126)&76.
\end{array}
\tag{53}
\]
Every form is nonzero because \(a=-57/34\ne0\), and their degrees are
separated in the same staircase as (46).  Lower target terms and
\(R_{\le2}\) cannot cancel the selected top.

## 6. Scope

Combining Sections 2--5 proves
\[
\boxed{
J_{x,y}\left(
(U+R_{\le2})\circ F|_{z=g},\
(Q_3+Q_{\le2})\circ F|_{z=g}
\right)\notin\mathbb C^\times
}
\tag{54}
\]
for every polynomial graph \(g\), every nonzero homogeneous cubic
\(Q_3\), and arbitrary target polynomials \(R_{\le2},Q_{\le2}\) of
degree at most two.

The accompanying exact verifier is
`verify_weighted_lift_all_cubic_pivot_closure.py`.
