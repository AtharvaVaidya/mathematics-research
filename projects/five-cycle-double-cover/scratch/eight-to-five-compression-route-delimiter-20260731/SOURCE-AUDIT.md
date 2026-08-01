# Primary-source audit and novelty boundary

Audit date: **2026-07-31**

## Sources read

1. Sang-il Oum, *A proof of the cycle double cover conjecture by OpenAI:
   An exposition*, arXiv:2607.16356v2, 23 July 2026,
   <https://arxiv.org/abs/2607.16356v2>.

   The downloaded PDF had SHA-256
   `69786adce3a924343e2d5debac6d7fb30aaa0b95b85abe8b32a53e17d5153da1`.
   Relevant items are Lemmas 11--12, Proposition 15, and Theorem 16.  They
   give the two-element edge labels, the flow-lifting formula, and the
   eight-cycle conclusion.

2. Radek Hušek and Robert Šámal, *Exponentially Many Circuit Double
   Covers*, arXiv:2607.24724v1, 27 July 2026,
   <https://arxiv.org/abs/2607.24724v1>.

   The downloaded PDF had SHA-256
   `06008575acdae9fc84e508d0e290eeaf84cebf0ffe4cfbf5f4af470af254c895`.
   Relevant items are Observations 2.1, 2.3, 2.4, 3.5, 3.15, Theorem 3.16,
   and Conjecture 3.19.  In particular, Observation 2.4 proves that the
   lifting data and labelled cycle double covers are in bijection, while
   Conjecture 3.19 remains equivalent to FiveCDC.

3. Daniel Král', Edita Máčajová, Ondřej Pangrác, André Raspaud,
   Jean-Sébastien Sereni, and Martin Škoviera, *Projective, affine, and
   abelian colorings of cubic graphs*, European Journal of Combinatorics
   30 (2009), 53--69, DOI
   <https://doi.org/10.1016/j.ejc.2007.11.029>.

   The author-hosted PDF used for the audit had SHA-256
   `d82790b298c58c682bc3244fb0aa8dec38e6b75316174d727bbe9dd315f2ae70`.
   Section 2 defines homomorphisms of partial Steiner triple systems, and
   Theorem 7.1 proves that a cubic graph has a FiveCDC exactly when it has
   a colouring by the Desargues configuration.  This is the closest prior
   framework: the context-free table in the present package is a
   configuration homomorphism problem.  No novelty is claimed for that
   language or for the Desargues/FiveCDC equivalence.

## What was searched

The bounded screen used the exact phrases and combinations

```text
"five-cycle double cover" recolouring
"cycle double cover" triangle cocycle
"pair labelling" "cycle double cover"
context-free pair recolouring cycle double cover
```

and followed the primary papers' discussion of configuration colourings,
Fano/affine colourings, Desargues colourings, and the July 2026 lifting
system.  Exact searches for the graph6 record and the twelve displayed
triples found no relevant mathematical source.

## Conservative novelty assessment

No source inspected states the following exact combination:

- a realized 12-vertex simple bridgeless Oum cover whose local triangle
  rows span the cycle space of `K6`;
- the resulting rigidity of every nonlinear context-free old-pair lookup
  into five-bit labels;
- the `K6 -> R5` obstruction; and
- the sharp order-12 lower bound for this full-rank mechanism.

This is only a bounded screen, so priority is unestablished.  The
triangle-cocycle/cut-space identity itself is elementary algebraic graph
theory, and configuration homomorphisms are established prior art.  Any
publication should present the result as a modest explicit route
delimiter and obtain specialist review before claiming novelty.

## Scope guard

The result does not resolve FiveCDC.  The witness has a checked
3-edge-colouring.  It excludes a context-free lookup keyed only by the old
pair type; global edge-dependent recolouring is outside the theorem.  The
orientable conjecture is not analyzed.

## AI-use disclosure

The audit, searches, comparison, prose, proof synthesis, and code were
performed by OpenAI Codex agents under Atharva Vaidya's direction.  This
is not an independent human literature review.
