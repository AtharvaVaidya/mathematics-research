# Even-marked circuit packing across a three-edge cut

Date: **2026-07-26**.

Status: **HUMAN-CHECKABLE EXACT GLUING THEOREM / ALL FOUR-MARK
THREE-CUTS REDUCED IN A NEW PROOF DRAFT**.

This note isolates the complete boundary information needed to glue the
even-marked circuit criterion across a nontrivial three-edge cut.  It
turns the observed repair of the structured three-sum examples into a
precise seven-state problem.

## 1. Marked cubic poles

Let \(H\) be a cubic graph with a three-edge cut
\[
 B=\{b_1,b_2,b_3\}
\]
whose shores are \(A\) and \(D\).  Assume that no marked edge belongs to
\(B\).  Cutting the three boundary edges produces two cubic three-poles.

For one shore \(P\), let \(S_P\) be its internal marked edges.  A
**closed admissible state** is an internal even subgraph \(Q_P\) which:

1. contains every edge of \(S_P\);
2. uses none of the three boundary semiedges; and
3. has an even number of marks on every circuit component.

For a two-element set \(I\in\binom{\{1,2,3\}}2\), an
**open admissible state** \((I,\epsilon)\) is an internal subgraph together
with the two boundary semiedges indexed by \(I\) such that:

1. it contains every edge of \(S_P\);
2. its only odd-degree internal vertices are the ends of those two
   semiedges;
3. every closed circuit component contains an even number of marks; and
4. its unique open path contains \(\epsilon\pmod2\) marked edges.

Thus the complete signature of a marked three-pole is a subset of the
seven-element state universe
\[
 \Sigma=\{0\}\ \cup\
 \left(\binom{\{1,2,3\}}2\times\mathbb F_2\right).             \tag{1}
\]

## 2. A two-mark shore always has the closed state

The marked cyclic-cut inequality forces substantially more than the
finite screen initially suggested.

> **Two-mark shore lemma.**  Let \(P=H[A]\) be connected and subcubic.
> Suppose the \(k\in\{2,3\}\) edges of \(\delta_H(A)\) have distinct ends
> in \(A\), so \(P\) has minimum degree two.  Let exactly two marked edges
> lie internally in \(P\).  If
> \[
>  |\delta_H(X)|+|S\cap E(H[X])|\ge4                         \tag{2}
> \]
> for every cyclic \(X\subseteq A\), then one circuit of \(P\) contains
> both marked edges.

**Proof.**  Delete every bridge of \(P\), and consider the tree whose
nodes are the resulting bridge-components.  If there is no bridge, then
\(P\) is 2-edge-connected.  A 2-edge-connected subcubic graph of minimum
degree two has no cutvertex: two different components behind a cutvertex
would each need at least two incident edges at that vertex, forcing
degree at least four.  Thus \(P\) is 2-connected.  Subdivide the two
marked edges.  Any two vertices of a 2-connected graph lie on a common
circuit, so undoing the subdivisions gives a circuit through both marks.

Suppose instead that the bridge-component tree is nontrivial.  It has at
least two leaves.  A leaf component \(K\) is cyclic.  Indeed, it cannot
be a single isolated vertex: such a vertex has only one incident bridge
but has degree at least two in \(P\), so it would have a nonbridge edge
inside the component.

Let \(X=V(K)\), let \(p(X)\) be the number of the \(k\) pole boundary
edges incident with \(X\), and let \(s(X)\) be the number of internal
marks in \(K\).  Exactly one bridge leaves \(K\), hence
\[
 |\delta_H(X)|=1+p(X).
\]
If \(K\) does not contain both marks, then \(s(X)\le1\), and (2) forces
\[
 p(X)\ge2.                                                   \tag{3}
\]
The leaf components are disjoint, and every pole boundary edge is
incident with at most one of them.  Two leaves satisfying (3) would
therefore consume at least four boundary edges, impossible because
\(k\le3\).  Consequently some leaf component contains both marked edges.
It is 2-edge-connected and subcubic, hence 2-connected by the preceding
argument, and has a circuit through both.  \(\square\)

The distinct-boundary-end hypothesis is automatic for a minimal cyclic
cut in a cubic graph.  If two edges of a cyclic three-cut share an end
on one shore, deleting that end exposes a cyclic cut of size at most two;
the two-cut case should be reduced first.

Two immediate consequences are useful.

> **Cyclic two-cut corollary.**  A four-mark core satisfying (2) and
> failing the even-marked circuit criterion has no cyclic two-edge cut.

**Proof.**  Let \(A,D\) be the shores of such a cut.  Applying (2) to
both gives at least two internal marks on each shore.  Since there are
only four marks, the cut itself is unmarked and each shore contains
exactly two.  The two-mark shore lemma supplies one circuit through the
two marks on each shore.  Their disjoint union contains all four marks
and every component has two marks, contradicting failure of the
criterion.  \(\square\)

> **Balanced cyclic three-cut corollary.**  If an unmarked cyclic
> three-edge cut has two marks on each shore, then the marked core packs.

**Proof.**  Apply the lemma to both shores and take the union of the two
closed circuits.  \(\square\)

Thus an unmarked cyclic three-cut in a surviving nonpacking core must
have the unbalanced internal distribution \(1+3\).  Cuts containing
marked boundary edges, and the compatibility of the odd open states in
the \(1+3\) case, remain separate obligations.

There is no loss of Tait-colouring information when one shore is capped
by a new cubic vertex.

> **Three-shore cap lemma.**  Let an unmarked three-edge cut of a
> Tait-colourable cubic graph \(H\) have shores \(A,D\).  Form \(H_A\)
> from \(H[A]\) by adjoining one new vertex adjacent to the three
> boundary ends, and define \(H_D\) similarly.  Then:
>
> 1. both capped shores are Tait-colourable;
> 2. every Tait colouring of either capped shore extends to a Tait
>    colouring of \(H\); and
> 3. a matching of internal edges on one shore which is universally
>    separated in \(H\) is universally separated in that capped shore.

**Proof.**  In every Tait colouring of a cubic graph, the Parity Lemma
forces the three edges of a three-edge cut to have the three distinct
colours.  Restrict a colouring of \(H\) to either shore and give the
three new cap edges the corresponding cut-edge colours.  This proves
the first assertion.

Conversely, fix an arbitrary colouring of \(H_A\) and any colouring of
\(H_D\).  At each cap vertex the three incident edges have distinct
colours.  A single global permutation of the colours on \(H_D\) can
therefore make the colours agree on all three ordered boundary
positions.  Delete the two cap vertices and join corresponding boundary
ends.  The result is a Tait colouring of \(H\) extending the prescribed
colouring of \(H_A\).  The same argument works with the shores reversed.

If two internal marked edges of \(A\) shared a bichromatic circuit in
some colouring of \(H_A\), extend that colouring to \(H\).  The circuit
remains a bichromatic circuit after the cap is replaced by the other
shore: if it avoids the cap this is immediate, while if it uses the cap,
its two cap edges extend through the unique bichromatic path on the
opposite shore.  This would contradict universal separation in \(H\).
\(\square\)

Thus the three-mark shore in the \(1+3\) case may be studied exactly as
a Tait-colourable cubic cap with a universally separated triple and one
distinguished unmarked cap vertex.  The local marked-cut inequality is
imposed only on cyclic shores avoiding that cap vertex.

The one-mark side of the unbalanced case can in fact be settled
completely.

> **One-mark shore lemma.**  Let \(P=H[A]\) be connected and subcubic.
> Suppose the three edges of \(\delta_H(A)\) have distinct ends
> \(u_1,u_2,u_3\) in \(A\), so \(P\) has minimum degree two.  Let exactly
> one marked edge \(e\) lie internally in \(P\).  If
> \[
>  |\delta_H(X)|+|S\cap E(H[X])|\ge4
> \]
> for every cyclic \(X\subseteq A\), then \(P\) admits each of the three
> odd open states
> \[
>   (\{1,2\},1),\quad(\{1,3\},1),\quad(\{2,3\},1).
> \]

**Proof.**  First \(P\) has no bridge.  Otherwise consider a leaf \(K\)
of its bridge-component tree.  As in the two-mark shore lemma, \(K\) is
cyclic.  If \(p(K)\) is the number of pole boundary edges incident with
\(K\) and \(s(K)\in\{0,1\}\) records whether \(K\) contains the mark,
then the displayed inequality gives
\[
  1+p(K)+s(K)\ge4.
\]
Thus an unmarked leaf consumes at least three of the boundary edges, and
a marked leaf consumes at least two.  There are at least two leaves.  If
one contains the mark, it and any other leaf consume at least
\(2+3>3\) boundary edges; if none contains the mark, two leaves consume
at least \(3+3>3\).  Both are impossible.

Hence \(P\) is 2-edge-connected.  Because it is subcubic with minimum
degree two, it is 2-connected by the cutvertex argument in the preceding
proof.  Fix two distinct boundary ends \(u_i,u_j\), add a new edge
\(u_i u_j\), and use the standard characterization of 2-connected
graphs that any two edges lie on a common circuit.  A circuit containing
both the new edge and \(e\), with the new edge deleted, is a
\(u_i\)-to-\(u_j\) path containing \(e\).  Together with boundary
semiedges \(i,j\), this path is the state \((\{i,j\},1)\): it contains
the sole mark, has no closed component, and its open path has odd marked
parity.  The argument works for all three boundary pairs. \(\square\)

Consequently, for an unmarked \(1+3\) cyclic three-cut, the one-mark
signature creates no compatibility obstruction.  It remains only to
prove that the three-mark shore has at least one odd open state (or to
construct a shore satisfying all inherited hypotheses but having none).

The isolated three-mark assertion is bypassed in the new global proof
draft `four-mark-core-closure.md`.  It decomposes all surviving unmarked
\(1+3\) cuts at once.  The weighted 3-sum tree has a central cyclically
\(4\)-edge-connected factor and one-mark branches.  Precolouring all
four marks with one Tait colour makes the central marks and the
same-colour cap edge for every branch into a matching of at most four
distinct edges.  Aldred--Ellingham--Hemminger--Holton handles four
selected edges; Knappe--Pitz handles the smaller set that can arise when
adjacent cap roots share their selected edge.  The one-mark shore lemma
then substitutes the branches back into the selected cycle.

The same proof also reduces cuts containing marked boundary edges.
Two marked cut edges force a pair of one-mark paths.  With one marked
cut edge, the Knappe--Pitz \(g(3)=3\) theorem gives a cycle through the
marked cap edge and the two internal marks on one shore; a one-mark path
on the other shore completes a four-mark circuit.  An independently
prompted Codex referee agent audited the decomposition proof and
reported the stated binary-cycle theorem sound; this is an AI-agent
audit, not independent human verification.

## 3. Exact gluing theorem

> **Three-cut signature theorem.**  The marked cubic graph \(H\) has a
> binary cycle containing every marked edge and having an even number of
> marks on every circuit component if and only if either
>
> 1. both shores admit the closed state \(0\); or
> 2. for some boundary pair \(I\) and parity \(\epsilon\), both shores
>    admit the same open state \((I,\epsilon)\).

**Proof.**  Let \(Q\) be a binary cycle of \(H\).  The parity of a cut
gives
\[
 |Q\cap B|\equiv0\pmod2.
\]
Since \(B\) has size three, \(Q\) uses either zero or two boundary edges.

If it uses zero, its restriction to each shore is a disjoint union of
circuits.  The global even-mark condition is exactly the closed
admissibility condition on both shores.

If it uses the pair \(I\), the restriction to either shore has exactly
two odd boundary ends.  Because every internal vertex has degree zero or
two in \(Q\), that restriction consists of one path joining the two
chosen boundary ends and some disjoint circuits.  Every circuit entirely
inside a shore must contain an even number of marks.  The two open paths
glue through the two selected cut edges to form one global circuit.  That
circuit has an even number of marks exactly when the two path parities
are equal.  Hence the two shores have the same state
\((I,\epsilon)\).

Conversely, gluing two closed states gives the required global binary
cycle.  Gluing matching open states joins their paths into one circuit;
its marked-edge count is
\(\epsilon+\epsilon=0\) in \(\mathbb F_2\), while every other circuit was
already even.  All marked edges are retained in either case.  \(\square\)

By the even-marked circuit criterion, the theorem is equivalently an
exact seven-state gluing rule for packing two edge-disjoint \(T\)-joins.
No SAT assumption enters the proof.

## 4. The stable-triple sums always pack

For the order-20 base used below, the finite search can be replaced by a
short certificate.  Write
\[
 a=(3,11),\qquad b=(6,15),\qquad c=(7,18).
\]
For each pair of marks, the following three rows are circuits of the base
graph:

| marks | circuit |
|:---|:---|
| \(a,b\) | \(2,16,6,15,5,12,3,11,4,17,7,19,2\) |
| \(a,b\) | \(0,8,14,6,15,5,12,3,11,0\) |
| \(a,b\) | \(0,8,14,1,15,6,16,2,19,7,17,4,13,3,11,0\) |
| \(a,c\) | \(1,9,18,7,17,4,11,3,12,5,15,1\) |
| \(a,c\) | \(0,8,14,1,9,18,7,19,2,16,5,12,3,11,0\) |
| \(a,c\) | \(0,8,14,6,16,2,10,18,7,17,4,13,3,11,0\) |
| \(b,c\) | \(0,11,4,17,7,18,9,1,14,6,15,5,12,0\) |
| \(b,c\) | \(1,9,18,7,19,2,16,6,15,1\) |
| \(b,c\) | \(0,11,4,17,7,18,10,2,16,6,15,5,12,0\) |

For each fixed pair, the intersection of the vertex sets of its three
displayed circuits is exactly the four endpoints of the two marks.
Consequently, deleting any vertex not incident with the retained marks
leaves at least one displayed circuit through both marks.  That circuit
is a closed admissible state: it contains both marks, so its unique
component has an even marked-edge count.

> **Stable-triple sum corollary.**  Every vertex three-sum of two copies
> of this base, retaining two of \(a,b,c\) on each side and deleting no
> retained-mark endpoint, packs two edge-disjoint \(T\)-joins for the four
> retained marks.

**Proof.**  The displayed circuit certificate gives the closed state on
each shore.  Apply the closed-state case of the three-cut signature
theorem.  \(\square\)

Thus the absence of a nonpacking witness in the structured screen is
proved directly for the entire construction class; universal Tait
separation and the marked cut inequality are not needed for this
particular conclusion.

## 5. Frozen structured screen

The base graph is the order-20 cubic graph

```text
S????A?O@?R?d?EGGSAK?H_?HG?Ao@A_?
```

with three marked edges
\[
 (3,11),\qquad(6,15),\qquad(7,18).
\]
The triple is separated in every proper three-edge-colouring and obeys
the exact marked cyclic-cut condition, but it packs.

`scratch/generate_marked_three_sums.py` takes two copies, retains any two
of the three marks on each side, deletes any vertex not incident with a
retained mark, and tries all six bijections between the resulting
three-edge boundaries.  Therefore it emits exactly
\[
 3\cdot3\cdot16\cdot16\cdot6=13\,824
\]
labelled graph6 rows.  The four retained marks are always relabelled to
`0-1,2-3,4-5,6-7`.

Piping that stream into
`scratch/tait_all_coloring_mark_separation` with

```text
--target 4
--required-edge-ends 0-1,2-3,4-5,6-7
--require-nonpacking
--marked-cyclic-connectivity 4
```

finds 288 rows on which all four required marks remain separated in every
Tait colouring and finds zero witnesses satisfying both nonpacking and
the exact marked cyclic-cut condition.

The exact command, counts, environment, generator/checker hashes, and
SHA-256 of the generated 13,824-row stream are frozen in
`scratch/marked-three-sums-13824-result.json`.

The finite result independently exercises the marked-core checker, while
the circuit table above proves its zero-witness conclusion without
search.  It still does not prove a universal three-cut reduction.  The
remaining local statement is to show that universal Tait separation
together with the marked cyclic-cut inequality forces compatible
seven-state signatures on arbitrary shores.  The theorem above states
exactly what must be proved or falsified.

A separate exact diagnostic used
`scratch/analyze_separated_triple_poles.py` on complete host screens.
For every universally separated marked triple supplied by the screen,
it deleted each eligible vertex, checked the exact local marked-cut
condition, and enumerated the resulting pole's admissible odd boundary
states directly from its binary cycle space.  The eligible-pole counts
were \(12\) at order \(16\), \(162\) at order \(18\), and \(427\) at
order \(20\).  Every one of these \(601\) poles admitted all three odd
states.  The order-\(20\) host screen covered the complete canonical
corpus of \(510\,489\) connected simple cubic graphs and found \(183\)
hosts with a universally separated triple.  These are finite
diagnostics, not a proof of the isolated three-mark shore statement.
The new global closure bypasses that isolated statement rather than
proving it.

There is also no universally separated triple at all in the
cyclically \(4\)-edge-connected part of the complete order-\(22\)
canonical connected simple cubic corpus.  The exact screen decoded
\(7\,319\,447\) graphs and enumerated \(95\,360\,112\) Tait colourings
modulo global colour permutation on its \(7\,174\,735\) colourable rows.
The frozen metadata and hashes are in
`scratch/order22-cyclic4-separated3-result.json`.  By contrast, the two
3-edge-connected order-\(20\) hosts with a separated triple both have a
cyclic three-edge cut splitting the marks \(1+2\), while all other
order-\(20\) hosts have a cyclic two-edge cut.  This motivates, but does
not prove, the sharper structural possibility that every universally
separated triple is exposed by a cyclic cut of size at most three.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the stable marked
triple, ran the exploratory three-sum screen, formulated the seven-state
signature, proved the gluing theorem, extracted the nine-circuit
certificate, and wrote the frozen generator and this note.  The proofs
and circuit table are intended for line-by-line human checking.  The
finite computation is not independent human verification.
