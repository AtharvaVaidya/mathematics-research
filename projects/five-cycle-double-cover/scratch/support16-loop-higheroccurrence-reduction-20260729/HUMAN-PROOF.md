# Interaction loops through support 16 and the higher-occurrence boundary

Date: 2026-07-29

Status: **CLEAN-OR-DELETE THEOREM FOR ALL TWO-OCCURRENCE STATES THROUGH
SUPPORT 16, INCLUDING LOOPS / EXACT NO-GO FOR FORCED TWO-TERMINAL
HIGHER-OCCURRENCE SWITCHES / NOT A FIVE-CYCLE-DOUBLE-COVER RESOLUTION**.

## 1. Conventions and statement

Put \(K=\mathbb F_2^2=\{0,1,2,3\}\), with addition written as xor.  Let
the first-coordinate support be a disjoint union of circuits
\[
                         H=D_1\mathbin{\dot\cup}\cdots
                              \mathbin{\dot\cup}D_m .
\]
At a split boundary occurrence \(i\), let
\[
                         d_i=c_{i-1}+c_i\ne0             \tag{1}
\]
be the derivative of the cyclic low-colour word on its support circuit.

First assume that every component of \(G-H\) has exactly two boundary
occurrences.  Contract every support circuit to a vertex and every
complement component to an edge.  The result is an interaction
multigraph \(J\); two occurrences on the same support circuit give a
loop.  Component charge makes the two derivatives of an interaction
edge equal.  Component maps can send this common derivative to any
element of \(K-\{0\}\).  Thus feasible component-map images are exactly
the nowhere-zero \(K\)-flows
\[
 t:E(J)\longrightarrow K-\{0\},\qquad
 \mathop{\mathbin\oplus}_{e\ni v}t_e=0,                 \tag{2}
\]
where a loop occurs twice in the vertex equation and cancels.

Integrating the increments in the cyclic order at \(v\) gives a closed
walk on the four points of \(K\).  A flow **deletes** if one local walk
omits a point.  It **cleans** if translations of the local walks make
the two occurrences of each interaction edge traverse the same
unoriented edge of \(K_4\).

We prove:

> **Loop theorem through 16.** Every flowable two-occurrence interaction
> state of total support at most \(16\), with loops allowed, has a
> feasible flow which cleans or deletes.

The previously proved loopless theorem works through support \(18\).
The genuinely new content here is the case with at least one
interaction loop.  For a globally cardinality-minimum extendable
projection, deletion is impossible, so such a projection is cleanable.
This is a bounded two-occurrence theorem, not the unrestricted FiveCDC
conjecture.

## 2. The exact legal move supplied by a loop

Let a loop component have its two occurrences at derivative positions
\(i<j\) on one support circuit, both currently carrying \(t\ne0\).
Choose another \(s\ne0,t\), and put \(\Delta=t+s\).  Changing the loop's
component map from \(t\) to \(s\) changes precisely
\[
                         d_i,d_j\longmapsto d_i+\Delta,d_j+\Delta .
                                                               \tag{3}
\]
The new integrated word is
\[
 c'_k=\begin{cases}
       c_k+\Delta,&i\le k<j,\\
       c_k,&\text{otherwise}.
      \end{cases}                                           \tag{4}
\]
The two changes cancel around the circuit, so (4) is integrable and
does not change any other circuit closure.

This move also has a literal graph realization.  In the loop component,
retain the edges of low colour \(t\) or \(s\).  Its only odd boundary
vertices are the two displayed occurrences, so they are joined by one
of the retained paths.  Interchanging \(t,s\) on that path has exactly
the boundary effect (3).  Thus (4) is not an operation on an arbitrary
unrealizable state.

If the current word already omits a colour, it deletes.  Otherwise a
proper dirty word of length four or five has, up to an affine
permutation of \(K\) and a dihedral circuit action, the unique form
shown below.  The table lists every possible equal-derivative pair and
one interval translation which deletes.

| word | derivative | loop positions | \(\Delta\) | changed word |
|---|---|---:|---:|---|
| `0123` | `3131` | \(0,2\) | 2 | `2323` |
| `0123` | `3131` | \(1,3\) | 2 | `0303` |
| `01023` | `31121` | \(1,2\) | 2 | `03023` |
| `01023` | `31121` | \(1,4\) | 2 | `03203` |
| `01023` | `31121` | \(2,4\) | 3 | `01313` |

Every last-column word uses at most three colours.  This proves:

> **Short-loop deletion lemma.** A dirty support circuit of length at
> most five which contains an interaction loop admits a legal
> loop-component map, equivalently a forced same-component Kempe path
> switch, which deletes that circuit.

## 3. The two-vertex local lemma

For a two-vertex interaction component, call a nonloop occurrence on
one circuit a **port**.  Every port occurs once on that circuit and its
edge has the same value at the other vertex.  Every loop symbol occurs
twice.  The sole condition on the port values is that their xor be zero;
loop values are independent nonzero elements.

For circuit lengths five and seven, after the short-loop lemma has been
used, the only needed cases are
\[
\begin{array}{c|c|c}
\text{length}&\text{ports}&\text{loop pairs}\\ \hline
5&5&0\\
7&3&2\\
7&5&1\\
7&7&0.
\end{array}                                               \tag{5}
\]
The length-five and loopless length-seven rows also have the elementary
bundle assignment: give two consecutive ports distinct values \(b,c\)
and every remaining port \(a=b+c\).  The walk visits only
\(\{0,b,a\}\).

For completeness, the verifier checks the slightly larger finite
statement including the unused length-five three-port row.  It
enumerates every placement of the ports and every perfect matching of
the remaining loop appearances, then every nonzero symbol assignment
until it finds a three-colour walk:

| length, ports | cyclic marked patterns | residual |
|---|---:|---:|
| \(5,3\) | 10 | 0 |
| \(5,5\) | 1 | 0 |
| \(7,3\) | 105 | 0 |
| \(7,5\) | 21 | 0 |
| \(7,7\) | 1 | 0 |

This is an exact 138-pattern check.  In a two-vertex bundle, every
zero-xor port assignment found locally is automatically a global flow:
the same port xor occurs at the other vertex, while loops cancel there
as well.

## 4. Human shape reduction through support 16

Delete the loops from \(J\) but retain its vertices.  Its connected
components are also the connected components of the full interaction
state, since a loop joins no two vertices.  Disconnected components can
be treated independently: one deleting component deletes globally, and
clean translations from components which all clean combine.
Consequently assume this loopless core is connected.

A core component on one vertex is a one-support-circuit boundary state,
so the universal one-circuit tensor theorem cleans it.  We may assume
there are at least two support circuits.  If a circuit word already
omits a colour, it deletes; hence every circuit length is at least four.
The total support bound leaves at most four interaction vertices.

If all circuit lengths are even, put one fixed nonzero value on every
interaction edge, including every loop.  Every vertex equation holds
and every local walk alternates between two points, so it deletes.
If a loop lies on a circuit of length at most five, Section 2 deletes.
We therefore retain only a loop on a circuit of length at least six and
at least two odd circuit lengths.

### Two vertices

The core is a parallel bundle.  The two core degrees have the same
parity; in the odd case the shorter circuit has length five or seven.
If it has length five, it cannot contain a surviving loop, so it has
five ports and the bundle assignment in Section 3 deletes.  If it has
length seven, its number of ports is \(3,5,\) or \(7\): one port is not
flowable, and the other cases are (5).  The paired-port lemma deletes.
This includes all odd pairs with total length at most sixteen:
\[
                  5+5,\ 5+7,\ 5+9,\ 5+11,\ 7+7,\ 7+9.
\]

### Four vertices

Four dirty circuits already use at least \(4+4+4+4=16\) support edges.
Equality forces four even lengths, handled by the constant flow.

### Three vertices

Up to sorting, the only length triples of even total at most sixteen
which survive the even-length and short-loop reductions are
\[
                              4+5+7,\qquad 5+5+6.       \tag{6}
\]
The discarded odd triple \(4+5+5\) could place a loop only on a
length-four or length-five circuit, so the short-loop lemma handles it.

In \(4+5+7\), every surviving loop lies on the length-seven circuit;
name it vertex 2.  The other lengths are distinct, so this naming loses
nothing.  If there are \(l=1,2\) loops at vertex 2, the core degree
vectors and the uniquely determined triangle bundle multiplicities
\((m_{01},m_{02},m_{12})\) are
\[
\begin{array}{c|c|c}
l& (d_0,d_1,d_2)&(m_{01},m_{02},m_{12})\\ \hline
1&(4,5,5)&(2,2,3)\\
2&(4,5,3)&(3,1,2).
\end{array}                                               \tag{7}
\]
Three loops would leave core degree one at vertex 2.  Its sole core
edge would be a bridge and cannot carry a nowhere-zero group flow.

In \(5+5+6\), every surviving loop lies on the unique length-six
circuit, again named vertex 2; the equal length-five vertices may be
exchanged.  The connected cases are
\[
\begin{array}{c|c|c}
l& (d_0,d_1,d_2)&(m_{01},m_{02},m_{12})\\ \hline
1&(5,5,4)&(3,2,2)\\
2&(5,5,2)&(4,1,1).
\end{array}                                               \tag{8}
\]
With three loops, vertex 2 is an isolated one-circuit component and the
remaining two-vertex component is handled separately.  Equations
(7)--(8) follow directly from
\[
 2m_{01}=d_0+d_1-d_2,\quad
 2m_{02}=d_0+d_2-d_1,\quad
 2m_{12}=d_1+d_2-d_0 .
\]
Thus no loop placement, extra loop count, or two-, three-, or
four-vertex shape is missing.

The four profiles in (7)--(8) are the complete finite remainder.  The
verifier labels all parallel edges, enumerates the cyclic orders at
each vertex modulo rotation and reversal, enumerates every normalized
nowhere-zero \(K\)-flow, and tests literal deletion and literal \(K_4\)
edge equality under all relative circuit translations:

| profile | local order counts | states | flows | selected clean | selected delete | residual |
|---|---:|---:|---:|---:|---:|---:|
| `457-a` | \(3,12,180\) | 6,480 | 138 | 0 | 6,480 | 0 |
| `457-b` | \(3,12,90\) | 3,240 | 126 | 0 | 3,240 | 0 |
| `556-a` | \(12,12,30\) | 4,320 | 138 | 168 | 4,152 | 0 |
| `556-b` | \(12,12,16\) | 2,304 | 180 | 12 | 2,292 | 0 |

“Selected” records the first witness found by the deterministic search;
it is not an exclusivity claim.  There are 16,344 states and no
residual.  Together with the preceding human reduction, this proves the
loop theorem.

Combining it with the prior loopless result gives:

> **Two-occurrence corollary.** Every flowable two-occurrence state of
> support at most \(16\), without any restriction on interaction loops,
> cleans or deletes.  Loopless states are known by the same method
> through support \(18\).

## 5. Components with three or more occurrences

Let a complement component have \(n_1,n_2,n_3\) boundary derivatives of
the three nonzero values.  Component charge is zero exactly when
\[
                         n_1\equiv n_2\equiv n_3\pmod2. \tag{9}
\]
In particular, a three-occurrence component has one occurrence of each
nonzero value.

For distinct colours \(x,y\), the odd boundary vertices of the
\(x,y\)-subgraph are exactly the occurrences whose derivatives lie in
\(\{x,y\}\).  If there are exactly two such occurrences, they are joined
by a forced path.  Switching it adds \(\Delta=x+y\) at those two
endpoints.

There is an important limitation:

> **Forced two-terminal redundancy lemma.** Every forced two-terminal
> switch has, on all boundary derivatives of its component, exactly the
> same effect as one uniform element of
> \(\operatorname{GL}(2,2)\).

Indeed, the two terminal values are either \(x,y\), in which case the
switch interchanges their sole occurrences, or \(x,x\), in which case
it changes both to the absent value \(y\).  No other boundary occurrence
has value \(x\) or \(y\).  In both cases the result is the global
transposition \(x\leftrightarrow y\), fixing the third nonzero value.
The verifier checks all 69 charge-zero multiplicity cases through
sixteen occurrences, but the preceding two sentences are the proof.

For a three-occurrence component, all three colour pairs have exactly
two terminals.  Hence its forced switches realize the three
transpositions, but these are already precisely its component-map
orbit.  If all three occurrences lie on one dirty circuit of length at
most five, one transposition always deletes.  There is no length-four
case; for the unique length-five dirty word the complete table is:

| word | derivative | triple positions | switched pair | changed word |
|---|---|---:|---:|---|
| `01023` | `31121` | \(0,1,3\) | \(1,3\) | `02323` |
| `01023` | `31121` | \(0,2,3\) | \(0,2\) | `23023` |
| `01023` | `31121` | \(0,3,4\) | \(0,4\) | `23203` |

This short-circuit lemma is useful, but the redundancy lemma explains
why it does not resolve the general higher-occurrence branch.

## 6. Sharp local failures at length six

The length-five bounds above are sharp in the abstract marked-word
model.  Up to affine colour maps and dihedral circuit actions, the
first loop failures are the following seven.  Each of the two displayed
interval changes replaces the loop value by one of its other two
possible nonzero values, and every changed word still uses all four
colours.

| word | derivative | marks | two changed words |
|---|---|---:|---|
| `010123` | `311131` | \(1,2\) | `030123`, `020123` |
| `010123` | `311131` | \(1,3\) | `032123`, `023123` |
| `010123` | `311131` | \(2,5\) | `012303`, `013213` |
| `010213` | `311232` | \(1,2\) | `030213`, `020213` |
| `010232` | `211211` | \(1,5\) | `032012`, `023102` |
| `012013` | `313212` | \(0,2\) | `102013`, `232013` |
| `012013` | `313212` | \(1,4\) | `030213`, `021313` |

For a three-occurrence component, the two first-failure orbits are:

| word | derivative | triple marks | three transposition words |
|---|---|---:|---|
| `010213` | `311232` | \(0,1,3\) | `210213`, `101213`, `023213` |
| `010213` | `311232` | \(1,4,5\) | `032013`, `023123`, `010203` |

These are local obstructions only.  They are not claimed to be
minimum projections, graph counterexamples, or even global
clean-or-delete residuals.  In particular, a state with only one
support circuit is clean by the tensor theorem.

## 7. The hard support-16 residuals with triples

The unrestricted fixed-word census uses
\[
 c=\texttt{01010123|01012302},\qquad
 d=\texttt{31111131|21113132}.
\]
Four of its eight abstract residual partitions contain a total of six
three-occurrence blocks:

```text
0001234003144422
0012344041300022
0012344403144422
0123444441300022
```

Every triple is split \(2+1\) across the two support circuits.  Its
same-circuit pair therefore gives a legal forced path switch, but the
redundancy lemma shows that switch is one component
\(\operatorname{GL}(2,2)\) transposition already present in the direct
map census.  The verifier independently rechecks every normalized map
tuple: each state has 320 circuit-integrable tuples, zero clean tuples,
and zero deleting tuples.  Therefore forced two-terminal switching
cannot discharge these four residuals.

This is an exact **no-go**, not a counterexample.  The partitions remain
abstract boundary states here; no minimum-projection or graph
realization claim is imported.  The missing mechanism is now precise:
a useful higher-occurrence Kempe move must come from a bichromatic
terminal set of size at least four and must exploit the path matching
inside the realized complement component.  Such a switch can change a
proper subset of one derivative-colour class and need not lie in the
uniform component-map orbit.

## 8. Verification and scope

`verify.py` independently checks:

1. the affine/dihedral dirty-word reductions through length six;
2. the short-loop and short-triple tables;
3. the 138 paired-port patterns;
4. the forced two-terminal redundancy cases through boundary size 16;
5. all 16,344 cyclic-order states in the four remaining loop profiles;
6. the six triple blocks and all \(4\cdot6^4\) normalized map tuples in
   the hard residual audit.

The frozen profile stream digest is

```text
8168cff38b861ac162ada05f89bb9f6986d9fe12d1ae3eb9b1bbb02682826228
```

This package proves a new bounded theorem for the two-occurrence branch.
It does not cover arbitrary higher-occurrence components, support above
the stated bounds, arbitrary-degree reductions, or the orientable
variant.  It does not prove or disprove FiveCDC.

OpenAI Codex agents under Atharva Vaidya's direction derived the
reductions, wrote the proof and verifier, and ran the finite searches.
The work has not received independent human peer review, and no
literature-priority claim is made.
