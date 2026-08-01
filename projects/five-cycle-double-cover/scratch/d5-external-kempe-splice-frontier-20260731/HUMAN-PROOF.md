# Kempe splicing at a typed cap

Date: **2026-07-31**

Status: **HUMAN-CHECKABLE LEMMAS AND LITERAL FINITE DELIMITERS / NOT A
UNIVERSAL EXTERNAL-COVERAGE THEOREM / NOT A PROOF OF FIVECDC**.

## 1. Definitions

Let a loopless cubic graph carry a `D5` flow

\[
 q:E(G)\longrightarrow \binom{[5]}2,
 \qquad \mathop{\triangle}_{e\ni v}q(e)=\varnothing.
\]

For a coordinate pair `P`, put

\[
              Y_P(q)=\{e:|q(e)\cap P|=1\}.
\]

It has degree zero or two at every vertex.  Let `D` be one circuit
component of `Y_T(q)`.  A component Kempe switch on `(T,D)` transposes the
two coordinates of `T` on every label of `D`; call the resulting flow
`q'`.  This is again a `D5` flow: at a vertex of `D`, exactly two incident
labels change, each by xor with `T`, so their two defects cancel; elsewhere
nothing changes.  Transposition preserves label weight two.

Three assertions must be kept separate throughout:

1. a **selected-port witness** is one flow and one external factor circuit
   containing the selected physical port and the root;
2. **aggregate external coverage** over a specified set of flows means that
   every physical port has a selected-port witness, possibly in a different
   flow; **orbit aggregate coverage** is the stronger special case in which
   that set is one Kempe orbit;
3. **simultaneous external coverage** means that the union of the external
   root circuits in one single flow covers all three physical ports.

The universal typed-signature target asks for aggregate coverage over all
`D5` flows.  It does not require the witnesses to lie in one orbit.
Simultaneous coverage is stronger still and is reported only when the
literal checker actually finds it.

## 2. The circuit-splice identity

> **Lemma 2.1 (factor splice).**  For every coordinate pair `P`,
>
> \[
> Y_P(q')=
> \begin{cases}
> Y_P(q)\mathbin\triangle D,&|P\cap T|=1,\\
> Y_P(q),&|P\cap T|\in\{0,2\}.
> \end{cases}
> \]

**Proof.**  Outside `D` no label changes.  On `D`, write `tau_T` for the
coordinate transposition.  An edge with old label `L` is active for `P`
after the switch exactly when

\[
 |\tau_T(L)\cap P|=1\pmod2,
\]

equivalently when `L` crosses `tau_T(P)`.  If `P` contains zero or two
coordinates of `T`, then `tau_T(P)=P`, so membership does not change.  If
`P` contains exactly one coordinate of `T`, then
\(\tau_T(P)=P\mathbin\triangle T\).  For every edge of `D`,

\[
 \bigl(|L\cap P|+|L\cap(P\mathbin\triangle T)|\bigr)\bmod2
       =|L\cap T|\bmod2=1.
\]

Thus membership is toggled on every edge of `D` and nowhere else.  This
is the displayed identity.  `square`

The lemma is stronger than a label-level description: it determines the
whole post-switch factor without solving any new equations.  The remaining
difficulty is component connectivity inside the symmetric difference.

## 2.5 Matching-deletion characterization

There is an elementary cover-theoretic way to expose the distinction
between the two modes.  For a pair `P`, define

\[
                         M_P=\{e:q(e)=P\}.
\]

The local coordinate-triangle rule makes `M_P` a matching: two incident
edges with label `P` would force the third incident label to be zero.
Put \(C_s=\{e:s\in q(e)\}\).  If `P={i,j}` and the other coordinates are
`k,l,m`, then on `G-M_P` the
four even subgraphs

\[
                         Y_P,\quad C_k,\quad C_l,\quad C_m              \tag{1}
\]

cover every remaining edge exactly twice.  Indeed, a remaining label
which crosses `P` belongs to `Y_P` and to exactly one of the last three
sets; a label disjoint from `P` belongs to exactly two of the last three.

This observation has an exact converse which does not invoke a solver.

> **Proposition 2.2 (external matching certificate).**  Fix physical ports
> `a,b` and let `c` be the inactive port.  An external typed state through
> `r,a,b` exists if and only if there are:
>
> - a matching `M` which does not contain `c`;
> - two Eulerian edge-subsets `E_i,E_j` of `G` with
>   \(E_i\cap E_j=M\);
> - their symmetric difference \(D=E_i\mathbin\triangle E_j\), having a
>   circuit component through `r,a,b`; and
> - three Eulerian edge-subsets `F_k,F_l,F_m` of `G-M` such that
>   \(D,F_k,F_l,F_m\) cover every edge of `G-M` exactly twice.

**Proof.**  From an external `D5` witness with factor `P={i,j}`, take
`E_i=C_i`, `E_j=C_j`, `M=M_P`, `D=Y_P`, and take the three remaining
coordinate subgraphs for the `F` sets.  Formula (1) checks the four-cover.
The inactive port has a label disjoint from `P`, so it is not in `M`.

Conversely, use the five Eulerian sets

\[
                         E_i,E_j,F_k,F_l,F_m.                        \tag{2}
\]

An edge in `M` lies in the first two sets and in none of the last three,
because those are subsets of `G-M`.  An edge of `D` outside `M` lies in
exactly one of `E_i,E_j`; the four-cover says it lies in exactly one of the
three `F` sets.  An edge outside \(M\cup D\) lies in neither of the first
two and in exactly two `F` sets.  Thus (2) covers every edge exactly twice
and gives a `D5` flow whose `ij` factor is `D`.  Since `c` is outside both
`D` and `M`, it lies in neither `E_i` nor `E_j`; its label is disjoint from
`ij`.  The specified component is therefore external.  `square`

For an arbitrary displayed typed state of factor `P`, this proof gives the
particularly sharp test

\[
 \text{internal mode}\iff c\in M_P,
 \qquad
 \text{external mode}\iff c\notin M_P.                         \tag{3}
\]

Consequently mode amplification can be viewed exactly as relocating the
four-cover deletion matching away from the inactive port while preserving a
root circuit in the associated symmetric difference.  This is a
reformulation of the gap, not a proof that such a relocation always exists.

The two Eulerian sets in Proposition 2.2 themselves have a useful
cycle-parity characterization.

> **Lemma 2.3 (matching lift).**  Let `M` be a matching and let `D` be a
> 2-regular subgraph of `G-M`.  There are Eulerian sets `E_i,E_j` with
> \(E_i\cap E_j=M\) and \(E_i\mathbin\triangle E_j=D\) if and only if:
>
> 1. every endpoint of `M` lies on `D`; and
> 2. every circuit component of `D` contains an even number of endpoints
>    of `M`.

**Proof.**  Put every edge of `M` into both sets.  At an endpoint of `M`,
each set already has local degree one, so the two incident `D` edges must
be split, one into each set.  At an unmarked vertex of `D`, its two edges
must instead be put into the same set.  Thus, while traversing a circuit of
`D`, the owner of the current edge changes exactly at the marked vertices.
A consistent assignment exists exactly when their number is even.  This
also proves necessity: an endpoint of `M` outside `D` would have odd degree
one, and a circuit with an odd number of switches cannot close.  `square`

Combining Proposition 2.2 and Lemma 2.3 removes `E_i,E_j` from the search:
it is enough to find a matching `M` avoiding the inactive port and a
2-regular `D` satisfying the two parity conditions, containing the desired
root circuit, and occurring as one member of a four-cover of `G-M`.
For every factor of the retained literal flow, `checker.py` verifies both
matching-lift parity conditions in addition to the four-cover count.

## 3. An exact cap splice

Suppose an internal typed state is normalized at the cap vertex `z` as

\[
 q(a)=01,\qquad q(b)=02,\qquad q(c)=12=P,
\]

and the root circuit `K` is the component of `Y_P(q)` containing `r,a,b`.
Take `T=13`, and let `D` be the `Y_T(q)` component containing `a,c`.
Switch on `D`.  The three new cap labels are

\[
 q'(a)=03,\qquad q'(b)=02,\qquad q'(c)=23.
\]

By Lemma 2.1,

\[
                       Y_{12}(q')=Y_{12}(q)\mathbin\triangle D.
\]

At `z` this new factor uses `b,c` and leaves `a=03` inactive and disjoint
from `12`.  Therefore:

> **Corollary 3.1 (conditional externalization).**  If the component of
> \(Y_P(q)\mathbin\triangle D\) containing `r` reaches `z`, then switching `D`
> gives an external state through physical ports `b,c`, and in particular
> externally covers the formerly inactive port `c`.

The same statement holds with `13` replaced by `14`, and after exchanging
`a,b` with `23` or `24`.  Consequently, a bad internal state which cannot
externally cover `c` after one switch must survive four explicit circuit
splices.  This is the exact global-reentry obstruction; merely counting
foreign labels on the two root-to-cap arcs does not decide it.

## 4. A stabilizer-orbit sufficient condition

Keep the same internal state.  Each edge of `K` has a unique label

\[
                     u(e)v(e),\qquad
 u(e)\in\{1,2\},\quad v(e)\in\{0,3,4\}.
\]

Switching any component of `Y_34` preserves `K`, all three cap labels, and
the positions with `v=0`; it swaps `v=3` and `v=4` on the intersection of
that component with `K`.  The `Y_34` components themselves are unchanged,
so these switches commute.

> **Lemma 4.1 (unentangled arc criterion).**  Let `R` be either root-to-cap
> arc of `K`.  If, for every component `D` of `Y_34`, all edges of
> `D` which lie on `R` have the same outside coordinate (`3` or `4`), then a
> set of commuting `Y_34` component switches produces an external state
> on the original physical pair `ab`.

**Proof.**  Independently switch each `Y_34` component whose nonempty
intersection with `R` has outside coordinate `4`, and leave the components
whose intersection has coordinate `3` unchanged.  The hypothesis makes
this choice consistent even when a component meets `R` more than once.
After the switches every edge of `R` has outside coordinate `0` or `3`.
Hence every edge of `R` is active for `Y_03`.  The arc joins the root to
`z`, where `Y_03` uses `a,b` and leaves `c=12` disjoint from `03`.
Therefore the root component supplies an external `ab` state.  `square`

Its contrapositive strengthens the earlier foreign-blocker condition:
if the whole `Y_34` stabilizer orbit contains no external `ab` state, then
on each root-to-cap arc some one `Y_34` component reappears with both
outside colours.  Call this an **entangled blocker**.  It is a necessary
obstruction for this restricted orbit, not a contradiction with girth or
connectivity.

## 5. The retained Petersen--Foster flow escapes in one switch

The sibling package `../d5-external-port-coverage-frontier-20260731`
contains a literal 1,335-edge flow on the 890-vertex Petersen--Foster graph.
At `z=0`, with root `r=552`, it has fixed typed mask `6`: physical pair
`01` is external, pair `02` is internal, and port slot `2` has no external
state.

The checker in this package enumerates all ten factors and every component
switch from those literal bytes.  There are 124 distinct component
choices.  Exactly six of the 124 component-switch choices supply a
selected-port witness for slot `2`:

| switch pair | component | size | contains root | cap slots in switch | new factor | new cap slots | new component size |
|---:|---:|---:|:---:|:---:|---:|:---:|---:|
| `13` (`10`) | 0 | 46 | no | `01` | `12` (`6`) | `12` | 517 |
| `13` (`10`) | 1 | 463 | yes | none | `23` (`12`) | `12` | 455 |
| `24` (`20`) | 0 | 275 | no | `01` | `04` (`17`) | `12` | 549 |
| `24` (`20`) | 1 | 265 | no | none | `04` (`17`) | `02` | 601 |
| `24` (`20`) | 5 | 46 | yes | none | `02` (`5`) | `12` | 444 |
| `34` (`24`) | 6 | 48 | yes | none | `23` (`12`) | `12` | 408 |

Four of these six switched flows simultaneously cover all three ports;
the first two cover ports `1,2` but lose the starting flow's external state
on `0,1`.  In either case the one-switch orbit has aggregate external
coverage.  The first row is exactly Corollary 3.1 after a coordinate
renaming.  This
proves that the displayed fixed-flow obstruction is not stable under even
one unrestricted component switch.  It does not prove that every bad flow
has such a switch.

For the two internal root-to-cap arcs, the checker also finds respectively
six and seven entangled `Y_34` components.  Thus Lemma 4.1 deliberately
does not apply to the starting flow; a genuinely global splice is what
repairs it.

## 6. Two exact eight-vertex delimiters

### 6.1 External coverage can require two switches

The graph6 word

```text
G?zTb_
```

has edge order and flow labels displayed by `checker.py`.  Take `z=0`,
root edge `10`, and selected cap slot `1`.  Direct enumeration of every
component switch proves that neither the starting flow nor any one-switch
neighbour has an external witness for this slot.  The following two
switches do:

```text
Y_03 on edges (0,1,3,4),
Y_01 on edges (0,2,6,7).
```

The resulting flow has an external `Y_12` circuit through root `10` and
cap slots `(1,2)`.

### 6.2 An internal mode need not flip in one switch

For graph6 word

```text
GCZJd_
```

use the displayed flow, `z=0`, root edge `4`, and physical pair of cap
slots `(0,2)`.  It initially has an internal state on this pair.  No
zero- or one-switch neighbour has an external state on the same pair.
The two switches

```text
Y_02 on edges (0,9,11),
Y_04 on edges (1,4,5)
```

produce an external `Y_24` circuit on slots `(0,2)`.

Both are delimiters for bounded-switch proof claims, not counterexamples to
existential external coverage.

## 7. Exact remaining gap

The factor-splice identity turns every proposed component switch into an
ordinary symmetric-difference calculation.  It supplies a rigorous
conditional externalization rule and shows constructively that the long
Petersen--Foster blockers are escapable.  What remains unproved is that,
from every relevant cap and root, the four splices in Corollary 3.1 (or a
longer sequence) must eventually connect the root component to the cap.
The eight-vertex examples show that no proof may stop after one switch.

## AI-use disclosure

OpenAI Codex agents, under human direction, derived the factor-splice and
unentangled-arc lemmas, found the six Petersen--Foster repairs, and found
the two finite delimiters.  All literal statements are replayed by a
standard-library checker.  No novelty, universal theorem, or FiveCDC
resolution is claimed; independent human review is required.
