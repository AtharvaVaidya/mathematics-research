# Two-occurrence interaction theorem: exact Petersen no-go

Date: 2026-07-29

Status: **SMALLEST EXACT SUBCLASS COUNTERSTATE / COMPLETE DESCENT /
NOT A FIVECDC COUNTEREXAMPLE**.

When every component of \(G-H\) has exactly two support occurrences,
contract support circuits to vertices and complement components to
edges.  The common nonzero derivative on a component is then a
nowhere-zero \(\mathbb F_2^2\)-flow on this interaction multigraph.
Componentwise \(\operatorname{GL}(2,2)\) maps range over all such flows.

After circuit integration, either occurrence of a component traverses
an edge of the \(K_4\) on the four low colours.  The component is clean
exactly when its two occurrences traverse the same \(K_4\) edge.

This package gives the smallest loopless abstract counterstate to the
claim that this subclass is always directly cleanable:

```text
support circuit orders  01234 | 03142
interaction graph        two vertices, five parallel edges
initial flow             11123
support low words        10130 | 13210
```

It is realized literally by the Petersen graph, with the two 5-circuits
as support and the perfect matching as the five complement components.
All 60 nowhere-zero interaction flows are exhausted:

```text
clean extensions       0
deletable extensions  60
```

Equivalently, after fixing one component map, exactly 320 of the
\(6^4\) map tuples are circuit-integrable; none is clean and all 320
delete a support circuit.

The deletion is explicit.  The first word `10130` omits colour 2, so
adding `(1,2)` around that 5-circuit changes its low word to `32312`
and removes it from the support.  The remaining size-five projection is
globally minimum because the Petersen graph is non-Tait and has girth
five.  It is clean because its complement is connected.

Thus support-preserving Kempe reconfiguration cannot rescue this fixed
projection—every possible extension has already been checked—but the
minimum-exchange descent succeeds universally.  This sharpens the proof
frontier without threatening FiveCDC.

`HUMAN-PROOF.md` contains the interaction-flow proof, the complete
ten-row orbit table, the Petersen graph construction, and the
smaller-size exact census.

## Replay

```sh
python3 verify.py
python3 independent_audit.py
shasum -a 256 -c SHA256SUMS
```

The verifiers use only the Python standard library.  `search_small.py`
is the transparent pairing search that first locates the state; the
frozen claims are independently rebuilt in the two verifiers.

## AI-use disclosure

OpenAI Codex agents under human direction formulated the interaction
model, found and audited the counterstate, and wrote this package.  It
has not received independent human peer review.  No FiveCDC-resolution
or literature-priority claim is made.
