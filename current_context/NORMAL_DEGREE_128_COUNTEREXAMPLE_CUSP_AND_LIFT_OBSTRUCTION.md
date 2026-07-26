# A normalized one-pole cusp at \((12,8)\) and its exact lift obstruction

Date: 26 July 2026

## Outcome

At the next normal-degree frontier
\[
 (\deg_yF,\deg_yG)=(12,8),
\]
the fourth-power chart has the same Laurent-time structure as the
cube chart at \((9,6)\), with one important numerical change.  After
normalization and depression there are six conserved Laurent
coefficients \(A_1,\ldots,A_6\), and
\[
 8A_7'=\frac{\lambda}{r}.
\]
The pure-power reduction therefore again has
\[
 v=u^m,\qquad r=\gamma u^{mn+1},\qquad
 8A_7=\alpha+\beta v^{-n}.
\]
For a depressed monic octic, the line-injectivity descent needs the
weighted pole bound
\[
 n\geq3\rho,
\]
rather than the bound \(n\geq2\rho\) which sufficed for a sextic.

There is a nontrivial exact rational invariant curve satisfying every
normalized condition.  It has one-pole time
\[
 A_7=-\frac{2^{18}\sqrt{21}}{3^7\,7^{10}}v^{-19}
\]
and normalized Jacobian
\[
 [f,g]_{v,w}
 =\frac{2^{21}19\sqrt{21}}{3^7\,7^{10}}v^{-20}.
\]
Its coefficient pole scale is \(\rho=1\), so its ratio is
\[
 \frac{\operatorname{pole}(A_7)}{\rho}=19.
\]
Thus it does not evade the degree-eight line threshold.

More strongly, this cusp cannot be the normalization of a polynomial
pair for **any** rational depressing center.  Its homogeneous binary
forms \(F_0,G_0\) have
\[
 \operatorname {Res}(F_0,G_0)
 =-\frac{2^{88}19^2}{3^{36}7^{48}}\ne0.
\]
Polynomiality at the root \(u=0\) would force the bounded center
parameter to tend to a common zero of \(F_0,G_0\), contradicting this
resultant.

This is an exact counterexample to any attempt to exclude the
\((12,8)\) chart using only the normalized Laurent equations or the
one-pole-time condition.  It is not a polynomial Keller
counterexample.  It supplies instead a reusable finite-cusp lift
obstruction and identifies the still-open task: classify the
non-homogeneous boundary arcs on which cancellation might reduce the
ratio from \(19\) below \(3\).

## 1. Normalized fourth-power geometry

Write the leading coefficients as
\[
 f_{12}=h^3,\qquad g_8=h^2.
\]
In the fourth-power chart, \(h=r^4\) with
\(r\in\mathbf C[x]\setminus\{0\}\).  Put \(z=ry\) and depress the
monic octic:
\[
 g=w^8+aw^6+bw^5+cw^4+dw^3+ew^2+fw+q.
\tag{1}
\]
Let
\[
 s=g^{1/8}=w+O(w^{-1}).
\]
The upper triangular equations put \(f\) in the approximate-root
form
\[
 f=(\Phi(s))_+,
\tag{2}
\]
where \(\Phi\) is a degree-twelve polynomial with constant
coefficients; its \(s^8\) term and its constant term can be removed
by target transformations.

In the inverse \(s\)-coordinate there is a unique expansion
\[
 \widehat f=\Phi(s)+\sum_{\ell\geq1}A_\ell s^{-\ell}.
\tag{3}
\]
At fixed \(s\), the chain rule gives
\[
 [f,g]_{x,w}
 =8s^7s_w\sum_{\ell\geq1}A_\ell'(x)s^{-\ell}.
\tag{4}
\]
Since \(s_w=1+O(s^{-2})\), the coefficients of
\(w^6,w^5,\ldots,w\) in (4) are triangular with diagonal \(8\).
Consequently
\[
 A_1'=\cdots=A_6'=0,\qquad
 8A_7'=\frac{\lambda}{r}.
\tag{5}
\]

Set \(T=8A_7\).  Then \(T'=\lambda/r\), so the same
Riemann--Hurwitz argument used in normal degree \((9,6)\) gives
either constant \(r\) and affine \(T\), or
\[
 r=\gamma u^{k+1},\qquad
 T=\alpha+\beta u^{-k}.
\tag{6}
\]
The coefficient field contains \(\mathbf C(u^k)\) and is contained
in \(\mathbf C(u)\).  Cyclic Galois correspondence therefore gives
\[
 K=\mathbf C(v),\qquad v=u^m,\qquad k=mn,
\tag{7}
\]
and
\[
 [f,g]_{v,w}=\frac{\lambda}{m\gamma v^{n+1}},
 \qquad 8A_7=\alpha+\beta v^{-n}.
\tag{8}
\]

## 2. The degree-eight polynomial-lift threshold

For the coefficient of \(w^{8-j}\) in (1), put
\[
 \rho=\max_{2\leq j\leq8}
 \frac{\operatorname {pole}_0(c_j)}j,
\tag{9}
\]
including \(0\) in the maximum.  Undo depression in the form
\[
 G(u,y)=g\bigl(u^m,\gamma u^{mn+1}y+t(u)\bigr),
\tag{10}
\]
and let \(e=\max(0,-\operatorname {ord}_0t)\).

Monicity gives the center bound
\[
 e\leq m\rho.
\tag{11}
\]
Indeed, if \(e>m\rho\), the term \(t^8\) is the unique most singular
term of \(G(u,0)=g(u^m,t)\), contradicting polynomiality.

The coefficient \(G_i(u)\) of \(y^i\) then satisfies
\[
 \operatorname {ord}_0G_i
 \geq i(mn+1)-m(8-i)\rho.
\tag{12}
\]
If \(n\geq3\rho\), then for every \(i\geq2\),
\[
\begin{aligned}
 \operatorname {ord}_0G_i
 &\geq i+m\bigl(3i-(8-i)\bigr)\rho\\
 &=i+4m(i-2)\rho>0.
\end{aligned}
\tag{13}
\]
Thus \(G(0,y)\) is affine.  If its linear coefficient is nonzero,
the second coordinate separates the line \(u=0\).  If it vanishes,
the Keller identity restricted to that line makes \(F(0,y)\) affine
and nonconstant.  The original Keller map is injective on one affine
line, hence is an automorphism by Gwoździewicz's theorem.

We record the reusable consequence:

> **Degree-eight line criterion.**  A noninvertible pure-power
> \((12,8)\) candidate must have an invariant one-pole coefficient
> curve with
> \[
> \operatorname {pole}_0(A_7)<3\rho.
> \tag{14}
> \]

The strict inequality in (14) is a necessary condition, not a claim
that such a curve exists.

## 3. An exact normalized one-pole cusp

It is enough to work on the zero upper-constant slice
\[
 f=(g^{3/2})_+.
\tag{15}
\]
Let \(\tau\) be a parameter and scale the seven coefficients of (1)
by their deficits:
\[
\begin{array}{c|c}
\text{coefficient}&\text{value}\\ \hline
a&\tau^2\\
b&-\dfrac{22\sqrt{21}}{441}\tau^3\\
c&\dfrac{169}{504}\tau^4\\
d&-\dfrac{47\sqrt{21}}{1029}\tau^5\\
e&\dfrac{6721}{148176}\tau^6\\
f&-\dfrac{13679\sqrt{21}}{1555848}\tau^7\\
q&\dfrac{268777}{49787136}\tau^8 .
\end{array}
\tag{16}
\]
The residue construction (3), checked exactly in the accompanying
verifier, gives
\[
 A_1=\cdots=A_6=0,\qquad
 A_7=-\frac{2^{18}\sqrt{21}}{3^7\,7^{10}}\tau^{19}.
\tag{17}
\]
Equation (4), or direct differentiation, gives
\[
 [f,g]_{\tau,w}
 =-\frac{2^{21}19\sqrt{21}}{3^7\,7^{10}}\tau^{18}.
\tag{18}
\]

Now put \(\tau=v^{-1}\).  Then
\[
 [f,g]_{v,w}
 =\frac{2^{21}19\sqrt{21}}{3^7\,7^{10}}v^{-20}.
\tag{19}
\]
This is exactly (8) with \(n=19\), after choosing the harmless
constant \(\gamma\).  The field generated by the coefficients is
\(\mathbf C(v)\), because it contains both \(v^{-2}\) and a nonzero
multiple of \(v^{-3}\).  The time has one pole and no finite critical
point.  Hence (16) satisfies the full normalized pure-power geometry,
not merely its leading equations.

Every coefficient in (16) has pole order equal to its deficit, so
\[
 \rho=1,\qquad n=19.
\tag{20}
\]
The cusp is therefore far from the possible escape range (14).

## 4. Exact obstruction to every polynomial lift

Because (16) is weighted homogeneous, there are monic polynomials
\(F_0,G_0\in\mathbf C[X]\), of degrees twelve and eight, such that
\[
 f(v,w)=v^{-12}F_0(vw),\qquad
 g(v,w)=v^{-8}G_0(vw).
\tag{21}
\]
Their explicit coefficients are generated from (15)--(16) by the
verifier.  Exact elimination gives
\[
 \boxed{
 \operatorname {Res}_X(F_0,G_0)
 =-\frac{2^{88}19^2}{3^{36}7^{48}}.
 }
\tag{22}
\]

Suppose a polynomial lift existed after an arbitrary rational
depressing center \(t(u)\).  At \(y=0\), put
\[
 X(u)=v\,t(u),\qquad v=u^m.
\]
Equations (10) and (21) imply
\[
\begin{aligned}
 G(u,0)&=v^{-8}G_0(X(u)),\\
 F(u,0)&=v^{-12}F_0(X(u)).
\end{aligned}
\tag{23}
\]
Both expressions must be regular at \(u=0\).

The rational function \(X(u)\) cannot tend to infinity: monicity of
\(G_0\) would make the first expression in (23) still more singular.
It therefore has a finite limit \(\xi\).  Regularity in (23) forces
\[
 G_0(\xi)=F_0(\xi)=0,
\]
contradicting (22).  Thus no rational center can lift this normalized
cusp to a pair in \(\mathbf C[u,y]^2\).

This argument is independent of the line criterion and proves the
following general lemma.

> **Finite-cusp lift obstruction.**  If a normalized weighted cusp
> has
> \[
> f=v^{-M}F_0(vw),\qquad
> g=v^{-N}G_0(vw)
> \]
> with monic \(F_0,G_0\) and
> \(\operatorname {Res}(F_0,G_0)\ne0\), then it admits no polynomial
> lift through a rational depressing center.

## 5. The entire Davenport--Stothers extremal stratum is isotrivial

The preceding cusp is not an isolated lucky certificate.  There is a
structural reason that no rational deformation of a
Davenport--Stothers extremal pair can enter the escape range (14).

Let \(K\) be a characteristic-zero function field and suppose
\[
 p,q\in K[w],\qquad
 \deg p=12,\quad\deg q=8,\quad
 \deg(p^2-q^3)\leq5,
\tag{24}
\]
with \(p,q\) monic.  A nonzero normalized Jacobian implies
\(\gcd(p,q)=1\).  Indeed, if a nonconstant
\(s\in K[w]\) divided both \(p\) and \(q\), then it would divide
\[
 \partial_vp\,\partial_wq-\partial_wp\,\partial_vq.
\]
The normalized bracket is a nonzero element of \(K\), independent of
\(w\), so this is impossible.

Apply the polynomial \(abc\) theorem over an algebraic closure of
\(K\) to
\[
 p^2-q^3-(p^2-q^3)=0.
\]
It gives
\[
 24\leq
 \deg\operatorname {rad}\bigl(pq(p^2-q^3)\bigr)-1.
\tag{25}
\]
The radical on the right has degree at most
\[
 12+8+5=25.
\]
Equality is forced everywhere.  Therefore
\[
 \deg(p^2-q^3)=5,
\]
and \(p,q,p^2-q^3\) are squarefree and pairwise coprime.

The rational function
\[
 R=\frac{p^2}{q^3}
\tag{26}
\]
has degree \(24\) and the exact ramification passport
\[
 [2^{12}],\qquad[3^8],\qquad[19,1^5]
\tag{27}
\]
over \(0,\infty,1\), respectively.  Indeed, the finite roots account
for the \(2^{12},3^8,1^5\) entries, while at \(w=\infty\),
\[
 R-1=\frac{p^2-q^3}{q^3}
\]
vanishes to order \(19\).  The ramification contribution is
\[
 12+16+18=46=2\cdot24-2.
\]
Riemann--Hurwitz leaves no fourth branch value.

There are only finitely many degree-24 covers with the fixed passport
(27), up to a source projective transformation.  Hence every
rational family satisfying (24) is isotrivial.  The point of
ramification index \(19\) is unique, so polynomial equivalence
preserves infinity and the source change is affine.  If a fixed
representative \(P_0,Q_0\) is monic and \(Q_0\) is depressed, every
other monic depressed representative has the form
\[
\begin{aligned}
 p(w)&=\alpha^{-12}P_0(\alpha w),\\
 q(w)&=\alpha^{-8}Q_0(\alpha w).
\end{aligned}
\tag{28}
\]
The translation part vanishes because it would create the
\(w^7\)-coefficient \(8\beta/\alpha\) in \(q\).  With
\(\tau=\alpha^{-1}\), every coefficient of deficit \(j\) is a
constant times \(\tau^j\).

The terminal Laurent coefficient is consequently
\[
 A_7=C\tau^{19}.
\tag{29}
\]
Here \(C\ne0\), since otherwise the normalized bracket would vanish.
Let \(\delta\) be the gcd of the deficits whose fixed coefficients
are nonzero.  The coefficient field is
\(\mathbf C(\tau^\delta)\).  But \(A_7\) is a polynomial in those
coefficients, so \(\tau^{19}\) belongs to that field.  Cyclic field
descent gives \(\delta\mid19\).  Since no nonzero deficit is as large
as \(19\), one has \(\delta=1\).  Thus the coefficient field is
\(\mathbf C(\tau)\).

If this family also has the pure-power one-pole time, then
\[
 C\tau^{19}=A+Bv^{-n},
\qquad \mathbf C(\tau)=\mathbf C(v).
\tag{30}
\]
The parameters differ by a Möbius transformation.  Comparing map
degrees gives \(n=19\).  The right side has no critical point away
from its pole; the derivative of the left side vanishes at the zero
of \(\tau\).  Hence that zero must be \(v=\infty\), and after a
constant rescaling
\[
 \tau=v^{-1}.
\tag{31}
\]
Every nonconstant coefficient then has weighted pole scale one:
\[
 \boxed{\frac{n}{\rho}=19.}
\tag{32}
\]

This proves:

> **Extremal-stratum obstruction.**  No coprime rational deformation
> with
> \(\deg_w(p^2-q^3)\leq5\) can have one-pole ratio below \(3\).
> Every nonzero-Jacobian one-pole deformation is isotrivial and has
> ratio exactly \(19\).

Thus a possible \((12,8)\) counterexample cannot lie on the
Davenport--Stothers equality stratum.  It must arise on a secondary
non-homogeneous boundary after the leading extremal pair has itself
degenerated.

There is a precise description of that secondary boundary.  The
polynomial \(abc\) argument also proves the sub-extremal lemma
\[
 \deg(p^2-q^3)\leq4
 \quad\Longrightarrow\quad
 p^2=q^3.
\tag{33}
\]
No coprimality hypothesis is needed.  If the difference were
nonzero, let \(S=\gcd(p^2,q^3)\), of degree \(s\), and divide the
three-term equation by \(S\).  Polynomial \(abc\) would give
\[
 24-s
 \leq
 \deg\operatorname {rad}
 \left(\frac{p^2q^3(p^2-q^3)}{S^3}\right)-1
 \leq20+(4-s)-1,
\]
which is impossible.  Unique factorization and monicity then give
\[
 \boxed{p=P^3,\qquad q=P^2}
\tag{34}
\]
for a monic quartic \(P\).

This applies directly to a putative low-ratio pole.  In the
zero-upper-constant slice,
\[
 f=s^{12}+\sum_{\ell\geq1}A_\ell s^{-\ell},
\]
so \(A_1=\cdots=A_7=0\) in a weighted leading form implies
\(\deg(f^2-g^3)\leq4\).  At a coefficient pole of scale \(\rho\),
the six conserved levels have lower weight than their leading
homogeneous terms.  If
\(\operatorname {pole}(A_7)<3\rho\), then it is certainly less than
the natural terminal weight \(19\rho\), so the leading \(A_7\) also
vanishes.  Equations (33)--(34) show that the weighted limit must be
\[
 f_0=P^3,\qquad g_0=P^2.
\tag{35}
\]
Depression of \(g_0\) makes
\[
 P=w^4+Aw^2+Bw+C.
\tag{36}
\]

Hence the danger locus is not an unknown component of a large
seven-variable resultant.  It is the explicit three-dimensional
common-quartic locus (35)--(36).  The next calculation should be the
normal cone and successive invariant equations along this locus.

## 6. Counterexample status and next exact target

The cusp (16) is an exact nonzero-Jacobian, one-pole solution
of the normalized \((12,8)\) system recorded in this project.  It
shows that the normalized equations themselves have highly
nontrivial solutions and that searching only for an inconsistency in
the six Laurent levels cannot close the frontier.

It is not a polynomial counterexample: both the threshold argument
and the resultant obstruction exclude its lift.  A genuine
counterexample candidate must instead come from a non-homogeneous
boundary arc satisfying all of the following:

1. \(A_1,\ldots,A_6\) are constant;
2. \(A_7\) has exactly one pole and no other critical point;
3. its pole ratio is strictly below \(3\);
4. its depressing-center limit avoids the finite-cusp resultant
   obstruction.

Section 5 removes the whole smooth Davenport--Stothers equality
stratum from this list and identifies every possible low-ratio
weighted limit with the common-quartic locus (35).  The sharply
constrained remaining problem is therefore its normal-cone
compactification, equivalently the collision boundary of passport
\([2^{12}],[3^8],[19,1^5]\).  That is the appropriate next target,
rather than an unrestricted coefficient search.
