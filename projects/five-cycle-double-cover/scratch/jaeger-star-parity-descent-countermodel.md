# A trapped singleton for star-fibre parity descent

Date: 2026-07-28

Status: **EXACT COUNTERMODEL TO FIXED-COORDINATE MONOTONE
EXCHANGE-DESCENT ONLY.  IT DOES NOT REFUTE THE SYMMETRIC MINIMUM
POTENTIAL AND IS NOT A COUNTEREXAMPLE TO FIVECDC.**

## Claim being tested

Fix a vertex-star fibre of a cubic graph and fix coordinate \(2\).  For a
tree triple \((T_0,T_1,T_2)\), let \(K_i=K(T_i)\) be the unique
all-vertices-odd subgraph of \(T_i\), and let
\[
 d(T_0,T_1,T_2)=
 \#\{Q\in\operatorname{comp}(K_2):
 |\delta(Q)\cap K_0\cap K_1|\equiv1\pmod2\}.
\]
The fixed-coordinate version of the proposed lemma said that every
connected component of every positive level set \(d^{-1}(k)\), under
reciprocal two-tree symmetric exchanges, has an exchange edge to a lower
level.

The explicit state below is a singleton component of \(d^{-1}(2)\).  All
of its legal exchange neighbours have defect \(4\), so the claim is false.

## Graph and state

The graph is the canonical graph6 record

```text
M?AA@BORDGEOEOAo?
```

It is record 244 in zero-based order in
`geng -Cq -d3 -D3 14` (line 245).  Numbering the edges as the graph6
parser does gives

```text
 0: 0-5     1: 1-6     2: 2-7     3: 0-8
 4: 1-8     5: 3-8     6: 1-9     7: 4-9
 8: 5-9     9: 0-10   10: 2-10   11: 5-10
12: 2-11   13: 3-11   14: 6-11   15: 3-12
16: 4-12   17: 7-12   18: 4-13   19: 6-13
20: 7-13
```

The exact checker verifies simplicity, cubicity, and connectivity after
every deletion of zero, one, or two edges.  Thus the graph is
3-edge-connected.

Take root \(0\), with its spokes assigned in edge order:
\[
 (s_0,s_1,s_2)=(0,3,9).
\]
The three omitted internal-edge classes are
\[
\begin{aligned}
 A_0&=\{2,5,10,14,16,18\},\\
 A_1&=\{4,6,8,12,13,20\},\\
 A_2&=\{1,7,11,15,17,19\}.
\end{aligned}
\]
They partition the 18 non-spoke edges.  Set
\(T_i=\{s_i\}\cup(E_{\rm int}-A_i)\).  Explicitly,
\[
\begin{aligned}
T_0={}&\{0,1,4,6,7,8,11,12,13,15,17,19,20\},\\
T_1={}&\{1,2,3,5,7,10,11,14,15,16,17,18,19\},\\
T_2={}&\{2,4,5,6,8,9,10,12,13,14,16,18,20\}.
\end{aligned}
\]
Each listed set is connected and has 13 edges on 14 vertices, hence is a
spanning tree.

The all-vertices-odd subgraphs of these trees are
\[
\begin{aligned}
K_0={}&\{0,1,4,6,7,8,11,12,15,20\},\\
K_1={}&\{1,2,3,7,11,14,15,19\},\\
K_2={}&\{4,8,9,12,13,14,16,20\}.
\end{aligned}
\]
For a human check, each \(K_i\) is a subset of \(T_i\), and direct degree
counting shows odd degree at every vertex.  Such a subgraph is unique in a
tree, so these are exactly the \(K(T_i)\).

Now
\[
 K_0\cap K_1=\{1,7,11,15\}.
\]
The components of \(K_2\) are
\[
\{0,10\},\{1,8\},\{2,3,6,11\},\{4,12\},\{5,9\},\{7,13\}.
\]
The four intersection edges, in the same order, join component pairs
\[
(1,3),\ (4,5),\ (5,0),\ (3,4).
\]
Therefore precisely components \(\{0,10\}\) and \(\{1,8\}\) have odd
boundary, and \(d=2\).

## Exhaustion of the exchange neighbourhood

A reciprocal exchange between coordinates \(i,j\) is exactly a swap of
one edge in \(A_i\) with one edge in \(A_j\) for which both new
complements are spanning trees.  There are
\(\binom32\cdot6\cdot6=108\) candidates.  Exactly the following 18 are
legal; the entries are `(coordinates; edge from first class, edge from
second class)`:

```text
(0,1;  2,12)  (0,1;  5, 4)  (0,1; 10, 8)
(0,1; 14,13)  (0,1; 16,20)  (0,1; 18, 6)

(0,2;  2,15)  (0,2;  5, 1)  (0,2; 10,11)
(0,2; 14,19)  (0,2; 16,17)  (0,2; 18, 7)

(1,2;  4, 1)  (1,2;  6, 7)  (1,2;  8,11)
(1,2; 12,19)  (1,2; 13,15)  (1,2; 20,17)
```

Recomputing the three odd-side forests and contracted boundary parities
after each exchange gives defect \(4\) in all 18 cases.  The remaining
90 candidates fail the spanning-tree condition in at least one changed
coordinate.  Consequently the displayed state has no same-level
neighbour and no lower-level neighbour.  It is a trapped singleton in
level \(2\).

The independent Python checker reconstructs the graph from graph6,
checks 3-edge-connectivity, checks the three trees and odd cores, and
exhausts all 108 candidate exchanges:

```sh
python3 scratch/verify_jaeger_star_parity_descent_countermodel.py
```

Its decisive output is:

```json
{
  "witness_score": 2,
  "valid_exchange_neighbours": 18,
  "neighbour_score_histogram": {"4": 18},
  "verified_trapped_singleton": true
}
```

The separate C++ whole-state enumerator finds 221,760 states in this
rooted fibre and independently reports the same masks, level, and
singleton component:

```sh
clang++ -O3 -std=c++20 scratch/search_jaeger_star_parity_descent.cpp \
  -o /tmp/search_jaeger_star_parity_descent
printf '%s\n' 'M?AA@BORDGEOEOAo?' |
  /tmp/search_jaeger_star_parity_descent --root 0 --objective fixed
```

It also checked root \(0\) of all 341 3-edge-connected graphs among the
480 canonical connected cubic graphs of order 14: 60,091,776 states in
total.  This was the only failed rooted instance in that bounded run.
That larger census is corroboration; the local 108-case verification is
already a complete countermodel.

SHA-256:

```text
c087d9de1e8193680f7293543a5d6bd3a3fe95515ca74df6aedc26a852dbe7a5  scratch/search_jaeger_star_parity_descent.cpp
8fae5e357ce6e44d59c28d5a07ea28b70320cf3f6ab70c29ce962ad9b76e3593  scratch/verify_jaeger_star_parity_descent_countermodel.py
```

## Consequence

Neutral reciprocal symmetric exchanges are not sufficient to guarantee
descent of one preselected coordinate's defect count, even when exchanges
involving the third tree are allowed.  This does not rule out a symmetric
potential which takes the minimum over coordinate or Fano planes.

Indeed, in functional order \(h=1,\ldots,7\), the witness's exact
seven-plane defect profile is
\[
                         (2,4,2,2,0,6,2).
\]
Thus it is already support-five-good in plane \(h=5\).  Even if one
temporarily restricts to the three coordinate planes \(h=1,2,4\), the
legal exchange `(coordinates 1,2; graph edges 4,1)` changes the profile
to
\[
                         (0,2,4,4,2,2,2),
\]
and hence immediately lowers the three-coordinate minimum from \(2\) to
\(0\).  The state is therefore **not** trapped for either symmetric
minimum objective.

This countermodel does **not** obstruct the target parity condition
itself: the same rooted fibre has many defect-zero states.  Hence it is
not evidence against FiveCDC and is not presented as a resolution of
that conjecture.

## AI-use disclosure

OpenAI Codex, under human direction, formulated and tested the descent
claim, found the finite countermodel, implemented both checkers, and
drafted this note.  Every asserted finite fact above is reproducible
from the explicit graph and state.
