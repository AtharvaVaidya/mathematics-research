# Local-rule rigidity in eight-to-five compression

Date: **2026-07-31**

Status: **new sharper no-go for context-free nonlinear recolouring; not a
proof or disproof of FiveCDC**.

Everything here is for the standard, unoriented conjecture.  A cycle is
an Eulerian edge-subset and empty members are allowed.  The witness is a
finite simple bridgeless cubic graph.

## 1. Exact input supplied by the eight-cycle theorem

Write (W=\mathbb F_2^3).  The Oum/Hušek--Šámal construction labels each
edge by a pair (P_e\in\binom W2).  At a cubic vertex the three pair
labels are

\[
                         xy,\quad xz,\quad yz                 \tag{1}
\]

for three distinct points (x,y,z\in W).  Indeed, if the first two
two-subsets are (A,B\), coordinate parity forces the third to be
(A\mathbin\triangle B); its size is two only when (A,B) meet in one
point.  Conversely, (1) gives even incidence in every old coordinate.

The eight even subgraphs are

\[
                         H_s=\{e:s\in P_e\}\qquad(s\in W).    \tag{2}
\]

Every edge is in its two pair coordinates.  There is no further hidden
restriction when the flow and lifting solution vary: from (1), put

\[
              \phi(xy)=x+y,\qquad t_{xyz}=x+y+z.              \tag{3}
\]

The three incident values are nonzero and xor to zero, and Oum's local
formula reconstructs (1).  Thus pair-labelled eight-covers are exactly
the construction's output family.  This is Hušek--Šámal, Observation
2.4; the short argument above makes the fact used here self-contained.

Every three-subset of (W) can occur as an affine triangle: for distinct
(x,y,z\), equations (3) give the required local flow and potential.

## 2. The nonlinear local rule that we rule out

Fix a set (S\subseteq W) of old coordinate names.  A
**context-free pair rule** is an arbitrary lookup table

\[
                       r:\binom S2\longrightarrow D_5,
        \qquad D_5=\{q\in\mathbb F_2^5:\operatorname{wt}(q)=2\}. \tag{4}
\]

It may be completely nonlinear in the binary names (x,y\).  It is only
required to give the same new label whenever the same old unordered pair
is encountered.  On a local triangle (xyz\), parity of the five new
coordinates is exactly

\[
                         r(xy)+r(xz)+r(yz)=0.                 \tag{5}
\]

This is more permissive than a fixed value-only map and is not assumed
to arise from xor-combinations of the old eight members.

## 3. Triangle-cocycle rigidity

Let (K_S\) be the complete graph on (S\).  Regard an
\(\mathbb F_2^d\)-valued pair table (r\) as an edge cochain on (K_S\).

**Lemma 1 (complete triangle rigidity).**  If (5) holds for every
three-subset of (S\), then there are words (a_x\in\mathbb F_2^d\) such
that

\[
                              r(xy)=a_x+a_y                   \tag{6}
\]

for every pair.  The (a_x\)'s are unique up to adding one common word.

**Proof.**  Fix (o\in S\), set (a_o=0\), and put (a_x=r(ox)\) for
(x\ne o\).  Equation (5) on (oxy\) gives (6).  If (b_x+b_y=a_x+a_y\)
for all pairs, then (a_x+b_x=a_y+b_y\) for all (x,y\), proving the
uniqueness statement. \(\square\)

The same conclusion holds when (5) is imposed only on a collection
\({\cal T}\) of triangles whose incidence vectors span the binary cycle
space of (K_S\).  To see this one coordinate at a time, (5) says that
the edge vector (r\) is orthogonal to \(\operatorname{span}({\cal T})\).
If this is the full cycle space, its orthogonal complement is the cut
space, whose elements are exactly (6).

For (S\) of size six, the cycle-space dimension is

\[
                            \binom62-6+1=10.                  \tag{7}
\]

## 4. Why six rigid old coordinates cannot map to five weight-two labels

Let (R_5\) be the graph on \(\mathbb F_2^5\) joining words at Hamming
distance two.  If (4)--(6) hold on all pairs of a six-set, then

\[
                         x\longmapsto a_x
\]

is a graph homomorphism (K_6\to R_5\).

**Lemma 2.**  The clique number of (R_5\) is five.

**Proof.**  Translate a clique so that it contains zero.  Every other
word then has weight two, and their two-subset supports are pairwise
intersecting.  Such a family is either contained in a star, with at most
four members, or contains a triangle (12,13,23\), after which there is
no fourth pair meeting all three.  Thus the clique has at most five
vertices.  Zero together with the four pairs in a four-edge star attains
five. \(\square\)

Consequently, any collection of realized local triangles spanning the
cycle space of (K_6\) makes a context-free rule (4) impossible.

## 5. A sharp 12-vertex realized rigidity witness

Take these twelve triples on old coordinate points (0,\ldots,5\), in
the displayed order:

\[
\begin{array}{rrrrrr}
012&013&014&015&023&024\\
025&123&134&135&245&345.
\end{array}                                                     \tag{8}
\]

Every pair occurs an even number of times.  Pair equal occurrences as
follows; each row is ``left vertex, right vertex, old pair label'':

```text
 0  1  01       2  3  01
 0  4  02       5  6  02
 1  4  03       2  5  04       3  6  05
 0  7  12
 1  8  13       7  9  13
 2  8  14       3  9  15       4  7  23
 5 10  24       6 10  25       8 11  34
 9 11  35      10 11  45
```

This produces a simple connected cubic graph.  Deleting each of its 18
edges leaves it connected, so it is bridgeless.  Its graph6 record in
the displayed vertex order is

```text
K`o_kP_COK?F
```

At every vertex (xyz\), the incident old labels are (xy,xz,yz\), so
they define an eight-cycle double cover (old coordinates 6 and 7 are
empty).  Equations (3) make it literally Oum-compatible.  All fifteen
pairs on (0,\ldots,5\) occur.

The twelve triangle incidence rows from (8), in the fifteen columns

```text
01 02 03 04 05 12 13 14 15 23 24 25 34 35 45
```

have binary rank ten.  By (7), they span the full cycle space of (K_6\).
Lemma 1 therefore forces every context-free recolouring satisfying local
parity on this single supplied cover to have form (6).  Lemma 2 then
contradicts the required weight-two output on all fifteen used pairs.

**Theorem 3 (realized nonlinear local-rule no-go).**  The displayed
simple bridgeless cubic graph and its supplied Oum eight-cover admit no
context-free pair rule from their old pair labels to five weight-two
labels that preserves vertex parity.

The rank-rigidity mechanism is sharp in graph order.  In any closed
pair-labelled cubic graph, every old pair occurs at an even number of
vertex incidences.  Hence the xor of all local triangle rows is zero.  A
set of rows of rank ten must therefore contain at least eleven rows.
Every cubic graph has even order, so at least twelve vertices are needed.
The witness attains twelve.  This is a minimum claim for the
**full-rank triangle-rigidity certificate**, not for every imaginable
nonlinear compression obstruction.

## 6. Why this is not a FiveCDC counterexample

The graph has the following proper 3-edge-colouring in the exact edge
order of the display above:

```text
0 1 1 1 2 0 2 2 1 1 2 0 0 2 0 0 2 1
```

Replace colours 0, 1, 2 by the weight-two labels 01, 02, 12.  At each
vertex these three labels xor to zero, giving a three-cycle double cover,
hence a FiveCDC after appending two empty members.

The positive cover must distinguish some graph edges having the same old
pair label.  Thus Theorem 3 isolates exactly what fails: a static lookup
table keyed only by the old unordered pair loses necessary global
context.  It does not rule out edge-dependent recolouring, changing the
Oum potential or flow, circuit switches, or selecting a different
eight-cover.  Choosing flow and potential existentially so that pure
merging succeeds is already equivalent to FiveCDC, as established in
the existing project package
`scratch/oum-combined-choice-equivalence-and-toggle.md`.

## 7. Standard versus orientable scope

No orientation variables are used.  The argument concerns parity of
Eulerian edge-subsets only.  The positive Tait cover can of course be
oriented componentwise, but no assertion is made that its two edge
occurrences receive opposite directions, and no orientable FiveCDC
criterion or counterexample follows.

## AI-use and trust disclosure

OpenAI Codex agents, under Atharva Vaidya's direction, found the
12-triangle full-rank witness, derived the rigidity and lower-bound
proofs, wrote the checker, and drafted this note.  The computation is
small, deterministic, and reproduced by a standalone standard-library
checker, but it was not independently authored by a human.  No peer
review or priority claim is made.  The proof above is intended to be
checked without trusting the program.
