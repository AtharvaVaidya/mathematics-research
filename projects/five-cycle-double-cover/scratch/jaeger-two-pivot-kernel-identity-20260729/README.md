# Two-pivot kernel interaction

This package proves the exact single- and two-pivot odd-kernel identities
in `HUMAN-PROOF.md` and independently checks a 130-vertex counterstate to
naive two-exchange additivity.

The finite witness shows that an exchange can leave all three kernels,
the full Fano flow, profile, and span flags unchanged while altering the
fundamental circuit used by a later disjoint exchange. Consequently,
flow-only or kernel-only uncrossing cannot establish a universal
radius-two descent theorem.

This is auxiliary structural progress, not a FiveCDC resolution.

The note also relates the kernel update to Hušek--Šámal's Theorem 3.16
component-parity criterion and proves an exact fixed-first-bit-cycle
preservation rule. A subsequent exact order-40 counterstate requires
three disjoint exchanges, so radius two itself is not universal.

Run:

```bash
python3 verify.py
python3 verify_radius3_cube.py
shasum -a 256 -c SHA256SUMS
```

AI-use disclosure: OpenAI Codex agents performed the derivation,
computation, checking, and drafting under human direction.
