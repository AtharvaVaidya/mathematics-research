# Reproducing the order-28 two-witness package

Run these commands from this directory.

## Fast integrity and semantic replay

```sh
shasum -a 256 -c SHA256SUMS
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  ../../scratch/verify_boundary_two_orbit_witness_fast.cpp \
  -lz -o /tmp/verify-boundary-two-orbit
/tmp/verify-boundary-two-orbit \
  artifacts/cyclic4-nontait-order28-poles.g6.gz \
  artifacts/cadical-two-orbit-witness.tsv.gz \
  > reproduced-independent-fast-replay.json
cmp reproduced-independent-fast-replay.json independent-fast-replay.json
```

The package verifier uses only the Python standard library.  The second
checker uses only the C++ standard library and zlib.  Both consume the
full 9,725,709-row streams and therefore take substantially longer than
the checksum pass.

## Regenerating the canonical source

With the frozen Snarkhunter 2.0b binary:

```sh
../../berge-fulkerson/search/canonical/tools/snarkhunter-2.0b/snarkhunter \
  28 4 S s C4 o g > regenerated-order28.g6 2> regenerated-snarkhunter.log
cmp regenerated-order28.g6 artifacts/cyclic4-nontait-order28.g6
```

The retained log records 12,517 generated graphs.  Canonical completeness
and option semantics are inherited from Snarkhunter; the package verifier
does not supply a second canonical generator.

## Regenerating the pole stream

Compile
`../four-pole-order20-cap-20260727/expand_independent_edge_deletions.cpp`
and pipe the retained cap source through it:

```sh
clang++ -std=c++17 -O3 \
  ../four-pole-order20-cap-20260727/expand_independent_edge_deletions.cpp \
  -o /tmp/expand_independent_edge_deletions
/tmp/expand_independent_edge_deletions \
  < artifacts/cyclic4-nontait-order28.g6 \
  2> regenerated-expand.log | gzip -n > regenerated-poles.g6.gz
gzip -cd regenerated-poles.g6.gz | shasum -a 256
```

The expected uncompressed digest is

```text
f42168e2786bdee409304e9e7b167ae0a0e250c78e7c2413e55ee56f5627a839
```

## Regenerating the witnesses

Compile `../../scratch/boundary_two_orbit_witness_cadical.cpp` against
CaDiCaL, then run it on the pole stream:

```sh
gzip -cd artifacts/cyclic4-nontait-order28-poles.g6.gz |
  /tmp/boundary_two_orbit_witness_cadical \
    --fail-on-missing --progress 100000 \
  2> regenerated-witness.log |
  gzip -n > regenerated-witness.tsv.gz
gzip -cd regenerated-witness.tsv.gz | shasum -a 256
```

The expected uncompressed digest is

```text
658374b00418fa626da704670689f4dfad25cf740121509a725da4158491ef7d
```

The original run used eight deterministic source shards.  The combined
stream is the concatenation of shard outputs in source order.  Solver
models are not assumed trustworthy by the replay: both checkers read and
verify every emitted edge labelling.
