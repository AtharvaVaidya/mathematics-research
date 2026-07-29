# Kempe escape from every order-fourteen boundary failure

Date: 2026-07-29

Status: **HUMAN-CHECKABLE GRAPH-INDEPENDENT DELETION THEOREM FOR ALL
224 FROZEN \(7+7\) FAILURES / NOT A FIVE-CYCLE-DOUBLE-COVER
RESOLUTION**.

## Result

The exhaustive order-fourteen boundary census has 224 failures of the
unqualified clean-or-delete map-choice lemma.  All occur on two
7-circuits, in exactly two component-size profiles:

```text
 46  profile 6+2+2+2+2
178  profile 4+4+2+2+2
```

Every one of these 224 abstract failures has a graph-independent Kempe
escape in the split-occurrence boundary model used by the circuit
census (in particular, in every cubic realization).  In a suitable
complement component, retain two low colours.
The resulting subgraph pairs its four or six odd boundary occurrences
by paths.  Regardless of the unknown pairing, at least one path can be
switched so that an explicit component-map assignment makes one
7-circuit omit a low colour.  Translating by that omitted colour and
deleting the circuit gives an extendable projection of size seven.

Therefore none of the 224 order-fourteen failures can be a globally
cardinality-minimum extendable projection in such a realization.

## The six-block refinement

Of the 46 states with a six-occurrence component:

- 26 use the two colours present at all six terminals, hence three
  Kempe paths;
- 20 require the two-colour subgraph containing the four majority
  terminals and the absent colour, hence two Kempe paths.

The second case is essential.  It is the rigid-six-pole Kempe move:
switching a path changes two majority-colour terminals to the formerly
absent colour.  An audit restricted to all six terminals misses 20 of
the 46 states.

For a path joining different support circuits, the switch temporarily
changes both circuit closure equations by the same nonzero value.  A
two-terminal path in another component supplies the same switch and
restores both closures.  In four \(3+1\) terminal-distribution cases no
such cross repair is available, but every perfect matching contains a
same-circuit pair among the three terminals on one circuit.

## Certificates

`failure-states.txt` is the complete list of 224 raw failures emitted by
the primary exhaustive \(7+7\) census.  A sibling package independently
regenerates all 333 word orbits, 91,481,505 charge-valid partitions, and
80,104,020 dirty states with a separately written valid-block exact-cover
enumerator.  It obtains the same 224-row failure set; the sorted-row
SHA-256 is
`eec4d091247385ab4aef5c567e52377062d6a7eae8f68e988069c1a3920215ca`.

`all-kempe-certificates.json` contains a pairing-robust strategy for
every state.  For four terminals it stores three endpoint-pair rows;
for six terminals it stores five.  Those rows hit all three or all
fifteen possible perfect matchings, respectively.  Every row gives:

- the primary path endpoints and any auxiliary path;
- five explicit \(\operatorname{GL}(2,2)\) maps;
- the integrated low words on the two 7-circuits;
- a deleted circuit and a colour absent from it;
- the exhaustive feasible-map and deletion-map counts.

There are 724 literal deletion rows in total:
\[
                   198\cdot3+26\cdot5=724.
\]

The short proof, including 27 fully displayed representative rows, is
in `HUMAN-PROOF.md`.

## Reproduction

The exhaustive builder independently confirms that every frozen input
is an unrestricted failure, searches all normalized component-map
tuples, and regenerates the JSON:

```sh
python3 build_all_certificates.py
```

The separately written literal checker does not repeat that search.  It
checks the matching-hitting condition and directly replays all 724
stored switches, maps, circuit integrations, and omitted-colour
deletions.  `verification-output.txt` freezes both checker outputs:

```sh
python3 verify_all_certificates.py
python3 verify_certificates.py
shasum -a 256 -c SHA256SUMS
```

Expected all-state checker output:

```text
states=224
profiles=46*(6+2+2+2+2),178*(4+4+2+2+2)
four-terminal strategies on six-blocks=20
literal deletion rows=724
PASS: every perfect matching hits a checked deletion row
```

## Scope and disclosure

This theorem removes every split-occurrence boundary obstruction at
total support size fourteen from the globally-minimum route.  A
reduction from arbitrary higher-degree vertices to that model is not
proved in this package.  The theorem also does not control possible
larger boundary obstructions and does not prove the five-cycle double
cover conjecture.

OpenAI Codex agents under human direction found the Kempe escape,
derived the proof, ran the exhaustive search, wrote a separately
implemented literal checker, and prepared this package.  The
graph-theoretic implication is the path-switch lemma; the remaining
finite claims are exposed as literal, replayable certificates.
