# Complete order-22 exceptional four-pole cap census

Status: **COMPLETE FINITE INDEPENDENT EXACT ENUMERATION / ORDER-22
EXCLUSION PROVED IN THE STATED SIMPLE SCOPE / NOT A FIVE-CDC
RESOLUTION**.

The human reduction in
`../../docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`
proves that every bridge-free connected simple terminal-distinct
four-pole with either exceptional exact boundary signature can be
obtained by deleting two independent edges from a bridgeless non-Tait
connected simple cubic graph of the same order.

The canonical order-22 source retained in
`../order22-filter-census-20260725/` contains all 7,319,447 connected
simple cubic graphs of order 22.  Two independent Tait-colourability
filters produce the same hard corpus byte-for-byte.  A separate Python
verifier checks the canonical-source digest and source indices, the
agreement of those two filters, and every retained hard-graph premise.
The exact counts are:

```text
connected simple cubic graphs             7,319,447
bridgeless graphs                          7,187,627
bridgeless non-Tait graphs                    12,892
independent-edge deletion four-poles       5,956,104
```

The 12,892 non-Tait caps split as follows:

```text
with a two-edge cut                            5,024
with a nontrivial three-edge cut               7,837
cyclically four-edge-connected                    31
```

Every independent edge pair in every one of the 12,892 caps was
classified by two separately written exact solvers:

* `boundary_exceptional_cadical.cpp`, which uses CaDiCaL;
* `boundary_exceptional_csp.cpp`, a direct finite-domain backtracker.

The stream was divided round-robin into eight deterministic shards.
For each solver and shard, an independent streaming auditor checked
every transcript row, rejected malformed or unqueried types, rejected
either exceptional signature, and recorded a SHA-256 digest.  The two
solvers agree exactly on all eight transcript digests and aggregate
totals:

```text
four-poles per implementation             5,956,104
exact signature queries per implementation 23,747,129
satisfiable queries per implementation    22,764,574
exceptional hits                                   0
```

Together with the proved cap reduction, this gives the finite theorem:

> No bridge-free connected simple terminal-distinct order-22
> four-pole has either exceptional exact boundary signature in the
> fixed five-colour \(D_5\) model.

Equivalently, any bridge-free connected simple terminal-distinct
four-pole with an exceptional signature has even order at least 24.
This does not cover repeated terminals, nonsimple or multigraph cores,
arbitrary-colour CDC signatures, or any higher order.  It does not
prove the universal exceptional-signature conjecture and does not
resolve the Five-Cycle Double Cover Conjecture.

## Retained evidence

`artifacts/order22-all-cap-poles.g6.gz` is the deterministic
5,956,104-row deletion-pole stream.  `artifacts/full-run/` contains the
input-shard manifest and, for both implementations on all eight
shards, the classifier logs, transcript-audit records, and PASS
markers.  The raw transcripts were checked as streams; they can be
regenerated from the retained inputs and classifier sources.

The package also retains the earlier complete cyclically-four
subcensus.  All 14,322 deletion poles from the 31 cyclically
four-edge-connected caps realize the full ten-type boundary signature
mask `0x3ff` under both implementations.

## Independent replay

`verify_completed_run.py` does not import either C++ classifier.  It:

1. verifies the complete canonical-source identity, source indices,
   and byte-for-byte agreement of the two hard-cap filters;
2. independently checks cubicity, connectedness, bridgelessness, and
   non-Taitness of every retained cap;
3. recomputes the cut profile;
4. reconstructs all 5,956,104 independent-edge deletion poles
   byte-for-byte while reading the compressed retained stream;
5. reconstructs the eight shard digests; and
6. checks all solver summaries, audit digests, and PASS markers.

Replay the frozen theorem with:

```sh
python3 verify_completed_run.py > reproduced-report.json
cmp reproduced-report.json report.json
shasum -a 256 -c SHA256SUMS
```

To rerun the two exact classifiers themselves:

```sh
gzip -dc artifacts/order22-all-cap-poles.g6.gz > order22-poles.g6
bash run_full_transcript_shards.sh \
  order22-poles.g6 \
  ../four-pole-order18-exceptional-20260727/boundary_exceptional_cadical \
  ../four-pole-order18-exceptional-20260727/boundary_exceptional_csp \
  rerun
```

Build instructions for the classifier binaries are in the order-18
package.  Exact source hashes are frozen in `SOURCES.sha256`.
