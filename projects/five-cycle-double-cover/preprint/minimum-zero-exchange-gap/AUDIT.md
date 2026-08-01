# Independent audit record

Date: 2026-07-28

Classification: **proof strategy countermodel, not a FiveCDC
counterexample**.

## Result of the audit

No mathematical gap was found in the two-edge-sum factorization argument.
The exact finite base package replayed successfully, including both LRAT
proofs under both retained checkers. The positive witnesses were also
checked by a separately written implementation, and their gluing was
checked for all 195 possible root edges.

This audit does not establish publication priority and is not a substitute
for human peer review.

## Algebra checked

For a two-edge sum with cut `{f,g}`, summing an `F_2^2` flow over either
shore gives `phi(f) + phi(g) = 0`, hence `phi(f) = phi(g)`. Restoring the
deleted root edge with this value gives a factor flow.

The zero count is exactly additive in both cases:

- common cut value nonzero: neither the two cut edges nor the two restored
  roots contribute zeros;
- common cut value zero: the two zero cut edges are replaced by one zero
  root in each factor.

If the sum zero set is a matching, the restored factor zero sets are
matchings. In the only nontrivial case, the zero cut edges already forbid
any other zero at the four root endpoints.

For either binary cycle, cut parity forces use of both cut edges or
neither. Restoring the common membership bit gives a binary cycle in each
factor. Therefore a certificate restricts factorwise and its matching
size is additive.

For identical rooted copies, identical minimum objects have identical
root states. They glue without a compatibility assumption. This proves
all three exact doubling formulas. The draft correctly limits general,
nonidentical sums to additive lower bounds unless compatible minimum root
states exist.

## Graph reconstruction checked

The two-edge sum preserves:

- cubicity, because each root endpoint loses and gains one incident edge;
- simplicity, because new edges join different factor copies;
- connectedness;
- bridgelessness, because every old edge and both new edges can be placed
  on an explicit cycle.

The order and size formulas are exact: no vertices are added or removed,
two factor edges are deleted, and two cut edges are added.

## Base certificate replay

The following command passed:

```sh
cd search/minimum-zero-exchange-countermodel-130v-20260727
shasum -a 256 -c SHA256SUMS
python3 verify.py
```

It reported a simple connected bridgeless cubic graph on 130 vertices and
195 edges, with:

```text
r_f = 5
r_M = 5
eta = 6
five-CDC = PASS
```

Both `flow-at-most-four-zero.lrat` and
`extension-at-most-five.lrat` were accepted by `lrat-check` and CakeML
`cake_lpr`.

The encoding was inspected:

- the flow instance has two flow bits per edge, an exact zero indicator,
  both vertex XOR equations, and an at-most-four sequential counter;
- the extension instance has `m`, two cycle bits, and two flow bits per
  edge; it enforces `m iff (a and b)`, `m iff flow is zero`, matching
  clauses, four vertex XOR equations, and an at-most-five counter;
- the truth-table parity clauses exclude exactly the odd assignments;
- the forward sequential-counter clauses enforce the stated upper bound
  and admit every assignment within the bound.

Thus the UNSAT statements match the mathematical lower bounds claimed in
the paper.

## Independent positive audit

The command

```sh
python3 preprint/minimum-zero-exchange-gap/audit_two_sum.py
```

checks the base edge list and positive witnesses without importing the
base verifier. It then constructs the two-copy sum at every root edge and
checks:

- graph simplicity, cubicity, connectedness, and bridgelessness;
- a glued matching-supported flow with exactly 10 zeros;
- a glued matching/four-flow certificate of size 12;
- a glued standard five-CDC.

## Remaining trust and publication boundaries

- The lower bounds are certificate-checked computations, not handwritten
  enumerations.
- This audit used AI agents and must not be described as independent
  human peer review.
- The draft now gives a documented related-work comparison, but priority
  and novelty have not been established by a domain specialist.
- The construction has low cyclic edge-connectivity and does not settle a
  reduced-domain minimum-zero strategy.
- The Five-Cycle Double Cover Conjecture remains unresolved by this work.
