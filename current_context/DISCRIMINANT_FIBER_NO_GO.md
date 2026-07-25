# The cubic-discriminant fiber through the 3D collision is not an affine plane

Date: 24 July 2026

The verified three-dimensional counterexample is the marked-root cover of

\[
\mathcal P(T)=CT^3-2T^2+BT-2A.
\]

This makes the cubic discriminant the most natural genuinely nonlinear
target function to try in a dimension descent.  Its pullback is a polynomial
submersion, and its level through all three displayed collision points is
smooth and irreducible.  Nevertheless, that level has Euler characteristic
three, so it is not \(\mathbb A^2\).

## 1. Pullback of the discriminant

Write the three-dimensional Keller map as \(F=(A,B,C)\), put
\(e=1+xy\), and let

\[
\Delta(A,B,C)=\operatorname{disc}_T
  (CT^3-2T^2+BT-2A).
\]

Exact substitution gives

\[
\frac{\Delta\circ F}{4}=a z^2+bz+c,
\]

where, with \(u=xy\),

\[
\begin{aligned}
a&=9x^2(1+u)^2,\\
b&=2(27u^3+36u^2-3u-8),\\
c&=9y^2(9u^2+6u-7).
\end{aligned}
\]

The discriminant of this quadratic in \(z\) collapses to

\[
b^2-4ac=64(3u+4).                                      \tag{1}
\]

The three exact collision points all satisfy

\[
\Delta\circ F=16.
\]

The gradient ideal of \(\Delta\circ F\) is the unit ideal.  This also has a
structural explanation: the critical locus of the cubic discriminant is the
triple-root locus, whereas the marked root in the normalized factorization
cover is simple.  Thus the level

\[
S=\{\Delta\circ F=16\}
\]

is a smooth affine surface.

## 2. Euler characteristic of the collision level

Project \(S\) to the \((x,y)\)-plane.  Let

\[
E=V(a)=V(x)\sqcup V(1+xy).
\]

The two pieces are \(\mathbb A^1\) and \(\mathbb G_m\), so
\(\chi(E)=1\).  On \(x=0\) one has \(b=-16\), and on \(1+xy=0\) one has
\(b=8\).  Hence the quadratic equation has exactly one \(z\)-solution over
every point of \(E\).

By (1), the branch curve away from \(E\) is

\[
\mathcal C:\quad
64(3xy+4)+144x^2(1+xy)^2=0.                            \tag{2}
\]

It is disjoint from \(E\).  Away from \(E\cup\mathcal C\), the projection
has two points in every fiber; over \(\mathcal C\) it has one.  Additivity of
the complex constructible Euler characteristic therefore gives

\[
\chi(S)=1-\chi(\mathcal C).                             \tag{3}
\]

The branch curve is explicit.  Set \(u=xy\) and
\(v=x(1+u)\).  Equation (2) becomes

\[
9v^2=-4(3u+4),
\]

so

\[
u=-\frac43-\frac34v^2,\qquad
x=-\frac{12v}{4+9v^2}.
\]

This identifies

\[
\mathcal C\cong
\mathbb A^1\setminus\left\{0,\frac{2i}{3},-\frac{2i}{3}\right\}.
\]

This is an isomorphism, not only a birational parametrization: in the
coordinate ring of \(\mathcal C\),
\[
64=v(144y-180v-81v^3),\qquad
(4+9v^2)^{-1}=-\frac{x}{12v}.
\]
Thus both deleted factors are explicit units, and the displayed formulas
and \(v=x(1+xy)\) are inverse regular maps.  In particular
\(\mathcal C\) is reduced and irreducible.

Consequently \(\chi(\mathcal C)=-2\), and (3) yields

\[
\boxed{\chi(S)=3.}
\]

The quadratic is primitive because \(\gcd(a,b)=1\).  Its discriminant has
odd valuation along the reduced nonempty divisor \(\mathcal C\), so it is
not a square in \(\mathbb C(x,y)\).  Gauss's lemma therefore makes \(S\)
irreducible.  (The Euler characteristic used above is the constructible
compact-support Euler characteristic; for the smooth complex surface \(S\)
it equals the ordinary Euler characteristic.)  Since
\(\chi(\mathbb A^2)=1\), neither this fiber nor a component containing the
three collision points is an affine plane.

## 3. Scope

This closes the most symmetric nonlinear target-section candidate supplied
by the marked-cubic construction.  It does not rule out a different
nonlinear target coordinate, nor does it rule out finding two Darboux
functions on a non-\(\mathbb A^2\) source surface by another mechanism.

Run

```sh
.venv/bin/python current_context/verify_discriminant_fiber.py
```

for the exact polynomial identities, the collision values, the unit
gradient ideal, and the branch parametrization.
