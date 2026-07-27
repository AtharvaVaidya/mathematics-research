# Five-CDC as a five-point restriction of the eight-coordinate triangle lift

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE EXACT REFORMULATION / LOCAL COMPRESSION
FREEDOM CLASSIFIED / NOT A RESOLUTION**.

The 2026 eight-coordinate construction starts with a nowhere-zero
\(\mathbb F_2^3\)-flow and assigns to every graph edge an unordered pair
of points of \(\mathbb F_2^3\).  At a cubic vertex, the three edge pairs
are the three sides of a triangle.  This note asks exactly what happens
when all those triangle points are required to lie in one five-point
subset.

The answer is rigid.  Every five-point subset singles out one Fano line.
Vertices carrying that line have four local choices; vertices carrying
any other line have exactly one.  Thus a five-coordinate compression has
no unaccounted local freedom: its remaining obstruction is precisely the
previously derived Fano component-parity lift.

## 1. Compatible coordinate triangles

Put \(W=\mathbb F_2^3\).  Let \(G\) be a finite loopless cubic multigraph
and let
\[
                     f:E(G)\longrightarrow W-\{0\}
\]
be a flow.  The three values incident with a vertex \(v\) are the three
nonzero members of a two-dimensional subspace
\[
                         H_v\le W.                    \tag{1}
\]

A **coordinate triangle** at \(v\) is a three-element set \(P_v\subset W\)
whose three pairwise differences are the three members of \(H_v-\{0\}\).
Equivalently, \(P_v\) is obtained by deleting one point from one of the
two affine cosets of \(H_v\).  Each incident edge is assigned the unique
pair in \(P_v\) whose difference is its flow value.

The triangles are **compatible** if the two ends of every graph edge
assign it the same unordered pair.  The triangle-gluing theorem in the
eight-coordinate construction says that compatible triangles exist for
every displayed nowhere-zero \(W\)-flow.  Their eight point-indexed
supports are Eulerian and double-cover every edge.

> **Five-point restriction theorem.**  
> A loopless cubic multigraph has a standard Five-Cycle Double Cover if
> and only if it has a nowhere-zero \(W\)-flow with compatible coordinate
> triangles \(P_v\) all contained in one five-element set \(S\subset W\).

### Proof

Given the restricted triangles, use the five points of \(S\) as the five
cover coordinates.  At every vertex, a point belongs to zero or two sides
of its coordinate triangle, so each coordinate support is Eulerian.
Every edge pair has two distinct points and is therefore covered exactly
twice.

Conversely, label every edge of a Five-CDC by the two cover coordinates
which contain it, and inject the at most five coordinates into \(W\).
At a cubic vertex the three weight-two labels xor to zero.  They are
therefore the three distinct edges of a triangle on three coordinate
names.  Taking pairwise differences gives a nowhere-zero \(W\)-flow, and
the coordinate triangles are already compatible.  Empty cover
coordinates may be used to pad to five. \(\square\)

This statement is for the standard, unoriented conjecture.  No direction
is assigned to either occurrence of an edge.

## 2. Every five-set has one special line

Let \(S\subset W\) have size five and put \(R=W-S\).  The three points of
\(R\) lie in a unique affine plane.  Its fourth point is
\[
                         p=\bigoplus_{r\in R}r.        \tag{2}
\]
In particular \(p\in S\).  Translate by \(p\).  The affine plane becomes
a two-dimensional subspace \(H\), and the five-set has the canonical form
\[
                         S=\{0\}\mathbin{\dot\cup}(a+H),
                         \qquad a\notin H.             \tag{3}
\]
Translation changes no pair difference.

> **Local five-point list theorem.**  
> With \(S\) in the form (3):
>
> 1. if \(H_v=H\), exactly four coordinate triangles for \(H_v\) lie in
>    \(S\); they are the four three-subsets of \(a+H\);
> 2. if \(H_v\ne H\), exactly one coordinate triangle for \(H_v\) lies in
>    \(S\), namely
>    \[
>                      \{0\}\cup(H_v\cap(a+H)).        \tag{4}
>    \]

### Proof

If \(H_v=H\), a coordinate triangle is three points of either \(H\) or
\(a+H\).  The set \(S\) contains only one point of \(H\), so the first
coset supplies none.  It contains all four points of \(a+H\), and deleting
any one of them gives the four claimed triangles.

Now suppose \(H_v\ne H\).  Two distinct two-dimensional subspaces of
\(W\) meet in a one-dimensional subspace, so
\[
                         |H_v\cap H|=2.               \tag{5}
\]
Every affine coset of \(H_v\) consequently contains two points of \(H\)
and two of \(a+H\).  A three-point subset of such a coset can lie in
\(\{0\}\cup(a+H)\) only if the coset contains \(0\) and the other point
of its intersection with \(H\) is the omitted point.  This forces the
coset to be \(H_v\) and gives exactly (4). \(\square\)

There are \(56\) choices of \(S\).  The literal checker
`../scratch/verify_five_point_triangle_list_lift.py` and the independently
structured bit-mask replay
`../scratch/verify_five_point_triangle_list_lift.mjs` both enumerate all
\(56\cdot7=392\) five-set/line cases.  They obtain \(56\) special cases
with four triangles and \(336\) nonspecial cases with one triangle, for
\[
                         56(4+6)=560
\]
admitted local triangles in total.

## 3. Exact shape of the remaining obstruction

The local theorem also determines every edge-pair shape.

* If \(f(e)\in H\), both coordinate labels on \(e\) lie in \(a+H\).
* If \(f(e)\notin H\), its coordinate pair is
  \[
                              \{0,f(e)\},              \tag{6}
  \]
  after the normalization (3).

For the first assertion, it is immediate at an \(H_v=H\) vertex.  At an
\(H_v\ne H\) vertex, the unique nonzero member of \(H_v\cap H\) is the
difference of the two points of (4) lying in \(a+H\).  The other two
differences use the pairs joining \(0\) to those two points.  This proves
both assertions.

Let \(F_H\) be the spanning subgraph of the \(H-\{0\}\)-valued edges.
It has degree three at vertices with \(H_v=H\) and degree one everywhere
else.  Summing the parity equation for any coordinate \(b\in a+H\) over
a component \(K\) of \(F_H\) shows that the boundary edges labelled
\(\{0,b\}\) occur evenly.  By (6), this says
\[
 |\,\delta(K)\cap f^{-1}(b)\,|\equiv0\pmod2
              \qquad(b\in a+H).                       \tag{7}
\]

Conversely, the componentwise conditions (7) are exactly the binary
lift equations already proved in
`five-cdc-fano-component-parity-lift.md`: they construct the choices on
the \(H\)-valued edges and hence compatible triangles inside \(S\).
Thus the five-point restriction of the eight-coordinate construction is
not a new relaxation.  It is another exact presentation of the same
Fano component-parity criterion.

The remaining universal obligation is still to **select** a nowhere-zero
\(\mathbb F_2^3\)-flow and a line \(H\) satisfying (7).  Fixed-flow
counterexamples in the project show that the choice of \(H\) alone is not
enough.  The local list theorem narrows where a successful compression can
act, but it does not prove that a successful flow exists.

## AI-use disclosure

OpenAI Codex, under human direction, derived this five-point list form,
wrote the literal enumeration, and drafted the note.  The underlying
eight-coordinate triangle-gluing theorem and the standard two-subset
Five-CDC encoding are attributed in the project status and source audit.
Every new deduction above is displayed for line-by-line checking.  This is
not independent human peer review and is not a resolution of Five-CDC.
