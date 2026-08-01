# Support-16 four-terminal matching game

This package applies matching-observed bichromatic Kempe path switches
to all eight hard residual partitions for

```text
word       01010123|01012302
derivative 31111131|21113132
```

Results:

- Six residuals have a universal strategy for colour pair `{1,3}`:
  every abstract terminal perfect matching admits a nonempty
  circuit-closed path subset which cleans or deletes.
- The two `8+2+2+2+2` residuals each retain one bad matching for every
  colour pair.
- Both triples of bad matchings are simultaneously realized by literal
  42-vertex simple cubic bridgeless graphs.
- Both realizing graphs are Tait-colourable, so their displayed
  support-16 projections are not globally minimum.

Run from this directory:

```bash
python3 matching_game.py
python3 realization_audit.py
```

Files:

- `HUMAN-PROOF.md`: quantifiers, universal reductions, adverse matching
  tables, graph realization, and scope.
- `matching_game.py`: exact all-matching/all-path-subset search.
- `matching-game-certificate.json`: complete matching-dependent
  strategies and first adverse rows.
- `realization_audit.py`: reconstruction and graph/path audit for both
  surviving systems.
- `SHA256SUMS`: integrity ledger.

This resolves the one-round matching game on the eight fixed-word
residuals.  It does not resolve FiveCDC.
