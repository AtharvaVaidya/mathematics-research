# Exact Jaeger star parity is invariant under nonroot triangle expansion

Date: 2026-07-28

Status: **HUMAN REDUCTION WITH A SEVEN-ROW LOCAL TABLE / EXACT TARGET,
NOT THE FALSE KERNEL-CLOSURE STRENGTHENING / NOT A UNIVERSAL
FIVE-CDC PROOF**.

## 1. The exact target in Eulerian-completion form

Let \(K\) be a forest in a graph and let \(A\) be disjoint from \(K\).
The following are equivalent:

1. \(A\) has even boundary on every component of \(K\);
2. there is a set \(P\subseteq K\) such that \(A\mathbin\triangle P\)
   is Eulerian.

Indeed, condition 2 says \(\partial P=\partial A\).  On each tree
component of \(K\), the incidence map has image exactly the even-cardinality
vertex sets.  This proves existence under condition 1, and also uniqueness
of \(P\).

For a star packing \(T_0,T_1,T_2\), put \(K_i=K(T_i)\).  The exact
coordinate-two target can therefore be written
\[
 \exists P\subseteq K_2\quad
       (K_0\cap K_1)\mathbin\triangle P
       \text{ is Eulerian}.                                  \tag{1}
\]
This is strictly weaker than the false condition
\(K_0\cap K_1\subseteq\operatorname{cl}(K_2)\): (1) permits a whole
quotient cycle rather than requiring every common edge to be a quotient
loop.

## 2. Contraction of a nonroot triangle

Let \(G^\triangle\) be obtained from a cubic graph \(G\) by replacing a
vertex \(z\) by a triangle \(\Delta=abc\), attaching the three old
edge identities at \(a,b,c\).  Parallel external edges are allowed in
this local statement; all tree and parity arguments are edge-labelled.
Fix a star root
\(r\notin\{a,b,c\}\).

Every triangle edge has multiplicity two in a star fibre at \(r\).
The three trees therefore contain six triangle-edge occurrences in
total.  A tree contains at most two edges of a triangle, so every tree
contains exactly two.  Contracting the triangle in each tree gives a
star packing \(\bar T_0,\bar T_1,\bar T_2\) of \(G\).

For every external tree edge, contraction removes either zero or two
vertices from one side of its fundamental cut.  Hence
\[
 e\in K(T_i)\quad\Longleftrightarrow\quad
 e\in K(\bar T_i)
 \qquad(e\notin E(\Delta)).                                  \tag{2}
\]

If (1) holds upstairs, contract the Eulerian subgraph
\((K_0\cap K_1)\triangle P\) and delete the resulting triangle loops.
Eulerian parity is preserved.  By (2), the remaining edge set is
\[
 (K(\bar T_0)\cap K(\bar T_1))\triangle\bar P,
 \qquad \bar P\subseteq K(\bar T_2).
\]
Thus exact component parity descends.

## 3. The local lifting equations

Conversely, suppose the contracted packing satisfies (1) in coordinate
two, witnessed by \(\bar P\subseteq\bar K_2\).

Use three-bit vertex masks for \(a,b,c\).  Let
\[
 b_i\subseteq\{a,b,c\}
\]
be the trace at \(z\) of the external edges in \(\bar K_i\), and let
\(p\subseteq b_2\) be the external trace of \(\bar P\).  Since every
\(\bar K_i\) has odd degree at \(z\),
\[
                 |b_i|\equiv1\pmod2.                         \tag{3}
\]
No external edge belongs to all three trees, so
\[
                         b_0\cap b_1\cap b_2=\varnothing.     \tag{4}
\]
Finally, the Eulerian condition at the contracted vertex says
\[
                    |(b_0\cap b_1)\triangle p|
                    \equiv0\pmod2.                           \tag{5}
\]

Choose one omitted triangle edge \(o_i\) for each coordinate, with
\((o_0,o_1,o_2)\) a permutation of \(ab,bc,ca\).  This produces the
three lifted trees and supplies every legal lift exactly once.  Let
\(x_i\) be the local triangle-edge part of \(K_i\).  It is the unique
subset of the two included triangle edges satisfying
\[
                         \partial x_i=\{a,b,c\}\triangle b_i. \tag{6}
\]

Put
\[
 z_{\rm ext}=(b_0\cap b_1)\triangle p,\qquad
 q=x_0\cap x_1.
\]
The lifted packing is good in coordinate two if one can choose
\(y\subseteq x_2\) with
\[
                         \partial y=z_{\rm ext}\triangle
                                      \partial q.             \tag{7}
\]
Then \(P=\bar P\cup y\) makes
\((K_0\cap K_1)\triangle P\) Eulerian upstairs.  All conditions away
from the triangle already hold downstairs, so (7) is the entire local
obligation.

## 4. Seven-row proof of the local obligation

Write vertex masks as
\[
 1=a,\quad2=b,\quad4=c,\quad7=abc,
\]
and triangle-edge masks as
\[
 1=ab,\quad2=bc,\quad4=ca.
\]
Equations (3)--(5) allow 60 quadruples
\((b_0,b_1,b_2;p)\).  Permuting \(a,b,c\) and swapping coordinates zero
and one reduces them to the following seven orbits.  Each row displays
one choice of omitted edges, the resulting \((x_0,x_1,x_2)\), and a
valid \(y\subseteq x_2\).

\[
\begin{array}{c|c|c|c|c}
(b_0,b_1,b_2)&p&(o_0,o_1,o_2)&(x_0,x_1,x_2)&y\\ \hline
(a,a,b)&b&(ab,bc,ca)&(bc,ab{+}ca,ab{+}bc)&ab\\
(a,b,a)&0&(ab,bc,ca)&(bc,ca,bc)&0\\
(a,b,c)&0&(ab,bc,ca)&(bc,ca,ab)&0\\
(a,b,abc)&0&(ab,bc,ca)&(bc,ca,0)&0\\
(a,b,abc)&a{+}b&(bc,ca,ab)&(ab{+}ca,ab{+}bc,0)&0\\
(a,b,abc)&a{+}c&(bc,ab,ca)&(ab{+}ca,ca,0)&0\\
(a,abc,b)&b&(ab,bc,ca)&(bc,0,ab{+}bc)&ab
\end{array}
\]

Every row is checked by the two incidence equations (6) and (7).
The orbit sizes are
\[
                         6,12,6,6,6,12,12,
\]
which sum to 60, proving completeness.  Thus every admissible contracted
trace has at least one parity-preserving legal triangle lift.

The independent standard-library checker

```sh
python3 scratch/verify_jaeger_star_exact_parity_triangle_lift.py
```

enumerates all 60 patterns, reconstructs the seven symmetry orbits,
checks the displayed representatives, and verifies directly that no
pattern lacks a lift.  The number of good lifts per pattern is:

```text
one lift     18 patterns
two lifts    12 patterns
three lifts   6 patterns
four lifts   24 patterns
```

## 5. Exact triangle-invariance theorem

Combining the two directions gives:

> **Theorem.**  Let \(r\) lie outside an expanded triangle.  A
> vertex-star fibre at \(r\) contains an exact component-parity-good
> packing in \(G^\triangle\) if and only if the corresponding fibre
> contains one after the triangle is contracted.

This sharply separates the live theorem from the discarded
kernel-closure route:

* closure-goodness descends but need not lift;
* exact component parity both descends and lifts.

Consequently the certified 16-vertex closure countermodel and its
infinite triangle-expansion family are irrelevant as obstructions to the
exact Jaeger selection lemma: their good contracted packings always have
some exact-parity-good lift, even though no closure-good lift exists.

There is no multigraph gap for simple 3-edge-connected cubic graphs other
than \(K_4\).  If exactly two triangle vertices have the same external
neighbour \(x\), then the triangle together with \(x\) has a two-edge cut:
the third triangle spoke and the third edge at \(x\).  If all three have
the same external neighbour, cubicity makes the whole connected graph
\(K_4\).  Hence every triangle in a simple 3-edge-connected cubic graph
other than \(K_4\) has three distinct external neighbours, and its
contraction remains simple.  It also remains 3-edge-connected, because
any one- or two-edge cut downstairs lifts unchanged after placing the
whole expanded triangle on the contracted vertex's shore.  The \(K_4\)
star fibres are checked directly.

It follows that every triangle in a non-\(K_4\), prescribed-root minimal
simple 3-edge-connected obstruction must contain the root.  For an
unrooted existence argument one may choose the root outside a triangle
and contract it.  The theorem still does not remove triangles containing
a preassigned root, and it does not prove the universal parity-and-base
selection statement on a triangle-free graph.

## 6. Matroid interpretation and remaining obstruction

Deleting the root turns a star packing into a partition of \(E(G-r)\)
into three cographic bases.  The odd forests are the fundamental
circuits of the three terminal parity elements.  The theorem above says
that a triangle expansion is a local three-element series extension for
this cographic partition problem and that the **linear** Eulerian
completion condition (1) is invariant under it.

What remains is not ordinary matroid closure.  It is the joint selection
of three cographic bases whose three parity-element fundamental circuits
satisfy one bilinear intersection equation modulo a graphic cycle space.
No standard basis-packing, matroid-intersection, or delta-matroid theorem
located so far supplies that joint selection.

## AI-use disclosure

OpenAI Codex, under human direction, derived the Eulerian-completion
formulation, contraction proof, local lifting equations, seven-orbit
table, and checker.  This is a reduction theorem for the surviving exact
Jaeger target, not a proof of that target or of Five-CDC.
