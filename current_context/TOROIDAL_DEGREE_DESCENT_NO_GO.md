# Classification and failure of one-boundary toroidal degree descent

Date: 25 July 2026

## Audited conclusion

Let \(k\) be a characteristic-zero field and suppose a terminal Laurent
normalization has produced
\[
[P,Q]_{x,y}=\kappa x^r,\qquad \kappa\in k^\times.
\tag{1}
\]
There is a larger class of polynomial charts that could in principle absorb
the factor \(x^r\) than the birational Rees chart
\((x,x^r y)\).  Every dominant triangular boundary chart
\[
u=\phi(x),\qquad v=V(x,y)
\]
whose Jacobian is a nonzero multiple of \(x^r\) reduces, after affine
rescaling and up to swapping its two outputs, to
\[
\boxed{
u=x^a,\qquad v=x^c y,\qquad
a+c=r+1,\quad 1\le a\le r+1.
}
\tag{2}
\]
Allowing a moving center replaces \(v\) by
\[
v=x^c y+f(x),\qquad f\in k[x],
\tag{3}
\]
without changing the Jacobian.  Iterating charts of this kind produces no
larger class: the composite again has the form (2)--(3).

If \(P,Q\in k[u,v]\), then (1) descends to the genuine Keller equation
\[
[\bar P,\bar Q]_{u,v}=\frac{\kappa}{a}.
\tag{4}
\]
For \(a=1\) this is the previously identified birational Rees descent.  For
\(a>1\) it is a finite degree-\(a\) descent.  Minimal function-field
degree together with the classical Galois case of the Jacobian conjecture
excludes every finite alternative: either the descended pair is a smaller
counterexample, or the original extension is cyclic Galois.  The exact
membership test at the top \(y\)-coefficient is
\[
\boxed{
\operatorname{lc}_y R
=x^{cd}H(x^a)
\quad\text{when }R\in k[x^a,x^c y+f(x)],\
d=\deg_yR.
}
\tag{5}
\]

Formula (5) excludes **every** such chart for both GGHV Proposition 4.3
supports.  In those supports
\[
\deg_yP=16,\qquad \operatorname{lc}_yP=\lambda x^8,\quad\lambda\ne0.
\tag{6}
\]
For \(r=2\), the three possibilities in (2) are
\[
(a,c)=(1,2),(2,1),(3,0).
\]
The first two require respectively \(8\ge32\) and \(8\ge16\); the last
requires \(8\equiv0\pmod3\).  All three fail.  This uses the required
outer vertex, so it applies to case c as well as a/b, independently of
the unsolved coefficient equations.

Normalization does not evade the obstruction.  The integral closure of
\[
B_{a,c,f}=k[x^a,x^c y+f(x)]
\tag{7}
\]
in \(k(x,y)\) is
\[
\boxed{
\widetilde B_{a,c,f}=k[x,x^c y].
}
\tag{8}
\]
Passing from (7) to (8) discards exactly the finite factor \(a\).  In the
normalized coordinates \((x,v)\), equation (1) still has Jacobian
\(\kappa x^{a-1}\), not a constant unless \(a=1\).

Consequently the degree-lowering bridge cannot be obtained from any
sequence in this triangular one-boundary toroidal class, including finite
cyclic covers, center translations, and normalization.  A successful
global descent must use genuinely non-toroidal information from more than
one boundary valuation, or prove an additional cyclic deck-invariance
theorem.

This is a structural no-go theorem, not a proof of \(JC(2)\).  The terminal
countermodels below have monomial, not constant, Jacobian and are not
asserted to arise from polynomial Keller maps.

## 1. Classification of triangular absorbing charts

Start with the general dominant triangular chart
\[
u=\phi(x),\qquad v=V(x,y),
\qquad \phi\in k[x],\quad V\in k[x,y].
\tag{9a}
\]
Its Jacobian is
\[
[u,v]_{x,y}=\phi'(x)V_y(x,y).
\tag{9b}
\]
If this is a nonzero scalar multiple of \(x^r\), then \(V_y\) is
independent of \(y\).  Characteristic zero gives
\[
V(x,y)=g(x)y+f(x).
\]
Unique factorization in \(k[x]\) then forces
\[
\phi'(x)=\alpha x^{a-1},\qquad
g(x)=\beta x^c,\qquad
a+c=r+1
\tag{9c}
\]
for some \(a\ge1,c\ge0\).  Integration gives
\[
\phi(x)=\frac{\alpha}{a}x^a+\gamma.
\]
An affine change of \(u\) and a scalar change of \(v\) therefore put the
chart in the form (2)--(3).  This proves that the list is exhaustive
within the full affine-linear-in-\(y\) one-boundary class, not just under
a monomial ansatz.

For completeness, the toric calculation gives the same list directly.

Consider a dominant polynomial monomial map
\[
u=\alpha x^a y^b,\qquad
v=\beta x^c y^d
\]
with nonnegative integral exponents.  Its Jacobian is
\[
[u,v]_{x,y}
=\alpha\beta(ad-bc)x^{a+c-1}y^{b+d-1}.
\tag{9}
\]
If (9) is a nonzero multiple of \(x^r\), then
\[
b+d=1.
\]
Thus \(\{b,d\}=\{0,1\}\).  After swapping \(u,v\), one has \(b=0,d=1\).
Dominance gives \(a\ne0\), and comparison of the \(x\)-exponent gives
\[
a+c=r+1.
\]
After harmless scalar rescaling this is exactly (2).  Conversely,
\[
[x^a,x^c y]_{x,y}=a x^{a+c-1}=a x^r.
\tag{10}
\]

The finite degree of the chart is also exact.  Put
\[
L=k(x^a,x^c y),\qquad K=k(x,y).
\]
Then \(x\) satisfies \(T^a-x^a\) over \(L\), while
\(y=(x^c y)/x^c\), so
\[
[K:L]=a.
\tag{11}
\]
The case \(a=1,c=r\) is the birational affine modification.  The opposite
endpoint \(a=r+1,c=0\) is the cyclic quotient
\((x,y)\mapsto(x^{r+1},y)\).

Adding \(f(x)\) as in (3) does not affect (10), (11), or dominance.
Unlike the birational case, the shifted subring for \(a>1\) need not
equal the unshifted subring, so the shift must not be silently discarded.
The leading-coefficient argument below handles every \(f\) at once.

## 2. Exact descent and field-degree bookkeeping

Let
\[
B_{a,c,f}=k[u,v],\qquad
u=x^a,\quad v=x^c y+f(x),\quad a+c=r+1.
\]
The generators \(u,v\) are algebraically independent.  If
\[
P=\bar P(u,v),\qquad Q=\bar Q(u,v),
\]
the chain rule gives
\[
[P,Q]_{x,y}
=a x^r[\bar P,\bar Q]_{u,v}.
\tag{12}
\]
Thus (1) implies (4).

Let \(D=[K:k(P,Q)]\).  Since \(k(P,Q)\subset k(u,v)\subset K\),
the tower formula and (11) give
\[
\boxed{
D=a\,[k(u,v):k(\bar P,\bar Q)].
}
\tag{13}
\]
Therefore a terminal pair in \(B_{a,c,f}\) yields a constant-Jacobian
pair of field degree \(D/a\).  In particular:

- \(a\mid D\);
- if the original counterexample was chosen with minimal function-field
  degree and \(D/a>1\), this is a strict minimality contradiction;
- the residual case \(D=a\) is not eliminated by minimality alone,
  because the descended Keller pair may be an automorphism.

This last qualification is essential.  Finite descent is a rigorous
degree reduction, but it does not by itself prove that the descended pair
is another counterexample.

For a counterexample chosen with **minimal function-field degree**, the
qualification can be discharged when \(a>1\).  If \(D/a>1\), the
descended pair is a counterexample of strictly smaller field degree.  If
\(D/a=1\), the birational Keller theorem makes the descended pair an
automorphism, hence
\[
k(P,Q)=k(u,v).
\]
Over an algebraically closed field, \(K/k(u,v)\) is then the cyclic
Galois extension generated by \(x^a=u\).  Transport through the Laurent
birational normalization shows that the original Keller extension is
Galois.  The classical Galois case of the Jacobian conjecture then makes
the original map an automorphism, again a contradiction.

The Galois case used here is a published theorem; see:

- M. J. Razar, *Polynomial maps with constant Jacobian*, Israel J.
  Math. **32** (1979), 97--106,
  <https://doi.org/10.1007/BF02764906>;
- D. Wright, *On the Jacobian conjecture*, Illinois J. Math. **25**
  (1981), 423--440,
  <https://doi.org/10.1215/ijm/1256047158>.

Consequently:
\[
\boxed{
\begin{gathered}
\text{a minimal-function-field-degree Keller counterexample}\\
\text{cannot descend through }B_{a,c,f}\text{ with }a>1.
\end{gathered}}
\tag{13a}
\]
The birational case \(a=1\) does not lower function-field degree and
still requires a separate degree or Newton-support minimality argument.

Target polynomial changes cannot repair failed membership.  If a target
automorphism sends \((P,Q)\) into \(B_{a,c,f}^2\), its polynomial inverse
puts \(P,Q\) themselves in \(B_{a,c,f}\).

## 3. Iteration gives no new one-boundary chart

The class (2)--(3) is closed under composition.  Indeed, compose
\[
u=x^a,\qquad v=x^c y+f(x)
\]
with
\[
U=u^b,\qquad V=u^d v+g(u).
\]
Then
\[
\begin{aligned}
U&=x^{ab},\\
V&=x^{ad+c}y+
   \bigl(x^{ad}f(x)+g(x^a)\bigr).
\end{aligned}
\tag{14}
\]
Thus the composite again has the form
\[
U=x^A,\qquad V=x^C y+F(x).
\tag{15}
\]
Its Jacobian is a nonzero scalar times \(x^{A+C-1}\).  If the total
factor absorbed is \(x^r\), then necessarily
\[
A+C=r+1.
\tag{16}
\]

Induction proves the same statement for every finite sequence.  Hence
factoring the Jacobian divisor into several line-centered Rees or cyclic
steps does not enlarge the terminal algebra class.

## 4. The top-coefficient semigroup test

Write an element of \(B_{a,c,f}\) uniquely as
\[
R=\sum_{j=0}^d R_j(u)v^j,\qquad R_d\ne0.
\]
Because \(v=x^c y+f(x)\) is affine linear in \(y\), substitution gives
\[
\deg_yR=d,\qquad
[y^d]R=x^{cd}R_d(x^a).
\tag{17}
\]
This proves (5).  In Newton-polygon language, every exponent \(e\)
occurring on the top \(y\)-row satisfies
\[
\boxed{
e\ge cd,\qquad e\equiv cd\pmod a.
}
\tag{18}
\]
The center \(f(x)\) affects lower \(y\)-rows but cannot affect (18).

For the exact GGHV a/b and case-c \(P\)-polygons, the unique top-row
point is \((e,d)=(8,16)\).  With \(r=2\), condition (18) gives:
\[
\begin{array}{c|c|c}
a&c&\text{required condition}\\ \hline
1&2&8\ge32,\\
2&1&8\ge16,\\
3&0&8\equiv0\pmod3.
\end{array}
\]
Every row is false.  Therefore
\[
\boxed{
P\notin B_{a,\,3-a,\,f}
\quad\text{for every }a=1,2,3\text{ and every }f\in k[x].
}
\tag{19}
\]
No coefficient equation or genericity assertion is used.

There is also a uniform all-scale statement for the a/b polygons
\[
\deg_yP=4R,\qquad [y^{4R}]P=\lambda x^{2R}.
\tag{20}
\]
The cases \(a=1,2\) fail (18) for every \(R\ge1\).  In the case
\(a=3,c=0\), the a/b boundary restriction is constant.  If
\(P=R_*(x^3,y+f(x))\), constancy at \(x=0\) forces
\[
R_*(u,v)=\text{constant}+uS(u,v),
\]
so \(P-\text{constant}\) is divisible by \(x^3\).  This contradicts the
required fixed vertex \((1,0)\).  Hence **every scale** of the a/b
five-block polygons also lies outside every one-boundary chart
(2)--(3), even when \(3\mid2R\).

## 5. Normalization retains a Jacobian defect

Set \(v=x^c y+f(x)\).  Since \(x\) is integral over \(B_{a,c,f}\),
\[
B_{a,c,f}[x]
=k[x,v]
=k[x,x^c y].
\tag{21}
\]
The right side is a polynomial ring, hence normal, and its fraction field
is \(K=k(x,y)\).  It is finite over \(B_{a,c,f}\), so (21) is exactly the
integral closure of \(B_{a,c,f}\) in \(K\).  This proves (8).

But
\[
[x,v]_{x,y}=x^c.
\tag{22}
\]
If \(P,Q\) merely belong to the normalization (21), equation (1) becomes
\[
[P,Q]_{x,v}=\kappa x^{r-c}
=\kappa x^{a-1}.
\tag{23}
\]
Thus normalization removes the degree-\(a\) cyclic cover and restores
the missing Jacobian exponent \(a-1\).  It cannot simultaneously keep
the finite quotient and turn (1) into a Keller equation.

Over a field containing the \(a\)-th roots of unity, this has an
equivalent deck-invariance formulation.  In the normalized coordinates
\((x,v)\), the group \(\mu_a\) acts by
\[
x\longmapsto\zeta x,\qquad v\longmapsto v,
\]
and
\[
B_{a,c,f}=k[x,v]^{\mu_a}.
\tag{24}
\]
In the original \(x,y\)-coordinates this sends
\[
y\longmapsto
\frac{x^c y+f(x)-f(\zeta x)}{(\zeta x)^c}.
\tag{25}
\]
So the extra input needed before finite descent is precisely invariance
under a nontrivial cyclic action.  Divisorial nonnegativity or
normalization does not imply it.

## 6. Exact normalization-escape family

The failure is realized by an infinite exact family.  For every
\(r\ge1\) and \(N\ge2\), put
\[
s=x^{r-1}y
\]
and
\[
\boxed{
\begin{aligned}
P_{r,N}&=x+s^N,\\
Q_{r,N}&=xs+\frac{N}{N+1}s^{N+1}.
\end{aligned}}
\tag{26}
\]
Since
\[
[x,s]_{x,y}=x^{r-1}
\]
and
\[
[x+s^N,\ xs+\tfrac{N}{N+1}s^{N+1}]_{x,s}=x,
\]
one has
\[
[P_{r,N},Q_{r,N}]_{x,y}=x^r.
\tag{27}
\]

Fix any \(a\ge2\) in (2) and put \(c=r+1-a\).  Then \(c\le r-1\), and
\[
s=x^{a-2}(x^c y).
\]
Consequently (26) lies in the normalization
\[
k[x,x^c y]=\widetilde B_{a,c,0}.
\]
It does not lie in \(B_{a,c,0}\), because the monomial \(x\) in
\(P_{r,N}\) has exponent \(1\), which is not divisible by \(a\).

The function-field degree is unbounded.  In the coordinates \((x,s)\),
\[
x=P_{r,N}-s^N
\]
and
\[
s^{N+1}-(N+1)P_{r,N}s+(N+1)Q_{r,N}=0.
\tag{28}
\]
Over \(k(P_{r,N})\), the second coordinate is a polynomial map of degree
\(N+1\) in \(s\).  Therefore
\[
\boxed{
[k(x,y):k(P_{r,N},Q_{r,N})]=N+1.
}
\tag{29}
\]

For the relevant range \(r\ge2\), this proves that even full
normalization, polynomial terminal coordinates, a contracted boundary,
and arbitrarily large field degree do not force the cyclic invariance
(24).  For \(r=2\), (26) specializes
to the Laurent escape family already audited in
`LAURENT_DEGREE_DESCENT_AUDIT.md`; the new point is that it lives
canonically in the normalization of the missing \(a=2\) descent algebra.

## 7. Strategic consequence

The exact hierarchy is now:

1. membership in one of the algebras \(B_{a,r+1-a,f}\) gives a genuine
   constant-Jacobian descent;
2. all iterated one-boundary toroidal and cyclic charts reduce to one of
   these algebras;
3. both GGHV supports fail every such membership test at a required
   vertex;
4. normalization replaces the desired Keller descent by a smaller
   monomial-Jacobian problem and admits countermodels of unbounded degree.

The promising global question is therefore no longer whether a clever
choice of Rees weight absorbs \(x^r\).  That entire one-boundary class is
classified and fails.  A genuinely new bridge must do at least one of:

- combine two or more independent boundary valuations into a
  non-triangular affine model;
- derive cyclic deck invariance (24) from global monodromy of the
  original Keller map; or
- use minimality before normalization to exclude the noninvariant
  summands, rather than hoping normalization removes them.

## Reproduction

Run:

```bash
.venv/bin/python current_context/verify_toroidal_degree_descent_no_go.py
```

The verifier checks the triangular classification, iterated-chart
formula, chain rule, GGHV and all-scale leading-coefficient exclusions,
normalization residual exponent, and the exact escape family with its
degree-\(N+1\) relation.
