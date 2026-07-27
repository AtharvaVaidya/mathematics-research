# The diagonal conormal truncation does not survive the full case-c tail

Date: 25 July 2026

## Audited conclusion

The tempting five-row ordinary-Jacobian model

\[
X=f+ua+u^2A,\qquad
Y=g+ub+u^2c+u^3B
\]

is not the diagonal finite-support system attached to the GGHV case-c
polygons.  The correct diagonal chart has eleven \(P\)-layers and sixteen
\(Q\)-layers, and its equation is an Euler bracket rather than an ordinary
Jacobian equation.  At the first nonlinear radial row, the Laurent slices
omitted by the \(2/3\)-truncation are nonzero.  On an exact point of the
certified square branch they cancel the entire middle contribution.

Consequently the quotient \(Q=C/f'\), its completed-square discriminant,
and the proposed identification of that discriminant with
\[
\delta=Y_2-\frac{169}{48}Y_0^2
\]
are not invariants of the full case-c equations as presently defined.  The
rank-one statement which remains valid is the independently proved radial
Hamiltonian statement: after quotienting the two canonical gauge lines,
the weight-two normal coordinate is \(\delta\), and both deficit-four
compatibility rows are nonzero multiples of \(\delta^2\).

This note is a scope correction.  It does not weaken the exact bounded
certificate, which always retained all radial slices.

## 1. The correct diagonal chart

Put
\[
x=u(t+uw),\qquad y=u^{-1}.
\]
Then
\[
xy=t+uw,\qquad
\det\frac{\partial(x,y)}{\partial(u,w)}=1.
\]
For the case-c polygons define
\[
F=u^8P(x,y),\qquad G=u^{12}Q(x,y).
\]
The complete support gives
\[
F=\sum_{i=0}^{10}u^iF_i(w),\qquad
G=\sum_{j=0}^{15}u^jG_j(w).
\]
Indeed, a monomial \(x^ay^b\) contributes
\[
u^{8+a-b}(t+uw)^a
\]
to \(F\), and the analogous exponent for \(G\) is \(12+a-b\).
The maximum exponents are \(10\) and \(15\), respectively.

Because \(P=u^{-8}F\) and \(Q=u^{-12}G\), the Keller equation
\([P,Q]=x^2\) is exactly
\[
u(F_uG_w-F_wG_u)-8FG_w+12F_wG
=u^{23}(t+uw)^2. \tag{1}
\]
Thus the coefficient of \(u^n\) on the left is
\[
E_n=\sum_{i+j=n}
\left((i-8)F_iG_j'+(12-j)F_i'G_j\right). \tag{2}
\]
The target occurs only at \(n=23,24,25\), where its coefficients are
\(t^2,2tw,w^2\).  In particular, the low-order equations are not the five
rows obtained by expanding \(X_uY_w-X_wY_u\) for a \(2/3\)-truncation.

There is a useful coefficientwise form of the complete expansion.  Let
\[
p_r(Z)=\sum_{b-a=8-r}p_{ab}Z^a,\qquad
q_r(Z)=\sum_{b-a=12-r}q_{ab}Z^a.
\]
Here \(0\le r\le9\) for \(P\) and \(0\le r\le13\) for \(Q\).  Taylor
expansion at \(Z=t\) gives
\[
\begin{aligned}
F_n(w)&=\sum_{r\le n}
\frac{p_r^{(n-r)}(t)}{(n-r)!}w^{n-r},\\
G_n(w)&=\sum_{r\le n}
\frac{q_r^{(n-r)}(t)}{(n-r)!}w^{n-r}.
\end{aligned} \tag{3}
\]
Terms with derivative order above the polynomial degree are zero.
Formula (3), together with (2), is the exact finite-support cap system.

For reference, the \(P\)-layer degree ranges are
\[
\begin{array}{c|cccccccccc}
r&0&1&2&3&4&5&6&7&8&9\\ \hline
\deg p_r&8&8&8&7&6&5&4&3&2&1
\end{array}
\]
with \(p_9\) supported only in degree \(1\).  The \(Q\)-layer degrees are
\[
\begin{array}{c|cccccccccccccc}
r&0&1&2&3&4&5&6&7&8&9&10&11&12&13\\ \hline
\deg q_r&12&12&12&12&11&10&9&8&7&6&5&4&3&2
\end{array}
\]
with \(q_{13}\) supported only in degree \(2\).

## 2. The first nonlinear radial row has five summands

Return to the exact radial coordinates \(z=xy\), \(h=xy^2\), and write
\[
P=\sum_{r=-8}^{2}z^rP_r(h),\qquad
Q=\sum_{s=-12}^{3}z^sQ_s(h).
\]
The radial output-degree-zero row, equivalently deficit four, is
\[
\mathcal R_0=
\sum_{r+s=1}h\left(rP_rQ_s'-sP_r'Q_s\right). \tag{4}
\]
It contains exactly the five pairs
\[
(-2,3),\quad(-1,2),\quad(0,1),\quad(1,0),\quad(2,-1). \tag{5}
\]
The proposed \(2/3\)-truncation retained only the middle two pairs.
Define
\[
\begin{aligned}
M&=[P_0,Q_1]+[P_1,Q_0],\\
T&=[P_{-2},Q_3]+[P_{-1},Q_2]+[P_2,Q_{-1}].
\end{aligned} \tag{6}
\]
Then the full row is \(M+T\).

The highest endpoint coefficient illustrates why one can nearly miss the
problem.  The omitted tail has no \(h^{19}\)-term.  At \(h^{18}\), however,
it contains
\[
[h^{18}]T
=-26\,[h^8]P_{-1}\,[h^{10}]Q_2
+30\,[h^6]P_2\,[h^{12}]Q_{-1}. \tag{7}
\]
There is no polygonal or bracket identity forcing (7) to vanish.

## 3. Exact square-branch countercheck

Work over the rational outer point \(s=26839\) in
\(\mathbf F_{32003}\), one of the certified good-reduction factors.  In
canonical endpoint coordinates take
\[
Y_0=1,\qquad
Y_2=\frac{169}{48},\qquad
X_1=X_3=X_4=X_5=X_6=0.
\]
This is an exact point of the deficit-four square branch.  Reconstruct the
radial blocks through deficit four by the canonical \(C\)-mode recurrence.
Direct exact arithmetic gives
\[
M\ne0,\qquad T\ne0,\qquad M+T=0. \tag{8}
\]
More precisely, both \(M\) and \(T\) have degree \(18\) and eighteen
nonzero terms, and
\[
[h^{18}]M=-5457,\qquad [h^{18}]T=5457
\quad\text{in }\mathbf F_{32003}. \tag{9}
\]
The companion verifier checks every coefficient of \(M+T\), not only
(9).  Since \(32003\) is a good prime for the exact outer model, the
nonzero reduction also proves that the omitted tail is not an identically
zero characteristic-zero expression.

## 4. Centering at the outer quartic does not repair the truncation

For the same outer point put
\[
\mathcal E(h)=hV(h)^2-LU(h)^3,\qquad
L=\frac{v_{10}^2}{u_7^3}.
\]
The outer ODE makes \(\mathcal E\) a squarefree quartic.  The exact sample
above gives
\[
\mathcal E=
15441h^4+14388h^3+3553h^2-6746h-2249
\]
and
\[
T\bmod\mathcal E
=6521h^3+1918h^2-13412h-5808\ne0. \tag{10}
\]
Thus merely centering at a root of the outer quartic does not annihilate
the missing tail even set-theoretically.

Any future quartic-centered conormal reduction must prove additional
divisibility statements.  At minimum:

1. each of the two deficit-four cokernel functionals applied to \(T\)
   must lie in \((\mathcal E)\), so that the omitted tail vanishes at every
   centered outer point;
2. for a first-thickening argument, the transported tail and its normal
   derivative must vanish modulo \(\mathcal E^2\);
3. the face factorization used to write \(a=hf'\) must hold for the
   **full transported layers**, and \(f'\) must remain a nonzerodivisor
   with \(\gcd(f',g')=1\) in the relevant critical algebra; and
4. the resulting conormal quotient must be identified, with its unit
   normalization, with the canonical radial quotient.

None of these assertions follows from \(\mathcal E(t)=0\), the outer ODE,
or the Newton support alone.  Equation (10) disproves the first assertion
for the literal omitted tail in the simplest certified square-branch
sample.

## 5. What remains true

The canonical radial kernel theorem gives gauge directions
\[
(X_0,X_1)=(2,1),\qquad
(X_2,X_3)=\left(\frac23,1\right),
\]
and hence the gauge covectors
\[
Y_0=X_0-2X_1,\qquad
Y_2=X_2-\frac23X_3.
\]
The symbolic Hamiltonian calculation gives
\[
\kappa_k=\frac{(4k+1)^2}{16k},
\]
so \(\kappa_3=169/48\).  The exact five-point recurrence then proves that
both deficit-four rows are units times
\[
\left(Y_2-\frac{169}{48}Y_0^2\right)^2.
\]
That is the safe rank-one conormal statement.  The present audit shows
that it cannot currently be rederived from the truncated local quotient
\(C/f'\).

Companion verifier:

```text
.venv/bin/python current_context/verify_case_c_conormal_truncation_no_go.py
```
