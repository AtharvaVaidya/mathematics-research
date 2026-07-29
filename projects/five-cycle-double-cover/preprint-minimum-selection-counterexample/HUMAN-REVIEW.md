# Human review guide

The preprint is intentionally split into elementary reductions and
finite claims. A human referee can review it in the following order.

## 1. Definitions and master lemma

- Confirm that an extendable projection is the support of one coordinate
  of a nowhere-zero \(\mathbb F_2^3\)-flow.
- Check the bijection
  \[
  (s',M=Z(s'),J),\quad J\cap M=\varnothing,\quad
  \partial J=\partial M
  \longleftrightarrow
  (M\dot\cup J,s').
  \]
- Check that cleanliness is equivalent to a second
  \(\partial M\)-join in the projection complement.

These steps are human proofs and do not depend on enumeration.

## 2. Base and closure enumeration

Replay:

```sh
python3 ../scratch/minimum-projection-strict-parity-lock-20260729/verify.py
python3 ../scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/verify.py
python3 ../scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/independent_audit.py
```

Confirm:

- base cycle-space size 1,024;
- 15,360 extensions of the displayed base support and zero clean ones;
- closure conditional minima \((a_0,a_1)=(7,5)\);
- unique \(a_1\)-minimum support \(\{5,13,14,16,17\}\).

The independent checker uses incidence-matrix elimination and Tarjan
bridges, unlike the primary checker.

## 3. Weighted global-minimum proof

- Verify \(w_0=a_0=7\) and \(w_1=a_1-1+2=6\).
- Derive
  \[
  \Delta_L(H)=2|(T-H)\cap L|-|T-H|+|H-T|.
  \]
- Replay the all-\(2^{14}\) lock audit: minimum lock size 8, 180
  minimum placements, chosen strict gap 1.
- Check that equality forces both the base terminal support and every
  local pole support, hence the literal 54-edge projection is unique.

## 4. Uncleanability

Check that the 54-edge projection complement has the five old base
components plus eight pole interiors. Under pole contraction, the
cut-colour parity on every old component is unchanged. Therefore a clean
extension upstairs would contradict the exhaustive base obstruction.

## 5. Positive FiveCDC control

- Check each base and closure pair-label row printed in the paper.
- Verify that permuting the five indices to match a replaced edge label,
  then gluing two equally labelled terminal links, preserves all vertex
  parities.
- Check the separate literal assignment against
  \[
  \sum_i x_{e,i}=2,\qquad
  \sum_{e\ni v}x_{e,i}=0\pmod2.
  \]

This is a SAT certificate. There is no UNSAT or FiveCDC-disproof claim.

## 6. Publication gate

Before dissemination, a human specialist should:

- compare the selection statement with Hušek--Šámal and earlier
  Fano-flow/join formulations;
- audit at least one checker line by line;
- reproduce the canonical graph and both five-cover certificates;
- confirm the scope language never implies a FiveCDC resolution;
- approve the explicit AI-use statement.
