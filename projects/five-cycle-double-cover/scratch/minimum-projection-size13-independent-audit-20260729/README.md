# Independent size-thirteen clean-or-delete audit

Date: 2026-07-29

Status: **INDEPENDENT EXACT REPLAY / NOT A FIVECDC RESOLUTION**.

This package independently reproduces the abstract size-thirteen
clean-or-delete boundary census.  It imports no code or data from the
primary through-thirteen package.

Run:

```sh
python3 replay.py
shasum -a 256 -c SHA256SUMS
```

The replay compiles `independent_audit.cpp` as C++17 in a temporary
directory, regenerates every canonical word orbit, exhausts every valid
block exact cover, and compares the resulting summary byte for byte with
`full-run-output.txt`.  The 2,583 single-thirteen-cycle word orbits are
split across at most eight local worker processes.  No network access or
third-party Python package is used.

## Independent method

`independent_word_orbits.py` generates proper cyclic words on the four
points of \(\mathbb F_2^2\), requiring every circuit to use all four
points.  It quotients by first-occurrence colour normalization, the
independent dihedral action on every circuit, and permutations of
equal-length circuits.

For a fixed word, the C++ auditor first enumerates every vertex block
whose four colour-cut parities agree.  It generates set partitions as
exact covers by these valid blocks, fixing the least uncovered vertex
to avoid component-order duplication.  On every dirty state it tries all
six \(\mathrm{GL}(2,2)\) maps on every block, checks circuit consistency,
and tests all relative circuit translations for cleanliness.

If direct cleaning fails, the same map search checks whether an integrated
circuit word omits a low colour.  Translating by the omitted colour makes
every low value on that circuit nonzero, so removing it from the
first-coordinate support yields a strictly smaller extendable
projection.  This is the deletion alternative.

## Exact results

| shape | word orbits | charge-valid | dirty | direct failures | neither clean nor delete |
|:--:|--:|--:|--:|--:|--:|
| \(13\) | 2,583 | 155,381,679 | 129,684,490 | 0 | 0 |
| \(4+9\) | 130 | 7,753,918 | 6,657,654 | 60 | 0 |
| \(5+8\) | 203 | 12,144,485 | 10,404,652 | 3,224 | 0 |
| \(6+7\) | 242 | 14,480,258 | 12,415,026 | 4,390 | 0 |
| \(4+4+5\) | 4 | 238,522 | 208,144 | 0 | 0 |

In total, 159,369,966 dirty states were checked.  All 7,674 direct
failures have a proper circuit-deletion witness.  There is no
clean-or-delete failure.

## Full-run provenance

The frozen output records a complete successful run on 2026-07-29 in the
Codex macOS workspace, using the system Python 3 interpreter and the
system `c++` compiler with:

```text
-O3 -std=c++17 -Wall -Wextra -pedantic
```

The single-circuit total was independently accumulated from eight
disjoint orbit chunks:

```text
(323, 19474925, 16279298, 0, 0)
(323, 19385069, 16138184, 0, 0)
(323, 19473161, 16268540, 0, 0)
(323, 19545083, 16283704, 0, 0)
(323, 19297049, 16031352, 0, 0)
(323, 19355219, 16152208, 0, 0)
(323, 19505771, 16342084, 0, 0)
(322, 19345402, 16189120, 0, 0)
```

Their sum is the first row of the exact table.  The other four shapes
were each run to completion in one process.  `replay.py` repeats the full
calculation rather than trusting these provenance tuples.

## Trust boundary and disclosure

This package independently checks word-orbit generation, valid partition
generation, component-map feasibility, direct cleanliness, and the
missing-colour deletion alternative.  It shares the mathematical boundary
model with the primary project; it does not independently prove the
minimum-projection exchange theorem or the Hušek--Šámal implication.

OpenAI Codex agents under human direction designed and implemented this
audit.  The source, frozen output, and full replay are included for review
without trusting an AI-generated summary.  This has not received
independent human peer review and makes no literature-wide priority claim.
