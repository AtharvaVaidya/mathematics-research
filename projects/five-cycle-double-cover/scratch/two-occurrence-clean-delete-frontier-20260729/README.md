# Loopless two-occurrence clean-or-delete frontier

Date: 2026-07-29

Status: **VERIFIED SPECIAL CASE / PROVISIONAL AI-ASSISTED RESEARCH
ARTIFACT / NOT A FIVECDC RESOLUTION**.

This package proves that every loopless two-occurrence interaction state
of total support at most \(16\) has a clean flow or a strict
support-circuit deletion.  Hence every globally cardinality-minimum
extendable projection in this subclass is clean.

The human reduction in `HUMAN-PROOF.md` leaves only the three
three-vertex interaction profiles

```text
edge multiplicities  degrees
3,2,2                5,5,4
3,3,2                6,5,5
4,3,1                7,5,4
```

The primary and independently structured exact checkers exhaust every
cyclic order and every nowhere-zero \(\mathbb F_2^2\)-flow.  Across
22,032 rotation states they find no state lacking both alternatives.

Replay from the repository root:

```sh
python3 scratch/two-occurrence-clean-delete-frontier-20260729/search_three_vertex.py --multiplicities 3,2,2
python3 scratch/two-occurrence-clean-delete-frontier-20260729/search_three_vertex.py --multiplicities 3,3,2
python3 scratch/two-occurrence-clean-delete-frontier-20260729/search_three_vertex.py --multiplicities 4,3,1
python3 scratch/two-occurrence-clean-delete-frontier-20260729/independent_audit.py
shasum -a 256 -c scratch/two-occurrence-clean-delete-frontier-20260729/SHA256SUMS
```

`search_two_vertex.py` is an additional exact regression through ten
parallel edges.  The human proof handles every number of parallel edges,
so this search is not part of the theorem's trust base.

The theorem assumes that the interaction multigraph has no loops.  It
does not settle the unrestricted size-\(16\) minimum-projection case, and
it does not resolve FiveCDC.

OpenAI Codex agents under Atharva Vaidya's direction developed the result,
code, audits, and prose.  Agent cross-checks are not independent human
verification or peer review.
