# Publication assessment

## Bottom line

This package is potentially worth circulating as a **working computational
research note**, but it is not yet ready to present as a resolved conjecture
or as established journal-level novelty.

The strongest publishable-looking content is:

- the order-sharp 12-vertex delimiter for graph-dependent full
  triangle-state compression, including state transport and a positive
  control that needs different local permutations at repeated state `012`;
- the exact coloured-surface realization of \(D_5\)-flows;
- the permutation formula for the Euler-characteristic change under one
  component switch;
- the cubic \(D_4\) trap theorem explaining why the degree-four
  reconfiguration trap cannot lift unchanged;
- the explicit four-coordinate generalized-switch orbit trap, which closes a
  natural contraction/reconfiguration strategy; and
- the human-checkable fixed-five reduction and rooted edge-insertion
  equivalence, which isolate an exact sufficient edge-extension premise;
- the explicit Tait formula and insertion adaptation, with its existence
  conclusion correctly identified as a special case of known 4-CDC work;
- the linear rooted-transition characterization and its exact native-XOR
  and certificate-producing CNF formulations;
- the human-checkable internal/external typed-port gluing lemma and
  double-star corollary;
- the complete 138,144-interface typed-cap census through order 14, stated
  with the limitation that the independent full replay stops at order 10;
- the complete order-14 terminal-plateau census and fixed-distance descent
  census; and
- the complete 195-edge elimination screen on a 130-vertex cyclically
  4-edge-connected girth-ten graph.

The broad embedding dictionary is established background, not a contribution
that should be advertised as new. The exact combination with proper
five-colour \(D_5\) data, the switch formula, the rooted reduction, and the
finite censuses may be new.  The rooted equivalence itself is elementary and
should not be called deep merely because it identifies the right frontier.
The triangle-state transport theorem may be new, but only a bounded source
audit has been performed.  The universal typed-cap double-star premise is
open; its order-14 frontier is evidence, not a reduction theorem.
No categorical novelty claim is justified until a specialist prior-art
review is complete.

## Literature checked for this draft

- Sang-il Oum, *A Proof of the Cycle Double Cover Conjecture by OpenAI: An
  Exposition*, arXiv:2607.16356v2. Section 9 defines a \(k\)-CDC as at most
  \(k\) Eulerian subgraphs, records the 8-CDC theorem, and retains FiveCDC as
  Conjecture 18; it states the orientable version separately as Conjecture 19.
- S. Liu, R.-X. Hao, R. Luo, and C.-Q. Zhang, *5-Cycle Double Covers,
  4-Flows, and Catlin Reduction*, SIAM J. Discrete Math. 37 (2023), 253-267.
- S. Liu, R.-X. Hao, R. Luo, and C.-Q. Zhang, *Five-Cycle Double Cover and
  Shortest Cycle Cover*, J. Graph Theory 108 (2025), 39-49.
- R. Hušek and R. Šámal, *Exponentially Many Circuit Double Covers*,
  arXiv:2607.24724v1.  Theorem 3.16 and Conjecture 3.19 give current
  unrooted flow-only context; they do not turn the rooted transition
  certificate or typed-cap premise into a FiveCDC theorem.
- D. Král', E. Máčajová, O. Pangrác, A. Raspaud, J.-S. Sereni, and
  M. Škoviera, *Projective, Affine, and Abelian Colorings of Cubic Graphs*,
  European J. Combin. 30 (2009), 53-69.  Configuration homomorphisms and
  the Desargues/FiveCDC equivalence are prior art, not contributions of this
  note.
- B. Ghanbari and R. Šámal, *Facial Diagrams and Cycle Double Cover*,
  arXiv:2605.01410, which studies embeddings and twist operations in the CDC
  setting.
- B. Ghanbari and R. Šámal, *Approximate Cycle Double Cover*,
  arXiv:2511.07285, which explicitly states the cubic CDC in terms of
  embeddings without singular edges.
- P. A. Catlin, *Embedded Graphs, Facial Colorings, and Double Cycle Covers*,
  in *Topics in Combinatorics and Graph Theory* (1990), 185-192,
  DOI 10.1007/978-3-642-46908-4_21.
- B. Mohar and C. Thomassen, *Graphs on Surfaces* (2001), and C.-Q. Zhang,
  *Circuit Double Cover of Graphs* (2012), as standard background.
- A. Hoffmann-Ostenhof, *A Note on 5-Cycle Double Covers*, Graphs and
  Combinatorics 29 (2013), 977--979.  Lemma 0.2 records the stronger known
  fact that any prescribed 2-regular subgraph of a cubic subdivision with a
  nowhere-zero 4-flow belongs to a 4-CDC.  Accordingly, the Tait
  prescribed-circuit existence result in this note is not claimed as new.

This is a targeted check, not a systematic prior-art review.

## Before public submission

1. Have a graph theorist independently check every ordinary proof.
2. Search specifically for coloured crystallizations, edge-coloured
   triangulations, transition systems, and permutation formulas for
   split/merge changes under Kempe switches.
3. Obtain a genuinely independent full implementation of the order-14
   terminal-plateau census, not only focused semantic verification of the
   frozen report.
4. Obtain a second full implementation of the order-12 and order-14
   typed-cap frontier; the current independent Python replay ends at order
   10.
5. Search specifically for prior typed multipole signatures, local
   transition-boundary connectivity encodings, and triangle-state transport
   criteria.
6. Archive exact source, reports, `geng` version, compiler version, and
   checksums at an immutable commit or DOI.
7. Decide whether the note should lead with the exact switch formula, the
   reconfiguration counterexample, or the rooted edge-extension reduction;
   each is more defensible than positive finite evidence alone.
8. Retain the full AI-use disclosure and comply with the target venue's
   authorship and AI policies.

Until those steps are complete, the accurate label is:

> Research note for independent verification; FiveCDC remains unresolved.
