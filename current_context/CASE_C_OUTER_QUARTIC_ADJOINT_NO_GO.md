# Case c: the outer quartic supplies no new linear terminal-row adjoint

Date: 25 July 2026

## Audited conclusion

Keep the corrected common diagonal object: the degree-four outer
incidence divisor
\[
E(h)=hV(h)^2-\lambda U(h)^3.
\]
Consider the first two case-c radial rows whose new-block operators
have nonzero cokernel,
\[
\begin{aligned}
L_4(A,B)&=[A,q_3]+[p_2,B],\\
L_5(A,B)&=[A,q_3]+[p_2,B],
\end{aligned}
\tag{1}
\]
with the deficit-dependent radial degrees and supports specified below.

The complete jet audit gives a sharp no-go theorem.

> **Outer-quartic adjoint no-go.** On every one of the five certified
> geometric outer points, reduction of either \(L_4\) or \(L_5\) modulo
> \(E^j\) is surjective for
> \[
> j=1,2,3,4.
> \tag{2}
> \]
> Therefore no nonzero linear functional supported on the four roots
> of \(E\), using normal derivatives of orders at most three, descends
> to either cokernel.
>
> At the first possible order, \(j=5\), the quartic-jet model is merely
> a coordinate realization of the already-known row cokernels.  The
> only linear adjoint common to both new-block images is
> \[
> \boxed{F\longmapsto[h^{19}]F.}
> \tag{3}
> \]
> It is the ordinary Newton support ceiling and is independent of
> \(E\).

In particular, fixing \(E\) in a classical transvectant or adjoint
construction cannot produce a new common *linear* invariant coupling
the two capped rows.  Through derivative order three it vanishes
identically if it annihilates the new blocks.  At derivative order
four it is only a repackaging of the existing two-dimensional
cokernels, and the common line is the bare top-coefficient row (3).

This does not exclude a genuinely nonlinear construction involving
products, norms, or determinants of several cokernel values.  It does
eliminate the proposed first step: there is no new scalar linear
outer-quartic adjoint from which such a coupling follows automatically.

## 1. Complete operators and row spaces

Use radial coordinates \(\{z,h\}=h\), and write
\[
[p_r,q_s]
=h\left(rp_rq_s'-sp_r'q_s\right).
\tag{4}
\]
The outer blocks are
\[
p_2=\frac{U(h)}h,\qquad q_3=\frac{V(h)}h.
\tag{5}
\]

At deficit four,
\[
\begin{aligned}
A=p_{-2}&\in\langle h^2,\ldots,h^8\rangle,\\
B=q_{-1}&\in\langle h,\ldots,h^{12}\rangle,
\end{aligned}
\tag{6}
\]
and
\[
L_4(A,B)=[A,q_3]+[p_2,B].
\tag{7}
\]
Its image lies in
\[
\langle1,h,\ldots,h^{18}\rangle
\tag{8}
\]
and has rank \(18\).  The complete row also contains the source
coefficient of \(h^{19}\), so its row space is
\[
W_4=\langle1,h,\ldots,h^{19}\rangle,
\qquad\dim W_4=20,
\tag{9}
\]
and \(\dim\operatorname {coker}_{W_4}L_4=2\).

At deficit five,
\[
\begin{aligned}
A=p_{-3}&\in\langle h^3,\ldots,h^8\rangle,\\
B=q_{-2}&\in\langle h^2,\ldots,h^{12}\rangle,
\end{aligned}
\tag{10}
\]
with the same formula (7), now using radial degrees \((-3,-2)\).
The image lies in
\[
\langle h,h^2,\ldots,h^{18}\rangle
\tag{11}
\]
and has rank \(17\).  The complete row space is
\[
W_5=\langle h,h^2,\ldots,h^{19}\rangle,
\qquad\dim W_5=19,
\tag{12}
\]
so its cokernel again has dimension two.

These are the complete new-block operators.  The source terms retained
in the recurrence are
\[
\begin{aligned}
S_4&=[p_1,q_0]+[p_0,q_1]+[p_{-1},q_2],\\
S_5&=[p_1,q_{-1}]+[p_0,q_0]
     +[p_{-1},q_1]+[p_{-2},q_2].
\end{aligned}
\tag{13}
\]

## 2. Quartic jets through order three are fully movable

For \(j\ge1\), put
\[
A_j=k[h]/(E^j).
\tag{14}
\]
Because \(E\) is squarefree, after extension to an algebraic closure
\[
A_j\simeq
\prod_{\alpha:E(\alpha)=0}
k[\epsilon_\alpha]/(\epsilon_\alpha^j).
\tag{15}
\]
Thus \(A_j^\vee\) is exactly the space of distributions on the four
outer incidence points using derivatives of orders \(0,\ldots,j-1\).

On the two rational factors and the cubic factor of the certified
outer Hurwitz algebra modulo \(32003\), the exact ranks are
\[
\begin{array}{c|ccccc}
&A_1&A_2&A_3&A_4&A_5\\ \hline
L_4&4&8&12&16&18\\
L_5&4&8&12&16&17.
\end{array}
\tag{16}
\]
The first four entries equal \(\dim A_j=4j\), proving (2).

For reproducibility, take the operator columns in support order:
all \(A\)-monomials followed by all \(B\)-monomials.  The determinants
of the first \(4j\) columns modulo \(E^j\), for \(j=1,2,3,4\), are:
\[
\begin{array}{c|c|rrrr}
\text{operator}&\text{factor}&j=1&j=2&j=3&j=4\\ \hline
L_4&t=26839&-15118&4149&6224&-13264\\
L_4&t=16621&6356&11610&-6102&-7721\\
L_4&K_3&
-3045+2843t+11230t^2&
4745+7246t+562t^2&
-14747+1856t+7785t^2&
-13464+9604t-2707t^2\\[2mm]
L_5&t=26839&5862&574&1637&-7634\\
L_5&t=16621&-11106&12957&14206&2100\\
L_5&K_3&
11507+9334t-14560t^2&
-9388-14360t+8299t^2&
-5638-12989t+10936t^2&
-4378-12647t-8654t^2.
\end{array}
\tag{17}
\]
Here
\[
K_3=\mathbf F_{32003}[t]/
(t^3-11133t^2-11294t-6180).
\]
Every entry in (17) is nonzero.

The five factors are exhausted by these two rational points and the
three conjugates represented by \(K_3\).  Since \(32003\) is a good
reduction prime, the nonzero minors lift to the characteristic-zero
outer Hurwitz field.

Now let \(\ell\in A_j^\vee\) annihilate the new-block image.  For
\(j\le4\), surjectivity gives
\[
\ell=0.
\tag{18}
\]
This excludes evaluation, residue, first-adjoint, and all higher local
jet variants through derivative order three.  It strengthens the raw
remainder audit: the failure is not confined to \(E\) or \(E^2\).

## 3. Order four recovers only the old cokernels

The polynomial \(E^5\) has degree \(20\).  Ordinary remainder therefore
gives an isomorphism
\[
W_4\xrightarrow{\sim}A_5.
\tag{19}
\]
It is injective on \(W_5\), whose image has codimension one in \(A_5\).

By (16), the annihilator of \(L_4\) in \(A_5^\vee\) has dimension two,
exactly the dimension of the original \(W_4\)-cokernel.  For \(L_5\)
the ambient annihilator has dimension three; one line annihilates all
of \(W_5\), leaving exactly the original two-dimensional
\(W_5\)-cokernel after restriction.

Thus order-four distributions on the roots of \(E\) do not give a
new quotient.  They are simply Hermite-interpolation coordinates for
the full bounded rows.

This observation covers a scalar transvectant with \(E\) as well.
For fixed \(E\), such a transvectant is linear in the row polynomial.
After restricting to \(W_4\) or \(W_5\), it is one of the functionals
already represented in (19).  If it annihilates a new-block image, it
belongs to the corresponding old cokernel dual.

## 4. The unique common adjoint is outer-independent

Embed both new-block images in \(W_4\).  Every column of \(L_4\) and
\(L_5\) has degree at most \(18\), so
\[
[h^{19}]
\]
annihilates both.

Exact good-reduction arithmetic gives
\[
\operatorname {rank}
\bigl(\operatorname {im}L_4+\operatorname {im}L_5\bigr)=19
\tag{20}
\]
on all five outer points.  Since the combined image is contained in
the \(19\)-dimensional space
\(\langle1,\ldots,h^{18}\rangle\), equality in (20) proves
\[
\operatorname {im}L_4+\operatorname {im}L_5
=\langle1,h,\ldots,h^{18}\rangle.
\tag{21}
\]
Consequently
\[
\boxed{
(\operatorname {im}L_4+\operatorname {im}L_5)^\perp
=k\,[h^{19}].
}
\tag{22}
\]

One common \(19\times19\) minor has values
\[
\begin{array}{c|c}
\text{factor}&\det\\ \hline
t=26839&-11441\\
t=16621&6477\\
K_3&-10846+9591t+15152t^2.
\end{array}
\tag{23}
\]
The chosen columns are columns
\[
0,1,\ldots,16,18
\]
of \(L_4\), followed by the first \(B\)-column of \(L_5\); the rows are
\(1,h,\ldots,h^{18}\).

The common functional has the explicit source values
\[
\begin{aligned}
[h^{19}]S_4
&=12[p_1]_{h^7}[q_0]_{h^{12}}
  -8[p_0]_{h^8}[q_1]_{h^{11}},\\
[h^{19}]S_5
&=19\left(
[p_1]_{h^7}[q_{-1}]_{h^{12}}
-[p_{-1}]_{h^8}[q_1]_{h^{11}}
\right).
\end{aligned}
\tag{24}
\]
These are ordinary support-top determinants.  Neither formula contains
\(E\), a root of \(E\), its discriminant, or a Kummer labeling.

Therefore the only common linear terminal-row adjoint cannot transport
the four normalized cap branches to the four outer incidence points.
It is already present before the outer quartic is introduced.

## 5. Consequence for the finite-support route

The finite Newton cutoff remains the correct source of the global
case-c obstruction, as the complete certificate demonstrates.  What
fails is the proposed simplification through one new quartic-supported
linear invariant:

1. the four roots and all jets through order three are freely movable
   by each new block;
2. order-four quartic jets merely re-coordinate the complete bounded
   rows;
3. the unique adjoint common to the first two capped rows is
   \([h^{19}]\), independent of the degree-four cover.

A promising further invariant would therefore have to be nonlinear in
at least two existing cokernel values and prove an additional
finite-support identity relating them.  That identity cannot be
obtained from the outer quartic, its root labeling, or a single
transvectant alone.

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_outer_quartic_adjoint_no_go.py
```
