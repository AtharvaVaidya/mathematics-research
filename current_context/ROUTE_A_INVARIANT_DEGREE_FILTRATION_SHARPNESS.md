# Route A: sharpness of the invariant degree filtration

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v)
\]
and
\[
\phi:B\hookrightarrow\mathbf C[a,b],\qquad
u=a^2,\quad v=4b(1+a^2b),\quad
w=a(1+2a^2b).
\tag{1}
\]
For \(F=A(u,v)+wC(u,v)\), put
\[
m=\deg_b\phi(F)(0,b)=\deg_v A(0,v).
\]
The invariant-ring estimate used in the singular dicritical audit is
sharp:
\[
\boxed{\deg_{a,b}\phi(F)\geq4m.}
\tag{2}
\]

This note adds the exact equality statement and audits the natural
global degree bounds.

> **Equality theorem.** If the coefficient of \(v^m\) in
> \(A(0,v)\) is \(\alpha_m\ne0\), then the Laurent block of
> \(\phi(F)\) which contains the boundary term
> \(4^m\alpha_m b^m\) has degree at least \(4m\).  Equality in that
> block occurs if and only if the whole block is
> \[
> \alpha_m\phi(v^m).
> \tag{3}
> \]
> In particular, equality in (2) admits no hidden cancellation of the
> distinguished \(v^m\)-term.

If \(H=(H_1,H_2)\) is the plane Keller lift and
\[
d_i=\deg H_i,\qquad m_i=\deg H_i(0,b),
\]
Chau's degree-ratio theorem gives, for coprime \(r_1,r_2\),
\[
(d_1,d_2)=K(r_1,r_2),\qquad
(m_1,m_2)=M(r_1,r_2),
\tag{4}
\]
and (2) gives only
\[
\boxed{K\geq4M.}
\tag{5}
\]
Neither the equality case \(K=4M\), the leading homogeneous Keller
relation, the boundary Jacobian equation, geometric degree six, nor
the standard Jelonek and Moh degree bounds contradict (4)--(5).

The unresolved condition is still global:
\[
J(H_1,H_2)\in\mathbf C^\times
\quad\text{on all of }\mathbf A^2,
\tag{6}
\]
not merely its leading homogeneous consequence or its restriction to
the distinguished line.

## 1. Laurent decomposition for the deck involution

Put
\[
z=a^2b.
\]
Then
\[
v=4a^{-2}z(z+1),\qquad
w=a(2z+1),
\tag{7}
\]
and the deck involution becomes
\[
\sigma(a,z)=(-a,-z-1).
\tag{8}
\]

Every polynomial \(G(a,b)\) has a unique finite Laurent expansion
\[
G(a,z/a^2)=\sum_{k\in\mathbf Z}a^k h_k(z).
\tag{9}
\]
If \(G=\phi(F)\), deck invariance gives
\[
h_k(-z-1)=(-1)^k h_k(z).
\tag{10}
\]

Suppose \(G(0,b)\) has leading term \(c b^m\), \(c\ne0\).  A monomial
\(a^ib^j=a^{i-2j}z^j\) with \(i=0,j=m\) belongs to the block
\(k=-2m\).  Polynomiality in \(a,b\) implies that this block has the
form
\[
a^{-2m}h(z),\qquad z^m\mid h(z).
\tag{11}
\]
Since \(k\) is even, (10) says \(h(-z-1)=h(z)\).  Applying this
identity to the zero of order at least \(m\) at \(z=0\) gives a zero
of order at least \(m\) at \(z=-1\).  Hence
\[
z^m(z+1)^m\mid h(z).
\tag{12}
\]

The term \(a^{-2m}z^j\) is \(a^{2j-2m}b^j\), of ordinary total degree
\[
3j-2m.
\]
Equations (11)--(12) therefore give
\[
\deg a^{-2m}h(z)
=-2m+3\deg h
\geq-2m+6m
=4m.
\tag{13}
\]
Equality holds precisely when
\[
h(z)=c[z(z+1)]^m.
\tag{14}
\]
Since \(c=4^m\alpha_m\), (7) turns (14) into (3).

This is the involution-theoretic form of the reduced-basis formula
\[
\deg\phi(F)=
\max\left\{
2i+4j:[u^iv^j]A\ne0,\quad
4+2i+4j:[u^iv^j]C\ne0
\right\}.
\tag{15}
\]
Indeed, the respective leading monomials are
\[
4^ja^{2i+2j}b^{2j},\qquad
2\cdot4^ja^{3+2i+2j}b^{1+2j};
\tag{16}
\]
their exponent pairs are all distinct.

## 2. Equality is compatible with the top Keller relation

Assume equality in (5), so \(d_i=4m_i\).  Formula (15) shows that
every monomial in the leading homogeneous form \(H_{i,+}\) is
divisible by
\[
a^{2m_i}.
\tag{17}
\]
For example, a term from \(u^iv^j\) of degree \(4m_i\) has
\(i+2j=2m_i\), and its leading \(a\)-exponent is
\[
2i+2j=4m_i-2j\geq2m_i.
\]
The \(wC\)-terms give the still larger minimum \(2m_i+1\).

For a Keller pair, the top homogeneous forms are algebraically
dependent.  With (4) and unique factorization,
\[
H_{1,+}=c_1R^{r_1},\qquad
H_{2,+}=c_2R^{r_2}
\tag{18}
\]
for a homogeneous polynomial \(R\) of degree \(K=4M\).  Equation
(17) implies only
\[
R=a^{2M}S,\qquad \deg S=2M.
\tag{19}
\]
This is consistent: for the distinguished equality blocks
\(H_i\sim\alpha_i v^{m_i}\), one may take \(R\) proportional to
\((ab)^{2M}\).  Thus the usual top-degree cancellation forced by
\(J(H_1,H_2)\in\mathbf C^\times\) supplies no contradiction.

## 3. The boundary Jacobian is only a Bezout identity

Write
\[
F_i=A_i(u,v)+wC_i(u,v),\qquad
\gamma_i(b)=A_i(0,4b),\qquad
\rho_i(b)=C_i(0,4b).
\]
Direct differentiation of (1) at \(a=0\) gives
\[
\partial_aH_i(0,b)=\rho_i(b),\qquad
\partial_bH_i(0,b)=\gamma_i'(b).
\]
Consequently the Keller equation restricted to the line is
\[
\boxed{\rho_1\gamma_2'-\gamma_1'\rho_2=c\ne0.}
\tag{20}
\]
It says exactly that \(\gamma_1'\) and \(\gamma_2'\) are coprime.
That is the immersion condition; it does not prevent distinct
normalization points from being identified.

The nodal parametrization
\[
\gamma(b)=(b^2-1,\ b(b^2-1))
\tag{21}
\]
has \(\gamma(1)=\gamma(-1)\) and nowhere-vanishing derivative.
Taking
\[
\rho_1=-1,\qquad \rho_2=-\frac32b
\]
makes the left side of (20) equal to \(1\).

There is an exact invariant lift realizing the equality degrees and
this first-neighborhood equation:
\[
\begin{aligned}
F_1&=\frac{v^2}{16}-1-w,\\
F_2&=\frac{v^3}{64}-\frac v4-\frac38vw.
\end{aligned}
\tag{22}
\]
Its plane pullback has
\[
\deg H_1=8,\qquad \deg H_2=12,\qquad
J(H_1,H_2)|_{a=0}=1,
\tag{23}
\]
and
\[
H_{1,+}^3=H_{2,+}^2.
\tag{24}
\]
Globally, however,
\[
J(H_1,H_2)
=\frac12(6a^3b+3a+2)(8a^4b^2+8a^2b+1),
\tag{25}
\]
so (22) is not a Keller pair.  It is a sharp countermodel only for
the filtration, top-form, singular-normalization, and boundary-jet
package.

The model also honestly misses the required geometric degree: the map
\(S\to\mathbf A^2\) in (22) has generic degree six, and its plane
pullback has generic degree twelve.  Indeed, with \(r=v/4\) and target
coordinates \(x,y\), \(r\) satisfies
\[
r^3-(1+3x)r+2y=0,
\tag{26}
\]
while \(u\) is generically quadratic over \(\mathbf C(v,w)\).  This
degree mismatch is precisely why (22) is not a Route A counterexample.

## 4. Why the available numerical theorems do not close the gap

Chau's theorem concerns the ratio of the two coordinate degrees of a
nonproper component and the ratio of the two coordinate degrees of the
map.  It does not identify their common multiplier with the geometric
degree of the map.  Thus geometric degree six does not turn (5) into
an upper bound for \(K\) or \(K/M\).

Jelonek--Lasoń prove that for a generically finite polynomial map of
algebraic degree
\[
D=\max(d_1,d_2),
\]
the nonproperness set is covered by polynomial curves of degree at
most \(D-1\).  Here the distinguished parametrization has degree
\(\max(m_1,m_2)\leq D/4\), so their inequality is automatically
satisfied and is strictly weaker than (2).

Heitmann proved that a noninvertible plane Keller pair must satisfy
\[
\gcd(d_1,d_2)\geq16.
\tag{27}
\]
In the notation (4), this says \(K\geq16\).  Combined with (5), it
gives only
\[
\boxed{K\geq\max(16,4M),}
\tag{28}
\]
which is consistent for arbitrarily large \(K,M\).  It rules out some
small equality cases but not the equality architecture itself.

Finally, generic degree six bounds the number of sheets in a generic
fiber and the number of retained points in a special quasi-finite
fiber.  It does not bound the raw total degrees \(d_i\), which can
also be changed drastically by polynomial target automorphisms without
changing geometric degree.

Therefore no all-degree contradiction follows from the present
degree data.  A successful continuation must connect the cubic
intermediate extension or the full dicritical sheet budget to the
global equation (6); the line restriction (20) and the top relation
(18) are both too weak.

## 5. References and verification

The degree-ratio statement appears in Nguyen Van Chau,
*Non-proper value set and the Jacobian condition*,
arXiv:math/0305088, Theorem 1, and in his later dicritical
formulations.

The nonproperness-curve degree bound is Z. Jelonek and M. Lasoń,
*Quantitative properties of the non-properness set of a polynomial
map*, Manuscripta Math. **156** (2018), 383--397,
arXiv:1411.5011, Theorem 2.2.

The gcd-degree bound is R. C. Heitmann,
*On the Jacobian conjecture*, J. Pure Appl. Algebra **64** (1990),
35--72, DOI
[10.1016/0022-4049(90)90005-3](https://doi.org/10.1016/0022-4049(90)90005-3).

Run

```sh
.venv/bin/python current_context/verify_route_a_invariant_degree_filtration_sharpness.py
```

for the chart, involution, reduced-basis, equality-block, nodal
boundary, top-form, Jacobian, and cubic-elimination checks.
