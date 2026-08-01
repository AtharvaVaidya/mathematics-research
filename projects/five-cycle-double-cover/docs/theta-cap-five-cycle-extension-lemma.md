# The theta-cap five-cycle extension lemma

Status: **human-checkable reduction with a finite exhaustive table;
excludes the terminal-distinct \(s=1\) residual branch from a
minimum-order bridgeless cubic counterexample; not a proof of
Five-CDC**.

OpenAI Codex agents, directed by Atharva Vaidya, found, checked, and
rewrote the argument and its replay program.  Agent cross-checks are not
independent human verification or peer review.

Write \(D_5=\binom{[5]}2\).  A \(D_5\)-labelling assigns one member of
\(D_5\) to each edge.  The two elements of the label specify the two
members of a five-cycle double cover containing that edge.

## Cubic local form

At a cubic vertex, the Eulerian parity equations say that every
coordinate occurs an even number of times among the three incident
two-subsets.  There are six coordinate occurrences in total.  No two
incident labels can agree: if two agreed, their symmetric difference
with the third would be the nonempty third label.  Consequently the
three labels are

\[
                         ab,\quad ac,\quad bc
\]

for three distinct coordinates \(a,b,c\).  Conversely these three
labels satisfy all five parity equations.  Thus a cubic \(D_5\)
labelling can be checked vertex by vertex by checking that the three
incident labels are the edges of a coordinate triangle.

For any shore, summing the vertex parity equations cancels the internal
edges.  Hence each coordinate has even degree in the multigraph formed
by the labels on the edge boundary.

## The cap

The seven-vertex cap has terminal vertices \(w_0,\ldots,w_4\), internal
vertices \(z_0,z_1\), and internal edges

\[
\begin{split}
&w_0w_1,\ w_2w_3,\\
&w_0z_0,\ w_2z_0,\ w_4z_0,\\
&w_1z_1,\ w_3z_1,\ w_4z_1.
\end{split}
\]

Each \(w_i\) has one dangling boundary edge.

**Lemma.** If the five dangling edges, in any order, are labelled by
the five distinct edges of a coordinate 5-cycle, the labelling extends
over all eight internal edges of this cap.

It is enough to use the canonical coordinate cycle

\[
             01,\ 12,\ 23,\ 34,\ 04.
\]

The dihedral group of this cycle has order ten.  The cap has four
automorphisms on its five terminals:

\[
\begin{split}
&(0,1,2,3,4),\quad(1,0,3,2,4),\\
&(2,3,0,1,4),\quad(3,2,1,0,4).
\end{split}
\]

Their joint action on the \(5!=120\) placements has six orbits, each of
size twenty.  The following table gives one extension in each orbit.
Boundary labels are in terminal order \(w_0,\ldots,w_4\).  Internal
labels are in the edge order

\[
(w_0w_1,w_2w_3,w_0z_0,w_2z_0,w_4z_0,w_1z_1,w_3z_1,w_4z_1).
\]

| boundary labels | internal labels |
|---|---|
| 01, 12, 23, 34, 04 | 02, 03, 12, 02, 01, 01, 04, 14 |
| 01, 12, 23, 04, 34 | 13, 03, 03, 02, 23, 23, 34, 24 |
| 01, 12, 34, 23, 04 | 14, 13, 04, 14, 01, 24, 12, 14 |
| 01, 12, 04, 23, 34 | 13, 24, 03, 02, 23, 23, 34, 24 |
| 01, 23, 12, 34, 04 | 13, 23, 03, 13, 01, 12, 24, 14 |
| 01, 23, 12, 04, 34 | 13, 02, 03, 01, 13, 12, 24, 14 |

For each row, direct inspection at the seven vertices shows that the
three incident labels form a coordinate triangle.  Coordinate
relabeling and a cap automorphism preserve that condition, proving the
remaining placements.

The standard-library replay

```sh
python3 scratch/theta_cap_boundary_language.py
```

enumerates all 60 ordered cubic local states.  It finds 6,000 ordered
boundary states for the theta cap and, independently of that language,
enumerates and verifies all 1,440 ordered labelled simple 5-cycles.  It
also constructs the six symmetry orbits and checks the displayed
witnesses.

## Consequence and limitation

If deleting a three-vertex path from a cubic graph leaves a five-pole
that admits a \(D_5\) labelling whose boundary labels form a simple
coordinate 5-cycle, replacing the path by this theta cap preserves a
standard five-cycle double cover.

The simple-cycle hypothesis is real.  The three-vertex path cap has
2,160 ordered boundary states; 120 of them do not extend through this
theta cap.  Therefore this lemma does not justify an unrestricted
replacement and does not resolve the conjecture.

## The stronger switching-attractor lemma

Although the cap does not accept every individual boundary word, it
accepts a state from every nonempty *realisable* five-pole relation.

Up to a global permutation of the five coordinates, there are 62
ordered even boundary words.  Direct elimination on the seven cap
vertices gives:

\[
              |\mathcal R_\Theta|=58.
\]

The four missing coordinate orbits have the following representatives.
For each row, \(I_{ab}\) is the set of boundary positions whose labels
contain exactly one of \(a,b\).

| missing word | \(ab\) | \(I_{ab}\) |
|---|---:|---|
| 01, 01, 02, 12, 01 | 03 | 0,1,2,4 |
| 01, 02, 01, 12, 01 | 03 | 0,1,2,4 |
| 01, 02, 12, 02, 02 | 03 | 0,1,3,4 |
| 01, 02, 12, 12, 12 | 13 | 0,2,3,4 |

In a labelled five-pole, the \(ab\)-bichromatic edges have degree zero
or two at every internal vertex.  In each row the four boundary ends
are therefore paired by two paths.  There are only three possible
pairings.  Switching \(a\) and \(b\) on either path preserves every
internal vertex equation and toggles \(a,b\) in the two endpoint
labels.

For every row and each of the three possible pairings, switching either
path gives one of the 58 theta-cap states.  This is twelve direct cases.
`theta_cap_boundary_language.py` prints all path pairings, both resulting
coordinate-orbit representatives, and an eight-edge cap witness for each
admitted state.  The frozen output is
`scratch/theta-cap-boundary-language-result.json`.  Each witness can be
checked by reading the eight internal labels in the edge order displayed
above and verifying the coordinate-triangle rule at the seven vertices.
The separately written
`scratch/theta_cap_boundary_language_independent.py` instead builds a
generic parity constraint problem from the seven named vertices.  It
reproduces all counts, the four missing words, all 24 switched ordered
words, the symmetry table, and the path-cap comparison without importing
the primary program.

It follows that:

> **Switching-attractor lemma.**  If a five-pole admits any \(D_5\)
> labelling, then it admits a \(D_5\) labelling that extends through the
> fixed ordered theta cap.

Indeed, an already admitted word needs no change.  For one of the four
missing words, the actual bichromatic path pairing is one of the three
rows just checked, and switching either of its paths reaches the cap
relation.

This explains why the 120 path-cap words missed by the theta cap do not
constitute a graph-level obstruction: the complete state relation of
the remaining pole cannot be trapped among those words.

## Minimal-counterexample consequence

Assume that a standard Five-CDC counterexample exists, reduce soundly to
the cubic case, and choose \(G\) of minimum order among all bridgeless
cubic multigraph counterexamples.  The standard minimum-counterexample
reductions in [`reductions.md`](reductions.md) then imply that \(G\) is
simple and cyclically
4-edge-connected.  It is important that minimality is taken in the full
bridgeless cubic domain, since the smaller cap below need not be
cyclically 4-edge-connected.

Suppose a cycle-separating five-edge cut has a nontrivial
factor-critical shore \(Q\), and suppose every cut edge has a different
endpoint on the other shore in the \(s=1\) one-boundary-five branch.
That outside shore has seven vertices.  Its two singleton
factor-critical components are \(z_0,z_1\); its five remaining vertices
are \(w_0,\ldots,w_4\), each incident with one cut edge.  Four of the
\(w_i\) are the endpoints of two root edges, which we name
\(w_0w_1,w_2w_3\).

Every root endpoint has one remaining incidence to
\(\{z_0,z_1\}\), while \(w_4\) has two and, by simplicity, meets both
singletons.  Each \(z_j\) has two remaining neighbours among the four
root endpoints.  If it met both ends of one root, those three vertices
would form a circuit separated by a three-edge cut from the
circuit-containing shore \(Q\), contrary to cyclic
4-edge-connectivity.  Therefore each \(z_j\) meets one end of each root.
Relabelling endpoints gives
\[
 N(z_0)=\{w_0,w_2,w_4\},\qquad
 N(z_1)=\{w_1,w_3,w_4\},
\]
which is exactly the ordered theta cap.

A connected factor-critical graph has no bridge.  For if \(uv\) were a
bridge with component orders \(a,b\), a perfect matching of \(Q-u\)
would force the component not containing \(u\) to have even order, while
a perfect matching of \(Q-v\) would force the other component to have
even order.  This contradicts the odd order of a factor-critical graph.
Ambient cubicity then makes the five boundary endpoints in \(Q\)
distinct.  A boundary vertex incident with exactly two cut edges would
have a unique internal edge, which would be a bridge of nontrivial
connected \(Q\); one incident with three cut edges would be isolated in
\(Q\).

Cap \(Q\) instead with a new 5-cycle \(c_0c_1c_2c_3c_4c_0\), joining
\(c_i\) to the \(i\)-th terminal in the same boundary order used for
\(w_i\).  The capped graph \(H\) is a simple bridgeless cubic graph with
two fewer vertices than \(G\).  Its new cycle edges lie on the cap cycle.
For every new spoke,
a path in the connected shore between its terminal and another terminal,
together with the two spokes and one of the two cap-cycle arcs, gives a
circuit through that spoke.  Every internal \(Q\)-edge already lies on
a circuit because \(Q\) has no bridge.

By the minimality of \(G\) in the full bridgeless cubic domain, \(H\)
has a standard Five-CDC.
Restriction to \(Q\) gives a nonempty \(D_5\) boundary relation.  The
switching-attractor lemma changes, if necessary, that labelling to one
accepted by the original theta cap.  Gluing the two labelings gives a
standard Five-CDC of \(G\), a contradiction.

Therefore:

> A minimum standard Five-CDC counterexample cannot lie in the
> terminal-distinct \(s=1\) one-boundary-five branch.

This does **not** exclude the \(s=1\) incidence shapes with two boundary
edges at one outside vertex, nor any of the \(s\ge2\) outside patterns.
They require an argument beyond this theta-cap lemma.  The subsequent
switching-core theorem in
[`one-boundary-five-D5-s123-reduction.md`](one-boundary-five-D5-s123-reduction.md)
excludes every retained \(s=1,2,3\) pattern.

## Prior work and novelty boundary

The \(D_5\) two-subset encoding, multipole state sets, gluing by equal
boundary labels, and bichromatic-chain switching are prior machinery.
In particular, Máčajová, Mazzuoccolo, and Trevisan introduce the
two-subset CDC-colouring language and bichromatic switches in
[*Cycle double covers of graphs with small oddness*](https://doi.org/10.26493/1855-3974.3409.c13),
Ars Mathematica Contemporanea 26 (2026), article P2.03.  The candidate
contribution requiring novelty review is
the specific ordered seven-vertex theta-cap computation
\(58/62\), the twelve-case hitting argument, and its scoped
minimum-counterexample consequence.  That priority assessment is
provisional pending specialist literature review.

The standard Five-Cycle Double Cover Conjecture remains unresolved.  No
claim here concerns the orientable variant.  This lemma itself is scoped
only to the terminal-distinct \(s=1\) branch.
