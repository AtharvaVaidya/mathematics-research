# Reproducing the endpoint-factor screen

The source graphs were generated with the bundled Snarkhunter 2.0b:

```sh
for n in 20 22 24 26; do
  ./berge-fulkerson/search/canonical/tools/snarkhunter-2.0b/snarkhunter \
    "$n" 4 S s C4 o g \
    > "cyclic4-nontait-order${n}.g6" \
    2> "snarkhunter-order${n}.log"
done
```

The classifiers are the two independent implementations already frozen
in `../rooted-three-pole-frontier-20260727/`.  On the recorded macOS
arm64 environment they were compiled as follows:

```sh
c++ -std=c++20 -O3 \
  search/rooted-three-pole-frontier-20260727/rooted_base_pair_screen_cadical.cpp \
  -I/opt/homebrew/include -L/opt/homebrew/lib -lcadical \
  -o rooted_base_pair_screen_cadical

c++ -std=c++20 -O3 \
  search/rooted-three-pole-frontier-20260727/rooted_base_pair_screen_csp.cpp \
  -o rooted_base_pair_screen_csp
```

All vertex deletions were expanded in source-order and
deleted-vertex-order:

```sh
python3 expand_vertex_deletions.py \
  artifacts/cyclic4-nontait-order20.g6 \
  artifacts/cyclic4-nontait-order22.g6 \
  artifacts/cyclic4-nontait-order24.g6 \
  artifacts/cyclic4-nontait-order26.g6 \
  > vertex-deleted-cores-through26.g6
```

The 38,244-line stream was split into six consecutive shards of 6,374
lines.  Each implementation was run on every shard with

```sh
rooted_base_pair_screen_IMPLEMENTATION \
  --transcript --fail-on-violation \
  < shard.g6 > transcript.tsv 2> shard.log
```

The six transcripts were concatenated in shard order `a` through `f`
and compressed with `gzip -n`.  `verify.py` checks the exact ordering,
the uncompressed transcript digest, all shard summaries and statuses,
and the semantic result:

```sh
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
shasum -a 256 -c SHA256SUMS
shasum -a 256 -c SOURCES.sha256
```

The two solver transcripts are retained separately even though their
uncompressed contents are byte-identical.
