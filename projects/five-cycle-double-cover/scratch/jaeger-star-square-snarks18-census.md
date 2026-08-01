# Whole-fibre square implication on all order-18 snarks

Date: 2026-07-28

Status: **COMPLETE CANONICAL POSITIVE CERTIFICATE CENSUS FOR THE STATED
SNARK CONVENTION / FINITE THEOREM ONLY / NOT A RESOLUTION OF FIVE-CDC**.

## Exact scope

Here a snark means a connected simple cubic graph which is
three-edge-connected, has girth at least five, and is not
three-edge-colourable.  The checker regenerates

```sh
geng -cq -d3 -D3 18
```

and checks the 41,301-record stream digest

```text
d8dc31164cab1da5d93b4696a3a4eae7bf6340f497207a1c195c42e563533136
```

It then tests the three snark conditions directly and obtains exactly:

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
Q???C@?K@O@aDAw?GW?J?_g?Y??
Q??CA?_CCOW_Q_M?AD@A_@K?F??
```

No appeal to a name or an external snark catalogue is needed for the
three-record selection.

For each graph, all 18 roots and all 231 eligible independent nonroot
edge pairs were checked.  Every one of the
\[
                    3\cdot18\cdot231=12,474
\]
instances has an explicit exact-good downstairs star packing and an
explicit exact-good square-local lift.  Thus the local-selection
implication (L) holds for every order-18 snark under the convention
above.

## Discovery and independent replay

The discovery program

```text
scratch/search_jaeger_star_square_snarks18.cpp
```

uses the same exact spanning-tree, odd-kernel, component-parity, and
local-lift tests as the complete order-16 census.  Its summed
early-stopping totals are:

```text
graphs                    3
roots                    54
witnesses            12,474
star states          510,180
exact-good states      1,634
local-lift attempts    31,669
failures                    0
```

The separately written standard-library checker

```text
scratch/verify_jaeger_star_square_snarks18.py
```

does not call or import the discovery code.  It independently:

1. regenerates and decodes the complete canonical order-18 stream;
2. tests three-edge-connectivity by every deletion of at most two edges;
3. rejects triangles and four-cycles directly;
4. tests three-edge-colourability by exhaustive backtracking;
5. verifies that the displayed three records are exactly the records
   which survive those tests; and
6. reconstructs and checks all 12,474 downstairs/lifted tree
   certificates, multiplicities, outside agreement, odd kernels, and
   component-parity profiles.

The checker reports 599 distinct downstairs states.  Reading the three
uncompressed corpus shards in graph-index order gives SHA-256

```text
042ae2532a19a7b169360274081d32dbbd966a0cf8a57e5a69e082e00824e8cf
```

## Logical boundary

This closes the first non-three-edge-colourable order beyond the complete
order-16 census, but only on the three snarks.  It does not check all
30,468 order-18 simple three-edge-connected cubic graphs, prove (L)
in arbitrary order, or resolve FiveCDC.  A failure of (L) would itself
only refute this square-local induction route, not FiveCDC.

## AI-use disclosure

OpenAI Codex, under human direction, produced the discovery run, the
independent checker, the complete positive certificate corpus, and this
note.  All conventions, graph6 records, source, and hashes are exposed
for human replay.  No claim of independent peer review or universal
resolution is made.
