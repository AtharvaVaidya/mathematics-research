# A nonlinear target-section family also cannot descend the 3D collision

Date: 24 July 2026

The linear-section obstruction leaves open nonlinear target coordinates.
This note eliminates an infinite triangular family chosen so that the
quotient cubic has a polynomial root.

## 1. The polynomial-root family

Let \(h(B,C)\in\mathbb C[B,C]\) satisfy

\[
h(0,0)=\varepsilon/2,\qquad \varepsilon\in\{+1,-1\},
\]

and define

\[
g(B,C)
=h(B,C)^2-\frac12B\,h(B,C)-\frac12C\,h(B,C)^3-\frac14.
\]

Then \(g(0,0)=0\), and

\[
(A,B,C)\longmapsto(H,B,C)
=\bigl(A+g(B,C),B,C\bigr)
\]

is a triangular polynomial automorphism of the target.

The special target graph \(H=-1/4\) contains the common collision value
\((-1/4,0,0)\). In the invariant cubic

\[
s^3-2s^2+BC\,s-2AC^2=0,
\]

the graph equation

\[
A=-\frac14-g(B,C)
\]

makes

\[
s=C\,h(B,C)
\]

a polynomial root. This is the simplest nonlinear attempt to split off a
sheet of the new three-dimensional cover before restricting to a surface.

## 2. Exact source factorization

On the source, put

\[
e=1+xy,\qquad t=h(b,c).
\]

The exact identity

\[
2\bigl(a+g(b,c)+1/4\bigr)=D_tR_t
\tag{1}
\]

holds, where

\[
D_t=e-xt
\]

and

\[
\begin{aligned}
R_t={}&-t^2x^2z-3t^2xy+2t^2
-tx^2yz-3txy^2\\
&-txz-ty+2x^2y^2z+6xy^3+4xyz+8y^2+2z.
\end{aligned}
\]

This factorization is the source-level version of the polynomial root of
the quotient cubic.

Because \((H,b,c)\circ F\) is again a three-dimensional Keller map,
\(H\circ F\) has nowhere-vanishing differential. Therefore its fiber
\(D_tR_t=0\) is smooth. The two factors cannot have a common zero: at such a
point the gradient of their product would vanish. Hence

\[
(D_t,R_t)=(1)
\]

in the source polynomial ring, and \(D_t\) is a unit on every component of
\(R_t=0\).

## 3. The collision distribution

Let

\[
\begin{aligned}
p_0&=(0,0,-1/4),\\
p_+&=(1,-3/2,13/2),\\
p_-&=(-1,3/2,13/2).
\end{aligned}
\]

For \(\varepsilon=+1\), the values are

\[
\begin{array}{c|ccc}
&p_0&p_+&p_-\\ \hline
D_t&1&-1&0\\
R_t&0&0&2.
\end{array}
\]

Thus \(R_t=0\) contains the exact collision pair \(p_0,p_+\), while
\(D_t=0\) contains \(p_-\).

For \(\varepsilon=-1\),

\[
\begin{array}{c|ccc}
&p_0&p_+&p_-\\ \hline
D_t&1&0&-1\\
R_t&0&2&0,
\end{array}
\]

so \(R_t=0\) contains \(p_0,p_-\).

On the component containing the collision pair, \(D_t\) is therefore a
unit taking the two different values \(1\) and \(-1\). It is a nonconstant
unit. No such component can be isomorphic to \(\mathbb A^2\).

If the two displayed points lie on different irreducible components of
\(R_t=0\), then no component contains that collision pair in the first
place. Thus in either case no affine-plane component carries the known
noninjectivity.

## Conclusion

No triangular target coordinate of the displayed polynomial-root family
turns the verified three-dimensional collision into a plane Keller
counterexample. The obstruction is structural: splitting the invariant
cubic forces a reducible smooth source fiber, and the complementary factor
becomes a nonconstant unit on the component containing two collision points.

This still leaves nonlinear target coordinates for which the invariant cubic
has no polynomial root.

Run:

```sh
.venv/bin/python current_context/verify_triangular_sections.py
```

to check the universal factorization and all collision values exactly.
