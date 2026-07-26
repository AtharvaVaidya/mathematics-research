# Global first-layer gluing with repeated roots

Date: 26 July 2026

## Outcome

The accepted local repeated-root compact-face theorem glues at the
globally first \(P\)-layer over the fixed base polynomial \(R\).
Different roots may split through different horizontal lengths; this
does not obstruct divisibility or the reciprocal degree bound.

Let \(g\ge2\), let \(R\) be the monic degree-\(g\) polynomial
\[
R(X)=\prod_{i=1}^r(X-\alpha_i)^{e_i},
\qquad
\sum_i e_i=g,
\tag{1}
\]
and let \(1<a<b\) be coprime.  Put
\[
n=ga,\qquad m=gb,\qquad N=n+m-2.
\]
Consider an actual reciprocal polynomial Keller pair with
\[
P(X,0)=R^a,\qquad Q(X,0)=R^b,
\]
coefficient bounds
\[
\deg_X P_j\le n-j,\qquad \deg_X Q_j\le m-j,
\]
and homogenized Keller identity
\[
\tau(P_XQ_\tau-P_\tau Q_X)+nPQ_X-mQP_X=-J\tau^N,
\qquad J\ne0.
\]
If
\[
P=R^a+\tau^E T+\text{higher order},
\qquad 0<E<g,
\]
and \(E\) is the first nonzero \(P\)-order, then
\[
\boxed{
T=aR^{a-1}L,\qquad \deg L\le g-E.
}
\tag{2}
\]

The order-\(E\) coefficient of \(Q\) is
\[
\boxed{
U_E=bR^{b-1}L+cR^{\,b-E/g},
}
\tag{3}
\]
where the second summand exists as a polynomial exactly when
\[
g\mid e_iE\quad\text{for every }i.
\tag{4}
\]
The same Kummer modes describe all possible \(Q\)-only coefficients
below \(E\).

The convenient condition
\[
\gcd(g,e_1,\ldots,e_r)=1
\tag{5}
\]
uniformly eliminates every such \(Q\)-only mode at orders
\(0<j<g\).  It is not asserted to be necessary for the existence of
a Keller pair.  Under (5), the first layer of both polynomials is the
same common-root deformation:
\[
T=aR^{a-1}L,\qquad U_E=bR^{b-1}L.
\tag{6}
\]

This note proves only this fixed-base first-layer statement.  It does
not iterate the replacement \(R\mapsto R+\tau^EL\), and does not
claim a normal form modulo \(\tau^g\).

## 1. The globally first \(P\)-coefficient

Assume
\[
P=R^a+\tau^E T+\text{higher order},
\qquad
\deg T\le ga-E,
\tag{7}
\]
where \(E>0\) is minimal among the positive \(P\)-orders.  At
\(\alpha_i\), put
\[
\sigma_i=\operatorname{ord}_{\alpha_i}T,
\qquad
h_i=ae_i-\sigma_i.
\tag{8}
\]
The integer \(h_i\) can be nonpositive at an inactive root.  The
degree bound gives
\[
\sum_i\sigma_i\le\deg T\le ga-E,
\qquad\text{hence}\qquad
\boxed{\sum_i h_i\ge E.}
\tag{9}
\]

Suppose \(E<g\).  We claim
\[
h_i\le e_i\qquad\text{for every }i.
\tag{10}
\]
If \(h_i\le0\), this is immediate.  If the order-\(E\) point is not
strict, then
\[
g h_i\le e_iE<e_i g,
\]
so \(h_i<e_i\).

Now suppose the point is strict:
\[
\frac E{h_i}<\frac g{e_i}.
\tag{11}
\]
The actual first local Newton face has no larger slope and is strict.
By the local repeated-root theorem it is a common deformation
\[
s^{e_i}C_i(z),\qquad
z=\frac{\tau^{d_i'}}{s^{h_i'}},
\]
with \(\deg(C_i)h_i'\le e_i\).

The polynomial \(C_i\) need not have a linear term.  Let \(k_0\ge1\)
be its first supported positive exponent.  The first supported face
monomial has order and horizontal length
\[
(k_0d_i',\,k_0h_i').
\tag{12}
\]
Global minimality gives \(k_0d_i'\ge E\), while polynomiality gives
\[
k_0h_i'\le e_i.
\tag{13}
\]
Since the face slope is at most the slope of the order-\(E\) point,
\[
\frac{k_0d_i'}{k_0h_i'}
=\frac{d_i'}{h_i'}
\le\frac E{h_i}.
\]
Therefore
\[
h_i
\le\frac{E}{k_0d_i'}\,k_0h_i'
\le k_0h_i'
\le e_i.
\tag{14}
\]
This proves (10), including the case where the order-\(E\) point lies
strictly above the first face.

It follows that
\[
\operatorname{ord}_{\alpha_i}T\ge(a-1)e_i
\quad\text{for every }i.
\]
Hence \(R^{a-1}\mid T\), giving (2), and
\[
\deg L
\le(ga-E)-g(a-1)
=g-E.
\tag{15}
\]
The different local horizontal lengths are simply
\[
\operatorname{ord}_{\alpha_i}L=e_i-h_i.
\tag{16}
\]
They are already compatible because \(L=T/(aR^{a-1})\) is a single
global polynomial.

## 2. The exact \(Q\)-equation and Kummer modes

Write
\[
Q=R^b+\sum_{j>0}\tau^jU_j.
\]
For \(j<E\), the order-\(j\) Keller equation is
\[
\boxed{
gR\,U_j'+(j-m)R'U_j=0.
}
\tag{17}
\]
A nonzero polynomial solution exists exactly when
\[
g\mid e_i j\quad\text{for all }i,
\tag{18}
\]
and is then
\[
\boxed{
U_j=cR^{\,b-j/g}.
}
\tag{19}
\]
Indeed, at \(\alpha_i\), (17) forces
\[
\operatorname{ord}_{\alpha_i}U_j
=e_i\left(b-\frac jg\right),
\]
and the equation forbids zeros away from \(R=0\).

Define the Kummer period
\[
\kappa_R
=\operatorname{lcm}_i\frac{g}{\gcd(g,e_i)}.
\tag{20}
\]
Condition (18) is \(\kappa_R\mid j\), and
\[
\kappa_R=g
\quad\Longleftrightarrow\quad
\gcd(g,e_1,\ldots,e_r)=1.
\tag{21}
\]
Thus (5) is precisely the condition that uniformly removes
sub-\(g\) polynomial solutions of the homogeneous \(Q\)-equation.
This describes an equation kernel; it is not a necessary condition
on a Keller pair.

At order \(E\), insert \(T=aR^{a-1}L\) and put
\[
D_E=U_E-bR^{b-1}L.
\]
The common-root contribution cancels and leaves
\[
\boxed{
gR\,D_E'+(E-m)R'D_E=0.
}
\tag{22}
\]
Therefore
\[
D_E=cR^{\,b-E/g}
\tag{23}
\]
when (4) holds, and \(D_E=0\) otherwise.  In particular, under (5)
and \(E<g\), equation (6) follows.

The common part has the correct reciprocal degrees.  In the formal
first-layer replacement
\[
R\longmapsto R+\tau^EL
\tag{24}
\]
the order-\(\ell E\) binomial terms obey
\[
\begin{aligned}
\deg_X\!\left(R^{a-\ell}L^\ell\right)
&\le(a-\ell)g+\ell(g-E)=n-\ell E,
&&0\le\ell\le a,\\
\deg_X\!\left(R^{b-\ell}L^\ell\right)
&\le(b-\ell)g+\ell(g-E)=m-\ell E,
&&0\le\ell\le b.
\end{aligned}
\tag{25}
\]
This verifies compatibility of the first correction only; it is not
an induction statement.

## 3. Exact classification when there is no strict root

For this section only, drop the restriction \(E<g\).  Let
\(\tau^ET\), with \(0<E\le n\), still be the globally first nonzero
\(P\)-coefficient over the fixed base \(R^a\), and suppose it has no
strict root:
\[
g h_i\le e_iE
\qquad\text{for every }i.
\tag{26}
\]
Summing and using (1) gives \(\sum_i h_i\le E\).  Together with (9),
all inequalities are equalities:
\[
\boxed{
\sum_i h_i=E,\qquad
g h_i=e_iE\quad\text{for every }i.
}
\tag{27}
\]
The degree of \(T\) also saturates its reciprocal bound.

Equation (27) is integral exactly when \(\kappa_R\mid E\).  It forces
\[
\sigma_i=e_i\left(a-\frac Eg\right),
\]
and saturation gives
\[
\boxed{
T=cR^{\,a-E/g}.
}
\tag{28}
\]
Under (5), \(g\mid E\).  Writing \(E=gr\) gives the familiar
fixed-base sectors
\[
\boxed{
T=cR^{a-r},\qquad 1\le r\le a.
}
\tag{29}
\]
At such an order the corresponding coefficient
\(c'R^{b-r}\) in \(Q\) is independent at the initial-bracket level.
This is the relative \(g\)-sector data that a common-root quotient
must retain.

## 4. CRT interpretation and exact obstruction

If full local first-layer factor jets
\[
L_i\pmod{(X-\alpha_i)^{e_i}}
\]
are prescribed, the Chinese remainder theorem gives a unique class
\[
[L]\in\mathbb C[X]/(R),
\]
with representative of degree less than \(g\).  Reciprocal gluing at
order \(E<g\) requires
\[
\deg L\le g-E.
\tag{30}
\]
Thus arbitrary local data have an obstruction in
\[
\mathbb C[X]_{<g}/\mathbb C[X]_{\le g-E},
\tag{31}
\]
an \((E-1)\)-dimensional space.  For the actual first coefficient
\(T\), equations (2) and (15) show that its quotient \(L\)
automatically passes this test.

For example, take
\[
R=X^2(X-1),\qquad g=3,\qquad E=2.
\]
The local conditions
\[
L\equiv0\pmod{X^2},\qquad L(1)=1
\]
have CRT representative \(L=X^2\), whose degree is
\(2>g-E=1\).  They cannot arise from a reciprocal first coefficient.

If (5) fails, a Kummer mode is a reciprocal-compatible obstruction
to identifying the two first coefficients with one common \(L\).
The smallest example is
\[
g=2,\qquad R=X^2,\qquad
P=R^a,\qquad
Q=R^b+c\tau R^{\,b-1/2}.
\tag{32}
\]
For \(a=2,b=3\),
\[
P=X^4,\qquad Q=X^6+c\tau X^5.
\]
Its homogenized bracket is identically zero, and the added
coefficient has degree \(5=m-1\).  It is not a common polynomial root
shift.

The smallest example with two distinct repeated factors is
\[
g=4,\qquad R=X^2(X-1)^2,\qquad
Q=R^b+c\tau^2R^{\,b-1/2}.
\tag{33}
\]
Its bracket contribution also vanishes identically and has degree
\(m-2\).  These examples are homogeneous kernel modes, not solutions
of the inhomogeneous Keller equation.

## 5. Scope

This theorem concerns the globally first residual layer over the fixed
base \(R\).  It proves:

* divisibility and the sharp degree bound for the first \(P\)-term;
* the exact first-layer \(Q\)-equation and all of its Kummer modes;
* simultaneous first-layer gluing when no such mode exists; and
* the exact no-strict and CRT classifications.

It does **not** iterate the correction.  After
\(R\mapsto R+\tau^EL\), repeated factors may split and the next
Newton support need not be governed by the original multiplicities.
Covariance of the bracket under a \(\tau\)-dependent coordinate does
not by itself control that new support or preserve the hypotheses of
the fixed-base theorem.  Consequently no normal form modulo
\(\tau^g\) is claimed here.
