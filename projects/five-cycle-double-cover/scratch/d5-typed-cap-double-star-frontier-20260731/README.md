# Typed cap double-star frontier

This package isolates the exact six-state interface needed to paste a
rooted `D5` factor across a cubic three-edge cut.

The human result is conditional: a common physical port pair and common
internal/external mode glue, and a double star on each shore guarantees
such a common state.  The finite result is complete for biconnected simple
cubic graphs through order 14: all 138,144 rooted cap interfaces contain a
double star.

A supplemental single-implementation run extends the same exact C++ census
to order 16: all 1,301,664 rooted interfaces on the 3,874 biconnected simple
cubic graphs contain a double star.  The only masks remain
`15,47,51,59,60,62,63`.  Two complete executions agree, one monolithic and
one in four shards, but both use the same enumerator.  This order-16 result
therefore has no independent second implementation and is not promoted to
the main human/finite theorem.  It is also far below the order-56 cutoff
for caps in the marked-girth obstruction branch.

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

The optional order-16 extension takes roughly 25 minutes on the development
machine and is replayed separately with:

```sh
./run_order16.sh
```
