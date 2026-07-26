# Publication and novelty assessment

Date: **2026-07-26**.

## Verdict

The project now has a **preprint-worthy computer-free marked-graph
theorem** and a separate narrow negative result.  Neither resolves the
five-cycle double cover conjecture.

The stronger paper candidate is the four-mark theorem in
`preprint-four-mark-core/main.tex`.  Under universal Tait separation and
the exact marked cyclic-cut inequality, four independent marked edges
are contained in a binary cycle whose components each contain an even
number of marks.  More precisely, the proof produces one four-mark
cycle or two disjoint two-mark cycles.  An independently prompted Codex
agent audited the proof, including adjacent cap roots and the sequential
three-sum lift.  That is not independent human verification.

The theorem appears new from targeted searches, but its novelty is the
combination and exact marked hypothesis, not the imported ingredients.
Kempe switching, prescribed-edge circuit theorems, and cubic cyclic
three-cut decomposition are prior.  The appropriate claim is
“apparently new, pending expert literature review,” not categorical
priority.  If a human graph theorist verifies the proof and finds no
prior equivalent statement, this is suitable as a short research note.

The same marked-core framework now gives a second short,
computer-free corollary.  In the extremal size-four branch,
common-colour precolouring places the eight suppressed marks on eight
vertex-disjoint bichromatic circuits.  Restoring the suppressed vertices
makes them eight vertex-disjoint odd circuits in the ambient graph.
Ambient girth at least ten therefore forces order at least
\(8\cdot11=88\), improving the project's earlier bound \(68\).  The
proof is in `docs/kempe-transversality-and-eight-mark-girth.md`.  Its
novelty is also provisional: the argument is elementary, and an expert
must check whether the same bound is implicit in the
resistance/oddness literature.

That corollary has since been strengthened.  A solver-free
three-matching/Kempe argument and sharp girth overlap bounds exclude
ambient orders \(88,90,92,94\) in the connected extremal exact-zero
size-four branch, giving \(|V(G)|\ge96\).  A separately prompted agent
reconstructed the proof and generalized its local inequalities.  This
appears original to the project, but it is not yet a good standalone
headline: the statement depends on the project's full branch reduction,
and an explicit abstract order-\(96\) incidence matrix shows that the
method stops there.  It belongs as a substantial section or companion
note after a human specialist verifies both the reduction chain and the
overlap proof.

The rooted cap analysis also now has a clean computer-free lemma:
the inherited marked-cut inequality rules out every bridge after
deleting the forbidden cap.  A surviving failure is a 2-connected
subcubic four-way linkage obstruction whose three complementary
pair-cycle systems are cross-intersecting.  This is a useful sharpening
and may be new in this exact marked setting, but it remains a reduction
rather than closure of the rooted theorem.

The exact exceptional four-pole algebra is also potentially publishable
as part of the structural note.  Its most useful new claim is not the
ten boundary types, which are published, but the rooted terminal-join
interpretation and zero-free-shore exclusion in the project's
\(0,0,b,b\) branch.  The finite two-plus-two table is independently
replayed and supports a minimal-factor theorem.  This material should be
presented as progress toward, not a proof of, the published exceptional-
signature conjecture.

The strongest submission-ready mathematical core is the pair of explicit
connected countermodels in
`preprint-fano-one-switch/main.tex`:

1. a planar 40-vertex countermodel to domination of all displayed
   \(\mathbb F_2^3\)-flows by one connected-circuit switch into the
   successful \(T\)-join-packing set; and
2. a nonplanar 46-vertex countermodel showing that no compatible
   eight-coordinate potential cover for the displayed flow can be purely
   merged to five coordinates, even after one legal connected-circuit
   switch.

Both graphs positively have standard five-cycle double covers.  The
paper therefore closes two plausible proof strategies; it supplies no
counterexample to five-CDC.

Those countermodels remain independently preprint-worthy but are less
conceptually clean than the four-mark theorem and should stay in a
separate manuscript.

A further finite result is potentially suitable as a short example or
appendix, rather than as the main paper.  The package
`search/cyclic4-universally-separated-triple-n24-20260726/` gives a
24-vertex cyclically \(4\)-edge-connected, Tait-colourable graph with a
universally separated three-edge matching.  This refutes the project's
provisional low-cut atom conjecture.  The graph has girth four and
marked-subdivision girth five, so it does not enter the surviving
girth-ten five-CDC branch.  Its value is as a sharp warning against an
otherwise plausible structural lemma, not as evidence against five-CDC.

## What is prior

The following ingredients must not be advertised as new:

- the definition of a \(k\)-cycle double cover as at most \(k\) Eulerian
  subgraphs;
- the direct two-subset edge-label formulation;
- standard reductions to cubic graphs and snarks;
- the matching/nowhere-zero-4-flow characterization of five-CDC;
- cycle-supported nowhere-zero-flow reconfiguration;
- Oum's 2026 eight-coordinate cycle-double-cover construction; and
- the standard/orientable distinction.

Relevant primary sources include:

- Sang-il Oum, *A proof of the cycle double cover conjecture by OpenAI:
  An exposition*, arXiv:2607.16356;
- L. Esperet et al., *Nowhere-zero flow reconfiguration*,
  arXiv:2512.17342v4;
- A. Hoffmann-Ostenhof, *A note on 5-cycle double covers*,
  arXiv:1209.0096 / Graphs and Combinatorics 2013;
- S. Liu et al., *5-Cycle Double Covers, 4-Flows, and Catlin Reduction*,
  SIAM J. Discrete Math. 37 (2023), 253–267; and
- X. Li et al., *Non-separating cycles and 5-cycle double covers*,
  Discrete Mathematics 348 (2025), 114515.

## What appears new

Subject to expert literature confirmation, the narrow claims that appear
not to have been recorded are:

- the 5-CDC-specific successful-value subset of the
  \(\mathbb F_2^3\)-flow reconfiguration graph;
- the explicit connected 40-vertex one-switch countermodel;
- the pure-coordinate-merge obstruction for all compatible potentials;
- the rigid 12-vertex cap forcing a \(K_6\) in the coordinate
  co-occurrence graph;
- the explicit connected 46-vertex countermodel and its non-cyclable
  three-cap composition;
- the displayed two-sum closure mechanisms;
- the 24-vertex cyclically-four universally separated triple and its
  complete order-20-host \(K_4\)-sum census;
- the exact paired cyclic-cut formula and signed-holonomy formulation for
  the connected eight-mark branch;
- the order-\(88\) lower bound within the extremal size-four branch; and
- the low-surplus strengthening of that branch bound to order \(96\);
- the rooted bridge-elimination and cross-intersecting four-way linkage
  reduction under the inherited marked-cut inequality; and
- the rooted terminal-join interpretation, zero-free-shore exclusion,
  and exact two-plus-two minimal-factor theorem for the published
  exceptional four-pole pair; and
- the exact computations reported in the draft.

This is a strong provisional novelty assessment, not proof of priority.
Before submission, a graph-theory expert should search MathSciNet and
zbMATH and contact authors of the 2025--2026 flow and five-CDC papers.

## Human-checkability

The central 46-vertex result has a SAT-free proof:

- the graph and flow are explicit;
- a finite row reduction proves potential rigidity;
- the retained labels force all 15 pairs on a six-element set, hence a
  \(K_6\);
- a triangle argument proves that no connected circuit reaches all three
  caps; and
- an untouched rigid cap therefore survives every allowed one-circuit
  switch.

The proof is written in
`search/fano-pure-merge-one-switch-countermodel-46v-20260726/HUMAN-PROOF.md`.
The independent checker enumerates 128 compatible potentials and reports
zero five-colourable co-occurrence graphs.  It is a useful replay, but it
is also AI-written and is not independent human verification.

The four-mark theorem, order-\(88\) equality exclusion, low-surplus
order-\(96\) branch bound, and rooted bridge reduction are fully
human-checkable line by line and use no finite computation.  The
order-\(96\) abstract frontier matrix has a transparent 255-subset-per-
shore checker, but the matrix is only a limitation of the current
method.  The
24-vertex example has a small exhaustive checker and frozen hashes; a
human-readable colouring/cut certificate should accompany any paper
that makes it a headline result.

## Separate computational result

The \(H_4\) minimum-support enumeration is a distinct possible
computational note.  It exhausts 4,931,430 globally minimum size-four
supports.  Completeness is certified by a 4,936,112-clause CNF and a
973,056,379-byte LRAT accepted by both C `lrat-check` and verified CakeML
`cake_lpr`.  Its positive packing-witness replay should be complete
before the result is publicized as a finished package.  It does not
resolve five-CDC.

## AI disclosure

The page-one disclosure in the preprint is appropriately prominent and
should remain.  It states that Codex agents generated proof ideas, prose,
programs, searches, constructions, and checking artifacts under human
direction; that the second-agent audit and “independent” checker are also
AI-assisted; and that no human verification or peer review is being
claimed.

## Recommended publication path

1. Release the current manuscript as a clearly labeled research draft
   only after a human author checks every proof, including the new
   order-\(88\) argument, and assumes authorship responsibility.
2. Ask at least one specialist in flows/cycle covers to verify novelty and
   the two-sum arguments.
3. Have a human independently reconstruct the 40- and 46-vertex graphs
   from the incidence data and rerun the small checkers.
4. Submit the focused countermodel paper to a graph-theory venue; keep the
   \(H_4\) certificate package and the broader conjecture-resolution lab
   as separate work unless a clean theorem connects them.
