# No coordinate-preserving descent of the cubic threefold Keller map

Date: 25 July 2026

## Outcome

Let
\[
F:\mathbf A^3_{\mathbf C}\longrightarrow\mathbf A^3_{\mathbf C}
\]
be the verified three-dimensional Keller map of geometric degree three.
There is no polynomial coordinate \(R\) on the target such that
\[
R\circ F
\]
is a polynomial coordinate on the source.

The point is not a bounded coordinate search.  If such a coordinate
existed, polynomial automorphisms would put the map in the form
\[
G(t,u,v)=\bigl(t,p(t,u,v),q(t,u,v)\bigr).
\tag{1}
\]
Almost every slice \(t=c\) would then be a three-sheeted polynomial
Keller map \(\mathbf A^2\to\mathbf A^2\), contradicting Orevkov's
theorem that a three-sheeted polynomial map of the complex plane
cannot have nonzero constant Jacobian.

This closes every possible source/target coordinate pair, including
wild nonlinear coordinates.  It does not close descent through a
non-coordinate polynomial whose fiber happens to be an affine plane.

## 1. The cubic map really has geometric degree three

Write the map as \(F=(A,B,C)\), where, with \(e=1+xy\),
\[
\begin{aligned}
A&=e^3z+y^2e(4+3xy),\\
B&=y+3xe^2z+3xy^2(4+3xy),\\
C&=2x-3x^2y-x^3z .
\end{aligned}
\tag{2}
\]
Exact differentiation gives
\[
\det\frac{\partial(A,B,C)}{\partial(x,y,z)}=-2.
\tag{3}
\]

Put
\[
\mathcal P(T)=CT^3-2T^2+BT-2A,\qquad
d(T)=\mathcal P'(T)=3CT^2-4T+B.
\tag{4}
\]
In the source function field,
\[
T=y+\frac1x,\qquad d(T)=\frac2x,
\tag{5}
\]
and
\[
x=\frac2{d(T)},\qquad
y=T-\frac{d(T)}2,\qquad
z=\frac54d(T)^2-\frac32T\,d(T)-\frac C8d(T)^3.
\tag{6}
\]
Thus
\[
\mathbf C(x,y,z)=\mathbf C(A,B,C)(T).
\tag{7}
\]

The cubic in (4) is irreducible over
\(\mathbf C(A,B,C)\).  Indeed, over
\(k=\mathbf C(B,C)\), it is the generic-fiber equation
\[
A=\frac12\bigl(CT^3-2T^2+BT\bigr).
\tag{8}
\]
The rational function on the right has degree three as a map
\(\mathbf P^1_T\to\mathbf P^1_A\), so
\[
[k(T):k(A)]=3.
\tag{9}
\]
Equations (7)--(9) prove
\[
\boxed{
[\mathbf C(x,y,z):\mathbf C(A,B,C)]=3.
}
\tag{10}
\]

## 2. Coordinate rectification preserves the Keller condition

Assume that \(R\in\mathbf C[A,B,C]\) is a target coordinate and
\[
r=R(A,B,C)\in\mathbf C[x,y,z]
\]
is a source coordinate.  Complete them to polynomial automorphisms
\[
\Phi=(R,S,T):\mathbf A^3_{\rm target}\xrightarrow{\sim}\mathbf A^3,
\qquad
\Psi=(r,u,v):\mathbf A^3_{\rm source}\xrightarrow{\sim}\mathbf A^3.
\tag{11}
\]
Then
\[
G=\Phi\circ F\circ\Psi^{-1}
\]
has the form (1).

The Jacobian determinant of a polynomial automorphism is a nonzero
constant: the chain rule with its polynomial inverse makes it a unit
of \(\mathbf C[x,y,z]\).  Hence \(G\) is again Keller and has the same
function-field degree three.  Since the first row of its Jacobian is
\((1,0,0)\),
\[
\det JG
=
\det\frac{\partial(p,q)}{\partial(u,v)}
\in\mathbf C^\times.
\tag{12}
\]
Therefore every specialization
\[
G_c=(p(c,u,v),q(c,u,v)):
\mathbf A^2\longrightarrow\mathbf A^2
\tag{13}
\]
has the same nonzero constant Jacobian.

Constant Jacobian alone does not yet show that (13) has degree three.
The specialization of geometric degree is the step that must be
audited.

## 3. Generic coordinate slices retain all three sheets

Let
\[
X=\operatorname{Spec}\mathbf C[t,u,v],\qquad
Y=\operatorname{Spec}\mathbf C[t,P,Q],
\]
and regard (1) as an étale, hence quasi-finite, morphism
\[
G:X\longrightarrow Y
\tag{14}
\]
over \(\mathbf A^1_t\).  Let \(K=\mathbf C(t,u,v)\) and
\(L=\mathbf C(t,p,q)\), so \([K:L]=3\).  Let
\[
\pi:Z\longrightarrow Y
\tag{15}
\]
be the normalization of \(Y\) in \(K\).  It is finite because
\(\mathbf A^3\) is Nagata and the field extension is finite.
This is also the relative normalization of \(Y\) in \(X\): if an
element of \(K\) is integral over \(\mathbf C[t,P,Q]\), then it is
integral over \(\mathbf C[t,u,v]\), and normality of the latter ring
puts the element back in \(\mathbf C[t,u,v]\).

The map (14) factors as
\[
X\xrightarrow{j}Z\xrightarrow{\pi}Y.
\tag{16}
\]
Zariski's Main Theorem identifies \(j\) as an open immersion: it is
the canonical map to the relative normalization and every point of
\(X\) is in the quasi-finite locus of \(G\).

Let \(E=Z\setminus j(X)\), with its reduced closed structure.
Since \(X\) is dense in the integral threefold \(Z\),
\(\dim E\le2\).  Finiteness of \(\pi\) makes
\[
D=\pi(E)\subsetneq Y
\tag{17}
\]
closed with \(\dim D\le2\).  Over \(Y\setminus D\), all points of the
finite normalization already lie in \(X\).  Shrinking once more by
generic flatness, there is a dense open set
\[
U\subset Y\setminus D
\tag{18}
\]
such that
\[
G^{-1}(U)\longrightarrow U
\tag{19}
\]
is finite locally free of rank three.  It is in fact finite étale
because \(G\) is étale.

Only finitely many planes
\[
Y_c=V(t-c)\simeq\mathbf A^2
\]
can be contained in the proper closed set \(Y\setminus U\): each such
plane must be an irreducible component of dimension two.  Hence, for
all but finitely many \(c\in\mathbf C\),
\[
U_c=U\cap Y_c
\]
is dense and nonempty in \(Y_c\).  Base-changing (19) gives a finite
étale rank-three map
\[
G_c^{-1}(U_c)\longrightarrow U_c.
\tag{20}
\]
Because \(G_c^{-1}(U_c)\) is a nonempty open subset of the irreducible
plane \(X_c\simeq\mathbf A^2\), (20) says exactly that
\[
\boxed{
[\mathbf C(u,v):
 \mathbf C(p(c,u,v),q(c,u,v))]=3
}
\tag{21}
\]
for general \(c\).

This avoids the two common specialization loopholes:

1. no special collision fiber is used to infer generic degree;
2. possible sheets at infinity are removed before specializing, and
   their image meets a general target plane in dimension at most one.

## 4. Orevkov contradiction

Orevkov's Theorem 1.1 states that the multiplicity of a polynomial
map \(\mathbf C^2\to\mathbf C^2\) with nonzero constant Jacobian cannot
equal three.  But (12), (13), and (21) produce exactly such a map for
every general \(c\).  This contradiction proves the claimed
coordinate-pullback exclusion.

Primary reference:

S. Yu. Orevkov, *On three-sheeted polynomial mappings of
\(\mathbf C^2\)*, Math. USSR-Izv. **29** (1987), no. 3, 587--596,
[DOI 10.1070/IM1987v029n03ABEH000984](https://doi.org/10.1070/IM1987v029n03ABEH000984);
[author PDF](https://www.math.univ-toulouse.fr/~orevkov/jc86.pdf).

The normalization and specialization steps use the relative
normalization theorem and Zariski's Main Theorem (Stacks Project,
[Tag 0BAK](https://stacks.math.columbia.edu/tag/0BAK) and
[Tag 03GW](https://stacks.math.columbia.edu/tag/03GW)), generic
flatness ([Tag 0529](https://stacks.math.columbia.edu/tag/0529)), and
the finite-flat/finite-locally-free equivalence
([Tag 02K9](https://stacks.math.columbia.edu/tag/02K9)).

## 5. The two tempting coordinate fibers are not affine planes

The first two displayed components of (2) also fail as direct source
slices for elementary topological reasons.

### 5.1 A general \(A\)-fiber

If \(a_0\ne0\), the equation \(A=a_0\) has no point on \(e=0\), while
on \(D(e)\) it uniquely determines
\[
z=
\frac{a_0-y^2e(4+3xy)}{e^3}.
\tag{22}
\]
Projection to \((x,y)\) therefore gives an isomorphism
\[
\boxed{
A^{-1}(a_0)\simeq
\mathbf A^2\setminus V(1+xy).
}
\tag{23}
\]
The deleted hyperbola is \(\mathbf G_m\), so
\[
\chi\bigl(A^{-1}(a_0)\bigr)=1-0=1.
\tag{24}
\]
The fiber is nevertheless not \(\mathbf A^2\): its coordinate ring
has the nonconstant unit \(1+xy\).

### 5.2 A general \(B\)-fiber

Fix \(b_0\ne0\).  Projection of \(B^{-1}(b_0)\) to the
\((x,y)\)-plane is an isomorphism over
\[
U=D\bigl(x(1+xy)\bigr),
\tag{25}
\]
because there
\[
z=
\frac{b_0-y-3xy^2(4+3xy)}
     {3x(1+xy)^2}.
\tag{26}
\]
There are exactly two exceptional base points:
\[
(x,y)=(0,b_0),\qquad
(x,y)=\left(\frac2{b_0},-\frac{b_0}2\right).
\tag{27}
\]
Above each, \(z\) is arbitrary, so each contributes an affine line.
The divisors \(V(x)\simeq\mathbf A^1\) and
\(V(1+xy)\simeq\mathbf G_m\) are disjoint.  Additivity of
constructible Euler characteristic gives
\[
\chi(U)=1-1-0=0
\]
and hence
\[
\boxed{
\chi\bigl(B^{-1}(b_0)\bigr)=0+1+1=2.
}
\tag{28}
\]
Thus a general \(B\)-fiber is not \(\mathbf A^2\), whose Euler
characteristic is \(1\).

These computations close the tempting transplant in which a displayed
three-dimensional source fiber was simply assumed to be an affine
plane.  They are independent of the stronger coordinate theorem above.

## 6. Publication assessment

The coordinate-slice proposition is rigorous and useful for organizing
future descents, but it is a short consequence of Orevkov's 1987
theorem plus standard relative normalization.  The fiber computations
are elementary.  This memo should be treated as a research no-go lemma,
not as a standalone publishable resolution of the plane Jacobian
conjecture.
