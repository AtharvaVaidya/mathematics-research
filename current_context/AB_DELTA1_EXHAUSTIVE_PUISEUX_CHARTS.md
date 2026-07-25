# Exhaustive pole-sensitive Puiseux chart table for \(\delta=1\)

Date: 24 July 2026

## 1. Result

Let
\[
A=p_0,\qquad B=q_0,\qquad
\deg A=8,\quad\deg B=12,
\]
and suppose
\[
A'(0)=B'(0)=0.
\]
Keep the original five-block pole allocation
\[
p_2=w^{-1}+O(1),\qquad
q_3=w^{-1}+O(1),\qquad
p_1,q_1,q_2\in\mathbf C[w].
\]

The local projection charts reduce to the following table.

| Projection chart | Outcome |
|---|---|
| Nonzero tangent | impossible |
| Vertical tangent / opposite projection | impossible |
| Horizontal, leading nonintegral exponent \(1<\lambda<2\) | \((m,n)=(3,5),(5,8),(7,11)\) survive |
| Horizontal, leading nonintegral exponent \(\lambda\ge2\) | impossible |
| Horizontal, analytic order at least three | impossible |
| Horizontal, nonzero analytic quadratic term | only \((m,N)=(3,10),(4,14)\) survive the degree caps |

Here \(m=\operatorname{ord}_0(A-A(0))\).  In the last line, \(N\) is
the order of the first nonanalytic term after the analytic quadratic
and cubic terms have been removed.

Thus the complete marked-cusp problem is reduced to five explicit cells:
\[
\boxed{
(3,5),\ (5,8),\ (7,11),\
(m,N)=(3,10),\ (4,14).
}
\]
The first three have exact local five-block countermodels, as recorded in
`AB_DELTA1_CUSP_JET_CLASSIFICATION.md`.  The last two have primitive
degree-\((8,12)\) boundary parametrizations, but no five-block lift is
claimed here.

## 2. Taylor identities in the \(A\)-projection

Write \(x=A-A(0)\) and \(B=g(x)\) on the chosen Puiseux branch.  The
five-block equations give
\[
\begin{aligned}
q_2&=g'p_2+\frac12g''p_1^2,\\
q_3&=g''p_1p_2+\frac16g'''p_1^3,\\
0&=\frac12g''p_2^2
+\frac12g'''p_1^2p_2
+\frac1{24}g''''p_1^4.
\end{aligned}
\tag{1}
\]

### Nonzero tangent

If
\[
g(x)=\kappa x+c x^{n/m}+\cdots,
\qquad \kappa c\ne0,\quad m<n<2m,
\]
the polynomiality of \(q_2\) forces
\[
n-2m+2r=-1,\qquad r=\operatorname{ord}_0p_1.
\]
The last identity of (1) has three valuations in arithmetic progression,
so it forces \(2r=m-1\).  Together these say \(n=m\), a contradiction.
If the first nonanalytic exponent is at least two, \(g''p_1^2\) is
regular and cannot cancel the fixed pole \(\kappa p_2\) in \(q_2\).
Thus every nonzero-tangent chart is impossible.

### Leading nonintegral horizontal tangent

Suppose
\[
g(x)=c x^{n/m}+\cdots,\qquad n>m,
\]
with no preceding analytic term.  If the exponent is nonintegral, the
three fourth-jet valuations are
\[
n-2m-2,\quad
n-3m+2r-1,\quad
n-4m+4r.
\]
Their cancellation forces \(2r=m-1\).  The two terms of \(q_3\) then
have the same valuation, and their leading coefficient cannot vanish
simultaneously with the fourth-jet coefficient.  The fixed pole of
\(q_3\) therefore forces
\[
2n=3m+1.
\]
In particular \(\lambda=n/m<2\).  The degree caps leave exactly
\[
(m,n,r)=(3,5,1),(5,8,2),(7,11,3).
\]
This both recovers the earlier three cells and rules out all leading
nonintegral exponents at least two.

## 3. Vertical tangent is impossible

Put
\[
y=B-B(0),\qquad
n=\operatorname{ord}_0y<m=\operatorname{ord}_0(A-A(0)),
\]
and use the inverse graph \(A=f(y)\).  Write
\[
s=\operatorname{ord}_0q_1,\qquad
t=\operatorname{ord}_0q_2\ge0.
\]
Expansion of \(P=f(Q)\) begins with
\[
\begin{aligned}
p_2&=f'q_2+\frac12f''q_1^2,\\
0&=f'q_3+f''q_1q_2+\frac16f'''q_1^3.
\end{aligned}
\tag{2}
\]
The first term in the \(p_2\) equation is regular.  Its fixed pole can
only come from the second term, so the leading inverse exponent must lie
strictly between one and two and
\[
m-2n+2s=-1.
\tag{3}
\]
After substituting (3), the three valuations in the second equation of
(2) are
\[
m-n-1,\qquad
m-2n+s+t,\qquad
m-3n+3s.
\]
The first exceeds the third by
\[
\frac{3m-2n+1}{2}>0,
\]
and the second exceeds the third by
\[
m-n+t+1>0.
\]
Thus the \(f'''q_1^3\) term has a unique lowest valuation, impossible.
If the inverse graph begins with an analytic quadratic or higher term,
\(f''q_1^2\) is regular and cannot supply the pole of \(p_2\).  Hence
every vertical chart is excluded.

## 4. The analytic-quadratic exception

The remaining horizontal possibility is
\[
g(x)=c_2x^2+c_3x^3+c\,x^{N/m}+\cdots,
\qquad c_2c\ne0,
\]
where \(N/m>3\) is the first nonintegral exponent.  Since \(g''(0)\ne0\),
the fixed pole in \(q_3\) forces
\[
\operatorname{ord}_0p_1=0.
\]
In the fourth-jet identity, the analytic term \(g''p_2^2\) has valuation
\(-2\).  The only possible competing singular term is
\(g''''p_1^4\), of valuation \(N-4m\).  Therefore
\[
\boxed{N=4m-2.}
\tag{4}
\]
If the first nonanalytic exponent were below three, the \(g'''\)-term in
\(q_3\) would create a lower unmatched pole; if it were at least four,
the analytic \(-2\) term would be unique.  If the analytic graph starts
in degree at least three, neither term of \(q_3\) can have a pole.

Subtracting \(c_2A^2+c_3A^3\) gives a nonzero polynomial of degree at
most \(24\), so \(N\le24\).  Equation (4) initially leaves
\[
(m,N)=(3,10),(4,14),(5,18),(6,22).
\]
The last two are incompatible with \(\deg A=8,\deg B=12\).  After
nonzero source and target scalings:

* for \(m=5\), put
  \(A=w^5+a_6w^6+a_7w^7+w^8\); vanishing of the coefficients of
  \(A^2+c_3A^3\) in degrees \(13,\ldots,17\) generates the unit ideal;
* for \(m=6\), put
  \(A=w^6+a_7w^7+w^8\); the analogous coefficients in degrees
  \(13,\ldots,21\) generate the unit ideal.

The two surviving cells are nonempty even with exact global degree caps:
\[
\begin{array}{c|c|c|c}
m&A&B&\operatorname{ord}_0(B-A^2)\\ \hline
3&w^3+w^7+w^8&w^6+w^{12}&10\\
4&w^4+w^7+w^8&w^8+2w^{11}+2w^{12}&14.
\end{array}
\]
For these two rows,
\[
\gcd(A',B')=w^{m-1},
\]
and the resultants after removing this factor are respectively
\[
21128962752,\qquad 1310720.
\]
The presence of the \(w^7\) term rules out a common polynomial right
factor, so both boundary parametrizations are primitive.

These are curve-level population witnesses only.  They do not satisfy,
as far as currently proved, the osculating-cubic remainder condition or
the remaining five-block identities.

## 5. Next finite global problem

The local problem is no longer an open-ended Puiseux search.  The next
step is to impose
\[
\mathcal H(A,B)=G,\qquad \deg G\le7,
\]
separately on the five cells above, while retaining the marked point
instead of also translating away the \(h^7\) coefficient of \(A\).
Each cell imposes several low-order zero conditions and should reduce the
global approximate-root equations to a small exact system.  This is much
sharper than classifying every primitive degree-\((8,12)\) pair.
