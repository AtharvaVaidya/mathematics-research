# Universal four-edge separation is absent in Tait-colourable graphs at order 22

Date: **2026-07-27**.

Status: **COMPLETE CANONICAL FINITE THEOREM / TWO ALGORITHMIC
IMPLEMENTATIONS AGREE / NOT A UNIVERSAL GRAPH THEOREM**.

Every one of the \(7\,319\,447\) connected simple cubic graphs on
22 vertices was generated canonically.  Exactly \(7\,174\,735\) are
Tait-colourable, and every one of those was checked.  None of the
Tait-colourable graphs has a four-edge matching which is separated on
every bichromatic factor circuit in every Tait colouring.

The primary checker enumerates Tait colourings directly.  A separately
written replay enumerates perfect matchings and even complementary
two-factors instead.  Their row, colourable-graph, and normalized
colouring counts agree on every one of four canonical shards.  Both find
zero witnesses.

This is a finite theorem at one order.  It does not exclude a witness at
order 24 or above, does not apply to multigraphs, and does not prove the
rooted four-mark assertion or the Five-Cycle Double Cover Conjecture.

## 1. Exact property tested

Let \(H\) be a Tait-colourable connected simple cubic graph.  For each proper
three-edge-colouring, each pair of colours induces a disjoint union of
even circuits.  Make a conflict graph \(\Omega(H)\) whose vertices are
the edge objects of \(H\).  Two edge objects conflict when either

1. they are adjacent in \(H\); or
2. some proper three-edge-colouring puts them on one bichromatic
   circuit.

A set of four edge objects is a universally separated four-edge
matching exactly when it is an independent set of size four in
\(\Omega(H)\).  Adjacency conflicts enforce the matching condition.
The remaining conflicts are precisely the negations of universal
bichromatic separation.  Thus searching \(\Omega(H)\) for an
independent four-set is equivalent to the intended definition; no SAT
relaxation or probabilistic filter is involved.

The Tait-colourability hypothesis is essential to this statement.  If
the definition were applied literally to a graph with no Tait
colouring, the phrase “in every Tait colouring” would be vacuously true.
Both implementations deliberately exclude such rows from the witness
search, so this census proves a theorem only about the nonempty
Tait-colouring domain.

## 2. Canonical corpus

Nauty `geng` 2.9.3 was run in four modular shards:

```sh
/opt/homebrew/bin/geng -cq -d3 -D3 22 0/4
/opt/homebrew/bin/geng -cq -d3 -D3 22 1/4
/opt/homebrew/bin/geng -cq -d3 -D3 22 2/4
/opt/homebrew/bin/geng -cq -d3 -D3 22 3/4
```

Here `-c` requires connectedness, `-d3 -D3` requires every degree to be
three, and `geng` generates simple graphs canonically.  The modular
shards are disjoint and their union is the complete corpus.  Their row
counts are

\[
  1\,376\,411,\quad
  2\,078\,782,\quad
  1\,716\,645,\quad
  2\,147\,609,
\]
which sum to
\[
                            7\,319\,447.                \tag{1}
\]

The generator binary has SHA-256

```text
ad2f68adf733dbed7cad543841cfa329740596ee5cd136f17a0a17f6e744f5ad
```

## 3. Primary direct-colouring check

The primary implementation is
`scratch/tait_all_coloring_mark_separation.cpp`.  It fixes one incident
colour frame to quotient by all six global colour permutations,
enumerates every resulting Tait colouring, records every bichromatic
factor circuit, accumulates \(\Omega(H)\), and performs an exact
backtracking search for an independent four-set.

Compile and run each shard with

```sh
clang++ -O3 -std=c++20 \
  scratch/tait_all_coloring_mark_separation.cpp \
  -o /tmp/tait_all_coloring_mark_separation

/opt/homebrew/bin/geng -cq -d3 -D3 22 SHARD/4 |
  /tmp/tait_all_coloring_mark_separation \
    --target 4 --stop-after-first --progress 250000
```

The four final rows were:

| shard | graphs | Tait-colourable | normalized colourings | witnesses |
|---:|---:|---:|---:|---:|
| 0 | 1,376,411 | 1,338,944 | 17,481,016 | 0 |
| 1 | 2,078,782 | 2,029,518 | 28,040,733 | 0 |
| 2 | 1,716,645 | 1,686,315 | 22,708,101 | 0 |
| 3 | 2,147,609 | 2,119,958 | 27,130,262 | 0 |
| **total** | **7,319,447** | **7,174,735** |
  **95,360,112** | **0** |

## 4. Independent perfect-matching replay

The independent implementation is
`scratch/verify_order22_separation_via_matchings.cpp`.  It does not use
the primary edge-colouring recursion.

For each graph it:

1. enumerates every perfect matching \(M\);
2. rejects \(M\) unless the complementary 2-factor consists only of
   even circuits;
3. independently chooses one of the two alternating colourings on every
   complementary circuit;
4. records all three bichromatic factor partitions; and
5. searches the resulting conflict graph for an independent four-set.

Every normalized Tait colouring is visited exactly six times: any of
its three colour classes may be the distinguished perfect matching, and
the other two colours may be ordered in two ways.  Dividing the visit
count by six therefore gives the same normalized-colouring count as the
primary program.

Compile and replay with

```sh
clang++ -O3 -std=c++20 \
  scratch/verify_order22_separation_via_matchings.cpp \
  -o /tmp/verify_order22_separation_via_matchings

/opt/homebrew/bin/geng -cq -d3 -D3 22 SHARD/4 |
  /tmp/verify_order22_separation_via_matchings \
    --target 4 --stop-after-first --progress 250000
```

The replay agrees in every column above.  Its additional perfect
matching counts are

\[
 57\,726\,499,\quad
 89\,547\,132,\quad
 74\,614\,913,\quad
 90\,695\,387,
\]
for a total of
\[
                           312\,583\,931.               \tag{2}
\]
It again found zero witnesses.

## 5. Controls

The two implementations agree exactly on complete lower-order corpora:

| order | graphs | Tait-colourable | normalized colourings | perfect matchings | witnesses |
|---:|---:|---:|---:|---:|---:|
| 12 | 85 | 80 | 307 | 902 | 0 |
| 16 | 4,060 | 3,848 | 23,420 | 73,929 | 0 |
| 18 | 41,301 | 39,687 | 307,606 | 995,256 | 0 |

A positive order-24 target-three control has graph6 encoding

```text
W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E
```

Both programs enumerate 36 normalized colourings, return the same first
separated triple with edge IDs \(0,1,34\), and correctly find no
separated four-set in that graph.  The replay visits 64 perfect
matchings.  This exercises the positive witness path as well as the
zero-witness census.

## 6. Consequence and boundary

The complete order-22 conclusion is

> No Tait-colourable connected simple cubic graph on 22 vertices has a
> universally separated four-edge matching.

The separate complete standard-hypothesis screen through order 20 is
frozen in `scratch/rooted-four-mark-order20-screen-result.json`.
Combining the two finite theorems gives:

> Any Tait-colourable connected simple cubic standard rooted four-mark
> atom satisfying universal separation and the marked cyclic-cut
> hypothesis has at least 24 vertices.

There is a universally separated four-edge matching at order 28, so the
unrestricted separation phenomenon is real.  The possible orders 24
and 26 are not settled by this computation.

Complete machine-readable counts, commands, environment data, hashes,
and scope warnings are in
`scratch/order22-universal-four-separation-result.json`.

SHA-256:

```text
primary source
a00c2f53a3b95a06a7e8767aae2eb2bfa794fc95eeeba18bcac34aea6a12072a

independent source
104dca4ac143581a9b306172354428a96913f3fe1701c60b2a018510990ecead

primary run binary
a63d8048528e3dfa751049fbad6aec3b4909d1f7508f9e56859edbb5af9a6aa0

independent run binary
3de46d3c343fb3b23679334f1058104488077386f49b4a2541273aa1e5d7d703
```

Mach-O linker UUIDs make recompilations non-byte-identical even under
the same compiler command; the source hashes and semantic output counts
are the reproducibility anchors.  The recorded run-binary hashes identify
the exact executables used for this census.

## AI-use disclosure

OpenAI Codex agents, under human direction, wrote both implementations,
ran the four-shard census, checked the controls, and prepared this
report.  The canonical corpus and exact counts are independently
replayable, but this is not independent human peer review.  The finite
theorem is not presented as a proof of the unrestricted conjecture.
