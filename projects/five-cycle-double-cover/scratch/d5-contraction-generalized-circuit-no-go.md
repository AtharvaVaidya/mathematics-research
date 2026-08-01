# A smallest generalized-circuit orbit trap for \(D_5\) contraction

Date: 2026-07-28

## Result and scope

The following proposed contraction lemma is false.

> **Refuted orbit lemma.**  Let \(H\) be obtained by contracting an edge
> \(uv\) of a simple biconnected cubic graph, let \(w\) be the resulting
> degree-four vertex, and retain the prescribed \(u\)-side/\(v\)-side
> \(2+2\) split at \(w\).  From every \(D_5\)-flow on \(H\), switches on
> arbitrary Eulerian edge-subsets of factors \(Y_{ij}\) reach a flow whose
> side xor has weight two.

There is an exact counterexample from a 14-vertex, simple,
3-vertex-connected cubic graph.  A complete census proves there is no such
counterexample from a biconnected simple cubic graph of order at most 12.

This is a counterexample to a **reconfiguration lemma**, not to FiveCDC.
The same contracted graph has a second, much larger switch orbit containing
many good flows, and those flows extend over the restored edge.

## The parent graph and contraction

The canonical graph6 row is

```text
M?AA@BORD_CoEOAo?
```

Its edge order is

\[
\begin{array}{c|ccccccccccccccccccccc}
r&0&1&2&3&4&5&6&7&8&9&10&11&12&13&14&15&16&17&18&19&20\\ \hline
e_r&
05&16&27&08&18&38&19&49&59&0\,10&2\,10&3\,10&
2\,11&5\,11&6\,11&3\,12&4\,12&7\,12&4\,13&6\,13&7\,13 .
\end{array}
\]

Contract \(e_{15}=3\,12\).  Relabel the contracted vertex as \(0\) and
the remaining old vertices in increasing order as \(1,\ldots,12\).
The 20 edges \(h_0,\ldots,h_{19}\) inherit the old-edge order

\[
(0,1,\ldots,14,16,17,18,19,20).
\]

The two sides at the contracted vertex are

\[
 U=\{h_5,h_{11}\},\qquad V=\{h_{15},h_{16}\}.
\]

The independent checker verifies directly, without a graph library, that
the parent graph is cubic, has no bridge, remains connected after deletion
of any one or two vertices, and that the contraction has degree sequence
\(4,3^{12}\).

## One trapped flow

In contracted-edge order, take

```text
01,02,03,13,03,01,23,02,03,03,02,23,23,13,12,01,23,12,01,02
```

Direct xor at every vertex is zero.  Its boundary value is

\[
q(h_5)+q(h_{11})=01+23=0123
                    =01+23=q(h_{15})+q(h_{16}),
\]

which has weight four and therefore cannot label the restored edge.

For a coordinate pair \(p=\{i,j\}\), a generalized factor switch chooses
an arbitrary Eulerian edge-subset \(Z\subseteq Y_{ij}\) and adds
\(\mathbf1_p\) to every label on \(Z\).  The independent enumeration finds
that the orbit of the displayed state, modulo the global \(S_5\) action,
has exactly 12 states.  All 12 have side xor \(0123\), of weight four.

## The four-coordinate trap

The obstruction has a short structural core.

**Lemma.**  Suppose a \(D_5\)-flow uses four coordinates \(S\) and omits
coordinate \(t\).  If every coordinate class

\[
C_i=\{e:i\in q(e)\},\qquad i\in S,
\]

is one circuit, then no generalized factor switch can introduce the fifth
coordinate nontrivially, modulo global coordinate permutations.

**Proof.**  A switch using a pair \(p\subseteq S\) plainly retains the
missing coordinate \(t\).  For \(p=\{i,t\}\), because \(t\) is absent,

\[
Y_{it}=C_i.
\]

A circuit has only one nonempty Eulerian edge-subset: its full edge set.
Switching on all of \(C_i\) replaces \(i\) by \(t\) on every label that
contains \(i\).  This is exactly the global coordinate transposition
\(i\leftrightarrow t\), hence it is the same normalized state. \(\square\)

Every state in the 12-state orbit uses exactly four coordinates, and every
one of its four coordinate classes is a single circuit.  Thus the fifth
coordinate is locked out throughout the orbit.  Switches between the four
used coordinates give the following complete normalized adjacency
certificate; omitted moves are normalized self-loops:

\[
\begin{array}{c|l}
0&4,7\\
1&5,6\\
2&4,6\\
3&5,7\\
4&0,2,8,10\\
5&1,3,9,11\\
6&1,2,8,11\\
7&0,3,9,10\\
8&4,6\\
9&5,7\\
10&4,7\\
11&5,6
\end{array}
\]

The 12 normalized label rows, in the same state order, are:

```text
00  01,01,02,12,02,01,12,01,02,02,03,23,23,12,13,03,12,13,03,01
01  01,01,02,03,13,01,03,01,13,13,12,23,01,03,13,03,12,13,03,01
02  01,02,01,02,12,01,01,02,12,12,13,23,03,02,23,03,12,23,03,02
03  01,02,01,13,03,01,23,02,03,03,02,23,12,13,23,03,12,23,03,02
04  01,02,12,02,12,01,01,02,12,12,13,23,23,02,03,23,01,03,23,02
05  01,02,12,13,03,01,23,02,03,03,02,23,01,13,03,23,01,03,23,02
06  01,02,03,02,12,01,01,02,12,12,13,23,01,02,12,01,23,12,01,02
07  01,02,03,13,03,01,23,02,03,03,02,23,23,13,12,01,23,12,01,02
08  01,02,23,02,12,01,01,02,12,12,13,23,12,02,01,12,03,01,12,02
09  01,02,23,13,03,01,23,02,03,03,02,23,03,13,01,12,03,01,12,02
10  01,23,02,12,02,01,03,23,02,02,03,23,23,12,13,12,03,13,12,23
11  01,23,02,03,13,01,12,23,13,13,12,23,01,03,13,12,03,13,12,23
```

Each row is a literal \(D_5\)-flow.  In every row, the \(U\)-side xor and
the \(V\)-side xor are both \(0123\).  For a hand replay of closure, form
each \(Y_{ij}\) from a row.  Away from \(w\) it has degree zero or two and
at \(w\) degree zero, two, or four.  Delete one edge from every factor
cycle to obtain a spanning forest; its non-tree edges give a binary
cycle-space basis.  Switching each of the \(2^\beta-1\) nonzero basis sums
and globally renaming coordinates gives exactly the neighbours in the
table or the same row.  The checker performs precisely this calculation.

The SHA-256 digest of the 12 rows joined by newline is

```text
6aee922a63835496506597e93a1a600314b59583f28e0617e90978c9688858e3
```

## Why this is not a FiveCDC counterexample

The contracted graph has exactly 1,681 \(S_5\)-normalized \(D_5\)-flows.
Its generalized switch graph has two orbits:

\[
\begin{array}{c|cc}
\text{orbit size}&12&1669\\ \hline
\text{states with weight-two side xor}&0&968.
\end{array}
\]

Every one of the 968 good states in the large orbit extends to the original
14-vertex cubic graph by assigning its side xor to the restored edge.
Only the claim “start from **every** flow” has failed.

## Complete smaller census

For each even \(n\in\{4,6,8,10,12\}\), `geng` canonically generated every
simple biconnected cubic graph.  Every edge was marked and contracted;
edge-orbit quotienting was not used.  For every contraction, the audit:

1. enumerated every \(D_5\)-flow modulo global \(S_5\);
2. generated the full binary cycle space of every \(Y_{ij}\);
3. built the complete generalized-switch graph; and
4. tested every switch component for a weight-two state.

The combined exact totals are:

\[
\begin{array}{l|r}
\text{biconnected cubic graphs}&107\\
\text{marked contractions}&1,812\\
\text{normalized contracted flows}&878,865\\
\text{generalized switch orbits}&11,664\\
\text{bad starting flows in ultimately good orbits}&387,045\\
\text{bad-only orbits}&0\\
\text{maximum shortest switch distance to good}&4.
\end{array}
\]

The 14-vertex graph above therefore has minimum possible parent order in
this complete simple-biconnected census.  No claim is made that it is the
only order-14 example.

## Reproduction

Compile and run the general auditor:

```text
clang++ -std=c++17 -O3 \
  scratch/audit_d5_contraction_circuit_orbits.cpp \
  -o /tmp/audit_d5_contraction_circuit_orbits

geng -q -C -d3 -D3 12 18:18 /tmp/cubic12.g6
/tmp/audit_d5_contraction_circuit_orbits /tmp/cubic12.g6
```

Run the independently written fixed-witness checker:

```text
python3 scratch/check_d5_contraction_circuit_orbit_counterexample.py
```

The Python checker uses no SAT, graph, or canonical-labelling package.  It
decodes graph6, checks 3-connectivity by vertex deletion, propagates the
XOR equations, enumerates all 120 coordinate permutations, constructs
cycle bases directly, reproduces both complete orbits, and prints the
12-row closure certificate.

## Consequence for the induction route

The progression is now exact:

1. component switches preserve side-xor weight;
2. allowing arbitrary factor circuits breaks that invariant and repairs
   many examples;
3. nevertheless, even the complete generalized factor-circuit orbit can
   be trapped away from weight two.

Therefore edge contraction plus factor-circuit reconfiguration does not
give a noncircular induction from an arbitrary contracted flow.  A viable
contraction proof would need either a principled way to select the large
good orbit or a move that escapes the four-coordinate single-circuit trap.
Proving merely that some good contracted flow exists is still exactly the
extension condition for the original graph.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the generalized
orbit test, wrote the exhaustive auditors, found and minimized the
counterexample by complete smaller-order census, proved the
four-coordinate trap lemma, and drafted this note.
