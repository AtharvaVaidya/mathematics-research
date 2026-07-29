# Independent audit of the order-fifteen one-circuit census

Date: 2026-07-29

Status: **EXACT SHARD AGGREGATION / ZERO-SUM-PARTITION CROSS-CHECK /
ZERO DIRECT-CLEANING FAILURES / CUBIC SPLIT-OCCURRENCE BOUNDARY MODEL /
NOT A FIVECDC RESOLUTION**.

## 1. Input boundary

The primary run divides the 20,004 canonical proper cyclic words of
length fifteen by word index modulo sixteen.  Every shard emits one
terminal row with its:

- shard index and selected-word count;
- charge-valid, dirty, and directly clean partition counts;
- failure count; and
- anchor-system and literal evaluation counts.

The independent parser requires exactly sixteen files and exactly one
well-formed terminal row in each.  It checks that shard indices
\(0,\ldots,15\) occur once each, that all rows declare the same
20,004-word universe, and that selected-word counts sum to 20,004.
It rejects any `COUNTERSTATE` line.

## 2. Independent partition-count comparison

The separate zero-sum-partition recurrence does not enumerate set
partitions and does not use the component-map cleaner.  It gives

```text
charge-valid     26,634,745,428
initially clean   3,235,970,836
dirty            23,398,774,592
```

Summing the sixteen primary terminal rows gives those three values
exactly.  In particular,
\[
 26{,}634{,}745{,}428-23{,}398{,}774{,}592
 =3{,}235{,}970{,}836.
\]

There is one one-block partition for each canonical word.  The cleaner
returns before its initial literal obstruction evaluation on those
rows.  Hence the expected number of generic evaluations is
\[
 26{,}634{,}745{,}428-20{,}004
 =26{,}634{,}725{,}424,
\]
which is also the exact aggregated value.

## 3. Direct-cleaning result

The aggregated terminal counts are

```text
dirty                 23,398,774,592
directly clean        23,398,774,592
failures                           0
anchor systems       199,816,760,346
anchor evaluations   199,816,760,346
```

Thus every dirty abstract one-circuit state in the order-fifteen census
has a directly cleaning component-map assignment.  The computation is
an exact finite cross-check of the separately proved universal
one-circuit tensor theorem.

The seconds field is deliberately excluded from the logical digest.
Sorting the sixteen rows by shard and hashing all other integer fields
gives

```text
0a227e97a93e36b3063261335755483f2e6f34cbf7d9a4226e0782917f479c51
```

## 4. Scope

This audit checks aggregation, partition-count agreement, and absence
of primary failures.  It is not a separately implemented cleaner or
canonical-word generator.  The one-circuit tensor proof supplies the
human theorem; this census supplies a large exact regression.

Several support circuits still require the separate smoothing/Kempe
arguments.  No arbitrary-degree reduction or FiveCDC resolution is
claimed.

OpenAI Codex agents under human direction wrote the parser and this
audit note.  The work awaits independent human review.
