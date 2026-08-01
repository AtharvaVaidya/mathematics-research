# Reduction ledger

Status: the elementary derivations below passed an independent proof-agent
audit and exhaustive local checks.  Published stronger girth/oddness results
are cited separately in `docs/current-status.md`.

## Basic equivalences

- Components combine coordinatewise, and covers restrict to components.
- Loops can be deleted and restored with any pair label.
- Isolated vertices are irrelevant.
- Subdivision preserves 5-CDC in both directions; a degree-two inserted
  vertex forces its two segment labels to agree.
- An even whole edge set gives the cover \(E,E,\varnothing,\varnothing,
  \varnothing\).
- A proper cubic 3-edge-coloring gives the labels \(12,13,23\).

## Reduction of existence to simple cubic graphs

The sound direction needed for search is:

\[
\text{some finite bridgeless counterexample exists}
\Longrightarrow
\text{some simple bridgeless cubic counterexample exists}.
\]

Delete loops and isolated vertices and select a counterexample component.
The remaining loopless bridgeless graph has nonloop degree at least two.
Replace a degree-\(d\) vertex by a cubic port gadget:

- for \(d\ge3\), a \(d\)-cycle with one original incidence attached at each
  cycle vertex;
- for \(d=2\), \(K_4\) minus one edge, using its two nonadjacent degree-two
  vertices as ports.

Assign distinct incidences to distinct ports.  This produces a simple cubic
graph even when the original graph has parallel edges.  Gadget edges lie on
gadget circuits.  An external edge lies on a lifted original circuit, so the
new graph is bridgeless.

If the expanded graph had a 5-CDC, restrict the five edge sets to the
external/original edges.  Summing a coordinate's parity equations over one
port gadget cancels each internal edge twice and leaves even parity on the
original incidences.  Exact double coverage is inherited.  Hence a cover of
the expansion would give a cover of the original graph, proving the displayed
implication by contraposition.

This transformation generally increases order.  It does not prove that the
smallest unrestricted counterexample is cubic.

## Minimum cubic counterexample

Assume a counterexample exists and choose a minimum-order bridgeless cubic
multigraph counterexample \(Q\).  Minimum order and minimum edge count agree
inside the cubic class.

### Two-edge cuts

For a cut \(\{a_1b_1,a_2b_2\}\), cap the two shores by \(a_1a_2\) and
\(b_1b_2\).  Both capped graphs are smaller bridgeless cubic multigraphs.
Their cap labels can be matched by \(S_5\), which is transitive on the ten
pair labels.  Delete the caps and restore both cut edges with the common
label.  Thus \(Q\) has no two-edge cut.

This excludes double parallel edges, except for the three-parallel-edge
two-vertex graph, which is 3-edge-colorable.  A connected bridgeless cubic
counterexample has no loop.  Hence \(Q\) is simple.

### Nontrivial three-edge cuts

Cap each shore of a three-edge cut by one new cubic vertex.  Each cap's
ordered three labels form a \(K_5\)-triangle.  Every prescribed bijection
between two triangle edge triples is induced by an \(S_5\) permutation.
Align, delete the cap vertices, and restore the original cut edges.  Hence
\(Q\) has no nontrivial three-edge cut and is cyclically
4-edge-connected.

### Triangles

Contract a triangle to a cubic vertex.  Given a cover of the smaller graph,
its three external labels are the edges \(P_1,P_2,P_3\) of a coordinate
triangle.  On expansion, label each internal triangle edge by the external
label opposite it.  Every expanded vertex sees the same coordinate triangle.
Thus a minimum cubic counterexample is triangle-free.

### Four-cycles

After triangle exclusion a four-cycle is chordless.  Delete its vertices,
leaving four terminal neighbors \(u_1,\ldots,u_4\).  In the remaining
connected graph, every bridge induces the same two-plus-two terminal split.
Choose one of the two adjacent pairings

\[
\{\{1,2\},\{3,4\}\},\qquad
\{\{2,3\},\{4,1\}\}
\]

that crosses this split, and add the two corresponding smoothing edges.
The resulting smaller cubic multigraph is bridgeless.

Let the smoothing labels be \(A,B\), so the four external labels on restoring
the square occur as \(A,A,B,B\).  Choose a two-subset \(T\) as follows:

- if \(A=B\), let \(T\) meet \(A\) once;
- if \(|A\cap B|=1\), take \(T=B\);
- if \(A\cap B=\varnothing\), take one element from each.

Label the square edges in order by

\[
T,\quad T\triangle A,\quad T\triangle A\triangle B,\quad
T\triangle A.
\]

All are two-subsets, and consecutive symmetric differences are
\(A,A,B,B\).  This extends the cover, so a minimum cubic counterexample has
no four-cycle.

These audited elementary reductions justify the usual strict-snark search
domain (simple cubic, non-3-edge-colorable, cyclically 4-edge-connected,
girth at least five).  They do not justify cyclic connectivity five or
higher.

## Stronger sourced restrictions

Huck's computer-assisted reducible-configuration result gives girth at least
10 for a smallest 5-CDC counterexample.  Huck also proves every bridgeless
cubic graph of oddness at most four has a 5-CDC.  These source-backed
restrictions may be used for minimum-counterexample search after recording
their imported-theorem status; this project has not recreated their original
computer proof.
