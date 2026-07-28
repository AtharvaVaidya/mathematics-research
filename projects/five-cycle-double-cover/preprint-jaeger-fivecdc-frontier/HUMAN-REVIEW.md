# Human review gate

This is an AI-assisted research draft, not a submission-ready proof of
FiveCDC. Before public circulation, a graph theorist should independently
check at least the following.

1. Verify the pair-labelling/component-parity theorem in Section 4 directly,
   including the affine-plane conventions and the leaf-bit formula. Compare
   the coordinate translation with Hušek--Šámal, arXiv:2607.24724v1,
   Theorem 3.16 and Conjecture 3.19. The manuscript claims no priority for
   this criterion.
2. Verify the prescribed-fibre feasibility proof against the exact
   Nash-Williams--Tutte hypotheses for multigraphs.
3. Verify that the use of Blasiak's toric-ideal theorem really gives
   connectivity of every unordered three-base fibre by single-element
   symmetric exchanges.
4. Check every row of the cube and Moebius-ladder no-go certificates without
   relying on the search programs.
5. Check the parity-element fundamental-circuit proof and both directions of
   the root-deletion/cographic-base correspondence. In particular, verify
   exactly where the vertex-star cocycle is used.
6. Audit the standard-library 12-vertex kernel-closure enumeration, including
   the forced-third-tree formula and the distinction between closure and
   quotient parity.
7. Audit the 16-vertex star-kernel-closure CNF semantics, replay both LRAT
   checkers, and independently check the positive five-point witness in the
   same fibre. Do not confuse this no-go for a stronger lemma with a FiveCDC
   counterexample.
8. Verify the closure triangle-contraction theorem by hand, including
   preservation of
   external odd-kernel membership and 3-edge-connectivity. Check that its
   contrapositive yields an infinite family only for the discarded closure
   strengthening.
9. Verify the separate exact triangle-invariance theorem by hand: the
   Eulerian-completion lemma, descent by contraction, equations
   (6.18)--(6.20), every row of the seven-orbit table, and the
   simple-3-edge-connected caveat. The checker is a backstop, not the proof.
10. Verify the square-local lifting no-go directly: the two displayed
    downstairs states, the eight gadget ports, completeness of the
    \(3^8\) omitted-owner enumeration, all 72 legal lifts, and the alternate
    state's successful lift. Audit the order-six statewise controls and the
    complete 672-instance order-eight whole-fibre census. Check the
    equal-or-disjoint fixed-cover extension lemma by hand, then replay the
    order-10 and order-12 whole-fibre censuses (6,300 and 53,352 instances)
    and the independently checked 572,880-row order-14 witness corpus.
    Preserve the distinction between failure for one selected state, a
    fixed outside five-labelling, and the still-open whole-fibre implication.
11. Audit the symmetric Fano-minimum score in the C++ whole-state enumerator.
   Its Python verifier independently checks graph/root coverage and hashes,
   but does not re-enumerate the 529,150,122 states. Separately verify the
   all-seven exchange identities (8.3)--(8.5), both complete 147-swap
   neighbourhoods used to refute immediate descent and fixed-kernel
   exposure, the order-36 sorted-profile neighbourhood, and the distinction
   between inactive and active same-level moves. Verify the two-exchange
   escape before concluding that the full plateau statement survives.
   Verify the four-case proof of the simultaneous-triangle Cartesian
   product, especially swaps involving two different triangle gadgets; do
   not infer that the defect is a product potential.
12. Audit the 34-vertex CNF generator, then replay both LRAT checkers from
   pinned source revisions.
13. Treat the order-14 and order-38 positive censuses as rerunnable
   computations, not archived witness-by-witness proofs. The order-44 result
   does retain and independently replay every literal witness.
14. Continue the specialist prior-art search for the
   odd-kernel/parity-element formulation, exact triangle invariance,
   cographic-base correspondence, symmetric potential, and fixed-fibre
   feasibility observation. Hušek--Šámal already settle the priority
   boundary for the flow-level component criterion; no remaining item is
   presented with a categorical novelty claim.
15. Decide whether Atharva Vaidya should be the sole named author and whether
   any additional human contributors meet the journal's authorship policy.
   AI systems must not be listed as authors, but their role must remain
   disclosed.

The most important negative check is conceptual: none of the finite positive
results supplies the missing universal selection lemma.
