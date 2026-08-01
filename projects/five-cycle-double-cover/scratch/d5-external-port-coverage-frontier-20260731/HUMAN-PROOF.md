# Local obstructions to external port coverage

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE LOCAL LEMMAS / POSITIVE SAT PROBES / NOT A
UNIVERSAL EXTERNAL-COVERAGE THEOREM / NOT A PROOF OF FIVECDC**.

## 1. Definitions

Let a loopless cubic graph carry a `D5` flow

\[
 q:E(A)\longrightarrow \binom{[5]}2,
 \qquad \mathop{\triangle}_{e\ni v}q(e)=\varnothing
 \quad(v\in V(A)).
\]

For a coordinate pair `P`, put

\[
 Y_P(q)=\{e:|q(e)\cap P|=1\}.
\]

Every vertex has degree zero or two in `Y_P`, so every nonempty component
is a circuit.  Let `z` be a cap vertex with physical ports `a,b,c`, and let
`r` be a proper root edge.  A state using ports `a,b` is realized when one
component of `Y_P` contains `r,a,b`; the third port `c` is then inactive.
The state is **external** when
\(P\cap q(c)=\varnothing\).

The local statements below use only the displayed equations.  The final
paragraph records separately how they enter the minimum-counterexample cap
setting.

## 2. An adjacent port is automatically externally covered

> **Lemma 2.1 (adjacent-port lemma).**  Suppose a proper root edge `r` and
> a port edge `a` have a common endpoint.  Then every `D5` flow on `A`
> supplies an external factor circuit containing `r` and `a`.  In
> particular, the physical port `a` is externally covered.

**Proof.**  Globally permute coordinates so the ordered connector triangle
at `z` is

\[
                         q(a)=01,\quad q(b)=02,\quad q(c)=12.       \tag{1}
\]

At the common endpoint of `r` and `a`, the three incident labels form a
coordinate triangle.  Hence `q(r)` is a weight-two label distinct from
`01` and meeting `01` in one coordinate.  It is therefore one of

\[
                         02,03,04,12,13,14.                        \tag{2}
\]

The four external factor pairs which use physical port `a` in (1) are

\[
                         03,04,13,14.                              \tag{3}
\]

Each pair in (3) crosses `01`.  For every label in (2), at least one pair
in (3) also crosses that label; explicitly one may choose

\[
\begin{array}{c|cccccc}
q(r)&02&03&04&12&13&14\\ \hline
Q&03&04&03&13&03&04.
\end{array}                                                       \tag{4}
\]

Thus `r` and `a` are consecutive active edges of `Y_Q`.  Their factor
component contains `z`.  At `z`, the factor uses `a` and exactly one other
port.  For `Q=03,04` the inactive connector is `12`; for `Q=13,14` it is
`02`.  In either case the inactive label is disjoint from `Q`, so the state
is external.  \(\square\)

This also explains why a SAT encoding for two independent root edges need
not handle the adjacent case: it is already settled by the six-entry local
table.

## 3. The two-arc foreign-blocker lemma

Consider an internal state on a factor circuit `K` using physical ports
`a,b`.  Normalize it as

\[
 q(a)=01,\qquad q(b)=02,\qquad q(c)=P=12.                         \tag{5}
\]

Every edge of `K` crosses `12`, and consequently has a unique expression

\[
 q(e)=u(e)v(e),\qquad
 u(e)\in\{1,2\},\quad v(e)\in\{0,3,4\}.                          \tag{6}
\]

Two consecutive labels on `K` are distinct and their xor is the third
incident weight-two label.  Therefore exactly one of `u` and `v` changes
at each step around `K`.  This is a closed-walk description on the six
states \(\{1,2\}\times\{0,3,4\}\).

Regard the root edge as the starting edge in either direction around `K`.
The two **root-to-cap arcs** are the two edge sequences which start with
`r` and first reach `z`, one through port `a` and the other through port
`b`.  They share only their starting edge `r`.

> **Lemma 3.1 (foreign blockers on both arcs).**  Put `v_r=v(r)` in (6).
> If the same physical pair `ab` has no external witness already in the
> displayed flow, then:
>
> - if `v_r=3`, each root-to-cap arc contains an edge with outside
>   coordinate `4`;
> - if `v_r=4`, each root-to-cap arc contains an edge with outside
>   coordinate `3`; and
> - if `v_r=0`, each root-to-cap arc contains both an edge with outside
>   coordinate `3` and an edge with outside coordinate `4`.

**Proof.**  An edge of `K` is active for `Y_03` exactly when its outside
coordinate in (6) is `0` or `3`.  Similarly it is active for `Y_04`
exactly when that coordinate is `0` or `4`.

Suppose first that `v_r=3`.  The root is active for `Y_03`.  If either
root-to-cap arc had no outside-`4` edge, every edge on that arc would be
active for `Y_03`.  It would be a factor path from `r` to `z`.  At `z`,
`Y_03` uses ports `a,b` and leaves `c=12` inactive and disjoint from `03`.
The factor component through the path would therefore be an external
`ab` witness, a contradiction.  Thus both arcs contain an outside-`4`
edge.  The case `v_r=4` is symmetric, using `Y_04`.

If `v_r=0`, the root is active for both `Y_03` and `Y_04`.  Applying the
same argument first to `Y_03` and then to `Y_04` forces, on each arc, an
outside-`4` blocker and an outside-`3` blocker, respectively.  \(\square\)

The lemma is only a necessary obstruction.  It does not say that the
blockers are distinct factor components, and it does not yet turn them
into a small edge cut or a short circuit.

## 4. Why a bare inverse-insertion tester does not yet prove coverage

There is a tempting minimality shortcut which needs an extra global
hypothesis.  Subdivide `r` and a selected port `a` by vertices `u,v`, join
them by a new edge `e`, and let `q` be a `D5` flow on the resulting parent.
Put `L=q(e)`.  At `u`, if the two old half-edge labels are `R_1,R_2`, then

\[
                         R_1\mathbin\triangle R_2=L,               \tag{7}
\]

and the analogous identity holds at `v`.  Both old halves cross `L`, but
the new edge with label `L` is inactive in `Y_L`.

The standard inverse switch-and-suppress operation works **if** `u,v` lie
on the same component of `Y_L`: transpose the two coordinates of `L` on
one `u`--`v` arc of that factor circuit, delete `e`, and suppress `u,v`.
At either subdivision vertex exactly one old half was transposed.  Equation
(7) says its new label equals the other half, so suppression is legal.  The
resulting `D5` flow on `A` has one `Y_L` circuit containing `r,a`.

An arbitrary parent flow need not satisfy that component condition.  Since
`e` is inactive in `Y_L`, its mere presence does not join the two
`Y_L` circuits through `u` and `v`.

The cube gives a literal eight-vertex example.  Colour its four vertical
edges `01`, and colour the edges of each horizontal 4-circuit alternately
`02,12`.  This is a `D5` flow.  Choose one vertical edge as `e`.  Its two
ends lie on the two different horizontal components of `Y_01`.  Deleting
`e` and suppressing its ends gives the triangular prism with one
distinguished edge on each triangle, but this particular parent flow has
no `Y_01` arc on which to perform the inverse operation.  Thus the claim
that the displayed inverse switch-and-suppress operation automatically
applies to *every* parent flow is already false on the cube.  This does not
exclude a different flow or a different argument producing a root-good
flow on the child.

The same issue survives a two-terminal equality-wire in place of `e`.
Summing xor conservation over all internal tester vertices makes its two
boundary labels equal, say to `L`.  Both boundary semiedges are inactive in
`Y_L`, so the tester itself supplies no `Y_L` path between `u,v`.  Such a
tester may restrict which global flows are allowed, but equality alone does
not prove the component condition required by the inverse operation.

Conditional on having that component condition, the proposed inequality
idea is sound: at `z`, the inactive port meets the active factor pair `L`
in zero or two coordinates.  Forcing its label to be unequal to `L` rules
out intersection two and therefore makes the state external.  What remains
missing is a bounded construction that forces both the needed `Y_L`
connectivity and the inequality.

## 5. A fixed-flow counterexample in the marked-girth geometry

The local blocker condition really can survive all of the graph geometry
available in this branch.  Here is a compact, independently replayable
example.

Let `F` be the Foster graph in LCF notation

```text
[17,-9,37,-37,9,-17]^15.
```

Delete vertex zero from ten copies of `F`.  Each resulting 89-vertex
3-pole has ports formerly adjacent to `0`, namely vertices `1,17,89` in
the zero-based LCF numbering.  Substitute these ten 3-poles for the vertices
of the Petersen graph, joining their ports in the displayed Petersen edge
order used by `check_pf_fixed_flow_counterexample.py`.  Sorting all edges
lexicographically gives a simple cubic graph `A` with 890 vertices and 1335
edges.  Its canonical reconstruction SHA-256 is

```text
3fe0630cb52d5a0b29a473faff02389195c7e119ea8f7a6f95f3ba9c38272282
```

The checker directly verifies connectedness after deleting any one or any
two edges, and verifies girth ten.  It also checks that the Petersen macro
is not 3-edge-colourable.  For completeness, this implies that `A` is
non-Tait: in any hypothetical 3-edge-colouring, the parity lemma applied to
an odd 89-vertex 3-pole says that its three boundary edges receive the three
different colours.  Contracting all ten 3-poles would therefore give a
3-edge-colouring of the Petersen graph, a contradiction.

Take cap vertex `z=0`, whose three incident edge indices are `0,1,2`, and
root edge `r=552=(363,400)`.  The checker verifies that `A-z` is connected,
bridgeless, and has girth ten, and that deleting `r` from `A-z` leaves it
connected with girth ten.  Thus this is the exact local marked-girth and
3-connectivity geometry, although it is not asserted to be an actual shore
of a minimum FiveCDC obstruction.

The file `pf-fixed-flow-labels.b85` is a base-85/zlib encoding of 1335 label
bytes.  Its decoded SHA-256 is

```text
6390ba1039116351e8e4343264f9881e4d1541dc028a661db848be9c695fdc9a
```

The checker verifies that every byte has weight two and that the xor of the
three incident labels is zero at every vertex.  Hence the bytes are a valid
`D5` flow, not merely SAT output.  In five-bit notation, the cap labels are
`18,6,20`, corresponding to `14,12,24`, and the root label is `18=14`.

There are exactly six coordinate pairs for which the root is active.  A
direct walk in each factor gives the complete table:

| factor pair | root-component edges | cap slots in component | state |
|---:|---:|:---:|:---:|
| `01` (`3`) | 449 | `0,1` | external |
| `04` (`17`) | 273 | none | none |
| `12` (`6`) | 523 | `0,2` | internal |
| `13` (`10`) | 463 | none | none |
| `24` (`20`) | 46 | none | none |
| `34` (`24`) | 48 | none | none |

Thus the fixed typed signature is bit mask `6`: the physical pair `01` is
external and physical pair `02` is internal.  Physical port slot `2` has no
external state anywhere in this displayed flow.

For the internal factor `P=12`, both root-to-cap arcs exhibit exactly the
blockers predicted by Lemma 3.1.  Their lengths include the root edge:

| arc | terminal port edge | length | outside `0` | outside `3` | outside `4` |
|---:|---:|---:|---:|---:|---:|
| 0 | 0 | 355 | 109 | 115 | 131 |
| 1 | 2 | 169 | 50 | 64 | 55 |

In particular, neither high girth nor 3-edge-connectivity makes the foreign
blockers disappear or forces them into an immediate small-cut contradiction.

This certificate refutes the strengthening

> every displayed `D5` flow in the marked-girth cap geometry externally
> covers all three physical ports,

and any proof step that attempts to derive externality solely from the
presence of the two blockers in that same flow.  It does **not** refute the
existential target that *some* `D5` flow covers every port: the sibling
full-signature certificate checks six flows on this same graph, including
the displayed one, whose aggregate exact signature is `63`.  A successful
proof may therefore need to change the flow or exploit genuinely additional
global structure.

## 6. Exact minimum-counterexample scope

In the existing edge-elimination branch, a relevant cap `A` is simple and
3-edge-connected.  Its core `K=A-z` is connected and bridgeless, has girth
at least nine, and `K-r` has girth at least ten.  The cap has order at least
56.  Because it is smaller than a hypothetical order-minimal FiveCDC
counterexample and is bridgeless, it has at least one `D5` flow.

Lemma 2.1 therefore settles every selected physical port adjacent to the
root.  A failure of existential external port coverage in this branch must
use a non-Tait cap (the Tait case was proved separately), a selected port
edge vertex-disjoint from the root, and, whenever that pair is represented
only internally, the two-arc blockers in Lemma 3.1.

Section 5 proves that no contradiction with the marked-girth or
3-connectivity hypotheses follows from those blockers alone in an arbitrary
fixed flow.  A signature could also fail to realize the selected physical
port at all, in which case Lemma 3.1 has no internal witness to start from.
Flow-changing arguments and this no-state case are the exact remaining gaps.

## AI-use disclosure

OpenAI Codex agents, under human direction, found the adjacent-port table,
the six-state circuit-word representation, the two-arc blocker condition,
the fixed-flow counterexample, and the SAT probes.  The proofs and a complete
semantic replay are supplied, but they have not undergone independent human
peer review.  No novelty or FiveCDC resolution claim is made.
