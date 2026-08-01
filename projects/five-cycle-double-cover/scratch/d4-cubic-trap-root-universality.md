# Four-coordinate circuit traps are root-universal in cubic graphs

Date: 2026-07-28

## Purpose

The degree-four contraction counterexample raises a sharp threat to the
cubic rooted Kempe-orbit route: perhaps a cubic \(D_5\)-flow orbit could be
trapped in four coordinates and keep some root pair off every factor
circuit.

That particular threat cannot occur.  The obstruction is excluded by a
short cubic/Tait-colouring argument.

## Definitions

Let \(G\) be a finite cubic graph and let \(q:E(G)\to D_5\) be a flow.
Suppose a state uses exactly four coordinates \(S\), omitting \(t\).
For \(i\in S\), write

\[
C_i=\{e:i\in q(e)\}=Y_{it}.
\]

Call a Kempe orbit **four-coordinate circuit-trapped** if, in every state
of the orbit:

1. exactly four coordinates are used; and
2. each of the four coordinate classes \(C_i\) is one circuit.

The second condition is the natural strong form of a fifth-coordinate
trap.  If \(C_i\) is one circuit, switching \(i,t\) on its only component
is merely the global coordinate renaming \(i\leftrightarrow t\).

The rooted orbit property asks, for any two distinct root edges \(r,s\),
for some state and some factor \(Y_{ij}\) in which \(r,s\) lie on the same
circuit.

## Tait quotient of a cubic \(D_4\)-flow

Identify complementary two-subsets of \(S\).  They form three classes:

\[
\{01,23\},\qquad \{02,13\},\qquad \{03,12\}.                 \tag{1}
\]

Regard these as three Tait colours.

At a cubic vertex, the three weight-two labels have xor zero.  They form a
triangle on three of the four coordinates.  Their three complementary
classes in (1) are consequently distinct.  Thus every cubic \(D_4\)-flow
projects to a proper three-edge-colouring of \(G\).

If \(p\subset S\) is a coordinate pair, then \(Y_p\) contains exactly the
two Tait colour classes other than the class \(\{p,S\setminus p\}\).
It is therefore a disjoint union of alternating bichromatic circuits.
Transposing the two coordinates of \(p\) on one component of \(Y_p\)
interchanges those two active Tait colours on that component.  This is
exactly an ordinary Tait Kempe switch.

## Root-universality theorem

**Theorem.**  Every four-coordinate circuit-trapped Kempe orbit on a cubic
graph is root-universal.  In fact, every root pair is rescued either in the
starting state or after one component switch between used coordinates.

**Proof.**  Fix a state \(q\) in the orbit and two root edges \(r,s\).

If \(q(r)\cap q(s)\) contains a coordinate \(i\), then both roots lie in
\(C_i=Y_{it}\).  By the circuit-trap hypothesis, \(C_i\) is one circuit, so
the roots are already rescued.

It remains to consider disjoint labels.  Two disjoint two-subsets of the
four-element set \(S\) are complementary, so \(q(r)\) and \(q(s)\) have
the same Tait colour \(A\) under (1).  Choose either other Tait colour
\(B\).  The union of colour classes \(A\cup B\) is a factor \(Y_p\), where
\(\{p,S\setminus p\}\) is the third Tait colour.

If \(r,s\) lie on the same component of \(Y_p\), that component is a
factor circuit and they are already rescued.

Otherwise, switch the two coordinates of \(p\) on the component containing
\(r\).  This changes the Tait colour of \(r\) from \(A\) to \(B\), while
the colour of \(s\) remains \(A\).  Labels from two distinct classes in
(1) meet in exactly one coordinate; hence the new labels of \(r,s\) share
some coordinate \(k\).

The switched state remains in the assumed circuit-trapped orbit.  Its
coordinate class \(C'_k=Y'_{kt}\) is therefore one circuit containing both
roots.  They are rescued after the one switch. \(\square\)

## Why the degree-four contraction trap does not lift

The proof uses cubicity at two exact points:

1. the local xor triple projects to three distinct Tait colours; and
2. every \(Y_p\) is a union of alternating circuits on which a component
   switch changes the Tait colour of exactly the selected root component.

At the contracted degree-four vertex, four labels meet and this Tait
quotient is not a proper cubic edge-colouring.  The 12-state contraction
trap in `scratch/d5-contraction-generalized-circuit-no-go.md` therefore
does not contradict the theorem and cannot be transplanted unchanged to a
cubic state.

The theorem closes only the **fully circuit-trapped \(D_4\) branch**.  It
does not prove the general cubic rooted-orbit theorem.  A remaining
counterexample, if one exists, must use at least one of:

- a genuine five-coordinate state;
- a four-coordinate state with a disconnected coordinate class, allowing
  a nontrivial switch against the missing coordinate; or
- an orbit that moves between these two regimes.

## Finite algebra replay

Run:

```text
python3 scratch/check_d4_cubic_trap_root_universality.py
```

The standard-library checker exhausts all cubic local \(D_4\) xor triples,
the three complementary Tait classes, every ordered pair of disjoint root
labels, both choices of the second Tait colour, and both coordinate-pair
representatives of the excluded class.  It verifies that the selected
transposition changes only the chosen root's Tait class and makes its new
label intersect the untouched root label.

The seeded generator
`scratch/search_d4_trapped_root_orbit.py` independently constructs
four-face/Tait examples and explores their complete component-Kempe
orbits.  Its role is regression testing; the theorem above is not inferred
from those samples.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the Tait quotient,
proved the one-switch root-universality theorem, wrote the finite replay,
and drafted this note.
