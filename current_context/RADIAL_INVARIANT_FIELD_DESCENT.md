# Field descent through the radial invariant

Date: 25 July 2026

This note isolates a field-descent statement for the universal radial
\((2,3)\) outer pair.  It replaces the selected Belyi root by a weighted
first integral and shows that the two have exactly the same monodromy.
No coefficient elimination is involved.

Work over an algebraically closed field \(k\) of characteristic zero.
Fix \(k_0\ge1\), and put
\[
p=2k_0+1,\qquad q=3k_0+1,\qquad N=5k_0+2.
\]
Let
\[
P_0=\frac{z^2U(w)}w,\qquad
Q_0=\frac{z^3V(w)}w,
\tag{1}
\]
where
\[
\deg U=p,\qquad \deg V=q,
\qquad U(0)V(0)[w^p]U[w^q]V\ne0.
\tag{2}
\]
These are the endpoint conditions of the universal outer pair.

## 1. The reciprocal coefficient pair is birational

Introduce
\[
t=w^{-1},\qquad \xi=zw^{k_0},
\tag{3}
\]
and the reversed polynomials
\[
A(t)=t^pU(t^{-1}),\qquad
B(t)=t^qV(t^{-1}).
\tag{4}
\]
Then
\[
P_0=\xi^2A(t),\qquad Q_0=\xi^3B(t).
\tag{5}
\]
Both the leading and constant coefficients of \(A,B\) are nonzero, and
\[
\deg A=p,\qquad\deg B=q,\qquad
\gcd(p,q)=1.
\tag{6}
\]

> **Birational endpoint lemma.**
> \[
> k(A(t),B(t))=k(t).
> \tag{7}
> \]

Indeed, by polynomial Lüroth, the normalization of the polynomial
parametrized curve \(t\mapsto(A(t),B(t))\) is parametrized by a polynomial
\(h(t)\).  If
\[
e=[k(t):k(A,B)]=\deg h,
\]
then \(e\) divides both \(\deg A\) and \(\deg B\).  But
\[
3(2k_0+1)-2(3k_0+1)=1,
\tag{8}
\]
so \(e=1\).

The point is not merely that the outer Belyi function
\[
R(w)=\frac{wV(w)^2}{U(w)^3}
\]
has trivial deck group.  Equation (7) says that the **ordered polynomial
pair** \((A,B)\) already recovers its source coordinate rationally.

## 2. Exact invariant-coordinate descent criterion

Let \(K\) be any extension of \(k\), and let \(M/K\) be a finite
separable extension containing a nondegenerate algebraic comparison
branch
\[
Z,W\in M^\times.
\]
Put
\[
T=W^{-1},\qquad \Xi=ZW^{k_0}.
\tag{9}
\]
Suppose \(P,Q\in K\) satisfy
\[
P=\Xi^2A(T),\qquad Q=\Xi^3B(T).
\tag{10}
\]
Then
\[
\boxed{\quad
Z,W\in K
\quad\Longleftrightarrow\quad
\Xi\in K.
\quad}
\tag{11}
\]

Only the reverse implication needs proof.  If \(\Xi\in K\), then
\[
A(T)=P/\Xi^2\in K,\qquad B(T)=Q/\Xi^3\in K.
\]
By (7), there is a rational function
\(\mathcal H\in k(X,Y)\) such that
\[
t=\mathcal H(A(t),B(t)).
\]
If \(T\) is algebraic over \(k\), then \(T\in k\subset K\).  Otherwise
\(T\) is transcendental over \(k\), so the nonzero denominator in this
rational identity remains nonzero after substitution.  In either case
substitution gives \(T\in K\), and hence
\[
W=T^{-1}\in K,\qquad Z=\Xi T^{k_0}\in K.
\]

The same proof gives a monodromy statement in the intended
function-field situation, where \(T\) is transcendental over \(k\).
More generally, it is enough to assume
\[
A(T)B(T)\ne0.
\]
In a normal closure of \(M/K\), an automorphism fixes \(\Xi\) if and
only if it fixes \(T\).  For the converse direction, fixing \(T\) fixes
both \(\Xi^2\) and \(\Xi^3\) through (10), because both displayed
coefficients are nonzero, and hence fixes \(\Xi\).
Thus the two elements have the same stabilizer:
\[
\operatorname {Stab}(\Xi)=\operatorname {Stab}(T).
\tag{12}
\]
In particular, nontrivial monodromy of the selected Belyi root cannot be
a pure Kummer action on \(T\) that leaves the weighted radial invariant
\(\Xi\) fixed.

For the normalized radial correspondence of
`RADIAL_RATIONAL_DESCENT_CRITERION.md`, (11) gives the equivalent
criterion
\[
\boxed{\quad
\text{the comparison branch descends}
\quad\Longleftrightarrow\quad
ZW^{k_0}\in k(z,w).
\quad}
\tag{13}
\]
At the sole possible ramification signature
\[
(\nu Z,\nu W)=(k_0,-1),
\tag{14}
\]
one has
\[
\nu(ZW^{k_0})=0.
\tag{15}
\]
So the remaining monodromy is carried by an algebraic **unit**, not by
a pole of the invariant coordinate.  Valuation nonnegativity and
normality do not prove that this unit belongs to the base field.

Equation (13) is narrower than the previous “selected Belyi root is
rational” formulation because \(\Xi\) is the exact first integral of the
high endpoint Hamiltonians.  A successful high-end argument need only
prove that this one weighted invariant is globally single-valued.

## 3. Why the coprime endpoint data is essential

There is an exact torus countermodel if the endpoint pair fails to recover
\(t\).  It realizes the full radial symplectic density, the normalized
identity germ, and the signature (14).

On \(k[z^{\pm1},w^{\pm1}]\), put
\[
\xi=zw^{k_0},\qquad s=w^{-N}.
\]
Then
\[
\Omega=\frac{z^4}{w^3}\,dz\wedge dw
=-\frac{\xi^4}{N}\,d\xi\wedge ds.
\tag{16}
\]
For \(\lambda\ne0\), define the simplified outer pair
\[
\widehat P_0=\xi^2,\qquad
\widehat Q_0=\xi^3\left(\lambda-\frac{s}{2N}\right).
\tag{17}
\]
It satisfies
\[
d\widehat P_0\wedge d\widehat Q_0=\Omega.
\tag{18}
\]
For \(a\ne0\), translate only the Darboux coordinate \(s\):
\[
\widehat P_a=\xi^2,\qquad
\widehat Q_a=\xi^3
\left(\lambda-\frac{s+a}{2N}\right).
\tag{19}
\]
This pair still satisfies (18).  Let
\[
\theta^N=1+aw^N
\tag{20}
\]
and choose at \(w=0\) the binomial branch \(\theta=1+O(w^N)\).  Then
\[
Z=z\theta^{k_0},\qquad W=w\theta^{-1}
\tag{21}
\]
has
\[
ZW^{k_0}=\xi,\qquad W^{-N}=w^{-N}+a,
\]
and hence
\[
(\widehat P_0,\widehat Q_0)(Z,W)
=(\widehat P_a,\widehat Q_a)(z,w).
\tag{22}
\]
The branch (21) is formally the identity at \(w=0\), but it has degree
\(N\): the polynomial \(1+aw^N\) has simple zero divisors, so (20) is
Eisenstein at each of them.  At such a divisor,
\[
(e,\nu Z,\nu W)=(N,k_0,-1).
\tag{23}
\]

This does not contradict (11), because the simplified first component in
(17) has reciprocal coefficient \(A(t)=1\); the ordered endpoint pair
does not recover \(t\).  It is also not a bounded polynomial
counterexample: (17) contains the Laurent monomial
\(z^3w^{-2k_0-2}\), outside the original-plane Newton support.

The countermodel proves a sharp negative statement nonetheless:
symplecticity, a normalized identity germ, exact Kummer degree \(N\), and
the sole allowed valuation signature are locally and torically compatible.
The genuine obstruction must use the coprime outer endpoint
parametrization or the original polynomial support.

## 4. Precise remaining lemma

The universal field-descent problem can now be stated in one coordinate:

> **Radial-invariant monodromy lemma.**  For a bounded polynomial Keller
> completion with the fixed outer pair, the algebraic comparison invariant
> \[
> \Xi=ZW^{k_0}
> \]
> is fixed by global monodromy, equivalently
> \(\Xi\in k(z,w)\).

By (11), this lemma is equivalent to full field descent and therefore
cannot be inferred from deck rigidity alone.  Its useful extra content is
that any proof may focus on an algebraic unit with valuation zero at the
only possible ramification divisor.  The torus model above shows that
local symplectic or valuation arguments alone cannot prove the lemma;
one must use the genuine reversed endpoint polynomials \(A,B\), global
component incidence, or original-plane integrality.

The coordinate identities and the sharp torus countermodel are checked
in `route_bd_radial_invariant_field_descent.py`.
