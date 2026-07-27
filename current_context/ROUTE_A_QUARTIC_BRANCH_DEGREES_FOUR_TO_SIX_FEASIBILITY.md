# Route A: branch degrees four through six survive finite geometry

Date: 26 July 2026

> **Subsequent global update.**  The three explicit curves below pass
> the finite singularity and puncture ledgers, but they do not pass
> global braid monodromy.  In each case the local group of the
> full-degree \((3,2)\) cusp surjects onto the affine complement group;
> its transposition image is contained in a nontransitive
> \(S_3\subset S_4\).  Thus none admits the required connected quartic
> transposition representation.  No computation of the full complement
> group is claimed.  See
> `ROUTE_A_TRIGONAL_CUSP_GLOBAL_MONODROMY_OBSTRUCTION.md`.

## Outcome

Assume the all-rational, one-boundary degree-four Route A profile isolated
in `ROUTE_A_LOW_LOG_COMPLEXITY_FIBER_OBSTRUCTION.md`.  The normalization
of the branch curve is \(\mathbf A^1\), and its two coordinate degrees
must be
\[
\deg p=k_P+2,\qquad
\deg q=k_Q+2,\qquad
1\le k_P,k_Q\le4.
\tag{1}
\]
The preceding genus argument removes projective branch degree three,
leaving
\[
D=4,\ 5,\ 6.
\]

None of these three degrees is excluded by polynomial parametrization,
genus, delta invariants, one-place-at-infinity geometry, or the required
local permutation types.

> **Degree-\(4,5,6\) feasibility theorem.**  The polynomial maps
> \[
> \begin{aligned}
> \gamma_4(t)&=(t^3,\ t^4+t^2),\\
> \gamma_5(t)&=(t^3,\ t^5+t^4+t^2),\\
> \gamma_6(t)&=(t^3,\ t^6+t^5+t^4+t^2)
> \end{aligned}
> \tag{2}
> \]
> are finite birational normalizations of irreducible affine plane
> curves \(\Delta_D\) of projective degree \(D\), each with one place at
> infinity.  Their singularity ledgers are
> \[
> \begin{array}{c|c|c|c|c}
> D&\text{affine cusp}&\text{ordinary affine nodes}
>   &\delta_\infty& p_a(\overline\Delta_D)\\ \hline
> 4&A_2&2&0&3\\
> 5&A_2&3&2&6\\
> 6&A_2&3&6&10.
> \end{array}
> \tag{3}
> \]
> The cusp and every node have distinct target values.
>
> At the cusp, two transposition meridians can be labeled
> \[
> (12),\ (23),
> \]
> giving orbit partition \(3+1\).  At every node the two commuting
> meridians can be labeled
> \[
> (12),\ (34),
> \]
> giving orbit partition \(2+2\).  These transpositions coexist in
> \(S_4\), and \((12),(23),(34)\) generate \(S_4\).

The coordinate degrees in (2) give
\[
(k_P,k_Q)=(1,D-2),
\tag{4}
\]
so the corresponding rational-fiber puncture counts forced by the
one-boundary Riemann--Hurwitz identity are
\[
(s_P,s_Q)=(4,2D-2).
\tag{5}
\]
Thus all three certificates meet the new puncture and pole-degree
bounds exactly.

This is a no-go result for the proposed finite-geometric classification,
not a construction of the hypothetical normalization.  The local
permutation labels in (3) do **not** prove that
\[
\pi_1(\mathbf A^2\setminus\Delta_D)\twoheadrightarrow S_4
\tag{6}
\]
with all smooth meridians sent to transpositions.  Nor do they construct a
normal finite flat surface \(Y\), embed the pseudoplane as
\(S\subset Y\), or satisfy the Keller condition.  Consequently the next
meaningful test is global braid monodromy, not coefficient elimination in
(2).

## 1. Birationality and the unique affine cusp

Write
\[
p=t^3
\]
and let \(q_D\) be the second component in (2).  If
\(\gamma_D(t)=\gamma_D(s)\), then either \(s=t\) or
\[
s=\zeta t,\qquad \zeta^2+\zeta+1=0.
\tag{7}
\]
For every \(D\), the difference \(q_D(t)-q_D(\zeta t)\) is not
identically zero.  Hence only finitely many pairs with \(s\ne t\) are
identified, proving generic injectivity and therefore birationality.

The derivative \(p'=3t^2\) vanishes only at \(t=0\), where \(q_D'\)
also vanishes.  Since
\[
(p,q_D)=(t^3,t^2+\text{higher terms}),
\]
the image has an ordinary \(A_2\) cusp at the origin, with
\[
\delta_0=1.
\tag{8}
\]
Away from \(t=0\), the normalization map is immersive.

## 2. Exact self-intersection equations

For \(D=4\),
\[
\frac{q_4(t)-q_4(\zeta t)}
     {(1-\zeta)t^2}
=t^2+\zeta+1.
\tag{9}
\]
This quadratic has two distinct nonzero roots.  It never vanishes
simultaneously with the corresponding equation for \(\zeta^2\), so
there is no triple self-intersection.

For both \(D=5\) and \(D=6\), the invariant \(t^6\) term in the latter
does not affect the difference, and
\[
\frac{q_D(t)-q_D(\zeta t)}
     {(1-\zeta)t^2}
=(\zeta+1)(t^3+1)+t^2.
\tag{10}
\]
This cubic has three distinct nonzero roots.  The equation obtained by
replacing \(\zeta\) by \(\zeta^2\) has no common root with (10), so no
three normalization parameters have the same image.

For the explicit coefficients in (2), the exact resultants over
\(\mathbf Q(\zeta)\) are
\[
\begin{array}{c|c|c}
D&
\operatorname {Res}_t(H_D,H_D')&
\operatorname {Res}_t(H_D,T_D)\\ \hline
4&4(\zeta+1)&108\\
5,6&-23\zeta&-1863(2\zeta+1),
\end{array}
\tag{11}
\]
where \(H_D\) is the right side of (9) or (10), and \(T_D\) is the
determinant of the two tangent vectors at \(t\) and \(\zeta t\).
Every entry is nonzero.  Thus all self-intersections are transverse
ordinary nodes.

Different roots of \(H_D\) have different \(p=t^3\) values.  Otherwise
their ratio would be a cube root of unity and the two equations with
\(\zeta,\zeta^2\) would have a common root.  Hence the node values are
pairwise distinct and are distinct from the cusp at the origin.

This yields two nodes for \(D=4\) and three nodes for \(D=5,6\).

## 3. Implicit equations and projective degree

Eliminating \(t\) gives
\[
\begin{aligned}
F_4(x,y)
&=x^4+3x^2y+x^2-y^3,\\
F_5(x,y)
&=-x^5-4x^4-3x^3y-3x^3-3x^2y-x^2+y^3,\\
F_6(x,y)
&=x^6-2x^5-3x^4y+x^4+3x^3y+3x^3\\
&\qquad+3x^2y^2+3x^2y+x^2-y^3.
\end{aligned}
\tag{12}
\]
These are the exact resultants
\[
F_D(x,y)=\operatorname {Res}_t(t^3-x,q_D(t)-y).
\tag{13}
\]
Birationality makes each \(F_D\) irreducible, and its displayed total
degree is \(D\).

The homogeneous parametrization has exactly one point above the line at
infinity, namely \(t=\infty\).

## 4. Infinity semigroups and the complete delta ledger

Put \(s=t^{-1}\) and work in the target chart where the homogenization of
\(q_D\) is nonzero.

For \(D=4\), local coordinates have orders
\[
(1,4),
\]
so the point at infinity is smooth.

For \(D=5\), local coordinates can be chosen with initial orders
\[
(2,5).
\]
This is the one-Puiseux-pair branch with
\[
\delta_\infty=\frac{(2-1)(5-1)}2=2.
\tag{14}
\]

For \(D=6\), the two raw coordinate orders are \(3,6\), but if they are
denoted by \(Y,X\), then
\[
\operatorname {ord}_s(X-Y^2)=7.
\]
The characteristic value pair is therefore
\[
(3,7),
\qquad
\delta_\infty=\frac{(3-1)(7-1)}2=6.
\tag{15}
\]

The arithmetic genera are
\[
p_a(D)=\frac{(D-1)(D-2)}2=3,6,10.
\tag{16}
\]
The cusp, nodes, and infinity contributions in (3) sum to these values:
\[
\begin{aligned}
3&=1+2,\\
6&=1+3+2,\\
10&=1+3+6.
\end{aligned}
\tag{17}
\]
Since Section 2 classified every affine failure of injectivity or
immersion, equations (16)--(17) also certify that there are no hidden
singularities.

## 5. What the local monodromy does and does not prove

An \(A_2\) cusp has two meridians satisfying the braid relation.  The
transpositions
\[
a=(12),\qquad b=(23)
\]
satisfy that relation and generate an \(S_3\) orbit plus a fixed fourth
sheet.  This is exactly the local \(3+1\) collision.

At an ordinary node, the two branch meridians commute.  Taking
\[
a=(12),\qquad c=(34)
\]
gives two disjoint length-two orbits, exactly the \(2+2\) collision.
Finally \(a,b,c\) generate \(S_4\).  Hence the singularities in (2) pass
the same local permutation test as the accepted quartic survivor.

But local label compatibility is weaker than a global meridian
representation (6).  Establishing or excluding (6) requires a
Zariski--van Kampen presentation or an exact braid factorization for
each \(\Delta_D\).  Even a successful representation would still have
to be lifted to the specific finite normalization containing
\(S(2,2,1)\).

There is a tempting parity shortcut, but it applies to the wrong
complement unless one first controls ramification at infinity.  For an
irreducible projective plane curve of degree \(D\),
\[
H_1(\mathbf P^2\setminus\overline\Delta_D,\mathbf Z)
\simeq\mathbf Z/D,
\]
so a representation taking a smooth meridian to a transposition can
exist only when \(D\) is even: composition with the sign character
would otherwise send the generator of \(\mathbf Z/D\) nontrivially to
\(\mathbf Z/2\).  Route A, however, starts from the finite cover over
\(\mathbf A^2\), hence from
\[
\mathbf A^2\setminus\Delta_D
=\mathbf P^2\setminus
  \bigl(\overline\Delta_D\cup L_\infty\bigr).
\]
Its abelianized meridians satisfy
\[
D\mu_\Delta+\mu_\infty=0,
\]
and therefore \(H_1(\mathbf A^2\setminus\Delta_D,\mathbf Z)\simeq
\mathbf Z\), generated by \(\mu_\Delta\).  There is no parity
obstruction to sending \(\mu_\Delta\) to a transposition; for odd
\(D\), the relation simply forces odd sign around \(L_\infty\).
Consequently degree five would be eliminated only after proving that
the normalization cover extends across \(L_\infty\) with trivial
inertia.  No such extension is part of the present Route A hypotheses,
and polynomial compactifications generally acquire boundary
ramification.

Thus the finite curve classification has reached its exact limit:
degrees \(4,5,6\) are all feasible, and global braid monodromy is the
next non-brute-force invariant.

## Verification

Run

```bash
.venv/bin/python \
  current_context/verify_route_a_quartic_branch_degrees_four_to_six_feasibility.py
```

The verifier checks the implicit resultants, singular-parameter
resultants, tangent determinants, absence of triple collisions, genus
and semigroup ledgers, puncture degrees, and local \(S_4\) permutation
orbits.
