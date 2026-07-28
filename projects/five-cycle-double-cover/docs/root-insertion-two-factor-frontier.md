# Root insertion and the two-factor interlacing frontier

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE LOCAL LEMMAS / EXACT FINITE SCREEN /
UNIVERSAL INTERLACING STEP OPEN**.

## 1. Purpose and honest outcome

Let \(G\) be a finite simple cubic graph and let
\(R=\{r_1,r_2\}\) be independent edges.  Put
\(U=V(r_1)\cup V(r_2)\) and \(H=G-U\).  The focused matching problem asks,
when \(\operatorname{def}(H)=2\), for a maximum matching \(P\) of \(H\)
such that
\[
                         G-(R\cup P)
\]
is bridgeless.  Its two-branch core is then a theta rather than a
loop--link--loop dumbbell.

This note isolates a particularly small class of candidate matchings.
Start with a perfect matching containing one root and insert the other
root by deleting the two matching edges at its endpoints.  The
bridgelessness of the resulting complement has an exact two-factor
interlacing criterion.

The construction is not universal: exact failures occur in the retained
non-Tait corpus from order 24 onward.  However, every one of the 807
deficient instances with an all-singleton canonical
Gallai--Edmonds \(D\)-set through order 28 has such a local witness.
Thus the construction loses no instance in the exact singleton branch
currently under study.

The finite observation is not a proof of the universal singleton lemma,
the focused perfect-or-theta alternative, or the Five-Cycle Double Cover
Conjecture.

## 2. The root-insertion construction

Let \(M\) be a perfect matching of \(G\) with
\[
                         r_1\in M,\qquad r_2\notin M.
\]
Write
\[
                         r_2=uv
\]
and let \(ux,vy\) be the two edges of \(M\) incident with \(u,v\).
The roots are independent, so these three matching edges are pairwise
disjoint.  Define
\[
                    N=M-\{ux,vy\}+\{uv\}.              \tag{2.1}
\]

> **Lemma 2.1 (local insertion).**
>
> \(N\) is a matching containing \(r_1,r_2\), and its only exposed
> vertices are \(x,y\).  Moreover,
> \[
>       G-N=(G-M)-uv+\{ux,vy\}.                         \tag{2.2}
> \]
> If \(\operatorname{def}(H)=2\), then
> \(P=N-R\) is a maximum matching of \(H\).

### Proof

Deleting \(ux,vy\) from the perfect matching \(M\) exposes
\(u,v,x,y\).  Adding \(uv\) covers \(u,v\), leaving exactly \(x,y\).
The edge \(r_1\) is disjoint from all four vertices and remains in the
matching.  Taking edge complements gives (2.2).

The matching \(P=N-R\) lies in \(H\) and has
\[
                 |P|=|M|-1-2=\frac{|V(G)|-6}{2}.
\]
When \(\operatorname{def}(H)=2\), this is the maximum possible size in
the \(|V(G)|-4\)-vertex graph \(H\). \(\square\)

If no perfect matching contains both roots, then any perfect matching
containing \(r_1\) automatically omits \(r_2\).  This is exactly the
deficiency-two situation: a perfect matching of \(H\) would extend
\(\{r_1,r_2\}\) to a perfect matching of \(G\).

## 3. Exact interlacing criterion

Put
\[
                            L=G-M.
\]
Since \(G\) is cubic and \(M\) is perfect, \(L\) is a spanning
2-factor.  Let \(Z\) be the cycle of \(L\) containing \(uv\), and let
\[
                            Q=Z-uv
\]
be the resulting \(u\)-to-\(v\) path.

> **Theorem 3.1 (two-factor criterion).**
>
> The complement \(G-N=L-uv+\{ux,vy\}\) is bridgeless if and only if
> one of the following holds:
>
> 1. \(x\) and \(y\) lie on the same cycle of \(L\) distinct from
>    \(Z\); or
> 2. \(x,y\in V(Q)\) and their order on \(Q\), read from \(u\) to
>    \(v\), is
>    \[
>                         u,\ldots,y,\ldots,x,\ldots,v. \tag{3.1}
>    \]
>
> In either positive case the component containing \(x,y\) suppresses
> to a theta.  In every other case it suppresses to a dumbbell.

### Proof

Before the two new edges are added, \(L-uv\) consists of the path \(Q\)
and all the other cycles of \(L\).

If \(x,y\) lie on the same cycle \(C\ne Z\), the two arcs of \(C\)
together with the third path
\[
                         x u Q v y
\]
are three edge-disjoint \(x\)-to-\(y\) paths.  Every edge in their
union lies on a cycle, and all remaining components are cycles of
\(L\).  The complement is bridgeless.

If \(x,y\in V(Q)\) in the crossed order (3.1), the following are three
edge-disjoint \(x\)-to-\(y\) paths:
\[
 Q[x,y],\qquad xu+Q[u,y],\qquad Q[x,v]+vy.              \tag{3.2}
\]
Again the complement is a theta plus disjoint cycles.

It remains to inspect the other placements.  If \(x,y\) lie in
distinct components of \(L-uv\), at least one of \(ux,vy\) is a bridge
in the graph obtained after adding both.  This includes the case in
which exactly one of \(x,y\) lies on \(Q\), and the case in which they
lie on two different cycles outside \(Z\).

If both lie on \(Q\) in the noncrossed order
\[
                         u,\ldots,x,\ldots,y,\ldots,v,
\]
then \(Q[u,x]+xu\) and \(Q[y,v]+vy\) are two cycles joined by the
nonempty path \(Q[x,y]\).  Every edge in the interior of that joining
path is a bridge.  These cases exhaust the components of \(L-uv\).
\(\square\)

This theorem is useful because it replaces a search over arbitrary
near-perfect matchings by a concrete question about two marked matching
edges in a 2-factor.

## 4. The singleton branch already has a standard 5-CDC

Retain the all-singleton Gallai--Edmonds setting of
`singleton-ge-tait-frontier.md`.  Thus
\[
                  V(G)=D\mathbin{\dot\cup}W,\qquad
                  W=A\cup U,
\]
and \(D\) is independent.  Since every vertex of \(D\) has all three
neighbours in \(W\), the number of \(D\)--\(W\) edges is \(3|D|\).
The cubic degree sum on \(W\) then gives
\[
 \begin{split}
  2|E(G[W])|
    &=3|W|-3|D|\\
    &=3(|D|+2)-3|D|=6.
 \end{split}
\]
Consequently
\[
                         |E(G[W])|=3.                 \tag{4.1}
\]
In the boundary-eight notation these are
\(T=\{r_1,r_2,e\}\).  The same count also covers the boundary-six
singleton case, where the third edge lies inside \(U\).

> **Theorem 4.1 (singleton oddness bound).**
>
> Let \(G\) be a finite bridgeless cubic graph with a vertex partition
> \(V(G)=D\mathbin{\dot\cup}W\) such that \(D\) is independent,
> \(|W|=|D|+2\), and every edge not in \(E(G[W])\) joins \(D\) to \(W\).
> Then \(E(G[W])\) has three edges and
> \[
>                            \omega(G)\le2,             \tag{4.2}
> \]
> where \(\omega\) denotes oddness.  In particular, \(G\) has a
> standard 5-cycle double cover.

### Proof

Equation (4.1) proves the first assertion.  Choose any
\(t\in E(G[W])\).  Schönberger's edge-prescribed strengthening of
Petersen's perfect-matching theorem supplies a perfect matching \(M\)
containing \(t\): every edge of a bridgeless cubic graph lies in some
perfect matching.

Every vertex of \(D\) must be covered by a distinct \(D\)--\(W\) edge
of \(M\), because there are no \(D\)--\(D\) edges.  These
\(|D|\) matching edges also cover \(|D|\) vertices of \(W\).  Exactly
two vertices of \(W\) remain, and they must be covered by one
\(W\)--\(W\) edge.  Thus \(M\) contains exactly one of the three edges
of \(E(G[W])\), namely \(t\).

The complementary 2-factor \(L=G-M\) contains the other two
\(W\)--\(W\) edges.  Every other edge of \(L\) crosses the bipartition
\((D,W)\).  Along a cycle, crossing edges change bipartition class and
\(W\)--\(W\) edges do not.  Hence a cycle of \(L\) is odd precisely
when it contains an odd number of the two exceptional edges.  They
either lie on the same cycle, in which case every cycle is even, or on
two different cycles, in which case exactly those two cycles are odd.
This proves (4.2).

If the complementary 2-factor has no odd component, alternating two
colours on its cycles and using a third colour on \(M\) gives a
3-edge-colouring.  Its three bichromatic 2-factors form a cycle double
cover with three (hence at most five) members.  If the complementary
2-factor has two odd components, Huck and Kochol's five-cycle-double-cover
theorem applies (*J. Combin. Theory Ser. B* 64 (1995), 119--125,
DOI `10.1006/jctb.1995.1029`).  These are the only two cases, so the
proof is complete. \(\square\)

> **Corollary 4.2.**
>
> The all-singleton Gallai--Edmonds branch cannot contain a counterexample
> to the standard Five-Cycle Double Cover Conjecture.

This is a closure of the standard branch.  It does **not** solve the
stronger prescribed-root problem: the Huck--Kochol cover need not
realize the two roots as the exact zero set of the particular
\(\mathbb F_2^2\)-flow required by the fixed-five gluing construction.

### 4.1 The sharper local parity fact

For a local insertion arising from a maximum matching \(P=N-R\), the
perfect matching \(M\) contains \(r_1\) and omits both \(r_2\) and \(e\).
Indeed \(P\) is a maximum matching of \(H\), so it matches every
vertex of \(A\) to a distinct singleton of \(D\); it cannot use the
extra \(A\)--\(A\) edge.  In the \(A\)--\(U\) case, \(e\) is incident
with a root endpoint already covered either by the kept root or by one
of \(ux,vy\).

Consequently the only edges of the 2-factor \(L=G-M\) that do not cross
the bipartition \((D,W)\) are \(r_2\) and \(e\).

> **Lemma 4.3 (two odd cycles or a Tait colouring).**
>
> If \(r_2\) and \(e\) lie on the same cycle of \(L\), then every cycle
> of \(L\) is even and \(G\) is Tait-colourable.  If they lie on
> different cycles, those two cycles are odd and every other cycle of
> \(L\) is even.

### Proof

Along a closed walk, every \(D\)--\(W\) edge changes bipartition class
and every \(W\)--\(W\) edge does not.  Hence a cycle has the same parity
as the number of its edges in \(\{r_2,e\}\).  If both special edges lie
on one cycle, that cycle contains two and every other cycle contains
zero, so all cycles are even.  Colour \(M\) with one colour and
alternate the other two colours around the cycles of \(L\) to obtain a
Tait colouring.  If the special edges lie on different cycles, each of
those cycles contains one and is odd; the cycles containing neither
are even. \(\square\)

Thus non-Taitness forces the second outcome for every available local
insertion perfect matching.  Theorem 4.1 gives the standard 5-CDC
without needing this sharper root placement.  The local statement remains
useful only for the prescribed-root theta required by the fixed-five
construction.

## 5. Exact finite screen

The checker is

```text
scratch/focused-local-insertion-census.cpp
```

For each independent root pair it:

1. checks whether \(H=G-U\) has a perfect matching by exact bit-mask
   recursion;
2. for each orientation of the roots and each possible pair \(ux,vy\),
   enumerates every perfect completion \(M\);
3. constructs (2.1) literally and tests every edge of \(G-N\) for being
   a bridge;
4. reconstructs the canonical exposed set \(D\) by testing all pairs
   \(H-\{d,d'\}\) for a perfect matching;
5. calls the instance `singleton` exactly when \(D\) is independent
   and \(C=V(H)-(D\cup N_H(D))\) is empty.

It uses neither the full theta classifier nor any SAT solver.  Compile
and run it with

```sh
c++ -std=c++17 -O3 -Wall -Wextra -pedantic \
  scratch/focused-local-insertion-census.cpp \
  -o /tmp/focused-local-insertion-census

for n in 10 12 14 16 18 20 22 24 26 28; do
  /tmp/focused-local-insertion-census "$n" \
    "search/focused-theta-choice-through28-20260727/artifacts/"\
"cyclic4-nontait-order$n.g6"
done
```

The retained results are in
`scratch/focused-local-insertion-result.ndjson`.

| order | deficient pairs | local witnesses | all local failures | singleton pairs | singleton local failures |
|---:|---:|---:|---:|---:|---:|
| 10 | 15 | 15 | 0 | 15 | 0 |
| 12 | 0 | 0 | 0 | 0 | 0 |
| 14 | 0 | 0 | 0 | 0 | 0 |
| 16 | 0 | 0 | 0 | 0 | 0 |
| 18 | 25 | 25 | 0 | 3 | 0 |
| 20 | 67 | 67 | 0 | 18 | 0 |
| 22 | 275 | 275 | 0 | 15 | 0 |
| 24 | 1,334 | 1,330 | 4 | 33 | 0 |
| 26 | 11,186 | 11,064 | 122 | 129 | 0 |
| 28 | 108,676 | 106,876 | 1,800 | 594 | 0 |

The first unrestricted failure is the order-24 row

```text
W??Y@a??K?C@A??Cg?GE?P????oCO???[g??CG?K?C??A_@
```

with root edge indices \(\{1,3\}\).  An independent direct enumeration
finds 140 maximum matchings of \(H\), of which 48 have theta
complements, but none of the 24 root-insertion perfect completions has a
bridgeless complement.  Its canonical \(D\)-set has one 17-vertex
factor-critical component and two singletons, so it lies in the
one-boundary-five branch rather than the singleton branch.

The exact source and result hashes for this run are

```text
0f62b85c3d319c8d28b4c97d1b8d87e8502d9dc02224ee61097a2339bea38ad3  scratch/focused-local-insertion-census.cpp
32a7e02da46999694630edeee0755b490f328ae91d8b30017f229db2c41be05a  scratch/focused-local-insertion-result.ndjson
8b9773202bb1bbef46e175e4f6cb195c237f8b6bc633a0e684c82d728d28192b  scratch/focused-local-insertion-progress.log
```

### 5.1 Independent clean-room replay

Every row was replayed by
`scratch/verify-root-insertion-census.py`, a separately written Python
bit-mask implementation.  It independently parses graph6, enumerates
perfect and near-perfect matchings, reconstructs the Gallai--Edmonds
sets, applies the local-insertion construction, and tests
bridgelessness by its own low-link routine.  Orders 10 through 22 are
retained in `scratch/root-insertion-independent-through22.json`, and
orders 24 and 26 are retained in
`scratch/root-insertion-independent-through26.json`.

The order-28 corpus was split by graph index modulo four; the four shard
totals sum to

```text
graphs                       12,517
independent root pairs    9,725,709
deficient pairs             108,676
local witnesses             106,876
local failures                1,800
singleton pairs                 594
singleton local failures          0
```

Every aggregate total and the first unrestricted failure agree with the
C++ implementation.  The combined comparison is retained as
`scratch/root-insertion-independent-order28-combined.json`; it records
the four shard hashes and explicitly limits the claim to this finite
corpus.

The compact publication checker
`scratch/check-root-insertion-published.py` verifies all cross-implementation
comparisons, the four recorded shard hashes, the displayed totals, and the
zero singleton-failure claim without trusting either program's summary.

## 6. Exact remaining lemma

The finite results motivate the following strictly scoped statement.

> **Root-insertion interlacing lemma.**
>
> Under the finite, simple, cubic, cyclically 4-edge-connected,
> non-Tait, boundary-eight, all-singleton Gallai--Edmonds hypotheses,
> one root orientation has a perfect matching \(M\) for which the two
> mates at the other root satisfy one of the two interlacing conditions
> in Theorem 3.1.

This lemma would directly produce a theta maximum and close the
singleton side of the focused perfect-or-theta problem.  It is stronger
than the implication currently needed, because it specifies a
one-root insertion witness.

No proof is presently known.  The promising human route is to combine:

* Theorem 4.1, which supplies a 2-factor with at most two odd cycles,
  and Lemma 4.3, which sharpens the parity statement for every non-Tait local
  2-factor;
* the two surplus-one versus one surplus-two decomposition of the
  \(A\)--\(D\) incidence graph;
* perfect-matching exchanges that move the two exposed singleton
  vertices; and
* cyclic four-edge-connectivity, which forbids a fixed three-edge
  separation between the two odd cycles.

The first unrestricted computational failures show why the
all-singleton hypothesis cannot be dropped from that argument.

## 7. AI-use disclosure

The construction, proof organization, and checker were developed with
substantial assistance from OpenAI Codex under human direction.  Lemmas
2.1 and 4.1 and Theorem 3.1 are written out in full and are independently
readable.  The finite screen is evidence only.  No AI-generated argument
or bounded computation is presented as a proof of the root-insertion
interlacing lemma, the focused perfect-or-theta alternative, or the
Five-Cycle Double Cover Conjecture.

No novelty claim is made here for Theorem 4.1.  It is a short synthesis
of a degree count with classical perfect-matching and oddness results, and
may be known in equivalent language.  A graph-theory specialist should
check the proof, the scope of both cited theorems, and the literature
before treating it as publishable mathematics.
