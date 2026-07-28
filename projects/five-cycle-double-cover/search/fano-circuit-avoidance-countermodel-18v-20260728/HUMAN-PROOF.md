# Human proof of the 18-vertex circuit-avoidance countermodel

## Exact statement refuted

The following natural strengthening of the Oum one-switch strategy is
false.

> Let \(G\) be a simple cyclically \(4\)-edge-connected cubic graph with a
> nowhere-zero \(\mathbb F_2^3\)-flow \(\phi\).  If \(s\ne t\) and at most
> three edges all have value \(s\), then there is a circuit through those
> edges avoiding the value class
> \(M_t=\{e:\phi(e)=t\}\).

The countermodel below is stronger than a disconnection example:
\(G-M_t\) is connected and bridgeless.  The obstruction is a two-vertex
separation.

This theorem is only about a proposed prescribed-circuit lemma.  It is not
a Five-Cycle Double Cover counterexample and not a counterexample to the
broader assertion that *some* connected-circuit switch repairs the fixed
flow.

## Graph and flow

Take the canonical graph6 string

```text
QCGY?c?W???F_GAAo@?D@P??`?G
```

with lexicographically ordered edges

```text
 0  0-3      9  3-5      18  8-12
 1  0-12    10  3-7      19  8-15
 2  0-14    11  4-5      20  9-11
 3  1-6     12  4-13     21 10-11
 4  1-9     13  5-16     22 10-13
 5  1-16    14  6-7      23 10-14
 6  2-4     15  6-15     24 12-13
 7  2-9     16  7-17     25 14-15
 8  2-17    17  8-11     26 16-17.
```

Assign the edge values

```text
6 3 5 3 4 7 5 3 6 3 5 6 3 5 1 2 4 4 5 1 7 3 5 6 6 3 2.
```

At every vertex the three incident values are distinct nonzero elements
whose XOR is zero.  Thus this is a nowhere-zero
\(\mathbb F_2^3\)-flow.  Distinctness also proves directly that each value
class \(M_t\) is a matching: if two incident values were both \(t\), the
third value forced by the flow equation would be zero.

The checker independently verifies that the graph is simple, connected,
cubic, non-Tait, of girth five, and has no cyclic edge cut of size below
four.  It is the first Blanuša snark.

## The initial Oum obstruction

For a fixed flow, an Oum-compatible eight-cover is described by vertex
potentials in \(\mathbb F_2^3\).  Fixing one potential to zero removes the
global translation symmetry.

For the displayed flow the compatibility system has 57 binary scalar
rows, rank 52, and two free bits.  Hence it has exactly four gauged
solutions.  The four coordinate co-occurrence graphs are:

- twice, the \(K_6\) on \(\{0,3,4,5,6,7\}\); and
- twice, the \(K_6\) on \(\{0,1,2,3,5,6\}\).

Each graph uses exactly the 15 edges of its displayed \(K_6\).  Therefore
none is five-colourable.  By the eight-coordinate
\(R_5\)-equivalence, none admits a general XOR compression to five
coordinates either.

## Three equal-value edges with no avoiding circuit

Set

\[
t=6,\qquad s=3,
\]

and prescribe the three value-\(3\) edges

\[
a=e_1=0\,12,\qquad
b=e_3=1\,6,\qquad
c=e_9=3\,5.
\]

Let \(H=G-M_6\).  Direct inspection, also replayed by the checker, shows
that \(H\) is connected and bridgeless.

Delete vertices \(1\) and \(6\) from \(H\).  Exactly two components remain:

\[
A=\{0,2,4,8,9,10,11,12,13,14,15\}
\]

and

\[
B=\{3,5,7,16,17\}.
\]

The edge \(a\) lies in \(A\), the edge \(c\) lies in \(B\), and the third
marked edge is precisely \(b=1\,6\).

Suppose a circuit \(C\) of \(H\) contained \(a,b,c\).  Removing the edge
\(b=1\,6\) from \(C\) would leave a path from \(1\) to \(6\) containing
both \(a\) and \(c\).  Deleting the endpoints \(1,6\) from that path leaves
one connected path containing both marked edges.  This is impossible
because \(a\) and \(c\) lie in different components of
\(H-\{1,6\}\).  Therefore no circuit avoids \(M_6\) and contains all three
marked edges.

The finite replay finds 692 elementary circuits in \(G\), of which 17
avoid \(M_6\), and zero of those 17 contain all three marks.

## Why the odd-cut argument does not close the gap

There is in fact no odd cut of \(H\) contained in the three marks.  This is
not an accident.

Let \(S\) be any odd set of equal-\(s\) edges, with \(s\ne t\), and suppose
that an \(H=G-M_t\) cut is contained in \(S\).  If the cut has odd
cardinality, the XOR of its flow values is \(s\).  Restoring the deleted
\(t\)-edges adds either \(0\) or \(t\) to the cut sum, according to their
parity.  The flow cut equation would therefore say either

\[
s=0
\quad\text{or}\quad
s+t=0,
\]

both impossible.

Thus flow parity eliminates exactly the odd-cut obstruction in the
Knappe--Pitz theorem.  It does not make \(G-M_t\)
3-edge-connected.  Here the two-vertex separator \(\{1,6\}\) gives a
Watkins--Mesner type three-mark obstruction even though the odd-cut test
passes.

## The marked disconnected switch really repairs the \(K_6\)

Consider the binary cycle \(Q\) with edge set

```text
1 2 3 5 9 10 13 14 18 19 25.
```

It is the disjoint union of

\[
0-12-8-15-14-0
\]

and

\[
1-6-7-3-5-16-1.
\]

Consequently \(Q\) contains all three marked edges \(e_1,e_3,e_9\).  It
contains no value-\(6\) edge.  Adding \(6\) to the flow along \(Q\) is
therefore a legal nowhere-zero binary-cycle switch.  The resulting values
are

```text
6 5 3 5 4 1 5 3 6 5 3 6 3 3 7 2 4 4 3 7 7 3 5 6 6 5 2.
```

The repaired compatibility system again has four gauged potentials.  Every
one of the four co-occurrence graphs uses 14 pair types, has clique number
five, and is five-colourable.  One checked colouring of coordinates
\(0,\ldots,7\) is

```text
4 4 0 0 1 2 3 0.
```

Thus the three prescribed inclusions occur in a genuine repair of the
initial \(K_6\) Oum obstruction, but no *connected* circuit can realize
those inclusions while avoiding \(M_6\).

## Sharp scope

The same starting flow has a different connected repair: switch value
\(1\) on the six-circuit

\[
0-3-5-4-13-12-0,
\]

whose edge IDs are

```text
0 1 9 11 12 24.
```

The resulting fixed flow has a five-colourable compatible cover.  Hence
the countermodel refutes only the prescribed-triple proof step.  It does
not refute the surviving existential claim that some circuit repairs every
merge-bad flow on a cyclically \(4\)-edge-connected non-Tait graph.

## Minimality scope

The frozen canonical Snarkhunter lists of simple cyclically
\(4\)-edge-connected non-Tait cubic graphs contain:

```text
order 10: 1
order 12: 0
order 14: 0
order 16: 0
order 18: 2.
```

The checker verifies the hashes and row counts of those lists.  It also
exhausts all 28,560 nowhere-zero \(\mathbb F_2^3\)-flows on the Petersen
graph and finds no prescribed avoidance failure for any choices of
\(s\ne t\) and at most three equal-\(s\) edges.  Relative to those frozen
complete source lists, order 18 is therefore minimal.

Canonical source completeness and the interpretation of the Snarkhunter
options are inherited from
`search/focused-theta-choice-through28-20260727/`; the present checker is
not a second canonical graph generator.

## AI-use disclosure

OpenAI Codex, under human direction, formulated the avoidance question,
found and minimized the finite countermodel, wrote the human proof and
independent checker, and ran the computations.  All universal statements
above have explicit proofs; every finite claim is replayable from
`checker.py`.  No AI-generated inference is presented as a resolution of
FiveCDC.
