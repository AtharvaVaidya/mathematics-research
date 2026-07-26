# Arbitrary nonhomogeneous targets through degree eleven

Date: 26 July 2026

## Outcome

Let \(F=(A,B,C)\) be the exact Gallagher weighted lift, let \(U\) be
its exact second-subduction coordinate, and let \(R_{\le2}\) be an
arbitrary polynomial in \(A,B,C\) of target degree at most two.  On
every polynomial graph, every nonconstant target polynomial
\(Q(A,B,C)\) of target degree at most eleven satisfies
\[
\boxed{
J_{x,y}\bigl(U+R_{\le2},Q\bigr)\notin\mathbf C^\times .
}
\tag{1}
\]

The degree-ten basis extends, but degree eleven introduces the first
genuine resonant augmented groups.  The ten cusp collisions are
replaced by
\[
T,\ AT,\ W,\ U,\ A^2T,\ AW,\ AU,\ BW,\ BU,\ CU.
\tag{2}
\]
After the scalar \(U\)-coefficient is removed modulo the actual first
coordinate, nine augmented atoms remain.

At a regular graph boundary the atoms separate directly for
\(L\ge2\).  At \(L=1\) there are four exact two-dimensional groups;
their Wronskian maps are injective.

At a pole boundary there are six two-dimensional groups.  Four are
immediately nonresonant.  The other two have the exact characteristic
families
\[
\begin{aligned}
 BW:\quad&
 \rho=5-16k,\qquad
 f=c\,u^{30k-10}(u^2-1)^{17k-5},\\
 AU:\quad&
 \rho=11-14k,\qquad
 f=c\,u^{22k-18}(u^2-1)^{17k-13},
\end{aligned}
\qquad k\ge2,\quad c\in\mathbf C^\times.
\tag{3}
\]
The first lower total-\(\gamma\) layer couples the \(BW\) family to
\(AT\), and the \(AU\) family to the \(W/A^2B^3\) group.  Exact local
jet determinants at \(u=1\) are nonzero for every \(k\ge2\):
\[
\begin{aligned}
\Delta_{BW/AT}
 &\doteq
 (17k-5)(105k-32),\\
\Delta_{AU/W}
 &\doteq
 (17k-13)^2.
\end{aligned}
\tag{4}
\]
Here \(\doteq\) means equality up to a fixed nonzero rational scalar.
Thus neither resonance can survive its first allowed interference.

No complete SAGBI basis or termination theorem is used.  This remains
a theorem about polynomial-graph restrictions of the weighted lift,
not a proof of the plane Jacobian conjecture.

## 1. Boundary notation

Put
\[
u=1+xy,\qquad
\gamma=\sum_{j=\rho}^{M}x^jf_j(u),\qquad f=f_\rho\ne0.
\tag{5}
\]
For a regular boundary, \(\rho=0\),
\[
L=\deg f\ge1,\qquad
f(1)=1,\qquad f'(1)=-\frac{57}{34}.
\tag{6}
\]
For a pole boundary, \(\rho<0\),
\[
\nu=\operatorname {ord}_{u=1}f\ge2-\rho.
\tag{7}
\]

For an ordinary monomial \(A^aB^bC^c\), set
\[
\beta=-2a-b+c,\qquad
h=6a+5b,\qquad
q=4a+4b+c=h+\beta.
\tag{8}
\]
Its regular top is \(x^\beta u^hf^q\), while its polar \(x\)-order is
\[
E=\beta+\rho q.
\tag{9}
\]
The first coordinate has top
\[
U_{\rm top}
=\theta x^{-5}u^{20}f^{17},\qquad \theta\ne0,
\tag{10}
\]
and polar order
\[
\alpha=-5+17\rho.
\tag{11}
\]

## 2. The degree-eleven vector-space basis

The primitive collision kernel of the ordinary labels remains
\[
(a,b,c)\longmapsto(\beta,h),
\qquad
\ker=\mathbf Z(5,-6,4).
\tag{12}
\]
Through target degree eleven the repeated ordinary labels are exactly
\[
B^6M\sim A^5C^4M,
\qquad \deg M\le2.
\tag{13}
\]
There are ten such pairs, one for every monomial \(M\) of degree at
most two.

Multiplication of the exact first subduction \(T\) by these ten
monomials first replaces the ten upper sides.  The exact identities
defining \(U\) and \(W\) then give the triangular replacements
\[
\begin{array}{c|c}
M&\text{replacement atom}\\ \hline
1&T\\
A&AT\\
B&W\\
C&U\\
A^2&A^2T\\
AB&AW\\
AC&AU\\
B^2&BW\\
BC&BU\\
C^2&CU.
\end{array}
\tag{14}
\]
The exact \(10\times10\) coefficient matrix on the ten removed upper
monomials has nonzero determinant.  Hence every target of degree at
most eleven has a unique expression
\[
Q=c+\mu U+\sum_{\Xi\in\mathcal A}\lambda_\Xi\Xi
 +\sum\nolimits'\lambda_{abc}A^aB^bC^c,
\tag{15}
\]
where
\[
\mathcal A
=\{T,AT,A^2T,W,AW,BW,AU,BU,CU\},
\tag{16}
\]
and the prime omits the ten upper cusp monomials.

As in degree ten, the \(U\)-term must be removed modulo the actual
first coordinate:
\[
P=U+R_{\le2},\qquad Q^\flat=Q-\mu P.
\tag{17}
\]
Then
\[
J(P,Q^\flat)=J(P,Q),
\tag{18}
\]
and only ordinary coefficients of degree at most two are changed.  If
\(Q^\flat\) is constant, its Jacobian is zero.  Otherwise its support
is the retained ordinary basis together with (16).

## 3. Exact augmented frontiers

The exact boundary polynomials have the following Pareto frontiers.
Each row records \((\beta,h,q)\):
\[
\begin{array}{c|c}
\text{atom}&\text{frontier}\\ \hline
T&(-6,25,19)\\
AT&(-8,31,23)\\
A^2T&(-10,37,27)\\
W&(-7,26,19),\ (-7,25,20)\\
AW&(-9,32,23),\ (-9,31,24)\\
BW&(-8,31,23),\ (-8,30,24)\\
AU&(-7,26,21)\\
BU&(-6,25,21)\\
CU&(-4,20,18).
\end{array}
\tag{19}
\]
The verifier obtains these frontiers from the full exact seed
polynomials, not from a formal monomial model.

For \(L\ge2\), the larger-\(q\) term uniquely dominates in each
two-frontier row.  All resulting \((\beta,h+Lq)\) labels are distinct
from one another and from the retained ordinary labels.  Their
Wronskian characteristics with (10) are
\[
\begin{array}{c|c}
T&7L-5\\
AT&21L+5\\
A^2T&35L+15\\
W&19L+15\\
AW&33L+25\\
BW&16L+10\\
AU&14L+10\\
BU&-3L-5\\
CU&-22L-20.
\end{array}
\tag{20}
\]
None vanishes for \(L\ge2\).

For an ordinary atom whose monomial characteristic vanishes, the first
nonmonomial term of \(f\) gives a nonzero deviation at degree loss at
most \(L\).  The exact degree-eleven gap audit finds seven possible
resonant ordinary atoms; in every case the next lower label is farther
than \(L\).  Thus no augmented atom enters that deviation coefficient.

## 4. The fixed linear boundary

When \(L=1\), (6) fixes
\[
f(u)=\frac{91}{34}-\frac{57}{34}u.
\tag{21}
\]
After exact substitution, the only repeated regular labels are
\[
\begin{array}{c|c}
(-4,38)&CU,\ AB^3C\\
(-6,46)&BU,\ AB^4\\
(-7,47)&AU,\ A^2B^3\\
(-8,54)&AT,\ BW.
\end{array}
\tag{22}
\]

For two target polynomials \(V_1,V_2\) in a row, apply the exact
Wronskian operator
\[
\mathcal W_\beta(V)
=-5H\,V'-\beta H'V,
\qquad
H=U_{\rm boundary}(u,f(u)).
\tag{23}
\]
The two outputs in each row have the same top degree.  The differences
of their normalized next/top coefficients are respectively
\[
-\frac{481}{342},\qquad
-\frac{91}{152},\qquad
-\frac{2639}{1368},\qquad
\frac{8968203125}{121057727177}.
\tag{24}
\]
They are all nonzero, so every map from a group in (22) to its
Wronskian coefficient is injective.  More precisely, a nonzero
combination in any row can lose at most one \(u\)-degree.  On each of
the four corresponding \(\beta\)-faces, the next lower target label is
at gap exactly two.  It therefore cannot enter the surviving
Wronskian coefficient.

There are two singleton ordinary characteristics at \(L=1\).  Their
first deviations lose one degree, while the next lower labels are
separated by gaps \(6\) and \(2\).  This completes the regular-boundary
argument.

## 5. Polar groups

At a pole, all retained polar labels \((\beta,q)\) are singletons
except the following exact groups:
\[
\begin{array}{c|c|c|c}
\text{group}&(\beta,q)&
P(u)\text{ in }f^qP(u)&
B=-5q-17\beta\\ \hline
W/A^2B^3&(-7,20)&a u^{27}+b u^{25}&19\\
CU/A^2B^2C^2&(-4,18)&a u^{22}+b u^{20}&-22\\
BU/A^2B^3C&(-6,21)&a u^{27}+b u^{25}&-3\\
BW/A^2B^4&(-8,24)&a u^{32}+b u^{30}&16\\
AU/A^3B^2C&(-7,21)&a u^{28}+b u^{26}&14\\
AW/A^3B^3&(-9,24)&a u^{33}+b u^{31}&33.
\end{array}
\tag{25}
\]

At a fixed earliest polar order, groups of different \(q\) are
separated by their orders at \(u=1\).  For one row of (25), its exact
Wronskian with (10), after removal of a nonzero monomial factor, is
\[
B\,u f'P
+f\bigl(\alpha uP'-20EP\bigr).
\tag{26}
\]
If \(P(1)\ne0\), its first coefficient is proportional to
\(B\nu P(1)\), and every \(B\) in (25) is nonzero.  If \(P(1)=0\),
then \(P\) is a nonzero multiple of \(u^r(u^2-1)\), and the next
coefficient is proportional to
\[
(B\nu+\alpha)P'(1).
\tag{27}
\]

For the \(W,CU,BU,AW\) rows, (27) never vanishes under
\(\rho<0,\nu\ge2-\rho\).  For example, the lower-bound expressions in
the two positive cases are
\[
33-2\rho,\qquad61-16\rho.
\tag{28}
\]
The two remaining equations have exactly the graph-compatible
solutions (3).  Indeed,
\[
\begin{aligned}
16\nu=5-17\rho
&\Longleftrightarrow
(\rho,\nu)=(5-16k,17k-5),\\
14\nu=5-17\rho
&\Longleftrightarrow
(\rho,\nu)=(11-14k,17k-13),
\end{aligned}
\tag{29}
\]
and (7) is equivalent to \(k\ge2\) in both families.
Reduction of the first equation modulo \(16\) forces
\(\rho\equiv5\pmod {16}\), while reduction of the second modulo \(14\)
forces \(\rho\equiv11\pmod {14}\).  Thus the parametrizations in (29)
are exhaustive over the integers.  The multiplier \(c\ne0\) in (3)
is free and does not change the logarithmic derivative used below.

## 6. The two resonant characteristic rays

Let the top \(U\)-sector be
\[
x^{-5}h(u)\gamma^{17},
\qquad h(u)=\theta u^{20},
\tag{30}
\]
and let a resonant target top be
\[
x^\beta b(u)\gamma^n.
\tag{31}
\]
The top-\(\gamma\) part of the Jacobian is
\[
x^{-5+\beta}\gamma^{16+n}\mathcal L(\gamma),
\tag{32}
\]
where \(\mathcal L\) is the linear first-order operator
\[
\begin{aligned}
\mathcal L(\gamma)
={}&h b(-5n-17\beta)\,u\gamma_u\\
&+u\bigl(17h b'-nh'b\bigr)x\gamma_x\\
&+u\bigl(-5hb'-\beta h'b\bigr)\gamma,
\end{aligned}
\tag{33}
\]
up to a fixed nonzero monomial factor.  Substitution of an
\(x^I\)-sector turns (33) into a one-variable Euler equation.

For the \(BW\) and \(AU\) combinations with \(P(1)=0\), its
graph-compatible polynomial solutions are exactly the sectors in
(3).  On the \(BW\) ray, the complete earliest \(E\)-face is the
two-dimensional \(BW/A^2B^4\) group; on the \(AU\) ray, it is the
two-dimensional \(AU/A^3B^2C\) group.  No other retained ordinary or
augmented atom has the same \(E=\beta+\rho q\) for any \(k\ge2\).
Thus a nonzero top Wronskian on that face cannot be cancelled by a
different \(q\)-group, and a hypothetical cancellation must solve the
characteristic equation.

Since \(\mathcal L\) is linear, an arbitrary sum of intermediate
resonant graph sectors is still killed by (33).  Every nonresonant
intermediate graph sector would give an earlier isolated coefficient,
so it must be absent.  The exact target-face audit also enumerates every
target order strictly between the resonant face and its first
lower-total-\(\gamma\) layer.  For \(BW\) these are the seven singleton
\(q=24\) labels with \(\beta=-7,\ldots,-1\).  For \(AU\) they are the
three singleton \(q=20\) labels with \(\beta=-10,-9,-8\), the
\(q=21\) labels with \(\beta=-6,\ldots,1\), and the duplicate \(BU\)
atom at \(\beta=-6\).  Every singleton is closed by the polar argument
of Section 5, while the \(BU\) group has
\[
 B\nu+\alpha=-289k+221\ne0.
\tag{34}
\]
Hence a nonzero coefficient on an intervening target face would itself
be an earlier obstruction.

The first graph sector not killed by (33) is the zero sector at
\(x^0\).  It is not the globally fixed linear polynomial (21).
Writing \(z=u-1\), the graph normalization fixes only
\[
 f_0(u)=1-\frac{57}{34}z+z^2h(u),
\tag{35}
\]
where \(h\) is arbitrary.  At precisely the same \(x\)-order, one
lower total-\(\gamma\)-degree of the exact seed enters.  Intermediate
resonant sectors cannot contaminate this coefficient: replacing any
one of the leading \(x^\rho f\) factors by a higher sector strictly
raises its \(x\)-order.

For \(BW\), the sole lower target atom at this order is \(AT\).
Take the \(z^{-1}\) and \(z^0\) Laurent coefficients of the normalized
residue and the leading \(AT\) Wronskian.  Their exact
\(2\times2\) determinant is the first line of (4), up to a nonzero
rational scalar.  The coefficient \(h(1)\) cancels identically, so
the determinant uses only the fixed 1-jet in (35).

For \(AU\), the lower target space is exactly the two-dimensional
\(W/A^2B^3\) group.  Take the \(z^{-1},z^0,z^1\) Laurent
coefficients of the residue and the two leading Wronskians.  Their
exact \(3\times3\) determinant is the second line of (4), again up to
a nonzero rational scalar.  Both \(h(1)\) and \(h'(1)\) cancel
identically.

Both determinants are nonzero for every \(k\ge2\).  Therefore no
choice of the available lower target coefficients cancels the first
resonant residue, for any allowed zero sector (35).

The exact polar-label audit also proves that these are the only lower
atoms at that order.  Every nonconstant monomial of \(R_{\le2}\)
starts strictly later than this residue for both families.

## 7. Conclusion and scope

At a regular boundary, Sections 3--4 isolate a nonzero Wronskian
coefficient.  At a pole boundary, Section 5 does so except on the two
families (3), and Section 6 closes those families at their first exact
lower interference layer.  The perturbation \(R_{\le2}\) is later in
both filtrations.  If the isolated coefficient has \(x\)-order zero,
its nonconstant \(u\)-dependence still prevents it from being a
nonzero scalar.  Together with (17)--(18), this proves (1).

The argument uses only the finite vector-space basis required through
degree eleven.  It does not assert that
\(\{A,B,C,T,U,W\}\) is a complete SAGBI basis, and it makes no claim in
degree twelve.

The accompanying exact verifier is
`verify_weighted_lift_nonhomogeneous_degree_eleven_newton_basis_closure.py`.
