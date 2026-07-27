# Order-28 two-orbit classification and the scoped order-30 bound

Date: **2026-07-27**.

Status: **FINITE EXPLICIT-WITNESS THEOREM / SIMPLE
TERMINAL-DISTINCT FIXED-FIVE SCOPE / NOT FIVE-CDC**.

## Finite theorem

Every independent-edge deletion from every retained cyclically
4-edge-connected non-3-edge-colourable simple cubic graph of order 28
realizes both fixed-five boundary types
\[
                    (01,01,01,01)
        \quad\text{and}\quad
                    (01,01,23,23),
\]
up to coordinate permutation.  Consequently none of these deletion
four-poles has one of the six exceptional exact fixed-five signatures.

## Human-checkable reduction to two positive witnesses

The ten boundary orbits are indexed in the frozen canonical order.  In
that order, orbit 0 is \(AA=(01,01,01,01)\), and orbit 2 is the doubled
disjoint type \((01,01,23,23)\).  The six exceptional exact masks obey:

| exact mask | orbit 0 | orbit 2 | excluded by |
|:--|:--:|:--:|:--|
| `0x02b` | present | absent | orbit-2 witness |
| `0x053` | present | absent | orbit-2 witness |
| `0x119` | present | absent | orbit-2 witness |
| `0x2e4` | absent | present | orbit-0 witness |
| `0x3a4` | absent | present | orbit-0 witness |
| `0x3c4` | absent | present | orbit-0 witness |

An exact mask cannot describe a pole which realizes an orbit absent from
that mask.  Thus one explicit witness for each of orbits 0 and 2 excludes
all six masks.  No UNSAT inference is used.

## Complete finite evidence

The documented command

```sh
snarkhunter 28 4 S s C4 o g
```

canonically generated the retained 12,517 simple cubic order-28 graphs
that are class 2, have girth at least four, and have cyclic edge
connectivity at least four.  Source completeness uses Snarkhunter 2.0b
and its documented option semantics.

Deleting all independent edge pairs produces 9,725,709 four-poles.  A
CaDiCaL-backed producer found and emitted the two complete labellings
above for every row.  Each labelling assigns one of the ten two-subsets
of \([5]\) to every proper edge and semiedge.  The certificate checker
xors the three incident labels at every cubic vertex and requires zero.
The complete totals are

```text
rows          9,725,709
queries      19,451,418
witnesses    19,451,418
missing               0
```

The eight process status files are all zero, and their per-shard source,
pole, and witness totals sum to the displayed values.

The package verifier independently:

1. checks every retained source graph for order, cubicity, connectedness,
   bridgelessness, triangle-freeness, and non-Taitness;
2. reconstructs every independent-edge deletion in deterministic order;
3. compares it byte-for-byte with the retained pole stream;
4. checks the two boundary words and every vertex equation in every
   displayed labelling; and
5. checks all row counts, logs, statuses, and uncompressed stream hashes.

It does not independently regenerate the canonical source or recheck
cyclic four-connectivity; those two provenance claims rely on the retained
Snarkhunter run.  A second zlib/C++ checker uses the pole and witness
streams directly and independently reconstructs their incidence
semantics.  It also passes on all 9,725,709 rows and 19,451,418
labellings.

## Scoped order-30 corollary

Assume the vertex-minimal, two-cut-reduced, bridge-free, connected,
simple, terminal-distinct fixed-five exceptional-pole hypotheses of
`docs/rooted-cap-end-factor-fork-lift.md`.

That human theorem proves that an exceptional pole whose simple cap has a
cyclic three-edge cut has cap order at least 30.  The previous complete
cyclically-four classifications exclude cap orders through 26.  The
finite theorem above now excludes the only remaining order-28
cyclically-four case.

A terminal-distinct cubic four-pole has four degree-two vertices and all
other vertices of degree three.  If it has \(n\) vertices and \(m\)
proper edges, then
\[
                           3n-4=2m,
\]
so \(n\) is even.  There is therefore no intervening order 29.
Consequently every pole in the stated scope with an exceptional exact
fixed-five signature has order at least 30.

This corollary is a finite structural lower bound, not a proof that every
four-pole has full signature.

## Scope boundary

Nothing here covers:

* repeated terminal endpoints;
* nonsimple or multigraph pole cores;
* arbitrary-colour rather than fixed-five boundary signatures;
* the existence of a five-cycle double cover in every bridgeless graph;
  or
* orientable five-cycle double covers.

## AI-use disclosure

OpenAI Codex agents, under human direction, designed and ran the
classification, wrote the checkers, found the two-orbit certificate
reduction, and drafted this proof.  The finite certificates and human
argument are exposed for line-by-line checking.  “Independent” here means
separately written computational replay, not independent human peer
review.
