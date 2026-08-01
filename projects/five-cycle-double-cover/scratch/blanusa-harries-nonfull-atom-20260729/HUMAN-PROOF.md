# Exact relation of a Blanuša six-pole

## Statement

Take the first retained order-18 Blanuša graph

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
```

and delete vertices 13 and 16.  The resulting 16-vertex graph has 21
internal edges and six distinct degree-two port vertices, in the order

```text
1, 2, 3, 6, 8, 9.
```

Label an edge by a two-subset of `{0,1,2,3,4}`, represented by its five-bit
mask.  A boundary word is extendible when the six dangling port edges and
the 21 internal edges can be labelled so that the xor of the three incident
labels is zero at every completed cubic vertex.

Among the 571 orbits of xor-zero ordered six-duad words under permutation
of the five coordinates, exactly 555 are extendible and 16 are not.

## Why this is the FiveCDC boundary condition

For edge `e`, bit `i` of its duad label is `x[e,i]`.  A duad has exactly two
bits, so `sum_i x[e,i] = 2`.  At a vertex, xor zero says that each coordinate
has even incident degree.  Therefore coordinate `i` is an Eulerian
edge-subset.  Conversely, five Eulerian edge-subsets covering every edge
twice give exactly such a duad label.  This proves the equivalence without
using the SAT solver.

At a port, the two internal labels xor to the fixed dangling boundary
label.  Thus a pole completion glues correctly across either a direct
identification or a new trivalent junction.

## Positive half

`boundary-relation.jsonl` contains one explicit 27-label completion for
each of the 555 positive orbit representatives.  The independent checker
verifies:

1. every label is one of the ten duads;
2. the final six labels equal the claimed boundary word;
3. the xor of the three labels at each of the 16 completed vertices is
   zero.

Permuting the five coordinates transports each representative witness to
its entire S5 orbit.

## Negative half

The 16 representatives are listed in
`negative-boundary-orbits.json`.  The CNF uses 105 internal coordinate
variables and 16 selector variables.

For every internal edge, 15 prime clauses impose Hamming weight exactly
two: ten clauses forbid three true coordinates and five clauses forbid
four false coordinates.  At every ordinary cubic vertex, four clauses per
coordinate impose even parity.

Selector `s_j` conditionally fixes the six port parities to negative
representative `j`.  One clause requires at least one selector.  Hence:

```text
CNF is SAT
iff some selector j is true and its boundary extends
iff at least one of the 16 representatives extends.
```

The CNF has 121 variables and 1476 clauses.  Its LRAT proof is accepted
independently by both `lrat-check` and `cake_lpr`.  Coordinate permutations
preserve the pole equations, so the 16 representative proofs exclude all
1440 ordered words in their S5 orbits.

## Shape of the obstruction

Eight negative orbits have multiplicities `2+2+2`.  In every one, the
three distinct duads are the three edges of a triangle.  Their missing
port-pair partitions are

```text
02|14|35  02|15|34  04|12|35  05|12|34
03|14|25  03|15|24  04|13|25  05|13|24.
```

No positional orbit is missing when the three distinct duads form a
3-star, a four-vertex path, or a two-edge path plus a disjoint edge.

The other eight negative orbits have multiplicities `2+1+1+1+1`.  Their
duad multigraph is `K4` minus an edge, with the opposite edge doubled.

## Consequence and limitation

This relation is genuinely non-full, but it cannot obstruct a network
formed only by pairwise port identifications.  Every diagonal word
`(d,d,d,d,d,d)` is positive.  Assigning one fixed duad `d` to every paired
port gives every atom a local completion, and those completions glue.

Thus this is a certified structural lemma and a search primitive, not a
counterexample to the Five-Cycle Double Cover Conjecture.

## Authorship, review, and novelty

OpenAI Codex agents authored this note, the SAT producer, the independently
written semantic/CNF checker, and the certificate package under the user's
direction.  “Independent” here means a separately implemented audit path,
not independent human authorship.  No human peer review has yet occurred.

The novelty status is provisional.  The checkable claim is the exact local
relation of one explicitly encoded six-pole.  We have not established that
this relation, its 16-orbit obstruction, or the Harries equality-gadget lift
is absent from the existing multipole, snark, flow, or cycle-double-cover
literature.  The auxiliary 366-vertex internal-girth-ten lift has not yielded
a counterexample.  No proof or disproof of FiveCDC is claimed here.
