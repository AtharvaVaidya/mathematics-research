# FiveCDC rooted resolution frontier

Date: **2026-07-28**

Status: **NO PROOF OR DISPROOF OF THE FIVE-CYCLE DOUBLE COVER
CONJECTURE.**

This note records the exact human-checkable implication now proved, the
smallest remaining premise, and the computational evidence.  It concerns
the standard, unoriented conjecture.  “Five” means “at most five”:
empty Eulerian members may be appended.

## 1. Exact formulation

Let
\[
 D_5=\binom{[5]}2\subseteq\mathbb F_2^5.
\]
A \(D_5\)-flow on a loopless cubic graph \(G\) labels every edge by a
weight-two vector and has xor zero at every vertex.  It is exactly a
five-even-subgraph double cover: coordinate \(i\) selects the Eulerian
edge set \(C_i\), and every edge lies in its two label coordinates.

For \(P=\{i,j\}\), put
\[
 Y_P=\{e:|q(e)\cap P|=1\}.
\]
Each \(Y_P\) is even, and its nonempty components are circuits.

## 2. The proved conditional implication

Let \(H\) be cubic with independent edges \(r,s\).  Subdivide \(r,s\)
with new vertices \(u,v\) and add \(e=uv\), producing \(G\).

> **Edge-adapted insertion equivalence.**  The graph \(H\) has a
> \(D_5\)-flow in which one factor circuit contains \(r,s\) if and only
> if \(G\) has a \(D_5\)-flow \(q\) in which \(u,v\) lie on one
> component of \(Y_{q(e)}(q)\).

For the forward direction, transpose the two coordinates of the common
factor on one open \(u\)-to-\(v\) arc and label \(e\) by that coordinate
pair.  For the reverse direction, transpose on one open factor arc,
delete \(e\), and suppress \(u,v\).  The endpoint labels become equal.
Every internal vertex sees two identical xor changes and each endpoint
defect is exactly cancelled by the inserted or deleted edge.

The fixed-five minimum-counterexample reductions have also been written
out.  A minimum counterexample may be taken simple, cubic, cyclically
4-edge-connected, non-3-edge-colourable, and, by Huck's theorem, of
girth at least ten.  Eliminating any edge produces a smaller simple
3-edge-connected cubic graph \(H\) with independent roots \(r,s\).
Moreover:

- \(g(H)\geq8\);
- every 8-circuit of \(H\) contains both roots;
- every 9-circuit contains at least one root.

Therefore FiveCDC follows from the following exact premise:

> **Remaining rooted premise.**  Every simple 3-edge-connected cubic
> graph \(H\) with the preceding root-specific short-cycle geometry,
> if it has any \(D_5\)-flow, has some \(D_5\)-flow with \(r,s\) on one
> factor circuit.

This premise is unproved.  The insertion equivalence shows that it is a
precise edge-extension form of the original difficulty, not a solved
local lemma.

There is also an exact matching form.  Root-goodness is equivalent to a
matching \(M\) avoiding the roots, a nowhere-zero 4-flow on \(H-M\), and
two edge-disjoint \(T\)-joins for \(T=V(M)\) whose union has one
component containing both roots.  The full forward and reverse proof is
`scratch/d5-root-good-matching-fourflow-characterization.md`.

Human proofs and the hostile audit are in:

- `scratch/d5-independent-root-feasibility-desargues-frontier.md`;
- `scratch/d5-terminal-root-universality-suffices.md`;
- `scratch/d5-terminal-root-universality-suffices-hostile-audit.md`;
- `preprint-d5-surface-kempe/main.pdf`.

## 3. Exact finite evidence

The following positive results are machine-assisted and have separate
semantic checkers.

| scope | exact result |
|---|---:|
| biconnected simple cubic graphs, order 14 | 480 |
| normalized \(D_5\)-flows, order 14 | 537,418 |
| terminal \(\Phi\)-plateaus, order 14 | 33,598 |
| non-root-universal terminal plateaus | 0 |
| fixed-distance \(d>1\) subplateaus | 642,167 |
| subplateaus without neutral descent | 0 |
| biconnected simple cubic graphs, order 16 | 3,874 |
| normalized flows, order 16 | 15,187,695 |
| initially bad state/root pairs, order 16 | 223,926,065 |
| unrescued pairs | 0 |

The order-16 census has no girth-eight graph.  A separate control reaches
the actual high-girth geometry: all 195 edge eliminations of a
130-vertex cyclically 4-edge-connected cubic graph of girth ten have
root-good \(D_5\)-flows.  The reduced graphs have girth nine or ten.
The complete labels are frozen in
`output/d5-root-feasibility-lift13-girth10/all-eliminations.json`;
an independent checker reconstructs every reduction and validates all
labels and factor paths.

These computations do not prove the remaining premise.

## 4. Routes now closed as insufficient

Several tempting strengthenings have exact countermodels:

1. The largest root-component rescue distance is unbounded, even on
   terminal spherical states.
2. Port monodromy forces a free \(6\times6\) action and 3,600-state
   all-bad orbit divisibility, but a disconnected
   \(\Theta\sqcup\Theta\) model realizes the bound.  Connected circuit
   incidence is essential.
3. Connectedness does force a factor-component chain whose consecutive
   factor pairs share a coordinate.  Ordinary shortest-chain descent is
   nevertheless false at minimum order 14.
4. Oum-compatible \((\phi,t)\) data are exactly arbitrary
   eight-coordinate pair-labelled double covers.  Existence of a choice
   whose co-occurrence graph is five-colourable is therefore exactly
   FiveCDC, not an intermediate theorem.
5. A literal flow produced from three spanning-tree fundamental
   completions can have a unique potential forcing \(K_6\).  Thus
   “every Jaeger tree flow compresses” is false.
6. The existential Jaeger-tree choice succeeds on every connected
   simple bridgeless cubic graph through order 14 (587 graphs), but
   monotone one-tree exchange is false at minimum order 12.

The surviving routes require either a genuinely global connected-chain
potential, a coordinated multi-tree exchange theorem, or a new
reducible configuration using the root-specific girth geometry.

## 5. Reproduction

From the project root:

```sh
python3 scratch/verify_d5_terminal_chi_chain_lex_order14_report.py
python3 scratch/verify_d5_root_component_distance_order16_summary.py
python3 scratch/verify_d5_root_feasibility_lift13_girth10.py
python3 scratch/verify_oum_combined_choice_12v.py
python3 scratch/verify_jaeger_tree_choice_through14.py
python3 scratch/verify_jaeger_one_tree_exchange_countermodel.py
python3 scratch/check_d5_root_port_monodromy_local_charge.py
python3 scratch/check_d5_connected_shared_coordinate_incidence.py
```

The PDF preprint is intentionally labeled as working research and says
explicitly that no proof or disproof has been obtained.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and audited the
conditional reductions, wrote the search and verification programs, ran
the finite experiments, and drafted the research notes and preprint.
The artifacts have not yet undergone independent human peer review.
