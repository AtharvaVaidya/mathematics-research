# Exceptional terminal-distinct four-poles reduce to independent-edge deletions

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE ENUMERATION REDUCTION / FINITE SEARCH
ACCELERATOR / NOT AN EXCLUSION OF THE EXCEPTIONAL SIGNATURES**.

This note proves that the exceptional four-poles relevant to a simple
cubic minimum-counterexample branch can be enumerated through
bridgeless non-Tait cubic graphs.  It does not assume that either
exceptional signature is realizable.

The reduction is deliberately restricted to a connected simple proper
core whose four semiedges have four distinct internal endpoints.  That
is the terminal-distinct geometry obtained by cutting an independent
cyclic four-edge cut in a simple cubic graph.  It is not a statement
about arbitrary multipoles with repeated terminal endpoints.

## 1. Setup

Let \(P\) be a connected simple graph with terminal set
\[
                         T=\{t_1,t_2,t_3,t_4\}.
\]
Every terminal has proper degree two, and every other vertex has proper
degree three.  Attaching one semiedge at each member of \(T\) makes
\(P\) a terminal-distinct cubic four-pole.

There are three perfect matchings of the four-element set \(T\).  Call
one of them **simple for \(P\)** if neither of its two pairs is already
an edge of \(P\).  Adding the two pairs of a simple matching produces a
simple cubic graph; call it a **two-edge cap** of \(P\).

## 2. A simple cap always exists

> **Lemma 2.1 (simple cap matching).**  
> Every connected terminal-distinct proper core \(P\) has a simple
> perfect matching on \(T\).

### Proof

The six pairs of \(T\) are partitioned by the three perfect matchings
of \(K_4\).  Suppose every perfect matching contained an edge of
\(P[T]\).  Choose one such edge from each of the three matching
classes.  The chosen three-edge subgraph is either:

1. a three-edge star; or
2. a triangle.

For completeness, choose \(t_1t_2\) from the first matching.  The
second choice is \(t_1t_3\) or \(t_2t_4\), and the third is
\(t_1t_4\) or \(t_2t_3\).  The four combinations give respectively a
star at \(t_1\), a triangle on \(t_1,t_2,t_3\), a triangle on
\(t_1,t_2,t_4\), or a star at \(t_2\).

The star is impossible because its centre would have three neighbours
in \(T\), while every terminal has proper degree two.  In the triangle
case, each of the three triangle vertices already has both of its
proper incident edges inside the triangle.  The triangle is therefore
a connected component of \(P\), contrary to connectedness and the
presence of the fourth terminal.  Hence at least one of the three
perfect matchings uses two nonedges of \(P\). \(\square\)

## 3. The cap lies in the bridgeless non-Tait cubic corpus

Máčajová, Mazzuoccolo, and Tabarelli associate a looped \(K_4\)
signature graph \(P^*\) to an ordered cubic four-pole.  Their Lemma 3.8
states that if a connected cubic four-pole is 3-edge-colourable, then
every vertex of \(P^*\) has degree at least one.  In their notation the
two exceptional signatures are
\[
\begin{aligned}
 {\cal E}_4(i;j,k)&=\{AA,AT_j,AT_k,T_jT_k\},\\
 {\cal E}_5(i;j,k)&=\{T_iT_i,T_jT_j,T_kT_k,T_iT_j,T_iT_k\},
\end{aligned}                                           \tag{1}
\]
where \(\{i,j,k\}=\{2,3,4\}\).

For the finite 5-CDC application below, let \(P^*_5\) denote the same
type graph using only CDC-colourings whose colour universe is the fixed
five-set \(\{0,1,2,3,4\}\).  This restriction matters: the computation
does not classify colourings requiring more than five colours.  The
conclusion of their Lemma 3.8 remains valid for \(P^*_5\), because its
proof starts from one Tait colouring and explicitly constructs the
needed CDC-colourings with at most four colours.

The vertex \(T_i\) is isolated in \({\cal E}_4\), and the vertex \(A\)
is isolated in \({\cal E}_5\).  Thus their lemma immediately gives:

> **Lemma 3.1.**  
> A connected cubic four-pole whose exact fixed-five-colour signature
> \(P^*_5\) is either graph in (1) is not 3-edge-colourable.

We now add the graph hypotheses inherited by a minimum exceptional
shore.

> **Theorem 3.2 (simple-cap enumeration reduction).**  
> Let \(P\) satisfy the setup of Section 1, assume that no proper edge
> of \(P\) is a bridge, and assume that its exact ordered boundary
> signature in the fixed five-colour model is a member of one of the
> two exceptional families (1).
> Then some simple two-edge cap
> \[
>                         G=P+\{e,f\}
> \]
> is a connected simple bridgeless cubic graph which is not
> 3-edge-colourable.  The two cap edges \(e,f\) are independent, and
> deleting them recovers \(P\).

### Proof

Choose a simple perfect matching on \(T\) by Lemma 2.1 and add its two
edges \(e,f\).  They have four distinct endpoints and were nonedges of
\(P\), so \(G\) is simple and \(e,f\) are independent.  Every terminal
degree rises from two to three, hence \(G\) is cubic.  It is connected
because \(P\) is connected.

Every proper edge of \(P\) lies on a cycle of \(P\), since \(P\) has no
bridge.  Each new cap edge also lies on a cycle: its endpoints are
joined by a path in connected \(P\).  Therefore \(G\) is bridgeless.

If \(G\) had a Tait colouring, deleting \(e,f\) and retaining their
colours on the resulting semiedges would give a Tait colouring of the
cubic four-pole \(P\).  This contradicts Lemma 3.1.  Thus \(G\) is not
3-edge-colourable.  Deleting \(e,f\) plainly returns \(P\).
\(\square\)

## 4. Exact finite-search consequence

Fix an even order \(n\).  To exclude every bridge-free connected simple
terminal-distinct four-pole with an exceptional exact five-colour
signature on \(n\) internal vertices, it is sufficient to:

1. canonically generate every connected simple cubic graph \(G\) on
   \(n\) vertices;
2. retain exactly the bridgeless non-3-edge-colourable graphs;
3. delete every pair of independent edges \(e,f\); and
4. compute the ordered four-terminal signature of \(G-\{e,f\}\),
   testing every terminal permutation of both exceptional families.

Theorem 3.2 proves completeness: any exceptional pole in the stated
scope occurs at least once in this deletion corpus.  Duplicate caps or
isomorphic deleted-edge presentations do not affect completeness and
may be quotiented by automorphisms.

This reduction explains why the earlier complete order-18 snark-cap
census is not merely a sample of hard graphs: in the bridge-free
terminal-distinct scope it is an exhaustive exceptional-pole test.
The larger direct census of all degree-\((2,3)\) proper cores is an
independent superset check.

The reduction does not cover a bridge-bearing pole, a repeated-terminal
multipole, or a non-simple proper core.  Those objects are not the
shores of the independent cyclic four-cuts in the present simple cubic
minimum-counterexample branch.  Nor does a finite order bound prove
that the exceptional five-colour signatures are universally
unrealizable.  It also does not settle the broader unbounded-colour
formulation of the published Conjecture 3.7.

## 5. What a non-cyclically-four cap must expose

The same cap records the next exact structural fork.  Call \(P\)
**two-cut reduced** if it has no nontrivial proper two-edge-cut shore.
The cuts isolating one degree-two terminal are trivial; they are not
cycle-separating and are ignored here.

There is one further elementary replacement which parallels the
two-pole and three-pole replacements in
`four-pole-boundary-human-lemmas.md`.

> **Lemma 5.1 (terminal-free three-cut replacement).**  
> Let a proper three-edge cut of a positive cubic four-pole separate a
> connected shore containing none of its four original terminals.
> Replacing that shore by one cubic vertex preserves the pole's exact
> five-coordinate boundary signature.

### Proof

Cutting the three edges turns the shore into a cubic three-pole.
Summing coordinate parity over its vertices says that its three
boundary labels \(a,b,c\in D_5\) satisfy
\[
                         a\mathbin\triangle
                         b\mathbin\triangle c=\varnothing.
\]
Thus \(a,b,c\) are the three edges of a triangle on three coordinate
names.  All ordered such triangles form one orbit under \(S_5\).

If the three-pole admitted no boundary word, the original four-pole
would have empty signature.  Otherwise one partial labelling, followed
by global coordinate permutations, realizes every locally valid
ordered triangle.  A single cubic vertex has exactly the same boundary
relation.  Restriction and extension across the three cut edges prove
equality of the full four-terminal relations before and after
replacement. \(\square\)

> **Theorem 5.2 (cyclic-three-cut fork).**  
> Let \(P\) satisfy Theorem 3.2 and be two-cut reduced and
> vertex-minimal among poles with its exact positive fixed-five-colour
> boundary signature.  Let \(G=P+\{e,f\}\) be any simple two-edge cap supplied by
> Lemma 2.1.  Then exactly one of the following holds:
>
> 1. \(G\) is cyclically \(4\)-edge-connected; or
> 2. \(G\) has a cyclic three-edge cut disjoint from \(\{e,f\}\) which
>    splits the four terminals of \(P\) as \(2+2\).  One whole cap edge
>    lies internally on each shore.

### Proof

Theorem 3.2 makes \(G\) bridgeless.  It has no cyclic two-edge cut.
Indeed, let \(C\) be such a cut and put
\[
                         r=|C\cap\{e,f\}|.
\]
If \(r=2\), deleting the caps leaves no proper edge between the two
nonempty shores, contradicting connectedness of \(P\).  If \(r=1\),
the one remaining member of \(C\) is a bridge of \(P\).  If \(r=0\),
the same vertex partition is a proper two-edge cut of \(P\).  Because
both cap edges are internal to shores, each shore contains an even
number of terminals.  It therefore cannot be a trivial cut isolating
one terminal, contradicting two-cut reduction.

If \(G\) is not cyclically \(4\)-edge-connected, it consequently has a
cyclic three-edge cut \(C\).  Again put
\(r=|C\cap\{e,f\}|\).  The case \(r=2\) leaves a proper one-edge cut of
\(P\), and \(r=1\) leaves a nontrivial proper two-edge cut.  Both are
excluded.  In the latter case the two-cut cannot merely isolate one
terminal, because the corresponding shore of the cyclic cut in \(G\)
contains a cycle.  Hence \(r=0\).

Both cap edges are internal to the two shores, so their endpoint pairs
show that each shore contains an even number of the four terminals.
The possible distributions are \(0+4\) and \(2+2\), up to reversing
the shores.

The shores are connected: if one shore had two components, then
bridgelessness would give at least two cut edges incident with each
component, exceeding \(|C|=3\).  The three cut edges also have distinct
ends on either shore.  Otherwise moving a common endpoint across the
cut replaces two crossing edges by one, preserves a cycle on each
shore, and creates the cyclic two-edge cut already excluded.

In the \(0+4\) case, the terminal-free connected shore can therefore
be replaced by one cubic vertex using Lemma 5.1, while retaining a
simple proper core.  A cyclic shore has more than one vertex, so the
replacement strictly reduces the order while preserving the exact
positive signature, contrary to vertex minimality.  Thus the
distribution is \(2+2\).  Since each cap edge has both ends on one
shore and each shore contains exactly two terminals, one cap edge lies
on each shore. \(\square\)

The second outcome is a genuine five-pole interface: cutting three
proper edges from a shore already containing two original terminals
creates five boundary positions.  The theorem does not eliminate that
interface.  It says that a minimal exceptional atom which is not
represented by a cyclically \(4\)-edge-connected cap must advertise
itself through this one exact terminal-splitting configuration.

## Primary-source attribution

The exceptional signatures and the 3-edge-colourability condition used
in Lemma 3.1 are from:

E. Máčajová, G. Mazzuoccolo, and G. Tabarelli, “Cycle separating cuts
in possible counterexamples to the cycle double cover and the
Berge--Fulkerson conjectures,” *Ars Mathematica Contemporanea* **26**
(2026), #P2.03, Lemma 3.8, Theorem 3.10, and Conjecture 3.7,
<https://doi.org/10.26493/1855-3974.3409.c13>.

The version-of-record PDF was checked directly.  Its SHA-256 in this
audit was

```text
edb4852b0ab2708c395f149021f4118d63e38018adbea6e157164c77f6de6b49
```

## AI-use disclosure

OpenAI Codex agents, under human direction, found the simple-cap
enumeration reduction, supplied the elementary \(K_4\) transversal
proof, checked the imported statement against the version-of-record
paper, and drafted this note.  The full argument is displayed for
line-by-line human checking.  It is not independent human review and
does not resolve Conjecture 3.7 or the Five-Cycle Double Cover
Conjecture.
