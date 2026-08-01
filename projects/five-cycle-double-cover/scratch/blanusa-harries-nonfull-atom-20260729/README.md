# Blanuša non-full six-pole relation

This package freezes and independently verifies the exact D5 boundary
relation of the 16-vertex six-pole obtained by deleting vertices 13 and 16
from the first retained order-18 Blanuša graph.

It is **not** a FiveCDC counterexample.  The exact result is 555 positive
and 16 negative S5-orbits among the 571 xor-zero boundary orbits.

Human-readable details are in `HUMAN-PROOF.md`.  The negative half has a
single LRAT certificate checked by two independent proof checkers; the
positive half has 555 explicit witnesses checked directly.

Run:

```sh
python3 independent_verify.py
```

The checker tool root may be supplied with `FIVECDC_TOOLS`; otherwise this
workspace's `.tools` directory is used.

Important files:

- `small-pole.txt`: canonical local topology and ordered ports;
- `boundary-relation.jsonl`: 555 witnesses and 16 negative rows;
- `negative-boundary-orbits.cnf`: selector CNF for all negative reps;
- `negative-boundary-orbits.lrat`: UNSAT proof;
- `independent_verify.py`: solver-free semantic and CNF audit plus dual
  LRAT checking;
- `relation-summary.json`: orbit and obstruction classification.

`construct_atom.py` also records a later Harries-cage equality-gadget lift
to internal girth ten.  That expansion is auxiliary and is not used to
establish the small six-pole relation.  It has not produced a FiveCDC
counterexample.

## AI-use and novelty status

The mathematical note, search/producer implementation, independent checker,
CNF builder, and certificate packaging were authored by OpenAI Codex agents
under the user's direction.  The checker was written separately from the
producer, but both are AI-authored.  No human peer review has yet occurred.

Novelty is provisional.  This package establishes a checkable local
six-pole relation; it does not claim a new theorem about all bridgeless
graphs, a proof or disproof of FiveCDC, or priority over prior multipole and
cycle-double-cover literature.  A literature review and independent human
verification are required before submission or public novelty claims.
