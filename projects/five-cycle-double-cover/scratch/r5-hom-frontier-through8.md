# The exact \(R_5\)-homomorphism frontier through eight vertices

## Result

Let \(R_5\) be the graph on \(\mathbb F_2^5\) in which two words are
adjacent when their Hamming distance is two.  For every simple graph \(J\)
on at most eight vertices,
\[
        J\longrightarrow R_5
        \quad\Longleftrightarrow\quad
        \chi(J)\leq 5.                                      \tag{1}
\]
Equivalently, the two minimal subgraph obstructions through order eight
are
\[
        K_6\qquad\hbox{and}\qquad K_3\mathbin{\vee}C_5.       \tag{2}
\]
Here \(\vee\) denotes graph join.

This statement has both a short human proof and a complete finite
certificate file.  The computation is a cross-check, not a premise of
the proof.

## Human proof

### The two target obstructions

The clique number of \(R_5\) is five.  Translate any clique so that one
vertex is \(0\).  Every other word then has weight two.  The supports of
these weight-two words are pairwise-intersecting two-subsets of a
five-set.  Such a family has at most four members: if all sets share a
point it is contained in a four-edge star; if
\(\{a,b\},\{a,c\}\) occur and some set misses \(a\), that set must be
\(\{b,c\}\), and no fourth set can be added.  Equality is attained by
\[
        0,\quad\{1,2\},\quad\{1,3\},\quad\{1,4\},\quad\{1,5\}.
\]
Consequently \(K_6\not\longrightarrow R_5\), while \(K_5\) is a
subgraph of \(R_5\).

Now suppose \(K_3\vee C_5\longrightarrow R_5\).  The triangle maps
injectively to a target triangle.  Translate and permute coordinates so
that its image is
\[
        0,\qquad \{1,2\},\qquad \{1,3\}.
\]
A direct two-subset calculation shows that the common neighbourhood of
these three target vertices is
\[
        \bigl\{\{2,3\},\{1,4\},\{1,5\}\bigr\}.
\]
The induced graph is \(K_1+K_2\).  Every vertex of the joined \(C_5\)
would have to map into this common neighbourhood.  A connected graph
with edges cannot map into its isolated vertex, and an odd cycle cannot
map to \(K_2\).  This is impossible.

### The eight-vertex critical dichotomy

We prove that every graph \(J\) on at most eight vertices with
\(\chi(J)\geq6\) contains one of (2).  Choose a vertex-minimal induced
subgraph \(F\) with \(\chi(F)\geq6\).  Deleting a vertex makes \(F\)
five-colourable, so adding that vertex back shows \(\chi(F)=6\).
Moreover,
\[
        \delta(F)\geq5,                                     \tag{3}
\]
because otherwise a five-colouring of \(F-v\) extends greedily to \(v\).

If \(|F|=6\), (3) gives \(F=K_6\).  If \(|F|=7\), the complement
\(\overline F\) has maximum degree at most one.  Since
\(\chi(F)=6\), that complement has exactly one edge; deleting either
endpoint of the missing edge from \(F\) leaves a \(K_6\).

It remains to take \(|F|=8\) and put \(D=\overline F\).  By (3),
\(\Delta(D)\leq2\), so every component of \(D\) is an isolated vertex,
a path, or a cycle.  A proper colouring of \(F\) is exactly a partition
of \(V(D)\) into cliques.  Write \(\theta(D)\) for the minimum number of
parts in such a partition and define its saving by
\[
        s(D)=|V(D)|-\theta(D).
\]
Vertex-criticality gives
\[
        \theta(D)=6,\qquad \theta(D-v)=5\quad(v\in V(D)),
\]
and hence
\[
        s(D)=s(D-v)=2\quad(v\in V(D)).                        \tag{4}
\]

Savings add over components.  Every nontrivial path or cycle with saving
at most two is in the following finite list:
\[
        P_2,P_3,P_4,P_5,C_3,C_4,C_5.
\]
Their savings are respectively
\[
        1,1,2,2,2,2,2.
\]
For each of the first six graphs, deleting a suitable vertex lowers the
saving.  For \(C_5\), deleting any vertex produces \(P_4\), whose saving
is still two.  Condition (4) therefore forces
\[
        D=C_5+3K_1,
\]
and hence
\[
        F=\overline D=K_3\vee C_5.
\]
This proves the dichotomy.

If \(\chi(J)\leq5\), a proper five-colouring maps \(J\) to the displayed
\(K_5\) in \(R_5\).  If \(\chi(J)\geq6\), the dichotomy puts one of the
two non-mappable graphs (2) inside \(J\).  This proves (1).  Both
obstructions are critical: deleting any vertex or edge makes them
five-colourable, so (2) is also the exact minimal list.

## Exhaustive certificate census

The producer
[`enumerate_r5_hom_frontier_order8.py`](enumerate_r5_hom_frontier_order8.py)
uses nauty 2.9.3 `geng` to generate every unlabeled simple graph of orders
one through eight.  For every positive instance it records a literal
image word in the even component of \(R_5\) for every source vertex.
For every negative instance it records either six clique vertices or the
triangle/cycle decomposition of \(K_3\vee C_5\).

| order | graphs | maps | contains \(K_6\) | exceptional \(K_3\vee C_5\) |
|---:|---:|---:|---:|---:|
| 1 | 1 | 1 | 0 | 0 |
| 2 | 2 | 2 | 0 | 0 |
| 3 | 4 | 4 | 0 | 0 |
| 4 | 11 | 11 | 0 | 0 |
| 5 | 34 | 34 | 0 | 0 |
| 6 | 156 | 155 | 1 | 0 |
| 7 | 1,044 | 1,037 | 7 | 0 |
| 8 | 12,346 | 12,257 | 88 | 1 |
| **total** | **13,598** | **13,501** | **96** | **1** |

Thus, among the 12,258 \(K_6\)-free graphs of order eight, exactly one
does not map.  Its graph6 record is
```
GUZ~~{
```
and its certificate identifies triangle \((5,6,7)\) and cyclic order
\((0,2,4,1,3)\).

The independent checker
[`verify_r5_hom_frontier_order8.py`](verify_r5_hom_frontier_order8.py)
does not invoke the homomorphism search.  It:

1. regenerates the complete `geng` stream and compares every graph6
   record in order;
2. decodes graph6 independently;
3. checks all 13,501 literal maps edge by edge;
4. checks all 96 displayed \(K_6\) witnesses;
5. checks the exact \(K_3\vee C_5\) decomposition;
6. exhaustively verifies that the 16-vertex even target component has
   clique number five; and
7. checks all 160 target triangles, each of which has a three-vertex,
   one-edge common neighbourhood.

The certificate file is
[`frontier.jsonl`](../output/r5-hom-frontier-order8/frontier.jsonl), with
13,599 lines and SHA-256
```
11d76be8a401309849269c1889372459a7d79b52b0eb5c745d8a49ac8e79cc96
```

Reproduction:
```sh
python3 scratch/enumerate_r5_hom_frontier_order8.py
python3 scratch/verify_r5_hom_frontier_order8.py
```

## Consequence for Oum-compatible eight-covers

Let \(W=\mathbb F_2^3\), and let \(Q(P)\) be the coordinate
co-occurrence graph of a compatible potential construction.  At a cubic
vertex \(v\), write the three incident nonzero flow values as \(a,b,c\),
where \(a+b+c=0\), and let the potential be \(t_v\).  The three incident
pair labels are the three edges of the triangle on
\[
        t_v+a,\qquad t_v+b,\qquad t_v+c.                       \tag{5}
\]
Consequently every co-occurrence edge belongs to a local triangle (at
each endpoint of the corresponding graph edge).

This local observation imposes no restriction on an individual
three-point support.  Conversely, for any three distinct points
\(x,y,z\in W\), take
\[
        t=x+y+z,\qquad a=y+z,\quad b=x+z,\quad c=x+y.
\]
Then \(a,b,c\) are nonzero, sum to zero, and (5) is exactly
\(\{x,y,z\}\).  In particular, “is a union of local triangles” alone
cannot rule out either obstruction: \(K_6\) and \(K_3\vee C_5\) both
have every edge in a triangle.  Even triangle-incidence parity alone is
insufficient, since taking every supporting triangle twice makes every
edge multiplicity even.  The existing potential-rigid cap gives an
actual compatible construction whose co-occurrence graph contains
\(K_6\).

There is, however, an exact structural success criterion.  On the eight
named coordinates, let a *nonco-occurrence* mean an edge of
\(\overline{Q(P)}\).  Then
\[
 Q(P)\longrightarrow R_5
\]
if and only if at least one of the following occurs:

1. three pairwise vertex-disjoint nonco-occurrences;
2. three coordinates that are pairwise nonco-occurring, together with
   one disjoint nonco-occurring pair; or
3. four coordinates that are pairwise nonco-occurring.

Indeed, a five-colouring partitions eight vertices into at most five
independent sets.  Those sets are vertex-disjoint cliques in the
complement, and their total saving
\(\sum(|C|-1)\) is at least three.  If a class has size at least four,
condition 3 holds.  Otherwise a class of size three must be accompanied
by a disjoint class of size at least two, giving condition 2; if every
class has size at most two, condition 1 follows.  The converse is
obtained by using the displayed sets as colour classes and leaving all
other coordinates singleton.  Equation (1) converts this exact
five-colour criterion into the \(R_5\)-homomorphism criterion.

Therefore a choice of flow \(\phi\) and compatible potential \(t\) is
successful as soon as it creates any one of these three frozen
nonco-occurrence packings.  Local triangles do not force such a packing.
Any universal argument must use the global potential equations, a change
of flow, or another global property to force one.  That is the precise
frontier left by this classification.
