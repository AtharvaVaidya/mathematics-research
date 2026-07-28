# Reproducing the order-30 census

Run all commands from the package directory.

## Fast retained-artifact audit

```sh
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

The first command checks the compressed and decompressed corpus hashes,
all 139,854 graph records, the primary result, all sixteen independent
reports, and exact aggregate agreement.

## Primary C++ replay

```sh
gzip -cd artifacts/Generated_graphs.30.04.sn.cyc4.g6.gz \
  > /tmp/Generated_graphs.30.04.sn.cyc4.g6

c++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  primary_census.cpp -o /tmp/focused-theta-choice-order30

/tmp/focused-theta-choice-order30 30 \
  /tmp/Generated_graphs.30.04.sn.cyc4.g6 \
  > /tmp/primary-result.json 2> /tmp/primary.log

cmp /tmp/primary-result.json artifacts/primary-result.json
```

The retained build used Apple clang with C++20.  The semantic result,
not the compiler-specific binary, is the certificate.

## Independent Python replay

The clean-room implementation accepts an explicit corpus and graph-index
shard.  Sixteen shards were used:

```sh
corpus=/tmp/Generated_graphs.30.04.sn.cyc4.g6
digest=bc6f29ec50910eae345ced81f87800686deb069dd1cb383d73dbcc56765f247d

for i in $(seq 0 15); do
  python3 independent_verifier.py \
    --orders 30 \
    --corpus "$corpus" \
    --expected-sha256 "$digest" \
    --shard-index "$i" \
    --shard-count 16 \
    > "/tmp/shard-$i.json" 2> "/tmp/shard-$i.log" &
done
wait

for i in $(seq 0 15); do
  cmp "/tmp/shard-$i.json" "artifacts/independent/shard-$i.json"
done
```

Elapsed-time metadata can differ with a modified interpreter or machine.
In that case, inspect `classification`, the sole `results` row, source
hash, shard metadata, and aggregate totals rather than requiring a
byte-for-byte comparison.

The retained sixteen-way replay took about 22.5 wall-clock minutes per
shard on the originating machine.  It uses only the Python standard
library.

## Logical scope

Both programs directly enumerate finite matching objects.  There is no
SAT `UNSAT` status and no proof certificate because the result is a
positive exhaustive classification, not a counterexample to Five-CDC.
The absence of an all-dumbbell pair at order 30 does not imply universal
absence.
