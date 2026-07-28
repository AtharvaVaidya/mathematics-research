# Petersen is a cover-level Kempe-to-\(R_5\) countermodel

## Exact statement and scope

Let a cover-level Kempe move on an indexed family
\((D_0,\ldots,D_7)\) choose \(i<j\), choose one connected component of
\(D_i\mathbin\triangle D_j\), and interchange membership in \(D_i,D_j\)
on that component.

The Petersen graph has an eight-coordinate cycle double cover, with two
empty coordinates, whose entire component under these moves has 20,160
states and contains no state whose coordinate co-occurrence graph maps to
the Hamming-distance-two graph \(R_5\).

The host graph is simple, cubic, non-Tait, has girth five, and has cyclic
edge-connectivity five.  Thus it meets the requested non-Tait and
cyclically-four conditions, but not the optional girth-at-least-ten
strengthening.

This is a countermodel only to the proposed universal procedure

> start with an arbitrary supplied at-most-eight cover, use cover-level
> component Kempe moves, and finish by an \(R_5\) compression.

It is **not** a counterexample to the Five-Cycle Double Cover Conjecture.
The use of two empty coordinates is explicit: the result applies when an
at-most-eight cover is represented as an indexed eight-cover by padding
with empty Eulerian edge sets.  It does not settle a separately imposed
variant requiring all eight input coordinates to be nonempty.

## The graph and cover

Use the following edge order and labels.  A label \(ab\) means that the
edge belongs to coordinates \(a\) and \(b\).

| edge | endpoints | label |
|---:|:---:|:---:|
| 0 | 01 | 35 |
| 1 | 12 | 45 |
| 2 | 23 | 24 |
| 3 | 04 | 03 |
| 4 | 34 | 02 |
| 5 | 05 | 05 |
| 6 | 16 | 34 |
| 7 | 27 | 25 |
| 8 | 57 | 15 |
| 9 | 38 | 04 |
| 10 | 58 | 01 |
| 11 | 68 | 14 |
| 12 | 49 | 23 |
| 13 | 69 | 13 |
| 14 | 79 | 12 |

All fifteen pairs on \(\{0,1,2,3,4,5\}\) occur exactly once.
Coordinates 6 and 7 are empty.

At graph vertices \(0,\ldots,9\), the three incident labels are,
respectively,

\[
\begin{array}{c|c}
0&35,03,05\\
1&35,45,34\\
2&45,24,25\\
3&24,02,04\\
4&03,02,23\\
5&05,15,01\\
6&34,14,13\\
7&25,15,12\\
8&04,01,14\\
9&23,13,12
\end{array}
\]

Every row consists of the three pairs of a three-element set.  Each
coordinate therefore occurs zero or two times at every graph vertex.
Consequently every \(D_i\) is Eulerian.  Each graph edge has a two-element
label, so it is covered exactly twice.  This proves directly that the
displayed labels form the intended eight-coordinate CDC.

## Every Kempe move is a global transposition

For an active coordinate \(a\in\{0,\ldots,5\}\), its support is the
following five-cycle, written by edge IDs:

\[
\begin{array}{c|l}
a& D_a\\ \hline
0&3,4,9,10,5\\
1&8,14,13,11,10\\
2&2,4,12,14,7\\
3&0,6,13,12,3\\
4&1,2,9,11,6\\
5&0,1,7,8,5
\end{array}
\]

For two active coordinates, the fifteen symmetric differences are the
following single eight-cycles:

\[
\begin{array}{c|l}
01&3,4,9,11,13,14,8,5\\
02&2,9,10,5,3,12,14,7\\
03&0,6,13,12,4,9,10,5\\
04&1,2,4,3,5,10,11,6\\
05&0,1,7,8,10,9,4,3\\
12&2,4,12,13,11,10,8,7\\
13&0,6,11,10,8,14,12,3\\
14&1,2,9,10,8,14,13,6\\
15&0,1,7,14,13,11,10,5\\
23&0,6,13,14,7,2,4,3\\
24&1,7,14,12,4,9,11,6\\
25&0,1,2,4,12,14,8,5\\
34&0,1,2,9,11,13,12,3\\
35&1,7,8,5,3,12,13,6\\
45&0,6,11,9,2,7,8,5
\end{array}
\]

Thus:

* for active \(i,j\), \(D_i\triangle D_j\) has one component;
* for active \(i\) and empty \(j\), it is the one five-cycle \(D_i\);
* for the two empty coordinates it is empty.

Swapping \(i,j\) on the whole of \(D_i\triangle D_j\) changes every edge
label containing exactly one of \(i,j\), and fixes labels containing both
or neither.  That is precisely the global permutation of coordinate names
\((i\,j)\).

After a global coordinate permutation, the same description remains true
with the names permuted.  Induction therefore shows that every reachable
state is a coordinate permutation of the displayed cover.  Conversely,
every transposition involving at least one active coordinate is legal;
the transposition of the two empty names has no effect.  Hence the
reachable component is exactly the orbit

\[
S_8/S_2,
\qquad |S_8/S_2|=\frac{8!}{2!}=20{,}160.
\]

Every orbit state uses all fifteen pairs on some six coordinate names.
Its co-occurrence graph is therefore \(K_6\) plus two isolated vertices.

## Why \(K_6\) cannot map to \(R_5\)

The vertices of \(R_5\) are the binary words in \(\mathbb F_2^5\), with
two words adjacent when their Hamming distance is two.  Translate any
clique so that it contains zero.  Every other word in it then has weight
two.  Their two-element supports must be pairwise intersecting, since two
weight-two words are at distance two exactly when their supports intersect
in one point.

A pairwise-intersecting family of two-subsets of a five-set has size at
most four: if all pairs contain one fixed point it is a star of size four;
otherwise three pairs form a triangle and no fourth distinct pair can meet
all three.  Including zero, every clique in \(R_5\) has size at most five.
A homomorphism from the loopless clique \(K_6\) would have to embed it as a
six-clique.  Therefore no reachable co-occurrence graph maps to \(R_5\).

## Human check that the host is a strict snark

The edge table immediately gives a simple connected cubic graph.  Its
six perfect matchings are

\[
\begin{split}
&(0,2,8,11,12),\quad(0,4,7,10,13),\\
&(1,3,8,9,13),\quad(1,4,5,11,14),\\
&(2,3,6,10,14),\quad(5,6,7,9,12).
\end{split}
\]

They are exhaustive by branching on the one matching edge incident with
vertex 0 and propagating the remaining degree-one conditions.  The
complement of each is two five-cycles.  A proper three-edge-colouring of
a cubic graph would have one colour class as a perfect matching and its
other two classes as an even-cycle 2-factor.  None exists here, so the
graph is non-Tait.

The displayed five-cycles show girth at most five; direct inspection of
the adjacency table gives no triangle or four-cycle, hence girth five.
If an edge cut of size at most four had cyclic shores, girth five would
force at least five vertices on each shore.  Since the graph has ten
vertices, each shore would have exactly five.  A simple five-vertex graph
of girth five has at most five internal edges, whereas cubic degree-sum
gives

\[
|\delta(S)|=3|S|-2|E(S)|\ge15-10=5,
\]

a contradiction.  The complement of any displayed perfect matching is
two five-cycles, so that matching is a cyclic five-edge cut.  The cyclic
edge-connectivity is exactly five.

## Exact replay

Run:

```sh
python3 scratch/audit_petersen_cover_kempe_component.py \
  > /tmp/petersen-cover-kempe-component-audit.json
cmp scratch/petersen-cover-kempe-component-audit.json \
  /tmp/petersen-cover-kempe-component-audit.json
```

The standard-library checker independently:

1. binds itself to the frozen source by SHA-256;
2. checks simplicity, cubicity, connectivity, bridgelessness, girth, and
   every edge deletion set through size five;
3. enumerates all perfect matchings and proves non-Taitness by their
   complementary 2-factors;
4. checks the CDC parity equations and the initial \(5/8/0\)-cycle
   symmetric-difference profile;
5. performs a complete BFS of all legal current-state Kempe moves;
6. obtains 20,160 states, distance layers
   \[
   1,27,295,1665,5104,8028,5040,
   \]
   with degree 27 at every state; and
7. independently computes \(\omega(R_5)=5\).

The finite discovery and verification were produced with substantial
assistance from OpenAI Codex under human direction.  The explicit proof,
source-bound data, and exhaustive checker are supplied so that the
mathematical conclusion does not require trusting an AI system.
