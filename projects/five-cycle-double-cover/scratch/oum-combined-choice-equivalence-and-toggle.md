# Oum combined choice: exact scope, toggle algebra, and the 12-vertex census

Date: 2026-07-28

Status: **EXACT EQUIVALENCE WITH FIVECDC / EXACT AFFINE TOGGLE LAW /
ALL-FLOW 12-VERTEX CENSUS / NOT A FIVECDC RESOLUTION**.

All vector arithmetic below is over
\(W=\mathbb F_2^3\).  Graphs are finite and loopless.  The main
equivalence is for cubic graphs; parallel edges cause no change.

## 1. Pair-labelled eight-covers are exactly Oum \((\phi,t)\) data

An eight-coordinate double-cover labelling is a map
\[
       P:E(G)\longrightarrow\binom W2
\]
such that, for every vertex \(v\) and point \(x\in W\), the number of
edges incident with \(v\) whose label contains \(x\) is even.

At a cubic vertex the three labels necessarily form the edges of a
triangle.  Indeed, write the first two labels as two-subsets \(A,B\).
Even coordinate incidence says that the third is their symmetric
difference \(A\mathbin\triangle B\).  Since it too has size two,
\(|A\cap B|=1\).  Thus for three distinct points \(x,y,z\), the local
labels are
\[
                 \{x,y\},\quad\{x,z\},\quad\{y,z\}.            \tag{1}
\]

Given such a pair labelling, define
\[
 \phi(e)=x+y\quad\text{when }P_e=\{x,y\},\qquad
 t_v=x+y+z\quad\text{for the local triangle (1).}              \tag{2}
\]
The three incident flow values at \(v\) are
\[
                 x+y,\quad x+z,\quad y+z,
\]
which are nonzero and sum to zero.  Hence \(\phi\) is a nowhere-zero
\(W\)-flow.

For the edge labelled \(\{x,y\}\), choose the other incident edge at
\(v\) whose flow value is \(x+z\).  Oum's endpoint formula gives
\[
 \left\{t_v+(x+z),\ t_v+(x+z)+\phi(e)\right\}
   =\{y,x\}.                                                   \tag{3}
\]
The same pair occurs at the other endpoint by definition of the original
edge label.  Thus \(t\) is compatible and Oum reconstructs \(P\).

Conversely, a nowhere-zero flow and compatible potential produce at each
cubic vertex exactly the triangle on
\[
                 t_v+\alpha,\quad t_v+\beta,\quad t_v+\gamma,
\]
where \(\alpha+\beta+\gamma=0\) are the incident flow values.
Consequently Oum's pair labels satisfy coordinate parity.  Equations
(2)--(3) recover \(\phi\) and \(t\) from them: the flow value is the xor
of the pair, and \(t_v\) is the xor of the three local triangle points.

> **Pair-data equivalence.**  On a loopless cubic graph, Oum-compatible
> pairs \((\phi,t)\), with the eight coordinate names fixed, are exactly
> eight-coordinate double-cover pair labellings.

This is stronger than merely saying that Oum's construction supplies
some eight-cover.

## 2. The global packing statement is precisely FiveCDC

Let \(J(\phi,t)\) be the coordinate co-occurrence graph on \(W\).  If
\(\chi(J)\leq5\), properly colour its eight vertices with at most five
colours.  Replace every old pair \(\{x,y\}\) by the pair of its two
different colours.  Parity survives merging, and every graph edge still
has two different labels.  This is a five-cycle double cover.

Conversely, take any five-cycle double cover, allowing empty coordinates.
Label each edge by the two coordinates containing it, inject the at most
five coordinate names into \(W\), and leave the remaining points unused.
This is an eight-coordinate pair labelling.  Section 1 produces a
nowhere-zero flow and compatible potential for which the co-occurrence
graph uses only those five points and is therefore five-colourable.

Hence:

> **Combined-choice equivalence.**  A loopless cubic graph \(G\) has a
> five-cycle double cover if and only if there exist a nowhere-zero
> \(\mathbb F_2^3\)-flow \(\phi\) and a compatible potential \(t\) for
> which
> \[
>                         \chi(J(\phi,t))\leq5.                \tag{4}
> \]

The order-eight \(R_5\) theorem proved separately says
\[
 J\longrightarrow R_5\quad\Longleftrightarrow\quad\chi(J)\leq5
\]
for every graph on the eight coordinate points.  Thus replacing (4) by
\(J(\phi,t)\to R_5\) does not weaken the equivalence.

It follows that the proposed universal choice of \((\phi,t)\) is not an
intermediate lemma: it is FiveCDC itself in pair-label coordinates.  A
combined-choice countermodel would be a genuine FiveCDC counterexample,
not a countermodel to a narrower method.

## 3. The affine solution space for a fixed flow

Fix a connected cubic graph, a nowhere-zero flow \(\phi\), and one
compatible potential \(t\).  If \(t'=t+h\), subtracting the two
compatibility systems gives
\[
             h_u+h_v\in\langle\phi(e)\rangle
             \qquad(e=uv).                                   \tag{5}
\]
Therefore the homogeneous toggle space is
\[
 K_\phi=\left\{h\in W^{V(G)}:
       h_u+h_v\in\langle\phi(e)\rangle\text{ for every }e=uv\right\}.
                                                                    \tag{6}
\]
The full compatible-potential set is the affine space \(t+K_\phi\).
Constant functions \(h_v=a\) form the three-dimensional global
translation subspace.

For each \(h\in K_\phi\), there is a unique scalar
\(\lambda_e\in\mathbb F_2\) such that
\[
                       h_u+h_v=\lambda_e\phi(e).              \tag{7}
\]
Telescoping around a circuit gives
\[
                 \bigoplus_{e\in C}\lambda_e\phi(e)=0
                 \qquad\text{for every circuit }C.            \tag{8}
\]
Conversely, if \(\lambda\in\mathbb F_2^{E(G)}\) satisfies (8), fix a
root \(r\), put \(h_r=0\), and define \(h_v\) as the xor of
\(\lambda_e\phi(e)\) along any \(r\)-\(v\) path.  Condition (8) makes
this path-independent and gives (7).  Thus
\[
 K_\phi/W_{\rm constant}
 \cong
 L_\phi:=
 \left\{\lambda\in\mathbb F_2^{E(G)}:
   \bigoplus_{e\in C}\lambda_e\phi(e)=0\text{ for every circuit }C
 \right\}.                                                     \tag{9}
\]
Equivalently, the \(W\)-valued edge vector
\((\lambda_e\phi(e))_e\) must be a coboundary.  This is the exact
linear/matroidal description of every free potential toggle.

## 4. Exact effect of a toggle on nonco-occurrences

At vertex \(v\), adding \(h_v\) translates the entire local triangle by
\(h_v\).  More explicitly, if
\[
 P_e=x_e+\langle\phi(e)\rangle
\]
is the old unordered pair computed at endpoint \(u\), then
\[
                       P'_e=P_e+h_u.                          \tag{10}
\]
At the other endpoint, (7) changes the translate by either \(0\) or
\(\phi(e)\), which fixes the same unordered pair.

The 28 coordinate pairs split into seven parallel classes.  For
\(d\ne0\), put
\[
 {\cal M}_d=\bigl\{x+\langle d\rangle:x\in W/\langle d\rangle\bigr\}.
\]
This is a perfect matching of four coordinate pairs, and every pair in
\(\binom W2\) belongs to exactly one \({\cal M}_d\).  For
\(E_d=\{e:\phi(e)=d\}\), let
\(\ell_e\in W/\langle d\rangle\) be the old label coset.  Equation (10)
says that under \(h\), the used part of this parallel class is exactly
\[
 \left\{\ell_e+[h_u]:
             e=uv\in E_d\right\}\subseteq W/\langle d\rangle. \tag{11}
\]
The missing pairs in \({\cal M}_d\) are the other quotient points.

For a basis \(h^1,\ldots,h^k\) of the gauged toggle space and parameters
\(\epsilon\in\mathbb F_2^k\), every occurrence in (11) is therefore an
affine map
\[
 \ell_e+\sum_j\epsilon_j[h^j_u]\in W/\langle d\rangle.         \tag{12}
\]
For any proposed missing pair \(q\in{\cal M}_d\), its occurrence event is
a union of affine subspaces
\[
 \bigcup_{e\in E_d}
 \left\{\epsilon:
   \sum_j\epsilon_j[h^j_u]=q-\ell_e\right\}.                   \tag{13}
\]
Inclusion--exclusion in (13) gives an exact averaging formula: every
nonempty intersection has size \(2^{k-r}\), where \(r\) is the rank of
the stacked quotient evaluations.  But no positive universal lower
bound follows.  The rigid example below has \(k=0\), so there is nothing
to average.

On eight named coordinates, success is equivalent to the
nonco-occurrence graph containing one of
\[
            3K_2,\qquad K_3+K_2,\qquad K_4.                   \tag{14}
\]
These are exactly the clique packings in the complement with total
colour-class saving at least three.

## 5. Which flows come from a spanning-tree coordinate?

For a spanning tree \(T\), let
\[
             F(T)=\mathop{\triangle}_{e\notin T}E(C_e),
                                                                    \tag{15}
\]
where \(C_e\) is the fundamental circuit in \(T+e\).  This is the
Eulerian set used in the spanning-tree construction of a
nowhere-zero \(\mathbb F_2^3\)-flow.

It is the unique Eulerian edge set containing every edge outside \(T\).
Indeed, the symmetric difference of two such sets would be an Eulerian
subgraph contained in the tree, hence empty.

Consequently an Eulerian set \(F\) equals \(F(T)\) for some spanning tree
if and only if its zero set \(E(G)\setminus F\) is a forest:

- necessity follows from \(E(G)\setminus F(T)\subseteq T\);
- for sufficiency, extend the zero forest to a spanning tree \(T\).
  Then \(F\) is Eulerian and contains every cotree edge, so uniqueness
  gives \(F=F(T)\).

Thus, after an invertible coordinate change, a flow is of
spanning-tree-coordinate type precisely when the zero sets of three
independent functional projections are forests.  The original
construction begins with three trees having empty common intersection;
the explicit positive and negative triples below satisfy this stronger
literal condition.

## 6. Exact all-flow census on the rigid 12-vertex graph

Consider the connected simple bipartite cubic graph
```text
K??FEaKR@oE_
```
with the ordered edge list frozen in the report.

The standard-library producer enumerates the 128 binary cycles, forms all
nowhere-zero three-coordinate flows, and quotients exactly by
\(\mathrm{GL}(3,2)\).  For every flow orbit it exhausts the compatible
potential affine space after the gauge \(t_0=0\), and tests (14).

The exact census is:

| item | count |
|---|---:|
| \(\mathrm{GL}(3,2)\)-flow orbits | 900 |
| labelled nowhere-zero flows | 150,192 |
| successful flow orbits | 836 |
| fixed-flow obstructed orbits | 64 |
| successful labelled flows | 139,440 |
| fixed-flow obstructed labelled flows | 10,752 |
| gauged labelled flow--potential pairs | 301,056 |
| successful gauged pairs | 280,896 |
| obstructed gauged pairs | 20,160 |

The gauged potential dimensions on the 900 flow orbits are
\[
\begin{array}{c|rrrr}
\dim&0&1&3&5\\ \hline
\text{orbits}&320&528&44&8.
\end{array}
\]
Among successful labelled flow--potential pairs, 270,816 have a
displayed \(3K_2\) packing and the remaining 10,080 require the broader
\(K_3+K_2\) packing.  No case requires \(K_4\) as the first available
type in the checker's fixed order.

For every one of the 900 flow orbits, the forest-zero functionals span
the full dual space.  More sharply, all 64 fixed-flow obstructed orbits
have all seven nonzero functional zero sets forest.  Hence the forest
condition alone does not imply potential compressibility.

### A literal spanning-tree-flow countermodel

Take the fixed flow
```text
1 2 3 4 7 3 5 3 6 5 7 2 5 1 4 6 2 4
```
in edge order.  The report gives three spanning trees for coordinate
bits \(1,2,4\), with edge-index sets
```text
1 2 3 4 7 8 11 14 15 16 17
0 3 4 5 6 8 9 12 13 14 17
0 1 2 5 6 7 9 11 12 13 16
```
Their common intersection is empty.  Direct fundamental-circuit xor
gives coordinate masks
```text
14069 101814 186200
```
which are exactly the three coordinate supports of the displayed flow.

The gauged compatible-potential space has dimension zero, with unique
potential
```text
0 5 5 1 5 6 7 4 7 3 7 2.
```
Its distinct labels are all 15 pairs on coordinates
\(\{0,1,2,3,4,6\}\), so \(J\) contains \(K_6\).  This refutes the
strictly stronger claim

> every particular flow produced from three spanning-tree fundamental
> completions has a compressible compatible potential.

It does not refute the existential choice of the three trees or the
existential choice of \((\phi,t)\).

### The same graph has a successful spanning-tree choice

A Tait flow on the same graph has values
```text
1 2 3 3 1 2 2 1 3 3 2 1 2 1 3 1 3 2.
```
After the invertible coordinate change \(1,2,3\mapsto5,6,3\), its three
coordinate supports are the fundamental completions of the three
displayed tree-index sets
```text
0 1 2 3 5 6 7 8 10 12 17
0 1 4 5 6 7 9 11 12 13 15
2 3 4 8 9 10 11 13 14 15 16.
```
These trees also have empty common intersection.  The zero potential
gives only the three labels \(36,35,56\), so the cover compresses
immediately.  Therefore the existential spanning-tree variant succeeds
on this graph even though 64 fixed-flow orbits fail.

## 7. Reproduction and independent verification

Producer:
```sh
python3 scratch/audit_oum_combined_choice_12v.py
```

Independent verifier:
```sh
python3 scratch/verify_oum_combined_choice_12v.py
```

The verifier regenerates all 900 flow orbits.  It does not use the
producer's Gaussian solver: for every flow it enumerates the \(2^{11}\)
binary choices on a fixed spanning tree, propagates the potential, checks
all cotree equations, reconstructs every edge label, and independently
tests five-colourability.  It also checks both displayed triples of
spanning trees and their coordinate completions.

The 2,071,165-byte report is
[`all-flow-orbits.json`](../output/oum-combined-choice-12v/all-flow-orbits.json).
Its SHA-256 is
```text
41c50f3413262cfb6a382424674edc2e226325f8b444af0f079ad89f5bc8924a
```

## 8. Frozen frontier

The affine toggle space and the parallel-class action (9)--(13) are
exact, but averaging cannot resolve the global statement: some legitimate
spanning-tree flows have no nontrivial gauged toggle and force \(K_6\).
Choosing the flow as well restores exactly the freedom of choosing an
arbitrary eight-coordinate double cover, and forcing (14) is equivalent
to FiveCDC.

Accordingly, the honest next target cannot be “choose arbitrary
\((\phi,t)\).”  It must identify a new property ensuring that among the
many spanning-tree triples at least one has a compressible completion, or
introduce a genuinely new operation beyond selecting Oum pair data.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the equivalence and
toggle description, performed the exhaustive census, found the explicit
positive and negative spanning-tree triples, wrote the producer and
independent verifier, and drafted this note.  The algebra and finite
certificates are included for independent human checking.  This is not
independent peer review and is not claimed as a resolution of FiveCDC.
