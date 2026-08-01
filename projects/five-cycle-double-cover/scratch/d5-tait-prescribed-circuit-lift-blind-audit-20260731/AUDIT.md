# Blind audit of the prescribed-circuit Tait lift

Date: **2026-07-31**

Verdict: **PASS, with explicit convention boundaries.**

This audit was written without relying on the producer's test code.  The
prescribed-circuit formula is correct, the root-feasibility corollary is
correct, and the insertion construction is correct on the domain used by
the minimum-counterexample reduction.  None of these statements resolves
FiveCDC.

## 1. Exact statement that was checked

Let `H` be a loopless cubic multigraph with a proper edge-colouring

\[
                 c:E(H)\longrightarrow\{2,3,4\}.
\]

Thus the three edge incidences at every vertex have distinct colours.
Let `K` be a circuit, meaning the edge set of a connected 2-regular
subgraph.  In particular, a pair of parallel edges is allowed to be a
2-circuit, but a general closed walk is not meant.  Define

\[
q(e)=
\begin{cases}
\{0,c(e)\},&e\in K,\\
\{2,3,4\}\setminus\{c(e)\},&e\notin K.
\end{cases}
\tag{1}
\]

Then every label has size two, the xor of the incident labels is zero at
every vertex, and

\[
                 Y_{01}(q)=E(K),
\qquad
Y_{01}(q):=\{e:|q(e)\cap\{0,1\}|=1\}.
\]

Parallel edges cause no problem when edges retain distinct identities.
Connectedness of `H` is not needed for this theorem.

## 2. Human-checkable proof

At a vertex not on `K`, the three incident colours are `2,3,4`, so the
three labels are `34,24,23`.  Every coordinate occurs twice and their xor
is zero.

At a vertex on `K`, exactly two incident edges belong to `K`.  Call their
distinct colours `a,b`; properness makes the third colour the remaining
element `c` of `{2,3,4}`.  The two circuit labels are `0a,0b`, while the
off-circuit label is

\[
             \{2,3,4\}\setminus\{c\}=\{a,b\}.
\]

Their xor is `(0+a)+(0+b)+(a+b)=0`.  This also covers a chord of `K`:
the chord is simply the third, off-circuit edge at each endpoint.

Coordinate `1` occurs in no label.  A label meets `{0,1}` oddly exactly
when it contains `0`, and (1) puts `0` on exactly the edges of `K`.
Therefore `Y_01(q)=E(K)`, including equality of components rather than
mere containment.

For completeness, let

\[
                   C_i=\{e:i\in q(e)\}.
\]

The vertex-xor equations say that every `C_i` has even degree at every
vertex, and every edge lies in exactly two `C_i` because every label has
size two.  Thus this is exactly a five-even-subgraph double cover, with
`C_1` empty.  Notice that `Y_01` is a coordinate-pair factor, not itself
one of the five cover members.

## 3. Why two roots lie on a suitable circuit

Assume now that `H` is 2-vertex-connected and let `r,s` be distinct
edges.  Subdivide them by vertices `x,y`.  Subdivision preserves
2-connectivity: deleting a new subdivision vertex amounts to deleting a
non-bridge edge of `H`, and deleting an old vertex leaves the subdivision
vertex attached to the surviving endpoint whenever necessary.  By the
vertex form of Menger's theorem, there are two internally disjoint
`x`-to-`y` paths.  Their union is a circuit through `x,y`.  Since each
new vertex has degree two, suppressing them gives a circuit of `H`
containing `r,s`.  Applying (1) makes that circuit exactly `Y_01`.

This proof remains valid for loopless multigraphs and for a 2-circuit
formed by parallel edges.  In the project's narrowed premise `H` is
simple and 3-edge-connected, hence 2-connected: if a cut vertex existed,
one component of `H-v` would have only one attachment to the degree-three
vertex `v`, producing a bridge.

## 4. Insertion check

Subdivide distinct roots `r,s` by `u,v`, copy each old root label to both
halves, and add the edge `uv`.  The circuit `K` becomes a circuit `K*`
through `u,v`.  Choose one `u`-to-`v` arc of `K*` and interchange
coordinates `0,1` on its edges.

Every arc edge initially has label `0c`, so it becomes `1c`; it remains
weight two and changes, as a binary vector, by `01`.  Each internal arc
vertex sees two such changes, which cancel.  Each endpoint sees one change
and therefore has defect `01`; assigning label `01` to the new edge
cancels both endpoint defects.  All other equations are unchanged.  This
proves the insertion direction needed by the induction.

The phrase "inverse edge insertion" refers to the inverse **graph
operation**.  It should not be read as an unconditional inverse map on all
flows.  The construction requires two distinct root edge identities and a
factor circuit containing both.  Those hypotheses hold in the stated
girth-ten minimum-counterexample application, where elimination produces
distinct independent roots.

## 5. Convention boundaries and nonclaims

1. **Loops.**  The theorem explicitly excludes them.  A loop contributes
   twice to vertex parity, while the displayed three-edge xor notation can
   be misread as counting it once; moreover a proper edge-colouring of a
   loop is not standard.  No looped extension was checked or inferred.
2. **Parallel edges.**  They are harmless mathematically, including
   2-circuits, provided edge identities are retained.  The producer's
   endpoint-tuple dictionaries test only simple graphs; the independent
   audit below adds parallel-edge cases.
3. **Circuit.**  It must mean a connected 2-regular edge-subgraph, not an
   arbitrary closed walk with repeated vertices or edges.
4. **Connectedness.**  It is unnecessary for the formula, but
   2-connectivity is essential for the assertion that every two distinct
   edges share a circuit.
5. **Orientability.**  No orientation is constructed or claimed.
6. **Novelty.**  This is an elementary local construction.  This audit did
   not establish priority or standalone publishability; any novelty claim
   should remain provisional pending a dedicated literature review.

## 6. Computational boundary

`independent_audit.py` uses edge IDs rather than endpoint pairs.  It
checks every circuit and every distinct edge pair in `K4` and in the
two-vertex cubic multigraph with three parallel edges, checks a
disconnected two-component parallel-edge control, converts each flow to
five coordinate subgraphs, and replays the insertion construction.  It
is supplementary to the proof above, not a substitute for it.

The producer's original `run_all.sh` also passed unchanged: six prism
controls, 1,596 edge pairs, 1,596 insertions, 8,184 abstract cyclic colour
words, and all recorded SHA-256 checks.

## AI-use disclosure

This blind audit, its proof presentation, and its checker were produced by
an OpenAI Codex agent under human direction.  It is not independent human
peer review.
