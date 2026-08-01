# Support-16 four-terminal matching-game blind audit

Run from this directory:

```sh
python3 -B audit.py
```

The standard-library checker independently reconstructs the eight states
from the published residual TSV; verifies the
`exists pair / forall matching / exists observed subset` quantifiers;
enumerates every abstract matching and every legal path subset; replays all
160 stored certificate rows; and reconstructs both 42-vertex literal graph
realizations, their adverse path systems, flows, bridge tests, and Tait
colourings.

Expected stdout is frozen in `audit-output.json`.  See `AUDIT.md` for the
publication verdict, the one certificate-field naming clarification, and
the exact scope.  No candidate code is imported, and no preprint or Git
state is modified.
