# Universal case-c fractional descent

## Result

The five nonintegral approximate-root modes now vanish on every possible
full case-c point:
\[
\boxed{c_{10}=c_9=c_7=c_6=c_5=0.}
\]
Together with the earlier endpoint,
\[
\boxed{c_{11}=0,}
\]
this leaves only the integral modes \(c_8P,c_4H\) and the cubic
remainder.

The correction is chart-free on the only surviving tail charts.  It uses
the globally required vertex \(r_4\ne0\), not \(r_0\ne0\).

## Scope of the chart cover

The prior exact results give:

- \(r_0\ne0\): all fractional modes vanish by the existing
  `route_bd_case_c_fractional_resonances_r0.py`.
- \(r_0=0,r_1\ne0\): the normalized formal-tail differential has a
  nonzero hyperelliptic de Rham class, so no full point exists on this
  chart.
- \(r_0=r_1=0\): the constant coefficient of the canonical square root
  is polynomial on the \(r_2,r_3,r_4\) leading charts.  The calculation
  below treats \(r_2\) as an arbitrary coefficient and therefore covers
  all three at once.

The required \(p_6\) vertex gives
\[
[h^8]p_6=\frac{r_4^2}{4}\ne0. \tag{1}
\]

## The \(c_9\) endpoint

Once \(H=(P^{1/2})_+\) is polynomial, write
\[
P=H^2+R,\qquad \deg_yR\le3.
\]
Let
\[
q_{9,9}=q_{9,9}^{\rm cube}+g.
\]
Because \(c_{10}=0\), the triangular approximate-root identity identifies
\(g=c_9\).  An unused grade-13 compatibility endpoint is
\[
E_{13}[h^{16}]
=-\frac{45}{1024}r_4^4g. \tag{2}
\]
Equations (1)--(2) give
\[
\boxed{c_9=0.}
\]

## The square cascade

After \(g=0\), put
\[
U=-4p_{4,6}+2r_4w_2+s_3^2.
\]
The next endpoint is
\[
E_{12}[h^{15}]=\frac34U^2, \tag{3}
\]
so \(U=0\).  In the approximate-root triangular coordinates, the
grade-11 endpoint then becomes
\[
E_{11}[h^{14}]=\frac{35}{1024}r_4^4c_7, \tag{4}
\]
hence \(c_7=0\).

Define
\[
\begin{aligned}
B={}&r_3r_4w_2+r_4^2w_1+r_4s_2s_3-2s_3w_2,\\
X={}&2p_{3,5}-r_4p_{4,5}+\frac B2.
\end{aligned}
\]
Two exact rows are
\[
\begin{aligned}
E_{10}[h^{13}]
  &=\frac3{64}\left(r_4^4c_6+64X^2\right),\\
E_9[h^{13}]
  &=\frac{3r_4}{128}\left(r_4^4c_6+24X^2\right).
\end{aligned} \tag{5}
\]
Their normalized difference is \(40X^2\).  Therefore \(X=0\), and (5)
then gives \(c_6=0\).  Finally,
\[
E_9[h^{12}]=\frac{35}{1024}r_4^4c_5, \tag{6}
\]
so \(c_5=0\).

Every equation is polynomial before using the already-required unit
\(r_4\).  No \(r_2\), \(r_3\), \(s_i\), \(w_i\), or auxiliary defect is
inverted.

## Consequence

On every possible full case-c point the positive part has the integral
normal form
\[
P_+=H^2+R,\qquad
Q_+=H^3+\frac32HR+c_8P_++c_4H+S,
\qquad
\deg_yR,\deg_yS\le3.
\]
This does not by itself solve the remaining lower-remainder equations,
but it removes every fractional approximate power globally.

For the actual non-cusp boundary curve, the highest surviving resonance
is now \(c_8\) or \(c_4\).  Hence
\[
\deg(q^2-Lp^3)\in\{20,16\}\quad\text{or}\quad\le15,
\]
so its cusp contact at infinity is \(4\), \(8\), or at least \(9\).

## Reproduction

```sh
python3 route_bd_case_c_universal_fractional_resonances.py
```
