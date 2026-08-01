# Simultaneous external-state frontier

This package checks a strengthening of the typed-cap gluing premise.  For a
proper cap/root interface `(z,r)`, it asks for **one** `D5` flow in which
external factor components through `r` collectively meet all three physical
ports at `z`.

The exact all-flow census passes for every biconnected simple cubic graph of
even order 4 through 14:

- 587 graphs;
- 565,046 canonical flows modulo global `S5`; and
- 138,144 proper rooted interfaces.

A structurally separate Python replay passes through order 12.  Run both with

```sh
./run_all.sh
```

Requirements are a C++20 compiler, Python 3, and nauty `geng` at
`/opt/homebrew/bin/geng` (or set `GENG`).  On the development machine the full
run takes about two minutes.

This is an order-bounded computer result, not a universal theorem and not a
resolution of FiveCDC.  It is explicitly **not orbitwise**: a particular
component-Kempe orbit can fail the simultaneous property even when another
flow for the same graph and interface succeeds.  See `HUMAN-PROOF.md` for the
exact statement, the elementary gluing implication, limitations, and AI-use
disclosure.
