# A clean-or-delete theorem through support sixteen

Date: 2026-07-29

Status: **EXACT SPECIAL-CASE THEOREM / HUMAN REDUCTION PLUS FINITE
CHECK / NOT A FIVECDC RESOLUTION**.

Let \(K=\mathbb F_2^2\).  Consider a two-occurrence boundary state:
the support is a disjoint union of circuits, and every component of the
complement meets the support in exactly two occurrences.  Its interaction
multigraph \(J\) has one vertex for each support circuit and one edge for
each complement component.  In this note \(J\) is assumed loopless.

As proved in the earlier interaction-flow dictionary, feasible images of
the component derivatives are exactly the nowhere-zero \(K\)-flows
\[
                 t:E(J)\longrightarrow K-\{0\}.
\]
Integrating \(t\) in the cyclic order at every vertex gives a closed walk
on the four points of \(K\).  A flow **deletes** when one of these walks
omits a point.  It is **clean** when translations of the vertex walks can
make the two occurrences of every interaction edge traverse the same
unoriented edge of the \(K_4\) on \(K\).

We prove:

> **Theorem.**  Every loopless two-occurrence state of total support at
> most \(16\) that admits a feasible flow admits a flow that is clean or
> deletes a support circuit.  Consequently, if the state comes from a
> cardinality-minimum extendable projection, it is clean.

The final sentence uses only strict minimality: a deleting flow is an
extension in which some support circuit omits a low colour, so the standard
circuit toggle removes that whole circuit and produces a strictly smaller
extendable projection.

## 1. Elementary reductions

The total support is
\[
                         \sum_{v\in V(J)}d(v)=2|E(J)|.
\]

If every degree of \(J\) is even, assign one fixed
\(a\in K-\{0\}\) to every edge.  This is a flow.  Every integrated local
walk alternates between two points, so it deletes.

If a vertex has degree at most three, every feasible local walk uses at
most three points.  Degrees zero, two, and three are immediate from the
number of prefixes.  Degree one cannot occur in a nowhere-zero flow.
Thus any feasible flow already deletes at that vertex.

Disconnected interaction graphs can be treated component by component.
Choose a clean-or-delete flow independently on each component.  If one
component deletes, the combined flow deletes; otherwise all components
clean, and their translations combine.

A connected loopless interaction graph on two vertices consists of \(m\)
parallel edges.  It always has a deleting flow:

- if \(m\) is even, give every edge the same value \(a\);
- if \(m\ge3\) is odd, choose two consecutive edges in the cyclic order
  at the first vertex, give them distinct values \(b,c\), and give every
  other edge \(a=b+c\).

For odd \(m\), the xor at both vertices is
\(b+c+(m-2)a=b+c+a=0\).  Starting immediately before the two selected
edges, the first walk has prefixes \(0,b,a\) and then alternates between
\(a\) and \(0\); it omits \(c\).  (The case \(m=1\) has no nowhere-zero
flow.)

If a connected three-vertex interaction graph is a path, the flow
condition at each leaf says that the xor on its parallel-edge bundle is
zero.  Apply the preceding construction independently to the two bundles.
Their xors also cancel at the middle vertex, and a leaf walk deletes.
Thus only a triangle with positive edge multiplicities remains.

## 2. The only finite cases

Suppose no elementary reduction applies.  Then \(J\) is connected,
has at least three vertices, has minimum degree at least four, and is not
Eulerian.

If the total support is at most \(16\), \(J\) has at most four vertices.
Four vertices force degree sequence \((4,4,4,4)\), which is Eulerian.
For three vertices, the only non-Eulerian degree sequences are
\[
        (5,5,4),\qquad (6,5,5),\qquad (7,5,4).
\]
Writing the multiplicities on \(01,02,12\), respectively, these are
\[
        (3,2,2),\qquad (3,3,2),\qquad (4,3,1).
\]

There are therefore exactly three finite profiles to check.

## 3. Exact finite check

For each profile, `search_three_vertex.py`:

1. labels all interaction edges;
2. enumerates every cyclic order at each vertex modulo rotation and
   reversal;
3. enumerates every assignment in \(\{1,2,3\}^{E(J)}\) and retains
   exactly those satisfying the xor flow equation at every vertex;
4. integrates the three closed walks;
5. exhausts all \(4^2\) relative translations and tests the literal
   clean equations; and
6. tests whether any local walk uses fewer than four points.

The complete counts are:

| multiplicities | degrees | rotation states | feasible flows | states with a clean flow | delete-only states | no-go states |
|---|---:|---:|---:|---:|---:|---:|
| \((3,2,2)\) | \((5,5,4)\) | 432 | 138 | 432 | 0 | 0 |
| \((3,3,2)\) | \((6,5,5)\) | 8,640 | 402 | 8,640 | 0 | 0 |
| \((4,3,1)\) | \((7,5,4)\) | 12,960 | 420 | 12,744 | 216 | 0 |

The independent checker does not use the alternating-form clean equation.
It constructs the two literal endpoint sets in \(K\) for every occurrence
and compares those two-element sets directly.  It regenerates the same
rotation representatives, flow totals, clean/delete partition, and
goal-count histogram for all three profiles.

This exhausts the reduction and proves the theorem.

## 4. Scope

The theorem excludes only loopless interaction multigraphs.  A loop in
\(J\) represents two occurrences of one complement component on the same
support circuit and is not covered by the three-profile reduction.

The theorem strengthens the exact frontier only in the two-occurrence
subclass at support size \(16\).  The general minimum-projection theorem
through size \(15\) allows arbitrary complement-component occurrence
counts; its size-\(16\) case remains open.  Nothing here proves or
disproves the Five-Cycle Double Cover Conjecture.

OpenAI Codex agents under Atharva Vaidya's direction found the reduction,
wrote the proof and programs, and performed the machine checks.  The work
has not received independent human peer review.
