# Route A: low-log-complexity generic fibers are impossible

Date: 26 July 2026

## Outcome

Let
\[
B=\mathbf C[u,v,w]/(w^2-u-u^2v)
\]
with
\[
\{u,v\}=-2w,\qquad
\{u,w\}=-u^2,\qquad
\{v,w\}=1+2uv,
\]
and suppose
\[
\{P,Q\}=1,\qquad P,Q\in B.
\tag{1}
\]
Put
\[
K=\mathbf C(P),\qquad
A_K=B\otimes_{\mathbf C[P]}K.
\]

The generic fiber of \(P\) cannot be either of the two smooth rational
affine curves of log complexity at most zero:
\[
\boxed{
A_K\not\simeq K[t],\qquad
A_K\not\simeq K[t,t^{-1}].
}
\tag{2}
\]
The same conclusion holds after interchanging \(P\) and \(Q\).

There is a sharper degree-four conclusion.  In either surviving quartic
normalization profile, every finite branch divisor has generic inertia a
transposition.  If the generic fiber of \(P\) is rational and its smooth
projective completion removes \(s\) geometric points, then
\[
\boxed{s\ge4.}
\tag{Q}
\]
Thus the three-punctured rational curve is excluded as well.
In the one-boundary \(3+1/2+2\) survivor, the two coordinate fibers
cannot both attain equality: if both are rational, at least one has at
least six punctures.

More precisely, the proof gives a general dichotomy.

> **Low-log-complexity fiber theorem.**
>
> 1. If \(A_K\simeq K[t]\), then
>    \[
>    \operatorname {Frac}(B)=\mathbf C(P,Q).
>    \tag{3}
>    \]
> 2. If \(A_K\simeq K[t,t^{-1}]\), then for some
>    \(\alpha\in K^\times,\beta\in K\), and
>    \(n\in\mathbf Z\setminus\{0\}\),
>    \[
>    Q=\alpha t^n+\beta.
>    \tag{4}
>    \]
>    Consequently
>    \[
>    \operatorname {Frac}(B)/\mathbf C(P,Q)
>    \tag{5}
>    \]
>    is a cyclic Galois extension of degree \(|n|\).
> 3. A Darboux map from this pseudoplane has neither degree one nor a
>    nontrivial Galois function-field extension.  Hence both alternatives
>    are impossible.

Thus any hypothetical Darboux pair must have genuinely nontrivial generic
fiber geometry.  In particular, a proposed construction based on an
\(\mathbf A^1\)-fibration, a split \(\mathbf G_m\)-fibration, or a cyclic
Kummer parameter on a generic fiber is closed in every degree.

This is an exact structural restriction, not a bounded search.  It does
not resolve the remaining degree-four normalization profiles: their
retained curves lie over the branch curve, whereas (2) concerns the
generic fibers of the Darboux coordinates themselves.  It does show that
a successful quartic construction cannot simplify those generic fibers
to a rational curve with fewer than four punctures.

The implication “Galois Keller extension is trivial” is prior
literature, not a new result here.  In particular, Lemmas 2.1--2.2 of
M. Miyanishi, [*Affine pseudo-planes and affine
pseudo-coverings*](https://ems.press/content/serial-article-files/45993),
Oberwolfach Report 19/2005, pp. 1110--1111, give the unit/Picard
criterion for an étale map to be an affine pseudo-covering and the free
normalization action for a Galois pseudo-covering.  Over simply connected
\(\mathbf A^2\), that Galois pseudo-covering is trivial.  Section 2
records a direct divisor-and-purity proof in the present notation.  The
new value here is its coupling to the generic-fiber slice/Kummer
calculation and to the accepted quartic transposition profile.  A
dedicated literature audit would still be required before claiming the
combined puncture and branch-degree bounds as new.

## 1. The Hamiltonian derivation on the generic fiber

Let
\[
\delta=\{P,-\}.
\]
Because \(\delta(P)=0\), it extends to a \(K\)-derivation of \(A_K\).
Equation (1) becomes
\[
\delta(Q)=1.
\tag{6}
\]

Suppose first that \(A_K=K[t]\).  Every \(K\)-derivation of \(K[t]\)
has the form
\[
\delta=h(t)\frac d{dt},\qquad h(t)\in K[t].
\tag{7}
\]
Writing \(Q=q(t)\), equation (6) gives
\[
h(t)q'(t)=1.
\tag{8}
\]
Both factors in (8) are units of \(K[t]\), so \(q'\in K^\times\).
Therefore
\[
Q=\alpha t+\beta,\qquad
\alpha\in K^\times,\quad\beta\in K.
\tag{9}
\]
It follows that \(K(t)=K(Q)\), proving (3).

Now suppose that \(A_K=K[t,t^{-1}]\).  Again
\[
\delta=h(t)\frac d{dt},
\qquad h(t)\in K[t,t^{-1}],
\]
and (8) remains valid.  The units of the Laurent ring are exactly
\(ct^m\), with \(c\in K^\times\) and \(m\in\mathbf Z\).  Hence \(q'\)
is a Laurent monomial.  A Laurent polynomial whose derivative is one
monomial has exactly one nonconstant monomial, so
\[
q(t)=\alpha t^n+\beta,\qquad n\ne0.
\tag{10}
\]
Conversely its Hamiltonian coefficient is forced to be
\[
h(t)=\frac{t^{1-n}}{\alpha n}.
\tag{11}
\]

Since \(K\) contains all roots of unity,
\[
K(t)/K(t^n)
\]
is cyclic Galois of degree \(|n|\), with automorphisms
\(t\mapsto\zeta t\).  Equations (10)--(11) prove (4)--(5).

The argument is insensitive to the chosen coordinate on the split
torus.  It is the unit group of the generic-fiber ring, rather than a
degree bound, that forces the Kummer form.

## 2. No nontrivial Galois Darboux extension

The following argument applies more generally to any smooth affine
surface \(X=\operatorname {Spec}A\) such that
\[
A^\times=\mathbf C^\times
\tag{12}
\]
and to any étale dominant morphism
\[
F:X\longrightarrow\mathbf A^2
\tag{13}
\]
whose function-field extension is Galois.

Let \(L=\mathbf C(P,Q)\), \(E=\operatorname {Frac}(B)\), and let
\[
\pi:Y\longrightarrow\mathbf A^2
\tag{14}
\]
be the finite normalization in \(E/L\).  Zariski's Main Theorem
identifies \(S=\operatorname {Spec}B\) with an open subset of \(Y\).

Assume \(E/L\) is Galois and let \(\Delta\subset\mathbf A^2\) be an
irreducible branch divisor of \(\pi\).  All height-one primes of \(Y\)
over \(\Delta\) have the same ramification index \(e>1\).  Since
\(F:S\to\mathbf A^2\) is étale, none of their generic points lies in
\(S\).

Choose an irreducible equation \(f(X,Y)\) for \(\Delta\).  The regular
function
\[
f(P,Q)\in B
\]
then has no height-one zero on \(S\).  If it were a nonunit, some
maximal ideal would contain it; the principal ideal theorem, applied in
the smooth (in particular normal) affine surface \(S\), would then
supply a height-one prime in its zero locus.  Such a prime would lie
over \(\Delta\), contrary to the preceding paragraph.  Hence
\(f(P,Q)\) is a unit.  It is nonconstant because \(P,Q\) are
algebraically independent.  This contradicts
\(B^\times=\mathbf C^\times\).

Thus (14) is unramified over every codimension-one point of the regular
surface \(\mathbf A^2\).  Zariski--Nagata purity for a finite dominant
map from a normal surface to a regular surface says that any nonétale
locus on the target is pure of codimension one.  There is no residual
codimension-two branch locus, so \(\pi\) is finite étale.  The affine
plane has no nontrivial connected finite étale cover, so
\[
Y\simeq\mathbf A^2,\qquad E=L.
\tag{15}
\]
Therefore every Galois Darboux extension on \(S\) has degree one.

This step also explains why the result is special to the filled
pseudoplane rather than the Laurent cylinder.  The Laurent ring has
many nonconstant units, so the branch equation need not yield a
contradiction there.

## 3. Degree one is impossible

Suppose \(E=L\).  Zariski's Main Theorem makes \(F\) an open immersion
\[
S\hookrightarrow\mathbf A^2.
\tag{16}
\]
Its complement has no curve component: an equation of such a component
would restrict to a nonconstant unit of \(B\).  Hence the complement is
finite.

Normal Hartogs extension gives
\[
\Gamma(S,\mathcal O_S)
=\Gamma(\mathbf A^2,\mathcal O_{\mathbf A^2})
=\mathbf C[X,Y].
\tag{17}
\]
Because \(S\) is affine, (17) forces the open immersion (16) to be
surjective.  This would make
\[
B\simeq\mathbf C[X,Y],
\]
contrary to
\[
\operatorname {Cl}(B)\simeq\mathbf Z/2.
\tag{18}
\]
So a Darboux map on \(S\) cannot have degree one.

Combining Sections 1--3 proves (2).

## 4. Simple finite inertia forces at least \(d\) punctures

There is a complementary Riemann--Hurwitz bound that uses the finite
normalization rather than the unit group.  Let
\[
d=[\operatorname {Frac}(B):\mathbf C(P,Q)]
\]
and suppose the generic fiber \(C/K\) of \(P\) is rational.  Let
\[
\overline C\simeq\mathbf P^1_{\overline K}
\]
be its smooth geometric completion and write
\[
\overline C\setminus C=\{x_1,\ldots,x_s\}.
\tag{19}
\]
The function \(Q\) extends to a degree-\(d\) rational map
\[
q:\overline C\longrightarrow\mathbf P^1.
\tag{20}
\]

Because \(dQ\) is nonzero everywhere on \(C\), every ramification point
of (20) belongs to the set (19).  Let \(k\ge1\) be the number of those
punctures at which \(Q\) has a pole.  If their pole orders are
\(m_1,\ldots,m_k\), then
\[
\sum_{i=1}^k m_i=d
\]
and their total ramification contribution is
\[
\sum_{i=1}^k(m_i-1)=d-k.
\tag{21}
\]

Assume every ramification point of (20) with finite \(Q\)-value is
simple.  Each of the remaining \(s-k\) punctures then contributes at
most one.  Riemann--Hurwitz gives
\[
2d-2
\le (d-k)+(s-k)
=d+s-2k.
\tag{22}
\]
Therefore
\[
\boxed{s\ge d-2+2k\ge d.}
\tag{23}
\]

For either surviving degree-four Route A profile, the finite branch
curve has generic inertia a transposition.  After taking a generic
vertical target line \(P=p\), every finite ramification point in (20)
is consequently simple.  Indeed, choose \(p\) outside the finite set of
critical values of the restrictions of \(P\) to the normalizations of
the branch and boundary curves.  The line \(P=p\) then meets every
horizontal branch component at a smooth generic point and transversely.
At a ramified boundary point the restriction of the finite surface map
to that line has the same index two as the surface inertia.  At an
unramified boundary point the surface map is étale, and transversality
makes the curve restriction unramified.  Vertical boundary or branch
components do not meet the generic line.  Thus every finite
ramification index of (20) is at most two.  Unramified boundary
punctures only lower the right side of (22), so (23) proves (Q).

The equality case is rigid.  If \(d=s=4\), then (22) forces
\[
k=1,
\]
all three nonpole punctures are simply ramified, and the unique pole has
order four.  After sending that pole to \(t=\infty\), one obtains
\[
q(t)\in\overline K[t],\qquad
\deg q=4,\qquad
q'(t)=c(t-a)(t-b)(t-c)
\tag{24}
\]
with \(a,b,c\) distinct.  The affine generic fiber is exactly
\[
\mathbf P^1\setminus\{a,b,c,\infty\}.
\]
Thus the minimal rational quartic survivor is not an arbitrary
four-punctured curve: it is the complement of the three simple critical
points and the pole of a quartic polynomial.  Its finite discriminant
has degree three in \(Q\).

There is a two-coordinate consequence for the \(r=1,\delta=1\)
quartic survivor.  Its only affine boundary curve is the ramification
curve \(E\); its normalization
\(\widetilde E\simeq\mathbf A^1\) maps birationally to \(\Delta\).  If
the generic \(P\)-fiber is rational, let \(k_P\) be its number of
\(Q\)-pole punctures.  The normalization of the generic \(P\)-fiber
inside the finite surface \(Y\) is finite over the affine \(Q\)-line.
Hence every finite-valued puncture centers on \(Y\setminus S=E\), while
every point outside that affine normalization is a \(Q\)-pole.  A
generic \(P\)-line meets \(E\) transversely, and every such intersection
is simply ramified.  Hence equality, not just inequality, holds in (22):
\[
6=(4-k_P)+\deg(P|_{\widetilde E}),
\qquad
\deg(P|_{\widetilde E})=k_P+2.
\tag{25}
\]
The total puncture count is therefore
\[
s_P=k_P+\deg(P|_{\widetilde E})=2k_P+2.
\tag{26}
\]
Similarly, if the generic \(Q\)-fiber is rational,
\[
\deg(Q|_{\widetilde E})=k_Q+2.
\tag{27}
\]

In particular, the two generic fibers cannot both have the minimal
four-puncture profile.  If they did, then \(k_P=k_Q=1\), so the
normalization parametrization
\[
\widetilde E\simeq\mathbf A^1
\longrightarrow
\Delta,\qquad
t\longmapsto(P|_{\widetilde E}(t),Q|_{\widetilde E}(t))
\]
would have both coordinate degrees at most three.  Its projective image
would be a rational plane curve of degree at most three.  But the
accepted survivor profile has two distinct affine singularity
contributions: the deficient \(3+1\) unibranch collision and at least one
two-branch \(2+2\) value.  The deficient point must be singular: if its
branch germ were smooth, its small-ball complement would have cyclic
local fundamental group generated by the generic transposition, whose
orbit partition is only \(2+1+1\), never \(3+1\).  A singular
unibranch plane-curve germ has delta invariant at least one, and the
distinct two-branch value also has delta invariant at least one.  Their
total delta is therefore at least two, whereas an irreducible rational
plane curve of degree at most three has arithmetic genus at most one.
This is impossible.  Equations (26)--(27) then show that
\[
\boxed{
\begin{gathered}
\text{in the }r=1,\delta=1\text{ survivor, if both generic coordinate}\\
\text{fibers are geometrically rational, at least one has at least six
punctures.}
\end{gathered}
}
\tag{28}
\]

The same calculation gives a finite-degree target for both quartic
survivors.  If both generic coordinate fibers are geometrically
rational, then \(1\le k_P,k_Q\le4\), and the ramified boundary
normalization parametrizes \(\Delta\) with coordinate degrees
\[
k_P+2,\qquad k_Q+2.
\]
Since that parametrization is birational,
\[
\boxed{3\le\deg\overline\Delta\le6.}
\tag{29}
\]
In the \(r=1,\delta=1\) survivor, (28) improves the lower bound to
\[
\boxed{4\le\deg\overline\Delta\le6.}
\tag{30}
\]
Thus the all-rational quartic problem reduces to branch curves of only
three projective degrees.  This does not yet exclude them, but it
converts the previously unbounded infinity-tree freedom into a
degree-\(4,5,6\) classification problem in the one-boundary case.

The transposition hypothesis is essential.  The three-punctured curve
\[
C_0=\mathbf P^1\setminus\{0,1,\infty\}
\]
has the exact slice
\[
q(t)=3t^4-4t^3,\qquad
\delta=\frac1{12t^2(t-1)}\frac d{dt},\qquad
\delta q=1.
\tag{31}
\]
Its three ramification indices are
\[
e_\infty=4,\qquad e_0=3,\qquad e_1=2,
\tag{32}
\]
whose contributions \(3+2+1=6\) saturate Riemann--Hurwitz.  The branch
cycles have types \((4)\), \((3)(1)\), and \((2)(1)(1)\), and generate
\(S_4\).  Thus three punctures support an exact quartic \(S_4\) slice
as soon as higher finite inertia is allowed.  The quartic pseudoplane
exclusion comes precisely from the accepted transposition-only
normalization audit, not from rationality by itself.

## 5. Scope and next use

The theorem strictly strengthens the earlier locally-finite-flow
obstruction in one direction.  It does not assume that
\(\{P,-\}\) is locally nilpotent or locally finite.  Instead it proves
that a low-log-complexity generic fiber would itself force a birational
or cyclic Galois Darboux extension, after which units, purity, and the
class group finish the exclusion.

What remains includes:

1. in the quartic survivors, rational generic fibers with at least four
   punctures;
2. positive-genus generic fibers whose forced differential \(dQ\) has
   all its ramification at the missing points; and
3. nonsplit or non-geometrically-integral degenerations not covered by
   the explicit split-ring hypotheses in (2).

The next promising extension is to couple the lower bound (23) to the
actual number of horizontal components in the canonical completion of
the pseudoplane.  Bare Riemann--Hurwitz counts punctures but does not say
which punctures arise from the same boundary divisor.  A useful next
theorem would force a rational generic fiber to have at most three
horizontal boundary branches, contradicting (Q), or would show directly
that four horizontal branches cannot coexist with the fixed pseudoplane
arm.  In the all-rational one-boundary case, the more concrete alternative
is now to classify the degree-\(4,5,6\) polynomial parametrizations in
(30) against the required \(3+1\) unibranch and \(2+2\) multibranch
monodromy.

## Verification

Run

```bash
.venv/bin/python \
  current_context/verify_route_a_low_log_complexity_fiber_obstruction.py
```

The verifier checks the Hamiltonian slice normal forms, the Kummer
degree and cyclic action, the quartic three-puncture threshold model,
the puncture inequality, and the pseudoplane Poisson identities used in
the statement.  The unit, purity, Zariski Main, Hartogs, class-group,
and geometric generic-line steps are theorem-level arguments and are
not replaced by a bounded computation.
