# Residual coexceptional entry into the two conductor arms

Date: 25 July 2026

This note continues Sections 1.15--1.16 of
`FIXED_SOURCE_PLANE_ROUTE.md`.  Assume that the conductor image
\(\Gamma\) is smooth.  For a reduced equation \(F\) of \(\Gamma\), write
\[
F(U,V)=D\prod_i H_i.
\]
The residual-oddness theorem gives
\[
H_i|_C=\lambda_i v^{m_i},\qquad
\sum_i m_i\equiv-1\pmod {2\delta}.
\tag{1}
\]
In particular some \(m_i\) is odd.  Fix such an irreducible residual
component \(H_i=0\), of degree \(d_i\).  Its total local intersections
with the conductor closure at the two marked ends are
\[
I_0=2d_i+m_i,\qquad I_\infty=2d_i-m_i.
\tag{2}
\]
They are both positive odd integers.  If \(H_i\) has several local
branches at an end, at least one branch has odd intersection with the
conductor branch.

## 1. The robust entry theorem

Intersection parity determines how far such a local branch must follow
the cusp, although it does not determine its exit vertex.

At \(P_0\), the conductor has characteristic pair \((2,5)\).  Along its
successive infinitely-near centers its multiplicities begin
\[
2,\ 2,\ 1,\ldots.
\]
Noether's intersection formula says that a branch separating before the
third center has even intersection with the conductor: every common
contribution is a multiple of \(2\).  Therefore a branch with odd
intersection must reach the third blowup center.  After that blowup it
either

1. exits on \(E_3\), or
2. follows the conductor through the triple-point blowup to \(E_4\) and
   possibly through further descendants of \(E_4\).

At \(P_\infty\), the characteristic pair is \((2,3)\), and the
multiplicity sequence begins
\[
2,\ 1,\ldots.
\]
Odd intersection forces the branch to reach the second blowup center.
It therefore either

1. exits on \(F_2\), or
2. follows the conductor through the triple-point blowup to \(F_3\) and
   possibly through further descendants of \(F_3\).

Thus one irreducible residual component is a projective bridge whose
normalization has a branch entering at least as far as \(E_3\) on the
\((2,5)\) arm and a branch entering at least as far as \(F_2\) on the
\((2,3)\) arm.

The qualification about exit vertices is essential.  The single number
\(I(C,H_i)\) does not determine the infinitely-near path because
Noether's sum also contains the multiplicities of the residual branch.
For example, a multiplicity-two residual branch can acquire odd total
intersection while exiting earlier than a smooth branch with the same
intersection number.  Any inference assigning \(E_4\) or \(F_3\) from
oddness alone would be false.

## 2. Exact sharp model

The smallest odd residual factor already present in the fixed-source
ring is
\[
H_0=3ct-2=v,\qquad
DH_0=9bc-27ac^2-8.
\tag{3}
\]
At \(P_0\), with local coordinates \(x=Z,\ y=3C-2Z^2\), its
homogenization is \(y=0\).  Its contact with the \((2,5)\) conductor is
exactly \(5\).  Under the first two blowups the strict equations are
\[
y=0\longmapsto u=0\longmapsto w=0.
\]
At the third center the conductor and \(H_0\) have different tangent
directions, so \(H_0\) exits on \(E_3\).  The fourth blowup creating
\(E_4\) does not contain its strict transform.

At \(P_\infty\), with \(x=Z,\ y=T\), the homogenized factor is
\[
3y-2x^2=0.
\]
Its conductor contact is exactly \(3\).  After the first blowup its
strict transform is \(3u-2x=0\), transverse to the conductor.  The
second blowup separates them, and \(H_0\) exits at a generic point of
\(F_2\); it does not pass through the third center creating \(F_3\).

Thus the minimal bridge has the exact boundary incidence
\[
E_3\ \longleftarrow\ \overline{H_0}\ \longrightarrow\ F_2.
\tag{4}
\]
This realizes the entry theorem sharply inside the actual ring, so the
entry statement itself cannot be upgraded to a contradiction.

## 3. Degree and log-canonical constraints

For the total residual factor \(H=\prod_iH_i\), of degree \(d\), let
\[
I_0=I_{P_0}(\overline C,\overline H),\qquad
I_\infty=I_{P_\infty}(\overline C,\overline H).
\]
The conormal-unit calculation in Section 1.15 gives
\[
I_0+I_\infty=4d,\qquad
I_0-I_\infty=2m\equiv-2\pmod {4\delta},
\tag{5}
\]
up to swapping the two ends.  Equivalently,
\[
m=2\delta\ell-1,\qquad -2d<m<2d.
\tag{6}
\]
For fixed \(d\) and conductor-cover degree \(2\delta\), (6) is a finite
list of possible total attachment pairs.  It is not a uniform degree
bound: \(d\) remains unrestricted.

The augmented-canonical labels on the forced entry vertices are
\[
\overline K(E_3)=1,\quad \overline K(E_4)=1,\qquad
\overline K(F_2)=0,\quad \overline K(F_3)=-1.
\tag{7}
\]
If a branch follows beyond the bare cusp resolution, generic blowups
along the common conductor/residual point create labels
\[
2,3,\ldots\quad\text{after }E_4,
\qquad
0,1,2,\ldots\quad\text{after }F_3.
\tag{8}
\]
These labels do not determine Borisov type.  Since
\(\Gamma\not\subset S_e\), no type-\(3\) divisor can have image
\(\Gamma\); the conductor and residual ends may be absorbed by type-\(2\)
vertices mapping to the relevant point of the target line at infinity.
Positive-label type-\(3\) branches may still leave the marked subtree,
but their images are the independently forced components
\(\Lambda\ne\Gamma\) of \(S_e\).

The ample-ramification theorem and the rule that final boundary
components are type \(1\) or \(3\) require further branches in a complete
Keller resolution.  They do not prohibit the local pattern (4):
\(E_3\) and \(F_2\) are not final in the bare cusp ancestry, and the
connected type-\(2\) subtree can be supplied with positive-label
type-\(3\) children exactly as in the compatibility skeleton of Section
1.14.  Neither the divisorial pullback multiplicities nor the
ramification indices of those children are determined by (1)--(8).

Consequently the strongest remaining finite problem is to solve the
full intersection system on a resolved compactification with:

1. a type-\(2\) path containing the forced \(E_3/F_2\) entries (or their
   deeper descendants),
2. type-\(3\) branches whose images are one-place curves
   \(\Lambda\ne\Gamma\),
3. an ample divisor \(\sum r_jE_j\) supported on those type-\(3\)
   branches, and
4. the pullback congruence (5).

Bare labels and local cusp multiplicities admit this configuration.  A
contradiction, if present, must use the global pullback and intersection
equations on the Stein compactification; it cannot be obtained by
assigning map types from the two cusp chains alone.

The two exact blowup-chart exits and the congruence arithmetic are
checked in `verify_fixed_plane_residual_arm_entry.py`.
