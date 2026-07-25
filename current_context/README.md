# July 2026 three-dimensional counterexample: relevance to the plane

This note records current context that postdates much of the plane-Jacobian
literature. It is not a solution of the two-dimensional problem.

## Exact three-dimensional construction

For

\[
\begin{aligned}
a&=(1+xy)^3z+y^2(1+xy)(4+3xy),\\
b&=y+3x(1+xy)^2z+3xy^2(4+3xy),\\
c&=2x-3x^2y-x^3z,
\end{aligned}
\]

direct symbolic calculation gives

\[
\det \frac{\partial(a,b,c)}{\partial(x,y,z)}=-2.
\]

The three distinct rational points

\[
(0,0,-1/4),\qquad (1,-3/2,13/2),\qquad
(-1,3/2,13/2)
\]

all map to \((-1/4,0,0)\). Thus the general Jacobian conjecture is false
in dimension three, while this says nothing by itself about dimension two.

## Hyperbolic quotient

For the grading with source invariants

\[
u=xy,\qquad v=x^2z,
\]

put

\[
L=2-3u-v,\qquad
M=v(1+u)^2+u^2(4+3u).
\]

The target invariants \(P=bc,\ Q=ac^2\) are

\[
P=L(u+3M),\qquad Q=L^2(1+u)M,
\]

and their exact quotient Jacobian is

\[
\frac{\partial(P,Q)}{\partial(u,v)}=2L^2.
\]

The map contracts the line \(L=0\) to \((0,0)\). The square factor is the
mechanism that permits the three-dimensional determinant to remain constant;
the quotient itself is not a plane Keller map.

## Why the direct target slice does not descend

The inverse image of the target plane \(c=0\) is reducible:

\[
c=xL=0.
\]

On \(x=0\), the restriction is the triangular automorphism

\[
(y,z)\longmapsto(z+4y^2,y).
\]

The two other collision points lie on the component \(L=0\), which is
\(\mathbb G_m\times\mathbb A^1\), not an affine plane. In coordinates
\((x,u)\), with \(x\ne0\),

\[
a=\frac{(u+1)(u+2)}{x^2},\qquad
b=\frac{4u+6}{x},\qquad
\frac{\partial(a,b)}{\partial(x,u)}=\frac{2}{x^4}.
\]

Thus the most direct two-dimensional slice is Laurent and has variable
ordinary Jacobian. It does not supply a polynomial map
\(\mathbb A^2\to\mathbb A^2\).

The most symmetric nonlinear target section fails as well.  For
\[
\Delta(A,B,C)=\operatorname{disc}_T(CT^3-2T^2+BT-2A),
\]
the pullback \(\Delta\circ F\) is a polynomial submersion and all three
collision points lie on its level \(16\).  That level is smooth and
irreducible, but an exact two-sheeted projection calculation gives Euler
characteristic \(3\), so it is not \(\mathbb A^2\).  See
`DISCRIMINANT_FIBER_NO_GO.md`.

The fixed source plane now has a sharper global obstruction candidate.
Its conductor completion admits an exact formal Darboux pair, so local
parity and completion arguments alone cannot work.  Rational descended
charts instead retain a logarithmic class in the one-dimensional kernel
\[
\ker\bigl(H^1_{\rm dR}(X^\circ)\to H^1_{\rm dR}(C^\circ)\bigr)
=\mathbf Q\,d\log(x/c).
\]
Both natural monomial orientations land in a nonzero odd residue coset.
The remaining question is whether every nonmonomial descended chart has
the same parity.  See `FIXED_SOURCE_PLANE_ROUTE.md`, Sections 1.3--1.5.

An independent all-degree formulation is recorded in
`STANDARD_SYSTEM_WEIGHTED_ESCAPE.md`.  In the finite standard system
equivalent to a counterexample, the equation-Jacobian has exact weight
\((m-1)(n-1)\) and is a nonzero constant along a Keller section.  The
natural degeneration forces that section to escape to weighted infinity,
so the missing theorem is a classification of boundary arcs rather than
an affine monodromy or larger Groebner calculation.

On the independent Danielewski-surface route, changing the affine-plane
chart cannot rescue a Chebyshev étale endomorphism.  A preserved boundary
line would make its \(z\)-coordinate satisfy a polynomial semiconjugacy
with an affine-linear self-map, forcing that coordinate to be constant.
The four resulting lines are then separated by their Picard classes and
explicit inverse images.  Thus no degree-\(d>1\) Chebyshev map, nor any
surface-automorphism conjugate of one, preserves an \(\mathbb A^2\) chart;
see `route_c/ROUTE_C_MEMO.md`.

Run `python current_context/verify_3d_descent.py` with SymPy available to
check every displayed identity exactly.

## Primary current reference

T. Shaska, *Graded Keller maps and the Jacobian Conjecture*,
[arXiv:2607.20210](https://arxiv.org/abs/2607.20210), submitted
22 July 2026. The paper also proves that every
\(\mathbb G_m\)-equivariant plane Keller map is an automorphism, so a plane
counterexample cannot be obtained by copying the grading of the
three-dimensional construction unchanged.
