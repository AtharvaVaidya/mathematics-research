# Proof-obligation ledger

Open obligations:

1. **Discharged (literature level):** verify the current (2026-07-24)
   primary-literature status.
2. **Discharged (semantic level):** freeze the graph conventions used by the
   standard conjecture.
3. **Discharged (semantic level):** prove that “at most five” is faithfully
   represented by five indexed coordinates padded with empty even subgraphs.
4. **Discharged for the fixed-graph semantics:** prove the SAT/XOR
   equivalence, including loops and parallel edges.  This now has a prose
   proof, two implementations, a Lean witness-subtype equivalence, and an
   independent semantic audit.  The universal conjecture is not formalized.
5. **Discharged at implementation level:** implement and freeze two
   independent exact verifiers.  Verifier A 1.0.0 is Python and uses chained
   XOR gates in ordinary CNF; Verifier B 0.1.0 is Go-standard-library-only and
   uses auxiliary-free truth-table CNF.  Their SAT models and graph-premise
   reports have been cross-checked on simple, looped, parallel, disconnected,
   and bridged controls.
6. **Discharged for pipeline controls; counterexample gate still open:**
   implement certificate-producing CNF and independent proof checking.
   CaDiCaL LRAT production, `lrat-check`, and the CakeML-generated `cake_lpr`
   checker all agree on independently generated negative-control proofs.
   There is no bridgeless UNSAT candidate on which to exercise the
   counterexample acceptance gate.
7. **Discharged for every restriction currently used:** the proof-agent
   independently verified the one-way expansion to a simple bridgeless cubic
   counterexample, the two/three-cut gluing lemmas, simplicity, and
   four-cycle reducibility.  Girth at least 10 and oddness at least 6 remain
   explicitly imported from Huck.  No restriction to cyclic connectivity
   five or higher is used.
8. **Discharged semantically; no orientable computation claimed:** keep the
   orientable variant separate.  `docs/orientable-encoding.md` uses signed
   direction variables and integer flow conservation; no primary-search
   artifact silently includes those constraints.
9. **Discharged for all recorded complete runs through order 22:**
   a clean-room Python/C++ audit scanned all 7,319,447 order-22 canonical
   records, exactly matched all 12,892 hard identities and structural rows,
   freshly regenerated every lower even order, and checked all 29 strict
   standard witnesses against direct semantics, both CNFs, and all 435
   symmetry units.  Together with the audited minimum-order reductions this
   proves that every bridgeless cubic multigraph whose components have at
   most 22 vertices has a standard 5-CDC.  The conclusion does not cover
   arbitrary noncubic graphs of that order, the orientable variant, or the
   universal conjecture.  Any enlarged census creates a new obligation.
10. **Discharged within the declared scope:** formalize the fixed-graph
    encoding, padding, and \(D_5\)-flow equivalences.  The Lean build has no
    `sorry`, `admit`, `unsafe`, or custom axioms and passed a separate
    semantic audit.  There is no final witness or universal theorem to
    formalize.
11. **Pure merge and one-circuit repair refuted; broader construction choice
    open:** fixed recombination, component-wise recoloring, and the stronger
    rule “arbitrarily relabel the eight coordinates as
    \(\mathbb F_2^3\), then choose any quotient line and solve the binary
    lift” are ruled out on supplied covers.  Allowing another compatible
    cover for the same fixed flow rescues the old 112-vertex
    coordinate-tree example, so that obstruction cannot be promoted to the
    fixed-flow level.  A different 12-vertex fixed flow does give an exact
    fixed-flow obstruction: its potential system is unique modulo
    translation and forces a coordinate \(K_6\), so no compatible cover
    purely merges into five symmetric-difference classes.  The
    port-deleted block remains rigid.  Three copies in a 46-vertex
    composition prove that no switch on one connected circuit universally
    repairs pure mergeability.  The proof and independent checker are in
    `search/fano-pure-merge-one-switch-countermodel-46v-20260726/`.
    Different initial-flow selection, non-pure compression, multiple
    switches, or a reduced theorem confined to cyclically
    4-edge-connected cubic graphs remain open.
12. The Petersen local states, cut tables, four-cycle no-good, affine-plane
    no-go, and CNF templates have exact exhaustive local checks.  Adding the
    histogram identities as redundant global constraints and measuring
    their solver effect remains open.
13. **Partially discharged; universal step open:** the exact quotient-lift
    theorem reduces 5-CDC to choosing a nowhere-zero
    \(\mathbb F_2^3\)-flow and a Fano line with no four-value odd boundary
    component.  A fixed flow can fail all lines.  A connected line-valued
    join is equivalent both to the published connected-congruent-join
    condition and to a 5-CDC with some connected coordinate complement.
    This is an exact strengthening of 5-CDC, not merely an unrelated
    sufficient property.  All 44,327 connected simple bridgeless cubic
    classes through order 18, all 1,082 records in the first hard-snark
    portfolio, and all 7,984 retained strong-snark records through order 40
    satisfy this stronger condition.  Exact switch laws and the new
    preparation-code theorem reduce the existential fixed-join step to
    finding a common-zero matching \(T\subseteq H\) for which
    \(\mu_G(T)<\kappa(E-H)\).  The primary canonical census has zero traps
    through order 18, and an independent implementation reproduces zero
    traps through order 16.  Moreover, \(\mu_G(T)=1\) is exactly a connected
    odd-factor problem in \(G-T\).  Cyclic 4-edge-connectivity does not make
    every relevant minimal \(T\) connected-odd-factor positive: complete
    order-34, order-36, and order-38 audits found 7, 29, and 597 exceptions
    with \(\mu=2,3\), and the exact 40-vertex \(R_2\) factorization found
    9,516 exceptions reaching \(\mu=4\). The correct high-specific
    condition still has zero traps across 328,184,467 realizable
    disconnected joins in those four audits. Relevant minimal zero
    sets on all 7,654 retained order-40 hosts have now also been screened
    directly: 6,053,028 supports split into 6,009,319 with \(\mu=1\) and
    43,709 without, with zero necessary trap candidates.  Candidate SAT
    plus a two-component complement would certify a trap, but no candidate
    occurred.  The independent replay now covers all 60 batches and all
    7,654 hosts, with 16,051,601,408 cycles classified and all 7,654
    support-completeness proofs and candidate CNFs checked.  Its exact
    totals match the primary run; the ledger is
    `fb9ebf90f57453efff948dd6d9cbc05c76bb086cdedc42e2396adaf94761c457`.
    This finite exclusion does not contradict the later 38-vertex
    preparation trap and does not discharge five-CDC.
    Separately, the exact matching/four-flow theorem now characterizes the
    target itself on finite loopless cubic multigraphs: a matching \(M\)
    must be the exact zero set of an \(\mathbb F_2^2\)-flow and the
    intersection of two binary cycles.  Both directions and the
    five-variable-per-edge CNF/XOR encoding have passed a clean-room audit.
    The intersection condition is equivalent to an odd factor avoiding
    \(M\) with an even number of \(M\)-endpoints in every component.  This
    is weaker than \(\mu_G(M)=1\).  Exact order-34 enumeration finds two of
    seven \(\mu=2\) supports satisfying the weaker condition and five
    failing it; every affected graph has another \(\mu=1\) support.  A
    universal existence theorem for some component-parity-good exact
    matching, or a graph for which all such matchings fail, remains open.
    Equivalently, the new Fano-flow branch asks for a one-switch exchange
    theorem.  In a nowhere-zero \(\mathbb F_2^3\)-flow, each of the seven
    value classes is an exact-zero matching after quotienting by its span.
    The stronger assertion that every flow already exposes a packing class
    has an independently checked order-ten countermodel.  The surviving
    lemma asserts that if all seven classes fail, adding one nonzero value
    on a binary cycle avoiding its own class makes some class pack.  Exact
    \(\mathrm{GL}(3,2)\)-orbit enumeration passes for all cubic graphs
    through order 14 and all frozen hard graphs through order 20.  A
    separate C++ enumerator matches the full order-14 Python totals and
    finds all 49,752,091 bad flow orbits on the 1,388 hard order-20 graphs
    repairable on one connected circuit.  Equivalently, the good flows
    dominate the tested \(\mathbb F_2^3\)-flow reconfiguration graphs.
    What remains is a
    universal proof that the seven nonpacking classes cannot be closed
    under all three-pair cycle exchanges.
    The related ten-flow zero-partition CNF is only a necessary relaxation;
    it is SAT on \(H_2\), so no rejection is obtained there.
    The still stronger fixed-high premise is refuted with certificates:
    Petersen's spanning two-factor of two 5-cycles is not a coordinate of
    any standard five-cover.  Two exact restricted CNFs and independently
    checked LRATs agree with a complete 4,096-flow enumeration.  The graph
    itself has an unrestricted five-cover, so the high coordinate must be
    allowed to change.
    The singleton sub-obligation is discharged universally on the strict
    domain: Tutte's peripheral-cycle theorem gives
    \(\mu_G(\{e\})=1\) for every edge of every finite simple 3-connected
    cubic graph.  An independent audit checked all 29,037 edges on the 985
    premise-satisfying hard rows through order 20 and reconstructed the
    excluded order-18 control.  Thus a remaining higher-\(\mu\) obstruction
    has support size at least two.  The exact-pair branch has now been
    reduced to a marked Tait-colourable cubic core: in girth at least five,
    four once-subdivided marks or the unique two-once/one-twice
    single-cross form give explicit connected component-cut parity tests.
    A clean-room audit checked all 1,439 exact pairs through order 10,
    including 19,624 fixed-\(Q\) orientation/parity comparisons and the
    three \(K_4\) boundary cases, with zero theorem failures.  What remains
    open is the universal existence of the required connected core
    subgraph under the minimum-counterexample hypotheses.  A targeted
    order-24 marked-core search found 291 complete connected-factor failures
    across the independent and one-cross geometries, but all 858 external
    reconstructions were explicitly Tait-colourable and had girth three or
    four.  Complete Flower-snark controls checked 2,475 exact minimal pairs
    on \(J_5,J_7,J_9\), all with \(\mu=1\).  An independent checker replayed
    every affine odd-factor space and reconstruction.  This finite pattern
    motivates, but does not prove, a pair-specific reducibility theorem.
    The unqualified theorem is explicitly refuted: opposite edges of
    \(K_4\), and an exact pair in the girth-five cyclically-5 dodecahedral
    graph, both have \(\mu=2\).  Both graphs are Tait-colourable, so these
    pairs are not inclusion-minimal.  The corrected non-Tait/minimal-pair
    statement passes a complete screen of 13,547,580 pairs on all 7,654
    retained order-40 strong snarks; the 517 pairs without a
    connected-complement cycle are all inexact.  Catlin contraction proves
    only aggregate quotient parity: connectivity can fail when contracted
    vertices are split back into marked ports.  That
    transition-connectivity gap remains open.
    Independently, the quotient \(E_5/K_a\) for each pair label proves a
    sound target obstruction: on a graph without a nowhere-zero
    \(\mathbb F_2^2\)-flow, a 5-CDC forces ten pairwise edge-disjoint
    inclusion-minimal exact zero supports.  Thus the minimal-support
    hypergraph must have matching number at least ten.  The theorem and its
    Petersen/\(R_2\)/\(R_4\) checks are discharged; searching for a
    bridgeless graph with matching number at most nine, or proving the
    packing universally without assuming a five-cover, remains open.  Its
    scalar resistance corollary is weaker than a known perfect-matching
    bound and is not a research claim.
    The reconstructed high-flow-resistance \(H_2,H_3,H_4,H_5\) are
    discharged as candidates.  Explicit flows and independently checked
    LRATs prove resistances two through five respectively, while all four
    complete standard formulas are SAT with two-verifier acceptance.
    Certificate-producing cut formulas prove cyclic 5-edge-connectivity for
    \(H_4\) and \(H_5\), and both matching/four-flow instances reverse-lift
    to independent five-covers.  Root replays accepted all retained
    resistance and cut LRATs with `lrat-check` and CakeML `cake_lpr`; the
    \(H_5\) clean-room audit reproduced its 202-vertex result byte-for-byte.
    A later stable-tile certificate discharges the uniform positive branch
    for the frozen reconstruction: after a global relabeling of
    \(\widehat H_2\), the open 40-vertex \(J\)-tile preserves boundary state
    \((01,01,02,23,03)\), so a checked XOR gluing lemma proves standard
    five-covers for every \(\widehat H_n\), \(n\ge2\).  The package ledger is
    `e09cee11f74b19e4a08f18c94534207e44f601a29f059a15fb614154900cbfac`.
    This closes that reconstructed family as a counterexample source but
    does not discharge any universal proof obligation.  Independently, the
    author-defined MNP coloring implies oddness exactly two, so
    Huck--Kochol already gives family-wide existence there; the stable
    certificate, not existence, is the only provisional novelty.
    At the small boundary, all 212 hard bases through order 18 have a
    complete independent reconstruction: their 3,336 relevant minimal
    supports have \(\mu\)-profile \(1:3272,\ 2:63,\ 3:1\), and all 29,312
    highs containing a non-\(\mu=1\) support also contain a \(\mu=1\)
    support.  This independently confirmed zero-candidate result remains a
    bounded census, not a proof of the universal obligation.
    The complete canonical order-20 boundary is now independently replayed:
    all 510,489 connected simple cubic rows were decoded and classified,
    all 5,821,693,952 ordered hard-row cycle pairs were traversed, and the
    resulting 21,686 minimal supports have
    \(\mu\)-profile \(1:21,219,\ 2:455,\ 3:8\), with four irrelevant.
    Every one of the 425,024 affected highs is dominated, so candidates and
    traps are zero.  The finite margin is at least three.  Exactly six hard
    rows are cyclically 4-edge-connected, and all 170 supports on that
    subcorpus have \(\mu=1\).  These statements are exact only at order 20.
    On the retained order-34/36/38 sources, an independent clean-room
    Walsh--Hadamard replay has reconstructed all 131,596,288 affected highs
    on 134 graphs.  The respective domination minima are 21, 22, and 20,
    with zero necessary candidates and exact agreement with every frozen
    histogram.  The primary reports' temporary helper binary is
    unretained, but portable source rebuilds match after removing only its
    path/hash provenance; the independent reconstruction does not use that
    binary.
    Relevant minimal zero sets now also have exact deletion/suppression,
    relevance-parity, and odd-factor-attachment
    formulations.  On \(R_2\), every cycle containing any relevant support
    contains one with \(\mu=1\); this now has both an independent full-cycle
    audit and a compact four-block proof using seven local Petersen
    odd-factor witnesses.  Generalizing that domination beyond the
    \(R_2\) decomposition remains open; the exact reusable hypotheses are
    isolated in `docs/four-block-domination-template.md`.  Prove the
    high-specific preparation condition
    universally, produce a preparation trap, or separate the connected-
    complement strengthening from ordinary 5-CDC. A separate exact census
    found no distinction between unrooted and singleton-root preparation
    among 44,327 connected simple bridgeless cubic bases through order 18;
    an independent checker revalidated all 212 hard cycle-code profiles and
    5,216,238 root obligations. This does not prove the rooted hypothesis
    redundant. Moreover, an exact census of 71,313 edge pairs and
    67,244,094 high/pair obligations finds nine failed pairs on two
    order-18 graphs. A complete witness shows that passing every singleton
    root does not imply the two-root property: roots
    \(\{9,19\}\) fail on one high although all 27,216 singleton
    obligations pass. Therefore arbitrary multi-root premises must remain
    explicit in substitution arguments. The exact adaptive one-step theorem
    discharges the corresponding local transfer question: a surviving next
    edge pulls back to roots \(\{s,e\}\), while a terminal or internal edge
    of the newest pole pulls back only to \(\{s\}\). A producer-free audit
    enumerates every cut state, fragment, and internal-root obligation and
    replays the order-28 surviving-root boundary. This permits fixed nested
    continuation inside the newest pole, not unrestricted branching.
    Induction gives an infinite family with 16 separately valid continuation
    roots at every depth. A second independent audit checks all 16
    constructions and the order/size recurrence, then proves exact zero
    coverage on the 7,984 retained strong-snark rows by comparing all
    14,067,888 edge pairs through cycle-space signatures. No two-edge cut
    occurs; because every cut Petersen pole implies such a cut, none of
    those rows has a first contraction. This is a proof-route theorem and
    finite coverage result, not five-CDC UNSAT. None of the universal
    alternatives has yet been done.
14. **Discharged for the retained package:** an independently written blind
    auditor reconstructed raw graph semantics, both CNF families, canonical
    counts, models, manifests, local obstruction counts, and all retained
    LRAT controls without importing either verifier or search implementation.
    Its final result has zero failures.  This is a package audit, not a
    resolution gate.
15. **Open resolution gate:** no finite bridgeless graph has produced a
    target-standard UNSAT formula, and no universal existence proof has been
    obtained.  Therefore neither the disproof nor proof acceptance package
    can be completed.
16. **Discharged for one restricted-domain finite case:** the explicit
    order-30,450 graph is simple, cubic, connected, bridgeless, has girth
    exactly 10, and has oddness at least 8.  The resistance lower certificate,
    exact implemented-\(F_{10}\) properness certificate, and compositional
    v4 five-cover have independent raw-artifact audits.  Proposition 11
    giving resistance monotonicity under proper superposition remains an
    imported literature theorem rather than a Lean theorem.  This positive
    case enters but does not exhaust the minimum-counterexample domain.
17. **Exact reduction established; exchange lemma open:** for any exact-zero
    matching \(M\), the condition \(A\cap B=M\) is exactly the packing of
    two edge-disjoint \(T\)-joins in
    \((G-M,T=\partial M)\).  The restricted flow proves bridgelessness,
    but a blind audit corrected the claim that the minimum \(T\)-cut is
    automatically two.  A \(T\)-odd component gives cut minimum zero and
    no \(T\)-join.  If all components are \(T\)-even, the minimum is two
    and the imported Codato--Conforti--Serafini theorem makes an
    odd-\(K_{2,3}\) graft minor necessary for remaining failure of this
    fixed \(M\).  A universal proof would follow by showing that a
    genuinely nonpacking minimum exact-zero matching can be exchanged for
    a smaller one.  A proved partial switch says that every \(T\)-join
    \(J\) meets each of the three nonzero flow-color classes in at least
    \(|M|\) edges, hence \(|J|\ge3|M|\); this does not yet imply packing.
    No complete exchange theorem is proved.  The finite package
    does prove that all 20,749 minimum supports in the complete order-20
    hard corpus and all 92,313 minimum supports of reconstructed \(H_3\)
    extend; the latter enumeration is complete by a two-checker LRAT.
    Existentially, every one of the 12,892 frozen hard order-22 rows has an
    extending minimum support; seven size-two lower bounds have LRATs
    accepted by both proof checkers.
    These finite discharges do not close the universal obligation.
18. **Blind-audit correction discharged exactly:** the frozen graph6
    instance `Is?AXW[[?` is a simple cubic connected bridgeless graph with
    an exact-zero matching whose complement has two \(T\)-odd components.
    It has no \(T\)-join and cut minimum zero even though all three quotient
    graphs are forests.  A direct Tait colouring and standard five-cover
    show that it is not a graph-level obstruction.  This package
    independently checks the corrected boundary of obligation 17.
19. **Component quotient lemma discharged:** after contracting the
    components of \(G-M\), the matching \(M\) forms a bridgeless quotient
    multigraph and each quotient degree equals the terminal count of the
    corresponding component.  Hence every parity-bad component has degree
    at least three, parity failure is impossible for \(|M|\le2\), and the
    only connected parity-bad quotient at \(|M|=3\) is the three-edge
    dipole.  This removes the component branch for all size-one and
    size-two minima but does not remove the odd-\(K_{2,3}\) graft-minor
    branch.
20. **Small-cut interaction discharged:** in the cyclically
    \(4\)-edge-connected minimum-counterexample domain, a \(T\)-odd
    component defines a cyclic cut of odd size.  Size three is excluded,
    so every such component has at least five terminals.  Consequently
    component parity is automatic for every exact-zero matching of size at
    most four on a reduced minimum counterexample.  Matching size five is
    the first surviving component-parity case; at that size failure forces
    the five-edge dipole quotient, with exactly two complement components.
21. **Single-switch \(K_6\) descent refuted exactly; reconfiguration open:**
    the quotient law for a fixed switch value reduces defect change to a
    minimum \(T\)-join calculation, but local optimality does not force two
    defects.  A frozen 36-vertex cyclically 4-edge-connected snark flow has
    four defects and minimum change zero for every one of the 15 values
    over its full \(2^{19}\)-element cycle space.  Structural checks, an
    independent four-pole transfer proof, dual-checked edge-colouring LRAT,
    and independent perfect-matching enumeration all pass.  Hence a
    universal proof must establish descent through a sequence of neutral
    switches, use a sound stronger structural restriction, or leave this
    route.  The frozen witness itself has a checked four-switch path
    \(4\to4\to2\to2\to0\), so it is not an absorbing component.  Its
    endpoint omits no \(K_6\)-star and initially yields only a
    six-coordinate double cover; a fifth checked star-cycle switch produces
    a standard five-cycle double cover of this finite witness.
22. **Defect-monotone star reconfiguration refuted exactly; nonmonotone
    theorem open:** the Petersen graph has a triangle-only flow whose
    complete triangle-preserving switch component is a free
    \(S_6\)-orbit of size 720.  Every state uses all 15 duads, so no state
    omits a \(K_6\)-star.  Any route to a star-omitting flow must therefore
    reintroduce defects.  Defect parity gives a lower bound of two, and a
    checked two-switch path \(0\to2\to0\) attains it and yields an explicit
    five-cover.  A universal \(K_6\) proof now requires a controlled
    nonmonotone reconfiguration theorem or a different potential; neither
    is proved.
23. **Triangle-only escape refuted by an infinite family; controlled
    barrier theorem open:** the Petersen-ring family \(R_n\) has a
    completely classified triangle-only component of
    \(15\cdot48^n\) states, all using every duad.  Thus the need to
    reintroduce defects is not confined to one graph.  A blockwise path
    proves the optimum defect barrier is still two for this family.
    What remains open is a universal theorem bounding or controlling the
    defect barrier for arbitrary bridgeless cubic graphs, or another
    potential forcing a star-omitting state.
24. **Connected-kernel universal normal form refuted exactly:** for any
    non-Tait cubic base \(B\), replacing every cotree edge by a diamond
    produces a graph with no connected-kernel
    \(\mathbb F_2^3\)-flow.  Conservation and kernel connectivity force the
    effective cotree values into the selected Fano line; the quotient
    outside-line support is then an even subset of a spanning tree and is
    empty, which would Tait-colour \(B\).  A literal local duad rule lifts
    every standard five-cover of \(B\) through the diamonds.  The
    34-vertex Petersen instance has an explicit target-standard SAT model
    and a two-checker LRAT for a 465-clause connected-kernel relaxation;
    iteration gives an infinite separation family.  Thus obligation
    “prove every bridgeless cubic graph has a connected-kernel flow” is
    closed as false.  Any surviving exchange obligation must permit
    disconnected joins and cannot impose a connected coordinate
    complement.
25. **Two derived minimum-support conditions are not sufficient for
    \(T\)-join packing:** a 22-vertex cyclically 4-edge-connected cubic
    graph has a displayed size-three exact-zero matching with connected
    terminal-even complement, all three colour-weighted \(T\)-join minima
    equal to \(|M|\), and all three quotient graphs forests, but no two
    edge-disjoint \(T\)-joins.  The obstruction is a forced four-cycle
    component carrying three marked edges, and two independent checkers
    enumerate all 512 joins.  The support is not globally minimum and the
    host has girth four, so the actual reduced-domain minimum-support
    exchange obligation remains open.  Any proof must use global
    minimality beyond the weighted inequalities and quotient-forest
    consequences.
26. **Unrestricted fixed-join preparation refuted exactly; reduced-domain
    exchange remains open:** a 38-vertex simple bridgeless cubic graph has
    a binary cycle with two-component complement containing exactly 125
    inclusion-minimal exact zero sets, every one of preparation minimum
    two.  A projection through two Petersen 2-poles gives the human proof;
    independent Python and JavaScript checkers replay the factored
    classifications and all \(2^{20}\) expanded cycles.  Both target
    verifiers accept a standard five-cover.  The graph has two nontrivial
    two-edge cuts, so this closes the unrestricted preparation obligation
    as false but does not rule out a theorem using the cyclically
    4-edge-connected, girth-at-least-10 minimum-counterexample hypotheses.
27. **Strict one-switch minimum-support descent refuted; neutral
    reconfiguration open:** a 16-vertex simple bridgeless cubic graph has a
    nonpacking size-two exact-zero matching for which every one of the
    \(3\cdot512\) constant-value binary-cycle switches either leaves the
    matching domain or has support size at least two.  Two independently
    written verifiers also enumerate all 128 \(T\)-joins and find no
    disjoint pair.  A checked neutral-then-decreasing path
    \(2\to2\to1\) reaches a packing globally minimum support.  Therefore
    local strict descent is closed as false, but the existential
    cardinal-minimum route survives.  The open obligation is to prove that
    a nonincreasing switch component at minimum cardinality contains a
    packing state, or to exploit the reduced cyclic-connectivity and girth
    hypotheses in another sound exchange argument.  The separate
    two-checker sublevel package proves that all 33,546 ordered
    support-\(\le2\) states on the six order-16 plateau hosts reach size
    one, with all 384 local plateaus at distance two.  This discharges only
    that finite boundary.  The complete hard order-18 extension independently
    replays 1,680,414 ordered sublevel states on 179 graphs and finds all
    7,704 local plateaus at distance two.  The bucket lemma reducing
    adjacency to equality of \(p\), \(q\), or \(p+q\) is proved directly.
    Minimum supports of size three or more remain the open obligation.
28. **Fano one-switch domination refuted; component parity still
    eliminated:** the disconnected statement first failed on two disjoint
    bad blocks.  The connected statement is now refuted by the certified
    40-vertex composition in
    `search/connected-one-switch-countermodel-40v-20260726/`.  Three
    monochromatic edges in the ten-vertex Tait base `It?GYDKKO` lie on no
    common circuit by a direct triangle argument.  Replacing them with
    three attached bad blocks forces every connected circuit to leave one
    block unchanged, which blocks all seven values after the switch.  The
    independent checker enumerates all 30 base circuits and all 6,780
    final circuits.  The graph has an explicit three-cover, padded by two
    empty coordinates, so this closes only the domination route.  The
    earlier 2,614-vertex \(H_5\)/LRAT package remains a valid superseded
    construction.  The structural
    lemma remains valid: for every actual three-bit value class \(M_k\), a
    linear functional taking \(k\) to one gives a binary cycle containing
    \(M_k\), so \(G-M_k\) already has a \(\partial M_k\)-join and the
    component-parity branch is impossible.  Remaining Fano-flow questions
    must use different initial-flow selection, more than one switch, or a
    stronger global invariant.  A reduced one-switch lemma confined to
    cyclically 4-edge-connected cubic graphs would still suffice by the
    audited two- and three-edge-cut reductions.  It survives the
    composition countermodel and has exact positive evidence on all 20
    strict order-22 snarks: 63,251,330 flow orbits, 279,836 initially bad,
    and zero switch-local bad flows.  The retained 38-graph strict
    order-24 extension adds 617,079,260 flow orbits and 5,161,169 bad
    flows, again with zero switch-local bad flows.  Its identities and
    premises are independently checked; completeness relies on the retained
    Snarkhunter run.
29. **Oum-potential pure-merge one-circuit route refuted; reduced branch
    open:** the exact 12-vertex cap in
    `search/fano-pure-merge-one-switch-countermodel-46v-20260726/` has a
    unique gauged potential system, even after deleting its selected port,
    and forces all 15 co-occurrences on six coordinates.  A coordinate
    \(K_6\) makes pure merging into five classes impossible.  Grafting three
    caps at a noncyclable monochromatic edge triple gives a 46-vertex simple
    connected bridgeless cubic graph for which every connected circuit
    leaves one rigid cap untouched.  This proves, without SAT, that no one
    connected-circuit switch repairs pure mergeability.  An independent
    checker verifies all finite ingredients and all 128 starting potential
    solutions.  The graph has a three-cycle double cover and three
    nontrivial two-edge cuts.  Thus a cyclically 4-edge-connected version
    would still be sufficient for the minimum-counterexample route and is
    the surviving formulation to prove or refute.
30. **Connected eight-mark branch sharpened; signed-holonomy closure
    open:** pairing the eight suppressed marks by the four zero edges
    gives the audited necessary inequality
    \(|\delta_H(X)|+p_P(X)\ge4\) on every cyclic core shore.  An
    independently written clean-room checker excludes all 105 pairings of
    the retained order-60 stable-eight core.  Universal separation and
    mark precolouring guarantee a binary cycle containing all eight marks,
    so the residual obstruction is exactly componentwise marked parity.
    In the bichromatic incidence code this is signed balance, equivalently
    trivial \(\mathbb F_2\)-voltage holonomy, and the full selector/potential
    system is quadratic rather than linear.  The remaining obligation is
    to prove that the paired-cut, girth, universal-separation, and
    minimum-support hypotheses force a balanced selector, or to produce a
    core satisfying all those hypotheses whose every selector has
    nontrivial signed holonomy and then test its expansion with a
    certificate-producing standard five-CDC solver.
31. **Size-four branch order bound improved to 88; closure still open:**
    precolouring all eight suppressed marks alike puts them on eight
    vertex-disjoint bichromatic circuits, one mark per circuit.  Restoring
    the suppressed endpoints turns these into eight vertex-disjoint odd
    circuits in the ambient cubic graph.  Ambient girth at least ten
    forces each to have length at least eleven, and therefore
    \(|V(G)|\ge88\).  The proof is elementary and recorded in
    `docs/kempe-transversality-and-eight-mark-girth.md`.  This is a lower
    bound, not a resolution: the remaining obligation is still the
    balanced-selector/signed-holonomy closure for the connected
    eight-mark core (the \(4+4\) branch is already eliminated by the
    four-mark closure theorem).
32. **Marked trace containment discharged; component topology open:**
    universal separation gives arbitrary mark precolouring, which rules
    out every nonempty cut supported inside the marked matching.  Hence
    deleting the marks leaves the core connected and the binary
    cycle-space restriction to all marked coordinates is surjective.
    Every prescribed trace is attainable.  An independent audit passed
    the proof after two notation/scope corrections.  This is a complete
    linear result but does not make each circuit component marked-even.
33. **Eulerian factor quotient proved; automatic lifting refuted:** the
    all-\(c\) lifted \(ac\)-factor contracts, after deleting \(M\), to a
    connected Eulerian multigraph with eight marked vertices.  It always
    has two edge-disjoint marked joins, but those joins lift precisely
    when a local three-state routing condition holds on every factor
    circuit.  A four-vertex Eulerian quotient has only two disjoint join
    pairs and both fail this condition.  The actual branch excludes the
    literal example.  An unavoidable single terminal-gap failure in an
    actual quotient forces a cyclic ambient 4-cut with two zero edges or
    a cyclic 6-cut with all four.  The remaining obligation is to reduce
    those cuts and the other gap equations, or find a compliant
    obstruction.
34. **Order-80 vertex-transitive equality scope eliminated:** among the
    33 cubic vertex-transitive order-80 census graphs, short-cycle
    incidence certificates eliminate 32 from the marked-girth condition.
    The sole girth-ten graph has 426,256 normalized Tait colourings and no
    universally separated eight-edge matching.  Exact encodings, hashes,
    and cross-checks are frozen.  Vertex-transitivity is not a sound
    reduction for a minimum counterexample, so the arbitrary equality
    case and all larger orders remain open.
35. **Complementary quotient construction excluded at equality:** when
    all eight \(ac\)-factor circuits are marked, the local lift equations
    for a quotient join and its full complement sum to \(0=1\) around a
    marked \(bc\)-circuit.  Hence any successful quotient pair at
    equality must leave some quotient edge unused.  This is a no-go
    theorem for the canonical quotient construction, not a nonpacking
    theorem.
36. **Cyclic four- and six-cut interfaces remain exact bottlenecks:** the
    four-cut word \(0,0,b,b\) projects both sides of the published
    exceptional four-pole signature pair, so boundary parity and minimum
    support alone do not reduce it.  In the six-cut branch, a global
    balanced all-eight cycle exists exactly when both four-mark shores
    have componentwise-even closed certificates.  Root-avoiding trace
    feasibility is proved, but root-avoiding component parity under the
    full inherited cut and girth hypotheses remains open.
37. **Order-88 equality case eliminated; larger size-four branch open:**
    ambient girth makes the equality \(ac/bc\) incidence multigraph
    simple.  A Kempe switch then creates a bichromatic \(C_{50}\)
    containing four marks; the \(4+4\) version would require an impossible
    simple 5-regular \(4\)-by-\(4\) incidence graph.  A blind independent
    audit passed the human proof.  Thus the extremal exact-zero size-four
    branch first advanced to \(|V(G)|\ge90\).  Obligation 38 records the
    subsequent low-surplus improvement.
38. **Orders through 94 eliminated in the connected size-four branch:**
    the three-matching cycle-rank argument gives the general Kempe
    incidence inequality \(2p+u\le d+2\).  Girth gives matching
    marked--marked and marked--unmarked overlap bounds, and exact surplus
    capacity excludes ambient orders \(88,90,92,94\).  An independent
    reconstruction passed the proof, so this branch has
    \(|V(G)|\ge96\).  An explicit abstract order-96 incidence matrix
    passes every proved pairwise and simultaneous-switch constraint,
    showing that this method alone cannot improve the bound.
39. **Rooted bridge mechanism eliminated; four-way linkage open:** under
    the marked cyclic-cut inequality, a bridge after deleting the
    forbidden cap creates an unmarked 2-cut whose shores must contain
    two marks each.  The two-mark shore theorem then supplies a closed
    cap-avoiding certificate.  The proof also applies under the weaker
    inequality inherited by the opposite cyclic-six-cut cap.  Every
    surviving rooted failure is therefore 2-connected after cap
    deletion and has three cross-intersecting complementary pair-cycle
    systems.  Excluding that simultaneous four-way linkage, or finding
    a fully compliant realization of it, remains open.
40. **Exceptional four-pole pair converted to rooted packing:** the
    canonical \(D_5\) quotient lift is exactly an ordered pair of
    edge-disjoint terminal joins, and the exceptional \(AT_\pi\) versus
    \(T_\pi T_\pi\) boundary types record use versus avoidance of the
    nonzero cap.  A zero-free cyclic-four-cut shore always has the
    avoiding state, so only internal-zero distributions \((1,1)\) and
    \((2,0)\) survive.  Exact ten-state composition forces a smaller
    exceptional four-type factor; the five-type case has one auxiliary
    escape.  The remaining obligation is the resulting rooted four-way
    linkage/exceptional-signature atom, not boundary-orbit ambiguity.
