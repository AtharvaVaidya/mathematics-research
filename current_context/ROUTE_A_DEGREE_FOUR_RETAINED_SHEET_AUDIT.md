# Route A: degree-four collapse and the retained-sheet escape

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad
S=\operatorname {Spec}B=S(2,2,1),
\]
and suppose that an étale morphism
\[
F:S\longrightarrow\mathbf A^2
\]
has geometric degree \(4\).  Let
\[
\pi:Y\longrightarrow\mathbf A^2
\]
be the finite normalization in
\(\operatorname {Frac}(B)/\mathbf C(F)\), with \(S\subset Y\) the
canonical open immersion.  Write
\[
R=(Y\setminus S)_{\mathrm{red}},\qquad
\Delta=\operatorname {Branch}(\pi)_{\mathrm{red}}.
\]

The cubic retained-line proof does not extend verbatim, but its
topological part has a sharp quartic successor.

> **Quartic collapse theorem.**  Every irreducible component of
> \(\Delta\) has normalization \(\mathbf A^1\).  If
> \[
> c=\#\operatorname {Irr}(\Delta),\qquad
> r=\#\operatorname {Irr}(R),
> \]
> if \(t\) is the number of branch components whose generic inertia is
> a \(3\)-cycle, and if \(\delta\) is the total support-orbit deficit at
> exceptional unibranch values, then
> \[
> \boxed{r=3-c-t-\delta.}
> \tag{1}
> \]
> Since every branch component supplies a distinct ramified boundary
> component, \(r\ge c\).  Consequently \(c=1\), and precisely three
> numerical cases remain:
> \[
> \begin{array}{c|c|c|c}
> \text{generic inertia}&t&\delta&r\\ \hline
> (3)(1)&1&0&1,\\
> (2)(1)(1)&0&1&1,\\
> (2)(1)(1)&0&0&2.
> \end{array}
> \tag{2}
> \]

The first line of (2) is impossible.  Its unique retained simple sheet
is a closed, unpunctured homology line in \(S\), so the cubic argument again
rectifies the branch to an affine line; cyclic complement monodromy
cannot act transitively on four sheets while a meridian acts as a
\(3\)-cycle.

The remaining two lines identify the exact new obstruction.

1. In the \(r=1,\delta=1\) case, the unique exceptional unibranch
   fiber has orbit partition
   \[
   4=3+1.
   \]
   One of the two generically fixed sheets is absorbed into the
   length-three boundary point.  Moreover this case must have at least
   one two-branch self-intersection of \(\Delta\).  At such a value the
   two local transpositions are disjoint and the fiber is
   \[
   4=2+2,
   \]
   entirely on the omitted boundary.  Thus the retained residual
   curves are punctured.
2. In the \(r=2,\delta=0\) case there is one extra boundary curve.
   Two-branch self-intersections again absorb all retained points.  If
   there is no such self-intersection, the residual degree-two cover
   over the normalization \(\mathbf A^1\) splits into two sections; to
   avoid the homology-line contradiction, the extra boundary curve
   must map to a curve different from \(\Delta\) and puncture both
   sections.  The branch must still be singular, since a smooth
   \(\mathbf A^1\) branch gives the cyclic-monodromy contradiction
   directly on \(Y\).

Thus degree four does **not** presently reduce to a complete retained
homology line.  The live problem is sharply localized: exclude the
\(3+1\) collision together with a \(2+2\) self-intersection, or exclude
an extra unramified boundary curve that punctures both retained
sections.  Bare Euler characteristic, divisor multiplicity, and
permutation transitivity do not exclude either configuration.

## 1. Topology inherited from the cubic proof

The following facts used in the cubic paper do not depend on the
degree of \(\pi\):

1. \(Y\) is a normal affine surface finite flat over \(\mathbf A^2\).
2. The boundary \(Y\setminus S\) is pure of dimension one.
3. A resolution of \(Y\) which is an isomorphism over \(S\) has
   exceptional divisors contained in the rational tree at infinity of
   the \(\mathbf Q\)-homology plane \(S\).
4. Every singular link of \(Y\) is therefore a rational homology
   three-sphere.
5. Alexander--Lefschetz duality and the pair sequence for
   \(S=Y\setminus R\) give
   \[
   H_c^1(R;\mathbf Q)=0.
   \tag{3}
   \]

The normalization sequence for the reduced affine curve \(R\) then
gives
\[
\dim H_c^1(R;\mathbf Q)
=\sum_i(2g_i+s_i-1)+\sum_{p\in R}(b_p-1).
\tag{4}
\]
Hence every boundary component has normalization \(\mathbf A^1\),
each has one place at infinity, distinct boundary components are
disjoint, and every boundary point is analytically unibranch.  In
particular
\[
\chi(R)=r.
\tag{5}
\]

## 2. The exact generic inertia list

Let \(\Delta_j\) be an irreducible branch component.  Tame generic
inertia is cyclic.  If every geometric inertia orbit were ramified,
then every prime over \(\Delta_j\) would be omitted from \(S\).  The
pullback of an equation of \(\Delta_j\) would be a nonconstant unit of
\(B\), which is impossible because \(B^\times=\mathbf C^\times\).

The cycle types \((4)\) and \((2)(2)\) are therefore excluded.  The
only possibilities are
\[
(2)(1)(1),\qquad (3)(1).
\tag{6}
\]
Equivalently, at the generic point one has one of
\[
\operatorname {div}_Y(f_j)=2E_j+C_{j,1}+C_{j,2}
\tag{7}
\]
after geometric residue-field splitting, or
\[
\operatorname {div}_Y(f_j)=3E_j+C_j.
\tag{8}
\]
In (7), the two fixed sheets can form one residue-degree-two prime.
The ramified prime \(E_j\) has residue degree one, lies in \(R\), and
maps birationally to \(\Delta_j\).

Distinct \(\Delta_j\) give distinct \(E_j\).  Since the normalization
of \(E_j\) is \(\mathbf A^1\), the same is true of the normalization of
\(\Delta_j\).  This proves both
\[
r\ge c
\tag{9}
\]
and the first assertion of the collapse theorem.

## 3. Multibranch values are exactly \(2+2\)

We first record the specialization fact used below.  Choose a small
analytic ball about a branch value \(q\), and a nearby smooth point on
one analytic branch of \(\Delta\).  A meridian about that smooth point
can be represented inside the punctured local ball.  Its generic
inertia permutation therefore belongs to the local monodromy group at
\(q\).  Equivalently, every local-monodromy orbit at \(q\) is a union
of orbits of the nearby generic inertia.  In particular, the endpoint
of a transposition branch has local fiber length at least two, and the
endpoint of a triple-inertia branch has length at least three.

Let \(q\in\Delta\) have at least two analytic branches.  Every target
branch has a ramification curve germ whose endpoint lies in \(R\).
Distinct target branches have distinct endpoints: a single unibranch
source curve germ has an irreducible analytic image, while distinct
boundary components are disjoint.

Each endpoint has local fiber length at least two.  Since the whole
fiber has length four, there are exactly two target branches, both
generically simple, their endpoints both have length two, and there is
no other support point:
\[
\pi^{-1}(q)_{\mathrm{support}}=\{p_1,p_2\},\qquad
\operatorname {length}_{p_1}= \operatorname {length}_{p_2}=2.
\tag{10}
\]
On the four sheets the two branch meridians are disjoint
transpositions.  No branch of generic type \((3)(1)\) can meet another
branch.  Notice that (10) need not be a transverse ordinary node; it
is a two-branch value, and that is all the Euler calculation needs.

Outside a finite set of singular values and points where the fiber
support differs from its generic value, the support count is constant;
call that finite set the exceptional set.  At an exceptional value
with one analytic branch, put
\[
k_j=
\begin{cases}
3,&\text{for generic type }(2)(1)(1),\\
2,&\text{for generic type }(3)(1),
\end{cases}
\qquad
\delta_q=k_j-o_q,
\tag{11}
\]
where \(o_q\) is the number of local-monodromy orbits, equivalently the
number of support points in the fiber.  The specialization observation
shows that adding local monodromy can merge generic-inertia orbits but
cannot split them.  Hence \(o_q\le k_j\) and \(\delta_q\ge0\).  Let
\[
\delta=\sum_{\text{unibranch }q}\delta_q.
\tag{12}
\]

## 4. Euler calculation

Let \(n\) be the total number of two-branch values, counted with one
for every extra normalization point.  Since the normalization of each
branch component is \(\mathbf A^1\),
\[
\chi(\Delta)=c-n.
\tag{13}
\]
There are \(c-t\) transposition components and \(t\) triple components,
so the sum of their generic support counts is
\[
3(c-t)+2t=3c-t.
\tag{14}
\]

Stratify \(\mathbf A^2\) by the complement of \(\Delta\), the smooth
normalization strata of its components, and the exceptional values.
Over the complement the fiber has four points.  A two-branch value
removes two generic three-point strata but contributes the two support
points in (10).  Its correction is therefore
\[
4-3-3+2=0;
\tag{15}
\]
the \(+4\) is the correction already present in
\(4(1-\chi(\Delta))\) when (13) identifies two normalization points.
Every exceptional unibranch value contributes \(-\delta_q\).
Consequently
\[
\chi(Y)=4-c-t-\delta.
\tag{16}
\]
Since \(\chi(S)=1\), additivity and (5) give
\[
r=\chi(R)=\chi(Y)-\chi(S)=3-c-t-\delta,
\]
which is (1).  Combining this equality with (9) yields
\[
2c+t+\delta\le3.
\tag{17}
\]
The branch is nonempty: otherwise the connected finite cover \(Y\) of
\(\mathbf A^2\) would be finite étale, hence trivial, contrary to
degree four.  Thus \(c\ge1\).  Equation (17) forces \(c=1\), and (2)
follows.

## 5. Triple inertia is impossible

Suppose the generic inertia is \((3)(1)\).  Then (2) gives
\[
r=1,\qquad \delta=0.
\]
Write \(E\) for the boundary and \(C\) for the retained simple prime.
There are no two-branch values by Section 3.  At every point of
\(\Delta\), the fiber has the same two support points as the generic
fiber.  Thus \(E\) and \(C\) never meet.  Since \(E\) is the whole
boundary,
\[
C\subset S.
\]
The base change \(F^{-1}(\Delta)\to\Delta\) is reduced and étale, and
its retained part has rank one.  Hence
\[
C\xrightarrow{\sim}\Delta.
\tag{18}
\]

The normalization \(\mathbf A^1\to\Delta\) is bijective because
\(\Delta\) has one analytic branch at every point.  Thus \(C\) is a
homology line.  Zaidenberg's theorem makes \(C\), and hence \(\Delta\),
smooth because \(S(2,2,1)\not\simeq\mathbf A^2\).  The
Abhyankar--Moh--Suzuki theorem then gives
\[
\mathbf A^2\setminus\Delta\simeq\mathbf A^1\times\mathbf G_m.
\]
Its fundamental group is cyclic.  But
\(\pi^{-1}(\mathbf A^2\setminus\Delta)\) is connected of degree four,
whereas a generator acting as a \(3\)-cycle has two orbits.  This is a
contradiction.

## 6. Geometry of the two simple-inertia survivors

We will use the following residual-cover lemma.  In the
simple-inertia case, let
\[
D_{\mathrm{res}}=\pi^*\Delta-2E
\]
as an effective Weil divisor, pull it back to the normalization
\(\widetilde\Delta\simeq\mathbf A^1\): more formally, normalize
\[
\left(
\operatorname {Supp}(D_{\mathrm{res}})
\times_\Delta\widetilde\Delta
\right)_{\mathrm{red}}.
\]
The result is finite over \(\widetilde\Delta\), and its
coordinate module is torsion-free of generic rank two over
\(\mathbf C[t]\).  It is therefore finite flat of degree two.  If
every residual fiber has two support points, flatness makes both local
fiber lengths equal to one.  The normalized cover is then unramified,
hence finite étale, and every finite étale cover of \(\mathbf A^1\)
splits.  Thus the residual cover is the disjoint union of two
rank-one sections.

If one of those sections avoids the boundary, its image is a
rank-one connected component of the reduced étale base change
\(F^{-1}(\Delta)\to\Delta\).  It maps isomorphically to \(\Delta\).
Since the no-node normalization
\(\mathbf A^1\to\Delta\) is bijective, the section is a homology line
on \(S\).

### 6.1 One boundary component and one orbit deficit

Now suppose
\[
r=1,\qquad \delta=1.
\tag{19}
\]
At the unique deficient unibranch value, the ramified endpoint lies on
the only boundary component \(E\).  Every other support point lies in
\(S\) and must have fiber length one by étaleness.  The only possible
length partition is therefore
\[
4=3+1.
\tag{20}
\]
In particular, the local monodromy is transitive on the ramified pair
and one generically fixed sheet, and fixes the remaining sheet.  This
is the quartic analogue of the cubic cusp collision, but it leaves one
simple support point.

This case must also contain a two-branch value.  Indeed, assume there
is none.  Pull the residual degree-two divisor in (7) back to the
normalization \(\widetilde\Delta\simeq\mathbf A^1\) and normalize it.
At every nonexceptional point its two sheets remain distinct.  At the
point (20), one residual sheet meets \(E\), but the other remains a
distinct support point.  The length-three point contains the
length-two ramified contribution and one residual contribution, so the
residual fiber still has two length-one points.  The residual-cover
lemma therefore splits the cover into two copies of
\(\mathbf A^1\).

One of the corresponding rank-one residual primes does not meet
\(E\): exactly one of the two sections supplies the residual branch at
the unique deficient value, and there are no other deficits or
two-branch values at which the other section could meet \(E\).  The
other section is therefore a closed, unpunctured affine curve in
\(S\), maps isomorphically to \(\Delta\), and is a homology line.  The
argument of Section 5 again gives a contradiction.  Hence a survivor
of (19) necessarily has a two-branch self-intersection.  At each such
value, (10) says that the entire fiber lies on \(E\), at two different
points.  Both residual sheets are thereby punctured.

### 6.2 Two boundary components and no orbit deficit

Finally suppose
\[
r=2,\qquad \delta=0.
\tag{21}
\]
Besides the ramified boundary \(E\), there is one curve \(E'\).
If \(E'\) dominates \(\Delta\), it has residue degree one.  Indeed,
residue degree two would make \(E\) and \(E'\) exhaust every prime
over \(\Delta\).  The pullback of an equation of \(\Delta\) would then
restrict to a nonconstant unit on \(S\), contradicting
\(B^\times=\mathbf C^\times\).  Thus the other residual prime is
retained.  In the absence of a two-branch value, support count three
keeps that retained prime disjoint from both boundary components.  It
is again a closed, unpunctured homology line, so this subcase is
impossible.

If there is no two-branch value at all, the normalized residual
degree-two cover of \(\mathbf A^1\) is étale and splits into two
rank-one sections.  Therefore the only remaining no-node escape has
\[
\pi(E')=\Gamma\ne\Delta
\tag{22}
\]
and \(E'\) meets both residual sections.  Removing \(E'\) punctures
both curves before they enter \(S\).

If there is a two-branch value, (10) already punctures both residual
sheets at omitted ramification points.  In either situation no closed,
unpunctured homology line is forced by the quartic bookkeeping.  Also,
\(\Delta\) cannot be a smooth affine line in either escape: if it
were, the connected cover of
\(\mathbf A^2\setminus\Delta\simeq\mathbf A^1\times\mathbf G_m\)
would have cyclic monodromy generated by a transposition, hence could
not be transitive on four sheets.

## 7. Exact permutation compatibility

The surviving local data are not a permutation-theoretic fantasy.
The three transpositions
\[
a=(12),\qquad b=(23),\qquad c=(34)
\tag{23}
\]
generate \(S_4\).

At a cusp-type unibranch value, \(a\) and \(b\) satisfy the braid
relation
\[
aba=bab
\]
and generate an \(S_3\) orbit of size three plus one fixed sheet,
exactly (20).  At a two-branch value, \(a\) and \(c\) commute and have
two orbits of size two, exactly (10).  Thus the local groups needed by
the first simple-inertia survivor coexist with transitive quartic
monodromy.  A global proof must use more than cycle partitions and
Euler characteristic.

## 8. An algebraic collision model

There is also a completely explicit connected quartic cover showing
why retained curves can cease to be complete.  Consider
\[
\pi_0:\mathbf A^2_{x,z}\longrightarrow\mathbf A^2_{x,y},
\qquad
y=z^4+xz.
\tag{24}
\]
It is finite flat of rank four, with basis \(1,z,z^2,z^3\).  The
quartic
\[
T^4+xT-y
\]
has discriminant
\[
D=-256y^3-27x^4.
\tag{25}
\]
The ramification curve and branch parametrization are
\[
E=V(x+4z^3),\qquad
(x,y)=(-4z^3,-3z^4).
\tag{26}
\]
Pulling (25) back to the source gives the exact factorization
\[
D(x,z)=
-(x+4z^3)^2
\bigl(27x^2+40xz^3+16z^6\bigr).
\tag{27}
\]
Over \(\mathbf C\), the residual quadratic factor splits into two
affine lines
\[
C_\pm=V(x-\alpha_\pm z^3),\qquad
\alpha_\pm=\frac{-20\pm4i\sqrt2}{27}.
\tag{28}
\]
Both meet \(E\) at the unique \((3,4)\)-cusp value.  After deleting
the ramification curve, each retained residual line becomes
\(\mathbf A^1\setminus\{0\}\), not a homology line.

This model is **not** a counterexample on \(S(2,2,1)\):
\[
\mathbf A^2\setminus E\simeq\mathbf A^1\times\mathbf G_m,
\]
and its exceptional fiber has one support point, so its orbit deficit
is \(2\), not one of the two surviving rows of (2).  Its role is
sharper and limited: it proves algebraically that, in degree four,
the residual fixed sheets can hit the omitted ramification boundary
and lose precisely the completeness needed by the cubic homology-line
argument.

## 9. Best next target

The most economical continuation is not a search over quartic
polynomials.  It is one of the following two structural statements:

1. prove that an irreducible rational branch curve of a quartic
   normalization of \(S(2,2,1)\) cannot have the simultaneous
   \(3+1\) unibranch collision and \(2+2\) self-intersection forced by
   Section 6.1; or
2. use \(\pi_1(S)=\mathbf Z/2\) and
   \(\operatorname {Cl}(S)=\mathbf Z/2\) to exclude the extra
   unramified boundary curve in (22), perhaps by comparing the two
   puncture meridians with the order-two boundary class.

Either result would restore a closed, unpunctured retained homology line and
finish degree four.  Without one of them, the cubic mechanism has
reached its exact limit.

The accompanying verifier
`verify_route_a_degree_four_retained_sheet_audit.py` checks the Euler
arithmetic, permutation partitions, transitivity examples, and the
explicit quartic factorization.  It does not verify the normalization,
duality, residual-cover, Zaidenberg, or Abhyankar--Moh--Suzuki
arguments, which remain theorem-level parts of this note.
