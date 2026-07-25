# Case-c integral cokernel and the status of \(c_8\)

## Conclusion

The low-grade integral system has two different notions of a “first
nonlinear row.”

1. The first nonzero internal bracket occurs at grade \(n=2\).  It
   determines \(q_3\), hence the last new remainder coefficient \(S_3\).
2. The first row with no new \(S_j\) is \(n=3\); this is the first
   compatibility row in the integral variables.
3. The first **Newton-degree cokernel** does not occur until \(n=9\).
   It is one-dimensional and is represented by the coefficient
   \([z^{13}]\).

The \(c_8\) support-cost monomial has zero class in this cokernel—and in
every Euler cokernel.  Thus it cannot be killed by a residue argument of
this kind.

The first residue is not a contradiction.  It is a genuine scalar
condition: it vanishes on some required-vertex faces and is nonzero on
others.  In fact it is exactly the first unsolved coefficient of the
already-known outer-face Bezout equation.

## 1. First nonzero internal row

After the \(c_4\) translation and the external \(c_8\) shear, write
\[
P=\frac zy+\sum_{m=0}^8p_m(z)y^m,\qquad
Q=\frac{z(z-c_8)}y+\sum_{m=0}^{12}q_m(z)y^m.
\]
The bottom rows give
\[
q_0'=(z-c_8)p_0',\qquad q_1=(z-c_8)p_1,
\]
and
\[
q_2=\sum_{k=0}^4 [z^k]p_2
\left(\frac{k+4}{k+3}z^{k+1}-c_8z^k\right).
\]
Consequently the internal term at \(n=1\) is zero.  The first nonzero
one is
\[
\begin{aligned}
\mathcal I_2
&=2p_0'q_2+p_1'q_1-p_1q_1'-2p_2q_0'\\
&=\boxed{
2z\,p_0'(D+3)^{-1}p_2-p_1^2,
}
\end{aligned}
\]
where \(D=z\,d/dz\).  This term is independent of \(c_8\).  The
\(n=2\) equation is an invertible Euler equation for \(q_3\), so in the
integral normal form it determines the last new coefficient \(S_3\).
The next row, \(n=3\), is therefore the first row with no new \(S_j\).

## 2. Exact degree-cokernel inventory

Let
\[
d_m=\deg p_m=\min(m+2,8),\qquad
e_m=\deg q_m=\min(m+3,12).
\]
At grade \(n=m-1\), the Euler operator is
\[
L_m(q)=zq'+mq.
\]
The base source has degree at most \(d_m+1\), and an internal term
formed from \(p_i,q_j\), \(i+j=m-1\), has degree at most
\[
d_i+e_j-1.
\]
These bounds do not exceed \(e_m\) for \(0\le m\le9\).  The first three
excesses are
\[
\begin{array}{c|c|c|c}
m&\text{source cap}&e_m&\dim\operatorname{coker}L_m\\ \hline
10&13&12&1\\
11&14&12&2\\
12&15&12&3.
\end{array}
\]
Thus the first degree-cap residue is at \(n=9\), represented by
\([z^{13}]\).

## 3. Exact first residue

Only the outer Newton faces contribute.  Put
\[
p_i=\alpha_i z^{i+2}\quad(0\le i\le6),\qquad
q_j=\beta_j z^{j+3}\quad(0\le j\le9).
\]
Then
\[
\boxed{
[z^{13}]\mathcal I_9
=\sum_{i=0}^6(18-5i)\alpha_i\beta_{9-i}.
} \tag{1}
\]

Set \(h=xy^2\), and write the outer faces as
\[
P^{(2)}=xU(h),\qquad Q^{(3)}=x^2yV(h),
\]
with
\[
\deg U=7,\quad \deg V=10,\quad U(0)=V(0)=1.
\]
The outer equation is
\[
\boxed{
UV+2hUV'-3hU'V=1.
} \tag{2}
\]
Under
\(\alpha_i=[h^{i+1}]U\) and
\(\beta_j=[h^{j+1}]V\), expression (1) is exactly
\([h^{11}]\) of the left side of (2).

The coefficients through \(h^{10}\) solve recursively for \(V\):
\[
[h^k]V=
-\frac1{2k+1}
\sum_{i=1}^{\min(7,k)}
(1+2k-5i)[h^i]U\,[h^{k-i}]V.
\]
Because \(V\) has no \(h^{11}\) term, \(h^{11}\) is the first
compatibility condition.

It is genuine rather than automatic or forced nonzero.  For
\[
U=1+bh^7,\qquad b\ne0,
\]
the residue is zero.  For
\[
U=1+ah^4+bh^7,\qquad ab\ne0,
\]
the recursively determined \(V\) gives
\[
[h^{11}](UV+2hUV'-3hU'V-1)
=-\frac{32}{3}ab\ne0.
\]

## 4. Why \(c_8\) has zero residue

At grade \(n=m-1\), changing the sheared base from \(z^2/y\) to
\(z(z-c_8)/y\) changes the equation by
\[
\begin{aligned}
&-z(z-c_8)p_m'-m(2z-c_8)p_m
-\bigl(-z^2p_m'-2mz\,p_m\bigr)\\
&\qquad
=c_8\left(zp_m'+mp_m\right)
=\boxed{c_8L_m(p_m)}.
\end{aligned}
\]
For every grade where \(p_m\) exists, this is in the Euler image.  At
the first cokernel \(m=10\), \(p_{10}=0\), so \(c_8\) is absent
altogether.

The same fact is visible on the next Newton face.  If
\[
P^{(2)}=y^{-2}A(h),\qquad Q^{(2)}=y^{-2}D(h),
\]
then the relevant operator is
\[
\mathcal L_A(D)=2(AD'-A'D).
\]
The shear introduces the missing \(h\)-monomial, but \(A-h\) is
supported in the allowed positive face and
\[
\mathcal L_A(h)=-\mathcal L_A(A-h).
\]
Hence the missing monomial represents zero in the restricted cokernel.

This closes the residue route for \(c_8\): any argument that kills
\(c_8\) must use a different invariant, not an Euler/outer-face
cokernel.

## Reproduction

```sh
python3 route_bd_case_c_integral_cokernel.py
```
