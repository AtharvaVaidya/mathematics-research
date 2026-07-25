# The algebraic symplectic bridge and its monodromy obstruction

Date: 24 July 2026

## 1. The exact branch construction

Let \(S\) be a normal irreducible surface with rational symplectic form
\(\Omega\).  Let
\[
F_0=(P_0,Q_0),\qquad F=(P,Q)
\]
be generically finite rational maps to \(\mathbf A^2\) such that
\[
dP_0\wedge dQ_0=\Omega=dP\wedge dQ.
\tag{1}
\]
Suppose \(F_0\) has geometric degree \(N\); in the original radial branch
of interest \(N=21\).

Form the correspondence
\[
\mathcal X_F
=S\times_{F,\mathbf A^2,F_0}S.
\tag{2}
\]
Over the locus where \(F_0\) is étale, projection to the first factor is
a finite étale cover of degree \(N\).  A chosen formal inverse branch at
the normalized point at infinity selects a geometric point of its generic
fiber and therefore a finite separable field extension
\[
K(S)\subset M
\]
together with algebraic functions \(Z,W\in M\) satisfying
\[
P_0(Z,W)=P,\qquad Q_0(Z,W)=Q.
\tag{3}
\]
They define an algebraic correspondence
\[
T=(Z,W),\qquad F=F_0\circ T.
\tag{4}
\]
Differentiating (3) gives
\[
T^*\Omega=\Omega.
\tag{5}
\]
Thus the formal Hamiltonian construction always produces an algebraic
symplectic branch after passing to the function field of a component of
(2).

The exact missing bridge has two logically independent parts:

1. **Trivial monodromy:** \(M=K(S)\), or equivalently the selected
   component of (2) is birational over the first copy of \(S\).
2. **No interior poles:** once \(Z,W\in K(S)\), every divisorial valuation
   away from the allowed compactification boundary is nonnegative.

Only after both statements does \(T\) extend to a regular automorphism of
the fixed compactified log surface, where the volume-divisor theorem from
`RADIAL_PARAHORIC_GEOMETRY.md` reduces it to the normalized identity.

Normality does not prove the first statement.  A normal ring is integrally
closed in its own fraction field, not in an algebraic extension of that
field.  A formal section at one completed valuation likewise selects a
decomposition-group orbit; it need not be fixed by global monodromy.

## 2. Degree-21 integral symplectic countermodel

The obstruction already occurs in a two-dimensional exact model.  Work
over a characteristic-zero field containing the \(21\)-st roots of unity,
and put
\[
A=k[x^{\pm1},y].
\]
On the second copy with coordinates \(X,Y\), define
\[
F_0(X,Y)
=\left(X^{21},\frac{Y}{21X^{20}}\right).
\tag{6}
\]
Its Jacobian is one.  For \(a\ne0\), define the bounded regular pair on
\(\operatorname {Spec}A\)
\[
F(x,y)
=\left(x^{21}+a,\frac{y}{21x^{20}}\right).
\tag{7}
\]
It also has Jacobian one and has the same leading outer data as (6).

Let \(\phi\) satisfy
\[
\phi^{21}=x^{21}+a
\tag{8}
\]
and choose at \(x=\infty\) the normalized formal branch
\[
\phi=x\left(1+\frac{a}{x^{21}}\right)^{1/21}
=x+\frac{a}{21}x^{-20}+O(x^{-41}).
\tag{9}
\]
Put
\[
T(x,y)
=\left(
\phi,\frac{y\phi^{20}}{x^{20}}
\right).
\tag{10}
\]
Since
\[
\phi'=\frac{x^{20}}{\phi^{20}},
\]
the Jacobian of (10) is one.  Moreover,
\[
F_0\circ T
=\left(
\phi^{21},
\frac{y\phi^{20}/x^{20}}{21\phi^{20}}
\right)
=F.
\tag{11}
\]

This countermodel has all of the tempting bridge properties:

- \(F_0\) and \(F\) are regular on the same Laurent surface and have
  constant Jacobian;
- the selected branch is formally the identity at infinity;
- \(\phi\) is integral over \(A\);
- the second coordinate in (10) belongs to the finite integral algebra
  \(A[\phi]\), so the algebraic branch has no pole on its normalization;
- the branch is exactly symplectic.

Nevertheless \(T\) is not rational over \(A\).  At every simple root of
\(x^{21}+a\), its valuation is one, so (8) is Eisenstein at that
divisorial valuation.  Hence
\[
[k(x,\phi):k(x)]=21.
\]
The branch has nontrivial cyclic Kummer monodromy.  Integrality,
regularity on the normalization, exact symplecticity, and one normalized
formal branch do not descend it to the base.

The same construction works for every \(N>1\):
\[
F_0=\left(X^N,\frac{Y}{NX^{N-1}}\right),\quad
F=\left(x^N+a,\frac{y}{Nx^{N-1}}\right),\quad
T=\left(\phi,\frac{y\phi^{N-1}}{x^{N-1}}\right),
\quad\phi^N=x^N+a.
\tag{12}
\]

The additive constant is not essential.  Even after fixing both additive
constants, a nonlinear symplectic target shear gives the same obstruction.
Put
\[
q=\frac{y}{21x^{20}},\qquad
F(x,y)=\left(x^{21}+q^2,\ q\right).
\tag{13}
\]
Then \(F=(A\circ F_0)(x,y)\) for the target shear
\[
A(P,Q)=(P+Q^2,Q),
\]
so \(F\) is regular on \(A\), has Jacobian one, and has the same leading
outer term as \(F_0\).  If
\[
\phi^{21}=x^{21}+q^2,\qquad
T=\left(\phi,21\phi^{20}q\right),
\tag{14}
\]
then again \(F_0\circ T=F\) and \(T\) is symplectic.  The normalized
branch is much closer to the identity:
\[
\frac{\phi}{x}
=\left(1+\frac{y^2}{21^2x^{61}}\right)^{1/21}
=1+\frac{y^2}{21^3}x^{-61}+O(x^{-122}).
\tag{15}
\]
Both coordinates of \(T\) lie in the integral algebra \(A[\phi]\).
Nevertheless the divisor
\[
y^2+21^2x^{61}=0
\]
is irreducible in \(k[x^{\pm1},y]\) and occurs with valuation one in
\(x^{21}+q^2\).  The Kummer equation in (14) is therefore Eisenstein at
that divisor and still has degree \(21\).

Thus fixing additive constants does not repair the bridge.  One must
either quotient the comparison by all polynomial symplectic target
automorphisms—including nonlinear shears—or prove monodromy triviality in
the fixed target chart.  The latter is exactly what a direct
\(F_0^{-1}\circ F\) compactification argument requires.

For the actual radial Newton support, however, the nonlinear-shear
mechanism is excluded by a small weighted-degree lemma.  Give target
variables weights
\[
\operatorname {wt}P=2,\qquad\operatorname {wt}Q=3.
\]
Writing \(P_0=z^2F(w)\), \(Q_0=z^3G(w)\), a weighted-homogeneous target
polynomial \(H\) satisfies
\[
H(P_0,Q_0)=z^{\operatorname {wt}H}H(F,G).
\]
There is no nonzero weighted-homogeneous relation \(H(F,G)=0\).  Indeed,
after factoring one monomial, such a relation would be a polynomial
relation with constant coefficients in
\[
\frac{G^2}{F^3}=R(w),
\]
but the outer Belyi function \(R\) is nonconstant.

Consequently a target polynomial automorphism
\[
A=(A_1,A_2)
\]
whose composition with \(F_0\) retains radial \(z\)-degree caps \(2,3\)
must satisfy
\[
A_1=\alpha P+\alpha_0,\qquad
A_2=\beta Q+\gamma P+\beta_0,
\qquad \alpha\beta\ne0.
\tag{16}
\]
The fixed outer and additive normalizations reduce (16) to the identity.
Thus exact Newton support removes both explicit target-shear
countermodels.  It still does not prove the required monodromy theorem:
an arbitrary component of (2) need not arise from a target automorphism.

## 3. Minimal viable bridge theorem

The compactified automorphism strategy therefore needs a theorem of the
following form.

> **Radial monodromy-and-divisor bridge.**
> Let \((P,Q)\) be a bounded pair with the fixed outer branch and constant
> bracket.  In the normalized degree-\(21\) component of the correspondence
> (2):
>
> 1. the global monodromy fixes the chosen formal inverse branch, so its
>    component has degree one over the source;
> 2. the resulting rational symplectomorphism has no interior pole divisor.

The second conclusion is now proved, conditional only on the first.
For an interior divisor, boundedness of \(P_0(Z,W),Q_0(Z,W)\) and the
symplectic differential inequality leave only valuation pairs
\((\nu Z,\nu W)=(0,0)\) or \((1,2)\).  Thus there are no interior poles.
The exceptional zero type forces \(W/Z^2=w/z^2\); symplecticity then gives
\[
Z=zh,\quad W=wh^2,\quad
(z\partial_z+2w\partial_w+1)h=1.
\]
Its first nonconstant Laurent term is incompatible with the universal
seven-mode kernel theorem, so \(h=1\).  The full proof is in
`RADIAL_RATIONAL_DESCENT_CRITERION.md`.

The Kummer model (6)--(11) still disproves “integral formal branch implies
degree one.”  The rational maps \(T_g\) in
`RADIAL_PARAHORIC_GEOMETRY.md` show why boundedness of the two pulled-back
coordinates is essential: two-end identity jets alone do not exclude
interior poles.

The sole remaining bridge is therefore the permutation/monodromy
representation of the selected degree-\(21\) branch.  A promising non-Gröbner
formulation is to show that the bounded support supplies a global section
of the finite étale correspondence (2), or equivalently an idempotent in
its generic algebra selecting the normalized branch.  The countermodel
shows that Hensel idempotents in one completion do not suffice; they must
be shown invariant under global monodromy.

The identities and degree-\(21\) countermodel are checked in
`route_bd_symplectic_bridge_countermodel.py`.
