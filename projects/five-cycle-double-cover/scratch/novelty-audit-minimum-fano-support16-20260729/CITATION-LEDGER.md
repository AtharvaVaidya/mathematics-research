# Bounded novelty and prior-art audit

Date: 2026-07-29

Objects audited:

1. `preprint-minimum-fano-projection/main.tex`;
2. `support16-residual-fourterminal-matching-game-20260729/`.

## Bottom line

The material does **not** resolve the Five-Cycle Double Cover Conjecture.
Hušek--Šámal still state FiveCDC as open and give the immediate
\(\mathbb F_2^3\)-flow/component-parity criterion on which the manuscript
builds.  The July 2026 Cycle Double Cover theorem supplies eight labelled
even subgraphs, not five.

The strongest defensible publication description after this bounded screen
is:

> An AI-assisted, provisional working preprint containing apparently new
> partial structural and exact finite results about the Hušek--Šámal
> FiveCDC flow criterion, plus explicit counterexamples to several natural
> proof strategies.  Priority has not been established.

Do not call the manuscript a proof, disproof, or resolution of FiveCDC.  Do
not use “first”, “novel”, or “new” without the qualifiers “apparently” and
“after a bounded search”.  The support-16 matching package is a useful
exact supplement, not a FiveCDC counterexample and not a theorem about
globally minimum projections.

This audit used primary papers, author manuscripts, and arXiv preprints.  It
did not include a systematic MathSciNet/Zentralblatt citation search, a
complete review of the Celmins and Preissmann theses, or consultation with a
human specialist.  “No exact match found” therefore means **unverified**,
not “proved new”.

## Classification key

- **KNOWN**: the same mathematical content was located in a primary source,
  or it is a standard named theorem used in the project.
- **STRAIGHTFORWARD COROLLARY**: a short deduction/reformulation from known
  material; exact prior wording was not necessarily located, but it should
  not be marketed as a priority result.
- **APPARENTLY NEW (BOUNDED SCREEN)**: no exact prior theorem was found, and
  the result is sufficiently project-specific that provisional circulation
  as an original contribution is reasonable.
- **UNVERIFIED / OVERLAP RISK**: no exact match was found, but close
  literature or incomplete searching makes a priority label unsafe.

## Citation ledger: foundations and manuscript results

| Candidate claim | Classification | Primary overlap and conservative assessment |
|---|---|---|
| FiveCDC means five labelled even subgraphs, with empty subgraphs allowed; hence “at most five” is faithful | **KNOWN** | Hušek--Šámal, Definition 1.2, allow empty even subgraphs and later identify FiveCDC with an 8-CyDC having three empty entries. Zhang (1996) also formulates a \(k\)-CDC as using at most \(k\) cycles/even subgraphs. |
| FiveCDC is still open after the July 2026 ordinary CDC proof | **KNOWN** | Hušek--Šámal state FiveCDC as Conjecture 1.9/3.19. Oum's exposition separates the five-coordinate strengthening from the proved eight-coordinate theorem. |
| A FiveCDC is equivalent to a nowhere-zero \(\mathbb F_2^3\)-flow whose distinguished-coordinate zero support satisfies component parity | **KNOWN** | Hušek--Šámal, Theorem 3.16 and Conjecture 3.19. This is the manuscript's immediate source and must not be claimed as project novelty. |
| Prescribed-cycle/2-regular-subgraph criterion for membership in a 5CDC | **KNOWN** | Hoffmann-Ostenhof (2013), Proposition 0.3. |
| Earlier flow-pair formulations of 5CDC and the distinction from orientable 5CDC | **KNOWN** | Xie--Zhang (2009), Theorem 6.1 and the orientable implications. The public draft should cite this as adjacent prior art even though its variables differ from the Hušek--Šámal criterion. |
| “Fano flow” language for nowhere-zero \(\mathbb Z_2^3\)-flows on cubic graphs | **KNOWN** | Máčajová--Škoviera (2005) and Jin--Mazzuoccolo--Steffen (2016). Their \(k\)-line Fano-flow problems concern which Fano-plane lines occur at vertices; they are not the manuscript's minimum coordinate-support problem. The manuscript should define “Fano projection” explicitly to prevent conflation. |
| Reduction from arbitrary bridgeless multigraphs to loopless cubic multigraphs | **STRAIGHTFORWARD COROLLARY** | Standard-looking vertex-expansion argument, with a complete proof in the manuscript. This bounded screen did not locate the exact loop-handling statement in a primary paper. Treat it as an elementary reduction, not a novelty contribution. The stronger reduction to simple, girth-\(\ge5\), cyclically 4-edge-connected snarks remains **unverified** unless its exact FiveCDC-preserving source/proof is supplied. |
| In a cubic nowhere-zero \(\mathbb F_2^3\)-flow, a fixed nonzero value class is a matching | **KNOWN** | Explicit in the Hušek--Šámal flow setup and immediate from the three distinct nonzero values meeting at a cubic vertex. |
| Minimum-projection exchange theorem; equivalently, each \(h-M_c\) is a shortest \(T_c\)-join in \(G-M_c\) | **STRAIGHTFORWARD COROLLARY** | No exact prior statement found. The proof is a one-cycle toggle of the Hušek--Šámal flow followed by the standard cycle/\(T\)-join correspondence. It is useful framework, but the safest priority language is “elementary optimization consequence of the Hušek--Šámal criterion”. |
| Edmonds--Johnson odd-cut duality for shortest \(T\)-joins | **KNOWN** | Edmonds--Johnson (1973). This primary citation is missing from the current `refs.bib` and should be added before circulation. |
| Zero dual price on quotient shores; \(|E-h|\ge |h|-|M_c|\); \(|h|\le6|V|/7\); equality rigidity | **UNVERIFIED / OVERLAP RISK** | The deduction is project-specific and no exact match was found. It combines standard \(T\)-join duality with the new minimum-projection setup. The density value and Fano-flow terminology are close enough to the short-cycle-cover and Fano-flow literature that specialist review is needed. Provisional phrasing: “a checkable deduction in this framework”, not a priority claim. |
| Flow-resistance bound \(|h|\ge4r_f(G)\) and every support circuit meets all four affine zero classes | **STRAIGHTFORWARD COROLLARY** | Immediate from the four rebased low flows and the exchange inequality. |
| Direct boundary repair / affine cleaning / dual-cut formulations | **APPARENTLY NEW (BOUNDED SCREEN)** | No exact formulation found. These are specialized translations of the Hušek--Šámal criterion into the manuscript's boundary-state language. The underlying linear/XOR duality is standard; only the exact graph-theoretic formulation is provisionally original. |
| Six-map witness-neutralization identity, colour-load inequality, and 40-state neutralization dynamics | **UNVERIFIED / OVERLAP RISK** | No exact match found. The identity is short and project-specific, but switching identities over binary isotropic systems and circuit partitions are a serious overlap risk. The finite dynamics is apparently new as a certificate about this exact counterstate, not a broad theorem. |
| Relative-\(\operatorname{GL}(2,2)\) tensor lemma and universal one-support-circuit cleaning | **UNVERIFIED / OVERLAP RISK** | No exact match found under the searched terminology. Bouchet's isotropic systems and Traldi's interlacement/circuit-partition matrices are close in algebraic flavor. A specialist comparison is required before claiming novelty. The displayed proof is human-checkable and can be circulated without a priority claim. |
| Circuitwise-balanced multi-circuit repair | **STRAIGHTFORWARD COROLLARY** | Direct summation/application of the tensor lemma once that lemma is accepted; its priority stands or falls with the tensor theorem. |
| Petersen two-occurrence boundary and strict deletion for every extension | **APPARENTLY NEW (BOUNDED SCREEN)** | Apparently new as this exact boundary-state theorem. The Petersen graph, its flows, and its possession of a 5CDC are classical and must not be presented as new. |
| Minimum projections are cleanable through support 15 | **APPARENTLY NEW (BOUNDED SCREEN)** | No prior theorem found in this language. This is a finite, heavily certificate-dependent theorem about a framework introduced two days earlier by Hušek--Šámal. It is publishable only with frozen enumerators, complete certificates/hashes, and explicit scope; it is not a general FiveCDC result. |
| Exact size-11 through size-15 residual censuses, including the pairing-robust Kempe reductions | **APPARENTLY NEW (BOUNDED SCREEN)** | The exact counts and residual classifications appear project-specific. “Exact computational classification” is safer than “first classification”. Independent agent implementations are not independent human verification. |
| Loopless two-occurrence clean-or-delete frontier through 18 and loop-allowed frontier through 16 | **APPARENTLY NEW (BOUNDED SCREEN)** | No exact prior result found. Multipole state/parity literature is adjacent, so publication should cite Fiol--Vilaltella and state that the contribution is the exact finite frontier in this boundary system. |
| Full-flow master minimization and cleanliness as a second disjoint join | **STRAIGHTFORWARD COROLLARY** | Best described as an elementary reformulation of the Hušek--Šámal criterion plus shortest-join language, not as a priority theorem. |
| Strict-lock 162-vertex graph with a unique uncleanable minimum projection but an explicit FiveCDC | **APPARENTLY NEW (BOUNDED SCREEN)** | No named prior conjecture/result matching “minimum extendable projection” was found. This is a counterexample to a project-proposed selection strategy only. It does not refute FiveCDC. Publish only with the graph, checker, exact uniqueness certificate, and this narrow wording. |
| Static-filter survivors, inflation theorems, rainbow/load counterstates, and two-round escape examples | **APPARENTLY NEW (BOUNDED SCREEN)** | These appear new as exact failed-approach certificates inside the project. Their publication value is methodological, not a resolution theorem. Conditional inflation must remain labeled conditional. |

## Citation ledger: support-16 four-terminal matching package

| Candidate claim | Classification | Primary overlap and conservative assessment |
|---|---|---|
| A proper 3-edge-colouring is equivalent to a nowhere-zero \(\mathbb F_2^2\)-flow on a cubic graph/multipole, with a parity restriction on semiedge states | **KNOWN** | Standard multipole/Fano-flow language; Fiol--Vilaltella (2015) explicitly develops semiedge states and the Parity Lemma. |
| A two-colour subgraph consists of alternating paths and circuits, and swapping the two colours on a component is a Kempe switch | **KNOWN** | Standard edge-Kempe operation; belcastro--Haas (2012) and Goedgebeur--Östergård (2021) study these switches on cubic graphs. |
| Terminals of a two-colour subgraph in a component are paired by its path components | **STRAIGHTFORWARD COROLLARY** | Immediate from degree parity in the bichromatic subgraph. Multipole literature supplies the boundary-state setting; no special novelty should be claimed for the pairing fact. |
| A matching-independent endpoint set that is a union of pairs in every perfect matching is only \(\varnothing\) or the full terminal set | **STRAIGHTFORWARD COROLLARY** | Elementary one-line matching argument. The consequence that such an action is only a uniform component transposition is likewise elementary. |
| For six of the eight fixed support-16 residuals, \(P=\{1,3\}\) gives a matching-observed strategy robust against every abstract terminal perfect matching | **APPARENTLY NEW (BOUNDED SCREEN)** | No exact or semantically close published theorem was found. This is an exact finite statement about eight project-generated residual words. It should be presented with the full 66-row certificate and checker, not as a general four-terminal theorem. |
| The remaining two \(8+2+2+2+2\) residuals each have one adverse joint matching for every colour pair | **APPARENTLY NEW (BOUNDED SCREEN)** | Exact finite obstruction inside the stated one-round game. The quantifier order \(\exists P\,\forall M\,\exists S(M)\) is essential and should be displayed in any publication. |
| Both adverse triples are simultaneously realized by simple connected bridgeless cubic 42-vertex graphs | **APPARENTLY NEW (BOUNDED SCREEN)** | Apparently new as two explicit realizations of this project-specific obstruction. They are Tait-colourable, their displayed size-16 projection is not globally minimum, and they are not FiveCDC counterexamples. |
| “One four-terminal path choice cannot finish the size-16 minimum-projection case” | **UNVERIFIED / TOO STRONG AS STATED** | The package defeats the precisely encoded one-round, one-colour-pair, support-preserving matching game. It does not exclude multi-round Kempe sequences, support-changing exchanges, or restrictions forced by global minimum. Use the exact game statement, not this informal universal sentence. |

## Primary-source ledger

1. Radek Hušek and Robert Šámal, *Exponentially Many Circuit Double
   Covers*, arXiv:2607.24724v1 (27 July 2026),
   <https://arxiv.org/abs/2607.24724>.  Immediate source for the
   \(\mathbb F_2^3\)-flow/component-parity criterion; explicitly leaves
   FiveCDC open.

2. Sang-il Oum, *A proof of the cycle double cover conjecture by OpenAI:
   An exposition*, arXiv:2607.16356v2,
   <https://arxiv.org/abs/2607.16356>.  Primary exposition of the July
   2026 eight-subgraph result and its separation from the five-subgraph
   conjecture.

3. Jim Geelen, *OpenAI's proof of the Cycle Double Cover Theorem*,
   arXiv:2607.15399, <https://arxiv.org/abs/2607.15399>.

4. Arthur Hoffmann-Ostenhof, *A Note on 5-Cycle Double Covers*, Graphs
   and Combinatorics 29 (2013), 977--979,
   <https://arxiv.org/abs/1209.0096> and
   <https://doi.org/10.1007/s00373-012-1169-8>.

5. Cun-Quan Zhang, *Nowhere-zero 4-flows and cycle double covers*,
   Discrete Mathematics 154 (1996), 245--253, author PDF
   <https://math.wvu.edu/~cqzhang/Publication-files/my-paper/DM-1996-5CDC.pdf>.
   Gives earlier necessary-and-sufficient flow formulations and the
   standard “at most \(k\)” convention.

6. Dezheng Xie and Cun-Quan Zhang, *Flows, flow-pair covers and cycle
   double covers*, Discrete Mathematics 309 (2009), 4682--4689,
   <https://doi.org/10.1016/j.disc.2008.05.056>, author PDF
   <https://math.wvu.edu/~cqzhang/Publication-files/my-paper/DM-2009-Xie-flow-cover.pdf>.
   Theorem 6.1 relates a \((4,4)\)-flow even-disjoint-pair-cover to 5CDC
   and treats orientable 5CDC separately.

7. Edita Máčajová and Martin Škoviera, *Fano colourings of cubic graphs
   and the Fulkerson Conjecture*, Theoretical Computer Science 349
   (2005), 112--120,
   <https://doi.org/10.1016/j.tcs.2005.09.034>.

8. Ligang Jin, Giuseppe Mazzuoccolo, and Eckhard Steffen, *Cores, joins
   and the Fano-flow conjectures*, arXiv:1601.05762,
   <https://arxiv.org/abs/1601.05762>.  Useful terminological and
   conceptual separation from minimum coordinate support.

9. Edita Máčajová, André Raspaud, Michael Tarsi, and Xuding Zhu, *Short
   cycle covers of graphs and nowhere-zero flows*, Journal of Graph
   Theory 68 (2011), 340--348,
   <https://doi.org/10.1002/jgt.20563>.  Adjacent Fano-flow/density and
   shortest-cycle-cover literature.

10. Jack Edmonds and Ellis L. Johnson, *Matching, Euler tours and the
    Chinese postman*, Mathematical Programming 5 (1973), 88--124,
    <https://doi.org/10.1007/BF01580113>, accessible author-era PDF
    <https://web.eecs.umich.edu/~pettie/matching/Edmonds-Johnson-chinese-postman.pdf>.
    Source for the \(T\)-join polyhedral machinery.

11. Siyan Liu, Rong-Xia Hao, Rong Luo, and Cun-Quan Zhang, *5-Cycle
    Double Covers, 4-Flows, and Catlin Reduction*, SIAM Journal on
    Discrete Mathematics 37 (2023), 253--267,
    <https://doi.org/10.1137/22M1472425>.  Important adjacent 4-flow,
    superposition, and snark-family literature; no exact
    minimum-projection theorem was located there.

12. M. A. Fiol and J. Vilaltella, *Some results on the structure of
    multipoles in the study of snarks*, Electronic Journal of
    Combinatorics 22 (2015), P1.45,
    <https://arxiv.org/abs/1308.0480> and
    <https://doi.org/10.37236/3629>.

13. sarah-marie belcastro and Ruth Haas, *Counting
    edge-Kempe-equivalence classes for 3-edge-colored cubic graphs*,
    arXiv:1209.1730, <https://arxiv.org/abs/1209.1730>.

14. Jan Goedgebeur and Patric R. J. Östergård, *Switching
    3-edge-colorings of cubic graphs*, arXiv:2105.01363,
    <https://arxiv.org/abs/2105.01363>.

15. André Bouchet, *Isotropic Systems*, European Journal of
    Combinatorics 8 (1987), 231--244,
    <https://doi.org/10.1016/S0195-6698(87)80027-6>.

16. Lorenzo Traldi, *Interlacement in 4-regular graphs: a new approach
    using nonsymmetric matrices*, arXiv:1204.0482,
    <https://arxiv.org/abs/1204.0482>; and *Circuit partitions and
    signed interlacement in 4-regular graphs*, arXiv:1607.04233,
    <https://arxiv.org/abs/1607.04233>.  These are the main identified
    overlap risks for the tensor/switching algebra, not evidence of an
    exact duplicate.

## Exact search log

Searches were run on 2026-07-29 using web/arXiv search, primary journal
landing pages, author-hosted PDFs, and reference chains in the primary
papers above.  Exact queries included:

```text
site:arxiv.org "minimum extendable projection" graph
site:arxiv.org "Fano projection" "cycle double cover"
site:arxiv.org "component-parity" "five-cycle double cover"
site:arxiv.org "componentwise" "GL(2,2)" graph flow
five cycle double cover conjecture nowhere-zero F2^3 flow component parity
"Exponentially Many Circuit Double Covers" Hušek Šámal
"A Note on 5-Cycle Double Covers" Hoffmann-Ostenhof
cycle double cover five even subgraphs Fano flow
"minimum support" nowhere-zero "Z_2^3" flow graph
"minimum support" nowhere-zero flow cycle double cover
"support" "5-cycle double cover" flow
"Fano flow" cycle double cover
site:arxiv.org graph circuit partition interlacement isotropic system GL(2,2) local maps
site:arxiv.org Bouchet isotropic systems Euler circuits circuit partitions PDF
site:arxiv.org cubic graph multipole parity lemma bichromatic paths terminals perfect matching
site:arxiv.org edge Kempe equivalence cubic graphs belcastro Haas
André Bouchet isotropic systems European Journal Combinatorics 1987 PDF
Lorenzo Traldi circuit partitions interlacement graph linear algebra PDF
cubic multipoles parity lemma Fiol Vilaltella PDF
bichromatic paths boundary terminals cubic multipole edge coloring
5-cycle double cover conjecture reduction cubic graph snark cyclically 4-edge-connected primary paper
site:arxiv.org "5-cycle double cover" snark reduction
"minimal counterexample" "5-cycle double cover" cubic
"5-cycle double cover" "cyclically 4-edge-connected"
"four-terminal matching game" graph Kempe
"matching-observed" Kempe graph
"one-colour-pair" Kempe matching
"relative GL(2,2)" graph circuit
"flow even-disjoint-pair-cover" Xie Zhang 2009
"(4, 4)-flow even-disjoint-pair-cover"
"even-disjoint-pair-cover" cycle double cover
```

The first four exact-phrase queries, all four support/minimum queries, and
all four exact matching-game/tensor queries returned no mathematical match.
This is evidence only that the project's terminology is not already common;
it does not exclude equivalent results under different language.

## Publication gate

Public circulation as a working preprint is defensible if all of the
following are done:

1. Lead with “FiveCDC remains open; this is a partial result.”
2. Add the missing Edmonds--Johnson, Fano-flow, flow-pair, multipole, and
   2023 Catlin-reduction citations.
3. Keep the orientable conjecture in a separate paragraph and do not infer
   an orientable result from the standard formulation.
4. Attach frozen source, inputs, certificates, hashes, and exact run
   instructions for every finite theorem.
5. Replace “independently verified” by “independently reimplemented by
   another AI agent” wherever that is the actual provenance.
6. Preserve the current honest AI-use disclosure and name the human
   director's role.  State that there has been no independent human peer
   review.
7. Obtain a specialist check of the relative-\(\operatorname{GL}(2,2)\)
   tensor theorem against Bouchet/Traldi and of the density theorem against
   Fano-flow/short-cycle-cover literature before formal journal submission.

Recommended support-16 wording:

> For the eight residual boundary states arising in our support-16 census,
> an exact checker proves that six are reduced by a one-colour-pair
> matching-observed Kempe strategy robust to every abstract terminal
> matching.  The other two admit simultaneously realizable adverse
> matchings on simple bridgeless cubic graphs.  These examples obstruct only
> the stated one-round strategy; they are Tait-colourable and are not
> counterexamples to FiveCDC or to the minimum-projection theorem.
