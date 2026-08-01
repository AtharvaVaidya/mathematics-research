# Even coordinate-changing local square lift fails for a fixed good state

Date: 2026-07-28

Status: **EXACT SOLVER-FREE LOCAL COUNTERMODEL / SURVIVING STAR-PARITY
TARGET / NOT KERNEL CLOSURE / NOT A COUNTEREXAMPLE TO THE EXISTENTIAL
STAR-FIBRE THEOREM OR TO FIVE-CDC**.

## 1. Quantifiers being tested

For a cubic graph \(H\), root \(r\), and independent nonroot edges
\(AC,BD\), replace those two edges by the square gadget
\[
 Aa,Bb,Cc,Dd,ab,bc,cd,da.
\]
Fix a vertex-star packing \(\mathcal T=(T_0,T_1,T_2)\) downstairs.
A **square-local lift of \(\mathcal T\)** keeps
\(T_i-\{AC,BD\}\) fixed outside the gadget and gives each gadget edge
multiplicity two.

The fixed-coordinate statement is already false in
`jaeger-star-exact-parity-four-cycle-lift-no-go.md`.  The stronger
statewise assertion is

> If \(\mathcal T\) is exact-good in at least one coordinate, some
> square-local lift of \(\mathcal T\) is exact-good in at least one
> coordinate, not necessarily the same one.                       \(\tag{S}\)

The countermodel below disproves (S).

This is still weaker than the existential fibre implication needed for
an induction:

> If the whole downstairs star fibre contains a good state, then the
> whole expanded star fibre contains a good state.                 \(\tag{F}\)

The example does not disprove (F); an explicit upstairs control witness
shows that (F) holds here.

## 2. The eight-vertex downstairs state

Use the labelled graph6 record

```text
G?zTb_
```

with root \(0\) and edge order

```text
 0:(0,4)   1:(0,5)   2:(0,6)   3:(1,4)
 4:(1,5)   5:(1,7)   6:(2,4)   7:(2,6)
 8:(2,7)   9:(3,5)  10:(3,6)  11:(3,7).
```

It is simple, cubic, planar, and 3-edge-connected.  Take

```text
T0 = {0,3,4,5,7,8,9}
T1 = {2,3,4,6,8,10,11}
T2 = {1,5,6,7,9,10,11}.
```

This is a star packing at root \(0\): each root edge occurs once and
every other edge twice.  Its odd kernels are

```text
K0 = {0,5,7,9}
K1 = {2,4,6,11}
K2 = {1,5,6,10}.
```

Thus \(K_0\cap K_1=\varnothing\), and coordinate two is exact-good.  The
complete defect profile is
\[
                              (2,2,0).                         \tag{1}
\]

## 3. Expansion and complete local enumeration

Expand
\[
                         AC=(1,7),\qquad BD=(2,4),
\]
using \(A=1,B=2,C=7,D=4\) and \(a,b,c,d=8,9,10,11\).  The expanded
edge order is

```text
 0:(0,4)   1:(0,5)   2:(0,6)   3:(1,4)   4:(1,5)
 5:(2,6)   6:(2,7)   7:(3,5)   8:(3,6)   9:(3,7)
10:(1,8)  11:(2,9)  12:(7,10) 13:(4,11)
14:(8,9)  15:(9,10) 16:(10,11) 17:(11,8).
```

This is again simple, cubic, and 3-edge-connected.  Its labelled graph6
record is

```text
KsWOHcG@GCgD
```

Every gadget edge has multiplicity two, so it has a unique omitted tree.
The \(3^8=6561\) omitted-owner words are therefore the complete local
search space.  Exactly 72 owner words make all three lifted edge sets
spanning trees.  Their defect profiles are:

```text
(2,2,2) : 38
(2,2,4) : 12
(2,4,2) :  2
(4,2,2) :  2
(4,4,2) : 18
```

Every coordinate of every one of the 72 legal lifts has positive defect.
This proves the failure of (S) without SAT, randomness, or an incomplete
generation step.

## 4. Changing the downstairs state rescues the same square

The same downstairs graph, root, and edge pair have another good state:

```text
R0 = {0,3,4,5,6,7,10}
R1 = {1,3,4,7,8,9,11}
R2 = {2,5,6,8,9,10,11}.
```

Its profile is \((0,2,2)\).  Unlike the countermodel state, it has the
following square-local lift:

```text
S0 = {0,3,4,5,8,10,11,12,13,14,15}
S1 = {1,3,4,5,6,7,9,11,14,16,17}
S2 = {2,6,7,8,9,10,12,13,15,16,17}.
```

The three local gadget masks in the order
\((Aa,Bb,Cc,Dd,ab,bc,cd,da)\) are

```text
00111111  11010010  11101101
```

and every gadget edge occurs twice.  The lifted profile is again
\[
                              (0,2,2).                         \tag{2}
\]
Consequently the expanded star fibre does contain a five-support state,
and it is obtained by a local lift after changing the selected downstairs
packing.  This precisely identifies the missing freedom: a square
reduction cannot be proved by lifting one already-selected good state.

## 5. Checker

Run

```sh
python3 scratch/verify_jaeger_star_square_any_coordinate_lift_countermodel.py
```

The independent standard-library checker:

1. verifies both graphs, both displayed packings, and 3-edge-connectivity;
2. reconstructs every odd kernel from subtree parities;
3. verifies the downstairs profile (1);
4. enumerates all \(3^8\) omitted-owner words and all 72 legal lifts;
5. regenerates the complete five-row profile histogram; and
6. verifies the alternate downstairs state and its good local lift (2).

## 6. Consequence for minimal-obstruction induction

The no-go is strong enough to reject both of the following local rules:

* preserve a prescribed good coordinate while lifting a fixed state;
* lift a fixed good state while allowing the output coordinate to change.

It is **not enough** to remove a four-cycle from an unrooted minimal
obstruction.  Such a reduction needs the whole-fibre implication (F), or
another selection theorem allowing changes outside the gadget.  The
control witness shows that the present graph satisfies (F), not that it
violates it.

Thus the exact unrooted reduction furnished by nonroot-triangle
contraction remains sound, but this work does not raise its conclusion
from triangle-free to girth at least five.  Nor does it establish cyclic
5-edge-connectivity.  The existential square contraction problem remains
open.

As a small positive control, exhaustive root-\(0\) tests on both
six-vertex connected cubic graphs found:

* \(K_{3,3}\): all 288 star states, each of the six eligible independent
  nonroot edge pairs; all \(1728\) state/pair instances admit an
  any-coordinate good local lift;
* the triangular prism: 156 good star states, each of the six eligible
  pairs; all \(936\) instances admit such a lift.

These order-six facts do not survive to the displayed order-eight state.
They are replayed by the companion exhaustive checker

```sh
python3 scratch/verify_jaeger_star_square_order6_controls.py
```

The two order-six graphs are vertex-transitive, so root \(0\) covers every
root orbit.  Four vertices cannot contain a root disjoint from the four
endpoints of two independent edges.  Hence the order-eight countermodel
is minimum-order among simple connected cubic instances of (S).

The stronger graph/root/pair-level existential statement nevertheless
passes completely at order eight.  The command

```sh
python3 scratch/verify_jaeger_star_square_existential_order8.py
```

hard-codes and checks the complete
`geng -cq -d3 -D3 8` stream.  Four of its five graphs are
3-edge-connected.  For all four graphs, all eight labelled roots, and all
21 eligible independent nonroot edge pairs, it finds some good
downstairs state with some good square-local lift:

```text
32 graph/root rows
672 graph/root/pair instances
688 good-state attempts before the 672 first witnesses
0 failures
```

This is an exact finite theorem, but it remains only order-eight evidence
for (F).

## AI-use disclosure

OpenAI Codex, under human direction, found the order-eight state, derived
the complete omitted-owner enumeration, produced the control witness, and
wrote the checker.  This is a certified countermodel to a local induction
lemma, not a proof or disproof of Five-CDC.
