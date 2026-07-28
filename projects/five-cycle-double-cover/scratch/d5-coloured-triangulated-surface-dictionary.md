# The coloured-surface dictionary for \(D_5\)-flows

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE DICTIONARY AND FIXED-SURFACE NO-GO /
NOT A FIVECDC RESOLUTION**.

## 1. From a \(D_5\)-flow to a coloured triangulation

Let \(G\) be a loopless cubic graph and let
\[
                    q:E(G)\longrightarrow\binom{[5]}2
\]
satisfy xor zero at every vertex.

At a cubic vertex, the three incident labels are the three sides of a
unique coordinate triangle.  Indeed, if two weight-two labels have
weight-two xor, they share exactly one coordinate; the xor is the third
side of their three-coordinate union.  Equal labels would force the
third label to be zero and are impossible.

For each \(v\in V(G)\), take an abstract triangle \(\Delta_v\) whose
three vertices have those three coordinate colours and whose side
corresponding to \(e\ni v\) has endpoint-colour set \(q(e)\).  For
each graph edge \(e=uv\), glue the corresponding sides of
\(\Delta_u,\Delta_v\) by the unique colour-preserving map.

Every triangle side is paired once.  The quotient is a closed
two-dimensional pseudomanifold with a proper vertex 5-colouring and
dual graph \(G\).  A quotient vertex can have disconnected link.
Splitting one vertex into one vertex per link component produces a
genuine closed triangulated surface \(S(q)\), without changing its
triangles, edges, or dual graph.  Since \(G\) is connected, \(S(q)\)
is connected.

## 2. Coordinate cycles are primal vertex links

Put
\[
                         C_i=\{e:i\in q(e)\}.
\]
In a triangle containing colour \(i\), exactly its two sides incident
with the \(i\)-corner belong to \(C_i\).  Traversing the dual
\(C_i\)-circuit is therefore exactly traversing the link of that primal
corner through the side gluings.

Consequently the components of \(C_i\) are in bijection with the
colour-\(i\) vertices of the normalized surface.  If
\(\kappa(C_i)\) denotes the number of nonempty components, then
\[
 |V(S(q))|=\sum_{i=0}^4\kappa(C_i),\qquad
 |E(S(q))|=|E(G)|,\qquad |F(S(q))|=|V(G)|.
\]
For a cubic graph with \(n\) vertices,
\[
                  \chi(S(q))=\sum_i\kappa(C_i)-\frac n2.        \tag{1}
\]

Equivalently, the dual embedding of \(G\) is cellular and its faces are
the coordinate-link components.  Colour each such face by its
coordinate \(i\).  The colouring is proper, and \(q(e)\) is exactly the
unordered pair of colours on the two faces incident with \(e\).
Conversely, any cellular embedding of a cubic graph with a proper
five-colouring of its faces gives a \(D_5\)-flow by this rule: the three
faces at a cubic vertex have distinct colours, so the three incident
edge labels are the sides of their colour triangle.  Thus
\[
\boxed{\text{\(D_5\)-flows}
\quad\longleftrightarrow\quad
\text{properly face-5-coloured cellular embeddings of \(G\)}.}
\]

## 3. Bichromatic factors are boundary curves

Fix \(i\ne j\).  Let \(H_{ij}\) be the primal subgraph induced by the
vertices of colours \(i,j\); its edges are precisely the primal edges
with label \(ij\).  Take a sufficiently small regular neighborhood
\(N(H_{ij})\subset S(q)\).

The boundary can be checked one triangle at a time.

- If the triangle contains neither \(i\) nor \(j\), no boundary arc
  occurs.
- If it contains exactly one, the boundary arc around that corner
  crosses the two sides containing exactly one of \(i,j\).
- If it contains both, the boundary arc around their common side
  crosses the other two sides, again those containing exactly one.

After the standard dual isotopy,
\[
                       \partial N(H_{ij})=Y_{ij}
                       =C_i\mathbin\triangle C_j.               \tag{2}
\]
Thus factor circuits are literal boundary curves on \(S(q)\).

## 4. What a component switch does topologically

Let \(K\) be one component of \(Y_{ij}\).  At every dual vertex of
\(K\), the curve crosses two triangle sides; the third side is inactive
and its label contains either both or neither of \(i,j\).

Transposing \(i,j\) on the edges of \(K\) is equivalently described as
follows:

1. apply the colour transposition to every triangle traversed by \(K\);
2. keep the active side gluings, where both incident triangles are
   transformed; and
3. on an inactive \(ij\)-side with exactly one transformed incident
   triangle, compose the gluing with the endpoint flip so that it is
   colour-preserving again.

The new coloured quotient is exactly \(S(q')\) for the switched flow.
This is a reversible triangle-band recolouring and regluing surgery.
It is not, in general, a handle slide of curves on one fixed surface.

## 5. Exact cube obstruction to a fixed-surface argument

Use the cube with ordered edges
\[
\begin{array}{c|rrrrrrrrrrrr}
e&0&1&2&3&4&5&6&7&8&9&10&11\\ \hline
uv&01&03&04&12&17&23&26&35&45&47&56&67
\end{array}
\]
and Tait-derived labels
\[
             01,02,12,02,12,01,12,12,01,02,02,01.
\]
The coordinate link-component counts are
\[
                              (2,1,1,0,0).
\]
By (1), the normalized surface has
\[
                              \chi=4-8/2=0.
\]

The edges \(\{0,1,3,5\}\) are one \(Y_{12}\)-circuit.  Transpose
coordinates \(1,2\) on that circuit.  The new coordinate component
counts are
\[
                              (2,2,2,0,0),
\]
so the new connected surface has
\[
                              \chi=6-8/2=2.
\]

Thus one legal, involutive Kempe switch changes the surface Euler
characteristic by two.  Both are orientable: the surgery changes a
torus into a sphere.

There is an independent orientability change on the same cube.  Start
from labels
\[
 01,02,12,03,13,01,13,12,13,23,23,12
\]
in the same edge order.  The coordinate component counts are
\((1,1,1,1,0)\), so \(\chi=0\).  The normalized surface is
nonorientable, hence a Klein bottle.  Switch \(0,1\) on the factor
square \(\{1,2,7,8\}\).  The component counts and Euler characteristic
remain unchanged, but the new surface is orientable, hence a torus.
The checker verifies orientability by propagating triangle orientations
across every colour-preserving side gluing.

Therefore a switch can change both genus and orientability.  A
fixed-surface boundary-curve or handle-slide theorem therefore cannot
be applied to the entire Kempe orbit.

This does not rule out a proof using the reversible surface surgeries
themselves.  It identifies the exact missing theorem: one would need
connectivity of marked boundary curves under surgeries which may create
or cancel a handle, not ordinary curve slides on a fixed surface.

## 6. Reproduction

```text
python3 scratch/audit_d5_surface_euler_switch.py
```

The checker replays the local xor equations, both legal factor component
switches, all coordinate-link decompositions, the Euler
characteristics, and the orientability constraints.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived and checked the
coloured-triangulation dictionary, isolated the triangle-band surgery,
found the cube Euler-characteristic change, and drafted this note.  The
finite witness and checker are fully exposed.  This is not peer review
and is not presented as a resolution of FiveCDC.
