# Dynamic Kempe frontier

This package contains two rigorous partial results for the
minimum-projection route to FiveCDC:

1. If the support is one circuit and every complement component has
   exactly two boundary terminals, every extension is directly cleanable.
   This excludes goal-free dynamic Kempe components in that entire,
   unbounded class.
2. The two-pole obtained from \(K_{3,3}-e\) is boundary-orbit-reflecting
   under three-edge-colour Kempe switches.  Chains of these poles have
   old-endpoint distance \(4r+1\).  They transfer a hypothetical
   goal-free base component to a dynamically exchange-compatible inflated
   component without adding boundary moves.

No goal-free component was found.  The package does not resolve FiveCDC
and does not construct a graph with a globally minimum positive
projection.  The random 8-pole searches are exploratory only.

## Replay

From this directory:

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

`verify.py` is dependency-free.  It exhausts all proper colourings of the
local \(K_{3,3}-e\) pole, its literal Kempe graph, chain distances for
one through eight copies, and all 146,599 pairings on one support circuit
through order fourteen.

`independent_audit.py` is separately written.  It scans all \(3^9\)
edge assignments of \(K_{3,3}\) and checks the two-terminal theorem by
direct cut-incidence parity.

`exploratory_search.py` is also dependency-free, but its randomly
generated graph families are not an exhaustive certificate.  Example
smoke tests are:

```sh
python3 exploratory_search.py --order 10 --trials 1
python3 exploratory_search.py --k33-cut --trials 1
```

See `HUMAN-PROOF.md` for the complete proof, conditional dynamic-trap
transfer, exact logical scope, and literature attribution.

## AI disclosure

OpenAI Codex agents proposed the \(K_{3,3}-e\) inflator, wrote the proofs
and checkers, ran the exploratory searches, and performed internal
criticism.  The known \(K_{3,3}\) Kempe-class fact is attributed to
Belcastro and Haas.  No human expert has yet certified the new
project-specific lemmas, and no claim of publication priority is made.
