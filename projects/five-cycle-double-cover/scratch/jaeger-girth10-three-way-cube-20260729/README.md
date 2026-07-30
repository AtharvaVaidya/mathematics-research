# Girth-10 three-way exchange cube

Date: **2026-07-29**

Status: **EXACT AUXILIARY COUNTEREXAMPLE. NOT A PROOF OR DISPROOF OF
FIVECDC.**

This package proves that a proper-subset-safe three-way Jaeger exchange
interaction does **not** force a graph circuit of length at most nine or
a cyclic edge cut of size at most four.

The witness lies in the 130-vertex lift-13 Petersen graph, independently
checked to be simple cubic, three-edge-connected, girth ten, and
cyclically five-edge-connected.  Three disjoint exchanges with
coordinate pairs `01,12,01` form an eight-state cube.  All seven proper
subsets are nonterminal and not below the seed potential
`Psi=(2,210)`; the full triple has `Psi=(2,209)`.  The six path-side
fundamental circuits have lengths

```text
(32,10), (29,11), (11,16).
```

The parent project's retained exact oddness census records this graph as
oddness zero, so it is Tait-colourable.  It is a high-girth positive
control, not a snark-domain or minimal-counterexample sample.

This closes the attempted explanation of the order-40 radius-three
example purely by its short circuits or small cyclic cuts.

It does not produce a high-girth radius-two counterexample.  The same
seed has a different, explicitly verified escape in two exchanges.
Thus a universal high-girth radius-two theorem remains open.

The host lift is Tait-colourable and therefore has exact oddness zero.
It is not a snark and is not a sample from the non-Tait,
oddness-at-least-six minimal-counterexample domain.  Its role here is
only to test whether high girth and high cyclic edge-connectivity
localize three-way exchange geometry.

Run the independent witness, full seed-neighborhood, and cyclic-cut
checks:

```sh
python3 verify.py
```

Run the exact circuit audit for all 196 two-step escapes in the frozen
lift-13 sample:

```sh
python3 audit_portfolio_circuits.py
```

Check frozen bytes:

```sh
shasum -a 256 -c SHA256SUMS
```

See `HUMAN-PROOF.md` for the exact table, proof, and trust boundary.

## Publication status and AI-use disclosure

The finite auxiliary obstruction appears new within this project.  It
is a proof-design constraint, not a standalone resolution of FiveCDC.

OpenAI Codex agents, directed by Atharva Vaidya, designed and ran the
search and audits, found the witness, wrote the independent verifier,
derived the circuit interpretation, and drafted this report.  No
independent human peer review has occurred.
