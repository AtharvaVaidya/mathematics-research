# Primitive global marked pairs exist, but their tangent cusps cannot lift

Date: 24 July 2026

## 1. Outcome

The proposed global shortcut does not work:

> A primitive degree-\((8,12)\) parametrization can have both a generalized
> Weierstrass remainder of degree at most seven and a marked nonimmersive
> point.

There are exact examples with remainder of degree exactly seven.  They
have an ordinary \((2,3)\) cusp at the marked point.  Thus neither
polynomial \(abc\), the contact order at infinity, nor primitivity alone
eliminates the remaining \(\delta=1\) boundary.

The fixed-pole five-block structure does eliminate these examples.  More
generally, it eliminates the whole missing chart in which the cusp has a
nonzero tangent and its first nonanalytic Puiseux exponent lies strictly
between one and two.

This turns the global computation into a useful diagnostic: the decisive
information is the asymmetry
\[
p_2=w^{-1}+O(1),\qquad q_2\in\mathbf C[w],
\]
not just the osculating cubic.

## 2. Exact generalized-Davenport countermodels

Work over
\[
K=\mathbf Q(r,t),\qquad
r^3=t,\qquad
512000000t^2-13257900t-177147=0.
\]
Equivalently,
\[
t=\frac{132579\mathbin{\pm}14949\sqrt{241}}{10240000}.
\]
Set
\[
\begin{aligned}
A={}&h^8+h^5+rh^4
+\frac{5r^2(35840000t-591093)}{403623}h^3\\
&+\frac{128000t-3339}{29898}h^2
+\frac{4r^2(1600000t-34263)}{44847},
\end{aligned}
\]
and
\[
\begin{aligned}
B={}&h^{12}+\frac32h^9+\frac32rh^8
+\frac{5r^2(35840000t-591093)}{269082}h^7\\
&+\frac{256000t+8271}{39864}h^6+\frac34rh^5\\
&+\frac{r^2(588800000t-10441179)}{1076328}h^4
+\frac{1264000t-6189}{199320}h^3\\
&+\frac{r(512000t-6561)}{14496}h^2
-\frac{1359632t-19683}{637824}.
\end{aligned}
\]

Direct reduction in \(K\) gives
\[
D:=B^2-A^3,\qquad \deg D=8,
\]
and the coefficients of \(h^{11},h^{10},h^9,h\) vanish.  Its leading
coefficient is
\[
[h^8]D=-\frac{19r(512000t-6561)}{579840}.
\]
Therefore, with
\[
u=\frac{19r(512000t-6561)}{579840},
\qquad
\mathcal H(X,Y)=Y^2-X^3+uX,
\]
one has
\[
\deg\mathcal H(A,B)=7.
\]
The degree-seven coefficient is
\[
\frac{r^2(5120000t-836163)}{1913472}\ne0.
\]
Also \(u\ne0\), so the Weierstrass cubic is smooth.

Both derivatives vanish at the marked point:
\[
A'(0)=B'(0)=0.
\]
After removing the common factor \(h\), their resultant is
\[
\operatorname{Res}_h\left(\frac{A'}h,\frac{B'}h\right)
=-\frac{2592}{648828125}
\left(33187589620394900t+273822469190757\right)\ne0.
\]
Hence \(\gcd(A',B')=h\).  If \(A\) and \(B\) had a common polynomial
right factor of degree \(e>1\), then \(e\mid\gcd(8,12)\) and the
derivative of that factor would divide \(h\).  Thus only \(e=2\) could
remain, but then the inner polynomial would be affine in \(h^2\), while
\([h^5]A=1\).  Consequently
\[
\boxed{K(A,B)=K(h).}
\]

The marked branch has a nonzero tangent.  Subtracting that tangent makes
the first surviving term cubic, while \(A-A(0)\) starts quadratically.
It is an ordinary cusp of type \((2,3)\).

## 3. Fixed-pole obstruction for the tangent chart

Let
\[
x=A-A(0),\qquad \operatorname{ord}_0x=m,
\]
and suppose the branch has the Puiseux expansion
\[
B-B(0)=\kappa x+c\,x^{n/m}+\cdots,
\qquad
\kappa c\ne0,\qquad m<n<2m.
\]
Let \(g\) denote this Puiseux graph and put
\[
r=\operatorname{ord}_0p_1.
\]
The five-block Taylor identities include
\[
\begin{aligned}
q_2&=g'p_2+\frac12g''p_1^2,\\
0&=\frac12g''p_2^2
+\frac12g'''p_1^2p_2
+\frac1{24}g''''p_1^4.
\end{aligned}
\tag{1}
\]
Because \(g'\) has the nonzero constant term \(\kappa\) and
\(p_2=w^{-1}+O(1)\), the first term of \(q_2\) has valuation \(-1\).
The other term has valuation
\[
n-2m+2r.
\]
Since \(q_2\) is polynomial, these poles must cancel:
\[
n-2m+2r=-1.
\tag{2}
\]

The three valuations in the second identity of (1) are
\[
n-2m-2,\qquad
n-3m+2r-1,\qquad
n-4m+4r.
\]
They form an arithmetic progression with common difference
\[
2r-m+1.
\]
If this difference were nonzero, the sum would have a unique
lowest-valuation term.  Hence
\[
2r=m-1.
\tag{3}
\]
Substituting (3) into (2) gives \(n=m\), contrary to \(n>m\).
Therefore
\[
\boxed{\text{the nonzero-tangent cusp chart cannot occur.}}
\]

In particular, the exact global \((2,3)\) countermodels above do not lift
to a five-block pair.

## 4. Strategic implication

The global generalized-Davenport problem is positive-dimensional after
the marked-cusp conditions and contains genuine primitive solutions.
A complete classification would be interesting, but it is no longer the
shortest route to the Jacobian obstruction.

The more promising direction is to finish the remaining local charts
while preserving the original pole placement.  Affine target shears are
dangerous here: replacing \(Q\) by \(Q-\kappa P\) transfers the pole of
\(p_2\) into the nominally polynomial coefficient \(q_2\), precisely the
information used above.  The next audit should therefore treat:

1. horizontal-tangent branches whose first nonanalytic exponent is at
   least two;
2. vertical-tangent branches using the opposite projection, while
   tracking how the \(p_2/q_3\) pole asymmetry transforms.

These are finite valuation problems and use stronger structure than a
large coefficient elimination.
