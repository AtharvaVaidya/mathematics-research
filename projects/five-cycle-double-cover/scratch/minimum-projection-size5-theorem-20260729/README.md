# Minimum extendable projections through size five

Date: 2026-07-29

Status: **HUMAN-CHECKABLE PARTIAL THEOREM / NOT A FIVE-CYCLE-DOUBLE-COVER
RESOLUTION**.

## Statement

Let \(G\) be a finite connected bridgeless loopless cubic graph.  Parallel
edges are allowed.  A binary cycle is an Eulerian edge set.  Call a binary
cycle \(h\) **extendable** if there are binary cycles \(p,q\) for which
\[
                         E(G)-h\subseteq p\cup q.          \tag{1}
\]
Equivalently, \((h,p,q)\) is a nowhere-zero
\(\mathbb F_2^3\)-flow.

For an extension \(f=(h,s)\), with
\(s:E(G)\to K=\mathbb F_2^2\), put
\[
                         M_c=\{e\in h:s(e)=c\}
                         \qquad(c\in K).                  \tag{2}
\]
The projection is **cleanable** if it has an extension for which every
component \(W\) of \(G-h\) satisfies
\[
                       |M_c\cap\delta(W)|\equiv0\pmod2
                       \qquad(c\in K).                    \tag{3}
\]
This is the Hušek--Šámal component condition.

> **Theorem.**  If the minimum cardinality of a nonzero extendable
> projection of a non-Tait graph \(G\) is at most five, then every
> cardinality-minimum extendable projection is cleanable.  If \(G\) is
> Tait-colourable, the zero projection is a clean minimum.

Thus every graph in the stated class whose minimum extendable-projection
size is at most five satisfies the proposed minimum-projection route.
This does not handle minimum size six or larger and does not prove
FiveCDC.

## 1. Minimum exchange input

Choose a cardinality-minimum nonzero extendable \(h\), and fix any
extension \(f=(h,s)\).  The minimum-projection exchange theorem says
that, for every \(c\in K\), \(h\) is a minimum binary cycle containing
\(M_c\).  In particular, every circuit component \(D\) of \(h\) contains
an edge of every \(M_c\): otherwise deleting \(D\) would give a smaller
binary cycle containing the omitted \(M_c\).

Since \(G\) is cubic and loopless, \(h\) is a disjoint union of ordinary
circuits, with a parallel pair allowed as a circuit of length two.
Every component has at least four edges by the preceding paragraph.
Consequently \(|h|\le5\) forces \(h\) to be one ordinary circuit \(D\)
of length four or five.

Write its vertices and edges cyclically as
\[
 v_0,e_0,v_1,e_1,\ldots,v_{n-1},e_{n-1},v_0,
 \qquad e_i=v_iv_{i+1},                                  \tag{4}
\]
with subscripts modulo \(n\), and write \(c_i=s(e_i)\).
Adjacent colours are distinct.  Indeed, \(c_{i-1}=c_i\) would make the
third edge at \(v_i\) have low value zero, contradicting the
nowhere-zero condition outside \(h\).

## 2. Dirty-component classification

Put \(K_0=G-h\).  Every component of \(K_0\) contains at least one
vertex of \(D\), since \(G\) is connected.  For a component \(W\), sum
the full flow over its cut.  The four parities
\[
                   |M_c\cap\delta(W)|\pmod2,\qquad c\in K, \tag{5}
\]
are equal.  Call \(W\) dirty when they are all one.

### Four-cycle

The four colours occur once each.  If \(W\) is dirty, every edge of
\(D\) crosses \(\delta(W)\), so membership in \(W\) alternates around
\(D\).  The two \(D\)-vertices outside \(W\) cannot lie in separate
\(K_0\)-components: either singleton component would see exactly two
affine colours oddly, contrary to (5).  Hence \(K_0\) has exactly two
components, the two alternating vertex pairs.

### Five-cycle

The colour occurring twice cannot occur on adjacent edges.  After a
rotation and affine-colour renaming, the cyclic word is
\[
                         A,B,A,C,D.                       \tag{6}
\]
For a dirty component \(W\), put
\[
 z_i=1[v_i\in W],\qquad y_i=z_i+z_{i+1}\in\mathbb F_2.    \tag{7}
\]
Dirtiness gives
\[
              y_1=y_3=y_4=1,\qquad y_0+y_2=1.            \tag{8}
\]
Solving (8), up to replacing \(W\) by its complement, gives exactly
\[
                    \{v_2,v_4\}\quad\hbox{or}\quad
                    \{v_1,v_4\}.                         \tag{9}
\]
The total number of dirty components is even, since summing (5) over
all components counts both ends of every crossing edge.  Among the four
sets in (9) and their complements, the only dirty set disjoint from a
given one is its complement.  Thus the other dirty component contains
all remaining \(D\)-vertices.  No further \(K_0\)-component is possible,
so \(K_0\) again has exactly two components.

The script `verify.py` exhausts all proper four- and five-colour cyclic
words and all set partitions of their vertices.  It independently
recovers precisely these partitions from (5).

## 3. A dirty lift would Tait-colour \(G\)

At \(v_i\), let \(k_i\) be its unique \(K_0\)-edge and put
\[
                       d_i=s(k_i)=c_{i-1}+c_i\ne0.        \tag{10}
\]
On either of the two components of \(K_0\), applying one invertible
linear map in \(\mathrm{GL}(2,2)\) to all its edge values preserves
internal conservation and nonzeroness.  We choose the two maps
independently and then put new nonzero values \(r_i\) on the edges
\(e_i\), seeking
\[
                         r_{i-1}+r_i=g_i,                 \tag{11}
\]
where \(g_i\) is the transformed value on \(k_i\).

For \(n=4\), the opposite boundary values agree:
\[
                         d_0=d_2=x,\qquad d_1=d_3=y.
\]
Map \(x\) and \(y\), independently on the two components, to one common
nonzero value \(\alpha\).  If
\(\{\alpha,\beta,\gamma\}=K-\{0\}\), putting \(\beta,\gamma\)
alternately on \(D\) satisfies (11).

For \(n=5\), write \(x=A+B\) and \(y=A+C\).  Then
\[
                         d=(x+y,x,x,y,x).                 \tag{12}
\]
Normalize \(x=1,y=2,x+y=3\).  The two partitions in (9) have the
following explicit repairs:

| \(K_0\)-components on the \(v_i\) | transformed \(g_0,\ldots,g_4\) | \(r_0,\ldots,r_4\) |
|---|---|---|
| \(\{0,1,3\}\mid\{2,4\}\) | \(3,1,2,2,2\) | \(2,3,1,3,1\) |
| \(\{0,2,3\}\mid\{1,4\}\) | \(3,3,1,2,3\) | \(1,2,3,1,2\) |

In the first row, the three-terminal component uses the normalized
identity and the two-terminal component maps \(x\) to \(2\).  In the
second, it maps \(x\) to \(3\).  Direct substitution, cyclically with
\(r_{-1}=r_4\), verifies (11).

We have therefore assigned every edge of \(G\) a nonzero
\(\mathbb F_2^2\)-value satisfying conservation.  At a cubic vertex,
the three incident nonzero values are the three distinct nonzero group
elements, so this is a Tait colouring.

If \(G\) is non-Tait, the assumed dirty extension is impossible, and
\(h\) is cleanable.  If \(G\) is Tait-colourable, let
\(t:E(G)\to K-\{0\}\) be a nowhere-zero \(K\)-flow.  Then \((h,t)\) is
an extension of every binary projection \(h\).  Its class \(M_0\) is
empty, while the four cut parities in (5) are equal; hence all are even.
In particular, the zero projection is a clean minimum.

## Scope and disclosure

The argument assumes a connected loopless cubic graph.  Parallel edges
are harmless; a two-edge circuit cannot satisfy the four-class circuit
condition.  Disconnected bridgeless graphs may be handled componentwise,
but no such reduction is claimed here.  Loops require separate
conventions and are outside the statement.

OpenAI Codex agents under human direction derived the lemma, checked the
finite boundary classification, and prepared this report.  The displayed
proof and dependency-free checker are included for verification without
trusting an AI system.  This has not received independent human peer
review, makes no literature-wide priority claim, and does not resolve
FiveCDC.
