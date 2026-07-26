# Route A: log topology collapses the cubic boundary

Date: 25 July 2026

## Outcome

Let
\[
 S=\operatorname {Spec}
 \mathbf C[u,v,w]/(w^2-u-u^2v)
\]
and suppose that an étale morphism
\[
 F:S\longrightarrow\mathbf A^2
\]
has geometric degree three.  Let
\[
 \pi:Y\longrightarrow\mathbf A^2
\]
be the finite normalization in
\(\mathbf C(S)/\mathbf C(F)\), identify \(S\) with its open image in
\(Y\), and put
\[
 R=(Y\setminus S)_{\mathrm{red}}.
\]
Write \(r\) for the number of irreducible components of \(R\),
\(\Delta\) for the reduced branch curve of \(\pi\), and \(c\) for the
number of irreducible components of \(\Delta\).

The earlier cubic-topology audit left open the possibility that
singular points of \(Y\) on \(R\) have links with positive rational
first homology.  That possibility occurs for abstract finite cubic
normalizations, but it cannot occur in a partial compactification of
this particular \(S\).

> **Log-topology cubic-collapse theorem.**  Every singularity of every
> normal partial compactification \(Y\supset S\) has a
> rational-homology-sphere link.  Consequently
> \[
> H_c^1(R;\mathbf Q)=0.
> \tag{1}
> \]
> Each irreducible component of \(R\) has normalization
> \(\mathbf A^1\), different components are disjoint, and every point
> of \(R\) is analytically unibranch.
>
> For the finite cubic normalization above, the branch curve has the
> same three properties: every component has normalization
> \(\mathbf A^1\), distinct components are disjoint, and every affine
> branch singularity is unibranch.  In particular
> \[
> \chi(\Delta)=c.
> \tag{2}
> \]
> The exact cubic Euler balance therefore reduces to
> \[
> r+c+N_{\mathrm{tr}}=2,
> \tag{3}
> \]
> where \(N_{\mathrm{tr}}\) is the number of affine singular strata
> with transitive local inertia.  Since every branch component has a
> ramified boundary component,
> \[
> r\ge c\ge1.
> \tag{4}
> \]
> Equations (3)--(4) force
> \[
> \boxed{r=c=1,\qquad N_{\mathrm{tr}}=0.}
> \tag{5}
> \]

Thus the hypothetical cubic normalization has exactly one boundary
curve, namely the ramified curve above its unique irreducible branch
component.  Both curves have normalization \(\mathbf A^1\) and are
topologically affine lines.  Every affine branch fiber has two support
points and local inertia \(C_2\).  In particular the finite flat triple
cover is Gorenstein everywhere: its non-Gorenstein length-three fiber
would have one support point and hence transitive local inertia.

This is a genuine Keller-specific global restriction.  The Hesse-cone
and positive-\(b_1\) compatibility models from the earlier topology
audit cannot occur as \(Y\), because their exceptional resolutions
would have positive-genus or cyclic boundary topology, whereas every
completion boundary of \(S\) is a rational tree.

It is not yet a degree-three contradiction.  The remaining possibility
is exceptionally rigid:

1. \(\Delta\) is an irreducible polynomial curve whose normalization
   map \(\mathbf A^1\to\Delta\) is bijective;
2. all affine local inertia is contained in a transposition subgroup;
3. the global \(S_3\)-monodromy must therefore be assembled through
   conjugation at infinity rather than at an affine transitive fiber;
4. the unique boundary component must carry all cubic ramification.

The next exact target is consequently monodromy at the single place at
infinity, coupled to the fixed \(D_-\) arm of the canonical degree-six
plane normalization.  More raw affine Euler or local-class-group
estimates cannot improve (5).

## 1. The pseudoplane is rationally acyclic

The known invariants are
\[
 \pi_1(S)=\mathbf Z/2,\qquad \chi(S)=1.
\tag{6}
\]
A smooth affine complex surface has the homotopy type of a CW complex
of real dimension at most two.  Hence \(H_i(S;\mathbf Q)=0\) for
\(i>2\).  Equation (6) gives \(H_1(S;\mathbf Q)=0\), and the Euler
characteristic then gives
\[
 H_2(S;\mathbf Q)=0.
\tag{7}
\]
Thus \(S\) is a \(\mathbf Q\)-homology plane.

It is also rational:
\[
 \mathbf C(S)=\mathbf C(u,w),
\qquad
 v=\frac{w^2-u}{u^2}.
\tag{8}
\]

## 2. Every SNC completion boundary is a rational tree

Let \((X,B)\) be any smooth projective SNC completion of \(S\).  Since
\(X\) is a smooth projective model of the rational function field
\(\mathbf C(u,w)\), it is a rational surface.  In particular
\[
 H^1(X;\mathbf Q)=0.
\tag{9}
\]

The relative cohomology of the pair is compactly supported cohomology:
\[
 H^i(X,B;\mathbf Q)\simeq H_c^i(S;\mathbf Q).
\tag{10}
\]
Poincaré duality on \(S\), together with (7), gives
\[
 H_c^1(S;\mathbf Q)=H_c^2(S;\mathbf Q)=0.
\tag{11}
\]
The long exact sequence of \((X,B)\) first shows that \(B\) is
connected and then, from (9)--(11), that
\[
 H^1(B;\mathbf Q)=0.
\tag{12}
\]

For an SNC projective curve,
\[
 \dim H^1(B;\mathbf Q)
 =
 2\sum_{B_i\subset B}g(B_i)
 +b_1(\Gamma_B),
\tag{13}
\]
where \(\Gamma_B\) is the dual graph.  Equation (12) therefore says
that every \(B_i\) is rational and \(\Gamma_B\) is a tree.

This is the standard rational-tree property of completions of smooth
\(\mathbf Q\)-homology planes.  It also follows from the completion
discussion in Dubouloz--Palka, *The Jacobian Conjecture fails for
pseudo-planes*, Adv. Math. 339 (2018), 248--284,
[arXiv:1701.01425](https://arxiv.org/abs/1701.01425).

## 3. Boundary singularities cannot have positive-\(b_1\) links

Resolve \(Y\) by a morphism
\[
 \mu:X^\circ\longrightarrow Y
\]
which is an isomorphism over \(S\), complete \(X^\circ\), and perform
boundary blowups until \(B=X\setminus S\) is SNC.  This is an SNC
completion of the same \(S\), so Section 2 applies.

Let \(p\in Y\setminus S\) be singular.  Its reduced exceptional divisor
\[
 Z_p=\mu^{-1}(p)_{\mathrm{red}}
\]
is a connected subdivisor of \(B\).  It is therefore a tree of smooth
rational curves.  Its intersection matrix is negative definite.  The
standard plumbing calculation gives
\[
 b_1(\operatorname {Link}(p,Y);\mathbf Q)
 =
 2\sum_{C\subset Z_p}g(C)+b_1(\Gamma_{Z_p})=0.
\tag{14}
\]
Equivalently, the link is a rational homology sphere.  Since a normal
surface has only isolated singularities, \(Y\) is a rational homology
four-manifold.

This is exactly where the abstract Hesse-cone countermodel ceases to
apply.  Its exceptional curve has genus one and cannot be a subdivisor
of the rational-tree boundary of \(S\).

## 4. Alexander--Lefschetz duality kills the free correction

By Hamm's affine CW-dimension theorem, a complex affine variety of
complex dimension two has the homotopy type of a CW complex of real
dimension at most two.  In particular
\[
H_3(Y;\mathbf Q)=0.
\]
The pair sequence and (7) give
\[
 H_3(Y,S;\mathbf Q)=0.
\tag{15}
\]
By Section 3, the complex orientation on the smooth locus extends over
the rational-homology-sphere links to make \(Y\) an oriented rational
homology four-manifold.  Rational Alexander--Lefschetz duality is
therefore valid and identifies
\[
 H_3(Y,Y\setminus R;\mathbf Q)
 \simeq H_c^1(R;\mathbf Q).
\tag{16}
\]
Since \(S=Y\setminus R\), equations (15)--(16) prove (1).

There is a useful exact curve-theoretic expansion of (1).  Let
\[
 \nu:\widetilde R=\coprod_{i=1}^r\widetilde R_i\longrightarrow R
\]
be the normalization.  Write \(g_i\) for the genus of the smooth
projective completion of \(\widetilde R_i\), \(s_i\ge1\) for its number
of punctures, and \(b_p\) for the number of analytic branches of \(R\)
at \(p\).  The normalization exact sequence for the constant sheaf
gives
\[
 \dim H_c^1(R;\mathbf Q)
 =
 \sum_{i=1}^r(2g_i+s_i-1)
 +\sum_{p\in R}(b_p-1).
\tag{17}
\]
Every term is nonnegative.  Equation (1) forces
\[
 g_i=0,\qquad s_i=1,\qquad b_p=1
\tag{18}
\]
for every \(i,p\).  Hence
\[
 \widetilde R_i\simeq\mathbf A^1,
\tag{19}
\]
the components of \(R\) are mutually disjoint, and all their
singularities are unibranch.

## 5. A multibranch target point would exceed cubic length

The finite normal cubic surface is Cohen--Macaulay over the regular
plane, hence \(\pi\) is finite flat of rank three.  At the generic
point of every branch component \(\Delta_j\), total cubic ramification
is excluded by the unit argument, so
\[
 \operatorname {div}_Y(f_j)=2E_j+C_j.
\tag{20}
\]
Here \(E_j\subset R\) is ramified and has residue degree one.  Different
\(\Delta_j\)'s require different \(E_j\)'s.  This proves \(r\ge c\).

Suppose that \(\Delta\) had two distinct analytic branches at
\(q\).  Each branch is generically simple and therefore specializes to
a non-étale point of the length-three fiber \(\pi^{-1}(q)\).  Two
different non-étale support points would contribute length at least
\[
 2+2=4,
\tag{21}
\]
which is impossible.  Indeed, a local factor of length one in a fiber
over the algebraically closed residue field is the reduced algebra
\(\mathbf C\).  The base-change identity for relative differentials
and Nakayama's lemma then make \(\pi\) étale at that point.  Hence every
non-étale support has local fiber length at least two.  This explicitly
rules out the possibility that the two target branches specialize to
two different boundary points.  Thus all the ramification branches
specialize to one point \(p\in R\).

The finite image of one irreducible analytic curve germ is
irreducible.  Distinct target branches at \(q\) must therefore come
from distinct analytic branches of \(R\) at \(p\).  This contradicts
\(b_p=1\) in (18).  Consequently every point of \(\Delta\) is
unibranch.  In particular distinct irreducible components of
\(\Delta\) are disjoint.

The residue-degree-one map
\[
 E_j\longrightarrow\Delta_j
\]
induces a finite birational map of normalizations.  By (19),
\[
 \widetilde\Delta_j\simeq\widetilde E_j\simeq\mathbf A^1.
\tag{22}
\]
The normalization of each \(\Delta_j\) is bijective because all
singular points are unibranch.  It is therefore a homeomorphism in the
complex topology, and
\[
 \chi(\Delta_j)=1.
\tag{23}
\]
Since the components are disjoint, equations (2) follows.

## 6. The Euler equation has a unique solution

The cubic normalization balance from
`ROUTE_A_CUBIC_NORMALIZATION_TOPOLOGY_AUDIT.md` is now unconditional:
\[
 r+\chi(\Delta)+N_{\mathrm{tr}}=2.
\tag{24}
\]
Substitution of (2) gives (3).  The integer constraints
\[
 r\ge c\ge1,\qquad N_{\mathrm{tr}}\ge0
\]
have the unique solution (5).

At a non-Gorenstein Miranda point, the length-three fiber is
\[
 \mathbf C[z,w]/(z,w)^2.
\]
It has one support point, so its local inertia is transitive.  Equation
\(N_{\mathrm{tr}}=0\) rules out every such point.  It also rules out
curvilinear total cubic fibers.  Hence every affine branch fiber has
the \(2+1\) support pattern and the cubic cover is Gorenstein.

## 7. What (5) does and does not settle

The normalization map
\[
 \mathbf A^1\longrightarrow\Delta
\tag{25}
\]
is polynomial, finite, and bijective.  It need not be an isomorphism:
a unibranch cusp is the basic remaining possibility.  Therefore the
standard theorem excluding a smooth embedded affine-line component of
the nonproper set does not by itself exclude (25).

There is also a scope issue in applying Chau's simply-connected-curve
theorem to the degree-six plane lift.  Its full nonproper-value set
contains both \(\Delta\) and the distinguished collision image
\(\Gamma_D\).  The latter is forced to identify distinct normalization
points, so the full union need not be simply connected.  The primary
results checked here are:

- Nguyen Van Chau, *Two remarks on non-zero constant Jacobian
  polynomial maps of \(\mathbf C^2\)*, Ann. Polon. Math. 82 (2003),
  39--44, especially Theorem 4 and Corollary 3;
- Nguyen Van Chau, *Non-proper value set and the Jacobian condition*,
  Ann. Polon. Math. 84 (2004), 203--210.

They do not, in the form cited, give a componentwise prohibition
against every singular bijective polynomial parametrization.  Thus
(5) should be used as a sharp reduction, not advertised as a completed
degree-three exclusion.

The live question is now finite and Keller-specific: can an irreducible
one-place polynomial curve with bijective normalization support a
connected cubic \(S_3\)-cover whose every affine inertia group is
\(C_2\), while its unique ramified boundary curve fits into the same
rational-tree completion as the fixed \(D_-\) arm?  Any contradiction
must enter through the single place at infinity.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_log_topology_cubic_collapse.py
```

for the rational-acyclic Betti calculation, the compactly-supported
curve formula, the cubic fiber-length obstruction, and the unique
integer solution of the Euler balance.  The completion, plumbing,
Alexander--Lefschetz, normalization, and finite-flat inputs are
theorem-level geometric arguments proved above.
