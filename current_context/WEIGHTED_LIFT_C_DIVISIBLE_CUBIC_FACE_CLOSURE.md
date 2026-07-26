# Closure of every \(C\)-divisible cubic target face

Date: 25 July 2026

## Outcome

Let \(F=(A,B,C)\) be the generic-degree-six Gallagher weighted lift
and let \(U(A,B,C)\) be the second-subduction polynomial from
`WEIGHTED_LIFT_FIRST_NONLINEAR_CUSP_SUBDUCTION.md`.  Let
\[
Q_2=\alpha A^2+\beta AB+\chi B^2+\mu AC+\nu BC+\rho C^2
\tag{1}
\]
be a nonzero homogeneous quadratic form.  Then, for every polynomial
graph \(z=g(x,y)\) and every target-linear form \(L\),
\[
\left((U+L)\circ F,\ (CQ_2)\circ F\right)\big|_{z=g}
\tag{2}
\]
does not have nonzero constant Jacobian.

Thus none of the six cubic target faces
\[
A^2C,\quad ABC,\quad B^2C,\quad AC^2,\quad BC^2,\quad C^3
\tag{3}
\]
provides a polynomial-graph descent, even when arbitrary coefficients
on the same \(C\)-divisible cubic face are allowed to interact.

There are only two possible resonance families.  If \(\alpha\ne0\),
the family is
\[
m=7k-2,\qquad
g_m=c\,x^{3k-2}y^{4k},\qquad k\ge1,
\tag{4}
\]
but its characteristic completion forces a forbidden \(x^1\)-term.
If \(\alpha=0,\beta\ne0\), the family is
\[
m=25k+18,\qquad
g_m=c\,x^{18k+13}y^{7k+5},\qquad k\ge0.
\tag{5}
\]
When \(\chi\ne0\), its completion forces a negative power of the
infinity-chart coordinate \(t\).  When \(\chi=0\), the ray completes
polynomially, but the fixed part of the graph leaves a nonzero
weighted-Euler defect.  Every other \(C\)-divisible cubic face is
nonresonant.

This closes one of the two cubic layers singled out by
`WEIGHTED_LIFT_ALL_QUADRATIC_PIVOT_CLOSURE.md`.  It does not treat the
binary cubic face in \(A,B\), whose characteristic polynomial has
degree three.

## 1. The first characteristic block

Put
\[
u=1+xy,\qquad t=\frac ux=y+\frac1x,\qquad
\gamma=1+a\,xy+x^2g(x,y),\qquad a=-\frac{57}{34}.
\tag{6}
\]
Up to nonzero constants, the relevant highest seed sectors are
\[
\begin{aligned}
M&=x^{-5}u^{20}\gamma^{17}
  =x^{15}t^{20}\gamma^{17},\\
A_{\rm h}&=q_6x^{-2}u^6\gamma^4
  =q_6x^4t^6\gamma^4,\\
B_{\rm h}&=p_5x^{-1}u^5\gamma^4
  =p_5x^4t^5\gamma^4,\\
C_{\rm h}&=x\gamma,
\end{aligned}
\tag{7}
\]
where \(p_5=-3/46\) and \(q_6=-5/92\).
Consequently
\[
C_{\rm h}
(\alpha A_{\rm h}^2+\beta A_{\rm h}B_{\rm h}
 +\chi B_{\rm h}^2)
=x^9t^{10}\gamma^9P(t),
\tag{8}
\]
with
\[
P(t)=\alpha q_6^2t^2+\beta p_5q_6t+\chi p_5^2.
\tag{9}
\]

Logarithmic differentiation shows that the highest Jacobian vanishes
exactly when
\[
x\left(-\frac{10}{t}+17\frac{P'}P\right)\gamma_x
-18\gamma_t
+\left(-\frac{30}{t}+15\frac{P'}P\right)\gamma=0.
\tag{10}
\]
The equation preserves each \(x\)-Laurent sector.  A sector
\(\gamma=x^I\phi(t)\) has the one-dimensional solution space
\[
\phi(t)=c\,t^{-(5I+15)/9}P(t)^{(17I+15)/18}.
\tag{11}
\]
If \(d=\deg P\) and the leading \(t\)-exponent is \(J\), then
\[
J=-\frac{5I+15}{9}
  +d\,\frac{17I+15}{18}.
\tag{12}
\]
This classifies the whole three-parameter block by the single integer
\(d=2,1,0\).

## 2. Closure of the \(d=2\) resonance

If \(\alpha\ne0\), equation (12) is
\[
3J=4I.
\tag{13}
\]
A highest graph monomial enters \(\gamma\) with
\(I=i+2\), \(J=m-i\).  Hence all possible resonances are precisely
\[
I=3k,\qquad J=4k,\qquad m=7k-2,\qquad k\ge1,
\tag{14}
\]
which is (4).

Normalize the leading coefficient of \(P\).  Equation (11) starts
with
\[
\gamma_I=cx^It^J(1+O(t^{-1})).
\tag{15}
\]
After returning to \(t=y+x^{-1}\), its highest-\(y\) monomial at
\(x\)-exponent one is
\[
c\binom{4k}{3k-1}x\,y^{k+1}\ne0.
\tag{16}
\]
Every lower \(t\)-power in (15) has smaller \(y\)-degree when it
reaches \(x\)-exponent one.  A different resonant sector cannot
cancel (16): along (13), the leading weight
\(I+J=7I/3\) is strictly increasing in \(I\), while the output
\(y\)-degree at \(x^1\) is \(J-I+1=I/3+1\).  Lower sectors therefore
produce lower \(y\)-degree, and a higher sector is absent by the
choice of the highest graph term.

But every graph contribution to \(\gamma\) is divisible by \(x^2\),
and its fixed part has only \(1\) and \(axy\).  Thus (16) is
impossible.  It occurs at ordinary-filtration drop
\[
(I+J)-\bigl(1+(k+1)\bigr)=6k-2.
\tag{17}
\]
The first lower seed sector occurs only at drop
\[
m+4=7k+2.
\tag{18}
\]
The adjacent \(ABC\) and \(B^2C\) sectors have already been included
in \(P\), while the \(C^2(A,B)\) block begins still later, at gap
\(3m+15\).  Hence no omitted sector reaches (16).

## 3. Closure of the \(d=1\) resonance

Suppose \(\alpha=0,\beta\ne0\).  Equation (12) becomes
\[
7I=18J+15.
\tag{19}
\]
Its graph solutions are exactly
\[
I=18k+15,\qquad J=7k+5,\qquad
m=25k+18,\qquad k\ge0,
\tag{20}
\]
giving (5).  The characteristic exponents in (11) are
\[
r=-10k-10,\qquad s=17k+15,\qquad J=r+s.
\tag{21}
\]

If \(\chi\ne0\), normalize \(P(t)=p_1(t+d)\), \(d\ne0\).
The characteristic sector is, up to a nonzero scalar,
\[
\gamma_I=cx^It^J(1+d/t)^s.
\tag{22}
\]
Its \(t^{-1}\)-coefficient is
\[
c\binom{s}{J+1}d^{J+1}
=c\binom{17k+15}{7k+6}d^{7k+6}\ne0.
\tag{23}
\]
For a polynomial graph, the coefficient of every \(x\)-power in
\[
\gamma(x,t)=1-a+axt+x^2g(x,t-x^{-1})
\tag{24}
\]
is a polynomial in \(t\).  It cannot contain \(t^{-1}\).
Because (10) preserves the \(x\)-Laurent sectors, another sector
cannot cancel (23).  The obstruction is only \(J+1=7k+6\) steps
below the leading term, before the first lower seed sector at
\(m+4=25k+22\).

If \(\chi=0\), the ray instead completes polynomially:
\[
\gamma_{\rm ray}
=c\,x^{I-J}u^J
=c\,x^{11k+10}u^{7k+5}.
\tag{25}
\]
The corresponding weighted-Euler operator is
\[
\mathcal L_{ABC}
=7x\partial_x-11u\partial_u-15.
\tag{26}
\]
On the fixed graph part it leaves
\[
\mathcal L_{ABC}(1+a(u-1))
=\frac{741}{17}xy+\frac{117}{34}.
\tag{27}
\]
Terms on the only relevant source diagonal are polynomials in
\(xy\) beginning in degree two.  If a finite nonzero sum of them
were present, its highest term \((xy)^n\) would have coefficient
\(-11n-15\ne0\) under (26).  Descending induction kills the entire
sum, so it cannot cancel (27).  This fixed defect occurs at drop
\(m\), again before the first lower seed sector.

If \(d=0\), equation (12) gives
\[
J=-\frac{5I+15}{9}<0,
\tag{28}
\]
so the \(B^2C\) face has no graph resonance.

## 4. The \(C^2(A,B)\) block and \(C^3\)

For the next block, put
\[
R(t)=\mu q_6t+\nu p_5.
\tag{29}
\]
Its highest sector is
\[
C_{\rm h}^2(\mu A_{\rm h}+\nu B_{\rm h})
=x^6t^5\gamma^6R(t).
\tag{30}
\]
The characteristic equation is
\[
x\left(-\frac{35}{t}+17\frac{R'}R\right)\gamma_x
-12\gamma_t
+\left(-\frac{45}{t}+15\frac{R'}R\right)\gamma=0,
\tag{31}
\]
and a sector \(x^I\phi(t)\) is
\[
\phi(t)=c\,t^{-(35I+45)/12}
R(t)^{(17I+15)/12}.
\tag{32}
\]
If \(\mu\ne0\), its leading exponent is
\[
J=-\frac{3I+5}{2}<0.
\tag{33}
\]
If \(\mu=0,\nu\ne0\), it is even smaller:
\[
J=-\frac{35I+45}{12}<0.
\tag{34}
\]
Thus neither \(AC^2\) nor \(BC^2\), nor any mixture of them, has a
graph resonance.

Finally, the \(C^3\) master operator is
\[
-60x\partial_x-66u\partial_u-60.
\tag{35}
\]
Its diagonal coefficient on a possible leading graph monomial
\(x^Iy^J\) is
\[
-60I-6J-60<0,
\tag{36}
\]
so this last face is also nonresonant.

## 5. Degree separation and constant graphs

For a nonconstant graph of degree \(m\), the six target degrees are
\[
\begin{array}{c|cccccc}
\text{face}&A^2C&ABC&B^2C&AC^2&BC^2&C^3\\ \hline
\deg&9m+39&9m+38&9m+37&6m+24&6m+23&3m+9.
\end{array}
\tag{37}
\]
This order selects the first nonzero characteristic block.  On both
resonant rays, the obstructions in Sections 2 and 3 occur before the
first lower seed or lower cubic block.  Moreover,
\(\deg U_0=17m+69\), whereas every target-linear \(L\) has degree at
most \(4m+18\).  For any selected cubic face, the gap from
\(J(U,CQ_2)\) to \(J(L,CQ_2)\) is at least
\[
13m+51.
\tag{38}
\]
On the \(d=2\) ray this is \(91k+25>6k-2\).  On the \(d=1\) ray
it is \(325k+285\), larger than both \(7k+6\) and
\(m=25k+18\).  Therefore \(J(L,CQ_2)\) enters strictly below every
displayed obstruction and cannot repair it.

It remains to check constant graphs.  Write
\[
h=ay+z_0x,\qquad C_0=x^2h,\qquad
U_0=\theta x^{32}y^{20}h^{17}.
\tag{39}
\]
Each cubic face is, up to a nonzero scalar, \(y^rC_0^s\), with
\[
(r,s)=(12,9),(11,9),(10,9),(6,6),(5,6),(0,3).
\tag{40}
\]
Direct differentiation gives
\[
\begin{aligned}
J(U_0,y^rC_0^s)
={}&\theta x^{31+2s}y^{19+r}h^{16+s}\\
&\quad\cdot
\bigl((32r-42s)ay+(49r-60s)z_0x\bigr).
\end{aligned}
\tag{41}
\]
For the six pairs in (40), the first coefficient is respectively
\[
6,\ -26,\ -58,\ -60,\ -92,\ -126,
\tag{42}
\]
and \(a\ne0\).  Hence every selected highest form is nonzero,
including when \(z_0=0\).  Their degrees are distinct, and the
linear correction is lower, completing the constant-graph case.

The accompanying exact verifier is
`verify_weighted_lift_c_divisible_cubic_face_closure.py`.
