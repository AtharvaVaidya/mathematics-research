# Complete cyclically-four order-26 cap classification

Status: **COMPLETE TWO-IMPLEMENTATION CLASSIFICATION OF THE RETAINED
1,297-GRAPH SOURCE / EXCEPTIONAL-POLE EXCLUSION THROUGH ORDER 26 AFTER
SEPARATE REDUCTIONS / NOT FIVE-CDC**.

The retained source is the output of:

```sh
snarkhunter 26 4 S s C4 o g > cyclic4-nontait-order26.g6
```

It contains 1,297 cyclically 4-edge-connected non-3-edge-colourable simple
cubic graphs of order 26 and girth at least four.  A cyclically
4-edge-connected simple cubic graph of this order is automatically
triangle-free, so the girth-four setting captures the entire intended
cyclically-four non-Tait cap class.  Completeness of the canonical source
relies on Snarkhunter 2.0b and its documented option semantics.

Deleting every independent edge pair produces 859,911 terminal-distinct
four-poles.  Two separately written exact classifiers were run in
full-signature mode on eight identical deterministic shards:

* the CaDiCaL implementation;
* the direct finite-domain backtracker.

Their complete tables agree byte-for-byte:

```text
source caps                       1,297
deletion four-poles             859,911
queries per implementation    8,599,110
satisfiable answers           8,599,110
rows with full mask 0x3ff       859,911
exceptional hits                      0
```

Thus every deletion pole in the retained source realizes all ten
fixed-five \(D_5\) boundary types.

Combined with the separately proved exceptional-atom descent, cyclic-three
cap elimination through order 36, simple-cap reduction, and the complete
order-22 and order-24 censuses, this proves that no bridge-free connected
simple terminal-distinct exceptional four-pole has order at most 26.  The
complete human proof chain and its exact scope are in `THEOREM.md`.

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

The checker does not independently regenerate the canonical 1,297-graph
source.  The classifier and expander sources are frozen by hash in
`SOURCES.sha256`.

This is a finite theorem in the simple terminal-distinct fixed-five scope.
It is not a universal exceptional-signature theorem, says nothing about
order 28 or higher, and does not resolve Five-CDC.
