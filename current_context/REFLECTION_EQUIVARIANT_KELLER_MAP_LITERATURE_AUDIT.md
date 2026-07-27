# Reflection-equivariant Keller maps: literature and quotient audit

## Scope and conclusion

Let \(k=\mathbf C\), let
\[
\rho(x,y)=(-x,y),
\]
and consider a \(\rho\)-equivariant polynomial map
\[
H=(G,F)
  =\bigl(xQ(x^2,y),\,P(x^2,y)\bigr):\mathbf A^2\longrightarrow\mathbf A^2
\]
with nonzero constant Jacobian.

This class is already ruled out as a source of counterexamples.  The directly
applicable result is Moskowicz--Valqui,
[*The Starred Dixmier Conjecture for \(A_1\)*][MV-journal],
Proposition 4.1 (\(\alpha\)-\(JC_2\)), not Miyanishi's small-group theorem.
After a linear change of coordinates, Proposition 4.1 says precisely that a
Keller map commuting with \((X,Y)\mapsto(X,-Y)\) is a triangular
automorphism.

Consequently, if
\[
F=P(x^2,y),\qquad G=xQ(x^2,y),\qquad
J_{x,y}(F,G)=c\in k^\times,
\]
then there are \(\lambda\in k^\times\) and \(A\in k[s]\) such that
\[
G=\lambda x,\qquad
F=-\frac{c}{\lambda}y+A(x^2).
\]
Equivalently,
\[
Q(s,y)=\lambda,\qquad
P(s,y)=-\frac{c}{\lambda}y+A(s).
\]

In particular, the nodal boundary conditions
\[
P(s,0)=s,\qquad Q(s,0)=s-1
\]
cannot have a polynomial Keller thickening, in any bidegree.  This supersedes
all degree-by-degree exclusions inside that parity ansatz.

This is a prior-art closure of a route, not a new proof of the planar
Jacobian conjecture and not a new publishable theorem by itself.

## 1. Exact match with Moskowicz--Valqui

Moskowicz--Valqui use the exchange involution
\[
\alpha(X)=Y,\qquad \alpha(Y)=X.
\]
Their Proposition 4.1 proves that an \(\alpha\)-equivariant endomorphism
\(f:k[X,Y]\to k[X,Y]\) with scalar nonzero Jacobian is an automorphism.

The linear change
\[
U=\frac{X+Y}{2},\qquad V=Y-X
\]
conjugates \(\alpha\) to
\[
\beta(U)=U,\qquad \beta(V)=-V.
\]
Thus their proposition is exactly the statement:

> If \(R(U,V)\) is even in \(V\), \(S(U,V)\) is odd in \(V\), and
> \(J_{U,V}(R,S)\in k^\times\), then
> \[
> S=\lambda V,\qquad R=\mu U+a(V^2)
> \]
> for suitable \(\lambda,\mu\in k^\times\) and \(a\in k[t]\), with
> \(\lambda\mu=J_{U,V}(R,S)\).

For the parity ansatz take \(U=y\), \(V=x\), \(R=F\), and \(S=G\).
The coordinate transposition changes the sign of the Jacobian and gives the
normal form stated above.

Vered Moskowicz later states a more general intertwining result in
[*Involutions and the Jacobian Conjecture*][M-involutions], Theorem 2.3:
if \(f\gamma=\delta f\) for two involutions \(\gamma,\delta\) and \(f\) is
Keller, then \(f\) is invertible.  For the present problem this adds no new
input: its proof conjugates both involutions to the exchange involution and
invokes Moskowicz--Valqui Proposition 4.1.

## 2. Proof audit of Proposition 4.1

The proof is not the tempting but invalid one-line quotient argument.  It is a
two-sided Newton-polygon argument.

Write
\[
R(U,V)\in k[U,V^2],\qquad S(U,V)\in V k[U,V^2],
\qquad [R,S]=1
\]
after scaling one component.  Subtracting a constant from \(R\), if needed,
does not change any hypothesis.

1. Use the **lower** \(V\)-degree \(w_{0,1}\), not the usual upper degree.
   The lower-bracket inequality is
   \[
   w_{0,1}([R,S])
   \geq w_{0,1}(R)+w_{0,1}(S)-1.
   \]
   Since \(w_{0,1}(R)\geq0\), \(w_{0,1}(S)\geq1\), and
   \(w_{0,1}([R,S])=0\), equality holds and the lowest \(V\)-forms have the
   shape
   \[
   R_-=U/\lambda,\qquad S_-=\lambda V
   \]
   up to the harmless subtracted constant.

2. Sweep the lower Newton boundary from direction \((0,1)\) to
   \((-1,1)\).  At a hypothetical first nontrivial face, the weights of the
   two starting vertices \((1,0)\) and \((0,1)\) have opposite signs.
   Hence the two face polynomials cannot have zero Jacobian (zero Jacobian
   would make them powers of one common weighted-homogeneous polynomial).
   The endpoint formula for a nonzero face bracket then forces the endpoints
   to add to \((1,1)\).  The only nonaligned nonnegative pair is
   \((1,0),(0,1)\), making both faces monomials and contradicting that this was
   a Newton direction.  Thus no such lower face occurs.

3. Sweep the upper Newton boundary from \((1,-1)\) to \((1,0)\).
   The same opposite-sign argument excludes every nontrivial face before
   \((1,0)\).

4. Therefore
   \[
   \deg_U S=0,\qquad \deg_U R=1.
   \]
   Write \(S=s(V)\) and \(R=a(V)+U b(V)\).  Then
   \[
   1=[R,S]=b(V)s'(V),
   \]
   so \(s(V)=\lambda V\), \(b(V)=1/\lambda\); parity makes
   \(a(V)\in k[V^2]\).

I checked the three external Newton facts against the exact version cited by
Moskowicz--Valqui, Guccione--Guccione--Valqui
arXiv:1401.1784v1:

- Proposition 1.11 is the lower-degree bracket inequality and equality
  criterion used in step 1;
- Propositions 3.12 and 3.13 are the consecutive-direction endpoint rules
  used in the upper and lower sweeps;
- the leading-form dependence result used in the opposite-sign step is the
  standard weighted-homogeneous Jacobian-zero criterion developed earlier in
  the same paper.

The important sign check is that the proof uses \(w_{0,1}\), the **minimum**
weighted degree.  Its inequality points in the displayed direction.  Reading
that \(w\) as the usual maximum degree would incorrectly make the first step
look reversed.

I found no logical gap in the specialization to the explicit reflection
\(\beta(U,V)=(U,-V)\).  The broader assertion in Moskowicz's Theorem 2.3 that
every polynomial involution is conjugate to the exchange involution is not
needed here.

## 3. Why Miyanishi's theorem is not the applicable result

Miyanishi's published theorem assumes that \(G\subset\mathrm{GL}(2,\mathbf C)\)
is **small**, meaning that \(G\) has no pseudo-reflections.  The published
abstract and the theorem in the paper both have this hypothesis.
The group
\[
\langle\rho\rangle,\qquad \rho(x,y)=(-x,y),
\]
is generated by a pseudo-reflection, so it is not small.

The introduction says that for a not-necessarily-small finite group one may
quotient by the normal subgroup generated by pseudo-reflections and that an
equivariant étale endomorphism induces an étale endomorphism of the smooth
quotient.  In the present case the quotient calculation exposes the missing
condition.

Put
\[
\pi(x,y)=(s,y)=(x^2,y).
\]
For
\[
H(x,y)=\bigl(xQ(s,y),P(s,y)\bigr)
\]
the induced quotient map is
\[
\overline H(s,y)=\bigl(sQ(s,y)^2,P(s,y)\bigr).
\]
The chain rule gives the exact identity
\[
J_{s,y}(\overline H)=Q(s,y)\,J_{x,y}(H).
\]
Thus, if \(J(H)=c\), then
\[
J(\overline H)=cQ.
\]
The descended map is étale exactly when \(Q\) is a unit, hence a nonzero
constant.  But this is already the triangular case above.  Therefore the
pseudo-reflection quotient reduction does not provide an independent proof:
in this example, proving that the quotient is étale is equivalent to proving
the substantive conclusion.

More generally, for a quotient map \(\pi:V\to V/N\) and an equivariant map
\(H\), the Jacobian chain rule reads
\[
\bigl(J\overline H\circ\pi\bigr)J\pi
  =(J\pi\circ H)JH.
\]
The quotient is étale only if the relative-discriminant ratio
\[
\frac{J\pi\circ H}{J\pi}
\]
is a unit.  Equivariance gives divisibility, but by itself it does not exclude
extra inverse-image components of the reflection divisor.

Accordingly:

- Miyanishi's small-group theorem is not contradicted;
- its main proof does not cover the reflection action;
- the introductory pseudo-reflection reduction hides the hard assertion for
  this parity class;
- Moskowicz--Valqui supply that hard assertion by a separate Newton-polygon
  proof.

## 4. An exact affine-surface countermodel to automatic étale descent

The failure of the quotient inference as a general formal principle can be
seen without any open conjecture.

Let
\[
X=\mathbf G_m\times\mathbf A^1
  =\operatorname{Spec}\mathbf C[z,z^{-1},y],
\qquad
\iota(z,y)=(z^{-1},y).
\]
The fixed loci \(z=1\) and \(z=-1\) are divisors, so this is reflection-type
ramification.  The invariant ring is
\[
\mathbf C[z,z^{-1},y]^\iota
  =\mathbf C[t,y],\qquad t=z+z^{-1},
\]
and hence \(X/\iota\simeq\mathbf A^2\).

The endomorphism
\[
f(z,y)=(z^2,y)
\]
is finite étale and commutes with \(\iota\).  On the quotient it induces
\[
\overline f(t,y)=(t^2-2,y),
\]
whose Jacobian is \(2t\), so \(\overline f\) is ramified.

Geometrically, the free orbit \(\{i,-i\}\) maps to the fixed point \(z=-1\).
The stabilizer jump is exactly the phenomenon represented by the extra
factor \(Q\) in the affine-plane calculation.

## 5. Research consequence

The parity ansatz should be closed rather than extended to higher
\((\deg_y P,\deg_y Q)\).  In particular, the first previously unexcluded
\((4,5)\) case cannot yield a counterexample, even though its coefficient
recurrences and top-face arithmetic are internally consistent.

Any replacement route must break the global pseudo-reflection equivariance,
not merely increase the parity bidegree.

## Primary sources

1. V. Moskowicz and C. Valqui,
   [*The Starred Dixmier Conjecture for \(A_1\)*][MV-journal],
   Communications in Algebra **43** (2015), 3073--3082,
   DOI 10.1080/00927872.2014.907418; see Proposition 4.1.
   [arXiv:1401.5141][MV-arxiv].
2. J. A. Guccione, J. J. Guccione, and C. Valqui,
   [*On the Shape of Possible Counterexamples to the Jacobian
   Conjecture*][GGV],
   Journal of Algebra **471** (2017), 13--74,
   DOI 10.1016/j.jalgebra.2016.08.039.
   The proof audit above used the exact arXiv version cited in
   Moskowicz--Valqui, [arXiv:1401.1784v1][GGV-v1].
3. M. Miyanishi,
   [*Equivariant Jacobian Conjecture in Dimension Two*][Miyanishi-journal],
   Transformation Groups **28** (2023), 951--971,
   DOI 10.1007/s00031-022-09727-7.
   [arXiv:2110.06709][Miyanishi-arxiv].
4. V. Moskowicz,
   [*Involutions and the Jacobian Conjecture*][M-involutions],
   arXiv:1410.7705, especially Theorem 2.3.

[MV-journal]: https://doi.org/10.1080/00927872.2014.907418
[MV-arxiv]: https://arxiv.org/abs/1401.5141
[GGV]: https://doi.org/10.1016/j.jalgebra.2016.08.039
[GGV-v1]: https://arxiv.org/abs/1401.1784v1
[Miyanishi-journal]: https://doi.org/10.1007/s00031-022-09727-7
[Miyanishi-arxiv]: https://arxiv.org/abs/2110.06709
[M-involutions]: https://arxiv.org/abs/1410.7705
