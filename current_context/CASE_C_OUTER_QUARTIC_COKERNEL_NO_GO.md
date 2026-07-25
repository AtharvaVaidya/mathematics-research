# Case c: the raw outer-quartic remainder is not a cokernel invariant

Date: 25 July 2026

## Audited conclusion

At the first two case-c radial cokernels, ordinary reduction modulo the
outer quartic \(E\), or its square \(E^2\), does not descend through the
cokernel.  The new-block operator is in fact surjective after these
reductions on each of the two rational and one cubic factors of the
certified outer Hurwitz algebra modulo \(32003\).

Thus the two canonical cokernel rows cannot be identified with raw
remainders modulo \(E\) or \(E^2\).  Any viable outer-quartic
interpretation must involve an additional adjoint, transvectant, or
other functional that annihilates the new-block image.

## 1. Complete deficit-four and deficit-five equations

Use the radial coordinates \(\{z,w\}=w\), and write
\[
P=\sum_r z^r p_r(w),\qquad Q=\sum_s z^s q_s(w).
\]
For two slices define
\[
[p_r,q_s]
=w\bigl(rp_rq_s'-sp_r'q_s\bigr).
\tag{1}
\]
This is their contribution to the coefficient of \(z^{r+s-1}\).
The fixed outer slices are \(p_2,q_3\).

At deficit four, the complete source and new-block operator are
\[
\begin{aligned}
S_4&=[p_1,q_0]+[p_0,q_1]+[p_{-1},q_2],\\
L_4(A,B)&=[A,q_3]+[p_2,B],
\end{aligned}
\tag{2}
\]
where
\[
A=p_{-2}\in\langle w^2,\ldots,w^8\rangle,\qquad
B=q_{-1}\in\langle w,\ldots,w^{12}\rangle.
\tag{3}
\]
Thus the full equation is
\[
L_4(p_{-2},q_{-1})+S_4=0.
\tag{4}
\]
Its exact linear profile is
\[
\#\mathrm{variables}=19,\qquad
\operatorname {rank}L_4=18,\qquad
\dim\operatorname {coker}L_4=2.
\tag{5}
\]
The complete output row space in the recurrence has dimension \(20\).

At deficit five,
\[
\begin{aligned}
S_5={}&[p_1,q_{-1}]+[p_0,q_0]+[p_{-1},q_1]+[p_{-2},q_2],\\
L_5(A,B)&=[A,q_3]+[p_2,B],
\end{aligned}
\tag{6}
\]
where now
\[
A=p_{-3}\in\langle w^3,\ldots,w^8\rangle,\qquad
B=q_{-2}\in\langle w^2,\ldots,w^{12}\rangle.
\tag{7}
\]
The full equation is
\[
L_5(p_{-3},q_{-2})+S_5=0,
\tag{8}
\]
with exact profile
\[
\#\mathrm{variables}=17,\qquad
\operatorname {rank}L_5=17,\qquad
\dim\operatorname {coker}L_5=2.
\tag{9}
\]
Here the complete output row space has dimension \(19\).

Equations (2) and (6) retain every source pair.  In particular, neither
calculation makes the invalid two-slice truncation that discards the
negative radial tails.

## 2. The outer quartic

Write the normalized outer pair as
\[
U(w)=\sum_{i=0}^7u_iw^i,\qquad
V(w)=\sum_{j=0}^{10}v_jw^j
\]
and put
\[
\lambda=\frac{v_{10}^2}{u_7^3},\qquad
E(w)=wV(w)^2-\lambda U(w)^3.
\tag{10}
\]
The outer equation cancels all terms above degree four, so \(E\) is the
outer quartic.

Work at the certified good-reduction prime \(32003\).  The five outer
points split into three field factors:
\[
t=26839,\qquad t=16621,\qquad
K_3=\mathbf F_{32003}[t]/
(t^3-11133t^2-11294t-6180).
\tag{11}
\]
The cubic factor represents its three conjugate geometric points at
once.

## 3. Exact remainder ranks

Reduce the deficit-four operator modulo \(E\):
\[
\overline L_4:
\langle w^2,\ldots,w^8\rangle
\oplus\langle w,\ldots,w^{12}\rangle
\longrightarrow K[w]/(E).
\tag{12}
\]
On all three factors in (11),
\[
\operatorname {rank}\overline L_4=4.
\tag{13}
\]
Hence (12) is surjective.  In the monomial quotient basis
\(1,w,w^2,w^3\), the determinant of the first four \(A\)-columns
\(w^2,w^3,w^4,w^5\) is
\[
\begin{array}{c|c}
\text{factor}&\det\\ \hline
t=26839&-15118\\
t=16621&6356\\
K_3&-3045+2843t+11230t^2.
\end{array}
\tag{14}
\]
Every entry in (14) is nonzero.

At deficit five, reduce modulo the first thickening:
\[
\overline L_5:
\langle w^3,\ldots,w^8\rangle
\oplus\langle w^2,\ldots,w^{12}\rangle
\longrightarrow K[w]/(E^2).
\tag{15}
\]
On every factor,
\[
\operatorname {rank}\overline L_5=8,
\tag{16}
\]
so (15) is also surjective.  Take the six \(A\)-columns
\(w^3,\ldots,w^8\), followed by the two \(B\)-columns \(w^2,w^3\).
Their \(8\times8\) determinants in the basis
\(1,w,\ldots,w^7\) are
\[
\begin{array}{c|c}
\text{factor}&\det\\ \hline
t=26839&574\\
t=16621&12957\\
K_3&-9388-14360t+8299t^2.
\end{array}
\tag{17}
\]
Again all three are nonzero.

## 4. Consequence

For ordinary remainder to define a functional on
\(\operatorname {coker}L_d\), it must annihilate
\(\operatorname {im}L_d\).  Equations (13) and (16) prove the opposite:
\[
\operatorname {rem}_E\circ L_4
\quad\text{and}\quad
\operatorname {rem}_{E^2}\circ L_5
\]
are surjective.  New-block variables can therefore alter the raw
remainder in every possible quotient direction.

This is a scoped no-go statement.  It does not say that the two cokernel
rows are unimportant, nor does it exclude a more structured
outer-quartic functional.  It says only that unweighted polynomial
division by \(E\) or \(E^2\) cannot be that functional.

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_outer_quartic_cokernel_no_go.py
```
