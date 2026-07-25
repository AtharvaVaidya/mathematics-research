# No graph descent from a quadratic triangular target coordinate

Date: 24 July 2026

Let \(F=(a,b,c):\mathbb A^3\to\mathbb A^3\) be the verified
three-dimensional Keller counterexample, with determinant \(-2\).  First
consider the triangular target coordinate

\[
H(A,B,C)=A+g(B,C),
\]

where \(g\) is any polynomial of degree at most two and \(g(0,0)=0\).  The
fiber \(H=-1/4\) contains the known collision value
\((-1/4,0,0)\) and is itself an affine plane.

This note rules out the simplest way its source fiber could contain an
affine plane carrying a plane Keller restriction: a polynomial graph

\[
z=\phi(x,y).
\]

## 1. The exact restricted-Jacobian condition

Put

\[
h(x,y,z)=a(x,y,z)+g(b(x,y,z),c(x,y,z))+1/4.
\]

Because \(a,b,c\) are linear in \(z\), \(h\) has degree at most two in
\(z\).  If \(z=\phi(x,y)\) is a component of \(h=0\), the determinant
identity for the coordinate systems

\[
(h,b,c)\quad\text{and}\quad(x,y,z)
\]

gives, up to the fixed orientation sign,

\[
h_z(x,y,\phi)\,
\operatorname{Jac}_{x,y}
\bigl(b(x,y,\phi),c(x,y,\phi)\bigr)=-2.
\tag{1}
\]

Therefore the restriction to the graph has constant nonzero Jacobian
exactly when

\[
h_z(x,y,\phi)\in\mathbb C^\times.
\tag{2}
\]

## 2. Constant normal derivative forces constant discriminant

Write

\[
h=A_2(x,y)z^2+A_1(x,y)z+A_0(x,y).
\]

If \(h(\phi)=0\) and \(h_z(\phi)=k\), then

\[
\begin{aligned}
k^2
&=(2A_2\phi+A_1)^2\\
&=A_1^2-4A_2A_0.
\end{aligned}
\tag{3}
\]

At \(x=y=0\), the specializations are \(a=z,\ b=c=0\), so
\(h=z+1/4\).  Hence (3) would have to be the polynomial identity

\[
A_1^2-4A_2A_0=1.
\tag{4}
\]

Take the completely generic quadratic

\[
g=g_{10}B+g_{01}C+g_{20}B^2+g_{11}BC+g_{02}C^2.
\]

Expanding (4) and equating its 27 nonzero \((x,y)\)-coefficient rows gives
an ideal in the five \(g_{ij}\).  Its exact Gröbner basis over
\(\mathbb Q\) is

\[
[1].
\]

Thus (4) is impossible for every quadratic \(g\).  This excludes a
polynomial graph of *any degree*; no ansatz for \(\phi\) is used.

The same calculation applies to every triangular orientation through the
collision value.  With \(U=A+1/4\), these are

\[
U+g(B,C),\qquad B+g(U,C),\qquad C+g(U,B).
\]

For the latter two orientations the constant value of the discriminant is
not fixed in advance.  The coefficient ideal is therefore saturated by
that constant, retaining exactly the nonzero-normal-derivative case.  All
three saturated ideals have exact Gröbner basis \([1]\).

As an independent smaller check, the verifier also inserts a generic affine
graph through the exact collision pair

\[
(0,0,-1/4),\qquad(1,-3/2,13/2)
\]

and directly eliminates the graph coefficients, the five coefficients of
\(g\), and the proposed normal derivative.  Those 77 equations again have
Gröbner basis \([1]\).

There is one elementary vertical affine plane through the same pair: the
cylinder over

\[
y=-\frac32x.
\]

For each of the three triangular orientations, the verifier imposes that
the source target-coordinate vanish identically on this cylinder and that
its normal derivative there be a nonzero constant.  After saturation by
that derivative, all three exact ideals again have basis \([1]\).

## Conclusion

No quadratic triangular target coordinate, in any of the three coordinate
orientations, can descend the known three-dimensional collision through a polynomial
graph component with constant restricted Jacobian.  A successful nonlinear
descent must either use a target coordinate of degree at least three or an
affine-plane component embedded in a genuinely nonlinear vertical form.

Run

```sh
.venv/bin/python current_context/search_quadratic_triangular_graph.py
```

for the exact Gröbner certificates.
