# Rooted cubic three-pole signature frontier

Status: **INDEPENDENT EXACT ROOTED BASE-PAIR THEOREM THROUGH ORDER 17 /
NONBRIDGE-SINGLETON THEOREM THROUGH ORDER 15 /
NO UNIVERSAL ROOT-SIGNATURE
THEOREM YET**.

The cyclic-three-cut factorization reduces one exceptional four-pole
branch to rooted cubic three-poles.  Fix the ordered connector triangle
\((01,02,12)\).  The distinguished root edge then has a signature on
the seven stabilizer orbits

```text
{01}, {02}, {12}, {03,04}, {13,14}, {23,24}, {34}.
```

`rooted_three_pole_csp.cpp` canonically reads connected simple graphs
with exactly three degree-two terminals, fixes the connector triangle,
and computes the exact root signature for every proper edge using
direct finite-domain propagation and recursive branching.

`rooted_three_pole_cadical.cpp` is an independently written SAT replay.
It gives every proper and boundary edge a one-hot ten-label domain,
encodes each cubic vertex by its complete binary-label support table,
fixes the same ordered connector triangle, and tests all ten possible
root labels incrementally.  It also checks the two members of every
nontrivial stabilizer orbit agree rather than assuming that symmetry.

The two `rooted_base_pair_screen_*.cpp` programs target the stronger
three-base-pair closure in
`docs/rooted-three-pole-base-pair-closure-target.md`.  They reuse the
two different decision engines but share only the transparent adaptive
screen: stop as soon as one of masks `0x0c`, `0x12`, or `0x21` is
contained; otherwise finish all seven orbit decisions and emit every
nonempty violation.  Transcript mode records a deterministic decision
row for every nonbridge root so the two implementations can be compared
cryptographically.

The immediate question is whether a nonbridge root can have one of the
four singleton signatures required by the equality-only exceptional
four-type orientation.  A positive row would refute that proposed
universal shortcut; a complete negative finite census would only give
an order lower bound.

The complete full-signature result through order 15 is:

```text
order  graphs  roots      singleton  singleton nonbridge
3      1       3          0          0
5      2       12         0          0
7      10      90         1          0
9      63      756        9          0
11     482     7,230      63         0
13     4,541   81,738     512        0
15     50,683  1,064,343  4,503      0
```

The direct finite-domain solver and the independent incremental-SAT
solver have byte-identical full per-root transcripts through order 13.
At order 15 they have byte-identical aggregate signature profiles and
both emit the empty nonbridge-singleton file.  The retained compressed
transcripts, report, source/binary hashes, and independent replay are
in `artifacts/`, `report.json`, and `verify_report.py`.

The same full transcripts prove a stronger finite pattern through order
13, and dedicated independently implemented screens extend it through
order 17: every nonempty nonbridge signature contains one of masks
`0x0c`, `0x12`, or `0x21`.  At order 15 the two implementations emit
the same complete transcript digest

```text
07e13a0c96f9aee26c84715ea61f1843d89ec9e21e1294828c113b617e2f3570
```

and independently report:

```text
graphs             50,683
nonbridge roots 1,057,568
empty               29,207
base-pair closed 1,028,361
violations                0
```

The 22 masks realized through order 13 consequently produce only
cross-relations `DI` and `DEI`, never any of the three exceptional
relations.  At order 17, eight canonical `geng` shards contain all
654,676 cores.  The direct finite-domain and incremental-SAT
implementations independently test all 15,645,623 nonbridge roots:

```text
empty                     337,059
base-pair closed        15,308,564
violations                       0
solver calls per engine 52,216,251
```

Their corresponding streamed transcript digests agree shard by shard.
The targeted order-15 and order-17 runs establish containment but do
not enumerate the sets of distinct masks.  This is the finite precursor
of the open base-pair closure target; it is not an induction.

A complete \(3\times7\) orbit table proves the exact fact that the base
pair itself against any nonempty invariant signature never produces
`E`, `EI`, or `D`.  It does not permit replacing the base pair by a
containing signature: for example
`R={12,03,04,01}` and `S={01}` give `EI`.  Consequently one order-17
shore excludes the `E` and `D` cyclic-three branches through total
order 36, but the mixed `EI` branch remains; if both shores lie in the
finite frontier, their two base pairs exclude all exceptional
relations.  `verify_report.py` checks the exact
\(3\cdot127\) base-pair relation cases.

Canonical order-\(n\) input is

```sh
geng -cq -d2 -D3 n m:m
```

where \(m=(3n-3)/2\) and \(n\) is odd.

The retained audit is replayed with:

```sh
python3 search/rooted-three-pole-frontier-20260727/verify_report.py
```

The order-17 evidence consists of 64 retained audit, summary, generator,
and PASS files under `artifacts/order17-base-pair/`; the full decision
transcript is represented by matching per-shard SHA-256 digests rather
than retained verbatim.  Replay its aggregation directly with:

```sh
python3 search/rooted-three-pole-frontier-20260727/verify_order17_base_pair_run.py \
  search/rooted-three-pole-frontier-20260727/artifacts/order17-base-pair
```
