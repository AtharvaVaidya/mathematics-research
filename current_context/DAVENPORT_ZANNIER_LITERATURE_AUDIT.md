# Davenport--Zannier literature audit for the radial outer equation

Date: 24 July 2026

This note concerns only the literature status of
\[
 UV+2wUV'-3wU'V=E\ne0,\qquad
 \deg U=2k+1,\quad \deg V=3k+1,
 \tag{1}
\]
and of the associated passport and Catalan count.  It does not audit the
seven-mode Hamiltonian deformation theorem or the lower-support
certificates.

## 1. The outer pair is exactly a classical Davenport--Zannier family

After scaling, take \(E=1\), and put
\[
 R(w)=\frac{wV(w)^2}{U(w)^3},\qquad
 \lambda=R(\infty)=\frac{v_{3k+1}^2}{u_{2k+1}^3}.
\]
Equation (1) gives \(R'=V/U^4\), so \(R-\lambda\) has order
\(5k+2\) at infinity.  Consequently
\[
 H(w):=wV(w)^2-\lambda U(w)^3
\]
has degree \(k+1\).  Thus
\[
 P=\lambda U^3,\qquad Q=wV^2
\]
have common degree \(n=6k+3\), passports
\[
 (3^{\,2k+1}),\qquad (2^{\,3k+1},1),
\]
and
\[
 \deg(P-Q)=k+1
 =(n+1)-\bigl((2k+1)+(3k+2)\bigr).
\]
This is exactly a Davenport--Zannier pair in the standard definition.

Conversely, a coprime extremal pair of this special form forces (1).
Indeed, from \(\deg H\le k+1\),
\[
 P'Q-PQ'=HQ'-H'Q
\]
has degree at most \(7k+3\), while
\[
 P'Q-PQ'
 =-\lambda U^2V\bigl(UV+2wUV'-3wU'V\bigr).
\]
Since \(\deg(U^2V)=7k+3\), the parenthesized polynomial is constant.

There is an even more exact match with Zannier's notation.  The lift
\[
 f(t)=U(t^2),\qquad g(t)=tV(t^2)
\]
satisfies
\[
 f(t)^3-g(t)^2=H(t^2),
\]
with
\[
 \deg f=4k+2=2n_0,\quad
 \deg g=6k+3=3n_0,\quad
 \deg(f^3-g^2)=2k+2=n_0+1,
\qquad n_0=2k+1.
\]
This attains Davenport's bound.  Quotienting by the involution
\(t\mapsto-t\) gives precisely Zannier's equation (12),
\[
 f_1(u)^3-u\,g_1(u)^2=h_1(u),
\]
with
\(\deg f_1=n_0=2k+1\),
\(\deg g_1=(3n_0-1)/2=3k+1\), and
\(\deg h_1=(n_0+1)/2=k+1\).

**Publication consequence.**  The outer ODE, its extremal
square/cube interpretation, and the fact that it defines a finite
three-point-cover problem are classical DZ structure, not a new theorem.
The particular way it arises as the leading edge of the GGHV Jacobian
system may still be new as an application.

## 2. The all-\(k\) Catalan count is already in Zannier (1995)

The three branch partitions are
\[
(2^{\,3k+1},1),\qquad
(3^{\,2k+1}),\qquad
(5k+2,1^{\,k+1}).
\tag{2}
\]
The first two partitions are the passport of a weighted bicolored plane
tree.  Elementary suppression gives an especially transparent
classification in this case:

* the underlying tree has \(5k+2\) edges but total weight \(6k+3\);
* because all black weighted degrees are at most two, exactly \(k+1\)
  edges have weight two and all other edges have weight one;
* suppressing every degree-two vertex leaves a plane tree with \(k\)
  trivalent vertices, \(k+2\) leaves, and one distinguished leaf (the
  unique black vertex of weighted degree one);
* deleting the distinguished leaf identifies this with a rooted plane
  full binary tree with \(k\) internal vertices.

Hence the number is
\[
\operatorname{Cat}_k=\frac1{k+1}\binom{2k}{k}.
\tag{3}
\]

This is not merely an unrecorded corollary.  Zannier identifies his
equation (12) with a plane degree-\(1/3\) tree carrying a distinguished
degree-one vertex (Section 5, pp. 121--122), and his Appendix derives
\[
F_n=\sum_{i+j=n}F_iF_j,\qquad F_1=1,
\]
for rooted trees on \(2n\) vertices.  Thus
\[
F_n=\operatorname{Cat}_{n-1}.
\]
Taking \(n=k+1\) gives (3).  Zannier also explicitly records that
\(n_0=7\), i.e. \(k=3\), has five nonisomorphic equation-(12)
possibilities.  Therefore the computed sequence
\[
1,2,5,14
\]
is a proved all-\(k\) Catalan theorem already present in the 1995
literature, rather than only a new experimental pattern.

The same conclusion follows from the later general correspondence between
DZ pairs and weighted bicolored plane trees.  In particular, Pakovich and
Zvonkin prove that equality in the polynomial \(abc\) bound is equivalent
to realization by such a weighted tree.

## 3. Why the non-separable-passport theorem does not prove the endpoint
Wronskian

The passport in (2) is highly **separable**, not non-separable.  It splits
into the balanced valuable subpassports
\[
(3)\mid(2,1)
\quad\text{and}\quad
k\text{ copies of }(3,3)\mid(2,2,2).
\tag{4}
\]
Therefore Kochetkov's simple non-separable formula
\[
\#\{\text{totally labelled trees}\}=(p+q-2)!
\]
does not apply.  Its inclusion--exclusion extension does count the trees,
and the special suppression argument above gives the simpler Catalan
answer, but neither statement controls coefficients of a normalized Belyi
map.

In particular, none of the cited DZ/tree results implies nonvanishing of
the radial endpoint determinant
\[
\Delta_k
=\det([w^i]B_j)_{4\le i\le8}
=\frac{\operatorname{Wr}(\widetilde B_1,\ldots,\widetilde B_5)(0)}
       {0!\,1!\,2!\,3!\,4!}.
\]
The literature results control:

1. existence of a cover with the passport;
2. the number of isomorphism classes;
3. in some cases, fields of definition or unitree rigidity.

They do **not** assert that a specified regular function on the finite
Hurwitz scheme is a unit.  The factor
\[
s_2=[t^{k-1}]
\left(\frac{U}{u_{2k+1}w^{2k+1}}\right)^{1/2}
\]
and the remaining \(4\times4\) minor are coefficient-level invariants of
the normalized representative, not combinatorial passport data.  Zannier's
rationality/descent criterion concerns a field of definition for a cover;
it is not rational descent of the comparison branch and gives no such
unit statement.

The Jacobian-conjecture literature does not close this gap either.
Guccione--Guccione--Valqui explicitly formulate the corresponding
**non-homogeneous** Davenport--Zannier classification as an open problem
in Remark 5.2 of their polynomial-system paper.  Thus there is no published
non-homogeneous DZ theorem available to turn the first resonant endpoint
Wronskian into an automatic nonzero passport invariant.

## 4. What remains potentially publishable

The following should not be claimed as novel:

* the outer ODE viewed in isolation;
* the Belyi/DZ passport;
* squarefreeness/coprimality consequences of extremality;
* finiteness of the normalized outer problem;
* the Catalan count \(C_k\), including the value five at \(k=3\).

The following are not supplied by the cited DZ literature and remain
plausible original contributions:

* embedding this classical DZ family as the exact outer edge of the
  GGHV \((72,108)\) system;
* the complete modular/tame elimination of all lower fibers at \(k=3\);
* the all-\(k\) seven-mode kernel theorem and its exact Hamiltonian
  interpretation;
* the endpoint/BCH square relations;
* any proof that \(\Delta_k\) is a unit on every member of the Catalan
  Hurwitz family;
* any rational-comparison/ring-descent theorem strong enough to turn the
  Kummer obstruction into a Jacobian-conjecture obstruction.

## 5. Strategic implication

The useful new coordinate system is the **involution lift**
\[
U(w),V(w)
\longmapsto
f(t)=U(t^2),\quad g(t)=tV(t^2).
\]
It imports the full classical extremal moment system for
\(f^3-g^2\), while the distinguished fixed point \(t=0\) remembers the
endpoint used by the Hamiltonian problem.  A promising non-brute-force
question is:

> Does \(\Delta_k=0\), translated into Zannier's symmetric power-sum
> coordinates, force an extra decomposition or automorphism of the rooted
> degree-\(1/3\) tree?

Enumeration alone cannot answer this.  A proof would have to use the
moment equations together with the distinguished involution/fixed-point
jet.  This is substantially narrower than eliminating all Catalan Hurwitz
points coefficientwise.

## Primary references

1. U. Zannier, *On Davenport's bound for the degree of \(f^3-g^2\) and
   Riemann's Existence Theorem*, Acta Arith. **71** (1995), 107--137.
   See Section 5 (especially equation (12)), Section 6, and the Appendix.
   <https://matwbn.icm.edu.pl/ksiazki/aa/aa71/aa7122.pdf>

2. F. Pakovich and A. K. Zvonkin, *Minimum degree of the difference of
   two polynomials over \(\mathbf Q\), and weighted plane trees*,
   Selecta Math. (N.S.) **20** (2014), 1003--1065,
   DOI: <https://doi.org/10.1007/s00029-014-0151-0>.

3. N. M. Adrianov, F. Pakovich, and A. K. Zvonkin,
   *Davenport--Zannier Polynomials and Dessins d'Enfants*,
   Mathematical Surveys and Monographs 249, AMS, 2020,
   DOI: <https://doi.org/10.1090/surv/249>.
   Chapters 2--3 give the DZ/weighted-tree correspondence and existence;
   Chapter 11 treats passport enumeration.

4. Yu. Yu. Kochetkov, *Enumeration of one class of plane weighted
   trees*, Fundam. Prikl. Mat. **18** (2013), no. 6, 171--184;
   English transl., J. Math. Sci. **209** (2015), 282--291,
   DOI: <https://doi.org/10.1007/s10958-015-2503-5>.

5. S. Lu and Y. Song, *Enumeration of weighted plane trees by a
   permutation model*, arXiv:2601.07544 (2026).
   This gives a constructive proof of Kochetkov's formula.
   <https://arxiv.org/abs/2601.07544>

6. S. Lu and Y. Song, *Counting Weighted Bi-Colored Plane Trees and
   Their Geometric Applications*, arXiv:2606.21074v2 (21 July 2026).
   This supplies a general counting algorithm and corresponding strong
   Hurwitz-number interpretation.
   <https://arxiv.org/abs/2606.21074>

7. J. A. Guccione, J. J. Guccione, and C. Valqui,
   *A System of Polynomial Equations Related to the Jacobian Conjecture*,
   arXiv:1406.0886v3 (2024), especially Remark 5.2.
   <https://arxiv.org/abs/1406.0886>
