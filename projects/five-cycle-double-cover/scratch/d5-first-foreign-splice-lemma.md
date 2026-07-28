# The first-foreign factor-splice lemma

Date: **2026-07-28**

Status: **HUMAN-CHECKABLE SWITCHING LEMMA / NAIVE IMMEDIATE-RESCUE
COROLLARY REFUTED / NOT A FIVECDC RESOLUTION**.

## 1. Exact factor identity

For a coordinate pair \(A\), let
\[
 a_A(L)=|A\cap L|\pmod2,\qquad
 Y_A(q)=\{e:a_A(q(e))=1\}.
\]
Let \(P,Q\) be coordinate pairs with \(|P\cap Q|=1\), and put
\[
                         P'=\tau_Q(P)=P\mathbin\triangle Q.
\]
Let \(H\) be one component of \(Y_Q(q)\), and obtain \(q'\) by
transposing the two coordinates of \(Q\) on \(H\).

Then
\[
             \boxed{Y_{P'}(q')
                    =Y_P(q)\mathbin\triangle
                     \bigl(Y_Q(q)\setminus H\bigr).}           \tag{1}
\]

Indeed, outside \(H\), labels are unchanged and
\(a_{P'}=a_P+a_Q\).  On \(H\),
\[
                       a_{P'}(\tau_Q L)=a_P(L).
\]
Since \(a_Q=1\) on every edge of \(H\), these two cases are exactly
the indicator identity
\[
 1_{Y_{P'}(q')}=1_{Y_P(q)}+1_{Y_Q(q)}+1_H\pmod2,
\]
which is (1).

The point is easy to miss: every later intersection with the switched
component \(H\) is absent from the toggling set in (1).  It causes no
splice in the new \(P'\)-factor.  Only components of \(Y_Q\) different
from \(H\) are visible.

## 2. First-foreign splice

Let \(C\) be the component of \(Y_P(q)\) containing root edge \(r\).
Let \(D\ne H\) be another component of \(Y_Q(q)\).  Orient the circuit
\(C\) from \(r\), ignoring every edge in \(H\), and suppose the first
edge encountered which belongs to any component of
\(Y_Q(q)\setminus H\) belongs to \(D\).

**First-foreign splice lemma.**  The component \(R\) of
\(Y_{P'}(q')\) containing \(r\) contains an edge of \(D\).

**Proof.**  By (1), the initial \(C\)-segment from \(r\) remains in the
new \(P'\)-factor until it reaches \(D\).  Let \(S\) be the maximal
common path of \(C\) and \(D\) beginning at that first encounter.
At the entrance vertex of \(S\), let \(c\) be the preceding
\(C\)-edge and let \(d\) be the incident \(D\)-edge outside \(S\).
The shared edges of \(S\) cancel in the symmetric difference, whereas
\(c\) and \(d\) remain.  Cubicity leaves degree two there, so the
transition in
\[
                      Y_P(q)\triangle(Y_Q(q)\setminus H)
\]
pairs \(c\) with \(d\).  Hence the new component reached from \(r\)
uses \(d\in D\). \(\square\)

Only one orientation of \(C\) needs to encounter \(D\) first.

## 3. Distance-two consequence

Suppose \(C,D\) form a factor-component chain of length two from roots
\(r\) to \(s\), with \(r\in C\cap H\) and \(s\in D\).  A \(Q\)-switch
does not change the support or component partition of \(Y_Q\), so
\(D\) is still a \(Q\)-component after the switch.  The first-foreign
lemma gives the new chain
\[
                              R,D.
\]
Therefore
\[
                              d_{q'}(r,s)\le2.                  \tag{2}
\]

This conclusion is independent of surface Euler characteristic and
terminality.  If the \(H\)-switch is neutral inside a terminal plateau,
(2) is a sound non-increasing endpoint move.

## 4. Why immediate rescue is false

It is tempting to strengthen (2) to \(d_{q'}(r,s)=1\), especially when
both orientations of \(C\) encounter a later \(H\)-segment before
reaching \(D\).  Identity (1) shows why that reasoning is unsound:
those \(H\)-segments are invisible.

A literal counterexample occurs on graph6
```text
K??FEbGL@WB_
```
with state
```text
03 05 06 05 06 03 06 03 05 03 06 05 05 06 03 05 03 06
```
and roots \(r=1,s=15\).  Take
\[
\begin{array}{c|c|l}
C&01&\{1,2,3,4,6,8,12,13\}\\
H&03&\{0,1,3,5,9,11,12,14\}\\
D&03&\{7,8,15,16\}.
\end{array}
\]
The cyclic order of \(C\) from \(r\) is
\[
                         1,4,3,6,8,13,12,2.
\]
The root component of \(C\cap H\) is \(\{1\}\).  In one orientation,
edge \(3\in H\) occurs before edge \(8\in D\); in the other, edge
\(12\in H\) occurs before that same \(D\)-edge.  Thus the naive
both-arc \(H/H\) hypothesis holds.

Switching \(03\) on \(H\) is neutral:
\[
                              \chi:0\longrightarrow0,
\]
but the exact rooted distance is
\[
                               2\longrightarrow2,
\]
not one.  The new \(P'=13\) component through \(r\) has edge mask
\(0x33cde\); it intersects \(D\) in edges \(7,16\), exactly as the
first-foreign lemma predicts, but does not contain \(s=15\).

The state lies in a genuine terminal equal-\(\chi\) plateau: exhaustive
breadth-first search modulo global \(S_5\) gives seven states and no
positive exit.

## 5. Reproduction

```text
python3 scratch/check_d5_terminal_both_arc_reentry_no_go.py
python3 scratch/audit_d5_first_foreign_splice_order12.py
```

The standard-library checker verifies the graph, bridgelessness, cubic
flow equations, factor components, both oriented scans, exact factor
distances, neutral switch, the new \(P'\)-component, and the complete
terminal plateau.

An independent complete terminal order-12 audit gives:
\[
\begin{array}{c|r}
\text{biconnected simple cubic graphs}&81\\
\text{normalized flows}&25\,960\\
\text{terminal equal-}\chi\text{ plateaus}&2\,659\\
\text{states in terminal plateaus}&20\,578\\
\text{first-foreign configurations}&2\,154\,613\\
\text{exact rooted distance-two cases}&1\,688\,084\\
\text{failures}&0.
\end{array}
\]
This finite audit is a cross-check, not a substitute for the proof of
(1) and the transition-pairing argument.

## AI-use disclosure

OpenAI Codex agents, under human direction, formulated and proved the
first-foreign splice lemma, found the terminal counterexample to the
stronger rescue claim, wrote the independent checker, and drafted this
note.  This is not peer review and is not a resolution of FiveCDC.
