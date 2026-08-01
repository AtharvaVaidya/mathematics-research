# External coverage under component-Kempe splicing

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE CONDITIONAL LEMMAS / EXACT FINITE
DELIMITERS / NOT A UNIVERSAL EXTERNAL-COVERAGE THEOREM / NOT A PROOF OF
FIVECDC**.

This scratch package records the exact effect of a component Kempe switch
on every factor, and applies it to the retained Petersen--Foster fixed-flow
obstruction.

The key identity is

```text
Y_P(sw_T,D(q)) = Y_P(q) xor D       when |P intersection T| = 1,
Y_P(sw_T,D(q)) = Y_P(q)             otherwise.
```

Thus a switch is literally a circuit splice for the six factors crossing
its coordinate pair.  On the retained 890-vertex flow, six of the 124
possible component switches repair the missing external port.  The checker
reconstructs all six repairs from literal labels.

The report distinguishes a witness for one selected port, aggregate
coverage using possibly different flows, orbit-aggregate coverage, and the
stronger condition that one flow simultaneously covers all three ports.

Two eight-vertex examples delimit possible strengthenings:

- one selected port of the cube has no external witness after zero or one
  component switch from the displayed flow, but has one after two switches;
- an internal state on a second graph cannot be changed to an external state
  on the same physical pair in zero or one switch, but can in two.

These examples do not refute the existential statement, because the
displayed two-switch paths are positive witnesses.

Run:

```sh
./run_all.sh
```

See `HUMAN-PROOF.md` for the proofs and exact scope.
