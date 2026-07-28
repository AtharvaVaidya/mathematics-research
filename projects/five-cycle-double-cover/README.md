# Five-cycle double cover laboratory

This repository is a machine-assisted research package for the five-cycle
double cover conjecture (5-CDC).  Its acceptance condition is:

> Given a finite undirected graph \(G=(V,E)\), find five indexed even
> (Eulerian) edge-subsets \(C_0,\ldots,C_4\) such that every edge belongs to
> exactly two of them.

The project does **not** currently claim a resolution.  Every result is
classified using the status vocabulary in the lab protocol.  In particular,
finite searches are not evidence of the universal statement.

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

The latest surface-Kempe audit closes several tempting local proof routes.
The human corner-pairing argument proves that factor switches with zero or
two remote twists are neutral, but explicit connected 2-lifts refute the
inferred boundary-size bound, universal local neutrality, and even the
weaker local nonnegative-delta claim.  A separate 56-vertex package
exhausts a terminal equal-\(\chi\) plateau with 55,652 states modulo
global \(S_5\): 1,041 states have disconnected neutral-component
hypergraphs, yet the whole plateau is root-universal.  See
`scratch/d5-local-neutral-corner-pairing-frontier.md` and
`scratch/d5-lift56-terminal-plateau-neutral-connectivity-no-go.md`.
These are exact route counterexamples and a positive finite plateau result,
not a proof or disproof of FiveCDC.

The sharper terminal-\(\chi\) chain census now checks every one of the
642,167 fixed-distance subplateaus arising from all 480 biconnected simple
cubic graphs of order 14.  Every bad subplateau has a neutral exit to lower
factor-component-chain distance; an independent order-12 implementation
agrees on 33,610 subplateaus.  Two standalone terminal witnesses also show
why this finite pattern has not yet become a proof: a neutral
shared-coordinate self-reentry switch can raise the distance \(2\to3\),
and a second terminal state has no immediate neutral descent at all even
though a neutral \(2\to2\to1\) route exists.  See
`scratch/d5-terminal-chi-chain-lexicographic-target.md` and
`scratch/d5-terminal-shared-pair-self-reentry-no-go.md`.  The universal
closed-subplateau exit lemma remains open.

The newest refinement proves a human-checkable first-foreign factor-splice
identity and measures the intervening foreign factor-component blocks by a
secondary potential \(b^*\).  Two separately implemented complete censuses
through order 14 find no closed terminal fixed-\((d,b^*)\) subplateau.  In
the primary lower-index-root accounting there are 646,399 such subplateaus;
in the independent directed-root accounting there are 1,293,664.  Both
have zero failures, and the primary full transcripts are protected by an
independent verifier and SHA-256 ledger.  A seven-state order-12 terminal
plateau refutes the stronger claim that the prescribed root-component
switch must immediately rescue the roots.  A separate order-14 witness
shows that even switching the root component or first blocker can fail,
while one neutral third-pair switch succeeds.  See
`scratch/d5-first-foreign-splice-lemma.md`,
`scratch/d5-terminal-foreign-block-potential-through-order14.md`, and
`scratch/d5-cyclic-block-one-step-no-go-order14.md`.  A clean
fresh-coordinate multi-splice lemma explains that third-pair rescue, but
an all-five-coordinate order-12 state refutes universal availability of a
fresh coordinate.  These results isolate the neutral closed-cage exclusion
still needed for a proof; they do not resolve FiveCDC.

An independent Fourier calculation also gives an exact formula for the
number of \(D_5\)-flows as a signed sum over contracted edge sets, involving
the binary ranks of their quotient Laplacians.  Direct enumeration agrees
on \(K_4\), \(K_{3,3}\), the cube, the Petersen graph, and loop/parallel-edge
controls.  The tempting mod-3 nonvanishing corollary fails already on
\(K_4\), whose signed-rank sum is \(18\).  The exact identity and its
standard-library checker are in
`scratch/d5-fourier-laplacian-count.md` and
`scratch/audit_d5_fourier_laplacian_count.py`.  The complete bridgeless
cubic census through order 12 finds no vanishing leading coefficient, but
\(K_{3,3}\) and the cube already refute two naive 2-adic leading-term
predictions.  This is a structural counting identity, bounded evidence,
and several failed modular proof routes, not a resolution.

The reduced Fano-flow branch has an exact affine pair-circuit theorem:
two value-\(s\) edges admit the required pure-deletion circuit precisely
when their endpoint pairs in the affine-complement circuit decomposition
agree.  The surviving APX obligation is to prove that some such affine
pair is also a packing deletion pair.  The frozen strict order-24 near-state
has APX score exactly one; its independent checker enumerates all 4,681
simple circuits, 1,371 legal switches, and 180 still-bad neighbours, every
one retaining positive APX score.  Global collision identities and explicit
four-defect certificates are proved, but aggregate counts and defect-weight
profiles are too weak to force the required correlation.  See
`scratch/fano-reduced-kp-two-bond-frontier.md` and
`scratch/fano-apx-score1-order24.json`.  This is a checked near-state and a
conditional reduction, not a FiveCDC proof.

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
\(r_f=r_M=5\), no matching/four-flow extension of size at most five, and
an explicit extension of size six.  The graph itself has a checked
standard five-cover, so it is a route countermodel rather than a Five-CDC
counterexample.

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
