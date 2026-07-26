# Human-checkable countermodel to the every-flow value-class lemma

This note disproves the following proposed strengthening:

> For every nowhere-zero \(\mathbb F_2^3\)-flow on a bridgeless cubic graph,
> at least one of its seven nonzero value classes is an exact-zero matching
> whose complement packs two edge-disjoint \(T\)-joins.

It does **not** disprove the five-cycle double cover conjecture.

## The graph and flow

Number the fifteen edges as follows:

| edge | endpoints | value |
|---:|:---:|---:|
| 0 | 03 | 7 |
| 1 | 06 | 6 |
| 2 | 07 | 1 |
| 3 | 14 | 7 |
| 4 | 16 | 3 |
| 5 | 17 | 4 |
| 6 | 25 | 6 |
| 7 | 27 | 5 |
| 8 | 28 | 3 |
| 9 | 36 | 5 |
| 10 | 39 | 2 |
| 11 | 48 | 1 |
| 12 | 49 | 6 |
| 13 | 58 | 2 |
| 14 | 59 | 4 |

Every vertex appears in three rows, so the graph is cubic.  The graph6
record is `ICOef?kF?`.  Deleting any one row leaves the displayed graph
connected; this is a short direct bridgelessness check.

Use bitwise xor for addition in \(\mathbb F_2^3\).  At vertices \(0,\ldots,9\)
the triples of incident values are respectively

\[
\begin{split}
&(7,6,1),\ (7,3,4),\ (6,5,3),\ (7,5,2),\ (7,1,6),\\
&(6,2,4),\ (6,3,5),\ (1,4,5),\ (3,1,2),\ (2,6,4).
\end{split}
\]

Each displayed triple has xor zero and contains no zero, proving directly
that the edge values form a nowhere-zero flow.  The seven value classes are

\[
\begin{array}{c|c}
k&M_k\\ \hline
1&\{2,11\}\\
2&\{10,13\}\\
3&\{4,8\}\\
4&\{5,14\}\\
5&\{7,9\}\\
6&\{1,6,12\}\\
7&\{0,3\}.
\end{array}
\]

Their endpoints are visibly distinct in each row, so every \(M_k\) is a
matching.  Quotienting the flow by \(\langle k\rangle\) gives an
\(\mathbb F_2^2\)-flow with exact zero set \(M_k\).

## Why none of the seven matchings packs

For a matching \(M\), put \(T=\partial M\).  The elementary even-marked
circuit criterion says that \(G-M\) packs two edge-disjoint \(T\)-joins
exactly when it contains a binary cycle \(Q\) which uses both remaining
edges at every vertex of \(T\), and every circuit component of \(Q\)
contains an even number of vertices of \(T\).

The following table gives every binary cycle satisfying the forced-edge
condition.  An empty entry means that there is none.  Each edge set in the
table can be checked by reading degrees from the fifteen-row incidence
table above.  Completeness is checked by putting variables \(q_e\) on the
edges, fixing \(q_e=0\) on \(M_k\), fixing the other two incident variables
to one at every terminal, and applying the ten equations
\(\bigoplus_{e\ni v}q_e=0\).  Straight propagation gives exactly the listed
solutions.

| \(k\) | possible circuit components of \(Q\) | terminal counts |
|---:|:---|:---:|
| 1 | \(\{0,1,9\}\), \(\{3,5,7,8,12,13,14\}\) | \(1,3\) |
| 2 | \(\{0,1,9\}\), \(\{6,8,11,12,14\}\) | \(1,3\) |
| 2 | \(\{0,2,4,5,9\}\), \(\{6,8,11,12,14\}\) | \(1,3\) |
| 3 | \(\{0,1,9\}\), \(\{3,5,6,7,11,13\}\) | \(1,3\) |
| 4 | none | -- |
| 5 | none | -- |
| 6 | none | -- |
| 7 | none | -- |

Thus every possible \(Q\) for values 1, 2, or 3 has two circuit
components with odd terminal counts, and for values 4 through 7 no
forced-edge binary cycle exists.  The criterion excludes two disjoint
\(T\)-joins for every \(M_k\).

There is a completely separate brute-force check.  Enumerating all edge
subsets of \(G-M_k\) gives respectively

\[
16,16,16,16,16,8,16
\]

\(T\)-joins.  For each \(k\), every pair of these joins shares at least one
edge.  `independent_checker.py` performs this literal enumeration without
using the circuit criterion or the search implementation.

## Why this is not a five-CDC counterexample

The edge colours

\[
(0,1,2,2,0,1,1,0,2,2,1,1,0,0,2)
\]

give the three colours exactly once at each vertex.  For each colour,
take the union of the other two colour classes.  These three Eulerian edge
sets cover every edge twice; append two empty sets.  Hence the graph has an
explicit standard five-cycle double cover.

The conclusion is only that an arbitrary nowhere-zero
\(\mathbb F_2^3\)-flow need not expose a usable value class.  A surviving
proof route must choose or modify the flow.

## AI-use disclosure

OpenAI Codex agents proposed the value-class lemma, found this finite
countermodel, wrote the programs, and drafted this proof under human
direction.  The arithmetic and graph checks are deliberately small enough
for direct human verification.  No claim should be published without a
human checking the incidence table, the short parity enumeration, and the
attribution.
