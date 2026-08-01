# The direct Hušek--Šámal one-switch frontier

Date: 2026-07-28

Status: **direct radius-one domination is false even on a strict
26-vertex snark, including when a value class already packs.  A
packing-to-multi-switch lemma is proved.**
Nothing in this note is a resolution of FiveCDC.

## 1. Exact formulation

Let \(G\) be a finite loopless cubic graph and let
\[
             f:E(G)\longrightarrow \mathbb F_2^3\setminus\{0\}
\]
be a nowhere-zero flow.  Identify a nonzero linear functional with
\(\mu\in\mathbb F_2^3\), using
\(\mu(x)=\langle\mu,x\rangle\).  Put
\[
 K_\mu(f)=\{e:\mu(f(e))=0\}.
\]
For any \(r\) with \(\mu(r)=1\), let \(Z_r(f)\) be the set of endpoints
of the matching \(M_r(f)=\{e:f(e)=r\}\).

The component defect is
\[
 d_\mu(f)=
 \#\{X\in\operatorname{Comp}(V(G),K_\mu(f)):
                         |X\cap Z_r(f)|\ \hbox{is odd}\}.                 \tag{1}
\]
Flow conservation makes the parity in (1) independent of the choice
of the four affine values \(r\) satisfying \(\mu(r)=1\).  We call \(f\)
**H--S-good** if \(d_\mu(f)=0\) for some \(\mu\ne0\).

Hušek and Šámal, Observation 3.15 and Theorem 3.16, prove that an
H--S-good flow produces a standard FiveCDC.  Their Conjecture 3.19 says
that every bridgeless graph has some H--S-good flow, and they prove
that this is equivalent to FiveCDC:

- [Hušek--Šámal, *Exponentially Many Circuit Double Covers*,
  arXiv:2607.24724](https://arxiv.org/abs/2607.24724).

A **legal simple-cycle switch** is a pair \((a,C)\), where
\(a\in\mathbb F_2^3\setminus\{0\}\), \(C\) is a simple cycle of \(G\),
and \(C\cap M_a(f)=\varnothing\).  Define
\[
 f^{a,C}(e)=
 \begin{cases}
 f(e)+a,&e\in C,\\
 f(e),&e\notin C.
 \end{cases}                                                           \tag{2}
\]
The cycle condition preserves flow conservation.  Avoiding \(M_a(f)\)
ensures that (2) is nowhere zero.  This is the connected-cycle
adjacency studied in:

- [Cranston et al., *Reconfiguration of Nowhere-zero Flows*,
  arXiv:2606.24685](https://arxiv.org/abs/2606.24685).

The natural reduced auxiliary statement was:

> **Reduced direct H--S one-switch lemma (refuted).**  
> If \(G\) is a finite simple cubic cyclically 4-edge-connected graph
> and \(f\) is a nowhere-zero \(\mathbb F_2^3\)-flow, then either \(f\)
> is H--S-good or \(f^{a,C}\) is H--S-good for some legal
> simple-cycle switch \((a,C)\).

This is deliberately a statement about the current H--S component
condition.  It is not the older assertion that one of the seven
value-class matchings packs two disjoint \(T\)-joins.  Section 5 gives
an exact strict-snark countermodel.

## 2. A human-checkable bridge from packing to reconfiguration

The two frontiers are distinct, but they are related by the following
elementary lemma.

> **Packing-to-switch lemma.**  
> Fix \(a\ne0\) and \(\mu(a)=1\).  Let
> \(F=\{e:\mu(f(e))=1\}\), \(M=M_a(f)\), and \(J_0=F-M\).
> If \(G-M\) contains two edge-disjoint \(\partial M\)-joins
> \(J_1,J_2\), then switching \(a\) on the even subgraph
> \[
>                         C=J_0\mathbin\triangle J_1                 \tag{3}
> \]
> produces an H--S-good flow.  The support \(C\) is a disjoint union
> of legal simple cycles.  In particular, it gives a legal sequence of
> simple-cycle switches.  If \(C\) is connected, one switch suffices.

Here is the complete proof.  The binary support \(F\) is an even
subgraph because \(\mu\circ f\) is a binary flow.  It contains \(M\), so
\(J_0=F-M\) has boundary \(\partial M\).  Similarly,
\(M\cup J_1\) is even.  Therefore
\[
 C=F\mathbin\triangle(M\cup J_1)=J_0\mathbin\triangle J_1
\]
is even and avoids \(M\).  In a cubic graph every nonempty component of
an even subgraph is a simple cycle.  Switching \(a\) on all components
of \(C\) changes the affine support from \(F\) to
\[
                    F\mathbin\triangle C=M\cup J_1.
\]
The disjoint join \(J_2\) lies in its complement.  Equivalently, every
component of that complement contains an even number of
\(\partial M\)-terminals.  This is precisely the H--S condition for
\(\mu\).  Finally, switching by \(a\) does not change \(M_a\), so the
components of \(C\) may be switched sequentially without ever creating
a zero edge.  This proves the lemma.

The radius-one difficulty is now visible: packing supplies an even
switch, but (3) need not be connected.  Section 5 shows that no
unrelated repairing circuit need exist either.

## 3. Why the refuted lemma would have proved FiveCDC

Assume a FiveCDC counterexample exists.  The audited cubic expansion
and minimum-counterexample reductions in `docs/reductions.md` yield a
minimum cubic counterexample \(G\) which is simple and cyclically
4-edge-connected.  Jaeger's 8-flow theorem supplies a nowhere-zero
\(\mathbb F_2^3\)-flow \(f\) on \(G\).

Had the reduced lemma been true, apply it.  If \(f\) is H--S-good,
Theorem 3.16 gives a
FiveCDC.  Otherwise one legal switch produces an H--S-good flow, and
the same theorem again gives a FiveCDC.  Both conclusions contradict
the choice of \(G\).

Thus the reduced lemma would have been sufficient for FiveCDC.  The
strict-snark countermodel below means this implication can no longer be
used as a proof route.

## 4. Exact positive cyclic-4 controls

The standalone standard-library checker
`verify_husek_samal_one_switch_boundary.py` verifies the following two
repairs.  Edge ids are in the displayed graph6 edge order.

### Order 36

The simple cubic graph is cyclically 4-edge-connected.  Its starting
flow has defect profile
\[
                     (8,6,6,10,8,4,6).
\]
Switch value \(a=7\) on the 24-edge simple cycle

```text
0,1,2,3,6,7,9,10,11,14,15,16,19,20,21,32,33,38,40,41,47,50,51,53
```

gives profile
\[
                     (10,6,6,6,6,0,8).
\]
Hence functional \(\mu=6\) is clean after one switch.

### Order 60

The simple cubic graph is cyclically 4-edge-connected.  Its starting
flow has all seven fixed projections dirty:
\[
                     (8,8,4,6,6,8,6).
\]
Switch value \(a=7\) on the 25-edge simple cycle

```text
1,2,8,11,18,22,24,26,27,30,31,33,35,37,39,40,42,43,45,62,65,67,73,74,75
```

gives profile
\[
                     (10,6,6,8,8,6,0).
\]
Hence functional \(\mu=7\) is clean after one switch.

For each positive control the checker independently verifies the graph,
flow equations, legality and simplicity of the switch support, the two
profiles, and the absence of cyclic edge cuts of sizes one, two, or
three.

## 5. Exact strict-snark radius-one countermodel

The retained state
`husek-samal-one-switch-countermodel-order26.txt` has graph6 record

```text
Y?HI@e??GC?Ba??CO???ACG??BH?G?g?C??O??GI??@??C@?A?C??C@_
```

and flow values, in graph6 edge order,

```text
7,5,3,7,1,3,2,3,5,5,2,6,1,4,7,2,3,7,6,5,4,1,6,4,4,6,2,5,6,4,2,1,4,3,3,2,6,7,1
```

Nauty's `labelg -q` gives the canonical unlabeled graph6 record

```text
Ys??O???GC__?`B??K?GO?O??_GA_?O?@??`G?o?_?KC?B?C??OO@??_
```

and `planarg -v` classifies the graph as nonplanar.  The first graph6
record is retained because its standard edge order is the one used by
the flow and cover certificates.

The independent checker verifies that the graph is simple cubic,
cyclically 4-edge-connected, has girth five, and has no Tait
3-edge-colouring.  Its initial H--S defect profile is
\[
                         (8,8,4,6,6,6,4).
\]
It enumerates all 8,797 simple cycles and all 1,604 legal
cycle--value switches.  None is H--S-good.  The minimum defect after at
most one switch is two; one attaining profile is
\[
                         (6,6,2,4,8,4,4).
\]

An independently checked standard FiveCDC, encoded as weight-two
five-bit labels, is

```text
12,6,20,12,6,3,5,3,18,9,17,3,17,24,3,18,18,9,17,9,
17,24,10,18,10,18,24,24,24,10,10,18,10,24,10,18,10,18,24
```

Thus this is a counterexample only to radius-one domination.

The exact H--S distance of the displayed flow is two.  One shortest
path is:

```text
1: a=1  C=1,2,3,7,8,9,10,11,13,15,16,19,20,27,28,29
2: a=5  C=0,1,2,4,6,7,8,9,10,11,15,30,32,33
```

The two successive profiles are
\[
                  (2,8,4,6,6,6,10),\qquad
                  (2,4,4,6,4,0,6).
\]
The exhaustive radius-one failure proves the lower bound, and the
displayed legal path proves the upper bound.

This proves:

> **Strict-snark auxiliary counterexample.**  
> Direct H--S radius-one domination fails for finite simple cubic
> cyclically 4-edge-connected non-Tait graphs of girth five.

It closes the proposed one-switch route but does not alter the status
of FiveCDC.

## 6. Two larger negative controls

### Cyclic-4, girth-five, but Tait-colourable

A second 40-vertex state is simple cubic, cyclically
4-edge-connected, and has girth five.  Its initial profile is
\[
                         (6,8,10,4,10,6,6).
\]
The checker exhausts all 941,438 simple cycles and all 48,544 legal
switches, finding no repair.  The graph has an explicit Tait
3-edge-colouring and hence a three-cycle double cover.  This was the
first countermodel found in the flow-preserving rewiring search; the
order-26 strict countermodel supersedes it structurally.

### Connected, with cyclic 2-edge cuts

The connected 40-vertex composition certificate in
`search/connected-one-switch-countermodel-40v-20260726/` has initial
profile
\[
                    (12,6,6,10,12,6,6).
\]
The new checker enumerates all 6,780 simple cycles.  Across all seven
switch values, exactly 1,844 cycle--value pairs are legal.  None yields
a zero entry in the resulting defect profile.  The smallest defect
after at most one switch is two; one attained profile is
\[
                      (8,2,8,10,10,6,4).
\]

The same audit finds five cyclic 2-edge cuts.  (Three are the displayed
graft cuts; two further cuts separate aggregate shores.)  Thus this
graph lies outside the sound minimum-counterexample domain.  Its
existing certificate also includes an explicit standard FiveCDC, so it
is not a FiveCDC counterexample.

This proves:

> **Finite auxiliary counterexample.**  
> Connectedness, simplicity, cubicity, and bridgelessness do not suffice
> for direct H--S radius-one domination.

## 7. Correction separating two frontiers

The order-60 starting flow is maximally bad only for its seven *current
H--S projections*.  It is not an all-value-classes-nonpacking flow.
In particular, its value-7 matching \(M_7\) already has two disjoint
\(\partial M_7\)-joins in \(G-M_7\).  The two checked edge sets are

```text
J1 =
1,2,13,16,18,20,26,32,35,44,46,49,50,53,57,60,61,62,63,64,69,71,72,73,75,81,83

J2 =
3,6,7,10,12,14,17,19,22,24,27,29,34,37,40,41,43,45,47,48,55,56,74,80,82,85,86,87,88
```

The verifier checks \(J_1\cap J_2=\varnothing\), both avoid \(M_7\),
and both have boundary exactly the endpoints of \(M_7\).  These joins
are aligned with the displayed repair: if
\(F=\{e:\langle7,f(e)\rangle=1\}\), then the 25-edge repair cycle is
exactly
\[
                           (F-M_7)\mathbin\triangle J_1.
\]
After the switch the affine support is \(M_7\cup J_1\), and \(J_2\)
lies in its complement.  Thus the numerical repair is also a direct
instance of the packing-to-switch lemma.

Consequently the order-60 result must not be advertised as extending
the older packing-bad one-switch census.  The H--S repair changes how a
functional sees the complementary factor and exposes a packing which
was already intrinsic to \(M_7\).

## 8. Packability itself does not restore radius one

A further tempting bridge was:

> If an H--S-bad flow already has a packable value class, then some
> legal simple-cycle switch makes it H--S-good.

This is false.  The first connected simple cubic countermodel found has
order 12.  Its graph6 record and flow are

```text
K?`DAagK_iH_
3,1,1,7,6,2,2,4,6,3,5,6,7,3,4,7,5,2
```

Its value-5 class consists of edges \(10,16\).  The following two
edge-disjoint joins avoid that class and have the same four-vertex
boundary:

```text
J1 = 4,5,7,8,9,15
J2 = 0,2,11,12,13,17
```

The initial H--S profile is
\[
                         (4,6,4,4,2,4,4).
\]
Complete edge-subset enumeration finds exactly 76 simple cycles and 100
legal cycle--value switches.  None is H--S-good.  The packing-to-switch
construction for \(\mu=1\) instead gives two disjoint five-cycles; both
must be switched.  The profiles after the first and second components
are
\[
                (2,4,4,2,2,4,4),\qquad
                (0,4,2,2,2,4,2).
\]
An exhaustive full-span flow-orbit census found no such countermodel in
connected simple cubic graphs through order 10.  Full span is sound here:
if the image of the flow lies in a proper subspace of
\(\mathbb F_2^3\), a nonzero functional annihilates the image and makes
the H--S defect zero.  The order-12 minimality statement is restricted to
connected simple cubic graphs, not multigraphs.

The phenomenon also occurs inside the strict-snark domain.  The retained
state `husek-samal-packable-one-switch-countermodel-order26.txt` is simple
cubic, cyclically 4-edge-connected, non-Tait, nonplanar, and has girth
five.  Its initial profile is
\[
                         (6,6,4,6,2,4,4),
\]
and value 4 packs.  The independent standard-library checker enumerates
all 9,213 simple cycles and all 1,485 legal switches, finding no good
switch.  The exact H--S distance is two.  It also checks an explicit
standard FiveCDC, so this is only an auxiliary countermodel.

Thus the packing-to-switch lemma is inherently a finite-sequence
statement: its even support can have more than one circuit component,
and no unrelated repairing single circuit need exist.

## 9. Reproduction

From the project root:

```bash
python3 scratch/verify_fano_order60_flow_repair.py
python3 scratch/verify_husek_samal_one_switch_boundary.py
python3 scratch/verify_husek_samal_packable_one_switch_countermodel.py
```

All three programs use only the Python standard library.  The second reads
the frozen order-40 construction certificate and independently checks
the order-26 and second order-40 states.  It uses its own graph, flow,
component-parity, simple-cycle, switch, Tait-colouring, FiveCDC, girth,
and cyclic-cut routines.  The third checks the stricter packable order-26
state.  A separate C++ implementation gives the same order-26 totals.

## 10. Remaining resolution obligation

Radius one is no longer a viable universal route.  The live exact
targets are:

1. prove that every reduced flow reaches an H--S-good flow after a
   finite sequence of legal simple-cycle switches;
2. prove a bounded-radius version, starting with radius two, or find a
   strict-snark countermodel at that radius; or
3. bypass reconfiguration and prove the existential Hušek--Šámal flow
   selection statement directly.

The packing-to-switch lemma resolves every flow having a packable value
class by an explicit finite switch sequence.  The remaining hard case
is therefore a flow for which all seven value-class matchings are
nonpacking, together with the problem of reaching a packable state.
Any finite-radius countermodel only refutes that radius unless the graph
is independently proved to have no H--S-good flow at all (equivalently,
no FiveCDC).

The first radius-two reconnaissance found no countermodel:

- all 280 retained strict order-26 snarks, 100 random nowhere-zero flows
  per graph: 28,000 flows, 26,443 H--S-bad, 25,230 radius-one traps, all
  repaired by radius two;
- seven retained strong order-34 snarks, 100 random flows per graph:
  700 flows, 695 H--S-bad, 689 radius-one traps, all repaired by radius
  two.

The search tested 4,432,803 second-neighbour candidates in the order-26
run and 1,594,834 in the order-34 run.  These are deterministic seeded
samples on retained graph lists, not flow censuses and not evidence of
list completeness.
