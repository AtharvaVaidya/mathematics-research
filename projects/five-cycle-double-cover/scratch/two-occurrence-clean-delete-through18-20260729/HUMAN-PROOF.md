# A clean-or-delete theorem through support eighteen

Date: 2026-07-29

Status: **HUMAN-READABLE REDUCTION PLUS TWO EXACT FINITE CHECKS / NOT A
FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. Statement

Put \(K=\mathbb F_2^2\).  A two-occurrence boundary state consists of a
disjoint union of support circuits and complement components, each of
which has exactly two boundary occurrences.  Contract every support
circuit to a vertex and every complement component to an interaction
edge.  We assume the resulting interaction multigraph \(J\) is loopless;
parallel edges are allowed.

The cyclic order of the incident interaction edges at a vertex is the
order of their occurrences around its support circuit.  A feasible
component-map image is a nowhere-zero \(K\)-flow
\[
                 t:E(J)\longrightarrow K-\{0\}.              \tag{1}
\]
Integrating the increments \(t_e\) in the cyclic order at each vertex
gives a closed walk on the four points of \(K\).

The flow **deletes** if some local walk omits a point of \(K\).  It is
**clean** if translations of the local walks make the two occurrences
of every interaction edge traverse the same unoriented edge of the
complete graph on \(K\).

We prove:

> **Theorem.** Every flowable loopless two-occurrence interaction state
> of total support at most \(18\) has a feasible flow which cleans or
> deletes.

If the state is induced by a globally cardinality-minimum extendable
projection, deletion is impossible: translating the deleting walk so
that its omitted point is the toggle colour and adding the corresponding
three-bit flow around that support circuit removes the whole circuit
without producing a zero edge.  The theorem therefore implies:

> **Corollary.** Every globally cardinality-minimum extendable projection
> in the loopless two-occurrence subclass with support at most \(18\) is
> cleanable.

The standard Fano-projection theorem identifies existence of a cleanable
projection in a cubic graph with the standard FiveCDC conclusion.  The
corollary is only a bounded conditional case and does not control the
minimum support in arbitrary graphs.

## 2. Interaction-flow and cleaning dictionaries

Let component \(e\) meet support circuits at occurrences \(p,q\).
Component charge says that their transformed derivatives agree; call
the common nonzero value \(t_e\).  The derivative xor around every
support circuit is zero, so
\[
                        \bigoplus_{e\ni v}t_e=0               \tag{2}
\]
at every interaction vertex.  Conversely, (2) integrates around every
support circuit, and a member of
\(\operatorname{GL}(2,2)\) on each complement component can send its
original nonzero derivative to any prescribed nonzero value.  Thus (1)
is exact.

If \(p_{v,e}\) is the integrated point immediately before occurrence
\((v,e)\), that occurrence traverses
\[
                         \{p_{v,e},p_{v,e}+t_e\}.              \tag{3}
\]
After translating the walk at \(v\) by \(x_v\), the two endpoint sets in
(3) agree exactly when
\[
 B(x_u+x_v,t_e)=B(p_{u,e}+p_{v,e},t_e),                       \tag{4}
\]
where \(B((a_1,a_2),(b_1,b_2))=a_1b_2+a_2b_1\).
The primary checker uses (4).  The independent checker forms the
two-point sets (3) literally.

## 3. Elementary reductions

The total support is
\[
                         \sum_{v\in V(J)}d(v)=2|E(J)|.         \tag{5}
\]

If all degrees are even, putting one fixed nonzero value on every edge
is a flow.  Every local walk alternates between two points and deletes.

If a vertex has degree at most three, every feasible local walk visits
at most three prefix points and therefore deletes.  Degree one cannot
occur in a nowhere-zero flow.

Disconnected interaction graphs are handled componentwise.  If one
component deletes, the combined flow deletes; if every component cleans,
their translations combine to clean the whole state.

A connected loopless interaction graph on two vertices is a parallel
bundle.  For an even number of edges, give every edge one fixed nonzero
value.  For an odd number \(m\ge3\), choose two consecutive edges at one
vertex, give them distinct values \(b,c\), and give all remaining edges
\(a=b+c\).  The xor is zero at both vertices, and the selected vertex
walk visits only \(0,b,a\), then alternates between \(a\) and \(0\).
It omits \(c\) and deletes.  A one-edge bundle is not flowable.

If a connected three-vertex graph is a path of parallel bundles, flow
conservation makes the xor on each leaf bundle zero.  Apply the preceding
bundle construction independently; a leaf walk deletes.  Thus the only
three-vertex cases needing enumeration are positive-multiplicity
triangles.

We may now assume that \(J\) is connected, loopless, non-Eulerian, has
minimum degree at least four, and has at least three vertices.

## 4. Exhaustive shapes

At support \(18\), (5) and minimum degree four give
\(|V(J)|\le4\).

### Three vertices

Write the three positive triangle multiplicities as \(a,b,c\).  They
sum to nine.  Up to permutation their positive integer partitions are
\[
\begin{array}{c|c}
(a,b,c)&\text{reduction}\\ \hline
(7,1,1)&\text{a degree-two vertex}\\
(6,2,1)&\text{a degree-three vertex}\\
(5,3,1)&\text{all degrees even}\\
(5,2,2)&\text{finite case}\\
(4,4,1)&\text{finite case}\\
(4,3,2)&\text{finite case}\\
(3,3,3)&\text{all degrees even}.
\end{array}
\]

The earlier even layers leave the three additional finite profiles
\((3,2,2),(3,3,2),(4,3,1)\).  The new programs recheck them rather than
importing their old output.

### Four vertices

The four degrees sum to \(18\).  If they are not all even and are each
at least four, their multiset must be
\[
                              (5,5,4,4).                       \tag{6}
\]
Write the multiplicities on
\((01,02,03,12,13,23)\).  Direct enumeration of the six nonnegative
integers, followed by all \(24\) vertex relabellings, gives exactly nine
orbits:
\[
\begin{array}{c|c}
(0,0,4,4,0,1)&\text{connected with a bridge}\\
(0,0,4,5,0,0)&\text{disconnected}\\
(0,1,3,3,1,1)&\text{finite case}\\
(0,1,3,3,2,0)&\text{finite case}\\
(0,1,3,4,1,0)&\text{finite case}\\
(0,2,2,2,2,1)&\text{finite case}\\
(0,2,2,2,3,0)&\text{finite case}\\
(1,1,2,2,1,2)&\text{finite case}\\
(1,1,2,3,1,1)&\text{finite case}.
\end{array}
\]
A bridge cannot carry a nonzero group flow, and disconnected states were
already reduced.  `enumerate_profiles.py` checks all 90 labelled
solutions of (6), their nine relabelling orbits, connectivity, and the
bridge claim.

For smaller total support, the same inequalities leave only the three
earlier triangle profiles displayed above; four vertices at support
\(16\) have degree sequence \((4,4,4,4)\) and delete by the Eulerian
reduction.  Hence the six triangle profiles and seven four-vertex
profiles form a complete finite list through support \(18\).

## 5. Exact census

For each finite profile the programs distinctly label the nine or fewer
interaction edges.  At each vertex they enumerate every cyclic order
modulo rotation and reversal.  They enumerate every assignment in
\(\{1,2,3\}^{E(J)}\), retaining exactly the assignments satisfying (2).

Both programs fix the value of edge zero to \(1\).  This is exact:
\(\operatorname{GL}(2,2)\) is transitive on the three nonzero values, so
every flow has a global linear image with that value, while both
cleanliness and deletion are invariant under a global linear map.

The primary program integrates each flow, exhausts every relative
circuit translation with the first translation fixed to zero, and tests
(4).  The audit independently represents a \(K_4\) edge by the four-bit
mask of its two endpoints and compares literal masks.

The complete results are:

| profile | states | clean | delete-only | residual |
|---|---:|---:|---:|---:|
| \(T(3,2,2)\) | 432 | 432 | 0 | 0 |
| \(T(3,3,2)\) | 8,640 | 8,640 | 0 | 0 |
| \(T(4,3,1)\) | 12,960 | 12,744 | 216 | 0 |
| \(T(5,2,2)\) | 388,800 | 388,800 | 0 | 0 |
| \(T(4,4,1)\) | 362,880 | 356,256 | 6,624 | 0 |
| \(T(4,3,2)\) | 259,200 | 259,200 | 0 | 0 |
| \(Q(0,1,3,3,1,1)\) | 1,296 | 1,296 | 0 | 0 |
| \(Q(0,1,3,3,2,0)\) | 1,296 | 1,296 | 0 | 0 |
| \(Q(0,1,3,4,1,0)\) | 1,296 | 1,188 | 108 | 0 |
| \(Q(0,2,2,2,2,1)\) | 1,296 | 1,296 | 0 | 0 |
| \(Q(0,2,2,2,3,0)\) | 1,296 | 1,296 | 0 | 0 |
| \(Q(1,1,2,2,1,2)\) | 1,296 | 1,296 | 0 | 0 |
| \(Q(1,1,2,3,1,1)\) | 1,296 | 1,296 | 0 | 0 |
| **total** | **1,041,984** | **1,035,036** | **6,948** | **0** |

Every finite state therefore has one of the two claimed outcomes.
Together with Sections 3 and 4, this proves the theorem.

## 6. Trust boundary and scope

The shape reduction and the implication “clean or delete implies a
minimum state is clean” are ordinary human mathematics.  The
classification of the 1,041,984 rotation states is computer-assisted.
The exact state totals and per-state summaries are frozen as assertions
in both programs, and the primary program additionally freezes a
64-bit FNV-1a-style stream digest for every profile.  (Its offset basis is
project-specific, so the digest is not claimed to be standard FNV-1a.)

This result does not cover:

- interaction loops (both occurrences of a complement component on one
  support circuit);
- complement components with other than two occurrences;
- minimum projections of support greater than \(18\); or
- the orientable FiveCDC variant.

Thus it is partial structural progress on a direct route to standard
FiveCDC, not a proof or disproof of the conjecture.

OpenAI Codex agents under Atharva Vaidya's direction derived and checked
this result.  No independent human review or literature-priority claim
is made.
