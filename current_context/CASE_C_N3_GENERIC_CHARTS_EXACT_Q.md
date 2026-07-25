# Exact characteristic-zero reconstruction for the generic case-c charts

## Audited status

The exact characteristic-zero outer Hurwitz algebra and every generic
chart row through deficit seven have been reconstructed and independently
transport-checked.  Fast nonhomogeneous modular standard-basis
calculations return the unit ideal on both normalized generic charts:

\[
\boxed{\begin{aligned}
L=0,\ A\ne0&\Longrightarrow\varnothing
&&\text{by a direct exact-\(K\) certificate},\\
L\ne0&\Longrightarrow\varnothing
&&\text{by the complete finite-field projective fiber plus proper
specialization}.
\end{aligned}}
\]

The row construction is an exact calculation over the irreducible
quintic number field, not an inference from the factorization modulo
\(32003\).  However, Singular's documentation guarantees
`modStd(I,1)` as an exact standard basis for homogeneous ideals (or
local orderings), while the global nonhomogeneous calculation used
below is only a high-probability result.  Therefore the previously
reported `UNIT 1` outputs are strong computational evidence, but are not
used as exact certificates.  A new weighted-projective calculation gives
a direct exact-\(K\) proof for the second chart.  The first chart retains
the rigorous projective good-reduction proof; only the optional
strengthening to a direct exact-\(K\) remainder remains open.

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

## Provisional unit computations

The same triangular normalizations as in the modular verifier are used.

On \(L\ne0\), normalize \(L=1\), eliminate \(X_1\) and \(X_6\), and work
in the four variables

\[
X_0,X_3,X_4,X_5.
\]

All three deficit-six rows are retained.  The nonhomogeneous
`modStd(...,1)` calculation reports the unit ideal for each of the three
minimal choices of two of the first three deficit-seven rows:

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

All three deficit-six rows are again retained.  The same calculation
reports the unit ideal when any one of the first three deficit-seven
rows is added:

```text
Q5 L_EQ_0_A_NE_0 MINIMAL (0,) UNIT 1
Q5 L_EQ_0_A_NE_0 MINIMAL (1,) UNIT 1
Q5 L_EQ_0_A_NE_0 MINIMAL (2,) UNIT 1
```

For performance, these provisional computations are performed in

\[
\mathbf Q[s,X]/(f)
\]

by adjoining \(f\) to each chart ideal and using Singular's
`modStd(...,1)` rational modular-lifting algorithm.  Since \(f\) is
irreducible, a genuinely exact unit certificate in this presentation
would be exactly the desired statement in \(K[X]\).  The issue is not
the quotient presentation but the documented exactness scope of
`modStd` for a global nonhomogeneous input.  The cached provisional run
took \(14.5\) seconds for all six minimal ideals.

### Homogenized direct-\(\mathbf Q\) path

There is a logically exact way to turn a normalized affine calculation
into a direct characteristic-zero certificate.  In
\(\mathbf Q[s,X,h]\), with \(f(s)\) adjoined to the chart ideal \(J\), set

```text
ideal Jh=homog(J,h);
ideal Hh=modStd(Jh,1);
```

and test a power of \(h\) for zero remainder.  Singular
`modstd.lib` 4.4.1.4 states that `modStd(...,1)` gives the standard basis
of the input ideal when its generators are homogeneous.  Therefore a
completed calculation with \(h^N\in J^h\) would dehomogenize to
\(1\in J\); unlike the nonhomogeneous run above, this implication is
exact.

The verifier contains this path, checks `homog(Jh)==1`, and allows one
sufficient minimal row choice to run without launching the three
redundant choices concurrently.  The optimized \(L\ne0\) replay was
nevertheless stopped after a bounded audit window because the complete-
projective-fiber proof below had already closed the theorem.  No completed
`HPOWER` output is archived, so this path is **not** cited as an executed
certificate.

## Weighted-projective repair

The imposed rows before chart normalization are homogeneous for weights

\[
\deg(X_0,X_1,X_3,X_4,X_5,X_6)=(1,1,2,3,3,4);
\]

\(X_2\) has already been replaced by \((169/48)X_0^2\).  Let \(F_5\)
be the unique weight-five row, let \(F_{6,i}\) be the three weight-six
rows, and let \(F_{7,j}\) be the five weight-seven rows.  The coefficient
of \(X_6\) in \(F_5\) is the weight-one chart form \(L\).  Modulo \(L\),
the coefficient of \(X_5\) is the weight-two chart form \(A\).

Work directly over the exact number field \(K=\mathbf Q[s]/(f)\).  For
the second chart define

\[
J_{\rm II}=(L,F_5,F_{6,0},F_{6,1},F_{6,2},F_{7,0}).
\]

Singular's ordinary (non-modular) exact `std` algorithm in
\(K[X_0,X_1,X_3,X_4,X_5,X_6]\), with the weighted ordering above,
returns

```text
Q5 WEIGHTED L_EQ_0_A_NE_0 TARGET_POWER 8
Q5 WEIGHTED L_EQ_0_A_NE_0 EXACT_REMAINDER_ZERO 1
Q5 WEIGHTED L_EQ_0_A_NE_0 EXACT IN 139.2s
```

Thus

\[
A^8\in J_{\rm II}
\]

by exact polynomial reduction, so no common zero can satisfy
\(L=0,\ A\ne0\).  This proof uses neither the nonhomogeneous `modStd`
claim nor specialization modulo \(32003\).

For the first chart, modular discovery gives

\[
L^{23}\in
J_{\rm I}:=(F_5,F_{6,0},F_{6,1},F_{6,2},F_{7,0},F_{7,1})
\quad\bmod 32003.
\]

All three choices of two among \(F_{7,0},F_{7,1},F_{7,2}\) have the
same first target power \(23\).  After replacing \(X_1\) by \(L\) and
ordering \(L\) last, a weighted modular basis has only 119 elements and
contains the literal polynomial \(L^{23}\); a lexicographic elimination
basis has 280 elements and also contains literal \(L^{23}\).  Direct
exact-\(K\) versions of these fixed-target calculations were tested with
weighted `std`, `slimgb`, lexicographic elimination, targeted `lift`, and
homogeneous modular reconstruction.  None completed within the bounded
audit windows, so no direct-\(K\) \(L^{23}\) claim is made.

This does **not** reopen the characteristic-zero theorem for chart I, but
the specialization argument must be stated globally.  The open set
\(D(L)\) is not proper, and its modular emptiness alone would not prevent
a generic \(L\ne0\) point from specializing to \(L=0\).  What is proper
is the **complete** weighted-projective consistency fiber.  The modular
calculations for

\[
D(L),\quad V(L)\cap D(A),\quad
V(L,A)\cap D(B),\quad V(L,A,B)
\]

together make that entire special fiber empty.  Coefficientwise exact-to-
modular transport identifies it with a good fiber of the characteristic-
zero projective model, so properness forces the generic fiber to be empty.
See `CASE_C_FULL_CERTIFICATE_BRIDGE.md` for the assembled argument.

The \(L^{23}\) computation above is additional structural evidence and a
sharply reduced target for a future direct-\(K\) replay, not the logical
basis of the proper-specialization proof.

The standalone weighted verifier is

```text
scratch_case_c_n3_weighted_projective_Q.py
```

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
   testing the minimal deficit-seven ideals with `modStd` removes this
   bottleneck, but the resulting global nonhomogeneous unit output needs
   one of the deterministic witnesses described above.

The local cache

```text
tmp/case_c_n3_generic_charts_Q.pkl
```

stores the reconstructed outer data and the imposed exact rows.  It is
only a runtime acceleration; deleting it makes the verifier reconstruct
and recertify everything from the 64 modular bases.

## Scope

This exactly certifies the characteristic-zero outer algebra, the lower
recurrence, the generic-chart equation transport, and direct exact-\(K\)
emptiness of the \(L=0,\ A\ne0\) chart.  Together with the already
audited **complete-fiber** weighted-projective good-reduction argument,
it also certifies the \(L\ne0\) chart in characteristic zero.  What
remains unavailable is only an optional direct exact-\(K\) \(L^{23}\)
certificate, and no completed direct-\(\mathbf Q\) `HPOWER` replay is
claimed.  This memo does not by itself treat the two special charts;
those have their separate determinant/resultant/deepest-branch arguments.
