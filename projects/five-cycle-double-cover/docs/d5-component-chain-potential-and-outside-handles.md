# The \(D_5\) component-chain potential and the outside-handle gap

Date: **2026-07-28**

Status: **EXACT FINITE EVIDENCE AND A LOCAL REROUTING LEMMA; NOT A
FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. The potential

Let \(q:E(G)\to\binom{[5]}2\) be a \(D_5\)-flow on a connected cubic
graph.  For a coordinate pair \(P=\{i,j\}\), write
\[
 Y_P=\{e:|q(e)\cap P|=1\}.
\]
Every \(Y_P\) is an even subgraph, hence a disjoint union of circuits.
Form a hypergraph on \(E(G)\) whose hyperedges are all circuit components
of all ten \(Y_P\).  For root edges \(r,s\), let \(d_q(r,s)\) be the
minimum number of hyperedges in a chain from \(r\) to \(s\), consecutive
hyperedges in the chain being required to share an edge.

The hypergraph is connected.  Indeed, at a cubic vertex the three incident
labels have the form \(ab,ac,bc\).  The first two incident graph edges lie
on the same component of \(Y_{bc}\), and similarly for either other pair.
Thus adjacent graph edges lie in a common hyperedge, and connectedness of
\(G\) finishes the argument.

Moreover,
\[
 d_q(r,s)=1
\quad\Longleftrightarrow\quad
r,s\text{ lie on one component of some }Y_P.
\]
Thus distance one is exactly the rooted condition needed by the smoothing
induction.

## 2. Exact switch law

Let \(K\) be one component of \(Y_P\), and transpose the two coordinates
in \(P\) on all edges of \(K\).  If \(q'\) is the resulting flow, then for
every coordinate pair \(Q\),
\[
 Y_Q(q')=
 \begin{cases}
 Y_Q(q),& |P\cap Q|\in\{0,2\},\\
 Y_Q(q)\mathbin\triangle K,& |P\cap Q|=1.
 \end{cases}
\]
This is an edgewise identity.  Outside \(K\) nothing changes.  On \(K\),
membership in \(Y_Q\) is toggled precisely when the transposition of \(P\)
moves exactly one coordinate of \(Q\).

The proposed descent statement is:

> Every connected component of states at one fixed bad value
> \(d_q(r,s)>1\), under Kempe moves preserving that value, has a Kempe
> edge to a state of smaller value.

If true, finiteness of every Kempe orbit would force distance one.  This
would prove the conditional rooted reconfiguration theorem used by the
current FiveCDC induction.

## 3. Complete local classification and outside handles

Suppose a component of \(Y_A\) and a component of \(Y_B\) share an edge
whose label is \(L\).  Then \(L\) is active in both factors.  Up to an
element of \(S_5\), there are exactly three possibilities:

| relation | \(A\) | \(B\) | \(L\) |
|---|---|---|---|
| \(|A\cap B|=1\), symmetric-difference label | \(01\) | \(02\) | \(12\) |
| \(|A\cap B|=1\), common-coordinate label | \(01\) | \(02\) | \(03\) |
| \(A\cap B=\varnothing\) | \(01\) | \(23\) | \(02\) |

For example, in the first two rows the equations saying that a weight-two
label is active in both \(01\) and \(02\) give \(L\in\{12,03,04\}\), and
the stabilizer interchanges \(03,04\).  In the disjoint case all four
cross labels form one stabilizer orbit.

Each case has two **independent outside handles**:

| \((A,B,L)\) | \(R\) | \(S\) |
|---|---|---|
| \((01,02,12)\) | \(13\) | \(23\) |
| \((01,02,03)\) | \(13\) | \(23\) |
| \((01,23,02)\) | \(04\) | \(24\) |

In every row:

* \(L\) is active in both \(Y_R\) and \(Y_S\);
* \(|R\cap A|=1\) and \(R\cap B=\varnothing\);
* \(|S\cap B|=1\) and \(S\cap A=\varnothing\).

Consequently, if \(H_R\) is the \(Y_R\)-component through the shared edge,
switching \(H_R\) gives
\[
       Y_A'=Y_A\triangle H_R,\qquad Y_B'=Y_B.
\]
The \(S\)-handle symmetrically reroutes \(Y_B\) while fixing \(Y_A\).
This is the exact point at which a fourth or fifth coordinate supplies
more freedom than a Tait-coloring argument.

This lemma is completely local and proved by the three-row table plus the
switch law.  It does **not** prove descent: the circuit \(H_R\) can return
through the global graph in a way that reroutes the wrong arc.  A proof
still needs a global assertion that repeated independent reroutings reach
the required exit of a shortest circuit chain without first increasing
the chain distance.

## 4. Why a fixed two-factor/Kotzig argument is insufficient

When \(|A\cap B|=1\), the symmetric difference \(T=A\triangle B\) is
itself a coordinate pair and
\[
                   Y_T=Y_A\triangle Y_B.
\]
On the union of these three factors, every used edge belongs to exactly
two of them.  After suppressing degree-two paths, the three missing-factor
types give an ordinary proper three-edge-coloring, and component switches
among \(A,B,T\) are ordinary bichromatic Kempe swaps.

Therefore an argument using only \(Y_A,Y_B,Y_T\) reduces to the rooted
Tait-Kempe branch.  That branch is false on the Wagner graph.  The outside
handles above are not optional; a valid proof must use them explicitly.

## 5. Sharp one-switch no-go

The graph

```text
M??CBAPsAWBOH_J??
```

with the explicit 21-edge labeling and roots \(1,17\) in
`scratch/d5-root-plateau-counterexample-order14-20260728.md` has
\[
                         d_q(1,17)=2.
\]
Modulo global \(S_5\), it has exactly three nontrivial one-switch
neighbours.  Every one also has distance two.  Thus even with all outside
handles available, a strict one-switch circuit-chain descent lemma is
false.

The displayed second switch reaches distance one, so this is sharp for
that state: one neutral move followed by descent succeeds.  The literal
checker

```text
python3 scratch/verify_d5_component_chain_one_switch_no_go.py
```

independently traces every factor component and every first move and prints
`PASS`.

A second exact witness rules out the next bounded version.  On

```text
M?AA@AWwAgAgAoI_?
```

there is a Tait-derived state, using only labels \(01,02,12\), and roots
for which the shortest distance sequence leading downward is
\[
                         2,\ 2,\ 2,\ 1.
\]
Thus neither the initial state nor any state one neutral move away has a
descent.  Two neutral moves are necessary before the lowering move.  The
extractor

```text
python3 scratch/extract_d5_component_chain_depth2_witness.py
```

prints the complete graph, four literal label tuples, three switched
factor components, and the distance sequence.  Its breadth-first
minimality check exhausts the closed equal-distance balls of radii zero
and one.

This obstruction is especially instructive: the shortest rescue uses
the factor sequence \(01,12,02\) and never introduces coordinate 3 or 4.
It is a genuine circuit-interlacement phenomenon already inside the
ordinary Tait subsystem, not a failure caused by choosing the wrong
outside handle.  Therefore a case table covering at most two switches
cannot prove the plateau lemma.

## 6. Exact finite audit

The C++ producer

```text
scratch/audit_d5_root_component_chain_potential.cpp
```

enumerates every \(D_5\)-flow modulo global \(S_5\), constructs the full
Kempe graph, computes all component-chain distances, and checks every
equal-distance plateau.

For all 480 biconnected simple cubic graphs of order 14:

| quantity | count |
|---|---:|
| normalized \(D_5\)-flows | 537,418 |
| unordered state/root-pair tests | 112,857,780 |
| equal-distance plateaus | 951,298 |
| maximum distance | 3 |
| maximum equal moves needed before a descent | 2 |
| plateau failures | **0** |

The complete report is

```text
scratch/d5-root-component-chain-all-biconnected-cubic-order14.jsonl
```

The augmented replay that measures exact distance to the descent boundary
is

```text
scratch/d5-root-component-chain-depth-all-biconnected-cubic-order14.jsonl
```

Only graph 253 reaches the sharp value two.

and

```text
python3 scratch/verify_d5_root_component_chain_order14_report.py
```

regenerates all graph identities, checks the arithmetic, and independently
replays five selected rows in Python.

A deterministic order-20 Tait-derived distance-three state was also
audited over its complete Kempe orbit:

| quantity | count |
|---|---:|
| normalized states | 18,893 |
| states at distance 1 | 11,811 |
| states at distance 2 | 7,058 |
| states at distance 3 | 24 |
| equal-distance plateaus | 54 |
| plateau failures | **0** |

The independent Python replay is

```text
python3 scratch/verify_d5_root_component_chain_order20.py
```

and prints `PASS`.

Finally, the flag graph of the \(3\times3\) toroidal square map supplies a
structured Tait-derived state on 72 vertices whose current factor-chain
distance reaches four.  Every root pair at distance at least three has an
immediate lowering move in that state, while 36 distance-two pairs are
strict local minima.  This supports, but does not prove, that the hard
case is the distance-two outside-handle cage.

The \(5\times5\) member has 200 vertices and reaches distance six.  More
generally these distances are unbounded: the three kinds of bichromatic
circuits in a square-map flag graph are exactly the flag cycles around a
face, vertex, or edge.  A chain of \(k\) such circuits projects to a walk
of length \(k\) in the vertex-edge-face incidence graph of the toroidal
map.  Features at unbounded toroidal distance therefore give root edges
at unbounded component-chain distance.  The potential is not secretly a
bounded three-level invariant.

## 7. A failed global arc potential

The sharp three-switch witness suggests measuring a distance-two chain
more finely.  For distinct factor components \(C\ni r\), \(D\ni s\) with
\(C\cap D\ne\varnothing\), let
\[
 \ell(C,D)=\min_{e\in C\cap D}
 \bigl(\operatorname{dist}_C(r,e)+\operatorname{dist}_D(e,s)\bigr).
\]
Let \(N\) be the number of distinct intersecting pairs \((C,D)\), after
identical components occurring in several coordinate factors are
identified, and let \(L=\min\ell(C,D)\).

Along the sharp depth-two witness, the neutral prefix has
\[
                       (N,L)=(1,4),(2,4),(2,5),
\]
so lexicographic ascent of \((N,L)\) looks natural.  The exact audit

```text
scratch/audit_d5_root_chain_interlacement_potential.py
```

confirms strict ascent at all 110 strict distance-local minima on that
host graph.  It then refutes the proposed potential on
`M??CBAPsAWBOH_J??`: for roots \(1,17\), one strict local minimum has
signature \((18,5)\), while its neutral neighbours have signatures
\((12,4),(10,4),(9,4),(5,4)\).  Hence the two sharp witnesses require
opposite directions in both chain multiplicity and constrained arc
distance.

This is a precise no-go for the most direct global interlacement measure,
not a refutation of the plateau lemma.

## 8. Exact remaining lemma

The unresolved human proof obligation can now be stated narrowly:

> **Outside-handle plateau lemma.** Let \(q\) be a \(D_5\)-flow, and let
> \(r,s\) be root edges with \(d_q(r,s)>1\).  In the graph of states
> reachable by moves that keep \(d(r,s)=d_q(r,s)\), the component of \(q\)
> contains a state admitting a move to smaller distance.

The three-case handle table is the available local mechanism.  The missing
step is global: rule out a closed cage in which every \(R\)- and
\(S\)-handle circuit returns with the wrong transition pairing.  The
two order-14 witnesses prove that this step cannot be replaced by either
a one-switch assertion or a case analysis confined to one neutral move
followed by descent.  The second witness also shows that ordinary
three-color circuit interlacement must be controlled even when outside
coordinates are available.

This difficulty is consistent with the existing edge-Kempe literature.
Belcastro and Haas show that Kempe-class counts multiply under cubic
two- and three-cut compositions and construct infinite families with
many classes; Goedgebeur and Östergård construct families with
exponentially many three-edge-Kempe classes.  Thus a finite classification
of Tait interlacement cages is not available.  On the positive side,
McDonald, Mohar, and Scheide prove that all four-edge-colorings of a
subcubic graph are Kempe equivalent.  A fresh D5 coordinate resembles
their extra edge color, but no valid simulation is currently known:
their bichromatic components may be paths, whereas every \(Y_{ij}\) in a
closed D5 flow is even and its Kempe components are circuits.

Primary references:

* S.-M. Belcastro and R. Haas,
  [*Counting edge-Kempe-equivalence classes for 3-edge-colored cubic
  graphs*](https://arxiv.org/abs/1209.1730).
* J. Goedgebeur and P. R. J. Östergård,
  [*Switching 3-edge-colorings of cubic
  graphs*](https://arxiv.org/abs/2105.01363).
* J. McDonald, B. Mohar, and D. Scheide,
  [*Kempe equivalence of edge-colourings in subcubic and subquartic
  graphs*](https://arxiv.org/abs/1005.2248).

Until that global cage lemma is proved, the component-chain potential is
a sharply formulated proof route, not a resolution of FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the potential and
outside-handle classification, implemented the Python and C++ audits,
constructed the toroidal flag stress family, analyzed the exact outputs,
and drafted this note.  Complete source, machine-readable output, and
independent replay scripts are supplied for human inspection.  These
results have not undergone peer review.
