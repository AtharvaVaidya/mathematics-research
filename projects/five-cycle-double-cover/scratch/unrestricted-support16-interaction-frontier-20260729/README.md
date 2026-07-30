# Unrestricted support-16 interaction frontier

Date: 2026-07-29

Status: **COMPLETE CANONICAL FIXED-WORD SUBCASE / EIGHT EXACT DIRECT
RESIDUALS / NOT A FULL SUPPORT-16 CENSUS / NOT A FIVECDC RESOLUTION**.

The requested all-shape support-\(16\) abstract census is too large for
this turn.  This package instead freezes a deliberately bounded but
complete subcase: every charge-valid complement-component partition of
the canonical hard word

```text
01010123|01012302
```

on two 8-circuits.  Interaction loops and complement blocks with more
than two occurrences are both allowed.  States consisting only of
loopless two-occurrence blocks would be excluded because they are covered
by the earlier theorem; this word has no such charge-valid partition.

The exact classification is:

| outcome | states |
|---|---:|
| clean | 8,041,808 |
| no clean map, but a strict circuit deletion exists | 4,514 |
| direct residual: neither clean nor strict-delete | 8 |
| **total** | **8,046,330** |

All counts are canonical state counts for this word orbit.  The full
dihedral/circuit-swap action has 512 normalized word images, all
different, and the displayed word is their unique minimum.  Its
stabilizer is therefore trivial.  Restricted-growth component labels
make every generated partition key unique.

The eight residuals are listed in `residuals.tsv`.  Each has five
components and exactly 320 feasible normalized component-map tuples,
with zero clean and zero deleting tuples.  The existing displayed
partition

```text
0123444444130244
```

from `minimum-projection-size16-multiswitch-counterstate-20260729` is one
of the eight.

## Precise minimum-projection meaning

The three categories are deliberately direct:

- a clean state already supplies the desired clean extension;
- a strict-delete state cannot be a cardinality-minimum extendable
  projection, because the deleting circuit toggle yields a smaller
  extendable projection;
- a residual survives only this direct component-map/translation test.

A residual is **not** thereby a globally minimum projection.  An abstract
boundary partition does not encode complement interiors, Kempe path
pairings, bridgeless realizability, or competing projections.  The known
42-vertex realization of `0123444444130244` is Tait-colourable and has
minimum projection zero.  This package constructs no graph realization
for the other seven residuals.

## Completeness boundary

Minimum-projection colour use leaves the support shapes

```text
16
4+12  5+11  6+10  7+9  8+8
4+4+8  4+5+7  4+6+6  5+5+6
4+4+4+4
```

The single-circuit shape is already covered by the tensor theorem.
This package completes one canonical word orbit in `8+8`; it does not
cover the remaining word orbits in `8+8` or any of the other nine
multi-circuit shapes.

There are 5,544 proper all-four-colour cyclic words of length eight, so
there are \(5,544^2=30,735,936\) ordered raw `8+8` word pairs.  The
global affine, two dihedral, and circuit-swap group has order 12,288.
Consequently `8+8` alone has at least 2,502 canonical word orbits.  This
package covers one of them—at most \(1/2502\), about 0.04%, of the
`8+8` word orbits.  State counts are not uniform across word orbits, so
that percentage must not be read as a percentage of all boundary states.

## Replay

```sh
sh run_all.sh
```

The primary C++ program exhausts all partitions and all component maps.
The first Python audit independently counts the charge-valid partitions
and the loop-only pair subcase.  The second Python audit independently
generates `GL(2,2)` from invertible matrices and replays all eight
residuals literally, including their canonical keys and occurrence
matrices.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, chose the bounded
subcase, wrote the programs and prose, and ran the checks.  The package
has not received independent human review.  It makes no FiveCDC
resolution or literature-priority claim.
