# Two-pivot odd-kernel identity and a neutral-memory counterstate

Status: **PROVED AUXILIARY LEMMA + EXACT FINITE COUNTERSTATE**, 2026-07-29.
This is not a proof or disproof of FiveCDC.

## 1. Single-pivot identity

Let `T` be a spanning tree of a connected graph of even order. Write
`K(T)` for the unique subset of `T` having odd degree at every vertex.
Let `e` be outside `T`, let `C=C_T(e)` be its fundamental circuit, and
let `f` be a tree edge of `C`. Then `T'=T+e-f` is a spanning tree and

```text
K(T') = K(T)                         if f is not in K(T),
K(T') = K(T) symmetric_difference C  if f is in K(T).
```

In the active second case,

```text
|K(T')|-|K(T)| = |C|-2|C intersection K(T)|.
```

Proof. Any two all-odd edge sets have even-degree symmetric difference.
If `f` is not in `K(T)`, then `K(T)` is already a subset of `T'` and
uniqueness on a tree gives the first equality. If `f` is in `K(T)`,
then `K(T) symmetric_difference C` has odd degree everywhere, removes
`f`, adds `e`, and is a subset of `T'`; uniqueness gives the second
equality. The size formula is the elementary size formula for symmetric
difference.

## 2. Two-pivot identity

Suppose the first pivot is `T'=T+e-f`. Let `g` be another edge outside
both `T` and `T'`, with all four named edges distinct, and put
`E=C_T(g)`. Define

```text
alpha = 1 if f is in E, otherwise 0.
```

Then the fundamental circuit of `g` after the first pivot is

```text
C_T'(g) = E symmetric_difference (alpha times C).
```

Here multiplication by zero means the empty set. Indeed, if `f` is not
in `E`, the old circuit survives in `T'+g`. If `f` is in `E`, the
symmetric difference `E symmetric_difference C` is the unique circuit
in `T'+g`: the two occurrences of `f` cancel and the new tree edge `e`
appears.

Let

```text
a = 1 if f is in K(T), otherwise 0,
b = 1 if h is in K(T'), otherwise 0,
```

where the second pivot removes `h` from `C_T'(g)`. Applying the
single-pivot identity twice gives the exact formula

```text
K(T+e+g-f-h)
  = K(T)
    symmetric_difference (b times E)
    symmetric_difference ((a xor (alpha and b)) times C).
```

This is the required interaction term. Even when the first pivot is
kernel-neutral (`a=0`), it changes the second update whenever
`alpha=b=1`.

For two reciprocal exchanges of a rooted three-tree state, apply this
identity separately to each affected tree. A coordinate touched only
once uses the single-pivot identity; a coordinate touched twice uses the
two-pivot identity. Summing the three resulting cardinalities gives the
endpoint kernel sum exactly.

## 3. Consequence for the Fano flow and span defects

Let the three tree kernels change from `K_i` to `K_i'` and put
`D_i=K_i symmetric_difference K_i'`. The associated nowhere-zero
`F_2^3` flow is defined by

```text
F(e)_i = 1 if and only if e is not in K_i.
```

Therefore the endpoint flow is controlled exactly by

```text
F'(e) = F(e) + (1[e in D_0],1[e in D_1],1[e in D_2]).
```

For a nonzero functional `q`, membership of an edge in the `q`-zero
subgraph changes exactly when

```text
q dot (1[e in D_0],1[e in D_1],1[e in D_2]) = 1.
```

This gives a useful fixed-topology special case. If the last scalar is
zero on every edge, the `q`-zero and complementary component partitions
are unchanged. If, in addition,

1. at every degree-one vertex of the `q`-zero subgraph, the chosen
   transverse bit of the vertex normal is unchanged; and
2. for each of the three nonzero directions in `ker(q)`, equality of the
   unique incident `q`-zero edge value to that direction is unchanged,

then the component demand vector, every parallel span matrix, the
`q`-profile entry, and all three `q`-parallel success flags are unchanged.

Proof. Under the first condition the two component partitions and their
degree-one vertices are identical. The component demand vector is the
parity sum of the stated transverse normal bits, so hypothesis 1 fixes
it. Each column of each parallel span matrix is the parity sum of
zero-component basis vectors at the eligible degree-one vertices inside
one complementary component; hypothesis 2 fixes eligibility. Thus the
matrices, their spans, and their membership answers are identical.

The hypotheses are intentionally explicit. Fixed component topology
alone does not imply fixed defects.

## 4. Hušek--Šámal component-parity form

Hušek and Šámal, *Exponentially Many Circuit Double Covers*,
[arXiv:2607.24724](https://arxiv.org/abs/2607.24724), Theorem 3.16,
give the exact flow criterion relevant to FiveCDC. For a nowhere-zero
`F_2^3` flow `phi`, define

```text
Q = {e : first bit of phi(e) is 1},
M = {e : phi(e) = 100},
Z = the endpoints of M.
```

Their theorem says that the five-label system for `phi` is solvable if
and only if every component of `G-Q` contains an even number of vertices
of `Z` (equivalently, `G-Q` contains a `Z`-join).

Here is an exact fixed-`Q` update rule. Let `phi'` be another nowhere-zero
flow whose first bit agrees with `phi` on every edge, and define `M'` and
`Z'` analogously. Then `Q'=Q`, so the components of `G-Q` are unchanged.
For every such component `H`,

```text
|Z' intersection V(H)| + |Z intersection V(H)|
  = |cut(H) intersection (M symmetric_difference M')|  (mod 2).
```

Proof. Both `M` and `M'` are matchings, since two incident `100` edges
would force a zero value on the third edge. Hence
`Z symmetric_difference Z'` is precisely the odd-degree boundary of
`M symmetric_difference M'`. The handshaking identity inside `H` says
that the number of these odd-degree vertices in `H` has the parity of
the edges of that symmetric difference crossing the cut of `H`.

Consequently, while `Q` is fixed, the Hušek--Šámal component-parity
criterion is preserved if and only if every component cut meets
`M symmetric_difference M'` evenly. Under the tree-kernel flow update
above, `Q` is fixed exactly when the kernel toggle in the selected first
coordinate is empty. This is a nontrivial special case in which the
effect of disjoint pivots on the FiveCDC criterion is completely
controlled.

## 5. Exact counterstate to naive additivity

The graph is the frozen 130-vertex girth-10 lift, rooted at vertex 65.
Take seed 211, trap-directed step 81 from the aggregate portfolio. The
two disjoint exchanges, both between coordinates 0 and 1, are

```text
first:  local positions (65,96), full graph6 edges (66,97)
second: local positions (64,63), full graph6 edges (64,63)
```

The exact states are:

| state | kernel sizes | profile | flags | full `Psi` |
|---|---|---|---:|---:|
| start | `(70,70,66)` | `(22,20,18,26,12,16,2)` | 0 | `(2,206)` |
| first only | `(70,70,66)` | same as start | 0 | `(2,206)` |
| second only | `(67,70,66)` | `(24,18,12,20,14,12,4)` | 0 | `(4,203)` |
| both | `(69,70,66)` | `(24,20,16,22,12,14,2)` | 0 | `(2,205)` |

Thus the first exchange is completely invisible to the kernels and Fano
flow. The second exchange is legal at the start but moves *up* in the
lexicographic objective. After the neutral first exchange, the same
disjoint second exchange moves below the start.

On tree coordinate 0, the second exchange's active fundamental circuit
has:

```text
at the start:       length 35, kernel intersection 19, size change -3
after the first:    length 25, kernel intersection 13, size change -1
```

The coordinate-1 side of the second exchange is inactive in both states.
The first exchange is inactive on both of its sides, so its kernels
really are unchanged.

This counterstate refutes any uncrossing rule that treats a
kernel-neutral exchange as forgettable, or that predicts a two-exchange
endpoint solely from the current three kernels/Fano flow and the two
edge pairs. The spanning-tree basis and its fundamental-circuit geometry
must remain part of the invariant.

## 6. Radius two is not universal

The separate exact package
`../jaeger-order40-augmented-radius-two-counterexample-20260729/`
contains an order-40 state with no lower-`Psi` or successful state through
distance two and an escape at exact distance three. Its three swaps use
six distinct local edges and coordinate pairs `(01,01,02)`. Thus the
194/196 disjoint two-step pattern that motivated this note does not yield
a universal radius-two theorem: even three disjoint pivots may be
necessary.

More strongly, all eight subsets of these three commuting label swaps
are legal states. Write the swaps as `A=(10,9)`, `B=(40,43)`, and
`C=(15,17)`. Their exact cube is:

| subset | kernel sizes | profile | flags | `Psi` |
|---|---|---|---:|---:|
| none | `(20,20,20)` | `(4,6,2,6,6,6,2)` | 0 | `(2,60)` |
| A | `(20,20,20)` | `(4,6,2,6,6,6,2)` | 0 | `(2,60)` |
| B | `(22,20,20)` | `(4,6,4,6,2,6,2)` | 0 | `(2,62)` |
| AB | `(20,20,20)` | `(4,6,4,6,2,4,2)` | 0 | `(2,60)` |
| C | `(20,20,21)` | `(6,6,4,8,6,4,2)` | 0 | `(2,61)` |
| AC | `(20,20,21)` | `(6,6,4,8,6,4,2)` | 0 | `(2,61)` |
| BC | `(22,20,21)` | `(6,10,6,6,4,6,2)` | 0 | `(2,63)` |
| ABC | `(20,20,21)` | `(6,6,6,6,4,4,0)` | 3 | `(0,61)` |

No proper subset is lower or successful; the full triple is. So the
disjoint-exchange pattern does not disappear—it exhibits a genuine
three-way interaction that cannot be certified by checking single
pivots and pairs alone.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the identities, found
the finite counterstate in a frozen exact portfolio, wrote the checker,
and drafted this note. No independent human peer review has occurred.
