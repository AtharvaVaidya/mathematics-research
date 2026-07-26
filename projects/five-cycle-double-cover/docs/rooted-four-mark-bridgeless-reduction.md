# Rooted four-mark failure survives only in a bridgeless deleted-root core

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE SHARPENING / OPPOSITE SIX-CUT CAP REDUCED
TO A GENUINE FOUR-WAY LINKAGE OBSTRUCTION / FULL ROOTED THEOREM OPEN**.

This note sharpens `rooted-four-mark-cap-avoidance.md` at exactly the
obstruction exhibited by its order-\(28\) countermodel.  Under the
standard marked cyclic-cut inequality, deleting the forbidden edge
cannot leave a bridge in a rooted counterexample.  More importantly, the
same proof applies to the opposite cap in
`cyclic-six-cut-four-mark-interface.md`, even though that cap is not
known to satisfy the full marked cyclic-cut inequality.

Thus the retained \(3+1\) two-cut countermodel is not merely absent by
inspection: its entire obstruction mechanism is rigorously excluded in
the inherited six-cut branch.  Any surviving failure has a
2-connected subcubic graph after the cap edge is deleted, every pair of
marks lies on a cap-avoiding circuit, no cap-avoiding circuit contains
all four marks, and the circuit families belonging to complementary
mark pairs are cross-intersecting.

This is an exact sharper obstruction, not a proof of the remaining
four-way linkage assertion.

## 1. Standard rooted setup

Let \(L\) be a connected simple cubic graph, let \(S\) be a four-edge
matching, and let \(f\in E(L)\setminus S\).  Assume:

1. \(L\) is Tait-colourable;
2. one Tait colouring gives every member of \(S\) one common colour
   \(c\) and gives \(f\) a different colour;
3. for every \(X\subseteq V(L)\) for which \(L[X]\) contains a circuit,
   \[
      |\delta_L(X)|+|S\cap E(L[X])|\ge4.                 \tag{1}
   \]

Universal separation implies hypothesis 2 by mark precolouring, but is
not otherwise needed in the next lemma.

A **closed rooted certificate** is a binary cycle \(Q\) which contains
all four marks, excludes \(f\), and has an even number of marks on every
circuit component.

## 2. The deleted root has no bridge

> **Root-bridge elimination lemma.**  Under the hypotheses of Section 1,
> if \(L-f\) has a bridge, then \(L\) has a closed rooted certificate.
> Consequently every counterexample to the standard rooted assertion
> has \(L-f\) bridgeless.

### Proof

A Tait-colourable cubic graph has no bridge, by the Parity Lemma.  Hence
\(L-f\) is connected.  Suppose \(h\) is a bridge of \(L-f\), and let
\(X,\bar X\) be the two shores of
\[
                 (L-f)-h.                              \tag{2}
\]
The edge \(f\) must join the two shores; otherwise \(h\) would already
be a bridge of \(L\).  Therefore
\[
                 \delta_L(X)=\{f,h\}.                   \tag{3}
\]

Both shores of (3) contain a circuit.  Indeed, a shore with \(n\)
vertices has
\[
          |E(L[X])|=\frac{3n-2}{2}.                     \tag{4}
\]
Its two boundary ends are distinct: if both cut edges had one common
end \(v\) on a nontrivial shore, the third edge at \(v\) would be a
bridge separating the rest of that shore; a one-vertex shore is
impossible in a simple cubic graph with boundary two.  Thus \(n\ge2\),
and (4) is at least \(n\), which is exactly the elementary edge-count
criterion for a connected graph to contain a circuit.  The same
argument applies to \(\bar X\).

The Parity Lemma says that the two members of a 2-edge cut have one
common Tait colour.  Since \(f\) has colour different from \(c\), the
edge \(h\) is not a member of \(S\).  Thus every mark is internal to one
of the two shores.  Applying (1) to both gives
\[
 |S\cap E(L[X])|\ge2,\qquad
 |S\cap E(L[\bar X])|\ge2.                              \tag{5}
\]
There are four marks in total, so equality holds in both inequalities.

The two-mark shore lemma in
`marked-three-edge-cut-signatures.md` now applies to each shore with
boundary size two.  It gives a circuit \(C_X\subseteq L[X]\) through
the two marks in \(X\), and a circuit
\(C_{\bar X}\subseteq L[\bar X]\) through the other two.  Their disjoint
union
\[
                  Q=C_X\mathbin{\dot\cup}C_{\bar X}      \tag{6}
\]
contains all four marks, has two marks on each component, and uses
neither \(f\) nor \(h\).  It is the required closed rooted certificate.
\(\square\)

The order-\(28\) countermodel in
`rooted-four-mark-cap-avoidance.md` fails precisely at (5): its two
shores contain three and one marks.  The lemma therefore excludes the
whole odd-shore two-cut mechanism, rather than only that one graph.

## 3. The same lemma holds for the opposite six-cut cap

Use the notation of `cyclic-six-cut-four-mark-interface.md`.  On the
opposite shore put
\[
                  L=H_B^+=H[B]+f_B                     \tag{7}
\]
and let \(S_B\) be its four internal marks.  The inherited colouring
gives every member of \(S_B\) colour \(c\) and gives the cap \(f_B\) the
different common colour of the two original cut edges.

The full inequality (1) is not known for \(L\).  What is proved in that
note is enough:
\[
 |\delta_L(Y)|+|S_B\cap E(L[Y])|\ge4                    \tag{8}
\]
whenever \(L[Y]\) contains a circuit and \(Y\) contains at most one
endpoint of \(f_B\).

> **Inherited opposite-cap bridge lemma.**  If \(L-f_B\) has a bridge,
> then the \(B\)-shore has a closed four-mark certificate.  Hence a
> failure of the inherited closed-state assertion on this shore forces
> \(L-f_B\) to be bridgeless.

### Proof

Repeat the proof of Section 2.  A bridge \(h\) of \(L-f_B\) gives the
2-edge cut
\[
                  \delta_L(X)=\{f_B,h\}.                \tag{9}
\]
Each shore contains exactly one endpoint of \(f_B\), so (8), rather
than the unavailable full inequality, applies to both shores.  Cut
parity again makes \(h\) the colour of \(f_B\), so neither cut edge is
marked.  Equation (8) forces the \(2+2\) internal mark split.

To apply the two-mark shore lemma, consider any cyclic subset \(Y\)
inside either shore.  Such a \(Y\) still contains at most one endpoint
of \(f_B\), so (8) supplies every inequality used in that lemma.  The
two resulting shore circuits give a closed certificate avoiding the
entire cut. \(\square\)

This proves that the simple \(B\)-cap cannot fail for the reason seen in
the naive rooted countermodel.

## 4. Exact structure after deleting the cap

Let \((L,S,f)\) be either a standard rooted counterexample or a failure
of the inherited opposite-cap conclusion.  Put
\[
                         J=L-f.                         \tag{10}
\]
The preceding lemmas say that \(J\) is connected and bridgeless.  Its
minimum degree is two and its maximum degree is three.

> **Subcubic block lemma.**  A connected bridgeless graph of minimum
> degree at least two and maximum degree at most three is
> 2-connected.

**Proof.**  If \(v\) were a cutvertex, every component of \(J-v\) would
need at least two edges to \(v\); a component with only one such edge
would make that edge a bridge.  Two components would therefore require
at least four edges incident with \(v\), contrary to
\(\deg_J(v)\le3\). \(\square\)

Subdividing two prescribed edges in a 2-connected graph and applying
the standard theorem that any two vertices of a 2-connected graph lie
on a common circuit gives:

> **Pair cyclability.**  Every two marks of \(S\) lie on one circuit of
> \(J=L-f\).

For a partition
\[
             S=\{s_i,s_j\}\mathbin{\dot\cup}\{s_k,s_\ell\}, \tag{11}
\]
let \({\cal C}_{ij}\) be the nonempty family of circuits of \(J\)
through \(s_i,s_j\).

> **Cross-intersection obstruction.**  In a rooted counterexample:
>
> 1. no circuit of \(J\) contains all four marks; and
> 2. for every one of the three partitions (11), every member of
>    \({\cal C}_{ij}\) meets every member of
>    \({\cal C}_{k\ell}\).

The first assertion is immediate because one such circuit would itself
be a closed rooted certificate.  For the second, two edge-disjoint
circuits in a subcubic graph are vertex-disjoint: at a common vertex
they would require four distinct incident edges.  Their union would
therefore be a binary cycle with two two-mark components, again a
closed rooted certificate.

Thus the remaining obstruction is genuinely simultaneous.  It is not
failure of a mark trace, a bridge, or pairwise cyclability.  It is a
cross-intersecting four-way linkage configuration in a 2-connected
subcubic graph.

## 5. Relevant prescribed/forbidden-cycle literature

Two sources delimit what may be imported.

Knappe and Pitz, *Circuits through prescribed edges*, J. Graph Theory
93 (2020), 470--482, prove that a connected graph contains a circuit
through **any** \(k\) prescribed edges exactly when it has no odd cut of
size at most \(k\).  Their later connectivity parameter satisfies
\[
                  g(4)=4.                              \tag{12}
\]
This is stronger than the \(g(3)=3\) special case already used in the
four-mark proof, but it does not close the present problem.  The
deleted-root graph \(J\) is only 2-connected, and cubic vertex stars are
odd 3-cuts.  The fixed four marks are independent, so the uniform
obstruction in their theorem is too coarse.

Sheng Bau, *Cycles with Prescribed and Forbidden Sets of Elements in
Cubic Graphs*, Graphs Combin. 18 (2002), 201--208,
<https://doi.org/10.1007/s003730200013>, is directly relevant and was
missing from the earlier literature audit.  Its abstract states a
necessary-and-sufficient canonical-contraction condition for a cycle
through three prescribed vertices and one prescribed edge while
excluding another edge in a 3-connected cubic graph, and a second
condition for four prescribed vertices avoiding one vertex in the
cyclically 4-connected case.  Neither statement, as published in the
abstract, is the four-prescribed-edges-plus-one-forbidden-edge theorem
needed here.  The full paper is not openly available from the DOI, so no
unstated part of its characterization is used in this note.

Goldstein's *Generalization of Menger's Edge Theorem to Four Vertices*,
<https://arxiv.org/abs/2111.10249>, and Abdi--Guenin's
*Packing odd \(T\)-joins with at most two terminals*,
<https://arxiv.org/abs/1410.7423>, give exact packing theorems when all
nonterminal vertices have even degree (with the stated terminal parity
conditions).  After the four marks are subdivided, the present core has
degree three at every nonterminal.  Those hypotheses fail exactly, so
their min--max conclusions cannot be imported without a new
parity-preserving transformation.

## 6. Exact structured finite screen

The existing generator `generate_marked_three_sums.py` produces
\(13\,824\) labelled four-mark graphs.  The all-Tait-colouring checker
finds \(288\) rows on which the four required marks are universally
separated, and \(240\) of those also satisfy the exact marked
cyclic-cut inequality (1).

The independent cycle-space consumer
`scratch/analyze_rooted_four_mark_batch.py` was run on those \(240\)
rows.  It:

1. independently decodes every graph6 row;
2. constructs a fundamental binary cycle basis;
3. solves the four all-mark trace equations by Gaussian elimination;
4. enumerates the resulting affine fibre in Gray order;
5. checks marked parity separately on every circuit component; and
6. intersects all componentwise-even all-mark cycles.

The exact totals are
\[
\begin{array}{c|r}
\text{marked-cut-compliant rows}&240\\
\text{componentwise-even all-mark cycles}&3\,818\,240\\
\text{rows with a forced unmarked edge}&0.
\end{array}                                             \tag{13}
\]
Thus every edge outside the four marks is avoided by at least one closed
certificate in every retained instance.  This is stronger than checking
one preselected root, but it is only a structured finite theorem.

As a control, the same consumer was run on all \(288\) universally
separated rows before the marked-cut filter.  It enumerated
\(4\,620\,800\) componentwise-even all-mark cycles and again found no
forced unmarked edge on any row.

A second targeted generator,
`scratch/generate_rooted_four_cut_repairs.py`, replaces one internal
edge on each side of the order-\(28\) countermodel's obstructing
two-cut by two cross edges.  It generates \(512\) simple connected
cubic graphs in which the old \(3+1\) shore has boundary four.  None
retains universal separation of the four marks.  This negative result
shows that the naive cut repair destroys a necessary inherited
hypothesis; it is not evidence for a universal theorem.

## 7. Remaining exact obligation

For the opposite cap, the unresolved assertion has now been reduced to:

> in the 2-connected subcubic graph \(H[B]\), four universally
> separated marks with all inherited girth and paired-cut data cannot
> form the cross-intersecting circuit configuration of Section 4.

For the flanked shore, the separate obligation remains to prove an
unrooted componentwise-even all-four cycle in the smoothed graph
\((H_A^\circ,S_A^\circ)\).  The bridge lemma does not address that
shore.

Either a four-way linkage theorem excluding the displayed
cross-intersection, or a graph satisfying it together with the full
inherited minimum-support data, would settle this subbranch.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the omitted
prescribed/forbidden-cycle and four-terminal packing sources, proved the
bridge and cross-intersection reductions, wrote the exact finite
consumer, and ran the structured screens.  Every universal claim in
Sections 2--4 is fully displayed for human checking.  The finite counts
are computational diagnostics, not a substitute for proof or human peer
review, and no five-cycle-double-cover resolution is claimed.
