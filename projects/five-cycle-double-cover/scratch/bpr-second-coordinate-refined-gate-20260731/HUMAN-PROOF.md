# The exact aggregate-gain gate for second-coordinate descent

Date: **2026-07-31**

Status: **SHARPENED FIXED-RESIDUAL DESCENT CHARACTERIZATION / REDUCED
CUT-SPACE OBSTRUCTION / HIGH-GIRTH CYCLICALLY-4 TAIT COUNTERCONTROL /
NON-TAIT COORDINATION STILL OPEN / NOT BPR / NOT FIVECDC**.

## 1. Fixed-Eulerian-set notation

Use the setup of `bpr-second-coordinate-descent-20260731`.  Thus (G) is a
finite loopless cubic graph with a nowhere-zero
(\mathbb F_2^3\)-flow, (M=M_b) is one value class, (J\subseteq G-M)
is a (\partial M\)-join, and

\[
 F=M\mathbin{\dot\cup}J
\]

is Eulerian.  Its residual components are the components (C) of (G-F).
For each one put

\[
 d_C=|\delta_G(C)|,
 \qquad q_C=|\delta_M(C)|,
 \qquad k_C=d_C-q_C.
\tag{1}
\]

Let (X\subseteq G-M_t) be a legal binary (t)-switch, and write

\[
 D^-=X\cap M_b,
 \qquad D^+=X\cap M_{b+t}.
\]

Assume the all-in condition (D^+\subseteq J).  Then

\[
 M'=(M-D^-)\mathbin{\dot\cup}D^+\subseteq F,
 \qquad J'=F-M'
\tag{2}
\]

is a valid new join.  In particular, (F), every residual component, and
every (d_C) stay fixed.  Define

\[
 q'_C=q_C-|D^-\cap\delta(C)|+|D^+\cap\delta(C)|,
 \quad
 \Delta_C=q'_C-q_C,
 \quad
 \epsilon_C=\Delta_C\pmod2.
\tag{3}
\]

Let

\[
 \mathcal O=\{C:q_C\text{ is odd}\},
 \qquad \mathcal E=\{C:q_C\text{ is even}\},
\]

and append a subscript (0) or (1) to select the value of
(\epsilon_C).

## 2. Exact second-coordinate change

Write

\[
 S(M,J)=\sum_{C:q_C\text{ is odd}}(d_C-q_C)
       =\sum_{C\in\mathcal O}k_C.
\tag{4}
\]

There are four disjoint component cases.

* If (C\in\mathcal O_0), it remains odd and contributes
  (k'_C-k_C=-\Delta_C).
* If (C\in\mathcal O_1), it becomes even and its old (k_C) summand is
  removed.
* If (C\in\mathcal E_1), it becomes odd and contributes the new summand
  (k'_C=d_C-q'_C).
* A component in (\mathcal E_0) contributes neither before nor after.

Therefore the exact global formula is

\[
 \boxed{
 S(M',J')-S(M,J)
 =-\sum_{C\in\mathcal O_0}\Delta_C
  -\sum_{C\in\mathcal O_1}k_C
  +\sum_{C\in\mathcal E_1}(d_C-q'_C).}
\tag{5}
\]

Define the **aggregate gain**

\[
 \boxed{
 \mathcal G(X)=
 \sum_{C\in\mathcal O_1}k_C
 +\sum_{C\in\mathcal O_0}\Delta_C
 -\sum_{C\in\mathcal E_1}(d_C-q'_C).}
\tag{6}
\]

Then (5) is simply

\[
                    S(M',J')-S(M,J)=-\mathcal G(X).
\tag{7}
\]

This is more permissive than the preceding componentwise theorem.  A
surviving old odd component may have (q'_C<q_C), and an old even component
may become odd, provided the losses are more than compensated in the single
global sum (6).

For example,

\[
 (d,q):\quad (6,1)\mid(6,2)
       \longmapsto (6,0)\mid(6,3)
\]

has potential ((0,5)\to(0,3)).  The old even six-cut flips, so the former
condition protecting every even component rejects this valid descent.
Likewise

\[
 (6,1)\mid(8,5)\longmapsto(6,0)\mid(8,3)
\]

has potential ((0,8)\to(0,5)), although the surviving old odd component
loses two target edges.  Its loss is compensated by removing the first
summand.

## 3. Exactly which old even components need parity protection

A fixed residual component is tight exactly when (d_C=4) and (q_C) is
odd.  Suppose the old first coordinate is zero.  Then no old odd component
has (d_C=4).  Since (d_C) remains fixed, a new tight component can only
be an old even four-cut whose parity flips.  Conversely, every such flip is
new tight.  Hence

\[
 \boxed{
 \#\{\text{new tight components}\}
 =|\{C\in\mathcal E:d_C=4,\ \epsilon_C=1\}|.}
\tag{8}
\]

This proves that only the family

\[
             \mathcal E_4=\{C\in\mathcal E:d_C=4\}
\tag{9}
\]

needs parity protection when descending from first coordinate zero.

## 4. Exact refined descent theorem

Recall

\[
 \Psi(M,J)=(\#\text{tight components},S(M,J)).
\]

**Theorem 4.1 (aggregate-gain characterization).**  Suppose the old first
coordinate is zero and the all-in hypothesis (2) holds.  Then

\[
 \boxed{
 \Psi(M',J')<_{\rm lex}\Psi(M,J)}
\]

if and only if

1. (\epsilon_C=0) for every (C\in\mathcal E_4); and
2. (\mathcal G(X)>0).

If (J) realizes (\Psi^*(M)), the same two conditions imply

\[
 \Psi^*(M')\le\Psi(M',J')<\Psi^*(M).
\]

**Proof.**  Because the old tight count is zero, lexicographic descent is
possible only if the new tight count is also zero.  By (8), this is
equivalent to condition 1.  With both first coordinates zero, strict
lexicographic descent is equivalent to strict decrease of (S), which by
(7) is equivalent to condition 2.  The optimized inequality follows because
(J') is an admissible new join. \(\square\)

Thus the theorem is a necessary-and-sufficient characterization for the
fixed-(F), all-in candidate.  It does **not** assert that a switch satisfying
the two conditions always exists.

There is also a scalar weighted form.  Since every residual cut edge lies in
(F\subseteq E(G)),

\[
                     0\le S(M,J)\le2|E(G)|.
\]

For (W=2|E(G)|+1), the scalar potential

\[
 \Pi_W(M,J)=W\,\#\{\text{tight components}\}+S(M,J)
\tag{10}
\]

induces the same lexicographic order.  From old first coordinate zero its
exact change is

\[
 \Pi_W(M',J')-\Pi_W(M,J)
 =W|\{C\in\mathcal E_4:\epsilon_C=1\}|-\mathcal G(X).
\tag{11}
\]

This scalarization does not make (\mathcal G) a linear cycle-space
functional; the parity-dependent appearance and disappearance of summands
is precisely the remaining difficulty.

## 5. The reduced binary obstruction

For a partner-free direction (t), the all-in cycle space is

\[
 Z_1(L_t;\mathbb F_2),\qquad
 L_t=G-\bigl(M_t\cup(M_{b+t}-J)\bigr).
\tag{12}
\]

Put

\[
 a_C=(M_b\cup M_{b+t})\cap E(L_t)\cap\delta_G(C).
\]

The parity part of Theorem 4.1 is now only

\[
 \langle a_Q,X\rangle=1,
 \qquad
 \langle a_C,X\rangle=0\quad(C\in\mathcal E_4).
\tag{13}
\]

Binary linear duality gives the exact reduced obstruction:

\[
 \boxed{
 \text{(13) is infeasible}
 \Longleftrightarrow
 \exists\mathcal I\subseteq\mathcal E_4:\quad
 a_Q\mathbin{\triangle}
 \mathop{\triangle}_{C\in\mathcal I}a_C
 \in B^1(L_t;\mathbb F_2).}
\tag{14}
\]

Only even four-cut rows occur in (14), rather than every old even residual
component.  If (13) is feasible, the independent integer test
(\mathcal G(X)>0) still has to be met.

## 6. High-girth cyclically-4 structure does not kill (14)

The frozen order-80 control in
`../order80-girth10-binary-repair-state.txt` gives a finite exact warning.
The checker in this package independently verifies that its host is simple,
connected, cubic, has girth ten, and has no cyclic edge cut of size one, two,
or three.  It also directly checks the three-edge-colouring in
`../order80-girth10-tait-flow-state.txt`; the host is therefore a Tait
control, not a BPR-domain graph.

For target (b=1), the frozen first join has

\[
                     \Psi(M,J)=(0,44),
\]

eleven residual components and five protected old even four-cuts.  The five
odd components with (k<9) have twelve partner-free directions in total.
The checker constructs the complete fundamental-cycle basis of every
all-in graph (L_t), enumerates every binary cycle, and evaluates the
refined parity equations and exact new potential.

Four directions fail the reduced parity gate.  Three already have
(a_Q\in B^1(L_t)).  A fourth has (a_Q\notin B^1(L_t)), but

\[
                     a_Q\triangle a_{C_4}\in B^1(L_t)
\]

for one protected even four-cut (C_4).  More sharply, one old
((5,1)) blocker has three partner-free directions (2,4,7): directions
2 and 7 have the single-row obstruction, while direction 4 has the displayed
one-protected-row obstruction.  Thus **none** of its partner-free directions
satisfies (13).

The remaining eight directions are feasible and all eight have a strict
fixed-(F) descent; their best new potentials range from ((0,20)) down to
((0,0)).  This demonstrates both sides of the sharpened gate: it permits
real descents rejected by the older protection rule, but it is not
automatically feasible.

Consequently simplicity, cyclic edge connectivity at least four, and girth
at least ten do not by themselves eliminate the cut-space obstruction.  The
finite countercontrol is Tait-colourable.  No certified **non-Tait** host
with this reduced obstruction was found here, so the additional BPR-domain
question remains open.

## 7. Exact computational audits and scope

Run:

```sh
python3 -B verify_refined_formula.py
python3 -B analyze_order80_control.py
shasum -a 256 -c SHA256SUMS
shasum -a 256 -c SOURCE-SHA256SUMS
```

The abstract checker verifies (5) on 1,771 single-component transitions,
the tight-creation identity (8) on 1,761 transitions, and the refined theorem
on 439,569 protected two-component transitions.  Of those, 188,563 have
positive aggregate gain and are checked to descend.

The graph checker imports no candidate helper.  It reconstructs the graph,
flow, join, residual components, cut rows, cycle bases, all-in cycles,
dual-obstruction subsets, and potentials directly from the two frozen state
files.

The result is an exact improvement of the conditional gate, not a universal
descent.  It neither proves nor refutes BPR and does not resolve FiveCDC.
All prose and code in this package were produced by OpenAI Codex under human
direction and have not received independent human peer review.
