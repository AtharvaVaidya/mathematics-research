# Human review guide

The manuscript is intentionally split between ordinary proofs, small
certificates, and large finite computations.

## Claims that should be checked as ordinary mathematics

1. The cover-flow proposition: \(D_5\)-flows are equivalent to five Eulerian edge-subsets
   covering every edge twice.
2. The local-triangle lemma: the three labels at a cubic vertex form a coordinate triangle.
3. The surface theorem and its converse: the normalized coloured-surface construction
   and its converse.
4. The boundary proposition: \(Y_{ij}\) is the boundary of a regular neighbourhood of
   the primal \(ij\)-subgraph.
5. The Euler-change theorem. In particular, check that pure
   circuit components cancel and that each alternating matching circuit
   contributes two cycles to the product permutation.
6. The four-coordinate one-step lock. Orbit closure in the certified trap
   proposition is a separate finite claim.
7. The cubic \(D_4\) trap theorem. Check the complementary-pair Tait quotient
   and both root-label cases; the orbit-wide circuit hypothesis is essential.
8. The first-foreign splice identity and its transition-pairing consequence.
   Check separately that it proves distance nonincrease, not immediate rescue.

## Small certificates

- Recompute the cube labels in equation (8), verify the \(Y_{12}\)-component,
  and count the coordinate circuits before and after the switch.
- Decode the graph6 row in the certified trap proposition, contract the specified edge, and
  verify the displayed state and side xor.
- Check the twelve rows and normalized adjacency in
  `orbit-certificate.txt`.

## Computational claims

Run:

```sh
python3 scratch/audit_d5_surface_euler_switch.py
python3 scratch/check_d5_contraction_circuit_orbit_counterexample.py
python3 scratch/check_d4_cubic_trap_root_universality.py
python3 scratch/verify_d5_surface_chi_plateaus_order12.py
python3 scratch/verify_d5_root_euler_potential_reports.py
python3 scratch/verify_d5_root_kempe_order14_report.py
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_terminal_foreign_block_order14.py
python3 scratch/verify_d5_cyclic_block_lex_reports.py
python3 scratch/check_d5_cyclic_block_one_step_no_go_order14.py
python3 scratch/check_d5_no_fresh_coordinate_blocker_order12.py
```

The terminal-plateau chain census is complete through order 14.  The two
block-potential implementations use different root accounting conventions,
so their subplateau totals should not be conflated.  Both are finite
censuses, not proofs for arbitrary graphs.  The two final witness checkers
also prevent the first-foreign and fresh-coordinate lemmas from being
overstated as universal one-step descent rules.

## Publication checks still required

- Obtain independent expert review.
- Run a broader literature search for the exact coloured-surface dictionary
  and Euler-change formula.
- Archive source, reports, and exact tool versions at an immutable commit or
  DOI.
- Replace the placeholder author line only after the responsible humans have
  verified and accepted the work.
- Check the target venue's AI-use and computer-assisted-proof policies.
