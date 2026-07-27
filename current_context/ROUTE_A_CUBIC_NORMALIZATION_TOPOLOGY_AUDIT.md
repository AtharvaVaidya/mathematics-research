# Route A: topology of the hypothetical cubic normalization

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad
S=\operatorname {Spec}B,
\]
and suppose that an étale Darboux map
\[
F=(P,Q):S\longrightarrow\mathbf A^2
\]
has generic degree \(3\).  Let
\[
\pi:Y\longrightarrow\mathbf A^2
\]
be the finite normalization in
\(\operatorname {Frac}(B)/\mathbf C(P,Q)\), and identify \(S\) with its
open image in \(Y\).  Write
\[
R=Y\setminus S
\]
for the boundary and \(\Delta\subset\mathbf A^2\) for the reduced branch
curve.

This audit combines the known invariants
\[
\chi(S)=1,\qquad
\pi_1(S)=\mathbf Z/2,\qquad
B^\times=\mathbf C^\times,\qquad
\operatorname {Cl}(B)=\mathbf Z/2
\]
with cubic monodromy and the boundary divisor sequence.

The result is an exact balance theorem, but not a contradiction:

> **Cubic normalization balance.** Let \(\Sigma\) be a finite
> stratification set containing all singular points of \(\Delta\), and
> let \(o_p\) be the number of orbits of the local inertia group at
> \(p\) on the three sheets.  Then
> \[
> \boxed{
> \chi(Y)=3-\chi(\Delta)+
> \sum_{p\in\Sigma}(o_p-2)
> }
> \tag{1}
> \]
> and
> \[
> \boxed{
> \chi(R)=2-\chi(\Delta)+
> \sum_{p\in\Sigma}(o_p-2).
> }
> \tag{2}
> \]
> At a smooth simple branch point \(o_p=2\).  At a singular point whose
> local inertia is transitive, \(o_p=1\), contributing \(-1\) to (1).

If the boundary over \(\Delta\) consists of exactly one ramified point
over every point of the branch curve, put
\[
b=\chi(R)-\chi(\Delta)
\]
for the Euler contribution of all additional boundary, counted with
the necessary overlap corrections.  Then (2) becomes
\[
\boxed{
2\chi(\Delta)+N_{\mathrm{tr}}+b=2,
}
\tag{3}
\]
where \(N_{\mathrm{tr}}\) is the number of singular strata with
transitive local inertia.

All terms in (3) have genuine geometric freedom.  In particular,
unramified boundary curves can have negative Euler characteristic.
The equation has monodromy-compatible solutions, and the coefficient
two in a simple branch is aligned with, rather than opposed to, the
\(\mathbf Z/2\) class group and fundamental group of \(S\).

There is one strong conditional refinement.  If \(Y\) is smooth, then
Alexander--Lefschetz duality and affineness force
\[
H_c^1(R;\mathbf Q)=0.
\]
If \(R\) is a pure curve with \(r\) irreducible components, this gives
\[
\chi(R)=r
\]
and hence
\[
\boxed{r+\chi(\Delta)+N_{\mathrm{tr}}=2.}
\tag{4}
\]
In particular a negative-Euler correction is impossible on a smooth
normalization, or more generally on a rational-homology-manifold
normalization.  The compatibility models below must use singularities
of \(Y\) on the omitted boundary whose links have positive rational
first homology.

The live obstruction is therefore a boundary-singularity problem, not
bare numerical topology.  A further argument must control the actual
singularities, algebraic types, and intersections of the boundary
curves, or the monodromy at infinity, strongly enough to remove the free
correction \(b\).

## 1. Euler characteristic of the quadratic pseudoplane

The morphism
\[
u:S\longrightarrow\mathbf A^1
\]
has
\[
S_{u\ne0}\simeq\mathbf G_m\times\mathbf A^1_w
\]
and reduced special fiber
\[
S_{u=0,\mathrm{red}}=D\simeq\mathbf A^1_v.
\]
Additivity of compactly supported Euler characteristic gives
\[
\chi(S)
=\chi(\mathbf G_m)\chi(\mathbf A^1)+\chi(\mathbf A^1)
=0+1=1.
\tag{5}
\]
For complex algebraic varieties this is the same numerical Euler
characteristic used below.

The known topology of this pseudoplane is
\[
\pi_1(S)=\mathbf Z/2.
\]
In particular \(S\) is a rational homology plane:
\[
H_1(S;\mathbf Q)=0,\qquad \chi(S)=1.
\]

## 2. Euler characteristic of a finite cubic normalization

Over \(\mathbf A^2\setminus\Delta\), the finite map \(\pi\) has three
distinct points in every fiber.  Over the smooth locus of a simple
branch component, the inertia is a transposition and the set of sheets
has two orbits:
\[
\{1,2\},\qquad\{3\}.
\]
Thus the underlying fiber of \(Y\) has two points.

At \(p\in\Sigma\), let \(H_p\subset S_3\) be the local inertia group.
The number of points in the normalized fiber is
\[
o_p=\#\bigl(H_p\backslash\{1,2,3\}\bigr).
\tag{6}
\]
The possible nontrivial cases are
\[
\begin{array}{c|c|c}
H_p&\text{sheet orbits}&o_p\\ \hline
\langle(12)\rangle&\{1,2\},\{3\}&2,\\
\langle(123)\rangle&\{1,2,3\}&1,\\
S_3&\{1,2,3\}&1.
\end{array}
\tag{7}
\]

Stratified additivity now gives
\[
\begin{aligned}
\chi(Y)
&=3\chi(\mathbf A^2\setminus\Delta)
+2\chi(\Delta\setminus\Sigma)
+\sum_{p\in\Sigma}o_p\\
&=3(1-\chi(\Delta))
+2(\chi(\Delta)-|\Sigma|)
+\sum_{p\in\Sigma}o_p\\
&=3-\chi(\Delta)
+\sum_{p\in\Sigma}(o_p-2),
\end{aligned}
\]
which proves (1).

Since \(S\subset Y\) is open and \(R\) is closed,
\[
\chi(Y)=\chi(S)+\chi(R).
\]
Using (5) gives (2).

Equation (1) is insensitive to scheme-theoretic ramification
multiplicity: Euler characteristic counts points, not lengths.  The
multiplicity two reappears in divisor classes and local meridians below.

## 3. Boundary correction and the minimal-boundary equation

At the generic point of each branch component, the cubic divisor is
\[
\operatorname {div}_Y(f_i)=2E_i+C_i,
\tag{8}
\]
where the ramified prime \(E_i\) is omitted from \(S\) and the
unramified prime \(C_i\) is retained.

In the minimal situation, the ramified boundary has one underlying
point over every point of \(\Delta\), including the singular strata.
It then contributes
\[
\chi(R_{\mathrm{ram}})=\chi(\Delta).
\]
Let \(b\) denote the constructible Euler integral contributed by all
additional boundary primes, subtracting their intersections with the
ramified boundary.  Substituting
\[
\chi(R)=\chi(\Delta)+b
\]
into (2) gives
\[
2\chi(\Delta)
+\sum_{p\in\Sigma}(2-o_p)+b=2.
\]
By (7), the sum is \(N_{\mathrm{tr}}\), proving (3).

There is no sign restriction on \(b\).  A closed affine curve may have
negative Euler characteristic; for example
\[
\mathbf A^1\setminus\{0,1\}
\]
has Euler characteristic \(-1\) and occurs as the affine plane curve
\[
xy(y-1)=1.
\]
Thus an extra unramified boundary divisor can increase \(\chi(S)\) when
it is removed from \(Y\).

Two useful conditional consequences are:

1. If there is no additional boundary, then
   \[
   2\chi(\Delta)+N_{\mathrm{tr}}=2.
   \tag{9}
   \]
2. A cuspidal cubic branch has
   \(\chi(\Delta)=1\) and one transitive singular stratum, so minimal
   boundary would give \(\chi(S)=0\).  Achieving \(\chi(S)=1\) requires
   \(b=-1\), which is numerically possible.

The standard cubic map
\[
(s,t)\longmapsto(s,t^3-3st)
\]
exhibits the second calculation: \(Y=\mathbf A^2\) has Euler
characteristic \(1\), its cuspidal branch has one transitive singular
point, and its ramification parabola has Euler characteristic \(1\).
Deleting only that parabola gives Euler characteristic zero.

## 4. Exact local monodromy at branch and boundary

### Simple branch component

For a positively oriented transverse meridian \(\mu\) around a smooth
branch component, the cubic monodromy is a transposition, say
\[
\rho(\mu)=(12).
\]
The punctured transverse inverse image has:

1. one connected double orbit, locally \(z\mapsto z^2\), approaching
   the omitted ramification divisor \(E\);
2. one trivial orbit, approaching the retained unramified divisor \(C\).

Adding \(C\) to the open surface fills the meridian on the fixed sheet.
The double-orbit meridian remains around the omitted divisor and
projects to \(\mu^2\).  This is compatible with a global order-two
meridian in \(\pi_1(S)\); local topology alone only makes it infinite
cyclic before the global relations are imposed.

### Unbranched \(1+2\) collision over \(\Gamma_D\)

The transverse inertia is trivial:
\[
\rho(\mu_{\Gamma_D})=1.
\]
The degree decomposition is a residue-field, or longitudinal,
decomposition:
\[
1+2.
\]
The \(D\)-sheet is retained and the mandatory degree-two prime is also
retained.  Hence no boundary prime dominates \(\Gamma_D\), and the
generic fiber of \(F\) over this curve still has three points.

After deleting the finitely many branch or missing values of the
degree-two curve map, longitudinal monodromy may interchange its two
sheets.  This \(S_2\)-monodromy is independent of the trivial
transverse inertia.

### Unbranched \(1+1+1\) collision over \(\Gamma_D\)

Again the transverse inertia is trivial.  If all three primes are
retained, there is no boundary contribution.  If exactly two primes
are retained, the third degree-one prime is an unramified boundary
divisor \(R_D\), and the generic fiber of \(F\) over \(\Gamma_D\) has
two points.

If \(\Gamma_D\) is smooth, then
\(\Gamma_D\simeq\mathbf A^1\), and a finite birational degree-one
boundary prime over it is also \(\mathbf A^1\).  It contributes \(+1\)
to \(b\).  If \(\Gamma_D\) is singular with normalization
\(\mathbf A^1\), write
\[
a_p=\#\bigl(R_D^{-1}(p)\bigr).
\]
Away from the finite singular set the map is an isomorphism, and
\[
\chi(R_D)
=\chi(\Gamma_D)+\sum_p(a_p-1).
\tag{10}
\]
Thus conductor gluing changes the Euler term, but does not force its
sign.

## 5. Class group and units of the boundary

Assume for clarity that \(R\) has pure codimension one, with
irreducible components \(R_1,\dots,R_r\).  The localization sequence is
\[
B^\times/(A')^\times
\longrightarrow
\bigoplus_{j=1}^r\mathbf Z[R_j]
\longrightarrow
\operatorname {Cl}(Y)
\longrightarrow
\operatorname {Cl}(S)
\longrightarrow0.
\tag{11}
\]
Because
\[
(A')^\times\subset B^\times=\mathbf C^\times,
\]
the first term is zero.  Hence the boundary divisor classes inject:
\[
\boxed{
0\longrightarrow\mathbf Z^r
\longrightarrow\operatorname {Cl}(Y)
\longrightarrow\mathbf Z/2
\longrightarrow0.
}
\tag{12}
\]

This is restrictive but consistent.  Equation (8) gives
\[
[C_i]=-2[E_i]\quad\text{in }\operatorname {Cl}(Y),
\]
and after quotienting by boundary classes it gives
\[
[C_i\cap S]=0\quad\text{in }\operatorname {Cl}(S),
\]
exactly the cubic branch-section theorem.

At an unbranched \(1+1+1\) collision with one omitted prime,
\[
\operatorname {div}_Y(f)
=\overline D+\overline C+R_D
\]
gives, after restriction,
\[
[C]=[D]\quad\text{in }\operatorname {Cl}(S).
\]
Again the boundary term supplies precisely the missing lift in
\(\operatorname {Cl}(Y)\).

The relation
\[
\operatorname {div}_S(u)=2D
\]
has the same form: in \(Y\), possible boundary valuations of \(u\)
lift the relation, while the quotient (12) retains the order-two class.
Thus the coefficient two in ramification and the order-two class of
\(D\) are arithmetically compatible.

## 6. The smooth-normalization obstruction

Suppose first that \(Y\) is smooth and that \(R\) is a pure reduced
curve.  Both \(Y\) and \(S\) are affine complex surfaces, so
they have the homotopy type of CW complexes of real dimension at most
two.  Hence
\[
H_3(Y;\mathbf Q)=0.
\]
Moreover (5) and \(\pi_1(S)=\mathbf Z/2\) give
\[
H_2(S;\mathbf Q)=0:
\]
\(S\) has no rational \(H_1\), has no homology above degree two, and has
Euler characteristic one.

The long exact sequence of the pair \((Y,S)\) now contains
\[
0=H_3(Y;\mathbf Q)
\longrightarrow H_3(Y,S;\mathbf Q)
\longrightarrow H_2(S;\mathbf Q)=0.
\]
Thus
\[
H_3(Y,S;\mathbf Q)=0.
\]
Alexander--Lefschetz duality in the oriented real four-manifold \(Y\)
identifies
\[
H_3(Y,Y\setminus R;\mathbf Q)
\simeq H_c^1(R;\mathbf Q).
\]
Therefore
\[
\boxed{H_c^1(R;\mathbf Q)=0.}
\tag{13}
\]

An affine curve has no positive-dimensional proper connected
components, so \(H_c^0(R)=0\).  Its top compactly supported cohomology
has one generator for each irreducible component:
\[
\dim H_c^2(R;\mathbf Q)=r.
\]
Equation (13) gives
\[
\chi(R)=r.
\tag{14}
\]
Substitution in (2) proves (4):
\[
r+\chi(\Delta)+N_{\mathrm{tr}}=2.
\]

Every irreducible branch component has a ramified boundary component
above it.  If \(c(\Delta)\) is the number of irreducible components of
\(\Delta\), then \(r\ge c(\Delta)\), and a smooth normalization must
satisfy
\[
\boxed{
c(\Delta)+\chi(\Delta)+N_{\mathrm{tr}}\le2.
}
\tag{15}
\]

This is a genuine global obstruction.  For example a cuspidal branch
with \(\chi(\Delta)=1\) and one transitive singularity would force
\(r=0\), although ramification requires \(r\ge1\).  Hence such a cubic
normalization cannot be smooth if its Darboux open subset is \(S\).

The same proof works whenever \(Y\) is a rational homology
four-manifold: equivalently, every isolated surface-singularity link is
a rational homology three-sphere.  Rational Poincaré and
Alexander--Lefschetz duality then replace their manifold versions.
Thus (4) and (15) also hold for quotient singularities and, more generally,
for any boundary singularities with rational-homology-sphere links.

For a normal, possibly singular \(Y\), all singular points lie in
\(R\), because \(S\) is smooth.  The links of those isolated surface
singularities replace ordinary Alexander--Lefschetz duality by a local
correction.  Only links with positive rational first homology can evade
the argument and support \(H_c^1(R)\ne0\), hence a negative-Euler
boundary.  Classifying that local correction is the sharpened remaining
route.

## 7. A sharp cubic singularity countermodel

Positive-\(H_1\) links genuinely occur in non-Galois cubic
normalizations.  Consider the affine cone
\[
Y_{\mathrm H}
=V\!\left(z^3+3xyz+x^3+y^3\right)
\subset\mathbf A^3_{x,y,z}
\tag{16}
\]
and the finite projection
\[
\pi_{\mathrm H}:Y_{\mathrm H}\longrightarrow\mathbf A^2_{x,y}.
\]
The projective Hesse cubic
\[
z^3+3xyz+x^3+y^3=0
\subset\mathbf P^2
\]
is smooth.  Hence the affine cone is normal and has exactly one
singular point, its vertex.

As a cubic in \(z\), its discriminant is
\[
\Delta_{\mathrm H}
=-27\left(x^6+6x^3y^3+y^6\right).
\tag{17}
\]
This polynomial is squarefree and not a square.  The defining cubic is
irreducible, so the generic Galois closure has group \(S_3\), with
transposition inertia along the generic branch points.

The link of the vertex is the circle bundle of degree \(-3\) over the
smooth elliptic Hesse cubic.  Its rational first Betti number is
\[
b_1(\operatorname {Link}(0,Y_{\mathrm H}))=2.
\tag{18}
\]
Thus \(Y_{\mathrm H}\) is not a rational homology four-manifold, and its
vertex supplies exactly the kind of local correction that evades
(13)--(15).

The numerical Euler formula is also exact.  The branch polynomial (17)
is a union of six distinct complex lines through the origin, so
\[
\chi(\Delta_{\mathrm H})=6-5=1.
\]
The origin has transitive local monodromy, hence \(o_0=1\), and (1)
gives
\[
\chi(Y_{\mathrm H})=3-1+(1-2)=1.
\]
This agrees with the fact that an affine cone is contractible.

The Hesse cone is not the desired global \(Y\): its étale open
complement is not the quadratic pseudoplane, and it does not satisfy the
required boundary class data.  It is a sharp countermodel to any claim
that degree-three normalization singularities automatically have
rational-homology-sphere links.

## 8. Fundamental group balance

The local complement of a boundary divisor has an infinite cyclic
meridian.  Finiteness of
\[
\pi_1(S)=\mathbf Z/2
\]
is a global statement: intersections, divisors in \(Y\), and retained
curves impose relations among those meridians.

The homological model is the same as the class-group model (12).  In a
smooth setting, the Gysin sequence contains
\[
H_2(Y)\longrightarrow
\bigoplus_j\mathbf Z[\mu_j]
\longrightarrow H_1(S)
\longrightarrow H_1(Y).
\tag{19}
\]
A relation with coefficient two can turn a boundary meridian into an
element of order two.  The minimal CW model
\[
\langle\lambda\mid\lambda^2\rangle
\]
has
\[
\pi_1=\mathbf Z/2,\qquad \chi=1,
\]
exactly the numerical topology of \(S\).  The simple-branch local model
supplies the natural doubled meridian, while retained sheets supply
the filling relations.

Therefore neither the local transposition nor the presence of a
boundary meridian contradicts \(\pi_1(S)=\mathbf Z/2\).  To obtain a contradiction one
would need an independent proof that some meridian survives with
infinite order, or that the intersection map in (19) cannot have the
required index two.

## 9. A complete compatibility datum

The following stratified datum satisfies every formula above.  It is a
topological/constructible model, not a claimed algebraic Darboux map.

1. Take a connected cubic monodromy representation with group \(S_3\)
   and a cuspidal branch curve \(\Delta\) of Euler characteristic \(1\).
   The cusp has transitive local inertia, so \(N_{\mathrm{tr}}=1\).
2. Take the ramified boundary constructibly bijective to \(\Delta\), of
   Euler characteristic \(1\).
3. Add one unramified boundary curve of Euler characteristic \(-1\),
   dominating an unbranched \(1+1+1\) collision curve.  Retain the
   \(D\)-sheet and one nonprincipal class-mate.
4. Place the negative-Euler boundary through isolated singularities of
   \(Y\) whose links have positive rational \(H_1\), supplying the required
   \(H_c^1(R)\).  Give the boundary lattice a relation of index two, so its meridian
   quotient is \(\mathbf Z/2\), and take the divisor-class quotient in
   (12) to be \(\mathbf Z/2\).

The Euler equation is
\[
2\chi(\Delta)+N_{\mathrm{tr}}+b
=2\cdot1+1-1=2,
\]
so \(\chi(S)=1\).  The monodromy is transitive \(S_3\), the branch
inertia is a transposition generically, the collision inertia is
trivial, and the fundamental-group presentation has order two.

This datum shows exactly why the audited invariants do not contradict
one another.  Its unramified boundary curve can be modeled by a rational
affine curve with normalization \(\mathbf A^1\) and two identifications,
which has Euler characteristic \(-1\).

The missing step is algebraic realization inside a finite normal
surface \(Y\), with suitable isolated boundary singularities and with
the Darboux open set isomorphic to the specific quadratic pseudoplane.
The topology and divisor arithmetic do not forbid such a realization,
but (15) proves that a smooth \(Y\) cannot realize this particular
datum.

## 10. Next rigorous target

The free variable in the global audit is
\[
b=\chi(R)-\chi(\Delta).
\]
A promising exclusion would prove one of:

1. every isolated singularity of a cubic normalization has too small a
   link correction to support the required negative \(b\);
2. every negative-Euler unramified boundary component forces an
   infinite-order meridian in \(H_1(S)\);
3. the intersection map in (19) cannot have cokernel
   \(\mathbf Z/2\) when all branch divisors have the \(2+1\) form; or
4. monodromy at infinity forces an additional transitive stratum
   without a compensating negative-Euler boundary.

Without such a singular-boundary theorem, Euler characteristic, local
monodromy, \(\pi_1\), units, and the class group remain mutually
compatible.  If \(Y\) is smooth, (15) is already a substantive
restriction.

## Scope of verification

The companion verifier checks (1)--(4), the orbit table (7), the
collision sheet counts, the class-lattice quotient, and the numerical
compatibility datum.  It does not replace the theorem-level facts
\(\pi_1(S)=\mathbf Z/2\), the localization sequence for class groups,
Alexander--Lefschetz duality, or the existence of the finite
normalization.
