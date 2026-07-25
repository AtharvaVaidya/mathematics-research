# No affine-graph descent through triangular target degree four

Date: 24 July 2026

This is a bounded extension of `QUADRATIC_TRIANGULAR_GRAPH_NO_GO.md`.
It searches all triangular target coordinates of degree at most four and
all affine source graphs through a verified collision pair.

Let \(U=A+1/4\).  The three target-coordinate orientations are

\[
U+g(B,C),\qquad B+g(U,C),\qquad C+g(U,B),
\]

where \(g\) is a completely generic polynomial in two variables, with no
constant term, of degree at most \(d\).

An affine graph through

\[
(0,0,-1/4),\qquad(1,-3/2,13/2)
\]

has the one-parameter form

\[
z=-\frac14+
\left(\frac{27}{4}+\frac32m\right)x+my.
\]

For each orientation, substitute this graph into the pullback of the target
coordinate and impose two polynomial identities:

\[
H\circ F=0,\qquad
\partial_z(H\circ F)=k.
\]

The system is saturated by \(k\), so only \(k\ne0\) is retained.  By the
three-dimensional determinant identity, any solution would restrict to a
plane polynomial map with constant nonzero Jacobian; because the graph
contains two points with the same target image, it would be an explicit
counterexample to \(JC(2)\).

The exact coefficient systems are:

| degree bound | orientation | coefficient rows | saturated basis |
|---:|---|---:|---|
| 3 | \(U+g(B,C)\) | 172 | \([1]\) |
| 3 | \(B+g(U,C)\) | 242 | \([1]\) |
| 3 | \(C+g(U,B)\) | 212 | \([1]\) |
| 4 | \(U+g(B,C)\) | 305 | \([1]\) |
| 4 | \(B+g(U,C)\) | 431 | \([1]\) |
| 4 | \(C+g(U,B)\) | 375 | \([1]\) |

Every basis is computed exactly over \(\mathbb Q\).  Thus no triangular
target coordinate through degree four descends the selected 3D collision
on an affine graph.  This is not an all-degree theorem: higher-degree target
coordinates and nonlinear source embeddings remain open.

Run:

```sh
.venv/bin/python current_context/search_bounded_triangular_affine_graph.py
```
