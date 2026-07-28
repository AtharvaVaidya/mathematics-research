# The sorted seven-defect profile is not a one-step descent potential

Date: 2026-07-28

Status: **EXACT FINITE COUNTERMODEL TO AN AUXILIARY LOCAL-DESCENT
CLAIM.  THE FULL SAME-\(d_{\min}\) COMPONENT ESCAPES IN TWO EXCHANGES.
THIS IS NOT A FIVE-CYCLE DOUBLE COVER COUNTEREXAMPLE.**

## 1. Claim tested

For a Jaeger vertex-star state, let
\[
 (d_1,\ldots,d_7)
\]
be the seven exact Fano-plane component defects and let
\[
 \sigma=\operatorname{sort}(d_1,\ldots,d_7)
\]
in nondecreasing order.  The following attractive strengthening of the
open plateau statement is false:

> If \(d_{\min}>0\), some legal reciprocal two-tree exchange
> lexicographically decreases \(\sigma\).

This matters because the previously rejected potential
\((d_{\min},\sum_h d_h)\) loses information.  Sorting the entire profile
retains every coordinate value up to Fano-plane permutation, but still is
not a discrete-convex exchange potential.

## 2. Literal state

Use the 36-vertex simple cubic graph

```text
chc?GC@@G?_P?H??_?G?@??C??G?@G??C??P??@G?A?__?@_???C???g???GA??@?A??CG???G???GG????C_???@??A??G??A??_???OH
```

in standard graph6 upper-triangle edge order.  Take root \(0\), assign
its three spokes to the tree coordinates in edge order
\[
 (31,3,0),
\]
and encode the three omitted classes among the other 51 edges by

```text
(1273387172628768, 107323987641370, 871088653415109).
```

Each mask has 17 bits and the three masks partition the 51 internal
edges.  Complementing one mask and adding its assigned spoke gives a
35-edge spanning tree.  The unique odd-degree subforests of these three
trees induce the exact ordered defect profile
\[
 (6,6,2,4,2,2,2),
\]
and therefore
\[
 \sigma=(2,2,2,2,4,6,6)>0.                         \tag{1}
\]

The graph is simple, cubic, and remains connected after deleting any
set of at most two edges.

## 3. Complete neighbourhood calculation

A reciprocal exchange chooses two of the three omitted classes and one
edge of each class.  There are exactly
\[
 3\cdot17\cdot17=867
\]
candidates.  Reconstructing the two changed complements and applying
the spanning-tree test leaves exactly 63 legal exchanges.

For every legal neighbour, reconstruct the three odd kernels, label an
edge by coordinate \(i\) precisely when it is absent from kernel \(K_i\),
and compute the exact component defects for all seven nonzero
functionals.  Comparison with (1) gives

| relation to \(\sigma\) | legal neighbours |
|---|---:|
| lexicographically lower | 0 |
| equal | 13 |
| higher | 50 |

All 13 equal neighbours preserve even the ordered profile
\((6,6,2,4,2,2,2)\).  Thus the displayed state is an exact positive
strict local minimum after equal moves are contracted only if one
forbids moving through the equal class.  It disproves the one-exchange
sorted-profile claim.

## 4. Why this does not refute the surviving plateau theorem

Breadth-first search from the displayed state, using only exchanges that
keep \(d_{\min}=2\), reaches a lower level in two moves.  One shortest
literal path is

```text
(1273387172628768, 107323987641370, 871088653415109)
profile (6,6,2,4,2,2,2)

(1273387172628752, 107323987641386, 871088653415109)
profile (6,6,2,4,4,2,2)

(1273387172629520, 107323987640618, 871088653415109)
profile (6,6,2,4,4,2,0).
```

The deterministic breadth-first order inserts 57 same-level states
before finding the last edge.  Hence this witness reinforces, rather
than removes, the exact logical distinction:

- immediate descent for \(d_{\min}\) is false;
- immediate descent for the full sorted profile is also false;
- escape through the whole same-\(d_{\min}\) component remains open.

## 5. Independent checker

Run

```sh
python3 scratch/verify_jaeger_sorted_profile_local_no_go_order36.py
```

The checker uses only the Python standard library.  It independently:

1. decodes the literal graph6 record;
2. checks simplicity, cubicity, and every deletion of at most two edges;
3. reconstructs all three spanning trees and their unique odd kernels;
4. checks the derived nowhere-zero \(\mathbb F_2^3\)-flow at every
   vertex;
5. reconstructs all seven exact component-parity defects;
6. enumerates all 867 candidate and all 63 legal reciprocal exchanges;
7. checks the \(0/13/50\) lower/equal/higher split; and
8. replays the two-exchange same-level escape.

No SAT solver, graph library, or discovery-program output is trusted by
this replay.

## 6. Scope

The graph already has a directly checked standard five-cycle double
cover in the separate APX countermodel package.  This state is therefore
not evidence against FiveCDC.  Its precise use is to rule out a tempting
majorization/discrete-convexity proof of the Jaeger plateau theorem.

## AI-use disclosure

OpenAI Codex agents, under human direction, proposed the sorted-profile
potential, found the countermodel by exact-neighbour search, wrote the
independent checker, and drafted this note.  The finite claim is fully
specified above and reproducible from the literal graph and masks.  It
has not yet received independent human peer review.
