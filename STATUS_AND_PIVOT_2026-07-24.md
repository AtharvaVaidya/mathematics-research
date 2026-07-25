# Status, publication audit, and strategic pivot

Date: updated 25 July 2026

## Executive assessment

The plane Jacobian conjecture has **not** been resolved in this workspace.
There is no complex counterexample and no proof of \(JC(2)\).

The strongest result is a candidate computational theorem eliminating both
GGHV coefficient systems for the remaining degree pair \((72,108)\).
Subject to an independent audit of the translation from the published
reduction and of the specialization argument, it would raise the lower bound
for the maximum coordinate degree of a plane Keller counterexample from
\(108\) to \(125\).

A priority search on 24 July found two nearly simultaneous external
developments.  A 23 July Zenodo preprint reports machine evidence at the same
\((72,108)\) frontier but explicitly says that its simultaneous
all-coefficient certificate is still missing.  A MathOverflow answer posted
the same day announces an independent complete computer-assisted
elimination, with its write-up still in preparation.  Our bounded
elimination may therefore be an independent co-discovery rather than a
priority claim.  The exact systems and certificates must be compared before
any novelty statement.

The most important correction from the literature audit is that the outer
Belyi/Davenport--Zannier family is classical.  Zannier's 1995 paper already
contains the relevant family, Catalan recursion, and the five \(k=3\)
possibilities.  The plausible novelty in the bounded result is therefore the
complete elimination of every **lower** coefficient fiber, not the outer
passport or its count.

## Results with the best publication prospects

### 1. Elimination of the \((72,108)\) systems

The exact computation has the following structure.

1. The outer equation is the classical degree-21 DZ/Belyi problem with
   passport
   \[
   (2^{10},1),\qquad(3^7),\qquad(17,1^4).
   \]
   It has five normalized geometric points.
2. Modulo \(32003\), the normalized outer algebra is reduced of length five:
   two rational points and one irreducible cubic factor.
3. For the full a/b system, the lower weighted projective fiber is empty over
   all five geometric outer points.
4. For the full case-c system, all 165 lower coefficients reduce to seven
   weighted parameters.  Exact Gröbner certificates over the same five outer
   points show that the lower fiber is supported only at the affine origin,
   so its weighted projectivization is empty.
5. Prime-to-\(p\) tame specialization of the outer covers and properness of
   the original weighted projectivization transport the special-fiber
   obstruction to characteristic zero.

The broad verifier suite passes.  The publication-critical Singular check
`route_bd_fbar_obstruction.py --run-singular` also passes over the two
rational factors and the cubic field factor.

This is the best candidate for a focused paper, but it is not ready for a
claim of record until:

- a second person matches every implemented support and localization to the
  GGHV alternatives;
- the tame-specialization and weighted-Proj argument is written
  scheme-theoretically and independently checked;
- the certificate bundle is reproduced on a clean machine with archived
  software versions, hashes, and Gröbner bases;
- the authors of the reduction are asked whether the system has already been
  eliminated or whether a normalization caveat is missing.
- the certificates are compared with the independent 23 July 2026
  announcements, with priority and overlap stated explicitly.

### 2. Uniform seven-mode deformation theorem

For every radial scale \(k\ge1\), the complete bounded linear kernel has
weights
\[
(1,1,2,2,3,3,4).
\]
It is parametrized by one scalar potential
\[
C=\frac{2UB-3VA}{E}
\]
with an explicit inverse formula.  The seven modes are Hamiltonian for
\[
\Omega=\frac{z^4}{w^3}\,dz\wedge dw
\]
and carry an explicit graded Lie bracket.

This is a clean structural theorem and a plausible companion result.  It
does not resolve the nonlinear support problem.  The endpoint square
patterns beyond the checked scales remain conjectural and should not be
advertised as an all-\(k\) theorem.

There is now a second all-\(k\) structural theorem.  Put \(r=k+1\).
For the full bounded radial supports, the common leading root is
\[
R=w^{r-1}(uw+vz),\qquad uv\ne0.
\]
The exact identity
\(\{P,Q^2-LP^3\}=2Qz^4/w^3\) implies that the top total degree of
\(Q^2-LP^3\) is among
\[
5r,4r,3r,2r\quad\text{or is at most }r+3.
\]
Thus its radial cusp-contact deficit is at least \(r=k+1\).  This concerns
the radial boundary at infinity; it does not by itself constrain the
separate affine case-c curve \(F(x=0)\).

### 3. Fixed-pinch-plane structural package

The fixed-plane route gives an explicit nonnormal pinch ring, an exact
Darboux reduction, broad all-degree no-go families, and a global conductor
image with \(\mathbf G_m\)-normalization.  A new residual-oddness theorem
shows that if \(F(U,V)=DH\) is the pullback of its image equation, then
\[
H|_C(-v)=-H|_C(v).
\]
Consequently an extra affine component over the conductor image is
compulsory.  In the smooth-image case one irreducible residual component
meets both marked cusp arms with positive odd multiplicity, with exponent
\(m\equiv-1\pmod{2\delta}\).  Combining the \(\mathbf G_m\)-normalization
with Chau's theorem that every irreducible nonproper component is
polynomially parametrized proves simultaneously:
\[
e^{-1}(\Gamma)\supsetneq C,
\qquad
\text{and a different dicritical component }\Lambda\ne\Gamma.
\]
This independently audited theorem is a potentially publishable global
incidence result, not a resolution of the fixed-ring Darboux equation or of
all plane Keller maps.

### 4. Homogeneous-centralizer and osculating-cubic package

For every radial \((2,3)\) scale \(k\), put \(r=k+1\).  A single
chain-rule identity and the homogeneous centralizer of
\[
R=w^{r-1}(uw+vz)
\]
give two all-\(k\) statements:
\[
\deg_{\rm tot}(Q^2-LP^3)
\in\{5r,4r,3r,2r\}\quad\text{or}\quad\le r+3,
\]
and, more strongly, constants \(c_5,c_4,c_3,c_2\) for which
\[
\deg_{\rm tot}\!
\left(Q^2-LP^3+c_5PQ+c_4P^2+c_3Q+c_2P\right)\le r+3.
\]
The corresponding target curve is generically a smooth Weierstrass
elliptic cubic with one flex at infinity.  In the full a/b branch its
pullback to the boundary has degree at most seven.

This is a clean, non-computational structural theorem and is plausibly
publishable with the seven-mode deformation theorem.  Its novelty has not
yet been checked exhaustively against the approximate-root and polynomial
Hall/Davenport literature, and it is not a contradiction by itself.

Completing the square and depressing this universal cubic gives a further
all-scale consequence.  For every polynomial boundary restriction of
degrees \((2r,3r)\), there are monic coordinates \(X,T\) with
\[
D=T^2-X^3,\qquad \deg D\le\max(2r,r+3).
\]
The exact identity
\[
T(2XT'-3X'T)=XD'-3X'D
\]
therefore gives
\[
\deg(2XT'-3X'T)\le\max(2,r-1),
\]
and in particular at most \(r-1\) for \(r\ge3\).  This low-degree
Wronskian is the numerator of
\(d\log(T^2/X^3)\), so it packages the finite ramification budget into
one explicit polynomial.  It cannot vanish for a primitive boundary
pair, and a marked point of coordinate order \(m\) contributes at least
\(m-1\) to its vanishing.  Hence every primitive marked pair satisfies
\(m\le r\).  At \(r=4\) this kills the order-five and order-seven cells
conceptually and is the source of the exact remaining \((3,5)\)
obstruction.

It now has a sharp intrinsic consequence for the full a/b boundary.  A
linear restriction to the normalization would give a polynomial embedding,
which the Abhyankar--Moh--Suzuki degree theorem excludes.  If the boundary
parametrization degree were \(\delta=4\), the restriction would be constant,
so the boundary would be a singular cubic fiber.  The cusp is excluded by
the earlier odd-valuation square.  Nodal normalization and the reduced
Jacobian leave only a degree-four power passport, but its fourth transverse
Taylor coefficient contains the uncancellable term
\[
\frac{\lambda^2}{2c}w^{-2},\qquad \lambda c\ne0.
\]
Therefore
\[
\boxed{\delta\ne4.}
\]
The degree-two parametrization case is also excluded.  A fixed-pole lemma
shows that the normalization branch must be nonimmersive at the marked
point \(w=0\).  The exact generalized degree-\((4,6)\) Davenport
classification leaves a unique degree-three family, but its normalization
is immersive everywhere because
\[
\operatorname{Res}(A',B')=-1728a^5\ne0.
\]
Hence \(\delta\ne2\).  The only surviving a/b boundary is birationally
parametrized (\(\delta=1\)), its osculating restriction has degree
\(2,\ldots,7\), and \(w=0\) is a marked nonimmersive point.

### 5. Normalization-genus and SAGBI rigidity

The osculating cubic now gives a scalable curve-theoretic sieve.  For a
primitive degree-\((2r,3r)\) boundary with osculating remainder
\(G=\mathcal H(A,B)\) of degree \(d\le r+3\), regular coordinates
\((u,f)\) at the unique infinity branch have orders
\[
\operatorname{ord}u=r,\qquad \operatorname{ord}f=9r-d.
\]
The plane-branch semigroup formula and the genus formula therefore give
\[
\sum_{p\in C\cap\mathbf A^2}\delta_p
\le
\left\lfloor\frac{(d+1)r-d+1}{2}\right\rfloor .
\]
For the full a/b system the leading ODE forces \(r=4,d=7\).  Hence the
infinity branch has Puiseux pair \((4,29)\), contributes exactly \(42\)
delta units, and leaves exactly \(13\) affine delta units.  The degree
semigroup has precisely the thirteen gaps already present in
\(\langle7,8,12\rangle\), so
\[
\operatorname{Deg}\mathbf C[A,B]=\langle7,8,12\rangle
\]
and \(G,A,B\) form a SAGBI basis at infinity.

This immediately eliminates the \((5,8),(7,11)\), and \((4,14)\)
marked cells.  A separate shear-correct exact calculation eliminates
\((3,10)\).  The last \((3,5)\) cell is now also excluded in
characteristic zero.  Retaining the degree-twelve approximate root
\(T\), the Wronskian identity
\[
T(2AT'-3A'T)=AD'-3A'D
\]
turns the global remainder bound into a triangular degree-three
Wronskian system.  Its exact rational radical forces
\[
a_5=0,\qquad a_7^2=4a_6,\qquad a_4a_7=2,
\]
and hence the required order-five coefficient vanishes.  Thus all five
primitive \(\delta=1\) cells are empty.

The genus/SAGBI statement is a strong candidate for the structural paper.
Its ingredients are classical, so novelty attaches only to their
application to the reduced-Jacobian osculating cubic and still requires a
focused literature comparison.

## Adversarial corrections

Several attractive arguments were rejected rather than promoted.

1. **The outer DZ family is not new.**  Its special role inside the GGHV
   system and the lower-fiber obstruction may be new.
2. **Trivial deck group does not imply field descent.**  Exact cyclic
   Kummer countermodels have a normalized identity germ and no nontrivial
   deck transformations but still have nontrivial monodromy.
3. **Rationality of a time-one map does not rationalize its graded
   Hamiltonian factors.**  The earlier cube/square/root factor tests are
   conditional unless an exact rational factorization is supplied.
4. **The full case-c line \(x=0\) is not contracted.**  It maps by
   polynomials of degrees \((8,12)\).  Only the central outer model
   contracts it.
5. **The fixed-cusp complement is not automatically available.**  A full
   completion can have additional asymptotic curves, its degree is not
   fixed by the outer mixed volume, and a passport does not determine a
   labeled monodromy representation.
6. **The identity branches do not separate components.**  An exact
   pullback countermodel using the actual rational function \(R\) joins all
   finite identity branches to the high-ramification infinity sheet on one
   irreducible component.
7. **A suspected case-c chart gap was real in the enlarged partial
   system but not in the full-vertex stratum.**  The earlier \(r_2\)
   presentation divided by \(r_4\) without stating why it is a unit.
   The required \(p_6\) endpoint gives
   \([h^8]p_6=r_4^2/4\ne0\), so \(r_4\ne0\) globally.  The
   denominator-free endpoint identity
   \[
   256r_4E_{14}-512E_{13}
   =2688r_4\left(p_{5,7}-\frac{r_4s_3}{2}\right)^2
   \]
   supplies the disputed \(q_{10}\) formula on both the \(r_2\)- and
   \(r_3\)-leading charts.  Thus the middle descent is exhaustive and
   the fractional mode \(c_{10}\) vanishes universally.  If the endpoint
   is deleted, \(r_4=0\) really does leave \(q_{10}\) free.  Subsequent
   unused endpoint rows and a paired-square cascade now also eliminate
   \(c_9,c_7,c_6,c_5\) on the tail charts, so every fractional mode is
   gone globally.
8. **The GGHV curve transfers, but its truncated toric tree does not.**
   Proposition 4.3 ends with the Laurent involution
   \(x\mapsto x^{-1},y\mapsto x^4y\), not a finite Kummer cover.
   Explicit reversed arcs show that the nonconstant case-c and a/b limit
   curves are genuine components of the original nonproper-value set, and
   their function-field degrees transfer birationally.  However, the
   determinant labels of the convenient reduced toric fan do not determine
   the cofactors of the complete original boundary matrix; omitted
   edge-cutting and target-infinity arms must first be restored.
9. **A tempting leading-ODE contradiction has a resonance loophole.**
   The leading coefficient of the osculating composition satisfies an
   exact first-order ODE.  Ignoring its resonant top \(y\)-degree falsely
   forces too many roots.  For \(r=2\) and every \(r\ge4\), the unique
   supported solution is
   \[
   k=y^{2r}(uy+v)^2H_r(uy/v),
   \]
   with \(H_r\) a genuine quartic and \(\deg_y k=2r+6\).  Only the
   exceptional scale \(r=3\) is obstructed at this layer.  This prevents
   promoting a false all-degree elimination.
10. **Osculating contact and primitivity do not eliminate the last a/b
    branch.**  Exact primitive degree-\((8,12)\) marked pairs exist over an
    explicit number field for which a smooth generalized Weierstrass cubic
    has pullback degree seven and \(A'(0)=B'(0)=0\).  Their marked branch is
    an ordinary tangent \((2,3)\) cusp.  What excludes this entire tangent
    chart is not Davenport contact but the original five-block pole
    asymmetry \(p_2=w^{-1}+O(1)\), \(q_2\in\mathbf C[w]\).  Thus any
    argument that shears the tangent away without tracking the pole has
    discarded essential information.
11. **The remaining a/b local problem is finite, but not empty.**  An
    exhaustive pole-sensitive Puiseux audit eliminates every nonzero-tangent
    and vertical chart.  Exactly five horizontal cells survive:
    \[
    (3,5),\ (5,8),\ (7,11),\quad (m,N)=(3,10),(4,14).
    \]
    The first three have exact local five-block countermodels; the last two
    have primitive global degree-\((8,12)\) boundary models.  Any further
    obstruction must use the global osculating remainder or the remaining
    five-block equations.  After imposing that global remainder with the
    linear shear retained, all five cells are now excluded.  The final
    \((3,5)\) contradiction comes from the exact Wronskian/radical
    calculation rather than a dense coefficientwise CRT lift.
12. **The first case-c Euler residue is classical, and \(c_8\) is invisible
    to all such residues.**  The degree-cap cokernel first appears at grade
    \(n=9\), where its scalar is exactly the \(h^{11}\) coefficient of the
    outer Bezout/DZ equation.  It is neither automatic nor a contradiction.
    The support-cost contribution of \(c_8\) is Euler-exact in every grade.
    Thus neither low-grade integration nor a cokernel attack on \(c_8\) is a
    viable route.

The corrected single-signature lemma remains valid: over \(x\ne0\), the only
uncancelled comparison ramification has
\[
(e,\nu Z,\nu W)=(5k+2,k,-1).
\]
If it is absent, purity and the split radial valuation force rational
descent.  What failed was the proposed easy proof that it is absent.

## New conceptual progress: the fixed cusp is the wrong branch

The Rees degeneration isolates the exact condition needed for étaleness over
the fixed cusp complement:
\[
Q(0,y)^2=L\,P(0,y)^3.
\]
Full vertices and the Jacobian equation would then force
\[
P(0,y)=Ay^8,\qquad Q(0,y)=By^{12}.
\]

This cusp-compatible stratum is now excluded without a large elimination.

- In case c, the coefficients of \(x\) and \(x^2\) in
  \(Q^2-LP^3\) force \(y^2\mid[x]P\), contradicting the required
  \((1,0)\) vertex.
- In the five-block a/b system, the \(z^4\) coefficient forces
  \[
  a_1^2=4Aw^7(1+wa_2),
  \]
  impossible because its right side has odd \(w\)-adic order seven.

Therefore any hypothetical full completion must have a genuinely
**non-cuspidal** critical/asymptotic curve.  This rules out the fixed-cusp
covering strategy as the main route rather than leaving it as a vague gap.

For the a/b asymptotic curve
\[
\Gamma=\overline{\{(a_0(w),b_0(w))\}},
\]
the normalization degree satisfies
\[
\delta=[\mathbf C(w):\mathbf C(a_0,b_0)]=1,
\]
and the generic transverse inertia contributed by the boundary is
a single 5-cycle.

For the full case-c polygons, exact normal-fan analysis leaves only two
finite asymptotic clusters:
\[
\begin{array}{c|c}
\text{cluster}&\text{initial multiplicities}\\ \hline
y=s&(2,3),\\
xy=t&(8,12).
\end{array}
\]
The outer third direction is excluded by \(\gcd(U,V)=1\).

Resolving the two clusters gives finite dicritical maps
\[
c\mapsto(c^2,c^3),\qquad c\mapsto(c^8,c^{12}),
\]
with positive augmented-canonical labels \(1\) and \(3\).  These local
arms are compatible with the required signs and give no discrepancy
contradiction.  The exact GGHV transfer audit further shows why their
provisional toric determinant labels cannot be used globally without the
omitted target-infinity descendants.  See
`current_context/CASE_C_CLUSTER_RESOLUTION_AUDIT.md` and
`current_context/GGHV_TRANSFER_CHAIN_AUDIT.md`.

## Chosen direction

A deliberately different counterexample route was tested through a
**cubic pseudo-plane selected by the exact three-dimensional
counterexample**.  On every fiber of its
third coordinate, the first two coordinates give a Darboux pair on
\(\mathbf G_m\times\mathbf A^1\) with Jacobian \(2/x^4\).  Polynomially
filling the puncture produces a double critical divisor, explaining exactly
why the three-dimensional collision does not immediately descend.

The exponent \(x^{-4}\) uniquely matches
\[
B_3=\mathbf C[u,v,w]/(w^3-u-u^2v)
\]
with
\[
\{u,w\}=-u^2,\qquad
\{u,v\}=-3w^2,\qquad
\{v,w\}=1+2uv.
\]
There is an explicit polynomial map \(\pi_3:\mathbf A^2\to B_3\) with
built-in cubic collisions and
\[
J(F\circ\pi_3,G\circ\pi_3)=-9\{F,G\}.
\]
Thus a regular pair \(F,G\in B_3\) with \(\{F,G\}=1\) would be an immediate
plane Keller counterexample.  The restricted three-dimensional pair already
has constant bracket \(-2/3\) on a cubic Kummer cover, but its two
coordinates have nontrivial deck characters and do not descend.  The proof
target is now the exact regular-descent/Darboux problem on \(B_3\), not a
blind polynomial-map search.  See
`current_context/THREE_DIMENSIONAL_CUBIC_PSEUDOPLANE_BRIDGE.md`.

The three easiest seeds have already been disposed of structurally.  The
Hamiltonian \(v\) has no rational slice because its generic fiber carries
the nonexact elliptic differential \(dw/\sqrt{1+4vw^3}\).  The Hamiltonian
\(w\) has a rational slice, but its two incompatible pole cancellations on
the reducible fiber \(w=0\) prevent a regular slice.  Finally,
\((v,w)\) is a Darboux pair modulo \(2\), but the coefficient functional
\([uv]\) annihilates every possible first correction, so it cannot lift even
modulo \(4\).  These are all-degree obstructions; the next search must deform
the boundary Hamiltonian itself.  See
`current_context/CUBIC_PSEUDOPLANE_FIRST_OBSTRUCTIONS.md`.

The first deformations out of \(v\) are now closed as well:
\[
P=v+f(w)\quad(f\in\mathbf C[w]),\qquad
P=v+wA(v)\quad(A\in\mathbf C[v])
\]
have no rational slice.  In both cases the generic fiber is a double cover
carrying an explicit nonzero holomorphic differential that a slice would
make exact.

Two prior-art corrections sharply narrow the novelty claim.  The surface
\(B_3\) is the classical pseudo-plane \(S(3,3,1)\).  Dubouloz--Palka
(Adv. Math. 339 (2018)) construct arbitrarily large families of nonproper
étale endomorphisms on every \(u(1+u^{\bar r}v)=w^k\), and Miyanishi
(J. Algebra 294 (2005)) proves that affine planes pseudo-cover all
pseudo-planes with a unique multiple fiber.  Thus neither the surface,
its nonproper dynamics, nor the existence type
\(\mathbf A^2\to B_3\) is new.

There is nevertheless an exact new lifting test for the particular
\(\pi_3\) selected by the three-dimensional fiber.  Writing
\[
h=1+3a^3b,\qquad t=1-h^3,
\]
a lift of \(\eta:B_3\to B_3\) requires a cube root \(A\) of
\(\pi_3^*\eta^*u\) and
\[
\frac{\pi_3^*\eta^*w}{A}\equiv1\pmod{A^3}.
\]
Every nonproper \(\mathbf C^*\)-equivariant Dubouloz--Palka map fails this:
the \(\alpha=0\) Shabat branch would require
\[
t(1-t)R_2^3\mid R_1-1,
\]
whose left and right degrees are \(3N+2\) and at most \(2N+1\);
the \(\alpha=1\) branch demands one linear expression in \(h\) vanish on
three distinct cube-root components.  Their standard \(\Theta^P\)
deformations only add a multiple of \(A^3\), so they cannot repair the
congruence.  See
`current_context/CUBIC_PSEUDOPLANE_ETALE_LIFT_AUDIT.md`.

This closes the known pseudo-plane endomorphism architecture rather than
opening a shortcut to a counterexample.  The route is therefore demoted.
The primary direction is now the normalization-genus/SAGBI analysis of the
actual boundary, followed only where necessary by sparse exact
certificates.  It is not a larger coefficient elimination and not an
attempt to reconstruct the entire completion tree prematurely.

The two sharply reduced proof targets have now both advanced.

1. In a/b, the exact Wronskian/radical obstruction eliminates the last
   \((3,5)\) cell.  Together with the earlier \(\delta=2,4\) exclusions,
   the complete a/b boundary alternative at this scale is empty.
2. In case c, the two generic triangular charts are empty at deficit
   seven over every factor of the complete five-point outer fiber.  The
   other two charts were already empty or supported only at the affine
   cone origin by deficits six and eight.  Thus the complete modular
   weighted-projective case-c fiber is empty; the characteristic-zero
   consequence uses the audited good-reduction and properness argument.

The next all-degree direction is not to enumerate the first degree pair
above \(125\).  It is to combine the depressed-Wronskian divisor
\[
\operatorname{div}d\log(T^2/X^3)
\]
with the all-degree dicritical node formula and the \(\Delta=0\) boundary
subtree.  The Wronskian has degree at most \(r-1\), so all finite
ramification and every marked nonimmersion must fit into one small
effective divisor.  The concrete target is a classification of its
possible allocations among boundary nodes and affine collisions.  This
is the scalable continuation of the successful \(r=4\) proof.

The decorated-boundary-tree route remains a useful independent check, but
it is secondary until the omitted edge-cutting and target-infinity arms can
be reconstructed from the original map.  The reduced toric fan alone does
not carry enough global information for an intersection-matrix
contradiction.

In parallel, the actual degree-\((8,12)\) boundary pair
\[
D(y)=q(y)^2-Lp(y)^3\ne0
\]
should be studied as a nonhomogeneous DZ/approximate-root object.  The goal is
to extract a small invariant of \(D\), not to eliminate all its coefficients.
The first such invariant is exact.  The endpoint descent and the
required-\(r_4\) square cascade now give
\[
c_{11}=c_{10}=c_9=c_7=c_6=c_5=0.
\]
Therefore in case c,
\[
\deg D\in\{20,16\}\quad\text{or}\quad\deg D\le15,
\]
so the boundary curve has cusp contact at infinity \(4\), \(8\), or at
least \(9\).  The only surviving approximate-root modes are the integral
terms \(c_8P,c_4H\).  The repaired chart audit and square cascade are in
`current_context/CASE_C_Q10_CHART_AUDIT.md` and
`current_context/CASE_C_UNIVERSAL_FRACTIONAL_DESCENT.md`.

For a/b, the remaining four blocks can now be incorporated without
coefficient elimination.  The identity
\[
\{P,Q^2-LP^3\}=2Q\{P,Q\}
\]
and the homogeneous centralizer of the common leading quartic imply
\[
\deg\bigl(b_0^2-La_0^3\bigr)
\in\{20,16,12,8\}\quad\text{or}\quad\le7.
\]
Thus the actual a/b boundary has cusp contact at infinity in
\(\{4,8,12,16\}\) or at least \(17\).  In particular the degree-23,
degree-22, and degree-21 terms all vanish.  The first tangent block by
itself still admits degree 23, so this improvement genuinely uses the
full five-block equation.  The proof and exact kernel check are in
`current_context/AB_BOUNDARY_CONTACT_SPECTRUM.md` and
`route_bd_ab_contact_spectrum.py`.

There is a stronger moving-target formulation.  For every \(r=k+1\ge2\),
the four possible high radial centralizer terms can be absorbed
successively into a generalized Weierstrass polynomial
\[
\mathcal H(X,Y)
=Y^2-LX^3+c_5XY+c_4X^2+c_3Y+c_2X+c_0
\]
so that
\[
\deg_{\rm tot}\mathcal H(P,Q)\le r+3.
\]
The exact identity
\[
\{P,\mathcal H(P,Q)\}
=(2Q+c_5P+c_3)\{P,Q\}
\]
is what makes the descending \(R^5,R^4,R^3,R^2\) cancellation stable.
For a/b (\(r=4\)), the restricted polynomial has degree at most seven,
or weighted pullback contact at least \(17\).  The target is generically
a smooth elliptic cubic with one smooth flex place at infinity, not a
cusp.  Intrinsic curve contact must be divided by the boundary
parametrization degree \(\delta\); before the later exclusions, the three
abstract lower bounds were \(17,9,5\).  The proof, an exact curve-level
counterexample to forgetting this division, and the verifier are in
`current_context/UNIVERSAL_OSCULATING_CUBIC.md` and
`route_bd_universal_osculating_cubic.py`.

The degree-four singular-fiber alternative and the degree-two
multisection alternative are now both excluded.  Thus \(\delta=1\):
the boundary is primitive, the moving cubic restricts with degree
\(2,\ldots,7\), and the fixed pole forces a marked nonimmersive point at
\(w=0\).  In the first nonintegral Puiseux chart, local valuation balance
leaves only types
\[
(3,5),\qquad(5,8),\qquad(7,11).
\]
Exact reduced-Jacobian countermodels realize all three local types, so the
next obstruction must use the global degree-\((8,12)\) Davenport data or
the outer endpoints, not only the first four transverse jets.

Computation will be used only after this geometry reduces the alternatives
to a finite list, and then only for exact certificates or countermodels.

## Verification status

The complete pre-existing exact verifier suite passes.  The following new or
corrected checks also pass independently:

- `route_bd_radial_cusp_complement_audit.py`;
- `route_bd_rees_cusp_degeneration_audit.py`;
- `route_bd_asymptotic_curve_invariant.py`;
- `route_bd_case_c_cusp_pde_obstruction.py`;
- `route_bd_case_c_toric_dicritical_reduction.py`;
- `route_bd_universal_osculating_cubic.py`;
- `route_bd_universal_depressed_wronskian.py`;
- `route_bd_osculating_leading_ode.py`;
- `route_bd_ab_osculating_delta4.py`;
- `route_bd_ab_delta4_nodal_obstruction.py`;
- `route_bd_ab_delta2_multisection_obstruction.py`;
- `route_bd_ab_delta1_cusp_jets.py`;
- `route_bd_ab_delta1_global_marked.py`;
- `route_bd_ab_delta1_tangent_cusp_obstruction.py`;
- `route_bd_ab_delta1_puiseux_chart_table.py`;
- `route_bd_ab_delta1_five_cell_global.py`;
- `route_bd_ab_delta1_35_wronskian.py`;
- `route_bd_ab_osculating_genus_budget.py`;
- `route_bd_case_c_universal_fractional_resonances.py`;
- `route_bd_case_c_integral_normal_form.py`;
- `route_bd_case_c_integral_cokernel.py`;
- `route_bd_case_c_n3_hurwitz_bridge.py`;
- `route_bd_case_c_n3_generic_charts.py`;
- `route_3d_cubic_pseudoplane_bridge.py`;
- `route_3d_cubic_pseudoplane_obstructions.py`;
- `route_3d_cubic_pseudoplane_etale_lift.py`;
- `route_bd_noncusp_difference_invariant.py`;
- `route_bd_ab_contact_spectrum.py`;
- `route_bd_gghv_transfer_chain_audit.py`;
- `route_bd_universal_contact_spectrum.py`;
- `route_bd_radial_rational_descent_criterion.py`;
- the full Singular algebraic-closure check
  `route_bd_fbar_obstruction.py --run-singular`.

Passing code is not peer review.  It verifies the algebra encoded in the
scripts; it does not by itself certify that every localization used by a
script covers the chart named in its prose.  The repaired \(r_4\)
presentation is a concrete example of why that audit matters.  Nor does
the suite by itself certify the imported reduction, the global
specialization argument, or novelty.

## Primary literature used in the audit

- U. Zannier, *On Davenport's bound for the degree of \(f^3-g^2\) and
  Riemann's Existence Theorem*, Acta Arith. 71 (1995), 107--137:
  <https://matwbn.icm.edu.pl/ksiazki/aa/aa71/aa7122.pdf>.
- N. V. Chau, *Two remarks on non-zero constant Jacobian polynomial maps
  of \(\mathbf C^2\)*, Ann. Polon. Math. 82 (2003), 39--44:
  <https://doi.org/10.4064/ap82-1-4>.
- J. A. Guccione, J. J. Guccione, E. Horruitiner, and C. Valqui,
  the degree-\((72,108)\) reduction used as the bounded input:
  <https://arxiv.org/abs/2204.14178>.
- F. Santibañez-Leal, *A planar program for the two-variable Jacobian
  conjecture: a theorem ladder, staircase transport, and machine
  certificates at the \((72,108)\) frontier*, version 0.07, deposited
  23 July 2026:
  <https://doi.org/10.5281/zenodo.21503368>.
- The explicit three-dimensional Keller map used for the cubic
  pseudo-plane bridge has an independent formal verification in the
  Archive of Formal Proofs:
  <https://isa-afp.org/entries/Jacobian_Counterexample.html>.

## 25 July adversarial pivot

The proposed Wronskian/divisor extrapolation above is now superseded.
The Wronskian theorem is correct, but it has no unused ramification
surplus.  At \(r=5\) there is an exact simple point modulo \(32003\)
which Hensel-lifts to a primitive characteristic-zero boundary pair with
\[
(\deg X,\deg T,\deg D,\deg W)=(10,15,10,4)
\]
and a marked \((3,5)\) cusp.  Its Wronskian is
\[
W\doteq h^2(h-\alpha)(h-\beta),
\]
so the marked cusp consumes two units and two free critical points
consume the remainder.  Repeating the scale-four Wronskian elimination
at larger scales is therefore not a viable strategy.

The original five-block fourth Taylor row supplies the missing invariant.
For
\[
\begin{aligned}
J&=A'B''-B'A'',\\
K&=A'J'-3A''J,\\
L&=A'K'-5A''K,
\end{aligned}
\qquad
\Phi=3K^2-JL,
\]
every genuine five-block solution satisfies
\[
\boxed{\Phi\in\mathbf C[h]^2.}
\]
If \(D=B^2-A^3\ne0\) has degree \(d\le2r\), then exactly
\[
\deg\Phi=d+8r-10,
\]
so \(d\) must be even.  Degree parity alone is insufficient, but the
full even-divisor condition rejects the \(r=5\) Wronskian countermodel.
The next proof target is to combine
\[
\operatorname{div}\Phi=2E
\]
with the special rational root
\[
C=\frac{h\,p_1^2}{U},
\qquad
UV+2hUV'-3hU'V=1.
\]
This keeps the successful low-degree ramification package while restoring
the fixed-pole and outer-endpoint information that the Wronskian forgot.

The counterexample-first pseudoplane route also acquired three exact
all-degree restrictions.  For
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v)
\]
one has \(\operatorname{Cl}(B)=\mathbf Z/2\), every Darboux map has
function-field degree at least two, and the image of
\(D=(u,w)\) must have a second source divisor above it.  A homogeneous
weight-\(-1\) Pfaff potential is impossible, while a Laurent countermodel
shows that homogenization cannot be forced formally.  The natural
two-component collision
\[
\operatorname{div}(w)=D+H,\qquad H=(1+uv,w),
\]
is itself impossible as the complete pullback of the collision curve:
rectification would force a polynomial solution of \(\{w,R\}=1\), but
every rational solution contains the pole \(-u^{-1}\).  Thus a surviving
construction needs at least a third divisor above that curve.

New exact artifacts:

- `route_bd_universal_wronskian_countermodel.py`;
- `route_bd_fiveblock_discriminant_square.py`;
- `route_a/pfaff_global_structure.py`;
- `route_a/verify_pfaff_homogeneous_obstruction.py`;
- `route_a/verify_dh_collision_architecture.py`.

## 25 July addendum: the full consecutive five-block class is empty

The completed-square root-consumption lemma is stronger than the first
marked-cusp statement suggested.  It eliminates not only the
pole-sensitive nonintegral family
\[
2n=3m+1,
\]
but also the sole analytic-quadratic Puiseux chart left by the exhaustive
fixed-pole analysis.

In that chart \(p_1(0)\ne0\) and
\(\operatorname{ord}_0 A'=m-1\ge2\).  Every finite zero of \(p_1\) is
therefore nonmarked and consumes at least its multiplicity in the divisor
of \(A'\).  If the high deficit-one mode is present, those zeros already
have total multiplicity \(2R-1=\deg A'\); if only the low mode is present,
they have total multiplicity \(2R-2\).  The additional marked zero makes
both degree ledgers impossible.

The normalization audit introduces no primitivity loophole.  If the
boundary map factors through a polynomial multisection of ramification
degree \(e\), all Puiseux orders are multiplied by \(e\) while the
prescribed transverse pole remains simple.  The nonintegral relation
forces \(e=1\); the analytic-quadratic relation permits at most \(e=2\)
and is still killed by the same root budget.  Consequently
\[
\boxed{\text{every genuine consecutive \((2,3)\) five-block completion
is impossible, at every scale}.}
\]

This result has passed an independent adversarial proof audit and the
updated exact symbolic checks.  It is a substantial all-scale theorem for
the a/b-type consecutive class, but it does not eliminate case c or prove
the plane Jacobian conjecture.
