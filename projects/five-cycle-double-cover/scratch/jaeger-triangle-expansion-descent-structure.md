# Triangle expansion: exact fibre product, non-invariant defect

Date: 2026-07-28

Status: **HUMAN EXCHANGE-GRAPH THEOREM / EXACT PROFILE COUNTEREXAMPLE TO
SCORE INVARIANCE / NOT A UNIVERSAL DESCENT PROOF**.

Let \(G^\triangle\) be obtained from a cubic graph \(G\) by replacing a
nonroot vertex \(v\) by a triangle and attaching the three former
incident edges to its three vertices.  Fix a different root \(r\), and
write \(\mathcal X(G,r)\) for the reciprocal-exchange graph of one
vertex-star fibre.

## The fibre graph is a Cartesian product

> **Theorem.**
> \[
> \mathcal X(G^\triangle,r)
> \cong
> \mathcal X(G,r)\mathbin{\square}
> \operatorname{Cay}(S_3,\{\text{three transpositions}\}).
> \]

Every triangle edge has multiplicity two, so the three trees together
use six triangle-edge copies.  A tree uses at most two edges of the
triangle.  Hence every tree uses exactly two, and the three omitted
triangle edges are distinct.  Contracting the triangle therefore sends
each tree to a spanning tree of \(G\), preserves every external
multiplicity, and gives a star-fibre state.  Conversely, a contracted
state and a bijection assigning the three triangle edges as the three
omitted edges reconstruct a unique lifted state.  This proves the
vertex-set bijection with
\(\mathcal X(G,r)\times S_3\).

There are three kinds of reciprocal swap:

1. If both swapped omitted edges are external, contraction turns it into
   exactly the same reciprocal swap in \(G\).  The changed lifted sets
   still use two triangle edges each, so they are trees exactly when
   their contractions are trees.
2. If both are triangle edges in two different omitted classes, the
   swap simply transposes those two omitted edges.  Both changed sets
   still contract to the old trees, so the swap is always legal.
3. If precisely one is a triangle edge, one changed tree acquires all
   three triangle edges and contains a cycle.  The swap is illegal.

These are precisely the Cartesian-product adjacencies.

## Why this does not prove descent invariance

External odd-kernel membership is preserved by contraction: expanding
one vertex changes the order of the side containing the triangle by
two.  Nevertheless the three new triangle edges can split or join the
zero-subgraph \(E_h\), so the seven-plane defect profile depends on the
\(S_3\) lift.

For the 14-vertex state in
`jaeger-star-parity-descent-countermodel.md`, expand vertex \(1\).  Its
contracted profile is
\[
                         (2,4,2,2,0,6,2).
\]
In omitted-triangle permutation order, the six lifted profiles are:

| permutation | profile | \(d_{\min}\) |
|---|---|---:|
| 012 | \((2,4,2,2,2,8,2)\) | 2 |
| 021 | \((2,4,2,2,0,8,2)\) | 0 |
| 102 | \((4,4,2,2,2,6,4)\) | 2 |
| 120 | \((2,4,2,2,0,8,2)\) | 0 |
| 201 | \((2,4,2,2,0,8,2)\) | 0 |
| 210 | \((2,4,2,2,0,6,4)\) | 0 |

Thus even \(d_{\min}=0\) is not preserved by choosing an arbitrary
lift.  The two positive lifts do have a triangle-only exchange to a
zero lift, but this is a feature of the displayed local table, not a
general invariance theorem.

The literal checker is

```sh
python3 scratch/verify_jaeger_triangle_expansion_descent_structure.py
```

It reconstructs all six tree triples, checks their star multiplicities,
contracts them back to the same three trees, and recomputes the six
profiles.

## Exact finite check on all thirteen expansions

Expanding each nonroot vertex of the same 14-vertex graph and keeping
root zero gives thirteen labelled order-16 fibres.  The whole-state C++
enumerator checks 1,330,560 states in each, 17,297,280 total.  Every
fibre has maximum \(d_{\min}=4\), and every positive same-level component
has a lower boundary.

The frozen rows are

```text
output/jaeger-fano-min-descent-triangle-expansions-16v/census.jsonl
```

and can be regenerated and audited with

```sh
python3 scratch/run_jaeger_triangle_expanded_fixedtrap_descent.py
python3 scratch/verify_jaeger_triangle_expanded_fixedtrap_descent.py
```

The second script independently regenerates the thirteen expansions,
checks simplicity, cubicity and 3-edge-connectivity, and audits row
coverage, totals and hashes.  It does not independently duplicate the
17,297,280-state enumeration.

## Remaining step

Triangle expansion preserves the exchange graph in the exact product
form above, but it decorates the six \(S_3\) sheets with different
defect values.  Therefore descent invariance would require a new local
six-sheet score theorem coupled to every contracted exchange.  Neither
the graph product alone nor preservation of external kernels supplies
that theorem.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the product
decomposition, computed and checked the explicit six-lift table, ran the
thirteen exact fibre enumerations, and drafted this note.  The universal
symmetric-descent lemma and FiveCDC remain unresolved.
