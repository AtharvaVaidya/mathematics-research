# Route A: the global residual-to-dicritical bridge is non-additive

Date: 25 July 2026

## Outcome

Retain the hypothetical Route A map
\[
 F:S\longrightarrow {\bf A}^2,\qquad
 S=\operatorname {Spec}
 {\bf C}[u,v,w]/(w^2-u-u^2v),
\tag{1}
\]
where \(F\) is etale of geometric degree three.  Let
\[
 \pi:Y\longrightarrow{\bf A}^2
\]
be the finite cubic normalization, let \(R=Y\setminus S\), and let
\[
 D=V(u,w)\simeq{\bf A}^1_v,\qquad
 \Gamma=\overline{F(D)}.
\]
After base change along the normalization \(D\to\Gamma\), write
\[
 {\cal A}_D\simeq {\bf C}[v]\times
 {\bf C}[v,\tau]/(\tau^2-g(v)).
\tag{2}
\]

There is an exact global compactification of the degree-six plane
composite \(H=F\circ\pi _2\).  It gives the following sharp answer to
the proposed residual-to-dicritical bridge.

> **Separation theorem.**  Let \(v_0\in{\bf A}^1\) be a zero of \(g\).
> The distinguished point over \(v_0\) lies on \(D\subset S\).  The
> point supporting the non-etale residual factor lies in
> \(R=Y\setminus S\), and the two points are distinct in the finite
> cubic fiber.  If \(\operatorname {ord}_{v_0}g\) is odd, the normalized
> residual double cover ramifies at the latter point.
>
> In the canonical finite degree-six normalization, the distinguished
> point has two lifts:
> \[
> d_+(v_0)\in{\bf A}^2,\qquad d_-(v_0)\in\widetilde Y\setminus{\bf A}^2.
> \]
> Every lift of the residual point lies instead over
> \(R\).  Thus an odd residual place gives two **separated boundary
> phenomena over the same target value**:
> \[
> \boxed{\text{one point on the fixed distinguished divisor }D_-
> \quad+\quad
> \text{points on the pre-existing cubic boundary}.}
> \tag{3}
> \]
> It does not produce a new boundary divisor or a new dicritical class.

The distinguished divisor is etale over the target at every one of
these points.  Its Orevkov summand is the already-known constant \(1\);
no root of \(g\) creates an exceptional local-degree excess on it.
In the smooth split local form of a simple branch point, the other two
cubic sheets have total length two, and their canonical double lifts
have total length four.  This realizes the already-known residual
four-sheet loss with no exceptional excess.  Several roots merely give
points on the fixed finite collection of boundary components; they do
not add components.  One component can carry arbitrarily many such
points in the exact local model below.  The losses are not thereby
added again in the global formula
\[
 \deg_{\rm geo}H-1=5.
\]

The deck involution supplies no missing pairing theorem.  It exchanges
the distinguished boundary divisor \(D_-\) with the retained divisor
\(D_+\), so it does not even preserve the plane boundary.  Over a
cubic boundary prime \(E\), whether a prolongation is fixed or paired
is controlled by the generic valuation of \(u\) at \(E\), not by the
parity of an intersection of \(E\)'s target image with \(\Gamma\).

Finally, if \(\deg g\) is odd, the ramified place at \(v=\infty\) lies
over the point at infinity of the polynomial curve \(\Gamma\).  It is
an endpoint in a projective boundary, not an affine nonproper value,
and hence does not determine an additional affine dicritical class.

Consequently the compactification does map every finite odd place to
the cubic boundary, but only as a **point on an existing boundary
component**.  It does not supply the hoped-for injection from odd
places to non-distinguished dicritical classes, or to independent
positive Orevkov summands.  The exact model below shows that no such
injection follows from the local compactification and sheet data.
A contradiction would need a new intersection bound for the fixed
boundary curves, not the residual defect budget.

## 1. The canonical finite double completion of the plane chart

Put \(K={\bf C}(S)\) and \(M=K(a)\), where \(a^2=u\).  The integral
closure of \({\bf C}[S]\) in \(M\) is
\[
 \widetilde B
 ={\bf C}[a,v,z]/(z^2-1-a^2v),
\tag{4}
\]
with
\[
 u=a^2,\qquad w=az.
\tag{5}
\]
The involution
\[
 \iota(a,v,z)=(-a,v,-z)
\tag{6}
\]
is fixed-point free, and its invariant ring is \({\bf C}[S]\).
Therefore
\[
 p:\widetilde S=\operatorname {Spec}\widetilde B\longrightarrow S
\tag{7}
\]
is a connected finite etale double cover.

Above \(D\) are the two disjoint divisors
\[
 D_+=V(a,z-1),\qquad D_-=V(a,z+1).
\tag{8}
\]
The polynomial plane chart is exactly
\[
 {\bf A}^2_{a,b}\simeq\widetilde S\setminus D_-,
\tag{9}
\]
under
\[
 z=1+2a^2b,\qquad
 v=4b(1+a^2b).
\tag{10}
\]
Indeed, on \(a\ne0\) its inverse is
\[
 b=\frac{z-1}{2a^2},
\]
while near \(D_+\) the same function is
\[
 b=\frac{v}{2(z+1)}.
\]
These expressions agree by (4) and cover the complement of \(D_-\).
The map (5) then becomes the canonical quadratic pseudoplane chart
\[
 u=a^2,\quad
 w=a(1+2a^2b),\quad
 v=4b(1+a^2b).
\tag{11}
\]

Let \(\widetilde Y\) be the normalization of \(Y\) in \(M\).
Transitivity of integral closure gives a finite tower
\[
 \widetilde Y\longrightarrow Y\longrightarrow{\bf A}^2
\tag{12}
\]
of generic degrees two and three.  Over the open set \(S\subset Y\),
the first map is (7).  Consequently (9) identifies the source plane
with an open subset of \(\widetilde Y\), and
\[
 \boxed{
 \widetilde Y\setminus{\bf A}^2
 =
 D_-\ \cup\
 \bigl(\widetilde Y\setminus\widetilde S\bigr),
 \qquad
 \widetilde Y\setminus\widetilde S
 =p^{-1}(R)
 }
\tag{13}
\]
set-theoretically.  The finite degree-six map in (12) restricts to
\(H=F\circ\pi _2\) on the plane.

This is the relevant global compactification.  It does not require a
choice of a projective resolution, and any later regular dicritical
model dominates it.

The involution (6) extends to \(\widetilde Y\), because normalization
is functorial under the Galois action of \(M/K\).  But
\[
 \iota(D_-)=D_+,\qquad
 D_+\subset{\bf A}^2,\quad
 D_-\cap{\bf A}^2=\varnothing.
\tag{14}
\]
Thus the involution does not preserve the boundary of the plane open.
This already rules out a blanket assertion that deck symmetry pairs
all dicritical divisors.

## 2. A residual branch point is necessarily on the cubic boundary

The first factor in (2) is the distinguished section.  At \(v=v_0\)
it gives a reduced point
\[
 d(v_0)\in D\subset S.
\]
If \(g(v_0)=0\), the second factor has a different underlying point
\[
 e(v_0)\in Y
\]
whose local fiber algebra is non-etale.  The two points are different
even when the residual factor is nonreduced, because the product
decomposition (2) is defined by complementary idempotents.

Suppose \(e(v_0)\) lay in \(S\).  Base change of the etale morphism
\(F:S\to{\bf A}^2\) along \(D\to{\bf A}^2\) would be etale at
\(e(v_0)\).  This contradicts the non-etale residual algebra at a zero
of \(g\).  Therefore
\[
 \boxed{e(v_0)\in R.}
\tag{15}
\]
In particular its target value
\[
 q_0=F(d(v_0))=\pi(e(v_0))
\]
lies on the cubic branch curve and on the nonproper-value set of
\(F\).

Writing \(g=c h^2s\) with \(s\) squarefree, the normalized residual
function field is
\[
 {\bf C}(v)(\sqrt{s}).
\]
If \(\operatorname {ord}_{v_0}g\) is odd, \(s(v_0)=0\), and the
normalized residual curve has one point of local degree two over
\(v_0\).  This point maps to (15).  Thus every finite odd place is an
endpoint of the retained residual curve on the cubic boundary.

Now pass to \(\widetilde Y\).  Since \(p\) is etale over \(S\), the
point \(d(v_0)\) has the two lifts
\[
 d_+(v_0)\in D_+,\qquad d_-(v_0)\in D_-.
\tag{16}
\]
By (9), only \(d_+(v_0)\) lies in the source plane.  Every point above
\(e(v_0)\in R\) lies in \(p^{-1}(R)\), by (13).  Equations
(15)--(16) prove the separation (3).

Notice what has and has not happened.  Varying \(v_0\) moves points on
the fixed curves \(D_-\) and \(p^{-1}(R)\).  It does not add
irreducible components to either curve.  Intersection multiplicity in
the target cannot be converted into the number of source boundary
components.

## 3. The distinguished local degree never jumps at a root

At every point of \(D_-\), the finite map
\[
 \widetilde S\longrightarrow S\stackrel F\longrightarrow{\bf A}^2
\]
is etale: the first arrow is finite etale and the second is etale on
all of \(S\).  Hence the two-dimensional local degree along \(D_-\)
is exactly one at every \(d_-(v_0)\), independently of \(g(v_0)\).

Equivalently, in the exact plane-at-infinity chart
\[
 (a,b)=(-t+\eta t^3,-t^{-2})
\]
the composite extends polynomially and has constant nonzero Jacobian.
On \(t=0\),
\[
 v=-8\eta,
\]
so every finite residual root corresponds to an ordinary value of the
same parameter \(\eta\).  No root is an exceptional local-degree value
of the distinguished dicritical map.

This proves
\[
 \boxed{\text{all finite roots of }g\text{ cost zero additional
 distinguished defect}.}
\tag{17}
\]
The distinguished class contributes its single unit once, not once
per point on it.

At a smooth simple cubic branch point where the quadratic
normalization is flat (in particular in the split local model below),
the residual point in \(Y\) has local length two.  The total degree of
its inverse image under \(\widetilde Y\to Y\) is two, so all boundary
points above it have total length
\[
 2\cdot2=4
\tag{18}
\]
in the degree-six map.  This is the four-sheet residual loss already
available in the non-distinguished budget.  Several branch points
reuse the same generic four sheets.

## 4. Exact transverse local model

The non-additivity can be seen without a coefficient search.  Let
\[
 \Gamma=V(y),\qquad \Delta=V(x)
\]
meet transversely at the origin.  The strict henselian local normal
form of a simple cubic branch, separated into its distinguished and
ramified points, is
\[
 Y_0={\bf A}^2_{x,y}\longrightarrow{\bf A}^2_{x,y},
\qquad
 Y_1={\bf A}^2_{r,y}\longrightarrow{\bf A}^2_{x,y},
\quad x=r^2.
\tag{19}
\]
The first component is the retained simple sheet.  On the second,
delete \(E=V(r)\); this is the omitted ramified double sheet.  Along
\(\Gamma\), the residual algebra is
\[
 \tau^2=x,
\tag{20}
\]
so the origin is an odd residual branch place.

Assume the canonical quadratic extension is split at the displayed
closed points; this is one of the allowed valuation cases.  Its local
degree-six normalization consists of two copies
\[
 Y_0^+,Y_0^-,Y_1^+,Y_1^-.
\]
The plane open contains
\[
 Y_0^+,\qquad
 Y_0^-\setminus V(y),\qquad
 Y_1^\pm\setminus V(r).
\tag{21}
\]
Thus the number of retained sheets and the missing local degrees are
\[
\begin{array}{c|c|c}
\text{target stratum}&\#H^{-1}(q)&\text{missing degree}\\ \hline
x\ne0,\ y\ne0&6&0\\
y=0,\ x\ne0&5&1\\
x=0,\ y\ne0&2&4\\
x=y=0&1&5.
\end{array}
\tag{22}
\]
At the origin the boundary points are separated:

* \(V(y)\subset Y_0^-\) maps etale with local degree one to
  \(\Gamma\);
* \(V(r)\subset Y_1^+\) and \(V(r)\subset Y_1^-\) each map with local
  degree two to \(\Delta\).

Hence
\[
 5=1+2+2.
\tag{23}
\]
The intersection point produces no fourth boundary component and no
excess over (23).  Replacing the single transverse intersection by
several transverse intersections changes the number of points on
these same components, not their generic local degrees.

There is an exact simultaneous version with arbitrarily many
intersections.  For a squarefree polynomial \(h(x)\), keep
\(\Gamma=V(y)\) and replace the ramified component in (19) by
\[
 {\bf A}^2_{x,r}\longrightarrow{\bf A}^2_{x,y},
 \qquad y=r^2+h(x).
\tag{24}
\]
Its one ramification divisor \(V(r)\) maps isomorphically to the one
smooth branch curve
\[
 \Delta=V(y-h(x)).
\]
Along \(\Gamma\), the residual equation is
\[
 r^2=-h(x).
\]
Every root of \(h\) is therefore an odd residual place, but all of
them lie on the same ramification divisor \(V(r)\).  This gives an
exact algebraic countermodel to any point-to-component count.  As with
(19), it is a local/semilocal cover model, not a connected global
Keller map.

Model (19)--(23) is a local normal form, not a global Keller
counterexample.  Its role is exact: it shows that simple odd residual
ramification, the actual distinguished boundary loss, the cubic
ramification boundary, and the full degree-six sheet ledger are
simultaneously locally compatible.

## 5. Why the deck action cannot supply the missing parity

Let \(E\) be a prime divisor of \(R\), and write
\[
 r_E=\operatorname {ord}_E(u).
\]
The prolongations of its valuation to \(M=K(\sqrt u)\) obey the usual
quadratic valuation rule:

* if \(r_E\) is odd, there is one ramified prolongation, fixed as a
  prime by the deck involution;
* if \(r_E\) is even, write \(u=t^{2k}\epsilon\).  The prolongation
  splits into a paired pair exactly when the residue
  \(\bar\epsilon\in{\bf C}(E)^\times\) is a square;
* if that residue is not a square, there is one unramified inert
  prolongation, again fixed as a prime.

Thus “the deck involution pairs all non-distinguished dicritical
classes without fixed classes” would require two new assertions for
every relevant \(E\): evenness of \(r_E\) and squareness of the
residual unit.  The oddness of
\(\operatorname {ord}_{v_0}g\) is instead the local intersection
parity of \(\Gamma\) with the cubic branch image at a closed target
point.  It does not determine the generic divisorial valuation
\(r_E\) or its residue square class.

This distinction is visible already on the distinguished divisor:
\[
 \operatorname {ord}_D(u)=2
\]
and the cover splits as \(D_+\sqcup D_-\), but the involution exchanges
one retained and one omitted divisor rather than pairing two
dicritical divisors.

## 6. The odd place at infinity

The normalization map \(D={\bf A}^1\to\Gamma\) is polynomial and
extends to the projective normalization
\[
 \overline\nu_D:{\bf P}^1\longrightarrow\overline\Gamma\subset{\bf P}^2.
\]
Its point \(v=\infty\) maps to the target line at infinity.  If
\(\deg g\) is odd, the normalized residual double cover has one
ramified point over \(v=\infty\).  This is an endpoint over
\(\overline\nu_D(\infty)\), not a point of the affine curve
\(\Gamma\subset{\bf A}^2\).

An affine dicritical component is a boundary divisor mapping
dominantly to an affine component of the nonproper-value set.  A
single endpoint over the target line at infinity supplies neither a
new divisor nor such a dominant map.  Therefore odd degree of \(g\)
does not force an additional affine dicritical class.

## 7. Exact conclusion and next viable target

The global compactification supplies a real theorem, but it points in
the opposite direction from the proposed root count:
\[
\begin{array}{c|c}
\text{residual datum}&\text{global boundary meaning}\\ \hline
\text{finite odd place}&
\text{a point where the residual curve meets }R\\
\text{distinguished lift}&
\text{a point on the one fixed divisor }D_-\\
\text{other degree-six lifts}&
\text{points on }p^{-1}(R)\\
\text{odd place at infinity}&
\text{one projective endpoint over }L_\infty.
\end{array}
\tag{25}
\]

None of these rows is an injection into boundary components.  Orevkov's
defect is a sum over dicritical components and their exceptional local
degrees, whereas the roots of \(g\) are intersection points of the
fixed target curves \(\Gamma\) and the cubic branch image.  The
distinguished local degree is constant at those points, and the local
model (19)--(23) shows that the residual four-sheet loss need not jump.

The next viable global input is consequently an intersection theorem,
for example a bound on
\[
 \overline\Gamma\cdot\overline\Delta
\]
derived from the actual divisor classes of \(D_-\) and
\(p^{-1}(R)\) on a common projective completion.  The degree-six defect
formula alone cannot provide that bound.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_global_monodromy_dicritical_bridge_no_go.py
```

for the canonical normalization, plane-open chart, deck action,
pseudoplane relation, constant Jacobian of the distinguished
infinity chart, quadratic valuation parity samples, residual local
normal form, and the exact sheet ledger (22)--(23).

The geometric-degree formula referenced here is equation (4.10) of
Nguyen Van Chau, *Non-zero constant Jacobian polynomial maps of
\({\bf C}^2\)*, Ann. Polon. Math. **71** (1999), 287--310.
