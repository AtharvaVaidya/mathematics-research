# Human review guide

The manuscript is intentionally split between ordinary proofs, small
certificates, and large finite computations.

## Claims that should be checked as ordinary mathematics

1. The cover-flow proposition: \(D_5\)-flows are equivalent to five Eulerian edge-subsets
   covering every edge twice.
2. The local-triangle lemma: the three labels at a cubic vertex form a coordinate triangle.
3. The context-free compression delimiter: verify that the twelve supplied
   local triangles span \(Z_1(K_6;\mathbb F_2)\), that triangle sums force
   a coboundary, and that weight-two output would give the impossible
   homomorphism \(K_6\to R_5\).
4. The surface theorem and its converse: the normalized coloured-surface construction
   and its converse.
5. The boundary proposition: \(Y_{ij}\) is the boundary of a regular neighbourhood of
   the primal \(ij\)-subgraph.
6. The Euler-change theorem. In particular, check that pure
   circuit components cancel and that each alternating matching circuit
   contributes two cycles to the product permutation.
7. The four-coordinate one-step lock. Orbit closure in the certified trap
   proposition is a separate finite claim.
8. The cubic \(D_4\) trap theorem. Check the complementary-pair Tait quotient
   and both root-label cases; the orbit-wide circuit hypothesis is essential.
9. The prescribed Tait-factor formula and its insertion corollary.  Check
   separately the \(23,24,34\) and \(0a,0b,ab\) vertex cases, the common-
   circuit lemma for two distinct roots, and the endpoint defects after
   insertion.  Treat existence as known via Hoffmann-Ostenhof's stronger
   4-CDC lemma; review only the explicit adaptation presented here.
10. The two-root insertion equivalence, in both directions.  At each new
   endpoint verify that the open-arc transposition makes the two surviving
   labels equal after deletion of the central edge.
11. The fixed-five minimum-counterexample reductions, especially suppression
   of degree-two vertices and coordinate matching across 2- and 3-edge cuts.
12. The strengthened elimination lemma: cyclically 4-edge-connected
    girth-at-least-five parent implies a simple 3-edge-connected reduced
    graph.

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
sh scratch/d5-tait-prescribed-circuit-lift-20260731/run_all.sh
sh scratch/d5-tait-prescribed-circuit-lift-blind-audit-20260731/run_all.sh
python3 scratch/verify_d5_surface_chi_plateaus_order12.py
python3 scratch/verify_d5_root_euler_potential_reports.py
python3 scratch/verify_d5_root_kempe_order14_report.py
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_root_component_distance_order16_summary.py
python3 scratch/verify_d5_root_feasibility_lift13_girth10.py
```

The order-14 report now covers all terminal equal-\(\chi\) plateaus, not
only the global maximum.  Its focused verifier checks the frozen graph order,
report digest, per-row failure fields, and summary arithmetic; it is not a
second full enumeration.  The order-16 result is a separate unrestricted
root-rescue census and contains no girth-eight graph.  The lift-13 checker
does independently reconstruct and semantically verify all 195 positive
high-girth witnesses.

## Publication checks still required

- Obtain independent expert review.
- Run a broader literature search for the exact coloured-surface dictionary
  and Euler-change formula.
- Archive source, reports, and exact tool versions at an immutable commit or
  DOI.
- Replace the placeholder author line only after the responsible humans have
  verified and accepted the work.
- Check the target venue's AI-use and computer-assisted-proof policies.
