# FiveCDC pulls back through graph coverings

Date: 2026-07-28

Status: human-checkable reduction; **not** a resolution of FiveCDC.

## Conventions

Use the incidence or dart definition of an undirected finite multigraph.  A
graph covering \(p:\widetilde G\to G\) consists of maps on vertices, edges,
and incidences such that, for each \(\widetilde v\in V(\widetilde G)\), the
incidences at \(\widetilde v\) map bijectively to the incidences at
\(p(\widetilde v)\).  This convention counts a loop twice at its incident
vertex.  It therefore covers simple graphs, parallel edges, and loops without
an implicit change of degree convention.

An Eulerian edge-subset is an edge-subset whose degree at every vertex is
even, again counting incidences.  A five-cycle double cover in the standard
Eulerian-subgraph formulation is a tuple
\((C_1,\ldots,C_5)\) of Eulerian edge-subsets such that every edge belongs to
exactly two \(C_i\).  Empty coordinates are allowed.

## Pullback theorem

**Theorem.**  If \(p:\widetilde G\to G\) is a finite graph covering and \(G\)
has a standard five-cycle double cover, then \(\widetilde G\) has a standard
five-cycle double cover.

**Proof.**  Let \((C_1,\ldots,C_5)\) be a five-cycle double cover of \(G\).
For each coordinate put
\[
   \widetilde C_i=p_E^{-1}(C_i).
\]
Fix a vertex \(\widetilde v\).  The covering bijection from the incidences at
\(\widetilde v\) to the incidences at \(p(\widetilde v)\) restricts to a
bijection between incidences belonging to \(\widetilde C_i\) and incidences
belonging to \(C_i\).  Hence
\[
 \deg_{\widetilde C_i}(\widetilde v)
   =\deg_{C_i}(p(\widetilde v)),
\]
which is even.  Thus every \(\widetilde C_i\) is Eulerian.

Now fix \(\widetilde e\in E(\widetilde G)\).  By definition,
\(\widetilde e\in\widetilde C_i\) exactly when
\(p_E(\widetilde e)\in C_i\).  The latter holds for exactly two indices
\(i\), because the edge \(p_E(\widetilde e)\) is double-covered downstairs.
Therefore every lifted edge belongs to exactly two of the five pulled-back
Eulerian subsets.  \(\square\)

The same argument proves pullback preservation for \(k\)-cycle double covers
for every fixed \(k\).

## Consequence for counterexample searches

If a bridgeless graph \(\widetilde G\) covers a smaller bridgeless graph \(G\)
known to have FiveCDC, then \(\widetilde G\) is not a counterexample.  Thus a
smallest counterexample, if one exists, cannot be a nontrivial cover of such a
quotient.

The word “bridgeless” on the quotient is important only when one wants to
invoke the conjecture for \(G\).  The pullback theorem itself has no
bridgelessness hypothesis: it starts from an actual cover downstairs.

## Exact computational audit

The direct portfolio began with all 7,654 retained canonical strong snarks of
order 40.  Each had an independently replayed standard FiveCDC witness.  One
deterministic connected 2-lift of every graph, and then one connected 2-lift
of every resulting order-80 graph, was generated.  Direct SAT happened to
find FiveCDC witnesses on all 7,654 graphs in each lifted layer, but those SAT
runs are logically unnecessary once the pullback theorem and the base
witnesses are known.

The independent checker
`scratch/verify_direct_fivecdc_lift_portfolio_20260728.py` reconstructs every
voltage lift and separately forms the literal pulled-back edge labels from the
base witness.  It checks exact weight two on every lifted edge and all five
parities at every lifted vertex.  This is a finite audit of the
implementation, not the proof of the theorem.

No UNSAT FiveCDC instance was found in this portfolio.

## Novelty caution

This pullback observation is elementary covering-space functoriality.  No
claim of literature novelty is made without a dedicated specialist search.
Its value here is as a sound pruning rule and as an explanation of why
ordinary covering/lift families cannot create counterexamples from positive
base graphs.
