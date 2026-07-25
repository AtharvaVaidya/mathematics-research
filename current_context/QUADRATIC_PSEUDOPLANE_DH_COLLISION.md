# The natural \(D+H\) collision on the quadratic pseudoplane

## Scope and outcome

Let

\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad
\{u,v\}=-2w,\quad \{u,w\}=-u^2,\quad
\{v,w\}=1+2uv.
\]

The principal divisor \(w=0\) is the disjoint union

\[
D=V(u,w)\simeq\mathbf A^1_v,\qquad
H=V(1+uv,w)\simeq\mathbf G_{m,u},
\qquad \operatorname{div}(w)=D+H.
\]

Suppose a hypothetical Darboux map

\[
e=(P,Q):S=\operatorname{Spec}B\longrightarrow\mathbf A^2,
\qquad \{P,Q\}=1,
\]

maps both \(D\) and \(H\) dominantly to the same irreducible plane curve
\(\Gamma\).  This note proves two statements.

1. The restrictions to the two components have a complete normal form.
   Their values and first symplectic normal jets always glue, so there is
   no first-order boundary contradiction.
2. The **exact natural architecture**

   \[
   e^{-1}(\Gamma)=D\sqcup H
   \quad\text{scheme-theoretically}
   \]

   is impossible.  Thus the class-mate \(H\) can be the collision
   component only if the pullback of \(\Gamma\) has at least one further
   divisor (or if the residual class component is not \(H\)).

This is a conditional obstruction on the proposed collision
architecture.  It neither constructs nor rules out every Darboux pair
on \(B\), and it does not resolve the plane Jacobian Conjecture.

## 1. Classification of the two restrictions

Let \(\nu:\widetilde\Gamma\to\Gamma\) be the normalization.  The earlier
collision theorem shows that

\[
\widetilde\Gamma\simeq\mathbf A^1
\]

and that \(D\to\widetilde\Gamma\) is an isomorphism.  Choose the
normalization coordinate \(t\) so that its pullback to \(D\) is \(v\).
Write

\[
\nu(t)=(A(t),B(t)),\qquad A,B\in\mathbf C[t].
\]

Because \(e|_D\) is an immersion, \(A'\) and \(B'\) have no common zero.
In particular \(\nu\) may have transverse self-intersections but has no
cuspidal branch.

The dominant map \(H\to\Gamma\) factors uniquely through the
normalization.  Its lift is a Laurent polynomial

\[
\phi(u)\in\mathbf C[u,u^{-1}].
\]

The tangent map of \(e|_H\) never vanishes.  Since \(\nu'\) never
vanishes, \(\phi'\) has no zero on \(\mathbf C^*\).  A Laurent polynomial
with this property has

\[
\phi'(u)=c u^m.
\]

The exponent \(m=-1\) is excluded because \(u^{-1}\) has no Laurent
polynomial primitive.  Consequently

\[
\boxed{\phi(u)=b+a u^n,\qquad
       a\in\mathbf C^*,\quad b\in\mathbf C,\quad
       n\in\mathbf Z\setminus\{0\}.}
\]

Thus, after the chosen normalization,

\[
\begin{array}{c|cc}
 &P&Q\\ \hline
D&A(v)&B(v)\\
H&A(b+a u^n)&B(b+a u^n).
\end{array}
\]

Generically \(D\) supplies one sheet over \(\Gamma\), while \(H\)
supplies \(|n|\) sheets and omits the normalization value \(t=b\).
This is precisely the allowed nonproper loss of sheets; it is not a
contradiction.

## 2. First symplectic jets always glue

Along \(D\), use \(w\) as normal parameter and write

\[
\begin{aligned}
P&=A(v)+wP_{1,D}(v)+O(w^2),\\
Q&=B(v)+wQ_{1,D}(v)+O(w^2).
\end{aligned}
\]

Since \(\{v,w\}=1\) on \(D\), the Darboux equation gives

\[
A'Q_{1,D}-P_{1,D}B'=1. \tag{D1}
\]

On \(H\), the coordinates are exactly

\[
v=-u^{-1}+u^{-2}w^2,\qquad \{u,w\}=-u^2.
\]

Writing the analogous first jets and using
\(\phi=b+a u^n\) gives

\[
A'(\phi)Q_{1,H}-P_{1,H}B'(\phi)
 =-\frac1{u^2\phi'(u)}
 =-\frac1{an}u^{-n-1}. \tag{H1}
\]

The immersion condition is equivalent to
\(\gcd(A',B')=1\).  Choose \(R,S\in\mathbf C[t]\) with

\[
A'S-RB'=1.
\]

Then a simultaneous solution of (D1)--(H1) is

\[
\begin{aligned}
(P_{1,D},Q_{1,D})&=(R(v),S(v)),\\
(P_{1,H},Q_{1,H})
 &=\left(\kappa(u)R(\phi(u)),
          \kappa(u)S(\phi(u))\right),\\
\kappa(u)&=-\frac1{u^2\phi'(u)}.
\end{aligned}
\]

There is no hidden gluing constraint between these two pairs.  Indeed

\[
B/(w)
\simeq
\mathbf C[u,v]/\bigl(u(1+uv)\bigr)
\simeq \mathbf C[v]\times\mathbf C[u,u^{-1}].
\]

The two CRT idempotents are

\[
e_D=1+uv,\qquad e_H=-uv.
\]

Every Laurent monomial on \(H\) has a polynomial lift: replace
\(u^{-m}\) by \((-v)^m\).  Hence for arbitrary
\((f_D,f_H)\) the expression

\[
(1+uv)f_D(v)-uv\,\widetilde f_H(u,v)
\]

has the prescribed restrictions to \(D\) and \(H\).  Applying this
independently to the values and normal coefficients gives global
polynomials \(P^{(1)},Q^{(1)}\in B\) satisfying

\[
\{P^{(1)},Q^{(1)}\}\equiv1\pmod w.
\]

So restriction data and BF0 cannot eliminate the \(D+H\) proposal.
Polynomial termination beyond the first formal layer is essential.

## 3. The exact two-component architecture is impossible

Let \(F(X,Y)\) be an irreducible equation of \(\Gamma\), and assume now
that the full scheme-theoretic pullback is exactly \(D\sqcup H\).
Étaleness makes both multiplicities one, so

\[
\operatorname{div}(F(P,Q))=D+H=\operatorname{div}(w).
\]

Since \(B^\times=\mathbf C^\times\),

\[
F(P,Q)=c\,w,\qquad c\in\mathbf C^*. \tag{2}
\]

The differential \(dw\) is nonzero everywhere on \(D\sqcup H\).
Equation (2), together with the fact that \(de\) is an isomorphism,
therefore implies that \(dF\) is nonzero at every point of \(\Gamma\):
\(D\to\Gamma\) is surjective.  Hence \(\Gamma\) is smooth.  Its
normalization is \(\mathbf A^1\), so \(\Gamma\) is a polynomially
embedded affine line.

By the Abhyankar--Moh--Suzuki theorem, \(F\) is a coordinate of
\(\mathbf C[X,Y]\).  Choose \(G\) such that

\[
\mathbf C[F,G]=\mathbf C[X,Y],\qquad
\operatorname{Jac}(F,G)=j\in\mathbf C^*.
\]

Using (2) and \(\{P,Q\}=1\), define

\[
\widehat P=w,\qquad
\widehat Q=\frac c j G(P,Q).
\]

Then \(\widehat Q\in B\) and

\[
\{w,\widehat Q\}=1. \tag{3}
\]

It remains to observe that (3) has no polynomial solution.

Write a hypothetical solution in the reduced basis as

\[
\widehat Q=C(u,v)+wK(u,v).
\]

Its even component would have to satisfy

\[
\delta C=1,\qquad
\delta=\{w,-\}|_{\mathbf C[u,v]}
       =u^2\partial_u-(1+2uv)\partial_v. \tag{4}
\]

On \(u\ne0\), put

\[
z=u+u^2v=w^2.
\]

Then

\[
\delta z=0,\qquad
\mathbf C[u,u^{-1},v]=\mathbf C[u,u^{-1},z],
\qquad
\delta=u^2\partial_u\big|_z.
\]

Every Laurent-polynomial solution of (4) is therefore

\[
C=-u^{-1}+R(z),\qquad R\in\mathbf C[z].
\]

The term \(-u^{-1}\) has an unavoidable pole along \(u=0\), while
\(R(u+u^2v)\) is regular there.  No such expression belongs to
\(\mathbf C[u,v]\).  This contradicts (3).

We have proved:

> **Exact \(D+H\) no-go theorem.** A Darboux map on the quadratic
> pseudoplane cannot have an irreducible plane curve whose full
> scheme-theoretic inverse image is exactly \(D\sqcup H=V(w)\).

After rectifying \(\Gamma\), the forced rational target coordinate is
\(-u^{-1}+R(w^2)\).  The obstruction is thus the global incompatibility
of the two boundary sheets, not a failure of their restrictions or
first normal jets.

## 4. Consequence for the next search

The most economical realization of the class-group collision is now
closed.  If \(H\) is the additional class-\([D]\) component above
\(e(D)\), then

\[
\operatorname{div}(F(P,Q))=D+H+E'
\]

must contain a nonempty further divisor \(E'\).  The next useful
invariant is therefore the incidence and class of \(E'\), especially
its intersections with \(D\) or \(H\); another search over unrestricted
coefficients would miss the geometric reason that the two-component
case fails.

## Verification

Run

```bash
.venv/bin/python route_a/verify_dh_collision_architecture.py
```

The verifier checks the CRT splitting, the Laurent normal forms, a
nontrivial nodal-curve instance of the universal first-jet gluing, and
the invariant/rational-slice identities used in the exact no-go theorem.
