# Local resolution of the two case-c finite clusters

Date: 24 July 2026

## Exact local models

The normal-fan reduction leaves two finite clusters.  After extracting
units, their projective monomial models are
\[
[P:Q:1]=[u^4r^2:r^3:u^{12}]
\tag{1}
\]
for the initial \((2,3)\) cluster, and
\[
[P:Q:1]=[u^4r^8:r^{12}:u^{12}]
\tag{2}
\]
for the initial \((8,12)\) cluster.

For (1), principalization uses four successive point blowups with primitive
valuation rays
\[
(1,1),(1,2),(1,3),(1,4).
\]
The last exceptional divisor is the unique finite dicritical and maps by
\[
c\longmapsto(c^2,c^3).
\tag{3}
\]

For (2), one ordinary blowup with ray \((1,1)\) principalizes the map.  Its
exceptional divisor is the unique finite dicritical and maps by
\[
c\longmapsto(c^8,c^{12})=(s^2,s^3),\qquad s=c^4.
\tag{4}
\]
It therefore has degree four onto the same cuspidal image.

## Canonical labels and the negative result

The reduced Jacobian equation uses the pulled-back Keller volume
\[
\Omega=x^2\,dx\wedge dy.
\]
For the local monomial coordinates used above, the augmented-canonical
label is the corresponding order of \(\Omega\) plus one.  Along the two
cancellation chains the labels are
\[
(-2,-1,0,1),\qquad(3).
\]
Thus the finite dicriticals have positive labels \(1\) and \(3\).  This is
compatible with, rather than contradictory to, the expected positive
ramification on components mapping to affine curves.

A minimal toric completion gives provisional negative determinant labels
on both finite arms.  Those signs also satisfy the local
ample-ramification requirement.  They are **not** invariants of the
complete original boundary tree: restoring the Laurent edge-cutting arms
and the target-infinity descendants changes the cofactors of the
intersection matrix.  See `GGHV_TRANSFER_CHAIN_AUDIT.md`.

Hence the two finite arms alone yield no discrepancy, determinant, or
one-point-at-infinity contradiction.  The outer face condition
\(\gcd(U,V)=1\) only excludes a finite asymptotic branch on that face.
It does not exclude horizontal descendants mapping to target infinity;
such omitted components can alter every global determinant computation.

The remaining global target is a transport-and-incidence theorem for the
complete boundary tree, not a further local blowup of (1) or (2).
