# Reproducing the five-cycle double cover laboratory

The package has a single non-destructive verification entry point:

```sh
sh tools/verify_all.sh
```

Expected final lines:

```text
PASS: the package is reproducible under the recorded scope.
NO RESOLUTION CLAIM: no target-standard UNSAT instance or universal proof exists.
ENTERED POSITIVE FRONTIER: one graph has girth 10, oddness at least 8, and a checked standard five-CDC.
```

The command validates existing reference runs and creates all fresh solver
outputs in a temporary directory. It does not overwrite a reference run. The
temporary directory is removed after success or failure.

The frontier statement concerns one explicit positive instance.  It is not a
census or clearance of the full reduced minimum-counterexample domain.

## Rooted-resolution frontier checks

The newest conditional reduction and finite controls are outside the older
master script's frozen acceptance boundary.  Run them directly:

```sh
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_root_component_distance_order16_summary.py
python3 scratch/verify_d5_root_feasibility_lift13_girth10.py
python3 scratch/verify_oum_combined_choice_12v.py
python3 scratch/verify_jaeger_tree_choice_through14.py
python3 scratch/verify_jaeger_one_tree_exchange_countermodel.py
python3 scratch/check_d5_root_port_monodromy_local_charge.py
python3 scratch/check_d5_connected_shared_coordinate_incidence.py
```

The first three commands verify the order-14 terminal census, the order-16
root-rescue census, and all 195 rooted reductions of the retained
130-vertex girth-ten graph.  The remaining commands verify exact no-go and
compression frontiers.  None is a universal FiveCDC proof.

## Jaeger fixed-fibre frontier checks

The human identities, complete order-14 census, certified 34-vertex
thinning obstruction, small no-go examples, and literal order-44 witnesses
can be checked independently with:

```sh
python3 scratch/verify_jaeger_five_point_frontier.py
python3 scratch/verify_jaeger_support5_component_criterion.py
python3 scratch/verify_jaeger_star_thinning_countermodel_34v.py
python3 scratch/verify_jaeger_34v_star_good_witness.py
python3 scratch/check_jaeger_fixed_third_tree_parity_no_go.py
python3 scratch/verify_jaeger_k_forest_petersen.py
python3 scratch/check_jaeger_perfect_forests_first_no_go.py
python3 scratch/verify_jaeger_star_parity_descent_countermodel.py
python3 scratch/verify_jaeger_kernel_closure_typea_countermodel.py
python3 scratch/verify_jaeger_kernel_closure_frontier.py
python3 scratch/verify_jaeger_fano_min_descent_frontier.py
python3 scratch/verify_jaeger_kernel_closure_order16_census.py
python3 scratch/verify_jaeger_star_kernel_closure_countermodel_16v.py
c++ -O3 -std=c++20 \
  scratch/count_jaeger_star_kernel_closure_countermodel_16v.cpp \
  -o /tmp/count_jaeger_star_kernel_closure_countermodel_16v
/tmp/count_jaeger_star_kernel_closure_countermodel_16v
python3 scratch/verify_jaeger_star_kernel_closure_triangle_expansion.py
python3 scratch/verify_jaeger_star_exact_parity_triangle_lift.py
python3 scratch/verify_jaeger_star_square_any_coordinate_lift_countermodel.py
python3 scratch/verify_jaeger_star_square_order6_controls.py
python3 scratch/verify_jaeger_star_square_existential_order8.py
python3 scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py
python3 scratch/verify_jaeger_reciprocal_exchange_defect_formula.py
python3 scratch/verify_jaeger_fano_min_immediate_descent_countermodel.py
python3 scratch/verify_jaeger_triangle_expansion_descent_structure.py
python3 scratch/verify_jaeger_triangle_expanded_fixedtrap_descent.py
python3 -m py_compile scratch/search_jaeger_lifted_immediate_traps.py
python3 scratch/search_jaeger_lifted_immediate_traps.py \
  --triangles 2 \
  --graph6 'Ot?GO?@?_G?T@IOSAIBO?' \
  --root 0 --spokes 2,1,0 \
  --omitted 1720610,271049,105492
python3 scratch/verify_jaeger_coordinate_five_order44.py \
  --input search/known_snarks/source/snarks_44.04.oddness4.cyc4.g6 \
  --witnesses output/jaeger-coordinate-five-order44/witnesses.jsonl
```

The thinning verifier invokes both pinned LRAT checkers.  The order-44
verifier does not trust producer-supplied flow values: it reconstructs the
three trees, their fundamental completions, all edge directions, and every
point-parity equation.  The reciprocal-exchange checker audits the exact
seven-plane cut formula on two frozen states.  The immediate-descent checker
verifies one positive state with no descending neighbour, a second with no
kernel-inert neighbour, and both two-step escapes.  The triangle coverage
verifier audits 13 exact fibres and
17,297,280 enumerated states but does not duplicate the C++ state
enumeration.  The square checkers prove one exact fixed-state no-go, its
order-six minimality control, and the positive whole-fibre statement in all
672 order-eight graph/root/pair instances. The simultaneous-triangle search
checks 3,780 two-gadget lifts of a frozen state; the corresponding Cartesian
product is a separate human theorem in
`scratch/jaeger-simultaneous-triangle-lift-plateau-search.md`. These commands
verify bounded or conditional claims only; the
universal star-packing selection lemma remains open.

## Required recorded environment

The byte-level audit was made on macOS arm64 with:

| tool | required recorded version |
|---|---|
| Python | 3.10.4 |
| Go | 1.26.5, darwin/arm64 |
| CaDiCaL | 3.0.1 |
| CryptoMiniSat | 5.14.7 |
| nauty `geng` | Homebrew 2.9.3, reporting Nauty&Traces 2.9301 |
| Lean | 4.32.1 |
| Lake | 5.0.0-src+f054605 |
| `lrat-check` source | commit `2e3b2dc0ecf938addbd779d42877b6ed69d9a985` |
| CakeML `cake_lpr` source | commit `a36874a8b750b43fe4b385b8ddbf5b033e46a3fa` |

Build the pinned external certificate checkers once:

```sh
sh tools/bootstrap_cert_checkers.sh
```

They are installed under ignored `.tools/cert-checkers/`. The master script
checks both Git commits before accepting either executable.

The Lean project pins mathlib commit
`520045ab14e26149ee970e2e617ca04b09bde5d6` in its Lake manifest. A clean Lean
build may download this dependency. Build products are ignored under
`formal/FiveCDC/.lake/`.

## What the master verification checks

1. It enforces the recorded tool versions and the two checker commits.
2. It verifies frozen Verifier A against `verifier_a/SHA256SUMS`.
3. It verifies Verifier B against the root-owned external freeze record
   `reproducibility/verifier-b-SHA256SUMS`, then runs Go tests, vet, and the
   race detector. Verifier B did not author this hash record.
4. It runs the Verifier A, canonical-search, structured-family, and
   obstruction unit suites.
5. It checks all 395 entries in the retained canonical run manifest and all
   104 entries in the retained obstruction run manifest.
6. It independently derives the central counts and classifications from the
   canonical summary, both structured ledgers, the structured derived
   summary, the obstruction summary, and the cross-verifier ledger.
7. It reruns the four-object Verifier A/B integration control in temporary
   storage. Both CNFs are solved, and every standard SAT model is cross-fed
   to both original-semantics checkers.
8. It checks the retained Petersen \(k=4\) LRAT with both external checkers.
   It also freshly emits LRATs for both encodings of the bridged one-edge
   control and checks each with both external checkers.
9. It runs the blind auditor against raw serialized artifacts without
   importing either verifier or any search implementation. Its output is
   redirected to temporary storage so the retained blind-audit result is not
   overwritten.
10. It runs the proof-agent’s exhaustive local checks and builds the Lean
    fixed-graph semantic formalization after verifying its source manifest.
11. It verifies the retained positive-frontier wave, including complete
    recursive manifests for the factorized \(R_2\) zero-set list, the exact
    \(R_2\) preparation audit, and the independent incremental-SAT
    cross-check, plus the compact four-block structural certificate. It
    checks the independent full-cycle audit freeze, directly validates all
    33,517 retained generic flow witnesses, compares their supports with the
    exact factorized family, and runs the focused suppression/preparation
    tests. It does not rerun the roughly 43-minute generic enumeration.
12. It verifies the minimum exact-zero matching package.  This includes
    direct semantic checks of all 92,313 minimum \(H_3\) supports and their
    five-cover witnesses, byte-for-byte reconstruction of the projected
    completeness CNF, and acceptance of its LRAT by both `lrat-check` and
    CakeML `cake_lpr`.  It also replays the switching-inequality stress test
    on those supports.
13. It verifies the full hard order-22 minimum-extension package: 12,892
    positive minimum witnesses, exhaustive non-three-edge-colourability,
    seven independently reconstructed lower-bound CNFs, and their LRATs
    under both proof checkers.  The result is finite.  A blind audit
    restored the separate \(T\)-odd-component branch before applying the
    odd-\(K_{2,3}\) packing theorem; the universal exchange lemma remains
    open.
14. It verifies the blind auditor's ten-vertex component-parity
    countermodel.  The checker independently confirms that the graph is
    simple, cubic, connected, and bridgeless; that the displayed exact-zero
    flow has two \(T\)-odd complement components and no \(T\)-join; and that
    the graph nevertheless has a Tait colouring and a standard five-cover.
    This is a countermodel to an intermediate inference, not to five-CDC.
15. It verifies the stronger 42-vertex globally minimum component-parity
    countermodel.  The checker independently reconstructs both bounded
    CNFs, checks the at-most-two LRAT with both proof checkers, recompiles
    the projected enumerator, classifies all 366 minimum supports, checks
    the explicit switch hazard, and reverse-lifts a parity-good minimum
    support to a standard five-cover.
16. It independently reconstructs the \(H_5\) Tait core and all 3,024
    five-cycle caps obtained from 252 marked-path choices and 12 cyclic
    orders modulo dihedral symmetry.  For every cap it directly checks an
    exact-zero matching of size at most two.  This is an exact finite
    corpus, not a universal theorem.
17. It reconstructs all 6,240 ordered five-pole boundary words, their 62
    color orbits and four multiset types, and the exact \(C_5\)-cap table.
    A second JavaScript implementation independently checks the core
    counts.  The retained abstract disjoint state sets show only that the
    current cap-and-switch axioms are insufficient; graph-pole realizability
    is not claimed.
18. It regenerates the pole-realizability quick census: all
    gluing-admissible five-poles through order 11 and all internally
    bridgeless four-poles through order 12.  It checks the complete state
    profiles, the sharp 46-state five-pole minimum in the internally
    bridgeless subcensus, the 9-state four-pole minimum, all \(C_5\)-cap
    intersections, and absence of a disjoint five-pole pair under every
    terminal permutation.  The frozen extended ledger reaches five-pole
    order 13 and four-pole order 14 but is regenerated only by the explicit
    `--extended` command.  Neither finite result is a universal theorem.
19. It verifies the 36-vertex \(K_6\)-defect snark plateau.  This includes
    exact graph6/splice reconstruction, all cuts of sizes one through three,
    the exhibited cyclic four-cut, girth and flow checks, a full
    \(2^{19}\)-cycle scan for all 15 switch values, an independent
    \(15\times8\) factor-transfer proof, byte reconstruction of the
    162-variable edge-colouring CNF, LRAT acceptance by both external
    checkers, a separate enumeration of all 208 perfect matchings, and the
    explicit neutral descent \(4\to4\to2\to2\to0\).  It also checks that
    this intermediate endpoint is a six-coordinate cover but omits no
    \(K_6\)-star, then checks a fifth star-cycle switch giving an explicit
    standard five-cycle double cover.  This is a certificate against an
    intermediate descent lemma, not a five-CDC counterexample.
20. It verifies the exact Petersen \(K_6\)-star barrier.  A primary census
    classifies all \(2^{24}\) abstract flow states.  An independently
    written verifier reconstructs the graph from literal edges, recovers
    all 64 binary cycles by scanning \(2^{15}\) edge subsets, checks all
    945 nonempty value-cycle switches, proves that the trapped
    triangle-only component is the free \(S_6\)-orbit of size 720, and
    checks the sharp two-switch escape \(0\to2\to0\) to an explicit
    standard five-cycle double cover.
21. It verifies the infinite Petersen-ring barrier theorem.  The human
    proof classifies both the crossing-label and remote-vertex parts of
    every triangle-preserving switch, proves the remote part is a forest,
    and derives the exact component formula \(15\cdot48^n\).  Independent
    Python and JavaScript implementations completely scan all 2,048
    binary cycles of the two-block graph, agree on its 29 nonempty
    triangle-preserving initial switches, verify the remote-forest
    condition for all 34,560 states and 15 switch values, and check the
    sharp path
    \(0\to2\to0\to2\to0\) and final standard five-cycle double cover.
    The eight-page draft in `preprint-k6-petersen-rings/` includes the
    literal human certificate and a prominent AI-assistance disclosure.
22. It verifies the cotree-diamond separation theorem.  The package
    reconstructs the 34-vertex simple bridgeless cubic graph, its
    constructive standard five-cover, the exact 153-variable/465-clause
    connected-kernel relaxation, and the six proof-shaped diamond-shore
    clauses in two independently structured implementations.  Both frozen
    target verifiers accept the positive cover.  The 20,031-byte LRAT is
    accepted by `lrat-check` and CakeML `cake_lpr`.  This proves only that
    the connected-complement sufficient condition is strictly stronger
    than ordinary five-CDC.  The seven-page draft in
    `preprint-connected-kernel-separator/` contains the complete elementary
    proof, a prominent AI-assistance disclosure, and an explicit discussion
    of the close all-edge \(K_4\) 2-cut precedent.
23. It verifies the weighted-\(T\)-join-minima countermodel.  Independent
    Python and JavaScript implementations reconstruct the 22-vertex host,
    all 512 \(T\)-joins, three exact colour-cost minima, three quotient
    forests, the forced odd-marked four-cycle, and cyclic
    4-edge-connectivity.  An explicit nowhere-zero flow proves that the
    displayed support is not globally minimum, preserving the scope of the
    still-open reduced-domain exchange theorem.
24. It verifies the fixed-join preparation trap by two independent
    implementations, including a direct scan of all \(2^{20}\) expanded
    binary cycles and both target-standard positive verifiers.
25. It verifies the 16-vertex minimum-support strict-switch plateau.  Both
    implementations reconstruct the graph, all 128 affine \(T\)-joins, all
    512 binary cycles, the complete switch profiles, the absence of a
    strictly decreasing matching-admissible switch, and the checked
    \(2\to2\to1\) neutral-descent path.  It also regenerates the exact
    canonical censuses at orders 10, 12, 14, and 16.  This is a failed
    intermediate lemma, not a five-CDC counterexample.
26. It verifies the complete support-\(\le2\) switch graphs on the six
    order-16 plateau hosts.  Independent Python and JavaScript
    implementations agree on all 33,546 ordered states and 384 strict local
    plateaus.  Every state reaches size one in the sublevel graph and every
    plateau has distance two.  This is an exact finite reconfiguration
    theorem, not a universal exchange result.
27. It verifies the complete hard order-18 support-\(\le2\) census.  A C++
    implementation and an independently written NumPy implementation agree
    field-for-field on 179 graphs, 1,680,414 ordered states, and 7,704
    strict local plateaus.  Every plateau has distance two and every state
    reaches size one.  The input hard-graph list and every output are
    hash-frozen.
28. It verifies the complete hard order-20 support-\(\le2\) census.  The
    two implementations agree field-for-field on 1,388 graphs and
    20,161,044 ordered states.  All 118,134 strict local nonpacking plateaus
    have distance two.  The only 21,492 states not reaching size one are
    the entire state space of the unique minimum-size-two graph, and every
    one already packs two \(T\)-joins.
29. It verifies all minimum size-two states on the seven hard order-22
    graphs with no size-one state.  Independent implementations agree on
    190,512 ordered states and 1,441 supports.  Fifteen supports do not
    pack, refuting the all-minima claim, but all 2,808 nonpacking
    realizations are one neutral switch from packing.
30. It verifies the complete minimum-size-three switch graph on the
    42-vertex component-parity countermodel.  Independent Python and C++
    implementations agree on 366 minimum supports, 3,670,272 ordered
    flows, 611,712 global-colour orbits, and the exact packing-distance
    profile.  Seventy-six supports do not pack; 170,352 nonpacking orbits
    have distance one and 720 have distance two; none is unreachable.
    All 720 distance-two orbits lie on support \(\{20,30,53\}\).  A
    separate Gaussian-elimination checker enumerates its 8,192 eligible
    even subgraphs, verifies the odd-marked-component obstruction, and
    checks a literal two-switch path to packing.  This refutes a
    one-switch theorem but not the universal component conjecture.

The machine-readable scope, expected hashes, counts, and classifications are
in `reproducibility/package-manifest.json`. The read-only derived report is:

```sh
python3 tools/verify_reference_artifacts.py
```

The adversarial narrative and two non-invalidating hardening findings are in
`blind-audit/REPORT.md`. In particular, Verifier A’s model-status parser is
too permissive, but the blind strict parser accepted every retained model and
checked its formula and original graph semantics.

## Scope separation enforced by the audit

### Standard target

The target uses five indexed coordinates, every edge has integer coverage
exactly two, and every vertex has even incidence multiplicity in each
coordinate. “At most five” is equivalent by padding unused coordinates with
empty edge sets. No orientation variables occur in this target.

All standard bridgeless instances in the retained computations are SAT and
carry directly checked witnesses. There is no target-standard UNSAT
certificate and no universal proof.

### Modified \(k=4\) control

The Petersen four-coordinate formula is UNSAT. Its retained LRAT is accepted
by both `lrat-check` and `cake_lpr`. This formula deliberately has four,
not five, coordinates; it validates the negative-certificate pipeline and is
not a counterexample to the five-cycle double cover conjecture.

### Bridged negative control

The one-edge graph is UNSAT in both independent CNF encodings. Both premise
checkers identify its edge as a bridge, so it fails the conjecture’s
bridgeless premise and cannot be a counterexample. The master run regenerates
and externally checks both LRATs in temporary storage.

### Orientable branch

The orientable formulation is documented separately in
`docs/orientable-encoding.md`. The retained order-38 secondary-branch
portfolio contains 298 orientable SAT witnesses with 57 ordered roots each;
the order-40 portfolio contains all 7,654 retained records with 60 roots
each. Every witness is checked directly against integer-flow conservation.
An independent standard-library order-38 audit checks all 16,986 ordered
roots, 56,620 integer balance equations, exact source-set identity, and the
complete reference CNF. The order-40 independent audit checks all 459,240
roots, 1,530,800 balance equations, exact source-set identity, and the
complete 6,000-variable/25,900-clause reference CNF. Orientable SAT implies
a standard positive witness on the same graph, but orientable UNSAT would
not imply standard UNSAT. The reproduction summary therefore reports these
positive cases separately and never promotes an orientable obstruction to
the standard target.

### Entered positive minimum-counterexample frontier

The sourced working restrictions for a minimum counterexample are girth at
least 10 and oddness at least 6.  The retained 30,450-vertex candidate-domain
specimen has girth exactly 10 and certified oddness at least 8, so the project
has entered this numeric intersection at one explicit point.  Its standard
five-coordinate formula is SAT and its witness is independently checked.
This is one positive specimen, not a census or exclusion of the restricted
domain.

### Exact finite \(R_2\) suppression/preparation wave

The complete minimal-support frontier has now reached all 298 retained
order-38 strong-snark records. Their \(2^{20}\)-word cycle spaces contain
234,582 minimal exact common-zero sets: 188,843 pairs, 44,434 triples,
1,287 quadruples, and 18 quintuples. Of these, 582 relevant supports have
\(\mu=2\), 15 have \(\mu=3\), and 1,014 are irrelevant. The 597 pointwise
exceptions occur on 119 graphs, but all 311,344,912 realizable disconnected
joins are preparable and there are no traps.

Together with the complete order-34, order-36, and \(R_2\) audits, this is
287,908 minimal supports, 10,149 relevant supports with \(\mu>1\),
329,515,008 binary-cycle classifications, and 328,184,467 realizable
disconnected joins, all preparable. These totals are explicitly finite and
do not contradict the later 38-vertex preparation trap; they do not resolve
five-CDC.

The direct order-40 screen now covers all 7,654 retained rows.  Across 60
frozen batches it classifies 6,053,028 inclusion-minimal exact zero
supports: 6,009,319 have \(\mu=1\), while 43,709 do not.  It finds zero
necessary trap candidates and hence zero preparation traps on this finite
source.  The necessity is exact: a trap high \(H\) must contain a minimal
support with \(\mu>1\) and avoid every minimal support with \(\mu=1\).
Moreover, candidate SAT with \(\kappa(E-H)=2\) would already certify a trap,
because every contained minimal support would have \(\mu=2\).

The frozen independent audit now covers all 60 batches and 7,654 graphs.
It directly checks all 6,053,028 supports, classifies
16,051,601,408 binary cycles, and internally validates 7,654
support-completeness UNSAT proofs plus 7,654 candidate CNFs.  Its support
profile and zero candidates match the primary run exactly.  Neither the
primary nor independently replayed zero-candidate result is a universal
preparation theorem or a five-CDC result.

At the small boundary, an exact census covers the 212 non-three-edge-
colourable hard bases through order 18.  Its 3,336 relevant minimal supports
have \(\mu\)-profile \((3272,63,1)\) for \(\mu=1,2,3\).  All 29,312 highs
containing one of the 64 non-\(\mu=1\) supports also contain a \(\mu=1\)
support, so there are again zero necessary candidates and zero traps.  A
producer-free standard-library audit independently rebuilds all 212 graph
identities and premises, exhausts 194,859,008 ordered cycle pairs, recovers
the entire support family, and reclassifies all 198,080 highs.  Its status
is PASS.  This is exact finite evidence only on the frozen bases.

For the retained 40-vertex \(R_2\) graph, the Petersen-pole factorization
gives the complete family of 33,517 inclusion-minimal exact common-zero
sets: 33,516 size-four matchings and one irrelevant size-six nonmatching
set. A separate incremental-SAT run produced the same support family; its
33,517 retained flow models are checked directly by the master verifier,
without repeating the long enumeration.

The independent full-cycle audit exhausts the \(2^{21}=2,097,152\) binary
cycles. It finds 6,625 connected joins, 122,510 unrealizable disconnected
joins, and 1,968,017 realizable disconnected joins, all preparable. Its
best-contained-\(\mu\) profile is exactly
\(\{0:126575,1:1970577\}\), with no preparation trap.

The separate four-block certificate explains the positive class
structurally: all 1,970,577 cycles containing a relevant support contain
one of 12,000 explicitly certified all-far type-A supports with
\(\mu=1\). The other 126,575 cycles contain no relevant support.
Its sound reusable theorem schema, including every hypothesis and the
remaining reduction gap, is recorded in
`docs/four-block-domination-template.md`.

The 70-vertex \(R_4\) graph also has a retained connected-kernel witness.
The lazy-cut search reached a connected 69-edge spanning-tree kernel after
three SAT iterations and 31 cut clauses, then lifted it to a standard
five-CDC accepted directly by frozen Verifier A. An independent
standard-library audit reconstructed all 976 CNF clauses, checked the
retained model and all 105 flow/cover labels, recovered the spanning-tree
kernel, and obtained PASS with no flaws. This is another finite positive
witness for a stronger sufficient condition; it does not establish the
condition for the recursive \(R_{2m}\) family.

The Petersen-pole tower theorem does establish the preparation condition
for the recursively generated family \(Q_m=R_{2m}\), \(m\ge1\): every
binary cycle containing an exact zero set contains an all-far exact zero set
of size \(1+3m\) with preparation minimum one. The proof uses explicit
Petersen flow and odd-factor tables plus a sound recursive gluing argument;
the executable certificate checks depths one and two without enumerating
the \(R_4\) cycle space. An independent standard-library audit matches the
entire report and all local tables, fully checks the depth-two witness and
all 127 proper subsets, and validates a depth-three recursive gluing sanity
instance.

More generally, the rooted substitution theorem proves a conditional
closure rule. If a base graph has the preparation property strengthened so
that its connected odd factor contains every designated substitution and
surviving root edge, then simultaneous Petersen-2-pole substitution on
distinct designated edges preserves the rooted property, even when those
edges share endpoints. A connected 3-edge-colourable cubic base satisfies
every rooted premise, giving a sound one-step unrooted corollary. That
corollary supplies only surviving base and new terminal roots; it does not
justify arbitrary later substitution on internal pole edges. The rooted
premise is essential to the general gluing proof, and the result does not
claim universal or unrooted closure. An independent audit reports PASS with
no gaps.

The exact adaptive one-step theorem now identifies the weakest rooted
pullback for a fixed next edge after one Petersen-2-pole substitution
\(G=B[P_2/s]\). A surviving base edge \(e'\) satisfies
\(\mathsf{RP}(G;\{e'\})\) exactly when
\(\mathsf{RP}(B;\{s,e\})\) holds, whereas either new terminal or any of the
14 internal pole edges requires exactly \(\mathsf{RP}(B;\{s\})\). Thus a
nested sequence may continue along a fixed terminal or internal edge of the
newest pole without accumulating all deeper roots. This does not permit an
arbitrary surviving or branching next edge. A clean-room audit independently
enumerates the 64 binary pole states, 4,096 flow states, all 16,384 internal
edge subsets, and all 882 nonempty-high/internal-root obligations. It finds
exactly five admissible connected fragments, of which the four stated
fragments are exactly those able to omit a far zero. The same audit rebuilds
the order-18 pair obstruction and all 32,768 cycle complements of its
order-28 substitution: all 150 connected odd factors containing surviving
root 19 project correctly, and none projects to an eligible factor containing
both base roots. This is an exact rooted transfer result and finite boundary
witness, not a five-CDC result or universal unrooted closure.

Iterating the terminal/internal half of that transfer gives an explicit
infinite nested family. From any fixed singleton-rooted base
\((B,s_1)\), every depth-\(m\) construction has order
\(|V(B)|+10m\), size \(|E(B)|+15m\), the root-free preparation property,
and 16 separately valid next roots in its newest pole. The 16 rooted
statements do not demand one common factor: the next edge is fixed before
the current high is quantified, and its witness may depend on both. A
clean-room construction checks all 14 internal and two terminal
continuations, and an exact base-to-internal-to-terminal depth-three path
at orders 10, 20, 30, and 40 contracts back to Petersen.

The associated zero-coverage census is finite and exact. A different
cycle-space-signature algorithm parsed, premise-checked, and canonically
identified every one of the 7,984 frozen order-34/36/38/40 source rows.
It exhaustively compared all 14,067,888 edge pairs and found no two-edge
cut. Since a forward cut Petersen pole has a nonempty ten-vertex shore whose
boundary consists exactly of its two terminal edges, every such pole would
create a two-edge cut. Consequently none of these 7,984 retained graphs
contains even the first required pole, and the covered identity list is
empty. This says nothing about other graphs or about five-CDC.

An exact finite census separately tested whether the rooted premise is
already forced by unrooted preparation on every connected simple bridgeless
cubic base through order 18. It canonically checked 44,327 bases and
1,181,250 base-edge singleton-root pairs. The 44,115 3-edge-colourable
bases have a uniform witness; complete cycle-code enumeration on the other
212 bases covered 194,859,008 ordered flow pairs and 5,216,238
realizable-high/root obligations. No unrooted or singleton-root failure was
found. A separately written checker regenerated all 45,982 canonical cubic
classes, independently reclassified the 212 hard graphs, rebuilt every
exact-zero-set family, and obtained PASS. This is finite evidence only: it
does not prove that the rooted hypothesis is redundant, and it has no
five-CDC conclusion. Because no eligible base edge was found, no
failure-driven substitution stage was performed.

The singleton result does not extend to simultaneous roots. An exact census
of all 71,313 edge pairs on the 212 hard bases checks 67,244,094
realizable-high/pair obligations. Nine root pairs fail on two order-18
graphs, across 128 highs and 144 obligations; all lower-order pairs pass.
An independent producer-free replay rebuilds every one of the 212 cycle
codes, exact-support families, connected odd factors, and unordered
pair-root obligations and matches all aggregate counts and the first
witness.
On the first retained 18-vertex graph
`Q????B?K?WWCg_?sIG?s?HO?KG?`, every singleton-root
obligation passes, but the binary high with edge set
\(\{0,2,3,5,10,11,18,20\}\) fails for roots \(\{9,19\}\). Its five
contained minimal supports are
\(\{10\},\{11\},\{18\},\{20\},\{2,5\}\). An independent complete
cycle-code replay finds exactly 13 connected odd factors avoiding at least
one candidate and none containing both roots; the pair-rooted minimum is
two for every candidate. This refutes only the attempt to infer a
multi-root preparation premise from singleton-root preparation. It does not
refute the conditional substitution theorem and is not five-CDC UNSAT.

This is an infinite positive structural family, not an infinite
counterexample family and not a universal five-CDC proof. The theorem and
its scope are in `docs/petersen-pole-tower-preparation-theorem.md`. The
general suppression characterization and remaining unrestricted
high-specific condition are documented in
`docs/suppression-zero-sets-and-connected-complements.md`.

## Retained reference results

| reference | central outcome | SHA-256 |
|---|---|---|
| fixed-join preparation trap `SHA256SUMS` | 38 vertices, 125 minimal exact supports all with preparation minimum two; standard five-cover SAT | `4d732e47f5e87c35492410228acf1b59e969560e229d47f50461c152db1bb775` |
| weighted \(T\)-join minima countermodel `SHA256SUMS` | weighted bounds and quotient forests do not force packing; displayed support nonminimum | `f1bebcc0e86530a6d5de9f115b3e3117a88d11821d0d45f5b36a1f243a5a8a5a` |
| connected-kernel separator preprint `SHA256SUMS` | seven-page human-checkable AI-disclosed draft, revised novelty scope, retained referee report | `8f7c3918ee2b7d159b84ffd3a753b03f666cf6d051f9a8860fdaf93b628061fe` |
| cotree-diamond separator `SHA256SUMS` | 34-vertex standard five-cover SAT; connected-kernel relaxation UNSAT with two-checker LRAT | `d65e11007860ac98306847915c96c3353932e42e88b4ccb5f92d6487bb6280b7` |
| canonical `summary.json` | 27 generated classes, 26 bridgeless, 26 SAT by each solver | `143f0497588de3bbb264a7cfda607150473687a036c714dbfa2eacfb48d7c2ab` |
| canonical `SHA256SUMS` | 395 retained entries | `30d9f41a5cfcc1b247c9fbdb3ff4b0b29b1608dce20c2da7d642517d329a48cf` |
| obstruction `summary.json` | standard Petersen \(k=5\) SAT; modified \(k=4\) certified UNSAT | `aada0cf923771abffa8cd6d76e9d745fc1a914df8e25c3498f4091d52465db83` |
| obstruction `SHA256SUMS` | 104 retained entries | `1bbf5d30b935417c8115edb90014d3022fcd6fcb60d2926442068fe2243026d4` |
| structured primary ledger | 28/28 standard instances SAT | `a18315521b3aa25d5b57006d41c1a5ff073549fe6e2e2223c7c636410dda00e5` |
| structured Verifier B ledger | 28/28 witnesses independently accepted | `a0fcb28faebe9159060d066b48a0c4dd13173db1cb960154fe14dfbd4c59bc77` |
| structured derived summary | zero rows in the girth/oddness intersection | `5b9240a09eb8eb4095494c1d6e815985269d958f9342d81572eb8663a31b46f8` |
| cross-verifier ledger | three standard SAT objects; one bridged UNSAT control | `d0d4419615ba1f011847cb30a0d4a52ac197efdb1cba2718f6648516550dc055` |
| \(R_2\) factorized zero-set `SHA256SUMS` | complete 33,517-support family | `58004c6d077fe3d75c4715ad8fae82c86ee25239ecdf2684d8c398f452959a87` |
| \(R_2\) preparation `SHA256SUMS` | all 1,968,017 realizable disconnected joins preparable | `11d8768991e93de766d56411789c13899833d9ee26e212d3aa32b865bb83a783` |
| \(R_2\) incremental-SAT `SHA256SUMS` | 33,517 directly validated models; exact support-set equality | `f8b17a7839964d9ab4da40953d4153a8c2a7a0c8d1160361472b38d9bb7917ee` |
| \(R_2\) four-block certificate `SHA256SUMS` | 1,970,577 support-containing cycles structurally dominated by \(\mu=1\) supports | `781fb31f9bc772e91f2d28ed0de7a5e489ce36eaf00238a638524a19a61d71f5` |
| independent \(R_2\) audit freeze | PASS; exact full-cycle classification | `a5dd710119e36f7982b33d00f668470162db578fb31338e41a052f90832c35d5` |
| independent \(R_2\) four-block audit manifest | PASS; 2,097,152 tuples and 12,000 glued factors checked | `9cff4cebf5a53c465bd019302dd8ae01d86880afc3a348b565522df7c0294034` |
| \(R_4\) connected-kernel `SHA256SUMS` | 70 vertices, 69-edge spanning-tree kernel, checked lifted five-CDC | `36e51f6843447a88fa2329fa40f60f4e104184fc1047e807cbddb49f4551ef45` |
| independent \(R_4\) connected-kernel audit manifest | PASS; CNF, flow, kernel, lift, and direct semantics reconstructed | `33ea61cebc1a21e429aabd896c18a94a1f3255e1d1e6c168819dc5592f4ba4c4` |
| Petersen-tower certificate `SHA256SUMS` | preparation theorem for every \(Q_m=R_{2m}\), with \(R_2/R_4\) executable instances | `9d234c9606daee3b30690c08483d86d8d9474289ad4ba1c126728b237d5101a9` |
| independent Petersen-tower audit manifest | PASS; report, local tables, depth 1/2 witnesses, and depth-3 sanity checked | `f047c4ee2b282f6f54dba669b234040d0802165bfcc8a8a0b4e23ab3047856c5` |
| rooted Petersen-2-pole closure `SHA256SUMS` | conditional rooted substitution closure; no universal or unrooted claim | `3862fef08af8d2aff4f8be9bdce21ceced72b64a9cc6428bb6bfb20501a32f05` |
| independent rooted-closure audit freeze | PASS with no gaps; local reconstruction, shared endpoints, arbitrary terminal subsets, and one-step corollary checked | `79b7d5f6b8db2a04e45bbbbb82a2d5ecea9cd018c1f3970861d714c5793e8031` |
| adaptive sequential Petersen-2-pole closure `SHA256SUMS` | exact surviving/terminal/internal pullbacks and order-28 boundary witness | `af05e5946416abe94c0f5b41a4c9ef68271311b2e274e9b0b88cb2fef2be3c2e` |
| independent adaptive sequential closure freeze | PASS; complete cut-state/fragment enumeration and order-18/order-28 projection replay | `5d5a83e0f33fecea6c697afd8efe79a184a7cb94b59d3c5ca8b6b9df9f42cfe2` |
| nested Petersen-pole family/reduction census `SHA256SUMS` | infinite rooted preparation family; exact zero coverage on 7,984 frozen rows | `365182246f383488acb3854bf432ca37052f6d8c4bac95445ff325e4a6aa8005` |
| independent nested-family/zero-coverage freeze | PASS; all 16 continuations, depth-three control, 7,984 identities, and 14,067,888 edge pairs checked | `964c902a2ac62ca7465e1ea2661ca13d0bd3f9907f64ede5cfcacd1566e9b4d1` |
| order-40 direct trap-candidate screen `SHA256SUMS` | 7,654 retained graphs, 6,053,028 minimal supports, zero necessary candidates | `53f8508433cc399a9954696a3bf7b3f91a18eeecf6ed0c1eaed6bb1ec41b2b96` |
| independent order-40 full trap audit ledger | PASS on all 60 batches, 7,654 graphs, 6,053,028 supports, and 16,051,601,408 binary cycles | `fb9ebf90f57453efff948dd6d9cbc05c76bb086cdedc42e2396adaf94761c457` |
| small-boundary necessary-candidate census `SHA256SUMS` | 212 hard bases, 3,336 supports, 29,312 dominated highs, zero candidates | `b1d4bd065957c844e72ad471e4d9bc0f2732628488c1acbd3f1ab66dd62d972f` |
| independent small-boundary census freeze | PASS; all identities, 194,859,008 ordered cycle pairs, supports, and highs rebuilt | `2be94696a0161f7dedd3a19343c1e9dfdb47ac61e05db650128aa57ef78494a7` |
| canonical order-20 preparation census `SHA256SUMS` | 510,489 cubic classes, 21,686 hard supports, 425,024 dominated highs, zero candidates | `a6cae1428bdf0da96246f3126b3feb3d9ba8c9d12c3349de39fc0a34e1eed922` |
| order-20 near-candidate profile `SHA256SUMS` | exact minimum domination margin three on 2,240 highs | `5943313f166cc470912754aaf5d9c0973ea8e90e8297f19e8f1b0f0fa0dee631` |
| independent order-20 clean-room ledger | PASS; all 510,489 identities and 5,821,693,952 ordered cycle pairs replayed | `99773ca7932a0b464fb6ae811ba52df2d58e0f6e7bc27b30078f2af729a1a040` |
| complete order-22 filter census `SHA256SUMS` | 7,319,447 canonical rows, 12,892 hard rows, 20 strict rows | `d54e2beb98bfb690903f10593d51483ab3052259d45c2e40d9e98451acd09a64` |
| strict standard-5CDC through order 18 `SHA256SUMS` | 3/3 direct and dual-semantic SAT witnesses | `68be23a56d4ebd31d5d73c85ef628c7fe8b43a2c4cc7e82a440ba76686225f88` |
| strict standard-5CDC order 20 `SHA256SUMS` | 6/6 direct and dual-semantic SAT witnesses | `8e5e62f6c16d714cff96db34da264001072dbc31797830026257c406ed33d93f` |
| strict standard-5CDC order 22 `SHA256SUMS` | 20/20 direct and dual-semantic SAT witnesses | `c5fef35d4c23842ef72721f7cc3e8602497d322a162d5b1c207c47f47d6989df` |
| independent finite cubic boundary through order 22 | PASS; full stream/filter replay, 29 complete model checks, bounded multigraph corollary | `2927237e34ebf3e8820eef8498ea7bea45df2f8e17adf903da535b64ffe3216a` |
| rooted-preparation necessity census `SHA256SUMS` | no rooted/unrooted failure through order 18; finite evidence only | `c029297da39a355d73b2d58602d00ec5521fb8393b05679b981b08664c6792c2` |
| independent rooted-preparation census freeze | PASS; canonical generation, 212 hard cycle codes, and 5,216,238 root obligations independently checked | `699a2b6b57b0ee639f195d5fc76f41b0045959d8f4a2740569c0b5b72f1b92c8` |
| independent pair-root preparation obstruction freeze | PASS; full 1,024-cycle replay, exact supports, odd factors, and global singleton audit | `02e08a92626a9998e20c574f048eeb8e9fb4600944ba9e3bb6cee545d46883dd` |
| multi-root preparation census `SHA256SUMS` | first pair-root failure at order 18; 71,313 pairs and 67,244,094 high/pair obligations checked | `b3794f6368c4797f2eb8327eb07e31f7eb88edbf0c0e436fabbb99a3b199c937` |
| independent full multi-root census freeze | PASS; all 212 cycle codes, support families, odd factors, and pair-root obligations rebuilt | `b43dd84c44c2691f245bf330554e838a53c9b254779701c6d15d836adeae3924` |
| order-38 minimal-zero-set audit `SHA256SUMS` | 234,582 supports and 311,344,912 realizable joins; zero traps in 298 retained graphs | `2900fd4fee0591878845f78e842aaf75adc25d8efec7c58f056aa9dce7a18d39` |
| independent order-38 minimal-zero-set audit freeze | PASS; all retained witnesses, family completeness, and 312,475,648 high cycles independently checked | `3b0ca93f2fbd46f6801a7e54f7352d28292454d07588b9507bd671d17c04bfde` |
| preparation-margin profile audit `SHA256SUMS` | PASS; 131,596,288 affected highs on 134 order-34/36/38 graphs independently reconstructed | `8c952b78dfff62f6186fef27e4b8cce610e1c226868c17532263d3e44105b27d` |
| peripheral-cycle singleton audit `SHA256SUMS` | PASS; universal theorem audited and all 29,037 edges on 985 finite controls checked | `f81e6f7f92e246835d42dfadb74f8ef07efad0021b6d4523fdacd6149bf65f86` |
| two-edge marked-core reduction audit ledger | PASS; 1,439 exact pairs, both girth-five geometries, and 19,624 fixed-subgraph parity checks | `de795daf3985565618dc16bb3d674c01b81405417fe2bea4ee6308b9881c98d0` |
| targeted marked-core exact-pair search `SHA256SUMS` | PASS; 291 affine failures, 858 Tait reconstructions, and 2,475 Flower-snark exact pairs checked | `349ced54ee9d6704ccf0d1a9f2b785975a81840bcf3deeb6cd42980535acb16c` |
| exact-pair theorem-resolution package ledger | PASS; \(K_4\) and dodecahedral literal exceptions plus all 13,547,580 pairs on 7,654 order-40 strong snarks | `0957e46c0d93fb486d3183933ed4d7f69cc0e1732315475a68eb6ed6910e4fde` |
| five-CDC label-packing package ledger | PASS; ten quotient-zero classes and the \(\nu(\mathcal M(G))\geq10\) obstruction, checked on Petersen/\(R_2\)/\(R_4\) | `1f0a195a6e81aa6d3628a668ed5c214bacad39e135390ce4c9551cbb1b9092dd` |
| affine-relabel quotient-lift `SHA256SUMS` | PASS; all 30 affine structures and 210 lines, zero lifts for the supplied coordinate-tree 8-CDC | `8c51ad2e65c5154b220e762f81e724cc515deeecf6c7d1fd5d3f55f7c6c461ff` |
| reconstructed \(H_2\) `SHA256SUMS` | PASS; cyclic connectivity 5, certified flow resistance 2, \(\mu=1\), and standard five-CDC SAT | `4babacb2794429d0eb74f5e8ee54a911ff21116d97b7c820a1bf9dd1a98f2870` |
| independent reconstructed-\(H_2\) audit ledger | PASS; raw reconstruction, all 9,388,877 small cuts, LRAT, exact pair, and five-cover replayed | `b7a8924312867cbf2292491b5581e2791eddb61e40c69607eae73e74fa2db652` |
| reconstructed \(H_3\) `SHA256SUMS` | PASS; cyclic connectivity 5, certified flow resistance 3, and standard five-CDC SAT | `d019c2f36a4a3ad392a00b4de64fa150c22ace4615d715583e015e14ba51e99f` |
| independent reconstructed-\(H_3\) audit ledger | PASS; graph, LRAT, direct cover, and matching reverse lift replayed | `929a46366e9275c6fe5603caa65ac61f41b318045534bba713b4f9d7e6fe0260` |
| reconstructed \(H_4\) `SHA256SUMS` | PASS; cyclic connectivity 5, certified flow resistance 4, and standard five-CDC SAT | `f7866131334940d4e8a98f56b9a530b8cc98a85b02124d2c8b235297a2ff39c4` |
| independent reconstructed-\(H_4\) audit ledger | PASS; both LRATs, both direct models, and matching reverse lift replayed | `4a9b1c26ee46aa7c2e49409464ccdb4d0757cb8f97825f7963c75bd049d91d98` |
| reconstructed \(H_5\) `SHA256SUMS` | PASS; cyclic connectivity 5, certified flow resistance 5, and standard five-CDC SAT | `cb8cb3b7cbdbd698c0e73b979e0f777249e2ea15b175cc94571f519a8ddff0a5` |
| independent reconstructed-\(H_5\) audit ledger | PASS; both LRATs, both direct models, and matching reverse lift replayed | `480e6ec07eb27c42259af23c0597d793b01848fc08d5367ed433f8d004817dc4` |
| stable \(D_5\)-tile family package ledger | PASS; frozen \(\widehat H_n\) standard five-CDC for every \(n\ge2\), 55-edge tile, \(H_2\)--\(H_5\) exact replays, Lean check | `e09cee11f74b19e4a08f18c94534207e44f601a29f059a15fb614154900cbfac` |
| MNP oddness-two novelty-audit ledger | PASS; human all-\(n\) deduction plus \(H_2\)--\(H_5\) matching controls and 8,190 transition patterns | `3dc1455e0290624e9d6c678b6e5b0ef1115cdc68c1dcdef6d29587a0e2686e81` |
| stable-tile preprint draft | 11-page PDF, explicit scope and AI disclosure, tile appendix, switching and quotient-forest proofs, visual QA PASS; not circulation-ready | `55d4d8aee19abe53c8e1d36418834c996e8acb0b9fc239aa9884e7f045510bf9` |
| minimum exact-zero matching package ledger | PASS; all 92,313 minimum \(H_3\) supports extend, H4/H5 minimum witnesses, two-checker projected-completeness LRAT | `623c4d27043934fcca68534f66c252e62357714916d467a1b349b66debf19904` |
| minimum switching audit ledger | PASS; all 92,313 frozen minimum \(H_3\) supports satisfy all three color inequalities; human proof is separate | `2291fb5a04d69d1e6ecea3e965bff32b4e19208a124a1d3f63b89f28cd3be7f7` |
| component-parity \(T\)-join countermodel ledger | PASS; ten-vertex exact audit countermodel to the unqualified cut claim, with an explicit five-cover positive control | `6be9aea938f86339e803b3803d208f4b1d0b14a226cae580b0df3663b68b83d2` |
| globally minimum component-parity countermodel ledger | PASS; 42-vertex minimum size-three parity-bad support, dual-checked LRAT, 366-support projection, and explicit five-cover positive control | `c6827a147ac5185ee8dabe3504e3ee9ef6a995b5ccb6dfa800fefe860f3a30db` |
| minimum size-three neutral escape ledger | PASS; literal globally minimum nonpacking support and one neutral switch to an explicit two-\(T\)-join packing | `bc8cfb145470a0689e6a136100c3c1ee174e638b022b2321aa73c47454f16214` |
| minimum size-three packing-component census ledger | PASS; 366 supports, 611,712 colour orbits, all nonpacking states within two neutral switches of packing | `0a36bd4b1f70cd4288e60a4b677aead723efeef7acc90b5037909d36098b299d` |
| full hard order-22 minimum-extension ledger | PASS; 12,892 extending minimum witnesses and seven two-checker lower-bound LRATs | `ed334f2df4131ed29b2924e4178e7f7853cf5a143e0427ac91ebb2c274d343f5` |
| orientable order-38 `SHA256SUMS` | separate secondary branch: 298/298 orientable SAT with direct root validation | `09634c7df6d1ae7faf0bd4bc1b1b8d07a5237ab0bb61405b35972ce32fd1e187` |
| independent orientable order-38 audit manifest | PASS; source set, roots, balances, and complete reference CNF checked | `f76e1d0c49ab1ea6cbd6a6ef73ab200da219a9baae755b1febaf51348dc1bc75` |
| orientable order-40 `SHA256SUMS` | separate secondary branch: 7,654/7,654 orientable SAT with direct root validation | `79317952a74da865e263889d5fe98e30430acd9682140dedb034a13e167b4cff` |
| independent orientable order-40 audit freeze | PASS; all 7,654 rows, roots, balances, and complete reference CNF checked | `59c7b7c4fa947c586e43ae461064923a870897ea43d3209c6dfac4987551c8cc` |

The canonical and obstruction runs are retained under `search/` and have
their own manifests. Structured and cross-verifier outputs are intentionally
ignored under `artifacts/`; their expected hashes and derived counts are
still frozen in the root reproducibility manifest.

If the ignored structured directory is absent, reconstruct it only when the
target path does not exist:

```sh
python3 -m search.structured.run_portfolio \
  --output artifacts/structured \
  --solver-timeout 120 \
  --oddness-timeout 120
python3 -m search.structured.crosscheck_verifier_b \
  --artifacts artifacts/structured
python3 -m search.structured.summarize_results
```

The runners intentionally refuse to overwrite output. To repeat the
canonical or obstruction experiments without touching the reference runs,
choose a new directory:

```sh
python3 search/canonical/canonical_search.py \
  --min-n 4 --max-n 10 \
  --geng "$(command -v geng)" \
  --cryptominisat "$(command -v cryptominisat5)" \
  --cadical "$(command -v cadical)" \
  --solver both \
  --oddness-max-vertices 10 \
  --cover-canon-max-vertices 10 \
  --output search/canonical/runs/reproduction-n10

python3 search/obstructions/run_experiments.py \
  --run-dir search/obstructions/runs/reproduction-control
```

Use unique names if either example directory already exists.

The retained \(R_2\) wave can be checked quickly without repeating the
generic enumeration:

```sh
(cd search/r2-pole-zero-set-audit-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/r2-preparation-audit-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/r2-incremental-sat-zero-set-crosscheck-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/r2-block-preparation-certificate-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd blind-audit &&
  shasum -a 256 -c r2-pole-zero-set-full-audit-SHA256SUMS)
shasum -a 256 \
  blind-audit/r2-four-block-certificate-audit-manifest.json \
  blind-audit/r2-four-block-certificate-audit-result.json \
  blind-audit/audit_r2_four_block_certificate.py
python3 -m unittest \
  tools.test_r2_pole_zero_sets \
  tools.test_r2_preparation_audit \
  tools.test_r2_block_preparation_certificate \
  tools.test_suppression_zero_set -v
python3 -m unittest \
  tools.test_minimal_zero_set_audit.MinimalZeroSetAuditTests.test_incremental_helper_matches_small_exact_supports \
  -v
(cd search/minimal-zero-set-audit-n38-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c \
  blind-audit/minimal-zero-set-n38-audit-SHA256SUMS
python3 -m unittest tools.test_minimal_zero_set_audit -v
(cd search/preparation-margin-profile-audit-20260725 &&
  shasum -a 256 -c SHA256SUMS)
python3 -m unittest discover \
  -s blind-audit -p 'test_preparation_margin_profiles.py' -v
(cd search/peripheral-cycle-singleton-audit-20260725 &&
  shasum -a 256 -c SHA256SUMS)
python3 -m unittest discover \
  -s tests -p 'test_peripheral_cycle_singleton_audit.py' -v
shasum -a 256 -c \
  blind-audit/two-edge-zero-set-core-reduction-audit-SHA256SUMS
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest \
  blind-audit/test_two_edge_zero_set_core_reduction_audit.py -v
(cd search/marked-core-exact-pair-search-20260725 &&
  shasum -a 256 -c SHA256SUMS)
python3 tools/verify_marked_core_search_report.py \
  search/marked-core-exact-pair-search-20260725/bipartite/report.json \
  search/marked-core-exact-pair-search-20260725/tait/report.json \
  search/marked-core-exact-pair-search-20260725/mixed/report.json
python3 -m unittest discover \
  -s tests -p 'test_marked_core_exact_pair_search.py' -v
(cd search/exact-pair-theory-resolution-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
(cd search/five-cdc-label-packing-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
(cd search/eight-cover-affine-relabel-audit-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
python3 -m unittest discover \
  -s tests -p 'test_fano_pointwise_compression_audit.py' -v
python3 tools/fano_pointwise_compression_audit.py >/dev/null
(cd search/mnp-h2-flow-resistance-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c blind-audit/mnp-h2-audit-SHA256SUMS
python3 blind-audit/audit_mnp_h2.py \
  --output /tmp/mnp-h2-independent-result.json
cmp /tmp/mnp-h2-independent-result.json \
  blind-audit/mnp-h2-independent-result.json
(cd search/exact-zero-partition-relaxation-h2-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
(cd search/matching-four-flow-h2-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
(cd search/matching-component-parity-order34-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
python3 -m unittest \
  tools.test_matching_component_parity_audit -v
(cd search/petersen-nonextendible-two-factor-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
python3 -m unittest tools.test_fixed_coordinate_five_cdc -v
(cd search/mnp-h3-flow-resistance-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c blind-audit/mnp-h3-audit-SHA256SUMS
.tools/cert-checkers/drat-trim/lrat-check \
  search/mnp-h3-flow-resistance-20260725/flow-at-most-two-zero.cnf \
  search/mnp-h3-flow-resistance-20260725/flow-at-most-two-zero.lrat
python3 -m unittest blind-audit/test_mnp_h3_audit.py -v
python3 blind-audit/audit_mnp_h3.py \
  --output /tmp/mnp-h3-independent-result.json
cmp /tmp/mnp-h3-independent-result.json \
  blind-audit/mnp-h3-independent-result.json
(cd search/mnp-h4-flow-resistance-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c blind-audit/mnp-h4-audit-SHA256SUMS
python3 -m unittest blind-audit/test_mnp_h4_audit.py -v
.tools/cert-checkers/drat-trim/lrat-check \
  search/mnp-h4-flow-resistance-20260725/flow-at-most-three-zero.cnf \
  search/mnp-h4-flow-resistance-20260725/flow-at-most-three-zero.lrat
.tools/cert-checkers/cake_lpr/cake_lpr \
  search/mnp-h4-flow-resistance-20260725/flow-at-most-three-zero.cnf \
  search/mnp-h4-flow-resistance-20260725/flow-at-most-three-zero.lrat
.tools/cert-checkers/drat-trim/lrat-check \
  search/mnp-h4-flow-resistance-20260725/cyclic-cut-at-most-four.cnf \
  search/mnp-h4-flow-resistance-20260725/cyclic-cut-at-most-four.lrat
.tools/cert-checkers/cake_lpr/cake_lpr \
  search/mnp-h4-flow-resistance-20260725/cyclic-cut-at-most-four.cnf \
  search/mnp-h4-flow-resistance-20260725/cyclic-cut-at-most-four.lrat
(cd search/mnp-h5-flow-resistance-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c blind-audit/mnp-h5-audit-SHA256SUMS
python3 -m unittest blind-audit/test_mnp_h5_audit.py -v
.tools/cert-checkers/drat-trim/lrat-check \
  search/mnp-h5-flow-resistance-20260725/flow-at-most-four-zero.cnf \
  search/mnp-h5-flow-resistance-20260725/flow-at-most-four-zero.lrat
.tools/cert-checkers/cake_lpr/cake_lpr \
  search/mnp-h5-flow-resistance-20260725/flow-at-most-four-zero.cnf \
  search/mnp-h5-flow-resistance-20260725/flow-at-most-four-zero.lrat
.tools/cert-checkers/drat-trim/lrat-check \
  search/mnp-h5-flow-resistance-20260725/cyclic-cut-at-most-four.cnf \
  search/mnp-h5-flow-resistance-20260725/cyclic-cut-at-most-four.lrat
.tools/cert-checkers/cake_lpr/cake_lpr \
  search/mnp-h5-flow-resistance-20260725/cyclic-cut-at-most-four.cnf \
  search/mnp-h5-flow-resistance-20260725/cyclic-cut-at-most-four.lrat
python3 blind-audit/audit_mnp_h5.py \
  --output /tmp/mnp-h5-independent-result.json
cmp /tmp/mnp-h5-independent-result.json \
  blind-audit/mnp-h5-independent-result.json
(cd search/mnp-stable-tile-five-cdc-20260725 &&
  shasum -a 256 -c SHA256SUMS)
python3 search/mnp-stable-tile-five-cdc-20260725/verify_stable_tile.py
python3 search/mnp-stable-tile-five-cdc-20260725/test_stable_tile.py -v
python3 search/mnp-stable-tile-five-cdc-20260725/verify_package.py
(cd formal/FiveCDC && lake env lean \
  ../../search/mnp-stable-tile-five-cdc-20260725/MNPStableTile.lean)
(cd search/mnp-oddness-two-novelty-audit-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_novelty_audit.py)
(cd preprint && shasum -a 256 -c SHA256SUMS)
(cd search/minimum-zero-matching-five-cdc-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify_package.py)
(cd search/component-parity-tjoin-countermodel-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify.py)
(cd search/minimum-component-parity-countermodel-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify.py)
(cd search/h5-core-cap-flow-bound-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify.py)
(cd search/five-pole-c5-boundary-calculus-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify.py)
node blind-audit/five-pole-cap-calculus-independent.js
shasum -a 256 -c \
  blind-audit/preparation-trap-candidate-n40-full-audit-SHA256SUMS
(cd search/order22-filter-census-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/through18-strict-standard-five-cdc-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/order20-standard-five-cdc-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/order22-standard-five-cdc-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c \
  blind-audit/order22-finite-package-audit-SHA256SUMS
python3 -m unittest -v \
  blind-audit/test_order22_finite_package_audit.py
```

The branch-specific order-\(98\) incidence closure has a smaller direct
replay:

```sh
python3 scratch/verify_diagonal_c14_c10_triple_overlap.py
clang++ -std=c++20 -O3 \
  scratch/verify_marked_two_factor_overlap_caps.cpp \
  -o /tmp/verify_marked_two_factor_overlap_caps
/tmp/verify_marked_two_factor_overlap_caps
python3 scratch/enumerate_order98_incidence_system.py
python3 scratch/check_order98_incidence_system_z3.py
python3 scratch/check_order98_diagonal_cap_control.py
python3 scratch/audit_order98_incidence_system_independent.py --prune-off
```

The last command uses SciPy/HiGHS as a supplementary third formulation.
The solver-free census and its prune-free replay are the transparent
finite proof.

The order-\(100\) continuation first reproduces the cap-table and exact
row-star reductions, then checks the three profile-level CNFs:

```sh
python3 scratch/enumerate_order100_incidence_relaxation.py
python3 scratch/check_order100_incidence_relaxation_z3.py
python3 scratch/enumerate_order100_exact_row_star_relaxation.py
python3 scratch/check_order100_exact_row_star_z3.py

c++ -std=c++20 -O3 scratch/cadical_incremental_server.cpp \
  -I/opt/homebrew/include /opt/homebrew/lib/libcadical.a \
  -o /tmp/cadical_incremental_server

python3 scratch/solve_order100_global_profile_sat.py \
  --profile 0 --cnf scratch/order100-global-profile0-final.cnf
python3 scratch/solve_order100_global_profile_sat.py \
  --profile 1 --cnf scratch/order100-global-profile1-final.cnf
python3 scratch/solve_order100_global_profile_sat.py \
  --profile 2 --cnf scratch/order100-global-profile2-final.cnf

python3 scratch/check_order100_global_profile_cnf.py \
  --profile 0 --cnf scratch/order100-global-profile0-final.cnf
python3 scratch/check_order100_global_profile_cnf.py \
  --profile 1 --cnf scratch/order100-global-profile1-final.cnf
python3 scratch/check_order100_global_profile_cnf.py \
  --profile 2 --cnf scratch/order100-global-profile2-final.cnf
```

For each frozen CNF, the retained LRAT can be checked with
`lrat-check CNF LRAT`; the expected output is `VERIFIED`.  The semantic
checker is producer-free and separately validates every appended lazy
clause as a forced short circuit.

Together these commands prove only the connected eight-mark extremal
exact-zero size-four branch bound \(|V(G)|\ge102\), not the five-cycle
double cover conjecture.

The \(R_4\) positive witness and tower theorem can likewise be checked
without rerunning either search:

```sh
(cd search/connected-kernel-r4-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/r4-tower-preparation-certificate-20260725 &&
  shasum -a 256 -c SHA256SUMS)
python3 -m verifier_a check-model \
  search/candidate_domain/runs/domain-20260725-v1/\
compositional-five-cdc-v4/r4.graph.json \
  search/connected-kernel-r4-20260725/lifted-cover.model
python3 -m unittest \
  tools.test_petersen_tower_preparation_certificate \
  tools.test_petersen_2pole_substitution_closure \
  tools.test_petersen_2pole_adaptive_sequential_closure -v
(cd search/petersen-2pole-adaptive-sequential-closure-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c \
  blind-audit/petersen-2pole-adaptive-sequential-closure-independent-SHA256SUMS
(cd search/nested-petersen-pole-reduction-census-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c \
  blind-audit/nested-petersen-pole-family-independent-SHA256SUMS
(cd search/order20-mu1-candidate-census-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/order20-mu1-near-candidate-analysis-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c \
  blind-audit/order20-mu1-cleanroom-independent-SHA256SUMS
(cd search/rooted-preparation-necessity-census-n18-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/rooted-preparation-multi-root-census-n18-20260725 &&
  shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c \
  blind-audit/rooted-preparation-census-n18-independent-SHA256SUMS
shasum -a 256 -c \
  blind-audit/pair-root-preparation-obstruction-SHA256SUMS
shasum -a 256 -c \
  blind-audit/rooted-preparation-multi-root-census-n18-independent-SHA256SUMS
python3 -m unittest \
  tools.test_rooted_preparation_hypothesis_census -v
python3 -m unittest \
  tools.test_rooted_preparation_multi_root_census -v
(cd search/k6-defect-switch-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify.py &&
  node verify_independent.js)
(cd search/k6-neutral-descent-exact-20260725 &&
  shasum -a 256 -c SHA256SUMS)
(cd search/k6-defect-two-sum-20260725 &&
  shasum -a 256 -c SHA256SUMS &&
  python3 verify.py &&
  node verify_independent.js)
sh search/k6-defect-snark-plateau-20260725/verify_package.sh
sh search/minimum-switch-local-plateau-20260725/verify_package.sh
sh search/minimum-switch-neutral-components-n16-20260725/verify_package.sh
sh search/minimum-switch-neutral-components-n18-20260725/verify_package.sh
sh search/minimum-switch-neutral-components-n20-20260725/verify_package.sh
sh search/minimum-switch-packing-components-n22-20260725/verify_package.sh
sh search/minimum-size-three-packing-components-20260725/verify_package.sh
sh search/three-sum-neutral-decomposition-20260725/verify_package.sh
sh search/flow-weak-oddness-coordinate-20260725/verify_package.sh
```

The checkpoint
`scratch/checkpoints/h4-minimum-supports.snapshot.json` records the exact
row count and SHA-256 of the current incomplete \(H_4\) prefix.  Its
`status` and `warning` fields are part of the claim: the projected-support
master had not reached UNSAT, so the rows prove only that the listed
4,425,636 distinct minimum supports pack.

## Repository and generated-file state

At audit time the Git branch was `main` with an unborn `HEAD`: the repository
had no commits, every package path was untracked, and no revision SHA existed.
This is recorded explicitly rather than replaced by an invented provenance
identifier. The reference run metadata likewise records an unborn, dirty
tree.

The sibling `berge-fulkerson/` directory is unrelated workspace content and
is outside this five-cycle-double-cover package and its master verification.

The following are generated and intentionally ignored:

- `.tools/`: pinned external checker clones and binaries;
- `artifacts/`: structured portfolios and cross-verifier solver output;
- `**/.lake/`: Lean dependency/build state;
- `**/__pycache__/` and `*.py[cod]`: Python bytecode.

The platform-specific `verifier_b/verifier-b` executable is not ignored; its
hash is part of the external Verifier B freeze record. A different Go release
or target may produce a different executable even from identical source.

## 2026-07-28 direct reductions and local-frontier replay

```sh
shasum -a 256 -c scratch/direct-fivecdc-curated-SHA256SUMS-20260728.txt
python3 scratch/verify_petersen_four_pole_extension_theorem_20260728.py
python3 scratch/verify_jaeger_sorted_profile_local_no_go_order36.py
python3 scratch/search_jaeger_star_square_existential_census.py --order 10
python3 scratch/search_jaeger_star_square_existential_census.py --order 12
clang++ -O3 -std=c++20 \
  scratch/search_jaeger_star_square_existential_order14.cpp \
  -o /tmp/search_square_order14
geng -cq -d3 -D3 14 |
  /tmp/search_square_order14 |
  gzip -9 >/tmp/square-order14-witnesses.tsv.gz
python3 scratch/verify_jaeger_star_square_existential_order14.py \
  /tmp/square-order14-witnesses.tsv.gz
```

The Petersen checker must report 13 certificate rows, 100 ordered label
pairs, 550 boundary assignments, and all internal parities true.  The
sorted-profile checker must report 867 candidates, 63 legal exchanges, a
0/13/50 lower/equal/higher split, and a distance-two same-level escape.
The square censuses must report 6,300 and 53,352 instances with zero
failures and witness digests
`1ae75f2864163e8ec6b04c0d92f012f00375ab55f92cc1284ad8233d4c42ab8f`
and
`b6b5420643799ddfe9ab3f252b0447c7de7704b27ddd8e75eaed39613b567b4e`.
The order-14 checker must report 341 retained graphs, 4,774 roots, 572,880
witnesses, 24,268 distinct downstairs states, and corpus digest
`26dfe990a6655170f5fdcb6faf1424db279b57e8d094269417b7330fb5affd41`.

The direct portfolio contains no UNSAT result.  Its large redundant graph
and model streams are intentionally excluded from the compact publication
package; their hashes and exact run counts are frozen in
`scratch/direct-fivecdc-counterexample-branch-report-20260728.md`.
