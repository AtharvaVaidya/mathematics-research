# Complete order-28 cyclically-four two-witness classification

Status: **COMPLETE EXPLICIT-WITNESS CLASSIFICATION OF THE RETAINED
12,517-GRAPH SOURCE / TWO INDEPENDENT FULL REPLAYS PASS / NOT FIVE-CDC**.

The retained source is the output of

```sh
snarkhunter 28 4 S s C4 o g
```

and contains 12,517 cyclically 4-edge-connected non-3-edge-colourable
simple cubic graphs of order 28 and girth at least four.  Completeness of
this canonical source relies on Snarkhunter 2.0b and its documented option
semantics.

Deleting every independent edge pair gives 9,725,709 terminal-distinct
four-poles.  For every pole, the retained certificate stream displays two
complete fixed-five \(D_5=\binom{[5]}2\) edge labellings:

1. boundary orbit 0, represented by \((01,01,01,01)\);
2. boundary orbit 2, represented by \((01,01,23,23)\).

The eight producer shards completed with status zero:

```text
source caps                         12,517
deletion four-poles              9,725,709
explicit D5 labellings          19,451,418
missing witnesses                        0
```

The first three published exceptional exact masks omit orbit 2 and the
last three omit orbit 0.  Therefore no retained pole has any of the six
exceptional exact fixed-five signatures.

`verify.py` reconstructs every deletion from its cap and checks every
displayed labelling at every vertex.  The separately written zlib/C++
checker `scratch/verify_boundary_two_orbit_witness_fast.cpp` instead
reads the pole stream as primary input and checks both witnesses without
importing the producer or the package verifier.  Both full replays pass.

Together with the human endpoint-fork lift for cyclic-three caps, this
finite classification raises the scoped simple terminal-distinct
fixed-five exceptional-pole lower bound from 28 to 30.  It does not prove
that exceptional poles never exist and does not resolve the Five-Cycle
Double Cover Conjecture.

See `THEOREM.md` for the proof and exact scope, and `REPRODUCING.md` for
replay instructions.
