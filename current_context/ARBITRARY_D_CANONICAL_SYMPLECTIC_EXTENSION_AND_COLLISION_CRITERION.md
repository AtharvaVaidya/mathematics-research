# Canonical symplectic extension and collision criterion for arbitrary \(d\)

Date: 25 July 2026

## Outcome

Let \(d\in\mathbf C[x]\) be monic of degree \(g\geq1\), let
\(u\ne0\), and set
\[
 \gamma(x)=(p_0(x),q_0(x))
 =\bigl(d(x)^2+ux,d(x)^3\bigr).
\tag{1}
\]
This note gives an intrinsic all-order form of the unrestricted
filtered Keller lift, independent of any two-block hypothesis.

If \(v=(p_1,q_1)\in\mathbf C[x]^2\) is any polynomial normal field
with
\[
 \det(\gamma',v)=p_0'q_1-q_0'p_1=1,
\tag{2}
\]
put
\[
 \Omega(x)=\det(v',v)=p_1'q_1-p_1q_1'.
\tag{3}
\]
There is a unique series \(\theta\in y\mathbf C[x][[y]]\) satisfying
\[
 y=\theta+\frac{\Omega(x)}2\theta^2.
\tag{4}
\]
Then
\[
 \boxed{(P,Q)=\gamma(x)+\theta(x,y)v(x)}
\tag{5}
\]
has \(J(P,Q)=1\) exactly.  Equivalently,
\[
 \theta=\sum_{n\geq1}
 \frac{(-1)^{n-1}C_{n-1}}{2^{n-1}}
 \Omega^{n-1}y^n.
\tag{6}
\]
Thus the Catalan series found in the resonant cyclic quotient is not
an accidental special-family pattern.  It is the canonical
straight-normal symplectic extension of every immersed polynomial
boundary curve.

For (1), no polynomial normal field satisfying (2) can have
\(\Omega=0\).  Therefore every straight-normal symplectic extension
(5) has infinitely many nonzero transverse coefficients.  This is
an exact all-order nontermination theorem for that gauge.

Two further facts sharply delimit the remaining search.

* The boundary map \(\gamma:\mathbf A^1\to\mathbf A^2\) is never
  injective.  An explicit polynomial of degree \(2g^2\) produces
  collisions.  Hence any polynomial termination of the filtered
  recurrence would already be a genuine noninvertible Keller map,
  not merely a pair requiring a separate invertibility audit.
* The new direct coefficient proof here excludes transverse
  \(y\)-degree at most four.  A repaired prior theorem of Moskowicz
  forces invertibility whenever either coordinate has \(y\)-degree at
  most four; a one-line leading-coefficient reduction therefore also
  excludes maximum transverse degree five.

This does not settle the arbitrary-\(d\) recurrence.  A higher-order
formal symplectic reparametrization can leave the straight-normal
gauge and move Catalan coefficients between Laurent slots.  The
unresolved question is whether such a reparametrization can both
respect all reciprocal degree windows and terminate.  The results
below show that any such termination must have transverse degree at
least six and would immediately be a counterexample to \(JC(2)\).

## 1. Intrinsic Catalan extension

Differentiate (5), first regarding \(x,\theta\) as independent:
\[
 \det\left(\frac{\partial(P,Q)}{\partial(x,\theta)}\right)
 =\det(\gamma'+\theta v',v)
 =1+\Omega\theta.
\tag{7}
\]
On the other hand, (4) gives
\[
 \frac{\partial y}{\partial\theta}=1+\Omega\theta.
\tag{8}
\]
Terms involving \(\partial_x\theta\) do not affect the determinant,
because they add a multiple of \(v\) to the first column.  Dividing
(7) by (8) proves \(J_{x,y}(P,Q)=1\).

The unique solution of (4) with \(\theta(x,0)=0\) is
\[
 \theta=\frac{\sqrt{1+2\Omega y}-1}{\Omega},
\tag{9}
\]
interpreted by its regular limit \(y\) when \(\Omega=0\).  Expanding
(9) gives (6).

For the bounded defect-one representative
\[
 p_1=-\frac{4d'}{3u^2},\qquad
 q_1=\frac1u-\frac{2dd'}{u^2},
\tag{10}
\]
direct differentiation gives
\[
 \boxed{
 \Omega=-\frac4{3u^4}\left(ud''+2(d')^3\right).
 }
\tag{11}
\]
This is the intrinsic version of the resonant identity
\(x^\delta\omega=\Omega\).  If \(g\geq2\), the two terms inside
parentheses have degrees \(g-2\) and \(3g-3\), so \(\Omega\ne0\).
For \(g=1\), \((d')^3\ne0\), with the same conclusion.

More generally, \(\Omega\ne0\) for **every** polynomial \(v\)
satisfying (2).  Indeed, if \(\det(v',v)=0\), the two components of
\(v\) have constant ratio, so
\[
 v=h(x)(a,b)
\tag{12}
\]
for a constant vector \((a,b)\ne(0,0)\).  Equation (2) says
\[
 h(x)\bigl(bp_0'(x)-aq_0'(x)\bigr)=1.
\tag{13}
\]
Both factors must therefore be constant, so \(v\) itself is
constant.  But
\[
 \deg p_0'=2g-1,\qquad \deg q_0'=3g-1
\tag{14}
\]
with nonzero leading coefficients.  No constant linear combination
\(bp_0'-aq_0'\) can equal \(1\): unequal degrees first force
\(a=0\), after which \(bp_0'\) is still nonconstant.

Since \(p_1\ne0\) and \(\Omega\ne0\), every coefficient
\[
 [y^n]P=
 \frac{(-1)^{n-1}C_{n-1}}{2^{n-1}}p_1\Omega^{n-1}
\tag{15}
\]
is nonzero.  The same argument applies to at least one coordinate
for any normal field.  Therefore (5) never terminates polynomially.

## 2. Every boundary has explicit self-collisions

Fix a primitive cube root of unity \(\zeta\), and put
\[
 c=\frac{1-\zeta^2}{u},\qquad
 \varphi(x)=x+c\,d(x)^2,
\tag{16}
\]
\[
 H_\zeta(x)=d(\varphi(x))-\zeta d(x).
\tag{17}
\]
Because \(\deg\varphi=2g\),
\[
 \deg H_\zeta=2g^2.
\tag{18}
\]
Every root \(\alpha\) of \(d\), counted with its multiplicity \(m\),
is a root of \(H_\zeta\) with exactly the same multiplicity.  To see
this, write \(x=\alpha+z\).  Then
\[
 \varphi(x)-\alpha=z+O(z^{2m}),
\]
so
\[
 H_\zeta(x)=(1-\zeta)a z^m+O(z^{m+1})
\tag{19}
\]
for a nonzero \(a\).

More exactly,
\[
 H_\zeta=dK_\zeta,\qquad
 \deg K_\zeta=2g^2-g,\qquad
 \gcd(K_\zeta,d)=1.
\tag{20}
\]
The factorization follows from (17), while the local computation
(19) proves the gcd assertion.  Since \(2g^2-g\geq1\),
\(K_\zeta\) has a root \(x_0\).  It is a nontrivial root of
\(H_\zeta\), in the precise sense that \(d(x_0)\ne0\).  For the
two-block forms \(d(0)=0\), so also \(x_0\ne0\).  Set
\(x_1=\varphi(x_0)\).  Then \(x_1\ne x_0\), while
\[
 d(x_1)=\zeta d(x_0).
\tag{21}
\]
Consequently
\[
\begin{aligned}
 q_0(x_1)-q_0(x_0)
 &= (\zeta^3-1)d(x_0)^3=0,\\
 p_0(x_1)-p_0(x_0)
 &= (\zeta^2-1)d(x_0)^2+u(x_1-x_0)=0.
\end{aligned}
\tag{22}
\]
Thus \(\gamma(x_1)=\gamma(x_0)\) with \(x_1\ne x_0\).

If a polynomial Keller completion \((P,Q)\) of this boundary were
an automorphism, its polynomial inverse restricted to \(y=0\)
would recover \(x\) from \((p_0(x),q_0(x))\), contradicting (22).
Hence every terminating completion is automatically a
counterexample.

## 3. Transverse degree at most two is impossible

We first prove a general lemma.

**Lemma.**  If \(P,Q\in\mathbf C[x,y]\) satisfy
\(J(P,Q)\in\mathbf C^*\) and
\[
 \max(\deg_yP,\deg_yQ)\leq2,
\tag{23}
\]
then \((P,Q)\) is a polynomial automorphism.

After rescaling, take \(J(P,Q)=1\).  The coefficient of \(y^3\) in
the Jacobian says that the two \(y^2\)-coefficient polynomials have
constant ratio.  A constant determinant-one target change therefore
puts the pair in the form
\[
 P=f(x)+a(x)y,\qquad
 Q=g(x)+b(x)y+h(x)y^2.
\tag{24}
\]
The three Jacobian equations are
\[
\begin{aligned}
 f'b-ag'&=1,\\
 2f'h+a'b-ab'&=0,\\
 2a'h-ah'&=0.
\end{aligned}
\tag{25}
\]

If \(h\ne0\), the last equation gives \(h=Ca^2\) for some
\(C\ne0\); the first equation shows \(a\ne0\).  The middle equation
then gives
\[
 b=a(2Cf+k)
\tag{26}
\]
for a constant \(k\).  Substitution into the first equation yields
\[
 a(Cf^2+kf-g)'=1.
\tag{27}
\]
Thus \(a\) is a nonzero constant and
\[
 g=Cf^2+kf-\frac{x}{a}+c.
\tag{28}
\]
Equations (23), (25), and (27) collapse to
\[
 Q=CP^2+kP-\frac{x}{a}+c.
\tag{29}
\]
Hence
\[
 x=a(CP^2+kP+c-Q),\qquad
 y=\frac{P-f(x)}a
\tag{30}
\]
is a polynomial inverse.

If \(h=0\), the equation \(a'b-ab'=0\) gives the same conclusion
with \(C=0\) when \(a\ne0\).  If \(a=0\), the first equation makes
\(f'\) and \(b\) nonzero constants, and the pair is triangular.
This proves the lemma.

Now suppose a completion of (1) had transverse degree at most two.
The lemma would make it an automorphism, while Section 2 proves that
its restriction to \(y=0\) is not injective.  This contradiction
proves
\[
 \boxed{
 \max(\deg_yP,\deg_yQ)\geq3
 }
\tag{31}
\]
for every possible polynomial Keller completion of the
arbitrary-\(d\) boundary.

## 4. Transverse degree three also reduces

The preceding lemma extends by one degree.

**Proposition.**  Every Keller pair satisfying
\[
 \max(\deg_yP,\deg_yQ)\leq3
\tag{32}
\]
is a polynomial automorphism.

First suppose one coordinate is linear in \(y\):
\[
 P=f(x)+a(x)y.
\tag{33}
\]
If \(Q=\sum_{j=0}^m q_j(x)y^j\), the coefficient of \(y^m\)
in \(J(P,Q)\) is
\[
 ma'q_m-aq_m'=0.
\tag{34}
\]
For \(a\ne0\), this says \(q_m=C_ma^m\).  Subtracting
\(C_mP^m\) from \(Q\) and descending on \(m\) gives
\[
 Q=H(P)+r(x).
\tag{35}
\]
The remaining Jacobian equation is
\[
 -a(x)r'(x)\in\mathbf C^*.
\tag{36}
\]
Thus \(a\) and \(r'\) are nonzero constants, and (35) gives a
polynomial inverse.  If \(a=0\), the equation
\(f'Q_y\in\mathbf C^*\) makes the pair triangular.  Hence every
Keller pair with one coordinate of \(y\)-degree at most one is an
automorphism.

If both coordinates initially have \(y\)-degree three, the
coefficient of \(y^5\) in their Jacobian says that their leading
coefficients have constant ratio.  A constant target change
therefore makes one coordinate have degree at most two.  Section 3
and the preceding paragraph leave only the possibility
\[
 \deg_yP=2,\qquad \deg_yQ=3.
\tag{37}
\]
We show that this degree pair cannot occur.

Let \(c(x)y^2\) and \(k(x)y^3\) be the leading terms of \(P,Q\).
The coefficient of \(y^4\) in the Jacobian is
\[
 3c'k-2ck'=0.
\tag{38}
\]
Thus \(k^2\) is a nonzero constant multiple of \(c^3\).
Unique factorization in \(\mathbf C[x]\), followed by harmless
constant target rescalings, gives
\[
 c=s^2,\qquad k=s^3
\tag{39}
\]
for a nonzero polynomial \(s\).

Complete the square over \(\mathbf C(x)\):
\[
 T=s(x)y+t(x),\qquad
 P=T^2+R(x),
\tag{40}
\]
and write
\[
 Q=T^3+B(x)T^2+C(x)T+D(x).
\tag{41}
\]
Because
\[
 J_{x,y}(P,Q)=s(x)J_{x,T}(P,Q),
\tag{42}
\]
comparison of the \(T^3,T^2,T\) coefficients gives
\[
 B=b,\qquad
 C=\frac32R+c_0,\qquad
 D=bR+d_0
\tag{43}
\]
for constants \(b,c_0,d_0\).  After replacing \(Q\) by
\(Q-bP-d_0\), the pair is
\[
 P=T^2+R,\qquad
 Q=T^3+\left(\frac32R+c_0\right)T,
\tag{44}
\]
and its constant Jacobian equation is
\[
 \boxed{
 sR'\left(\frac32R+c_0\right)\in\mathbf C^*.
 }
\tag{45}
\]

Although \(T,R\) were introduced over \(\mathbf C(x)\),
polynomiality rules out every finite pole.  Indeed
\(P=T^2+R\) implies that if \(t\) has a pole, then \(R\) has twice
its order and leading term \(-t^2\).  The constant term in \(y\)
of the second polynomial in (43) then has leading part
\[
 t^3+\frac32Rt=-\frac12t^3,
\tag{46}
\]
which cannot be polynomial.  A pole of \(R\) without a pole of
\(t\) is already impossible from \(P\).  Hence
\(t,R\in\mathbf C[x]\).

All three factors on the left of (44) are now polynomials whose
product is a nonzero constant.  Thus \(R'\) and
\(\frac32R+c_0\) would both be nonzero constants.  The first says
that \(R\) is nonconstant linear, while the second says it is
constant, a contradiction.  Therefore (45) is impossible and the
proposition follows.

Combining the proposition with Section 2 strengthens (31) to
\[
 \boxed{
 \max(\deg_yP,\deg_yQ)\geq4
 }
\tag{47}
\]
for every possible polynomial Keller completion of the
arbitrary-\(d\) boundary.

## 5. Transverse degree four also reduces

The same method closes the next degree.

**Proposition.**  Every Keller pair satisfying
\[
 \max(\deg_yP,\deg_yQ)\leq4
\tag{48}
\]
is a polynomial automorphism.

After killing one quartic leading coefficient by a constant target
change, suppose \(\deg_yQ=4\) and put \(m=\deg_yP\leq3\).
The cases \(m\leq1\) are covered by (33)--(36).  If \(m=2\), the
highest Jacobian equation is
\[
 4c'k-2ck'=0,
\tag{49}
\]
so the quartic coefficient \(k\) is a constant multiple of the
square of the quadratic coefficient \(c\).  Subtracting that
constant multiple of \(P^2\) from \(Q\) reduces to transverse degree
at most three.  It remains only to exclude
\[
 \deg_yP=3,\qquad \deg_yQ=4.
\tag{50}
\]

Let \(c(x)y^3\) and \(k(x)y^4\) be the leading terms.  The coefficient
of \(y^6\) says
\[
 4c'k-3ck'=0.
\tag{51}
\]
Unique factorization and constant rescaling therefore give
\[
 c=r^3,\qquad k=r^4
\tag{52}
\]
for a nonzero polynomial \(r\).  Over \(\mathbf C(x)\), put
\[
 z=ry
\tag{53}
\]
and write
\[
\begin{aligned}
 P&=f+Az+Bz^2+z^3,\\
 Q&=g+Dz+Ez^2+Hz^3+z^4.
\end{aligned}
\tag{54}
\]
Successively setting the \(z^5,z^4,z^3,z^2\) Jacobian
coefficients to zero gives, after harmless constant target shears,
\[
\begin{aligned}
 H&=\frac43B,\\
 E&=\frac29B^2+\frac43A+C,\\
 D&=\frac23CB+\frac49AB-\frac4{81}B^3+\frac43f+K,\\
 g&=\frac{
 54A^2-36AB^2+162AC+5B^4-27B^2C
 +81BK+108Bf}{243}+L,
\end{aligned}
\tag{55}
\]
where \(C,K,L\) are constants.

Depress the cubic by
\[
 T=z+\frac B3,\qquad
 p=A-\frac{B^2}3,\qquad
 q=f-\frac{AB}3+\frac{2B^3}{27}.
\tag{56}
\]
Equations (54)--(55) become the compact normal form
\[
\begin{aligned}
 P={}&T^3+pT+q,\\
 Q={}&T^4+\left(\frac43p+C\right)T^2
       +\left(\frac43q+K\right)T\\
    &+\frac29p^2+\frac23Cp+L.
\end{aligned}
\tag{57}
\]
Since \(J_{x,y}=rJ_{x,T}\), its two remaining equations are
\[
 \frac d{dx}
 \left(\frac{4pq+3Kp+6Cq}{3}\right)=0
\tag{58}
\]
and
\[
 r\frac d{dx}
 \left(
 -\frac13Cp^2-\frac4{27}p^3
 +Kq+\frac23q^2
 \right)\in\mathbf C^*.
\tag{59}
\]

We must justify passing from rational to polynomial \(p,q,T\).
Write \(T=ry+t(x)\).  If \(p\) and \(q\) had poles at the same
finite point, the product term \(pq\) in the first integral (58)
would dominate its linear terms, an impossibility.  If \(p\) alone
had a pole, polynomiality of the constant term
\[
 P(x,0)=t^3+pt+q
\tag{60}
\]
has two possibilities.  If \(t\) has a pole, then
\(p\sim-t^2\), and substitution in the constant term of \(Q\) in
(57) leaves the nonzero leading term \(-t^4/9\).  If \(t\) is
regular, it must vanish deeply enough that \(pt\) is regular, but
then the term \(2p^2/9\) is the unique highest pole in \(Q(x,0)\).
Both possibilities are impossible.  The case where \(q\) alone has
a pole forces \(t\) to have a pole and \(q\sim-t^3\), after which
the leading term of \(Q(x,0)\) is \(-t^4/3\).  Finally, a pole of
\(t\) with regular \(p,q\) is already impossible in (60).  Thus
\[
 t,p,q\in\mathbf C[x].
\tag{61}
\]

Let the constant in (58), multiplied by three, be \(I\).  Then
\[
 (4p+6C)q=I-3Kp.
\tag{62}
\]
If \(p\) is nonconstant, polynomial division forces
\[
 q=-\frac{3K}{4}
\tag{63}
\]
(and the corresponding constant remainder must vanish).  Hence
one of \(p,q\) is constant; the same statement is immediate if
\(p\) itself is constant.

The bracket in (59) must be a nonconstant affine polynomial,
because its derivative times the polynomial \(r\) is a nonzero
constant.  If \(p\) is nonconstant and \(q\) constant, however,
that bracket has degree \(3\deg p\).  If \(p\) is constant and
\(q\) nonconstant, it has degree \(2\deg q\).  If both are
constant, its derivative is zero.  Every case is impossible.
This excludes (50) and proves the proposition.

Combining the proposition with the collision theorem strengthens
(47) to
\[
 \boxed{
 \max(\deg_yP,\deg_yQ)\geq5
 }
\tag{64}
\]
for every possible polynomial Keller completion of the
arbitrary-\(d\) boundary.

## 6. Prior partial-degree theorem pushes the bound to six

The preceding sections give a self-contained coefficient proof
through maximum transverse degree four.  There is a stronger prior
partial-degree result: the repaired form of Moskowicz, *A variation
on Magnus' theorem and its generalizations*, Theorem 2.7, says that
a plane Keller map is invertible whenever **either** coordinate has
\(y\)-degree at most four.  The defect in one auxiliary
number-theoretic lemma and its repair are audited in
`NONEQUIVARIANT_NORMAL_DEGREE_FOUR_EXCLUSION.md`; the present note
uses only the repaired theorem statement.

For completeness, the short repair in the present setting is as
follows.  Write \(n=\deg_yP>0\), \(r=\deg_yQ>0\), and let \(u,v\)
be the \(x\)-degrees of their leading \(y\)-coefficients.  The top
Jacobian equation gives
\[
 ru=nv.
\tag{65}
\]
If \(u=0\), then also \(v=0\).  If \(u,v>0\), writing
\[
 n=A\widetilde n,\qquad u=A\widetilde u,\qquad
 \gcd(\widetilde n,\widetilde u)=1
\]
and similarly for \(r,v\), equation (65) forces the two reduced
pairs to be identical.  Choose a sufficiently large \(L\) so that
\(\widetilde u+L\widetilde n\) is prime, and apply the source shear
\(y\mapsto y+x^L\).  The resulting total degree of \(P\) is
\[
 A(\widetilde u+L\widetilde n).
\]
If \(n\leq4\), then \(A\mid n\), so
\(A\in\{1,2,3,4\}\).  This total degree is therefore a prime, a
product of two primes, or four times a prime, precisely the classical
Magnus-type degree classes used in Moskowicz's Theorem 1.2.  When
\(u=v=0\), take \(L\) itself prime and obtain the same conclusion.
The case \(n=0\) is triangular.  This proves the partial-degree
statement without the defective simultaneous-prime lemma.

It immediately covers every pair of maximum \(y\)-degree at most
five.  If one coordinate already has degree at most four, apply the
theorem.  If both have degree five, the coefficient of \(y^9\) in
the Jacobian is
\[
 5(p_5'q_5-p_5q_5')=0.
\tag{66}
\]
Thus \(p_5/q_5\) is constant, and a constant linear target change
cancels one quintic term.  The transformed Keller map has a
coordinate of \(y\)-degree at most four, so it too is invertible.

The self-collision theorem in Section 2 therefore yields the
strongest transverse termination bound established in this note:
\[
 \boxed{
 \max(\deg_yP,\deg_yQ)\geq6.
 }
\tag{67}
\]
This last step is a corollary of prior art, not a new
partial-degree theorem.  The intrinsic Catalan extension,
self-collision polynomial, and direct degree-three/four normal
forms are the structural content developed in this note.

## Verification and exact remaining criterion

`verify_arbitrary_d_canonical_symplectic_extension_and_collision.py`
checks:

1. the Bezout identity and the closed formula (11);
2. the Catalan equation and the exact Jacobian through formal order
   seven for a nontrivial repeated-root \(d\);
3. the collision polynomial, its degree \(2g^2\), and its exact
   inherited-root multiplicity for two-block and arbitrary monic
   examples, including degree one and a repeated-root polynomial
   with no root at the origin;
4. the degree-two classification identities and polynomial inverse;
5. the degree-\((2,3)\) normal form and its impossible constant
   Jacobian equation;
6. the depressed degree-\((3,4)\) normal form, first integral, and
   terminal derivative.

The remaining all-order problem is now cleanly separated from the
canonical lift.  One must either:

* prove that every symplectic source reparametrization preserving
  the boundary eventually violates a reciprocal Laurent window; or
* find one for which the normalized series terminates.

The second outcome, together with Section 2, would be an explicit
counterexample without any further global-invertibility argument.
