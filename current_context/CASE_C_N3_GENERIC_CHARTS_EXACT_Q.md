# Exact characteristic-zero certificate for the generic case-c charts

## Result

The two normalized generic charts in the case-c \(n=3\) fiber are empty
directly over the exact characteristic-zero outer Hurwitz algebra:

\[
\boxed{L\ne0\Longrightarrow\varnothing,\qquad
       L=0,\ A\ne0\Longrightarrow\varnothing.}
\]

This is now an exact calculation over the irreducible quintic number
field, not an inference from the factorization modulo \(32003\).

The standalone verifier is

```text
scratch_case_c_n3_generic_charts_Q.py
```

The existing modular verifier
`route_bd_case_c_n3_generic_charts.py` was not modified.

## Exact outer algebra and transport

The verifier reconstructs the normalized outer algebra

\[
K=\mathbf Q[s]/(f(s)),\qquad s=u_7^{-1},
\]

by the existing 64-prime CRT and rational-reconstruction procedure.
The primitive integer form of \(f\) is

\[
\begin{aligned}
f_{\rm prim}(s)={}&
5515523528689697521685932802788985662696864088064s^5\\
&+65062739516770841146036374449381894864326252512971587584s^4\\
&+344441584702591633271258969281268771087358180440968435133841408s^3\\
&+1237781539078909858338290542300930711454790682861991293593776119332864s^2\\
&+2419327446396921250927947382299550515503991095316771187749320719639052502144s\\
&-930206660129096433749475266122359445351031352517661885125550567798599734193335611.
\end{aligned}
\]

It is squarefree and irreducible over \(\mathbf Q\).  The reconstructed
outer coefficients satisfy the normalized outer ODE exactly in \(K[w]\).

The lower radial recurrence is then performed over \(K\) through deficit
seven.  Its cokernel-row counts by deficit are

\[
(0,0,0,2,2,4,5).
\]

After the endpoint change and the exact square substitution

\[
X_2=\frac{169}{48}X_0^2,
\]

the surviving row inventory is

\[
\begin{array}{c|ccc}
\text{weight}&5&6&7\\ \hline
\text{rows}&1&3&5.
\end{array}
\]

As an adversarial transport check, every exact imposed row is reduced at
the two rational points and the cubic factor modulo \(32003\).  The
result agrees coefficient-for-coefficient and in the original row order
with the independently generated modular rows.  Thus the primitive
element, endpoint-coordinate order, row order, and all row scalars are
locked.

## Exact unit certificates

The same triangular normalizations as in the modular verifier are used.

On \(L\ne0\), normalize \(L=1\), eliminate \(X_1\) and \(X_6\), and work
in the four variables

\[
X_0,X_3,X_4,X_5.
\]

All three deficit-six rows are retained.  Each of the three minimal
choices of two of the first three deficit-seven rows gives the unit
ideal:

```text
Q5 L_NE_0 MINIMAL (0, 1) UNIT 1
Q5 L_NE_0 MINIMAL (0, 2) UNIT 1
Q5 L_NE_0 MINIMAL (1, 2) UNIT 1
```

On \(L=0,\ A\ne0\), normalize \(A=1\), eliminate \(X_1,X_3,X_5\), and
work in

\[
X_0,X_4,X_6.
\]

All three deficit-six rows are again retained.  Each one of the first
three deficit-seven rows separately gives the unit ideal:

```text
Q5 L_EQ_0_A_NE_0 MINIMAL (0,) UNIT 1
Q5 L_EQ_0_A_NE_0 MINIMAL (1,) UNIT 1
Q5 L_EQ_0_A_NE_0 MINIMAL (2,) UNIT 1
```

For performance, the certificates are computed in

\[
\mathbf Q[s,X]/(f)
\]

by adjoining \(f\) to each chart ideal and using Singular's exact
`modStd(...,1)` rational modular-lifting algorithm.  Since \(f\) is
irreducible, this quotient is \(K[X]\), so a unit certificate in either
presentation is exactly the same statement.  The cached certificate run
took \(14.5\) seconds for all six minimal ideals.

## Diagnosed implementation failures

Three implementation details caused or threatened the earlier direct
lift.

1. The generic substitution and chart builder take zero and one from the
   **coefficient ring**.  For the exact lift these must be
   `QuotientElement.coerce(0)` and `QuotientElement.coerce(1)`, not
   `ParameterPolynomial()` and `ParameterPolynomial(1)`.
2. Singular must receive a large algebraic coefficient as
   `(numerator/denominator)*(s^k)`.  The superficially equivalent
   `numerator*s^k/denominator` is parsed as `number^number` when the
   integer is large.
3. A direct `std` over the algebraic coefficient field suffers severe
   coefficient swell, especially if it first computes the known-proper
   deficit-six ideal.  Adjoining \(f\) in a rational polynomial ring and
   certifying the minimal deficit-seven ideals with exact `modStd`
   removes this irrelevant bottleneck.

The local cache

```text
tmp/case_c_n3_generic_charts_Q.pkl
```

stores the reconstructed outer data and the imposed exact rows.  It is
only a runtime acceleration; deleting it makes the verifier reconstruct
and recertify everything from the 64 modular bases.

## Scope

This certifies the two generic \(n=3\) charts directly in characteristic
zero.  It does not by itself treat the two special charts; those have
their separate determinant/resultant/deepest-branch arguments.  Together
with those arguments it removes the remaining dependence of the generic
chart conclusion on proper specialization.
