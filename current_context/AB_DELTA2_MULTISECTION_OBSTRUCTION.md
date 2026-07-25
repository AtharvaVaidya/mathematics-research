# The degree-two elliptic multisection is impossible

Date: 24 July 2026

## Verdict

The degree-two normalization alternative for the full a/b asymptotic
component does not occur:
\[
\boxed{\delta\ne2.}
\]

The proof has two independent pieces.

1. A generalized degree-\((4,6)\) Davenport calculation classifies every
   primitive polynomial multisection for which the osculating cubic has
   restriction degree at most three.  Restriction degree two is
   impossible; degree three has one explicit two-parameter normal form.
2. A fixed-pole fourth-jet lemma says that the marked normalization
   branch at \(w=0\) must be nonimmersive.  The Davenport normal form is
   immersive everywhere.

No broad Gröbner elimination is used.

## 1. A fixed-pole immersion obstruction

Write the original five-block pair as
\[
\begin{aligned}
P&=p_0+p_1z+p_2z^2,\\
Q&=q_0+q_1z+q_2z^2+q_3z^3,
\end{aligned}
\]
where
\[
\boxed{
p_1,q_1,q_2\in\mathbf C[w],\qquad
p_2=A_2(w)+\frac1w,\qquad
q_3=B_3(w)+\frac1w.
}
\tag{1}
\]
Suppose
\[
p_0=A(h(w)),\qquad q_0=B(h(w))
\]
is a polynomial normalization of the boundary curve, and put
\(h_0=h(0)\).

Assume first that \(A'(h_0)\ne0\).  Over \(\mathbf C(w)\), the boundary
is locally the graph
\[
Q=g(P),\qquad g(A(h))=B(h).
\]
Set \(N=Q-g(P)\).  The exact identity
\[
\{P,N\}=\{P,Q\}=\frac{z^4}{w^3}
\]
and \(p_0'\ne0\) in \(\mathbf C(w)\) show that
\[
N=O(z^5).
\]
Consequently the coefficients through order four are
\[
\begin{aligned}
q_1&=g'p_1,\\
q_2&=g'p_2+\frac12g''p_1^2,\\
q_3&=g''p_1p_2+\frac16g'''p_1^3,\\
0&=\frac12g''p_2^2
  +\frac12g'''p_1^2p_2
  +\frac1{24}g''''p_1^4,
\end{aligned}
\tag{2}
\]
with the derivatives evaluated at \(p_0=A(h(w))\).

The fixed pole of \(q_3\) in (1) forces
\[
g''(A(h_0))\,p_1(0)\ne0:
\]
it is the only possible coefficient of \(w^{-1}\) in the third equation
of (2).  But then the last equation has the uncancelled term
\[
\frac12g''(A(h_0))\frac1{w^2}.
\]
The other two terms have pole orders at most one and zero.  This is a
contradiction.

If \(A'(h_0)=0\) but \(B'(h_0)\ne0\), write the boundary instead as
\[
P=f(Q),\qquad f(B(h))=A(h).
\]
Again \(P-f(Q)=O(z^5)\).  Its second coefficient is
\[
p_2=f'q_2+\frac12f''q_1^2.
\tag{3}
\]
At \(w=0\),
\[
f'(B(h_0))=\frac{A'(h_0)}{B'(h_0)}=0.
\]
Because \(q_1,q_2\) are polynomial, the right side of (3) is regular.
This contradicts the fixed \(w^{-1}\) term in \(p_2\).

We have proved the general lemma
\[
\boxed{
\text{every full a/b boundary must satisfy }
A'(h_0)=B'(h_0)=0.
}
\tag{4}
\]
Thus the marked normalization point must be a cuspidal, rather than an
immersed, branch of the boundary curve.

## 2. Generalized Davenport classification in degrees \((4,6)\)

Now assume \(\delta=2\).  The normalization has
\[
\deg A=4,\qquad\deg B=6,
\]
and the osculating theorem gives
\[
\deg_h\mathcal H(A,B)\le3.
\]

Complete the square in \(Y\), translate \(X\) to remove the quadratic
term of the cubic, rescale the leading coefficients, and translate the
normalization parameter to center \(A\).  These are invertible affine
changes and preserve primitivity and immersion.  We may write
\[
\begin{aligned}
A&=h^4+a_2h^2+a_1h+a_0,\\
B&=h^6+b_5h^5+\cdots+b_0,\\
\mathcal H&=Y^2-X^3+uX+v.
\end{aligned}
\tag{5}
\]

Canceling degrees \(11,10,\ldots,6\) in \(B^2-A^3\) determines
\[
\begin{aligned}
b_5&=0,&
b_4&=\frac32a_2,&
b_3&=\frac32a_1,\\
b_2&=\frac32a_0+\frac38a_2^2,&
b_1&=\frac34a_1a_2,&
b_0&=\frac34a_0a_2+\frac38a_1^2-\frac1{16}a_2^3.
\end{aligned}
\tag{6}
\]
If \(a_1=0\), both \(A\) and \(B\) are polynomials in \(h^2\), contrary
to
\[
\mathbf C(A,B)=\mathbf C(h).
\]
Hence \(a_1\ne0\).

The degree-five coefficient is
\[
-\frac38a_1(4a_0-a_2^2),
\]
so the bound \(\deg\mathcal H(A,B)\le3\) forces
\[
a_0=\frac14a_2^2.
\]
The degree-four coefficient uniquely sets
\[
u=-\frac38a_1^2a_2.
\]
After these substitutions the restriction is exactly
\[
\boxed{
\mathcal H(A,B)
=\frac18a_1^3h^3
+\frac3{16}a_1^3a_2h
+\frac9{64}a_1^4+v.
}
\tag{7}
\]
In particular its degree is three, not two.

Writing \(a=a_1\ne0\) and \(b=a_2\), the complete normal form is
\[
\boxed{
\begin{aligned}
A={}&h^4+bh^2+ah+\frac14b^2,\\
B={}&h^6+\frac32bh^4+\frac32ah^3
       +\frac34b^2h^2+\frac34abh+\frac18(b^3+3a^2).
\end{aligned}}
\tag{8}
\]
A direct resultant calculation gives
\[
\boxed{\operatorname{Res}_h(A',B')=-1728a^5\ne0.}
\tag{9}
\]
Thus the normalization is immersive at every finite \(h\), contradicting
the necessary condition (4).  This proves \(\delta\ne2\).

## 3. Exact curve-level countermodel and scope

The cubic degree in (7) is genuinely attainable before the transverse
five-block poles are imposed.  Take
\[
a=1,\qquad b=0,\qquad v=0.
\]
Then
\[
A=h^4+h,\qquad
B=h^6+\frac32h^3+\frac38,
\]
and
\[
B^2-A^3=\frac18h^3+\frac9{64}.
\]
Moreover \(h\in\mathbf C(A,B)\): the right side determines \(h^3\), and
\(A=h(h^3+1)\).  Composing with \(h=w^2\) gives polynomial boundary
degrees \((8,12)\) and parametrization degree exactly two.

This example shows why curve contact, genus, and the elliptic pencil alone
do not exclude \(\delta=2\).  The contradiction genuinely uses both
fixed transverse poles \(z^2/w\) and \(z^3/w\).

## 4. Remaining branch

The a/b normalization degree is now forced to be
\[
\boxed{\delta=1.}
\]
By the immersion lemma, its marked point \(w=0\) must be a cuspidal point
of the degree-twelve boundary curve.  This is the next finite geometric
target.
