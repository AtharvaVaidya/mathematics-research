# Squarefree common-root boundary is impossible for a reciprocal Keller pair

Date: 26 July 2026

## Outcome

Let \(g\ge2\), let \(1<a<b\) be coprime, and put
\[
n=ga,\qquad m=gb,\qquad N=n+m-2.
\tag{1}
\]
Suppose \(P,Q\in\mathbf C[X,\tau]\) obey the reciprocal degree bounds
\[
\deg_X[\tau^j]P\le n-j,\qquad
\deg_X[\tau^j]Q\le m-j,
\tag{2}
\]
and the homogenized Keller identity
\[
\mathscr K_X(P,Q):=
\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X
=-c\tau^N,\qquad c\ne0.
\tag{3}
\]
Assume their boundary powers have a common squarefree root:
\[
P(X,0)=R(X)^a,\qquad Q(X,0)=R(X)^b,
\tag{4}
\]
where \(R\) is monic and squarefree of degree \(g\).

Then no such pair exists.

More precisely, the strict compact-face theorem and the reciprocal
degree bounds force an exact normal form
\[
\boxed{
\begin{aligned}
P&=S^aA(\tau^g/S)
  =\sum_{q=0}^a A_q\tau^{gq}S^{a-q},\\
Q&=S^bB(\tau^g/S)
  =\sum_{q=0}^b B_q\tau^{gq}S^{b-q},
\end{aligned}}
\tag{5}
\]
where
\[
A_0=B_0=1
\tag{6}
\]
and
\[
S(X,\tau)
=R(X)+\sum_{1\le e<g}\tau^eL_e(X),
\qquad \deg L_e\le g-e.
\tag{7}
\]
The relative unit \(B^a/A^b\) is arbitrary; it is not normalized
away.

For every pair of the form (5), however,
\[
\mathscr K_X(P,Q)=0.
\tag{8}
\]
This contradicts (3).  Consequently an actual reciprocal Keller pair
cannot have a squarefree common-root boundary of the form (4).

This is an exclusion theorem for one boundary architecture, not a
proof of the plane Jacobian conjecture.  It uses the full polynomial
identity (3), not merely determinant contact or a truncated finite
standard system.

## 1. The strict compact-face input

Let \(\alpha\) be a root of \(R\).  During the argument the local
coordinate will be
\[
s=S(X,\tau).
\tag{9}
\]
Since \(S(X,0)=R(X)\) and \(R'(\alpha)\ne0\), this is a valid formal
coordinate near \((\alpha,0)\).  More explicitly, the formal implicit
function theorem gives an inverse
\[
X=\chi(s,\tau),\qquad
\chi(s,\tau)=\chi(s,0)+O(\tau),
\]
where \(\chi(s,0)\) is the local inverse of \(R\).  Consequently this
coordinate change preserves the least \(\tau\)-order:
\[
\tau^jT_j(X)+O(\tau^{j+1})
=\tau^jT_j(\chi(s,0))+O(\tau^{j+1}).
\]
It also preserves the relevant local vanishing order, since
\[
\operatorname{ord}_{s=0}T_j(\chi(s,0))
=\operatorname{ord}_{X=\alpha}T_j.
\]

The bracket is covariant under this \(\tau\)-dependent coordinate.
If
\[
P=f(S,\tau),\qquad Q=k(S,\tau),
\]
then the chain rule gives
\[
\boxed{
\mathscr K_X(P,Q)
=S_X\mathscr K_S(f,k),
}
\tag{10}
\]
where
\[
\mathscr K_S(f,k)
=\tau(f_Sk_\tau-f_\tau k_S)+nfk_S-mkf_S
\tag{11}
\]
and the \(\tau\)-derivatives on the right are taken with \(S\) fixed.
Indeed, the two terms containing \(S_\tau f_Sk_S\) cancel.

Suppose the first compact local face from \(s^a\) has primitive
weights
\[
\operatorname{wt}(s)=d',\qquad
\operatorname{wt}(\tau)=h',\qquad
\gcd(d',h')=1,
\tag{12}
\]
and is strict:
\[
d'<gh'.
\tag{13}
\]
Put
\[
z=\frac{\tau^{d'}}{s^{h'}}.
\tag{14}
\]
The complete initial \(P\)-face is
\[
P_0=s^aA_0(z),\qquad A_0(0)=1.
\tag{15}
\]

The matching \(Q\)-face is automatic.  To recall the argument, a
lowest \(Q\)-face in one lattice coset has the form
\[
Q_{u,v}=\tau^us^vB_0(z),\qquad B_0(0)\ne0,
\]
and weight
\[
w=h'u+d'v.
\]
Writing
\[
\Delta=d'-gh'<0,\qquad L=u+gv-gb,
\]
direct differentiation gives
\[
\begin{aligned}
\mathscr K_S(P_0,Q_{u,v})
=\tau^us^{a+v-1}\bigl(
&aL A_0B_0+a\Delta zA_0B_0'\\
&+(gbh'-w)zA_0'B_0
\bigr).
\end{aligned}
\tag{16}
\]
If \(w<bd'\), this bracket lies below the scalar forcing in (3), so it
must vanish.  Its constant term in \(z\) forces \(L=0\).  But then
\[
w=h'g(b-v)+d'v
=bd'+(b-v)(gh'-d')\ge bd',
\tag{17}
\]
a contradiction.  Hence no \(Q\)-face lies below \(s^b\), and the
weight lattice forces the complete face at weight \(bd'\) to be
\[
Q_0=s^bB_0(z),\qquad B_0(0)=1.
\tag{18}
\]

For this matched initial pair,
\[
\boxed{
\mathscr K_S(P_0,Q_0)
=(d'-gh')s^{a+b-1}z
\left(aA_0B_0'-bA_0'B_0\right).
}
\tag{19}
\]
The left side has face weight \((a+b-1)d'\), whereas the scalar
forcing has weight \(h'N\).  Their gap is
\[
h'N-(a+b-1)d'
=(a+b-1)(gh'-d')+h'(g-2)>0.
\tag{20}
\]
This is positive also when \(g=2\).  Thus (3), (10), and the fact that
\(S_X\) is a local unit force
\[
aA_0B_0'-bA_0'B_0=0.
\tag{21}
\]

If one of \(A_0,B_0\) were \(1\), (21) would make the other one
constant.  Every nontrivial strict face therefore occurs in both
coordinates.  Unique factorization and \(\gcd(a,b)=1\) give
\[
A_0=C^a,\qquad B_0=C^b,\qquad C(0)=1.
\tag{22}
\]
If the horizontal and vertical drops of the \(P\)-face are \(h,d\)
and \(e=\gcd(h,d)\), then
\[
h=h'e,\qquad d=d'e,\qquad \deg A_0=e.
\]
Equation (22) gives \(a\mid e\), while
\[
e\le h\le a.
\]
Consequently \(e=h=a\), \(h'=1\), and \(\deg C=1\).  Every strict
first face is therefore exactly
\[
\boxed{
P_0=(s+\kappa\tau^\delta)^a,\qquad
Q_0=(s+\kappa\tau^\delta)^b,
\qquad 1\le\delta<g,
}
\tag{23}
\]
for some \(\kappa\ne0\).  The symmetric statement holds if the first
strict face is detected from \(Q\).

The crucial information in (23) is not just the completed face.  It
contains a nonzero term
\[
a\kappa\tau^\delta s^{a-1}
\tag{24}
\]
at a primitive order \(\delta<g\).

## 2. Bridge through all orders below \(g\)

Starting with \(S=R\), successively compare \(P,Q\) with \(S^a,S^b\).
At a stage of the construction let \(j<g\) be the least order at
which either residual pair differs:
\[
P-S^a=\tau^jT_j+O(\tau^{j+1}),\qquad
Q-S^b=\tau^jU_j+O(\tau^{j+1}).
\tag{25}
\]

Suppose first that \(T_j\ne0\).  At a root where
\(\operatorname{ord}_\alpha T_j<a\), put
\[
h=a-\operatorname{ord}_\alpha T_j\ge1.
\]
The point supplied by \(T_j\) has slope \(j/h<g\), so the actual first
local face has slope at most \(j/h\) and is strict.  By (23) it is a
common reduced shift with primitive order \(\delta<g\).  Its
order-\(\delta\) term is a residual, so least-order minimality gives
\(\delta\ge j\).  But its slope is \(\delta\), hence
\[
\delta\le\frac jh\le j.
\]
Thus \(\delta=j\), \(h=1\), and
\[
\operatorname{ord}_\alpha T_j=a-1.
\]
Applying the same argument at every root shows that each active root
has order exactly \(a-1\), while every inactive root has order at
least \(a\).  Squarefreeness therefore gives
\[
T_j=aR^{a-1}L_j.
\tag{26}
\]
The reciprocal bound gives
\[
\deg L_j
\le(ga-j)-g(a-1)
=g-j.
\tag{27}
\]

The same local face identifies \(U_j\).  At an active root its
order-\(j\) term agrees with \(bL_j(\alpha)s^{b-1}\) modulo \(s^b\).
At an inactive root, \(L_j(\alpha)=0\).  If
\(\operatorname{ord}_\alpha U_j<b\) there, the \(Q\)-point would
again expose a strict common shift and make the root active in
\(P\), a contradiction.  Hence
\[
U_j-bR^{b-1}L_j
\]
is divisible by \(R^b\).  Both terms have degree at most \(m-j\):
\[
\deg U_j\le m-j,\qquad
\deg\!\left(R^{b-1}L_j\right)
\le g(b-1)+(g-j)=m-j.
\]
Thus the difference has degree at most \(m-j<m=\deg R^b\), so it
vanishes:
\[
\boxed{U_j=bR^{b-1}L_j.}
\tag{28}
\]

Replacing
\[
S\longmapsto S+\tau^jL_j
\tag{29}
\]
removes both residuals at order \(j\) and changes no lower order.

For completeness, a nonzero residual cannot avoid a strict root when
\(0<j<g\).  For a nonzero \(P\)-coefficient \(T_j\), define at the
\(g\) roots of \(R\)
\[
\sigma_\alpha
=\min\{\operatorname{ord}_\alpha T_j,a\},
\qquad
h_\alpha=a-\sigma_\alpha.
\tag{30}
\]
The truncation in (30) is essential.  The degree bound gives
\[
j\le ga-\sum_\alpha\sigma_\alpha
=\sum_\alpha h_\alpha.
\tag{31}
\]
If no root were strict, then \(j\ge gh_\alpha\) for every
\(\alpha\), hence
\[
\sum_\alpha h_\alpha\le j.
\]
Equality would hold throughout and would force
\(h_\alpha=j/g\) at all \(g\) roots, impossible because
\(0<j<g\).  The same argument applies to a nonzero \(Q\)-coefficient,
with \(a\) replaced by \(b\).  A strict face detected from either
coordinate is common by Section 1.  In particular, if \(T_j=0\) and
\(U_j\ne0\), the degree average gives a strict \(Q\)-root, whose
common reduced shift would make \(T_j\ne0\).  Thus a \(Q\)-only
subresonant layer is impossible.

Iterating (29) yields the reciprocal approximate root
\[
S=R+\sum_{1\le e<g}\tau^eL_e,
\qquad \deg L_e\le g-e,
\tag{32}
\]
and
\[
\boxed{
P\equiv S^a\pmod{\tau^g},\qquad
Q\equiv S^b\pmod{\tau^g}.
}
\tag{33}
\]

## 3. Least-residual induction after resonance

Retain independent scalar \(g\)-sectors:
\[
\begin{aligned}
P_{\mathrm{mod}}
&=\sum_{q=0}^a A_q\tau^{gq}S^{a-q},\\
Q_{\mathrm{mod}}
&=\sum_{q=0}^b B_q\tau^{gq}S^{b-q},
\end{aligned}
\qquad A_0=B_0=1.
\tag{34}
\]
Initially only \(A_0,B_0\) are chosen.  Equation (33) says the model
already agrees with \(P,Q\) through all orders below \(g\).

Assume inductively that the model agrees through order \(j-1\), and
let \(j\ge g\) be the least order at which either coordinate differs:
\[
\begin{aligned}
P-P_{\mathrm{mod}}
&=\tau^jT_j(X)+O(\tau^{j+1}),\\
Q-Q_{\mathrm{mod}}
&=\tau^jU_j(X)+O(\tau^{j+1}).
\end{aligned}
\tag{35}
\]
Either \(T_j\) or \(U_j\) is nonzero.  Notice that \(j\) is the least
residual order, not merely the first order not divisible by \(g\).
All earlier \(g\)-multiple residuals have already been classified
and absorbed into the scalar coefficients \(A_q,B_q\).

### 3.1 A strict root would create an earlier residual

Suppose first that \(T_j\ne0\).  At a root \(\alpha\) put
\[
\sigma_\alpha
=\min\{\operatorname{ord}_\alpha T_j,a\},
\qquad
h_\alpha=a-\sigma_\alpha.
\tag{36}
\]
If
\[
j<gh_\alpha
\tag{37}
\]
at some root, the point supplied by
\(\tau^jT_j\) lies below the slope-\(g\) line from \(s^a\).  The
actual first local face is therefore strict.

In the local coordinate \(s=S(X,\tau)\), every positive term of the
existing model is
\[
A_q\tau^{gq}s^{a-q}.
\]
For strict weights (12)--(13), its excess over \(s^a\) is
\[
q(gh'-d')>0.
\tag{38}
\]
Thus the existing \(g\)-sector lies strictly above the first strict
face and cannot alter its initial pair.

By (23), that face is a common reduced shift with primitive order
\(1\le\delta<g\).  Its expansion contains the nonzero term (24).
But the model (34), written in the \(s\)-coordinate, contains only
\(g\)-multiple positive \(\tau\)-orders, while (35) contains no
residual below \(j\).  Since
\[
\delta<g\le j,
\]
the term (24) is an impossible residual before order \(j\).
Therefore (37) cannot occur:
\[
\boxed{j\ge gh_\alpha\quad\text{at every root}.}
\tag{39}
\]

The identical argument applies if \(U_j\ne0\), using
\[
\rho_\alpha
=\min\{\operatorname{ord}_\alpha U_j,b\},
\qquad
k_\alpha=b-\rho_\alpha.
\tag{40}
\]
A strict \(Q\)-face is common and would create the same forbidden
primitive residual in \(P\).  This also covers a genuinely
\(Q\)-only least residual.

### 3.2 The degree average forces a scalar resonant layer

Continue with \(T_j\ne0\).  Its reciprocal degree bound and (36) give
\[
\sum_\alpha\sigma_\alpha
\le\deg T_j
\le ga-j.
\]
Equivalently,
\[
\boxed{j\le\sum_\alpha h_\alpha.}
\tag{41}
\]
On the other hand, (39) gives
\[
\sum_\alpha h_\alpha\le j.
\tag{42}
\]
All inequalities are equalities.  Since there are exactly \(g\)
roots and each \(h_\alpha\le j/g\), equality forces
\[
\boxed{
j=gq,\qquad h_\alpha=q\quad\text{for every }\alpha.
}
\tag{43}
\]
Here \(1\le q\le a\).  Consequently
\[
\sigma_\alpha=a-q<a,
\]
so the truncation in (36) is no longer active and
\[
\operatorname{ord}_\alpha T_j=a-q
\quad\text{at every root}.
\]
The degree bound is saturated:
\[
\deg T_j=g(a-q)=n-j.
\]
There is no room for any further zero, and squarefreeness gives
\[
\boxed{T_j=c_qR^{a-q}}
\tag{44}
\]
for a scalar \(c_q\ne0\).

At order \(j=gq\),
\[
[\tau^{gq}]
\left(\tau^{gq}S^{a-q}\right)
=R^{a-q}.
\tag{45}
\]
Thus replacing
\[
A_q\longmapsto A_q+c_q
\tag{46}
\]
removes the \(P\)-residual at order \(j\).  It changes no earlier
coefficient; the \(\tau\)-dependence of \(S\) only changes later
orders.

The symmetric calculation for \(U_j\ne0\) gives
\[
\boxed{
j=gq,\qquad U_j=d_qR^{b-q},\qquad 1\le q\le b,
}
\tag{47}
\]
which is removed by \(B_q\mapsto B_q+d_q\).

If \(T_j,U_j\) are both nonzero, the common order \(j\) gives the same
\(q=j/g\), and (46)--(47) are performed simultaneously.  If only one
is nonzero, only its scalar is changed.  If \(j>n\), then
\(T_j=0\) automatically; if \(j>m\), then both residuals vanish.
This covers simultaneous residuals, \(P\)-only residuals, and
\(Q\)-only residuals without assuming any relation between \(A\) and
\(B\).

The induction terminates because \(P,Q\) have finite \(\tau\)-degree.
It proves the exact normal form (5).

## 4. Reciprocal degree preservation

Every coefficient created in the bridge satisfies the correct bound.
Indeed, from
\[
\deg_X[\tau^e]S\le g-e
\tag{48}
\]
one obtains
\[
\deg_X[\tau^r]S^k\le gk-r.
\tag{49}
\]
Therefore
\[
\deg_X[\tau^r]\left(\tau^{gq}S^{a-q}\right)
\le g(a-q)-(r-gq)
=n-r,
\tag{50}
\]
and similarly
\[
\deg_X[\tau^r]\left(\tau^{gq}S^{b-q}\right)
\le m-r.
\tag{51}
\]
Thus every bridge update and scalar absorption stays inside the
original reciprocal polynomial class.  Also
\[
gq+(g-1)(a-q)\le n,\qquad
gq+(g-1)(b-q)\le m,
\]
so the model introduces no excessive \(\tau\)-degree.

## 5. The exact normal form has zero bracket

Set
\[
z=\frac{\tau^g}{S},\qquad
f(S,\tau)=S^aA(z),\qquad
k(S,\tau)=S^bB(z).
\tag{52}
\]
Direct differentiation at fixed \(S\) gives
\[
\begin{aligned}
f_S&=S^{a-1}(aA-zA'),&
f_\tau&=gS^azA'/\tau,\\
k_S&=S^{b-1}(bB-zB'),&
k_\tau&=gS^bzB'/\tau.
\end{aligned}
\tag{53}
\]
Substitution into (11), with \(n=ga\) and \(m=gb\), gives
\[
\mathscr K_S(f,k)=0
\tag{54}
\]
for arbitrary polynomials \(A,B\).  Equation (10) then yields
\[
\mathscr K_X(P,Q)=S_X\mathscr K_S(f,k)=0.
\tag{55}
\]
This contradicts the nonzero scalar forcing in (3).

No exceptional residue survives when \(g=2\): the strict-face gap
(20) remains positive, the bridge handles the sole subresonant order
\(\delta=1\), the truncated degree average is unchanged, and
(54) is an exact identity for every \(g\ge1\).

## 6. What has been proved

The exclusion rests on four rigid facts:

1. every strict first compact face of an actual pair is a common
   reduced-root shift;
2. after the subresonant bridge, such a shift would appear at an
   already-vanished order \(<g\);
3. the truncated root-multiplicity average makes every remaining
   least residual a scalar \(g\)-sector term; and
4. an exact pair made only of a common \(\tau\)-dependent root and
   scalar \(g\)-sectors has identically zero homogenized bracket.

The earlier local post-blowup kernel countermodel is irrelevant to
this theorem: it violated the global reciprocal degree average used
in (41)--(44).  No local kernel quotient is invoked here.

The accompanying exact checks are in
`verify_standard_system_squarefree_common_root_exclusion.py`.
