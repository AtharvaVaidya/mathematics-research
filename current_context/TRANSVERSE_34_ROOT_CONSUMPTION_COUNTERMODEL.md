# Why polar-root consumption does not extend beyond transverse degree two

Date: 25 July 2026

## Result

The completed-square multiplicity theorem for transverse degrees \((2,3)\)
has a clean conditional \((m,m+1)\) analogue, but it does not hold for a
general radial block once \(m>2\).

Already for transverse degrees \((3,4)\), there is a genuine local analytic
family
\[
P=\sum_{i=0}^3p_i(h)z^i,\qquad
Q=\sum_{j=0}^4q_j(h)z^j
\]
with
\[
\{P,Q\}_{z,h}=z^6,
\]
such that
\[
p_2(0)=0,\qquad p_2'(0)\ne0,\qquad p_0'(0)=1.
\]
Thus a simple zero of the first polar coefficient \(p_{m-1}\) need not
consume even one zero of the boundary derivative.

The obstruction at \((2,3)\) is special because completing the square
removes the only intermediate transverse coefficient.

## 1. Conditional pure-Tschirnhaus theorem

Suppose \(n=m+1\) and a local source change puts the block in the much
smaller stratum
\[
P=\zeta^m+H(h),
\]
with boundary \(z=0\) given by \(\zeta=s(h)\).  Suppose
\[
\{P,Q\}_{\zeta,h}=u(h)(\zeta-s(h))^{2m},\qquad u(0)\ne0,
\]
and write
\[
Q=\sum_{j=0}^{m+1}q_j(h)\zeta^j.
\]
Three exact coefficient rows are
\[
\begin{aligned}
-H'q_1&=u(-s)^{2m},\\
m q_1'-(m+1)H'q_{m+1}
 &=u\binom{2m}{m}(-s)^m,\\
m q_{m+1}'&=u.
\end{aligned}
\tag{1}
\]

Put
\[
r=\operatorname{ord}_0s,\qquad b=\operatorname{ord}_0H'.
\]
The last row says \(q_{m+1}\) is either a unit or has a simple zero.
If \(q_1\) has positive order, valuation comparison in the first two
rows excludes \(b<mr-1\).  The only constant-\(q_1\) resonance has
\(b=2mr\).  Consequently
\[
\operatorname{ord}_0H'\ge mr-1.
\]
Since the boundary restriction is \(H+s^m\),
\[
\boxed{
\operatorname{ord}_0\frac d{dh}(H+s^m)\ge mr-1.
}
\tag{2}
\]
For \(m=2\), this is exactly the bound \(2r-1\) used in the all-scale
marked-cusp theorem.

## 2. The surviving intermediate coefficient

For \(m>2\), a Tschirnhaus shift removes the \(\zeta^{m-1}\) term but
leaves
\[
c_{m-2}\zeta^{m-2}+\cdots+c_1\zeta.
\]
These terms enter \(P_\zeta\) in the coefficient rows used in (1).
In particular \(c_1\) may be a unit at a zero of the first polar
coefficient.  There is then no reason for \(P_\zeta\) or the boundary
derivative to vanish.

The following example shows that this is an actual solution phenomenon,
not merely a missing step in the valuation proof.

## 3. Exact \((3,4)\) initial data

At \(h=0\), take
\[
\begin{aligned}
P&=z^3+2z,\\
Q&=-2z^4-3z^3+2z^2-3z-3,
\end{aligned}
\]
and prescribe
\[
\begin{aligned}
P_h={}&\frac18z^3+\frac{5361}{3622}z^2
       +\frac{305}{7244}z+1,\\
Q_h={}&-\frac{62617}{14488}z^3-\frac{7943}{1811}z^2
       +\frac{28061}{14488}z-\frac32.
\end{aligned}
\]
Direct calculation gives
\[
\boxed{P_zQ_h-P_hQ_z=z^6.} \tag{3}
\]
In particular,
\[
p_2(0)=0,\qquad
p_2'(0)=\frac{5361}{3622}\ne0,\qquad
p_0'(0)=1.
\]
Both leading coefficients \(p_3(0)=1\) and \(q_4(0)=-2\) are units.

## 4. Why this integrates to a local family

Regard the four \(p_i\) and five \(q_j\) as analytic functions of \(h\).
The seven coefficient conditions
\[
[z^0]\{P,Q\}=\cdots=[z^5]\{P,Q\}=0,\qquad
[z^6]\{P,Q\}=1
\]
are linear in the nine coefficient derivatives.  Add the harmless gauges
\[
p_0'=1,\qquad q_4'=0.
\]
At the displayed initial point, the resulting \(9\times9\) derivative
matrix has determinant
\[
\boxed{-28976\ne0.}
\]
It therefore defines a rational analytic vector field in a neighborhood
of the point.  The local existence theorem for ordinary differential
equations produces analytic coefficient functions satisfying
\(\{P,Q\}=z^6\) identically.  Since \(p_2'(0)\ne0\), its polar zero remains
simple.

## 5. Strategic conclusion

The root-consumption mechanism gives a real all-\(m\) theorem only on the
pure stratum \(P=\zeta^m+H\).  A general \((m,m+1)\) radial block does not
lie on that stratum, and the first omitted coefficient already supplies
a local countermodel at \((3,4)\).

Therefore an infinite-corner Jacobian obstruction cannot follow from a
zero of the first polar deformation alone.  It would first need a global
argument forcing all lower Tschirnhaus coefficients to vanish, or a
different invariant that controls them simultaneously.

## 6. Audit against minimal-counterexample and Newton-corner reductions

The known reduction used in this project does **not** supply that missing
global argument.  Proposition 4.3 of Guccione--Guccione--Horruitiner--Valqui
reduces a hypothetical minimal survivor to full two-dimensional Newton
polygons.  It fixes their vertices and outer faces, but retains 61
\(P\)-coefficients and 125 \(Q\)-coefficients in case c (25 and 47 in
cases a/b).  The interior and lower coefficients are variables of the
reduced Keller system, not coefficients known to vanish.

Likewise, the outer formal normalization
\[
P_{\rm out}=u_p\zeta^m\sigma^{-mk},\qquad
Q_{\rm out}=v_q\zeta^n\sigma^{-nk}(1-\sigma^N)^{1/m}
\]
normalizes the outer face only.  At radial deficit \(d\), the allowed
\(P\)-coefficient interval is
\[
\begin{cases}
[0,mk+d],&d<m,\\
[1,m(k+1)],&d=m,\\
[d-m,m(k+1)],&d>m,
\end{cases}
\]
with the analogous \(Q\)-interval.  These nonempty transformed lattices
are precisely the lower extension data.  Replacing them by their
associated graded is known to give the wrong kernel dimensions, so outer
purity cannot be propagated inward by a filtration argument.

There is also a simple coordinate-count explanation.  A translation in
the transverse variable removes the single \(\zeta^{m-1}\) coefficient.
After that normalization, the coefficients of
\(\zeta^{m-2},\ldots,\zeta\) are genuine moduli; the Newton vertex and
common-leading-root conditions do not provide another \(m-2\) source
gauges.  The exact \((3,4)\) family above realizes the first such modulus
as the unit term \(2z\), while keeping unit leading coefficients and the
full constant-bracket identity.

Thus no presently verified minimal-counterexample, leading-corner, or
outer-normal-form hypothesis restores the pure stratum
\(P=\zeta^m+H\).  Proving that purity from the complete global Keller
system would be a new theorem, not a consequence of the known Newton
reductions.  The polar-root-consumption route should therefore stop at
\((2,3)\) unless a genuinely new global invariant controls all
intermediate coefficients simultaneously.

Run:

```bash
.venv/bin/python route_bd_transverse_34_local_countermodel.py
```
