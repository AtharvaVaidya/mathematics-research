# Finite endpoint charge is exactly sheet loss

Date: 25 July 2026

## Outcome

This note combines three kinds of information which had previously been
kept separate:

1. the endpoint charge
   \(\kappa=a+\sigma\) coming from the resolved normal map;
2. the genus and punctures of a residual component above a smooth
   conductor image \(\Gamma\simeq\mathbf G_m\); and
3. the Chau--Jelonek description of the nonproper-value set.

The result is an exact conservation law.  At a finite nonproper value,
endpoint charge is not merely nonnegative: it is precisely the number
of sheets which disappear there.  Globally,
\[
 \sum_{\substack{w\text{ residual boundary}\\
                  \bar f(w)\in\Gamma}}
 \kappa_w
 =
 \sum_{p\in\Gamma\cap S_e}
 \bigl(n-\#e^{-1}(p)\bigr).
\tag{1}
\]
Componentwise, both sides are
\[
 2g(H)+s(H)-2.
\tag{2}
\]

Thus Riemann--Hurwitz, endpoint charge, Euler characteristic, and
finite sheet loss do **not** supply independent inequalities.  They are
the same equality in four forms.  In particular, the degree-\(2\delta\)
conductor component gives no divisibility condition on the global
degree \(n\).

There is also an exact fixed-source first-order model.  In the actual
\((t,c)\)-plane it realizes

- the fixed conductor;
- a disjoint residual curve;
- the sharp quartic target with residue exponent \(j=-1\);
- the degree partition \(3=2+1\);
- one missing residual sheet;
- the forced odd normal coefficient \(v/18\); and
- the Keller equation modulo the squarefree pullback divisor.

It does **not** give a polynomial Keller pair: the Jacobian is only
\(1\) modulo the two displayed curve equations, and no global
nonproper-value set or global boundary morphism is constructed.

## 1. The sheet-loss theorem

Work over \(\mathbf C\).  Let
\[
 e:\mathbf A^2\longrightarrow\mathbf A^2
\]
be an everywhere-etale polynomial map of generic degree \(n\), and let
\(S_e\) be its nonproper-value set.  Let
\(\Gamma\subset\mathbf A^2\) be a smooth closed curve isomorphic to
\(\mathbf G_m\), not an irreducible component of \(S_e\).  Write
\[
 e^{-1}(\Gamma)=\coprod_\nu H_\nu
\]
for its connected components.  They are smooth and disjoint because
the pullback of a smooth reduced Cartier divisor by an etale map is
smooth and reduced.

Choose a normalization coordinate \(s\) on \(\Gamma\), so
\[
 \mathbf C[\Gamma]=\mathbf C[s,s^{-1}].
\]
Let \(\overline H_\nu\) be the smooth projective completion of
\(H_\nu\).  The restriction
\[
 f_\nu:H_\nu\longrightarrow\Gamma
\]
extends uniquely to a finite morphism
\[
 \bar f_\nu:\overline H_\nu\longrightarrow\mathbf P^1_s
\]
of degree \(e_\nu\).

Let
\[
 \omega_\Gamma
 =\operatorname {Res}_\Gamma\frac{dX\wedge dY}{F}
 =\lambda s^j\,\frac{ds}{s},
 \qquad \lambda\ne0.
\tag{3}
\]
For every boundary point
\(w\in\overline H_\nu\setminus H_\nu\), let \(e_w\) be the local degree
of \(\bar f_\nu\), let \(p=\bar f_\nu(w)\), and define
\[
 \kappa_w
 :=e_w\bigl(\operatorname {ord}_p\omega_\Gamma+1\bigr).
\tag{4}
\]
The resolved normal-map calculation in
`FIXED_PLANE_NORMAL_MAP_GLUING.md` identifies (4) with the boundary
quantity \(a+\sigma\).

The pullback rule for a differential is
\[
 \operatorname {ord}_w(\bar f_\nu^*\omega_\Gamma)
 =e_w\bigl(\operatorname {ord}_p\omega_\Gamma+1\bigr)-1
 =\kappa_w-1.
\tag{5}
\]
Because \(f_\nu\) is etale and \(\omega_\Gamma\) has no zero on the
affine curve \(\Gamma\), the divisor of
\(\bar f_\nu^*\omega_\Gamma\) is supported on the boundary.  Taking its
degree gives
\[
 \boxed{\qquad
 \sum_{w\in\overline H_\nu\setminus H_\nu}\kappa_w
 =2g_\nu+s_\nu-2,
 \qquad}
\tag{6}
\]
where \(g_\nu=g(\overline H_\nu)\) and
\(s_\nu=\#(\overline H_\nu\setminus H_\nu)\).

At \(s=0\) and \(s=\infty\), (3)--(4) give
\[
 \sum_{w\mid0}\kappa_w=e_\nu j,\qquad
 \sum_{w\mid\infty}\kappa_w=-e_\nu j.
\tag{7}
\]
These contributions cancel on every component.

Now let \(p\in\Gamma\) be affine.  The differential (3) has order zero
at \(p\), so every omitted point over \(p\) has
\[
 \boxed{\qquad \kappa_w=e_w>0.\qquad}
\tag{8}
\]
The degree formula for the finite completion is
\[
 e_\nu
 =\#f_\nu^{-1}(p)
  +\sum_{\substack{w\notin H_\nu\\\bar f_\nu(w)=p}}e_w.
\tag{9}
\]
Finite points have multiplicity one because \(e\) is etale.  Combining
(8)--(9) proves the componentwise sheet-loss identity
\[
 \boxed{\qquad
 \sum_{\substack{w\notin H_\nu\\\bar f_\nu(w)=p}}\kappa_w
 =e_\nu-\#f_\nu^{-1}(p).
 \qquad}
\tag{10}
\]

Since \(\Gamma\) is not a component of \(S_e\), its generic fiber has
all \(n\) sheets and
\[
 \sum_\nu e_\nu=n.
\tag{11}
\]
Every inverse image of a point of \(\Gamma\) lies on one of the
\(H_\nu\).  For a quasi-finite etale map, a target point is outside
\(S_e\) exactly when its fiber has the full \(n\) points: \(n\)
disjoint local etale sheets already exhaust the generic degree, whereas
a smaller fiber loses the missing degree at infinity.  Thus the
positive terms in (10) occur exactly on \(\Gamma\cap S_e\).  Summing
(10) over the components and over
\(p\in\Gamma\cap S_e\) gives (1).  Summing (6), and then using (7),
gives the same equality.  This proves that the endpoint-charge equation
and the Euler sheet-loss equation are identical, not competing bounds.

For the fixed conductor \(C\), the completed cover has degree
\(2\delta\), genus zero, exactly two punctures, and no omitted finite
point.  It contributes
\[
 -2\delta j+2\delta j=0.
\tag{12}
\]
The remaining degree equation is only
\[
 \boxed{\qquad n=2\delta+\sum_{\nu\ne C}e_\nu.\qquad}
\tag{13}
\]
Nothing in (1)--(13) makes \(2\delta\) divide \(n\).

## 2. What the Chau--Jelonek theorem adds

For a noninvertible Keller map, \(S_e\ne\varnothing\).  The
Chau--Jelonek theorem says that every irreducible component of \(S_e\)
is polynomially parametrized and has one-place affine normalization
\(\mathbf A^1\).  The conductor image has normalization
\(\mathbf G_m\), so it is not such a component.  Hence
\(\Gamma\cap S_e\) is finite, exactly the situation covered by
(1).

The stronger theorem of Nguyen Van Chau also excludes an irreducible
component of \(S_e\) which is itself a smooth embedded affine line.
Accordingly, a straight line may be used only as a local incidence
stress test, not as the complete nonproper-value set of a Keller map.

Even the stronger singular/one-place requirement creates no numerical
contradiction.  For example, retain the quartic target of Section 3 and
take the cuspidal polynomial curve
\[
 \Lambda:\quad Y^2=(X-1)^3,
 \qquad r\longmapsto(1+r^2,r^3).
\tag{14}
\]
It has normalization \(\mathbf A^1\), one place at infinity, and is
singular at \((1,0)\).  On the normalization of \(\Gamma\), its
intersection equation is
\[
 -9s^4\bigl(Y^2-(X-1)^3\bigr)
 =(s+1)^2
 \bigl(9s^8-18s^7+18s^5-9s^4-1\bigr).
\tag{15}
\]
The degree-eight factor is squarefree and does not vanish at \(-1\).
Thus there are nine distinct affine intersection points.  The smooth
plane curve
\[
 z\,s\,R(s)=1,\qquad
 R(s)=(s+1)
 \bigl(9s^8-18s^7+18s^5-9s^4-1\bigr),
\tag{16}
\]
is \(\mathbf P^1\) minus those nine points and \(0,\infty\).  Its
identity map to \(\Gamma\) is etale and omits exactly the nine
intersection values.  It has
\[
 g=0,\quad s_{\rm boundary}=11,\quad
 2g+s_{\rm boundary}-2=9,
\tag{17}
\]
exactly the nine units of sheet loss.

This is an abstract curve-level stress test, not a surface map and not
the fixed-source residual curve constructed next.  Its role is precise:
the singular polynomial-parametrization and one-place clauses do not
turn (1) into a new inequality.

## 3. An exact residual curve in the fixed source plane

Return to the actual fixed source
\(\mathbf A^2_{t,c}\).  Put
\[
 v=3ct-2,\qquad
 D=v^2-9c
   =9c^2t^2-12ct-9c+4,
\tag{18}
\]
and introduce
\[
 K=v+D
   =9c^2t^2-9ct-9c+2.
\tag{19}
\]
The conductor is \(C=(D=0)\).  The curve
\[
 H=(K=0)
\]
is smooth and disjoint from \(C\).  Indeed, on \(H\),
\[
 c=\frac{v(v+1)}9,\qquad
 t=\frac{3(v+2)}{v(v+1)},
\tag{20}
\]
so
\[
 H\simeq\mathbf P^1_v\setminus\{0,-1,\infty\}.
\tag{21}
\]
Conversely, (20) gives every point of \(H\).  Also
\[
 K|_C=v,
\tag{22}
\]
which is a unit on the conductor.  Hence \(C\cap H=\varnothing\), and
the residual restriction has the required odd exponent one.

Use the sharp target curve
\[
 \Gamma:\quad
 F(X,Y)=(3XY+1)^2-X=0
\tag{23}
\]
with normalization
\[
 X=s^2,\qquad
 Y=-\frac{s^{-1}+s^{-2}}3.
\tag{24}
\]
Map the two source curves by
\[
 C\longrightarrow\Gamma:\ s=c=\frac{v^2}{9},
\qquad
 H\longrightarrow\Gamma:\ s=v.
\tag{25}
\]
The first map has degree two and is finite etale.  The second is a
degree-one etale open immersion which omits only \(s=-1\), namely the
target point
\[
 p=(X,Y)=(1,0).
\tag{26}
\]

These two curve maps are restrictions of global source polynomials.
Set
\[
 B_0=2+4t-3ct^2,
\tag{27}
\]
\[
 \iota_C=\frac{tv-3}{6},\qquad
 \iota_H=\frac{t(v+1)-3}{6}.
\tag{28}
\]
The exact identities
\[
 v\iota_C-1=\frac t6D,\qquad
 v\iota_H-1=\frac t6K
\tag{29}
\]
show that these are the respective polynomial representatives of
\(v^{-1}\).  Moreover
\[
 e_C=K\iota_C,\qquad e_H=-D\iota_H,\qquad
 e_C+e_H=1
\tag{30}
\]
are CRT idempotents modulo \(DK\).

Choose
\[
 \begin{aligned}
 X_C&=c^2,&
 Y_C&=-\frac{B_0+1}{4}
       -\frac{3(B_0+1)^2}{16},\\
 X_H&=v^2,&
 Y_H&=-\frac{\iota_H+\iota_H^2}{3},
 \end{aligned}
\tag{31}
\]
and define
\[
 U_0=e_CX_C+e_HX_H,\qquad
 V_0=e_CY_C+e_HY_H.
\tag{32}
\]
Equations (28)--(31) prove directly that (32) restricts to (24) with
the two choices of \(s\) in (25).  In particular
\[
 F(U_0,V_0)\in(DK).
\tag{33}
\]

## 4. Hermite CRT gives an exact first Keller jet

Write
\[
 \{A,B\}=A_tB_c-A_cB_t.
\]
The tangent coordinate \(U_0\) has unit derivative on both source
curves.  More explicitly,
\[
 \{U_0,D\}|_C=-\frac4{27}v^5,
\qquad
 \{U_0,K\}|_H=-6v^2(v+1).
\tag{34}
\]
Together with
\[
 K|_C=v,\qquad D|_H=-v,
\tag{35}
\]
all four displayed factors are units in the relevant coordinate rings.

Let \(J_0=\{U_0,V_0\}\).  Define residue classes
\[
 \beta_C=
 \frac{1-J_0}{K\{U_0,D\}}\pmod D,\qquad
 \beta_H=
 \frac{1-J_0}{D\{U_0,K\}}\pmod K.
\tag{36}
\]
They are regular by (34)--(35).  Since \(D\) and \(K\) are comaximal,
CRT gives a polynomial \(\beta\in\mathbf C[t,c]\) with these two
restrictions.  Put
\[
 U=U_0,\qquad V=V_0+DK\beta.
\tag{37}
\]
Then
\[
 \begin{aligned}
 \{U,V\}
 &\equiv J_0+K\beta_C\{U_0,D\}\equiv1\pmod D,\\
 \{U,V\}
 &\equiv J_0+D\beta_H\{U_0,K\}\equiv1\pmod K.
 \end{aligned}
\]
Therefore
\[
 \boxed{\qquad \{U,V\}\equiv1\pmod {DK}.\qquad}
\tag{38}
\]
This is an exact Hermite-CRT construction, but only to first order
along \(C\sqcup H\).

Since the values still lie on \(\Gamma\),
\[
 F(U,V)=DKL
\tag{39}
\]
for a polynomial \(L\).  The Jacobian equality along the two curves
determines its restrictions without expanding (39).  Along (24),
\[
 F_Y=-6s^3.
\tag{40}
\]
Wedge \(dF(U,V)\) with \(dU\).  On \(C\), respectively \(H\), equations
(34)--(40) give
\[
 F_Y=KL\{U,D\},\qquad
 F_Y=DL\{U,K\}.
\]
Hence
\[
 \boxed{\qquad
 L|_C=\frac1{18},\qquad
 L|_H=-\frac1{v+1}.
\qquad}
\tag{41}
\]
Both are units.  Most importantly,
\[
 \boxed{\qquad
 \left.\frac{F(U,V)}D\right|_C
 =K|_C\,L|_C=\frac v{18}.
\qquad}
\tag{42}
\]
This is exactly the odd normal coefficient forced by the
fixed-conductor determinant and the quartic residue calculation.

## 5. The complete endpoint ledger of the model

For (23)--(24),
\[
 \omega_\Gamma
 =-\frac1{3s}\frac{ds}{s},
\qquad j=-1.
\tag{43}
\]
The conductor cover in (25) therefore has endpoint charges
\[
 (-2,+2).
\tag{44}
\]
The residual curve \(H\) has endpoint charges
\[
 (-1,+1)
\]
over \(s=0,\infty\), and one finite charge \(+1\) at its omitted value
\(s=-1\).  Thus
\[
 -1+1+1=1
 =2g(H)+s(H)-2
 =0+3-2.
\tag{45}
\]
Away from \(p\), the two curves supply \(2+1=3\) sheets; at \(p\), the
residual sheet is absent and the conductor still supplies two.  Hence
\[
 3-\#e^{-1}(p)=1,
\tag{46}
\]
exactly the finite charge in (45).  This is the smallest possible
degree partition and explicitly shows that a degree-two conductor orbit
does not imply divisibility of the total degree.

The line \(Y=0\) meets \(\Gamma\) only at \(p\), so it is a convenient
local incidence marker.  It is **not** asserted to be an actual
nonproper-value component: Chau's stronger line theorem prohibits that
for an everywhere-nonsingular polynomial map.  The singular cusp model
in Section 2 separately shows that imposing a genuine
polynomially-parametrized singular one-place curve still leaves the
sheet-loss equation numerically exact.

## 6. Exact conclusion

The positive theorem is the conservation law (1)/(10):

> finite endpoint charge is exactly missing-sheet multiplicity.

Its strategic consequence is negative but precise:

> conductor degree, endpoint charge, component genus, Euler
> characteristic, and the Chau--Jelonek one-place theorem cannot by
> themselves yield a global degree or divisibility contradiction.

The fixed-source model (18)--(46) is stronger than a numerical ledger:
the source curves, target curve, restriction maps, polynomial value
lifts, first normal jets, and odd residual coefficient all exist
simultaneously.  What remains absent is exactly what a real solution
would require:

1. \(\{U,V\}=1\) in the whole polynomial ring, rather than modulo
   \(DK\);
2. a generically finite polynomial surface map of degree three;
3. a genuine Chau-admissible nonproper-value curve producing the missing
   sheet;
4. a resolved global boundary satisfying finality and the Green
   equations; and
5. connected global monodromy compatible with all these data.

Thus the promising next input is not another genus estimate.  It must
couple the first-order CRT data to higher normal order, or couple the
distinguished conductor orbit to the full monodromy/finality tree.

The exact polynomial, curve, residue, charge, and Hermite-CRT
calculations are checked by
`verify_fixed_plane_sheet_loss_first_order_crt.py`.

The nonproper-value inputs used above are Nguyen Van Chau,
*Non-proper value set and the Jacobian condition*
([arXiv:math/0305088](https://arxiv.org/abs/math/0305088)), and the
polynomial-parametrization/line exclusion summarized in
*Plane Jacobian conjecture*
([Annales Polonici Mathematici 93 (2008)](https://www.impan.pl/shop/publication/transaction/download/product/85382)).
