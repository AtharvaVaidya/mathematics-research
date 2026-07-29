# Proposition-5 neutralization dynamics

Date: 2026-07-29

Status: **EXACT FAILED-APPROACH CERTIFICATE / NOT A FIVECDC
RESOLUTION**.

This package closes a tempting iteration argument in the
minimum-projection program.

For the first order-fourteen abstract clean-or-delete counterstate:

- its 40 reduced integrable component-map states form one strongly
  connected directed graph under legal Proposition-5 obstruction
  neutralizations;
- there are 320 switch certificates and 136 distinct directed state
  pairs;
- the shortest directed cycle has length four and is written out in
  `HUMAN-PROOF.md`;
- consequently no nonconstant potential can be weakly monotone on all
  neutralizing moves, and no potential can strictly decrease at every
  move;
- in the displayed 18-vertex realization, all 40 states and all four
  relative circuit translations violate a minimum-projection exchange
  inequality, so the obstruction cycle does not occur at a genuine
  minimum there.

The correct conclusion is not that the global-minimum proof route
fails.  It is that Proposition 5 alone has cyclic dynamics and any
termination theorem must use global-minimum information essentially.

## Reproduction

Run:

```sh
python3 analyze_dynamics.py
python3 independent_audit.py
```

The primary checker uses the five-parameter normal form and Tarjan's
strong-component algorithm.  The independent checker enumerates
literal normalized component maps, computes four-colour cut parities
directly, and tests reachability from every state.  Both also enumerate
the 1,024 binary cycles of the fixed graph to audit all 160 exchange
profiles.

## Scope and disclosure

This package certifies a failed proof strategy, not a counterexample to
FiveCDC.  It has not received independent human peer review.

OpenAI Codex agents under human direction derived the result, wrote the
proof, and implemented both exact checks.  No external novelty claim is
made.
