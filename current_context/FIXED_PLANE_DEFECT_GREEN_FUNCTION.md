# The global defect Green function and its sharp limitation

Date: 25 July 2026

This note propagates the boundary defect
\[
\sigma=db-\eta
\]
through an arbitrary connected point-mapping subtree.  It gives a
positive Green-kernel formula and a universal conductor identity.  It
also gives an exact finality-compatible local counterledger showing that
these facts do **not** force every point-mapping defect to be
nonnegative.

Thus the defect method yields a sharp necessary inequality for every
proposed cap, but the conductor self-intersection alone does not yet
produce a contradiction for every compactification tree.

## 1. Global defect equation

Retain the smooth-\(\Gamma\), reduced-pullback, coefficient-one, and
separated-contact hypotheses of
`GLOBAL_PULLBACK_INTERSECTION_SYSTEM.md`.  The two boundary systems are
\[
Qb=y,\qquad Q\eta+z=d\,y,
\]
where \(z\ge0\) is the boundary-incidence vector of the strict affine
part of \(\phi^*\overline\Gamma\).  Hence
\[
\boxed{\qquad \sigma=db-\eta,\qquad Q\sigma=z.\qquad}
\tag{1}
\]

On a dicritical curve,
\[
\begin{array}{c|c}
\text{type}&\sigma\\ \hline
1&db>0,\\
3&0.
\end{array}
\tag{2}
\]
The type-\(3\) row uses the fact that no type-\(3\) image is
\(\Gamma\), so its coefficient in \(G\) is zero.

## 2. Green function on a point-mapping component

Let \(S\) be a connected component of the boundary after all
dicritical vertices are removed.  Every \(E_i\), \(i\in S\), has
\[
P\cdot E_i=y_i=0.
\]
Since \(P^2=n>0\), the Hodge index theorem makes the intersection
matrix \(Q_S\) negative definite.  Put
\[
A_S=-Q_S.
\]
The boundary graph is a tree, so \(A_S\) is an irreducible
positive-definite \(Z\)-matrix.  It is therefore a nonsingular
\(M\)-matrix and
\[
A_S^{-1}>0
\tag{3}
\]
entrywise.

Let \(D\) denote the dicritical vertices adjacent to \(S\), and let
\(V\) be their incidence matrix with \(S\).  Restricting (1) to \(S\)
gives
\[
Q_S\sigma_S+V\sigma_D=z_S.
\]
Consequently
\[
\boxed{\qquad
\sigma_S=A_S^{-1}V\sigma_D-A_S^{-1}z_S.
\qquad}
\tag{4}
\]

This is the global point-subtree Green formula.  Its two terms have
opposite signs:

1. type-\(1\) attachments supply positive defect, while type-\(3\)
   attachments supply zero;
2. every strict affine intersection recorded by \(z_S\) pushes the
   interior defect downward.

The exact escape condition for a negative point defect is therefore
\[
\boxed{\qquad
\sigma_i<0
\quad\Longleftrightarrow\quad
(A_S^{-1}z_S)_i>
(A_S^{-1}V\sigma_D)_i.
\qquad}
\tag{4a}
\]
Any universal sign theorem must bound the Green potential of the strict
affine incidences by the Green potential supplied by the type-\(1\)
attachments.

In particular, for any exceptional cap \(T\) whose new labels are all
positive, Keller finality makes every final curve of \(T\) type \(3\).
Taking a final row of (4) recovers the weighted-attachment condition
\[
\boxed{\qquad
\sum_{p\in D}(A_T^{-1}V)_{fp}\sigma_p
=\sum_{j\in T}(A_T^{-1})_{fj}z_j\ge0.
\qquad}
\tag{5}
\]
This is the desired universal inequality for a positive-label cap.

## 3. The conductor and affine-component identities

Let \(Z\) be one strict affine component of \(G\), with boundary
incidence vector \(h_Z\).  If the strict affine components are pairwise
disjoint, then
\[
\boxed{\qquad h_Z^T\sigma=Z^2.\qquad}
\tag{6}
\]
Indeed,
\[
\begin{aligned}
h_Z^T\sigma
&=d(P\cdot Z)-\sum_i\eta_i(E_i\cdot Z)\\
&=d(e_Zd)-(G\cdot Z-Z^2)
=Z^2.
\end{aligned}
\]
Without disjointness, the right side is
\[
Z^2+\sum_{W\ne Z}W\cdot Z.
\tag{7}
\]

For the conductor, \(C^2=-q\) and its incidence vector is
\(\mathbf e_\alpha+\mathbf e_\beta\).  Thus
\[
\boxed{\qquad
\sigma_\alpha+\sigma_\beta=-q.
\qquad}
\tag{8}
\]
Equivalently, this follows immediately from
\[
b_\alpha+b_\beta=2\delta d,\qquad
\eta_\alpha+\eta_\beta=2\delta d^2+q.
\]
If \(q>0\), at least one conductor endpoint has negative defect.  If
\(q=0\), their defects are opposite or both zero.

Equation (8) is strong but not by itself contradictory.  Formula (4)
allows a negative interior defect whenever the strict affine incidence
term dominates the positive dicritical boundary term.

## 4. Exact finality-compatible counterledger

The failure of a global nonnegative-defect principle already appears in
a four-vertex blowup cluster.  Let \(E_0\) be an old boundary attachment
with augmented-canonical label \(-2\).  Perform:

1. a generic blowup on \(E_0\), creating \(E_1\) of label \(-1\);
2. a crossing blowup of \(E_0\cap E_1\), creating \(E_2\) of label
   \(-3\);
3. a generic blowup on \(E_2\), creating \(E_3\) of label \(-2\).

The new-curve graph and self-intersections are
\[
E_0-E_2-E_1,\qquad E_2-E_3,
\]
\[
E_1^2=E_2^2=-2,\qquad E_3^2=-1.
\tag{9}
\]
Only \(E_3\) is final.  Take \(d=1\) and, in the order
\((E_0,E_1,E_2,E_3)\),
\[
\begin{aligned}
b&=(2,1,2,1),\\
\sigma&=(2,-1,1,1),\\
\eta=b-\sigma&=(0,2,1,0).
\end{aligned}
\tag{10}
\]
On the three new exceptional rows,
\[
Qb=(0,0,1),\qquad
Q\sigma=(3,0,0).
\tag{11}
\]
Therefore:

- \(E_1,E_2\) are point-mapping;
- the sole final curve \(E_3\) is type \(1\), since
  \(a_3=-2b_3=-2\), and its dicritical intersection is \(1\);
- \(\eta\ge0\), the final coefficient is \(\eta_3=0\), and
  \(z=(3,0,0)\ge0\);
- all three ramification coefficients
  \(a_i-1+3b_i\) are nonnegative.

Nevertheless
\[
\boxed{\sigma_1=-1.}
\tag{12}
\]
The three units of \(z_1\) overwhelm the positive defect supplied at
the attachment and the final type-\(1\) end.  This is an exact
finality-compatible point-subtree ledger with a negative internal
defect.

The attachment row of \(E_0\) is intentionally not specified: this is a
local counterledger, not a complete compactification or a morphism.
Its purpose is precise.  It disproves any argument that uses only

\[
Q\sigma=z\ge0,\quad\text{effective ramification, and valid final types}
\]
to infer \(\sigma_i\ge0\) at every point-mapping vertex.

## 5. Consequence for the fixed-plane route

The universal part of the defect method is now exact:

1. every positive-label cap obeys the weighted inequality (5);
2. the conductor endpoints obey the negative budget (8); and
3. every disjoint strict affine component contributes its
   self-intersection through (6).

But (8) does not say that all attachment defects around a negative
endpoint are negative.  A type-\(1\) dicritical can feed sufficient
positive Green mass through the point subtree, while affine incidences
create a localized negative defect as in (12).

Therefore a global contradiction needs one more fixed-plane input,
such as:

- a bound on the Green weights from type-\(1\) dicriticals to the two
  conductor arms;
- a restriction on where the residual bridge may contribute the vector
  \(z\); or
- an ample-ramification inequality coupling \(r=a-1+3b\) to the same
  point-subtree Green kernel.

The identities, the exact four-vertex counterledger, and representative
Green matrices are checked in
`verify_fixed_plane_defect_green_function.py`.
