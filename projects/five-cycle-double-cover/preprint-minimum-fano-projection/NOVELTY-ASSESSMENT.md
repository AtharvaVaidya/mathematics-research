# Provisional novelty assessment

Date: 2026-07-29

Status: **PLAUSIBLY NEW PARTIAL THEOREM / PRIORITY NOT ESTABLISHED /
HUMAN LITERATURE REVIEW REQUIRED**.

## Result assessed

The manuscript proves:

1. the simultaneous minimum-projection exchange theorem;
2. exact cleanability of every cardinality-minimum extendable projection
   of size at most fifteen in connected bridgeless loopless cubic graphs;
3. a universal relative-\(\mathrm{GL}(2,2)\) tensor theorem implying
   direct cleanability of every one-support-circuit boundary state, and
   of every several-circuit state with circuitwise component balance;
4. an interaction-multigraph dictionary for two-occurrence complement
   components and the Petersen system as the smallest loopless abstract
   failure of direct cleaning in that subclass, together with a complete
   strict descent to a clean global minimum;
5. the first failure in the all-four-colour minimum-projection census, at
   support shape \(5+6\), of the stronger direct
   componentwise-\(\mathrm{GL}(2,2)\) cleaning statement;
6. a size-five replacement certificate excluding every such failure from
   global minimality;
7. exhaustive size-twelve and size-thirteen clean-or-delete theorems,
   each independently reproduced by two exact enumerators;
8. a sharp size-fourteen counterstate to the unrestricted
   clean-or-delete boundary lemma, together with a simple bridgeless
   cubic realization whose displayed projection is uncleanable but whose
   four global minima are all cleanable; and
9. a complete size-fourteen primary census whose only 224 residuals all
   have shape \(7+7\), an independent full \(7+7\) census, and a
   pairing-robust Kempe path theorem that sends every residual to a
   strict size-seven deletion; and
10. a complete size-fifteen primary census of 35,247,202,556
   charge-valid states whose only 6,036 residuals all have shape \(7+8\),
   together with an independently written induction audit and
   realization-robust inverse Kempe lifts;
11. a general \(K_4-e\) inflation theorem showing that all four static
   exchange inequalities can be forced without changing the local
   two-colour boundary pairings, together with an explicit state that
   defeats every one-round fixed-colour Kempe move but escapes in two
   rounds;
12. an unbounded two-terminal cleaning theorem for one-circuit supports;
   and
13. a conditional orbit-reflecting \(K_{3,3}-e\) inflation theorem that
    transfers any hypothetical goal-free dynamic boundary orbit to one
    satisfying all four recomputed exchange inequalities at every
    reachable state.

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

The \(K_{3,3}\) input used by the dynamic inflation is prior work:

- sarah-marie belcastro and Ruth Haas, *Counting edge-Kempe-equivalence
  classes for 3-edge-colored cubic graphs*, arXiv:1209.1730,
  <https://arxiv.org/abs/1209.1730>.  Section 4.2 records the two
  edge-Kempe classes of \(K_{3,3}\) and the Hamiltonian property of every
  colour pair.  The project claims novelty only for its conditional
  orbit-reflecting use of the edge-deleted pole, not for that fact.

A targeted arXiv search on 29 July 2026 for combinations of “minimum
extendable projection,” “minimum support,” “Fano projection,”
“componentwise GL(2,2),” and “five-cycle double cover” found no matching
prior theorem.  Because the Hušek--Šámal preprint itself was only two days
old, this search cannot establish priority or rule out unpublished
parallel work.

The later relative-\(\mathrm{GL}(2,2)\) tensor proof has not received a
literature-wide novelty screen.  Its Euler-tour, interlacement, and
quadratic-parity language is close to established circuit-partition and
isotropic-system theory.  The manuscript therefore makes no priority
claim for that lemma pending expert comparison with Bouchet's and
Traldi's frameworks.

## Publication judgment

The exchange theorem, through-fifteen boundary theorem, the universal
one-circuit tensor theorem, the
triangle-expanded-Petersen direct-repair countermodel, and the sharp
size-fourteen clean-or-delete countermodel form a coherent, reproducible
research note.  The static-inflation theorem further identifies a precise
proof-method boundary: the initial shortest-join inequalities have no
additional universal local boundary force once every support circuit uses
all four colours; any general descent must reapply them dynamically.
The size-fourteen and size-fifteen advances are not merely larger
censuses.  At size fourteen the two-colour path-switch argument quantifies
over every possible terminal pairing in an unknown cubic realization; at
size fifteen the inverse-smoothing audit links every residual to the
size-fourteen family, and a separate matching-game checker verifies every
residual directly.  The tensor theorem removes the entire
one-circuit branch by a short human argument.  The Petersen interaction
system shows sharply why circuitwise component balance cannot simply be
dropped: direct cleaning fails, but strict deletion succeeds for every
extension.  The two-terminal theorem also excludes an
unbounded dynamic-trap class without computation, while the conditional
\(K_{3,3}-e\) theorem cleanly separates boundary-orbit obstruction from
the metric exchange inequalities.  A targeted web/arXiv screen found no
theorem stated in the language of minimum extendable Fano projections, but
this does not establish priority.  The result is suitable for public
circulation as an explicitly provisional AI-assisted working preprint.
A formal venue submission should wait until a graph theorist:

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
cubic.  A separate elementary incidence-cluster theorem shows that the
standard universal FiveCDC assertion reduces from arbitrary finite
bridgeless multigraphs to loopless cubic multigraphs, and the usual local
reductions reach strong snarks.  No novelty is claimed for those standard
graph-class reductions, and they do not extend the size-fifteen boundary
theorem to higher-degree vertices.

## AI-use disclosure

OpenAI Codex agents under Atharva Vaidya's direction discovered the proof
route, counterstates, size-fourteen and size-fifteen Kempe escapes, the
relative-\(\mathrm{GL}(2,2)\) tensor proof, the Petersen interaction
dictionary and descent, and the static-inflation obstruction; proposed
the two-terminal cleaning and orbit-reflecting
\(K_{3,3}-e\) lemmas; wrote the exact
classifiers, exhaustive certificate builders, and independent checkers;
performed the preliminary literature screen; and drafted the manuscript
and this assessment.  A hostile agent audit of the inflation proof passed
after correcting its terminal-distance exposition.  Agent agreement is
not independent human verification or peer review.
