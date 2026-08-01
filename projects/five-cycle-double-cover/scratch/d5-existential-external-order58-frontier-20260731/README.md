# Existential external-coverage order-58 frontier

This package contains a self-contained edge-rooted nonbacktracking-walk
proof that a relevant three-cut cap starts at order 58, improving the
previous order-56 cutoff.  The proof explicitly audits every possible
degree-one pattern after deletion of the marked root.

Run the arithmetic replay with:

```sh
./run_all.sh
```

The complete replay uses Python 3, CaDiCaL, and CryptoMiniSat.  The smoke
checker currently looks for the solver binaries at
`/opt/homebrew/bin/cadical` and `/opt/homebrew/bin/cryptominisat5`; the exact
versions used for the retained output are recorded in `VERSIONS.txt`.

The accompanying 18-row `(3,9)`-cage control is deliberately scoped: it
does not classify all order-58 caps, because short circuits through the cap
vertex are permitted by the minimum-counterexample geometry.
It additionally gives elementary cycle-packing certificates showing that
five edge subdivisions cannot raise any of those 18 cages to girth ten.

`simultaneous_external_sat.py` gives an exact six-case SAT/XOR
characterization of the stronger target in which one flow has external
states covering all three ports.  Positive models are semantically replayed;
negative answers remain uncertified unless all six emitted proofs are checked
independently.

This package does not prove existential external-port coverage and does not
resolve FiveCDC.
