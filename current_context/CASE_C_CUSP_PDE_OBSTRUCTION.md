# The cusp-compatible case-c stratum is empty

Date: 24 July 2026

Assume the complete case-c Newton polygons, with every actual polygon
vertex nonzero, and suppose the critical line is contained in one fixed
target cusp.  The Rees calculation then gives
\[
 P(0,y)=Ay^8,\qquad Q(0,y)=By^{12},\qquad B^2=LA^3,
\]
with \(A,B,L\ne0\), and
\[
 Q^2-LP^3=x^3S.
\]
Write
\[
 P=\sum_{i\ge0}x^ip_i(y),\qquad
 Q=\sum_{i\ge0}x^iq_i(y).
\]

The coefficient of \(x\) in \(Q^2-LP^3\) is zero, hence
\[
 2By^{12}q_1-3LA^2y^{16}p_1=0
\]
and therefore
\[
 q_1=\frac{3B}{2A}y^4p_1.
\]
The coefficient of \(x^2\) is also zero.  Substitution gives
\[
q_2=\frac{3B}{2A}y^4p_2+
      \frac{3B}{8A^2}\frac{p_1^2}{y^4}.
\]
Equivalently, without using Laurent notation,
\[
 8A^2y^4q_2=12ABy^8p_2+3Bp_1^2.
\]
The left side and the first term on the right are divisible by \(y^4\).
Since the characteristic is zero and \(B\ne0\), this forces
\(y^4\mid p_1^2\), hence
\[
y^2\mid p_1.
\]

But \((1,0)\) is a required nonzero vertex of the case-c Newton polygon.
Its coefficient is exactly \(p_1(0)\), whereas the divisibility above
forces \(p_1(0)=0\).  This is a contradiction.

There is an even more local certificate.  Put \(c=p_1(0)\).  The
case-c support has \(p_2\in y^2K[y]\) and \(q_2\in yK[y]\), so the
coefficient of \(x^2y^8\) in the cusp equation is
\[
 [x^2y^8](Q^2-LP^3)
   =-\frac{3B^2}{4A^2}c^2.
\]
Over characteristic zero it cannot vanish when the three full-vertex
coefficients \(A,B,c\) are nonzero.

Thus the fixed-cusp containment needed by the proposed finite-etale Rees
route is not merely restrictive: it is incompatible with the complete
case-c Newton polygon.  This eliminates the cusp-compatible stratum, but
does **not** by itself eliminate case c; a hypothetical case-c Keller pair
must instead map its critical line outside every fixed cusp
\(q^2=Lp^3\).

The exact symbolic check is
`route_bd_case_c_cusp_pde_obstruction.py`.
