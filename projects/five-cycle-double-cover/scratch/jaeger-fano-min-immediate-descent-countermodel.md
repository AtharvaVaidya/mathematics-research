# A positive symmetric state with no one-exchange descent

Date: 2026-07-28

Status: **EXACT COUNTERMODELS TO IMMEDIATE STRICT DESCENT AND TO
FIXED-KERNEL EXPOSURE.  THEY DO NOT REFUTE DESCENT THROUGH A FULL
SAME-LEVEL COMPONENT AND ARE NOT COUNTEREXAMPLES TO FIVECDC.**

## Claim refuted

For a vertex-star tree packing, let
\[
 d_{\min}=\min_{0\ne h\in(\mathbb F_2^3)^*}d_h,
\]
where \(d_h\) is the number of components failing the exact five-point
component-parity criterion in Fano plane \(h\).  The tempting local claim

> every state with \(d_{\min}>0\) has an incident reciprocal two-tree
> exchange that strictly lowers \(d_{\min}\)

is false.

This is narrower than the same-level-component descent statement tested
in `jaeger-fano-minimum-parity-descent-through14.md`.  The state below
has a neutral exchange followed by a descending exchange.

## Literal graph and state

Use the graph6 record

```text
O??CA?_ceOGgH_F?AK@P?
```

with root \(13\).  In literal graph6-parser edge order, assign root
spokes

```text
(16, 17, 15)
```

to coordinates \(0,1,2\).  In the 21-edge internal order obtained by
deleting those spokes, take omitted-class masks

```text
(857601, 1059160, 180390).
```

The three spanning trees are

```text
T0 = {1,2,3,4,5,6,7,8,11,13,14,16,18,20,23}
T1 = {0,1,2,5,7,9,10,12,14,17,18,19,20,21,22}
T2 = {0,3,4,6,8,9,10,11,12,13,15,19,21,22,23}.
```

Their unique all-vertices-odd subgraphs are

```text
K0 = {2,3,4,5,7,11,13,16,20,23}
K1 = {0,1,2,5,7,9,14,17,18,22}
K2 = {0,3,6,9,13,15,19,21,22,23}.
```

Direct reconstruction gives the seven-plane profile

\[
                         (4,4,4,2,4,6,4),
\]

so \(d_{\min}=2>0\).

## Complete incident neighbourhood

Each omitted class has seven edges.  There are therefore exactly
\[
                  \binom32\,7^2=147
\]
candidate reciprocal exchanges.  Exactly 23 preserve both changed
spanning trees.  Their new minimum-score histogram is

```text
d_min = 2 : 18 exchanges
d_min = 4 :  5 exchanges
```

There is no neighbour with score \(0\), and hence no immediately
descending exchange.

## Exact neutral escape

Swap graph edge \(19\) from omitted class \(0\) with graph edge \(6\)
from omitted class \(1\).  The new masks are

```text
(792129, 1124632, 180390).
```

Both removed tree edges lie outside their old odd kernels.  The
odd-kernel exchange law therefore leaves all three \(K_i\), the
\(\mathbb F_2^3\)-flow, and the complete profile unchanged.

From that neutral state, swap graph edge \(22\) from omitted class \(0\)
with graph edge \(7\) from omitted class \(2\).  The masks become

```text
(267969, 1124632, 704550)
```

and the exact profile is

\[
                         (2,2,2,2,4,6,0).
\]

Thus a score-zero state is reached in exactly two exchanges: one
kernel-inert neutral move and one strict descent.  This explains why a
proof based on averaging only the exchanges incident with the current
state cannot establish the observed same-level-component theorem.
Any successful exchange proof must permit neutral rearrangements of the
underlying trees that alter which active exchanges are available.

## Fixed-kernel exposure is also false

The first example suggests a stronger repair: hold the three odd
kernels fixed, move by kernel-inert reciprocal exchanges, and ask that
some realization in this neutral component expose a descending
exchange.  That statement is also false.

In the same graph, root, spoke assignment, and internal-edge order, take

```text
(1722528, 307976, 66647).
```

Its exact profile is
\[
                         (4,4,4,4,6,2,2),
\]
so again \(d_{\min}=2\).  The complete incident neighbourhood has 147
candidate swaps and 23 legal swaps.  All 23 neighbours still have
\(d_{\min}=2\), and none preserves the ordered triple of odd kernels.
Consequently this state's component in the graph of realizations of its
fixed kernel triple is a singleton and no fixed-kernel motion can expose
a descending edge.

The full same-level route survives.  Swapping graph edge \(5\) from
omitted class zero with graph edge \(3\) from omitted class one gives

```text
(1722504, 308000, 66647)
```

with profile \((4,2,2,4,6,2,2)\).  This is an **active** same-level
exchange: it changes the kernel triple.  From there, swapping graph edge
\(20\) from class zero with graph edge \(12\) from class one gives

```text
(1595528, 434976, 66647)
```

with profile \((6,4,4,4,4,4,0)\).  Thus descent again occurs at distance
two, but the first move cannot be confined to a fixed-kernel realization
class.

The remaining possible theorem must therefore use the entire connected
same-\(d_{\min}\) component (including active neutral exchanges), or a
different global argument.  Neither immediate averaging nor a
fixed-kernel exposure lemma is sufficient.

## Independent reproduction

Run

```sh
python3 scratch/verify_jaeger_fano_min_immediate_descent_countermodel.py
```

The checker independently:

1. parses the literal graph6 record;
2. verifies simplicity, cubicity, and connectivity after deletion of
   every set of at most two edges;
3. reconstructs the three trees and their unique odd kernels;
4. recomputes the exact seven-plane profile;
5. exhausts all 147 candidate incident exchanges and checks the full
   neighbour-profile histogram;
6. reconstructs the kernel-inert intermediate state and the descending
   second step for the first example;
7. exhausts the second state's neighbourhood, verifies that all 23
   legal neighbours remain at score two and that none preserves the
   kernel triple; and
8. reconstructs its active same-level step and descending second step.

## Scope

These are finite countermodels to immediate one-exchange strict descent
and fixed-kernel exposure.  They support rather than refute the broader
possibility of descent through connected full same-level plateaux.  They
say nothing adverse about the standard Five-Cycle Double Cover
Conjecture.

## AI-use disclosure

OpenAI Codex, under human direction, found both states during exploratory
exact-neighbour searches, independently replayed them, derived the two
distinct two-step mechanisms, implemented the standalone checker, and
drafted this note.  Every finite assertion above is reproduced from the
literal graph and masks by the checker.
