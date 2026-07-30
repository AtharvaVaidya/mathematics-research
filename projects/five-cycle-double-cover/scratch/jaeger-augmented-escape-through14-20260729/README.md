# Augmented-trap escape frontier through order 14

Date: **2026-07-29**

Status: **EXACT FINITE FRONTIER. NOT A PROOF OR DISPROOF OF FIVECDC.**

The complete canonical census proves:

> Every augmented trap in every rooted-star three-tree fibre of every
> simple three-edge-connected cubic graph through order 14 has exact
> augmented escape distance two.

Here “augmented trap” means a positive Jaeger three-tree state with no
successful one-step parallel component--circuit span flag and no legal
reciprocal neighbour that is successful or lowers
\(\Psi=(d_{\min},\sum_i|K_i|)\) lexicographically.  Every certified
two-step path has a safe equal-\(\Psi\) intermediate state.

Exact totals:

| quantity | count |
|---|---:|
| canonical graphs | 419 |
| rooted vertex-orbit fibres | 3,567 |
| states in source census | 529,150,122 |
| old-objective traps | 14,643 |
| augmented traps | 557 |
| augmented-trap source rows | 187 |
| safe first states examined | 659 |
| legal second arcs examined | 4,210 |
| largest number of safe first states examined for one certificate | 4 |
| exact distance-two certificates | 557 |

The input is the exhaustive frozen corpus
`../jaeger-high-girth-local-trap-frontier-20260729/trap-structures-through14.jsonl`.
The audit reconstructs every old trap and every legal incident
neighbour, filters the 557 augmented traps, and then recomputes an
explicit two-exchange escape for each one.

Run the fast package and dependency-integrity checks:

```sh
python3 verify.py
```

Replay all 14,643 old-trap neighbourhoods and compare the 557
certificates byte-for-byte:

```sh
python3 verify.py --replay
```

Or run the producer directly:

```sh
python3 audit.py > /tmp/through14-replay.jsonl
cmp audit-output.jsonl /tmp/through14-replay.jsonl
```

Read `HUMAN-PROOF.md` for the mathematical argument and trust boundary.

## Scope warning

This finite result does not resolve FiveCDC.  A separate exact
order-40 example in this repository has augmented escape distance
three, so radius two is not universal.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, designed and ran the
enumeration, wrote the audit and verifier, and drafted this report.  No
independent human peer review has occurred.
