# Lift-13 full-lexicographic escape portfolio

Status: **COMPUTATIONAL EVIDENCE / PARTIAL STRUCTURAL PROGRESS**, checked
2026-07-29.

This package is a deterministic, exact sample of one auxiliary local
descent strategy related to the Five-Cycle Double Cover Conjecture. It is
not a proof of a universal escape theorem and is not a proof or disproof of
FiveCDC.

## Exact sampled result

The frozen trap-directed producer was run on the 130-vertex girth-10
13-lift of the Petersen graph using:

- seed 211, 500 steps, at roots
  `0,13,26,39,52,65,78,91,104,117`; and
- seed 307, 300 steps, at roots `0,39,91`.

The graph has exact oddness zero and is Tait-colourable.  This portfolio is
therefore a high-girth positive control, not evidence sampled from the
snark or minimal-counterexample domain.

Across the 13 runs:

```text
sampled state visits:                  5,900
sum of distinct states over runs:      5,891
old-objective local minima audited:      223
exact augmented traps:                   196
producer legal-neighbor evaluations: 2,420,070
```

For every one of the 196 augmented traps, the independent auditor:

1. reconstructs its rooted three-tree state;
2. recomputes all odd kernels, all seven profile entries, the full
   lexicographic objective
   `Psi=(minimum profile entry, total kernel size)`, and all 21 parallel
   span tests;
3. independently enumerates and byte-compares the complete first
   neighborhood to the producer row;
4. verifies that no first neighbor has a smaller full `Psi` or a successful
   span flag; and
5. searches the safe equal-`Psi` plateau through radius three.

All 196 sampled traps have **exact augmented escape distance 2**. No
radius-three counterexample was found.

The independent audit reconstructed 2,408,448 candidate swaps in the 196
seed neighborhoods, then examined 1,281 safe equal-plateau source states
before locating all escapes. In total it tested 18,149,376 candidate swaps
and evaluated 545,379 legal neighbor arcs. The hardest sampled trap was
root 65, seed 211, step 150, where 82 safe sources were processed before a
two-step escape was found.

This is finite sampled evidence only. The 5,891 distinct-state sum is not
the size of a union because runs can overlap, and the sample is not a
complete enumeration of the graph's state space. Therefore this package
does not prove that every trap escapes within radius two or three.

## Subsequent exact radius-two counterexample

The universal radius-two proposal is now known to be false. The separate
package
`../jaeger-order40-augmented-radius-two-counterexample-20260729/`
exhausts the first two layers around a cyclically four-edge-connected
order-40 state and finds no lower-`Psi` or successful state, followed by
an exact escape at distance three.

Its three exchanges are disjoint, with coordinate pairs `(01,01,02)`.
Thus the 196/196 result here must be read only as the deterministic sample
reported above, not as evidence elevated to a conjectural theorem.

## Frozen data

- `producer.cpp`: the exact C++ discovery program.
- `raw/*.jsonl`: all 13 raw deterministic producer outputs, including each
  augmented state and its complete first-neighbor table.
- `audit_radius3.py`: the independent standard-library Python auditor.
- `audits/*.jsonl`: the corresponding exact audit outputs and literal
  two-exchange escape paths.
- `verify.py`: fast aggregate/semantic checks, plus an optional full replay.
- `reproduce_search.py`: recompiles the producer and byte-replays all raw
  search outputs.
- `SUMMARY.json`: the exact aggregate counts and SHA-256 hashes.
- `SHA256SUMS`: package and external graph integrity manifest.

The auditor imports only the independently written state semantics from
the adjacent
`../jaeger-lift13-girth10-augmented-trap-20260729/independent_verify.py`.
It does not import discovery code.

## Verification

Fast frozen-output audit:

```bash
python3 verify.py
shasum -a 256 -c SHA256SUMS
```

Exact recomputation of every trap neighborhood and escape:

```bash
python3 verify.py --replay
```

This slow command launches one bounded-memory process per raw run,
sequentially. Each trap clears its state and neighbor caches before the
next trap.

Byte-replay the 13 deterministic discovery runs:

```bash
python3 reproduce_search.py
```

Search replay and audit replay are deliberately separate: the former
checks discovery reproducibility; the latter independently checks the
finite mathematical assertions about every sampled trap.

## Interpretation

The earlier exact witness package proves that the graph itself has a
standard FiveCDC. These traps therefore obstruct a particular naive
descent lemma, not the conjecture.

The portfolio records a full-lexicographic radius-two phenomenon on this
sample. The exact order-40 counterstate shows it does not extend to a
universal theorem.

## AI-use disclosure

The search design, code, computations, audits, and exposition were
produced by OpenAI Codex agents under human direction. Public use must
retain this disclosure and the explicit sampled-only limitation.
