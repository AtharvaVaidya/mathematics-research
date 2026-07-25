# Case-c \(n=3\) Hurwitz bridge

## Result

In the integral normal form

\[
 P_+=H^2+R,\qquad
 Q_+=H^3+\frac32HR+c_8P_++c_4H+S,
 \qquad \deg_yR,\deg_yS\leq 3,
\]

grade \(n=3\) is the first bracket row with no new coefficient of
\(S\).  On the complete five-point outer Hurwitz fiber, its first
nonautomatic radial coefficient is exactly the radical equation

\[
 \boxed{\left(Y_2-\frac{169}{48}Y_0^2\right)^2=0},
\]

where, in the canonical seven-mode coordinates,

\[
 Y_0=X_0-2X_1,\qquad
 Y_2=X_2-\frac23X_3.
\]

There are two compatibility rows at this layer, and both are nonzero
scalar multiples of the displayed square.  Thus this row genuinely cuts
the lower deformation space, but it does not yield a contradiction:
set-theoretically it leaves the branch

\[
 Y_2=\frac{169}{48}Y_0^2.
\]

## Why this is the \(n=3\) row

Put \(w=zy\).  A monomial \(z^j y^3\) becomes \(z^{j-3}w^3\), so its
radial \(z\)-degree is \(j-3\).  The dictionary in this row is therefore

\[
\begin{array}{c|ccccc}
j&7&6&5&4&3\\ \hline
\text{radial degree}&4&3&2&1&0\\
\text{radial deficit}&0&1&2&3&4 .
\end{array}
\]

The \(z^7y^3\) coefficient is the outer equation.  The next three
coefficients \(z^6y^3,z^5y^3,z^4y^3\) are automatic on the outer
Hurwitz algebra.  The first nonautomatic coefficient is \(z^3y^3\),
or radial deficit four, and it gives the square above.

## Scope of the certificate

The fast verifier checks the complete reduced five-point fiber modulo
\(32003\): both rational points and the irreducible cubic factor.  Its
optional `--exact-lift` mode reconstructs the characteristic-zero
five-point quotient and repeats the four radial stages directly in that
quotient.  This avoids selecting numerical roots or expanding a large
global elimination ideal.  Both the fast audit and the exact lift pass.

Run:

```bash
.venv/bin/python route_bd_case_c_n3_hurwitz_bridge.py
.venv/bin/python route_bd_case_c_n3_hurwitz_bridge.py --exact-lift
```

The first command is suitable for the bundled regression suite.  The
second is a slower independent characteristic-zero certificate.

## The weight-five row is triangularly solvable

After imposing

\[
Y_2=\frac{169}{48}Y_0^2,
\]

the next radial layer has exactly one surviving weight-five
compatibility on each of the three reduced outer factors.  It is not
divisible by \(Y_0\), so replacing the radical branch by the special
subbranch \(Y_0=0\) would lose possible solutions.  It also involves the
remaining lower modes (including the weight-four mode) and does not
factor by an evident universal endpoint coordinate in the current
audit.

Nevertheless, it is not yet an obstruction.  Write the survivor as

\[
 F_5=L(Y_0,X_1)X_6+F_5^{(0)}.
\]

Here \(L\) is a nonzero outer-dependent linear form.  On \(L\ne0\), the
equation simply determines \(X_6\).  On the exceptional divisor \(L=0\),
put \(T=X_3\) and \(R=Y_0^2\).  The remaining equation has the form

\[
 F_5^{(0)}
 =A(T,R)X_5+B(T,R)X_4
  +Y_0C(T,R),
\]

where \(A,B\) are linear in \(T,R\), and \(C\) is quadratic.  The
\(2\times2\) coefficient matrix taking \((T,R)\) to \((A,B)\) has
nonzero determinant on both rational outer points and on the cubic
factor.  Therefore:

- if \((T,R)\ne(0,0)\), one of \(X_4,X_5\) solves the equation;
- if \((T,R)=(0,0)\), then \(Y_0=T=0\) and \(F_5^{(0)}=0\).

Thus the weight-five compatibility is solvable over every choice of the
earlier modes.  The good-reduction calculation also shows that the
coefficient determinant is a unit in the characteristic-zero
five-point algebra: its norm remains nonzero modulo \(32003\).

## Deficit-six chart table

The weight-five cover is exhaustive because \(L\ne0\) and \(L=0\)
partition the square branch, while on \(L=0\) the determinant above
shows

\[
A=B=0\quad\Longleftrightarrow\quad X_3=Y_0^2=0
\]

set-theoretically.  Reducing the three deficit-six rows gives:

\[
\begin{array}{c|c|c}
\text{chart}&\text{elimination}&\text{deficit-six outcome}\\ \hline
L\ne0
  &X_6=-F_5^{(0)}/L
  &\text{three nonzero, pairwise nonproportional cuts}\\
L=0,\ A\ne0
  &X_5=-(BX_4+Y_0C)/A
  &\text{a nonzero row independent of }X_6\text{ remains}\\
L=A=0,\ B\ne0
  &X_4=-Y_0C/B
  &\text{empty}\\
L=A=B=0
  &Y_0=X_1=X_3=0
  &X_4=X_5=0,\quad X_6\text{ free}.
\end{array}
\]

On the third chart, \(B\ne0\) is equivalent to \(Y_0\ne0\), so normalize
\(Y_0=1\).  Two rows are linear in \(X_6\); eliminating \(X_6\) leaves a
quadratic in \(X_5\), while the third row is another quadratic in
\(X_5\).  Their resultant is nonzero on both rational factors and the
cubic factor.  Hence this chart is empty over the algebraic closure, not
merely over the sampled finite field.

On the fourth chart, the three rows have coefficient matrix in

\[
(X_4^2,\ X_4X_5,\ X_5^2)
\]

with nonzero determinant on every outer factor.  They therefore force
\(X_4=X_5=0\) set-theoretically.  No deficit-six row contains \(X_6\) on
this chart.

The modular determinants and resultant are nonzero in every factor of a
good reduced five-point fiber.  Consequently their norms are nonzero in
characteristic zero as well.  This is a nonvanishing certificate, while
the optional exact lift independently proves the central deficit-four
square identity itself.

## Deepest branch at deficit seven

The cheapest surviving branch after deficit six is

\[
Y_0=X_1=Y_2=X_3=X_4=X_5=0,\qquad X_6\ \text{free}.
\]

Deficit seven is automatic on this branch on all five outer points.
This is also forced by the grading: a polynomial in the sole surviving
weight-four variable \(X_6\) cannot have weight seven.

At deficit eight, exactly five rows survive on every outer factor, and
each is a nonzero scalar multiple of

\[
X_6^2.
\]

Consequently deficit eight forces \(X_6=0\) set-theoretically.  The
deepest branch is therefore completely rigid:

\[
Y_0=X_1=Y_2=X_3=X_4=X_5=X_6=0.
\]

This is the correct stopping point for this chart.  The two generic
deficit-six loci are analyzed separately in
`CASE_C_N3_GENERIC_CHARTS.md`.  After normalizing \(L=1\) or \(A=1\) and
performing the triangular eliminations described above, their rows through
deficit seven generate the unit ideal over every factor of the complete
modular five-point fiber.  Hence both generic charts are empty at deficit
seven.  Together with the third and fourth charts here, this gives an
exhaustive small-chart proof of modular weighted-projective emptiness
through deficit eight.

This triangular route is preferable to a global Gröbner expansion,
since:

1. all earlier radial coefficients are automatic;
2. the square branch has already removed one deformation direction;
3. weight five has now been proved triangularly solvable, so it should
   be eliminated rather than treated as an obstruction; and
4. one deficit-six chart is eliminated and the deepest surviving chart
   is rigidified to the origin by a one-monomial test; and
5. the \(c_8\) shear contributes only Euler-image terms to the relevant
   cokernels, so it should not be reintroduced into this calculation.

The companion verifier is:

```bash
.venv/bin/python route_bd_case_c_n3_generic_charts.py
```

## Publication assessment

This bridge is a compact, independently checkable structural lemma for
the bounded \((72,108)\) case-c elimination.  Together with the
fractional-resonance descent and the integral normal form, it is
potentially worth including in a paper or computational appendix because
it replaces a large block expansion by one canonical square, an
exhaustive triangular chart cover, and small determinant/resultant
certificates.

It is not a proof of the Jacobian Conjecture, and the endpoint-square
pattern by itself should not be advertised as a new general theorem:
the all-\(k\) formula is presently supported by the complete small
Hurwitz fibers and a local Hamiltonian coefficient calculation, not by a
global proof for arbitrary \(k\).
