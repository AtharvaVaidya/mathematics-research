# Linear rooted-factor SAT encoding

This package implements an exact SAT encoding for the following question.

Given a loopless cubic graph H and two distinct independent root edges r,s,
is there a labeling of every edge by a two-subset of {0,1,2,3,4} such that
the three labels incident with each vertex have zero symmetric difference
and r,s belong to one circuit of

    Y_01 = {e : exactly one of 0,1 belongs to the label of e}?

This is the rooted D5-flow feasibility premise left by the edge-elimination
route in the accompanying preprint.  It is not by itself equivalent to the
Five-Cycle Double Cover Conjecture.

The new point is a linear-size connectivity certificate.  It uses one
variable for each possible local transition between two incident edges.
The selected transitions have boundary {r,s} in the transition graph.
This is equivalent to r and s lying in one Y_01 circuit and avoids the
quadratic layered-reachability encoding used by the earlier search script.

Files:

- HUMAN-PROOF.md: a human-checkable equivalence proof.
- search.py: standard-library generator, solver driver, and model checker.
- run_all.sh: deterministic regression commands.

Timing is omitted by default so the JSON regressions are byte-stable.
Pass `--include-timing` for exploratory performance runs.

CaDiCaL is used only as the SAT engine.  Every SAT model is checked from the
graph semantics.  An UNSAT row is deliberately reported as
UNSAT_UNCERTIFIED unless a proof path is supplied; a conjecture-level
counterexample would additionally require an independently checked proof.

AI-use disclosure: the formulation, implementation, and exposition were
developed in an AI-assisted research process.  All claims are intended to
stand on the explicit proof and replayable computations, not on the identity
of the author or the software that suggested them.
