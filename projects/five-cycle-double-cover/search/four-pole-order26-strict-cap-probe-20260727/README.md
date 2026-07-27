# Order-26 strict-snark four-pole signature probe

Status: **COMPLETE TWO-IMPLEMENTATION EXACT CLASSIFICATION OF THE RETAINED
280-GRAPH SOURCE / FINITE EVIDENCE / NOT A FIVE-CDC RESOLUTION**.

The retained source is the 280-record output of the documented Snarkhunter
2.0b command

```sh
snarkhunter 26 5 S s C4 o g > strict-snarks-order26.g6
```

The generator log reports that 280 graphs were produced.  The independent
verifier in this package checks that the records are distinct connected
simple cubic graphs of order 26, have girth at least five, are cyclically
4-edge-connected, and are not three-edge-colourable.  It does not
independently regenerate the canonical list, so completeness of the
280-graph strict-snark source relies on Snarkhunter and its option
semantics.

Deleting every pair of independent edges from these graphs produces exactly
185,640 terminal-distinct four-poles.  Two separately written exact
boundary-signature classifiers were run on this same stream:

* `boundary_exceptional_cadical.cpp`, using CaDiCaL;
* `boundary_exceptional_csp.cpp`, using a direct finite-domain backtracker.

The CaDiCaL implementation ran on the full stream.  The slower direct
implementation ran on eight consecutive 23,205-row shards, whose outputs
were concatenated in source order.  Their full tables agree byte-for-byte:

```text
rows                 185,640
queries            1,856,400
satisfiable        1,856,400
mask on every row      0x3ff
```

Thus every retained deletion pole realizes all ten two-subsets of the fixed
five-colour universe.  In particular, none has either exceptional boundary
signature.

This is stronger per pole than merely excluding the two exceptional masks,
but it is only a finite computation on the retained strict-snark source.
It does not cover all non-Tait cubic graphs of order 26, does not prove that
high cyclic connectivity forces full boundary signature, and does not
resolve the Five-Cycle Double Cover Conjecture.

## Retained evidence and replay

`artifacts/strict-snarks-order26.g6` is the 280-graph input.
`artifacts/strict-snarks-order26-poles.g6.gz` is the exact deterministic
independent-edge-deletion expansion.  The two compressed TSV files record
the full per-pole classifications.  The CaDiCaL log and eight direct-CSP
logs and status files record the aggregate solver outcomes.

The checker is independent of both boundary classifiers.  It decodes and
checks the graph premises, reconstructs the pole stream byte-for-byte,
checks both classification tables against every input row, sums the
sharded direct-CSP logs, and verifies the source and artifact hashes:

```sh
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
shasum -a 256 -c SHA256SUMS
```

The classifier sources are retained in
`../four-pole-order18-exceptional-20260727/`; their exact hashes are frozen
in `SOURCES.sha256`.
