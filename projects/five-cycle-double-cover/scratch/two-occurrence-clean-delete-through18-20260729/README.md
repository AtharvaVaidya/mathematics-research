# Loopless two-occurrence clean-or-delete theorem through support 18

Date: 2026-07-29

Status: **VERIFIED SPECIAL-CASE THEOREM / DIRECT FIVECDC-ROUTE
PROGRESS / NOT A FIVECDC RESOLUTION**.

This package advances the exact loopless two-occurrence frontier from
total support \(16\) to total support \(18\).

> Every flowable loopless two-occurrence interaction state of total
> support at most \(18\) has a nowhere-zero
> \(\mathbb F_2^2\)-interaction flow which either is clean or strictly
> deletes a support circuit.

Consequently, every globally cardinality-minimum extendable projection
in this subclass and range is cleanable.  Cleanability is the condition
used in the Hušek–Šámal Fano-projection formulation of standard FiveCDC.
This closes only a bounded subclass.  It neither proves nor disproves
FiveCDC.

The new support-\(18\) layer reduces to:

- triangle multiplicity profiles
  \((5,2,2),(4,4,1),(4,3,2)\); and
- seven connected bridgeless four-vertex multiplicity profiles of
  degree type \((5,5,4,4)\).

The two exact implementations exhaust all labelled-edge cyclic orders
modulo rotation and reversal.  The primary checker uses the alternating
bilinear translation equations.  The independent audit constructs the
two literal endpoint sets in the \(K_4\) on
\(\mathbb F_2^2\) and compares their cosets without using that equation.

The frozen totals are:

| range | cyclic-order states | clean states | delete-only states | residuals |
|---|---:|---:|---:|---:|
| previous layers through 16 | 22,032 | 21,816 | 216 | 0 |
| new layer at 18 | 1,019,952 | 1,013,220 | 6,732 | 0 |
| combined finite census | 1,041,984 | 1,035,036 | 6,948 | 0 |

Here “clean state” means at least one normalized feasible flow cleans;
“delete-only” means no feasible flow cleans but at least one strictly
deletes.  A state may have both cleaning and deleting flows and is counted
in the first column.

## Replay

From this directory:

```sh
sh run_all.sh
```

Or run the pieces separately:

```sh
python3 enumerate_profiles.py
c++ -std=c++17 -O3 verify_support18.cpp -o /tmp/verify_support18
/tmp/verify_support18
c++ -std=c++17 -O3 independent_literal_audit.cpp \
  -o /tmp/independent_literal_audit
/tmp/independent_literal_audit
shasum -a 256 -c SHA256SUMS
```

The frozen run used Apple clang 21.0.0, Python 3.14.5, and Darwin
25.5.0 arm64.  Both programs use only the C++17 standard library; the
profile enumerator uses only the Python standard library.

## Files

- `HUMAN-PROOF.md`: definitions, reductions, finite-case list, and
  proof of the theorem from the checked census;
- `LEDGER.md`: statement, experiment, obstruction, and proof-obligation
  ledgers;
- `enumerate_profiles.py`: exact classification of the four-vertex
  degree-\((5,5,4,4)\) multiplicity orbits;
- `verify_support18.cpp`: primary alternating-form checker;
- `independent_literal_audit.cpp`: independently structured literal
  endpoint-set checker;
- `verification-output.txt`, `independent-output.txt`, and
  `profiles-output.txt`: frozen outputs;
- `SHA256SUMS`: file-integrity ledger.

## Novelty and publication scope

Within this project this is a new, strictly stronger bounded
special-case theorem.  No external literature-priority search specific
to this exact support-\(18\) formulation is included here, so novelty in
the publication sense is **not established**.  The appropriate current
publication treatment is an incremental proposition in the existing
minimum-projection manuscript, subject to human review—not a standalone
FiveCDC resolution announcement.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, selected the finite
frontier, derived the reduction, wrote both programs and the prose, and
ran the checks.  The two programs are independently structured but were
produced in the same AI-assisted research process; this is not
independent human verification or peer review.
