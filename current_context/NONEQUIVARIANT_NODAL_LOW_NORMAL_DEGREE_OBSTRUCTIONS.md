# Keller maps of cubic normal degree and the quartic frontier

Date: 26 July 2026

## Outcome

Let
\[
 \gamma(x)=(p(x),q(x))
 =
 \bigl(x^3-x,\ x^5-x^4+x^3-x\bigr).
\tag{1}
\]
Then
\[
 \gamma(0)=\gamma(1)=(0,0)
\]
and \(\gamma\) is an immersion.  An explicit Bezout certificate is
\[
\begin{aligned}
 &(180x^3-69x^2+108x+22)p'(x)\\
 &\qquad+(-108x-45)q'(x)=23.
\end{aligned}
\tag{2}
\]
The two tangent vectors at the colliding parameters are
\[
 \gamma'(0)=(-1,-1),\qquad \gamma'(1)=(2,3),
\]
so the branches are transverse.  The third zero \(-1\) of \(p\) is not
a preimage of the collision because \(q(-1)=-2\).

Moreover, there is no affine target map taking \(\gamma(x)\) to
\(\gamma(1-x)\).  Indeed,
\[
 p(1-x)=-x^3+3x^2-2x.
\]
In an affine combination of \(1,p,q\), degree forces the coefficient of
the degree-five polynomial \(q\) to vanish, after which the \(x^2\)
coefficient cannot be produced from \(1,p\).  Thus (1) is a convenient
affine-asymmetric nodal boundary.
More importantly, the thickening class studied below imposes **no**
source or target involution on the full plane map, so the known
equivariant-involution automorphism theorems do not apply.

This note proves an obstruction uniform in the \(x\)-degrees:

> **Theorem.** Let \(F,G\in\mathbf C[x,y]\) satisfy
> \(J(F,G)\in\mathbf C^\times\), and suppose the boundary
> \(x\mapsto(F(x,0),G(x,0))\) is noninjective.
>
> 1. One necessarily has
>    \[
>    \boxed{\max(\deg_yF,\deg_yG)\geq4.}
>    \]
> 2. After swapping the two coordinates and applying invertible
>    constant linear target changes, the only exact bidegree not
>    covered by the preceding reductions is \((3,2)\).  Writing
>    \[
>    \begin{aligned}
>    F&=p+a y+b y^2+c y^3,\\
>    G&=q+d y+e y^2,
>    \end{aligned}
>    \tag{3}
>    \]
>    their leading coefficients have the form
>    \[
>       c=\alpha h^3,\qquad e=\beta h^2
>    \tag{4}
>    \]
>    for \(\alpha,\beta\in\mathbf C^\times\).
>    The remaining four equations then exclude both constant and
>    nonconstant \(h\).  Thus the \((3,2)\) case does not occur at all.

There is a global corollary.

> **Corollary.** Every polynomial map
> \((F,G):\mathbf C^2\to\mathbf C^2\) with nonzero constant Jacobian
> and
> \[
> \max(\deg_yF,\deg_yG)\leq3
> \]
> is a polynomial automorphism.

Indeed, the theorem makes the restriction to the line \(y=0\)
injective.  The injectivity-on-one-line theorem then implies that the
Keller map is an automorphism; see V. Shpilrain and J.-T. Yu,
*Polynomial retracts and the Jacobian conjecture*, Trans. Amer. Math.
Soc. **352** (2000), 477--484, Corollary 1.5
([accessible preprint](https://arxiv.org/abs/math/9701210)).  Their
corollary cites J. Gwoździewicz, *Injectivity on one line*, Bull. Soc.
Sci. Lett. Łódź Sér. Rech. Déform. **15** (1993), 59--60.

Consequently, the first non-equivariant nodal architecture is not a
quadratic or cubic normal thickening, regardless of its \(x\)-degree.
For the boundary (1), any counterexample thickening must begin at
normal degree at least four.

This is a scoped obstruction and reduction, not a counterexample or a
proof of the plane Jacobian conjecture.

### Relation to a prior partial-degree claim

Moskowicz,
[*A variation on Magnus' theorem and its generalizations*,
Theorem 2.7](https://arxiv.org/abs/1810.08202), gives the stronger
criterion that a Keller map is invertible whenever even one coordinate
has \(y\)-degree at most four.  One route through the printed proof
invokes Theorem 2.4 and its number-theoretic Lemma 2.3.  The lemma is
false as stated: for
\[
(a,b,c,d,\epsilon)=(1,1,2,1,2),
\]
its two linear forms are \(L+1,L+2\), while the lemma requires both to
be coprime to \(2\).  Consecutive integers cannot both be odd.
However, this tuple is not realized by the nonzero-leading-degree
Keller branch: the top Jacobian coefficient forces \(nv=ru\), whereas
\((n,u,r,v)=(1,1,2,4)\) violates that equality.  More generally, when
\(u,v>0\), the same equality makes the two reduced degree pairs equal,
so the unequal-pair branch of Theorem 2.4 is vacuous for Keller data.

More importantly, Theorem 2.7 is repairable without Lemma 2.3.  If
\(n,u>0\), write \(n=A\widetilde n\), \(u=A\widetilde u\), with
\(\gcd(\widetilde n,\widetilde u)=1\).  In the cited partial-degree
range, \(A\mid n\le4\), so \(A\in\{1,2,3,4\}\).  Dirichlet supplies
arbitrarily large \(L\) for which
\(\widetilde u+L\widetilde n\) is prime.  After the triangular source
change \(y\mapsto y+x^L\), the relevant coordinate has total degree
\(A(\widetilde u+L\widetilde n)\), to which the classical
Magnus-type criterion used in that paper applies.  If \(u=0<n\), take
\(L\) itself to be a sufficiently large prime and use the same
argument; the \(n=0\) case is triangular.  Thus the stronger prior
statement remains available despite the defective auxiliary lemma.

Even the exact \((3,2)\) nonexistence statement follows quickly from
that repaired theorem and the weighted-bidegree classification of
M. Karaś, *On weighted bidegree of polynomial automorphisms of
\(\mathbf C^2\)*, Bull. Polish Acad. Sci. Math. **70** (2022),
107--114, Theorem 1.1
([DOI](https://doi.org/10.4064/ba220430-21-3)).
Indeed, the leading equation gives
\(f_3=\alpha h^3,\ g_2=\beta h^2\).  For the weight \((1,N)\), with
\(N\) larger than every lower coefficient \(x\)-degree, the weighted
coordinate degrees are
\[
3(N+\deg h),\qquad2(N+\deg h).
\]
The repaired partial-degree theorem first makes the Keller pair an
automorphism, while Karaś's theorem requires one of these non-base
weighted degrees to divide the other, which is impossible.

The argument below independently proves the simultaneous bound
\(\max(\deg_yF,\deg_yG)\le3\), without that number-theoretic lemma.
It is retained as a coefficient-level alternative proof and as the
input for the quartic normal-form calculation below.  The exact
\((3,2)\) coefficient integral is likewise presented as an alternative
structural proof, not as a new nonexistence statement.

## 1. Quadratic normal degree forces boundary injectivity

We first prove a boundary theorem which does not use (1).

### Proposition 1

Let \(K\) be a characteristic-zero field.  Suppose
\[
 F,G\in K[x,y],\qquad J(F,G)=\lambda\in K^\times,
\]
and
\[
 \deg_yF,\deg_yG\leq2.
\]
Then the polynomial curve
\[
 x\longmapsto(F(x,0),G(x,0))
\]
is injective over every extension field of \(K\).

#### Proof

If both \(y\)-degrees are at most one, write
\[
 F=p+ay,\qquad G=q+cy.
\]
The coefficient of \(y\) in the Jacobian gives
\[
 a'c-ac'=0.
\]
Thus \((a,c)=h(\alpha,\beta)\) for a polynomial \(h\) and constants
\(\alpha,\beta\), not both zero.  The constant coefficient is
\[
 h(\beta p'-\alpha q')=\lambda.
\]
Both factors are units.  Hence \(h\) is constant and
\(\beta p-\alpha q\) is an affine linear polynomial of nonzero slope.
It recovers \(x\) from \((p(x),q(x))\).

Now suppose a quadratic term occurs.  If
\[
 F=p+ay+by^2,\qquad G=q+cy+dy^2,
\]
the coefficient of \(y^3\) is
\[
 2(b'd-bd')=0.
\]
If \(b=d=0\), this is the linear case.  Otherwise
\((b,d)=h(\alpha,\beta)\) for a polynomial \(h\) and a nonzero constant
vector \((\alpha,\beta)\).  A matrix in \(\operatorname{GL}_2(K)\)
sends this vector to \((\widetilde b,0)\), with
\(\widetilde b\ne0\).  Renaming the transformed coefficients, we may
write
\[
 F=p+ay+by^2,\qquad G=q+cy,\qquad b\ne0.
\tag{5}
\]
The coefficient \(c\) cannot vanish identically: otherwise the
coefficient of \(y\) in the Jacobian would give \(bq'=0\), and then the
constant Jacobian would be zero.
The three Jacobian equations are
\[
\begin{aligned}
 b'c-2bc'&=0,\\
 a'c-ac'-2bq'&=0,\\
 p'c-aq'&=\lambda.
\end{aligned}
\tag{6}
\]
The first two integrate in \(K(x)\) to
\[
 b=\kappa c^2,\qquad
 a=c(2\kappa q+\ell),
\tag{7}
\]
where \(\kappa\ne0\) and \(\ell\) are constants.  Substitution in the
last equation gives
\[
 c\bigl(p'-\kappa(q^2)'-\ell q'\bigr)=\lambda.
\]
Again both polynomial factors are units.  Thus \(c\) is constant and
\[
 p-\kappa q^2-\ell q
\]
is affine linear of nonzero slope.  It recovers \(x\) from the boundary
point.  This proves injectivity. \(\square\)

No bound on the \(x\)-degrees was used.

## 2. A cubic coordinate against a linear coordinate is still rigid

### Proposition 2

Suppose \(J(F,G)\in K^\times\),
\[
 \deg_yF\leq3,\qquad \deg_yG\leq1.
\]
Then the boundary is injective.

#### Proof

Only the genuinely cubic case remains after Proposition 1.  Write
\[
 F=p+ay+by^2+cy^3,\qquad G=q+dy.
\]
Here \(d\ne0\).  If \(d=0\), the coefficient of \(y^2\) in the
Jacobian gives \(cq'=0\); since \(c\ne0\), the Jacobian then vanishes.
The coefficients of \(y^3,y^2,y,1\) give
\[
\begin{aligned}
 c'd-3cd'&=0,\\
 b'd-2bd'-3cq'&=0,\\
 a'd-ad'-2bq'&=0,\\
 p'd-aq'&=\lambda.
\end{aligned}
\tag{8}
\]
 The first three equations give
\[
 c=\rho d^3,\qquad
 b=d^2(3\rho q+\mu),\qquad
 a=d(3\rho q^2+2\mu q+\ell)
\tag{9}
\]
for constants \(\rho\ne0,\mu,\ell\).  The last equation becomes
\[
 d\bigl(p'-(\rho q^3+\mu q^2+\ell q)'\bigr)=\lambda.
\]
Therefore \(d\) is constant and
\(p-\rho q^3-\mu q^2-\ell q\) is affine linear of nonzero slope.  The boundary
is injective. \(\square\)

If both coordinates initially have \(y\)-degree three, their cubic
coefficients \(c_F,c_G\) satisfy the top equation
\[
3(c_F'c_G-c_Fc_G')=0.
\]
If both are nonzero, \(c_F/c_G\in K^\times\), and a constant target
change eliminates one cubic term.  If one is zero, the pair already
has bidegree \((3,\le2)\).  Propositions 1 and 2 therefore show that,
up to swapping coordinates, the first exact bidegree still requiring
analysis is \((3,2)\).

## 3. The exact \((3,2)\) system

For (3), the equation \(J(F,G)=\lambda\) is equivalent to
\[
\begin{aligned}
 2c'e-3ce'&=0,                                      &&[y^4]\\
 2b'e-2be'+c'd-3cd'&=0,                            &&[y^3]\\
 2a'e-ae'+b'd-2bd'-3cq'&=0,                        &&[y^2]\\
 2p'e+a'd-ad'-2bq'&=0,                             &&[y^1]\\
 p'd-aq'&=\lambda.                                 &&[y^0]
\end{aligned}
\tag{10}
\]
Exact bidegree \((3,2)\) means \(c,e\ne0\), so all divisions below
are legitimate in \(\mathbf C(x)\).
The first equation integrates to
\[
 c^2=C e^3,\qquad C\in\mathbf C^\times.
\]
Unique factorization gives (4).  After scaling the two target
coordinates by nonzero constants, we may take
\[
 c=h^3,\qquad e=h^2.
\tag{11}
\]

### Proposition 3: the constant leading factor is impossible

If \(h\) in (11) is constant, system (10) has no polynomial solution
with \(\lambda\ne0\).

#### Proof

After a constant rescaling of \(y\), take \(h=1\).  The second equation
of (10) integrates to
\[
 2b-3d=k
\tag{12}
\]
for a constant \(k\).  The third equation then integrates to
\[
 d=\frac{2b-k}{3},\qquad
 a=\frac{b^2+kb}{6}+\frac32q+A
\tag{13}
\]
for a constant \(A\).  The fourth equation has the first integral
\[
 2p+\frac{b^3}{27}-\frac{k b^2}{18}
 -\frac{k^2b}{18}-bq-\frac{2A}{3}b-\frac{k}{2}q=B.
\tag{14}
\]
The irrelevant constant \(B\) disappears after differentiation.

Substituting (13)--(14) into the last equation of (10) gives
\[
 p'd-aq'=\Psi'(x),
\tag{15}
\]
where
\[
\begin{aligned}
\Psi={}&-\frac{b^4}{108}+\frac{k b^3}{54}
-\frac{k^3b}{108}
+\frac{q(b^2-kb)}6+\frac{A(b^2-kb)}9\\
&-\frac{k^2q}{12}-\frac34q^2-Aq.
\end{aligned}
\tag{16}
\]
This polynomial is exactly a constant minus a square:
\[
\boxed{
\Psi=
\frac{k^4}{432}+\frac{Ak^2}{18}+\frac{A^2}{3}
-\frac34
\left(
 q-\frac{2b^2-2kb-k^2}{18}+\frac{2A}{3}
\right)^2.
}
\tag{17}
\]
If (15) were the nonzero constant \(\lambda\), the derivative of the
square in (17) would be a nonzero constant.  No square of a polynomial
has nonzero constant derivative.  This is a contradiction. \(\square\)

### Proposition 4: the rational quotient has no pole

The polynomial \(h\) in (11) must be constant.

#### Proof

The second equation of (10), after (11), is
\[
\left(\frac{2b-3hd}{h^2}\right)'=0.
\]
Hence
\[
 2b-3hd=k h^2.
\tag{18}
\]
for a constant \(k\).

In the rational function field set
\[
 u=\frac d h.
\]
Then (18) becomes
\[
 d=hu,\qquad
 b=h^2\left(\frac32u+\frac k2\right).
\tag{19}
\]
Write \(a=hV\) with \(V\in\mathbf C(x)\).  Substitution in the
\(y^2\) equation of (10), followed by division by \(h^3\), gives
\[
 2V'-\left(\frac32u+k\right)u'-3q'=0.
\tag{20}
\]
Therefore
\[
\boxed{
 V=\frac38u^2+\frac k2u+\frac32q+A
}
\tag{21}
\]
for a constant \(A\).

The \(y\) equation of (10), divided by \(h^2\), is exactly
\[
 \Phi'=0,
\]
where
\[
\boxed{
\Phi=
 2p+\frac18u^3-\frac32uq-Au-kq.
}
\tag{22}
\]
Thus \(\Phi\in\mathbf C\).

This identity forces \(u\) to have no finite pole.  Indeed, if \(u\)
had a finite pole of order \(r>0\), taking the valuation there would
make \(u^3/8\) the unique term of order \(-3r\) in (22); all terms
linear in \(u\) have order at least \(-r\), while \(p,q\) are regular.
Hence \(u\in\mathbf C[x]\).  Formula (21) then also gives
\(V\in\mathbf C[x]\).

Formulae (19) and (21) now show that every positive-\(y\) coefficient
of both coordinates is divisible by \(h\).  In particular, the last
equation of (10) factors as
\[
 \lambda=p'd-aq'=h\bigl(p'u-Vq'\bigr).
\tag{23}
\]
Since \(\lambda\) is a nonzero constant, \(h\) is a unit. \(\square\)

Proposition 4 reduces to constant \(h\), and Proposition 3 excludes
that case.  This proves the theorem.

## 4. The unique quartic-normal frontier

The same top-coefficient equation removes every normal-degree-four
bidegree except \((4,3)\).  Suppose, after swapping coordinates, that
\[
\deg_yF=4,\qquad \deg_yG=n\le4,
\]
and let \(f_4,g_n\) be the leading coefficients.  The coefficient of
\(y^{n+3}\) in the Jacobian is
\[
n f_4'g_n-4f_4g_n'=0.
\tag{24}
\]

If \(n=1\), then \(f_4=\kappa g_1^4\), and the target shear
\[
F\longmapsto F-\kappa G^4
\]
lowers \(\deg_yF\).  If \(n=2\), the same argument gives
\(f_4=\kappa g_2^2\) and the shear \(F\mapsto F-\kappa G^2\).
If \(n=4\), the leading coefficients are proportional and a constant
linear target change lowers one degree to at most three; if the other
degree is then one or two, apply the corresponding power shear once
more.  The case \(n=0\) is incompatible with an exact quartic
coordinate and a nonzero constant Jacobian.

Consequently:

> **Quartic reduction.**  If
> \(\max(\deg_yF,\deg_yG)\le4\) and the Keller map is not an
> automorphism, then, up to swapping its coordinates, its exact normal
> bidegree is
> \[
> \boxed{(4,3)}.
> \tag{25}
> \]

In that case (24) gives
\[
f_4=\alpha h^4,\qquad g_3=\beta h^3
\]
for a polynomial \(h\) and nonzero constants \(\alpha,\beta\).  Unlike
the power-related cases, no polynomial target shear removes the
quartic term.

## 5. Consequence for the next architecture

The asymmetric boundary (1) remains a valid built-in collision, but a
counterexample thickening cannot have normal degree at most three.  At
the stage of this calculation, the next exact architecture was
\[
\max(\deg_yF,\deg_yG)=4.
\tag{26}
\]
The quartic reduction left \((4,3)\), whose rational depressed normal
form and local valuations are now completely treated in the companion
note `NONEQUIVARIANT_NORMAL_DEGREE_FOUR_EXCLUSION.md`, retaining
\[
 p=x^3-x,\qquad q=x^5-x^4+x^3-x
\]
only at the final two coefficient equations.

The repaired one-coordinate partial-degree theorem discussed above
goes further.  Combined with the leading-coefficient relation and
constant target shears, it excludes every exact normal pair of maximum
degree at most seven.  The first arithmetic frontier is \((8,6)\);
its common leading factor must have even degree.  This current frontier
uses no parity assumption and should not be confused with the
reflection-equivariant ansatz excluded elsewhere.
