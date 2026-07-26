# Route A: finite-flat triple covers and the non-Gorenstein locus

Date: 25 July 2026

## Outcome

Let
\[
\pi:Y\longrightarrow\mathbf A^2
\]
be the finite normalization attached to a hypothetical generic
degree-three Darboux map from the quadratic pseudoplane
\[
S=\operatorname{Spec}
\mathbf C[u,v,w]/(w^2-u-u^2v)\subset Y.
\]
Then:

1. \(\pi\) is automatically finite flat of rank \(3\).
2. Locally on the base, \(Y\) is governed by four Miranda
   coefficients \(a,b,c,d\).  The non-Gorenstein locus is exactly the
   common zero locus
   \[
   V(a,b,c,d).
   \tag{1}
   \]
   Its fiber algebra is
   \[
   \mathbf C[z,w]/(z,w)^2.
   \tag{2}
   \]
3. At such a point the total space is singular, the branch equation
   has multiplicity at least four, and the underlying cubic fiber has
   one point.  Hence its local inertia is transitive.
4. Normality, \(S_3\) generic monodromy, and generically simple
   transposition branching do **not** eliminate (1).  There is an exact
   normal \(S_3\) countermodel whose only singularity is a
   non-Gorenstein cyclic quotient of type
   \(\frac13(1,1)\), while its branch is a squarefree union of four
   lines.
5. The proposed canonical-class shortcut needs correction.  Hurwitz
   and boundary-class independence show that \(K_Y\) is not
   **principal**.  They do not show that \(K_Y\) is not Cartier.
   Therefore they do not by themselves show that \(Y\) is
   non-Gorenstein.

The non-Gorenstein case remains locally and numerically possible.  It
is sharply constrained: it is the noncurvilinear length-three fiber,
and it forces a branch point of multiplicity at least four.  Any
exclusion must use the special global boundary incidence of the
quadratic pseudoplane, not normality or cubic monodromy alone.

## 1. Finite degree three implies finite flat rank three

Write
\[
T=\mathbf C[P,Q]\simeq\mathbf C[x,y],
\qquad A=\mathcal O(Y).
\]
By construction \(A\) is a finite normal domain over \(T\), with
\[
[\operatorname{Frac}A:\operatorname{Frac}T]=3.
\]

A normal two-dimensional noetherian ring satisfies \(S_2\), hence is
Cohen--Macaulay.  At a point \(p\in Y\) over \(q\in\mathbf A^2\), the
local homomorphism
\[
T_q\longrightarrow A_p
\]
has regular source, Cohen--Macaulay target, equal dimensions, and
zero-dimensional fiber.  Miracle flatness therefore makes it flat.
Since the map is finite, it is finite locally free.  Its generic rank
is three, so
\[
\boxed{\pi_*{\mathcal O}_Y
\text{ is locally free of rank }3.}
\tag{3}
\]

References:

- Stacks Project, miracle flatness, Tag
  [00R4](https://stacks.math.columbia.edu/tag/00R4).
- R. Miranda, *Triple Covers in Algebraic Geometry*, Theorems 2.7 and
  3.6:
  <https://www.math.colostate.edu/~miranda/preprints/TripleCoversInAG.pdf>.

Since every vector bundle on \(\mathbf A^2\) is trivial, one can even
write globally
\[
\pi_*{\mathcal O}_Y\simeq
{\mathcal O}_{\mathbf A^2}\oplus E
\]
with \(E\) a free rank-two trace-zero module.  The local analysis below
does not need a chosen global trivialization.

## 2. Miranda's four-coefficient algebra

Choose a local basis \(z,w\) for the trace-zero module \(E\).  A flat
triple cover has multiplication
\[
\begin{aligned}
z^2&=2A+az+bw,\\
zw&=-B-dz-aw,\\
w^2&=2C+cz+dw,
\end{aligned}
\tag{4}
\]
where
\[
A=a^2-bd,\qquad
B=ad-bc,\qquad
C=d^2-ac.
\tag{5}
\]
Equivalently, in the rank-two vector bundle with fiber coordinates
\(z,w\), the cover is cut out by
\[
\begin{aligned}
F&=z^2-az-bw-2A,\\
G&=zw+dz+aw+B,\\
H&=w^2-cz-dw-2C.
\end{aligned}
\tag{6}
\]
These are the \(2\times2\) minors of a \(2\times3\) matrix, so the
codimension-two cover is Cohen--Macaulay.

The branch equation is
\[
\begin{aligned}
D&=B^2-4AC\\
 &=b^2c^2-3a^2d^2+4a^3c+4bd^3-6abcd.
\end{aligned}
\tag{7}
\]
Miranda proves that \(D=0\) is precisely the branch divisor and that
the total-ramification locus is \(V(A,B,C)\).

## 3. Exact Gorenstein classification of length-three fibers

Let \(k\) be algebraically closed of characteristic zero.  A
commutative \(k\)-algebra of length three is a product of local
Artin algebras.  The possibilities are:

\[
\begin{array}{c|c|c}
\text{fiber algebra}&\text{support type}&\text{Gorenstein?}\\ \hline
k^3&1+1+1&\text{yes},\\
k\times k[\epsilon]/(\epsilon^2)&1+2&\text{yes},\\
k[t]/(t^3)&3\text{ curvilinear}&\text{yes},\\
k[z,w]/(z,w)^2&3\text{ noncurvilinear}&\text{no}.
\end{array}
\tag{8}
\]

For completeness, if a local length-three algebra has embedding
dimension one, its maximal ideal is principal and its socle is
one-dimensional.  If it has embedding dimension two, its Hilbert
function is \((1,2)\), its maximal ideal squares to zero, and its
socle has dimension two.  The Artin Gorenstein criterion is precisely
one-dimensional socle.

Reducing (4) modulo the maximal ideal \(m_q\) of the base shows that
the last case in (8) occurs exactly when
\[
a(q)=b(q)=c(q)=d(q)=0.
\tag{9}
\]
Thus (1) is the non-Gorenstein locus of the finite flat morphism.  This
fiberwise criterion is legitimate because a flat morphism is
Gorenstein exactly when its fibers are Gorenstein; see Stacks Project,
Tag [0C05](https://stacks.math.columbia.edu/tag/0C05).

Since the base is regular, \(Y\) is Gorenstein at a point exactly when
the finite-flat morphism is Gorenstein there.  Therefore:
\[
\boxed{
Y\text{ is non-Gorenstein over }q
\iff a,b,c,d\in m_q.
}
\tag{10}
\]

## 4. Consequences of a non-Gorenstein triple point

Assume (9).

### 4.1 It is an isolated singular point on a normal surface

The fiber is (2), so its unique point is not regular.  This also
appears as case (i) of Miranda's Proposition 5.2.  Since a normal
surface is regular in codimension one, the common zero locus (1) must
be finite for the hypothetical \(Y\).

### 4.2 The branch has multiplicity at least four

Every monomial in (7) has degree four in \(a,b,c,d\).  Hence
\[
D\in m_q^4.
\tag{11}
\]
Thus the branch multiplicity at \(q\) is at least four.  In
particular, a non-Gorenstein point is neither the ordinary
simple-branch situation nor the ordinary nodal/cuspidal
curvilinear-total-ramification situation.

### 4.3 The local inertia is transitive

The underlying fiber of (2) has one point.  For a finite normal cover,
points in the normalized fiber correspond to local monodromy orbits.
Therefore the local inertia has one orbit on the three sheets.  In an
\(S_3\) cover it is either \(C_3\) or \(S_3\); if the nearby branch
components have transposition inertia, their generated transitive
subgroup is \(S_3\).

In the Euler formula this point contributes exactly
\[
o_q-2=1-2=-1.
\tag{12}
\]
The multiplicity-four fact (11) is invisible to that Euler count.

### 4.4 The singularity has minimal multiplicity, but need not be
eliminated formally

Let \(m_Y=(m_q,z,w)\).  Relations (4), together with (9), give
\[
m_Y^2=m_qm_Y.
\tag{13}
\]
Thus this two-dimensional Cohen--Macaulay singularity has
\[
\operatorname{embdim}=4,\qquad e=3.
\tag{14}
\]
Its tangent cone is a degree-three codimension-two curve cone.  If the
linear parts of \(a,b,c,d\) are sufficiently general, the tangent cone
is the reduced twisted-cubic cone and the singularity is rational.  If
the linear parts degenerate, (13) alone does not guarantee a reduced
tangent cone, so it is not legitimate to assert rationality in full
generality.

## 5. Exact normal non-Gorenstein \(S_3\) countermodel

Set the base ring to \(R=\mathbf C[x,y]\) and choose
\[
a=x,\qquad b=y,\qquad c=x+y,\qquad d=x+2y.
\tag{15}
\]
Then
\[
\begin{aligned}
A&=x^2-xy-2y^2,\\
B&=x^2+xy-y^2,\\
C&=3xy+4y^2.
\end{aligned}
\tag{16}
\]
Let
\[
Y_{\rm ng}=\operatorname{Spec}
R[z,w]/(F,G,H)
\tag{17}
\]
with (6).

The algebra is free of rank three over \(R\), with basis \(1,z,w\).
Over \(\mathbf C(x,y)\), eliminate \(w\) using \(b=y\ne0\).  The
resulting cubic for \(z\) is
\[
z^3+3(bd-a^2)z+
(3abd-2a^3-b^2c).
\tag{18}
\]
After setting \(t=x/y\) and \(Z=z/y\), it becomes
\[
p(Z)=Z^3+(-3t^2+3t+6)Z
-2t^3+3t^2+5t-1.
\tag{19}
\]
This polynomial has no root in \(\mathbf C(t)\).  Since it is monic,
any rational-function root is integral over \(\mathbf C[t]\), hence
lies in \(\mathbf C[t]\); degree comparison makes it
\(\alpha t+\beta\).  Equating coefficients gives
\[
\begin{aligned}
\alpha^3-3\alpha-2&=0,\\
3(\alpha^2-1)\beta+3\alpha+3&=0,\\
3\alpha\beta^2+6\alpha+3\beta+5&=0,\\
\beta^3+6\beta-1&=0.
\end{aligned}
\tag{20}
\]
For \(\alpha=2\), the second equation gives \(\beta=-1\), which fails
the third.  For \(\alpha=-1\), the last two equations have resultant
\(-208\).  Thus (19) is irreducible.  Hence (17) is a domain.

The grading
\[
\deg x=\deg y=\deg z=\deg w=1
\]
makes (17) the affine cone over an integral nondegenerate degree-three
curve in \(\mathbf P^3\).  Its Hilbert series is
\[
\frac{1+2t}{(1-t)^2}.
\tag{21}
\]
An integral nondegenerate degree-three curve in \(\mathbf P^3\) is a
twisted cubic.  Consequently \(Y_{\rm ng}\) is its normal affine cone,
with one singular point at the vertex.  Equivalently, it is the cyclic
quotient singularity
\[
\mathbf A^2/\tfrac13(1,1).
\tag{22}
\]
Its link is the lens space \(L(3,1)\), so
\[
H_1(\operatorname{Link};\mathbf Z)=\mathbf Z/3,
\qquad b_1(\operatorname{Link};\mathbf Q)=0.
\tag{23}
\]

At the origin all four coefficients (15) vanish, and the fiber is
\(\mathbf C[z,w]/(z,w)^2\).  Hence the vertex is non-Gorenstein.

The branch equation factors as
\[
\boxed{
D=(x^2-9xy-11y^2)(x^2-xy-3y^2).
}
\tag{24}
\]
Over \(\mathbf C\), this is a squarefree union of four distinct lines
through the origin.  The cubic field is irreducible, and (24) is not a
square, so the generic Galois group is \(S_3\).  Along each generic
branch point the inertia is a transposition.  At the origin the fiber
has one point, and the four transpositions generate the transitive
group \(S_3\).

Thus (17) simultaneously has:

- a normal integral total space;
- finite flat degree three over a smooth plane;
- \(S_3\) generic monodromy;
- squarefree, generically simple branching;
- one isolated non-Gorenstein point.

This is a direct counterexample to any proposed local exclusion using
only normality and cubic branch monodromy.

## 6. Hurwitz and the boundary lattice: what follows and what does not

Let \(R_1,\ldots,R_r\) be the irreducible boundary divisors of the
hypothetical completion \(Y\setminus S\).  The unit/class sequence gives
\[
0\longrightarrow
\bigoplus_{i=1}^r\mathbf Z[R_i]
\longrightarrow\operatorname{Cl}(Y)
\longrightarrow\mathbf Z/2
\longrightarrow0.
\tag{25}
\]
Hence no nonzero integral combination of boundary primes is
principal.

Since \(\pi\) is generically separable and the base has trivial
canonical divisor, the divisorial Hurwitz formula is
\[
K_Y\sim \operatorname{Diff}_{Y/\mathbf A^2}
=\sum_i \delta_i R_i,
\qquad \delta_i>0
\tag{26}
\]
over the ramified boundary primes.  At a tame simple branch
\(\delta_i=1\); at a tame totally ramified cubic prime
\(\delta_i=2\).

Equations (25)--(26) prove
\[
[K_Y]\ne0\quad\text{in }\operatorname{Cl}(Y),
\tag{27}
\]
provided there is ramification.  In other words, the canonical module
is not free and \(K_Y\) is not principal.

They do **not** prove that \(K_Y\) is not Cartier.  On a normal affine
scheme,
\[
Y\text{ Gorenstein}
\iff \omega_Y\text{ invertible}
\iff K_Y\text{ Cartier},
\]
not \(K_Y\sim0\).  A nontrivial Cartier divisor is a nonzero element of
\(\operatorname{Pic}(Y)\subset\operatorname{Cl}(Y)\).  The boundary
sequence has no mechanism forcing
\[
\operatorname{Pic}(Y)\cap
\bigoplus_i\mathbf Z[R_i]=0.
\]
Indeed, if \(Y\) were locally factorial, the entire free boundary
lattice in (25) would lie in \(\operatorname{Pic}(Y)\).

Therefore:

> Boundary independence plus Hurwitz excludes a *trivial* canonical
> module.  It does not exclude a Gorenstein total space.

Any Gorenstein contradiction would need an additional statement about
\(\operatorname{Pic}(Y)\), local Cartier indices at boundary
intersections, or a forced principal trivialization of \(\omega_Y\).

## 7. Interaction with the Euler and collision audits

The model (17) has branch equal to four lines through one point:
\[
c(\Delta)=4,\qquad \chi(\Delta)=1,\qquad N_{\rm tr}=1.
\]
It violates the pseudoplane rational-homology-manifold inequality
\[
c(\Delta)+\chi(\Delta)+N_{\rm tr}\le2,
\]
so it is not itself a global Darboux completion.  That does not yield
a local exclusion.

For example, an irreducible rational affine branch with normalization
\(\mathbf A^1\) and one ordinary quadruple point has
\[
c(\Delta)=1,\qquad
\chi(\Delta)=1-(4-1)=-2.
\]
If the quadruple point is transitive, then
\[
c(\Delta)+\chi(\Delta)+N_{\rm tr}
=1-2+1=0\le2.
\tag{28}
\]
This local monodromy is combinatorially possible: assign the four
ordered branch meridians
\[
(12),(12),(23),(23).
\]
Their product is the identity, as required after killing the central
total meridian, while they generate \(S_3\).

The smooth/rational-homology-manifold balance would require
\[
r=2-\chi(\Delta)-N_{\rm tr}=3,
\tag{29}
\]
which is compatible with one ramified and two additional boundary
components.  Thus even the stronger topology does not numerically
forbid a multiplicity-four transitive branch point.

A non-Gorenstein point lies over the branch divisor, not over the
generic unbranched collision curve \(\Gamma_D\).  It may occur at a
special intersection with that curve, but the generic \(1+2\) or
\(1+1+1\) collision classification does not control it.

The Hesse cone and (17) show that two independent local escape modes
exist:

\[
\begin{array}{c|c|c|c}
\text{model}&\text{fiber at vertex}&\text{Gorenstein?}&b_1(\text{link})\\ \hline
\text{Hesse cubic cone}&\mathbf C[t]/(t^3)&\text{yes}&2,\\
\text{twisted-cubic cone (17)}
&\mathbf C[z,w]/(z,w)^2&\text{no}&0.
\end{array}
\tag{30}
\]

Gorensteinness and the positive-\(b_1\) link correction are therefore
orthogonal.  Excluding one does not automatically exclude the other.

## 8. Best next target

The finite-flat reduction has converted the vague singularity question
into a concrete one:

\[
\text{Can }V(a,b,c,d)
\text{ occur compatibly with the distinguished boundary sheets?}
\]

The promising next checks are:

1. pull the four coefficient functions \(a,b,c,d\) to the divisorial
   valuations of the branch and collision curves and use the known
   class labels of the retained sheets;
2. compute the local conductor and class of the noncurvilinear fiber
   at an intersection with the closure of \(D\) or \(H\);
3. determine whether the Darboux symplectic form forces the relative
   dualizing module to be not merely invertible but **trivial**.  Only
   that stronger statement would combine with (27) to exclude the
   Gorenstein case.

No contradiction is obtained here.  The exact countermodel makes this
a no-go theorem for a broad local strategy, while (10)--(11) provide a
sharper algebraic target for the next incidence calculation.
