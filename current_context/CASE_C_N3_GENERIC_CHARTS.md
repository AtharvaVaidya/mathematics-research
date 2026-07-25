# Case-c \(n=3\): the two generic charts die at deficit seven

## Certified result

Continue from the square branch and the deficit-five survivor in
`CASE_C_N3_HURWITZ_BRIDGE.md`:

\[
Y_2=\frac{169}{48}Y_0^2,\qquad
F_5=L(Y_0,X_1)X_6+F_5^{(0)}=0.
\]

The two generic charts left open there are both empty after adding only
the deficit-six and deficit-seven consistency rows:

\[
\boxed{L\ne0\ \Longrightarrow\ \varnothing},\qquad
\boxed{L=0,\ A\ne0\ \Longrightarrow\ \varnothing}.
\]

This statement has been checked exactly over both rational factors and
the irreducible cubic factor of the complete five-point outer Hurwitz fiber
over \(\mathbf F_{32003}\).  The cubic calculation handles its three
geometric conjugates simultaneously.

The deficit-six rows alone do **not** give either contradiction.  Singular
returns a nonunit standard basis on both reduced charts through weight six
and the unit ideal after the five weight-seven rows are added.  Thus the
new conclusion is a genuine deficit-seven obstruction, not a relabeling of
the already-known deficit-six cuts.

## Chart \(L\ne0\)

The form \(L\) has weight one.  A geometric point on this chart can be
rescaled uniquely to \(L=1\).  The coefficient of \(X_1\) in \(L\) is a
unit on every outer factor, so this normalization eliminates \(X_1\).
The deficit-five row is then monic in \(X_6\) and eliminates \(X_6\).
Together with

\[
Y_2=\frac{169}{48}Y_0^2,
\]

the chart is reduced isomorphically to four affine variables

\[
(Y_0,X_3,X_4,X_5).
\]

It has precisely three inherited weight-six rows, with term counts

\[
(41,41,15),
\]

and five inherited weight-seven rows, with term counts

\[
(60,60,60,56,15).
\]

The first three rows generate a proper ideal.  In fact, adjoining **any
two of the first three** weight-seven rows already gives the unit ideal;
all eight rows therefore do as well.  This holds over each of

\[
\mathbf F_{32003},\quad
\mathbf F_{32003},\quad
\mathbf F_{32003^3}.
\]

This is an exact contradiction on the normalized chart.

## Chart \(L=0,\ A\ne0\)

On \(L=0\), solve the nonzero \(X_1\)-coefficient of \(L\), and write

\[
F_5=A(X_3,Y_0^2)X_5+B(X_3,Y_0^2)X_4+Y_0C(X_3,Y_0^2).
\]

The form \(A\) has weight two.  Over the algebraic closure, every point of
this chart can therefore be rescaled to \(A=1\).  Its \(X_3\)-coefficient
is a unit on every outer factor, so \(A=1\) eliminates \(X_3\), after which
\(F_5=0\) is monic in \(X_5\) and eliminates \(X_5\).  The remaining affine
variables are only

\[
(Y_0,X_4,X_6).
\]

The three inherited weight-six rows have term counts

\[
(15,15,12),
\]

and the five inherited weight-seven rows have term counts

\[
(19,19,19,19,12).
\]

Again the weight-six ideal is proper.  Here the obstruction is even
sparser: adjoining **any one of the first three** weight-seven rows gives
the unit ideal on every outer factor.  This is a second exact chart
contradiction.

## Exhaustive case-c consequence

The chart cover from the earlier bridge is exhaustive:

1. \(L\ne0\): empty at deficit seven by the first certificate above;
2. \(L=0,A\ne0\): empty at deficit seven by the second certificate above;
3. \(L=A=0,B\ne0\): empty already at deficit six;
4. \(L=A=B=0\): deficit six forces \(X_4=X_5=0\), deficit seven is
   automatic, and deficit eight forces \(X_6=0\).

The fourth branch ends only at the affine cone origin, so it contributes
no weighted-projective point.  Consequently the complete modular
weighted-projective case-c fiber is empty through deficit eight, now by a
small triangular chart proof rather than a seven-variable origin-power
calculation.

The characteristic-zero deduction is slightly broader than either
individual affine certificate.  An open chart can specialize into its
boundary, so modular emptiness of one affine normalization alone is not a
proper-specialization argument.  What is proper is the **complete**
weighted-projective fiber.  Because the four charts above exhaust its
special fiber and all four are empty projectively, any characteristic-zero
point would have a specialization there, a contradiction, provided the
previously audited outer-Hurwitz integral model and reduction import are
used.

Thus:

- the unit ideals are unconditional exact finite-field computations;
- the passage to the complete characteristic-zero case-c fiber uses the
  existing good-reduction, exhaustiveness, and projectivity audit;
- this eliminates the bounded case-c alternative, not the unrestricted
  Jacobian Conjecture.

## Verifier

Run:

```bash
.venv/bin/python route_bd_case_c_n3_generic_charts.py
```

The script constructs only the seven Hamiltonian modes and the consistency
rows through deficit seven.  It never expands the original 165 lower
coefficients (or the larger unreduced coefficient presentation).  On each
chart it performs the displayed triangular substitutions before invoking
Singular in four and three variables, respectively.
