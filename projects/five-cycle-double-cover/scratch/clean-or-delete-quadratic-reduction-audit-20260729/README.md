# Quadratic-reduction hostile audit

This package independently audits Propositions 1--5 of
`clean-or-delete-quadratic-reduction-20260729.md`.

Run:

```bash
python3 verify_quadratic_reduction.py
```

The checker uses only the Python standard library.  It verifies all 16
local six-map rows and 126,258 balanced literal circuit rows through
length eight.

The audit validates legal neutralization of one current dual witness.
It explicitly does not infer simultaneous cleanliness or FiveCDC.
