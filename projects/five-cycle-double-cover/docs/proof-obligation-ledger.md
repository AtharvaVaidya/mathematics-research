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
17. **Exact reduction established; unrestricted exchange lemma refuted:**
    for any exact-zero
    matching \(M\), the condition \(A\cap B=M\) is exactly the packing of
    two edge-disjoint \(T\)-joins in
    \((G-M,T=\partial M)\).  The restricted flow proves bridgelessness,
    but a blind audit corrected the claim that the minimum \(T\)-cut is
    automatically two.  A \(T\)-odd component gives cut minimum zero and
    no \(T\)-join.  If all components are \(T\)-even, the minimum is two
    and the imported Codato--Conforti--Serafini theorem makes an
    odd-\(K_{2,3}\) graft minor necessary for remaining failure of this
    fixed \(M\).  A universal proof would have followed by showing that a
    genuinely nonpacking minimum exact-zero matching can be exchanged for
    a smaller one.  The 130-vertex package
    `search/minimum-zero-exchange-countermodel-130v-20260727/` now refutes
    this: \(r_f=r_M=5\), while the least matching/four-flow extension has
    size six.  A proved partial switch says that every \(T\)-join
    \(J\) meets each of the three nonzero flow-color classes in at least
    \(|M|\) edges, hence \(|J|\ge3|M|\); this does not yet imply packing.
    Therefore no unrestricted complete exchange theorem is possible.  The
    finite package
    does prove that all 20,749 minimum supports in the complete order-20
    hard corpus and all 92,313 minimum supports of reconstructed \(H_3\)
    extend; the latter enumeration is complete by a two-checker LRAT.
    Existentially, every one of the 12,892 frozen hard order-22 rows has an
    extending minimum support; seven size-two lower bounds have LRATs
    accepted by both proof checkers.
    These finite discharges remain useful controls but do not restore the
    refuted universal obligation.  A narrower theorem may still use the
    cyclically \(4\)-edge-connected, girth-at-least-ten
    minimum-counterexample hypotheses.
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
    Snarkhunter run.  The exact cut reduction in
    `docs/fano-canonical-join-cut-certificates.md` now shows that failure of
    all seven value-class packing tests forces a rainbow-odd component for
    every nonzero functional.  For a fixed functional and line value,
    failure of all line-preserving switches is equivalent to a split cut in
    \(G-M_t\), with a four-shore checkerboard whose two diagonal systems
    carry the two affine translation pairs.  This is a human-checkable
    necessary condition, not yet an uncrossing proof: cyclic
    4-edge-connectivity does not by itself exclude the split cut after
    deleting \(M_t\).  The stronger common-dual argument in
    `docs/fano-combined-line-span.md` proves universally that, for a fixed
    Fano line, the sum of the three initially valid switch images contains
    the full rainbow-defect vector.  Its explicit telescoping potential
    rules out a common odd split-cut dual without any girth or connectivity
    hypothesis.  This remains a linearized result: simultaneous affine-edge
    overlaps contribute a quadratic correction.  The exact residual
    formulation is now two binary cycles \(p,q\) which cover the line
    factor and for which \(\{e:p_e=q_e=1\}\) has even degree after every
    factor component is contracted.  Universal feasibility for a
    prescribed line is now refuted by the certified Petersen package
    `search/fano-two-cycle-petersen-countermodel-20260726/`.  Two lines
    of its displayed flow have perfect-matching factors whose contractions
    are \(K_5\).  A clean lift would partition \(E(K_5)\) into four even
    color classes; the \(3+3+3+3>10\) count forces an absent class and
    hence a nowhere-zero \(\mathbb F_2^2\)-flow, contradicting the
    Petersen graph's lack of a Tait coloring.  Ordinary CNFs, DRAT proofs,
    and an independent 64-by-64 cycle-pair enumeration certify both failed
    lines.  The same flow has five cleanable lines and the graph has an
    explicit five-CDC, so the then-surviving obligation was the assertion
    that every fixed three-bit flow has **some** cleanable line, not
    prescribed-line cleaning.  That assertion is now refuted by
    `docs/fano-all-seven-petersen-sum-obstruction.md` and
    `search/fano-all-seven-petersen-sums-20260727/`.  The first targeted
    Petersen three-sum gives an order-26 flow whose seven projection
    formulas are all UNSAT; seven textual DRATs and an independent
    exhaustive cycle-space classifier agree.  A 34-vertex tree of four
    Petersen factors gives a SAT-free human proof: three leaf factors have
    perfect-matching obstruction sets \(\{4,5,6\}\), \(\{1,2\}\), and
    \(\{3,7\}\), and the leaf-localization lemma pulls any hypothetical
    global clean pair back to the corresponding Petersen factor.  Both
    graphs have explicit positive five-covers.  Thus only a theorem that
    first selects a suitable flow, or a different route, can survive.
    One exact
    positive boundary is also proved:
    because every switch image has even weight on the factor components,
    the common-span theorem implies that any line factor with at most two
    components is good already or is cleaned by one valid switch.  Ordinary
    CNFs plus direct semantic checking also find the quadratic system SAT
    on all fourteen lines of the retained 40- and 46-vertex connected
    local countermodels; those models are evidence, not a universal proof.
    Two further reductions now sharpen the surviving existential branch.
    A fixed nowhere-zero \(\mathbb F_2^2\)-flow cleans every binary
    projection, so an all-seven search may be restricted soundly to snarks.
    The explicit \(D_5\) extension table in
    `docs/fano-triangle-expansion-invariance.md` proves that
    fixed-projection cleanability is invariant under vertex-to-triangle
    expansion and that such an expansion cannot create the first covering
    three-dimensional all-bad subspace.  Finally, the exact two-checker
    census in `search/fano-some-good-line-census-20260726/` finds no
    all-seven obstruction in every connected simple bridgeless cubic graph
    through order 18, the retained strict snarks at orders 20--24, or ten
    retained cyclically 5-connected order-26 snarks.  This is a finite
    boundary.  The new order-26 countermodel has a cyclic three-edge cut and
    was not among the ten cyclically 5-connected order-26 controls, so the
    two computations are consistent.  A cyclically 4-edge-connected
    every-flow version remains logically separate but is no longer needed
    as an unqualified claim.
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
    the surviving formulation to prove or refute.  The natural
    prescribed-edge proof of that reduced statement is now itself
    refuted by
    `search/fano-circuit-avoidance-countermodel-18v-20260728/`.
    On the first Blanuša snark a merge-bad flow has connected bridgeless
    \(G-M_6\), but three value-3 edges lie on no common circuit because of
    a two-vertex separator.  A disconnected binary cycle through the
    triple repairs all four compatible \(K_6\) covers.  No odd cut is
    contained in the triple, so Knappe--Pitz fails here through its
    3-edge-connectivity hypothesis rather than its odd-cut criterion.
    The same flow has another connected repair; therefore the existential
    reduced formulation remains open.  Separately, on at most eight old
    coordinates, \(H\to R_5\) is equivalent to
    \(\chi(H)\le5\) by the \(K_6/K_3\vee C_5\) dichotomy, so general XOR
    compression does not widen this branch.
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
38. **Orders through 100 eliminated in the connected size-four branch:**
    the three-matching cycle-rank argument gives the general Kempe
    incidence inequality \(2p+u\le d+2\).  Girth gives matching
    marked--marked and marked--unmarked overlap bounds, and exact surplus
    capacity excludes ambient orders \(88,90,92,94\).  An independent
    reconstruction passed the proof.  Three later local girth lemmas
    eliminate the displayed abstract survivor and impose a doubled-neighbour
    spacing constraint.  A solver-free census exhausts all 109 canonical
    order-96 profile pairs with zero matrices, and an independent QF_LIA
    encoding returns 109/109 UNSAT.  A separate audit normalized all
    108,900 labelled profile pairs and repeated the search without the
    forward prune.  At order 98, the general incidence inequality first
    excludes the arithmetically possible unmarked circuit.  A
    human-checkable weighted-prism/\(K_{3,3}\) lemma supplies the missing
    diagonal overlap cap.  A solver-free census then exhausts all 335
    canonical profile pairs with zero matrices; independent Z3 and HiGHS
    formulations agree, and a prune-free replay remains empty after
    9,193,235 nodes.  At order 100, a human argument excludes unmarked
    factor circuits.  Exact weighted row/column stars reduce 1,002
    all-marked profile pairs first to 155 and then to three.  Three
    profile-level CNFs choose every incidence matrix, cyclic position
    set, bijection, and twist inside those alignments; independently
    checked LRATs prove all three UNSAT already in the deleted-matching
    core.  A producer-free semantic checker regenerates the base formulas
    and verifies all 996,904 lazy clauses as forced short circuits.
    Hence this branch now has \(|V(G)|\ge102\).  This remains a branch
    bound, not a five-CDC resolution.
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
41. **Ozeki four-terminal gate reduced to low separator interfaces:**
    after certificate-safe irreducibility reductions, Ozeki's \(V_8\)
    outcome contains two explicitly displayed vertex-disjoint
    pair-circuits and cannot be a rooted failure.  Before any nontrivial
    one-terminal reduction, the four private factor-circuits also prove
    triple cyclability and exclude the nice decomposition.  A failure of
    the remaining forbidden-vertex path hypothesis has one of two exact
    forms.  If deletion of the forbidden vertex is not 2-connected, a
    two-cut has terminal split \(2+2\), or split \(1+3\) with a singleton
    one-terminal side.  Directly splicing two triple-circuits eliminates
    the \(2+2\) split.  If deletion remains 2-connected, three stable
    vertices separate the four terminals into exactly four components
    with boundary profile \(2222\) or \(2223\).  Triple cyclability
    eliminates \(2222\) and forces the unique incidence graph
    \(K_{4,3}\) minus a three-edge matching.  Irreducibility makes all
    three boundary-two components singleton terminals.  Any two such
    rows share a separator neighbour, so their private circuits cannot
    be vertex-disjoint.  This eliminates the three-vertex row star.
    Independently, its counterfactual triangular-prism quotient would
    force the marked and root edges to have the same Tait colour by a
    per-colour cross-edge count.  The \(1+3\) singleton two-cut is now
    also closed under the same simultaneous premises.  If its singleton
    is \(z_1\), adjacent to separator vertices \(w,u\), then
    \(K=H-\{w,z_1\}\) is 2-connected: a cut vertex would induce a
    terminal-free, one-terminal, or \(2+2\) side behind
    \(\{w,x\}\), contradicted respectively by irreducibility, private
    circuit disjointness, or triple-circuit splicing.  The four vertices
    \(u,z_2,z_3,z_4\) all have degree two in \(K\).  A general endpoint
    lemma, obtained from Ozeki's Section 4.9 path-obstruction
    description with endpoint-safe one-terminal lifting, says that a
    2-connected subcubic graph has a path starting at any one of four
    specified degree-two vertices and passing through the other three.
    The two obstruction outcomes would require either at least seven
    incidences at two subcubic separator vertices or one vertex adjacent
    to four terminals.  This supplies P4 in the exact
    irreducible/private-circuit state.  Literal preservation through
    arbitrary one-terminal reductions is now refuted and replaced by an
    exact trace table.  A separator containing another terminal is
    certificate-producing under triple cyclability.  For a
    terminal-free separator, the sole marked-borrower state
    \(R^\ast=R_j\) leaves a pairwise disjoint \(2+1+1\) circuit packet.
    The full marked-cut and universal-separation hypotheses permit that
    borrower: an audited order-56 graph realizes it and has an explicit
    root-avoiding four-mark circuit.  What remains open is using the
    \(2+1+1\) packet to close the two projected outer interfaces N
    (expanded singleton of a nice decomposition) and E (nested expanded
    \(1+3\) endpoint interface), not an augmented \(K_{3,2}\) attachment
    case.  The exact simultaneous-state proof is in
    `docs/rooted-four-mark-singleton-endpoint-closure.md`; a finite audit
    checks 1,100,688 subdivided cubic endpoint instances through base
    order twelve.  The trace table, packet lemma, and borrower certificate
    are in `docs/one-terminal-trace-lift-frontier.md`.
42. **Exceptional split atoms isolated, not eliminated:** the surviving
    \((1,1)\) and \((2,0)\) internal-zero distributions split by whether
    the exceptional shore has a simple opposite cap or a terminal-flanked
    cap.  Smoothing the latter is exact.  In the simple six-mark case a
    \(2+4\) bridge descends to a closed four-mark atom, while a \(3+3\)
    bridge exposes a cyclic five-cut of type \(000bb\).  These sharper
    atoms remain open.
43. **Factor-signature closure refuted; binary rooted state remains:**
    the aligned unmarked-crossing equality atom cannot be closed by
    forcing a bichromatic cap circuit.  At order 20, the one-sided
    three-mark signature-cover claim first fails; its witness also
    exposed that the global marked-cut screen must test the complementary
    one-mark shore.  A second order-20 cap then refutes even the corrected
    two-sided version.  It has 36 normalized Tait colourings, three
    universally separated marks, paired cyclic two-cut mark counts
    \(2,2\), and signatures
    \(\varnothing,\varnothing,\{01,12\}\).  Independent C++ and
    standard-library Python checkers are frozen in
    `search/cap-signature-order20-two-sided-20260727/`.  This is not a
    rooted counterexample: gluing the singleton cap at the missing pair
    gives two order-26 marked graphs with 480 componentwise-even
    all-mark cycles and no forced unmarked edge.  The three-mark cap has
    every binary odd open state.  The remaining obligation is therefore
    the genuine root-avoiding component-parity state under the full
    \(2+1+1\) packet, T3, P4, and global marked-cut hypotheses; no
    factor-signature surrogate remains valid.
44. **Rooted failure reduced to an odd-\(K_{2,3}\) graft minor:** after
    deleting the forbidden root and subdividing the four marks, the
    bridge-elimination lemma gives a 2-connected subcubic graph with four
    degree-two terminals.  A closed rooted certificate is exactly a pair
    of edge-disjoint terminal joins, and the minimum terminal-cut is two.
    The Codato--Conforti--Serafini packing theorem therefore makes an
    odd-\(K_{2,3}\) graft minor necessary for every surviving rooted
    failure.  The elementary proof is in
    `docs/rooted-four-mark-odd-k23-reduction.md`.  Excluding this minor
    using the simultaneous private-circuit, T3, P4, marked-cut, and
    root-colour data remains open.
45. **Prescribed rooted cap atom absent through order 20:** the corrected
    physical-port classifier exhausts every connected simple cubic cap
    through order 20.  There are eight aligned packet states at order 18
    and 132 at order 20; every one has the prescribed odd state, and no
    state forces an internal edge of the required root colour.  A separate
    all-pairs intersection checks all 3,396 order-20 paired-cut cap triples
    and likewise finds no eligible forced root.  Counts, hashes, commands,
    and scope limitations are frozen in
    `scratch/rooted-cap-order20-result.json`.  This is a finite exclusion,
    not the universal rooted theorem.
46. **Cycle-transparent odd-\(K_{2,3}\) models excluded:** replacing the
    four terminal branch vertices of the critical graft by private cycles,
    then adding the retained edge and deleted root required by the
    one-mark boundary count, gives 3,888 cyclic-order rows when the fifth
    branch is a vertex and 5,346 when it is also a cycle.  Respectively
    3,726 and 5,184 have a rooted certificate.  Each mode leaves 162
    Tait-colourable failures, but only six colourings make all marks
    common-colour, and a direct three-cut parity argument makes the root
    that same colour in all twelve controls.  Hence none satisfies the
    inherited different-colour root premise.
    The exact generator and result are
    `scratch/search_odd_k23_cycle_expansions.py` and
    `scratch/odd-k23-cycle-expansion-result.json`.  General graft-minor
    branch sets are not yet reduced to this cycle-transparent form.
47. **A first nontransparent odd-\(K_{2,3}\) branch move is
    certificate-producing:** applying the canonical two-attachment
    chord relocation to all 324 transparent certificate-free bases gives
    3,240 distinct marked rooted cubic graphs, all in the \(X\)-branch.
    Every graph has an explicit closed rooted certificate; a
    standard-library checker independently verifies the complete
    3,240-certificate bundle.  The screen excludes only this declared
    one-chord move, not arbitrary branch sets.  Counts, hashes, commands,
    and the scope warning are frozen in
    `scratch/odd-k23-one-chord-result.json`.
48. **Two chord moves expose both global rooted premises:** two
    successive canonical relocations give 396,360
    distinct second-layer graphs.  Of 20,306 graphs with a compatible
    common-mark/different-root Tait colouring, 20,194 have a closed
    rooted certificate.  The remaining 112 are genuine rooted failures,
    but all violate both universal factor separation and the marked
    cyclic-cut inequality; in fact all six marked pairs are bad across
    their two normalized colourings, and every row has a one-mark cyclic
    two-cut plus at least one unmarked cyclic three-cut.  A separate
    standard-library checker independently verifies all 112 controls.
    The exact construction and scope are frozen in
    `scratch/odd-k23-two-chord-result.json`.  The next model must repair
    the low one-mark cut before it can distinguish the two global gates.
49. **Every direct cubic repair of the two-chord failures is
    certificate-producing:** all 15,008 internal-edge 2-switches that
    raise the unique one-mark cyclic two-cut boundary from two to four
    were checked.  Exactly 7,896 retain a common-mark/different-root
    Tait colouring, and every one has an explicit closed rooted
    certificate.  A project-independent checker validates the complete
    certificate bundle.  This is a finite repair theorem for the
    declared 112 controls, not a universal cut-repair lemma.  The frozen
    result is `scratch/odd-k23-two-cut-repair-result.json`.
50. **Four-mark core closure needs only one common-colour colouring:**
    a literal hypothesis audit of `four-mark-core-closure.md` shows that
    universal separation is used only to obtain a Tait colouring in
    which the four marks have one common colour.  The rest of the human
    proof uses only that fixed colouring, Tait cut parity, the marked
    cyclic-cut inequality, and the cited decomposition and
    prescribed-cycle theorems.  The theorem is therefore valid under
    the strictly weaker hypotheses “one common-colour Tait colouring +
    marked cyclic-cut inequality.”  This strengthens the unrooted
    closure but does not make its certificate avoid a prescribed root
    edge; the rooted \(2+1+1\) cap atom remains open.
51. **Root avoidance fails only through a multi-contact toggle
    obstruction:** in a common-colour Tait colouring, the factor circuit
    through a differently coloured root avoids all four marks.  If its
    intersection with every component of an unrooted marked-even
    certificate is empty or one path, symmetric difference removes the
    root and only merges marked-even components, yielding a rooted
    certificate.  Therefore every rooted failure forces at least two
    separated contacts with one certificate component, for every
    mark-free root circuit.  The complete elementary proof is in
    `docs/rooted-four-mark-unmarked-toggle.md`.  This adds a sound filter
    to the odd-\(K_{2,3}\)/\(2+1+1\) frontier but does not yet exclude
    multiple contacts.
52. **Forbidden-root edge reduction gives an exact independent
    four-cut gate:** in a simple cyclically \(4\)-edge-connected cubic
    factor, reduce the forbidden edge \(f=uv\) by deleting \(u,v\) and
    joining their two remaining neighbour pairs.  A fixed
    common-colour Tait colouring in which the four marks are separated
    makes their four reduced images a matching: any new adjacency
    would put two marks on one bichromatic factor circuit.  If the
    reduced graph is cyclically \(4\)-edge-connected, the
    Aldred--Ellingham--Hemminger--Holton four-edge theorem gives a cycle
    through the reduced marks, which lifts to an all-four circuit
    avoiding \(f\).  Pulling back a smallest cyclic cut when the
    reduction fails shows exactly that \(f\) lies in an independent
    cyclic four-edge cut.  Hence the rooted theorem is proved outright
    for cyclically \(5\)-edge-connected factors; only the root-containing
    four-cut interface survives at cyclic connectivity four.  See
    `docs/root-edge-reduction-four-cut-gate.md`.  This is a universal
    human-checkable rooted reduction, not the remaining four-cut
    closure or a five-CDC proof.
53. **Universally separated four-edge matchings are absent from the
    Tait-colourable order-22 domain:** canonical `geng` generation
    exhausts all \(7\,319\,447\) connected simple cubic graphs on 22
    vertices.  The direct
    edge-colouring checker and an independently written
    perfect-matching/even-two-factor replay agree shard by shard on
    \(7\,174\,735\) Tait-colourable graphs and \(95\,360\,112\)
    normalized Tait colourings; both find zero universally separated
    four-edge matchings among those Tait-colourable graphs.  Graphs
    without a Tait colouring are outside the theorem because both
    programs skip the otherwise vacuous universal-quantifier case.
    The replay additionally visits
    \(312\,583\,931\) perfect matchings.  Complete lower-order controls
    and one positive order-24 target-three control exercise both the
    zero- and positive-witness paths.  See
    `docs/order22-universal-four-separation-screen.md` and
    `scratch/order22-universal-four-separation-result.json`.  This is a
    complete finite theorem at order 22, not a universal separation
    theorem or a five-CDC proof.
54. **Terminal-distinct exceptional poles admit complete simple-cap
    enumeration:** a connected simple proper core with four distinct
    degree-two terminals always has a perfect matching of its terminals
    consisting of two nonedges.  Adding those edges gives a simple cubic
    cap.  If the pole is bridge-free and has either published
    exceptional exact signature, the cap is bridgeless and non-Tait:
    a cap Tait colouring would restrict to the pole, while
    Máčajová--Mazzuoccolo--Tabarelli Lemma 3.8 excludes a connected
    Tait-colourable pole with either exceptional signature graph.
    Therefore enumerating bridgeless non-Tait cubic graphs and deleting
    every independent edge pair is complete for this pole scope.
    Moreover, for a vertex-minimal two-cut-reduced exceptional pole,
    every simple cap is either cyclically \(4\)-edge-connected or has a
    cyclic three-cut disjoint from the cap edges, splitting the four
    terminals \(2+2\).  The latter is an exact five-pole interface, not
    an elimination.  See
    `docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`.
55. **The exceptional cyclic-three cap fork has a seven-state exact
    rooted factorization:** cutting the surviving \(2+2\) cyclic
    three-cut gives two rooted cubic three-poles.  Normalizing their
    three connector labels to the ordered triangle
    \((01,02,12)\) leaves seven stabilizer orbits for each root label.
    Exact gluing says that equality, intersection, or disjointness of
    the two root-label sets is respectively equivalent to the doubled
    boundary types \(AA,AT_\pi,T_\pi T_\pi\).  In the exceptional
    four-type family, the missing-\(AT_i\) orientation forces both
    rooted signatures to be the same singleton among
    \(\{01,02,12,34\}\); the other orientations force exact
    cross-intersection.  The exceptional five-type family forces one
    of exactly thirteen unordered disjoint rooted-signature patterns.
    A human proof and independent Python/JavaScript finite replay are
    in
    `docs/exceptional-cyclic-three-root-signature-factorization.md`.
    The rooted signatures themselves remain neither excluded nor
    realized.
56. **No order-18 simple four-pole core has an exceptional exact
    signature:** all \(4\,159\,098\) connected simple graphs with four
    degree-two terminals and every other vertex cubic have been
    classified by independent incremental-SAT and direct finite-domain
    implementations.  The programs make \(16\,453\,323\) exact mask
    queries apiece, agree on every streamed decision digest shard by
    shard, and find zero instances of the six exceptional ordered
    masks in the fixed five-colour \(D_5\) model.  A third parser
    independently checks transcript syntax and the exceptional flag.
    This is a complete finite theorem at order 18 only; it is not a
    universal four-pole theorem or an unbounded-colour classification.
    The frozen replay
    is `search/four-pole-order18-exceptional-20260727/`.
57. **Three-base-pair closure holds for rooted simple three-poles
    through order 17:** fixing connector triangle \((01,02,12)\), every
    nonempty exact signature of a nonbridge root contains one of
    \(\{12,03,04\}\), \(\{02,13,14\}\), or
    \(\{01,23,24\}\).  Independent direct-CSP and incremental-SAT
    screens test all \(15\,645\,623\) nonbridge roots on the
    \(654\,676\) canonical order-17 cores.  Their eight complete
    streamed transcript digests agree shard by shard, and both find
    zero violations.
    A complete \(3\times7\) relation table proves this only for the base
    pair itself.  The inference to an arbitrary containing signature is
    false: \(R=\{12,03,04,01\}\) and \(S=\{01\}\) give the mixed
    exceptional relation \(\{\mathsf E,\mathsf I\}\).  Hence one
    order-17 shore excludes equality-only and disjointness-only through
    total order 36, but not the mixed \({\cal E}_4\) orientation.
    Two shores within the finite frontier do exclude all exceptional
    relations.  See
    `docs/rooted-three-pole-base-pair-closure-target.md`.
58. **Five-CDC is exactly an anisotropic-flow problem in the elliptic
    four-space:** on the even-weight subspace \(V\leq\mathbb F_2^5\),
    the quadratic form \(q(x)=\sum_{i<j}x_ix_j\) has precisely the ten
    weight-two vectors as its anisotropic points.  The five Eulerian
    incidence coordinates are therefore equivalent, edge by edge and
    vertex by vertex, to a \(V\)-flow with \(q(\phi(e))=1\).  Equivalently
    it is a nowhere-zero binary four-flow avoiding a binary
    five-circuit in the nonzero value set.  This human-checkable
    reformulation includes loops and parallel edges but is not a proof
    of existence and does not add orientability.  See
    `docs/five-cdc-elliptic-quadratic-flow-model.md`.
59. **The claimed simple terminal-distinct lower bound of order 28 is
    withdrawn; the cyclically-four cap censuses remain valid:** the
    simple-cap theorem reduces the cyclically-four branch at each even
    order to all
    independent-edge deletions from bridgeless non-Tait cubic caps.
    At order 22, two independent filters select the same \(12\,892\)
    caps from the complete \(7\,319\,447\)-graph canonical source.  Their
    \(5\,956\,104\) deletions have been classified by independent SAT and
    direct finite-domain solvers with matching complete transcript
    digests and zero exceptional hits.  A third verifier checks the
    canonical identities, cap premises, the entire deletion stream, and
    both decision ledgers.  The former proof that any first exception
    through order 36 has a cyclically 4-edge-connected cap used the false
    one-sided inference corrected in item 57.  Snarkhunter generates 155
    such non-Tait caps at order 24 and 1,297 at order 26.  Both exact
    classifiers give full mask `0x3ff` on all \(86\,490\) order-24 and
    \(859\,911\) order-26 deletion poles.  A solver-independent verifier
    reconstructs the latter stream and checks both complete tables and all
    shard logs.  Therefore every retained cyclically-four cap deletion
    has full signature, but a mixed-orientation cyclic-three atom is not
    reduced to that corpus.  No global lower bound for all bridge-free
    connected simple terminal-distinct poles follows.  This also does not
    cover repeated terminals, nonsimple cores, or unbounded-colour CDC
    signatures.
    See `search/four-pole-order26-cyclic4-cap-20260727/`.
60. **The quotient-lift theorem has an exact one-cycle
    component-parity normal form:**
    in the elliptic normal form
    \(q(x,y,t,z)=x+y+xy+tz\), the first three coordinates give a
    nowhere-zero \(\mathbb F_2^3\)-flow \(f\).  For the Fano line
    \(L=\{t=0\}\setminus\{0\}\) and \(r=(0,0,1)\), the last coordinate
    is a binary cycle \(C\) and edgewise anisotropy is exactly
    \(M_r\subseteq C\subseteq M_r\cup M_L\).  This cycle exists exactly
    when every component of \(G[M_L]\) contains an even number of
    vertices of \(\partial M_r\).  A singular-vector quotient proves
    the converse from every five-cover.  Thus existence of some
    \(f,L,r\) with this parity property is equivalent to Five-CDC.
    This repackages the earlier all-four-outside-values boundary
    criterion in `docs/proof-agent-audit.md`; flow conservation shows
    that either every \(r\notin L\) passes on a line component or all
    four fail.
    Fixed-flow and one-connected-circuit-switch versions are refuted by
    the already retained eight- and ten-vertex examples, respectively;
    the latter has an explicit two-switch repair.
    Flow selection or a genuinely multi-step transformation remains
    open.  See `docs/five-cdc-fano-component-parity-lift.md`.
61. **Every constant-step Fano reconfiguration theorem is refuted, but
    component domination remains open:** a recursive connected simple
    bridgeless cubic family has \(3^d\) certified bad-block ports while
    every connected circuit meets at most \(2^d\) ports.  Hence the
    displayed flow has distance at least
    \(\lceil(3/2)^d\rceil\) from the Fano-good set, if that set is
    reachable.  Every member is Tait-colourable and has an explicit
    three-cycle double cover, so this is not a Five-CDC obstruction.
    The 40-vertex first member has exact distance two, with the two
    switches and all parity rows independently replayed by
    `scratch/verify_fano_multistep_two_switch.py`.  The remaining
    resolution obligation is unbounded global flow selection or proof
    that every relevant reconfiguration component meets the good-flow
    set.  See
    `scratch/fano-multistep-reconfiguration-audit-20260727.md`.
62. **Internal cyclic four-edge-connectivity of a pole does not force a
    full fixed-five signature; the focused cap lift remains open:** the
    explicit order-16 terminal-distinct pole
    `O????A?[BOI_g_Ao?kCo?` has exact mask `0x3fe`, with a direct scalar
    parity proof excluding \(AA\).  Every simple cap creates a cyclic
    triangle cut, so it does not refute the deletion-pole claim for
    cyclically-four-connected non-Tait caps.  In that focused geometry,
    every component outside the four prescribed endpoints has even
    attachment number, eliminating the scalar obstruction.  The exact
    unresolved lift asks for an \(\mathbb F_2^2\)-flow whose zero set
    contains the prescribed independent pair and whose complement
    packs two edge-disjoint boundary joins.  See
    `scratch/fixed-five-d5-four-pole-full-signature-frontier.md`.
63. **Flow resistance through five does not obstruct prescribed
    \(AA\) on the reconstructed \(H_n\) family:** for every one of the
    \(97\,608\) independent edge pairs across \(H_2,H_3,H_4,H_5\), an
    explicit fixed-five \(D_5\)-labelling assigns the same label to the
    prescribed edges.  Cutting those edges gives boundary type \(AA\).
    A greedy set of 394 complete labellings covers every pair, and a
    solver-independent verifier checks all vertex equations and recomputes
    the coverage.  This is finite evidence for the focused cap lift, not
    its universal proof.  See
    `search/mnp-h2-h5-aa-deletion-probe-20260727/`.
64. **The rooted base-pair target is proved whenever the one-vertex cap
    is Tait-colourable:** normalize a Tait colouring to the connector
    triangle \(01,02,12\).  A proper cycle through the nonbridge root can
    be translated by \(0123\) and \(0124\); the two translations and the
    original labelling realize exactly one of the three base pairs.  One
    Tait cap excludes equality-only and disjointness-only; two Tait caps
    exclude all exceptional relations.  The mixed
    \(\{\mathsf E,\mathsf I\}\) relation survives one-sidedly.  The
    minimal exceptional cap is simple, bridgeless, cubic, and has no cyclic
    two-edge cut.  A cutvertex would expose a bridge, and a two-vertex cut
    would expose a cyclic two-edge cut, so the cap is 3-connected.  The cited
    three-sum decomposition theorem therefore applies and its factor tree is
    a path.  Both endpoint factors
    are non-Tait for \({\cal E}_5\);
    an \({\cal E}_4\) endpoint may be Tait only at a mixed-orientation
    end cut, with the opposite root signature correspondingly restricted.
    See `docs/rooted-three-pole-tait-cap-closure.md`.
65. **Cyclically-four non-Tait endpoint factors through order 26 have
    base-pair closure:** the complete retained order-\(20,22,24,26\)
    sources contain \(6,31,155,1297\) factors.  All 38,244 vertex
    deletions and 1,360,452 nonbridge roots were classified by independent
    incremental-SAT and direct finite-domain implementations, with matching
    complete transcripts, 4,157,844 calls per implementation, and zero
    empty or violating rows.  A solver-independent verifier reconstructs
    every source premise, core, root, decision, and shard summary.  With
    the Tait-cap and rooted-order-17 theorems this forces both endpoint
    factors above order 26 for equality-only or disjointness-only
    cyclic-three relations, giving cap order at least 54.  It does not
    eliminate the mixed relation by the original one-sided argument; item
    67 supplies the missing fork transport.  See
    `search/rooted-three-pole-nontait-endpoint-frontier-20260727/`.
66. **The mixed cyclic-three branch has a completed path-rooted triangle
    induction through cap order 26:** connector-end
    \(K_4\) contraction preserves the class of fork triples
    \(\{qr,ps,pt\}\), while a root-end triangle forces exactly such a
    triple.  Hence every nonempty path-rooted cap signature contains a
    fork triple whenever its triangle-free contraction has base-pair
    closure.  In a relation with no disjoint pair, the common
    intersectors of a fork are exactly \(\{pq,pr\}\), so the opposite
    signature has size at most two and cannot contain its own fork.
    At cap order at most 26 both capped shores have order at most 24.
    Two exact implementations now classify every one of the 10,824,084
    proper roots in the 330,790 vertex-deleted cores from all 13,901
    retained triangle-free 3-connected non-Tait caps at orders 20, 22,
    and 24.  Every signature is nonempty and base-pair closed, and the
    complete transcripts agree byte-for-byte.  Thus the finite branch is
    closed independently of item 67.  See
    `docs/rooted-cap-triangle-induction.md` and
    `search/rooted-three-pole-c3-cap-frontier-through24-20260727/`.
67. **A root-end base pair lifts through an arbitrary factor path as a
    fork, restoring the simple terminal-distinct order-28 lower bound:**
    fix one labelling of the rest of a rooted shore and normalize the
    ordered triangle at its root-end factor interface.  All three
    endpoint base-pair labellings can be inverse-normalized and glued to
    that same fixed remainder.  The whole shore signature therefore
    contains a coordinate image of a base pair, namely a fork
    \(\{qr,ps,pt\}\).  Any two forks have both an unequal intersecting
    cross-pair and a disjoint cross-pair; a direct proof and the complete
    \(30^2\) table are retained.  Hence the completed endpoint theorem
    through factor order 26 excludes the mixed cyclic-three relation
    whenever both endpoint factors have order at most 26.  A surviving
    mixed branch has one endpoint factor of order at least 28 and cap
    order at least 30; the pure relations still force both endpoints
    above 26 and cap order at least 54.  Together with the cyclically-four
    cap census through order 26, this soundly restores the global
    simple terminal-distinct exceptional-pole lower bound of order 28.
    A first order-28 exception must have a cyclically four-edge-connected
    cap.  This is a fixed-five structural result, not Five-CDC.
    See `docs/rooted-cap-end-factor-fork-lift.md`.
68. **Restricting the eight-coordinate triangle lift to five points has
    exactly one local source of freedom:** every five-point subset
    \(S\subseteq\mathbb F_2^3\) has the form
    \(\{0\}\dot\cup(a+H)\) after translation, for a unique Fano line
    \(H\).  A vertex whose incident flow values form \(H\) has four local
    coordinate triangles contained in \(S\); each of the other six local
    Fano lines has exactly one.  Line-valued edges receive two labels in
    \(a+H\), while every outside-valued edge receives \(\{0,f(e)\}\).
    Componentwise coordinate parity is therefore exactly the existing
    Fano component-parity lift, with no hidden local compression cases.
    Independent Python and JavaScript enumerations agree on all
    \(56\cdot7=392\) five-set/line cases.  The unresolved obligation
    remains global selection of the flow and special line, not local
    triangle choice.  See
    `docs/five-cdc-five-point-triangle-list-lift.md`.
69. **Rooted minimum exact-zero supports obey a quotient-forest theorem,
    but not every rooted minimum packs:** for prescribed independent
    roots \(R\subseteq M\), inclusion-minimality implies that
    \(Q_c-R\) is a forest for each nonzero quotient-flow value \(c\);
    hence every quotient cycle uses a root and the quotient cycle rank is
    at most two.  The stronger all-minima packing assertion is false on a
    22-vertex simple cubic cyclically 4-edge-connected non-Tait graph:
    the rooted minimum \(\{24,27,31\}\) has a one-vertex degree-three
    obstruction to the even-marked circuit criterion.  A checked
    root-preserving neutral switch reaches the packing minimum
    \(\{13,24,27\}\), with two explicit disjoint \(T\)-joins.  The
    standard-library replay passes.  Across the retained complete
    order-22 focused corpus, all 14,322 independent pairs have some
    packing rooted minimum, although 352 also have nonpacking minima.
    The universal obligation is therefore rooted flow feasibility plus
    reachability of packing inside the rooted minimum neutral component,
    or exclusion of the surviving size-five parity and odd-\(K_{2,3}\)
    graft branches.  See
    `scratch/focused-aa-rooted-minimum-frontier.md`.
70. **Deleting the four endpoints of prescribed independent roots leaves
    matching deficiency at most two, but the theta choice is open:** for
    every finite 3-edge-connected cubic graph \(G\), roots \(R=\{e,f\}\),
    and \(U=V(e)\cup V(f)\), the Tutte--Berge inequalities give
    \(\operatorname{def}(G-U)\le2\).  A maximum matching in the
    deficiency-two case has a complement whose suppressed two-branch
    core is either a theta or a loop--link--loop dumbbell; it is an exact
    zero matching for an \(\mathbb F_2^2\)-flow exactly in the theta
    case.  Under simple cyclic four-connectivity, a tight barrier has
    only singleton three-boundary odd components except possibly one
    five-boundary component, and every dumbbell-link edge has a nonroot
    matching chord across its cyclic cut.  A checked smallest
    10-vertex 3-edge-connected control has only dumbbell maxima, showing
    that 3-edge-connectivity alone is insufficient; it is Tait-colourable
    and has a cyclic three-edge cut.  The remaining focused obligation is
    to turn the matching chords into a theta-producing exchange, or find
    a cyclically-four non-Tait countermodel.  See
    `scratch/prescribed-root-matching-deficiency-frontier.md`.
71. **The focused perfect-or-theta alternative holds throughout the
    retained complete corpora at every even order from 10 through 30:**
    two independent exact implementations classify 136,557,951
    independent root pairs in 153,863 cyclically-four non-Tait simple
    cubic graphs.  Exactly 135,214,569 leave a perfectly matchable
    endpoint-deleted graph; the other 1,343,382 have deficiency two and
    every one admits some
    maximum matching whose complement is theta rather than dumbbell.
    There are no all-dumbbell pairs.  All deficient instances have
    \(|\delta(U)|=8\), but this is only a bounded observation.  The human
    exchange audit proves that maximum near-perfect matchings are related
    by even alternating circuits and exposed-vertex rotations.  The
    universal obligation is to show that a complement-bridge-minimizing
    dumbbell state cannot be closed under all such moves.  See
    `search/focused-theta-choice-through28-20260727/`,
    `search/focused-theta-choice-order30-20260727/`, and
    `scratch/focused-theta-choice-census-frontier.md`.
72. **The complete retained order-28 cyclically-four cap class has no
    exceptional deletion pole, raising the scoped lower bound to
    order 30:** Snarkhunter supplies 12,517 documented cyclically
    4-edge-connected non-Tait simple cubic caps.  Their 9,725,709
    independent-edge deletions have 19,451,418 retained positive
    \(D_5\)-labellings: every pole realizes both orbit 0,
    \((01,01,01,01)\), and orbit 2,
    \((01,01,23,23)\).  The first three exceptional exact masks omit
    orbit 2 and the last three omit orbit 0, so the two witnesses
    exclude all six masks.  An independent verifier reconstructs every
    deletion and checks every displayed vertex equation.  Combined with
    the human cyclic-three endpoint-fork bound of 30, the previous
    cyclically-four classifications through 26, and the parity identity
    \(3n-4=2m\) for a terminal-distinct cubic four-pole, this proves the
    stated order-30 lower bound in the vertex-minimal, two-cut-reduced,
    bridge-free, connected, simple, terminal-distinct fixed-five scope.
    It is not a universal full-signature theorem and not Five-CDC.  See
    `search/four-pole-order28-cyclic4-cap-20260727/`.
73. **Boundary-eight local rotation closure does not replace cyclic
    four-edge-connectivity:** the graph
    `Q???C@?GF?CKSOF?AQ?W_B_AA_?` with roots \(\{12,20\}\) is simple,
    cubic, 3-edge-connected, non-Tait, and has matching deficiency two.
    All 40 maximum matchings give dumbbell complements, while their full
    elementary exchange graph is connected with 384 edges.  For the
    canonical barrier \(A=\{6,16\}\), the roots and the unique unused
    \(A\)-edge form a cyclic three-edge cut; this makes that edge a
    complement bridge for every maximum matching.  A direct cut proof,
    two \(K_{2,3}\)-to-Petersen contractions, and a standard-library
    checker independently establish the claims.  Thus a proof from the
    boundary-eight incidence counts, non-Taitness, and exchange
    minimality alone is impossible.  The focused cyclic-four
    singleton-barrier lemma and the one-boundary-five case remain open.
    See `scratch/boundary-eight-rotation-closure-frontier.md`.
74. **The all-singleton Gallai--Edmonds branch cannot contain a standard
    Five-CDC counterexample:** write its partition as
    \(V(G)=D\dot\cup W\), with \(D\) independent and
    \(|W|=|D|+2\).  Cubic degree counting gives
    \(|E(G[W])|=3\).  Schönberger's edge-prescribed matching theorem
    gives a perfect matching through any chosen edge of \(G[W]\); counting
    then shows that it contains exactly one such edge.  The complementary
    2-factor contains the other two, so its cycles contain an odd number
    of same-side edges on zero or exactly two components.  Its oddness is
    therefore at most two, and Huck--Kochol (1995) gives a standard
    five-cycle double cover.  This is a human-checkable universal closure
    of the standard singleton branch.  It neither proves the stronger
    prescribed-root theta statement nor treats the one-boundary-five
    factor-critical branch.  See
    `scratch/root-insertion-two-factor-frontier.md`.
75. **Universal five-pole nonemptiness is already equivalent to the
    standard conjecture, and the 46-state screen now reaches order 15:**
    replace an edge \(uv\) of a finite simple bridgeless cubic graph by a
    six-edge path whose five internal vertices are the terminals of a
    five-pole.  Every proper edge of the new core lies on a circuit.
    Summing a pole \(D_5\)-labelling over the old vertex set forces the
    first and last path-edge labels to agree, so deleting the path and
    restoring \(uv\) gives a Five-CDC of the original graph.  Conversely,
    after normalizing the old edge label to \(01\), the path labels
    \(01,02,03,01,02,01\) and semiedge labels
    \(12,23,13,12,12\) extend the cover.  Thus the universal 46-of-62
    theorem would resolve Five-CDC; it is not merely a five-cut
    reduction.  The bounded threshold census nevertheless has a clean
    extension: all 69,243 canonical internally bridgeless order-15
    five-poles reach 46 states, with zero below-threshold records.
    Structural replay passes, while the universal nonemptiness proof
    remains exactly the unresolved obligation.  See
    `docs/five-pole-realizability-frontier.md` and
    `search/five-pole-46-threshold-order15-20260727/`.
76. **A fixed Jaeger multiplicity fibre has an exact five-support
    criterion:** in a cubic graph let \(T_1,T_2,T_3\) be spanning trees
    with empty common intersection and let \(K_i\) be the unique
    all-vertices-odd forest contained in \(T_i\).  In a vertex-star fibre,
    the canonical five-point lift exists exactly when
    \(K_1\cap K_2\) has even boundary on every component of \(K_3\).
    Equivalently, \(K_1\cap K_2\) is Eulerian after the \(K_3\)-components
    are contracted.  This follows both from the local five-point triangle
    table and from the identity \(F(T)=E-K(T)\) for the fundamental
    completion.  The component criterion has been exhaustively compared
    with the direct pair-labelling CSP on all 30,744 nowhere-zero
    \(\mathbb F_2^3\)-flows on connected simple cubic graphs through order
    eight, with zero mismatches.  See
    `scratch/jaeger-support5-component-criterion.md` and
    `scratch/jaeger-k-forest-star-parity-identities.md`.
77. **Every prescribed Type A or Type B three-tree multiplicity pattern is
    feasible in a 3-edge-connected cubic graph:** if an edge has
    multiplicity \(m_e\in\{0,1,2\}\), put \(d_e=2-m_e\).  The only
    three-unit defect patterns are Type A (three distinct \(d_e=1\)) and
    Type B (one \(d_e=2\), one \(d_e=1\)).  Replacing \(e\) by \(m_e\)
    parallel copies gives, for every \(k\)-part vertex partition with
    \(q\) crossing original edges and crossing defect \(D\),
    \(2q-D\ge3k-3\).  Nash--Williams--Tutte therefore partitions the
    multigraph into three spanning trees.  Fixed-fibre exchange
    connectivity follows independently from Blasiak's graphic-matroid
    toric-ideal theorem.  This is a human reduction; it does not select a
    packing satisfying item 76.  See
    `scratch/jaeger-tree-choice-through14-and-exchange-no-go.md`.
78. **The exact fixed-fibre five-support frontier reaches all simple
    bridgeless cubic graphs through order 14:** all 587 graphs and all
    944,974 Type A/B placements were classified.  Of 804,204 feasible
    fibres, every one has a compatible pair labelling supported on at most
    five Fano points.  A separately written verifier checks graph
    premises, placement completeness, and every retained witness.  This is
    a bounded theorem, not a proof of the universal selection lemma.  See
    `output/jaeger-five-point-fibres-through14/census.jsonl` and
    `scratch/verify_jaeger_five_point_frontier.py`.
79. **The canonical vertex-star five-support frontier has independently
    checked larger hard-snark samples:** all \(705\cdot38=26{,}790\)
    order-38 star fibres and all \(31\cdot44=1{,}364\) star fibres in the
    retained order-44 oddness-four source list admit witnesses supported
    in the fixed set \(\{0,4,5,6,7\}\).  The order-44 verifier independently
    decodes graph6, checks simplicity, cubicity, connectivity and
    bridgelessness, reconstructs all three fundamental completions, and
    checks point parity on every literal witness.  The result is finite and
    source-list oddness is provenance, not recomputed.  See
    `scratch/jaeger-coordinate-five-star-order38-result.json`,
    `output/jaeger-coordinate-five-order44/result.json`, and
    `scratch/verify_jaeger_coordinate_five_order44.py`.
80. **The surviving universal obligation is a joint parity-and-base
    selection lemma:** for every 3-edge-connected cubic graph and a chosen
    vertex star, select a three-tree packing in that fixed fibre so that
    item 76 holds (the fixed canonical coordinate would suffice).
    Choosing an arbitrary third tree and repairing the other two is false,
    and choosing parity-good perfect forests before extending them is also
    false.  Consequently the forest variables and all matroid-union rank
    inequalities must be controlled jointly.  No proof or counterexample
    to this exact existential lemma is presently known.
81. **Defect-monotone reciprocal exchange in one fixed Fano coordinate is
    false:** the
    14-vertex 3-edge-connected cubic graph
    `M?AA@BORDGEOEOAo?`, root zero, has an explicit star-packing state with
    two bad \(K_3\)-components.  Among all 108 candidate reciprocal
    two-tree swaps, 18 preserve the spanning-tree conditions and every one
    raises the defect to four; the other 90 are illegal.  Thus the state is
    a singleton component of its fixed-coordinate defect-two level.  It is
    already good in another Fano plane, with seven-plane profile
    \((2,4,2,2,0,6,2)\), and one reciprocal exchange gives profile
    \((0,2,4,4,2,2,2)\).  Thus the countermodel does not refute descent for
    the symmetric minimum over all seven planes.  See
    `scratch/jaeger-star-parity-descent-countermodel.md` and
    `scratch/verify_jaeger_star_parity_descent_countermodel.py`.
82. **The symmetric Fano-minimum exchange potential satisfies a complete
    bounded descent theorem through order 14:** for every simple
    3-edge-connected cubic graph through 14 vertices, every root
    automorphism orbit, and every state in the corresponding star fibre,
    each positive same-level component for
    \(d_{\min}=\min_{0\ne h\in(\mathbb F_2^3)^*}d_h\) has an exchange edge
    to a lower level.  The exact census covers 419 graphs, 3,567 rooted
    instances, and 529,150,122 states with no failure; the largest
    \(d_{\min}\) is four.  An independent verifier regenerates the complete
    graph stream, 3-edge-connectivity filter, root orbits, row ordering,
    totals, and digest.  It does not independently re-enumerate all states,
    so the C++ enumerator remains inside the trust boundary.  This is a
    finite theorem, not a universal descent proof.  See
    `scratch/jaeger-fano-minimum-parity-descent-through14.md` and
    `output/jaeger-fano-min-descent-through14/census.jsonl`.
83. **Odd kernels are fundamental circuits of one parity element, but a
    natural closure strengthening fails outside vertex-star fibres:**
    adjoining the all-ones column \(p\) to a reduced incidence matrix gives
    \(C(T,p)=K(T)\cup\{p\}\) for every spanning tree \(T\), equivalently
    \(1_{e\in K(T)}=\det A_{T-e+p}\pmod2\).  Requiring
    \(K_1\cap K_2\subseteq\operatorname{cl}(K_3)\) is sufficient for the
    exact component-parity target.  On graph6 ``K?`@E`gFCKEO``, however, each
    of two automorphic non-star Type-A fibres has 355,392 ordered packings,
    none closure-good in any coordinate, while 7,704 satisfy the actual
    parity target.  A standard-library independent checker exhausts all
    packings.  The vertex-star case retains extra structure:
    \(\delta(r)\cup\{p\}\) is a four-element cocycle, and deleting \(r\)
    turns a packing into a partition into three cographic bases with three
    terminal joins.  All 5,646 feasible vertex-star fibres through order
    14, all 1,364 retained order-44 stars, and 2,500 deterministic random
    order-50 stars passed the initial closure test.  Item 84 records the
    later exact vertex-star countermodel, so the proposed sufficient
    theorem is now false.  See
    `scratch/jaeger-parity-element-and-kernel-closure-no-go.md`.
84. **Graphic closure is false even in a 3-connected vertex-star fibre,
    while the exact parity target survives:** graph6
    `O??CA?_ceOGgH_F?AK@P?`, rooted at vertex 13, is simple cubic,
    3-edge-connected, and 3-vertex-connected.  Its star fibre contains
    5,723,136 ordered three-tree packings.  An independent cographic-base
    partition enumeration finds zero packing good for
    \(K_i\cap K_j\subseteq\operatorname{cl}(K_k)\), but 40,464 packings
    good for the exact contracted component-parity condition.  A
    744-variable, 101,037-clause CNF is UNSAT, with an LRAT proof accepted
    by both `lrat-check` and verified CakeML `cake_lpr`; a separate literal
    five-point witness confirms that this is not a Five-CDC obstruction.
    Triangle contraction proves that nonroot triangle expansion preserves
    closure failure, yielding an infinite family of simple cubic
    3-edge-connected countermodels to this strengthening.  The universal
    obligation remains the weaker joint parity-and-base selection lemma in
    item 80.  See
    `scratch/jaeger-star-kernel-closure-countermodel-16v.md` and
    `scratch/jaeger-star-kernel-closure-triangle-expansion.md`.
85. **The surviving exact star-parity target is invariant under nonroot
    triangle expansion and contraction:** exact component parity is
    equivalent to the existence of \(P\subseteq K_k\) for which
    \((K_i\cap K_j)\triangle P\) is Eulerian.  Contracting a triangle
    preserves every external odd-kernel membership and Eulerian parity.
    Conversely, the local lift has 60 admissible odd-kernel traces; vertex
    permutations and swapping \(i,j\) reduce them to seven rows, and every
    row has a legal omitted-edge permutation and a local
    \(P\)-completion.  A standard-library checker verifies all patterns
    and symmetry orbits.  Thus the infinite triangle-expanded
    countermodels in item 84 obstruct only graphic closure, not the exact
    parity lemma.  In a simple 3-edge-connected cubic graph other than
    \(K_4\), every triangle has three distinct external neighbours:
    equality of exactly two gives a 2-edge cut, and equality of all three
    gives \(K_4\).  Thus every triangle of a non-\(K_4\)
    prescribed-root minimal exact obstruction must contain the root.
    Triangle-free joint parity-and-base selection remains open.  See
    `scratch/jaeger-star-exact-parity-triangle-invariance.md`.
85. **The order-16 vertex-star closure countermodel is not a countermodel
    to symmetric Fano-minimum descent:** on graph6
    `O??CA?_ceOGgH_F?AK@P?`, root 13, the exact whole-state descent
    enumerator checks all 953,856 states, reaches maximum
    \(d_{\min}=4\), and finds no trapped positive same-level component.
    An independently written local replay reconstructs one explicit state
    with profile \((4,4,4,4,4,4,4)\), exhausts all 147 candidate
    reciprocal exchanges, and finds 25 legal neighbours: 22 lower
    \(d_{\min}\) to two and three preserve four.  The independent checker
    does not re-enumerate the entire fibre, so the full-state C++ program
    remains in the trust boundary.  This is one targeted order-16 fibre,
    not a complete order-16 descent census and not a universal proof.  See
    `output/jaeger-fano-min-descent-order16-closure-no-go/result.json` and
    `scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py`.
86. **The seven-plane defect has an exact human exchange law:** a
    reciprocal exchange toggles each zero-subgraph by
    \(E_f'=E_f\triangle Z_f\), where \(Z_f\) is the corresponding linear
    combination of the two active fundamental circuits.  For a component
    \(Q\) of \(E_h\), its defect is the parity of any one of the four
    boundary colour classes in \(h^{-1}(1)\); the four parities agree by
    the flow cut equation.  This proves in particular that every \(d_h\)
    is even.  When \(Z_h=\varnothing\), the component vector changes by
    \(\beta_h'=\beta_h+\partial_hR\), hence
    \(d_h'-d_h=|\partial_hR|-2|\partial_hR\cap\beta_h|\).
    The split/merge case has a separate exact determinant/normal formula.
    A literal checker verifies the set and Hamming formulas on all legal
    exchanges at the frozen 14- and 16-vertex states.  The flow-level
    component condition is independently Hušek--Šámal,
    arXiv:2607.24724, Theorem 3.16; the star/tree selection is the open
    obligation here.  See `scratch/jaeger-fano-reciprocal-exchange-law.md`
    and `scratch/verify_jaeger_reciprocal_exchange_defect_formula.py`.
87. **Immediate symmetric descent and fixed-kernel exposure are both
    false, while full same-level descent survives:** on graph6
    `O??CA?_ceOGgH_F?AK@P?`, root 13, an
    explicit state has profile \((4,4,4,2,4,6,4)\).  All 147 candidate
    reciprocal exchanges are replayed: 23 are legal, with minimum-score
    histogram \(\{2:18,4:5\}\), so none lowers \(d_{\min}=2\).  A
    kernel-inert exchange preserves the entire flow and profile but changes
    the ambient tree realizations; one further both-active exchange reaches
    profile \((2,2,2,2,4,6,0)\).  This refutes every one-exchange averaging
    lemma but not descent from a same-level component.  A second state
    with profile \((4,4,4,4,6,2,2)\) has 23 legal neighbours, all still
    at score two, and no kernel-inert neighbour.  Its fixed-kernel
    realization component is a singleton; an active same-level exchange
    followed by a second exchange reaches zero.  This refutes the proposed
    fixed-kernel exposure repair.  The surviving obligation is the full
    same-level-component boundary theorem, allowing active neutral moves.
    See
    `scratch/jaeger-fano-min-immediate-descent-countermodel.md` and its
    independent checker.
88. **Nonroot triangle expansion gives an exact fibre-graph product but
    not defect-score invariance:** contracting the triangle identifies
    the expanded star-fibre exchange graph with
    \(\mathcal X(G,r)\square\operatorname{Cay}(S_3,\text{transpositions})\).
    External swaps project exactly, triangle-only swaps generate the
    \(S_3\) factor, and mixed swaps are illegal because one tree acquires
    the whole triangle.  Nevertheless one contracted profile
    \((2,4,2,2,0,6,2)\) has four zero-defect lifts and two positive
    defect-two lifts, so descent invariance does not follow from the graph
    product.  Exact whole-state checks of all thirteen nonroot triangle
    expansions of the 14-vertex fixed-coordinate graph cover 17,297,280
    states with no trapped positive component.  This is a finite theorem,
    not an inductive reduction.  See
    `scratch/jaeger-triangle-expansion-descent-structure.md` and
    `output/jaeger-fano-min-descent-triangle-expansions-16v/census.jsonl`.
89. **The affine pair-exchange axiom is false even in its exact reduced
    domain:** a 36-vertex simple cubic girth-five,
    cyclically 4-edge-connected non-Tait graph has a bad nowhere-zero
    \(\mathbb F_2^3\)-flow with 33 affine-compatible line occurrences
    (32 distinct edge pairs) and no packing deletion among them.  A
    standard-library checker independently enumerates all 221 perfect
    matchings, all cyclic cuts of size at most three, and every relevant
    binary cycle space; a separate C++/CaDiCaL replay also returns APX
    score zero.  The same graph has an explicit standard five-cover, and
    the same flow has 6,699 good legal circuit switches.  Thus APX and any
    universal \(Q\)-bound forcing inequalities (25)/(26) are closed
    negatively, while the reduced one-switch lemma and FiveCDC remain
    open.  See `scratch/fano-apx-countermodel-order36.md`.
90. **Fixed-state square lifting is false; whole-fibre square reduction is
    still open:** on the planar order-eight graph6 `G?zTb_`, root zero, an
    exact-good state of profile \((2,2,0)\) and one independent smoothing
    pair have 72 legal local lifts among all \(3^8\) gadget words, but none
    is good in any coordinate.  Another good state for the same
    graph/root/pair does lift, so the no-go concerns the order of
    quantifiers and not existence in the fibre.  Both order-six graphs pass
    the stronger statewise property.  A complete census of all four simple
    3-edge-connected cubic order-eight graphs, all roots, and all eligible
    smoothing pairs finds no failure of the whole-fibre implication in 672
    instances.  A square induction must therefore select the downstairs
    state and lift jointly.  See
    `scratch/jaeger-star-square-any-coordinate-lift-no-go.md`.
91. **Simultaneous nonroot triangle expansion has an exact exchange-graph
    product, but not a product defect:** expanding a set \(S\) of original
    nonroot vertices gives
    \(\mathcal X(G^S,r)\cong\mathcal X(G,r)\square
    \operatorname{Cay}(S_3,\mathcal T)^{\square|S|}\), even when expanded
    vertices are adjacent. External swaps project, same-triangle swaps are
    transpositions, and every mixed or different-triangle swap completes a
    triangle in one changed tree. The defect varies between sheets, so the
    product does not prove descent. Exhaustive one- and two-triangle lifts
    of two adversarial order-16 states find no strict trap, and broad
    plateau sampling also escapes, but these are finite or exploratory
    evidence only. The full same-level-component boundary theorem remains
    open. See
    `scratch/jaeger-simultaneous-triangle-lift-plateau-search.md`.

92. **Whole-fibre square selection:** prove that whenever a downstairs
    star fibre has an exact-good state, every eligible square smoothing has
    some (pair-dependent) good state with a good local lift.  A fixed
    outside five-cover extends exactly when the deleted labels are equal or
    disjoint.  Complete censuses have zero failures through downstairs
    order 16, including independently replayed 572,880- and
    7,737,408-witness layers at orders 14 and 16.  All three order-18
    snarks also pass all 12,474 labelled instances.  Thus any simple
    3-edge-connected cubic countermodel to the stronger local-selection
    statement has order at least 18.  The fixed-label
    shortcut is false: on a three-edge cut all three pair labels intersect
    pairwise once, and the triangular prism has the tree-local antecedent
    and conclusion while no FiveCDC makes the selected pair equal or
    disjoint.
    Status: **OPEN / exact finite frontier**.

93. **Full plateau-component boundary:** prove that every positive
    same-\(d_{\min}\) exchange component has an edge to a lower level.
    Immediate scalar descent, fixed-kernel exposure, and immediate
    lexicographic descent of the sorted seven-defect profile are all false.
    The order-36 sorted-profile local minimum escapes in two same-level
    moves.  A stronger order-40 separator has exact plateau escape distance
    four: its complete radius-three ball has 958 states and no earlier
    descending boundary.  It too escapes.  Furthermore, two adjacent
    equal-profile states have total-defect Laplacians \(10\) and \(-14\),
    refuting profile-only averaging and universal sub/superharmonicity.
    Neither witness is a trapped component.
    Status: **OPEN / one-step and radius-three strengthenings refuted**.

94. **Minimal-counterexample substitution reduction:** characterize
    non-covering multipoles whose boundary relation is universally
    FiveCDC-extendable.  Ordinary graph covers and the adjacent-vertex
    Petersen four-pole substitution are now soundly positive and cannot
    generate a smallest counterexample from a positive base.
    Status: **OPEN beyond the proved operations**.

95. **Exploit full-boundary four-poles globally:** both the
    cube-minus-adjacent-vertices and Heawood-minus-adjacent-vertices poles
    realize all 640 xor-zero \(D_5\) boundary words and therefore give
    arbitrary-port FiveCDC/bridgelessness-preserving insertions.  The cube
    pole is minimum-order in the connected simple terminal-distinct cubic
    class; the Heawood pole has a girth-six core.  Prove that every minimal
    counterexample contains a reducible full-boundary pole, or find a
    finite unavoidable family of such poles.  Neither known configuration
    is proved unavoidable.
    Status: **OPEN / exact local theorem available**.
