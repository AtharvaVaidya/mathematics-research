# Experiment ledger

## Girth-ten/oddness-eight candidate-domain specimen

Status: **VERIFIED FINITE CASE / POSITIVE FRONTIER SPECIMEN**.

The deterministic run
`search/candidate_domain/runs/domain-20260725-v1/` contains one graph with
30,450 vertices and 45,675 edges.  Independent graph algorithms and both
premise parsers find it simple, connected, cubic, and bridgeless.  Exact BFS
gives girth 10.

The base resistance certificate proves \(\rho(R_4)=7\): the at-most-six
deletion formula is UNSAT with an LRAT accepted by `lrat-check` and
`cake_lpr`, while a directly checked seven-deletion model supplies the
matching upper bound.  Properness of the exact implemented \(F_{10}\)
six-pole is certified separately:

```text
improper-colouring CNF  1,305 variables, 4,344 clauses
CNF SHA-256             c5bc0eae7fe58090562f5c5fa8f440553460ddf543e04bf5b023e4d0f79dda18
LRAT bytes              831,347,425
LRAT SHA-256            1b02ae63f650386e27568e109ee8d4c656e2bcfa6ccec964f9cfad8954ef4814
```

Both external proof checkers accepted that LRAT in fresh runs.  The blind
auditor reconstructed the 4,344 clauses from the raw retained graph and
matched them in order and multiplicity.  Applying the sourced proper
superposition theorem gives resistance at least 7 and hence even oddness at
least 8.

The graph is SAT for the standard five-coordinate target.  The authoritative
v4 witness was assembled from a five-cover of \(R_4\) and ten equal-boundary
\(F_{10}\) templates.  Its retained hashes are:

```text
Verifier-B assignment  c1a721f5a560866f1189591425e6b24e9a12eb73fa86b6a9e3103046b2ea3ff4
JSON labels            be31250209e2e0a2a6d8fc692315502334ba5b41a5bb83a6ebbe853ec613d5dd
DIMACS model           308d14967a103f17f39209de661b7a592e7ffe2c1566132842b98bb52c35ea7a
```

The three formats agree exactly.  Direct original semantics, a fresh
Verifier B run, and the blind auditor all accept the witness.  Complete
unconditioned native-XOR, Verifier-A-CNF, and Verifier-B-CNF source instances
are retained.  Fixed-primary-unit solver checks establish that this known
witness extends to each complete encoding; those checks are not
unconditioned monolithic solve timings.

For this particular cover, the five coordinate-complement component counts
are 4,275, 4,390, 3,295, 4,602, and 4,311.  It therefore does not directly
witness the stronger connected-kernel property.  This is a property of the
retained cover, not a proof that the graph has no other cover or flow with a
connected kernel.

## Reconstructed high-flow-resistance \(H_2\)

Status: **VERIFIED FINITE CASE / POSITIVE TARGET WITNESS**.

The order-82 graph \(H_2\) from Mattiolo--Negrini--Pagani
(arXiv:2604.22501v1) was reconstructed from the author vector figures and
the labelled recursive boundary.  The source archive has no machine-readable
author edge list, so the package claims exact figure-based reconstruction,
not a canonical comparison with an author-supplied graph file.

The inferred boundary map and all four repaired figure edges are frozen.
Independent checks find a simple connected cubic graph with 123 edges,
girth five, and no cyclic edge cut of size at most four; the latter exhausts
9,388,877 deletion sets.  A retained \(\mathbb F_2^2\)-flow has exact zero
set \(\{34,122\}\).  The at-most-one-zero formula has 246 variables and
8,159 clauses and is UNSAT; its LRAT is accepted by a separately built
checker.  Together these prove flow resistance exactly two.

This extreme pair is nevertheless positive for both follow-up tests.  A
23-edge binary cycle contains both zero edges and has a connected 100-edge
complement, so \(\mu(\{34,122\})=1\).  The complete standard five-CDC CNF is
SAT with coordinate sizes \(47,62,39,44,54\); direct semantics and both
frozen project verifiers accept the cover.  The deterministic reconstruction
ledger hash is
`4babacb2794429d0eb74f5e8ee54a911ff21116d97b7c820a1bf9dd1a98f2870`;
the independent audit ledger hash is
`b7a8924312867cbf2292491b5581e2791eddb61e40c69607eae73e74fa2db652`.
Thus this high-resistance family member is eliminated as a counterexample;
no universal conclusion follows.

## Connected-kernel census and switch audit

Status: **VERIFIED FINITE CASES FOR A SUFFICIENT CONDITION / PARTIAL
STRUCTURAL PROGRESS**.

The connected-kernel condition asks for a nowhere-zero
\(\mathbb F_2^3\)-flow whose edges in some Fano line induce a connected
spanning join.  It constructively implies a five-cover, but may be stronger
than the target conjecture.

Canonical `geng` runs found and lifted such a flow on every connected simple
bridgeless cubic class through order 18:

| range | generated | bridgeless | lifted |
|---:|---:|---:|---:|
| 4--14 | 621 | 587 | 587 |
| 16 | 4,060 | 3,874 | 3,874 |
| 18 | 41,301 | 39,866 | 39,866 |
| **total** | **45,982** | **44,327** | **44,327** |

For order 18, the summary, result stream, and manifest hashes are,
respectively:

```text
3fe7c917d4d7fbf5df23b53dc539b5b98cc9f35337519a0477f0e5478985f415
a7288aab34f632f281f1bd7dbb46d280b15763093cbd9e0e15ddbc2c47207cc8
15e2a8e7ac14456abb274589d60c6678f2281ec705fe4cb041b05422a0302f3f
```

The exact flow-switch audit enumerated 556,248 nowhere-zero flows on all 26
bridgeless canonical graphs through order 10.  It classified 446,040 as
already liftable, 109,872 at elementary-switch distance one, 336 at distance
two, and zero unresolved.  Across 3,681,048 disconnected flow-line pairs,
zero were stable against every component-decreasing elementary switch.  The
retained summary SHA-256 is
`310149c88ef91ab40b22891e06676687c4a51a4eeb407c07f04643ff283764d5`.

The arbitrary-binary-cycle continuation found the first immediate
constant-value trap at order 12, graph6 `K?ABAfCi?wF?`.  Four disjoint
two-edge outside color classes hit all nine component-reducing cycles.  A
two-step mixed escape—line value 1 on circuit mask 2998, then outside value
4 on circuit mask 67293—connects the join.  The complete order-12
fixed-join census checked 85 canonical graphs, 81 bridgeless graphs, and
9,132 realizable disconnected joins.  Every one has some low-coordinate
recoloring followed by a reducing outside switch; there are zero
existential fixed-join traps.  The report SHA-256 is
`36b29a079d544e2b6d8b057d374e84ca27cdcd913f4df2b22aea32a74bb6e4a9`.

The attempted connected-kernel solve on the order-30,450 candidate was
manually interrupted during its first SAT call and has no result.  Its
partial CNF is not counted as either SAT or UNSAT.

### Current hard-snark data portfolio

Nineteen graph6 source files were downloaded from the House of Graphs snark
meta-directory and retained byte-for-byte.  They contain 1,085 raw records
and 1,082 unique graphs:

| source-list class | records |
|---|---:|
| cyclic connectivity at least 5, through order 30 | 600 |
| girth at least 6, selected available orders through 40 | 318 |
| circular flow number 5, through order 36 | 136 |
| exact order-44 oddness-4 list | 31 |

The counts overlap.  Every unique graph independently passed
simple/cubic/connected/bridgeless checks.  Every one admitted a
connected-kernel flow and direct \(D_5\) lift; there were zero solver limits
and zero stronger-property UNSAT rows.  The authoritative run is
`search/known-snark-kernel-portfolio-v2-20260725/`.

The source-list names are provenance rather than recomputed invariants:
cyclic connectivity, girth, circular flow number, and oddness were not
independently recomputed for all 1,082 records.  The graph premises and every
retained flow and pair-label witness are independently checkable.

### Strong-snark portfolio through order 40

The four retained House of Graphs lists in the strong-snark,
girth-at-least-five table column contain 7,984 records:

| order | source records | connected-kernel lifts |
|---:|---:|---:|
| 34 | 7 | 7 |
| 36 | 25 | 25 |
| 38 | 298 | 298 |
| 40 | 7,654 | 7,654 |

Every record passed direct simple/cubic/connected/bridgeless checks and
every returned \(\mathbb F_2^3\) flow and \(D_5\) lift passed the original
parity semantics.  There were zero iteration limits and zero
stronger-property UNSAT rows.  The separate blind audit passed all 7,984
rows and found 7,984 nauty isomorphism classes.  Strongness and girth remain
source-list provenance rather than recomputed properties.  The result-stream
SHA-256 is
`764d1a625b47d751351c997872164d91ab0ef4c5ab3980a2411ff66d392096cc`;
the blind result SHA-256 is
`94bd885cf9f9f87c637629575d1b49fe8b84d944202a8161cbf6482439639d91`.

### Exact fixed-join preparation code

For \(J=E-H\), arbitrary low-coordinate recoloring and normalization of the
outside value reduce preparation to an exact common-zero-set problem:

\[
 T=E-(p\cup q)\subseteq H,\qquad
 \mu_G(T)=\min_{H'\supseteq T}\kappa(E-H').
\]

A realizable disconnected join is preparable iff some relevant
inclusion-minimal \(T\) has \(\mu_G(T)<\kappa(J)\).  The canonical primary
census found zero traps through order 18.  At order 18, 179 non-three-edge-
colourable bridgeless classes supplied 173,316 realizable disconnected hard
joins, all preparable.  An independently written implementation replayed
all canonical order-14 and order-16 graphs and again found zero traps among
112,732 and 1,869,590 realizable disconnected joins.  These are per-join
existential results, not reachability results for an initially fixed pair of
low coordinates and not a universal theorem.

### Connected odd factors and complete strong-snark preparation audits

For a relevant zero set \(T\), \(\mu_G(T)\) equals the minimum component
count of a spanning odd factor of \(G-T\).  A complete minimal-support
enumerator combines checked \(\mathbb F_2^2\)-flow witnesses with exhaustive
binary cycle-space evaluation.

| order | graphs | minimal supports | relevant \(\mu>1\) | realizable disconnected | preparable | traps |
|---:|---:|---:|---:|---:|---:|---:|
| 34 | 7 | 4,418 | 7 | 1,824,090 | 1,824,090 | 0 |
| 36 | 25 | 15,391 | 29 | 13,047,448 | 13,047,448 | 0 |
| 38 | 298 | 234,582 | 597 | 311,344,912 | 311,344,912 | 0 |
| 40 \(R_2\) | 1 | 33,517 | 9,516 | 1,968,017 | 1,968,017 | 0 |

The order-36 minimal supports split into 14,247 pairs, 1,135 triples, and
nine four-edge sets.  Among the relevant exceptions, 23 have \(\mu=2\)
and six have \(\mu=3\).  Thus the pointwise connected-odd-factor conjecture
is false even on cyclically-4-connected hosts, but every affected high
cycle also contains another minimal support with smaller \(\mu\).

Independent order-34 and order-36 audits used two-bit global blocking CNFs
rather than the producer's one-hot enumeration.  They checked all 19,809
flows, proved the unlisted-family formula UNSAT for each graph with
CaDiCaL's internal DRAT/LRAT checking, exhaustively recomputed all 36
exceptions, and classified all 14,942,208 high cycles with zero
discrepancies.  Temporary proof bytes were not retained.  The primary reports are in
`search/minimal-zero-set-audit-n34-20260725/` and
`search/minimal-zero-set-audit-n36-20260725/`.

The order-38 audit adds 188,843 pairs, 44,434 triples, 1,287 quadruples,
and 18 quintuples. Its 597 relevant exceptions comprise 582 supports with
\(\mu=2\) and 15 with \(\mu=3\), on 119 of the 298 hosts. An independent
two-bit blocking audit validated every retained flow and \(\mu\) witness,
checked the exceptional proper subsets, and reclassified all 312,475,648
high cycles with a separately compiled exhaustive helper. Its temporary
proof bytes are not retained, but CaDiCaL internally checked every
family-completeness proof and the audit result is PASS.

### Direct order-40 trap-candidate screen

The complete retained order-40 source has now been screened by the exact
necessary condition

\[
  \exists\,T\subseteq H\text{ minimal exact with }\mu(T)>1,
  \qquad
  \nexists\,S\subseteq H\text{ minimal exact with }\mu(S)=1.
\]

Every trap must satisfy this condition.  Realizability supplies a contained
minimal exact support; the trap inequality and the fact that \(H\) itself
is feasible give \(\mu(T)=\kappa(E-H)\geq2\).  Conversely, any contained
\(\mu=1\) support strictly prepares a disconnected complement.  Candidate
SAT with exactly two complement components is already sufficient for a
trap, since every contained minimal support then has \(\mu=2\); for three
or more components the screen remains only a necessary filter.

| graphs | batches | minimal supports | \(\mu=1\) | non-\(\mu=1\) | candidates | traps |
|---:|---:|---:|---:|---:|---:|---:|
| 7,654 | 60 | 6,053,028 | 6,009,319 | 43,709 | 0 | 0 |

The independent PASS replay covers all 60 batches and 7,654 graphs.  It
directly checks all 6,053,028 flow supports, classifies
16,051,601,408 binary cycles, and internally validates 7,654
support-completeness UNSAT proofs and 7,654 candidate CNFs.  The exact
\(\mu\)-profile and zero-candidate result match the primary run.  The
result, manifest, and checksum-ledger SHA-256 values are respectively
`0bacec06192ea5c03855ccc95070173c350f81fc809e59fbc0dbe73de2bb4c54`,
`ed8e85f845ef398e63fc2e705236b6ae311f3c4e8a2336f77ea548f34c5a096e`,
and
`fb9ebf90f57453efff948dd6d9cbc05c76bb086cdedc42e2396adaf94761c457`.
Zero candidates excludes preparation traps only on this retained finite
source; it is not a universal preparation theorem and not five-CDC.

The complete small-boundary control covers all 212 hard bases through order
18.  It finds 3,336 relevant minimal supports with
\(\mu\)-profile \(1:3272,\ 2:63,\ 3:1\).  The 64 non-\(\mu=1\) supports
occur on 60 graphs and are contained in 29,312 distinct highs; every one of
those highs also contains a \(\mu=1\) support.  Thus the candidate and trap
counts are both zero.  An independent standard-library checker reconstructs
all source identities and graph premises, independently rejects
three-edge-colourability for every base, exhausts 194,859,008 ordered cycle
pairs, and matches all support and high classifications.  Its status is
PASS.

### Complete canonical order-20 preparation-candidate census

The boundary was extended to every canonical connected simple cubic graph
of order 20.  The exact stream contains 510,489 rows: 497,818 are
bridgeless, 496,430 of those are 3-edge-colourable, and 1,388 are hard.
The hard rows contribute 21,686 inclusion-minimal exact supports, of which
21,682 are relevant.  Their exact profile is

\[
\mu=1:21,219,\qquad \mu=2:455,\qquad \mu=3:8.
\]

All 425,024 high cycles containing a non-\(\mu=1\) support also contain a
\(\mu=1\) support.  The necessary-candidate and preparation-trap counts
are therefore both zero.  The smallest number of contained
\(\mu=1\) supports on an affected high is three, attained by 2,240 highs
on 20 graphs.  In the unique affected graph having no singleton
\(\mu=1\) support, the minimum is twelve on 16 highs.

A producer-free C++20 replay independently decoded and re-encoded all
510,489 graph6 rows, reclassified bridges and Tait colourability, and
literally traversed all 5,821,693,952 ordered cycle pairs.  It reconstructed
every aggregate and all 1,388 semantic hard-row projections with zero
discrepancies.  An exhaustive two- and three-edge-deletion test found
exactly six cyclically 4-edge-connected hard graphs; all 170 of their
minimal exact supports have \(\mu=1\).  This is an independently verified
finite order-20 result, not a larger-order or universal theorem.

### Complete standard five-CDC cubic boundary through order 22

A separate target-standard run—not the preparation strengthening—generated
all 7,319,447 canonical connected simple cubic graphs of order 22.  It
classified 7,187,627 as bridgeless, 7,174,735 of those as
three-edge-colourable, and 12,892 as hard.  Literal structural filtering
found 31 hard rows with no 2-cut or nontrivial 3-cut and 20 that also have
girth at least five.  All 20 strict rows are standard five-CDC SAT.

The lower complete filters contribute three strict rows through order 18
and six at order 20.  For every one of these 29 rows, the retained package
contains the graph, pair labels, a complete CNF, and a satisfying
assignment.  The primary checker validates exact-two coverage and all five
vertex parities; the independent Go checker accepts the same raw witnesses.

A producer-independent Python/C++ audit then:

- scanned and decoded all 7,319,447 fixed-width order-22 records;
- matched all 12,892 hard identities, girths, 2-cuts, and
  inclusion-minimal nontrivial 3-cuts;
- freshly regenerated and filtered every even order from 4 through 20;
- checked every assignment against every clause in both CNF families;
- checked all 435 retained \(S_5\)-normalization units and exhaustively
  regressed the local normalization rule.

The exact bounded corollary is: every finite bridgeless cubic multigraph
whose connected components have at most 22 vertices has a standard 5-CDC.
The proof chooses a minimum-order bad cubic component and applies the audited
loop/parallel-edge, cut, triangle, and square reductions before invoking the
29 strict witnesses.  Cubic expansion can increase order, so this statement
does not cover arbitrary noncubic graphs of order at most 22.  The frozen
construction packages are under `search/*standard-five-cdc-20260725/` and
`search/order22-filter-census-20260725/`; the independent audit ledger is
`blind-audit/order22-finite-package-audit-SHA256SUMS`.

### Peripheral-cycle singleton theorem

Tutte's theorem that every edge of a finite 3-connected graph lies on a
peripheral cycle gives a universal preparation statement for singleton
supports.  In a cubic graph, the complement of such an induced cycle is
connected: the outside vertex-deletion graph is connected and every cycle
vertex has one spoke to it.  Hence
\(\mu_G(\{e\})=1\) for every edge of every finite simple 3-connected cubic
graph.

An independent standard-library implementation checked all 1,600 frozen
hard rows through order 20.  Among the 985 rows satisfying the simple
3-connected cubic premise, it found a connected-complement cycle through
each of 29,037 edges, with zero failures.  It independently reconstructed
the order-18 singleton \(\mu=2\) control and explicit cuts excluding that
graph from the premise.  On the seven order-34 sources it also found the
two arbitrary co-cyclic pair failures while confirming
\(\mu=1\) for all 4,188 exact minimal pairs.  This last pair result is
finite evidence only; the theorem proved here is the singleton case.

### Exact-pair marked-core reduction

For a connected simple cubic graph other than \(K_4\), an exact
two-edge \(\mathbb F_2^2\)-zero set is a nonadjacent matching.  Deleting
the pair and suppressing its four degree-two ends produces a loopless
Tait-colourable cubic multigraph.  In girth at least five there are only
two endpoint geometries: four independent ends give four once-subdivided
marked core edges; one cross-edge gives two once-subdivided marked edges
and one twice-subdivided edge.  The connected-odd-factor condition is
equivalent in each case to a connected spanning core subgraph satisfying
explicit component-cut parity equations.  On the twice-subdivided path,
the alternative using only the middle edge is odd but necessarily forms a
separate component.

The producer-independent audit enumerated all 27 canonical simple cubic
graphs of orders 4, 6, 8, and 10 and all 1,439 exact pairs.  It found zero
nonadjacency failures and exactly three suppression degeneracies, the
three perfect matchings of \(K_4\).  The repaired core theorem applies to
the other 1,436 pairs.  It checked 530 independent-end cases and 15,784
fixed-\(Q\) orientation eliminations, plus all 60 girth-five single-cross
cases and 3,840 further fixed-\(Q\) comparisons, with zero discrepancies.
Direct odd-factor enumeration matched all 120 reconstructed connected
factors; all 480 middle-only controls were disconnected.  This is an exact
reduction and finite audit, not a proof that every exact pair has
\(\mu=1\).

A targeted marked-core search then tested 5,000 marked sets on 50
order-24 cubic-bipartite cores and 10,000 marked sets on 100 arbitrary
order-24 Tait-colourable cores.  Complete affine enumeration found 79 and
197 connected-odd-factor failures respectively.  All three external
pairings were reconstructed for every failure: all 828 graphs have
explicit proper three-edge-colourings, so the proposed exact pair is
nonminimal because the empty zero set is already realizable.  A separate
one-cross search tested 2,000 marked triples, found 15 failures, and again
gave explicit Tait colourings for all 30 simple reconstructions.  Every
one of the 858 reconstructions has girth three or four.

As a non-Tait control, complete cycle-space audits of the Flower snarks
\(J_5,J_7,J_9\) checked respectively 375, 777, and 1,323 exact minimal
pairs.  Every one of the 2,475 pairs has a directly recorded
connected-complement cycle.  A separate checker re-enumerated the full
affine odd-factor spaces for the 291 failed marked instances and validated
all reconstructions, exact flows, colourings, and cyclic-cut metadata.
The frozen package is
`search/marked-core-exact-pair-search-20260725/`.  These deterministic
samples do not prove the suggested alternative “connected factor, or Tait
reconstruction, or a cyclic cut below four.”

A follow-up specification audit falsified the unqualified version of the
pair lemma and isolated the needed hypothesis.  In lexicographic edge
order on \(K_4\), the exact flow
\((0,1,1,1,1,0)\) has the opposite-edge zero set
\(\{01,23\}\), while both containing cycles leave two disjoint edges.
The dodecahedral graph supplies a strict-looking but still Tait
counterexample: it is simple cubic of girth five with no cycle-separating
cut of size at most four, yet the retained exact pair has \(\mu=2\).
Exhaustive replay checks all \(2^{11}\) binary cycles, the 512 cycles
containing the pair, the flow, the Tait colouring, and all cuts of size at
most four.

The corrected non-Tait/inclusion-minimal statement was then screened on
the complete 7,654-row order-40 strong-snark source.  Of 13,547,580 edge
pairs, 13,547,063 have an explicit connected-complement cycle.  The
remaining 517 all fail a direct exact-zero-pair flow test, leaving zero
exact failures.  The same audit records why Catlin perfect-matching
contraction is insufficient: ordinary 4-edge-connectivity and aggregate
parity survive, but connectivity need not survive splitting each quotient
vertex into its two ports.  The frozen package is
`search/exact-pair-theory-resolution-20260725/`, whose ledger hash is
`0957e46c0d93fb486d3183933ed4d7f69cc0e1732315475a68eb6ed6910e4fde`.

For the 40-vertex \(R_2\) graph, the Petersen 2-pole decomposition instead
gives a solver-free exact factorization of all 33,517 minimal supports:
33,516 size-four cycle-contained matchings and one irrelevant size-six
nonmatching support.  A full \(2^{21}\)-cycle audit found 24,000 relevant
supports with \(\mu=1\), 8,160 with \(\mu=2\), 1,308 with \(\mu=3\), and 48
with \(\mu=4\). It classified all 1,968,017 realizable disconnected joins
as preparable. Across the order-34, order-36, order-38, and \(R_2\) audits
this is 287,908 minimal supports and 329,515,008 high-cycle
classifications; all 328,184,467 realizable disconnected joins are
preparable. These totals remain finite evidence for a universal statement.

The domination margins on the three retained strong-snark sources were
then reconstructed by a clean-room Walsh--Hadamard implementation.  It
classified all 131,596,288 affected highs on 134 graphs and reproduced
every primary per-graph and aggregate histogram:

| order | affected graphs | affected highs | minimum contained \(\mu=1\) supports | highs at minimum |
|---:|---:|---:|---:|---:|
| 34 | 4 | 204,800 | 21 | 1 |
| 36 | 11 | 1,122,304 | 22 | 16 |
| 38 | 119 | 30,312,192 | 20 | 3 |

All three necessary-candidate counts are zero.  The audit also checks all
254,391 retained \(\mathbb F_2^2\)-flow witnesses, every relevant
\(\mu\)-witness, edge-mask guards, and an edge-62 UBSan control.  The
primary reports' recorded `/private/tmp` helper binary was not retained;
the source rebuilds reproduce the reports after deleting only the helper
path and binary-hash fields.  The combined audit ledger is
`search/preparation-margin-profile-audit-20260725/SHA256SUMS`.

The independent \(R_2\) checker reproduced those figures without importing
the producer and sharpened the result: all 1,970,577 cycles containing any
relevant support contain a support with \(\mu=1\); the remaining 126,575
cycles contain no support.  Hence no \(R_2\) high cycle needs one of the
9,516 exceptional supports for preparation.

A compact structural certificate now proves that domination without the
global cycle scan.  Support containment is exactly nonemptiness of the base
and three pole-internal blocks.  A pole cycle cannot remain inside the
five-edge tree formed by the cut edge and its neighbors, so each nonempty
pole block supplies a far edge.  Four base and three pole odd-factor
witness rows glue to a connected odd factor for all
\(12\cdot10^3=12,000\) all-far supports.  The corresponding block-state
product is \(15\cdot31^3+3\cdot16\cdot31\cdot32^2=1,970,577\).  An
independent standard-library checker verified all 2,097,152 compatible
local tuples, the type-B necessity direction, and all 12,000 gluings with
zero failures.

A third route used a generic incremental one-hot CaDiCaL enumeration rather
than the pole factorization.  It returned 33,517 directly validated flow
models and an exactly equal support set with the same canonical digest.
Because its terminal UNSAT proof bytes were not retained, this is an
independent computational cross-check, not a second completeness
certificate.

### Rooted-preparation necessity census

An exact bounded census searched for a base \(B\) and edge \(s\) for which
unrooted preparation holds but preparation rooted at \(s\) fails. All
45,982 canonical connected simple cubic classes through order 18 were
generated; 44,327 were bridgeless, giving 1,181,250 singleton-root pairs.
Of these bases, 44,115 were 3-edge-colourable and 212 required complete
cycle-code evaluation.

The hard computation covered 198,080 binary-cycle words, 194,859,008
ordered flow pairs, 195,000 realizable highs, and 5,216,238 high/root
obligations. It found zero unrooted failures and zero singleton-root
failures. An independent checker that does not import the producer
regenerated the graph6 streams, independently reclassified every graph,
rebuilt all 212 exact common-zero-set families, and matched every retained
profile. The substitution stage was not reached because no eligible failed
root existed. These are finite preparation-property results only; rooted
redundancy and five-CDC remain unresolved.

### Pair-root preparation obstruction

A complete exact pair census separates singleton-root from multi-root
preparation. Across all 212 hard bases it checks 71,313 unordered edge
pairs and 67,244,094 realizable-high/pair obligations. Nine pairs fail on
two order-18 graphs, across 128 highs and 144 obligations. The first failure
is order-minimal. A producer-free full replay independently derives the
cycle codes, minimal exact supports, connected factors, and all pair-root
quantifiers on the 212 graphs and matches every total. The first witness is
on the graph6 record
`Q????B?K?WWCg_?sIG?s?HO?KG?`. The graph is simple, cubic, connected, and
bridgeless. Its binary cycle code has dimension ten. The high with mask
1,313,837 contains exactly the five minimal supports
\(\{10\},\{11\},\{18\},\{20\},\{2,5\}\).

The full exact-zero enumeration yields 43,950 exact sets and 15
inclusion-minimal relevant sets. For the five contained supports, unrooted
minima are \(1,1,1,1,2\), while all five minima subject to containing roots
\(\{9,19\}\) equal two. Among all 1,024 spanning odd factors, exactly 13
connected factors avoid some candidate and none contains both roots. A
global replay checks 1,008 realizable highs and all 27,216 singleton-root
obligations with zero failures. This is an exact obstruction to a
multi-root strengthening, not a five-CDC obstruction.

### Adaptive sequential Petersen-2-pole transfer

The exact one-step pullback depends on where the fixed next edge lies. For
\(G=B[P_2/s]\), a surviving edge \(e'\) satisfies
\(\mathsf{RP}(G;\{e'\})\) iff \(\mathsf{RP}(B;\{s,e\})\); either new
terminal and every internal pole edge \(p\) satisfy
\(\mathsf{RP}(G;\{p\})\) iff \(\mathsf{RP}(B;\{s\})\). This permits a
sequential substitution path that always continues inside the newest pole,
but not unrestricted surviving-edge branching.

An independent standard-library checker enumerates all 64 binary and 4,096
\(\mathbb F_2^2\) cut states and proves equal terminal data directly. Among
all 16,384 internal edge subsets it finds exactly five connected
parity-correct fragments; exactly four can omit a far edge, and they are the
four primary templates. They cover all 882 nonempty-high/internal-root
obligations. The checker also independently rebuilds the order-18 pair
obstruction and its order-28 substitution. The latter has 32,768 binary
cycles, 175 connected odd factors, and 150 factors containing surviving
root 19. Every such factor projects correctly, with zero eligible projected
pair-root factors. The displayed high and exact support \(\{9,32\}\) are
validated directly. This is rooted preparation transfer plus a finite
boundary witness, not a five-CDC result.

### Nested Petersen-pole family and zero-coverage census

Inducting the adaptive singleton transfer produces an infinite family from
any verified singleton-rooted base. Each substitution adds 10 vertices and
15 edges. At every finite depth the graph has root-free preparation and 16
separate continuation-root properties—14 internal and two terminal—in its
newest pole. The next root is fixed before the high is quantified; the 16
properties do not require one common witness. A clean-room constructor
checks every continuation and a base/internal/terminal depth-three path at
orders 10, 20, 30, and 40, including exact reverse contractions to Petersen.

The retained reduction census independently parses and premise-checks all
7,984 frozen source rows and reproduces their 7,984 nauty identities. Its
cut algorithm is independent of the producer: two edges form a cut exactly
when their membership columns agree across a binary cycle-space basis.
All 14,067,888 edge pairs are compared, with zero matches. A forward cut
Petersen pole has a ten-vertex shore with exactly its two terminals in the
boundary, so it necessarily implies a two-edge cut. Hence all 7,984 rows
have zero cut poles, zero nested reductions, and an empty covered-identity
list. This is finite zero coverage only.

### Suppression and connected-complement characterizations

A relevant exact common-zero set is a matching \(T\).  Deleting \(T\) and
suppressing its degree-two endpoints produces a cubic pseudograph; exact
zero set \(T\) exists precisely when this core is Tait-colorable.  Relevance
is the exact condition that every component of \(G-T\) contains an even
number of \(T\)-endpoints.  Splitting odd factors into endpoint matchings,
branch attachments, and a branch subgraph gives a separate exact
attachment-parity formula for \(\mu_G(T)\).

On the order-34 control with \(T=\{e_{16},e_{26},e_{41}\}\), the suppressed
core is simple, connected, and Tait-colorable, while \(G-V(T)\) is connected.
Nevertheless \(\mu=2\).  Two bridges of the branch graph require shore
parities \((1,1)\); the 16 possible endpoint attachments give only
\((1,0)\) or \((0,1)\), eight times each.  This is a direct obstruction to
the discarded connectivity-only strengthening.

Separately, quotienting a \(D_5\)-flow by the weight-four vector omitting
coordinate \(i\) sends exactly the labels in \(E-C_i\) to the distinguished
Fano line.  Thus connected-kernel flow is equivalent to a 5-CDC with a
connected coordinate complement.  The executable controls are
`tools/suppression_zero_set.py` and
`tools/test_suppression_zero_set.py`.

## Exact obstruction and certificate controls

Status: **PARTIAL STRUCTURAL PROGRESS / CONTROL VALIDATION**.

Constructor C exhausted the ten pair-label local code and retained a
manifested run under
`search/obstructions/runs/control-20260725-v3/`.

- The 1,000 ordered cubic triples have exactly 60 XOR-zero states, precisely
  the ordered \(K_5\)-triangles.
- Ordered cut-label XOR counts at sizes 1–4 are respectively
  \(0,10,60,640\); the four-cut rows split into 280 paired and 360
  four-cycle patterns.
- Of all 10,000 ordered four-cycle boundaries, 640 satisfy cut parity and
  exactly 60 fail to extend.  All 60 are the proved alternating-intersecting
  pattern, with no discrepancy.
- All \(2^{10}\) binary Petersen-state histograms were checked; the
  16-element kernel is the \(K_5\) cut space, and the integer histogram
  identities hold on independently generated Petersen witnesses.
- Standard Petersen \(k=5\) is SAT through A-XOR, A-CNF, B-CNF, and B's
  backtracker; every witness is accepted by both semantics checkers.
- The deliberately modified Petersen \(k=4\) control is UNSAT.  Its
  60-variable, 310-clause auxiliary-free CNF has an LRAT accepted by both
  `lrat-check` and CakeML `cake_lpr`.  This is not the target formula.
- The 112-vertex disjoint affine-plane 8-CDC is checked exactly and has
  co-occurrence \(K_8\).  All 120 normalized seven-column subsets rule out a
  fixed \(5\times8\) XOR compression.

### Circuit-component recoloring controls

For a supplied cubic CDC, an exact analyzer splits every old coordinate into
circuits, makes two circuits adjacent when they share a graph edge, and
computes the chromatic number of this component-conflict graph.  Proper
colorings are exactly the valid partitions of those circuits into new CDC
coordinates.

- The disjoint 112-vertex affine control has 56 circuit components, 84
  simple conflicts, chromatic number 4, and a checked four-coordinate
  recoloring.
- A connected 13-switch control has 30 components, 71 conflicts, chromatic
  number 4, and a checked four-coordinate recoloring.
- A connected, bridgeless 24-switch obstruction has exactly eight circuit
  components, 28 conflicts, conflict graph \(K_8\), and chromatic number 8.
  For each coordinate, the six selected plane links are independently
  checked to form a tree on the seven containing planes.

The last row disproves only universal partition-and-recolor compression of
an arbitrary supplied 8-CDC.  It is not a target-standard UNSAT result.
Artifacts are under `search/component-recoloring-affine-20260725/` and
`search/component-recoloring-obstruction-20260725/`.

### Affine relabelling plus quotient-lift audit

The coordinate-tree supplied 8-CDC was tested under every arbitrary
bijection of its coordinates with \(\mathbb F_2^3\), followed by every
Fano-line quotient lift.  Translation and \(GL(3,2)\) reduce the 8!
bijections to 30 labelled affine structures; every orbit size is checked as
168.  All 210 structure/line cases fail, and the minimum number of
four-value-odd components is two.  Direct binary Gaussian elimination
agrees with the component criterion in every case.  The connected affine
control has one good structure and three good lines.  The deterministic
package `search/eight-cover-affine-relabel-audit-20260725/` has
`SHA256SUMS` hash
`8c51ad2e65c5154b220e762f81e724cc515deeecf6c7d1fd5d3f55f7c6c461ff`.
This is a compression no-go for one supplied cover, not standard 5-CDC
UNSAT.

### Ten-support packing obstruction

For each \(a\in D_5\), an exact two-dimensional quotient of a standard
five-cover gives an \(\mathbb F_2^2\)-flow whose zero set is exactly the
\(a\)-label class.  Without a nowhere-zero \(\mathbb F_2^2\)-flow, the ten
classes contain ten pairwise edge-disjoint inclusion-minimal exact supports.
Thus the minimal-support hypergraph has matching number at least ten.  The
Petersen, \(R_2\), and \(R_4\) retained witnesses pass direct quotient
checks; Petersen and \(R_2\) materialize ten disjoint minimal supports.
The package ledger hash is
`1f0a195a6e81aa6d3628a668ed5c214bacad39e135390ce4c9551cbb1b9092dd`.
The numerical \(10r_f\leq |E|\) consequence is explicitly not claimed as
new; the packing condition is the usable obstruction.

### Exact matching/four-flow encoding and component parity

For finite loopless cubic multigraphs, an exact alternative target formula
uses a matching \(M\), two cycles with intersection \(M\), and an
\(\mathbb F_2^2\)-flow with exact zero set \(M\).  The \(H_2\) control has
615 variables, 2,296 ordinary clauses, and 328 native XOR rows and is SAT.
A clean-room audit reconstructed every constraint and explicitly
reverse-lifted the model to a five-cover of sizes
\(59,55,44,23,65\).  The frozen package ledger hash is
`4dc828e60075db452c527816dbdc33ccad38c1bb78f7811b8308aaea1b9868dd`.

The cycle-intersection condition is equivalent to even endpoint demand in
every component of the complement odd factor.  A complete replay of the
seven order-34 relevant minimal exact supports with \(\mu=2\) checks 32,768
containing cycles per support.  Two supports are GOOD, with 416 good cycles
each, and five are BAD.  Every graph has a separate \(\mu=1\) positive
control, so BAD is a support classification rather than graph UNSAT.  The
package ledger hash is
`dc7dec518d61a39d46ff7e1dc72896e4eb33880e9a9ba979293def882c47bfce`.

### Minimum exact-zero matching frontier

Status: **EXACT FINITE THEOREM / UNIVERSAL EXCHANGE STEP OPEN**.

The two-cycle intersection condition is equivalent to packing two
edge-disjoint \(T\)-joins in \((G-M,\partial M)\).  The imported
Codato--Conforti--Serafini theorem reduces any failure for a fixed exact-zero
matching with componentwise even terminal parity to the odd-\(K_{2,3}\)
graft-minor obstruction.  A \(T\)-odd component is a separate obstruction
with no \(T\)-join at all; this hypothesis was restored after blind audit.
The auditor's ten-vertex graph6 instance `Is?AXW[[?` is frozen in
`search/component-parity-tjoin-countermodel-20260725/`; its independent
checker confirms cut minimum zero, no \(T\)-join, all three quotient
forests, and an explicit standard five-cover positive control.
The
human proof of the reduction, including the boundary calculation and the
precise imported-theorem boundary, is in
`docs/minimum-zero-tjoin-route.md`.

For every \(T\)-join \(J\) and every nonzero restricted-flow color \(c\),
the binary-cycle switch on \(M\cup J\) has exact zero matching
\(J\cap\phi^{-1}(c)\).  If \(M\) is minimum, this proves the new inequality
\(|J\cap\phi^{-1}(c)|\ge|M|\) and therefore \(|J|\ge3|M|\).  A diagnostic
all-support audit on reconstructed \(H_3\) found no violation: every one of
the 92,313 rows has color-specific shortest \(T\)-join costs at least three,
79,669 have equality in some color, and unweighted shortest sizes range
from 12 to 25.  These values test the proof but do not establish the open
packing step.

The complete order-20 hard source has 20,749 minimum exact supports.
Of these, 20,720 have a connected complementary odd factor.  The remaining
29 occur on 12 hosts; exhaustive cycle enumeration proves that all 29
still satisfy the weaker exact component-parity condition.  Thus every
minimum support in the complete order-20 hard corpus extends.  All 20
strict order-22 rows have a minimum connected-complement support.

On reconstructed \(H_3\), the source formula restricts to exact-zero
matchings of size at most three.  The pre-existing resistance LRAT excludes
sizes zero, one, and two.  Projected enumeration finds exactly 92,313
distinct size-three supports, and a compact witness row supplies the two
flow coordinates and two intersecting cycles for each.  A direct checker
reconstructs all five cover coordinates for all rows.  After one support
blocking clause per row is appended, the completeness CNF is UNSAT; the
retained LRAT is accepted independently by `lrat-check` and CakeML
`cake_lpr`.  Therefore **every** minimum exact-zero matching of this fixed
graph extends.  Minimum-cardinality witnesses also extend on \(H_4\) and
\(H_5\).

The full hard order-22 source was then tested by an independently replayed
minimum-extension package.  All 12,892 rows have some extending minimum
support, with profile \(1:12885,\ 2:7\).  The seven at-most-one lower-bound
formulas have 132 variables and 438 clauses each; all seven text LRATs pass
both `lrat-check` and CakeML `cake_lpr`.  All 12,892 compact positive
witnesses are directly checked and reverse-lifted.  The package ledger is
`ed334f2df4131ed29b2924e4178e7f7853cf5a143e0427ac91ebb2c274d343f5`.

Reproduction:

```sh
(cd search/minimum-zero-matching-five-cdc-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
```

The package ledger SHA-256 is
`623c4d27043934fcca68534f66c252e62357714916d467a1b349b66debf19904`.
No extrapolation to all graphs is made.

### Certified nonextendible Petersen two-factor

Fix the Petersen two-factor
\(\{0,1,2,3,4,10,11,12,13,14\}\).  The complete direct formula with its
first coordinate fixed has 175 variables and 690 clauses; the exact
matching/four-flow cross-formula has 75 variables and 295 clauses.  Both
are UNSAT.  Both retained LRATs pass `lrat-check` and CakeML `cake_lpr`.
A standard-library checker independently enumerates the 64 binary cycles,
all 4,096 ordered flow pairs, and all parity-good matching subsets, finding
zero exact extension.  The unrestricted Petersen model remains valid with
coordinate sizes \(6,5,5,9,5\).  This is a fixed-coordinate obstruction,
not a target graph counterexample.  The frozen ledger hash is
`d8a2eeb9241e2cb23f48cf4d2e9502a467e4cf46c4ab53dff1419cc582ff6b9c`.

### Ten-flow exact-zero partition relaxation

The target-sound relaxation asks for ten \(\mathbb F_2^2\)-flows whose
nonempty exact zero sets partition all edge objects.  On \(H_2\) its 3,690
variables, 15,918 ordinary clauses, and 1,640 native XOR rows are SAT.  The
zero-set sizes are \(43,12,10,15,5,7,5,4,9,13\).  The flows need not be
compatible quotients of one five-cover, so SAT is only a positive
relaxation witness; certified UNSAT plus the no-nowhere-zero-flow premise
would be a sound rejection.  The frozen ledger hash is
`056a1e3e8cb6990af9a58390b2eab1e0d07ab93397c9851b7dc1e4e6f15a7501`.

### Reconstructed high-flow-resistance \(H_3\)

The next exact figure-and-label recursion step yields a simple cubic graph
on 122 vertices and 183 edges.  Exhausting all 46,234,462 edge deletions of
size at most four proves cyclic connectivity at least five.  An explicit
three-zero flow and a checked LRAT excluding all two-zero flows establish
flow resistance three.  The direct standard five-cover formula is SAT with
coordinate sizes \(77,74,58,77,80\); both semantic verifiers accept it.
The exact matching/four-flow formula is independently SAT and reverse-lifts
to another valid five-cover.  A fresh clean-room run reproduced independent
result SHA-256
`fc466809140c3851441da82d319b38a68c9e8e03fc36434a1cd2946790d3babe`.
The package and audit ledger hashes are respectively
`d019c2f36a4a3ad392a00b4de64fa150c22ace4615d715583e015e14ba51e99f`
and
`929a46366e9275c6fe5603caa65ac61f41b318045534bba713b4f9d7e6fe0260`.
The reconstruction remains figure-derived because no author graph file is
available for identity comparison.

### Reconstructed high-flow-resistance \(H_4\)

The next exact recursion step has 162 vertices and 243 edges.  It is simple,
cubic, girth five, and cyclically 5-edge-connected; the last property is
proved by a 1,859-variable, 5,402-clause UNSAT cut formula and retained
LRAT.  An explicit four-zero flow plus a 1,455-variable, 3,708-clause
UNSAT formula excluding at most three zeros proves flow resistance four.
The direct standard five-cover formula is SAT with coordinate sizes
\(130,112,68,72,104\), and the exact matching/four-flow instance is also
SAT and reverse-lifts to a valid five-cover.  Both LRATs pass `lrat-check`
and CakeML `cake_lpr`; a fresh producer-free audit is byte-identical.  The
package and audit ledger hashes are respectively
`f7866131334940d4e8a98f56b9a530b8cc98a85b02124d2c8b235297a2ff39c4`
and
`4a9b1c26ee46aa7c2e49409464ccdb4d0757cb8f97825f7963c75bd049d91d98`.

### Reconstructed high-flow-resistance \(H_5\)

One more exact recursion step has 202 vertices and 303 edges.  It is simple,
cubic, girth five, and cyclically 5-edge-connected, with the latter proved
by a 2,319-variable, 6,742-clause UNSAT cut formula and retained LRAT.  An
explicit five-zero flow plus a 2,117-variable, 5,224-clause UNSAT formula
excluding at most four zeros proves flow resistance five.  The authoritative
standard formula is SAT with coordinate sizes \(144,143,95,98,126\).
Both independently generated direct models pass both semantic verifiers;
the matching/four-flow model independently reverse-lifts to another valid
five-cover.  The root replay checked both LRATs under `lrat-check` and
CakeML `cake_lpr` and regenerated the clean-room result byte-for-byte, with
SHA-256
`e2060d12ef8e5263ab2d6aac58bedd4396a0c99064ea6b549cf7bf6f42bde91d`.
The package and audit ledger hashes are respectively
`cb8cb3b7cbdbd698c0e73b979e0f777249e2ea15b175cc94571f519a8ddff0a5`
and
`480e6ec07eb27c42259af23c0597d793b01848fc08d5367ed433f8d004817dc4`.

### Stable \(D_5\)-tile induction for the frozen reconstruction

The finite witnesses were relabeled and cut at the recursive closure.  A
single raw open-\(J\) tile was found with identical input/output state
\((01,01,02,23,03)\).  Its 55 internal edges and ten boundary half-edges
are conservative at all 40 internal vertices.  The relabeled
\(\widehat H_2\) base has the same state, so the generic boundary-cancellation
identity proves a standard five-CDC on every frozen reconstructed
\(\widehat H_n\), \(n\ge2\).  The coordinate-size formula is
\[
(62,54,39,47,44)+(n-2)(32,24,29,20,15).
\]

The checker pins 12 provenance inputs, replays the induced labeling
edge-for-edge on \(\widehat H_2,\widehat H_3,\widehat H_4,\widehat H_5\),
checks the 55-edge/40-vertex tile, and reproduces its semantic report.  Six
negative tests reject corrupted topology, labels, base relabeling, and
coordinate increments.  The independent Lean file evaluates all 65 tile
objects and 40 conservation equations.  The package ledger SHA-256 is
`e09cee11f74b19e4a08f18c94534207e44f601a29f059a15fb614154900cbfac`.

### Oddness-two novelty audit

The author-defined MNP family is already covered by a prior sufficient
theorem.  Figures 3 and 6 and Theorem 3.6 of arXiv:2604.22501 give a
3-edge-coloring proper except at two vertices, each incident with
\((a,c,c)\).  Hence the \(a\)-edges form a perfect matching.  In the
complementary 2-factor a circuit has parity equal to the number of conflict
vertices it contains modulo two.  The conflicts cannot share a circuit,
since otherwise all factor circuits would be even and the graph would be
3-edge-colorable.  Thus there are exactly two odd circuits, and
Huck--Kochol (1995) already supplies a five-cycle double cover.

The uniform deduction is human, not a finite extrapolation.  As
corroboration, an independent checker validates retained perfect matchings
on the four frozen graphs and 8,190 abstract transition patterns.  The
novelty-audit ledger SHA-256 is
`3dc1455e0290624e9d6c678b6e5b0ef1115cdc68c1dcdef6d29587a0e2686e81`.
The audit does not identify the author family formally with the frozen
figure transcription, does not address orientability, and limits any
publication claim to the explicit stable certificate and its packaging.

Reproduction:

```sh
python3 -m unittest search.obstructions.test_obstruction_miner -v
python3 search/obstructions/run_experiments.py \
  --run-dir search/obstructions/runs/my-new-run
```

The retained run has 104 checksum entries.  Key hashes:

```text
summary.json          aada0cf923771abffa8cd6d76e9d745fc1a914df8e25c3498f4091d52465db83
SHA256SUMS            1bbf5d30b935417c8115edb90014d3022fcd6fcb60d2926442068fe2243026d4
Petersen k=4 CNF      b8bfd5e8ba32e46098f47fab81bd35a374315c4fb51758bb4aa109e94f4edca3
Petersen k=4 LRAT     1ad51b7ab5f2970d728e1c4bb8787e7083f463c8502035137cd29724d4bba4fc
```

## Structured-family portfolio

Status: **COMPUTATIONAL EVIDENCE**.  It found no counterexample and does not
establish a new universal family theorem.

Twenty-eight deterministic simple cubic bridgeless graphs were generated
from six flower snarks, eleven generalized Petersen graphs, four explicit
dot products, one order-40 Petersen-\(P_2\) insertion, and six voltage-cover
controls.  CryptoMiniSat returned SAT for every native-XOR instance.
Verifier A accepted every model, and independently translated models were
accepted 28/28 by Verifier B.  On the order-40 oddness-six graph, Verifier
B's independent ten-label backtracker also constructed a second witness
after 145,856 nodes.

The strongest boundary specimens were:

- order 40, girth 5, exact oddness 6: SAT;
- order 130, girth 10, exact oddness 0: SAT.

No connected graph in this original batch simultaneously had girth at least
10 and oddness at least 6.  The later candidate-domain experiment above
enters that intersection at one positive graph; neither batch clears the
domain.

Reproduction:

```sh
python3 -m unittest search.structured.test_families -v
python3 -m search.structured.run_portfolio \
  --output artifacts/structured \
  --solver-timeout 120 \
  --oddness-timeout 120
python3 search/structured/crosscheck_verifier_b.py \
  --artifacts artifacts/structured
```

The first command reports six passing tests.  The stored run hashes are:

```text
primary ledger       a18315521b3aa25d5b57006d41c1a5ff073549fe6e2e2223c7c636410dda00e5
verifier-B ledger    a0fcb28faebe9159060d066b48a0c4dd13173db1cb960154fe14dfbd4c59bc77
verifier-A manifest  aaf7028de7f8f96b1949c7000c1caf8f83a756af196f9796433a0b73c08ff8fc
verifier-B binary    78416436bb35a758841e535fe2aff7b98d0f014f05e3f526a112f9b2b90328fe
```

Voltage-cover rows are explicitly inheritance controls: a 5-CDC on a base
pulls back to every graph cover.  Dot products were solved from scratch; no
preservation rule was assumed.

## Canonical simple-cubic run through order 10

Status: **VERIFIED FINITE CASE / PIPELINE VALIDATION**.  This is below known
published bounds and proves no new finite frontier.

Constructor A used nauty `geng` 2.9.3 to emit one representative of every
connected simple cubic isomorphism class at orders 4, 6, 8, and 10.  The
pipeline independently parsed graph6, rechecked simplicity, cubicity,
connectivity, bridges, girth, exact 3-edge-colourability, and (within this
range) oddness.  It then solved both Verifier A's native-XOR instance with
CryptoMiniSat 5.14.7 and its ordinary CNF with CaDiCaL 3.0.1.  Every returned
model was checked against the original graph semantics.

| order | generated | bridgeless | SAT by each solver |
|---:|---:|---:|---:|
| 4 | 1 | 1 | 1 |
| 6 | 2 | 2 | 2 |
| 8 | 5 | 5 | 5 |
| 10 | 19 | 18 | 18 |
| **total** | **27** | **26** | **26** |

There were 52 accepted solver models, 25 of the eligible graphs were
3-edge-colourable, and the Petersen graph was the sole non-3-edge-colourable
case.  The sourced minimum-counterexample filter
\(girth\geq10,\ oddness\geq6\) selected zero graphs; that empty filtered
domain is recorded separately from the raw validation census.

Reproduction:

```sh
python3 -m unittest search.canonical.test_canonical_search -v
python3 search/canonical/canonical_search.py \
  --min-n 4 --max-n 10 \
  --geng /opt/homebrew/bin/geng \
  --cryptominisat /opt/homebrew/bin/cryptominisat5 \
  --cadical /opt/homebrew/bin/cadical \
  --solver both \
  --oddness-max-vertices 10 \
  --cover-canon-max-vertices 10 \
  --output search/canonical/runs/integration-n10-20260725
```

The stored run is immutable-by-convention because the generator refuses to
overwrite an existing output directory.  Key hashes:

```text
canonical_search.py  f7d7d271356bcd0ae62cd2efaf16bacb080a3b18084d9c19dd64e31d15bbed03
results.jsonl        4a823ba7276c613df7bf889cd2973f094ffe4c9d4a97becb1cbc16750a52ad34
summary.json         143f0497588de3bbb264a7cfda607150473687a036c714dbfa2eacfb48d7c2ab
SHA256SUMS           30d9f41a5cfcc1b247c9fbdb3ff4b0b29b1608dce20c2da7d642517d329a48cf
```

All 395 entries in the run manifest pass from the run directory.

## Independent-verifier integration controls

Status: **PIPELINE VALIDATION**, not a finite-case theorem.

The integration script `tools/crosscheck_verifiers.py` translated four fixed
graph objects into both verifier formats, generated both ordinary CNFs, solved
both with CaDiCaL 3.0.1, and passed every SAT model to both direct semantics
checkers.

Command:

```sh
python3 tools/crosscheck_verifiers.py \
  crosscheck/graphs/k4.json \
  crosscheck/graphs/petersen.json \
  crosscheck/graphs/loops-and-parallels.json \
  crosscheck/graphs/bridge-negative-control.json \
  --output artifacts/crosscheck-20260725
```

Results:

| object | premise | verifier-A CNF | verifier-B CNF |
|---|---|---:|---:|
| \(K_4\) | bridgeless | SAT | SAT |
| Petersen graph | bridgeless | SAT | SAT |
| loops/parallel/disconnected control | bridgeless | SAT | SAT |
| one-edge bridge control | **not bridgeless** | UNSAT | UNSAT |

The ledger hash is
`d0d4419615ba1f011847cb30a0d4a52ac197efdb1cba2718f6648516550dc055`.
The bridge row is deliberately a negative control: its certified UNSAT
formula can never be a counterexample because it fails the premise.

For that negative control, CaDiCaL emitted LRAT independently for each CNF.
Both the C `lrat-check` program and the CakeML-generated `cake_lpr` program
accepted both proofs.  The two CNF/proof hash pairs are:

```text
Verifier A CNF   02c37f810840205fcfce5e3be75d736a73719276cb498d11829bfe249b5149a2
Verifier A LRAT  bf109104dc0f487b2a787ee2a5c2f1c16e5c8a4a4f60dd04c5e2d6f5fa213f6d
Verifier B CNF   142112d3521bf316043334cb4fe02afbfa00248eceb549bc0c5593485f63cad6
Verifier B LRAT  87f93ea6877a7723b88297eb5890fddbf95edaacf5499a8f02ce6100f819e770
```

The tracked fixture hashes and full timing/command data are in the generated
ledger.  `artifacts/` is intentionally ignored because solver output is
reproducible and can become large.

## Pole-state realizability census

Status: **EXACT FINITE CENSUS / SEEDED DIAGNOSTICS / NO UNIVERSAL
THEOREM**.

The deterministic package
`search/pole-state-realizability-20260725/` canonically regenerates
terminal-distinct simple cubic multipoles and solves every \(D_5\)
boundary color-orbit.  Its extended ledger contains:

- 5,214 internally bridgeless five-poles through order 13, with state-set
  sizes \(46,56,57,58,60,61,62\);
- 298 sharp 46-state poles, every complete relation equal to one ordered
  \(C_5\)-cap relation;
- 69,243 internally bridgeless five-poles at order 15, every one reaching
  the 46-state threshold in a stopping census;
- 6,894 gluing-admissible five-poles through order 13 and no disjoint
  complete pair under any terminal permutation;
- 19,513 internally bridgeless four-poles through order 14, all with nine
  or ten boundary types; and
- seeded larger portfolios, explicitly separated from the exhaustive
  scopes.

Quick regeneration through five-pole order 11 and four-pole order 12
takes about 22 seconds on the recorded host:

```sh
python3 search/pole-state-realizability-20260725/verify.py --quick
```

The package ledger SHA-256 is
`c6d483fa89b736dbe8c22f9d693f699a084d050142b87b6a7325c5779def0e5e`.
Rejected boundary states trust CaDiCaL rather than retained per-query
UNSAT certificates.  The result is a reproducible finite census, not a
certified counterexample, a universal pole theorem, or a five-CDC
resolution.

The order-15 threshold transcripts and structural replay are frozen in
`search/five-pole-46-threshold-order15-20260727/`.  This run stops after
46 admitted states and therefore does not supply an exact order-15
profile.

A human scope correction in
`docs/five-pole-realizability-frontier.md` shows that universal nonempty
state relations for internally bridgeless five-poles would already imply
Five-CDC: replace one edge of a bridgeless cubic graph by a six-edge path,
use the five internal path vertices as terminals, and contract any pole
labelling back through the equality of its two endpoint labels.  The
reverse extension is explicit.  Therefore the proposed 46-state theorem
is stronger than the original conjecture and must not be presented as a
strictly easier auxiliary target.

## Required fields for search runs

Each substantive entry must record the UTC timestamp, git revision (or
explicit dirty-tree status), verifier hashes, generator and solver versions,
exact command, random seed (if any), graph domain, result counts, timeouts,
and artifact checksums.

## \(K_6\) switch-local-minimum certificates

Status: **EXACT FINITE FAILED-LEMMA CERTIFICATES / NO FIVE-CDC
COUNTEREXAMPLE**.

The branch first froze a 14-vertex Heawood flow with two defects and no
improving one-step switch in
`search/k6-defect-switch-20260725/`.  A neutral switch followed by a reducing
switch reaches zero defects, so the state is a local plateau rather than an
absorbing reconfiguration component.  Exact complete state audits on
\(K_{3,3}\) and Petersen are in
`search/k6-neutral-descent-exact-20260725/`.

Label-preserving 2-edge sums preserve switch-local minimality and add defect
counts.  The package `search/k6-defect-two-sum-20260725/` freezes the
connected four-defect instance and proves the factor-additivity lemma,
yielding connected examples with arbitrarily many even defects; these have
cyclic 2-cuts.

The stronger retained instance is
`search/k6-defect-snark-plateau-20260725/`.  It crosses two order-18 snark
flows to obtain a 36-vertex, 54-edge, girth-five graph with cyclic
edge-connectivity exactly four and defects
\(\{3,16,21,34\}\).  The full cycle space has dimension 19.  Exact counts of
admissible cycles by switch value are:

```text
t=3: 524288
t=5,9,12,30: 8192 each
t=15,18,20,23,27: 32768 each
t=6,10,17,24,29: 131072 each
```

For every value the minimum defect change is zero.  The independent
four-pole verifier reconstructs the full \(15\times8\) transfer table from
256 affine subsets in each boundary sector.  The graph metadata checker
finds no cyclic cut of size at most three and verifies the exhibited
four-cut.  The Tait CNF has 162 variables and 540 clauses; its 16,152-byte
LRAT is accepted by both retained checkers.  The independent
perfect-matching proof enumerates 208 matchings in 14,713 recursion nodes.
The explicit admissible trajectory

```text
4 -> 4 -> 2 -> 2 -> 0
```

uses switch values \(3,18,3,17\) and is checked edge by edge.  This
intermediate flow is certified as a six-coordinate double cover and
certified not to omit a \(K_6\)-star.  A fifth switch, value \(3\) on
edges \(8,9,15,16,20,29,47,48,50,53\), eliminates the coordinate-1
support and gives an explicit standard five-cycle double cover.

Run:

```sh
sh search/k6-defect-snark-plateau-20260725/verify_package.sh
```

The package-manifest SHA-256 is
`0a02548e3d9c70a25d4d02f6b8ca01b98d6ee1126514b3ffd56dec0396039a62`.
All search and documentation were produced with substantial disclosed
OpenAI Codex assistance.  The retained witness, proof certificates, and
independent source are the evidentiary basis.

## Petersen \(K_6\)-star defect barrier

Status: **EXACT FINITE FAILED-LEMMA CERTIFICATE / POSITIVE FIVE-COVER
ENDPOINT**.

The package `search/k6-petersen-star-barrier-20260725/` classifies all
\(2^{24}=16,777,216\) abstract Petersen flow states.  Of 6,093,360
nowhere-zero flows, 37,440 are triangle-only; 36,000 already omit a
\(K_6\)-star.  The remaining 1,440 split into two components of 720
under triangle-preserving constant-value cycle switches.

For the retained state, every one of the 15 duads occurs exactly once.
Its 15 triangle-preserving neighbors are exactly the global
transpositions of the six \(K_6\)-vertices.  They generate a free
\(S_6\)-orbit of size 720, which is the entire component and contains no
star-omitting state.  An independently written Python verifier reconstructs
the Petersen graph from literal edges, scans all \(2^{15}\) edge subsets
to recover its 64 binary cycles, checks all 945 nonempty value-cycle
switches, identifies the 15 transpositions, and generates all 720
permutations.

The sharp escape is

```text
0 -> 2 -> 0 defects
```

using value \(1\) on edge cycle \(0,1,2,3,4\), then value \(10\) on
edge cycle \(2,3,4,5,7,8\).  The endpoint omits star 5 and is an explicit
standard five-cycle double cover.  Defect parity proves that any escape
must reach at least two defects, so the displayed barrier is optimal.

Run:

```sh
sh search/k6-petersen-star-barrier-20260725/verify_package.sh
```

The package-manifest SHA-256 is
`66f20ac1b0e203914a0dc884d74c228e9e11c76db0f32327ee7bddba6983bb26`.
This is a counterexample to defect-monotone star reconfiguration, not to
the five-cycle double cover conjecture.

## Infinite Petersen-ring \(K_6\)-star barrier

Status: **INFINITE EXACT RECONFIGURATION THEOREM / POSITIVE FIVE-COVER
ENDPOINTS**.

The package `search/k6-petersen-ring-barrier-20260725/` deletes the
same label-\(\{0,1\}\) edge from each of \(n\) Petersen witnesses and
joins the resulting terminals in a ring with label-\(\{0,1\}\)
connectors.  The graph \(R_n\) is connected, simple, bridgeless, cubic,
and has \(10n\) vertices and \(15n\) edges.

For switch value \(t\), the crossing-label even subgraph \(Q_t\) is:

- \(n\) disjoint 8-circuits when \(t=\{0,1\}\) or \(t\) is disjoint
  from \(\{0,1\}\); and
- one \(8n\)-circuit when \(t\) meets \(\{0,1\}\) once.

The local triangle lemma proves that these component switches are all the
triangle-preserving moves.  Component states are uniquely the tuples
\((\sigma_1,\ldots,\sigma_n)\in S_6^n\) with a common image of the
connector duad.  Consequently the component has

\[
15\cdot|\operatorname{Stab}_{S_6}(\{0,1\})|^n
=15\cdot48^n
\]

states, every one using all 15 duads.  No state omits a star.  The result
is unchanged under the standard connected-circuit move convention.

The one-Petersen escape avoids the deleted edge, so it can be applied
blockwise.  The exact profile is \(0,(2,0)^n\), and the endpoint omits
star 5.  Defect parity and the trapped zero-defect component prove that
barrier two is optimal.

The two independent finite backstops completely scan all \(2^{11}=2048\)
binary cycles of \(R_2\), find exactly 29 nonempty triangle-preserving
switches at the initial state, generate the complete 34,560-state
component, and verify the path \(0\to2\to0\to2\to0\) and final standard
five-cover.

Run:

```sh
sh search/k6-petersen-ring-barrier-20260725/verify_package.sh
```

The package-manifest SHA-256 is
`403a0b6690f53497038ae6d4eb43eb6666b218e80fe65d544a960cd83b0d53fe`.
This theorem concerns the triangle-only stratum and does not claim that
the full nowhere-zero flow component is disconnected.

## Cotree-diamond connected-kernel separator

Status: **INFINITE EXACT SEPARATION / STANDARD FIVE-COVERS POSITIVE**.

The package
`search/connected-kernel-cotree-diamond-separator-20260725/` replaces the
six edges of a Petersen cotree by diamonds.  The resulting graph is simple,
bridgeless, cubic, and has 34 vertices and 51 edges.  Its canonical graph6
encoding is frozen in the package.

The human proof does not use SAT.  In a connected-kernel
\(\mathbb F_2^3\)-flow, conservation over a diamond makes its two attachment
values equal, and kernel connectivity forces that value into the selected
Fano line.  Contracting the diamonds gives a Petersen flow whose
outside-line support is an even edge-subset of the complementary spanning
tree, hence empty.  This would be a proper Petersen 3-edge-colouring,
contradicting its six explicitly listed odd complementary two-factors.

A local duad rule independently lifts a Petersen five-cover through all six
diamonds.  The retained coordinate sizes are \(30,30,17,16,9\), and both
frozen target verifiers accept the model.  Two independently structured
package checkers reconstruct this lift from literal data.

The 153-variable connected-kernel relaxation has 465 clauses: 459 flow
clauses and six necessary diamond-shore connectivity clauses.  Its
20,031-byte LRAT is accepted by both `lrat-check` and CakeML `cake_lpr`.
Run:

```sh
sh search/connected-kernel-cotree-diamond-separator-20260725/verify_package.sh
```

The package-manifest SHA-256 is
`d65e11007860ac98306847915c96c3353932e42e88b4ccb5f92d6487bb6280b7`.
Iterating the construction gives orders \(10,34,106,322,\ldots\), an
infinite family with ordinary five-covers and no connected-kernel flow.
This refutes only the stronger connected-complement normal form and is not
a counterexample to five-CDC.

## Weighted \(T\)-join minima countermodel

Status: **EXACT INTERMEDIATE FAILED-LEMMA CERTIFICATE / NONMINIMUM
SUPPORT**.

The package `search/tjoin-weighted-minima-countermodel-20260725/` freezes a
22-vertex, 33-edge simple connected bridgeless cubic graph with a displayed
size-three exact-zero matching.  The complement is connected and
terminal-even, every one of the three color-weighted \(T\)-join minima is
exactly three, and all three minimum-zero quotient multigraphs are forests.
Nevertheless, exhaustive enumeration of all 512 \(T\)-joins finds no
edge-disjoint pair.

The human obstruction is a four-cycle containing exactly three of the six
marked core edges.  Parity forces it to be an entire component of every
binary cycle containing all marks, violating the even-marked circuit
criterion equivalent to two-\(T\)-join packing.  Independently structured
Python and JavaScript checkers reconstruct the graph, cost matrices,
quotients, cycle obstruction, and exhaustive join list.  They also exhaust
all cuts of size at most three and confirm cyclic 4-edge-connectivity.

Run:

```sh
sh search/tjoin-weighted-minima-countermodel-20260725/verify_package.sh
```

The package-manifest SHA-256 is
`f1bebcc0e86530a6d5de9f115b3e3117a88d11821d0d45f5b36a1f243a5a8a5a`.
An explicit nowhere-zero flow proves that the displayed support is not
globally minimum, and the graph has girth four.  Thus the package refutes
only the attempted sufficiency of the two derived minimum-support
conditions; the actual reduced-domain minimum-support exchange theorem
remains open.

## Fixed-join preparation trap

Status: **FAILED UNIVERSAL LEMMA / EXACT HUMAN-CHECKABLE COUNTERMODEL**.

The package `search/fixed-join-preparation-trap-20260725/` freezes a
38-vertex, 57-edge simple connected bridgeless cubic graph obtained by
replacing two edges of an 18-vertex base with Petersen 2-poles.  Its
displayed binary cycle has a two-component complement and contains exactly
125 inclusion-minimal exact \(\mathbb F_2^2\)-flow zero sets.  Their size
profile is 100 of size three and 25 of size four; every one has preparation
minimum two.

The primary checker factors the enumeration into the 1,024 base cycles and
the 4,096 local flows of each restored pole.  The independent checker builds
the expanded cycle space from scratch and scans all
\(2^{20}=1,048,576\) cycles.  It independently recovers the 125 supports,
finds 953,312 cycles containing at least one, and finds no connected
complement.  Projection of a hypothetical connected spanning odd factor
through both poles gives the human contradiction described in the package
README.

Both target verifiers accept the explicit standard five-cover with
coordinate sizes \(27,27,21,19,20\).  The graph's two nontrivial two-edge
cuts place it outside the reduced cyclically 4-edge-connected domain.  The
result refutes the unrestricted preparation lemma only.  The package
manifest SHA-256 is
`4d732e47f5e87c35492410228acf1b59e969560e229d47f50461c152db1bb775`.

## Minimum-support strict-switch local plateau

The exact package
`search/minimum-switch-local-plateau-20260725/` freezes the first
switch-local nonpacking flow found by the canonical primary census.  Its
16-vertex graph has graph6 string `O???EA_E@IGcW_c_BO?W_`, 24 edges, cycle
space size 512, and initial exact zero edges \(\{2,13\}\).  The primary and
independent verifiers agree on:

- 128 affine \(T\)-joins and zero disjoint pairs;
- eight binary cycles containing every required terminal-incident edge,
  none satisfying the even-marked circuit criterion;
- zero strictly decreasing matching-admissible switches;
- the neutral-descent profile \(2\to2\to1\); and
- an explicit final packing cycle of bit mask `972523`.

The exact primary census totals are:

| order | hard graphs | distinct supports | nonpacking supports | local-minimum nonpacking signatures | minimum nonpacking supports |
|---:|---:|---:|---:|---:|---:|
| 10 | 1 | 301 | 191 | 0 | 0 |
| 12 | 1 | 874 | 617 | 0 | 0 |
| 14 | 5 | 12,569 | 9,285 | 0 | 0 |
| 16 | 26 | 187,421 | 146,097 | 64 | 0 |

The order-16 local plateaus occur on six graphs.  Their complete ordered
flow-state graphs restricted to matching supports of size at most two all
connect to size-one states.  This finite result refutes only strict
single-switch descent; it does not refute the minimum-support conjecture or
five-CDC.  The package-manifest SHA-256 is
`17eb426b9f8311e5af4d8247f1c4025f8fe730f74425cd3242c15dda87895d0f`.

The follow-up exact reconfiguration package
`search/minimum-switch-neutral-components-n16-20260725/` builds the full
state graph induced by ordered flows whose matching exact-zero support has
size one or two on the six plateau hosts.  Primary Python and independent
JavaScript implementations agree on 33,546 states and 384 strict local
plateaus.  A multi-source breadth-first search from all size-one states
reaches the entire sublevel graph, and every plateau has distance exactly
two.  Its package-manifest SHA-256 is
`7d0bb2fc8497bde97e4a205d0676e0db9496da61b790d606ad4450ecacb17d02`.

The complete hard order-18 extension is in
`search/minimum-switch-neutral-components-n18-20260725/`.  Its primary C++
checker and independent NumPy checker agree on every retained field for all
179 graphs:

| quantity | exact count |
|---|---:|
| ordered support-\(\le2\) states | 1,680,414 |
| graphs with local plateaus | 56 |
| strict local nonpacking plateaus | 7,704 |
| unreachable states | 0 |
| unreachable plateaus | 0 |
| plateau distance from size one | 2 |

The state-graph construction uses the proved three-bucket adjacency lemma
rather than checking all \(3\cdot1024\) switches separately at each state.
The source graph6 list was previously frozen as the complete hard order-18
control.  The package-manifest SHA-256 is
`13ef63605817255cb1e27cd803b832498c98a3a9dd4118cf8a7ec7f74f83096f`.

The complete hard order-20 extension is in
`search/minimum-switch-neutral-components-n20-20260725/`.  Its primary C++
and independent NumPy implementations agree on every retained field for all
1,388 hard graphs:

| quantity | exact count |
|---|---:|
| ordered support-\(\le2\) states | 20,161,044 |
| graphs with local plateaus | 589 |
| strict local nonpacking plateaus | 118,134 |
| unreachable states | 21,492 |
| unreachable nonpacking states | 0 |
| unreachable plateaus | 0 |
| plateau distance from size one | 2 |

The unreachable states constitute the entire state space of the unique
minimum-size-two graph and all pack two \(T\)-joins.  Thus every nonpacking
state reaches size one on this finite boundary.  The package-manifest
SHA-256 is
`9cfc63ef7c4883bf5b18758e800b3b28c6d565cb6a5832c810e92be447174393`.

The next exact package,
`search/minimum-switch-packing-components-n22-20260725/`, covers the seven
hard order-22 graphs whose minimum exact-zero matching size is two:

| quantity | exact count |
|---|---:|
| ordered minimum states | 190,512 |
| distinct minimum supports | 1,441 |
| nonpacking minimum supports | 15 |
| nonpacking ordered states | 2,808 |
| unreachable nonpacking states | 0 |
| maximum distance to packing | 1 |

The 15 supports occur on two graphs and refute “every minimum support
packs.”  Both implementations find every nonpacking realization one
neutral switch from a packing state.  The package-manifest SHA-256 is
`0532c24206dd4fd10aa159227680d6296e707e285a1d09d921591920e7ae299a`.

The minimum-size-three continuation is
`search/minimum-size-three-packing-components-20260725/`:

| quantity | exact count |
|---|---:|
| globally minimum supports | 366 |
| packing minimum supports | 290 |
| nonpacking minimum supports | 76 |
| ordered minimum flow states | 3,670,272 |
| global-colour orbit states | 611,712 |
| nonpacking orbit states at distance one | 170,352 |
| nonpacking orbit states at distance two | 720 |
| unreachable nonpacking orbit states | 0 |

The graph is the 42-vertex global component-parity countermodel.  Both
implementations prove that every minimum neutral component contains a
packing state, but the 720 distance-two orbits refute the stronger
one-switch claim.  All 720 use support \(\{20,30,53\}\); a separate
Gaussian-elimination checker exhausts its 8,192 eligible even subgraphs,
proves their odd-marked-component obstruction, and checks a literal
two-switch path to packing.  The package-manifest SHA-256 is
`0a36bd4b1f70cd4288e60a4b677aead723efeef7acc90b5037909d36098b299d`.

## Connected Fano one-switch composition diagnostics

Audit date: **2026-07-26**.

The initially stated Fano one-switch conjecture needs connectedness.  Two
disjoint copies of the exact ten-vertex bad-flow block remain bad after
every single circuit switch, because a circuit lies in one component and
the untouched bad component blocks every value.  This is a semantic
countermodel to the disconnected formulation only; five-covers combine
coordinatewise across components.

The first connectedization test is frozen in
`search/fano-bad-flow-two-sum-20260726/` and produced by
`scratch/fano_bad_flow_two_sum_search.py`.  It deletes one edge from each
copy of the bad block, applies every aligning element of
\(\mathrm{GL}(3,2)\) to the second flow, and reconnects the four ends in
both possible pairings.  The exact output has:

| quantity | count |
|---|---:|
| connected two-edge-sum flows | 10,800 |
| initially bad | 10,800 |
| one-circuit repairable | 10,800 |
| switch-local bad | 0 |

Thus the obvious connected two-sum does not preserve the disconnected
obstruction.  A thirty-vertex identity three-block chain is also bad and
one-circuit repairable.  The deterministic seed-20260726 sample in
`scratch/fano_bad_flow_three_chain_search.py` tests 100 independently
chosen ordered port quadruples and aligning linear relabellings; all 100
flows are initially bad and all 100 have a one-circuit repair.  These are
structured diagnostics, not canonical graph censuses and not universal
proofs.

The universal connected statement is nevertheless false.  The minimized
certified composition in
`search/connected-one-switch-countermodel-40v-20260726/` uses a
ten-vertex Tait base with three monochromatic edges on no common circuit.
Replacing those three edges by flow-aligned two-sums with the ten-vertex
bad block gives:

| quantity | count |
|---|---:|
| vertices | 40 |
| edges | 60 |
| attached bad blocks | 3 |
| standard five-cover coordinate sizes | 40; 40; 40; 0; 0 |

The independent checker reconstructs all three two-sums, verifies
simplicity, connectivity, cubicity, every single-edge deletion, all flow
equations, all seven bad-block graft obstructions, and the explicit
positive three-cover.  It enumerates all 30 base circuits and all 6,780
final circuits, directly confirming that every final circuit leaves a
bad block untouched.  The short human proof uses two forced-triangle
arguments.  This is a countermodel to the one-switch lemma only, not to
five-CDC.  The earlier 2,614-vertex \(H_5\)/LRAT package remains a valid
superseded construction.

## Fixed-flow Fano pure-merge and one-circuit repair

Audit date: **2026-07-26**.

`tools/fixed_fano_cover_merge_audit.py` now enumerates the affine space of
Oum-compatible vertex potentials for a supplied fixed
\(\mathbb F_2^3\)-flow.  It tests both the restrictive merge of three
disjoint coordinate pairs and the exact broader criterion: proper
five-colorability of the coordinate co-occurrence graph.

On the old 112-vertex supplied-cover \(K_8\) obstruction, changing the
compatible cover while retaining the fixed flow makes 380 of the 420
three-pair merges satisfiable; only 40 are unsatisfiable.  Thus internal
cover freedom repairs that supplied-cover example.

The complete fixed-flow frontier for connected simple bridgeless cubic
graphs through order 10 checks 26 graphs and 3,295
\(\mathrm{GL}(3,2)\)-flow orbits with no fixed-flow obstruction.  At order
12, graph `K??FEaKR@oE_` has a flow with one gauged potential solution and
15 used pair types forming \(K_6\).  The port-deleted system has 37 scalar
equations, rank 36, and the unique gauged potential

```text
0 5 5 1 5 6 7 4 7 3 7 2.
```

Its internal labels plus dangling port label 13 are all 15 pairs on
`0 1 2 3 4 6`.

The restricted one-circuit repair frontiers gave:

| corpus | flow orbits | pure-merge bad | unrepairable |
|:---|---:|---:|---:|
| complete order 12 | 73,152 | 351 | 0 |
| complete order 14 | 2,216,590 | 20,676 under the three-pair criterion | 0 |
| 26 hard order-16 graphs | 600,440 | 7,385 | 0 |
| first matching-bad hard order-18 flows | 164 tested | 16 | 0 |

These positive frontiers motivated the composition test but are not
universal evidence.

The exact 46-vertex composition is frozen in
`search/fano-pure-merge-one-switch-countermodel-46v-20260726/`.  The
starting fixed flow has 128 gauged compatible potentials: 32 use 15 pair
types, 96 use 24, and every co-occurrence graph has clique number at least
six and is not five-colorable.  A discovery SAT encoding found all seven
connected switch-value instances UNSAT, with 9,551--9,807 variables and
89,662--118,558 clauses.  The retained theorem does not rely on those SAT
answers: potential rigidity plus base-edge noncyclability gives a direct
human proof.

An arbitrary disconnected binary-cycle switch is stronger than the stated
one-circuit operation and can repair the composition for switch values
1, 2, 6, and 7.  The value-1 witness is the union of one six-cycle in each
rigid cap.  This confirms that connectedness is essential to the exact
countermodel and that multiple local repairs remain possible.

A first seeded reduced-domain probe uses
`scratch/fixed_fano_pure_merge_strict_sampler.py`.  It is a random sample,
not a flow-orbit census.  On all 20 retained strict order-22 snarks it
accepts 2,000 distinct nowhere-zero flows per graph: 7,444 of 40,000 are
pure-merge bad, and every one has a legal connected-circuit repair.  On all
38 retained strict order-24 snarks it accepts 1,000 flows per graph: 8,967
of 38,000 are pure-merge bad, and again every one is repairable.  The
frozen outputs are
`scratch/fixed-fano-pure-merge-strict22-sample2000.json` and
`scratch/fixed-fano-pure-merge-strict24-sample1000.json`.  These samples
support only the surviving cyclically 4-edge-connected one-circuit
formulation; they do not prove it or independently certify source-list
completeness.

The 2026-07-28 extension samples 500 flows on each of the seven retained
order-34 strong snarks and on the unique retained
girth-at-least-six snarks of orders 28, 30, and 36.  Among these 5,000 new
flows, 2,245 are pure-merge-bad and every one has a checked
connected-circuit repair.  The order-34 replay independently checks the
source hash, graph premises, retained potential spaces, \(R_5\)
obstructions, and repair witnesses in
`scratch/audit_strict_oum_one_switch_20260728.py`.  All flow selections
remain seeded samples, not complete flow-orbit censuses.

The same audit proves a useful exact collapse: for every graph \(H\) on at
most eight vertices,
\[
 H\to R_5\quad\Longleftrightarrow\quad\chi(H)\le5.
\]
The only 6-critical cores possible at this order are \(K_6\) and
\(K_3\vee C_5\), and neither maps to \(R_5\).

The proposed Knappe--Pitz closure after deleting one value matching is
false.  The canonical order-18 package
`search/fano-circuit-avoidance-countermodel-18v-20260728/` has a
merge-bad flow on the first Blanuša snark for which \(G-M_6\) is connected
and bridgeless.  Three value-3 edges have no common circuit, certified by
a two-vertex separator, although no odd cut is contained in the triple.
The disjoint union of a five-cycle and six-cycle through those marks is a
legal value-6 binary-cycle switch and changes all four compatible
\(K_6\) covers into five-colourable covers.  An independent
standard-library checker verifies 1,024 binary cycles, 692 elementary
circuits, 17 circuits avoiding \(M_6\), four initial potentials, four
repaired potentials, and a 28,560-flow Petersen minimality control.  A
different connected six-circuit repairs the same starting flow, so the
unrestricted reduced existential claim remains open.

## Order-22 four-mark separation/nonpacking screen

`scratch/tait_all_coloring_mark_separation.cpp` was run on all 7,319,447
rows of the frozen complete canonical connected simple cubic order-22
corpus with target four, cyclic edge-connectivity at least four, and the
nonpacking requirement enabled.  It enumerated 95,360,112 proper
three-edge-colourings modulo global colour permutation on 7,174,735
colourable rows.  It found zero hosts with a four-edge matching that is
simultaneously:

1. separated on every bichromatic circuit in every Tait colouring; and
2. excluded by the exact even-marked circuit packing criterion.

The input, source, empty witness stream, command, and exact counts are
bound in
`scratch/order22-cyclic4-separated4-nonpacking-result.json`.  This is a
finite negative screen only.  The minimum-counterexample branch already
has order at least 88 by the later monochromatic-mark girth lemma, so no
universal marked-core conclusion follows.

The host-only cyclic-connectivity proxy in the first version of this
screen has since been replaced by the exact marked lift condition
\[
 |\delta_H(X)|+|S\cap E(H[X])|\ge4
\]
for every cyclic shore \(X\).  The proof that this is forced by cyclic
4-edge-connectivity of the ambient two-component lift is in
`docs/marked-core-cyclic-lift-condition.md`.  Rerunning the complete
order-22 corpus with this exact condition again produced zero witnesses.

A 44-vertex four-mark countermodel shows that the marked cut hypothesis
cannot be dropped: all 5,832 Tait colourings separate its marks and all
524,288 cycles containing the marks have an odd marked-component profile,
but three cyclic two-edge cuts each isolate one mark and violate the
exact inequality by \(2+1<4\).  Its canonical encoding and complete
profile counts are frozen in
`scratch/four-mark-lowcut-countermodel-44v-result.json`.

Finally, all 13,824 tested three-edge-sums of two copies of the stable
order-20 separated-triple core were screened over all retained mark-pair
choices, allowed deleted vertices, and six boundary bijections.  There
were 288 universally separated marked instances and no instance
simultaneously satisfying the exact marked cut condition and the
nonpacking criterion.  A nine-circuit certificate now proves directly
that every permitted factor pole has a closed admissible state, so every
one of these 13,824 three-sums packs irrespective of the marked cut and
Tait-separation tests.  This is a theorem for the stated construction
family, not a universal three-cut reduction; the local compatibility
implication for arbitrary poles remains open.  The exact
seven-state boundary-signature gluing theorem, frozen generator, command,
and hashes are in `docs/marked-three-edge-cut-signatures.md` and
`scratch/marked-three-sums-13824-result.json`.

The same signature analysis now gives a universal low-cut reduction.  A
bridge-component count proves that any two- or three-pole with distinct
boundary ends, exactly two internal marks, and the exact marked cut
inequality has a closed circuit through both marks.  It follows that a
nonpacking four-mark core satisfying the exact inequality has no cyclic
two-edge cut.  It also cannot have an unmarked cyclic three-edge cut with
a \(2+2\) mark distribution.  Complete cubic-cap screens through order
14 independently found only signatures containing the closed state
(36,070 eligible marked poles through order 12 and 282,734 at order 14);
these counts are supporting diagnostics, not the proof.  A second
bridge-component argument proves that the one-mark shore of an unmarked
\(1+3\) cyclic three-cut has all three odd open states.  Thus only the
three-mark shore remained in that isolated local formulation; marked
boundary cuts were also open at this checkpoint.  Both obligations are
superseded by the later global proof draft in
`docs/four-mark-core-closure.md`.

## Exhausted \(H_4\) minimum-support enumeration

Audit date: **2026-07-26**.

The incremental \(H_4\) master solver exhausted after enumerating exactly
4,931,430 distinct globally minimum size-four supports.  Every support
admits two edge-disjoint \(T\)-joins; none is nonpacking.  The final
increment contained 5,794 supports beyond the 4,925,636-row checkpoint.
Four-field row parsing, global duplicate detection, exact old-prefix
matching, and witness replay passed.  The retained corpus SHA-256 is
`a7ede3be51d3b937bacf702d67aa51431192bcdea9b008bf835e25f82967b483`;
metadata are in
`scratch/checkpoints/h4-minimum-supports.snapshot.json`.

The terminal exhaustion has now been independently proof-certified.  A
fresh blocking formula contains 1,697 variables and 4,936,112 clauses:
4,682 base clauses and 4,931,430 support-blocking clauses.  CaDiCaL 3.0.1
proved it UNSAT and emitted a 973,056,379-byte textual LRAT.  The
independent C `lrat-check` reports `c VERIFIED`, and the verified CakeML
`cake_lpr` reports `s VERIFIED UNSAT`.  The frozen CNF and LRAT are
`search/h4-all-minimum-support-packing-20260726/all-supports-blocked.cnf`
and
`search/h4-all-minimum-support-packing-20260726/all-supports-blocked.lrat`;
their SHA-256 values are
`12061f07adc80081c6c329b1882201a734d004445a1e84d493f9bd7cd3743741`
and
`6bdeaff7fe3f37dca1c34c6653f0d1f1477490ffdd50f2d954fd88cc2c649934`.

The positive side is now independently frozen as well.
`packing-witnesses.bin` has 31 bytes per row and 152,874,330 bytes in
total; its SHA-256 is
`040fd474e7f3dfae0e530eed5579a4892bafcada1cbf0f85418393e3cbd297c3`.
Each record is a 243-bit binary cycle through all support endpoints, with
an even number of endpoints on every circuit component.  The independently
written, solver-free checker validates the graph, proves every support row
distinct, and replays the elementary even-marked-circuit criterion on all
4,931,430 rows.  It reports
`VERIFIED rows 4931430 distinct 4931430 packing_witnesses 4931430`.
The complete package is
`search/h4-all-minimum-support-packing-20260726/`; its manifest SHA-256 is
`ce247fb04a4a5a02c1d7e872cf3131447b90f568638340584dd5ebeb4a03f385`.
Thus every minimum exact-zero matching of this fixed \(H_4\) extends to a
standard five-cycle double cover.  This is a finite fixed-graph theorem,
not a universal claim.

## One-mark three-pole theorem and order-20 signature audit

Audit date: **2026-07-26**.

The bridge-component argument in
`docs/marked-three-edge-cut-signatures.md` proves that a one-mark
three-pole satisfying the exact marked cyclic-cut inequality and having
three distinct boundary ends realizes all three odd open boundary
states.  This is a human proof and does not depend on enumeration.

The complete order-20 connected simple cubic corpus has 510,489 rows, of
which 496,430 are Tait-colourable.  The target-three universal-separation
screen found 183 host witnesses.  Passing those caps to
`scratch/analyze_separated_triple_poles.py` produced 427 eligible poles:
every one had signature size three and there were no incomplete
signatures.  Together with the order-16 and order-18 audits, all 601
eligible poles tested have the full three-state odd signature.  This
finite audit does not prove the remaining universal assertion for the
three-mark shore of a \(1+3\) cut.

## Cyclically four-edge-connected separated-triple frontier

Audit date: **2026-07-26**.

The exact target-three conflict-graph screen was rerun with ordinary
cyclic edge connectivity at least four on the complete order-22
canonical connected simple cubic corpus.  It decoded 7,319,447 rows,
found 7,174,735 Tait-colourable rows, enumerated 95,360,112 Tait
colourings modulo global colour permutation, and found no universally
separated three-edge matching.  Input, source, binary, command, counts,
and SHA-256 values are frozen in
`scratch/order22-cyclic4-separated3-result.json`.

At order 20, imposing edge connectivity three leaves exactly two hosts
with a universally separated triple, and both have a cyclic three-edge
cut splitting the marks \(1+2\); every remaining order-20 host witness
has a cyclic two-edge cut.  This motivated a low-cut exposure conjecture,
which the order-24 construction below now refutes.

A first cyclic-four-cut construction test uses the earliest order-20
cyclically-4 host with a universally separated pair as one factor and
\(K_4\) as the other.  It deletes every eligible independent edge pair
on both sides, tries all retained \(K_4\) mark edges and all 24 boundary
bijections, and emits 93,888 labelled order-24 graphs.  Every required
triple is defeated by an explicit Tait colouring; none remains
universally separated.  The generator, exact stream hash, command, and
counts are frozen in
`scratch/separated-pair-k4-four-sums-result.json`.  This rules out only
that structured four-sum construction.

The factor screen was then completed over **all** 250 cyclically
four-edge-connected order-20 hosts with a universally separated pair.
Exact all-colouring enumeration found 934 literal separated pairs, or
789 marked-host automorphism orbits.  Quotienting eligible host port pairs
by the marked stabilizer leaves 233,670 orbits; \(K_4\) contributes three
boundary-bijection orbits.  Thus the factorwise-complete stream has
701,010 order-24 rows.  Only the inherited pair was fixed, and the checker
searched every edge as a possible third mark.

There are 144 positive rows: 142 distinct emitted graph6 records, 20
unmarked graph isomorphism classes, and 46 marked-graph isomorphism
classes.  The first is the nonplanar graph

```text
W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E
```

with marks \(01,23,20\,23\).  A clean-room standard-library verifier
independently enumerates all 36 Tait colourings modulo global colour
permutation, checks every bichromatic component, tests all edge-deletion
sets of size at most three, and finds a cyclic four-edge cut.  The exact
construction, complete hit stream, hashes, and verifier are frozen in
`search/cyclic4-universally-separated-triple-n24-20260726/`.

Consequently the low-cut exposure conjecture is false: a universally
separated triple can occur in a cyclically \(4\)-edge-connected
Tait-colourable simple cubic graph.  This affects the structural
diagnostic only; the later four-mark closure proof bypasses that
conjecture.  Moreover every one of the 144 hits has girth four and
marked-subdivision girth five.  Hence zero satisfy the connected-branch
condition \(|C|+|C\cap S|\ge10\) for every circuit.  The two-count
difference between 144 hits and 142 literal rows comes from exactly two
duplicate construction pairs, each producing the same literal graph and
same marked triple; it is not a verification discrepancy.
The full 701,010-row stream was independently rerun with the exact
`--min-subdivided-girth 10` filter and produced zero witnesses, so no
alternative third mark repairs a displayed \(K_4\) sum.

## Monochromatic-mark girth bound

Audit date: **2026-07-26**.

The mark-precolouring lemma yields a finite-search-independent
improvement for the size-four extremal branch.  After deleting a
four-edge matching and suppressing its eight endpoints, precolour all
eight marked core edges with one Tait colour.  Universal separation
puts the marks on eight pairwise vertex-disjoint bichromatic even
circuits, exactly one mark per circuit.  Undoing suppression turns these
into eight pairwise vertex-disjoint odd circuits in the ambient graph.
Ambient girth at least ten makes every one have length at least eleven,
so the ambient graph has at least 88 vertices.  The complete proof and
scope discussion are in
`docs/kempe-transversality-and-eight-mark-girth.md`.  No enumeration is
used in this bound.

## Unrestricted three-pole diagnostic

Audit date: **2026-07-26**.

`scratch/search_unrestricted_triple_poles.py` removes the universal Tait
separation hypothesis and enumerates every three-edge matching and every
eligible cap vertex.  It checks the inherited marked cyclic-cut
inequality and exhausts the binary cycle space for an admissible odd
open state.

On the complete connected simple cubic corpora it found:

| order | graphs | Tait graphs | eligible poles | empty odd signatures |
|---:|---:|---:|---:|---:|
| 8 | 5 | 5 | 360 | 0 |
| 10 | 19 | 17 | 6,446 | 0 |
| 12 | 85 | 80 | 86,086 | 0 |
| 14 | 509 | 475 | 1,109,842 | 0 |

Before the Tait-colourability filter was added, the order-12 graph
`K?ABCiWFBOKO`, cap vertex 6, and marks
\((0,5),(3,7),(4,8)\) gave an empty odd signature.  The cap has no Tait
colouring, so it is outside the marked-core hypotheses.  These counts
are exploratory finite evidence only; they are not used in the new
global proof.

## Four-mark core closure theorem

Audit date: **2026-07-26**.

`docs/four-mark-core-closure.md` gives a new human-checkable proof
of the universal marked-core theorem.  The decisive imported facts are
Knappe--Pitz \(g(3)=3\), the canonical cubic 3-sum decomposition of
Nedela--Seifrtová--Škoviera, and the
Aldred--Ellingham--Hemminger--Holton cycle theorem for four independent
edges in a quasi \(4\)-connected graph.

The proof reduces marked cyclic three-cuts directly.  In a surviving
nonpacking graph, every decomposition cut is unmarked and splits the
four marks \(1+3\).  A weighted-tree argument selects a central
cyclically \(4\)-edge-connected factor; all other incident components
are one-mark shores.  Universal separation precolours the four marks
with one Tait colour.  In the central factor, the internal marks and the
same-colour cap edge at each one-mark branch form a matching of at most
four distinct edges: adjacent cap roots can share their selected edge.
Aldred handles the four-edge case and Knappe--Pitz handles the smaller
case.  A cycle through the selected set, with the one-mark paths
substituted at its cap vertices, becomes a circuit through all four
marks.

An independently prompted Codex referee agent audited the argument and
reported that the stated binary-cycle theorem is sound.  The audit
correctly limits the strengthening: an unmarked \(2+2\) cut can yield
two two-mark circuits, so the theorem does not unconditionally give one
four-mark circuit.  This remains an AI-agent audit rather than
independent human verification or peer review.  The theorem eliminates
the size-four/two-component marked-core branch, not the full
five-cycle double cover conjecture.

## Connected stable-eight paired-cut clean-room audit

Audit date: **2026-07-26**.

The paired lift formula for a connected eight-mark core was checked by a
second implementation in
`scratch/audit_stable8_paired_cuts_cleanroom.py`.  It does not import or
execute the original checker.  It decodes the graph6 core, enumerates all
edge-deletion sets of sizes one through three, tests all unions of
deletion components for cyclic shores, independently generates the 105
perfect pairings, brute-forces every flexible boundary assignment, and
directly constructs the lifted cuts.

The audit reports `PASS_EXACT_MATCH`.  The core is simple, connected,
cubic, and bridgeless, with an eight-edge marked matching.  There are
exactly 49 cyclic cuts below four: seven of size two and 42 of size three.
All 105 pairings fail the paired-cut condition.  The minimum-score
histogram is
\[
      2:27,\qquad 3:78.
\]
All 777 retained violation records and all 5,355 direct lift checks agree.
The checker also reconstructs the first expansion exactly and independently
solves the binary parity system for a 44-edge cycle-space element containing
all eight marks.

The proof audit confirmed the lift formula, the pairwise boundary
optimization, the all-one cycle-space argument, and the stated
decomposition-tree consequence.  It corrected one non-material sentence:
a cyclic bridge forces at least three strict pairing crossings, not all
four.  The finite result excludes only this retained core and its
pairings.

## Eight-mark bichromatic incidence code

Audit date: **2026-07-26**.

`docs/eight-mark-bichromatic-code.md` gives an exact code/flow
formulation after all eight marks are precoloured \(c\).  Vertices of a
connected bipartite multigraph \(\Gamma\) are the \(ac\)- and
\(bc\)-circuits; its edges are the \(c\)-edges.  Universal separation
makes the eight marks a matching in \(\Gamma\).  Symmetric differences
of selected bichromatic circuits form an injective linear code, with
\(c\)-trace equal to a cut of \(\Gamma\), and the all-mark selectors form
an affine space of dimension \(|V(\Gamma)|-8\).

For a fixed selector, componentwise even marked parity is equivalent to
balance of the signed selected 2-factor, existence of a binary vertex
potential, or trivial voltage holonomy.  When the selector is variable,
the exact joint condition is quadratic.  The displayed order-12
graph6 example `K??FEagT@WB_` supplies three good all-mark selectors whose
affine triple sum is bad, proving that no purely linear selector code,
even after existential linear projection, captures the condition.
Neutral flow switches are exactly Kempe switches and generally mutate
the incidence graph rather than act inside one fixed code.  This is an
algebraic reduction, not a closure of the connected eight-mark branch.

## Stable-eight factor-quotient diagnostic

Audit date: **2026-07-26**.

`scratch/stable8_factor_quotient_diagnostic.cpp` reconstructs the retained
order-60 stable-eight core, the first terminal pairing, the all-\(c\)
colouring, its lifted \(ac\)-factor, and the contracted complementary
quotient.  The ambient expansion has 68 vertices and 102 edges.  The
factor has lifted lengths
\[
       17,13,5,9,5,5,9,5,
\]
and the quotient has eight vertices, 30 edges, and nine loops.

Two exact computations give
\[
 14\,801\,616\,000
\]
ordered edge-disjoint quotient-\(T\)-join pairs.  Zero pairs satisfy the
four-state local lifting test at all eight factors.  Every obstruction
mask contains factor zero, and all 128 masks containing it occur.  The
smallest displayed local obstruction is on a lifted 5-cycle with state
counts \((2,1,1,1)\).

A separate enumeration of all \(2^{23}=8\,388\,608\) core cycles with
all marks present finds zero having even marked count on every component.
The quotient-pair and direct-cycle computations therefore agree exactly.
A clean compilation and rerun produced a byte-identical result with
SHA-256
`4a2be7f9455ea3258df2d08055e988eef382b703abd5006888059912a52f41f4`.
The core fails every one of the 105 paired-cut choices, so it is outside
the surviving branch.

## Order-80 cubic vertex-transitive control

Audit date: **2026-07-26**.

The graph6/sparse6 conversion of the Potočnik--Spiga--Verret census,
commit `68c592d4790ab1737f04d86d3102c4999bbc6c09`, contains exactly 33
cubic vertex-transitive graphs of order 80.  The census file hash is
`4bac89beec1465265318266117c38a2c1680e73a21efd322411207cef5313088`.

Only eight rows have girth at least seven.  Seven have girth eight.  For
each, summing the requirement that every eight-cycle contain at least two
marks exceeds the maximum total incidence contributed by any eight
edges:

| Index | Eight-cycles | Required | Capacity |
|---:|---:|---:|---:|
| 3 | 40 | 80 | 32 |
| 4 | 40 | 80 | 32 |
| 20 | 10 | 20 | 8 |
| 21 | 10 | 20 | 8 |
| 28 | 20 | 40 | 16 |
| 32 | 80 | 160 | 48 |
| 33 | 40 | 80 | 32 |

The remaining index 30 has girth ten.  Exhaustive enumeration of all
426,256 Tait colourings modulo global colour permutation finds zero
universally separated eight-edge matchings.  The exact input and
reproduction commands are in
`docs/order80-vertex-transitive-control.md`.  This is a finite
vertex-transitive control, not a complete order-80 census.

The same graph has 20 normalized Tait colourings in which all three
bichromatic factors consist entirely of \(C_{10}\)'s.  For each of the
60 choices of common factor colour, there are exactly 1,249
factor-transversal eight-edge mark sets.  The exhaustive scan therefore
checks 74,940 records and 19,184,640 selectors.  Every record has a good
selector; the number ranges from 94 to 138, with 8,208,840 good
selectors in total.  A clean rerun is byte-identical and an independent
isomorphism-based implementation reproduces all 60 cases and the full
profile histogram.

## Equality incidence rotation countermodel and rooted cap control

Audit date: **2026-07-26**.

The decorated incidence certificate in
`scratch/equality88-rotation-countermodel-result.json` reconstructs a
simple connected order-80 Tait core with eight marked \(C_{10}\)'s in
each of two factors and zero good factor selectors among all 256.
Independent C++ and Python implementations agree.  The core has girth
three, fails universal separation after an explicit Kempe switch, and
its marked subdivision has checked edge-disjoint terminal joins of sizes
32 and 40.  It excludes the incidence-only implication, not the
five-CDC conclusion or the equality branch under its full hypotheses.

The rooted countermodel frozen in
`scratch/rooted-four-mark-countermodel-result.json` has order 28,
162 normalized Tait colourings, 2,048 all-mark binary cycles, 1,024
root-avoiding all-mark cycles, 360 componentwise-even all-mark cycles,
and zero cycles satisfying both conditions.  Its exact \(3+1\) cyclic
2-cut explains the obstruction.  It fails the marked-cut inequality
with value \(2+1=3\) and has marked-subdivision girth five.  A complete
simple-cubic screen through order 20 found no universally separated
four-mark instance satisfying the standard marked-cut hypothesis.

## Low-surplus Kempe frontier and complete ambient-order-98 census

Audit date: **2026-07-26**.

The independently reconstructed human proof excludes ambient orders
\(88,90,92,94\) in the connected extremal exact-zero size-four branch.
Its arbitrary-surplus form proves \(2p+u\le d+2\), the corresponding
simultaneous-switch inequality, and sharp girth overlap bounds.

The transparent frontier checker
`scratch/verify_order96_kempe_incidence_frontier.py` verifies the
displayed \(8\)-by-\(8\) order-\(96\) incidence matrix against row and
column capacities, diagonal constraints, pairwise overlap bounds,
single switches, and all \(255\) nonempty simultaneous switches from
each shore.  It reports PASS with minimum slack one on both shores.
This is an abstract necessary-condition skeleton, not a graph
realization.

Three later local girth constraints exclude that skeleton and two
all-multiplicity-at-most-two replacements.  The complete strengthened
incidence census then enumerates all 109 canonical excess-profile pairs
and finds zero matrices:

```text
order-96 strengthened incidence census: PASS
canonical_profile_pairs=109
surviving_profiles=0
surviving_matrices=0
total_search_nodes=3266
census_sha256=6b754326a9490ec51788965ccc4caea257031b7cb8180bea22a71477bcd94529
```

An independent QF_LIA implementation returns 109/109 UNSAT with status
digest
`36307d048a74da4f6c7ba93bcb0def2535747cc142c98a73cc39d814563e4093`.
A separate audit checked the 109 orbits against all 108,900 labelled
profile pairs and reran a prune-free 11,762-node DFS.

At order \(98\), the general factor-size and Kempe-incidence argument
excludes the newly possible unmarked circuit.  The resulting all-marked
system has 335 simultaneous-\(S_8\) profile-pair orbits.  The new
diagonal total-excess-two overlap lemma, proved by a weighted
triangular-prism/\(K_{3,3}\) argument, closes the last local gap.  The
complete output is:

```text
order-98 strengthened incidence census: PASS
canonical_profile_pairs=335
surviving_profiles=0
surviving_matrices=0
total_search_nodes=32327
census_sha256=7341775b73eedeaa51e72aa1abf0ef277c58651de01c42f982850828f402836c
```

An independently generated QF_LIA implementation returns 335/335 UNSAT
with status digest
`d25fc082531d63325351ef8bbb29234ffc90e164fdfe6d184fe79af0b0d1d2d1`.
A separate audit normalizes all \(792^2=627,264\) labelled profile pairs
to the same 335 orbits, obtains zero survivors with the forward prune
disabled after 9,193,235 nodes, and finds all 335 independently generated
HiGHS MILP instances infeasible.  Omitting only the new diagonal cap
leaves exactly two survivors.

The independent audit note and checker are
`docs/order98-independent-incidence-audit.md` and
`scratch/audit_order98_incidence_system_independent.py`.  The frozen
audit result has SHA-256
`42752bef8ece3d62fa7437743cb20be216d49f28374711c91d310bceeed324cc`.

This raises the connected eight-mark size-four branch bound to ambient
order 100; it is not a general graph census or a five-CDC proof.

## Certified ambient-order-100 global-profile closure

Audit date: **2026-07-26**.

The human unmarked-factor argument in
`docs/order100-unmarked-exclusion-and-row-star-frontier.md` reduces order
100 to the all-marked case.  The cap-table census leaves 155 of 1,002
canonical profile pairs, and the exact weighted row/column-star replay
leaves exactly three relative alignments of
\((2,2,1,1,0,0,0,0)\).

`scratch/solve_order100_global_profile_sat.py` does not fix one of the
1,864, 1,680, or 1,984 labelled incidence matrices.  For each of the
three profile alignments it chooses all 64 cell geometries, enforces exact
position covers and Kempe support caps, and reconstructs all \(46\)
common-colour tokens of the \(92\)-vertex core.  The final results are:

```text
profile  variables  base clauses  semantic lazy clauses  terminal clauses
0        36388      96072         94135                  0
1        36188      95537         115385                 0
2        35988      95002         787384                 0
```

All three formulas are UNSAT already in \(G-M\).  CaDiCaL generated LRAT
proofs and the independent C `lrat-check` reported `VERIFIED` on every
one.  The producer-free
`scratch/check_order100_global_profile_cnf.py` independently regenerates
the local domains, Sinz encodings, exact position covers, support links,
and support caps.  It then decodes every appended negative-option clause
and reconstructs its forced partial graph.  All \(996,904\) lazy clauses
contain an actual circuit of length below ten; none uses the terminal
pairing fallback.  The checker also requires its three profiles to agree
exactly with the independent row-star survivor artifact.

```text
CNF p0   4e53fb27d42318aab96014ed1319f0e98398260e731176a186d0029285bb4d25
CNF p1   e3b3e7691f0c8b05193c9ea02055985fb6cf8fac0621c2a87371951a307b7741
CNF p2   120fa2c89cb13dd7d706a58cadd290b805dec4a7aca3b92c97d68477c0849ac0
LRAT p0  a34d8d9170f596e43d02779f6ac7d9271ba1bf1b08ea2ecf862cf59a2230e4c8
LRAT p1  265a74e8e9a3fc7606fba45734e7180d9137e1dbbdde7e95cae08f469f2047d5
LRAT p2  f96d88f051b2a00613265207118bc460102f34c69698a89143b2c971b0fc11cb
checker  217ddb77675e9e1484e25de9d84feadcce132542af6b07f60c7543c3bcdc1032
```

This closes ambient order 100 only in the connected eight-mark extremal
exact-zero size-four branch and raises its bound to \(102\).  It is not a
general graph census and not a proof of five-CDC.

SHA-256:

```text
audit/generalization  0d2dda5d69b48941c3d365071696ed7407680adc5e325bbe1a5a32f73a862e7d
order-94 proof         2c1ce21aa9045ad203a6d65d8ac31f601e1a2d366f61295ceb0d985611d89a5d
frontier checker       6a84b0ffc9ccaa96f375e83654a64c064f2d17645bd520526c630faa25f6562d
```

## Rooted marked-cut bridge reduction

Audit date: **2026-07-26**.

The exact bridge reduction in
`docs/rooted-four-mark-bridgeless-reduction.md` eliminates the \(3+1\)
two-cut mechanism under the inherited marked-cut inequality.  On the
existing \(13\,824\)-row structured family, 240 instances satisfy both
universal separation and the marked cyclic-cut inequality.  Independent
cycle-space enumeration checks \(3\,818\,240\) componentwise-even
all-mark cycles and finds zero instances with any forced unmarked edge.
This is a finite diagnostic supporting the scoped reduction, not a
universal rooted theorem.

## Exceptional four-pole two-plus-two algebra

Audit date: **2026-07-26**.

The producer and independently written JavaScript verifier enumerate all
640 ordered xor-zero \(D_5\) boundary words.  Their ten \(S_5\)-orbit
sizes agree exactly:
\[
10,60,30,60,60,120,120,30,120,30.
\]
Both reconstruct the complete \(10\)-by-\(10\) singleton composition
table, exactly 259 nonempty masks satisfying the published necessary
switching lemmas, and the same exceptional factorization counts.

The computation supports the human factorization theorem in
`docs/four-pole-exception-rooted-packing-algebra.md`; it does not assert
that the 259 masks are graph-realizable or settle the published
exceptional-signature conjecture.

SHA-256:

```text
human note            de05a42e5868db0b97b7a3880c74873e33892626afa4c584825a45562e45b9be
Python producer       9469b35d5034b9196d37092a8c701132046d68aee04854deee5f4947f8455661
frozen JSON           e12307cad9a7176dfc8072f9d4052edd148cea5b4d9e11be8617c936a00d65c9
independent JS        09c36ddf3ec5901e9b8a6a6a051b745bd31b7420fe811b6a098a263503e3faa5
```

## Complete order-22 universal four-separation census

Audit date: **2026-07-27**.

Four canonical `geng` shards exhaust all \(7\,319\,447\) connected
simple cubic graphs on 22 vertices.  The primary direct-colouring
implementation and a separately written perfect-matching/even-two-factor
replay agree on every shard:

```text
shard  graphs     Tait graphs  normalized colourings  witnesses
0      1376411    1338944      17481016                0
1      2078782    2029518      28040733                0
2      1716645    1686315      22708101                0
3      2147609    2119958      27130262                0
total  7319447    7174735      95360112                0
```

The independent replay visits \(312\,583\,931\) perfect matchings and
derives every normalized Tait colouring six times, from the three
choices of distinguished colour matching and two orders of the
complementary colours.  Complete order-12, order-16, and order-18
controls agree exactly.  On a positive order-24 target-three control,
both implementations return the same first marked edge IDs
\(0,1,34\), while both correctly reject target four.

The result proves only that no Tait-colourable connected simple cubic
order-22 graph has a universally bichromatic-factor-separated four-edge
matching.  Uncolourable rows are outside the theorem because both
implementations skip their vacuous no-colouring case.  It is not a
multigraph theorem and does not settle orders 24 or higher.
Details, hashes, and commands are in
`docs/order22-universal-four-separation-screen.md` and
`scratch/order22-universal-four-separation-result.json`.

SHA-256:

```text
primary source       a00c2f53a3b95a06a7e8767aae2eb2bfa794fc95eeeba18bcac34aea6a12072a
independent source   104dca4ac143581a9b306172354428a96913f3fe1701c60b2a018510990ecead
geng binary          ad2f68adf733dbed7cad543841cfa329740596ee5cd136f17a0a17f6e744f5ad
```

## Complete order-18 exceptional-signature census

Audit date: **2026-07-27**.

The exact command

```text
geng -cq -d2 -D3 18 25:25
```

has \(4\,159\,098\) canonical rows.  Each row was classified by both an
incremental-SAT implementation and an independently written direct
finite-domain implementation.  Their aggregate counts per
implementation are:

```text
rows          4,159,098
queries      16,453,323
satisfiable  15,295,709
exceptional           0
```

Every complete decision transcript was streamed through a third parser
and hashed.  SAT and CSP transcript digests agree on each of eight
shards.  The exact finite conclusion is that none of these order-18
degree-\((2,3)\) cores realizes any of the six ordered exceptional
boundary masks in the fixed five-colour \(D_5\) model.  It is not a
universal absence theorem or a classification with unboundedly many
colours.

Frozen package:
`search/four-pole-order18-exceptional-20260727/`.

SHA-256:

```text
SAT source       37d5a07702260522d722867929843fadc099cf28e4a511a9b45399383d855ce4
CSP source       3f4fbb38ed3a085fb596a858598a157681b325112dafa7728069a3933a097893
stream auditor   d79f17ec8147822510c6201bfb0a303dc5a8245b74829384ee37e059ef3b158a
run verifier     a54ed8df84bd3d0dfeef177c2b9fa74c89322d42bac666ca4d77f256563686cd
result report    ca6f3c93bf78f496447451c698b2698807b39313ead1450445003e59d6f34d38
```

## Rooted base-pair closure screen through order 17

Audit date: **2026-07-27**.

For every nonbridge root of every connected simple cubic three-pole
core through order 17, the targeted screen asks whether the exact
seven-orbit root signature is empty or contains one of masks
`0x0c`, `0x12`, `0x21`.  On the 654,676 order-17 cores:

```text
nonbridge roots         15,645,623
empty                      337,059
base-pair closed         15,308,564
violations                        0
solver calls per engine  52,216,251
```

The direct finite-domain and independent incremental-SAT programs have
the same complete streamed transcript digest on each of eight canonical
shards.

The result is a finite theorem through order 17, not an induction.
The complete-signature corpus through order 13 realizes 22 nonempty
nonbridge masks, whose only inclusion-minimal elements are the three
base pairs; its \(22^2\) cross-relations are only `DI` and `DEI`.
A separate exhaustive \(3\times127\) check shows that the base pair
itself against any nonempty stabilizer-invariant signature never has
relation `E`, `EI`, or `D`.  It does not justify replacing the base
pair by a containing signature: `R={12,03,04,01}` and `S={01}` give
`EI`.  With the simple-cap fork, one order-17 shore therefore excludes
the `E` and `D` cyclic-three branches through total order 36, but the
mixed `EI` branch remains.  Artifacts and the independent replay are in
`search/rooted-three-pole-frontier-20260727/`.

## Complete order-20 exceptional cap census

Audit date: **2026-07-27**.

The canonical order-20 cubic corpus and the proved simple-cap reduction
give:

```text
connected simple cubic graphs       510,489
bridgeless graphs                    497,818
bridgeless non-Tait caps               1,388
independent-edge deletions            520,500
```

The direct edge-colouring filter and an independent
perfect-matching/even-complement filter produce the same cap stream.
The independently retained pole expansion was then checked by both
boundary classifiers:

```text
queries per implementation        2,074,239
satisfiable answers               1,978,630
exceptional hits                          0
```

A separate standard-library verifier reconstructs the cap properties
and every deletion rather than trusting the producer.  Hence no
bridge-free connected simple terminal-distinct four-pole of order 20
has either exceptional exact five-colour \(D_5\) signature.  This is
finite and scoped.

Frozen package: `search/four-pole-order20-cap-20260727/`.

SHA-256:

```text
cap stream        e29e65288c1b158afafaafe4c6d2d7862ed64ed4e48e15c49d7b06a221607020
pole stream       9618a6b119ee21d73edab67372991d5abf12df240605c67151a5e308aa0c58ad
result report     d50e21fcb8c977cb036eafb4e9d7c03ddc3e37494a07438d751636711bdfc24d
independent audit a9ee46eba77186102d886c4a30046ad6aa3badbe74647bb1b01b253d7035f7f0
```

## Complete order-22 exceptional cap census

Audit date: **2026-07-27**.

The canonical order-22 source and simple-cap reduction give:

```text
connected simple cubic graphs          7,319,447
bridgeless graphs                       7,187,627
bridgeless non-Tait caps                   12,892
independent-edge deletion poles         5,956,104
```

The direct Tait-colouring filter and an independent
perfect-matching/even-complement filter select the same hard corpus
byte-for-byte.  The pole stream was distributed over eight deterministic
shards and checked by both boundary implementations:

```text
queries per implementation             23,747,129
satisfiable answers per implementation 22,764,574
exceptional hits                                0
```

The two implementations agree on every complete streamed transcript
digest.  A separate verifier checks the canonical-source identities, the
two hard-cap streams, every retained graph premise, the entire pole
expansion byte-for-byte, and all sixteen classifier/auditor records.
Combined with the cap reduction, this excludes both exceptional exact
fixed-five \(D_5\) signatures for every bridge-free connected simple
terminal-distinct order-22 four-pole.

This advances the even-order lower bound in that scope to 24.  It is not a
universal exceptional-signature theorem and not a Five-CDC resolution.

Frozen package: `search/four-pole-order22-cap-20260727/`.

SHA-256:

```text
hard cap stream 230f2cd88e72011d73a40c5f3d7d5f9fb0fca6110de2ec2541581bc50982037c
raw pole stream cf7a19244912c746c1ef1247a4b45e6ad1df647feaa4251e59db381351b5db46
result report   4f1c8e73be167facd2cc378d3087a5196e841d0f282ab242a4de32ade146b746
verifier source f7d234b504034cd7b3528ed6820279bdc769a4c3c1292dbffaa40e423b60a501
```

## Order-24 strict-snark full-signature probe

Audit date: **2026-07-27**.

The retained Snarkhunter 2.0b source has 38 distinct strict snarks of
order 24.  Its graph identities and the strict-snark premises are checked
independently, while completeness of the canonical list continues to rely
on the generator and its option semantics.  Expanding every independent
edge pair gives 21,204 terminal-distinct deletion poles.

Both exact boundary implementations classify the complete retained pole
stream in full-signature mode:

```text
rows per implementation          21,204
queries per implementation      212,040
satisfiable answers             212,040
rows with full mask 0x3ff        21,204
exceptional hits                      0
```

Their TSV outputs are byte-identical.  A third implementation decodes and
checks every cap, reconstructs all deletion poles, and compares the two
tables row by row.  Hence every retained pole realizes all ten boundary
types in the fixed-five \(D_5\) model.

This is not a census of every order-24 non-Tait cap and not a proof that
cyclically-four-connected caps universally have full signature.

Frozen package:
`search/four-pole-order24-strict-cap-probe-20260727/`.

SHA-256:

```text
source graph stream e981f9b6953628bb03077f228c5373992430369adc13dd6cde02d330a730c313
raw pole stream     31231a552a4e713b58b915032a1a9f575d19aaa379ad074eca9ed3c105ab5400
raw solver table    fbc25fd53702e7ea6cff44b18a62563ba1b45cfeea9298177d38ff87fba227b6
result report       0cf2cc6575faf5dea0cac4f2d5e71bb3fd00e692fb20f6ff444bc7222e801010
independent audit   7e52f0ea194fe0344b7f602d929de14fe01382da94a5aac6911a4912a31090a6
```

## Complete cyclically-four order-24 cap classification

Audit date: **2026-07-27**.

Running Snarkhunter at girth four rather than five produces 155
cyclically 4-edge-connected non-Tait simple cubic caps of order 24.  This
is the complete intended cap scope, subject to the generator's
completeness: a triangle would itself form the cyclic shore of a
three-edge cut, so no additional girth-three cap can occur.

Every independent edge pair gives:

```text
source caps                          155
deletion poles                    86,490
queries per implementation       864,900
satisfiable answers              864,900
rows with full mask 0x3ff         86,490
exceptional hits                       0
```

The two full tables agree byte-for-byte.  A separate verifier checks the
155 graph premises, reconstructs every deletion pole, and validates both
sharded tables.  Combined with the atom descent and rooted cyclic-three
elimination, this excludes simple terminal-distinct exceptional poles
through order 24 and raises that even-order lower bound to 26.

Frozen package:
`search/four-pole-order24-cyclic4-cap-20260727/`.

SHA-256:

```text
source graph stream 37ef068ab597c6cc882eb2121d9743464b0717bc4beefab4348ef4221b6a7456
raw pole stream     4c79b5caa25f331c94cd1c458ad1b0a9bccc9d89328e3c3fe4c25a3e8ec0d5fc
raw solver table    23298cb8c6abf989052a249db8ce48c9d73b233ef1c5b07d73054d4a130913d4
result report       2ce165e81478efe41df19d129aaeaa2f8938ef683131c1b5c49b3c45fd3f301b
independent audit   b61c66c713a3832b49a2fe1a7244d915187817fafaa5238a8e01d7af32232ca7
```

## Order-26 strict-snark full-signature probe

Audit date: **2026-07-27**.

The documented Snarkhunter 2.0b source contains 280 strict snarks of order
26.  Its graph identities and strict-snark premises are checked by a
separate standard-library verifier, while completeness of the canonical
list relies on the generator.  Expanding every independent edge pair gives
185,640 four-poles.

The CaDiCaL and direct finite-domain classifiers agree byte-for-byte on the
complete full-signature table:

```text
rows per implementation          185,640
queries per implementation     1,856,400
satisfiable answers            1,856,400
rows with full mask 0x3ff        185,640
exceptional hits                       0
```

The direct implementation was split into eight equal consecutive shards;
the independent verifier sums their logs and checks the concatenated table
row-by-row.  This is finite evidence on the retained source, not a complete
order-26 non-Tait census.

Frozen package:
`search/four-pole-order26-strict-cap-probe-20260727/`.

SHA-256:

```text
source graph stream 5ce072d86e9fa639f34d1a9ec916b69c62a46816f5486a0d813e56279320e35d
raw pole stream     9073b2390f68070a121ae0523d5000acc0e5e2ad8ec8d6214a65a6d23ef106dc
raw solver table    07c466b2c0839098b534f2a1bb1e894b973a619bb3eccd3118a69edfed8a1f68
result report       a1a1d7bd6b9cf03dbda75543a6ce9a53f2f9c57cb39dca27626027d15af7c0a1
```

## Complete cyclically-four order-26 cap classification

Audit date: **2026-07-27**.

The complete Snarkhunter girth-four run contains 1,297 cyclically
4-edge-connected non-Tait simple cubic caps of order 26.  Triangle
exclusion makes this the complete intended cyclically-four cap scope,
subject to the generator and its option semantics.  Expanding all
independent edge pairs gives:

```text
source caps                        1,297
deletion poles                   859,911
queries per implementation     8,599,110
satisfiable answers            8,599,110
rows with full mask 0x3ff        859,911
exceptional hits                       0
```

The CaDiCaL and independently written direct finite-domain tables agree
byte-for-byte.  A third implementation checks all graph premises,
reconstructs the complete deletion stream, validates every table row and
all sixteen shard logs, and reproduces the committed report.

The finite conclusion is exactly the displayed cyclically-four cap
classification.  A later hostile audit found that the attempted reduction
of every cyclic-three cap to this corpus used a false one-sided base-pair
inference: the mixed equality/intersection relation can survive one-sidedly.
Therefore this package alone does **not** rule out all exceptional
terminal-distinct four-poles through order 26 and does not establish a
global lower bound of 28.  The unaffected cyclically-four theorem and the
withdrawal are both retained.

Frozen package:
`search/four-pole-order26-cyclic4-cap-20260727/`.

SHA-256:

```text
source graph stream 1d2b95b9d412f5f6b8ccb788779bd685df23b3239bda8c7e9557266375519760
raw pole stream     8e346b040fb4c69bef5ab6b21b30c30635a22ba4086a9b5ea567cdf3d10378e4
raw solver table    abc46bc0af6f94596ae11c68af95acc55cf8d73d82f81aea4a06ab8614a14da2
result report       69d8eb39b70df89906a9c3be28dc323231ef0bd173f7dbffee8311ce0156de71
independent audit   e78d88124b2f75a4c6a7c3514017aece816834106d26595e56166ce84532380e
```

## Certified low-arity \(D_5\)-polymorphism no-go

Audit date: **2026-07-27**.

Treating the cubic \(D_5\) vertex constraint as the ordered triangle
relation on the ten edges of \(K_5\), four deterministic CNFs search for
standard closure operations.  Independently checked LRAT certificates
exclude:

```text
nonprojection idempotent binary polymorphisms
ternary majority polymorphisms
ternary minority polymorphisms
idempotent cyclic ternary polymorphisms
```

This certifies a failed proof strategy, not a Five-CDC theorem.  It does
not classify every higher-arity polymorphism or decide realizability of
the exceptional four-pole signatures.  Frozen package:
`search/d5-triangle-polymorphism-no-go-20260727/`.

## Multi-switch Fano lower-bound family

Audit date: **2026-07-27**.

The memo
`scratch/fano-multistep-reconfiguration-audit-20260727.md` audits the two
current nowhere-zero-flow reconfiguration papers and proves a recursive
lower-bound family.  Its essential exact data are:

```text
host leaf ports at depth d                  3^d
maximum ports met by one connected circuit 2^d
final graph order                           15*3^d - 5
switch-distance lower bound                 ceil((3/2)^d)
Five-CDC counterexample                     no
explicit three-cycle double cover           yes
```

The ten-vertex host has three displayed value-two port edges on no common
connected circuit.  Replacing each recursively by a fresh rooted host
multiplies the port count by three and the circuit capacity by at most two.
Grafting a certified all-seven-bad block at every leaf makes every shorter
switch sequence leave one complete bad footprint untouched.  The proof is
by projection through the aligned two-edge sums and is displayed without
relying on a solver.

The first member is the frozen 40-vertex one-switch countermodel.  It
repairs in exactly two value-four circuit switches.  The new independent
checker

```sh
python3 scratch/verify_fano_multistep_two_switch.py
```

reconstructs the graph and both switches and returns:

```text
defect rows:
10 6 6 12 12 6 6
 8 2 6  8 12 8 4
 6 0 8  6 10 8 4
final unique good line: 145
status: PASS
```

This closes every constant-step exchange lemma.  The component-domination
assertion with an unbounded path remains open.

## Cyclically-four pole/full-signature structural probe

Audit date: **2026-07-27**.

The audit
`scratch/fixed-five-d5-four-pole-full-signature-frontier.md` separates two
claims that the earlier positive cap censuses did not distinguish.

The broad statement for internally cyclically-four proper poles is false.
The explicit order-16 graph6 record

```text
O????A?[BOI_g_Ao?kCo?
```

with terminals \(5,6,7,8\) has exact fixed-five mask `0x3fe`.  An explicit
edge list and complete small-cut shore table verify its graph premises, and
a three-line linear parity argument excludes \(AA\).  CaDiCaL and a direct
finite-domain implementation independently classify the remaining states.

The focused statement for deletion poles of cyclically-four-connected
non-Tait caps remains open.  A human lemma now proves that, for two
independent cap edges, every component outside their four endpoints has
even attachment number.  This constructs the required one-bit projection
of an \(AA\) state.  It does not construct a simultaneous \(D_5\) label.
The missing condition has the exact form:

```text
an F2^2-flow whose zero set contains the prescribed pair
and whose complement has two edge-disjoint boundary T-joins.
```

All 14,322 complete order-22 cyclically-four deletion poles and all 21,204
retained strict order-24 deletion poles have full mask `0x3ff` under two
classifiers.  These finite results support but do not prove the focused
claim.

## Prescribed-\(AA\) certificates for \(H_2,\ldots,H_5\)

Audit date: **2026-07-27**.

The reconstructed high-flow-resistance graphs \(H_2,H_3,H_4,H_5\) have
orders 82, 122, 162, and 202 and certified flow resistances \(2,3,4,5\).
Every independent edge pair was tested in the equivalent cap form: require
a fixed-five \(D_5\)-labelling that assigns the two prescribed edges one
common label.

```text
graph  independent pairs  explicit labellings
H2                 7,257                   79
H3                16,287                   92
H4                28,917                  103
H5                45,147                  120
total             97,608                  394
```

The 394 complete edge labellings form a greedy cover of all 97,608 pairs.
A solver-independent verifier checks every graph identity, cubic and
bridgeless premise, every \(D_5\) label, every vertex xor equation, every
pivot assumption, and the complete pair coverage.  Hence every associated
deletion four-pole realizes boundary type \(AA\).

This is a finite positive theorem, not a universal prescribed-pair result.
Frozen package:
`search/mnp-h2-h5-aa-deletion-probe-20260727/`.

SHA-256:

```text
certificate table ad2192ff178482a97d5a905d71bcfe47f3b4e96879cb41ad7bb5ae6099d2f8e7
result report     c92f338124fa57347d041fdc109f07ae24b0916787f4b904ed62fc41a611a854
independent audit e76003fa7ec5aefb51d0e7aa19e3c37f938995c1313c20c752074263747ab03d
```

## Cyclically-four endpoint root screen through factor order 26

Audit date: **2026-07-27**.

The complete retained cyclically 4-edge-connected non-Tait factor sources
of orders \(20,22,24,26\) contain:

```text
factor order                  20       22       24        26
source factors                 6       31      155     1,297
vertex-deleted cores         120      682    3,720    33,722
```

Independent incremental-CaDiCaL and direct finite-domain classifiers
screen every nonbridge root:

```text
source factors                         1,489
vertex-deleted cores                  38,244
nonbridge roots                    1,360,452
solver calls per implementation    4,157,844
empty signatures                           0
base-pair-closed roots             1,360,452
violations                                 0
```

The two complete uncompressed transcripts are byte-identical with SHA-256

```text
bfb90fd89b43e66f02ada87abcb87ab643d87a4b36dba616cd1f3e5d603b7364
```

A third implementation reconstructs every source graph and vertex
deletion, checks triangle-freeness, cyclic four-edge-connectivity and
non-Taitness, identifies each nonbridge root, verifies every adaptive
decision, and aggregates all twelve shard logs and statuses.  It reproduced
the frozen report twice.

The finite theorem supplies base-pair closure for endpoint factors through
order 26.  It yields cap order at least 54 for equality-only or
disjointness-only cyclic-three relations.  It does not eliminate the mixed
equality/intersection relation.

Frozen package:
`search/rooted-three-pole-nontait-endpoint-frontier-20260727/`.

## Focused theta-choice census at order 30

Audit date: **2026-07-27**.

The official House of Graphs order-30 cyclically-four snark corpus has
139,854 distinct graph6 records (compressed SHA-256
`93b8abf7b907fee03b9ecb99b917d14c2cc4f97bc115c0e793635db22c408567`;
decompressed SHA-256
`bc6f29ec50910eae345ced81f87800686deb069dd1cb383d73dbcc56765f247d`).
The primary C++ classifier and a separately written standard-library
Python replay in sixteen disjoint shards agree exactly:

```text
graphs                             139,854
independent root pairs         125,868,600
deficiency zero                124,646,796
deficiency two, theta found      1,221,804
deficiency two, all dumbbell             0
boundary-six deficient pairs             0
boundary-eight deficient pairs   1,221,804
near matchings checked            7,814,531
```

Every independent shard reports `PASS`, and the compact package verifier
rechecks the complete corpus, every retained hash, and exact aggregate
agreement.  This is a finite structural theorem, not a universal
theta-choice theorem or a Five-CDC resolution.

Frozen package:
`search/focused-theta-choice-order30-20260727/`.

SHA-256:

```text
report       9a188be2ee948282a7550c5e5f3eeffe7d7dd8e94ac0e1cc64f08e703550ffcd
checksums    ac96945c376fcd63a351b3da287751646ea563f23ae86366cd17c04b27496ccc
```

## Jaeger fixed-fibre support-five frontier

Audit date: **2026-07-28**.

The exact fixed-fibre search labels every edge by its membership
multiplicity in three spanning trees, derives the three fundamental
completions, and asks for a compatible pair labelling on at most five
points.  All simple bridgeless cubic graphs through order 14 give:

```text
graphs                                      587
Type A/B placements                     944,974
feasible fixed fibres                    804,204
feasible fibres with support at most 5   804,204
failures                                       0
```

The retained census SHA-256 is
`482e2ee028aa1663f2b91b71569422ab59c1033d51601ca52fac581b173872f1`.
The independently written replay
`scratch/verify_jaeger_five_point_frontier.py` accepts the complete stream.

For the stronger fixed-coordinate star test, all 26,790 star fibres on the
705 retained order-38 records pass.  A separately frozen order-44 literal
witness package covers 31 graphs and all 1,364 roots, again with zero
failures.  Its primary hashes are:

```text
result                         040226e29e81fc6635f17813dd9bc5747ba33d8a226bba1b35ff7ca18e28000c
literal witnesses              3ff25437d5e32fff7c60ceca695a6476d6c7d2404c1e8551bf14987f228cd4b4
normalized semantic witnesses  abb8bab730e873a6648d6e56987b6595f95162b2a3e7bd07d592b8d300790800
input graph list               d701f0cffce5aaba17315d2d9d3851bb747c4e1ece3e2cf188522237b388a0ef
```

The independent verifier reconstructs all three spanning trees and
fundamental completions rather than trusting producer-supplied flow values.
These are bounded positive results.  They do not prove that every
3-edge-connected cubic graph has a parity-good star packing.

## Jaeger parity-element and kernel-closure frontier

Audit date: **2026-07-28**.

Appending an all-ones column \(p\) to a reduced binary incidence matrix
turns every odd kernel into the fundamental circuit
\(C(T,p)-p\).  The stronger search target asks for a packing and
coordinate with
\(K_j\cap K_k\subseteq\operatorname{cl}(K_i)\), which implies but is
stronger than exact component parity.

The frozen census gives:

```text
connected simple cubic graphs through order 14       621
vertex-star patterns                               8,392
feasible vertex-star fibres                        5,646
kernel-closure-good vertex-star fibres              5,646

connected simple cubic graphs through order 12       112
Type A/B patterns                                110,127
feasible Type A/B fibres                          90,203
kernel-closure-good Type A/B fibres                90,201
generic Type-A failures                                 2
```

Both failures occur on graph6 `K?\`@E\`gFCKEO`, at defect triples
\(\{0,4,11\}\) and \(\{1,3,10\}\).  An independent exhaustive checker
finds 355,392 ordered packings per fibre, zero closure-good packings, and
7,704 exact-parity-good packings.  A second independent semantic replay
checks all 12,695 positive Type-A/B witnesses through order ten.

The still-open vertex-star strengthening also passed the retained
34-vertex hard graph, all 1,364 star fibres in the order-44 oddness-four
list, and all 2,500 roots in 50 deterministic random order-50
3-edge-connected cubic graphs.

Frozen package:
`output/jaeger-kernel-closure-frontier/`.

## Jaeger symmetric-descent frontier

Audit date: **2026-07-28**.

For the symmetric defect \(d_{\min}\), the minimum of the exact
component-parity defect over all seven Fano planes, the complete
reciprocal-exchange census through order 14 contains:

```text
simple 3-edge-connected cubic graphs       419
root automorphism-orbit instances        3,567
exact star-fibre states             529,150,122
trapped positive-level components             0
maximum d_min                                  4
```

The row-level census has SHA-256
`f1d720265cc58a732cf2b58920b8dacc12f36191cecc731949622f5c80f4f2e0`.
The independent coverage verifier regenerates the graph streams,
3-edge-connectivity filters and root orbits and checks every aggregate and
digest.  The C++ state enumeration is not independently duplicated.

This is a finite theorem; the universal symmetric-descent theorem remains
open.

## Jaeger vertex-star kernel-closure countermodel at order 16

Audit date: **2026-07-28**.

The complete connected-simple-cubic order-16 search contains:

```text
graphs                                      4,060
vertex-star roots                          64,960
feasible star fibres                       45,248
kernel-closure-good feasible fibres        45,247
kernel-closure failures                         1
```

The unique failure is graph6 `O??CA?_ceOGgH_F?AK@P?`, root 13.  The
frozen producer stream
`output/jaeger-kernel-closure-frontier/stars-order16.jsonl` has SHA-256
`889d0e5857b62e082f3fcad0a929e7c0d92032a8e675f4d2ff9f40272ea43d46`.
This bounded census locates the first failure after the all-positive
through-order-14 census; it is not by itself a proof of unlabeled
minimality beyond the stated generator stream.

The failed fibre was then checked without the producer.  Deleting the
root yields 16,200 cographic bases and 158,976 unordered partitions into
three such bases.  Restoring coordinate order and the spoke bijection
gives 5,723,136 ordered packings, with histogram:

```text
(closure-good coordinates, parity-good coordinates)  count
(0,0)                                             5,682,672
(0,1)                                                40,464
```

A separately generated 744-variable, 101,037-clause CNF is UNSAT.  Its
LRAT certificate is accepted by both `lrat-check` and verified CakeML
`cake_lpr`.  Primary hashes:

```text
CNF   ccd8ef9504ef725dc02be9234992cbc9e238f1c12ed39ad3068645c73e3c5baf
LRAT  ffcd95bc48db7c5be222e05b86aa72cf0828ef01e45e7cf45e9a92cab76aa3a5
```

An independent literal witness verifies exact component parity and a
five-point pair labelling in the same fibre.  Thus this is a
counterexample only to the closure strengthening, not to the surviving
Jaeger parity lemma or Five-CDC.  See
`scratch/jaeger-star-kernel-closure-countermodel-16v.md`.

The three disjoint triangles contract to Petersen.  A direct no-SAT
checker exhibits a closure-good packing after contracting one triangle
and verifies that all six legal lifts fail closure.  A human contraction
theorem proves that closure failure is preserved by expanding any
nonroot vertex into a triangle, giving an infinite countermodel family.
See `scratch/jaeger-star-kernel-closure-triangle-expansion.md`.

For the surviving exact condition, the same local lift problem has the
opposite answer.  There are 60 admissible triples of odd-kernel traces
together with an Eulerian-completion trace.  They form seven orbits under
triangle-vertex permutations and exchange of the two common-kernel
coordinates.  Every orbit has at least one exact-parity-preserving legal
lift:

```text
good legal lifts per trace  traces
1                           18
2                           12
3                            6
4                           24
```

This is a complete local theorem, not a random test.  The human proof and
independent exhaustive table are in
`scratch/jaeger-star-exact-parity-triangle-invariance.md` and
`scratch/verify_jaeger_star_exact_parity_triangle_lift.py`.

## Targeted symmetric descent on the order-16 closure countermodel

Audit date: **2026-07-28**.

The unique order-16 vertex-star fibre failing the stronger kernel-closure
condition was checked separately under the exact symmetric potential
\(d_{\min}\):

```text
graph6                         O??CA?_ceOGgH_F?AK@P?
root                                                  13
exact star-fibre states                           953,856
maximum d_min                                           4
trapped positive same-level components                  0
```

The independent local replay uses omitted-class masks
`8413,1725442,363296`.  It reconstructs the exact seven-plane profile
\((4,4,4,4,4,4,4)\) and exhausts all 147 incident exchange candidates:
25 are legal, of which 22 lower the symmetric minimum to two and three
stay at four.

The machine-readable row and digest manifest are in
`output/jaeger-fano-min-descent-order16-closure-no-go/`.  This is a
targeted exact fibre result only.  The C++ whole-state enumeration is not
duplicated in the independent Python checker, and no complete order-16
descent census or universal theorem is claimed.

## Immediate-descent no-go and triangle-expansion audit

Audit date: **2026-07-28**.

The exact positive order-16 state in
`jaeger-fano-min-immediate-descent-countermodel.md` has 147 candidate
swaps and 23 legal neighbours:

```text
neighbour d_min       2   4
count                18   5
```

There is no immediate descent from its value two.  One kernel-inert
neutral move followed by one active move reaches zero.  This is an exact
countermodel to one-step averaging only.

A second exact state in the same fibre, with omitted masks
`1722528,307976,66647` and profile \((4,4,4,4,6,2,2)\), has 23 legal
neighbours, all at \(d_{\min}=2\), and zero kernel-inert neighbours.
Its fixed-kernel realization component is therefore a singleton.  An
active same-level exchange followed by one further exchange reaches
profile \((6,4,4,4,4,4,0)\).  This refutes fixed-kernel exposure but
still does not refute the full same-level-component theorem.  The same
independent Python checker exhausts both incident neighbourhoods and
replays both two-step paths.

The thirteen labelled graphs obtained by expanding one nonroot vertex
of graph6 `M?AA@BORDGEOEOAo?` were then checked completely at root zero:

```text
triangle-expanded fibres                         13
states per fibre                          1,330,560
total exact states                       17,297,280
maximum d_min                                      4
trapped positive same-level components             0
```

The census SHA-256 is
`501cc9db6987bc2b458abbf5f82bbcd37ccda74aff9817e91c36a9f6c49d80d3`.
The coverage verifier independently regenerates all thirteen
expansions, checks simplicity, cubicity and 3-edge-connectivity, and
audits rows, totals and hashes.  The 17,297,280-state enumeration itself
remains in the C++ trust boundary.

## Affine pair-exchange countermodel at order 36

Audit date: **2026-07-28**.

Adversarial exact-flow search found a score-zero countermodel to APX on
the seventeenth retained order-36 strong-snark row.  Direct independent
replay gives:

```text
vertices / edges                              36 / 54
girth / cyclic edge connectivity                5 / 4
perfect matchings exhausted                       221
original nonpacking value classes                   7
all original/pair-deletion packing queries         198
binary cycles tested                         1,274,117
affine-compatible line occurrences                  33
distinct affine-compatible pairs                    32
affine-compatible packing pairs                       0
```

The checker also validates a standard five-cover with coordinate sizes
\(25,19,21,21,22\).  A complete connected-circuit audit enumerates
166,792 simple circuits and 9,532 legal circuit/value switches, 6,699 of
which make the flow good.  Therefore the witness refutes APX only; it is
neither a FiveCDC counterexample nor a countermodel to the broader reduced
one-switch lemma.  See `scratch/fano-apx-countermodel-order36.md` and
`scratch/fano-apx-countermodel-order36-result.json`.

## Square-local lifting quantifier boundary

Audit date: **2026-07-28**.

The solver-free fixed-state checker on graph6 `G?zTb_`, root zero,
enumerates all 6,561 assignments to the eight square edges. Exactly 72
give legal three-tree lifts and none is good in any coordinate. An
alternate good state for the same graph/root/smoothing pair does lift.

Complete controls give:

```text
order-six graphs                                      2
order-six good-state/pair instances               2,664
order-six fixed-state failures                         0
order-eight graphs / roots / pairs                4 / 32 / 672
order-eight whole-fibre failures                       0
state attempts in order-eight existential search     688
```

Thus the first fixed-state failure occurs at order eight, while the weaker
whole-fibre square implication survives every order-eight instance. See
`scratch/verify_jaeger_star_square_order6_controls.py` and
`scratch/verify_jaeger_star_square_existential_order8.py`.

## Simultaneous-triangle plateau stress

Audit date: **2026-07-28**.

The exact product-neighbour search exhausts all 3,780 two-triangle lifts
of each of two frozen order-16 boundary-free states. Among lifts with no
lower neighbour, their minimum equal-neighbour counts are respectively 14
and 7; no strict trap occurs. The second run is reproduced directly by
`scratch/search_jaeger_lifted_immediate_traps.py`.

Broader randomized sampling covers all 2,828 order-16 simple
3-edge-connected cubic graphs at root zero, every root of the order-36 APX
host, and 211 canonically distinct one- to three-triangle expansions of
that host. All replayed plateaux escape within the stated search limits.
These are explicitly exploratory state samples, not exhaustive fibre
theorems. The separate simultaneous-triangle Cartesian-product identity is
proved by hand in
`scratch/jaeger-simultaneous-triangle-lift-plateau-search.md`.

## Direct exact portfolio and local theorem audits

Audit date: **2026-07-28**.

The direct CaDiCaL portfolio checked 7,654 retained order-40 strong snarks,
their deterministic connected 2-lifts at orders 80 and 160, and three
successive Petersen four-pole substitution layers at orders 48, 56, and 64.
All 45,924 instances were SAT with raw semantic replay.  The cover-pullback
and Petersen-extension theorems subsequently explain every derived layer
from the positive bases; the large witness streams are therefore retained
locally but omitted from the curated publication bundle.

The square whole-fibre checker exhausts 14 simple 3-edge-connected cubic
graphs at order 10 and 57 at order 12.  Across 6,300 and 53,352 labelled
root/independent-edge-pair instances it finds zero failures.  Witness
digests are
`1ae75f2864163e8ec6b04c0d92f012f00375ab55f92cc1284ad8233d4c42ab8f`
and
`b6b5420643799ddfe9ab3f252b0447c7de7704b27ddd8e75eaed39613b567b4e`.
At order 14, a certificate producer covers 341 graphs, 4,774 roots, and
572,880 edge-pair instances.  A separately written standard-library checker
reconstructs every witness; the corpus uses 24,268 distinct downstairs
states and has SHA-256
`26dfe990a6655170f5fdcb6faf1424db279b57e8d094269417b7330fb5affd41`.

The sorted-profile checker exhausts the complete 867-candidate
neighbourhood of one order-36 state, finds the exact 0/13/50 split among
63 legal moves, and independently replays a distance-two same-level escape.
All three results are exact for their stated domains and are not a
resolution of FiveCDC.

## Heawood four-pole full-boundary audit

Audit date: **2026-07-28**.

The independent standard-library checker parses graph6 `KhEGHC@AI?_P`,
reconstructs the ordered 16-edge proper core and ports \((0,3,8,11)\),
checks simplicity, connectedness, bridgelessness, and girth six, then
verifies the displayed ten certificate rows.  Their 120 coordinate
permutations cover exactly all 640 xor-zero ordered boundary words.  The
frozen result JSON is byte-equal to fresh checker output, and the four-file
checksum ledger passes.

This is a complete finite boundary theorem plus a human gluing reduction;
no SAT solver or UNSAT certificate is involved.

## Fixed-label square-selection cut audit

Audit date: **2026-07-28**.

The triangular-prism checker enumerates all 540 indexed FiveCDC pair
labellings.  For the two chosen matching edges in one three-edge cut, every
labelling gives labels meeting in exactly one coordinate, as forced by the
human cut-parity identity.  It separately reconstructs the explicit
downstairs and square-local lifted tree states, both with profile
\((2,0,2)\).  The result is an exact no-go only for the proposed fixed-label
selection bridge.

## Radius-three plateau separator audit

Audit date: **2026-07-28**.

The independent standard-library checker reconstructs a simple
3-edge-connected cubic order-40 graph and literal star state with
\(d_{\min}=2\).  Its complete same-level breadth-first layers through
radius three contain 1, 13, 108, and 836 states.  Across 1,037,514
candidate exchanges, 67,392 are legal oriented arcs; no defect-zero
boundary leaves layers zero through two, while 32 such arcs leave layer
three.  An explicit shortest four-exchange path reaches defect zero.
Canonical digests of the complete radius-three ball and all scored legal
arcs are
`51aa4f3ff1efa9bebcffe0f2869919c7bd25d60c2047f8b5383b8be90d435c58`
and
`d2ad5a4bb090e43efffba60e51dec5c66037cf10465b7c43f86a2c5b3407c4ce`.
This is an exact bounded-radius no-go, not a trapped plateau or a FiveCDC
counterexample.

## Equal-profile plateau Laplacian audit

Audit date: **2026-07-28**.

The derived standard-library checker exhausts both reciprocal-exchange
neighbourhoods of two adjacent order-40 states with identical ordered
profile \((8,2,8,8,6,10,10)\).  Their legal degrees are 65 and 63, while
the coordinate Laplacians are
`(-12,140,-6,-6,28,-40,-94)` and
`(-16,134,-6,-2,34,-58,-100)`.  The resulting total-defect Laplacians are
10 and -14.  This exact sign reversal rules out a profile-only formula and
universal sub/superharmonicity for total defect.  It does not refute the
topology-sensitive plateau theorem.
