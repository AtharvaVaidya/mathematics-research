# Exact retained cyclic-4 all-seven projection census through order 28

Date: 2026-07-28

Status: **FINITE NEGATIVE CENSUS / NEW EXACT INNER ALGORITHM / NOT A
FIVE-CDC RESOLUTION**.

## Target

For a connected cubic graph \(G\), a nowhere-zero
\(\mathbb F_2^3\)-flow is a three-dimensional binary cycle subspace
\(S\) whose seven nonzero vectors cover every edge. For a binary
projection \(h\), put \(F=E(G)-\operatorname{supp}h\). The exact
two-cycle cleaning condition asks for binary cycles \(p,q\) such that

\[
F\subseteq\operatorname{supp}p\cup\operatorname{supp}q
\]

and

\[
|\delta(W)\cap\operatorname{supp}p\cap\operatorname{supp}q|
\equiv0\pmod2
\]

for every component \(W\) of \(F\). The search asks whether all seven
nonzero members of some covering three-space are uncleanable.

## Linear inner decision

The previous exact classifier enumerated all unordered pairs \((p,q)\).
There is a much faster equivalent decision.

Fix \(h\) and the first cycle \(p\). Choose a binary cycle basis
\(b_1,\ldots,b_d\), and write

\[
q=\sum_{j=1}^d z_jb_j.
\]

Coverage forces \(q_e=1\) for each \(e\in F-\operatorname{supp}p\).
For each factor component \(W\), the defect condition is

\[
\sum_{e\in\delta(W)\cap\operatorname{supp}p}q_e=0.
\]

Both are linear equations in \(z_1,\ldots,z_d\). Thus, for each \(p\),
Gaussian elimination decides whether a suitable \(q\) exists. Exhausting
all \(p\) is exactly equivalent to exhausting all pairs; it is not a
relaxation.

The implementation is
`scratch/fano_all_bad_projection_search_linear.cpp`.

On the Petersen graph and both order-18 Blanuša snarks, the new
classifier exactly matches the older direct pair enumerator:

| order | direct bad count | linear bad count |
|---:|---:|---:|
| 10 | 7 | 7 |
| 18 | 5 | 5 |
| 18 | 9 | 9 |

The direct implementation is
`scratch/fano_all_bad_projection_search.cpp`.

## Results

The complete retained inputs from the focused cyclic-4 cap search gave:

| order | retained cyclic-4 non-Tait rows | cycle-space size | all-seven obstructions | largest individual bad set |
|---:|---:|---:|---:|---:|
| 26 | 1,297 | 16,384 | 0 | 207 |
| 28 | 12,517 | 32,768 | 0 | 570 |

The full per-row JSONL outputs are:

- `scratch/fano-all-seven-cyclic4-order26-results.jsonl`;
- `scratch/fano-all-seven-cyclic4-order28-results.jsonl`.

Run the frozen report checker:

```bash
python3 scratch/verify_fano_all_seven_cyclic4_results.py
```

To replay the semantic classification from source:

```bash
c++ -O3 -std=c++20 \
  scratch/fano_all_bad_projection_search_linear.cpp \
  -o /tmp/fano-linear

/tmp/fano-linear \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order26.g6

/tmp/fano-linear \
  search/focused-theta-choice-through28-20260727/artifacts/cyclic4-nontait-order28.g6
```

The order-28 replay was sharded only for wall-clock time. Every graph and
every projection was still decided exactly.

## Structural diagnostic

Representative closest covering three-spaces contain respectively
three, four, and five bad vectors at orders 26, 28, and 30. Simple
factor invariants do not explain the surviving clean vectors:

- bad factors can be forests or have positive cycle rank;
- clean factors can also be forests or have positive cycle rank;
- perfect-matching factors occur among bad projections but do not
  characterize them; and
- the bad cycles already span the full cycle space in representative
  order-28 and order-30 graphs.

Thus neither forestness, matchingness, nor binary rank supplies the
missing simultaneous-seven obstruction theorem.

These are retained generated sets, not a proof covering all cyclically
4-edge-connected cubic graphs. No FiveCDC conclusion follows from this
finite census.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the linear inner
algorithm, implemented it, ran and cross-checked the censuses, and drafted
this report. The proof of equivalence is displayed above and the frozen
outputs are independently replayable. This is not independent human peer
review.
