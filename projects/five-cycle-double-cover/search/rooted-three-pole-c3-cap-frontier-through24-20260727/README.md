# Triangle-free rooted cap screen through order 24

Status: **finite two-implementation theorem; not Five-CDC**.

Snarkhunter generated every retained triangle-free 3-connected non-Tait
simple cubic cap at orders 20, 22, and 24:

| cap order | caps | vertex-deleted three-poles |
|---:|---:|---:|
| 20 | 128 | 2,560 |
| 22 | 1,161 | 25,542 |
| 24 | 12,612 | 302,688 |
| **total** | **13,901** | **330,790** |

For each three-pole, both classifiers examined every proper root edge.
All 10,824,084 root signatures are nonempty and contain at least one of
the three normalized base pairs.  There are no empty signatures and no
violations.

The CaDiCaL and direct finite-domain implementations made 33,363,003
label-existence calls each.  Their complete 10,824,084-row transcripts
are byte-for-byte identical and have raw SHA-256

```text
130180f347c4fe3f82b94eeb16c3c990be967680ef16a02283e4962383464c75
```

The normalized boundary word is \((01,02,12)\), and the three base pairs
are

```text
{12,03,04}, {02,13,14}, {01,23,24}.
```

The human triangle-induction theorem in
`../../docs/rooted-cap-triangle-induction.md` transports this closure
through root-end and connector-end \(K_4\) factors.  Consequently the
whole-shore mixed cyclic-three premise is now verified through cap order
26.  This is an independent finite route to a bound already superseded
by the endpoint-fork order-30 theorem; it does not improve that bound.

`verify.py` reconstructs every vertex deletion, checks the cap premises,
replays every transcript row, compares the implementations, checks all
shard statuses and summaries, and recomputes the totals.

Canonical source completeness and Snarkhunter option semantics rely on
the retained Snarkhunter 2.0b logs.  The verifier is not a second
canonical generator.

## AI-use disclosure

OpenAI Codex, under human direction, developed both classifiers, the
triangle-induction proof, the exhaustive run, the verifier, and this
package.  Universal claims used in the finite consequence are written
out in full; machine claims are reproducible from hashed sources and
complete transcripts.  No part of this package is represented as a
resolution of Five-CDC.
