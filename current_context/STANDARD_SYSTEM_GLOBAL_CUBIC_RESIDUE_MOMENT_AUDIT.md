# Cubic lifted-endpoint residue and the Rees deck orbit

Date: 26 July 2026

## Outcome

At a principal lifted endpoint, the first degree-bound obstruction is
an intrinsic residue moment.

Write
\[
F(x,y)=\sum_{i\geq0}p_i(x)y^i,\qquad
G(x,y)=\sum_{i\geq0}q_i(x)y^i,
\]
with
\[
\deg p_i\leq n-i,\qquad \deg q_i\leq m-i,
\]
where \(n,m\geq3\), and suppose
\[
A=p_0',\qquad B=q_0',\qquad
\deg A=n-1,\qquad \deg B=m-1,\qquad \gcd(A,B)=1.
\]
Normalize the first equation as
\[
Aq_1-Bp_1=c\ne0.
\]
The order-two equation has a unique bounded solution.  If
\[
H_3=
2p_1'q_2-p_1q_2'+p_2'q_1-2p_2q_1',
\qquad h_3=-\frac13H_3,
\]
then the order-three equation has a bounded solution if and only if
\[
\boxed{\quad
\Lambda_3
=
\sum_{B(\zeta)=0}
\operatorname {Res}_{x=\zeta}
\frac{h_3(x)\,dx}{A(x)B(x)}
=0.
\quad}
\]
When \(B\) is squarefree this is
\[
\Lambda_3
=\sum_{B(\zeta)=0}
\frac{h_3(\zeta)}{A(\zeta)B'(\zeta)}.
\]
Equivalently, if
\[
q_{h_3}=\operatorname {rem}(A^{-1}h_3,B),
\qquad \deg q_{h_3}<m-1,
\]
then
\[
\Lambda_3
=
\frac{[x^{m-2}]q_{h_3}}{\operatorname {lc}(B)}.
\]
Thus \(\Lambda_3=0\) is precisely the condition that
\(\deg q_{h_3}\leq m-3\).

This residue does not close the repeated-root problem.  Under a Rees
deck transformation
\[
(t,z)\longmapsto(\omega t,\omega^{-d}z),
\qquad \omega^h=1,
\]
the cubic endpoint residue on consecutive germs in a nonzero root
orbit transforms by
\[
\boxed{\Lambda_{j+1}=\omega^{-(2d+3)}\Lambda_j.}
\]
For an equivariant principal endpoint germ at a deck-fixed root, it
must therefore vanish unless
\[
h\mid 2d+3.
\]

For the exact numerical survivor
\[
(g,e,h,d,G,a,b)=(9,7,4,5,1,2,3)
\]
one has
\[
W(y)=y^3(y^4+c),\qquad c\ne0.
\]
Here \(2d+3=13\equiv1\pmod4\).  Hence, if an equivariant principal
endpoint chain reaches the fixed zero root, its cubic endpoint
residue is forced to vanish.  On the four nonzero roots the residues,
if a principal endpoint chain reaches them, have the form
\[
(\Lambda,-i\Lambda,-\Lambda,i\Lambda)
\]
after a choice of generator.  Their trace is identically zero and
their norm is
\[
-\Lambda^4.
\]
Equivalently, because the residue and the nonzero root have the same
deck character in this case, there is an undetermined scalar \(K\)
such that
\[
\Lambda_\beta=K\beta,\qquad
\sum_{\beta^4=-c}\Lambda_\beta=0,\qquad
\prod_{\beta^4=-c}\Lambda_\beta=K^4c.
\]
The root sum and root product do not force \(K\ne0\).  A new
nonhomogeneous global identity would be needed to do that.

There is an additional, decisive scope issue.  The known local
secondary survivor at a nonzero root,
\[
p=z^2+2t,\qquad q=z^3+3tz,
\]
is not a principal lifted endpoint.  Its initial derivatives are
\[
A=2z,\qquad B=3z^2,
\]
so \(\gcd(A,B)=z\), and
\[
Aq_1-Bp_1=0.
\]
It produces the scalar \(6t^2\) through the drifted Rees operator,
not through the principal Bezout equation.  Consequently no
canonical \(\Lambda_3\) can be assigned to this local face alone.
One first needs the actual compensating chain that reaches coprime
principal endpoint data.

The cubic residue is therefore a sharp test once an endpoint lift is
known, but deck trace/product arguments do not themselves construct
or exclude that lift.

## 1. The order-\(r\) equation and its codimension

The coefficient of \(y^{r-1}\) in
\[
J(F,G)=F_xG_y-F_yG_x
\]
is
\[
r(Aq_r-Bp_r)+H_r,
\]
where
\[
H_r=
\sum_{\substack{i+j=r\\i,j\geq1}}
\left(jp_i'q_j-ip_iq_j'\right).
\]
Therefore, for \(r\geq2\),
\[
r(Aq_r-Bp_r)=-H_r.
\]
The source term obeys
\[
\deg H_r\leq (n-1)+(m-1)-r+1.
\]

Put
\[
\alpha=n-1,\qquad \beta=m-1.
\]
For \(2\leq r\leq\min(n,m)\) and a polynomial \(h\) of degree at most
\(\alpha+\beta-r+1\), reduction modulo \(B\) gives the unique
candidate
\[
q_h=\operatorname {rem}(A^{-1}h,B),\qquad \deg q_h<\beta.
\]
The equation
\[
Aq-Bp=h
\]
has a solution with
\[
\deg q\leq\beta-r+1,\qquad
\deg p\leq\alpha-r+1
\]
if and only if the highest \(r-2\) coefficients of \(q_h\) vanish.
The image therefore has codimension \(r-2\).  At \(r=2\) it is the
whole target, while \(r=3\) gives the first scalar condition.

## 2. Why the scalar is a residue

For \(r=3\), the modular representative \(q_h\) has degree less than
\(\beta\), and
\[
h=Aq_h-Bp
\]
for some polynomial \(p\).  Hence
\[
\frac{h\,dx}{AB}-\frac{q_h\,dx}{B}
=-\frac{p\,dx}{A}.
\]
The right side has no pole at a zero of \(B\).  Summing residues over
the zero divisor of \(B\) gives
\[
\sum_{B(\zeta)=0}\operatorname {Res}_\zeta
\frac{h\,dx}{AB}
=
\sum_{B(\zeta)=0}\operatorname {Res}_\zeta
\frac{q_h\,dx}{B}
=\frac{[x^{\beta-1}]q_h}{\operatorname {lc}(B)}.
\]
This proof includes multiple roots of \(B\).  The evaluation formula
in the outcome is the squarefree specialization.

The same differential has no residue at infinity because
\[
\deg h\leq \alpha+\beta-2.
\]
Thus the moment may equally be computed, with the opposite sign, on
the zero divisor of \(A\).

The one-parameter change between degree-bounded first Bezout
solutions,
\[
(p_1,q_1)\longmapsto(p_1+\lambda A,q_1+\lambda B),
\]
is induced by the source shear \(x\mapsto x+\lambda y\).  Recomputing
the unique bounded second lift after that shear leaves the residue
class unchanged.  Hence \(\Lambda_3\) belongs to the endpoint data,
not to the chosen Bezout representative.

## 3. Scaling law

Consider the rescaled germs
\[
\widetilde F(x,y)=uF(\lambda x,\mu y),\qquad
\widetilde G(x,y)=vG(\lambda x,\mu y).
\]
Their order-three data satisfy
\[
\widetilde A=u\lambda A(\lambda x),\qquad
\widetilde B=v\lambda B(\lambda x),\qquad
\widetilde h_3=uv\lambda\mu^3h_3(\lambda x).
\]
At a corresponding root \(x=\zeta/\lambda\),
\[
\frac{\widetilde h_3(\zeta/\lambda)}
{\widetilde A(\zeta/\lambda)\widetilde B'(\zeta/\lambda)}
=\frac{\mu^3}{\lambda^2}
\frac{h_3(\zeta)}{A(\zeta)B'(\zeta)}.
\]
Therefore
\[
\boxed{
\widetilde\Lambda_3=\frac{\mu^3}{\lambda^2}\Lambda_3.
}
\]
The target factors \(u,v\) cancel.

Now let \(\beta_{j+1}=\omega^{-d}\beta_j\) be consecutive Rees roots,
and use centered local germs
\[
F_\beta(x,s)=p(s,\beta+x),\qquad
G_\beta(x,s)=q(s,\beta+x).
\]
Deck equivariance, with its harmless target characters
\(u_\beta,v_\beta\), gives
\[
F_{\beta_{j+1}}(x,s)
=u_\beta F_{\beta_j}(\omega^d x,\omega^{-1}s),
\qquad
G_{\beta_{j+1}}(x,s)
=v_\beta G_{\beta_j}(\omega^d x,\omega^{-1}s).
\]
Thus the next germ is obtained from the preceding one with
\[
\lambda=\omega^d,\qquad \mu=\omega^{-1},
\]
up to target characters, which cancel in the residue.  This gives
\[
\Lambda_{j+1}
=\omega^{-(2d+3)}\Lambda_j.
\]
The fixed-root assertion follows by applying the same relation to one
germ.

## 4. The numerical survivor

For
\[
e=7,\qquad h=4,\qquad k=1,
\]
the residual multiplicity is
\[
f=e-kh=3.
\]
The numerical identities are
\[
G=hg-ed=4\cdot9-7\cdot5=1,
\qquad
L=g-kd=4.
\]
After normalizing the first face, its residual polynomial is
\[
W(y)=y^3(y^4+c).
\]
The four nonzero roots form one deck orbit because
\(\gcd(d,h)=1\).

Choose \(\omega=i\).  Since \(d=5\),
\[
\omega^{-(2d+3)}=\omega^{-13}=\omega^{-1}=-i.
\]
Thus the orbit has the displayed residue vector and zero trace.
The product of its four entries is \(-\Lambda^4\).

If \(\beta^4=-c\), then the residue character agrees with the root
character:
\[
\omega^{-(2d+3)}=\omega^{-d}
\quad\text{because}\quad
2d+3\equiv d\pmod4.
\]
Hence \(\Lambda_\beta/\beta\) is deck invariant, giving the scalar
\(K\) in the outcome.  Since
\[
\prod_{\beta^4=-c}\beta=c,
\]
the product identity becomes \(K^4c\).  Neither this identity nor
the zero trace prohibits \(K=0\).

Finally, substitution into the transformed Rees operator
\[
\mathcal L(p,q)
=t(p_zq_t-p_tq_z)+2p q_z-3q p_z
\]
gives
\[
\mathcal L(z^2+2t,z^3+3tz)=6t^2.
\]
This verifies the local survivor but also displays why it is not the
principal constant-Jacobian recurrence: its ordinary Jacobian is
\(-6t\), and its first Bezout scalar is zero.

## Scope

The residue formula is an exact principal-endpoint obstruction and
the deck-character calculation is exact for an equivariant family of
such endpoint germs.  They do not prove that the unmatched Rees
chain reaches a principal endpoint, nor do they identify the
undetermined orbit amplitude \(K\).

Accordingly, this audit proves a negative conclusion about the
proposed shortcut:

> The sum and product identities of the exceptional-root orbit do
> not force a nonzero cubic endpoint obstruction in the numerical
> survivor.  The trace cancels by character, the fixed-root moment
> vanishes by symmetry, and the norm remains proportional to an
> unconstrained fourth power.

The next useful input would be an equivariant construction or
classification of the actual principal endpoint jets.  Once those
jets are known, \(\Lambda_3\) is the first exact scalar to evaluate.
