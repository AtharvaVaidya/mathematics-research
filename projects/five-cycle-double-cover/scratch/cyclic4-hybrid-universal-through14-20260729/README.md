# Cyclically-4 hybrid macro frontier through order 14

This package contains a constructive positive census for a restricted
FiveCDC composition family.

Main result:

```text
110 cyclically-4 simple cubic macros
9,278 independent positive-even junction-set orbits
12 girth-at-least-five macros / 455 junction orbits
9,278 explicit six-state macro witnesses
2,592 explicit internal atom completions
0 ansatz failures and 0 target candidates
```

The six connector states are

```text
P_ab = {0a, 0b, cd}, where {a,b,c,d}={1,2,3,4}.
```

They give a short composition lemma: any macro-edge labelling with
path-state connectors and xor-zero junctions works for every connector
matching, either atom type, and every port order.

Run the solver-free audit:

```sh
python3 verify.py
```

The audit checks the SHA-256 ledger, rebuilds the graph and automorphism
census, verifies all macro witnesses, reconstructs both Blanuša six-poles,
and checks all 2,592 atom completions.

See `HUMAN-PROOF.md` for the proof, exact scope, limitation, and AI-use
disclosure.  This is not a resolution of the Five-Cycle Double Cover
Conjecture.
