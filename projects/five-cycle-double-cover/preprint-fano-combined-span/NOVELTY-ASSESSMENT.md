# Provisional novelty and publication assessment

Date: 2026-07-28

## Bottom line

This looks potentially worth circulating as a **short technical
preprint after independent human verification**, but not as a claimed
advance resolving the five-cycle double cover conjecture.

The plausible novelty is moderate and quite specific:

- the common-dual/combined-image theorem for the three switches
  associated with one Fano line;
- the explicit quadratic telescoping potential proving that theorem;
- the exact two-binary-cycle normal form for fixed functional
  projection and its product-boundary cleaning equations; and
- the cotree-diamond theorem showing that the minimum number of
  components in a Fano-line subgraph is unbounded even on
  FiveCDC-positive graphs;
- the simple-contraction obstruction, with the displayed Petersen flow
  as a minimal-looking, human-checkable illustration; and
- the explicit cyclically 4-edge-connected order-60 flow on which all
  seven fixed functional projections fail, with a completion-sound
  four-pole proof and solver-independent exhaustive checker.

The Petersen graph itself is not novel, and “Petersen obstructs a
constrained flow condition” is not new. The order-60 theorem materially
sharpens the structural boundary: it shows that the existential choice of
the flow in the Hušek--Šámal formulation cannot be replaced by an
arbitrary Jaeger 8-flow, even in the cyclically 4-edge-connected domain.
The publication case rests on this result together with the
linear-versus-quadratic mechanism as a coherent package.

## Primary literature checked

The audit used keyword search and direct full-text inspection where an
open manuscript was available, through 28 July 2026.

1. F. Jaeger, *Flows and generalized coloring theorems in graphs*,
   JCTB 26 (1979), 205–216.
   DOI: <https://doi.org/10.1016/0095-8956(79)90057-1>

2. F. C. Holroyd and M. Škoviera, *Colouring of cubic graphs by
   Steiner triple systems*, JCTB 91 (2004), 57–66.
   DOI: <https://doi.org/10.1016/j.jctb.2003.10.003>

3. E. Máčajová and M. Škoviera, *Fano colourings of cubic graphs and
   the Fulkerson Conjecture*, TCS 349 (2005), 112–120.
   DOI: <https://doi.org/10.1016/j.tcs.2005.09.034>

4. D. Král’ et al., *Projective, affine, and abelian colorings of cubic
   graphs*, EJC 30 (2009), 53–69.
   DOI: <https://doi.org/10.1016/j.ejc.2007.11.029>

5. E. Máčajová et al., *Short cycle covers of graphs and nowhere-zero
   flows*, JGT 68 (2011), 340–348.
   DOI: <https://doi.org/10.1002/jgt.20563>

6. L. Jin, G. Mazzuoccolo, and E. Steffen, *Cores, joins and the
   Fano-flow conjectures*, DMGT 38 (2018), 165–175.
   DOI: <https://doi.org/10.7151/dmgt.1999>

7. J. Karabáš et al., *Cubic graphs with colouring defect 3*, EJC
   31(2) (2024), P2.6.
   DOI: <https://doi.org/10.37236/12333>

8. V. Mkrtchyan, *Non-conflicting nowhere-zero
   Z2 × Z2-flows in cubic graphs*, AJC 91(3) (2025), 392–413.
   Primary PDF:
   <https://ajc.maths.uq.edu.au/pdf/91/ajc_v91_p392.pdf>

9. D. W. Cranston et al., *Reconfiguration of Nowhere-zero Flows*,
   arXiv:2606.24685 (2026).
   <https://arxiv.org/abs/2606.24685>

10. R. Hušek and R. Šámal, *Exponentially Many Circuit Double Covers*,
    arXiv:2607.24724 (2026).
    <https://arxiv.org/abs/2607.24724>

Targeted searches for combinations of “Fano flow,” “kernel line,”
“functional projection,” “line-preserving,” “affine coset,” “binary
cycle,” “switching,” “Petersen,” “line subgraph components,”
“connected kernel,” “cotree diamond,” and “cyclically 4-edge-connected”
did not locate the exact statements in the draft.  Search-engine coverage
is imperfect; this is not a priority determination.

## Closest overlap

Mkrtchyan’s 2025 paper is the closest conceptual neighbour. It defines a
non-conflicting nowhere-zero F2²-flow on the contraction of a
complementary 2-factor, proves a Petersen obstruction
(Proposition 2.21), and constructs infinite obstruction families.

That condition is not the condition in this draft:

- Mkrtchyan fixes a perfect matching/complementary 2-factor and asks for
  a non-conflicting F2²-flow on the contracted graph.
- This draft fixes a functional projection of an F2³-flow, parametrises
  every lift by two binary cycles on the original graph, and asks for
  four affine colour classes to have even boundary on every kernel-factor
  component.

The paper should retain an explicit comparison and should not imply that
Petersen’s exceptional role is new. Before submission, a human expert
should determine whether the two conditions admit a useful formal
implication in any special case.

Hušek--Šámal is the closest direct FiveCDC neighbour.  Their Theorem 3.16
states the component condition independently, and their Conjecture 3.19
makes the flow choice existential.  The order-60 theorem is best
understood as proving that this quantifier is necessary, not as evidence
against their conjecture.

## Publication judgment

Current rating: **promising short note, not yet submission-ready**.

Reasons in favour:

- The main span theorem has a compact proof with an explicit certificate,
  rather than being only computational.
- The normal form cleanly isolates the nonlinear gap and prevents a
  misleading proof strategy.
- The structural obstruction theorem is more informative than a bare
  SAT counterexample.
- The unbounded-component theorem is a short infinite construction with
  a direct proof and explicit sharp witnesses.
- The Petersen instance is fully finite and has a human proof, while
  CNF/DRAT and exhaustive enumeration remain as redundant audits.
- The order-60 theorem reaches the natural cyclic-connectivity reduction,
  has a short human local-to-global lemma, and replaces discovery SAT with
  an exact standard-library elimination checker.

Reasons for caution:

- No independent human has checked the proof.
- The terminology is project-internal and needs polishing against the
  established Fano-flow literature.
- The relation to 5-CDC is motivational and indirect.
- The order-60 local profiles are a finite computer-assisted proof, not a
  short handwritten classification; the checker itself still needs an
  independent human code audit or a proof-certificate translation.
- The literature audit is not a substitute for MathSciNet/Zentralblatt
  review or consultation with specialists.
- The most eye-catching example is classical and has a nearby 2025
  obstruction theorem in a different formalism.

## Minimum bar before public submission

1. A graph theorist independently rederive the combined-image, quadratic
   normal-form, unbounded-component, and matching-contraction theorems
   from the definitions.
2. A human verify every row of the potential identity and the
   cut-space duality step.
3. A second person reconstruct the Petersen matching contractions and
   Tait obstruction without using the checker.
4. A human audit the order-60 local-to-global lemma and independently
   reimplement or proof-certificate-check the two pole profiles.
5. Rerun all artifacts in a clean environment and archive exact
   versions/checksums.
6. Expand the literature review using MathSciNet or Zentralblatt and,
   ideally, ask authors working on Fano flows or non-conflicting flows
   about prior overlap.
7. Replace the author placeholder and let the human author rewrite the
   claims in their own scholarly voice.
8. Keep the full AI-use disclosure. Do not call the checkers
   “independent verification” without the qualifier that they are
   separately written but AI-assisted.
