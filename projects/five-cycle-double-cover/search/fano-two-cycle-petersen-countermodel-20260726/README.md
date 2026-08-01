# Petersen fixed-line quadratic countermodel

This package refutes one intermediate statement in the Fano-flow route:
for a **prescribed** nonzero functional \(\mu\), it is not always possible
to make its kernel line good while preserving \(\mu\circ f\).

It does **not** refute the five-cycle double cover conjecture.  The same
Petersen graph has the explicit five-cycle double cover recorded in
`construction.json`.  Five of the seven Fano lines are cleanable for the
displayed flow; only the lines `123` and `167` fail.

The graph is simple, connected, cubic, bridgeless, nonplanar, has girth
five and cyclic edge-connectivity five, and is isomorphic to the Petersen
graph.  Its nauty-canonical graph6 encoding is:

```text
IsP@OkWHG
```

Read `HUMAN-PROOF.md`, then run:

```sh
python3 independent_checker.py
python3 verify_package.py
```

The first checker independently enumerates the 64 binary cycles and all
4,096 ordered pairs for each line.  The second reconstructs both ordinary
CNFs byte for byte and checks their DRAT proofs with `drat-trim`.

AI use was substantive and is disclosed in `HUMAN-PROOF.md`.  This
package has not received independent human peer review.
