# A full-boundary Heawood four-pole for standard FiveCDC

Date: 2026-07-28

Status: **human-checkable finite boundary theorem and non-covering
substitution reduction; not a resolution of FiveCDC**.

## 1. Pair-label convention

Put
\[
                 D_5=\binom{\{0,1,2,3,4\}}2\subseteq\mathbb F_2^5.
\]
A standard five-cycle double cover is equivalently a label in \(D_5\) on
each edge such that the xor of the incident labels is zero at every vertex.
The five coordinate supports are then Eulerian, and every edge belongs to
exactly two supports.  At a cubic vertex the three labels are the three
edges of a triangle in \(K_5\).

For an ordered four-pole, summing all internal vertex equations shows that
every realizable boundary word \((A_0,A_1,A_2,A_3)\) satisfies
\[
                         A_0+A_1+A_2+A_3=0.             \tag{1}
\]

## 2. The pole

Take the Heawood graph and delete the adjacent vertices \(0,1\) in the
standard NetworkX labelling, then relabel the remaining vertices in
increasing order.  The resulting proper four-pole has graph6 encoding

```text
KhEGHC@AI?_P
```

Its ordered ports are
\[
                         (0,3,8,11),
\]
and its ordered proper edges are
\[
\begin{split}
 &(0,1),(1,2),(2,3),(3,4),(0,5),(4,5),(5,6),(2,7),\\
 &(6,7),(7,8),(4,9),(8,9),(1,10),(9,10),(6,11),(10,11).
\end{split}                                                \tag{2}
\]
The table itself makes the graph definition independent of NetworkX.  A
direct graph check shows that the core is simple, connected, bridgeless,
and has girth six.  Thus this is not the Petersen four-pole, is not a graph
covering construction, and does not introduce an internal triangle,
quadrilateral, or pentagon.

## 3. Full-boundary theorem

> **Theorem.**  For every \(A_0,A_1,A_2,A_3\in D_5\) satisfying (1), the
> Heawood four-pole (2) has a \(D_5\)-labelling with those ordered boundary
> labels.

There are \(640\) ordered words satisfying (1).  Under a simultaneous
permutation of the five coordinates, they form ten orbits.  Representatives
and one extension on the sixteen edges in the order (2) are:

| type | port labels | proper-edge labels |
|---|---|---|
| `AA` | `02 02 02 02` | `01 02 01 12 12 02 01 12 02 01 01 12 12 02 12 01` |
| `AT2` | `02 02 03 03` | `01 02 03 23 12 02 01 23 03 02 03 23 12 02 13 01` |
| `AT3` | `02 03 02 03` | `01 02 04 34 12 14 24 24 34 23 13 03 12 01 23 02` |
| `AT4` | `02 03 03 02` | `01 02 01 13 12 01 02 12 01 02 03 23 12 02 12 01` |
| `T2T2` | `02 02 13 13` | `01 02 01 12 12 02 01 12 02 01 01 03 12 13 12 23` |
| `T2T3` | `02 03 12 13` | `01 02 01 13 12 01 02 12 01 02 03 01 12 13 12 23` |
| `T2T4` | `02 03 13 12` | `01 02 04 34 12 13 23 24 12 14 14 34 12 13 13 23` |
| `T3T3` | `02 13 02 13` | `01 02 01 03 12 02 01 12 02 01 23 12 12 13 12 23` |
| `T3T4` | `02 13 03 12` | `01 02 03 01 12 02 01 23 03 02 12 23 12 13 13 23` |
| `T4T4` | `02 13 13 02` | `01 02 01 03 12 01 02 12 24 14 13 34 12 14 04 24` |

Every displayed label has weight two.  Appending the four port labels at
vertices \(0,3,8,11\), respectively, the xor of the three labels at every
vertex is zero.  This is a row-by-row human check against (2).

For completeness of the table, regard the four boundary labels as four
ordered edges of a loopless multigraph on the five coordinate vertices.
Condition (1) says every coordinate vertex has even degree.  Relabelling
the five vertices gives exactly the ten displayed ordered-edge orbits.
Alternatively, the companion standard-library checker enumerates all
\(10^4\) words, retains the 640 satisfying (1), and verifies that the
\(120\) coordinate permutations of the ten rows cover them exactly.
Applying the same coordinate permutation to the associated internal row
preserves weight and xor.  Therefore every word satisfying (1) extends,
which proves the theorem.

## 4. Non-covering substitution reduction

Let \(G\) be a cubic graph with a standard FiveCDC, and let
\[
                    e=ab,\qquad f=cd
\]
be independent edges.  Let
\[
             \pi:\{a,b,c,d\}\longrightarrow\{0,3,8,11\}
\]
be an arbitrary bijection.  Delete \(e,f\), take a fresh copy of the
Heawood four-pole, and add the four edges
\[
                         z\pi(z)\qquad(z\in\{a,b,c,d\}).
\]
There is no restriction relating \(\pi(a),\pi(b)\) or
\(\pi(c),\pi(d)\); all \(4!\) port bijections are allowed.

If the old labels of \(e,f\) are \(q,r\), label \(a\pi(a),b\pi(b)\) by
\(q\), and \(c\pi(c),d\pi(d)\) by \(r\).  In the frozen port order
\((0,3,8,11)\), this is some permutation of \((q,q,r,r)\).  Its xor is
zero, so the full-boundary theorem extends it through the pole.  Every old
vertex retains its former parity equation.  Hence:

> **Corollary (Heawood insertion).**  Every such Heawood four-pole
> substitution in a FiveCDC-positive cubic graph is FiveCDC-positive, for
> every port bijection.

The operation adds twelve vertices rather than eight, has a girth-six
proper core rather than the Petersen core, and is not a lift or covering.
If \(G\) is simple and the two edges are independent, the output is simple.

> **Bridgelessness lemma.**  If \(G\) is connected and bridgeless, every
> graph produced by the arbitrary-port construction above is connected and
> bridgeless.

**Proof.**  Write \(H=G-\{e,f\}\).  Every component of \(H\) contains at
least two of the four exposed endpoints: a component containing exactly
one would have a one-edge boundary in \(G\), making that edge a bridge.
Attaching every component to the connected pole therefore makes the output
connected.

It remains to put every edge on a circuit.  Every proper pole edge already
lies on a circuit inside the pole; this is independently checked from (2).
For a joining edge \(z\pi(z)\), choose another exposed endpoint \(z'\) in
the same component of \(H\).  A path from \(z\) to \(z'\) inside that
component, the joining edge at \(z'\), and a path in the connected pole
from \(\pi(z')\) to \(\pi(z)\) close a circuit through \(z\pi(z)\).

Finally let \(g\) be an old edge of \(H\).  If \(g\) is not a bridge of its
component of \(H\), it already lies on an \(H\)-circuit.  Otherwise, deleting
\(g\) splits that component into shores \(X,Y\).  Each shore contains an
exposed endpoint: if, say, \(X\) did not, then
\(\delta_G(X)=\{g\}\), contrary to bridgelessness of \(G\).  Join an exposed
endpoint in \(X\) to one in \(Y\) through the connected pole and use paths
inside \(X,Y\) to the two ends of \(g\).  This closes a circuit through
\(g\).  Thus every output edge is on a circuit, so the output is
bridgeless. \(\square\)

Equivalently, if a cubic graph is obtained by this insertion and is a
FiveCDC counterexample, then the smaller graph obtained by replacing the
pole with the two original independent edges must already be a
counterexample.  This is a sound pruning reduction for minimal
counterexamples.  It does not say that every four-pole is full and does
not resolve the conjecture.

## 5. Replay and limitations

Run:

```sh
python3 scratch/verify_heawood_four_pole_full_boundary_20260728.py
```

The checker uses only the Python standard library.  It independently parses
the graph6 record, checks the frozen edge table and simple/connected/
bridgeless/girth metadata, verifies all displayed vertex equations, and
exhausts the boundary orbit coverage.
Positive finite certificates do not require SAT or an UNSAT proof trace.

The theorem concerns the standard Eulerian-subgraph formulation only.
Nothing here gives the opposite-direction traversal condition of an
orientable five-cycle double cover.  No literature-novelty claim should be
made without comparison by a graph-theory specialist.

## AI-use disclosure

OpenAI Codex agents, under human direction, selected the non-covering pole,
found the finite labels, wrote the independent checker, and drafted this
proof.  The full certificate is exposed for human checking.  AI assistance
is not independent peer review.
