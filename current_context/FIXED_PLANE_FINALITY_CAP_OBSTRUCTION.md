# A defect obstruction to capping final point curves

Date: 25 July 2026

This note sharpens the remaining failure in
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`.  It proves that the
19-vertex effective-\(G\) ledger cannot be repaired by **any exceptional
cluster supported over its positive-label final curve \(E_{12}\)**, nor
by a cluster supported over either boundary crossing on \(E_{12}\),
while retaining the old intersection ledger.

This is not a proof for every compactification tree: an enlarged tree
whose global solution changes the old \(b,\eta\) coefficients remains
possible.

## 1. The boundary defect

Retain the smooth-\(\Gamma\), reduced-pullback, and separated-contact
hypotheses of the global pullback memo.  Thus
\[
Qb=y,\qquad Q\eta+z=d\,y,
\tag{1}
\]
where \(z\ge0\) records the intersections of the strict affine part of
\(\phi^*\overline\Gamma\) with the boundary.

Define the integral defect vector
\[
\boxed{\qquad \sigma=d\,b-\eta.\qquad}
\tag{2}
\]
Subtracting the two equations in (1) gives the exact identity
\[
\boxed{\qquad Q\sigma=z.\qquad}
\tag{3}
\]

At a dicritical curve \(\eta_i=0\).  Hence
\[
\begin{array}{c|c}
\text{final type}&\sigma_i\\ \hline
\text{type 3}&0,\\
\text{type 1 of pullback multiplicity }m&dm.
\end{array}
\tag{4}
\]
This couples finality directly to the effective divisor \(G\); neither
\(Qb=y\) nor \(Q\eta+z=dy\) alone sees (4).

## 2. Exact pendant-chain formula

Let \(E_0\) be an old boundary curve and attach a chain
\[
E_0-E_1-\cdots-E_\ell
\tag{5}
\]
by successive generic blowups.  Thus the new internal curves have
self-intersection \(-2\), while \(E_\ell^2=-1\).  Suppose no branching or
crossing blowup is subsequently made on this chain.  Write
\[
z_i=E_i\cdot\left(C+\sum_jH_j\right)\ge0
\qquad(1\le i\le\ell).
\]

The cap rows of (3) are
\[
\begin{aligned}
\sigma_{i-1}-2\sigma_i+\sigma_{i+1}&=z_i
&& (1\le i<\ell),\\
\sigma_{\ell-1}-\sigma_\ell&=z_\ell.
\end{aligned}
\tag{6}
\]
If \(\Delta_i=\sigma_i-\sigma_{i-1}\), then
\[
\Delta_{i+1}-\Delta_i=z_i,\qquad
\Delta_\ell=-z_\ell.
\]
Backward summation gives the exact moment identity
\[
\boxed{\qquad
\sigma_0=\sigma_\ell+\sum_{i=1}^{\ell}i\,z_i.
\qquad}
\tag{7}
\]
In particular,
\[
\begin{array}{ll}
\text{final type 3:}&\sigma_0=\sum i z_i\ge0,\\[1mm]
\text{final type 1 of multiplicity }m:
&\sigma_0=dm+\sum i z_i\ge dm.
\end{array}
\tag{8}
\]

There is an identical formula for the pullback line:
\[
\boxed{\qquad
b_0=b_\ell+\sum_{i=1}^{\ell}i\,y_i.
\qquad}
\tag{9}
\]
Thus a type-\(3\) cap consumes positive line degree from its attachment,
and a type-\(1\) cap has \(b_0>b_\ell\).

No assumption that the cap avoids the strict affine pullback is used:
the nonnegative \(z_i\) in (7) allow affine branches to enter the cap.
If the cap is disjoint from them, all \(z_i=0\) and the defect is
constant along the chain.

## 3. The arbitrary-cluster negativity lemma

The chain formula is a special case of a negativity statement.  Let
\(T\) be any connected exceptional cluster produced by point blowups
over either

1. a smooth point of one old boundary component, or
2. a crossing of two old boundary components.

Let \(Q_T\) be the intersection matrix of the new exceptional curves,
and let \(V\) be their incidence matrix with the strict transforms of
the old boundary components through the center.  The cap rows of (3)
are
\[
Q_T\sigma_T+V\sigma_{\rm old}=z_T.
\tag{10}
\]
The exceptional intersection form is negative definite.  Moreover
\[
A:=-Q_T
\]
is an irreducible nonsingular \(M\)-matrix: its diagonal is positive,
its off-diagonal entries are nonpositive, and
\[
A^{-1}>0
\tag{11}
\]
entrywise.  Indeed, negative definiteness of \(Q_T\) makes \(A\) a
positive-definite \(Z\)-matrix, hence a nonsingular \(M\)-matrix.  The
connectedness of the exceptional dual graph makes it irreducible; after
writing \(A=sI-N\), with \(N\ge0\) irreducible and
\(s>\rho(N)\), the convergent Neumann series for \(A^{-1}\) is
entrywise strictly positive.  Equation (10) becomes
\[
\sigma_T=A^{-1}V\sigma_{\rm old}-A^{-1}z_T.
\tag{12}
\]

Assume every augmented-canonical label created in the cluster is
positive.  Every final exceptional curve in the cluster can then be
dicritical only as type \(3\).  Keller finality and (4) force
\[
\sigma_f=0
\tag{13}
\]
for every such final curve \(f\).  Taking the \(f\)-row of (12) gives
\[
\sum_p(A^{-1}V)_{fp}\sigma_p
=\sum_j(A^{-1})_{fj}z_j\ge0.
\tag{14}
\]
Every attachment weight on the left is positive.  Consequently:
\[
\boxed{\text{if all old boundary defects at the center are negative,
no positive-label final cap exists.}}
\tag{15}
\]
This allows arbitrary generic blowups, crossing blowups, and branching
inside the cluster.  Strict affine pullback branches cause no problem:
they only contribute the nonnegative vector \(z_T\).

## 4. Application to the 19-vertex ledger

For the degree-nine ledger, the six final point-mapping curves have:
\[
\begin{array}{c|rrrrrr}
i&10&11&12&15&17&18\\ \hline
a_i&-5&-1&2&-1&-1&0\\
b_i&7&3&24&16&3&12\\
\eta_i&48&21&221&138&21&105\\
\sigma_i=9b_i-\eta_i&15&6&-5&6&6&3.
\end{array}
\tag{16}
\]

The decisive entry is
\[
\boxed{\sigma_{12}=-5.}
\tag{17}
\]
The first blowup at a smooth point of \(E_{12}\) creates label \(3\).
Every subsequent generic or crossing blowup inside that cluster again
creates a positive label.  The one-attachment case of (15), together
with (17), therefore rules out the entire cluster.

There are two crossing alternatives for the first blowup on \(E_{12}\).
Its neighbors are \(E_3,E_4\), and
\[
\sigma_3=9\cdot8-74=-2,\qquad
\sigma_4=9\cdot16-147=-3.
\tag{18}
\]
At either crossing, both old attachment defects are negative.  The
first exceptional has augmented-canonical label
\[
a_{12}+a_j=3,
\]
and every label subsequently created inside the cluster is positive.
The two-attachment case of (15) excludes both clusters, even if strict
affine components pass through the chosen crossing.

Thus all three possible first centers on \(E_{12}\)—a generic point or
either boundary crossing—are obstructed for arbitrary further blowups
supported over that center:
\[
\boxed{\text{\(E_{12}\) cannot be capped while the 19 old
\(b,\eta\) coefficients are retained.}}
\tag{19}
\]

## 5. Geometric no-repair lemma

There is a separate, more elementary reason that post hoc blowups cannot
repair finality in an actual resolved morphism.  If
\[
\rho:X'\to X
\]
is any further sequence of point blowups after \(\phi:X\to\mathbf P^2\)
is already a morphism, then every \(\rho\)-exceptional curve is collapsed
by \(\rho\) to a source point.  The composite
\[
\phi\circ\rho
\]
therefore maps it to a target point, so it has \(y=0\) and is neither
type \(1\) nor type \(3\).

The numerical recurrences say the same thing.  At a generic blowup of a
point-mapping curve, nonnegativity of the old and new \(Qb\)-rows forces
\[
b_{\rm new}=b_{\rm parent},\qquad
y_{\rm new}=y_{\rm parent}=0.
\tag{20}
\]
At the crossing of two point-mapping curves it forces
\[
b_{\rm new}=b_i+b_j,\qquad y_{\rm new}=0.
\tag{21}
\]

Thus the 19-vertex ledger cannot be turned into a valid resolution by
simply blowing up its six bad final curves after the putative morphism
has been constructed.  A valid competing tree must change the
pre-resolution base-point structure and hence change the old \(b,y,\eta\)
data.  This sharply limits what a future search is allowed to call a
“cap repair.”

## 6. Remaining scope

The argument does not yet exclude:

1. a different global solution on an enlarged tree in which the old
   19 coefficients change;
2. a repair that connects the \(E_{12}\) cluster to additional old
   boundary components having nonnegative defect; or
3. a different tree in which the positive-label final obstruction occurs
   at another place.

The next useful target is therefore to propagate the defect inequality
(14) through the entire point-mapping subtree, rather than to attach
more local caps to the fixed ledger.  The exact defect ledger and the
cap recurrences are checked in
`verify_fixed_plane_finality_cap_obstruction.py`.
