# Odd-side forests in a Jaeger star fibre

Date: 2026-07-28

Status: **HUMAN ALGEBRAIC IDENTITIES / EXACT PETERSEN OBSTRUCTION TO
DISJOINTNESS / NOT A PROOF OF THE PARITY-SELECTION LEMMA**.

## 1. The odd-side forest is the zero set

Let \(G\) be a cubic graph of even order, let \(T\) be a spanning tree,
and define
\[
 K(T)=\{e\in T:\text{a component of }T-e\text{ has odd order}\}.
\]
Both components have the same parity, so this is well defined.

Let \(F(T)\) be the fundamental completion: the xor of the fundamental
circuits of all edges outside \(T\).  If \(e\in T\), and \(X\) is one
side of \(T-e\), then
\[
 e\in F(T)
 \quad\Longleftrightarrow\quad
 |\delta_G(X)-\{e\}|\text{ is odd}.
\]
Since \(G\) is cubic,
\[
 |\delta_G(X)|\equiv 3|X|\equiv |X|\pmod2.
\]
It follows that \(e\in F(T)\) exactly when \(|X|\) is even.  Every
cotree edge belongs to \(F(T)\), and therefore
\[
                         F(T)=E(G)-K(T).                       \tag{1}
\]

In particular, \(K(T)\) is a forest and every vertex has odd degree in
\(K(T)\): the complement of an Eulerian subgraph in a cubic graph has
odd degree at every vertex.  Equivalently,
\[
                         \partial K(T)=V(G).                   \tag{2}
\]
Thus every component of \(K(T)\) has even order.

There is also a rooted description.  Root \(T\) arbitrarily.  A
nonroot edge belongs to \(K(T)\) exactly when the subtree below it has
odd order.  The usual leaf recursion then gives (2) directly.

## 2. The star-fibre parity target

Take a vertex-star multiplicity fibre and number the three incident
edges so that the \(i\)-th spoke belongs only to \(T_i\).  Put
\[
 K_i=K(T_i),\qquad F_i=E(G)-K_i,
\]
and let \(\phi=(1_{F_1},1_{F_2},1_{F_3})\).  Empty common intersection
of the three trees implies
\[
                         K_1\cap K_2\cap K_3=\varnothing.       \tag{3}
\]
Consequently the pure third-coordinate value class is exactly
\[
 \{e:\phi(e)=001\}=K_1\cap K_2.                               \tag{4}
\]

For the coordinate plane \(\ker(x_3)\), the five-point
component-parity criterion therefore says precisely:
\[
 |\delta_G(Q)\cap K_1\cap K_2|\equiv0\pmod2
 \quad\text{for every component }Q\text{ of }K_3.             \tag{5}
\]
Equivalently, \(K_1\cap K_2\) is Eulerian after every component of
\(K_3\) is contracted.

Some parity is automatic but not enough.  By (2), for every component
\(Q\) of \(K_3\),
\[
 |\delta_G(Q)\cap K_1|
 \equiv|\delta_G(Q)\cap K_2|
 \equiv |Q|\equiv0\pmod2.                                    \tag{6}
\]
The parity of the intersection of those two even sets is not
determined.  If
\[
 \omega_3(Q)=|\delta_G(Q)\cap K_1\cap K_2|\pmod2,
\]
then
\[
                  \bigoplus_Q\omega_3(Q)=0,                   \tag{7}
\]
because every edge between distinct contracted components is counted
at both ends.  Thus the failing components always occur in pairs.
The missing theorem must eliminate these paired local defects; their
global parity already vanishes.

## 3. Exact exchange law

Make a tree exchange
\[
 T'=T-a+b,\qquad a\in C_T(b),
\]
where \(C_T(b)\) is the fundamental circuit of \(b\).  The fundamental
completion exchange identity and (1) give
\[
 K(T')=
 \begin{cases}
 K(T),&a\notin K(T),\\
 K(T)\mathbin\triangle C_T(b),&a\in K(T).
 \end{cases}                                                   \tag{8}
\]
Thus an exchange removing an edge outside the odd-side forest is
completion-neutral.  An active exchange toggles one whole fundamental
circuit.  Since a circuit is Eulerian, (8) also directly preserves the
boundary identity (2).

Suppose \(K_3\) is fixed and exchanges in the first two trees give
\[
 K_1'=K_1\triangle\alpha C_1,\qquad
 K_2'=K_2\triangle\beta C_2,
\]
where \(\alpha,\beta\in\{0,1\}\) record whether the corresponding
removed edge lies in its old \(K\)-forest.  For edge-indicator
functions over \(\mathbb F_2\),
\[
\begin{split}
 1_{K_1'\cap K_2'}
  ={}&1_{K_1\cap K_2}
   +\alpha\,1_{C_1\cap K_2}
   +\beta\,1_{C_2\cap K_1}\\
   &+\alpha\beta\,1_{C_1\cap C_2}.                             \tag{9}
\end{split}
\]
Taking boundaries after contracting \(K_3\) gives the exact update of
the defect vector \(\omega_3\).  Formula (9) exposes the difficulty:
the target is bilinear in the two odd-side forests, so ordinary linear
boundary invariance does not force (5).

## 4. A rigorous obstruction to the disjointness strengthening

A tempting strengthening of (5) is to seek a packing with
\[
                         K_i\cap K_j=\varnothing               \tag{10}
\]
for some two coordinates.  This is false already in the Petersen
graph, independently of the chosen star or packing.

Indeed, let \(K,L\) be two edge-disjoint spanning subgraphs of a cubic
graph such that every vertex has odd degree in each.  At a vertex,
\[
 \deg_K(v)+\deg_L(v)\leq3
\]
and both summands are positive and odd.  Hence both are one.  Therefore
\(K\) and \(L\) are disjoint perfect matchings, and \(K\cup L\) is a
2-factor whose cycles alternate between the two matchings.  Every one
of those cycles is even.

The Petersen graph has no even 2-factor.  In its standard outer-cycle,
inner-star presentation, a perfect matching uses an odd number of
spokes.  Three spokes are impossible: the two unmatched outer indices
would have to differ by one modulo five, while the same two inner
indices would have to differ by two.  With one or five spokes, the
complement is directly two 5-cycles.  Hence every 2-factor of Petersen
is two odd 5-cycles.

By (2), every \(K(T_i)\) is an all-vertex odd subgraph.  The preceding
argument proves
\[
                  K(T_i)\cap K(T_j)\ne\varnothing
                  \quad\text{for every }i\ne j                 \tag{11}
\]
for every triple of Petersen spanning trees, including every
vertex-star packing.  Thus no proof of (5) can work by forcing the pure
coordinate class (4) to be empty.

The independent exhaustive checker enumerates every star packing.  For
each of the ten choices of the star it finds 4,416 ordered packings;
none has a disjoint pair of \(K\)-forests.  Nevertheless 384 packings
have at least one coordinate satisfying (5), confirming that the exact
contracted-Eulerian target survives while the disjointness
strengthening fails:

```sh
python3 scratch/verify_jaeger_k_forest_petersen.py
```

## What remains

Equations (5), (8), and (9) reduce the star-fibre support-five problem
to cancelling an even set of component defects by legal reciprocal
tree exchanges.  No argument proving that cancellation exists in every
3-edge-connected cubic graph is obtained here.  The Petersen
obstruction shows that nonemptiness of the pure coordinate class is not
itself a defect; only its boundary in the contracted \(K_i\)-quotient
matters.

## AI-use disclosure

OpenAI Codex, under human direction, derived the identities, found the
Petersen obstruction, implemented the exhaustive checker, and drafted
this note.  The universal component-parity selection lemma remains
unproved, and no resolution of FiveCDC is claimed.
