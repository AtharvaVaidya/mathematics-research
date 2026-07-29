# Size-fifteen induction audit

This package isolates the exact logical content of smoothing an
order-fifteen boundary state to order fourteen.

It proves the removable repeated-colour lemma, gives necessary and
sufficient lift tests for fixed clean/deletion certificates, describes
the matching-level Kempe lift criterion, and independently checks
canonical equivalence to the 224 frozen order-fourteen residuals.

Run the frozen targeted-family audit with:

```sh
python3 audit_induction.py
```

To audit full-census residual files:

```sh
python3 audit_induction.py --expect-full-7p8 /path/to/*-shard16-*.txt
```

The checker ignores non-`COUNTERSTATE`/`RESIDUAL` lines and fails if it
finds zero residual rows.  Use `--allow-empty` only for a deliberately
empty shape.  Shard completeness must still be verified separately.

Canonical-set digests are SHA-256 hashes of the lexicographically sorted
ASCII lines

```text
length+length word|word partition
```

including one final newline per state.  The targeted 6,180 literal rows
have 5,622 fully canonical classes and digest
`703a6beac5682565e1c0f0bc6a4f4e481ea2508cde4589047c87483fdb1c416a`.

The complete primary \(7+8\) census emits 6,036 residual rows.  Every
row is covered; they form 5,200 fully canonical classes with digest
`f2c0c2b53322c72f00672e3f9c7d807aeb26a6ba771357a673c84c2fdaf96206`.
The `--expect-full-7p8` flag makes those counts and the digest mandatory.

This is a partial computational boundary result, not a resolution of
the Five-Cycle Double Cover Conjecture.
