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

## Reproduction

From `projects/five-cycle-double-cover/`:

```sh
c++ -O3 -std=c++20 scratch/verify_fano_cyclic4_allseven_order60.cpp \
  -o /tmp/verify-fano-order60
/tmp/verify-fano-order60
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
