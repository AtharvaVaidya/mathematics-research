# Corrected finite order-24 cyclically-four cap theorem

Date: **2026-07-27**.

Status: **TWO-IMPLEMENTATION FINITE ENUMERATION / RETAINED
CYCLICALLY-FOUR CAP SCOPE / CORRECTED 2026-07-27 / NOT FIVE-CDC**.

## Theorem

Every one of the 86,490 terminal-distinct four-poles obtained by deleting
an independent edge pair from one of the retained 155 cyclically
4-edge-connected non-Tait simple cubic graphs of order 24 has the full
fixed-five \(D_5\) boundary signature.

The theorem is about the fixed five-colour relation used by Five-CDC.  It
does not assert the arbitrary-colour version of Conjecture 3.7 of
Máčajová--Mazzuoccolo--Tabarelli.

The former claim excluding every simple terminal-distinct exceptional pole
through order 24 is withdrawn.  Its cyclic-three reduction used the false
inference that a root signature containing a base pair retains every
relation-avoidance property of the base pair itself.  The counterexample
\[
 R=\{12,03,04,01\},\qquad S=\{01\},\qquad
 \operatorname{rel}(R,S)=\{\mathsf E,\mathsf I\}
\]
shows that the mixed exceptional orientation can survive.  See
`../../docs/rooted-three-pole-base-pair-closure-target.md` and
`../../docs/rooted-three-pole-tait-cap-closure.md`.

## Proof

A simple cubic graph of order 24 with cyclic edge-connectivity at least
four has no triangle.  Indeed, a triangle has three leaving edges.  Its
complement has 21 vertices and
\[
                  36-3-3=30
\]
internal edges, so the complement contains a circuit.  The triangle and
that circuit would be separated by a cyclic three-edge cut.  Hence every
graph in the intended cyclically-four class has girth at least four.

The documented Snarkhunter command

```sh
snarkhunter 24 4 S s C4 o g
```

canonically generates the retained 155 simple cubic order-24 graphs that are
class 2, have girth at least four, and have cyclic edge-connectivity at
least four.  This source completeness uses Snarkhunter 2.0b and its
documented option semantics.

Deleting every independent edge pair from those 155 caps gives 86,490
four-poles.  Independent CaDiCaL and direct finite-domain implementations
agree byte-for-byte on the complete exact boundary tables.  Every row has
mask `0x3ff`, so every deletion pole realizes all ten fixed-five boundary
types. \(\square\)

## Independent computational check

`verify.py` imports neither classifier.  It checks that all 155 records are
distinct connected simple cubic non-Tait graphs of order 24, have no
triangle, and have no cycle-separating cut of size at most three.  It then
reconstructs all 86,490 independent-edge deletions byte-for-byte and checks
both complete tables row-by-row.

The verifier does not independently implement canonical generation.
Completeness of the 155-record source therefore relies on the retained
Snarkhunter run.  No reduction from arbitrary exceptional poles is claimed.

## Scope boundary

Nothing here covers:

* repeated terminal endpoints;
* nonsimple or multigraph four-pole cores;
* arbitrary-colour rather than fixed-five boundary signatures;
* cyclic-three caps outside the retained source; or
* the orientable Five-CDC condition.

Excluding the published exceptional signatures at every order would remove
one four-cut branch in a minimum-counterexample analysis.  This retained
cap classification does not resolve that universal signature conjecture or
the Five-Cycle Double Cover Conjecture.

## AI-use disclosure

OpenAI Codex agents, under human direction, assembled the reduction chain,
ran the two exact classifications, wrote the independent verifier, and
drafted this proof.  The exceptional signatures and cited structural
theorems are attributed in their source notes.  The proof and complete
finite evidence are exposed for human checking; this is not independent
human peer review.
