# Five-cycle double cover laboratory report

Audit date: **2026-07-28**.

## 1. Outcome

**Classification: PARTIAL STRUCTURAL PROGRESS / VERIFIED FINITE CASES /
CONTROL VALIDATION.**

This project does **not** resolve the five-cycle double cover conjecture.
It found neither:

- a finite bridgeless graph whose target five-coordinate formula is
  independently certified UNSAT; nor
- a proof that every finite bridgeless graph has the required cover.

This is the only status consistent with the acceptance gates.  Sang-il
Oum's July 2026 exposition proves an eight-coordinate cycle double cover and
still states the five-coordinate strengthening separately as Conjecture 18:
<https://arxiv.org/abs/2607.16356>.  The 2023 SIAM paper likewise describes
5-CDC as the stronger conjecture and proves it for cubic graphs of oddness at
most four: <https://epubs.siam.org/doi/10.1137/22M1472425>.
Hušek and Šámal's arXiv:2607.24724v1, submitted July 27, 2026, likewise
states FiveCDC as open. Their Theorem 3.16 independently proves the exact
five-support component-parity characterization used in the Jaeger branch,
and their Conjecture 3.19 isolates the equivalent missing flow-selection
step. This project therefore claims no novelty or priority for that
criterion.

The strongest new outputs of this project are:

- an exact quotient-lift characterization of the remaining obstruction;
- a human proof that the exact Jaeger star component-parity target is
  invariant under contracting or lifting any triangle away from the root,
  reduced to seven local trace rows and backed by an exhaustive 60-trace
  checker;
- a human-checkable endpoint-fork reduction and a complete
  9,725,709-pole order-28 explicit-witness census, together proving a
  scoped order-30 lower bound for simple terminal-distinct fixed-five
  exceptional poles;
- a second, whole-shore triangle-induction route through cap order 26,
  backed by two identical 10,824,084-root exhaustive transcripts;
- a universal prescribed-root matching-deficiency bound of two, plus an
  exact 136,557,951-pair focused census through order 30 in which every
  deficiency-two instance has a theta complement;
- a fully audited standard five-CDC theorem for every bridgeless cubic
  multigraph whose components have at most 22 vertices;
- a constructive connected-kernel sufficient condition, verified on all
  44,327 connected simple bridgeless cubic isomorphism classes through
  order 18;
- a 34-vertex certified separator, and an infinite cotree-diamond family,
  proving that the connected-kernel condition is strictly stronger than
  ordinary five-CDC;
- an explicit 30,450-vertex positive specimen with girth exactly 10 and
  certified oddness at least 8, so the search has entered the sourced
  minimum-counterexample domain; and
- a complete standard five-cover for that specimen, assembled
  compositionally and accepted by independent original-semantics checkers.

These are accompanied by two independent verifiers,
certificate-pipeline controls, a Lean formalization of the fixed-graph
semantics, blind raw-artifact audits, and reproducibility scripts.

## 2. Frozen statement and exact negation

For a finite undirected graph \(G=(V,E)\), the target asks for five indexed
edge-subsets \(C_0,\ldots,C_4\) such that

\[
 \deg_{C_i}(v)\equiv0\pmod2\quad(v\in V,\;0\leq i<5)
\]

and every edge belongs to exactly two indexed subsets.

“Five” faithfully means **at most five**: an at-most-\(k\) family, \(k\leq5\),
is padded by empty even subgraphs.  Indexed slots preserve repeated members.
The machine-checked equivalence is in
`formal/FiveCDC/FiveCDC/Padding.lean`.

The exact negation is the existence of a finite bridgeless \(G\) for which
no such indexed tuple exists.  Computationally, this means the complete
standard formula below is UNSAT.  No graph qualifies without a separately
checked proof certificate and an independent bridgelessness check.

Parallel edges are distinct edge values.  A loop has two incidences at its
endpoint, so it cancels from vertex parity but remains one edge subject to
exact-two coverage.  Even edge-subsets may be empty, disconnected, or have
vertices of any even degree.  These conventions are frozen in
`docs/statement-ledger.md`.

## 3. Mandatory SAT/XOR characterization

For each \(e\in E\) and \(i\in\{0,\ldots,4\}\), introduce
\(x_{e,i}\in\{0,1\}\).  Impose

\[
 \sum_{i=0}^{4}x_{e,i}=2\qquad(e\in E)
\]

as an integer cardinality constraint, and

\[
 \bigoplus_{\text{incidences of }e\text{ at }v}x_{e,i}=0
 \qquad(v\in V,\;0\leq i<5)
\]

as native XOR rows.  A loop contributes the same membership bit twice.

Setting \(C_i=\{e:x_{e,i}=1\}\) is a bijection between satisfying
assignments and indexed 5-CDCs.  The forward and reverse maps, including
loop multiplicity and parallel edges, are proved as an equivalence of Lean
witness subtypes in `formal/FiveCDC/FiveCDC/Encoding.lean`.

The two certificate-producing CNF routes are deliberately different:

- Verifier A uses chained XOR-gate auxiliaries.
- Verifier B uses no XOR auxiliaries and blocks every odd truth-table row.

Both encode exact-two with ordinary clauses.  Native XOR is used for
discovery with CryptoMiniSat; ordinary CNF is used with CaDiCaL for
certificate production.  A pseudo-Boolean parity alternative is specified
but not frozen as a third generator.

## 4. Sound search reductions

The audited one-way implication needed for search is

\[
\text{bridgeless counterexample}
\Longrightarrow
\text{simple bridgeless cubic counterexample}.
\]

It is obtained with explicit cubic port gadgets; a cover of the expanded
graph restricts to one of the original graph.  The reverse direction is not
claimed.

Minimizing first among bridgeless cubic **multigraphs**, two- and three-cut
gluing gives simplicity and cyclic 4-edge-connectivity.  Triangle and
four-cycle reductions give elementary girth at least five.  Published
results raise the minimum-counterexample working restrictions to girth at
least ten and oddness at least six.  The project does not claim a reduction
to cyclic connectivity five or six.  Details and scope are in
`docs/reductions.md` and `docs/proof-agent-audit.md`.

Brinkmann, Goedgebeur, Hägglund, and Markström generated all snarks through
36 vertices and report that even the orientable 5-CDC holds throughout that
census: <https://arxiv.org/abs/1206.6690>.  The small canonical run here is
therefore pipeline validation, not a new finite frontier.

The project nevertheless supplies modern per-instance artifacts for a
complete bounded theorem through order 22.  At order 22, canonical
generation yields 7,319,447 connected simple cubic classes, of which
7,187,627 are bridgeless and 12,892 are bridgeless non-Tait.  Exact cut and
girth filtering leaves 20 strict rows; lower complete filters leave three
strict rows through order 18 and six at order 20.  Every one of the 29 rows
has a standard five-cover checked in the original graph semantics and
against both full CNF encodings.

A clean-room audit independently scanned the full order-22 stream, exactly
matched all hard identities and structural classifications, regenerated
every lower even order, and checked all 29 models and 435 symmetry units.
Combining this enumeration with the audited minimum-order multigraph
reductions proves:

\[
\boxed{\text{Every bridgeless cubic multigraph whose components have
at most 22 vertices has a standard 5-CDC.}}
\]

This is not a theorem for arbitrary noncubic graphs of order at most 22,
because cubic expansion can increase order.  It is not an orientable or a
universal conclusion.

Graph covers, voltage lifts, and 2-lifts of a positive base cannot create a
counterexample: every base cover pulls back.  They were retained only as
positive stress tests.  Dot products and substitutions without a proved
preservation theorem were solved from scratch.

## 5. Search portfolio and finite outcomes

### Canonical simple cubic census through order 10

`geng` generated 27 connected simple cubic isomorphism classes at orders
4, 6, 8, and 10.  Independent premise checks retained 26 bridgeless graphs.
Both the native-XOR and CNF pipelines returned SAT on all 26, yielding 52
directly accepted models.  The Petersen graph was the sole
non-3-edge-colourable graph.  The girth-ten/oddness-six filter retained
zero graphs.

Automorphisms and the \(S_5\) action were used for cover canonicalization
and safe first-vertex symmetry units.  The retained run has 395
checksum-verified files.

### Structured constructions

Twenty-eight deterministic simple cubic bridgeless instances covered:

- flower snarks;
- generalized Petersen graphs;
- explicit dot products;
- a Petersen two-pole insertion;
- voltage and covering-graph controls.

All 28 standard formulas were SAT and all witnesses were accepted by both
semantic checkers.  Verifier B independently reconstructed a witness for the
order-40 oddness-six specimen after 145,856 backtracking nodes.

The two strongest specimens in the original structured batch were:

- order 40, girth 5, oddness 6: SAT;
- order 130, girth 10, oddness 0: SAT.

That original batch did not contain a graph satisfying both restrictions.
The later candidate-domain branch does: its explicit order-30,450 graph has
girth exactly 10 and oddness at least 8.  Its standard formula is SAT.  This
**enters one point** of the sourced minimum-counterexample domain; it neither
enumerates that domain nor excludes a counterexample elsewhere in it.

### Candidate-domain positive specimen

The deterministic graph in
`search/candidate_domain/runs/domain-20260725-v1/` is a proper
superposition of the 70-vertex graph \(R_4\): every one of its 105 edges is
replaced by the exact 288-vertex six-pole \(F_{10}\).  Independent checks
establish:

- 30,450 vertices and 45,675 edges;
- simple, connected, cubic, and bridgeless;
- girth exactly 10, with a retained ten-cycle witness;
- \(\rho(R_4)=7\), from an UNSAT LRAT lower certificate and a direct
  seven-vertex deletion upper witness;
- properness of the exact implemented \(F_{10}\), from a separately audited
  1,305-variable, 4,344-clause UNSAT formula whose 831,347,425-byte text
  LRAT is accepted by both `lrat-check` and CakeML `cake_lpr`.

Proposition 11 of Lukot'ka--Macajova--Mazak--Skoviera then gives
\(\rho(G)\ge7\).  Since \(\rho(G)\le\omega(G)\) and cubic oddness is even,
\(\omega(G)\ge8\).  The proposition is imported literature mathematics,
not proof-assistant formalized.

The standard five-cover was obtained without a monolithic search.  An exact
five-cover of \(R_4\) was combined with ten local \(F_{10}\) templates, one
for every pair label, whose six boundary semiedges all carry that label.
The assembled 45,675-edge witness passes direct exact-two and vertex-parity
semantics and fresh Verifier B checking.  The blind auditor reconstructed
the graph, both resistance and properness certificates, and the final v4
cover from raw artifacts and returned PASS.

None of the five coordinate complements in this particular v4 cover is
connected: their component counts are 4,275, 4,390, 3,295, 4,602, and
4,311.  Thus the retained standard witness does not itself certify the
stronger connected-kernel condition.  A separate monolithic
connected-kernel attempt on this graph was interrupted without a result.

Complete unconditioned source instances are retained in native XOR and in
the two ordinary-CNF encodings.  Giving the compositional witness as primary
units to CaDiCaL or CryptoMiniSat confirms that it extends to models of all
three complete encodings.  This fixed-witness extension check is not
reported as an unconditioned monolithic solve.

The recent high-flow-resistance \(H_2\) construction supplies a separate
stress test.  An exact reconstruction from the paper's vector figures and
labelled recursive boundary has 82 vertices, 123 edges, girth five, and no
cyclic cut below five.  An at-most-one-zero CNF is certified UNSAT by a
retained independently checked LRAT, while an explicit two-zero flow proves
resistance exactly two.  The two zero edges lie on a retained 23-edge
binary cycle whose complement is connected, and the complete standard
five-cover formula is SAT.  Both frozen semantics verifiers accept its
coordinate-size-\((47,62,39,44,54)\) witness.  Because the source provides
no machine-readable author edge list, the package records the inferred
boundary mapping and explicitly limits provenance to figure-based
reconstruction.

### Local obstruction mining

The exhaustive pair-label computation established:

- 60 allowed ordered cubic states, exactly the ordered triangles of \(K_5\);
- cut-state counts \(0,10,60,640\) at boundary sizes one through four;
- exactly 60 nonextendible four-cycle boundaries among 640 parity-valid
  boundaries, all alternating distinct intersecting pair labels;
- the Petersen-state histogram kernel is the 16-element cut space of
  \(K_5\).

The standard five-coordinate Petersen formula is SAT in four pipelines.
The deliberately modified four-coordinate Petersen formula is UNSAT; its
60-variable, 310-clause CNF has a retained LRAT accepted by two external
checkers.  This is a pipeline control, not the target problem.

### Eight-coordinate compression

A checked 112-vertex cubic 8-CDC has coordinate co-occurrence graph \(K_8\).
Since the five-bit distance-two graph has clique number five, that supplied
cover cannot be compressed to five coordinates by any fixed XOR
recombination.  Fixed merging and any fixed value-by-value map from the
seven nonzero \(\mathbb F_2^3\) values also fail.

These are no-go results for universal postprocessing of a supplied
eight-cover.  They do not show that the underlying graph lacks another
five-cover.

Allowing a graph-dependent recoloring of whole circuit components is
strictly more flexible than a fixed coordinate map, but it also fails
universally.  For a supplied cubic CDC, the least coordinate count obtainable
by partitioning its circuit components is exactly the chromatic number of
the component-conflict graph.  A connected, bridgeless 112-vertex supplied
8-CDC was constructed by 24 label-preserving two-switches so that every old
coordinate is one circuit and the conflict graph is \(K_8\).  Its exact
chromatic number is eight.  The construction closes only this component-wise
partition rule; changing the supplied cover or jointly choosing the
eight-cover remains open.

Even allowing an arbitrary affine relabelling before the full quotient lift
does not give a universal postprocessor.  An old 8-CDC pair label
\(\{s,t\}\) maps to \(\rho(s)+\rho(t)\) for any bijection
\(\rho:[8]\to\mathbb F_2^3\).  Translation cancels and \(GL(3,2)\)
only renames values and lines, so there are exactly 30 affine structures and
seven quotient lines per structure.  A direct audit finds zero liftable
cases among all 210 for the coordinate-tree supplied cover; the minimum is
two bad components.  A separate Gaussian elimination and the component
criterion agree case by case.  The connected affine control has one good
structure and three good lines.  This is still a supplied-cover no-go, not
target UNSAT.

### \(K_6\)-flow reconfiguration

Nonzero \(\mathbb F_2^4\) flow values can be identified with the 15
duads of \(K_6\).  At a cubic vertex the three incident duads are either
a triangle or a perfect matching; call the latter a defect.  A
triangle-only flow gives six Eulerian coordinate supports, and omitting
one \(K_6\)-star gives exactly a standard five-cycle double cover.  This
reformulation substantially overlaps the published duad/syntheme
framework, so the publication audit in `preprint-k6/NO-GO.md` recommends
against publishing the reformulation by itself.

Two exact packages identify the limitations of the natural descent
strategy.  First,
`search/k6-defect-snark-plateau-20260725/` freezes a 36-vertex,
cyclically 4-edge-connected snark flow with four defects and no
immediately defect-reducing constant-value cycle switch.  Its complete
\(2^{19}\)-cycle scan, independent four-pole calculation, graph audit,
dual-checked edge-colouring LRAT, and independent perfect-matching proof
all pass.  A checked path nevertheless has defect counts
\(4\to4\to2\to2\to0\), and a fifth star-cycle switch gives an explicit
standard five-cycle double cover.

Second, `search/k6-petersen-star-barrier-20260725/` proves that
triangle-preserving reconfiguration itself is insufficient.  A frozen
Petersen flow lies in a complete 720-state triangle-only component, the
free \(S_6\)-orbit, and every state uses all 15 duads.  Reaching a
star-omitting flow therefore requires reintroducing defects.  A checked
two-switch path \(0\to2\to0\) attains the parity lower bound and ends in
an explicit five-cycle double cover.

Third, `search/k6-petersen-ring-barrier-20260725/` turns the finite
obstruction into an exact infinite theorem.  A ring of \(n\) labeled
Petersen two-poles has a triangle-only component of exactly
\(15\cdot48^n\) states, all using all 15 duads.  A corrected local proof
splits neutral switches into crossing-label components and an even
subgraph induced by remote vertices; the latter induced graph is always a
forest.  A blockwise path \(0,(2,0)^n\) reaches a standard five-cover, so
the sharp barrier is still two.  The family has cyclic 2-edge cuts and
does not settle connectivity of the full nowhere-zero-flow
reconfiguration graph.  It is nevertheless a plausible short-note
contribution; `preprint-k6-petersen-rings/` contains an AI-disclosed draft
pending independent human review.

A universal proof by this route would still need a controlled nonmonotone
reconfiguration theorem; none is currently proved.

### Connected-kernel and flow-switch searches

For a nowhere-zero \(\mathbb F_2^3\)-flow \(\phi\) and Fano line \(L\), the
\(L\)-valued edges form a spanning join in a cubic graph.  If that join is
connected, the quotient-lift obstruction is vacuous and a five-cover is
constructed by a binary \(T\)-join.  This condition is exactly the
published connected congruent-join condition.  It also has an exact
five-coordinate meaning: quotienting by the weight-four vector omitting
coordinate \(i\) sends exactly the labels outside \(C_i\) to the chosen
Fano line.  Hence a connected-kernel flow exists if and only if some 5-CDC
has a connected coordinate complement \(E-C_i\).  It is a precise
strengthening of five-CDC and is now proved to be strictly stronger.

Canonical `geng` enumeration established the stronger connected-kernel
condition, with explicit lifted witnesses, for every connected simple
bridgeless cubic class through order 18:

| order range | generated | bridgeless | connected-kernel lift |
|---:|---:|---:|---:|
| 4--14 | 621 | 587 | 587 |
| 16 | 4,060 | 3,874 | 3,874 |
| 18 | 41,301 | 39,866 | 39,866 |
| **total** | **45,982** | **44,327** | **44,327** |

The fixed-flow switch audit exhaustively enumerated 556,248 nowhere-zero
flows on the 26 bridgeless canonical graphs through order 10.  Of these,
446,040 already lifted, 109,872 were repaired by one elementary circuit
switch, 336 by two, and none remained unresolved.  Every one of the
3,681,048 disconnected flow-line pairs admitted a component-decreasing
elementary switch.

A separate current-data portfolio tested 1,082 unique downloaded snarks,
including all records in the retained lists for cyclic connectivity at least
five through order 30, girth at least six through the available order-40
lists, circular flow number five through order 36, and the exact 31
order-44 oddness-four snarks.  Overlapping source lists account for the
difference between 1,085 raw and 1,082 unique records.  All 1,082 passed
fresh simple/cubic/connected/bridgeless checks and admitted an explicit
connected-kernel flow and lifted five-cover.  The list classifications are
source provenance; the run independently checks the graph premises and
witnesses, not the advertised cyclic connectivity, girth, circular flow
number, or oddness invariants.

A second current-data portfolio retained all four House of Graphs
strong-snark lists in the girth-at-least-five column through order 40:
7, 25, 298, and 7,654 records at orders 34, 36, 38, and 40.  All 7,984
records passed fresh simple/cubic/connected/bridgeless checks and admitted
an explicit connected-kernel flow and lifted five-cover, with no solver
limit or stronger-property UNSAT row.  Strongness and the advertised girth
remain source-list provenance; the graph premises and positive witnesses
are direct checks.  The authoritative result stream has SHA-256
`764d1a625b47d751351c997872164d91ab0ef4c5ab3980a2411ff66d392096cc`.

The order-40 Lukotka \(R_2\) witness was also reconstructed by a blind
checker.  Its \(\{1,2,3\}\)-kernel is a 39-edge spanning tree; every quotient
fiber and lifted label passes direct checks and both frozen verifiers.
Separately, exhaustive enumeration of all 192 perfect matchings confirms
girth five and exact oddness six.

The universal connected-kernel route is nevertheless false.  Replace every
cotree edge of a non-Tait cubic base \(B\) by a diamond.  Connectivity
forces the effective value of each diamond into the selected Fano line;
after contraction, the outside-line quotient support is an even subset of
the complementary spanning tree and is therefore empty.  This would
3-edge-colour \(B\).  Conversely, a local three-duad rule lifts every
standard five-cover of \(B\) through every diamond.

For Petersen this produces a 34-vertex, 51-edge simple bridgeless cubic
separator.  Its explicit standard cover has coordinate sizes
\(30,30,17,16,9\), while a 153-variable, 465-clause connected-kernel
relaxation is UNSAT with a 20,031-byte LRAT accepted by `lrat-check` and
CakeML `cake_lpr`.  Independent Python and JavaScript checkers reconstruct
the human construction, CNF, and positive target witness.  Iteration gives
orders \(10,34,106,322,\ldots\).  Thus all surviving universal arguments
must allow disconnected kernels.

The proved switch law is \(J'=J\) for a line-valued switch and
\(J'=J\mathbin{\triangle}C\) for an outside-line switch on a circuit
\(C\).  Consequently a component-minimal disconnected join forces each
complementary circuit meeting multiple components to use all four outside
values.  This four-value-surjective circuit is the current local
obstruction.

Allowing arbitrary binary-cycle rather than elementary-circuit switches
produces a sharper exact criterion: every outside color class must hit every
cycle whose symmetric difference with the join reduces its component count.
The smallest immediate hitting-set trap occurs at order 12.  Its four color
classes are disjoint two-edge transversals of all nine reducing cycles.
It is not sequence-stable: one line-valued preparation circuit followed by
one outside-valued circuit makes the join connected.  Across all 9,132
realizable disconnected joins on the 81 bridgeless canonical order-12
graphs, every join has some low-coordinate recoloring followed by a
component-reducing switch.

The preparation step now has an exact code formulation.  Write a flow as
\((p,q,H)\), where all three coordinates are binary cycles and
\(J=E-H\).  A line switch on the whole of \(H\) normalizes any chosen
outside value to \(4=(0,0,1)\).  Some low-coordinate choice prepares a
reducing switch exactly when

\[
 C\in Z_1(G;\mathbb F_2),\quad
 \kappa(J\mathbin\triangle C)<\kappa(J),\quad
 J\cup C\subseteq p\cup q.
\]

Equivalently, put \(T=E-(p\cup q)\).  For

\[
 \mu_G(T)=\min\{\kappa(E-H'):H'\in Z_1(G;\mathbb F_2),\ T\subseteq H'\},
\]

a realizable disconnected \(J=E-H\) is a trap exactly when every relevant
inclusion-minimal common-zero set \(T\subseteq H\) has
\(\mu_G(T)=\kappa(J)>1\).  Relevant \(T\)'s are matchings in a cubic graph.
Three-edge-colourable graphs satisfy the preparation lemma directly with
\(T=\varnothing\).

The primary canonical census exhausts the non-three-edge-colourable
bridgeless classes through order 18.  Its 179 hard order-18 graphs contribute
173,316 realizable disconnected joins, every one preparable and none a trap.
An independently written producer and replay checker exhaust all graphs at
orders 14 and 16, respectively validating 112,732 and 1,869,590 realizable
disconnected joins with zero traps.  This exact finite result removes
line-switch reachability from the proof obligation; it does not establish
the universal preparation lemma.

The universal preparation lemma is in fact false.  The 38-vertex package
`search/fixed-join-preparation-trap-20260725/` inserts Petersen 2-poles at
two edges of an 18-vertex base.  Its displayed high cycle has a
two-component complement and contains exactly 125 inclusion-minimal exact
zero sets, all with preparation minimum two.  Any hypothetical connected
complement is a connected spanning odd factor; terminal parity forces it
through both poles, and contraction gives a base odd factor containing
both roots while avoiding one of five exact base supports.  Exhaustive
enumeration of the 25 connected base odd factors rules this out.
Independent Python and JavaScript checkers agree, including a direct scan
of all \(2^{20}\) expanded binary cycles.  The graph has a target-standard
five-cover and two nontrivial two-edge cuts.  Thus this closes only the
unrestricted intermediate lemma and leaves open any suitably reduced-domain
preparation theorem.

There is a second exact reformulation:

\[
 \mu_G(T)=\min\{\kappa(F):F\text{ is a spanning odd factor of }G-T\}.
\]

Thus \(\mu_G(T)=1\) exactly when \(G-T\) has a connected odd factor.
Catlin's four-edge-connected theorem does not apply directly because the
endpoints of a nonempty relevant matching \(T\) have degree two in \(G-T\).
The tempting stronger claim that cyclic 4-edge-connectivity nevertheless
forces every relevant minimal \(T\) to have \(\mu=1\) is false.

There is one universal positive subcase.  By Tutte's peripheral-cycle
theorem, every edge \(e\) of a finite simple 3-connected cubic graph lies
on an induced cycle \(C\) with \(G-V(C)\) connected.  Cubicity supplies one
outside spoke at every vertex of \(C\), so \(E(G)-E(C)\) is connected and
\(\mu_G(\{e\})=1\).  A separate standard-library audit checks the theorem
computationally on all 29,037 edges of 985 premise-satisfying hard graphs
through order 20.  The order-18 singleton \(\mu=2\) control has an explicit
2-vertex cut and cyclic 2-edge cut and therefore does not contradict the
theorem.  This eliminates singleton higher-\(\mu\) obstructions from the
minimum-counterexample domain; it does not settle exact pairs.

Exact pairs nevertheless now admit a smaller exact search representation.
For a connected simple cubic \(G\ne K_4\), deleting a two-edge exact zero
set and suppressing its four degree-two endpoints produces a loopless
Tait-colourable cubic core.  Girth at least five leaves exactly two
geometries: four once-subdivided marked edges, or two once-subdivided edges
and one twice-subdivided edge.  A connected odd factor exists exactly when
the core minus those marked edges has a connected spanning subgraph
satisfying an explicit parity equation on every marked component.  In the
single-cross form, connectivity forces the two outer edges of the
twice-subdivided path.

An independently written standard-library checker enumerated all 1,439
exact pairs on the 27 canonical simple cubic graphs through order 10.  The
only suppression boundary cases were the three perfect matchings of
\(K_4\).  It verified 530 independent-end cases, all 60 girth-five
single-cross cases, and 19,624 fixed-subgraph parity/orientation
comparisons.  Direct connected-odd-factor enumeration agreed throughout;
all 480 middle-only path selections were odd but disconnected.  This is a
proved and audited reformulation of the pair obligation, not a universal
solution of it.

A targeted use of this representation sampled 15,000 marked sets on
order-24 Tait-colourable cores.  Complete odd-factor enumeration found 276
failures, but all 828 external pairings had explicit Tait colourings.  The
mixed one-cross sample found 15 failures among 2,000 marked triples, and
all 30 pairings were again Tait-colourable.  Every reconstruction in these
two samples has girth three or four, so none survives the strict
minimum-counterexample reductions.  Complete Flower-snark controls
independently checked 2,475 exact minimal pairs on \(J_5,J_7,J_9\), all
with connected-complement witnesses.  A second implementation re-enumerated
every failed affine odd-factor space and checked all 858 reconstructions.
This is a rigorously scoped null result, not the missing pair theorem.

The qualifier “minimal” or “non-Tait” is essential.  The literal claim
that every exact pair in a cyclically 4-edge-connected cubic graph has
\(\mu=1\) is false.  Opposite edges of \(K_4\) give the smallest example.
The dodecahedral graph gives a nonvacuous girth-five, cyclically-5 example:
a retained exact flow has zero set \(\{(0,1),(2,6)\}\), and exhaustive
enumeration finds 512 containing binary cycles with minimum
complement-component count two.  Both graphs are Tait-colourable, so their
pairs are not inclusion-minimal because the empty zero set is exact.

After making that correction, a complete pair screen on all 7,654 retained
order-40 strong snarks checks 13,547,580 pairs.  Exactly 517 arbitrary
pairs lack a containing cycle with connected complement, and all 517 fail
the exact \(\mathbb F_2^2\)-zero-set test.  Thus the corrected pair
statement has no counterexample in this finite corpus.  Catlin's ordinary
4-edge-connected collapsibility theorem does not close the universal
argument: perfect-matching contraction preserves only aggregate parity at
each contracted vertex.  When the vertex is split back into two ports, the
quotient factor can disconnect.  Requiring the lift to stay connected is
an additional transition-system condition not supplied by Catlin's
theorem.

The zero sets themselves now have a purely graph-theoretic form.  A relevant
exact \(T\) is a matching; after deleting \(T\) and suppressing its
degree-two endpoints, the resulting cubic pseudograph is Tait-colorable.
Inclusion-minimality is minimality of that colorability-restoring deletion,
and relevance says each component of \(G-T\) contains an even number of
\(T\)-endpoints.  Splitting an odd factor into endpoint matchings, branch
attachments, and a branch subgraph gives an exact attachment-parity formula
for \(\mu_G(T)\).  On one order-34 \(\mu=2\) witness, two branch-graph
bridges impose incompatible cut parities for all 16 possible attachment
choices, giving a direct obstruction rather than only an exhaustive cycle
calculation.

Complete minimal-support audits on all seven order-34 and all 25 order-36
retained strong snarks found:

| order | graphs | minimal zero sets | relevant \(\mu>1\) | realizable disconnected joins | traps |
|---:|---:|---:|---:|---:|---:|
| 34 | 7 | 4,418 | 7 | 1,824,090 | 0 |
| 36 | 25 | 15,391 | 29 | 13,047,448 | 0 |
| 38 | 298 | 234,582 | 597 | 311,344,912 | 0 |
| 40 \(R_2\) | 1 | 33,517 | 9,516 | 1,968,017 | 0 |

At order 36, 23 exceptional sets have \(\mu=2\) and six have \(\mu=3\).
Every realizable disconnected high cycle in the complete solver-assisted
audits contains
some other minimal zero set with sufficiently smaller \(\mu\), so every
one is preparable. Independent two-bit blocking encodings reconstructed the
order-34 and order-36 minimal families, all 36 exceptions, and all
14,942,208 high-cycle classifications. The completeness proofs were checked
internally by CaDiCaL but their temporary proof bytes were not retained, so
these remain solver-assisted finite results rather than standalone
universal certificates.

The order-38 primary computation adds 188,843 pairs, 44,434 triples, 1,287
quadruples, and 18 quintuples. Its 597 relevant exceptions comprise 582
sets with \(\mu=2\) and 15 with \(\mu=3\), spread over 119 graphs. An
independent two-bit blocking audit validated every retained flow and
\(\mu\) witness and exhaustively reclassified all 312,475,648 high cycles.
Across the order-34, order-36, order-38, and \(R_2\) audits there are
287,908 minimal supports, 10,149 relevant pointwise exceptions, and
329,515,008 complete high-cycle classifications. All 328,184,467
realizable disconnected joins are preparable. This aggregate remains
finite and does not contradict the later 38-vertex preparation trap.

An independent margin reconstruction additionally checks every high
containing a pointwise exception on the retained order-34/36/38 sources.
Using a producer-free parser and a clean-room Walsh--Hadamard computation,
it evaluates 131,596,288 affected highs on all 134 affected graphs and
matches every complete histogram.  The minimum numbers of contained
\(\mu=1\) supports are 21, 22, and 20, attained on 1, 16, and 3 highs,
respectively; all necessary-candidate counts remain zero.  It separately
validates all 254,391 retained flow witnesses and the edge-mask boundary.
The frozen reports' helper path and Mach-O hash refer to an unretained
temporary binary, so those two provenance fields are not replayable.
Rebuilding the bound source reproduces all normalized reports, and the
clean-room result supplies an independent mathematical check.

A separate direct screen covers all 7,654 retained order-40 graphs in 60
batches.  It enumerates 6,053,028 minimal exact supports, classifying
6,009,319 as \(\mu=1\) and 43,709 as non-\(\mu=1\), and finds zero
necessary trap candidates.  Necessity follows because every trap high
contains some inclusion-minimal exact support, traphood forces that
support's preparation minimum to equal the disconnected complement count,
and any contained \(\mu=1\) support would prepare it.  Candidate SAT with a
two-component complement would already certify a trap by forcing every
contained minimal support to have \(\mu=2\).

The independent audit now replays the complete source: all 60 batches,
7,654 graphs, 6,053,028 directly checked supports, and
16,051,601,408 binary cycles.  It also internally checks 7,654
support-completeness UNSAT proofs and 7,654 candidate CNFs.  The support
split and zero-candidate total match the primary run exactly; the frozen
audit ledger is
`fb9ebf90f57453efff948dd6d9cbc05c76bb086cdedc42e2396adaf94761c457`.
This conclusion is still strictly finite: it excludes preparation traps on
the retained source, not on all bridgeless graphs, and it is not a
five-CDC conclusion.

The small-boundary companion census is complete on the 212 hard bases
through order 18.  It reconstructs 3,336 relevant minimal supports with
\(\mu\)-profile \(1:3272,\ 2:63,\ 3:1\).  All 29,312 highs containing one
of the 64 non-\(\mu=1\) supports are dominated by a contained \(\mu=1\)
support, yielding zero candidates and traps.  A producer-free audit
independently checks all source identities and graph premises, exhausts
194,859,008 ordered cycle pairs, and matches every support and high
classification.  Its status is PASS.  This exact result remains limited to
the frozen small boundary.

The complete canonical order-20 extension is also independently verified.
Of 510,489 connected simple cubic classes, 497,818 are bridgeless and
1,388 of those are non-Tait.  Literal traversal of 5,821,693,952 ordered
cycle pairs reconstructs 21,686 minimal exact supports, with relevant
\(\mu\)-profile \(1:21,219,\ 2:455,\ 3:8\) and four irrelevant supports.
All 425,024 affected highs contain a \(\mu=1\) support; the minimum such
margin is three, on 2,240 highs across 20 graphs.  Thus candidates and
traps are zero.  The clean-room replay matches all 1,388 semantic rows and
finds exactly six cyclically 4-edge-connected hard graphs, all of whose 170
supports have \(\mu=1\).  This is an exact finite order-20 result and has
no universal or five-CDC conclusion.

The \(R_2\) row uses a different completeness route.  Its Petersen 2-pole
decomposition gives the exact support count
\(12\cdot14^3+3\cdot14^2+1=33,517\), with 33,516 size-four matchings and one
irrelevant size-six support.  A direct enumeration of all
\(2^{21}=2,097,152\) binary cycles found a relevant \(\mu\)-profile
\((24,000,8,160,1,308,48)\) for \(\mu=1,2,3,4\), respectively, and again
zero high-specific traps.  This is exact finite evidence on a graph already
known to have a 5-CDC with a connected coordinate complement.

The independent checker proves a stronger finite statement about this
cycle space: 1,970,577 cycles contain a support with \(\mu=1\), and the
other 126,575 contain no relevant support at all.  In particular, no cycle
has best-contained minimum \(2,3,\) or \(4\).  The large exceptional support
population is therefore pointwise real but globally dominated on \(R_2\).
A generic incremental SAT enumerator independently returned exactly the same
33,517 supports with validated flow witnesses; its terminal UNSAT proof was
not retained, so the pole factorization remains the completeness argument.

This domination also has a compact structural proof.  Relevant-support
containment is equivalent to nonempty intersections with the unreplaced
base and all three pole interiors.  Every nonempty pole restriction contains
an edge far from the cut edge, because the cut edge and its four neighbors
form a tree.  Choosing those three far edges and any used base edge produces
an all-far support.  Four base odd-factor witnesses and three pole fragments
glue to a connected spanning odd factor avoiding all 12,000 such supports.
The local state product
\(15\cdot31^3+3\cdot16\cdot31\cdot32^2\) gives 1,970,577 directly.  A
standard-library blind audit independently checked the full compatible
tuple space, including the type-B necessity argument, and every glued
factor without importing the certificate producer.

The related rooted-preparation necessity census exhausts all 44,327
connected simple bridgeless cubic bases through order 18 and all 1,181,250
singleton edge roots. The 44,115 3-edge-colourable bases have the uniform
nowhere-zero-flow/full-factor witness. On the remaining 212 bases, complete
cycle-code enumeration covered 194,859,008 ordered flow pairs and
5,216,238 realizable-high/root obligations; neither an unrooted nor a rooted
failure occurred. A separate checker regenerated the canonical graph
streams, used an independent direct edge-colouring search, and recomputed
all 212 exact-zero-set families and rooted quantifiers. This is a finite
negative search for a necessity witness, not a theorem that the rooted
premise is redundant and not a five-CDC result.

The stronger multi-root inference is false. An exact census checks all
71,313 edge pairs on the 212 hard bases and 67,244,094
realizable-high/pair obligations. Nine root pairs fail on two order-18
graphs; the failures cover 128 highs and 144 obligations, while all lower
orders pass. An independent replay rebuilds every hard graph's cycle code,
exact-support family, connected odd factors, and unordered pair-root
quantifiers and matches every aggregate. On the first 18-vertex graph6 record
`Q????B?K?WWCg_?sIG?s?HO?KG?`, every singleton-root obligation passes, but
the high \(\{0,2,3,5,10,11,18,20\}\) fails for roots \(\{9,19\}\).
Independent enumeration of the full 1,024-word cycle code produces exactly
the five high-contained minimal supports
\(\{10\},\{11\},\{18\},\{20\},\{2,5\}\). Their unrooted minima are
\(1,1,1,1,2\), while every pair-rooted minimum is two. Exactly 13 connected
odd factors avoid some candidate, and none contains both roots. This
invalidates only the deduction of arbitrary multi-root preparation from
singleton preparation; it neither invalidates the conditional closure
theorem nor gives a five-CDC counterexample.

The exact adaptive transfer theorem resolves which rooted premise is needed
for a fixed next Petersen-2-pole substitution edge. If \(G=B[P_2/s]\), a
surviving edge \(e'\) pulls back to roots \(\{s,e\}\); a new terminal or any
internal pole edge pulls back only to \(\{s\}\). A clean-room checker
independently exhausts all cut binary/flow states, all internal fragment
subsets, and all 882 high/internal-root pairs. It finds precisely the four
deletion-useful fragments in the proof. On the order-28 graph obtained from
the order-18 pair witness, it enumerates all 32,768 cycle complements and
checks every one of the 150 connected odd factors containing surviving
root 19. All project to pair-root factors downstairs and none avoids a
contained support, validating the claimed boundary obstruction. This gives
a nested newest-pole rule, not unrestricted branching, universal unrooted
closure, or a five-CDC conclusion.

Induction now turns that newest-pole transfer into an infinite rooted
preparation family. Every substitution adds 10 vertices and 15 edges, and
each resulting graph is separately rooted at all 14 internal and two
terminal continuation edges. An independent implementation constructs all
16 choices and exactly reverses a canonical depth-three
base/internal/terminal control. It also audits finite coverage independently
of the producer: all 7,984 order-34/36/38/40 source graphs are parsed,
premise-checked, and canonically identified, while 14,067,888 edge pairs are
tested through cycle-space column equality. Zero two-edge cuts occur. Since
the two terminals of any cut Petersen pole are the complete boundary of
its ten-vertex shore, their removal must disconnect the graph; zero
two-edge cuts therefore means zero first contractions in this portfolio.
The infinite theorem is conditional on a singleton-rooted base, and the
zero-coverage conclusion is limited to these frozen rows. Neither resolves
five-CDC.

## 6. Strongest structural result: quotient-lift criterion

Let

\[
 E_5=\{x\in\mathbb F_2^5:|x|\equiv0\pmod2\},\qquad
 D_5=\{x\in E_5:|x|=2\}.
\]

A 5-CDC is exactly a conserved \(D_5\)-valued edge labeling.  Quotient
\(E_5\) by a forbidden weight-four vector.  The quotient is
\(\mathbb F_2^3\); among its seven nonzero values, a Fano line \(L\) has two
allowed lifts per value and the four outside values have one allowed lift
each.

For a nowhere-zero quotient flow \(\phi\), the prescribed outside lift bits
extend to a binary cycle exactly when every connected component \(K\) of
the \(L\)-valued edge subgraph satisfies the boundary parity condition.
Flow conservation makes failure equivalent to:

> all four values outside \(L\) occur oddly on \(\delta(K)\).

Therefore a 5-CDC exists exactly when there are a nowhere-zero
\(\mathbb F_2^3\)-flow \(\phi\) and a Fano line \(L\) with no component
having that four-value odd boundary.

An exact eight-vertex cubic bridgeless example carries a fixed
\(\mathbb F_2^3\)-flow for which every one of the seven lines fails.  The
graph is 3-edge-colourable and has a 5-CDC, so this only disproves the
shortcut “keep an arbitrary flow and choose a line.”  The unresolved
bottleneck is whether one can always choose or modify the flow so the
component obstruction disappears.

The complete proof and exhaustive audit are in
`docs/proof-agent-audit.md`.

### Exact cubic matching/four-flow certificate

The existence characterization itself is prior: Hoffmann-Ostenhof,
Corollary 0.6, characterizes cubic graphs with a 5-CDC by a matching
\(M\), a nowhere-zero 4-flow on \(G-M\), and two 2-regular subgraphs whose
exact intersection is \(M\)
(<https://doi.org/10.1007/s00373-012-1169-8>).  The contribution below is
the convention-complete proof, exact SAT certificate form, and the
subsequent component-parity analysis.

There is also an exact target-standard formulation, separate from the
connected-kernel strengthening.  A finite loopless cubic multigraph has a
5-CDC if and only if it has a matching \(M\), binary cycles \(A,B\) with
\(A\cap B=M\), and an \(\mathbb F_2^2\)-flow whose exact zero set is \(M\).
The project proves both constructions explicitly and encodes the theorem
with five primary variables per edge.  An independent audit checked the
quotient and lift algebra, multigraph/disconnected boundary cases, all
2,296 clauses and 328 native XOR rows of the \(H_2\) instance, and a direct
reverse reconstruction of five Eulerian edge sets.

The intersection condition has the exact component form
\[
\forall W\in\operatorname{Comp}(E-H),\qquad
|W\cap\partial M|\equiv0\pmod2
\]
for some binary cycle \(H\supseteq M\).  Equivalently, the certificate uses
a spanning odd factor avoiding \(M\), with an even number of \(M\)-endpoints
in each component.  This is weaker than requiring the odd factor to be
connected.  Exhaustion of the seven order-34 non-\(\mu=1\) supports finds
two satisfying this weaker condition and five not satisfying it; all
affected graphs have a different connected-complement support and remain
positive.

For an exact-zero matching \(M\), the intersection condition has an
equivalent classical packing form.  With \(K=G-M\) and
\(T=\partial M\), cycles \(A,B\) satisfy \(A\cap B=M\) exactly when
\(K\) contains two edge-disjoint \(T\)-joins.  The restricted
\(\mathbb F_2^2\)-flow makes \(K\) bridgeless.  This does not by itself
force the minimum \(T\)-cut to be two: a \(T\)-odd component has empty
boundary and no \(T\)-join.  Under the additional componentwise
\(T\)-even condition, the cut minimum is two, and the imported
Codato--Conforti--Serafini theorem makes any remaining failure require an
odd-\(K_{2,3}\) graft minor.  A
universal proof would follow from an exchange lemma showing
that every genuinely nonpacking minimum exact-zero matching can be replaced
by a smaller one.  That lemma is not proved.

The blind-audit correction is reproducible rather than merely narrative.
The frozen ten-vertex graph6 instance `Is?AXW[[?` is simple, cubic,
connected, and bridgeless.  Its exact-zero matching leaves two
\(K_{2,3}\) components with three terminals apiece, so the complement has
no \(T\)-join and cut minimum zero.  All three quotient graphs are forests.
The same independent checker verifies a Tait colouring and a standard
five-cover, proving that this is a countermodel to the unqualified
intermediate inference, not to five-CDC.

A second frozen countermodel shows that global minimum cardinality does not
repair the universal fixed-support assertion.
`search/minimum-component-parity-countermodel-20260725/` contains a
42-vertex graph with a minimum size-three exact-zero matching whose
complement terminal profile is \((3,3)\).  A short three-pole capping
argument proves the lower bound, and a separately reconstructed
314-variable, 960-clause UNSAT instance has an LRAT accepted by both proof
checkers.  Of the 366 projected minimum supports, only this one is
parity-bad; the other 365 have connected complements and a retained
minimum alternative yields a checked standard five-cover.  Thus the
existential minimum-support route survives, while any proof that silently
chooses an arbitrary minimum support does not.  The bad support is a
nontrivial cyclic three-edge cut and is outside the reduced
cyclically-4-edge-connected counterexample domain.

The companion finite cap diagnostic probes the five-terminal scale that
can first survive that reduction.  From the 192-vertex Tait core of
reconstructed \(H_5\), it rebuilds every one of the 3,024 five-cycle caps
obtained from 252 marked-path choices and 12 cyclic orders modulo dihedral
symmetry.  A producer-independent checker verifies that every resulting
simple cubic bridgeless graph has an exact-zero matching of size at most
two.  This is a complete theorem for the retained corpus, not a universal
five-boundary or five-CDC theorem.

The source-independent five-pole calculation is sharper.  It classifies
all 6,240 xor-zero ordered boundary words into 62 \(S_5\)-orbits and four
human-checkable Eulerian-multigraph types.  A fixed \(C_5\) cap order admits
4,620 words (46 orbits), and every orbit is admitted by some one of the 12
orders.  This yields a conditional five-cut reducibility theorem.  Directly
checked disjoint abstract state sets of sizes 8 and 10 nevertheless meet
every cap set and obey the known bichromatic-switch closure, proving that
these finite necessary axioms alone are insufficient.  No graph pole
realizing either abstract set is claimed.

The follow-up realizability census is exact within a larger natural finite
scope.  All 5,214 connected simple internally bridgeless
terminal-distinct cubic five-poles through order 13 have at least 46 of
the 62 boundary orbits.  The 298 sharp relations are exactly ordered
\(C_5\)-cap relations.  Every one of the 19,513 analogous four-poles
through order 14 has nine or ten of the ten boundary types, so neither
small signature in Máčajová--Mazzuoccolo--Tabarelli Conjecture 3.7 occurs
in that scope.  A human degree-count proof shows that an internal bridge
of a five-pole would create a cycle-separating cut of size at most three
in the reduced minimum-counterexample domain.

The five-pole threshold screen has now been extended exhaustively to the
69,243 internally bridgeless order-15 cores.  Every record reaches 46
satisfiable boundary orbits before the classifier stops.  A separate
standard-library replay regenerates the canonical corpus, checks all
degree profiles and bridges, and matches every retained record; optional
full mode recompiles and demands byte-identical classifier transcripts.
This threshold-only run does not count exact 46-state relations.

The package
`search/pole-state-realizability-20260725/` regenerates these censuses
from canonical graph streams and exact boundary SAT queries; quick mode
replays through five-pole order 11 and four-pole order 12.  Larger seeded
samples through pole order 25 preserve the same lower bounds.  The solver
trust and finite scope are explicit: no universal 46-state or 9-state
theorem is claimed.  Coherent bichromatic-pairing/transport constraints
still admit the abstract small signatures, so internal path-intersection
topology remains the precise gap.

The logical strength of the five-pole target has also been corrected.
Replacing one edge \(uv\) of any simple bridgeless cubic graph by a
six-edge \(u\)--\(v\) path produces an internally bridgeless five-pole
whose five internal path vertices are the terminals.  Summing the pole
equations over the old graph vertices makes the two path-end labels
equal, so any pole labelling contracts to a Five-CDC of the original
graph.  The reverse extension uses path labels
\(01,02,03,01,02,01\).  Hence universal five-pole nonemptiness, and a
fortiori the 46-state theorem, would resolve standard Five-CDC.  It is
not merely a cut-reduction lemma.

A partial exchange inequality is proved directly.  If \(J\) is any
\(T\)-join and \(c\) is one of the three nonzero values of the restricted
flow, switching by \(c\) on \(M\cup J\) makes
\(J\cap\phi^{-1}(c)\) the exact zero set of another flow; cubic parity makes
that set a matching.  Thus minimum cardinality of \(M\) gives
\(|J\cap\phi^{-1}(c)|\ge|M|\) for every color, and
\(|J|\ge3|M|\).  The proof is elementary and fully written out, but the
inequality does not rule out the graft minor or prove packing.

The checkable finite result is unusually complete.  All 20,749 minimum
supports on the complete order-20 hard corpus pass the exact extension
criterion.  On reconstructed \(H_3\), all 92,313 minimum exact-zero
matchings are enumerated and all extend.  Their semantic witnesses are
checked row-by-row, while a support-blocking completeness CNF is UNSAT with
an LRAT accepted by both `lrat-check` and CakeML `cake_lpr`.  Minimum
witnesses also extend on \(H_4\) and \(H_5\).  The package ledger is
`623c4d27043934fcca68534f66c252e62357714916d467a1b349b66debf19904`.

At the full hard order-22 boundary, all 12,892 frozen rows have some
extending minimum support.  The minimum-size profile is
\(1:12885,\ 2:7\).  A producer-independent verifier checks all compact
witnesses and reverse lifts; the seven at-most-one lower-bound LRATs pass
both proof checkers.  The package ledger is
`ed334f2df4131ed29b2924e4178e7f7853cf5a143e0427ac91ebb2c274d343f5`.
This finite evidence remains correct, but the unrestricted minimum-zero
matching conjecture is now refuted by the independently checked
130-vertex package
`search/minimum-zero-exchange-countermodel-130v-20260727/`.  That graph
has \(r_f=r_M=5\), needs matching size six in every matching/four-flow
five-cover certificate, and nevertheless has an explicit standard
five-cover.  Hence it refutes the proof route, not Five-CDC.

The stronger fixed-coordinate premise is already false on Petersen.  Its
spanning two-factor of two 5-cycles cannot be any member of a standard
5-CDC, although the graph has an unrestricted 5-CDC.  Two exact restricted
CNFs are UNSAT, each with an LRAT accepted by both independent proof
checkers, and a producer-free 4,096-flow enumeration agrees.  Thus an
argument may change the high cycle as well as the low flow coordinates; the
certified result is not graph-level UNSAT.

For a cheaper necessary screen, the ten pair-label quotients can be encoded
as ten independent \(\mathbb F_2^2\)-flows whose nonempty exact zero sets
partition the edges.  This relaxation is SAT on \(H_2\); its converse is
not claimed.

The next reconstructed resistance-family member \(H_3\) is also positive.
It is a cyclically 5-edge-connected 122-vertex snark with certified flow
resistance three, but its direct standard formula and exact
matching/four-flow formula are both SAT.  The direct cover has coordinate
sizes \(77,74,58,77,80\).  Its compact resistance LRAT, graph properties,
two-verifier target checks, and matching-form reverse lift have all passed
a fresh independent replay.

Two further exact recursion steps remain positive.  The reconstructed
\(H_4\) and \(H_5\) have orders 162 and 202, and certified flow resistances
four and five.  Independently reconstructed cyclic-cut CNFs and LRATs prove
cyclic connectivity at least five in both cases.  Their authoritative
standard formulas are SAT, with direct coordinate sizes
\(130,112,68,72,104\) and \(144,143,95,98,126\), respectively; both
semantic verifiers and independent matching/four-flow reverse lifts agree.
The four new cyclic-cut/resistance LRATs pass both the C checker and the
CakeML-verified checker.

The finite family search has since produced a uniform positive transfer for
the frozen figure reconstruction \(\widehat H_n\), \(n\ge2\).  A
40-vertex, 55-edge open \(J\)-tile has identical input and output
\(D_5\)-state
\[
(01,01,02,23,03).
\]
A global relabeling puts the complete \(\widehat H_2\) witness into that
state.  Conservation at the 40 tile vertices and the two closure identities
then give a direct gluing induction, with coordinate vector
\[
(62,54,39,47,44)+(n-2)(32,24,29,20,15).
\]
The package checker validates the full base, tile, recursive topology, and
edge-for-edge \(\widehat H_2\)--\(\widehat H_5\) controls; six corrupted
certificates are rejected, and the finite boundary algebra also compiles in
Lean.  The package ledger is
`e09cee11f74b19e4a08f18c94534207e44f601a29f059a15fb614154900cbfac`.
This theorem is family-specific, standard rather than orientable, and does
not resolve the universal conjecture.

It is also not a new existence mechanism for the intended author family.
The coloring printed by Mattiolo--Negrini--Pagani has two conflicts, each
with incident colors \((a,c,c)\).  The \(a\)-edges are a perfect matching;
the complementary 2-factor has exactly two odd circuits.  Huck--Kochol's
1995 theorem already implies a standard five-CDC for every author-defined
\(H_n\).  The stable labeling and certificate packaging may be distinct,
but a categorical novelty claim is not supported.  Because the source has
no author-supplied graph file, the project distinguishes the published
\(H_n^{\mathrm{MNP}}\) from the frozen \(\widehat H_n\).
Moreover, the bare two-subset \(D_5\) labeling is explicitly prior:
Máčajová--Mazzuoccolo--Tabarelli (2026), Definition 3.1, calls the same
object a `CDC-coloring`, and its Remark 3.2 applies the boundary framework
with at most five colors.  Only the specific stable tile remains a plausible
new artifact, pending specialist comparison.

A separate human argument now disposes of the all-singleton
Gallai--Edmonds barrier branch for the standard conjecture.  If
\(V(G)=D\dot\cup W\), \(D\) is independent, and
\(|W|=|D|+2\), cubic degree counting gives exactly three edges in
\(G[W]\).  A perfect matching through any one of them contains exactly
one, so its complementary 2-factor contains precisely the other two.
Every remaining 2-factor edge crosses \((D,W)\); consequently the
2-factor has zero or two odd circuits.  Huck--Kochol's 1995 theorem gives
a standard five-cycle double cover.  This closes the singleton branch
without proving the stronger prescribed-root theta lemma.  The
one-five-boundary factor-critical branch remains the exact open case of
this route.  A full proof and the independently replayed order-28 local
insertion screen are in
`scratch/root-insertion-two-factor-frontier.md`.

## 7. Verification and certificates

Verifier A 1.0.0 is frozen by a source manifest.  Verifier B 0.1.0 is an
independently written Go-standard-library implementation frozen by a
root-owned external manifest.  Cross-check controls cover:

- a simple graph;
- the Petersen graph;
- loops, parallel edges, and disconnected components;
- a bridged negative control.

Both encodings and both direct semantics checkers agree on every cross-fed
model.  The bridged one-edge graph is UNSAT in both encodings, and both
fresh LRATs are accepted by pinned `lrat-check` and CakeML `cake_lpr`.
Because this graph has a bridge, neither proof is a counterexample
certificate.

The retained modified-\(k=4\) Petersen LRAT is also accepted by both
checkers.  There is **no target-standard bridgeless UNSAT certificate**.

The blind auditor independently reconstructed raw graph semantics, both CNF
families, canonical counts, model validity, automorphism/S5
canonicalization, exact oddness, local obstruction counts, manifests, and
the retained LRAT controls without importing either verifier or any search
implementation.  Its final result is PASS with zero failures.

The audit found one hardening issue: Verifier A's solver-model parser accepts
a missing SAT status and can accept an `UNSATISFIABLE` followed by
`SATISFIABLE` history.  Every retained model nevertheless passes the blind
auditor's strict parser and direct graph semantics.  This does not change a
recorded result, but Verifier A should be hardened before relying on it in a
future counterexample acceptance package.  Verifier B's recursive bridge DFS
also has a potential resource limit on very large graphs.

## 8. Formalization

The Lean 4 project under `formal/FiveCDC/` pins Lean 4.32.1 and mathlib
commit `520045ab14e26149ee970e2e617ca04b09bde5d6`.  It proves:

- the fixed-graph SAT/XOR witness equivalence;
- loop and parallel-edge semantics;
- at-most-five iff five via empty padding;
- the restricted \(D_5\)-flow iff five-CDC equivalence.

The build completes without `sorry`, `admit`, `unsafe`, or custom axioms and
passed a separate semantic audit.  It does not formalize bridgelessness,
the universal theorem, the exact negation, search reductions, CNF
certificates, or orientability.

The strict one-switch version of the minimum-support exchange lemma is also
false.  The 16-vertex package
`search/minimum-switch-local-plateau-20260725/` gives a size-two exact-zero
matching with no two edge-disjoint \(T\)-joins and no strictly decreasing
matching-preserving constant-value cycle switch.  Both verifiers enumerate
the 512 binary cycles, all three values, and all 128 affine \(T\)-joins.
The state escapes by a neutral switch and then a decreasing switch, with
support profile \(2\to2\to1\); the final globally minimum support packs.
The primary canonical census finds no such local plateau through order 14
and 64 flow signatures at order 16, but no nonpacking globally minimum
support.  The package SHA-256 is
`17eb426b9f8311e5af4d8247f1c4025f8fe730f74425cd3242c15dda87895d0f`.
Thus global minimum-support packing and neutral nonincreasing
reconfiguration remain open, while strict local descent is closed as
false.

The exact follow-up package
`search/minimum-switch-neutral-components-n16-20260725/` verifies the
complete support-\(\le2\) state graph on all six order-16 plateau hosts.
Both implementations agree on 33,546 ordered states and 384 local
plateaus; every state reaches size one inside the sublevel graph and every
plateau has distance exactly two.  This proves neutral-then-descent only on
that finite boundary.  Its package SHA-256 is
`7d0bb2fc8497bde97e4a205d0676e0db9496da61b790d606ad4450ecacb17d02`.

The complete hard order-18 extension is independently replayed in
`search/minimum-switch-neutral-components-n18-20260725/`.  The elementary
bucket lemma says one-switch adjacency is exactly equality of \(p\), \(q\),
or \(p+q\).  Across all 179 graphs the two implementations agree on
1,680,414 ordered support-\(\le2\) states and 7,704 strict local plateaus
on 56 graphs.  Every plateau has distance exactly two from size one and no
state is unreachable.  The package SHA-256 is
`13ef63605817255cb1e27cd803b832498c98a3a9dd4118cf8a7ec7f74f83096f`.
Higher minimum-support levels remain open.

The complete order-20 continuation is independently replayed in
`search/minimum-switch-neutral-components-n20-20260725/`.  Both
implementations agree field-for-field on 1,388 hard graphs, 20,161,044
ordered states, and 118,134 strict local nonpacking plateaus.  Every plateau
has distance two.  The 21,492 states that do not reach size one are exactly
the states of the unique minimum-size-two graph, and all of them already
pack.  Thus every nonpacking state reaches size one at this finite boundary.
The package SHA-256 is
`9cfc63ef7c4883bf5b18758e800b3b28c6d565cb6a5832c810e92be447174393`.
The universal higher-support statement remains open.

The complete minimum-size-two order-22 continuation is frozen in
`search/minimum-switch-packing-components-n22-20260725/`.  There is no
size-one state on its seven graphs.  Of 1,441 distinct globally minimum
supports, 15 do not pack, so the universal all-minima statement is false.
All 2,808 ordered realizations of those supports have exact neutral-switch
distance one from a packing state.  Its package SHA-256 is
`0532c24206dd4fd10aa159227680d6296e707e285a1d09d921591920e7ae299a`.

The first complete size-three neutral-component census is
`search/minimum-size-three-packing-components-20260725/`.  On the
42-vertex component-parity countermodel, 290 of 366 globally minimum
supports pack and 76 do not.  The 3,670,272 ordered flows form 611,712
global-colour orbits.  Every nonpacking orbit reaches packing, but 720
orbits have exact distance two, so no one-switch theorem survives.
Independent Python and C++ implementations agree on the packing
classification, flow counts, bucket graph, and complete distance profile.
All 720 distance-two orbits lie on support \(\{20,30,53\}\); a separate
Gaussian-elimination checker verifies the complete 8,192-candidate
odd-marked-component obstruction and a literal two-switch path to packing.
Its package SHA-256 is
`0a36bd4b1f70cd4288e60a4b677aead723efeef7acc90b5037909d36098b299d`.
The universal higher-support component statement remains open.
The surviving proof obligation is existential on every minimum neutral
component.

The retained distance-two path is now decomposed exactly across its cyclic
three-edge cut.  The cycle space and neutral switch graph are fibre
products over matching even boundary words, not Cartesian products of
pole state graphs.  A one-zero-cut packing lemma proves that the global
support packs exactly when both capped supports pack.  The first switch
changes both capped flows without repairing either support, while the
second boundary-compatible switch repairs both at once.  The complete
human proof and independent finite checker are in
`docs/three-sum-neutral-decomposition.md` and
`search/three-sum-neutral-decomposition-20260725/`; the package manifest is
`024a703ed8d32dc882fa9396074465c45eccbce5b71aa65ae89e187009652bf1`.

A separate coordinate-factor lemma now gives the sound numerical
minimum-counterexample restriction
\[
 \omega_{\rm w}(G)\le2r_f(G),\qquad r_f(G)\ge4
\]
for a smallest five-CDC counterexample, where the second inequality uses
Huck's published strict weak-oddness bound.  Every odd coordinate-factor
component must contain a zero-edge endpoint, which is the complete human
proof of the first inequality.  Independent Python and JavaScript checks
give retained profiles \((4,4,6)\), \((4,6,8)\), and \((6,8,8)\) on
\(H_3,H_4,H_5\).  The extremal size-four case must instead have profile
\((8,8,8)\).  Common-colour mark precolouring and suppression lifting
give eight vertex-disjoint odd ambient circuits; girth at least ten
therefore gives order at least 88.  Thus a smallest counterexample has
\(r_M\ge5\), or is in that size-four/order-at-least-88 branch.  The
human proof and clean-room audit are in
`docs/kempe-transversality-and-eight-mark-girth.md` and
`docs/audit-eight-mark-girth-bound.md`.  The package manifest for the
earlier coordinate audit is
`8d77ffe71b6b3cc3f05f95edff8501f8ed1a39e75f8edf6366d1ce7ad785ba31`.
At the first surviving resistance level, the completed \(H_4\) census
contains 4,931,430 distinct minimum size-four supports and no nonpacking
row.  Its blocking CNF is UNSAT with an LRAT accepted by two proof
checkers; this remains a finite theorem about one frozen graph.

## 9. Orientable secondary branch

Orientability is not present in any primary search artifact.  Its separate
encoding uses signed variables \(p_{e,i},n_{e,i}\), requires exactly one
occurrence in each direction in distinct slots, and imposes integer flow
conservation.  Loops use distinguishable darts.

Reducing signs modulo two yields the standard pair-label formulation, so
orientable implies standard.  The converse is not assumed.  No orientable
result was used to classify a standard instance.  See
`docs/orientable-encoding.md`.

## 10. Acceptance-gate verdict and reproduction

| Gate | Verdict |
|---|---|
| Statement and exact negation frozen | PASS |
| SAT/XOR equivalence, loops, parallel edges | PASS within fixed-graph scope |
| Two independent encodings and semantic checkers | PASS |
| Native XOR and certificate-producing CNF | PASS |
| Independent LRAT checking | PASS on non-target controls and connected-kernel separator |
| Canonical and structured search artifacts | PASS within recorded domains |
| Blind adversarial audit | PASS, zero failures |
| Lean semantic formalization | PASS within documented scope |
| Qualifying target counterexample | **ABSENT** |
| Universal proof | **ABSENT** |
| Resolution | **NOT ACHIEVED** |

Run the non-destructive master verification:

```sh
sh tools/verify_all.sh
```

It checks pinned versions and commits, frozen sources, unit suites, retained
manifests, derived counts, fresh cross-verifier models, retained LRAT
certificate files checked by two external proof checkers each, the blind
audit, the proof-agent finite checks, and the Lean build.  Exact hashes,
environment requirements, and reconstruction commands are in
`REPRODUCING.md`.

The next mathematically meaningful branch is not a larger raw low-order
census.  Both the connected-kernel normal form and the unrestricted
fixed-join preparation lemma have now been separated from the target
exactly.  The surviving universal proof branch is a minimum
exact-zero-matching exchange theorem that packs the required two
\(T\)-joins, possibly using the cyclically 4-edge-connected,
girth-at-least-10 minimum-counterexample hypotheses essentially.  Any
target-standard UNSAT candidate still requires the full
independent-certificate gate.
