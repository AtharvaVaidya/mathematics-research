# The standard-system escape mechanism

Date: 24 July 2026

This note reformulates the all-degree obstruction in the finite standard
system of Guccione--Guccione--Valqui.  It does not prove the plane Jacobian
conjecture.  Its purpose is to identify exactly why a finite-etale or
monodromy argument by itself cannot finish the problem, and to connect the
finite system with the weighted boundary problem already visible in the
radial calculations.

Let \(1<n,m\), with neither dividing the other, and put
\[
N=m+n-2,\qquad W=N+1=m+n-1.
\]
Write
\[
Z=x+Z_{-1}x^{-1}+\cdots+Z_{-N}x^{-N}+\cdots .
\]
The standard system has variables \(Z_{-1},\ldots,Z_{-N}\), parameters
\(\lambda_0=1,\lambda_1,\ldots,\lambda_N\), and last inhomogeneous term
\(Y\).  Its equations are
\[
\begin{aligned}
(Z^n)_{-i}&=0 &&(1\le i<m),\\
\left(\sum_{k=0}^N\lambda_k Z^{m-k}\right)_{m-i-1}&=0
 &&(m\le i<N),\\
\left(\sum_{k=0}^N\lambda_k Z^{m-k}\right)_{1-n}+Y&=0.
\end{aligned}
\tag{1}
\]
A counterexample of degrees \((n,m)\) gives a solution of (1) in
\(\mathbb C[Y]^N\), with
\(\deg_Y Z_{-j}\le j+1\).

## 1. Exact weighted structure

Give the symbols the weights
\[
\operatorname{wt}(Z_{-j})=j+1,\qquad
\operatorname{wt}(\lambda_k)=k,\qquad
\operatorname{wt}(Y)=W.
\tag{2}
\]
If a coefficient of \(Z^{m-k}\) has \(x\)-exponent \(r\), its coefficient
weight is \(m-k-r\).  After multiplication by \(\lambda_k\), its total
weight is \(m-r\), independent of \(k\).  Hence every equation in (1) is
weighted homogeneous:
\[
\operatorname{wt}(E_i)=
\begin{cases}
n+i,&1\le i<m,\\
i+1,&m\le i\le N.
\end{cases}
\tag{3}
\]

Let
\[
\mathcal J=\det\left(\frac{\partial E_i}{\partial Z_{-j}}\right)_
{1\le i,j\le N}.
\]
Subtracting the sum of the variable weights from the sum of the equation
weights gives
\[
\operatorname{wt}(\mathcal J)=(m-1)(n-1)=:D. \tag{4}
\]
For a genuine Keller solution \(C_{-j}(Y)\), Theorem 2.3 of the standard
system paper makes this matrix invertible over \(\mathbb C[Y]\).
Consequently
\[
\mathcal J(C(Y),\lambda)\in\mathbb C^\times. \tag{5}
\]

## 2. The forced arc to weighted infinity

For \(t\ne0\), set
\[
\lambda_k(t)=t^k\lambda_k,\qquad
\widetilde C_{-j}(t)
=t^{j+1}C_{-j}(t^{-W}). \tag{6}
\]
Weighted homogeneity shows exactly that
\[
E(\widetilde C(t),\lambda(t),1)=0. \tag{7}
\]
Moreover, (4)--(5) give
\[
\mathcal J(\widetilde C(t),\lambda(t))
=t^D\mathcal J(C(t^{-W}),\lambda)
=\delta t^D,\qquad\delta\in\mathbb C^\times. \tag{8}
\]

The arc (6) cannot have a finite limit as \(t\to0\).  Indeed, if every
\(\widetilde C_{-j}\) were regular at zero, then the degree bound implies
that its limit is zero except possibly for a linear \(Y\)-term in
\(C_{-N}\).  The first block equation with \(i=m-1\) contains
\(nC_{-N}\), forcing that last limit to vanish as well.  The last equation
would then read \(1=0\).

Thus every counterexample produces an escaping Laurent arc in the fiber
over
\[
(\lambda_1,\ldots,\lambda_N;Y)=(0,\ldots,0;1),
\]
and its equation-Jacobian vanishes to the exact order \(D\).  This gives a
precise limitation of the tempting monodromy argument: although the
counterexample section is etale over the affine \(Y\)-line, the total
standard-system family is not proper at the homogeneous parameter.  The
section must leave every affine chart.

The all-degree problem can therefore be restated as follows:

> Classify the weighted-projective boundary arcs of (1) with determinant
> order exactly \((m-1)(n-1)\), and show that none obeys the coefficient
> degree bounds coming from a Keller map.

This is the finite-system counterpart of the dicritical-tree problem and
of the radial Kummer lattice.  It is a boundary-classification problem,
not a request for a larger affine Groebner basis.

## 3. The smallest example

For \((n,m)=(2,3)\), \(N=3\), the system reduces to
\[
2Z_{-2}=0,\qquad
2Z_{-3}+Z_{-1}^2=0,
\]
\[
3Z_{-3}+3Z_{-1}^2
+2\lambda_1Z_{-2}+\lambda_2Z_{-1}+Y=0.
\]
Eliminating \(Z_{-2},Z_{-3}\) leaves
\[
\frac32 Z_{-1}^2+\lambda_2Z_{-1}+Y=0. \tag{9}
\]
No polynomial \(Z_{-1}(Y)\) satisfies (9): its left side has even positive
degree if \(Z_{-1}\) is nonconstant, and has a surviving \(Y\)-term if it
is constant.  The equation-Jacobian is
\[
4(3Z_{-1}+\lambda_2),
\]
of weight \(D=2\).  This toy case displays both mechanisms transparently:
the affine section is impossible, while the algebraic roots escape with a
square-root pole under (6).

The exact weight arithmetic and the \((2,3)\) calculation are checked by
`verify_standard_system_weights.py`.

## 4. Classification of the first boundary slope

There is a complete description of the homogeneous base locus seen by
an escaping polynomial section.  Put
\[
g=\gcd(n,m).
\]
For a putative section define
\[
h=\max_{1\le j\le N}
\frac{\deg_Y C_{-j}}{j+1}.
\tag{10}
\]
Escape is equivalent to \(h>1/W\), while the coefficient bounds give
\(h\le1\).  Let \(\gamma_{-j}\) be the coefficient of
\(Y^{h(j+1)}\) in \(C_{-j}\), interpreted as zero when
\(h(j+1)\notin\mathbb Z\) or the maximum is not attained.

In an equation of weight \(e\), the \(\lambda_k\)-summand has
\(Y\)-degree at most \(h(e-k)<he\) for \(k>0\).  In the last equation
the inhomogeneous \(Y\)-term has degree one, whereas \(hW>1\).
Consequently the coefficient of degree \(he\) in every equation is
the homogeneous system with \(\lambda_1=\cdots=\lambda_N=Y=0\),
evaluated at \(\gamma\).

> **Common-root boundary lemma.**  The zero locus of that homogeneous
> system is exactly
> \[
> \Gamma^g=R(x),\qquad
> R=x^g+r_{g-2}x^{g-2}+\cdots+r_0.
> \tag{11}
> \]
> Thus it is an affine cone of dimension \(g-1\), parametrized by the
> coefficients of the monic polynomial \(R\) with vanishing
> \(x^{g-1}\)-coefficient.  In particular, it is just the origin when
> \(g=1\).

Here is a self-contained proof.  Extend
\(\Gamma=x+\gamma_{-1}x^{-1}+\cdots\) uniquely beyond the coefficients
occurring in the finite system so that
\[
P=\Gamma^n\in k[x].
\]
The second homogeneous block says that the coefficients of
\(\Gamma^m\) at \(x^{-1},\ldots,x^{1-n}\) vanish.  Write
\[
\Gamma^m=Q+F,\qquad Q\in k[x],\quad \deg_xF\le-n.
\]
Then
\[
mP'Q-nPQ'
=nF'\Gamma^n-mnF\Gamma^{n-1}\Gamma'. \tag{12}
\]
The left side is a polynomial and the right side has strictly negative
\(x\)-degree, so both sides vanish.  It follows that
\((P^m/Q^n)'=0\).  Monicity and unique factorization give
\[
P=R^{n/g},\qquad Q=R^{m/g},
\]
and the chosen monic Laurent roots then give \(\Gamma^g=R\).
The converse is immediate.

This lemma shows both the reach and the limitation of a slope-only
argument.  It proves at once that coprime \((n,m)\) admit no escaping
section.  But when \(g>1\), which includes every degree pair still
relevant to a hypothetical counterexample, the boundary cone is
positive-dimensional.

There is a concrete coefficient-bound-compatible counterpattern.
Choose
\[
R=x^g+a,\qquad
\Gamma=(x^g+a)^{1/g}
=x+\sum_{\ell\ge1}\binom{1/g}{\ell}
 a^\ell x^{1-\ell g}. \tag{13}
\]
Hence, for \(\ell g\le W\),
\[
\gamma_{-(\ell g-1)}
=\binom{1/g}{\ell}a^\ell,
\qquad
\gamma_{-j}=0\quad(g\nmid j+1). \tag{14}
\]
Taking these as the coefficients of the maximal allowed powers
\(Y^{j+1}\) gives the Laurent valuation
\[
\operatorname{ord}_t\widetilde C_{-j}
=-(W-1)(j+1)
\quad\text{whenever }\gamma_{-j}\ne0. \tag{15}
\]
All first weighted initial equations vanish by (11).  Moreover the
homogeneous equation-Jacobian vanishes on this pattern: the
\((g-1)\)-dimensional tangent space obtained by varying \(R\) lies in
the kernel of the linearized homogeneous system.

The exact determinant order is also numerically compatible with this
pattern.  This is clearest in the reciprocal coordinate
\[
\tau=Y^{-1},\qquad
u_{-j}(\tau)=\tau^{j+1}C_{-j}(\tau^{-1}).
\tag{16}
\]
The coefficient bounds are precisely
\[
u_{-j}\in k[\tau],\qquad \deg_\tau u_{-j}\le j+1.
\tag{17}
\]
After multiplying an equation of weight \(e_i\) by \(\tau^{e_i}\),
the parameters become \(\lambda_k\tau^k\), and the last inhomogeneous
term becomes \(\tau^{W-1}\).  Similarly, (5) becomes
\[
\widehat{\mathcal J}(\tau)
:=\mathcal J\bigl(u(\tau),
\lambda_1\tau,\ldots,\lambda_N\tau^N\bigr)
=\delta\tau^D. \tag{18}
\]
Every monomial of \(\widehat{\mathcal J}\) has \(\tau\)-degree at most
\(D\), because its weighted degree is \(D\) and (17) bounds the degree
of each substituted variable by its weight.  Thus the demanded order
\(D\) is exactly the largest order allowed by the coefficient bounds;
it is not too large.  At \(\tau=0\), (18) starts with
\(\mathcal J_0(\gamma)=0\), as forced by the tangent space to (11).

Therefore weights, first slopes, and the number \(D\) alone cannot
exclude the boundary arc.  They reduce the problem to a higher-contact
statement:

> **Residual normal-contact lemma.**  There is no tuple of polynomials
> \(u_{-j}(\tau)\) satisfying (17), based at a nonzero point of the
> common-root cone (11), that solves the reciprocal standard equations
> and has determinant contact (18).

This is strictly sharper than the original affine formulation: any
proof must now use the normal equations to the common-root cone, not
only the global weighted degrees.  Conversely, proving the residual
normal-contact lemma for every \(g>1\) closes the weighted-escape route.

## 5. The equation-Jacobian is a derivative resultant

The determinant has a more concrete interpretation.  Let \(C\) be an
actual standard-system solution and let \(P,Q,F\) be its associated
series, so
\[
P=C^n\in k[x],\qquad
Q=\sum_k\lambda_kC^{m-k}+F\in k[x],\qquad
\deg_xF\le1-n.
\]
Put
\[
G(C)=\sum_k\lambda_k(m-k)C^{m-k-1}.
\]
The linear map represented by the equation-Jacobian sends a negative
Laurent jet \(U\) to
\[
U\longmapsto
\left(\Pi_{m-1}(nC^{n-1}U),\,
      \Pi_{n-1}(G(C)U)\right). \tag{19}
\]
Make the unipotent triangular jet change \(U=C_xV\).  Since
\[
P_x=nC^{n-1}C_x,\qquad
G(C)C_x=Q_x-F_x
\]
and \(F_xV\) starts below all coefficients retained by
\(\Pi_{n-1}\), (19) becomes
\[
V\longmapsto
\left(\Pi_{m-1}(P_xV),\,
      \Pi_{n-1}(Q_xV)\right). \tag{20}
\]
Up to reversing coefficient order, (20) is the Sylvester map for
\(P_x\) and \(Q_x\).  Both coefficient reversals and the change by
\(C_x=1+O(x^{-2})\) have determinant a constant unit.  Therefore
\[
\boxed{\ \mathcal J=\pm\operatorname{Res}_x(P_x,Q_x)\ }. \tag{21}
\]
The sign depends only on the row and coefficient conventions.  In the
\((2,3)\) example it is positive.

Now assume \(n<m\), write \(n=ga,\ m=gb\), and take a point of the
common-root cone:
\[
P_0=R^a,\qquad Q_0=R^b.
\]
Then
\[
A_0:=(P_0)_x=aR^{a-1}R',\qquad
B_0:=(Q_0)_x=bR^{b-1}R'
=H_0A_0,
\quad H_0=\frac baR^{b-a}. \tag{22}
\]
Thus the Sylvester matrix has corank
\[
\deg\gcd(A_0,B_0)=\deg A_0=n-1. \tag{23}
\]
This is substantially larger than the \(g-1\) tangent space of the
reduced common-root cone: the normal cone itself is nonreduced.

The first transverse determinant is the classical Sylvester remainder.
For
\[
A=A_0+\epsilon A_1+\cdots,\qquad
B=B_0+\epsilon B_1+\cdots,
\]
let
\[
K_1\equiv B_1-H_0A_1\pmod{A_0},\qquad \deg K_1<n-1. \tag{24}
\]
If \(K_1\) is coprime to \(A_0\), then, up to a nonzero scalar,
\[
\operatorname{Res}(A,B)
=\epsilon^{\,n-1}\operatorname{Res}(A_0,K_1)
+O(\epsilon^n). \tag{25}
\]
Hence a generic transverse arc has determinant order \(n-1\).  Higher
order is exactly higher contact of the Euclidean remainder with the
zero scheme of \(A_0\).

This admits a rootwise form.  Over an algebraic closure, Hensel-factor
\(A\) according to the roots of \(R\) and \(R'\).  If \(R\) and \(R'\)
are squarefree with disjoint zero sets, then
\[
\operatorname{ord}_\tau\mathcal J
=\sum_{R(\alpha)=0} I_{(\alpha,0)}(A,B)
+ \sum_{R'(\beta)=0} I_{(\beta,0)}(A,B). \tag{26}
\]
At a root of \(R\), the special-fiber multiplicities of \(A,B\) are
\(a-1,b-1\); at a simple root of \(R'\), both are one.  For the
maximally symmetric example \(R=x^g+c\), \(c\ne0\), the \(g\) roots of
\(R\) are simple, while \(R'=gx^{g-1}\) gives one additional critical
cluster of multiplicity \(g-1\).  Thus (26) becomes
\[
\operatorname{ord}_\tau\mathcal J
=\sum_{\alpha^g=-c}I_{(\alpha,0)}(A,B)+I_{(0,0)}(A,B). \tag{27}
\]

There is, however, no Hessian or resultant upper bound smaller than
\(D\).  At any common-root point, keep \(C\) fixed and turn on only the
standard parameter \(\lambda_{m-1}=L\).  The lower Jacobian symbol is
then
\[
mC^{m-1}+L.
\]
At \(L=0\), its \(n-1\) rows lie in the span of the upper block, by
(22).  Subtract those fixed row combinations.  Every lower row is now
divisible by \(L\).  The coefficient of \(L^{n-1}\) is obtained by
taking the constant \(L\)-entry in all lower rows; the complementary
\((m-1)\)-square upper block is triangular with diagonal \(n\).
Consequently
\[
\boxed{\ \det J(C,\lambda_{m-1}=L)
=\pm n^{m-1}L^{n-1}\ }. \tag{28}
\]
Putting \(L=\lambda_{m-1}\tau^{m-1}\) gives
\[
\operatorname{ord}_\tau\det J=(n-1)(m-1)=D. \tag{29}
\]
Thus an allowed normal parameter already saturates the required
determinant order.  In the rootwise model for \(R=x^g+c\), it assigns
contact \((m-1)(a-1)\) to each of the \(g\) root clusters and
\((m-1)(g-1)\) to the critical cluster; their sum is \(D\).

Equation (28) is only an ambient normal-cone arc: with \(C\) fixed, the
remaining standard equations need not vanish.  That distinction is
now the exact obstruction.  A determinant-only argument cannot close
the problem.

> **Sharpened residual lemma.**  Along every reciprocal
> standard-system solution based at a nonzero common-root point, at
> least one Hensel factor in (26) has contact strictly smaller than its
> maximal \((m-1)\deg A_{\mathrm{factor}}\).  Equivalently, after the
> normal equations and common-root tangent directions are eliminated,
> the Sylvester remainder must appear before order \(m-1\) on at least
> one root or critical-point cluster.

By (21) and (26), this lemma would force
\(\operatorname{ord}_\tau\mathcal J<D\), contradicting (18).  Formula
(28) shows why its proof must use the standard equations themselves,
especially the last inhomogeneous term, rather than weights, the
Hessian, or the derivative resultant in isolation.

## 6. The nonreduced normal cone and its first obstruction

The saturating direction (28) is not tangent to the standard-system
fiber.  This exposes the scheme structure that a successful argument
has to control.

Continue to assume \(n=ga<m=gb\).  At
\[
C_0^g=R,\qquad P_0=C_0^n=R^a,
\]
the kernel of the homogeneous equation-Jacobian has dimension \(n-1\).
It has a simple parametrization: choose an arbitrary polynomial
\[
T=\dot P,\qquad \deg T\le n-2,
\]
and solve
\[
T=nC_0^{n-1}\dot C. \tag{30}
\]
The first block then vanishes by construction.  The second linearized
power is
\[
mC_0^{m-1}\dot C
=\frac mn C_0^{m-n}T
=\frac ba R^{b-a}T\in k[x], \tag{31}
\]
so its retained negative coefficients vanish as well.  This accounts
for the full \(n-1\)-dimensional kernel.

Only a \(g-1\)-dimensional subspace is tangent to the reduced
common-root cone.  It consists of
\[
T=aR^{a-1}\dot R,\qquad \deg\dot R\le g-2. \tag{32}
\]
The quotient, of dimension \(n-g\), is a space of infinitesimal normal
directions that exist only because the homogeneous fiber is
nonreduced.

The first higher normal equation is explicit.  In the model with all
\(\lambda_k=0\), deform
\[
P_\epsilon=R^a+\epsilon T.
\]
Then
\[
P_\epsilon^{\,b/a}
=\sum_{\ell\ge0}
\binom{b/a}{\ell}
\epsilon^\ell R^{\,b-a\ell}T^\ell. \tag{33}
\]
Since \(\gcd(a,b)=1\) and \(a>1\), put
\[
\ell_0=\left\lfloor\frac ba\right\rfloor+1.
\]
Every term with \(\ell<\ell_0\) is polynomial.  The first possible
normal obstruction is
\[
\binom{b/a}{\ell_0}
\left[R^{\,b-a\ell_0}T^{\ell_0}\right]_
{x^{-1},\ldots,x^{1-n}}. \tag{34}
\]
For a generic non-tangent \(T\), (34) is nonzero.  The corresponding
Sylvester remainder first appears at order \(\ell_0\), and (25) gives
the generic determinant contact
\[
(n-1)\ell_0, \tag{35}
\]
which is far below \(D=(n-1)(m-1)\).

Formula (34) also explains the rootwise strata.  At a simple root
\(\alpha\) of \(R\), put \(s_\alpha=\operatorname{ord}_\alpha T\).
The \(\ell\)-th term of (33) has local exponent
\[
b-(a-s_\alpha)\ell.
\]
If \(s_\alpha<a\), its first pole occurs at
\[
\ell_\alpha=
\left\lfloor\frac{b}{a-s_\alpha}\right\rfloor+1. \tag{36}
\]
Thus extra vanishing of \(T\) at selected roots delays precisely those
Hensel factors.  These are the special local-contact strata that replace
a single generic Hessian calculation.

Finally, take the ambient saturating parameter from (28).  At order
\(m-1\), \(\lambda_{m-1}\) contributes the negative band of \(C_0\)
itself to the second block.  A linear correction whose first block
vanishes is of the form (30), and its second contribution is the
polynomial (31).  It therefore cannot cancel that negative band.  For a
nonzero point of the common-root cone, \(C_0\) is not polynomial and
its first negative term lies in the retained band.  Hence
\[
\partial_{\lambda_{m-1}}E(C_0)
\notin\operatorname{im}J(C_0). \tag{37}
\]

So the one-step saturator (28) is excluded by the equations, but the
problem is not yet closed.  Earlier nilpotent normal jets \(T\) can
have vanishing linear equation and only meet their first obstruction
at (34); successive \(\lambda_k\)'s and higher jets may cancel these
obstructions.  Any genuine boundary arc with contact \(D\) must realize
such a cascade.  A complete proof now amounts to showing that this
cascade cannot delay every local remainder in (26) all the way to
order \(m-1\).

## 7. A binomial countermodel, and why it is a translation gauge

The squarefree hypothesis alone does not make the approximate-root
induction valid when the \(\lambda_k\)'s are present.  There is an
explicit formal countermodel through every order retained by the finite
system.

Let
\[
N=m+n-2,\qquad q_*=\left\lfloor\frac{N}{n}\right\rfloor,
\]
choose any \(R\), squarefree or not, and put
\[
P(\tau)=R^a+c\tau^n,\qquad C=P^{1/n}. \tag{38}
\]
For \(0\le q\le q_*\), set
\[
\lambda_{nq}=\binom{b/a}{q}(-c)^q,
\qquad \lambda_k=0\quad(n\nmid k). \tag{39}
\]
Then
\[
\begin{aligned}
\sum_{q=0}^{q_*}
\lambda_{nq}\tau^{nq}C^{m-nq}
&=
\sum_{q=0}^{q_*}
\binom{b/a}{q}(-c\tau^n)^q
P^{\,b/a-q}\\
&\equiv (P-c\tau^n)^{b/a}
=R^b
\pmod{\tau^{N+1}}. \tag{40}
\end{aligned}
\]
Indeed, the omitted term starts at
\[
n(q_*+1)>N.
\]
Thus all retained negative Laurent coefficients vanish through order
\(N\), although \(P\) in (38) is not an \(a\)-th power in
\(k[[\tau]][x]\).  The model fails the reciprocal standard system only
at the final inhomogeneous equation: its \(x^{1-n}\)-coefficient at
order \(\tau^N\) is still zero rather than \(-1\).

This disproves an unnormalized claim that the Laurent gap forces every
coefficient of \(P\) to be absorbed into an \(a\)-th root before the
forcing order.  It also works for repeated-root \(R\), so separating
squarefree and repeated roots does not remove it.

The countermodel is nevertheless a gauge orbit, not a candidate
Keller arc.  The reciprocal term \(c\tau^n\) is exactly a global
constant \(c\) in the original polynomial \(P(x,Y)\).  Replacing the
target coordinate by \(P-c\) is an allowed affine target translation.
Writing the old powers of \(P\) in terms of the translated monic root
produces precisely the binomial coefficients (39):
\[
P^{(m-k)/n}
=\sum_{q\ge0}
\binom{(m-k)/n}{q}
c^q(P-c)^{(m-k)/n-q}. \tag{41}
\]
Consequently target translation acts triangularly on each congruence
class
\[
\lambda_k,\lambda_{k+n},\lambda_{k+2n},\ldots. \tag{42}
\]
The family (38)--(39) is the orbit of the trivial common-root solution
\((P-c)=R^a\).

This has two implications.

1. Any approximate-root induction must first quotient the translation
   action (42), for example by fixing the global constant of the
   original \(P\).  Without that normalization the induction is
   false, even for squarefree \(R\).
2. The final \(\tau^N x^{1-n}\) forcing is unchanged by this target
   translation.  Hence the countermodel cannot satisfy the last
   equation; it only shows that the preceding homogeneous gap does not
   detect a removable constant shift.

After fixing this gauge, the unresolved question is whether a different
combination of genuine \(x\)-dependent normal coefficients and
translation-invariant combinations of the \(\lambda_k\)'s can reproduce
the same cancellation cascade.  The Laurent-gap lemma (34) remains the
natural tool, but it must be applied to invariants of (42), not to the
raw coefficients of \(P\).

In fact there is a larger formal reparametrization countermodel, so
target translation is not the whole story.  Fix \(1\le c\le a\), put
\[
z=\frac{\tau^g}{R},
\qquad
P=R^a(1+\kappa z^c)
=R^a+\kappa\tau^{gc}R^{a-c}. \tag{43}
\]
Every monomial in (43) obeys the reciprocal total-degree bound \(n=ga\).
For a parameter with index \(k=gq\),
\[
\tau^{gq}C^{m-gq}
=R^bz^q(1+\kappa z^c)^{(b-q)/a}. \tag{44}
\]
Let
\[
Q_*=\left\lfloor\frac Ng\right\rfloor=a+b-1.
\]
There are unique constants \(\mu_0,\ldots,\mu_{Q_*}\), with
\(\mu_0=1\), such that
\[
\sum_{q=0}^{Q_*}
\mu_qz^q(1+\kappa z^c)^{(b-q)/a}
=1+O(z^{Q_*+1}). \tag{45}
\]
This is triangular: the \(q\)-th summand begins with \(\mu_qz^q\).
Setting
\[
\lambda_{gq}=\mu_q,\qquad \lambda_k=0\quad(g\nmid k)
\]
makes the second standard expression equal to
\[
R^b+O\!\left(\tau^{g(Q_*+1)}\right)
=R^b+O(\tau^{N+2}). \tag{46}
\]
Thus it is polynomial through and beyond the entire retained range.
When \(c=a\), (43) is the constant-translation model.  For \(c<a\),
the extra term is genuinely \(x\)-dependent and cannot be removed by
an affine target translation.

The reparametrization has a useful exact interpretation.  Let \(y(w)\)
be the formal solution with \(y(0)=1\) of
\[
y^a+\kappa w^cy^{a-c}=1. \tag{47}
\]
For
\[
D=C^g=R(1+\kappa z^c)^{1/a},
\qquad w=\frac{\tau^g}{D},
\]
one has \(R=Dy(w)\).  Hence
\[
R^b=D^by(w)^b
=\sum_{q\ge0}\mu_q\tau^{gq}D^{b-q}. \tag{48}
\]
Equation (45) is simply the finite truncation of this formal change of
the approximate root \(D\).

Consequently even a translation-normalized, squarefree-\(R\)
approximate-root induction is false if it tries to eliminate all
normal coefficients before the forcing order.  The full
\(g\)-multiple parameter sector is large enough to hide the genuine
homogeneous deformations (43), but it is not all coordinate gauge.
For a fixed pair
\[
P=R^aA(z),\qquad Q=R^bB(z),
\]
an honest change \(R\mapsto R\phi(z)\) can normalize one of \(A,B\),
while the relative unit
\[
\mathcal I=\frac{B^a}{A^b}=\frac{Q^a}{P^b}
\]
survives up to tangent-to-the-identity composition.  Its order and
leading coefficient are quotient invariants.  Thus (43) with \(c<a\)
is physical relative \(g\)-sector data, not the orbit of the pure-power
pair.  The exact quotient and a degree-bound-compatible countermodel
are proved in
`STANDARD_SYSTEM_G_MULTIPLE_REPARAMETRIZATION_QUOTIENT.md`.

Like the constant model, (43) still cannot supply the final
\(\tau^Nx^{1-n}\) term.  This shifts attention from divisibility of
individual normal coefficients to the interaction between the retained
relative unit and the nonzero residue classes of \(\tau\)-order modulo
\(g\).

## 8. The mod-\(g\) normal equation and branch residues

There are two exact ways to isolate the residue classes suggested by
(43)--(48).  First group the second standard expression according to
\(k=gq+r\).  If
\[
D=C^g,\qquad w=\frac{\tau^g}{D},\qquad
A_r(w)=\sum_q\lambda_{gq+r}w^q,
\]
then
\[
\sum_{k=0}^N\lambda_k\tau^kC^{m-k}
=\sum_{r=0}^{g-1}\tau^rC^{-r}D^bA_r(w). \tag{49}
\]
Every \(g\)-sector countermodel above lies in the \(r=0\)
sector.  On the other hand,
\[
N=g(a+b)-2\equiv-2\pmod g. \tag{50}
\]
Thus for \(g>2\) the final forcing lies in the nonzero
\(r=g-2\) class.  When \(g=2\), it lies in the resonant zero class and
requires a separate local argument.

Formula (49) is an exact decomposition, but it is not yet a normal-form
theorem.  A change of approximate root
\(D\mapsto D\phi(\tau^g/D)\) can produce a new root whose coefficients
have non-\(g\)-multiple \(\tau\)-orders.  Such coefficients mix the
apparent classes in (49).  A proof therefore cannot simply declare the
summands with different \(r\)'s independent.

The Keller identity gives an invariant version of the same congruence.
For an original Keller pair \(p,q\), put
\[
P(X,\tau)=\tau^np(X/\tau,1/\tau),\qquad
Q(X,\tau)=\tau^mq(X/\tau,1/\tau).
\]
The chain rule gives the exact homogenized identity
\[
\boxed{\;
\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X
=-c\tau^N .
\;} \tag{51}
\]
At the common-root boundary \(P_0=R^a,\ Q_0=R^b\), consider a first
graded deformation of order \(d<N\):
\[
P=R^a(1+\epsilon\tau^dU)+O(\epsilon^2),\qquad
Q=R^b(1+\epsilon\tau^dV)+O(\epsilon^2).
\]
Writing
\[
Z=aV-bU,
\]
the coefficient of \(\epsilon\tau^d\) in (51) is
\[
R^{a+b-1}\bigl(gRZ'+dR'Z\bigr)=0. \tag{52}
\]
Consequently
\[
Z=\kappa R^{-d/g}. \tag{53}
\]
If \(R\) is squarefree, rationality of \(Z\) forces either \(Z=0\) or
\(g\mid d\).  More generally, if
\[
R=\prod_i(X-\alpha_i)^{e_i},
\]
then (53) is rational exactly when \(g\mid de_i\) for every \(i\).
After choosing \(g\) minimally, so that
\(\gcd(g,e_1,e_2,\ldots)=1\), this again forces \(g\mid d\).
If the multiplicities have a common divisor with \(g\), the Kummer
exponent was not minimal and should first be reduced.

Equation (52) therefore proves a genuine mod-\(g\) statement: every
nonzero transverse relative deformation occurs at a \(g\)-multiple
order and is precisely the resonance already realized by (43).  It
does not, however, eliminate the case \(Z=0\).  Indeed, for every
polynomial \(T\) in the full nonreduced kernel (30), take
\[
U=\frac{T}{R^a},\qquad
V=\frac ba\,\frac{T}{R^a}.
\]
Then \(Z=0\), although \(T\) need not be divisible by
\(R^{a-1}\) and hence need not be tangent to the reduced common-root
cone.  This is the precise reason that the linearized Keller identity,
by itself, does not prove approximate-root induction.

The all-order invariant form is also linear.  Work \(\tau\)-adically
over \(k(X)\); after the common powers of \(R\) are removed, the
relative ratio has constant term one.  Put
\[
\ell=\log(Q^a/P^b).
\]
Then (51) is equivalent to
\[
\tau\left(
\frac{P_X}{P}\ell_\tau-\frac{P_\tau}{P}\ell_X
\right)+ag\,\ell_X
=-\frac{ac\tau^N}{PQ}.
\]
If the lower \(P\)- and \(\ell\)-orders are all divisible by \(g\),
the residue classes in this equation decouple.  For \(g>2\), its
order-\(N\) equation is exactly (63), even when the relative
\(g\)-sector unit is nontrivial.  The unresolved mixing is therefore
the non-\(g\)-multiple \(Z=0\) nilpotent cascade in the coefficients of
the transport operator, not the relative unit by itself.

There is a second consequence of (51) that is exact to all orders.
Let \(\gamma\) be a normalization branch of the curve \(P=0\), and
write \(X=X(\tau)\) on that branch.  Since
\[
\frac{dX}{d\tau}=-\frac{P_\tau}{P_X},
\]
restriction of (51) to \(P=0\) gives
\[
\begin{aligned}
d\!\left(\frac{Q}{\tau^m}\right)
&=\frac{\tau(P_XQ_\tau-P_\tau Q_X)-mQP_X}
        {\tau^{m+1}P_X}\,d\tau\\
&=-c\,\frac{\tau^{n-3}}{P_X|_\gamma}\,d\tau.
\end{aligned} \tag{54}
\]
The right side is therefore an exact meromorphic differential on
every individual normalization branch.  In particular,
\[
\boxed{\quad
\operatorname{Res}_\gamma
\frac{\tau^{n-3}\,d\tau}{P_X}=0 .
\quad} \tag{55}
\]
If \(\tau=t^e\) is a local parameter, (55) is equivalently
\[
\boxed{\quad
[t^{em}]
\left(\frac{\tau^N}{P_X}\Big|_\gamma\right)=0 .
\quad} \tag{56}
\]
Indeed,
\[
\frac{\tau^{n-3}\,d\tau}{P_X}
=e\,t^{-em-1}
\left(\frac{\tau^N}{P_X}\Big|_\gamma\right)dt.
\]

The branch qualifier in (55) is essential.  For a monic polynomial
with simple generic roots \(X_i(\tau)\),
\[
\sum_i\frac1{P_X(X_i(\tau),\tau)}=0 \qquad(n>1), \tag{57}
\]
so the sum of (55) over all branches vanishes identically.  Even the
sum over all branches specializing to one root of \(R\) can cancel.
For example, the \(a\) branches of
\(R^a+c\tau^n=0\) have leading coefficients proportional to
the \(a\)-th roots of \(-c\), and their local residue contributions
sum to zero.

Individual branches do detect the missing congruence.  Near a simple
root of \(R\), write \(s=X-\alpha\) and consider the local model
\[
P=s^a+\kappa\tau^{n-2}s. \tag{58}
\]
This perturbation has precisely the non-\(g\)-multiple order
\(n-2\equiv-2\pmod g\).  On the fixed branch \(s=0\),
\[
P_X=\kappa\tau^{n-2},\qquad
\frac{\tau^N}{P_X}=\frac1\kappa\tau^m. \tag{59}
\]
On each of the other \(a-1\) Puiseux branches,
\(s^{a-1}=-\kappa\tau^{n-2}\), and hence
\[
P_X=-(a-1)\kappa\tau^{n-2},\qquad
\frac{\tau^N}{P_X}
=-\frac1{(a-1)\kappa}\tau^m. \tag{60}
\]
Every individual coefficient in (59)--(60) is nonzero, while their
sum is
\[
\frac1\kappa
+(a-1)\left(-\frac1{(a-1)\kappa}\right)=0. \tag{61}
\]
Thus a global or cluster-summed residue misses exactly the obstruction
that the normalization-branch residue sees.

This test also explains the exceptional \(g=2\) behavior.  On a moving
branch of the pure \(g\)-sector model (43),
\[
\operatorname{ord}_\tau P_X=n-g,\qquad
\operatorname{ord}_\tau\frac{\tau^N}{P_X}=m+g-2. \tag{62}
\]
For \(g=2\), (62) is the forbidden \(m\)-th coefficient, so each
branch already violates (56).  For \(g>2\), it starts strictly after
\(\tau^m\), and the pure \(g\)-sector family is invisible to this
residue.

The best remaining local statement is now quite concrete:

> **Branch-resonance lemma.**  After choosing an honest
> approximate-root slice while retaining the relative unit
> \(Q^a/P^b\), the standard equations through order \(N\), including
> the final inhomogeneous equation, force on at least one normalization
> branch a nonzero \(t^{em}\)-coefficient in \(\tau^N/P_X\).

Equations (54)--(56) would contradict this immediately.  The model
(58) shows that the lemma has exactly the right residue class and that
it must be proved branchwise.  What remains open is the normal-form
step: showing that the \(Z=0\) nilpotent cascade cannot redistribute
the \((-2\bmod g)\) forcing among earlier jets while keeping every
individual resonance in (56) zero.

For comparison, if every lower-order jet could first be normalized
away, the coefficient of order \(d=N\) in (51) would give, with
\(W=R^{a+b}Z\),
\[
gRW'-2R'W=-cR. \tag{63}
\]
For squarefree \(R\), a rational solution \(W\) has no poles and must
vanish at every root of \(R\), so \(W=RH\).  Equation (63) becomes
\[
gRH'+(g-2)R'H=-c. \tag{64}
\]
For \(g>2\), leading degrees rule out (64); for \(g=2\), it asks for a
rational primitive of \(1/R\), whose simple-pole residues are nonzero.
This is a useful endpoint check, not yet a proof: in the actual
homogenized pair there are no new degree-\(N\) coefficients of \(P\)
or \(Q\), and the order-\(N\) term is a nonlinear combination of the
earlier jets.  Reaching (63) therefore requires precisely the missing
normal-form lemma.

## 9. What local Brieskorn theory can and cannot add

The exact-differential interpretation is not new in its global form.
Heitmann's Theorem 2.5 in *J. Pure Appl. Algebra* 64 (1990), 35--72,
makes the two-dimensional Jacobian conjecture equivalent to the
statement that exactness of the generic Gelfand--Leray differential
forces the generic curve to have genus zero.  Friedland's
Gauss--Manin and monodromy formulation studies the same global
cohomology.  Consequently, replacing (54) by the bare assertion that
all global periods vanish would only restate a known equivalent form
of the conjecture.

There is still a useful local grading.  Near a simple root of \(R\),
give \(s\) weight \(g\) and \(\tau\) weight one.  A \(g\)-sector leading
pencil has the form
\[
F_0(s,\tau)
=\sum_{c=0}^a u_c\tau^{gc}s^{a-c}
=\tau^n\Phi(s/\tau^g),\qquad u_0\ne0. \tag{65}
\]
If \(\Phi\) is squarefree, \(F_0\) has an isolated singularity.  In its
Jacobian algebra,
\[
\mathcal Q_{F_0}
=k[s,\tau]/((F_0)_s,(F_0)_\tau),
\]
one has
\[
[\tau^{n-3}]\ne0. \tag{66}
\]
Indeed, \((F_0)_s\) and \((F_0)_\tau\) have weights \(n-g\) and
\(n-1\).  A weighted representation
\(\tau^{n-3}=A(F_0)_s+B(F_0)_\tau\) would require
\(\operatorname{wt}B=-2\) and
\(\operatorname{wt}A=g-3\).  Thus \(B=0\); for \(g=2\) also \(A=0\),
while for \(g\ge3\) one must have
\(A=c\tau^{g-3}\).  The term
\(cau_0\tau^{g-3}s^{a-1}\) then forces \(c=0\), a contradiction.
The corresponding two-form
\[
\tau^{n-3}\,ds\wedge d\tau
\]
has character \(\zeta^{-2}\) under
\(\tau\mapsto\zeta\tau,\ \zeta^g=1\).  This recovers the nonzero
\((-2\bmod g)\) class in a Brieskorn grading.

This nonvanishing is not yet an obstruction to a Keller pair.
The primitive \(Q/\tau^m\) is meromorphic at infinity, and ordinary
local Brieskorn quotients only mod out holomorphic primitives.
Moreover, the relevant generic fibers are the pencil
\(P-u\tau^n=0\), singular at infinity for every \(u\), rather than the
ordinary Milnor fibers \(P=\epsilon\).  The correct object is therefore
a pole-filtered, logarithmic Gauss--Manin module for the pencil.  On
each punctured normalization branch that module reduces to (55), and
there is no higher local residue after the ordinary residue vanishes.

There is an elementary calculation showing exactly how the linear
tail crosses this pole filtration.  Put
\[
\tau=y^{-1},\qquad
z=y^{g-1}(x-\alpha y),
\]
so
\[
dx\wedge dy=-\tau^{g-3}\,dz\wedge d\tau.
\]
Expand two original polynomials as finite Laurent series
\[
p=\sum_r p_r(z)\tau^r,\qquad
q=\sum_l q_l(z)\tau^l. \tag{67}
\]
Polynomiality in \(x,y\) implies that every monomial
\(\tau^rz^j\) in (67) satisfies
\[
r\le(g-1)j. \tag{68}
\]
In particular, for \(r>0\),
\[
\operatorname{ord}_{z=0}p_r,\,
\operatorname{ord}_{z=0}q_r
\ge\left\lceil\frac r{g-1}\right\rceil. \tag{69}
\]
The coefficient of \(\tau^{g-3}\) in
\(p_zq_\tau-p_\tau q_z\), evaluated at \(z=0\), is
\[
\begin{aligned}
&\sum_{r+l=g-2}
\bigl(l\,p_r'(0)q_l(0)-r\,p_r(0)q_l'(0)\bigr)\\
&\hspace{20mm}
=p_{-1}(0)q_{g-1}'(0)
-p_{g-1}'(0)q_{-1}(0). \tag{70}
\end{aligned}
\]
All other summands vanish by (69).  The four surviving coefficients
are exactly the affine-linear terms:
\[
\begin{aligned}
p_{\rm lin}&=p_{-1}(0)y+p_{g-1}'(0)(x-\alpha y),\\
q_{\rm lin}&=q_{-1}(0)y+q_{g-1}'(0)(x-\alpha y).
\end{aligned}
\]
Thus (70) is the negative of their ordinary Jacobian.  The
\(\tau^{g-3}\) forcing is not a new local period obstruction: at the
coarsest pole-graded level it is precisely the original linear
Jacobian reappearing across the two distant Laurent orders
\(-1\) and \(g-1\).

This calculation rules out a tempting but invalid shortcut.  The
nonzero class (66) cannot simply be declared incompatible with
exactness; the meromorphic linear tail supplies the same graded class.
The remaining useful target must be global and strictly narrower than
Heitmann's equivalence:

> **Pole-filtered monodromy lemma.**  In the trace-zero
> \(A_{a-1}\) local system of the finite cover
> \(\Phi(z)=u\), choose a common approximate-root slice, retain the
> relative \(g\)-sector unit, and quotient the endpoint pairing (70).
> Then the \(\zeta^{-2}\) forcing class cannot extend as a polynomial,
> single-valued section compatible with all boundary clusters.

This is the first formulation that uses the new standard-system
grading without confusing it with ordinary branch residues or with
the full, already-known exact-differential equivalence.  It is also
where genuine global monodromy is unavoidable: the punctured-disc
calculation has no further cohomology to offer.
