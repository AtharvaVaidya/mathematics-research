# Petersen--Foster girth-10 non-Tait test graph

This directory gives a reproducible, independently checkable construction of
a simple bridgeless cubic graph with:

- 890 vertices and 1,335 edges;
- girth 10;
- edge-connectivity 3 and cyclic edge-connectivity 3;
- no Tait (proper 3-edge) colouring; and
- an explicit standard five-cycle-double-cover witness.

It is therefore a genuine high-girth non-Tait test graph for FiveCDC code.
It is **not** a counterexample to FiveCDC.  Because it has a cyclic 3-edge
cut, it is also not a snark under the convention requiring cyclic
4-edge-connectivity.

## Construction

The Foster graph is constructed from the LCF string

```text
[17,-9,37,-37,9,-17]^15
```

Delete vertex 0, leaving a three-pole whose boundary vertices are the former
neighbours 1, 17, and 89.  Replace every vertex of the Petersen graph by one
copy of this three-pole, and join the three boundary vertices according to the
three incidences of the corresponding Petersen vertex.  The precise edge and
port order is fixed in `verify.py`.

The Foster identification is independently cross-referenced by House of
Graphs graph 37261:

<https://houseofgraphs.org/api/graphs/37261>

The construction itself is elementary; no claim of publication-level novelty
is made for the substitution.

## Reproduction

Run:

```sh
python3 verify.py > reproduced-output.json
diff -u verification-output.json reproduced-output.json
```

The verifier uses only the Python standard library.  It reconstructs the graph
from the LCF string, checks simplicity, cubicity, connectivity, absence of
1- and 2-edge cuts, girth, the Petersen non-colourability certificate, the
explicit cyclic 3-edge cut, and every local parity condition in the FiveCDC
witness.

`fivecdc-labels.txt` contains one mask for each edge in graph6 edge order
(`v=1..n-1`, then `u=0..v-1`).  Bit `i` of a mask says that the edge is in
Eulerian edge-subset `i`.  The verifier checks that every mask has exactly two
bits and that the XOR of incident masks is zero at every vertex.

## Flow-reconfiguration calibration

The same graph has a frozen nowhere-zero
\(\mathbb F_2^3\)-flow calibration:

- a Jaeger-derived H--S-bad flow with profile
  `(174,192,138,184,130,140,110)`;
- an H--S-good target flow derived directly from the explicit FiveCDC;
- zero-allowing fixed-value Eulerian-support distance exactly 3;
- legal nowhere-zero fixed-value Eulerian-support distance exactly 5; and
- a complete independent replay of all 2,640 legal reciprocal-exchange
  neighbours of the frozen Jaeger state.

The word **Eulerian-support** is essential.  The certified five supports are
disconnected, with 63 simple-cycle components in total.  For the narrower
connected-simple-cycle move graph used by Cranston et al., this package proves
only a lower bound of 5 and an explicit upper bound of 63—not distance 5.

Run the self-contained audit:

```sh
python3 verify_reconfiguration.py > reproduced-reconfiguration-output.json
diff -u reconfiguration-output.json reproduced-reconfiguration-output.json
python3 audit-blind-20260729/independent_check.py \
  > reproduced-independent-output.json
diff -u audit-blind-20260729/independent-output.json \
  reproduced-independent-output.json
```

The exhaustive completeness proof for three and four moves is written in
`HUMAN-RECONFIGURATION-PROOF.md`.  The exact flow, tree-state, and five path
supports are frozen compactly in `reconfiguration-certificate.json`.
The blind-audit checker imports none of the source checker and reconstructs
the graph, flows, lower-bound enumeration, and five-move witness independently.
Both implementations were AI-assisted; “independent” refers to implementation
lineage, not human authorship.

## Scope

This artifact closes a test-infrastructure gap: previous retained girth-10
examples in this project were Tait-colourable controls.  It does not resolve
FiveCDC and should not be described as doing so.

The graph and witness were generated during an AI-assisted search.  All
mathematical claims in this directory are reduced to the written human proof
and the deterministic standard-library verifier.
