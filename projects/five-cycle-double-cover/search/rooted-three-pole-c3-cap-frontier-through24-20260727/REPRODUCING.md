# Reproducing the triangle-free rooted cap screen

Run from the package directory.

## Full integrity and semantic replay

```sh
shasum -a 256 -c SHA256SUMS
shasum -a 256 -c SOURCES.sha256
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
```

The verifier reads both complete transcripts and reconstructs every cap
and deletion.  It is therefore substantially slower than the checksum
pass.

## Classifiers

The two sources are:

```text
../rooted-three-pole-frontier-20260727/rooted_base_pair_screen_cadical.cpp
../rooted-three-pole-frontier-20260727/rooted_base_pair_screen_csp.cpp
```

Compile the first against the frozen CaDiCaL library and the second with
the C++ standard library.  Both accept graph6 three-poles on standard
input and, with

```text
--transcript --fail-on-violation
```

emit one tab-separated row per nonbridge root.  The six deterministic
core shards are the consecutive partition with sizes

```text
55132 55132 55132 55132 55132 55130
```

Concatenate shard transcripts in order and compress with `gzip -n`.

## Regenerating the caps

With the frozen Snarkhunter 2.0b binary:

```sh
for n in 20 22 24; do
  ../../berge-fulkerson/search/canonical/tools/snarkhunter-2.0b/snarkhunter \
    "$n" 4 S s C3 o g > "/tmp/c3-nontait-order$n.g6" \
    2> "/tmp/snarkhunter-order$n.log"
  cmp "/tmp/c3-nontait-order$n.g6" "artifacts/c3-nontait-order$n.g6"
done
```

`verify.py` independently reconstructs the vertex-deleted core stream
and requires byte identity with the retained compressed artifact.
