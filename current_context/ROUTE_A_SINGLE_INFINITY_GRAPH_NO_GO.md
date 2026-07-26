# Route A: the single cubic boundary does not give a Chau contradiction

Date: 25 July 2026

## Outcome

Assume the hypotheses and conclusions of
`ROUTE_A_LOG_TOPOLOGY_CUBIC_COLLAPSE.md`.  Thus the cubic normalization
\[
 \pi:Y\longrightarrow\mathbf A^2
\]
has one ramified boundary component \(E=Y\setminus S\), its branch
curve \(\Delta\) is irreducible, the normalization map
\[
 \mathbf A^1\longrightarrow\Delta
\tag{1}
\]
is finite and bijective, and every affine local inertia group is
\(C_2\).

Let
\[
 H=F\circ\pi_2:\mathbf A^2\longrightarrow\mathbf A^2
\]
be the canonical degree-six plane Keller lift, and let
\(\Gamma_D\) be the image of the distinguished line.  The finite
degree-six normalization has boundary
\[
 D_-\cup p^{-1}(E).
\tag{2}
\]
Therefore its nonproper-value set is exactly
\[
 \boxed{A_H=\Gamma_D\cup\Delta.}
\tag{3}
\]

The two most immediate hoped-for contradictions both fail, and they
fail for exact reasons.

> **Single-infinity graph no-go.**
>
> 1. The rational-tree boundary does not force \(\Delta\) to be
>    smooth.  For every \(m\ge1\), the local \(2+1\) cubic model over
>    \[
>    \Delta_m: y^2=x^{2m+1}
>    \tag{4}
>    \]
>    has ramified surface germ
>    \[
>    z^2=y^2-x^{2m+1}.
>    \tag{5}
>    \]
>    This is the rational double point \(A_{2m}\); its exceptional
>    divisor is a rational chain and its link is a rational homology
>    sphere.  Its ramification curve is the singular unibranch cusp
>    (4), and its local inertia is only \(C_2\).
>
> 2. The full nonproper set \(A_H\) is never simply connected.
>    The normalization of \(\Gamma_D\) is \(\mathbf A^1\), but the
>    normalization map identifies at least two distinct points.
>    If
>    \[
>    \rho_\Gamma
>    =
>    \sum_{q\in\Gamma_D}
>       \bigl(\#\nu_\Gamma^{-1}(q)-1\bigr),
>    \tag{6}
>    \]
>    then \(\rho_\Gamma\ge1\) and
>    \[
>    \pi_1(\Gamma_D)\simeq F_{\rho_\Gamma}.
>    \tag{7}
>    \]
>    If \(k=\#(\Gamma_D\cap\Delta)\ge1\), then
>    \[
>    \boxed{
>    \pi_1(A_H)
>    \simeq F_{\rho_\Gamma+k-1}.
>    }
>    \tag{8}
>    \]
>    If \(k=0\), \(A_H\) is disconnected.  In either case the
>    simply-connected exceptional-curve prohibition does not apply.

The deck involution does not alter this conclusion.  It exchanges
\(D_-\) with the retained \(D_+\), while it either fixes or permutes
the components over \(E\), according to the parity and residue of the
valuation of \(u\) along \(E\).  Every component over \(E\) still has
target image \(\Delta\).  The involution changes the source-boundary
covering data, not the target union (3), and supplies no two-cell that
could kill the free subgroup (7).

Thus the log-topology collapse is strong but stops one step short of a
Chau contradiction.  The surviving obstruction must use monodromy or
determinant labels at the common point at infinity, not merely:

- rationality of the source boundary tree;
- bijectivity of the normalization of \(\Delta\);
- the one-point-at-infinity theorem for \(A_H\); or
- the deck action on the two source-boundary arms.

## 1. Why the boundary images give the whole nonproper set

Let
\[
 \widetilde Y\longrightarrow\mathbf A^2
\]
be the finite degree-six normalization containing the source plane as
the open subset
\[
 \mathbf A^2=\widetilde Y\setminus
 \bigl(D_-\cup p^{-1}(E)\bigr).
\tag{9}
\]
Every boundary point gives a sequence in the open plane escaping to
infinity whose \(H\)-image converges to the finite image of that point.
Conversely, a nonproper sequence for \(H\) has, after passing to the
finite normalization and a subsequence, a limit over its limiting
target value.  Since it has no limit in the source plane, that limit
lies in (9)'s boundary.  Hence
\[
 A_H=
 \operatorname {image}(D_-)
 \cup\operatorname {image}(p^{-1}(E)).
\tag{10}
\]
The first image is \(\Gamma_D\), and the second is \(\Delta\), proving
(3).  The two curves are distinct because the cubic branch-section
theorem says that \(\Gamma_D\) is not a branch component.

## 2. A rational-chain singularity with cuspidal branch

Fix \(m\ge1\), and put
\[
 f_m(x,y)=y^2-x^{2m+1}.
\tag{11}
\]
The normalization
\[
 t\longmapsto(t^2,t^{2m+1})
\tag{12}
\]
is finite and bijective.  The image is singular and unibranch at the
origin.

Consider the rank-two cover
\[
 Z_m:
 \quad z^2=f_m(x,y).
\tag{13}
\]
After the linear change
\[
 r=z-y,\qquad s=z+y,
\]
equation (13) becomes
\[
 rs=-x^{2m+1}.
\tag{14}
\]
This is the \(A_{2m}\) rational double point.  It is normal and
Gorenstein, its minimal exceptional divisor is a chain of \(2m\)
smooth rational curves, and its link has finite first homology.

The ramification curve on \(Z_m\) is
\[
 V(z,f_m)\simeq V(f_m)=\Delta_m.
\tag{15}
\]
It is singular and unibranch.  Adding a disjoint étale degree-one
factor gives the completed local \(2+1\) cubic algebra
\[
 \mathcal O_{\mathbf A^2,q}
 \ \times\
 \mathcal O_{\mathbf A^2,q}[z]/(z^2-f_m).
\tag{16}
\]
This is the correct henselian/semilocal form of a connected cubic cover
at a point with two support points.  It has:

- simple transposition inertia;
- no transitive local inertia;
- a Gorenstein normal ramified surface germ;
- a rational-chain exceptional divisor; and
- a singular bijectively normalized branch cusp.

The product in (16) is a local countermodel, not a claimed connected
global \(S_3\)-cover.  It proves precisely that the rational-tree and
local-inertia hypotheses do not imply smoothness of \(\Delta\).

## 3. The distinguished image already carries a free loop

The restriction of the plane Keller map to the distinguished line
\[
 L=V(a)\simeq\mathbf A^1
\]
is the normalization map
\[
 \nu_\Gamma:L\longrightarrow\Gamma_D.
\tag{17}
\]
It is finite and birational.  The smooth-collision theorem and
Gwoździewicz's injectivity-on-one-line theorem imply that it is not
injective: otherwise \(H\) would be an automorphism, contrary to its
geometric degree six.  The Keller differential makes (17) immersive,
so its singularities arise from identifications of distinct
normalization points rather than cuspidal ramification.

Topologically, a finite quotient of \(\mathbf A^1\simeq\mathbf R^2\)
obtained by identifying finite fibers deformation-retracts onto a
graph.  Its first Betti number is (6), and its fundamental group is the
free group in (7).  In particular
\[
 \rho_\Gamma\ge1.
\tag{18}
\]

## 4. Attaching the cubic branch cannot kill the loop

By the cubic-collapse theorem, \(\Delta\) is homeomorphic to
\(\mathbf A^1\), hence contractible.  The intersection
\[
 I=\Gamma_D\cap\Delta
\]
is finite because the curves are distinct.

If \(I=\varnothing\), the union (3) is disconnected.  Suppose
\(\#I=k\ge1\).  Replace the curves by small compatible graph
deformation retracts.  The intersection consists of \(k\) vertices.
The graph form of van Kampen, or equivalently joining two connected
graphs along \(k\) vertices, gives
\[
 \pi_1(\Gamma_D\cup\Delta)
 \simeq
 \pi_1(\Gamma_D)*\pi_1(\Delta)*F_{k-1}.
\tag{19}
\]
Since \(\pi_1(\Delta)=1\), equations (7) and (19) prove (8).
In particular the inclusion
\[
 \pi_1(\Gamma_D)\hookrightarrow\pi_1(A_H)
\tag{20}
\]
is injective.  Attaching a complex curve along finitely many points
adds graph edges; it cannot add a two-cell and kill an existing loop.

The one-point-at-infinity theorem says that the projective closures of
the components of \(A_H\) share one target point at infinity.  It does
not change the affine calculation (19).  Nor does the rational-tree
property of a source completion identify (19) with the dual graph of
that source boundary.  They are different graphs connected by a map,
and no graph isomorphism is forced.

## 5. Exact scope of the Chau input

The relevant primary statements in Nguyen Van Chau,
*Two remarks on non-zero constant Jacobian polynomial maps of
\(\mathbf C^2\)*, Ann. Polon. Math. 82 (2003), 39--44, are:

1. Theorem 4: a polynomial map whose nonproper set has an irreducible
   component isomorphic to the affine line must have singularities.
2. Corollary 3: the exceptional value set of a Keller map cannot be a
   simply connected curve.

Statement 1 does not apply to a singular cusp such as (4), even though
its normalization map is bijective.  Statement 2 does not apply because
(7)--(8) show that the full exceptional curve (3) is not simply
connected.  Chau's 2004 one-point-at-infinity theorem imposes a common
projective endpoint but does not change this affine fundamental group.

Therefore no contradiction follows from the cited Chau results.  A
stronger componentwise theorem excluding singular finite-bijective
dicritical parametrizations would close the route, but that statement
is not among the primary results verified here.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_single_infinity_graph_no_go.py
```

for the cusp normalization, the \(A_{2m}\) change of variables,
singular-locus equations, the \(2+1\) length ledger, and the free-rank
formula (8).  The rational-double-point classification, finite
normalization boundary criterion, and van Kampen argument are
theorem-level inputs proved above.
