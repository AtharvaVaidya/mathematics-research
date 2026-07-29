# A unique globally minimum projection which is not cleanable

Date: 2026-07-29

Status: **EXACT PROOF-METHOD COUNTEREXAMPLE / HAS A FIVE-CYCLE DOUBLE
COVER / NOT A FIVECDC COUNTEREXAMPLE**.

This package constructs a simple connected bridgeless cubic graph
\(G\) with
\[
                         |V(G)|=162,\qquad |E(G)|=243
\]
whose unique cardinality-minimum extendable binary projection has size
54 and has no clean extension.

The construction uses an order-18 strict parity-lock closure with
canonical graph6 string
```text
Q???C@?K?WEOM?_aGo?I__W@G_?
```
and distinguished edge 5.  Exact cycle-space enumeration gives
\[
                         a_0(5)=7,\qquad a_1(5)=5.
\]
Deleting the distinguished edge and inserting the resulting two-pole
therefore has effective projection costs
\[
                         w_0=7,\qquad w_1=6.
\]

An exact search of all \(2^{14}\) lock placements on the audited
18-vertex base proves that eight locks are necessary and sufficient for
the target to become uniquely minimum.  There are 180 minimum
placements.  The frozen graph uses
```text
L = {0,2,3,4,7,8,9,10}.
```

This graph is not a FiveCDC counterexample.  The package contains two
literal five-class certificates:

- a compositional certificate obtained by gluing five-cycle double
  covers of the base and closure; and
- a separately generated direct SAT/PB witness for the mandatory
  variables \(x[e,i]\), with exactly two true variables per edge and
  even incidence parity at every vertex and index.

The first exploratory Z3 query incorrectly called the binary Python API
`Xor(*three_arguments)`, causing its third Boolean to be interpreted as
a context argument.  That result was discarded.  The frozen direct
witness comes only from the corrected nested three-way XOR encoding and
is independently checked without Z3.

Files:

- `HUMAN-PROOF.md`: complete construction and proof;
- `verify.py`: self-contained exact checker;
- `graph-edges.tsv`: the labelled 243-edge order;
- `canonical.g6` and `canonical.s6`: canonical graph6 and sparse6 graph
  encodings;
- `fivecdc-certificates.txt`: component, compositional, and direct
  certificates;
- `verification-output.txt`: frozen replay output; and
- `SHA256SUMS`: artifact ledger.

Replay from the repository root:

```sh
python3 projects/five-cycle-double-cover/scratch/minimum-projection-strict-parity-lock-20260729/verify.py
shasum -a 256 -c projects/five-cycle-double-cover/scratch/minimum-projection-strict-parity-lock-20260729/SHA256SUMS
```

Canonical sparse6 verification uses Brendan McKay's `labelg`.

OpenAI Codex agents under Atharva Vaidya's direction found the lock,
performed the exact searches, wrote the proof and checkers, and
generated the certificates.  Separate agent audits are computational
cross-checks, not independent human peer review.  No literature-wide
novelty or priority claim is made.
