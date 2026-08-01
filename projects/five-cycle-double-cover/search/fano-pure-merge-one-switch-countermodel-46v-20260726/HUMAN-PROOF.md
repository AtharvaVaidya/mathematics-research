# Human proof of the 46-vertex pure-merge one-circuit countermodel

## Scope

This note proves a negative result about one proposed route from an
eight-cycle double cover to a five-cycle double cover. It does **not**
disprove the five-cycle double-cover conjecture. The graph constructed below
is three-edge-colorable and therefore has an explicit three-cycle double
cover.

All vector arithmetic is in \(\mathbb F_2^3\), represented by the integers
\(0,\ldots,7\) with addition equal to bitwise xor.

## Potentials, pair labels, and pure merges

Let \(G\) be a cubic graph with a nowhere-zero flow
\(\phi:E(G)\to\mathbb F_2^3\). A family of vertex potentials
\((t_v:v\in V(G))\) is *compatible* when, for every edge \(e=uv\),

\[
 t_u+t_v\in d_e+\langle\phi(e)\rangle,\qquad
 d_e=\phi(f_u)+\phi(f_v),
\tag{1}
\]

where \(f_u\ne e\) and \(f_v\ne e\) are incident with \(u\) and \(v\).
The choice of either other edge at an endpoint does not matter because the
three incident flow values sum to zero.

Such a potential gives the two-element edge label

\[
 P_e=t_u+\phi(f_u)+\langle\phi(e)\rangle
     =t_v+\phi(f_v)+\langle\phi(e)\rangle.
\tag{2}
\]

For each \(s\in\mathbb F_2^3\), the edges whose label contains \(s\)
form an Eulerian subgraph. Thus the eight coordinates form a cycle double
cover.

A *pure merge into at most five coordinates* partitions the eight original
coordinates into at most five classes and takes the symmetric difference
inside each class. An edge survives in exactly two merged coordinates
precisely when its two labels lie in different classes. Consequently:

> **Coloring equivalence.** A compatible pair labeling admits a pure merge
> into at most five Eulerian subgraphs if and only if its coordinate
> co-occurrence graph—vertices \(0,\ldots,7\), with \(a b\) an edge whenever
> some \(P_e=\{a,b\}\)—is properly colorable with at most five colors.

The forward direction reads the merge classes as colors. For the reverse
direction, symmetrically difference all original coordinate subgraphs of
each color. Symmetric differences preserve even degree. The proper-coloring
condition makes every original edge survive once in each of two distinct
output coordinates.

This is the exact intermediate operation refuted below. It is much narrower
than an arbitrary construction of a five-cycle double cover.

## A potential-rigid 12-vertex cap

Let \(B\) have graph6 record

```text
K??FEaKR@oE_
```

and the following edge and flow table. The column \(d_e\) is from (1), and
the final column is the pair label from the gauged potential displayed
below.

| edge | endpoints | \(\phi(e)\) | \(d_e\) | \(P_e\) |
|---:|:---:|---:|---:|:---:|
| 0 | \(0,6\) | 1 | 6 | 23 |
| 1 | \(0,7\) | 2 | 6 | 13 |
| 2 | \(0,8\) | 3 | 4 | 12 |
| 3 | \(1,6\) | 4 | 6 | 26 |
| 4 | \(1,7\) | 7 | 6 | 16 |
| 5 | \(1,9\) | 3 | 5 | 12 |
| 6 | \(2,6\) | 5 | 2 | 36 |
| 7 | \(2,10\) | 3 | 2 | 03 |
| 8 | \(2,11\) | 6 | 7 | 06 |
| 9 | \(3,7\) | 5 | 5 | 36 |
| 10 | \(3,10\) | 7 | 6 | 34 |
| 11 | \(3,11\) | 2 | 3 | 46 |
| 12 | \(4,8\) | 5 | 2 | 14 |
| 13 | \(4,9\) | 1 | 6 | 01 |
| 14 | \(4,10\) | 4 | 6 | 04 |
| 15 | \(5,8\) | 6 | 1 | 24 |
| 16 | \(5,9\) | 2 | 5 | 02 |
| 17 | \(5,11\) | 4 | 0 | 04 |

Use edge 1 as a port and delete it. We now prove that the remaining
compatibility equations determine all twelve potentials up to adding one
common vector.

Fix the translation by \(t_0=0\). On the spanning tree whose edges, in
order, are

```text
0 2 3 6 12 15 4 5 7 8 9
```

write

\[
 t_u+t_v=d_e+\lambda_j\phi(e)
\]

when the \(j\)-th displayed tree edge is \(e=uv\). The tree equations
express every \(t_v\) in the eleven scalars
\(\lambda_0,\ldots,\lambda_{10}\). Substitution into the six remaining
internal edges \(10,11,13,14,16,17\), followed by elementary xor row
operations, gives

```text
λ3 + λ10      = 0
λ2 + λ6 + λ9 = 0
λ2 + λ8      = 1
λ1 + λ7      = 0
λ6           = 1
λ2 + λ5      = 1
λ2 + λ4      = 1
λ0 + λ1 + λ3 = 0
λ1 + λ2      = 0
λ1           = 1
λ0           = 1
```

These equations have the unique solution

```text
(λ0,...,λ10) = (1,1,1,0,0,0,1,1,0,0,0).
```

Back-substitution gives

```text
(t0,...,t11) = (0,5,5,1,5,6,7,4,7,3,7,2).
```

This is a complete 11-variable hand check of rigidity. Equivalently, the 37
scalar equations consisting of two equations for each of the 17 retained
edges and the three equations \(t_0=0\) have rank 36.

Compute (2) from these twelve values. The retained internal labels, together
with the dangling label 13 calculated independently from either side of the
deleted port, use exactly

```text
01 02 03 04 06
12 13 14 16
23 24 26
34 36
46
```

These are all fifteen pairs on the six coordinates
\(\{0,1,2,3,4,6\}\). The co-occurrence graph therefore contains \(K_6\)
and cannot be five-colored. Adding a common vector \(a\) to every potential
just replaces every coordinate \(s\) by \(s+a\), so it translates the same
\(K_6\).

We have proved the local statement needed later:

> **Rigid-cap lemma.** Suppose a copy of \(B-e_1\), together with its two
> dangling flow-2 ports, occurs in a larger cubic flow graph and its internal
> and port flow values are the displayed ones. Every compatible global
> potential forces a coordinate \(K_6\) on the internal edges and the two
> ports. Hence no compatible eight-cover for that fixed global flow admits a
> pure five-way merge.

Indeed, restrict any global potential to the cap. Its internal equations are
the equations just solved. At the two cap endpoints, formula (2) gives the
labels of the two external connector edges, so the missing pair 13 is also
present.

## A ten-vertex base with three noncyclable edges

Let \(H\) have graph6 record

```text
It?GYDKKO
```

and this edge table:

| edge | endpoints | color | flow |
|---:|:---:|---:|---:|
| 0 | 01 | 0 | 1 |
| 1 | 02 | 1 | 2 |
| 2 | 03 | 2 | 3 |
| 3 | 23 | 0 | 1 |
| 4 | 45 | 2 | 3 |
| 5 | 46 | 0 | 1 |
| 6 | 56 | 1 | 2 |
| 7 | 17 | 1 | 2 |
| 8 | 67 | 2 | 3 |
| 9 | 18 | 2 | 3 |
| 10 | 48 | 1 | 2 |
| 11 | 58 | 0 | 1 |
| 12 | 29 | 2 | 3 |
| 13 | 39 | 1 | 2 |
| 14 | 79 | 0 | 1 |

Every vertex sees one edge of each color, and \(1+2+3=0\). This is a
proper three-edge-coloring and a nowhere-zero flow.

Put

\[
 P=\{1,6,7\}=\{02,56,17\}.
\]

No circuit of \(H\) contains all three edges. Here is a short proof.
Suppose that a circuit \(C\) contains \(P\).

In the triangle on \(0,2,3\), the boundary behavior of a circuit forces
\(01\in C\). Otherwise the forced degrees make
\(0\,2\,9\,3\,0\) the whole circuit. Applying the same argument to the
triangle on \(4,5,6\) forces \(67\in C\), and exactly one of \(48,58\)
lies in \(C\).

At vertex 7, the edges \(17,67\) exclude \(79\). At vertex 1, the edges
\(17,01\) exclude \(18\). Vertex 8 is then incident with exactly one edge of
\(C\): exactly one of \(48,58\), while \(18\) is absent. This contradicts
the even degree of a circuit. Thus \(P\) is noncyclable.

For comparison with the verbal argument, the independent checker enumerates
all 30 circuits of \(H\) and finds zero containing \(P\).

## The 46-vertex construction

For each edge in \(P\), take a fresh copy of \(B\), delete its port edge 1,
delete the selected base edge, and join corresponding endpoints with two new
edges. Give both connectors flow value 2. This is an aligned edge two-sum.
Call the resulting graph and flow \((G,\phi)\).

The complete edge list, edge origins, flow, compatible pair labeling,
three-edge-coloring, and graph6 record are frozen in `construction.json`.
The construction has

```text
vertices       46
edges          69
rigid caps      3
```

It is simple, connected, cubic, and bridgeless. For bridgelessness, each
summand is connected and bridgeless and the deleted ports are replaced by
two connectors; every original or connector edge remains on a circuit.
The independent checker makes the stronger finite check that deletion of
each of the 69 edges leaves the graph connected.

The displayed flow is conserved because every affected vertex loses and
gains the same flow value. It has a compatible potential: put \(t_v=0\) on
the base and use the twelve cap potentials displayed above on each copy.
The base color labels are

```text
color 0 -> 23
color 1 -> 13
color 2 -> 12
```

so the base side and the cap side assign pair 13 to every connector.

## No one connected-circuit switch can repair the pure merge

Let \(C\) be any connected circuit of \(G\). If it lies entirely in one cap,
it misses the other two caps and their connectors.

Otherwise, a circuit crosses the two-edge boundary of any cap in zero or two
edges. Whenever it uses both connectors, replace its path through that cap by
the deleted base edge. After doing this for every traversed cap, one obtains
a circuit of \(H\). If \(C\) traversed all three caps, the projected circuit
would contain all three edges of \(P\), contradicting the preceding
noncyclability proof. Hence \(C\) leaves at least one whole cap and both of
its connectors untouched.

Now choose any nonzero \(a\in\mathbb F_2^3\), and switch the flow on \(C\):

\[
 \phi'(e)=
 \begin{cases}
 \phi(e)+a,&e\in C,\\
 \phi(e),&e\notin C.
 \end{cases}
\]

Restrict attention to switches for which \(\phi'\) is nowhere zero, as the
flow construction requires. On the untouched cap and its connectors,
\(\phi'=\phi\). The rigid-cap lemma says that every potential compatible
with \(\phi'\) forces a coordinate \(K_6\). By the coloring equivalence, no
such compatible eight-cover admits a pure merge into five coordinates.

We have therefore proved:

> **Theorem.** There is an explicit simple connected bridgeless cubic graph
> \(G\) with a nowhere-zero \(\mathbb F_2^3\)-flow \(\phi\) such that:
>
> 1. no compatible eight-cover obtained from \(\phi\) by the potential
>    construction admits a pure merge into at most five Eulerian subgraphs;
>    and
> 2. after every nowhere-zero switch \(\phi+a\chi_C\) on one connected
>    circuit \(C\), no compatible eight-cover obtained from the switched
>    flow admits such a pure merge.

The obstruction uses three two-edge cuts. It therefore does not refute a
version restricted to cyclically 4-edge-connected cubic graphs.

## Explicit positive five-cycle double cover

The base and cap colorings align at every deleted color-1 edge. Give both
connectors color 1. The result is a proper three-edge-coloring of \(G\).
If \(M_0,M_1,M_2\) are its color classes, then

\[
 E(G)\setminus M_0,\quad E(G)\setminus M_1,\quad E(G)\setminus M_2
\]

are Eulerian, and every edge belongs to exactly two of them. Their sizes are

```text
46 46 46
```

Appending two empty Eulerian subgraphs gives a standard five-cycle double
cover with coordinate sizes

```text
46 46 46 0 0.
```

Thus the theorem is not a counterexample to the five-cycle double-cover
conjecture.

## Independent finite check

`independent_checker.py` imports no producer or project module. It:

1. reconstructs the 46-vertex graph from the frozen 10- and 12-vertex
   constants;
2. checks simplicity, cubicity, connectedness, all 69 one-edge deletions,
   every flow equation, the eight-cover parity equations, and the explicit
   three-edge-coloring/five-cover;
3. independently row-reduces the port-deleted cap system, obtains rank 36,
   and checks the exact forced \(K_6\);
4. enumerates all 30 base circuits and checks noncyclability;
5. independently enumerates the 128 globally compatible gauged potential
   solutions and confirms that every co-occurrence graph contains a
   \(K_6\) and none is five-colorable; and
6. reconstructs the graph6 record and, when nauty `labelg` is installed,
   computes the canonical graph6 record.

The frozen output is `independent-check.json`.

## AI-use disclosure

OpenAI Codex agents, using GPT-5-series models under the user's direction,
formulated and tested the pure-merge repair strategy, found the 12-vertex
rigid cap and the 46-vertex composition, wrote both producer and independent
checker, performed the finite computations, and drafted this proof. A
separate Codex agent was assigned to revise and referee the associated
preprint. This is substantive AI assistance. It is **not** independent human
peer review.

Before publication, a human author should independently check equations
(1)–(2), the eleven displayed scalar equations and their back-substitution,
the \(K_6\) label list, the base noncyclability argument, the two-edge-sum
projection, the source code, and the literature attribution.
