# Exact degree-six ternary source-boundary Wronskian closure

Date: 25 July 2026

## Outcome

Consider the degree-six homogeneous ternary target faces whose least
\(C\)-tier is
\[
CB^5
\qquad\text{or}\qquad
CAB^4.
\tag{1}
\]
The two graph-compatible pure characteristics left by the highest
equation are
\[
\begin{array}{c|c|c|c|c|c}
N&\ell&d&I&J&m\\ \hline
5&1&0&9&0&7\\
5&1&1&30&15&43.
\end{array}
\tag{2}
\]

The naive top Euler equation on the source boundary is not used.
Instead, this note retains the full seed on that boundary and
includes every degree-six target monomial having the same source
\(x\)-exponent.  Those monomials are exactly
\[
\begin{aligned}
\beta=-4:\quad&CB^5,\ C^2A^2B^2,\\
\beta=-5:\quad&CAB^4,\ C^2A^3B.
\end{aligned}
\tag{3}
\]
For an arbitrary coefficient of the second monomial in either row,
the exact boundary Wronskian has a nonzero highest \(u\)-coefficient.
Thus neither characteristic can extend to a polynomial graph with
constant restricted Jacobian.

This is a rigorous closure of the first two ternary pure faces.  It
does not assert the previously proposed all-degree pure-face Euler
argument.

## 1. Exact full-seed boundary functions

Put
\[
u=1+xy,\qquad
\gamma=1-\frac{57}{34}(u-1)+x^2g
\]
and let
\[
f(u)=\gamma\big|_{\text{source boundary}},
\qquad
f(1)=1,\qquad f'(1)=-\frac{57}{34}.
\tag{4}
\]
In particular,
\[
L:=\deg f\ge1.
\tag{5}
\]
Let \(p(w),q(w)\) be the exact Gallagher seed polynomials and let
\(\mathcal N(w,\gamma)\) be the exact 77-term second-subduction
numerator.  Since \(w=u\gamma\), define
\[
\begin{aligned}
\mathsf A(u,f)
&=\frac{q(uf)+uf^2}{f^2},\\
\mathsf B(u,f)
&=\frac{p(uf)+f}{f},\\
\mathsf H(u,f)
&=\frac{\mathcal N(uf,f)}{f^5}.
\end{aligned}
\tag{6}
\]
These are polynomials in \(u,f\).  On the source boundary,
\[
U=x^{-5}\mathsf H,\qquad
A=x^{-2}\mathsf A,\qquad
B=x^{-1}\mathsf B,\qquad
C=xf.
\tag{7}
\]

The exact seed tops give
\[
\begin{aligned}
\deg_u\mathsf A(u,f(u))&=6+4L,\\
\deg_u\mathsf B(u,f(u))&=5+4L,\\
\deg_u\mathsf H(u,f(u))&=20+17L.
\end{aligned}
\tag{8}
\]
If \(c\ne0\) is the leading coefficient of \(f\), the corresponding
leading coefficients are
\[
q_6c^4,\qquad p_5c^4,\qquad\theta c^{17},
\tag{9}
\]
respectively.  The exact support inequalities make each top unique
for every \(L\ge1\).

## 2. Exhaustion of same-boundary counterterms

For a target monomial \(A^aB^bC^c\) of total degree six, its source
\(x\)-exponent is
\[
\beta=-2a-b+c=6-3a-2b.
\tag{10}
\]
Consequently
\[
\begin{aligned}
\beta=-4&\iff 3a+2b=10
&&\iff (a,b,c)=(0,5,1),(2,2,2),\\
\beta=-5&\iff 3a+2b=11
&&\iff (a,b,c)=(1,4,1),(3,1,2).
\end{aligned}
\tag{11}
\]
This proves the exhaustion in (3); no other degree-six target
coefficient can enter either boundary Wronskian.

After normalizing the coefficient of the least-\(C\) monomial, the
two exact boundary target functions are therefore
\[
\begin{aligned}
\mathsf K_4
&=f\mathsf B^5
+\lambda f^2\mathsf A^2\mathsf B^2,\\
\mathsf K_5
&=f\mathsf A\mathsf B^4
+\mu f^2\mathsf A^3\mathsf B.
\end{aligned}
\tag{12}
\]
Their two summands have degrees
\[
\begin{array}{c|cc}
&\text{least-\(C\) term}&\text{counterterm}\\ \hline
\mathsf K_4&25+21L&22+18L\\
\mathsf K_5&26+21L&23+18L.
\end{array}
\tag{13}
\]
The gap is \(3+3L>0\).  Hence \(\lambda,\mu\) cannot change either
leading coefficient:
\[
\operatorname{lc}(\mathsf K_4)=p_5^5c^{21},
\qquad
\operatorname{lc}(\mathsf K_5)=q_6p_5^4c^{21}.
\tag{14}
\]

## 3. The exact Wronskian obstruction

For boundary functions \(x^\alpha H(u)\) and \(x^\beta K(u)\),
the \((x,y)\)-Jacobian is
\[
J_{x,y}\bigl(x^\alpha H,x^\beta K\bigr)
=x^{\alpha+\beta}
\left(
\alpha HK'-\beta H'K
\right).
\tag{15}
\]

### 3.1. The \(CB^5\) face

Here \(\alpha=-5,\beta=-4\), so the exact boundary coefficient is
\[
\mathsf W_4=-5\mathsf H\mathsf K_4'
+4\mathsf H'\mathsf K_4.
\tag{16}
\]
Its highest \(u\)-degree is
\[
44+38L,
\tag{17}
\]
and its coefficient is
\[
\boxed{
\theta p_5^5c^{38}(-45-37L)\ne0.
}
\tag{18}
\]
Indeed,
\[
-5(25+21L)+4(20+17L)=-45-37L.
\]
The counterterm in (12) is too low to affect this coefficient.

### 3.2. The \(CAB^4\) face

Here \(\alpha=\beta=-5\), so
\[
\mathsf W_5
=5\left(\mathsf H'\mathsf K_5
-\mathsf H\mathsf K_5'\right).
\tag{19}
\]
Its highest \(u\)-degree is
\[
45+38L,
\tag{20}
\]
and its coefficient is
\[
\boxed{
5\theta q_6p_5^4c^{38}(-6-4L)\ne0.
}
\tag{21}
\]
Again, the same-boundary counterterm is strictly lower.

For the two characteristics in (2), the graph-degree bounds give
\[
1\le L\le4
\qquad\text{and}\qquad
1\le L\le22,
\tag{22}
\]
respectively, although (18) and (21) are nonzero for every
\(L\ge1\).  This completes both degree-six boundary closures.

The accompanying exact verifier is
`verify_weighted_lift_degree_six_ternary_boundary_wronskian_closure.py`.
