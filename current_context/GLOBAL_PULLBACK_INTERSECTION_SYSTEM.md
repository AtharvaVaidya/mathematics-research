# The fixed-plane global pullback/intersection system

Date: 25 July 2026

**Subsequent normal-map audit.**  The full-effectivity witness below
passes the numerical equations stated here, but its residual bridge
cannot realize the particular Laurent degree-nine target curve displayed
in (36).  `FIXED_PLANE_NORMAL_MAP_GLUING.md` derives a pointwise endpoint
charge law from the resolved target normal maps; for that curve the law
requires zero charge at each end, whereas nodes \(3\) and \(6\) have
charges \(-1\) and \(1\).  This strengthens the already-recorded
finality failure without changing the witness's role as an independence
example for the integral intersection equations.

This note records the exact numerical system imposed on a projective
resolution of a hypothetical fixed-plane Darboux pair.  It also separates
three logically different levels:

1. the pullback-line and canonical equations;
2. effectivity of the full conductor-image pullback; and
3. the final-curve/minimality conditions of a Keller resolution.

The first two levels are numerically compatible.  The explicit
full-effectivity witness below fails the third level, so it is not a
compactified Keller map and is not a counterexample.  The remaining
problem is precisely the simultaneous effectivity/finality coupling.

## 1. Universal boundary equations

Let
\[
\pi:X\longrightarrow\mathbf P^2
\]
be a sequence of point blowups at infinity resolving the rational
extension of
\[
e:\mathbf A^2\longrightarrow\mathbf A^2,
\]
and let
\[
\phi:X\longrightarrow\mathbf P^2
\]
be the resulting morphism.  Write the reduced boundary as
\[
B=\sum_iE_i
\]
and let \(Q=(E_i\cdot E_j)\).  Define the augmented-canonical labels
\(a_i\), the pullback-line multiplicities \(b_i\), and the line-incidence
vector \(y\) by
\[
K_X+B=\sum_i a_iE_i,\qquad
P:=\phi^*L_\infty=\sum_i b_iE_i,\qquad
y=Qb.
\tag{1}
\]
Projection formula gives
\[
y_i=L_\infty\cdot\phi_*E_i.
\tag{2}
\]
Thus \(y_i>0\) exactly on dicritical curves (types \(1\) and \(3\)), and
\[
P^2=b^TQb=b^Ty=n,
\tag{3}
\]
where \(n=\deg\phi\).

The ramification divisor is
\[
R=K_X-\phi^*K_{\mathbf P^2}
  =\sum_i r_iE_i,\qquad
r_i=a_i-1+3b_i\ge0.
\tag{4}
\]
At the generic point of a type-\(1\) divisor its ramification order is
\(b_i-1\), so
\[
\text{type 1:}\qquad a_i=-2b_i,\quad b_i>0,\quad y_i>0.
\tag{5}
\]
For type \(3\),
\[
\text{type 3:}\qquad b_i=0,\quad a_i\ge1,\quad y_i>0.
\tag{6}
\]
Point-mapping curves have \(y_i=0\).

These equations are stronger than a labeled-tree test: \(Qb=y\), rather
than the signs of \(a_i\), determines whether a proposed assignment can
be a pullback of the target line.

## 2. The conductor and its image

Let \(C\) be the resolved conductor closure.  The bare two-cusp
resolution has \(C^2=0\).  If \(q\) further blowups are centered on
\(C\), then
\[
C^2=-q.
\tag{7}
\]
Let \(E_\alpha,E_\beta\) be the two boundary components met by \(C\).
If the conductor cover has degree \(2\delta\) and
\(\overline\Gamma\subset\mathbf P^2\) has degree \(d\), then
\[
b_\alpha+b_\beta=P\cdot C=2\delta d.
\tag{8}
\]
Adjunction and the fact that \(C\) meets the boundary twice give
\[
a_\alpha+a_\beta=(K_X+B)\cdot C=q,
\tag{9}
\]
and hence
\[
R\cdot C=r_\alpha+r_\beta
=6\delta d+q-2.
\tag{10}
\]

Put
\[
G:=\phi^*\overline\Gamma\sim dP.
\]
Projection formula gives the three scalar identities
\[
G^2=nd^2,\qquad P\cdot G=nd,\qquad
G\cdot C=2\delta d^2.
\tag{11}
\]
Here is the precise reason that \(\Gamma\) is not a type-\(3\) image.
After base change to \(\mathbf C\), the Chau--Jelonek theorem says that
every irreducible component of the nonproper-value set of a generically
finite polynomial map \(\mathbf A^2\to\mathbf A^2\) is polynomially
parametrized and has one-place affine normalization \(\mathbf A^1\).
By contrast, the two-puncture theorem gives
\(\Gamma^\nu\simeq\mathbf G_m\).  Equivalently, a polynomial
parametrization \(\mathbf A^1\to\Gamma\) would lift to
\(\mathbf G_m\), but every unit of \(\mathbf C[t]\) is constant.
Thus no type-\(3\) divisor in a resolution of this same polynomial map
can map onto \(\Gamma\).  This uses the standard transfer identifying
type-\(3\) images with components of the nonproper-value set; it is
asserted only after the hypothetical fixed-plane pair is base-changed to
\(\mathbf C\) and \(\phi\) is chosen as a compatible resolution of that
pair.

A generic point of \(\Gamma\) therefore has all \(n\) inverse images in
the affine plane.  The conductor contributes \(2\delta\) of them, while
residual affine components \(H_j\) contribute degrees \(e_j\):
\[
\sum_j e_j=n-2\delta\ge1.
\tag{12}
\]

For the completion of an individual residual component \(H_j\), of
geometric genus \(g_j\),
\[
P\cdot H_j=e_jd,\qquad
G\cdot H_j=e_jd^2,
\tag{13}
\]
\[
R\cdot H_j
=2g_j-2-H_j^2+3e_jd.
\tag{14}
\]

## 3. The full effective-divisor coupling

For the clean form used below, assume \(\Gamma\) is smooth.  Since \(e\)
is étale, the pullback of the reduced smooth Cartier divisor \(\Gamma\)
is reduced and smooth.  Consequently its distinct affine components are
disjoint and each occurs with coefficient one.  Make further boundary
blowups, if necessary, so that the completions of these components have
separated boundary contacts.  (A blowup centered on \(C\) is included in
the integer \(q\) of (7).)  On this chosen resolution write
\[
G=C+\sum_jH_j+\sum_i\eta_iE_i,
\qquad \eta_i\in\mathbf Z_{\ge0}.
\tag{15}
\]
No dicritical boundary curve can be a component of \(G\): type \(1\)
maps to \(L_\infty\), and every type-\(3\) image is a curve different
from \(\Gamma\).  Therefore
\[
\eta_i y_i=0\quad\text{for every }i.
\tag{16}
\]

Let \(z_i\) be the total intersection of \(E_i\) with the strict affine
part \(C+\sum H_j\).  Intersecting (15) with every boundary component
gives the complete vector equation
\[
\boxed{\qquad z+Q\eta=d\,y.\qquad}
\tag{17}
\]
Here \(z\ge0\), and \(z_\alpha,z_\beta\ge1\).  Intersecting with \(C\)
gives
\[
\boxed{\qquad
\eta_\alpha+\eta_\beta-q=2\delta d^2.
\qquad}
\tag{18}
\]
The absence of a term \(\sum_jH_j\cdot C\) in (18) uses exactly the
smooth-\(\Gamma\), separated-components hypothesis above.  Without it
the universally valid equation is
\[
-q+\sum_jH_j\cdot C+\eta_\alpha+\eta_\beta=2\delta d^2.
\tag{18'}
\]
Equations (16)--(18), not merely (8)--(11), are the
\(G\)-effectivity test.

Dotting (17) with \(b\) recovers
\[
b^Tz=nd,
\tag{19}
\]
because \(b^TQ\eta=y^T\eta=0\).  Subtracting the conductor incidence
from \(z\) then recovers
\[
\sum_jP\cdot H_j=(n-2\delta)d.
\tag{20}
\]
Thus the cover-degree equation is already built into the vector system.

## 4. A scalar witness that fails effectivity

There is a 15-vertex blowup tree satisfying (1)--(10).  In the index
order
\[
(L,E_1,E_2,E_3,E_4,F_1,F_2,F_3,8,\ldots,14),
\]
its self-intersections and augmented-canonical labels are
\[
\begin{aligned}
E_i^2={}&(-1,-2,-3,-4,-1,-6,-2,-3,-3,-1,-3,-1,-1,-1,-1),\\
a={}&(-2,-1,0,1,1,-1,0,-1,-2,2,-3,-4,2,-3,-2).
\end{aligned}
\tag{21}
\]
The edges are
\[
\begin{split}
&(0,1),(0,5),(1,2),(2,4),(3,4),(3,9),(3,12),\\
&(5,11),(6,7),(7,13),(8,10),(8,13),(10,11),(10,14).
\end{split}
\tag{22}
\]
The pullback-line vector is
\[
b=(16,12,8,4,12,4,1,2,3,0,4,8,4,5,1),
\tag{23}
\]
and
\[
Qb=(0,\ldots,0,4,0,0,0,0,3),\qquad b^TQb=3.
\tag{24}
\]
Node \(9\) is type \(3\), node \(14\) is type \(1\), all ramification
coefficients (4) are nonnegative, and the conductor endpoints
\((4,7)\) give
\[
\delta=1,\qquad d=7.
\]

This scalar witness does **not** pass the smooth-\(\Gamma\) system
(17)--(18).  In fact any effective
\(\eta\) supported off nodes \(9,14\) and satisfying
\[
Q\eta\le7y-\mathbf e_4-\mathbf e_7
\]
obeys the sharp linear bound
\[
\eta_4+\eta_7\le\frac{483}{5}<98.
\tag{25}
\]
But (18) requires \(\eta_4+\eta_7=2\cdot7^2=98\).
The exact rational dual certificate for (25) is checked by the verifier.
Thus scalar compatibility can genuinely disappear at the
full-effectivity stage.

## 5. A full \(G\)-effective numerical witness

Effectivity itself is nevertheless not a contradiction.  An
11-blowup extension of the cusp tree has 19 boundary vertices.  Starting
from the eight bare vertices, perform
\[
\begin{split}
&(F_1,F_3),\ (F_1,8),\ (8,9),\ \operatorname{gen}(8),\
(E_3,E_4),\\
&\operatorname{gen}(E_2),\ \operatorname{gen}(9),\
\operatorname{gen}(L),\ \operatorname{gen}(13),\
\operatorname{gen}(8),\ \operatorname{gen}(E_1),
\end{split}
\tag{26}
\]
where a pair denotes a crossing blowup and \(\operatorname{gen}\) a
generic boundary blowup.  Its data are
\[
\begin{aligned}
E_i^2={}&(-2,-3,-4,-3,-2,-5,-2,-2,-5,-3,-1,-1,-1,-2,-1,-1,-1,-1,-1),\\
a={}&(-2,-1,0,1,1,-1,0,-1,-2,-3,-5,-1,2,1,-2,-1,2,-1,0),
\end{aligned}
\tag{27}
\]
with edges
\[
\begin{split}
&(0,1),(0,5),(0,15),(1,2),(1,18),(2,4),(2,13),(3,12),(4,12),\\
&(5,9),(6,7),(7,8),(8,10),(8,11),(8,17),(9,10),(9,14),(13,16).
\end{split}
\tag{28}
\]

Take
\[
\begin{aligned}
b={}&(16,12,8,8,16,4,1,2,3,4,7,3,24,4,1,16,0,3,12),\\
y={}&3\mathbf e_{14}+4\mathbf e_{16},\\
\eta={}&(138,105,72,74,147,33,8,15,21,27,48,21,221,36,0,138,0,21,105),\\
z={}&\mathbf e_3+\mathbf e_4+\mathbf e_6+\mathbf e_7.
\end{aligned}
\tag{29}
\]
Then, exactly,
\[
Qb=y,\qquad b^TQb=3,\qquad
Q\eta+z=9y,\qquad \eta^Ty=0.
\tag{30}
\]
Node \(14\) is type \(1\), with \(a_{14}=-2b_{14}\), and node \(16\)
is type \(3\), with \(b_{16}=0,a_{16}=2\).  Every coefficient of \(R\)
is nonnegative.

The endpoints \(E_4,F_3\), namely nodes \(4,7\), give
\[
n=3,\qquad\delta=1,\qquad d=9,
\tag{31}
\]
\[
b_4+b_7=18,\qquad
\eta_4+\eta_7=162.
\tag{32}
\]
The two remaining units in \(z\) occur at \(E_3,F_2\), namely nodes
\(3,6\).  They therefore describe exactly one degree-one residual
bridge with the sharp incidence found in
`FIXED_PLANE_RESIDUAL_ARM_ENTRY.md`.

The individual component equations are also exact:
\[
C^2=0,\qquad H^2=-1,\qquad g(H)=0,
\tag{33}
\]
\[
G\cdot C=162,\quad R\cdot C=52,\qquad
G\cdot H=81,\quad R\cdot H=26.
\tag{34}
\]
Finally the full square computed from (15) is
\[
C^2+H^2+\eta^TQ\eta+2\eta^Tz
=243=nd^2.
\tag{35}
\]

Even the degree-nine target curve and conductor residue are compatible
at curve level.  For \(AB=-2/3\), put
\[
\bar U(s)=As,\qquad
\bar V(s)=Bs^{-1}+A^8s^8.
\tag{36}
\]
Then
\[
\bar U\bar V-\bar U^9+\frac23=0,
\qquad
\operatorname {Res}_{s=0}(\bar U\,d\bar V)=\frac23.
\tag{37}
\]
This is a smooth affine degree-nine curve isomorphic to
\(\mathbf G_m\).

The word **witness** here means a witness to the integral intersection
ledger only.  The vectors in (29) do not construct two global sections
of a line bundle, a morphism \(\phi\), or a polynomial Keller map, and
they do not verify the local mapping data at every boundary crossing.
They prove compatibility of the displayed necessary numerical
conditions, nothing more.

## 6. Exact remaining failure

The witness in Section 5 is not a valid minimal Keller resolution.
Besides its two final dicritical curves \(14,16\), it has six final
point-mapping boundary curves:
\[
10,\ 11,\ 12,\ 15,\ 17,\ 18.
\tag{38}
\]
This violates the final-boundary requirement that every final curve be
type \(1\) or type \(3\).  Here “final” means that no later blowup was
centered on that exceptional curve, equivalently that its
self-intersection is still \(-1\); it need not be a leaf of the dual
graph.

Adding generic caps to these final curves and resolving the enlarged integer
system did not produce a replacement witness in the tested range, but
that computation is not a proof of impossibility.  Conversely, the
19-vertex ledger proves that the canonical, ramification, conductor,
residual-oddness, component-adjunction, and full \(G\)-effectivity
equations alone do not contradict one another.

The remaining finite target is therefore:
\[
\boxed{\text{combine (1)--(18) with finality/minimality, or derive a new
constraint on the six forced point-mapping tails.}}
\tag{39}
\]
The exact ledgers, the dual certificate (25), and the failure list (38)
are checked in
`verify_fixed_plane_global_pullback_system.py`.
