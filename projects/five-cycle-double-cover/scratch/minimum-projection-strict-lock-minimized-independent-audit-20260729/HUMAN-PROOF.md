# A globally minimum dirty projection in a graph that still has FiveCDC

## 1. The strict two-pole

Let \(S\) be the cubic graph whose ordered edge list is the constant
`CLOSURE_EDGES` in `verify.py`, and distinguish
\[
                         e_*=e_5=5\,10.
\]
For \(b\in\{0,1\}\), let \(a_b\) be the minimum size of the first
coordinate of a nowhere-zero \(\mathbb F_2^3\)-flow on \(S\), subject
to the first coordinate of \(e_*\) being \(b\).

The binary cycle space of \(S\) has dimension ten.  A binary cycle
\(h\) is extendable precisely when two further binary cycles \(p,q\)
satisfy
\[
                           h\cup p\cup q=E(S).             \tag{1}
\]
Exhausting the 1,024 cycles and the \(1,024^2\) ordered pairs gives
\[
                            a_0=7,\qquad a_1=5.            \tag{2}
\]
There are nine \(a_0\)-minimum supports, with 6,336 ordered extensions
in total.  The \(a_1\)-minimum support is uniquely
\[
                         \{5,13,14,16,17\},               \tag{3}
\]
and has 240 ordered extensions.

For completeness, the nine tied \(a_0\)-minimum supports and their
ordered-extension counts are

```text
{4,12,14,21,23,25,26}       960
{4,7,8,10,11,13,14}         480
{4,6,8,9,11,13,14}          480
{1,12,13,15,17,21,23}       960
{0,12,13,16,17,18,19}       768
{3,7,8,16,17,18,20}         480
{2,6,8,16,17,18,20}         480
{1,15,16,18,19,22,23}       960
{4,13,14,15,17,24,25}       768
```

Delete \(e_*\) and attach one new terminal link at each exposed
endpoint.  If the terminal first bit is zero, the replacement cost is
\(w_0=a_0=7\).  If it is one, deleting \(e_*\) removes one projected
edge and the two links add two, so
\[
                         w_1=a_1+1=6.                     \tag{4}
\]
This is a strict parity lock.

## 2. Exact minimization of the lock set

Let \(B\) be the ordered 18-vertex base graph in `BASE_EDGES`, and let
\[
                              T=\{0,\ldots,13\}
\]
be its two displayed 7-circuits.  Its binary cycle space also has
dimension ten.  Exact use of (1) gives 1,008 extendable terminal
supports.

Choose \(L\subseteq T\) and replace exactly the edges in \(L\) by the
strict two-pole.  Leave the other base edges unchanged.  The cost of
the target terminal support \(T\) is
\[
                              14+5|L|.                    \tag{5}
\]
For another extendable terminal support \(H\), put
\[
                    O=T-H,\qquad A=H-T.
\]
Relative to (5), its local lower bound is
\[
 \Delta_L(H)
     =|O\cap L|-|O-L|+|A|
     =2|O\cap L|-|O|+|A|.                                \tag{6}
\]

The checker exhausts all 16,384 subsets \(L\) against all 1,007
competitors.  No set of size at most seven makes every value in (6)
positive.  Exactly 180 sets of size eight do.  We use
\[
                       L=\{0,2,3,4,7,8,9,10\},            \tag{7}
\]
for which
\[
                         \min_{H\ne T}\Delta_L(H)=1.       \tag{8}
\]

## 3. The 162-vertex graph and its unique minimum

Apply the eight substitutions (7), using disjoint fresh copies of
\(S-e_*\).  The resulting graph \(G\) has
\[
                         |V(G)|=18+18\cdot8=162,
 \qquad |E(G)|=243.                                      \tag{9}
\]
Direct adjacency checks prove that it is simple and cubic.  Deleting
each edge in turn leaves it connected, so it is bridgeless.

Any nowhere-zero flow on \(G\) contracts through every two-pole:
summing conservation over the internal vertices says that its two
nonzero terminal values are equal.  It therefore induces a
nowhere-zero flow on \(B\).  Equations (4) and (6) give a lower bound
of 54, with equality possible only at terminal support \(T\).

The target lift exists.  On every locked edge use the unique local
support (3), delete edge 5, and add the two projected terminal links.
On every unlocked target edge retain the edge.  This gives
\[
                            6\cdot8+6=54                 \tag{10}
\]
projected edges.  The checker constructs a literal nowhere-zero
three-bit flow realizing it.

Equality in the contraction bound forces the terminal support to be
\(T\), and equality in each local bound forces the unique support
(3).  Hence the size-54 support itself is the unique globally minimum
support.  It is the disjoint union of two 27-circuits.

## 4. Why the minimum projection is uncleanable

The base support \(T\) has exactly 15,360 ordered low-coordinate
extensions and none is clean.  This is independently regenerated from
the 1,024-element base cycle space.

Suppose the lifted size-54 support had a clean extension.  Contract each
two-pole.  Its two terminal links have equal low value.  In \(G-H\),
each gadget interior is its own component.  For every old complement
component, the two link contributions replacing a base support edge
are therefore exactly the two contributions of the contracted edge.
If both endpoints lie in the same old component, the equal
contributions cancel; otherwise one appears at each endpoint
component.  Thus cleanliness upstairs implies cleanliness of the
contracted base extension, contradicting the exact base calculation.

The unique global minimum is therefore uncleanable.  This refutes the
minimum-projection selection conjecture used in the attempted proof
route.

## 5. Why this is not a FiveCDC counterexample

For a cubic graph, label each edge by the two indices of the five
Eulerian subgraphs that contain it.  The mandatory formula is
\[
 \sum_{i=0}^4x_{e,i}=2,\qquad
 \sum_{e\ni v}x_{e,i}=0\pmod2.                           \tag{11}
\]
At a cubic vertex the three two-subset labels are precisely the three
edges of a triangle on three of the five indices.

`fivecdc-direct-labels.txt` is a literal satisfying assignment of
(11) for all 243 edges.  The checker also expands (11) to ordinary
CNF: five four-positive clauses and ten three-negative clauses enforce
exactly two variables on each edge, while four clauses encode each
degree-three even-parity row.  There are
\[
                         1,215\text{ variables},\qquad
                         6,885\text{ clauses}.            \tag{12}
\]

There is a shorter compositional proof.  Fix FiveCDC pair-labelings of
the base \(B\) and closure \(S\).  For a replaced base edge, permute the
five indices on its copy of \(S\) so that the label on \(e_*\) equals
the base-edge label.  Delete both matched edges and give each new link
that common label.  At each of the four exposed endpoints a like-labelled
edge has merely been replaced by a like-labelled link, so all five
parities are unchanged.  Repeating independently for all eight locks
constructs a FiveCDC of \(G\).

Consequently this graph separates two statements:

- “a globally minimum projection is cleanable” is false;
- FiveCDC still holds for this graph.

No UNSAT claim or FiveCDC disproof is made.
