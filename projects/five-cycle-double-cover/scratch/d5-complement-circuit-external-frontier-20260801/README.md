# Complement-circuit external frontier

This package proves the exact weight-four complement-circuit switching law,
audits its external-interface effect through order 14, and freezes the 12
order-14 countermodels to immediate one-translation rescue.

The countermodels are not FiveCDC counterexamples and lie outside the
non-Tait marked-girth minimal-counterexample domain.  Every one escapes after
two complement translations, or after one boundary-preserving complement
five-circuit followed by ordinary Kempe moves.

Run:

```text
./run_all.sh
```

The full order-14 C++ census requires `geng` and may take several minutes.
`audit_full_cycle_space.py` reuses the frozen all-flow engine from the typed
cap package; `check_literal_delimiter.py` is a standalone semantic replay.

See `HUMAN-PROOF.md` for the proof, exact quantifiers, finite counts, and
AI-use disclosure.
