# The surviving birational boundary has a marked cusp

Date: 24 July 2026

## Current theorem and scope

The osculating-cubic and fixed-pole arguments eliminate
\(\delta=4\) and \(\delta=2\).  Hence the full a/b boundary, if it
existed, would be birationally parametrized:
\[
\boxed{\delta=1.}
\]
Choose its normalization parameter to be \(w\), and write
\[
p_0=A(w),\qquad q_0=B(w),\qquad
\deg A=8,\quad\deg B=12.
\]
The fixed-pole immersion lemma proves
\[
\boxed{A'(0)=B'(0)=0.}
\]
Thus the marked source corner \(w=0\) must map to a cuspidal branch of
the boundary curve.

This memo classifies the first nonintegral Puiseux chart
\[
1<\frac nm<2,
\qquad
m=\operatorname{ord}_0(A-A(0)),
\quad
n=\operatorname{ord}_0(B-B(0)).
\]
In that chart the first four five-block identities leave exactly
\[
\boxed{(m,n)=(3,5),(5,8),(7,11).}
\]
All three types admit exact local five-block solutions with
\(\{P,Q\}=z^4/w^3\).  Therefore the local jets do not finish the
\(\delta=1\) branch.

The scope qualification is essential.  Charts with an integral analytic
part in \(B(A)\), or with the opposite projection as the first usable
graph coordinate, require a separate audit.  The result below is a
finite, exact subcase theorem, not a complete elimination of
\(\delta=1\).

## 1. Valuation classification

Work in the original five-block coordinates
\[
\begin{aligned}
P&=p_0+p_1z+p_2z^2,\\
Q&=q_0+q_1z+q_2z^2+q_3z^3,
\end{aligned}
\]
with
\[
p_1,q_1,q_2\in\mathbf C[w],\qquad
p_2=\frac1w+O(1),\qquad
q_3=\frac1w+O(1).
\]
In the stated Puiseux chart,
\[
B-B(0)=\gamma(A-A(0))^\lambda+\cdots,
\qquad
\lambda=\frac nm,\quad1<\lambda<2.
\]
Let
\[
r=\operatorname{ord}_0p_1.
\]
The fixed pole of \(q_3\) implies \(p_1\ne0\).

As in the immersion lemma, over \(\mathbf C(w)\) one has
\[
Q-g(P)=O(z^5),
\]
where \(g(A(w))=B(w)\).  Therefore
\[
\begin{aligned}
q_3&=g''p_1p_2+\frac16g'''p_1^3,\\
0&=\frac12g''p_2^2
  +\frac12g'''p_1^2p_2
  +\frac1{24}g''''p_1^4.
\end{aligned}
\tag{1}
\]
Because \(1<\lambda<2\), the leading coefficients of
\(g'',g''',g''''\) are all nonzero, and
\[
\operatorname{ord}_0 g^{(j)}=n-jm.
\]
The three valuations in the second equation of (1) are
\[
\begin{aligned}
E_1&=n-2m-2,\\
E_2&=n-3m+2r-1,\\
E_3&=n-4m+4r.
\end{aligned}
\]
Their consecutive differences are equal:
\[
E_2-E_1=E_3-E_2=2r-(m-1).
\]
If this number were positive or negative, the sum would have a unique
lowest-valuation term and could not vanish.  Hence
\[
r=\frac{m-1}{2}.
\tag{2}
\]
The two terms in the first equation of (1) then have equal valuation.
Since \(q_3\) has exact order \(-1\), one obtains
\[
n-2m+r-1=-1,
\]
and therefore
\[
\boxed{2n=3m+1.}
\tag{3}
\]

Thus \(m\) is odd.  The degree caps \(m\le8,n\le12\), together with
\(1<n/m<2\), leave exactly
\[
\boxed{(m,n,r)=(3,5,1),(5,8,2),(7,11,3).}
\]

## 2. Exact local five-block countermodels

The three valuation types are genuinely compatible with the complete
five-block bracket, not only with its leading valuation.

Let \(m\in\{3,5,7\}\), and put
\[
n=\frac{3m+1}{2},\qquad
r=\frac{m-1}{2},\qquad
\lambda=\frac nm.
\]
Choose \(C\ne0\) satisfying
\[
\boxed{
12+12(\lambda-2)C^2
+(\lambda-2)(\lambda-3)C^4=0.
}
\tag{4}
\]
The quadratic in \(C^2\) has complex roots.  None makes
\[
\lambda(\lambda-1)C
\left(1+\frac{\lambda-2}{6}C^2\right)
\]
zero.  Hence choose \(b\ne0\) so that
\[
b\lambda(\lambda-1)C
\left(1+\frac{\lambda-2}{6}C^2\right)=1.
\tag{5}
\]

Define
\[
\begin{aligned}
P={}&w^m+Cw^rz+\frac{z^2}{w},\\
Q={}&b\Bigg[
w^n+\lambda Cw^mz\\
&\quad+\lambda\left(1+\frac{\lambda-1}{2}C^2\right)w^rz^2\\
&\quad+\lambda(\lambda-1)C
\left(1+\frac{\lambda-2}{6}C^2\right)\frac{z^3}{w}
\Bigg].
\end{aligned}
\tag{6}
\]
Equation (4) is exactly the vanishing of the unwanted fourth Taylor
coefficient.  Direct differentiation then gives
\[
\boxed{\{P,Q\}_{z,w}=\frac{z^4}{w^3}.}
\tag{7}
\]
Condition (5) simultaneously normalizes the fixed \(z^3/w\) coefficient
and the right side of (7).

These models have boundary degrees \((m,n)\), not the required
\((8,12)\), and their outer coefficients \(a_2,b_3\) vanish.  They are
not candidates for the full GGHV system.  Their role is exact and
negative: the critical exponent four, the two fixed poles, and the
first Puiseux data do not by themselves exclude the three cusp types.

## 3. Strongest next global input

The outer endpoints alone describe behavior at the other end
\(w=\infty\).  They do not directly couple to the marked cusp at \(w=0\);
high-degree terms can be added to a boundary parametrization without
changing its first Puiseux pair.  A proof based only on the endpoint
vertices is therefore unlikely to distinguish the exact local models
above.

The stronger global datum is the osculating relation
\[
\mathcal H(A(w),B(w))=G(w),\qquad \deg G\le7,
\]
for primitive degrees \((8,12)\).  It couples the marked cusp to the
contact of order at least \(29\) with a smooth cubic at infinity.  The
appropriate next problem is a generalized Davenport classification:

> classify primitive degree-\((8,12)\) pairs with generalized
> Weierstrass remainder of degree at most seven and with a marked
> nonimmersive point.

This is a finite approximate-root/Hurwitz problem.  It uses the genuinely
global invariant supplied by the osculating theorem while avoiding a
search through all five-block coefficients.
