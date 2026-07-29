# Current-status audit

Search date: **2026-07-29**.

## Classification

**PARTIAL STRUCTURAL PROGRESS.**

The five-cycle double cover conjecture remains open.  In July 2026 the
ordinary cycle double cover conjecture was announced as proved; the proof
yields an 8-cycle double cover for every bridgeless graph.  Sang-il Oum's
exposition dated 2026-07-24 states the five-coordinate strengthening
separately as Conjecture 18.

## 2026-07-29 resolution-frontier update

The exact surviving obligation is existential.  In the cubic reduction,
Hušek--Šámal's Theorem 3.16 and Conjecture 3.19 ask for **some**
nowhere-zero \(\mathbb F_2^3\)-flow having a functional whose kernel
components satisfy the required parity condition.  Equivalently, in the
project's two-cycle language, some extendable binary projection must have
a clean extension.  A graph whose mandatory exact-two/XOR formula is
independently certified UNSAT would settle the conjecture negatively.
Neither object is presently known.

The proposed shortcut “choose a cardinality-minimum extendable projection”
is now refuted.  The frozen strict-lock construction is a simple connected
bridgeless nonplanar cubic graph on 162 vertices and 243 edges.  It has a
unique globally minimum extendable projection, of size 54 and consisting
of two 27-circuits, and that projection has no clean extension.  The graph
itself has two explicit standard FiveCDC certificates, including a direct
assignment to the mandatory exact-two/XOR variables.  Thus this is a
counterexample to a proof strategy, not to FiveCDC.

The construction, a complete human proof, primary and independently
written checkers, canonical graph encodings, literal certificates, and
hashes are frozen in:

- `scratch/minimum-projection-strict-parity-lock-20260729/`; and
- `scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/`.

The focused AI-disclosed manuscript is
`preprint-minimum-selection-counterexample/main.pdf`; the expanded research
draft is `preprint-minimum-fano-projection/main.pdf`.  Both explicitly state
that FiveCDC remains open and that no literature-wide priority claim has
been established.

Primary/current sources:

- OpenAI, *A Proof of the Cycle Double Cover Conjecture* (2026):
  <https://cdn.openai.com/pdf/04d1d1e4-bc75-476a-97cf-49055cd98d31/cdc_proof.pdf>
- S.-i. Oum, *A proof of the cycle double cover conjecture by OpenAI: An
  exposition*, arXiv:2607.16356v2 (2026):
  <https://arxiv.org/abs/2607.16356>
- R. Hušek and R. Šámal, *Exponentially Many Circuit Double Covers*,
  arXiv:2607.24724v1 (submitted 2026-07-27):
  <https://arxiv.org/abs/2607.24724>. Their Theorem 3.16 independently
  gives the exact five-support component-parity characterization, their
  Conjecture 3.19 is the equivalent remaining flow-selection problem, and
  their introduction explicitly retains FiveCDC as open.
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

The reduced probe now also includes all seven retained order-34 strong
snarks and the unique retained girth-at-least-six snarks of orders 28, 30,
and 36.  Among 5,000 newly sampled nowhere-zero flows, 2,245 are
pure-merge-bad and every one has an exactly checked connected-circuit
repair.  The flow selection is random, so this remains finite sampled
evidence.  The replay and human scope audit are in
`scratch/audit_strict_oum_one_switch_20260728.py` and
`scratch/strict-oum-one-switch-audit-20260728.md`.

For an eight-coordinate cover the apparently broader \(R_5\)-compression
criterion is now proved equivalent to five-colour pure merging.  Every
graph on at most eight vertices with chromatic number at least six contains
\(K_6\) or \(K_3\vee C_5\); neither maps to \(R_5\).  Thus this distinction
does not create a second reduced branch.

The most direct attempted proof of the surviving one-circuit statement is
false even on the first Blanuša snark.  The exact package
`search/fano-circuit-avoidance-countermodel-18v-20260728/` gives a
merge-bad fixed flow for which \(G-M_6\) is connected and bridgeless, but
three value-3 edges lie on no common circuit of \(G-M_6\).  A two-vertex
separator proves noncontainment, while a disconnected binary cycle through
all three marks repairs every compatible \(K_6\) cover.  Flow parity does
exclude every odd cut contained in the marked triple; the failure is a
two-separation outside the hypotheses of Knappe--Pitz.  The same fixed flow
has a different connected-circuit repair, so this kills only the
prescribed-triple proof step, not the surviving existential one-circuit
formulation and not FiveCDC.

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

A threshold-only extension exhausts all 69,243 internally bridgeless
order-15 cores.  Every record reaches 46 satisfiable boundary orbits;
there is no order-15 counterexample to the threshold.  Since the
classifier stops at 46, this run does not determine the full state-size
profile.  A fresh canonical-corpus replay, bridge checks, transcripts,
and an optional byte-identical CaDiCaL replay are in
`search/five-pole-46-threshold-order15-20260727/`.

The internal-bridge restriction has a short human proof in
`docs/five-pole-realizability-frontier.md`: a bridge splitting off
\(k\le2\) distinct terminals creates a cycle-separating cut of size
\(k+1\le3\), contradicting the reduced cyclically 4-edge-connected
domain.  The universal 46-state lower bound remains unproved.  If true, it
would force two five-pole shore relations to intersect by
\(46+46-62=30\), excluding the corresponding five-cut.

A scope audit proves that the universal lower bound would in fact resolve
standard Five-CDC, rather than merely remove five-cuts.  Given any edge
\(uv\) of a simple bridgeless cubic graph, replace it by a six-edge path
with five new degree-two terminal vertices.  The resulting five-pole core
is internally bridgeless.  Any \(D_5\)-labelling of the pole has equal
labels on the two path-end edges after summing over the old vertices, so
it contracts back to a \(D_5\)-labelling of the original graph.
Conversely, the closed label walk
\[
01,02,03,01,02,01
\]
extends any normalized label on the replaced edge, with terminal labels
\(12,23,13,12,12\).  Thus universal nonemptiness for this five-pole class
is already equivalent, after the standard reduction, to Five-CDC; the
46-state assertion is strictly stronger.  The complete human proof is in
`docs/five-pole-realizability-frontier.md`.

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

This once isolated a proposed universal bottleneck: prove that some
minimum-cardinality exact-zero matching extends, equivalently derive a
smaller exact-zero matching from any genuinely nonpacking minimum support.
That unrestricted statement is now false.  The certified 130-vertex
countermodel described below has \(r_f=r_M=5\), but every
matching/four-flow extension has matching size at least six.  The earlier
finite frontier remains valid: every one of
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
These are finite theorems that preceded the 130-vertex refutation; they are
not a proof of five-CDC.

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

## Equality incidence, rooted interfaces, and the order-88 exclusion

Audit date: **2026-07-26**.

The bare equality incidence data are not enough to force a good
bichromatic selector.  The explicit decorated \(8+8\), 5-regular
incidence object in `docs/equality88-incidence-rotation-countermodel.md`
reconstructs a simple connected order-80 Tait core for which all 256
factor selectors fail componentwise mark parity.  Two independent
programs reproduce the exact profile histogram.  The object has girth
three, is not universally separated, and has an unrestricted pair of
edge-disjoint terminal joins, so it is a countermodel only to the
incidence-only proof shortcut.

The rooted four-mark analysis in
`docs/rooted-four-mark-cap-avoidance.md` proves, by cycle/cut
orthogonality, that an inherited cap with four common-colour marks and a
differently coloured cap edge always has an all-mark binary cycle
avoiding the cap.  The remaining issue is componentwise mark parity.
An exact order-28 countermodel shows that universal separation and the
colour pattern alone do not force rooted componentwise parity; its
cyclic 2-cut has a \(3+1\) mark split and it fails the required marked
cut inequality.

The equality case itself is nevertheless impossible.  The solver-free
argument in `docs/equality88-kempe-girth-contradiction.md` shows that two
lifted marked \(C_{10}\) factor circuits cannot share a second
\(c\)-edge in an ambient graph of girth at least ten.  The delicate
two-overlap case is a \(C_{18}\) with two chords and yields the parity
contradiction \(2\alpha=9\).  Thus the equality incidence multigraph is
simple.  Switching one \(ac\)-\(C_{10}\) then splices five opposite
factor \(P_9\)'s into a single \(C_{50}\) containing four marks,
contradicting universal separation.  In the \(4+4\) branch, simplicity
would require a 5-regular simple bipartite graph on \(4+4\) vertices,
which is impossible.

A separately prompted blind agent reconstructed the full proof and
issued a pass after one exposition correction, recorded in
`docs/equality88-overlap-audit.md`.  The equality proof alone implies
\[
                         |V(G)|\ge90.
\]
The stronger low-surplus result below supersedes this numerical bound.

For the sole girth-ten order-80 vertex-transitive graph, a further exact
diagnostic enumerated the 20 Tait colourings whose three bichromatic
factors are all \(C_{10}\)'s.  Across 60 common-colour cases and 74,940
factor-transversal mark records, every record has a good selector
(minimum 94 of 256).  An independent isomorphism audit reproduces the
totals.  This finite result is consistent with, but not used by, the
general order-88 exclusion proof.

## Low-surplus Kempe bound and certified order-100 global-profile closure

Audit date: **2026-07-26**.

The equality argument extends to all ambient orders through \(94\).
For a marked bichromatic factor circuit with \(d\) common-colour edges,
let \(p\) and \(u\) be the numbers of marked and unmarked circuits of
the opposite factor that it meets.  Cutting the common-colour edges
produces three perfect matchings on \(2d\) endpoints.  Their cycle-space
rank, followed by universal separation after the Kempe switch, gives
the human-checkable inequality
\[
                         2p+u\le d+2.
\]
Ambient girth at least ten also gives sharp marked--marked and
marked--unmarked overlap bounds.  Exact surplus capacity first excludes
\(t=0,1,2,3\) in \(|V(G)|=88+2t\), giving \(|V(G)|\ge96\).

Three further human local lemmas sharpen the order-\(96\) boundary:
a sum-\(26\) triple-overlap obstruction, a diagonal mixed-parity
obstruction, and a spacing theorem saying that a marked core \(C_{10}\)
can double-overlap with at most one opposite marked core \(C_{12}\).
After those lemmas are imposed, a solver-free canonical backtracker
exhausts all \(109\) simultaneous-\(S_8\) profile-pair orbits in \(3,266\)
nodes and finds no incidence matrix.  A separately implemented
quantifier-free integer encoding returns UNSAT on all \(109\) instances.
An independent audit additionally normalized all \(108,900\) labelled
profile pairs and reran a prune-free DFS with the same empty result.
At ambient order \(98\), the factor-size equation first permits an
unmarked circuit.  A direct application of the same incidence inequality
excludes that possibility, leaving \(335\) simultaneous-\(S_8\)
all-marked profile-pair orbits.  A further human local lemma shows that
a same-mark pair with total excess two cannot share three common-colour
edges: after taking the symmetric difference, contraction gives either
the triangular prism or \(K_{3,3}\), and a weighted short circuit
contradicts girth ten.

The strengthened solver-free census exhausts all \(335\) orbits in
\(32,327\) nodes and finds no matrix.  A separately generated Z3
encoding returns \(335/335\) UNSAT.  A third audit independently
normalizes all \(792^2=627,264\) labelled profile pairs, reruns the
primary search without its forward prune for \(9,193,235\) nodes, and
finds all \(335\) independently generated HiGHS models infeasible.
Deleting only the new diagonal cap leaves exactly two survivors.

At order \(100\), a human Kempe-incidence argument first excludes every
factor with an unmarked circuit.  The all-marked cap-table census has
\(1002\) canonical excess-profile pairs, of which \(155\) survive.  Exact
weighted two-circuit row-and-column stars reduce these to three relative
alignments of the partition
\((2,2,1,1,0,0,0,0)\).  A profile-level Boolean encoding then chooses,
rather than fixes, every incidence cell, cyclic position set, bijection,
and endpoint twist.  It reconstructs the complete \(92\)-vertex
suppressed core and rejects precisely forced circuits of length below ten.

The three final formulas have respectively
\[
\begin{array}{c|r|r|r}
\text{profile}&\text{variables}&\text{base clauses}&\text{sound lazy clauses}\\
\hline
0&36\,388&96\,072&94\,135\\
1&36\,188&95\,537&115\,385\\
2&35\,988&95\,002&787\,384
\end{array}
\]
and are all UNSAT before any of the \(105\) terminal pairings is reached.
CaDiCaL emitted LRAT proofs, and the independent C `lrat-check` accepted
all three.  A separately written producer-free checker regenerates the
local option domains and base CNFs and verifies, clause by clause, that
every one of the \(996\,904\) appended clauses forces an actual short
circuit.  It also checks that the three formulas exactly match the three
surviving row-star profiles.  Consequently the connected extremal
exact-zero size-four branch satisfies
\[
                         |V(G)|\ge102.
\]

The proof, audits, and checkers are
`docs/order94-kempe-surplus-bound.md`,
`docs/audit-and-generalization-order94-kempe.md`,
`docs/order96-incidence-skeleton-nonrealizability.md`,
`docs/order96-complete-incidence-census.md`,
`docs/diagonal-c14-c10-triple-overlap.md`,
`docs/order98-complete-incidence-census.md`,
`docs/order98-independent-incidence-audit.md`,
`docs/order100-unmarked-exclusion-and-row-star-frontier.md`,
`scratch/enumerate_order96_incidence_system.py`, and
`scratch/check_order96_incidence_system_z3.py`, together with their
order-\(98\) counterparts, plus
`scratch/check_order100_global_profile_cnf.py`.  This is a
branch-specific theorem and does not resolve five-CDC.

## Rooted bridge elimination

Audit date: **2026-07-26**.

The marked cyclic-cut inequality excludes the \(3+1\) bridge mechanism
of the rooted order-\(28\) countermodel uniformly.  If deletion of the
forbidden cap \(f\) leaves a bridge \(h\), then
\(\{f,h\}\) is an unmarked 2-cut with two cyclic shores.  The marked-cut
inequality forces a \(2+2\) mark split, and the audited two-mark shore
lemma supplies one two-mark circuit on each shore, both avoiding the
cap.  The same proof uses only the weaker inequality already inherited
on the opposite shore of the cyclic six-cut reduction.

Consequently any surviving rooted failure has a connected bridgeless,
hence 2-connected, subcubic deleted-root graph.  Every mark pair is
cyclable, no circuit contains all four marks, and for each of the three
pairings the two complementary pair-cycle families are cross-intersecting.
The remaining problem is therefore a genuine four-way linkage
obstruction, not trace feasibility or a hidden bridge.  The proof and a
240-instance structured finite screen are recorded in
`docs/rooted-four-mark-bridgeless-reduction.md`.

Subdividing the four marks converts this obstruction to a four-terminal
linkage problem.  Ozeki's four-terminal theorem has two structural
outcomes after its prerequisite reductions.  The \(V_8\)-subdivision
outcome is impossible here: its four spoke paths and four alternating rim
segments explicitly form two vertex-disjoint pair-circuits.  The private
factor-circuits also settle triple cyclability and exclude the nice
decomposition when the original subdivided graph is already irreducible;
see `docs/rooted-four-mark-ozeki-linkage-gate.md`.

The remaining forbidden-vertex path failure has now been localized.  If
deletion of the forbidden vertex is not 2-connected, an articulation
initially gives a \(2+2\) terminal split or a \(1+3\) split with a
singleton one-terminal side.  Triple-circuit splicing eliminates the
\(2+2\) split.  If deletion remains 2-connected, Ozeki's
four-terminal path corollary and a subcubic degree count give a stable
three-vertex separator, exactly four terminal components, and boundary
profile \(2222\) or \(2223\).  Triple cyclability eliminates \(2222\)
and forces the \(2223\) incidence graph to be \(K_{4,3}\) minus a
three-edge matching.  One-terminal irreducibility makes each of its
three boundary-two components a singleton.  The corresponding private
circuits must use both separator neighbours, but any two boundary-two
rows share a neighbour, contradicting their vertex-disjointness.  Thus
the entire three-vertex row star is impossible.  As an independent
check, the counterfactual triangular-prism quotient forces its marked
and root edges to have the same Tait colour by counting cross edges of
each colour from its two triangles, contrary to the inherited
precolouring.  The separator analysis's sole P4 residual was the
\(1+3\) singleton two-vertex interface; it is closed below under the
same simultaneous irreducibility/private-circuit premises.  The separator proof is in
`docs/rooted-four-mark-p4-row-star-reduction.md`.

The one-terminal reductions preserve triple cyclability once it has
been established: a terminal-triple circuit has a unique segment through
the reduced side, and replacing that segment either preserves the triple
or creates a four-terminal circuit which lifts back immediately.
Separator terminals cause no exception, and a parallel edge seen only
after suppressing the replacement terminal is a representation issue,
not a failure of certificate lifting.  This does not yet establish T3
before the first reduction when the original graph is reducible.

In the last \(1+3\) interface, suppressing the singleton terminal gives
a marked edge \(s_1=wu\).  P4 is exactly the assertion that, after
deleting \(w\), there is a path starting at \(u\) through the other
three subdivided marks.  This assertion now has a human-checkable proof.
Put \(K=H-\{w,z_1\}\).  If \(K\) had a cut vertex \(x\), the components
behind \(\{w,x\}\) would either violate irreducibility, force a private
circuit to meet \(R_1\) at \(w\), or give a \(2+2\) terminal split which
triple-circuit splicing turns into a four-terminal circuit.  Hence \(K\)
is 2-connected, and \(u,z_2,z_3,z_4\) all have degree two.

The needed endpoint statement is general: in a 2-connected subcubic
graph, a path can start at any one of four specified degree-two vertices
and pass through the other three.  Add a leaf at the prescribed start,
make the endpoint-safe one-terminal reductions, and use Ozeki's
Section 4.9 path-obstruction description.  Its two irreducible
obstructions require either at least seven cut incidences at two
subcubic vertices or one vertex adjacent to all four terminals.  Both
are impossible.  The complete lifting details are in
`docs/rooted-four-mark-singleton-endpoint-closure.md`.  An independent
finite audit checks 1,100,688 subdivided cubic endpoint instances through
base order twelve; it is not used in the proof.

Thus P4 now holds in the exact simultaneous irreducible/private-circuit
state.  Literal four-private-circuit preservation through arbitrary
one-terminal preprocessing is false.  The exact replacement frontier is
now known.  If another terminal lies on the separator, triple
cyclability directly splices a four-terminal circuit, so that case
closes without preservation.  With a terminal-free separator, the only
marked borrower \(R^\ast=R_j\) leaves a pairwise disjoint \(2+1+1\)
circuit packet: one circuit through the reduced and borrowed terminals,
plus the other two private circuits.  Full universal separation and the
marked cyclic-cut inequality do not exclude this state; an audited
order-56 compliant graph realizes it and has a displayed root-avoiding
four-mark circuit.  The remaining rooted obligation is to use that
\(2+1+1\) packet in the two projected outer interfaces N and E described
in `docs/one-terminal-trace-lift-frontier.md`, not an augmented
\(K_{3,2}\) attachment obstruction.

## Exceptional four-pole rooted-packing algebra

Audit date: **2026-07-26**.

The two exceptional four-pole signatures isolated by
Máčajová--Mazzuoccolo--Tabarelli have an exact interpretation in the
project's distinguished quotient.  A projection-coherent
five-coordinate lift is equivalent to an ordered pair of edge-disjoint
terminal joins.  For the nonzero cap \(f\), boundary type
\(T_\pi T_\pi\) means that both joins avoid \(f\), whereas
\(AT_\pi\) means that exactly one uses it.  The published exceptional
pair therefore has opposite rooted-packing polarities.

In the actual cyclic-four-cut branch, a connected shore with no internal
zero edge has two edge-disjoint paths between the zero terminals which
both avoid the nonzero cap.  Hence an exceptional four-type shore must
contain at least one internal zero edge.  Since there are two proper
zero edges in total, only the distributions \((1,1)\) and \((2,0)\),
with the four-type shore first, remain.

The cap geometry has now been separated correctly.  A simple opposite cap
produces rooted four- or six-mark atoms; a terminal-flanked cap smooths
exactly to a simple 2-connected unrooted atom.  In the six-mark simple-cap
case, a bridge gives either a smaller closed four-mark atom or a cyclic
five-cut with exact boundary word \(000bb\).  Repeated nontrivial
two-plus-two pole decompositions descend to a smaller exceptional shore.
These are reductions, not eliminations; the surviving obligations are
listed in `docs/exceptional-four-cut-surviving-split-atoms.md`.

An exact ten-state two-plus-two composition table gives a further
minimality reduction: an exceptional four-type signature cannot be
created without an exceptional four-type factor.  The five-type
signature has the analogous conclusion except for one explicitly listed
looped-edge/looped-path auxiliary factorization.  Independent Python and
JavaScript implementations agree on all 640 boundary words, ten orbit
classes, 259 published-lemma-admissible masks, and all exceptional
factorizations.

The human proof, table, frozen result, and independent verifier are in
`docs/four-pole-exception-rooted-packing-algebra.md` and the corresponding
`scratch/four_pole_two_plus_two_algebra.py`,
`scratch/four-pole-two-plus-two-algebra-result.json`, and
`scratch/verify_four_pole_two_plus_two_algebra.mjs`.  The full published
exceptional-signature conjecture remains neither realized nor refuted.

## Root reduction localizes forbidden-cycle failure to a four-cut

Audit date: **2026-07-27**.

There is now a direct human-checkable rooted theorem for the highly
connected case.  Let \(H\) be simple and cyclically
\(4\)-edge-connected, let four matching edges be separated in one Tait
colouring and have one common colour, and let a forbidden root \(f\)
have a different colour.  Delete the two ends of \(f\) and join their
two remaining neighbour pairs.  Fixed-colouring separation guarantees
that the four marked images are still a matching: any new adjacency
would put two marks on one bichromatic factor circuit.

If the reduced graph is cyclically \(4\)-edge-connected, the
Aldred--Ellingham--Hemminger--Holton four-independent-edge theorem gives
a cycle through the four images.  Expanding the two new edges lifts it
to one all-four circuit avoiding \(f\).  If the reduction is not
cyclically \(4\)-edge-connected, a direct shore-placement argument
pulls a small cyclic cut back and proves that \(f\) belongs to an
independent cyclic four-edge cut of \(H\).

Consequently the rooted four-mark circuit assertion is proved outright
for cyclically \(5\)-edge-connected factors.  At cyclic connectivity
four, every surviving failure is localized to a root-containing
independent four-cut; the remaining four-pole interface is still open.
The full proof is
`docs/root-edge-reduction-four-cut-gate.md`.

## Order-22 universal four-separation census

Audit date: **2026-07-27**.

Canonical generation and two algorithmically different checkers now
exclude a universally separated four-edge matching from every
Tait-colourable connected simple cubic graph on 22 vertices.  The
complete corpus has \(7\,319\,447\) graphs, of which \(7\,174\,735\)
are Tait-colourable; the remaining graphs are outside this theorem
because the implementations skip the vacuous no-colouring case.
Both the direct colouring recursion and the independent
perfect-matching/even-two-factor replay enumerate exactly
\(95\,360\,112\) normalized Tait colourings and find zero witnesses.
The independent replay visits \(312\,583\,931\) perfect matchings.

Together with the separately frozen complete standard-hypothesis screen
through order 20, this raises the minimum possible order of a simple
cubic standard rooted four-mark atom to 24.  It is a finite lower bound,
not a universal rooted theorem.  The report and machine-readable
metadata are
`docs/order22-universal-four-separation-screen.md` and
`scratch/order22-universal-four-separation-result.json`.

## Simple-cap reduction for exceptional four-poles

Audit date: **2026-07-27**.

The finite search scope for the remaining exceptional four-pole branch
now has a human-checkable completeness proof.  Every connected simple
terminal-distinct four-pole core admits a perfect matching of its four
degree-two terminals using two nonedges.  Adding those two independent
edges creates a simple cubic cap.  When the pole is bridge-free and has
one of the two exact exceptional signatures, the cap is bridgeless and
non-3-edge-colourable.  Hence a canonical census of bridgeless non-Tait
cubic graphs followed by every independent-edge deletion exhausts this
entire pole scope; it is not merely a hard-family sample.

For a vertex-minimal two-cut-reduced exceptional pole, every such cap
has a sharper fork.  It is either cyclically \(4\)-edge-connected, or
it has a cyclic three-edge cut disjoint from the two cap edges which
splits the original terminals \(2+2\), with one whole cap edge on each
shore.  A terminal-free three-cut shore is replaceable by one cubic
vertex and therefore cannot occur in a minimum atom.  The surviving
\(2+2\) cyclic-three-cut outcome is a five-pole interface and remains
open.  The complete proof is
`docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`.

The surviving \(2+2\) cyclic-three-cut fork now has an exact
seven-state rooted description.  Fixing the three connector labels to
the ordered triangle \((01,02,12)\) leaves seven stabilizer orbits for
the label of the distinguished cap edge on either shore.  Gluing the
two rooted three-poles converts equality, one-point intersection, and
disjointness of their root-label sets exactly into
\(AA,AT_\pi,T_\pi T_\pi\).

Consequently the exceptional four-type signature in its missing
\(AT_i\) orientation forces both shore root signatures to be the same
singleton, one of \(\{01,02,12,34\}\).  Its other two orientations
force a precise cross-intersection relation.  The exceptional five-type
signature forces one of only thirteen unordered disjoint root-signature
patterns.  A literal \(127^2\)-pair enumeration and an independently
written JavaScript replay agree with the human classification.  This
reduces the five-pole interface but does not eliminate the surviving
rooted three-pole signatures.  See
`docs/exceptional-cyclic-three-root-signature-factorization.md`.

## Independent order-18 exceptional four-pole census

Audit date: **2026-07-27**.

Two algorithmically independent classifiers have now exhausted all
\(4\,159\,098\) connected simple order-18 graphs with exactly four
degree-two vertices and all remaining vertices cubic.  One classifier
uses incremental CaDiCaL; the other is a direct finite-domain solver
with generalized arc consistency and recursive branching.  Per
implementation they made \(16\,453\,323\) exact signature queries,
obtained \(15\,295\,709\) satisfiable answers, and found no boundary
signature in the fixed five-colour \(D_5\) model equal to any of the
six ordered exceptional masks.

A third streaming checker validated every transcript row and rejected
observed-but-unqueried masks or any exceptional flag.  The SAT and
non-SAT transcript SHA-256 digests agree separately on all eight
canonical `geng` shards.  An earlier preparatory run was discarded
without a conclusion after audit found that transcript mode did not
increment the classifier's auxiliary hit counter; the retained sources
fix that issue and add an independent streaming guard.  The complete
finite statement, hashes, artifacts, and replay are in
`search/four-pole-order18-exceptional-20260727/`.

This excludes exceptional signatures only in the stated finite simple
scope.  It neither proves the universal exceptional-signature
conjecture nor resolves Five-CDC.

## Complete order-20 exceptional cap census

Audit date: **2026-07-27**.

The simple-cap reduction makes a much smaller complete order-20 search
possible.  Two independent filters agree byte-for-byte on all \(1\,388\)
bridgeless non-Tait connected simple cubic caps among the \(510\,489\)
canonical cubic graphs.  Deleting every independent edge pair gives
\(520\,500\) four-pole rows.  Independent SAT and direct finite-domain
classifiers make \(2\,074\,239\) exact mask queries apiece, agree on
every per-pole decision transcript, and find zero exceptional
signatures.

A third verifier decodes all retained caps, checks connectedness,
cubicity, every single-edge deletion, and non-Taitness by
perfect-matching complements; reconstructs all independent-edge
deletions byte-for-byte; rebuilds the input shards; and verifies both
classifier streams.  Combined with the proved cap reduction, this gives
the finite theorem that no bridge-free connected simple
terminal-distinct order-20 four-pole has either exceptional exact
five-colour \(D_5\) signature.  The package is
`search/four-pole-order20-cap-20260727/`.

This order-20 statement alone says nothing about order 22 or higher,
repeated terminals, nonsimple cores, or multigraphs, and it is not a
Five-CDC resolution.

## Complete order-22 exceptional cap census

Audit date: **2026-07-27**.

The cap-reduction frontier has now been extended by one complete order.
The canonical source contains all \(7\,319\,447\) connected simple cubic
graphs of order 22.  Independent direct-colouring and
perfect-matching/even-complement filters agree byte-for-byte on the
\(12\,892\) bridgeless non-Tait caps among the \(7\,187\,627\)
bridgeless graphs.  Deleting every independent edge pair gives exactly
\(5\,956\,104\) terminal-distinct four-poles.

Independent CaDiCaL and direct finite-domain classifiers make
\(23\,747\,129\) exact-signature queries apiece, obtain
\(22\,764\,574\) satisfiable answers apiece, agree on every one of eight
streamed transcript digests, and find zero exceptional signatures.
The retained full pole stream has SHA-256
`cf7a19244912c746c1ef1247a4b45e6ad1df647feaa4251e59db381351b5db46`.

A separate standard-library verifier checks the canonical-source
identity and source indices, both filter outputs, every retained cap,
the complete \(5\,956\,104\)-row pole expansion byte-for-byte, all
eight shard digests, and both decision ledgers.  Together with the
proved simple-cap reduction, this proves:

> No bridge-free connected simple terminal-distinct order-22 four-pole
> has either exceptional exact boundary signature in the fixed
> five-colour \(D_5\) model.

Thus any exceptional pole in this simple terminal-distinct scope has
even order at least 24.  The theorem does not cover repeated terminals,
nonsimple or multigraph cores, arbitrary-colour signatures, or higher
orders, and it does not resolve Five-CDC.  The frozen package is
`search/four-pole-order22-cap-20260727/`.

## Order-24 strict-snark full-signature probe

Audit date: **2026-07-27**.

The retained Snarkhunter 2.0b source contains 38 distinct strict snarks
of order 24.  An independent standard-library checker verifies their
connected simple cubic, girth-five, cyclically-four-edge-connected, and
non-Tait premises, but does not independently regenerate the canonical
source list.  Deleting every independent edge pair produces 21,204
terminal-distinct four-poles.

The independent CaDiCaL and direct finite-domain boundary classifiers
made all 212,040 exact-boundary queries on this stream.  Their full
classification tables agree byte-for-byte, and every row has mask
`0x3ff`: all ten fixed-five \(D_5\) boundary types are realizable.
The verifier reconstructs every deletion pole and checks both tables
row by row.  The frozen package is
`search/four-pole-order24-strict-cap-probe-20260727/`.

This is exact finite evidence on the retained strict-snark source, not
a complete census of all order-24 non-Tait caps.  Source completeness
still relies on the documented Snarkhunter run.  In particular, the
result does not prove that cyclically-four-connected caps universally
have full signature and does not resolve Five-CDC.

## Complete cyclically-four order-24 cap classification

Audit date: **2026-07-27**.

The order-24 search has now been enlarged from the 38 girth-five strict
snarks to all 155 cyclically 4-edge-connected class-2 simple cubic graphs
produced by the documented Snarkhunter girth-four run.  The girth-four
scope is complete for this cap class: a cyclically 4-edge-connected simple
cubic graph of order 24 cannot contain a triangle, since the triangle and
the cyclic complement would form a cyclic three-cut.

Deleting every independent edge pair gives 86,490 poles.  Independent
CaDiCaL and direct finite-domain classifiers agree byte-for-byte on all
864,900 exact queries per implementation, and every pole has full mask
`0x3ff`.  A separate verifier checks all graph premises, reconstructs every
deletion, and checks both tables row-by-row.  Source completeness relies on
Snarkhunter and its option semantics.

Combining this complete cyclically-four cap classification with the proved
exceptional-atom descent, the cyclic-three cap elimination through order
36, the simple-cap theorem, and the complete order-22 census yields a
finite theorem: no bridge-free connected simple terminal-distinct
four-pole of order at most 24 has either exceptional exact fixed-five
signature.  Any such pole has even order at least 26.  The proof chain and
artifacts are in `search/four-pole-order24-cyclic4-cap-20260727/`.

This advances only the finite exceptional-pole frontier.  It does not prove
the universal exceptional-signature conjecture or Five-CDC.

## Order-26 strict-snark full-signature probe

Audit date: **2026-07-27**.

The same two-implementation stress test has now been extended to the 280
strict snarks of order 26 produced by the documented Snarkhunter 2.0b
command.  Deleting every independent edge pair gives 185,640
terminal-distinct four-poles.  The CaDiCaL implementation classified the
whole stream, while the independently written direct finite-domain
implementation classified eight consecutive 23,205-row shards.

Their concatenated TSV tables agree byte-for-byte.  All 1,856,400 exact
boundary queries per implementation are satisfiable, so every retained
pole again has the full fixed-five mask `0x3ff`.  A separate
standard-library verifier checks the 280 graph premises, reconstructs all
185,640 poles, and validates both tables row-by-row.

Completeness of the 280-graph source relies on Snarkhunter and its option
semantics; this is not a census of all order-26 non-Tait caps or a universal
full-signature theorem.  The frozen package is
`search/four-pole-order26-strict-cap-probe-20260727/`.

## Complete cyclically-four order-26 cap classification

Audit date: **2026-07-27**.

The order-26 search has now been enlarged from the 280 girth-five strict
snarks to all 1,297 cyclically 4-edge-connected class-2 simple cubic graphs
produced by the documented Snarkhunter girth-four run.  As at order 24,
this is the complete intended cap class subject to Snarkhunter: a triangle
and its cyclic complement would form a cyclic three-edge cut.

Deleting every independent edge pair gives 859,911 terminal-distinct
four-poles.  The independent CaDiCaL and direct finite-domain classifiers
each make 8,599,110 exact boundary queries.  Their complete tables agree
byte-for-byte, every query is satisfiable, every pole has mask `0x3ff`,
and there are no exceptional hits.

A solver-independent verifier checks all 1,297 source records for order,
distinctness, cubicity, connectedness, triangle-freeness, cyclic
4-edge-connectivity, and non-Taitness.  It reconstructs all 859,911
deletion poles byte-for-byte and checks both tables and all sixteen shard
logs.  The replay reproduces the committed report exactly.

This proves the complete intended classification of cyclically
4-edge-connected non-Tait caps at order 26.  A later audit found that the
claimed reduction from every exceptional pole through order 26 to this cap
class used an invalid one-sided base-pair inference: a containing root
signature can add equality to a base-pair-versus-shore relation that was
intersection-only.  Therefore the former global exceptional-pole
lower bound of 28 is withdrawn.  The complete finite package remains
`search/four-pole-order26-cyclic4-cap-20260727/`; its cap classification
and verifier are unaffected.  Canonical source completeness still relies
on Snarkhunter and its option semantics.  This is not a universal
exceptional-signature theorem and does not resolve Five-CDC.

## Rooted three-pole base-pair frontier through order 17

Audit date: **2026-07-27**.

For a rooted cubic three-pole with connector triangle
\((01,02,12)\), define the three base pairs
\[
 \{12,03,04\},\qquad \{02,13,14\},\qquad \{01,23,24\}.
\]
Complete exact signatures through rooted order 13 show that these are
the three inclusion-minimal nonempty nonbridge masks.  Dedicated
adaptive screens have now extended the containment statement through
order 17.  On all \(654\,676\) canonical order-17 cores, independent
direct-CSP and incremental-SAT implementations test all
\(15\,645\,623\) nonbridge roots and report \(337\,059\) empty
signatures, \(15\,308\,564\) signatures containing a base pair, and
zero violations.  The corresponding streamed transcript digests agree
on all eight shards, with \(52\,216\,251\) solver calls per
implementation.

Thus base-pair closure is a finite theorem through rooted order 17.
A complete \(3\times7\) orbit table shows that the base pair itself
against any nonempty invariant signature never has any of the three
exceptional relations.  This does not remain true after replacing the
base pair by an arbitrary containing root signature.  Explicitly,
\[
 R=\{12,03,04,01\},\qquad S=\{01\}
\]
are invariant, \(R\) contains a base pair, and
\(\operatorname{rel}(R,S)=\{\mathsf E,\mathsf I\}\).
Consequently the order-17 theorem on one shore excludes the
equality-only and disjointness-only cyclic-three relations through total
order 36, but not the mixed \(\{\mathsf E,\mathsf I\}\) orientation of
\({\cal E}_4\).  If both shores are within the finite frontier, their two
base pairs do exclude all exceptional relations.  The corrected
conditional proof and finite artifacts are
`docs/rooted-three-pole-base-pair-closure-target.md` and
`search/rooted-three-pole-frontier-20260727/`.

## Tait-cap closure of the rooted three-pole target

Audit date: **2026-07-27**.

The rooted base-pair target now has an unbounded human-checkable positive
class.  If capping the three connectors by one vertex gives a
three-edge-colourable cubic graph, map its three Tait colours to
\(01,02,12\).  For any proper cycle through the nonbridge root, translating
the cycle labels by \(0123\) and \(0124\) preserves the \(D_5\) constraint
and realizes the two mixed labels aligned with the root's original
triangle label.  These three root values are exactly one base pair.

One Tait cap therefore excludes the equality-only and disjointness-only
root relations; two Tait caps exclude all three exceptional relations.
The mixed \(\{\mathsf E,\mathsf I\}\) relation is not excluded
one-sidedly.  Under the minimal simple-cap hypotheses, and assuming the
cap is simple, bridgeless, and has no cyclic two-edge cut.  An elementary
cubic cut argument therefore makes it 3-connected, so the published
three-sum decomposition applies and its factor tree is a path between the
two cap edges.  Both endpoint
factors are non-three-edge-colourable for \({\cal E}_5\); for
\({\cal E}_4\), a Tait endpoint can survive only at a mixed-orientation
end cut and forces a two-label restriction on the opposite root
signature.  The corrected proof is in
`docs/rooted-three-pole-tait-cap-closure.md`.

This is a universal structural reduction, not the full base-pair theorem:
the case of non-Tait shore caps remains open.

## Cyclically-four endpoint base-pair frontier through factor order 26

Audit date: **2026-07-27**.

The non-Tait endpoint case is now classified through factor order 26.
Snarkhunter supplies respectively \(6,31,155,1297\) triangle-free
cyclically 4-edge-connected non-Tait simple cubic factors of orders
\(20,22,24,26\).  Deleting every vertex gives 38,244 rooted cores.
Independent incremental-CaDiCaL and direct finite-domain implementations
test all 1,360,452 nonbridge roots in 4,157,844 solver calls each.  Their
complete transcripts agree byte-for-byte; every row contains a base pair
and there are no empty rows or violations.  The independent verifier
reconstructs all source premises, cores, roots, decisions, shard logs, and
the committed report.

Together with the rooted-order-17 theorem and the human Tait-cap theorem,
every endpoint factor of order at most 26 has base-pair closure.  For the
equality-only and disjointness-only cyclic-three relations, one endpoint
base pair is already impossible, so both endpoint factors have order at
least 28 and the cap has order at least 54.

The original one-sided inference did **not** eliminate the mixed
equality/intersection relation.  Base pairs in endpoint factors need not
remain the three distinguished base pairs after transport through a path.
The later endpoint-fork lift below preserves their fork shape and supplies
the missing two-sided argument.  The endpoint theorem and full finite
package are in
`search/rooted-three-pole-nontait-endpoint-frontier-20260727/`.

## Triangle induction for the mixed cyclic-three branch

Audit date: **2026-07-27**.

A new human reduction narrows the mixed branch to triangle-free
3-connected shore caps.  Along a three-sum factor path, an exposed
triangle is an endpoint \(K_4\) factor.  Contracting one at the connector
end maps the three base pairs by the explicit table
\[
                       P_0\mapsto P_0,\qquad
                       P_1\mapsto P_2,\qquad
                       P_2\mapsto P_1.
\]
A triangle through the root permits three distinct root labels.  Thus,
assuming base-pair closure for triangle-free caps through order \(N\),
every nonempty path-rooted cap signature through \(N\) contains a
**fork triple**
\[
                         \{qr,ps,pt\},
\]
where \(p,q,r,s,t\) are the five distinct coordinates.  Coordinate
permutations preserve this shape.  This strengthened conclusion is
necessary: cardinality three alone is insufficient, since two copies of
\(\{01,02,12\}\) have the mixed equality/intersection relation.

If a fork triple lies on one side of a relation with no disjoint pair,
every label on the other side must meet all three fork labels, and the
only possibilities are the two labels \(\{pq,pr\}\).  The other shore's
own fork triple cannot fit in a two-element set.  For a cap of order at
most 26, both capped shores of one principal cut have order at most 24.
The triangle-free screen is now complete: two exact implementations
classify every one of the 10,824,084 proper roots in all 330,790
vertex-deleted cores from the 13,901 retained caps at orders 20, 22, and
24.  Every signature is nonempty and contains a base pair, and the
complete transcripts agree byte-for-byte.  The triangle induction
therefore proves the stronger whole-shore statement and eliminates the
mixed cyclic-three branch through cap order 26.  The endpoint-fork lift
in the next section remains stronger, since it combines with the
order-28 cyclically-four census to give the current lower bound 30.
The human proof, local table replay, and finite package are in
`docs/rooted-cap-triangle-induction.md` and
`search/rooted-three-pole-c3-cap-frontier-through24-20260727/`.

## Root-end fork lift and restored order-28 bound

Audit date: **2026-07-27**.

A base pair in a root-end factor transports through an arbitrary
three-sum path as a fork triple.  Fix one labelling of the rest of the
shore and let \(\alpha\) be its ordered triangle at the endpoint-factor
interface.  Normalize \(\alpha\) to \(01,02,12\).  Each of the three
endpoint base-pair labellings can then be inverse-normalized and glued to
the same fixed remainder.  The resulting whole-shore root labels are one
coordinate image of a base pair, hence a fork
\[
                              \{qr,ps,pt\}.
\]

Any two forks have an unequal intersecting cross-pair and a disjoint
cross-pair.  The human proof is short: the labels meeting all three members
of one fork form a two-element set, while the fork itself has three
members; and the only label having no unequal intersection with all three
members is the fork's distinguished independent edge.  A standard-library
replay checks all 30 forks and all 900 ordered fork pairs, obtaining 330
relations \(\{\mathsf I,\mathsf D\}\) and 570 relations
\(\{\mathsf E,\mathsf I,\mathsf D\}\).

The completed endpoint base-pair theorem through factor order 26 therefore
excludes the mixed cyclic-three relation whenever both cap-edge endpoint
factors have order at most 26.  A surviving mixed branch has at least one
endpoint factor of order 28 and cap order at least 30.  Equality-only and
disjointness-only still force both endpoint factors above 26 and cap order
at least 54.

Together with the complete cyclically-four cap census through order 26,
this soundly restores the simple terminal-distinct exceptional-pole lower
bound of order 28.  Any first order-28 exception must have a cyclically
4-edge-connected cap.  The complete proof and literal replay are in
`docs/rooted-cap-end-factor-fork-lift.md`.  This is a fixed-five
exceptional-signature result, not a resolution of Five-CDC.

## Order-28 cyclically-four classification and scoped order-30 bound

Audit date: **2026-07-27**.

The retained Snarkhunter source contains all 12,517 documented
cyclically 4-edge-connected non-Tait simple cubic caps of order 28.
Deleting every independent edge pair gives 9,725,709 terminal-distinct
four-poles.  For every pole, a certificate-producing CaDiCaL run emits
two complete \(D_5\)-labellings: boundary orbit 0,
\((01,01,01,01)\), and boundary orbit 2,
\((01,01,23,23)\).  All eight shards finished with status zero and
zero missing witnesses, for 19,451,418 displayed labellings.

These two positive witnesses exclude all six exceptional exact masks
without any UNSAT inference.  Masks `0x02b`, `0x053`, and `0x119` omit
orbit 2; masks `0x2e4`, `0x3a4`, and `0x3c4` omit orbit 0.  The package
verifier reconstructs every cap deletion and checks every displayed
label at every vertex.  It independently confirms the full source,
pole, witness, log, and status totals and the uncompressed stream
digests.

The root-end fork theorem already puts every cyclic-three exceptional
cap at order at least 30.  The earlier exact classifications eliminate
the cyclically-four cases through order 26, and this computation
eliminates order 28.  A terminal-distinct cubic four-pole has
\(3n-4=2m\), hence even order.  Therefore the scoped vertex-minimal,
two-cut-reduced, bridge-free, connected, simple, terminal-distinct
fixed-five exceptional-pole lower bound is now order 30.

The finite theorem, human mask table, replay, and explicit certificates
are in `search/four-pole-order28-cyclic4-cap-20260727/`.  Canonical
source completeness and cyclic-four provenance rely on the retained
Snarkhunter run.  This does not prove that exceptional poles never
exist, does not cover multigraph or repeated-terminal poles, and does
not resolve Five-CDC.

## Elliptic quadratic-flow reformulation

Audit date: **2026-07-27**.

Let \(V\) be the even-weight subspace of \(\mathbb F_2^5\), and put
\[
 q(x)=\sum_{i<j}x_ix_j .
\]
On \(V\), the anisotropic vectors \(q(x)=1\) are exactly the ten
weight-two vectors.  Therefore the standard Five-Cycle Double Cover
problem is exactly the existence of a \(V\)-flow taking only
anisotropic values.  Equivalently, it asks for a nowhere-zero
\(\mathbb F_2^4\)-flow whose avoided nonzero values contain a binary
five-circuit.  This is a human-checkable change of language, not a
solution and not an orientability statement.  The exact proof,
including loops and parallel edges, is
`docs/five-cdc-elliptic-quadratic-flow-model.md`.

## Fano component-parity lift

Audit date: **2026-07-27**.

The existing quotient-lift theorem admits a particularly concrete
elliptic normal form.  In
coordinates
\[
             q(x,y,t,z)=x+y+xy+tz,
\]
let \(L\) be the three nonzero vectors with \(t=0\), and let
\(r=(0,0,1)\).  For a nowhere-zero \(\mathbb F_2^3\)-flow \(f\), a
binary cycle \(C\) lifts \(f\) to an anisotropic four-flow exactly when
\[
             M_r\subseteq C\subseteq M_r\cup M_L.
\]
Such a cycle exists exactly when every component of the \(L\)-valued
subgraph contains an even number of vertices of \(\partial M_r\).
Conversely, quotienting any anisotropic four-flow by a nonzero singular
vector yields this form.  Hence this component-parity condition, for
some \(f,L,r\), is equivalent to standard Five-CDC.  It is the
one-forced-value version of Section 6 of
`docs/proof-agent-audit.md`, not a logically new characterization.

The universal fixed-flow and one-switch versions were already known
inside this project to be false.  The eight-vertex fixed-flow example
in `docs/proof-agent-audit.md` fails every line, and the ten-vertex
example in `docs/flow-switch-audit.md` remains bad after every one
elementary circuit switch but has an explicit two-switch repair.  The
normal-form proof is
`docs/five-cdc-fano-component-parity-lift.md`.

This is an exact reformulation and a narrowing of the flow-selection
obligation, not a resolution.

## Five-point restriction of the eight-coordinate lift

Audit date: **2026-07-27**.

The new eight-coordinate triangle construction can be restricted to five
coordinate points without leaving any unclassified local cases.  After a
translation, every five-set in \(\mathbb F_2^3\) has the form
\[
                         \{0\}\dot\cup(a+L)
\]
for one uniquely determined Fano line \(L\).  At a cubic vertex whose
three incident flow values form \(L\), four local coordinate triangles fit
inside this five-set.  For each of the other six possible local Fano
lines, exactly one triangle fits.

The resulting pair shapes are forced: an \(L\)-valued edge has both
coordinate labels in \(a+L\), while an outside-valued edge has pair
\(\{0,f(e)\}\).  Summing coordinate parity over an \(L\)-component gives
exactly the component-parity test above.  Conversely, that test constructs
the compatible restricted triangles.  Thus coordinated eight-to-five
compression is precisely the existing flow-and-line selection problem;
there is no additional local merge choice that could evade it.

The human proof is
`docs/five-cdc-five-point-triangle-list-lift.md`.  Independent Python and
JavaScript checkers enumerate all \(56\cdot7=392\) five-set/line cases and
agree on 56 four-choice cases and 336 unique-choice cases.  This sharpens
the interface with the eight-coordinate proof but does not establish that
a suitable flow and line always exist.

## Unbounded Fano-switch distance

Audit date: **2026-07-27**.

Recent nowhere-zero-flow reconfiguration theorems do not presently supply
the missing Fano component-parity step: the universal connectivity theorem
is for \(\mathbb F_2^8\), not the eight-element group
\(\mathbb F_2^3\), while the applicable \(\mathbb F_2^3\) theorem excludes
only frozen flows.

A new recursive family also proves that no constant number of connected
circuit switches can suffice.  At depth \(d\), a host has \(3^d\) protected
ports and every connected circuit meets at most \(2^d\) of them.  Grafting
the certified all-seven-bad block at each port gives a connected simple
bridgeless cubic graph of order \(15\cdot3^d-5\) whose displayed flow has
switch distance at least \(\lceil(3/2)^d\rceil\) from the Fano-good set, if
that set is reachable at all.  Every graph in the family is
three-edge-colourable and has an explicit three-cycle double cover.

The first 40-vertex member has exact distance two; an independently written
checker verifies both displayed switches and all component-parity rows.
This refutes bounded-radius domination only.  It does not refute eventual
good-flow domination inside every reconfiguration component and does not
refute Five-CDC.  The human proof and literature audit are in
`scratch/fano-multistep-reconfiguration-audit-20260727.md`.

## Full-signature cap hypothesis: scalar frontier

Audit date: **2026-07-27**.

Internal cyclic four-edge-connectivity of a proper terminal-distinct
four-pole does not force full fixed-five signature.  The explicit order-16
pole

```text
O????A?[BOI_g_Ao?kCo?
```

has exact mask `0x3fe`.  Its missing \(AA\) state has a short parity proof:
three terminals have one common neighbour, forcing three odd scalar
projections at that cubic vertex.  Every simple cap of this pole creates a
cyclic triangle cut, so the example does not refute the focused hypothesis
for deletion poles of cyclically-four-connected non-Tait caps.

For that focused geometry, a human lemma now proves that every component
outside the four endpoints of the prescribed independent cap edges has an
even number of attachments.  This removes the elementary scalar obstruction
to \(AA\).  The simultaneous lift remains exact and open: \(AA\) is
equivalent to an \(\mathbb F_2^2\)-flow whose zero set contains the
prescribed edge pair and whose complement packs two edge-disjoint boundary
joins.  The complete order-22, order-24, and cyclically-four order-26 cap
computations are positive, but they do not prove this universal
prescribed-zero packing statement.  Details are in
`scratch/fixed-five-d5-four-pole-full-signature-frontier.md`.

## Prescribed-\(AA\) rooted-minimum exchange frontier

Audit date: **2026-07-27**.

For a prescribed independent pair \(R=\{e,f\}\), let \(M\supseteq R\) be
an inclusion-minimal exact zero matching of an
\(\mathbb F_2^2\)-flow.  For each nonzero value \(c\), contract the
components induced by the two values different from \(0,c\), retaining
the edges of \(M\) as a quotient multigraph \(Q_c\).  A root-preserving
exchange argument proves that
\[
                              Q_c-R
\]
is a forest.  Equivalently, every quotient cycle uses a root edge and
the cycle rank of \(Q_c\) is at most two.  This is the correct rooted
analogue of the unrooted quotient-forest theorem; the stronger unrooted
three-colour \(T\)-join inequalities do not survive because their switch
removes the prescribed roots from the zero set.

The shortcut “every rooted cardinal-minimum support packs” is false even
in the focused domain.  The 22-vertex simple cubic cyclically
4-edge-connected non-Tait graph

```text
U??????_A?C?s?QCO`@S?AP?d??gG?d??B_??M??
```

has roots \(\{24,27\}\) and a rooted minimum exact zero matching
\(\{24,27,31\}\) which does not pack two boundary joins.  A three-edge
star forced into any candidate even cycle gives a one-vertex human
obstruction.  A displayed root-preserving neutral circuit switch sends it
to the packing minimum \(\{13,24,27\}\), with two explicit disjoint
\(T\)-joins.  Thus the surviving existential target must allow neutral
movement among rooted minima.

A standard-library verifier checks the host, all small cuts, non-Taitness,
rooted minimality, the local obstruction, the neutral switch, and both
target joins.  The complete retained order-22 focused audit finds a
packing minimum for all 14,322 independent pairs, while 352 pairs also
have nonpacking minimum choices.  The exact universal alternatives left
open are rooted-flow feasibility, a size-at-least-five component-parity
obstruction, an odd-\(K_{2,3}\) graft minor, or a proof that every rooted
minimum neutral component reaches packing.  Details are in
`scratch/focused-aa-rooted-minimum-frontier.md`.  None of these results
resolves Five-CDC.

## Prescribed-root deficiency-two and theta-core frontier

Audit date: **2026-07-27**.

Let \(R=\{e,f\}\) be two independent edges of a finite
3-edge-connected cubic graph, let \(U=V(e)\cup V(f)\), and put
\(H=G-U\).  A direct Tutte--Berge argument now proves the universal
bound
\[
                         \operatorname{def}(H)\le2.
\]
Indeed, if \(S\subseteq V(H)\) and \(t=o(H-S)\), every odd component has
at least three boundary edges, while all their boundary edges end in
\(S\cup U\).  Since \(|\delta(U)|\le8\),
\[
                         3t\le3|S|+8,
\]
so \(t-|S|\le2\).  Thus \(H\) either has a perfect matching or a maximum
matching missing exactly two vertices.

In the deficiency-two case, adjoining the roots to a maximum matching
and suppressing degree-two vertices in its complement leaves exactly one
of two cores: a theta with three parallel paths between the unmatched
vertices, or a loop--link--loop dumbbell.  The matching is the exact zero
set of an \(\mathbb F_2^2\)-flow exactly in the theta case.  In the
focused simple cyclically 4-edge-connected domain, every tight
Tutte--Berge barrier is rigid: all odd components are singleton
three-boundary shores, except possibly one five-boundary component when
\(|\delta(U)|=8\).  Moreover, every edge of a bad dumbbell link has a
nonroot matching chord across its cyclic cut.  Turning those chords into
a root-preserving alternating exchange that forces a theta remains open.

The theta conclusion is false under 3-edge-connectivity alone.  The
10-vertex graph

```text
I?BeeOwM?
```

with roots \(\{2,5\}\) has exactly four maximum matchings of \(G-U\), and
all four give a dumbbell.  A standard-library checker verifies the
graph, matchings, cores, and lower-order minimality.  This graph is
Tait-colourable and has a cyclic three-edge cut, so it is not a focused
counterexample and has no Five-CDC consequence.  The human proof and
replay are in
`scratch/prescribed-root-matching-deficiency-frontier.md` and
`scratch/prescribed-root-matching-deficiency-checker.py`.

The proposed local rotation-closure proof has now been tested at its
sharp limit.  The simple cubic graph

```text
Q???C@?GF?CKSOF?AQ?W_B_AA_?
```

with roots \(\{12,20\}\) is 3-edge-connected and non-Tait.  The graph
\(G-U\) has 40 maximum matchings; every one gives a dumbbell complement,
and the complete 384-edge elementary exchange graph on those matchings is
connected.  This rules out any argument using only non-Taitness, the
boundary-eight barrier counts, and closure under alternating paths and
circuits.  It still is not a focused counterexample: the roots together
with the canonical extra barrier edge form an explicit cyclic
three-edge cut.  The human obstruction is the one-line cut identity
\(\delta_{G-(R\cup P)}(X)=\{23\}\) for every maximum \(P\), and a
standard-library checker verifies all graph, matching, exchange, and
Petersen-contraction claims.  Thus global cyclic four-edge-connectivity
is an essential remaining hypothesis, not a dispensable technicality.
See `scratch/boundary-eight-rotation-closure-frontier.md`.

The focused theta choice has also been screened exactly on all
136,557,951 independent root pairs in the retained complete cyclically
4-edge-connected non-Tait corpora at every even order from 10 through
30.  Of these, 135,214,569 have deficiency zero.  Every one of the
remaining 1,343,382
deficiency-two pairs has at least one maximum matching with a theta
complement; no all-dumbbell pair occurs.  A separately written
standard-library replay reconstructs the same counts.  All
deficiency-two instances in this bounded corpus have
\(|\delta(U)|=8\), a finite clue rather than a theorem.  Human
alternating-path and symmetric-difference lemmas reduce the surviving
universal task to a rotation-closure statement for a
bridge-minimizing dumbbell matching.  That statement remains open.
The finite packages, including both complete replays, are
`search/focused-theta-choice-through28-20260727/` and
`search/focused-theta-choice-order30-20260727/`; the human frontier is
in `scratch/focused-theta-choice-census-frontier.md`.

### The all-singleton barrier branch already has a standard five-CDC

Audit date: **2026-07-27**.

The prescribed-root theta problem remains open in the all-singleton
Gallai--Edmonds branch, but that branch can no longer contain a
counterexample to the **standard** Five-Cycle Double Cover Conjecture.
The reason is an elementary oddness bound.

In this branch there is a partition
\[
                      V(G)=D\mathbin{\dot\cup}W
\]
with \(D\) independent and \(|W|=|D|+2\).  Cubic degree counting gives
\[
 2|E(G[W])|=3|W|-3|D|=6,
 \qquad\text{so}\qquad |E(G[W])|=3.                 \tag{S1}
\]
Choose one edge \(t\in E(G[W])\).  By Schönberger's edge-prescribed
strengthening of Petersen's theorem, a bridgeless cubic graph has a
perfect matching \(M\) containing \(t\).  Since \(D\) is independent,
\(M\) uses \(|D|\) distinct \(D\)--\(W\) edges to cover \(D\).  Only two
vertices of \(W\) remain, so \(M\) contains exactly one \(W\)--\(W\)
edge, namely \(t\).

The complementary 2-factor \(G-M\) therefore contains exactly the other
two \(W\)--\(W\) edges.  All its remaining edges cross \((D,W)\).  A
cycle is odd exactly when it contains an odd number of the two exceptional
edges.  If they lie on the same cycle there are no odd cycles; if they lie
on different cycles there are exactly two.  Hence
\[
                              \omega(G)\le2.          \tag{S2}
\]
Huck and Kochol's theorem then supplies a standard five-cycle double
cover (JCTB 64 (1995), 119--125,
DOI `10.1006/jctb.1995.1029`).

This proof closes the standard all-singleton branch, including both the
boundary-six and boundary-eight geometries.  It does **not** produce the
particular prescribed-root \(\mathbb F_2^2\)-flow needed by the fixed-five
gluing route.  Within the present deficiency analysis, a standard
counterexample can therefore survive only in the one-five-boundary
factor-critical-component branch.  The proof and the independent finite
root-insertion audit are in
`scratch/root-insertion-two-factor-frontier.md`.

## High-flow-resistance prescribed-\(AA\) theorem

Audit date: **2026-07-27**.

The focused prescribed-equal-label test has now been completed for every
independent edge pair of the reconstructed Mattiolo--Negrini--Pagani graphs
\(H_2,H_3,H_4,H_5\), whose certified flow resistances are \(2,3,4,5\).
Across orders 82, 122, 162, and 202 there are exactly 97,608 independent
pairs.

For every pair \(e,f\), an explicit fixed-five \(D_5\)-labelling assigns
the same label to \(e\) and \(f\).  Equivalently, every corresponding
deletion four-pole realizes boundary type \(AA\).  A greedy certificate
cover needs only 394 complete labellings: 79, 92, 103, and 120 for the four
graphs.  The independent verifier imports no SAT code; it checks every
vertex xor equation and reconstructs coverage of all 97,608 pairs.

Thus increasing flow resistance through five does not obstruct even the
strong prescribed-\(AA\) property on this family.  This is a finite theorem
for four retained graphs, not a universal cap theorem and not a Five-CDC
resolution.  The explicit certificates are in
`search/mnp-h2-h5-aa-deletion-probe-20260727/`.

## Minimum-zero exchange route: refutation and amplification

Audit date: **2026-07-28**.

The unrestricted assertion that some cardinality-minimum exact-zero
matching always extends to a matching/four-flow five-cover certificate is
false.  The independently replayed 130-vertex package has
\[
 r_f=r_M=5,\qquad \eta=6,
\]
where \(\eta\) is the least matching size in such a certificate.  Its two
lower bounds have LRATs accepted by `lrat-check` and CakeML `cake_lpr`;
the graph, positive witnesses, and resulting standard five-cover are
checked directly.  Thus this is a proof-strategy countermodel, not a
Five-CDC counterexample.

The gap is unbounded under identical rooted two-edge sums.  Shore parity
restores every flow and both binary cycles factorwise, with exact additivity
of the zero matching.  Conversely, identical minimum objects glue because
their root states agree.  Iterating gives connected simple bridgeless cubic
graphs \(G_n\) with
\[
 r_f(G_n)=r_M(G_n)=5\cdot2^n,\qquad
 \eta(G_n)=6\cdot2^n.
\]
The composition proof is elementary and human-checkable; a separate audit
checks all 195 possible roots in the first 260-vertex sum.  Every member
has a standard five-cover and the family has cyclic two-edge cuts.  See
`docs/minimum-zero-two-sum-amplification.md` and
`preprint/minimum-zero-exchange-gap/`.

## Four-cycle Fourier and strict Oum-switch frontiers

Audit date: **2026-07-28**.

Deleting one coordinate from a five-cover gives four binary cycles whose
edge columns have Hamming weight one or two.  For
\(A=\{x\in\mathbb F_2^4:\operatorname{wt}(x)\in\{1,2\}\}\), the exact
Fourier transform by dual Hamming weight is
\[
 (10,2,-2,-2,2).
\]
This yields a signed potential expansion for the number of five-covers.
The length-seven simplex code and the cographic cut code of \(K_6\) show
that analogous positivity is false for arbitrary coloopless binary and
cographic codes.  The graphic positivity statement remains exactly
Five-CDC.  See `docs/five-cdc-cycle-code-fourier-no-go.md`.

For co-occurrence graphs on at most eight vertices, a human critical-graph
argument proves
\[
 H\to R_5\quad\Longleftrightarrow\quad\chi(H)\le5.
\]
Thus the proposed general \(R_5\) compression of Oum eight-covers is
exactly ordinary five-colour merging, not a stronger escape.  In a
cyclically 4-edge-connected cubic graph, any three edges carrying one
common nonzero \(\mathbb F_2^3\)-flow value lie on a circuit; this removes
the precise noncyclable-triple mechanism of the unrestricted 46-vertex
countermodel.  It does not ensure that the circuit avoids the value used
for the switch.

The retained strict-snark screen sampled 5,000 nowhere-zero flows at
orders 28--36.  Exactly 2,245 were initially merge-bad, and every one has
a checked legal one-circuit repair.  The potential and repair decisions
are exact for each sampled flow, but the flow sample is not exhaustive and
no girth-ten strict snark was tractable.  The human proof and replay are in
`scratch/strict-oum-one-switch-audit-20260728.md`.

A separate seeded construction joined disjoint five-cycles by random
cross-block perfect matchings, then filtered for connected bridgeless
non-Tait graphs.  Across 600,000 generated graphs at orders 20, 30, and
40, it found 1,606 snarks; all 1,606 had direct standard Five-CDC SAT
models whose edge weights and vertex XOR equations were checked
semantically.  This is a noncanonical random family screen with possible
duplicates, not a census.  The fixed seeds, counts, code hash, and
limitations are in
`scratch/random-c5-factor-fivecdc-search-20260728.json`.

## APX and square-local Jaeger route eliminations

Audit date: **2026-07-28**.

The affine pair-exchange axiom (APX) is false even on a simple girth-five,
cyclically 4-edge-connected 36-vertex snark. The exact checker exhausts all
221 perfect matchings and all 198 relevant binary-cycle packing queries;
none of the 32 distinct affine-compatible pairs packs. This is not a
FiveCDC counterexample: the graph has a directly checked standard
five-cover, and 6,699 of 9,532 legal circuit switches repair the displayed
flow. The broader reduced one-switch lemma remains open. See
`scratch/fano-apx-countermodel-order36.md`.

A separate solver-free no-go closes fixed-state square lifting. On graph6
`G?zTb_`, root zero, one good state has exactly 72 legal local lifts and
none is good in any coordinate. An alternate state for the same
graph/root/smoothing pair does lift. Both order-six graphs pass the stronger
statewise property, and all 672 order-eight whole-fibre instances admit a
jointly chosen good state and lift. Hence the whole-fibre square reduction
also remains open. See
`scratch/jaeger-star-square-any-coordinate-lift-no-go.md`.

Together these results eliminate two plausible short proofs without
changing the resolution status. The sharp Jaeger obligation is still a
universal full same-level-component descent theorem, or an equivalent joint
tree-packing/parity selection theorem.

For any set \(S\) of simultaneous nonroot triangle expansions, the exchange
graph now has the human-proved factorization
\[
\mathcal X(G^S,r)\cong\mathcal X(G,r)\square
\operatorname{Cay}(S_3,\mathcal T)^{\square|S|}.
\]
The defect is not constant on the \(S_3\) sheets, so this is structural
rather than a descent proof. Exhaustive two-triangle searches on two
adversarial order-16 states find no strict trap (minimum neutral degrees 14
and 7), and randomized order-16, order-36, and triangle-expanded stress
tests also escape. Only the product identity is a theorem; the latter
results are finite or exploratory. See
`scratch/jaeger-simultaneous-triangle-lift-plateau-search.md`.

## Direct reductions, square frontier, and sorted-profile no-go

Audit date: **2026-07-28**.

The mandated direct exact-two/parity encoding was run on all 7,654 retained
canonical order-40 strong snarks and on five derived layers at orders
48, 56, 64, 80, and 160.  All 45,924 instances were SAT and every model was
checked against the raw edge-weight and vertex-XOR semantics.  No target
UNSAT result or proof certificate was produced.

Two infinite search directions are now pruned by proofs rather than finite
extrapolation:

1. FiveCDC pulls back along any finite graph covering, including loops and
   parallel edges under the incidence/dart convention.
2. The Petersen four-pole obtained by deleting adjacent vertices extends
   every boundary multiset \(q,q,r,r\) of pair labels, for every port
   placement.  A 13-row human table and an independent exhaustive checker
   cover all 550 labelled boundary assignments.

Neither result resolves FiveCDC; they show that positive bases cannot be
turned into counterexamples by those two operations.

For square expansion, a fixed five-labelling extends if and only if the two
deleted pair labels are equal or disjoint.  The stronger whole-fibre
state-and-lift statement has zero failures in complete solver-free censuses
through downstairs order 12: 6,300 instances at order 10 and 53,352 at
order 12.  Certificate censuses add all 572,880 labelled instances at
order 14 and all 7,737,408 at order 16; separately written checkers
reconstruct every witness.  The order-16 corpus covers 2,828 canonical
simple three-edge-connected graphs, 45,248 labelled roots, and 309,472
distinct selected downstairs states.  All three order-18 snarks under the
explicit simple/3-edge-connected/girth-at-least-five/non-Tait convention
also pass all 12,474 root/pair instances.  A future countermodel in the
complete simple three-edge-connected cubic class therefore has downstairs
order at least 18.

Finally, the sorted seven-defect profile is not a one-step descent
potential.  On the explicit order-36 state, all 867 reciprocal candidates
are reconstructed; 63 are legal, with 0 lexicographically lower, 13 equal,
and 50 higher neighbours.  A two-exchange path within \(d_{\min}=2\)
reaches defect zero, so the full same-level-component theorem survives.

Two further exact quantifier barriers are now frozen.  In every FiveCDC,
the labels on a three-edge cut form, up to \(S_5\),
\(\{0,1\},\{0,2\},\{1,2\}\), so any two intersect once.  On the triangular
prism this prevents the two selected square-smoothing edges from ever
having equal or disjoint labels, although an exact-good star state and
exact-good square-local lift both exist.  Hence fixed-label selection
cannot prove the still-open whole-fibre implication.

For descent, a literal order-40 state has exact plateau escape distance
four.  Its complete level-two ball through radius three has layer sizes
\(1,13,108,836\); all 1,037,514 candidate swaps and 67,392 legal oriented
arcs are independently reconstructed.  No descending boundary occurs
before layer three, and an explicit fourth exchange reaches defect zero.
This refutes only every radius-three strengthening.  The full unbounded
same-level-component theorem remains open.

The natural averaging repair is also false.  Two adjacent states with the
same ordered profile \((8,2,8,8,6,10,10)\) have 65 and 63 legal neighbours,
but the graph Laplacian of total defect is \(+10\) at one and \(-14\) at
the other.  Hence total defect is neither universally subharmonic nor
superharmonic, and its Laplacian is not determined by the current profile.
The universal plateau divergence identity only moves the unknown sign to
the exterior boundary; a surviving proof must retain fundamental-cycle and
quotient-boundary incidence data.
See the exact notes and independent checkers under `scratch/`.

## Full-boundary Heawood four-pole reduction

Audit date: **2026-07-28**.

Deleting two adjacent vertices of the Heawood graph gives the frozen
12-vertex four-pole `KhEGHC@AI?_P`, with ordered ports
\((0,3,8,11)\).  Its proper core is simple, connected, bridgeless, and has
girth six.  Every ordered four-tuple of pair labels with xor zero extends
through the pole.  There are 640 such boundary words; ten displayed orbit
representatives and their internal labels cover them under all 120
coordinate permutations.  The independent checker validates the edge
table, graph metadata, all internal parities, orbit sizes, and exact
coverage.

It follows that replacing two independent edges of a FiveCDC-positive cubic
graph by this pole preserves standard FiveCDC for every one of the \(4!\)
port bijections.  A separate edge-by-edge lemma proves that the substitution
also preserves bridgelessness.  This is a non-covering, non-Petersen
reducible configuration.  It does not imply that every prospective
counterexample contains such a pole, so FiveCDC remains unresolved.

## Minimum-order cube full-boundary four-pole

Audit date: **2026-07-28**.

Deleting adjacent vertices \(0,1\) from the cube leaves the ordered ports
\((2,3,4,7)\) and the seven-edge proper core
\[
(2,3),(2,6),(3,5),(4,5),(4,7),(5,6),(6,7).
\]
The core is simple, connected, and bridgeless.  A ten-row human certificate
has the same orbit-size vector
\[
10,60,60,60,30,120,120,30,120,30
\]
as the Heawood certificate, and its coordinate-permutation orbits cover
exactly all 640 xor-zero boundary words.  A separately written
standard-library checker reconstructs the graph and verifies every row,
orbit, and word.

The order is sharp in the connected simple terminal-distinct cubic
four-pole class.  If the proper core has \(n\) vertices and \(m\) edges,
then \(2m=3n-4\), so \(n\) is even and \(n\ge4\).  At \(n=4\) all proper
vertices have degree two; connectedness and simplicity force \(C_4\).
This is the \(K_{3,3}\)-minus-adjacent-vertices pole, whose independently
checked relation has 580 of 640 admissible words and misses exactly the
60-word orbit represented by `02 02 03 03`.  Hence the six-vertex cube
pole is minimum.

The generic insertion and bridgelessness lemmas apply for every port
bijection.  This is a sharper local reduction than the Heawood result;
the Heawood pole remains distinct for its girth-six core.  Neither
configuration is known to be unavoidable, so this theorem does not resolve
FiveCDC.

## Exact signed-partition algebra for clean Fano lines

Audit date: **2026-07-28**.

For a fixed nonzero functional \(\mu\), a cut shore is now represented by
the partition of its line-valued boundary incidences into internal line
components, together with one affine-color defect bit on each block.
Closed shore components must already have zero defect.  On gluing, make a
bipartite multigraph whose vertices are the two shore partitions and whose
edges are the line-valued cut edges.  The global line is clean exactly when
both shore states are admissible and the xor of the block bits is zero in
every component of this bipartite graph.

This is an exact human-checkable composition theorem, not a heuristic.  For
\(m=0,1,2,3,4\) line-valued terminals, boundary conservation leaves
\[
                         1,\ 1,\ 3,\ 11,\ 47
\]
signed states, and respectively
\[
                         1,\ 1,\ 7,\ 79,\ 1283
\]
compatible ordered pairs for either fixed total parity.  The checker
reconstructs the tables, every covering binary three-space of Petersen, all
29,750 Petersen flow/functional/cut comparisons, and 546 diamond-interface
comparisons in the unbounded-component family through order 322.

The richer state is necessary.  Two explicit clean \(K_4\) cap flows have
two-terminal states \((0,0)\) and \((1,1)\).  Gluing their cap ends produces
an eight-vertex simple bridgeless cubic graph on which the selected line is
dirty.  The same graph has an explicit Tait/FiveCDC witness.  Thus
cap-by-cap fixed-flow induction is unsound unless the full signed
connectivity states are aligned.  This freezes a proof-strategy no-go; it
does not obstruct changing the shore flows and does not resolve the
four-pole or FiveCDC selection problem.  See
`scratch/fano-clean-line-signed-partitions-20260728.md`.

## Three-cut lock in the order-18 six-bad Fano flow

Audit date: **2026-07-28**.

The order-18 flow on
`Q???C@?K@O@aDAw?GW?J?_g?Y??` has now been corrected from an exploratory
cyclically-4 description.  Its graph has the cyclic three-cut consisting
of edge ids \(14,18,26\), namely
\((2,13),(5,15),(6,17)\).  The two connected shores each have nine
vertices and twelve induced edges.

Deleting the endpoints of all 27 edges and directly enumerating each
1024-element binary pole cycle space gives exact completion-sound local
UNSAT profiles.  The twelve deletions inside one shore have profile
\(\{4,5,6\}\), the twelve inside the other have profile
\(\{1,3,7\}\), and the three cut-edge deletions have empty profile.
Every deletion with a nonempty profile retains the opposite cyclic shore
behind a three-boundary.  Therefore any multi-pole completion using these
local obstructions has a cyclic three-cut; \(\mathrm{GL}(3,2)\) relabelling
does not alter the lock.

This closes the attempted construction of a cyclically 4-edge-connected
all-seven fixed-flow obstruction from this core.  It does not rule out a
different core and is not a FiveCDC result.  The human proof and
solver-independent checker are in
`scratch/fano-six-bad-threecut-lock-20260728.md`.

## Cyclically 4-edge-connected all-seven fixed-flow obstruction

Audit date: **2026-07-28**.

A different core and a completion-sound pole composition now produce the
previously missing auxiliary countermodel.  Two order-32 deleted-edge
four-poles, after explicit \(\mathrm{GL}(3,2)\) relabellings, have exact
local bad-functional profiles
\[
                    \{5,6,7\}\quad\hbox{and}\quad
                    \{1,2,3,4,5\}.
\]
Their four equal-valued ports glue to a simple cubic order-60 graph with a
nowhere-zero \(\mathbb F_2^3\)-flow.  A closed dirty factor component
inside a pole remains a global component under every completion, so the
profile union proves that none of the seven functional projections of
this fixed flow can be cleaned.

The solver-independent checker enumerates all \(2^{17}\) binary first
cycles for each pole/functional and decides the remaining linear system by
Gaussian elimination.  It reconstructs the graph, validates flow
conservation, checks every one of the 121,575 edge sets of size at most
three for cyclic separation, and validates an explicit standard FiveCDC.
Nauty independently gives the canonical graph6 record and confirms
nonplanarity.

This is not a FiveCDC counterexample.  It refutes the stronger assertion
that every chosen nowhere-zero three-bit flow has a clean projection even
in the cyclically 4-edge-connected domain.  The remaining exact obligation
is existential flow selection or repair, matching Hušek--Šámal Conjecture
3.19.  See
`scratch/fano-cyclic4-allseven-order60-20260728.md` and
`scratch/verify_fano_cyclic4_allseven_order60.cpp`.

## Direct Hušek--Šámal reconfiguration boundary

Audit date: **2026-07-28**.

For a nowhere-zero \(\mathbb F_2^3\)-flow \(f\), write
\(K_\mu=\{e:\langle\mu,f(e)\rangle=0\}\), and let \(d_\mu(f)\) count
the components of \(K_\mu\) containing an odd number of endpoints of
one affine value class.  Hušek--Šámal goodness is \(d_\mu(f)=0\) for
some nonzero \(\mu\).

The proposed radius-one theorem is false even in the strict-snark
domain.  A retained order-26 simple cubic cyclically 4-edge-connected
non-Tait graph of girth five has a nowhere-zero flow with profile
\((6,6,4,6,2,4,4)\).  Its value-4 class already packs two
edge-disjoint boundary joins.  A standard-library implementation
enumerates all 9,213 simple cycles and all 1,485 legal cycle--value
switches; none is good.  It also exhausts Tait colourings, validates
cyclic cuts of sizes at most three, and checks an explicit FiveCDC.  The
displayed flow has exact H--S distance two, with checked intermediate
profiles
\[
              (4,6,4,2,4,4,4),\qquad(4,6,4,0,6,4,4).
\]
Thus even an already packable state can require both components of the
packing-to-switch support; this closes only the radius-one proof route.

There is nevertheless a human packing-to-switch theorem.  If a value
class \(M_a\) has two disjoint \(\partial M_a\)-joins \(J_1,J_2\), take
\(\mu(a)=1\), \(F=\{e:\mu(f(e))=1\}\), and \(J_0=F-M_a\).  The even
subgraph \(C=J_0\triangle J_1\) avoids \(M_a\); switching \(a\) on its
simple-cycle components changes \(F\) to \(M_a\cup J_1\), whose
complement contains \(J_2\).  Hence a finite legal switch sequence is
H--S-good.  The order-60 one-cycle repair is a literal instance.

Seeded radius-two reconnaissance on all 280 retained strict order-26
snarks sampled 28,000 flows and repaired all 25,230 radius-one traps.
A second run on seven retained strong order-34 snarks sampled 700 flows
and repaired all 689 radius-one traps.  These are samples, not censuses.
The exact surviving problem is finite-radius or unrestricted
reconfiguration of all-seven-nonpacking flows, or direct existential
flow selection.  See
`scratch/husek-samal-one-switch-reduced-frontier-20260728.md`.

## Binary packing repair and its exact connectivity boundary

Audit date: **2026-07-28**.

For distinct Fano values \(t,b\), a binary repair chooses an even
subgraph \(X\) avoiding the current value-\(t\) class, switches \(t\) on
\(X\), and asks that the new value-\(b\) matching pack two disjoint
boundary joins.  The exact formulation uses switch variables and two
join variables.  The targets \(b\) and \(b+t\) are equivalent, reducing
the 42 ordered queries to 21 Fano point--line incidences.

This route survives the sound minimum-counterexample class but not
connectedness alone.  An adversarial order-36 state has only 14 of 21
repairing incidences.  Three linear relabellings partition all 21 failed
incidences.  Joining the three copies by two crossed cubic 2-sums gives
a connected simple bridgeless cubic graph of order 108 whose displayed
flow has no binary repair.

The combined selector-gated formula has 10,227 variables and 51,193
clauses.  Its LRAT is accepted by both `lrat-check` and the
CakeML-generated verified `cake_lpr`.  A separately structured checker
reconstructs the composition, flow, all CNF clauses, graph metadata, and
an explicit standard FiveCDC.  The graph has girth five and exactly two
cyclic 2-edge cuts, so it is not a FiveCDC counterexample and does not
refute the cyclically 4-edge-connected girth-ten repair conjecture.

On the positive side, a solver-free certificate on the retained
80-vertex cubic vertex-transitive girth-ten graph checks one binary
repair through explicit switch and join sets and constructs the resulting
FiveCDC.  Seeded samples found no repair failure in the reduced snark
controls, but those are not censuses.

See `scratch/fano-binary-packing-repair-frontier-20260728.md` and
`search/fano-binary-repair-connected-countermodel-108v-20260728/`.
