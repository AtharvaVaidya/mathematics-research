# The equal-value avoiding-circuit lemma is false

Date: 2026-07-28

## Exact statement tested

Let \(G\) be a simple cyclically \(4\)-edge-connected cubic graph, let
\(\phi:E(G)\to \mathbb F_2^3\setminus\{0\}\) be a nowhere-zero flow, and
write

\[
E_a=\{e:\phi(e)=a\}.
\]

The proposed lemma said that, for distinct nonzero \(s,t\), every set
\(S\subseteq E_s\) of at most three edges lies in one circuit avoiding
\(E_t\). Here a **circuit** means a closed trail, equivalently a nonempty
connected Eulerian edge-subgraph. The statement is false, even when
\(G-E_t\) is connected and \(G\) is a snark.

This is a counterexample to a proposed *proof step*, not a counterexample to
the Five-Cycle Double Cover Conjecture.

## An 18-vertex snark witness

Use the graph6 record

```text
Q???C@?GCoOoDO[?CcAO_?k?J??
```

This is an 18-vertex Blanuša snark. Number its edges lexicographically:

| id | edge | \(\phi\) | id | edge | \(\phi\) | id | edge | \(\phi\) |
|---:|:---:|---:|---:|:---:|---:|---:|:---:|---:|
| 0 | 0–7 | 2 | 9 | 3–10 | 4 | 18 | 6–11 | 6 |
| 1 | 0–10 | 6 | 10 | 3–12 | 1 | 19 | 6–16 | 2 |
| 2 | 0–11 | 4 | 11 | 3–13 | 5 | 20 | 6–17 | 4 |
| 3 | 1–8 | 2 | 12 | 4–10 | 2 | 21 | 7–12 | 5 |
| 4 | 1–13 | 1 | 13 | 4–15 | 1 | 22 | 7–17 | 7 |
| 5 | 1–15 | 3 | 14 | 4–17 | 3 | 23 | 8–14 | 1 |
| 6 | 2–9 | 3 | 15 | 5–11 | 2 | 24 | 8–16 | 3 |
| 7 | 2–13 | 4 | 16 | 5–12 | 4 | 25 | 9–15 | 2 |
| 8 | 2–14 | 7 | 17 | 5–14 | 6 | 26 | 9–16 | 1 |

The values \(1,\ldots,7\) denote the nonzero binary vectors in
\(\mathbb F_2^3\), with addition implemented by bitwise XOR. Directly XORing
the three incident values at every vertex gives zero, so the table is a
nowhere-zero flow.

Take

\[
t=4,\qquad s=3,\qquad S=\{e_5,e_6,e_{14}\}.
\]

Then

\[
E_4=\{e_2,e_7,e_9,e_{16},e_{20}\}.
\]

The graph \(H=G-E_4\) is connected. Nevertheless, no circuit of \(H\)
contains all three edges of \(S\).

## A short, human-checkable exhaustive proof

The connected graph \(H\) has 18 vertices and 22 edges, so its binary cycle
space has dimension

\[
22-18+1=5.
\]

The following five even edge-sets form a basis:

\[
\begin{aligned}
B_0={}&\{0,1,4,5,10,11,12,13,21\},\\
B_1={}&\{3,5,6,8,23,25\},\\
B_2={}&\{0,1,12,14,22\},\\
B_3={}&\{3,5,15,17,18,19,23,25,26\},\\
B_4={}&\{3,5,24,25,26\}.
\end{aligned}
\]

Each row can be checked directly to have even degree at every vertex.
They are independent: edges \(4,6,14,17,24\), respectively, occur in just
one of these five basis rows. Dimension then proves that this is the whole
cycle space.

Write an arbitrary even subgraph as
\(\sum_{i=0}^4 a_iB_i\), with coefficients in \(\mathbb F_2\). Requiring
edges \(5,6,14\) gives

\[
a_1=1,\qquad a_2=1,\qquad a_0+a_1+a_3+a_4=1.
\]

Thus \(a_0=a_3+a_4\), and there are exactly four even subgraphs containing
\(S\). Their edge sets are:

\[
\begin{array}{c|l|l}
(a_3,a_4)&\text{edge set}&\text{nontrivial component vertex sets}\\ \hline
(0,0)&
\{0,1,3,5,6,8,12,14,22,23,25\}&
\{0,4,7,10,17\};\ \{1,2,8,9,14,15\}\\
(1,0)&
\{4,5,6,8,10,11,13,14,15,17,18,19,21,22,26\}&
\{1,3,4,7,12,13,15,17\};\ \{2,5,6,9,11,14,16\}\\
(0,1)&
\{4,5,6,8,10,11,13,14,21,22,23,24,26\}&
\{1,3,4,7,12,13,15,17\};\ \{2,8,9,14,16\}\\
(1,1)&
\{0,1,3,5,6,8,12,14,15,17,18,19,22,24,25\}&
\{0,4,7,10,17\};\
\{1,2,5,6,8,9,11,14,15,16\}
\end{array}
\]

Every row has two nontrivial components. These are all the even subgraphs
of \(H\) containing \(S\), so none is a circuit.

## Independent finite checks

Run:

```bash
python3 scratch/verify_avoiding_circuit_counterexample.py
```

The checker uses only the Python standard library. It decodes the graph6
record, verifies the displayed edge list and flow, exhausts all vertex
shores to prove cyclic edge-connectivity four, exhaustively rejects a
proper three-edge-colouring, verifies bridgelessness and girth five, and
enumerates all \(2^5=32\) even subgraphs of \(H\).

For a small-order comparison, run:

```bash
python3 scratch/audit_petersen_avoiding_circuits.py
```

This second standard-library checker exhausts all \(64^3\) triples of binary
flows on the Petersen graph. It retains all 28,560 labelled nowhere-zero
\(\mathbb F_2^3\)-flows and checks all 655,200 resulting choices of
connected \(t\)-deletion and three equal-\(s\) edges. Every one has a
circuit. Thus the failure is absent from the Petersen graph but occurs
already on 18 vertices. Together with the standard small-snark
classification (the Petersen graph is the only snark below order 18), this
makes the displayed 18-vertex witness order-minimal among snarks.

## What remains true

There are two useful sharp remnants.

1. For every fixed \(t\), \(G-E_t\) has no bridge. Indeed, if
   \(\delta_{G-E_t}(X)=\{e\}\), then the flow cut equation in \(G\) says
   \(\phi(e)\) is either \(0\) or \(t\), both impossible for
   \(e\notin E_t\).

2. If \(G-E_t\) is connected, then any one or two prescribed edges lie on
   a circuit avoiding \(E_t\). This is the \(k=2\) case of the
   Knappe–Pitz circuit theorem, since a connected bridgeless graph has no
   odd cut of size at most two.

For three equal-value edges, the flow cut equation also shows that \(S\)
itself cannot be an odd cut: if
\(\delta_{G-E_t}(X)=S\), then the cut sum in \(G\) is either \(s\) or
\(s+t\), never zero. Hence Jaeger’s theorem supplies an even subgraph
through \(S\), but the explicit witness above shows that it need not be
connected. If \(G-E_t\) is additionally 3-edge-connected, the
\(g(3)=3\) result of Knappe and Pitz does supply a circuit. The exact
failure frontier is therefore the 2-edge-cut structure of \(G-E_t\).

Reference: P. Knappe and M. Pitz, “Circuits through prescribed edges,”
*Journal of Graph Theory* 93 (2020), 470–482,
<https://doi.org/10.1002/jgt.22497>.
