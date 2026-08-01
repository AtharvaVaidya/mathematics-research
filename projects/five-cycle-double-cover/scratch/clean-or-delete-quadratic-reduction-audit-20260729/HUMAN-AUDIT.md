# Independent audit of the quadratic clean-or-delete reduction

Date: 2026-07-29

Status: **PROPOSITIONS 1--5 PASS AT THEIR STATED SCOPE / SINGLE-WITNESS
NEUTRALIZATION ONLY / NO GLOBAL CLEANLINESS IMPLICATION / NOT A
FIVECDC RESOLUTION**.

## Proposition 1

For \(K=\mathbb F_2^2\), the colour indicator expands as
\[
 {\bf1}_{x=\gamma}
 =(1+x_1+\gamma_1)(1+x_2+\gamma_2).
\]
Adding this expression at the two sides of a transition leaves the
quadratic term plus two linear multiples of the transition.  Summing
over one component block kills those linear multiples because the
block transition xor is zero.  Hence all four cut-colour parities are
equal to the displayed quadratic obstruction \(Q_a\).

The separate assertion that \(\sum q(L_ad_i)\) is independent of
\(L_a\) is also valid: every invertible two-dimensional binary map
preserves the alternating polar form, so \(q\circ L+q\) is linear and
vanishes after block charge is applied.

## Proposition 2 and Corollary 3

Translating one circuit by \(z_j\) changes a vertex summand by
\[
 B(z_j,r_{i-1}+r_i)=B(z_j,t_i).
\]
This gives exactly \(B(z_j,T_{a,j})\).  The xor of the \(T_{a,j}\)
over all circuits is zero, so fixing one common translation loses no
solutions.

The dual statement is the ordinary binary Fredholm alternative.
Nondegeneracy of \(B\) converts a zero sum of selected coefficient
functionals into
\[
                 \bigoplus_{a\in S}T_{a,j}=0
\]
on every circuit.  Requiring every circuit is equivalent to requiring
all but the gauged circuit because their xor is zero.

## Proposition 4

If a circuit omits \(\mu\), translating its low values by \(\mu\)
makes every one nonzero.  Removing that circuit from the first binary
support leaves full values \((0,r_i+\mu)\ne0\); transition equations
and all other nonzero values are unchanged.  This is a literal,
strictly smaller extendable projection.

## Proposition 5

Let \(S\) satisfy the coefficient-balance part of the dual condition.
Left-composing all selected block maps by one \(U\) changes the
transition xor on each circuit by
\[
 (U+I)\bigoplus_{\pi_i\in S}t_i=0.
\]
The switch is therefore integrable.  The selected balance also
persists afterward because \(T'_{a,j}=UT_{a,j}\) for \(a\in S\).

The checker independently constructs all six elements of
\(\operatorname{GL}(2,2)\).  For every one of the 16 pairs
\((r,a)\in K^2\), it verifies that the sum over the identity and the
two order-three maps equals the sum over the three involutions and
equals
\[
                      q(r+a)+{\bf1}_{a\ne0}.
\]

It then independently enumerates every nonzero transition word through
length eight whose total xor is zero, and every selected-position word
whose selected transition xor is zero.  For all 126,258 balanced rows,
both three-map identities hold.

The run cancellation is sound: \(b_i=r_i+a_i\) is constant across a
selected run, while \(a_i\) is constant across an unselected run.
The two boundary edges of each cyclic run therefore contribute equal
terms, which cancel in characteristic two.  Empty and full selected
sets have no cut edges and are included.

Thus, if the current witness has obstruction bit one, some legal
common switch makes that same witness's bit zero.

## Exact non-implication

This does **not** prove that all dual witnesses can be neutralized
simultaneously.  Switching on \(S\) changes the obstruction vector and
can change coefficient vectors involved in other dual relations.
Another witness may remain or appear.  No termination measure,
monotonicity statement, global clean assignment, arbitrary-degree
reduction, or FiveCDC resolution follows from Proposition 5.

One expositional clarification would help the source note: invariance
of \(F_S\) under arbitrary per-circuit translations follows directly
from Proposition 2 and the balance of \(S\), and should be stated
explicitly.

OpenAI Codex agents under human direction performed this independent
audit, wrote the checker, and prepared this note.  The result awaits
independent human review.
