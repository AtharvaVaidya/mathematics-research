# Perfect forests do not automatically extend to a Jaeger tree packing

Date: 2026-07-28

Status: **HUMAN MATROID-RANK CERTIFICATE / EXACT FINITE NO-GO /
NOT A FIVEDC COUNTEREXAMPLE**.

## 1. What Scott's theorem supplies

A perfect forest is a spanning forest whose vertices all have odd
degree and whose components are induced subgraphs.  Scott's Perfect
Forest Theorem says that every connected graph of even order has such
a forest.

This is stronger than the parity property required of the odd kernel
\(K(T)\) of a spanning tree, except that the Jaeger problem needs three
forests simultaneously.  In the star fibre at \(r\), put

\[
 m_e=\begin{cases}
 1,&e\in\delta(r),\\
 2,&e\notin\delta(r).
 \end{cases}
\]

The natural forest-first plan is to choose perfect forests
\(K_1,K_2,K_3\) satisfying

\[
 \sum_i 1_{e\in K_i}\leq m_e                              \tag{1}
\]

and the target parity, then extend them simultaneously to spanning
trees \(T_i\supseteq K_i\) whose multiset union is
\(2G-\delta(r)\).  Since an all-odd subforest of a tree is unique, such
an extension would automatically have \(K(T_i)=K_i\).

The universal extension step is false even when the chosen perfect
forests are perfect matchings and the target parity is vacuous.

Scott's result used here is A. D. Scott, *On Induced Subgraphs with All
Degrees Odd*, Graphs and Combinatorics 17 (2001), 539--553,
doi:10.1007/s003730170028.  A short linear-algebra proof appears in
G. Gutin, *Note on Perfect Forests*, Journal of Graph Theory 82 (2016),
233--235, doi:10.1002/jgt.21897.

## 2. Exact graph and forests

Use the following labelled 10-vertex Möbius ladder:

```text
0:(0,5)  1:(0,6)  2:(0,7)
3:(1,5)  4:(1,7)  5:(1,8)
6:(2,5)  7:(2,8)  8:(2,9)
9:(3,6) 10:(3,7) 11:(3,9)
12:(4,6) 13:(4,8) 14:(4,9).
```

It is simple, cubic, and 3-edge-connected.  Take \(r=0\), so
\(\delta(r)=\{0,1,2\}\), and choose

\[
\begin{aligned}
K_1&=\{0,4,7,11,12\},\\
K_2&=\{1,5,6,10,14\},\\
K_3&=\{2,5,6,11,12\}.
\end{aligned}                                                \tag{2}
\]

Each \(K_i\) is a perfect matching.  It is therefore a Scott-perfect
forest: it spans all ten vertices, every degree is one, it is acyclic,
and every two-vertex component is induced.

The root edges \(0,1,2\) occur once, one in each forest.  No nonroot
edge occurs more than twice, so (1) holds.  Moreover,

\[
                         K_1\cap K_2=\varnothing.              \tag{3}
\]

Thus \(K_1\cap K_2\) has even boundary on every \(K_3\)-component.
The chosen forests already satisfy the exact Jaeger component-parity
target.

## 3. Ten-copy rank obstruction

After reserving the copies used by (2), the residual multiset is

```text
3a 3b 4 7 8a 8b 9a 9b 10 13a 13b 14.
```

Here `a` and `b` distinguish the two copies of one original edge.
Let

\[
 X=\{3a,3b,7,8a,8b,9a,9b,13a,13b,14\};                     \tag{4}
\]

that is, delete residual copies 4 and 10.  Consider the graphic
matroid after contracting \(K_i\).  Its rank on \(X\) is three for
each \(i\).

This rank calculation can be checked without matroid terminology.
Every \(K_i\) has five matching components.  After adding all distinct
underlying edges of \(X\), the vertex components are respectively

```text
K1 + X: {0,1,5,7} | {2,3,4,6,8,9}
K2 + X: {0,3,6,7} | {1,2,4,5,8,9}
K3 + X: {0,7}     | {1,2,3,4,5,6,8,9}.
```

Thus \(X\) can merge only three of the five initial components in each
coordinate.  Duplicate copies do not increase graphic rank, so

\[
                         r_i(X)=5-2=3
                         \quad(i=1,2,3).                       \tag{5}
\]

Suppose simultaneous extensions existed.  Let \(A_i\) be the residual
copies assigned to \(T_i-K_i\).  Since \(K_i\cup A_i\) is a tree,
the subset \(A_i\cap X\) is independent after contracting \(K_i\).
Consequently

\[
                         |A_i\cap X|\leq r_i(X)=3.             \tag{6}
\]

But \(A_1,A_2,A_3\) partition every residual copy, including all ten
copies of \(X\).  Summing (6) gives

\[
 10=|X|
   =\sum_i|A_i\cap X|
   \leq\sum_i r_i(X)
   =9,
\]

a contradiction.  This is the failed matroid-union inequality in
literal form and is a complete human proof of nonextension.

## 4. Consequence and precise scope

Scott's theorem, or a prescribed-parity strengthening applied to the
three coordinates separately, cannot be followed by a generic
simultaneous-extension theorem.  The displayed forests satisfy:

1. the full Scott induced-component condition;
2. the star-fibre edge capacities;
3. the prescribed distinct root edges; and
4. the desired quotient parity, in the strongest form
   \(K_1\cap K_2=\varnothing\).

They still do not extend.  Any viable perfect-forest proof must choose
the forests jointly with the matroid-union rank inequalities, rather
than first solve parity and then appeal to tree packing.

This does **not** disprove the existential perfect-forest route or the
Jaeger lemma.  Another forest choice on the same graph and root extends:

```text
K1 = 0 5 8 10 12
K2 = 1 4 6 11 13
K3 = 2 4 6 7 8 10 12

T1 = 0 3 5 7 8 10 11 12 13
T2 = 1 3 4 5 6 9 11 13 14
T3 = 2 4 6 7 8 9 10 12 14.
```

These are again Scott-perfect forests, the three trees partition
\(2G-\delta(0)\), and direct odd-subtree calculation gives
\(K(T_i)=K_i\).  Here also \(K_1\cap K_2=\varnothing\).

The surviving theorem would have to assert the existence of forests
that satisfy both component parity and every simultaneous-extension
rank inequality.  Scott's one-forest existence theorem supplies
neither the cross-coordinate capacities nor those rank inequalities.

## 5. Reproduction

Run:

```sh
python3 scratch/check_jaeger_perfect_forests_first_no_go.py
```

The standard-library checker verifies graph connectivity after every
one- and two-edge deletion, all perfect-forest conditions, capacities,
component parity, the ten-copy rank certificate, and a separate
exhaustive residual-copy assignment with zero extensions.  It also
checks the positive triple above and recomputes its three odd kernels.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the exact
perfect-forest extension sublemma, found the finite obstruction, derived
the ten-copy rank certificate, wrote the independent checker, and
drafted this note.  The cited theorem is prior human work.  This is not
independent peer review and is not claimed as a resolution of FiveCDC.
