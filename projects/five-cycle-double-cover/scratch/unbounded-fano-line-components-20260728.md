# FiveCDC-positive graphs with unbounded Fano-line component number

Date: **2026-07-28**.

Status: **human-checkable infinite separation theorem; not a resolution
of FiveCDC**.

## Statement

Let \(f:E(G)\to\mathbb F_2^3-\{0\}\) be a nowhere-zero flow and let
\(L\) be a Fano line, that is, the three nonzero vectors in a
two-dimensional subspace.  Write
\[
 \kappa_L(f)=
 c\bigl(V(G),\{e:f(e)\in L\}\bigr).
\]

There is an infinite sequence of finite simple bridgeless cubic graphs
\(G_0,G_1,\ldots\) such that

1. every \(G_d\) has a standard five-cycle double cover;
2. for every nowhere-zero \(\mathbb F_2^3\)-flow \(f\) on \(G_d\) and
   every Fano line \(L\),
   \[
                         \kappa_L(f)\ge d+1;             \tag{1}
   \]
3. equality is attained for every \(d\); and
4. their orders satisfy
   \[
             |V(G_0)|=10,\qquad
             |V(G_{d+1})|=3|V(G_d)|+4,
   \]
   hence begin \(10,34,106,322,\ldots\).

Thus no universal constant bounds the number of components needed in a
Fano line, even among graphs already possessing FiveCDC.  In particular,
the valid theorem that a line with at most two components can be cleaned
does not furnish a universal proof of FiveCDC.

## Cotree-diamond expansion

Let \(H\) be a simple cubic graph and \(T\) a spanning tree.  For every
cotree edge \(uv\), delete \(uv\), add four private vertices \(a,b,c,d\),
and insert
\[
 ua,\ ac,\ ad,\ bc,\ bd,\ cd,\ bv.                    \tag{2}
\]
The four private vertices induce the diamond \(K_4-ab\).  Call the
result \(D_T(H)\).

The graph \(D_T(H)\) is again simple and cubic.  It is bridgeless when
\(H\) is bridgeless: every unchanged edge lies on the lift of an old
circuit, every boundary edge in (2) lies on the lift of a circuit
through \(uv\), and every internal diamond edge lies on a triangle or
on such a lifted circuit.

If \(H\) is not Tait-colourable, neither is \(D_T(H)\).  Indeed, xor
conservation over the four private vertices makes the two boundary
values of a diamond equal in every nowhere-zero
\(\mathbb F_2^2\)-flow.  Suppressing all diamonds would therefore give
a Tait colouring of \(H\).

## Component-growth lemma

> **Lemma.** Let \(H\) be non-Tait, let \(T\) be a spanning tree, and
> let \(H'=D_T(H)\).  Every nowhere-zero
> \(\mathbb F_2^3\)-flow \(f'\) on \(H'\), after suppressing the
> diamonds, gives a nowhere-zero flow \(f\) on \(H\).  For every Fano
> line \(L\),
> \[
>                         \kappa_L(f')\ge\kappa_L(f)+1. \tag{3}
> \]

**Proof.** Conservation over one diamond shows that its two boundary
values are equal; use this nonzero common value on the suppressed edge.
This gives \(f\).

Let \(h:\mathbb F_2^3\to\mathbb F_2\) have kernel
\(L\cup\{0\}\).  Then \(h\circ f\) is a binary flow, so its support is
an even edge-subset of \(H\).  It is nonempty: otherwise every value of
\(f\) would belong to \(L\), and the three incident nonzero line values
at each cubic vertex would be the three distinct elements of \(L\),
giving a Tait colouring of \(H\).

A nonempty even edge-subset cannot lie in the tree \(T\).  Hence some
cotree edge has suppressed value outside \(L\).  In its diamond both
boundary edges are outside \(L\), so the line-valued edges on the four
private vertices form at least one component isolated from the rest of
\(H'\).

For every line-valued suppressed edge, its replacement can preserve,
split, or add to the old line components, but cannot join two distinct
ones: any line-valued path between old vertices projects to a walk of
line-valued edges in \(H\).  A diamond whose suppressed value is outside
\(L\) contributes the isolated component just found.  Therefore the
number of line components increases by at least one, proving (3).
\(\square\)

## FiveCDC preservation

Represent a FiveCDC by a two-subset label on every edge.  Suppose the
deleted edge \(uv\) has label
\(\ell=\{i,j\}\).  Choose \(k\notin\ell\), put
\[
 r=\{i,k\},\qquad s=\{j,k\},
\]
and assign the seven edges in (2), in their displayed order, the labels
\[
                         \ell,r,s,s,r,\ell,\ell.       \tag{4}
\]
At every new vertex the three incident labels have empty symmetric
difference.  Every new label still has size two.  Thus (4) preserves
Eulerian parity and exact double coverage, independently in every
cotree diamond.

## Induction and sharpness

Take \(G_0\) to be the Petersen graph.  It is non-Tait: its six perfect
matchings all have two five-cycles as complementary 2-factor.  It has
the standard FiveCDC

```text
C1 = 0 1 2 5 8 14
C2 = 2 3 4 5 7 10
C3 = 0 4 6 9 12
C4 = 1 3 6 7 8 9 11 13
C5 = 10 11 12 13 14
```

in the edge order used by the checker.  Given \(G_d\), choose any
spanning tree \(T_d\) and put
\[
                         G_{d+1}=D_{T_d}(G_d).
\]
FiveCDC preservation and non-Tait preservation apply at every step.
Starting from the trivial bound \(\kappa_L(f)\ge1\), repeated use of
(3) proves (1).

For sharpness, start with the displayed Petersen flow

```text
5 1 3 1 2 7 4 2 2 3 3 1 2 6 4
```

and \(L=\{1,2,3\}\).  Its outside-line support is one circuit and its
line subgraph is connected.  At each step choose \(T_d\) to contain all
but one edge of that circuit; a circuit minus one edge is a forest and
extends to a spanning tree.

Lift a line-valued diamond entirely inside \(L\).  For an outside value
\(x\), choose two other outside values \(y,z\) and assign flow values
\[
               x,y,x+y,z,x+z,y+z,x                  \tag{5}
\]
in the edge order (2).  The outside support replaces the selected old
edge by a four-edge path, so it remains one circuit.  The three
line-valued internal edges of that diamond form one new isolated star.
All other line components lift without splitting.  Thus exactly one
component is added at every step and equality holds in (1).

## Reproduction and scope

Run:

```text
python3 scratch/verify_unbounded_fano_line_components.py
```

The standard-library checker constructs depths zero through three,
orders \(10,34,106,322\).  It checks simplicity, cubicity,
bridgelessness, the spanning-tree choices, the outside circuit, every
flow equation, every FiveCDC parity equation, and exact line-component
counts \(1,2,3,4\).  It also independently enumerates the six Petersen
perfect matchings and their two odd complementary circuits.

The universal lower bound is the displayed induction, not an exhaustive
flow enumeration.  This theorem refutes a stronger bounded-component
normal form.  It neither refutes FiveCDC nor supplies the missing global
flow/tree selection theorem.

## AI-use disclosure

OpenAI Codex agents, directed by the user, identified the bounded-component
route, derived the cotree-diamond induction and sharp construction, wrote
the checker, and drafted this note.  The argument and literal construction
are included for verification without trusting the AI system.  No claim
of novelty is made without specialist literature review.
