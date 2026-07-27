# Reproducing the focused theta census

Run from the repository root.

## Integrity and compact audit

```sh
(
  cd search/focused-theta-choice-through28-20260727
  shasum -a 256 -c SHA256SUMS
  python3 verify.py > reproduced-report.json
  cmp reproduced-report.json report.json
)
```

## Primary C++ classifier

```sh
clang++ -O3 -std=c++17 -Wall -Wextra -pedantic \
  scratch/focused-theta-choice-census.cpp \
  -o /tmp/focused-theta-choice-census

for n in 10 12 14 16 18 20 22 24 26 28; do
  /tmp/focused-theta-choice-census "$n" \
    "search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order$n.g6"
done > /tmp/primary-results.ndjson

cmp /tmp/primary-results.ndjson \
  search/focused-theta-choice-through28-20260727/primary-results.ndjson
```

Progress is written to standard error.  The order-28 run is the dominant
part.

## Independent Python replay

```sh
python3 scratch/verify-focused-theta-choice-census.py \
  --orders 10,12,14,16,18,20,22,24,26 \
  > /tmp/independent-through26.json
python3 scratch/verify-focused-theta-choice-census.py \
  --orders 28 \
  > /tmp/independent-order28.json
```

The `elapsed_seconds` field is machine-dependent.  All mathematical
fields and corpus hashes must match the retained replay files.  The
Python code neither executes nor imports the primary classifier.

## Regenerating the sources

With the frozen Snarkhunter 2.0b binary:

```sh
for n in 10 12 14 16 18 20 22 24 26 28; do
  ./berge-fulkerson/search/canonical/tools/snarkhunter-2.0b/snarkhunter \
    "$n" 4 S s C4 o g > "/tmp/cyclic4-nontait-order$n.g6" \
    2> "/tmp/snarkhunter-order$n.log"
  cmp "/tmp/cyclic4-nontait-order$n.g6" \
    "search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order$n.g6"
done
```

The package classifiers check the supplied graphs and root pairs, but
canonical completeness and the option meanings rely on Snarkhunter.
