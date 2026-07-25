# Route A: homogeneous Pfaff obstruction and descent audit

## Scope and conclusion

Let
\[
B=k[u,v,w]/(w^2-u-u^2v),\qquad
\operatorname{wt}(u,v,w)=(2,-2,1),
\]
over a characteristic-zero field, with
\[
\{u,v\}=-2w,\qquad \{u,w\}=-u^2,\qquad
\{v,w\}=1+2uv.
\]
The bracket raises weight by \(1\), and
\[
\mathcal E=2u\partial_u-2v\partial_v+w\partial_w.
\]

For a Darboux pair \(\{P,Q\}=1\), the polynomial Pfaff decomposition
\[
\beta=P\,dQ+dh
\]
implies
\[
\{P,h\}=-(\mathcal E+1)P,\qquad
\{Q,h\}=-\mathcal E Q. \tag{Pf}
\]

This note establishes two exact conclusions.

1. If \(h\) is homogeneous of weight \(-1\), then (Pf) has no
   Darboux pair in \(B\).
2. The tempting next claim, that arbitrary \(h\) can always be made
   weight \(-1\) by extreme-weight centralizer arguments and polynomial
   target shears, is false without an essential use of boundary
   regularity.  An explicit Laurent Darboux pair resists every
   polynomial target symplectomorphism.

Thus the first statement is a genuine all-degree theorem, while the
second prevents it from being promoted to a solution by a formal
grading descent.

## 1. Weight-zero centralizer lemma

Put \(s=uv\).  In the reduced basis
\[
u^iv^jw^\epsilon,\qquad \epsilon\in\{0,1\},
\]
the weight-zero and weight-minus-one subspaces are
\[
B_0=k[s],\qquad B_{-1}=vw\,k[s].
\]
Indeed, weight zero forces \(\epsilon=0\) and \(i=j\), while weight
\(-1\) forces \(\epsilon=1\) and \(j=i+1\).

Let
\[
h=vw\,A(s)\ne0,\qquad f=F(s).
\]
A direct bracket calculation gives
\[
\{s,vw\}=-s(1+s)
\]
and hence
\[
\boxed{\quad
\{F(s),h\}=-s(1+s)A(s)F'(s).
\quad} \tag{1}
\]
Because \(B\) is a domain and the characteristic is zero, (1) proves
\[
\operatorname{Cent}_B(h)\cap B_0=k. \tag{2}
\]

Only the weight-zero part of the centralizer is needed; no global
centralizer theorem is being assumed.

## 2. No Darboux pair when \(h\) has weight \(-1\)

Write the finite weight decompositions
\[
P=\sum_i P_i,\qquad Q=\sum_j Q_j.
\]
Since bracketing with a weight-minus-one \(h\) preserves weight, the
weight components of (Pf) are
\[
\{P_i,h\}=-(i+1)P_i,\qquad
\{Q_j,h\}=-jQ_j. \tag{3}
\]

The weight-zero component of \(\{P,Q\}=1\) is
\[
\sum_i \{P_i,Q_{-i-1}\}=1. \tag{4}
\]
For \(j=-i-1\), put
\[
R_i=\{P_i,Q_j\}.
\]
It has weight \(i+j+1=0\).  Jacobi and (3) give
\[
\begin{aligned}
\{R_i,h\}
&=\{\{P_i,Q_j\},h\}\\
&=\{\{P_i,h\},Q_j\}+\{P_i,\{Q_j,h\}\}\\
&=\bigl(-(i+1)-j\bigr)R_i=0.
\end{aligned}
\]
By (2), every \(R_i\) is a scalar.  Equation (4) says that their finite
sum is \(1\), so some \(R_i=c\ne0\).  Then
\[
\{P_i,c^{-1}Q_{-i-1}\}=1
\]
is a homogeneous Darboux pair.  This contradicts the already proved
complete homogeneous obstruction in Section 3 of `route_a/ROUTE_A_MEMO.md`.

If \(h=0\), (Pf) directly forces \(P=P_{-1}\) and \(Q=Q_0\), which is
again a forbidden homogeneous Darboux pair.  Therefore:

> **Homogeneous-Pfaff theorem.**
> No Darboux pair in \(B\) can have a Pfaff potential homogeneous of
> weight \(-1\).

The proof is degree-independent and uses only the exact homogeneous-pair
theorem, weight decomposition, Jacobi, and the elementary centralizer
identity (1).

## 3. Exact countermodel to formal shear descent

The countermodel lives on the Laurent symplectic cylinder
\[
L=k[r,r^{-1},w],\qquad \{r,w\}=1,
\]
with weights \(\operatorname{wt}(r,w)=(-2,1)\) and primitive
\[
\beta=w\,dr+2r\,dw.
\]
Set
\[
P=r^2,\qquad
Q=\frac{w}{2r}+\frac r2,\qquad
h=\frac32rw-\frac16r^3.
\]
Then, exactly,
\[
\{P,Q\}=1,\qquad
\beta=P\,dQ+dh,
\]
and
\[
\{P,h\}=-(\mathcal E+1)P,\qquad
\{Q,h\}=-\mathcal E Q.
\]
The potential has weights \(-1\) and \(-6\).

This is stronger than a one-step failure.  No polynomial canonical
change of the target coordinates can replace \(h\) by a homogeneous
weight-minus-one potential.

### 3.1 The quadratic involution

The extension
\[
\operatorname{Frac}(L)/k(P,Q)
\]
has degree two.  Its involution is
\[
\sigma(r,w)=(-r,-w-2r^2),
\]
which fixes \(P,Q\).  A calculation gives
\[
h-\sigma(h)=-\frac{10}{3}r^3. \tag{5}
\]

Every weight-minus-one Laurent polynomial has the form
\[
H=\sum_{n\ge1}c_n r^nw^{2n-1}. \tag{6}
\]
Suppose \(H-\sigma(H)\) equals the right side of (5), and take the
largest \(N\) with \(c_N\ne0\).  If \(N\) is even, the coefficient of
\(r^Nw^{2N-1}\) in \(H-\sigma(H)\) is nonzero.  If \(N>1\) is odd, that
top term cancels but the coefficient of
\(r^{N+2}w^{2N-2}\) is nonzero.  Neither can occur in (5).  Hence
\(N=1\), and coefficient comparison gives the unique candidate
\[
H_0=\frac53rw. \tag{7}
\]
Moreover,
\[
K:=h-H_0=-\frac13PQ. \tag{8}
\]

### 3.2 Polynomial target changes cannot realize the primitive

Suppose polynomials \(F(X,Y),G(X,Y)\) formed a canonical target pair
and gave the homogeneous potential \(H_0\).  Since polynomial closed
one-forms on \(\mathbb A^2\) are exact, (8) would force
\[
F\,dG-X\,dY=d(cXY),\qquad c=-\frac13. \tag{9}
\]
Comparing the \(dX,dY\) coefficients in (9) gives
\[
FG_X=cY,\qquad FG_Y=(1+c)X.
\]
Eliminating \(F\),
\[
(1+c)XG_X-cYG_Y=0,
\]
or
\[
2XG_X+YG_Y=0. \tag{10}
\]
On a monomial \(X^aY^b\), the operator in (10) has eigenvalue
\(2a+b\).  Its polynomial kernel is therefore only the constants.
Thus \(G\) would be constant, contradicting (9).

This proves:

> **Laurent nonhomogenization countermodel.**
> The mixed-weight Pfaff equations, their extreme components,
> centralizer extraction, and polynomial target shears do not by
> themselves force \(h\) to weight \(-1\).

The countermodel is not regular in \(B\), so it does not disprove a
future boundary-sensitive descent.  It proves that boundary regularity
must enter essentially, rather than being checked after a purely
Laurent or graded normalization.

## 4. A boundary-sensitive structural reduction

There is an exact reason to focus next on the field degree and the
missing boundary, rather than on wider coefficient searches.

Let \(D=(u,w)\).  Localizing gives
\[
B[u^{-1}]=k[u,u^{-1},w],
\]
so Nagata's theorem says that \(\operatorname{Cl}(B)\) is generated by
\([D]\).  At the generic point of \(D\),
\[
\operatorname{ord}_D(u)=2,\qquad \operatorname{ord}_D(w)=1,
\]
and therefore
\[
\operatorname{div}(u)=2D.
\]
The class of \(D\) is not principal: if
\(\operatorname{div}(f)=D\), then \(f\) becomes a unit after inverting
\(u\), hence \(f=cu^n\), whose \(D\)-valuation is even.  Consequently
\[
\operatorname{Cl}(B)\simeq\mathbb Z/2.
\]
The same localization argument gives \(B^\times=k^\times\).

A Darboux pair defines an étale morphism
\[
\phi=(P,Q):\operatorname{Spec}B\longrightarrow\mathbb A^2
\]
and a finite function-field degree
\[
d=[\operatorname{Frac}(B):k(P,Q)].
\]
One necessarily has
\[
\boxed{d\ge2.} \tag{11}
\]
Indeed, if \(d=1\), Zariski's Main Theorem makes \(\phi\) an open
immersion.  Its complement cannot contain a divisor, since the
defining irreducible polynomial of such a divisor would restrict to a
nonconstant unit on \(\operatorname{Spec}B\).  Removing codimension at
least two from \(\mathbb A^2\) does not change its class group, giving
\(\operatorname{Cl}(B)=0\), contrary to the calculation above.

This does not solve Route A: nonproper étale maps of degree at least two
are precisely the hard case.  It does identify the correct locus of
difficulty.

## 5. Review, novelty level, and recommended pivot

The homogeneous-Pfaff theorem is a clean new all-degree lemma inside
this project.  Together with the Laurent nonhomogenization theorem, it
is mathematically substantive: one result closes the normalized case,
and the other exactly explains why the obvious normalization argument
cannot finish the proof.  Without a literature audit and a theorem
excluding all boundary-regular pairs, this is not yet a standalone
publishable resolution of JC(2).  It is a credible component of a
paper on Darboux coordinates and étale maps of the quadratic
pseudoplane.

The most promising next direction is a **boundary-sensitive
finite-degree analysis**, not additional bounded coefficient search:

1. use (11) to start with the quadratic function-field case;
2. study the quadratic involution on the normalization of
   \(k[P,Q]\) and its behavior at the missing divisorial valuations;
3. combine the anti-invariant Pfaff potential \(h-\sigma(h)\) with the
   unique \(2\)-torsion boundary class \([D]\);
4. prove that the Laurent-type missing integral element required by a
   degree-two Darboux chart cannot be simultaneously regular along the
   two boundary components of \(w=0\).

The countermodel shows exactly what this argument must rule out: a
quadratic hidden coordinate fixed only up to an involution, with the
nonhomogeneous part of \(h\) lying outside the polynomial target field.
This turns the next search into a normalization/valuation problem with
a sharp target, rather than a brute-force coefficient problem.

## 6. Exact verifier

Run

```sh
.venv/bin/python route_a/verify_pfaff_homogeneous_obstruction.py
```

The script verifies the centralizer identity, complementary eigenvalue
cancellation, the Laurent Darboux/Pfaff identities, the quadratic
involution, and the target Euler-PDE obstruction.
