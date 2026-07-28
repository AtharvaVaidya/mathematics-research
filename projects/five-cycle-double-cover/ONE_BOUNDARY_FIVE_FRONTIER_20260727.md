# One-boundary-five FiveCDC frontier

Date: **2026-07-27**

Status: **AI-assisted research draft. The standard Five-Cycle Double
Cover Conjecture remains unresolved. No counterexample is claimed. The
orientable variant is not analyzed here.**

This index freezes the current surviving branch of the prescribed-root
matching analysis. The all-singleton Gallai--Edmonds branch is already
closed for the standard FiveCDC conclusion by the oddness-at-most-two
argument in `docs/root-insertion-two-factor-frontier.md`. What remains is
the branch with one nontrivial factor-critical component having five
boundary edges.

## Human-checkable statements

`docs/one-boundary-five-oddness-frontier.md` displays proofs of the
following statements under its precise finite, simple, bridgeless cubic
and cyclically-four hypotheses:

1. the nontrivial factor-critical component has no bridge, so its five
   boundary edges have five distinct endpoints;
2. every proper circuit-containing shore inside that component has
   completed boundary at least four;
3. a perfect matching containing a prescribed root uses exactly one root
   and exactly one edge of the five-edge boundary;
4. at least two distinct boundary terminals are attainable, by the
   perfect-matching polytope;
5. if an attainable exposed terminal has a near-perfect matching leaving
   at most two internal odd circuits, then the completed cubic graph has
   oddness at most four and hence a standard FiveCDC by the cited
   small-oddness theorem; and
6. it is enough that at most one boundary terminal fail that sufficient
   condition.

`docs/one-boundary-five-completion-frontier.md` gives a solver-free proof
that the parameter value \(s=0\) is impossible in the cyclically-four
branch: the singleton outside vertex and one root edge form a triangle
whose boundary has size three.

These arguments are printed for line-by-line human checking. The final
FiveCDC implication in item 5 invokes the cited published
Huck--Kochol small-oddness theorem; this archive does not reprove that
external theorem.

## Exact limits of those reductions

The retained explicit examples show why the remaining step cannot be
replaced by a purely local odd-circuit count.

- The 9-vertex pole `H?b@bQS` has a unique relevant near-perfect matching
  whose complement contains a triangle, refuting the proposed coforest
  shortcut under factor-criticality alone.
- The displayed 15-vertex pole has two relevant near-perfect matchings,
  both leaving two odd internal circuits. This makes the threshold two
  in the conditional reduction sharp outside the cyclically-four domain.
- A 67-vertex locally cyclically-four factor-critical five-pole has all
  five terminals bad even at threshold two: every relevant near-perfect
  matching leaves at least four internal odd circuits.
- That 67-vertex pole occurs in explicit simple cubic, bridgeless,
  cyclically-four, non-Tait completions at \(s=1\) and \(s=2\). Both
  displayed completions have exact oddness four. Therefore they are not
  FiveCDC counterexamples; rather, they show that global closure of the
  two complementary paths must be used.

Before the order-100 specimen below, the unresolved obligation could
still have been met by proving oddness at most four throughout the branch.
That route is now closed.  The surviving universal obligation is to use
the outside pairing/closure structure to obtain a prescribed-root theta,
an exact-zero flow, a standard five-CDC directly, or some other mechanism
which does not rely on a universal oddness-at-most-four bound.

## Oddness-six strategy counterexample

The compact package
`search/one-boundary-five-oddness6-completion-20260727/` gives a
100-vertex simple cubic cyclically four-edge-connected completion with
the exact one-boundary-five Gallai--Edmonds profile and exact oddness six.
Its displayed resistance-transfer argument derives the lower bound from
a source-resistance CNF whose LRAT is accepted by both `lrat-check` and
CakeML `cake_lpr`; an explicit perfect matching supplies the upper bound.

This closes one question and sharpens the remaining obligation: the whole
branch cannot be disposed of by proving oddness at most four.  It does not
produce a FiveCDC counterexample.  The same package retains a SAT model
and a compact edge labelling for an explicit standard five-cycle double
cover, checked independently in the original and edge-label semantics.

## Theta-cap switching exclusion

The displayed argument in
`docs/theta-cap-five-cycle-extension-lemma.md` closes one exact incidence
subcase.  The ordered seven-vertex theta cap has 6,000 \(D_5\) boundary
words, comprising 58 of the 62 global-coordinate orbits.  For each missing
orbit there is a coordinate pair whose bichromatic subgraph has four
boundary ends; whichever of the three path pairings occurs inside the
opposite five-pole, switching either path reaches the theta relation.

For a minimum-order bridgeless cubic counterexample, the
terminal-distinct \(s=1\) outside is forced to be this theta cap.  Capping
the factor-critical shore by an ordered 5-cycle gives a smaller simple
bridgeless cubic graph, hence a nonempty shore relation by minimality.
The switching lemma makes that relation meet the theta relation, and exact
boundary-label gluing gives a FiveCDC, a contradiction.

This theta lemma alone does not close the repeated-endpoint \(s=1\)
shapes, whose outside cap is not theta, or any \(s\ge2\) pattern.
Primary and independently written parity-CSP programs reproduce its
complete finite table.  The underlying
two-subset/multipole/switching language is prior work, and novelty of the
specific cap lemma remains provisional pending specialist review.

## Switching-core exclusion through \(s=2\)

The subsequent displayed proof in
`docs/one-boundary-five-D5-s12-reduction.md` closes all remaining
\(s=1\) patterns and every \(s=2\) outside.  For a candidate avoidance
set, repeatedly delete any boundary orbit which cannot satisfy the
mandatory bichromatic switches and one complete path-pairing alternative.
Every graph-realizable relation survives every deletion round, so it is
contained in the greatest remaining core.

The exact incidence generator retains all 6 \(s=1\) and 128 \(s=2\)
patterns allowed by the inherited Gallai--Edmonds, bridgelessness,
cyclic-four, and root-attainability conditions.  For every
terminal-distinct pattern, the complement of the outside relation has
empty core.  For every repeated-endpoint pattern, its 25-orbit core is
exactly the set in which the two repeated labels are equal or disjoint.
A smaller three-vertex path cap forces those two labels instead to be
distinct and intersecting, so the factor-critical-shore relation cannot
be contained in that core.

The primary finite-domain solver and independently implemented local-row
join reproduce the same relation/core profiles and local identity.  They
share the exact structural pattern generator; this is recorded as a
trust boundary rather than described as full implementation
independence.  The smaller 5-cycle and path caps are proved simple,
cubic, bridgeless, and smaller in the full bridgeless cubic minimality
domain.  Together with the earlier \(s=0\) triangle-cut proof, the branch
is reduced to \(s\ge3\).  FiveCDC remains open.

## Reproducible artifacts and trust boundaries

The focused standard-library replays are:

- `scratch/audit_factor_critical_ear_forest.py`;
- `scratch/check_cyclic4_threshold_two_core.py`;
- `scratch/check_cyclic4_all_bad_threshold_three_core.py`;
- `scratch/check_one_boundary_five_completion_frontier.py`;
- `scratch/check_s1_theta_q67_completions.py`;
- `scratch/enumerate_one_boundary_five_outside.py`; and
- `scratch/check_s2_q67_completion_classes.py`.

The corresponding retained JSON records are checksum-frozen. The
120-bijection \(s=1\) replay and the selected \(s=2\) replay enumerate
perfect matchings directly. Nauty `labelg` is used only for the reported
isomorphism-class counts; it is not needed for the displayed graph,
small-cut, or oddness conclusions.

The C++ source
`scratch/factor-critical-five-pole-oddness-census.cpp` and retained
`scratch/factor-critical-five-pole-oddness-order17.json` record the
bounded order-17 pole census. The full input stream is not included in
this compact update, so the JSON is a provenance record rather than a
standalone replay of canonical generation. It is finite evidence only.

Run the focused integrity and semantic replay commands in
`REPRODUCING.md`. `ONE_BOUNDARY_FIVE_SHA256SUMS` freezes every file in
the earlier update, including the nested oddness-six package manifest.
`THETA_CAP_SWITCHING_SHA256SUMS` separately freezes the theta-cap proof,
both implementations, and both retained results.
`S12_D5_REDUCTION_SHA256SUMS` freezes the \(s\le2\) proof and its nested
six-file computation checksum package.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, developed or revised the
arguments, programs, computations, audits, and prose in this update.
Agent-to-agent checks are not independent human verification or peer
review. The universal claims above are accompanied by displayed proofs,
and computational claims are labelled separately with their replay and
trust boundaries. Independent specialist review is required before
submission or citation as new mathematics.
