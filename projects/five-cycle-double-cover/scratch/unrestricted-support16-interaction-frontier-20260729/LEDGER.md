# Support-16 unrestricted interaction ledgers

Date: 2026-07-29

## Statement ledger

- **Requested universe:** every abstract support-16 boundary state,
  allowing interaction loops and complement components with more than two
  occurrences, after excluding the loopless two-occurrence theorem.
- **Completed universe:** every charge-valid partition of the single
  canonical `8+8` word orbit `01010123|01012302`.
- **Canonical state key:** `01010123|01012302|<restricted-growth partition>`.
- **Flowable:** charge validity supplies the displayed identity extension.
- **Clean:** some feasible component-map tuple and relative circuit
  translation has even component/colour boundary parity everywhere.
- **Strict-delete:** if no clean outcome exists, some feasible tuple has
  an integrated support circuit omitting a colour.
- **Residual:** neither direct outcome exists.  This does not assert global
  minimality or realizability.
- **Standard/orientable:** standard route only; orientation is absent.

## Experiment ledger

| experiment | exact result |
|---|---|
| canonical word orbit | 512 normalized images, trivial stabilizer |
| charge-valid partition recurrence | 8,046,330 |
| primary full map/translation census | 8,041,808 clean; 4,514 delete-only; 8 residual |
| loop-only category | 2,835 clean; 0 delete-only; 0 residual |
| higher-only category | 3,060,801 clean; 2,872 delete-only; 8 residual |
| loop-and-higher category | 4,978,172 clean; 1,642 delete-only; 0 residual |
| independent residual evaluator | every row 320 feasible, 0 clean, 0 delete |
| residual canonical SHA-256 | `3b0d26a74107e67b64878342cb9fb509bc1b8830d9da89a308fb5a1305274c0d` |

No random sampling, floating-point computation, solver, or unrecorded
timeout is part of the completed subcase.

## Obstruction ledger

- Exactly eight canonical direct residuals survive.
- All eight have five components and at least one higher-occurrence
  component.
- None has a size-two interaction loop.
- The four block profiles
  `8+2+2+2+2`, `6+4+2+2+2`, `6+3+3+2+2`, and `5+4+3+2+2`
  occur twice each.
- The existing `0123444444130244` obstruction is included.
- The lexicographically first residual is `0001234000314200`.
- The minimum possible largest block among these residuals is five,
  attained by the two `5+4+3+2+2` rows.

## Proof-obligation ledger

Closed:

- complete canonical partition generation for the fixed word orbit;
- exact charge-valid count by an independent recurrence;
- exhaustive component-map, circuit-closure, translation, clean, and
  deletion tests;
- independent literal replay and canonical audit of all residuals;
- interaction-loop and higher-occurrence classification;
- exact correspondence with the previously displayed obstruction.

Open:

- every other canonical word orbit of `8+8`;
- the other nine multi-circuit support shapes;
- graph realizability of the seven new residuals;
- global minimum or realization-robust Kempe analysis for any new row;
- a universal clean/delete/Kempe theorem at support 16;
- formal proof-assistant verification and independent human review.

## Epistemic status

**VERIFIED FINITE SUBCASE / PARTIAL STRUCTURAL PROGRESS.**

Not `RESOLVED—PROVED` and not `RESOLVED—DISPROVED`.
