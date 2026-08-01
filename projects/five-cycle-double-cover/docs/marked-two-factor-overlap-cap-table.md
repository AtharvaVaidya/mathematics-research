# Exact local overlap caps for marked factor circuits through excess four

Date: **2026-07-26**.

Status: **EXACT FINITE LOCAL CENSUS / TRANSPARENT CHECKER /
SELECTED CAPS HAVE SHORT HUMAN PROOFS / FIVE-CDC STILL OPEN**.

This note determines the strongest bound supplied by the union of one
marked \(ac\)-factor circuit and one marked \(bc\)-factor circuit when
their core lengths are at most \(18\).  It also records precisely which
part is a short paper proof and which part is a finite enumeration.

The result is local.  An entry called *sharp* below means that the
weighted two-circuit union has a girth-ten realization.  It does not say
that this union extends to a full cubic graph with all eight marked
factor circuits.

## 1. Setup and answer

Let the two marked core circuits have lengths
\[
                          10+2x,\qquad 10+2y,
 \qquad 0\le x,y\le4,                                 \tag{1}
\]
and let \(m\) be their number of common core \(c\)-edges.  The table rows
are \(x=0,\ldots,4\), and the columns are \(y=0,\ldots,4\).

For different marks, the exact local maxima are
\[
\boxed{
\begin{pmatrix}
1&2&2&2&2\\
2&2&2&3&3\\
2&2&3&3&4\\
2&3&3&3&4\\
2&3&4&4&4
\end{pmatrix}}.                                      \tag{2}
\]

For the same mark, the exact local maxima are
\[
\boxed{
\begin{pmatrix}
1&1&2&2&2\\
1&2&2&2&3\\
2&2&2&3&3\\
2&2&3&3&4\\
2&3&3&4&4
\end{pmatrix}}.                                      \tag{3}
\]

Both matrices are symmetric, as they must be.

## 2. Exact weighted-kernel reduction

Put \(a=5+x\) and \(b=5+y\).  Thus the core circuits contain \(a\) and
\(b\) \(c\)-edges.

Delete the \(m\) common \(c\)-connections from both lifted circuits and
suppress the interiors of all remaining paths.  The \(2m\) connection
endpoints carry three perfect matchings:

- \(Q\), formed by the common connections;
- \(P_A\), formed by the residual \(A\)-paths; and
- \(P_B\), formed by the residual \(B\)-paths.

Both \(Q\cup P_A\) and \(Q\cup P_B\) are Hamilton circuits on these
\(2m\) endpoints.  Conversely, every pair of such residual matchings,
with the path weights described next, expands to exactly one abstract
two-factor union.  Internal vertices of different residual paths are
distinct.  Thus every circuit in the expansion is exactly an expanded
circuit of the three-matching kernel.  In particular,
\[
 \text{expanded union has girth at least ten}
 \quad\Longleftrightarrow\quad
 \text{every weighted kernel circuit has weight at least ten}. \tag{4}
\]

This includes parallel kernel edges: they represent internally disjoint
paths and their two-edge kernel circuit expands to the union of those
paths.  If both have weight one, (4) rejects the resulting parallel
ambient edges automatically.

### 2.1 Same mark

The common marked edge is represented by one connection of weight two;
the other \(m-1\) connections have weight one.  If
\[
                  d^A_0+\cdots+d^A_{m-1}=a,\qquad d^A_i\ge1,
\]
then the residual \(A\)-path weights are exactly
\[
                            2d^A_i-1.                 \tag{5}
\]
The \(B\)-weights are obtained from a positive composition of \(b\) in
the same way.

### 2.2 Different marks

All common connections have weight one.  Each circuit has a private
marked \(c\)-edge, so
\[
                         m\le a-1,\qquad m\le b-1.    \tag{6}
\]
For a positive composition \(d^A_0+\cdots+d^A_{m-1}=a\), exactly one
part contains the private mark.  That part is at least two.  Its path
weight is \(2d^A_i\); every other path has weight \(2d^A_j-1\).
The statement for \(B\) is identical.  The location of the subdivision
inside that degree-two path cannot affect any circuit length, so no
data have been discarded.

Equations (5)--(6) give a complete finite parameterization, not a
relaxation.

## 3. Bounds before enumeration

The general marked-overlap theorem gives
\[
                              m\le x+y+1.             \tag{7}
\]
For different marks this improves, whenever \(x+y\ge2\), to
\[
                              m\le x+y.               \tag{8}
\]
Indeed, equality in (7) makes the symmetric difference have total
length \(20\).  It is therefore \(C_{20}\) or \(C_{10}\sqcup C_{10}\).
Any three of the common unit connections give the three-chord argument
in `docs/order96-incidence-skeleton-nonrealizability.md`: in the first
case the five chord-matching types force a circuit of length at most
eight, and in the second case three cross-connections force one of
length at most eight.

Together, (6)--(8) leave the elementary search cap
\[
 \begin{cases}
 \min(x+y,\ 4+\min(x,y)),&\text{different marks and }x+y\ge2,\\
 x+y+1,&\text{different marks and }x+y<2,\\
 \min(x+y+1,\ 5+\min(x,y)),&\text{same mark}.
 \end{cases}                                         \tag{9}
\]

The especially important same-mark, \(x+y=2,m=3\) case has a separate
short proof in `docs/diagonal-c14-c10-triple-overlap.md`.  Its
six-vertex kernel is either the triangular prism or \(K_{3,3}\);
total kernel weight \(22\) forces a circuit of length at most nine in
both cases.  Hence every corresponding entry of (3) is at most two.

## 4. Finite part of the proof

It remains to decide the values allowed by (9).  The checker uses the
following exhaustive normalization.

Label the common matching
\[
                  Q=\{(2i,2i+1):0\le i<m\}
\]
and fix
\[
                  P_A=\{(2i+1,2(i+1)):0\le i<m\},
\]
with indices modulo \(m\).  A matching \(P_B\) whose union with \(Q\)
is Hamiltonian is specified by:

1. a cyclic permutation of the \(m\) common edges; and
2. one orientation bit for each common edge.

Rotate the \(B\)-circuit so edge \(0\) comes first.  Reflection of the
fixed \(A\)-circuit reverses the orientation of edge \(0\), so that bit
may also be fixed.  Every reflected \(A\)-weight sequence remains in
the composition list.  The retained
\[
                       (m-1)!\,2^{m-1}               \tag{10}
\]
signed orders are consequently exhaustive, though not necessarily
isomorphism-free.

For each signed order the checker:

1. generates every composition in Section 2;
2. generates every simple kernel circuit by depth-first search,
   including two-edge circuits made of parallel kernel edges;
3. sums the exact positive integer path weights; and
4. accepts precisely when every circuit has weight at least ten.

All multiplicities through six are decided directly this way.  This is
more than is needed for most cells.

For a possible multiplicity \(m\ge7\), let \(U\) be the expanded union.
It is a simple graph of minimum degree two, with
\[
\begin{array}{c|c|c}
&|V(U)|&|E(U)|\\ \hline
\text{different marks}&22+2(x+y)-2m&22+2(x+y)-m\\
\text{same mark}&21+2(x+y)-2m&21+2(x+y)-m .
\end{array}                                          \tag{11}
\]
The checker applies the irregular Moore bound of Alon, Hoory, and
Linial.  For average degree \(d\) and girth at least ten it requires
\[
                |V(U)|\ge
                2\sum_{i=0}^{4}(d-1)^i.              \tag{12}
\]
Every multiplicity at least seven still allowed by (9) violates (12).
The comparison is performed with integers after clearing
denominators.  The primary reference is N. Alon, S. Hoory, and
N. Linial, [*The Moore Bound for Irregular
Graphs*](https://web.math.princeton.edu/~nalon/PDFS/ahl1.pdf),
Graphs and Combinatorics 18 (2002), 53--57.

The direct search makes 214 yes/no decisions; (12) removes the remaining
14 high-multiplicity cases.  The resulting maxima are exactly (2)--(3).

## 5. Sharpness data

For every one of the 50 entries, the checker retains and prints one
accepted tuple
\[
       (\text{\(A\)-path weights},\text{\(B\)-path weights},
        \text{signed \(B\)-order})                   \tag{13}
\]
at the displayed maximum.  The checker then obtains girth at least ten
by enumerating all circuits of that same kernel.  Thus the numbers in
(2)--(3) are maxima in the exact local model, rather than upper bounds
rounded down without witnesses.

These lower witnesses are deliberately not called ambient graph
realizations.  Compatibility with the other six factor circuits is an
additional global condition.

## 6. Reproduction

Run:

```text
clang++ -std=c++20 -O3 \
  scratch/verify_marked_two_factor_overlap_caps.cpp \
  -o /tmp/verify_marked_two_factor_overlap_caps
/tmp/verify_marked_two_factor_overlap_caps \
  > /tmp/marked-overlap-caps.out \
  2> /tmp/marked-overlap-caps-witnesses.txt
```

The retained standard output is:

```text
offdiagonal
1 2 2 2 2
2 2 2 3 3
2 2 3 3 4
2 3 3 3 4
2 3 4 4 4
diagonal
1 1 2 2 2
1 2 2 2 3
2 2 2 3 3
2 2 3 3 4
2 3 3 4 4
marked two-factor overlap cap census: PASS
exact_search_decisions=214
irregular_moore_exclusions=14
```

The standard-output SHA-256 is
`588d534c9e79e7bb14eaf9ab5f6d25e46ea407603dd75133457dffbd9120456c`.
The witness-stream SHA-256 is
`1a768838ca2a03b18106f9f4bfd47878c0aefee4752f022aac94d3ba9518083d`.
The verifier source SHA-256 is
`72a272ad9d455817d5fca908715215023f033c2afe8ac0536b19b244bfa94790`.

## 7. Scope and proof status

The weighted-kernel equivalence, the preliminary bounds, the
same-mark sum-two obstruction, and the Moore exclusions are displayed
as human-checkable arguments.  The remaining individual caps are a
small computer-assisted finite theorem: their authority is the
self-contained exhaustive checker, not a SAT solver without a proof
object and not a heuristic rotation search.

Consequently these tables may safely strengthen an incidence
relaxation only when that relaxation uses exactly the local hypotheses
of Section 1.  They do not eliminate all order-\(96\), order-\(98\), or
order-\(100\) profiles without a separate complete incidence census,
and they do not resolve the five-cycle double cover conjecture.

## AI-use disclosure

An OpenAI Codex agent, under human direction, formulated the exact
weighted-kernel model, found and checked the cap tables, supplied the
short sum-two proof, and wrote the checker and this note.  The
computation is reproducible and its scope is explicit, but it is not
independent human peer review.
