# Support-16 loop theorem blind audit

Run:

```sh
python3 audit.py
```

The independent standard-library checker validates the marked-word orbit
counts, the 138 paired-port cases used by the shape reduction, the exact
four-profile remainder, and all 16,344 literal endpoint-set cleaning/deletion
tests.  See `AUDIT.md` for the findings and publication boundary.

The final bounded theorem is conditional on two results imported by the
candidate proof:

1. the prior loopless two-occurrence theorem; and
2. the universal one-circuit tensor theorem.

This audit neither reproves those dependencies nor independently checks the
candidate package's separate higher-occurrence no-go census.  No preprint or
Git state is modified.
