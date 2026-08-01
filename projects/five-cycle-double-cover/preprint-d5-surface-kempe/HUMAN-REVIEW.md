# Human review guide

The manuscript is intentionally split between ordinary proofs, small
certificates, and large finite computations.

## Claims that should be checked as ordinary mathematics

1. The cover-flow proposition: \(D_5\)-flows are equivalent to five Eulerian edge-subsets
   covering every edge twice.
2. The local-triangle lemma: the three labels at a cubic vertex form a coordinate triangle.
3. The triangle-state compression delimiter: check state transport along
   every connected state-adjacency graph, the rank-ten cycle-space step,
   and the resulting impossible homomorphism \(K_6\to R_5\).  Check the
   order-10 exclusion separately: even positive pair incidence makes all
   fifteen pairs occur twice, so the xor of ten proposed independent rows
   vanishes.
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
13. The linear rooted-transition theorem: the active-edge transition graph
    has exactly the factor circuits as components, and a selected transition
    set has boundary \(\{r,s\}\) exactly when the roots share one component.
    Recheck the absence of a separate at-most-one transition constraint and
    the \(8m\)-variable, \(133m/3\)-clause count.
14. The typed-port gluing lemma: normalize both ordered connector triangles,
    treat the unique internal factor and the two external factors separately,
    and verify that deleting the caps joins the two rooted factor paths.
    Then check the double-star intersection corollary.
15. The finite rooted-certificate proof boundary: the Tait case is analytic;
    the non-Tait case through order 28 depends on the documented complete Snarkhunter streams
    and on the literal positive-flow checker, not on accepting SAT answers.
    Check separately that Brinkmann--Goedgebeur--Hagglund--Markstrom,
    Observation 6.6, strictly subsumes the existential cutoff; no novelty is
    claimed for the order-28 theorem.
16. The relevant-cap theorem: recheck all three restored-cut cases, cap
    3-edge-connectivity and bridgelessness, the marked-girth lift, and the
    (W_1,\ldots,W_4) count yielding (n^2\ge46n-147).  Then check the
    Alon--Hoory--Linial application to \(K-r\), including the exact threshold
    and parity step, and the external-mode Tait-cap argument separately.
17. The adjacent-port lemma: after normalizing the cap labels to
    `01,02,12`, check the six possible root labels and the displayed
    external-factor choices.  Verify that adjacency, not merely simultaneous
    activity, places the root and port in the same factor component.

## Small certificates

- Recompute the cube labels in equation (8), verify the \(Y_{12}\)-component,
  and count the coordinate circuits before and after the switch.
- Decode the graph6 row in the certified trap proposition, contract the specified edge, and
  verify the displayed state and side xor.
- Check the twelve rows and normalized adjacency in
  `orbit-certificate.txt`.
- Decode graph6 ``KQh?k`CGGQ?R``, reconstruct the eighteen labelled edges of
  the triangle-state witness, verify that all state-adjacency graphs are
  connected, and confirm the two different local colour profiles at the
  repeated state `012`.

## Computational claims

Run:

```sh
python3 scratch/audit_d5_surface_euler_switch.py
(cd scratch/eight-to-five-triangle-state-rigidity-20260731 && ./run_all.sh)
python3 scratch/check_d5_contraction_circuit_orbit_counterexample.py
python3 scratch/check_d4_cubic_trap_root_universality.py
sh scratch/d5-tait-prescribed-circuit-lift-20260731/run_all.sh
sh scratch/d5-tait-prescribed-circuit-lift-blind-audit-20260731/run_all.sh
(cd scratch/d5-root-transition-sat-20260731 && ./run_all.sh)
(cd scratch/d5-typed-cap-double-star-frontier-20260731 && ./run_all.sh)
(cd scratch/d5-root-pair-census-20260731 && ./run_all.sh)
(cd scratch/d5-relevant-cap-order56-cutoff-20260731 && ./run_all.sh)
(cd scratch/petersen-foster-full-typed-cap-signature-20260731 && ./run_all.sh)
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
high-girth witnesses.  The triangle-state package contains two
independently structured exact checkers.  The typed-cap package recomputes
all flows and interfaces independently only through order 10; the complete
order-12 and order-14 census presently has one C++ implementation plus
deterministic reproduction.  The rooted-frontier package contains 30,858
literal positive flows; its checker is solver-independent and exhausts all
10,689,351 independent root pairs on the 14,009 non-Tait rows through order
28.  The order-56 package replays the cut/walk arithmetic and the exact
irregular-Moore threshold.  The
Petersen--Foster checker validates six literal 1,335-edge flows and all six
typed component claims on one interface.

## Publication checks still required

- Obtain independent expert review.
- Run a broader literature search for the exact coloured-surface dictionary
  and Euler-change formula, the triangle-state transport criterion, rooted
  transition systems, and typed multipole/cap signatures.
- Obtain a second full implementation of the typed-cap order-14 frontier.
- Archive source, reports, and exact tool versions at an immutable commit or
  DOI.
- Replace the placeholder author line only after the responsible humans have
  verified and accepted the work.
- Check the target venue's AI-use and computer-assisted-proof policies.

The universal double-star premise and terminal-plateau conjecture remain
open.  No finite table in the manuscript resolves FiveCDC.
