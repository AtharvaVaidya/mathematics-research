# Disjoint-factor mediator distance through order 12

Date: **2026-07-28**

Status: **COMPLETE FINITE CENSUS / THE TWO-SWITCH PATTERN IS FALSE
IN GENERAL**.

## Claim tested

Let \(q\) be a \(D_5\)-flow, let \(P,Q\in\binom{[5]}2\) be disjoint,
and let \(A,B\) be intersecting circuit components of \(Y_P,Y_Q\).
For each \(e\in A\), \(g\in B\), measure the minimum number of legal
componentwise Kempe switches needed to reach a state in which some
factor circuit contains \(e,g\).

The complete order-12 census found maximum distance two.  A separate
40-vertex witness in `scratch/d5-disjoint-two-switch-no-go.md` shows
that this finite pattern is not a theorem: distance three can be
necessary.

## Exact order-12 result

Nauty's

```text
geng -Cq -d3 -D3 12
```

generates all 81 biconnected simple cubic graphs of order 12.  The audit
enumerated every \(D_5\)-flow modulo global \(S_5\), constructed every
Kempe orbit, and tested every distinct state/root requirement generated
by a pair of intersecting circuits of disjoint factors.

| quantity | count |
|---|---:|
| graphs | 81 |
| normalized \(D_5\)-flows | 25,960 |
| Kempe orbits | 2,650 |
| required state/root pairs | 3,970,092 |
| already rooted at distance 0 | 3,783,384 |
| first rooted at distance 1 | 181,065 |
| first rooted at distance 2 | 5,643 |
| distance greater than 2 | **0** |

The machine-readable report is
`scratch/d5-disjoint-mediator-distance-order12.json`.

## Independent check

The producer propagates bit sets through complete Kempe orbit graphs.
The verifier independently:

1. regenerates all 81 graph6 records and checks every report total;
2. hard-codes the aggregate arithmetic above; and
3. selects five deterministic boundary/extremal rows and directly
   expands the radius-zero, radius-one, and radius-two neighborhoods
   from each state, recomputing the complete distance histogram.

This is a focused semantic replay, not a second full 81-graph distance
census.  Its scope is explicit in its `PASS` output.

## Structural interpretation

For disjoint \(P=01,Q=23\), with fifth coordinate \(4\), the edge-label
regions are

\[
\begin{array}{c|c}
({\bf1}_{Y_P},{\bf1}_{Y_Q})&\text{labels}\\ \hline
11&P\times Q\\
10&P\times\{4\}\\
01&Q\times\{4\}\\
00&\{P,Q\}.
\end{array}
\]

At a cubic contact where an \(A\)-branch, a \(B\)-branch, and a common
branch meet, the local label triangle is \(\{p,q,4\}\).  This makes the
fifth coordinate the unique mediator between the two disjoint factor
pairs.  It explains the short rescues in small graphs, but it does not
control global component interlacement.  The order-40 distance-three
witness is the exact obstruction to upgrading this census pattern into
a two-switch lemma.

Thus the surviving rooted-transitivity route needs an unbounded
component-chain argument or a global monotone invariant.

## Reproduction

```text
python3 scratch/audit_d5_disjoint_mediator_distance_order12.py \
  --output scratch/d5-disjoint-mediator-distance-order12.json

python3 scratch/verify_d5_disjoint_mediator_distance_order12.py
```

## AI-use disclosure

OpenAI Codex agents, under human direction, designed and ran the exact
census, wrote the focused independent verifier, discovered the
order-40 counterexample to the apparent bound, and drafted this note.
These computations are finite evidence and proof-strategy diagnostics,
not peer review or a resolution of FiveCDC.
