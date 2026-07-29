# Five-cycle double cover laboratory

This repository is a machine-assisted research package for the five-cycle
double cover conjecture (5-CDC).  Its acceptance condition is:

> Given a finite undirected graph \(G=(V,E)\), find five indexed even
> (Eulerian) edge-subsets \(C_0,\ldots,C_4\) such that every edge belongs to
> exactly two of them.

The project does **not** currently claim a resolution.  Every result is
classified using the status vocabulary in the lab protocol.  In particular,
finite searches are not evidence of the universal statement.

The newest publication-candidate update is
`preprint-minimum-fano-projection/`.  It proves a simultaneous
minimum-support exchange theorem and an exact boundary-cleaning
theorem for every support shape through size fifteen in connected
bridgeless loopless cubic graphs.  The checker exhausts
proper affine circuit words, complement-component partitions, independent
componentwise \(\mathrm{GL}(2,2)\) maps, and repaired circuit values.  It
directly cleans all 125,178 valid dirty canonical states through size ten.
At size eleven it finds the first 14 direct-repair failures, but constructs
a size-five extendable replacement for each, excluding all of them by
global minimality.  At size twelve, two independent enumerators classify
all 13,788,824 dirty
states: 13,788,432 clean directly and 392 admit a strict circuit deletion,
so none survives global minimality.  At size thirteen, two independent exact classifiers agree on
all 189,998,862 charge-valid states: 159,369,966 are dirty, 159,362,292
clean directly, and the remaining 7,674 admit a strict circuit deletion,
with zero residuals.  At size fourteen the primary exact classifier
enumerates 9,481 word orbits and 2,616,134,989 charge-valid states.
Among 2,255,478,176 dirty states, 2,255,331,588 clean directly and
146,364 admit strict circuit deletion, leaving 224 residuals, all of
shape \(7+7\).  A second full \(7+7\) enumerator independently reproduces
all 333 word orbits, 91,481,505 charge-valid states, and the same 224
rows.  A graph-independent Kempe path argument in the split-occurrence
model, backed by 724 literal matching-robust certificates, gives every
residual a strict size-seven deletion escape.  Thus no residual can be
globally minimum.  At size fifteen, the exact classifier covers 26,492
canonical word orbits and 35,247,202,556 charge-valid states.  Among
31,088,622,592 dirty states, 31,086,255,789 clean directly, 2,360,767
admit a strict circuit deletion, and 6,036 residual \(7+8\) states are
all covered by realization-robust inverse Kempe lifts from size fourteen.
A human-checkable relative-\(\operatorname{GL}(2,2)\) tensor theorem
independently proves direct cleaning for every charge-valid one-circuit
boundary at arbitrary length.  Its circuitwise-balanced multi-circuit
corollary is sharp for direct cleaning: the Petersen graph gives the
smallest loopless two-occurrence abstract failure, but all 60 of its
interaction flows strictly delete a support circuit and an explicit
deletion reaches a clean global minimum of size five.  Consequently any
counterexample to the
proposed minimum-projection selection principle has minimum support at
least sixteen.

The unrestricted boundary dichotomy nevertheless fails sharply at size
fourteen: an explicit \(7+7\) state has an 18-vertex
simple bridgeless cubic realization whose size-fourteen projection has
15,360 extensions and no clean one.  The same graph has four cleanable
global minima of size five, so this refutes the proof method, not
FiveCDC; the new theorem escapes only after a support-neutral Kempe
recolouring.  Its exact finite evidence also includes
147,539 minima on frozen sources through
order 28, 433,730 minima on 7,661 retained order-34/order-40 strong-snark
rows, and a certified 130-vertex case with minimum size 42 and 11,264
cleanable minima.  The manuscript includes full proofs, exact replay
packages, and an AI-use disclosure.  This remains a partial theorem and
does **not** resolve FiveCDC.
The fixed-map translation search is reduced by a displayed human proof to
an affine XOR system in
`scratch/minimum-projection-fixed-map-affine-cleaning-20260729/README.md`;
the note derives dual-cut feasible moves and records the exact
size-fourteen failure of the unrestricted map-choice statement.  The
size-fourteen Kempe theorem is in
`scratch/minimum-projection-through14-cleanability-20260729/` and
`scratch/minimum-projection-size14-kempe-escape-20260729/`.  Larger support
sizes remain uncontrolled in general; the unresolved structural frontier
begins with unbalanced multi-circuit states at size sixteen.  The
size-fifteen census, independent lift audit, anchor audit, and universal
tensor proof are in the corresponding
`scratch/minimum-projection-size15-*` and
`scratch/minimum-projection-single-circuit-tensor-frontier-20260729/`
packages.  The Petersen interaction dictionary, two exact checkers, and
complete descent are in
`scratch/minimum-projection-two-occurrence-interaction-20260729/`.
The exact standard convention and a
self-contained graph-class reduction are now frozen in
`scratch/cubic-reduction-standard-fivecdc-20260729/`: the universal
assertion for arbitrary finite bridgeless multigraphs is equivalent to its
restriction to loopless cubic multigraphs, simple cubic graphs, and strong
snarks.  This does not extend the minimum-projection boundary theorem
itself beyond cubic graphs.

The static-exchange limitation is isolated in
`scratch/general-kempe-descent-static-exchange-obstruction-20260729/`.
A human proof shows that coloured \(K_4-e\) two-pole inflation can preserve
all local two-colour boundary pairings while forcing the four initial
minimum-exchange inequalities.  The 230-vertex witness defeats every
one-round fixed-colour path multiswitch and then escapes in two rounds.
It is Tait-colourable with minimum projection zero.  Hence it rules out
only a static one-round proof strategy: a viable general argument must use
the dynamic reapplication of exchange after each neutral recolouring.
The package contains two differently structured inequality checks, a full
boundary-profile reconfiguration census, exact hashes, and an explicit
AI-use/human-review warning.

The dynamic frontier is now sharpened in
`scratch/minimum-projection-dynamic-kempe-frontier-20260729/`.  A
human-checkable theorem there proves direct cleaning for a two-terminal
one-circuit subclass; the newer tensor package removes the two-terminal
restriction and proves the full abstract one-circuit statement.  The same
dynamic package proves that the edge-deleted
\(K_{3,3}\) two-pole is boundary-orbit-reflecting: chaining it transfers
any hypothetical goal-free dynamic boundary orbit to one satisfying all
four recomputed exchange inequalities after every reachable move.  It
does not find such an orbit or establish global support minimality.  Two
independently written checkers and a hostile agent audit pass; priority and
the proofs themselves still require independent expert human review.

The earlier `preprint-husek-samal-reconfiguration/` proves a human-checkable
packing-to-switch lemma and gives an exact cyclically 4-edge-connected
26-vertex snark flow showing that a packable value class can still require
two simple-cycle switches to reach the Hušek--Šámal component condition.
The standard-library checker exhausts every legal radius-one move and also
checks an explicit standard FiveCDC.  A related package,
`search/fano-binary-repair-connected-countermodel-108v-20260728/`, gives a
connected 108-vertex obstruction to a stronger binary-repair lemma, with a
51,193-clause CNF and LRAT accepted by both C and CakeML checkers.  Its two
cyclic 2-edge cuts keep it outside the minimum-counterexample domain.
Both results disclose AI use and make no FiveCDC resolution or priority
claim.

The newest exact handoff is
`ROOTED_RESOLUTION_FRONTIER_20260728.md`.  It gives the fully written
fixed-five minimum-counterexample reduction, the two-way rooted
edge-insertion equivalence, the resulting 3-edge-connected
girth-eight/short-cycle frontier, and the complete 195-edge elimination
screen on a 130-vertex cyclically 4-edge-connected girth-ten graph.  The
remaining rooted premise is explicitly unproved and is an exact
edge-extension form of FiveCDC, not a resolution.

A second current frontier starts from Jaeger's three-tree construction of
a nowhere-zero \(\mathbb F_2^3\)-flow.  In a vertex-star multiplicity
fibre, let \(K_i\) be the unique all-vertices-odd forest contained in the
spanning tree \(T_i\).  The canonical five-point lift exists exactly when
\(K_1\cap K_2\) has even boundary on every component of \(K_3\).  The
identity and a self-contained component-parity proof are in
`scratch/jaeger-k-forest-star-parity-identities.md` and
`scratch/jaeger-support5-component-criterion.md`.  Hušek and Šámal,
arXiv:2607.24724v1, independently give the equivalent flow-level
characterization in their Theorem 3.16 and retain the flow-selection step
as Conjecture 3.19; this project claims no priority for that criterion.
The exact star target is invariant under contracting or lifting a triangle
away from the root, by the seven-row human proof in
`scratch/jaeger-star-exact-parity-triangle-invariance.md`.  Every one of 804,204
feasible Type A/B fibres through order 14 passes, as do all 26,790 retained
order-38 and all 1,364 retained order-44 star fibres.  The order-44 package
contains literal witnesses checked by an independently written semantic
verifier.  The universal joint parity-and-tree-packing selection lemma is
still unproved.  Certified countermodels rule out three tempting
strengthenings: thinning a star flow to five values, fixing the third tree
before repair, and choosing parity-good perfect forests before simultaneous
tree extension.

The consolidated outcome is in `docs/lab-report.md`.  Exact conventions,
encodings, literature status, experiments, and open proof obligations are
recorded under `docs/`. The complete deterministic handoff is in
`REPRODUCING.md`; run `sh tools/verify_all.sh` for the non-destructive master
verification.

The current publication draft is in `preprint/`.  It presents the explicit
stable \(D_5\)-tile construction for the frozen figure transcription of the
Mattiolo--Negrini--Pagani family, with a full AI-use disclosure and a
novelty audit explaining why Huck--Kochol already implies existence for the
author-defined family.  It is a review draft, not a universal resolution or
a circulation-ready manuscript.  An independent assessment of the newer
minimum-support and cap results is in `preprint-structural/NO-GO.md`; it
recommends against a second preprint because the universal exchange theorem
is still missing and the main framework overlaps published 4-flow,
\(T\)-join, and multipole-boundary methods.

The independent \(K_6\)-reformulation publication audit is in
`preprint-k6/NO-GO.md`.  It likewise recommends **no standalone preprint**:
the duad/syntheme encoding substantially overlaps Král' et al. (2009), and
the relevant spectrum was already computed by Goodall--Garijo--Nešetřil
(2014).  The branch nevertheless produced a useful certified negative
result.  The package
`search/k6-defect-snark-plateau-20260725/` freezes a 36-vertex
cyclically 4-edge-connected snark flow with four \(K_6\) defects and no
immediately defect-reducing constant-value cycle switch.  Its full
\(2^{19}\)-cycle scan, independent four-pole transfer proof, structural
audit, dual-checked LRAT, and perfect-matching enumeration all pass.  This
refutes a proposed descent lemma, not the five-cycle double cover
conjecture.  A checked four-switch path reaches a six-coordinate cover,
and the human star-cycle elimination lemma then gives an explicit fifth
switch to a standard five-cycle double cover of the witness.

The exact Petersen package
`search/k6-petersen-star-barrier-20260725/` exposes a sharper obstruction:
a triangle-only flow lies in a 720-state component under
triangle-preserving switches, and every state in that component uses all
15 duads.  Thus a universal reconfiguration proof must sometimes
reintroduce defects.  The package proves the optimal barrier is two and
supplies a two-switch path to an explicit five-cycle double cover.

The obstruction now extends to the infinite Petersen-ring family in
`search/k6-petersen-ring-barrier-20260725/`.  For every \(n\ge1\), the
triangle-only component has exactly \(15\cdot48^n\) states, none omitting
a \(K_6\)-star, while a sharp defect-two path reaches an explicit standard
five-cycle double cover.  A corrected human proof accounts for both
crossing-label circuits and the previously omitted remote-vertex case;
Python and independently structured JavaScript backstop the complete
34,560-state \(R_2\) component.  A narrowly scoped, prominently
AI-disclosed research draft is in `preprint-k6-petersen-rings/`.  It is
preprint-worthy pending independent human proof and novelty review, and
does not claim a resolution of five-CDC.

A second exact theorem closes the tempting connected-kernel route.
Replacing every cotree edge of a non-Tait cubic base by a diamond produces
no connected-kernel \(\mathbb F_2^3\)-flow, while a local duad rule lifts
any ordinary five-cover through every diamond.  The 34-vertex Petersen
instance in
`search/connected-kernel-cotree-diamond-separator-20260725/` has an
explicit standard five-cover accepted by both target verifiers and a
two-checker LRAT for a 465-clause connected-kernel relaxation.  Iteration
gives an infinite separation family.  This proves that a connected
coordinate complement is a strictly stronger normal form; it does not
produce a five-CDC counterexample.  A seven-page, AI-disclosed research
draft is frozen under `preprint-connected-kernel-separator/`.  Independent
referee review found the proof correct after minor clarification and
identified Jin--Mazzuoccolo--Steffen's all-edge \(K_4\) 2-cut construction
as a close gadget precedent; the draft now claims only the narrower
connected-join separation and cotree refinement.

A different exact package now closes the unrestricted fixed-join
preparation route.  The 38-vertex graph in
`search/fixed-join-preparation-trap-20260725/` has a binary cycle whose
complement has two components and contains 125 inclusion-minimal exact
\(\mathbb F_2^2\)-flow zero sets; every one has preparation minimum two.
Projection through two inserted Petersen 2-poles gives a short human proof,
and independent Python and JavaScript checkers replay the complete finite
claims.  The graph has an explicit standard five-cover and two nontrivial
two-edge cuts.  It is therefore a counterexample only to the unrestricted
preparation lemma—not to five-CDC, and not to a preparation statement
restricted to cyclically 4-edge-connected minimum counterexamples.

The minimum-support branch has also been hardened against an overly strong
exchange claim.  The exact package
`search/minimum-switch-local-plateau-20260725/` gives a 16-vertex simple
bridgeless cubic graph, an \(\mathbb F_2^2\)-flow with two matching zero
edges, and a complete proof that this support neither packs two \(T\)-joins
nor admits a strictly decreasing matching-preserving constant-value cycle
switch.  A neutral switch followed by a decreasing switch has support
profile \(2\to2\to1\), and the final support packs.  Thus strict one-step
descent is false, while neutral nonincreasing reconfiguration and the
globally minimum-support conjecture remain open.  Independent Python and
JavaScript verifiers check the literal witness; an exact primary census
finds no such local plateau through order 14 and 64 flow signatures at
order 16.  This is not a five-CDC counterexample.

The follow-up package
`search/minimum-switch-neutral-components-n16-20260725/` builds the full
support-\(\le2\) switch graph on all six order-16 hosts with local plateaus.
Two independent implementations agree that all 33,546 ordered states reach
a size-one state without exceeding support two, and that all 384 local
plateaus have distance exactly two.  This proves neutral-then-descent on
that finite boundary; the universal neutral-reconfiguration statement
remains open.

The complete hard order-18 extension is frozen in
`search/minimum-switch-neutral-components-n18-20260725/`.  A
human-checkable bucket lemma reduces one-switch adjacency to sharing one of
\(p,q,p+q\).  Independent C++ and NumPy implementations replay all 179
graphs and 1,680,414 ordered support-\(\le2\) states.  All 7,704 strict
local plateaus on 56 graphs again have distance exactly two from size one.
This closes the finite support-size-two boundary through order 18, not the
universal or higher-support problem.

The complete hard order-20 extension is frozen in
`search/minimum-switch-neutral-components-n20-20260725/`.  The two
implementations agree field-for-field on all 1,388 non-Tait graphs and
20,161,044 ordered support-\(\le2\) states.  All 118,134 strict local
nonpacking plateaus have distance exactly two.  Exactly 21,492 states do
not reach size one; they are all the states on the unique minimum-size-two
graph, and every one already packs two \(T\)-joins.  Thus every nonpacking
state reaches size one on this finite boundary.  This is still not a
universal exchange theorem.

Order 22 is the first exact boundary where the stronger quantifier fails.
The package
`search/minimum-switch-packing-components-n22-20260725/` covers the seven
hard graphs whose globally minimum exact-zero matching size is two.  Among
1,441 distinct minimum supports, 15 supports on two graphs do not pack.
Nevertheless, all 2,808 ordered realizations of those supports are one
neutral switch from a packing state.  Thus “every minimum support packs” is
false, while the existential neutral-component formulation survives this
complete finite boundary.

The first complete minimum-size-three component census is frozen in
`search/minimum-size-three-packing-components-20260725/`.  On the
42-vertex parity-countermodel it classifies all 366 globally minimum
supports and 611,712 global-colour flow orbits.  Seventy-six supports do
not pack.  Every nonpacking orbit nevertheless reaches packing by neutral
switches, but 720 orbits have exact distance two, refuting the stronger
one-switch claim.  Independent Python and C++ implementations agree on
all counts.  All 720 distance-two orbits occur on the single support
\(\{20,30,53\}\).  An additional Gaussian-elimination checker enumerates
the 8,192 eligible even subgraphs for that support and verifies directly
that every one has an odd-marked component, while also checking a literal
two-switch path to packing.  This preserves, but does not prove, the
universal minimum-component formulation.

The unique distance-two support is now explained compositionally in
`docs/three-sum-neutral-decomposition.md` and the sealed package
`search/three-sum-neutral-decomposition-20260725/`.  Binary cycle spaces
across a cubic three-edge sum form an exact fibre product over the even
three-bit boundary words.  For a flow with exactly one zero joining edge,
the global support packs precisely when both capped pole supports pack.
The retained first switch changes both nonpacking pole flows with boundary
word \(000\); the second, with boundary word \(110\), repairs both poles
simultaneously.  An independent checker reimplements graph6 parsing,
capping, cycle-space enumeration, and all six capped packing tests.  This
explains the finite path but is not a universal exchange theorem.

A separate exact proof route is recorded in
`docs/minimum-zero-tjoin-route.md`.  On loopless cubic graphs it converts
the remaining extension condition for an exact-zero matching into packing
two edge-disjoint \(T\)-joins.  A classical packing theorem reduces every
fixed-matching failure, after the necessary componentwise \(T\)-even
condition, to the presence of an odd-\(K_{2,3}\) graft minor.  Without
that condition, a \(T\)-odd component is the first obstruction.  For a
minimum exact-zero matching \(M\), a direct flow switch further proves
that every associated \(T\)-join \(J\) obeys \(|J|\ge3|M|\).  The finite
audit package
`search/component-parity-tjoin-countermodel-20260725/` freezes the exact
ten-vertex example that exposed the missing hypothesis; it also verifies a
standard five-cover, so it is not a counterexample to the conjecture.  The
stronger package
`search/minimum-component-parity-countermodel-20260725/` freezes a
42-vertex graph with a **globally minimum** size-three exact-zero matching
whose complement has two terminal-odd components.  A human three-pole
inequality and a dual-checked LRAT prove minimality.  Complete projected
enumeration finds 365 other minimum supports with connected complements,
including an explicit standard-five-cover certificate, so this refutes
“every minimum support is parity-good” but not the surviving existential
minimum-support route.  Its three-edge cut also excludes it from the
cyclically 4-edge-connected minimum-counterexample domain.  The exact
finite cap diagnostic `search/h5-core-cap-flow-bound-20260725/`
reconstructs all 3,024 ways, modulo dihedral symmetry, to attach a
five-cycle to five of the ten marked paths in the certified \(H_5\) Tait
core.  Every capped graph has a directly checked exact-zero matching of
size at most two.  This is finite positive evidence for a boundary exchange
lemma, not a universal theorem.  The more general exact package
`search/five-pole-c5-boundary-calculus-20260725/` classifies all 6,240
ordered five-boundary words into 62 \(S_5\)-orbits and four elementary
types, proves a conditional five-cut reducibility theorem, and exhibits
disjoint abstract state sets showing that the present cap-and-switch axioms
still do not force compatibility.  The finite certificate package proves,
among other controls, that all 92,313
minimum exact-zero matchings of the reconstructed \(H_3\) extend.  The
full hard order-22 package proves that all 12,892 frozen rows have some
extending minimum support.  This once suggested a universal exchange
lemma, but that unrestricted lemma is now refuted by the certified
130-vertex graph in
`search/minimum-zero-exchange-countermodel-130v-20260727/`: it has
\(r_f=r_M=5\), no matching/four-flow packing certificate of size at most
five, and an explicit packing certificate of size six.  The later
Fano-lift audit in
`search/minimum-fano-class-nonpacking-130v-20260729/` exhibits a
nowhere-zero \(\mathbb F_2^3\)-flow with a value class of size five.
Thus \(\rho_3=5\), but every \(\rho_3\)-minimum class is nonpacking: even
the existential minimum-Fano-class selection principle is false.  This
distinguishes one-join Fano liftability from two-join packing.  The graph
itself has a checked standard five-cover, so it is a route countermodel
rather than a Five-CDC counterexample.

The conditional infinite-family package
`search/mnp-minimum-support-packing-20260729/` gives a complementary
positive theorem.  In the figure-derived reconstruction
\(\widehat H_n\) of the Mattiolo--Negrini--Pagani family, the displayed
minimum exact-zero matching of size \(n\) packs two boundary joins for
every \(n\ge2\), and lifts to a globally minimum nonzero Fano value
class.  The tile parity proof and recurrence are human-checkable and
replay through arbitrary finite prefixes; global minimality imports the
published equality \(r_f(H_n)=n\), and graph identity remains explicitly
conditional on independent verification of the figure transcription.

The exact finite census in
`scratch/minimum-projection-census-through28-20260729/` tests the separate
minimum-extendable-projection conjecture.  Every minimum projection is
cleanable on all 14,009 frozen cyclically-4 non-Tait records through
order 28 and all 12,892 frozen order-22 hard records, covering 147,539
minimum projections in total.  Population completeness is inherited
from the cited upstream canonical-generation packages; the claim about
the literal frozen files is replayed exactly.  The adjacent
`scratch/petersen-minimum-tjoin-countermodel-20260729/` explains why a
proof cannot use only one of the four affine matchings: a literal Petersen
matching has two shortest containing cycles, and both leave odd terminal
components.  These are finite evidence and an auxiliary obstruction, not
a universal proof.
The eight-page working preprint in
`preprint-minimum-fano-projection/` now includes both exact censuses, the
human exchange proof, the Petersen limitation, full reproducibility
instructions, and an explicit AI-use disclosure.

The certified large-graph stress test in
`search/minimum-projection-n130-20260729/` separates the two minimization
parameters completely.  On the retained 130-vertex graph the minimum
extendable projection size is 42, there are exactly 11,264 minimum
supports, and every one is cleanable.  Two CNF/LRAT pairs prove the
size-\(\le41\) lower bound and completeness of the list, with both C and
verified CakeML proof checks.  On the same graph the minimum nonzero Fano
value-class size is only \(\rho_3=5\), and no such size-five class packs.
Thus the graph refutes minimum-value-class selection while strongly
passing the distinct minimum-projection test.

The new coordinate-factor lemma in
`docs/flow-resistance-weak-oddness.md` proves directly that
\(\omega_{\rm w}(G)\le2r_f(G)\) for loopless cubic multigraphs.  Huck's
published weak-oddness restriction for a possible minimum five-CDC
counterexample therefore gives the sound reduction \(r_f(G)\ge4\) for a
smallest counterexample.  At exact-zero matching size four, extremality
forces all three coordinate factors to have profile \((8,8,8)\);
suppressing the eight zero endpoints, precolouring all resulting marks
alike, and lifting the eight disjoint marked bichromatic circuits gives
\(|V(G)|\ge88\).  Thus a smallest
counterexample has \(r_M\ge5\), or lies in this separated
size-four/order-at-least-88 branch.  The human proof and clean-room audit
are in `docs/kempe-transversality-and-eight-mark-girth.md` and
`docs/audit-eight-mark-girth-bound.md`.  The two-implementation finite package
`search/flow-weak-oddness-coordinate-20260725/` checks the retained
\(H_3,H_4,H_5\) coordinate profiles \((4,4,6)\), \((4,6,8)\), and
\((6,8,8)\).  The completed \(H_4\) search exhausts 4,931,430 distinct
globally minimum size-four supports; every one packs, and the blocking
CNF's UNSAT LRAT is accepted by two proof checkers.  This is a complete
finite theorem for that one frozen graph, not a universal closure.

The exact package
`search/tjoin-weighted-minima-countermodel-20260725/` closes one attempted
shortcut: a 22-vertex cyclically 4-edge-connected host satisfies the three
colour-weighted \(T\)-join lower bounds and all three quotient-forest
conditions, yet does not pack two \(T\)-joins.  Its displayed support is
not globally minimum and the graph has girth four.  The later 130-vertex
package closes the unrestricted global-minimum route itself; only variants
using additional reduced-domain hypotheses remain possible.

Two-edge sums amplify the 130-vertex separation.  The elementary
composition proof in `docs/minimum-zero-two-sum-amplification.md` gives
connected simple bridgeless cubic graphs \(G_n\) with
\[
r_f(G_n)=r_M(G_n)=5\cdot2^n,\qquad
\eta(G_n)=6\cdot2^n,
\]
where \(\eta\) is the least matching size in a matching/four-flow
five-cover certificate.  Thus \(\eta-r_M\) is unbounded.  Every member
still has an explicit standard five-cover and has cyclic two-edge cuts, so
this is a secondary obstruction theorem, not a resolution of Five-CDC.

The follow-up realizability frontier is recorded in
`docs/five-pole-realizability-frontier.md`.  A human degree-count argument
shows why internally bridgeless poles are the sound objects in the reduced
minimum-counterexample domain.  Exact finite search then finds a sharp
46-state lower bound for all 5,214 canonical five-poles through order 13,
with every extremal relation \(C_5\)-like.  The analogous four-pole census
has only nine- and ten-state relations through order 14, excluding the two
small signatures conjectured in Máčajová--Mazzuoccolo--Tabarelli within
that finite scope.  Neither finite pattern is promoted to a universal
theorem or a publication claim.

The surviving size-four branch now has an exact factor-quotient
formulation.  Contracting the eight marked bichromatic factor circuits
gives a connected Eulerian quotient, but quotient \(T\)-joins must satisfy
additional cyclic-port routing equations to lift.  A small
human-checkable quotient refutes automatic lifting, while the actual
minimum-counterexample hypotheses reduce an unavoidable terminal-gap
failure to a cyclic four-cut with two zero edges or a cyclic six-cut with
all four.  See `docs/eulerian-factor-quotient-tjoin-reduction.md`,
`docs/two-tjoin-cycle-lift-obstruction.md`, and
`docs/size-four-terminal-gap-cut-reduction.md`.

As a finite equality control, all 33 cubic vertex-transitive order-80
graphs in the Potočnik--Spiga--Verret census are excluded from the
stable-eight core: 32 fail exact marked-girth incidence bounds, and the
sole girth-ten graph has 426,256 normalized Tait colourings but no
universally separated eight-edge matching.  Exact scope and
reproduction data are in `docs/order80-vertex-transitive-control.md`.
This is not an enumeration of arbitrary order-80 cubic graphs.

The ambient orders \(88,90,92,94,96,98,100\) are now excluded in the
extremal exact-zero size-four branch by solver-free girth/Kempe
arguments, complete finite incidence censuses, and a certified global
rotation closure at order 100.  At equality, all
marked bichromatic factor circuits are core \(C_{10}\)'s lifting to
\(C_{11}\)'s.  Ambient girth forces their bipartite incidence multigraph
to be simple; switching one factor circuit would then create a
bichromatic \(C_{50}\) carrying four marks, contrary to universal
separation.  At positive surplus, a three-matching cycle-rank argument,
the general inequality \(2p+u\le d+2\), sharp marked-circuit overlap
bounds, and simultaneous spacing constraints remove the subsequent
orders.

At order \(98\), all 335 canonical incidence profile pairs are
infeasible.  The solver-free backtracker, an independent Z3 formulation,
a prune-free 9,193,235-node replay, and an independently generated HiGHS
formulation agree.  The new human local ingredient is a weighted
triangular-prism/\(K_{3,3}\) diagonal-overlap lemma.  This first gave the
rigorously scoped branch bound
\[
                         |V(G)|\ge100.
\]
See
`docs/equality88-kempe-girth-contradiction.md`,
`docs/equality88-overlap-audit.md`,
`docs/order94-kempe-surplus-bound.md`, and
`docs/order98-complete-incidence-census.md`.

At order \(100\), a human argument excludes unmarked factor circuits.
The exact pairwise incidence relaxation leaves 155 canonical profiles,
weighted row/column stars leave three, and three profile-level CNFs
choose every remaining incidence matrix, cyclic position, bijection, and
twist.  Independently checked LRATs prove all three UNSAT already in the
deleted-matching core.  A producer-free semantic checker regenerates the
base encodings and verifies all 996,904 learned clauses as forced short
circuits.  The updated branch-specific bound is therefore
\[
                         |V(G)|\ge102.
\]
See `docs/order100-unmarked-exclusion-and-row-star-frontier.md`.  None of
these branch-specific bounds resolves five-CDC.

The cyclic six-cut reduction has also been sharpened to a rooted
four-mark obligation.  Cycle/cut orthogonality always supplies an
all-mark binary cycle avoiding the cap, but componentwise even mark
parity remains open.  An exact order-28 countermodel shows why universal
separation alone is insufficient and pinpoints the missing marked-cut
hypothesis.  Under that marked-cut hypothesis, a new bridge-elimination
lemma proves that every surviving rooted failure has a 2-connected
subcubic deleted-root graph in which all three complementary mark-pair
circuit families are cross-intersecting.  See
`docs/rooted-four-mark-cap-avoidance.md` and
`docs/rooted-four-mark-bridgeless-reduction.md`.

The cyclic four-cut exceptional pair now has an exact rooted-packing
interpretation.  Projection-coherent five-coordinate lifts are precisely
ordered pairs of edge-disjoint terminal joins, and the two exceptional
boundary polarities say respectively that the distinguished nonzero cap
must be used or avoided.  A zero-free shore always has the avoiding
state, so only internal-zero distributions \((1,1)\) and \((2,0)\)
survive.  Exact ten-state composition also shows that a two-plus-two
decomposition cannot first create the four-type exception.  The full
exceptional-signature conjecture remains open.  See
`docs/four-pole-exception-rooted-packing-algebra.md`.

The current sharp Jaeger frontier is the symmetric seven-plane exchange
potential.  A complete exact census of 529,150,122 star-fibre states on all
simple 3-edge-connected cubic graphs through order 14 finds no trapped
positive-level component.  A parity-element reformulation identifies every
odd kernel as a fundamental circuit and exposes a cographic-base selection
language.  Its natural graphic-closure strengthening is now false even for
a vertex-star fibre: a dual-certified 16-vertex example has zero
closure-good packings among 5,723,136, but 40,464 exact parity-good
packings.  A human triangle-contraction theorem extends that auxiliary
failure to an infinite rooted family.  The exact parity selection lemma and
the universal symmetric-descent theorem remain open.  The seven-plane
defect now has a self-contained exact exchange law, but immediate descent
is false: a positive 16-vertex state has no descending neighbour, while a
kernel-inert neutral exchange exposes a descent on the following move.
The natural fixed-kernel exposure repair is also false: a second exact
state has no kernel-inert neighbour and first needs an active same-level
exchange.
The triangle-style fixed-state lifting rule also fails for a square:
an exact planar order-eight state has 72 legal local lifts but none good in
any coordinate. An alternate state for the same fibre does lift, and a
complete 672-instance order-eight census has no whole-fibre failure, so the
existential square reduction remains open.
Nonroot triangle expansion gives an exact Cartesian product of fibre
exchange graphs, and simultaneous expansions give one \(S_3\) Cayley
factor per triangle. An explicit six-lift table shows that the defect score
is not contraction-invariant.  Thirteen such expanded fibres, containing
17,297,280 states, pass exact descent checks.  The remaining sharp
obligation is the full same-level-component boundary theorem;
consequently the standard Five-Cycle Double Cover Conjecture is not
resolved.  See
`scratch/jaeger-fano-reciprocal-exchange-law.md`,
`scratch/jaeger-fano-min-immediate-descent-countermodel.md`, and
`scratch/jaeger-triangle-expansion-descent-structure.md`.

## Exact direct-search reductions and sharpened local frontiers

Audit date: **2026-07-28**.

Two direct counterexample families are now eliminated by human proofs.
A standard FiveCDC pulls back through every finite graph covering, with
loops handled by the two-incidence convention.  Therefore connected
2-lifts of positive graphs cannot be counterexamples.  Separately, deleting
two independent edges of a positive cubic graph and inserting the
Petersen four-pole obtained by deleting adjacent vertices preserves
FiveCDC for every port bijection.  A displayed 13-row table covers the
three \(S_5\)-orbits of boundary-label pairs; an independent checker
exhausts all 550 labelled boundary assignments.  These are sound pruning
reductions, not a proof of FiveCDC.  See
`scratch/fivecdc-cover-pullback-reduction-20260728.md` and
`scratch/fivecdc-petersen-four-pole-extension-theorem-20260728.md`.

The direct exact-two/XOR solver found checked standard FiveCDC witnesses on
all 45,924 tested graphs at orders 40, 48, 56, 64, 80, and 160.  The lift
and Petersen-substitution theorems explain five of the six layers once the
order-40 bases are positive.  No target UNSAT instance occurred, so no
FiveCDC UNSAT certificate exists in this portfolio.

For the square route, a fixed outside five-cover extends across the square
exactly when the two deleted edge labels are equal or disjoint.  Complete
whole-fibre censuses through order 16 check 8,370,612 labelled
root/edge-pair instances with zero failures.  The 572,880 order-14 and
7,737,408 order-16 witnesses are replayed by separately written
standard-library checkers.  All three order-18 snarks add 12,474 checked
instances with zero failures.  For the exchange
route, a 36-vertex state proves that even the sorted seven-defect profile
need not decrease in one legal exchange: its 63 legal neighbours split as
0 lower, 13 equal, and 50 higher.  A checked two-exchange same-level escape
still reaches defect zero.  A 40-vertex state has exact plateau escape
distance four: complete enumeration of its 958-state radius-three ball
finds no earlier descending boundary.  Two adjacent equal-profile states
on that graph have total-defect Laplacians \(+10\) and \(-14\), refuting
profile-only averaging and universal sub/superharmonicity of total defect.
On the square side, a human
three-edge-cut lemma and a triangular-prism witness show that no choice of
downstairs five-cover can always make the two deleted labels equal or
disjoint, even when a good tree-local lift exists.  Thus the whole-fibre
square implication and the full unbounded plateau-component theorem both
remain open.

A genuinely different non-covering reduction is now proved in two forms.
Deleting adjacent vertices from the cube gives a six-vertex, seven-edge
four-pole through which every one of the 640 xor-zero ordered boundary
words extends.  Ten displayed \(S_5\)-orbit rows prove the claim.  This
pole has minimum possible order among connected simple terminal-distinct
cubic full-boundary four-poles: the only order-four core is \(C_4\), the
\(K_{3,3}\)-minus-adjacent-vertices pole, and its exact boundary relation
misses the 60-word orbit represented by `02 02 03 03`.  See
`scratch/fivecdc-minimum-full-boundary-cube-four-pole-20260728.md`.

Deleting two adjacent Heawood vertices similarly gives a 12-vertex,
four-port full-boundary pole whose proper core has girth six.  Independent
standard-library checkers verify both ten-row tables, every internal
parity, and exact coverage of all 640 words.  Consequently either pole may
replace two independent edges of any FiveCDC-positive cubic graph using
any of the \(4!\) port bijections while preserving standard FiveCDC and
bridgelessness.  These are sound minimal-counterexample pruning rules, not
a universal reduction: neither pole is proved unavoidable.  See
`scratch/fivecdc-heawood-full-four-pole-theorem-20260728.md`.
The Petersen, cube, and Heawood reductions, together with the sharp
\(K_{3,3}\) boundary obstruction, are assembled in the explicitly
AI-disclosed working preprint
`preprint-fivecdc-four-pole-reductions/`.
