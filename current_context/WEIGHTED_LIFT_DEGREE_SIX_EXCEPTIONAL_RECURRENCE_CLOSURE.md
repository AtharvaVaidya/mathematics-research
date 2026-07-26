# Closure of the first exceptional all-degree binary face

Date: 25 July 2026

## Outcome

The first family left open by
`WEIGHTED_LIFT_ALL_DEGREE_BINARY_TARGET_REDUCTION.md` is
\[
Q_6=B^5(\lambda A+\mu B),\qquad \lambda\mu\ne0,
\tag{1}
\]
on the characteristic rays
\[
\begin{aligned}
I&=48k+33,&J&=47k+32,\\
r&=30k+20,&s&=17k+12,\qquad k\ge1.
\end{aligned}
\tag{2}
\]
It is not exceptional after the first lower seed is included.  The
graph-weight-\((m+4)\) equation has the exact scalar residue
\[
\boxed{
-\frac{453}{34}
-\frac{7(931k+616)}{15}
=-\frac{221578k+153403}{510}\ne0.
}
\tag{3}
\]
The coefficient is independent of the characteristic amplitude, of
the mixed-face parameter, and of every same-weight graph correction.
Consequently no polynomial graph can make
\[
\bigl(U,\ B^5(\lambda A+\mu B)\bigr)
\tag{4}
\]
have constant nonzero Jacobian.

Together with the preceding all-degree reduction, this closes every
homogeneous binary second target through degree six.  It does not
address the next exceptional families in degree seven or higher, nor
targets involving \(C\).

## 1. The exact first two seed slices

Put
\[
u=1+xy,\qquad t=\frac ux,\qquad
\gamma=1-\frac{57}{34}xy+x^2g(x,y).
\tag{5}
\]
The exact second-subduction numerator has consecutive terms
\[
\theta w^{20}\gamma^2
-\frac{70}{3}\theta w^{19}\gamma^2,
\tag{6}
\]
before division by \(x^5\gamma^5\).  Hence its first two
graph-weight slices are
\[
\begin{aligned}
U^{(0)}&=\theta x^{15}t^{20}\gamma^{17},\\
U^{(1)}&=-\frac{70}{3}\theta
 x^{14}t^{19}\gamma^{16}.
\end{aligned}
\tag{7}
\]
The seed ratios
\[
\frac{q_5}{q_6}=-\frac{28}{5},
\qquad
\frac{p_4}{p_5}=-\frac{35}{6}
\tag{8}
\]
give
\[
\frac{q_5}{q_6}+5\frac{p_4}{p_5}
=-\frac{1043}{30},
\qquad
6\frac{p_4}{p_5}=-35.
\tag{9}
\]
After absorbing the nonzero coefficient
\(\lambda q_6p_5^5\), and writing
\[
\eta=\frac{\mu p_5}{\lambda q_6},
\tag{10}
\]
the first two slices of (1) therefore are
\[
\begin{aligned}
V^{(0)}
 &=x^{24}t^{30}\gamma^{24}(t+\eta),\\
V^{(1)}
 &=x^{23}t^{29}\gamma^{23}
   \left(-\frac{1043}{30}t-35\eta\right).
\end{aligned}
\tag{11}
\]
Every omitted numerator term is strictly below this first-lower
slice for \(m\ge1\).  No full additional \(m+4\) gap is asserted:
for example, the exact \(U\)-numerator contains \(w^{20}\), whose
gap below \(w^{19}\gamma^2\) is only \(m\).  In the target, \(q_4\)
and \(p_3\) cost \(2(m+4)\) relative to \(q_6\) and \(p_5\);
using two of the displayed first-lower seeds does the same.  The
added \(w\gamma\) in \(A\) and \(\gamma\) in \(B\) each cost
\(4m+18\).  Thus only the terms in (7) and (11) occur on the
graph-weight-\((m+4)\) slice.

## 2. Reduction to one inhomogeneous characteristic equation

The top-top Jacobian is a nonzero common factor times
\[
\mathcal L(\gamma)
=x\left(\frac{30}{t}+\frac{17}{t+\eta}\right)\gamma_x
-48\gamma_t
+\left(-\frac{30}{t}+\frac{15}{t+\eta}\right)\gamma.
\tag{12}
\]
The characteristic polynomial
\[
G=c\,x^{48k+33}t^{30k+20}
(t+\eta)^{17k+12}
\tag{13}
\]
satisfies \(\mathcal L(G)=0\).

At the next seed slice, divide
\[
J(U^{(1)},V^{(0)})+J(U^{(0)},V^{(1)})
\tag{14}
\]
by the same top-top common factor.  Direct differentiation, followed
only by the substitutions in (2), gives
\[
\begin{aligned}
\mathcal R_k
=-\frac{7}{15xt^2(t+\eta)^2}
\bigl(& (900k+600)\eta^2\\
 &+(1440k+940)\eta t\\
 &+(931k+616)t^2\bigr).
\end{aligned}
\tag{15}
\]
Thus the exact first lower recurrence is
\[
\mathcal L(\delta\gamma)+\mathcal R_k=0.
\tag{16}
\]
The characteristic amplitude \(c\) cancels from (15).  This is the
promised reduction: no search over the many coefficients of the
degree-\(m\) graph is needed.

## 3. The source-axis scalar obstruction

Set
\[
H=u+\eta x,\qquad
K=47u+30\eta x,\qquad
L=-15u-30\eta x.
\tag{17}
\]
Multiplication of (16) by \(uH\), followed by return to source
coordinates, turns its homogeneous part into the polynomial operator
\[
\mathcal E(\phi)
=xK(x\phi_x-y\phi_y)
+u(K-48H)\phi_y
+xL\phi.
\tag{18}
\]
Under the same transformation the lower-seed forcing is
\[
\begin{aligned}
uH\mathcal R_k
=-\frac{7x}{15uH}\bigl(&
(931k+616)u^2\\
&+(1440k+940)\eta ux\\
&+(900k+600)\eta^2x^2
\bigr).
\end{aligned}
\tag{19}
\]

The fixed graph jet is
\[
\gamma_{\rm fix}=1-\frac{57}{34}(u-1).
\tag{20}
\]
Since \(u=1+xy\) and \(H=1+O(x)\), equations (18)--(20) give
\[
\begin{aligned}
\mathcal E(\gamma_{\rm fix})
&\equiv-\frac{453}{34}x\pmod{x^2},\\
uH\mathcal R_k
&\equiv-\frac{7(931k+616)}{15}x\pmod{x^2}.
\end{aligned}
\tag{21}
\]
Their sum is exactly (3).

Every polynomial graph correction enters \(\gamma\) as
\(x^2h(x,y)\).  Each of the three terms in (18) remains divisible
by \(x^2\) on such a correction.  Therefore no same-weight or lower
graph coefficient changes (21).  The characteristic term (13) is
itself graph-divisible for \(k\ge1\), since in the \((x,u)\)-chart
it is
\[
G=c\,x^{k+1}u^{30k+20}(u+\eta x)^{17k+12},
\tag{22}
\]
and it already lies in the kernel of the homogeneous operator.

Finally, the numerator in (3) is positive for every \(k\ge1\).
Hence the graph-weight-\((m+4)\) Jacobian coefficient cannot vanish,
which closes the family (1).

The accompanying exact verifier is
`verify_weighted_lift_degree_six_exceptional_recurrence_closure.py`.
