# External-port coverage frontier

This package isolates two human-checkable local facts for the weaker typed
cap target: external states, rather than double stars, should cover all
three physical ports.

- Any port edge adjacent to the proper root is externally covered in every
  `D5` flow, by a six-case local table.
- An internal root-to-cap factor circuit without an external companion on
  the same physical pair must contain a foreign-coordinate blocker on both
  root-to-cap arcs (two kinds of blocker when the root uses the connector's
  shared outside coordinate).
- A cube flow shows that the standard inverse switch-and-suppress operation
  does not automatically apply to every flow on an inverse-inserted parent;
  this is a delimiter for that operation, not a universal no-go theorem.
- A replayable Petersen--Foster certificate gives a stronger delimiter in
  the exact marked-girth geometry: one valid displayed `D5` flow externally
  covers only two of the three physical ports.  Its two foreign blockers
  persist on long root-to-cap arcs.  This refutes arbitrary-flow and
  blocker-only externality arguments, not existential external coverage.

`probe.py` also implements the fixed-factor SAT test for an external state.
It imports the frozen root-transition CNF, adds two clauses forbidding the
inactive cap port from having label `01`, and semantically checks every SAT
model.  A bare UNSAT answer is deliberately reported as uncertified.
`batch_probe.py` applies it to a graph6 corpus.  `CENSUS.md` records the
exact 44,220-query development screen and its limitations.

Run the local table audit with:

```sh
./run_all.sh
```

The quick replay also reconstructs the 890-vertex Petersen--Foster graph,
checks its graph/core geometry, decodes and checks the fixed flow certificate,
enumerates all six root-active factors, and audits the two blocker arcs.

The exact optional SAT replay commands and development environment versions
are in `CENSUS.md` and `VERSIONS.txt`.  The complete retained-corpus replay
takes several minutes; the Petersen--Foster sample is slower and is kept out
of the quick local regression.

The universal *existential* external-coverage statement remains open.  The
fixed-flow certificate proves that the blocker lemma cannot by itself be
converted into a contradiction with marked girth or 3-connectivity: a proof
must be able to change the flow or use additional global information.  This
package does not resolve FiveCDC.
