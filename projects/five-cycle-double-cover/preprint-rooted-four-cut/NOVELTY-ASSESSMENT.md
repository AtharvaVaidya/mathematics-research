# Novelty and publication assessment

Date: 2026-07-27.

## Blunt verdict

This package is potentially publishable as a focused structural and
computer-assisted research note after independent human review. It is not a
proof or disproof of the Five-Cycle Double Cover Conjecture, and it should
not be promoted as one.

The strongest paper-level content is the combination of:

- a human-checkable four-mark circuit theorem and forbidden-edge cut gate;
- exact fixed-five rooted factorization, cycle-switch, and coordinate-cut
  certificates;
- the two-solver rooted base-pair census through order 17; and
- the two-solver full fixed-five boundary census for the cyclically
  4-edge-connected order-22 cap slice.

The order-22 universally-separated-matching census is also exact and useful,
but it is diagnostic evidence rather than progress that closes the
conjecture.

A specialist editor may prefer two shorter papers: one on the marked-circuit
theorems and one on fixed-five rooted signatures and their finite frontiers.
The present combined draft is defensible as a research report, but its
themes are broad.

## What is prior

The following must not be claimed as new:

- the definition of a \(k\)-cycle double cover as at most \(k\) Eulerian
  subgraphs covering every edge twice;
- padding with empty Eulerian subgraphs;
- the ten two-subset edge labels and the `CDC-colouring` viewpoint;
- standard nowhere-zero-flow and quadratic-form background;
- the published four-pole boundary types and exceptional type sets;
- Kempe switching, prescribed-edge cycle results, and cubic
  three-cut decomposition; and
- the distinction between standard and orientable Five-CDC.

The closest direct overlap is E. Máčajová, G. Mazzuoccolo, and G. Tabarelli,
“Cycle separating cuts in possible counterexamples to the cycle double
cover and the Berge--Fulkerson conjectures,” *Ars Mathematica
Contemporanea* 26 (2026), #P2.03,
<https://doi.org/10.26493/1855-3974.3409.c13>. Their relation allows an
unbounded colour universe. The signatures classified by this package are
strictly the fixed-five \(D_5\) signatures \(\mathcal C_5\); the finite
computations do not classify the published arbitrary-colour relation.

Other close ingredients are Knappe--Pitz on circuits through prescribed
edges, Aldred--Ellingham--Hemminger--Holton on cycles in quasi
4-connected graphs, and the cubic decomposition results of
Nedela--Seifrtová--Škoviera and Pastor. The elliptic model
\(q=e_2\) on the even subspace of \(\mathbb F_2^5\) is an elementary
repackaging of the ten-label model, not a headline novelty claim.

## What appears new, provisionally

Targeted searches found no prior use of the exact rooted
three-pole/base-pair factorization developed here and no prior version of
the order-17 or order-22 fixed-five frontier computations. Subject to a
specialist priority search, the following appear new to the authors:

- the exact factorization of the surviving fixed-five cyclic-three
  interface into rooted signatures;
- the cycle-translation blocker theorem and its
  \(K_{1,4}\)/non-bipartite support classification;
- the complement-cycle/base-pair cut certificate;
- the constructive Tait-cap closure theorem, which turns a Tait colouring
  and any proper root cycle into one complete rooted base pair;
- the companion path-rooted fork-triple induction, conditional on
  triangle-free base-pair closure and not on the unfinished finite screen;
- the finite theorem that every nonempty nonbridge rooted signature through
  order 17 contains a base pair;
- the full-ten-type theorem for all 14,322 independent-edge deletion poles
  in the 31 cyclically 4-edge-connected non-Tait order-22 caps; and
- the exact order-22 universally-separated four-mark census.

“Appears new to the authors” is the strongest responsible wording. The
closest four-pole paper is very recent, and absence searches—especially a
zero-citation database result—are weak evidence of priority.

The four-mark core theorem and forbidden-edge gate may also be new in their
exact hypotheses, but their ingredients are published and elementary. Their
novelty is the combination, not a new general cycle theorem.

The Tait-cap theorem is also elementary once its two cycle translations are
seen. Its responsible novelty claim is the exact rooted formulation and
exceptional-interface consequence, not the underlying Tait-colouring or
cycle-switch ideas. A hostile audit disproved the initially stronger
one-sided consequence: base-pair containment does not exclude the mixed
\(\{\mathsf E,\mathsf I\}\) relation. The corrected statement is what the
manuscript claims. A global order-28 lower bound that depended on the false
inference has been withdrawn. The later cap-connectivity repair is elementary:
bridgelessness plus absence of a cyclic two-edge cut forces a simple cubic
cap to be 3-connected. It restores the decomposition premise, not the false
one-sided relation inference.

The fork-triple induction required its own correction during hostile audit.
The statement “at least three labels” is too weak:
\(\{01,02,12\}\) paired with itself has the mixed
equality/intersection relation. The repaired theorem preserves the exact
fork shape \(\{qr,ps,pt\}\). Its common intersectors are only
\(\{pq,pr\}\), which is the structural fact needed for the conditional
mixed-branch reduction. This human reduction appears new provisionally,
but no finite order-28 consequence is claimed until the independent
triangle-free screen is complete.

## What has actually been checked

The manuscript contains complete line-by-line proofs for the structural
claims. The finite claims have independently written decision engines and
matching deterministic transcripts:

- order 17: 654,676 canonical cores, 15,645,623 nonbridge roots, zero
  base-pair violations, and matching digests on all eight shards;
- cyclically-four order-22 cap slice: 31 caps, 14,322 deletion poles,
  143,220 SAT answers per solver, every signature mask `0x3ff`, and
  byte-identical output SHA-256
  `52edd8a189012acefd3565a79d5c58b6f209bbe40156560eb57e2c569fd7c091`;
- separated-mark census: 7,174,735 Tait-colourable order-22 graphs and
  zero separated four-edge matchings by two enumeration methods.

All programs, audits, and “independent” implementations were produced or
reviewed by OpenAI Codex agents under human direction. Agreement between
them is strong internal evidence, not independent human verification.

The larger all-cap order-22 census was incomplete when this package was
frozen. It is deliberately not claimed.

## Minimum bar before public submission

1. A human graph theorist should verify every displayed proof, especially
   the imported theorem hypotheses, fixed-five versus arbitrary-colour
   distinction, rooted gluing, proper-core cut parity, and the corrected
   one-sided versus two-sided Tait-shore distinction.
2. A separate person should reproduce each finite theorem from canonical
   input on an independently provisioned machine and compare retained
   digests.
3. A specialist should search MathSciNet, zbMATH, Scopus, and the recent
   Five-CDC/four-flow literature for equivalent rooted-signature results.
4. The source, exact generator version, raw logs, compressed transcripts,
   and hashes should be archived at a stable DOI.
5. The human author should decide authorship and responsibility under the
   target venue's AI policy and retain the page-one AI disclosure.

Until those steps are complete, the correct label is:

> AI-assisted research draft containing apparently new structural
> reductions and exact finite theorems; no Five-CDC resolution.
