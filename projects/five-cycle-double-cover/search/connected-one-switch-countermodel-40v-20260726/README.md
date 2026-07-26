# Certified 40-vertex connected one-switch countermodel

This package refutes the unrestricted connected one-circuit Fano-flow
domination lemma used as an intermediate approach to the five-cycle
double cover conjecture. It does **not** refute five-CDC; the graph has
an explicit three-cycle double cover.

Read `HUMAN-PROOF.md` first. The proof reduces to:

- a ten-vertex Tait base with the three value-2 edges
  \(02,56,17\) on no common circuit;
- the independently checked ten-vertex bad-flow block; and
- two elementary aligned two-sum arguments.

The final graph is simple, connected, cubic, bridgeless, and has 40
vertices and 60 edges. `independent_checker.py` reconstructs it without
importing the producer and enumerates every connected circuit.
`canonical.g6` is its nauty-canonical graph6 encoding. The graph is
planar.

Run:

```sh
python3 independent_checker.py
python3 verify_package.py
```

The source package containing the bad block is
`../fano-value-class-flow-countermodel-20260726/`.

AI use was substantive and is disclosed in `HUMAN-PROOF.md`. The
package has not received independent human peer review.
