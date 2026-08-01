# Terminal surface-Euler plateaus through order 12

Date: **2026-07-28**

Status: **COMPLETE FINITE CENSUS / NEW STRUCTURAL PROOF TARGET /
NOT A FIVECDC RESOLUTION**.

## Potential

For a \(D_5\)-flow \(q\) on a cubic graph with \(n\) vertices, let
\[
                       \Phi(q)=\sum_{i=0}^4\kappa(C_i)-\frac n2.
\]
By the coloured-triangulation dictionary,
\(\Phi(q)=\chi(S(q))\), the Euler characteristic of the normalized
properly 5-coloured surface dual to the graph.

A strict one-step ascent theorem is false.  Equal-\(\Phi\) switches are
essential.  Define a **\(\Phi\)-plateau** to be a connected component
of the Kempe state graph after retaining only equal-\(\Phi\) moves.
Call it **terminal** when none of its states has a
\(\Phi\)-increasing move.

Every state has a \(\Phi\)-nondecreasing path to a terminal plateau.
Therefore the following statement would prove orbit-rooted
transitivity:

> Every terminal \(\Phi\)-plateau is root-universal.

## Complete order-12 result

Across all 81 biconnected simple cubic graphs of order 12:

| quantity | count |
|---|---:|
| normalized \(D_5\)-flows | 25,960 |
| Kempe orbits | 2,650 |
| terminal \(\Phi\)-plateaus | 2,659 |
| failing terminal plateaus | **0** |

The terminal Euler characteristics range from \(-3\) to \(2\), and
terminal plateau sizes range from 1 to 432.  Thus the positive result
is not confined to planar/spherical states or to isolated maxima.

For every audited initial state and every unordered root-edge pair,
there is a path to a rooted factor circuit along which the surface
Euler characteristic never decreases.

## Why this survives the earlier no-gos

- Strict component-size ascent fails on the cube.
- Matroid-style orbit-circuit elimination fails on the Petersen graph.
- A disjoint-factor mediator can require at least three switches.
- A switch can change both genus and orientability of the coloured
  surface.

The terminal-plateau formulation permits arbitrarily many
Euler-neutral surgeries before the next handle cancellation.  It is
therefore compatible with all four obstructions.

The exact human theorem now needed is:

> **Terminal-plateau theorem.**  Let \(q\) be a \(D_5\)-flow on a
> connected bridgeless cubic graph.  If the equal-\(\Phi\) plateau of
> \(q\) has no outgoing \(\Phi\)-increasing switch, then for every
> pair of graph edges \(r,s\), some state in that plateau has a
> bichromatic boundary component containing both.

This theorem remains unproved.  The census isolates it as a coherent
global target rather than a bounded local move assertion.

## Exact one-switch Euler formula

The surface interpretation has an equivalent purely finite formula.
Fix coordinates \(i,j\), put \(A=C_i,B=C_j\), and suppress every
degree-two path in each noncircuit component of \(A\cup B\).  Label an
edge of the resulting cubic multigraph \(H_{ij}\) by its membership
vector
\[
             10,\quad01,\quad11
             \qquad\text{in }(A,B).
\]
Parity makes this a Tait colouring.  Let \(m_{10},m_{01},m_{11}\) be
the three fixed-point-free involutions on \(V(H_{ij})\) defined by its
three perfect matchings.

If \(K\) is a \(Y_{ij}\)-component, it is one alternating circuit of
\(m_{10}\cup m_{01}\).  Let \(W=V(K)\).  Switching \(i,j\) on \(K\)
replaces
\[
\begin{array}{c|cc}
 &W&V(H_{ij})-W\\ \hline
m'_{10}&m_{01}&m_{10}\\
m'_{01}&m_{10}&m_{01},
\end{array}
\qquad m'_{11}=m_{11}.                                        \tag{1}
\]
For two perfect matchings \(m_a,m_b\), their alternating-cycle count is
half the number \(z(m_am_b)\) of permutation cycles of their product.
All suppressed pure circuit components either remain fixed or merely
move from \(A\) to \(B\), so their total contribution cancels.  Hence
the exact Euler change is
\[
\Delta\Phi=
\frac12\bigl[
 z(m'_{10}m_{11})+z(m'_{01}m_{11})
-z(m_{10}m_{11})-z(m_{01}m_{11})
\bigr].                                                       \tag{2}
\]

Formula (2) is also the precise split/merge count for the two
coordinate-link circuit partitions.  It explains why a single switch
can change \(\Phi\) by more than two: one alternating \(K\)-circuit can
change transitions at arbitrarily many contacts with the
\(11\)-matching.

There is an important limit to a fixed interlacement argument.  Within
one fixed pair \(i,j\), switching \(K\) does not change the uncoloured
\(10/01\)-circuit \(K\), its \(11\)-matching chords, or their cyclic
interlacement word; it only exchanges the two alternating colours on
all of \(K\).  This is exactly the fixed Tait-core obstruction.  A
proof of the terminal-plateau theorem must use a neutral switch for a
different coordinate pair to change the interlacement core before
returning to \(i,j\).

## Reproduction

```text
python3 scratch/audit_d5_surface_chi_plateaus_order12.py \
  --output scratch/d5-surface-chi-terminal-plateaus-order12.json
```

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the normalized
surface Euler characteristic, formulated the terminal-plateau target,
ran the complete order-12 audit, and drafted this note.  This is finite
evidence and has not undergone peer review; it is not presented as a
resolution of FiveCDC.
