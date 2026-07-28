# Human review gate

This is an AI-assisted research draft, not a submission-ready proof of
FiveCDC. Before public circulation, a graph theorist should independently
check at least the following.

1. Verify the pair-labelling/component-parity theorem in Section 4 directly,
   including the affine-plane conventions and the leaf-bit formula.
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
8. Verify the triangle-contraction theorem by hand, including preservation of
   external odd-kernel membership and 3-edge-connectivity. Check that its
   contrapositive yields an infinite family only for the discarded closure
   strengthening.
9. Audit the symmetric Fano-minimum score in the C++ whole-state enumerator.
   Its Python verifier independently checks graph/root coverage and hashes,
   but does not re-enumerate the 529,150,122 states.
10. Audit the 34-vertex CNF generator, then replay both LRAT checkers from
   pinned source revisions.
11. Treat the order-14 and order-38 positive censuses as rerunnable
   computations, not archived witness-by-witness proofs. The order-44 result
   does retain and independently replay every literal witness.
12. Conduct a specialist prior-art search for the exact five-point
    component-parity criterion, odd-kernel/parity-element formulation,
    cographic-base correspondence, symmetric potential, and fixed-fibre
    feasibility observation. The current manuscript makes no categorical
    novelty or priority claim.
13. Decide whether Atharva Vaidya should be the sole named author and whether
   any additional human contributors meet the journal's authorship policy.
   AI systems must not be listed as authors, but their role must remain
   disclosed.

The most important negative check is conceptual: none of the finite positive
results supplies the missing universal selection lemma.
