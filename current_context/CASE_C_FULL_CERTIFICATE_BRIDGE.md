# Full certificate bridge for GGHV case c

Date: 25 July 2026

## Audited theorem

Assume the characteristic-zero reductions in the public preprint
Guccione--Guccione--Horruitiner--Valqui (GGHV), *Increasing the degree of
a possible counterexample to the Jacobian Conjecture from 100 to 108*,
arXiv:2204.14178.  Then the coefficient system in Proposition 4.3(1)
has no solution over an algebraically closed field of characteristic
zero.

Together with the independent all-scale elimination of Proposition
4.3(2), this gives the bounded corollary

\[
\boxed{\max(\deg P,\deg Q)\geq125}
\]

for a hypothetical plane Keller counterexample in characteristic zero.
This is a bounded exclusion with a new derivation, not a proof of the plane Jacobian
Conjecture.  An independent announcement of the same bounded conclusion
exists, so no priority claim is made here.

The computer-assisted part is exact.  Its trusted base consists of
rational and finite-field arithmetic, SymPy's exact polynomial
arithmetic, and Singular's exact finite-field standard-basis algorithm.
The direct characteristic-zero homogeneous `modStd(...,1)` path described
below additionally trusts the exactness guarantee in Singular
`modstd.lib` 4.4.1.4.

## 1. External preprint input

This archive does not reprove the classification of small possible
counterexamples.  The external implications used are:

1. GGHV Theorem 2.1 and the exhaustive small-case table on its page 3
   reduce a counterexample with maximum degree below \(125\) to degree
   pair \((72,108)\), up to swapping the coordinates, and to the corner
   cases \((8,28)\), \((9,27)\).
2. GGHV Proposition 4.1 and Corollary 5.7, the latter proved through
   Theorem 5.1, eliminate the \((9,27)\) configuration.
3. GGHV Proposition 4.3 reduces the remaining \((8,28)\) configuration
   to exactly two displayed Newton-polygon alternatives.
4. Proposition 4.3(2), the common outcome of the proof's cases a and b,
   is excluded by `ALLSCALE_MARKED_CUSP_OBSTRUCTION.md`.
5. Proposition 4.3(1), the proof's case c, is excluded by the certificate
   audited here.

Items 1--3 are external theorem dependencies.  Items 4--5 are the new
work in this archive.

## 2. Exact import of the case-c polygons

GGHV Proposition 4.3(1) gives

\[
\begin{aligned}
\Delta_P&=\operatorname{conv}
\{(0,0),(1,0),(8,14),(8,16),(0,8)\},\\
\Delta_Q&=\operatorname{conv}
\{(0,0),(2,1),(12,21),(12,24),(0,12)\}.
\end{aligned}
\]

Put

\[
z=xy,\qquad h=xy^2.
\]

The exponent map is unimodular:

\[
x^ay^b=z^{\,2a-b}h^{\,b-a},\qquad
\det\begin{pmatrix}2&-1\\-1&1\end{pmatrix}=1.
\]

Enumerating every lattice point, not only the vertices, gives exactly 61
\(P\)-positions and 125 \(Q\)-positions.  After removing the two
bracket-invisible additive constants and the 19 outer coefficients, the
remaining count is

\[
61+125-2-8-11=165.
\]

These are precisely the supports used by
`route_bd_case_c_radial_obstruction.py`.

Since

\[
\det\frac{\partial(z,h)}{\partial(x,y)}=h,\qquad
x^2=\frac{z^4}{h^2},
\]

the reduced bracket is, after an inessential sign change,

\[
\{P,Q\}_{z,h}=\frac{z^4}{h^3}.
\]

The outer blocks are

\[
P_2=z^2\frac{U(h)}h,\qquad
Q_3=z^3\frac{V(h)}h,
\]

with

\[
\deg U=7,\quad \deg V=10,\quad U(0)=V(0)=1,
\]

and their bracket equation is

\[
UV+2hUV'-3hU'V=1. \tag{1}
\]

Thus no support, vertex, or fixed-pole condition is lost in the radial
presentation.

## 3. Exhaustion of the outer fiber

For

\[
R(h)=h\frac{V(h)^2}{U(h)^3},
\]

equation (1) gives

\[
R'(h)=\frac{V(h)}{U(h)^4}.
\]

The resulting passport is

\[
(2^{10},1),\qquad(3^7),\qquad(17,1^4).
\]

The exact character calculation gives weighted Hurwitz number five.
Every permutation triple is transitive: a component disjoint from the
17-cycle would lie among the four fixed sheets of that permutation, where
the other two permutations would have to be mutual inverses; one is an
involution and the other is a product of 3-cycles with no fixed point, so
no such component exists.  Cover automorphisms are trivial because they
fix the unique simple zero and unique 17-fold point; in the normalized
coordinate they are \(h\mapsto\lambda h\), and \(R(h)=h+O(h^2)\) forces
\(\lambda=1\).

The reconstructed irreducible quintic field

\[
K=\mathbf Q[s]/(f(s)),\qquad s=u_7^{-1},
\]

contains five distinct normalized solutions of (1).  The Hurwitz count
therefore proves that these are the complete geometric outer fiber.  In
particular, the locus \(u_1=0\) contains no additional cover; normalization
by \(u_1=1\) is exhaustive.

At \(p=32003\), the primitive quintic has squarefree factorization

\[
(s-26839)(s-16621)
(s^3-11133s^2-11294s-6180).
\]

The two linear factors and one cubic factor are all five geometric outer
points of the good reduced fiber.

## 4. Why seven modes are exhaustive

At successive radial deficits, the dimensions of the bounded homogeneous
kernels are

\[
(2,2,2,1,0,0,\ldots,0).
\]

The seven canonical modes consequently have weights

\[
(1,1,2,2,3,3,4).
\]

There are two independent checks.

- `route_bd_universal_radial_kernel_theorem.py` gives the
  characteristic-zero kernel parametrization and endpoint count.
- `verify_case_c_full_certificate_bridge.py` computes all fifteen linear
  kernel dimensions on every factor of the good reduced outer fiber.  The
  kernel dimensions are
  \((2,2,2,1,0,\ldots,0)\) on the two rational points and on the cubic
  factor.  The nonzero maximal minors in good reduction prove the
  corresponding rank lower bounds in characteristic zero, while the
  seven explicit characteristic-zero modes give the reverse bounds.

At each later stage, exact row reduction solves every new coefficient as
a polynomial in these seven parameters and records all cokernel rows.
Therefore a solution of the original 165-coordinate system determines a
point of the seven-mode consistency scheme.  Failure of any retained
cokernel row cannot be repaired by a later coefficient.

## 5. Complete special-fiber certificate

The consistency rows are weighted homogeneous for

\[
\mathbf P(1,1,2,2,3,3,4).
\]

Already the rows through deficit eight generate an ideal \(I_8\) such
that, over each of

\[
\mathbf F_{32003},\quad
\mathbf F_{32003},\quad
\mathbf F_{32003^3},
\]

Singular verifies

\[
X_i^{32}\in I_8\qquad(0\le i\le6).
\]

The three quotient dimensions are all \(380\).  Thus the common affine
zero set is supported only at the cone origin, and

\[
\operatorname{Proj}
\mathbf F_{32003^{\,e}}[X_0,\ldots,X_6]/I_8
=\varnothing
\]

for \(e=1,1,3\).  Since these factors exhaust the reduced outer algebra,
the complete weighted-projective special fiber is empty.

For the characteristic-zero lift, the proof uses the equivalent
set-theoretic square branch.  The two deficit-four rows are exact nonzero
multiples of

\[
\left(X_2-\frac{169}{48}X_0^2\right)^2.
\]

Every field-valued solution therefore satisfies the homogeneous root
equation \(X_2=(169/48)X_0^2\).  Substituting that equation leaves rows of
weights \(5,6,7,8\) with counts \(1,3,5,6\).  The four charts below prove
that this square-branch projective special fiber is empty.  The
unspecialized \(X_i^{32}\) calculation is an independent global
cross-check of the same set-theoretic conclusion.

The four-chart calculation is an independent, more transparent
decomposition of the same statement:

\[
D(L),\quad V(L)\cap D(A),\quad
V(L,A)\cap D(B),\quad V(L,A,B).
\]

The first two charts have exact finite-field unit ideals.  The third is
killed by a nonzero quadratic resultant.  On the fourth, a \(3\times3\)
determinant forces \(X_4=X_5=0\), and the deficit-eight rows force
\(X_6=0\).  It is essential that all four charts be assembled.  Emptiness
of \(D(L)\) alone would not justify proper specialization, because a
generic \(L\ne0\) point could specialize to \(L=0\).

## 6. Characteristic-zero specialization

The exact square identity and every square-branch row through deficit
eight are constructed in \(K[X]\).  Every coefficient is integral at the
selected primes above \(32003\), and the exact-to-modular verifier compares
every imposed row coefficient-for-coefficient, in its original order,
with the independently constructed finite-field rows.

After localizing the ring of integers of \(K\) at the finitely many
denominators, the weighted homogeneous equations define a closed
subscheme

\[
\mathcal X\subset\mathbf P_R(1,1,2,2,3,3,4).
\]

Weighted projective space is proper over \(R\) (equivalently, pass to a
Veronese subring), hence \(\mathcal X\to\operatorname{Spec}R\) is proper.
If the characteristic-zero generic fiber were nonempty, its image would
be a closed subset containing the generic point of the integral base and
therefore all of \(\operatorname{Spec}R\).  That contradicts the empty
fiber above \(32003\).  Consequently the characteristic-zero
weighted-projective fiber is empty.

No flatness assumption is used.  Properness of the **complete** projective
fiber, rather than of an affine chart, is the decisive point.

## 7. Direct characteristic-zero generic-chart certificates

There is also a direct affine route.  Adjoin the irreducible \(f(s)\) to
each normalized chart ideal \(J\subset\mathbf Q[s,X]\), homogenize all
generators with a new variable \(h\), and run

```text
ideal Jh=homog(J,h);
ideal Hh=modStd(Jh,1);
```

in Singular 4.4.1.  The installed `modstd.lib` documentation states that
with `exactness=1` the result is a verified standard basis, and that for
homogeneous generators it is a standard basis of the input ideal (not
merely a high-probability superideal).  Therefore a zero remainder for
\(h^N\) proves

\[
h^N\in J^h,
\]

and dehomogenizing at \(h=1\) proves \(1\in J\).  This is a direct
characteristic-zero certificate in the rational presentation
\(\mathbf Q[s,X]/(f)\).

This paragraph audits the implication, not a completed run: the optimized
\(D(L)\) job was stopped after a bounded window once the independent
proper-specialization proof was complete, and no `HPOWER` output is
claimed.

This should not be confused with the fast nonhomogeneous
`modStd(J,1)` run: for a global nonhomogeneous input, the library labels
equality with the input ideal as high probability.  Only the explicitly
homogenized run would qualify as an exact direct certificate.  No output
from that optional route is used in the proper-specialization proof.

Independently, ordinary exact `std` over \(K\) proves

\[
A^8\in
(L,F_5,F_{6,0},F_{6,1},F_{6,2},F_{7,0}),
\]

which kills \(V(L)\cap D(A)\).  The complete-special-fiber argument in
Sections 5--6 remains a separate proof even if the direct \(D(L)\)
calculation is omitted.

## 8. The cone origin and the required vertices

The GGHV opposite vertices do **not** occur in the early deficit-two and
deficit-three blocks.  Their correct radial locations are

\[
(0,8)\mapsto(-8,8),\qquad
(0,12)\mapsto(-12,12),
\]

so the required coefficients are

\[
[z^{-8}h^8]P\ne0,\qquad
[z^{-12}h^{12}]Q\ne0.
\]

They occur at deficits ten and fifteen.  This corrects an earlier wording
error in `CASE_C_N3_EXACT_INTERFACE.md`.

The correction does not leave a solution at the seven-mode origin.
When all seven modes vanish, the first four lower blocks vanish.  Every
later source is then zero, and the zero-kernel statement after deficit
four forces each later block to be zero by induction.  In particular,
both displayed required coefficients vanish.  Hence every genuine case-c
solution gives a nonzero weighted-projective point, and the affine cone
origin is forbidden.

## 9. Reproducibility checklist

Required:

- Python 3.12 with the pinned `requirements.txt`;
- Singular 4.4 or newer;
- exact factorization of the outer quintic;
- all two linear plus one cubic factors at \(32003\);
- coefficientwise exact-to-modular agreement through deficit eight;
- \(X_i^{32}\) reductions for all seven modes on every outer factor;
- exact kernel ranks through all fifteen deficits; and
- verification that the two required vertices are at deficits ten and
  fifteen and vanish under zero-kernel propagation.

Quick interface audit:

```bash
.venv/bin/python \
  current_context/verify_case_c_full_certificate_bridge.py
```

Complete special-fiber replay:

```bash
.venv/bin/python \
  current_context/verify_case_c_full_certificate_bridge.py \
  --run-special-fiber
```

Modular square branch and its two generic charts:

```bash
.venv/bin/python route_bd_case_c_n3_hurwitz_bridge.py
.venv/bin/python route_bd_case_c_n3_generic_charts.py
```

Exact-quintic row transport and boundary charts:

```bash
.venv/bin/python scratch_case_c_n3_special_charts_Q.py
```

Direct homogeneous characteristic-zero generic charts:

```bash
.venv/bin/python scratch_case_c_n3_generic_charts_Q.py \
  --skip-modular-crosscheck --chart L_NE_0 --one-certificate
.venv/bin/python scratch_case_c_n3_generic_charts_Q.py \
  --skip-modular-crosscheck --chart L_EQ_0_A_NE_0 --one-certificate
```

One minimal row choice is already a sufficient certificate on each chart;
running the three redundant choices concurrently oversubscribes Singular's
own modular workers and is not the recommended publication replay.

The files in `tmp/` are runtime accelerators.  A publication replay must
first move

```text
tmp/case_c_n3_generic_charts_Q.pkl
tmp/case_c_n3_special_charts_Q.pkl
tmp/case_c_n3_special_recurrence_Q.pkl
```

out of `tmp`, run the reconstruction from scratch, and archive:

1. stdout and stderr;
2. Python, SymPy, and Singular versions;
3. the exact `modstd.lib` version string;
4. SHA-256 hashes of every verifier and log; and
5. the regenerated cache hashes only as diagnostics, never as premises.

The canonical driver is
`publication_artifacts/degree-125-bound/cleanroom-2026-07-25/replay.sh`
and must be invoked from the repository root after the three caches have
been moved aside.

## Publication verdict

The bounded theorem is mathematically closed by the complete-projective-
fiber specialization argument, subject to the explicitly listed
public GGHV preprint inputs and standard CAS trust assumptions.  A direct
\(K\)-basis containing \(L^{23}\), or a completed homogeneous
direct-\(\mathbf Q\) `HPOWER` replay, is optional and is not a missing
lemma.

The publication bundle includes a clean-room cache-free run, archived log,
and software/source hashes.  The remaining work before submission is an
independent human line-by-line check of the external GGHV implications.
That remaining task does not expand the theorem to arbitrary degree, so
this result must not be presented as \(JC(2)\).
