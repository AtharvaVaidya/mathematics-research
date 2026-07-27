# Root avoidance by an unmarked circuit toggle

Date: **2026-07-27**.

Status: **HUMAN-CHECKABLE ROOT-TOGGLE LEMMA / MULTI-CONTACT
OBSTRUCTION ISOLATED / ROOTED THEOREM STILL OPEN**.

This note gives a short exact reduction for the standard rooted
four-mark problem.  The common-colour Tait colouring always supplies a
mark-free factor circuit through the forbidden root.  Symmetric
difference with that circuit removes the root from any unrooted
certificate.  The operation preserves componentwise marked parity
unless the factor circuit has two separated contacts with one
certificate component.

Thus a rooted failure is not merely a failure of affine trace
feasibility.  It forces a concrete **multi-contact obstruction** between
every usable unrooted certificate and every mark-free root circuit.
The lemma does not by itself exclude that obstruction.

## 1. Setup

Let \(L\) be a finite simple cubic graph, let
\[
                         S=\{s_1,s_2,s_3,s_4\}
\]
be a four-edge matching, and let \(f\in E(L)\setminus S\).
A **closed certificate** is a binary cycle \(Q\subseteq E(L)\) which
contains \(S\) and has an even number of marked edges on every circuit
component.  It is **rooted** when \(f\notin Q\).

Assume that \(L\) has a Tait colouring in which all members of \(S\)
have one common colour \(c\), while \(f\) has a different colour \(a\).
Write \(b\) for the third colour.  The \(ab\)-factor circuit through
\(f\), denoted \(C_f\), contains no member of \(S\).

The sharpened theorem in `four-mark-core-closure.md` says that the
marked cyclic-cut inequality already supplies a closed certificate
\(Q\).  If \(f\notin Q\), the rooted problem is finished.  The only
case considered below is \(f\in Q\).

We may delete every unmarked component of \(Q\).  If the component
containing \(f\) were deleted, this would itself produce a rooted
certificate.  Hence in a surviving case every component of \(Q\)
contains two or four marks.

## 2. The toggle lemma

For two subgraphs, intersection below means edge intersection.  In a
subcubic graph, two distinct circuits which meet at a vertex share an
edge: each uses two of at most three incident edges.  Consequently a
connected nonempty intersection of two distinct circuits is a path.

> **Unmarked root-toggle lemma.**  Let \(Q\) be a closed certificate
> containing \(f\), with no unmarked component.  Let \(C\) be a circuit
> such that
> \[
>                         f\in C,\qquad C\cap S=\varnothing.
>                                                               \tag{1}
> \]
> Suppose that, for every circuit component \(Q_i\) of \(Q\), the
> intersection \(C\cap Q_i\) is empty or connected.  Then
> \[
>                              Q'=Q\mathbin\triangle C             \tag{2}
> \]
> is a closed rooted certificate.

### Proof

Both \(Q\) and \(C\) are even subgraphs, so \(Q'\) is a binary cycle.
Condition (1) says that symmetric difference changes no marked edge,
and hence \(S\subseteq Q'\).  Since both \(Q\) and \(C\) contain \(f\),
equation (2) excludes \(f\).

It remains to check marked parity component by component.  Components
of \(Q\) disjoint from \(C\) survive unchanged.  Let
\[
                         Q_1,\ldots,Q_r
\]
be the components met by \(C\).  For each \(i\), the intersection is a
nonempty path \(P_i\).  It cannot be all of \(Q_i\): the component
\(Q_i\) contains a mark, while \(C\) contains none.  Therefore
\(Q_i-P_i\) is the complementary path between the two ends of \(P_i\).

Traverse \(C\) cyclically.  Its paths outside
\(P_1\cup\cdots\cup P_r\), together with the complementary paths
\(Q_i-P_i\), form one circuit.  This is exactly the part of
\(Q\triangle C\) obtained from the met components.  It contains the
marks formerly contained in \(Q_1,\ldots,Q_r\), whose total number is
even because every \(Q_i\) was marked-even.  All untouched components
also remain marked-even.  Thus every component of \(Q'\) has even
marked parity. \(\square\)

The proof also covers \(r=1\): two circuits with one common path are
spliced into their one symmetric-difference circuit.  When \(r>1\),
the same traversal merges the \(r\) certificate components rather than
splitting any one of them.

## 3. Exact obstruction forced by rooted failure

Apply the lemma to the common-colour \(ab\)-factor circuit \(C_f\).

> **Multi-contact corollary.**  If the standard rooted assertion fails,
> then every closed certificate \(Q\) containing \(f\), after deletion
> of its unmarked components, has a component \(Q_i\) for which
> \[
>                   C_f\cap Q_i
> \quad\text{has at least two connected components}.             \tag{3}
> \]

More generally, (3) holds with \(C_f\) replaced by every mark-free
circuit through \(f\).  Otherwise the unmarked root-toggle lemma gives
a rooted certificate.

This is stronger than saying merely that a root-avoiding all-mark
binary cycle might have odd marked components.  It identifies the
only way in which the already proved unrooted certificate can resist
the canonical mark-free factor toggle.

## 4. Relation to the remaining \(2+1+1\) atom

At a forced one-mark three-edge shore, the two separated contacts in
(3) project to the same repeated-boundary phenomenon seen in the
marked-borrower packet:
\[
                         D_{ij},\quad R_k,\quad R_l .
\]
If the contact with each certificate component were one path, the
toggle lemma would close the root immediately.  Hence any genuine
rooted cap-avoidance atom must realize both:

1. the odd-\(K_{2,3}\) graft-minor obstruction from
   `rooted-four-mark-odd-k23-reduction.md`; and
2. the multi-contact obstruction (3).

This conjunction is a sound additional filter for structural
normalization and finite searches.  It is not yet a proof that such a
graph cannot exist.  In particular, multiple common paths can split a
two-mark or four-mark certificate component into odd-marked circuits
after the toggle.

## AI-use disclosure

OpenAI Codex agents, under human direction, identified the symmetric-
difference reduction, checked its subcubic intersection cases, and
wrote this note.  The proof is displayed in full for line-by-line human
verification.  No finite computation is used in the lemma, and no
resolution of the Five-Cycle Double Cover Conjecture is claimed.
