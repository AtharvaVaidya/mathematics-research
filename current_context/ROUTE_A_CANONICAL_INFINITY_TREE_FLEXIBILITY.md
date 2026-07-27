# Route A: the canonical pseudoplane arm does not determine the infinity tree

Date: 25 July 2026

## Outcome

Let
\[
 \pi_2:{\bf A}^2_{a,b}\longrightarrow
 S=\operatorname {Spec}
 {\bf C}[u,v,w]/(w^2-u-u^2v)
\tag{1}
\]
be the canonical quadratic chart
\[
 u=a^2,\qquad
 v=4b(1+a^2b),\qquad
 w=a(1+2a^2b).
\tag{2}
\]
Its finite etale completion
\[
 \widetilde S
 =
 \operatorname {Spec}
 {\bf C}[a,v,z]/(z^2-1-a^2v)
\]
adds the divisor
\[
 D_-=V(a,z+1)\simeq{\bf A}^1_v.
\]

There is a canonical minimal **local regular point-blowup extraction**
of \(D_-\) from the standard completion
\[
 {\bf A}^2_{a,b}\subset{\bf P}^1_a\times{\bf P}^1_b.
\]
Put \(s=1/b\).  Four ordinary point blowups over
\((a,s)=(0,0)\) are necessary and sufficient for the valuation of
\(D_-\) to appear with a nonconstant residue parameter.  The
resulting boundary arm is
\[
\begin{array}{ccccccc}
 &&E_1&&&&\\[-2mm]
 &&|&&&&\\[-1mm]
 B_\infty&-&E_2&-&E_3&-&D_- ,
\end{array}
\tag{3}
\]
where the horizontal display is understood as
\(B_\infty-E_2-E_3-D_-\), with the extra leaf \(E_1\) attached to
\(E_2\).  Its exact labels are
\[
\begin{array}{c|ccccc}
 &B_\infty&E_1&E_2&E_3&D_-\\ \hline
\text{self-intersection}&-2&-2&-2&-2&-1\\
1+\operatorname {ord}(da\wedge db)&-1&0&-1&0&1\\
\operatorname {ord}(a)&0&1&1&1&1\\
\operatorname {ord}(s)&1&1&2&2&2\\
(\operatorname {ord}u,\operatorname {ord}v,
 \operatorname {ord}w)
&(0,-2,-1)&(2,-1,1)&(2,-2,1)&(2,-1,1)&(2,0,1).
\end{array}
\tag{4}
\]
The self-intersection row in (4) belongs to this minimal four-blowup
model.  Further blowups centered on the arm can decrease those
self-intersections; the divisorial valuations and canonical orders in
the remaining rows are intrinsic to the displayed divisors.

The final divisor is selected by the key-polynomial valuation
\[
 \operatorname {ord}_{D_-}(a)=1,\qquad
 \operatorname {ord}_{D_-}(s)=2,\qquad
 \operatorname {ord}_{D_-}(s+a^2)=4.
\tag{5}
\]
Its affine parameter is
\[
 q_3=\frac{s+a^2}{a^4},
\qquad
 v|_{D_-}=4q_3.
\tag{6}
\]
In the exact dicritical chart
\[
 (a,b)=(-t+\eta t^3,-t^{-2}),
\]
one has
\[
 q_3|_{t=0}=-2\eta,\qquad
 v|_{t=0}=-8\eta.
\tag{7}
\]

This is the full local arm forced near
\((a,b)=(0,\infty)\) by the explicit pseudoplane chart.  It does
**not** determine a canonical minimal completion of the whole finite
degree-six normalization.  The remaining arms come from:

1. the closures of the cubic boundary \(R=Y\setminus S\);
2. the pole valuations of the unknown Darboux coordinates \(P,Q\);
3. the branch discriminant \(\Delta(P,Q)\); and
4. the resolution of their target curves at the line at infinity.

None of those data is determined by (1)--(7).

This limitation persists after imposing a minimal embedded resolution
on the target.  For every \(k\ge2\), put
\[
 r=k+1,\qquad \delta=2k+1
\tag{8}
\]
and consider the irreducible polynomially parametrized curve
\[
 \Delta_k:
 \quad
 (x,y)=\bigl(t^\delta,t^r-1\bigr),
\qquad
 (y+1)^\delta=x^r.
\tag{9}
\]
It has normalization \({\bf A}^1_t\), one place at infinity, and an
affine cusp at \((0,-1)\).  With the fixed line
\(\Gamma=V(y)\),
\[
 \deg\Delta_k=\delta,\qquad
 \deg\bigl(\Delta_k|_\Gamma\bigr)=r,\qquad
 I_\infty(\Gamma,\Delta_k)=k,
\tag{10}
\]
so
\[
 r+k=\delta.
\tag{11}
\]
At infinity the branch has primitive valuation pair
\[
 \bigl(\operatorname {ord}_q y,
       \operatorname {ord}_q z\bigr)
 =(k,2k+1),
\tag{12}
\]
and its minimal embedded resolution is governed by
\[
 \frac{2k+1}{k}=[2,k].
\tag{13}
\]
Here \([2,k]\) denotes the Euclidean/Puiseux quotient sequence, not a
choice of negative continued-fraction self-intersection convention.
Under the ordinary point-blowup convention in which the reduced total
transform is required to be simple normal crossings, the multiplicity
sequence is
\[
 k,\ k,\ \underbrace{1,\ldots,1}_{k\ {\rm times}}.
\]
Consequently the minimal embedded resolution uses exactly \(k+2\)
successive point blowups.  The final quotient \(k\), the length of the
multiplicity sequence, and hence the number of exceptional components
are unbounded.  Thus even the canonical minimal target resolution tree
can grow arbitrarily while preserving irreducibility, polynomial
parametrization, one place at infinity, and an affine singularity.
This particular cusp parametrization is finite and injective, but its
image is singular.  The cited Chau theorems exclude a smooth
\(\mathbf A^1\) component or a simply connected full nonproper set;
they do not give a componentwise prohibition for every singular
bijective parametrization.  The family's role is specifically to show
that the chart, Bezout data, and canonical minimal resolution alone do
not bound the tree.

The exact conclusion is therefore:

> **Canonical-arm theorem and no-go.**  The pseudoplane chart forces
> the four-blowup arm (3)--(7), ending in the etale index-one
> dicritical \(D_-\).  It supplies no labels on the cubic-boundary
> arms and no bound on the primitive infinity pair of the branch
> curve.  Canonical minimal resolution does not, by itself, couple
> \(I_\infty\) to the discriminant degree: the family (8)--(13)
> realizes unbounded minimal trees with
> \[
> I_\infty=k,\qquad \delta=2k+1.
> \]

This does not construct a Keller map.  It closes the proposed
deduction from the explicit chart plus canonical minimality.  A
further obstruction would need an additional theorem coupling the
unknown cubic-boundary valuations to the fixed arm (3), for example a
functorial determinant or finality relation crossing from
\(p^{-1}(R)\) to \(D_-\).

## 1. The four forced blowups

Work near the point
\[
 a=0,\qquad b=\infty
\]
of \({\bf P}^1_a\times{\bf P}^1_b\), with \(s=1/b\).  The escaping
dicritical chart gives
\[
 a=-t+\eta t^3,\qquad s=-t^2.
\tag{14}
\]
In particular
\[
 \operatorname {ord}_t a=1,\qquad
 \operatorname {ord}_t s=2.
\]

Blow up the point \(a=s=0\).  In the chart
\[
 s=a s_1,
\]
the branch still passes through
\[
 a=s_1=0.
\]
This is the intersection of the first exceptional divisor with the
strict transform of \(B_\infty=V(s)\).

Blow up that corner and use
\[
 s=a^2r.
\tag{15}
\]
Equation (14) gives
\[
 r\longrightarrow-1.
\]
The point \(r=-1\) is a smooth point of the new exceptional divisor,
away from its two boundary corners.

Set
\[
 q=r+1=\frac{s+a^2}{a^2}.
\tag{16}
\]
Along (14), \(q\) has order two in \(a\).  Blow up the smooth point
\(a=q=0\), writing
\[
 q=a q_2.
\tag{17}
\]
The branch reaches the smooth point \(q_2=0\) of this third
exceptional divisor, away from the preceding divisor.  A fourth
blowup,
\[
 q_2=a q_3,
\tag{18}
\]
finally makes \(q_3\) a free parameter.  Equations (16)--(18) give
\[
 q_3=\frac{s+a^2}{a^4},
\]
which proves the key valuation (5).

Fewer than four ordinary point blowups in a regular model cannot
extract this valuation as a divisor with a nonconstant residue:
after the second blowup the residue \(r=-1\) is fixed, and after the
third the residue \(q_2=0\) is still fixed.  The generic residue
appears for the first time in (18).  This proves minimality in the
stated regular point-blowup category; it is not a claim about weighted
blowups or singular birational models.

## 2. Graph, self-intersections, and canonical labels

Start with \(B_\infty^2=0\).

1. The first blowup changes \(B_\infty^2\) to \(-1\) and creates
   \(E_1^2=-1\).
2. The second blowup is at \(B_\infty\cap E_1\).  It changes both
   self-intersections to \(-2\) and inserts \(E_2^2=-1\).
3. The third blowup is at a smooth point of \(E_2\).  It changes
   \(E_2^2\) to \(-2\) and creates \(E_3^2=-1\).
4. The fourth blowup is at a smooth point of \(E_3\).  It changes
   \(E_3^2\) to \(-2\) and creates \(D_-^2=-1\).

This proves the graph and self-intersection row in (3)--(4).

For the canonical labels, use
\[
 da\wedge db=-s^{-2}da\wedge ds.
\tag{19}
\]
Generic local charts for the five divisors are
\[
\begin{array}{c|cc}
 &a&s\\ \hline
B_\infty&c&t\\
E_1&t&tc\\
E_2&t&t^2c\\
E_3&t&-t^2+t^3c\\
D_-&t&-t^2+t^4c,
\end{array}
\tag{20}
\]
where \(c\) is the coordinate along the displayed divisor.  The
Jacobians
\[
 \operatorname {Jac}_{t,c}(a,s)
\]
have respective \(t\)-orders
\[
 0,\ 1,\ 2,\ 3,\ 4.
\]
Subtracting twice the \(s\)-orders in (20) gives
\[
 \operatorname {ord}(da\wedge db)
 =-2,-1,-2,-1,0,
\]
and hence the second row of (4).

## 3. Pseudoplane valuations along the fixed arm

In \((a,s)\)-coordinates, equations (2) are
\[
 u=a^2,\qquad
 v=4\,\frac{s+a^2}{s^2},\qquad
 w=a\,\frac{s+2a^2}{s}.
\tag{21}
\]
Substitution of the charts (20) gives the last three rows of (4).
The two nonmonomial improvements are exactly:

* on \(E_3\), \(s+a^2\) has order three rather than two;
* on \(D_-\), \(s+a^2\) has order four.

In particular \(v\) has successive orders
\[
 -2,-1,-2,-1,0,
\tag{22}
\]
matching the alternating canonical labels in (4).

On \(D_-\), (21) and (20) give
\[
 v=4\,\frac{a^4q_3}{(-a^2+a^4q_3)^2}
\longrightarrow4q_3,
\]
which proves (6).  Direct substitution of (14) yields (7).

The final canonical label is
\[
 1+\operatorname {ord}_{D_-}(da\wedge db)=1.
\]
This is the compactification form of the already-proved fact that the
distinguished dicritical chart is etale and has Puiseux index one.

## 4. What the fixed arm says about an actual Keller pair

Let
\[
 H=F\circ\pi_2=(H_1,H_2).
\]
Every \(H_i\) is invariant under the deck involution and therefore
extends regularly across \(D_-\).  Its restriction is
\[
 H_i|_{D_-}=A_i(0,v)=A_i(0,4q_3),
\tag{23}
\]
where \(F_i=A_i(u,v)+wC_i(u,v)\).  Hence
\[
 \deg_{q_3}(H_i|_{D_-})=m_i
\tag{24}
\]
is the degree of the distinguished polynomial parametrization of
\(\Gamma\).

The point \(q_3=\infty\) is the intersection \(D_-\cap E_3\).
Resolving the target map there must recover the degree ratio
\[
 \frac{m_1}{m_2}=\frac{\deg H_1}{\deg H_2},
\]
but the arm (3) contains no discriminant-degree label.  The cubic
boundary \(p^{-1}(R)\) is affine-disjoint from \(D_-\), and its
closures can meet this arm only over projective infinity.  Their
valuations of \(u\), their residue square classes in
\({\bf C}(E)\), and their target pole orders are not determined by
(20)--(24).

Thus the local minimality of the \(D_-\)-arm supplies no equation
containing both
\[
 I_\infty(\Gamma,\Delta)
\quad\text{and}\quad
 \deg\Delta.
\]

## 5. Unbounded canonical minimal target trees

Fix \(k\ge2\) and the coprime integers (8).  The homomorphism
\[
 {\bf C}[x,y]/\bigl((y+1)^\delta-x^r\bigr)
 \longrightarrow{\bf C}[t],
\qquad
 x\longmapsto t^\delta,\quad
 y\longmapsto t^r-1
\tag{25}
\]
is the normalization.  Coprimality of \(r,\delta\) implies that its
fraction field is \({\bf C}(t)\), and the polynomial
\((y+1)^\delta-x^r\) is irreducible.

Both parameter derivatives vanish at \(t=0\), so the image has an
affine cusp at \((0,-1)\).  The polynomial parametrization has exactly
one projective end.

Homogenization gives
\[
 (Y+Z)^\delta-X^rZ^k=0.
\tag{26}
\]
On \(\overline\Gamma=V(Y)\), this restricts to
\[
 Z^k(Z^r-X^r).
\tag{27}
\]
The factor \(Z^k\) is the intersection at the common infinity point
\([1:0:0]\), while the other factor supplies \(r\) finite simple
intersections.  This proves (10)--(11).

With \(q=1/t\), local target coordinates at \([1:0:0]\) are
\[
 z=\frac Z X=q^\delta,\qquad
 y_{\rm loc}=\frac Y X=q^k-q^\delta.
\tag{28}
\]
Thus the primitive valuation pair is (12).  Its Euclidean algorithm is
\[
 2k+1=2\cdot k+1,\qquad k=k\cdot1,
\]
giving (13).  The quotient \(k\) is part of the canonical minimal
embedded-resolution data and cannot be removed by contracting a
nonminimal blowup.  As above, \([2,k]\) is the Euclidean/Puiseux
quotient sequence.  Equivalently, the first division contributes two
centers of multiplicity \(k\), and the second contributes \(k\)
centers of multiplicity \(1\).  Therefore the ordinary embedded
resolution with simple-normal-crossings reduced total transform has
multiplicity sequence
\[
 k,\ k,\ \underbrace{1,\ldots,1}_{k\ {\rm times}}
\]
and exactly \(k+2\) point blowups.  For example, \(k=2\) gives
\((2,2,1,1)\) and four blowups, while \(k=3\) gives
\((3,3,1,1,1)\) and five.

Along the affine line \(\Gamma=V(y)\), the simple cubic semilocal
model
\[
 {\bf C}[x,y]\times
 {\bf C}[x,y,\tau]/
 \bigl(\tau^2-((y+1)^\delta-x^r)\bigr)
\tag{29}
\]
has residual discriminant
\[
 4(1-x^r).
\tag{30}
\]
It has \(r\) distinct odd finite places, while its one ramification
component has the minimal infinity type (12).  The componentwise
normal finite cover (29) is the exact semilocal countermodel; it is
not a global Keller normalization.

## 6. Exact conclusion

The explicit pseudoplane chart determines
\[
 \boxed{
 B_\infty-E_2-E_3-D_-
 \quad\text{with the leaf }E_1\text{ at }E_2,
 }
\]
and all labels in (4).  This is useful permanent structure: any
projective resolution of the degree-six plane composite contains a
model dominating this arm.

What it does not determine is equally exact.  The primitive infinity
pair of the cubic branch curve can be
\[
 (k,2k+1)
\]
with arbitrary \(k\), even for a singular polynomially parametrized
one-place curve.  The displayed curve is not a full hypothetical
Keller nonproper set: it supplies no source map or monodromy data.  Its
injective normalization is not, by itself, excluded by the
componentwise form of the Chau results cited in this project.  It is a
countermodel only to deductions from minimal resolution, degree, and
intersection labels.  Therefore those data leave the resolution graph
outside the forced arm unbounded.

The next possible theorem must cross the separation between the two
parts.  A viable statement would have to identify a valuation or
determinant label on a cubic-boundary arm with one of the fixed labels
in (4).  Canonical minimality of the two arms separately does not make
that identification.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_canonical_infinity_tree_flexibility.py
```

for the four blowup charts, graph and self-intersections, canonical
orders, pseudoplane valuations, key-polynomial parameter, exact
dicritical limit, polynomial one-place curve family, finite/infinite
intersection split, residual discriminant, and Euclidean resolution
data.
