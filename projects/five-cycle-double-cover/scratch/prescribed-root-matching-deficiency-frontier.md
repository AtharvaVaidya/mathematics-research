# Prescribed roots: matching deficiency two and the theta-core frontier

Date: **2026-07-27**.

Status: **UNIVERSAL DEFICIENCY LEMMA / CYCLIC-FOUR BARRIER RIGIDITY /
SHARP 3-EDGE-CONNECTED LIMITATION / FOCUSED THETA CHOICE OPEN**.

Let \(G\) be a finite loopless cubic graph, let
\[
                         R=\{e,f\}
\]
be two independent edges, let \(U=V(e)\cup V(f)\), and put
\[
                         H=G-U.
\]
This memo audits the proposal that \(H\) always has matching deficiency at
most two when \(G\) is \(3\)-edge-connected.  The proposal is correct.

It then isolates the extra condition needed for fixed-five \(AA\).
If \(H\) has no perfect matching, choose a maximum matching \(P\) missing
two vertices.  The complement of \(R\cup P\), after degree-two
suppression, has one of exactly two cores:

1. three parallel edges between the two unsaturated vertices; or
2. one link between them and one loop at each.

Only the first, theta, core gives a nowhere-zero
\(\mathbb F_2^2\)-flow.  A smallest simple \(3\)-edge-connected
countermodel shows that one cannot force the theta choice from
\(3\)-edge-connectivity alone.  That countermodel is Tait-colourable and
has a cyclic \(3\)-edge-cut, so it does not refute the focused
cyclically-\(4\) non-Tait claim.

No Five-Cycle Double Cover conclusion is claimed.

## 1. The universal matching-deficiency lemma

For a graph \(J\), write
\[
 \operatorname{def}(J)=|V(J)|-2\nu(J),
\]
where \(\nu(J)\) is its maximum matching size.  Thus the deficiency is the
number of vertices missed by a maximum matching.

> **Theorem 1.1 (prescribed-root deficiency bound).**  Let \(G\) be a
> finite \(3\)-edge-connected loopless cubic graph, and let \(R\) be an
> independent edge pair with endpoint set \(U\).  Then
> \[
>                         \operatorname{def}(G-U)\le2.
> \]
> Since \(|V(G-U)|\) is even, the deficiency is either zero or two.

### Proof

Put \(H=G-U\).  Fix any \(S\subseteq V(H)\), and let
\[
 C_1,\ldots,C_t
\]
be the odd components of \(H-S\).  Each \(C_i\) is a nonempty proper
vertex set of \(G\).  Three-edge-connectivity gives
\[
                         |\delta_G(C_i)|\ge3.           \tag{1.1}
\]

There are no \(G\)-edges between distinct components of \(H-S\): such an
edge would have both ends in \(H-S\) and would join the components.
Consequently every edge in a boundary \(\delta_G(C_i)\) ends either in
\(S\) or in \(U\).  Edges ending in \(S\) contribute at most the total
cubic degree \(3|S|\).  Hence
\[
 \sum_{i=1}^t|\delta_G(C_i)|
       \le 3|S|+|\delta_G(U)|.                          \tag{1.2}
\]

The four vertices of \(U\) have total degree 12.  An edge internal to
\(U\) consumes two of those incidences, so
\[
 |\delta_G(U)|=12-2|E(G[U])|.                           \tag{1.3}
\]
The two root edges belong to \(E(G[U])\).  Therefore
\[
                         |\delta_G(U)|\le8.             \tag{1.4}
\]

Combining (1.1)--(1.4) gives
\[
                         3t\le3|S|+8,
\]
and integrality yields
\[
                    o(H-S)-|S|=t-|S|\le2.              \tag{1.5}
\]
The Tutte--Berge formula says
\[
 \operatorname{def}(H)
   =\max_{S\subseteq V(H)}\bigl(o(H-S)-|S|\bigr).
\]
Thus \(\operatorname{def}(H)\le2\).

A cubic graph has even order, so \(H\), obtained by deleting four
vertices, also has even order.  Its matching deficiency is therefore
even.  The only possibilities are zero and two. \(\square\)

> **Corollary 1.2.**  The root pair \(R\) extends either to a perfect
> matching of \(G\), or to a matching of \(G\) missing exactly two
> vertices.

### Proof

If \(H\) has a perfect matching \(P\), then \(R\cup P\) is perfect in
\(G\).  If \(\operatorname{def}(H)=2\), a maximum \(P\) misses two
vertices of \(H\), and \(R\cup P\) misses exactly the same two vertices in
\(G\). \(\square\)

The constant two is sharp; Section 4 gives a ten-vertex instance with
deficiency exactly two.

## 2. The exact two-core dichotomy

Assume now that \(\operatorname{def}(H)=2\).  Let \(P\) be a maximum
matching of \(H\), missing vertices \(a,b\), and put
\[
                         M=R\cup P,\qquad F=G-M.
\]
Every vertex covered by \(M\) has degree two in \(F\), while \(a,b\) have
degree three.

> **Lemma 2.1 (theta or loop--link--loop).**  Every component of \(F\)
> avoiding \(a,b\) is a circuit.  The vertices \(a,b\) lie in the same
> component.  Suppressing all degree-two paths in that component gives
> exactly one of:
>
> 1. three parallel \(ab\)-edges; or
> 2. one \(ab\)-edge, one loop at \(a\), and one loop at \(b\).

### Proof

A component avoiding \(a,b\) is finite and \(2\)-regular, hence a circuit.
Every graph component has an even number of odd-degree vertices, so the
two degree-three vertices \(a,b\) lie in the same component.

After suppression, let \(x\) be the number of \(ab\)-edges, and let
\(\ell_a,\ell_b\) be the numbers of loops at \(a,b\).  Degree three gives
\[
 x+2\ell_a=3,\qquad x+2\ell_b=3.
\]
The core is connected, so \(x\ge1\).  Therefore either
\[
 (x,\ell_a,\ell_b)=(3,0,0)
\]
or
\[
 (x,\ell_a,\ell_b)=(1,1,1).
\]
\(\square\)

> **Lemma 2.2 (flow test).**  The matching \(M=R\cup P\) is the exact
> zero set of an \(\mathbb F_2^2\)-flow if and only if its two-vertex core
> is the theta core.

### Proof

Extend a flow on \(F\) by zero on \(M\).  Every circuit component of \(F\)
accepts an arbitrary constant nonzero value.

For a theta core, give its three \(ab\)-paths the three distinct nonzero
values \(1,2,3\), constant along each suppressed path.  Their xor is zero
at both \(a\) and \(b\), so this is nowhere-zero.

For a loop--link--loop core, the two incidences of the loop path at \(a\)
have the same value and cancel in the xor equation.  The link value is
therefore forced to zero.  The same conclusion holds at \(b\).  Thus no
nowhere-zero flow exists. \(\square\)

The focused rooted-flow question in the deficiency-two branch is now
exact:

> Can one choose a maximum matching \(P\) of \(G-U\) whose core is theta?

The word “choose” matters.  One graph may have both theta and dumbbell
maximum matchings.

## 3. What cyclic four-connectivity forces in a tight barrier

The Tutte--Berge proof can be sharpened substantially in the focused
domain, although the sharpening does not yet force a theta choice.

> **Theorem 3.1 (tight-barrier rigidity).**  Let \(G\) be finite,
> connected, simple, cubic, and cyclically \(4\)-edge-connected.  Let
> \(R,U,H\) be as above, and suppose
> \(\operatorname{def}(H)=2\).  Choose \(S\subseteq V(H)\) satisfying
> \[
>                         o(H-S)=|S|+2.                 \tag{3.1}
> \]
> Put \(b=|\delta_G(U)|\).  Then:
>
> 1. \(b\in\{6,8\}\);
> 2. if \(b=6\), every odd component of \(H-S\) is a singleton with
>    \(G\)-boundary three;
> 3. if \(b=8\), all odd components are such singletons, with at most one
>    exception; the exceptional component, if present, has boundary five.

### Proof

Let the odd components be \(C_1,\ldots,C_t\), where
\(t=|S|+2\), and put
\[
                         q_i=|\delta_G(C_i)|.
\]
Because \(C_i\) has odd order and \(G\) is cubic,
\[
 q_i\equiv 3|C_i|\equiv1\pmod2.                        \tag{3.2}
\]
Three-edge-connectivity gives \(q_i\ge3\).  The boundary estimate from
Theorem 1.1 gives
\[
 \sum_iq_i\le3|S|+b.
\]
Since \(t=|S|+2\),
\[
 \sum_i(q_i-3)\le b-6.                                 \tag{3.3}
\]
The left side is a sum of nonnegative even integers.  Formula
\[
 b=12-2|E(G[U])|
\]
shows that \(b\) is even and at most eight.  Equation (3.3) forces
\(b\ge6\), proving \(b\in\{6,8\}\).

If \(b=6\), every \(q_i=3\).  If \(b=8\), at most one \(q_i\) can exceed
three, and that one can only equal five.

It remains to show that a \(3\)-boundary component \(C_i\) is a singleton.
If \(C_i\) were acyclic, connectedness would make it a tree, and cubic
degree counting would give
\[
 |\delta_G(C_i)|=3|C_i|-2(|C_i|-1)=|C_i|+2.
\]
Boundary three would force \(|C_i|=1\).

If \(C_i\) contained a cycle, its complement would contain one as well.
Indeed, the complement contains all four vertices of \(U\).  More
formally, a forest with \(r\) components and \(y\ge4\) vertices has
boundary
\[
 3y-2(y-r)=y+2r>3.
\]
Thus \(\delta_G(C_i)\) would be a cyclic \(3\)-edge-cut, contrary to
cyclic four-connectivity.  Hence \(C_i\) is a singleton. \(\square\)

When \(b=6\), the induced graph \(G[U]\) has the two roots plus one
additional edge.  When \(b=8\), the roots are the only edges of
\(G[U]\).  The theorem reduces the unresolved theta problem to an
extremely rigid barrier: all odd pieces are isolated vertices except
possibly one five-boundary piece.

There is also a direct exchange supply along a bad core.

> **Lemma 3.2 (a matching chord across every dumbbell bridge).**  Retain
> the hypotheses of Theorem 3.1.  Let \(P\) be a maximum matching of
> \(H\) whose complement \(F=G-(R\cup P)\) has a loop--link--loop core.
> For every original edge \(g\) on the suppressed link, the two cyclic
> shores of \(F-g\) are joined by at least three edges of \(R\cup P\).
> In particular, at least one edge of \(P\) crosses that shore.

### Proof

Delete \(g\) from the component of \(F\) containing the two branch
vertices.  The component on either side contains one of the two loop
circuits.  Let \(X\) be the vertex set on one side.  The only
\(F\)-edge in \(\delta_G(X)\) is \(g\); all other cut edges lie in
\(R\cup P\).  Both shores contain a circuit, so cyclic
four-connectivity gives
\[
                         |\delta_G(X)|\ge4.
\]
Thus at least three matching edges cross.  Only two of them can be the
two roots, so at least one belongs to \(P\). \(\square\)

Lemma 3.2 supplies an exchange chord across every bridge of a bad core.
What remains unproved is that these chords can be combined into a
root-preserving alternating exchange which destroys both loops without
reducing the matching size.

Non-Taitness is not used in Theorems 1.1 or 3.1.  It remains additional
focused data which a future exchange argument may need.

## 4. A sharp ten-vertex limitation

The theta conclusion is false if one assumes only simple cubic
\(3\)-edge-connectivity.

Consider graph6

```text
I?BeeOwM?
```

with indexed edges

| \(i\) | edge | \(i\) | edge | \(i\) | edge |
|---:|:---:|---:|:---:|---:|:---:|
| 0 | 0--5 | 5 | 3--6 | 10 | 3--8 |
| 1 | 1--5 | 6 | 0--7 | 11 | 4--8 |
| 2 | 2--5 | 7 | 1--7 | 12 | 2--9 |
| 3 | 0--6 | 8 | 4--7 | 13 | 3--9 |
| 4 | 1--6 | 9 | 2--8 | 14 | 4--9 |

It consists of two \(K_{2,3}\) shores
\[
 X=\{0,1,5,6,7\},\qquad
 \bar X=\{2,3,4,8,9\},
\]
joined by the three cut edges
\[
                         \delta(X)=\{2,5,8\}.           \tag{4.1}
\]
Direct cut enumeration gives edge connectivity three.

Take roots
\[
                         R=\{2,5\}.
\]
They are independent, with
\[
 U=\{2,3,5,6\}.
\]
The graph \(H=G-U\) has vertices
\[
 \{0,1,4,7,8,9\}
\]
and edges
\[
 6=(0,7),\quad7=(1,7),\quad8=(4,7),\quad
 11=(4,8),\quad14=(4,9).
\]

Its maximum matching size is two.  A size-two matching cannot use edge
8: after choosing \(8=(4,7)\), all remaining \(H\)-edges meet vertex 4 or
7.  Therefore the complete maximum-matching list is
\[
 \{6,11\},\quad\{6,14\},\quad\{7,11\},\quad\{7,14\}.   \tag{4.2}
\]
Thus \(\operatorname{def}(H)=6-2\cdot2=2\).

For every matching in (4.2), the zero matching \(R\cup P\) contains cut
edges 2 and 5 but not cut edge 8.  Its complement therefore has exactly
one strand across (4.1).  The two unmatched vertices lie on opposite
shores.  Lemma 2.1 forces the remaining two incidences at each branch
vertex to form a loop.  Every maximum matching has the
loop--link--loop core; none has a theta core.

The graph is Tait-colourable.  One explicit partition into its three
colour classes is

```text
{0,5,7,9,14}
{1,3,8,10,12}
{2,4,6,11,13}
```

Also, (4.1) is a cyclic \(3\)-edge-cut.  Hence:

> **Proposition 4.1.**  Three-edge-connectivity alone does not make the
> deficiency-two matching selectable with a theta core.

The countermodel is outside the focused domain for two independent
reasons: it is Tait-colourable, and it is not cyclically
\(4\)-edge-connected.

Among finite **simple** \(3\)-edge-connected cubic graphs, order ten is
smallest for this failure.  The complete canonical connected cubic lists
at orders four, six, and eight contain respectively \(1,2,5\) graphs;
after the edge-connectivity filter, all \(3\)-edge-connected rows and all
207 independent root pairs satisfy the perfect-or-theta alternative.  The
small checker below contains those eight graph6 rows and checks every
pair.  This finite minimality statement is separate from the universal
proof of Theorem 1.1.

## 5. Exact focused status

The following implications are now proved:

```text
3-edge-connected cubic
    => prescribed H has deficiency 0 or 2

deficiency 0
    => the roots extend to a perfect matching
    => an exact-zero rooted flow exists

deficiency 2 + a theta maximum
    => a near-perfect exact-zero rooted flow exists
```

The implication

```text
cyclically-4 non-Tait + deficiency 2
    => some maximum matching has theta core
```

remains open.  Proposition 4.1 cannot be promoted into a focused
counterexample.  Theorem 3.1 shows exactly what a focused obstruction
would have to survive: a tight barrier with singleton odd components
except possibly one five-boundary component.

Even a positive theta theorem would establish only rooted exact-zero
**feasibility**.  Proposition 4.3 of
`scratch/fixed-five-d5-four-pole-full-signature-frontier.md` still requires
the complement to pack two edge-disjoint boundary \(T\)-joins.  These
obligations must not be conflated.

## 6. Independent replay

The checker uses only the Python standard library:

```sh
python3 scratch/prescribed-root-matching-deficiency-checker.py \
  > /tmp/prescribed-root-matching-deficiency.json
```

It verifies:

- the literal graph6 and edge table;
- simplicity, cubicity, and edge connectivity three;
- the displayed cyclic \(3\)-cut;
- the explicit Tait colouring;
- the four and only four maximum matchings of \(H\);
- the loop--link--loop core for every maximum matching; and
- absence of a smaller simple \(3\)-edge-connected obstruction in the
  retained complete order-\(4,6,8\) graph6 lists.

Source SHA-256:

```text
ad7164408dbb712fa3f3b776243f2824a6c6beb7b65d42eb2e9aa31e3cb10673
```

The lower-order graph lists are the direct canonical output of:

```sh
geng -cq -d3 -D3 4
geng -cq -d3 -D3 6
geng -cq -d3 -D3 8
```

No larger census is used as a theorem in this memo.

## AI-use disclosure

The deficiency proof, tight-barrier refinement, countermodel search,
checker, and exposition were developed with substantial assistance from
OpenAI Codex under human direction.  The universal arguments are written
out in full.  The finite countermodel and lower-order minimality check are
independently replayable without trusting an AI system.
