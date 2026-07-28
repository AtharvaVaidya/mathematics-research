# Order-30 focused theta-choice census

Status: **VERIFIED FINITE STRUCTURAL RESULT — NOT A FIVE-CDC
RESOLUTION**.

This package classifies every unordered pair of independent edges in the
139,854 order-30 simple cubic snarks of cyclic edge-connectivity at least
four in the cited House of Graphs corpus.  For roots \(R\), put
\[
                         H=G-V(R).
\]
When \(H\) has deficiency two, the two implementations enumerate maximum
near-perfect matchings until the complement of the roots and matching is
bridgeless.  In the proved two-core dichotomy this is exactly the theta
outcome; exhausting all maximum matchings would be the all-dumbbell
outcome.

The two implementations agree exactly:

| quantity | total |
|---|---:|
| graphs | 139,854 |
| independent root pairs | 125,868,600 |
| deficiency zero | 124,646,796 |
| deficiency two, theta found | 1,221,804 |
| deficiency two, all dumbbell | **0** |
| deficiency-two boundary six | 0 |
| deficiency-two boundary eight | 1,221,804 |
| near-perfect matchings checked through first theta | 7,814,531 |

The primary implementation is C++20.  The clean-room replay is a
separately written Python standard-library program, run in sixteen
disjoint graph-index shards.  All shards report `PASS`; their sum equals
the primary result in every field.

## Exact claim boundary

This proves only that no all-dumbbell prescribed-root obstruction occurs
in this finite corpus.  It does **not** prove:

- the universal focused theta-choice lemma;
- the Five-Cycle Double Cover Conjecture;
- a result for multigraphs;
- an orientable five-cycle double cover statement; or
- novelty relative to the published finite orientable computations.

The standard Five-CDC remains open.

## Corpus

Source: [House of Graphs snark directory](https://houseofgraphs.org/meta-directory/snarks)

Direct retained file:
`Generated_graphs.30.04.sn.cyc4.g6.gz`.

- compressed SHA-256:
  `93b8abf7b907fee03b9ecb99b917d14c2cc4f97bc115c0e793635db22c408567`;
- decompressed SHA-256:
  `bc6f29ec50910eae345ced81f87800686deb069dd1cb383d73dbcc56765f247d`;
- 139,854 distinct graph6 records.

The package verifier independently checks the hashes, uniqueness, order,
and simple-cubic degree profile of every retained record.  The snark and
cyclic-connectivity classification is inherited from the cited source
corpus.

## Files

- `report.json`: frozen scope, totals, source attribution, and hashes;
- `primary_census.cpp`: primary exact classifier;
- `independent_verifier.py`: clean-room semantic replay;
- `verify.py`: compact corpus/hash/aggregate audit;
- `artifacts/primary-result.json` and `artifacts/primary.log`;
- `artifacts/independent/shard-*.json` and `shard-*.log`;
- `SHA256SUMS`: complete package integrity ledger.

See `REPRODUCING.md` for exact commands.

## AI-use disclosure

The research workflow, code, verification design, and exposition were
developed with substantial assistance from OpenAI Codex under human
direction.  The finite claim is supported by two source-visible
implementations and deterministic artifacts.  No AI-generated or
computer-generated observation here is represented as a proof of the
universal conjecture.
