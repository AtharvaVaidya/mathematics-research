# A global minimum support that does not pack

Publication status: public, independently reproducible research artifact.

Status: **exact finite counterexample to “every global minimizer packs”**.
It is **not** a counterexample to the existential statement “some global
minimizer packs,” and it is not a counterexample to FiveCDC.

The graph is the connected simple cubic graph

```text
U??????_A?E?I?B@A_Os?GoBA?A@_C@O?D_??U??
```

with indexed edges

```text
 0  0-9    1  1-10   2  2-11   3  3-11   4  2-12   5  4-12
 6  4-13   7  5-13   8 11-13   9  3-14  10  5-14  11 12-14
12  3-15  13  4-15  14  6-15  15  2-16  16  6-16  17  7-16
18  0-17  19  1-17  20  6-17  21  1-18  22  8-18  23  9-18
24  0-19  25  8-19  26 10-19  27  5-20  28  7-20  29  8-20
30  7-21  31  9-21  32 10-21
```

The standard-library checker proves by complete enumeration of the
`4096^2 = 16,777,216` ordered binary-cycle pairs that the least possible
exact-zero support of an \(\mathbb F_2^2\)-flow has size two.  It finds
19,440 ordered minimum states and 222 distinct minimum supports.  This
also lower-bounds any designated value class in a nowhere-zero
\(\mathbb F_2^3\)-flow: quotienting by that value produces an
\(\mathbb F_2^2\)-flow whose exact-zero set is precisely the class.

## Literal minimum flow

In edge order `0,...,32`, take the nowhere-zero conserved
\(\mathbb F_2^3\)-flow

```text
5 3 6 5 1 3 1 2 3 3 1 2 6 2 4 7 2 5 7 1 6 2 1 3 2 3 1 3 1 2 4 6 2
```

Its exact value-4 class is

```text
M = {14,30}.
```

Thus \(T=V(M)=\{6,7,15,21\}\), and \(K=G-M\).

## Short human proof that this minimum support does not pack

Suppose \(J_1,J_2\subseteq E(K)\) were edge-disjoint \(T\)-joins, and put
\(C=J_1\cup J_2\).  Each terminal has degree two in \(K\).  Each join has
odd degree there, so the two joins must use the two incident edges, one
each.  Hence \(C\) is an even subgraph and contains edges
`16,17,20,28` (among the other forced terminal edges).

Vertex 16 has incident edges `{15,16,17}`.  Since `16,17` lie in the even
subgraph \(C\), edge `15` does not.

For

```text
S' = {2,3,4,5,6,11,12,13,14,15,16}
```

the cut in \(K\) is `{17,20,27}`.  Every even subgraph crosses every cut
evenly.  Since `17,20` lie in \(C\), edge `27` does not.

On the other hand, for

```text
S = {2,3,4,5,11,12,13,14,15}
```

we have \(S\cap T=\{15\}\) and

```text
delta_K(S) = {15,27}.
```

Every \(T\)-join crosses this \(T\)-cut oddly.  Consequently each of the
two edge-disjoint joins must use one of `15,27`, forcing both edges into
\(C\).  This contradicts the preceding two parity deductions.  Therefore
the global minimum support `{14,30}` does not pack.

The checker also verifies the equivalent complete binary-cycle test: all
64 possible even subgraphs through the terminal-incident edges fail.  Of
these, 48 have circuit terminal profile `(1,3)` and 16 have profile
`(1,1,2)`.

## A packing global co-minimizer one neutral switch away

Switch flow value `1` on the binary cycle

```text
{2,3,12,14,15,16}.
```

The resulting nowhere-zero flow is

```text
5 3 7 4 1 3 1 2 3 3 1 2 7 2 5 6 3 5 7 1 6 2 1 3 2 3 1 3 1 2 4 6 2
```

and its exact value-4 class is the size-two global co-minimizer

```text
M' = {3,30},   T' = {3,7,11,21}.
```

It packs, as witnessed by the following two edge-disjoint \(T'\)-joins:

```text
J1 = {1,7,8,9,10,21,22,28,29,32}
J2 = {0,2,12,14,15,17,18,20,31}.
```

Their union is one circuit through all four terminals.  This explicit
neutral exchange is why the example refutes only the universal
“every minimizer” strengthening.  The existential “some minimizer”
statement remains true on this graph.

## Scope and graph metadata

The checker independently validates the graph6 decoding, simplicity,
cubicity, connectedness, bridgelessness, girth five, and edge connectivity
three.  The displayed 3-edge cut `{14,15,27}` separates two cyclic shores,
so cyclic edge connectivity is exactly three.  The example is therefore
outside the surviving cyclically-4/girth-at-least-10 reduced domain.

Run:

```sh
python3 verify.py
```

The sole output is a canonical one-line JSON report ending in
`"status":"PASS"`.

## AI-use disclosure

This example was found, lifted, analyzed, and packaged with substantial
assistance from OpenAI Codex agents under human direction.  The complete
literal graph, flows, short parity proof, and dependency-free exhaustive
checker are included so that no mathematical claim requires trusting an
AI system.
