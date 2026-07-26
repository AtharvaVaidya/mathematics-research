# The exact order-88 incidence object does not force a good selector

Date: **2026-07-26**.

Status: **human-checkable equality reduction and finite abstract
countermodel**.  The countermodel satisfies the factor-incidence data forced
by equality, but it fails other minimum-counterexample hypotheses.  It is
not a counterexample to the five-cycle double cover conjecture.

## 1. What equality forces

Work in the connected size-four branch described in
`connected-eight-mark-paired-cut-condition.md`.  Thus \(G\) is the ambient
cubic graph, \(M\) is the four-edge exact-zero matching, \(K=G-M\), and
suppressing the eight vertices \(T=\partial M\) in \(K\) produces a connected
simple cubic core \(H\) with an eight-edge marked matching \(S\).

The monochromatic-mark girth argument supplies, for either of the two
bichromatic factors containing the common mark colour, eight
vertex-disjoint odd circuits in \(K\).  Each circuit contains exactly one
vertex of \(T\).  The ambient girth bound makes every such circuit have
length at least \(11\).

Suppose now that \(|V(G)|=88\).  The eight disjoint circuits already use at
least
\[
             8\cdot 11=88
\]
vertices.  Equality therefore says that they span \(K\), and that every one
has length exactly \(11\).  Suppressing its unique terminal replaces its
two-edge path by one marked edge.  Consequently each corresponding core
circuit has length \(10\).  The same argument applies to both factors.
Hence the all-\(c\) Tait colouring of \(H\) has
\[
 H[a,c]=A_0\sqcup\cdots\sqcup A_7,\qquad
 H[b,c]=B_0\sqcup\cdots\sqcup B_7,                    \tag{1}
\]
where every displayed circuit has length \(10\) and contains exactly one
mark.

Let \(\Gamma\) be the bipartite incidence multigraph whose vertices are the
sixteen circuits in (1) and whose edges are the \(c\)-edges of \(H\).  A
10-cycle has five \(c\)-edges, so \(\Gamma\) is 5-regular.  It is connected
because \(H\) is connected.  Relabeling the factor circuits makes the mark
edges
\[
             A_iB_i\quad(0\le i<8),                  \tag{2}
\]
so the marks form a distinguished perfect matching in \(\Gamma\).
Parallel incidence edges are allowed even though \(H\) itself is simple.

This proves the claimed \(8+8\), 5-regular equality object without assuming
that the suppressed core has girth ten.  The girth-ten hypothesis belongs
to the ambient expansion.

## 2. Selectors and the missing transition data

An all-mark selector is normalized by eight bits \(x_i\).  Select \(A_i\)
when \(x_i=1\), and select \(B_i\) when \(x_i=0\).  Equivalently,
\(y_i=1-x_i\).  The binary cycle
\[
 Q_x=\mathop{\triangle}_{x_i=1}E(A_i)
      \mathbin\triangle
      \mathop{\triangle}_{x_i=0}E(B_i)                \tag{3}
\]
contains every marked edge, since its indicator on \(A_iB_i\) is
\(x_i+(1-x_i)=1\).  There are exactly \(2^8=256\) selectors.  A selector is
**good** when every circuit component of \(Q_x\) contains an even number of
marks.

The incidence multigraph alone does not determine the components of
\(Q_x\).  Give every incidence edge \(e\) two ports \(e^0,e^1\), cyclic
orders \(\rho_A,\rho_B\) at the two sides, and a bit \(\tau_e\).  The
coloured core is reconstructed by
\[
\begin{array}{rcl}
c&:&e^0e^1,\\
a&:&e^1(\rho_Ae)^0,\\
b&:&e^{1-\tau_e}(\rho_Be)^{\tau_{\rho_Be}}.
\end{array}                                            \tag{4}
\]
Thus a decorated incidence object is enough to trace (3) by hand.

There is one useful rotation-independent sufficient condition.  Let
\[
 U_x=\{A_i:x_i=1\}\cup\{B_i:x_i=0\}.
\]
If the multigraph induced by \(U_x\) is a forest and each of its components
has even order, then \(x\) is good.  Indeed, begin with the selected factor
circuits.  Every internal incidence edge is a common \(c\)-edge of two
selected circuits; cancelling it in the symmetric difference joins the two
remaining paths.  In a forest each cancellation joins two previously
distinct components.  A resulting circuit therefore has as many marks as
there are vertices in the corresponding forest component, which is even.

The countermodel below has no selector satisfying even this sufficient
condition, and its transition data make all 256 selectors bad.

## 3. Explicit decorated incidence countermodel

Use the following row-column multiplicity matrix, with rows \(A_0,\ldots,A_7\)
and columns \(B_0,\ldots,B_7\):
\[
\begin{pmatrix}
2&0&1&2&0&0&0&0\\
0&1&1&0&1&2&0&0\\
0&2&1&0&0&0&2&0\\
0&0&0&2&1&0&0&2\\
1&0&1&0&1&0&1&1\\
1&0&1&0&1&2&0&0\\
0&2&0&0&0&0&2&1\\
1&0&0&1&1&1&0&1
\end{pmatrix}.                                        \tag{5}
\]
Every row and column sums to five, and the multigraph is connected.  Number
one distinguished diagonal edge \(A_iB_i\) by \(i\), for \(0\le i<8\).
After removing those eight copies from (5), number the remaining edge
objects \(8,\ldots,39\) in row-major order.

The cyclic orders are:
\[
\begin{array}{c|l}
A_0&(9,0,11,8,10)\\
A_1&(15,14,1,13,12)\\
A_2&(16,17,2,19,18)\\
A_3&(22,3,21,20,23)\\
A_4&(27,25,26,4,24)\\
A_5&(5,31,30,28,29)\\
A_6&(6,32,33,34,35)\\
A_7&(7,37,38,36,39)
\end{array}
\qquad
\begin{array}{c|l}
B_0&(8,24,36,28,0)\\
B_1&(32,17,16,33,1)\\
B_2&(9,25,29,12,2)\\
B_3&(3,20,10,37,11)\\
B_4&(38,13,4,30,21)\\
B_5&(14,15,39,5,31)\\
B_6&(26,19,18,34,6)\\
B_7&(23,7,22,35,27).
\end{array}                                            \tag{6}
\]
In edge-ID order \(0,\ldots,39\), the twist word is
```text
1110111111000001001100001111000111010001
```

Formula (4) reconstructs a connected simple cubic graph \(H\) with 80
vertices and 120 edges.  The three edge classes are perfect matchings, so
the displayed colouring is a proper Tait colouring.  Direct tracing gives
eight 10-cycles in each of \(H[a,c]\) and \(H[b,c]\), one distinguished
mark per cycle.

## 4. Exact enumeration

Two implementations agree on the complete selector space:

1. the C++ search reconstructs (4) and evaluates the local selector state
   at every port;
2. the clean-room Python audit reads the explicit 120-edge coloured graph,
   recovers the sixteen factor circuits, and forms the literal symmetric
   differences (3).

Both enumerate all 256 selectors and find **zero good selectors**.  Omitting
components with no marks, the exact marked-component profile histogram is:

| Profile | Count | Profile | Count |
|---|---:|---|---:|
| \(1+1+1+1+1+1+1+1\) | 5 | \(1+1+1+1+1+1+2\) | 13 |
| \(1+1+1+1+1+3\) | 22 | \(1+1+1+1+2+2\) | 6 |
| \(1+1+1+1+4\) | 27 | \(1+1+1+2+3\) | 22 |
| \(1+1+1+5\) | 56 | \(1+1+2+4\) | 28 |
| \(1+1+3+3\) | 7 | \(1+1+6\) | 27 |
| \(1+2+2+3\) | 6 | \(1+2+5\) | 9 |
| \(1+3+4\) | 8 | \(1+7\) | 19 |
| \(3+5\) | 1 |  |  |

The counts sum to 256.  Every listed profile has an odd part, which is
exactly the failure of componentwise even marked parity.  A separate
enumeration of the 256 transversals of (5) finds zero whose induced
multigraph is a forest with all component orders even.

## 5. Why this does not close the order-88 branch

This computation disproves only the proposed implication

> the \(8+8\), 5-regular marked incidence object, even with arbitrary
> compatible cyclic transition data, always has a good bichromatic
> selector.

It does not disprove the unrestricted two-\(T\)-join packing statement.
After subdividing the eight marks, a CNF parity solve finds two
edge-disjoint \(T\)-joins of sizes 32 and 40.  The saved edge lists are
checked directly, without trusting the SAT solver, by recomputing both
boundaries and their disjointness.  Thus this example packs outside the
bichromatic selector image.

It also lies outside the surviving minimum-counterexample class:

- the core and its marked subdivision both have girth \(3\);
- although the displayed colouring separates the marks, switching \(a\)
  and \(c\) on its factor circuit through vertices
  \[
  0,1,16,17,18,19,20,21,22,23
  \]
  produces a Tait colouring in which marked edges 2 and 3 lie on one
  \(bc\)-circuit; hence the marked set is not universally separated; and
- no terminal pairing or minimum-support condition is asserted.

The equality incidence/rotation route therefore needs genuine use of
ambient girth, universal separation, the paired low-cut inequalities, or
minimum-support exchange constraints.  Pure 5-regular incidence and local
rotation data are insufficient.

## 6. Reproduction

From the repository root:

```sh
clang++ -std=c++20 -O3 -Wall -Wextra -pedantic \
  scratch/equality88_rotation_search.cpp \
  -o /tmp/equality88_rotation_search
/tmp/equality88_rotation_search 100000 20260726

python3 -B scratch/verify_equality88_rotation_countermodel.py
python3 -B scratch/audit_equality88_rotation_countermodel.py
```

The deterministic search reaches the displayed zero-selector rotation
system at iteration 9244.  The main verifier also checks the incidence
degrees, rotation incidences, reconstructed simplicity, connectivity,
Tait colouring, factor lengths, selector histogram, planarity, girth,
the explicit Kempe conflict, and the two-\(T\)-join witness.

The certificate is
`scratch/equality88-rotation-countermodel-result.json`.
The SHA-256 values are:

```text
f0088de73fec2c2f858f89d59b77e3492d020a9e889f3a98c4a42687cfcdb963  equality88_rotation_search.cpp
1ffe2c541b5be61a3d11a50cb6e9db5bdd545c135beda50763fdfcd0340b1cd4  verify_equality88_rotation_countermodel.py
dff4bb3f6c34744c10dcaa392f2917efcdc4e95a7758ac0739072fd3ed46e509  audit_equality88_rotation_countermodel.py
4d1bdb6dbad4333f3598dec4eae7566ccc995cb2a69b0fc6e01e16674806e753  equality88-rotation-countermodel-result.json
```

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the equality-case
incidence formulation, searched the finite rotation space, wrote the
checkers, and drafted this note.  The search used heuristic simulated
annealing, but every claimed property of the resulting finite witness is
rechecked exhaustively or by direct graph traversal.  This is not human
peer review, and no claim of resolving the five-cycle double cover
conjecture is made.
