# Human-checkable finite proof

## The statement

For every canonical simple three-edge-connected cubic graph \(G\) with
\(|V(G)|\leq 14\), every root orbit representative \(r\), and every
ordered partition of the edges of \(G-r\) into three cographic bases,
consider the associated Jaeger three-tree state.  Give a positive state
the lexicographic potential
\[
  \Psi=(d_{\min},|K_0|+|K_1|+|K_2|),
\]
where the \(K_i\) are its three unique odd kernels and \(d_{\min}\) is
the minimum of its seven Fano component defects.

A state is an **augmented trap** when all its 21 parallel
component--circuit span flags fail and no legal reciprocal-exchange
neighbour either has a successful flag or has smaller \(\Psi\).

The finite theorem checked here is:

> Every augmented trap in this complete through-order-14 state space
> has an escape of exactly two reciprocal exchanges.  The intermediate
> state may be chosen to have the same \(\Psi\) and still have no
> successful flag.

This is not a theorem for graphs of arbitrary order and is not a proof
or disproof of the five-cycle-double-cover conjecture.

## Why the enumeration proves the statement

Deleting a prescribed cubic vertex turns a Jaeger vertex-star packing
into an ordered partition of the remaining edges into three cographic
bases.  Conversely, adjoining one distinct root edge to the complement
of each class reconstructs the three spanning trees.  Thus enumeration
of every ordered cographic-basis partition enumerates the entire
rooted-star state fibre.

The frozen source corpus covers 419 canonical simple
three-edge-connected cubic graphs through order 14.  One representative
of each vertex-automorphism orbit gives 3,567 rooted fibres.  The source
producer enumerated all 529,150,122 states and retained the 14,643
positive states for which:

1. all 21 exact binary span tests fail; and
2. every legal reciprocal neighbour has \(\Psi'\geq\Psi\).

These are the old-objective traps.  Every augmented trap is necessarily
on this list.

For each of those 14,643 masks, `audit.py` independently reconstructs
the graph, root spokes, three tree complements, odd kernels, seven
defects, and 21 span flags using the standard-library semantic checker.
It enumerates every exchange between every pair of omitted classes and
retains an exchange only when both changed complements are spanning
trees.  It verifies the frozen legal-neighbour count and verifies again
that no neighbour lowers \(\Psi\).

If any neighbour has a successful span flag, the old trap is not an
augmented trap.  Exactly 557 masks, in 187 source rows, survive this
test.

For every survivor, the audit considers all legal first neighbours
having exactly the same \(\Psi\) and zero successful flags.  From each
such state it enumerates every legal second exchange.  It records the
first endpoint for which either
\[
 \Psi''<\Psi
 \quad\text{or}\quad
 \text{successful\_flags}(S'')>0.
\]
All 557 survivors have such an endpoint.  The audit examined 659 safe
first states and 4,210 second arcs before finding all certificates; no
certificate required more than four safe first states.

Because an augmented trap has no escape in one exchange by definition,
and because the recorded path has two legal exchanges, its escape
distance is exactly two.

## Trust boundary and independent checking

`audit-output.jsonl` contains the graph6 string, root, source trap index,
potential, two local exchange pairs, and endpoint data for every one of
the 557 certificates.  It is evidence, not an axiom: run

```sh
python3 audit.py > /tmp/through14-replay.jsonl
cmp audit-output.jsonl /tmp/through14-replay.jsonl
```

to reconstruct every certificate from the frozen masks.

The complete 529,150,122-state enumeration is inherited from
`../jaeger-high-girth-local-trap-frontier-20260729`.  Its independent
verifier checks graph6 decoding, simplicity, cubicity,
three-edge-connectivity, root orbits, state totals, and frozen hashes;
its optional `--replay-full` mode regenerates the full census.  This
smaller package does not pretend to duplicate that costly first-stage
enumeration.

There is an exact order-40 augmented trap elsewhere in the project whose
shortest escape has length three.  It prevents extrapolating this finite
radius-two statement to all orders.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, designed and ran the
enumeration, wrote the audit and verifier, and drafted this note.  No
independent human peer review has occurred.
