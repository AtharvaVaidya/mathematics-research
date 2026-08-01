# Independent size-twelve clean-or-delete audit

Date: 2026-07-29

Status: **INDEPENDENT EXACT REPLAY / NOT A FIVECDC RESOLUTION**.

This package independently reproduces the abstract size-twelve boundary
census used by the minimum-extendable-projection programme.  It does not
import or link the primary through-twelve verifier.

Run:

```sh
python3 replay.py
shasum -a 256 -c SHA256SUMS
```

The first command compiles the C++17 auditor in a temporary directory,
regenerates every word orbit, and checks all five support shapes.  On the
reference machine it takes about one minute.

## Independent method

`independent_word_orbits.py` generates proper cyclic words on the four
points of \(\mathbb F_2^2\), requiring every circuit to use all four
points.  It quotients by first-occurrence colour normalization (the global
\(S_4=\mathrm{AGL}(2,2)\) action), independent dihedral actions on the
circuits, and permutations of equal-length circuits.

For each word, `independent_audit.cpp` does not scan Bell-number many set
partitions.  It first enumerates every vertex block whose four
colour-cut parities agree.  It then generates every partition as an
exact cover by such blocks, fixing the least remaining vertex to avoid
component-order duplicates.  This is equivalent to the component
charge condition because every circuit cut has even size.

For every dirty partition, the auditor independently enumerates all six
\(\mathrm{GL}(2,2)\) maps on every component.  It checks cyclic
consistency separately on every support circuit.  It then:

1. tries every relative circuit starting colour and tests all four
   repaired cut-colour parities for direct cleanliness; and
2. if direct cleaning fails, tests whether a repaired circuit omits one
   low colour.  Translating that circuit by the omitted colour makes all
   its low values nonzero, so deleting the circuit from the
   first-coordinate support gives a strictly smaller extendable
   projection.

A common translation of all circuits merely permutes the four repaired
colours, so the first circuit start is fixed to zero without loss.

## Frozen results

| shape | word orbits | charge-valid | dirty | direct failures | neither clean nor delete |
|:--:|--:|--:|--:|--:|--:|
| \(12\) | 1,014 | 14,196,654 | 11,465,978 | 0 | 0 |
| \(4+8\) | 66 | 922,048 | 773,721 | 4 | 0 |
| \(5+7\) | 64 | 884,604 | 738,969 | 206 | 0 |
| \(6+6\) | 66 | 926,640 | 774,196 | 182 | 0 |
| \(4+4+4\) | 3 | 41,975 | 35,960 | 0 | 0 |

Thus all 392 direct-repair failures have a strictly smaller
union-of-circuits support.  No abstract clean-or-delete failure occurs
at size twelve.

## Trust boundary and disclosure

This audit independently regenerates the word orbits, valid block exact
covers, component-map search, cleanliness decisions, and
circuit-deletion decisions.  It shares the mathematical boundary model
with the primary work and does not independently prove the
minimum-projection exchange theorem or the implication from a clean
projection to FiveCDC.

OpenAI Codex agents under human direction designed and implemented this
independent audit.  Source and exact counts are included for review
without trusting an AI-generated summary.  The result has not received
independent human peer review and makes no literature-wide priority
claim.
