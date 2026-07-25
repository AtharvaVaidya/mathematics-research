# Exact characteristic-zero certificate for the special case-c charts

## Result

Let

\[
K=\mathbf Q[s]/(f(s))
\]

be the irreducible quintic normalized outer Hurwitz field reconstructed by
`route_bd_ab_outer_lift.py`.  On the square branch

\[
X_2=\frac{169}{48}X_0^2
\]

of the case-c \(n=3\) recurrence, the two special charts are now treated
directly over \(K\):

\[
\boxed{L=A=0,\ B\ne0\Longrightarrow\varnothing},
\]

and

\[
\boxed{L=A=B=0\Longrightarrow
       X_0=X_1=X_2=X_3=X_4=X_5=X_6=0}.
\]

Thus the deepest chart contains only the affine cone origin.  There is no
nonzero weighted-projective point on either special chart.

The standalone verifier is

```text
scratch_case_c_n3_special_charts_Q.py
```

It is deliberately separate from the fast modular verifier and from the
generic-chart Gröbner calculation.

## Exact recurrence and transport

The verifier reconstructs the outer coefficients \(U,V\) in \(K[w]\) and
performs the canonical seven-mode recurrence through radial deficit eight.
The exact cokernel-row counts are

\[
(0,0,0,2,2,4,5,6).
\]

After the endpoint-coordinate change and the square substitution, the
nonzero row inventory is

\[
\begin{array}{c|rrrr}
\text{weight}&5&6&7&8\\ \hline
\text{rows}&1&3&5&6.
\end{array}
\]

Every exact imposed row is then specialized, coefficient-for-coefficient
and in its original order, to:

- the first rational factor modulo \(32003\);
- the second rational factor modulo \(32003\); and
- the irreducible cubic factor modulo \(32003\).

The comparison agrees exactly through deficit eight.  It therefore locks
the primitive element, endpoint-coordinate convention, pivot profile, row
order, and row scalars.  It is stronger than merely comparing ranks or
supports.

## Chart \(L=A=0,\ B\ne0\)

Write the weight-five survivor on \(L=0\) as

\[
F_5=A(X_3,X_0^2)X_5+B(X_3,X_0^2)X_4+C.
\]

The verifier checks directly in \(K\) that all of the following are
nonzero:

1. the \(X_1\)- and \(X_0\)-coefficients of \(L\);
2. the \(X_3\)-coefficient of \(A\);
3. the determinant of the coefficient map
   \[
   (X_3,X_0^2)\longmapsto(A,B);
   \]
4. the scalar \(B/X_0^2\) after imposing \(A=0\);
5. both coefficients used to eliminate \(X_6\); and
6. the resultant of the two remaining quadratics in \(X_5\).

Each scalar also has nonzero image on both rational factors and throughout
the cubic factor modulo \(32003\).  In particular, every division in the
triangular chart reduction is by a genuine field unit and by a unit of the
chosen good reduction.

On this chart \(B\ne0\) is equivalent to \(X_0\ne0\), so weighted scaling
normalizes \(X_0=1\).  Two deficit-six rows are linear in \(X_6\); their
compatibility and the third row are quadratics in \(X_5\).  Their exact
resultant is nonzero in \(K\).  Hence they have no common root over
\(\overline K\), proving that this chart is empty.

## Chart \(L=A=B=0\)

The nonzero \(2\times2\) coefficient determinant above gives, set
theoretically,

\[
L=A=B=0\quad\Longrightarrow\quad
X_0=X_1=X_2=X_3=0.
\]

The three deficit-six rows are then a coefficient matrix multiplying

\[
(X_4^2,\ X_4X_5,\ X_5^2).
\]

Its exact \(3\times3\) determinant is nonzero in \(K\), and is a unit on
every reduced outer factor modulo \(32003\).  Therefore

\[
X_4=X_5=0
\]

set-theoretically.

Deficit seven vanishes identically on the remaining \(X_6\)-axis.  At
deficit eight exactly five rows survive, and each is

\[
c_iX_6^2
\]

with \(c_i\ne0\) in \(K\).  All five \(c_i\) are also units at the chosen
good reduction.  Thus \(X_6=0\), leaving only the affine cone origin.

## Why this removes proper specialization for these charts

The special-chart contradictions are finite scalar nonvanishing
certificates, not affine unit-ideal computations.  Once the exact rows are
known to be integral at \(32003\) and to reduce coefficient-for-coefficient,
all triangular operations commute with reduction because every divisor
has unit reduction.  A scalar whose reduction is nonzero cannot have been
zero in \(K\).

The verifier nevertheless computes every scalar directly in \(K\), so the
conclusion does not require the proper-specialization argument used in the
earlier modular-only audit.

## Scope and remaining interface

This result closes the two special charts of the seven-mode \(n=3\)
coefficient model directly in characteristic zero.  It does **not**, by
itself:

- certify the two generic charts \(L\ne0\) and \(L=0,A\ne0\);
- prove that every original 165-coordinate case-c point is represented by
  the canonical seven-mode recurrence; or
- prove that the affine cone origin is excluded by the required original
  Newton vertex.

The last two items belong to the coefficient-model/interface audit.  In
particular, the statement “only the cone origin survives” eliminates the
weighted-projective fiber only after the required case-c vertex is proved
to give a nonzero projective coordinate in this model.

## Reproduction

The first run reconstructs the outer quotient and performs the exact
recurrence.  It checkpoints each completed deficit in

```text
tmp/case_c_n3_special_recurrence_Q.pkl
```

and stores the final rows in

```text
tmp/case_c_n3_special_charts_Q.pkl.
```

These files are runtime accelerators only.  Removing them forces a complete
reconstruction.  With the final cache present, the full row
cross-specialization and all special-chart scalar checks take about ten
seconds.
