# Audit of the ternary pure-face boundary separation

Date: 25 July 2026

## Outcome

The maximal-\(x\) and nonzero-root arguments for nonpolynomial and
mixed least-\(C\) faces remain valid.  The proposed proof for a pure
least-\(C\) face does not.

The defect is a change of valuation.  Loss pairs computed with
\(t\) fixed isolate the \(x^I\) and \(x^{-1}\) equations, but the
pure-face argument then sets \(t=u/x\) and uses the divisor \(x=0\)
with \(u\) fixed.  On that divisor:

- all 77 seed terms of \(U\), not only \(w^{20}\gamma^2\), have the
  same \(x^{-5}\)-factor;
- every seed term of \(A\) has the same \(x^{-2}\)-factor, and every
  seed term of \(B\) the same \(x^{-1}\)-factor;
- a higher \(C\)-tier can have exactly the same boundary
  \(x\)-valuation as the pure least-\(C\) monomial.

Thus the top Euler operator alone does not govern the fixed boundary
jet.  An exact boundary Wronskian using the full seed is required,
and higher \(C\)-tiers may enter it.  Consequently the claimed
all-degree homogeneous ternary closure is not established by the
current pure-face argument.

There is still a rigorous partial salvage: the exact first-lower
\(x^{-1}\) forcing closes every pure face except two explicit
algebraic exceptional loci given in Section 4.

## 1. Exact restriction to the source boundary

Put \(u=1+xy\) and write
\[
\gamma=f(u)+O(x),
\qquad
f(1)=1,\quad f'(1)=-\frac{57}{34}.
\tag{1}
\]
Since \(w=u\gamma\), the exact seed formulas restrict to
\[
\begin{aligned}
U&=x^{-5}\,\overline U(u)+O(x^{-4}),\\
A&=x^{-2}\,\overline A(u)+O(x^{-1}),\\
B&=x^{-1}\,\overline B(u)+O(1),\\
C&=x\,f(u)+O(x^2),
\end{aligned}
\tag{2}
\]
where
\[
\begin{aligned}
\overline U
&=\frac{\mathcal N(uf,f)}{f^5},\\
\overline A
&=\frac{q(uf)+uf^2}{f^2},\\
\overline B
&=\frac{p(uf)+f}{f}.
\end{aligned}
\tag{3}
\]
Here \(\mathcal N\) is the full 77-term second-subduction numerator.

Formula (3), rather than its highest \(u\)-degree monomial, is forced
on the boundary.  Indeed,
\[
\frac{w^i\gamma^j}{x^5\gamma^5}
=x^{-5}u^if^{i+j-5}
\tag{4}
\]
for every support monomial of \(\mathcal N\).  Likewise every
\(q_kw^k/(x^2\gamma^2)\) contributes to \(\overline A\), and every
\(p_kw^k/(x\gamma)\) contributes to \(\overline B\), at the same
boundary \(x\)-order.

This explicitly disproves the assertion that lower seeds enter only
after the boundary \(x^0\)-coefficient.

## 2. The actual pure-face boundary equation

For the pure least-\(C\) monomial
\[
V=C^\ell A^dB^{N-d},
\tag{5}
\]
put
\[
\beta=\ell-N-d,\qquad
\overline V=f^\ell\overline A^d\overline B^{N-d}.
\tag{6}
\]
Then
\[
V=x^\beta\overline V(u)+O(x^{\beta+1}).
\tag{7}
\]
The identity
\[
J_{x,y}=xJ_{x,u}
\tag{8}
\]
gives the exact leading boundary coefficient
\[
\boxed{
J_{x,y}(U,V)
=x^{\beta-5}
\left(
-5\overline U\,\overline V'
-\beta\overline U'\,\overline V
\right)
+O(x^{\beta-4}).
}
\tag{9}
\]
Thus the necessary boundary equation is the full Wronskian
\[
-5\overline U\,\overline V'
-\beta\overline U'\,\overline V=0,
\tag{10}
\]
not
\[
(17d-3N-22\ell)uf'
+(15d-5N-20\ell)f=0.
\tag{11}
\]
Equation (11) is only the highest-\(u\)-degree part of (10).  Its
fixed-jet contradiction cannot be applied to the full boundary
coefficient.

The distinction is already visible in the local jet.  Write
\[
f=1-\frac{57}{34}v+h_2v^2+O(v^3),
\qquad v=u-1.
\tag{12}
\]
Exact expansion of (3) gives
\[
\begin{aligned}
\overline B
&=\frac{23}{34}v+O(v^2),\\
\overline A
&=-\frac{157216h_2-412769}{106352}v^2+O(v^3),\\
\overline U
&=-\frac{
729(3523346237408h_2-9052069219409)
}{
123353897489720731381006336
}v^5+O(v^6).
\end{aligned}
\tag{13}
\]
The leading coefficients of \(\overline A\) and \(\overline U\)
depend on the free second graph jet \(h_2\), and their exceptional
values are distinct.  This behavior is absent from the top Euler
model.

## 3. Explicit higher-\(C\) counterterm

The failure is not limited to lower seed coefficients.  Suppose
\[
N-d\ge3.
\tag{14}
\]
The next \(C\)-tier may contain
\[
V_1
=C^{\ell+1}A^{d+2}B^{N-d-3}.
\tag{15}
\]
It has the same total target degree as (5), and its boundary
\(x\)-exponent is
\[
\begin{aligned}
\beta_1
&=(\ell+1)-2(d+2)-(N-d-3)\\
&=\ell-N-d\\
&=\beta.
\end{aligned}
\tag{16}
\]
Hence \(V_1\) contributes to exactly the same coefficient
\(x^{\beta-5}\) in (9).  It can participate directly in the boundary
Wronskian.

This is compatible with the maximal-\(x\) calculation: (15) is lower
there by \(3(I+1)\).  The equality (16) appears only after changing
to the source-boundary valuation \(t=u/x\).  Therefore maximal-\(x\)
separation cannot be reused at \(x=0,u\) fixed.

More generally, the \(k\)-th higher \(C\)-tier monomial
\[
C^{\ell+k}A^{d+2k}B^{N-d-3k}
\tag{17}
\]
has the same boundary exponent whenever \(N-d\ge3k\).

## 4. What the first-lower pole still proves

For \(P=t^d\), the exact ternary forcing from the maximal-\(x\)
calculation is
\[
\mathcal R
=\frac{7K_{N,\ell,d,I}}{
30(4N+\ell)xt^2
},
\tag{18}
\]
where
\[
\boxed{
\begin{aligned}
K_{N,\ell,d,I}
={}&(N-\ell+d)\\
&\cdot\left(
I(100\ell-25N+17d)
+100\ell+25N+15d
\right).
\end{aligned}
}
\tag{19}
\]
The characteristic operator on the polynomial \(x^{-1}\)-sector has
at most a simple pole at \(t=0\), whereas (18) has a double pole.
Therefore every pure face with
\[
K_{N,\ell,d,I}\ne0
\tag{20}
\]
is rigorously closed before the boundary issue arises.

Algebraically, the double-pole coefficient can vanish only on
\[
\boxed{
N-\ell+d=0
\quad\text{or}\quad
I(100\ell-25N+17d)
+100\ell+25N+15d=0.
}
\tag{21}
\]
The first factor does not produce a graph characteristic.  Indeed,
it gives \(d=\ell-N\), and substitution in the characteristic
relation yields
\[
J=-\frac{3I+5}{2}<0.
\tag{22}
\]
Thus the exact unresolved locus is
\[
\boxed{
I(100\ell-25N+17d)
+100\ell+25N+15d=0.
}
\tag{23}
\]

For \(\ell=0\), combining (23) with resonance and \(0\le d\le N\)
forces
\[
\boxed{d=N,\qquad I=5,\qquad J=15.}
\tag{24}
\]
Hence the only binary pure family missed by the corrected pole
argument is \(A^N\) on the \((I,J)=(5,15)\) sector.  For \(N\ge2\),
\[
J(U,A^N)=NA^{N-1}J(U,A)
\tag{25}
\]
cannot be a nonzero constant: \(A^{N-1}\) would have to be a unit,
making \(A\) constant and the Jacobian zero.  The binary remainder
therefore reduces to the single base target \(A\).

With \(\ell>0\), the first unresolved target degree is six.  Its two
least-\(C\) pure faces are
\[
\begin{array}{c|c|c|c|c|c}
n&N&\ell&d&I&J\\ \hline
6&5&1&0&9&0\\
6&5&1&1&30&15.
\end{array}
\tag{26}
\]
They are \(CB^5\) and \(CAB^4\), respectively.  Their same-boundary
next-\(C\) counterterms include
\[
C^2A^2B^2,\qquad C^2A^3B,
\tag{27}
\]
exactly as in (15).  These degree-six families must be treated using
the full Wronskian (10).  No counterexample is asserted.

## 5. Correct scope after the audit

The following parts of the ternary argument survive:

1. exact isolation of the least-\(C\) maximal-\(x\) face;
2. exclusion of every nonpolynomial characteristic;
3. exclusion of every mixed polynomial characteristic by a nonzero
   root;
4. exclusion of every pure characteristic outside (23).

The all-degree ternary conclusion does not yet follow because the
exceptional pure locus (23) was closed only by the invalid boundary
separation.  The binary pure-face theorem that uses the same Euler
boundary step also requires this correction.

The accompanying exact audit is
`verify_weighted_lift_ternary_pure_boundary_separation_audit.py`.
