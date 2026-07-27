# Complete cyclically-four order-24 cap classification

Status: **COMPLETE TWO-IMPLEMENTATION CLASSIFICATION OF THE RETAINED
155-GRAPH CYCLICALLY-FOUR SOURCE / NOT A GLOBAL EXCEPTIONAL-POLE
EXCLUSION / NOT FIVE-CDC**.

The retained source is the output of:

```sh
snarkhunter 24 4 S s C4 o g > cyclic4-nontait-order24.g6
```

It contains 155 cyclically 4-edge-connected non-3-edge-colourable simple
cubic graphs of order 24 and girth at least four.  A cyclically
4-edge-connected simple cubic graph of this order is automatically
triangle-free, so the girth-four setting captures the entire intended
cyclically-four non-Tait cap class.  Completeness of the canonical source
relies on Snarkhunter 2.0b and its documented option semantics.

Deleting every independent edge pair produces 86,490 terminal-distinct
four-poles.  Two separately written exact classifiers were run in
full-signature mode on eight identical deterministic shards:

* the CaDiCaL implementation;
* the direct finite-domain backtracker.

Their complete tables agree byte-for-byte:

```text
source caps                         155
deletion four-poles              86,490
queries per implementation      864,900
satisfiable answers             864,900
rows with full mask 0x3ff        86,490
exceptional hits                      0
```

Thus every deletion pole in the retained source realizes all ten
fixed-five \(D_5\) boundary types.

A later audit found that the attempted reduction from every small
exceptional pole to this cap class used a false one-sided base-pair
inference.  The computation therefore does not exclude cyclic-three poles
with the mixed relation and yields no global lower bound.  The exact
correction and the retained finite theorem are in `THEOREM.md`.

## Replay

`verify.py` independently checks each retained graph's order, cubicity,
connectedness, bridgelessness, triangle-freeness, cyclic
4-edge-connectivity, and non-Taitness.  It reconstructs all deletion poles
byte-for-byte and checks both classification tables and all sixteen shard
logs:

```sh
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
shasum -a 256 -c SHA256SUMS
```

The checker does not independently regenerate the canonical 155-graph
source.  The classifier and expander sources are frozen by hash in
`SOURCES.sha256`.

This is a finite theorem about independent-edge deletions of the retained
cyclically-four caps.  It is not a universal exceptional-signature theorem
and does not resolve Five-CDC.
