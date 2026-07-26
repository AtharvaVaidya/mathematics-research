# Route A: unbranched cubic collision above the distinguished line

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad
S=\operatorname {Spec}B,
\]
and suppose that a Darboux pair \(P,Q\in B\) induces an étale map
\[
F=(P,Q):S\longrightarrow\mathbf A^2
\]
of generic degree \(3\).  Put
\[
D=V(u,w)\simeq\mathbf A^1_v,\qquad
\Gamma_D=\overline{F(D)}=V(f).
\]

The cubic branch-section audit proves that \(\Gamma_D\) is not a branch
component of the finite normalization \(Y\to\mathbf A^2\).  This note
classifies the two possible generic decompositions over \(\Gamma_D\)
and audits the class group, conormal bundle, normal bundle, and
normalization conductor.

The result is a sharp no-go for these invariants:

> **Unbranched collision theorem.** At the generic point of
> \(\Gamma_D\), the decomposition in \(Y\) is exactly one of
> \[
> 1+2,\qquad 1+1+1.
> \]
> The degree-one prime supplied by \(D\) is retained in \(S\), and the
> mandatory collision theorem forces at least one additional prime to
> be retained.  If exactly one additional prime \(C\) is retained, then
> \[
> \operatorname {div}_S(f(P,Q))=D+C,\qquad [C]=[D]\ne0.
> \]
> If two additional primes \(C_1,C_2\) are retained, then
> \[
> \operatorname {div}_S(f(P,Q))=D+C_1+C_2,\qquad
> [C_1]+[C_2]=[D].
> \]
> Thus exactly one of \(C_1,C_2\) has the nonzero class in
> \(\operatorname {Cl}(B)\simeq\mathbf Z/2\).

No contradiction follows from these relations.  Normal bundles become
trivial on \(D\simeq\mathbf A^1\), the conormal of the total pullback is
trivial because it is principal, and the conductor of
\(D\to\Gamma_D\) is a principal ideal in \(\mathbf C[v]\).

There are exact global countermodels for both generic decompositions.
Most sharply, the map on the same quadratic pseudoplane
\[
\Psi:S\longrightarrow\mathbf A^2,\qquad
x=w,\qquad y=-v-2uv^2,
\tag{1}
\]
has generic degree \(3\), is unramified above the generic point of
\(x=0\), and has three degree-one primes there: \(D\), \(H\), and one
prime omitted from \(S\).  On \(S\),
\[
\operatorname {div}(x)=D+H,\qquad [D]=[H]\ne0.
\]
Its Jacobian bracket is \(1\) on both retained components, but is not
constant globally.  Thus the entire divisor, class, normal-bundle, and
generic-degree package coexists on \(S\).  Any exclusion must use the
global Darboux equation away from the collision divisor.

## 1. The decomposition table

Let \(A' \subset K=\operatorname {Frac}B\) be the integral closure of
\(\mathbf C[P,Q]\), and put \(Y=\operatorname {Spec}A'\).  As in the
degree-two and cubic branch audits, the induced map \(S\to Y\) is an
open immersion.

Let \(\overline D\) denote the closure of \(D\) in \(Y\).  The map
\[
D\longrightarrow\Gamma_D
\]
is the normalization and has residue degree one.  Since \(\Gamma_D\)
is not a branch component, all ramification indices over its generic
point are one.  The DVR degree formula therefore gives
\[
3=\sum_i f_i
\]
with one distinguished summand \(f_{\overline D}=1\).  The only
possibilities are
\[
\begin{array}{c|c}
\text{type}&\text{primes and residue degrees}\\ \hline
1+2&\overline D(1),\ \overline C(2),\\
1+1+1&\overline D(1),\ \overline C_1(1),\
       \overline C_2(1).
\end{array}
\tag{2}
\]

A prime of \(Y\) is called retained if it meets the open set \(S\).
Its intersection with \(S\) is then a prime divisor.  The mandatory
collision theorem says that at least one prime other than
\(\overline D\) is retained.

Set
\[
g=f(P,Q).
\]
Because \(F\) is étale, the pullback of the reduced curve
\(V(f)\) is reduced.  Hence every retained prime in
\(\operatorname {div}_S(g)\) has multiplicity one.

For type \(1+2\), the degree-two prime must be retained, and
\[
\operatorname {div}_S(g)=D+C.
\tag{3}
\]

For type \(1+1+1\), either exactly one additional prime is retained,
again giving (3), or both are retained and
\[
\operatorname {div}_S(g)=D+C_1+C_2.
\tag{4}
\]
An unramified prime may be omitted from \(S\); étaleness only forces
ramified primes to be omitted, not the converse.

## 2. Exact class-group consequences

The pseudoplane has
\[
B^\times=\mathbf C^\times,\qquad
\operatorname {Cl}(B)=\langle[D]\rangle\simeq\mathbf Z/2,
\qquad [D]\ne0.
\tag{5}
\]

Taking classes in (3) gives
\[
[C]=-[D]=[D].
\tag{6}
\]
Thus the unique additional retained component must be nonprincipal.

Taking classes in (4) gives
\[
[C_1]+[C_2]=[D].
\tag{7}
\]
Since the only classes are \(0\) and \([D]\), exactly one of
\(C_1,C_2\) is principal and the other has class \([D]\).

These conditions are internally consistent.  The standard class-mate
\[
H=V(1+uv,w)\simeq\mathbf G_m
\]
satisfies
\[
\operatorname {div}(w)=D+H,\qquad [H]=[D],
\tag{8}
\]
and the principal prime
\[
C_0=V(u-1)\simeq\mathbf A^1
\]
has class zero.

There is one genuine refinement from the earlier exact \(D+H\) audit.
If (3) holds, then \(C\ne H\): the exact architecture
\[
\operatorname {div}_S(g)=D+H
\]
is impossible for a Darboux map.  In type \(1+1+1\), \(H\) can occur
only if the third, principal component is also retained.

## 3. Why normal bundles add no obstruction

Let
\[
Z=V(g)=F^{-1}(\Gamma_D)\subset S.
\]
It is an effective principal Cartier divisor.  Because it is an étale
base change of the plane Cartier divisor \(\Gamma_D\), its conormal
bundle is
\[
I_Z/I_Z^2
\simeq (F|_Z)^*(I_{\Gamma_D}/I_{\Gamma_D}^2)
\simeq\mathcal O_Z.
\tag{9}
\]

The distinguished component has
\[
N_{D/S}\simeq\mathcal O_S(D)|_D.
\]
Although \(\mathcal O_S(D)\) is the nontrivial two-torsion line bundle
on \(S\), its restriction to \(D\simeq\mathbf A^1\) is trivial:
\[
\operatorname {Pic}(\mathbf A^1)=0.
\tag{10}
\]

If \(R=Z-D\), restriction of the principal divisor relation gives,
where intersections are interpreted Cartier-theoretically,
\[
N_{D/S}\otimes\mathcal O_D(R|_D)\simeq\mathcal O_D.
\tag{11}
\]
Every finite divisor on \(\mathbf A^1\) is principal, so (11) imposes
no numerical degree condition.  This is precisely where an argument
that would work on a complete curve loses its force.

## 4. Why the normalization conductor adds no obstruction

The restriction
\[
D=\mathbf A^1_v\longrightarrow\Gamma_D
\]
is the normalization.  If \(\Gamma_D\) is singular, its conductor pulls
back to an ideal
\[
(c(v))\subset\mathbf C[v].
\tag{12}
\]
It is supported at the finitely many preimages of the singular points
and is principal because \(\mathbf C[v]\) is a PID.

Ambient étaleness has a useful local interpretation but gives no new
class.  At a point of \(D\) above a singular point of \(\Gamma_D\), the
completed germ of \(Z\) is an étale copy of the completed plane-curve
germ.  The other local branches are supplied by collision components
meeting \(D\).  This records incidence and sheet gluing, but the
conductor divisor (12) remains principal on \(D\).

If \(\Gamma_D\) is smooth, the conductor is the unit ideal.  The exact
countermodel below already has a smooth target line, so conductor data
cannot furnish a universal contradiction.

The inclusion \(A'\subset B\) itself is not a finite normalization
extension: it realizes \(S\) as an open subset of \(Y\).  Consequently
the usual finite-ring conductor is not a mechanism for recovering the
omitted divisors; for localizations it is typically zero.

## 5. Same-surface degree-three countermodel for \(1+1+1\)

Put
\[
s=uv,\qquad
A(s)=s(1+s)(1+2s).
\]
On the Laurent chart,
\[
\operatorname {Frac}B=\mathbf C(s,w),\qquad
v=\frac{s(1+s)}{w^2}.
\]
The map (1) becomes
\[
x=w,\qquad y=-\frac{A(s)}{w^2}.
\tag{13}
\]
Thus \(s\) satisfies
\[
A(s)+yw^2=0,
\tag{14}
\]
a cubic equation.  Since \(A\) has degree three and the rational
function in (13) has degree three in \(s\), the generic degree is
exactly \(3\).

Above \(x=w=0\), equation (14) has the three simple roots
\[
s=0,\qquad s=-1,\qquad s=-\frac12.
\tag{15}
\]
They correspond respectively to

1. \(D\), retained in \(S\);
2. \(H\), retained in \(S\);
3. a prime at which \(u=w^2/(1+s)\to0\) but
   \(v=s/u\to\infty\), hence omitted from the affine surface \(S\).

All three roots in (15) are simple:
\[
A'(0)=1,\qquad A'(-1)=1,\qquad A'(-1/2)=-1/2.
\]
Therefore \(x=0\) is unbranched in the cubic normalization.

On the two retained components,
\[
\begin{array}{c|c}
D& y=-v,\\
H& y=v=-u^{-1}.
\end{array}
\]
Both have residue degree one.  Moreover
\[
\operatorname {div}_S(x)=\operatorname {div}(w)=D+H,
\]
so the class relation is exactly (6), while the third degree-one prime
is lost at the boundary.

The Poisson Jacobian of (1) is
\[
\{x,y\}=1+6uv+6u^2v^2
       =1+6vw^2
       =A'(s).
\tag{16}
\]
It equals \(1\) identically on \(D\) and \(H\), and is nonzero on the
third generic prime.  It is not constant on \(S\), so (1) is not a
Darboux map.  This isolates the missing input exactly: the collision
geometry and divisor theory are correct, but the Jacobian fails away
from the special fiber.

## 6. Exact degree-three countermodel for \(1+2\)

Consider the finite cubic map
\[
\Phi:\mathbf A^2_{t,y}\longrightarrow\mathbf A^2_{x,y},\qquad
x=t(t^2+yt+1),\qquad y=y.
\tag{17}
\]
Its Jacobian is
\[
J_\Phi=3t^2+2yt+1.
\tag{18}
\]
Delete its ramification curve and put
\[
U=\mathbf A^2_{t,y}\setminus V(3t^2+2yt+1).
\]
Then \(\Phi|_U\) is everywhere étale and still has generic degree three.

Above the generically unbranched target line \(x=0\),
\[
\Phi^*(x)=t(t^2+yt+1).
\]
The first component
\[
D_0=V(t)\simeq\mathbf A^1_y
\]
maps isomorphically and remains entirely in \(U\), because
\(J_\Phi|_{D_0}=1\).  The second component is
\[
C_2=V(t^2+yt+1)\simeq\mathbf G_m,
\qquad y=-t-t^{-1},
\]
and has residue degree two over \(\mathbf C(y)\).  On it,
\[
J_\Phi=t^2-1.
\]
Deleting the two ramification points \(t=\pm1\) leaves an étale
degree-two sheet.  This realizes the exact generic \(1+2\) geometry
while retaining a full affine-line degree-one sheet.

This model does not have the class group of \(S\):
\(\mathcal O(U)\) is a localization of a UFD and has nonconstant units.
Its role is to prove that degree-three algebra, generic étaleness,
surjectivity of the degree-one sheet, and the \(1+2\) decomposition are
mutually compatible.

On \(S\) itself, the class and first-neighborhood data of \(1+2\) also
coexist.  With
\[
q_2=v+uv^2+u^2,
\]
the map \((w,q_2)\) restricts to
\[
q_2|_D=v,\qquad q_2|_H=u^2,
\]
and its Jacobian is nonzero generically on both \(D\) and \(H\).
This same-surface model has generic degree five, not three.  It confirms
that the class and normal data themselves do not obstruct residue
degree two, while honestly marking the degree mismatch.

## 7. Consequence for the live route

The complete information supplied by the audited invariants is the
table (2)--(7), plus the exclusion of the exact two-component \(D+H\)
architecture for an actual Darboux pair.  Both generic decompositions
have exact algebraic models, and type \(1+1+1\) has a degree-three model
on the pseudoplane itself satisfying the correct class relation and
Jacobian equation along the entire retained collision fiber.

The promising next problem is therefore construction/obstruction for
the **global** equation
\[
\{P,Q\}=1
\]
starting from (1).  Perturbations must change the Jacobian away from
\(w=0\) without destroying the three-sheet boundary pattern.  Divisor
classes, normal bundles, and conductors have no remaining contradiction
to offer.

## Theorem-level inputs

The exact verifier checks every displayed polynomial and degree
calculation in the countermodels.  The following remain theorem-level:

1. the open immersion \(S\subset Y\);
2. the prior proof that \(\Gamma_D\) is not a branch component;
3. the mandatory collision theorem;
4. the class-group computation
   \(\operatorname {Cl}(B)=\mathbf Z/2\);
5. the exact \(D+H\) Darboux no-go.
