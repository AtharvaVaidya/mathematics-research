# Typed cap double-star frontier

This package isolates the exact six-state interface needed to paste a
rooted `D5` factor across a cubic three-edge cut.

The human result is conditional: a common physical port pair and common
internal/external mode glue, and a double star on each shore guarantees
such a common state.  The finite result is complete for biconnected simple
cubic graphs through order 14: all 138,144 rooted cap interfaces contain a
double star.

This is not a resolution of the Five-Cycle Double Cover Conjecture.  Read
`HUMAN-PROOF.md` for the definitions, proof, finite scope, and limitation.

Reproduce with:

```sh
./run_all.sh
```

Requirements:

- a C++20 compiler;
- nauty `geng` at `/opt/homebrew/bin/geng`, or set `GENG`;
- Python 3 for the independent through-order-10 replay.

The complete C++ frontier takes roughly one minute on the development
machine.  No SAT solver is used.
