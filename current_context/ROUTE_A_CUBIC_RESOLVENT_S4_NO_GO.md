# Route A: the canonical double cover is compatible with an \(S_3\) cubic

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad S=\operatorname {Spec}B.
\]
The canonical quadratic extension \(K(\sqrt u)/K\), where
\(K=\operatorname {Frac}B\), is unramified at every height-one prime of
\(S\).  It is tempting to compare it with the quadratic extension of a
hypothetical non-Galois cubic \(K/L\) that completes \(K/L\) to its
\(S_3\)-Galois closure.

That comparison cannot give a contradiction.  There is an exact
generically cubic map on this same surface for which

1. \(K/L\) is the cubic resolvent of a generic \(S_4\)-quartic and has
   \(S_3\)-Galois closure;
2. \(K(\sqrt u)/K\) is the canonical unramified double cover;
3. the quadratic extension completing the cubic to its \(S_3\)-closure
   is instead ramified along a principal retained sheet; and
4. adjoining \(\sqrt u\) produces the degree-six edge field of the
   \(S_4\)-quartic.

Thus the class group, \(\pi _1(S)=\mathbf Z/2\), purity, and branch
monodromy are mutually compatible.  The example is not a Darboux map:
its bracket vanishes on two curves and it contracts the distinguished
double fiber.  Étaleness and quasi-finiteness, rather than the abstract
resolvent comparison, remain the essential missing input.

## 1. The canonical finite étale double cover

The integral closure of \(B\) in \(K(\sqrt u)\) is
\[
\widetilde B
=
\mathbf C[a,v,z]/(z^2-1-a^2v),
\tag{1}
\]
with
\[
u=a^2,\qquad w=az.
\tag{2}
\]
The involution
\[
(a,v,z)\longmapsto(-a,v,-z)
\tag{3}
\]
is free, since a fixed point would have \(a=z=0\), contrary to (1).
Its invariant ring is \(B\).  Hence
\[
\widetilde S=\operatorname {Spec}\widetilde B\longrightarrow S
\tag{4}
\]
is a connected finite étale double cover.  This also matches
\[
\operatorname {div}_S(u)=2D,\qquad D=V(u,w).
\tag{5}
\]

## 2. An exact cubic resolvent on \(S\)

Define
\[
P=w,\qquad
Q=\frac{u(u+2-v)}4.
\tag{6}
\]
The surface equation gives
\[
P^2=u(u+1)^2-4Qu.
\tag{7}
\]
Consequently \(u\) is a root of
\[
r(T)=T(T+1)^2-4QT-P^2.
\tag{8}
\]
Conversely, away from \(u=0\),
\[
w=P,\qquad v=u+2-\frac{4Q}{u},
\tag{9}
\]
so
\[
K=\mathbf C(P,Q)(u).
\tag{10}
\]

Equation (8) is the cubic resolvent of
\[
q(Z)=Z^4+Z^2+PZ+Q.
\tag{11}
\]
Indeed, after adjoining \(s^2=T\), it factors as
\[
q(Z)
=
\left(
Z^2-sZ+\frac{T+1+P/s}{2}
\right)
\left(
Z^2+sZ+\frac{T+1-P/s}{2}
\right),
\tag{12}
\]
where juxtaposition denotes multiplication.  The equality follows from
(8).

The generic Galois group of (11) over \(\mathbf C(P,Q)\) is \(S_4\).
First, (11) is irreducible because the rational map
\[
Z\longmapsto Z^4+Z^2+PZ
\]
has degree four over \(\mathbf C(P)\).  Next,
\[
Q=\frac{T(T+1)^2-P^2}{4T}
\]
has degree three as a rational function of \(T\), so the cubic resolvent
(8) is irreducible.  The quartic group therefore acts transitively on
the three resolvent partitions.  Finally, the discriminant (16) has odd
\(Q\)-degree three, so it is not a square in \(\mathbf C(P,Q)\).
The group is consequently \(S_4\), rather than \(A_4\).

As an independent arithmetic cross-check, specialize to
\[
q_0(Z)=Z^4+Z^2+Z+1.
\tag{13}
\]
Its discriminant is \(257\).  Modulo \(3\), \(q_0\) is irreducible,
giving a four-cycle; modulo \(2\),
\[
q_0=(Z+1)(Z^3+Z^2+1),
\tag{14}
\]
giving a three-cycle.  Thus its Galois group is the full \(S_4\), and
it matches the generic calculation.

It follows that (8) is an \(S_3\)-cubic over
\(L=\mathbf C(P,Q)\).  The field
\[
K(\sqrt u)
\tag{15}
\]
is the degree-six field that chooses one of the two edges in a resolvent
partition.  Its normal closure over \(L\) has group \(S_4\).  In
particular the canonical double cover is perfectly compatible with the
non-Galois cubic.

## 3. The discriminant extension is different

The discriminants of (8) and (11) are equal:
\[
\Delta(P,Q)
=
-27P^4+144P^2Q-4P^2
+256Q^3-128Q^2+16Q.
\tag{16}
\]
Substitution of (6), followed by the relation
\(w^2=u+u^2v\), gives the exact factorization
\[
\boxed{
\Delta(P,Q)
=
u\,(u-4v+4)\,
\left(2u^2+uv+2u+1\right)^2.
}
\tag{17}
\]
Therefore the quadratic extension completing the cubic \(K/L\) to its
\(S_3\)-Galois closure is
\[
K(\sqrt{\Delta})
=
K\!\left(\sqrt{u(u-4v+4)}\right),
\tag{18}
\]
not \(K(\sqrt u)\).

The divisor
\[
C=V(u-4v+4)
\tag{19}
\]
is a principal prime.  Indeed,
\[
B/(u-4v+4)
\simeq
\mathbf C[u,w]/\left(4w^2-u(u+2)^2\right),
\tag{20}
\]
and the polynomial on the right is irreducible.  At the generic point of
\(C\), \(u\) is a unit and \(u-4v+4\) has valuation one.  Hence (18) is
ramified along \(C\), while (15) is unramified there.

The canonical cover actually splits over the normalization of \(C\):
equation (20) gives
\[
\sqrt u=\frac{2w}{u+2}\qquad\text{in }\operatorname {Frac}(C).
\]
This is the six-edge action of a quartic transposition: two edges are
fixed and the other four are exchanged in two pairs, with cycle type
\(2^2 1^2\).

This is exactly the distinction forced in the cubic branch-section
audit: the discriminant double cover ramifies on the retained simple
sheet, whereas the canonical double cover extends étale over all of
\(S\).

## 4. Exact branch geometry and exact failure of étaleness

Put
\[
R=2u^2+uv+2u+1.
\tag{21}
\]
For the Route A bracket
\[
\{u,v\}=-2w,\qquad
\{u,w\}=-u^2,\qquad
\{v,w\}=1+2uv,
\tag{22}
\]
one obtains
\[
\boxed{\{P,Q\}=\frac{uR}{4}.}
\tag{23}
\]
Also
\[
r'(u)=R.
\tag{24}
\]
Thus \(E=V(R)\) is the ramified double sheet, and its square in (17) is
the usual cubic discriminant multiplicity.  The principal curve \(C\)
occurs with multiplicity one and is the retained unramified sheet.

The remaining factor \(u\) in (17) contributes \(2D\) because of (5).
It is vertical rather than a branch sheet:
\[
P|_D=Q|_D=0.
\tag{25}
\]
Accordingly the model fails the two hypotheses an actual Route A
Darboux map would satisfy:

- the bracket (23) vanishes on \(D\cup E\);
- the entire curve \(D\) is contracted to the origin.

Those failures are sharp.  On the retained curve \(C\), the bracket is
generically nonzero, and the class-zero \(2+1\) cubic branch geometry is
exactly the allowed one.

## 5. Consequence for the cubic strategy

No argument using only

- \(\operatorname {Cl}(B)=\mathbf Z/2\);
- \(\pi _1(S)=\mathbf Z/2\);
- the canonical étale cover \(K(\sqrt u)/K\);
- purity of branch;
- the \(S_3\) quadratic resolvent; or
- transposition monodromy and the principal retained sheet

can exclude the generic cubic.  Equations (6)--(25) realize all of them
simultaneously on the actual Route A surface.

A successful cubic exclusion must use a condition absent here, such as
the constant bracket to prevent \(D\cup E\), or quasi-finiteness to
prevent the contraction (25).  In particular, identifying the
canonical cover with the discriminant cover is not a valid next step.

## 6. Construction-first closure of the quartic-resolvent ansatz

There is nevertheless a useful positive obstruction if one tries to
correct (6) while retaining its exact quartic-resolvent form.  Fix a
constant \(c\ne0\), and suppose
\[
P^2=u(u+c)^2-4Qu.
\tag{26}
\]
The case above is \(c=1\).

Since \(P^2\in(u)\subset D=(u,w)\) and \(D\) is prime, \(P\in D\).
Consequently
\[
P=wA+uH
\tag{27}
\]
for some \(A,H\in B\).  Conversely, every expression (27) makes the
quotient in (26) polynomial, because
\[
\frac{P^2}{u}
=(1+uv)A^2+2wAH+uH^2.
\tag{28}
\]
Thus every polynomial correction that preserves (26) is parametrized
exactly by
\[
\begin{aligned}
P&=wA+uH,\\
Q&=\frac{(u+c)^2}{4}
-\frac{(1+uv)A^2+2wAH+uH^2}{4}.
\end{aligned}
\tag{29}
\]

Write
\[
A_0(v)=A(0,v,0).
\tag{30}
\]
On the reduced double fiber \(D\simeq\mathbf A^1_v\),
\[
P|_D=0,\qquad
Q|_D=\frac{c^2-A_0(v)^2}{4}.
\tag{31}
\]
This already conflicts with the mandatory birational collision theorem.
If \(A_0\) is constant, \(D\) is contracted.  If
\(\deg A_0=d>0\), the restriction \(D\to\overline{F(D)}\) has degree
\(2d\), rather than degree one.

At \(u=w=0\), the only surviving Poisson coefficient is
\(\{v,w\}=1\).  Taking the first normal jets of (29) therefore gives
\[
\boxed{
\{P,Q\}|_D
=
\frac12 A_0(v)^2 A_0'(v).
}
\tag{32}
\]

If \(\{P,Q\}=\lambda\in\mathbf C^\times\), equation (32) would imply
\[
\left(A_0^3\right)'=6\lambda.
\tag{33}
\]
There is no polynomial solution: a constant \(A_0\) makes the left side
zero, while a nonconstant polynomial of degree \(d\) makes it have
degree \(3d-1\ne0\).  Hence
\[
\boxed{
\text{no polynomial Darboux pair can satisfy the exact resolvent
identity (26).}
}
\tag{34}
\]

This is stronger than the failure of the seed (6): it closes every
polynomial correction that keeps \(u\) as the cubic resolvent coordinate
of \(Z^4+cZ^2+PZ+Q\).

The linearization also explains why a naive first correction looks
misleadingly viable.  Around \(A_0=1\), writing
\(A_0=1+\varepsilon a(v)+O(\varepsilon^2)\), equation (32) begins with
\[
\{P,Q\}|_D=\frac{\varepsilon}{2}a'(v)+O(\varepsilon^2).
\tag{35}
\]
The first row can be solved by \(a'=2\lambda\), but the exact equation
resums to the nonpolynomial cube root
\[
A_0(v)^3=6\lambda v+\text{constant}.
\tag{36}
\]
Thus the obstruction is nonlinear but structural, not a failure of a
bounded coefficient search.

### Polynomially varying quartic coefficient

The same boundary argument closes a larger and more natural ansatz.
Let \(C(X,Y)\in\mathbf C[X,Y]\), and suppose a Darboux pair satisfies
\[
P^2
=
u\left(u+C(P,Q)\right)^2-4Qu.
\tag{37}
\]
This says that \(u\) is the resolvent coordinate of
\[
Z^4+C(P,Q)Z^2+PZ+Q.
\tag{38}
\]

Again \(P=wA+uH\).  Put
\[
Q_0(v)=Q(0,v,0),\qquad A_0(v)=A(0,v,0).
\]
Dividing (37) by \(u\) and restricting to \(D\) gives
\[
A_0(v)^2=C(0,Q_0(v))^2-4Q_0(v).
\tag{39}
\]
On the other hand, if \(\{P,Q\}=\lambda\ne0\), then the boundary
bracket is
\[
-A_0(v)Q_0'(v)=\lambda.
\tag{40}
\]
Both factors in (40) are polynomials, so each is a nonzero constant.
Thus \(A_0\) is constant and \(Q_0\) is affine nonconstant.  As \(Q_0\)
ranges over the affine line, (39) would force
\[
C(0,Y)^2-4Y=\text{constant}
\tag{41}
\]
in \(\mathbf C[Y]\).  This is impossible: a constant \(C(0,Y)\) leaves
the linear term \(-4Y\), while a nonconstant square has even positive
degree and cannot cancel it.

Therefore (37) admits no polynomial Darboux pair.  This closes every
correction that retains \(P,Q\) as the linear and constant coefficients
of the quartic, even when its quadratic coefficient is allowed to vary
arbitrarily over the target.

In fact the coefficient need not descend from the target.  The boundary
calculation proves the following source-ring statement.

> **Quartic-resolvent Darboux obstruction.**  There are no
> \(b,c,a\in B\) and \(\lambda\in\mathbf C^\times\) such that
> \[
> \{b,c\}=\lambda,\qquad
> b^2=u(u+a)^2-4uc.
> \tag{42}
> \]

Indeed \(b=wA+uH\).  If \(a_0,c_0,A_0\) denote restriction to \(D\),
division by \(u\) and restriction give
\[
A_0^2=a_0^2-4c_0,
\tag{43}
\]
while the bracket gives
\[
-A_0c_0'=\lambda.
\tag{44}
\]
Thus \(A_0\) is a nonzero constant and \(c_0\) is affine nonconstant.
Equation (43) would make the polynomial square \(a_0^2\) affine
nonconstant, which is impossible.

This is the maximal conclusion of the construction: any surviving
quartic interpretation must use resolvent coefficients \(b,c\) that do
not themselves form a Darboux pair.  Abstract \(S_4/S_3\) monodromy
places no such requirement on those coefficient functions.
