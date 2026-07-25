# Shear-correct global audit of the five \(\delta=1\) cells

Date: 24 July 2026

## 1. Safe result

The exhaustive pole-sensitive Puiseux analysis left five cells.  After
imposing the global generalized-Weierstrass remainder condition with the
linear target shear retained, all five die in characteristic zero:

| Cell | Global outcome |
|---|---|
| \((m,n)=(7,11)\) | empty |
| \((m,n)=(5,8)\) | empty |
| analytic-quadratic \((m,N)=(4,14)\) | every point is composite |
| analytic-quadratic \((m,N)=(3,10)\) | saturated cell is empty |
| \((m,n)=(3,5)\) | empty by the exact Wronskian/radical obstruction |

For the final \((3,5)\) cell, retaining the degree-twelve approximate
root gives an exact characteristic-zero proof.  If
\(D=T^2-A^3\) has degree at most eight, then
\[
T(2AT'-3A'T)=AD'-3A'D
\]
forces \(\deg(2AT'-3A'T)\le3\).  The resulting triangular Wronskian
system has exact radical forcing the order-five coefficient to vanish.
See `AB_DELTA1_35_WRONSKIAN_OBSTRUCTION.md`.

Thus the rigorous current conclusion is
\[
\boxed{\text{all five primitive }\delta=1\text{ cells are empty}.}
\]

## 2. Why the linear shear is essential

The general osculating cubic contains \(XY\), \(Y\), and \(X^2\) terms.
Completing the square replaces the original boundary coordinate by
\[
\widetilde B=B+\ell A+\text{constant}.
\]
The high-degree approximate-root calculation belongs to
\((A,\widetilde B)\), but the pole-sensitive Puiseux cell belongs to the
original \((A,B)\).  Removing \(\ell\) by an affine target shear would
transfer the pole of \(p_2\) into \(q_2\), so it is not legitimate in the
local five-block argument.

The global calculation therefore keeps
\[
B=\widetilde B-\ell A-\text{constant}.
\]
At a horizontal cell with
\[
\operatorname{ord}_0(A-A(0))=m,
\]
the condition \(\operatorname{ord}_0(B-B(0))>m\) determines
\[
\ell=[h^m]\widetilde B
\]
after normalizing \([h^m]A=1\).  This eliminates the shear exactly
without setting it to zero.

The source coordinate is translated only to put the marked point at
\(h=0\).  The coefficient \([h^7]A\) is retained.  A source scaling,
combined with the target scaling that preserves monic leading terms,
normalizes the nonzero local coefficient \([h^m]A\) to one.

## 3. Triangular approximate-root system

Write
\[
A=h^8+\sum_{i=0}^7a_i h^i,\qquad
\widetilde B=h^{12}+\sum_{i=0}^{11}b_i h^i.
\]
The coefficients of degrees \(23,\ldots,12\) in
\[
D=\widetilde B^2-A^3
\]
uniquely determine \(b_{11},\ldots,b_0\) as polynomials in the \(a_i\).
The generalized-Weierstrass remainder has degree at most seven precisely
when
\[
[h^{11}]D=[h^{10}]D=[h^9]D=0;
\]
the \(h^8\) coefficient is canceled by the linear \(uA\) term.

All systems below are formed only after this triangular reduction.

## 4. Exact per-cell outcomes

### The \((7,11)\) and \((5,8)\) cells

Set
\[
a_1=\cdots=a_{m-1}=0,\qquad a_m=1,
\]
put
\[
\ell=[h^m]\widetilde B,
\qquad B=\widetilde B-\ell A,
\]
and impose
\[
[h^j]B=0\quad(1\le j<n)
\]
together with the three remainder equations.

For both \((m,n)=(7,11)\) and \((5,8)\), the exact rational ideal is the
unit ideal.  These closures are empty even before saturation by the
required nonzero \(h^n\) coefficient.

### The analytic-quadratic \((4,14)\) cell

Put
\[
x=A-A(0),
\]
and impose
\[
\widetilde B-\widetilde B(0)-\ell x-c_2x^2-c_3x^3
=O(h^{14}).
\]
The exact radical of this system is
\[
\left\langle
a_5,a_6,a_7,\,
2c_2+c_3-1,\,
12a_0+8c_2-9
\right\rangle.
\]
Hence
\[
A=h^8+h^4+a_0\in\mathbf C[h^4],
\]
and the triangular formula puts \(\widetilde B\) in
\(\mathbf C[h^4]\) as well.  Every point is a degree-four composition,
so the primitive boundary cell is empty.

### The analytic-quadratic \((3,10)\) cell

The same construction with \(m=3\) and contact ten has radical
\[
\begin{aligned}
\langle\;&a_5,\ a_7^2-4a_6,\
a_6a_7-4a_6c_2+3a_5-2c_3,\\
&a_4a_7-2,\ 2a_4a_6-a_7,\\
&24a_0a_6c_2-18a_0a_5-3a_5^2+3a_4a_6
+12a_0c_3-6a_7+8c_2\;\rangle.
\end{aligned}
\]
The coefficient of \(h^{10}\) in the transverse remainder reduces to
zero modulo this radical.  Thus every point in the contact-\(\ge10\)
closure actually has contact \(>10\).  Saturating by the required
nonzero \(h^{10}\) coefficient gives the unit ideal:
\[
\boxed{(3,10)\text{ is empty}.}
\]

## 5. The final \((3,5)\) system

Set
\[
A=h^8+a_7h^7+a_6h^6+a_5h^5+a_4h^4+h^3+a_0.
\]
Let \(\widetilde B\) be the unique triangular approximate root and put
\[
\ell=[h^3]\widetilde B,\qquad B=\widetilde B-\ell A.
\]
The exact closure ideal has six generators:
\[
[h]B,\quad[h^2]B,\quad[h^4]B,\quad
[h^{11}]D,\quad[h^{10}]D,\quad[h^9]D.
\]
The actual cell is the saturation by
\[
L=[h^5]B\ne0.
\]
This is now a completely explicit system in the five variables
\[
a_0,a_4,a_5,a_6,a_7.
\]

Over \(\mathbf F_{32003}\), adjoining \(sL-1\) gives the unit ideal.
The direct dense characteristic-zero saturation did not finish within
the original bounded calculation.  The later Wronskian reformulation
proves the same vanishing over \(\mathbf Q\) by an exact primary
decomposition in coordinates adapted to its unique minimal component.

The modular Nullstellensatz lift was also measured during discovery.  A
direct unit certificate has seven multipliers with degrees
\[
(19,20,20,17,16,15,18)
\]
and respective monomial counts
\[
(3582,4189,4382,2482,1982,1560,3499),
\]
for \(21676\) monomials in total.  A smaller certificate proves
\(L\) itself belongs to the unsaturated ideal modulo \(32003\).  Its six
multipliers have degrees
\[
(16,17,17,14,13,12)
\]
and monomial counts
\[
(412,499,438,282,230,176),
\]
for \(2037\) monomials in total.  Although its support was identical
across the tested primes, a later syzygy audit found a 397-dimensional
ambiguity in the raw multiplier space.  Coefficientwise CRT of those raw
lifts is therefore not valid.  The corrected reconstruction script first
reduces modulo the full syzygy module; it is retained only as an
independent check because the Wronskian proof no longer needs a large
certificate.

## 6. Exact resolution

The exact proof is in
`AB_DELTA1_35_WRONSKIAN_OBSTRUCTION.md` and
`route_bd_ab_delta1_35_wronskian.py`.  It checks the empty \(a_7=0\)
chart and, on \(a_7\ne0\), makes an invertible coordinate change in which
the exact radical is
\[
(z,y,x,v,r,ut-1).
\]
This gives \(a_5=0\), \(a_7^2=4a_6\), \(a_4a_7=2\), and finally
\([h^5]B=0\).  Saturation by the required nonzero coefficient is empty.
