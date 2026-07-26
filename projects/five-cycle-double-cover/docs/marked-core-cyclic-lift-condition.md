# The exact marked cyclic-cut condition for the size-four core

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE NECESSARY CONDITION / NEW UNIVERSAL CLOSURE
PROOF DRAFT AWAITING INDEPENDENT AUDIT**.

This note sharpens the size-four branch of
`extremal-marked-core-reduction.md`.  It distinguishes the marked
connectivity actually inherited from a cyclically \(4\)-edge-connected
ambient graph from the stronger, unnecessary demand that the suppressed
core itself be cyclically \(4\)-edge-connected.

## 1. Setup

Let \(G\) be cubic and cyclically \(4\)-edge-connected.  Let \(M\) be a
matching of size four such that \(G-M\) has two components.  Every edge of
\(M\) then joins the two components, and each component \(D\) contains four
endpoints of \(M\).  Suppress those four degree-two vertices in \(D\).
This gives a cubic core \(H\) with a four-edge matching \(S\); the members
of \(S\) are the edges created by suppression.

For \(X\subseteq V(H)\), write
\[
 s(X)=|S\cap E(H[X])|.
\]

## 2. Exact lift-cut lemma

> **Marked cyclic-cut lemma.**  If \(H[X]\) contains a circuit, then
> \[
> |\delta_H(X)|+s(X)\ge4.                         \tag{1}
> \]

**Proof.**  Lift \(X\) to a vertex set \(Y\subseteq V(D)\) as follows.
For every marked edge with both ends in \(X\), include its subdivision
vertex in \(Y\).  For every marked edge crossing \(\delta_H(X)\), leave
its subdivision vertex outside \(Y\).

An unmarked core edge contributes to \(\delta_G(Y)\) exactly when it is in
\(\delta_H(X)\).  A marked core edge crossing \(\delta_H(X)\) likewise
contributes exactly one of its two subdivided halves.  A marked edge
internal to \(X\) contributes no half-edge to the cut, but its subdivision
vertex has one incident edge of \(M\), and that matching edge joins the
other component of \(G-M\); it therefore contributes one cut edge.
Consequently
\[
 |\delta_G(Y)|=|\delta_H(X)|+s(X).                \tag{2}
\]

Subdividing edges does not destroy the circuit in \(H[X]\), so \(G[Y]\)
contains a circuit.  The other component of \(G-M\) lies in
\(G-Y\) and also contains a circuit because it has minimum degree two.
Thus \(\delta_G(Y)\) is cycle-separating.  Cyclic
\(4\)-edge-connectivity of \(G\), together with (2), proves (1).
\(\square\)

The same proof applies to disconnected \(H[X]\): choose one cyclic
component.  Therefore it is enough computationally to inspect connected
cyclic shores.  A violation of (1) has boundary at most three, so it
appears as a connected component after deletion of at most three edges.
The option

```text
--marked-cyclic-connectivity 4
```

in `scratch/tait_all_coloring_mark_separation.cpp` checks exactly (1);
it does not replace it by ordinary cyclic connectivity of \(H\).

## 3. Four marks already refute the unqualified core assertion

The order-\(44\) cubic graph

```text
k??????O@?B?D?EGGSAK?H_?HG?Ao@A_A?????????????C?G?C???M???B_???[_??????????????????O?C??C????B_????M?????[_???????????????????????C??_???O?????B_?????B_?????@o
```

with marked edges
\[
 (1,9),\quad(22,26),\quad(30,34),\quad(38,42)
\]
is a counterexample to the statement that every universally separated
four-edge matching packs two \(T\)-joins.

The exact checks give:

- the graph is simple, connected, cubic, and bridgeless;
- all \(5\,832\) Tait colourings modulo global colour permutation separate
  the four marks;
- the binary cycle space has dimension \(23\);
- the four equations requiring all marks have rank \(4\), leaving
  \(2^{19}=524\,288\) binary cycles; and
- their marked-component profiles are
  \[
  \begin{array}{c|r}
  (1,1,1,1)&198\,656\\
  (1,1,2)&168\,960\\
  (1,3)&156\,672.
  \end{array}
  \]

No profile is even componentwise, so the even-marked circuit criterion
proves nonpacking.

This example does **not** satisfy (1).  It has three cyclic two-edge cuts
\[
\begin{split}
 &\{(0,20),(8,24)\},\\
 &\{(0,28),(11,32)\},\\
 &\{(0,36),(12,40)\},
\end{split}
\]
and the eight-vertex shore of each cut contains exactly one mark.  Hence
the left side of (1) is \(2+1=3\).  The obstruction is therefore excluded
by the actual ambient hypothesis.

## 4. Exact order-22 screen under the correct condition

The complete frozen order-\(22\) canonical connected simple cubic corpus
contains \(7\,319\,447\) graphs.  The marked-core enumerator checked
\(95\,360\,112\) Tait colourings modulo global colour permutation on its
\(7\,174\,735\) colourable rows.  It found no four-edge matching which
simultaneously:

1. is separated in every Tait colouring;
2. fails the even-marked circuit packing criterion; and
3. satisfies the exact marked cyclic-cut inequality (1).

The counts, command, source hash, input hash, log hash, and empty witness
stream are frozen in
`scratch/order22-cyclic4-separated4-nonpacking-result.json`.
This is an exact finite theorem only at order \(22\).  The minimum
five-CDC counterexample branch with a size-four support has order at least
\(68\), so the screen is not a proof of the universal marked-core lemma.

## 5. New closure proof draft

The following statement eliminates the size-four/two-component branch
if the new proof draft passes independent audit:

> Every connected Tait-colourable cubic graph with a universally
> separated four-edge matching satisfying (1) has a binary cycle
> containing all four marks with an even number of marks on every circuit
> component.

`four-mark-core-closure.md` now gives a human-checkable proof using (1).
It reduces cyclic two-cuts and all marked or balanced cyclic three-cuts.
The remaining unmarked \(1+3\) cuts are organized by the standard
3-sum decomposition into cyclically \(4\)-edge-connected cubic factors.
A weighted-tree argument identifies a central factor.  Universal
separation permits all four marks to be precoloured alike; the actual
central marks together with the same-colour cap edge of each one-mark
branch form four independent edges.  The 1997 quasi-\(4\)-connected
four-edge cycle theorem supplies a central cycle, and the one-mark shore
lemma glues every branch into it.

The order-\(44\) example remains useful because it shows why the proof
must use (1).  The order-\(22\) census is now only a finite cross-check,
not part of the proof.  The new argument is not yet promoted to audited
theorem status.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the four-mark
countermodel inside an earlier six-mark construction, formulated and
proved the exact lift-cut lemma, implemented the finite check, and drafted
this note.  The displayed proof is intended for line-by-line human
checking.  The finite census is not independent human review and makes no
universal claim.
