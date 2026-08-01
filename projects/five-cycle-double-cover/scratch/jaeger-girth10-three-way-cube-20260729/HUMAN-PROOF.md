# Human-checkable proof and trust boundary

## Exact finite statement

There is a rooted Jaeger three-tree state on a simple cubic,
three-edge-connected, cyclically five-edge-connected graph of girth ten
with three pairwise-disjoint reciprocal exchanges \(A,B,C\) such that:

1. all eight subset states are legal;
2. none of the seven proper-subset states has a successful parallel span
   flag or potential below the seed; and
3. the full state \(ABC\) has smaller potential.

Moreover, all six fundamental-circuit sides along the path
\[
 S\longrightarrow A\longrightarrow AB\longrightarrow ABC
\]
have length at least ten.  Thus a proper-subset-safe three-way
interaction does not force either a graph circuit of length at most nine
or a cyclic edge cut of size at most four.

This does not say that the seed's global escape distance is three.  The
checker verifies a different two-exchange escape.  Consequently the
result rules out one proposed localization proof, but does not refute a
high-girth radius-two theorem and does not resolve FiveCDC.

The host graph is Tait-colourable, so a Tait colour class is a perfect
matching whose complementary two-factor has only even circuits; its
exact oddness is zero.  It is therefore not a snark and lies outside
the non-Tait, oddness-at-least-six minimal-counterexample domain.  The
witness tests the proposed high-girth/high-connectivity localization
lemma only.

## The witness

Use the 130-vertex 13-lift of the Petersen graph in
`../../artifacts/structured/graphs/lift13_petersen_girth10.json`, with
edges sorted in graph6 order and root \(0\).  The root spokes have edge
IDs \(4,39,70\).  The other 192 edges are partitioned into omitted
classes by the masks in `WITNESS.json`.

The parent project's retained exact oddness census records this graph as
oddness zero, hence Tait-colourable.  The statement proved here is therefore
a high-girth control outside the snark and minimal-counterexample domains.

For coordinate \(i\), adjoining root spoke \(i\) to the complement of
omitted class \(i\) gives a spanning tree \(T_i\).  Its unique all-odd
edge subset is \(K_i\).  As elsewhere in the project, the potential is
\[
 \Psi=(d_{\min},|K_0|+|K_1|+|K_2|)
\]
with lexicographic order, and a successful parallel
component--circuit span flag is terminal below every positive
potential.

The three local-position exchanges are
\[
 A=(0,102),\qquad B=(41,153),\qquad C=(178,78).
\]
Their coordinate pairs are \(01,12,01\), and all six local positions
are distinct.  Direct reconstruction gives:

| subset | kernel sizes | profile | flags | \(\Psi\) |
|---|---|---|---:|---:|
| \(\varnothing\) | `(72,69,69)` | `(22,28,14,24,16,14,2)` | 0 | `(2,210)` |
| \(A\) | `(72,69,69)` | `(22,28,14,24,16,14,2)` | 0 | `(2,210)` |
| \(B\) | `(72,70,68)` | `(20,22,10,26,16,14,2)` | 0 | `(2,210)` |
| \(AB\) | `(72,70,68)` | `(20,22,10,26,16,14,2)` | 0 | `(2,210)` |
| \(C\) | `(73,69,69)` | `(20,26,14,26,14,20,6)` | 0 | `(6,211)` |
| \(AC\) | `(71,67,69)` | `(18,26,12,24,12,16,4)` | 0 | `(4,207)` |
| \(BC\) | `(73,70,68)` | `(20,20,14,30,10,22,6)` | 0 | `(6,211)` |
| \(ABC\) | `(71,70,68)` | `(20,22,10,24,16,14,2)` | 0 | `(2,209)` |

The first exchange is kernel- and flow-neutral.  Along the displayed
path, the two fundamental-circuit sides of each exchange are:

| exchange | coordinate | length | active? | \(|C\cap K|\) |
|---|---:|---:|---:|---:|
| \(A\) | 0 | 32 | no | 14 |
| \(A\) | 1 | 10 | no | 5 |
| \(B\) after \(A\) | 1 | 29 | yes | 14 |
| \(B\) after \(A\) | 2 | 11 | yes | 6 |
| \(C\) after \(AB\) | 0 | 11 | yes | 6 |
| \(C\) after \(AB\) | 1 | 16 | no | 7 |

For an active side the odd-kernel size change is
\(|C|-2|C\cap K|\).  Hence \(B\)'s two active sides change sizes by
\(+1\) and \(-1\), while \(C\)'s active side changes size by \(-1\).
This explains the kernel-sum part of the exact cube without appealing
to numerical approximation.

The seed itself is an augmented trap.  Exhausting all
\(3\cdot64^2=12,288\) candidate reciprocal swaps leaves 382 legal
neighbors, 90 of them equal-potential.  None is lower or successful.
Nevertheless,
`(0,102)` followed by `(124,153)` reaches profile
`(24,20,14,24,16,14,2)`, kernel sizes `(72,69,68)`, zero flags, and
\(\Psi=(2,209)\).  Thus the seed's exact augmented escape distance is
two, outside the displayed three-exchange cube.

## Graph structure

The Python verifier checks simplicity, cubicity, connectedness after
deleting every zero-, one-, or two-edge set, and girth ten.

`check_cyclic5.cpp` exhausts all 1,216,865 triples of edges.  It finds
130 disconnecting triples, none separating two cyclic components.  To
cover four-edge cuts, after deleting each triple it finds every bridge.
Any four-edge cut is found this way: after restoring any one of its
four crossing edges, that edge is a bridge between the separated
sides.  The checker classifies all 25,155 distinct four-edge cuts and
finds none separating two cyclic components.  Together with
three-edge-connectivity, this proves cyclic five-edge-connectivity.

## Portfolio comparison

`audit_portfolio_circuits.py` rechecks the two-step certificates for all
196 augmented traps in the frozen 13-run lift portfolio.  This is an
exact audit of a deterministic sample, not of the graph's full state
space.

Of those 196 paths, 194 use disjoint exchanges, 181 have a first
exchange inactive on both sides, and every second exchange is active on
at least one side.  All 784 path-side circuits have length at least ten.
Among the 144 disjoint paths for which the second swap is also legal at
the seed, the neutral first step changes a second fundamental circuit in
133 cases.  High girth therefore does not remove tree-basis memory.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, designed and ran the
search and audits, found the witness, wrote the independent verifier,
derived the circuit interpretation, and drafted this note.  No
independent human peer review has occurred.
