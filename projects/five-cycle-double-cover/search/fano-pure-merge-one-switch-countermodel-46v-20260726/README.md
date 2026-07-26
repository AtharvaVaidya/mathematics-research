# 46-vertex Fano pure-merge one-circuit countermodel

This directory freezes a human-verifiable countermodel to a proposed
five-cycle-double-cover proof strategy.

The exact theorem is in `HUMAN-PROOF.md`: one fixed nowhere-zero
\(\mathbb F_2^3\)-flow has no potential-compatible eight-cover that purely
merges into five coordinates, and no switch on one connected circuit repairs
that defect. The construction is a simple connected bridgeless cubic graph
on 46 vertices.

This is **not** a five-cycle-double-cover counterexample. The same graph has
the explicit cover sizes `46 46 46 0 0`.

Files:

- `HUMAN-PROOF.md` — complete mathematical argument and AI-use disclosure;
- `construction.json` — full graph, flow, labels, coloring, and provenance;
- `independent_checker.py` — independent standard-library checker;
- `independent-check.json` — frozen checker output;
- `canonical.g6` — nauty-canonical graph6 record.

Run:

```bash
python3 independent_checker.py
```

Expected final JSON line:

```text
{"five_colorable_solutions": 0, "potential_solutions": 128, "status": "PASS", ...}
```

The SAT encodings used during discovery are diagnostic only. The theorem in
`HUMAN-PROOF.md` does not depend on their UNSAT answers.
