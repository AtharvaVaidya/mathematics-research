# Support-16 loop and higher-occurrence reduction

This package proves that every flowable two-occurrence interaction state
of support at most 16 cleans or deletes even when interaction loops are
allowed.  Together with the prior loopless theorem, it covers all
two-occurrence states through 16 and loopless states through 18.

It also proves that a forced two-terminal Kempe switch in a
higher-occurrence complement component is boundary-equivalent to an
already available uniform `GL(2,2)` component map.  In particular, this
move does not resolve the four hard support-16 abstract residuals which
contain six three-occurrence blocks.

Run the exact verifier from the repository root:

```bash
python3 projects/five-cycle-double-cover/scratch/support16-loop-higheroccurrence-reduction-20260729/verify.py
```

Expected final line:

```text
PASS support-16 loop/higher-occurrence exact verifier
```

Files:

- `HUMAN-PROOF.md`: definitions, legal moves, full shape reduction,
  finite tables, sharp length-six failures, and scope.
- `verify.py`: self-contained exact finite verifier.
- `SHA256SUMS`: integrity ledger.

This is a bounded structural theorem, not a resolution of the
Five-Cycle Double Cover Conjecture.
