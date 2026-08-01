# Exact size-fifteen minimum-projection frontier

Date: 2026-07-29

Status: **SIZE-FIFTEEN FRONTIER PROVED WITH A HUMAN TENSOR ARGUMENT,
EXACT FINITE CENSUS, AND KEMPE CERTIFICATES / CUBIC SPLIT-OCCURRENCE
MODEL ONLY / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

This package advances the minimum-extendable-projection program from
support size fourteen to size fifteen in finite connected bridgeless
loopless cubic multigraphs.  Parallel edges are allowed.  It does not
contain a reduction from arbitrary degree, and it does not claim FiveCDC.

## Theorem

Let \(h\) be a binary cycle of minimum cardinality among the first
coordinates of nowhere-zero
\(\mathbb F_2\times\mathbb F_2^2\)-flows on such a graph.  An extension
is **clean** when, for every component \(W\) of \(G-h\), each of the four
low colours occurs an even number of times on \(\delta(W)\).

> **Theorem.** Every cardinality-minimum extendable projection of size
> at most fifteen is cleanable.

The sibling through-size-fourteen package proves the preceding cases.
This package proves the size-fifteen step.  It neither bounds the
minimum support in general nor proves that a counterexample to FiveCDC
must have support at most fifteen.

## Exact size-fifteen census

The primary classifier uses the same conventions and mutually exclusive
outcomes as the frozen through-size-fourteen package.

| shape | canonical words | charge-valid | dirty | direct clean | delete | residual |
|:---:|---:|---:|---:|---:|---:|---:|
| 4+4+7 | 34 | 45,252,514 | 40,901,504 | 40,901,444 | 60 | 0 |
| 4+5+6 | 72 | 94,943,832 | 85,691,028 | 85,687,790 | 3,238 | 0 |
| 5+5+5 | 20 | 26,498,996 | 23,865,564 | 23,865,124 | 440 | 0 |
| 4+11 | 985 | 1,305,883,765 | 1,166,954,048 | 1,166,933,276 | 20,772 | 0 |
| 5+10 | 1,489 | 1,975,366,285 | 1,762,347,048 | 1,761,806,487 | 540,561 | 0 |
| 6+9 | 1,924 | 2,555,260,324 | 2,281,097,772 | 2,280,299,726 | 798,046 | 0 |
| 7+8 | 1,964 | 2,609,251,412 | 2,328,991,036 | 2,327,987,350 | 997,650 | 6,036 |
| 15 | 20,004 | 26,634,745,428 | 23,398,774,592 | 23,398,774,592 | 0 | 0 |
| **total** | **26,492** | **35,247,202,556** | **31,088,622,592** | **31,086,255,789** | **2,360,767** | **6,036** |

The complete shape list and the human interpretation of every finite
test are proved in `HUMAN-PROOF.md`.

The single-circuit row is also covered without enumeration by the
universal tensor theorem in
`minimum-projection-single-circuit-tensor-frontier-20260729/`.  The
sixteen completed anchor/Laplacian shards are retained as an exact
finite cross-check.  The independently written parser and audit in
`minimum-projection-size15-anchor-single-audit-20260729/` verify:

```text
canonical_words=20,004
charge_valid=26,634,745,428
initially_clean=3,235,970,836
dirty=23,398,774,592
direct_clean=23,398,774,592
failures=0
```

The separate zero-sum-partition recurrence first reproduces the frozen
single-circuit size-fourteen counts exactly and then independently
derives the charge-valid and dirty totals above.

The tensor proof has a useful several-circuit corollary.  If every
complement block is charge-balanced separately on every support circuit,
then the per-circuit pair tensors add to one tensor instance, so one map
tuple cleans all circuits simultaneously.  Ordinary boundary states
need only total blockwise balance across all circuits; the stronger
hypothesis is not automatic, and the multi-circuit census remains
necessary.

## Targeted residual regression

Inverting a same-block smoothing on the 224 frozen size-fourteen
residual rows produces 6,180 distinct raw size-fifteen states.  Every
one is again a direct clean/delete residual:

```text
unique_extensions=6180
RESULT clean=0 delete=0 residual=6180
```

The realization-robust one/two-path Kempe game rescues all of them:

```text
RESULT checked=6180 robust=6180 kempe_counterstates=0
```

The full \(7+8\) census emitted 6,036 residual rows.  The separately
written package `minimum-projection-size15-induction-audit-20260729/`
canonically checked every row: all 6,036 belong to the targeted family
and therefore transport one of the realization-robust one/two-path
Kempe rescues checked above.  They represent 5,200 fully canonical
states, with digest
`f2c0c2b53322c72f00672e3f9c7d807aeb26a6ba771357a673c84c2fdaf96206`.
No other completed shape has a residual.

As a redundant literal check, `verify_full_residual_kempe.py` runs the
same realization-robust game directly on every emitted residual:

```text
RESULT checked=6036 robust=6036 kempe_counterstates=0
```

## Reproduction and frozen checks

The census is exactly divided by canonical-word index modulo sixteen:

```sh
./run_census.sh
```

`verify_baseline.cpp` is the direct size-fifteen specialization of the
frozen size-fourteen classifier.  `verify_sharded.cpp` adds a logically
equivalent pruning: it computes each component/map contribution to the
support-circuit closure equations and skips a full clean/delete
evaluation when their xor is nonzero.

`verify_summary.py` requires all 112 multi-circuit shard files, all
sixteen single-circuit shard files, and `EXPECTED.json`.  It verifies
disjoint shard coverage, accounting identities, all frozen totals, the
literal count of 6,036 residual rows, and their sorted SHA-256 digest.

Targeted regressions replay with:

```sh
python3 targeted_extensions.py
python3 verify_targeted_kempe.py
python3 verify_full_residual_kempe.py
python3 verify_smoothing_obstruction.py
python3 single15_zero_sum_partition_audit.py --length 14
python3 single15_zero_sum_partition_audit.py --length 15
shasum -a 256 -c SHA256SUMS
```

## Trust boundary and disclosure

The classifier retains every zero-charge abstract component partition.
This is a safe over-approximation: some boundary states may not have a
bridgeless cubic realization.  Word orbits, partition counts, and
primary clean/delete decisions are not independently reimplemented for
all eight branches.  The single-circuit tensor theorem is a
human-checkable proof and the zero-sum recurrence independently checks
its census totals.  The induction-audit package is independently
written, but its coverage conclusion depends on the residual rows
emitted here.

OpenAI Codex agents under human direction proposed the reductions,
implemented and ran the exact searches, and wrote the proof notes.  The
work has not received independent human peer review.
