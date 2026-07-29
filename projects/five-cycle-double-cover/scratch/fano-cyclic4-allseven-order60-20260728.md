# A cyclically 4-edge-connected obstruction to cleaning every projection of a fixed Fano flow

Audit date: **2026-07-28**.

Status: **auxiliary theorem, not a Five-Cycle Double Cover resolution**.
The mathematical reduction below is human-checkable.  The finite local
classifications are replayed by a solver-independent C++ program using only
exhaustive binary-cycle enumeration and Gaussian elimination over
\(\mathbb F_2\).  The construction and this exposition were produced with
substantive OpenAI Codex assistance and have not yet received independent
human review.

## Statement

There is a simple nonplanar cubic graph \(G\) of order \(60\), with cyclic
edge-connectivity at least four, and a nowhere-zero
\(\mathbb F_2^3\)-flow \(f\) such that none of the seven nonzero functional
projections of \(f\) has a clean lift with that projection fixed.

Here “clean” is the exact component-parity condition in
Hušek--Šámal, *Exponentially Many Circuit Double Covers*,
[arXiv:2607.24724](https://arxiv.org/abs/2607.24724), Theorem 3.16.
Equivalently, for a nonzero functional \(\mu\), put
\[
 h=\mu\circ f,\qquad F_\mu=h^{-1}(0).
\]
A fixed-projection clean lift exists exactly when there are two binary
cycles \(p,q\) which cover \(F_\mu\) and satisfy
\[
 \sum_{e\in\delta(X)}p(e)q(e)=0\pmod2
 \tag{1}
\]
for every component \(X\) of \(F_\mu\).

The same graph has an explicit standard FiveCDC.  It is therefore not a
counterexample to FiveCDC.  Instead, it refutes the tempting stronger
claim that *every* nowhere-zero three-bit flow on a cyclically
4-edge-connected cubic graph has a clean functional projection.  The
existential choice of the flow in Hušek--Šámal Conjecture 3.19 is essential.

## Exact construction

Represent the nonzero elements of \(\mathbb F_2^3\) by the integers
\(1,\ldots,7\), with addition given by bitwise xor and
\(\mu_a(x)=\operatorname{parity}(a\mathbin{\&}x)\).

Start with the order-32 graph

```text
_??G@EOGG?GB_AO_g_?CP_??C??O????[O?CA?AG??CA??@???A?O??C???????G????g???@W???E????@c
```

and give its 48 edges, in graph6 order
\((v,u)\) with \(u=1,\ldots,31\) and \(v=0,\ldots,u-1\), the values

```text
3 6 2 7 5 7 2 7 5 2 1 7 2 4 6 5
6 6 5 3 6 5 5 5 6 3 6 3 6 3 5 6
3 2 4 4 1 1 6 7 2 3 1 2 6 6 2 4
```

The xor of the three incident values is zero at every vertex.

Make two four-poles:

- \(A\): delete the endpoints \(6,7\) of edge 2 and apply
  \(T_A=(0,4,3,7,1,5,2,6)\);
- \(B\): delete the endpoints \(8,9\) of edge 6 and apply
  \(T_B=(0,7,3,4,5,2,6,1)\).

Both tuples list the image of \(0,1,\ldots,7\).  Each is an invertible
linear map.  The sorted old-vertex/value ports, before and after the maps,
are

```text
A: (2,6) (13,4) (15,6) (25,4)  ->  (2,2) (13,1) (15,2) (25,1)
B: (0,7) ( 2,7) ( 3,5) (11,5)  ->  (0,1) ( 2,1) ( 3,2) (11,2)
```

Relabel the retained vertices of \(A\), in increasing old-vertex order, by
\(0,\ldots,29\), and those of \(B\) by \(30,\ldots,59\).  Join ports
\[
 (A_0,B_2),\quad(A_1,B_0),\quad(A_2,B_3),\quad(A_3,B_1).
\]
The four new edges, with their common flow values, are
\[
 (2,33):2,\quad(11,30):1,\quad(13,39):2,\quad(23,32):1.
\]
This gives a simple cubic graph and a nowhere-zero flow.  Its labelled
graph6 record is

```text
{??K`C?O[@G@P??Go??G?A????w_?_O@C??GC??G??@????G??????C???@O???J???B????BG?G???????????C?G???????????????@???????????G_???????A??A@?????_G????@AG????AG??????DC????A???????@???????O????????F?????C?C?????A?G_??????@??????_?@????????G?????@???????@????????????_????????I????????@W????????W?????????X
```

Running nauty `labelg -q` gives the canonical record

```text
{s?GO?@?O????@????W?G?A_?K???G?A???_??E???A???C???????B???G_??@O???_????O??????????K????I??O??????@_????GO????@G????AO??????????C???????CG?????OO@????W??_???@G?O????W?G????o?I?????????????@?AC?????????_?G??_??O????C??????G?_?_?????G????????_??????GO_??????C__???????CO???????@@???????A?g???????CC
```

Nauty `planarg -v` returns this record, independently confirming that it
is nonplanar.

## Why the two local classifications imply the global obstruction

Regard each joining edge as a semiedge in each pole.  The restriction of a
global binary cycle to either pole has even incidence at every retained
vertex, so it is a binary pole cycle.  Likewise, global coverage of
\(F_\mu\) restricts to coverage of every proper and semiedge occurrence of
the local factor.

A component of the local factor which touches no factor-valued semiedge is
also a complete global factor component contained in that pole.  Therefore
equation (1) for a global clean lift includes every “closed component”
equation imposed by the local test.  Consequently:

> If the exact local formula is unsatisfiable on either pole for
> \(\mu\), no completion of the pole can yield a global clean lift for
> that \(\mu\).

The exact local bad-functional profiles are
\[
             \operatorname{bad}(A)=\{5,6,7\},\qquad
             \operatorname{bad}(B)=\{1,2,3,4,5\}.
\]
Their union is all of \(\{1,\ldots,7\}\), proving the statement.

## Solver-independent exhaustive proof of the local profiles

Each pole has 43 proper edges, four semiedges, and binary pole-cycle
dimension 17.  For each functional, the checker enumerates all
\(2^{17}=131072\) choices of the first cycle \(p\).

Once \(p\) is fixed, every remaining condition on \(q\) is linear over
\(\mathbb F_2\):

1. \(q\) is expressed in a computed basis of the pole cycle space;
2. if a factor edge is absent from \(p\), coverage forces \(q(e)=1\);
3. for each closed factor component \(X\), equation (1) becomes
   \[
      \sum_{e\in\delta(X):\,p(e)=1}q(e)=0.
   \]

Binary Gaussian elimination decides this system exactly.  Thus every
possible pair \((p,q)\) is covered without invoking a SAT solver or trusting
a search heuristic.  The program obtains precisely the two profiles above.
This is a finite computer-assisted proof, not a claimed handwritten
enumeration.

## Independent graph checks and a positive FiveCDC

The same checker reconstructs the order-60 graph from the order-32 source
and pole recipe, then verifies:

- 60 vertices, 90 distinct edges, degree three at every vertex;
- nonzero values and flow conservation at every vertex;
- every one of the
  \[
  {90\choose1}+{90\choose2}+{90\choose3}=121575
  \]
  edge sets fails to separate two cyclic components;
- the labelled graph6 record above; and
- the following standard FiveCDC.

In graph6 edge order, label each edge by this five-bit, weight-two integer:

```text
3 20 5 20 17 9 5 12 12 9 12 5 5 6 5
3 24 5 10 9 17 24 12 20 9 17 24 18 9 17
3 18 24 10 24 24 10 18 9 17 10 18 24 9 9
6 6 10 9 6 3 5 12 20 18 10 24 17 3 3
17 18 5 5 10 17 9 24 20 12 12 20 24 18 18
10 24 3 3 24 17 9 18 10 24 9 17 10 18 24
```

The five coordinates are the five Eulerian edge-subsets.  Weight two gives
exact double coverage, and xor zero around each vertex gives even degree in
each coordinate.  These two facts are exactly the standard FiveCDC
conditions.

## A checked bad-to-good flow repair

The positive cover does more than show that some unrelated good flow
exists.  Label its five cycle slots by
\[
                   000,\ 001,\ 010,\ 011,\ 100.
\]
If edge \(e\) belongs to the two slots labelled \(i,j\), put
\(g(e)=i+j\).  This is the nowhere-zero flow induced by the cover in the
Hušek--Šámal construction.

The displayed all-seven-bad flow has a one-switch repair.  Add
\(7=111\) on the simple cycle with graph6 edge ids

```text
1,2,8,11,18,22,24,26,27,30,31,33,35,37,39,40,42,43,45,62,65,67,73,74,75.
```

None of those 25 edges initially has value 7.  The resulting assignment
is therefore still nowhere-zero, and its seven odd-component counts are
\[
                         (10,6,6,8,8,6,0).
\]
It satisfies the Hušek--Šámal condition for functional \(7=111\).
Thus the obstruction is maximally bad inside all seven fixed projection
fibres but lies at flow-reconfiguration distance one from a good flow.

There is also an explicit path from \(f\) to the particular cover-induced
flow \(g\).  A switch \((a,C)\) replaces \(f(e)\) by
\(f(e)+a\) on \(C\).  It preserves flow conservation, and is nowhere-zero
provided no edge of \(C\) currently has value \(a\).  In graph6 edge ids,
this is the adjacency used by Cranston et al.,
*Reconfiguration of Nowhere-zero Flows*,
[arXiv:2606.24685](https://arxiv.org/abs/2606.24685).  The exact switches
are:

```text
 1: a=1  C=13,15,17,22,23,28,31,32,34,36,37,45,49,51,52,54,56,57,60,61,62,64,70,71,73,74,75
 2: a=6  C=0,17,19,20,24,25
 3: a=7  C=3,6,7,10,12,14,15,43,45,52,53,54,55,57,58,59,60,63,68,69
 4: a=2  C=2,3,4,28,32,35,36,44,45,46,63,64,68,69,73,76,78,80,81
 5: a=5  C=3,5,6,10,43,45,46,62,63,65,66,68,70,72
 6: a=3  C=64,65,67,70,71
 7: a=6  C=35,36,39,41,42
 8: a=7  C=18,22,24,26,27,28,29
 9: a=5  C=1,2,16,22,25,26
10: a=5  C=1,4,6,7,8,9
11: a=4  C=47,77,78,86,87,89
12: a=7  C=82,83,86,88,89
13: a=1  C=82,83,86,88,89
```

After switch 11, functional \(4=100\) already has zero odd components,
so the flow is good in the exact sense of Theorem 3.16.  The last two
switches reach \(g\) exactly.  The numbers of edges still differing from
\(g\), including the initial state, are

```text
74,63,59,51,44,34,29,24,19,15,9,5,5,0.
```

The seven odd-component counts at the initial flow, after switch 11, and
at the target are respectively
\[
 (8,8,4,6,6,8,6),\quad
 (8,10,4,0,10,14,16),\quad
 (10,10,4,0,10,16,14).
\]
The standard-library checker independently reconstructs the graph and both
flows, verifies every switch support is one connected 2-regular subgraph,
checks the no-zero condition before every switch and flow conservation
after it, recomputes all fourteen seven-functional profiles, and checks
equality with the cover-induced target.

These paths are certificates for one graph, not a universal repair
theorem.  They do show that the all-seven obstruction and a good flow lie
in the same \(\mathbb F_2^3\)-flow-reconfiguration component.

## Reproduction

From `projects/five-cycle-double-cover/`:

```sh
c++ -O3 -std=c++20 scratch/verify_fano_cyclic4_allseven_order60.cpp \
  -o /tmp/verify-fano-order60
/tmp/verify-fano-order60
python3 scratch/verify_fano_order60_flow_repair.py
```

The expected one-line JSON result includes

```json
{
  "order": 60,
  "edges": 90,
  "first_local_bad": [5, 6, 7],
  "second_local_bad": [1, 2, 3, 4, 5],
  "all_seven_blocked": true,
  "cyclic_edge_connectivity_at_least_four": true,
  "standard_fivecdc_witness": true,
  "fivecdc_counterexample": false,
  "solver_independent": true
}
```

The discovery-only program
`scratch/search_fano_order32_near_pole_profiles.py` uses CaDiCaL to scan all
48 adjacent-vertex deletions of the order-32 near-flow.  It is retained for
provenance but is not part of the theorem's trust base.

## Novelty and scope

Targeted searches through 2026-07-28 did not locate this particular
fixed-projection statement or a prior cyclically 4-edge-connected
counterexample to it.  That is only a provisional literature assessment,
not a priority claim.  The result is potentially useful as a sharp warning
for proofs based on an arbitrary Jaeger 8-flow: even after the usual
cyclic-connectivity reduction, all seven projections of the chosen flow
can fail simultaneously.

It neither proves nor disproves FiveCDC.  A valid proof must make the
existential flow choice, change the flow, or use a different formulation.
The displayed five-cover proves that such a repair exists on this example.
