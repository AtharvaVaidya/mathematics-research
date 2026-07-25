# The a/b boundary has contact at least four at infinity

Date: 24 July 2026

## Theorem

Use the a/b five-block coordinates
\[
\begin{aligned}
P&=\frac{z^2}{w}+a_0(w)+za_1(w)+z^2a_2(w),\\
Q&=\frac{z^3}{w}+b_0(w)+zb_1(w)+z^2b_2(w)+z^3b_3(w),
\end{aligned}
\]
with
\[
\{P,Q\}_{z,w}=P_zQ_w-P_wQ_z=\frac{z^4}{w^3}.
\]
Assume the four full vertices
\[
[w^8]a_0,\quad [w^6]a_2,\quad
[w^{12}]b_0,\quad [w^9]b_3
\]
are nonzero.  Put
\[
p(w)=a_0(w),\qquad q(w)=b_0(w),
\]
and let \(L\) be the unique constant that cancels the degree-24 term of
\[
D_\partial(w)=q(w)^2-Lp(w)^3.
\]
If \(D_\partial\ne0\), then
\[
\boxed{\deg_wD_\partial\in\{20,16,12,8\}\ \text{or}\quad
\deg_wD_\partial\le7.}
\]
Equivalently, the intersection multiplicity at the common cusp direction
at infinity belongs to
\[
\boxed{\{4,8,12,16\}\ \text{or is at least }17.}
\]
In particular the coefficients of \(w^{23},w^{22},w^{21}\) all vanish.
This is stronger than the proposed cancellation of only the \(w^{23}\)
coefficient, and it uses all five bracket blocks through a single
coordinate-free identity rather than coefficient elimination.

The already-proved cusp-exclusion theorem says \(D_\partial\ne0\) for a
full five-block solution, so the displayed alternatives are the actual
non-cusp spectrum.

## 1. The leading homogeneous root

Give both \(z\) and \(w\) total degree one, allowing Laurent powers of
\(w\).  The largest total degrees of \(P,Q\) are 8 and 12.  Their leading
parts have the support
\[
\begin{aligned}
P_8&=A w^8+Czw^7+Ez^2w^6,\\
Q_{12}&=B w^{12}+Dzw^{11}+Fz^2w^{10}+Gz^3w^9.
\end{aligned}
\]
The degree-18 part of the bracket vanishes:
\[
\{P_8,Q_{12}\}=0.
\]
For homogeneous polynomials of degrees 8 and 12, Euler's identity turns
this into
\[
2P_8\,dQ_{12}-3Q_{12}\,dP_8=0,
\]
so \(Q_{12}^2/P_8^3\) is constant.  Unique factorization gives
\[
P_8=\alpha R^2,\qquad Q_{12}=\beta R^3
\]
for a homogeneous quartic \(R\), with
\[
L=\frac{\beta^2}{\alpha^3}.
\]

The support and the two endpoint conditions \(A,E\ne0\) determine the
shape of \(R\).  Since \(P_8\) has exact \(w\)-valuation six and exact
\(z\)-degree two, \(R\) has exact \(w\)-valuation three and exact
\(z\)-degree one.  Hence
\[
\boxed{R=w^3(uw+vz),\qquad uv\ne0.}
\]
Here \(u\ne0\) follows from \(A\ne0\), and \(v\ne0\) follows from
\(E\ne0\).  The \(Q\)-endpoint conditions are then automatic consequences
of \(Q_{12}=\beta R^3\), but they independently ensure that neither
leading form was lost.  Restricting the two leading forms to \(z=0\)
gives \(A=\alpha u^2\) and \(B=\beta u^3\), so the constant
\(B^2/A^3\) selected from the boundary is indeed
\(\beta^2/\alpha^3\).  Thus the whole degree-24 part of \(D\), not just
its \(z=0\) coefficient, vanishes.

## 2. The centralizer identity

Set
\[
D=Q^2-LP^3.
\]
With the bracket convention above, the exact identity is
\[
\boxed{\{P,D\}=2Q\{P,Q\}=2Q\frac{z^4}{w^3}.}
\]
The right side has total Laurent degree at most
\[
12+(4-3)=13.
\]
The degree-24 part of \(D\) vanishes by the definition of \(L\).  Suppose
that \(d\le23\) is the largest total degree for which \(D_d\ne0\).  If
\(d>7\), the degree-\((d+6)\) part of the left side has no possible match
on the right, and therefore
\[
\{P_8,D_d\}=0.
\]
Since \(P_8=\alpha R^2\) and the Laurent polynomial ring is a domain,
\[
\{R,D_d\}=0.
\]

There is a short homogeneous centralizer lemma.  If a nonzero homogeneous
rational function \(H\) of degree \(d\) satisfies \(\{R,H\}=0\), then
Euler's identity gives
\[
4R\,\mathrm dH-d\,H\,\mathrm dR=0,
\]
where \(\mathrm d\) is the exterior derivative and \(d\) is the integer
degree.  Consequently
\[
\mathrm d\!\left(\frac{H^4}{R^d}\right)=0,\qquad H^4=cR^d.
\]
Taking the valuation along the irreducible linear factor \(uw+vz\) shows
that \(4\mid d\).  In that case unique factorization gives
\[
H=c'R^{d/4}.
\]
Applied to \(H=D_d\), this leaves only
\[
d\in\{20,16,12,8\}
\]
above seven.

## 3. Total degree versus the boundary degree

The argument so far concerns the largest **total Laurent degree** of the
two-variable expression \(D(z,w)\), not automatically the degree of its
restriction to \(z=0\).  This distinction causes no loss here.

If \(d>7\), the preceding section proves
\[
D_d=cR^{d/4}.
\]
Because \(u\ne0\),
\[
D_d(0,w)=c(uw^4)^{d/4}=cu^{d/4}w^d\ne0.
\]
Thus the leading total-degree term survives restriction, and
\[
\deg_wD(0,w)=d.
\]
If the largest total degree is at most seven, restriction can only lower
degree, so \(\deg_wD(0,w)\le7\).  Since
\[
D(0,w)=q(w)^2-Lp(w)^3,
\]
this proves the theorem.

## 4. Direct view of the \(w^{23}\) cancellation

The next homogeneous bracket equation is
\[
\{P_8,Q_{11}\}+\{P_7,Q_{12}\}=0.
\]
Substituting \(P_8=\alpha R^2,Q_{12}=\beta R^3\) gives
\[
\left\{R,\,2\alpha Q_{11}-3\beta RP_7\right\}=0.
\]
The expression in the second slot is homogeneous of degree 11.  The
centralizer lemma has no nonzero degree-11 solution, so
\[
2\alpha Q_{11}=3\beta RP_7.
\]
The degree-23 part of \(Q^2-LP^3\) is consequently
\[
\begin{aligned}
D_{23}
&=2Q_{12}Q_{11}-3LP_8^2P_7\\
&=\frac{\beta R^3}{\alpha}
  \left(2\alpha Q_{11}-3\beta RP_7\right)=0.
\end{aligned}
\]
This makes explicit where blocks two through five enter: together with
the first block they are precisely the coefficients of the homogeneous
equation above.

## 5. Verification

Run
```bash
PYTHONPATH=/tmp/codex-mathdeps.IyweI7 \
python3 route_bd_ab_contact_spectrum.py
```
The verifier checks the bracket convention, the leading and next-layer
identities, the exact degree ledger, and the homogeneous centralizer
kernels in every degree from 8 through 23.
