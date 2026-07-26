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

## O30 — Equality incidence/rotation forces a good selector

Status: **FAILED APPROACH**, proved by exact finite countermodel.

At ambient equality \(|V(G)|=88\), an all-mark-colour Tait colouring of
the suppressed core gives a connected 5-regular bipartite incidence
multigraph on eight \(ac\)- and eight \(bc\)-circuits, with the eight
marks forming a perfect matching.  Retaining cyclic port orders and twist
bits reconstructs the complete coloured core, so one might hope that
these equality data alone force a componentwise marked-even selector.

The explicit decorated incidence object in
`docs/equality88-incidence-rotation-countermodel.md` disproves that
inference.  It reconstructs a connected simple cubic 80-vertex core with
the required eight 10-cycles in both factors, but two independent
implementations enumerate all 256 selectors and find zero good.

This does not obstruct five-CDC.  The marked subdivision has an explicit
pair of edge-disjoint \(T\)-joins, while the core has girth three and
fails universal separation after one Kempe switch.  Any closure theorem
must genuinely use the remaining minimum-counterexample hypotheses rather
than incidence regularity and rotation data alone.  The separate
CVT[80,30] scan reinforces the distinction: all 74,940 of its eligible
factor-transversal records have at least 94 good selectors.
