# Current-status audit

Search date: **2026-07-26**.

## Classification

**PARTIAL STRUCTURAL PROGRESS.**

The five-cycle double cover conjecture remains open.  In July 2026 the
ordinary cycle double cover conjecture was announced as proved; the proof
yields an 8-cycle double cover for every bridgeless graph.  Sang-il Oum's
exposition dated 2026-07-24 states the five-coordinate strengthening
separately as Conjecture 18.

Primary/current sources:

- OpenAI, *A Proof of the Cycle Double Cover Conjecture* (2026):
  <https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf>
- S.-i. Oum, *A proof of the cycle double cover conjecture by OpenAI: An
  exposition*, arXiv:2607.16356v2 (2026):
  <https://arxiv.org/abs/2607.16356>
- J. Geelen, *OpenAI's proof of the Cycle Double Cover Theorem*,
  arXiv:2607.15399 (2026): <https://arxiv.org/abs/2607.15399>
- S. Liu, R.-X. Hao, R. Luo, and C.-Q. Zhang, *Five-cycle double cover and
  shortest cycle cover*, J. Graph Theory 108 (2025), 39–49,
  DOI 10.1002/jgt.23164.
- E. Máčajová, G. Mazzuoccolo, and G. Tabarelli, *Cycle separating cuts in
  possible counterexamples to the cycle double cover and the
  Berge--Fulkerson conjectures*, Ars Math. Contemp. 26 (2026), #P2.03,
  DOI 10.26493/1855-3974.3409.c13.  Its Definition 3.1 is the same
  two-subset edge-label encoding under the name `CDC-coloring`, and Remark
  3.2 explicitly carries its boundary-cut analysis to the five-color
  setting.

These very recent proof/exposition sources are not yet a substitute for
journal refereeing.  They are, however, direct and current sources for the
new 8-CDC theorem and for the fact that the 5-CDC remains posed as a
conjecture.

## Standard convention

Oum defines a \(k\)-CDC as a collection of **at most \(k\) Eulerian
subgraphs**, every edge lying in exactly two.  Zhang's monograph defines a
\(k\)-even-subgraph double cover by \(|\mathcal F|\leq k\), explicitly allows
loops and parallel edges, and explicitly uses an empty even subgraph to pass
from three to four coordinates.

Sources:

- Oum, §9.1, Definition preceding Theorem 16 and Conjecture 18:
  <https://arxiv.org/pdf/2607.16356>
- C.-Q. Zhang, *Circuit Double Cover of Graphs*, Cambridge UP (2012),
  Definitions 1.0.1, 1.0.2, 1.3.1 and Theorem 1.3.2:
  <https://assets.cambridge.org/97805212/82352/excerpt/9780521282352_excerpt.pdf>
- C.-Q. Zhang, *Cycle Double Covers and Long Circuits of Graphs*, Discrete
  Math. 154 (1996), 245–253:
  <https://math.wvu.edu/~cqzhang/Publication-files/my-paper/DM-1996-5CDC.pdf>

Consequently the project's five indexed coordinates, padded by empty
Eulerian subgraphs, faithfully represent the standard “at most five”
formulation.

## Sound reductions and known frontier

The literature supports reduction from general finite bridgeless multigraphs
to cubic graphs while preserving the number of even-subgraph coordinates.
A 3-edge-colourable cubic graph has a 3-CDC, so a cubic counterexample must be
non-3-edge-colourable.  A minimum counterexample can be taken to be a snark
under the nontrivial definition (simple, cubic, cyclically 4-edge-connected,
and not 3-edge-colourable), and known reductions give girth at least 10 and
oddness at least 6.

No source in this audit justifies restricting a minimum 5-CDC counterexample
to cyclic connectivity 5 or 6.  Such stronger reductions from neighbouring
flow or matching conjectures must not be imported.

Relevant sources:

- G. Brinkmann, J. Goedgebeur, J. Hägglund, and K. Markström, *Generation and
  Properties of Snarks*, JCTB 103 (2013), 468–488,
  DOI 10.1016/j.jctb.2013.05.001:
  <https://arxiv.org/abs/1206.6690>
- A. Huck, *Reducible configurations for the cycle double cover conjecture*,
  Discrete Appl. Math. 99 (2000), 71–90,
  DOI 10.1016/S0166-218X(99)00126-2.
- A. Huck, *On cycle-double covers of graphs with small oddness*, Discrete
  Math. 229 (2001), 125–165,
  DOI 10.1016/S0012-365X(00)00205-3.

Brinkmann et al. exhaustively generated all snarks through 36 vertices and
reported that every one has an **orientable** 5-CDC, hence also a standard
5-CDC.  That published computation is not accompanied here by modern
per-instance certificates.  Complete proper-snark lists through 38 vertices
were announced in 2026, but this audit found no corresponding 5-CDC test:

- G. Brinkmann and M. Van Overberghe, arXiv:2603.17789 (2026):
  <https://arxiv.org/abs/2603.17789>

Order 38 is the immediate frontier for reproducing the published
small-order snark census, subject to obtaining and independently validating
the complete graph list.  It is not the most relevant domain for a *minimum*
standard counterexample: the sourced girth-at-least-10 and
oddness-at-least-6 reductions should be applied before spending effort on a
raw all-snarks census.

The project now has a smaller but fully certificate-carrying finite theorem.
The complete canonical order-22 stream contains 7,319,447 connected simple
cubic classes: 7,187,627 are bridgeless, 7,174,735 of those are
three-edge-colourable, and 12,892 are hard.  Exact two-/three-cut and girth
filtering leaves 20 cyclically 4-edge-connected girth-at-least-five hard
rows.  Together with three strict rows through order 18 and six at order 20,
all 29 have standard five-coordinate witnesses checked directly against the
graph semantics and against both complete CNF encodings.  A clean-room audit
regenerated every lower even order, matched all 12,892 order-22 hard rows,
checked all 435 symmetry units, and replayed all 29 models clause by clause.
Consequently:

> Every finite bridgeless cubic multigraph whose connected components have
> at most 22 vertices has a standard five-cycle double cover.

The multigraph conclusion uses the audited minimum-order loop, parallel-edge,
cut, triangle, and square reductions, and combines disconnected components
coordinatewise.  It does **not** apply to arbitrary noncubic graphs with at
most 22 vertices: the cubic-expansion reduction can increase order.  It is
also neither universal nor orientable.

The project has now entered that restricted domain at one explicit point.
The deterministic graph retained under
`search/candidate_domain/runs/domain-20260725-v1/` has 30,450 vertices,
girth exactly 10, and certified oddness at least 8.  Its standard
five-cycle-double-cover formula is SAT, with a compositional witness accepted
by an independent checker and a blind raw-artifact audit.  This is a
**verified positive finite case**, not an enumeration of the restricted
domain and not evidence that the conjecture is universally true.

A current high-flow-resistance construction has also been reconstructed and
checked directly.  The figure-derived Mattiolo--Negrini--Pagani \(H_2\) has
82 vertices, 123 edges, girth five, and no cyclic cut of size at most four.
An independently checked LRAT for the at-most-one-zero
\(\mathbb F_2^2\)-flow formula, together with an explicit two-zero flow,
proves flow resistance two.  Its exact zero pair is not an obstruction: a
23-edge binary cycle through the pair has connected 100-edge complement.
The full standard five-cover formula is SAT with coordinate sizes
\(47,62,39,44,54\), and both project verifiers accept the witness.  The
arXiv source contains vector figures but no author graph file, so this is an
exact labelled-figure reconstruction rather than an isomorphism comparison
against machine-readable author data.  It is another **verified positive
finite case**, not a family theorem.

Separately, every one of the 44,327 connected simple bridgeless cubic
isomorphism classes through order 18 satisfies the stronger
connected-kernel-flow sufficient condition.  The same condition was then
verified with explicit lifts on 1,082 unique downloaded hard-snark records
drawn from the retained cyclic-connectivity-five, girth-six,
circular-flow-number-five, and oddness-four lists through orders 30, 40, 36,
and 44 respectively.  A second portfolio checked all 7,984 records in the
retained House of Graphs strong-snark, girth-at-least-five lists through
order 40; all also have explicit connected-kernel lifts.  “Strong” and the
advertised girth are source-list provenance in this second computation,
while simplicity, cubicity, connectivity, bridgelessness, and every retained
flow and five-cover are checked directly.

The fixed-join preparation problem now also has an exact cycle-code
characterization.  If \(H\) is the high-coordinate cycle and
\(J=E-H\), normalize the outside switch value to \(4\).  Then \(J\) is
preparable precisely when there are binary cycles \(p,q,C\) such that
\(J\cup C\subseteq p\cup q\) and
\(\kappa(J\mathbin\triangle C)<\kappa(J)\).  Equivalently, for a common-zero
set \(T=E-(p\cup q)\subseteq H\), some cycle \(H'\supseteq T\) has
\(\kappa(E-H')<\kappa(J)\).  Canonical exact tests found no preparation trap
through order 18; an independently written implementation replayed the
order-14 and order-16 cases.  These remain exact finite positive results,
but the later 38-vertex two-pole construction below proves that they do not
extend to an unrestricted universal lemma.

The direct necessary-condition screen has also reached all 7,654 retained
order-40 rows.  It enumerates 6,053,028 minimal exact zero supports,
classifies 6,009,319 as \(\mu=1\) and 43,709 as non-\(\mu=1\), and exhausts
the \(2^{21}\) binary cycles of every graph.  No cycle contains a
non-\(\mu=1\) minimal support while avoiding all \(\mu=1\) supports, so
there are zero preparation-trap candidates on this frozen source.  This
condition is necessary because any trap high contains a minimal exact
support, and any contained \(\mu=1\) support would strictly prepare its
disconnected complement.  If a candidate with a two-component complement
had occurred, it would already be a trap: every contained minimal support
would satisfy \(2\leq\mu\leq2\).

The independent replay now covers all 60 batches and all 7,654 graphs.
It directly flow-checks all 6,053,028 supports, classifies
16,051,601,408 binary cycles, and internally checks 7,654 support-
completeness UNSAT proofs plus 7,654 candidate CNFs.  Its totals and zero
candidates match the primary run exactly.  The independent ledger SHA-256
is
`fb9ebf90f57453efff948dd6d9cbc05c76bb086cdedc42e2396adaf94761c457`.
This complete finite replay excludes preparation traps only on the retained
order-40 source and does not establish five-CDC.

The corresponding complete small-boundary census covers the 212 hard
non-three-edge-colourable bases through order 18.  It finds 3,336 relevant
minimal supports with \(\mu\)-profile \(1:3272,\ 2:63,\ 3:1\).  Every one
of the 29,312 highs containing a non-\(\mu=1\) support also contains a
\(\mu=1\) support, leaving zero candidates and traps.  A producer-free
audit independently parses and checks all bases, confirms that none is
three-edge-colourable, exhausts 194,859,008 ordered cycle pairs, and
reconstructs every support and high classification.  This PASS result
remains bounded finite evidence, not a universal theorem or five-CDC.

The complete canonical order-20 census is now independently verified as
well.  Among 510,489 connected simple cubic classes, 497,818 are
bridgeless, 496,430 of those are 3-edge-colourable, and 1,388 are hard.
The hard rows have 21,686 minimal exact supports, split as
\(\mu=1:21,219,\ \mu=2:455,\ \mu=3:8\), with four irrelevant supports.
All 425,024 highs containing a non-\(\mu=1\) support also contain a
\(\mu=1\) support, so the necessary-candidate and trap counts are zero.
The minimum finite domination margin is three, on 2,240 highs across 20
graphs.  A clean-room C++20 replay decoded every graph and literally
traversed 5,821,693,952 ordered cycle pairs, matching every aggregate and
all 1,388 semantic rows.  It independently found exactly six cyclically
4-edge-connected hard rows; all 170 of their supports have \(\mu=1\).
This exact extension through order 20 remains a finite preparation result,
not a five-CDC theorem.

The preparation minimum also has an exact connected-odd-factor meaning:
\(\mu_G(T)\) is the minimum component count of a spanning odd factor of
\(G-T\).  A relevant minimal \(T\) is equivalently a matching whose deletion
and degree-two suppression restores Tait colorability, subject to an exact
component-parity relevance test.  Its odd factors admit a separate exact
attachment-parity formulation.  Cyclic 4-edge-connectivity does not force
\(\mu_G(T)=1\).

The singleton case is nevertheless universal on the relevant strict
domain.  Tutte's peripheral-cycle theorem implies that every edge \(e\) of
a finite simple 3-connected cubic graph lies in a binary cycle whose edge
complement is connected, so \(\mu_G(\{e\})=1\).  An independent
standard-library audit found such a witness for all 29,037 edges of 985
simple 3-connected hard graphs through order 20.  It also reconstructed
the order-18 singleton \(\mu=2\) control and exhibited both a 2-vertex cut
and a cyclic 2-edge cut, placing it outside the theorem.  Thus every
higher-\(\mu\) support in the minimum-counterexample domain has size at
least two.

The exact-pair case now has a complete marked-core reduction, but not a
universal positive theorem.  An exact two-edge zero set is a nonadjacent
matching; deleting it and suppressing its four degree-two ends gives a
loopless Tait-colourable cubic core.  In girth at least five the endpoint
geometry is either four once-subdivided marked core edges, or two such
edges plus one twice-subdivided edge.  In the latter case connectivity
forces both outer halves of the twice-subdivided path.  In both cases
\(\mu_G(T)=1\) is equivalent to an explicit connected spanning subgraph of
the core satisfying one parity equation for every marked component.

A clean-room audit checked all 1,439 exact pairs in the 27 canonical
simple cubic graphs through order 10.  It found precisely the three
excluded \(K_4\) suppression degeneracies, checked 530 independent-end
cases and all 60 girth-five single-cross cases, and compared 19,624
fixed-subgraph orientation/parity instances with zero discrepancies.  All
480 middle-edge-only odd factors in the single-cross controls were
disconnected, as the proof requires.  This exact reduction converts the
pair branch to a smaller marked Tait-core search; it does not show that
every marked instance has the required connected subgraph.

A targeted search has now exercised that smaller representation beyond the
canonical order-22 boundary.  Among 15,000 deterministic marked sets on
order-24 Tait-colourable cores, 276 had no connected odd factor; all 828
reconstructed pairings were nevertheless explicitly Tait-colourable and
therefore did not yield exact *minimal* pairs in a snark.  The one-cross
sample had 15 failures among 2,000 marked triples, but again all 30
reconstructions were Tait-colourable.  Every one of these 858 reconstructions
has girth three or four.  Conversely, complete exact-flow audits of the
Flower snarks \(J_5,J_7,J_9\) checked 2,475 exact minimal pairs and found
\(\mu=1\) for every one.  An independent checker re-enumerated all affine
odd-factor spaces and validated every reconstruction, flow, colouring, and
cut classification.  This is structured finite support for a possible
pair-specific reducibility theorem, not a proof of one.

The unqualified pair-specific statement is false, even at high cyclic
connectivity, because “exact” does not mean inclusion-minimal on a
three-edge-colourable graph.  In \(K_4\), the two opposite zero edges of
the flow \((0,1,1,1,1,0)\) have \(\mu=2\).  More substantively, the
dodecahedral graph is simple, cubic, girth five, and cyclically
5-edge-connected, yet it has an exact two-edge zero flow whose 512
containing binary cycles all have disconnected complements
(\(\mu=2\)).  It is Tait-colourable, so the empty exact zero set is a
proper subset of the pair.  Thus a viable universal pair lemma must assume
that the graph is non-Tait, or equivalently in this setting that the pair
is inclusion-minimal.

The corrected statement has been screened on all 7,654 retained order-40
strong snarks.  Of 13,547,580 edge pairs, 517 have no
connected-complement containing cycle; direct \(\mathbb F_2^2\)-flow
tests reject every one of those 517 as an exact zero pair.  Hence all exact
pairs in this complete retained corpus have \(\mu=1\).  Catlin's
collapsibility theorem does not promote this finite result to a proof:
contracting a suitable perfect matching gives an ordinary
4-edge-connected quotient and the desired aggregate parities, but splitting
its vertices back into two marked ports can disconnect the lifted factor.
This transition-connectivity condition is the precise remaining gap.  The
literal counterexamples, replay checkers, complete order-40 screen, and
source notes are frozen under
`search/exact-pair-theory-resolution-20260725/`.

A standard five-cover also forces a new simultaneous packing condition.
For every one of the ten pair labels \(a\), quotienting \(E_5\) by the
two-dimensional subspace that meets \(D_5\) only in \(a\) produces an
\(\mathbb F_2^2\)-flow whose exact zero set is precisely the \(a\)-label
class.  If the graph has no nowhere-zero \(\mathbb F_2^2\)-flow, all ten
classes are nonempty and contain ten pairwise edge-disjoint globally
minimal exact supports.  Thus the minimal-support hypergraph must have
matching number at least ten.  Matching number at most nine would be a
sound target-standard obstruction.  The theorem includes loops by
edge-end incidence and isolates the Tait/empty-support exception; exact
checks on Petersen, \(R_2\), and \(R_4\) pass.  Its scalar consequence
\(10r_f\leq |E|\) is not new and is weaker than the known cubic
\(r_f\leq\gamma_2\leq |E|/15\) bound; the useful information is the
ten-support packing.  The frozen package is
`search/five-cdc-label-packing-20260725/`.

Complete minimal-support audits on the retained order-34, order-36, and
order-38 strong snarks found respectively 7, 29, and 597 relevant minimal
zero sets with \(\mu>1\). The order-38 exceptions occur on 119 of 298
graphs and reach \(\mu=3\). On the 40-vertex \(R_2\) graph, an exact
Petersen-pole factorization found 33,517 minimal supports; 9,516 relevant
supports have \(\mu>1\), including 48 with \(\mu=4\). Nevertheless, all
328,184,467 realizable disconnected joins across these four audits are
preparable; every trap count is zero. The order-34 and order-36 support
families passed independently encoded completeness audits, while the
\(R_2\) family has a direct product proof and its full
\(2^{21}\)-cycle classification is
independently audited.  These computations refute an overstrong pointwise
shortcut; the later 38-vertex two-pole graph also refutes the unrestricted
high-specific universal lemma.
The independent order-38 audit also validates all retained flow and
\(\mu\) witnesses, uses separate two-bit blocking formulas with internally
checked temporary proofs, and exhaustively reclassifies all 312,475,648
high cycles. Its proof bytes are not retained, so the result remains
rerunnable solver-assisted finite evidence.

A separate clean-room margin audit has now reconstructed every affected
high on the retained order-34, order-36, and order-38 sources.  Its
Walsh--Hadamard implementation imports no project cycle-space or margin
code and checks 131,596,288 highs on all 134 affected graphs.  The minimum
number of contained \(\mu=1\) supports is respectively 21, 22, and 20; the
minima occur on 1, 16, and 3 highs, and the necessary-candidate count is
zero at every order.  The reconstruction matches every complete histogram
and all 254,391 retained flow witnesses.  The frozen primary reports name
an unretained temporary helper binary; portable source rebuilds match after
removing only that non-replayable path/hash provenance.  This disclosure
does not affect the independently reconstructed finite profiles.

The independent \(R_2\) audit additionally found that every cycle containing
any relevant support already contains one with \(\mu=1\).  This domination
now has a compact \(R_2\)-specific proof: nonempty base and pole blocks
supply an all-far support, and seven local Petersen odd-factor rows glue to
a connected odd factor avoiding it.  The Boolean block count reproduces the
1,970,577/126,575 cycle split without a global scan.  A separate
standard-library blind checker reconstructed all compatible block tuples
and all 12,000 glued factors with zero discrepancy.  A generic
incremental SAT enumeration returned the same 33,517-support family and
directly checked flow witnesses, providing a third representation of the
finite result.

The rooted premise used by the Petersen-2-pole substitution theorem was
also tested for necessity through order 18. Across all 44,327 connected
simple bridgeless cubic bases and 1,181,250 singleton edge roots, no graph
had unrooted preparation while failing rooted preparation. Complete
cycle-code evaluation on the 212 non-3-edge-colourable bases checked
194,859,008 ordered flow pairs and 5,216,238 realizable-high/root
obligations. An independent checker regenerated the canonical graph6
streams, reclassified all hard graphs by a different colouring search, and
recomputed every semantic profile with zero discrepancy. This bounded
result does not make the rooted hypothesis redundant in general. It also
has no five-CDC conclusion, and no failure-driven substitution was
performed because the census found no eligible base edge.

That bounded singleton result cannot be promoted to arbitrary root sets.
An exact census tests all 71,313 edge pairs on the 212 hard bases and
67,244,094 realizable-high/pair obligations. Nine pairs fail on two
order-18 graphs, with 144 failed obligations across 128 highs; all pairs
below order 18 pass. A producer-free checker independently rebuilds all 212
cycle codes, exact-support families, connected odd factors, and pair-root
obligations and matches the census exactly. On the first simple bridgeless
cubic 18-vertex graph
`Q????B?K?WWCg_?sIG?s?HO?KG?`, all 27,216 singleton-root obligations pass,
but one high fails for the root pair \(\{9,19\}\). Complete independent
enumeration derives exactly five minimal supports inside that high and 13
connected odd factors avoiding at least one of them; none contains both
roots, and every support has pair-rooted minimum two. Thus the multi-root
premise in the conditional Petersen substitution theorem is genuinely
stronger than the singleton property. The conditional theorem itself
remains valid, and this preparation obstruction is not standard five-CDC
UNSAT.

The adaptive sequential boundary is now exact. For one substitution
\(G=B[P_2/s]\), a fixed surviving edge \(e'\) is a valid next root exactly
under the downstairs pair-root property \(\mathsf{RP}(B;\{s,e\})\), while
either terminal and every internal pole edge require only
\(\mathsf{RP}(B;\{s\})\). Hence a nested construction may continue inside
the newest pole without accumulating a root stack; a surviving or branching
next edge still needs joint containment. A producer-free audit exhaustively
enumerates the cut-pole states and fragments, checks all 882 internal-root
obligations, and reconstructs the 28-vertex boundary graph obtained by
substituting edge 9 in the first pair-root witness. All 150 connected odd
factors containing surviving root 19 project correctly, and none yields an
eligible pair-root factor downstairs. This sharpens the rooted transfer
theorem only; it is not universal unrooted closure or five-CDC UNSAT.

The nested newest-pole rule therefore yields an explicit infinite family:
after \(m\) substitutions the graph has \(|V(B)|+10m\) vertices and
\(|E(B)|+15m\) edges, has root-free preparation, and is separately rooted
at all 16 internal/terminal continuation edges of the newest pole. A
clean-room audit constructs every continuation and an exactly reversible
depth-three positive control. Its independent finite census also checks all
7,984 retained order-34/36/38/40 source identities and premises. Using
cycle-space edge signatures, it exhausts 14,067,888 edge pairs and finds
zero two-edge cuts. Every forward cut Petersen pole would expose its two
terminal edges as a two-edge cut, so none of those retained graphs lies in
this nested reduction family. This is exact zero coverage of the frozen
portfolio only, not universal noncoverage and not a five-CDC statement.

Another tempting eight-to-five shortcut is now closed exactly.  For one
supplied cubic CDC, partitioning and recoloring its circuit components is
equivalent to coloring their conflict graph.  A connected bridgeless
112-vertex supplied 8-CDC was constructed whose eight coordinate supports
are single circuits and whose component-conflict graph is \(K_8\).
Therefore this cover cannot be reduced even to seven coordinates by that
operation.  This is a no-go theorem for postprocessing one supplied cover,
not a graph without some other 5-CDC.  Indeed, an independent audit found a
proper three-edge-coloring of this particular graph, whose three
complementary two-factors give a standard 3-CDC.

Arbitrary affine relabelling before quotient lifting does not rescue that
same supplied coordinate-tree cover.  Mapping the eight old coordinates
bijectively to \(\mathbb F_2^3\), taking pair differences, choosing any
Fano line, and solving the binary lift leaves only 30 affine structures
modulo translation and \(GL(3,2)\).  All \(30\cdot7=210\) cases are
inconsistent, with at least two bad line-subgraph components.  Direct
Gaussian elimination independently agrees with the quotient component
criterion; a companion supplied cover has one good structure and three good
lines.  This closes only relabel-then-lift postprocessing of the retained
8-cover, not another cover or the graph's target formula.

Allowing another potential-compatible 8-cover for the same fixed flow does
rescue that old 112-vertex example: 380 of the 420 three-pair coordinate
merges are feasible for some compatible cover.  Thus its frozen supplied
\(K_8\) conflict graph was genuinely a supplied-cover obstruction.

The broader fixed-flow pure-merge assertion is nevertheless false.  On the
12-vertex bipartite cubic graph `K??FEaKR@oE_`, one nowhere-zero
\(\mathbb F_2^3\)-flow has a unique compatible potential modulo translation,
and its coordinate co-occurrence graph is exactly \(K_6\) on six
coordinates.  Even deleting one flow-2 port leaves a rank-36 potential
system whose two dangling labels complete the same \(K_6\).  Hence no
compatible cover for that fixed flow purely merges to five coordinates.

Three copies of this rigid cap, inserted at the noncyclable same-flow edge
set \(\{02,56,17\}\) of the Tait base `It?GYDKKO`, give a 46-vertex
connected countermodel to one-circuit repair.  Every connected circuit
misses one cap and its two connectors; that unchanged cap still forces
\(K_6\) after the switch.  The theorem has a SAT-free hand proof and an
independent checker in
`search/fano-pure-merge-one-switch-countermodel-46v-20260726/`.  The
checker also enumerates all 128 compatible potentials of the starting
flow.  This closes unrestricted “pure merge plus one connected-circuit
switch,” not five-CDC: the graph has the explicit cover
\(46,46,46,0,0\), and its two-edge cuts leave the cyclically
4-edge-connected restriction open.  A seeded nonexhaustive probe of all
20 retained strict order-22 and 38 retained strict order-24 snarks samples
78,000 nowhere-zero flows; all 16,411 pure-merge-bad samples have a
connected-circuit repair.  This is evidence for the reduced restriction,
not a proof.

The connected-kernel condition has also been scoped exactly.  Quotienting a
\(D_5\)-flow by the weight-four vector omitting coordinate \(i\) sends
precisely the labels outside \(C_i\) to the distinguished Fano line.
Consequently a connected-kernel flow exists if and only if some 5-CDC has a
connected coordinate complement \(E-C_i\).  This is a precise strengthening
of five-CDC, not merely an unrelated sufficient condition.  It is now
proved to be a **strict** strengthening.  Replace every cotree edge of a
non-Tait cubic graph \(B\) by a diamond \(K_4-e\).  Connectedness of a
hypothetical line-valued kernel forces both attachment values of every
diamond into the line.  Contracting the diamonds and projecting modulo the
line leaves an even edge-subset contained in the spanning tree, hence no
outside-line value at all; this would 3-edge-colour \(B\).  Conversely, a
literal three-duad local rule lifts any standard five-cover of \(B\) through
every diamond.

For Petersen this gives a 34-vertex, 51-edge simple bridgeless cubic graph
whose connected-kernel relaxation is UNSAT while its target-standard
five-cover is SAT with coordinate sizes \(30,30,17,16,9\).  The 153-variable,
465-clause CNF has a 20,031-byte LRAT accepted by both retained checkers;
independent Python and JavaScript programs reconstruct the graph, formula,
and positive cover.  Iteration gives an infinite separation family of
orders \(10,34,106,322,\ldots\).  This closes the connected-kernel universal
route without producing a five-CDC counterexample.  The certificate package
is `search/connected-kernel-cotree-diamond-separator-20260725/`.

The unrestricted fixed-join preparation route is also now closed as false.
The explicit 38-vertex simple bridgeless cubic graph in
`search/fixed-join-preparation-trap-20260725/` has a binary cycle \(H\)
with \(\kappa(E-H)=2\) and exactly 125 contained inclusion-minimal exact
\(\mathbb F_2^2\)-flow zero sets, every one satisfying \(\mu_G(T)=2\).
The human proof projects any hypothetical connected spanning odd factor
through two Petersen 2-poles to one of 25 exhaustively listed base factors.
Independent Python and JavaScript implementations agree, the latter
scanning all \(2^{20}\) expanded cycles.  A standard five-cover of sizes
\(27,27,21,19,20\) is checked by both target verifiers.  The graph has two
nontrivial two-edge cuts, so this refutes only the unrestricted preparation
lemma; it neither refutes five-CDC nor a preparation theorem confined to a
cyclically 4-edge-connected minimum-counterexample domain.

Strict one-step descent in the minimum-support route is now also known to
be false.  The package
`search/minimum-switch-local-plateau-20260725/` freezes a 16-vertex simple
bridgeless cubic graph and an exact-zero matching \(M=\{2,13\}\) of size
two.  Direct enumeration of all 128 affine \(T\)-joins finds no disjoint
pair.  Across all 512 binary cycles and all three nonzero switch values,
every matching-preserving switched support has size at least two.  The
complete profiles are retained and independently reconstructed.

The obstruction is local rather than global.  A neutral switch changes
\(\{2,13\}\) to \(\{2,12\}\), and a second switch reaches the globally
minimum support \(\{2\}\), which has an explicit two-\(T\)-join packing
cycle.  Thus the checked trajectory is \(2\to2\to1\).  The exact primary
census has no switch-local nonpacking flow through orders 10, 12, and 14;
at order 16 it finds 64 such flow signatures on six hard graphs, but no
nonpacking globally minimum support.  On each of those six graphs the
complete matching-support-\(\le2\) flow graph is connected to a size-one
state.  The surviving exchange question must therefore allow neutral
reconfiguration, and the cardinal-minimum support conjecture is unaffected.

The complete finite reconfiguration assertion is frozen separately in
`search/minimum-switch-neutral-components-n16-20260725/`.  Across the six
order-16 hosts it contains 33,546 ordered flows with matching exact-zero
support of size one or two.  Independent Python and JavaScript state-graph
constructions find that every state is reachable from the size-one set
inside this sublevel graph.  All 384 strict local plateaus are at distance
two.  Reversing a shortest path gives neutral size-two switches followed
by one descent.  This is an exact finite theorem, not a universal exchange
proof.

The same statement now has a complete hard order-18 census.  In
`search/minimum-switch-neutral-components-n18-20260725/`, independent C++
and NumPy implementations enumerate 1,680,414 ordered support-one-or-two
states on all 179 canonical hard graphs.  Fifty-six graphs contain 7,704
strict local nonpacking plateaus.  Every state is reachable from the
size-one set inside the sublevel graph, and every plateau has distance
exactly two.

The underlying bucket lemma is elementary: a value-1, value-2, or value-3
switch preserves \(q\), \(p\), or \(p+q\), respectively, and the converse
holds because the difference of two binary flows is a binary cycle.  This
makes the exhaustive adjacency calculation transparent.  The result still
does not address a graph whose globally minimum support has size three or
more.

The same exact analysis is now complete at order 20 in
`search/minimum-switch-neutral-components-n20-20260725/`.  Independent C++
and NumPy implementations agree on all 1,388 hard graphs and 20,161,044
ordered support-one-or-two states.  There are 118,134 strict local
nonpacking plateaus on 589 graphs, each at distance exactly two.  The only
21,492 states not connected to size one are all states on the unique
minimum-size-two graph, and every one already packs.  Consequently every
nonpacking state reaches size one on this complete finite boundary.

The order-22 minimum-size-two boundary changes the correct quantifier.
`search/minimum-switch-packing-components-n22-20260725/` exhausts all
190,512 ordered minimum states on the seven hard graphs with no size-one
support.  Fifteen of the 1,441 distinct minimum supports do not pack,
refuting the claim that every minimum support extends.  All 2,808
nonpacking realizations are nevertheless one neutral switch from packing.
The viable statement is therefore about the existence of a packing state
in each minimum neutral component.

The minimum-size-three package
`search/minimum-size-three-packing-components-20260725/` completely
classifies the 42-vertex global component-parity countermodel.  Its 366
minimum supports split into 290 packing and 76 nonpacking supports.
Across 611,712 global-colour flow orbits, every nonpacking orbit reaches
packing; 170,352 have distance one and 720 have distance two.  Hence even
the one-switch component statement is false, but no packing-free minimum
component occurs in this complete graph-level census.  The Python and C++
implementations are independently written and agree on all retained
fields.  All 720 distance-two orbits occur on support
\(\{20,30,53\}\).  A separate Gaussian-elimination checker verifies its
8,192-candidate odd-marked-component obstruction and a literal two-switch
path to packing.

For the
40-vertex \(R_2\) graph, an independent blind audit checked the retained
connected-kernel lift and separately confirmed girth five and exact oddness
six by enumerating all 192 perfect matchings.

These finite censuses and the single restricted-domain specimen do not
change the current literature classification: no target-standard
counterexample certificate or universal proof is known here.

An exact alternative target formulation is now available for finite
loopless cubic multigraphs.  A graph has a standard 5-CDC exactly when it
has a matching \(M\), two binary cycles with intersection \(M\), and an
\(\mathbb F_2^2\)-flow with exact zero set \(M\).  A separate clean-room
audit checked both constructions, the \(E_4/\langle1111\rangle\) quotient,
empty and nonempty matchings, parallel edges, disconnected controls, every
CNF/XOR constraint, and an explicit reverse lift on \(H_2\).  The retained
\(H_2\) encoding has 615 variables, 2,296 ordinary clauses, and 328 native
XOR rows and is SAT.  This is an exact search formulation, not a
relaxation.

The cycle-intersection part of that theorem reduces further to a component
parity test: for a binary cycle \(H\supseteq M\), a second cycle meeting it
exactly in \(M\) exists precisely when every component of \(E-H\) contains
an even number of \(M\)-endpoints.  Hence the target asks for a spanning
odd factor avoiding an exact-zero matching and pairing those endpoint
demands inside each component.  Connected complement implies this
condition but is not necessary.  On the seven retained order-34 supports
with \(\mu=2\), exact enumeration finds two supports with 416 good cycles
each and five with none; every affected graph nevertheless has a separate
\(\mu=1\) positive support.  This falsifies only the pointwise
every-support strengthening.

Nor can a proof fix an arbitrary high coordinate and recolor only the two
low coordinates.  For the Petersen graph, the spanning two-factor of two
5-cycles cannot occur as a coordinate of any standard five-cover, although
the graph itself has a checked five-cover.  A 690-clause direct
fixed-coordinate CNF and a 295-clause exact matching/four-flow CNF are both
UNSAT; their LRATs are accepted by both project proof checkers.  Independent
enumeration of all 4,096 binary-flow pairs reproduces zero extensions, while
the unrestricted positive model has coordinate sizes \(6,5,5,9,5\).
This restricted-domain obstruction does not challenge the graph-level
conjecture.

The ten pair-label quotients also yield a weaker certificate-oriented
screen: a five-cover on a graph with no nowhere-zero
\(\mathbb F_2^2\)-flow forces ten independent such flows whose nonempty
exact zero sets partition the edges.  The \(H_2\) relaxation has 3,690
variables, 15,918 ordinary clauses, and 1,640 native XOR rows and is SAT,
with zero-class sizes summing to all 123 edges.  UNSAT would be target-sound
after the missing premise and proof certificate are checked; SAT has no
converse meaning.

The recursive high-flow-resistance stress test has been extended three steps.
The figure-derived \(H_3\) has 122 vertices and 183 edges and is simple,
cubic, girth five, and cyclically 5-edge-connected by exhaustive deletion
of all 46,234,462 edge sets of size at most four.  An explicit three-zero
flow and an independently checked LRAT excluding two-zero flows prove
\(r_f(H_3)=3\).  Nevertheless its authoritative direct standard formula is
SAT, with coordinate sizes \(77,74,58,77,80\); both semantic verifiers
accept the models, and the exact matching/four-flow formula independently
reverse-lifts to another five-cover.  A fresh clean-room replay reproduced
the frozen result byte-for-byte.  This is another positive family member,
not evidence that the entire recursive family has five-covers.

The same exact figure-and-label recursion now gives \(H_4\) and \(H_5\), on
162 and 202 vertices respectively.  Both are simple cubic girth-five
graphs.  Certificate-producing cyclic-cut formulas, independently rebuilt
clause-for-clause, prove both cyclically 5-edge-connected.  Explicit flows
and two-checker LRATs prove \(r_f(H_4)=4\) and \(r_f(H_5)=5\).  Both complete
standard five-cover formulas are nevertheless SAT: retained direct cover
sizes are \(130,112,68,72,104\) for \(H_4\) and
\(144,143,95,98,126\) for \(H_5\).  Both semantic verifiers accept both
independent models, and matching/four-flow reverse lifts give separate
cross-checks.  The root replay accepted all four new LRATs with both
`lrat-check` and CakeML `cake_lpr`, and reproduced the \(H_5\) clean-room
result byte-for-byte.

A separate stable-tile certificate now upgrades those finite controls to an
inductive result for the frozen figure reconstruction, denoted
\(\widehat H_n\).  The open 40-vertex, 55-edge \(J\)-tile has the same
\(D_5\) boundary state
\((01,01,02,23,03)\) on input and output.  After one global coordinate
permutation, the complete \(\widehat H_2\) certificate has that state, so a
direct XOR gluing lemma proves a standard five-CDC for every
\(\widehat H_n\), \(n\ge2\), with coordinate sizes
\[
(62,54,39,47,44)+(n-2)(32,24,29,20,15).
\]
The 25-file package, six corruption tests, exact \(\widehat H_2\) through
\(\widehat H_5\) replays, and Lean evaluation are green; the package ledger
SHA-256 is
`e09cee11f74b19e4a08f18c94534207e44f601a29f059a15fb614154900cbfac`.
This is not a universal result and does not address orientability.

The publication novelty is limited.  In the author-defined MNP family, the
published almost-proper edge-coloring has exactly two conflicts, both of
type \((a,c,c)\).  Its \(a\)-edges form a perfect matching whose complement
has exactly two odd circuits.  Huck--Kochol (1995) therefore already
implies a standard five-CDC for every author-defined \(H_n\).  The new
object is the explicit stable \(D_5\) certificate for the frozen
transcription, not the family-wide existence conclusion.  No
author-supplied machine graph is available to certify formal identity
between the two notations.  The novelty-audit ledger SHA-256 is
`3dc1455e0290624e9d6c678b6e5b0ef1115cdc68c1dcdef6d29587a0e2686e81`.

The exact matching/four-flow characterization has also produced a sharper
proof route.  For an exact-zero matching \(M\), put
\(K=G-M\) and \(T=\partial M\).  Two binary cycles intersect exactly in
\(M\) if and only if \(K\) packs two edge-disjoint \(T\)-joins.  The
nowhere-zero \(\mathbb F_2^2\)-flow on \(K\) makes \(K\) bridgeless, while
each terminal has degree two.  A missing hypothesis in the first version
of this route was found by blind audit: \(K\) can have a component with an
odd number of terminals, in which case no \(T\)-join exists and the
minimum \(T\)-cut is zero.  If every component is \(T\)-even, the minimum
\(T\)-cut is two, and the Codato--Conforti--Serafini packing theorem shows
that remaining failure for this fixed \(M\) forces an odd-\(K_{2,3}\)
graft minor.

The correction is frozen as an exact ten-vertex countermodel in
`search/component-parity-tjoin-countermodel-20260725/`.  It is simple,
cubic, connected, and bridgeless; the displayed exact-zero matching leaves
two complement components with three terminals each, so there is no
\(T\)-join and the minimum \(T\)-cut is zero.  The same checker verifies a
Tait colouring and a standard five-cover.  Thus it refutes only the
unqualified intermediate cut claim, not five-CDC.

Contracting every component of \(G-M\) and retaining the matching edges
gives a bridgeless quotient multigraph whose vertex degrees are exactly the
component terminal counts.  Consequently component parity cannot fail for
\(|M|\le2\).  If \(G\) is connected and \(|M|=3\), the only parity-bad
quotient is two vertices joined by three parallel edges.  The frozen
ten-vertex countermodel realizes precisely this first possible quotient
shape, but with a nonminimum matching.

The stronger claim for globally minimum supports is now also known to be
false.  The package
`search/minimum-component-parity-countermodel-20260725/` constructs a
42-vertex simple connected bridgeless cubic graph with a globally minimum
size-three exact-zero matching whose complement has two 21-vertex
components with terminal profile \((3,3)\).  A human capping proof and an
independently reconstructed 314-variable, 960-clause CNF with a
dual-checked LRAT establish the lower bound.  Projected enumeration finds
exactly 366 minimum supports: this is the unique parity-bad support and
the other 365 have connected complements.  One of those alternatives is
reverse-lifted to a checked standard five-cover.  The graph is therefore a
countermodel to “every minimum support is parity-good,” not to the
existential minimum-support route or to five-CDC.  Its nontrivial cyclic
three-edge cut also prevents it from occurring as a reduced minimum
counterexample.

For the reduced minimum-counterexample domain the bound improves.  Every
\(T\)-odd complement component and its complement both contain cycles, so
the number of nonloop quotient edges incident with it is the odd size of a
cyclic edge cut.  (Quotient loops contribute two terminals but no cut
edge.)  The audited cyclically \(4\)-edge-connected reduction excludes cut
size three; hence the first possible parity-bad component has at least five
terminals and \(|M|\ge5\).  Thus every exact-zero matching of size at most
four is automatically componentwise \(T\)-even on a reduced minimum
counterexample.  At \(|M|=5\), parity failure forces exactly two complement
components joined by all five matching edges.

The exact package `search/h5-core-cap-flow-bound-20260725/` probes this
five-boundary regime on a certified large core.  Starting from the
192-vertex Tait core obtained from reconstructed \(H_5\), it exhausts all
\(\binom{10}{5}\) choices of marked paths and all 12 cyclic attachment
orders modulo the dihedral symmetry of a five-cycle.  An independent
checker reconstructs all 3,024 simple cubic bridgeless caps and verifies an
exact-zero matching of size at most two in every case.  This exact finite
result eliminates the first parity-obstruction scale throughout that
corpus; it is not a universal exchange theorem.

A new three-bit-flow formulation now isolates a sharper exchange
obligation.  For a nowhere-zero
\(\mathbb F_2^3\)-flow \(f\), every value class
\(M_k=\{e:f(e)=k\}\) is a matching, and quotienting by
\(\langle k\rangle\) makes it the exact zero set of an
\(\mathbb F_2^2\)-flow.  Thus any value class whose complement packs two
\(T\)-joins yields a standard five-cover.  The claim that every arbitrary
three-bit flow already has such a value is false: the exact order-ten
package `search/fano-value-class-flow-countermodel-20260726/` gives a
nowhere-zero flow for which all seven classes fail, while an independent
subset enumerator and a human forced-cycle table check the seven failures.
The graph is Tait-colourable and has an explicit five-cover, so this is a
route countermodel only.

The formerly surviving **connected-graph** one-switch lemma asserted that
every such bad flow on a connected graph can be repaired by adding a
nonzero value \(a\) on one circuit disjoint from the \(a\)-value class.
The switch preserves nowhere-zeroness and exchanges the other six value
classes in three pairs.  The exact
\(\mathrm{GL}(3,2)\)-quotiented census in
`search/fano-flow-one-switch-frontier-20260726/` finds no switch-local bad
flow among every connected simple bridgeless cubic graph through order 14,
all 26 frozen hard graphs at order 16, and all 179 frozen hard graphs at
order 18.  A separately written C++ enumerator exactly matches the complete
Python order-14 totals and extends the search to all 1,388 frozen hard
graphs at order 20.  That stage exhausts 847,539,220 flow orbits and finds
49,752,091 initially bad flows, every one of which has a one-switch repair.
The full order-20 computation still passes when switches are restricted to
one connected circuit.  In the terminology of the 2025--2026
nowhere-zero-flow reconfiguration literature, the refuted lemma says
that good \(\mathbb F_2^3\)-flows form a dominating set in the flow
reconfiguration graph of every connected bridgeless cubic graph.
The order-18 hard stage contains 21,324,510 flow orbits and
757,221 initially bad flows; all 757,221 have a one-switch repair.
The retained verifier independently reconstructs the first bad-flow repair
on 432 graph rows, but does not re-enumerate the full flow corpus.

For every value class \(M_k\), a linear functional taking \(k\) to one
gives a binary cycle containing \(M_k\).  Removing \(M_k\) from that cycle
gives a \(\partial M_k\)-join in \(G-M_k\).  Thus the component-parity
failure possible for an arbitrary exact-zero matching is impossible here;
every nonpacking value class must lie in the odd-\(K_{2,3}\) graft-minor
branch of the packing theorem.

The universal connected lemma is now refuted by
`search/connected-one-switch-countermodel-40v-20260726/`.  Its explicit
simple connected bridgeless cubic graph has 40 vertices and 60 edges.  In
the ten-vertex Tait base `It?GYDKKO`, the three monochromatic edges
\(\{02,56,17\}\) lie on no common circuit by a short forced-triangle
argument.  Replacing them with three attached ten-vertex bad blocks
ensures that every connected circuit leaves one block untouched.  A human
two-sum projection proof shows that the original flow and every
one-circuit neighbor remain bad.  The independent checker reconstructs
the graph, verifies bridgelessness and all flow equations, enumerates all
30 base circuits and all 6,780 final circuits, and accepts an explicit
three-cover with coordinate sizes \(40,40,40,0,0\).  Thus this closes the
domination route, not five-CDC.  The earlier 2,614-vertex \(H_5\)/LRAT
package remains a valid superseded construction.  Multi-switch
reachability or selection of a different initial three-bit flow remain
possible but unproved routes.

A narrower one-switch route survives on the sound minimum-counterexample
domain.  The two- and three-edge-cut gluing reductions make a minimum cubic
counterexample cyclically 4-edge-connected, while the connected composition
countermodel has nontrivial two-edge cuts at its three grafts.  The exact
elementary-circuit
run on all 20 strict order-22 snarks checks 63,251,330 flow orbits, including
279,836 bad flows, and repairs every bad flow in one connected-circuit
switch.  The complete 38-graph strict order-24 extension checks a further
617,079,260 flow orbits and repairs all 5,161,169 bad flows.  Thus the
cyclically 4-edge-connected one-switch lemma remains a sufficient but
unproved replacement, with exact evidence through the retained Snarkhunter
strict-snark order-24 frontier.  Identities and premises are independently
checked, but list completeness is not independently regenerated.

The complete five-pole boundary calculus is also finite.  An ordered
boundary word is a five-edge Eulerian multigraph on the five coordinate
colors.  Hence, up to boundary-position and color permutations, it is one
of four human-classified types: a 5-cycle, or a triangle plus a digon that
coincides with a triangle edge, shares one triangle vertex, or is disjoint.
There are 6,240 ordered words and 62 fixed-position \(S_5\)-orbits.  The
exact \(C_5\)-cap recurrence shows that a fixed cyclic order admits 4,620
words (46 orbits), while all 62 occur over the 12 undirected cyclic orders.
This gives a conditional five-cut reducibility theorem for a minimum
counterexample.  However, explicit disjoint abstract state sets of sizes 8
and 10 meet every cap set and satisfy the elementary bichromatic-switch
closure.  Thus those necessary axioms alone do not force the two shores to
glue; graph-pole realizability is the open issue.  The note and checker are
in `search/five-pole-c5-boundary-calculus-20260725/`.

The first graph-realizability census is consistent with a much stronger
lower bound.  Two independent exact solvers agree through order 11, and a
deterministic extended run covers all 5,214 connected simple internally
bridgeless terminal-distinct cubic five-poles through order 13.  Every pole
admits at least 46 of the 62 boundary orbits.  Exactly 298 attain 46, and
each of their complete relations equals one of the twelve ordered
\(C_5\)-cap relations.  Additional portfolios of 1,080 deterministic
marked-core, three-vertex-path, and 2-lift samples through pole order 25,
498 strict-snark path fragments, and all 37 Petersen five-edge-marking
orbits also have at least 46 states.  These are exhaustive only through
order 13 and in the explicitly named finite families.

The internal-bridge restriction has a short human proof in
`docs/five-pole-realizability-frontier.md`: a bridge splitting off
\(k\le2\) distinct terminals creates a cycle-separating cut of size
\(k+1\le3\), contradicting the reduced cyclically 4-edge-connected
domain.  The universal 46-state lower bound remains unproved.  If true, it
would force two five-pole shore relations to intersect by
\(46+46-62=30\), excluding the corresponding five-cut; it would still not
resolve highly connected graphs.

The adjacent four-pole obstruction from Máčajová--Mazzuoccolo--Tabarelli
has also been tested without being claimed solved.  Every one of the
19,513 internally bridgeless terminal-distinct simple cubic four-poles
through order 14 has exactly nine or ten of the ten \(D_5\) boundary types;
690 deterministic samples through order 24 have the same profile.  Hence
the two hypothetical size-four/size-five signatures in their Conjecture
3.7 do not occur in this finite scope.  A universal proof is still needed
before upgrading the cyclic-connectivity reduction.

There is now a human-checkable partial exchange lemma.  For a \(T\)-join
\(J\subseteq G-M\) and a nonzero flow value \(c\), switching the flow by
\(c\) on the binary cycle \(M\cup J\) produces another exact-zero matching,
namely \(J\cap\phi^{-1}(c)\).  Minimum cardinality of \(M\) therefore forces
\(|J\cap\phi^{-1}(c)|\ge|M|\) in each of the three nonzero colors and hence
\(|J|\ge3|M|\).  This restriction is proved in
`docs/minimum-zero-tjoin-route.md`; it does not itself produce two disjoint
\(T\)-joins.

This isolates the universal bottleneck: prove that some
minimum-cardinality exact-zero matching extends, equivalently derive a
smaller exact-zero matching from any genuinely nonpacking minimum support.
The exchange step is open.  The finite frontier is stronger: every one of
the 20,749 minimum supports on the complete 1,388 hard order-20 hosts
extends by the exact component-parity criterion, including all 29 minimum
supports without connected complement.  On reconstructed \(H_3\), a
projected exhaustive enumeration finds exactly 92,313 minimum supports and
all extend.  A support-blocking CNF proves enumeration completeness, and
its LRAT is accepted by both project proof checkers.  Minimum witnesses also
extend on \(H_4\) and \(H_5\).  The package ledger SHA-256 is
`623c4d27043934fcca68534f66c252e62357714916d467a1b349b66debf19904`.

The full hard order-22 source has also been checked at the minimum-support
level.  All 12,892 frozen rows have some extending minimum support:
12,885 minima have size one and seven have size two.  All positive
certificates are independently replayed and reverse-lifted.  Each of the
seven nontrivial lower bounds has a 132-variable, 438-clause CNF and LRAT
accepted by both `lrat-check` and CakeML `cake_lpr`.  The finite-package
ledger is
`ed334f2df4131ed29b2924e4178e7f7853cf5a143e0427ac91ebb2c274d343f5`.
These are finite theorems, not a proof of the minimum-zero matching
conjecture or five-CDC.

The single size-three distance-two phenomenon now has an exact
three-edge-sum explanation.  Binary cycles, ordered
\(\mathbb F_2^2\)-flows, and constant-cycle switches combine as fibre
products over their even three-bit boundary data.  With exactly one zero
joining edge, the two-\(T\)-join packing predicate holds globally if and
only if it holds on both capped poles.  On the retained path, the first
boundary-\(000\) switch changes both pole flow orbits but leaves both
nonpacking; the second boundary-\(110\) switch repairs both simultaneously.
The human proof and two-checker finite package are in
`docs/three-sum-neutral-decomposition.md` and
`search/three-sum-neutral-decomposition-20260725/`.  This rules out an
additive pole-distance argument but does not settle the universal
cyclically 4-edge-connected branch.

There is also a new elementary numerical reduction.  For any
\(\mathbb F_2^2\)-flow on a loopless cubic multigraph, each nonzero linear
functional gives an even factor, and every odd component of that factor
contains a zero-edge endpoint.  Hence
\[
 \omega_{\rm w}(G)\le2r_f(G).
\]
Combining this with Huck's sourced condition
\(\omega_{\rm w}>6\) for a possible minimum five-CDC counterexample proves
that a smallest counterexample has flow resistance at least four.  If its
minimum exact-zero matching has size four, all three coordinate factors
must attain \((8,8,8)\).  Suppressing the eight zero endpoints then yields
eight vertex-disjoint marked bichromatic core circuits.  Precolouring the
marks alike and undoing suppression turns them into eight vertex-disjoint
odd ambient circuits, each of length at least eleven, so the original
graph has order at least 88.  Hence the
surviving dichotomy is \(r_M\ge5\), or the separated
size-four/order-at-least-88 branch.  The
proof and two-implementation coordinate audit are frozen in
`docs/flow-resistance-weak-oddness.md` and
`search/flow-weak-oddness-coordinate-20260725/`; the strengthening and
its clean-room audit are in
`docs/kempe-transversality-and-eight-mark-girth.md` and
`docs/audit-eight-mark-girth-bound.md`.  The \(H_4\)
projected-support master enumeration has now exhausted after exactly
4,931,430 distinct globally minimum size-four supports, all packing and
none nonpacking.  The retained corpus has SHA-256
`a7ede3be51d3b937bacf702d67aa51431192bcdea9b008bf835e25f82967b483`.
Completeness is now proof-certified: the fresh blocking CNF has 1,697
variables and 4,936,112 clauses (4,682 base clauses plus one block for
each support), and CaDiCaL 3.0.1 produced a 973,056,379-byte textual LRAT.
Both the independent C `lrat-check` and the CakeML-generated
`cake_lpr` report verified UNSAT.  The CNF SHA-256 is
`12061f07adc80081c6c329b1882201a734d004445a1e84d493f9bd7cd3743741`;
the LRAT SHA-256 is
`6bdeaff7fe3f37dca1c34c6653f0d1f1477490ffdd50f2d954fd88cc2c649934`.
The compact positive side is also complete.  A 152,874,330-byte file
stores one 243-bit even-marked circuit witness for every support.  An
independently written, solver-free checker reconstructed the graph, proved
all 4,931,430 rows distinct, and directly verified every circuit witness;
it reports
`VERIFIED rows 4931430 distinct 4931430 packing_witnesses 4931430`.
The full one-command acceptance package is
`search/h4-all-minimum-support-packing-20260726/`, whose manifest has
SHA-256
`ce247fb04a4a5a02c1d7e872cf3131447b90f568638340584dd5ebeb4a03f385`.
This proves the all-minimum-support extension theorem for the single
frozen \(H_4\), not any universal statement.

The marked-core obstruction itself has now been screened exactly on the
complete order-22 canonical connected simple cubic corpus.  The exact
ambient lift condition is
\[
 |\delta_H(X)|+|S\cap E(H[X])|\ge4
\]
for every cyclic shore \(X\); a direct human proof is in
`docs/marked-core-cyclic-lift-condition.md`.  The program enumerated
95,360,112 Tait colourings modulo global colour permutation on the
7,174,735 colourable rows.  No four-edge matching simultaneously has this
marked cut property, is separated in every Tait colouring, and is
nonpacking under the even-marked circuit criterion.  The frozen finite
result is
`scratch/order22-cyclic4-separated4-nonpacking-result.json`.  This is
consistent with a marked-core reducibility theorem, but is far below the
order-at-least-88 surviving branch and is not evidence of completeness
there.

The stronger assertion without the marked cut hypothesis is false already
on a 44-vertex core.  Its four marks are separated in all 5,832 Tait
colourings, but all 524,288 binary cycles containing them have one of the
odd profiles \((1,1,1,1)\), \((1,1,2)\), or \((1,3)\).  Three cyclic
two-edge cuts isolate one mark each, giving \(2+1<4\), so the example is
excluded by the exact lift condition.  Its data are in
`scratch/four-mark-lowcut-countermodel-44v-result.json`.

Packing across a nontrivial three-edge cut has now been reduced exactly
to seven local states: one closed state, or one of the three boundary
edge pairs together with the parity of marks on its open path.  Two
shores glue precisely when both have the closed state or share the same
pair-and-parity state.  A direct proof is in
`docs/marked-three-edge-cut-signatures.md`.  The frozen 13,824-instance
three-sum screen finds 288 universally separated marked rows and no row
which is also nonpacking and satisfies the marked cut condition.  The
zero-witness conclusion for this family now has a direct nine-circuit
proof: every permitted factor pole has the closed state, so every gluing
packs.

There is now also a universal low-cut lemma.  In a two- or three-pole
with distinct boundary ends, exactly two internal marks, and the exact
marked cyclic-cut inequality, a bridge-component count forces a circuit
through both marks.  Consequently a nonpacking four-mark core satisfying
the exact inequality has no cyclic two-edge cut, and an unmarked cyclic
three-edge cut cannot split the marks \(2+2\).  A second
bridge-component argument proves that the one-mark shore of an unmarked
\(1+3\) cut realizes all three odd open states.  Exact complete-host
diagnostics found the full
three-state signature on every eligible separated-triple pole tested:
12 at order 16, 162 at order 18, and 427 at order 20.  These 601 finite
cases are evidence, not the missing universal proof.  A complete
order-22 screen further found no universally separated triple in any
cyclically \(4\)-edge-connected Tait-colourable connected simple cubic
graph: 7,319,447 graphs and 95,360,112 Tait colourings modulo global
colour permutation were covered.  This frontier is sharp at the next
even order.  A systematic \(K_4\) four-sum screen over all 250
cyclically-four order-20 separated-pair hosts found 144 positive
order-24 rows, representing 20 unmarked and 46 marked isomorphism
classes.  The first explicit graph has graph6 record
shown below and marks \(01,23,20\,23\).

```text
W`??A???A_@_A_cO?S_Gc`_?@O@@?@OO??_????_??H_A?E
```

A clean-room verifier checks all 36 normalized Tait
colourings and every edge-deletion set of size at most three.  Thus the
provisional low-cut exposure conjecture is false; exact data are in
`search/cyclic4-universally-separated-triple-n24-20260726/`.  All 144
hits have girth four and marked-subdivision girth five, so none satisfy
the actual connected-branch requirement
\(|C|+|C\cap S|\ge10\) for every core circuit.  Thus this refutes the
low-cut diagnostic without entering the surviving high-marked-girth
branch.  A direct rerun of all 701,010 construction rows with the exact
marked-subdivision-girth-at-least-ten filter produced zero witnesses.

A new human-checkable proof, independently audited by a second Codex
agent, now bypasses the isolated three-mark
signature conjecture and closes the entire universally separated
four-mark core statement under the exact marked-cut inequality.  Cuts
with one or two marked boundary edges are reduced using the one-mark
shore lemma and the Knappe--Pitz \(g(3)=3\) circuit theorem.  All
remaining cuts are unmarked \(1+3\) cuts.  The canonical 3-sum
decomposition has a central cyclically \(4\)-edge-connected factor and
one-mark branches.  Precolouring all four marks alike makes the central
marks and one cap edge per branch into a same-colour matching of at most
four distinct edges.  Aldred--Ellingham--Hemminger--Holton handles four
distinct selected edges; Knappe--Pitz handles the smaller set that can
arise when adjacent cap roots share their selected edge.  The one-mark
paths then glue the branches back.  The full proof and exact
sources are in `docs/four-mark-core-closure.md`.  The audit confirmed
the stated binary-cycle theorem and emphasized that an unmarked \(2+2\)
cut may produce two two-mark circuits rather than one four-mark circuit.
This is an AI-agent audit, not independent human verification or peer
review.  The size-four/two-component marked-core branch is eliminated;
the connected eight-mark branch and the global minimum-support exchange
step remain open.

## Eight-coordinate construction

For each edge \(e\), the 2026 proof constructs a two-element label
\(P_e\subseteq\mathbb F_2^3\).  At every vertex, each of the eight elements
occurs on an even number of incident edge-labels.  The eight coordinate
supports are therefore Eulerian and double-cover the edges.  The 5-CDC asks
for the same two-element local-parity labeling with a universe of size five.

The most direct compression attempt is now scoped exactly.  For one
compatible potential, partitioning the eight coordinates and taking
symmetric differences gives a five-cover exactly when the coordinate
co-occurrence graph is five-colorable.  The 12-vertex rigid cap above forces
a \(K_6\), and the 46-vertex composition proves that no one connected-circuit
flow switch universally repairs this obstruction.  Different initial-flow
selection, non-pure recombination, multiple switches, or a theorem restricted
to the cyclically 4-edge-connected minimum-counterexample domain remain
possible.

This must not be confused with the older seven-even-subgraph 4-cover: the
seven nonzero linear combinations of three binary-flow supports cover each
edge four times, not twice.

## \(K_6\) defect-switch branch

A nowhere-zero \(\mathbb F_2^4\)-flow may be identified with an edge
labeling by the 15 duads of \(K_6\).  At a cubic vertex the three incident
duads are either a triangle or a perfect matching; the latter is called a
defect.  Omitting one \(K_6\) star is exactly the desired five-coordinate
label alphabet.  The exact reformulation and quotient \(T\)-join law are
recorded in `docs/k6-flow-reformulation.md` and
`docs/k6-defect-quotient-code.md`.

The tempting universal single-switch descent lemma is false even in the
nontrivial snark domain.  The exact package
`search/k6-defect-snark-plateau-20260725/` contains a 36-vertex simple
cubic graph of girth five and cyclic edge-connectivity four, a conserved
nowhere-zero flow with defects \(\{3,16,21,34\}\), and the following
independent evidence:

- a full scan of all \(2^{19}=524{,}288\) binary cycles for each of the 15
  nonzero switch values;
- an independent \(15\times8\) four-pole transfer calculation, with 256
  affine subsets per boundary sector;
- exhaustive cuts of sizes one through three and an exhibited cyclic
  four-cut;
- a 162-variable, 540-clause edge-colouring CNF whose LRAT is accepted by
  both `lrat-check` and CakeML `cake_lpr`; and
- an independent enumeration of all 208 perfect matchings, none with an
  all-even complementary 2-factor.

Every switch minimum is zero.  Thus cyclic edge-connectivity four does not
force a positive-defect state to have an immediately improving switch, even
for snarks.  The plateau nevertheless has a checked four-switch neutral
descent \(4\to4\to2\to2\to0\).  Its endpoint is a six-coordinate cover,
not immediately a five-cover: all local states are triangles, but the used
duads meet every \(K_6\)-vertex and omit no star.  A fifth checked switch
uses the star-cycle elimination lemma in
`docs/k6-star-cycle-elimination.md`, deletes one coordinate support, and
gives an explicit standard five-cycle double cover of the graph.

Triangle-preserving reconfiguration is nevertheless not universal.  The
exact package `search/k6-petersen-star-barrier-20260725/` freezes a
triangle-only Petersen flow whose entire such component is the free
\(S_6\)-orbit of size \(720\); all its states use all 15 duads and omit no
star.  Any path to a star-omitting flow must reintroduce at least two
defects.  A checked two-switch path attains that bound and ends at an
explicit standard five-cycle double cover.  Therefore a surviving
universal \(K_6\) route needs a controlled nonmonotone reconfiguration
theorem, a sound stronger structural restriction, or a different
potential.  The separate minimum-zero-matching/\(T\)-join route remains
open.

This barrier is not an isolated finite accident.  The exact package
`search/k6-petersen-ring-barrier-20260725/` replaces one edge in each of
\(n\) Petersen copies by a ring of equal-label connectors.  For every
\(n\ge1\), the resulting connected simple bridgeless cubic graph has a
triangle-only component of exactly \(15\cdot48^n\) states and no state in
that component omits a star.  The same component is obtained whether moves
may use arbitrary binary cycles or only connected circuits.  A blockwise
path has profile \(0,(2,0)^n\) and ends at a standard five-cycle double
cover, so the sharp defect barrier remains two.  This is an infinite exact
reconfiguration theorem, not a resolution of five-CDC; the family has
cyclic 2-edge cuts.

The publication audit in `preprint-k6/NO-GO.md` still correctly finds the
bare reformulation and the isolated Petersen example insufficiently novel
for a standalone preprint.  The subsequent infinite component theorem
crosses a plausible short-note threshold.  The research draft in
`preprint-k6-petersen-rings/` states the result narrowly, gives the corrected
human proof and literal certificate tables, and discloses substantial
OpenAI Codex assistance on its first page.  Novelty remains provisional
until a subject expert repeats the literature search and proof audit.

## Four-pole boundary branch and novelty correction

The exact five-coordinate boundary relation of an ordered cubic 4-pole has
ten \(S_5\)-orbits.  An independent rediscovery in this project initially
looked new, but the subsequent literature check found the same framework in
Máčajová--Mazzuoccolo--Tabarelli, *Ars Mathematica Contemporanea* 26
(2026), #P2.03, DOI 10.26493/1855-3974.3409.c13.  Their Theorem 3.6
identifies the unique pair of disjoint signatures that could occur on the
two sides of a cycle-separating 4-cut in a minimum CDC counterexample, and
their Remark 3.2 says the argument uses at most five colours and extends to
5CDC.  Their Conjecture 3.7 states that neither exceptional signature is
realizable.  The ten-orbit framework must therefore not be claimed as
novel here.

The retained finite census
`search/four-pole-signature-census-20260725/` tests all 1,273,263
independent deleted-edge 4-poles in 1,082 unique published snarks of orders
10 through 44.  Every pole realizes all ten boundary types; neither
exceptional signature occurs.  Source hashes, per-graph pole counts, the
CaDiCaL encoder, a standard-library ledger verifier, and a separately
written CNF/model checker are retained.  This is potentially new
computational evidence for Conjecture 3.7, but it is a finite positive
census, not a proof and not a 5CDC resolution.

The same package contains a canonical complete order-18 census.  `geng`
produces 41,301 connected simple cubic graphs; an independent backtracking
checker selects exactly 179 that are bridgeless and
non-3-edge-colourable.  Among their 53,163 independent-edge poles there
are 8,332 ordinary cut-driven signatures of sizes three or four, but no
instance of either exceptional signature.  A second verifier regenerates
the complete source scope, rechecks bridgelessness and Tait
non-colourability, and audits every retained signature row.

The human-checkable note `docs/four-pole-boundary-human-lemmas.md` proves
the direct label equivalence, the ten-type classification, exact
factorization across a two-edge join, and the boundary relations forced by
a disconnected pole or an internal pole bridge.  In particular, ordinary
two-pole substitution cannot create a first counterexample from positive
factors.  The remaining four-pole step is precisely the published
Conjecture 3.7 rather than a solved reduction.

The follow-up package
`search/four-pole-order16-frontier-20260726/` completes the larger natural
scope of all 280,855 connected simple terminal-distinct cubic four-pole
cores of order 16.  The exact profile is
\[
0:4745,\qquad4:21801,\qquad9:43650,\qquad10:210659.
\]
There is again no size-five row and neither exceptional signature occurs.
After an independent proper-bridge audit, 38,357 internally bridgeless
poles have size nine and 205,241 have size ten.

The size-nine frontier has additional structure.  Exactly 127 of the
38,357 internally bridgeless rows are not 3-edge-colourable.  Of these,
124 have a nontrivial proper two-edge cut.  The remaining three canonical
records all miss only type \(AA\); each has a cycle-separating proper
three-edge cut and proper-core girth four or five.  Thus none lies in the
cyclically-4/girth-reduced minimum-counterexample domain.  These are
positive nine-type poles, not exceptional signatures or counterexamples.
In fact every one of the 127 non-colourable size-nine rows has a
cycle-separating proper cut of size two or three.  Hence every
internally-cyclically-4 non-colourable pole in the complete order-16 scope
has all ten boundary types.

The same human note now includes an exact small-cut replacement lemma.  A
two-edge-cut shore containing no original pole terminal is a 2-pole and,
when nonempty, has precisely the equality interface of one edge.  A shore
containing one original terminal is a 3-pole and, when nonempty, has
precisely the triangle interface of one cubic vertex.  Replacing either
shore preserves the complete five-coordinate boundary relation.  Hence a
minimum positive exceptional pole has no nontrivial zero- or one-terminal
two-cut shore.  The unresolved two-plus-two split remains a genuine
four-pole composition.

## Orientable branch

The orientable 5-CDC is a separate stronger conjecture.  Each coordinate has a
directed Eulerian orientation and the two occurrences of every edge point in
opposite directions.  Oum states it separately as Conjecture 19.  It implies
Tutte's nowhere-zero 5-flow conjecture, so orientability is not included in
the standard SAT/XOR acceptance condition.

## Connected eight-mark paired-cut and incidence-code reduction

Audit date: **2026-07-26**.

In the connected size-four branch, the four zero edges pair the eight
marked edges of the suppressed Tait-colourable core.  This pairing cannot
be discarded.  For a cyclic core cut \(X\), let \(p_P(X)\) count pairing
edges whose two marks lie strictly internally on opposite shores.  The
exact lift and boundary-optimization lemmas in
`docs/connected-eight-mark-paired-cut-condition.md` prove the necessary
condition
\[
       |\delta_H(X)|+p_P(X)\ge4.
\]
A separately prompted Codex agent audited the proof and wrote an
independent clean-room checker.  It confirmed all 49 low cyclic cuts and
all 105 perfect pairings of the retained order-60 stable-eight-mark core.
No pairing survives: 27 have minimum score two and 78 have minimum score
three.  Thus the entire previously retained order-68 expansion family is
excluded structurally.  This is an AI-agent audit, not human peer review,
and it is not a universal closure theorem.

Universal separation allows all eight marks to be precoloured with one
Tait colour.  Linear cycle-space duality then guarantees a binary cycle
containing all eight marks.  The only remaining packing obstruction is
componentwise mark parity.  The exact algebraic formulation in
`docs/eight-mark-bichromatic-code.md` encodes selected \(ac\)- and
\(bc\)-circuits by a connected bipartite incidence multigraph.  The
all-mark selectors form an affine cut-space slice, while componentwise
evenness is precisely signed balance, or trivial
\(\mathbb F_2\)-voltage holonomy, on the selected circuit system.  Jointly
these conditions form the explicit quadratic system (15).  A checked
12-vertex example proves that the good selectors are not an affine
subspace, so the residual topology cannot be replaced by pure XOR in the
selector variables.

The connected eight-mark branch therefore remains open, but its finite
search space and exact obstruction have been sharpened: a surviving core
must satisfy the paired low-cut inequalities, the inherited marked
circuit-length condition
\[
 |C|+|C\cap S|\ge10
\]
for every core circuit, universal separation under every Tait colouring,
and global minimum-support constraints, while every selector in the
incidence code must have nontrivial signed holonomy on some circuit
component.  It is the ambient expansion, not necessarily the suppressed
core itself, which has girth at least ten.

There is also a new direct order bound.  Precolour all eight marks with
one Tait colour.  Universal separation places them on eight
vertex-disjoint bichromatic even circuits, one mark per circuit.
Undoing suppression replaces each unique marked edge by a two-edge path,
so these become eight vertex-disjoint odd circuits of the ambient graph.
If the ambient girth is at least ten, every such odd circuit has length
at least eleven.  Hence every minimum counterexample in the exact-zero
size-four extremal branch has
\[
 |V(G)|\ge 8\cdot11=88,
\]
improving the earlier bound \(68\).  The human-checkable proof is in
`docs/kempe-transversality-and-eight-mark-girth.md`; it applies to both
the connected eight-mark branch and the two-component \(4+4\) branch.

## Cycle-trace surjectivity and the factor-quotient obstruction

Audit date: **2026-07-26**.

Universal separation has a further exact linear consequence.  Arbitrary
precolouring of the marks rules out every nonempty cut supported inside
the marked matching.  Equivalently, deleting the marks leaves the core
connected, and restriction of the binary cycle space to the eight marked
coordinates is surjective.  Thus every prescribed marked trace occurs.
The proof in `docs/universal-separation-cut-surjectivity.md` passed an
independent line-by-line Codex-agent audit after correcting `dim` to
affine dimension for nonzero fibres and narrowing one signed-holonomy
sentence.  Surjectivity does not control marked parity separately on
each circuit component, so it does not close the branch.

For an all-\(c\) Tait colouring, lift the \(ac\)-factor, contract its
circuits, and delete the four zero edges.  The resulting quotient is a
connected Eulerian multigraph with eight distinct marked vertices.
Every connected Eulerian multigraph has two edge-disjoint joins for any
even terminal set: construct one in a spanning tree and take its edge
complement.  However, the two joins must also route edge-disjointly
through the cyclic order of the ports on every contracted factor
circuit.  The exact necessary-and-sufficient local transition system is
proved in `docs/eulerian-factor-quotient-tjoin-reduction.md`.

Eulerianity alone is insufficient.  The four-vertex quotient in
`docs/two-tjoin-cycle-lift-obstruction.md` has exactly four \(T\)-joins
and two disjoint pairs, but both pairs fail the marked alternating-gap
test at the same factor circuit.  This is a human-checkable obstruction
to the quotient proof, not to five-CDC.

The actual minimum-counterexample hypotheses exclude that literal small
quotient.  Every factor-quotient degree is at least ten, there are eight
marked quotient vertices, and every quotient shore obeys the paired-cut
inequality.  More generally, an unavoidable failure at one marked
terminal gap is exactly an even-terminal two-edge cut in the quotient.
The paired-cut inequality promotes it to either a cyclic ambient
four-edge cut containing two zero edges or a cyclic six-edge cut
containing all four.  Simultaneous terminal-gap failure has the explicit
cut-space certificate in
`docs/size-four-terminal-gap-cut-reduction.md`.  Eliminating these cut
branches, the other same-parity gap equations, and nonpartitioning join
pairs remains open.

An exact diagnostic on the excluded order-60 stable-eight core confirms
that the lift issue is real.  Its quotient has
\(14\,801\,616\,000\) ordered edge-disjoint quotient-\(T\)-join pairs,
but none passes every cyclic-port test.  A clean rerun reproduced the
saved result byte for byte.  Independent enumeration of all \(2^{23}\)
all-mark core cycles also finds zero with even marked parity on every
component.  The core fails the paired-cut condition, and its reconstructed
ambient graphs have standard five-covers, so this is only a diagnostic.

## Order-80 vertex-transitive equality control

Audit date: **2026-07-26**.

The 88-vertex ambient lower bound makes order 80 the equality order for
the suppressed core.  The complete Potočnik--Spiga--Verret census contains
33 cubic vertex-transitive graphs of that order.  Exact short-cycle
incidence counts eliminate 32: graphs of girth at most six fail
immediately, and each of the seven girth-eight graphs has insufficient
eight-edge incidence capacity to put at least two marks on every
eight-cycle.  The sole girth-ten graph has exactly 426,256 normalized Tait
colourings and no universally separated eight-edge matching.

The script, census commit and hash, exact incidence certificates, input
encoding, and Tait result are frozen in
`docs/order80-vertex-transitive-control.md` and
`scratch/order80-cvt-stable8-marked-girth-result.json`.  The cycle
enumerator agrees with NetworkX on all 994 connected simple Graph Atlas
graphs, and a separate MILP agrees with the seven counting
infeasibilities.  This eliminates the vertex-transitive equality scope
only; vertex-transitivity is not a minimum-counterexample reduction.

## Equality incidence countermodel and exact CVT selector control

Audit date: **2026-07-26**.

The order-\(88\) equality equations alone do not force a good
bichromatic selector.  An explicit connected 5-regular bipartite
incidence multigraph on \(8+8\) factor vertices, with a marked perfect
matching and compatible cyclic transition data, reconstructs a connected
simple cubic 80-vertex Tait-coloured core.  Both relevant factors are
eight 10-cycles with one mark each, but exhaustive enumeration finds zero
good selectors among all 256.

This is deliberately an abstract route countermodel, not a surviving
core: its core and marked subdivision have girth three, one Kempe switch
violates universal separation, and an independently checked SAT witness
gives two unrestricted edge-disjoint \(T\)-joins.  The construction and
two independently structured selector checks are in
`docs/equality88-incidence-rotation-countermodel.md`.

The sole girth-ten vertex-transitive graph behaves oppositely.  Among its
426,256 normalized Tait colourings, exactly 20 have all three
bichromatic factors equal to eight 10-cycles.  For every colouring and
each of three common colours, the incidence multigraph has exactly 1,249
edge-object perfect transversals.  The resulting 74,940
colouring/common-colour/mark-set records contain 19,184,640 selectors.
Every record has a good selector; in fact the count per record lies
between 94 and 138.  A NetworkX audit verifies that all 60 cases are
colour-preservingly isomorphic and independently reproduces the
transversal and selector histograms.  Exact artifacts are in
`docs/order80-c10-selector-transversal-scan.md`.

Together these computations show that abstract equality incidence is
too weak, while the natural girth-ten vertex-transitive control is
strongly positive.  Arbitrary non-vertex-transitive equality cores and
all larger orders remain open.
