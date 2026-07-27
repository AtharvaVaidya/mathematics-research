# Cycle translations obstruct rigid rooted three-poles

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE NECESSARY CONDITION / NOT A UNIVERSAL
NONRIGIDITY THEOREM**.

The cyclic-three-cut factorization in
`exceptional-cyclic-three-root-signature-factorization.md` shows that
one orientation of the exceptional four-type signature requires a
rooted cubic three-pole whose distinguished proper edge has one exact
possible label.  This note proves two structural restrictions on such
a pole:

1. in the reduced cap geometry, the distinguished edge is a
   nonbridge of its shore; and
2. every cycle through it must carry a translation-blocking set of
   \(D_5\)-labels.

The second restriction has a short graph-theoretic classification.  It
does not by itself prove that a nonbridge singleton root is impossible.

## 1. The \(D_5\) flow model

Identify a label in
\[
                       D_5=\binom{[5]}2
\]
with its two-element incidence vector in the even subspace
\[
 \Gamma=\{x\in{\mathbb F}_2^5:\text{\(x\) has even weight}\}.
                                                               \tag{1}
\]
Addition in \(\Gamma\) is symmetric difference.

At a cubic vertex, three incident \(D_5\)-labels satisfy coordinate
parity precisely when their sum is zero.  Any such triple consists of
the three edges of a triangle in \(K_5\): if two labels \(ab,ac\)
share \(a\), their sum is \(bc\).  Conversely every triangle has zero
sum.

Let \(Q\) be a cubic three-pole with ordered connector labels
\[
                          (01,02,12),                           \tag{2}
\]
and let \(r\) be a proper edge.  A **root labelling** is a
\(D_5\)-labelling of all proper edges and semiedges satisfying parity
at every internal vertex and (2).

## 2. Translating a proper cycle

> **Lemma 2.1 (cycle translation).**  
> Let \(\lambda\) be a root labelling, let \(C\) be a proper cycle of
> \(Q\), and let \(h\in\Gamma\).  If
> \[
>                         \lambda(e)+h\in D_5
>                    \quad\text{for every }e\in E(C),           \tag{3}
> \]
> then replacing \(\lambda(e)\) by \(\lambda(e)+h\) on every member
> of \(C\), and changing no other label, gives another root
> labelling.

### Proof

Every vertex of \(C\) is incident with exactly two edges of \(C\).
The change in its incident-label sum is therefore \(h+h=0\).
Vertices outside \(C\) are unchanged.  A proper cycle contains no
connector semiedge, so (2) is unchanged.  Condition (3) says exactly
that all translated edge values remain in the allowed set
\(D_5\). \(\square\)

For a cycle \(C\), let
\[
 S_C=\{\lambda(e):e\in E(C)\}\subseteq E(K_5)                   \tag{4}
\]
be its set of distinct labels, viewed as an ordinary edge set on five
coordinate vertices.

> **Lemma 2.2 (translation blockers).**  
> The only \(h\in\Gamma\) satisfying
> \[
>                         A+h\in D_5
>                    \quad\text{for every }A\in S_C             \tag{5}
> \]
> is \(h=0\) if and only if the graph \(([5],S_C)\)
>
> 1. spans all five coordinate vertices; and
> 2. is either non-bipartite or is the four-edge star \(K_{1,4}\).

### Proof

The nonzero elements of \(\Gamma\) have weight two or four.

First let \(h\) have weight four, say
\[
                           h=[5]\setminus\{v\}.
\]
For \(A\in D_5\), the symmetric difference \(A+h\) has weight two
exactly when \(A\) avoids \(v\).  Thus this \(h\) satisfies (5)
exactly when \(v\) is absent from the edge set \(S_C\).  All weight-four
translations are blocked precisely when \(S_C\) spans \([5]\).

Now let \(h=B\) have weight two.  For \(A\in D_5\), the sum \(A+B\)
again has weight two exactly when
\[
                              |A\cap B|=1.                      \tag{6}
\]
Consequently \(B\) satisfies (5) exactly when every edge in \(S_C\)
crosses the cut
\[
                              B\mid([5]\setminus B).            \tag{7}
\]

Consecutive labels on \(C\) share exactly one coordinate, because
they are two members of the local triangle at their common vertex.
Hence the edge set \(S_C\) is connected under edge adjacency, and
the graph \(([5],S_C)\) is connected on the vertices it uses.

Assume now that it spans all five vertices.  If it is non-bipartite,
it is contained in no cut, so (7) is impossible for every two-set
\(B\).  If it is bipartite, connectedness makes its bipartition
unique.  A \(2+3\) bipartition supplies exactly the admissible
weight-two translation in (7).  A \(1+4\) bipartition can be connected
and spanning only if all four edges from the singleton side occur;
the graph is then \(K_{1,4}\).  No side of that bipartition has size
two, so no weight-two translation is admissible.

Combining the weight-four and weight-two cases proves both
directions. \(\square\)

The inclusion-minimal connected blockers are easy to visualize.  Up
to relabelling the five coordinates, they are:

1. the star \(K_{1,4}\);
2. a triangle with two pendant edges attached at two different
   triangle vertices (the bull graph); and
3. the five-cycle \(C_5\).

Indeed, a connected spanning bipartite blocker is the star.  A
connected spanning non-bipartite graph contains a triangle or a
five-cycle.  Minimality gives \(C_5\) in the latter case.  Starting
from a triangle, the two unused vertices must attach separately at
different triangle vertices: attaching both at one vertex contains a
star, while attaching them by a path leaves a triangle plus a
disjoint edge after deleting the joining edge and is not
inclusion-minimal.

A literal \(2^{10}-1\)-support replay checks the classification without
being needed by the proof.  Of 968 connected nonempty edge supports,
538 are translation blockers.  The 77 inclusion-minimal connected
blockers split as five stars, 60 labelled bull graphs, and twelve
labelled five-cycles.  The Python producer and independently written
JavaScript verifier are:

```text
scratch/rooted_cycle_translation_blockers.py
scratch/rooted-cycle-translation-blockers-result.json
scratch/verify_rooted_cycle_translation_blockers.mjs
```

## 3. Consequence for an exact singleton root

The stabilizer of the ordered word (2) only swaps coordinates \(3\)
and \(4\).  Its fixed \(D_5\)-labels are
\[
                            01,\quad02,\quad12,\quad34.         \tag{8}
\]

> **Theorem 3.1 (cycle-support obstruction).**  
> Suppose the exact root signature of \((Q,r)\) is the singleton
> \(\{A\}\), where \(A\) is one of the four labels in (8).  If \(r\)
> is a nonbridge, then in every root labelling and on every proper
> cycle \(C\) containing \(r\), the label graph
> \(([5],S_C)\) spans all five coordinates and is either
> non-bipartite or \(K_{1,4}\).

### Proof

Because \(r\) is a nonbridge, it lies on a proper cycle.  If the label
support of such a cycle were not a blocker, Lemma 2.2 would give a
nonzero \(h\) satisfying (3).  Lemma 2.1 would then produce a second
root labelling in which the label of \(r\) is \(A+h\).  This is a
member of \(D_5\) different from \(A\), contradicting the exact
singleton signature.  Lemma 2.2 supplies the stated classification.
\(\square\)

Thus a singleton nonbridge cannot be witnessed by a root-cycle using
only three coordinate names, by any nonspanning label support, or by
a spanning \(2+3\)-bipartite support.  This is a search constraint and
a possible starting point for a reducibility argument; it is not yet
the missing proof that every nonbridge root admits a second label.

## 4. The cap roots are nonbridges

Return to the reduced cap
\[
                           G=P+\{e,f\}
\]
and the cyclic three-edge cut from Theorem 5.2 of
`exceptional-four-pole-simple-cap-enumeration-reduction.md`.
Cutting its three members produces rooted shores
\((Q_1,e)\) and \((Q_2,f)\).

> **Lemma 4.1 (shore-root nonbridge).**  
> If \(G\) is bridgeless cubic and has no cyclic two-edge cut, then
> neither \(e\) nor \(f\) is a bridge of its rooted shore.

### Proof

Suppose, by symmetry, that \(e\) is a bridge of \(Q_1\).  Its deletion
splits \(Q_1\) into two connected vertex sets \(X,Y\).  Let \(k\) of
the three cut connectors be incident with \(X\).  The cases \(k=0\)
and \(k=3\) would make \(e\) a bridge of \(G\), so \(k\in\{1,2\}\).
Choose \(Z=X\) when \(k=1\) and \(Z=Y\) when \(k=2\).  Exactly two
edges of \(G\) leave \(Z\): the root \(e\) and one connector.

The shore \(Z\) is connected.  If it has \(n\) vertices and \(m\)
internal edges, cubic degree counting gives
\[
                              3n=2m+2,
\]
and hence
\[
                              m-n+1=n/2>0.                      \tag{9}
\]
So \(Z\) contains a cycle.  The complement is connected through the
other rooted component, the opposite three-cut shore, and the two
remaining connectors; the same degree count shows that it too
contains a cycle.  The two leaving edges therefore form a cyclic
two-edge cut of \(G\), contrary to hypothesis.  Thus \(e\) is a
nonbridge, and the proof for \(f\) is identical. \(\square\)

In the minimum exceptional-pole branch, Theorem 5.2 already proves
that \(G\) has no cyclic two-edge cut.  Therefore the equality-only
orientation of the exceptional four-type signature requires two
nonbridge rooted shores satisfying Theorem 3.1.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the cycle-translation
argument, reduced its admissible shifts to cuts of \(K_5\), proved the
translation-blocker classification and the cap-root nonbridge lemma,
and drafted this note.  Every mathematical step is displayed for
line-by-line human checking.  This is not independent human review and
does not resolve the exceptional-signature conjecture or the
Five-Cycle Double Cover Conjecture.
