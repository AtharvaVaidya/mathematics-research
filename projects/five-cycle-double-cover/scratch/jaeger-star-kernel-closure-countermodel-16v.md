# A 16-vertex countermodel to the star kernel-closure strengthening

Date: 2026-07-28

Status: **DUAL-CHECKED COUNTEREXAMPLE TO A SUFFICIENT
STRENGTHENING / THE EXACT COMPONENT-PARITY TARGET SURVIVES / NOT A
COUNTEREXAMPLE TO FIVE-CDC**.

## 1. Statement refuted

For a spanning tree \(T\) of an even-order cubic graph, put
\[
 K(T)=\{e\in T:\text{the two components of }T-e\text{ have odd order}\}.
\]
Equivalently, \(K(T)\) is the unique subset of \(T\) having odd degree
at every vertex.

The following attractive strengthening of the surviving Jaeger
star-fibre target is false:

> Given a vertex \(r\) of a 3-edge-connected cubic graph, choose three
> spanning trees \(T_0,T_1,T_2\) in the star fibre
> \(2E(G)-\delta(r)\) and a coordinate \(k\) so that, for
> \(\{i,j,k\}=\{0,1,2\}\),
> \[
>                     K(T_i)\cap K(T_j)
>               \subseteq \operatorname{cl}_G K(T_k).        \tag{1}
> \]

The countermodel is

```text
graph6  O??CA?_ceOGgH_F?AK@P?
root    13
```

in the following edge order:

```text
 0 0-6    1 0-9    2 0-10   3 1-7    4 1-10   5 1-11
 6 2-8    7 2-12   8 2-15   9 3-9   10 3-13  11 3-14
12 4-10  13 4-13  14 4-15  15 5-11  16 5-12  17 5-13
18 6-9   19 6-12  20 7-11  21 7-14  22 8-14  23 8-15
```

Thus \(\delta(13)=\{10,13,17\}\).  Direct checks show that the graph is
simple, cubic, 3-edge-connected, and 3-vertex-connected.  It is
nonplanar, nonbipartite, and has girth three.

## 2. Why the cographic reformulation is exact

Let \(H=G-r\).  In every star-fibre packing each tree contains exactly
one root spoke, because each tree must meet \(r\) and the three spokes
have total multiplicity three.  Hence
\[
 B_i=T_i-r
\]
is a spanning tree of \(H\).  Every edge of \(H\) occurs in exactly two
of the \(B_i\), so
\[
 A_i=E(H)-B_i
\]
partition \(E(H)\).  Each \(A_i\) is a basis of the cographic matroid
\(M^*(H)\).  Conversely, a partition of \(E(H)\) into three cographic
bases, together with a bijection from the three root spokes to the
three coordinates, reconstructs one and only one ordered star
packing.

For this graph, \(H\) has 15 vertices and 21 edges.  Its cographic
matroid has rank seven.  The independent exhaustive counter

```sh
clang++ -O3 -std=c++20 \
  scratch/count_jaeger_star_kernel_closure_countermodel_16v.cpp \
  -o /tmp/count_star_kernel_closure_16v
/tmp/count_star_kernel_closure_16v
```

enumerates all seven-subsets \(A\) for which \(H-A\) is a tree, all
partitions into three such subsets, and all spoke bijections.  Its
exact totals are

```text
cographic bases                         16,200
unordered partitions into three bases 158,976
ordered star packings                5,723,136
packings satisfying (1)                      0
packings satisfying exact parity        40,464
```

The complete histogram
\[
\begin{array}{c|r}
(\text{number of closure-good coordinates},
 \text{number of parity-good coordinates})&\text{packings}\\ \hline
(0,0)&5,682,672\\
(0,1)&   40,464
\end{array}
\]
is especially informative: closure fails in every coordinate of every
packing, while the exact target has many witnesses.

This cographic reformulation is therefore useful as an exact
enumeration and optimization language, but it does **not** yield the
proposed universal closure theorem.

## 3. Certificate-producing CNF

The independently written CNF generator uses four variable families:

* \(t_{e,i}\): edge \(e\) is in coordinate tree \(i\);
* \(k_{e,i}\): edge \(e\) is in its odd forest \(K_i\);
* \(z_e\): \(e\in K_0\cap K_1\);
* \(y_{e,f}\): edge \(f\) lies in a conditional \(K_2\)-path joining
  the endpoints of \(e\).

The star edges have exact multiplicity one and all other edges exact
multiplicity two.  For each coordinate and every nonempty vertex set
not containing vertex zero, one cut clause requires a selected edge to
leave the set.  Thus every coordinate is connected.  The fixed total
multiplicity is
\[
 3+2\cdot21=45=3(16-1).
\]
Three connected spanning subgraphs use at least \(3(16-1)\) edges in
total, so equality forces all three to be spanning trees.  This avoids
any opaque acyclicity gadget.

The clauses \(k_{e,i}\Rightarrow t_{e,i}\), together with odd incidence
parity at every vertex, define the unique \(K(T_i)\).  Finally,
\(z_e\leftrightarrow(k_{e,0}\wedge k_{e,1})\), and the \(y\)-row has
boundary \(z_e(\partial e)\) while being contained in \(K_2\).  Since
\(K_2\) is a forest, such a row exists exactly when the endpoints of
every \(z_e\)-edge lie in one \(K_2\)-component.  Permuting tree
coordinates shows that singling out coordinate two loses no candidate
for (1).

The resulting formula has 744 variables and 101,037 clauses:

```text
CNF SHA-256
ccd8ef9504ef725dc02be9234992cbc9e238f1c12ed39ad3068645c73e3c5baf

LRAT SHA-256
ffcd95bc48db7c5be222e05b86aa72cf0828ef01e45e7cf45e9a92cab76aa3a5
```

The LRAT proof is accepted independently by both `lrat-check` and the
verified CakeML checker `cake_lpr`.  Reproduce everything with

```sh
python3 scratch/certify_jaeger_star_kernel_closure_countermodel_16v.py \
  --cnf output/jaeger-star-kernel-closure-countermodel-16v/star-kernel-closure.cnf
python3 scratch/verify_jaeger_star_kernel_closure_countermodel_16v.py
```

## 4. A human-checkable exact-parity witness

The same star fibre has the following ordered packing:

```text
T0 = 0 2 3 8 11 12 13 14 15 16 18 19 20 21 23
T1 = 0 1 2 3 4 5 6 7 8 9 12 16 17 19 22
T2 = 1 4 5 6 7 9 10 11 14 15 18 20 21 22 23

K0 = 0 3 8 11 12 13 14 15 18 19 23
K1 = 2 3 4 5 8 9 12 17 19 22
K2 = 1 4 7 9 10 11 14 15 18 21 22
```

The edge multiplicities are visibly one on \(10,13,17\) and two
elsewhere.  Each displayed \(T_i\) has 15 edges and is connected.
Deleting a displayed \(K_i\)-edge from its tree leaves odd sides; the
equivalent, quicker check is that \(K_i\subseteq T_i\) has odd degree
at every vertex.

For coordinate two,
\[
                    K_0\cap K_1=\{3,8,12,19\}.                \tag{2}
\]
The components of \(K_2\) are
\[
\begin{split}
&\{0,3,6,7,8,9,13,14\},\quad \{1,10\},\quad \{2,12\},\\
&\{4,15\},\quad \{5,11\}.
\end{split}
\]
After contraction, the four edges in (2) form a four-cycle on four of
these components.  They are therefore Eulerian in the quotient, which
is the exact component-parity condition.  None of the four is a loop,
which illustrates precisely why (1) is too strong.

For a direct five-point lift, in edge order \(0,\ldots,23\), use

```text
06 56 05 04 45 05 07 47 04 45 56 46
04 06 46 57 07 05 46 04 07 47 67 06
```

as the pairs of Fano points.  Only the five points
\(\{0,4,5,6,7\}\) occur.  The xor of each pair is the corresponding
fundamental-completion flow value, and at every vertex each point
occurs an even number of times.  These are 24 short local checks,
performed independently by the verifier.

## 5. Consequence and boundary

In the binary graphic matroid with the parity column \(p\), one indeed
has
\[
                         C(p,T)=K(T)\cup\{p\}.
\]
The countermodel proves that binary circuit elimination, basis
partition, and cographic exchange alone cannot force
\[
 (C(p,T_i)-p)\cap(C(p,T_j)-p)
       \subseteq\operatorname{cl}(C(p,T_k)-p)
\]
even with the full simple-cubic, 3-connected, vertex-star hypotheses.
Any proof of the surviving Jaeger lemma must use the weaker fact that
the crossing edges have **even boundary** after contraction, not that
there are no crossing edges.

No Five-CDC counterexample is obtained.  On the contrary, the explicit
five-point labelling above certifies that this very fibre meets the
exact target.

## AI-use disclosure

OpenAI Codex, under human direction, found the countermodel in an exact
SAT census, derived the cographic base-partition audit, wrote the two
independent encodings/checkers, generated and checked the LRAT
certificate, and drafted this note.  The result refutes only the stated
sufficient strengthening.  It does not resolve Five-CDC.
