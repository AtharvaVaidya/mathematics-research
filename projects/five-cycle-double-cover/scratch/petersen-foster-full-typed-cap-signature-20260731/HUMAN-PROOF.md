# A complete six-state signature on the Petersen--Foster control

Date: **2026-07-31**

Status: **EXPLICIT FINITE WITNESS / NOT A UNIVERSAL THEOREM**.

## Graph

Start with the Foster graph in LCF form

```text
[17,-9,37,-37,9,-17]^15.
```

Delete vertex zero, leaving boundary vertices formerly numbered `1,17,89`.
Replace each vertex of the Petersen graph by one copy of this three-pole
and join its three boundary vertices according to the three incidences of
the Petersen vertex.  With vertices renumbered copywise, this produces the
simple cubic graph `F` on 890 vertices and 1,335 edges reconstructed in the
checker.

The checker verifies connectivity, absence of one- and two-edge cuts, and
girth ten directly.  The graph is non-Tait for a short independent reason.
In any Tait colouring of a cubic three-pole with three semiedges, the parity
lemma makes the three boundary colours distinct.  A Tait colouring of `F`
would therefore induce a Tait colouring on the Petersen macrograph.  The
Petersen graph is not Tait-colourable: every perfect matching has a
complement consisting of two odd 5-circuits, whereas the other two colour
classes of a Tait colouring would form an even alternating factor.

## Rooted cap interface

Take cap vertex

```text
z = 0
```

whose three port edges in the checker's canonical edge order are

```text
0=(0,1), 1=(0,81), 2=(0,89).
```

Take the proper root

```text
r = 552 = (363,400).
```

Deleting `z` leaves a connected bridgeless core with three degree-two
vertices, all other degrees three, and girth ten.  Deleting `r` leaves it
connected and cannot create a shorter circuit.  Thus this interface lies
inside the marked-girth cap domain, although no claim is made that it is a
shore of an actual minimum FiveCDC obstruction.

## Six literal witnesses

For each bit `b=0,...,5`, `verify.py` contains a literal edge-label word

\[
                    q_b:E(F)\longrightarrow D_5.
\]

The bits are ordered

```text
01-in, 01-out, 02-in, 02-out, 12-in, 12-out,
```

where `01,02,12` here denote physical port-slot pairs, not coordinate
pairs.  The factor coordinate pairs used by the six witnesses are,
respectively,

```text
18, 17, 6, 6, 24, 5
```

as five-bit masks.  For each word the checker verifies:

1. every label has Hamming weight two;
2. the XOR of the three incident labels is zero at every vertex;
3. the root and the required two ports lie on one component of the named
   factor `Y_P`;
4. the third port is inactive; and
5. its label equals `P` in internal mode and is disjoint from `P` in
   external mode.

These six witnessed states exhaust the six-state universe.  Therefore the
exact typed signature is the full mask `63`, and in particular contains a
double star.

## Exact limitation

The result concerns one vertex-root interface of one graph.  It does not
show that another interface of this graph is full, that every relevant
non-Tait cap contains a double star, or that any minimum obstruction is
three-cut reducible.  Its role is calibration: the surviving non-Tait,
high-girth cap branch is nonempty and can exhibit maximal rather than
minimal typed flexibility.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the six witnesses by a
deterministic component-Kempe walk, compressed them, implemented the
semantic checker, and drafted this note.  The retained proof is the six
literal label words and direct verification, not the heuristic search.
Independent human review is required before citation.
