# The lifted defect-one endpoint is formally unobstructed, but its degree filtration has residue-moment obstructions

Date: 26 July 2026

## Outcome

Let \(k\) be a field of characteristic zero and write
\[
F(x,y)=\sum_{i\geq 0}p_i(x)y^i,\qquad
G(x,y)=\sum_{i\geq 0}q_i(x)y^i.
\tag{1}
\]
Suppose the defect-one endpoint satisfies
\[
p_0'q_1-p_1q_0'=c,\qquad c\in k^\times.
\tag{2}
\]
There is **no obstruction in the formal completion along \(y=0\)**:
every datum (2) has an explicit extension in \(k[x][[y]]\) with
\[
J(F,G)=c
\tag{3}
\]
and with the prescribed zero- and one-jets.

The reciprocal total-degree bounds are a genuinely global extra
condition.  If
\[
\deg p_i\leq n-i,\qquad \deg q_i\leq m-i,
\tag{4}
\]
and \(p_0,q_0\) have full degrees \(n,m\), then for
\(2\leq r\leq\min(n,m)\) the equation at order \(r\) has an exact
\((r-2)\)-dimensional cokernel.  Its obstruction is the high-degree
part of one modular inverse, or, when \(q_0'\) is squarefree, a vector
of residue moments.  The order \(r=2\) equation is always uniquely
solvable, while \(r=3\) is the first possible obstruction and carries
one scalar class.

Thus a purely formal/local lifted-endpoint argument is a dead route.
The viable route is instead the finite degree-at-infinity obstruction
sequence below, coupled to the earlier repeated-root Rees data.  This
note does **not** prove that its first scalar is nonzero for every
repeated-root chain.

## 1. Explicit all-order formal lift

Put
\[
A=p_0',\qquad B=q_0',\qquad
W=p_1'q_1-p_1q_1'.
\tag{5}
\]
First consider the polynomial map with a new transverse variable
\(z\),
\[
\mathcal F(x,z)=p_0(x)+p_1(x)z,\qquad
\mathcal G(x,z)=q_0(x)+q_1(x)z.
\tag{6}
\]
Its Jacobian is
\[
J_{x,z}(\mathcal F,\mathcal G)
=Aq_1-Bp_1+z(p_1'q_1-p_1q_1')
=c+Wz.
\tag{7}
\]

There is a unique series \(\phi\in yk[x][[y]]\), with
\(\phi=y+O(y^2)\), satisfying
\[
c\phi+\frac{W}{2}\phi^2=cy.
\tag{8}
\]
Equivalently,
\[
\phi
=\sum_{r\geq1}(-1)^{r-1}C_{r-1}
\left(\frac{W}{2c}\right)^{r-1}y^r,
\tag{9}
\]
where \(C_j\) is the \(j\)-th Catalan number.  Formula (9) also covers
\(W=0\), when \(\phi=y\).

Define
\[
F=\mathcal F(x,\phi)=p_0+p_1\phi,\qquad
G=\mathcal G(x,\phi)=q_0+q_1\phi.
\tag{10}
\]
Differentiating (8) in \(y\) gives
\[
(c+W\phi)\phi_y=c.
\tag{11}
\]
The source change \((x,y)\mapsto(x,\phi(x,y))\) has Jacobian
\(\phi_y\).  Equations (7) and (11) therefore prove
\[
J_{x,y}(F,G)
=J_{x,z}(\mathcal F,\mathcal G)(x,\phi)\phi_y
=(c+W\phi)\phi_y=c.
\tag{12}
\]
Every coefficient in (9)--(10) is a polynomial in \(x\).  This is an
exact formal lift, not merely an order-by-order existence statement.
It preserves \(p_0,q_0,p_1,q_1\) exactly.

The construction normally violates (4).  Indeed, the \(r\)-th
coefficient of \(\phi\) contains \(W^{r-1}\), so its \(x\)-degree can
grow with \(r\), whereas the permitted degrees in (4) decrease and
eventually force termination.

## 2. The exact filtered recurrence

Assume now
\[
\deg p_0=n,\qquad \deg q_0=m,
\qquad n,m\geq3.
\tag{13}
\]
Thus
\[
\alpha:=\deg A=n-1,\qquad
\beta:=\deg B=m-1.
\tag{14}
\]
Identity (2) implies \(\gcd(A,B)=1\).

The coefficient of \(y^{r-1}\) in the Jacobian is
\[
\sum_{i+j=r}\left(jp_i'q_j-ip_iq_j'\right).
\tag{15}
\]
For \(r\geq2\), isolate the two terms involving the new coefficients:
\[
r(Aq_r-Bp_r)=-H_r,
\tag{16}
\]
where
\[
H_r
=\sum_{\substack{i+j=r\\i,j\geq1}}
\left(jp_i'q_j-ip_iq_j'\right).
\tag{17}
\]
If all preceding coefficients obey (4), then
\[
\deg H_r\leq n+m-r-1
=\alpha+\beta-r+1.
\tag{18}
\]

For \(2\leq r\leq\min(n,m)\), define
\[
T_r:
k[x]_{\leq\beta-r+1}\oplus
k[x]_{\leq\alpha-r+1}
\longrightarrow
k[x]_{\leq\alpha+\beta-r+1},
\qquad
T_r(q,p)=Aq-Bp.
\tag{19}
\]
This map is injective.  Indeed, \(Aq=Bp\) and \(\gcd(A,B)=1\)
give \(q=Bs,\ p=As\), while \(\deg q<\deg B\) forces \(s=0\).
Consequently,
\[
\dim\operatorname{coker}T_r=r-2.
\tag{20}
\]
In particular, \(T_2\) is an isomorphism: the second coefficient is
always uniquely determined inside the reciprocal bounds.

## 3. Modular and residue descriptions of the obstruction

Let \(h\in k[x]\) have degree at most
\(\alpha+\beta-r+1\).  Since \(A\) is invertible modulo \(B\), let
\[
q_h=\operatorname{rem}_B(A^{-1}h),
\qquad \deg q_h<\beta.
\tag{21}
\]
Then
\[
\boxed{\quad
h\in\operatorname{im}T_r
\quad\Longleftrightarrow\quad
\deg q_h\leq\beta-r+1.
\quad}
\tag{22}
\]
The forward implication follows by reducing \(h=Aq-Bp\) modulo
\(B\).  Conversely, if the right side holds, put
\[
p=\frac{Aq_h-h}{B}.
\tag{23}
\]
It is a polynomial, and the degree bound on \(h\) gives
\(\deg p\leq\alpha-r+1\).  This proves (22).

Thus the top \(r-2\) coefficients of \(q_h\), in degrees
\[
\beta-r+2,\ldots,\beta-1,
\tag{24}
\]
are a complete obstruction vector.

When \(B\) is squarefree, (22) has a residue-moment form.  For a root
\(\zeta\) of \(B\),
\[
\operatorname{res}_{x=\zeta}\frac{h(x)\,dx}{A(x)B(x)}
=\frac{h(\zeta)}{A(\zeta)B'(\zeta)}.
\tag{25}
\]
The partial-fraction expansion of \(q_h/B\) at infinity shows that
\[
h\in\operatorname{im}T_r
\quad\Longleftrightarrow\quad
\boxed{\quad
\sum_{B(\zeta)=0}
\frac{\zeta^\ell h(\zeta)}
     {A(\zeta)B'(\zeta)}
=0
\quad(0\leq\ell\leq r-3).
\ }
\tag{26}
\]
For nonsquarefree \(B\), the modular criterion (22) remains valid
without change; (26) is replaced by the corresponding higher-pole
principal-part functionals.

Applied to (16), one takes \(h=-H_r/r\).  Scalar division by \(r\)
does not affect vanishing.

## 4. The first scalar is intrinsic

At \(r=2\), let \((p_2,q_2)\) be the unique bounded solution.  Put
\[
H_3
=2p_1'q_2-p_1q_2'
 +p_2'q_1-2p_2q_1'.
\tag{27}
\]
The first obstruction is the one-dimensional class
\[
\left[-\frac{H_3}{3}\right]\in\operatorname{coker}T_3.
\tag{28}
\]

This class does not depend on the choice of degree-bounded Bezout
representative in (2).  Indeed, all such representatives differ by
\[
(p_1,q_1)\longmapsto
(p_1+\lambda A,\ q_1+\lambda B),
\qquad \lambda\in k.
\tag{29}
\]
This is precisely the change of first jet induced by the
Jacobian-one source shear
\[
(x,y)\longmapsto(x+\lambda y,y).
\tag{30}
\]
Precomposing a two-jet satisfying the equations through order one
with (30) preserves the reciprocal degree bounds.  The induced
third coefficients also obey
\(\deg p_3\leq n-3,\ \deg q_3\leq m-3\).  Comparing the coefficient of
\(y^2\) before and after the shear shows that the two values of
\(H_3\) differ by
\[
3(A\widetilde q_3-B\widetilde p_3)\in\operatorname{im}T_3.
\tag{31}
\]
Hence (28) is invariant.  For fixed \(c\), it is intrinsic to the
parametrized boundary curve \(x\mapsto(p_0(x),q_0(x))\) with its fixed
\(x\)-coordinate and degree filtration, and is independent of the
bounded Bezout representative.  No invariance under arbitrary
reparametrization is asserted.

## 5. An exact cubic witness

The cokernel is not merely formal dimension counting.  Take
\[
\begin{aligned}
p_0&=\frac{x^3}{3}+\frac{x^2}{2}+x,
&q_0&=\frac{x^3}{3}+x^2+3x,\\
p_1&=\frac{x-1}{3},
&q_1&=\frac{x}{3}.
\end{aligned}
\tag{32}
\]
Then
\[
A=x^2+x+1,\qquad B=x^2+2x+3,
\qquad Aq_1-Bp_1=1.
\tag{33}
\]
The unique bounded second coefficients are
\[
p_2=\frac{1-x}{54},\qquad q_2=-\frac{x}{54}.
\tag{34}
\]
They give
\[
H_3=-\frac1{54},
\qquad
Aq_3-Bp_3=\frac1{162}.
\tag{35}
\]
For total degrees \(n=m=3\), both \(p_3\) and \(q_3\) would have to be
constants.  Comparing the \(x^2\) and \(x\) coefficients in (35)
forces both constants to vanish, contradicting the constant term.
Thus this two-jet has no degree-three Keller extension.

Nevertheless it has the exact formal extension (10), because here
\[
W=\frac19,\qquad
\phi+\frac{\phi^2}{18}=y.
\tag{36}
\]
Its third coefficients are
\[
p_3=\frac{x-1}{486},\qquad q_3=\frac{x}{486},
\tag{37}
\]
which solve (35) but exceed the degree-three bounds.  The example
pinpoints the distinction between formal lifting and filtered
algebraization.

## 6. Scope for the repeated-root program

The formal lift in Section 1 retains every piece of repeated-root
information encoded in the zero- and one-jets.  Therefore that
jet-level information cannot create an obstruction in the formal
completion alone.  The full reciprocal boundary and the preceding
Rees chain contain additional data not encoded by those two jets.

Repeatedness of the reciprocal top boundary is also insufficient by
itself.  For example,
\[
F=y+x^2,\qquad G=x+F^2
\tag{38}
\]
has \(J(F,G)=-1\), and its reciprocal pair is
\[
P=X^2+\tau,\qquad
Q=(X^2+\tau)^2+X\tau^3.
\tag{39}
\]
Thus
\[
P(X,0)=R,\qquad Q(X,0)=R^2,\qquad R=X^2,
\tag{40}
\]
with \(R\) repeated.  This example is in the exponent-one regime, so
it does not settle the counterexample range with both normalized
exponents greater than one.  It does show that “the common boundary
has a repeated root” cannot be the missing obstruction by itself.

What remains promising is more specific: transport the earlier Rees
chain into \(p_0,p_1,p_2,q_0,q_1,q_2\), then evaluate (28), together
with any leading-diagonal conditions imposed by
\(P(X,0)=R^a,\ Q(X,0)=R^b\).  If the scalar survives deck
equivariance and is forced nonzero for \(a,b>1\), the unmatched chain
is excluded at the first genuinely global step.  If it vanishes, the
higher obstruction vector (24)--(26) supplies the exact next target.

The closed formal identity, all recurrence equations, the modular
criterion on exact test families, the cubic nonextension, and the
repeated-boundary automorphism are checked by
`verify_standard_system_lifted_endpoint_formal_and_filtered_recurrence.py`.
