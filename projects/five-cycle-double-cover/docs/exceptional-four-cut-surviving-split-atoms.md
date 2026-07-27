# The two surviving exceptional four-cut distributions reduce to closed-state atoms

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE BRANCH REDUCTION / NEITHER DISTRIBUTION
ELIMINATED IN FULL**.

This note continues
`four-pole-exception-rooted-packing-algebra.md`.  Use the connected
size-four minimum-support setup and suppose a cyclic four-cut has
boundary flow
\[
                         (0,0,b,b),\qquad b\ne0,        \tag{1}
\]
with the published exceptional signatures
\(({\cal E}_4,{\cal E}_5)\) on its two shores.  The two zero cut edges
belong to the cardinal-minimum exact-zero matching \(M\), while two
further members of \(M\) are proper internal shore edges.

The preceding zero-free-shore lemma leaves only the internal-zero
distributions
\[
                 (k_4,k_5)=(1,1)\quad\text{or}\quad(2,0), \tag{2}
\]
where the first coordinate belongs to the \({\cal E}_4\) shore.

The conclusions below are exact:

1. in the \((1,1)\) branch, the \({\cal E}_4\) shore is either a
   rooted four-mark cross-intersection atom on the simple opposite cap,
   or an unrooted four-mark cross-intersection atom after smoothing the
   terminal-flanked cap;
2. in the \((2,0)\) branch the \({\cal E}_5\) shore has an explicit
   cost-zero avoiding lift, while the \({\cal E}_4\) shore is either a
   rooted six-mark obstruction or a smoothed unrooted six-mark
   obstruction;
3. in the simple-cap six-mark case, a bridge in the deleted-root graph
   gives either a smaller closed four-mark problem or an exact cyclic
   five-cut with three zero matching edges; and
4. repeated nontrivial two-plus-two pole decompositions descend to a
   smaller exceptional shore.  The auxiliary looped-edge/looped-path
   factorization cannot occur as two cyclic shores of the actual minimum
   counterexample.

No assertion below assumes Máčajová--Mazzuoccolo--Tabarelli
Conjecture 3.7.

## 1. Capped shore cores

Let \(H\) be the globally suppressed Tait-colourable core, let \(S\) be
its universally separated eight-edge matching, and let \(P\) pair the
marks according to the four edges of \(M\).  The two nonzero members of
the cut survive in \(H\) as
\[
                         e_1=x_1y_1,\qquad e_2=x_2y_2, \tag{3}
\]
where \(x_1,x_2\) lie on one core shore and \(y_1,y_2\) on the other.

On a shore \(W\), delete the two edges (3) and add the cap
\[
                         f=w_1w_2.                     \tag{4}
\]
Call the resulting cubic cap \(L_W\).  If the original shore contains
\(k\) proper internal edges of \(M\), then \(L_W\) has
\[
                         |S_W|=2k+2                   \tag{5}
\]
marked edges:

- two marks have their \(P\)-mates on the opposite original shore; and
- the remaining \(2k\) marks form \(k\) pairs internal to \(W\).

The inherited Tait colouring gives every mark colour \(c\) and gives
\(f\) a different colour.  The standard cap-gluing argument proves that
\(S_W\) remains universally separated in \(L_W\).

There are two geometrically different caps.  The shore containing the
marked edge \(s_q\) flanked by the two nonzero quotient edges is the
**flanked shore**.  Its cap \(f\) is parallel to \(s_q\).  The other
shore is the **opposite shore**.  Its cap is simple: an existing edge
between its two boundary ends would close a marked core circuit of
length four, contrary to the inherited marked-girth inequality.  Which
of these two shores has signature \({\cal E}_4\) is not determined by
the internal-zero distribution.

## 2. The exact inherited cut inequality

For \(Y\subseteq V(L_W)\), let
\[
 m(Y)=|S_W\cap E(L_W[Y])|,\qquad
 p(Y)=|\{\text{\(P\)-pairs strictly split by }Y\}|.     \tag{6}
\]
Here a shore mark whose mate lies outside \(W\) contributes to \(p(Y)\)
exactly when that mark is internal to \(Y\).

Suppose \(Y\) contains at most one endpoint of \(f\) and
\(L_W[Y]\) contains a circuit.  Replacing the cap by the two original
cut edges gives
\[
                  |\delta_H(Y)|=|\delta_{L_W}(Y)|.     \tag{7}
\]
The opposite original shore contains a circuit, so the global paired
cut inequality applies:
\[
                  |\delta_H(Y)|+p(Y)\ge4.              \tag{8}
\]
Every split pair counted by \(p(Y)\) uses a distinct mark internal to
\(Y\), and hence
\[
                         p(Y)\le m(Y).                 \tag{9}
\]
Combining (7)--(9) gives
\[
 \boxed{|\delta_{L_W}(Y)|+m(Y)\ge4}
 \quad\text{whenever \(Y\) contains at most one root endpoint.} \tag{10}
\]

On the simple opposite cap, this is exactly the partial marked
inequality used in `rooted-four-mark-bridgeless-reduction.md`.  It is
not silently promoted to subsets containing both root endpoints.  On
the flanked cap it does not remove the parallel two-circuit
\(\{f,s_q\}\), and the simple-cap theorem cannot be applied directly.

The all-\(c\) colouring also gives, for either value of \(k\), a binary
cycle which contains every mark and avoids \(f\).  This follows from the
root-avoiding trace lemma.  The remaining obstruction is solely that
some circuit components of every such trace contain an odd number of
marks.

## 3. The \((1,1)\) distribution

Both caps now have four marks.  On the \({\cal E}_4\) shore,
Lemma 2.1 and equation (14) of
`four-pole-exception-rooted-packing-algebra.md` say that a
componentwise-even all-four cycle avoiding \(f\) would produce the
forbidden boundary type \(T_\pi T_\pi\).  Therefore no such closed
rooted certificate exists.

### 3.1 The \({\cal E}_4\) shore is the simple opposite shore

In this subcase the bridge proof in
`rooted-four-mark-bridgeless-reduction.md` uses only (10), not the
unavailable inequality at a two-root-endpoint subset.  It applies
verbatim:

> **Proposition 3.1 (simple-cap four-mark exceptional atom).**  
> In the simple-cap subcase of the \((1,1)\) distribution, put
> \[
>                         J_4=L_4-f
> \]
> on the \({\cal E}_4\) shore.  Then:
>
> 1. \(J_4\) is connected, bridgeless, and 2-connected;
> 2. every two marks lie on a circuit of \(J_4\);
> 3. no circuit of \(J_4\) contains all four marks; and
> 4. for every partition of the marks into two pairs, every circuit
>    through one pair meets every circuit through the complementary
>    pair.

The proof is the root-bridge elimination, subcubic block lemma, and
cross-intersection argument already displayed in the cited note.

### 3.2 The \({\cal E}_4\) shore is terminal-flanked

Write \(s_q=x_1x_2\) for the marked edge parallel to the cap \(f\), and
write \(x_1z_1,x_2z_2\) for the third edges at its ends.  Delete
\(x_1,x_2\) and replace the path
\[
                         z_1x_1s_qx_2z_2
\]
by one marked edge \(g=z_1z_2\).  Retain the other three marks.  Denote
the smoothed marked graph by \((L^\circ,S^\circ)\).

The smoothing proof in Section 5 of
`cyclic-six-cut-four-mark-interface.md` depends only on the local
flanked geometry, not on all four pairing edges crossing the original
shore.  It therefore applies here without change:

1. \(L^\circ\) is a connected simple Tait-colourable cubic graph;
2. \(S^\circ\) is a universally separated four-edge matching; and
3. replacing \(g\) by the displayed three-edge path is a bijection
   \[
   \begin{split}
   &\{\text{binary cycles of \(L\) containing \(S_4\) and avoiding
   \(f\)}\}\\
   &\qquad\longleftrightarrow
   \{\text{binary cycles of \(L^\circ\) containing \(S^\circ\)}\},
   \end{split}                                         \tag{11}
   \]
   preserving circuit components and marked parity componentwise.

Thus \(L^\circ\) has no componentwise-even binary cycle containing all
four marks.  Since a connected Tait-colourable cubic graph is
bridgeless, the subcubic block lemma makes \(L^\circ\) 2-connected.
Every pair of marks is cyclable; no circuit contains all four; and
circuit families through complementary mark pairs are cross-intersecting
by the same disjoint-union argument as in Proposition 3.1.

This is an unrooted, simple cross-intersection atom.  The marked cut
inequality is not asserted to survive smoothing.

There is additional pairing data not present in an arbitrary rooted
four-mark problem: one pair of marks comes from the proper internal
zero edge, while the other two marks have mates on the opposite
original shore.  Every applicable cyclic cut in the unsmoothed shore
core still obeys (8), with this particular pairing.

Thus \((1,1)\) has not merely been renamed “rooted”: in either cap
geometry it has been reduced to a 2-connected cross-intersecting
four-way linkage with one internal mark pair, two external demands, and
universal separation.  The exact paired inequality remains available
in the unsmoothed core; it is not promoted to a marked-cut inequality
on \(L^\circ\).

## 4. The zero-free \({\cal E}_5\) shore in \((2,0)\)

On the \({\cal E}_5\) shore, \(k=0\).  The zero-free shore avoidance
lemma supplies two edge-disjoint joins avoiding \(f\).  In the canonical
quotient lift:

- the only zero edge in the capped shore is the artificial zero cap;
- after cutting the caps, no proper internal pole edge receives the
  zero-kernel label \(A\); and
- the boundary type is \(T_\pi T_\pi\), as required by
  \({\cal E}_5\).

This is stronger than abstract membership of \(T_\pi T_\pi\) in the
signature: it is a projection-coherent realization of internal
zero-cost zero.

The entire obstruction is therefore on the \({\cal E}_4\) shore.  Its
cap has
\[
                         |S_4|=6,                     \tag{12}
\]
consisting of two internal \(P\)-pairs and two marks whose mates lie on
the zero-free shore.  A componentwise-even all-six cycle avoiding \(f\)
would again give the forbidden type \(T_\pi T_\pi\).  Hence every
root-avoiding all-six trace has an odd-marked component.

If this \({\cal E}_4\) shore is terminal-flanked, perform exactly the
smoothing of Section 3.2, now retaining five old marks in addition to
the replacement mark \(g\).  The same local proof gives a connected
simple Tait-colourable cubic graph with a universally separated
six-edge matching and an exact parity-preserving bijection between
root-avoiding all-six cycles before smoothing and all-six cycles after
smoothing.  Consequently the smoothed graph is a 2-connected unrooted
six-mark obstruction.  Again, no marked cut inequality on the smoothed
graph is claimed.

## 5. Bridge alternatives in the simple-cap six-mark obstruction

This section applies only when the \({\cal E}_4\) shore is the simple
opposite shore.  Put
\[
                         J_6=L_4-f.                    \tag{13}
\]
Unlike the four-mark case, a bridge of \(J_6\) is not automatically a
contradiction.

Suppose \(h\) is a bridge.  Since \(L_4\) is Tait-colourable and
therefore bridgeless, \(f\) crosses the same two shores, so
\[
                         \delta_{L_4}(X)=\{f,h\}.       \tag{14}
\]
Both shores contain a circuit by the standard cubic degree count.  Each
contains one root endpoint, so (10) applies to both.  The Parity Lemma
gives \(h\) the colour of \(f\), different from the common mark colour;
thus neither cut edge is marked.  Equation (10) forces at least two
internal marks on either shore.  With six total marks, the only splits
are
\[
                         2+4\quad\text{or}\quad3+3.    \tag{15}
\]

### 5.1 The \(2+4\) alternative

The two-mark shore lemma gives a circuit through the two marks on the
small marked shore, avoiding both \(f\) and \(h\).  The remaining
obligation is entirely on the four-mark shore: after capping its two
boundary positions, one needs a componentwise-even all-four cycle in
the compatible closed state.

Thus a \(2+4\) bridge does not create a new six-mark primitive.  It
reduces the obstruction to a strictly smaller closed four-mark cap.
Before Proposition 3.1 is applied to that descendant, its own cap must
again be audited as simple or parallel; in the parallel case the
smoothing reduction of Section 3.2 is the applicable conclusion.  No
claim is made that the four-mark descendant is automatically solvable.

### 5.2 The \(3+3\) alternative is a cyclic five-cut

Because the cut edges in (14) are unmarked, every one of the six marks
is internal to one shore.  For an unmarked cut, pairing parity gives
\[
                         p(X)\equiv m(X)\pmod2.         \tag{16}
\]
The stronger paired inequality (8), applied to both shores of (14),
gives
\[
                         p(X),p(\bar X)\ge2.            \tag{17}
\]
There are only four global pairing edges.  In the \(3+3\) split,
(16)--(17) therefore force
\[
                         p(X)=p(\bar X)=3.              \tag{18}
\]

Lift \(X\) back to the ambient expansion.  Its cut consists of:

- the two nonzero core edges represented by \(f,h\); and
- the three zero matching edges counted by (18).

Both shores contain circuits, so this is a cyclic five-edge cut with
flow word
\[
                         (0,0,0,b,b).                  \tag{19}
\]

> **Proposition 5.1 (simple-cap six-mark bridge trichotomy).**  
> A surviving simple-cap \((2,0)\) obstruction has one of three forms:
>
> 1. \(J_6\) is bridgeless, and hence 2-connected by the subcubic block
>    lemma;
> 2. it reduces across a \(2+4\) bridge to a closed four-mark atom; or
> 3. it exposes the cyclic five-cut (19), containing exactly three
>    edges of \(M\).

The third outcome moves the problem to an exact five-pole interface; it
is not eliminated by cyclic four-edge-connectivity.

## 6. The pairing enumeration

The parity assertion above has a literal eight-line verification.  For a
shore with \(k\) internal pairs, label the two external-demand marks
\(x_0,x_1\).  For a subset \(R\) of the shore marks,
\[
 p(R)=|\{x_0,x_1\}\cap R|
      +|\{\text{internal pairs split by }R\}|.          \tag{20}
\]

The script `scratch/exceptional_cut_pairing_states.py` enumerates (20)
and retains states with \(p(R),p(\bar R)\ge2\).  It gives
\[
\begin{array}{c|c}
k&(|R|,p(R),p(\bar R))\\ \hline
1&(2,2,2)\\
2&(2,2,2),(2,2,4),(3,3,3),(4,2,2),(4,4,2).
\end{array}                                             \tag{21}
\]
In particular the \(3+3\) row is uniquely \((3,3,3)\).

The frozen output is
`scratch/exceptional-cut-pairing-states-result.json`.  The independently
written bit-mask consumer
`scratch/verify_exceptional_cut_pairing_states.mjs` recomputes the rows
without importing the Python producer and reports
`PASS: independent pairing-state replay`.

The SHA-256 digests are:

```text
2d59aacd37d75b3a40477d510ff518dd1d5b906e5f795c9ffbc747d6e2fd5a17  scratch/exceptional_cut_pairing_states.py
4eb2ad037cdaab5f43f5f36e206e97786d7851c382c3aff84f6513e061aa3226  scratch/verify_exceptional_cut_pairing_states.mjs
acf170b07c5808d38abd4ce7771732df177b0265061f20ca62a0b2d6eaf4d504  scratch/exceptional-cut-pairing-states-result.json
```

## 7. Two-plus-two descent to a smaller exceptional atom

There is also an intrinsic pole reduction.  Suppose one exceptional
shore pole has a proper two-edge cut which splits its four original
terminals \(2+2\).  Cutting those two edges expresses its signature as
the exact two-plus-two composition of the two smaller shore signatures.

Theorem 6.1 of
`four-pole-exception-rooted-packing-algebra.md` gives:

- an \({\cal E}_4\) composition has a smaller \({\cal E}_4\) factor;
- an \({\cal E}_5\) composition has a smaller \({\cal E}_5\) factor,
  unless the two factors have the looped-edge and looped-three-vertex-
  path signatures.

The auxiliary exception cannot occur for this cut inside the actual
minimum counterexample.  Both cut factors are connected.  If a connected
acyclic cubic four-pole has \(n\) internal vertices, then it has
\(n-1\) proper edges and four semiedges, so the degree sum gives
\[
                         3n=2(n-1)+4,
\]
and hence \(n=2\).  Its signature is therefore one of the four-cycle
signatures shown in Figure 1 of the primary paper; it has neither the
three-type looped-edge nor the five-type looped-path signature.  Hence
both auxiliary factors would contain circuits.

Each factor, viewed in the ambient graph, is then a shore of a
cycle-separating four-cut: its boundary consists of two original cut
edges and the two new connector edges.  Theorem 3.10 of Máčajová--
Mazzuoccolo--Tabarelli says its signature must be one of
\({\cal E}_4,{\cal E}_5\), contradicting the auxiliary signature.

Therefore every actual nontrivial two-plus-two decomposition contains a
strictly smaller exceptional cyclic shore.  Repeating this descent
terminates.

Nontrivial zero- or one-terminal two-cut shores are removed by the exact
edge/vertex replacement lemma in
`four-pole-boundary-human-lemmas.md`; the replacement preserves the full
boundary relation.  A bridge is excluded in the actual cyclically
four-edge-connected, distinct-boundary-endpoint domain by the same cubic
degree count used in the zero-free shore lemma.

Consequently the exceptional branch contains a terminal atom whose
proper graph has:

1. no bridge;
2. no nontrivial two-edge-cut shore with zero or one original terminal;
3. no two-plus-two decomposition; and
4. one of the two exact exceptional signatures.

The unavoidable two-edge cuts isolating a single degree-two boundary
vertex are regarded as trivial.  This atom conclusion does not preserve
the particular internal-zero distribution during descent, so it is a
structural target, not an elimination of either row in (2).

## 8. Exact remaining obligations

The original four-cut branch is now reduced to the following alternatives.

For \((1,1)\):

- on the simple opposite cap, exclude or realize the paired,
  universally separated cross-intersection atom of Proposition 3.1;
  or
- on the terminal-flanked cap, exclude or realize the smoothed simple
  unrooted cross-intersection atom of Section 3.2 while retaining its
  unsmoothed pairing data.

For \((2,0)\):

- exclude the 2-connected smoothed unrooted six-mark atom when the
  \({\cal E}_4\) shore is terminal-flanked;
- exclude the 2-connected rooted six-mark atom when it is opposite;
- reduce its \(2+4\) bridge descendant by solving the resulting closed
  four-mark atom; or
- analyze the exact \(000bb\) cyclic five-pole interface with three
  zero matching edges.

These obligations are strictly stronger than the bare ten-type
exceptional signatures.  Neither boundary parity nor minimum-support
cardinality alone resolves them.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the capped-core
inequality, pairing enumeration, rooted bridge alternatives, and
two-plus-two descent, wrote the replay script, and drafted this note.
The exceptional signatures and their minimum-counterexample theorem are
prior work of Máčajová, Mazzuoccolo, and Tabarelli and are explicitly
attributed.  Every universal deduction is displayed for line-by-line
checking.  The finite pairing enumeration is a transparent parity check,
not a graph census.  This is not human peer review and not a resolution
of five-CDC.
