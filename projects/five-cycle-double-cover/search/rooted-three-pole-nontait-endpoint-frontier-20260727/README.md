# Non-Tait endpoint rooted-three-pole frontier through factor order 26

Status: **TWO-IMPLEMENTATION FINITE CLASSIFICATION / CORRECTED
PURE-RELATION CONSEQUENCE / NOT FIVE-CDC**.

This package screens the complete retained cyclically
4-edge-connected non-Tait simple cubic factor sources of orders
\(20,22,24,26\).  The earlier complete rooted-order-17 package covers
factor orders through \(18\), while the human Tait-cap theorem covers
all Tait-colourable factors.

For every retained non-Tait factor, every vertex is deleted in turn.
Two independent exact implementations then test every nonbridge proper
root of the resulting rooted three-pole:

- an incremental CaDiCaL implementation; and
- a direct finite-domain backtracker.

They independently test 1,360,452 roots in 38,244 cores, make
4,157,844 solver calls per implementation, and find that every tested
root signature contains one of the three base pairs.  There are no
empty signatures or violations, and the complete transcripts agree
byte-for-byte.

`verify.py` imports neither solver.  It checks all source graph
premises, reconstructs the full vertex-deleted core stream,
independently identifies every nonbridge root, checks every adaptive
base-pair decision, compares the two transcripts, checks the six
shard logs and statuses per implementation, and reproduces
`report.json`.

`THEOREM.md` proves the finite statement, supplies the elementary
3-connectivity lemma needed for the cap decomposition, and derives the
sound consequence: equality-only and disjointness-only exceptional
cyclic-three caps have order at least 54.  The mixed
\(\{\mathsf E,\mathsf I\}\) relation is deliberately left open.

## Replay

```sh
python3 verify.py > reproduced-report.json
cmp reproduced-report.json report.json
shasum -a 256 -c SHA256SUMS
```

Canonical source completeness relies on Snarkhunter 2.0b and its
option semantics.  This package does not prove universal rooted
base-pair closure or Five-CDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, designed and ran this
screen, wrote its verifier and theorem chain, and prepared the package.
All limitations above are intentional and form part of the result.
