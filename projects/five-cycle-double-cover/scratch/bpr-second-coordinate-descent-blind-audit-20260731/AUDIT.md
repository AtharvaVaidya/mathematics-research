# Adversarial audit of the second-coordinate descent frontier

Date: **2026-07-31**

Verdict: **THE STATED LOCAL LEMMAS AND CONDITIONAL THEOREM SURVIVE THE
AUDIT.  THE MISSING COORDINATION STEP IS REAL, SO THIS IS NOT BPR AND NOT A
FIVE-CYCLE-DOUBLE-COVER RESOLUTION.**

This is an independently implemented, AI-authored audit of
`bpr-second-coordinate-descent-20260731`.  The checker here imports no code
from that package and generates profiles by multiplicity vectors rather than
by its sorted-multiset routine.  This is not independent human peer review.

## 1. Setup checks

At a cubic vertex of a nowhere-zero \(\mathbb F_2^3\)-flow, the three
incident values are distinct: equality of two would force the third to be
zero.  Hence a fixed nonzero value class (M_b) is a matching.  If (J) is
the stated \(\partial M_b\)-join in (H=G-M_b), then
(F=M_b\mathbin{\dot\cup}J) is Eulerian.

For a residual component (Q) of (G-F), every cut edge belongs to (F),
and every non-(b) cut edge belongs to (J).  Thus

\[
 k_Q=|\delta_H(Q)|=|\delta_J(Q)|,
 \qquad d_Q=k_Q+q_Q.
\]

If (q_Q) is odd, the Eulerian cut parity makes (k_Q) odd, while the flow
cut equation gives

\[
 \bigoplus_{e\in\delta_H(Q)}f(e)=b. \tag{1}
\]

No (H)-edge has value (b), so (k_Q=1) is impossible.  This validates
the numerical domain used in the profile lemma.  Excluding the tight pair
((3,1)), the coordinatewise-minimal odd profiles are exactly ((3,3))
and ((5,1)).  This is only a statement about numerical profiles, as the
candidate note correctly says.

## 2. Partner-free directions and sharpness

The six nonzero values other than (b) split into three pairs
(\{u,u+b\}).  In the quotient by \(\langle b\rangle\), their images are
the three nonzero vectors (c_1,c_2,c_3\in\mathbb F_2^2), whose unique
nontrivial relation is

\[
 c_1+c_2+c_3=0.
\]

If (n_i) is the total multiplicity in pair (i), projecting (1) says the
three parities (n_i\bmod2) are equal.  Since (k_Q=n_1+n_2+n_3) is odd,
all three are odd.  If no occurring direction were partner-free, both
members of every pair would occur.  Each odd (n_i) would then be at least
three, forcing (k_Q\ge9).  This proves the claimed result for
(k_Q=3,5,7).  At (k_Q=3), all three pair totals equal one, so every
occurring direction is partner-free.

The example for (b=1),

\[
 2,2,3,4,4,5,6,6,7,
\]

has xor one and contains both members of each of the pairs
(\{2,3\},\{4,5\},\{6,7\}).  Thus nine is sharp for the
**partner-free criterion**.  It is not a counterexample to the existence of
some other useful switch at size nine, and the source package does not claim
that stronger conclusion.

The independent multiplicity-vector enumeration obtained the following
counts per fixed target (b):

| (k) | admissible profiles | no partner-free direction |
|---:|---:|---:|
| 3 | 4 | 0 |
| 5 | 24 | 0 |
| 7 | 84 | 0 |
| 9 | 224 | 4 |

Multiplying by the seven target values gives exactly
(28,168,588,1568) admissible profiles and (0,0,0,28) failures,
matching the candidate package.

## 3. The nonzero cycle-space functional

Fix a partner-free occurring value (t), put

\[
 P_t=M_b\cup M_{b+t},\qquad L=G-M_t,
\]

and set (S=\delta_{M_b}(Q)).  Partner-freeness is used at one exact point:
there is no (b+t) edge on the (H)-cut of (Q), so

\[
 P_t\cap\delta_G(Q)=S. \tag{2}
\]

Because (t\ne b), every edge of (S) remains in (L).  Suppose the
functional (X\mapsto|X\cap S|\bmod2) vanished on the binary cycle space
of (L).  Binary cycle/cut orthogonality would give a shore (W) with

\[
 \delta_L(W)=S.
\]

The edges removed from (L) all have value (t).  Consequently the full
cut \(\delta_G(W)\) consists of the odd number (q_Q) of (b)-edges in
(S), plus some number of (t)-edges.  Its flow xor is therefore (b) or
(b+t), both nonzero.  This contradicts the flow cut equation.  The
functional is nonzero.

Any nonzero witness in the cycle space is a legal binary (t)-switch:
it is Eulerian, and it contains no edge initially valued (t), so adding
(t) creates no zero edge.  If “cycle” is intended to mean one circuit
rather than an arbitrary Eulerian support, decompose the witness into
circuits; an odd total intersection with (S) leaves at least one circuit
with odd intersection.  Thus no connectivity assumption on the witness is
hidden here.

The independent checker verified cycle/cut orthogonality for every simple
graph on at most five labelled vertices (1,099 graphs) and tested all
59,809 edge-set functionals.  It also checked all 84 possible
((b,t,\text{parity of the }t\text{-edges})) cut-xor cases.  These finite
checks are cross-checks; the preceding argument is the human proof.

The conclusion is exactly that the **old shore** (Q) has even target-cut
parity after the switch, independently of which new join is later chosen.
It does not prevent a proper subshore, a supershore, or a crossing shore
from becoming a new odd or tight residual component.

## 4. Exact hypotheses and proof of Theorem 4.1

The conditional descent needs all of the following hypotheses:

1. the base graph and flow setup above;
2. an old join (J) for which the first coordinate of \(\Psi(M,J)\) is
   zero;
3. an old odd residual component (Q);
4. a legal (t)-switch support (X\subseteq G-M_t);
5. the **all-in** condition
   (D^+=X\cap M_{b+t}\subseteq J);
6. odd switch effect on (Q);
7. even switch effect on every old terminal-even component; and
8. the integer inequality (q'_C\ge q_C) for every old odd component
   whose switch effect is even.

The global statement additionally requires that (J) realize
\(\Psi^*(M)\).

The all-in condition is what permits the fixed-(F) argument.  It gives

\[
 M'\subseteq F,qquad J'=F-M'
 =(J-D^+)\mathbin{\dot\cup}D^-.
\]

Thus (J') is a valid new join, (F) stays fixed, and the residual
components and their total cut sizes (d_C) stay fixed.  Without all-in,
(M') can contain an edge outside (F); neither the displayed formula for
(J') nor the fixed-shore comparison follows.

Condition 7 ensures that every new odd fixed residual component was already
old odd.  Since the old first coordinate is zero, an old odd component has
(d_C\ne4).  Fixed (d_C) then prevents every new odd component from being
tight.  Condition 6 removes (Q)'s positive (k_Q) summand.  Any other old
odd component with odd effect is also removed.  For every old odd component
that remains odd, condition 8 gives

\[
 k'_C=d_C-q'_C\le d_C-q_C=k_C.
\]

The first coordinate therefore remains zero and the second decreases
strictly.  If (J) was globally optimal, the candidate (J') gives
\(\Psi^*(M')\le\Psi(M',J')<\Psi^*(M)\).

The phrase “exact sufficient condition” should not be read as a necessary
and sufficient characterization.  The displayed assumptions are sufficient
and the arithmetic under fixed (F) is exact; their universal attainability
is not proved.

The independent checker exhaustively verified 49,920 two-component
arithmetic instances through total cut size fourteen satisfying these
hypotheses.  Component contributions are separable, so this directly checks
the only inequalities used in the proof.

## 5. Why parity protection is not integer protection

Condition 8 is essential.  Consider the abstract fixed-component profiles
((d,q))

\[
 \text{old: }(6,3)\mid(8,5),qquad
 \text{new: }(6,2)\mid(8,1).
\]

The selected first component changes from odd to even.  The second remains
odd—its parity is protected—but its (q)-value falls by four.  The old
second coordinate is (3+3=6), while the new one is (8-1=7).  Parity
protection alone therefore allows the potential to increase.

Condition 7 is separately essential.  In

\[
 \text{old: }(6,3)\mid(4,2),qquad
 \text{new: }(6,2)\mid(4,1),
\]

the selected odd component disappears, but the unprotected old even
four-cut becomes a new tight component.  The potential moves from
((0,3)) to ((1,3)), which is lexicographically worse.

These are arithmetic counterprofiles to weakened arguments, not asserted
graph realizations and not counterexamples to Theorem 4.1.

## 6. The coordination obstruction remains open

The partner-free functional is proved nonzero on
(Z_1(G-M_t;\mathbb F_2)).  The all-in requirement restricts the search to

\[
 Z_1\bigl(G-(M_t\cup(M_{b+t}-J));\mathbb F_2\bigr),
\]

on which the same functional may vanish.  For the selected shore and all
old even shores, the parity equations are a binary linear system on this
smaller cycle space.  The source's obstruction (22) is the standard exact
dual certificate: infeasibility occurs precisely when the selected row,
xored with some protected-even rows, annihilates the cycle space, equivalently
belongs to its cut space.  The checker independently verified 299,593 such
binary systems through six free variables.

Even feasibility of those parity equations does not imply the signed
integer inequalities in condition 8.  Conversely, abandoning fixed (F)
and globally rerouting may alter the residual component shores, so the old
componentwise (d_C-q_C) comparison no longer controls which new shores are
odd or tight.  These are two distinct unresolved coordination problems.

Theorem 3.1 therefore cannot simply be fed into Theorem 4.1: it does not
guarantee all-in, protection of old even shores, or favorable integer gains.
The candidate package states this limitation accurately.

## 7. Reproduction and scope

Run:

```sh
python3 -B independent_checker.py
shasum -a 256 -c SHA256SUMS
```

No hidden assumption invalidating the stated conditional results was found.
No complete descent theorem, BPR proof, BPR counterexample, or FiveCDC
resolution follows.  All code and prose in this audit package were produced
by OpenAI Codex under human direction and have not received independent
human peer review.
