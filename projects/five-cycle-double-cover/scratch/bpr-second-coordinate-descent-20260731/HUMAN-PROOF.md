# The larger-blocker switch lemma and the exact second-coordinate gate

Date: **2026-07-31**

Status: **UNCONDITIONAL SINGLE-SHORE PARITY KILL / CONDITIONAL GLOBAL
LEXICOGRAPHIC DESCENT / COORDINATION STEP OPEN / NOT BPR / NOT FIVECDC**.

## 1. Setup

Let \(G\) be a finite loopless cubic graph and let

\[
 f:E(G)\longrightarrow \mathbb F_2^3-\{0\}
\]

be a nowhere-zero flow.  Fix \(b\ne0\), put

\[
 M=M_b=f^{-1}(b),\qquad H=G-M,\qquad T=\partial M,
\]

and let \(J\subseteq H\) be a \(T\)-join.  Set

\[
 F=M\mathbin{\dot\cup}J.
\tag{1}
\]

Then \(F\) is Eulerian and the residual graph is
\(G-F=(G-M)-J\).  For a component \(Q\) of \(G-F\), write

\[
 k_Q=|\delta_H(Q)|=|\delta_J(Q)|,
 \qquad q_Q=|\delta_M(Q)|,
 \qquad d_Q=k_Q+q_Q.
\tag{2}
\]

The component is canonical odd when \(q_Q\) is odd.  In that case
\(k_Q\) is also odd.  Every \(H\)-cut edge lies in \(J\), and XORing
the flow equations over \(Q\) gives

\[
 \bigoplus_{e\in\delta_H(Q)} f(e)=b.
\tag{3}
\]

In particular \(k_Q\ge3\).  The case \((k_Q,q_Q)=(3,1)\) is the tight
case.  The coordinatewise-minimal non-tight odd profiles are precisely

\[
 \boxed{(k_Q,q_Q)=(3,3)\quad\hbox{and}\quad(5,1).}
\tag{4}
\]

Indeed, if \(k_Q=3\), non-tightness forces \(q_Q\ge3\); if
\(k_Q\ge5\), the minimum possible odd value of \(q_Q\) is one.
Every other non-tight odd profile dominates one of the two profiles in
(4).  This is a classification of minimal numerical profiles, not a
claim that an arbitrary larger blocker has one of the two exact pairs.

## 2. Partner-free directions below nine

For fixed \(b\), the six possible \(H\)-cut values form three pairs

\[
 \{u,u+b\}.
\tag{5}
\]

Call an occurring cut value \(t\) **partner-free** if \(b+t\) does not
occur on the same \(H\)-cut.

**Lemma 2.1 (partner-free direction).**  If \(k_Q\in\{3,5,7\}\), then
the \(H\)-cut of \(Q\) has a partner-free occurring value.  When
\(k_Q=3\), every occurring value is partner-free.

**Proof.**  Quotient \(\mathbb F_2^3\) by \(\langle b\rangle\).  The
three pairs in (5) map to the three nonzero elements
\(c_1,c_2,c_3\) of \(\mathbb F_2^2\), where
\(c_1+c_2+c_3=0\).  Let \(n_i\) count cut values in the \(i\)-th pair.
Equation (3) projects to

\[
 (n_1\bmod2)c_1+(n_2\bmod2)c_2+(n_3\bmod2)c_3=0.
\tag{6}
\]

The three parities in (6) are therefore equal.  Their sum
\(k_Q\) is odd, so all three are odd.  If no occurring value were
partner-free, then both values in every occupied pair would occur.
Each \(n_i\) would consequently be an odd integer at least three, so
\(k_Q\ge9\), a contradiction.

For \(k_Q=3\), suppose both members \(t,b+t\) of one pair occurred.
Their XOR is \(b\), so (3) would force the third value to be zero.
Thus no occurring value has its partner. \(\square\)

The bound is sharp.  With \(b=1\), the nine-value multiset

\[
 2,2,3,\ 4,4,5,\ 6,6,7
\tag{7}
\]

has XOR one and contains both members of each partner pair.  Thus this
argument does not select a direction for a general blocker with
\(k_Q\ge9\).

## 3. Every partner-free direction has a legal parity-killing cycle

Fix a partner-free value \(t\) occurring on \(\delta_H(Q)\), and put

\[
 P_t=M_b\cup M_{b+t},\qquad L=G-M_t.
\tag{8}
\]

Because no \(H\)-cut edge has value \(b+t\),

\[
 P_t\cap\delta_G(Q)=\delta_M(Q)=:S.
\tag{9}
\]

On the binary cycle space \(Z_1(L;\mathbb F_2)\), consider

\[
 \epsilon_Q(X)=|X\cap S|\pmod2.
\tag{10}
\]

**Theorem 3.1 (single-shore parity kill).**  The functional
\(\epsilon_Q\) is nonzero on \(Z_1(L;\mathbb F_2)\).  Hence there is a
legal binary \(t\)-switch support \(X\subseteq G-M_t\) with
\(\epsilon_Q(X)=1\).

**Proof.**  Suppose \(\epsilon_Q\) vanished on the cycle space.  The
orthogonal complement of the binary cycle space is the cut space, so
there would be a shore \(W\subseteq V(G)\) with

\[
 \delta_L(W)=S.
\tag{11}
\]

The full cut \(\delta_G(W)\) would then consist of the \(q_Q\) edges
of \(S\), all of value \(b\), and some edges of value \(t\).  Since
\(q_Q\) is odd, the XOR of its flow values would be either \(b\) or
\(b+t\), according to the parity of the number of \(t\)-edges.  Both
are nonzero because \(b\) and \(t\) are distinct nonzero vectors.  This
contradicts the flow cut equation. \(\square\)

Switching the flow by \(t\) on \(X\) replaces the target matching by

\[
 M'=(M-D^-)\mathbin{\dot\cup}D^+,
 \quad D^-=X\cap M_b,
 \quad D^+=X\cap M_{b+t}.
\tag{12}
\]

Equations (9)--(10) give

\[
 |\delta_{M'}(Q)|\equiv q_Q+\epsilon_Q(X)\equiv0\pmod2.
\tag{13}
\]

This conclusion is independent of the new join.  Under every global
rerouting after the switch, the *old shore* \(Q\) is terminal-even and
therefore cannot itself be a new canonical odd component or a tight
component.  New odd components on different shores are not excluded.

For the two minimal profiles in (4), Theorem 3.1 always applies.  It
also applies to every blocker with \(k_Q=7\).  No girth or cyclic
connectivity hypothesis is used.

## 4. An exact sufficient condition for lexicographic descent

Recall the sharp potential

\[
 \Psi(M,J)=\left(
 \#\{C:C\text{ is tight}\},
 \sum_{C:q_C\text{ odd}} k_C
 \right).
\tag{14}
\]

Suppose the first coordinate is zero.  Let \(Q\) be an odd component,
choose a direction \(t\), and let \(X\) be a legal switch satisfying

\[
 D^+\subseteq J.
\tag{15}
\]

Then \(M'\subseteq F\), so

\[
 J'=F-M'=(J-D^+)\mathbin{\dot\cup}D^-
\tag{16}
\]

is a valid new join.  The Eulerian set \(F\), the residual graph
\(G-F\), every residual component, and every \(d_C\) remain fixed.  Put

\[
 q'_C=q_C-|D^-\cap\delta(C)|+|D^+\cap\delta(C)|,
 \qquad k'_C=d_C-q'_C,
\tag{17}
\]

and let \(\epsilon_C(X)\equiv q'_C-q_C\pmod2\).

**Theorem 4.1 (fixed-Eulerian-set second-coordinate descent).**  Assume
in addition that

1. \(\epsilon_Q(X)=1\);
2. \(\epsilon_C(X)=0\) for every old terminal-even component \(C\); and
3. \(q'_C\ge q_C\) for every old odd component \(C\) with
   \(\epsilon_C(X)=0\).

Then

\[
 \Psi(M',J')<_{\rm lex}\Psi(M,J).
\tag{18}
\]

If \(J\) realizes the globally optimized value \(\Psi^*(M)\), then
global reoptimization after the switch gives the strict descent

\[
 \Psi^*(M')\le\Psi(M',J')<_{\rm lex}\Psi^*(M).
\tag{19}
\]

**Proof.**  Condition 2 says that every new odd component was already
old odd.  Since the old first coordinate is zero, every old odd
component has \(d_C\ne4\); the fixed value of \(d_C\) therefore prevents
every new odd component from being tight.

Condition 1 removes \(Q\) from the odd-component sum.  Any other old
odd component with odd switch effect is also removed.  For every old
odd component which remains odd, condition 3 and (17) give
\(k'_C\le k_C\).  Thus the first coordinate stays zero while the second
coordinate loses at least the positive summand \(k_Q\) and gains
nothing.  This proves (18), and (19) follows because \(J'\) is one
admissible choice in the global new-join minimization. \(\square\)

The integer inequalities in condition 3 are essential.  Merely keeping
the parity of another odd component fixed does not keep its summand
\(k_C=d_C-q_C\) fixed: a switch may reduce \(q_C\) by an even amount and
thereby increase \(k_C\).

## 5. The remaining coordination obstruction

The unconditional cycle from Theorem 3.1 need not satisfy the all-in
condition (15).  The all-in cycle space is

\[
 Z_1(L_t;\mathbb F_2),\qquad
 L_t=G-\bigl(M_t\cup(M_{b+t}-J)\bigr).
\tag{20}
\]

On this smaller space, even the single equation
\(\epsilon_Q(X)=1\) can fail.  It is feasible exactly when the vector
\(S=\delta_M(Q)\) is not in the cut space of \(L_t\).

More generally, impose the parity part of Theorem 4.1:

\[
 \epsilon_Q(X)=1,
 \qquad \epsilon_C(X)=0
 \quad(C\text{ old terminal-even}).
\tag{21}
\]

Writing
\(a_C=P_t\cap E(L_t)\cap\delta_G(C)\), system (21) is infeasible if
and only if there is a subfamily \(\mathcal I\) of the old even
components such that

\[
 a_Q\mathbin{\triangle}
 \mathop{\triangle}_{C\in\mathcal I}a_C
 \quad\hbox{belongs to the cut space of }L_t.
\tag{22}
\]

This is the exact binary coordination obstruction.  Even when (21) is
feasible, the signed integer gains in condition 3 remain to be
controlled.  Allowing the unrestricted global reroutes from the
preceding package can improve on the fixed-\(F\) candidate (16), but no
argument presently prevents those reroutes from creating new odd or
tight components on other shores.

Consequently Theorem 3.1 closes the local existence question for every
minimal larger blocker, but it does **not** prove a universal
high-girth descent lemma.  The unresolved step is simultaneous global
coordination, not the existence of a cycle that flips a selected
minimal shore.

## 6. Scope of the non-Tait high-girth check

The existing 30,450-vertex candidate-domain graph is independently
certified simple, connected, cubic, bridgeless, non-Tait (oddness at
least eight), and of girth exactly ten.  Its retained result explicitly
does **not** claim or certify cyclic edge connectivity, and the graph
has a checked standard FiveCDC.  It therefore cannot be cited as the
requested certified cyclically-4 counterexample to second-coordinate
descent.

Separate searches of Petersen 13-lifts found no non-Tait girth-ten
cyclically-4 host in the tested samples.  The available order-80
larger-blocker realization is Tait-colourable and is excluded as a BPR
witness.  No certified non-Tait, girth-at-least-ten, cyclically-4
counterexample to the descent statement was found in this branch.

## 7. What is proved

The human-checkable results of this note are:

1. the minimal larger profiles are \((3,3)\) and \((5,1)\);
2. every odd blocker with \(k_Q<9\) has a partner-free direction, with
   the bound nine sharp;
3. every partner-free direction admits a legal cycle that makes the
   selected old shore terminal-even, independently of global rerouting;
4. Theorem 4.1 gives an exact sufficient condition for strict descent
   of the globally reoptimized lexicographic potential; and
5. (22) isolates the parity part of the remaining all-in coordination
   obstruction.

No universal descent theorem, BPR theorem, FiveCDC proof, or FiveCDC
counterexample is claimed.
