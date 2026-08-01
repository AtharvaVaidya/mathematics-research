# Independent order-fifteen anchor-shard aggregation

Status: **ALL SIXTEEN RESULT FOOTERS INDEPENDENTLY AGGREGATED / EXACT
AGREEMENT WITH ZERO-SUM-PARTITION RECURRENCE / ZERO FAILURES / NOT A
FIVECDC RESOLUTION**.

`audit_anchor_shards.py` parses exactly one result footer from each of
the sixteen one-circuit anchor census shards.  It checks:

- all shard indices occur exactly once;
- the selected canonical-word total is 20,004;
- charge-valid and dirty totals agree with the independent
  zero-sum-partition recurrence;
- every dirty state directly cleans; and
- no counterstate or failure row occurs.

Run after the shards finish:

```bash
python3 audit_anchor_shards.py /tmp/fivecdc15-run/15-shard16-*.txt
```

The script uses only the Python standard library.  `HUMAN-PROOF.md`
records the audit boundary, and `verification-output.txt` freezes the
passing aggregation.
