# Full boundary-valuation obstruction for homogeneous ternary targets

Date: 25 July 2026

> **Independent-referee correction.**  The first version exhausted
> only target monomials having the same boundary exponent as the
> least-\(C\) face and silently assumed that the graph was regular in
> the \((x,u)\)-chart.  Neither point was justified.  The corrected
> proof starts with the globally lowest block of the full target and
> treats a polar graph valuation \(\rho<0\) separately.  The regular
> calculation in Sections 1--3 and the polar two-endpoint argument in
> Section 8 together repair both gaps.

## Outcome

Let \(V_D(A,B,C)\ne0\) be homogeneous of target degree \(D\ge1\),
and let
\[
\gamma
=1-\frac{57}{34}xy+x^2g(x,y),
\qquad g\in\mathbb C[x,y].
\tag{H}
\]
For the Gallagher weighted lift and its second-subduction coordinate
\(U\),
\[
\boxed{J(U,V_D(A,B,C))\notin\mathbb C^\times.}
\]
Thus every nonzero homogeneous ternary target is excluded on every
polynomial graph.

For a pure least-\(C\) face
\[
C^\ell A^dB^{N-d},
\qquad
N,\ell\ge0,\quad 0\le d\le N,\quad 4N+\ell>0,
\tag{1}
\]
the exact first-lower double pole closes all but one algebraic locus
without using the boundary.  The full boundary-valuation theorem
closes that exceptional locus as a special case.

The first primitive \(I=J\) audit is
\[
(N,\ell,d,I,J)=(13,2,5,15,15),
\tag{2}
\]
with target \(C^2A^5B^8\).  Its two same-boundary counterterms
\(C^3A^7B^5\) and \(C^4A^9B^2\) are included explicitly below.

The key point is to retain those possible poles.  Write the finite
Laurent expansion in the \((x,u)\)-chart as
\[
\gamma(x,u)=x^\rho f(u)+O(x^{\rho+1}),
\qquad f\ne0.
\tag{H1}
\]
The fixed term in (H) gives \(\rho\le0\).  Sections 1--7 treat
\(\rho=0\); Section 8 proves the complementary case \(\rho<0\).

## 1. Exact source-boundary data

Assume first that \(\rho=0\).  Expanding a graph monomial gives
\[
x^2x^iy^j=x^{i+2-j}(u-1)^j.
\tag{H2}
\]
Consequently the \(x^0\)-coefficient has the form
\[
f(u)=\gamma\big|_{\text{source boundary}},
\qquad
f(1)=1,\qquad f'(1)=-\frac{57}{34},
\qquad L=\deg f\ge1.
\tag{3}
\]
Using the exact seed polynomials and the full 77-term numerator
\(\mathcal N\), put
\[
\begin{aligned}
\overline A&=\frac{q(uf)+uf^2}{f^2},\\
\overline B&=\frac{p(uf)+f}{f},\\
\overline U&=\frac{\mathcal N(uf,f)}{f^5}.
\end{aligned}
\tag{4}
\]
If \(c\ne0\) is the leading coefficient of \(f\), exact support
gives
\[
\begin{array}{c|c|c}
&\deg_u&\operatorname{lc}\\ \hline
\overline A&6+4L&q_6c^4\\
\overline B&5+4L&p_5c^4\\
\overline U&20+17L&\theta c^{17}.
\end{array}
\tag{5}
\]
Every non-top exact seed monomial is lower by at least \(L+1\).
This is a symbolic support gap, not a finite-degree observation.  A
lower \(q_k\)- or \(p_k\)-term in \(\overline A\) or \(\overline B\)
has gap
\[
(6-k)(L+1)\quad\hbox{or}\quad(5-k)(L+1),
\]
and the added terms have still larger gaps.  For a support monomial
\(u^if^{\,i+j-5}\) of \(\overline U\), put
\[
a=20-i,\qquad b=22-i-j.
\]
The exact 77-term support has \(a,b\ge0\), with \(b=0\) only at the
top and with \(b=1\) only for \((a,b)=(1,1)\).  Its degree gap is
\[
a+Lb\ge L+1.
\tag{5a}
\]

For the pure face (1), define
\[
q_*=4N+\ell,\qquad
\beta=\ell-N-d,
\tag{6}
\]
and
\[
\overline V_0
=f^\ell\overline A^d\overline B^{N-d}.
\tag{7}
\]
Then
\[
\deg_u\overline V_0
=5N+d+q_*L,
\tag{8}
\]
with leading coefficient
\[
q_6^dp_5^{N-d}c^{q_*}.
\tag{9}
\]

## 2. The globally leading boundary block

For a monomial \(A^aB^bC^c\), define its source-boundary exponent
\[
\beta(a,b,c)=-2a-b+c.
\]
Choose the least exponent occurring with nonzero coefficient in the
full homogeneous target \(V_D\), and within that block choose the
monomial having least \(C\)-exponent.  Write it as (1), so
\(D=N+\ell\).

A monomial in the same target degree and the same globally leading
boundary block must be
\[
\boxed{
C^{\ell+k}A^{d+2k}B^{N-d-3k}
}
\tag{10}
\]
for an integer
\[
0\le k\le\left\lfloor\frac{N-d}{3}\right\rfloor.
\tag{11}
\]
Indeed, equality of the boundary exponent
\(-2a-b+c\), together with equality of total target degree, gives
\[
\Delta a=2k,\qquad
\Delta b=-3k,\qquad
\Delta c=k.
\tag{12}
\]
The \(k\)-th term in (10) is lower in \(u\)-degree than (7) by
\[
\boxed{3k(L+1).}
\tag{13}
\]
Thus the selected coefficient controls the leading \(u\)-term of the
whole globally lowest boundary block for every \(L\ge1\), regardless
of all same-boundary counterterm coefficients.  Terms with larger
boundary exponent occur at later powers of \(x\) and cannot enter
this leading boundary coefficient.

## 3. General leading Wronskian

On the boundary,
\[
U=x^{-5}\overline U,\qquad
V=x^\beta\overline V.
\]
Hence the exact boundary coefficient is
\[
\mathcal W
=-5\overline U\,\overline V'
-\beta\overline U'\,\overline V.
\tag{14}
\]
Put
\[
B_*=17d-3N-22\ell,\qquad
C_*=15d-5N-20\ell.
\tag{15}
\]
Equations (5), (8), and (14) give
\[
\boxed{
\operatorname{lc}(\mathcal W)
=
\theta q_6^dp_5^{N-d}c^{q_*+17}
\left(B_*L+C_*\right)
}
\tag{16}
\]
unless the displayed bracket vanishes.  All counterterms (10) are
too low to affect it.

### 3.1. Cancellation of the bracket cannot persist

Suppose
\[
B_*L+C_*=0.
\tag{16a}
\]
The fixed jets rule out \(f=cu^L\): they would force \(c=1\) and
\(L=-57/34\).  Hence, for some \(1\le\delta\le L\),
\[
f(u)=cu^L+bu^{L-\delta}
+O(u^{L-\delta-1}),
\qquad b\ne0.
\tag{16b}
\]
The top full-seed terms are
\[
\overline U_0=\theta u^{20}f^{17},\qquad
\overline V_0
=q_6^dp_5^{N-d}u^{5N+d}f^{q_*}.
\tag{16c}
\]
Their Wronskian equals
\[
\overline U_0\overline V_0
B_*
\left(\frac{f'}f-\frac Lu\right).
\tag{16d}
\]
Here \(B_*\ne0\): otherwise (16a) would also give \(C_*=0\),
contrary to
\[
17C_*-15B_*=-10(4N+\ell)\ne0.
\tag{16e}
\]
Equation (16b) therefore gives the first nonzero coefficient
\[
\boxed{
-B_*\delta\,
\theta q_6^dp_5^{N-d}
c^{q_*+16}b\ne0.
}
\tag{16f}
\]
It occurs after degree drop \(\delta\le L\).  The symbolic support
lemma (5a) puts every non-top seed at drop at least \(L+1\), while
the \(k\)-th same-boundary target monomial is lower by
\(3k(L+1)\).  Neither can cancel (16f).

Equations (16) and (16a)--(16f) prove the regular-branch outcome: the
exact Wronskian of the globally lowest boundary block is always
nonzero.  If its \(x\)-power is not zero, this is immediately
incompatible with a constant Jacobian.  If that power is zero
(\(\beta=5\)), the coefficient is still nonconstant in \(u\):
even after the drop \(\delta\le L\), its degree is at least
\[
(20+17L)+(5N+d+q_*L)-1-L>0.
\]
Thus it cannot be the nonzero constant right side either.

### 3.2. Why global boundary minimality is necessary

Exhausting only monomials with the same boundary exponent does not
isolate a nonminimal block.  For example,
\[
CB^5\quad\hbox{has exponent }-4,
\qquad
C^2A^4\quad\hbox{has exponent }-6.
\]
If both occur, the latter precedes the former at the boundary; its
higher \(x\)-jets can reach the coefficient belonging to \(CB^5\).
The proof above avoids this cross-tier contamination by starting
with the globally least exponent of the full target.

## 4. First-lower audit for a pure least-\(C\) face

The exact first-lower double-pole numerator for a pure face factors
as
\[
\begin{aligned}
K={}&(N-\ell+d)\\
&\cdot
\left[
I(100\ell-25N+17d)
+100\ell+25N+15d
\right].
\end{aligned}
\tag{17}
\]
If \(K\ne0\), the double pole closes the face before the boundary.
The first factor \(N-\ell+d=0\) gives
\[
J=-\frac{3I+5}{2}<0
\]
and is not graph-compatible.  It remains to impose
\[
I(100\ell-25N+17d)
+100\ell+25N+15d=0.
\tag{18}
\]

Define
\[
X=25N-17d-100\ell.
\tag{19}
\]
Positivity of \(I\) in (18) gives \(X>0\), and the characteristic
equation simplifies exactly to
\[
\begin{aligned}
I&=\frac{100\ell+25N+15d}{X},\\
J&=\frac{120d}{X},\\
I-J&=\frac{5(5N-21d+20\ell)}{X}.
\end{aligned}
\tag{20}
\]
The established graph-divisibility alternatives leave only
\[
I-J\ge2
\qquad\text{or}\qquad
I=J.
\tag{20a}
\]
Indeed, \(J\ge I+1\) is descending and \(J=I-1\) forces a forbidden
\(x^1\)-term.  The case \(I=J\) is retained because it lies on the
source boundary and must be treated by the full Wronskian.

## 5. Graph-interior sectors \(I-J\ge2\)

Assume \(I-J\ge2\).  Equation (20) first gives
\[
21d<5N+20\ell,
\]
and hence
\[
C_*=15d-5N-20\ell<0.
\tag{21}
\]

Suppose for contradiction that \(B_*\ge0\).  The inequality
\(I-J\ge2\) gives
\[
300\ell\ge25N+71d.
\tag{22}
\]
Together with
\[
17d\ge3N+22\ell,
\tag{23}
\]
this implies
\[
d\ge\frac{25N}{61}.
\tag{24}
\]
On the other hand, (22) and \(X>0\) give
\[
0<X
\le\frac{50N-122d}{3},
\]
so
\[
d<\frac{25N}{61},
\tag{25}
\]
a contradiction.  Therefore
\[
B_*<0,\qquad C_*<0.
\tag{26}
\]
For every boundary degree \(L\ge1\),
\[
B_*L+C_*<0.
\]
The exact leading coefficient (16) is nonzero, closing every such
graph-interior exceptional face in the regular branch.

## 6. Boundary-diagonal sectors \(I=J\)

On the exceptional locus (18), equation \(I=J\) is equivalent to
\[
21d=5N+20\ell.
\tag{27}
\]
The maximal characteristic lies on the source boundary itself, so
\[
L=\deg f=I.
\tag{28}
\]
The characteristic relation gives
\[
B_*I+C_*=0,
\tag{29}
\]
and the leading coefficient (16) cancels.

This cancellation cannot persist.  The fixed jets (3) rule out
\(f=cu^I\): they would force \(c=1\) and
\(I=-57/34\).  Hence, for some
\[
1\le\delta\le I,
\]
one has
\[
f(u)=cu^I+bu^{I-\delta}
+O(u^{I-\delta-1}),
\qquad b\ne0.
\tag{30}
\]
The top full-seed terms are
\[
\overline U_0=\theta u^{20}f^{17},\qquad
\overline V_0
=q_6^dp_5^{N-d}u^{5N+d}f^{q_*}.
\tag{31}
\]
Using (29), their Wronskian becomes
\[
\overline U_0\overline V_0
B_*
\left(
\frac{f'}f-\frac Iu
\right).
\tag{32}
\]
Equation (30) therefore gives the first nonzero coefficient
\[
\boxed{
-B_*\delta\,
\theta q_6^dp_5^{N-d}
c^{q_*+16}b
\ne0.
}
\tag{33}
\]
It occurs after degree drop \(\delta\le I\).

Every non-top exact seed term is lower by at least \(I+1\), and the
\(k\)-th same-boundary counterterm is lower by \(3k(I+1)\).
Consequently neither can reach (33).  This reproduces Section 3.1
for every boundary-diagonal exceptional face in the regular branch.

## 7. Primitive boundary-diagonal audit

The first primitive solution of (27), (18), and the characteristic
integrality conditions is
\[
(N,\ell,d,I,J)=(13,2,5,15,15).
\tag{34}
\]
Here
\[
q_*=54,\qquad
B_*=2,\qquad C_*=-30,\qquad
\beta=-16.
\tag{35}
\]
Every same-boundary target monomial is one of
\[
C^2A^5B^8,\qquad
C^3A^7B^5,\qquad
C^4A^9B^2.
\tag{36}
\]
Their successive degree gaps are \(48\).  If
\[
f=cu^{15}+bu^{15-\delta}+\cdots,
\qquad1\le\delta\le15,
\]
the exact first surviving Wronskian coefficient is
\[
-2\delta\,
\theta q_6^5p_5^8c^{70}b\ne0
\tag{37}
\]
at degree \(1154-\delta\).  The first lower seed can occur only
after degree drop \(16\), so (37) is isolated.

## 8. Polar graph valuations

It remains to treat \(\rho<0\) in (H1).  Formula (H2) shows that every
graph monomial contributing to \(f\) has
\[
j=i+2-\rho\ge2-\rho.
\]
Therefore
\[
f\in(u-1)^{2-\rho}\mathbb C[u],
\qquad
L:=\deg f\ge2-\rho,
\qquad
L+\rho+1\ge3.
\tag{38}
\]

Because \(\rho<0\), the unique highest power of \(\gamma\) in each
exact seed gives the lowest \(x\)-valuation.  The exact leading terms
are
\[
\begin{aligned}
U_0&=\theta x^{-5+17\rho}u^{20}f^{17},\\
A_0&=q_6x^{-2+4\rho}u^6f^4,\\
B_0&=p_5x^{-1+4\rho}u^5f^4,\\
C_0&=x^{1+\rho}f.
\end{aligned}
\tag{39}
\]
The uniqueness follows directly from the exact support: the top
\(\gamma\)-powers are respectively \(17,4,4\), and every other
nonzero seed term has a strictly smaller \(\gamma\)-power.

For a target monomial \(A^aB^bC^c\), put
\[
\begin{aligned}
Q&=4a+4b+c,\\
R&=6a+5b,\\
E_\rho(a,b,c)
&=(-2+4\rho)a+(-1+4\rho)b+(1+\rho)c.
\end{aligned}
\tag{40}
\]
Its leading term is a nonzero constant times
\[
x^{E_\rho(a,b,c)}u^Rf^Q.
\tag{41}
\]
Choose the globally least \(E_\rho\)-block of the full homogeneous
target.  Two monomials of the same target degree lie in that block
exactly when their exponent differences have the form
\[
\Delta c=k,\qquad
\Delta a=(2-3\rho)k,\qquad
\Delta b=-3(1-\rho)k.
\tag{42}
\]
Among the nonzero coefficients in this finite chain, denote the
smallest-\(c\) endpoint by \((a_0,b_0,c_0)\) and the largest-\(c\)
endpoint by \((a_K,b_K,c_K)\), where their \(c\)-exponents differ by
\(K\ge0\).

At \(u=\infty\), one step in (42) lowers the degree of (41) by
\[
3(L+\rho+1)>0,
\tag{43}
\]
so the endpoint \(k=0\) uniquely controls the leading coefficient.
At \(u=1\), one step lowers \(Q\) by \(3\); since (38) makes \(f\)
vanish there, the endpoint \(k=K\) uniquely controls the least
vanishing order.  This two-endpoint separation is independent of all
intermediate target coefficients.

Put
\[
\alpha=-5+17\rho.
\]
For a boundary term \(x^\alpha H(u)\) and a target term \(x^EK(u)\),
the exact leading Jacobian coefficient is
\[
\alpha HK'-EH'K.
\tag{44}
\]
At \(u=1\), the coefficient of the first possible derivative of
\(f\) for the \(k=K\) endpoint is, up to a nonzero common factor,
\[
14a_K-3b_K-22c_K.
\]
Thus vanishing of (44) would force
\[
F:=-14a_K+3b_K+22c_K=0.
\tag{45}
\]

Now put
\[
G:=22a_K+5b_K-20c_K.
\tag{46}
\]
Under (45),
\[
b_K=\frac{14a_K-22c_K}{3},
\qquad
G=\frac{136a_K-170c_K}{3}>0.
\tag{47}
\]
Indeed \(b_K\ge0\) gives \(a_K\ge11c_K/7\), and equality
\(a_K=c_K=0\) would force \(b_K=0\), contrary to positive target
degree.

Finally, direct substitution of (42) into the leading coefficient at
\(u=\infty\) gives the exact factor
\[
\boxed{
(17\rho-5)
\left[
\frac G{17}+3K(L+\rho+1)
\right].
}
\tag{48}
\]
The first factor is negative and the bracket is positive by (38) and
(47).  Hence (48) is nonzero, contradicting (44).  If (45) does not
hold, the earlier \(u=1\) coefficient is already nonzero.

Thus the globally lowest target block has a nonzero exact Jacobian
coefficient for every \(\rho<0\).  If its \(x\)-power is nonzero, it
cannot occur in a constant.  If its \(x\)-power is zero, the
coefficient still vanishes at \(u=1\), because (38) gives
\(\operatorname{ord}_{u=1}f\ge3\) while \(Q\ge1\); being nonzero, it
cannot be a nonzero constant.

Sections 1--3 and Section 8 exhaust \(\rho\le0\).  This proves the
full boundary-valuation theorem for every polynomial graph.

The accompanying exact verifier is
`verify_weighted_lift_ternary_pure_full_boundary_closure.py`.
