# One-flow simultaneous external coverage

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE REDUCTION / COMPLETE FINITE CENSUS THROUGH ORDER
14 / NOT A UNIVERSAL THEOREM / NOT A PROOF OF FIVECDC**.

## 1. Definitions

Let `D5` be the ten weight-two vectors of `F_2^5`.  A `D5` flow on a cubic
graph assigns a member of `D5` to every edge and has xor zero at every
vertex.  For a coordinate pair `P`, let `Y_P` consist of the edges whose
labels meet `P` in exactly one coordinate.  Every `Y_P` is an even subgraph.

Fix a cap vertex `z`, order its three incident edges as physical ports
`a,b,c`, and fix an edge `r` not incident with `z`.  A factor component
through `r` and two cap ports is *external* when its coordinate pair is
disjoint from the label on the inactive third cap edge.  Equivalently, after
normalizing the cap labels to `01,02,12`, it uses one of the two coordinates
outside the cap triangle.

For one fixed flow `q`, let `E_q(z,r)` be the set of physical two-port pairs
for which such an external component exists.  The simultaneous property is

```
there is one D5 flow q with |E_q(z,r)| >= 2.
```

Any two distinct two-subsets of `{a,b,c}` cover all three physical ports, so
this is exactly the condition implemented by the checkers.

## 2. Why this condition is sufficient for typed gluing

Suppose two capped shores of a cubic three-edge cut each satisfy the
simultaneous property for their relevant root edge.  Choose a witnessing flow
on each shore.  Each set `E_q(z,r)` has at least two of the three possible
physical port pairs, so the two sets intersect.  Choose a common physical
pair.

Normalize both cap triangles to the same ordered labels `01,02,12`.  For the
chosen physical pair, the inactive cap label is then identical on the two
shores.  An external factor pair is disjoint from that label.  The two unused
coordinate names may be interchanged independently on either shore, so a
global `S5` relabelling makes the two chosen external factor pairs identical
while preserving the ordered cap triangle.  Deleting the two cap vertices and
identifying corresponding ports therefore pastes the two even factors, and
the common factor component contains both prescribed roots.  This is the
external/external case of the typed gluing lemma.

Thus a universal simultaneous theorem for the relevant caps would supply the
exact local premise needed by that reduction.  The finite census below does
not establish universality.

## 3. Complete finite result

The C++ checker reads every graph produced by

```sh
geng -Cq -d3 -D3 n
```

for even `n=4,6,8,10,12,14`.  For each biconnected simple cubic graph it
enumerates every `D5` flow modulo global `S5`.  For every proper `(z,r)` and
every individual flow, it reconstructs every `Y_P` component and records the
physical cap ports covered by external components containing `r`.  It accepts
the interface only when one individual flow records all three physical ports.

The totals are:

| order | graphs | flows / `S5` | interfaces | witnessed |
|---:|---:|---:|---:|---:|
| 4 | 1 | 2 | 12 | 12 |
| 6 | 2 | 13 | 72 | 72 |
| 8 | 5 | 128 | 360 | 360 |
| 10 | 18 | 1,525 | 2,160 | 2,160 |
| 12 | 81 | 25,960 | 14,580 | 14,580 |
| 14 | 480 | 537,418 | 120,960 | 120,960 |

The Python checker independently decodes graph6, enumerates flows after fixing
the first edge to `01`, reconstructs factor components, and checks the same
one-flow predicate through order 12.  It intentionally retains duplicates
under the stabilizer of `01`; duplicates do not affect an existential result.

## 4. Exact limitations

This property quantifies over all `D5` flows of an interface.  It is not a
claim about an arbitrary fixed flow or about every component-Kempe orbit.
Both stronger statements have explicit small counterexamples in companion
packages.  The all-flow census stops at order 14, far below the current lower
bound for a relevant non-Tait marked-girth cap.  No finite cutoff theorem is
known.  Consequently this result neither proves nor disproves FiveCDC.

The C++ program reuses the separately published C++ graph6 decoder and
canonical flow enumerator; the Python replay uses the separately published
Python decoder/enumerator.  Their external-state predicates are separately
implemented.  The dependency hashes are frozen by `SHA256SUMS`.

## AI-use disclosure

OpenAI Codex agents, under human direction, proposed the simultaneous
condition, implemented the two checkers, ran the census, and drafted this
note.  Agent cross-checks are not independent human verification or peer
review.  A human graph theorist must check the reduction and novelty, rerun
the retained artifacts, and accept normal scholarly responsibility before
formal submission.
