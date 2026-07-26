# Global minimal-boundary closure for homogeneous weighted-lift targets

Date: 25 July 2026

## Outcome

Let \(F=(A,B,C)\) be the Gallagher weighted lift and let \(U\) be
the exact second-subduction coordinate.  For every nonzero homogeneous
polynomial
\[
Q_n(A,B,C)\in\mathbf C[A,B,C],\qquad n\ge1,
\tag{1}
\]
and every polynomial graph \(z=g(x,y)\), the restricted Jacobian
\[
J_{x,y}\bigl(U,Q_n(A,B,C)\bigr)
\tag{2}
\]
is not a nonzero constant.  The same conclusion holds with \(U\)
replaced by \(U+R_{\le1}(A,B,C)\), where \(R_{\le1}\) is affine.
A constant may also be added to the second coordinate.

This statement does **not** allow arbitrary lower-degree terms in the
second coordinate.

The proof repairs two gaps in the earlier pure-face argument:

1. it selects the globally minimal source-boundary exponent of the
   entire homogeneous target, rather than a least-\(C\) monomial that
   may have earlier higher-\(C\) faces in front of it;
2. it does not assume that the graph function is regular at the source
   boundary.  A separate endpoint argument closes every graph for
   which that function has a pole.

The proof is exact and all-degree.  The computer verifier checks the
finite seed-support statements and the displayed symbolic identities;
the endpoint argument itself is given below.

## 1. Exact boundary coordinates

Put
\[
u=1+xy,\qquad
\gamma=1-\frac{57}{34}(u-1)+x^2g\left(x,\frac{u-1}{x}\right).
\tag{3}
\]
This is a Laurent polynomial in \(x\) with coefficients in
\(\mathbf C[u]\).  Write
\[
\gamma=\sum_{j=\rho}^{M}x^jf_j(u),\qquad
f_\rho\ne0,
\tag{4}
\]
and set \(f=f_\rho\).  Necessarily
\[
\rho\le0.
\tag{5}
\]
Indeed, if no negative power occurs, the coefficient of \(x^0\)
has value \(1\) at \(u=1\), so it is nonzero.

Let \(p,q\) be the exact Gallagher seed polynomials and let
\(\mathcal N\) be the exact 77-term numerator of \(U\).  After
\(w=u\gamma\), define the polynomial templates
\[
\begin{aligned}
\mathsf A(u,\gamma)
 &=\frac{q(u\gamma)+u\gamma^2}{\gamma^2},\\
\mathsf B(u,\gamma)
 &=\frac{p(u\gamma)+\gamma}{\gamma},\\
\mathsf H(u,\gamma)
 &=\frac{\mathcal N(u\gamma,\gamma)}{\gamma^5}.
\end{aligned}
\tag{6}
\]
The exact divisibilities in the seed make all three expressions
polynomials in \(u,\gamma\), and
\[
A=x^{-2}\mathsf A,\qquad
B=x^{-1}\mathsf B,\qquad
U=x^{-5}\mathsf H,\qquad
C=x\gamma.
\tag{7}
\]

The exact supports have unique top \(\gamma\)-degree terms
\[
\begin{aligned}
\mathsf A&=q_6u^6\gamma^4+
  \{\text{terms of }\gamma\text{-degree}<4\},\\
\mathsf B&=p_5u^5\gamma^4+
  \{\text{terms of }\gamma\text{-degree}<4\},\\
\mathsf H&=\theta u^{20}\gamma^{17}+
  \{\text{terms of }\gamma\text{-degree}<17\},
\end{aligned}
\tag{8}
\]
where \(q_6p_5\theta\ne0\).

For functions \(x^\alpha H(u)\) and \(x^\beta V(u)\), the coordinate
change \(u=1+xy\) gives
\[
J_{x,y}\left(x^\alpha H,x^\beta V\right)
=x^{\alpha+\beta}
\left(\alpha HV'-\beta H'V\right).
\tag{9}
\]

## 2. Regular boundary: \(\rho=0\)

Here
\[
f(1)=1,\qquad f'(1)=-\frac{57}{34},\qquad
L:=\deg f\ge1.
\tag{10}
\]
Substitution in the exact templates gives
\[
\begin{array}{c|c|c}
&\deg_u&\operatorname{lc}\\ \hline
\mathsf A(u,f)&6+4L&q_6c^4\\
\mathsf B(u,f)&5+4L&p_5c^4\\
\mathsf H(u,f)&20+17L&\theta c^{17},
\end{array}
\tag{11}
\]
where \(c=\operatorname{lc}(f)\ne0\).  Every non-top seed term is
lower in \(u\)-degree by at least \(L+1\).  This follows directly
from the finite exact supports: for \(\mathsf A,\mathsf B\), every
non-top term loses at least one \(u\)-power and one \(f\)-power
(with only still-lower terminal terms); for \(\mathsf H\), the only
additional edge possibility loses two \(f\)-powers and no
\(u\)-power.  Thus its loss is at least
\(\min(L+1,2L)=L+1\).

### 2.1. Select the global face

For a target monomial \(A^aB^bC^c\), put
\[
\beta(a,b,c)=-2a-b+c.
\tag{12}
\]
Let \(\beta_0\) be the minimum of (12) over the support of \(Q_n\).
No target monomial has an earlier boundary order.  Because
\(\gamma=f+O(x)\) and (7) is exact, every omitted graph coefficient
has strictly larger \(x\)-order; differentiation in (9) preserves the
sum of the two displayed \(x\)-orders.  Hence
\(x^{\beta_0-5}\) is the globally earliest possible Jacobian order,
not merely the earliest term inside one selected face.

Choose, among the monomials on this face, the one with smallest
\(C\)-exponent and write it as
\[
C^\ell A^dB^{N-d},\qquad N+\ell=n.
\tag{13}
\]
Every other monomial of the same total degree and the same
\(\beta_0\) is uniquely of the form
\[
C^{\ell+k}A^{d+2k}B^{N-d-3k},
\qquad k\ge0.
\tag{14}
\]
The \(k\)-th term is lower than (13) in \(u\)-degree by
\[
3k(L+1).
\tag{15}
\]
Consequently the nonzero coefficient of (13) controls the leading
term of the complete global minimal face.

Set
\[
q_*=4N+\ell,\qquad
\beta_0=\ell-N-d,
\tag{16}
\]
and
\[
B_*=17d-3N-22\ell,\qquad
C_*=15d-5N-20\ell.
\tag{17}
\]
The boundary coefficient of the Jacobian at
\(x^{\beta_0-5}\) is
\[
\mathcal W=-5\mathsf H\,\mathsf V'
-\beta_0\mathsf H'\mathsf V,
\tag{18}
\]
where \(\mathsf V\) is the complete face (14).  Its leading
\(u\)-coefficient is a nonzero seed-and-target scalar times
\[
B_*L+C_*.
\tag{19}
\]

If (19) is nonzero, then \(\mathcal W\ne0\).  Suppose it vanishes.
The identity
\[
17C_*-15B_*=-10q_*
\tag{20}
\]
shows that \(B_*\ne0\).

The fixed jets in (10) rule out \(f=cu^L\): such an equality would
give \(c=1\) and \(L=-57/34\).  Hence, for some
\(1\le\delta\le L\),
\[
f=cu^L+bu^{L-\delta}+\cdots,\qquad b\ne0.
\tag{21}
\]
The top seed terms in (18) are
\[
\theta u^{20}f^{17},
\qquad
\lambda q_6^dp_5^{N-d}u^{5N+d}f^{q_*},
\tag{22}
\]
where \(\lambda\ne0\) is the coefficient of (13).  Their Wronskian
is their product times
\[
B_*\frac{f'}f+\frac{C_*}{u}.
\tag{23}
\]
After the leading cancellation (19), (21) gives the first surviving
coefficient
\[
-\lambda B_*\delta\,
\theta q_6^dp_5^{N-d}c^{q_*+16}b\ne0.
\tag{24}
\]
It occurs after degree drop \(\delta\le L\).  Every non-top exact
seed starts after a drop of at least \(L+1\), and every other
same-face target term starts after at least \(3(L+1)\).  Thus
nothing can cancel (24).

This proves \(\mathcal W\ne0\) for the globally minimal face.  It
also resolves the apparent problem that, for example, \(C^2A^4\)
has an earlier boundary exponent than \(CB^5\): the proof starts
with whichever face is globally earlier.

## 3. Pole boundary: \(\rho<0\)

The leading coefficient \(f\) in (4) comes only from graph monomials
\(x^ry^s\) satisfying
\[
r+2-s=\rho.
\tag{25}
\]
Therefore
\[
f(u)=\sum_r c_r(u-1)^{r+2-\rho}.
\tag{26}
\]
In particular,
\[
\nu:=\operatorname{ord}_{u=1}f\ge2-\rho,\qquad
L:=\deg f\ge2-\rho,
\qquad L+\rho+1\ge3.
\tag{27}
\]

Because \(\rho<0\), the unique largest \(\gamma\)-degree terms in
(8) give the unique lowest \(x\)-orders:
\[
\begin{aligned}
U&=x^\alpha\bigl(\theta u^{20}f^{17}\bigr)+\cdots,
&\alpha&=-5+17\rho,\\
A&=x^{-2+4\rho}\bigl(q_6u^6f^4\bigr)+\cdots,\\
B&=x^{-1+4\rho}\bigl(p_5u^5f^4\bigr)+\cdots,\\
C&=x^{1+\rho}f+\cdots .
\end{aligned}
\tag{28}
\]

For a target monomial \(A^aB^bC^c\), define
\[
\begin{aligned}
q&=4a+4b+c,\\
s&=6a+5b,\\
E&=-2a-b+c+\rho q.
\end{aligned}
\tag{29}
\]
Its leading boundary term is a nonzero scalar times
\[
x^E u^sf^q.
\tag{30}
\]
Let \(E_0\) be the global minimum of \(E\) over the support of
\(Q_n\).  On an \(E_0\)-face, increasing \(c\) by an integer \(k\)
forces
\[
\Delta c=k,\qquad
\Delta a=(2-3\rho)k,\qquad
\Delta b=-3(1-\rho)k.
\tag{31}
\]
Consequently
\[
\Delta q=-3k,\qquad
\Delta s=-3(1+\rho)k.
\tag{32}
\]

The unique top \(\gamma\)-degrees in (28) and the global minimality
of \(E_0\) imply that \(x^{\alpha+E_0}\) is the globally earliest
Jacobian order.  Every lower seed, later graph coefficient, or target
monomial outside this face has strictly larger \(x\)-order, so none
can feed the coefficient studied below.

Let \(k=0\) be the endpoint with smallest \(c\), and let \(k=K\)
be the endpoint with largest \(c\) present in the target face.
Equation (27) and (32) show:

- at \(u=\infty\), the \(k\)-th term loses
  \(3k(L+\rho+1)>0\) degrees, so \(k=0\) uniquely dominates;
- at \(u=1\), the factor \(u^s\) is a unit and \(q\) decreases
  with \(k\), so \(k=K\) uniquely has the smallest vanishing order.

No cancellation between target coefficients is possible at either
endpoint.

Let \((a,b,c)\), \(q\), and \(s\) now denote the \(k=K\) endpoint.
The coefficient at the globally earliest Jacobian order is
\[
\mathcal W_\rho
=\alpha\mathsf H_0\mathsf V_0'
-E_0\mathsf H_0'\mathsf V_0.
\tag{33}
\]
If it vanished identically, its order at \(u=1\) would force
\[
\alpha q-17E_0=0.
\tag{34}
\]
Since \(E_0=(-2a-b+c)+\rho q\) and
\(\alpha=-5+17\rho\), equation (34) is
\[
F:=-14a+3b+22c=0.
\tag{35}
\]

At infinity the dominant monomial is the \(k=0\) endpoint.  Using
(31)--(34), vanishing of its leading coefficient becomes
\[
\frac{G}{17}+3K(L+\rho+1)=0,
\qquad
G:=22a+5b-20c.
\tag{36}
\]
But (35) gives
\[
b=\frac{14a-22c}{3},\qquad
a\ge\frac{11}{7}c,
\tag{37}
\]
and hence
\[
G=\frac{136a-170c}{3}>0
\tag{38}
\]
for every nonconstant target monomial.  The second term in (36) is
also nonnegative, and is positive when \(K>0\).  This contradicts
(36), including the case \(K=0\).

Thus \(\mathcal W_\rho\ne0\).  Moreover it vanishes at \(u=1\) to
positive order, since \(\nu\ge2-\rho\ge3\), so it cannot equal a
nonzero constant even if its \(x\)-exponent happens to be zero.

## 4. Affine first-coordinate perturbations and the constant RHS

For \(\rho=0\), the boundary \(x\)-orders of \(U,A,B,C\) are
\[
-5,\quad-2,\quad-1,\quad1.
\tag{39}
\]
For \(\rho<0\), subtracting the order of \(U\) from those of
\(A,B,C\) gives
\[
3-13\rho,\qquad4-13\rho,\qquad6-16\rho,
\tag{40}
\]
all strictly positive.  Therefore an affine
\(R_{\le1}(A,B,C)\) cannot enter the globally earliest coefficient
used in either Section 2 or Section 3.  A constant has zero
derivative.

Finally, if the earliest \(x\)-exponent of the Jacobian is nonzero,
a nonzero coefficient directly contradicts a constant Jacobian.  If
that exponent is zero, the coefficients constructed above are
nonconstant polynomials in \(u\): in the regular case their surviving
degree, in the cancellation case, is at least
\[
19+5N+d+(q_*+17)L-\delta
\ge19+5N+d+(q_*+16)L>0,
\tag{41}
\]
and without the leading cancellation it is larger.  In the pole case
they vanish at \(u=1\) to order at least
\(\nu(17+q)-1>0\).
They therefore still cannot equal a nonzero constant.

This completes the homogeneous-target theorem.

## 5. Exact scope

The argument applies to
\[
\left(
U+R_{\le1}(A,B,C),
Q_n(A,B,C)+\text{constant}
\right),
\qquad Q_n\ne0\text{ homogeneous}.
\tag{42}
\]
It does not establish a theorem for an arbitrary nonhomogeneous
second coordinate.  A lower-degree face can have an earlier boundary
order, and its later \(x\)-jets can feed coefficients belonging to a
higher-degree face.  Any extension to such targets needs a new global
filtration argument rather than reuse of the homogeneous proof.
