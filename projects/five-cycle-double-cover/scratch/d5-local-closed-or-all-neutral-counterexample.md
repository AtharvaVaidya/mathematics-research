# An order-14 counterexample to the closed-or-all-neutral dichotomy

Date: **2026-07-28**

Status: **EXACT LOCAL REFUTATION / NOT A COUNTEREXAMPLE TO FiveCDC**.

## Statement refuted

Let \(q\) be a \(D_5\)-flow on a cubic graph.  Fix two incident graph
edges.  Exactly three factors \(Y_P\) are active on both edges.  For the
component \(K_P\) through those edges, let \(B(P,K_P)\) be the set of
edges labelled exactly \(P\) having one endpoint in \(V(K_P)\) and the
other outside.  The following proposed dichotomy is false:

> Either some \(B(P,K_P)\) is empty, or all three switches on \(K_P\)
> have \(\Delta\chi=0\).

## Explicit witness

The graph is the simple cubic graph

```text
M???FBObB_DOD_B_?
```

in graph6.  In the standard graph6 upper-triangle edge order, its edges
and two-subset labels (written as hexadecimal bit masks on
\(\{0,1,2,3,4\}\)) are:

| edge | endpoints | label | edge | endpoints | label |
|---:|:---:|:---:|---:|:---:|:---:|
| 0 | 0--7 | 03 | 11 | 3--10 | 0c |
| 1 | 1--7 | 05 | 12 | 2--11 | 03 |
| 2 | 2--7 | 06 | 13 | 4--11 | 09 |
| 3 | 0--8 | 0a | 14 | 6--11 | 0a |
| 4 | 1--8 | 0c | 15 | 3--12 | 0a |
| 5 | 3--8 | 06 | 16 | 5--12 | 09 |
| 6 | 0--9 | 09 | 17 | 6--12 | 03 |
| 7 | 4--9 | 18 | 18 | 4--13 | 11 |
| 8 | 5--9 | 11 | 19 | 5--13 | 18 |
| 9 | 1--10 | 09 | 20 | 6--13 | 09 |
| 10 | 2--10 | 05 | | | |

At vertex \(2\), take edges \(10\) and \(12\), labelled
\(\{0,2\}\) and \(\{0,1\}\).  The three pairs active on both are
\[
                         03,\qquad 04,\qquad 12.
\]
Their factor components and boundary sets are:

| \(P\) | \(E(K_P)\) | \(B(P,K_P)\) | \(\Delta\chi\) |
|:---:|:---|:---|---:|
| 03 | 10,11,12,14,15,17 | 9,13,16,20 | \(+2\) |
| 04 | 0,1,6,7,9,10,12,13 | 8,18 | \(0\) |
| 12 | 10,11,12,14,15,17 | 2,5 | \(0\) |

Thus all three boundary sets are nonempty, while the changes are
\((2,0,0)\), not \((0,0,0)\).

For a direct component-count check, before switching,
\[
              (\kappa(C_0),\ldots,\kappa(C_4))=(1,1,1,1,1),
              \qquad \chi=5-7=-2.
\]
The standalone checker prints the five component counts after every
switch and verifies that their sum changes by the values in the table.

## Why this is a valid \(D_5\)-flow

Every displayed label has exactly two bits.  At each vertex, the XOR of
the three incident labels is zero.  Equivalently, every coordinate
occurs an even number of times among the three incident edges, so each
\(C_i\) is Eulerian.  The checker verifies these equations directly.
It also decodes the graph6 string independently and verifies simplicity,
cubicity, connectedness, and bridgelessness by deleting each edge in
turn.

## Reproduction

```text
python3 scratch/check_d5_local_closed_or_all_neutral_counterexample.py
```

The script is standalone and imports no project module.

## Consequence

The sufficient fact
\[
                         B(P,K_P)=\varnothing
                         \quad\Longrightarrow\quad
                         \Delta\chi=0
\]
is not challenged.  What fails is the attempted three-way strengthening.
Any terminal-plateau proof must therefore use the weaker universal
zero-neutrality lemma, terminality, or more global circuit-interlacement
data; boundary nonemptiness alone does not force simultaneous neutrality.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the candidate in an
exact finite search, reduced it to the explicit table above, wrote the
independent checker, and drafted this note.  The witness is fully
checkable without trusting an AI system or the original census code.
