# Case-c toric reduction of the missing-end problem

Date: 24 July 2026

## Conclusion

For the full case-c Newton polygons, every branch at source infinity on
which both \(P\) and \(Q\) can remain finite must start in one of exactly
three toric directions:
\[
(-2,1),\qquad(-1,0),\qquad(1,-1).
\tag{1}
\]
The first is the outer Davenport--Zannier face.  It cannot be the start of
a finite asymptotic branch because its two face polynomials are controlled
by coprime polynomials \(U,V\).  The other two directions have exactly one
open-orbit common basepoint each:
\[
\begin{array}{c|c|c}
\text{valuation of }(x,y)&\text{boundary coordinate}&
 \text{common-root multiplicities}\\ \hline
(-1,0)&y=s&(2,3)\\
(1,-1)&z=xy=t&(8,12).
\end{array}
\tag{2}
\]
Thus the toric first step reduces the case-c nonproper-value and
cusp-missing-end problem to the two infinitely-near clusters over
\((y=s)\) and \((z=t)\).  This is a genuine reduction, not an exclusion:
further nonmonomial blowups above either point can still produce a
dicritical component.

## 1. The exact normal-fan calculation

The two polygons are
\[
\begin{aligned}
\Delta_P&=\operatorname {conv}\{(0,0),(1,0),(8,14),(8,16),(0,8)\},\\
\Delta_Q&=\operatorname {conv}\{(0,0),(2,1),(12,21),(12,24),(0,12)\}.
\end{aligned}
\tag{3}
\]
Their primitive inward edge normals are respectively
\[
\begin{aligned}
\mathcal N_P&=\{(0,1),(-2,1),(-1,0),(1,-1),(1,0)\},\\
\mathcal N_Q&=\{(-1,2),(-2,1),(-1,0),(1,-1),(1,0)\}.
\end{aligned}
\tag{4}
\]

Let a branch at infinity have leading valuation
\[
\nu(x)=a,\qquad \nu(y)=b,
\]
with \(a<0\) or \(b<0\).  If the minimum of \(au+bv\) on one support is
negative and is attained at a single required vertex, its nonzero initial
monomial cannot cancel, so that coordinate has a pole.  Therefore every
negative minimum must be attained on an edge.

The origin is the unique minimum of either polygon only in a cone which,
when intersected with an infinity direction, makes the other polygon have
a negative vertex minimum.  Hence a finite-value branch must lie on a
common negative edge-normal ray.  Intersecting (4) and discarding the
nonnegative origin normal \((1,0)\) gives exactly (1).

## 2. The outer ray is impossible

For \(\nu=(-2,1)\), put
\[
w=xy^2,\qquad \nu(w)=0.
\]
The two initial faces are
\[
\operatorname {in}_\nu(P)=xU(w),\qquad
\operatorname {in}_\nu(Q)=x^2yV(w).
\tag{5}
\]
The outer equation is
\[
UV+2wUV'-3wU'V=1.
\tag{6}
\]
It implies \(\gcd(U,V)=1\): a common root would make the left side of
(6) vanish at that root.  Cancellation of both negative pole orders in
(5) would require \(U(w_0)=V(w_0)=0\) at an open-orbit boundary point,
which is impossible.

Thus the outer toric divisor maps to target infinity and cannot itself
start a finite nonproper branch.

## 3. The two surviving basepoints

For \(\nu=(-1,0)\), the common vertical faces are
\[
\begin{aligned}
\operatorname {in}_\nu(P)&=x^8 A(y),&
A(y)&=a\,y^{14}(y-s)^2,\\
\operatorname {in}_\nu(Q)&=x^{12}B(y),&
B(y)&=b\,y^{21}(y-s)^3,
\end{aligned}
\tag{7}
\]
with \(a,b,s\ne0\).  This is the exact square/cube vertical-edge theorem.
The only common zero on the open torus of the divisor is \(y=s\), with
multiplicities \((2,3)\).  The common factor at \(y=0\) is the toric node
leading to the adjacent outer ray, already excluded by (6).

For \(\nu=(1,-1)\), put \(z=xy\).  The forced top faces are
\[
\begin{aligned}
\operatorname {in}_\nu(P)&=a\,y^8(z-t)^8,\\
\operatorname {in}_\nu(Q)&=b\,y^{12}(z-t)^{12},
\end{aligned}
\tag{8}
\]
with \(a,b,t\ne0\).  Their unique open-orbit common zero is \(z=t\), with
multiplicities \((8,12)\).

Equations (7)--(8) identify the two resolution clusters on which the next
argument should focus.  A useful next target is to compute, without
coefficient elimination, the determinant/canonical labels and the
possible target parameter \(\tau=Q/(\sqrt L P)\) along every dicritical
descendant of these two marked basepoints.  Excluding a finite nonzero
\(\tau\)-value on both clusters would prove the radial missing-end lemma.

## Scope

This note does not claim that the two clusters are impossible.  Repeated
cancellation can replace the initial monomial valuation by a nonmonomial
divisorial valuation, precisely the phenomenon that the all-degree
dicritical ledger leaves open.  The result is the finite localization of
that phenomenon to two explicitly marked basepoints.
