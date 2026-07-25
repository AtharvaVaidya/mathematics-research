# Case-c integral normal form and the thirteen remaining ODEs

## 1. Exact positive-part identity

After the universal fractional descent,
\[
P_+=H^2+R,\qquad
Q_+=H^3+\frac32HR+c_8P_++c_4H+S,
\qquad
\deg_yR,\deg_yS\le3.
\]
For the transformed case-c bracket
\[
\langle A,B\rangle
=y\left(A_zB_y-A_yB_z\right),
\]
one has the exact identity
\[
\boxed{
\langle P_+,Q_+\rangle
=\langle P_+,S\rangle
-\left(\frac32R+c_4\right)\langle H,R\rangle .
} \tag{1}
\]
The \(c_8P_+\) term disappears because it is central.

## 2. The two integral modes have different status

The term \(c_4H\) is removable **inside** the normalized GGHV slice.
Set
\[
\lambda=\frac{2c_4}{3},\qquad
\widetilde P=P+\lambda,\qquad
\widetilde R=R+\lambda,\qquad
\widetilde S=S-c_8\lambda.
\]
Then
\[
Q_+
=H^3+\frac32H\widetilde R+c_8\widetilde P+\widetilde S.
\]
Only the allowed constant coefficient of \(P\) changes, so this target
translation preserves the case-c support.

The \(c_8\) mode is also removable as a Keller pair by the target shear
\[
\widetilde Q=Q-c_8P,
\]
but not inside the normalized slice.  The unique \(P\)-support point
missing from the \(Q\)-support is
\[
(1,0),
\]
so the shear introduces precisely that monomial into \(Q\).

It is nevertheless useful to make the shear for invariant analysis.  The
fixed negative blocks become
\[
P_-=\frac z y,\qquad
\widetilde Q_-=\frac{z(z-c_8)}y,
\]
and still satisfy
\[
\langle P_-,\widetilde Q_-\rangle=\frac{z^2}{y^2}.
\]

## 3. Thirteen reduced equations

After the slice-preserving \(c_4\) translation and the external \(c_8\)
shear, write
\[
P=\frac zy+P_+,\qquad
Q=\frac{z(z-c_8)}y+
H^3+\frac32HR+S.
\]
Put
\[
p_j=[y^j]P_+,\qquad
q_j=\left[y^j\right]\left(H^3+\frac32HR+S\right)
\]
and
\[
\mathcal I
=\langle P_+,S\rangle-\frac32R\langle H,R\rangle .
\]
After the grade-\(-2\) target is removed, the entire case-c equation is
equivalent to the thirteen ODEs, for \(-1\le n\le11\),
\[
\boxed{
zq_{n+1}'+(n+1)q_{n+1}
-z(z-c_8)p_{n+1}'
-(n+1)(2z-c_8)p_{n+1}
+[y^n]\mathcal I=0,
} \tag{2}
\]
where the last term is zero for \(n=-1\), and absent coefficients are
read as zero.

This is the exact remaining system in invariant variables: five
coefficients of \(H\), four of \(R\), four of \(S\), and the one constant
\(c_8\), with their already-known support bounds.  It replaces the raw
186-coefficient presentation.

## 4. The bottom two rows are not the obstruction

For \(n=-1\), (2) is
\[
zq_0'-z(z-c_8)p_0'=0.
\]
If
\[
p_0=a_0+a_1z+a_2z^2,
\]
the complete degree-capped solution is
\[
q_0=C-a_1c_8z+
\left(\frac{a_1}{2}-a_2c_8\right)z^2
+\frac{2a_2}{3}z^3.
\]

For \(n=0\), the internal bracket vanishes identically and
\[
\left(zq_1-z(z-c_8)p_1\right)'=0.
\]
Polynomiality at \(z=0\) gives
\[
\boxed{q_1=(z-c_8)p_1.} \tag{3}
\]
Every polynomial \(p_1\) of degree at most three gives a \(q_1\) of
degree at most four, exactly matching the case-c caps.

The apparently first nonlinear internal term also vanishes.  Directly
in the \(p_j,q_j\) coefficients,
\[
[y^1]\langle P_+,Q_+\rangle=p_0'q_1-p_1q_0'.
\]
Equations (3) and the \(n=-1\) row give
\[
q_1=(z-c_8)p_1,\qquad q_0'=(z-c_8)p_0',
\]
so this expression is identically zero.  Consequently the \(n=1\) row
is another invertible Euler equation:
\[
zq_2'+2q_2=z(z-c_8)p_2'+2(2z-c_8)p_2.
\]
For \(p_2=\sum_{k=0}^4b_kz^k\), its complete solution is
\[
\boxed{
q_2=\sum_{k=0}^4b_k\left(
\frac{k+4}{k+3}z^{k+1}-c_8z^k
\right),
}
\]
which has degree at most five, exactly the allowed cap.

Therefore the lowest three equations cannot provide the contradiction.
A successful continuation must use grade \(n=2\) or higher, or a global
invariant coupling several equations.  More importantly, the direct
coefficient recurrence shows why a row-by-row low-end brute-force
attack is unlikely to pay off: its Euler operator is invertible and its
degree bound is not yet tight.

## Reproduction

```sh
python3 route_bd_case_c_integral_normal_form.py
```
