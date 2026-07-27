# Route A: projective intersection does not bound the residual polynomial

Date: 25 July 2026

## Outcome

Continue with the hypothetical etale cubic map
\[
 F=(P,Q):S\longrightarrow{\bf A}^2,
\qquad
 S=\operatorname {Spec}
 {\bf C}[u,v,w]/(w^2-u-u^2v),
\tag{1}
\]
and its finite cubic normalization
\[
 \pi:Y\longrightarrow{\bf A}^2.
\]
Let
\[
 D=V(u,w)\simeq{\bf A}^1_v,\qquad
 \nu_D(v)=\bigl(A(v),B(v)\bigr)=F|_D(v)
\tag{2}
\]
be the normalization of
\(\Gamma=\overline{F(D)}\).  Let \(\Delta(X,Y)\) be a polynomial
equation of the cubic discriminant curve, chosen with its generic
branch multiplicity one, and put
\[
 M=\max(\deg A,\deg B),\qquad
 \delta=\deg\Delta.
\tag{3}
\]
The residual splitting gives
\[
 {\cal A}_D\simeq{\bf C}[v]\times
 {\bf C}[v,\tau]/(\tau^2-g(v)),
\qquad
 \Delta(A(v),B(v))=c\,g(v),
\quad c\in{\bf C}^{\times}.
\tag{4}
\]

The exact projective calculation is
\[
 \boxed{
 \deg\overline\Gamma=M,\qquad
 \overline\Gamma\cdot\overline\Delta=M\delta,
 \qquad
 \deg g+I_\infty=M\delta,
 }
\tag{5}
\]
where
\[
 I_\infty
 =
 I_{\overline\nu_D(\infty)}
   (\overline\Gamma,\overline\Delta)
 \ge0
\tag{6}
\]
is the intersection multiplicity carried by the unique projective end
of the normalized polynomial curve.  Thus Bezout gives precisely
\[
 \deg g\le M\delta
\tag{7}
\]
and no stronger bound.

The finite degree-six normalization makes clear why its boundary
divisor classes do not improve (7).  If
\[
 \widetilde Y\longrightarrow Y\longrightarrow{\bf A}^2
\tag{8}
\]
is obtained by adjoining \(\sqrt u\), then the source plane is the
open complement of
\[
 D_-\cup p^{-1}(R),\qquad R=Y\setminus S.
\tag{9}
\]
The map \(D\to\Gamma\) is finite: it is the normalization of the
affine curve \(\Gamma\).  Hence \(D\subset Y\), and its finite lifts
\(D_\pm\subset\widetilde Y\), are closed.  The distinguished divisor
\(D_-\) and the ramified cubic boundary \(p^{-1}(R)\) are therefore
disjoint closed subsets in the affine normalization.  At a finite
intersection \(q\in\Gamma\cap\Delta\), the point of \(D_-\) meets the
**retained unramified pullback** of \(\Delta\); the ramified residual
point is a different point over \(q\).  Consequently
\[
 \boxed{
 \sum_{x\in D_-}
 I_x\bigl(D_-,p^*C_\Delta\bigr)=\deg g,
 \qquad
 D_-\cap p^{-1}(R)=\varnothing,
 }
\tag{10}
\]
where, componentwise if \(\Delta\) is reducible, \(C_\Delta\) denotes
the closure in \(Y\) of the generic retained unramified prime over
that branch component, and the sum is taken over the affine part.

There is an additional exact class-group obstruction to the proposed
argument, but it obstructs the argument rather than the hypothetical
map:
\[
 \boxed{
 \operatorname {Cl}(\widetilde Y)
 \simeq
 \bigoplus_{E\subset\widetilde Y\setminus{\bf A}^2}
 {\bf Z}[E].
 }
\tag{11}
\]
Thus \(D_-\) and every prime over \(R\) are linearly independent in
the affine divisor class group.  Any projective relation coupling
them must introduce divisors at infinity.  Those same infinity
divisors carry the free term \(I_\infty\) in (5).

Adjunction supplies no invariant missing inequality.  Blowing up a
smooth point of the projective end of \(\overline D_-\) changes
\(\overline D_-^2\) by \(-1\) and introduces a new infinity divisor,
while leaving the affine map, \(g\), \(M\), \(\delta\), and all finite
incidences unchanged.  Hence raw self-intersection or boundary
adjunction data cannot bound \(\deg g\) without an additional
canonical-minimality theorem.

Finally, two exact families show that (5)--(11) are sharp.

1. For every \(0\le r\le\delta\), a single smooth irreducible branch
   curve of degree \(\delta\) can meet a fixed polynomial line in
   exactly \(r\) finite simple points and carry the remaining
   \(\delta-r\) intersections at infinity.
2. The connected smooth Miranda cubic family realizes squarefree
   residual polynomials of arbitrary degree.  In degree \(r\), its
   branch curve has degree \(2r+2\), so (5) reads
   \[
   r+(r+2)=2r+2.
   \]

These are not Keller maps from the quadratic pseudoplane, but they
prove that Bezout, finite flatness, normality, connected cubic
monodromy, the split distinguished section, and the projective
intersection ledger do not force a bound incompatible with arbitrary
\(g\).

The proposed projective-intersection shortcut is therefore closed.
A surviving global route would have to control the **specific
infinity divisor configuration** of the pseudoplane completion, in a
canonical minimal model, strongly enough to bound \(I_\infty\) and
\(\delta\) simultaneously.  Neither the affine boundary classes nor
adjunction on a nonminimal completion does so.

## 1. Homogenization gives the exact Bezout identity

Let
\[
 A_h(V,T)=T^M A(V/T),\qquad
 B_h(V,T)=T^M B(V/T).
\]
Since at least one of \(A,B\) has degree \(M\), the triple
\[
 [V:T]\longmapsto
 [A_h(V,T):B_h(V,T):T^M]
\tag{12}
\]
has no base point.  It extends \(\nu_D\) to a morphism
\[
 \overline\nu_D:{\bf P}^1\longrightarrow{\bf P}^2.
\]
The affine normalization is birational, so (12) is generically
degree one onto \(\overline\Gamma\).  Pullback of a general line has
degree \(M\), proving
\[
 \deg\overline\Gamma=M.
\tag{13}
\]

Let \(\Delta_h(X,Y,Z)\) be the degree-\(\delta\) homogenization of
\(\Delta\).  Its pullback through (12) is a section of
\[
 {\cal O}_{{\bf P}^1}(M\delta).
\]
On \(T=1\), equation (4) identifies this section with \(c\,g(V)\).
If \(r=\deg g\), its divisor therefore consists of the finite zero
divisor of \(g\), of degree \(r\), and a zero of order
\[
 M\delta-r
\tag{14}
\]
at \(T=0\).  This proves (5)--(6) directly.  It also shows that all
leading cancellation in \(\Delta(A,B)\) has a precise geometric
meaning: it is intersection transferred to the one point at infinity.

No transversality is assumed.  Multiple roots of \(g\) are counted
with their orders, and (14) counts all infinitely-near intersection
multiplicity at the projective end.

## 2. Projection formula: the finite roots lie on the retained sheet

Let \(E_\Delta\subset R\) be a ramified cubic prime over a component
of \(\Delta\), and let \(C_\Delta\) be the closure in \(Y\) of its
generic retained unramified simple prime.  All notation in this
section is interpreted componentwise and then summed if \(\Delta\)
is reducible.  At a generic simple branch point,
\[
 \operatorname {div}_Y(\Delta)
 =
 2E_\Delta+C_\Delta
\tag{15}
\]
componentwise.  Pulling to the quadratic normalization gives
\[
 \operatorname {div}_{\widetilde Y}(\Delta)
 =
 2p^*E_\Delta+p^*C_\Delta.
\tag{16}
\]

The distinguished divisor \(D_-\) lies over \(D\subset S\), whereas
\(p^*E_\Delta\) lies over \(R=Y\setminus S\).  Hence
\[
 D_-\cap p^*E_\Delta=\varnothing
\tag{17}
\]
on the affine normalization.  At a root \(v_0\) of \(g\), the point
on \(D_-\) maps to the retained point of the cubic fiber.  Because
the degree-six finite map is etale there,
\[
 I_{d_-(v_0)}
 \bigl(D_-,p^*C_\Delta\bigr)
 =
 \operatorname {ord}_{v_0}
 \Delta(A(v),B(v))
 =
 \operatorname {ord}_{v_0}g.
\tag{18}
\]
Summation proves (10).

On a projective finite normalization
\[
 \overline f:\overline{\widetilde Y}\longrightarrow{\bf P}^2,
\]
the projection formula gives
\[
 \overline D_-\cdot
 \overline f^{\,*}\overline\Delta
 =
 \overline f_*\overline D_-\cdot\overline\Delta
 =
 \overline\Gamma\cdot\overline\Delta
 =
 M\delta.
\tag{19}
\]
Equations (17)--(18) allocate \(\deg g\) of this intersection to the
retained pullback in the affine part.  Equation (14) allocates the
remainder to infinity.  The ramified cubic boundary contributes no
finite intersection with \(D_-\).

This is the precise point at which the hoped-for argument reverses
direction: projective intersection theory sees the retained sheet
through \(D_-\), not the separated ramified sheet that supplies the
non-distinguished dicritical classes.

## 3. The affine boundary lattice is free

The variety \(\widetilde Y\) is normal and affine, finite over the
target plane.  Its plane source
\[
 U={\bf A}^2_{a,b}\subset\widetilde Y
\]
is a dense open set.  Every unit on \(\widetilde Y\) restricts to a
unit on \(U\), so
\[
 {\cal O}(\widetilde Y)^\times
 \subset
 {\cal O}(U)^\times={\bf C}^\times.
\]
Constants give equality.

Let \(E_1,\ldots,E_N\) be the codimension-one components of
\(\widetilde Y\setminus U\).  The localization sequence for a normal
variety is
\[
 {\cal O}(\widetilde Y)^\times
 \longrightarrow{\cal O}(U)^\times
 \longrightarrow\bigoplus_{j=1}^N{\bf Z}[E_j]
 \longrightarrow\operatorname {Cl}(\widetilde Y)
 \longrightarrow\operatorname {Cl}(U)
 \longrightarrow0.
\tag{20}
\]
The first arrow is an isomorphism and
\(\operatorname {Cl}(U)=0\).  Therefore the middle divisor map is an
isomorphism, proving (11).

In particular, there is no affine class relation of the form
\[
 n[D_-]=\sum_jm_j[E_j]
\tag{21}
\]
with \(E_j\subset p^{-1}(R)\), unless every coefficient is zero.
The principal divisor (16) does not contradict this: its retained
term \(p^*C_\Delta\) is not a boundary divisor and supplies the
opposite class.

After projective completion, relations can and do appear, but they
must use the new divisors over the target line at infinity.  Forgetting
those divisors discards exactly the degrees of freedom in (14).

## 4. The invariant-ring degree estimate is redundant

Let
\[
 H=(H_1,H_2)=F\circ\pi_2,\qquad
 d_i=\deg H_i,\qquad
 m_i=\deg H_i(0,b).
\]
Then \(m_i=\deg A_i\) in (2), and hence
\[
 M=\max(m_1,m_2).
\tag{22}
\]
The sharp invariant-ring filtration gives
\[
 d_i\ge4m_i,\qquad
 D_H:=\max(d_1,d_2)\ge4M.
\tag{23}
\]

On one hand, restriction of
\(\Delta(H_1,H_2)\) to \(a=0\) has degree \(\deg g\), so the same
filtration gives
\[
 \deg\Delta(H_1,H_2)\ge4\deg g.
\tag{24}
\]
On the other hand, ordinary composition gives
\[
 \deg\Delta(H_1,H_2)\le\delta D_H.
\tag{25}
\]
But (5) and (23) already imply
\[
 4\deg g
\le4M\delta
\le\delta D_H.
\tag{26}
\]
Thus (24)--(25) add no new inequality.  Equality or leading-term
cancellation merely changes \(I_\infty\) in (14).

## 5. Adjunction depends on a noncanonical infinity model

Choose any smooth projective completion \(X\) resolving the rational
extension of the finite map, and let \(\widehat D_-\) be the strict
transform of \(D_-\).  The curve \(D_-\simeq{\bf A}^1\), so its
normalization has a single projective end.

Blow up a smooth point of \(\widehat D_-\) over that end.  If
\(\widehat D_-'\) is the new strict transform, then
\[
 (\widehat D_-')^2=\widehat D_-^2-1.
\tag{27}
\]
This operation changes no affine datum: \(F\), \(H\), \(g\), \(M\),
\(\delta\), and the finite intersection ledger (18) are identical.
Adjunction remains an equality because the exceptional divisor changes
the canonical and boundary terms at the same time.

Repeating the blowup makes the raw self-intersection arbitrarily
negative.  Therefore no inequality involving only
\[
 \widehat D_-^2,\qquad
 K_X\cdot\widehat D_-,
\qquad
 \widehat D_-\cdot(X\setminus{\bf A}^2)
\]
is an invariant bound on \(\deg g\) until a canonical minimal
completion and its allowed contractions have been specified.  The
present Route A package supplies no such minimality theorem.

## 6. Exact branch curves with arbitrary finite intersection

Fix integers
\[
 \delta\ge2,\qquad 0\le r\le\delta.
\]
Take
\[
 \Gamma=V(y)
\]
and, for \(r\ge1\),
\[
 \Delta_{\delta,r}:
 \quad
 yx^{\delta-1}-(x^r+1)=0.
\tag{28}
\]
For \(r=0\), replace \(x^r+1\) by the nonzero constant \(2\).
The polynomial in (28) is irreducible because it is primitive and
linear in \(y\), with coprime \(y\)-coefficient and constant term.  It
is smooth: its \(y\)-derivative is \(x^{\delta-1}\), while \(x=0\)
does not lie on the curve.

The finite affine intersections with \(\Gamma\) are the \(r\) simple
roots of
\[
 x^r+1.
\]
Homogenization gives
\[
 YX^{\delta-1}
 -X^rZ^{\delta-r}
 -Z^\delta=0,
\tag{29}
\]
whose restriction to \(\overline\Gamma=V(Y)\) is
\[
 -Z^{\delta-r}(X^r+Z^r).
\tag{30}
\]
Thus
\[
 \deg g=r,\qquad I_\infty=\delta-r,
\qquad r+(\delta-r)=\delta,
\tag{31}
\]
which realizes every allocation allowed by (5) when \(M=1\).

The corresponding simple cubic local package is the finite flat
rank-three algebra
\[
 {\bf C}[x,y]\times
 {\bf C}[x,y,z]/(z^2-\Delta_{\delta,r}(x,y)).
\tag{32}
\]
Its distinguished factor is etale everywhere.  The second factor is
smooth and ramifies along the one divisor \(z=0\), which maps
isomorphically to the one smooth curve \(\Delta_{\delta,r}\).  Along
\(\Gamma\), its residual equation has exactly the \(r\) odd places
in (31), all on that same ramification divisor.

This is the exact semilocal normal form relevant to the retained versus
ramified cubic points.  Algebra (32) is disconnected globally and is
not asserted to be the hypothetical cubic normalization.

## 7. Connected smooth cubic countermodels

Connectedness of the generic cubic does not restore a Bezout bound.
For any squarefree polynomial \(G(x)\) of degree \(r\ge1\), the
Miranda algebra with coefficients
\[
 a=1,\qquad b=y,\qquad c=-G/3,\qquad d=0
\]
is finite flat of rank three, connected, and has smooth total space.
Along \(\Gamma=V(y)\) it splits as
\[
 {\bf C}[x]\times
 {\bf C}[x,\tau]/(\tau^2-G(x)).
\tag{33}
\]
Its branch polynomial is
\[
 {\cal D}
 =\frac{G(x)}9\bigl(y^2G(x)-12\bigr).
\tag{34}
\]
Therefore
\[
 \delta=2r+2,\qquad
 \deg {\cal D}(x,0)=r,\qquad
 I_\infty=r+2.
\tag{35}
\]
All three quantities are unbounded and satisfy (5) identically.

This family does not have the quadratic pseudoplane as its etale open.
It proves the narrower, exact negative statement needed here:
normality, connected cubic monodromy, finite flatness, smooth total
space, the global split section, and projective Bezout do not constrain
\(\deg g\) beyond (5).

## 8. Exact conclusion

The projective ledger is now complete:
\[
\boxed{
\begin{aligned}
\deg g
&=\text{finite intersection of }D_-
  \text{ with the retained branch pullback},\\
I_\infty
&=\text{the remaining intersection at the unique projective end},\\
D_-\cap p^{-1}(R)
&=\varnothing\quad\text{in the affine normalization},\\
\operatorname {Cl}(\widetilde Y)
&=\text{the free lattice on all affine boundary primes}.
\end{aligned}}
\tag{36}
\]

There is consequently no projective-intersection contradiction from
the presently known divisor classes.  A new theorem would have to
select and control a minimal completion and then couple:

1. the infinity multiplicity \(I_\infty\);
2. the discriminant degree \(\delta\);
3. the ramification coefficients of primes over \(R\); and
4. the canonical/self-intersection labels of the unique end of
   \(D_-\).

Without that additional theorem, Bezout, adjunction, and the affine
boundary lattice are identities with free infinity corrections.

## Verification

Run

```sh
.venv/bin/python current_context/verify_route_a_projective_intersection_bound_no_go.py
```

for homogenization and intersection allocation in (28)--(31), the
smooth irreducible branch curves, residual discriminants, local
ramification Jacobians, the invariant-degree inequality chain, and
the connected Miranda degree ledger (33)--(35).
