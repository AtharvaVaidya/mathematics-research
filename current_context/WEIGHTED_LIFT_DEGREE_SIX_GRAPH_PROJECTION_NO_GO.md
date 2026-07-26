# No polynomial-graph/linear-projection descent of the degree-six weighted lift

Date: 25 July 2026

## Outcome

Consider the Gallagher weighted-lift counterexample in dimension three
coming from a seed of degree five, hence having generic fiber degree
six.  No polynomial graph
\[
z=g(x,y)
\tag{1}
\]
and no rank-two linear projection of its target can restrict the map
to a plane polynomial map with nonzero constant Jacobian.

This is an all-degree graph theorem, not a coefficient search.  It
also shows that retaining a known collision cannot help: the exact
six-point fiber can be placed on a polynomial graph by interpolation,
but every linear projection on every such graph has nonconstant or
zero Jacobian.

The same leading-form proof works for every weighted lift from a
degree-\(d\) seed, \(d\ge2\), on every nonconstant polynomial graph.
It also covers constant graphs whenever the lift parameter \(a\ne0\).
In particular it covers the degree-five seed audited here, for which
\[
a=-\frac{57}{34}.
\]

## 1. The exact degree-six member

The rational-collision atlas chooses
\[
G(w)=w(w+1)(w-3)(w-4)(w-5)(w+4)
\]
and
\[
\lambda=G'(0)-G'(1)=-92,\qquad H(w)=\frac{G(w)}{\lambda}.
\tag{2}
\]
Put
\[
p(w)=H'(w)-H'(0),\qquad q(w)=wH'(w)-H(w).
\tag{3}
\]
Explicitly,
\[
\begin{aligned}
p(w)={}&-\frac3{46}w^5+\frac{35}{92}w^4
 +\frac9{23}w^3-\frac{381}{92}w^2+\frac{56}{23}w,\\
q(w)={}&-\frac5{92}w^6+\frac7{23}w^5
 +\frac{27}{92}w^4-\frac{127}{46}w^3+\frac{28}{23}w^2.
\end{aligned}
\tag{4}
\]
The endpoint identities are
\[
p(0)=0,\qquad p(1)=-1,\qquad \int_0^1p(w)\,dw=0.
\tag{5}
\]
Moreover
\[
H'(0)=\frac{60}{23},\qquad H''(1)=-\frac{80}{23},
\qquad
a=-\frac{1+H''(1)}{2+H''(1)}=-\frac{57}{34}.
\tag{6}
\]

Set
\[
\begin{aligned}
u&=1+xy,&
\gamma&=1+a\,xy+x^2z,&
w&=u\gamma,\\
\alpha&=u+\frac{q(w)}{\gamma^2},&
\beta&=1+\frac{p(w)}{\gamma}.
\end{aligned}
\tag{7}
\]
The endpoint identities make
\[
F=(A,B,C)=
\left(\frac{\alpha}{x^2},\frac{\beta}{x},x\gamma\right)
\tag{8}
\]
a polynomial map.  Exact expansion gives
\[
\deg(A,B,C)=(22,21,4),\qquad \det JF=1.
\tag{9}
\]
Its generic fiber degree is six.

The roots
\[
0,-1,3,4,5,-4
\tag{10}
\]
of \(H\) reconstruct six distinct rational points over
\[
\left(0,-\frac{60}{23},1\right).
\tag{11}
\]
The verifier checks all six images exactly.  Their \(x\)-coordinates
are distinct, so a univariate interpolation polynomial \(g(x)\)
places all six points on one polynomial graph (1).  The obstruction
below is therefore not vacuous.

## 2. The restricted Jacobian for an arbitrary linear projection

Let two independent target linear forms have row vectors \(U,V\), and
put
\[
\Lambda=U\times V=(\lambda_A,\lambda_B,\lambda_C)\ne0.
\tag{12}
\]
On the graph (1), write \(A_g=A(x,y,g(x,y))\), and similarly for
\(B_g,C_g\).  Direct expansion of the wedge product gives
\[
\operatorname{Jac}_{x,y}
\bigl(U\!\cdot F_g,V\!\cdot F_g\bigr)
=
\lambda_A J(B_g,C_g)
+\lambda_B J(C_g,A_g)
+\lambda_C J(A_g,B_g),
\tag{13}
\]
where \(J(R,S)=R_xS_y-R_yS_x\).

This convention is sign-safe: the coefficient of \(J(A_g,C_g)\) is
\(-\lambda_B\), which is exactly the coefficient
\(+\lambda_B\) of \(J(C_g,A_g)\).  Reversing \(U,V\) changes every
sign simultaneously and does not affect the argument.

There is also an intrinsic version.  If
\(\mathcal V_\Lambda=\operatorname{adj}(JF)\Lambda\), then
\[
JF\,\mathcal V_\Lambda=(\det JF)\Lambda.
\]
For \(f=z-g(x,y)\), the right side of (13), up to the common
orientation convention, is
\[
\mathcal V_\Lambda(f)\big|_{f=0}.
\tag{14}
\]
Thus the graph condition is a first-order Darboux/PDE condition.
The weighted leading forms show that it has no solution before that
PDE needs to be integrated.

## 3. Highest homogeneous forms on a nonconstant graph

We first state the calculation for a general weighted lift from a
degree-\(d\) seed.  Put
\[
r=d-1,
\]
and suppose
\[
g=g_m+\text{lower-degree terms},\qquad m\ge1,
\tag{15}
\]
where \(g_m\) is homogeneous of degree \(m\) and nonzero.

If \(p_d\) is the leading coefficient of the seed, then the defining
relation \(q'=wp'/c\) gives
\[
q_{d+1}=\frac{d}{c(d+1)}p_d\ne0.
\tag{16}
\]
Since the highest term of \(\gamma\) on the graph is \(b x^2g_m\),
the highest ordinary homogeneous pieces of the three restricted
components are, up to the displayed nonzero scalar factors,
\[
\begin{aligned}
A_{\rm top}
&=q_{d+1}b^r
  x^{3d-3}y^{d+1}g_m^r,\\
B_{\rm top}
&=p_db^r
  x^{3d-3}y^dg_m^r,\\
C_{\rm top}
&=b x^3g_m.
\end{aligned}
\tag{17}
\]
In particular,
\[
A_{\rm top}
=\frac{q_{d+1}}{p_d}\,yB_{\rm top},
\quad
A_{\rm top}
=q_{d+1}y^{d+1}C_{\rm top}^{\,r},
\quad
B_{\rm top}
=p_dy^dC_{\rm top}^{\,r}.
\tag{18}
\]

For clarity, the exact useful identities following from (18) are
\[
\begin{aligned}
J(A_{\rm top},B_{\rm top})
&=-\frac{q_{d+1}}{p_d}\,
  B_{\rm top}\,\partial_xB_{\rm top},\\
J(C_{\rm top},A_{\rm top})
&=q_{d+1}(d+1)y^d
  C_{\rm top}^{\,r}\partial_xC_{\rm top},\\
J(B_{\rm top},C_{\rm top})
&=-p_dd\,y^{d-1}
  C_{\rm top}^{\,r}\partial_xC_{\rm top}.
\end{aligned}
\tag{19}
\]
Every polynomial in (19) is nonzero.  Indeed,
\(C_{\rm top}=b x^3g_m\) is a nonzero polynomial divisible by
\(x^3\), so it cannot be independent of \(x\); the same applies to
\(B_{\rm top}\).

The degrees of these three nonzero leading Jacobians are
\[
\begin{aligned}
\deg J(A_g,B_g)&=8d-7+2(d-1)m,\\
\deg J(C_g,A_g)&=4d-1+dm,\\
\deg J(B_g,C_g)&=4d-2+dm.
\end{aligned}
\tag{20}
\]
For every \(d\ge2,m\ge1\), they are strictly decreasing in the order
shown.  No lower seed term reaches the degrees in (20): increasing
the seed index by one raises the graph-substituted degree by
\(m+4>0\).

Now suppose (13) is constant.  Its highest-degree term first forces
\(\lambda_C=0\), because \(J(A_g,B_g)\) is the unique term of the
first degree in (20).  The next degree forces
\(\lambda_B=0\), and the last forces
\(\lambda_A=0\).  This contradicts (12).

Hence no nonconstant polynomial graph works.

## 4. Constant graphs for the degree-five seed

Let \(g=z_0\) be constant.  For the audited seed \(a=-57/34\ne0\).
The common top piece of \(\gamma\) is
\[
\gamma_{\rm top}=a\,xy+x^2z_0
=x(ay+z_0x).
\tag{21}
\]
Consequently
\[
C_{\rm top}=x^2(ay+z_0x),
\tag{22}
\]
and the other two leading forms still satisfy
\[
A_{\rm top}=q_6y^6C_{\rm top}^4,\qquad
B_{\rm top}=p_5y^5C_{\rm top}^4.
\tag{23}
\]
Since
\[
\partial_xC_{\rm top}=2axy+3z_0x^2\ne0,
\]
the three identities (19), now with \(d=5\), remain nonzero.
Their degrees are
\[
33,\qquad19,\qquad18.
\tag{24}
\]
The same descending-degree argument forces
\(\Lambda=0\).  Thus constant graphs do not work either.

Independently, they could not retain the displayed collision: the six
exact \(z\)-coordinates in the fiber (11) are pairwise distinct.

## 5. Relation to the cubic graph audit

For the minimal quadratic seed \(d=2\), the same three top degrees are
\[
9+2m,\qquad7+2m,\qquad6+2m.
\tag{25}
\]
Thus the polynomial-graph plus *linear target projection* obstruction
extends uniformly from the cubic member to the degree-six member and
indeed to all weighted lifts.

This is distinct from the earlier quadratic-triangular target audit.
That audit required the graph to be a component of a nonlinear target
coordinate fiber and used a discriminant identity.  Here the graph is
arbitrary and need not be preserved by any target coordinate; linearity
of the final projection instead exposes the separated weighted degrees
in (20).

## Conclusion

For the generic-degree-six Gallagher weighted lift,
\[
\boxed{
\text{no polynomial graph }z=g(x,y)
\text{ and no rank-two linear target projection}
}
\]
produce a plane Keller map.  This includes graphs containing any two,
or all six, of the known colliding points.

The weighted-lift formulas and collision atlas are from Alexis
Gallagher's
[construction note](https://github.com/algal/jacobianfun/blob/main/RESEARCH.md)
and
[exact atlas verifier](https://github.com/algal/jacobianfun/blob/main/verify_counterexamples.py);
the accompanying explanation is
[The Jacobian counterexample, explained](https://jacobianfun.org/jacobian-explained).
Those sources explicitly make no historical-priority claim for the
weighted-lift family.  The graph/projection obstruction above is an
independent deduction from their formulas.  It is a broad no-go lemma,
not a resolution of the plane Jacobian conjecture.
