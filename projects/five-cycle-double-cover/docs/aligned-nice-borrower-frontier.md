# The aligned marked borrower in Ozeki's nice decomposition

Date: **2026-07-26**.

Status: **RESIDUAL N REDUCED TO ONE ALIGNMENT / CAPPED
WATKINS--MESNER REDUCTION / ONE \(b_3\)-TIGHT EQUALITY ATOM**.

This note sharpens residual N from
`one-terminal-trace-lift-frontier.md`.  It does not prove the rooted
four-mark theorem.  The nonaligned borrower closes by the original
\(b_3\) argument.  The aligned borrower has a natural three-terminal
cap to which Watkins--Mesner applies.  That argument forces a cyclic
one-mark shore of cap boundary at most two, but converting the cap
back to the original graph exposes one exact exception: the shore
contains the third nice-decomposition port \(b_3\), and the restored
\(b_3\)-edge makes the marked cyclic-cut inequality tight rather than
violated.

An order-16 graph freezes the local geometry immediately before full
(P4) and the marked-cut inequality enter.  Its rank-six cycle space is
small enough for direct human or exhaustive checking.

## 1. Every nonaligned borrower closes

Use the nice-decomposition notation
\[
\begin{array}{c|c}
X_1&\{a_1,b_1\}\\
X_2&\{a_2,b_2\}\\
A&\{a_1,a_2,b_3\}\\
B&\{b_1,b_2,b_3\}.
\end{array}                                             \tag{1}
\]
Let the expanded singleton row be \(X_1\), with terminal \(z_i\).
Let \(z_2\) be the other singleton terminal in \(X_2\).  The
marked-borrower packet is
\[
             D_{ij},\qquad R_k,\qquad R_l,             \tag{2}
\]
where \(D_{ij}\) contains \(z_i,z_j\), the other two circuits are
private, and all three circuits are pairwise vertex-disjoint.

> **Borrower-alignment lemma.**  If \(j\ne2\), the nice decomposition
> is impossible.  Consequently residual N survives only when
> \(j=2\), so that \(D_{i2}\) contains both singleton rows.

### Proof

If \(j\ne2\), one of the unchanged private circuits in (2) is
\(R_2\).  The circuit \(D_{ij}\) contains the terminal in \(X_1\);
after deleting the singleton row path, it supplies an outside
\(a_1\)-to-\(b_1\) path.  Every such path either contains \(b_3\), or
traverses \(X_2\) through both \(a_2,b_2\).  The latter is impossible:
\(R_2\) contains \(a_2,z_2,b_2\) and is disjoint from \(D_{ij}\).
Thus
\[
                         b_3\in V(D_{ij}).             \tag{3}
\]

Conversely, deleting the \(X_2\) singleton path from \(R_2\) gives an
outside \(a_2\)-to-\(b_2\) path.  It either contains \(b_3\), or
traverses \(X_1\) through \(a_1,b_1\).  The second alternative is
impossible because \(D_{ij}\) contains both boundary vertices of
\(X_1\) and is disjoint from \(R_2\).  Hence
\[
                            b_3\in V(R_2),             \tag{4}
\]
contradicting (3) and the disjointness in (2). \(\square\)

This proof uses the paired packet honestly; it never treats
\(D_{ij}\) as two private circuits.

## 2. The exact aligned \(B\)-cap

Relabel the aligned case as
\[
 z_1\in\operatorname{int}X_1,\quad
 z_2\in\operatorname{int}X_2,\quad
 z_k,z_l\in\operatorname{int}B,
\]
with \(A\) unmarked.  The packet is
\[
                         D_{12},R_k,R_l.               \tag{5}
\]
The restriction of \(D_{12}\) to \(B\) is an unmarked
\(b_1\)-to-\(b_2\) path \(P_0\).  The circuits \(R_k,R_l\) are
contained in \(B\), are disjoint from \(P_0\), and are mutually
disjoint.  Indeed, they avoid \(b_1,b_2\), which lie on \(D_{12}\);
a simple circuit through a terminal in \(B\) cannot leave through
the sole remaining port \(b_3\) and return through that same vertex.

Add a dummy degree-two vertex \(d\) adjacent to \(b_1,b_2\), and put
\[
                      H=B+d,\qquad
 C_d=db_1\cup P_0\cup b_2d.                            \tag{6}
\]
Then
\[
                            C_d,R_k,R_l                \tag{7}
\]
are three pairwise vertex-disjoint private circuits through
\(d,z_k,z_l\).

A circuit of \(H\) through all three of \(d,z_k,z_l\) is equivalent
to a \(b_1\)-to-\(b_2\) path in \(B\) through \(z_k,z_l\).  Ozeki's
nice-decomposition analysis supplies the complementary
\(A\)-side route through the two singleton rows and avoiding \(b_3\).
Thus such a cap circuit gives an all-four circuit in the reduced
nice graph.  Four-terminal acyclicity therefore says that \(H\) has
no circuit through
\[
                              \{d,z_k,z_l\}.            \tag{8}
\]

This is exactly a Watkins--Mesner instance.

## 3. The three-case Watkins--Mesner splitter

Use the equivalent three-case statement of Watkins--Mesner: for three
vertices on no common circuit in a 2-connected graph, either

1. one two-cut separates three disjoint terminal component-unions;
2. three terminal two-cuts have one common vertex and otherwise
   disjoint second vertices; or
3. the three terminal two-cuts are disjoint, and after deleting the
   three terminal component-unions the remainder has exactly two
   components, each meeting each two-cut once.

This is Lemma 2.2 of Sun--Yu, *On a coloring conjecture of Hajós*.
It is equivalent to the \(K_{3,2}\)-decomposition form used in the
Ozeki notes.

For \(u\in\{d,k,l\}\), write \(T_u\) for the corresponding two-cut,
\(D_u\) for its terminal component-union, and
\[
                            S_u=D_u\cup T_u.            \tag{9}
\]
Say that \(C_u\) **exits** when it is not contained in \(S_u\).
An exiting circuit contains both vertices of \(T_u\).

> **At-most-one-exit lemma.**  Among \(C_d,R_k,R_l\), at most one
> circuit exits its Watkins--Mesner terminal shore.

### Proof

In case 1, any two exiting circuits contain the common two-cut and
therefore intersect.  In case 2, any two contain the common cut
vertex and again intersect.

In case 3, an exiting circuit has an inside \(T_u\)-path through
\(D_u\) and an outside path between the two remainder components.
The outside path must cross some other \(D_v\), hence contains both
vertices of \(T_v\).  If two circuits, say \(C_u,C_v\), exit, the
outside path of \(C_u\) cannot cross \(D_v\), because \(C_v\)
contains \(T_v\); symmetrically the outside path of \(C_v\) cannot
cross \(D_u\).  Both must therefore cross the third terminal
component-union \(D_w\), and both contain \(T_w\), a contradiction.
\(\square\)

Consequently at least two of the three private circuits in (7) are
localized in their terminal shores.

## 4. Localizing a contained circuit as an edge shore

The whole set \(S_u\) in (9) need not have small edge boundary.
The correct operation is to assign the two cut vertices to the side
containing \(D_u\) or to its complement.

> **Subcubic localization lemma.**  If a circuit \(C_u\) is contained
> in \(S_u\), a vertex shore \(W_u\subseteq S_u\) can be chosen so
> that
> \[
>       C_u\subseteq H[W_u],\qquad
>       |\delta_H(W_u)|\le2,                           \tag{10}
> \]
> and \(W_u\) contains no other member of \(\{d,z_k,z_l\}\).

### Proof

Start with the components of \(D_u\) met by \(C_u\).  Include every
cut vertex used by \(C_u\).  At such a vertex the circuit already
uses two internal incident edges, so subcubicity leaves at most one
crossing edge.  Assign each unused cut vertex to whichever shore
minimizes its crossing incidences.  A degree-at-most-three vertex
then contributes at most one.  The elementary four assignments of
the two cut vertices also cover the possibility that they are
adjacent.  Thus the total boundary is at most two.

The terminal component-unions are disjoint.  If a cut vertex were
another one of the three terminals, containment or exit through that
vertex would meet its private circuit; equivalently one may use the
standard terminal-avoiding normalization of the Watkins--Mesner
cuts.  Hence \(W_u\) contains only \(u\) among the three specified
vertices. \(\square\)

The majority assignment in this lemma is essential.  Taking all of
\(S_u\) can have boundary four even when (10) has boundary two.

## 5. Conversion to the original marked cubic graph

For \(u=k\) or \(l\), suppress the degree-two terminal \(z_u\).
Because \(C_u\subseteq H[W_u]\), the corresponding marked edge is
internal and the shore remains cyclic.  The dummy cap edges
\(db_1,db_2\) correspond one-for-one to the two outer marked edges
incident with \(b_1,b_2\).  The only edge of the original nice graph
not represented in \(H\) is the edge leaving \(B\) at \(b_3\).
Therefore
\[
 |\delta_L(W_u)|
   =|\delta_H(W_u)|+\mathbf 1_{\{b_3\in W_u\}}.         \tag{11}
\]

The shore has exactly one internal mark.  The marked cyclic-cut
inequality
\[
             |\delta_L(W_u)|+
             |S\cap E(L[W_u])|\ge4                    \tag{12}
\]
contradicts (10) unless
\[
 b_3\in W_u,\qquad
 |\delta_H(W_u)|=2,\qquad
 |\delta_L(W_u)|=3.                                   \tag{13}
\]

If both \(R_k,R_l\) are contained in their terminal shores, their
localized shores can be chosen so that at least one avoids \(b_3\):
in the disjoint-cut case \(b_3\) belongs to at most one shore; in the
common-interface cases a shore whose circuit avoids \(b_3\) assigns
that interface vertex to the other side.  Hence (12) excludes that
possibility.

Together with the at-most-one-exit lemma, a surviving aligned
borrower has exactly the following state:

\[
\begin{array}{c|c}
C_d&\text{contained in its Watkins--Mesner shore}\\
R_k&\text{contained in a tight shore satisfying (13)}\\
R_l&\text{exits its terminal shore}
\end{array}                                            \tag{14}
\]
after possibly exchanging \(k,l\).

Restoring the third \(B\)-edge makes the cut in (13) a three-edge cut
of the cubic graph.  Tait parity gives one boundary edge of each
colour.  The shore contains exactly the common-colour mark \(s_k\),
and the root lies in the outer \(A\)-part.  Thus (13) is an equality
case of the marked cyclic-cut inequality, not a contradiction.

In Watkins--Mesner cases 1 and 2, the exiting \(R_l\) contains the
common interface (the whole common two-cut in case 1 and the common
vertex in case 2).  In case 3 it has an inside \(T_l\)-path and an
outside path crossing \(D_d\) or \(D_k\).  These are the exact open
traces to be compared with the nested endpoint residual E.

## 6. A frozen order-16 control

The graph

```text
O?AA@qoPaW??C@??o?_OA
```

has terminals
\[
                            \{14,15,2,6\}.              \tag{15}
\]
Its nice parts are
\[
\begin{aligned}
X_1&:11-14-0,\\
X_2&:13-15-4,\\
A&:\text{the star with centre \(12\) and leaves \(11,13,3\)},\\
B&:\text{the induced graph on \(0,\ldots,10\)}.
\end{aligned}                                          \tag{16}
\]
The aligned packet is
\[
\begin{aligned}
D_{12}&=(0,14,11,12,13,15,4,10,5,0),\\
R_k&=(2,7,3,8,2),\\
R_l&=(6,1,9,6).
\end{aligned}                                          \tag{17}
\]
The three circuits are pairwise vertex-disjoint.

Four displayed T3 circuits are
\[
\begin{array}{c|l}
\{2,6,14\}&
(11,14,0,5,9,6,1,10,4,7,2,8,3,12,11)\\
\{2,6,15\}&
(13,15,4,10,1,6,9,5,0,8,2,7,3,12,13)\\
\{2,14,15\}&
(11,14,0,8,2,7,4,15,13,12,11)\\
\{6,14,15\}&
(11,14,0,5,9,6,1,10,4,15,13,12,11).
\end{array}                                            \tag{18}
\]

The graph is 2-connected and subcubic.  Its cycle-space rank is six.
Exactly four nonzero binary cycles cover all four terminals; their
marked-component profiles are
\[
 (3,1),\qquad(2,1,1),\qquad(3,1),\qquad(3,1).          \tag{19}
\]
Thus it has no componentwise-even certificate.

It satisfies (P4) after deleting \(b_3=3\), but full (P4) fails
exactly after deletions
\[
                              0,\quad4,\quad12.         \tag{20}
\]
The cap \(B+d\) is 2-connected and has graph6 record

```text
K?AA@qoPaWP?
```

Its common two-cut \(\{0,4\}\) exposes the three private cap
circuits.  The \(R_k\)-shore contains \(b_3\), so restoring the third
port changes its boundary from two to three.  The \(R_l\)-shore
avoids \(b_3\), retains boundary two, and violates (12).  This is a
literal finite model of the conversion distinction in (11).

The independent checker is

```sh
python3 scratch/verify_aligned_nice_countermodel.py
```

## 7. Completed fixed-star screen

The exact generator

```sh
python3 scratch/search_aligned_nice_full_p4.py \
  --minimum-B-order 6 --maximum-B-order 11
```

canonically generates the \(B\)-part and attaches the minimum
three-port \(A\)-star and the two singleton rows.

Through \(B\)-order 10, no packet row was both T3 and
certificate-free.  At \(B\)-order 11, 5,524 nonisomorphic connected
subcubic graphs gave 9,660 packet extensions.  Of these, 3,804
assembled graphs were 2-connected, 436 satisfied T3, and ten were
simultaneously T3 and certificate-free.  All ten failed full (P4);
their deletion-failure profiles and multiplicities were
\[
\begin{array}{c|r}
\{0,2,12\}&5\\
\{0,4,12\}&2\\
\{1,4,12\}&2\\
\{2,3,12\}&1.
\end{array}                                            \tag{21}
\]

This is an exact finite statement only for the fixed minimum
\(A\)-star and the completed orders.  Ozeki's nice obstruction is
compatible with full (P4) in general, so (21) is not a P4-only
theorem.

## 8. Remaining atom

Residual N is no longer an arbitrary marked borrower.  It is the
\(b_3\)-tight equality state (13)--(14):

1. the dummy packet circuit and exactly one marked factor circuit are
   localized by Watkins--Mesner;
2. the marked localized shore contains \(b_3\) and has cap boundary
   two;
3. restoring the \(b_3\)-edge gives an \(abc\) three-cut with exactly
   one internal mark and marked-cut value four;
4. the other marked factor circuit has the corresponding exiting
   two-cut trace.

The next valid step is either to descend this equality shore by the
existing endpoint recursion E, or to use universal Tait separation
to exclude the exiting trace.  Omitting the \(b_3\) correction in
(11), or calling all of \(S_u\) a two-edge shore, would be invalid.
