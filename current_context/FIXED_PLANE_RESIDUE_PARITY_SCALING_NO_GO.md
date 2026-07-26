# Fixed-plane residue parity is not invariant under rational canonical scaling

Date: 25 July 2026

## Audited conclusion

The residue-parity conjecture in `FIXED_PLANE_RESIDUE_PARITY.md`, as
stated for arbitrary rational descended Darboux pairs, is false.
Rational canonical scalings which are the identity on the conductor and
have zero added residue at the distinguished \(I=\infty\) endpoint can:

1. create nonintegral residues of \((3/2)\beta\); or
2. keep every residue integral while changing its mod-two divisor class
   away from \(\operatorname {div}(x/c)\).

The construction is exact and nonmonomial.  It preserves the Darboux
equation, conductor descent, the conductor boundary values, and
\(\operatorname {Res}_{c=0}(u\,dw)=2/3\).  What it does not preserve is
global polynomiality: it introduces pole divisors on interior level
curves of \(I=AB\).

Thus tame symbols, the quadratic conductor sign line, and endpoint
residues cannot by themselves prove the proposed quantization.  A valid
replacement theorem must use the absence of every additional affine
pole divisor, or an equivalent global polynomial/termination property.

## 1. The rational descended model

Use the exact rational pair from
`verify_fixed_plane_rational_conductor_model.py`:
\[
\begin{aligned}
x&=v^2,\qquad y=v(v^2-9c),\\
A&=\frac{x^3}{6561c^2},\\
B&=-\frac{243cy}{2x^3}-\frac{2}{3A}.
\end{aligned}
\tag{1}
\]
It satisfies
\[
dA\wedge dB=dt\wedge dc,\qquad
t=\frac{v+2}{3c}.
\tag{2}
\]
Put
\[
I=AB
=-\frac{-9cv+36c+v^3}{54c}.
\tag{3}
\]
On the conductor \(c=v^2/9\),
\[
I=-\frac23,\qquad
A=\frac c9,\qquad B=-\frac6c.
\tag{4}
\]
The Liouville difference is
\[
\beta=A\,dB-t\,dc
=dS+2\,d\log\left(\frac{x}{c}\right),
\qquad
S=-\frac56v+\frac{v^3}{54c}.
\tag{5}
\]
In particular
\[
\operatorname {Res}_{c=0}(A\,dB|_C)=\frac23.
\tag{6}
\]

## 2. A general canonical-scaling lemma

Let \(f(T)\in\mathbf Q(T)^\times\), and define
\[
U=A f(I),\qquad V=\frac{B}{f(I)}.
\tag{7}
\]
Since \(I=AB\),
\[
dU\wedge dV=dA\wedge dB
\tag{8}
\]
and
\[
U\,dV-A\,dB=-I\,d\log f(I).
\tag{9}
\]
If \(f(-2/3)=1\), then (4) shows that \(U,V\) have exactly the same
conductor restrictions as \(A,B\), so (6) is unchanged.  Because
\(U,V\) are rational functions of the descended pair \(A,B\), they
remain in the fixed-plane pinch fraction field and remain fixed by the
conductor descent.

Factor
\[
f(T)=C\prod_i(T-a_i)^{n_i}.
\]
Modulo an exact differential, (9) is
\[
-I\,d\log f(I)
\equiv-\sum_i n_i a_i\,d\log(I-a_i).
\tag{10}
\]
Thus the residue on \(I=a_i\) is
\[
-n_i a_i.
\tag{11}
\]
The tame symbol records the integer order \(n_i\), but the additive
Liouville residue also contains the freely chosen action value \(a_i\).
There is no integrality mechanism in ordinary divisor theory or
algebraic \(K\)-theory which quantizes these rational constants.

The added residue at the \(I=\infty\) valuation is
\[
\sum_i n_i a_i.
\tag{12}
\]
Consequently a symmetric scaling
\[
f_{a,b}(I)
=C\frac{I^2-a^2}{I^2-b^2}
\tag{13}
\]
is endpoint-residue neutral: its four action values have sum zero.
Choose \(C\) so that \(f_{a,b}(-2/3)=1\).  If
\(\pm a,\pm b\ne-2/3\), it is also a unit on the conductor.

## 3. Exact failure of residue integrality

Take
\[
a=\frac15,\qquad b=\frac14
\tag{14}
\]
in (13), with the conductor-normalizing constant \(C\).
The four new residues of \((3/2)\beta\) are
\[
-\frac3{10},\quad \frac3{10},\quad
\frac38,\quad-\frac38
\tag{15}
\]
on
\[
I=\frac15,\quad I=-\frac15,\quad
I=\frac14,\quad I=-\frac14,
\]
respectively.  They are nonintegral.  Equations (8), (12), and
\(f(-2/3)=1\) show that this pair is nevertheless symplectic,
conductor-fixed, boundary-residue preserving, and neutral at the
distinguished infinity valuation.

This disproves part 1 of the residue-parity conjecture under its stated
rational hypotheses.

## 4. Integral residues with the wrong parity class

The failure is not merely a denominator issue.  Take instead
\[
a=2,\qquad b=\frac43,\qquad
f(I)=\frac38\,\frac{I^2-4}{I^2-16/9}.
\tag{16}
\]
Since \(I|_C=-2/3\), the factor \(3/8\) gives
\[
f(-2/3)=1.
\tag{17}
\]
The new residues of \((3/2)\beta\) at
\[
I=2,\quad I=-2,\quad I=\frac43,\quad I=-\frac43
\]
are
\[
-3,\quad3,\quad2,\quad-2.
\tag{18}
\]
They are all integral, and their sum is zero.

Combining (5), (9), and (16), the logarithmic part of the scaled form is
\[
\begin{aligned}
\frac32\beta_f
\equiv{}&
3\,d\log(x/c)
-3\,d\log(I-2)+3\,d\log(I+2)\\
&+2\,d\log(I-4/3)-2\,d\log(I+4/3).
\end{aligned}
\tag{19}
\]
Modulo two, (19) has square class
\[
\left[\frac{x}{c}(I^2-4)\right].
\tag{20}
\]
It is not \([x/c]\).  Indeed,
\[
\begin{aligned}
I-2&=-\frac{v^3-9cv+144c}{54c},\\
I+2&=-\frac{v^3-9cv-72c}{54c},
\end{aligned}
\tag{21}
\]
and both numerators are irreducible in \(\mathbf Q[v,c]\): each is
primitive and linear in \(c\), with coprime coefficients.  Their prime
divisors occur oddly in (20) and are not components of
\(\operatorname {div}(x/c)\).

Equivalently, after cancelling square factors, (20) is represented by
the product of the two new irreducible level divisors, up to a nonzero
constant.  This disproves part 2 of the conjecture even inside the
subclass for which all residues of \((3/2)\beta\) are integral.

## 5. What endpoint regularity can still mean

The symmetric construction is stronger than mere regularity of \(f\) at
the conductor:

- \(f(-2/3)=1\), so the two conductor functions and their boundary
  action are unchanged;
- the first moment (12) is zero, so the Liouville form gains no residue
  at the \(I=\infty\) valuation; and
- \(f(I)\) tends to a nonzero constant as \(I\to\infty\), so the leading
  endpoint pole orders of the two coordinates are unchanged.

Nevertheless \(V=B/f(I)\) has new poles on \(I=\pm b\).  These are
genuine affine level divisors.  The construction therefore does not
give a polynomial pair in the pinch ring, and it is not a Keller
counterexample.

This identifies the precise scope of the no-go.  If “global polynomial
endpoint regularity” means only the conductor values, endpoint pole
orders, and endpoint Liouville residues, then (16) already satisfies it
and parity is false.  If it means \(U,V\in R\), or equivalently forbids
all additional affine pole divisors, then the scaling countermodel is
excluded—but that global pole-freeness is the substantive missing
hypothesis.  It is not a consequence of the quadratic conductor,
Maslov parity, or tame symbols.

The robust statement left by this audit is weaker:

> Endpoint-neutral rational symplectic transformations can move the odd
> residue class onto arbitrary interior level divisors.  Any polynomial
> obstruction must prove that no such interior divisor can occur, rather
> than trying to quantize residues from conductor descent alone.

Companion verifier:

```text
.venv/bin/python current_context/verify_fixed_plane_residue_parity_scaling_no_go.py
```
