# Human-checkable proof of the local obstruction

This note isolates the finite mathematical claim checked by
`independent_verify.py`. It is not a proof or disproof of the Five-Cycle
Double Cover Conjecture.

## Definitions

Let `G` be a cubic graph, let `r` be a degree-three vertex, and let
`s_0,s_1,s_2` be its incident edges. A rooted three-tree state is a
partition `A_0,A_1,A_2` of the edges not incident with `r`, such that

```text
T_i = {s_i} union (E(G-r) minus A_i)
```

is a spanning tree of `G`.

For a spanning tree `T` of an even-order graph, its odd kernel `K(T)` is
the unique subset of `T` whose induced degree is odd at every vertex.
Uniqueness follows because the incidence map restricted to a tree is
injective after one redundant parity equation is removed. Concretely, root
the tree and put a parent edge in `K(T)` exactly when the child-side
subtree has odd cardinality.

The three kernels define a nowhere-zero `F_2^3` flow by

```text
f(e)_i = 1  iff  e is not in K(T_i).
```

For each nonzero functional `h` in the dual of `F_2^3`, the checker forms
the `h`-zero subgraph, computes its component parity demand `beta_h`, and
tests the three nonzero directions in `ker(h)` by exact Gaussian
elimination over `F_2`. The seven demand weights form the displayed
profile. A successful direction contributes one parallel span flag. The
objective is

```text
Psi = (minimum profile entry, |K(T_0)|+|K(T_1)|+|K(T_2)|),
```

ordered lexicographically. A positive state is an augmented trap when it
has no successful flag and no legal reciprocal-exchange neighbor has
either a successful flag or smaller `Psi`.

An exchange between classes `i` and `j` swaps one edge from `A_i` with one
edge from `A_j`. It is legal precisely when both resulting `T_i` and
`T_j` remain trees. Each side has a fundamental circuit. A side is active
when the removed edge belongs to the old odd kernel of its tree.

## Finite proof

Take the graph, root, edge order, and 192 labels specified in `README.md`
and the frozen JSON row.

1. Direct degree counting gives 130 vertices, 195 distinct non-loop edges,
   and degree three at every vertex.
2. Breadth-first search after deleting each zero-, one-, or two-edge set
   stays connected. Hence the graph is 3-edge-connected, in particular
   bridgeless.
3. Exhausting all 1,216,865 three-edge sets finds 130 disconnecting sets,
   each isolating one vertex, and no set separating two cyclic components.
   Hence the graph is cyclically 4-edge-connected.
4. Breadth-first searches from every vertex find no cycle shorter than 10
   and do find a cycle of length 10. Hence the girth is 10.
5. Each label occurs 64 times. For each `i`, `T_i` has 129 edges and a
   disjoint-set acyclicity check shows it is a spanning tree.
6. The rooted-subtree parity rule gives kernel sizes `(67,68,67)`. Direct
   degree counting checks that every vertex has odd kernel degree.
7. The 21 component/span calculations give profile
   `(20,24,10,18,10,16,2)` and zero successful flags. Therefore
   `Psi=(2,202)`.
8. There are exactly 12,288 possible swaps between distinct 64-element
   classes. Testing both resulting edge sets for the tree property leaves
   exactly 436 legal exchanges.
9. Repeating the kernel and Fano calculations for every one of those 436
   states finds zero
   successful neighbors and zero neighbors below `(2,202)`. This proves
   the augmented-trap property without relying on the discovery search.
10. Reconstructing the fundamental circuit on both sides of every legal
    exchange gives 423 active sides. Their minimum length is 10, attained
    16 times. The literal circuit in `README.md` is one attainment.
11. The same complete layer-one audit finds 107 equal-`Psi` and 329
    higher-`Psi` neighbors, so there is no augmented escape of length one.
    The two literal legal swaps in `README.md` lead first to an equal state
    and then to a state with `Psi=(2,201)`. Hence the exact shortest
    augmented escape distance is two.

The frozen 500-step trajectory contains seven further sampled augmented
traps. The separate all-eight checker repeats the full layer-one
enumeration and validates a literal two-exchange escape for each. All eight
sampled traps have exact distance two. This last sentence is deliberately
limited to the eight frozen states; the trajectory is heuristic and does
not enumerate the graph's full state space.

Consequently the displayed state is an augmented trap and has no active
reciprocal-exchange circuit of length at most 9. This finite object is a
counterexample to the quoted auxiliary lemma, not to FiveCDC.

## What remains outside this proof

The separate file `fivecdc-witness.txt` labels each of the 195 structured
graph edges by one of the ten two-subsets of `{0,1,2,3,4}`. Reading one
coordinate at a time gives five edge subsets of sizes
`(64,82,94,71,79)`. Direct incidence counting shows even degree at every
vertex in every subset. Every edge label has two distinct coordinates, so
every edge occurs exactly twice. Therefore this graph itself has a
standard FiveCDC and is not a counterexample to the main conjecture.

The augmented-trap result still closes a specific local-descent proof route
and identifies an obstruction that a viable proof invariant must overcome.
