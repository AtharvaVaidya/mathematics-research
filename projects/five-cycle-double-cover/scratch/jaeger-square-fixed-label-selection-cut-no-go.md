# A three-edge cut kills the fixed-five-label square-selection route

Date: 2026-07-28

Status: **HUMAN COUNTERMODEL TO THE FIXED-COVER LABEL-SELECTION
STATEMENT / TREE-LOCAL (L) AND (F) HOLD IN THE EXAMPLE / NOT A
COUNTEREXAMPLE TO FIVE-CDC**.

## 1. The cut lemma

Write an indexed five-cycle double cover as a label
\[
             \lambda(g)\in\binom{\{0,1,2,3,4\}}2
\]
on every edge \(g\), recording the two cover members containing \(g\).

> **Lemma.**  If a three-edge cut is
> \(\delta(X)=\{g_0,g_1,g_2\}\), then the three labels
> \(P_i=\lambda(g_i)\) meet pairwise in exactly one point.

**Proof.**  Every Eulerian edge-subset meets every cut evenly.  Applying
this to each of the five cover coordinates gives
\[
                         P_0\mathbin\triangle
                         P_1\mathbin\triangle P_2=\varnothing.       \tag{1}
\]
Hence \(P_2=P_0\triangle P_1\).  Since all three sets have size two,
\[
          2=|P_0\triangle P_1|
            =4-2|P_0\cap P_1|,
\]
so \(|P_0\cap P_1|=1\).  Write
\(P_0=\{a,b\}\) and \(P_1=\{a,c\}\), where \(a,b,c\) are distinct.
Equation (1) now forces
\[
                         P_2=P_0\triangle P_1=\{b,c\}.              \tag{2}
\]
Thus all three labels are the three sides of one triangle on the common
three-coordinate set \(\{a,b,c\}\); in particular, every two meet in
exactly one point. \(\square\)

Modulo the \(S_5\) action, the boundary pattern is uniquely
\[
                         01,\quad02,\quad12.                       \tag{3}
\]
In particular, no two edges of a three-edge cut have equal or disjoint
five-cover labels.

## 2. A six-vertex literal countermodel

Use the triangular prism with ordered edges

```text
0:(0,1)  1:(0,2)  2:(0,3)
3:(1,2)  4:(1,4)  5:(2,5)
6:(3,4)  7:(3,5)  8:(4,5).
```

Its exact labelled graph6 record is `E{Sw`.  (The edge order above is
part of the certificate and is not the graph6 upper-triangle order.)
Take root \(r=0\), and select the independent nonroot edges
\[
                            e=4=(1,4),\qquad f=5=(2,5).             \tag{4}
\]
They belong to the three-edge cut
\[
                   \delta(\{0,1,2\})=\{2,4,5\}.                    \tag{5}
\]
The cut lemma says something stronger than the failed selection
assertion: **no five-cycle double cover of this graph whatsoever** gives
\(e,f\) equal or disjoint labels.

The antecedent is nonvacuous in the exact Jaeger star fibre.  The three
trees

```text
T0 = {0,3,4,6,7}
T1 = {1,3,5,7,8}
T2 = {2,4,5,6,8}
```

They have each root edge once and every nonroot edge twice.
Their edge-bit masks (edge 0 is the low bit) are

```text
217  426  372
```

Their odd kernels are

```text
K0 = {0,3,4,7}
K1 = {1,3,5,7,8}
K2 = {2,4,5},
```

and their coordinate defect profile is
\[
                              (2,0,2).                            \tag{6}
\]
Thus this is an exact-good star state.  One compatible canonical
five-point labelling, in edge order, is

```text
06  56  05  46  04  45  07  57  47.
```

The three cut labels are \(05,04,45\), displaying (3) directly.  Because
the cut lemma applies to every five-cover, changing the tree state, the
good Fano functional, the port solution, or the \(S_5\) normalization
cannot repair (3).

This disproves the proposed fixed-label selection statement:

> An exact-good star fibre and an independent nonroot edge pair need not
> contain any exact-good state whose induced five-cover labels on that
> pair are equal or disjoint.

The obstruction is structural rather than a missed automorphism orbit.

## 3. Why this does not refute tree-local square lifting

The fixed-cover square criterion holds the entire outside
five-labelling fixed.  A square-local lift of a tree triple holds the
outside **tree memberships** fixed.  Its odd kernels and the compatible
five-labelling may nevertheless change on old edges, because the square
can reconnect the components created by deleting \(e,f\).  These are
different assertions.

Indeed, delete edges 4 and 5 and insert
\[
 Aa,Bb,Cc,Dd,ab,bc,cd,da
\]
with \(A=1,B=2,C=4,D=5\).  In the expanded edge order used by the checker,
the exact labelled graph6 record is `I{CY@CH@g`, and
the following is a square-local lift of the displayed state:

```text
S0 = {0,3,4,5,7,9,10,11,14}
S1 = {1,3,5,6,8,9,11,12,13}
S2 = {2,4,6,7,8,10,12,13,14}.
```

The full lifted edge-bit masks are

```text
20153  15210  30164
```

and the gadget-only masks in the order
\((Aa,Bb,Cc,Dd,ab,bc,cd,da)\) are

```text
10011101  01110110  11101011.
```

Its defect profile is again \((2,0,2)\).  Consequently:

* the fixed-five-label selection route is false;
* the stronger tree-local statement (L) is **true** for this literal
  graph/root/pair instance;
* hence the whole-fibre implication (F) is also true here; and
* neither this prism nor its square expansion is a counterexample to
  Five-CDC.

The failure therefore cannot be used to reject (L), (F), or ordinary
four-cycle reducibility.  It only proves that (L) cannot be established
by first choosing a downstairs five-cover whose labels extend unchanged.

## 4. Independent replay

Run

```sh
python3 scratch/verify_jaeger_square_fixed_label_selection_cut_no_go.py
```

The standard-library checker independently:

1. verifies simplicity, cubicity, and three-edge-connectivity downstairs
   and upstairs;
2. reconstructs the two displayed odd-kernel profiles and all tree
   multiplicities;
3. checks the displayed canonical five-point labelling against the
   completion flow;
4. directly generates all \(540\) indexed pair-label assignments on the
   five named cover coordinates (unused coordinates are allowed), with
   every edge in exactly two coordinates and Eulerian parity at every
   vertex, and verifies the one-point-intersection statement for every
   one; and
5. checks the explicit exact-good square-local lift.

The exhaustive enumeration is a redundant finite audit of the two-line
cut proof, not the logical basis of the universal cut lemma.

## AI-use disclosure

OpenAI Codex, under human direction, identified the three-edge-cut
obstruction, proved the cut lemma, found the literal star/lift witnesses,
and wrote the independent checker.  This note disproves one proposed
selection lemma.  It does not claim a proof or disproof of Five-CDC.
