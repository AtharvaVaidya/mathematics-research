# The parity-element extension and a sharp kernel-closure no-go

Date: 2026-07-28

Status: **HUMAN LINEAR-ALGEBRA REFORMULATION / EXACT EXHAUSTIVE
COUNTERMODEL TO A STRONGER SELECTION LEMMA / STAR CASE STILL OPEN / NOT A
PROOF OF FIVEDC**.

## 1. Odd kernels are fundamental circuits of one parity element

Let \(G=(V,E)\) be a connected loopless graph of even order \(n\), fix a
root \(\rho\), and let

\[
 A\in\mathbb F_2^{(n-1)\times E}
\]

be the vertex-edge incidence matrix with the row of \(\rho\) deleted.
The column matroid of \(A\) is the graphic matroid \(M(G)\).  Put

\[
                         p=\mathbf 1\in\mathbb F_2^{n-1}
\]

and let \(\widetilde M\) be the binary single-element extension
represented by \([A\mid p]\).

If \(T\) is a spanning tree, then \(A_T\) is invertible.  Let
\(z_T=A_T^{-1}p\).  The full incidence boundary of the edge set
\(\operatorname{supp}(z_T)\) is all of \(V\): the nonroot equations say
this directly, and the root equation follows because \(n\) is even.
There is a unique all-vertices-odd subset of a tree, so

\[
 \operatorname{supp}(z_T)=K(T),
\]

where \(K(T)\) is the odd-side forest.  Equivalently,

\[
                C_{\widetilde M}(T,p)=K(T)\cup\{p\}.          \tag{1}
\]

This is literally the fundamental circuit of \(p\) with respect to the
basis \(T\).  The dependence

\[
                         p=\sum_{e\in K(T)}A_e
\]

is unique because \(A_T\) is a basis, and its nonzero support is
therefore a circuit.

Cramer's rule gives a determinant version:

\[
 1_{e\in K(T)}
   =\det A_{T-e+p}\pmod 2,                                   \tag{2}
\]

where the notation means that the column \(e\) of the tree basis is
replaced by \(p\).  Thus every odd-kernel membership bit is a maximal
minor over \(\mathbb F_2\), not an additional nonlinear graph
primitive.

Parallel graph edges cause no problem: they are represented by equal
columns and remain distinct parallel matroid elements.  A graph loop is
a zero column and never belongs to a tree or to \(K(T)\).  The present
search and countermodel are simple and loopless.

## 2. What is special about a vertex-star fibre

Let \(G\) now be cubic and 3-edge-connected, choose a vertex \(r\), and
put \(D=\delta(r)\).  The star fibre has one copy of each edge of \(D\)
and two copies of every edge outside \(D\).  Its total size is
\(3(n-1)\), and a fibre packing is a partition of these copies into
three graphic bases \(T_1,T_2,T_3\).

Every tree crosses \(D\), while there are only three copies in \(D\).
Consequently each \(T_i\) contains exactly one member of \(D\).
Moreover, every \(K(T_i)\) contains that member: at \(r\), the tree has
degree one and the odd kernel has odd degree.

The parity-element extension records the same fact abstractly.  Sum all
nonroot rows of \([A\mid p]\).  On an original graph column this
functional is one exactly on \(D\), and on \(p\) it is
\(n-1=1\pmod2\).  Hence

\[
                         D\cup\{p\}
\]

is a cocycle of \(\widetilde M\).  Binary circuit-cocircuit
orthogonality applied to (1) says that \(|K(T_i)\cap D|\) is odd; the
base-packing count then makes it exactly one.

This distinguished four-element cocycle, together with the parallel
pairs outside \(D\), is genuine extra structure.  A generic Type-A
fibre merely has three multiplicity-one edges; they need not form a
vertex cut.  The no-go below shows that this distinction matters.

### Root deletion gives three cographic bases

There is a second exact form of the star structure.  Delete \(r\) and
its three spokes, and write \(H=G-r\).  In every star-fibre packing,
\(r\) has degree one in each \(T_i\).  If the spoke in \(T_i\) is
\(ru_i\), then

\[
                         S_i=T_i-r
\]

is a spanning tree of \(H\).  Every edge of \(H\) occurs in exactly two
of the \(S_i\), so the three complements

\[
                         R_i=E(H)-S_i
\]

partition \(E(H)\).  Conversely, a partition of \(E(H)\) into three
bases \(R_i\) of the cographic matroid \(M^*(H)\), together with a
bijection between the \(R_i\) and the three neighbours \(u_i\) of \(r\),
reconstructs a star-fibre packing by

\[
                         T_i=S_i+ru_i.
\]

Thus star-fibre packings are exactly three-base partitions of one
cographic matroid, plus a three-way terminal assignment.

Let \(J_i=K(T_i)-ru_i\).  Inside the tree \(S_i\), it is the unique join
with boundary

\[
                         \partial_H J_i=V(H)-\{u_i\}.          \tag{3}
\]

Indeed, every vertex other than \(u_i\) must have odd \(J_i\)-degree,
while the root spoke supplies the required odd degree at \(u_i\).
Adding the leaf \(r\) does not change connectivity between vertices of
\(H\), so the star closure target is equivalently

\[
                 J_j\cap J_k\subseteq
                 \operatorname{cl}_{M(H)}(J_i)                \tag{4}
\]

for some coordinate \(i\).

This exposes exactly where a cographic base-partition or exchange
theorem would have to act.  Ordinary equitability of the three bases
\(R_i\) does not directly control the terminal joins (3).

## 3. A tempting closure strengthening

For a packing put \(K_i=K(T_i)\).  The exact coordinate-\(3\)
five-support target is

\[
 |\delta(Q)\cap K_1\cap K_2|=0\pmod2
 \quad\text{for every component \(Q\) of \(K_3\)}.            \tag{5}
\]

A cleaner-looking sufficient condition is

\[
                         K_1\cap K_2
                 \subseteq \operatorname{cl}_{M(G)}(K_3).    \tag{6}
\]

Because \(K_3\) is a forest, an edge belongs to its graphic closure
exactly when its endpoints lie in one \(K_3\)-component.  Thus (6)
makes every \(K_1\cap K_2\) edge a loop after contraction, and it
immediately implies (5).

In the parity-element coordinates, if \(a_e\) is the incidence column
of an edge not in \(T_3\), then

\[
 e\in\operatorname{cl}(K_3)
 \quad\Longleftrightarrow\quad
 \operatorname{supp}(A_{T_3}^{-1}a_e)
       \subseteq\operatorname{supp}(A_{T_3}^{-1}p).           \tag{7}
\]

The left support is the \(T_3\)-path joining the endpoints of \(e\);
the right support is \(K_3\).  Formula (7) is a determinant/linear
algebra version of kernel closure.

The universal assertion “every feasible Type-A/B fibre has a packing
and a coordinate satisfying (6)” is false.

## 4. The 12-vertex countermodel

The canonical graph6 record is

```text
K?`@E`gFCKEO
```

with labelled edges

```text
 0:(0,4)   1:(1,5)   2:(2,6)   3:(0,7)   4:(1,7)   5:(3,7)
 6:(1,8)   7:(2,8)   8:(4,8)   9:(3,9)  10:(4,9)  11:(5,9)
12:(0,10) 13:(5,10) 14:(6,10) 15:(2,11) 16:(3,11) 17:(6,11).
```

It is simple, cubic, and remains connected after deletion of any one or
two edges.

The edges

```text
0,10,11,1,4,3
```

form the six-cycle

\[
0-4-9-5-1-7-0.
\]

Give multiplicity one to either alternating matching

\[
 D_0=\{0,4,11\}
 \quad\text{or}\quad
 D_1=\{1,3,10\},
\]

and multiplicity two to every other edge.  The two fibres are
isomorphic under an automorphism of the graph.

For each fibre there are exactly \(355\,392\) ordered spanning-tree
packings.  None satisfies (6) in any of the three coordinates.
Nevertheless exactly \(7\,704\) packings satisfy the actual parity
condition (5), always in exactly one coordinate.  The complete
histogram is

| closure-good coordinates | parity-good coordinates | packings |
|---:|---:|---:|
| 0 | 0 | 347,688 |
| 0 | 1 | 7,704 |

Thus the obstruction is precisely to replacing “even degree in the
quotient” by “every edge becomes a quotient loop.”  It is not an
obstruction to the component-parity lemma.

One literal parity-good packing for \(D_0\) is

```text
T1 = 0 1 2 3 4 5 6 7 10 14 15
T2 = 1 2 5 8 9 10 11 12 13 16 17
T3 = 3 6 7 8 9 12 13 14 15 16 17

K1 = 1 3 4 5 6 10 14 15
K2 = 1 2 5 8 9 12 16
K3 = 3 6 7 8 9 13 17.
```

Direct subtree-size calculation gives the displayed kernels.  This
packing is parity-good in one coordinate and closure-good in none.

## 5. Complete independent enumeration

The standard-library checker

```sh
python3 scratch/verify_jaeger_kernel_closure_typea_countermodel.py
```

does not call or import the SAT producer.  It:

1. decodes the graph6 record and checks the literal edge list;
2. verifies simplicity, cubicity, and connectivity after every
   one- and two-edge deletion;
3. tests all \(\binom{18}{11}=31\,824\) candidate edge sets and finds
   exactly \(8\,640\) spanning trees;
4. computes \(K(T)\) independently by rooted odd-subtree recursion;
5. enumerates every ordered packing in each of the two fibres; and
6. directly tests all three closure and component-parity coordinates.

The enumeration of tree triples has a short completeness formula.  Let
\(D\) be the multiplicity-one set and \(M=E-D\).  Once two tree masks
\(T_1,T_2\) are fixed, the multiplicities force

\[
 T_3=((T_1\mathbin\triangle T_2)\cap M)
       \ \cup\ (D-(T_1\cup T_2)).                            \tag{8}
\]

The checker iterates every ordered pair of the 8,640 trees, applies
(8), and retains it exactly when the forced third set is also a
spanning tree.  Thus no packing is omitted and no SAT assumption enters
the no-go.

## 6. Bounded search boundary

The SAT producer

```text
scratch/search_jaeger_star_kernel_closure_sat.cpp
```

uses conditional \(\mathbb F_2\) path commodities.  If an edge belongs
to \(K_1\cap K_2\), its commodity has boundary equal to the two
endpoints and is constrained to use only \(K_3\).  Since \(K_3\) is a
forest, such a commodity exists exactly when the endpoints are in one
component.  Returned models are separately replayed using disjoint-set
connectivity and independently reconstructed odd kernels.

The frozen Type-A/B witness frontier through order ten is independently
replayed by

```sh
python3 scratch/verify_jaeger_kernel_closure_frontier.py
```

It decodes every graph again, verifies all three spanning trees and
edge multiplicities, recomputes the odd kernels by subtree recursion,
and tests graphic closure without importing the SAT producer.  It
checks 12,695 literal witnesses among 14,757 patterns on the 27
connected simple cubic graphs through order ten.

The bounded results are:

* all 621 connected simple cubic graphs through order 14 were tested in
  every vertex-star fibre; 419 graphs had feasible star fibres, covering
  5,646 rooted instances, and every one satisfied (6);
* all 112 connected simple cubic graphs through order 12 were tested in
  every Type-A/B fibre: 110,127 patterns, 90,203 feasible fibres,
  90,201 closure-good fibres, and precisely the two failures above;
* the 34-vertex strong-snark thinning countermodel passed all 34 star
  fibres; and
* all 31 retained order-44 oddness-four cyclically-four-connected
  snarks passed all 1,364 star fibres; and
* 50 deterministic random simple 3-edge-connected cubic graphs of order
  50 passed all 2,500 star fibres.

These are finite exact checks, not an induction.  The surviving
star-specific statement is:

> In a vertex-star fibre, can the three bases be chosen so that, after
> permuting them, the common parallel classes in the two parity-element
> fundamental circuits lie in the graphic closure of the third circuit
> minus \(p\)?

A proof would imply the exact component-parity target.  No proof is
given here.  The Type-A countermodel shows that any proof must use the
special cocycle \(D\cup\{p\}\); a theorem for arbitrary three-defect
fibres is impossible.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the parity-element
representation, formulated and encoded the kernel-closure strengthening,
found the 12-vertex countermodel, wrote the independent exhaustive
checker, and drafted this note.  The universal star-fibre closure lemma
and the Five-Cycle Double Cover Conjecture remain unproved.  This work
has not received independent human peer review.
