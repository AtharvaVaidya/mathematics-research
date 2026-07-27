# A Tait-colourable cap forces rooted base-pair closure

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE UNIVERSAL LEMMA / CORRECTED ONE-SIDED
CYCLIC-THREE CONSEQUENCE / NOT FIVE-CDC**.

Fix a rooted cubic three-pole \((Q,r)\) whose ordered connector word is
\[
                           (01,02,12).
\]
Let \(\widehat Q\) be the cubic graph obtained by adjoining one cap vertex
to the three connector ends.  Recall the three base pairs
\[
\begin{aligned}
 P_0&=\{12,03,04\},\\
 P_1&=\{02,13,14\},\\
 P_2&=\{01,23,24\}.
\end{aligned}                                                    \tag{1}
\]

The open base-pair target asks whether every nonempty root signature of a
nonbridge root contains one of (1).  The following substantial special
case is unconditional.

> **Tait-cap closure theorem.**  
> If \(\widehat Q\) is three-edge-colourable and \(r\) is a nonbridge of
> the proper core of \(Q\), then
> \[
>                       P_i\subseteq{\cal R}(Q,r)
> \]
> for some \(i\in\{0,1,2\}\).

## Proof

Fix a Tait colouring of \(\widehat Q\).  The three edges at the cap vertex
have three distinct colours.  Map their colours, in physical connector
order, to
\[
                            01,\quad02,\quad12.                  \tag{2}
\]
Give every edge with one of these three Tait colours the corresponding
label in (2).  At every cubic vertex the incident labels are the three
edges of the triangle on \(\{0,1,2\}\), and hence have symmetric-difference
sum zero.  Deleting the cap vertex gives a root labelling of \(Q\) with
the required connector word.

The root \(r\) receives one of \(01,02,12\).  Because it is a nonbridge,
it lies on a proper cycle \(C\) of \(Q\).  No connector semiedge belongs
to \(C\).

First translate every label on \(C\) by the even vector
\[
                              h_3=0123.
\]
The only labels occurring on \(C\) before the translation are those in
(2), and
\[
               01+h_3=23,\qquad02+h_3=13,\qquad12+h_3=03.       \tag{3}
\]
Thus all translated values are still members of \(D_5\).  At each vertex
of \(C\), exactly two incident labels change by \(h_3\), so the
vertex sum changes by \(h_3+h_3=0\).  The connector word is unchanged.
Consequently (3) gives a second root labelling.

Repeat with
\[
                              h_4=0124.
\]
Now
\[
               01+h_4=24,\qquad02+h_4=14,\qquad12+h_4=04.       \tag{4}
\]
This gives a third root labelling.

If the original root label is \(12\), equations (3)--(4) realize
\(12,03,04=P_0\).  If it is \(02\), they realize
\(02,13,14=P_1\).  If it is \(01\), they realize
\(01,23,24=P_2\).  This proves the theorem. \(\square\)

The proof is constructive.  Given a Tait colouring and any proper cycle
through \(r\), it writes the three required \(D_5\)-labellings explicitly.
It uses no enumeration and no orientability condition.

## Exceptional cyclic-three consequence

Return to the cyclic-three factorization of
`exceptional-cyclic-three-root-signature-factorization.md`.  Its two
rooted shores are \((Q_1,e)\) and \((Q_2,f)\), and Lemma 4.1 of
`rooted-cycle-translation-obstruction.md` proves that both roots are
nonbridges.

> **Corrected corollary.**
>
> 1. If either one-vertex shore cap
>    \(\widehat Q_1,\widehat Q_2\) is three-edge-colourable, then the
>    glued four-pole cannot have the disjointness-only relation
>    \(\{\mathsf D\}\), and cannot have the equality-only relation
>    \(\{\mathsf E\}\).
> 2. If both shore caps are three-edge-colourable, the glued four-pole
>    cannot have any of the three exceptional relation sets
>    \[
>       \{\mathsf E\},\qquad
>       \{\mathsf E,\mathsf I\},\qquad
>       \{\mathsf D\}.
>    \]

For the first assertion, the theorem puts a base pair \(P_i\) inside
one root signature \(R\).  The other root signature \(S\) is nonempty
and invariant under \(3\leftrightarrow4\).  The orbit table in
Lemma 1.2 of `rooted-three-pole-base-pair-closure-target.md` shows that
\(\operatorname{rel}(R,S)\) is neither equality-only nor
disjointness-only.  Thus the exceptional \({\cal E}_5\) relation is
excluded, as is the equality-only orientation of \({\cal E}_4\).

For the second assertion, the two Tait caps supply
\(P_i\subseteq R\) and \(P_j\subseteq S\).  Lemma 1.1 of the cited
note gives
\[
 \{\mathsf I,\mathsf D\}\subseteq
 \operatorname{rel}(P_i,P_j)
 \subseteq\operatorname{rel}(R,S),
\]
which excludes all three exceptional sets.

The mixed relation cannot be removed one-sidedly.  For example,
\[
 P_0=\{12,03,04\},\qquad
 S=\{01\},\qquad R=P_0\cup\{01\}
\]
are stabilizer-invariant and satisfy
\[
                  \operatorname{rel}(R,S)
                  =\{\mathsf E,\mathsf I\}.
\]
More precisely, put
\[
 A_0=\{01,02\},\qquad A_1=\{01,12\},\qquad
 A_2=\{02,12\}.
\]
If \(P_i\subseteq R\) and
\(\operatorname{rel}(R,S)=\{\mathsf E,\mathsf I\}\), the same orbit
table forces
\[
                         \varnothing\ne S\subseteq A_i
 \quad\text{and}\quad R\cap S\ne\varnothing.             \tag{5}
\]
These are necessary constraints, not an exclusion.

There is also a useful decomposition form.  Under the vertex-minimal
and two-cut-reduced hypotheses of the simple-cap fork, every nontrivial
cyclic three-cut separates the two cap edges \(e,f\).  The cap is in
fact 3-connected.  The fork already proves that it is simple,
bridgeless, cubic, and has no cyclic two-edge cut.  A cutvertex in a
bridgeless cubic graph would leave one component attached by only one
of the three incident edges, making that edge a bridge.  If
\(\{u,v\}\) were a two-vertex cut, every component of
\(G-\{u,v\}\) would have at least three boundary edges: a smaller
boundary would be a bridge or, by cubic degree counting and simplicity,
a cyclic two-edge cut.  The six incidences at \(u,v\) then force
\(uv\notin E(G)\), exactly two components with three boundary edges
each, and a \(2+1\) attachment to \(u,v\).  Adjoining to one component
the vertex receiving two of its boundary edges exposes a cyclic
two-edge cut, a contradiction.

Thus the published cubic three-sum decomposition theorem applies.  Its
factor-incidence tree is a path:
an edge off the \(e\)-to-\(f\) path would expose a terminal-free cyclic
shore, which the exact three-cut replacement removes.  Applying the
corrected corollary to the cuts adjacent to the two ends gives the
following scoped conclusions.

- For the \({\cal E}_5\) signature, both endpoint factors containing
  \(e\) and \(f\) are non-three-edge-colourable.
- For \({\cal E}_4(i;j,k)\), an endpoint factor is non-three-edge-colourable
  whenever its adjacent decomposition cut has pairing \(i\), the
  equality-only orientation.  A Tait-colourable endpoint is possible
  only when that cut has pairing \(j\) or \(k\), and then the opposite
  root signature satisfies (5).

If the decomposition tree has one node, that node is the cap \(G\)
itself and is non-three-edge-colourable by the simple-cap theorem.

This path restriction does not eliminate the branch.  A three-sum path
may retain the mixed \({\cal E}_4\) orientation at a Tait endpoint, and
the universal base-pair theorem for non-Tait factors remains open.

## AI-use disclosure

OpenAI Codex, under human direction, identified the two four-coordinate
cycle translations and drafted this proof.  Every mathematical step is
displayed above for line-by-line human checking.  This is not independent
human peer review and is not a resolution of the Five-Cycle Double Cover
Conjecture.  A later hostile audit found and corrected an overstrong
one-sided exceptional corollary; the explicit set-system counterexample
is displayed above.
