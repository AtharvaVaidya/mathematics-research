# The order-18 six-bad flow is locked to a cyclic three-cut

Date: 2026-07-28

Status: **HUMAN-CHECKABLE ROUTE EXCLUSION / SOLVER-INDEPENDENT COMPLETE
LOCAL ENUMERATION / NOT A FIVE-CDC RESOLUTION**.

## 1. Scope

This note corrects a mistaken exploratory description of the flow

```text
graph6  Q???C@?K@O@aDAw?GW?J?_g?Y??
flow    1 5 6 5 3 4 6 5 3 3 4 7 2 7 5 2 5 7 1 6 7 3 1 2 6 2 4
```

in graph6 edge order.  The graph is simple, cubic, 3-edge-connected,
girth five, and non-3-edge-colourable, but it is **not** cyclically
4-edge-connected.  It has the cyclic three-cut

\[
 e_{14}=(2,13),\qquad e_{18}=(5,15),\qquad e_{26}=(6,17).
\]

The two shores are

\[
\begin{aligned}
A&=\{2,3,4,5,9,10,11,12,17\},\\
B&=\{0,1,6,7,8,13,14,15,16\}.
\end{aligned}
\]

Each shore has nine vertices and twelve induced edges, and each induced
subgraph is connected.  Thus each shore contains a cycle, so the displayed
cut is cyclic.

The correction matters because the flow has six uncleanable Fano
projections and looked like a promising building block for a cyclically
4-edge-connected seven-projection obstruction.  The theorem below shows
that this entire composition route is topologically locked to the same
three-cut.

This concerns the stronger auxiliary assertion that every fixed
nowhere-zero \(\mathbb F_2^3\)-flow has a clean projection.  It neither
proves nor disproves FiveCDC.

## 2. Exact local pole formula

Delete the endpoints of an edge \(e\).  The result is a four-pole with
22 proper edges and four semiedges.  Fix a nonzero functional \(\mu\).
Let \(Z_\mu\) be the proper edges and semiedges whose flow value lies in
\(\ker\mu\).

The completion-sound local two-cycle formula asks for two binary pole
cycles \(p,q\), meaning that each has even incidence at every one of the
16 proper vertices, such that:

1. \(Z_\mu\subseteq p\cup q\); and
2. for every component \(K\) of the proper \(Z_\mu\)-edge graph that
   touches no \(Z_\mu\)-semiedge,
   \[
        |\,\delta(K)\cap p\cap q\,|\equiv0\pmod2,
   \]
   where \(\delta(K)\) includes semiedges incident with \(K\).

The formula is necessary in every completion.  Restrict global cleaning
cycles to the pole.  Their vertex parities and coverage give condition 1.
A zero-edge component with no zero semiedge cannot merge with a component
outside the pole, so its global defect equation is exactly condition 2.
Consequently local UNSAT is preserved by arbitrary gluing.

The formula is also the exact local existential condition when the
outside is left unrestricted: components touching a zero semiedge export
their signed defect and impose no local parity equation.  This is the
four-terminal specialization of the signed-partition composition law in
`fano-clean-line-signed-partitions-20260728.md`.

## 3. Complete local profile

The solver-independent checker row-reduces the 16 by 26 pole incidence
matrix.  Every deleted-edge pole has exactly \(2^{10}=1024\) binary pole
cycles.  It directly tests all relevant ordered pairs of cycles—without a
SAT solver—and obtains:

| deleted edge location | edge ids | locally UNSAT functionals |
|---|---|---|
| inside \(B\) | `0,1,12,13,15,16,17,19,20,21,22,23` | `4,5,6` |
| inside \(A\) | `2,3,4,5,6,7,8,9,10,11,24,25` | `1,3,7` |
| the cyclic three-cut | `14,18,26` | none |

Thus the histogram is

```text
12 poles with profile {4,5,6}
12 poles with profile {1,3,7}
 3 poles with profile {}
```

The checker emits explicit hexadecimal \(p,q\) witnesses for every
locally satisfiable functional, so both the positive and negative sides of
the table are replayable by finite enumeration.

## 4. Three-cut lock

Suppose the deleted edge lies inside \(A\).  Its endpoints are in \(A\),
so all nine vertices of \(B\), all twelve edges induced by \(B\), and the
three incidences of the original cut remain in the four-pole.  Some cut
incidences may have become semiedges, but the boundary of \(B\) in the
pole still has size three.  Hence the pole contains the connected cyclic
shore \(B\) behind a three-boundary.  The same argument with \(A\) and
\(B\) exchanged applies when the deleted edge lies inside \(B\).

The only deletions that avoid such a retained cyclic shore are the three
cut edges, and their local UNSAT profile is empty.

It follows that every pole from this flow with a nonempty local
obstruction profile contains a cyclic subgraph separated from its four
ports by three edges.  In any completion whose outside contains a cycle,
those three edges form a cyclic three-cut.  In particular:

> **Three-cut-lock theorem.**  No composition of two or more of these
> deleted-edge four-poles can both (i) obtain a seven-functional
> obstruction by taking the union of completion-sound local UNSAT
> profiles and (ii) be cyclically 4-edge-connected.

Applying an element of \(\mathrm{GL}(3,2)\) only relabels the seven flow
values and functionals.  It changes neither the empty/nonempty status of a
local profile nor the retained three-boundary, so arbitrary linear
relabeling does not evade the theorem.

This explains two earlier computational observations:

- two compatible relabelled poles never supplied a cyclically
  4-edge-connected all-seven construction; and
- the order-26 all-seven flow obtained by a Petersen graft retained
  cyclic three-cuts.

The theorem closes this particular building-block strategy.  It gives no
reason that a different cyclically 4-edge-connected flow cannot obstruct
all seven projections.

## 5. Reproduction

Run:

```bash
python3 scratch/verify_fano_six_bad_threecut_lock.py
```

The checker uses only the Python standard library.  It:

1. decodes the exact graph6 record and checks cubicity and all flow
   equations;
2. checks the displayed cut, shore connectivity, and induced edge counts;
3. constructs all 27 deleted-edge four-poles;
4. independently enumerates each 1024-element pole cycle space;
5. evaluates the exact local two-cycle formula for all seven functionals;
6. checks the complete profile table; and
7. verifies the retained cyclic shore and boundary size for every
   obstructive deletion.

## 6. AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, found the candidate flow,
formulated and tested the local pole abstraction, discovered the
three-cut lock, wrote the checker, and drafted this note.  The proof and
finite enumeration are exposed for human checking.  This is not
independent human verification or peer review.
