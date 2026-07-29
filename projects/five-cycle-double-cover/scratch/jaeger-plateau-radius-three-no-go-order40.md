# Three neutral layers can be necessary in a Jaeger plateau

Date: 2026-07-28

Status: **EXACT FINITE COUNTERMODEL TO A RADIUS-THREE
STRENGTHENING OF THE PLATEAU ROUTE.  THE FULL PLATEAU COMPONENT
ESCAPE STATEMENT REMAINS OPEN.  THIS IS NOT A FIVE-CYCLE DOUBLE COVER
COUNTEREXAMPLE.**

## 1. Precise claim and conclusion

Fix a vertex-star packing state \(s=(T_0,T_1,T_2)\).  Two states are
adjacent when one legal reciprocal exchange moves one nonroot edge
between each of two omitted classes, so that the two changed
complements remain spanning trees.  Let
\[
 d(s)=\min_{0\ne h\in(\mathbb F_2^3)^*}d_h(s)
\]
be the minimum of the seven exact component-parity defects.

For a positive level-\(q\) state, define its plateau distance to another
state to be the length of a path all of whose vertices before the last
have defect \(q\).  The following bounded strengthening of the surviving
plateau proposal is false:

> Every positive Jaeger star state has a lower-defect state at plateau
> distance at most three.

The literal state below has \(d(s)=2\), has no lower-defect state at
plateau distance at most three, and has one at distance four.  Thus its
exact plateau escape distance is four.

This result does **not** refute the unbounded statement that the full
connected same-\(d\) component always has a lower boundary edge.

## 2. Literal graph and state

Use the standard graph6 record

```text
ghe?GC@@G??@?@??_@I??A?C_?G??G@?CA?@?C?G_??_@?@???@?@??_?C?G??C@?O??C?A??G????G????C????@??O??G?????_????H????_@?????G_????@G??_?C@
```

The decoded graph is simple, cubic, has 40 vertices and 60 edges, and
remains connected after deletion of every set of at most two edges.
Take root \(0\).  In literal graph6 edge order its incident edges are
\(\{0,3,5\}\); assign the spokes to coordinates in the order
\[
                         (3,0,5).
\]

Delete the three spokes from edge order.  The remaining 57 positions
are the internal-edge order.  The three omitted classes are the
19-bit masks

```text
(95184251351218348, 47576007214007363, 1354929510630160).
```

They partition the internal edges.  Complementing each class and
adjoining its assigned spoke gives a 39-edge spanning tree.  The unique
all-vertices-odd subforests of those trees induce the ordered seven-plane
profile
\[
                         (8,2,8,8,6,10,10),                 \tag{1}
\]
so \(d(s)=2\).

The SHA-256 digest of the canonical JSON containing the graph, root,
spokes, start state, and displayed escape path is

```text
675a4216436209f769074c8dc452630c1a67b961f21fb88cd436255587708538
```

## 3. The exact state-graph separator

Let \(L_j\) be the set of level-2 states at plateau distance exactly
\(j\) from \(s\), and put \(B_3=L_0\cup L_1\cup L_2\cup L_3\).
Complete breadth-first reconstruction gives

| layer | \(|L_j|\) |
|---:|---:|
| 0 | 1 |
| 1 | 13 |
| 2 | 108 |
| 3 | 836 |
| **total** | **958** |

Each state has three omitted classes of 19 edges.  Therefore the audit
tests exactly
\[
              958\cdot 3\cdot19^2=1{,}037{,}514
\]
candidate swaps.  Exactly 67,392 are legal oriented exchange arcs.
Their target score, when it differs from two, is:

| source layer | score 0 | score 4 | score 6 | score 8 |
|---:|---:|---:|---:|---:|
| 0 | 0 | 38 | 14 | 0 |
| 1 | 0 | 508 | 174 | 0 |
| 2 | 0 | 4,276 | 1,317 | 8 |
| 3 | 32 | 32,591 | 8,997 | 103 |

The remaining 19,334 legal arcs have score two.  In particular:

- no state in \(L_0\cup L_1\cup L_2\) has a score-zero boundary edge;
- exactly 32 oriented score-zero boundary edges leave \(L_3\).

Consequently \(B_3\) is an explicit three-layer separator in the
reciprocal-exchange graph: every level-preserving path from \(s\) to a
lower score uses at least three neutral exchanges and then one
descending exchange.  This is the finite obstruction behind the
failure of every radius-three plateau lemma; it is stronger than a
one-state local minimum.

For reproducibility, canonical lexicographic JSON encodings have hashes

```text
complete radius-three plateau ball:
51aa4f3ff1efa9bebcffe0f2869919c7bd25d60c2047f8b5383b8be90d435c58

all 67,392 examined legal oriented arcs with target scores:
d2ad5a4bb090e43efffba60e51dec5c66037cf10465b7c43f86a2c5b3407c4ce
```

These digests are regression identifiers, not substitutes for checking:
the standalone program reconstructs the sets and asserts the hashes.

## 4. A shortest escape

One shortest literal path has profiles

```text
(8,2,8,8,6,10,10)
(8,2,8,8,6,10,10)
(6,2,8,6,10,6,6)
(2,4,8,8,6,6,8)
(4,6,6,8,8,10,0)
```

and omitted masks

```text
(95184251351218348, 47576007214007363, 1354929510630160)
(95183701612181676, 47576556953044035, 1354929510630160)
(95183701612705836, 47576556953044035, 1354929510106000)
(95183727382509612, 47576556953044035, 1354903740302224)
(77169328873060396, 65590955462493251, 1354903740302224).
```

In graph edge IDs, with endpoints shown as a human-readable check, the
four reciprocal exchanges are:

| step | coordinates | exchanged graph edges |
|---:|:---:|:---|
| 1 | \(0,1\) | \(27=(20,21)\), \(42=(28,29)\) |
| 2 | \(0,2\) | \(10=(8,9)\), \(22=(8,19)\) |
| 3 | \(0,2\) | \(36=(25,26)\), \(38=(26,27)\) |
| 4 | \(0,1\) | \(18=(15,16)\), \(57=(15,39)\) |

The first three targets remain at level two.  The fourth has a zero in
functional \(h=7\).

## 5. Human proof of the finite conclusion

The finite argument has only four ingredients.

1. For each coordinate, complement its omitted mask among the 57
   internal edges and add its spoke.  A union-find or deletion
   connectivity test verifies that each result is a spanning tree.
2. In a tree, an edge belongs to the unique all-vertices-odd subforest
   exactly when the component below that edge has odd order.  This
   reconstructs the three odd kernels without a solver.
3. Label an edge by coordinate \(i\) when it is absent from kernel
   \(K_i\).  For each nonzero functional \(h\), form the zero-plane
   subgraph and xor the exact leaf charges component by component.  The
   number of nonzero component charges is \(d_h\).
4. For every pair of omitted classes and every ordered choice of one
   edge from each, toggle the two positions and retain the candidate
   exactly when both changed complements are spanning trees.  Ordinary
   breadth-first search restricted to score two produces the four
   layers and boundary table above.

The table proves the lower bound four; the displayed path proves the
upper bound four.  No SAT answer or discovery-program trace is used in
this proof.

## 6. Independent reproduction and scope

Run

```sh
python3 scratch/verify_jaeger_plateau_escape_radius4_order40.py
```

The checker uses only the Python standard library.  It independently
decodes graph6, checks simplicity/cubicity/three-edge-connectivity,
reconstructs all trees and odd kernels, checks the derived nowhere-zero
\(\mathbb F_2^3\)-flow, recomputes every component defect, enumerates the
complete radius-three plateau ball and its boundary, asserts every
count and digest, and replays the shortest escape.

The C++ audit

```sh
clang++ -O3 -std=c++20 -I/opt/homebrew/include \
  scratch/audit_jaeger_plateau_component_literal.cpp \
  /opt/homebrew/lib/libcadical.a -o /tmp/audit_jaeger_plateau
```

was the discovery implementation.  The Python checker is independently
written and does not import, invoke, or trust it.

The full same-level component is much larger than \(B_3\), and the
displayed state escapes.  Thus this package neither supplies a trapped
component nor proves the full plateau theorem.  The underlying graph
has a standard FiveCDC witness in the separate direct-search corpus, so
it is not a counterexample to FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the state by exact
exchange search, isolated the three-layer separator, wrote the
independent checker, and drafted this note.  Every finite assertion is
specified above and mechanically reproducible.  It has not received
independent human peer review.
