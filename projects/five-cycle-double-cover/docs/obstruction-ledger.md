# Obstruction ledger

## O1 — Fixed merging of the new eight coordinates

Status: **FAILED APPROACH**, proved.

A valid cubic 8-CDC can have coordinate co-occurrence graph \(K_8\) (the
explicit affine-plane/cube construction is in
`docs/algebraic-characterization.md`).  Fixed merging into five coordinates
would require a proper five-coloring of this \(K_8\), so it cannot be a
universal rule.

## O2 — Fixed XOR recombination of the new eight coordinates

Status: **FAILED APPROACH**, proved.

An XOR recombination corresponds to assigning a five-bit column to every old
coordinate so that co-occurring columns have Hamming distance two.  The
distance-two graph on five-bit words has clique number five, whereas O1 gives
a cover with co-occurrence \(K_8\).  Therefore no fixed XOR postprocessing
works for every supplied 8-CDC.

Graph-dependent recoloring, changing the original 8-cover, or jointly choosing
the 2026 lifting potentials remain open.

## O3 — Fixed map from seven-valued binary flow directions

Status: **FAILED APPROACH**, proved.

No map from \(\mathbb F_2^3\setminus\{0\}\) to the ten two-subsets of
\([5]\) sends every Fano line to a \(K_5\)-triangle.  This blocks a new label
depending only on the nowhere-zero flow value of an edge.

## O4 — Four-cycle boundary pattern

Status: **SOUND SEARCH CONSTRAINT**.

For a cubic four-cycle, an alternating external boundary
\((a,b,a,b)\) with distinct intersecting pair-labels has no internal
extension.  An exhaustive independent check covers all 640 ordered
parity-valid boundary tuples: precisely 60 are nonextendible, and all 60
have this form.  Separately, the proof-agent smoothing argument shows that a
minimum cubic multigraph counterexample has no four-cycle; that global
reduction does not rely on pruning an arbitrary boundary.

## O5 — Covering graphs and 2-lifts of settled bases

Status: **FAILED COUNTEREXAMPLE FAMILY**, proved.

If \(p:H\to G\) is a graph covering map and \(G\) has a 5-CDC, the inverse
image of each of its five even edge-subgraphs is even at every lifted vertex
and every lifted edge is still covered twice.  Hence \(H\) has a 5-CDC.
Voltage lifts and 2-lifts of already settled base graphs are positive stress
tests, not candidate counterexamples.

## O6 — Choosing a quotient line for a fixed binary flow

Status: **FAILED APPROACH**, proved by an exact eight-vertex example.

The quotient-lift theorem in `docs/proof-agent-audit.md` says that a
nowhere-zero \(\mathbb F_2^3\)-flow lifts to pair labels for a chosen Fano
line unless a component of the line-valued subgraph sees all four outside
values oddly across its boundary.

One explicit simple cubic bridgeless graph carries a fixed flow for which
each of the seven Fano lines has such a component.  The graph is
3-edge-colourable and therefore has a 5-CDC; it obstructs only the proposed
rule “keep the flow and choose a better line.”  A successful proof may still
change the flow as well as the line.

## O7 — Component-minimal connected-kernel switching

Status: **LOCAL OBSTRUCTION / NOT YET A SOUND GLOBAL NO-GOOD**.

Fix a Fano line \(L\), let \(J\) be the line-valued spanning join of a
nowhere-zero \(\mathbb F_2^3\)-flow, and switch value \(t\) along a valid
binary circuit \(C\).  If \(t\in L\), then \(J\) is unchanged.  If
\(t\notin L\), then

\[
  J\longmapsto J\mathbin{\triangle}C.
\]

The complement of \(J\) is a disjoint union of circuits.  If one such
circuit meets at least two \(J\)-components and omits an outside-line value,
switching by the omitted value adds the entire circuit to \(J\) and strictly
decreases its component count.  Therefore a pair locally minimal under
these switches forces every component-joining complementary circuit to use
all four outside values.

The four-value-surjective circuit occurs locally already on \(K_4\), but
other circuit switches repair it.  Exhaustively, none of 3,681,048
disconnected flow-line pairs through order 10 is stable against every
component-decreasing elementary switch.

Arbitrary binary-cycle switches admit a precise stronger obstruction:
each of the four outside color classes must hit every cycle \(C\) with
\(\kappa(J\mathbin{\triangle}C)<\kappa(J)\).  The smallest such immediate
trap occurs on an order-12 graph, where the four color classes are disjoint
two-edge transversals of all nine reducing cycles.  It escapes after a
line-valued recoloring and one outside switch.  Moreover, all 9,132
realizable disconnected joins in the exact order-12 census have *some*
low-coordinate assignment allowing a reduction.  The immediate hitting-set
pattern must not be used as a pruning clause until a recoloring-independent
obstruction is proved.

## O8 — Equal-boundary \(F_{10}\) is transparent to five-covers

Status: **FAILED COUNTEREXAMPLE SPECIMEN / POSITIVE COMPOSITION RULE**.

For each of the ten \(D_5\) pair labels, the exact implemented \(F_{10}\)
six-pole has an internally conserved labeling in which all six terminal
semiedges receive that label.  Thus any five-cover of a cubic base graph
lifts through the particular three-lane \(F_{10}\) superposition used by
the candidate-domain construction: use the corresponding local template on
each substituted edge, and conservation at the three junction lanes is the
base vertex equation.

This explains the positive order-30,450 witness and yields a reusable
positive closure rule for this exact superposition.  It does not say that
every cover of the superposition restricts to the base, and therefore does
not supply a counterexample-preserving reduction in the reverse direction.

The reverse implication fails at the local aggregate level as strongly as
possible.  Exact SAT models exist for every one of the 16 even five-bit
values as the XOR of the three terminal labels on either connector: zero,
all ten weight-two labels, and all five weight-four labels.  Hence
contracting a general local five-cover can produce zero or forbidden
weight-four values on a base edge.  The exhaustive retained boundary run is
`search/candidate_domain/runs/f10-connector-aggregates-20260725/`.

## O9 — Recoloring circuit components of one supplied 8-CDC

Status: **FAILED UNIVERSAL APPROACH**, proved.

For a supplied CDC of a cubic graph, split each old coordinate into circuit
components and join two components when they share an original edge.  A
partition of these circuits into \(r\) new coordinates is a valid \(r\)-CDC
if and only if it is a proper \(r\)-coloring of this component-conflict
graph.

The retained affine-plane construction has a connected, bridgeless
112-vertex realization in which 24 label-preserving two-switches make each
of the eight old coordinate supports a single circuit.  Every pair of
coordinates still occurs on an edge, so the component-conflict graph is
exactly \(K_8\).  Its chromatic number is eight.  Thus even graph-dependent
recoloring of the circuit components of an arbitrary supplied 8-CDC is not
a universal eight-to-five compression.

This does not rule out changing the supplied 8-CDC, splitting circuits into
smaller non-Eulerian pieces as part of a joint construction, or coordinating
the choices in the 2026 eight-cover proof.  The theorem, construction, and
scope are in `docs/component-recoloring.md`.  An independent checker also
found a proper three-edge-coloring of the host, so its complementary
two-factors explicitly form a standard 3-CDC.

## O10 — Affine relabelling followed by quotient lifting

Status: **FAILED UNIVERSAL APPROACH**, proved for a supplied-cover rule.

Map the eight coordinates of a supplied 8-CDC by an arbitrary bijection
\(\rho\) to \(\mathbb F_2^3\), replace an old pair \(\{s,t\}\) by the
flow value \(\rho(s)+\rho(t)\), choose any Fano quotient line, and solve the
remaining binary lift.  Translation cancels in every pair sum, while
\(GL(3,2)\) only renames values and lines.  Exact orbit enumeration leaves
30 affine structures and 210 structure/line cases.

For the retained coordinate-tree cover, all 210 binary lift systems are
inconsistent and every case has at least two bad components.  Independent
Gaussian elimination agrees with the quotient component test.  A positive
control has one good affine structure and three good lines.  This excludes
the entire relabel-then-lift rule for that supplied 8-CDC, but does not
exclude another cover, changing the underlying projected flow by other
means, or a direct 5-CDC.

## O11 — Minimal-exact-support packing

Status: **SOUND TARGET SEARCH CONSTRAINT**.

If a graph has no nowhere-zero \(\mathbb F_2^2\)-flow, every standard
five-cover partitions its edges into ten nonempty exact zero sets, one for
each pair label.  Selecting a minimal exact subset of each gives ten
pairwise edge-disjoint members of the minimal-support hypergraph.  Therefore
\(\nu(\mathcal M(G))\leq9\) is a sound sufficient obstruction to a standard
5-CDC.  It is not known whether such a bridgeless graph exists.  The scalar
resistance bound obtained by forgetting the packing is weaker than a known
perfect-matching bound and must not be advertised as new.

## O12 — First high-flow-resistance \(H_n\) stress case

Status: **FAILED COUNTEREXAMPLE SPECIMEN / POSITIVE TARGET WITNESS**.

The reconstructed Mattiolo--Negrini--Pagani \(H_2\) is simple, cubic,
girth five, and cyclically 5-edge-connected.  A retained LRAT plus an
explicit flow proves flow resistance exactly two.  Nevertheless its
distinguished exact zero pair has \(\mu=1\), and its complete standard
five-cover formula is SAT with a witness accepted independently by both
project verifiers.  High flow resistance at this density therefore supplies
no obstruction at \(n=2\).  The result does not settle later members beyond
the separately tested \(H_3,H_4,H_5\), and the reconstruction provenance is
limited to the paper's vector figures because no author graph file was
supplied.

## O13 — Component-paired odd-factor obstruction

Status: **EXACT TARGET CHARACTERIZATION / POINTWISE STRENGTHENING FALSE**.

For a loopless cubic multigraph, the matching/four-flow theorem reduces the
standard five-cover target to an exact-zero matching \(M\) and two binary
cycles meeting exactly in \(M\).  If \(H\supseteq M\) is the first cycle,
the second exists precisely when every component of \(E-H\) contains an
even number of endpoints of \(M\).  Equivalently, there must be a spanning
odd factor avoiding \(M\) and pairing the \(M\)-endpoint demands inside
each component.

Thus failure of this condition for every exact-zero matching is an exact
target obstruction.  Failure for one support is not.  Complete enumeration
on the seven retained order-34 minimal supports with \(\mu=2\) finds two
GOOD supports and five BAD supports; every affected graph has a different
\(\mu=1\) GOOD support.  This both proves that connected complement is
unnecessarily strong and refutes the tempting claim that every relevant
minimal support is component-parity good.

## O14 — Second high-flow-resistance family stress case

Status: **FAILED COUNTEREXAMPLE SPECIMEN / POSITIVE TARGET WITNESS**.

The reconstructed \(H_3\) is simple, cubic, girth five, cyclically
5-edge-connected, and has certified flow resistance three: a retained LRAT
rules out flows with at most two zero edges.  Its direct standard
five-cover formula is nevertheless SAT with coordinate sizes
\(77,74,58,77,80\), accepted by both semantic verifiers.  The exact
matching/four-flow formula also supplies an independently reverse-lifted
five-cover.  Hence increasing this family's flow resistance from two to
three still does not produce the target obstruction.  No inference is made
for all \(H_n\).

## O15 — Third and fourth high-flow-resistance family stress cases

Status: **FAILED COUNTEREXAMPLE SPECIMENS / POSITIVE TARGET WITNESSES**.

The reconstructed \(H_4\) and \(H_5\) are simple cubic girth-five graphs,
and retained cut-CNF LRATs prove each cyclically 5-edge-connected.
Explicit flows plus independently checked LRATs establish flow resistances
four and five.  Their full direct standard formulas remain SAT with
coordinate-size vectors \(130,112,68,72,104\) and
\(144,143,95,98,126\).  Both project verifiers accept the direct models,
and matching/four-flow reverse lifts supply independent five-covers.  Thus
flow resistance growing through five still does not produce a target
obstruction in the reconstructed family.  A later explicit stable
\(D_5\)-tile does prove a cover transfer for every frozen
\(\widehat H_n\), \(n\ge2\): its input and output state is
\((01,01,02,23,03)\), and its package ledger is
`e09cee11f74b19e4a08f18c94534207e44f601a29f059a15fb614154900cbfac`.
Consequently this entire reconstructed family is discharged as a
counterexample source.  The result remains family-specific and
standard rather than orientable.

For the author-defined MNP graphs, existence is also a prior corollary:
their displayed almost-proper coloring yields a 2-factor with exactly two
odd circuits, so Huck--Kochol (1995) applies.  The project therefore makes
no novelty claim for family-wide five-cover existence.

## O16 — Prescribing an arbitrary high coordinate

Status: **FAILED UNIVERSAL APPROACH / CERTIFIED RESTRICTED UNSAT**.

In the Petersen graph, prescribe the spanning two-factor consisting of its
two disjoint 5-cycles as one coordinate.  The exact direct target formula
with those coordinate units is UNSAT, as is the exact cubic
matching/four-flow cross-formula.  Both LRATs pass two independent proof
checkers.  Exhausting all 4,096 ordered \(\mathbb F_2^2\)-flow pairs finds
the same obstruction: none has an exact zero matching whose endpoint demand
is even in all five perfect-matching complement components.

The Petersen graph itself has a retained standard 5-CDC, directly checked
at sizes \(6,5,5,9,5\).  Therefore this is not graph-level UNSAT.  It
proves only that a universal argument cannot fix an arbitrary binary high
cycle and expect low-coordinate recoloring alone to finish the lift.

## O17 — Odd-\(K_{2,3}\) graft obstruction

Status: **NECESSARY FIXED-SUPPORT OBSTRUCTION / UNIVERSAL EXCHANGE OPEN**.

For an exact-zero matching \(M\), put \(K=G-M\) and
\(T=\partial M\).  The fixed support extends to the exact
matching/four-flow five-cover certificate if and only if \(K\) packs two
edge-disjoint \(T\)-joins.  The flow on \(K\) is nowhere zero, hence
\(K\) is bridgeless; every terminal has degree two.  This does not
automatically make the minimum \(T\)-cut two.  If a component of \(K\)
contains an odd number of terminals, its empty boundary is a \(T\)-cut and
no \(T\)-join exists.  If every component is \(T\)-even, then and only then
the present argument gives minimum \(T\)-cut two.

The first branch is realized by the frozen ten-vertex graph6 instance
`Is?AXW[[?` in
`search/component-parity-tjoin-countermodel-20260725/`.  It consists of two
\(K_{2,3}\) components joined by the zero matching.  Each complement
component has three terminals, all three color quotients are forests, and
there is no \(T\)-join.  The matching is not globally minimum and the graph
has a checked five-cover, so this is a sharpness example for the
intermediate hypotheses only.

Under that component hypothesis, the Codato--Conforti--Serafini packing
theorem implies that remaining failure to pack two \(T\)-joins forces an
odd-\(K_{2,3}\) graft minor.  Such a minor allows edge deletion as well as
parity-aware edge contraction.
This direction is sound and is the only obstruction imported from that
theorem.  The presence of such a minor is not asserted to be
sufficient for failure.

Minimum exact-zero matchings obey a further necessary condition.  Switching
the flow along \(M\cup J\) for any \(T\)-join \(J\), separately in each
nonzero flow color, proves that \(J\) contains at least \(|M|\) edges of
each color.  In particular \(|J|\ge3|M|\).  This is a proved obstruction to
a short exchange, not a proof that two disjoint \(T\)-joins exist.

The surviving proof target is an exchange theorem at minimum support:
derive a smaller exact-zero matching from a genuinely nonpacking minimum
matching, or prove that at least one minimum matching avoids the
obstruction.  Exact finite evidence finds no counterexample: every minimum
support in the complete order-20 hard corpus extends, and every one of
92,313 minimum supports of reconstructed \(H_3\) extends with a
certificate-complete projected enumeration.  This does not establish the
exchange theorem.

Candidate patterns, UNSAT cores, and near-solutions belong here only with a
proof that the recorded constraint preserves every genuine counterexample.

## O18 — Immediate \(K_6\)-defect descent on a snark

Status: **FAILED APPROACH / EXACT CYCLICALLY 4-EDGE-CONNECTED SNARK
CERTIFICATE**.

Identify nonzero \(\mathbb F_2^4\) flow values with the duads of \(K_6\).
At a cubic vertex, a perfect-matching triple is a defect.  A constant-value
switch adds \(t\) along a binary cycle \(Q\), subject to the nowhere-zero
condition \(Q\cap\phi^{-1}(t)=\varnothing\).

The 36-vertex witness in
`search/k6-defect-snark-plateau-20260725/` is simple, cubic, bridgeless,
girth five, cyclically 4-edge-connected, and non-3-edge-colourable.  Its
flow has four defects.  Exhaustion of all \(2^{19}\) binary cycles for all
15 switch values finds no negative defect change.  An independent
four-pole transfer calculation reaches the same result; the graph's
non-3-edge-colourability has a two-checker LRAT and an independent
perfect-matching proof.

Therefore neither of the following may be used:

1. every positive switch-local minimum has exactly two defects; or
2. every positive-defect flow on a cyclically 4-edge-connected snark has an
   immediately improving constant-value cycle switch.

This does not obstruct neutral multi-switch paths, cyclic-connectivity-five
arguments, or five-cycle double covers themselves.  Indeed, the retained
trajectory uses switch values \(3,18,3,17\) and has defect counts
\(4\to4\to2\to2\to0\).  Its zero-defect endpoint is only a
six-coordinate cover because it omits no \(K_6\)-star.  A fifth checked
star-cycle switch then eliminates one coordinate and gives a standard
five-cycle double cover.  The witness is a failed-lemma certificate, not
a five-CDC counterexample.

## O19 — Defect-monotone \(K_6\)-star reconfiguration

Status: **FAILED APPROACH / EXACT PETERSEN BARRIER CERTIFICATE**.

The Petersen package
`search/k6-petersen-star-barrier-20260725/` freezes a zero-defect flow
using every duad exactly once.  Of its 945 nonempty constant-value cycle
switches, exactly 15 remain triangle-only; they are precisely the global
\(K_6\)-coordinate transpositions.  They generate a free \(S_6\)-orbit
of size 720, and exhaustive adjacency checking proves this is the whole
triangle-preserving component.  Every orbit member still uses all 15
duads, so none omits a star.

Therefore a universal route may not assume that a triangle-only flow can
be reconfigured to a five-cover while never increasing the defect count.
The obstruction is sharp: a retained two-switch path has defect counts
\(0\to2\to0\) and its endpoint omits a star.  Since the defect count is
always even, barrier two is optimal.  This is a reconfiguration
obstruction, not a graph-level five-CDC counterexample.

## O20 — Triangle-only \(K_6\) reconfiguration, even in infinite families

Status: **FAILED UNIVERSAL APPROACH / INFINITE EXACT BARRIER FAMILY**.

The Petersen obstruction persists under the labeled ring construction in
`search/k6-petersen-ring-barrier-20260725/`.  For every \(n\ge1\), the
triangle-only component has exactly \(15\cdot48^n\) states.  Every state
uses all 15 duads and omits no \(K_6\)-star.  The proof classifies every
triangle-preserving switch by the components of its crossing-label
subgraph; it applies both to arbitrary even-subgraph moves and to the
standard connected-circuit convention.

Therefore no universal proof may insist on staying in the triangle-only
stratum, even after excluding an isolated small-graph phenomenon.  The
barrier does not grow with the number of blocks: a sequential path has
profile \(0,(2,0)^n\) and ends at a standard five-cycle double cover.
The obstruction is to monotonicity, not to five-CDC.

## O21 — Universal connected-kernel / connected-complement normal form

Status: **FAILED UNIVERSAL APPROACH / INFINITE EXACT SEPARATION FAMILY**.

Let \(B\) be a non-3-edge-colourable cubic graph and \(T\) a spanning tree.
Replace every cotree edge by a diamond \(K_4-e\).  In any hypothetical
connected-kernel \(\mathbb F_2^3\)-flow on the expanded graph, flow
conservation makes the two attachment values of each diamond equal.
Connectivity of the selected line-valued subgraph forces these common
values into the line.  After diamond contraction, the outside-line support
is a binary cycle of \(B\) contained in \(T\), so it is empty.  The
contracted flow would therefore be a nowhere-zero \(\mathbb F_2^2\)-flow,
equivalently a proper 3-edge-colouring of \(B\), a contradiction.

Any five-cover of \(B\) nevertheless lifts through each diamond by a local
three-duad rule.  With \(B\) equal to Petersen, the 34-vertex retained graph
has an explicit standard five-cover accepted by both target verifiers, but
a 153-variable, 465-clause relaxation of its connected-kernel formula is
UNSAT with a two-checker LRAT.  Iteration gives an infinite separation
family.

Therefore no universal proof may assume that every five-cycle double cover
can be chosen with a connected coordinate complement, or equivalently that
every bridgeless cubic graph has a connected congruent join.  The surviving
preparation and exchange routes must allow disconnected kernels.  This is
not a graph-level five-CDC obstruction: every retained separator has a
constructively lifted standard five-cover.

## O22 — Weighted \(T\)-join minima plus quotient forests

Status: **FAILED INTERMEDIATE LEMMA / EXACT CYCLICALLY 4-EDGE-CONNECTED
COUNTERMODEL**.

The 22-vertex graph in
`search/tjoin-weighted-minima-countermodel-20260725/` has a size-three
exact-zero matching \(M\) whose complement is connected and
\(\partial M\)-even.  For every one of the three nonzero flow colours,
the minimum colour cost of a \(T\)-join is exactly \(3=|M|\), and the
corresponding minimum-zero quotient is a forest.  Yet no two \(T\)-joins
are edge-disjoint.

Three of the marked core edges are three sides of a four-cycle.  Every
binary cycle containing all six marks has that four-cycle as an entire
component with three marks, contradicting the even-marked circuit
criterion for two-\(T\)-join packing.  Both retained checkers also enumerate
all 512 joins and all cuts of size at most three.

Therefore the switching inequalities and quotient-forest theorem, even
together, are not sufficient axioms for packing.  A minimum-support
exchange proof must exploit global minimality beyond those consequences.
The displayed \(M\) is not minimum—an explicit nowhere-zero flow exists—and
the host has girth four.  Thus this does not refute the actual minimum
exact-zero-matching conjecture in the reduced girth-at-least-five domain,
and it is not a five-CDC counterexample.

## O23 — Unrestricted fixed-join preparation

Status: **FAILED UNIVERSAL APPROACH / EXACT 38-VERTEX PREPARATION TRAP**.

The graph in `search/fixed-join-preparation-trap-20260725/` is simple,
connected, bridgeless, and cubic.  A displayed binary cycle \(H\) has
\(\kappa(E-H)=2\) and contains exactly 125 inclusion-minimal exact zero
sets, all satisfying \(\mu_G(T)=2\).  Hence no choice of low coordinates
prepares this fixed high coordinate.

The graph is obtained by inserting Petersen 2-poles at two rooted edges of
an 18-vertex base.  Terminal parity and connectivity force a hypothetical
connected spanning odd factor to cross both poles in both terminal edges.
Contraction would produce a connected base odd factor containing both roots
and avoiding one of five minimal base supports; exhaustive enumeration of
the 25 base factors shows none exists.  Independent checkers replay the
factorization and all \(2^{20}\) expanded binary cycles.

This obstruction uses two nontrivial two-edge cuts.  A target-standard
five-cover is explicitly verified.  Therefore only the unrestricted
preparation lemma fails; a reduced-domain preparation theorem and the
minimum-support exchange route remain logically possible, and five-CDC is
unaffected.

## O24 — Strict one-switch descent for exact-zero matchings

Status: **FAILED UNIVERSAL APPROACH / EXACT 16-VERTEX LOCAL PLATEAU**.

The graph in `search/minimum-switch-local-plateau-20260725/` is simple,
connected, bridgeless, and cubic.  Its displayed
\(\mathbb F_2^2\)-flow has exact zero matching \(M=\{2,13\}\).  The 128
affine \(T\)-joins in \(G-M\) contain no edge-disjoint pair.  Exhausting all
512 binary cycles for all three nonzero switch values finds no
matching-preserving support smaller than \(M\).

The exact switch law is

\[
Z(\phi+c1_X)=(M-X)\cup(X\cap\phi^{-1}(c)).
\]

Independent Python and JavaScript checkers reconstruct the complete switch
profiles and the nonpacking assertion.  A neutral switch followed by a
strict switch has profile \(2\to2\to1\), and the final size-one support has
an explicit packing circuit.  Hence this is a local plateau, not a
counterexample to the minimum-support conjecture or to five-CDC.  It proves
that any surviving exchange theorem must use neutral reconfiguration,
global minimality, or the reduced minimum-counterexample hypotheses.

## O25 — Disconnected Fano one-switch domination

Status: **FAILED AS STATED / CONNECTED REPAIR CONJECTURE LATER REFUTED**.

Take two disjoint copies of the ten-vertex bad-flow instance from
`search/fano-value-class-flow-countermodel-20260726/`.  For a value \(k\),
the disjoint union packs two \(\partial M_k\)-joins exactly when both
components do.  Initially neither component packs for any of the seven
values.  A connected circuit is contained in one graph component, so a
single switch leaves the other bad for every value.  The union is therefore
switch-local bad.

This refutes the one-switch domination assertion without a connectedness
hypothesis.  It does not affect five-CDC, since covers of components combine
coordinatewise.  The corrected conjecture is restricted to connected
bridgeless cubic graphs.

The most direct connectedization attempt does not preserve the obstruction:
all 10,800 aligned two-edge sums of two copies are initially bad but
one-circuit repairable.  A deterministic sample of 100 aligned three-block
chains has the same outcome.

## O26 — Connected Fano one-switch domination

Status: **REFUTED / POSITIVE STANDARD FIVE-CDC CONTROL**.

The package
`search/connected-one-switch-countermodel-40v-20260726/` freezes a
40-vertex simple connected bridgeless cubic graph with a nowhere-zero
\(\mathbb F_2^3\)-flow that is bad and remains bad after every allowed
switch on one connected circuit.

The finite obstruction is the monochromatic edge set
\(P=\{02,56,17\}\) in the ten-vertex Tait graph `It?GYDKKO`.  A direct
triangle argument proves that no circuit contains all three edges.
Replacing them by flow-aligned two-sums with three copies of the
ten-vertex bad block ensures that every circuit leaves one bad block
unchanged.  Projecting hypothetical global disjoint \(T\)-joins through
that block contradicts its seven frozen nonpacking certificates.

An independently written checker reconstructs the composition, checks
every single-edge deletion and every flow equation, enumerates all 30
base circuits and all 6,780 final circuits, and verifies an explicit
three-cycle double cover (padded by two empty coordinates).  Consequently
O26 refutes only the one-switch domination route.  It is not a five-CDC
counterexample.  The earlier 2,614-vertex \(H_5\)/LRAT package is a valid
but superseded construction.

## O27 — Fixed-flow Oum-potential pure merging

Status: **FAILED UNIVERSAL APPROACH / EXACT 12-VERTEX RIGID \(K_6\)
COUNTERMODEL**.

The bipartite cubic graph `K??FEaKR@oE_`, with the frozen nowhere-zero
\(\mathbb F_2^3\)-flow in
`search/fano-pure-merge-one-switch-countermodel-46v-20260726/`, has a
unique compatible vertex-potential system modulo global translation.
Its two-element edge labels use all 15 pairs on six of the eight
coordinates.  Their co-occurrence graph therefore contains \(K_6\), so no
partition of the eight coordinates into at most five classes can preserve
exact-two coverage under symmetric-difference merging.

The stronger port-deleted statement is also exact.  Deleting edge 1 and
fixing one translation gives a 37-equation, 36-variable binary system of
rank 36.  The two dangling port labels agree, and the retained labels plus
that port label still give the same \(K_6\).  The human proof reduces this
to eleven displayed scalar equations with a unique solution.

This rules out pure five-way merging for one fixed flow, even after all
compatible potential choices are allowed.  It does not rule out choosing a
different flow or constructing a five-cover by another method.  The graph
is three-edge-colorable.

## O28 — One connected-circuit repair of fixed-flow pure merging

Status: **REFUTED / HUMAN-CHECKABLE 46-VERTEX COMPOSITION / POSITIVE
STANDARD FIVE-CDC CONTROL**.

In the Tait base `It?GYDKKO`, the three flow-2 edges
\(\{02,56,17\}\) lie on no common circuit.  Replace each by an aligned
two-sum with a fresh copy of the O27 port-deleted rigid block.  Any connected
circuit leaves one whole block and both connectors untouched: otherwise
contracting each traversed block path would give a base circuit containing
all three marked edges.  The untouched block forces a coordinate \(K_6\)
after every nowhere-zero switch on the circuit.  Hence no one connected
circuit switch makes the fixed flow purely mergeable to five coordinates.

The complete package is
`search/fano-pure-merge-one-switch-countermodel-46v-20260726/`.  Its
independent checker imports no producer, reconstructs the graph, checks all
69 single-edge deletions, row-reduces the rigid cap, enumerates all 30 base
circuits, and independently enumerates all 128 compatible gauged potentials
of the starting 46-vertex flow.  Every co-occurrence graph contains a
\(K_6\).

The final graph is simple, connected, cubic, bridgeless, nonplanar, and
three-edge-colorable.  Its explicit standard five-cover has coordinate
sizes \(46,46,46,0,0\).  O28 therefore refutes only the
“pure merge plus one connected-circuit repair” strategy.  Its three
nontrivial two-edge cuts leave the cyclically 4-edge-connected restriction
open.

## O29 — Automatic lifting from an Eulerian factor quotient

Status: **REFUTED AS STATED / EXACT HUMAN-CHECKABLE LOCAL OBSTRUCTION**.

Contracting the monochromatic lifted two-factor in the connected
stable-eight branch and deleting the zero matching does produce a
connected Eulerian multigraph.  Such a quotient always has two
edge-disjoint \(T\)-joins, even a complementary pair.  This does not imply
two joins in the uncontracted graph: the two parity paths chosen through
each factor circuit must also be edge-disjoint in their fixed cyclic port
order.

The four-vertex quotient in
`docs/two-tjoin-cycle-lift-obstruction.md` is a triangle with a doubled
pendant side.  Its complete list has four \(T\)-joins and only two
edge-disjoint unordered pairs.  Both fail the marked alternating-gap
criterion at the degree-four quotient vertex.  Its literal 14-vertex
expansion has 64 \(T\)-joins and no disjoint pair.

The actual minimum-counterexample branch excludes this literal quotient:
it has the wrong number of marked factor vertices, degree below ten, and
a paired-cut violation.  The forcing mechanism nevertheless survives in
general exactly when the two terminal-flanking ports form an
even-terminal quotient 2-cut.  The paired-cut inequality promotes such a
certificate to a cyclic ambient 4-cut containing two zero edges or a
cyclic 6-cut containing all four.  Thus O29 refutes automatic quotient
lifting but leaves a sharply reduced cut and simultaneous-gap obligation;
it is not a graph-level five-CDC obstruction.

## O30 — Equality incidence and transition data alone

Status: **REFUTED AS A SUFFICIENT CONDITION / EXACT ORDER-80
COUNTERMODEL**.

The decorated \(8+8\), 5-regular incidence object in
`docs/equality88-incidence-rotation-countermodel.md` reconstructs a
simple connected order-80 Tait core with the two required \(C_{10}\)
factor decompositions, but all 256 factor selectors have an
odd-marked component.  Independent implementations reproduce the
complete histogram.

This does not survive the minimum-counterexample hypotheses: the core
has girth three, an explicit Kempe switch violates universal separation,
and unrestricted terminal joins pack.  The learned constraint is exact:
any equality proof must use girth or universal separation, not merely
the 5-regular incidence degrees and cyclic transition data.  The
subsequent overlap/Kempe theorem does exactly this and rules out equality.

## O31 — Naive rooted four-mark cap avoidance

Status: **REFUTED WITHOUT THE MARKED-CUT HYPOTHESIS / EXACT
ORDER-28 COUNTERMODEL**.

The graph in `scratch/rooted-four-mark-countermodel-result.json` is
Tait-colourable and its four-edge matching is universally separated.
With the marks one colour and the root a second colour, every
componentwise-even all-mark binary cycle uses the root.  A cyclic
two-edge cut separates the marks \(3+1\), giving the direct human
obstruction.

The same shore has marked-cut score \(2+1=3\) and marked-subdivision
girth five, so it lies outside the inherited six-cut interface.  The
countermodel refutes only the naive rooted theorem; the full rooted
component-parity statement under the marked-cut, girth, paired-cut, and
minimum-support hypotheses remains open.

## O32 — Local Kempe incidence inequalities at order 96

Status: **REFUTED FOR THE EARLIER INEQUALITY SET / LATER LOCAL
CONSTRAINTS EXCLUDE THE ENTIRE ORDER-96 SYSTEM**.

The \(8\)-by-\(8\) incidence matrix displayed in
`docs/audit-and-generalization-order94-kempe.md` has the exact
order-\(96\) row and column length profiles.  It satisfies every sharp
pairwise overlap bound, every single-switch inequality, and the exact
simultaneous-switch inequality for all 255 nonempty subsets on either
shore.  The independent checker reports minimum slack one.

No compatible cyclic orders, Tait core, girth-ten realization, universal
separation, or five-CDC obstruction is asserted.  O32 refutes only the
claim that the earlier overlap and Kempe inequalities by themselves can
push the connected size-four lower bound past 96.  The later sum-\(26\),
diagonal-parity, and short-factor spacing lemmas do supply the missing
information: the complete strengthened census has no order-96 matrix and
raises this branch to order at least 98.

## O33 — Order-98 incidence relaxation

Status: **EXCLUDED BY A NEW LOCAL DIAGONAL CAP / COMPLETE THREE-WAY
FINITE REPLAY**.

The earlier order-96 constraints permit abstract all-marked order-98
profile systems.  The missing local condition is that same-mark factor
circuits whose excesses sum to two cannot have overlap three.  Such an
overlap contracts to a positive weighting of either the triangular prism
or \(K_{3,3}\) with total weight 22; the prism has two disjoint triangles
and the \(K_{3,3}\) four-circuits average below ten, contradicting girth
ten in either case.

With this cap, the complete solver-free census has zero matrices on all
335 simultaneous-\(S_8\) profile orbits.  Independent Z3 and HiGHS
encodings agree, and a prune-free replay is empty.  Removing only the new
cap restores exactly two profile survivors.  Thus O33 is eliminated at
the incidence level and the connected size-four branch advances to order
at least 100; no global five-CDC conclusion follows.

## O34 — Order-100 row-star and global-rotation frontier

Status: **EXCLUDED BY THREE PROFILE-LEVEL CNFS / LRAT AND SEMANTIC
CLAUSE AUDITS**.

At order 100, the human incidence argument excludes all unmarked factor
circuits.  The all-marked cap-table relaxation retains 155 canonical
profiles, and exact weighted row-and-column stars retain three profile
alignments.  Those three profiles contain 5,528 labelled row-star
matrices, or 827 orbits under their aligned stabilizers, so checking one
matrix from each profile would not eliminate O34.

The final encoding instead chooses the entire incidence matrix and its
geometry inside each profile.  Its variables select every cell's cyclic
positions, bijection, and endpoint twists; exact cover constraints glue
all 46 common-colour tokens.  Short circuits generate sound negative
option clauses.  The three final CNFs are UNSAT already before terminal
pairing, and independent `lrat-check` runs accept all three LRATs.  A
producer-free checker separately regenerates the finite domains and base
formulas and confirms that all 996,904 learned clauses force concrete
circuits of length below ten.

Thus O34 is eliminated and the connected eight-mark extremal exact-zero
size-four branch advances to order at least 102.  This remains a
branch-specific obstruction ledger entry, not a resolution of five-CDC.

## O35 — Pointwise exclusion of the two rooted coordinate cuts

Status: **FAILED APPROACH**, refuted by a smallest retained order-seven
control.

For a rooted three-pole with boundary word \((01,02,12)\), a tempting
strengthening of the complement-cycle argument was the following:
whenever a nonbridge root has label \(12\) in one fixed \(D_5\)-labelling,
it cannot simultaneously be a bridge after deleting the coordinate-\(3\)
support and after deleting the coordinate-\(4\) support.  If true, one
complement-cycle switch and the \(3\leftrightarrow4\) symmetry would have
supplied the whole base pair \(\{12,03,04\}\).

The claim already fails on graph6 `FCpv?`, with root edge \(0\).  An exact
labelling and two explicit root-separating cuts witness both bridge
conditions although the unlabelled root is not a bridge.  The complete root
signature has orbit mask `0x2d`, which contains both base pairs `0x0c` and
`0x21`; the pole is therefore repairable only after changing the labelling.
The independently checked control is
`scratch/root-double-coordinate-cut-order7-result.json`, its verifier is
`scratch/verify_root_double_coordinate_cut.py`, and the general SAT
falsifier is `scratch/test_root_double_coordinate_cut.cpp`.

Thus the coordinate-cut certificates in
`docs/rooted-base-pair-cycle-cut-certificate.md` cannot be contradicted
pointwise.  A proof of universal base-pair closure must relate different
labellings or use a genuinely multi-step reconfiguration.

## O36 — Base-pair completion inside one cycle-reconfiguration component

Status: **FAILED APPROACH**, refuted by the same smallest order-seven
control.

One might try to repair O35 by allowing an arbitrary sequence of legal
constant translations on proper circuits while keeping the boundary word
fixed.  This is still too restrictive.  The graph6 pole `FCpv?` has exactly
55 fixed-boundary \(D_5\)-labellings.  Their exact circuit-reconfiguration
graph has three components:

```text
component size   root labels on edge 0
47               12, 03, 04
 2               01
 6               23, 24
```

Thus the base pair \(\{01,23,24\}\) exists in the full signature but is
split between two reconfiguration components.  The two-labelling component
with root \(01\) is closed under every legal single-circuit translation.
Complete lower-order inputs at orders three and five contain no such
control, so this is smallest in the retained simple rooted corpus.

`scratch/test_root_reconfiguration_component.py` enumerates the affine
\(\mathbb F_2^4\)-flow space and every circuit move.  The independently
structured checker in `scratch/verify_root_double_coordinate_cut.py`
reconstructs all 55 flows and the three component profiles from the raw
graph and displayed labelling.

Consequently recent ordinary nowhere-zero-flow reconfiguration machinery
cannot be imported as a base-pair proof merely by restricting its moves to
anisotropic flows.  A universal argument must compare distinct
reconfiguration components, use a larger move, or bypass reconfiguration.

## O37 — Standard low-arity polymorphism closure

Status: **FAILED APPROACH**, excluded by independently checked LRAT
certificates.

The cubic \(D_5\) vertex rule is the ordered ternary relation
\[
 R(a,b,c)\quad\Longleftrightarrow\quad
 a,b,c\in\binom{[5]}2,\qquad a+b+c=0.
\]
Equivalently, \(a,b,c\) are the three edges of a triangle in \(K_5\).
Every boundary relation obtained by existentially gluing copies of this
local relation must be preserved by its polymorphisms.  This suggested
trying to exclude the published exceptional signatures with a standard
binary, majority, minority, or cyclic closure operation.

Deterministic finite searches instead prove that \(R\) has:

```text
no nonprojection idempotent binary polymorphism
no ternary majority polymorphism
no ternary minority polymorphism
no idempotent cyclic ternary polymorphism
```

The four ordinary CNFs contain respectively 364,612; 4,336,400;
4,336,400; and 4,344,950 clauses.  CaDiCaL produced LRAT certificates,
and the separately built `lrat-check` accepts all four.  The generators,
compressed proofs, replay, dimensions, and SHA-256 values are frozen in
`search/d5-triangle-polymorphism-no-go-20260727/`.

This does not classify every higher-arity polymorphism and does not show
that either exceptional relation is realizable.  It closes only the usual
low-arity universal-algebra shortcut: any successful algebraic invariant
must be subtler than these standard closure identities.

## O38 — Uniformly bounded Fano-flow reconfiguration

Status: **FAILED APPROACH / HUMAN-CHECKABLE INFINITE LOWER-BOUND FAMILY /
POSITIVE THREE-CDC CONTROLS**.

A recursive family now rules out every universal constant bound on the
number of connected-circuit switches needed to reach a Fano-good
\(\mathbb F_2^3\)-flow.  The host \(H_d\) has \(3^d\) leaf ports and every
connected circuit meets at most \(2^d\) of them.  Grafting one certified
all-seven-bad block at every port gives a connected simple bridgeless cubic
graph \(G_d\) with
\[
 |V(G_d)|=15\cdot3^d-5.
\]
Each switch can touch at most \(2^d\) bad-block footprints.  If fewer than
\(\lceil(3/2)^d\rceil\) switches are used, one block and both of its
connectors remain unchanged; its two-\(T\)-join obstruction excludes every
Fano-good line.  Thus every path from the displayed flow to the good-flow
set has length at least
\[
 \left\lceil(3/2)^d\right\rceil
 =\Omega\!\left(|V(G_d)|^{\log_3(3/2)}\right),
\]
if such a path exists.

Every \(G_d\) is explicitly three-edge-colourable and therefore has a
three-cycle double cover.  The result refutes only constant-radius
domination; it does not refute eventual good-flow domination in every
reconfiguration component and does not refute Five-CDC.  The first
40-vertex member has exact distance two: the two displayed switches and all
seven component-defect rows are replayed by the independent checker
`scratch/verify_fano_multistep_two_switch.py`.  The proof and exact
literature audit are in
`scratch/fano-multistep-reconfiguration-audit-20260727.md`.

## O39 — Internal pole connectivity forces full fixed-five signature

Status: **FAILED BROAD LEMMA / EXPLICIT ORDER-16 HUMAN COUNTERMODEL /
FOCUSED CAP VERSION OPEN**.

The terminal-distinct order-16 pole

```text
O????A?[BOI_g_Ao?kCo?
```

is connected, simple, bridge-free, and has exact cyclic connectivity four,
but its exact fixed-five boundary mask is `0x3fe`: it misses \(AA\).  Three
of its terminals \(5,7,8\) have a common neighbour \(14\).  If every
semiedge had label \(A\), applying
\[
 p_A(B)=|A\cap B|\pmod2
\]
would give value one on all three proper edges at vertex \(14\), contrary
to its parity equation.  Two independently written classifiers agree on
the other nine states.

Every simple cap of this pole creates a cyclic triangle cut, so it does not
refute the focused conjecture for poles obtained by deleting two independent
edges from a cyclically four-edge-connected non-Tait cubic graph.  In that
focused geometry, a new human lemma proves that every component outside the
four cap-edge endpoints has an even number of attachments.  This eliminates
the scalar \(AA\) parity obstruction, but not the simultaneous \(D_5\)
lift.  Exactly, \(AA\) is equivalent to an \(\mathbb F_2^2\)-flow whose
zero set contains the prescribed edge pair and whose complement packs two
edge-disjoint boundary joins.  That prescribed-zero packing theorem remains
open.  Full details are in
`scratch/fixed-five-d5-four-pole-full-signature-frontier.md`.

The rooted-minimum shortcut is now also classified.  For a rooted
inclusion-minimal exact zero matching \(M\supseteq R\), every quotient
\(Q_c-R\) is a forest, but not every rooted cardinal-minimum matching
packs.  A 22-vertex simple cubic cyclically 4-edge-connected non-Tait
example has a nonpacking rooted minimum \(\{24,27,31\}\); a literal
root-preserving neutral switch reaches the packing minimum
\(\{13,24,27\}\).  The human obstruction and standard-library replay are
in `scratch/focused-aa-rooted-minimum-frontier.md`.  This refutes only the
all-minima strengthening.  Rooted feasibility and the existential
neutral-component statement remain open.

The perfect-matching shortcut has a sharp replacement.  For any
3-edge-connected cubic graph and independent roots with endpoint set
\(U\), Tutte--Berge gives
\(\operatorname{def}(G-U)\le2\).  In the deficiency-two case, the
complement of a rooted near-perfect matching suppresses either to a theta
or to a loop--link--loop dumbbell, and it supports a nowhere-zero
\(\mathbb F_2^2\)-flow exactly in the theta case.  Cyclic
four-connectivity makes every tight barrier almost entirely singleton and
puts a nonroot matching chord across every dumbbell-link bridge, but the
alternating exchange that would force a theta is not yet proved.  The
theta assertion already fails on a checked 10-vertex
3-edge-connected cubic graph; that control is Tait-colourable and has a
cyclic three-edge cut, so it lies outside the focused domain.  See
`scratch/prescribed-root-matching-deficiency-frontier.md`.

No focused limitation appears through order 30.  Two independent exact
implementations classify all 136,557,951 independent root pairs in the
retained complete cyclically-four non-Tait corpora at every even order
from 10 through 30: 135,214,569 have deficiency zero, and all 1,343,382
deficiency-two pairs admit a theta maximum; zero pairs are all-dumbbell.
Every deficient bounded instance has \(|\delta(U)|=8\).  The exact
unproved step is now a rotation-closure lemma turning one of the
matching chords across a bad link cut into an alternating switch that
strictly decreases the number of complement bridges.  See
`search/focused-theta-choice-through28-20260727/`,
`search/focused-theta-choice-order30-20260727/`, and
`scratch/focused-theta-choice-census-frontier.md`.

The purely local rotation-closure strengthening is false even after
adding non-Taitness.  The checked 18-vertex graph
`Q???C@?GF?CKSOF?AQ?W_B_AA_?`, with roots \(\{12,20\}\), has deficiency
two and 40 maximum matchings; every complement is a dumbbell, although
the 384-edge elementary exchange graph is connected.  Its canonical
barrier has a nontrivial boundary-three factor-critical component, and
the roots plus the never-selected barrier edge form a cyclic
three-edge cut.  Hence it misses exactly the global cyclic-four
hypothesis.  The exact singleton-barrier cyclic-four lemma and the
one-boundary-five case remain open.  See
`scratch/boundary-eight-rotation-closure-frontier.md`.

The all-singleton branch is nevertheless closed for the **standard**
Five-CDC by a different argument.  Write its Gallai--Edmonds partition as
\(V(G)=D\dot\cup W\), where \(D\) is independent and
\(|W|=|D|+2\).  Cubic degree counting forces exactly three edges inside
\(W\).  A perfect matching through any prescribed one of those edges
contains exactly one of the three.  Its complementary 2-factor therefore
has only two non-\(D\)--\(W\) edges, and hence zero or two odd cycles.
Huck--Kochol (1995) gives a standard five-cycle double cover.  Thus the
unresolved prescribed-root theta lemma is stronger than is needed to
dispose of this branch as a possible standard counterexample.  The only
standard obstruction left by this barrier route is the one-boundary-five
branch.  See `scratch/root-insertion-two-factor-frontier.md`.

The independent whole-shore cyclic-three route is also complete through
cap order 26.  Across 13,901 retained triangle-free 3-connected non-Tait
caps at orders 20, 22, and 24, two exact implementations classify all
330,790 vertex deletions and 10,824,084 proper roots.  Every normalized
root signature is nonempty and contains a base pair, with byte-identical
complete transcripts.  The human triangle induction transports this as
a fork through endpoint \(K_4\) factors, and two opposing forks exclude
the mixed exceptional relation.  See
`search/rooted-three-pole-c3-cap-frontier-through24-20260727/`.

The remaining finite order-28 cyclically-four branch is now closed.
Across all 12,517 retained caps and 9,725,709 independent-edge
deletions, every pole has explicit orbit-0 and orbit-2
\(D_5\)-labellings.  Those two positive witnesses exclude all six
exceptional exact masks, and two separately written full-stream
checkers pass all 19,451,418 labellings.  Combining this with the
cyclic-three endpoint-fork theorem and even pole order raises the scoped
simple terminal-distinct fixed-five exceptional-pole lower bound to
30.  This remains a bounded structural theorem, not a universal
full-signature theorem or a Five-CDC resolution.  See
`search/four-pole-order28-cyclic4-cap-20260727/`.

## O40 — Small five-pole caps force a fork in every rooted signature

Status: **FINITE GADGET SHORTCUT STALLS / EXACT EXPLORATORY CENSUS /
NO UNIVERSAL NO-GO CLAIM**.

Cutting a distinguished root with label \(A\) turns a rooted three-pole
into a five-pole with normalized boundary word
\[
                         (01,02,12,A,A).
\]
This suggested capping the five boundary ends by a strictly smaller
five-pole.  Minimality would then force the root signature to meet the
cap's admitted \(A\)-set.  A sufficiently rich family of caps might have
forced every surviving signature to contain a fork triple.

The exact small-cap probe does not do so.  Two independently structured
implementations agree through order nine.  The faster direct-CSP
implementation then enumerates every connected simple cap core with five
degree-two terminals and all other vertices cubic through order \(13\):
\[
                       1+6+52+536+6374=6969
\]
input cores, of which 6894 pass the gluing-admissibility test.  That test
retains a cap when every internal bridge has terminals on both sides, the
condition which makes the bridge lie on a cycle after gluing to a
connected opposite rooted core.  Over all terminal permutations it finds
the same 22 distinct admitted \(A\)-sets at every new order.  Requiring a
\(3\leftrightarrow4\)-invariant root signature to hit every one of those
sets still leaves ten fork-free signatures.  Their seven maximal members
are
\[
\begin{gathered}
\{01,02,12\},\\
\{01,02,03,04\},\quad
\{01,12,13,14\},\quad
\{02,12,23,24\},\\
\{01,03,04,13,14,34\},\\
\{02,03,04,23,24,34\},\\
\{12,13,14,23,24,34\}.
\end{gathered}
\]
Thus these cap inequalities alone do not imply the fork theorem, even
before proving the required strict-size and minimum-counterexample
hypotheses.

There is a simple reason the stabilization is structural rather than a
numerical accident.  Each of the seven displayed maximal fork-free sets
meets every one of the three base pairs \(P_0,P_1,P_2\).  Consequently it
meets every cap admission set which itself contains a base pair.  Adding
any number of caps already covered by the desired base-pair theorem can
never eliminate any of the seven abstract survivors.  A pure
existential-hitting proof of base-pair closure would therefore have to use
a cap whose own root signature violates base-pair closure, or retain
richer information than its admitted \(A\)-set.  The former would be a
counterexample to the target rather than a proof of it.

The exploratory producer and retained outputs are
`scratch/rooted_five_pole_cap_hitting_probe.py`,
`scratch/rooted_five_pole_cap_hitting_probe.cpp`,
`scratch/rooted-five-pole-cap-hitting-order5-7-result.json`, and
the corresponding `scratch/rooted-five-pole-cap-hitting-*-cpp-result.json`
files through order 13.  This finite failure does not prove that larger or
purpose-built caps are useless.  It shows that extending the naive cap
family through order 13 adds no new root-admission set and prevents
silently treating small-cap hitting as the missing universal base-pair
argument.

## O41 — Thinning a Jaeger star flow to five values

Status: **FAILED APPROACH / DUAL-CERTIFIED FINITE COUNTERMODEL**.

On the retained 34-vertex simple bridgeless cubic graph, root zero, every
Fano direction occurs at least twice in every fixed-star packing that would
support the proposed thinning conclusion.  The complete
`star-thin-any.cnf` is UNSAT; its LRAT is accepted independently by
`lrat-check` and the verified CakeML `cake_lpr` checker.  The same fixed
star fibre nevertheless has an explicit support-five pair labelling, so
this is not a Five-CDC counterexample.  It proves only that support five
cannot be forced by making some flow value occur at most once.  See
`output/jaeger-star-thinning-countermodel-34v/` and
`scratch/verify_jaeger_star_thinning_countermodel_34v.py`.

## O42 — Fix the third tree, then repair the other two

Status: **FAILED APPROACH / EXACT SMALL COUNTERMODEL**.

In the cube at root zero, one displayed extendible third tree has 16
ordered residual completions and all 16 fail the required quotient parity,
although another jointly chosen triple succeeds.  Of 132 extendible third
trees in that star fibre, 12 are bad.  Hence an arbitrary \(T_3\) cannot be
frozen before choosing \(T_1,T_2\).  The exact existential star-packing
lemma survives.  See `scratch/jaeger-fixed-third-tree-parity-no-go.md` and
`scratch/check_jaeger_fixed_third_tree_parity_no_go.py`.

## O43 — Force two odd-side forests to be disjoint

Status: **FAILED APPROACH / HUMAN PETERSEN OBSTRUCTION**.

If two edge-disjoint spanning subgraphs of a cubic graph have odd degree at
every vertex, both are perfect matchings and their union is an even
2-factor.  Every Petersen 2-factor consists of two 5-cycles, so no two
odd-side forests \(K(T_i),K(T_j)\) can be disjoint.  A complete independent
enumeration checks all 4,416 ordered star packings at each Petersen root,
while also finding 384 parity-good packings.  Thus emptiness of
\(K(T_i)\cap K(T_j)\) is strictly stronger than the needed contracted
Eulerian condition.  See `scratch/jaeger-k-forest-star-parity-identities.md`
and `scratch/verify_jaeger_k_forest_petersen.py`.

## O44 — Choose Scott-perfect forests first, then extend

Status: **FAILED APPROACH / HUMAN MATROID-RANK OBSTRUCTION**.

For a labelled 10-vertex Möbius ladder and a fixed root, three displayed
perfect matchings respect all star-fibre capacities, use the three root
edges separately, and even have \(K_1\cap K_2=\varnothing\).  Nevertheless
they have no simultaneous extension to three spanning trees: a ten-copy
residual subset has contracted graphic ranks \(3,3,3\), contradicting the
necessary matroid-union inequality \(10\le3+3+3\).  A separate exhaustive
assignment check returns zero extensions, while another forest triple on
the same graph does extend.  Thus Scott's perfect-forest theorem must be
coupled to the full family of matroid-union inequalities.  See
`scratch/jaeger-perfect-forests-first-no-go.md` and
`scratch/check_jaeger_perfect_forests_first_no_go.py`.

## O45 — Never increase one fixed-coordinate star-parity defect

Status: **FAILED APPROACH / EXACT HUMAN-CHECKABLE COUNTERMODEL**.

On graph6 `M?AA@BORDGEOEOAo?`, root zero, the displayed three-tree packing
has two bad components for one preselected Fano coordinate.  It has exactly
18 legal reciprocal
two-tree exchange neighbours, all of defect four, and no same-level or
descending neighbour.  The remaining 90 of 108 candidate swaps violate a
tree condition.  Thus this state is a trapped singleton at defect two for
that coordinate.  Its full seven-plane profile is
\((2,4,2,2,0,6,2)\), so it is already support-five-good in a different
plane; a reciprocal exchange also lowers the symmetric minimum in another
coordinate.  This refutes only preselected-coordinate descent.  It is not
a Five-CDC counterexample and does not refute the seven-plane potential.
See `scratch/jaeger-star-parity-descent-countermodel.md`.

## O46 — Replace contracted parity by graphic closure in every Type-A fibre

Status: **FAILED APPROACH / EXACT EXHAUSTIVE COUNTERMODEL**.

The sufficient condition
\(K_1\cap K_2\subseteq\operatorname{cl}_{M(G)}(K_3)\) replaces “even
degree after contracting \(K_3\)-components” by the stronger demand that
every relevant edge become a quotient loop.  On graph6
``K?`@E`gFCKEO``, the two automorphic Type-A defect triples
\(\{0,4,11\}\) and \(\{1,3,10\}\) each have 355,392 ordered spanning-tree
packings.  None is closure-good in any coordinate, although 7,704
packings satisfy the exact component-parity condition in one coordinate.
An independent checker reconstructs all 8,640 spanning trees and
exhausts every packing without using the SAT producer.  This rules out the
generic Type-A/B closure theorem only.  A vertex-star fibre has the extra
four-cocycle \(\delta(r)\cup\{p\}\) in the parity-element extension.  The
later countermodel in O47 shows that this extra structure still does not
force closure.  See
`scratch/jaeger-parity-element-and-kernel-closure-no-go.md`.

## O47 — Replace exact star-component parity by graphic closure

Status: **FAILED APPROACH / DUAL-CHECKED VERTEX-STAR COUNTERMODEL /
INFINITE FAMILY**.

In graph6 `O??CA?_ceOGgH_F?AK@P?`, rooted at vertex 13, none of the
5,723,136 ordered star-fibre packings satisfies
\[
K_i\cap K_j\subseteq\operatorname{cl}(K_k)
\]
in any coordinate.  The graph is simple cubic, 3-edge-connected, and
3-vertex-connected.  A direct cographic-base partition counter enumerates
the whole fibre; independently, a 744-variable, 101,037-clause CNF is
UNSAT and its LRAT proof is accepted by both `lrat-check` and verified
CakeML `cake_lpr`.

The exact component-parity target survives strongly: 40,464 packings pass
it, and a literal five-point pair labelling gives a short independent
witness.  In that witness, the four common-kernel edges form a quotient
4-cycle rather than quotient loops, exposing exactly what closure
incorrectly forbids.

Triangle contraction gives a human infinite-family theorem.  A star
packing rooted outside an expanded triangle uses two triangle edges in
each tree; contraction preserves all external odd-kernel memberships.
Thus closure-goodness descends, and its contrapositive shows that
triangle-expanding any nonroot vertex preserves closure failure.  The
countermodel's three disjoint triangles contract to Petersen and form one
alternating class of the bad root's distance-two 6-cycle.  See
`scratch/jaeger-star-kernel-closure-countermodel-16v.md` and
`scratch/jaeger-star-kernel-closure-triangle-expansion.md`.

## O48 — Force symmetric descent in one reciprocal exchange

Status: **FAILED APPROACH / EXACT HUMAN-CHECKABLE COUNTERMODEL**.

On graph6 `O??CA?_ceOGgH_F?AK@P?`, root 13, the explicit star-fibre
state with omitted masks `857601,1059160,180390` has exact profile
\((4,4,4,2,4,6,4)\).  Exhausting all 147 candidate reciprocal swaps
gives 23 legal neighbours, 18 still at \(d_{\min}=2\) and five at
\(d_{\min}=4\); none descends.

This is not a trap for the same-level-component theorem.  The
kernel-inert exchange `(coordinates 0,1; edge IDs 19,6)` leaves all
three kernels and the full profile unchanged.  It exposes the exchange
`(coordinates 0,2; edge IDs 22,7)`, which then reaches profile
\((2,2,2,2,4,6,0)\).  Thus the exact obstruction is to immediate
averaging; a valid proof must use neutral realization changes.  See
`scratch/jaeger-fano-min-immediate-descent-countermodel.md`.

## O49 — Deduce descent invariance from triangle contraction alone

Status: **FAILED APPROACH / HUMAN PRODUCT THEOREM AND EXACT SCORE
COUNTEREXAMPLE**.

Nonroot triangle expansion gives an exact Cartesian product of the
star-fibre exchange graph with the transposition Cayley graph of \(S_3\).
However the defect score is not pulled back from the contracted factor.
For one contracted state with profile \((2,4,2,2,0,6,2)\), the six
omitted-triangle assignments have four profiles with \(d_{\min}=0\) and
two with \(d_{\min}=2\).  Therefore the exchange-graph product and
preservation of external odd-kernel membership do not prove descent
invariance.  See
`scratch/jaeger-triangle-expansion-descent-structure.md`.

## O50 — Expose descent while keeping the odd-kernel triple fixed

Status: **FAILED APPROACH / EXACT HUMAN-CHECKABLE COUNTERMODEL**.

On graph6 `O??CA?_ceOGgH_F?AK@P?`, root 13, the state with omitted
masks `1722528,307976,66647` has exact profile
\((4,4,4,4,6,2,2)\).  All 147 incident reciprocal swaps are tested.
Exactly 23 are legal; every one remains at \(d_{\min}=2\), and none
preserves the ordered triple of odd kernels.  Hence the state's
fixed-kernel realization component is a singleton and cannot expose a
descending exchange.

The full same-level route still escapes in two steps.  The first,
necessarily active, exchange changes the masks to
`1722504,308000,66647` and the profile to
\((4,2,2,4,6,2,2)\).  A second exchange reaches masks
`1595528,434976,66647` and profile \((6,4,4,4,4,4,0)\).
Thus a prospective proof must permit active same-level exchanges, not
only neutral re-realizations of one kernel triple.  See
`scratch/jaeger-fano-min-immediate-descent-countermodel.md` and its
independent checker.

## O51 — Force a packing pair from an affine-complement collision (APX)

Status: **FAILED APPROACH / EXACT CYCLICALLY-4 NON-TAIT COUNTERMODEL**.

The affine pair-exchange axiom is false on graph6
`chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH`.
The graph is simple cubic, girth five, cyclically 4-edge-connected, and
non-3-edge-colourable.  A displayed bad nowhere-zero
\(\mathbb F_2^3\)-flow has 33 affine-compatible line occurrences,
representing 32 distinct value-class edge pairs, but none of those pair
deletions packs two boundary \(T\)-joins.

The standard-library checker exhausts all 221 perfect matchings, every
edge cut of size at most three, and 198 packing queries by complete binary
cycle-space enumeration.  An independent C++/CaDiCaL implementation also
returns APX score zero.  The counting identities survive, but the global
budgets are \(L_B(H)=0\), separated lower bound \(9\), and \(3Q=402\).

This refutes only APX.  The same graph has a literal standard five-cover,
and the same flow has 6,699 good switches among 9,532 legal
connected-circuit switches.  See
`scratch/fano-apx-countermodel-order36.md`.

## O52 — Lift an already selected good state through a square

Status: **FAILED APPROACH / EXACT MINIMUM-ORDER STATE COUNTERMODEL**.

On the planar order-eight graph6 `G?zTb_`, root zero, the displayed
star-fibre state has profile \((2,2,0)\). Replacing the independent edges
\((1,7)\) and \((2,4)\) by a square gives \(3^8=6561\) omitted-owner
assignments. Exactly 72 are legal three-tree lifts, with profile histogram
\[
(2,2,2):38,\quad(2,2,4):12,\quad(2,4,2):2,\quad
(4,2,2):2,\quad(4,4,2):18.
\]
No lift is good in any coordinate.

This refutes only fixed-state local lifting. Another good state for the
same graph, root, and smoothing pair has a good local lift. Both order-six
graphs satisfy the stronger statewise claim, while a complete order-eight
census finds a jointly chosen good state and lift in all 672
graph/root/pair instances. Later complete censuses extend the whole-fibre
frontier through order 14; the final 572,880-witness layer is replayed by a
separately written checker. The whole-fibre existential square reduction
remains open. See
`scratch/jaeger-star-square-any-coordinate-lift-no-go.md`.

## O53 — Use the sorted seven-defect profile as a one-step potential

Status: **FAILED APPROACH / EXACT ORDER-36 COUNTERMODEL**.

The explicit state in
`scratch/jaeger-sorted-profile-local-no-go-order36.md` has profile
\((6,6,2,4,2,2,2)\) and sorted profile
\((2,2,2,2,4,6,6)\).  Of 867 reciprocal candidates, exactly 63 are legal:
zero are lexicographically lower, 13 are equal, and 50 are higher.  The
independent standard-library checker reconstructs every tree, odd kernel,
defect, and exchange.  A checked two-exchange same-level path reaches
defect zero, so this refutes only one-step majorization, not the full
plateau-component theorem.

## O54 — Generate counterexamples by covers or the tested Petersen four-pole

Status: **FAILED COUNTEREXAMPLE FAMILIES / HUMAN POSITIVE REDUCTIONS**.

Every finite cover of a FiveCDC-positive graph is positive by taking edge
preimages coordinatewise.  Every replacement of two independent edges by
the Petersen four-pole obtained from deleting adjacent vertices is also
positive for every port bijection.  The latter has a 13-row pair-label
certificate independently checked on all 550 boundary assignments.  These
operations cannot produce a counterexample from a positive base; they do
not prove that every graph reduces by such operations.

## O55 — Generate counterexamples by arbitrary-port Heawood insertion

Status: **FAILED COUNTEREXAMPLE FAMILY / FULL-BOUNDARY POSITIVE THEOREM**.

The Heawood four-pole obtained by deleting adjacent vertices extends all
640 xor-zero ordered \(D_5\) boundary words.  Its ten-row orbit certificate
is independently checked, and an edge-by-edge argument proves arbitrary
port insertion preserves bridgelessness.  Hence this genuine non-covering,
girth-six substitution cannot create a FiveCDC counterexample from a
positive base.  The theorem does not make the configuration unavoidable.

## O56 — Select a square-compatible downstairs FiveCDC by relabelling

Status: **FAILED APPROACH / HUMAN THREE-CUT OBSTRUCTION**.

For any three-edge cut, coordinatewise Eulerian cut parity implies that
its three weight-two labels xor to zero.  Consequently they are
\(\{0,1\},\{0,2\},\{1,2\}\) up to \(S_5\), and intersect pairwise once.
On the triangular prism, choose the two nonroot matching edges in the same
three-cut.  No FiveCDC can label them equally or disjointly, even though an
explicit star state and square-local lift both have exact-good profile
\((2,0,2)\).  This kills only the fixed-label selection bridge, not the
whole-fibre square implication or FiveCDC.  See
`scratch/jaeger-square-fixed-label-selection-cut-no-go.md`.

## O57 — Bound every same-level plateau escape by three

Status: **FAILED APPROACH / EXACT ORDER-40 SEPARATOR**.

The literal state in
`scratch/jaeger-plateau-radius-three-no-go-order40.md` has \(d_{\min}=2\)
and complete same-level ball layer sizes \(1,13,108,836\) through radius
three.  Exhausting 1,037,514 candidate swaps finds 67,392 legal oriented
arcs, with no defect-zero boundary before layer three.  A displayed fourth
exchange reaches defect zero, so the exact plateau escape distance is four.
The state escapes and its full plateau component is not claimed trapped;
the unbounded component theorem and FiveCDC remain open.

## O58 — Force plateau descent by profile-only defect averaging

Status: **FAILED APPROACH / EXACT ADJACENT-STATE COUNTERMODEL**.

Two adjacent order-40 star states have the identical ordered profile
\((8,2,8,8,6,10,10)\) but legal degrees 65 and 63.  Complete incident
enumeration gives coordinate Laplacians
\[
(-12,140,-6,-6,28,-40,-94)
\quad\hbox{and}\quad
(-16,134,-6,-2,34,-58,-100),
\]
so the Laplacian of total defect is respectively \(+10\) and \(-14\).
Thus it is neither a function of the current ordered profile nor
universally one-signed.  Summing over a plateau gives only the ordinary
boundary-divergence identity and does not determine the exterior sign.
See `scratch/jaeger-plateau-profile-laplacian-no-go.md`.

## O59 — Generate counterexamples by arbitrary-port cube insertion

Status: **FAILED COUNTEREXAMPLE FAMILY / MINIMUM FULL-BOUNDARY POSITIVE
THEOREM**.

The four-pole obtained by deleting adjacent vertices from the cube extends
all 640 xor-zero ordered \(D_5\) boundary words.  Its ten-row orbit
certificate is independently checked, and the generic insertion proof
shows that every port bijection preserves FiveCDC and bridgelessness.
Moreover this six-vertex core is minimum-order among connected simple
terminal-distinct cubic full-boundary four-poles: the unique order-four
core is \(C_4\), whose exact relation misses the 60-word orbit represented
by `02 02 03 03`.  Thus cube insertion cannot create a counterexample from
a positive base.  The theorem does not show that the cube pole is
unavoidable in a minimal counterexample.

## O60 — Glue arbitrary clean Fano cap flows across a small cut

Status: **FAILED APPROACH / EXACT SIGNED-PARTITION COMPOSITION LAW**.

The exact shore state for a fixed Fano line is a partition of the
line-valued terminals by internal line connectivity, with one affine
defect bit per block.  Global components are the components of the
bipartite block graph formed by the line-valued cut edges, and each must
have zero xor defect.  For four line terminals this already gives 47
parity-compatible signed states, so a boundary value word alone is
incomplete.

The failure is literal at a two-cut.  Two displayed \(K_4\) cap flows have
clean selected lines and signed endpoint states \((0,0)\) and \((1,1)\).
Joining corresponding cap ends makes two dirty global components.  The
eight-vertex glued graph is simple, bridgeless, cubic, Tait-colourable, and
has an explicit FiveCDC.  Therefore the example refutes only fixed-flow
cap gluing; a valid reduction may change flows but must align the full
signed states.  The proof, tables, and independent replay are in
`scratch/fano-clean-line-signed-partitions-20260728.md`.

## O61 — Compose the order-18 six-bad Fano flow into a cyclic-4
all-seven obstruction

Status: **FAILED BUILDING-BLOCK ROUTE / EXACT THREE-CUT LOCK**.

The graph6 core `Q???C@?K@O@aDAw?GW?J?_g?Y??` was mistakenly treated
during exploration as cyclically 4-edge-connected.  It has the cyclic
three-cut with edge ids \(14,18,26\), splitting it into connected
nine-vertex shores with twelve induced edges each.

For all 27 adjacent-vertex-deletion four-poles, a standard-library
enumerator reconstructs the 1024 binary pole cycles and evaluates the
exact completion-sound two-cycle formula.  The twelve internal deletions
on the two sides have respective local UNSAT profiles
\(\{4,5,6\}\) and \(\{1,3,7\}\); the three cut-edge deletions have empty
profile.  Every nonempty-profile pole retains the opposite cyclic shore
behind three boundary incidences.  Hence any completion with a cyclic
outside, including every multi-pole macro, has a cyclic three-cut.
Linear relabelling changes the functional names but not this topology.

Thus this core cannot generate the desired cyclically 4-edge-connected
seven-projection obstruction by union of local UNSAT profiles.  Different
cores and the FiveCDC conjecture remain open.  See
`scratch/fano-six-bad-threecut-lock-20260728.md`.

## O62 — Every fixed Fano flow on a cyclically 4-edge-connected cubic
graph has a clean projection

Status: **FAILED APPROACH / EXACT ORDER-60 COUNTERMODEL**.

Two explicitly relabelled deleted-edge four-poles from one order-32 flow
have completion-sound local bad-functional profiles
\(\{5,6,7\}\) and \(\{1,2,3,4,5\}\).  Gluing equal-valued ports gives a
simple cubic order-60 graph with a nowhere-zero \(\mathbb F_2^3\)-flow.
Because every local closed factor component remains a global component,
the union of the two profiles proves that none of the seven fixed
functional projections can be cleaned.

A solver-independent C++ checker enumerates all \(2^{17}\) first pole
cycles for each local functional and decides the remaining cycle by exact
binary Gaussian elimination.  It also checks all 121,575 edge sets of
sizes one through three, proving cyclic edge-connectivity at least four.
The same graph has an explicit semantically checked standard FiveCDC.
Thus the result refutes only universal cleaning of an arbitrary fixed
flow.  It confirms that the existential flow choice in the
Hušek--Šámal formulation cannot be dropped.  See
`scratch/fano-cyclic4-allseven-order60-20260728.md`.

## O63 — Direct H--S radius-one domination on the reduced snark domain

Status: **FAILED APPROACH / EXACT STRICT ORDER-26 COUNTERMODEL**.

The retained order-26 graph is simple cubic, cyclically
4-edge-connected, non-Tait, and has girth five.  Its displayed
nowhere-zero \(\mathbb F_2^3\)-flow has defect profile
\((6,6,4,6,2,4,4)\), and its value-4 class already packs two disjoint
boundary joins.  Complete simple-cycle enumeration gives 9,213 cycles
and 1,485 legal value switches; every neighbour remains dirty.  A
separately written standard-library checker also checks the packing,
graph premises, and an explicit FiveCDC.

The state is not a multi-switch obstruction: a displayed two-switch
path reaches profile \((4,6,4,0,6,4,4)\), so its exact distance is two.
This refutes radius one even for an already packable strict state, but not
FiveCDC or unrestricted H--S reconfiguration.  See
`scratch/husek-samal-one-switch-reduced-frontier-20260728.md`.

## O64 — Connected binary-cycle repair to a packable value class

Status: **FAILED OUTSIDE CYCLIC-4 / EXACT ORDER-108 COUNTERMODEL**.

The proposed binary repair chooses an even support avoiding one Fano
value class, switches by that value, and asks that one target value class
pack.  Targets paired by translation are equivalent, leaving 21 Fano
point--line incidences.

A connected order-36 state fails seven incidences.  Three explicit linear
relabelings partition all 21 incidences among three copies.  Two crossed
cubic 2-sums give a connected simple bridgeless cubic order-108 graph.
The full selector-gated formula for all 21 global repairs has 10,227
variables and 51,193 clauses and is UNSAT.  Both `lrat-check` and
CakeML `cake_lpr` accept the LRAT; an independent semantic checker
reconstructs every clause.

The graph has girth five and exactly two cyclic 2-edge cuts.  It also has
an explicit standard FiveCDC.  Hence this refutes connected binary repair
but leaves open the cyclically 4-edge-connected, girth-ten version that
would suffice for FiveCDC.  See
`search/fano-binary-repair-connected-countermodel-108v-20260728/`.

## O65 — Some globally minimum Fano value class packs

Status: **FAILED APPROACH / CERTIFIED ORDER-130 COUNTERMODEL**.

The retained 130-vertex simple bridgeless cubic graph has
\(\rho_3=5\): an explicit nowhere-zero \(\mathbb F_2^3\)-flow has a
designated five-edge value class, and the separately checked
\(r_f\ge5\) LRAT gives the lower bound.  The complete
exact-zero-matching/two-cycle CNF at size at most five is UNSAT, with its
LRAT accepted by C and CakeML.  Therefore no globally minimum Fano value
class packs two boundary joins.

A size-six packing certificate and explicit FiveCDC exist.  Thus the
result refutes only minimum-value-class selection.  It does not refute
minimum-coordinate-projection selection: the latter parameter is exactly
42 on the same graph, with all 11,264 minima cleanable.  See
`search/minimum-fano-class-nonpacking-130v-20260729/` and
`search/minimum-projection-n130-20260729/`.

## O66 — One shortest cycle containing one affine matching is clean

Status: **FAILED INTERMEDIATE LEMMA / PETERSEN COUNTERMODEL**.

In the literal Petersen graph, the matching \(M=\{06,14,25\}\) is
contained in exactly two minimum binary cycles, both of size eight.  For
each minimum, the components of the complement have \(M\)-endpoint
parities \((1,0,1)\).  A dependency-free checker exhausts all
\(2^{15}\) edge subsets.

This does not realize the four synchronized affine matchings of an
extendable Fano projection.  It proves that any positive argument must
use their simultaneous flow constraints rather than a generic
one-matching shortest-\(T\)-join theorem.  See
`scratch/petersen-minimum-tjoin-countermodel-20260729/`.

## O67 — No counterexample to minimum-projection selection has support at
most twelve

Status: **CLOSED / HUMAN THEOREM EXCLUDES THE RANGE**.

For a globally minimum extendable projection \(h\), every circuit component
meets all four affine value classes.  An exact direct boundary oracle
exhausts every resulting support shape through total size ten.  It applies
an independent \(\operatorname{GL}(2,2)\) map inside each complement
component, solves the circuit vertex equations with arbitrary low values
on \(h\), and tests the repaired affine cut parities.  All 125,178 valid
dirty canonical word/partition states are cleaned.

At size eleven there are 14 direct-repair failures, all in the \(5+6\)
shape.  Each has an explicit boundary certificate for a size-five
extendable replacement, so none is globally minimum.  All 14 minimal
realizations are the triangle-expanded Petersen graph
`Kt?G?DIPOqCo`; its target size-eleven projection is genuinely
uncleanable, but its minimum extendable support is five and clean.

Thus no counterexample to the minimum-projection selection principle has
minimum size at most eleven.

At size twelve, two independent exact classifiers agree on 13,788,824
dirty boundary states.  Of these, 13,788,432 clean directly and 392 admit
a strict circuit deletion; zero survive both branches.  The 392 literal
deletion certificates are frozen and independently parsed.  Therefore no
counterexample has minimum size twelve either.  The theorem gives no universal
minimum-support bound and does not settle FiveCDC.  See
`scratch/minimum-projection-through12-clean-or-delete-20260729/`.

## O68 — No counterexample to minimum-projection selection has support at
most fifteen

Status: **CLOSED / EXACT FINITE BOUNDARY THEOREM**.

The size-thirteen classifiers enumerate 189,998,862 charge-valid states.
Of 159,369,966 dirty states, 159,362,292 clean directly and 7,674 have a
strict circuit deletion.  At size fourteen there are 2,255,478,176 dirty
states: 2,255,331,588 clean directly, 146,364 delete strictly, and 224
residual \(7+7\) states all have matching-robust Kempe deletion
certificates.  At size fifteen there are 31,088,622,592 dirty states:
31,086,255,789 clean directly, 2,360,767 delete strictly, and all 6,036
residual \(7+8\) states have realization-robust inverse Kempe escapes.

Thus global minimum projections of size at most fifteen are cleanable.
This was genuine finite structural progress, but it supplied no universal
support bound.

## O69 — Every globally minimum extendable projection is cleanable

Status: **FAILED APPROACH / EXACT 162-VERTEX STRICT-LOCK COUNTERMODEL**.

The retained simple connected bridgeless cubic graph has 162 vertices and
243 edges.  Its unique globally minimum extendable projection has size 54,
is the union of two 27-circuits, and has no clean extension.  An exhaustive
\(2^{14}\)-placement search proves that eight parity locks are necessary
and sufficient in the construction, with 180 minimum lock sets.

The graph has a direct FiveCDC assignment and a second compositional
FiveCDC.  Hence it refutes the minimum-selection proof strategy but not
FiveCDC.  Canonical graph encodings, a complete human proof, two
independently written audits, literal certificates, and hashes are in
`scratch/minimum-projection-strict-parity-lock-20260729/` and
`scratch/minimum-projection-strict-lock-minimized-independent-audit-20260729/`.

## O70 — Four affine rebases exhaust the minimum-projection exchange

Status: **FAILED INTERMEDIATE MODEL / EXACT FULL-FLOW CORRECTION**.

The four low flows \(s+c\,h\) attached to one extension do not exhaust
competing extendable projections.  The exact master problem ranges over
every low flow \(s'\), its zero set \(M=Z(s')\), and every
\(\partial M\)-join \(J\subseteq E-M\), with cost \(|M|+|J|\).
The retained 278-vertex graph has a displayed projection of size fourteen
satisfying all four static affine inequalities but a full-flow competitor
of cost seven.  Both checkers lift and verify the literal flows.

The correction is frozen in
`scratch/minimum-projection-full-flow-exchange-20260729/`.  It explains
why the static exchange argument was incomplete; the later strict lock
also proves that even a true master optimum need not clean.
