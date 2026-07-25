# Case-c all-parameter approximate-root normal form

Date: 2026-07-24

## Result

Let \(K=\mathbf C(h)\), with derivation \(d/dh\), and write the positive
\(y\)-part of the case-c pair as
\[
 P=\sum_{d=0}^8p_d(h)y^d,\qquad
 Q=\sum_{e=0}^{12}q_e(h)y^e.
\]
After choosing \(\alpha^8=a\), the forced top edge gives
\[
 p_8=a h^8=(\alpha h)^8.
\]
In the Laurent-series field \(K((y^{-1}))\), take the unique branch
\[
 L=P^{1/8}=\alpha h\,y+O(1)
\]
and define
\[
 A_j=(L^j)_+,
\]
where the plus sign means polynomial part in \(y\).

The complete, unspecialized solution of the nine upper identities
\(E_{12},\ldots,E_{20}=0\) is
\[
 \boxed{\quad
 Q=\sum_{j=4}^{12}c_jA_j+S_3,\qquad
 c_j\in\mathbf C,\quad \deg_yS_3\le3.
 \quad} \tag{1}
\]
This is an exact all-parameter statement over characteristic zero.  It is not
a statement about a sampled family or a finite-field fiber.

## Proof of completeness

Put
\[
 J(f,g)=f_hg_y-f_yg_h.
\]
The case-c grade identities \(E_{12},\ldots,E_{20}=0\) are exactly
\[
 \deg_y J(P,Q)\le10. \tag{2}
\]

The polynomials \(A_0,\ldots,A_{12}\) form a triangular basis of the
polynomials of \(y\)-degree at most \(12\):
\[
 A_j=(\alpha h)^j y^j+\text{lower powers of }y.
\]
Thus every \(Q\) has a unique expression
\[
 Q=\sum_{j=0}^{12}d_j(h)A_j.
\]

The exact Laurent power \(L^j\) commutes with \(P=L^8\).  Since
\(L^j-A_j\) starts in degree \(y^{-1}\),
\[
 \deg_yJ(P,A_j)\le6. \tag{3}
\]
On the other hand,
\[
 J(P,d_jA_j)
 =d_jJ(P,A_j)-d_j'P_yA_j,
\]
and the last term has leading coefficient
\[
 -8(\alpha h)^{j+8}d_j'\,y^{j+7}.
\]
Reading (2) successively in degrees \(19,18,\ldots,11\) gives
\[
 d_{12}'=d_{11}'=\cdots=d_4'=0.
\]
Hence \(d_4,\ldots,d_{12}\) are constants, while the four remaining terms
have degree at most three.  This proves (1).  Conversely, (3) and
\(\deg_yS_3\le3\) immediately imply (2).

## Square/cube interpretation

The canonical approximate square root is
\[
 H=A_4=(P^{1/2})_+.
\]
It satisfies
\[
 P=H^2+R,\qquad \deg_yR\le3. \tag{4}
\]
Also \(A_8=P\), and
\[
 A_{12}-H^3-\frac32HR
\]
has \(y\)-degree at most two.  Thus, if the fractional resonances
\(c_j\) with \(j\notin\{4,8,12\}\) vanish, (1) becomes the expected
polynomial square/cube approximate-root form, up to terms of degree three.

Write the already-proved first descent as
\[
 p_7=h^4r(h),\qquad \deg r=4.
\]
The first three coefficients of \(H\) are
\[
\begin{aligned}
 [y^4]H&=\alpha^4h^4,\\
 [y^3]H&=\frac{r}{2\alpha^4},\\
 [y^2]H&=
 \frac{p_6-r^2/(4\alpha^8)}{2\alpha^4h^4}.
\end{aligned} \tag{5}
\]
The previous exact descent proves that the numerator in the last line is
divisible by \(h^2\).  The next two compatibility grades in fact give the
stronger universal result
\[
 \boxed{\quad h^4\mid p_6-\frac{r^2}{4\alpha^8}.\quad} \tag{5a}
\]
Hence the \(y^2\) coefficient displayed in (5) is a polynomial in \(h\).

The proof of (5a) is an exhaustive three-chart argument.  Write
\(r=r_0+r_1h+\cdots+r_4h^4\), and let \(D_2,D_3\) be four times the
coefficients of \(h^2,h^3\), respectively, in
\(\alpha^8p_6-r^2/4\).

* On \(r_0\ne0\), grade 15 gives a nonzero multiple of \(r_0D_2^2\).
  After \(D_2=0\), the resultant of the next grade-15 and grade-14
  equations with respect to the \(q_{10}\) resonance is
  \[
  181440\,\alpha^{16}b\,r_0^5D_3^2.
  \]
* On \(r_0=0,\ r_1\ne0\), grade 15 gives a nonzero multiple of
  \(r_1D_2^2\).  If \(D_3\ne0\), eliminating \(p_{5,0}\) from the next
  two equations gives
  \[
  -8640\,\alpha^{32}b^3r_1^2D_3^2,
  \]
  a contradiction.
* On \(r_0=r_1=0\), three grade-14 rows are successively nonzero
  multiples of
  \[
  p_{6,2}^3,\qquad p_{5,0}^2,\qquad p_{6,3}^3.
  \]
  They force all three coefficients to vanish, hence \(D_2=D_3=0\).

These charts include every possible order of vanishing of \(r\) at \(h=0\).

Put
\[
 s=\frac{p_6-r^2/(4\alpha^8)}{h^4}.
\]
The next coefficient of the approximate square root is
\[
 [y]H=
 \frac{p_5-rs/(2\alpha^8)}{2\alpha^4h^4}. \tag{5b}
\]
The middle identities \(E_{11},\ldots,E_9\), together with the already
used upper endpoint rows, give the second universal divisibility
\[
 \boxed{\quad h^4\mid p_5-\frac{rs}{2\alpha^8}.\quad} \tag{5c}
\]
Its proof is exhaustive in the five charts
\(\operatorname{ord}_h(r)=0,1,2,3,4\).  The \(r_0\)- and \(r_1\)-unit
charts reduce successively to nonzero multiples of squares of the four
low defect coefficients.  The \(r_2\)- and \(r_3\)-unit charts use exact
radical consequences through \(E_9\); their final complementary-chart
ideals contain the third and seventh powers, respectively, of
\([h^3](p_5-rs/(2\alpha^8))\).  The order-four chart is the maximal
\(r=h^4\) calculation.  Hence (5b) is polynomial in \(h\).

The analogous statements for the last two coefficients of \(H\) are false
for the upper system alone.  There are exact full-vertex solutions of
\(E_{12},\ldots,E_{20}=0\) for which
\[
[y]H=\frac1{2h^2},
\]
and others for which \([y]H=0\) but
\[
[1]H=\frac1{2h^2}.
\]
Both are recorded term by term in
`route_bd_case_c_approx_pole_witness.py`.  For each underlying fixed \(P\),
the complete partner matrix has rank \(124\) and its target augmentation
has rank \(125\), so that particular upper fiber does not extend to a full
solution merely by changing \(Q\).  The point of the witnesses is sharper:
polynomiality of the last two coefficients, if universal for full solutions,
must use the lower equations \(E_{11},\ldots,E_{-1}\).

The first pole fiber is eliminated as soon as \(E_{11}\) is imposed: the
resulting affine system forces the scalar in
\(q_{12}=B(z-1)^{12}\) to be zero.  The second survives through \(E_9\),
but \(E_8\) again forces \(B=0\).  The exact rank pairs are checked in the
same witness verifier.

## Identification and elimination of the first resonance

The forced coefficient \(q_{12}=b h^{12}\) fixes
\[
 c_{12}=\frac b{\alpha^{12}}.
\]
The \(y^{11}\) coefficient in (1) is
\[
 q_{11}
 =\frac{3b}{2\alpha^8}h^8r
 c_{11}\alpha^{11}h^{11}. \tag{6}
\]
Consequently the resonant parameter called \(\lambda\) in the descending
coefficient calculation is exactly
\[
 \lambda=c_{11}\alpha^{11}.
\]
The exact grade-15 endpoint equation is
\[
 -\frac{77}{1024}
 \frac{\lambda r_4^4}{\alpha^{24}}=0.
\]
The required \(p_6\) vertex gives \(r_4\ne0\), so
\[
 \boxed{c_{11}=0.}
\]

The same basis also recovers the opposite required edge coefficient.  From
\([h^8]p_6=r_4^2/(4\alpha^8)\), the \(c_{12}A_{12}\) contribution gives
\[
 [h^{12}]q_9
 =\frac{b r_4^3}{8\alpha^{24}}\ne0. \tag{7}
\]

## Exact scope and next obstruction

Formula (1) compresses every upper-grade solution, with all coefficients
still free, to nine constants and a cubic remainder.  It also gives a
coordinate-free interpretation of every raw resonant parameter:
\(c_j\) is the coefficient of the fractional approximate power
\((P^{j/8})_+\).

The later all-chart audits eliminate every fractional mode:
\[
c_{11}=c_{10}=c_9=c_7=c_6=c_5=0.
\]
See `current_context/CASE_C_Q10_CHART_AUDIT.md` and
`current_context/CASE_C_UNIVERSAL_FRACTIONAL_DESCENT.md`.  The required
\(p_6\) vertex forces \(r_4\ne0\), which supplies the only unit in the
lower square cascade.  The canonical square root \(H\) is polynomial on
every surviving chart; the \(r_0\) and \(r_1\) charts are already excluded
by the formal-tail obstruction.  Thus the only remaining approximate-root
modes are the genuine integral powers \(c_8P\) and \(c_4H\), together with
the cubic remainder.
The theorem above turns that task into a finite exact resonance
problem; it does not claim that case c, the \((72,108)\) frontier, or
\(JC(2)\) is already resolved.

## Reproduction

```sh
.venv/bin/python route_bd_case_c_approx_root.py
.venv/bin/python route_bd_case_c_approx_divisibility.py
.venv/bin/python route_bd_case_c_approx_pole_witness.py
.venv/bin/python route_bd_case_c_middle_divisibility_r0.py
.venv/bin/python route_bd_case_c_middle_divisibility_r1.py
.venv/bin/python route_bd_case_c_middle_divisibility_r2.py
.venv/bin/python route_bd_case_c_middle_divisibility_r3.py
.venv/bin/python route_bd_case_c_middle_divisibility.py
```

The verifier constructs every \(A_j\), \(0\le j\le12\), from the finite
binomial expansion with symbolic \(p_0,\ldots,p_7\), symbolic coefficient
derivatives, and no numerical substitutions.  It checks (3), the triangular
diagonal, (4)--(7), and the endpoint resonance normalization exactly.
