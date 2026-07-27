# Exact some-good-line projection census

This package searches the surviving algebraic branch of the Fano-flow
approach.  It does **not** claim a proof of five-CDC.

For a connected cubic graph, a nowhere-zero
\(\mathbb F_2^3\)-flow is a three-dimensional binary cycle subspace
\(S\) whose supports cover every edge.  Its seven nonzero functional
projections are exactly \(S-\{0\}\).  For each binary cycle \(h\), the
checker directly enumerates binary-cycle pairs \(p,q\) and tests
\[
E-\operatorname{supp}h\subseteq
\operatorname{supp}p\cup\operatorname{supp}q
\]
and
\[
|\delta(W)\cap\operatorname{supp}p\cap\operatorname{supp}q|
\equiv0\pmod2
\]
for every component \(W\) of
\(E-\operatorname{supp}h\).  It then searches the bad projections for
all seven nonzero members of a covering three-space.

No such obstruction occurs in:

- every connected simple bridgeless cubic graph through order 18;
- the retained 6, 20, and 38 strict snarks of orders 20, 22, and 24;
- the retained ten cyclically-5-connected order-26 snarks.

The complete order-18 boundary contains 39,866 bridgeless isomorphism
classes.  Exact profile counts are in `SUMMARY.json`.

The C++ checker is
`../../scratch/fano_all_bad_projection_search.cpp`.  An independently
written Python checker,
`../../scratch/search_fano_all_bad_projection_subspaces.py`, completely
replays through order 16 and separately matches representatives of
every order-18 non-Tait profile.

The Tait shortcut is a proved theorem, not a heuristic: a fixed
nowhere-zero \(\mathbb F_2^2\)-flow cleans every binary projection.
Therefore only non-Tait graphs need the expensive projection-pair
enumeration.

The repeated bad-count doubling on the Petersen/Tietze expansion chain
is also proved rather than extrapolated.  The local \(D_5\) argument in
`../../docs/fano-triangle-expansion-invariance.md` proves that
cleanability is invariant under vertex-to-triangle expansion and that
such an expansion cannot create the first all-seven obstruction.

Representative reproduction:

```sh
c++ -O3 -std=c++20 \
  ../../scratch/fano_all_bad_projection_search.cpp \
  -o /tmp/fano-all-bad

geng -cq -d3 -D3 18 | /tmp/fano-all-bad /dev/stdin

/tmp/fano-all-bad \
  ../order22-filter-census-20260725/strict-snarks-order20.g6 \
  ../order22-filter-census-20260725/strict-snarks-order22.g6 \
  ../fano-flow-one-switch-frontier-20260726/strict-snarks-order24.g6
```

Generation used nauty 2.9.3.  AI use was substantive: OpenAI Codex
agents derived the projection-space reduction and Tait shortcut, wrote
both exact checkers, ran the censuses, and drafted this report under
human direction.  No human peer review is claimed.
