# Universal one-circuit tensor theorem

This package proves the abstract relative-\(\mathrm{GL}(2,2)\) tensor
lemma for every finite number of vertices.  It implies that every
charge-valid one-support-circuit state is directly cleanable, at
arbitrary circuit length and with arbitrarily many complement
components.  More generally, the same conclusion holds with several
support circuits when every complement block has zero derivative charge
on each circuit separately.  The proof is in `HUMAN-PROOF.md`; the SAT
artifacts through five vertices are retained as cross-checks.

Run:

```sh
python3 verify_tensor_frontier.py
python3 independent_audit.py
```

The script generates exact CNF instances, asks CaDiCaL for DRAT proofs,
and enables CaDiCaL's internal DRAT checking.  This is not a second
independent DRAT implementation; the retained artifacts can also be
fed to an external checker.  A SAT result would be
printed as a literal list of the four-bit pair-functional masks and
then independently checked by direct enumeration.

`verify_tensor_frontier_xor.py` is a separately implemented native-XOR
encoding of the same exact negation.  The deterministic generated
instances for three through six vertices are retained.  Its solver
answer is only a discovery cross-check: an UNSAT result is not a
certificate, while a SAT result is accepted only after the script
independently enumerates every relative map assignment.

The separately written audit reconstructs all 16 rank-one-gadget
realizations, checks the expansion coefficients through \(K_7\),
exhausts 12,321 charge-zero cyclic words through length six (including
all bases and cuts), and exhausts all 4,096 three-vertex tensor systems
without using the CNF generator.  It checks both the fixed-gauge
three-vertex census and the literal
\(\lambda^{\otimes 3}\) parity identity used in the proof.

The `generated/` directory contains the exact ordinary \(k=3,4,5\)
CNFs, DRAT proofs, and solver status files, together with the native-XOR
instances through \(k=6\).  The separate `generated-k6/`
directory, when present in a working tree, contains an interrupted
ordinary-CNF run and is not part of the certified package.

The optional heuristic search

```sh
clang++ -std=c++20 -O3 -DNDEBUG search_k6.cpp -o search_k6
./search_k6 500
```

does not prove anything unless it prints a zero candidate, which must
then be confirmed by the exact checker.

The several-support-circuit case without the separate charge condition
remains open.  This package is not a FiveCDC resolution.
