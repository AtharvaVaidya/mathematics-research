# Independent size-fourteen \(7+7\) audit and Kempe escape

Date: 2026-07-29

Status: **INDEPENDENT EXACT \(7+7\) BRANCH THEOREM / NOT A FIVECDC
RESOLUTION**.

This package independently regenerates the complete size-fourteen
\(7+7\) boundary census and independently proves that every one of its
224 clean-or-delete failures is excluded by global projection
minimality.

The resulting scoped theorem is:

> In a finite loopless cubic multigraph, every globally
> cardinality-minimum extendable projection whose support is the
> disjoint union of two 7-circuits is cleanable.

Parallel edges are allowed.  Loops, noncubic graphs, other
size-fourteen shapes, and larger supports are not covered here.  The
full Five-Cycle Double Cover Conjecture remains unresolved.

## Reproduce

The complete independent census uses up to eight local C++ worker
processes:

```sh
python3 replay_full_census.py
```

The separate semantic and Kempe-certificate audit takes only a few
seconds:

```sh
python3 independent_audit.py
```

Then verify every frozen byte:

```sh
shasum -a 256 -c SHA256SUMS
```

No network access or third-party Python package is required.  The full
census compiles C++17 with
`-O3 -std=c++17 -Wall -Wextra -pedantic`.

## Independent census

`independent_word_orbits.py` regenerates all proper \(7+7\) word
orbits under first-occurrence colour normalization, the two dihedral
actions, and interchange of the equal circuits.  It obtains 333
orbits.

`independent_full_census.cpp` does not use the primary derivative-subset
partition generator.  It characterizes a valid component block by the
equal parity of the four low colours on its support cut, then generates
partitions as anchored exact covers by valid blocks.  Section 2 of
`HUMAN-PROOF.md` proves this cut-parity condition equivalent to zero
boundary charge.  The independent totals are:

| quantity | exact value |
|---|---:|
| word orbits | 333 |
| charge-valid partitions | 91,481,505 |
| dirty states | 80,104,020 |
| direct-cleaning failures | 37,463 |
| failures of both cleaning and deletion | 224 |

The independently regenerated 224-row failure set agrees exactly with
the primary set.  Its sorted-row SHA-256 is

```text
eec4d091247385ab4aef5c567e52377062d6a7eae8f68e988069c1a3920215ca
```

`full-replay-output.txt` freezes a complete successful replay.

## Independent Kempe audit

`independent_audit.py` shares no implementation with the full census.
It parses all 224 frozen rows and reconstructs the word derivative,
block charges, dirtiness, normalized component-map orbit, circuit
integrations, cleaning parity, and missing-colour deletion test.
Every row is independently confirmed to have 320 feasible normalized
map assignments and initially no clean or deletion map.

For a complement component and a pair of nonzero low colours, the
two-colour subgraph of any loopless cubic realization pairs its selected
boundary occurrences by paths.  The checker enumerates every possible
perfect matching of those occurrences.  It accepts a strategy only if
every matching contains an endpoint pair with a literal deletion
certificate.  A cross-circuit switch is allowed only when another
component has a forced two-terminal cross-circuit path of the same
colour pair.

The exact audit gives:

| quantity | exact value |
|---|---:|
| failure profile \(6+2+2+2+2\) | 46 |
| failure profile \(4+4+2+2+2\) | 178 |
| perfect-matching obligations | 984 |
| selected literal deletion witnesses | 1,566 |
| witnesses needing no compensation | 750 |
| witnesses using a forced compensating path | 816 |

The canonical certificate content has SHA-256

```text
5c08f4a410a55c3460cb8742567a9da8613cf44faaf84d5b3a4df107a5c6724b
```

`certificates.json` contains every selected strategy, good endpoint
pair, optional auxiliary endpoints, five component maps, integrated
base word, deleted circuit, and missing colour.  The checker reconstructs
the complete JSON object and compares it with this frozen file.

## Files

- `HUMAN-PROOF.md` gives the graph-independent proof, including why
  quantifying over all terminal perfect matchings is sufficient.
- `independent_word_orbits.py` regenerates the 333 word orbits.
- `independent_full_census.cpp` exhausts all valid-block exact covers.
- `replay_full_census.py` runs the sharded census and compares the exact
  totals and failure set.
- `independent_audit.py` independently rechecks all failure semantics
  and Kempe escapes.
- `census-7+7.txt` freezes the primary census used only for the exact
  failure-set comparison and second audit.
- `certificates.json` freezes all literal Kempe deletion certificates.
- `full-replay-output.txt` and `SHA256SUMS` freeze the successful run.

## Trust boundary and AI disclosure

The package independently checks the full \(7+7\) boundary census and
the graph-independent Kempe deletion of every residual row.  It relies
on the broader project's affine cleaning lemma to identify the checked
boundary cleanliness condition with the minimum-projection cleaning
move.  It does not prove any reduction from general bridgeless graphs
to this one cubic support shape.

OpenAI Codex agents under human direction found the Kempe escape and
wrote the programs and exposition.  All source, data, certificates, and
hashes are supplied for human verification.  This has not yet received
independent human peer review, and no literature-wide priority claim is
made.
