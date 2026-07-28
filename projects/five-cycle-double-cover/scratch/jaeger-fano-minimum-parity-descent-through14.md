# Symmetric Fano-minimum parity descent through order 14

Date: 2026-07-28

Status: **EXACT FINITE THEOREM FOR SIMPLE 3-EDGE-CONNECTED CUBIC GRAPHS
THROUGH 14 VERTICES / NOT A UNIVERSAL PROOF / NOT A RESOLUTION OF
FIVECDC.**

## 1. Symmetric defect

Let a vertex-star tree packing produce the nowhere-zero flow
\[
 \phi=(1_{F_0},1_{F_1},1_{F_2}):E(G)\longrightarrow
 \mathbb F_2^3-\{0\}.
\]
For each nonzero functional \(h\in(\mathbb F_2^3)^*\), let
\[
 E_h=\{e:h(\phi(e))=0\}.
\]
At every cubic vertex, \(E_h\) has degree one or three.  If \(Q\) is a
component of \(E_h\), the five-point support criterion assigns it a
well-defined leaf-parity defect \(\omega_h(Q)\in\mathbb F_2\).  Put
\[
 d_h(\phi)=\#\{Q:\omega_h(Q)=1\},\qquad
 d_{\min}(\phi)=\min_{h\ne0}d_h(\phi).                 \tag{1}
\]
Thus \(d_{\min}=0\) exactly when at least one of the seven Fano planes
passes the component criterion, which is exactly the support-five target
for this flow.

The earlier fixed-coordinate trapped state in
`jaeger-star-parity-descent-countermodel.md` does not obstruct (1).  Its
seven-plane profile is
\[
                         (2,4,2,2,0,6,2),
\]
so it already has \(d_{\min}=0\).

## 2. Finite theorem

> **Theorem 2.1 (exhaustive, through order 14).**
> Let \(G\) be a simple 3-edge-connected cubic graph with
> \(|V(G)|\leq14\), let \(r\in V(G)\), and fix any assignment of the three
> edges at \(r\) to the three trees in a vertex-star fibre.  In the graph
> whose vertices are all tree packings in that fibre and whose edges are
> reciprocal two-tree symmetric exchanges, every connected component of
> every positive level set \(d_{\min}^{-1}(k)\) has an exchange edge to a
> lower level.

In particular, from every packing in every tested fibre there is a path
to a support-five-good packing along which \(d_{\min}\) never increases.
At each positive level one first follows same-level exchanges to a
component boundary and then takes a strictly descending exchange.

This is a finite exhaustive theorem.  No argument extending it to
arbitrary order is known.

## 3. Exact state model

Delete the root \(r\), leaving a graph \(H\) with
\(3|V(G)|/2-3\) internal edges.  For one fixed spoke assignment, a state
is an ordered partition
\[
                   E(H)=A_0\mathbin{\dot\cup}A_1
                         \mathbin{\dot\cup}A_2                \tag{2}
\]
such that every \(E(H)-A_i\) is a spanning tree of \(H\).  Each \(A_i\)
is therefore a cographic basis.  The corresponding tree of \(G\) is
\[
                 T_i=\{s_i\}\cup(E(H)-A_i).                  \tag{3}
\]
The enumerator examines every partition (2), not a random sample.

For each \(T_i\), it computes the unique all-vertices-odd subgraph
\(K_i=K(T_i)\), using odd rooted-subtree sizes.  The flow value on edge
\(e\) is reconstructed literally as
\[
 \phi(e)=\sum_{i:e\notin K_i}2^i.                             \tag{4}
\]

For every \(h=1,\ldots,7\), the checker then:

1. finds the unique normal \(h_v\) of the incident flow plane at every
   vertex;
2. constructs \(E_h\);
3. chooses any \(w\) with \(h(w)=1\);
4. gives each degree-one vertex the coordinate-free forced bit
   \[
                    \ell_v=(h_v+h)(w);
   \]
5. xors these bits separately in every component of \(E_h\).

The number of components with xor one is \(d_h\).  This is the exact
component criterion, not a proxy for it.

A reciprocal exchange between coordinates \(i,j\) is exactly a swap of
one edge of \(A_i\) with one edge of \(A_j\) for which the two new
complements remain spanning trees.  The checker generates every such
swap.  It joins equal-\(d_{\min}\) neighbours in a disjoint-set
structure and marks every state having a lower-\(d_{\min}\) neighbour.
After all exchanges are generated, a positive component fails precisely
when its disjoint-set root has no marked member.

## 4. Complete census

Canonical graphs were generated with

```sh
/opt/homebrew/bin/geng -Cq -d3 -D3 n
```

and then independently tested for connectivity after deletion of every
set of at most two edges.  One root from every vertex-automorphism orbit
was tested.  This is sound because a graph automorphism transports the
entire state and exchange graphs, while a permutation of the three
spokes only permutes flow coordinates; \(d_{\min}\) is invariant under
all Fano-plane permutations.

| order | 3EC graphs | rooted orbit instances | exact states | failures |
|---:|---:|---:|---:|---:|
| 4  | 1   | 1    | 6           | 0 |
| 6  | 2   | 2    | 84          | 0 |
| 8  | 4   | 8    | 2,304       | 0 |
| 10 | 14  | 44   | 96,720      | 0 |
| 12 | 57  | 329  | 5,994,624   | 0 |
| 14 | 341 | 3,183| 523,056,384 | 0 |
| **total** | **419** | **3,567** | **529,150,122** | **0** |

The largest value of \(d_{\min}\) encountered was \(4\).  Every
positive same-level component had a lower-level boundary.

The frozen row-level census is

```text
output/jaeger-fano-min-descent-through14/census.jsonl
```

with SHA-256

```text
f1d720265cc58a732cf2b58920b8dacc12f36191cecc731949622f5c80f4f2e0
```

### A targeted exact order-16 fibre

The unique vertex-star fibre that refutes the separate kernel-closure
strengthening in the complete order-16 closure search was also checked
exactly for the symmetric descent objective.  It is

```text
graph6 O??CA?_ceOGgH_F?AK@P?
root   13
```

The whole-state enumerator found 953,856 states, maximum
\(d_{\min}=4\), and no positive same-level component without a lower
boundary.  This is one targeted fibre, not a complete order-16 descent
census.

An independently written Python replay freezes a particularly symmetric
state in that fibre.  Its omitted-class masks, in the separately frozen
edge order, are

```text
8413 1725442 363296
```

and its exact profile is

\[
                         (4,4,4,4,4,4,4).
\]

Of the \(3\cdot7\cdot7=147\) candidate reciprocal exchanges, exactly 25
are legal; 22 lower \(d_{\min}\) from four to two and the remaining
three preserve it.  Thus even this all-seven-symmetric state is not a
local obstruction.  Reproduce the independent local calculation with

```sh
python3 scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py
```

The frozen machine-readable row is

```text
output/jaeger-fano-min-descent-order16-closure-no-go/result.json
```

The trust boundary is explicit: the C++ program exhausts all 953,856
states, while the independent Python program reconstructs the literal
graph and explicit state and exhausts all 147 incident exchange
candidates.  It does not independently re-enumerate the whole fibre.

## 5. Reproduction and trust boundary

The exact state/exchange enumerator is

```text
scratch/search_jaeger_star_parity_descent.cpp
```

and accepts `--objective seven`.  The complete runner is

```text
scratch/run_jaeger_fano_min_descent_frontier.py
```

For example:

```sh
python3 scratch/run_jaeger_fano_min_descent_frontier.py \
  --orders 4 6 8 10 12 14 --workers 14 \
  --output output/jaeger-fano-min-descent-through14/census.jsonl
```

The independent coverage verifier regenerates every canonical graph
stream, rechecks 3-edge-connectivity, recomputes every vertex orbit, and
checks the census order, totals, objective, failure flags, and digest:

```sh
python3 scratch/verify_jaeger_fano_min_descent_frontier.py
```

It prints `coverage_verified: true` and `failures: 0`.

SHA-256 of the proof programs:

```text
c087d9de1e8193680f7293543a5d6bd3a3fe95515ca74df6aedc26a852dbe7a5  scratch/search_jaeger_star_parity_descent.cpp
a1966f7d240632eb52ff4bf04c6825a4b213e70bddf5ca76c959a49b0df7f2fc  scratch/run_jaeger_fano_min_descent_frontier.py
d74e4aa788000960954140e9c4b1b2b96c6e4cda025d8e97e2ad9fe7f574fe23  scratch/verify_jaeger_fano_min_descent_frontier.py
8fae5e357ce6e44d59c28d5a07ea28b70320cf3f6ab70c29ce962ad9b76e3593  scratch/verify_jaeger_star_parity_descent_countermodel.py
7a3432cd3574191d7b732f6f62a50263e64868d144196777e684473b5e642c63  scratch/verify_jaeger_fano_min_descent_order16_closure_no_go.py
```

The trust boundary is explicit.  The C++ source is the exhaustive
whole-state proof program.  The Python verifier independently audits
coverage and integrity but does not re-enumerate all 529,150,122 states
in a second implementation.  The coordinate-free seven-plane profile
is independently implemented on the explicit fixed-coordinate
countermodel in
`verify_jaeger_star_parity_descent_countermodel.py`.

## 6. What this does and does not establish

The symmetric minimum survives the first fixed-coordinate obstruction
and every exhaustive test through order 14.  This makes it a materially
stronger exchange potential than a preselected coordinate defect.

It is not yet a proof of the universal monotone-descent statement.
There is no sound reduction saying that a minimal failure must have at
most 14 vertices, and the census covers simple graphs only.  Therefore
this result must not be cited as a proof of FiveCDC.

## AI-use disclosure

OpenAI Codex, under human direction, formulated the symmetric potential,
implemented the exact seven-plane component score and exchange census,
found and corrected the fixed-coordinate overclaim, ran the exhaustive
search, and drafted this note.  The code, canonical inputs, row-level
outputs, hashes, and trust boundary are disclosed for human audit.
