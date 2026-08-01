# Rooted D5-interface census through the retained order-34 corpus

Status: **certificate-checked finite theorem / no universal claim / no
resolution of FiveCDC**.

This package proves three positive rooted-interface predicates for:

- every one of the 3,874 biconnected simple cubic graphs on 16 vertices;
- every graph in the retained canonical cyclically 4-edge-connected non-Tait
  corpora at orders 18, 20, 22, 24, and 26 (1,491 graphs total); and
- the seven literal rows in the retained order-34 strong-snark file.

There are 5,372 graphs and 2,674,404 proper `(cap vertex, root edge)`
interfaces in total.  All 2,674,404 interfaces satisfy each of:

1. the aggregate typed signature contains a double star;
2. aggregate external components cover all three cap ports; and
3. one individual `D5` flow has external components through the root that
   collectively cover all three cap ports.

The C++ search writes a compact positive certificate containing 124,081
explicit `D5` flows.  A separately written Python checker decodes every graph,
checks every flow's vertex xor equations, reconstructs every factor component,
and verifies every claimed interface.  It also independently checks the graph
premises: cubicity and biconnectedness throughout, and non-Taitness and cyclic
4-edge-connectivity for the named snark corpora (plus girth at least five for
the order-34 file).

Run from this directory:

```sh
./run_all.sh
```

Requirements are Python 3, a C++20 compiler, and nauty `geng` (set `GENG` if
it is not `/opt/homebrew/bin/geng`).  The development run takes several
minutes; order 26 dominates the independent replay.

The exact theorem, definitions, proof obligations, limitations, provenance,
and AI-use disclosure are in `HUMAN-PROOF.md` and `SOURCES.md`.
