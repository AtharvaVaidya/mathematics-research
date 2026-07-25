# Case-c \(q_{10}\) chart audit

## Correction

The earlier wording around
`route_bd_case_c_middle_divisibility_r2.py` made the use of \(r_4^{-1}\)
look like an uncovered subchart.  In the actual case-c coefficient
stratum it is not an extra assumption.

Write
\[
 r=r_0+r_1h+r_2h^2+r_3h^3+r_4h^4,\qquad
 p_6=\frac{r^2}{4}+h^4(s_0+s_1h+s_2h^2+s_3h^3).
\]
The required top vertex of \(p_6\) is nonzero, while
\[
 [h^8]p_6=\frac{r_4^2}{4}.
\]
Therefore
\[
 \boxed{r_4\ne0}
\]
globally, before splitting into the \(r_0,r_1,r_2,r_3,r_4\) leading
charts.

## Denominator-free endpoint identity

On \(r_0=r_1=0\), let \(E_{14}\) and \(E_{13}\) denote the two
degree-\(17\) compatibility rows and put
\[
 d=p_{5,7}-\frac{r_4s_3}{2}.
\]
The exact polynomial identity is
\[
 256r_4E_{14}-512E_{13}=2688r_4d^2. \tag{1}
\]
Thus the required vertex, not an ad hoc chart localization, gives
\(d=0\).  Substitution in \(E_{14}\) gives
\[
 E_{14}\big|_{d=0}
 =-\frac5{64}r_4^4
 \left(
 q_{10,10}
 -\frac{6r_2r_4+3r_3^2+6s_2}{4}
 \right). \tag{2}
\]
Hence
\[
 \boxed{
 q_{10,10}=
 \frac{6r_2r_4+3r_3^2+6s_2}{4}
 }. \tag{3}
\]
Identity (1) contains no division by a coefficient.

This covers both disputed cases:

- On the \(r_2\)-leading chart, \(r_2\ne0\) and the already-required
  vertex supplies \(r_4\ne0\).
- On the \(r_3\)-leading chart, set \(r_2=0\) in (1)--(3).  The proof
  still uses only \(r_4\ne0\), so
  \[
  q_{10,10}=\frac{3r_3^2+6s_2}{4}.
  \]

Together with the existing \(r_0\)- and \(r_1\)-unit identities, this
proves (3) on every full case-c chart.

## Exact artificial countermodel

There is a genuine warning hidden behind the earlier concern.  If the
required \(p_6\) vertex is deleted and one imposes \(r_4=0\), the same two
endpoint rows reduce to
\[
 E_{14}=12p_{5,7}^2,\qquad E_{13}=0.
\]
Taking \(p_{5,7}=0\) solves both for arbitrary \(q_{10,10}\).  Thus the
endpoint argument does **not** prove the resonance on the enlarged
partial system.  That degeneration is excluded from the full coefficient
stratum precisely because it has \([h^8]p_6=0\).

## Universal fractional consequence

The all-parameter approximate-root calculation gives the triangular slot
\[
 q_{10,10}
 =
 [h^{10}y^{10}]A_{12}+c_{10}
 =
 \frac{6r_2r_4+3r_3^2+6s_2}{4}+c_{10}.
\]
Comparing with (3) now proves
\[
 \boxed{c_{10}=0}
\]
universally on the full case-c stratum, not merely on the \(r_0\)-unit
chart.

The later audit `CASE_C_UNIVERSAL_FRACTIONAL_DESCENT.md` now globalizes
the \(c_9,c_7,c_6,c_5\) eliminations by a required-\(r_4\) square
cascade.  Thus this limitation of the first audit has been removed.

## Reproduction

```sh
python3 route_bd_case_c_q10_chart_audit.py
python3 route_bd_case_c_middle_divisibility_r2.py
python3 route_bd_case_c_middle_divisibility_r3.py
python3 route_bd_case_c_constant_descent_r3.py
```
