# Four-coordinate complement circuits and the exact external-reentry delimiter

Date: **2026-08-01**

Status: **HUMAN-CHECKABLE SWITCHING THEOREM / COMPLETE FINITE FRONTIER
THROUGH ORDER 14 / SHARP COUNTERMODELS TO ONE-STEP RESCUE / NOT A
FIVECDC RESOLUTION**.

## 1. The complement-circuit switch

Let a loopless cubic graph carry a `D5` flow

\[
 q:E(G)\longrightarrow \binom{[5]}2,
 \qquad \mathop\triangle_{e\ni v}q(e)=\varnothing.
\]

Fix a coordinate `h`, put `S=[5]-{h}`, and let `C` be a circuit every one
of whose labels avoids `h`.  Define

\[
 q^C(e)=\begin{cases}q(e)\mathbin\triangle S,&e\in C,\\
 q(e),&e\notin C.\end{cases}                                      \tag{1}
\]

> **Theorem 1 (four-coordinate complement switch).**  Formula (1) is a
> `D5` flow.  For every coordinate pair `P`,
> \[
> Y_P(q^C)=\begin{cases}
> Y_P(q)\mathbin\triangle C,&h\in P,\\
> Y_P(q),&h\notin P.
> \end{cases}                                                     \tag{2}
> \]

**Proof.**  A label `A` on `C` is a two-subset of the four-set `S`, so
`A triangle S=S-A` is again a two-subset.  At a vertex of `C`, exactly two
incident labels receive the same xor shift `S`; the two shifts cancel.
All other vertex equations are unchanged.  This proves that (1) is a
`D5` flow.

For an edge of `C`, factor activity changes by

\[
 |S\cap P|\pmod2.
\]

Since `P` has size two and `S` omits exactly `h`, this parity is one
exactly when `h` belongs to `P`.  This proves (2). \(\square\)

The support may more generally be any Eulerian edge set
`X` contained in

\[
 B_h(q):=\{e:h\notin q(e)\}.                                     \tag{3}
\]

Every component of `X` is a circuit, so the preceding proof applies
componentwise, with `X` in place of `C` in (1)--(2).

## 2. Completeness among constant circuit translations

Suppose one adds one fixed vector `t in F_2^5` to every label on a circuit.
If all old and new labels have weight two, `t` has even weight.  The only
possibilities are:

1. `t=0`;
2. `|t|=2`, and every circuit label crosses `t`; or
3. `|t|=4`, and every circuit label avoids the unique coordinate outside
   `t`.

This follows immediately from

\[
 |A\mathbin\triangle t|=2+|t|-2|A\cap t|=2.                    \tag{4}
\]

In case 2 the circuit is a component of `Y_t`: the active degree in a
cubic graph is zero or two, and the circuit already supplies both active
edges at each of its vertices.  The operation is therefore an ordinary
component Kempe switch.  Case 3 is Theorem 1.  Thus, apart from the identity,
ordinary weight-two Kempe switches and weight-four complement-circuit
switches are the complete constant-translation moves on one circuit.

The weight-four move can cross ordinary Kempe orbits.  It is not an
unnoticed rephrasing of a weight-two component switch.

## 3. Exact cycle-space and rescue characterization

Let `U` be the root edge together with the three cap edges.  Boundary-word
preserving complement supports are exactly

\[
             Z_1(B_h(q)-U),                                    \tag{5}
\]

the binary cycle space of `B_h(q)-U`.  In particular, a nonzero eligible
support exists exactly when

\[
 |E(B_h-U)|-|V(G)|+c(B_h-U)>0.                                 \tag{6}
\]

This is the usual cycle/cut orthogonality statement: the cycle space is the
orthogonal complement of the cut space.  It characterizes availability of
a support, not whether its three simultaneous circuit splices repair the
root interface.

Normalize the cap labels to

\[
 q(a)=01,\qquad q(b)=02,\qquad q(c)=12.                         \tag{7}
\]

For either unused coordinate `h in {3,4}`, put

\[
 F_0=Y_{0h},\qquad F_1=Y_{1h},\qquad F_2=Y_{2h}.                \tag{8}
\]

These are respectively the external factors for physical pairs `ab`,
`ac`, and `bc`.  If `X` in (5) is toggled, (2) gives

\[
                       F_i'=F_i\mathbin\triangle X
                       \quad(i=0,1,2).                         \tag{9}
\]

Consequently `X` is a simultaneous external rescue exactly when at least
two of the following three directly checkable statements hold:

- one component of `F_0 triangle X` contains `r,a,b`;
- one component of `F_1 triangle X` contains `r,a,c`;
- one component of `F_2 triangle X` contains `r,b,c`.

Equations (5) and (9), plus these three component tests, are the exact finite
obstruction format for boundary-preserving complement rescue.  Connectivity
is the genuinely non-linear datum left after cycle/cut orthogonality; cycle
rank alone does not decide it.

Marked girth does not fill this gap.  It lower-bounds the length of a
nonzero member of (5), but does not force (6), much less two of the three
component statements after (9).

There is an exact local count showing why the obvious averaging argument
stops.  At a cubic vertex the three labels form the three edges of a
coordinate triangle.  In `B_h` the local degree is one when that triangle
uses `h`, and three when it omits `h`.  If `t_h` is the number of local
triangles omitting `h`, then

\[
 |E(B_h)|=\frac n2+t_h,
 \qquad \sum_{h=0}^4t_h=2n.                                  \tag{10}
\]

Thus averaging guarantees only `max t_h >= 2n/5`.  A crude edge-count
guarantee of a circuit would need roughly `t_h >= n/2` even before the four
forbidden terminal edges are removed.  Girth supplies no missing density.
Any proof of (6), or of the stronger rescue criterion, must therefore use
more than local degree counts plus marked girth.

## 4. Complete finite frontier

The C++ audit enumerates every normalized `D5` flow, every ordinary Kempe
orbit, every rooted cap interface, and every legal simple complement circuit.

Through order 12 there are two ordinary-orbit simultaneous failures.  Both
are repaired immediately by a complement triangle disjoint from the root
and cap.

At order 14 the exact hierarchy is:

| quantity | count |
|---|---:|
| graphs | 480 |
| normalized flows | 537,418 |
| ordinary Kempe orbits | 33,102 |
| orbit interfaces | 8,341,704 |
| ordinary-orbit simultaneous failures | 72 |
| immediate one-simple-complement rescues | 60 |
| strict immediate failures | **12** |
| rescued with a support disjoint from root and cap | 52 |

The minimum rescue-circuit lengths among the 60 positive cases are 28
triangles, 28 four-circuits, and four five-circuits.

The 12 strict failures occur on two graph6 records:

```text
M??CB?X[E_P_H_B_?   4 strict interfaces
M?AACGohBAJ?AgE_?   8 strict interfaces
```

The first graph has girth four, edge-connectivity three, cyclic
edge-connectivity three, and is Tait-colourable.  The second has girth
three, cyclic edge-connectivity two, and is Tait-colourable.  Neither is in
the non-Tait marked-girth cap domain.

The focused Python audit goes further on all 12 strict interfaces:

1. every arbitrary Eulerian support in the full fixed-`h` cycle space still
   fails to give an **immediate** simultaneous flow;
2. two successive, independently chosen complement translations do give an
   immediate simultaneous flow; and
3. already one simple five-circuit, chosen disjoint from root and cap, moves
   to an ordinary Kempe orbit which contains a simultaneous flow.

Thus these are exact countermodels to immediate one-translation rescue, but
not closed obstructions under the enlarged move system.  At the quotient
whose vertices are ordinary Kempe orbits, their distance to a good orbit is
one complement move.

## 5. A literal human-checkable delimiter and escape

Use graph

```text
M?AACGohBAJ?AgE_?
```

with cap `z=0`, root edge `r=19`, and edge-order flow

```text
03 0c 05 06 06 14 06 03 05 06 05 03 0a 06 0c 06 14 12 12 0a 18
```

Its 432-state ordinary Kempe orbit has no simultaneous external flow.  Take
the five-circuit with edge indices

```text
1 12 13 18 20
```

and omit coordinate `h=0`.  All five labels avoid zero, and the support is
disjoint from the root and all three cap edges.  Complementing inside
`{1,2,3,4}` and globally normalizing gives

```text
03 05 0a 09 09 0c 09 03 0a 09 0a 03 0c 14 18 09 0c 05 18 11 09
```

The fixed external mask is still zero: this is not an immediate repair.
Four ordinary component switches, on the displayed pair/component data,
then give a simultaneous state:

```text
05 : 0 3 4 5 6 7 9 11 12 13
12 : 0 2 7 8 10 11
0c : 1 4 9 10 16 17
18 : 4 5 9 10 12 13
```

The final typed mask is 10 and its external physical mask is 3.  The
standalone checker reconstructs every intermediate flow, verifies every
factor component, exhausts the 432-state bad orbit, and checks the final
escape.

## 6. What remains open

The complement theorem supplies the first exact flow-changing mechanism in
this branch that can repair global reentry while leaving the root and cap
labels fixed.  It does **not** prove that a proper marked-girth non-Tait cap
has a rescuing support or a good enlarged orbit.

The exact surviving lemma is:

> In every proper rooted cap in the minimum-counterexample domain, some
> ordinary Kempe orbit either already has a simultaneous external flow or
> has a boundary-preserving complement-circuit edge to an orbit which does.

This statement is verified by the complete census only through order 14,
where its unrestricted version survives despite the 12 immediate
countermodels.  It is also consistent with the two frozen cyclically
four-connected non-Tait graphs of order 18 and six such graphs of order 20:
all their ordinary Kempe orbits are already simultaneous for every rooted
interface.  Those order-18/20 controls are finite corpus results, not a
universal theorem.

A false universal simultaneous-external theorem still has the exact six-case
SAT/CNF counterexample format in the companion
`d5-existential-external-order58-frontier-20260731` package.  Every one of
the six normalized connectivity formulas would have to be UNSAT with
independently checked proof certificates.  No such cap is known.

## Novelty and AI-use disclosure

Adding a fixed group element on a circuit is standard flow-switching
machinery.  No novelty is claimed for that general operation.  The exact
weight-four factor law, its use as a cross-Kempe-orbit external-reentry move,
and the stated finite delimiters appear to be new within this project, but
no comprehensive priority claim has been established.

OpenAI Codex agents, under human direction, found the cross-orbit move,
proved and classified it, implemented the exact censuses, found the 12 sharp
delimiters, and drafted this note.  The work has not undergone independent
human peer review and is not a resolution of FiveCDC.
