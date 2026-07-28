# Root-good \(D_5\)-flows as connected pairs of \(T\)-joins

Date: **2026-07-28**

Status: **EXACT HUMAN-CHECKABLE EQUIVALENCE / NOT A FIVECDC
RESOLUTION**.

All graphs below are finite, loopless, and cubic.  Parallel edge objects
cause no change.  Fix distinct graph edges \(r,s\).

## 1. Statement

For a matching \(M\), put
\[
                    T=\partial M=V(M),\qquad K=G-M.
\]
A \(T\)-join in \(K\) is an edge set whose odd-degree vertices are
exactly \(T\).

> **Rooted matching/four-flow theorem.**  The following are equivalent.
>
> 1. \(G\) has a \(D_5\)-flow for which \(r,s\) lie on one component of
>    one factor \(Y_{ij}\).
> 2. There exist:
>    - a matching \(M\) avoiding \(r,s\);
>    - a nowhere-zero \(\mathbb F_2^2\)-flow on \(K=G-M\); and
>    - two edge-disjoint \(T\)-joins \(J_0,J_1\subseteq K\)
>      such that \(r,s\) lie on one connected component of
>      \(J_0\cup J_1\).

Because \(G\) is cubic and the joins are edge-disjoint,
\(J_0\cup J_1\) is automatically 2-regular: at a vertex of \(T\), each
join uses exactly one of the two \(K\)-edges; outside \(T\), a join has
degree zero or two and both joins cannot simultaneously have degree two.
Thus its nonempty components are circuits.

## 2. From a root-good flow to the packing

Let \(q:E(G)\to D_5\) be root-good for the factor
\[
                         Y_{ij}=C_i\mathbin\triangle C_j.
\]
Put
\[
                   M=C_i\cap C_j.
\]
An edge lies in \(M\) exactly when its label is \(ij\).  At a cubic
vertex the three labels are the three edges of a coordinate triangle,
so a fixed label occurs at most once.  Hence \(M\) is a matching.
Because \(r,s\in Y_{ij}\), neither root belongs to \(M\).

Set
\[
             J_0=C_i-M,\qquad J_1=C_j-M.
\]
The two joins are edge-disjoint.  Since \(C_i,C_j\) are even,
\[
             \partial J_0=\partial M=T=\partial J_1.
\]
Their union is \(C_i\triangle C_j=Y_{ij}\), so one component contains
both roots.

Finally,
\[
                Y_{ij},\quad C_k\quad(k\notin\{i,j\})
\]
is a four-even-subgraph double cover of \(K\).  Quotienting its
weight-two words by the all-ones word gives a nowhere-zero
\(\mathbb F_2^2\)-flow on \(K\).  Equivalently, a subdivision of a
cubic graph has a 4-CDC exactly when it has a nowhere-zero 4-flow.

## 3. From the packing to a root-good flow

Assume condition 2 and put
\[
             A=M\mathbin{\dot\cup}J_0,\qquad
             B=M\mathbin{\dot\cup}J_1.
\]
Because \(\partial J_i=\partial M\), both \(A\) and \(B\) are binary
cycles.  Edge-disjointness gives
\[
                    A\cap B=M,\qquad
                    A\mathbin\triangle B=J_0\cup J_1.          \tag{1}
\]

It remains to retain the prescribed first member in a 4-CDC of \(K\).
This can be checked directly.  Write the three nonzero values of
\(\mathbb F_2^2\) as \(1,2,3\), use the linear section
\[
 s(1)=1100,\qquad s(2)=1010,\qquad s(3)=0110,
\]
and put \(k=1111\).  Let \(\ell\) be coordinate zero of \(s\), let
\(\phi\) be the given nowhere-zero flow, and put
\[
 h(e)=1_{J_0\cup J_1}(e)+\ell(\phi(e)),\qquad
 d(e)=s(\phi(e))+h(e)k.
\]
The support of \(h\) is a binary cycle, so \(d\) is an even
four-coordinate flow.  The two members of each nonzero quotient coset
are complementary weight-two words; hence every \(d(e)\) has weight
two.  Its coordinate-zero support is exactly \(J_0\cup J_1\).
Consequently \(K\) has a 4-CDC
\[
                   J_0\cup J_1,\ D_1,\ D_2,\ D_3.
\]

Replace its first member by \(A,B\).  Edges of \(M\) occur in \(A,B\);
edges of \(J_0\cup J_1\) occur in exactly one of \(A,B\) and exactly one
of \(D_1,D_2,D_3\); all other edges occur in exactly two of
\(D_1,D_2,D_3\).  Therefore
\[
                         A,\ B,\ D_1,\ D_2,\ D_3
\]
is a 5-CDC of \(G\).  By (1), the factor obtained from its first two
coordinates is \(J_0\cup J_1\), whose displayed component contains
\(r,s\).  This proves condition 1.

## 4. Equivalent marked-circuit form

Condition 2 may instead be stated using a 2-regular subgraph
\(D\subseteq K\):

- \(D\) contains every vertex of \(T\);
- every component of \(D\) contains an even number of vertices of \(T\);
- one component of \(D\) contains \(r,s\).

To obtain \(J_0,J_1\), traverse each circuit of \(D\).  Keep the current
join name at an unmarked vertex and swap names at a vertex of \(T\).
The even-mark condition makes the rule consistent on returning to the
start.  At each marked vertex one incident circuit edge goes to each
join; at every unmarked vertex both go to the same join.  Conversely,
the union of two edge-disjoint \(T\)-joins has exactly this form.

This version isolates the remaining routing problem: find one exact-zero
matching whose 4-flow complement has a marked circuit system joining the
two roots.

## 5. Relation to known results and the current frontier

Hoffmann-Ostenhof's Corollary 0.6 characterizes an unrooted 5-CDC by a
matching \(M\), a nowhere-zero 4-flow on \(G-M\), and two 2-regular
subgraphs whose exact intersection is \(M\).  The theorem above is its
rooted factor-connectivity refinement, proved here to eliminate any
convention gap.  No claim is made that this refinement is absent from
the literature.

For the minimum-counterexample edge elimination, \(G\) may be restricted
to a simple 3-edge-connected cubic graph of girth at least eight, with
every 8-circuit through both roots and every 9-circuit through at least
one.  A proof of the remaining rooted premise is therefore equivalent to
showing that some certificate in condition 2 exists in that restricted
class.  The present theorem changes the language of the obstruction; it
does not prove that the obstruction cannot occur.

Primary comparison:

- A. Hoffmann-Ostenhof, *A note on 5-cycle double covers*, Graphs and
  Combinatorics 29 (2013), 977--979,
  <https://doi.org/10.1007/s00373-012-1169-8>.

## AI-use disclosure

An OpenAI Codex agent, under human direction, derived and wrote this
rooted refinement after comparing it with the project's independently
proved matching/four-flow theorem.  The equivalence is ordinary
mathematics written out in full.  It is not a proof of FiveCDC and has
not yet received independent human peer review.
