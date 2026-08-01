# Reconstructed MNP minimum-support packing

Status: **PASS for the finite certificate and recursive replay; the all-\(n\)
minimality input is cited from MNP**.

This package proves a narrow infinite-family result:

> In the frozen, figure-derived reconstruction
> \(\widehat H_n\), \(n\ge2\), the published exact-zero matching
> \(M_n=\{\epsilon_1,\ldots,\epsilon_n\}\) packs two edge-disjoint
> \(\partial M_n\)-joins.

The joins have sizes \(12n+3\) and \(11n+26\).  Mattiolo, Negrini, and
Pagani prove \(r_f(H_n)=n\), so—conditional on fidelity of the graph
transcription—this support is globally minimum.  The lifting argument in
`THEOREM.md` makes it a globally minimum **nonzero** value class of a
nowhere-zero \(\mathbb F_2^3\)-flow as well.

This is not a resolution of FiveCDC and not a girth-at-least-10 result.
MNP prove cyclic edge-connectivity 5 for their family; the reconstructed
graphs checked here through \(n=100\) have girth 5.  Those are different
properties.

## Replay

Only the Python standard library is required.

```sh
python3 verify.py --max-n 20
```

The default replay:

- decodes literal graph6 encodings of the \(H_2\) base and the closed
  42-vertex `J` graph;
- checks all 40 two-bit parity equations in the open tile;
- checks the literal \(H_2\) matching and two boundary joins;
- applies the recursive substitution and checks every graph through
  \(n=20\);
- checks simplicity, connectedness, cubicity, bridgelessness, and girth 5
  through the requested finite prefix;
- checks that the matching remains a matching and that both joins have
  exactly its odd vertex set;
- checks disjointness, the stable interface, and all four size formulas;
- compares the generated \(H_2,H_3,H_4,H_5\) edge lists byte-semantically
  with four frozen regression digests produced by the same reconstructed
  recurrence.

The checker is iterative and accepts any larger finite prefix:

```sh
python3 verify.py --max-n 100
```

Both commands pass in the frozen environment; the stress test reaches an
order-4,002 graph with 6,003 edges.  The \(n=20\) endpoint has
802 vertices and 1,203 edges, with class sizes

```text
M=20, J1=243, J2=246, R=694.
```

## What is finite, and what is imported

The base, tile, gluing state, recurrence, parity, disjointness, and count
formulas are all literal and checked here.  The human induction in
`THEOREM.md` turns the one-tile check into an all-\(n\) theorem.

The package does **not** machine-reprove MNP's lower bound.  It imports:

- Lemma 3.5: the displayed \(\mathbb F_2^2\)-flow has exact zeros
  \(\epsilon_1,\ldots,\epsilon_n\) and \(r_f(Y_n)=n\);
- Theorem 3.6: \(r_f(H_n)=n\);
- Section 4 / Theorem 1.1: cyclic edge-connectivity 5.

Primary source:
[Mattiolo--Negrini--Pagani, arXiv:2604.22501v1](https://arxiv.org/abs/2604.22501).

The arXiv source has vector figures but no author-supplied machine-readable
edge list.  `certificate.json` records exact source and figure hashes and
the reconstruction qualification.  Identity with the author-defined
family therefore still needs direct human comparison with those figures.

## Files

- `THEOREM.md`: complete human proof, full 40-row local tile table,
  \(\mathbb F_2^3\) lift, source boundary, and AI disclosure.
- `certificate.json`: literal graph encodings, edge sets, interface,
  digests, count formulas, and source provenance.
- `verify.py`: dependency-free checker and recursive generator.
- `verification.json`: concise retained result of the \(n\le20\) replay.
- `SHA256SUMS`: integrity manifest for the five package files other than
  the manifest itself.

## Novelty and AI disclosure

No priority claim is made.  The result is a specialized packing refinement
for a family already known, by a separate oddness-two route, to have
five-cycle double covers.  A literature review and independent graph
theorist review are required before a standalone scholarly submission or
priority claim.

The stable state, tile certificate, induction, and checker were developed
with substantial OpenAI Codex assistance under human direction on
2026-07-29.  The full literal data and dependency-free verifier are
provided so that the new mathematics can be checked without trusting an AI
system.
