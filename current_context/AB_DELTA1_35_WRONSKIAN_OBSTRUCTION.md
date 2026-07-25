# Exact Wronskian obstruction for the final \((3,5)\) cell

Date: 25 July 2026

## Result

The last characteristic-zero a/b boundary cell is empty:

\[
\boxed{(m,n)=(3,5)\text{ cannot occur}.}
\]

Together with the earlier shear-correct five-cell audit, this eliminates
all five primitive \(\delta=1\) cells.  The earlier \(\delta=2,4\)
arguments therefore eliminate the complete a/b boundary alternative at
this scale.

This proof replaces the large modular lift by a small differential
identity and an exact characteristic-zero primary decomposition.

## 1. Retain the approximate root

Write

\[
A=h^8+a_7h^7+a_6h^6+a_5h^5+a_4h^4+h^3+a_0
\]

and retain an independent monic polynomial

\[
T=h^{12}+\sum_{i=0}^{11}b_i h^i.
\]

The triangular approximate-root equations and the three osculating
remainder equations say

\[
D=T^2-A^3,\qquad \deg D\le 8.
\]

Define

\[
W=2AT'-3A'T.
\]

The exact identity

\[
TW=AD'-3A'D
\]

shows that \(\deg(TW)\le15\).  Since \(T\) is monic of degree twelve,
successive comparison from the leading coefficient downward gives

\[
\boxed{\deg W\le3}.
\]

This inference is valid over the coefficient quotient ring even if that
ring has zero divisors: the leading coefficient of \(T\) is the unit \(1\).

## 2. Insert the marked \((3,5)\) conditions

The original boundary coordinate is

\[
B=T-b_3A+\text{constant}.
\]

The contact-\(\ge5\) closure has

\[
b_1=b_2=0,\qquad b_4=b_3a_4.
\]

The coefficient that must be nonzero in the actual cell is

\[
L=[h^5](B-B(0))=b_5-b_3a_5.
\]

The equations

\[
[h^{18}]W=\cdots=[h^{12}]W=0
\]

solve triangularly for \(b_{11},\ldots,b_5\).  Substitution leaves only
the eight rows

\[
[h^{11}]W=\cdots=[h^4]W=0
\]

in the seven variables

\[
a_0,a_4,a_5,a_6,a_7,b_0,b_3.
\]

The chart \(a_7=0\) has unit ideal over \(\mathbf Q\), so every point has
\(a_7\ne0\).

## 3. Coordinates adapted to the unique component

Put \(t=a_7\), \(u=t^{-1}\), and \(q=b_3\).  Introduce the five transverse
coordinates

\[
\begin{aligned}
x&=a_4a_7-2,\\
y&=a_7^2-4a_6,\\
z&=a_5,\\
r&=6a_0a_7+3a_4-8b_3,\\
v&=3a_7b_0+a_4b_3-6a_0.
\end{aligned}
\]

Conversely, on \(ut=1\),

\[
\begin{aligned}
a_4&=(x+2)u,&
a_6&=(t^2-y)/4,&
a_5&=z,\\
a_0&=(8q-3a_4+r)u/6,&
b_0&=(6a_0-a_4q+v)u/3.
\end{aligned}
\]

Thus this is an invertible coordinate change on the complete
\(a_7\ne0\) chart, not a one-way parametrization.

## 4. Exact radical

After the coordinate change, Singular's modular primary-decomposition
algorithm over \(\mathbf Q\), including its exact final verification,
finds two primary pieces.  Their associated primes are

\[
\mathfrak p=(z,y,x,v,r,ut-1)
\]

and the embedded prime

\[
\mathfrak p+(2tq-3,\;3u-2q).
\]

Consequently

\[
\sqrt I=\mathfrak p.
\]

The conclusion is in fact stronger than radical membership.  Reduction of
the transformed contact coefficient modulo each of the two exact primary
components is zero.  Since the primary-decomposition routine also verifies
that their intersection is the input ideal, this proves

\[
\boxed{L\in I}
\]

over \(\mathbf Q\), without rational reconstruction of a large lift.

In the original variables every solution therefore satisfies

\[
a_5=0,\qquad a_7^2=4a_6,\qquad a_4a_7=2
\]

as well as the two displayed linear relations for \(a_0,b_0\).
Substitution into the triangular formula for \(b_5\) gives \(b_5=0\).
Equivalently—and scheme-theoretically more strongly—the checked component
reductions give

\[
L=b_5-b_3a_5\in I.
\]

Thus saturation by \(L\ne0\) is empty.

## 5. Verification and correction to the earlier CRT route

Run:

```bash
.venv/bin/python route_bd_ab_delta1_35_wronskian.py
```

The verifier checks the differential identity, triangular Wronskian
descent, empty \(a_7=0\) chart, invertible localized coordinate change,
exact primary decomposition over \(\mathbf Q\), and zero reduction of
the contact lead modulo every primary component.

The earlier 2,037-term modular lift should not be used as a
coefficientwise CRT certificate.  Its multiplier module has nontrivial
syzygies, so raw lifts at different primes need not be coordinates of one
rational lift even when their monomial supports agree.  A canonical
syzygy-reduced reconstruction is a valid independent route, but it is no
longer needed for the theorem above.
