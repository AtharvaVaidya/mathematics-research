# Publication and novelty audit

Date: 2026-07-28

Scope: `preprint-fano-one-switch/`, the binary-packing-repair frontier
note, and the certified order-144 package added in commit `598396a`.

## Bottom line

There is a legitimate publication candidate here, but it is a negative
methods paper, not a resolution of the Five-Cycle Double Cover
Conjecture.

The strongest submission-ready mathematical core is the pair of
human-checkable construction theorems already in `main.tex`:

1. the explicit 40-vertex flow that remains unsuccessful after every
   legal connected-circuit switch; and
2. the explicit 46-vertex potential-rigid construction that forces a
   coordinate `K_6` before and after every legal connected-circuit
   switch, defeating pure merging into five coordinates.

The new 144-vertex computation is a strong certified boundary result:
it defeats every legal binary-cycle repair on a simple non-Tait cubic
graph of cyclic edge-connectivity at least four.  It should be included
as a computational appendix or companion data result.  It is not, by
itself, a strong standalone paper because it refutes an auxiliary
statement introduced during this project and the host has girth five,
outside the surviving girth-at-least-ten reduction.

The exact constructions, the particular repair targets, and the
certified countermodels appear novel in the literature search described
below.  This novelty judgment is provisional.  A specialist search and
direct contact with researchers working on five-cycle double covers and
flow reconfiguration are still required before a priority claim.

As part of this audit, the three separately written standard-library
checkers for the 10-, 40-, and 46-vertex constructions were rerun from
the repository and returned `VERIFIED`, `ACCEPTED`, and `PASS`,
respectively.  This is an implementation replay, not new human
verification.

## Claim-by-claim assessment

| Claim | What the project actually proves | Novelty assessment | Publication treatment |
|---|---|---|---|
| Pair-label encoding of a 5-CDC | A 5-CDC is equivalent to labelling every edge by a two-subset of `[5]` with even coordinate incidence at every vertex. | Standard or immediate from the definition; not new. | Preliminary proposition only. |
| Matching/4-flow sufficient condition | A supplied `F_2^3` flow yields a 5-CDC when one value class packs two edge-disjoint boundary joins. | The underlying matching/nowhere-zero-4-flow characterization is prior. The displayed specialization and explicit coordinate lift are useful exposition, not a priority theorem. | Attribute Hoffmann-Ostenhof explicitly and retain the self-contained proof for convention checking. |
| Four canonical joins and their tetrahedral intersections | For a fixed value class, four linear functionals give four boundary joins whose pairwise intersections are the other six value classes. | Elementary and plausibly unrecorded in this exact form; too small for a headline novelty claim. | State as an elementary structural proposition. |
| Connected-circuit domination fails | The 40-vertex construction is bad initially and after every legal connected-circuit switch, while having a 3-CDC. | Likely new. Exact-phrase and topic searches found no prior 5-CDC-specific domination statement or this construction. | Main human theorem. Emphasize the construction and proof, not the conjecture-resolution context. |
| Pure merging fails before and after one connected-circuit switch | The 46-vertex construction forces a translated `K_6` in the coordinate co-occurrence graph on an untouched rigid cap. | Likely new. The potential construction is prior; the pure-merge obstruction, rigid cap, and composition appear new. | Main human theorem. Clearly define “potential-compatible” and “pure merge” as project-local terminology. |
| Forty-two binary repair queries reduce to 21 | Paired targets `b` and `b+t` are equivalent by symmetric difference with a functional support cycle. | Likely new in this exact formulation, but elementary once stated. | Lemma supporting the computational appendix. |
| Order-108 connected binary-repair countermodel | Connectedness alone does not force a repair; the selector formula is UNSAT and certified. | Likely new but structurally expected from the two-sum construction. | Secondary computational result. |
| Order-144 cyclically-four binary-repair countermodel | All seven initial packing formulas, all 21 normalized arbitrary binary-cycle repair formulas, and Tait colouring are UNSAT. | The exact object and certificates appear new. The statement being refuted is project-generated, so novelty is real but narrow. | Certified computational appendix or companion artifact, not the title claim. |
| Finite flow-orbit frontiers | Large retained censuses have zero obstructions in the stated scopes. | Potentially useful data, but scope completeness and rerun provenance vary by row. | Label “Computational Observation”; move most totals to an appendix or data paper. |
| FiveCDC | No proof or disproof. Every principal countermodel in the draft has an explicit standard FiveCDC, often a 3-CDC. | The conjecture remains open. | Put this in the title-page status box, abstract, introduction, every theorem discussion, and conclusion. |
| Orientable FiveCDC | Not encoded or tested. | No result. | State explicitly that orientability is outside scope. |

## Literature boundary

The following primary sources establish the principal prior-art
boundaries.

- Arthur Hoffmann-Ostenhof, *A note on 5-cycle double covers*,
  [arXiv:1209.0096](https://arxiv.org/abs/1209.0096), gives the
  matching/nowhere-zero-4-flow characterization underlying the
  successful-value condition.  The paper must not claim this
  characterization as new.
- Siyan Liu, Rong-Xia Hao, Rong Luo, and Cun-Quan Zhang,
  *5-Cycle Double Covers, 4-Flows, and Catlin Reduction*,
  [DOI 10.1137/22M1472425](https://doi.org/10.1137/22M1472425),
  develops a published 4-flow route and sufficient conditions for
  several snark families.
- The same authors, *Five-Cycle Double Cover and Shortest Cycle Cover*,
  [DOI 10.1002/jgt.23164](https://doi.org/10.1002/jgt.23164),
  treats weak-oddness-two graphs and further sufficient conditions.
- Louis Esperet, Kevin Hendrey, Aurélie Lagoutte, Margaux Marseloo,
  Sergey Norin, and Raphael Steiner, *Nowhere-zero flow
  reconfiguration*, [arXiv:2512.17342v4](https://arxiv.org/abs/2512.17342),
  introduces the relevant cycle-supported reconfiguration graph.
  In particular, adjacency and the absence of frozen flows for most
  groups are prior; neither implies domination by successful flows.
- Daniel W. Cranston, Jiaao Li, Bo Su, Zhouningxin Wang, and Ningyan Xu,
  *Reconfiguration of Nowhere-zero Flows*,
  [arXiv:2606.24685](https://arxiv.org/abs/2606.24685), develops
  flow-connectedness and cubic reductions.  The draft should retain
  its distinction between connectivity of a reconfiguration graph and
  domination by a 5-CDC-sufficient target set.
- Jim Geelen’s [exposition](https://arxiv.org/abs/2607.15399),
  Sang-il Oum’s [exposition](https://arxiv.org/abs/2607.16356), and
  Shiva Kintali’s [three-bit-flow account](https://arxiv.org/abs/2607.14140)
  establish the current cycle-double-cover background and the prior
  flow-to-two-label construction.  They do not settle the restriction
  to five Eulerian members.
- Ligang Jin, Giuseppe Mazzuoccolo, and Eckhard Steffen,
  *Cores, Joins and the Fano-Flow Conjectures*,
  [arXiv:1601.05762](https://arxiv.org/abs/1601.05762), uses
  “Fano-flow conjectures” for a different family of statements.  The
  present project must not suggest that its countermodels refute those
  conjectures.

Searches through 2026-07-28 for the exact phrases “binary packing
repair,” “one-circuit repair” with five-cycle double covers, and the
specific value-class/two-join repair statement found no matching prior
paper.  Exact-phrase absence is not a comprehensive novelty proof.
Before submission, a human author should search MathSciNet, zbMATH,
Google Scholar citation chains, theses, and the relevant monographs,
then ask the authors of the recent reconfiguration papers whether the
specific domination and binary-repair variants have appeared under
different terminology.

## Audit of the order-144 certificate package

The finite claim is well specified and substantially stronger than a
solver log.

- `countermodel-order144.txt` freezes the graph and the 216 flow values.
- `verify_graph_flow.cpp` independently decodes the graph, checks
  simplicity, cubicity, connectedness, bridgelessness, the flow,
  girth five, and absence of a cycle-separating edge deletion of size
  one, two, or three.
- Seven CNFs encode failure of the initial value-class packing tests.
- Twenty-one CNFs encode all normalized point-line binary-cycle repair
  incidences.  The point-line symmetry supplies the other 21 ordered
  target choices.
- One CNF encodes non-3-edge-colourability.
- Each of the 29 CNFs has an LRAT accepted by both the C
  `lrat-check` implementation and the CakeML-generated verified
  `cake_lpr` checker.
- `verify.py` reconstructs the CNF clauses from the displayed semantics
  instead of importing the producer.
- `fivecdc.witness` is a positive certificate checked directly by
  `verify_fivecdc.py`.

The logical scope is exact:

> There exists a simple connected non-Tait cubic graph of order 144,
> girth five, and cyclic edge-connectivity at least four, together with
> a nowhere-zero `F_2^3` flow, such that no value class initially packs
> two edge-disjoint boundary joins and no legal switch on an arbitrary
> binary cycle makes any value class pack.

This statement is certified.  It refutes the repair statement with only
the cyclic-connectivity restriction.  It does not refute the stated BPR
conjecture because that conjecture additionally assumes girth at least
ten.  It does not refute FiveCDC because the same graph has an explicit
FiveCDC with member sizes `93, 96, 69, 84, 90`.

The phrase “human-checkable” needs two meanings in the paper:

1. the 40- and 46-vertex theorems have ordinary finite proofs that a
   human can check from the displayed incidence tables and row
   reductions; and
2. the 144-vertex negative statement is mechanically checkable by a
   human running small proof checkers, but it is not a realistic
   line-by-line hand proof.

Do not call the two LRAT replays “two independent proofs.”  They are two
checkers replaying the same proof objects.  Do not call the clause
reconstructor “independent verification” without immediately adding
that it was also AI-written and has not been independently reviewed by a
human.

## Technical caveats to fix before an external release

1. **Portable replay.** `prove_all.py` and `verify.py` default to
   absolute paths under `/Users/atharvavaidya/Documents/conjectures`,
   and `reproduce.sh` does not pass portable overrides.  Add command-line
   forwarding or environment-variable discovery, document checker
   installation and exact versions, and test the package in a clean
   Linux container.
2. **Separate replay from regeneration.** A frozen-certificate checker
   should only replay the checked-in CNFs/LRATs.  A separate regeneration
   command may rebuild and overwrite them.  The present `reproduce.sh`
   mixes these operations.
3. **Manifest provenance.** `proof-manifest.json` records local executable
   paths.  Replace these with tool names, versions, source commit hashes,
   and build instructions; keep host paths only in an un-hashed run log.
4. **Canonicality.** The package freezes a labelled graph6 record.  It
   does not presently establish in the README that the record is
   nauty-canonical.  Either add a canonicalization transcript and hash or
   continue to call it only a labelled encoding.
5. **No minimality claim.** No search proves that order 144 is the
   smallest obstruction.  Avoid “smallest,” “minimal,” and similar
   wording.
6. **Cyclic connectivity wording.** The structural checker establishes
   no cyclic cut of size at most three.  Prefer “cyclic edge-connectivity
   at least four” unless exact equality is separately checked.
7. **Planarity metadata.** Nonplanarity is not mathematically used.  If
   retained, give a portable certificate or label the `planarg`
   transcript as software-reported metadata.
8. **Independent human rerun.** At least one human other than the
   submitting author should rebuild the CNFs from the mathematical
   definition, replay the LRATs, and check a randomly selected set of
   clauses by hand before submission.
9. **Artifact size and logs.** The repository commit includes all solver
   logs.  A release tarball should contain the graph, flow, CNFs, LRATs,
   checkers, manifests, concise verification logs, and source; verbose
   solver telemetry can be optional.
10. **Frontier census claims.** Keep exact finite scopes and distinguish
    complete graph/flow enumeration from sampled flows, retained external
    graph-generation output, and aggregate-only verification.

## Recommended manuscript

Recommended title:

> **Obstructions to local Fano-flow repair strategies for five-cycle
> double covers**

Recommended organization:

1. Definitions, pair labels, and explicit statement that FiveCDC remains
   open.
2. Prior matching/4-flow characterization and the successful-value
   specialization.
3. The four canonical joins and exact switch law.
4. The 40-vertex connected-circuit construction, with the full
   human-checkable proof.
5. Potential-compatible eight-covers and the 46-vertex rigid-cap
   construction, with the full human-checkable proof.
6. Arbitrary binary-cycle repair: exact definition, the 42-to-21
   symmetry, and the order-144 certified countermodel.
7. What survives: the girth-at-least-ten branch, richer transformations,
   and direct FiveCDC search.
8. Reproducibility appendix and artifact DOI.

The very large finite-frontier table should move to an appendix.  It is
context for how plausible the false statements looked, not the
mathematical center of the paper.

### Candidate revised abstract

> Let `f` be a nowhere-zero `F_2^3` flow on a loopless cubic graph.  Each
> nonzero value class is a matching, and the published
> matching/4-flow characterization yields a standard five-cycle double
> cover whenever the complement of one value class packs two
> edge-disjoint boundary joins.  We study whether this sufficient
> condition can always be reached by local changes of `f`.
>
> We give two explicit composition countermodels with ordinary finite
> proofs.  A 40-vertex connected bridgeless cubic graph has a supplied
> flow for which no value class packs, and the same remains true after
> every legal switch on one connected circuit.  A separate 46-vertex
> construction contains a potential-rigid cap that forces a `K_6` in
> the coordinate co-occurrence graph, before and after every such
> switch, and therefore prevents pure merging of the associated
> eight-cover into five Eulerian coordinates.
>
> We also give a certificate-checked computational boundary result.  On
> a simple non-Tait cubic graph of order 144, girth five, and cyclic
> edge-connectivity at least four, all seven initial packing tests and
> all 21 normalized arbitrary binary-cycle repair tests are
> unsatisfiable.  Twenty-nine LRAT certificates are replayed by two
> proof checkers, and a separately structured program reconstructs the
> formulas.  Each graph in the paper has an explicit standard
> five-cycle double cover.  Thus the results eliminate three local
> repair strategies but neither prove nor disprove the Five-Cycle
> Double Cover Conjecture.

## Required AI-use and responsibility statement

The existing disclosure is unusually candid and should remain on page
one.  For a submitted version, replace the placeholder author line with
the human author or authors who have actually reviewed the work and are
willing to accept responsibility.  Do not list an AI system as an
author.

Suggested final wording:

> **AI-use disclosure.** OpenAI Codex agents using GPT-5-series models,
> directed by Atharva Vaidya, materially contributed to selecting the
> auxiliary conjectures, mathematical exploration, proof search,
> construction discovery, SAT/CNF encoding, source code, certificate
> generation, checking programs, literature search, and drafting.
> All “independent” or “clean-room” programs described here were also
> AI-assisted and are independent only at the implementation level; they
> are not independent human verification or peer review.  The named
> human authors have [insert the checks actually completed], rerun the
> released artifacts, and accept responsibility for the claims and
> presentation.  The paper proves only the explicitly stated auxiliary
> negative results and does not resolve the Five-Cycle Double Cover
> Conjecture.

The bracketed sentence must describe completed human work, not intended
future work.

## Release recommendation

The repository artifact is suitable for public release now as a
versioned research record with “provisional / requires human review”
status.  An arXiv submission is reasonable after the portable replay,
human rerun, and specialist novelty checks above.  A journal submission
is premature until those checks are complete.

The order-144 result should not be announced as a FiveCDC breakthrough.
A precise public summary would be:

> We found and certificate-checked a cyclically-four, girth-five
> countermodel to a specific binary Fano-flow repair strategy.  The same
> graph has an explicit five-cycle double cover, and the Five-Cycle
> Double Cover Conjecture remains open.
