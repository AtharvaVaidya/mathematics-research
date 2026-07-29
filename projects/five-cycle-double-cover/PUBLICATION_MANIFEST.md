# Publication manifest: marked circuits and rooted interfaces

Date: **2026-07-27**

Status: **AI-assisted research draft; the Five-Cycle Double Cover
Conjecture remains unresolved.**

This manifest records the material included through the
`codex/fivecdc-matching-frontier-20260727` branch, including the later
five-pole path-extension, order-15 threshold, and open-ear update.  It
extends the earlier `codex/five-cdc-marked-circuits-20260727` publication
branch.
OpenAI Codex agents, directed by Atharva Vaidya, generated or revised the
arguments, programs, computations, audits, and prose. Agent cross-checks
are not independent human verification or peer review.

## Minimum-class correction and MNP family update (2026-07-29)

- `scratch/minimum-projection-size5-theorem-20260729/` contains the full
  human proof for minimum sizes at most five.  The cumulative package
  `scratch/minimum-projection-through12-clean-or-delete-20260729/` and
  `scratch/minimum-projection-size12-independent-audit-20260729/` extend
  this through size twelve; the matching
  `scratch/minimum-projection-through13-clean-or-delete-20260729/` and
  `scratch/minimum-projection-size13-independent-audit-20260729/` packages
  extend it through size thirteen.  The new
  `scratch/minimum-projection-through14-cleanability-20260729/`,
  `scratch/minimum-projection-size14-7p7-independent-audit-20260729/`,
  and `scratch/minimum-projection-size14-kempe-escape-20260729/` packages
  extend the minimum-projection theorem through size fourteen.  The
  `scratch/minimum-projection-size15-exact-frontier-20260729/`,
  `scratch/minimum-projection-size15-induction-audit-20260729/`, and
  `scratch/minimum-projection-size15-anchor-single-audit-20260729/`
  packages extend it through size fifteen in connected bridgeless loopless
  cubic graphs.  The exact affine boundary classifiers enumerate
  every support shape forced by minimum exchange and directly clean all
  125,178 valid dirty canonical word/partition states using independent
  \(\operatorname{GL}(2,2)\) maps on complement components and repaired
  low values on the projection circuits.  The dependency-free replay and
  a separately written through-nine checker agree, and two agents
  independently reproduced the size-ten counts.  At size eleven it finds
  the first 14 direct-repair failures, all in the \(5+6\) shape, and
  constructs a size-five extendable replacement for every one.  A
  separately written valid-block checker reproduces all size-eleven
  counts and replacements.  At size twelve, two independent enumerators
  classify all 13,788,824 dirty states: 13,788,432 clean directly and 392
  admit a strict circuit deletion, with zero residuals.  At size thirteen,
  two independent implementations agree on all five support shapes and
  all 189,998,862 charge-valid states.  Of 159,369,966 dirty states,
  159,362,292 clean directly and 7,674 admit a strict circuit deletion,
  again with zero residuals.  At size fourteen the primary exact classifier
  enumerates 9,481 word orbits and 2,616,134,989 charge-valid states.
  Of 2,255,478,176 dirty states, 2,255,331,588 clean directly and
  146,364 admit strict circuit deletion, leaving 224 residuals, all in
  shape \(7+7\).  A separately written full \(7+7\) census reproduces
  all 333 word orbits, 91,481,505 charge-valid states, and exactly the
  same residual set.  A split-occurrence two-colour path lemma and 724
  literal matching-robust deletion rows send every residual to a
  size-seven extendable projection.  At size fifteen the primary
  classifier covers 26,492 canonical word orbits and 35,247,202,556
  charge-valid states.  Its 31,088,622,592 dirty states split into
  31,086,255,789 direct repairs, 2,360,767 strict circuit deletions, and
  6,036 residual \(7+8\) states.  An independently written induction
  checker canonically links every residual to the size-fourteen
  inverse-extension family; a separate realization-robust matching-game
  replay verifies all 6,036 rows directly.  Consequently any counterexample
  to the minimum-projection selection principle in this cubic setting has
  minimum size at least sixteen.
- `scratch/minimum-projection-single-circuit-tensor-frontier-20260729/`
  proves a human-checkable relative-\(\operatorname{GL}(2,2)\) tensor
  lemma by a three-point linear functional and leaf/cycle cancellation.
  It implies that every charge-valid one-circuit boundary state directly
  cleans, with no bound on circuit length, component count, or component
  degree.  Summing the tensors also treats several circuits when every
  component is charge-balanced separately on each circuit.  The latter
  hypothesis is stronger than ordinary conservation, so this does not
  settle the general multi-circuit case.  A separately written finite
  audit checks the cancellation expansion through seven tensor vertices,
  all 4,096 three-vertex tensor instances, and the boundary identities.
- `scratch/minimum-projection-two-occurrence-interaction-20260729/`
  identifies two-occurrence complement components with edges of an
  interaction multigraph on the support circuits.  Feasible map images
  are exactly its nowhere-zero \(\mathbb F_2^2\)-flows, and cleanliness
  means that the two occurrences traverse the same unoriented edge of
  \(K_4\).  The Petersen graph gives the smallest loopless abstract
  direct-cleaning failure in this subclass: all 60 interaction flows
  fail to clean, but every one strictly deletes a support circuit.  An
  explicit deletion reaches a globally minimum size-five clean
  projection.  The human ten-orbit table, primary and independent
  checkers, smaller-size census, hostile audit, and hash ledger pass.
  This is a proof-boundary result, not a FiveCDC counterexample.
- `scratch/two-occurrence-clean-delete-frontier-20260729/` extends that
  interaction analysis through total support sixteen when the
  interaction multigraph is loopless.  A human reduction leaves only
  the parallel-triangle multiplicity profiles
  \((3,2,2)\), \((3,3,2)\), and \((4,3,1)\).
  Two independently structured exact checkers classify all 22,032
  cyclic-order states as 21,816 clean and 216 delete-only, with zero
  residuals.  Hence every globally minimum projection in this subclass
  is cleanable.  Interaction loops and general occurrence multiplicities
  remain open at size sixteen.
- `scratch/minimum-projection-fixed-map-affine-cleaning-20260729/README.md`
  gives a complete human-checkable derivation of the one-bit cut defect,
  the affine XOR cleaning system for fixed component maps, the
  circuit-deletion alternative, and dual-cut coordinated feasible moves.
  It also records the sharp size-fourteen failure of the unrestricted
  map-choice implication.
- `scratch/clean-or-delete-quadratic-reduction-20260729.md` gives the
  companion algebraic proof of the quadratic parity collapse, translation
  linearization, exact dual obstruction, deletion certificate, and
  six-map witness-neutralization identity.
- `scratch/clean-or-delete-quadratic-reduction-audit-20260729/`
  independently audits the new six-map witness-neutralization theorem.
  The theorem proves that a common \(\operatorname{GL}(2,2)\) switch on
  the components selected by any one dual inconsistency witness preserves
  circuit integrability and can change that witness's obstruction bit
  from one to zero.  The checker recomputes the 16-entry quadratic table
  and verifies both three-map identities on 126,258 balanced circuit rows
  through length eight.  This is a single-witness theorem only; it does
  not prove simultaneous cleanliness or termination.
- `scratch/minimum-projection-dual-neutralization-dynamics-20260729/`
  gives the exact limit of iterating that theorem without extra data.
  On the size-fourteen counterstate its forty reduced map states form one
  strongly connected directed graph under legal witness neutralizations,
  with 320 switch certificates, 136 directed state pairs, and a displayed
  four-step cycle.  A human-checkable graph cycle has exchange gain
  \(6-2=4\) at one state for every relative translation; both checkers
  find a positive gain on all 160 state/translation pairs in the fixed
  18-vertex realization.  This proves only that global-minimum
  information must enter a termination argument.
- `scratch/minimum-projection-tjoin-dual-zero-price-20260729/` gives a
  human-checkable shortest-\(T_c\)-join duality proof that every shore
  which is a union of components of \(G-h\) has coefficient zero in
  every optimal dual.  Thus all positive dual shores split complement
  components, the rainbow neutralization witness is already zero-priced,
  and the aggregate four-dual optimum is always \(3|h|\).  The same
  load count proves
  \(|E-h|\ge |h|-|M_c|\) for every affine colour and
  \(|h|\le6|V|/7\) in cubic graphs.  Two separately structured finite
  checkers audit the six-map algebra and cut-parity identities; the
  universal theorem itself is the displayed LP proof and remains subject
  to expert human review.
- `scratch/minimum-projection-density-equality-rigidity-20260729/`
  decomposes the density slack exactly as
  \(4|E-h|-3|h|=\sum_c(A_c+U_c)\).
  Equality forces every positive dual shore to have one support and one
  complement edge, every complement edge to be saturated in all four
  duals, \(G-h\) to be a forest, \(|h|\) divisible by twelve, all
  complement and boundary derivative colours equinumerous, and every
  affine witness exactly colour-balanced.  An uncleanable equality-case
  minimum projection must have support at least 24.  The human proof, two
  arithmetic audits, hostile audit, outputs, and ledger pass; positive
  slack remains open.
- `scratch/minimum-projection-sixmap-color-load-frontier-20260729/`
  couples the legal six-map witness switch to dynamically recomputed
  global-minimum exchange.  If \(N_b\) and \(O_a\) are complement-edge
  colour loads inside and outside a six-map-integrable component union,
  then
  \(O_a+N_b\le |E-h|-|h|/2\) for every nonzero \(a,b\).
  Equivalently,
  \(k_a(\overline Y)+k_b(Y)\le2(|V|-|h|)\) in boundary-occurrence
  language.  Any violation explicitly constructs a legal recolouring
  and a strict colour-avoiding projection descent.  The full human proof,
  two independent finite audits, hostile logical audit, outputs, and
  hash ledger pass.  Rainbow parity is not yet proved to force a
  violation.
- `scratch/minimum-projection-rainbow-load-counterstate-20260729/`
  shows that local rainbow parity does not force that violation.  The
  cube graph has a support 6-circuit, two complementary 3-stars, a
  rainbow-odd six-map-integrable shore, all four support colours, and all
  nine load inequalities.  Lengths four and five are impossible in the
  corresponding minimally connected two-tree model.  The graph is
  Tait-colourable and four of its six switches clean the state, so the
  displayed projection is not globally minimum.  This is an audited
  proof-method counterstate, not a FiveCDC counterexample.
- `scratch/minimum-projection-rainbow-load-survivor-20260729/`
  strengthens that local counterstate to a fully goal-free
  support-fourteen boundary.  None of its component-map tuples cleans or
  deletes; it has a rainbow-odd six-map-integrable witness and satisfies
  every load inequality.  A 278-vertex simple bridgeless cubic inflation
  makes the fixed projection uncleanable and attains all four exact
  static shortest-join optima.  Exact contraction, weighted base
  enumeration, and an explicit lift prove that the graph's actual
  minimum projection size is seven.  Both implementations, two hostile
  audits, corrected replay instructions, outputs, and ledger pass.  This
  isolates dynamic global minimality; it is not a FiveCDC counterexample.
- `scratch/minimum-projection-size14-dichotomy-counterstate-20260729/`
  gives the first total-support counterstate to unrestricted clean or
  delete.  Its \(7+7\) word/partition has 320 normalized feasible map
  tuples and zero clean or deletion outcomes; a 40-case reduced table is
  an XOR-checkable certificate.  A simple connected bridgeless nonplanar
  cubic realization has canonical graph6
  `Qs???SC@GS@_CDOoC@@@?O?CO?g`.  Its displayed size-fourteen projection
  has 15,360 extensions and none clean, but its minimum projection size is
  five and all four minima are cleanable.  This refutes only the boundary
  lemma, not the minimum-projection conjecture or FiveCDC.
- `scratch/minimum-projection-size14-independent-audit-20260729/`
  independently exhausts all \(6^5\) map assignments and reconstructs the
  realization, \(K_{3,3}\) subdivision, 1,024-cycle space, 15,360 target
  extensions, and four cleanable minima without importing the primary
  checker or its output.
- `scratch/minimum-projection-size14-kempe-escape-20260729/` proves the
  split-occurrence path-switch lemma and freezes pairing-robust strategies
  for all 224 residual \(7+7\) states.  Its exhaustive builder and a
  separately structured literal checker verify 724 deletion rows that hit
  every possible four- or six-terminal path pairing.
- `scratch/minimum-projection-size14-7p7-independent-audit-20260729/`
  independently regenerates the complete \(7+7\) census by a valid-block
  exact-cover implementation and separately reconstructs the Kempe
  strategies.  Its sorted 224-row failure digest agrees with the primary
  census.
- `scratch/minimum-projection-known-strong-snarks-20260729/` freezes an
  exact SAT scan of seven retained order-34 and 7,654 retained order-40
  graph6 rows.  Every row has minimum projection size ten, and all 433,730
  minimum projections are cleanable.  The package includes literal inputs
  and outputs, two implementations, exact hashes, and replay scripts.  The
  linear implementation independently cross-checks all order-34 rows and
  the first five order-40 rows; completeness of the named graph populations
  is inherited from upstream provenance.
- `search/minimum-fano-class-nonpacking-130v-20260729/` proves
  \(\rho_3=5\) for the retained 130-vertex graph by an explicit
  nowhere-zero Fano flow and the existing doubly checked flow-resistance
  LRAT.  A second doubly checked LRAT proves that no size-five class
  packs.  This refutes the auxiliary claim that some globally minimum
  Fano value class must pack, while the retained size-six certificate
  and FiveCDC keep the graph positive for the original conjecture.
- `scratch/husek-samal-minimum-class-theory-20260729.md` has been
  corrected accordingly.  Its exchange inequalities remain valid, but
  the minimum-class route is now stated only as a possible
  reduced-domain experiment.
- `search/mnp-minimum-support-packing-20260729/` proves an infinite
  positive packing theorem for the explicit figure-derived reconstruction
  \(\widehat H_n\): the displayed size-\(n\) support packs two disjoint
  boundary joins for all \(n\ge2\).  Conditional on transcription identity
  with the Mattiolo--Negrini--Pagani family and their theorem
  \(r_f(H_n)=n\), it lifts to a globally minimum nonzero Fano value class.
  The graph identity and novelty assessment still require independent
  human review.
- `scratch/minimum-projection-census-through28-20260729/` exactly replays
  the minimum-extendable-projection test on 14,009 frozen cyclically-4
  non-Tait records through order 28 and 12,892 frozen order-22 hard
  records.  All 147,539 minimum projections are cleanable.  Completeness
  of the graph populations is inherited from the documented upstream
  canonical-generation packages.
- `scratch/petersen-minimum-tjoin-countermodel-20260729/` gives a
  dependency-free \(2^{15}\)-subset proof that a single matching can have
  two shortest containing cycles with neither complement terminal-even.
  This closes a tempting one-matching shortcut but does not realize the
  four synchronized affine classes.
- `preprint-minimum-fano-projection/` is the corresponding working
  preprint.  It contains the human exchange and size-through-fifteen
  proofs, the universal tensor argument, the six-map
  witness-neutralization proof, the sharp size-fourteen
  support-preserving method counterstate, the Kempe escapes, all exact
  census reports, the Petersen limitation, checksums, and an explicit
  AI-use and human-review disclosure.
- `scratch/cubic-reduction-standard-fivecdc-20260729/` fixes the exact
  indexed even-subgraph convention and proves that the universal standard
  assertion is equivalent across finite bridgeless multigraphs, loopless
  cubic multigraphs, simple cubic graphs, and strong snarks.  It includes
  loops by incidence multiplicity, separates the orientable conclusion,
  and freezes an exhaustive local \(D_5\)-label checker.  A hostile second
  audit checked the structural reductions by hand.  No novelty is claimed
  for these standard graph-class reductions.
- `scratch/general-kempe-descent-static-exchange-obstruction-20260729/`
  proves a general coloured \(K_4-e\) inflation theorem.  It preserves the
  support, complement-component partition, and all two-colour boundary
  pairings while making all four static minimum-exchange inequalities
  hold.  Its explicit 230-vertex simple bridgeless cubic state defeats all
  97 nonempty one-round fixed-colour path multiswitches but reaches a
  strict deletion after two recomputed switches.  The graph is
  Tait-colourable and has minimum projection zero, so this is a
  proof-method obstruction, not a FiveCDC or minimum-projection
  counterexample.  A full-cycle checker, a separate shortest-\(T\)-join
  checker, a complete boundary-profile reconfiguration census, exact
  hashes, a human proof, and a hostile agent audit are included.
- `scratch/minimum-projection-dynamic-kempe-frontier-20260729/` proves two
  dynamic-frontier statements.  First, if the support is one circuit and
  every complement component has exactly two vertices on it, every
  extension is directly cleanable by componentwise
  \(\operatorname{GL}(2,2)\) maps and support reintegration.  This is an
  unbounded human theorem.  Second, chains of the edge-deleted
  \(K_{3,3}\) two-pole reflect boundary-changing Kempe moves and transfer
  any hypothetical goal-free base orbit to one satisfying all four
  recomputed exchange inequalities at every reachable state.  The latter
  theorem is conditional: no base orbit or globally minimum
  counterexample is supplied.  The package includes two independently
  written dependency-free checkers, exact hashes, exploratory results
  clearly separated from the theorems, and a hostile agent audit.
- `search/minimum-projection-n130-20260729/` certifies that the retained
  130-vertex graph has minimum extendable projection size \(42\), exactly
  11,264 minimum supports, and no unclean minimum.  One LRAT proves the
  size-\(\le41\) formula UNSAT; a second blocks all listed size-42
  supports and proves enumeration completeness.  Both are accepted by C
  `lrat-check` and verified CakeML `cake_lpr`.  The same graph has
  \(\rho_3=5\), so the package explicitly separates minimum projection
  from minimum nonzero value class.

These are proof-strategy results in the cubic setting, not a proof or
disproof of FiveCDC.  The standard universal conjecture reduces to that
setting, but the size-through-fifteen projection theorem remains a cubic
statement and larger supports are open.

## Rooted-resolution update (2026-07-28)

- `ROOTED_RESOLUTION_FRONTIER_20260728.md` states the exact current
  theorem and remaining premise.
- `scratch/d5-terminal-root-universality-suffices.md` and its hostile
  audit write out the fixed-five reductions, including degree-two
  suppression and 2-/3-cut pasting.
- `scratch/d5-independent-root-feasibility-desargues-frontier.md` proves
  the two-way edge-adapted insertion equivalence and the strengthened
  3-edge-connected, root-specific 8/9-cycle geometry.
- `scratch/d5-root-good-matching-fourflow-characterization.md` gives the
  exact rooted matching, nowhere-zero 4-flow, and connected
  two-\(T\)-join equivalence.
- `output/d5-root-feasibility-lift13-girth10/all-eliminations.json`
  retains root-good labels for all 195 edge eliminations of the
  130-vertex girth-ten control; the separately written verifier
  reconstructs and checks every witness.
- `scratch/oum-combined-choice-equivalence-and-toggle.md`,
  `scratch/jaeger-tree-choice-through14-and-exchange-no-go.md`, and their
  reports/checkers delimit the eight-to-five and spanning-tree routes.
- `scratch/d5-root-port-monodromy-local-charge.md` and
  `scratch/d5-connected-shared-coordinate-incidence-and-shortest-no-go.md`
  record the exact monodromy divisor, connected incidence theorem, and
  sharp scope failures.
- `preprint-d5-surface-kempe/` contains the updated 16-page working
  preprint, source, checksum ledger, review guide, and cautious
  publication assessment.

This update is a conditional reduction and finite-evidence package.  It
does not prove or disprove FiveCDC, and it makes no orientable claim.

## H--S reconfiguration and binary-repair update (2026-07-28)

- `scratch/husek-samal-fixed-pair-packing-switch-equivalence-20260728.md`
  proves a two-way, fixed-\((\lambda,a)\) theorem: legal binary
  \(a\)-switches are in bijection with the \(T_a\)-joins in
  \(G-M_a\), and one reaches the Hušek--Šámal component condition exactly
  when \(M_a\) packs two edge-disjoint \(T_a\)-joins.  The proof allows
  parallel edges and does not assume connectedness or bridgelessness.
- `scratch/husek-samal-perfect-kernel-transition-csp-20260728.md`
  treats the special case in which the selected binary kernel is a
  perfect matching.  Contracting that matching gives a 4-regular
  transition multigraph; clean fixed-projection lifts are exactly its
  six-state vertex assignments followed by a consistent affine XOR
  system.  Petersen shows that this special CSP is not universally
  feasible.
- `scratch/husek-samal-shortest-projection-obstruction-12v-20260728.md`
  gives a self-contained 12-vertex counterexample to choosing a shortest
  binary cycle first and then extending it to a nowhere-zero
  \(\mathbb F_2^3\)-flow.  The graph is a Petersen triangle expansion;
  its unique shortest cycle cannot be a flow coordinate, although the
  graph has a FiveCDC.  The accompanying projection--resistance lemma
  proves the obstruction without SAT.
- `preprint-husek-samal-reconfiguration/` is an eight-page working
  preprint with a page-one AI-use disclosure and human-review gate.  Its
  strengthened strict order-26 theorem shows that an H--S-bad flow can
  already have a packable value class yet have no good simple-cycle
  neighbour.  A solver-free checker exhausts 9,213 cycles and 1,485 legal
  switches, checks the two joins, exact distance two, graph premises, and
  an explicit FiveCDC.
- `scratch/fano-binary-packing-repair-frontier-20260728.md` proves the
  exact 21-incidence symmetry and SAT/XOR formulation for binary repair.
- `search/fano-binary-repair-connected-countermodel-108v-20260728/`
  freezes a connected simple bridgeless cubic order-108 countermodel to
  binary repair under connectedness alone.  The 51,193-clause formula is
  UNSAT, with LRAT accepted by both `lrat-check` and verified CakeML
  `cake_lpr`; an independently structured checker reconstructs the graph,
  flow, formula, and a positive FiveCDC.
- The order-108 graph has exactly two cyclic 2-edge cuts.  Therefore it
  is not a FiveCDC counterexample and does not refute the surviving
  cyclically-4, girth-ten binary-repair lemma.
- `search/fano-binary-repair-cyclic4-countermodel-144v-20260728/`
  freezes the next exact boundary: a simple cubic, cyclically-4,
  non-Tait order-144 graph and flow on which all seven starting packing
  tests and all 21 normalized binary-cycle repairs are UNSAT.  Twenty-nine
  individual LRATs are accepted by both `lrat-check` and verified CakeML
  `cake_lpr`, and a clean-room checker reconstructs every clause.
- The order-144 graph has girth five and an explicit checked standard
  FiveCDC.  It refutes only the cyclically-4-only repair statement; the
  girth-at-least-ten BPR lemma and FiveCDC remain open.
- `verify_order80_girth10_binary_repair.py` supplies a solver-free
  positive girth-ten control on a Tait-colourable order-80 graph.

These are auxiliary publishable-candidate results, not a resolution.
Novelty remains provisional pending specialist review.

## KMNS girth-construction audit (2026-07-28)

- `search/kmns-girth-claim-obstruction-20260728/` records a local
  obstruction in the literal Figure 4 construction of Karabáš,
  Máčajová, Nedela, and Škoviera (2022).
- The ordinary proof exhibits connector-terminal paths of lengths
  \(4,3,3\).  Across the \((3,3,1)\)-pole \(Z\), every one of the 18
  structural connector identifications (36 ordered junctions before
  quotienting by the symmetry of the two isolated edges) therefore closes
  a cycle of length at most nine.
- A standard-library checker reconstructs the corrected Figure 2
  Petersen graph, exhausts all 20 admissible decycling triples and all
  60 distinguished-terminal choices, and checks all 18 structural
  identifications.  It reports bounds eight or nine, with largest certified
  per-identification upper bound nine.
- A separately prompted Codex agent blind-audited the paper transcription,
  multipole convention, proof, and checker and found the narrow claim sound.
  This is an AI cross-check, not independent human review.

This is a candidate gap report awaiting human confirmation of the authors'
multipole convention and intent.  It concerns only the displayed
construction: it does not refute their broader existence theorem, does not
exclude a repaired superposition, and has no implication for FiveCDC.

## Jaeger fixed-fibre and five-point lifting update (2026-07-28)

- `preprint-jaeger-fivecdc-frontier/` is a 34-page working preprint with
  an explicit unresolved-status box, detailed AI-use disclosure,
  reproducibility table, human-review gate, and rendered PDF.
- `scratch/jaeger-support5-component-criterion.md` proves the exact
  component-parity criterion for restricting Oum-compatible pairs to five
  affine points.
- `scratch/jaeger-k-forest-star-parity-identities.md` proves that the
  fundamental completion of a cubic spanning tree is the complement of
  its unique all-vertices-odd forest, and translates five support to an
  Eulerian intersection after component contraction.
- Hušek--Šámal, arXiv:2607.24724v1, Theorem 3.16 is now cited as the
  independent source of the flow-level component criterion; the draft
  explicitly withdraws priority for that characterization.
- `scratch/jaeger-star-exact-parity-triangle-invariance.md` gives a
  two-way human reduction for nonroot triangle expansion, with all 60
  admissible traces reduced to seven checked symmetry orbits.
- `scratch/jaeger-tree-choice-through14-and-exchange-no-go.md` proves
  prescribed Type A/B multiplicity feasibility by the
  Nash--Williams--Tutte partition inequality.
- `output/jaeger-five-point-fibres-through14/` and its independent verifier
  cover 587 simple bridgeless cubic graphs, 944,974 placements, and all
  804,204 feasible fibres, with zero support-five failures.
- `output/jaeger-coordinate-five-order44/` retains literal witnesses for
  31 graphs and all 1,364 roots.  Its separate standard-library verifier
  reconstructs graph premises, trees, completions, flow values, supported
  pairs, and point parity.
- `output/jaeger-star-thinning-countermodel-34v/` retains a complete CNF
  and dual-accepted LRAT for failure of every thinning direction, plus a
  positive five-point witness in the same fibre.
- The Petersen, fixed-third-tree, perfect-forest-extension, and
  fixed-coordinate monotone-descent notes are countermodels to stronger
  intermediate lemmas only.
- `output/jaeger-fano-min-descent-through14/` and
  `scratch/jaeger-fano-minimum-parity-descent-through14.md` give the exact
  all-seven symmetric descent theorem through order 14: 419 graphs, 3,567
  root-orbit fibres, and 529,150,122 states with no trapped positive-level
  component.  The independent verifier audits graph and root coverage,
  totals, ordering, and hashes; it does not duplicate the whole-state
  enumeration.
- `scratch/jaeger-fano-reciprocal-exchange-law.md` gives the exact
  simultaneous update of all seven Fano-plane component defects.
  `scratch/jaeger-fano-min-immediate-descent-countermodel.md` and its
  standalone checker show that immediate descent and fixed-kernel
  exposure both fail, while explicitly exhibiting two-step escapes.
- `scratch/jaeger-simultaneous-triangle-lift-plateau-search.md` proves that
  simultaneous nonroot triangle expansions give one Cartesian
  \(\operatorname{Cay}(S_3,\mathcal T)\) factor per triangle. The
  accompanying exact lift search finds no strict trap in two adversarial
  order-16 controls; broader plateau data are labeled exploratory.
- `scratch/jaeger-star-square-any-coordinate-lift-no-go.md` gives the
  minimum-order fixed-state square-lift failure. The order-six controls and
  complete 672-instance order-eight census preserve the weaker whole-fibre
  implication.  The new fixed-cover square-extension lemma proves that the
  two deleted pair labels extend exactly when they are equal or disjoint.
  Complete solver-free whole-fibre censuses at orders ten and twelve check
  6,300 and 53,352 labelled instances with zero failures.  The order-14
  and order-16 certificate censuses add 572,880 and 7,737,408 explicit
  witnesses, each reconstructed by separately written standard-library
  checkers.  The order-16 layer covers all 2,828 canonical simple
  three-edge-connected graphs and 45,248 labelled roots.  Thus any
  countermodel to the local-selection statement in this class has order at
  least 18.  A complete 41,301-record regeneration additionally identifies
  exactly three order-18 snarks and replays all 12,474 of their positive
  instances.
- `scratch/jaeger-sorted-profile-local-no-go-order36.md` and its
  independent checker refute one-step lexicographic descent of the complete
  sorted seven-defect profile.  The exact 63-neighbour split is
  0 lower, 13 equal, and 50 higher; a checked two-exchange same-level path
  reaches defect zero, so the full plateau-component statement remains
  open.
- `scratch/jaeger-square-fixed-label-selection-cut-no-go.md` proves by
  three-edge-cut parity that the relevant triangular-prism edge labels
  always intersect once in every FiveCDC.  Its independent checker
  enumerates all 540 indexed labellings and also reconstructs exact-good
  downstairs and square-local lifted tree states.  Thus only the
  fixed-label selection bridge is refuted.
- `scratch/jaeger-plateau-radius-three-no-go-order40.md` and its independent
  checker reconstruct a complete 958-state same-level ball with layers
  \(1,13,108,836\), test 1,037,514 candidate swaps, and prove exact plateau
  escape distance four.  The state escapes; the full unbounded component
  theorem remains open.
- `scratch/jaeger-plateau-profile-laplacian-no-go.md` gives two adjacent
  equal-profile states whose total-defect Laplacians have opposite signs,
  \(+10\) and \(-14\).  Its exhaustive checker verifies both complete
  neighbourhoods.  This refutes profile-only averaging and universal
  sub/superharmonicity of total defect, not topology-sensitive descent.
- `output/jaeger-fano-min-descent-triangle-expansions-16v/` retains the
  exact thirteen-fibre control: 17,297,280 states, maximum
  \(d_{\min}=4\), and no trapped positive same-level component.  Its
  coverage verifier is standard-library only and does not duplicate the
  C++ whole-state enumeration.
- `scratch/jaeger-parity-element-and-kernel-closure-no-go.md` identifies
  odd kernels as fundamental circuits after adjoining one all-ones column
  and rewrites star packings as three cographic bases plus terminal joins.
  `output/jaeger-kernel-closure-frontier/` freezes the positive tests
  through order 14 and a generic Type-A 12-vertex no-go.
- `output/jaeger-star-kernel-closure-countermodel-16v/` contains a
  certificate-producing CNF and LRAT, accepted by both `lrat-check` and
  verified CakeML `cake_lpr`, that refutes kernel closure in a vertex-star
  fibre.  A solver-free enumeration checks all 5,723,136 packings: zero
  are closure-good, while 40,464 meet the exact component-parity target.
  The human triangle-contraction theorem extends the closure failure to an
  infinite rooted family of simple cubic 3-edge-connected graphs.
- `formal/FiveCDC/`, `verifier_a/`, and `verifier_b/` retain the
  fixed-graph semantic formalization and two independently implemented
  target checkers.
- `scratch/fano-apx-countermodel-order36.md` and its independent verifier
  refute the affine pair-exchange axiom on a 36-vertex cyclically
  4-edge-connected snark. The same graph has a checked standard five-cover,
  and the same flow has thousands of one-switch repairs, so APX alone is
  closed negatively while FiveCDC and the reduced one-switch lemma remain
  open.

The exact universal obligation is still to select a parity-good packing in
every required vertex-star fibre.  Universal descent for the symmetric
seven-plane potential would suffice and remains open.  Kernel closure is
now disproved even for a vertex-star fibre; every retained countermodel
nevertheless has an exact five-point witness.  The standard FiveCDC
conjecture therefore remains unresolved, and the orientable conjecture is
not addressed.

## Direct covering and Petersen-substitution update (2026-07-28)

- `scratch/fivecdc-cover-pullback-reduction-20260728.md` gives a
  human-checkable proof that every finite graph cover of a FiveCDC-positive
  graph is FiveCDC-positive.  Its incidence convention explicitly handles
  loops and parallel edges.
- `scratch/fivecdc-petersen-four-pole-extension-theorem-20260728.md`
  proves that replacing two independent edges of a positive cubic graph by
  the Petersen four-pole obtained by deleting adjacent vertices preserves
  FiveCDC for every port bijection.  Its 13-row pair-label table covers the
  three \(S_5\) orbit types.
- `scratch/verify_petersen_four_pole_extension_theorem_20260728.py`
  independently checks all 100 ordered pair-label choices, 550 labelled
  boundary placements, 120 coordinate permutations, and every internal
  parity.
- `scratch/direct-fivecdc-counterexample-branch-report-20260728.md` records
  the exact solver semantics and 45,924 checked SAT instances at orders
  40, 48, 56, 64, 80, and 160.
- `scratch/direct-fivecdc-curated-SHA256SUMS-20260728.txt` freezes the
  compact 16-entry publication package.  The large graph/model streams are
  intentionally excluded; their hashes remain in the report.

This update provides two sound positive reductions and finite encoder
controls.  It contains no UNSAT target, no counterexample, and no claimed
resolution.

## Minimum cube/Heawood full-boundary and local-barrier update (2026-07-28)

- `preprint-fivecdc-four-pole-reductions/` is a nine-page standalone
  working preprint with a prominent unresolved-status box, detailed AI-use
  disclosure, complete Petersen, cube, and Heawood certificate tables,
  deterministic rendered PDF, checksum ledger, and human-review gate.
- `scratch/fivecdc-minimum-full-boundary-cube-four-pole-20260728.md`
  proves that deleting adjacent cube vertices gives a six-vertex
  full-boundary pole.  A ten-row human certificate and separately written
  checker cover all 640 admissible words.  The degree identity
  \(2m=3n-4\), together with the exact \(K_{2,2}\) obstruction, proves
  that six is the minimum possible order in the connected simple
  terminal-distinct cubic class.
- `scratch/fivecdc-heawood-full-four-pole-theorem-20260728.md` proves that
  the four-pole obtained by deleting adjacent vertices of the Heawood graph
  extends every xor-zero ordered boundary word over the ten pair labels.
  Its ten orbit rows cover all 640 words under \(S_5\).
- `scratch/verify_heawood_four_pole_full_boundary_20260728.py` independently
  checks the graph metadata, all internal vertex parities, the ten orbit
  sizes, all 120 coordinate permutations, and exact 640-word coverage.
- Arbitrary-port insertion of this pole into two independent edges
  preserves both standard FiveCDC and bridgelessness.  This is a
  non-covering, non-Petersen positive reduction, but the pole is not known
  to be unavoidable in a minimal counterexample.
- `scratch/verify_k33_four_pole_boundary_20260728.py` exhausts the
  \(K_{2,2}\) pole left by adjacent deletion in \(K_{3,3}\).  It verifies
  640 admissible xor-zero words, exactly 580 extensions, and one exact
  60-word missing \(S_5\)-orbit represented by `02 02 03 03`; the preprint
  also gives a direct human nonextension proof.
- `LOCAL_FRONTIER_SHA256SUMS_20260728` now also freezes the cube and Heawood
  theorems, triangular-prism fixed-label no-go, order-40 radius-three
  plateau separator and profile-Laplacian no-go, and the nested order-16
  and order-18-snark certificate manifests.
- `scratch/fano-six-bad-threecut-lock-20260728.md` corrects the
  order-18 six-bad-flow core: edge ids 14, 18, and 26 form a cyclic
  three-cut.  Its standard-library checker enumerates every 1024-element
  deleted-edge pole cycle space and verifies the exact local profile split
  `12 x 456`, `12 x 137`, `3 x empty`.  Every obstructive pole retains a
  cyclic shore behind a three-boundary, excluding that core from
  cyclically-4 all-seven local-obstruction compositions.
- `scratch/fano-cyclic4-allseven-order60-20260728.md` gives the complete
  order-60 construction and the human local-to-global reduction.  Two
  relabelled four-poles have completion-sound bad profiles `567` and
  `12345`, so the displayed fixed flow has no clean functional projection.
- `scratch/verify_fano_cyclic4_allseven_order60.cpp` is the
  solver-independent replay: it exhausts 131,072 first pole cycles per
  local projection, solves the remaining equations by binary elimination,
  checks all 121,575 edge sets of sizes one through three, and verifies a
  literal standard FiveCDC.  The graph is cyclically 4-edge-connected but
  is not a FiveCDC counterexample.
- `scratch/search_fano_order32_near_pole_profiles.py` and the optional
  `--sample` mode of `scratch/fano_all_bad_projection_search_linear.cpp`
  preserve the CaDiCaL-assisted discovery provenance; neither is in the
  theorem's trust base.

These are exact human-checkable or independently replayable advances.  They
do not prove or disprove FiveCDC, and no target UNSAT certificate exists in
this update.

## Five-pole path-extension and ear frontier

- `docs/five-pole-realizability-frontier.md` gives the human-checkable
  bridge and path-extension lemmas and states the corrected logical scope:
  universal boundary nonemptiness in the stated class would already imply
  standard FiveCDC.
- `search/five-pole-46-threshold-order15-20260727/` contains all 69,243
  order-15 canonical records, eight threshold transcripts, the primary
  CaDiCaL classifier, checksums, report, and an independent
  structure/corpus verifier with optional full replay.
- `search/five-pole-universal-split-order17-20260727/` contains the eight
  exact summaries and corpus identities for 1,109,844 order-17 cores and
  11,098,440 positive terminal-pair checks, plus primary source and an
  independent structure/corpus verifier.
- `scratch/vertex-edge-universal-split-state-frontier.md` gives
  line-by-line proofs of the boundary/closed-graph equivalence and the
  prescribed matching, exact \(\mathbb F_2^2\)-flow, and avoiding
  two-\(T\)-join equivalence.  The rooted theorem is open.
- `scratch/audit_vertex_edge_split_state_equivalence.py` independently
  checks the complete local algebra and the retained summary totals.
- `scratch/d5-five-pole-ear-operator-frontier.md` and its two audit
  programs give the exact ear operator, restricted finite semigroups, and
  an independently replayed abstract countermodel to coarse induction.
  The countermodel is not claimed to be graph-realizable.
- `FIVE_POLE_FRONTIER_SHA256SUMS` freezes the focused proof/audit sources
  and the nested order-15 package manifest.
- `VERTEX_EDGE_SPLIT_SHA256SUMS` freezes the rooted proof/audit sources and
  nested order-17 package manifest.

This update does not prove or disprove FiveCDC and does not address the
orientable variant.  The still-running order-40 rooted strong-snark job is
not part of this publication snapshot.

## One-boundary-five update

`ONE_BOUNDARY_FIVE_FRONTIER_20260727.md` indexes the new focused update.
It contains:

- `docs/one-boundary-five-oddness-frontier.md`, with displayed proofs of
  the exact boundary matching count, the two-attainable-terminal lemma,
  and the conditional oddness-four reduction;
- `docs/one-boundary-five-completion-frontier.md`, including the
  human-checkable cyclic-three-cut proof excluding \(s=0\);
- seven standard-library replay programs for the explicit small poles,
  the locally cyclically-four 67-vertex core, and its \(s=1\) and \(s=2\)
  completions;
- the order-17 C++ census source and retained aggregate;
- retained JSON outputs for the explicit countermodels, sharp-threshold
  core, all-five-bad core, 720-case \(s=0\) audit, 120 \(s=1\)
  bijections, and 9,600 \(s=2\) gluings; and
- `search/one-boundary-five-oddness6-completion-20260727/`, a complete
  compact order-100 specimen with exact one-boundary-five profile and
  exact oddness six, together with a two-checker resistance LRAT, an
  explicit 2-factor, a positive standard five-CDC model, an independently
  checked compact edge labelling, and full cut replay;
- `docs/theta-cap-five-cycle-extension-lemma.md`, with a displayed
  \(58/62\) ordered theta-cap computation, bichromatic switching-attractor
  proof, and the corrected global-minimality argument excluding the
  terminal-distinct \(s=1\) outside;
- `docs/reductions.md`, recording the elementary reduction to the simple
  cyclically 4-edge-connected minimum bridgeless cubic domain;
- primary and separately written standard-library parity-CSP programs,
  with byte-reproducible retained JSON reports;
- `docs/one-boundary-five-D5-s123-reduction.md`, with the
  greatest-switching-core implication, two smaller-cap arguments, and the
  exact elimination of every retained \(s=1,2,3\) outside pattern;
- a shared exact incidence generator, primary finite-domain relation
  solver, independently implemented local-row relation solver, both
  retained reports, and their nested checksum package;
- `S123_D5_REDUCTION_SHA256SUMS`;
- `THETA_CAP_SWITCHING_SHA256SUMS` and
  `ONE_BOUNDARY_FIVE_SHA256SUMS`.

The locally cyclically-four all-five-bad pole refutes a proposed local
matching lemma, not FiveCDC.  Its displayed globally admissible
completions have exact oddness four and are not counterexamples.  The
order-100 specimen proves that oddness at most four is not universal in
this branch, but it too has a checked standard five-CDC.  The theta-cap
lemma closes the terminal-distinct \(s=1\) incidence branch, and the
switching-core/compatible-pair argument closes the repeated-endpoint
\(s=1\) shapes and every retained \(s=2,3\) outside.  Together with the
\(s=0\) triangle-cut argument, only \(s\ge4\) remains in this branch.
The index records the AI-use disclosure and exact machine trust
boundaries.  This update concerns only the standard conjecture.

## Prescribed-root matching frontier

`MATCHING_FRONTIER_20260727.md` indexes the added matching branch:

- `docs/prescribed-root-matching-deficiency-frontier.md`
- `docs/focused-theta-choice-census-frontier.md`
- `docs/boundary-eight-rotation-closure-frontier.md`
- `docs/singleton-ge-tait-frontier.md`
- `docs/root-insertion-two-factor-frontier.md`
- `scratch/prescribed-root-matching-deficiency-checker.py`
- `scratch/rotation-closure-countermodel-checker.py`
- `scratch/focused-local-insertion-census.cpp`
- `scratch/verify-root-insertion-census.py`
- `scratch/check-root-insertion-published.py`
- `scratch/focused-local-insertion-result.ndjson`
- `scratch/root-insertion-independent-through22.json`
- `scratch/root-insertion-independent-through26.json`
- `scratch/root-insertion-independent-order28-combined.json`
- `scratch/root-insertion-independent-order28-shard0.json` through
  `scratch/root-insertion-independent-order28-shard3.json`
- `scratch/focused-theta-choice-census.cpp`
- `scratch/verify-focused-theta-choice-census.py`
- `scratch/focused-theta-choice-census-result.json`
- `search/focused-theta-choice-through28-20260727/`
- `search/focused-theta-choice-order30-20260727/`

The universal deficiency-two theorem, boundary-eight incidence theorem,
and disconnected singleton-case Tait theorem have complete displayed
proofs.  The new oddness argument closes the whole all-singleton branch
for the standard five-cycle-double-cover conclusion.  The stronger
prescribed-root connected singleton case remains open.  The focused and
root-insertion censuses through order 28, and the separate focused-theta
order-30 census, are exact over their recorded corpora but are not
promoted to universal statements.

## Preprint

The complete `preprint-rooted-four-cut/` directory is included:

- `main.tex`
- `references.bib`
- `output/pdf/main.pdf` (29 pages)
- `README.md`
- `AUDIT.md`
- `NOVELTY-ASSESSMENT.md`
- `CHECKSUMS.sha256`
- `CHECKSUMS-PUBLISHED.sha256`

The abstract, front-matter disclosure, introduction, README, and novelty
assessment all state that the paper neither proves nor disproves five-CDC.

## Human-checkable proof and reduction notes

- `docs/five-cdc-elliptic-quadratic-flow-model.md`
- `docs/four-mark-core-closure.md`
- `docs/root-edge-reduction-four-cut-gate.md`
- `docs/rooted-cycle-translation-obstruction.md`
- `docs/exceptional-cyclic-three-root-signature-factorization.md`
- `docs/rooted-base-pair-cycle-cut-certificate.md`
- `docs/rooted-four-mark-unmarked-toggle.md`
- `docs/rooted-four-mark-bridgeless-reduction.md`
- `docs/rooted-four-mark-odd-k23-reduction.md`
- `docs/rooted-four-mark-ozeki-linkage-gate.md`
- `docs/rooted-four-mark-p4-row-star-reduction.md`
- `docs/rooted-four-mark-singleton-endpoint-closure.md`
- `docs/order22-universal-four-separation-screen.md`
- `docs/exceptional-four-cut-surviving-split-atoms.md`
- `docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`
- `docs/rooted-three-pole-base-pair-closure-target.md`
- `docs/rooted-three-pole-tait-cap-closure.md`
- `docs/rooted-cap-triangle-induction.md`
- `docs/rooted-cap-end-factor-fork-lift.md`
- `docs/five-cdc-five-point-triangle-list-lift.md`

The current research state and open obligations are recorded in:

- `docs/current-status.md`
- `docs/proof-obligation-ledger.md`
- `docs/experiment-ledger.md`
- `docs/publication-assessment-20260726.md`

## Compact checker and result files

- `scratch/tait_all_coloring_mark_separation.cpp`
- `scratch/verify_order22_separation_via_matchings.cpp`
- `scratch/order22-universal-four-separation-result.json`
- `scratch/rooted_cycle_translation_blockers.py`
- `scratch/verify_rooted_cycle_translation_blockers.mjs`
- `scratch/rooted-cycle-translation-blockers-result.json`
- `scratch/rooted_three_pole_signature_factorization.py`
- `scratch/verify_rooted_three_pole_signature_factorization.mjs`
- `scratch/rooted-three-pole-signature-factorization-result.json`
- `scratch/rooted-four-mark-order20-screen-result.json`
- `scratch/verify_rooted_cap_triangle_table.py`
- `scratch/rooted-cap-triangle-table-v2.json`
- `scratch/verify_rooted_end_factor_fork_lift.py`
- `scratch/rooted-end-factor-fork-lift-replay.json`
- `scratch/verify_five_point_triangle_list_lift.py`
- `scratch/five-point-triangle-list-lift-result.json`
- `scratch/verify_five_point_triangle_list_lift.mjs`
- `scratch/five-point-triangle-list-lift-independent.json`
- `scratch/boundary_two_orbit_witness_cadical.cpp`
- `scratch/verify_boundary_two_orbit_witness.py`
- `scratch/verify_boundary_two_orbit_witness_fast.cpp`

## Reproducibility packages

The branch includes all non-cache files in:

- `search/rooted-three-pole-frontier-20260727/` — 90 files, 354,336
  bytes; complete compact order-17 base-pair records and replay scripts.
- `search/four-pole-order22-cap-20260727/` — 84 files, 23,728,989
  bytes; completed cyclically-four order-22 cap-slice records, compressed
  transcripts, corpus identities, and verifier sources.
- `search/four-pole-order24-cyclic4-cap-20260727/` — 44 files,
  1,067,314 bytes; complete retained cyclically-four order-24
  classification and its corrected scope documentation.
- `search/four-pole-order26-cyclic4-cap-20260727/` — 44 files,
  14,019,526 bytes; complete retained cyclically-four order-26
  classification.  Its 1,297 cap records and 859,911 deletion-pole rows
  remain valid; the package alone implies no global exceptional-pole
  lower bound.
- `search/four-pole-order26-strict-cap-probe-20260727/` — 28 files,
  2,341,537 bytes; a finite retained strict-snark source probe, explicitly
  distinct from the complete cyclically-four order-26 classification.
- `search/mnp-h2-h5-aa-deletion-probe-20260727/` — 12 files, 129,104
  bytes; explicit \(H_2,\ldots,H_5\) prescribed-\(AA\) certificates and a
  solver-independent checker.
- `search/rooted-three-pole-nontait-endpoint-frontier-20260727/` — 44
  files, 9,037,638 bytes; complete retained endpoint-factor classification
  through order 26, two byte-identical solver transcripts, a
  solver-independent replay, the sound pure-relation cap bound 54, and,
  through the separate endpoint-fork lift, the scoped mixed-branch bound.
- `search/four-pole-order28-cyclic4-cap-20260727/` — 36 files, 851,281
  bytes in Git; complete 12,517-graph source, theorem, reproduction notes,
  logs, statuses, hashes, compact reports, and checker.  The full local
  package has two independently replayed positive labellings for each of
  9,725,709 poles and proves the scoped order-30 bound.
- `search/focused-theta-choice-through28-20260727/` — compact complete
  retained source corpus, generator logs, two classifier sources, frozen
  result streams, and aggregate verifier for 14,009 graphs and 10,689,351
  independent root pairs.
- `search/focused-theta-choice-order30-20260727/` — 42 files, 1,719,245
  bytes; complete retained 139,854-graph House of Graphs corpus, primary
  C++20 result, sixteen clean-room Python shard reports and logs, compact
  verifier, reproduction instructions, and checksum ledger for
  125,868,600 independent root pairs.
- `search/rooted-three-pole-c3-cap-frontier-through24-20260727/` —
  compact publication subset of the complete 10,824,084-root
  triangle-free cap screen: source corpora, expanded cores, logs,
  statuses, hashes, summaries, report, verifier, and regeneration notes.

Excluded deliberately: `__pycache__`, `.DS_Store`, private attachments,
temporary `/private/tmp` output, compiled checker binaries, unrelated dirty
files, broad 294 MB graph streams, multi-gigabyte proof files, and
placeholder material. The two byte-identical 34,355,648-byte C3-cap
transcripts are omitted with compressed and uncompressed hashes and exact
regeneration instructions retained. The order-28 witness stream
(363,463,166 compressed bytes) and generated pole stream (40,210,290
compressed bytes) are also omitted; their compressed and uncompressed
hashes and regeneration commands are retained.

## Validation performed before publication

- Every entry in the full laboratory
  `preprint-rooted-four-cut/CHECKSUMS.sha256` passed; every present Git
  artifact passes `CHECKSUMS-PUBLISHED.sha256`.
- The preprint PDF metadata reports 29 pages.  Extracted first-page text
  contains the no-resolution statement, and page two contains the explicit
  AI-use disclosure.
- A clean Tectonic 0.16.9 rebuild produced the committed 29-page PDF with
  SHA-256
  `8d0da87f5e07abf1dc5cc25e05f16faeb442a7dead8754f7b8bb4b88596f9b95`.
  All 29 pages were rendered and visually inspected.
- JSON syntax checks passed for the order-22 separation result, order-17
  base-pair report, and cyclically-four order-22 report.
- Both independently structured order-22 separation checkers compiled and
  agreed on the complete order-12 control:
  85 rows, 80 Tait-colourable graphs, 307 normalized colourings, zero
  target-four witnesses; the matching replay counted 902 perfect matchings.
- The rooted order-17 transcript verifier reconstructed 654,676 canonical
  cores, 15,645,623 nonbridge roots, and zero base-pair violations.
- `verify_report.py` accepted the frozen rooted-frontier report.
- The compact package checksum ledgers passed.  The corrected order-24 and
  order-26 cyclically-four `verify.py` programs were both replayed and
  reproduced their committed JSON reports byte for byte.  The order-26
  replay reconstructed all 1,297 source graphs and 859,911 deletion poles.
  The \(H_2,\ldots,H_5\) verifier had already reproduced its committed
  report independently.
- The corrected rooted base-pair note and Tait-cap closure proof were
  checked for local references, explicit scope, the mixed-relation
  counterexample, and AI-use disclosure.  The audit withdraws the former
  one-sided proof of the order-26 and order-28 lower-bound conclusions
  while preserving the exact finite cyclically-four cap classifications;
  the later endpoint-fork proof independently restores the stated scoped
  order-28 bound.
- The endpoint package passed `SHA256SUMS`, `SOURCES.sha256`, and a fresh
  independent semantic replay over 1,360,452 roots in 38,244 cores; it
  reproduced `report.json` byte for byte.
- The fork-triple checker reproduced
  `scratch/rooted-cap-triangle-table-v2.json` byte for byte. The complete
  two-implementation triangle-free screen now classifies 10,824,084 roots
  with no empty signature or base-pair violation. The compact Git subset's
  present-artifact checksums and source manifest pass; the full row replay
  requires the two hash-frozen omitted transcripts.
- The endpoint-fork checker reproduced
  `scratch/rooted-end-factor-fork-lift-replay.json` byte for byte,
  enumerating all 60 ordered connector triangles, 30 forks, and 900 ordered
  fork pairs.  The human lift bypasses that screen and restores the
  stated bridge-free simple terminal-distinct fixed-five lower bound 28.
- The full order-28 package passed both semantic replays over 9,725,709
  rows and 19,451,418 displayed labellings.  Its two positive boundary
  orbits exclude all six exceptional masks and raise the same scoped lower
  bound to 30.  The independently written C++ replay was rerun before this
  publication and reproduced its compact JSON byte for byte.
- The Python and JavaScript five-point checkers independently agree on all
  392 five-set/line cases.
- The two small prescribed-root countermodel checkers pass using only the
  Python standard library. The focused-theta package checksum ledger and
  aggregate verifier pass; the retained result classifies 14,009 graphs
  and 10,689,351 root pairs with zero all-dumbbell cases through order 28.
- The order-30 focused-theta package passed its complete checksum ledger
  and compact verifier. The audit directly checked the retained corpus
  hashes, 139,854 unique order-30 simple-cubic records, all sixteen
  clean-room shard reports, and exact agreement with the C++ totals:
  125,868,600 independent root pairs, 1,221,804 deficiency-two theta
  choices, and zero all-dumbbell cases.
- The order-100 oddness-six package passed its nested and focused checksum
  ledgers, quick structural replay, and full cyclic-cut replay.  The pinned
  `lrat-check` and CakeML `cake_lpr` checkers both accepted the retained
  source-resistance LRAT.  Verifier A accepted the retained standard
  five-CDC SAT model, while the package replay independently accepted the
  compact edge labelling.  The existing resistance renderer regenerated
  the retained CNF byte for byte.  The certificate checkers establish
  UNSAT of that CNF; the renderer is not a second independently written
  semantic encoder.

No fresh full order-22 census is claimed by this publication preparation.
The frozen reports state their exact scope and provenance.
