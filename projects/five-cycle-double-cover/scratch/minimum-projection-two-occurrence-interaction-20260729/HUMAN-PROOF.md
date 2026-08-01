# Two-occurrence components, interaction flows, and the Petersen no-go

Date: 2026-07-29

Status: **EXACT SUBCLASS COUNTERTHEOREM / SMALLEST LOOPLESS
TWO-OCCURRENCE ABSTRACT COUNTERSTATE / COMPLETE MINIMUM-PROJECTION DESCENT /
NOT A FIVECDC COUNTEREXAMPLE**.

## 1. Interaction multigraph

Let \(H=D_1\mathbin{\dot\cup}\cdots\mathbin{\dot\cup}D_m\) be the
first-coordinate support of a nowhere-zero
\(\mathbb F_2\times K\)-flow, where \(K=\mathbb F_2^2\).  Assume the
ambient graph is cubic and every component \(W_a\) of \(G-H\) contains
exactly two support-boundary occurrences.

At an occurrence \(p\), let \(d_p\in K-\{0\}\) be the low-flow
derivative of the two adjacent support values.  Component charge gives
\[
                              d_p+d_q=0
\]
for the two occurrences \(p,q\) of \(W_a\).  Thus both values are one
common nonzero element \(z_a\).

Define the **interaction multigraph** \(J\) as follows:

- its vertices are the support circuits \(D_j\);
- its edge \(a\) is the complement component \(W_a\);
- the endpoints of \(a\) are the circuits containing its two
  occurrences.  Two occurrences on the same circuit give a loop.

The derivative xor around every support circuit is zero.  Therefore
\[
                         \bigoplus_{a\ni D_j} z_a=0,     \tag{1}
\]
where a loop is incident twice and cancels.  In other words, \(z\) is a
nowhere-zero \(K\)-flow on \(J\).

Conversely, a nowhere-zero \(K\)-flow on \(J\) integrates around every
support circuit.  A component map
\(L_a\in\operatorname{GL}(2,2)\) can send \(z_a\) to any prescribed
nonzero \(t_a\).  Consequently:

> **Interaction-flow dictionary.**  Feasible component-map images are
> exactly the nowhere-zero \(K\)-flows \(t\) on \(J\).

This is the promised relation between thin complement components and an
ordinary nowhere-zero flow.

## 2. Cleanliness as two equal edges of \(K_4\)

Integrate a feasible \(t\) around the support circuits.  At either
occurrence of component \(a\), the two adjacent support colours are
\[
                              \{x,x+t_a\}.               \tag{2}
\]
Because \(t_a\ne0\), (2) is an unoriented edge of the complete graph on
the four points of \(K\).

The cut of a two-occurrence component sees the xor of the two
two-element colour sets in (2).  A support edge joining the two
occurrences is counted twice and cancels, as it should.  Hence:

> **\(K_4\)-walk dictionary.**  Component \(a\) is clean exactly when
> its two occurrences traverse the same unoriented edge of \(K_4\).
> The whole extension is clean exactly when this holds for every
> interaction edge.

Thus each support circuit is a closed walk in \(K_4\), and a clean
extension asks the two appearances of every interaction edge to be the
same \(K_4\) edge, not merely parallel edges having the same difference.

## 3. The Petersen double-occurrence system

Take two support 5-circuits.  Let their component orders be
\[
                      A=\texttt{01234},\qquad
                      B=\texttt{03142}.                 \tag{3}
\]
The interaction graph is two vertices joined by five parallel edges.
Its nowhere-zero \(K\)-flows are precisely the tuples
\[
                  (t_0,t_1,t_2,t_3,t_4)\in\{1,2,3\}^5,
                  \qquad t_0+\cdots+t_4=0.              \tag{4}
\]
There are
\[
 \frac14\left(3^5+3(-1)^5\right)=60.
\]
This is the four-character xor count: the trivial character contributes
\(3^5\), while each of the three nontrivial characters sums to \(-1\)
on \(K-\{0\}\).

The global action \(\operatorname{GL}(2,2)\cong S_3\) on the three
nonzero values is free on (4): a 5-tuple of equal nonzero entries cannot
xor to zero, so every tuple uses at least two values.  Hence the 60
flows split into ten orbits of six.

Here is the complete orbit table.  The middle columns are the integrated
zero-start support words in orders \(A,B\); the following integer is the
number of colours used.

| flow representative | \(A\)-word | colours | \(B\)-word | colours |
|---|---:|---:|---:|---:|
| `11123` | `10130` | 3 | `13210` | 4 |
| `11213` | `10230` | 4 | `10120` | 3 |
| `11231` | `10210` | 3 | `12320` | 4 |
| `12113` | `13230` | 4 | `10210` | 3 |
| `12131` | `13210` | 4 | `12010` | 3 |
| `12223` | `13130` | 3 | `13120` | 4 |
| `12232` | `13120` | 4 | `12020` | 3 |
| `12311` | `13010` | 3 | `10230` | 4 |
| `12322` | `13020` | 4 | `13130` | 3 |
| `12333` | `13030` | 3 | `12030` | 4 |

Every entry is checked by five xors.  The ten representatives are the
lexicographically least elements of the ten free \(S_3\)-orbits, so the
table is complete.  Translating a circuit by a constant permutes its
four colours and does not change the displayed count.

The normalized component-map census follows from the same table without
another search.  Fixing \(L_0=I\) forces \(t_0=1\).  Exactly \(60/3=20\)
flows in (4) have that first value, by the transitive \(S_3\)-action.
For each of the other four components, exactly two elements of
\(\operatorname{GL}(2,2)\) send its fixed initial derivative to a
prescribed nonzero value.  Hence exactly
\[
                              20\cdot2^4=320
\]
of the \(6^4\) normalized map tuples are circuit-integrable.  The table
shows that none cleans and all 320 admit a circuit deletion.

If an extension were clean, the \(K_4\)-walk dictionary would make the
two circuits traverse the same five assigned \(K_4\) edges.  Their
colour sets would both equal the union of the endpoints of those five
edges and would therefore have equal cardinality.  Every row of the
table has cardinalities \(3\) and \(4\), a contradiction.

We have proved:

> **Petersen two-occurrence no-go.**  The double-occurrence system (3)
> is extendable but has no clean extension.  This remains true after
> every support-neutral Kempe sequence, because the table already
> contains every possible nowhere-zero extension of the fixed support.

The same table also gives the descent: every feasible flow makes exactly
one support circuit omit a colour.  Adding \((1,c)\) around that circuit,
where \(c\) is omitted, deletes it from the first-coordinate support
without creating a zero edge.

For the displayed initial flow `11123`, use the literal low words
\[
                         \texttt{10130|13210}.           \tag{5}
\]
The first word omits \(2\).  Adding \((1,2)\) around the first circuit
changes it to `32312` and deletes that circuit.

## 4. Literal Petersen realization and global minimum

Use vertices \(0,\ldots,9\).  The support edges are the two 5-circuits
\[
\begin{split}
 &01,12,23,34,40,\\
 &56,67,78,89,95.
\end{split}
\]
The five complement components are the single matching edges
\[
                         05,\ 17,\ 29,\ 36,\ 48.        \tag{6}
\]
Their orders around the support circuits are exactly (3).  This is the
Petersen graph.

In the edge order just displayed, assign low values
\[
\texttt{10130},\quad\texttt{13210},\quad\texttt{11123}.
\]
At every vertex the three low values xor to zero; putting first
coordinate one on the ten support edges and zero on (6) gives a
nowhere-zero three-coordinate flow.

The graph is simple, cubic, bridgeless, and has girth five.  It is not
Tait-colourable.  One elementary certificate for the last statement is
that it has six perfect matchings and the complement of each is two
5-circuits.  In a Tait colouring, deleting one colour class would leave
even alternating circuits, which is impossible.

After the explicit deletion in (5), the support is the second
5-circuit.  This size-five projection is globally minimum:

- support zero would be a Tait colouring, which does not exist;
- every nonzero binary cycle has at least five edges because the graph
  has girth five;
- the displayed descended extension has support five.

It is also clean.  Removing the remaining support 5-circuit leaves the
other 5-circuit together with all five matching edges, a connected
spanning subgraph.  Hence \(G-H'\) has one component, whose cut is empty.

The Petersen state is therefore a particularly sharp warning: a fixed
nonminimum projection can be uncleanable under **all** its extensions,
even when every complement component has two occurrences, while a
single strict deletion reaches a globally minimum clean projection.

## 5. Smallest loopless two-occurrence abstract counterstate

For a loopless cubic boundary model, support circuits have length at
least two.  A two-occurrence-component state has even total support
size.  One-support-circuit states are cleanable by the universal tensor
theorem.

The primary verifier enumerates every perfect matching of the labelled
occurrences, every nowhere-zero \(K\)-flow on its interaction graph, and
every relative circuit translation for all multi-circuit shapes of total
size four, six, and eight:

| shape | pairings | flowable | cleanable |
|---|---:|---:|---:|
| \(2+2\) | 3 | 3 | 3 |
| \(2+4\) | 15 | 15 | 15 |
| \(3+3\) | 15 | 6 | 6 |
| \(2+2+2\) | 15 | 15 | 15 |
| \(2+6\) | 105 | 105 | 105 |
| \(3+5\) | 105 | 60 | 60 |
| \(4+4\) | 105 | 105 | 105 |
| \(2+2+4\) | 105 | 105 | 105 |
| \(2+3+3\) | 105 | 42 | 42 |
| \(2+2+2+2\) | 105 | 105 | 105 |

These are all integer partitions of the relevant even sizes into at
least two parts of size at least two.  Total size ten is therefore the
first possible loopless counterstate, and (3) attains it.  For simple
graphs, where circuit lengths are at least three, the same conclusion
follows from the corresponding subrows.

This finite minimality statement is separately replayable by both
`verify.py` and `search_small.py`; it is not used to prove the Petersen
no-go itself.

## 6. Verification and scope

`verify.py` checks the interaction dictionary, all 60 flows, the ten-row
orbit table, all \(6^4\) normalized component maps, the complete
smaller-size pairing census, the literal graph, girth, bridges,
non-Tait-colourability, and the descended flow.

`independent_audit.py` instead enumerates all 240 proper cyclic
four-colour words of length five.  It finds 960 compatible word pairs,
zero clean pairs, and the same \(3/4\) or \(4/3\) deletion profile.  It
also proves non-Tait-colourability by independently enumerating the six
perfect matchings.

This result refutes the proposed universal two-occurrence direct-cleaning
subclass.  It does not refute the minimum extendable projection
conjecture and does not resolve FiveCDC: the exact counterstate is not
minimum, and its minimum descendant is explicitly clean.

OpenAI Codex agents under human direction derived the interaction-flow
model, found the Petersen state by exact search, and wrote this proof
package.  It has not received independent human peer review.  No
literature-priority claim is made.
