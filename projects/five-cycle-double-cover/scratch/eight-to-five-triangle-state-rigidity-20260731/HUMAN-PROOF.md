# Triangle-state rigidity beyond context-free pair recolouring

Date: **2026-07-31**

Status: **sharp no-go for a graph-dependent local Oum-state rule; not a
proof or disproof of FiveCDC**.

This note concerns standard Eulerian edge-subsets only.  The witness is a
finite simple bridgeless cubic graph and has an explicit FiveCDC.

## 1. Local states in the Oum/Hušek--Šámal eight-cover

Let \(W=\mathbb F_2^3\).  An Oum pair-labelled eight-cover labels every
edge by a pair \(P_e\in\binom W2\).  At a cubic vertex \(v\), the three
edge labels are the sides

\[
                           xy,\quad xz,\quad yz                \tag{1}
\]

of a three-point set

\[
                           T_v=\{x,y,z\}\subset W.             \tag{2}
\]

We call \(T_v\) the **local triangle state**.  In the flow notation, if
the incident values are \(\alpha,\beta,\gamma\) and the lifting potential
is \(t_v\), then

\[
                  T_v=\{t_v+\alpha,t_v+\beta,t_v+\gamma\}.
\]

Conversely every three-subset is a legal local state: put
\(t_v=x+y+z\), and the side \(xy\) has flow value \(x+y\).  This is the
pair form of Oum's lifting construction and Hušek--Šámal Observation 2.4.

## 2. The next rule after a context-free pair lookup

For a fixed supplied cover, a **triangle-state rule** may be chosen after
seeing the whole graph.  For every distinct state \(T\) occurring in the
cover and every side \(p\in\binom T2\), it chooses

\[
                              r_T(p)\in D_5,
        \qquad D_5=\{q\in\mathbb F_2^5:\operatorname{wt}(q)=2\}. \tag{3}
\]

It must satisfy two conditions.

1. Local parity:
   \[
                    \sum_{p\in\binom T2}r_T(p)=0              \tag{4}
   \]
   for every occurring state \(T\).
2. Edge agreement: if edge \(uv\) has old label \(p\), then
   \[
                              r_{T_u}(p)=r_{T_v}(p).            \tag{5}
   \]

Unlike a context-free pair lookup, the value on one old pair \(p\) may
depend on the whole local affine triangle \(T\).  Unlike an unrestricted
vertex rule, two vertices having the same Oum state must reuse the same
three local labels.

For a fixed old pair \(p\), form its **state-adjacency graph** \(A_p\).
Its vertices are the distinct occurring triangle states containing \(p\),
and each graph edge of the supplied cover labelled \(p\) joins its two
endpoint states in \(A_p\).  Parallel edges and loops may be discarded
when asking whether \(A_p\) is connected.

**Lemma 1 (state transport).**  If \(A_p\) is connected, edge agreement
forces \(r_T(p)\) to have one value \(r(p)\), independent of the state
\(T\) containing \(p\).

**Proof.**  Equality (5) holds across every edge of \(A_p\), and hence
propagates along its paths. \(\square\)

Thus connectedness of every \(A_p\) collapses the graph-dependent
triangle-state rule back to a pair table, but this time the collapse is a
theorem about the supplied graph rather than an assumption on the rule.

## 3. Cycle-space rigidity

Let \(S\) be six old coordinate points.  Regard the fifteen pair values
\(r(p)\) as an edge cochain on \(K_S\).  Each equation (4) says that the
cochain sums to zero on one triangle of \(K_S\).

The binary cycle space of \(K_6\) has dimension

\[
                              15-6+1=10.                       \tag{6}
\]

If the incidence rows of the distinct occurring triangle states have
rank ten, they span this cycle space.  Coordinate by coordinate, a
cochain orthogonal to the cycle space lies in the cut space.  Therefore
there are words \(a_x\in\mathbb F_2^5\), unique up to a common translate,
such that

\[
                              r(xy)=a_x+a_y.                   \tag{7}
\]

Let \(R_5\) be the graph on \(\mathbb F_2^5\) joining words at Hamming
distance two.  Because every \(r(xy)\) has weight two, (7) would be a
homomorphism \(K_6\to R_5\).  This is impossible: \(\omega(R_5)=5\).

For completeness, translate any clique of \(R_5\) to contain zero.  The
other words are pairwise-intersecting two-subsets of \([5]\).  They are
either contained in a four-edge star or form a three-edge triangle, so
there are at most four of them.  Zero and a four-edge star attain five.

## 4. A 12-vertex graph-dependent obstruction

Use these local states, in vertex order; \(012\) occurs twice:

\[
\begin{array}{rrrrrr}
012&012&013&014&023&025\\
045&124&125&135&234&345.
\end{array}                                                     \tag{8}
\]

Pair their side occurrences into graph edges as follows.  Each row is
``left vertex, right vertex, old pair label'':

```text
 0  2  01       1  3  01
 0  4  02       1  5  02
 2  4  03       3  6  04       5  6  05
 0  7  12       1  8  12
 2  9  13       3  7  14       8  9  15
 4 10  23       7 10  24       5  8  25
10 11  34       9 11  35       6 11  45
```

The result is a simple connected cubic graph.  Deleting any edge leaves
it connected, so it is bridgeless.  Its graph6 record in this vertex order
is

```text
KQh?k`CGGQ?R
```

At every vertex, the incident labels are exactly the three sides of its
state, hence define an eight-cycle double cover with old coordinates 6
and 7 empty.  It is literally Oum-compatible: on an edge \(xy\), set
\(\phi(e)=x+y\), and at state \(xyz\), set \(t_v=x+y+z\).

All fifteen old pairs occur.  For twelve of them, exactly two states
contain the pair and the displayed edge joins those states.  For the
remaining pairs \(01,02,12\), the state \(012\) occurs twice and the two
edges join it respectively to

\[
 \begin{array}{c|c}
 p&\text{other states}\\ \hline
 01&013,014\\
 02&023,025\\
 12&124,125.
 \end{array}
\]

Thus every state-adjacency graph \(A_p\) is connected.  Lemma 1 makes
the rule context-free on all fifteen pairs.

There are eleven distinct rows in (8).  In pair-column order

```text
01 02 03 04 05 12 13 14 15 23 24 25 34 35 45
```

their binary rank is ten.  Section 3 now applies and gives a
contradiction.

**Theorem 2 (triangle-state no-go).**  The displayed simple bridgeless
cubic graph and its supplied Oum eight-cover admit no graph-dependent
triangle-state rule satisfying (3)--(5).

The mechanism is sharp in order.  Rank ten requires at least ten distinct
triangle states, so a smaller cubic witness could only have order ten.
Then all ten vertex states would be distinct.  Full rank in the cycle
space of \(K_6\) forces all fifteen pair columns to occur.  The thirty
pair incidences of ten cubic vertices would give every pair exactly twice,
because every pair has positive even incidence in a closed cover.  The xor
of the ten triangle rows would consequently be zero, making them
dependent and their rank at most nine, a contradiction.  Thus order at
least twelve is necessary, and the witness attains it.  This is a minimum
statement for this particular connected-state/full-rank certificate, not
for every possible restricted compression model.

## 5. Exactly where vertex context repairs the witness

In the displayed graph-edge order, a proper 3-edge-colouring is

```text
0 1 1 2 2 2 0 2 0 1 0 2 0 1 1 2 0 1
```

Map its colours 0, 1, 2 to the new labels \(01,02,12\).  This is a
three-cycle double cover and hence a FiveCDC.

At vertex 0, whose old state is \(012\), the old sides \(01,02,12\)
receive colours \(0,1,2\).  At vertex 1, which has the identical old state
\(012\), those sides receive colours \(1,2,0\).  The positive cover thus
uses two different local permutations at two occurrences of the same
Oum state.  That one bit of vertex-occurrence context is precisely what
the triangle-state rule forbids.

If an allowed rule may depend arbitrarily on the vertex identity, the
restriction disappears completely.  At each cubic vertex, both the old
labels and the labels of any FiveCDC form the three sides of a triangle;
there is a unique bijection between their three triangle points inducing
the edge correspondence.  Conversely, compatible vertex-specific local
triangles are exactly a FiveCDC labelling.  Therefore

\[
 \boxed{\text{unrestricted vertex-specific local compression exists}
        \iff\text{the graph has a FiveCDC}.}
\]

Theorem 2 closes this natural state-only rule.  It does not exclude other
intermediate rules using bounded neighbourhood context, and it does not
settle the existential vertex-specific problem.

## 6. Orientable scope

No orientation variables occur.  Local xor parity proves only that the
five output edge-subsets are Eulerian.  Neither the obstruction nor the
positive control asserts the opposite-direction condition of the
orientable variant.

## AI-use and trust disclosure

OpenAI Codex agents, under Atharva Vaidya's direction, formulated the
triangle-state model, found the order-12 witness, derived the proof and
sharpness statement, wrote the exact checks, and drafted this note.  The
checkers are deterministic but AI-written and are not independent human
review.  No priority or FiveCDC-resolution claim is made.
