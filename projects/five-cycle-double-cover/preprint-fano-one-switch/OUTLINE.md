# Preprint outline

## Provisional title

**A one-circuit repair conjecture for five-cycle double covers: an exact
countermodel and a finite reconfiguration frontier**

Status: **provisional computational note / no resolution of the five-cycle
double cover conjecture**.

## Proposed abstract

For a nowhere-zero \(\mathbb F_2^3\)-flow \(f\) on a loopless cubic graph,
each nonzero value class
\[
M_k=\{e:f(e)=k\}
\]
is a matching, and quotienting by \(\langle k\rangle\) makes \(M_k\) the
exact zero set of an \(\mathbb F_2^2\)-flow. Combining this observation with
the published matching/four-flow characterization of five-cycle double
covers shows that \(f\) yields a standard five-cycle double cover whenever
some \((G-M_k,\partial M_k)\) packs two edge-disjoint \(T\)-joins. We give a
human-checkable ten-vertex countermodel showing that an arbitrary
\(\mathbb F_2^3\)-flow need not have such a successful value. We then
formulate the surviving connected one-circuit repair conjecture: every
unsuccessful flow on a connected graph has an adjacent successful flow in
the nowhere-zero-flow
reconfiguration graph. This is equivalent to saying that the successful
flows form a dominating set, not that the whole reconfiguration graph is
connected. Exact computation finds no counterexample among all connected
simple bridgeless cubic graphs through order 14, all hard graphs at orders
16 and 18, and all 1,388 hard graphs at order 20. At order 20,
49,752,091 initially unsuccessful representatives among 847,539,220
\(\mathrm{GL}(3,2)\)-orbits are all repairable by one connected-circuit
switch. The universal repair statement remains unproved.

## Exact scoped contributions

1. **A 5CDC-specific reformulation for a supplied three-bit flow.**
   For each \(k\ne0\), the value class \(M_k\) is an exact-zero matching
   after quotienting \(f\) by \(\langle k\rangle\). If its complement packs
   two edge-disjoint \(T\)-joins, the published matching/four-flow
   criterion constructs a standard five-cycle double cover.  Moreover, a
   linear functional taking \(k\) to one gives a binary cycle containing
   \(M_k\), so \(G-M_k\) always has a \(\partial M_k\)-join.  The
   component-parity obstruction for arbitrary exact-zero matchings cannot
   occur for these value classes.

   The four linear functionals \(\lambda\) with \(\lambda(k)=1\) give four
   canonical \(\partial M_k\)-joins.  They double-cover \(G-M_k\), and
   their six pairwise intersections are exactly the other six value
   classes \(M_w\), one per pair.  Include this tetrahedral \(T\)-join
   structure as an elementary proposition; it sharpens the simultaneous
   obstruction that the conjecture must overcome.

2. **An exact circuit-switch law.**
   If \(C\) is a circuit disjoint from \(M_a\), adding \(a\) on \(C\)
   preserves nowhere-zeroness, fixes \(M_a\), and for
   \(b\notin\{0,a\}\) gives
   \[
   M'_b=(M_b-C)\cup(M_{a+b}\cap C).
   \]
   In \(\mathbb F_2^3\), this is exactly one adjacency in the standard
   nowhere-zero-flow reconfiguration graph.

3. **A new candidate conjecture, not a theorem.**
   The successful \(\mathbb F_2^3\)-flows dominate the reconfiguration
   graph of every finite connected bridgeless loopless cubic graph.
   Connectedness cannot be omitted: two disjoint copies of the displayed
   bad-flow countermodel remain bad after any one circuit switch, because
   the untouched component is still bad for every value.

4. **A human-checkable countermodel to a strictly stronger claim.**
   The graph6 graph `ICOef?kF?` has a displayed nowhere-zero
   \(\mathbb F_2^3\)-flow for which all seven value classes fail the
   two-\(T\)-join packing test. The same graph is 3-edge-colourable and has
   an explicit standard five-cycle double cover. It is therefore a
   countermodel only to “every supplied flow already has a successful
   value,” not to 5CDC and not to the one-switch conjecture.

5. **A finite computational frontier.**
   Exact orbit enumeration finds every initially unsuccessful retained
   flow one-switch repairable in the scopes listed below. This is
   computational evidence only.

## Prior work and novelty caveats

- The shell-flow formulation of a five-colourable cycle double cover as an
  \(S_2^5\)-flow is prior work in the Jaeger \(B\)-flow tradition and is
  discussed by Goodall, Garijo, and Nešetřil.

- Hoffmann-Ostenhof’s Corollary 0.6 in *A note on 5-cycle double covers*
  (Graphs and Combinatorics 29 (2013), 977-979,
  [arXiv:1209.0096](https://arxiv.org/abs/1209.0096)) already gives the
  matching/nowhere-zero-4-flow characterization underlying the
  \(T\)-join formulation. The preprint must not claim that characterization
  as new.

- The reconfiguration graph whose flows are adjacent when their difference
  is supported on one circuit is prior work. Cite the current six-author
  version of Esperet, Hendrey, Lagoutte, Marseloo, Norin, and Steiner,
  *Nowhere-zero flow reconfiguration*,
  [arXiv:2512.17342v4](https://arxiv.org/abs/2512.17342v4), and Cranston,
  Li, Su, Wang, and Xu, *Reconfiguration of Nowhere-zero Flows*,
  [arXiv:2606.24685](https://arxiv.org/abs/2606.24685).

- Esperet et al. prove, among other things, that groups of order at least
  six admit no frozen flow in the relevant sense, while their universal
  connectivity result uses \(\mathbb Z_2^8\), not
  \(\mathbb F_2^3\). “Every flow has some neighbour” is much weaker than
  “every unsuccessful flow has a successful neighbour.”

- Cranston et al. develop flow-connectedness, reductions, and results for
  several groups and graph classes. Their terminology and adjacency are
  not new here. No 5CDC-specific dominating-set theorem was found in the
  audited versions.

- The potentially new items are narrowly limited to the successful-value
  target inside the reconfiguration graph, the domination conjecture, the
  exact countermodel to the stronger supplied-flow claim, and the stated
  finite census. This novelty judgment is provisional. Before submission,
  a human expert should search independently and contact the authors of the
  two 2025-2026 reconfiguration preprints.

## Theorem and conjecture labels

### Proposition 1 — Value classes are exact-zero matchings

Let \(G\) be loopless and cubic and let
\[
f:E(G)\to\mathbb F_2^3\setminus\{0\}
\]
be a flow. For every \(k\ne0\), \(M_k=f^{-1}(k)\) is a matching, and the
quotient flow \(E(G)\to\mathbb F_2^3/\langle k\rangle\cong\mathbb F_2^2\)
has exact zero set \(M_k\).

Label this as an elementary proposition, not as the paper’s main novelty.
Add the following consequence to its proof.  Choose a linear functional
\(\lambda_k\) with \(\lambda_k(k)=1\).  The support of
\(\lambda_k\circ f\) is a binary cycle containing \(M_k\); after deleting
\(M_k\), it is a \(\partial M_k\)-join in \(G-M_k\).  Thus every component
of \(G-M_k\) contains an even number of terminals, and every nonpacking
value class lies in the odd-\(K_{2,3}\) graft-minor branch of the published
packing theorem.

### Proposition 2 — Successful value implies a standard 5CDC

If, for some \(k\ne0\), the graft
\((G-M_k,\partial M_k)\) packs two edge-disjoint \(T\)-joins, then \(G\)
has a standard five-cycle double cover.

The proof should be self-contained but explicitly identify
Hoffmann-Ostenhof’s Corollary 0.6 as prior.

### Lemma 3 — Exact one-circuit exchange

For \(a\ne0\) and a circuit \(C\cap M_a=\varnothing\), the switch
\[
f'(e)=
\begin{cases}
f(e)+a,&e\in C,\\
f(e),&e\notin C
\end{cases}
\]
is a nowhere-zero flow and obeys the displayed value-class exchange law.

### Conjecture 4 — One-circuit repair

If a nowhere-zero \(\mathbb F_2^3\)-flow on a finite connected bridgeless
loopless cubic graph has no successful value, then one valid circuit switch
produces a flow with a successful value.

Equivalent reconfiguration wording: the successful flows form a dominating
set. Do not call this a proved theorem.

The paper should immediately note why connectedness is necessary.  In a
disjoint union, two-\(T\)-join packing holds for a value class exactly when
it holds in every component.  Two copies of Theorem 6's bad-flow instance
are therefore bad, and a circuit switch changes only one component.  The
other component blocks every value after the switch.

### Conditional Corollary 5 — Implication for 5CDC

If Conjecture 4 holds for all finite connected bridgeless loopless cubic
graphs, then all finite bridgeless graphs have standard five-cycle double
covers after reducing and solving each connected component. The proof uses the
classical existence of a nowhere-zero group flow of order eight on a
bridgeless graph, then Proposition 2 before or after the single repair.

This is a conditional implication only. Any reduction from the cubic
formulation to arbitrary finite bridgeless graphs must be cited precisely
or proved separately; it should not be silently asserted.

### Theorem 6 — Countermodel to the every-flow value-class claim

The displayed ten-vertex graph and flow have no successful value class,
although the graph has an explicit standard five-cycle double cover.

This theorem has a complete finite proof independent of SAT.

### Computational Result 7 — Retained frontier

The retained programs report no switch-local unsuccessful flow in the
specified finite scopes. Label the statement “Computational Result,”
conditional on correct execution and artifact integrity, rather than a
mathematical theorem proved solely in the text.

## Human-checkable proof plan

### Proposition 1

At a cubic vertex, the three incident nonzero values sum to zero. No two
can agree, because the third would then be zero. Hence each value occurs at
most once at a vertex, proving that \(M_k\) is a matching. In the quotient
by \(\langle k\rangle=\{0,k\}\), an edge maps to zero exactly when its
original value is \(k\), because the original flow is nowhere zero.

### Proposition 2

1. Put \(T=\partial M_k\).
2. From two edge-disjoint \(T\)-joins \(J_1,J_2\subseteq G-M_k\), form the
   binary cycles
   \[
   A=M_k\dot\cup J_1,\qquad B=M_k\dot\cup J_2.
   \]
   Their intersection is exactly \(M_k\).
3. The quotient flow is nowhere zero on \(G-M_k\), so \(G-M_k\) has a
   nowhere-zero 4-flow.
4. Give the standard explicit lift showing that
   \(A\triangle B\) is one coordinate of a 4-cycle double cover of
   \(G-M_k\): represent the three nonzero \(\mathbb F_2^2\) values by
   \(1100,1010,0110\), add \(1111\) according to the binary cycle
   \(1_{A\triangle B}+\ell\circ\phi\), and read the four coordinates.
5. Replace the \(A\triangle B\) coordinate by \(A,B\). The resulting five
   binary cycles cover \(M_k\) twice and every other edge twice.

### Lemma 3 and the reconfiguration identification

Adding a constant on a binary circuit preserves conservation. The only
way to create a zero is to switch an edge previously valued \(a\), excluded
by \(C\cap M_a=\varnothing\). Check the value-class identity edge by edge.
If two \(\mathbb F_2^3\)-flows differ only on a connected circuit, flow
conservation at each degree-two circuit vertex forces the difference to be
constant around the circuit. Thus these switches are exactly the
adjacencies already used in the cited reconfiguration papers.

### Conditional Corollary 5

Start from a nowhere-zero \(\mathbb F_2^3\)-flow. If it has a successful
value, apply Proposition 2. Otherwise apply Conjecture 4 once, then apply
Proposition 2. No iteration, termination measure, or connectivity of the
whole reconfiguration graph is assumed.

### Theorem 6

Use the fifteen-edge incidence/value table frozen in
`search/fano-value-class-flow-countermodel-20260726/HUMAN-PROOF.md`.

1. Cubicity is immediate from the table. The Hamilton circuit
   \[
   0,3,6,1,4,9,5,8,2,7,0
   \]
   proves connectedness and puts every Hamilton edge on a circuit; every
   remaining chord lies on a circuit with one Hamilton path, so the graph
   is bridgeless.
2. At vertices \(0,\ldots,9\), check the incident triples
   \[
   (7,6,1),(7,3,4),(6,5,3),(7,5,2),(7,1,6),
   (6,2,4),(6,3,5),(1,4,5),(3,1,2),(2,6,4).
   \]
   Each has xor zero.
3. List the seven value classes
   \[
   \begin{array}{c|c}
   1:\{2,11\}&2:\{10,13\}\\
   3:\{4,8\}&4:\{5,14\}\\
   5:\{7,9\}&6:\{1,6,12\}\\
   7:\{0,3\}.
   \end{array}
   \]
   Their endpoints are pairwise distinct within each row.
4. Prove the even-marked-circuit criterion: two disjoint \(T\)-joins are
   equivalent to a binary cycle containing all terminals with an even
   number of terminals in each circuit component.
5. For each value class, fix the matching edges to zero and the other two
   incident edges at every terminal to one in the binary-cycle equations.
   Include the reduced systems. For values 1 and 3 the system has a unique
   solution; for value 2 it has affine dimension one; for values 4-7 it
   contains \(0=1\). The three surviving circuit decompositions all have
   terminal counts \(1,3\), so none satisfies the criterion. This is a
   compact human certificate of all seven failures.
6. Verify the displayed proper 3-edge-colouring. The three unions of two
   colour classes are Eulerian and cover every edge twice; append two empty
   members. This proves directly that the graph is not a 5CDC
   counterexample.

The independent checker literally enumerates all \(T\)-joins, but the
paper’s proof must not depend on trusting that program.

## Computational verification scope

| graph scope | \(\mathrm{GL}(3,2)\)-orbit representatives | initially unsuccessful | repaired in one switch | switch-local bad |
|---|---:|---:|---:|---:|
| all connected simple bridgeless cubic graphs, orders 4-10 | 3,295 | 5 | 5 | 0 |
| all such graphs, order 12 | 73,152 | 304 | 304 | 0 |
| all such graphs, order 14 | 2,216,590 | 18,152 | 18,152 | 0 |
| all 26 hard graphs, order 16 | 600,440 | 10,413 | 10,413 | 0 |
| all 179 hard graphs, order 18 | 21,324,510 | 757,221 | 757,221 | 0 |
| all 1,388 hard graphs, order 20 | 847,539,220 | 49,752,091 | 49,752,091 | 0 |

Artifact directories:

- `search/fano-value-class-flow-countermodel-20260726/`
- `search/fano-flow-one-switch-frontier-20260726/`

Required verification commands:

```sh
(cd search/fano-value-class-flow-countermodel-20260726 && \
  python3 independent_checker.py && shasum -a 256 -c SHA256SUMS)

(cd search/fano-flow-one-switch-frontier-20260726 && \
  python3 verify.py && shasum -a 256 -c SHA256SUMS)
```

The frontier has these strengths:

- complete canonical graph scopes through order 14;
- exact \(\mathrm{GL}(3,2)\)-orbit normalization for the unsuccessful-flow
  question;
- a separately written C++ implementation matching the full Python
  order-14 totals;
- complete C++ runs on all 1,388 retained hard order-20 graphs; and
- a second order-20 run restricting switches to connected circuits, with
  the same repair count.

## Computational limitations

- The universal one-circuit conjecture is not proved by any finite run.
- Orders 16, 18, and 20 include only hard
  (connected, simple, bridgeless, cubic, non-3-edge-colourable) graphs, not
  every bridgeless cubic graph. This matters because the countermodel to
  the stronger every-flow claim is itself 3-edge-colourable.
- The Python verifier checks all frozen aggregate identities and
  reconstructs the first bad-flow repair on 432 graph rows, but it does
  not independently re-enumerate every order-16, order-18, or order-20
  flow orbit.
- The C++ order-20 run is an independently written producer, not a formal
  proof certificate for 847,539,220 separate orbit decisions.
- No complete archive of per-flow witnesses is retained.
- The computation concerns the standard, unoriented five-cycle double
  cover problem only.

## Proposed paper structure

1. Introduction and non-resolution statement.
2. Prior 5CDC and flow-reconfiguration formulations.
3. Exact-zero value classes and the two-\(T\)-join criterion.
4. Circuit switches and the domination conjecture.
5. Human-checkable countermodel to the every-flow claim.
6. Exact finite search, symmetry quotient, and independent checks.
7. Limitations and the remaining simultaneous exchange obstruction.
8. Reproducibility statement.
9. AI-use statement.

## Publication recommendation

The combination is defensible as an arXiv computational note after an
independent human rerun and expert novelty review. The human theorem is a
small but exact countermodel; the main positive statement is still a
conjecture, while the large finite frontier is the substantive evidence.
A conventional graph-theory journal is likely to require either a
structural theorem proving the conjecture for a nontrivial infinite class
or a more independently certified exhaustive computation.

## Explicit AI-use disclosure for page 1

> **AI-assistance disclosure.** OpenAI Codex agents (GPT-5-series models)
> proposed the successful-value and one-circuit-repair formulations, wrote
> the producer and checking programs, performed the computational searches
> and literature audit, found the ten-vertex countermodel, and drafted
> substantial portions of this manuscript under human direction. The
> independent checker and the separately written C++ implementation were
> also AI-assisted and must not be described as independent human
> verification. The universal one-circuit repair statement is unproved,
> the finite searches do not resolve the five-cycle double cover
> conjecture, and no human author or referee is represented as having
> certified the full computation. A public submission should retain this
> disclosure and name only human authors who independently check the
> proofs, rerun the computation, verify the literature attribution, and
> accept normal scholarly responsibility.
