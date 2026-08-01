# A minimum-order full-boundary four-pole for FiveCDC

Date: 2026-07-28

Status: **HUMAN-CHECKABLE LOCAL REDUCTION WITH AN INDEPENDENT FINITE
CHECKER.  THIS DOES NOT RESOLVE FIVECDC.**

## 1. Statement

Let \(D_5=\binom{[5]}2\), written as two-digit pair labels.  A boundary
word of a cubic four-pole is admissible when its four labels xor to zero.

Take the cube with edge set

```text
(0,1) (0,3) (0,4) (1,2) (1,7) (2,3)
(2,6) (3,5) (4,5) (4,7) (5,6) (6,7)
```

and delete the adjacent vertices \(0,1\).  The remaining proper core has
ports

```text
(2,3,4,7)
```

and proper edges, in certificate order,

```text
(2,3) (2,6) (3,5) (4,5) (4,7) (5,6) (6,7).
```

> **Theorem.** Every one of the 640 ordered xor-zero words in \(D_5^4\)
> extends through this six-vertex four-pole.  Moreover, six is the minimum
> possible order of a connected simple terminal-distinct cubic four-pole
> with the full boundary relation.

The proper core is simple, connected, and bridgeless.  Therefore, by the
standard pair-label insertion lemma, it may replace two independent edges
of a FiveCDC-positive simple cubic bridgeless graph using any of the
\(4!\) port bijections, while preserving FiveCDC, simplicity, cubicity,
and bridgelessness.

## 2. Ten-row certificate

The ten xor-zero boundary orbits under \(S_5\) have representatives below.
The last column lists labels on the seven proper edges in the order above.

| type | port labels | proper-edge labels |
|---|---|---|
| AA | `02 02 02 02` | `12 01 01 12 01 02 12` |
| AT2 | `02 02 03 03` | `01 12 12 02 23 01 02` |
| AT3 | `02 03 02 03` | `23 03 02 12 01 01 13` |
| AT4 | `02 03 03 02` | `01 12 13 34 04 14 24` |
| T2T2 | `02 02 13 13` | `24 04 04 14 34 01 14` |
| T2T3 | `02 03 12 13` | `23 03 02 24 14 04 34` |
| T2T4 | `02 03 13 12` | `23 03 02 12 23 01 13` |
| T3T3 | `02 13 02 13` | `03 23 01 12 01 02 03` |
| T3T4 | `02 13 03 12` | `23 03 12 02 23 01 13` |
| T4T4 | `02 13 13 02` | `03 23 01 12 23 02 03` |

At each of the six completed vertices, xor the three incident labels.
Every row gives zero.  Simultaneously permuting the five coordinates
preserves weight two and every vertex equation.  The orbit sizes are

```text
10, 60, 60, 60, 30, 120, 120, 30, 120, 30,
```

which sum to 640 and are exactly the ten admissible boundary orbits.
This proves full boundary without a SAT solver.

## 3. Minimum order

Let a connected simple terminal-distinct cubic four-pole have \(n\)
proper vertices.  Four specified vertices have degree two and every other
vertex has degree three, so

\[
                         2m=3n-4.
\]

Thus \(n\) is even and \(n\ge4\).  If \(n=4\), all vertices are ports and
the connected simple proper core is 2-regular, hence it is \(C_4\).
This is exactly the pole obtained by deleting adjacent vertices of
\(K_{3,3}\).  Its boundary relation has 580 of the 640 admissible words
and omits the orbit represented by `02 02 03 03`; a direct nonextension
proof and complete checker are in the four-pole preprint package.
Consequently no order-four pole is full-boundary.  The displayed
order-six cube pole proves the lower bound sharp.

## 4. Independent replay

Run

```sh
python3 scratch/verify_cube_four_pole_full_boundary_20260728.py
python3 scratch/verify_k33_four_pole_boundary_20260728.py
```

The first standard-library checker verifies the literal graph, degree
pattern, edge-by-edge bridgelessness, all ten rows, their orbit sizes, and
exact coverage of all 640 admissible words.  The second independently
checks the unique order-four core's 580-word relation and missing orbit.

## Scope and AI-use disclosure

This theorem supplies a smaller positive reducible configuration than the
Heawood pole.  It does not show that a prospective minimal counterexample
contains the cube pole, and it does not prove FiveCDC.  The multipole
boundary framework is prior work; whether this particular full-boundary
certificate has appeared previously requires specialist review.

OpenAI Codex agents, under human direction, found the certificate, wrote
the checker, and drafted this note.  The table is directly checkable by
humans and the finite calculation is reproducible.  It has not received
independent human peer review.
