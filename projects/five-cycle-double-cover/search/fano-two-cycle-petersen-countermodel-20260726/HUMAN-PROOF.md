# Human-checkable proof and exact scope

## 1. What is, and is not, disproved

Fix a nowhere-zero \(\mathbb F_2^3\)-flow \(f\), a nonzero functional
\(\mu\), and its kernel line
\[
L=\ker\mu-\{0\}.
\]
Put \(F_L=\{e:f(e)\in L\}\).  Every flow with the same
\(\mu\)-projection can be written
\[
f'_e=b\,\mu(f_e)+(p_e,q_e),
\]
where \(p,q\) are binary cycles and \(b\notin\ker\mu\).  It is
nowhere-zero exactly when \(p_e\lor q_e=1\) on \(F_L\).  A component
\(W\) of \(F_L\) is not rainbow-odd exactly when
\[
\sum_{e\in\delta(W)}p_eq_e=0.                         \tag{1}
\]

This package gives a Petersen flow for which no such \(p,q\) exist when
\(L=\{1,2,3\}\), and likewise when \(L=\{1,6,7\}\).

This only refutes universal **fixed-line, fixed-\(\mu\)-projection**
cleaning.  It does not say that every line fails, does not forbid
changing \(\mu\circ f\), and does not refute five-CDC.

## 2. The graph and flow

Edges are indexed in this order:

| id | edge | \(f(e)\) |
|---:|:---:|---:|
| 0 | 0--2 | 6 |
| 1 | 0--4 | 3 |
| 2 | 0--6 | 5 |
| 3 | 1--4 | 5 |
| 4 | 1--7 | 1 |
| 5 | 1--8 | 4 |
| 6 | 2--3 | 2 |
| 7 | 2--7 | 4 |
| 8 | 3--5 | 5 |
| 9 | 3--8 | 7 |
| 10 | 4--5 | 6 |
| 11 | 5--9 | 3 |
| 12 | 6--8 | 3 |
| 13 | 6--9 | 6 |
| 14 | 7--9 | 5 |

The flow-conservation triples at vertices are:

| vertex | incident values | XOR |
|---:|:---:|---:|
| 0 | 6,3,5 | 0 |
| 1 | 5,1,4 | 0 |
| 2 | 6,2,4 | 0 |
| 3 | 2,5,7 | 0 |
| 4 | 3,5,6 | 0 |
| 5 | 5,6,3 | 0 |
| 6 | 5,3,6 | 0 |
| 7 | 1,4,5 | 0 |
| 8 | 4,7,3 | 0 |
| 9 | 3,6,5 | 0 |

The edge list is visibly simple and cubic.  Direct deletion of each edge
leaves the graph connected.  Exhaustive shore enumeration gives cyclic
edge-connectivity five.  Shortest-path checks after each edge deletion
give girth five.  Nauty gives canonical graph6 `IsP@OkWHG`; an explicit
isomorphism check identifies the Petersen graph.

## 3. The two failed lines

For \(L=123\), the factor consists of the five disjoint edges
\[
\{1,4,6,11,12\},
\]
with vertex components
\[
\{0,4\},\{1,7\},\{2,3\},\{5,9\},\{6,8\}.
\]
For \(L=167\), it consists of edge ids
\[
\{0,4,9,10,13\},
\]
with components
\[
\{0,2\},\{1,7\},\{3,8\},\{4,5\},\{6,9\}.
\]

In either case, contract the five displayed matching edges.  The ten
remaining edges join every pair of contracted vertices exactly once.
Thus the quotient is the simple graph \(K_5\).

Suppose a clean lift \(f'\) preserving \(\mu\circ f\) existed.  On the
ten affine edges, its four affine colors partition \(E(K_5)\).
Cleanliness says that every one of these four color classes has even
degree at each contracted vertex.  Every nonempty even subgraph of the
simple graph \(K_5\) contains a cycle and therefore has at least three
edges.  Four nonempty classes would require at least \(4\cdot3=12\)
edges, but \(K_5\) has only ten.  Hence some affine color is absent.

Choose that absent affine color as the base \(b\) in the decomposition
\[
                         f'=b(\mu\circ f)+s,
\qquad s:E(G)\to\ker\mu\cong{\mathbb F}_2^2.
\]
On every affine edge, \(s\ne0\), since the color \(b\) is absent.  On
every factor edge, \(s=f'\ne0\), since \(f'\) is nowhere-zero.  Therefore
\(s\) is a nowhere-zero \(\mathbb F_2^2\)-flow on the whole Petersen
graph.  At every cubic vertex its three incident nonzero values are the
three distinct nonzero elements of \(\mathbb F_2^2\), so this is a
proper three-edge-coloring.

The Petersen graph has no such coloring.  For a self-contained finite
check, its six perfect matchings in the displayed edge indexing are
\[
\begin{gathered}
(0,3,8,12,14),\ (0,4,9,10,13),\
(1,4,6,11,12),\\
(1,5,7,8,13),\ (2,3,7,9,11),\
(2,5,6,10,14).
\end{gathered}
\]
The complement of each is two 5-cycles.  In a three-edge-coloring, one
color class is a perfect matching and its complement alternates the
other two colors, so every complementary cycle would have even length.
This contradiction proves both fixed-line UNSAT claims without SAT or
exhaustive cycle-pair enumeration.

The following independent exhaustion is retained as a cross-check.
The cycle space has dimension \(15-10+1=6\), hence exactly 64 binary
cycles.  For either failed line, exhaustive enumeration gives:

| condition | ordered pairs \(p,q\) |
|:---|---:|
| all binary-cycle pairs | 4,096 |
| pairs covering the five factor edges | 960 |
| covering pairs satisfying (1) on all five components | **0** |

More explicitly, among the 960 covering pairs the nonzero five-bit
defect masks and multiplicities are:

| masks | multiplicity each |
|:---|---:|
| 00011, 00101, 00110, 01001, 01010, 01100, 10001, 10010, 10100, 11000 | 72 |
| 01111, 10111, 11011, 11101, 11110 | 48 |

These are all fifteen nonzero even-weight five-bit vectors.  The zero
mask never occurs.  `independent_checker.py` derives the table directly
from vertex parity and (1); it does not read the CNFs.

The ordinary CNFs use variables \(p_e,q_e\), product variables
\(r_e\leftrightarrow(p_e\land q_e)\) on factor-component cuts, cubic
even-parity clauses at every vertex, cover clauses on factor edges, and
chain XOR clauses imposing even product parity.  Both instances have 65
variables and 210 clauses.  CaDiCaL's DRAT proofs are independently
checked by `drat-trim`.

## 4. The other lines and the positive five-CDC

The other five lines have explicit \(p,q\) witnesses in
`construction.json`; the independent checker verifies them from the
graph semantics.

The following five Eulerian edge-id sets cover every edge exactly twice:
\[
\begin{aligned}
&[0,1,3,4,7],\\
&[3,5,8,9,10],\\
&[0,2,6,8,11,13],\\
&[1,2,4,5,10,11,12,14],\\
&[6,7,9,12,13,14].
\end{aligned}
\]
This directly proves that the displayed graph is not a five-CDC
counterexample.

## 5. Why the some-good-line branch survives on Petersen

The independent checker also classifies every possible functional
projection \(h=\mu\circ f\), hence every one of the 64 binary cycles of
Petersen.  The exact two-cycle normal form is feasible for 57 of them.
The seven failures are the zero cycle and the six 10-edge complements
of the six perfect matchings listed above.

The six nonzero bad projections have binary rank five; their XOR is zero
and every proper subset is independent.  A nowhere-zero
\(\mathbb F_2^3\)-flow on Petersen cannot have its values in a
two-dimensional subspace, since that would be a Tait coloring.
Therefore its seven nonzero functional projections are the seven
nonzero vectors of a three-dimensional subspace of the cycle space.
Such a subspace contains at most three of the six independent-up-to-their-
total-sum bad projections.  Consequently every Petersen Fano flow has
at least four cleanable lines.

This explains structurally why the fixed-line countermodel does not
threaten the surviving some-good-line route.

## 6. AI-use disclosure

OpenAI Codex agents discovered the order-14 precursor, found its
Petersen reduction, derived the two-cycle normal form and exhaustive
defect table, wrote the CNF/checkers, and drafted this proof under human
direction.  The calculations are supplied for independent checking.
No claim here has been independently peer reviewed by a human.
