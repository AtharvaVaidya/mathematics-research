# Order-34 full-\(H\) one-move trap

## Scope and claim

This package proves a finite computational proposition about one particular
nowhere-zero \(\mathbb F_2^3\)-flow.  It does **not** resolve the Five-Cycle
Double Cover Conjecture and it does **not** give a counterexample to that
conjecture.  In fact, an explicit standard FiveCDC of the graph is included
below.

The proposition checked here is:

> There is a simple, connected, bridgeless, cubic, non-3-edge-colourable
> graph \(G\) of order 34, and a full-span nowhere-zero
> \(\mathbb F_2^3\)-flow \(f\), for which all seven full-\(H\) systems fail
> and every legal addition \(f+h\chi_Z\) on a nonempty binary cycle \(Z\)
> also has all seven systems fail.  Nevertheless, a successful full-\(H\)
> flow is reached in two legal additions.

Thus the tempting universal assertion “every all-fail flow on a snark has a
successful one-move neighbour” is false.  The weaker radius-two assertion is
not decided by this example and remains open.

No priority or literature-novelty claim is made here.  This appears to be a
new computational observation within this project, but a targeted literature
review and independent mathematical review are required before scholarly
submission.  On its own it is best viewed as a reproducible negative lemma or
preprint appendix, not as a resolution of FiveCDC.

## Prior-art boundary

Hušek and Šámal, *Exponentially Many Circuit Double Covers*,
[arXiv:2607.24724](https://arxiv.org/abs/2607.24724), Theorem 3.16 and
Conjecture 3.19, already give the underlying exact flow criterion: for a
nowhere-zero \(\mathbb F_2^3\)-flow, FiveCDC is equivalent to choosing the
flow so that each relevant component contains an even number of endpoints
of the distinguished value class.  The full-\(H\) systems used here are a
restricted circuit-switching reconfiguration of that prior criterion.
Neither the flow equivalence nor the component-parity theorem is claimed as
new here.  The scoped contribution of this package is only the explicit
order-34 local trap, its complete one-move census, and its exact two-move
escape.

## Frozen graph and flow

The graph6 record is

```text
ahc?GC@?G?_`_?C?g?G?@@?C?GGC?G?GCG?@??CG@??_??@G??@????_???GA??@????C???@G?_??G???@C????H??_@?G
```

Edges are numbered in native graph6 upper-triangle order.  The graph has 34
vertices and 51 edges.  The two checkers establish that it is simple, cubic,
connected, bridgeless, nonplanar, has girth 5 and cyclic edge-connectivity 4,
and is not 3-edge-colourable.  A cyclic 4-cut is formed by edge IDs
\(\{6,9,19,27\}\).

The frozen flow, indexed by edge ID, is

```text
[2,5,2,1,6,6,2,4,2,5,4,2,3,4,6,7,2,
 5,2,6,7,4,4,3,6,7,7,1,3,6,6,5,3,7,
 5,2,3,6,1,7,1,5,7,4,2,3,2,1,5,6,3]
```

Every value is nonzero, the XOR of the three incident values is zero at
every vertex, and the values span all of \(\mathbb F_2^3\).

For a plane \(H\), the semantic checker contracts every connected component
of the \(H\)-valued edges.  For an outside representative \(d\), it forms
the target boundary of the \(d\)-valued edges.  Each outside circuit and
each nonzero \(h\in H\) supplies the contracted boundary of the circuit
edges valued \(d\) or \(d+h\).  The full-\(H\) system succeeds exactly when
the target lies in the binary span of those columns.  Both implementations
evaluate this condition directly for all seven planes.

The connected graph has binary cycle-space dimension
\(51-34+1=18\), so there are exactly \(2^{18}=262{,}144\) binary cycles.
The complete enumeration finds 19,193 legal nonempty additions:

```text
increment h:       1     2     3     4     5    6     7
legal additions: 8191   255  2047  4095  2047  511  2047
```

All 19,193 resulting flows have success mask zero.  The FNV-1a-style
64-bit replay checksum of the ordered legal neighbourhood is
`3cfa857e5d405801`.

Since the initial flow and its complete one-neighbourhood all fail, the
success distance is greater than one.  The following two legal additions
give a success, proving the distance is exactly two:

```text
first:  cycle edge mask 31,             increment 3
second: cycle edge mask 57287149911532, increment 5
final success mask: 64
```

The complete intermediate and final flow words are frozen in
`fullh-order34-local-trap-certificate.jsonl`.

## Explicit standard FiveCDC

Each duad `ij` on an edge means that the edge belongs to \(C_i\) and \(C_j\).
This makes “covered exactly twice” immediate.  The edge endpoints and duads
are:

| edge | endpoints | duad |
|---:|:---:|:---:|
| 0 | 0–1 | 24 |
| 1 | 1–2 | 45 |
| 2 | 2–3 | 34 |
| 3 | 0–4 | 34 |
| 4 | 3–4 | 14 |
| 5 | 5–6 | 45 |
| 6 | 6–7 | 24 |
| 7 | 7–8 | 23 |
| 8 | 8–9 | 13 |
| 9 | 9–10 | 14 |
| 10 | 5–11 | 35 |
| 11 | 10–11 | 45 |
| 12 | 0–12 | 23 |
| 13 | 3–13 | 13 |
| 14 | 12–13 | 35 |
| 15 | 1–14 | 25 |
| 16 | 13–14 | 15 |
| 17 | 14–15 | 12 |
| 18 | 5–16 | 34 |
| 19 | 15–16 | 13 |
| 20 | 10–17 | 15 |
| 21 | 16–17 | 14 |
| 22 | 6–18 | 25 |
| 23 | 17–18 | 45 |
| 24 | 11–19 | 34 |
| 25 | 18–19 | 24 |
| 26 | 4–20 | 13 |
| 27 | 19–20 | 23 |
| 28 | 15–21 | 23 |
| 29 | 20–21 | 12 |
| 30 | 8–22 | 12 |
| 31 | 21–22 | 13 |
| 32 | 22–23 | 23 |
| 33 | 2–24 | 35 |
| 34 | 23–24 | 34 |
| 35 | 24–25 | 45 |
| 36 | 25–26 | 24 |
| 37 | 7–27 | 34 |
| 38 | 26–27 | 23 |
| 39 | 27–28 | 24 |
| 40 | 25–29 | 25 |
| 41 | 28–29 | 23 |
| 42 | 9–30 | 34 |
| 43 | 29–30 | 35 |
| 44 | 26–31 | 34 |
| 45 | 30–31 | 45 |
| 46 | 28–32 | 34 |
| 47 | 31–32 | 35 |
| 48 | 12–33 | 25 |
| 49 | 23–33 | 24 |
| 50 | 32–33 | 45 |

Equivalently, the five Eulerian edge-subsets are

```text
C1 = {4,8,9,13,16,17,19,20,21,26,29,30,31}
C2 = {0,6,7,12,15,17,22,25,27,28,29,30,32,36,38,39,40,41,48,49}
C3 = {2,3,7,8,10,12,13,14,18,19,24,26,27,28,31,32,33,34,37,38,41,42,43,44,46,47}
C4 = {0,1,2,3,4,5,6,9,11,18,21,23,24,25,34,35,36,37,39,42,44,45,46,49,50}
C5 = {1,5,10,11,14,15,16,20,22,23,33,35,40,43,45,47,48,50}
```

For a direct human check, use the endpoint table to verify that every vertex
has degree zero or two in each \(C_i\).  The independent verifier performs
exactly this incidence-parity check, without using the full-\(H\) code.

## Files

* `audit_fullh_order34_local_trap_certificate.cpp` is the exhaustive C++
  generator/checker.
* `search_qfull_one_move_random_wide.cpp`,
  `search_six_point_star_perpacking_parity.cpp`, and
  `census_jaeger_two_tree_exchange_through14.cpp` are the frozen local
  implementation dependencies included so that the C++ replay is
  self-contained.
* `fullh-order34-local-trap-certificate.jsonl` is its frozen output.
* `verify_fullh_order34_local_trap.py` is an independently written semantic
  checker.  It independently parses graph6, checks graph metadata and
  non-3-edge-colourability, reconstructs the cycle space, re-evaluates every
  full-\(H\) system for every legal neighbour, checks the distance-two path,
  and checks the displayed FiveCDC.
* `SHA256SUMS` pins all package files other than the manifest itself.

## Exact replay

Run from the repository root.  A C++20 compiler and Python 3 with NetworkX
3.x are required.

```sh
c++ -std=c++20 -O2 \
  -DSIX_POINT_PARITY_MAX_N=40 \
  -DSIX_POINT_PARITY_MAX_M=60 \
  scratch/fullh-order34-local-trap-20260729/audit_fullh_order34_local_trap_certificate.cpp \
  -o /tmp/audit_fullh_order34_local_trap_certificate

/tmp/audit_fullh_order34_local_trap_certificate \
  > /tmp/fullh-order34-local-trap-certificate.jsonl

cmp /tmp/fullh-order34-local-trap-certificate.jsonl \
  scratch/fullh-order34-local-trap-20260729/fullh-order34-local-trap-certificate.jsonl

python3 \
  scratch/fullh-order34-local-trap-20260729/verify_fullh_order34_local_trap.py

(cd scratch/fullh-order34-local-trap-20260729 && shasum -a 256 -c SHA256SUMS)
```

Expected independent-checker output:

```text
PASS: independent order-34 full-H local-trap replay
graph: simple cubic, nonplanar, girth 5, cyclic connectivity 4
non-Tait; all 19,193 legal one-move neighbours still fail
shortest successful full-H distance: 2
explicit standard FiveCDC: verified
```

## AI-use and review disclosure

OpenAI Codex agents generated the conjectural reconfiguration questions,
implemented the searches and independent checker, found and corrected an
edge-ordering error during cross-checking, and drafted this documentation
under the direction of the human repository owner.  The computations have
not been peer reviewed.  Any preprint or submission using this package
should disclose that AI involvement explicitly, identify the human authors
who independently reviewed and take responsibility for the claims, and
avoid presenting this finite negative lemma as a resolution of FiveCDC.
