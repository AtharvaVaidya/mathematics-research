# Research ledgers

Date frozen: 2026-07-29

## Statement ledger

- **Targeted theorem:** every flowable loopless two-occurrence
  interaction state of total support at most 18 has a clean or deleting
  nowhere-zero \(\mathbb F_2^2\)-flow.
- **Exact negation:** a loopless interaction multigraph \(J\), cyclic
  order at every vertex, and at most nine interaction edges, admitting a
  nowhere-zero \(\mathbb F_2^2\)-flow, such that no such flow is clean
  and no such flow makes a local integrated walk omit a colour.
- **Parallel edges:** allowed and distinctly labelled during the census.
- **Loops:** excluded.  They are not silently represented as ordinary
  edges.
- **“At most”:** support size is twice the number of interaction edges,
  hence even.  Elementary reductions plus the six triangle and seven
  four-vertex profiles cover every size through 18.
- **Variant:** standard FiveCDC route only.  No orientation variables or
  orientable conclusion occur.

## Experiment ledger

| experiment | method | exact result |
|---|---|---|
| four-vertex shape classification | all six-tuples summing to 9, all \(S_4\) relabellings | 90 labelled rows, 9 orbits; 1 disconnected, 1 bridged, 7 finite |
| primary census | C++17, alternating-form equations, all normalized flows and cyclic orders | 1,041,984 states; 0 residual |
| independent census | separate C++17 implementation, literal \(K_4\) endpoint masks | exact agreement on every frozen profile count; 0 residual |
| new support-18 layer | three triangle plus seven four-vertex profiles | 1,019,952 states: 1,013,220 clean, 6,732 delete-only |
| cumulative checked profiles | previous and new layers | 1,041,984 states: 1,035,036 clean, 6,948 delete-only |

No random sampling, floating-point arithmetic, SAT solver, or unrecorded
timeout is part of the theorem.

Frozen environment:

```text
Apple clang version 21.0.0 (clang-2100.1.1.101)
Target: arm64-apple-darwin25.5.0
Python 3.14.5
Darwin 25.5.0 arm64
```

## Obstruction ledger

- The profile \(T(4,4,1)\) has 6,624 rotation states with no clean flow,
  but each has a deleting flow.  Therefore the stronger universal
  direct-cleaning claim fails at the new layer.
- The profile \(Q(0,1,3,4,1,0)\) has 108 further delete-only states.
- These rows validate the necessity of the “clean **or delete**”
  dichotomy.  They are not obstructions to a globally minimum
  projection, because deletion strictly reduces its support.
- No clean-or-delete obstruction survives through support 18 in the
  loopless two-occurrence subclass.

## Proof-obligation ledger

Closed in this package:

- exact interaction-flow semantics in the two-occurrence loopless case;
- complete elementary shape reduction through support 18;
- exact four-vertex multiplicity-orbit list;
- exhaustive clean/delete classification by two implementations;
- strict-deletion implication for a cardinality-minimum projection.

Still open:

- extension to interaction loops, already open at support 16;
- extension to arbitrary complement-component occurrence counts, already
  open at support 16;
- any unbounded theorem controlling minimum projections;
- conversion of this bounded proposition into a FiveCDC resolution;
- independent human audit and external novelty/priority verification;
- proof-assistant formalization of the finite enumerators and reduction.

## Epistemic status

**VERIFIED FINITE CASE / PARTIAL STRUCTURAL PROGRESS.**

Not `RESOLVED—PROVED` and not `RESOLVED—DISPROVED`.
