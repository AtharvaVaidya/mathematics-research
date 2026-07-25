# The five-block fourth-jet discriminant

Date: 25 July 2026

## Result

Let
\[
A=A(h),\qquad B=B(h)
\]
be the boundary restriction of a genuine five-block radial solution, and
write derivatives with respect to \(h\).  Define
\[
\begin{aligned}
J&=A'B''-B'A'',\\
K&=A'J'-3A''J,\\
L&=A'K'-5A''K,\\
\Phi&=3K^2-JL.
\end{aligned}
\]
Then
\[
\boxed{\Phi\text{ is a square in }\mathbf C[h].}
\]

This condition is strictly stronger than the depressed-Wronskian degree
bound.  The exact primitive scale-five pair in
`UNIVERSAL_WRONSKIAN_COUNTERMODEL.md` satisfies every Wronskian and marked
\((3,5)\) condition but its \(\Phi\) is not a square.  Thus it cannot
extend to the original five-block system.

## Derivation

On a graph branch \(B=g(A)\), the first four transverse Taylor identities
include
\[
0=\frac12g''p_2^2
  \frac12g'''p_1^2p_2
  \frac1{24}g''''p_1^4.
\]
The fixed \(w^{-1}\) term makes \(p_2\) a nonzero rational function.  Put
\[
C=\frac{p_1^2}{p_2}.
\]
After division by \(p_2^2/24\),
\[
g''''C^2+12g'''C+12g''=0. \tag{1}
\]
The discriminant of (1) is
\[
48\bigl(3(g''')^2-g''g''''\bigr).
\]
Direct differentiation with \(d/dA=(A')^{-1}d/dh\) gives
\[
g''=\frac{J}{(A')^3},\qquad
g'''=\frac{K}{(A')^5},\qquad
g''''=\frac{L}{(A')^7}.
\]
Consequently the discriminant is
\[
\frac{48\Phi}{(A')^{10}}.
\]
Because (1) has the rational root \(C\), its discriminant is a square in
\(\mathbf C(h)\).  The denominator and the constant \(48\) are squares
over \(\mathbf C\), so \(\Phi\) is a square in \(\mathbf C(h)\).
A polynomial which is a rational-function square has even valuation at
every irreducible factor and is therefore a polynomial square.

No division chart is omitted: the identity
\[
(2g''''C+12g''')^2
=\operatorname{disc}(1)+4g''''\,
 (g''''C^2+12g'''C+12g'')
\]
also proves the square statement when \(g''''=0\).

## Exact all-scale degree

Complete and depress the osculating cubic, and normalize
\[
\deg A=2r,\qquad \deg B=3r,\qquad
D=B^2-A^3,\qquad \deg D=d\le2r.
\]
If \(D\ne0\), then
\[
\boxed{\deg\Phi=d+8r-10.} \tag{2}
\]
More precisely, with \(M=2r\) and \(\delta=\operatorname{lc}(D)\), the
leading coefficient is
\[
-\frac{3M^6\delta}{32}
(d-3M)(d-2M)(2d-5M)(2d-3M).
\]
None of these factors vanishes for \(0\le d\le M\).  Formula (2) follows
by taking the first Laurent variation away from the exact branch
\(B=A^{3/2}\), on which \(\Phi\) vanishes identically.

The first universal consequence is the parity obstruction
\[
\boxed{d\text{ must be even}.}
\]
This is not yet an all-scale contradiction: the generic depressed
remainder has \(d=2r\), which already has the required parity.

For the pole-sensitive nonintegral marked cells
\[
2n=3m+1,\qquad m\ \text{odd},
\]
the marked point contributes the even order
\[
\operatorname{ord}_0\Phi=4m+2n-10=7m-9.
\]
Thus local parity is exactly compatible.  A proof must use the remaining
global zeros of \(\Phi\), not only its total degree and marked order.

## Scale-five falsification

At the explicit simple point modulo \(32003\) underlying the scale-five
Hensel lift,
\[
\deg\Phi=40
\]
and its factor degrees and multiplicities are
\[
(1,12),\quad(2,1),\quad(4,1),\quad(5,1),\quad(17,1).
\]
The four non-monomial factors occur to odd multiplicity, so \(\Phi\) is
not a square even over the algebraic closure of the residue field.  This
open squarefree defect persists on the characteristic-zero Hensel lift.

Hence:

> The Wronskian-only countermodel is not a five-block countermodel.
> The fourth-jet discriminant detects the missing pole-sensitive
> structure without expanding the lower coefficient system.

## Strategic use

The next structural problem is the divisor classification
\[
\operatorname{div}(\Phi)=2E
\]
together with the outer equation
\[
UV+2hUV'-3hU'V=1.
\]
Since \(p_2=U/h\), the rational root in (1) has the special form
\[
C=\frac{h\,p_1^2}{U}.
\]
Thus the square root of \(\Phi\) is not arbitrary: its two rational
branches must contain one whose denominator and numerator divisors match
the fixed outer polynomial \(U\) and the square \(p_1^2\).  This is the
promising all-scale coupling.  Degree parity alone is insufficient.

Run:

```bash
.venv/bin/python route_bd_fiveblock_discriminant_square.py
```
