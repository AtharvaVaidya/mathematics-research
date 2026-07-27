# Endpoint base-pair closure through factor order 26

Date: **2026-07-27**.

Status: **HUMAN REDUCTION PLUS TWO-IMPLEMENTATION FINITE
CLASSIFICATION / PURE-RELATION CYCLIC-THREE BOUND / NOT FIVE-CDC**.

## 1. Finite theorem

Let \(F\) be a cyclically \(4\)-edge-connected simple cubic graph of
even order at most \(26\).  Delete any vertex \(z\), regard its three
former incident edges as the ordered connector word
\[
                              (01,02,12),
\]
and distinguish any nonbridge proper edge \(r\) of \(F-z\).
If the resulting rooted three-pole has a nonempty fixed-five root
signature, then that signature contains one of
\[
 \{12,03,04\},\qquad\{02,13,14\},\qquad\{01,23,24\}.             \tag{1}
\]

For factor order at most \(18\), this is the complete rooted-order-17
theorem in `../rooted-three-pole-frontier-20260727/`.

For orders \(20,22,24,26\), split into two cases.  If \(F\) is
three-edge-colourable, the explicit cycle-translation proof in
`../../docs/rooted-three-pole-tait-cap-closure.md` gives (1) without
enumeration.  Otherwise \(F\) belongs to the complete retained
Snarkhunter sources of respectively
\[
                              6,\quad31,\quad155,\quad1297        \tag{2}
\]
cyclically \(4\)-edge-connected non-Tait simple cubic graphs.
Triangle exclusion makes the girth-four source complete for this
class, subject to Snarkhunter and its option semantics.

Deleting every vertex in (2) produces
\[
                              38\,244                              \tag{3}
\]
three-pole cores.  Independent incremental-CaDiCaL and direct
finite-domain implementations test every nonbridge proper root in
these cores.  Each tests
\[
                   1\,360\,452\text{ roots in }4\,157\,844
                   \text{ solver calls},                         \tag{4}
\]
with zero empty rows and zero violations.  Their complete transcripts
agree byte-for-byte and have uncompressed SHA-256
\[
\texttt{bfb90fd89b43e66f02ada87abcb87ab643d87a4b36dba616cd1f3e5d603b7364}.
\]
The independent `verify.py` reconstructs all sources and vertex
deletions, checks the graph premises, recomputes every nonbridge root
and adaptive decision, and reproduces `report.json`.

## 2. The simple cap is 3-connected

The three-sum decomposition used below really does apply in the
minimal simple-cap fork.  Here is the missing elementary argument.

> **Lemma (cap connectivity).**  
> Let \(G\) be a connected simple cubic bridgeless graph with no cyclic
> two-edge cut.  Then \(G\) is 3-connected.

### Proof

A cutvertex \(v\) is impossible.  The components of \(G-v\) receive
the three edges incident with \(v\); if there is more than one
component, one receives exactly one such edge, which is then a bridge.

Suppose that \(\{u,v\}\) is a two-vertex cut.  Every component \(D\) of
\(G-\{u,v\}\) has at least three boundary edges.  Indeed, it cannot
have one because \(G\) is bridgeless.  If it had two, then both shores
of that two-edge cut would contain cycles: for either shore \(X\),
cubic degree counting gives
\[
                       |E(G[X])|=(3|X|-2)/2,
\]
and simplicity excludes the only subcyclic small possibility
\(|X|=2\), which would require two parallel internal edges.  This
would be a forbidden cyclic two-edge cut.

The vertices \(u,v\) supply at most six boundary incidences to the
components.  Thus \(uv\notin E(G)\), there are exactly two components,
and each has three boundary edges.  Neither component attaches all
three edges to only one of \(u,v\), since that vertex would be a
cutvertex.  Relabel a component \(D\) so that it sends two edges to
\(u\) and one to \(v\).  Then
\(\delta_G(D\cup\{u\})\) has two edges.  The same cubic degree count
shows that both shores are cyclic, again a contradiction.  Therefore
there is no two-vertex cut. \(\square\)

The simple-cap fork proves that its cap \(G=P+\{e,f\}\) is simple,
bridgeless, and has no cyclic two-edge cut.  Hence the lemma supplies
the 3-connectivity premise of the standard cubic three-sum
decomposition theorem.

## 3. Correct cyclic-three consequence

Assume the vertex-minimal, two-cut-reduced, bridge-free connected
simple terminal-distinct fixed-five exceptional four-pole hypotheses
of
`../../docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`,
and let \(G=P+\{e,f\}\) be one of its simple caps.  If \(G\) has a
cyclic three-edge cut, every such cut separates \(e\) from \(f\).
The cap-connectivity lemma and the published decomposition theorem
therefore give a factor-incidence tree, and every tree edge lies on the
path between the factors containing \(e\) and \(f\).  The tree is a
path
\[
                              F_1,\ldots,F_k,\qquad k\ge2.        \tag{5}
\]

At either endpoint cut, deleting its virtual cap vertex gives the
rooted three-pole obtained from \(F_1\) or \(F_k\), and the distinguished
cap edge is a nonbridge.  Thus an endpoint factor of order at most
\(26\) has a root signature containing a base pair by Section 1.
The one-sided relation table in
`../../docs/rooted-three-pole-base-pair-closure-target.md` excludes
both equality-only and disjointness-only gluing whenever one shore
contains a base pair.  Consequently:

> **Pure-relation endpoint bound.**  
> If the exact relation at the cyclic three-cut is
> \(\{\mathsf E\}\) or \(\{\mathsf D\}\), then
> \[
>                       |V(F_1)|,|V(F_k)|\ge28.
> \]
> In particular,
> \[
>                              |V(G)|\ge54.                       \tag{6}
> \]

Indeed, every internal simple cubic factor has order at least four and
reversing the \(k-1\) vertex three-sums gives
\[
 |V(G)|=\sum_{i=1}^k|V(F_i)|-2(k-1)
 \ge28+28+4(k-2)-2(k-1)=2k+50\ge54.
\]
By the exact rooted factorization, (6) applies to the exceptional
five-type signature and to the equality-only orientation of the
exceptional four-type signature.

The mixed relation
\[
                         \{\mathsf E,\mathsf I\}                  \tag{7}
\]
is **not** excluded by one endpoint base pair.  Nor may base pairs in
the two endpoint factors of a path with \(k>2\) be treated as base
pairs on the two shores of one cut.  The finite classification therefore
does not by itself give an order bound for (7).  An explicit
set-system counterexample to the invalid one-sided inference is
displayed in the Tait-cap note.  Closing (7) requires a sound path
composition argument or a direct finite cap census.

## 4. Scope

The finite source completeness in (2) relies on Snarkhunter.  The
finite theorem covers vertex deletions of cyclically
\(4\)-edge-connected simple cubic factors, not arbitrary rooted
three-poles.  The order-54 conclusion covers only the two pure
relations.  It does not cover the mixed relation (7), repeated
terminals, nonsimple pole cores, arbitrary-colour CDC signatures, or
the orientable condition.

Nothing here resolves the Five-Cycle Double Cover Conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the endpoint-factor
reduction, ran the two rooted classifiers, wrote the independent
verifier, found the cap-connectivity repair, and drafted this proof.
Every finite artifact and human step is exposed for checking.  A
hostile audit corrected the earlier false claim that one base-pair
shore excludes the mixed relation; that claim is not used here.
