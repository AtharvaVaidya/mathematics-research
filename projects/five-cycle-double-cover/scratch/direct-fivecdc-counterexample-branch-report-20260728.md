# Direct FiveCDC counterexample branch: exact report

Date: 2026-07-28

Conclusion: **no FiveCDC counterexample was found**.  Two sound positive
reductions were proved and independently audited.  FiveCDC remains
unresolved.

## Exact target encoding

For every edge \(e\) and coordinate \(i\in\{0,1,2,3,4\}\), the direct solver
uses the base variable
\[
 x_{e,i}=5e+i+1.
\]
For each edge it emits the ten negative three-clauses and five positive
four-clauses that are equivalent to \(\sum_i x_{e,i}=2\).  For every vertex
and coordinate, its three incident variables are folded through two
left-associated XOR gates, each represented by the standard four-clause
equivalence, and the final accumulator is forced false.  No S5 symmetry
units are used.

For a cubic graph of order \(n\), this is \(17.5n\) variables and \(67.5n\)
clauses.  It is the ordinary-CNF version of the mandated exact-two/XOR
formula.  The C++ harness uses CaDiCaL 3.0.1.  Before printing SAT, it
independently checks the five-bit model against the original, non-CNF
semantics: every edge mask has weight two and every vertex-coordinate XOR is
zero.  It also recomputes connectivity and bridges from graph6.

An UNSAT return would be printed only as `UNSAT_UNCERTIFIED` and would trigger
a fresh frozen CNF, LRAT production, and independent proof checking.  No
UNSAT return occurred, so no proof trace was relevant.

## Direct exact runs

| family | order | graphs | result | independent replay |
|---|---:|---:|---|---|
| canonical retained strong snarks | 40 | 7,654 | all SAT | all graph premises and covers PASS |
| deterministic connected 2-lifts | 80 | 7,654 | all SAT | all lifts reconstructed; pullback covers PASS |
| second connected 2-lift layer | 160 | 7,654 | all SAT | all lifts reconstructed; pullback covers PASS |
| Petersen four-pole substitutions | 48 | 7,654 | all SAT | all operations, premises, and covers PASS |
| second Petersen substitution layer | 56 | 7,654 | all SAT | all operations, premises, and covers PASS |
| third Petersen substitution layer | 64 | 7,654 | all SAT | all operations, premises, and covers PASS |

The order-80 outputs are 7,654 pairwise nonisomorphic graphs under nauty
canonical labeling.  The order-48 outputs are likewise 7,654 pairwise
nonisomorphic graphs.  No uniqueness claim is made for the later layers.

The lift layers are only encoder controls, because the covering pullback
theorem below makes them positive once their bases are positive.  The
Petersen-substitution layers were initially a genuine non-covering search;
the exact four-pole theorem below subsequently explains all of them.

The large graph6/model JSONL streams remain under
`scratch/output/direct-fivecdc-20260728/` and are intentionally excluded from
the curated publication bundle.  Their exact SHA-256 values are:

| stream | SHA-256 |
|---|---|
| order-40 results | `1f91f1910f5920f9da5a1c874ab302f2cb3026f6d8355fd8aee24aa83fc43f1d` |
| order-80 graphs | `5e8af84be5125572d746e676595f7ff7ff43592cba01fee020e1ce6433a78987` |
| order-80 source | `59de869b53283f2b3b60df0a21ce95087a97ee81b9f2c3158b12294f7b527a54` |
| order-80 results | `af55c08ad7c67c2461b2a96f6a5c77a86e30ce85aa82547e97d48b6f4d4bad85` |
| order-160 graphs | `2c1249616821ab9c0d4603d32df6d574a2960dd502d3e9045191d6fd6bd31841` |
| order-160 source | `1bcea8bcd10708b19bdb3c8b22b54161b317beea89d4ef51361c351f83f31b99` |
| order-160 results | `7d2e95a9a21362ea99c62f053c1688d08613c7880c5e54bde63b46e7c7d52b9d` |
| order-48 graphs | `783ae8c506601379f6feba796327de789fbdd9e8f75418bab9aa019ec44e47d6` |
| order-48 source | `e13a52cfc6fcaf37706de6a5524892ba762e4cb68311a69ccf4e4ece63960648` |
| order-48 results | `e745d17cf6108f03aced571a69ba5d5143efe0b0708532a6648077a763144e66` |
| order-56 graphs | `76631b300f56c90310d4f59276bb5f7549d67e4aa5dc7da952870dbac99dc7cb` |
| order-56 source | `bc70e3c5446d9bccdf62234e912854e65b696569255216b967db27cf1a9d43c8` |
| order-56 results | `9ed584ba34dfa5d87a76ac4e291fbfd46bc659130616385003fae25f805a1a0d` |
| order-64 graphs | `dd22fd4cb68d1f7c5e9046a8242c82217ac2bb8858d6d035773d997af1dc0a0f` |
| order-64 source | `ec978f83fbc27729c5d31c2287f323138e33b9701733901fdfa0bcff4a00b21d` |
| order-64 results | `239212f59b4f96b453b17821c746956c0353aed9bcfb28779ab032d268c935bd` |

## Reduction 1: pullback through graph coverings

If \(p:\widetilde G\to G\) is a finite graph covering and
\((C_1,\ldots,C_5)\) is a standard FiveCDC of \(G\), then
\[
 \widetilde C_i=p_E^{-1}(C_i)
\]
is a FiveCDC of \(\widetilde G\).  The local bijection on incidences preserves
the degree of every coordinate at every lifted vertex, including the
two-incidence convention for loops.  Every lifted edge inherits exactly the
two coordinates of its image.

The complete human proof, including parallel-edge and loop conventions, is
in `scratch/fivecdc-cover-pullback-reduction-20260728.md`.

## Reduction 2: exact Petersen four-pole substitution

Let \(G\) be a cubic graph with a FiveCDC.  Choose independent edges
\[
 e=\{a,b\},\qquad f=\{c,d\}.
\]
Delete \(e,f\).  In the Petersen graph with graph6 encoding `ICOf@pSb?`,
delete adjacent vertices \(0,3\).  Its four boundary vertices, in the frozen
order, are
\[
 (6,9,7,8).
\]
Join \((a,b,c,d)\) bijectively to those four ports in any order.  The theorem
states that every such resulting cubic graph has a FiveCDC.

To see the exact boundary requirement, let \(q,r\) be the two-coordinate
labels of \(e,f\).  Keep every unaffected label and put \(q,q,r,r\) on the
four new joining edges at their old endpoints.  Old-vertex parity is
unchanged.  The Petersen pole must extend an arbitrary placement of
\(q,q,r,r\).

The ten frozen internal edges are
\[
 (1,4),(1,6),(1,8),(2,5),(2,6),
 (2,7),(4,7),(4,9),(5,8),(5,9).
\]
Under S5, ordered pairs \(q,r\) have three types: equal, intersecting in one
coordinate, or disjoint.  The human note gives a 13-row table: one row for
the equal type and six port placements for each of the other two types.
Every row assigns weight-two labels to the ten internal edges and has XOR
zero at all eight internal vertices.

The independent checker verifies the displayed 13 rows and exhausts:

- all 100 ordered choices of \(q,r\);
- all 550 distinct labeled boundary placements;
- all 120 coordinate permutations; and
- every internal weight and parity condition.

It returns `all_boundary_assignments_extend: true`.

The full statement, attachment conventions, table, and human proof are in
`scratch/fivecdc-petersen-four-pole-extension-theorem-20260728.md`.

## Exact consequence and limits

A smallest counterexample cannot be:

1. a nontrivial cover of a smaller FiveCDC-positive quotient; or
2. obtained from a smaller FiveCDC-positive cubic graph by the specified
   Petersen four-pole replacement of two independent edges.

These are valid pruning reductions, not a proof of FiveCDC.  They concern
the standard Eulerian-subgraph conjecture only; orientability is not asserted.
The Petersen table and pullback observation are elementary enough for direct
human checking, but no literature-novelty claim should be made without
specialist comparison.

## Curated files

The recommended compact package is:

- the two human notes;
- the exact local checker;
- the direct solver and the two independently written semantic/reconstruction
  checkers;
- the two deterministic generators;
- the seven compact JSON audit summaries; and
- `scratch/direct-fivecdc-curated-SHA256SUMS-20260728.txt`.

Do not include the large redundant graph/model streams in a manuscript or
preprint archive.
