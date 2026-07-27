# Triangle induction for rooted cap signatures

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE REDUCTION / FINITE TRIANGLE-FREE PREMISE
CURRENTLY BEING CHECKED / END-FACTOR LIFT NOW BYPASSES THIS PREMISE FOR
THE ORDER-28 BOUND / NOT FIVE-CDC**.

Fix a simple 3-connected cubic graph \(H\), a vertex \(z\), and a
proper root \(r\) of the three-pole \(H-z\).  Normalize the three
connectors at \(z\) to
\[
                              (01,02,12).                        \tag{1}
\]
Write \(R(H,z,r)\) for the resulting fixed-five root signature and
retain the base pairs
\[
\begin{aligned}
 P_0&=\{12,03,04\},\\
 P_1&=\{02,13,14\},\\
 P_2&=\{01,23,24\}.                                  \tag{2}
\end{aligned}
\]

For five distinct coordinates \(p,q,r,s,t\), call
\[
                 Q(p;q,r;s,t)=\{qr,ps,pt\}                         \tag{F}
\]
a **fork triple**.  Thus the three base pairs in (2) are particular
fork triples.  Coordinate permutations preserve the class of fork
triples.

This note reduces graphs with triangles to triangle-free graphs without
assuming universal base-pair closure.

Call \((H,z,r)\) **path-rooted** if the standard decomposition of \(H\)
along cyclic three-edge cuts has a factor-incidence path whose two end
factors contain \(z\) and \(r\), respectively.  This is exactly the
geometry supplied by the minimal simple-cap fork after cutting at a
principal cyclic three-cut.  Deleting \(z\) from a 3-connected graph
leaves a 2-connected graph, so every proper root \(r\) in this setup is
a nonbridge.

> **Path-rooted triangle-induction theorem.**  
> Fix an even order bound \(N\).  Suppose that, for every triangle-free
> simple 3-connected cubic graph \(J\) of order at most \(N\), every
> nonempty signature \(R(J,w,s)\) contains a base pair from (2).
> Then for every path-rooted triple \((H,z,r)\) of order at most \(N\),
> \[
> R(H,z,r)\ne\varnothing
> \quad\Longrightarrow\quad
> Q(p;q,r',s,t)\subseteq R(H,z,r)
> \quad\text{for some five distinct }p,q,r',s,t.        \tag{3}
> \]

The shape in (3), rather than cardinality alone, is essential.  For
example, two copies of \(\{01,02,12\}\) have the exceptional mixed
equality/intersection relation despite both having three labels.

## 1. Contracting a cubic triangle

Let \(T\) be a triangle of a simple 3-connected cubic graph \(H\) with
\(|V(H)|>4\).  Its three outside neighbours are distinct.  Otherwise,
if two triangle vertices had the same outside neighbour, deleting that
neighbour and the third triangle vertex would separate the remaining
triangle edge.

Contract \(T\) to one cubic vertex, obtaining \(H/T\).  The graph
\(H/T\) is simple and cubic.  It is also 3-connected.  Indeed,
bridges and cyclic two-edge cuts of \(H/T\) lift to bridges and cyclic
two-edge cuts of \(H\): if the contracted vertex lies on a shore,
replace it by all three vertices of \(T\); a cycle through the
contracted vertex lifts through one of the two corresponding arcs of
the triangle.  A simple bridgeless cubic graph without a cyclic
two-edge cut is 3-connected by the elementary cap-connectivity lemma.

Triangle contraction preserves Tait colourability.  In a Tait
colouring the three external edges of \(T\) have three distinct colours,
so they colour the contracted vertex.  Conversely, expand a coloured
cubic vertex and give each triangle edge the colour of the opposite
external edge.

The same local rule works for \(D_5\)-labellings.  If the three external
labels are \(a,b,c\), then
\[
                              a+b+c=0
\]
and they are the three edges of a coordinate triangle.  Assign to each
new internal triangle edge the label on the opposite external edge.
This extends every contracted labelling; summing parity over the three
triangle vertices proves the converse.

Consequently, if \(z\notin V(T)\) and \(r\notin E(T)\), contraction
preserves the normalized root signature exactly (including when \(r\)
is one of the three external edges of \(T\)):
\[
                         R(H,z,r)=R(H/T,z,r).                    \tag{4}
\]

## 2. A triangle through the root

Suppose \(z\notin V(T)\) and \(r\in E(T)\).
Fix any normalized labelling, which exists when the signature is
nonempty.  Normalize the external labels of \(T\), for this local
calculation only, to \(01,02,12\), with \(r\) joining the vertices
incident with \(01\) and \(02\).

If \(x\) is the label of \(r\), the other two internal labels are
\(01+x\) and \(02+x\).  Requiring all three labels to lie in \(D_5\)
gives exactly
\[
                             x\in\{12,03,04\}.                   \tag{5}
\]
All three choices in (5) change only the labels inside \(T\), so all
extend the same fixed outside labelling.  They are distinct.  Therefore
\[
                    Q(0;1,2;3,4)=\{12,03,04\}
                    \subseteq R(H,z,r).                         \tag{6}
\]
The same conclusion holds for either of the other two internal root
positions by symmetry.

## 3. A triangle through the deleted connector vertex

Suppose now that \(z\in V(T)\) but \(r\notin E(T)\).  Name the other
two triangle vertices \(p,q\), and use connector order
\[
 zp=01,\qquad zq=02,\qquad zx=12,
\]
where \(zx\) is the third edge at \(z\).  Put \(t=\phi(pq)\).
The labels on the two external edges from \(p,q\) are
\[
                             01+t,\qquad02+t.
\]
Exactly three values of \(t\) are possible:
\[
\begin{array}{c|ccc}
t&12&03&04\\ \hline
\text{effective connector word after contracting }T
 &(02,01,12)&(13,23,12)&(14,24,12).
\end{array}                                                     \tag{7}
\]

Normalize each effective word in (7) back to (1).  Applying the inverse
coordinate permutations to a contracted root signature gives the
expanded signature.  Direct substitution in the three base pairs gives
\[
\begin{array}{c|c|c}
\text{contracted subset}&\text{labels forced in the expanded signature}
 &\text{retained base pair}\\ \hline
P_0&\{12,03,04,34\}&P_0\\
P_1&\{01,13,14,23,24\}&P_2\\
P_2&\{02,13,14,23,24\}&P_1.
\end{array}                                                     \tag{8}
\]
The unused-coordinate swap in each normalization changes neither the
conclusion nor the stabilizer-invariant signature.

Thus a base pair in \(R(H/T,T,r)\) forces a base pair in
\(R(H,z,r)\).  More generally, if the contracted signature contains a
fork triple, fix any one of the three effective words in (7) and one
normalization for that word.  Its inverse is one coordinate permutation
applied simultaneously to all three fork labels.  It therefore injects
the contracted fork as another fork triple in the expanded signature.

If \(z\in V(T)\) and \(r\in E(T)\), the root is the edge
joining the two other triangle vertices.  Contract the triangle to a
vertex \(v\) and then delete \(v\).  What remains is an **unrooted**
three-pole.  Nonemptiness of the original root signature gives it one
admissible ordered connector triangle.  Global coordinate permutations
act transitively on all ordered connector triangles, so it admits all
three effective words in (7).  Expanding them back with the normalized
connectors (1) realizes all three root values
\[
                              12,\quad03,\quad04.
\]
Thus \(P_0\subseteq R(H,z,r)\); the other physical connector orders give
\(P_1\) or \(P_2\) by symmetry.

## 4. Induction along the factor path

Induct on \(|V(H)|\).  The triangle-free case is the premise of the
theorem.  If \(H=K_4\), direct Tait-cap closure gives (2).

In a cyclically \(4\)-edge-connected cubic factor, a triangle can occur
only when the factor is \(K_4\): otherwise the triangle and its
complement are the two cyclic shores of a three-edge cut.  Hence a
triangle in a graph whose factor tree is a path can occur only at a
\(K_4\) end factor.  Indeed a triangle cannot cross a principal
three-cut, because it would use two cut edges sharing their endpoint on
one shore, whereas the three edges of a cyclic three-cut in a
3-connected cubic graph have distinct ends on both shores.  An internal
\(K_4\) factor loses two distinct gluing vertices and contributes no
triangle.  Thus an exposed triangle contains \(z\), contains \(r\), or,
when the path has one node, contains both.

- At the \(z\)-end, contract the exposed triangle.  This removes the
  endpoint \(K_4\) factor, leaves a shorter path-rooted triple, and
  preserves simple 3-connectivity.  Apply induction and the
  fork-preservation argument after (8).
- At the \(r\)-end, use (6).
- In the one-node case containing both, the unrooted-three-pole
  argument after (8) supplies a base pair directly.

Every contraction reduces the order by two and preserves the required
path-rooted cap premises.  This proves (3). \(\square\)

## 5. Intended finite consequence

At a surviving cyclic three-cut of a simple exceptional cap \(G\), the
two capped shores \(H_1,H_2\) satisfy
\[
                         |V(H_1)|+|V(H_2)|=|V(G)|+2.             \tag{9}
\]
They are simple, 3-connected, and path-rooted.  Hence if
\(|V(G)|\le26\), both have order at most \(24\).

Suppose a fork \(Q(p;q,r;s,t)=\{qr,ps,pt\}\) lies in one shore
signature and the mixed exceptional relation has no disjoint pair.
Every label \(b\) in the opposite signature must meet all three fork
labels.  Meeting both \(ps\) and \(pt\) forces either \(p\in b\) or
\(b=st\); the latter misses \(qr\).  Meeting \(qr\) then gives
\[
                              b\in\{pq,pr\}.                     \tag{10}
\]
Thus the opposite signature has at most two labels.  Applying (3) to
both shores is impossible: whichever shore supplies its fork restricts
the other to at most two labels, while (3) puts three distinct labels
there.

Once the pending triangle-free 3-connected screen through order 24 is
complete and independently replayed, this will eliminate the mixed
cyclic-three branch through cap order 26.  Together with the already
complete cyclically-four cap census through order 26, it would restore
the simple terminal-distinct exceptional-pole lower bound of order 28.
Until that finite premise is frozen, this paragraph remains a conditional
whole-shore consequence.  The later human endpoint-fork transport in
`rooted-cap-end-factor-fork-lift.md` obtains the required fork directly
from each root-end factor and therefore restores the order-28 bound
without using this pending screen.  The present screen remains useful as
a stronger independent whole-shore check.

For error detection, the standard-library replay
`scratch/verify_rooted_cap_triangle_table.py` exhaustively reconstructs
(5), all coordinate normalizations in (7), all three rows of (8), and
the common-intersector set of every fork triple.
It returns `PASS`.  Frozen SHA-256 values are:

```text
2c4dc8f501a3eb0db354146ae1ee9e83231cfe9d45af97b5fa03780d08481006  verifier
1047a5ddbe98c641cdae37a81c7e4bf30d50a6171fee612eca05fd964b8ead74  result
```

## AI-use disclosure

OpenAI Codex, under human direction, found the three triangle cases and
the connector-expansion table (8), and drafted this proof.  The argument
is displayed for line-by-line checking.  The finite premise in Section
5 is explicitly marked pending, and this note does not resolve
Five-CDC.
