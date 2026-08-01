# Jaeger-tree choice through order 14 and exchange-fibre reduction

Date: 2026-07-28

Status: **EXACT FINITE POSITIVE FRONTIER / MINIMUM ONE-EXCHANGE
COUNTERMODEL / SYMMETRIC-EXCHANGE FIBRE REDUCTION / NOT A UNIVERSAL
PROOF**.

## 1. Forest-coordinate flows

Let \(G\) be connected and let
\(\phi:E(G)\to W-\{0\}\), where \(W=\mathbb F_2^3\), be a flow.  For a
nonzero functional \(\mu\in W^*\), put
\[
 Z_\mu=\{e:\mu(\phi(e))=0\}.
\]
The support of \(\mu\phi\) is Eulerian.  From the fundamental-completion
lemma, it is the coordinate supplied by some spanning tree exactly when
\(Z_\mu\) is a forest.

Define
\[
 {\cal F}(\phi)=\{\mu\in W^*-\{0\}:Z_\mu\text{ is a forest}\}.  \tag{1}
\]
After an invertible change of coordinates, all three coordinates of
\(\phi\) are spanning-tree coordinates if and only if
\[
                    \operatorname{rank}\langle{\cal F}(\phi)\rangle=3.
                                                                    \tag{2}
\]
This is the exact linear-matroid characterization of
*forest-coordinate flow*.  It does not by itself guarantee that the
three extending trees can be chosen with empty common intersection.

There is also an exact criterion for that stronger requirement.  Fix an
ordered functional basis and its three zero forests \(Z_1,Z_2,Z_3\).
There are spanning trees
\[
                 T_i\supseteq Z_i,\qquad T_1\cap T_2\cap T_3=\varnothing
                                                                    \tag{3}
\]
if and only if there are tree extensions \(T_1\supseteq Z_1\) and
\(T_2\supseteq Z_2\) such that, with \(I=T_1\cap T_2\),
\[
                 I\cap Z_3=\varnothing
             \quad\text{and}\quad
                 G-I\text{ is connected}.                    \tag{4}
\]

Necessity is immediate from \(Z_3\subseteq T_3\) and
\(T_3\subseteq E(G)-I\).  Conversely, under (4), the forest \(Z_3\) is
contained in the connected graph \(G-I\), so it extends to a spanning
tree \(T_3\) of \(G-I\).  This gives (3).  The criterion is symmetric
after reordering the coordinates.

## 2. Exact existential census through order 14

Nauty's `geng` canonically generated every connected simple cubic graph
of orders \(4,6,8,10,12,14\).  Every nonbridgeless graph was discarded.
For each remaining graph, the certificate contains:

1. three literal spanning trees with empty common intersection;
2. the nowhere-zero flow obtained by xor of their three fundamental
   completions;
3. a literal compatible potential;
4. every resulting two-point edge label; and
5. a proper five-colouring of the coordinate co-occurrence graph.

The census is:

| order | generated | bridgeless | Tait-colourable | non-Tait | direct Tait-tree witness | searched forest-flow witness |
|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 1 | 1 | 0 | 1 | 0 |
| 6 | 2 | 2 | 2 | 0 | 2 | 0 |
| 8 | 5 | 5 | 5 | 0 | 5 | 0 |
| 10 | 19 | 18 | 17 | 1 | 17 | 1 |
| 12 | 85 | 81 | 80 | 1 | 79 | 2 |
| 14 | 509 | 480 | 475 | 5 | 471 | 9 |
| **total** | **621** | **587** | **580** | **7** | **575** | **12** |

For 575 graphs, a Tait flow directly supplied the witness.  A particular
Tait colouring need not have simultaneous tree extensions satisfying
(3), which accounts for five colourable graphs sent to the general
search.  Together with the seven non-Tait graphs, these are the twelve
searched cases.  In every one, the first normalized flow orbit already
contained a successful forest-coordinate basis; at most thirteen
functional bases were examined.

The complete witness file is
[`witnesses.json`](../output/jaeger-tree-choice-through14/witnesses.json),
SHA-256
```text
12544d274a20e122e18d8962174fc4b74633f47ef38cfe921bae6e870a11add4
```

Reproduction and independent semantic verification:
```sh
python3 scratch/census_jaeger_tree_choice_through14.py
python3 scratch/verify_jaeger_tree_choice_through14.py
```

The verifier independently regenerates the complete `geng` stream,
checks bridgelessness and Tait status, and verifies every tree,
fundamental-completion characterization, flow equation, potential
equation, pair label, coordinate parity, and five-colouring.

This proves only a finite frontier.  It gives no universal selection
theorem.

## 3. The natural one-tree exchange claim is false

For a Jaeger tree triple \((T_1,T_2,T_3)\), define one local move to:

1. choose one \(T_i\);
2. remove one tree edge and add one cotree edge so that \(T_i\) remains a
   spanning tree;
3. require the new three trees still to have empty common intersection;
4. recompute all three fundamental completions; and
5. choose an arbitrary compatible potential for the new flow.

The tempting exchange claim is:

> If the starting tree triple forces an obstruction, some one-tree local
> move yields a five-colourable co-occurrence graph.

This claim is false on the 12-vertex graph
```text
K??FEaKR@oE_
```
with its standard 18-edge order.  Take
```text
T1 = 1 3 6 8 9 11 12 13 14 16 17
T2 = 0 2 3 5 6 7 8 9 10 12 16
T3 = 0 1 2 4 5 7 10 11 13 14 17.
```
These are spanning trees and their common intersection is empty.  Their
fundamental-completion masks are
```text
100085 191542 113496,
```
giving flow
```text
1 2 3 4 7 3 5 1 4 5 3 6 4 6 2 7 5 2.
```
The compatible-potential system has the unique gauged solution
```text
0 5 2 0 3 0 7 4 6 4 4 1,
```
whose labels contain \(K_6\) on
\(\{1,2,3,5,6,7\}\).

There are 105 raw single-tree basis exchanges.  Exactly 27 preserve the
empty-common-intersection condition.  They produce six distinct
nowhere-zero flows.  Every one of the 27 new potential systems again has
one gauged solution and forces a \(K_6\):

| forced \(K_6\) coordinates | exchange multiplicity |
|---|---:|
| \(1,2,3,4,5,7\) | 7 |
| \(1,2,3,4,6,7\) | 3 |
| \(1,2,3,5,6,7\) | 17 |

Thus no admissible one-tree exchange even reduces the obstruction type:
the \(K_6\) moves among coordinate six-sets.

The complete 27-row certificate is
[`report.json`](../output/jaeger-one-tree-exchange-countermodel-12v/report.json),
SHA-256
```text
aca033b668059051aa796755425db56f5dd78650bb8a84886a501bbb98fc2004
```

Reproduction and an independent tree-propagation verifier:
```sh
python3 scratch/audit_jaeger_one_tree_exchange_countermodel.py
python3 scratch/verify_jaeger_one_tree_exchange_countermodel.py
```

The verifier independently enumerates all 105 basis exchanges, recovers
the 27 admissible ones, checks every completion and all six neighbour
flows, enumerates every gauged potential by \(2^{11}\) spanning-tree
choices, and checks every displayed \(K_6\).

This is minimum graph order within the connected simple bridgeless cubic
class.  An obstruction needs at least the 15 distinct co-occurrences of
\(K_6\), so a cubic host has at least ten vertices.  The previously
frozen complete frontier
`scratch/fixed-fano-merge-frontier-n10-direct.json` checks all 26 graphs
and all 3,295 flow orbits through order ten with no fixed-flow
obstruction.  Hence there is no obstructed starting triple, locked or
otherwise, below order twelve.

The same 12-vertex graph has many successful, more distant Jaeger-tree
choices, including the explicit witness in the order-14 census.  This is
therefore a countermodel only to the radius-one exchange lemma, not to the
existential tree-choice statement and not to FiveCDC.

## 4. Coordinated two-tree exchange

The one-tree plateau disappears if one basis exchange is allowed in each
of two distinct trees and only the final triple is required to have empty
common intersection.  On the frozen triple above there are

```text
35, 33, 37
```

basis exchanges in the three trees.  Hence there are 3,671 raw pairs of
exchanges in two distinct trees.  Exactly 358 final triples have empty
common intersection.  Among them, 116 admit a five-colourable compatible
potential and 242 remain obstructed.  They give 46 distinct neighbour
flows, 24 successful and 22 obstructed.

The first successful pair is especially informative:

```text
T1: remove edge 1, add edge 2
T2: remove edge 2, add edge 15.
```

Changing only \(T_1\) changes its completion from \(100085\) to \(179443\)
and gives the successful flow, but the intermediate triple is illegal:
edge 2 lies in all three trees.  Changing only \(T_2\) is legal but
completion-neutral, so it leaves the obstructed flow unchanged.  Together,
the neutral \(T_2\) exchange removes edge 2 from the common intersection
and makes the successful \(T_1\) change feasible.  The final completion
masks and flow are

```text
179443 191542 113496
1 3 2 4 7 3 5 1 4 4 3 7 5 7 2 7 4 3.
```

There are two gauged compatible potentials, both successful.  One is

```text
0 1 7 6 4 2 7 6 4 2 0 1,
```

and its unused coordinate pairs include the disjoint matching

```text
01, 24, 35.
```

This escape is checked independently by

```sh
python3 scratch/audit_jaeger_two_tree_exchange_frozen_12v.py
python3 scratch/verify_jaeger_two_tree_exchange_frozen_12v.py
```

The complete 358-row file is
[`frozen-12v-neighbours.json`](../output/jaeger-two-tree-exchange-through14/frozen-12v-neighbours.json),
SHA-256

```text
21468b526b4322984587675f3a9932d6bd919d254eb72d704be28b6190612749
```

The exact audit can be strengthened from this one state to every
obstructed literal Jaeger triple on the same graph.  The graph has 9,216
spanning trees and 101 distinct fundamental-completion masks.  Its 64 bad
\(\mathrm{GL}(3,2)\)-flow orbits give 1,792 bad completion-support types
modulo permutation of the three coordinates.  Exhausting
1,040,726,016 raw tree products leaves 3,137,600 literal triples with empty
common intersection, again modulo coordinate permutation.  Every one of
the 3,137,600 has a successful coordinated two-tree neighbour.  The
replayable C++ audit is

```sh
c++ -O3 -std=c++20 scratch/audit_jaeger_two_tree_exchange_12v.cpp \
  -o /tmp/audit_jaeger_two_tree_exchange_12v
/tmp/audit_jaeger_two_tree_exchange_12v
```

In fact the program checks a stronger statement: every one of these
states has a neighbour in which at least one of the seven nonzero flow
values occurs at most once.  This implies success without solving the
compatible-potential system.  Indeed, the only two minimal
six-chromatic co-occurrence graphs on eight coordinates are \(K_6\) and
\(K_3\mathbin\vee C_5\).  The pairs of each fixed nonzero difference form
a four-edge matching of \(K_8\).  A \(K_6\) uses at least two pairs of
every difference (three for the difference of its two omitted points).
The complement of \(K_3\mathbin\vee C_5\) is a five-cycle; a matching
contains at most two edges of that cycle, so the obstruction again uses
at least two pairs of every difference.  A flow direction occurring at
most once therefore rules out both obstructions for every potential.

### Canonical frontier through order 14

The coordinated-neighbour statement was then audited for every connected
simple bridgeless cubic graph through order 14.  For each graph the
program independently enumerates all nowhere-zero
\(\mathbb F_2^3\)-flow orbits, solves every compatible-potential space,
enumerates every spanning tree and fundamental completion, and checks
every obstructed literal tree triple modulo coordinate permutation.

| order | graphs | flow orbits | bad flow orbits | graphs with a bad orbit | bad support types | bad literal triples | successful neighbours |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 4 | 1 | 2 | 0 | 0 | 0 | 0 | 0 |
| 6 | 2 | 15 | 0 | 0 | 0 | 0 | 0 |
| 8 | 5 | 178 | 0 | 0 | 0 | 0 | 0 |
| 10 | 18 | 3,164 | 0 | 0 | 0 | 0 | 0 |
| 12 | 81 | 73,459 | 351 | 13 | 9,780 | 19,014,690 | 19,014,690 |
| 14 | 480 | 2,218,848 | 20,107 | 250 | 535,900 | 3,052,488,205 | 3,052,488,205 |
| **total** | **587** | **2,295,666** | **20,458** | **263** | **545,680** | **3,071,502,895** | **3,071,502,895** |

Thus:

> Every obstructed literal Jaeger tree triple in every connected simple
> bridgeless cubic graph through order 14 has a successful coordinated
> two-tree basis-exchange neighbour.

The enumeration considered 8,243,504,814,802 raw products of tree
extension fibres before the empty-common-intersection filter.  The
combined report is
[`census-combined.json`](../output/jaeger-two-tree-exchange-through14/census-combined.json),
SHA-256

```text
29a3d70d8137cd7d871b091262c57e995db7eae94de978757ea6840768186ead
```

The producer source has SHA-256

```text
b5bd28fc05bf57b9d3a394ecd5c6504a8f79e3ff93cf76521dc12607a6ba5fa3
```

and the independent structural verifier regenerates all 621 canonical
input graphs, rechecks the 587 bridgeless premises, checks every
aggregate, and cross-checks the rigid graph against the separate
all-flow audit:

```sh
python3 scratch/verify_jaeger_two_tree_exchange_through14.py
```

For replay, compile
`scratch/census_jaeger_two_tree_exchange_through14.cpp`.  OpenMP is
optional; it only parallelizes independent bad support types.

This remains a finite theorem, not a universal exchange lemma.

### Exchange identity

There is a short human proof of the algebra used by the audit.  Let
\(F(T)\) be the xor of the fundamental circuits of all cotree edges of a
spanning tree \(T\).  Make the basis exchange

\[
                 T'=T-a+b,\qquad a\in C_T(b),
\]

where \(C_T(b)\) is the fundamental circuit of the old cotree edge \(b\).
In the old cotree coordinates, the required coefficients of \(F(T')\)
are one on every cotree edge except possibly \(b\).  Thus \(F(T')\) is
either \(F(T)\) or \(F(T)\mathbin\triangle C_T(b)\).  Since \(a\) must have
coefficient one in the new cotree description, the choice is forced:

\[
 F(T')=
 \begin{cases}
 F(T),&a\in F(T),\\
 F(T)\mathbin\triangle C_T(b),&a\notin F(T).
 \end{cases}                                      \tag{5}
\]

For the successful pair above, the first fundamental circuit is the edge
set

```text
1 2 9 11 12 13 16 17
```

(mask 211462); removed edge 1 is not in \(F(T_1)\), so this circuit is
xored into the first completion.  The second circuit has edge set

```text
0 2 3 5 15 16
```

(mask 98349); removed edge 2 is in \(F(T_2)\), so the second completion is
unchanged.

Consequently the first stronger human statement suggested by the
finite audit was not ordinary basis exchange, but a constrained
two-basis avoidance lemma: for every bad triple of graphic-matroid bases
with empty common intersection, two exchanges must simultaneously

1. keep the final triple's common intersection empty; and
2. move the three completion supports, according to (5), outside the
   graph-dependent set of Oum-bad flows.

Standard strong basis exchange supplies neither the three-basis
intersection constraint nor avoidance of that nonlinear bad-flow set.
Any universal proof needs an additional coupled exchange or covering
property.  One initially attractive sufficient target was to make one
Fano value class have size at most one.  If only coordinate \(i\)
changes on a fundamental circuit \(C\), then for every value \(d\)

\[
 |E_d(\phi')|
   = |E_d(\phi)-C| + |E_{d+e_i}(\phi)\cap C|.       \tag{6}
\]

Thus a circuit satisfying the right side of (6) at most one, together
with a second exchange that repairs the triple-intersection constraint,
would escape every \(K_6\) and \(K_3\mathbin\vee C_5\) obstruction
uniformly.  The next subsection records why this is only a sufficient
condition and cannot be the terminal condition of a universal descent.

### The direction-thinning target is not universal

The last sufficient target also fails as a universal local lemma.  Its
minimum countermodel found by the canonical search has order 14 and
graph6 encoding

```text
M???FBObBCF?B_D_?
```

It is simple, cubic, bipartite, nonplanar, and 3-vertex- and
3-edge-connected.  For the tree masks

```text
1950903 1218046 1014601
```

the completion masks are

```text
211822 1010371 1412534,
```

and the seven nonzero flow values occur with multiplicities

```text
2 3 4 4 3 2 3.
```

The unique compatible potential forces a \(K_6\).  Among 5,628 raw
coordinated pairs of exchanges, 379 are admissible, and none makes a
flow-value class have size at most one.  Nevertheless 329 of the 379
are successful after the potential test.  The first success is the
reciprocal exchange that swaps edge 0 of the first tree with edge 3 of
the second tree.  Thus direction thinning is sufficient but not the
mechanism behind coordinated escape.

The exact report is
[`direction-thinning-countermodel-14v.json`](../output/jaeger-two-tree-exchange-through14/direction-thinning-countermodel-14v.json),
SHA-256

```text
219eb34e9a96f512f9739482d94976bf26d3065fdcdc74accd87f93f2d97a79b
```

and is independently replayed by

```sh
python3 scratch/audit_jaeger_direction_thinning_countermodel_14v.py
python3 scratch/verify_jaeger_direction_thinning_countermodel_14v.py
```

### Symmetric exchanges and fixed-multiplicity fibres

There is a more rigid coordinated move.  For two of the three trees,
make a reciprocal symmetric basis exchange

\[
 T_i'=T_i-e+f,\qquad T_j'=T_j-f+e,
\]

where both displayed sets are spanning trees.  This move preserves
their intersection exactly:

\[
                         T_i'\cap T_j'=T_i\cap T_j.            \tag{7}
\]

Consequently it automatically preserves the empty common intersection
of the triple.  It also preserves, for every graph edge \(a\), the tree
multiplicity

\[
              m_a=\bigl|\{k:a\in T_k\}\bigr|.                 \tag{8}
\]

Conversely, Blasiak's proof of White's conjecture for graphic matroids
shows that two multisets of spanning trees with the same multiset union
are connected by single-element symmetric exchanges.  Therefore,
after quotienting by the harmless \(S_3\)-action permuting the three
flow coordinates, the symmetric-exchange components are precisely the
feasible fixed-\(m\) fibres.  The imported result is:

> J. Blasiak, *The toric ideal of a graphic matroid is generated by
> quadrics*, Combinatorica **28** (2008), 283--297,
> DOI 10.1007/s00493-008-2256-6.

For a cubic graph this invariant has only three units of freedom.  If
\(|V(G)|=n\), then \(|E(G)|=3n/2\), while the three trees contain
\(3(n-1)\) edge occurrences.  Empty common intersection says
\(m_a\leq2\), and hence

\[
             \sum_{a\in E(G)}(2-m_a)
               =2|E(G)|-3(n-1)=3.                            \tag{9}
\]

Every fibre therefore has one of exactly two defect types:

1. three distinct edges have multiplicity one and every other edge has
   multiplicity two; or
2. one edge has multiplicity zero, one other edge has multiplicity one,
   and every other edge has multiplicity two.

Equivalently, the three complementary cotrees cover \(E(G)\) and have
total covering excess exactly three.  This is a substantial reduction
of the exchange problem: the component invariant is not an arbitrary
vector on \(E(G)\), but one of these two three-defect patterns.

There is no separate existence gap on a 3-edge-connected graph.  For a
connected graph, three spanning trees with empty common intersection
exist exactly when the ground set of the cographic matroid is coverable
by three bases.  The matroid partition theorem and

\[
 r_{M(G)^*}(A)=|A|+1-c(G-A)
\]

give the exact criterion

\[
                 3\bigl(c(G-A)-1\bigr)\leq2|A|
                 \quad\text{for every }A\subseteq E(G).       \tag{10}
\]

If \(G\) is 3-edge-connected and \(c(G-A)\geq2\), sum the boundaries of
the components of \(G-A\).  Each has at least three edges, and each
edge of \(A\) is counted at most twice, so
\(3c(G-A)\leq2|A|\), which is stronger than (10).  Thus every
3-edge-connected graph has at least one such triple.

The exact order-12 audit checked all 19,014,690 obstructed literal
states and found a successful *symmetric* exchange for every one.  The
14-vertex direction-thinning countermodel above also has an immediate
successful symmetric exchange.  These are finite theorems, not the
missing universal statement.

The remaining proof obligation is now particularly crisp:

> **Fixed-fibre representative lemma.**  In every feasible
> three-spanning-tree multiplicity fibre of a 3-edge-connected cubic
> graph, at least one tree triple has a fundamental-completion flow with
> a five-colourable compatible Oum potential.

If this lemma is true, Blasiak connectivity proves that no
symmetric-exchange component is all bad.  On the 3-edge-connected cubic
class it would prove FiveCDC; extending that conclusion to the original
formulation also requires the exact reduction, verified separately.
If it is false, one explicit all-bad defect fibre is the decisive
countermodel to this proof route.  At present neither outcome has been
proved.

### Exact fixed-fibre SAT frontier

The feasibility part of the fibre problem is actually unconditional on
the 3-edge-connected cubic class.  Let \(d_e=2-m_e\), so that
\(\sum_e d_e=3\), and replace every edge \(e\) by \(2-d_e\) parallel
copies.  Call the resulting multigraph \(H_d\).  For a partition
\(\mathcal P\) of \(V(G)\) into \(r\geq2\) parts, 3-edge-connectivity
gives

\[
  2|E_G(\mathcal P)|
    =\sum_{X\in\mathcal P}|\delta_G(X)|\geq3r.
\]

At most the three defect copies cross the partition, and therefore

\[
        |E_{H_d}(\mathcal P)|
           =2|E_G(\mathcal P)|
              -\sum_{e\in E_G(\mathcal P)}d_e
           \geq3r-3.                                         \tag{11}
\]

The Nash-Williams--Tutte spanning-tree-packing theorem gives three
edge-disjoint spanning trees in \(H_d\).  Since

\[
                    |E(H_d)|=2|E(G)|-3=3(n-1),
\]

the three trees partition all copies of \(H_d\).  Projecting copies
back to \(G\) realizes the prescribed multiplicity fibre.  Thus *every*
type-A or type-B defect placement is feasible on every
3-edge-connected cubic graph.

An incremental certificate-checking SAT encoding then asked whether
each fibre has a good representative.  Its tree variables are encoded
as rooted arborescences with strictly decreasing unary depth.  The
fundamental completion \(F(T_i)\) is encoded by the two conditions

\[
                  E(G)-T_i\subseteq F(T_i),
        \qquad F(T_i)\text{ is Eulerian};
\]

uniqueness proves this is the literal fundamental completion.  Rather
than assume a potential formula, the remaining variables encode an
eight-point pair labelling, pair xor equal to the three completion
bits, coordinate parity at every vertex, and a proper five-colouring
of the used coordinate pairs.  The pair-data equivalence proved
separately shows that this is exactly a successful compatible Oum
potential.  Every SAT model is then rechecked directly by graph
traversal, recomputation of all three fundamental completions,
coordinate parity, pair xor, and the displayed five-colouring.

Of the 587 connected simple bridgeless cubic graphs through order 14,
324 have no obstructed completion flow at all.  On the remaining 263
hard graphs the audit tested 452,086 defect placements.  Exactly
450,786 were feasible; every one of those 450,786 has a good
representative.  The 1,300 infeasible placements all lie on two
edge-connectivity-two graphs.  In particular:

> Every feasible three-tree multiplicity fibre in every connected
> simple bridgeless cubic graph through order 14 has a good
> representative.

The complete report is
[`fixed-fibre-hard-through14.jsonl`](../output/jaeger-two-tree-exchange-through14/fixed-fibre-hard-through14.jsonl),
SHA-256

```text
3a685728f0a0e9f46b3673905b88431c33a70c855d568ce8af64bbd178ce7526
```

The most proof-friendly subfamily fixes a vertex \(v\) and puts the
three defects on \(\delta(v)\).  Every resulting tree has \(v\) as a
leaf, and the three incident completion-flow values are necessarily

\[
                         110,\quad101,\quad011.               \tag{12}
\]

Across all 419 simple 3-edge-connected cubic graphs through order 14,
all 5,646 vertex-star fibres have a representative in which one of

\[
                         110,101,011,111                     \tag{13}
\]

occurs at most once.  Since the first three values already occur once
at \(v\), choosing one of them means it is unique.  This finite pattern
suggested the following substantially narrower sufficient theorem.

> **Vertex-star thinning lemma.**  For every 3-edge-connected cubic
> graph \(G\) and vertex \(v\), the edges of
> \(2G-\delta(v)\) can be partitioned into three spanning trees so that
> the fundamental-completion flow has a value in
> \(\{110,101,011,111\}\) occurring at most once.

The packing argument above already proves the required tree partition
exists.  The direction-count observation proves that the conclusion of
the vertex-star thinning lemma would make the Oum pair cover
five-colourable for every compatible potential.  Hence this one
statement would prove FiveCDC for 3-edge-connected cubic graphs; a
separately justified reduction would then transfer it to the intended
general formulation.  **The lemma is false.**

The exact countermodel has 34 vertices and graph6 encoding

```text
as???SK????A?A?C_@_?B?@_??G??_I?GA_AA????_??@?????B??@_?o??????_C??CGO??B@????a????__??C@O??A?_
```

It is simple, cubic, nonplanar, nonbipartite, and 3-vertex- and
3-edge-connected.  In column-major edge order, edges 0, 1, and 2 form
the star at vertex 0.  Fix

\[
 m_0=m_1=m_2=1,\qquad m_e=2\quad(3\leq e<51).
\]

For **every** triple of spanning trees in this fixed fibre and **every**
nonzero \(d\in\mathbb F_2^3\), the associated
fundamental-completion flow satisfies

\[
                         |E_d(\phi)|\geq2.                    \tag{14}
\]

Thus no Fano direction can be thinned, including all four directions in
(13).  The semantic CNF has 4,444 variables and 251,803 clauses.  Its
files are
[`star-thin-any.cnf`](../output/jaeger-star-thinning-countermodel-34v/star-thin-any.cnf)
and
[`star-thin-any.lrat`](../output/jaeger-star-thinning-countermodel-34v/star-thin-any.lrat),
with SHA-256 values

```text
8c96bd3d02685c12dca1eee78047459c65a60b0defdf87b68c000274dee9e6c0
a9600d2cf2efa191f789438f811f116932d79ca0493f1522bc7e3b0ccee01ae4
```

respectively.  The LRAT is accepted independently by both
`lrat-check` and the verified CakeML checker `cake_lpr`.  The
independently written verifier also checks the graph premises and the
CNF semantics:

```sh
python3 scratch/verify_jaeger_star_thinning_countermodel_34v.py
```

This is a countermodel only to thinning.  The same fixed fibre has a
checked good representative supported on exactly the five Oum points

```text
3 4 5 6 7.
```

All ten pairs among those five points occur, so the five coordinate
subgraphs themselves are a literal FiveCDC; no colour merging is
needed.  Its seven flow-value counts are

```text
7 5 10 7 7 7 8.
```

This witness is still non-thin, and support four is impossible because
four points realize at most six nonzero pair differences whereas (14)
forces all seven.  The fully displayed trees, labels, and human semantic
proof are in
[`jaeger-fixed-fibre-independent-audit.md`](jaeger-fixed-fibre-independent-audit.md).
The independently written checker reparses graph6, verifies all three
trees and star multiplicities, recomputes the fundamental completions,
and checks every flow value, pair xor, local parity, and co-occurrence:

```sh
python3 scratch/verify_jaeger_34v_star_good_witness.py
```

For comparison, the adjacent type-B choice puts multiplicity zero on
an edge \(e_0\) and multiplicity one on an adjacent edge.  It forces
flow value \(111\) on \(e_0\).  All 33,876 such fibres through order 14
have a representative with some *non-\(111\)* value occurring at most
once.

The still sharper one-direction guesses were already false.  Requiring
\(111\) to be absent in every vertex-star fibre already fails on the
Petersen graph

```text
ICOf@pSb?
```

and requiring \(111\) to be unique in every adjacent type-B fibre first
fails on three order-12 graphs.  The 34-vertex certificate (14) now
shows that even the disjunctive set (13), and indeed every possible
direction-thinning target, is false.

The special-fibre report is
[`special-defect-fibres-through14.jsonl`](../output/jaeger-two-tree-exchange-through14/special-defect-fibres-through14.jsonl),
SHA-256

```text
9b01ad63b0811df259e89a9651932a8498f8e5a02c834ec1d97fb8f11684bbd6
```

Reproduction and an independently written structural verifier:

```sh
python3 scratch/run_jaeger_fixed_fibre_frontier.py \
  --mode full --workers 8 \
  --output output/jaeger-two-tree-exchange-through14/fixed-fibre-hard-through14.jsonl
python3 scratch/run_jaeger_fixed_fibre_frontier.py \
  --mode special --workers 8 \
  --output output/jaeger-two-tree-exchange-through14/special-defect-fibres-through14.jsonl
python3 scratch/verify_jaeger_fixed_fibre_frontier.py
```

## 5. Frozen frontier

The surviving fixed-fibre problem is exactly:

> Does every feasible Type-A or Type-B three-tree multiplicity fibre of
> a cubic 3-edge-connected graph have a representative whose compatible
> Oum pair labelling has a five-colourable co-occurrence graph?

The answer is exactly verified through order 14 in the strictly stronger
**support-five** form: every one of the 804,204 feasible fibres among
all 944,974 Type-A/Type-B placements has a checked compatible Oum pair
labelling using at most five of the eight points.  Those five point
coordinates are themselves the five Eulerian subgraphs of a FiveCDC;
no colouring or merge is needed.  The complete 587-graph report is
[`census.jsonl`](../output/jaeger-five-point-fibres-through14/census.jsonl),
SHA-256

```text
482e2ee028aa1663f2b91b71569422ab59c1033d51601ca52fac581b173872f1
```

and is reproduced and structurally checked by

```sh
python3 scratch/run_jaeger_five_point_frontier.py --workers 8 \
  --output output/jaeger-five-point-fibres-through14/census.jsonl
python3 scratch/verify_jaeger_five_point_frontier.py
```

There is an exact human criterion for this selection target.  Given a
three-point omitted set \(B\subset W=\mathbb F_2^3\), write its affine
span as \(A=b+U_0\), let \(a^*=A-B\), and put \(S=W-B\).  For a
completion flow \(\phi\), define

\[
 E_0=\{e:\phi(e)\in U_0\}.
\]

At every degree-one vertex \(v\) of a component of \((V,E_0)\), the
local flow plane forces one binary port value \(\ell_v\).  The
component-parity theorem proves that a compatible pair labelling
supported in \(S\) exists if and only if

\[
             \bigoplus_{v\in L(Q)}\ell_v=0
             \qquad\text{for every component }Q\text{ of }(V,E_0).
                                                               \tag{15}
\]

The local classification, the incidence-matrix proof of (15), and an
independent exhaustive checker are in
[`jaeger-support5-component-criterion.md`](jaeger-support5-component-criterion.md):

```sh
python3 scratch/verify_jaeger_support5_component_criterion.py
```

Thus the surviving human target is the following exact selection lemma:

> **Component-leaf-parity selection lemma.**  In every feasible
> Type-A or Type-B fixed multiplicity fibre of a 3-edge-connected cubic
> graph, one can choose the three trees and an omitted triple \(B\) so
> that (15) holds in every component.

This statement is **unproved**.  It is equivalent to support-five
selection inside every fibre and is stronger than necessary: proving it
even just for one vertex-star fibre in each 3-edge-connected cubic graph
would resolve FiveCDC after the stated reductions.  The finite census
cannot replace this missing parity-selection proof.

For independent cross-checking, the weaker support-six property was
also frozen on the same 804,204 feasible fibres.  Its report
[`census.jsonl`](../output/jaeger-six-point-fibres-through14/census.jsonl)
has SHA-256

```text
9bfa6ba83f22a6b2013699a817662ce3e6d57734f86d332c23463bfa8b02cfd6
```

and is checked by `scratch/verify_jaeger_six_point_frontier.py`.

Single-tree descent is ruled out by the order-12 radius-one
countermodel; coordinated-neighbour direction thinning is ruled out by
the order-14 countermodel; and fixed-vertex-star thinning in every one
of the seven directions is ruled out by the certified 34-vertex fibre.
None of these no-go results is a counterexample to component-parity
selection, the good-representative lemma, or FiveCDC.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated the forest and
simultaneous-extension criteria, ran the canonical census, found the
locked exchange triple, wrote both producers and independent verifiers,
and drafted this note.  All finite claims have replayable literal
certificates.  This is not independent peer review and is not claimed as
a resolution of FiveCDC.
