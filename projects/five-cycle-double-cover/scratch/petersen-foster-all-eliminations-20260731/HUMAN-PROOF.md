# Human proof boundary for the all-edge Petersen--Foster certificate

## 1. The parent graph

Write the Foster graph in LCF form

```text
[17,-9,37,-37,9,-17]^15.
```

Delete vertex zero.  Its three neighbours, formerly numbered `1,17,89`,
are the ports of the resulting three-pole.  Replace every vertex of the
Petersen graph by one copy of this pole and join the ports in the fixed
Petersen edge order.  Renumbering the ten copies consecutively gives the
890-vertex, 1,335-edge graph `G` reconstructed in `checker.py`.

The checker directly proves that `G` is simple, cubic, connected,
bridgeless, and has girth ten.  Its canonical ordered-edge digest is

```text
3fe0630cb52d5a0b29a473faff02389195c7e119ea8f7a6f95f3ba9c38272282
```

The graph is non-Tait.  In a Tait colouring of a cubic three-pole, the
parity lemma forces its three semiedges to have distinct colours.  A Tait
colouring of `G` would consequently induce one on the Petersen
macrograph, which is impossible.

## 2. Edge elimination

Fix an edge `e=uv` of `G`.  Since the girth is ten, the four neighbours
of `u,v` other than each other are distinct.  Delete `u,v`, add one edge
between the two remaining neighbours of `u`, and add another between the
two remaining neighbours of `v`.  Call these ordered artificial edges
`r,s`; the resulting graph is `H=G÷e` in the edge-elimination notation of
the project.

The checker performs this construction independently for every edge
index `e=0,...,1334`.  It verifies that each `H` is simple, cubic, and
bridgeless.  A cycle of `H` avoiding both artificial roots is a parent
cycle and has length at least ten.  The checker finds the shortest cycle
through either root by deleting that root and running one breadth-first
search between its endpoints.  The minimum is nine in every row, proving
the asserted reduced girth exactly.

## 3. Literal `D5` witnesses

Identify a two-subset of `{0,1,2,3,4}` with its nonzero five-bit mask.
For each reduced edge `a`, the certificate supplies one mask `q(a)`.
The checker verifies

\[
 |q(a)|=2\quad(a\in E(H)),\qquad
 \bigoplus_{a\ni v}q(a)=0\quad(v\in V(H)).
\]

For each coordinate `i`, let

\[
 C_i=\{a:i\in q(a)\}.
\]

The second displayed identity says every vertex has even degree in every
`C_i`.  Hence `C_0,...,C_4` are five Eulerian edge-subsets, and the first
identity says every edge lies in exactly two of them.  This is exactly the
standard five-cycle-double-cover formula on `H`.

For the pair `P={0,1}`, put

\[
 Y_{01}=C_0\mathbin\triangle C_1
       =\{a:|q(a)\cap\{0,1\}|=1\}.
\]

It is Eulerian; in a cubic graph its nonempty components are circuits.
The checker starts at `r`, follows the active edge incidences, and proves
that `s` lies in the same component.  It separately checks the displayed
simple edge-path from `r` to `s`.

Thus every one of the 1,335 eliminated graphs has an `(r,s)`-good `D5`
flow.  The standard two-root insertion lemma then reconstructs a `D5`
flow on the parent: subdivide `r,s`, transpose coordinates 0 and 1 along
one root-to-root arc of their common `Y_01` circuit, add back `uv`, and
label it `01`.  Internal XOR equations are unchanged; the new `01` edge
cancels the endpoint defects; all labels retain weight two.

## 4. What is computer-assisted

The preceding implications are ordinary finite graph arguments.  The
large proposition—one witness for each of 1,335 graphs—is computational.
The producer used a CNF encoding and CaDiCaL, but the retained result is
positive, so solver correctness is not part of the final trust base:
`checker.py` verifies each literal assignment directly from the graph
semantics.

The result is not an induction and does not extend beyond this named
graph.  In particular, it neither proves the universal rooted premise nor
FiveCDC.

## AI-use disclosure

OpenAI Codex agents made substantive contributions to the computation,
checker, proof organization, and prose.  This is not peer review or a
claim of autonomous mathematical authorship.  A human author must audit
the construction and accept responsibility before publication.
