# Provisional novelty assessment

Date: 2026-07-29

Status: **PLAUSIBLY NEW PARTIAL THEOREM / PRIORITY NOT ESTABLISHED /
HUMAN LITERATURE REVIEW REQUIRED**.

## Result assessed

The manuscript proves:

1. the simultaneous minimum-projection exchange theorem;
2. exact cleanability of every cardinality-minimum extendable projection
   of size at most fourteen in connected bridgeless loopless cubic graphs;
3. the first failure, at support shape \(5+6\), of the stronger direct
   componentwise-\(\mathrm{GL}(2,2)\) cleaning statement;
4. a size-five replacement certificate excluding every such failure from
   global minimality;
5. exhaustive size-twelve and size-thirteen clean-or-delete theorems,
   each independently reproduced by two exact enumerators;
6. a sharp size-fourteen counterstate to the unrestricted
   clean-or-delete boundary lemma, together with a simple bridgeless
   cubic realization whose displayed projection is uncleanable but whose
   four global minima are all cleanable; and
7. a complete size-fourteen primary census whose only 224 residuals all
   have shape \(7+7\), an independent full \(7+7\) census, and a
   pairing-robust Kempe path theorem that sends every residual to a
   strict size-seven deletion.

This is a partial theorem about the Hušek--Šámal flow criterion.  It does
not resolve the Five-Cycle Double Cover Conjecture.

## Primary-source screen

The immediate source is:

- Radek Hušek and Robert Šámal, *Exponentially Many Circuit Double
  Covers*, arXiv:2607.24724v1, submitted 27 July 2026,
  <https://arxiv.org/abs/2607.24724>.

That paper defines labeled cycle double covers using even subgraphs,
allows the empty subgraph, states FiveCDC as open, and proves that its
component-parity condition on a nowhere-zero
\(\mathbb F_2^3\)-flow is equivalent to FiveCDC.  It does not state a
minimum-coordinate-support selection theorem or the componentwise direct
repair used here.

The prescribed-cycle antecedent is:

- Arthur Hoffmann-Ostenhof, *A Note on 5-Cycle Double Covers*, Graphs and
  Combinatorics 29 (2013), 977--979,
  <https://doi.org/10.1007/s00373-012-1169-8>.

A targeted arXiv search on 29 July 2026 for combinations of “minimum
extendable projection,” “minimum support,” “Fano projection,”
“componentwise GL(2,2),” and “five-cycle double cover” found no matching
prior theorem.  Because the Hušek--Šámal preprint itself was only two days
old, this search cannot establish priority or rule out unpublished
parallel work.

## Publication judgment

The exchange theorem, through-fourteen boundary theorem, the
triangle-expanded-Petersen direct-repair countermodel, and the sharp
size-fourteen clean-or-delete countermodel form a coherent, reproducible
research note.  The new size-fourteen ingredient is not merely a larger
census: its two-colour path-switch argument quantifies over every possible
terminal pairing in an unknown cubic realization and is checked by 724
literal deletion rows.  A targeted web/arXiv screen found no theorem
stated in the language of minimum extendable Fano projections, but this
does not establish priority.  The result is suitable for public circulation
as an AI-assisted preprint **after** a graph theorist:

- checks the flow-to-cleanliness semantics line by line;
- audits both finite classifiers in a clean environment;
- checks the split-occurrence Kempe lemma and matching-hitting implication;
- repeats the literature search using MathSciNet, zbMATH, and expert
  contacts;
- confirms authorship and disclosure policy for the chosen venue; and
- decides whether a computational theorem of this scope merits a
  standalone submission or should be communicated first to Hušek and
  Šámal.

Until that review, the GitHub draft should remain explicitly provisional
and should not be described as a FiveCDC resolution.  The theorem is
cubic; no arbitrary-degree reduction is supplied.

## AI-use disclosure

OpenAI Codex agents under Atharva Vaidya's direction discovered the proof
route, counterstates, and size-fourteen Kempe escape; wrote the exact
classifiers, exhaustive certificate builders, and independent checkers;
performed the preliminary literature screen; and drafted the manuscript
and this assessment.  Agent agreement is not independent human
verification or peer review.
