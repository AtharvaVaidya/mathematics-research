# Augmented lexicographic radius-three frontier

Date: **2026-07-29**

Status: **HUMAN-CHECKABLE PATH ALGEBRA AND PRECISE PROOF
OBLIGATION / EXACT AND SAMPLED FINITE EVIDENCE / NO UNIVERSAL PROOF.**

This note uses the project's current order
\[
                 \Psi=(d_{\min},S),\qquad
                 S=|K_0|+|K_1|+|K_2|,
\]
lexicographically, and declares any state with a successful parallel
component--circuit span flag terminal below every positive value of
\(\Psi\).  It does not use \(d_{\min}\) alone.

## 1. The bounded escape statements

Call a state **safe at level \(\Psi_0\)** when all 21 parallel-span
flags fail and its potential is exactly \(\Psi_0\).  An augmented
escape path from a positive safe state \(s_0\) is a legal reciprocal
exchange path
\[
                         s_0,s_1,\ldots,s_t
\]
such that every \(s_q\), \(q<t\), is safe at level \(\Psi(s_0)\), and
the endpoint either has a successful flag or has strictly smaller
\(\Psi\).

The strongest bounded statement consistent with every current exact
check is:

> **Augmented lexicographic radius-three obligation.**  Every positive
> safe Jaeger star state has an augmented escape path of length at
> most three.

The stronger radius-two obligation is false.  The independently checked
package
`jaeger-order40-augmented-radius-two-counterexample-20260729/`
gives a cyclically four-edge-connected cubic graph and a state of exact
augmented escape distance three.  Radius one is also false: the frozen
Möbius--Kantor state and the frozen 130-vertex girth-ten lift state are
augmented immediate traps, and both have exact escape distance two.

The order-40 state previously described as having augmented distance
three is not a counterexample to radius two in this order.  Its
distance-three statement uses \(d_{\min}\) as the only numeric level.
Its first exchange changes the kernel-size triple
\[
                  (26,27,25)\longrightarrow(26,27,24),
\]
so under lexicographic \(\Psi\) it immediately lowers \(S\) from 78 to
77 and has escape distance one.

## 2. Exact kernel law for one, two, or three exchanges

Index a legal path by \(q=1,\ldots,t\), with \(t\leq3\).  At step \(q\)
the reciprocal exchange uses coordinates \(i_q,j_q\).  For every
coordinate \(i\), define \(Z_{q,i}=\varnothing\) when \(i\) is not
involved.  If \(i\) is involved, let \(C_{q,i}\) be the fundamental
circuit in the **current** tree \(T_i^{q-1}\) of the edge inserted at
step \(q\), and let \(b_{q,i}\) be the removed tree edge.  Put
\[
 Z_{q,i}=
 \begin{cases}
 C_{q,i},&b_{q,i}\in K_i^{q-1},\\
 \varnothing,&b_{q,i}\notin K_i^{q-1}.
 \end{cases}                                                \tag{1}
\]
The one-step odd-kernel exchange law gives
\[
                  K_i^q=K_i^{q-1}\mathbin\triangle Z_{q,i}. \tag{2}
\]
Consequently, with
\[
                  Y_i^t=\mathop{\triangle}_{q=1}^t Z_{q,i},
\]
telescoping gives the exact endpoint identities
\[
\boxed{
\begin{aligned}
 K_i^t&=K_i^0\mathbin\triangle Y_i^t,\\
 |K_i^t|&=|K_i^0|+|Y_i^t|-2|K_i^0\cap Y_i^t|,\\
 S_t&=\sum_i\bigl(|K_i^0|+|Y_i^t|
                         -2|K_i^0\cap Y_i^t|\bigr).
\end{aligned}}                                               \tag{3}
\]
Thus each reciprocal exchange changes the flow through at most two
legal circuit additions, one in each changed coordinate.  A path of
length at most three has at most six such additions.

For the derived \(W=\mathbb F_2^3\)-flow and every nonzero functional
\(h\), put
\[
 Y_h^t=\mathop{\triangle}_{i:h(e_i)=1}Y_i^t.
\]
Then
\[
\boxed{
\begin{aligned}
 \phi_t&=\phi_0+\sum_i e_i1_{Y_i^t},\\
 E_h^t&=E_h^0\mathbin\triangle Y_h^t.
\end{aligned}}                                               \tag{4}
\]
Equations (3)--(4) are valid without any disjointness assumption on
the circuits and already include cancellation when a later active
switch undoes an earlier one.

Choose \(g,\ell\) completing \(h\) to a basis of \(W^*\).  If
\(Y_h^t=\varnothing\), the \(E_h\)-component quotient is fixed and the
defect update is
\[
 \beta_h^t=\beta_h^0+\partial_h R,\qquad
 R=(Y_g^t\cap E_\ell^0)
   \mathbin\triangle(E_g^0\cap Y_\ell^t)
   \mathbin\triangle(Y_g^t\cap Y_\ell^t).                   \tag{5}
\]
If \(Y_h^t\ne\varnothing\), the exact rule is instead to take the
components of \(E_h^0\triangle Y_h^t\) and, on every new component
\(Q\), compute
\[
 |\delta(Q)\cap(E_g^0\triangle Y_g^t)
                  \cap(E_\ell^0\triangle Y_\ell^t)|\pmod2.  \tag{6}
\]
The 21 terminal span flags are then recomputed from these new
components and the outside-circuit switch spaces.

This separates two notions that must not be conflated.  By
Hušek--Šámal Theorem 3.16, a zero entry of the seven-component profile
is direct component-parity success for the **current** nowhere-zero
\(\mathbb F_2^3\)-flow.  A positive parallel span flag is a separate
certificate that allowed whole-circuit switches reach a zero defect.
The radius-two counterexample has positive profile and zero flags at
every state through distance two.  Its distance-three endpoint has a
zero profile entry and, additionally, three successful flags.

## 3. Eliminating adaptive fundamental circuits

The word “current” in (1) is essential, but it can be unfolded by an
exact tree-pivot identity.  Let
\[
                         T'=T-b+a,\qquad b\in C_T(a).
\]
For any \(x\notin T'\),
\[
 C_{T'}(x)=
 \begin{cases}
 C_T(a),&x=b,\\
 C_T(x),&x\ne b\text{ and }b\notin C_T(x),\\
 C_T(x)\mathbin\triangle C_T(a),
      &x\ne b\text{ and }b\in C_T(x).
 \end{cases}                                                \tag{7}
\]
This follows because the displayed sets are the unique circuits in
\(T'+x\).  Applying (7) after each earlier pivot expresses every
circuit occurring in a path of length at most three as an xor of
fundamental circuits relative to the starting trees.  At most six
binary pivot-incidence tests are required.

## 4. Finite syntactic case reduction

Write \(A,B,C\) for the three unordered coordinate pairs.  Up to
renaming coordinates and reversing the word, the coordinate-pair
words of length at most three have the following forms:

```text
length 1: A
length 2: AA, AB
length 3: AAA, AAB, ABA, ABC.
```

At each exchange the two sides have activity pattern
\((0,0),(1,0),(0,1)\), or \((1,1)\).  Before quotienting further
symmetries, this gives at most
\[
                   4+2\cdot4^2+4\cdot4^3=292              \tag{8}
\]
coordinate/activity templates.  Unfolding the at most six binary
branches in (7) gives at most
\[
                         292\cdot2^6=18\,688               \tag{9}
\]
syntactic path skeletons.

This is a real reduction, but it is not yet a finite proof.  A skeleton
does not determine:

1. the sizes and intersections of the starting fundamental circuits;
2. how \(E_h\triangle Y_h\) splits or merges components;
3. the placement of the old defect support on those components; or
4. the outside-component circuit spans used by the 21 terminal flags.

Those data are unbounded with the graph order.  Therefore checking the
18,688 Boolean skeletons without retaining the circuit/component
incidence geometry would be unsound.

There is a proved compression on the planes whose topology stays
fixed.  For an orthogonal marked addition
\[
                         f'=f+h\chi_Z,\qquad h\in H=\ker a,
\]
contract the \(H\)-edge components and let \(B\) be outside-edge
incidence.  On an outside circuit \(C\), the marked selector spaces
satisfy
\[
 A'_{C,h}=A_{C,h},\qquad
 A'_{C,k}=A_{C,k}+u_C\quad(k\ne h),\qquad
 u_C=B\chi_{Z\cap C},
\]
with \(\bigoplus_Cu_C=0\), while
\[
                         \beta'=\beta+B(\chi_Zw_h).
\]
This follows from the two-dimensional identity
\(1_{p\in\{0,k\}}=1+\lambda_k(p)\), and is independently checked by
`verify_qfull_marked_orthogonal_move_update.py`.  It safely compresses
the fixed-\(H\) part of the 292 templates.  It does **not** force an
endpoint: exact controls realize every relevant flip-parity pattern,
including no change, and the four Fano planes whose defining
functional evaluates nontrivially on \(h\) undergo the component
changes excluded from this formula.  Thus no `AA` or `AB`
template is discharged by marked \(q_{\rm full}\) alone.

For radius two only the words `AA` and `AB` occur, giving 32
activity-decorated templates before symmetry.  The frozen Möbius
escape realizes `AA` with activity patterns `(1,0),(1,1)`.  The first
frozen girth-ten escape realizes `AA` with `(0,0),(0,1)`.  Across the
eight independently replayed girth-ten sample traps, both `AA` and
`AB` occur, and second-step activity patterns `(0,1)`, `(1,0)`, and
`(1,1)` occur.  Hence neither a fixed coordinate word nor a
fixed “both steps active” assumption can prove an escape statement.
The order-40 counterexample proves that the full 32-template
radius-two obligation cannot be discharged at all.

## 5. Exact finite frontier and remaining human step

The following evidence uses the lexicographic \(\Psi\) above.

- The Möbius--Kantor trap has exact augmented escape distance two.
- All eight traps in the frozen 130-vertex girth-ten package have
  exact distance two; the checker exhausts 98,304 reciprocal
  candidates and all 3,220 legal first neighbourhoods.
- The expanded frozen lift portfolio contains 196 sampled augmented
  immediate traps.  Independent replay found a two-exchange escape for
  every sampled trap.  This is randomized state sampling, not a
  state-space census.
- Two seeded runs on all seven retained order-34 strong snarks found
  169 further augmented immediate traps; exact independent replay found
  distance two for all 169.
- The corrected order-40 state has lexicographic escape distance one.
- A different state on that same order-40 graph has exact escape
  distance three.  It has 93 legal first neighbors, of which 24 are
  safe and equal.  Exhausting all 2,196 legal arcs from those 24 states
  finds no lower or span-successful endpoint.  The third exchange of a
  literal path reaches profile minimum zero.

Thus radius two is false and no radius-three counterexample is known.
The precise surviving human proof obligation is:

> Given a positive state \(s\) with zero successful flags and no
> lower-\(\Psi\) or span-successful neighbour, prove that there are
> safe equal-\(\Psi\) reciprocal neighbors \(s',s''\) such that
> \(s''\) has a neighbor \(s'''\) with either
> \(\Psi(s''')<\Psi(s)\) or a successful span flag.

Equations (3)--(7) reduce this statement to exact circuit,
component-boundary, and outside-span data for the four length-three word
types `AAA`, `AAB`, `ABA`, and `ABC`.  What is missing is a
graph-order-independent argument that forces one favourable realization
of those data.  No current averaging or matroid-connectivity lemma
supplies it.

## AI-use disclosure

OpenAI Codex agents, directed by Atharva Vaidya, derived and checked
the multi-exchange formulas, classified the path skeletons, ran the
finite searches, found the order mismatch in the earlier order-40
artifact, found the exact radius-two counterexample, and drafted this
note.  The radius-two statement is false; the universal radius-three
statement remains unproved.
