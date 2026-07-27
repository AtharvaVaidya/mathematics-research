# Nodal-curve Keller thickenings: rank-one and parity-face obstructions

Date: 26 July 2026

## Outcome

Consider the noninjective polynomial immersion
\[
\gamma(x)=(x^2,x^3-x).
\tag{1}
\]
It has the collision \(\gamma(1)=\gamma(-1)=(1,0)\), while
\[
\gcd(2x,3x^2-1)=1.
\]
Consequently a polynomial map with nonzero constant Jacobian whose
restriction to \(y=0\) is (1) would be a counterexample to the
two-dimensional Jacobian conjecture.

This note gives two exact obstructions to constructing such a map.

1. Every separated rank-one thickening is classified.  A
   noninjective boundary forces a nonzero quadratic obstruction, and
   the unique thickening is then an infinite algebraic square-root
   series.  Polynomial termination is impossible.
2. In the natural parity-preserving class
   \[
   F=P(x^2,y),\qquad G=xQ(x^2,y),
   \tag{2}
   \]
   the top \(y\)-face satisfies a sharp two-adic constraint.  Moreover
   \[
   \deg_yQ=1,\qquad \deg_yP=2,\qquad
   (\deg_yP,\deg_yQ)=(4,2),(4,3)
   \tag{3}
   \]
   are all impossible.

The first bidegree not excluded by the coefficient arguments alone is
\((4,5)\), whose top coefficients are forced into a power pattern.
It is not a viable counterexample seed.  The entire parity-preserving
class is already excluded by a global equivariance theorem, as follows.

### Literature closure of the parity class

Set
\[
A(X,Y)=F(Y,X),\qquad B(X,Y)=-G(Y,X).
\]
Then
\[
J_{X,Y}(A,B)=1,\qquad
A(X,-Y)=A(X,Y),\qquad B(X,-Y)=-B(X,Y).
\]
Thus the Keller endomorphism \(X\mapsto A,\ Y\mapsto B\) commutes with
the reflection \((X,Y)\mapsto(X,-Y)\).  Proposition 4.1 of
Moskowicz--Valqui,
[*The Starred Dixmier Conjecture for \(A_1\)*, Communications in
Algebra **43** (2015)](https://arxiv.org/abs/1401.5141), proves in this
case that
\[
B=\lambda Y,\qquad A=\lambda^{-1}X+g(Y^2)
\]
for some \(\lambda\in K^\times\).  But the prescribed boundary gives
\[
B(0,Y)=-G(Y,0)=Y-Y^3,
\]
a contradiction.  Hence no parity-preserving thickening satisfying
(13)--(14) exists at any bidegree.

The coefficient calculations below are retained as an independent,
elementary audit of how the obstruction appears locally.  They are
not a new global result and should not guide further construction
search.

## 1. Exact separated rank-one classification

Let \(K\) be a field of characteristic zero.  Start with any
polynomially parametrized boundary curve
\[
\gamma(x)=(p_0(x),q_0(x))
\]
and consider
\[
F=p_0(x)+p_1(x)\phi(y),\qquad
G=q_0(x)+q_1(x)\phi(y),\qquad \phi(0)=0.
\tag{4}
\]
Set
\[
R=p_0'q_1-p_1q_0',
\qquad
W=p_1'q_1-p_1q_1'.
\tag{5}
\]
A direct calculation gives
\[
J(F,G)=\phi'(y)\bigl(R(x)+W(x)\phi(y)\bigr).
\tag{6}
\]

### Theorem 1

Suppose \(\phi\) is nonconstant and \(J(F,G)=\lambda\in K^\times\).
Then \(R=r\) and \(W=w\) are constants, \(r\ne0\), and
\[
r\phi+\frac w2\phi^2=\lambda y.
\tag{7}
\]

If \(w=0\), then \(\phi=(\lambda/r)y\).  In this case the boundary
curve is injective.

If \(w\ne0\), there is a unique formal solution with \(\phi(0)=0\),
\[
\phi(y)=\frac{-r+\sqrt{r^2+2w\lambda y}}{w},
\tag{8}
\]
where the square-root branch has constant term \(r\).  This solution
is algebraic but is not a polynomial.

#### Proof

The two formal series \(1,\phi\) are linearly independent over \(K\).
Since (6) is independent of \(x\), differentiating with respect to
\(x\) gives
\[
R'(x)+W'(x)\phi(y)=0.
\]
Thus \(R,W\) are constants.  At \(y=0\), (6) shows
\(r\phi'(0)=\lambda\), so \(r\ne0\).  Integrating
\(\phi'(r+w\phi)=\lambda\) gives (7) and hence (8).

It remains to justify the injectivity statement when \(w=0\).
Since \(r\ne0\), \((p_1,q_1)\ne(0,0)\).  If \(q_1\ne0\), then
\(W=0\) gives \((p_1/q_1)'=0\); if \(q_1=0\), then \(p_1\ne0\)
and the conclusion is immediate.  Thus
\[
p_1=\alpha h,\qquad q_1=\beta h
\]
for some \(h\in K[x]\) and constants \(\alpha,\beta\), not both zero.
Now
\[
r=R=h(\beta p_0'-\alpha q_0').
\]
Both factors are units in \(K[x]\).  Hence \(h\) is constant and
\[
\beta p_0-\alpha q_0=r_0x+d
\tag{9}
\]
with \(r_0\ne0\).  Formula (9) recovers \(x\) from the point
\((p_0(x),q_0(x))\), proving injectivity.

Finally, if \(w\ne0\) and \(\phi\) were a polynomial, the product
\(\phi'(r+w\phi)=\lambda\) would make both factors units in \(K[y]\).
This contradicts \(w\ne0\), \(\lambda\ne0\), and nonconstant
\(\phi\).  \(\square\)

The key geometric conclusion is:

> A noninjective boundary cannot terminate inside a separated
> rank-one normal displacement.  The same Wronskian which permits the
> collision forces the infinite algebraic tail.

### The original exact ansatz

For
\[
F=x^2+A(y),\qquad
G=x^3-x+xB(y),\qquad A(0)=B(0)=0,
\tag{10}
\]
one obtains
\[
J(F,G)=(2B'-3A')x^2+A'(1-B).
\]
Thus \(J(F,G)=\lambda\) is equivalent to
\[
2B'=3A',
\qquad
A'(1-B)=\lambda.
\]
Consequently
\[
B=\frac32A,\qquad
A-\frac34A^2=\lambda y,
\tag{11}
\]
and the unique formal solution is
\[
\boxed{
A(y)=\frac23\bigl(1-\sqrt{1-3\lambda y}\bigr),
\qquad
B(y)=1-\sqrt{1-3\lambda y}.
}
\tag{12}
\]
For \(\lambda\ne0\), neither series is a polynomial.

## 2. The parity-preserving Keller equation

Put \(s=x^2\) and impose (2), with boundary conditions
\[
P(s,0)=s,\qquad Q(s,0)=s-1.
\tag{13}
\]
The constant-Jacobian equation is
\[
\boxed{
2s(P_sQ_y-P_yQ_s)-P_yQ=1.
}
\tag{14}
\]
At \(s=0\), equation (14) reads
\[
-P_y(0,y)Q(0,y)=1.
\]
The only units of \(K[y]\) are constants.  Using (13) at \(y=0\)
therefore gives
\[
\boxed{P(0,y)=y,\qquad Q(0,y)=-1.}
\tag{15}
\]
In particular, the \(y^i\)-coefficient of \(P\) is divisible by
\(s\) for \(i\ne1\); for \(Q\), every positive-\(y\) coefficient is
divisible by \(s\), while \(q_0=s-1\).

Write
\[
m=\deg_yP,\qquad n=\deg_yQ.
\]
The case \(n=0\) is impossible: then \(Q=s-1\), and (14) would give
\[
-(3s-1)P_y=1.
\]
Hence \(m,n\ge1\).

Let \(p_m(s)\) and \(q_n(s)\) be the top \(y\)-coefficients.  The
coefficient of \(y^{m+n-1}\) in (14) is
\[
2s(np_m'q_n-mp_mq_n')-mp_mq_n=0.
\tag{16}
\]
Taking the order at \(s=0\) gives
\[
2\bigl(n\,v_s(p_m)-m\,v_s(q_n)\bigr)=m.
\tag{17}
\]
More generally, after (17) shows that \(m\) is even, integration of
(16) in \(K(s)\) gives
\[
\boxed{p_m^n=C\,s^{m/2}q_n^m}
\tag{18}
\]
for some \(C\in K^\times\).

### Theorem 2: top-face arithmetic

Every polynomial solution of (13)--(14) must satisfy
\[
\boxed{v_2(m)>v_2(n).}
\tag{19}
\]
In particular \(m\) is even.

#### Proof

Let \(g=\gcd(m,n)\).  The left side of
\[
n\,v_s(p_m)-m\,v_s(q_n)=m/2
\]
is divisible by \(g\), so \(g\mid m/2\).  Equivalently, \(m/g\) is
even, which is exactly (19).  \(\square\)

This already excludes every odd \(m\) and every pair with equal
two-adic order, such as \((2,2)\) and \((4,4)\).

## 3. Two infinite low-support exclusions

### Theorem 3

There is no polynomial solution of (13)--(14) with \(n=1\).

#### Proof

Write
\[
Q=s-1+b(s)y,\qquad
P=\sum_{r=0}^m p_r(s)y^r.
\]
By (15), \(B=v_s(b)\ge1\), \(p_0=s\), \(p_1(0)=1\), and
\(p_r(0)=0\) for \(r\ne1\).

The top equation gives
\[
p_m=C\,s^{m/2}b^m.
\tag{20}
\]
The coefficient of \(y^r\) is the triangular recurrence
\[
2sbp_r'-r(2sb'+b)p_r
-(r+1)(3s-1)p_{r+1}
=\delta_{r0}.
\tag{21}
\]
The homogeneous equation for the first two terms in (21) has the
rational solution
\[
p_r^{\rm hom}=C_r s^{r/2}b^r.
\tag{22}
\]
It is polynomial only when \(r\) is even.  Descending from (20) in
(21), a valuation induction therefore gives
\[
v_s(p_r)\ge rB+\left\lceil\frac r2\right\rceil
\qquad (r\ge2).
\tag{23}
\]
Indeed, a particular solution at level \(r\) loses at most \(B\)
orders relative to \(p_{r+1}\), while the possible polynomial
homogeneous term (22) has order \(rB+r/2\).

Thus \(v_s(p_2)>B\).  But the \(r=1\) instance of (21) has left
side of exact order \(B\): since \(p_1(0)=1\), its leading term is
\[
-(2B+1)b_Bs^B.
\]
The \(p_2\)-term has strictly larger order.  This is a contradiction.
\(\square\)

### Theorem 4

There is no polynomial solution of (13)--(14) with \(m=2\).

#### Proof

Write
\[
P=s+a(s)y+c(s)y^2,\qquad
Q=\sum_{j=0}^n q_j(s)y^j.
\]
Here \(a(0)=1\), \(C=v_s(c)\ge1\), \(q_0=s-1\), and
\(v_s(q_j)\ge1\) for \(j\ge1\).
If \(E=v_s(q_n)\), the top equation is
\[
nC-2E=1.
\tag{24}
\]
Thus \(n,C\) are odd and \(E=(nC-1)/2\).

For \(1\le r\le n\), the coefficient of \(y^r\) is
\[
\begin{aligned}
0={}&2s(r+1)q_{r+1}
 +2sr a'q_r-2saq_r'-aq_r\\
&+2s(r-1)c'q_{r-1}-4scq_{r-1}'-2cq_{r-1},
\end{aligned}
\tag{25}
\]
where \(q_{n+1}=0\).

The \(q_r\)-group in (25) has exact order \(v_s(q_r)\), with
nonzero leading multiplier \(-(2v_s(q_r)+1)\).
Starting with \(r=n\), comparison with the \(cq_{r-1}\)-group forces
\[
v_s(q_{r-1})=v_s(q_r)-C.
\tag{26}
\]
The leading multiplier of the latter group at the forced order is a
nonzero multiple of \((n-r+1)C\), while the \(q_{r+1}\)-term has
strictly higher order.  There is a possible homogeneous resonance
when \(r\) is even: its order is
\[
\frac{(r-1)C-1}{2}.
\]
That is strictly larger than the forced particular order
\[
\frac{(2r-n-2)C-1}{2}.
\]
It therefore cannot change the descending lowest-order chain, and
(26) continues downward.

At \(r=(n+1)/2\), the forced value is \((C-1)/2\).  If \(C=1\),
this already contradicts divisibility by \(s\).  If \(C\ge3\), the
next forced value is negative.  The case \(n=1\) contradicts (25)
immediately because \(E=(C-1)/2<C=v_s(cq_0)\).
Thus no solution exists.  \(\square\)

## 4. The first two isolated bidegrees

The next two propositions use only the \(s\)-orders of the explicit
coefficient equations.  Every named order below is a positive
integer by (15).

### Proposition 5: \((m,n)=(4,2)\)

There is no polynomial solution with
\[
P=s+ay+uy^2+vy^3+wy^4,\qquad
Q=s-1+by+cy^2.
\]

Put \(C=v_s(c)\) and \(W=v_s(w)\), which are defined because
\(c,w\ne0\).
The top equation gives
\[
W=2C+1.
\tag{27}
\]
If \(b=0\) and \(v\ne0\),
the \(y^4\) equation has only the \(cv\)-group, whose multiplier
\(4v_s(v)-6C-3\) is nonzero.  Hence \(b=0\) forces \(v=0\).  Then the
\(y^3\) equation either has the \(w\)-group uniquely if \(u=0\), or
forces \(C+v_s(u)=W\).  In the latter case \(W=2C+1\) gives
\(v_s(u)=C+1\), after which the \(ac\)-group is the unique lowest term of the
\(y^2\) equation, with multiplier \(-(2C+1)\).  Thus \(b\ne0\).
Put \(B=v_s(b)\).
Now if \(v=0\), the \(bw\)-group is the sole \(y^4\) group and has
nonzero multiplier \(2W-8B-4\).  Hence \(v\ne0\), so
\(V=v_s(v)\) is defined.

In the \(y^4\) equation the two leading groups have multipliers
\[
2W-8B-4,\qquad 4V-6C-3.
\]
Neither vanishes: the first is nonzero after (27), and the second is
odd.  Hence
\[
B+W=C+V,\qquad V=B+C+1.
\tag{28}
\]
If \(u=0\), the \(y^1\) equation forces \(B=C+1\).  In the
\(y^3\) equation the \(bv\)- and \(w\)-groups must then have equal
orders, so (28) gives \(C=2B\), contrary to \(B=C+1\).  Hence
\(u\ne0\), and \(U=v_s(u)\) is defined.

The \(y^1\) equation has three possible lowest orders
\[
B,\qquad C+1,\qquad U,
\]
all with nonzero leading multipliers.  Its minimum must occur at
least twice.  There are three cases.

- If \(U=B\le C+1\), the \(y^2\) equation, using (28), forces
  \(C=2B\).  Then the \(cu\)-group in the \(y^3\) equation has unique
  order \(C+U=3B\), while the other groups have order at least
  \(4B+1\).
- If \(B=C+1\le U\), the \(y^3\) equation forces
  \(U=C+1=B\), reducing to the preceding case; but its conclusion
  \(C=2B\) is then impossible.
- If \(U=C+1\le B\), the \(y^2\) equation has its \(c\)-group, of
  order \(C\), as a unique lowest term.

Every case is contradictory.

### Proposition 6: \((m,n)=(4,3)\)

There is no polynomial solution with
\[
P=s+ay+uy^2+vy^3+wy^4,\qquad
Q=s-1+by+cy^2+dy^3.
\]

Since \(d,w\ne0\), put \(D=v_s(d)\) and \(W=v_s(w)\).
If \(c=0\), the \(y^5\) equation either has the parity-impossible
condition \(2(v_s(v)-D)=1\) when \(v\ne0\), or \(v=0\); in the latter
case the \(y^3\) equation has the \(d\)-group as its unique lowest
term.  Thus a hypothetical solution has \(c,v\ne0\).  Put \(C=v_s(c)\) and
\(V=v_s(v)\).
The top equation gives
\[
3W=4D+2,
\qquad W>D.
\tag{29}
\]
The two groups in the \(y^5\) equation have orders \(C+W\) and
\(D+V\).  Their leading multipliers are
\[
4(W-2C-1),\qquad 6V-6D-3.
\]
The second is nonzero.  The first cannot vanish, since combining
\(W=2C+1\) with (29) would give the parity-impossible equation
\(4D=6C+1\).  Therefore
\[
C+W=D+V,
\qquad V=C+W-D>C.
\tag{30}
\]
Put \(\delta=W-D=(D+2)/3>0\), so \(V=C+\delta\).
If \(b=0\), the \(y^1\) equation forces \(u\ne0\) and
\(v_s(u)=C+1\).
In the \(y^2\) equation the possible lowest orders are then
\(C,V,D+1\); since \(V>C\), cancellation forces \(C=D+1\).  The
\(ad\)-group is consequently the unique lowest term of the \(y^3\)
equation, at order \(D\), a contradiction.  Thus \(b\ne0\).  If
\(u=0\), the \(y^1\) equation forces \(v_s(b)=C+1\); the same \(y^2\)
comparison gives \(C=D+1\), and again the \(ad\)-group is uniquely
lowest in degree \(y^3\).  Thus \(u\ne0\).
Put \(B=v_s(b)\) and \(U=v_s(u)\).

As in Proposition 5, the \(y^1\) equation leaves three cases.

- If \(U=B\le C+1\), the only possible lowest orders in the \(y^3\)
  equation are \(D\) and \(B+C\), so \(D=B+C\).  The \(y^2\)
  equation then forces \(C=2B\), hence \(D=3B\), contradicting
  \(3W=4D+2\) modulo \(3\).
- If \(B=C+1\le U\), the \(y^2\) equation forces \(D+1=C\).
  The \(d\)-group is then the unique lowest term of the \(y^3\)
  equation.
- If \(U=C+1\le B\), the \(y^2\) equation again forces \(D+1=C\),
  and gives the same unique-lowest-term contradiction in degree
  \(y^3\).

All leading multipliers invoked here are nonzero: those of the
\(a c\)- and \(a d\)-groups are odd negatives, while those of the
\(bu\)- and \(cu\)-groups in the relevant cases are visibly nonzero.
\(\square\)

## 5. First coefficient-level Newton face

The first bidegree not excluded by the preceding coefficient results is
\[
\boxed{(m,n)=(4,5).}
\tag{32}
\]
Equation (18) becomes
\[
p_4^5=C\,s^2q_5^4.
\tag{33}
\]
Unique factorization gives
\[
\boxed{
p_4=\alpha s^{\,2+4k}R(s)^4,\qquad
q_5=\beta s^{\,2+5k}R(s)^5
}
\tag{34}
\]
for \(k\ge0\) and \(s\nmid R\), with a compatible relation between
\(\alpha,\beta,C\).  The minimal branch is
\[
p_4=\alpha s^2R^4,\qquad q_5=\beta s^2R^5.
\tag{35}
\]

Before applying the global equivariance theorem above, this would give
a substantially smaller search space than an unrestricted Keller
coefficient system.  If \(d=\deg_sR\), the two top monomials
in the original variables have total degrees
\[
\deg\bigl(p_4(x^2)y^4\bigr)=8d+8,\qquad
\deg\bigl(xq_5(x^2)y^5\bigr)=10d+10.
\tag{36}
\]
Thus \(d\ge12\) places this formal face at total degree at least \(130\).
It cannot extend to a Keller map because the parity class is globally
excluded.

## Scope

These calculations do not prove the Jacobian conjecture and do not
produce a counterexample.  Together with the cited theorem, they show
that the parity-preserving nodal architecture is closed and should not
consume further search time.  Independently, the calculations prove:

- exact nontermination of every separated rank-one thickening of a
  noninjective boundary;
- sharp top-face arithmetic in the full parity-preserving nodal
  class;
- four low-support exclusions, two of them infinite families; and
- a first coefficient-level high-degree Newton face, which is globally
  unrealizable because of reflection equivariance.
