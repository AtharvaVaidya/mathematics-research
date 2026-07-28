# The Jaeger star-fibre parity target and a fixed-base no-go

Date: 2026-07-28

Status: **EXACT REFORMULATION / HUMAN-CHECKABLE CUBE COUNTEREXAMPLE TO
A FIXED-THIRD-TREE SUBLEMMA / NOT A FIVEDC COUNTEREXAMPLE**.

## 1. The odd kernel of a tree

Let \(G\) be cubic and let \(T\) be a spanning tree.  Since
\(|V(G)|\) is even, there is a unique edge set \(K(T)\subseteq T\)
having odd degree at every vertex.

Here is a direct proof.  Root \(T\).  For a nonroot vertex \(v\), the
edge from \(v\) to its parent must belong to \(K(T)\) exactly when the
subtree rooted at \(v\) has odd order.  This follows by summing the
required odd degrees over that subtree: internal edges count twice and
only the parent edge can cross its boundary.  These forced choices
satisfy the root equation because the total number of vertices is even.
They prove existence and uniqueness.  Equivalently,

\[
 e\in K(T)
 \quad\Longleftrightarrow\quad
 \text{the two components of \(T-e\) have odd order}.          \tag{1}
\]

The fundamental completion \(F(T)\), namely the unique Eulerian edge
set containing every edge outside \(T\), is

\[
                         F(T)=E(G)-K(T).                       \tag{2}
\]

Indeed, the complement of an all-odd subgraph in a cubic graph is
Eulerian, and it contains \(E-T\).  Uniqueness follows by taking the
symmetric difference of two such completions, which is an Eulerian
subgraph of a tree and therefore empty.

## 2. Exact translation of the surviving target

Fix a vertex \(r\), and partition the edge copies of
\(2G-\delta(r)\) into spanning trees \(T_1,T_2,T_3\).  Every edge away
from \(r\) occurs in exactly two trees, every edge at \(r\) occurs in
one tree, and no edge occurs in all three.

Put \(K_i=K(T_i)\).  By (2), the \(i\)-th coordinate of the associated
fundamental-completion flow is zero exactly on \(K_i\).  Consequently
the edges of pure third-coordinate value are exactly

\[
            E_{\text{pure }3}
            =K_1\cap K_2\cap(E-K_3)
            =K_1\cap K_2.                                    \tag{3}
\]

In the last equality the coordinate convention is
\(\phi=(1_{F(T_1)},1_{F(T_2)},1_{F(T_3)})\): pure value \(001\) means
membership in \(F(T_3)\) and nonmembership in \(F(T_1),F(T_2)\).
An edge in \(K_1\cap K_2\) cannot lie in \(K_3\), because the
three-tree intersection is empty.

Also,
\[
                         E-F(T_3)=K_3.                         \tag{4}
\]

Thus the forest-coordinate support-five criterion becomes exactly:

> Choose the three-tree partition so that \(K_1\cap K_2\) has even
> edge boundary on every component of \(K_3\).

Equivalently, contract every component of \(K_3\); the image of
\(K_1\cap K_2\) must be Eulerian.

This translation isolates the genuine parity-base difficulty.  The
Nash-Williams--Tutte theorem supplies the three-tree packing, but it
does not control the nonlinear map \(T\mapsto K(T)\).

## 3. A natural fixed-base lemma is false

A tempting matroid strategy is:

1. choose the third spanning tree \(T_3\);
2. partition the residual copies into \(T_1,T_2\); and
3. use two-base exchange or matroid parity to repair the quotient
   boundary of \(K_1\cap K_2\).

The universal statement required by this strategy would be:

> **False fixed-third-tree extension lemma.**
> If \(T_3\) occurs in some three-tree partition of
> \(2G-\delta(r)\), then it has a completion \(T_1,T_2\) for which
> \(K_1\cap K_2\) has even boundary on every \(K_3\)-component.

The cube already refutes it.

Use the following edge-indexed presentation of the cube:

```text
0:(0,4)  1:(0,5)  2:(0,6)
3:(1,4)  4:(1,5)  5:(1,7)
6:(2,4)  7:(2,6)  8:(2,7)
9:(3,5) 10:(3,6) 11:(3,7).
```

Take \(r=0\), so the defect star is \(\{0,1,2\}\), and fix

\[
                 T_3=\{0,3,4,7,8,9,11\}.                    \tag{5}
\]

It is a spanning tree and it occurs in 16 ordered three-tree
partitions of the required multiset.  Its odd kernel is

\[
                 K_3=\{0,4,7,11\},                           \tag{6}
\]

whose four components are the matched pairs

\[
 A=\{0,4\},\quad B=\{1,5\},\quad
 C=\{2,6\},\quad D=\{3,7\}.                                  \tag{7}
\]

Normalize by putting root edge 1 in \(T_1\) and root edge 2 in \(T_2\);
swapping the first two trees gives the other eight ordered completions.
For every normalized completion,

\[
                         K_1=\{1,5,6,10\}.                    \tag{8}
\]

The complete enumeration is:

| \(T_1\) | \(T_2\) | \(K_2\) | \(K_1\cap K_2\) |
|---|---|---|---|
| 1 3 4 5 6 7 10 | 2 5 6 8 9 10 11 | 2 5 6 9 | 5 6 |
| 1 3 4 5 6 10 11 | 2 5 6 7 8 9 10 | 2 5 6 9 | 5 6 |
| 1 3 5 6 7 9 10 | 2 4 5 6 8 10 11 | 2 4 6 11 | 6 |
| 1 3 5 6 9 10 11 | 2 4 5 6 7 8 10 | 2 4 6 7 8 10 | 6 10 |
| 1 4 5 6 7 8 10 | 2 3 5 6 9 10 11 | 2 5 6 9 | 5 6 |
| 1 4 5 6 8 10 11 | 2 3 5 6 7 9 10 | 2 5 6 9 | 5 6 |
| 1 5 6 7 8 9 10 | 2 3 4 5 6 10 11 | 2 4 6 11 | 6 |
| 1 5 6 8 9 10 11 | 2 3 4 5 6 7 10 | 2 3 4 5 7 10 | 5 10 |

In the quotient by (7), edge 5 joins \(B\) to \(D\), edge 6 joins
\(C\) to \(A\), and edge 10 joins \(D\) to \(C\).  Each of the four
possible last-column sets

\[
                    \{5,6\},\quad\{6\},\quad
                    \{6,10\},\quad\{5,10\}                   \tag{9}
\]

has an odd-degree quotient vertex.  Hence all 16 ordered extensions of
the fixed \(T_3\) fail the required component parity.

The table is a human-sized complete proof: spanning-tree status can be
checked directly, (1) recomputes every displayed \(K_i\), and residual
edge multiplicities force exactly the eight normalized rows.

## 4. Scope and consequence for parity-base methods

This is not a counterexample to the existential star-fibre lemma.
Jointly choosing all three trees works on the same cube and root:

```text
T1 = 1 3 4 7 8 9 11
T2 = 2 5 6 8 9 10 11
T3 = 0 3 4 5 6 7 10.
```

Here

```text
K1 = 1 3 7 11
K2 = 2 5 6 9
K1 intersection K2 = empty,
```

so component parity is immediate.  Of the 132 extendible choices of a
third tree in this cube star fibre, 120 admit a parity-good completion
and 12 do not.

The no-go is therefore precise: tree packing followed by a
fixed-\(T_3\) two-base parity repair cannot be a universal proof.  A
successful matroid argument must co-optimize the third base with the
other two, or retain enough exchange freedom to replace \(T_3\).
Ordinary Nash-Williams--Tutte feasibility alone loses exactly the
information needed by the odd-kernel quotient condition.

The potentially useful positive reformulation is that \(K(T)\) is a
spanning all-odd forest, and every spanning tree containing such a
forest has it as its odd kernel.  One may therefore try to choose three
capacity-respecting all-odd forests first and then solve a simultaneous
tree-extension problem.  The cube witness shows that fixing the third
forest/base before the other two is too rigid.

## 5. Reproduction

Run:

```sh
python3 scratch/check_jaeger_fixed_third_tree_parity_no_go.py
```

The checker uses only the Python standard library.  It verifies that
the displayed graph is simple, cubic, and remains connected after
deleting any two edges; enumerates all 384 spanning trees; independently
checks uniqueness of every odd kernel; enumerates the 16 fixed-base
extensions; checks all quotient boundaries; checks the successful
jointly chosen triple; and exhausts all 132 extendible third trees.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the odd-kernel
translation, tested the fixed-base parity strategy, found the cube
witness, wrote the independent exact checker, and drafted this
note.  The displayed finite proof is intended for direct human
verification.  This is not independent peer review and is not claimed
as a resolution of FiveCDC.
