# Bounded novelty audit: six path states and two Blanuša six-poles

Audit date: 2026-07-29.

## Question audited

The precise candidate contribution is the following positive boundary
inclusion, not the duad encoding by itself and not the FiveCDC conjecture.

Let `D` be the ten two-subsets (duads) of `{0,1,2,3,4}`.  Put
`Y={1,2,3,4}`.  For `{a,b}⊂Y`, with `{c,d}=Y-{a,b}`, define

```text
P_ab = {0a, 0b, cd}.
```

Let `P_ord` contain the 36 ordered triples obtained by ordering the members of
the six sets `P_ab`.  For each of two explicit ordered six-poles `A` and `B`
obtained by deleting two vertices from the two 18-vertex Blanuša snarks, let
`R_X ⊆ D^6` be the boundary words that extend to a duad labelling of the
internal edges with xor zero at every internal vertex.

The audited statement is

```text
P_ord × P_ord ⊆ R_A ∩ R_B.
```

Equivalently, all 1,296 ordered concatenations of two path states extend
through each atom.  The saved relation is a positive subrelation; the statement
does not assert that either full `R_X` equals this product.

The associated composition lemma says that any macro duad labelling having
xor zero at junctions and a path state at every connector extends after
arbitrarily matching the connectors, choosing atom `A` or `B` for every pair,
and ordering the ports arbitrarily.

## Search boundary

This was a bounded web and full-text audit, not a systematic MathSciNet or
zbMATH review.  Searches covered combinations of:

```text
five-cycle double cover; 5-CDC; B-flow; Z_2^5; weight-two flow;
multipole state; multipole boundary; circuit double cover multipole;
Blanuša 6-pole; Blanuša six-pole; Petersen coloring; normal edge coloring.
```

Primary journal pages, arXiv records, and accessible paper text were preferred.
The sources below were inspected for an exact statement, equivalent
formulation, or the same explicit atoms.

## Closest literature and exact comparison

| Source | What is already present | Difference from the audited statement |
|---|---|---|
| A. Huck and M. Kochol, “Five cycle double covers of some cubic graphs,” *JCTB* 64 (1995), 119–125 | Sufficient FiveCDC results for cubic graphs, including graphs with a 2-factor having at most two odd components. | No matching six-state duad relation for the two ordered Blanuša six-poles was found. |
| A. Hoffmann-Ostenhof, “A note on 5-cycle double covers,” *Graphs and Combinatorics* 29 (2013), 977–979; [arXiv:1209.0096](https://arxiv.org/abs/1209.0096) | Characterizes when a prescribed 2-regular subgraph belongs to a 5-cycle double cover. | Global prescribed-cycle criterion, not the audited local ordered-boundary inclusion. |
| S. Liu, R.-X. Hao, R. Luo, and C.-Q. Zhang, “5-Cycle Double Covers, 4-Flows, and Catlin Reduction,” *SIAM Journal on Discrete Mathematics* 37 (2023), 253–267; [journal](https://doi.org/10.1137/22M1472425) | Develops sufficient FiveCDC conditions for superpositions using nowhere-zero 4-flows and Catlin reduction, and verifies several snark families. | This is close prior art for the superposition strategy.  In the inspected article metadata and searchable text, no ordered weight-two `F_2^5` six-pole state relation or the two explicit Blanuša atom tables was found. |
| M. A. Fiol and J. Vilaltella, “Some results on the structure of multipoles in the study of snarks,” *EJC* 22(1) (2015), P1.45; [journal](https://doi.org/10.37236/3629) | Defines semiedge states of multipoles, quotients by color permutations, and studies completeness, closure, and reducibility. | The states are boundary restrictions of proper 3-edge-colorings with three colors.  The audited states are ordered triples of weight-two vectors in `F_2^5` for five named even subgraphs. |
| R. Nedela and M. Škoviera, “Decompositions and reductions of snarks,” *JGT* 22 (1996), 253–279; [journal](https://doi.org/10.1002/(SICI)1097-0118(199607)22:3%3C253::AID-JGT6%3E3.0.CO;2-L) | Systematic multipole decompositions and reductions of snarks along edge cuts. | Supplies structural vocabulary and close methodology, but no audited FiveCDC boundary relation was found. |
| R. Hušek and R. Šámal, “Counting circuit double covers,” *JGT* 108 (2025), 374–395; [arXiv:2303.10615](https://arxiv.org/abs/2303.10615) | The closest conceptual prior art.  It defines ordered multipoles, circuit-double-cover boundaries, multiplicity vectors, and linear gluing representations. | Its boundary records identities and pairings of paths in circuit double covers with an unrestricted number of circuits.  The audited boundary fixes five named even subgraphs and records, on each semiedge, exactly the two names containing it.  No six `P_ab` states or Blanuša atom table was found. |
| R. Hušek and R. Šámal, “Homomorphisms of Cayley graphs and Cycle Double Covers,” *EJC* 27(2) (2020), P2.2; [arXiv:1901.03112](https://arxiv.org/abs/1901.03112) | Group-valued flow and Cayley-homomorphism language for cycle double covers, especially the orientable branch. | Related algebraic setting, but not the standard FiveCDC local six-pole extension statement audited here. |
| G. Mazzuoccolo and V. Mkrtchyan, “Normal 6-edge-colorings of some bridgeless cubic graphs,” *Discrete Applied Mathematics* (2020); [arXiv:1903.06043](https://arxiv.org/abs/1903.06043), and F. Pirot, J.-S. Sereni, R. Škrekovski, “Variations on the Petersen colouring conjecture,” *EJC* 27(1) (2020), P1.8; [arXiv:1905.07913](https://arxiv.org/abs/1905.07913) | Five-color/Petersen-coloring and normal-edge-coloring structures on cubic graphs. | Superficially close because the Petersen graph and five colors generate ten incidences.  Their edge labels and local normality condition are not the weight-two `F_2^5` flow condition, and no audited boundary inclusion was found. |
| R. Hušek and R. Šámal, “Exponentially Many Circuit Double Covers,” [arXiv:2607.24724](https://arxiv.org/abs/2607.24724) (submitted 2026-07-27) | Explicitly defines a cycle as an even subgraph, permits empty members in a labelled `k`-CyDC, and gives an equivalent flow/linear-system condition for 5-CyDC. | Confirms that the general encoding is prior art.  No multipole treatment, six path-state set, or Blanuša boundary table was found in the inspected version. |

The elementary equivalence

```text
five labelled even subgraphs covering each edge twice
⇔
an F_2^5-flow whose nonzero edge values have Hamming weight two
```

must therefore be presented as background, not as a novelty claim.

## Result of the audit

No inspected source states the exact inclusion

```text
P_ord × P_ord ⊆ R_A ∩ R_B
```

for the two specified ordered Blanuša-derived six-poles, nor the consequent
all-matchings/all-atom-types/all-port-orders composition lemma.

This supports the classification:

```text
possible local novelty; moderate confidence; not established novelty.
```

The finite cyclically-4 macro census through order 14 also appears to be a new
computational artifact, but the census is evidence for the usefulness of the
lemma, not evidence for the general FiveCDC conjecture.

Reasons confidence is not high:

1. multipole literature is large and uses terminology that varies by author;
2. old theses and unpublished state tables are not reliably indexed;
3. the exact relation may occur as an unremarked computation inside software;
4. no subject-matter expert has yet been asked to check the claim;
5. all current programs, proof tables, and prose were produced by collaborating
   OpenAI Codex agents, so “independent checker” means independent
   implementation, not independent authorship.

## Publication assessment

The result is plausibly suitable for a short computational note or an addendum
to a broader FiveCDC search paper after independent human review.  It is not
currently suitable for announcement as a FiveCDC resolution.

The strongest defensible abstract claim is:

> We give an explicit six-state positive boundary subrelation shared by two
> ordered six-poles obtained from the Blanuša snarks.  It yields a constructive
> composition lemma for a class of cubic expansions.  A solver-free certificate
> verifies all local completion rows, and a canonical census applies the lemma
> to 9,278 junction-set orbits in cyclically 4-edge-connected simple cubic
> macros of order at most 14.

## Human-checkability status

The mathematical implication from the local relation to the composition lemma
is a short ordinary proof included in `preprint.tex`.  The local relation has a
finite proof table: each of 2,592 rows lists 21 internal duads and can be checked
by testing Hamming weight two and vertex xor zero.  The separate verifier
performs exactly those checks and does not call a SAT solver.

This is a checkable computer-assisted proof, not yet a hand derivation reducing
the 2,592 rows to a small list of conceptual cases.  A hand reduction using
atom automorphisms and coordinate symmetries would materially improve a
publication.
