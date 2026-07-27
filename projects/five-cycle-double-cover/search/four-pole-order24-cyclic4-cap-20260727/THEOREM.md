# Finite exceptional-pole exclusion through order 24

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE REDUCTION PLUS TWO-IMPLEMENTATION FINITE
ENUMERATION / SIMPLE TERMINAL-DISTINCT SCOPE / NOT FIVE-CDC**.

## Theorem

There is no bridge-free connected simple terminal-distinct cubic four-pole
on at most 24 internal vertices whose exact fixed-five \(D_5\) boundary
signature is one of the six ordered exceptional signatures of
Máčajová--Mazzuoccolo--Tabarelli.

Consequently any such exceptional pole has even order at least 26.

The theorem is about the fixed five-colour relation used by Five-CDC.  It
does not assert the arbitrary-colour version of their Conjecture 3.7.

## Proof

The degree sum of a terminal-distinct cubic four-pole on \(n\) internal
vertices is
\[
                  3(n-4)+2\cdot4=3n-4.
\]
It is even, so \(n\) is even.

The complete cap census in
`../four-pole-order22-cap-20260727/` already excludes every pole in the
stated scope through order 22.  Suppose, for a contradiction, that a pole
of order at most 24 has an exceptional signature.

The exact two-cut descent in
`../../docs/exceptional-four-cut-surviving-split-atoms.md` produces a
terminal atom of no larger order which:

1. is bridge-free, connected, simple, and terminal-distinct;
2. is two-cut reduced;
3. is vertex-minimal with its exceptional exact signature; and
4. still has one of the same two exceptional signature families.

No atom of order at most 22 exists, so this atom has order 24.

Corollary 2.1 of
`../../docs/rooted-three-pole-base-pair-closure-target.md` applies through
cap order 36.  It combines the simple-cap fork with the complete rooted
base-pair theorem through order 17 and excludes the surviving cyclic
three-cut interface.  Therefore the order-24 atom has a simple
cyclically 4-edge-connected cap \(G\).  Theorem 3.2 of
`../../docs/exceptional-four-pole-simple-cap-enumeration-reduction.md`
also proves that \(G\) is connected, simple, cubic, bridgeless, and
non-3-edge-colourable.  The two cap edges are independent, and deleting
them recovers the atom.

It remains to justify that the retained source contains \(G\).
A simple cubic graph of order 24 with cyclic edge-connectivity at least
four has no triangle.  Indeed, a triangle has three leaving edges.  Its
complement has 21 vertices and
\[
                  36-3-3=30
\]
internal edges, so the complement contains a circuit.  The triangle and
that circuit would be separated by a cyclic three-edge cut.  Hence \(G\)
has girth at least four.

The documented Snarkhunter command

```sh
snarkhunter 24 4 S s C4 o g
```

canonically generates the 155 simple cubic order-24 graphs that are
class 2, have girth at least four, and have cyclic edge-connectivity at
least four.  Thus \(G\) is one of the retained 155 records.  This source
completeness uses Snarkhunter 2.0b and its documented option semantics.

Deleting every independent edge pair from those 155 caps gives 86,490
four-poles.  Independent CaDiCaL and direct finite-domain implementations
agree byte-for-byte on the complete exact boundary tables.  Every row has
mask `0x3ff`, so every deletion pole realizes all ten fixed-five boundary
types.  No row can have one of the proper exceptional exact signatures.
In particular, the deletion that recovers the assumed atom is not
exceptional, a contradiction. \(\square\)

## Independent computational check

`verify.py` imports neither classifier.  It checks that all 155 records are
distinct connected simple cubic non-Tait graphs of order 24, have no
triangle, and have no cycle-separating cut of size at most three.  It then
reconstructs all 86,490 independent-edge deletions byte-for-byte and checks
both complete tables row-by-row.

The verifier does not independently implement canonical generation.
Completeness of the 155-record source therefore relies on the retained
Snarkhunter run.  The theorem's reduction from arbitrary exceptional poles
through order 24 also relies on the three human arguments cited above;
the finite table alone is not that reduction.

## Scope boundary

Nothing here covers:

* repeated terminal endpoints;
* nonsimple or multigraph four-pole cores;
* arbitrary-colour rather than fixed-five boundary signatures;
* order 26 or higher; or
* the orientable Five-CDC condition.

Excluding the published exceptional signatures at every order would remove
one four-cut branch in a minimum-counterexample analysis.  This finite
order-24 exclusion does not resolve that universal signature conjecture or
the Five-Cycle Double Cover Conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, assembled the reduction chain,
ran the two exact classifications, wrote the independent verifier, and
drafted this proof.  The exceptional signatures and cited structural
theorems are attributed in their source notes.  The proof and complete
finite evidence are exposed for human checking; this is not independent
human peer review.
