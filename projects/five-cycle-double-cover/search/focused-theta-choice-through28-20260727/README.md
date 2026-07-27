# Focused prescribed-root theta census through order 28

Status: **finite two-implementation theorem; no universal claim**.

This package classifies every independent edge pair \(R\) in every
retained cyclically 4-edge-connected non-Tait simple cubic graph of every
even order from 10 through 28.  Put \(U=V(R)\) and \(H=G-U\).

For all 10,689,351 pairs, exactly one of the following verified positive
outcomes occurs:

1. \(H\) has a perfect matching; or
2. \(H\) has deficiency two and some maximum near-perfect matching \(P\)
   makes \(G-(R\cup P)\) bridgeless.

The second complement suppresses to a theta, so it carries a nowhere-zero
\(\mathbb F_2^2\)-flow.  No root pair for which every maximum matching
gives a loop--link--loop dumbbell was found.

The complete count is:

| graphs | root pairs | perfect | deficiency-two theta | all dumbbell |
|---:|---:|---:|---:|---:|
| 14,009 | 10,689,351 | 10,567,773 | 121,578 | 0 |

Every deficient instance has \(|\delta(U)|=8\); none has boundary six.
This is a bounded observation, not a universal lemma.

`verify.py` checks the ten source hashes and generator logs, the
independent-pair arithmetic, both result streams, and every aggregate.
The classifiers are separately written C++ and Python implementations;
the Python replay does not execute or import the C++ program.

Canonical source completeness and the meanings of the Snarkhunter
options are inherited from the documented Snarkhunter 2.0b runs.  The
package does not provide a second canonical graph generator.

This result does **not** prove the focused assertion at arbitrary order
and does **not** resolve the Five-Cycle Double Cover Conjecture.

## AI-use disclosure

OpenAI Codex, under human direction, developed the matching
classification, wrote both implementations and this package, ran the
finite computations, and audited the results.  The mathematical
deficiency and theta-core lemmas are written out in
`../../scratch/prescribed-root-matching-deficiency-frontier.md`.
Every finite count is reproducible.  No AI-generated inference is
presented as a universal theorem.
