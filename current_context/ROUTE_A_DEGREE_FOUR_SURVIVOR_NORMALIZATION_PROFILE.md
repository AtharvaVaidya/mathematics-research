# Route A: normalization profiles of the two degree-four survivors

Date: 25 July 2026

## Outcome

Assume the hypotheses and conclusions of
`ROUTE_A_DEGREE_FOUR_RETAINED_SHEET_AUDIT.md`.  Thus
\[
S=S(2,2,1)\subset Y,\qquad
\pi:Y\longrightarrow\mathbf A^2
\]
is the finite normalization of a hypothetical degree-four étale map,
the reduced branch curve \(\Delta\) is irreducible with normalization
\[
\nu:\widetilde\Delta\simeq\mathbf A^1\longrightarrow\Delta,
\]
and the generic inertia is a transposition.  Write \(E\) for the
ramified boundary prime and
\[
D_{\rm res}=\pi^*\Delta-2E.
\]
Normalize the reduced pullback of \(D_{\rm res}\) to
\(\widetilde\Delta\); denote the resulting finite flat double cover by
\[
\rho:Z\longrightarrow\widetilde\Delta\simeq\mathbf A^1.
\tag{1}
\]

The two survivors have substantially different, but completely
determined, normalization profiles.

> **Residual-parity theorem.**
>
> 1. In the \(r=1,\delta=1\) survivor, let \(n\ge1\) be the number of
>    two-branch values of \(\Delta\).  At such a value \(q\), let
>    \(m_q\) be the local intersection multiplicity of its two
>    analytic branches, and put
>    \[
>    e=\#\{q:m_q\text{ is odd}\}.
>    \tag{2}
>    \]
>    The cover (1) is ramified at both normalization points over \(q\)
>    exactly when \(m_q\) is odd.  It is unramified over the unique
>    \(3+1\) value and over every nondeficient unibranch value.
>    Consequently:
>    \[
>    \begin{cases}
>    Z\simeq\mathbf A^1\amalg\mathbf A^1,&e=0,\\[1mm]
>    Z\text{ is connected, and its smooth projective completion has
>    genus }e-1,&e>0.
>    \end{cases}
>    \tag{3}
>    \]
>    In the connected case the completion has two points over
>    infinity.  The retained curve
>    \[
>    C=F^{-1}(\Delta)\subset S
>    \]
>    is obtained from \(Z\) by deleting exactly
>    \[
>    1+4n-2e
>    \tag{4}
>    \]
>    normalization points.  In all cases
>    \[
>    \boxed{\chi(C)=1-4n.}
>    \tag{5}
>    \]
>    If \(e>0\), then \(C\) is irreducible and principal.
>
> 2. In the no-two-branch \(r=2,\delta=0\) survivor, suppose the extra
>    boundary component \(E'\) has image
>    \(\Gamma\ne\Delta\) and punctures both residual sections.  Then
>    \[
>    Z=Z_1\amalg Z_2,\qquad Z_i\simeq\mathbf A^1.
>    \tag{6}
>    \]
>    Let \(\widetilde E'\to E'\) be the normalization and put
>    \[
>    K_i=\{p\in\widetilde E':
>    \text{the image of }p\text{ lies on the image of }Z_i\},
>    \qquad k_i=\#K_i,
>    \tag{7}
>    \]
>    counted by distinct normalization points rather than
>    intersection multiplicity.  Then \(k_i\ge1\), the two sets \(K_i\)
>    are disjoint, and the normalization of the retained component
>    \(C_i\subset S\) is
>    \[
>    \mathbf A^1\setminus\{k_i\text{ points}\}.
>    \tag{8}
>    \]
>    Hence
>    \[
>    \boxed{\chi(C_1\amalg C_2)=2-k_1-k_2.}
>    \tag{9}
>    \]
>    Moreover
>    \[
>    [C_1]=[C_2]\quad\text{in}\quad
>    \operatorname {Cl}(S)\simeq\mathbf Z/2.
>    \tag{10}
>    \]
>
> 3. Every \(r=2,\delta=0\) survivor is automatically Gorenstein:
>    \[
>    \omega_Y\simeq\mathcal O_Y(E).
>    \tag{11}
>    \]
>    In particular \(E\) is Cartier.  Under the no-two-branch
>    hypotheses of item 2, \(Y\) is additionally smooth along \(E'\)
>    and along both residual closures.  In the \(r=1,\delta=1\)
>    survivor, either \(Y\) is Gorenstein with the same
>    \(\omega_Y\)- and Cartier-\(E\) conclusions, or the length-three
>    local factor at the \(3+1\) point is noncurvilinear.  That sole
>    non-Gorenstein alternative forces the branch multiplicity at the
>    \(3+1\) value to be at least four.

These statements do not exclude either survivor.  They show exactly
why three tempting shortcuts fail:

* a two-branch value does not automatically ramify the normalized
  residual cover—its intersection parity matters;
* the \(3+1\) collision is not a branch point of (1), despite one
  residual closure meeting \(E\); and
* puncturing both split sections is compatible with both possible
  common classes in \(\operatorname {Cl}(S)\).

The corresponding complement homology is equally rigid.  Put
\[
U=S\setminus F^{-1}(\Delta).
\tag{12}
\]
If the residual curve in the first survivor is connected, then
\[
H_1(U;\mathbf Z)\simeq\mathbf Z\oplus\mathbf Z/2.
\tag{13}
\]
If it has two components, or in the second survivor, then
\[
H_1(U;\mathbf Z)\simeq
\begin{cases}
\mathbf Z^2\oplus\mathbf Z/2,&[C_1]=[C_2]=0,\\
\mathbf Z^2,&[C_1]=[C_2]\ne0.
\end{cases}
\tag{14}
\]
Thus a successful monodromy exclusion must rule out the appropriate
group in (13) or (14), not merely observe that
\(\pi_1(S)=\mathbf Z/2\).

## 1. The residual double cover

At a smooth point of \(\Delta\), label the generic transposition
\[
a=(12).
\]
The two fixed sheets \(3,4\) form the degree-two residual cover.  The
construction (1) is intrinsic: normality removes embedded
zero-dimensional structure, and torsion-freeness over
\(\mathbf C[t]\) makes the resulting rank-two module finite flat.

At the deficient unibranch value, local monodromy contains a second
transposition
\[
b=(23).
\]
The group \(\langle a,b\rangle\) has orbits \(3+1\).  One residual
closure reaches the length-three boundary point, while the other
reaches the remaining length-one point.  After normalizing the
residual pullback, these are still two distinct points over the one
normalization parameter.  Therefore \(\rho\) is unramified there.
The same support argument applies at a nondeficient unibranch value:
the two residual normalization points remain distinct.

Now let \(q\) be a two-branch value.  Its local meridians act as
disjoint transpositions, which after relabeling are
\[
a=(12),\qquad c=(34).
\tag{15}
\]
Choose the normalization branch whose generic meridian is \(a\).
The residual sheets are \(3,4\).  Going once around its parameter
near \(q\) links the other target branch \(m_q\) times, so the
residual monodromy is
\[
c^{m_q}.
\tag{16}
\]
It is nontrivial exactly when \(m_q\) is odd.  The same calculation on
the other normalization branch gives \(a^{m_q}\).  Thus every odd
two-branch value supplies two simple branch points of \(\rho\), and
every even value supplies none.

This is also visible in the normalized local equation.  Up to a unit,
the residual quadratic base change has the form
\[
z^2=t^{m_q}.
\tag{17}
\]
For odd \(m_q\), its normalization is ramified of index two.  For even
\(m_q\), its reduced normalization has two unramified branches.  The
unnormalized fiber in \(Y\) has one support point in either case, so
fiber support alone cannot distinguish the alternatives.

## 2. Riemann--Hurwitz and the deleted points

The finite branch divisor of \(\rho\) has degree \(2e\).  If \(e=0\),
then (1) is finite étale over \(\mathbf A^1\), hence splits.  If
\(e>0\), its monodromy is nontrivial, so it is connected.  Removing
square factors from (16) writes its function field as
\[
\mathbf C(t)\bigl(\sqrt{h(t)}\bigr),
\qquad h\text{ squarefree},\quad\deg h=2e.
\tag{18}
\]
The smooth projective double cover of \(\mathbf P^1\) is therefore
unramified at infinity, has two points above infinity, and
Riemann--Hurwitz gives
\[
2g-2=-4+2e,\qquad g=e-1.
\tag{19}
\]

The points deleted in passing from \(Z\) to the retained curve in
\(S\) are:

1. one residual normalization point at the unique \(3+1\) collision;
2. two points for every odd two-branch value, one over each
   normalization branch; and
3. four points for every even two-branch value, two over each
   normalization branch.

This gives (4):
\[
1+2e+4(n-e)=1+4n-2e.
\]
For \(e>0\), equations (17)--(18) give
\[
\chi(Z)=2-2e.
\]
For \(e=0\), the two affine lines also have total Euler
characteristic \(2\).  Subtracting the deleted points proves (5) in
both cases.

The accepted quartic collapse already proves \(n\ge1\): without a
two-branch value, one of the two residual sections avoids the sole
boundary component and becomes a homology line.  The parity theorem
does not strengthen this to \(e\ge1\).  Even tangential
self-intersections remain a genuine escape.

## 3. The extra unramified boundary curve

Assume now \(r=2,\delta=0\) and that \(\Delta\) has no two-branch
value.  The residual-cover lemma gives (6).  Let
\(\overline C_i\subset Y\) be the images of the two normalized
sections.

Every point of \(E'\) above \(\Delta\) lies on one of the
\(\overline C_i\).  It cannot lie on \(E\), because distinct boundary
components are disjoint.  Conversely, every point at which \(E'\)
punctures \(\overline C_i\) maps to \(\Gamma\cap\Delta\).  The
\(\delta=0\) support pattern is \(2+1+1\), so the two residual points
in a fiber are distinct.  A single point of \(E'\) therefore cannot
puncture both sections.  This proves the disjointness in (7).

The local fiber length at every residual point is one.  The standard
differential/Nakayama criterion consequently says that \(\pi\) is
étale at such a point.  Thus the local intersection multiplicity of
\(E'\) and \(\overline C_i\) is exactly the intersection multiplicity
of the corresponding normalization branch of \(\Gamma\) with
\(\Delta\).  Multiplicity does not affect the number of punctures:
each distinct normalization point removes one point from \(Z_i\).
This proves (8)--(9).

Finally, if \(f=0\) is a reduced equation of \(\Delta\), étaleness of
\(F\) makes its pullback reduced on \(S\), and
\[
\operatorname {div}_S f(P,Q)=C_1+C_2.
\tag{20}
\]
Therefore \([C_1]+[C_2]=0\).  Since
\(\operatorname {Cl}(S)\simeq\mathbf Z/2\), equation (10) follows.
Nothing in (20) distinguishes the two possibilities in (14).

## 4. The Gorenstein dichotomy

In an \(r=2,\delta=0\) survivor, a fiber over \(\Delta\) has support
\(2+1+1\) away from the two-branch values and support \(2+2\) at a
two-branch value.  Thus every local factor has length at most two.
Every Artinian local algebra of length at most two over
\(\mathbf C\) is Gorenstein.  Outside \(\Delta\) the map is étale, so
all fibers there are Gorenstein as well.

A finite flat morphism is Gorenstein exactly when all its fibers are
Gorenstein.  Hence \(Y\) is Gorenstein in the second survivor.  The
divisorial different is supported on the unique ramified prime \(E\),
with coefficient one at its generic simple-ramification point.
Therefore
\[
\omega_Y\simeq\mathcal O_Y(E),
\tag{21}
\]
which proves (11).  Since the left side is invertible, \(E\) is
Cartier.

Under the no-two-branch hypotheses of item 2, every point of \(E'\)
and every point of either residual closure is a length-one factor of
its target fiber.  After henselization that factor is finite flat of
rank one, hence isomorphic to the base.  Thus \(\pi\) is étale there
and \(Y\) is smooth along all three curves.  In particular \(E'\) and
the residual closures are Cartier divisors in this subcase as well.
This is a real restriction, but it is compatible with the boundary
localization sequence: it places the free boundary lattice inside
\(\operatorname {Pic}(Y)\), not at zero.  At a two-branch value a
residual closure instead ends in a rank-two factor, so this
rank-one argument makes no smoothness assertion there.

For the first survivor, every local factor except the length-three
factor at the \(3+1\) value is again Gorenstein.  A local
length-three algebra over \(\mathbf C\) is either
\[
\mathbf C[t]/(t^3)
\quad\text{or}\quad
\mathbf C[z,w]/(z,w)^2.
\tag{22}
\]
The first is Gorenstein and the second is not.  Apply the
four-coefficient description of a finite flat triple cover to the
rank-three henselian factor.  In the non-Gorenstein case all four
Miranda coefficients vanish, and every term of its discriminant has
degree four in those coefficients.  The local branch equation
therefore has multiplicity at least four.  Otherwise \(Y\) is
Gorenstein everywhere and the same different argument gives
\(\omega_Y\simeq\mathcal O_Y(E)\), hence \(E\) is Cartier.  This
conclusion does not include smoothness along a residual closure at a
two-branch value.

This dichotomy eliminates neither possibility.  It says that an
ordinary cuspidal \(3+1\) collision must lie on the Gorenstein side;
the only non-Gorenstein escape is a substantially more singular
unibranch branch value of multiplicity at least four.

## 5. Integral first homology of the complements

The surface \(S\) has the homotopy type of a real two-dimensional CW
complex,
\[
H_1(S;\mathbf Z)\simeq\mathbf Z/2,\qquad
\chi(S)=1.
\]
It follows that \(H_2(S;\mathbf Z)=0\).  Alexander--Lefschetz duality
for a reduced divisor with \(s\) irreducible components gives the
exact sequence
\[
0\longrightarrow\mathbf Z^s
\longrightarrow H_1(U;\mathbf Z)
\longrightarrow\mathbf Z/2
\longrightarrow0.
\tag{23}
\]
The extension class is the vector of divisor classes in
\[
\operatorname {Pic}(S)\simeq H^2(S;\mathbf Z)
\simeq\mathbf Z/2.
\tag{24}
\]
For one principal component that vector is zero, so (23) splits and
gives (13).  For two components, (20) says that the vector is either
\((0,0)\) or \((1,1)\).  The first gives the split group in (14); the
Smith normal form of
\[
\langle \mu_1,\mu_2,h\mid 2h=0\rangle
\]
is \(\mathbf Z^2\oplus\mathbf Z/2\), while that of
\[
\langle \mu_1,\mu_2,h\mid 2h=\mu_1+\mu_2\rangle
\]
is \(\mathbf Z^2\).  This proves (13)--(14).

## 6. Exact obstruction and next theorem

The first survivor is no longer just “a cusp plus a node.”  It forces
one of two sharply different objects:

* if some two-branch contact is odd, an irreducible principal
  hyperelliptic curve of genus \(e-1\), with
  \(1+4n-2e\) additional punctures and complement homology
  \(\mathbf Z\oplus\mathbf Z/2\);
* if every two-branch contact is even, two rational residual
  components whose divisor classes agree in \(\mathbf Z/2\).

The second survivor forces two punctured rational sections with equal
class, together with a single unramified boundary normalization
\(\mathbf A^1\) meeting both.

None of these profiles contradicts rational acyclicity, the order-two
class group, or transitive \(S_4\)-monodromy.  A valid continuation
must add one genuinely new input, for example:

1. a theorem forcing an odd self-intersection and then prohibiting the
   principal hyperelliptic curve with homology (13);
2. a theorem determining the common class in (10) and excluding its
   corresponding group in (14); or
3. a completion/intersection theorem showing that one affine-line
   boundary component cannot meet both residual sections while
   remaining disjoint from the ramification boundary.

The companion verifier checks the parity cover, Riemann--Hurwitz and
puncture ledgers, Euler identities, permutation orbits, and Smith
normal forms.  It does not verify the finite-normalization,
Alexander--Lefschetz, étale-local, or divisor-class arguments above.
