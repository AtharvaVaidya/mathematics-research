# A certified 34-vertex countermodel to universal star thinning

Date: 2026-07-28

Status: **EXACT COUNTERMODEL TO THE STAR-THINNING LEMMA / THE SAME
FIBRE HAS A VERIFIED FIVE-CYCLE DOUBLE COVER / NOT A COUNTEREXAMPLE TO
FIVECDC**.

## 1. The graph and fixed fibre

The graph has graph6 encoding

```text
as???SK????A?A?C_@_?B?@_??G??_I?GA_AA????_??@?????B??@_?o??????_C??CGO??B@????a????__??C@O??A?_
```

Edges are ordered column-major.  The first three are

```text
0:(0,1)  1:(0,2)  2:(0,3).
```

Direct graph checks give 34 vertices, 51 edges, simplicity, cubicity,
connectivity, edge-connectivity three, vertex-connectivity three,
nonbipartiteness, nonplanarity, and no bridges.

Fix the vertex-star multiplicities

\[
 m_0=m_1=m_2=1,\qquad m_e=2\quad(3\leq e<51).       \tag{1}
\]

A state in this fibre is an ordered triple of spanning trees
\((T_1,T_2,T_3)\) with
\(\sum_i1_{e\in T_i}=m_e\).  Let \(F_i\) be the fundamental completion
of \(T_i\), and put

\[
 \phi(e)=\sum_{i=1}^3 1_{e\in F_i}2^{i-1}
       \in\mathbb F_2^3-\{0\}.                       \tag{2}
\]

The certified statement is:

> **Countermodel theorem.**  For every state in the fixed fibre (1) and
> every \(d\in\mathbb F_2^3-\{0\}\),
> \[
>                       |\phi^{-1}(d)|\geq2.          \tag{3}
> \]

Thus the graph refutes not only the proposed vertex-star target using
\(011,101,110,111\), but the stronger claim that some star-fibre state
has *any* Fano direction occurring at most once.

## 2. Human semantic proof of the CNF

The independently written generator
`scratch/certify_jaeger_star_thinning_countermodel_34v.py` produces a
CNF with 4,444 variables and 251,803 clauses.

For each coordinate \(i\), the tree variables are tied to a rooted
orientation.  Every nonroot vertex chooses exactly one parent edge,
the root chooses none, and unary levels strictly decrease from a child
to its parent.  Hence the chosen edges form a connected acyclic graph
with 33 edges: exactly a spanning tree.  Conversely every spanning
tree has such an orientation and level assignment.

The clauses on each edge impose exactly (1).  Completion variables
\(f_{e,i}\) satisfy

\[
 e\notin T_i\Longrightarrow f_{e,i}=1
 \quad\text{and}\quad
 \sum_{e\in\delta(x)}f_{e,i}=0\pmod2
 \quad(x\in V(G)).                                  \tag{4}
\]

An Eulerian set containing every cotree edge is unique: the symmetric
difference of two such sets would be an Eulerian subset of a tree and
therefore empty.  Thus (4) encodes the literal fundamental completion,
not a relaxation of it.  Condition (1) also ensures that at least one
coordinate is one on every edge.

For every edge and each \(d=1,\ldots,7\), a Tseitin variable is
equivalent to \(\phi(e)=d\).  Exactly one value \(d\) is selected, and
pairwise clauses forbid two different edges from both having that
value.  Consequently the CNF is satisfiable exactly when (3) is false.

The CNF
[`star-thin-any.cnf`](../output/jaeger-star-thinning-countermodel-34v/star-thin-any.cnf)
has SHA-256

```text
8c96bd3d02685c12dca1eee78047459c65a60b0defdf87b68c000274dee9e6c0
```

CaDiCaL 3.0.1 produced the 61 MB text LRAT certificate
[`star-thin-any.lrat`](../output/jaeger-star-thinning-countermodel-34v/star-thin-any.lrat),
SHA-256

```text
a9600d2cf2efa191f789438f811f116932d79ca0493f1522bc7e3b0ccee01ae4
```

It is accepted independently by both `lrat-check` and the verified
CakeML checker `cake_lpr`.

## 3. Exact exchange law and the failed descent

Delete vertex 0 and call the resulting graph \(H\).  After assigning
the three spokes to the three trees, a fibre state is equivalently a
partition

\[
 E(H)=A_1\mathbin{\dot\cup}A_2\mathbin{\dot\cup}A_3,
 \qquad S_i=E(H)-A_i\text{ a spanning tree}.          \tag{5}
\]

The restriction \(Q_i=F_i\cap E(H)\) is the unique join of the two
terminals opposite the \(i\)-th spoke that contains \(A_i\).

Take \(f\in A_i\) and \(e\in A_j\).  Swapping their cotree colours gives

\[
 A_i'=A_i-f+e,\quad A_j'=A_j-e+f,
\]
\[
 S_i'=S_i-e+f,\quad S_j'=S_j-f+e.                    \tag{6}
\]

It is a legal symmetric exchange exactly when

\[
                e\in C_{S_i}(f),\qquad
                f\in C_{S_j}(e).                     \tag{7}
\]

The joins then obey the exact update law

\[
 Q_i'=
 \begin{cases}
 Q_i,&e\in Q_i,\\
 Q_i\mathbin\triangle C_{S_i}(f),&e\notin Q_i,
 \end{cases}
\qquad
 Q_j'=
 \begin{cases}
 Q_j,&f\in Q_j,\\
 Q_j\mathbin\triangle C_{S_j}(e),&f\notin Q_j.
 \end{cases}                                        \tag{8}
\]

Indeed, in the first case the old join already contains the new cotree
set.  In the second, toggling the unique fundamental circuit removes
the old cotree edge \(f\), inserts the new cotree edge \(e\), preserves
the join boundary, and contains every member of \(A_i'\).  Uniqueness
then proves (8).  The proof for \(j\) is identical.

If only coordinate \(i\) is active on circuit \(C\), and
\(n_d=|\phi^{-1}(d)|\), then

\[
 n_d'=n_d-|C\cap\phi^{-1}(d)|
             +|C\cap\phi^{-1}(d+2^{i-1})|.           \tag{9}
\]

When both coordinates are active, the exact new value at an edge is

\[
 \phi'(a)=\phi(a)
   +1_{a\in C_{S_i}(f)}2^{i-1}
   +1_{a\in C_{S_j}(e)}2^{j-1}.                      \tag{10}
\]

A natural nonnegative descent potential is

\[
                P=\prod_{d=1}^7\max(n_d-1,0),        \tag{11}
\]

or the four-factor restriction to \(d=3,5,6,7\).  Its zero set is
exactly the proposed thinning conclusion.  Certificate (3) proves
that \(P>0\) throughout this entire symmetric-exchange fibre.
Therefore no extremal-exchange proof whose terminal condition is
direction thinning can succeed.  Equations (8)--(10) remain valid, but
the target potential was wrong.

## 4. Why the same fibre still succeeds

The obstruction is only to a sufficient thinning rule.  A separately
encoded SAT instance can impose the stronger requirement that at most
six of the eight Oum coordinate points occur.  It finds the following
literal tree masks:

```text
1526086090292436
841235911889914
2136277625188137
```

Their independently recomputed fundamental completions are

```text
1080729282132779
1604148423146565
1545481159659998.
```

The seven flow-value counts are

```text
4 3 12 10 7 6 9,
```

so this successful representative is itself nowhere near direction
thinning.  Its eight point coordinates have the proper five-colouring

```text
1 1 0 3 4 4 2 0.
```

Only the six points

```text
0 3 4 5 6 7
```

occur.  Among their fifteen possible pairs, exactly one, \(45\), is
missing; all other fourteen occur.  Merging points 4 and 5 therefore
gives five Eulerian edge subsets covering every edge twice.  This is
the irreducible six-point success mechanism: one unused pair on the
six-point support.

The complete labels and the resulting five-coordinate labels are in
[`star-good-six-witness.json`](../output/jaeger-star-thinning-countermodel-34v/star-good-six-witness.json),
SHA-256

```text
e3160e5f6b2985823a3421e9f3b1a4582c9c8be4b9abfd1f0e2312d311eb8358
```

The independently written verifier checks the graph, the three trees,
the star multiplicities, the completion characterization, all pair
xors, all local parity equations, the five-colouring, the resulting
five-cover, and both proof checkers:

```sh
python3 scratch/verify_jaeger_star_thinning_countermodel_34v.py
```

The correct surviving target must therefore optimize the full
non-co-occurrence packing condition—\(3K_2\), \(K_3+K_2\), or
\(K_4\)—rather than a single flow-value count.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the graph by exact SAT
search, independently regenerated the CNFs, produced and checked the
LRAT certificate, constructed the successful five-cover, and drafted
this note.  The result refutes a proposed proof lemma only and is not
claimed as a resolution of FiveCDC.
