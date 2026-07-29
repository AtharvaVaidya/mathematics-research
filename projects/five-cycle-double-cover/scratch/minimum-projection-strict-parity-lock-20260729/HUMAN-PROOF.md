# A strict parity lock for the minimum-projection method

## 1. Statement and exact scope

There is a simple connected bridgeless cubic graph \(G\) on 162
vertices with a unique cardinality-minimum extendable binary projection
\(H\).  It has
\[
                              |H|=54,
\]
is the disjoint union of two 27-circuits, and has no clean extension.

Because the minimum projection is unique, this refutes both the proposed
assertion that every globally minimum extendable projection is cleanable
and the weaker selection assertion that some globally minimum projection
is cleanable.  It does **not** refute the five-cycle-double-cover
conjecture: Section 7 gives two explicit five-cycle double covers of
\(G\).

## 2. Base graph

Use the audited 18-vertex cubic base \(B\).  Its first fourteen edges
are the two 7-circuits
\[
0\,1\,2\,3\,4\,5\,6\,0,\qquad
7\,8\,9\,10\,11\,12\,13\,7.
\]
The remaining edges, in order, are
\[
\begin{gathered}
0\!-\!11,\ 1\!-\!9,\ 2\!-\!12,\ 3\!-\!10,\\
14\!-\!4,\ 14\!-\!5,\ 14\!-\!15,\ 15\!-\!6,\ 15\!-\!16,\\
16\!-\!13,\ 16\!-\!17,\ 17\!-\!7,\ 17\!-\!8.
\end{gathered}
\]
Let \(h=\{0,\ldots,13\}\).  The displayed low word is
```text
3231320|1320320|3112213212312
```
and gives a nowhere-zero \(\mathbb F_2^3\)-flow with first support
\(h\).

Exact enumeration of the 1,024 binary cycles of \(B\) gives 1,008
extendable projections.  For \(h\) there are 15,360 ordered low-flow
extensions and zero clean extensions.  Thus \(h\) itself is
uncleanable.

## 3. The strict lock

Let \(S\) be the simple bridgeless cubic graph with canonical graph6
encoding
```text
Q???C@?K?WEOM?_aGo?I__W@G_?
```
and edge order
\[
\begin{split}
&(0,7),(1,8),(2,9),(3,9),(4,10),(5,10),(2,11),(3,11),
(6,11),\\
&(2,12),(3,12),(4,12),(0,13),(6,13),(10,13),(1,14),
(5,14),\\
&(6,14),(5,15),(7,15),(9,15),(0,16),(7,16),(8,16),
(1,17),(4,17),(8,17).
\end{split}
\]
Distinguish \(e_\ast=5=(5,10)\).

For \(b\in\{0,1\}\), let \(a_b(e_\ast)\) be the minimum size of the
first-coordinate projection of a nowhere-zero
\(\mathbb F_2^3\)-flow on \(S\), conditional on the first bit of
\(e_\ast\) being \(b\).  Enumerating the 1,024 binary cycles and all
70,780 two-low-cycle missing sets gives
\[
                           a_0(e_\ast)=7,\qquad
                           a_1(e_\ast)=5.                 \tag{1}
\]
The minimum support through \(e_\ast\) is unique:
\[
                         \{5,13,14,16,17\}.               \tag{2}
\]
It is the 5-cycle
\[
                         5-10-13-6-14-5.
\]
One literal full flow attaining (2), in the displayed edge order, is
\[
\begin{split}
(&4,6,2,6,4,5,4,2,6,6,4,2,2,3,1,2,7,5,2,6,4,6,2,4,4,6,2).
\end{split}                                               \tag{3}
\]
Here the distinguished value is \((1,2)\in\mathbb F_2\times K\).
For any desired odd terminal value \((1,t)\), the invertible linear map
\[
                 \Phi_t(x,\ell)=(x,\ell+x(2+t))
\]
preserves the first coordinate and sends \((1,2)\) to \((1,t)\).
Applying \(\Phi_t\) to (3) therefore gives the same projected support
with any prescribed odd terminal value.  This is the literal lift used
on the eight differently coloured base edges.

Delete \(e_\ast\), attach one external link at each of its endpoints,
and count projected edges in the inserted replacement.  If the common
terminal first bit is zero, its contribution is at least \(a_0=7\).
If it is one, deleting \(e_\ast\) subtracts one projected edge and the
two terminal links add two, so its contribution is at least
\(a_1+1=6\).  Thus
\[
                              w_0=7>w_1=6.                \tag{4}
\]
The unique odd minimum is the 4-edge path obtained from (2), together
with the two links, so its projected replacement is a unique 6-edge
path.

## 4. Exact lock-placement minimum

For \(L\subseteq h\), replace exactly the base edges in \(L\) by fresh
copies of the lock.  Leave every other base edge unchanged.  The target
cost is
\[
                              14+5|L|.                    \tag{5}
\]
For another extendable base projection \(k\), its cost minus (5) is
\[
 |L\cap(h-k)|-| (h-L)\cap(h-k)|+|k-h|.                   \tag{6}
\]
The terms are, respectively, omitted locked target edges, omitted
unlocked target edges, and added complement edges.

The checker tests (6) against all 1,008 extendable base projections for
all \(2^{14}\) sets \(L\).  Exactly 2,280 placements make \(h\) uniquely
optimal.  Their minimum size is eight, with 180 minimizers.  Choose
\[
                         L=\{0,2,3,4,7,8,9,10\}.          \tag{7}
\]
The minimum strict gap in (6) is one.

The resulting graph has
\[
 |V(G)|=18+8\cdot18=162,\qquad
 |E(G)|=27+8\cdot27=243.                                 \tag{8}
\]
It is simple and cubic by inspection of the two-pole substitution.
It is connected and bridgeless because both \(B\) and \(S\) are
bridgeless and both terminal vertices remain joined inside and outside
each substituted pole.  The checker also deletes every edge and tests
connectivity directly.  Since \(B\) is a minor of \(G\) and is
nonplanar, \(G\) is nonplanar.  The checker verifies in \(B\) the
\(K_{3,3}\)-subdivision with branch bipartition
\(\{2,10,16\}\mid\{3,9,12\}\) and paths
\[
\begin{gathered}
2\!-\!3,\ 2\!-\!1\!-\!9,\ 2\!-\!12,\quad
10\!-\!3,\ 10\!-\!9,\ 10\!-\!11\!-\!12,\\
16\!-\!15\!-\!14\!-\!4\!-\!3,\quad
16\!-\!17\!-\!8\!-\!9,\quad
16\!-\!13\!-\!12.
\end{gathered}
\]
Contracting every inserted pole recovers \(B\).

## 5. Exact and unique global minimum

Contract an arbitrary nowhere-zero flow on \(G\) through every inserted
two-pole.  Summing conservation over a pole says its two nonzero
terminal-link values are equal.  Restoring \(e_\ast\) with that value
gives a nowhere-zero flow on \(S\), while contracting all poles gives a
nowhere-zero flow on \(B\).

Equation (4) therefore bounds every pole contribution and (6) bounds
the whole projection.  The transformed copies of (3) lift the displayed
base flow and attain cost
\[
                              14+5\cdot8=54.              \tag{9}
\]
Consequently \(\mu(G)=54\).  Equality in (6) forces the contracted
support to equal \(h\).  Equality in every local bound then forces the
unique local support (2).  Hence the 54-edge projection \(H\) is unique.
It expands each base 7-circuit to a 27-circuit.

## 6. Every extension of the minimum is unclean

Delete \(H\).  The components containing the original base vertices
induce exactly the five components of \(B-h\); their labels on vertices
\(0,\ldots,13\) are
```text
01234444413024
```
The eight pole interiors give eight additional components.

Take any extension of \(H\) and contract the poles.  Its terminal values
give an extension of \(h\) on \(B\).  On each of the five old
components, the support-cut colours are unchanged: every old support
edge has merely been replaced by a support path whose endpoint links
carry the contracted value.  Thus a clean extension of \(H\) would
contract to a clean extension of \(h\).  The exact base enumeration in
Section 2 shows that none exists.  Therefore every extension of the
unique global minimum \(H\) is unclean.

## 7. The graph nevertheless has a FiveCDC

Each line of `fivecdc-certificates.txt` labels every edge by a two-subset
of \(\{0,1,2,3,4\}\).  Reading coordinate \(i\) gives one Eulerian
edge-subset, and every edge occurs in exactly two coordinates.

The compositional certificate is human-readable.  Start with the
27-edge certificates for \(B\) and \(S\).  For a replaced base edge
whose pair is \(P\), permute the five coordinates of the closure
certificate so that the pair on \(e_\ast\) becomes \(P\).  Delete the
two old edges and label both terminal links by \(P\).  At every affected
vertex, the removed incidence is replaced by the same pair, so all five
parities remain even.  Exact-two coverage is literal on every new edge.
Doing this independently for the eight locks produces the frozen
243-pair `COMPOSITIONAL` row.

The `DIRECT_SAT` row was generated separately from the mandatory
encoding
\[
 \sum_{i=0}^4x_{e,i}=2\quad(e\in E),\qquad
 \sum_{e\ni v}x_{e,i}=0\pmod2\quad(v\in V,\ 0\le i<5).
\]
The corrected solver used a nested three-input XOR.  An earlier malformed
Python call to a binary `Xor` API was discarded and contributes no data
to this package.  The checker verifies both final rows directly, without
using a SAT solver.

Thus the graph has a FiveCDC even though its unique globally minimum
extendable projection is not cleanable.  Global minimum alone cannot
select the required cover.
