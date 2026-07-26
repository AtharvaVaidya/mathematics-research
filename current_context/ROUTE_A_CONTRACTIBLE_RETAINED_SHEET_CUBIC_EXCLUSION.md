# Route A: the contractible retained sheet excludes cubic degree

Date: 25 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v),\qquad S=\operatorname {Spec}B,
\]
and suppose that a Darboux pair \(P,Q\in B\) induces an étale map
\[
F=(P,Q):S\longrightarrow\mathbf A^2
\]
of geometric degree \(3\).  Let
\[
\pi:Y\longrightarrow\mathbf A^2
\]
be the finite normalization in
\(\operatorname {Frac}(B)/\mathbf C(P,Q)\), with \(S\subset Y\) the
open immersion supplied by Zariski's Main Theorem.

The log-topology cubic-collapse theorem proved earlier says that:

1. the reduced branch curve \(\Delta\) is irreducible and its
   normalization is a finite bijection
   \(\mathbf A^1\to\Delta\);
2. the boundary \(R=(Y\setminus S)_{\mathrm{red}}\) has exactly one
   irreducible component \(E\);
3. generically over \(\Delta\),
   \[
   \operatorname {div}_Y(f)=2E+\overline C,
   \tag{1}
   \]
   where \(f=0\) defines \(\Delta\), and every affine branch fiber has
   exactly two support points, of lengths \(2\) and \(1\).

These facts, combined with the classification of homology lines on
\(\mathbf Q\)-homology planes, give a contradiction.

> **Cubic exclusion theorem.** There is no étale morphism
> \[
> F:S(2,2,1)\longrightarrow\mathbf A^2
> \]
> of geometric degree \(3\).  Equivalently, there is no Darboux pair
> \(P,Q\in B\) with \(\{P,Q\}=1\) and
> \[
> [\operatorname {Frac}B:\mathbf C(P,Q)]=3.
> \]

The key new bridge is that the retained curve is not merely a generic
sheet:
\[
\overline C\cap E=\varnothing,\qquad
C:=\overline C\subset S,\qquad
C\xrightarrow{\;\sim\;}\Delta.
\tag{2}
\]
Thus \(C\) is a homology line on the specific pseudoplane.  A theorem
of Zaidenberg forces every such curve on \(S\) to be smooth, because a
singular homology line can occur only when the ambient
\(\mathbf Q\)-homology plane is \(\mathbf A^2\).  It follows that
\(\Delta\simeq\mathbf A^1\) is a smooth embedded affine line.  The
Abhyankar--Moh--Suzuki theorem rectifies it.  But then the connected
cubic cover away from \(\Delta\) has cyclic monodromy, whereas its
generic branch meridian is a transposition.  This is impossible.

This is a genuine degree-three exclusion.  It does not assume that
every principal affine line on \(S\) is a fiber of the standard
\(\mathbf A^1\)-fibration; that stronger assertion is false in this
level of generality and is not needed.

## 1. The retained prime never reaches the boundary

First, the affine open immersion \(S\subset Y\) has no isolated
boundary point away from its divisorial boundary.  Here is the standard
normal-surface purity argument.  If \(z\in Y\setminus S\) were such a
point, choose a function \(g\in\mathcal O(Y)\) which vanishes on every
divisorial boundary component but not at \(z\).  Then
\[
W=D_Y(g)
\]
is a normal affine surface, its nonempty complement
\[
Z=W\setminus(S\cap W)
\]
is finite, and
\[
S\cap W=D_S(g)
\]
is affine.  Normality and codimension-two Hartogs extension give
\[
\Gamma(W\setminus Z,\mathcal O)=\Gamma(W,\mathcal O).
\]
If \(W\setminus Z\) were affine, its canonical affinization would
therefore identify it with \(W\), contradicting \(Z\ne\varnothing\).
Thus the boundary is pure of codimension one.  Since the collapse has
\(r=1\), its underlying set is exactly \(E\).
This is also the normal-surface case of the Stacks Project,
[Section 31.17, “Complements of affine
opens”](https://stacks.math.columbia.edu/tag/0BCQ).

Both maps
\[
E\longrightarrow\Delta,\qquad
\overline C\longrightarrow\Delta
\tag{3}
\]
are finite and generically have residue degree one.  Their
normalizations are therefore identified with the normalization
\(\mathbf A^1\) of \(\Delta\): each finite birational curve map factors
through this common normalization.

The normalization map
\[
\nu:\mathbf A^1\longrightarrow\Delta
\tag{4}
\]
is bijective.  Consequently, for every \(q\in\Delta\), each curve in
(3) has exactly one point above \(q\).  Indeed, every point above \(q\)
lifts to a point of the normalization, and (4) has only one such
point.

Suppose that \(p\in E\cap\overline C\), and put \(q=\pi(p)\).  The
unique point of \(E\) above \(q\) and the unique point of
\(\overline C\) above \(q\) would then be the same point \(p\).
There are no further points of \(\pi^{-1}(q)\): the underlying inverse
image of \(\Delta\) is \(E\cup\overline C\).  Indeed, because \(\pi\)
is finite flat and \(Y\) is a normal, hence Cohen--Macaulay, surface,
the pullback equation \(f\) is a nonzerodivisor and
\(\mathcal O_Y/(f)\) is Cohen--Macaulay of pure dimension one.  It has
no isolated or embedded zero-dimensional component.  Finiteness also
prevents a one-dimensional component from mapping to a point, so every
component dominates \(\Delta\), and (1) lists all of them.

Hence the length-three fiber over \(q\) would have only one support
point.

This contradicts the cubic-collapse theorem, which excludes both
possible local length-three algebras:

- the curvilinear algebra \(\mathbf C[t]/(t^3)\), whose local inertia
  is transitive; and
- the non-Gorenstein algebra
  \(\mathbf C[x,y]/(x,y)^2\).

Equivalently, a one-support fiber has one orbit on the three local
sheets, so \(o_q=1\); it is a transitive stratum and contributes to
\(N_{\mathrm{tr}}\).  The already-proved equality
\(N_{\mathrm{tr}}=0\) rules it out.  Every affine branch fiber
therefore has the \(2+1\) support pattern, so
\[
E\cap\overline C=\varnothing.
\tag{5}
\]
Since \(E\) is the whole reduced boundary, (5) puts
\(\overline C\) entirely inside \(S\).  We henceforth write
\[
C=\overline C.
\]

The familiar cubic
\[
z^3-3xz+2y=0
\]
is a useful adversarial check on this step.  Its total surface is
smooth, its branch is the cusp \(y^2=x^3\), and eliminating \(y\)
gives
\[
y^2-x^3=-\frac14(x-z^2)^2(4x-z^2).
\]
The ramified and retained primes meet at the cusp; the fiber there is
\(\mathbf C[z]/(z^3)\), with transitive local monodromy.  Thus this
standard countermodel fails exactly at \(N_{\mathrm{tr}}=0\), as the
argument predicts.

## 2. The retained curve is the branch curve

The scheme-theoretic inverse image of \(\Delta\) in \(S\) is
\[
F^{-1}(\Delta)=V(f(P,Q))=C.
\tag{6}
\]
To justify the last equality scheme-theoretically, first note that
\(S\times_{\mathbf A^2}\Delta\) is reduced: it is an étale base change
of the reduced complex curve \(\Delta\).  Its underlying set is the
intersection with \(S\) of the pure divisor
\(\pi^{-1}(\Delta)_{\mathrm{red}}=E\cup\overline C\).  Equation (5) and
\(E=Y\setminus S\) leave precisely \(C\), with no isolated component
by flat purity.  Thus the reduced base change is exactly the integral
curve \(C\).  Equivalently, restriction of (1) to \(S\) gives the
reduced divisor
\[
\operatorname {div}_S(f(P,Q))=C.
\tag{7}
\]

By (5), the finite morphism
\(\overline C\to\Delta\) in \(Y\) is precisely the restriction
\[
F|_C:C\longrightarrow\Delta.
\]
It is finite, surjective, and generically of degree one.  It is also
étale, because (6) is a base change of the étale morphism \(F\).
Thus it is finite étale of constant rank one.

A finite étale algebra of rank one is the base ring itself: locally it
is free of rank one, and its identity element is a basis in every
residue fiber.  Therefore
\[
\boxed{F|_C:C\xrightarrow{\sim}\Delta.}
\tag{8}
\]

The finite bijective normalization (4) is a homeomorphism in the
complex topology.  Equations (4) and (8) show that \(C\) is an
irreducible affine curve homeomorphic to \(\mathbf A^1(\mathbf C)\),
with normalization \(\mathbf A^1\).  In the terminology of
Zaidenberg, \(C\) is a homology line.

## 3. A homology line on this pseudoplane is smooth

The surface \(S\) is smooth: for
\[
H=w^2-u-u^2v
\]
one has
\[
H_u=-1-2uv,\qquad H_v=-u^2,\qquad H_w=2w,
\]
and the three derivatives cannot vanish simultaneously.  It is the
smooth \(\mathbf Q\)-homology plane \(S(2,2,1)\), with
\[
\operatorname {Cl}(S)\simeq\mathbf Z/2.
\tag{9}
\]
In particular \(S\not\simeq\mathbf A^2\).

Zaidenberg's homology-line theorem states:

> If \(X\) is a smooth \(\mathbf Q\)-homology plane and
> \(\Gamma\subset X\) is a singular homology line, then
> \(X\simeq\mathbf A^2\); moreover, after an automorphism of
> \(\mathbf A^2\), \(\Gamma\) has equation
> \(x^k-y^\ell=0\) for coprime \(k,\ell\ge2\).

This is Theorem 1(c) of M. Zaidenberg, *Affine lines on
\(\mathbf Q\)-homology planes and group actions*, Transform. Groups
**11** (2006), 725--735,
[doi:10.1007/s00031-005-1122-5](https://doi.org/10.1007/s00031-005-1122-5).
The paper defines a \(\mathbf Q\)-homology plane to be smooth and
\(\mathbf Q\)-acyclic, and a homology line to be an irreducible affine
curve homeomorphic to \(\mathbf R^2\), equivalently in this setting
with normalization \(\mathbf A^1\) and Euler characteristic one.  Thus
all its hypotheses apply to \(S\) and \(C\).

If \(C\) were singular, the theorem would give
\(S\simeq\mathbf A^2\), contradicting (9).  Hence
\[
C\simeq\mathbf A^1.
\tag{10}
\]
By (8), the branch curve is also smooth:
\[
\boxed{\Delta\simeq\mathbf A^1.}
\tag{11}
\]

Notice that the conclusion used here is smoothness, not verticality
for the standard fibration \(u:S\to\mathbf A^1\).  For example,
\[
V(v)\subset S,\qquad
B/(v)\simeq\mathbf C[u,w]/(w^2-u)\simeq\mathbf C[w],
\tag{12}
\]
is a principal affine line which is not a fiber of \(u\).  Thus an
argument claiming that every principal contractible curve is a
standard fiber would be invalid.  The homology-line theorem supplies
exactly the weaker fact needed in (10).

## 4. Cyclic complement monodromy contradicts simple cubic inertia

By the Abhyankar--Moh--Suzuki embedding theorem, a smooth closed
embedding
\[
\Delta\simeq\mathbf A^1\hookrightarrow\mathbf A^2
\]
is rectifiable by a polynomial automorphism of \(\mathbf A^2\).
Consequently
\[
V:=\mathbf A^2\setminus\Delta
\simeq\mathbf A^1\times\mathbf G_m,
\qquad
\pi_1(V)\simeq\mathbf Z.
\tag{13}
\]

Set
\[
U=S\setminus C.
\]
Equations (1), (5), and the fact that \(R=E\) give
\[
U
=Y\setminus(E\cup C)
=\pi^{-1}(V).
\tag{14}
\]
Therefore
\[
\pi|_U:U\longrightarrow V
\tag{15}
\]
is a finite étale cover of degree three.  It is connected because
\(U\) is a nonempty open subset of the irreducible surface \(S\).

The monodromy image of a connected degree-three cover is a transitive
subgroup of \(S_3\).  By (13), it is generated by one meridian around
\(\Delta\), hence is cyclic.  The only cyclic transitive subgroup of
\(S_3\) is \(A_3\simeq C_3\), generated by a three-cycle.

On the other hand, the generic ramification in (1) is simple:
\[
3=2\cdot1+1\cdot1.
\]
A positively oriented meridian around \(\Delta\) therefore acts on the
three sheets as a transposition.  The cyclic group generated by a
transposition has two orbits and is not transitive.  This contradicts
the connectedness of (15).

The assumed degree-three étale map \(F\) cannot exist.

## 5. Dependency audit

The proof uses the following earlier Route A results:

1. the open immersion \(S\subset Y\);
2. the cubic branch divisor \(2E+\overline C\);
3. the log-topology collapse
   \(r=c=1\), bijective \(\mathbf A^1\)-normalization of \(\Delta\),
   and the \(2+1\) support pattern in every affine branch fiber;
4. \(\operatorname {Cl}(S)\simeq\mathbf Z/2\).

The external theorem-level inputs are:

1. Zaidenberg's singular-homology-line theorem, quoted with its exact
   hypotheses in Section 3;
2. the Abhyankar--Moh--Suzuki rectification theorem for smooth
   embeddings of \(\mathbf A^1\) in \(\mathbf A^2\);
3. the standard equivalence between connected finite étale covers over
   \(\mathbf C\) and finite topological covering spaces.

No classification of all principal curves on \(S\), no assumption that
\(C\) is a fiber of \(u\), and no unproved componentwise version of
Chau's nonproper-set theorem is used.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_contractible_retained_sheet_cubic_exclusion.py
```

The verifier checks smoothness of \(S\), the explicit transverse
principal affine line (12), the two length-three local algebras, the
rank-one étale algebra step, and the cyclic-subgroup obstruction in
\(S_3\).  The geometric inputs listed in Section 5 remain
theorem-level arguments.
