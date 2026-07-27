# Local \((4,5)\) nodal-parity squarefree-root obstruction

## Literature status

The parity ansatz studied here is globally impossible, independently
of the local argument below.  Indeed, from a solution \(F=P(x^2,y)\),
\(G=xQ(x^2,y)\), set
\[
A(X,Y)=F(Y,X),\qquad B(X,Y)=-G(Y,X).
\]
This is a Keller endomorphism commuting with
\((X,Y)\mapsto(X,-Y)\).  Moskowicz--Valqui, Proposition 4.1,
[*The Starred Dixmier Conjecture for \(A_1\)*, Communications in
Algebra **43** (2015)](https://arxiv.org/abs/1401.5141), makes it
triangular, with \(B=\lambda Y\).  The boundary condition instead
gives \(B(0,Y)=Y-Y^3\), a contradiction.

Accordingly, the result below is retained as an independent local
verification inside an ansatz already excluded by prior work.  It is
not a new global Jacobian-conjecture result or a viable construction
frontier.

## Result

Let \(K\) be a field of characteristic zero and let
\[
 P=\sum_{i=0}^4p_i(s)y^i,\qquad
 Q=\sum_{j=0}^5q_j(s)y^j
 \quad\text{in }K[s,y]
\]
satisfy
\[
 2s(P_sQ_y-P_yQ_s)-P_yQ=1,                 \tag{1}
\]
with
\[
 P(s,0)=s,\qquad Q(s,0)=s-1.               \tag{2}
\]
Suppose that their top coefficients have the forced \((4,5)\) form
\[
 p_4=\alpha s^{\,2+4k}R^4,\qquad
 q_5=\beta s^{\,2+5k}R^5,                  \tag{3}
\]
where \(\alpha,\beta\ne0\), \(k\geq0\), and \(s\nmid R\).

> **Theorem.** The polynomial \(R\) has no simple root.  In
> particular, if \(R\) is squarefree, then \(R\) is constant.

Thus the minimal branch \(k=0\) has no nonconstant squarefree seed.
In particular the proposed squarefree seed \(\deg R=12\), whose top
total degree is \(130\), is excluded without solving its coefficient
system.

The proof uses only the first three descending \(y\)-diagonals and a
local Newton-face argument at one simple zero of \(R\).  It applies to
every \(k\geq0\), although the minimal branch was the motivating case.

## 1. The first three diagonals

Write
\[
 p_3=v,\quad p_2=u,\quad p_1=a,\qquad
 q_4=e,\quad q_3=d,\quad q_2=c,
\]
and put \(w=p_4,\ f=q_5\).
The coefficient of \(y^8\) in (1) is
\[
 2s(5w'f-4wf')-4wf=0.                      \tag{4}
\]
Equation (3) satisfies (4).

The coefficient of \(y^7\), divided by \(wf\), can be written as
\[
 2sU_1'+(1+2k+2sR'/R)U_1=0,\qquad
 U_1=5\frac vw-4\frac ef.                  \tag{5}
\]
Its general solution is
\[
 U_1=C\,s^{-k-1/2}R^{-1}.
\]
Since \(U_1\in K(s)\), necessarily \(C=0\).  Consequently
\[
 h:=\frac{v}{4w}=\frac{e}{5f}.             \tag{6}
\]

Make the rational translation \(Y=y+h(s)\), or equivalently replace
\(y\) by \(Y-h(s)\).  The skew term
\(P_sQ_y-P_yQ_s\) is invariant under this simultaneous translation.
The \(Y^3\)-coefficient of \(P\) and the \(Y^4\)-coefficient of \(Q\)
vanish.  Set
\[
 A=u-6wh^2,\qquad C=d-10fh^2,               \tag{7}
\]
\[
 B=a-2uh+8wh^3,\qquad
 D=c-3dh+20fh^3.                            \tag{8}
\]
The coefficients of \(Y^6\) and \(Y^5\), respectively, give
\[
 2sU_2'+2(1+2k+2sR'/R)U_2=0,\qquad
 U_2=5\frac Aw-4\frac Cf,                  \tag{9}
\]
\[
 2sU_3'+3(1+2k+2sR'/R)U_3=0,\qquad
 U_3=5\frac Bw-4\frac Df.                 \tag{10}
\]
The even diagonal has one rational homogeneous mode, whereas the odd
diagonal has none:
\[
 U_2=\frac{\gamma}{s^{\,2k+1}R^2},\qquad
 U_3=0,\qquad \gamma\in K.                 \tag{11}
\]
Solving (6), (9), and (10) downward gives the exact recurrence
\[
 \boxed{\begin{aligned}
 e={}&5fh,\\
 d={}&\frac{5f}{4w}u+\frac52fh^2
       -\frac{\gamma f}{4s^{\,2k+1}R^2},\\
 c={}&\frac{5f}{4w}a+\frac{5f}{4w}uh
       -\frac52fh^3
       -\frac{3\gamma f h}{4s^{\,2k+1}R^2}.
 \end{aligned}}                                               \tag{12}
\]
This is the finite recurrence for the first coefficient-level
bidegree not excluded by the preceding local tests.  The squarefree
obstruction comes from its poles.

## 2. Valuations at a simple zero

It is harmless to extend \(K\) algebraically.  If \(R\) is
nonconstant and squarefree, choose a zero \(r\) and use
\(t=R(s)\) as a local parameter.  The hypothesis \(s\nmid R\)
gives \(r\ne0\).  Write \(\nu=\operatorname{ord}_t\).
All powers of \(s\), and \(\alpha,\beta\), are local units.  Hence
\[
 \nu(w)=4,\qquad \nu(f)=5,\qquad
 \nu(f/w)=1.                                \tag{13}
\]

From (12),
\[
 \nu(e)=1+\nu(v),                            \tag{14}
\]
and the three possible orders in the formula for \(d\) are
\[
 1+\nu(u),\qquad 2\nu(v)-3,\qquad 3.         \tag{15}
\]
Because \(d\) is regular, a negative second entry in (15) cannot be
cancelled by either of the other entries.  Therefore
\[
 \nu(v)\ge2.                                \tag{16}
\]
The four possible orders in the formula for \(c\) are
\[
 1+\nu(a),\qquad
 \nu(u)+\nu(v)-3,\qquad
 3\nu(v)-7,\qquad
 \nu(v)-1.                                  \tag{17}
\]
These order lists will also ensure that no lower coefficient lies
below the Newton faces used next.

## 3. Local Newton-face lemma

We use the following elementary observation.  Suppose, at a
nonzero value of \(s\), a common upper Newton face has slope
\(H>1\), and write its face terms after \(y=t^{-H}z\) as
\[
 P=t^A F(z)+\text{higher \(t\)-order},\qquad
 Q=t^B G(z)+\text{higher \(t\)-order}.
\]
For every face below, the top endpoints imply
\[
 B=\frac54A,\qquad A<0.
\]
At fixed \(y\),
\[
 P_tQ_y-P_yQ_t
 =t^{A+B+H-1}\bigl(AF G'-BF'G\bigr)+\cdots. \tag{18}
\]
In the \(t\)-coordinate the full equation is
\[
2sR'(s)(P_tQ_y-P_yQ_t)-P_yQ=1.
\]
Here \(s\), \(R'(s)\), and \(2\) are local units.  The bracket term has
one lower \(t\)-order than \(P_yQ\), and in the cases below its order
is negative.  Equation (1) therefore forces
\[
 5F'G-4FG'=0,\qquad F^5=\lambda G^4.        \tag{19}
\]
Unique factorization, together with
\(\deg F=4,\deg G=5\), gives
\[
 F=\lambda_1L^4,\qquad G=\lambda_2L^5       \tag{20}
\]
for a linear polynomial \(L\).

We now apply this observation three times.

### Step 1: \(\nu(v)\ne2\)

If \(\nu(v)=2\), take \(H=2\).  Equations (13)--(17) show that no
lower coefficient lies below the faces through the top terms.
The \(P\)-face has the shape
\[
 F(z)=w_0z^4+v_0z^3+\epsilon u_0z^2,
 \qquad w_0v_0\ne0,\quad \epsilon\in\{0,1\}. \tag{21}
\]
It is divisible by \(z^2\) and has a nonzero \(z^3\)-coefficient.
It cannot be the fourth power of a linear polynomial: a linear
polynomial proportional to \(z\) has no \(z^3\)-term in its fourth
power, while every other linear polynomial has a nonzero constant
term.  This contradicts (20).  Thus
\[
 \nu(v)\ge3,\qquad \nu(e)\ge4.              \tag{22}
\]

### Step 2: \(\nu(u)\ge2\)

Assume \(\nu(u)=j\in\{0,1\}\).  In (12), the first term of \(d\)
then has strictly smaller order than the other two, so
\[
 \nu(d)=j+1.
\]
Take
\[
 H=\frac{4-j}{2},
\]
which is \(2\) or \(3/2\).  Formula (17) shows that \(c\) does not
lie below the resulting \(Q\)-face.  The two face polynomials begin
\[
 F(z)=w_0z^4+u_0z^2,\qquad
 G(z)=f_0z^5+d_0z^3,
 \qquad w_0u_0f_0d_0\ne0.                  \tag{23}
\]
Again \(F\) is not a fourth power of a linear polynomial.  Hence
\[
 \nu(u)\ge2,\qquad \nu(d)\ge3.              \tag{24}
\]

### Step 3: \(\nu(a)\ge1\)

If \(\nu(a)=0\), (12), (17), (22), and (24) give
\[
 \nu(c)=1.
\]
Take \(H=4/3\).  The face polynomials begin
\[
 F(z)=w_0z^4+a_0z,\qquad
 G(z)=f_0z^5+c_0z^2,
 \qquad w_0a_0f_0c_0\ne0.                  \tag{25}
\]
No omitted term lies below this face, by (14)--(17) and
(22)--(24).  The first polynomial in (25) is not a fourth power of
a linear polynomial.  Therefore
\[
 \nu(a)\ge1,\qquad \nu(c)\ge2.              \tag{26}
\]

## 4. The last coefficient and contradiction

It remains to treat \(q_1=b\).  The coefficient of \(y^4\) in (1)
is a sum over
\[
 (p_0,q_5),\ (p_1,q_4),\ (p_2,q_3),\
 (p_3,q_2),\ (p_4,q_1).                    \tag{27}
\]
The first four pairs have summed valuation at least \(5\), so their
derivative terms have valuation at least \(4\).  If \(\nu(b)=0\),
the last pair has the unique order-three term
\[
 2s\,p_4'b.
\]
Its leading coefficient is nonzero because \(r\ne0\), \(R'(r)\ne0\),
\(\alpha\ne0\), and \(b(r)\ne0\).  This is impossible.  Thus
\[
 \nu(b)\ge1.                                \tag{28}
\]

Equations (22), (24), (26), and (28) say that at \(s=r\) every
positive-\(y\) coefficient of both \(P\) and \(Q\) vanishes.
Consequently
\[
 P_y(r,y)=Q_y(r,y)=0.
\]
The left side of (1) is then zero, contradicting its right side.
This proves the theorem.

## Scope

This is a complete local exclusion of every simple root in the
coefficient-level \((4,5)\) face.  It neither excludes repeated-root
\(R\) by its own argument nor resolves the Jacobian conjecture.  More
importantly, the cited equivariance theorem excludes the entire parity
ansatz, including the repeated-root case.  Therefore there is no open
counterexample seed here; any viable nodal construction must break the
global involution symmetry.
