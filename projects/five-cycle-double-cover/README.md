# Five-cycle double cover research archive

Status as of **2026-07-27**: the standard five-cycle double cover
conjecture remains open.  Nothing in this directory is a proof or a
counterexample to that conjecture.

This is a curated, reproducible publication bundle from an autonomous
conjecture-resolution laboratory.  It contains four research drafts, a
computer-free marked-graph theorem, explicit human-checkable
countermodels to two intermediate proof strategies, exact SAT/XOR
documentation, and compact checker sources.  Temporary search output and
multi-gigabyte certificates are deliberately not committed.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, generated and revised
arguments, programs, audits, computations, and manuscript text in this
research archive.  Agent-to-agent checks are not independent human
verification or peer review.  The papers display their mathematical
arguments for line-by-line human checking, separate computational claims
from human proofs, and require independent specialist review before
submission.

## Five-pole path-extension and ear frontier

The newest five-pole branch is deliberately scoped as a reformulation and
bounded evidence, not a resolution:

- [`docs/five-pole-realizability-frontier.md`](docs/five-pole-realizability-frontier.md)
  gives a line-by-line path-extension proof that universal nonemptiness of
  the stated internally bridgeless five-pole boundary relation is already
  equivalent, after the standard reductions, to FiveCDC.  Consequently the
  proposed universal 46-of-62 orbit lower bound would be stronger than the
  original conjecture; it is not a known auxiliary lemma.
- [`search/five-pole-46-threshold-order15-20260727/`](search/five-pole-46-threshold-order15-20260727/)
  is an exact threshold census of all 69,243 connected simple internally
  bridgeless terminal-distinct cubic five-pole cores of order 15.  Every
  record reaches 46 satisfiable boundary orbits.  The package includes the
  primary classifier, all eight transcripts, hashes, a fresh canonical
  corpus/structure replay, and an optional byte-identical full replay.
  Positive models were not retained, so the classifier and CaDiCaL remain
  in the trust base.
- [`search/five-pole-universal-split-order17-20260727/`](search/five-pole-universal-split-order17-20260727/)
  exhausts all 1,109,844 corresponding order-17 cores.  For every core,
  all ten choices of a doubled terminal pair admit the boundary state
  `01,01,23,24,34`, for 11,098,440 positive SAT checks.  The independent
  verifier regenerates and structurally checks every canonical shard.
  [`scratch/vertex-edge-universal-split-state-frontier.md`](scratch/vertex-edge-universal-split-state-frontier.md)
  proves that this state is equivalent to a prescribed vertex/edge 5-CDC,
  and then to a rooted exact-zero matching, four-flow, and two-\(T\)-join
  certificate.  The arbitrary-order rooted theorem remains open.
- [`scratch/d5-five-pole-ear-operator-frontier.md`](scratch/d5-five-pole-ear-operator-frontier.md)
  proves the exact open-ear operator and records two checked restricted
  infinite ear families.  It also gives an abstract, explicitly
  non-graph-realizability countermodel showing why coarse support and
  switching invariants cannot prove the universal 46-orbit statement.
  The primary and independent standard-library audits are retained beside
  the note.

None of these artifacts proves or disproves FiveCDC, and none concerns the
orientable variant.  The order-40 rooted strong-snark computation was still
running when this snapshot was frozen and is not included.

## One-boundary-five Gallai--Edmonds frontier

[`ONE_BOUNDARY_FIVE_FRONTIER_20260727.md`](ONE_BOUNDARY_FIVE_FRONTIER_20260727.md)
indexes the newest surviving standard-FiveCDC branch.  The companion
human notes prove the exact matching count, the two-attainable-terminal
lemma, a conditional oddness-four reduction, and the solver-free exclusion
of the \(s=0\) completion.  Explicit checked poles show that three tempting
local matching strengthenings are false, including an all-five-bad
locally cyclically-four 67-vertex core.

That core nevertheless has explicit cyclically-four \(s=1\) and \(s=2\)
completions of exact oddness four.  They are not FiveCDC counterexamples.
A newer order-100 completion in
[`search/one-boundary-five-oddness6-completion-20260727/`](search/one-boundary-five-oddness6-completion-20260727/)
has the exact same one-boundary-five profile and exact oddness six.  This
rules out closing the entire branch by an oddness-at-most-four theorem.
The specimen has an explicit standard five-cycle double cover, so it is
not a counterexample.  The surviving proof obligation must use how the two
complementary paths close through the outside shore.  The update includes
standard-library replays, checked proof certificates, retained witnesses,
checksum ledgers, exact trust boundaries, and a separate AI-use
disclosure.  It neither resolves standard FiveCDC nor addresses the
orientable variant.

The human-checkable
[`docs/theta-cap-five-cycle-extension-lemma.md`](docs/theta-cap-five-cycle-extension-lemma.md)
now excludes the terminal-distinct \(s=1\) outside from a minimum-order
bridgeless cubic counterexample.  Its ordered seven-vertex theta cap
accepts 58 of the 62 \(D_5\) boundary orbits; every one of the four
missing orbits can be switched along either bichromatic path into the cap
relation.  Primary and separately written standard-library programs
reproduce the complete 6,240-word calculation.  The repeated-endpoint
\(s=1\) incidence shapes and all \(s\ge2\) outside patterns remain open.
The encoding and switching method are prior machinery; only this specific
cap calculation and scoped consequence are offered as provisionally new.

## Main research drafts

- [`preprint-rooted-four-cut/output/pdf/main.pdf`](preprint-rooted-four-cut/output/pdf/main.pdf)
  is a 29-page structural and computer-assisted research report on marked
  circuits and fixed-five rooted interfaces.  It includes human-checkable
  proofs of the exact elliptic-flow reformulation, a four-mark closure
  theorem, a forbidden-root cut gate, the corrected Tait-cap closure, and
  the root-end fork lift; it separately labels every finite census used
  in the scoped exceptional-pole lower bound.  Its
  source, audit, novelty assessment, and checksum ledger are in
  [`preprint-rooted-four-cut/`](preprint-rooted-four-cut/).  The paper
  explicitly says that it neither proves nor disproves five-CDC.
- [`output/pdf/four-universally-separated-marks-preprint-20260726.pdf`](output/pdf/four-universally-separated-marks-preprint-20260726.pdf)
  proves a marked cubic-graph theorem.  Under universal Tait separation
  and a precise cyclic-cut inequality, four marked edges lie in one
  four-mark cycle or two disjoint two-mark cycles.  The argument is
  computer-free.  Its source is
  [`preprint-four-mark-core/main.tex`](preprint-four-mark-core/main.tex),
  and a standalone proof is in
  [`docs/four-mark-core-closure.md`](docs/four-mark-core-closure.md).
- [`output/pdf/two-connected-countermodels-five-cdc-preprint.pdf`](output/pdf/two-connected-countermodels-five-cdc-preprint.pdf)
  gives explicit 40- and 46-vertex countermodels to two proposed
  one-circuit repair strategies.  Both graphs positively have standard
  five-cycle double covers, so they are not counterexamples to five-CDC.
  Its source is
  [`preprint-fano-one-switch/main.tex`](preprint-fano-one-switch/main.tex).
- [`preprint-fano-combined-span/main.pdf`](preprint-fano-combined-span/main.pdf)
  proves a universal combined-image identity and exact quadratic normal
  form for fixed-projection Fano-flow cleaning, then gives a
  human-checkable Petersen obstruction to one prescribed-line
  strengthening.  The Petersen graph positively has a five-cycle double
  cover, so this is not a counterexample to five-CDC.  Source and the
  cautious novelty audit are in
  [`preprint-fano-combined-span/`](preprint-fano-combined-span/).

All four PDFs prominently disclose substantive AI involvement and
explicitly state their scope.  Their novelty assessments are provisional
pending independent expert literature review.

## Current compact four-pole frontier

Five compact finite packages sharpen the fixed-five four-pole boundary
without claiming a universal theorem:

- [`search/four-pole-order24-cyclic4-cap-20260727/`](search/four-pole-order24-cyclic4-cap-20260727/)
  gives a complete two-implementation classification of the retained
  155-graph cyclically 4-edge-connected non-Tait order-24 source.  All
  86,490 independent-edge deletion poles have full fixed-five boundary
  signature.
- [`search/four-pole-order26-cyclic4-cap-20260727/`](search/four-pole-order26-cyclic4-cap-20260727/)
  gives the corresponding complete retained cyclically-four order-26
  classification: 1,297 source graphs and 859,911 independent-edge
  deletion poles, all with full fixed-five boundary signature.
- [`search/four-pole-order26-strict-cap-probe-20260727/`](search/four-pole-order26-strict-cap-probe-20260727/)
  checks all 185,640 deletion poles from a retained 280-graph strict-snark
  source.  Every row again has full signature.  This earlier finite probe
  is retained as an independently frozen strict-source control.
- [`search/four-pole-order28-cyclic4-cap-20260727/`](search/four-pole-order28-cyclic4-cap-20260727/)
  records the complete retained 12,517-graph order-28 source and compact
  reports for 9,725,709 deletion poles.  Two positive boundary witnesses
  per pole exclude all six exceptional masks.  The ordinary Git archive
  omits the 363 MB witness stream and its 40 MB generated pole stream but
  preserves their hashes, generation commands, checker sources, logs, and
  independently reproduced summary.
- [`search/mnp-h2-h5-aa-deletion-probe-20260727/`](search/mnp-h2-h5-aa-deletion-probe-20260727/)
  supplies 394 explicit edge-labelling certificates covering all 97,608
  independent edge pairs in the reconstructed \(H_2,\ldots,H_5\) family.
  Each certificate directly proves the prescribed \(AA\) boundary state.

Each package has a solver-independent verifier, frozen checksums, precise
source limitations, and an AI-use disclosure.  None resolves five-CDC.
The finite cap classifications remain valid.  A hostile audit withdrew an
earlier reduction from all small exceptional poles because it used a false
one-sided base-pair inference.  The later two-sided endpoint-fork lift
below supplies a different sound reduction and restores only the stated
bridge-free simple terminal-distinct fixed-five lower bound of order 28.

The corrected human proof
[`docs/rooted-three-pole-tait-cap-closure.md`](docs/rooted-three-pole-tait-cap-closure.md)
shows that a Tait-colourable one-vertex shore cap forces a base pair in its
root signature.  One such shore excludes only the equality-only and
disjointness-only relations; two such shores exclude all three exceptional
relations.

The frozen
[`search/rooted-three-pole-nontait-endpoint-frontier-20260727/`](search/rooted-three-pole-nontait-endpoint-frontier-20260727/)
package extends endpoint base-pair closure through factor order 26 using
two independent classifiers and a solver-independent replay.  It gives cap
order at least 54 for equality-only or disjointness-only cyclic-three
relations.  The package alone does not eliminate the mixed relation.

The human-checkable
[`docs/rooted-cap-triangle-induction.md`](docs/rooted-cap-triangle-induction.md)
reduces that mixed branch through cap order 26 to a triangle-free
3-connected shore screen through order 24. The screen is now frozen in
[`search/rooted-three-pole-c3-cap-frontier-through24-20260727/`](search/rooted-three-pole-c3-cap-frontier-through24-20260727/):
two exact implementations classify all 10,824,084 proper roots, with no
empty signature or base-pair violation. This is a bounded result, not a
universal rooted-closure theorem.

The independent human argument in
[`docs/rooted-cap-end-factor-fork-lift.md`](docs/rooted-cap-end-factor-fork-lift.md)
bypasses that screen for the stronger finite lower bound.  A base pair in
each root-end factor transports through its three-sum path as a fork
triple; any two forks force both an unequal-intersection and a disjoint
cross-pair.  With the completed endpoint and cyclically-four cap
classifications through order 26, this first restores the scoped simple
terminal-distinct exceptional-pole lower bound of order 28.  The complete
order-28 two-witness classification then raises that scoped bound to 30.
This is not a universal exceptional-pole theorem, and Five-CDC remains
unresolved.

The exact five-point restriction theorem in
[`docs/five-cdc-five-point-triangle-list-lift.md`](docs/five-cdc-five-point-triangle-list-lift.md)
classifies all local ways to compress the eight-coordinate triangle lift
to five coordinate points.  Independent Python and JavaScript checkers
agree on all 392 five-set/line cases.  The remaining global flow-and-line
selection problem is still open.

## Fixed-line Fano branch

The standard five-cycle double cover conjecture remains unresolved.  The
new fixed-line package has plausible, moderate, and specific novelty, but
every theorem and priority claim still requires independent human
verification:

- [`docs/fano-combined-line-span.md`](docs/fano-combined-line-span.md)
  contains the universal linear identity and exact nonlinear normal form;
  [`docs/fano-triangle-expansion-invariance.md`](docs/fano-triangle-expansion-invariance.md)
  proves that triangle expansion cannot create the first all-seven
  fixed-projection obstruction.
- [`search/fano-two-cycle-petersen-countermodel-20260726/`](search/fano-two-cycle-petersen-countermodel-20260726/)
  freezes the Petersen proof, semantic checker, CNFs, and verified DRAT
  certificates for two failed prescribed lines.
- [`search/fano-some-good-line-census-20260726/`](search/fano-some-good-line-census-20260726/)
  is an exact negative census through every connected simple bridgeless
  cubic graph of order \(18\), plus retained strict snarks at orders
  \(20,22,24\) and ten targeted cyclically-5-connected order-\(26\)
  snarks.  It finds no all-seven obstruction in that stated scope.
- [`docs/aligned-nice-borrower-frontier.md`](docs/aligned-nice-borrower-frontier.md)
  records that the aligned rooted branch remains open at one
  \(b_3\)-tight equality atom.

## Latest structural branch

The connected eight-mark branch remains open.  The newest notes expose
its exact remaining constraints without claiming a five-CDC resolution:

- [`docs/kempe-transversality-and-eight-mark-girth.md`](docs/kempe-transversality-and-eight-mark-girth.md)
  proves human-checkable Kempe and marked-girth lemmas.  Its
  \(|V|\ge88\) corollary is scoped to the extremal exact-zero size-four
  branch: arbitrary matchings need not produce distinct suppressed marks
  forming matchings.
- [`docs/audit-eight-mark-girth-bound.md`](docs/audit-eight-mark-girth-bound.md)
  independently reconstructs that corollary, verifies the numerical
  bound, and records the necessary suppression hypotheses.
- [`docs/eight-mark-bichromatic-code.md`](docs/eight-mark-bichromatic-code.md)
  reduces the fixed-colouring problem to an exact signed-graph component
  test.
- [`docs/connected-eight-mark-paired-cut-condition.md`](docs/connected-eight-mark-paired-cut-condition.md)
  derives the paired cyclic-cut condition that retains the four matching
  pairs lost by the simpler unpaired inequality.
- [`docs/cyclic-four-separated-triple-atom-reduction.md`](docs/cyclic-four-separated-triple-atom-reduction.md)
  explicitly marks the proposed cyclic-four atom lemma as refuted while
  retaining its sound conditional reductions.
- [`docs/eulerian-factor-quotient-tjoin-reduction.md`](docs/eulerian-factor-quotient-tjoin-reduction.md),
  [`docs/two-tjoin-cycle-lift-obstruction.md`](docs/two-tjoin-cycle-lift-obstruction.md),
  and [`docs/size-four-terminal-gap-cut-reduction.md`](docs/size-four-terminal-gap-cut-reduction.md)
  prove the exact local lifting criterion, refute automatic quotient
  lifting, and reduce unavoidable terminal-gap failure to explicit cyclic
  four- and six-cut interfaces.
- [`docs/cyclic-four-cut-zero-pair-signature.md`](docs/cyclic-four-cut-zero-pair-signature.md)
  and [`docs/cyclic-six-cut-four-mark-interface.md`](docs/cyclic-six-cut-four-mark-interface.md)
  audit those two cut frontiers.  Both notes identify precise remaining
  obligations; neither eliminates its cut branch.
- [`docs/equality-complementary-quotient-no-go.md`](docs/equality-complementary-quotient-no-go.md)
  proves that the canonical complementary quotient-join construction
  cannot lift in the sharp order-\(88\) equality case.

Two new finite equality diagnostics sharply delimit the selector route:

- [`docs/equality88-incidence-rotation-countermodel.md`](docs/equality88-incidence-rotation-countermodel.md)
  gives an explicit decorated \(8+8\), 5-regular incidence object whose
  reconstructed simple cubic 80-vertex core has zero good bichromatic
  selectors.  It fails girth and universal separation and positively has
  unrestricted two-\(T\)-join packing, so it is a countermodel only to the
  incidence-only proof strategy.
- [`docs/order80-vertex-transitive-control.md`](docs/order80-vertex-transitive-control.md)
  eliminates the 33 order-80 cubic vertex-transitive census graphs from the
  surviving equality scope.  Its follow-up
  [`docs/order80-c10-selector-transversal-scan.md`](docs/order80-c10-selector-transversal-scan.md)
  checks all 74,940 factor-transversal records in the sole girth-ten graph:
  every record has between 94 and 138 good selectors.  Vertex-transitivity
  is not a minimum-counterexample reduction.

The finite diagnostics are now complemented by a solver-free
low-surplus theorem.  The equality proof in
[`docs/equality88-kempe-girth-contradiction.md`](docs/equality88-kempe-girth-contradiction.md)
and its blind audit
[`docs/equality88-overlap-audit.md`](docs/equality88-overlap-audit.md)
use ambient girth and a literal Kempe splice to exclude order \(88\).
The general argument in
[`docs/order94-kempe-surplus-bound.md`](docs/order94-kempe-surplus-bound.md),
independently reconstructed and generalized in
[`docs/audit-and-generalization-order94-kempe.md`](docs/audit-and-generalization-order94-kempe.md),
also excludes orders \(90,92,94\).  Its exact scoped conclusion is:
\[
  |V(G)|\ge96
\]
in the connected eight-mark extremal exact-zero size-four
minimum-counterexample branch.  It is not a bound for arbitrary cubic
graphs and does not resolve five-CDC.

The transparent checker
[`scratch/verify_order96_kempe_incidence_frontier.py`](scratch/verify_order96_kempe_incidence_frontier.py)
verifies an explicit abstract order-\(96\) incidence matrix against all
proved pairwise, single-switch, and nonempty simultaneous-switch
inequalities.  The matrix passes with minimum slack one.  It is a
method-frontier certificate, not a graph realization or a conjecture
counterexample.

The next ambient order, \(100\), now has a certified but still scoped
exclusion in
[`docs/order100-unmarked-exclusion-and-row-star-frontier.md`](docs/order100-unmarked-exclusion-and-row-star-frontier.md).
A short human-checkable Kempe-incidence proof excludes unmarked
bichromatic factor circuits.  In the all-marked case, a solver-free
enumeration reduces all \(1002\) simultaneous profile orbits first to
\(155\), then an exact weighted-kernel row-and-column-star census reduces
them to three abstract profile orbits.  An independently written Z3
replay agrees on the three survivors.  The complete star-compatible
incidence space contains \(827\) matrix orbits.

A profile-level gluing formula then ranges over every labelled matrix,
cyclic position assignment, common-edge bijection, and endpoint
orientation in each of those three profiles; it does not select one
representative matrix.  All three profile formulas are UNSAT already in
\(G-M\).  Their committed CNFs have independently verified LRAT hashes,
and a separate producer-free semantic checker reconstructs the complete
base formulas and verifies all \(996{,}904\) dynamically learned clauses
from forced short circuits.  The exact scoped consequence is
\[
  |V(G)|\ge102
\]
in the connected eight-mark extremal exact-zero size-four branch.  This
does **not** cover other matching sizes or exchange branches and is not a
resolution of five-CDC.

Two adjacent reductions are also current but remain open:

- [`docs/fano-canonical-join-cut-certificates.md`](docs/fano-canonical-join-cut-certificates.md)
  converts failure of the seven canonical Fano packing tests into exact
  binary cut certificates and a checkerboard obstruction.  These are
  human-checkable necessary conditions; the required uncrossing step is
  open.
- [`scratch/rooted-p4-structured-endpoint-screen-result.json`](scratch/rooted-p4-structured-endpoint-screen-result.json)
  records an exact negative screen on 240 structured order-38 rows:
  101,760 endpoint-path tests and no rooted \(P_4\) failure.  This is
  finite evidence on one labelled construction family, not a universal
  rooted theorem and not five-CDC.

The cyclic six-cut branch has also been reduced more sharply:

- [`docs/rooted-four-mark-cap-avoidance.md`](docs/rooted-four-mark-cap-avoidance.md)
  proves that the all-mark trace can always avoid the cap edge, and gives
  an exact order-28 countermodel showing that universal separation alone
  does not force componentwise marked parity.
- [`docs/rooted-four-mark-bridgeless-reduction.md`](docs/rooted-four-mark-bridgeless-reduction.md)
  proves that the marked-cut hypothesis eliminates the countermodel's
  odd-shore bridge mechanism.  Any surviving deleted-root graph is
  2-connected and its complementary mark-pair circuit families form a
  genuine cross-intersecting four-way linkage obstruction.

The rooted theorem remains open.  The attached finite rooted screens are
diagnostics within their stated scopes, not substitutes for a universal
proof.

The adjacent cyclic four-cut branch now has an exact rooted-packing
interpretation.  The human-checkable note
[`docs/four-pole-exception-rooted-packing-algebra.md`](docs/four-pole-exception-rooted-packing-algebra.md)
identifies projection-coherent lifts with ordered pairs of edge-disjoint
terminal joins, excludes a zero-free exceptional shore, and proves an
exact two-plus-two minimal-factor reduction.  Its independent JavaScript
checker reconstructs all 640 boundary words, ten symmetry orbits, 259
admissible masks, and the exceptional factorizations.  This finite
algebra neither proves graph realizability of an exceptional signature
nor resolves Máčajová--Mazzuoccolo--Tabarelli Conjecture 3.7, which
remains open.

The compact package
[`search/cyclic4-universally-separated-triple-n24-20260726/`](search/cyclic4-universally-separated-triple-n24-20260726/)
freezes the refuting order-24 graph, all 144 retained hits, exact search
scope, canonical records, hashes, and independently structured single-
and batch-verifiers.  It establishes that a universally separated triple
can occur in a cyclically four-edge-connected Tait-colourable cubic graph.
All 144 construction hits have marked-subdivision girth five, however,
so none satisfies the surviving connected-branch threshold of ten.

## Human-checkable material

- [`MATCHING_FRONTIER_20260727.md`](MATCHING_FRONTIER_20260727.md)
  indexes the prescribed-root matching branch. It separates the universal
  deficiency theorem, boundary-eight and singleton Gallai--Edmonds
  reductions, exact finite censuses through order 30, checked
  countermodels to weaker lemmas, and the prescribed-root case that
  remains open.
- [`search/focused-theta-choice-order30-20260727/`](search/focused-theta-choice-order30-20260727/)
  classifies all 125,868,600 independent root pairs in the cited
  139,854-graph order-30 House of Graphs corpus. A primary C++20
  implementation and a separately written Python replay in sixteen
  shards agree: all 1,221,804 deficiency-two pairs admit a theta choice,
  and no all-dumbbell pair occurs. This is a verified finite structural
  result, not a universal theorem or a Five-CDC resolution.
- [`docs/root-insertion-two-factor-frontier.md`](docs/root-insertion-two-factor-frontier.md)
  gives a line-by-line proof that the all-singleton Gallai--Edmonds
  branch already has a **standard** five-cycle double cover: an
  edge-prescribed perfect matching leaves a 2-factor with at most two
  odd circuits.  It also proves the exact root-insertion interlacing
  criterion and records a two-implementation finite screen through order
  28.  This closes one standard branch, not the prescribed-root
  alternative or Five-CDC itself.
- [`docs/four-mark-core-closure.md`](docs/four-mark-core-closure.md) gives
  the full computer-free four-mark proof.
- [`docs/audit-eight-mark-girth-bound.md`](docs/audit-eight-mark-girth-bound.md)
  gives a clean-room, computer-free proof and scope audit of the
  conditional order-\(88\) corollary.
- [`search/connected-one-switch-countermodel-40v-20260726/HUMAN-PROOF.md`](search/connected-one-switch-countermodel-40v-20260726/HUMAN-PROOF.md)
  proves the planar 40-vertex intermediate countermodel.
- [`search/fano-pure-merge-one-switch-countermodel-46v-20260726/HUMAN-PROOF.md`](search/fano-pure-merge-one-switch-countermodel-46v-20260726/HUMAN-PROOF.md)
  proves the nonplanar 46-vertex pure-merge countermodel.
- [`docs/encoding.md`](docs/encoding.md) proves the equivalence between
  five Eulerian edge-subsets and the exact SAT/XOR edge-label formula,
  including graph-convention cautions.
- [`docs/order100-unmarked-exclusion-and-row-star-frontier.md`](docs/order100-unmarked-exclusion-and-row-star-frontier.md)
  gives the complete human proof excluding unmarked factors at order
  \(100\), proves completeness of the profile-level finite encoding, and
  clearly separates the scoped order-\(100\) exclusion from five-CDC.
- [`docs/publication-assessment-20260726.md`](docs/publication-assessment-20260726.md)
  separates apparently new statements from known ingredients.
- [`docs/current-status.md`](docs/current-status.md) and
  [`docs/proof-obligation-ledger.md`](docs/proof-obligation-ledger.md)
  record the broader search status and remaining proof obligations.

## Quick independent checks

The compact countermodel checkers use only the Python standard library:

```sh
python3 search/fano-value-class-flow-countermodel-20260726/independent_checker.py
python3 search/connected-one-switch-countermodel-40v-20260726/independent_checker.py
python3 search/connected-one-switch-countermodel-40v-20260726/verify_package.py
python3 search/fano-pure-merge-one-switch-countermodel-46v-20260726/independent_checker.py
python3 -m tools.test_encode_five_cdc_xor_fast
python3 search/h4-all-minimum-support-packing-20260726/verify_upper_witness.py
python3 -B search/cyclic4-universally-separated-triple-n24-20260726/verify_package.py
python3 -B scratch/verify_equality88_rotation_countermodel.py
python3 -B scratch/audit_equality88_rotation_countermodel.py
python3 -B scratch/audit_order80_c10_selector_scan.py
python3 -B scratch/verify_order96_kempe_incidence_frontier.py
python3 -B scratch/prescribed-root-matching-deficiency-checker.py
python3 -B scratch/rotation-closure-countermodel-checker.py
(cd search/focused-theta-choice-through28-20260727 && python3 verify.py)
(cd search/focused-theta-choice-order30-20260727 && \
  python3 verify.py && shasum -a 256 -c SHA256SUMS)
shasum -a 256 -c ROOT_INSERTION_SHA256SUMS
python3 -B scratch/check-root-insertion-published.py
(cd search/rooted-three-pole-c3-cap-frontier-through24-20260727 && \
  shasum -a 256 -c CHECKSUMS-PUBLISHED.sha256)
python3 -B scratch/check_order100_row_star_patterns.py
python3 -B scratch/enumerate_order100_incidence_relaxation.py
python3 -B scratch/enumerate_order100_exact_row_star_relaxation.py \
  --baseline-json scratch/order100-incidence-relaxation-survivors.json
python3 -B scratch/enumerate_order100_row_star_matrix_orbits.py
for profile in 0 1 2; do
  python3 -B scratch/check_order100_global_profile_cnf.py \
    --profile "$profile" \
    --cnf "scratch/order100-global-profile${profile}-final.cnf"
done
python3 -B scratch/audit_fano_canonical_cut_certificates.py
python3 -B scratch/verify_rooted_four_mark_countermodel.py
python3 -B scratch/four_pole_two_plus_two_algebra.py
node scratch/verify_four_pole_two_plus_two_algebra.mjs
```

The 40-vertex checker optionally uses nauty's `labelg` to recheck the
canonical graph6 encoding.  Its semantic checks still run when nauty is
absent.

The complete laboratory replay is documented in
[`REPRODUCING.md`](REPRODUCING.md).  Some commands there refer to the full
local laboratory rather than this curated Git bundle.  See
[`ARTIFACTS.md`](ARTIFACTS.md) for the exact included and omitted scope.

## Standard versus orientable five-CDC

This archive's primary target is the standard conjecture: at most five
Eulerian edge-subsets cover every edge exactly twice.  Empty Eulerian
subgraphs may pad a cover with fewer than five coordinates.  The
orientable version is stronger and is not silently substituted for the
standard formulation.

## AI-use disclosure

OpenAI Codex agents, operating under Atharva Vaidya's direction, made
substantive contributions throughout this project: proposing and
refuting intermediate claims, finding proof architectures and finite
constructions, writing programs and checkers, conducting literature
searches, drafting manuscripts, and performing additional agent audits.
Those agent audits are not independent human verification or peer review.

No mathematical claim should be accepted because an AI system generated
or checked it.  A human graph theorist should independently verify every
proof and attribution, rerun the checkers, conduct a specialist novelty
search, and assume normal scholarly responsibility before any formal
submission.
