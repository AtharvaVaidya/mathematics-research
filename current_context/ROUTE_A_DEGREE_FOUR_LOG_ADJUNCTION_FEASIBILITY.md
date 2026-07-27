# Route A: log adjunction does not eliminate the quartic survivors

Date: 26 July 2026

## Outcome

Assume the notation and conclusions of
`ROUTE_A_DEGREE_FOUR_SURVIVOR_NORMALIZATION_PROFILE.md`.  Thus
\[
 \pi:Y\longrightarrow {\bf A}^2
\]
is the finite flat degree-four normalization of a hypothetical
étale map from
\[
 S=S(2,2,1)\subset Y,
\]
the reduced branch curve \(\Delta\) is irreducible with normalization
\({\bf A}^1\), \(E\) is its generically simply ramified boundary
prime, and
\[
 \operatorname {div}_Y(f_\Delta)=2E+D_{\rm res}.
\tag{1}
\]

The canonical divisor and adjunction impose exact restrictions, but
they do **not** contradict either remaining normalization profile.

> **Log-adjunction feasibility theorem.**
>
> 1. In the Gorenstein \(r=1,\delta=1\) survivor, \(E\) and
>    \(D=D_{\rm res}\) are Cartier and
>    \[
>    \omega_Y\simeq{\cal O}_Y(E),\qquad
>    \omega_D\simeq{\cal O}_D(-E),\qquad
>    \omega_E\simeq{\cal O}_E(-D).
>    \tag{2}
>    \]
>    If \(\eta:Z\to D\) is the normalization and
>    \({\mathfrak c}\) is its conductor divisor, then
>    \[
>    \omega_Z({\mathfrak c})
>       \simeq{\cal O}_Z(-\eta^*E).
>    \tag{3}
>    \]
>
> 2. In the no-two-branch \(r=2,\delta=0\) survivor, write
>    \[
>    D_{\rm res}=C_1+C_2.
>    \]
>    The four curves \(E,E',C_1,C_2\) are Cartier along all incidences
>    relevant here; \(E,C_1,C_2\) are pairwise disjoint.  One has
>    \[
>    \omega_{C_i}\simeq{\cal O}_{C_i},\qquad
>    \omega_E\simeq{\cal O}_E,\qquad
>    {\cal O}_{E'}(C_1+C_2)\simeq{\cal O}_{E'}.
>    \tag{4}
>    \]
>    Thus the total intersection divisor cut on \(E'\) by the two
>    residual closures must be principal.  On the normalization
>    \({\bf A}^1\) this supplies no degree obstruction.
>
> 3. Let \(n\) be the number of two-branch values and \(e\) the number
>    with odd branch-intersection multiplicity in the first survivor.
>    On the smooth projective normalization of the retained residual
>    curve, with every deleted point included in the log boundary,
>    the total log-canonical degree is
>    \[
>    \boxed{4n-1}.
>    \tag{5}
>    \]
>    In the second survivor it is
>    \[
>    \boxed{k_1+k_2-2}.
>    \tag{6}
>    \]
>    These numbers are nonnegative in every surviving case.
>
> 4. Both conclusions are sharp at the level of finite branch,
>    ramification, normalization, and adjunction data.  Explicit
>    algebraic certificates are given below:
>
>    * a cusp plus one odd two-branch value with connected residual
>      normalization \(Z\simeq{\bf G}_m\); and
>    * a unibranch cusp with two split residual affine lines and one
>      affine-line incidence curve puncturing one point on each.

These certificates are deliberately scoped.  They are not finite
global Keller maps from \(S(2,2,1)\), and they do not construct the
normal affine surface \(Y\).  They prove that finite canonical,
adjunction, ramification, parity, and intersection-divisor constraints
are mutually consistent.  Consequently a quartic exclusion must use
an additional global input coupling these curves in the specific
partial compactification of the pseudoplane, or controlling their
common place at infinity.  In the non-Gorenstein \(3+1\) alternative,
even (2)--(3) are unavailable.

## 1. The forced adjunction identities

Suppose first that the \(r=1,\delta=1\) survivor is Gorenstein.  The
different calculation gives
\[
 \omega_Y\simeq{\cal O}_Y(E),
\tag{7}
\]
so \(E\) is Cartier.  Equation (1) then makes \(D\) Cartier and gives
\[
 D\sim-2E.
\tag{8}
\]
Cartier adjunction yields
\[
\begin{aligned}
 \omega_D
 &\simeq
 (\omega_Y\otimes{\cal O}_Y(D))|_D
 \simeq{\cal O}_D(E+D)
 \simeq{\cal O}_D(-E),\\
 \omega_E
 &\simeq
 (\omega_Y\otimes{\cal O}_Y(E))|_E
 \simeq{\cal O}_E(2E).
\end{aligned}
\tag{9}
\]
Restricting (1) to \(E\) gives
\[
 {\cal O}_E(2E+D)\simeq{\cal O}_E,
\]
and hence the last line of (2).

For a reduced Gorenstein curve, normalization changes the dualizing
sheaf by the conductor:
\[
 \eta^*\omega_D\simeq\omega_Z({\mathfrak c}).
\tag{10}
\]
Pulling the first line of (9) to \(Z\) proves (3).

Now take the no-two-branch \(r=2,\delta=0\) survivor.  Its exact fiber
audit proves that \(Y\) is Gorenstein,
\[
 \omega_Y\simeq{\cal O}_Y(E),
\tag{11}
\]
and that \(Y\) is smooth along \(E'\) and the two residual closures.
There is no residual collision in this subcase, so \(E,C_1,C_2\) are
pairwise disjoint.  From
\[
 \operatorname {div}_Y(f_\Delta)=2E+C_1+C_2
\tag{12}
\]
one gets
\[
 {\cal O}_{C_i}(C_i)\simeq{\cal O}_{C_i}.
\tag{13}
\]
Adjunction and disjointness from \(E\) give
\[
 \omega_{C_i}
 \simeq{\cal O}_{C_i}(E+C_i)
 \simeq{\cal O}_{C_i}.
\]
Restricting (12) to \(E\) similarly gives
\({\cal O}_E(2E)\simeq{\cal O}_E\), which together with (11) proves
\(\omega_E\simeq{\cal O}_E\).  Finally \(E'\cap E=\varnothing\), so
restriction of (12) to \(E'\) proves
\[
 {\cal O}_{E'}(C_1+C_2)\simeq{\cal O}_{E'}.
\tag{14}
\]

Equation (14) is the strongest finite intersection statement supplied
by the principal pullback and the canonical class.  It asks for a
principal effective divisor on an affine-line normalization, not for
that divisor to vanish.

## 2. Log-canonical degrees

In the connected case of the first survivor, the smooth projective
completion \(\overline Z\) has
\[
 g(\overline Z)=e-1
\]
and two points over infinity.  Passing from \(Z\) to the retained
curve deletes
\[
 d=1+4n-2e
\tag{15}
\]
further finite points.  If \(B_Z\) is the sum of all punctures, then
\[
\begin{aligned}
\deg(K_{\overline Z}+B_Z)
 &=2(e-1)-2+(2+d)\\
 &=4n-1.
\end{aligned}
\tag{16}
\]
When \(e=0\), there are two projective rational components.  Their
canonical degrees total \(-4\), while the two infinity points and
\(1+4n\) deleted finite points give total boundary degree \(3+4n\).
The result is again \(4n-1\).

In the second survivor, the \(i\)-th retained normalization is
\[
 {\bf P}^1\setminus
 \{\infty,\ k_i\text{ finite points}\}.
\]
Its log-canonical degree is \(k_i-1\).  Summing proves (6).  Since
\(n\ge1\) and \(k_i\ge1\), neither profile violates log
nonnegativity.

## 3. Exact odd-contact certificate for the first survivor

Consider the polynomially parametrized irreducible plane curve
\[
 \nu(t)=\bigl(x(t),y(t)\bigr)
       =\bigl(t^2,t^3-t^5\bigr).
\tag{17}
\]
Its equation is
\[
 \Delta_{\rm odd}:\qquad
 y^2=x^3(1-x)^2.
\tag{18}
\]
The normalization is \({\bf A}^1_t\).  There are exactly two affine
singular values:

* \(t=0\) maps to an \(A_2\) cusp at \((0,0)\);
* \(t=1\) and \(t=-1\) map to an ordinary node at \((1,0)\).

The two node branches are transverse, so their intersection
multiplicity is one.  Thus
\[
 n=e=1.
\]
The normalized residual cover prescribed by the parity theorem is
\[
 Z:\qquad z^2=t^2-1.
\tag{19}
\]
It is smooth and connected, is branched simply at \(t=\pm1\), and is
unramified at the cusp parameter \(t=0\).  With
\[
 r=t+z
\]
one has
\[
 Z\simeq{\bf G}_m,\qquad
 t=\frac{r+r^{-1}}2,\qquad
 z=\frac{r-r^{-1}}2.
\tag{20}
\]
Moreover
\[
 \frac{dt}{z}=\frac{dr}{r},
\tag{21}
\]
so \(\omega_Z\) is explicitly trivial.

Choose the residual point \(r=i\) over the cusp to be the one absorbed
into the ramified boundary.  The two node points are \(r=1,-1\).
The divisor deleted in passing from the residual normalization to the
retained curve is therefore
\[
 {\mathfrak d}=[i]+[1]+[-1]
 =\operatorname {div}_Z\bigl((r-i)(r-1)(r+1)\bigr).
\tag{22}
\]
It is an effective principal divisor on \(Z\).  This is the
**log-puncture divisor**, not the conductor divisor in (3).

Indeed, the residual branch in the rank-three cusp factor below meets
the ramified divisor to order two, while the two node intersections
are transverse.  The rank-one cusp factor is a copy of the cuspidal
branch and has conductor exponent two at its normalization point.
Thus the separate adjunction ledger is
\[
 \eta^*E=2[i]+[1]+[-1],
 \qquad
 {\mathfrak c}=2[-i].
\tag{22a}
\]
Since \(dt/z=dr/r\), equation (3) is realized by
\[
\begin{aligned}
 {\mathfrak c}+\eta^*E
 &=2[-i]+2[i]+[1]+[-1]\\
 &=\operatorname {div}_Z
 \bigl((r+i)^2(r-i)^2(r-1)(r+1)\bigr).
\end{aligned}
\tag{22b}
\]
Thus conductor adjunction and log deletion are both satisfied, but by
different effective divisors.  The retained
normalization is
\[
 {\bf G}_m\setminus\{i,1,-1\},
\]
has Euler characteristic \(-3=1-4n\), and has log-canonical degree
\(3=4n-1\).  Thus the minimal connected survivor satisfies the
canonical and log ledgers exactly.

The local finite-flat algebras at its two singular values are also
standard and Gorenstein.  The displays below are completed local normal
forms **after independent formal coordinate changes** at the cusp and
the node.  They are not asserted to be literal restrictions of one
global polynomial cover.  At the cusp, over
\[
 R=\mathbf C[[x,y]],
\]
take
\[
 A_{\rm cusp}
 =
 R[z]/(z^3+xz-y)\ \times\ R.
\tag{23}
\]
The first factor is a smooth rank-three total space, its discriminant
is
\[
 -4x^3-27y^2,
\]
and its special fiber is \(\mathbf C[z]/(z^3)\).  Together with the
rank-one factor this is the required \(3+1\) fiber.  Pulling the
discriminant to the rank-three total space gives
\[
 -4x^3-27(z^3+xz)^2
 =-(x+3z^2)^2(4x+3z^2),
\tag{24}
\]
displaying the ramified double divisor and the residual simple
divisor.

After formal coordinates put the two node branches at \(x=0\) and
\(y=0\), and use
\[
 A_{\rm node}
 =
 R[s]/(s^2-x)\ \times\ R[q]/(q^2-y).
\tag{25}
\]
Its branch is \(xy=0\); its special fiber has two support points of
length two, and the two meridians are disjoint transpositions.  The
local labels
\[
 (12),\qquad(23),\qquad(34)
\tag{26}
\]
for the generic branch, cusp collision, and second node branch
generate \(S_4\).  Hence there is no local
permutation-generation obstruction to transitivity.  This does not
construct a representation of the global branch-complement group:
relations at infinity and the gluing of the completed local factors
remain unchecked.

## 4. Exact extra-boundary incidence certificate

For the no-two-branch survivor take the cuspidal branch
\[
 \Delta_0:\quad y^2=x^3,\qquad
 (x,y)=(t^2,t^3),
\tag{27}
\]
and the affine line
\[
 \Gamma:\quad x=1.
\tag{28}
\]
The curve \(\Delta_0\) is irreducible, unibranch, singular, and has
normalization \({\bf A}^1_t\).  The line \(\Gamma\simeq{\bf A}^1_y\)
meets it transversely at exactly
\[
 (1,1),\qquad(1,-1),
\tag{29}
\]
corresponding to \(t=1,-1\).  On \(\Gamma\), the full intersection
divisor is
\[
 [(1,1)]+[(1,-1)]
 =
 \operatorname {div}_\Gamma(y^2-1).
\tag{30}
\]

Let the normalized residual cover be the split cover
\[
 Z_1\amalg Z_2
 ={\bf A}^1_t\amalg{\bf A}^1_t.
\tag{31}
\]
Allocate the point \(t=1\) to the intersection of \(E'\) with the
first residual closure and \(t=-1\) to its intersection with the
second.  Then
\[
 k_1=k_2=1,
\]
both retained normalizations are \({\bf G}_m\), and their total
log-canonical degree is zero, as required by (6).  Equation (30)
is exactly the principal-intersection condition (14).

The unibranch branch singularity itself has the finite-flat local
model
\[
 A_0
 =
 R[s]/(s^2-(y^2-x^3))\ \times\ R\ \times\ R.
\tag{32}
\]
The rank-two factor is the normal \(A_2\) surface singularity
\[
 (s-y)(s+y)=-x^3;
\]
it is Gorenstein, is generically simply ramified along \(\Delta_0\),
and has fiber partition \(2+1+1\) at the cusp.  At either point (29),
the two rank-one factors are étale copies of the target.  A germ of
\(\Gamma\) in the chosen rank-one factor gives an unramified boundary
germ meeting the corresponding residual closure and remaining
disjoint from the ramified factor.  Thus both incidences in (30) have
exact smooth local surface models.

This does not glue the two rank-one germs into the boundary of a
global Keller normalization.  It proves the narrower and necessary
point: no finite log-adjunction, ramification, intersection-parity, or
principal-divisor calculation distinguishes this configuration from
an allowed one.

## 5. Consequence for the next Route A step

The canonical class produces useful identities, but all of them live
in Picard groups of affine curves whose missing points absorb the
degree.  In the smallest connected first-survivor profile the relevant
normalization is the factorial curve \({\bf G}_m\); in the smallest
second-survivor profile it is a pair of factorial affine lines and the
intersection divisor on \(E'\) is explicitly principal.

Therefore a successful continuation cannot use only:

1. \(K_Y\sim E\);
2. Cartier adjunction on \(E,E',D,C_i\);
3. parity and Riemann--Hurwitz for the residual cover;
4. the principal divisor \(2E+D_{\rm res}\); or
5. finite intersection multiplicities with \(E'\).

It must add a global coupling not present in these certificates.  The
most precise remaining possibilities are:

* control of the unique projective end of each boundary normalization
  in one canonical completion of \(S(2,2,1)\);
* a restriction on the image of
  \(\operatorname {Pic}(Y)\to\operatorname {Pic}(E')\), stronger than
  the principal restriction (14); or
* a Keller-specific monodromy theorem forcing the two local
  \(E'\)-incidences to lie on the same residual section.

The companion verifier is
`verify_route_a_degree_four_log_adjunction_feasibility.py`.
